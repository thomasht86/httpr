import os

import pytest
from pytest_httpbin import certs


# =============================================================================
# Unit test fixtures (pytest-httpbin)
# =============================================================================


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
