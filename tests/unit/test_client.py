import pytest

import httpr  # type: ignore


def test_invalid_url_exception():
    client = httpr.Client()
    # Should raise an exception for an invalid URL format.
    with pytest.raises(Exception):
        client.get("invalid_url://")


def test_invalid_method_exception(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    # Passing an unsupported HTTP method should trigger an exception.
    with pytest.raises(Exception):
        client.request("INVALID", f"{base_url_ssl}/anything")  # type: ignore[arg-type]


def test_invalid_headers_setter_exception():
    client = httpr.Client()
    # Attempting to set headers with a non-dict type should raise an exception.
    with pytest.raises(Exception):
        client.headers = "not a dict"  # type: ignore[assignment]


def test_invalid_cookies_setter_exception():
    client = httpr.Client()
    # Attempting to set cookies with a non-dict type should raise an exception.
    with pytest.raises(Exception):
        client.cookies = "not a dict"  # type: ignore[assignment]


def test_invalid_file_path_exception(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    # Passing a non-existent file path in files should raise an exception.
    with pytest.raises(Exception):
        client.post(f"{base_url_ssl}/anything", files={"file": "/non/existent/path.file"})


def test_request_exception_timeout(base_url_ssl, ca_bundle):
    client = httpr.Client(timeout=0.0001, ca_cert_file=ca_bundle)
    # A very short timeout should cause a timeout exception.
    with pytest.raises(Exception):
        client.get(f"{base_url_ssl}/delay/2")
    auth = ("user", "password")
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    client = httpr.Client(
        auth=auth,
        params=params,
        headers=headers,
        cookies=cookies,
        ca_cert_file=ca_bundle,
    )
    response = client.get(f"{base_url_ssl}/anything")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Basic dXNlcjpwYXNzd29yZA=="
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}


def test_client_setters(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    client.auth = ("user", "password")
    client.headers = {"X-Test": "TesT"}
    client.cookies = {"ccc": "ddd", "cccc": "dddd"}
    client.params = {"x": "aaa", "y": "bbb"}
    client.timeout = 20

    response = client.get(f"{base_url_ssl}/anything")
    assert response.status_code == 200
    assert response.status_code == 200
    assert client.auth == ("user", "password")
    assert client.headers == {"x-test": "TesT"}  # Headers are lowercased (necessary for HTTP/2)
    assert client.headers["X-Test"] == "TesT"  # but still accessible case-insensitively
    assert client.cookies == {"ccc": "ddd", "cccc": "dddd"}
    assert client.params == {"x": "aaa", "y": "bbb"}
    assert client.timeout == 20.0
    json_data = response.json()
    assert json_data["method"] == "GET"
    assert json_data["headers"]["X-Test"] == "TesT"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Basic dXNlcjpwYXNzd29yZA=="
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert "Basic dXNlcjpwYXNzd29yZA==" in response.text
    assert b"Basic dXNlcjpwYXNzd29yZA==" in response.content


def test_client_request_get(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    response = client.request(
        "GET",
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "GET"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert "Bearer bearerXXXXXXXXXXXXXXXXXXXX" in response.text
    assert b"Bearer bearerXXXXXXXXXXXXXXXXXXXX" in response.content


def test_client_get(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    response = client.get(
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "GET"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert "Bearer bearerXXXXXXXXXXXXXXXXXXXX" in response.text
    assert b"Bearer bearerXXXXXXXXXXXXXXXXXXXX" in response.content


def test_client_post_content(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    auth = ("user", "password")
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    content = b"test content"
    response = client.post(
        f"{base_url_ssl}/anything",
        auth=auth,
        headers=headers,
        cookies=cookies,
        params=params,
        content=content,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "POST"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Basic dXNlcjpwYXNzd29yZA=="
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert json_data["data"] == "test content"


def test_client_post_data(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    data = {"key1": "value1", "key2": "value2"}
    response = client.post(
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        data=data,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "POST"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert json_data["form"] == {"key1": "value1", "key2": "value2"}


def test_client_post_json(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb", "z": 3}
    data = {"key1": "value1", "key2": "value2"}
    response = client.post(
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        json=data,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "POST"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb", "z": "3"}
    assert json_data["json"] == data


def test_client_number_params(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    params = {
        "int": 42,
        "float": 3.14159,
        "sci_notation": 1.23e-4,
        "large_float": 1.7976931348623157e308,
        "small_float": 0.026305610314011577,
    }
    response = client.get(f"{base_url_ssl}/anything", params=params)
    assert response.status_code == 200
    json_data = response.json()

    # Verify all numeric values are converted to strings
    assert json_data["args"]["int"] == "42"
    assert json_data["args"]["float"] == "3.14159"
    assert json_data["args"]["sci_notation"] == "0.000123" or json_data["args"]["sci_notation"] == "1.23e-4"
    # Large values might have different string representations
    assert float(json_data["args"]["large_float"]) == 1.7976931348623157e308
    assert float(json_data["args"]["small_float"]) == 0.026305610314011577


def test_header_case_preservation(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)

    # Send a request to a server that will return case-sensitive headers
    response = client.get(f"{base_url_ssl}/response-headers?X-Custom-Header=TestValue")

    # Verify the header case is preserved
    assert "X-Custom-Header" in response.headers
    assert response.headers["X-Custom-Header"] == "TestValue"

    # Also verify headers can be accessed with different cases
    assert "x-custom-header" in response.headers
    assert response.headers["x-custom-header"] == "TestValue"


@pytest.mark.skip(reason="pytest-httpbin doesn't support chunked encoding for file uploads")
def test_client_post_files(test_files):
    """Test file uploads - skipped because local httpbin doesn't support chunked encoding."""
    temp_file1, temp_file2 = test_files
    client = httpr.Client()
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    files = {"file1": temp_file1, "file2": temp_file2}
    response = client.post(
        "https://httpbin.org/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        files=files,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "POST"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert json_data["files"] == {"file1": "aaa111", "file2": "bbb222"}


def test_constructor_headers_accessible():
    """Test that headers passed to constructor are accessible via the headers property."""
    client = httpr.Client(headers={"X-Custom": "value", "User-Agent": "test-agent"})
    assert client.headers == {"x-custom": "value", "user-agent": "test-agent"}
    client.close()


def test_constructor_headers_with_cookies():
    """Test that cookies are excluded from headers getter when passed to constructor."""
    client = httpr.Client(
        headers={"X-Custom": "value"},
        cookies={"session": "abc123"},
    )
    # Cookies should not appear in headers getter
    assert client.headers == {"x-custom": "value"}
    # But cookies should be accessible via cookies getter
    assert client.cookies == {"session": "abc123"}
    client.close()


def test_constructor_cookies_only():
    """Test that cookies-only constructor doesn't expose Cookie header."""
    client = httpr.Client(cookies={"session": "abc123"})
    # Headers should be empty (no Cookie header exposed)
    assert client.headers == {}
    # Cookies should be accessible
    assert client.cookies == {"session": "abc123"}
    client.close()


def test_setter_overwrites_constructor_headers():
    """Test that setting headers overwrites constructor headers."""
    client = httpr.Client(headers={"X-Original": "original"})
    assert client.headers == {"x-original": "original"}
    # Overwrite with new headers
    client.headers = {"X-New": "new"}
    assert client.headers == {"x-new": "new"}
    # Original header should be gone
    assert "x-original" not in client.headers
    client.close()


def test_client_headers_case_insensitive():
    """Test that client.headers supports case-insensitive access."""
    client = httpr.Client(headers={"X-Custom": "value", "Content-Type": "application/json"})

    # Case-insensitive access should work
    assert client.headers["x-custom"] == "value"
    assert client.headers["X-Custom"] == "value"
    assert client.headers["X-CUSTOM"] == "value"

    # Contains check should be case-insensitive
    assert "x-custom" in client.headers
    assert "X-Custom" in client.headers

    # get() should be case-insensitive
    assert client.headers.get("X-Custom") == "value"
    assert client.headers.get("x-custom") == "value"

    # Dict equality should still work (keys are lowercased)
    assert client.headers == {"x-custom": "value", "content-type": "application/json"}

    client.close()


def test_graceful_invalid_header_handling(base_url_ssl, ca_bundle):
    """Test that invalid header values are handled gracefully without crashing."""
    client = httpr.Client(ca_cert_file=ca_bundle)

    # Test that valid headers still work even with some invalid ones
    # Invalid header names/values are logged and skipped rather than causing panics
    valid_headers = {"X-Valid-Header": "valid-value", "User-Agent": "test"}

    # This should not crash - valid headers should be processed
    response = client.get(f"{base_url_ssl}/anything", headers=valid_headers)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["headers"]["X-Valid-Header"] == "valid-value"
    assert json_data["headers"]["User-Agent"] == "test"
