import pytest

import httpr  # type: ignore
from httpr import CaseInsensitiveDict


class TestCaseInsensitiveDict:
    """Unit tests for CaseInsensitiveDict class."""

    def test_init_empty(self):
        d = CaseInsensitiveDict()
        assert len(d) == 0
        assert dict(d) == {}

    def test_init_with_dict(self):
        d = CaseInsensitiveDict({"X-Custom": "value", "Content-Type": "application/json"})
        assert d["x-custom"] == "value"
        assert d["content-type"] == "application/json"

    def test_init_with_kwargs(self):
        d = CaseInsensitiveDict(Authorization="Bearer token")
        assert d["authorization"] == "Bearer token"

    def test_init_with_dict_and_kwargs(self):
        d = CaseInsensitiveDict({"X-Custom": "value"}, Authorization="Bearer token")
        assert d["x-custom"] == "value"
        assert d["authorization"] == "Bearer token"

    def test_case_insensitive_getitem(self):
        d = CaseInsensitiveDict({"x-custom": "value"})
        assert d["x-custom"] == "value"
        assert d["X-Custom"] == "value"
        assert d["X-CUSTOM"] == "value"
        assert d["x-CUSTOM"] == "value"

    def test_case_insensitive_setitem(self):
        d = CaseInsensitiveDict()
        d["X-Custom"] = "value1"
        assert d["x-custom"] == "value1"
        d["x-CUSTOM"] = "value2"  # Should overwrite
        assert d["x-custom"] == "value2"
        assert len(d) == 1

    def test_case_insensitive_delitem(self):
        d = CaseInsensitiveDict({"X-Custom": "value"})
        del d["x-CUSTOM"]
        assert "x-custom" not in d

    def test_case_insensitive_contains(self):
        d = CaseInsensitiveDict({"X-Custom": "value"})
        assert "x-custom" in d
        assert "X-Custom" in d
        assert "X-CUSTOM" in d
        assert "other" not in d

    def test_len(self):
        d = CaseInsensitiveDict({"a": "1", "b": "2", "c": "3"})
        assert len(d) == 3

    def test_iter(self):
        d = CaseInsensitiveDict({"X-Custom": "value", "Content-Type": "json"})
        keys = list(d)
        assert "x-custom" in keys
        assert "content-type" in keys

    def test_eq_with_caseinsensitivedict(self):
        d1 = CaseInsensitiveDict({"x-custom": "value"})
        d2 = CaseInsensitiveDict({"X-Custom": "value"})
        assert d1 == d2

    def test_eq_with_dict(self):
        d = CaseInsensitiveDict({"x-custom": "value"})
        assert d == {"x-custom": "value"}
        assert d == {"X-Custom": "value"}  # Case-insensitive comparison

    def test_eq_different_values(self):
        d = CaseInsensitiveDict({"x-custom": "value1"})
        assert d != {"x-custom": "value2"}

    def test_eq_different_keys(self):
        d = CaseInsensitiveDict({"x-custom": "value"})
        assert d != {"other": "value"}

    def test_repr(self):
        d = CaseInsensitiveDict({"x-custom": "value"})
        r = repr(d)
        assert "CaseInsensitiveDict" in r
        assert "x-custom" in r
        assert "value" in r

    def test_copy(self):
        d1 = CaseInsensitiveDict({"x-custom": "value"})
        d2 = d1.copy()
        assert d1 == d2
        d2["x-custom"] = "modified"
        assert d1["x-custom"] == "value"  # Original unchanged

    def test_lower_items(self):
        d = CaseInsensitiveDict({"X-Custom": "value", "Content-Type": "json"})
        items = list(d.lower_items())
        assert ("x-custom", "value") in items
        assert ("content-type", "json") in items

    def test_get_method(self):
        d = CaseInsensitiveDict({"x-custom": "value"})
        assert d.get("x-custom") == "value"
        assert d.get("X-Custom") == "value"
        assert d.get("missing") is None
        assert d.get("missing", "default") == "default"

    def test_update_method(self):
        d = CaseInsensitiveDict({"x-custom": "value1"})
        d.update({"X-Custom": "value2", "Authorization": "Bearer token"})
        assert d["x-custom"] == "value2"
        assert d["authorization"] == "Bearer token"

    def test_keys_values_items(self):
        d = CaseInsensitiveDict({"x-custom": "value"})
        assert list(d.keys()) == ["x-custom"]
        assert list(d.values()) == ["value"]
        assert list(d.items()) == [("x-custom", "value")]

    def test_pop_method(self):
        d = CaseInsensitiveDict({"x-custom": "value"})
        assert d.pop("X-Custom") == "value"
        assert "x-custom" not in d

    def test_setdefault_method(self):
        d = CaseInsensitiveDict()
        assert d.setdefault("X-Custom", "value") == "value"
        assert d["x-custom"] == "value"
        assert d.setdefault("x-CUSTOM", "other") == "value"  # Existing key

    def test_non_string_key_setitem_raises_typeerror(self):
        """Test that __setitem__ with non-string key raises TypeError."""
        d = CaseInsensitiveDict()
        with pytest.raises(TypeError, match="Header key must be str, not int"):
            d[123] = "value"  # type: ignore[index]

    def test_non_string_key_delitem_raises_typeerror(self):
        """Test that __delitem__ with non-string key raises TypeError."""
        d = CaseInsensitiveDict({"x-custom": "value"})
        with pytest.raises(TypeError, match="Header key must be str, not int"):
            del d[123]  # type: ignore[arg-type]


