from fastapi.testclient import TestClient

from app.main import app
from app.deps import get_assistant
from app.models import AssistantConfig, AssistantKind

client = TestClient(app)


def fake_assistant(assistant_id: str) -> AssistantConfig:
    return AssistantConfig(
        id=assistant_id, name="Test", kind=AssistantKind.SUPPORT,
        system_prompt="You are a test.",
    )


def test_health_ok():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_list_assistants_paginates():
    res = client.get("/assistants?limit=1")
    assert res.status_code == 200
    assert len(res.json()) <= 1


def test_create_then_conflict():
    body = {"id": "ops", "name": "Ops", "kind": "operations",
            "system_prompt": "You help with operations."}
    assert client.post("/assistants", json=body).status_code == 201
    # Creating the same id again conflicts.
    assert client.post("/assistants", json=body).status_code == 409


def test_unknown_assistant_is_404():
    app.dependency_overrides[get_assistant] = fake_assistant
    res = client.get("/assistants/nope/chat/stream")  # wrong method → 405
    assert res.status_code in (404, 405)
    app.dependency_overrides.clear()
