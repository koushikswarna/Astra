"""CLI input parsing.

Determines whether user input is a command (like "remember X")
or a regular chat message. Keeps the main loop clean.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ParsedInput:
    """Result of parsing user input."""
    is_command: bool
    command: str = ""
    args: str = ""
    raw: str = ""


def parse(text: str) -> ParsedInput:
    """Parse user input into a command or chat message.

    Commands are detected by matching against known prefixes.
    Everything else is treated as a regular message.
    """
    stripped = text.strip()
    lower = stripped.lower()

    # exit commands
    if lower in ("quit", "exit", "bye"):
        return ParsedInput(is_command=True, command="quit", raw=stripped)

    # single-word commands
    single_commands = {"help", "history", "clear", "status", "personality"}
    if lower in single_commands:
        return ParsedInput(is_command=True, command=lower, raw=stripped)

    # prefix commands (command + argument)
    prefix_commands = {"remember", "recall"}
    for cmd in prefix_commands:
        if lower.startswith(cmd + " "):
            args = stripped[len(cmd):].strip()
            return ParsedInput(is_command=True, command=cmd, args=args, raw=stripped)

    # not a command
    return ParsedInput(is_command=False, raw=stripped)
