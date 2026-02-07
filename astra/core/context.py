"""Context window management.

Handles building the prompt context from multiple sources
(conversation history, recalled memories, system instructions)
while staying within the model's token budget.
"""

from __future__ import annotations

from astra.memory.manager import MemoryManager
from astra.types import Personality
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class ContextBuilder:
    """Constructs the prompt context for generation."""

    def __init__(
        self,
        memory: MemoryManager,
        personality: Personality,
        max_context_chars: int = 2048,
    ):
        self.memory = memory
        self.personality = personality
        self.max_context_chars = max_context_chars

    def build(self, user_text: str) -> str:
        """Build the full prompt context for a user message.

        Order of assembly:
        1. System preamble (personality)
        2. Recalled long-term memories (if any)
        3. Conversation history (already includes the current user message)
        4. "Astra:" prompt suffix
        """
        # recall relevant memories first
        recalled = self.memory.recall(user_text, n=3)
        extra = ""
        if recalled:
            extra = "\n".join(f"(recalled: {doc})" for doc in recalled)

        # add user message to history
        self.memory.add_turn("User", user_text)

        # build the prompt
        prompt = self.memory.build_prompt(self.personality, extra_context=extra)

        # rough length check
        if len(prompt) > self.max_context_chars:
            _log.warning(
                f"Prompt is {len(prompt)} chars (limit: {self.max_context_chars}). "
                f"Older history may be needed to be trimmed."
            )

        return prompt

    def get_recalled_memories(self, query: str) -> list[str]:
        """Get relevant memories without building a full prompt."""
        return self.memory.recall(query, n=3)
