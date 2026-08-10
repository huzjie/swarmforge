"""Intelligent task router — routes tasks to best-fit agent/swarm."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum
import re

class RoutingStrategy(Enum):
    CAPABILITY_MATCH = "capability_match"
    LOAD_BALANCED = "load_balanced"
    COST_OPTIMIZED = "cost_optimized"
    LATENCY_OPTIMIZED = "latency_optimized"
    ROUND_ROBIN = "round_robin"

@dataclass
class RouteDecision:
    target_type: str  # "agent" or "swarm"
    target_name: str
    confidence: float
    reasoning: str
    estimated_cost: float = 0.0
    estimated_latency_ms: float = 0.0

class TaskRouter:
    def __init__(self, strategy: RoutingStrategy = RoutingStrategy.CAPABILITY_MATCH):
        self.strategy = strategy
        self._agent_capabilities: Dict[str, List[str]] = {}
        self._swarm_capabilities: Dict[str, List[str]] = {}
        self._cost_map: Dict[str, float] = {}
        self._latency_map: Dict[str, float] = {}
        self._rr_counter: Dict[str, int] = {}

    def register_agent(self, name: str, capabilities: List[str], cost_per_1k: float = 0.01, avg_latency_ms: float = 1000):
        self._agent_capabilities[name] = capabilities
        self._cost_map[name] = cost_per_1k
        self._latency_map[name] = avg_latency_ms

    def register_swarm(self, name: str, capabilities: List[str]):
        self._swarm_capabilities[name] = capabilities

    def route(self, task: str) -> Optional[RouteDecision]:
        task_lower = task.lower()
        candidates = []
        for name, caps in self._agent_capabilities.items():
            score = sum(1 for c in caps if c.lower() in task_lower)
            if score > 0:
                candidates.append((name, "agent", score, self._cost_map.get(name, 0.01), self._latency_map.get(name, 1000)))
        for name, caps in self._swarm_capabilities.items():
            score = sum(1 for c in caps if c.lower() in task_lower)
            if score > 0:
                candidates.append((name, "swarm", score * 0.8, 0.05, 2000))
        if not candidates:
            return None
        if self.strategy == RoutingStrategy.CAPABILITY_MATCH:
            best = max(candidates, key=lambda x: x[2])
        elif self.strategy == RoutingStrategy.COST_OPTIMIZED:
            best = min(candidates, key=lambda x: x[3])
        elif self.strategy == RoutingStrategy.LATENCY_OPTIMIZED:
            best = min(candidates, key=lambda x: x[4])
        else:
            best = candidates[0]
        return RouteDecision(target_type=best[1], target_name=best[0], confidence=min(best[2] / 3, 1.0), reasoning=f"Matched {best[2]} capabilities")
