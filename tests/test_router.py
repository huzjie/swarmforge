"""Tests for task router."""
import pytest
from swarmforge.core.router import TaskRouter, RoutingStrategy, RouteDecision

class TestTaskRouter:
    def test_register_agent(self):
        router = TaskRouter()
        router.register_agent("coder", ["code_generation", "code_review"])
        assert "coder" in router._agent_capabilities

    def test_route_by_capability(self):
        router = TaskRouter(strategy=RoutingStrategy.CAPABILITY_MATCH)
        router.register_agent("coder", ["code_generation", "code_review"])
        router.register_agent("analyst", ["data_analysis", "reporting"])
        decision = router.route("Write a Python script for data analysis")
        assert decision is not None
        assert decision.target_type == "agent"

    def test_route_no_match(self):
        router = TaskRouter()
        decision = router.route("Some random task")
        assert decision is None

    def test_route_cost_optimized(self):
        router = TaskRouter(strategy=RoutingStrategy.COST_OPTIMIZED)
        router.register_agent("cheap", ["general"], cost_per_1k=0.001)
        router.register_agent("expensive", ["general"], cost_per_1k=0.1)
        decision = router.route("general task")
        assert decision is not None
        assert decision.target_name == "cheap"
