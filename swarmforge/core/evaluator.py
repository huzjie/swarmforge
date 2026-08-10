"""Agent evaluator — benchmark and evaluate agent performance."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import asyncio

@dataclass
class EvalMetric:
    name: str
    value: float
    unit: str = ""
    threshold: Optional[float] = None
    passed: bool = True

@dataclass
class EvalResult:
    agent_name: str
    task: str
    metrics: List[EvalMetric] = field(default_factory=list)
    response: str = ""
    duration_ms: float = 0.0
    tokens_used: int = 0
    success: bool = True
    errors: List[str] = field(default_factory=list)

class AgentEvaluator:
    def __init__(self):
        self._results: List[EvalResult] = []

    async def evaluate(self, agent, test_cases: List[Dict]) -> List[EvalResult]:
        results = []
        for tc in test_cases:
            start = time.time()
            try:
                result = await agent.run(tc.get("task", ""), tc.get("context"))
                duration = (time.time() - start) * 1000
                eval_result = EvalResult(
                    agent_name=agent.config.name,
                    task=tc.get("task", ""),
                    response=result.get("response", ""),
                    duration_ms=duration,
                    tokens_used=result.get("tokens_used", 0),
                    success=result.get("success", True),
                )
                if "expected" in tc:
                    expected = tc["expected"]
                    actual = result.get("response", "")
                    accuracy = self._compute_accuracy(expected, actual)
                    eval_result.metrics.append(EvalMetric(name="accuracy", value=accuracy, unit="ratio", threshold=0.7, passed=accuracy >= 0.7))
                eval_result.metrics.append(EvalMetric(name="latency", value=duration, unit="ms", threshold=tc.get("max_latency_ms", 5000), passed=duration <= tc.get("max_latency_ms", 5000)))
            except Exception as e:
                eval_result = EvalResult(agent_name=agent.config.name, task=tc.get("task", ""), success=False, errors=[str(e)])
            results.append(eval_result)
        self._results.extend(results)
        return results

    def _compute_accuracy(self, expected: str, actual: str) -> float:
        if not expected or not actual:
            return 0.0
        exp_words = set(expected.lower().split())
        act_words = set(actual.lower().split())
        if not exp_words:
            return 0.0
        return len(exp_words & act_words) / len(exp_words)

    def get_summary(self) -> Dict:
        if not self._results:
            return {}
        total = len(self._results)
        successful = sum(1 for r in self._results if r.success)
        avg_latency = sum(r.duration_ms for r in self._results) / total if total else 0
        avg_tokens = sum(r.tokens_used for r in self._results) / total if total else 0
        return {"total_tests": total, "success_rate": successful / total if total else 0, "avg_latency_ms": avg_latency, "avg_tokens": avg_tokens}
