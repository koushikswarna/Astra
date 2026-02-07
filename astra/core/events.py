"""Simple event bus for decoupled component communication.

Components can emit events and other components can subscribe
to them without direct imports or references. This keeps
things like "log every generation" or "play a sound on new message"
from creating spaghetti dependencies.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable

from astra.constants import EventType
from astra.utils.logging import get_logger

_log = get_logger(__name__)

# subscriber callback signature
EventHandler = Callable[[EventType, dict[str, Any]], None]


class EventBus:
    """Pub/sub event system."""

    def __init__(self):
        self._handlers: dict[EventType, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event: EventType, handler: EventHandler) -> None:
        """Register a handler for an event type."""
        self._handlers[event].append(handler)
        _log.debug(f"Subscribed {handler.__qualname__} to {event.value}")

    def unsubscribe(self, event: EventType, handler: EventHandler) -> None:
        """Remove a handler."""
        try:
            self._handlers[event].remove(handler)
        except ValueError:
            pass

    def emit(self, event: EventType, data: dict[str, Any] | None = None) -> None:
        """Fire an event, calling all registered handlers."""
        data = data or {}
        handlers = self._handlers.get(event, [])

        for handler in handlers:
            try:
                handler(event, data)
            except Exception as exc:
                # don't let a broken handler crash the whole pipeline
                _log.error(f"Event handler {handler.__qualname__} failed on {event.value}: {exc}")

    def clear(self) -> None:
        """Remove all handlers."""
        self._handlers.clear()

    @property
    def stats(self) -> dict[str, int]:
        """How many handlers are registered per event type."""
        return {k.value: len(v) for k, v in self._handlers.items() if v}
