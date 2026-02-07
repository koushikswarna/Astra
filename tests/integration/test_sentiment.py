"""Integration tests for sentiment analysis."""

import os
import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("ASTRA_RUN_SLOW_TESTS") != "1",
    reason="Slow test: set ASTRA_RUN_SLOW_TESTS=1 to run",
)


class TestSentimentAnalyzer:
    def test_positive(self):
        from astra.nlp.sentiment import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze("I love this so much!")
        assert result.label == "POSITIVE"
        assert result.score > 0.5

    def test_negative(self):
        from astra.nlp.sentiment import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze("This is terrible and awful")
        assert result.label == "NEGATIVE"

    def test_batch(self):
        from astra.nlp.sentiment import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        results = analyzer.analyze_batch(["Great!", "Horrible."])
        assert len(results) == 2
