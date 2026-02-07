"""Audio-related configuration.

Separate from the main config hierarchy because voice is entirely
optional and most users won't touch these values.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AudioSettings:
    """Low-level audio parameters."""
    sample_rate: int = 16000
    channels: int = 1

    # speech recognition
    energy_threshold: int = 300
    dynamic_energy: bool = True
    pause_threshold: float = 0.8

    # TTS
    tts_rate: int = 170
    tts_volume: float = 1.0
    voice_index: int = 0

    # timeouts
    listen_timeout: int = 5
    phrase_time_limit: int = 10
    ambient_noise_duration: float = 0.5
