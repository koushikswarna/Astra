"""Tokenizer wrapper and helpers.

Centralizes tokenizer setup so we handle the pad_token situation
in one place instead of scattering workarounds everywhere.
"""

from __future__ import annotations

from transformers import AutoTokenizer, PreTrainedTokenizerBase

from astra.utils.logging import get_logger

_log = get_logger(__name__)


class TokenizerWrapper:
    """Wraps a HuggingFace tokenizer with sane defaults."""

    def __init__(self, model_name: str):
        self._tokenizer: PreTrainedTokenizerBase = AutoTokenizer.from_pretrained(model_name)
        self._fix_pad_token()

    def _fix_pad_token(self) -> None:
        """Many causal LM tokenizers don't have a pad token set,
        which causes warnings during generation. We just alias it
        to the EOS token.
        """
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token
            self._tokenizer.pad_token_id = self._tokenizer.eos_token_id
            _log.debug("Set pad_token = eos_token")

    def encode(self, text: str, **kwargs):
        """Tokenize text, return tensors."""
        return self._tokenizer(text, return_tensors="pt", **kwargs)

    def decode(self, token_ids, **kwargs) -> str:
        return self._tokenizer.decode(token_ids, skip_special_tokens=True, **kwargs)

    @property
    def pad_token_id(self) -> int | None:
        return self._tokenizer.pad_token_id

    @property
    def eos_token_id(self) -> int | None:
        return self._tokenizer.eos_token_id

    @property
    def vocab_size(self) -> int:
        return self._tokenizer.vocab_size

    def count_tokens(self, text: str) -> int:
        """How many tokens a string would consume."""
        return len(self._tokenizer.encode(text))
