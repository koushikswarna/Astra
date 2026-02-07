"""Data format migrations.

When the memory JSON schema changes between versions, this module
handles upgrading old formats to the current one. Not exactly
Alembic, but it gets the job done for a local app.
"""

from __future__ import annotations

from typing import Any

from astra.utils.logging import get_logger

_log = get_logger(__name__)

# current schema version for the memory JSON
CURRENT_VERSION = 2


def detect_version(data: Any) -> int:
    """Figure out what schema version a loaded JSON blob is."""
    if data is None:
        return CURRENT_VERSION  # nothing to migrate

    # v1: the original format was {"history": [["User", "text"], ...]}
    if isinstance(data, dict) and "history" in data:
        return 1

    # v2: bare list of [role, text] tuples
    if isinstance(data, list):
        return 2

    # unknown format, treat as current
    _log.warning(f"Unrecognized memory format (type={type(data).__name__}), treating as v{CURRENT_VERSION}")
    return CURRENT_VERSION


def migrate(data: Any) -> list[list[str]]:
    """Migrate data to the current schema (v2: bare list of turns).

    Returns the migrated data, ready for ShortTermMemory to consume.
    """
    version = detect_version(data)

    if version == CURRENT_VERSION:
        if data is None:
            return []
        return data  # type: ignore[return-value]

    if version == 1:
        _log.info("Migrating memory from v1 (dict wrapper) to v2 (bare list)")
        history = data.get("history", [])
        return history

    # shouldn't get here, but be safe
    return []
