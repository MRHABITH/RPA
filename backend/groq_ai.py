"""Wrapper for Groq LLM with safe fallback for local demos."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "llama-3.3-70b-versatile"


def _offline_summary(text: str, prefix: str) -> str:
    compact = " ".join(text.split())
    if not compact:
        return f"{prefix}: No content available."
    return f"{prefix}: {compact[:140]}"


def summarize_email(email_text: str) -> str:
    """Generate a concise email summary using Groq or fallback text."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return _offline_summary(email_text, "[Fallback summary]")

    try:
        from groq import Groq  # lazy import so app still runs without package usage

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You summarize emails in one clear sentence.",
                },
                {"role": "user", "content": email_text},
            ],
            temperature=0.2,
            max_tokens=80,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return _offline_summary(email_text, "[Groq error fallback]")


def generate_reminder(task_title: str, due_time: str) -> str:
    """Create reminder sentence via Groq model."""
    prompt = f"Task: {task_title}\nTime: {due_time}\nCreate a short reminder."
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return f"Reminder: {task_title} now (scheduled at {due_time})."

    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a task reminder assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=60,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return f"Reminder: {task_title} now (scheduled at {due_time})."
