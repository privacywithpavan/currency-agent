import asyncio
from fastmcp import Client


async def test_server():
    async with Client("http://localhost:8080/mcp") as client:
        tools = await client.list_tools()
        for tool in tools:
            print(f"--- 🛠️  Tool found: {tool.name} ---")
        print("--- 🪛  Calling get_exchange_rate tool for MYR to INR ---")
        result = await client.call_tool(
            "get_exchange_rate", {"currency_from": "MYR", "currency_to": "INR"}
        )
        print(f"--- ✅  Success: {result.content[0].text} ---")


if __name__ == "__main__":
    asyncio.run(test_server())
