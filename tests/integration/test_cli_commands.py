"""Tests for CLI input parsing and command dispatch."""

from astra.ui.cli.parser import parse, ParsedInput


class TestParser:
    def test_quit_command(self):
        result = parse("quit")
        assert result.is_command
        assert result.command == "quit"

    def test_exit_command(self):
        result = parse("exit")
        assert result.is_command
        assert result.command == "quit"

    def test_help_command(self):
        result = parse("help")
        assert result.is_command
        assert result.command == "help"

    def test_remember_command(self):
        result = parse("remember my favorite color is blue")
        assert result.is_command
        assert result.command == "remember"
        assert result.args == "my favorite color is blue"

    def test_recall_command(self):
        result = parse("recall favorite color")
        assert result.is_command
        assert result.command == "recall"
        assert result.args == "favorite color"

    def test_regular_message(self):
        result = parse("hello how are you")
        assert not result.is_command
        assert result.raw == "hello how are you"

    def test_whitespace_handling(self):
        result = parse("  history  ")
        assert result.is_command
        assert result.command == "history"

    def test_case_insensitive(self):
        result = parse("QUIT")
        assert result.is_command
        assert result.command == "quit"

    def test_status_command(self):
        result = parse("status")
        assert result.is_command
        assert result.command == "status"
