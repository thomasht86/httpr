import pytest
import json
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

    def test_params_in_url(self, client):
        params = {'key1': 'value1', 'key2': 'value2'}
        response = client.get("http://httpbin.org/get", params=params)
        response_data = json.loads(response)
        assert response_data["args"] == params

    def test_custom_headers(self, client):
        headers = {"User-Agent": "test-agent/1.0"}
        response = client.get("http://httpbin.org/headers", headers=headers)
        response_data = json.loads(response)
        assert headers["User-Agent"] in response_data["headers"]["User-Agent"]

    def test_post_form_data(self, client):
        data = {'key': 'value'}
        response = client.post("http://httpbin.org/post", data=data)
        response_data = json.loads(response)
        assert response_data["form"] == data

    def test_post_json_data(self, client):
        data = {"key": "value"}
        response = client.post("http://httpbin.org/post", json=data)
        response_data = json.loads(response)
        assert response_data["json"] == data

    def test_response_status_code(self, client):
        response = client.get("http://httpbin.org/status/200")
        assert client._last_response.status_code == 200

    def test_cookie_handling(self, client):
        response = client.get("http://httpbin.org/cookies/set/testcookie/testvalue")
        assert "testcookie" in client.cookies
        assert client.cookies["testcookie"] == "testvalue"

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
    async def test_async_post_json(self, async_client):
        data = {"key": "value"}
        response = await async_client.post("http://httpbin.org/post", json=data)
        response_data = json.loads(response)
        assert response_data["json"] == data

    @pytest.mark.asyncio
    async def test_async_status_code_handling(self, async_client):
        response = await async_client.get("http://httpbin.org/status/404")
        assert async_client._last_response.status_code == 404

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
