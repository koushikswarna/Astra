"""Integration tests for the text generator.

These actually load the model so they're slow.
Skip in CI unless ASTRA_RUN_SLOW_TESTS is set.
"""

import os
import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("ASTRA_RUN_SLOW_TESTS") != "1",
    reason="Slow test: set ASTRA_RUN_SLOW_TESTS=1 to run",
)


class TestTextGenerator:
    def test_basic_generation(self):
        from astra.models.generator import TextGenerator
        gen = TextGenerator()
        result = gen.generate("The weather today is", max_new_tokens=20)
        assert result.text
        assert len(result.text) > 0

    def test_generation_result_fields(self):
        from astra.models.generator import TextGenerator
        gen = TextGenerator()
        result = gen.generate("Hello", max_new_tokens=10)
        assert result.prompt_tokens > 0
        assert result.completion_tokens > 0
