from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.deps import get_assistant
from app.llm import ask, ask_stream
from app.conversations import get_conversation
from app.schemas import ChatRequest, ChatResponse
from app.models import is_deterministic

router = APIRouter(prefix="/assistants", tags=["chat"])


@router.post("/{assistant_id}/chat/stream")
async def chat_stream(assistant_id: str, message: str):
    """Stream the assistant's answer to the client as it is generated."""
    cfg = get_assistant(assistant_id)  # raises 404 if unknown
    return StreamingResponse(ask_stream(cfg, message), media_type="text/plain")


@router.post("/{assistant_id}/sessions/{session_id}/chat",
             response_model=ChatResponse)
async def chat_in_session(assistant_id: str, session_id: str,
                          body: ChatRequest) -> ChatResponse:
    """A turn within a remembered conversation."""
    cfg = get_assistant(assistant_id)
    convo = get_conversation(session_id)
    convo.add("user", body.message)
    answer = await ask(cfg, body.message)
    convo.add("assistant", answer)
    return ChatResponse(assistant_id=assistant_id, answer=answer,
                        deterministic=is_deterministic(cfg))
