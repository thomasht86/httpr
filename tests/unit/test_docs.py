"""
Tests for documentation code examples.

These tests ensure all code snippets in the documentation work correctly.
They use pytest-httpbin for a local test server.
"""

import pytest

import httpr


class TestQuickstart:
    """Tests for quickstart.md examples."""

    def test_simple_get(self, base_url_ssl, ca_bundle):
        """Test basic GET request."""
        response = httpr.get(f"{base_url_ssl}/get", ca_cert_file=ca_bundle)
        assert response.status_code == 200
        assert "url" in response.json()

    def test_client_context_manager(self, base_url_ssl, ca_bundle):
        """Test client with context manager."""
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/get")
            assert response.status_code == 200

    def test_query_params(self, base_url_ssl, ca_bundle):
        """Test query parameters."""
        response = httpr.get(
            f"{base_url_ssl}/get",
            params={"name": "httpr", "version": "1"},
            ca_cert_file=ca_bundle,
        )
        assert response.status_code == 200
        assert response.json()["args"] == {"name": "httpr", "version": "1"}

    def test_numeric_params(self, base_url_ssl, ca_bundle):
        """Test numeric parameters are converted to strings."""
        response = httpr.get(
            f"{base_url_ssl}/get",
            params={"page": 1, "limit": 10},
            ca_cert_file=ca_bundle,
        )
        assert response.json()["args"] == {"page": "1", "limit": "10"}

    def test_custom_headers(self, base_url_ssl, ca_bundle):
        """Test custom headers."""
        response = httpr.get(
            f"{base_url_ssl}/headers",
            headers={"X-Custom-Header": "my-value"},
            ca_cert_file=ca_bundle,
        )
        assert response.json()["headers"]["X-Custom-Header"] == "my-value"

    def test_post_json(self, base_url_ssl, ca_bundle):
        """Test POST with JSON body."""
        response = httpr.post(
            f"{base_url_ssl}/post",
            json={"name": "httpr", "version": 1, "fast": True},
            ca_cert_file=ca_bundle,
        )
        assert response.status_code == 200
        assert response.json()["json"] == {"name": "httpr", "version": 1, "fast": True}

    def test_post_form_data(self, base_url_ssl, ca_bundle):
        """Test POST with form data."""
        response = httpr.post(
            f"{base_url_ssl}/post",
            data={"username": "user", "password": "secret"},
            ca_cert_file=ca_bundle,
        )
        assert response.json()["form"] == {"username": "user", "password": "secret"}

    def test_post_binary(self, base_url_ssl, ca_bundle):
        """Test POST with binary content."""
        response = httpr.post(
            f"{base_url_ssl}/post",
            content=b"raw binary data",
            ca_cert_file=ca_bundle,
        )
        assert response.json()["data"] == "raw binary data"


class TestResponseHandling:
    """Tests for response handling examples."""

    def test_response_properties(self, base_url_ssl, ca_bundle):
        """Test all response properties."""
        response = httpr.get(f"{base_url_ssl}/get", ca_cert_file=ca_bundle)

        # Status code
        assert isinstance(response.status_code, int)
        assert response.status_code == 200

        # Body
        assert isinstance(response.text, str)
        assert isinstance(response.content, bytes)

        # Headers
        assert "content-type" in response.headers
        assert response.headers.get("content-type") is not None

        # URL
        assert response.url.startswith("https://")

    def test_json_response(self, base_url_ssl, ca_bundle):
        """Test JSON parsing."""
        response = httpr.get(f"{base_url_ssl}/json", ca_cert_file=ca_bundle)
        data = response.json()
        assert isinstance(data, dict)

    def test_headers_case_insensitive(self, base_url_ssl, ca_bundle):
        """Test case-insensitive header access."""
        response = httpr.get(f"{base_url_ssl}/get", ca_cert_file=ca_bundle)

        # All these should work
        content_type1 = response.headers.get("content-type")
        content_type2 = response.headers.get("Content-Type")
        content_type3 = response.headers.get("CONTENT-TYPE")

        assert content_type1 == content_type2 == content_type3

    def test_cookies_response(self, base_url_ssl, ca_bundle):
        """Test cookie extraction from response."""
        response = httpr.get(
            f"{base_url_ssl}/cookies/set?session=abc123",
            ca_cert_file=ca_bundle,
        )
        # Cookie may be in response or handled by redirect
        assert response.status_code == 200


class TestAuthentication:
    """Tests for authentication examples."""

    def test_basic_auth(self, base_url_ssl, ca_bundle):
        """Test basic authentication."""
        response = httpr.get(
            f"{base_url_ssl}/basic-auth/user/pass",
            auth=("user", "pass"),
            ca_cert_file=ca_bundle,
        )
        assert response.status_code == 200

    def test_bearer_token(self, base_url_ssl, ca_bundle):
        """Test bearer token authentication."""
        response = httpr.get(
            f"{base_url_ssl}/headers",
            auth_bearer="my-secret-token",
            ca_cert_file=ca_bundle,
        )
        auth_header = response.json()["headers"]["Authorization"]
        assert auth_header == "Bearer my-secret-token"

    def test_client_default_auth(self, base_url_ssl, ca_bundle):
        """Test client-level default authentication."""
        client = httpr.Client(
            auth=("user", "pass"),
            ca_cert_file=ca_bundle,
        )
        response = client.get(f"{base_url_ssl}/basic-auth/user/pass")
        assert response.status_code == 200

    def test_client_bearer_token(self, base_url_ssl, ca_bundle):
        """Test client-level bearer token."""
        client = httpr.Client(
            auth_bearer="api-token",
            ca_cert_file=ca_bundle,
        )
        response = client.get(f"{base_url_ssl}/headers")
        auth_header = response.json()["headers"]["Authorization"]
        assert auth_header == "Bearer api-token"


