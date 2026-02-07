"""NLP processing -- sentiment, pre/post processing, content filters.

Sentiment analysis import is lazy since it loads a transformers model.
"""

from astra.nlp.preprocessing import Preprocessor
from astra.nlp.postprocessing import Postprocessor

__all__ = ["SentimentAnalyzer", "Preprocessor", "Postprocessor"]


def __getattr__(name):
    if name == "SentimentAnalyzer":
        from astra.nlp.sentiment import SentimentAnalyzer
        return SentimentAnalyzer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
