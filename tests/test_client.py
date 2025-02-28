# filepath: /Users/thomas/Repos/httpr-1/tests/test_client_exceptions.py
from time import sleep
import pytest
import httpr  # type: ignore
import certifi

def retry(max_retries=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        sleep(delay)
                        continue
                    else:
                        raise e
        return wrapper
    return decorator

@retry()
def test_invalid_url_exception():
    client = httpr.Client()
    # Should raise an exception for an invalid URL format.
    with pytest.raises(Exception):
        client.get("invalid_url://")

@retry()
def test_invalid_method_exception():
    client = httpr.Client()
    # Passing an unsupported HTTP method should trigger an exception.
    with pytest.raises(Exception):
        client.request("INVALID", "https://httpbin.org/anything")

@retry()
def test_invalid_headers_setter_exception():
    client = httpr.Client()
    # Attempting to set headers with a non-dict type should raise an exception.
    with pytest.raises(Exception):
        client.headers = "not a dict"

@retry()
def test_invalid_cookies_setter_exception():
    client = httpr.Client()
    # Attempting to set cookies with a non-dict type should raise an exception.
    with pytest.raises(Exception):
        client.cookies = "not a dict"

@retry()
def test_invalid_file_path_exception():
    client = httpr.Client()
    # Passing a non-existent file path in files should raise an exception.
    with pytest.raises(Exception):
        client.post(
            "https://httpbin.org/anything",
            files={"file": "/non/existent/path.file"}
        )

@retry()
def test_request_exception_timeout():
    client = httpr.Client(timeout=0.0001)  # unrealistic timeout to force a timeout error
    # A very short timeout should cause a timeout exception.
    with pytest.raises(Exception):
        client.get("https://httpbin.org/delay/2")
    auth = ("user", "password")
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    client = httpr.Client(
        auth=auth,
        params=params,
        headers=headers,
        cookies=cookies,
        ca_cert_file=certifi.where(),
    )
    response = client.get("https://httpbin.org/anything")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Basic dXNlcjpwYXNzd29yZA=="
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}


@retry()
def test_client_setters():
    client = httpr.Client()
    client.auth = ("user", "password")
    client.headers = {"X-Test": "TesT"}
    client.cookies = {"ccc": "ddd", "cccc": "dddd"}
    client.params = {"x": "aaa", "y": "bbb"}
    client.timeout = 20

    response = client.get("https://httpbin.org/anything")
    assert response.status_code == 200
    assert response.status_code == 200
    assert client.auth == ("user", "password")
    assert client.headers == {"x-test": "TesT"} # Headers are lowercased (necessary for HTTP/2)
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


@retry()
def test_client_request_get():
    client = httpr.Client()
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    response = client.request(
        "GET",
        "https://httpbin.org/anything",
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


@retry()
def test_client_get():
    client = httpr.Client()
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    response = client.get(
        "https://httpbin.org/anything",
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


@retry()
def test_client_post_content():
    client = httpr.Client()
    auth = ("user", "password")
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    content = b"test content"
    response = client.post(
        "https://httpbin.org/anything",
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


@retry()
def test_client_post_data():
    client = httpr.Client()
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    data = {"key1": "value1", "key2": "value2"}
    response = client.post(
        "https://httpbin.org/anything",
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


@retry()
def test_client_post_json():
    client = httpr.Client()
    auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb", "z": 3}
    data = {"key1": "value1", "key2": "value2"}
    response = client.post(
        "https://httpbin.org/anything",
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

@retry()
def test_client_number_params():
    client = httpr.Client()
    params = {
        "int": 42,
        "float": 3.14159,
        "sci_notation": 1.23e-4,
        "large_float": 1.7976931348623157e+308,
        "small_float": 0.026305610314011577,
    }
    response = client.get("https://httpbin.org/anything", params=params)
    assert response.status_code == 200
    json_data = response.json()
    
    # Verify all numeric values are converted to strings
    assert json_data["args"]["int"] == "42"
    assert json_data["args"]["float"] == "3.14159"
    assert json_data["args"]["sci_notation"] == "0.000123" or json_data["args"]["sci_notation"] == "1.23e-4"
    # Large values might have different string representations
    assert float(json_data["args"]["large_float"]) == 1.7976931348623157e+308
    assert float(json_data["args"]["small_float"]) == 0.026305610314011577

@retry()
def test_header_case_preservation():
    client = httpr.Client()
    
    # Send a request to a server that will return case-sensitive headers
    response = client.get("https://httpbin.org/response-headers?X-Custom-Header=TestValue")
    
    # Verify the header case is preserved
    assert "X-Custom-Header" in response.headers
    assert response.headers["X-Custom-Header"] == "TestValue"
    
    # Also verify headers can be accessed with different cases
    assert "x-custom-header" in response.headers
    assert response.headers["x-custom-header"] == "TestValue"

@pytest.fixture(scope="session")
def test_files(tmp_path_factory):
    tmp_path_factory.mktemp("data")
    temp_file1 = tmp_path_factory.mktemp("data") / "img1.png"
    with open(temp_file1, "w") as f:
        f.write("aaa111")
    temp_file2 = tmp_path_factory.mktemp("data") / "img2.png"
    with open(temp_file2, "w") as f:
        f.write("bbb222")
    return str(temp_file1), str(temp_file2)


def test_client_post_files(test_files):
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
