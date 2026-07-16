from dataclasses import dataclass, field


@dataclass
class Conversation:
    """The running message history for one session."""
    session_id: str
    messages: list[dict] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        # Keep only the last 20 turns so context (and cost) stay bounded.
        self.messages = self.messages[-20:]


# In-memory store; the agent project moves this to Redis for durability.
CONVERSATIONS: dict[str, Conversation] = {}


def get_conversation(session_id: str) -> Conversation:
    """Fetch-or-create the conversation for a session."""
    if session_id not in CONVERSATIONS:
        CONVERSATIONS[session_id] = Conversation(session_id=session_id)
    return CONVERSATIONS[session_id]
