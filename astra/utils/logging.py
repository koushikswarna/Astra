"""Structured logging setup.

We use stdlib logging but configure it once with a consistent
format. Debug messages go to a file, info+ goes to console.
"""

import logging
import sys
from pathlib import Path

_CONFIGURED = False

LOG_FORMAT = "%(asctime)s [%(levelname)-5s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S"


def setup_logging(
    level: int = logging.INFO,
    log_file: Path | None = None,
    debug: bool = False,
):
    """Configure root logger. Safe to call multiple times."""
    global _CONFIGURED
    if _CONFIGURED:
        return
    _CONFIGURED = True

    root = logging.getLogger("astra")
    root.setLevel(logging.DEBUG if debug else level)

    # console handler -- info and above
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(level)
    console.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
    root.addHandler(console)

    # file handler if a path is given
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(str(log_file), encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
        root.addHandler(fh)


def get_logger(name: str) -> logging.Logger:
    """Grab a child logger under the astra namespace."""
    return logging.getLogger(f"astra.{name}")
