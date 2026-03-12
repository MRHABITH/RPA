"""Streamlit dashboard for AI Agent RPA system."""

from __future__ import annotations

from datetime import time

import streamlit as st

from backend.agent_controller import AgentController
from backend.database import add_task, get_bot_statuses, initialize_database

initialize_database()

st.set_page_config(page_title="AI RPA Dashboard", page_icon="🤖", layout="centered")
st.title("🤖 AI RPA Dashboard")
st.caption("Email Monitoring + Task Reminder Automation")

if "controller" not in st.session_state:
    st.session_state.controller = AgentController()
    st.session_state.controller.start()

controller: AgentController = st.session_state.controller

with st.sidebar:
    st.subheader("Add Reminder Task")
    task_title = st.text_input("Task title", placeholder="Submit report")
    task_time = st.time_input("Due time", value=time(hour=17, minute=0))
    if st.button("Save Task"):
        if task_title.strip():
            add_task(task_title, task_time.strftime("%H:%M"))
            st.success("Task added.")
        else:
            st.warning("Please enter a task title.")

st.header("Email Automation")
st.write("Latest Email Summary:")
st.info(controller.state.get("latest_email_summary", "No data yet."))

st.header("Reminder Automation")
st.write("Latest Reminder:")
st.info(controller.state.get("latest_reminder", "No data yet."))

st.header("Status")
statuses = get_bot_statuses()
if statuses:
    for row in statuses:
        st.write(f"**{row['bot_name']}**: {row['status']} (updated {row['last_updated']})")
else:
    st.write("Bots are starting...")

st.button("Refresh", help="Click to manually refresh dashboard")
