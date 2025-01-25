import unittest
import asyncio
from httpr import Client, AsyncClient


class TestHttpRequests(unittest.TestCase):
    def setUp(self):
        self.sync_client = Client()
        self.async_client = AsyncClient()

    def test_synchronous_request(self):
        response = self.sync_client.get("https://example.com")
        self.assertIsNotNone(response)

    async def async_get(self):
        response = await self.async_client.get("https://example.com")
        return response

    def test_asynchronous_request(self):
        response = asyncio.run(self.async_get())
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()
