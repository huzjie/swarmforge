"""
SwarmForge Handoff Protocol — agent-to-agent context passing and routing.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class HandoffStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    CAPABILITY_MATCH = "capability_match"
    LOAD_BALANCED = "load_balanced"
    CUSTOM = "custom"
    BROADCAST = "broadcast"


@dataclass
class HandoffContext:
    """Context passed during agent handoff."""
    task_id: str
    source_agent: str
    target_agent: str
    message: str
    conversation_summary: str = ""
    artifacts: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HandoffResult:
    success: bool
    target_agent: str
    response: Optional[str] = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    tokens_used: int = 0


class HandoffProtocol:
    """Manages handoff between agents in a swarm."""

    def __init__(self, strategy: HandoffStrategy = HandoffStrategy.CAPABILITY_MATCH):
        self.strategy = strategy
        self._handoff_history: List[Dict[str, Any]] = []
        self._capability_map: Dict[str, List[str]] = {}

    def register_capabilities(self, agent_name: str, capabilities: List[str]) -> None:
        self._capability_map[agent_name] = capabilities

    def get_capable_agents(self, required_capability: str) -> List[str]:
        return [
            name for name, caps in self._capability_map.items()
            if required_capability in caps
        ]

    def select_target(
        self,
        candidates: List[str],
        context: HandoffContext,
        agent_loads: Optional[Dict[str, int]] = None,
    ) -> str:
        if not candidates:
            raise ValueError("No candidates for handoff")

        if self.strategy == HandoffStrategy.ROUND_ROBIN:
            idx = len(self._handoff_history) % len(candidates)
            return candidates[idx]
        elif self.strategy == HandoffStrategy.LOAD_BALANCED and agent_loads:
            return min(candidates, key=lambda a: agent_loads.get(a, 0))
        elif self.strategy == HandoffStrategy.BROADCAST:
            return candidates[0]  # first; broadcast handled by caller
        else:
            return candidates[0]

    def record_handoff(self, source: str, target: str, result: HandoffResult) -> None:
        self._handoff_history.append({
            "timestamp": time.time(),
            "source": source,
            "target": target,
            "success": result.success,
            "latency_ms": result.latency_ms,
            "tokens_used": result.tokens_used,
        })

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._handoff_history[-limit:]

    def get_stats(self) -> Dict[str, Any]:
        total = len(self._handoff_history)
        if total == 0:
            return {"total_handoffs": 0}

        successful = sum(1 for h in self._handoff_history if h["success"])
        avg_latency = sum(h["latency_ms"] for h in self._handoff_history) / total
        total_tokens = sum(h["tokens_used"] for h in self._handoff_history)

        return {
            "total_handoffs": total,
            "success_rate": successful / total,
            "avg_latency_ms": avg_latency,
            "total_tokens_used": total_tokens,
        }
