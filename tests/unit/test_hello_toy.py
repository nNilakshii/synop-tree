"""P0.3.7: exercise the toy server fully in memory (no transport)."""

from mcp import Client
from mcp.types import TextContent, TextResourceContents

from toys.hello_server import mcp


async def test_add_tool_returns_sum() -> None:
    async with Client(mcp, raise_exceptions=True) as client:
        result = await client.call_tool("add", {"a": 17, "b": 25})

    assert not result.is_error
    assert result.structured_content == {"result": 42}
    assert result.content == [TextContent(type="text", text="42")]


async def test_add_rejects_bad_arguments() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": "seventeen", "b": 25})

    assert result.is_error


async def test_lists_tool_template_and_prompt() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        templates = await client.list_resource_templates()
        prompts = await client.list_prompts()

    assert [t.name for t in tools.tools] == ["add"]
    assert [t.uri_template for t in templates.resource_templates] == ["hello://greeting/{name}"]
    assert [p.name for p in prompts.prompts] == ["greet_user"]


async def test_greeting_resource() -> None:
    async with Client(mcp) as client:
        result = await client.read_resource("hello://greeting/Nilakshi")

    (content,) = result.contents
    assert isinstance(content, TextResourceContents)
    assert content.text == "Hello, Nilakshi!"


async def test_greet_user_prompt() -> None:
    async with Client(mcp) as client:
        result = await client.get_prompt("greet_user", {"name": "Ada"})

    (message,) = result.messages
    assert message.role == "user"
    assert isinstance(message.content, TextContent)
    assert "Ada" in message.content.text
    assert "friendly" in message.content.text
