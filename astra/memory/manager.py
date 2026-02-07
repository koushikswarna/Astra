"""Unified memory manager.

The assistant talks to this instead of juggling short-term
and long-term memory separately. Single point of contact
for all memory operations.
"""

from __future__ import annotations

from astra.config.base import MemoryConfig
from astra.memory.embeddings import EmbeddingEngine
from astra.memory.long_term import LongTermMemory
from astra.memory.persistence import PersistenceLayer
from astra.memory.short_term import ShortTermMemory
from astra.storage.vector_store import VectorStore
from astra.types import Metadata, Personality
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class MemoryManager:
    """Facade over both memory subsystems."""

    def __init__(
        self,
        config: MemoryConfig,
        enable_long_term: bool = True,
        embedding_model: str | None = None,
    ):
        self.config = config

        # short-term (always available)
        self.short_term = ShortTermMemory(max_turns=config.max_history)
        self._persistence = PersistenceLayer(config.memory_json_path)
        self._persistence.bind_short_term(self.short_term)
        self._persistence.load_short_term(self.short_term)

        # long-term (optional, needs chromadb + sentence-transformers)
        self.long_term: LongTermMemory | None = None
        if enable_long_term:
            try:
                store = VectorStore(
                    persist_dir=config.chroma_dir,
                    collection_name=config.chroma_collection,
                )
                embedder = EmbeddingEngine(
                    model_name=embedding_model or "all-MiniLM-L6-v2",
                )
                self.long_term = LongTermMemory(store, embedder)
            except Exception as exc:
                _log.warning(f"Long-term memory unavailable: {exc}")

    @property
    def has_long_term(self) -> bool:
        return self.long_term is not None

    def add_turn(self, role: str, text: str) -> None:
        """Add a conversation turn to short-term memory."""
        self.short_term.add(role, text)

    def build_prompt(self, personality: Personality, extra_context: str = "",
                     eos_token: str = "") -> str:
        return self.short_term.format_prompt(personality, extra_context, eos_token=eos_token)

    def recall(self, query: str, n: int = 3) -> list[str]:
        """Semantic recall from long-term memory."""
        if self.long_term:
            return self.long_term.retrieve(query, n=n)
        return []

    def store_long_term(self, text: str, source: str = "user") -> None:
        """Explicitly store something in long-term memory."""
        if self.long_term:
            self.long_term.add(text, metadata={"source": source})

    def save(self) -> None:
        self._persistence.save_short_term(self.short_term)

    def clear_history(self) -> None:
        """Clear conversation history (short-term only)."""
        self.short_term.clear()
        self.save()

    def clear_all(self) -> None:
        """Nuclear option -- wipe both memories."""
        self.clear_history()
        if self.long_term:
            self.long_term.clear()
