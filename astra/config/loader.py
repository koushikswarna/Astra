"""Config loading from YAML file and environment variables.

Priority (highest wins):
  1. Explicit keyword args passed to load_config()
  2. Environment variables (ASTRA_*)
  3. YAML config file (~/.astra/config.yaml)
  4. Hardcoded defaults
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from astra.config.base import AstraConfig, MemoryConfig, VoiceConfig
from astra.config.model_config import GenerationConfig, ModelConfig
from astra.config.paths import CONFIG_FILE


def _load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML if the file exists and pyyaml is available."""
    if not path.exists():
        return {}
    try:
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else {}
    except ImportError:
        # pyyaml not installed, skip file-based config
        return {}


def _env_bool(key: str, default: bool) -> bool:
    val = os.environ.get(key, "").lower()
    if val in ("1", "true", "yes"):
        return True
    if val in ("0", "false", "no"):
        return False
    return default


def _env_int(key: str, default: int) -> int:
    val = os.environ.get(key)
    if val is not None:
        try:
            return int(val)
        except ValueError:
            pass
    return default


def _env_float(key: str, default: float) -> float:
    val = os.environ.get(key)
    if val is not None:
        try:
            return float(val)
        except ValueError:
            pass
    return default


def load_config(**overrides: Any) -> AstraConfig:
    """Build an AstraConfig from all sources.

    Keyword arguments take highest priority, then env vars, then YAML, then defaults.
    """
    yaml_data = _load_yaml(CONFIG_FILE)
    models_yaml = yaml_data.get("models", {})
    gen_yaml = models_yaml.get("generation", {})
    memory_yaml = yaml_data.get("memory", {})
    voice_yaml = yaml_data.get("voice", {})

    gen_config = GenerationConfig(
        max_new_tokens=_env_int("ASTRA_MAX_NEW_TOKENS", gen_yaml.get("max_new_tokens", GenerationConfig.max_new_tokens)),
        temperature=_env_float("ASTRA_TEMPERATURE", gen_yaml.get("temperature", GenerationConfig.temperature)),
        top_p=_env_float("ASTRA_TOP_P", gen_yaml.get("top_p", GenerationConfig.top_p)),
    )

    model_config = ModelConfig(
        chat_model=os.environ.get("ASTRA_CHAT_MODEL", models_yaml.get("chat_model", ModelConfig.chat_model)),
        embedding_model=os.environ.get("ASTRA_EMBEDDING_MODEL", models_yaml.get("embedding_model", ModelConfig.embedding_model)),
        sentiment_model=os.environ.get("ASTRA_SENTIMENT_MODEL", models_yaml.get("sentiment_model", ModelConfig.sentiment_model)),
        generation=gen_config,
    )

    memory_config = MemoryConfig(
        max_history=_env_int("ASTRA_MAX_HISTORY", memory_yaml.get("max_history", MemoryConfig.max_history)),
    )

    voice_config = VoiceConfig(
        tts_rate=_env_int("ASTRA_TTS_RATE", voice_yaml.get("tts_rate", VoiceConfig.tts_rate)),
        listen_timeout=_env_int("ASTRA_LISTEN_TIMEOUT", voice_yaml.get("listen_timeout", VoiceConfig.listen_timeout)),
        phrase_limit=_env_int("ASTRA_PHRASE_LIMIT", voice_yaml.get("phrase_limit", VoiceConfig.phrase_limit)),
    )

    cfg = AstraConfig(
        models=model_config,
        memory=memory_config,
        voice=voice_config,
        enable_voice=_env_bool("ASTRA_ENABLE_VOICE", yaml_data.get("enable_voice", False)),
        enable_long_term_memory=_env_bool("ASTRA_ENABLE_LTM", yaml_data.get("enable_long_term_memory", True)),
        enable_sentiment=_env_bool("ASTRA_ENABLE_SENTIMENT", yaml_data.get("enable_sentiment", True)),
        debug=_env_bool("ASTRA_DEBUG", yaml_data.get("debug", False)),
    )

    # apply any explicit overrides last
    for key, val in overrides.items():
        if hasattr(cfg, key):
            setattr(cfg, key, val)

    return cfg
