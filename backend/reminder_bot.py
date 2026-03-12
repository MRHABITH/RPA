"""Task reminder bot that checks due times and emits reminders."""

from __future__ import annotations

from datetime import datetime

from backend.database import get_pending_tasks, mark_task_notified, update_bot_status
from backend.groq_ai import generate_reminder


def run_reminder_bot(state: dict) -> None:
    """Find due tasks and create AI reminder messages."""
    update_bot_status("Reminder Bot", "Running")
    now_hm = datetime.now().strftime("%H:%M")
    pending = get_pending_tasks()

    triggered = None
    for task in pending:
        if task["due_time"] <= now_hm:
            triggered = task
            break

    if triggered:
        msg = generate_reminder(triggered["title"], triggered["due_time"])
        state["latest_reminder"] = msg
        mark_task_notified(triggered["id"])
    elif pending:
        nxt = pending[0]
        state["latest_reminder"] = f"Upcoming Task: {nxt['title']} - {nxt['due_time']}"
    else:
        state["latest_reminder"] = "No pending tasks."
