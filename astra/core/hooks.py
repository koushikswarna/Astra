"""Lifecycle hooks for the response pipeline.

Hooks let you inject custom behavior at specific points
in the response lifecycle without modifying the core logic.
Think pre-commit hooks but for chat.
"""

from __future__ import annotations

from typing import Any, Callable

from astra.types import ResponseBundle
from astra.utils.logging import get_logger

_log = get_logger(__name__)

# hook function signatures
PreResponseHook = Callable[[str], str | None]  # receives user text, can modify or reject
PostResponseHook = Callable[[ResponseBundle], ResponseBundle]  # can modify the response


class HookManager:
    """Manages pre/post response hooks."""

    def __init__(self):
        self._pre_hooks: list[PreResponseHook] = []
        self._post_hooks: list[PostResponseHook] = []

    def add_pre_hook(self, hook: PreResponseHook) -> None:
        """Add a hook that runs before generation.

        If the hook returns None, the message is rejected.
        If it returns a modified string, that string is used instead.
        """
        self._pre_hooks.append(hook)

    def add_post_hook(self, hook: PostResponseHook) -> None:
        """Add a hook that runs after generation, can modify the response."""
        self._post_hooks.append(hook)

    def run_pre_hooks(self, user_text: str) -> str | None:
        """Run all pre-hooks. Returns modified text or None to reject."""
        current = user_text
        for hook in self._pre_hooks:
            try:
                result = hook(current)
                if result is None:
                    _log.debug(f"Pre-hook {hook.__qualname__} rejected input")
                    return None
                current = result
            except Exception as exc:
                _log.error(f"Pre-hook {hook.__qualname__} failed: {exc}")
        return current

    def run_post_hooks(self, response: ResponseBundle) -> ResponseBundle:
        """Run all post-hooks on the response."""
        current = response
        for hook in self._post_hooks:
            try:
                current = hook(current)
            except Exception as exc:
                _log.error(f"Post-hook {hook.__qualname__} failed: {exc}")
        return current

    def clear(self) -> None:
        self._pre_hooks.clear()
        self._post_hooks.clear()
