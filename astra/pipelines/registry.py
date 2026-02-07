"""Pipeline step registry.

Allows steps to be registered by name and instantiated dynamically.
Overkill for the current setup, but it makes the plugin system
possible later.
"""

from __future__ import annotations

from typing import Type

from astra.pipelines.base import PipelineStep
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class PipelineRegistry:
    """Registry of available pipeline steps."""

    _steps: dict[str, Type[PipelineStep]] = {}

    @classmethod
    def register(cls, name: str, step_class: Type[PipelineStep]) -> None:
        if name in cls._steps:
            _log.warning(f"Overwriting pipeline step '{name}'")
        cls._steps[name] = step_class

    @classmethod
    def get(cls, name: str) -> Type[PipelineStep]:
        if name not in cls._steps:
            raise KeyError(f"Unknown pipeline step: {name}")
        return cls._steps[name]

    @classmethod
    def available(cls) -> list[str]:
        return list(cls._steps.keys())

    @classmethod
    def create(cls, name: str, **kwargs) -> PipelineStep:
        """Instantiate a step by name."""
        step_class = cls.get(name)
        return step_class(**kwargs)
