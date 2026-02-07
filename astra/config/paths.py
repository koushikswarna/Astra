"""Path resolution for Astra's data and config directories.

We store everything under ~/.astra/ by default so users can run
the assistant from any working directory without littering files.
"""

import os
from pathlib import Path

from astra.config.defaults import DEFAULT_MEMORY_FILENAME, DEFAULT_CHROMA_DIRNAME


def _get_data_root() -> Path:
    """Resolve the root directory for persistent data.

    Respects ASTRA_DATA_DIR env var if set, otherwise defaults to ~/.astra
    """
    env_override = os.environ.get("ASTRA_DATA_DIR")
    if env_override:
        root = Path(env_override)
    else:
        root = Path.home() / ".astra"

    root.mkdir(parents=True, exist_ok=True)
    return root


def _get_config_path() -> Path:
    """Where to look for astra_config.yaml."""
    env_override = os.environ.get("ASTRA_CONFIG_FILE")
    if env_override:
        return Path(env_override)
    return _get_data_root() / "config.yaml"


DATA_ROOT = _get_data_root()
CONFIG_FILE = _get_config_path()
MEMORY_JSON_PATH = DATA_ROOT / DEFAULT_MEMORY_FILENAME
CHROMA_DIR_PATH = DATA_ROOT / DEFAULT_CHROMA_DIRNAME
LOG_DIR = DATA_ROOT / "logs"

# make sure the log dir exists too
LOG_DIR.mkdir(parents=True, exist_ok=True)
