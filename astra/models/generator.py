"""Text generation using a local transformer model.

This is where the actual inference happens. The generator
owns the model, tokenizer, and cache, and exposes a clean
generate() method that the rest of the app calls.
"""

from __future__ import annotations

import torch

from astra.config.model_config import GenerationConfig, ModelConfig
from astra.exceptions import GenerationError
from astra.models.base import BaseModel
from astra.models.cache import CacheManager
from astra.models.loader import ModelLoader
from astra.models.tokenization import TokenizerWrapper
from astra.types import GenerationResult
from astra.utils.logging import get_logger
from astra.utils.timing import timed

_log = get_logger(__name__)


class TextGenerator(BaseModel):
    """Local text generation using HuggingFace transformers."""

    def __init__(self, config: ModelConfig | None = None):
        self._config = config or ModelConfig()
        self._tokenizer = TokenizerWrapper(self._config.chat_model)
        self._loader = ModelLoader(self._config.chat_model)
        self._model = self._loader.load()
        self._cache = CacheManager()

    @timed(label="generation")
    def generate(self, prompt: str, **kwargs) -> GenerationResult:
        gen_cfg = self._config.generation

        # merge any per-call overrides with the config defaults
        max_new_tokens = kwargs.get("max_new_tokens", gen_cfg.max_new_tokens)
        temperature = kwargs.get("temperature", gen_cfg.temperature)
        top_p = kwargs.get("top_p", gen_cfg.top_p)

        inputs = self._tokenizer.encode(prompt)
        input_ids = inputs["input_ids"].to(self._loader.device_name)
        attention_mask = inputs["attention_mask"].to(self._loader.device_name)
        prompt_len = input_ids.shape[1]

        try:
            with torch.no_grad():
                output_ids = self._model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=max_new_tokens,
                    do_sample=gen_cfg.do_sample,
                    temperature=temperature,
                    top_p=top_p,
                    repetition_penalty=gen_cfg.repetition_penalty,
                    pad_token_id=self._tokenizer.pad_token_id,
                )
        except Exception as exc:
            raise GenerationError(f"Generation failed: {exc}") from exc

        full_text = self._tokenizer.decode(output_ids[0])
        completion_len = output_ids.shape[1] - prompt_len

        # strip the prompt from the output to get just the continuation
        if full_text.startswith(prompt):
            generated = full_text[len(prompt):].strip()
        else:
            generated = full_text.strip()

        # clear cache if memory pressure is building
        if self._cache.should_clear():
            self._cache.clear()

        return GenerationResult(
            text=generated,
            prompt_tokens=prompt_len,
            completion_tokens=completion_len,
            raw_output=full_text,
        )

    def warmup(self) -> None:
        """Run a short generation to warm up the model."""
        _log.debug("Warming up model...")
        self.generate("Hello", max_new_tokens=5)
        _log.debug("Warmup complete")

    @property
    def model_name(self) -> str:
        return self._config.chat_model

    @property
    def device(self) -> str:
        return self._loader.device_name

    def token_count(self, text: str) -> int:
        """How many tokens a text would consume."""
        return self._tokenizer.count_tokens(text)
