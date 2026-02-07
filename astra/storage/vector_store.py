"""ChromaDB vector storage backend.

Wraps chromadb.PersistentClient for storing and querying
document embeddings. Used by long-term memory.
"""

from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Any

import chromadb

from astra.exceptions import StorageError
from astra.storage.base import StorageBackend
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class VectorStore(StorageBackend):

    def __init__(
        self,
        persist_dir: str | Path,
        collection_name: str = "astra_memory",
    ):
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        try:
            self.client = chromadb.PersistentClient(path=str(self.persist_dir))
            self.collection = self.client.get_or_create_collection(collection_name)
        except Exception as exc:
            raise StorageError(f"ChromaDB init failed: {exc}") from exc

        _log.debug(f"VectorStore ready at {self.persist_dir} (collection: {collection_name})")

    def add(
        self,
        document: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Insert a document with its precomputed embedding. Returns the assigned ID."""
        doc_id = f"mem_{int(time.time() * 1000)}_{random.randint(0, 9999)}"
        kwargs = {
            "ids": [doc_id],
            "documents": [document],
            "embeddings": [embedding],
        }
        # chromadb 1.3+ rejects empty metadata dicts
        if metadata:
            kwargs["metadatas"] = [metadata]
        self.collection.add(**kwargs)
        return doc_id

    def query(
        self,
        embedding: list[float],
        n_results: int = 3,
    ) -> list[str]:
        """Find the closest documents to the given embedding."""
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
        )
        docs: list[str] = []
        for batch in results.get("documents", []):
            docs.extend(batch)
        return docs

    def save(self, data: Any, **kwargs) -> None:
        # chromadb persists automatically with PersistentClient
        pass

    def load(self, **kwargs) -> Any:
        # data is always live in chromadb
        return self.collection.get(include=["documents", "metadatas"])

    def clear(self) -> None:
        """Delete all documents in the collection."""
        all_ids = self.collection.get()["ids"]
        if all_ids:
            self.collection.delete(ids=all_ids)
            _log.debug(f"Cleared {len(all_ids)} documents from vector store")

    def exists(self) -> bool:
        return self.collection.count() > 0

    @property
    def count(self) -> int:
        return self.collection.count()
