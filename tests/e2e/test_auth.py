"""E2E authentication tests using httpbun container."""

import pytest

import httpr


@pytest.mark.e2e
class TestBasicAuth:
    """Test HTTP Basic Authentication against httpbun container."""

    def test_basic_auth_success(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test successful basic auth with correct credentials."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.get(
            f"{e2e_base_url}/basic-auth/testuser/testpass",
            auth=("testuser", "testpass"),
        )

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True
        assert data["user"] == "testuser"

    def test_basic_auth_failure(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test basic auth with incorrect credentials returns 401."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.get(
            f"{e2e_base_url}/basic-auth/testuser/testpass",
            auth=("wronguser", "wrongpass"),
        )

        assert response.status_code == 401

    def test_basic_auth_client_level(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test basic auth configured at client level."""
        client = httpr.Client(
            ca_cert_file=e2e_ca_cert,
            auth=("myuser", "mypass"),
        )
        response = client.get(f"{e2e_base_url}/basic-auth/myuser/mypass")

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True


@pytest.mark.e2e
class TestBearerAuth:
    """Test Bearer token authentication against httpbun container."""

    def test_bearer_auth_success(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test successful bearer auth with correct token."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.get(
            f"{e2e_base_url}/bearer/my-secret-token",
            auth_bearer="my-secret-token",
        )

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True
        assert data["token"] == "my-secret-token"

    def test_bearer_auth_failure(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test bearer auth with wrong token returns authenticated=false."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.get(
            f"{e2e_base_url}/bearer/expected-token",
            auth_bearer="wrong-token",
        )

        # httpbun returns 200 with authenticated=false for wrong tokens
        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is False

    def test_bearer_auth_client_level(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test bearer auth configured at client level."""
        client = httpr.Client(
            ca_cert_file=e2e_ca_cert,
            auth_bearer="client-token",
        )
        response = client.get(f"{e2e_base_url}/bearer/client-token")

        assert response.status_code == 200
        data = response.json()
        assert data["authenticated"] is True

    def test_bearer_auth_header_check(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test that bearer token is sent in Authorization header."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        response = client.get(
            f"{e2e_base_url}/headers",
            auth_bearer="check-header-token",
        )

        assert response.status_code == 200
        data = response.json()
        # Verify Authorization header contains Bearer token
        assert "Authorization" in data["headers"]
        assert data["headers"]["Authorization"] == "Bearer check-header-token"
