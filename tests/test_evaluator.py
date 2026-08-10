"""Tests for agent evaluator."""
import pytest
from swarmforge.core.evaluator import AgentEvaluator, EvalMetric, EvalResult

class TestAgentEvaluator:
    def test_compute_accuracy_exact(self):
        evaluator = AgentEvaluator()
        acc = evaluator._compute_accuracy("hello world", "hello world")
        assert acc == 1.0

    def test_compute_accuracy_partial(self):
        evaluator = AgentEvaluator()
        acc = evaluator._compute_accuracy("hello world today", "hello world")
        assert acc > 0.5

    def test_compute_accuracy_empty(self):
        evaluator = AgentEvaluator()
        acc = evaluator._compute_accuracy("", "something")
        assert acc == 0.0

    def test_get_summary_empty(self):
        evaluator = AgentEvaluator()
        assert evaluator.get_summary() == {}
