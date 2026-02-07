"""CLI interface for Astra.

The run function is imported lazily to avoid loading the full
model stack just because this package was imported.
"""

__all__ = ["run"]


def __getattr__(name):
    if name == "run":
        from astra.ui.cli.app import run
        return run
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
