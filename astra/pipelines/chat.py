"""The main chat pipeline.

Orchestrates the full flow from user input to assistant response:
preprocess -> sentiment -> context recall -> generate -> postprocess.

Each stage is modular and can be independently tested or replaced.
"""

from __future__ import annotations

from typing import Any

from astra.constants import MEMORY_TRIGGER_KEYWORDS
from astra.memory.manager import MemoryManager
from astra.models.generator import TextGenerator
from astra.nlp.filters import ContentFilter
from astra.nlp.postprocessing import Postprocessor
from astra.nlp.preprocessing import Preprocessor
from astra.nlp.sentiment import SentimentAnalyzer
from astra.pipelines.middleware import LoggingMiddleware, MiddlewareChain, TimingMiddleware
from astra.types import Personality, ResponseBundle, SentimentResult
from astra.utils.logging import get_logger
from astra.utils.text import contains_any

_log = get_logger(__name__)


class ChatPipeline:
    """End-to-end chat processing pipeline."""

    def __init__(
        self,
        generator: TextGenerator,
        memory: MemoryManager,
        personality: Personality,
        sentiment_analyzer: SentimentAnalyzer | None = None,
        content_filter: ContentFilter | None = None,
    ):
        self.generator = generator
        self.memory = memory
        self.personality = personality
        self.sentiment = sentiment_analyzer
        self.filter = content_filter or ContentFilter()
        self.preprocessor = Preprocessor()
        self.postprocessor = Postprocessor()

        # middleware chain wraps the core generation
        self._middleware = MiddlewareChain()
        self._middleware.add(LoggingMiddleware())
        self._middleware.add(TimingMiddleware())

    def run(self, user_text: str) -> ResponseBundle:
        """Process a user message through the full pipeline."""

        # step 1: preprocess
        cleaned = self.preprocessor.process(user_text)

        # step 1.5: content filter
        is_safe, reason = self.filter.check_input(cleaned)
        if not is_safe:
            _log.warning(f"Input blocked: {reason}")
            return ResponseBundle(reply="I can't process that input.")

        # step 2: sentiment analysis (if available)
        sentiment: SentimentResult | None = None
        if self.sentiment:
            try:
                sentiment = self.sentiment.analyze(cleaned)
            except Exception:
                _log.debug("Sentiment analysis failed, continuing without it")

        # step 3: recall relevant long-term memories
        recalled = self.memory.recall(cleaned, n=self.memory.config.recall_top_n)
        extra_context = ""
        if recalled:
            extra_context = "\n".join(f"(recalled: {doc})" for doc in recalled)

        # step 4: add user turn to history and build prompt
        self.memory.add_turn("User", cleaned)
        prompt = self.memory.build_prompt(self.personality, extra_context=extra_context)

        # step 5: generate via middleware chain
        def core_generate(ctx: dict[str, Any]) -> dict[str, Any]:
            result = self.generator.generate(ctx["prompt"])
            ctx["generation_result"] = result
            ctx["reply"] = result.text
            return ctx

        context = {"prompt": prompt, "user_text": cleaned}
        context = self._middleware.execute(context, core_generate)

        # step 6: postprocess the generated text
        raw_reply = context.get("reply", "")
        reply = self.postprocessor.process(raw_reply)
        reply = self.filter.check_output(reply)

        # step 7: store assistant response in history
        self.memory.add_turn("Astra", reply)
        self.memory.save()

        # step 8: auto-store to long-term memory if triggered
        if contains_any(user_text, MEMORY_TRIGGER_KEYWORDS):
            self.memory.store_long_term(cleaned, source="auto")

        return ResponseBundle(
            reply=reply,
            sentiment=sentiment,
            recalled_memories=recalled,
            generation=context.get("generation_result"),
        )
