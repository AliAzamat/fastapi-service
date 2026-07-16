# AI Service with FastAPI

A project that puts a real HTTP API in front of the assistant modeled in Python. Utilizes FastAPI's app and routing, Pydantic request/response validation, async endpoints that call the model, dependency injection, list/CRUD routes, exception handlers and middleware, streaming responses, and tests with the TestClient — the exact server shape the evaluation platform is built on. The anchor: an `/assistants/{id}/chat` endpoint that takes a question and returns a validated answer.

## Stack
- Python
- FastAPI
- Pydantic
- asyncio
- Uvicorn
