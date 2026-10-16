"""Protocol smoke check for the already-running optional workshop MCP server."""

import asyncio
from uuid import UUID, uuid4

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main() -> None:
    async with streamablehttp_client("http://127.0.0.1:8765/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            names = {tool.name for tool in (await session.list_tools()).tools}
            assert names == {"ping", "add"}, names
            challenge = str(uuid4())
            pong = await session.call_tool("ping", {"challenge": challenge})
            assert not pong.isError, pong
            data = pong.structuredContent
            assert data is not None, pong
            assert data["message"] == "pong", data
            assert data["challenge"] == challenge, data
            UUID(data["server_instance"])
            result = await session.call_tool("add", {"a": 19, "b": 23})
            assert not result.isError, result
            assert result.structuredContent == {"sum": 42}, result
            invalid = await session.call_tool("ping", {"challenge": ""})
            assert invalid.isError, invalid
            assert "challenge must not be blank" in str(invalid.content), invalid
            missing = await session.call_tool("add", {"a": 19})
            assert missing.isError, missing
            print("PASS: initialize, discovery, ping, add, blank challenge, missing argument")
            print(f"server_instance={data['server_instance']}; challenge={challenge}")


if __name__ == "__main__":
    asyncio.run(main())
