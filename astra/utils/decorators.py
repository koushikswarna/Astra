"""Reusable decorators."""

from __future__ import annotations

import functools
import importlib
import time
from typing import Any, Callable, TypeVar

from astra.utils.logging import get_logger

_log = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def retry(
    max_attempts: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """Retry a function on failure with exponential backoff.

    Mostly used around network calls (model downloads, speech API).
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < max_attempts:
                        _log.warning(
                            f"{func.__name__} attempt {attempt}/{max_attempts} "
                            f"failed: {exc}. Retrying in {current_delay:.1f}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
            raise last_exc  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]
    return decorator


def lazy_import(module_path: str, attribute: str | None = None) -> Any:
    """Import a module (and optionally an attribute) lazily.

    Handy for optional heavy deps like pyttsx3 or streamlit
    that we don't want to load at startup.
    """
    mod = importlib.import_module(module_path)
    if attribute:
        return getattr(mod, attribute)
    return mod


def singleton(cls):
    """Class decorator -- only one instance ever created."""
    instances: dict[type, Any] = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
