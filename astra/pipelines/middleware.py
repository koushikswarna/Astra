"""Middleware chain for the chat pipeline.

Middleware wraps around the core generate step and can inspect
or modify the request/response at various points. Think of it
like Express middleware but for chat turns.
"""

from __future__ import annotations

from typing import Any, Callable

from astra.pipelines.base import PipelineStep
from astra.utils.logging import get_logger

_log = get_logger(__name__)

# type alias for a middleware function
MiddlewareFn = Callable[[dict[str, Any], Callable], dict[str, Any]]


class MiddlewareChain:
    """Executes a chain of middleware around a core handler."""

    def __init__(self):
        self._middlewares: list[MiddlewareFn] = []

    def add(self, middleware: MiddlewareFn) -> None:
        self._middlewares.append(middleware)

    def execute(self, context: dict[str, Any], core: Callable) -> dict[str, Any]:
        """Run the middleware chain with the core handler at the center."""

        def build_chain(index: int) -> Callable:
            if index >= len(self._middlewares):
                return core

            mw = self._middlewares[index]
            next_handler = build_chain(index + 1)
            return lambda ctx: mw(ctx, next_handler)

        chain = build_chain(0)
        return chain(context)


class LoggingMiddleware:
    """Logs the input and output of each pipeline pass."""

    def __call__(self, context: dict[str, Any], next_handler: Callable) -> dict[str, Any]:
        user_text = context.get("user_text", "")
        _log.debug(f"Pipeline input: {user_text[:80]}...")

        result = next_handler(context)

        reply = result.get("reply", "")
        _log.debug(f"Pipeline output: {reply[:80]}...")
        return result


class TimingMiddleware:
    """Records how long the core generation takes."""

    def __call__(self, context: dict[str, Any], next_handler: Callable) -> dict[str, Any]:
        import time
        start = time.perf_counter()
        result = next_handler(context)
        elapsed = time.perf_counter() - start
        result["generation_time"] = elapsed
        _log.debug(f"Generation took {elapsed:.3f}s")
        return result
