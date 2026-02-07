"""Shared test fixtures."""

import pytest
from pathlib import Path

from astra.config.base import AstraConfig, MemoryConfig
from astra.types import Personality


@pytest.fixture
def tmp_data_dir(tmp_path):
    """Temporary directory for test data."""
    return tmp_path / "astra_test"


@pytest.fixture
def test_config(tmp_data_dir):
    """AstraConfig pointing at temp directories so tests don't touch real data."""
    return AstraConfig(
        memory=MemoryConfig(
            memory_json_path=str(tmp_data_dir / "memory.json"),
            chroma_dir=str(tmp_data_dir / "chroma"),
        ),
        enable_long_term_memory=False,  # skip chromadb in unit tests
        enable_sentiment=False,  # skip model loading in unit tests
    )


@pytest.fixture
def sample_personality():
    return Personality(tone="friendly", mood="cheerful")


@pytest.fixture
def sample_turns():
    """A few conversation turns for testing."""
    return [
        ("User", "Hello there"),
        ("Astra", "Hi! How can I help?"),
        ("User", "What's the weather like?"),
        ("Astra", "I don't have access to weather data, but I hope it's nice!"),
    ]
