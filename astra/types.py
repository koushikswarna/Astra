"""Shared type aliases and protocols used across the codebase."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol, runtime_checkable


# conversation turn: (role, text)
Turn = tuple[str, str]

# raw embedding vector from sentence-transformers
Embedding = list[float]

# metadata dict attached to memories, pipeline results, etc.
Metadata = dict[str, Any]


class Role(str, Enum):
    """Speaker roles in a conversation."""
    USER = "User"
    ASSISTANT = "Astra"
    SYSTEM = "System"


@dataclass(frozen=True)
class Personality:
    """Immutable personality descriptor."""
    tone: str
    mood: str

    def describe(self) -> str:
        return f"{self.tone} and {self.mood}"


@dataclass
class ChatMessage:
    """A single message in a conversation."""
    role: Role
    content: str
    metadata: Metadata = field(default_factory=dict)

    @property
    def is_user(self) -> bool:
        return self.role == Role.USER


@dataclass
class GenerationResult:
    """Output from the text generation pipeline."""
    text: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    raw_output: str = ""


@dataclass
class SentimentResult:
    """Sentiment analysis output."""
    label: str = "NEUTRAL"
    score: float = 0.0

    def __str__(self) -> str:
        return f"{self.label} ({self.score:.2f})"


@dataclass
class ResponseBundle:
    """Everything produced by a single respond() call."""
    reply: str
    sentiment: SentimentResult | None = None
    recalled_memories: list[str] = field(default_factory=list)
    generation: GenerationResult | None = None


# ---- Protocols (structural typing for swappable components) ----

@runtime_checkable
class MemoryBackend(Protocol):
    """Any object that can store and retrieve text."""
    def store(self, text: str, metadata: Metadata | None = None) -> None: ...
    def search(self, query: str, n: int = 3) -> list[str]: ...


@runtime_checkable
class TextGeneratorProtocol(Protocol):
    """Anything that turns a prompt into text."""
    def generate(self, prompt: str, **kwargs: Any) -> str: ...


@runtime_checkable
class SentimentAnalyzerProtocol(Protocol):
    def analyze(self, text: str) -> SentimentResult: ...
