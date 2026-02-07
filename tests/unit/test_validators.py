"""Tests for input validators."""

import pytest

from astra.exceptions import ConfigError
from astra.utils.validators import (
    validate_max_tokens,
    validate_nonempty,
    validate_positive_int,
    validate_temperature,
)


class TestValidateTemperature:
    def test_valid(self):
        assert validate_temperature(0.7) == 0.7
        assert validate_temperature(2.0) == 2.0

    def test_zero(self):
        with pytest.raises(ConfigError):
            validate_temperature(0.0)

    def test_too_high(self):
        with pytest.raises(ConfigError):
            validate_temperature(3.0)


class TestValidateMaxTokens:
    def test_valid(self):
        assert validate_max_tokens(128) == 128

    def test_zero(self):
        with pytest.raises(ConfigError):
            validate_max_tokens(0)

    def test_too_high(self):
        with pytest.raises(ConfigError):
            validate_max_tokens(10000)


class TestValidateNonempty:
    def test_valid(self):
        assert validate_nonempty("hello") == "hello"

    def test_empty(self):
        with pytest.raises(ValueError):
            validate_nonempty("")

    def test_whitespace_only(self):
        with pytest.raises(ValueError):
            validate_nonempty("   ")


class TestValidatePositiveInt:
    def test_valid(self):
        assert validate_positive_int(5) == 5

    def test_zero(self):
        with pytest.raises(ConfigError):
            validate_positive_int(0)
