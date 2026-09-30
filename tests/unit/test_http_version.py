"""`http1_only` and `response.http_version` (issue #113).

pytest-httpbin only speaks HTTP/1.1, so these tests cover the plumbing; the
HTTP/2 cases run against httpbun over TLS in tests/e2e/test_http_version.py.
"""

import pytest

import httpr


def test_http_version_buffered(base_url):
    response = httpr.Client().get(f"{base_url}/get")
    assert response.http_version == "HTTP/1.1"


def test_http_version_over_tls_without_h2(base_url_ssl, ca_bundle):
    """ALPN falls back to HTTP/1.1 when the server doesn't offer h2."""
    response = httpr.Client(ca_cert_file=ca_bundle).get(f"{base_url_ssl}/get")
    assert response.status_code == 200
    assert response.http_version == "HTTP/1.1"


def test_http_version_streaming(base_url):
    with httpr.Client().stream("GET", f"{base_url}/get") as response:
        assert response.http_version == "HTTP/1.1"


@pytest.mark.asyncio
async def test_http_version_async(base_url):
    async with httpr.AsyncClient() as client:
        response = await client.get(f"{base_url}/get")
        assert response.http_version == "HTTP/1.1"
        async with client.stream("GET", f"{base_url}/get") as streamed:
            assert streamed.http_version == "HTTP/1.1"


@pytest.mark.parametrize("client_cls", [httpr.Client, httpr.AsyncClient])
def test_http1_only_accepted(base_url, client_cls):
    client = client_cls(http1_only=True)
    if client_cls is httpr.Client:
        assert client.get(f"{base_url}/get").http_version == "HTTP/1.1"


@pytest.mark.parametrize("client_cls", [httpr.Client, httpr.AsyncClient])
def test_http1_only_and_http2_only_conflict(client_cls):
    with pytest.raises(ValueError, match="http1_only or http2_only"):
        client_cls(http1_only=True, http2_only=True)
