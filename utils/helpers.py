import streamlit as st
from datetime import datetime
import os

def log_agent(name, message):
    """Logs agent actions to a text file with full timestamp."""
    log_dir = "logs"
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(f"{log_dir}/agent_logs.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{name}] {message}\n")
    except Exception as e:
        st.warning(f"Failed to log message: {e}")
