"""Input preprocessing pipeline.

Cleans and normalizes user input before it hits the model.
Things like collapsing whitespace, stripping weird unicode,
detecting language, etc.
"""

from __future__ import annotations

import re

from astra.utils.logging import get_logger
from astra.utils.text import sanitize

_log = get_logger(__name__)


class Preprocessor:
    """Cleans user input before it enters the chat pipeline."""

    def __init__(self, max_input_length: int = 1024):
        self.max_input_length = max_input_length
        # patterns we strip out
        self._url_pattern = re.compile(r"https?://\S+")
        self._repeated_punct = re.compile(r"([!?.]){4,}")

    def process(self, text: str) -> str:
        """Full preprocessing pipeline."""
        text = sanitize(text)
        text = self._collapse_repeated_punctuation(text)
        text = self._enforce_length(text)
        return text

    def _collapse_repeated_punctuation(self, text: str) -> str:
        """Turn "!!!!!!" into "!!!" -- the model doesn't need that many."""
        return self._repeated_punct.sub(r"\1\1\1", text)

    def _enforce_length(self, text: str) -> str:
        """Hard cap on input length to prevent prompt injection / abuse."""
        if len(text) > self.max_input_length:
            _log.warning(f"Input truncated from {len(text)} to {self.max_input_length} chars")
            return text[: self.max_input_length]
        return text

    def strip_urls(self, text: str) -> str:
        """Remove URLs from text. Not always wanted, so it's opt-in."""
        return self._url_pattern.sub("[link]", text)


# convenience function for simple use cases
def preprocess(text: str) -> str:
    """One-shot preprocessing without constructing a Preprocessor."""
    return Preprocessor().process(text)
