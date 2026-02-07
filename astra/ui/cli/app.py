"""Main CLI application loop.

This is where the terminal interaction happens. Reads input,
dispatches commands, and prints responses. The engine does
all the heavy lifting -- this is just the I/O layer.
"""

from __future__ import annotations

from astra.config import AstraConfig, load_config
from astra.core.engine import InferenceEngine
from astra.ui.cli.commands import COMMANDS
from astra.ui.cli.parser import parse
from astra.ui.cli import formatters as fmt
from astra.ui.cli.repl import safe_input, setup_readline
from astra.utils.logging import get_logger, setup_logging

_log = get_logger(__name__)


def run(voice: bool = False, config: AstraConfig | None = None) -> None:
    """Start the CLI chat loop."""
    setup_logging()
    setup_readline()

    cfg = config or load_config(enable_voice=voice)
    engine = InferenceEngine(cfg)

    # voice setup (lazy import so we don't pull in pyttsx3 unless needed)
    voice_io = None
    if voice and cfg.enable_voice:
        try:
            from astra.voice.engine import VoiceEngine
            voice_io = VoiceEngine()
            voice_io.greet()
        except Exception as exc:
            print(fmt.warning(f"Voice unavailable: {exc}"))

    print(fmt.bot_message("Hello! Type 'help' for commands, 'quit' to exit."))

    while True:
        # get input (text or voice)
        user_input = _get_input(voice_io)
        if user_input is None:
            # EOF or interrupt
            break

        if not user_input.strip():
            continue

        # parse and dispatch
        parsed = parse(user_input)

        if parsed.is_command:
            if parsed.command == "quit":
                engine.shutdown()
                print(fmt.bot_message("See you later."))
                break

            handler = COMMANDS.get(parsed.command)
            if handler:
                handler(engine=engine, args=parsed.args)
            else:
                print(fmt.warning(f"Unknown command: {parsed.command}"))
            continue

        # regular chat message
        response = engine.respond(user_input)
        print(fmt.bot_message(response.reply))

        if response.sentiment:
            print(fmt.sentiment_badge(response.sentiment.label, response.sentiment.score))

        # speak the response if voice is active
        if voice_io:
            voice_io.speak(response.reply)


def _get_input(voice_io=None) -> str | None:
    """Get user input from keyboard or microphone."""
    if voice_io:
        choice = safe_input("(enter to type, 'v' to speak): ")
        if choice is None:
            return None
        if choice.strip().lower() == "v":
            text = voice_io.listen()
            if not text:
                print(fmt.info("Didn't catch that. Try typing."))
                return ""
            return text

    return safe_input(fmt.user_prompt())
