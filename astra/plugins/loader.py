"""Dynamic plugin loading.

Discovers and loads plugins from a directory or from
installed packages using entry points. Currently just
scans a directory -- entry point support is a TODO.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from astra.plugins.base import Plugin
from astra.utils.logging import get_logger

if TYPE_CHECKING:
    from astra.core.engine import InferenceEngine

_log = get_logger(__name__)


def load_plugins(
    plugins_dir: Path | None = None,
    engine: "InferenceEngine | None" = None,
) -> list[Plugin]:
    """Discover and load plugins from a directory.

    Looks for .py files in the given directory, imports them,
    and looks for a `plugin` attribute or a subclass of Plugin.
    """
    if plugins_dir is None:
        from astra.config.paths import DATA_ROOT
        plugins_dir = DATA_ROOT / "plugins"

    if not plugins_dir.exists():
        return []

    loaded: list[Plugin] = []

    for py_file in sorted(plugins_dir.glob("*.py")):
        if py_file.name.startswith("_"):
            continue

        module_name = f"astra_plugin_{py_file.stem}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # look for a `plugin` attribute or any Plugin subclass
            plugin_obj = getattr(module, "plugin", None)
            if plugin_obj is None:
                # scan for Plugin subclasses
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, Plugin)
                        and attr is not Plugin
                    ):
                        plugin_obj = attr()
                        break

            if plugin_obj:
                loaded.append(plugin_obj)
                _log.info(f"Discovered plugin: {plugin_obj.name} from {py_file.name}")

        except Exception as exc:
            _log.error(f"Failed to load plugin from {py_file.name}: {exc}")

    return loaded
