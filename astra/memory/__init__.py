"""Memory subsystem -- short-term conversation buffer and long-term vector memory.

Heavy imports (sentence-transformers, chromadb) are deferred to avoid
loading ML models at package import time.
"""

# only import the lightweight stuff eagerly
from astra.memory.short_term import ShortTermMemory

__all__ = ["ShortTermMemory", "LongTermMemory", "MemoryManager"]


def __getattr__(name):
    """Lazy-load heavy components on first access."""
    if name == "LongTermMemory":
        from astra.memory.long_term import LongTermMemory
        return LongTermMemory
    if name == "MemoryManager":
        from astra.memory.manager import MemoryManager
        return MemoryManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
