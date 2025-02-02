import httpr
import pytest

BASE_URL = "https://httpbin.org"


def test_get():
    r = httpr.get(f"{BASE_URL}/get")
    assert r.status_code == 200
    data = r.json()
    assert "url" in data


def test_post_form_data():
    data = {"key": "value"}
    r = httpr.post(f"{BASE_URL}/post", data=data)
    json_data = r.json()
    assert r.status_code == 200
    # httpbin returns form data as strings in the 'form' field.
    assert json_data.get("form") == {"key": "value"}


def test_post_json_data():
    data = {"key": "value"}
    r = httpr.post(f"{BASE_URL}/post", json=data)
    json_data = r.json()
    assert r.status_code == 200
    # the JSON payload is echoed in the 'json' field.
    assert json_data.get("json") == data


def test_put():
    data = {"key": "value"}
    r = httpr.put(f"{BASE_URL}/put", data=data)
    json_data = r.json()
    assert r.status_code == 200
    assert json_data.get("form") == data


def test_delete():
    r = httpr.delete(f"{BASE_URL}/delete")
    json_data = r.json()
    assert r.status_code == 200
    # httpbin echoes an empty JSON or additional data.
    assert isinstance(json_data, dict)


def test_head():
    r = httpr.head(f"{BASE_URL}/get")
    assert r.status_code == 200
    # HEAD responses should have no body.
    assert r.text == ""


def test_options():
    r = httpr.options(f"{BASE_URL}/get")
    # Options might return 200 or 204
    assert r.status_code in (200, 204)


def test_params_encoding():
    params = {"key1": "value1", "key2": ["value2", "value3"]}
    r = httpr.get(f"{BASE_URL}/get", params=params)
    json_data = r.json()
    # httpbin returns parameters in the 'args' field.
    args = json_data.get("args")
    assert args.get("key1") == "value1"
    # Verify that both values are present in the URL query string.
    url_str = str(r.url)
    assert "key2=value2" in url_str
    assert "key2=value3" in url_str


def test_custom_headers():
    headers = {"User-Agent": "my-app/0.0.1"}
    r = httpr.get(f"{BASE_URL}/headers", headers=headers)
    json_data = r.json()
    # httpbin echoes headers with capitalized keys.
    assert json_data["headers"].get("User-Agent") == "my-app/0.0.1"


def test_timeout():
    # The /delay/ endpoint enforces a delay; setting a very short timeout should raise an exception.
    with pytest.raises(httpr.TimeoutException):
        httpr.get(f"{BASE_URL}/delay/3", timeout=0.001)


def test_redirect_following():
    # Request a URL that redirects (HTTP -> HTTPS).
    r = httpr.get("http://github.com/", follow_redirects=True)
    assert r.status_code == 200
    # Ensure the final URL is HTTPS.
    assert r.url.scheme == "https"
    assert "github.com" in r.url.host


def test_streaming_response():
    with httpr.stream("GET", f"{BASE_URL}/get") as r:
        content = b""
        for chunk in r.iter_bytes():
            content += chunk
    assert b'"url":' in content
