"""REPL (Read-Eval-Print Loop) utilities.

History management, input handling, and the core loop logic
that the CLI app delegates to.
"""

from __future__ import annotations

import readline
import atexit
from pathlib import Path

from astra.config.paths import DATA_ROOT
from astra.utils.logging import get_logger

_log = get_logger(__name__)

HISTORY_FILE = DATA_ROOT / "cli_history"
MAX_HISTORY_LENGTH = 500


def setup_readline() -> None:
    """Configure readline for a nicer REPL experience.

    Enables persistent command history across sessions
    and basic tab completion.
    """
    try:
        if HISTORY_FILE.exists():
            readline.read_history_file(str(HISTORY_FILE))
        readline.set_history_length(MAX_HISTORY_LENGTH)
        atexit.register(_save_history)
    except (OSError, ImportError):
        # readline might not be available on all platforms
        _log.debug("readline setup failed, continuing without history")


def _save_history() -> None:
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        readline.write_history_file(str(HISTORY_FILE))
    except OSError:
        pass


def safe_input(prompt: str = "") -> str | None:
    """Read input, returning None on EOF/interrupt."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()  # newline after ^C
        return None
