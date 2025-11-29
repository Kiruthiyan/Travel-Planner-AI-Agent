import streamlit as st

class SessionMemory:
    @staticmethod
    def init_session():
        """Initialize the session memory for user preferences."""
        st.session_state.setdefault("user_session", {})

    @staticmethod
    def save_preferences(data: dict):
        """Update session memory with new preferences."""
        st.session_state.setdefault("user_session", {})
        st.session_state.user_session.update(data)

    @staticmethod
    def get_preferences() -> dict:
        """Retrieve current session preferences."""
        return st.session_state.get("user_session", {})
