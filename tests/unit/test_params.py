"""Query parameter, form data and cookie handling (issues #82 and #87).

Values are normalised with httpx's rules (lists repeat the key, booleans are
lowercased, None is sent empty), client-level params are merged with the
request's own, and per-request cookies join the client's in a single header.
"""

import threading
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

import httpr  # type: ignore


@contextmanager
def _echo_server() -> Iterator[str]:
    """Serves one URL that echoes the raw request body back as text/plain."""

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}/echo"
    finally:
        server.shutdown()
        server.server_close()


class TestParamNormalisation:
    def test_list_repeats_key(self, base_url_ssl, ca_bundle):
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/get", params={"tag": ["a", "b"]})
        assert response.json()["args"] == {"tag": ["a", "b"]}
        assert response.url.endswith("/get?tag=a&tag=b")

    def test_tuple_repeats_key(self, base_url_ssl, ca_bundle):
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/get", params={"n": (1, 2)})
        assert response.json()["args"] == {"n": ["1", "2"]}

    def test_bool_none_and_numbers(self, base_url_ssl, ca_bundle):
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.get(
                f"{base_url_ssl}/get",
                params={"n": 5, "f": 1.5, "yes": True, "no": False, "none": None},
            )
        assert response.json()["args"] == {"n": "5", "f": "1.5", "yes": "true", "no": "false", "none": ""}
        assert response.url.endswith("/get?n=5&f=1.5&yes=true&no=false&none=")

    def test_sequence_of_pairs(self, base_url_ssl, ca_bundle):
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/get", params=[("k", "1"), ("k", 2), ("j", True)])
        assert response.json()["args"] == {"k": ["1", "2"], "j": "true"}

    def test_empty_params_sends_no_query(self, base_url_ssl, ca_bundle):
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/get", params={})
        assert response.url.endswith("/get")

    def test_params_appended_to_inline_query(self, base_url_ssl, ca_bundle):
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/get?inline=1", params={"q": "2"})
        assert response.json()["args"] == {"inline": "1", "q": "2"}

    @pytest.mark.parametrize("bad", ["a=1", b"a=1", 5, ["not-a-pair"]])
    def test_invalid_params_raise_type_error(self, bad):
        client = httpr.Client()
        with pytest.raises(TypeError, match="params must be a mapping or a sequence"):
            client.get("https://example.invalid/", params=bad)

    def test_invalid_client_params_raise_type_error(self):
        with pytest.raises(TypeError, match="params must be a mapping"):
            httpr.Client(params="a=1")


