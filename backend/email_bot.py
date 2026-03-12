"""Email monitoring bot.

Default behavior uses backend/sample_emails.txt lines as unread emails.
You can replace load_unread_emails() with an IMAP implementation later.
"""

from __future__ import annotations

from pathlib import Path

from backend.database import update_bot_status
from backend.groq_ai import summarize_email

SAMPLE_EMAILS_FILE = Path(__file__).resolve().parent / "sample_emails.txt"


def load_unread_emails() -> list[str]:
    """Read local sample emails as a stand-in for unread mailbox items."""
    if not SAMPLE_EMAILS_FILE.exists():
        SAMPLE_EMAILS_FILE.write_text(
            "Meeting tomorrow at 10 AM in conference room B.\n"
            "Submit report by 5 PM today.\n",
            encoding="utf-8",
        )
    emails = [line.strip() for line in SAMPLE_EMAILS_FILE.read_text(encoding="utf-8").splitlines()]
    return [email for email in emails if email]


def run_email_bot(state: dict) -> None:
    """Poll unread emails, summarize latest, and update shared state."""
    update_bot_status("Email Bot", "Running")
    emails = load_unread_emails()
    if not emails:
        state["latest_email_summary"] = "No unread emails found."
        return

    latest_email = emails[-1]
    state["latest_email_summary"] = summarize_email(latest_email)
