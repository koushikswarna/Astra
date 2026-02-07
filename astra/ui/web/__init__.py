"""Streamlit web interface for Astra.

Lazily imported to avoid loading streamlit + model stack eagerly.
"""

__all__ = ["run"]


def __getattr__(name):
    if name == "run":
        from astra.ui.web.app import run
        return run
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
