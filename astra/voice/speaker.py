"""Text-to-speech output.

Uses pyttsx3 for offline TTS. The quality isn't amazing but
it works without an internet connection, which is kind of the
whole point of a local assistant.
"""

from __future__ import annotations

import threading

import pyttsx3

from astra.exceptions import SpeakError
from astra.utils.logging import get_logger
from astra.voice.audio_config import AudioSettings

_log = get_logger(__name__)


class Speaker:
    """Speaks text aloud using the system TTS engine."""

    def __init__(self, settings: AudioSettings | None = None):
        self.settings = settings or AudioSettings()
        self._engine = pyttsx3.init()
        self._configure()
        self._lock = threading.Lock()

    def _configure(self) -> None:
        self._engine.setProperty("rate", self.settings.tts_rate)
        self._engine.setProperty("volume", self.settings.tts_volume)

        voices = self._engine.getProperty("voices")
        if voices and self.settings.voice_index < len(voices):
            self._engine.setProperty("voice", voices[self.settings.voice_index].id)

    def speak(self, text: str, blocking: bool = False) -> None:
        """Say something. Runs in a background thread by default."""
        if blocking:
            self._speak_sync(text)
        else:
            thread = threading.Thread(target=self._speak_sync, args=(text,), daemon=True)
            thread.start()

    def _speak_sync(self, text: str) -> None:
        """Actually run the TTS engine. Thread-safe via lock."""
        with self._lock:
            try:
                self._engine.say(text)
                self._engine.runAndWait()
            except Exception as exc:
                raise SpeakError(f"TTS failed: {exc}") from exc

    @property
    def available_voices(self) -> list[str]:
        """List available system voices by name."""
        voices = self._engine.getProperty("voices")
        return [v.name for v in voices] if voices else []
