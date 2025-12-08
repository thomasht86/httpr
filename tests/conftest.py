import pytest
from pytest_httpbin import certs


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
