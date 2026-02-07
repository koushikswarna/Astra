"""Plugin interface.

Plugins can extend Astra with custom commands, hooks, or
pipeline steps. They're loaded dynamically from a plugins
directory or via entry points.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from astra.core.engine import InferenceEngine


class Plugin(ABC):
    """Base class for Astra plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable plugin name."""

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def description(self) -> str:
        return ""

    @abstractmethod
    def initialize(self, engine: InferenceEngine) -> None:
        """Called when the plugin is loaded.

        Use this to register hooks, commands, event handlers, etc.
        """

    def shutdown(self) -> None:
        """Called when the engine is shutting down. Optional cleanup."""
        pass

    def __repr__(self) -> str:
        return f"<Plugin: {self.name} v{self.version}>"
