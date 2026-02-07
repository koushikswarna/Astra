"""Memory persistence coordination.

Handles the lifecycle of saving/loading both short-term and long-term
memory. The manager delegates here for the actual I/O orchestration.
"""

from __future__ import annotations

from pathlib import Path

from astra.memory.short_term import ShortTermMemory
from astra.storage.json_store import JSONStore
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class PersistenceLayer:
    """Coordinates memory persistence across backends."""

    def __init__(self, memory_json_path: str | Path):
        self.json_store = JSONStore(memory_json_path)

    def bind_short_term(self, memory: ShortTermMemory) -> None:
        """Attach the JSON store to a short-term memory instance."""
        memory.attach_store(self.json_store)

    def save_short_term(self, memory: ShortTermMemory) -> None:
        memory.save()
        _log.debug("Short-term memory persisted")

    def load_short_term(self, memory: ShortTermMemory) -> None:
        memory.load()

    def wipe_short_term(self) -> None:
        """Delete the memory file entirely."""
        self.json_store.clear()
        _log.info("Short-term memory file deleted")

    def has_saved_state(self) -> bool:
        return self.json_store.exists()
