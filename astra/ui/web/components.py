"""Reusable Streamlit UI components.

Small building blocks that get assembled into pages.
Keeps the main app.py from turning into a wall of st.* calls.
"""

from __future__ import annotations

import streamlit as st

from astra.types import SentimentResult


def render_chat_message(role: str, text: str) -> None:
    """Render a single chat message with the appropriate avatar."""
    st_role = "user" if role == "User" else "assistant"
    with st.chat_message(st_role):
        st.write(text)


def render_sentiment(sentiment: SentimentResult | None) -> None:
    """Show sentiment as a caption below a message."""
    if sentiment:
        st.caption(f"Sentiment: {sentiment}")


def render_thinking_spinner():
    """Context manager for the 'thinking' state."""
    return st.spinner("Thinking...")


def memory_count_badge(count: int) -> None:
    """Show how many long-term memories are stored."""
    st.metric("Stored memories", count)


def empty_state_message() -> None:
    """Shown when there's no conversation yet."""
    st.markdown(
        "<div style='text-align: center; color: #888; padding: 2em;'>"
        "Start a conversation below.</div>",
        unsafe_allow_html=True,
    )
