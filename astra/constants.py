"""Enumerations and constant values that don't belong in config.

Config is for tunable settings. This module is for things that
are baked into the application logic and shouldn't change at runtime.
"""

from enum import Enum, auto


class UIMode(str, Enum):
    CLI = "cli"
    STREAMLIT = "streamlit"


class MemoryType(Enum):
    SHORT_TERM = auto()
    LONG_TERM = auto()


class EventType(str, Enum):
    """Events emitted by the core engine."""
    PRE_GENERATE = "pre_generate"
    POST_GENERATE = "post_generate"
    MEMORY_STORE = "memory_store"
    MEMORY_RECALL = "memory_recall"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    VOICE_INPUT = "voice_input"
    VOICE_OUTPUT = "voice_output"
    ERROR = "error"


# personality trait pools
TONE_OPTIONS = [
    "curious", "sarcastic", "friendly", "calm",
    "enthusiastic", "thoughtful", "dry", "warm",
]

MOOD_OPTIONS = [
    "playful", "philosophical", "cheerful",
    "melancholic", "analytic", "deadpan", "earnest",
]

# keywords that trigger auto-save to long-term memory
MEMORY_TRIGGER_KEYWORDS = frozenset({
    "remember", "note that", "don't forget",
    "keep in mind", "save this", "store this",
})

# built-in CLI command names (used by the command registry)
BUILTIN_COMMANDS = frozenset({
    "help", "quit", "exit", "bye",
    "remember", "recall", "history",
    "clear", "personality", "status",
})
