"""Conversation session management.

A session represents a single run of the assistant (from startup
to shutdown). It tracks conversation state, timing, and provides
a clean boundary for testing.
"""

from __future__ import annotations

import time
import uuid

from astra.types import Personality, ResponseBundle
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class Session:
    """Tracks the state of a single conversation session."""

    def __init__(self, personality: Personality):
        self.id = str(uuid.uuid4())[:8]
        self.personality = personality
        self.started_at = time.time()
        self.turn_count = 0
        self._responses: list[ResponseBundle] = []

    @property
    def duration(self) -> float:
        """How long this session has been running, in seconds."""
        return time.time() - self.started_at

    @property
    def duration_formatted(self) -> str:
        mins, secs = divmod(int(self.duration), 60)
        if mins:
            return f"{mins}m {secs}s"
        return f"{secs}s"

    def record_response(self, response: ResponseBundle) -> None:
        """Track a completed response."""
        self.turn_count += 1
        self._responses.append(response)

    @property
    def last_response(self) -> ResponseBundle | None:
        return self._responses[-1] if self._responses else None

    def summary(self) -> dict:
        """Session stats for display."""
        return {
            "session_id": self.id,
            "personality": self.personality.describe(),
            "turns": self.turn_count,
            "duration": self.duration_formatted,
        }

    def __repr__(self) -> str:
        return f"Session(id={self.id}, turns={self.turn_count})"
