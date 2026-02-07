"""Streamlit sidebar panel.

Settings, controls, and debug info live here. Keeps the
main chat area clean.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

from astra.ui.web import state
from astra.ui.web.components import memory_count_badge

if TYPE_CHECKING:
    from astra.core.engine import InferenceEngine


def render_sidebar(engine: InferenceEngine) -> None:
    """Render the sidebar panel."""
    with st.sidebar:
        st.header("Astra")
        st.caption(f"Personality: {engine.personality.describe()}")

        st.divider()

        # session stats
        stats = engine.session.summary()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Turns", stats["turns"])
        with col2:
            st.metric("Session", stats["duration"])

        st.divider()

        # controls
        if st.button("Clear history", use_container_width=True):
            engine.clear_history()
            state.clear_messages()
            st.rerun()

        # long-term memory section
        if engine.memory.has_long_term:
            st.divider()
            st.subheader("Long-term memory")
            memory_count_badge(engine.memory.long_term.size())

            if st.button("Show stored memories", use_container_width=True):
                data = engine.memory.long_term.store.load()
                docs = data.get("documents", [])
                if docs:
                    for doc in docs:
                        st.text(f"- {doc}")
                else:
                    st.info("No stored memories yet.")

            if st.button("Clear long-term memory", use_container_width=True):
                engine.memory.long_term.clear()
                st.success("Long-term memory cleared.")
