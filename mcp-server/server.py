import asyncio
import httpx
import logging
from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Currency MCP Server 💵")


@mcp.tool()
def get_exchange_rate(currency_from: str, currency_to: str) -> dict:
    """Use this tool to get the exchange rate between two currencies.
    Args:
        currency_from (str): The currency to convert from (e.g., "USD").
        currency_to (str): The currency to convert to (e.g., "EUR").
    Returns:
        A dictionary containing the exchange rate data, or an error message if the request fails.
    """
    logger.info(
        f"--- 🛠️ Tool: get_exchange_rate called for converting {currency_from} to {currency_to} ---"
    )
    try:
        response = httpx.get(
            f"https://api.frankfurter.app/latest",
            params={"from": currency_from, "to": currency_to},
        )
        response.raise_for_status()

        data = response.json()
        if "rates" not in data:
            return {"error": "Invalid response from exchange rate API"}
        logger.info(f"✅ API response: {data}")
        return data
    except Exception as e:
        logger.error(f"Error fetching exchange rate: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    logger.info("🚀 MCP server started on port 8080")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port="8080",
        )
    )
