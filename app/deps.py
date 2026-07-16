from fastapi import Depends, HTTPException

from app.models import AssistantConfig
from app.store import ASSISTANTS


def get_assistant(assistant_id: str) -> AssistantConfig:
    """A dependency: resolve an assistant or fail with 404."""
    cfg = ASSISTANTS.get(assistant_id)
    if cfg is None:
        raise HTTPException(status_code=404, detail="assistant not found")
    return cfg


# Type alias so endpoints read cleanly: assistant: AssistantDep
AssistantDep = Depends(get_assistant)
