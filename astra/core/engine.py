"""Main inference engine.

This is the central coordinator -- it owns the pipeline, session,
hooks, and event bus. The UI layers (CLI, web) talk to this and
nothing else. If Astra has a brain, this is it.
"""

from __future__ import annotations

from astra.config.base import AstraConfig
from astra.constants import EventType
from astra.core.events import EventBus
from astra.core.hooks import HookManager
from astra.core.personality import random_personality
from astra.core.session import Session
from astra.memory.manager import MemoryManager
from astra.models.generator import TextGenerator
from astra.nlp.filters import ContentFilter
from astra.nlp.sentiment import SentimentAnalyzer
from astra.pipelines.chat import ChatPipeline
from astra.types import Personality, ResponseBundle
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class InferenceEngine:
    """Top-level engine that drives the assistant."""

    def __init__(self, config: AstraConfig, personality: Personality | None = None):
        self.config = config
        self.personality = personality or random_personality()

        _log.info("Initializing Astra engine...")

        # memory subsystem
        self.memory = MemoryManager(
            config=config.memory,
            enable_long_term=config.enable_long_term_memory,
            embedding_model=config.models.embedding_model,
        )

        # text generation
        self.generator = TextGenerator(config.models)

        # sentiment (optional, try and fall back)
        self.sentiment: SentimentAnalyzer | None = None
        if config.enable_sentiment:
            try:
                self.sentiment = SentimentAnalyzer(config.models.sentiment_model)
            except Exception as exc:
                _log.warning(f"Sentiment analysis unavailable: {exc}")

        # content filter
        self.filter = ContentFilter(enabled=True)

        # the chat pipeline ties everything together
        self.pipeline = ChatPipeline(
            generator=self.generator,
            memory=self.memory,
            personality=self.personality,
            sentiment_analyzer=self.sentiment,
            content_filter=self.filter,
        )

        # hooks and events for extensibility
        self.hooks = HookManager()
        self.events = EventBus()

        # session tracking
        self.session = Session(self.personality)
        self.events.emit(EventType.SESSION_START, {"session": self.session.summary()})

        _log.info(f"Engine ready (personality: {self.personality.describe()})")

    def respond(self, user_text: str) -> ResponseBundle:
        """Process a user message and generate a response.

        This is the main entry point that the UI calls.
        """
        # run pre-hooks (can reject or modify input)
        modified = self.hooks.run_pre_hooks(user_text)
        if modified is None:
            return ResponseBundle(reply="That input was filtered out.")
        user_text = modified

        # run the pipeline
        response = self.pipeline.run(user_text)

        # run post-hooks
        response = self.hooks.run_post_hooks(response)

        # track in session
        self.session.record_response(response)
        self.events.emit(EventType.POST_GENERATE, {
            "turn": self.session.turn_count,
            "reply_length": len(response.reply),
        })

        return response

    def store_memory(self, text: str, source: str = "user") -> None:
        """Explicitly store something in long-term memory."""
        self.memory.store_long_term(text, source=source)
        self.events.emit(EventType.MEMORY_STORE, {"text": text[:50]})

    def recall_memory(self, query: str, n: int = 5) -> list[str]:
        """Search long-term memory."""
        results = self.memory.recall(query, n=n)
        self.events.emit(EventType.MEMORY_RECALL, {"query": query, "results": len(results)})
        return results

    def clear_history(self) -> None:
        self.memory.clear_history()

    def shutdown(self) -> None:
        """Clean shutdown -- save state and emit session end."""
        self.memory.save()
        self.events.emit(EventType.SESSION_END, {"session": self.session.summary()})
        _log.info(f"Session {self.session.id} ended after {self.session.turn_count} turns")
