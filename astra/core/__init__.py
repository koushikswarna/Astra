"""Core engine, session management, events, and hooks.

InferenceEngine import is lazy since it loads the full model stack.
"""

from astra.core.session import Session

__all__ = ["InferenceEngine", "Session"]


def __getattr__(name):
    if name == "InferenceEngine":
        from astra.core.engine import InferenceEngine
        return InferenceEngine
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
