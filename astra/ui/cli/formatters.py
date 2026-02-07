"""Output formatting for the CLI.

ANSI colors and text formatting to make the terminal output
look decent. Nothing fancy -- no curses, no rich, just raw
escape codes.
"""

from __future__ import annotations

import sys

# ANSI color codes
_COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "cyan": "\033[36m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "red": "\033[31m",
    "magenta": "\033[35m",
    "blue": "\033[34m",
}

# disable colors if not a real terminal
_USE_COLOR = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    if not _USE_COLOR:
        return text
    return f"{_COLORS.get(code, '')}{text}{_COLORS['reset']}"


def bot_message(text: str) -> str:
    return f"{_c('cyan', 'Astra:')} {text}"


def user_prompt() -> str:
    return _c("green", "You: ")


def info(text: str) -> str:
    return _c("dim", text)


def warning(text: str) -> str:
    return _c("yellow", text)


def error(text: str) -> str:
    return _c("red", text)


def sentiment_badge(label: str, score: float) -> str:
    return _c("dim", f"  [{label} {score:.2f}]")


def header(text: str) -> str:
    return _c("bold", text)


def divider(char: str = "-", width: int = 40) -> str:
    return _c("dim", char * width)
