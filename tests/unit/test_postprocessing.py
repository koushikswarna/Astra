"""Tests for output postprocessing."""

from astra.nlp.postprocessing import Postprocessor, postprocess


class TestPostprocessor:
    def test_stop_at_user_marker(self):
        p = Postprocessor()
        result = p.process("Hello! User: How are you?")
        assert "User:" not in result
        assert "Hello!" in result

    def test_empty_gives_fallback(self):
        p = Postprocessor()
        result = p.process("")
        assert result  # should return a fallback message

    def test_strips_whitespace(self):
        p = Postprocessor()
        result = p.process("  hello  ")
        assert result == "hello"

    def test_incomplete_sentence_trimming(self):
        p = Postprocessor()
        result = p.process("This is a full sentence. This one is incompl")
        assert result.endswith(".")

    def test_complete_sentence_preserved(self):
        p = Postprocessor()
        result = p.process("This is complete.")
        assert result == "This is complete."


class TestConvenienceFunction:
    def test_postprocess(self):
        result = postprocess("Hi there! User: blah")
        assert "User:" not in result
