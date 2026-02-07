"""Tests for the config system."""

import os
import pytest

from astra.config.base import AstraConfig, MemoryConfig, VoiceConfig
from astra.config.defaults import DEFAULT_MAX_HISTORY, DEFAULT_TEMPERATURE
from astra.config.model_config import GenerationConfig, ModelConfig
from astra.config.loader import load_config, _env_bool, _env_int, _env_float


class TestDefaults:
    def test_generation_config_defaults(self):
        cfg = GenerationConfig()
        assert cfg.temperature == DEFAULT_TEMPERATURE
        assert cfg.do_sample is True

    def test_model_config_creates_generation(self):
        cfg = ModelConfig()
        assert cfg.generation is not None
        assert isinstance(cfg.generation, GenerationConfig)

    def test_astra_config_defaults(self):
        cfg = AstraConfig()
        assert cfg.enable_sentiment is True
        assert cfg.enable_long_term_memory is True
        assert cfg.debug is False


class TestEnvHelpers:
    def test_env_bool_true(self, monkeypatch):
        monkeypatch.setenv("TEST_BOOL", "true")
        assert _env_bool("TEST_BOOL", False) is True

    def test_env_bool_false(self, monkeypatch):
        monkeypatch.setenv("TEST_BOOL", "0")
        assert _env_bool("TEST_BOOL", True) is False

    def test_env_bool_default(self):
        assert _env_bool("NONEXISTENT_KEY_123", True) is True

    def test_env_int(self, monkeypatch):
        monkeypatch.setenv("TEST_INT", "42")
        assert _env_int("TEST_INT", 0) == 42

    def test_env_int_invalid(self, monkeypatch):
        monkeypatch.setenv("TEST_INT", "not_a_number")
        assert _env_int("TEST_INT", 99) == 99

    def test_env_float(self, monkeypatch):
        monkeypatch.setenv("TEST_FLOAT", "0.75")
        assert _env_float("TEST_FLOAT", 0.0) == 0.75


class TestLoadConfig:
    def test_load_with_overrides(self):
        cfg = load_config(debug=True, enable_voice=True)
        assert cfg.debug is True
        assert cfg.enable_voice is True

    def test_load_default(self):
        cfg = load_config()
        assert isinstance(cfg, AstraConfig)
        assert cfg.memory.max_history == DEFAULT_MAX_HISTORY
