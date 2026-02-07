"""Exception hierarchy for Astra.

All custom exceptions inherit from AstraError so callers
can catch broadly or narrowly as needed.
"""


class AstraError(Exception):
    """Root of the exception tree."""


class ConfigError(AstraError):
    """Something is wrong with the configuration (missing file, bad value, etc.)."""


class ModelError(AstraError):
    """Model loading, inference, or tokenization failure."""


class ModelLoadError(ModelError):
    """Specifically failed to load a model from disk or HuggingFace hub."""


class GenerationError(ModelError):
    """The model produced no output or the generation call itself failed."""


class MemoryError_(AstraError):
    """Memory subsystem failure. Underscore to avoid shadowing builtin MemoryError."""


class ShortTermMemoryError(MemoryError_):
    """Problem with the conversation history buffer."""


class LongTermMemoryError(MemoryError_):
    """ChromaDB or embedding-related failure."""


class EmbeddingError(LongTermMemoryError):
    """Failed to produce an embedding vector."""


class StorageError(AstraError):
    """Persistence layer error (JSON, vector store, migrations)."""


class VoiceError(AstraError):
    """Speech recognition or TTS failure."""


class ListenError(VoiceError):
    """Microphone or speech recognition issue."""


class SpeakError(VoiceError):
    """TTS engine failure."""


class PipelineError(AstraError):
    """A pipeline step failed to process its input."""


class PluginError(AstraError):
    """Plugin loading or execution failure."""


class UIError(AstraError):
    """UI-layer error (CLI or web)."""
