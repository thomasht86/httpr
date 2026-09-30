"""E2E protocol selection tests against httpbun over TLS, which offers h2 (issue #113)."""

import pytest

import httpr


@pytest.mark.e2e
class TestHttpVersion:
    def test_default_negotiates_http2(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """`http2_only=False` (the default) is ALPN negotiation, not HTTP/1-only."""
        with httpr.Client(ca_cert_file=e2e_ca_cert) as client:
            assert client.get(f"{e2e_base_url}/get").http_version == "HTTP/2"

    def test_http2_only(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        with httpr.Client(ca_cert_file=e2e_ca_cert, http2_only=True) as client:
            assert client.get(f"{e2e_base_url}/get").http_version == "HTTP/2"

    def test_http1_only(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        with httpr.Client(ca_cert_file=e2e_ca_cert, http1_only=True) as client:
            response = client.get(f"{e2e_base_url}/get")
            assert response.status_code == 200
            assert response.http_version == "HTTP/1.1"

    def test_http1_only_streaming(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        with httpr.Client(ca_cert_file=e2e_ca_cert, http1_only=True) as client:
            with client.stream("GET", f"{e2e_base_url}/get") as response:
                assert response.http_version == "HTTP/1.1"

    def test_http1_only_survives_proxy_rebuild(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Assigning `proxy` rebuilds the reqwest client from `ClientConfig` (issue #84)."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert, http1_only=True)
        client.proxy = None
        assert client.get(f"{e2e_base_url}/get").http_version == "HTTP/1.1"

    def test_http1_only_survives_reopen(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        client = httpr.Client(ca_cert_file=e2e_ca_cert, http1_only=True)
        client.close()
        with pytest.warns(httpr.ClientReopenedWarning):
            response = client.get(f"{e2e_base_url}/get")
        assert response.http_version == "HTTP/1.1"

    @pytest.mark.asyncio
    async def test_async_client(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        async with httpr.AsyncClient(ca_cert_file=e2e_ca_cert) as client:
            assert (await client.get(f"{e2e_base_url}/get")).http_version == "HTTP/2"
        async with httpr.AsyncClient(ca_cert_file=e2e_ca_cert, http1_only=True) as client:
            assert (await client.get(f"{e2e_base_url}/get")).http_version == "HTTP/1.1"
