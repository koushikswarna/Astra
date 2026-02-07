"""Abstract UI interface.

Both CLI and web UIs implement this so we can treat them
uniformly from the app layer. Also makes it possible to
test UI logic without actually running a terminal or server.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from astra.core.engine import InferenceEngine


class BaseUI(ABC):
    """Interface that all UI backends implement."""

    def __init__(self, engine: InferenceEngine):
        self.engine = engine

    @abstractmethod
    def run(self) -> None:
        """Start the UI loop (blocking)."""

    @abstractmethod
    def display_message(self, role: str, text: str) -> None:
        """Show a message to the user."""

    @abstractmethod
    def get_input(self) -> str:
        """Get input from the user."""
