# Synchronous
import asyncio
from httpr import Client

# Asynchronous
from httpr import AsyncClient

client = Client()
response = client.get("https://example.com")
print("Sync:", response)


async def fetch():
    client = AsyncClient()
    response = await client.get("https://example.com")
    return response


response = asyncio.run(fetch())
print("Async:", response)
