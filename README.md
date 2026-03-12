# AI Agent Based Robotic Process Automation for Daily Tasks

Beginner-friendly project that demonstrates an AI Agent workflow automating:
1. Email Monitoring Bot
2. Task Reminder Bot

## Project Structure

```
ai-rpa-agent/
├── backend/
│   ├── agent_controller.py
│   ├── email_bot.py
│   ├── reminder_bot.py
│   ├── groq_ai.py
│   └── database.py
├── frontend/
│   └── dashboard.py
├── tasks.db
├── requirements.txt
└── main.py
```

## How It Works

- Streamlit dashboard starts the `AgentController`.
- Controller schedules:
  - Email bot every 8 seconds.
  - Reminder bot every 5 seconds.
- Email bot reads local sample unread emails and summarizes latest text with Groq (`llama-3.3-70b-versatile`).
- Reminder bot checks SQLite tasks and creates reminder messages when due.
- Bot outputs and status are shown in real time on dashboard.

## Setup

1. **Create and activate a virtual environment**
   - Windows: `python -m venv .venv && .venv\\Scripts\\activate`
   - Linux/Mac: `python -m venv .venv && source .venv/bin/activate`

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Configure Groq key**
   ```bash
   export GROQ_API_KEY="your_key_here"
   ```
   Without a key, app uses fallback text generation.

4. **Run app**
   ```bash
   streamlit run main.py
   ```

## Step-by-step Demo Flow

1. Open dashboard.
2. AI Agent controller starts both bots.
3. Email bot reads sample unread email line and creates summary.
4. Add tasks from sidebar with time.
5. Reminder bot monitors due times and shows reminder when time is reached.

## Notes

- For a real inbox, replace `load_unread_emails()` in `backend/email_bot.py` with IMAP integration.
- SQLite file `tasks.db` is created automatically.
