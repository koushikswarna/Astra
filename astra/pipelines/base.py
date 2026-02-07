"""Abstract pipeline step.

Each step in the chat pipeline takes some context, does
its thing, and passes the result along. Steps can be
skipped, reordered, or replaced without touching the
pipeline orchestration code.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PipelineStep(ABC):
    """A single processing step in a pipeline."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name for logging/debugging."""

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        """Process the context dict and return the (possibly modified) context.

        Each step reads what it needs from the context, does its work,
        and writes its results back into the context for downstream steps.
        """

    def should_skip(self, context: dict[str, Any]) -> bool:
        """Override to conditionally skip this step."""
        return False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
