"""Abstract model interface.

Defines the contract that any text generation backend must satisfy.
Right now we only have a HuggingFace transformers backend, but this
makes it easy to plug in an API-based model later without changing
the rest of the codebase.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from astra.types import GenerationResult


class BaseModel(ABC):

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> GenerationResult:
        """Given a prompt, produce a continuation."""

    @abstractmethod
    def warmup(self) -> None:
        """Run a throwaway generation to warm up the model/cache."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the name/identifier of the loaded model."""

    @property
    @abstractmethod
    def device(self) -> str:
        """Which device the model is running on (cpu, cuda, mps)."""
