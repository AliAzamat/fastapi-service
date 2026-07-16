from openai import AsyncOpenAI
from app.models import AssistantConfig

client = AsyncOpenAI()


async def ask(cfg: AssistantConfig, user_message: str) -> str:
    """Send one turn to the model and return its full text reply."""
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=cfg.temperature,
        messages=[
            {"role": "system", "content": cfg.system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content or ""


async def ask_stream(cfg: AssistantConfig, user_message: str):
    """Yield the reply in chunks as the model generates it."""
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=cfg.temperature,
        stream=True,  # ask the API to push tokens as they're produced
        messages=[
            {"role": "system", "content": cfg.system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
