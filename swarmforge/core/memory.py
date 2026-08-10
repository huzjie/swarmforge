"""
SwarmForge Memory System — persistent conversation & state memory for agents.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MemoryType(Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    WORKING = "working"
    EPISODIC = "episodic"


@dataclass
class MemoryEntry:
    id: str
    content: str
    memory_type: MemoryType = MemoryType.SHORT_TERM
    importance: float = 0.5
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None


class ConversationMemory:
    """Manages conversation history for an agent or swarm."""

    def __init__(self, max_turns: int = 50, max_tokens: int = 100000):
        self.max_turns = max_turns
        self.max_tokens = max_tokens
        self.messages: List[Dict[str, Any]] = []
        self._token_count = 0

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        msg = {"role": role, "content": content, "timestamp": time.time()}
        if metadata:
            msg["metadata"] = metadata
        self.messages.append(msg)
        self._token_count += len(content) // 4  # rough estimate
        self._trim()

    def add_system(self, content: str) -> None:
        self.add_message("system", content)

    def add_user(self, content: str) -> None:
        self.add_message("user", content)

    def add_assistant(self, content: str) -> None:
        self.add_message("assistant", content)

    def add_tool_result(self, tool_name: str, result: Any) -> None:
        self.add_message("tool", str(result), {"tool_name": tool_name})

    def get_messages(self, include_system: bool = True) -> List[Dict[str, Any]]:
        msgs = self.messages.copy()
        if not include_system:
            msgs = [m for m in msgs if m["role"] != "system"]
        return msgs

    def get_last_n(self, n: int) -> List[Dict[str, Any]]:
        return self.messages[-n:] if n > 0 else []

    def _trim(self) -> None:
        while len(self.messages) > self.max_turns or self._token_count > self.max_tokens:
            removed = self.messages.pop(1)  # keep system message
            self._token_count -= len(removed.get("content", "")) // 4

    def clear(self) -> None:
        self.messages = []
        self._token_count = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "messages": self.messages,
            "token_count": self._token_count,
            "max_turns": self.max_turns,
        }

    def summary(self) -> str:
        return f"ConversationMemory({len(self.messages)} messages, ~{self._token_count} tokens)"


class MemoryStore:
    """Persistent memory store with vector search capabilities."""

    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        self._entries: Dict[str, MemoryEntry] = {}
        self._index: Dict[str, List[str]] = {}  # simple keyword index

    def add(self, entry: MemoryEntry) -> None:
        self._entries[entry.id] = entry
        for word in entry.content.lower().split():
            if word not in self._index:
                self._index[word] = []
            self._index[word].append(entry.id)

    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        return self._entries.get(entry_id)

    def search(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        query_words = query.lower().split()
        scores: Dict[str, float] = {}
        for word in query_words:
            for eid in self._index.get(word, []):
                scores[eid] = scores.get(eid, 0) + 1
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [self._entries[eid] for eid, _ in ranked[:top_k]]

    def get_all(self) -> List[MemoryEntry]:
        return list(self._entries.values())

    def forget(self, entry_id: str) -> bool:
        if entry_id in self._entries:
            del self._entries[entry_id]
            return True
        return False

    def clear(self) -> None:
        self._entries.clear()
        self._index.clear()
