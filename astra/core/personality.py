"""Personality trait system.

Picks a random personality on each session start (or restores
a saved one). The personality affects the system prompt preamble,
which nudges the model's tone and style.
"""

from __future__ import annotations

import random

from astra.constants import MOOD_OPTIONS, TONE_OPTIONS
from astra.types import Personality
from astra.utils.logging import get_logger

_log = get_logger(__name__)


def random_personality() -> Personality:
    """Generate a random personality from the trait pools."""
    p = Personality(
        tone=random.choice(TONE_OPTIONS),
        mood=random.choice(MOOD_OPTIONS),
    )
    _log.debug(f"Generated personality: {p.describe()}")
    return p


def parse_personality(tone: str, mood: str) -> Personality:
    """Create a personality from explicit values (e.g., from config or CLI args)."""
    return Personality(tone=tone, mood=mood)


# some presets for common personality combos
PRESETS: dict[str, Personality] = {
    "default": Personality(tone="friendly", mood="cheerful"),
    "professional": Personality(tone="calm", mood="analytic"),
    "casual": Personality(tone="warm", mood="playful"),
    "edgy": Personality(tone="sarcastic", mood="deadpan"),
    "nerd": Personality(tone="enthusiastic", mood="analytic"),
    "zen": Personality(tone="thoughtful", mood="philosophical"),
}


def get_preset(name: str) -> Personality:
    """Look up a personality preset by name."""
    if name not in PRESETS:
        available = ", ".join(PRESETS.keys())
        raise ValueError(f"Unknown personality preset '{name}'. Available: {available}")
    return PRESETS[name]
