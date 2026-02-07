"""Tests for input preprocessing."""

from astra.nlp.preprocessing import Preprocessor, preprocess


class TestPreprocessor:
    def test_basic_sanitization(self):
        p = Preprocessor()
        result = p.process("  hello   world  \n\n  test  ")
        assert result == "hello world test"

    def test_collapse_repeated_punctuation(self):
        p = Preprocessor()
        result = p.process("wow!!!!!!!")
        assert result == "wow!!!"

    def test_max_length(self):
        p = Preprocessor(max_input_length=10)
        result = p.process("a" * 100)
        assert len(result) == 10

    def test_strip_urls(self):
        p = Preprocessor()
        result = p.strip_urls("check out https://example.com for details")
        assert "[link]" in result
        assert "https://" not in result

    def test_empty_input(self):
        p = Preprocessor()
        result = p.process("")
        assert result == ""


class TestConvenienceFunction:
    def test_preprocess(self):
        result = preprocess("  hello  ")
        assert result == "hello"
