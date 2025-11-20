import streamlit as st
from datetime import datetime
import os

def format_datetime(dt):
    """Formats a date object into a readable string."""
    # st.date_input returns a date object, converting to string ensures format matches
    return datetime.strptime(str(dt), "%Y-%m-%d").strftime("%b %d, %Y")

def log_agent(name, message):
    """Logs agent actions to a text file."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    with open(f"{log_dir}/agent_logs.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%H:%M:%S")
        f.write(f"[{timestamp}] [{name}] {message}\n")