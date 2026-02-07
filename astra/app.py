"""Application factory.

Single function that wires everything together and returns
a configured engine ready to use. Both the CLI and web UI
call this (or something similar) to bootstrap the app.
"""

from __future__ import annotations

from astra.config import AstraConfig, load_config
from astra.core.engine import InferenceEngine
from astra.core.personality import random_personality
from astra.plugins.loader import load_plugins
from astra.plugins.registry import PluginRegistry
from astra.types import Personality
from astra.utils.logging import get_logger, setup_logging

_log = get_logger(__name__)


def create_app(
    config: AstraConfig | None = None,
    personality: Personality | None = None,
    load_user_plugins: bool = True,
    **config_overrides,
) -> InferenceEngine:
    """Build and return a fully configured Astra engine.

    This is the recommended way to create an engine instance.
    Pass config overrides as keyword arguments.
    """
    cfg = config or load_config(**config_overrides)

    setup_logging(debug=cfg.debug)
    _log.info("Creating Astra application...")

    p = personality or random_personality()
    engine = InferenceEngine(cfg, personality=p)

    # load plugins if requested
    if load_user_plugins:
        registry = PluginRegistry()
        plugins = load_plugins(engine=engine)
        for plugin in plugins:
            registry.register(plugin, engine)
        if plugins:
            _log.info(f"Loaded {len(plugins)} plugin(s)")

    return engine
