# Mood GenAI — AI Mood Booster

A small full-stack web app that turns how you feel into personalized quotes, poetry, and emotional companionship. You describe your mood and preferred language; **Groq** (Llama 3.1) generates structured responses served through a **FastAPI** backend and a glassmorphism-style frontend.

## Features

- **Mood-based generation** — Enter a feeling (e.g. nostalgic, inspired) and a language (Urdu, English, Hindi, etc.).
- **Structured AI output** — Responses include detected mood, content (quote/poetry), and author or poet attribution.
- **Conversation memory** — Follow-up questions reuse server-side chat history so the model can explain or refine earlier poems.
- **Content guardrails** — System prompt filters inappropriate Roman Urdu/Hinglish slang and returns a polite refusal instead of poetry when needed.
- **Premium UI** — Responsive single-page interface with loading states, result cards, and a scrollable chat log.

## Tech stack

| Layer      | Technology                          |
| ---------- | ----------------------------------- |
| Backend    | Python, FastAPI, Uvicorn, Pydantic  |
| AI         | Groq API (`llama-3.1-8b-instant`)   |
| Frontend   | HTML, CSS, vanilla JavaScript       |
| Config     | `python-dotenv`                     |

## Project structure

```
Mood_Genai/
├── main.py           # FastAPI app and routes
├── ai_logic.py       # Groq client, prompts, chat memory
├── schemas.py        # Request/response models
├── static/
│   ├── index.html    # Web UI
│   └── style.css     # Styling
├── .env              # API keys (not committed — create locally)
└── .venv/            # Python virtual environment (optional)
```

## Prerequisites

- **Python 3.10+**
- A [Groq](https://console.groq.com/) API key

## Setup

1. **Clone or download** this repository and open a terminal in the project folder.

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   ```

   Windows (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   macOS / Linux:

   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install fastapi uvicorn groq python-dotenv pydantic
   ```

4. **Configure environment variables** — Create a `.env` file in the project root:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

   Never commit `.env` or share your API key publicly.

## Run the app

```bash
python main.py
```

Or with Uvicorn directly:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API

### `POST /generate-quote`

Generates mood-based content from the AI.

**Request body**

```json
{
  "mood": "feeling nostalgic about home",
  "language": "Urdu"
}
```

**Response**

```json
{
  "mood_detected": "Nostalgic",
  "content": "Generated quote or poetry text...",
  "author_or_poet": "Optional attribution"
}
```

### `GET /`

Serves the web UI (`static/index.html`).

## How it works

1. The browser sends mood and language to `/generate-quote`.
2. `ai_logic.py` appends the message to an in-memory `CHAT_MEMORY` list and calls Groq with a JSON response format.
3. The model returns structured JSON matching `MoodResponse`; the UI displays the content and logs the exchange.
4. Follow-up questions hit the same endpoint; prior turns stay in memory for contextual replies.

> **Note:** Chat memory lives in process memory and resets when the server restarts. It is not shared across multiple server workers.

## License

No license file is included. Add one if you plan to open-source or distribute this project.
