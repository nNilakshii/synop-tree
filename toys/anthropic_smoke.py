"""Anthropic API smoke test (P0.3.10): one tool_use round trip, printing token usage.

    uv run python toys/anthropic_smoke.py

Model comes from config.yaml (models.eval_agent_main); the key from ANTHROPIC_API_KEY / .env.
Costs a fraction of a cent. Not a pytest: tests never call real LLM APIs.
"""

import asyncio

import anthropic
from anthropic.types.beta import (
    BetaMessage,
    BetaMessageParam,
    BetaToolParam,
    BetaToolResultBlockParam,
    BetaUsage,
)
from pydantic import BaseModel

from synop_tree.config import load_config

ADD_TOOL: BetaToolParam = {
    "name": "add",
    "description": "Add two integers and return the sum.",
    "input_schema": {
        "type": "object",
        "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
        "required": ["a", "b"],
        "additionalProperties": False,
    },
    "strict": True,
}


class AddArgs(BaseModel):
    a: int
    b: int


def show_usage(label: str, usage: BetaUsage) -> None:
    print(
        f"[{label}] input={usage.input_tokens} output={usage.output_tokens} "
        f"cache_read={usage.cache_read_input_tokens} "
        f"cache_write={usage.cache_creation_input_tokens}"
    )


async def main() -> None:
    config = load_config()
    key = config.secrets.anthropic_api_key
    client = anthropic.AsyncAnthropic(api_key=key.get_secret_value() if key else None)
    model = config.models.eval_agent_main

    async def ask(messages: list[BetaMessageParam]) -> BetaMessage:
        return await client.beta.messages.create(
            model=model,
            max_tokens=2000,
            tools=[ADD_TOOL],
            messages=messages,
            # On a safety decline the API re-runs the request on a fallback model.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )

    messages: list[BetaMessageParam] = [
        {"role": "user", "content": "Use the add tool to compute 17 + 25, then state the result."}
    ]
    first = await ask(messages)
    show_usage("turn 1", first.usage)
    calls = [b for b in first.content if b.type == "tool_use"]
    if first.stop_reason != "tool_use" or not calls:
        raise SystemExit(f"expected a tool_use, got stop_reason={first.stop_reason}")

    call = calls[0]
    args = AddArgs.model_validate(call.input)
    result = args.a + args.b
    print(f"model called {call.name}({call.input}) -> {result}")
    tool_result: BetaToolResultBlockParam = {
        "type": "tool_result",
        "tool_use_id": call.id,
        "content": str(result),
    }
    messages.append({"role": "assistant", "content": first.content})
    messages.append({"role": "user", "content": [tool_result]})

    second = await ask(messages)
    show_usage("turn 2", second.usage)
    text = "".join(b.text for b in second.content if b.type == "text")
    print(f"model ({second.model}, stop={second.stop_reason}): {text.strip()}")


if __name__ == "__main__":
    asyncio.run(main())
