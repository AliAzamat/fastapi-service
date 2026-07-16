from fastapi import APIRouter, HTTPException, Query, status

from app.models import AssistantConfig, AssistantKind
from app.store import ASSISTANTS
from app.schemas import AssistantOut, CreateAssistant

router = APIRouter(prefix="/assistants", tags=["assistants"])


@router.get("", response_model=list[AssistantOut])
async def list_assistants(
    kind: AssistantKind | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[AssistantConfig]:
    """List assistants, optionally filtered by kind, with pagination."""
    items = list(ASSISTANTS.values())
    if kind is not None:
        items = [a for a in items if a.kind == kind]
    return items[offset:offset + limit]


@router.post("", response_model=AssistantOut, status_code=status.HTTP_201_CREATED)
async def create_assistant(body: CreateAssistant) -> AssistantConfig:
    """Register a new assistant; 409 if the id is already taken."""
    if body.id in ASSISTANTS:
        raise HTTPException(status_code=409, detail="assistant id already exists")
    cfg = AssistantConfig(
        id=body.id, name=body.name, kind=body.kind,
        system_prompt=body.system_prompt,
    )
    ASSISTANTS[cfg.id] = cfg
    return cfg
