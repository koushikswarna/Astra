"""Content filters for input and output.

Basic safety layer -- nothing production-grade, but enough to
catch obvious problems before they reach the model or the user.
"""

from __future__ import annotations

import re

from astra.utils.logging import get_logger

_log = get_logger(__name__)

# not trying to be comprehensive here, just catching the obvious stuff
_BLOCKED_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(DAN|jailbr)", re.IGNORECASE),
    re.compile(r"system\s*:\s*you\s+are", re.IGNORECASE),
]


class ContentFilter:
    """Simple content filter for obvious prompt injection and safety issues."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._blocked_patterns = _BLOCKED_PATTERNS

    def check_input(self, text: str) -> tuple[bool, str]:
        """Check user input. Returns (is_safe, reason)."""
        if not self.enabled:
            return True, ""

        for pattern in self._blocked_patterns:
            if pattern.search(text):
                _log.warning(f"Input blocked by filter: {pattern.pattern}")
                return False, "Input contains blocked pattern"

        return True, ""

    def check_output(self, text: str) -> str:
        """Sanitize model output. Returns cleaned text."""
        if not self.enabled:
            return text

        # strip any accidental system-prompt-like prefixes the model might emit
        if text.strip().lower().startswith("system:"):
            text = text.split(":", 1)[1].strip() if ":" in text else text

        return text

    def add_pattern(self, pattern: str) -> None:
        """Add a custom blocked pattern at runtime."""
        self._blocked_patterns.append(re.compile(pattern, re.IGNORECASE))
