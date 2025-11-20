import streamlit as st

class SessionMemory:
    @staticmethod
    def init_session():
        if "user_session" not in st.session_state:
            st.session_state.user_session = {}

    @staticmethod
    def save_preferences(data: dict):
        if "user_session" not in st.session_state:
            st.session_state.user_session = {}
        st.session_state.user_session.update(data)

    @staticmethod
    def get_preferences():
        return st.session_state.get("user_session", {})