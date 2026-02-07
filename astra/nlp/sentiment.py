"""Sentiment analysis using a HuggingFace pipeline.

Runs a lightweight classifier to detect the emotional tone
of user messages. This feeds into personality-aware responses
and gets displayed as metadata in the UI.
"""

from __future__ import annotations

from transformers import pipeline as hf_pipeline

from astra.config.defaults import DEFAULT_SENTIMENT_MODEL
from astra.types import SentimentResult
from astra.utils.logging import get_logger
from astra.utils.text import truncate

_log = get_logger(__name__)


class SentimentAnalyzer:

    def __init__(self, model: str = DEFAULT_SENTIMENT_MODEL):
        _log.info(f"Loading sentiment model: {model}")
        self._pipeline = hf_pipeline("sentiment-analysis", model=model)
        self._model_name = model

    def analyze(self, text: str) -> SentimentResult:
        """Run sentiment classification on the input text.

        Long text gets truncated because the underlying model
        has a 512 token limit and will choke on anything bigger.
        """
        truncated = truncate(text, max_len=512, suffix="")
        result = self._pipeline(truncated)[0]
        return SentimentResult(
            label=result["label"],
            score=round(result["score"], 4),
        )

    def analyze_batch(self, texts: list[str]) -> list[SentimentResult]:
        """Classify multiple texts in one call."""
        truncated = [truncate(t, max_len=512, suffix="") for t in texts]
        results = self._pipeline(truncated)
        return [
            SentimentResult(label=r["label"], score=round(r["score"], 4))
            for r in results
        ]

    def __repr__(self) -> str:
        return f"SentimentAnalyzer(model={self._model_name!r})"
