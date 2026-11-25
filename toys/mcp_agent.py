"""Minimal MCP -> Claude agent loop (P0.3.11). Seed of the eval bridge (P5.3.5).

    uv run python toys/mcp_agent.py "what is 17+25?"

Spawns toys/hello_server.py over stdio, converts its MCP tools into Anthropic tool
definitions, and lets Claude call them through MCP until it answers.
Model from config.yaml (models.eval_agent_main); key from ANTHROPIC_API_KEY / .env.
"""

import asyncio
import sys
from collections.abc import Awaitable, Callable
from pathlib import Path

import anthropic
from anthropic.types.beta import (
    BetaMessage,
    BetaMessageParam,
    BetaToolParam,
    BetaToolResultBlockParam,
)
from mcp import Client, StdioServerParameters
from mcp.types import TextContent, Tool

from synop_tree.config import load_config

SERVER = Path(__file__).with_name("hello_server.py")
MAX_TURNS = 6

AskFn = Callable[[list[BetaMessageParam], list[BetaToolParam]], Awaitable[BetaMessage]]


def mcp_tool_to_anthropic(tool: Tool) -> BetaToolParam:
    """MCP tool definition -> Anthropic tool definition (both use JSON Schema for inputs)."""
    return {
        "name": tool.name,
        "description": tool.description or "",
        "input_schema": tool.input_schema,
    }


async def run_agent(question: str, mcp_client: Client, ask: AskFn) -> tuple[str, int]:
    """Loop until the model stops calling tools. Returns (answer, tool calls made)."""
    tools = [mcp_tool_to_anthropic(t) for t in (await mcp_client.list_tools()).tools]
    messages: list[BetaMessageParam] = [{"role": "user", "content": question}]
    calls_made = 0

    for _ in range(MAX_TURNS):
        response = await ask(messages, tools)
        messages.append({"role": "assistant", "content": response.content})
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        if response.stop_reason != "tool_use" or not tool_uses:
            return "".join(b.text for b in response.content if b.type == "text").strip(), calls_made

        results: list[BetaToolResultBlockParam] = []
        for use in tool_uses:  # all results go back in ONE user message
            result = await mcp_client.call_tool(use.name, dict(use.input))
            text = "\n".join(c.text for c in result.content if isinstance(c, TextContent))
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": use.id,
                    "content": text,
                    "is_error": result.is_error,
                }
            )
            calls_made += 1
        messages.append({"role": "user", "content": results})

    raise RuntimeError(f"no answer after {MAX_TURNS} turns")


async def main(question: str) -> None:
    config = load_config()
    key = config.secrets.anthropic_api_key
    claude = anthropic.AsyncAnthropic(api_key=key.get_secret_value() if key else None)

    async def ask(messages: list[BetaMessageParam], tools: list[BetaToolParam]) -> BetaMessage:
        return await claude.beta.messages.create(
            model=config.models.eval_agent_main,
            max_tokens=4000,
            system="Use the provided tools for arithmetic. Answer in one short sentence.",
            tools=tools,
            messages=messages,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )

    server = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with Client(server) as mcp_client:
        answer, calls = await run_agent(question, mcp_client, ask)
    print(f"{answer}   [MCP tool calls: {calls}]")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "What is 17+25?"))
