import pytest
import httpr  # type: ignore


def test_request_get(base_url_ssl, ca_bundle):
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    response = httpr.request(
        "GET",
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        ca_cert_file=ca_bundle,
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


def test_get(base_url_ssl, ca_bundle):
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    response = httpr.get(
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        ca_cert_file=ca_bundle,
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


def test_head(base_url_ssl, ca_bundle):
    response = httpr.head(f"{base_url_ssl}/anything", ca_cert_file=ca_bundle)
    assert response.status_code == 200
    assert "content-length" in response.headers


def test_options(base_url_ssl, ca_bundle):
    response = httpr.options(f"{base_url_ssl}/anything", ca_cert_file=ca_bundle)
    assert response.status_code == 200
    assert sorted(response.headers["allow"].split(", ")) == [
        "DELETE",
        "GET",
        "HEAD",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
        "TRACE",
    ]


def test_delete(base_url_ssl, ca_bundle):
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    response = httpr.delete(
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        ca_cert_file=ca_bundle,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "DELETE"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert "Bearer bearerXXXXXXXXXXXXXXXXXXXX" in response.text
    assert b"Bearer bearerXXXXXXXXXXXXXXXXXXXX" in response.content


def test_post_content(base_url_ssl, ca_bundle):
    auth = ("user", "password")
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    content = b"test content"
    response = httpr.post(
        f"{base_url_ssl}/anything",
        auth=auth,
        headers=headers,
        cookies=cookies,
        params=params,
        content=content,
        ca_cert_file=ca_bundle,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "POST"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Basic dXNlcjpwYXNzd29yZA=="
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert json_data["data"] == "test content"


def test_post_data(base_url_ssl, ca_bundle):
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    data = {"key1": "value1", "key2": "value2"}
    response = httpr.post(
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        data=data,
        ca_cert_file=ca_bundle,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "POST"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert json_data["form"] == {"key1": "value1", "key2": "value2"}


def test_post_json(base_url_ssl, ca_bundle):
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    data = {"key1": "value1", "key2": "value2"}
    response = httpr.post(
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        json=data,
        ca_cert_file=ca_bundle,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "POST"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert json_data["json"] == data


@pytest.mark.skip(reason="pytest-httpbin doesn't support chunked encoding for file uploads")
def test_client_post_files(test_files):
    """Test file uploads - skipped because local httpbin doesn't support chunked encoding."""
    temp_file1, temp_file2 = test_files
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    files = {"file1": temp_file1, "file2": temp_file2}
    response = httpr.post(
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


def test_patch(base_url_ssl, ca_bundle):
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    data = {"key1": "value1", "key2": "value2"}
    response = httpr.patch(
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        data=data,
        ca_cert_file=ca_bundle,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "PATCH"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert json_data["form"] == {"key1": "value1", "key2": "value2"}


def test_put(base_url_ssl, ca_bundle):
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    data = {"key1": "value1", "key2": "value2"}
    response = httpr.put(
        f"{base_url_ssl}/anything",
        auth_bearer=auth_bearer,
        headers=headers,
        cookies=cookies,
        params=params,
        data=data,
        ca_cert_file=ca_bundle,
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "PUT"
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Bearer bearerXXXXXXXXXXXXXXXXXXXX"
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
    assert json_data["form"] == {"key1": "value1", "key2": "value2"}
