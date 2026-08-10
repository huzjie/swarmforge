"""bias detector guardrail for SwarmForge."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class GuardResult:
    passed: bool
    reason: Optional[str] = None
    score: float = 0.0

class bias detectorGuard:
    async def check(self, content: str) -> GuardResult:
        return GuardResult(passed=True)

    async def sanitize(self, content: str) -> str:
        return content
