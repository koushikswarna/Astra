"""Microphone input and speech-to-text.

Uses the SpeechRecognition library with Google's web API for
recognition. Yeah, it phones home -- local whisper would be
better but that's a bigger dependency.
"""

from __future__ import annotations

import speech_recognition as sr

from astra.exceptions import ListenError
from astra.utils.logging import get_logger
from astra.voice.audio_config import AudioSettings

_log = get_logger(__name__)


class Listener:
    """Captures and transcribes microphone input."""

    def __init__(self, settings: AudioSettings | None = None):
        self.settings = settings or AudioSettings()
        self.recognizer = sr.Recognizer()

        # configure the recognizer
        self.recognizer.energy_threshold = self.settings.energy_threshold
        self.recognizer.dynamic_energy_threshold = self.settings.dynamic_energy
        self.recognizer.pause_threshold = self.settings.pause_threshold

    def listen(self) -> str:
        """Block until the user says something, then return the transcript.

        Returns empty string if nothing was understood.
        """
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(
                source, duration=self.settings.ambient_noise_duration
            )
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=self.settings.listen_timeout,
                    phrase_time_limit=self.settings.phrase_time_limit,
                )
            except sr.WaitTimeoutError:
                _log.debug("Listen timeout -- no speech detected")
                return ""

        return self._transcribe(audio)

    def _transcribe(self, audio: sr.AudioData) -> str:
        """Send audio to Google and get text back."""
        try:
            text = self.recognizer.recognize_google(audio)
            _log.info(f"Transcribed: {text}")
            return text
        except sr.UnknownValueError:
            _log.debug("Speech was unintelligible")
            return ""
        except sr.RequestError as exc:
            raise ListenError(
                f"Speech recognition API error (need internet?): {exc}"
            ) from exc
