"""Benchmarks for httpr's request path against a local payload server.

The payload server runs in a separate process (see `bench_server.py`), so the
measured region covers httpr and its Rust stack only: request building, the
reqwest/hyper client, transfer decoding and response materialisation.

These are deliberately end-to-end at the client level. Under CodSpeed's CPU
simulation instrument the syscall *wait* time is not measured, so what is left is
the CPU cost httpr itself is responsible for on every request.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

import httpr


class TestClientConstruction:
    """Client setup cost, which includes building the reqwest client and TLS config."""

    def test_default_client(self, benchmark) -> None:
        benchmark.group = "Client construction"

        def build_and_close() -> None:
            httpr.Client().close()

        benchmark(build_and_close)

    def test_client_with_options(self, benchmark) -> None:
        benchmark.group = "Client construction"
        headers = {f"X-Custom-{i}": f"value-{i}" for i in range(20)}
        params = {f"p{i}": str(i) for i in range(10)}
        cookies = {f"c{i}": f"v{i}" for i in range(10)}

        def build_and_close() -> None:
            httpr.Client(
                headers=headers,
                params=params,
                cookies=cookies,
                auth_bearer="token",
                timeout=5,
                follow_redirects=False,
                http2_only=False,
            ).close()

        benchmark(build_and_close)


class TestSyncRequests:
    """Per-request overhead for the synchronous client."""

    def test_get_session_reuse(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        """Baseline: smallest possible GET on a pooled connection."""
        url = f"{payload_server}/get"
        benchmark.group = "Sync GET"
        assert benchmark(lambda: bench_client.get(url).status_code) == 200

    def test_get_new_client_per_request(self, benchmark, payload_server: str) -> None:
        """Cost of the one-shot pattern: build a client, request, tear it down."""
        url = f"{payload_server}/get"
        benchmark.group = "Sync GET"

        def request_with_fresh_client() -> int:
            with httpr.Client() as client:
                return client.get(url).status_code

        assert benchmark(request_with_fresh_client) == 200

    def test_get_with_query_params(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        """Query-string serialisation on top of the baseline GET."""
        url = f"{payload_server}/get"
        params = {f"param{i}": f"value {i}" for i in range(20)}
        benchmark.group = "Sync GET"
        assert benchmark(lambda: bench_client.get(url, params=params).status_code) == 200

    def test_get_with_request_headers(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        """Per-request header map construction on top of the baseline GET."""
        url = f"{payload_server}/get"
        headers = {f"X-Request-Header-{i}": f"value-{i}" for i in range(20)}
        benchmark.group = "Sync GET"
        assert benchmark(lambda: bench_client.get(url, headers=headers).status_code) == 200

    def test_get_large_body(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        """100 KB body: transfer plus `Response.content` materialisation."""
        url = f"{payload_server}/bytes/102400"
        benchmark.group = "Sync GET"
        assert len(benchmark(lambda: bench_client.get(url).content)) == 102400

    def test_get_redirect_chain(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        """Three 302 hops, followed by the client."""
        url = f"{payload_server}/redirect/3"
        benchmark.group = "Sync GET"
        assert benchmark(lambda: bench_client.get(url).status_code) == 200

    def test_get_with_cookie_store(self, benchmark, payload_server: str) -> None:
        """A response setting 10 cookies, stored in the client's cookie jar."""
        url = f"{payload_server}/cookies"
        with httpr.Client(cookie_store=True) as client:
            client.get(url)
            benchmark.group = "Sync GET"
            assert benchmark(lambda: client.get(url).status_code) == 200


class TestTransferDecoding:
    """Compressed response bodies, decoded by reqwest before httpr sees them."""

    @pytest.mark.parametrize("encoding", ["gzip", "deflate"])
    def test_compressed_json(self, benchmark, bench_client: httpr.Client, payload_server: str, encoding: str) -> None:
        url = f"{payload_server}/{encoding}/medium"
        benchmark.group = "Transfer decoding"
        assert len(benchmark(lambda: bench_client.get(url).content)) > 0

    def test_uncompressed_json(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        """Reference point for the compressed variants: same payload, no encoding."""
        url = f"{payload_server}/json/medium"
        benchmark.group = "Transfer decoding"
        assert len(benchmark(lambda: bench_client.get(url).content)) > 0


class TestUploads:
    """Request-body serialisation."""

    def test_post_json(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        url = f"{payload_server}/echo"
        payload = {
            "id": 42,
            "name": "benchmark",
            "values": list(range(100)),
            "nested": {"a": 1, "b": [1.5, 2.5, 3.5], "c": None},
        }
        benchmark.group = "Upload"
        assert benchmark(lambda: bench_client.post(url, json=payload).status_code) == 200

    def test_post_form_data(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        url = f"{payload_server}/echo"
        form = {f"field{i}": f"value {i}" for i in range(30)}
        benchmark.group = "Upload"
        assert benchmark(lambda: bench_client.post(url, data=form).status_code) == 200

    def test_post_raw_content(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        url = f"{payload_server}/echo"
        content = b"x" * 102400
        benchmark.group = "Upload"
        assert benchmark(lambda: bench_client.post(url, content=content).status_code) == 200

    def test_post_multipart(self, benchmark, bench_client: httpr.Client, payload_server: str, upload_file: str) -> None:
        url = f"{payload_server}/echo"
        files = {"upload": upload_file}
        benchmark.group = "Upload"
        assert benchmark(lambda: bench_client.post(url, files=files).status_code) == 200


class TestStreaming:
    """Streaming responses, chunk by chunk."""

    def test_iter_bytes(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        url = f"{payload_server}/stream/32"
        benchmark.group = "Streaming"

        def consume() -> int:
            total = 0
            with bench_client.stream("GET", url) as response:
                for chunk in response.iter_bytes():
                    total += len(chunk)
            return total

        assert benchmark(consume) > 0

    def test_iter_lines(self, benchmark, bench_client: httpr.Client, payload_server: str) -> None:
        url = f"{payload_server}/stream/32"
        benchmark.group = "Streaming"

        def consume() -> int:
            count = 0
            with bench_client.stream("GET", url) as response:
                for _line in response.iter_lines():
                    count += 1
            return count

        assert benchmark(consume) >= 0


class TestAsyncRequests:
    """AsyncClient overhead: the thread-pool dispatch on top of the sync client."""

    def test_single_request(self, benchmark, async_bench_client: httpr.AsyncClient, payload_server: str) -> None:
        """One awaited GET on a warm client: the executor round trip plus the request.

        Concurrency itself is deliberately not benchmarked here. Overlapping
        requests spend their time waiting on sockets, which the CPU simulation
        instrument does not measure; `tests/benchmark/test_performance.py` covers
        it in wall-clock terms instead.
        """
        url = f"{payload_server}/get"
        loop = asyncio.new_event_loop()
        benchmark.group = "Async"
        try:
            assert benchmark(lambda: loop.run_until_complete(async_bench_client.get(url)).status_code) == 200
        finally:
            loop.close()


@pytest.fixture(scope="session")
def upload_file(tmp_path_factory: pytest.TempPathFactory) -> str:
    """A 100 KB file on disk, for the multipart upload benchmark."""
    path: Path = tmp_path_factory.mktemp("bench-upload") / "payload.bin"
    path.write_bytes(b"y" * 102400)
    return str(path)


@pytest.fixture(scope="session")
def async_bench_client(payload_server: str):
    """A warm AsyncClient, so its executor threads exist before any measurement."""
    client = httpr.AsyncClient()
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(client.get(f"{payload_server}/get"))
        yield client
    finally:
        loop.close()
        client.close()
