import pytest
from httpr import Client, AsyncClient


# Synchronous Client Tests
class TestSyncClient:
    @pytest.fixture
    def client(self):
        return Client(timeout=10.0)  # Use float for timeout

    def test_get_success(self, client):
        response = client.get("http://httpbin.org/get")
        assert isinstance(response, str)
        assert '"url": "http://httpbin.org/get"' in response

    def test_invalid_url(self, client):
        with pytest.raises(Exception):
            client.get("invalid://url")

    def test_timeout(self):
        fast_client = Client(timeout=0.1)  # Use float for timeout
        with pytest.raises(Exception):
            fast_client.get("http://httpbin.org/delay/1")

    def test_redirect_following(self):
        no_redirect_client = Client(follow_redirects=False)
        response = no_redirect_client.get("http://httpbin.org/redirect/1")
        assert "Redirecting..." in response


# Async Client Tests
class TestAsyncClient:
    @pytest.fixture
    def async_client(self):
        return AsyncClient(follow_redirects=True)

    @pytest.mark.asyncio
    async def test_async_get_success(self, async_client):
        response = await async_client.get("http://httpbin.org/get")
        assert isinstance(response, str)
        assert '"url": "http://httpbin.org/get"' in response

    @pytest.mark.asyncio
    async def test_async_timeout_validation(self):
        with pytest.raises(TypeError):
            AsyncClient(timeout="invalid")

    @pytest.mark.asyncio
    async def test_async_timeout_behavior(self):
        fast_client = AsyncClient(timeout=0.1)
        with pytest.raises(Exception):
            await fast_client.get("http://httpbin.org/delay/1")

    @pytest.mark.asyncio
    async def test_async_redirect_handling(self):
        client = AsyncClient(follow_redirects=True)
        response = await client.get("http://httpbin.org/redirect/1")
        assert "http://httpbin.org/get" in response


# Configuration Tests
def test_client_configuration():
    client = Client(
        base_url="http://httpbin.org",
        timeout=5.0,
        follow_redirects=True,
        default_headers={"User-Agent": "test-agent"},
    )

    assert client.base_url == "http://httpbin.org"
    assert client.timeout == 5.0
    assert client.follow_redirects is True
    assert "User-Agent" in client.default_headers
