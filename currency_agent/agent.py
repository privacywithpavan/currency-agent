import logging
from dotenv import load_dotenv, find_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import uvicorn

_ = load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

SYSTEM_INSTRUCTION = """
You are a specialized assistant for currency conversions.
Your sole purpose is to use the 'get_exchange_rate' tool to answer questions about currency exchange rates.
If the user asks about anything other than currency conversion or exchange rates, politely state that you cannot help with that topic and can only assist with currency-related queries.
Do not attempt to answer unrelated questions or use tools for other purposes.
"""

logger.info("--- 🔧 Loading MCP tools from MCP Server... ---")
logger.info("--- 🤖 Creating ADK Currency Agent... ---")

root_agent = LlmAgent(
    name="currency_agent",
    description="An agent that provides currency exchange rates and conversion.",
    instruction=SYSTEM_INSTRUCTION,
    model="gemini-2.5-flash",
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://localhost:8080/mcp"
            )
        )
    ],
)

a2a_app = to_a2a(root_agent, port=10000)


if __name__ == "__main__":
    logger.info("🚀 Agent server started on port 10000")
    uvicorn.run(a2a_app, host="0.0.0.0", port=10000)
