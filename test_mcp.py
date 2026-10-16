"""Small, real MCP server for MCP_FUNDAMENTALS.md; run directly, not with pytest."""

from uuid import uuid4

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Workshop MCP",
    host="127.0.0.1",
    port=8765,
    stateless_http=True,
    json_response=True,
)
# Changes on each server start; lets participants distinguish live runs.
SERVER_INSTANCE = str(uuid4())


@mcp.tool()
def ping(challenge: str) -> dict[str, str]:
    """Echo a nonblank challenge and identify this running workshop server."""
    if not challenge.strip():
        raise ValueError("challenge must not be blank")
    return {
        "message": "pong",
        "challenge": challenge,
        "server_instance": SERVER_INSTANCE,
    }


@mcp.tool()
def add(a: int, b: int) -> dict[str, int]:
    """Add two integers and return their sum."""
    return {"sum": a + b}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
