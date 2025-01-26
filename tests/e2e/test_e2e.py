import pytest
from httpr import Client, AsyncClient
import httpbin

# Synchronous Client Tests
class TestSyncClient:
    @pytest.fixture
    def client(self):
        return Client(timeout=10)

    def test_get_success(self, client):
        response = client.get(httpbin.url("/get"))
        assert isinstance(response, str)
        assert '"url": "http://httpbin.org/get"' in response

    def test_invalid_url(self, client):
        with pytest.raises(Exception):
            client.get("invalid://url")

    def test_timeout(self):
        fast_client = Client(timeout=0.1)
        with pytest.raises(Exception):
            fast_client.get(httpbin.url("/delay/1"))

    def test_redirect_following(self):
        no_redirect_client = Client(follow_redirects=False)
        response = no_redirect_client.get(httpbin.url("/redirect/1"))
        assert "Redirecting..." in response

# Async Client Tests  
class TestAsyncClient:
    @pytest.fixture
    async def async_client(self):
        return AsyncClient()

    @pytest.mark.asyncio
    async def test_async_get_success(self, async_client):
        response = await async_client.get(httpbin.url("/get"))
        assert '"url": "http://httpbin.org/get"' in response

    @pytest.mark.asyncio 
    async def test_async_timeout(self):
        fast_client = AsyncClient()
        with pytest.raises(Exception):
            await fast_client.get(httpbin.url("/delay/1"))

    @pytest.mark.asyncio
    async def test_async_redirect_handling(self):
        client = AsyncClient(follow_redirects=True)
        response = await client.get(httpbin.url("/redirect/1"))
        assert "http://httpbin.org/get" in response

# Configuration Tests
def test_client_configuration():
    client = Client(
        base_url="http://httpbin.org",
        timeout=5,
        follow_redirects=True,
        default_headers={"User-Agent": "test-agent"}
    )
    
    assert client.base_url == "http://httpbin.org"
    assert client.timeout == 5
    assert client.follow_redirects is True
    assert "User-Agent" in client.default_headers
