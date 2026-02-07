"""Input validation helpers.

These run at system boundaries -- user input, config values,
external API responses. Internal code trusts internal data.
"""

from astra.exceptions import ConfigError


def validate_temperature(value: float) -> float:
    if not 0.0 < value <= 2.0:
        raise ConfigError(f"Temperature must be in (0, 2], got {value}")
    return value


def validate_max_tokens(value: int) -> int:
    if value < 1 or value > 4096:
        raise ConfigError(f"max_new_tokens must be in [1, 4096], got {value}")
    return value


def validate_nonempty(text: str, field_name: str = "input") -> str:
    text = text.strip()
    if not text:
        raise ValueError(f"{field_name} cannot be empty")
    return text


def validate_positive_int(value: int, field_name: str = "value") -> int:
    if value < 1:
        raise ConfigError(f"{field_name} must be >= 1, got {value}")
    return value
