"""Workflow engine — multi-step task orchestration with DAG support."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import asyncio
import time

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class WorkflowStep:
    name: str
    agent_name: str
    task_template: str
    depends_on: List[str] = field(default_factory=list)
    condition: Optional[str] = None
    timeout_seconds: int = 300
    retry_count: int = 0
    status: StepStatus = StepStatus.PENDING
    result: Any = None

@dataclass
class WorkflowDefinition:
    name: str
    description: str = ""
    steps: List[WorkflowStep] = field(default_factory=list)
    max_parallel: int = 5
    global_timeout: int = 3600

class WorkflowEngine:
    def __init__(self, swarm=None):
        self.swarm = swarm
    async def execute(self, workflow: WorkflowDefinition, inputs: Dict = None) -> Dict:
        results = {}
        errors = []
        semaphore = asyncio.Semaphore(workflow.max_parallel)
        async def run_step(step: WorkflowStep):
            async with semaphore:
                for dep in step.depends_on:
                    while dep not in results:
                        await asyncio.sleep(0.5)
                step.status = StepStatus.RUNNING
                try:
                    if self.swarm:
                        agent = self.swarm.get_agent(step.agent_name)
                        if agent:
                            task = step.task_template.format(**(inputs or {}), **(results or {}))
                            r = await asyncio.wait_for(agent.run(task), timeout=step.timeout_seconds)
                            step.result = r
                            step.status = StepStatus.COMPLETED
                            results[step.name] = r
                        else:
                            raise ValueError(f"Agent {step.agent_name} not found")
                    else:
                        step.status = StepStatus.COMPLETED
                        results[step.name] = {"status": "mock"}
                except Exception as e:
                    step.status = StepStatus.FAILED
                    errors.append({"step": step.name, "error": str(e)})
        tasks = [run_step(s) for s in workflow.steps]
        await asyncio.gather(*tasks, return_exceptions=True)
        return {"workflow": workflow.name, "results": results, "errors": errors, "success": len(errors) == 0}
