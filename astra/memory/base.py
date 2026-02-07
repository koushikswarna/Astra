"""Abstract memory interface.

Both short-term (conversation buffer) and long-term (semantic/vector)
memory implement this so the assistant can treat them uniformly
when it needs to.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from astra.types import Metadata


class BaseMemory(ABC):

    @abstractmethod
    def add(self, text: str, **kwargs) -> None:
        """Store a piece of information."""

    @abstractmethod
    def retrieve(self, query: str, n: int = 3) -> list[str]:
        """Get relevant information given a query."""

    @abstractmethod
    def clear(self) -> None:
        """Wipe all stored data."""

    @abstractmethod
    def size(self) -> int:
        """How many items are currently stored."""
