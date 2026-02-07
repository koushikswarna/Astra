"""Chat rendering for the Streamlit web UI.

Handles displaying the conversation and processing new
messages through the engine.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

from astra.ui.web import state
from astra.ui.web.components import (
    empty_state_message,
    render_chat_message,
    render_sentiment,
    render_thinking_spinner,
)

if TYPE_CHECKING:
    from astra.core.engine import InferenceEngine


def render_chat_history() -> None:
    """Render all messages in the session."""
    messages = state.get_messages()
    if not messages:
        empty_state_message()
        return

    for role, text in messages:
        render_chat_message(role, text)


def handle_chat_input(engine: InferenceEngine) -> None:
    """Process new chat input from the user."""
    if prompt := st.chat_input("Say something..."):
        # show user message immediately
        render_chat_message("User", prompt)
        state.add_message("User", prompt)

        # generate response
        with st.chat_message("assistant"):
            with render_thinking_spinner():
                response = engine.respond(prompt)

            st.write(response.reply)
            render_sentiment(response.sentiment)

        state.add_message("Astra", response.reply)
