"""Toy MCP client (P0.3.9): connect, list tools, call `add`, print the result.

stdio (spawns the server):  uv run python toys/hello_client.py 17 25
Streamable HTTP:            uv run python toys/hello_client.py 17 25 --url http://127.0.0.1:8000/mcp
"""

import argparse
import asyncio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters
from mcp.types import TextContent

SERVER = Path(__file__).with_name("hello_server.py")


async def main(a: int, b: int, url: str | None) -> int:
    target = url or StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with Client(target) as client:
        tools = await client.list_tools()
        print("tools:", ", ".join(t.name for t in tools.tools))

        result = await client.call_tool("add", {"a": a, "b": b})
        if result.is_error:
            print("error:", result.content, file=sys.stderr)
            return 1
        text = next(c.text for c in result.content if isinstance(c, TextContent))
        print(f"add({a}, {b}) = {text}   structured={result.structured_content}")
        print("protocol:", client.protocol_version)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("a", type=int)
    parser.add_argument("b", type=int)
    parser.add_argument("--url", help="Streamable HTTP endpoint instead of spawning stdio")
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args.a, args.b, args.url)))
