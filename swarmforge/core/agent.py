"""
SwarmForge Agent — the core agent runtime with provider-agnostic LLM integration.
"""
from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Optional, Callable

from swarmforge.core.memory import ConversationMemory, MemoryStore
from swarmforge.core.tool import Tool, ToolRegistry, ToolResult
from swarmforge.core.handoff import HandoffContext, HandoffResult


class AgentRole(Enum):
    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    REVIEWER = "reviewer"
    RESEARCHER = "researcher"
    CODER = "coder"
    ANALYST = "analyst"
    CUSTOM = "custom"


@dataclass
class AgentConfig:
    name: str
    role: AgentRole = AgentRole.WORKER
    description: str = ""
    system_prompt: str = ""
    model: str = "gpt-4"
    provider: str = "openai"
    temperature: float = 0.7
    max_tokens: int = 4096
    capabilities: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    max_iterations: int = 10
    require_approval: bool = False


class Agent:
    """An individual AI agent with tools, memory, and handoff capability."""

    def __init__(
        self,
        config: AgentConfig,
        tool_registry: Optional[ToolRegistry] = None,
        llm_client: Optional[Any] = None,
    ):
        self.config = config
        self.id = str(uuid.uuid4())[:8]
        self.tool_registry = tool_registry or ToolRegistry()
        self.llm_client = llm_client
        self.memory = ConversationMemory()
        self.long_term_memory = MemoryStore(namespace=config.name)
        self._iteration_count = 0
        self._total_tokens = 0
        self._total_latency_ms = 0.0

        # Set system prompt
        if config.system_prompt:
            self.memory.add_system(config.system_prompt)
        else:
            self.memory.add_system(self._default_system_prompt())

    def _default_system_prompt(self) -> str:
        return f"""You are {self.config.name}, a {self.config.role.value} agent in the SwarmForge multi-agent platform.
Your capabilities: {', '.join(self.config.capabilities) if self.config.capabilities else 'general task execution'}.
You can use tools to accomplish tasks. Always respond with clear, actionable output.
When you need help from another agent, use the handoff mechanism."""

    async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a task with the ReAct (Reasoning + Acting) loop."""
        start_time = time.time()
        self._iteration_count = 0
        self.memory.add_user(task)

        if context:
            self.memory.add_system(f"Context: {str(context)}")

        final_response = ""
        tool_calls_made = []

        while self._iteration_count < self.config.max_iterations:
            self._iteration_count += 1

            # Get LLM response
            response = await self._call_llm()
            final_response = response.get("content", "")
            tool_calls = response.get("tool_calls", [])

            if not tool_calls:
                break  # Agent decided task is complete

            # Execute tool calls
            for tc in tool_calls:
                tool_name = tc.get("function", {}).get("name", "")
                tool_args = tc.get("function", {}).get("arguments", "{}")
                if isinstance(tool_args, str):
                    import json
                    tool_args = json.loads(tool_args)

                tool = self.tool_registry.get(tool_name)
                if tool:
                    result = await tool.execute(**tool_args)
                    tool_calls_made.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "success": result.success,
                    })
                    self.memory.add_tool_result(tool_name, result.data if result.success else result.error)
                else:
                    self.memory.add_tool_result(tool_name, f"Tool '{tool_name}' not found")

        elapsed = (time.time() - start_time) * 1000
        self._total_latency_ms += elapsed

        return {
            "agent_id": self.id,
            "agent_name": self.config.name,
            "response": final_response,
            "iterations": self._iteration_count,
            "tool_calls": tool_calls_made,
            "latency_ms": elapsed,
            "tokens_used": self._total_tokens,
            "success": True,
        }

    async def run_streaming(self, task: str) -> AsyncIterator[Dict[str, Any]]:
        """Execute a task with streaming output."""
        self.memory.add_user(task)
        self._iteration_count = 0

        yield {"type": "status", "agent": self.config.name, "status": "thinking"}

        while self._iteration_count < self.config.max_iterations:
            self._iteration_count += 1
            response = await self._call_llm()
            content = response.get("content", "")

            yield {
                "type": "message",
                "agent": self.config.name,
                "content": content,
                "iteration": self._iteration_count,
            }

            tool_calls = response.get("tool_calls", [])
            if not tool_calls:
                yield {"type": "done", "agent": self.config.name}
                return

            for tc in tool_calls:
                yield {
                    "type": "tool_call",
                    "agent": self.config.name,
                    "tool": tc.get("function", {}).get("name", "unknown"),
                }

    async def _call_llm(self) -> Dict[str, Any]:
        """Call the LLM provider. In production, routes to OpenAI/Anthropic/etc."""
        messages = self.memory.get_messages()
        tools = self.tool_registry.get_openai_schemas() if self.tool_registry._tools else None

        if self.llm_client:
            # Real LLM call
            kwargs = {
                "model": self.config.model,
                "messages": messages,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
            }
            if tools:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"

            result = await self.llm_client.chat.completions.create(**kwargs)
            choice = result.choices[0]
            self._total_tokens += result.usage.total_tokens if hasattr(result, "usage") else 0

            response = {"content": choice.message.content or ""}
            if hasattr(choice.message, "tool_calls") and choice.message.tool_calls:
                response["tool_calls"] = [
                    {"function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                    for tc in choice.message.tool_calls
                ]
            return response
        else:
            # Mock response for testing
            return {"content": f"[{self.config.name}] Task acknowledged. Iteration {self._iteration_count}."}

    def handoff(self, target_agent: str, message: str, context: Optional[Dict] = None) -> HandoffContext:
        """Create a handoff to another agent."""
        return HandoffContext(
            task_id=str(uuid.uuid4()),
            source_agent=self.config.name,
            target_agent=target_agent,
            message=message,
            conversation_summary=self.memory.summary(),
            artifacts=context or {},
        )

    def get_stats(self) -> Dict[str, Any]:
        return {
            "agent_id": self.id,
            "name": self.config.name,
            "role": self.config.role.value,
            "total_iterations": self._iteration_count,
            "total_tokens": self._total_tokens,
            "total_latency_ms": self._total_latency_ms,
        }

    def __repr__(self) -> str:
        return f"Agent({self.config.name}, {self.config.role.value}, id={self.id})"
