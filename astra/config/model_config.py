"""Model-specific configuration.

Keeps model settings isolated so we can swap models
without touching the rest of the config hierarchy.
"""

from dataclasses import dataclass

from astra.config.defaults import (
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_MAX_NEW_TOKENS,
    DEFAULT_MODEL_NAME,
    DEFAULT_SENTIMENT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
)


@dataclass
class GenerationConfig:
    """Controls text generation behavior."""
    max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    top_p: float = DEFAULT_TOP_P
    do_sample: bool = True
    repetition_penalty: float = 1.1


@dataclass
class ModelConfig:
    """Which models to load and how to configure them."""
    chat_model: str = DEFAULT_MODEL_NAME
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    sentiment_model: str = DEFAULT_SENTIMENT_MODEL
    generation: GenerationConfig = None  # type: ignore[assignment]

    def __post_init__(self):
        if self.generation is None:
            self.generation = GenerationConfig()
