"""Performance timing utilities.

Mostly used during development to figure out where
the latency is hiding (spoiler: it's always the model).
"""

import functools
import time
from contextlib import contextmanager

from astra.utils.logging import get_logger

_log = get_logger(__name__)


@contextmanager
def timer(label: str = "operation"):
    """Context manager that logs elapsed time."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    _log.debug(f"{label} took {elapsed:.3f}s")


def timed(func=None, *, label: str = ""):
    """Decorator that logs how long a function takes.

    Usage:
        @timed
        def slow_thing(): ...

        @timed(label="model inference")
        def generate(): ...
    """
    def decorator(fn):
        tag = label or fn.__qualname__

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            elapsed = time.perf_counter() - start
            _log.debug(f"{tag}: {elapsed:.3f}s")
            return result

        return wrapper

    if func is not None:
        # called as @timed without parens
        return decorator(func)
    return decorator
