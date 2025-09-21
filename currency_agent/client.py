import asyncio
from uuid import uuid4
import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    SendMessageRequest,
    MessageSendParams,
    GetTaskRequest,
    TaskQueryParams,
)


AGENT_URL = "http://localhost:10000"


def create_send_message_payload(text: str):
    return {
        "message": {
            "role": "user",
            "parts": [{"kind": "text", "text": text}],
            "messageId": uuid4().hex,
        }
    }


async def run(client: A2AClient, text: str):
    send_message_payload = create_send_message_payload(text)
    request = SendMessageRequest(
        id=str(uuid4()), params=MessageSendParams(**send_message_payload)
    )
    message_response = await client.send_message(request)

    task_id = message_response.root.result.id
    get_request = GetTaskRequest(id=str(uuid4()), params=TaskQueryParams(id=task_id))
    task_response = await client.get_task(get_request)
    print(task_response.root.result.artifacts[0].parts[0].root.text)


async def main(text: str):
    print(f"--- 🔄 Connecting to agent at {AGENT_URL}... ---")
    try:
        async with httpx.AsyncClient() as httpx_client:
            resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=AGENT_URL,
            )

            agent_card = await resolver.get_agent_card()

            client = A2AClient(
                httpx_client=httpx_client,
                agent_card=agent_card,
            )

            print("--- ✅ Connection successful. ---")

            await run(client, text)
    except Exception as e:
        print(f"--- ❌ An error occurred: {e} ---")
        print("Ensure the agent server is running.")


if __name__ == "__main__":
    asyncio.run(main("how much is 45000 INR in MYR?"))
