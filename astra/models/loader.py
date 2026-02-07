"""Model loading and device placement.

Separated from the generation logic so we can eventually
support multiple model backends (GGUF, ONNX, API) without
touching the generator code.
"""

from __future__ import annotations

import torch
from transformers import AutoModelForCausalLM

from astra.exceptions import ModelLoadError
from astra.utils.environment import detect_device
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class ModelLoader:
    """Loads a causal LM and places it on the best available device."""

    def __init__(self, model_name: str, device: str | None = None):
        self.model_name = model_name
        self.device_name = device or detect_device()
        self._model = None

    def load(self) -> torch.nn.Module:
        """Download (if needed) and load the model onto the target device."""
        if self._model is not None:
            return self._model

        _log.info(f"Loading model: {self.model_name}")
        try:
            model = AutoModelForCausalLM.from_pretrained(self.model_name)
        except Exception as exc:
            raise ModelLoadError(
                f"Failed to load {self.model_name}. "
                f"Is the model name correct? Do you have internet for first download? "
                f"Error: {exc}"
            ) from exc

        device = torch.device(self.device_name)
        model.to(device)
        model.eval()

        self._model = model
        _log.info(f"Model loaded on {device}")
        return model

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def unload(self) -> None:
        """Free model memory."""
        if self._model is not None:
            del self._model
            self._model = None
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            _log.info("Model unloaded")
