"""E2E SSL tests using httpbun container."""

import pytest

import httpr


@pytest.mark.e2e
class TestSSL:
    """SSL/TLS tests against httpbun container."""

    def test_get_with_ssl(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test basic HTTPS GET request with custom CA certificate."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.get(f"{e2e_base_url}/any")

        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "GET"
        assert "httpbun.local" in data["url"]

    def test_post_json_with_ssl(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test HTTPS POST with JSON body."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        payload = {"key": "value", "number": 42}
        response = client.post(f"{e2e_base_url}/any", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "POST"
        assert data["json"] == payload

    def test_headers_with_ssl(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test custom headers are sent correctly over SSL."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        custom_headers = {"X-Custom-Header": "test-value", "X-Another": "another-value"}
        response = client.get(f"{e2e_base_url}/headers", headers=custom_headers)

        assert response.status_code == 200
        data = response.json()
        # httpbun returns headers in lowercase
        assert data["headers"]["X-Custom-Header"] == "test-value"
        assert data["headers"]["X-Another"] == "another-value"