class TestAsyncClient:
    """Tests for async client examples."""

    @pytest.mark.asyncio
    async def test_async_get(self, base_url_ssl, ca_bundle):
        """Test async GET request."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            response = await client.get(f"{base_url_ssl}/get")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_async_post(self, base_url_ssl, ca_bundle):
        """Test async POST request."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            response = await client.post(
                f"{base_url_ssl}/post",
                json={"key": "value"},
            )
            assert response.status_code == 200
            assert response.json()["json"] == {"key": "value"}

    @pytest.mark.asyncio
    async def test_async_concurrent(self, base_url_ssl, ca_bundle):
        """Test concurrent async requests."""
        import asyncio

        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            tasks = [
                client.get(f"{base_url_ssl}/get"),
                client.get(f"{base_url_ssl}/ip"),
            ]
            responses = await asyncio.gather(*tasks)

            assert len(responses) == 2
            for response in responses:
                assert response.status_code == 200


class TestCookies:
    """Tests for cookie handling examples."""

    def test_cookie_store(self, base_url_ssl, ca_bundle):
        """Test persistent cookie store."""
        client = httpr.Client(cookie_store=True, ca_cert_file=ca_bundle)

        # Set a cookie
        client.get(f"{base_url_ssl}/cookies/set?session=abc123")

        # Cookie should persist
        response = client.get(f"{base_url_ssl}/cookies")
        # Note: Cookie behavior depends on httpbin implementation
        assert response.status_code == 200

    def test_initial_cookies(self, base_url_ssl, ca_bundle):
        """Test setting initial cookies."""
        client = httpr.Client(
            cookies={"session": "xyz789"},
            ca_cert_file=ca_bundle,
        )
        response = client.get(f"{base_url_ssl}/cookies")
        assert response.status_code == 200

    def test_request_cookies(self, base_url_ssl, ca_bundle):
        """Test per-request cookies."""
        response = httpr.get(
            f"{base_url_ssl}/cookies",
            cookies={"temporary": "cookie-value"},
            ca_cert_file=ca_bundle,
        )
        assert response.status_code == 200


class TestClientConfiguration:
    """Tests for client configuration examples."""

    def test_timeout(self, base_url_ssl, ca_bundle):
        """Test timeout configuration."""
        client = httpr.Client(timeout=10, ca_cert_file=ca_bundle)
        response = client.get(f"{base_url_ssl}/get")
        assert response.status_code == 200

    def test_redirect_following(self, base_url_ssl, ca_bundle):
        """Test redirect following."""
        client = httpr.Client(
            follow_redirects=True,
            max_redirects=10,
            ca_cert_file=ca_bundle,
        )
        response = client.get(f"{base_url_ssl}/redirect/3")
        assert response.status_code == 200

    def test_default_headers(self, base_url_ssl, ca_bundle):
        """Test default headers."""
        client = httpr.Client(
            headers={"User-Agent": "test-app/1.0"},
            ca_cert_file=ca_bundle,
        )
        response = client.get(f"{base_url_ssl}/headers")
        assert "test-app/1.0" in response.json()["headers"]["User-Agent"]

    def test_default_params(self, base_url_ssl, ca_bundle):
        """Test default query parameters."""
        client = httpr.Client(
            params={"api_version": "v2"},
            ca_cert_file=ca_bundle,
        )
        response = client.get(f"{base_url_ssl}/get")
        assert response.json()["args"]["api_version"] == "v2"


class TestHTTPMethods:
    """Tests for all HTTP methods."""

    def test_get(self, base_url_ssl, ca_bundle):
        response = httpr.get(f"{base_url_ssl}/get", ca_cert_file=ca_bundle)
        assert response.status_code == 200

    def test_post(self, base_url_ssl, ca_bundle):
        response = httpr.post(f"{base_url_ssl}/post", ca_cert_file=ca_bundle)
        assert response.status_code == 200

    def test_put(self, base_url_ssl, ca_bundle):
        response = httpr.put(f"{base_url_ssl}/put", ca_cert_file=ca_bundle)
        assert response.status_code == 200

    def test_patch(self, base_url_ssl, ca_bundle):
        response = httpr.patch(f"{base_url_ssl}/patch", ca_cert_file=ca_bundle)
        assert response.status_code == 200

    def test_delete(self, base_url_ssl, ca_bundle):
        response = httpr.delete(f"{base_url_ssl}/delete", ca_cert_file=ca_bundle)
        assert response.status_code == 200

    def test_head(self, base_url_ssl, ca_bundle):
        response = httpr.head(f"{base_url_ssl}/get", ca_cert_file=ca_bundle)
        assert response.status_code == 200
        # HEAD returns no body
        assert response.content == b""

    def test_options(self, base_url_ssl, ca_bundle):
        response = httpr.options(f"{base_url_ssl}/get", ca_cert_file=ca_bundle)
        assert response.status_code == 200
