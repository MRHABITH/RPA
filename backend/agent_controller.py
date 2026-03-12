"""Central AI agent controller that schedules both RPA bots."""

from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from backend.email_bot import run_email_bot
from backend.reminder_bot import run_reminder_bot


class AgentController:
    """Coordinates bot execution and shared dashboard state."""

    def __init__(self) -> None:
        self.state: dict[str, str] = {
            "latest_email_summary": "Waiting for email scan...",
            "latest_reminder": "Waiting for reminder scan...",
        }
        self.scheduler = BackgroundScheduler(daemon=True)
        self._started = False

    def start(self) -> None:
        """Start recurring jobs once."""
        if self._started:
            return
        self.scheduler.add_job(lambda: run_email_bot(self.state), "interval", seconds=8, id="email_bot")
        self.scheduler.add_job(
            lambda: run_reminder_bot(self.state), "interval", seconds=5, id="reminder_bot"
        )
        self.scheduler.start()
        self._started = True

    def stop(self) -> None:
        """Stop scheduler safely."""
        if self._started:
            self.scheduler.shutdown(wait=False)
            self._started = False
