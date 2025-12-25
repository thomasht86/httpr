"""E2E async client tests using httpbun container."""

import pytest

import httpr


@pytest.mark.e2e
class TestAsyncClient:
    """Test AsyncClient against httpbun container."""

    async def test_async_get(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test basic async GET request over HTTPS."""
        async with httpr.AsyncClient(ca_cert_file=e2e_ca_cert) as client:
            response = await client.get(f"{e2e_base_url}/any")

        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "GET"

    async def test_async_post_json(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test async POST with JSON body."""
        async with httpr.AsyncClient(ca_cert_file=e2e_ca_cert) as client:
            payload = {"async": True, "value": 123}
            response = await client.post(f"{e2e_base_url}/any", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "POST"
        assert data["json"] == payload

    async def test_async_multiple_requests(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test multiple async requests with same client."""
        async with httpr.AsyncClient(ca_cert_file=e2e_ca_cert) as client:
            response1 = await client.get(f"{e2e_base_url}/any")
            response2 = await client.get(f"{e2e_base_url}/headers")
            response3 = await client.post(f"{e2e_base_url}/any", json={"test": 1})

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

    async def test_async_with_auth(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test async request with basic auth."""
        async with httpr.AsyncClient(ca_cert_file=e2e_ca_cert) as client:
            response = await client.get(
                f"{e2e_base_url}/basic-auth/asyncuser/asyncpass",
                auth=("asyncuser", "asyncpass"),
            )

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True

    async def test_async_streaming(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test async streaming response."""
        async with httpr.AsyncClient(ca_cert_file=e2e_ca_cert) as client:
            url = f"{e2e_base_url}/drip?numbytes=10&duration=1&delay=0"

            chunks = []
            async with client.stream("GET", url) as response:
                assert response.status_code == 200
                for chunk in response.iter_bytes():
                    chunks.append(chunk)

        total_bytes = b"".join(chunks)
        assert len(total_bytes) == 10

    async def test_async_redirect(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test async redirect following."""
        async with httpr.AsyncClient(ca_cert_file=e2e_ca_cert, follow_redirects=True) as client:
            response = await client.get(f"{e2e_base_url}/redirect/2")

        assert response.status_code == 200
        assert "anything" in response.url

    async def test_async_headers(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test async request with custom headers."""
        async with httpr.AsyncClient(ca_cert_file=e2e_ca_cert) as client:
            response = await client.get(
                f"{e2e_base_url}/headers",
                headers={"X-Async-Header": "async-value"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["headers"]["X-Async-Header"] == "async-value"
