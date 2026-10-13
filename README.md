# AI Assistant Service (FastAPI)

**A FastAPI service for configurable AI assistants: Pydantic request/response contracts, paginated list and create routes with conflict handling, a dependency that resolves assistants or returns 404, session-scoped chat with bounded history, token streaming, a domain-error handler, request-timing middleware, and TestClient tests.**

This is the HTTP layer on top of the typed assistant model from [python-ai-backends](https://github.com/AliAzamat/python-ai-backends): the same `AssistantConfig` objects, now served, validated at the edge, and tested.

## API

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness |
| `GET` | `/assistants?kind=&limit=&offset=` | List assistants, optionally filtered by kind; `limit` 1–100 (default 20) |
| `POST` | `/assistants` | Create `{id, name, kind, system_prompt}` → `201`; `409` if the ID exists |
| `POST` | `/assistants/{id}/sessions/{session_id}/chat` | `{"message": "..."}` (1–4000 chars) → `{assistant_id, answer, deterministic}` |
| `POST` | `/assistants/{id}/chat/stream?message=` | Streams the reply as `text/plain` chunks |

## Design notes

- **Contracts at the edge.** Separate Pydantic schemas for input (`CreateAssistant`, `ChatRequest`) and output (`AssistantOut`, `ChatResponse`) keep internal fields such as the system prompt out of responses.
- **Dependencies for lookups.** `get_assistant` resolves an assistant or raises a 404, so routes don't repeat that logic.
- **Bounded conversations.** Session history keeps the last 20 messages so context size and cost stay capped.
- **Streaming.** The streaming route relays OpenAI's token stream through a `StreamingResponse` as it's generated.
- **One error path.** Domain exceptions (`AssistantError` with `NotFound` / `Conflict` subclasses) map to JSON responses in a single exception handler.
- **Request timing.** Middleware logs path, status, and latency for every request.

## Running

Requires Python 3.10+.

```bash
git clone https://github.com/AliAzamat/fastapi-service.git
cd fastapi-service
pip install fastapi uvicorn openai pytest httpx
```

**This repo needs `app/models.py`, which isn't committed.** It's the `AssistantConfig` / `AssistantKind` / `is_deterministic` module from python-ai-backends; copying it in makes the project work:

```bash
curl -o app/models.py https://raw.githubusercontent.com/AliAzamat/python-ai-backends/main/app/models.py

OPENAI_API_KEY=dummy python -m pytest -q    # 4 tests pass with models.py in place
export OPENAI_API_KEY=<your key>
uvicorn app.main:app --reload
```

## Limitations

- **The chat routes aren't mounted.** `app/main.py` includes only the assistants router, so both chat endpoints return 404 until `app.include_router(chat.router)` is added.
- Assistants and conversations are in-memory dictionaries, and stored conversation history isn't yet sent back to the model — each turn is answered on its own.
- `deps.AssistantDep` is defined but routes call `get_assistant()` directly rather than injecting it; no dependency file is included.
