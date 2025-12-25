"""E2E redirect tests using httpbun container."""

import pytest

import httpr


@pytest.mark.e2e
class TestRedirects:
    """Test redirect handling against httpbun container."""

    def test_follow_redirects_enabled(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test following redirect chain with follow_redirects=True (default)."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert, follow_redirects=True)
        response = client.get(f"{e2e_base_url}/redirect/3")

        # Should follow all redirects and end at /anything
        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "GET"
        # Final URL should be /anything after 3 redirects
        assert "anything" in response.url

    def test_follow_redirects_disabled(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test redirect not followed when follow_redirects=False."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert, follow_redirects=False)
        response = client.get(f"{e2e_base_url}/redirect/1")

        # Should get the redirect response, not follow it
        assert response.status_code == 302
        # Location header should be present
        assert "location" in response.headers

    def test_max_redirects_exceeded(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test TooManyRedirects exception when max_redirects is exceeded."""
        client = httpr.Client(
            ca_cert_file=e2e_ca_cert,
            follow_redirects=True,
            max_redirects=2,
        )

        # Request 5 redirects but only allow 2
        with pytest.raises(httpr.TooManyRedirects):
            client.get(f"{e2e_base_url}/redirect/5")

    def test_redirect_preserves_method_get(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test that GET method is preserved through redirects."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert, follow_redirects=True)
        response = client.get(f"{e2e_base_url}/redirect/2")

        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "GET"

    def test_absolute_redirect(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test absolute redirect handling."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert, follow_redirects=True)
        response = client.get(f"{e2e_base_url}/absolute-redirect/2")

        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "GET"

    def test_relative_redirect(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test relative redirect handling."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert, follow_redirects=True)
        response = client.get(f"{e2e_base_url}/relative-redirect/2")

        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "GET"
