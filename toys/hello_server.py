"""Toy MCP server (P0.3.3): one tool, one resource template, one prompt.

stdio (default):   uv run python toys/hello_server.py
Streamable HTTP:   uv run python toys/hello_server.py --http   -> http://127.0.0.1:8000/mcp

Never print() here: on stdio, stdout is the JSON-RPC channel. Log to stderr.
"""

import logging
import sys

from mcp.server import MCPServer

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("hello")

mcp = MCPServer("hello")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    log.info("add(%s, %s)", a, b)
    return a + b


@mcp.resource("hello://greeting/{name}")
def greeting(name: str) -> str:
    """A friendly greeting for `name`."""
    return f"Hello, {name}!"


@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Ask the model to write a short greeting."""
    return f"Write a {style} one-line greeting for someone named {name}."


if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
    else:
        mcp.run()
