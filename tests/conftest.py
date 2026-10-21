import os
import ssl
from wsgiref.simple_server import WSGIServer

import pytest
from pytest_httpbin import certs, serve

# =============================================================================
# Unit test fixtures (pytest-httpbin)
# =============================================================================

# pytest-httpbin's TLS server does each handshake on its single accept thread with a
# hardcoded 1 s socket timeout. A stall of more than 1 s on a loaded CI runner makes
# it drop the connection, and the test fails with RequestError (the Windows x64 wheel
# job of v0.7.8). Handshakes normally take under 10 ms, so allow 10 s instead.
HTTPBIN_TLS_HANDSHAKE_TIMEOUT = 10.0


def _httpbin_secure_get_request(self):
    sock, address = WSGIServer.get_request(self)
    sock.settimeout(HTTPBIN_TLS_HANDSHAKE_TIMEOUT)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        os.path.join(serve.CERT_DIR, "server.pem"),
        os.path.join(serve.CERT_DIR, "server.key"),
    )
    return context.wrap_socket(sock, server_side=True, suppress_ragged_eofs=True), address


serve.SecureWSGIServer.get_request = _httpbin_secure_get_request  # type: ignore[method-assign]


@pytest.fixture
def base_url(httpbin):
    """HTTP base URL from pytest-httpbin."""
    return httpbin.url


@pytest.fixture
def base_url_ssl(httpbin_secure):
    """HTTPS base URL from pytest-httpbin."""
    return httpbin_secure.url


@pytest.fixture
def ca_bundle():
    """CA bundle path for SSL verification with pytest-httpbin."""
    return certs.where()


@pytest.fixture(scope="session")
def test_files(tmp_path_factory):
    """Temporary test files for multipart upload tests."""
    tmp_path_factory.mktemp("data")
    temp_file1 = tmp_path_factory.mktemp("data") / "img1.png"
    with open(temp_file1, "w") as f:
        f.write("aaa111")
    temp_file2 = tmp_path_factory.mktemp("data") / "img2.png"
    with open(temp_file2, "w") as f:
        f.write("bbb222")
    return str(temp_file1), str(temp_file2)


# =============================================================================
# E2E test fixtures (httpbun container)
# =============================================================================


@pytest.fixture
def e2e_base_url() -> str:
    """Base URL for e2e tests against httpbun container.

    Set HTTPR_E2E_URL environment variable to the httpbun URL.
    Skips test if not set (e.g., when running unit tests only).
    """
    url = os.environ.get("HTTPR_E2E_URL")
    if not url:
        pytest.skip("HTTPR_E2E_URL not set - run 'task e2e' for e2e tests")
    return url


@pytest.fixture
def e2e_ca_cert() -> str:
    """CA certificate path for e2e tests against httpbun container.

    Set HTTPR_E2E_CA environment variable to the CA certificate path.
    Skips test if not set (e.g., when running unit tests only).
    """
    ca_path = os.environ.get("HTTPR_E2E_CA")
    if not ca_path:
        pytest.skip("HTTPR_E2E_CA not set - run 'task e2e' for e2e tests")
    if not os.path.exists(ca_path):
        pytest.skip(f"CA cert not found at {ca_path} - run 'task certs' first")
    return ca_path
