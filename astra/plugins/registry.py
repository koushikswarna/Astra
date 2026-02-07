"""Plugin registration and lifecycle management."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astra.plugins.base import Plugin
from astra.utils.logging import get_logger

if TYPE_CHECKING:
    from astra.core.engine import InferenceEngine

_log = get_logger(__name__)


class PluginRegistry:
    """Manages loaded plugins."""

    def __init__(self):
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin, engine: InferenceEngine) -> None:
        """Register and initialize a plugin."""
        if plugin.name in self._plugins:
            _log.warning(f"Plugin '{plugin.name}' already registered, skipping")
            return

        try:
            plugin.initialize(engine)
            self._plugins[plugin.name] = plugin
            _log.info(f"Plugin loaded: {plugin}")
        except Exception as exc:
            _log.error(f"Plugin '{plugin.name}' failed to initialize: {exc}")

    def unregister(self, name: str) -> None:
        """Remove a plugin."""
        plugin = self._plugins.pop(name, None)
        if plugin:
            try:
                plugin.shutdown()
            except Exception as exc:
                _log.error(f"Plugin '{name}' shutdown error: {exc}")

    def shutdown_all(self) -> None:
        """Shut down all plugins."""
        for name in list(self._plugins.keys()):
            self.unregister(name)

    @property
    def loaded(self) -> list[str]:
        return list(self._plugins.keys())

    def get(self, name: str) -> Plugin | None:
        return self._plugins.get(name)
