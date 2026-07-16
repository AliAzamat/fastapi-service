from pydantic import BaseModel, Field

from app.models import AssistantKind


class ChatRequest(BaseModel):
    """The JSON body a client POSTs to ask the assistant a question."""
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    """The JSON we promise to return — the contract clients code against."""
    assistant_id: str
    answer: str
    deterministic: bool


class AssistantOut(BaseModel):
    """The public view of a configured assistant."""
    id: str
    name: str
    kind: AssistantKind


class CreateAssistant(BaseModel):
    """The body to register a new assistant."""
    id: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1)
    kind: AssistantKind
    system_prompt: str = Field(min_length=1)
