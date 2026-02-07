"""Top-level configuration object.

Everything flows through AstraConfig. Components receive
the specific sub-config they need rather than the whole thing.
"""

from dataclasses import dataclass, field

from astra.config.defaults import (
    DEFAULT_CHROMA_COLLECTION,
    DEFAULT_LISTEN_TIMEOUT,
    DEFAULT_MAX_HISTORY,
    DEFAULT_PHRASE_LIMIT,
    DEFAULT_TTS_RATE,
)
from astra.config.model_config import ModelConfig
from astra.config.paths import CHROMA_DIR_PATH, MEMORY_JSON_PATH


@dataclass
class VoiceConfig:
    tts_rate: int = DEFAULT_TTS_RATE
    listen_timeout: int = DEFAULT_LISTEN_TIMEOUT
    phrase_limit: int = DEFAULT_PHRASE_LIMIT
    voice_index: int = 0  # which system voice to pick


@dataclass
class MemoryConfig:
    max_history: int = DEFAULT_MAX_HISTORY
    memory_json_path: str = str(MEMORY_JSON_PATH)
    chroma_dir: str = str(CHROMA_DIR_PATH)
    chroma_collection: str = DEFAULT_CHROMA_COLLECTION
    recall_top_n: int = 3


@dataclass
class AstraConfig:
    """Master config. Built by the loader, consumed by the app factory."""
    models: ModelConfig = field(default_factory=ModelConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    voice: VoiceConfig = field(default_factory=VoiceConfig)

    enable_voice: bool = False
    enable_long_term_memory: bool = True
    enable_sentiment: bool = True

    debug: bool = False
