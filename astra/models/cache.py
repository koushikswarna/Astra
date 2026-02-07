"""KV cache management for transformer inference.

Tracks cache state and provides utilities for clearing
or resizing the cache between generations. Mostly relevant
when running on GPU with limited VRAM.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import torch

from astra.utils.logging import get_logger

_log = get_logger(__name__)


@dataclass
class CacheStats:
    """Tracking stats for the generation cache."""
    hits: int = 0
    misses: int = 0
    clears: int = 0
    total_tokens_cached: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class CacheManager:
    """Manages KV cache lifecycle during generation.

    For distilgpt2 on CPU this doesn't matter much, but it
    becomes important with larger models on GPU where VRAM
    pressure is real.
    """

    def __init__(self, max_cache_size_mb: int = 512):
        self.max_cache_size_mb = max_cache_size_mb
        self.stats = CacheStats()
        self._past_key_values = None

    def should_clear(self) -> bool:
        """Check if we're approaching the cache size limit."""
        if not torch.cuda.is_available():
            return False

        allocated = torch.cuda.memory_allocated() / (1024 * 1024)
        return allocated > self.max_cache_size_mb

    def clear(self) -> None:
        """Drop cached KV pairs and free memory."""
        self._past_key_values = None
        self.stats.clears += 1

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            _log.debug("GPU cache cleared")

    def store(self, past_key_values) -> None:
        self._past_key_values = past_key_values
        self.stats.hits += 1

    def get(self):
        if self._past_key_values is not None:
            self.stats.hits += 1
            return self._past_key_values
        self.stats.misses += 1
        return None

    def report(self) -> str:
        return (
            f"Cache stats: {self.stats.hits} hits, "
            f"{self.stats.misses} misses, "
            f"{self.stats.clears} clears, "
            f"hit rate: {self.stats.hit_rate:.1%}"
        )
