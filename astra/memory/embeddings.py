"""Embedding model wrapper.

Isolates the sentence-transformers dependency so the rest of the
memory system only deals with float vectors, not model objects.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer

from astra.config.defaults import DEFAULT_EMBEDDING_MODEL
from astra.exceptions import EmbeddingError
from astra.types import Embedding
from astra.utils.logging import get_logger
from astra.utils.timing import timed

_log = get_logger(__name__)


class EmbeddingEngine:
    """Thin wrapper around SentenceTransformer for producing embeddings."""

    def __init__(self, model_name: str = DEFAULT_EMBEDDING_MODEL):
        _log.info(f"Loading embedding model: {model_name}")
        self._model = SentenceTransformer(model_name)
        self._model_name = model_name

    @timed(label="embedding")
    def encode(self, text: str) -> Embedding:
        """Produce a vector for a single text string."""
        try:
            return self._model.encode(text).tolist()
        except Exception as exc:
            raise EmbeddingError(f"Failed to encode text: {exc}") from exc

    def encode_batch(self, texts: list[str]) -> list[Embedding]:
        """Encode multiple texts in one pass (more efficient than looping)."""
        try:
            return [vec.tolist() for vec in self._model.encode(texts)]
        except Exception as exc:
            raise EmbeddingError(f"Batch encoding failed: {exc}") from exc

    @property
    def dimension(self) -> int:
        """Dimensionality of the embedding vectors."""
        return self._model.get_sentence_embedding_dimension()

    def __repr__(self) -> str:
        return f"EmbeddingEngine(model={self._model_name!r}, dim={self.dimension})"
