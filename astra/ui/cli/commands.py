"""CLI command handlers.

Each command is a function that takes the engine + args and
does its thing. Registered in a dict so the main loop can
dispatch by name.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from astra.ui.cli import formatters as fmt

if TYPE_CHECKING:
    from astra.core.engine import InferenceEngine

HELP_TEXT = """\
Commands:
  remember <text>   Save to long-term memory
  recall <query>    Search long-term memory
  history           Show conversation history
  clear             Clear conversation history
  personality       Show current personality
  status            Show session stats
  quit / exit       Exit
"""


def handle_help(**kwargs) -> None:
    print(HELP_TEXT)


def handle_remember(engine: InferenceEngine, args: str, **kwargs) -> None:
    if not args:
        print(fmt.warning("Usage: remember <text to store>"))
        return
    engine.store_memory(args, source="manual")
    print(fmt.bot_message("Got it, stored."))


def handle_recall(engine: InferenceEngine, args: str, **kwargs) -> None:
    if not args:
        print(fmt.warning("Usage: recall <search query>"))
        return
    results = engine.recall_memory(args, n=5)
    if results:
        for i, doc in enumerate(results, 1):
            print(f"  {i}. {doc}")
    else:
        print(fmt.info("  (nothing found)"))


def handle_history(engine: InferenceEngine, **kwargs) -> None:
    history = engine.memory.short_term.history
    if not history:
        print(fmt.info("  (no history yet)"))
        return
    for role, text in history:
        print(f"  {role}: {text}")


def handle_clear(engine: InferenceEngine, **kwargs) -> None:
    engine.clear_history()
    print(fmt.info("History cleared."))


def handle_personality(engine: InferenceEngine, **kwargs) -> None:
    p = engine.personality
    print(fmt.info(f"  Tone: {p.tone}"))
    print(fmt.info(f"  Mood: {p.mood}"))


def handle_status(engine: InferenceEngine, **kwargs) -> None:
    stats = engine.session.summary()
    for key, val in stats.items():
        print(fmt.info(f"  {key}: {val}"))

    if engine.memory.has_long_term:
        print(fmt.info(f"  long_term_memories: {engine.memory.long_term.size()}"))


# command dispatch table
COMMANDS: dict[str, callable] = {
    "help": handle_help,
    "remember": handle_remember,
    "recall": handle_recall,
    "history": handle_history,
    "clear": handle_clear,
    "personality": handle_personality,
    "status": handle_status,
}
