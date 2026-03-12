"""SQLite helpers for reminders and bot state."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[1] / "tasks.db"


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection with row support."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """Create all tables used by the app."""
    with closing(get_connection()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_time TEXT NOT NULL,
                notified INTEGER NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bot_status (
                bot_name TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def add_task(title: str, due_time: str) -> None:
    """Add a reminder task with HH:MM 24h time."""
    with closing(get_connection()) as conn:
        conn.execute(
            "INSERT INTO tasks (title, due_time) VALUES (?, ?)",
            (title.strip(), due_time.strip()),
        )
        conn.commit()


def get_pending_tasks() -> list[dict[str, Any]]:
    """Return tasks not yet notified."""
    with closing(get_connection()) as conn:
        rows = conn.execute(
            "SELECT id, title, due_time FROM tasks WHERE notified = 0 ORDER BY due_time"
        ).fetchall()
    return [dict(r) for r in rows]


def mark_task_notified(task_id: int) -> None:
    """Set a task as notified to avoid duplicate alerts."""
    with closing(get_connection()) as conn:
        conn.execute("UPDATE tasks SET notified = 1 WHERE id = ?", (task_id,))
        conn.commit()


def update_bot_status(bot_name: str, status: str) -> None:
    """Store heartbeat status for each bot."""
    with closing(get_connection()) as conn:
        conn.execute(
            """
            INSERT INTO bot_status (bot_name, status, last_updated)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(bot_name)
            DO UPDATE SET status=excluded.status, last_updated=CURRENT_TIMESTAMP
            """,
            (bot_name, status),
        )
        conn.commit()


def get_bot_statuses() -> list[dict[str, Any]]:
    """Load all bot statuses for the dashboard."""
    with closing(get_connection()) as conn:
        rows = conn.execute(
            "SELECT bot_name, status, last_updated FROM bot_status ORDER BY bot_name"
        ).fetchall()
    return [dict(r) for r in rows]
