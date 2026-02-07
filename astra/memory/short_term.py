"""Sliding-window conversation memory.

Keeps the last N exchanges (user + assistant pairs) so the model
has recent context without blowing up the prompt length.
Persists to a JSON file between sessions.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from astra.memory.base import BaseMemory
from astra.storage.json_store import JSONStore
from astra.storage.migrations import migrate
from astra.types import Personality, Turn
from astra.utils.logging import get_logger

_log = get_logger(__name__)


@dataclass
class ShortTermMemory(BaseMemory):
    max_turns: int = 8
    history: list[Turn] = field(default_factory=list)
    _store: JSONStore | None = field(default=None, repr=False)

    def attach_store(self, store: JSONStore) -> None:
        """Hook up a JSON store for persistence."""
        self._store = store

    def add(self, role: str, text: str, **kwargs) -> None:
        self.history.append((role, text))
        self._trim()

    def retrieve(self, query: str, n: int = 3) -> list[str]:
        # for short-term memory, "retrieve" means recent messages
        return [text for _, text in self.history[-n:]]

    def clear(self) -> None:
        self.history.clear()

    def size(self) -> int:
        return len(self.history)

    def format_prompt(
        self,
        personality: Personality,
        extra_context: str = "",
    ) -> str:
        """Build a full prompt string from conversation history.

        The last entry in self.history should be the user's latest message.
        This method renders everything and appends "Astra:" so the model
        knows whose turn it is to speak.
        """
        parts = [
            f"Astra is a {personality.describe()} assistant. Keep replies helpful and concise.\n",
        ]

        if extra_context:
            parts.append(extra_context)

        for role, text in self.history:
            parts.append(f"{role}: {text}")

        parts.append("Astra:")
        return "\n".join(parts)

    def save(self) -> None:
        if self._store is None:
            return
        self._store.save(self.history)

    def load(self) -> None:
        if self._store is None:
            return
        raw = self._store.load()
        if raw is not None:
            migrated = migrate(raw)
            # JSON round-trips tuples as lists, convert back
            self.history = [tuple(entry) for entry in migrated]
            _log.debug(f"Loaded {len(self.history)} turns from disk")

    def _trim(self) -> None:
        """Keep only the last max_turns * 2 entries (user+bot pairs)."""
        limit = self.max_turns * 2
        if len(self.history) > limit:
            self.history = self.history[-limit:]
