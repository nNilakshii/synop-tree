"""P0.3.11: the MCP -> Anthropic bridge, driven by a scripted fake model (no API calls)."""

from typing import Any

from anthropic.types.beta import BetaMessage, BetaMessageParam, BetaToolParam
from mcp import Client

from toys.hello_server import mcp
from toys.mcp_agent import mcp_tool_to_anthropic, run_agent


def _message(stop_reason: str, content: list[dict[str, Any]]) -> BetaMessage:
    return BetaMessage.model_validate(
        {
            "id": "msg_fake",
            "type": "message",
            "role": "assistant",
            "model": "fake-model",
            "content": content,
            "stop_reason": stop_reason,
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        }
    )


async def test_mcp_tool_converts_to_anthropic_definition() -> None:
    async with Client(mcp) as client:
        (tool,) = (await client.list_tools()).tools

    converted = mcp_tool_to_anthropic(tool)

    assert converted["name"] == "add"
    assert converted.get("description") == "Add two integers and return the sum."
    assert converted["input_schema"] == tool.input_schema  # JSON Schema passes through as-is
    assert set(tool.input_schema["required"]) == {"a", "b"}


async def test_agent_loop_routes_tool_call_through_mcp() -> None:
    seen: list[list[BetaMessageParam]] = []

    async def fake_ask(messages: list[BetaMessageParam], tools: list[BetaToolParam]) -> BetaMessage:
        seen.append(list(messages))
        assert [t["name"] for t in tools] == ["add"]
        if len(seen) == 1:
            use = {"type": "tool_use", "id": "tu_1", "name": "add", "input": {"a": 17, "b": 25}}
            return _message("tool_use", [use])
        return _message("end_turn", [{"type": "text", "text": "17 + 25 = 42."}])

    async with Client(mcp) as client:
        answer, calls = await run_agent("what is 17+25?", client, fake_ask)

    assert answer == "17 + 25 = 42."
    assert calls == 1
    tool_result_turn = seen[1][-1]
    assert tool_result_turn["role"] == "user"
    (result,) = tool_result_turn["content"]
    assert isinstance(result, dict)
    assert result["type"] == "tool_result"
    assert result.get("content") == "42"
    assert result.get("is_error") is False
