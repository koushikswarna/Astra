"""JSON file storage backend.

Used for short-term memory persistence. Nothing fancy -- just
json.dump and json.load with some safety around missing files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from astra.exceptions import StorageError
from astra.storage.base import StorageBackend
from astra.utils.logging import get_logger

_log = get_logger(__name__)


class JSONStore(StorageBackend):

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(self, data: Any, **kwargs) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # atomic-ish rename so we don't corrupt on crash
            tmp.rename(self.path)
        except (OSError, TypeError) as exc:
            raise StorageError(f"Failed to save JSON to {self.path}: {exc}") from exc

    def load(self, **kwargs) -> Any:
        if not self.path.exists():
            return None
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            _log.warning(f"Corrupt or unreadable JSON at {self.path}: {exc}")
            return None

    def clear(self) -> None:
        if self.path.exists():
            self.path.unlink()
            _log.debug(f"Deleted {self.path}")

    def exists(self) -> bool:
        return self.path.exists() and self.path.stat().st_size > 0
