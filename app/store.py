from app.models import AssistantConfig, AssistantKind

# Extracted from main.py so dependencies and routes can share it.
ASSISTANTS: dict[str, AssistantConfig] = {
    "support": AssistantConfig(
        id="support",
        name="Support Bot",
        kind=AssistantKind.SUPPORT,
        system_prompt="You are a concise, friendly product support agent.",
    ),
}
