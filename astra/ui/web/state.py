"""Streamlit session state management.

Wraps st.session_state with typed accessors so the rest of
the web UI doesn't have to deal with KeyError checks everywhere.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    pass

# session state keys
_MESSAGES_KEY = "messages"
_INITIALIZED_KEY = "initialized"


def initialize() -> None:
    """Set up session state on first load."""
    if _INITIALIZED_KEY not in st.session_state:
        st.session_state[_MESSAGES_KEY] = []
        st.session_state[_INITIALIZED_KEY] = True


def get_messages() -> list[tuple[str, str]]:
    """Get the message history from session state."""
    return st.session_state.get(_MESSAGES_KEY, [])


def add_message(role: str, text: str) -> None:
    """Append a message to session state."""
    if _MESSAGES_KEY not in st.session_state:
        st.session_state[_MESSAGES_KEY] = []
    st.session_state[_MESSAGES_KEY].append((role, text))


def clear_messages() -> None:
    """Wipe the session message history."""
    st.session_state[_MESSAGES_KEY] = []
