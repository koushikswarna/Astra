"""Abstract storage backend.

Every persistence mechanism (JSON files, ChromaDB, future SQLite, etc.)
implements this interface so the memory layer doesn't care about
the underlying storage technology.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class StorageBackend(ABC):

    @abstractmethod
    def save(self, data: Any, **kwargs) -> None:
        """Persist data to the backing store."""

    @abstractmethod
    def load(self, **kwargs) -> Any:
        """Read data from the backing store."""

    @abstractmethod
    def clear(self) -> None:
        """Wipe the stored data."""

    @abstractmethod
    def exists(self) -> bool:
        """Check whether the backing store has any data."""