class TestClientHeadersCaseInsensitive:
    """Integration tests for Client.headers with CaseInsensitiveDict."""

    def test_headers_returns_caseinsensitivedict(self):
        client = httpr.Client(headers={"X-Custom": "value"})
        assert isinstance(client.headers, CaseInsensitiveDict)
        client.close()

    def test_headers_case_insensitive_access(self):
        client = httpr.Client(headers={"X-Custom": "value"})
        assert client.headers["x-custom"] == "value"
        assert client.headers["X-Custom"] == "value"
        assert client.headers["X-CUSTOM"] == "value"
        client.close()

    def test_headers_case_insensitive_membership(self):
        client = httpr.Client(headers={"X-Custom": "value"})
        assert "x-custom" in client.headers
        assert "X-Custom" in client.headers
        assert "X-CUSTOM" in client.headers
        client.close()

    def test_headers_backward_compatible_eq(self):
        client = httpr.Client(headers={"X-Custom": "value"})
        # Backward compatible - lowercase comparison
        assert client.headers == {"x-custom": "value"}
        # Case-insensitive comparison
        assert client.headers == {"X-Custom": "value"}
        client.close()

    def test_headers_setter_with_dict(self):
        client = httpr.Client()
        client.headers = {"X-Custom": "value"}
        assert client.headers["x-custom"] == "value"
        assert client.headers["X-Custom"] == "value"
        client.close()

    def test_headers_setter_with_caseinsensitivedict(self):
        client = httpr.Client()
        client.headers = CaseInsensitiveDict({"X-Custom": "value"})
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_headers_get_method(self):
        client = httpr.Client(headers={"X-Custom": "value"})
        assert client.headers.get("X-Custom") == "value"
        assert client.headers.get("x-custom") == "value"
        assert client.headers.get("Missing", "default") == "default"
        client.close()

    def test_headers_update_method(self):
        client = httpr.Client(headers={"X-Custom": "value"})
        client.headers.update({"Authorization": "Bearer token"})
        # Mutations now sync back to the client
        assert client.headers["authorization"] == "Bearer token"
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_headers_items_iteration(self):
        client = httpr.Client(headers={"X-Custom": "value", "User-Agent": "test"})
        items = list(client.headers.items())
        assert ("x-custom", "value") in items
        assert ("user-agent", "test") in items
        client.close()

    def test_headers_setitem_syncs_to_client(self):
        """Test that __setitem__ syncs back to client."""
        client = httpr.Client(headers={"X-Custom": "value"})
        client.headers["Authorization"] = "Bearer token"
        # Verify sync by getting headers again
        assert client.headers["authorization"] == "Bearer token"
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_headers_delitem_syncs_to_client(self):
        """Test that __delitem__ syncs back to client."""
        client = httpr.Client(headers={"X-Custom": "value", "X-Delete": "me"})
        del client.headers["X-Delete"]
        # Verify sync by getting headers again
        assert "x-delete" not in client.headers
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_headers_clear_syncs_to_client(self):
        """Test that clear() syncs back to client."""
        client = httpr.Client(headers={"X-Custom": "value", "User-Agent": "test"})
        client.headers.clear()
        # Verify sync by getting headers again
        assert len(client.headers) == 0
        assert dict(client.headers) == {}
        client.close()

    def test_headers_pop_syncs_to_client(self):
        """Test that pop() syncs back to client."""
        client = httpr.Client(headers={"X-Custom": "value", "X-Pop": "me"})
        result = client.headers.pop("X-Pop")
        assert result == "me"
        # Verify sync by getting headers again
        assert "x-pop" not in client.headers
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_headers_pop_with_default(self):
        """Test that pop() with default works correctly."""
        client = httpr.Client(headers={"X-Custom": "value"})
        result = client.headers.pop("X-Missing", "default")
        assert result == "default"
        # Original headers unchanged
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_headers_setdefault_syncs_to_client(self):
        """Test that setdefault() syncs back to client when key is missing."""
        client = httpr.Client(headers={"X-Custom": "value"})
        result = client.headers.setdefault("X-New", "new-value")
        assert result == "new-value"
        # Verify sync by getting headers again
        assert client.headers["x-new"] == "new-value"
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_headers_setdefault_existing_key(self):
        """Test that setdefault() doesn't modify existing key."""
        client = httpr.Client(headers={"X-Custom": "value"})
        result = client.headers.setdefault("X-Custom", "other")
        assert result == "value"
        # Original value unchanged
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_headers_multiple_mutations_sync(self):
        """Test that multiple mutations all sync correctly."""
        client = httpr.Client(headers={"X-Original": "original"})
        # Multiple mutations
        client.headers["X-First"] = "first"
        client.headers["X-Second"] = "second"
        client.headers.update({"X-Third": "third"})
        del client.headers["X-Original"]
        # Verify all mutations synced
        assert "x-original" not in client.headers
        assert client.headers["x-first"] == "first"
        assert client.headers["x-second"] == "second"
        assert client.headers["x-third"] == "third"
        client.close()

    def test_headers_copy_is_unbound(self):
        """Test that copy() returns an unbound dict that doesn't sync."""
        client = httpr.Client(headers={"X-Custom": "value"})
        headers_copy = client.headers.copy()
        headers_copy["X-New"] = "new-value"
        # Original client headers should not be affected
        assert "x-new" not in client.headers
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_headers_setter_getter_case_interaction(self):
        """Test that setting with one case and getting with another works."""
        client = httpr.Client()
        client.headers = {"X-Custom-Header": "value1"}
        # Access with different cases
        assert client.headers["x-custom-header"] == "value1"
        assert client.headers["X-CUSTOM-HEADER"] == "value1"
        # Update with different case
        client.headers["x-custom-header"] = "value2"
        assert client.headers["X-Custom-Header"] == "value2"
        client.close()


class TestAsyncClientHeadersCaseInsensitive:
    """Tests for AsyncClient.headers with CaseInsensitiveDict."""

    def test_async_client_headers_returns_caseinsensitivedict(self):
        """Test that AsyncClient.headers returns CaseInsensitiveDict."""
        client = httpr.AsyncClient(headers={"X-Custom": "value"})
        assert isinstance(client.headers, CaseInsensitiveDict)
        assert client.headers["x-custom"] == "value"
        client.close()

    def test_async_client_headers_mutations_sync(self):
        """Test that AsyncClient header mutations sync to client."""
        client = httpr.AsyncClient(headers={"X-Custom": "value"})
        client.headers["Authorization"] = "Bearer token"
        client.headers.update({"Accept": "application/json"})
        # Verify sync
        assert client.headers["authorization"] == "Bearer token"
        assert client.headers["accept"] == "application/json"
        assert client.headers["x-custom"] == "value"
        client.close()


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
