"""Voice I/O coordinator.

Ties together the listener and speaker into a single interface
that the rest of the app uses. Handles the "is voice available?"
question so nobody else has to.
"""

from __future__ import annotations

from astra.utils.logging import get_logger
from astra.voice.audio_config import AudioSettings
from astra.voice.listener import Listener
from astra.voice.speaker import Speaker

_log = get_logger(__name__)


class VoiceEngine:
    """Unified voice input/output."""

    def __init__(self, settings: AudioSettings | None = None):
        self.settings = settings or AudioSettings()
        self.listener = Listener(self.settings)
        self.speaker = Speaker(self.settings)
        _log.info("Voice engine initialized")

    def listen(self) -> str:
        """Capture speech from the microphone."""
        text = self.listener.listen()
        if text:
            print(f"Heard: {text}")
        return text

    def speak(self, text: str, blocking: bool = False) -> None:
        """Speak text aloud."""
        self.speaker.speak(text, blocking=blocking)

    def greet(self) -> None:
        """Say the startup greeting."""
        self.speak("Hello, I'm Astra. Voice mode is active.")

    @staticmethod
    def is_available() -> bool:
        """Check if voice dependencies are installed."""
        try:
            import speech_recognition  # noqa: F401
            import pyttsx3  # noqa: F401
            return True
        except ImportError:
            return False