class TestClientParams:
    def test_constructor_accepts_non_string_values(self, base_url_ssl, ca_bundle):
        with httpr.Client(params={"n": 5, "flag": True, "tag": ["a", "b"]}, ca_cert_file=ca_bundle) as client:
            assert client.params == {"n": "5", "flag": "true", "tag": ["a", "b"]}
            response = client.get(f"{base_url_ssl}/get")
        assert response.json()["args"] == {"n": "5", "flag": "true", "tag": ["a", "b"]}

    def test_getter_round_trips_through_setter(self):
        client = httpr.Client(params={"tag": ["a", "b"], "x": 1})
        snapshot = client.params
        client.params = snapshot
        assert client.params == {"tag": ["a", "b"], "x": "1"}
        client.params = None
        assert client.params is None

    def test_client_params_merged_with_request_params(self, base_url_ssl, ca_bundle):
        with httpr.Client(params={"api_key": "SECRET"}, ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/get", params={"q": "1"})
        assert response.json()["args"] == {"api_key": "SECRET", "q": "1"}
        # client params come first, then the request's own
        assert response.url.endswith("/get?api_key=SECRET&q=1")

    def test_request_param_overrides_client_param(self, base_url_ssl, ca_bundle):
        with httpr.Client(params={"v": ["1", "2"], "keep": "yes"}, ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/get", params={"v": "3"})
        # every client value for an overridden key is dropped, as in httpx
        assert response.json()["args"] == {"keep": "yes", "v": "3"}

    def test_empty_request_params_keep_client_params(self, base_url_ssl, ca_bundle):
        with httpr.Client(params={"api_key": "SECRET"}, ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/get", params={})
        assert response.json()["args"] == {"api_key": "SECRET"}

    def test_stream_merges_client_params(self, base_url_ssl, ca_bundle):
        with httpr.Client(params={"api_key": "SECRET"}, ca_cert_file=ca_bundle) as client:
            with client.stream("GET", f"{base_url_ssl}/get", params={"tag": ["a", "b"]}) as response:
                body = response.read()
        import json

        assert json.loads(body)["args"] == {"api_key": "SECRET", "tag": ["a", "b"]}


class TestFormData:
    def test_list_value_repeats_field(self, base_url_ssl, ca_bundle):
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.post(f"{base_url_ssl}/post", data={"tag": ["a", "b"], "n": 1})
        json_data = response.json()
        assert json_data["form"] == {"tag": ["a", "b"], "n": "1"}
        assert json_data["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

    def test_bool_and_none_values(self, base_url_ssl, ca_bundle):
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.post(f"{base_url_ssl}/post", data={"yes": True, "none": None})
        assert response.json()["form"] == {"yes": "true", "none": ""}

    def test_field_order_preserved(self):
        # serde_json would have alphabetised these; httpbin sorts parsed form keys,
        # so check the raw body against a local echo server instead.
        with _echo_server() as url, httpr.Client() as client:
            response = client.post(url, data={"zeta": "1", "mid": "2", "alpha": "3"})
        assert response.text == "zeta=1&mid=2&alpha=3"

    def test_invalid_data_raises_type_error(self):
        client = httpr.Client()
        with pytest.raises(TypeError, match="data must be a mapping or a sequence"):
            client.post("https://example.invalid/", data="raw string")


class TestCookies:
    def test_request_cookies_merged_into_single_header(self, base_url_ssl, ca_bundle):
        with httpr.Client(cookies={"session": "abc"}, ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/headers", cookies={"tracking": "t1"})
        assert response.json()["headers"]["Cookie"] == "session=abc; tracking=t1"

    def test_request_cookie_overrides_client_cookie(self, base_url_ssl, ca_bundle):
        with httpr.Client(cookies={"session": "abc", "keep": "1"}, ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/headers", cookies={"session": "xyz"})
        assert response.json()["headers"]["Cookie"] == "session=xyz; keep=1"

    def test_request_cookies_without_client_cookies(self, base_url_ssl, ca_bundle):
        with httpr.Client(ca_cert_file=ca_bundle) as client:
            response = client.get(f"{base_url_ssl}/headers", cookies={"only": "me"})
        assert response.json()["headers"]["Cookie"] == "only=me"

    def test_client_cookies_untouched_by_request_cookies(self, base_url_ssl, ca_bundle):
        with httpr.Client(cookies={"session": "abc"}, ca_cert_file=ca_bundle) as client:
            client.get(f"{base_url_ssl}/headers", cookies={"tracking": "t1"})
            assert client.cookies == {"session": "abc"}
            response = client.get(f"{base_url_ssl}/headers")
        assert response.json()["headers"]["Cookie"] == "session=abc"

    def test_stream_merges_cookies(self, base_url_ssl, ca_bundle):
        import json

        with httpr.Client(cookies={"session": "abc"}, ca_cert_file=ca_bundle) as client:
            with client.stream("GET", f"{base_url_ssl}/headers", cookies={"tracking": "t1"}) as response:
                body = response.read()
        assert json.loads(body)["headers"]["Cookie"] == "session=abc; tracking=t1"


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_async_params_merge_and_normalise(self, base_url_ssl, ca_bundle):
        async with httpr.AsyncClient(params={"api_key": "SECRET"}, ca_cert_file=ca_bundle) as client:
            response = await client.get(f"{base_url_ssl}/get", params={"tag": ["a", "b"], "flag": False})
        assert response.json()["args"] == {"api_key": "SECRET", "tag": ["a", "b"], "flag": "false"}

    @pytest.mark.asyncio
    async def test_async_cookies_merge(self, base_url_ssl, ca_bundle):
        async with httpr.AsyncClient(cookies={"session": "abc"}, ca_cert_file=ca_bundle) as client:
            response = await client.get(f"{base_url_ssl}/headers", cookies={"tracking": "t1"})
        assert response.json()["headers"]["Cookie"] == "session=abc; tracking=t1"

    @pytest.mark.asyncio
    async def test_async_stream_params(self, base_url_ssl, ca_bundle):
        import json

        async with httpr.AsyncClient(params={"a": 1}, ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/get", params={"b": [2, 3]}) as response:
                body = response.read()
        assert json.loads(body)["args"] == {"a": "1", "b": ["2", "3"]}
