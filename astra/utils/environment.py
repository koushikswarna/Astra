"""Runtime environment detection.

Figures out what hardware and optional deps are available
so the rest of the app can make informed decisions.
"""

import platform
import sys

from astra.utils.logging import get_logger

_log = get_logger(__name__)


def detect_device() -> str:
    """Return the best available torch device as a string."""
    try:
        import torch
        if torch.cuda.is_available():
            name = torch.cuda.get_device_name(0)
            _log.info(f"CUDA available: {name}")
            return "cuda"
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            _log.info("MPS (Apple Silicon) available")
            return "mps"
    except ImportError:
        pass
    return "cpu"


def is_package_available(name: str) -> bool:
    """Check if a Python package is importable without actually importing it."""
    from importlib.util import find_spec
    return find_spec(name) is not None


def check_optional_deps() -> dict[str, bool]:
    """Map of optional feature -> whether the required package exists."""
    return {
        "chromadb": is_package_available("chromadb"),
        "sentence_transformers": is_package_available("sentence_transformers"),
        "speech_recognition": is_package_available("speech_recognition"),
        "pyttsx3": is_package_available("pyttsx3"),
        "streamlit": is_package_available("streamlit"),
        "yaml": is_package_available("yaml"),
    }


def system_info() -> dict[str, str]:
    """Grab basic system info for debug/logging purposes."""
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor() or "unknown",
    }
