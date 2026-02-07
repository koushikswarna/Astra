"""Default values for every config field.

Kept separate from the dataclass so we can reference these
in tests and in the config loader without constructing a full object.
"""

DEFAULT_MODEL_NAME = "microsoft/DialoGPT-medium"
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"

DEFAULT_MAX_HISTORY = 8
DEFAULT_TEMPERATURE = 0.75
DEFAULT_MAX_NEW_TOKENS = 80
DEFAULT_TOP_P = 0.92

DEFAULT_TTS_RATE = 170
DEFAULT_LISTEN_TIMEOUT = 5
DEFAULT_PHRASE_LIMIT = 10

DEFAULT_CHROMA_COLLECTION = "astra_memory"
DEFAULT_MEMORY_FILENAME = "memory.json"
DEFAULT_CHROMA_DIRNAME = "chroma_store"
