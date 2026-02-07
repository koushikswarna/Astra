"""Tests for text utilities."""

from astra.utils.text import (
    contains_any,
    extract_first_response,
    sanitize,
    truncate,
    word_count,
)


class TestSanitize:
    def test_collapse_whitespace(self):
        assert sanitize("hello   world") == "hello world"

    def test_strip_newlines(self):
        assert sanitize("hello\n\nworld") == "hello world"

    def test_strip_edges(self):
        assert sanitize("  hello  ") == "hello"

    def test_empty(self):
        assert sanitize("") == ""


class TestTruncate:
    def test_short_text(self):
        assert truncate("hi", 10) == "hi"

    def test_long_text(self):
        result = truncate("a" * 100, 20)
        assert len(result) == 20
        assert result.endswith("...")

    def test_custom_suffix(self):
        result = truncate("a" * 100, 20, suffix="~")
        assert result.endswith("~")


class TestExtractFirstResponse:
    def test_no_markers(self):
        assert extract_first_response("hello world") == "hello world"

    def test_user_marker(self):
        result = extract_first_response("Sure thing! User: blah blah")
        assert result == "Sure thing!"

    def test_multiple_markers(self):
        result = extract_first_response("OK. Human: what User: something")
        assert result == "OK."

    def test_custom_markers(self):
        result = extract_first_response("Hi [END]more", stop_markers=["[END]"])
        assert result == "Hi"


class TestContainsAny:
    def test_match(self):
        assert contains_any("please remember this", {"remember", "note"})

    def test_no_match(self):
        assert not contains_any("hello world", {"remember", "note"})

    def test_case_insensitive(self):
        assert contains_any("REMEMBER THIS", {"remember"})


class TestWordCount:
    def test_basic(self):
        assert word_count("hello world") == 2

    def test_empty(self):
        assert word_count("") == 0
