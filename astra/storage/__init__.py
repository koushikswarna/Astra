"""Storage backends -- JSON files and ChromaDB vectors.

VectorStore import is lazy to avoid loading chromadb eagerly.
"""

from astra.storage.base import StorageBackend
from astra.storage.json_store import JSONStore

__all__ = ["StorageBackend", "JSONStore", "VectorStore"]


def __getattr__(name):
    if name == "VectorStore":
        from astra.storage.vector_store import VectorStore
        return VectorStore
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
