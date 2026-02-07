"""Vector-backed semantic memory.

Uses ChromaDB for storage and sentence-transformers for embeddings.
This is where "remember this" and "what did I say about X" live.
"""

from __future__ import annotations

from astra.exceptions import LongTermMemoryError
from astra.memory.base import BaseMemory
from astra.memory.embeddings import EmbeddingEngine
from astra.storage.vector_store import VectorStore
from astra.types import Metadata
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class LongTermMemory(BaseMemory):

    def __init__(
        self,
        vector_store: VectorStore,
        embedder: EmbeddingEngine,
    ):
        self.store = vector_store
        self.embedder = embedder
        _log.info(f"Long-term memory initialized ({self.store.count} existing documents)")

    def add(self, text: str, metadata: Metadata | None = None, **kwargs) -> str:
        """Embed and store a text snippet. Returns the doc ID."""
        try:
            embedding = self.embedder.encode(text)
            doc_id = self.store.add(
                document=text,
                embedding=embedding,
                metadata=metadata,
            )
            _log.debug(f"Stored memory {doc_id}: {text[:60]}...")
            return doc_id
        except Exception as exc:
            raise LongTermMemoryError(f"Failed to store memory: {exc}") from exc

    def retrieve(self, query: str, n: int = 3) -> list[str]:
        """Semantic search -- find the n most relevant stored memories."""
        try:
            embedding = self.embedder.encode(query)
            return self.store.query(embedding, n_results=n)
        except Exception as exc:
            _log.warning(f"Memory recall failed: {exc}")
            return []

    def clear(self) -> None:
        self.store.clear()
        _log.info("Long-term memory cleared")

    def size(self) -> int:
        return self.store.count

    # alias for code that reads more naturally
    search = retrieve
