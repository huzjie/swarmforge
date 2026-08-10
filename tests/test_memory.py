"""
Tests for the Memory system.
"""
import pytest
from swarmforge.core.memory import ConversationMemory, MemoryStore, MemoryEntry, MemoryType


class TestConversationMemory:
    def test_add_messages(self):
        mem = ConversationMemory(max_turns=10)
        mem.add_system("System prompt")
        mem.add_user("Hello")
        mem.add_assistant("Hi there!")
        assert len(mem.messages) == 3

    def test_max_turns(self):
        mem = ConversationMemory(max_turns=5)
        for i in range(10):
            mem.add_user(f"Message {i}")
        # Should keep system message + 5 recent
        assert len(mem.messages) <= 6

    def test_get_messages_no_system(self):
        mem = ConversationMemory()
        mem.add_system("system")
        mem.add_user("user msg")
        msgs = mem.get_messages(include_system=False)
        assert len(msgs) == 1
        assert msgs[0]["role"] == "user"

    def test_clear(self):
        mem = ConversationMemory()
        mem.add_user("test")
        mem.clear()
        assert len(mem.messages) == 0

    def test_summary(self):
        mem = ConversationMemory()
        mem.add_user("Hello world")
        assert "1 messages" in mem.summary()


class TestMemoryStore:
    def test_add_and_get(self):
        store = MemoryStore("test")
        entry = MemoryEntry(id="1", content="Test memory", memory_type=MemoryType.SHORT_TERM)
        store.add(entry)
        assert store.get("1") is not None
        assert store.get("1").content == "Test memory"

    def test_search(self):
        store = MemoryStore("test")
        store.add(MemoryEntry(id="1", content="Python programming tips"))
        store.add(MemoryEntry(id="2", content="JavaScript frontend guide"))
        store.add(MemoryEntry(id="3", content="Python async patterns"))

        results = store.search("Python")
        assert len(results) == 2
        assert all("Python" in r.content for r in results)

    def test_forget(self):
        store = MemoryStore("test")
        store.add(MemoryEntry(id="1", content="test"))
        assert store.forget("1") is True
        assert store.get("1") is None
        assert store.forget("nonexistent") is False
