"""Tests for response cache."""
import pytest
import time
from swarmforge.core.cache import ResponseCache

class TestResponseCache:
    def test_set_and_get(self):
        cache = ResponseCache(ttl_seconds=60)
        messages = [{"role": "user", "content": "Hello"}]
        cache.set("gpt-4", messages, 0.7, "Hi there!")
        result = cache.get("gpt-4", messages, 0.7)
        assert result == "Hi there!"

    def test_cache_miss(self):
        cache = ResponseCache()
        result = cache.get("gpt-4", [{"role": "user", "content": "New"}], 0.7)
        assert result is None

    def test_ttl_expiry(self):
        cache = ResponseCache(ttl_seconds=0.01)
        cache.set("gpt-4", [{"role": "user", "content": "Hello"}], 0.7, "Hi!")
        time.sleep(0.02)
        result = cache.get("gpt-4", [{"role": "user", "content": "Hello"}], 0.7)
        assert result is None

    def test_clear(self):
        cache = ResponseCache()
        cache.set("gpt-4", [{"role": "user", "content": "Test"}], 0.7, "Response")
        cache.clear()
        assert cache.stats()["entries"] == 0

    def test_stats(self):
        cache = ResponseCache(max_entries=5)
        cache.set("gpt-4", [{"role": "user", "content": "A"}], 0.7, "R")
        stats = cache.stats()
        assert stats["entries"] == 1
        assert stats["max_entries"] == 5
