"""Tests for the personality system."""

import pytest

from astra.core.personality import (
    PRESETS,
    get_preset,
    parse_personality,
    random_personality,
)
from astra.types import Personality


class TestRandomPersonality:
    def test_returns_personality(self):
        p = random_personality()
        assert isinstance(p, Personality)
        assert p.tone
        assert p.mood

    def test_randomness(self):
        # generate a bunch and check we get at least 2 different ones
        personalities = {random_personality().describe() for _ in range(20)}
        assert len(personalities) > 1


class TestPresets:
    def test_get_valid_preset(self):
        p = get_preset("professional")
        assert p.tone == "calm"
        assert p.mood == "analytic"

    def test_get_invalid_preset(self):
        with pytest.raises(ValueError, match="Unknown personality preset"):
            get_preset("nonexistent")

    def test_all_presets_are_valid(self):
        for name, p in PRESETS.items():
            assert isinstance(p, Personality)
            assert p.tone
            assert p.mood


class TestParsePersonality:
    def test_parse(self):
        p = parse_personality("curious", "playful")
        assert p.tone == "curious"
        assert p.mood == "playful"
