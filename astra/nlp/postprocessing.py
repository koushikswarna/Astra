"""Output postprocessing.

Cleans up model output before showing it to the user. The main
job is stopping the model from hallucinating extra conversation
turns and trimming trailing garbage.
"""

from __future__ import annotations

import re

from astra.utils.logging import get_logger
from astra.utils.text import extract_first_response

_log = get_logger(__name__)

# markers where we know the model started hallucinating another turn
_DEFAULT_STOP_MARKERS = ["User:", "Human:", "System:", "Assistant:"]


class Postprocessor:
    """Cleans model-generated text."""

    def __init__(self, stop_markers: list[str] | None = None):
        self.stop_markers = stop_markers or _DEFAULT_STOP_MARKERS
        self._trailing_junk = re.compile(r"\s*[\w]*$")  # incomplete last word

    def process(self, text: str) -> str:
        """Full postprocessing pipeline."""
        text = extract_first_response(text, self.stop_markers)
        text = self._strip_incomplete_sentence(text)
        text = text.strip()

        if not text:
            text = "I'm not sure how to respond to that."
            _log.debug("Empty generation, using fallback response")

        return text

    def _strip_incomplete_sentence(self, text: str) -> str:
        """If the text ends mid-sentence (no terminal punctuation),
        try to cut back to the last complete sentence.
        """
        if not text:
            return text

        # if it ends with proper punctuation, it's fine
        if text[-1] in ".!?\"'":
            return text

        # find the last sentence boundary
        last_period = max(text.rfind("."), text.rfind("!"), text.rfind("?"))
        if last_period > len(text) * 0.3:
            # only trim if we're not throwing away most of the text
            return text[: last_period + 1]

        # no good boundary found, return as-is
        return text


def postprocess(text: str) -> str:
    """One-shot postprocessing."""
    return Postprocessor().process(text)
