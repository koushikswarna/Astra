"""Text manipulation utilities.

Small helpers that get used all over the place -- prompt building,
output cleaning, memory storage, etc.
"""

import re
import unicodedata


def sanitize(text: str) -> str:
    """Normalize whitespace and strip control characters.

    We collapse all runs of whitespace into single spaces because
    newlines in user input can break the prompt format.
    """
    # strip unicode control chars but keep normal whitespace
    cleaned = "".join(
        ch for ch in text
        if not unicodedata.category(ch).startswith("C") or ch in ("\n", "\t", " ")
    )
    # collapse whitespace
    return re.sub(r"\s+", " ", cleaned).strip()


def truncate(text: str, max_len: int = 512, suffix: str = "...") -> str:
    """Truncate text to max_len characters, appending suffix if truncated."""
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix


def extract_first_response(text: str, stop_markers: list[str] | None = None) -> str:
    """Cut off generated text at the first occurrence of any stop marker.

    This is how we deal with the model hallucinating additional
    conversation turns -- we just chop at "User:" or similar.
    """
    if stop_markers is None:
        stop_markers = ["User:", "Human:", "\n\n\n"]

    earliest = len(text)
    for marker in stop_markers:
        idx = text.find(marker)
        if idx != -1 and idx < earliest:
            earliest = idx

    return text[:earliest].strip()


def contains_any(text: str, keywords: frozenset[str] | set[str]) -> bool:
    """Case-insensitive check for any keyword in text."""
    lower = text.lower()
    return any(kw in lower for kw in keywords)


def word_count(text: str) -> int:
    return len(text.split())
