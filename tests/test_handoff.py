"""
Tests for the Handoff Protocol.
"""
import pytest
from swarmforge.core.handoff import (
    HandoffProtocol, HandoffStrategy,
    HandoffContext, HandoffResult,
)


class TestHandoffProtocol:
    def test_register_capabilities(self):
        hp = HandoffProtocol()
        hp.register_capabilities("agent-a", ["search", "code"])
        hp.register_capabilities("agent-b", ["analyze", "review"])
        assert hp.get_capable_agents("search") == ["agent-a"]
        assert hp.get_capable_agents("analyze") == ["agent-b"]

    def test_select_target_capability_match(self):
        hp = HandoffProtocol(strategy=HandoffStrategy.CAPABILITY_MATCH)
        ctx = HandoffContext(
            task_id="t1", source_agent="a", target_agent="",
            message="Need search",
        )
        target = hp.select_target(["agent-a", "agent-b"], ctx)
        assert target in ["agent-a", "agent-b"]

    def test_select_target_round_robin(self):
        hp = HandoffProtocol(strategy=HandoffStrategy.ROUND_ROBIN)
        ctx = HandoffContext(task_id="t1", source_agent="a", target_agent="", message="test")
        targets = []
        for _ in range(6):
            targets.append(hp.select_target(["a", "b", "c"], ctx))
        assert "a" in targets and "b" in targets and "c" in targets

    def test_select_target_load_balanced(self):
        hp = HandoffProtocol(strategy=HandoffStrategy.LOAD_BALANCED)
        ctx = HandoffContext(task_id="t1", source_agent="a", target_agent="", message="test")
        loads = {"a": 10, "b": 5, "c": 3}
        target = hp.select_target(["a", "b", "c"], ctx, loads)
        assert target == "c"  # least loaded

    def test_record_and_stats(self):
        hp = HandoffProtocol()
        hp.record_handoff("a", "b", HandoffResult(success=True, target_agent="b", latency_ms=100))
        hp.record_handoff("b", "c", HandoffResult(success=False, target_agent="c", latency_ms=200))
        stats = hp.get_stats()
        assert stats["total_handoffs"] == 2
        assert stats["success_rate"] == 0.5
        assert stats["avg_latency_ms"] == 150.0

    def test_empty_stats(self):
        hp = HandoffProtocol()
        stats = hp.get_stats()
        assert stats["total_handoffs"] == 0
