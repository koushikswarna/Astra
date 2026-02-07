"""Shared tokenizer utilities.

Helper functions that work with any HuggingFace tokenizer, used by
both the model layer and the NLP preprocessing layer.
"""

from __future__ import annotations

from transformers import PreTrainedTokenizerBase


def estimate_token_count(text: str) -> int:
    """Quick and dirty token estimate without loading a tokenizer.

    Rule of thumb: ~4 characters per token for English text.
    Not accurate, but useful for rough checks before spending
    time on actual tokenization.
    """
    return len(text) // 4 + 1


def fits_in_context(
    text: str,
    tokenizer: PreTrainedTokenizerBase,
    max_tokens: int = 1024,
) -> bool:
    """Check if text fits within a token budget."""
    token_count = len(tokenizer.encode(text))
    return token_count <= max_tokens


def trim_to_budget(
    text: str,
    tokenizer: PreTrainedTokenizerBase,
    max_tokens: int = 1024,
    from_start: bool = False,
) -> str:
    """Trim text to fit within a token budget.

    By default trims from the beginning (keeps the end),
    since recent context is usually more important.
    """
    tokens = tokenizer.encode(text)
    if len(tokens) <= max_tokens:
        return text

    if from_start:
        trimmed_tokens = tokens[:max_tokens]
    else:
        trimmed_tokens = tokens[-max_tokens:]

    return tokenizer.decode(trimmed_tokens, skip_special_tokens=True)
