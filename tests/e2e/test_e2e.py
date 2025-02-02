import pytest
import json
from httpr import Client, AsyncClient


# Define a common base URL fixture for httpbin.org endpoints
@pytest.fixture(scope="session")
def base_url():
    return "http://httpbin.org"


# -----------------------------
# Synchronous Client Tests
# -----------------------------
class TestSyncClient:
    @pytest.fixture
    def client(self):
        """Creates a synchronous httpr Client with a 10-second timeout."""
        return Client(timeout=10.0)

    def test_get_success(self, client, base_url):
        """Test a successful GET request."""
        response = client.get(f"{base_url}/get")
        assert isinstance(response, str)
        response_data = json.loads(response)
        assert response_data["url"] == f"{base_url}/get"

    def test_invalid_url(self, client):
        """Test that an invalid URL raises an exception."""
        with pytest.raises(Exception):
            client.get("invalid://url")

    def test_params_in_url(self, client, base_url):
        """Test that URL parameters are correctly passed and received."""
        params = {"key1": "value1", "key2": "value2"}
        response = client.get(f"{base_url}/get", params=params)
        response_data = json.loads(response)
        assert response_data["args"] == params

    def test_custom_headers(self, client, base_url):
        """Test that custom headers are correctly sent."""
        headers = {"User-Agent": "test-agent/1.0"}
        response = client.get(f"{base_url}/headers", headers=headers)
        response_data = json.loads(response)
        # The header key may have different capitalization in the response
        actual_agent = response_data["headers"].get("User-Agent") or response_data[
            "headers"
        ].get("user-agent")
        assert actual_agent == headers["User-Agent"]

    def test_post_form_data(self, client, base_url):
        """Test that form data is correctly posted."""
        data = {"key": "value"}
        response = client.post(f"{base_url}/post", data=data)
        response_data = json.loads(response)
        assert response_data["form"] == data

    def test_post_json_data(self, client, base_url):
        """Test that JSON data is correctly posted."""
        data = {"key": "value"}
        response = client.post(f"{base_url}/post", json=data)
        response_data = json.loads(response)
        assert response_data["json"] == data

    def test_response_status_code(self, client, base_url):
        """Test that the client stores the last response's status code."""
        client.get(f"{base_url}/status/200")
        assert client._last_response.status_code == 200

    def test_cookie_handling(self, client, base_url):
        """Test that cookies are stored correctly after a set-cookie request."""
        client.get(f"{base_url}/cookies/set/testcookie/testvalue")
        assert "testcookie" in client.cookies
        assert client.cookies["testcookie"] == "testvalue"

    def test_timeout(self, base_url):
        """Test that a request exceeding the timeout raises an exception."""
        fast_client = Client(timeout=0.1)
        with pytest.raises(Exception):
            fast_client.get(f"{base_url}/delay/1")

    def test_redirect_following(self, base_url):
        """Test that redirect following can be disabled."""
        no_redirect_client = Client(follow_redirects=False)
        response = no_redirect_client.get(f"{base_url}/redirect/1")
        assert "Redirecting" in response  # Assuming the response contains this phrase


# -----------------------------
# Asynchronous Client Tests
# -----------------------------
class TestAsyncClient:
    @pytest.fixture
    def async_client(self):
        """Creates an asynchronous httpr AsyncClient with redirect following enabled."""
        return AsyncClient(follow_redirects=True)

    @pytest.mark.asyncio
    async def test_async_get_success(self, async_client, base_url):
        """Test a successful asynchronous GET request."""
        response = await async_client.get(f"{base_url}/get")
        assert isinstance(response, str)
        response_data = json.loads(response)
        assert response_data["url"] == f"{base_url}/get"

    @pytest.mark.asyncio
    async def test_async_timeout_validation(self):
        """Test that providing an invalid timeout type raises a TypeError."""
        with pytest.raises(TypeError):
            AsyncClient(timeout="invalid")

    @pytest.mark.asyncio
    async def test_async_timeout_behavior(self, base_url):
        """Test that an asynchronous request exceeding the timeout raises an exception."""
        fast_client = AsyncClient(timeout=0.1)
        with pytest.raises(Exception):
            await fast_client.get(f"{base_url}/delay/1")

    @pytest.mark.asyncio
    async def test_async_post_json(self, async_client, base_url):
        """Test that JSON data is correctly posted in an asynchronous request."""
        data = {"key": "value"}
        response = await async_client.post(f"{base_url}/post", json=data)
        response_data = json.loads(response)
        assert response_data["json"] == data

    @pytest.mark.asyncio
    async def test_async_status_code_handling(self, async_client, base_url):
        """Test that the asynchronous client stores the last response's status code."""
        await async_client.get(f"{base_url}/status/404")
        assert async_client._last_response.status_code == 404

    @pytest.mark.asyncio
    async def test_async_redirect_handling(self, base_url):
        """Test that the asynchronous client follows redirects correctly."""
        client = AsyncClient(follow_redirects=True)
        response = await client.get(f"{base_url}/redirect/1")
        response_data = json.loads(response)
        # After following the redirect, the final URL should be /get
        assert response_data["url"] == f"{base_url}/get"


# -----------------------------
# Configuration Tests
# -----------------------------
def test_client_configuration():
    """Test that client configuration is properly set upon initialization."""
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
