"""
SwarmForge Swarm — orchestrate multiple agents working together.
"""
from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Optional

from swarmforge.core.agent import Agent, AgentConfig, AgentRole
from swarmforge.core.handoff import (
    HandoffProtocol, HandoffStrategy,
    HandoffContext, HandoffResult,
)
from swarmforge.core.tool import ToolRegistry


class SwarmTopology(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    MESH = "mesh"
    BROADCAST = "broadcast"


@dataclass
class SwarmConfig:
    name: str
    topology: SwarmTopology = SwarmTopology.PARALLEL
    handoff_strategy: HandoffStrategy = HandoffStrategy.CAPABILITY_MATCH
    max_concurrent_agents: int = 10
    global_timeout_seconds: int = 600
    retry_on_failure: bool = True
    max_retries: int = 3


@dataclass
class SwarmRun:
    id: str
    swarm_name: str
    task: str
    topology: str
    started_at: float
    finished_at: Optional[float] = None
    status: str = "running"
    results: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class Swarm:
    """Orchestrates multiple agents as a coordinated swarm."""

    def __init__(
        self,
        config: SwarmConfig,
        tool_registry: Optional[ToolRegistry] = None,
    ):
        self.config = config
        self.id = str(uuid.uuid4())[:8]
        self.agents: Dict[str, Agent] = {}
        self.handoff = HandoffProtocol(strategy=config.handoff_strategy)
        self.tool_registry = tool_registry or ToolRegistry()
        self._runs: List[SwarmRun] = []
        self._semaphore = asyncio.Semaphore(config.max_concurrent_agents)

    def add_agent(self, agent: Agent) -> None:
        self.agents[agent.config.name] = agent
        self.handoff.register_capabilities(agent.config.name, agent.config.capabilities)

    def remove_agent(self, name: str) -> None:
        self.agents.pop(name, None)

    def get_agent(self, name: str) -> Optional[Agent]:
        return self.agents.get(name)

    async def run(self, task: str, context: Optional[Dict] = None) -> SwarmRun:
        """Execute a task across the swarm."""
        run = SwarmRun(
            id=str(uuid.uuid4()),
            swarm_name=self.config.name,
            task=task,
            topology=self.config.topology.value,
            started_at=time.time(),
        )
        self._runs.append(run)

        try:
            if self.config.topology == SwarmTopology.SEQUENTIAL:
                results = await self._run_sequential(task, context)
            elif self.config.topology == SwarmTopology.PARALLEL:
                results = await self._run_parallel(task, context)
            elif self.config.topology == SwarmTopology.HIERARCHICAL:
                results = await self._run_hierarchical(task, context)
            elif self.config.topology == SwarmTopology.BROADCAST:
                results = await self._run_broadcast(task, context)
            else:
                results = await self._run_parallel(task, context)

            run.results = results
            run.status = "completed"
        except Exception as e:
            run.errors.append(str(e))
            run.status = "failed"
        finally:
            run.finished_at = time.time()

        return run

    async def run_streaming(self, task: str) -> AsyncIterator[Dict[str, Any]]:
        """Execute with streaming progress updates."""
        yield {"type": "swarm_start", "swarm": self.config.name, "task": task}

        run = SwarmRun(
            id=str(uuid.uuid4()),
            swarm_name=self.config.name,
            task=task,
            topology=self.config.topology.value,
            started_at=time.time(),
        )

        try:
            agents_list = list(self.agents.values())
            if not agents_list:
                yield {"type": "error", "message": "No agents in swarm"}
                return

            # Assign sub-tasks
            sub_tasks = self._decompose_task(task, len(agents_list))
            tasks_coros = []

            for i, agent in enumerate(agents_list):
                sub_task = sub_tasks[i] if i < len(sub_tasks) else task
                tasks_coros.append(self._run_agent_with_semaphore(agent, sub_task))

            yield {"type": "dispatch", "agents": [a.config.name for a in agents_list]}

            results = await asyncio.gather(*tasks_coros, return_exceptions=True)

            for i, r in enumerate(results):
                agent_name = agents_list[i].config.name
                if isinstance(r, Exception):
                    yield {"type": "agent_error", "agent": agent_name, "error": str(r)}
                else:
                    yield {"type": "agent_done", "agent": agent_name, "result": r}

            run.results = [r for r in results if not isinstance(r, Exception)]
            run.status = "completed"
            yield {"type": "swarm_done", "swarm": self.config.name}

        except Exception as e:
            run.errors.append(str(e))
            run.status = "failed"
            yield {"type": "swarm_error", "error": str(e)}

    async def _run_sequential(self, task: str, context: Optional[Dict]) -> List[Dict]:
        results = []
        carry_context = context or {}
        for agent in self.agents.values():
            result = await agent.run(task, carry_context)
            results.append(result)
            carry_context["previous_result"] = result
        return results

    async def _run_parallel(self, task: str, context: Optional[Dict]) -> List[Dict]:
        agents_list = list(self.agents.values())
        sub_tasks = self._decompose_task(task, len(agents_list))
        tasks_coros = [
            self._run_agent_with_semaphore(agent, sub_tasks[i] if i < len(sub_tasks) else task)
            for i, agent in enumerate(agents_list)
        ]
        results = await asyncio.gather(*tasks_coros, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]

    async def _run_hierarchical(self, task: str, context: Optional[Dict]) -> List[Dict]:
        orchestrators = [
            a for a in self.agents.values()
            if a.config.role == AgentRole.ORCHESTRATOR
        ]
        workers = [
            a for a in self.agents.values()
            if a.config.role != AgentRole.ORCHESTRATOR
        ]

        if not orchestrators:
            return await self._run_parallel(task, context)

        orch = orchestrators[0]
        plan = await orch.run(f"Plan the following task: {task}", context)
        sub_tasks = self._decompose_task(task, len(workers))

        worker_results = await asyncio.gather(*[
            self._run_agent_with_semaphore(w, st)
            for w, st in zip(workers, sub_tasks)
        ])

        summary = await orch.run(
            f"Synthesize these results: {worker_results}",
            context,
        )
        return [plan, summary] + list(worker_results)

    async def _run_broadcast(self, task: str, context: Optional[Dict]) -> List[Dict]:
        results = await asyncio.gather(*[
            self._run_agent_with_semaphore(a, task)
            for a in self.agents.values()
        ])
        # Synthesize with first agent
        if self.agents:
            first = list(self.agents.values())[0]
            synthesis = await first.run(
                f"Synthesize and deduplicate these results: {results}",
                context,
            )
            results = [synthesis] + list(results)
        return results

    async def _run_agent_with_semaphore(self, agent: Agent, task: str) -> Dict:
        async with self._semaphore:
            return await agent.run(task)

    def _decompose_task(self, task: str, n_agents: int) -> List[str]:
        """Decompose a task into sub-tasks for parallel execution."""
        if n_agents <= 1:
            return [task]
        return [f"[Sub-task {i+1}/{n_agents}] {task}" for i in range(n_agents)]

    def get_stats(self) -> Dict[str, Any]:
        return {
            "swarm_id": self.id,
            "name": self.config.name,
            "topology": self.config.topology.value,
            "agent_count": len(self.agents),
            "total_runs": len(self._runs),
            "agent_stats": {name: agent.get_stats() for name, agent in self.agents.items()},
        }

    def get_runs(self, limit: int = 50) -> List[SwarmRun]:
        return self._runs[-limit:]

    def __repr__(self) -> str:
        return f"Swarm({self.config.name}, {len(self.agents)} agents, {self.config.topology.value})"
