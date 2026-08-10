"""Response cache — reduce redundant LLM calls."""
import hashlib
import json
import time
from typing import Any, Dict, Optional

class ResponseCache:
    def __init__(self, ttl_seconds: int = 3600, max_entries: int = 10000):
        self.ttl = ttl_seconds
        self.max_entries = max_entries
        self._cache: Dict[str, tuple[float, Any]] = {}

    def _key(self, model: str, messages: list, temperature: float) -> str:
        raw = json.dumps({"model": model, "messages": messages, "temperature": temperature}, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, model: str, messages: list, temperature: float) -> Optional[Any]:
        key = self._key(model, messages, temperature)
        if key in self._cache:
            ts, val = self._cache[key]
            if time.time() - ts < self.ttl:
                return val
            del self._cache[key]
        return None

    def set(self, model: str, messages: list, temperature: float, value: Any):
        if len(self._cache) >= self.max_entries:
            oldest = min(self._cache.items(), key=lambda x: x[1][0])
            del self._cache[oldest[0]]
        key = self._key(model, messages, temperature)
        self._cache[key] = (time.time(), value)

    def clear(self):
        self._cache.clear()

    def stats(self) -> Dict:
        return {"entries": len(self._cache), "max_entries": self.max_entries, "ttl_seconds": self.ttl}
