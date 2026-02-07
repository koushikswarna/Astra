"""Streamlit web application entry point.

This is what gets called when you run:
    streamlit run main.py -- --ui streamlit

The engine is cached with @st.cache_resource so the model
only loads once, not on every Streamlit rerun.
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Astra", layout="wide", page_icon="*")


@st.cache_resource
def _get_engine():
    """Create the engine once and cache it across reruns.

    This is critical -- without caching, the model would reload
    every time the user sends a message.
    """
    from astra.config import load_config
    from astra.core.engine import InferenceEngine
    from astra.utils.logging import setup_logging

    setup_logging()
    config = load_config(enable_voice=False)
    return InferenceEngine(config)


def run() -> None:
    """Main Streamlit app."""
    from astra.ui.web import state
    from astra.ui.web.chat import handle_chat_input, render_chat_history
    from astra.ui.web.sidebar import render_sidebar

    state.initialize()
    engine = _get_engine()

    st.title("Astra")

    render_sidebar(engine)
    render_chat_history()
    handle_chat_input(engine)
