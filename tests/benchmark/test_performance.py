"""Performance benchmarks for httpr using pytest-benchmark.

These benchmarks track httpr's performance over time to detect regressions.
Results are published to GitHub Pages via github-action-benchmark.
"""

import asyncio
import os

import pytest

import httpr


@pytest.fixture
def bench_server_url():
    """URL for the benchmark server (benchmark/server.py).

    Set BENCHMARK_SERVER_URL env var to enable CBOR benchmarks.
    The server provides /cbor/1, /cbor/10, /cbor/100 endpoints.
    """
    url = os.environ.get("BENCHMARK_SERVER_URL")
    if not url:
        pytest.skip("BENCHMARK_SERVER_URL not set - start benchmark server for CBOR tests")
    return url


class TestSyncClient:
    """Benchmark synchronous client operations."""

    def test_single_request(self, benchmark, base_url):
        """Benchmark single GET request without session reuse."""

        def make_request():
            with httpr.Client() as client:
                return client.get(f"{base_url}/get").text

        benchmark(make_request)

    def test_session_reuse(self, benchmark, base_url):
        """Benchmark GET request with session reuse."""
        with httpr.Client() as client:

            def make_request():
                return client.get(f"{base_url}/get").text

            benchmark(make_request)

    def test_json_parsing(self, benchmark, base_url):
        """Benchmark JSON response parsing."""
        with httpr.Client() as client:

            def parse_json():
                return client.get(f"{base_url}/json").json()

            benchmark(parse_json)

    def test_post_json(self, benchmark, base_url):
        """Benchmark POST request with JSON body."""
        payload = {"key": "value", "number": 42, "nested": {"a": 1, "b": 2}}
        with httpr.Client() as client:

            def post_json():
                return client.post(f"{base_url}/post", json=payload).json()

            benchmark(post_json)


class TestAsyncClient:
    """Benchmark async client operations."""

    def test_single_request(self, benchmark, base_url):
        """Benchmark single async GET request."""

        async def run():
            async with httpr.AsyncClient() as client:
                return await client.get(f"{base_url}/get")

        benchmark(lambda: asyncio.run(run()))

    def test_session_reuse(self, benchmark, base_url):
        """Benchmark async GET request with session reuse."""
        # Note: Each iteration creates a new event loop + client due to asyncio.run()
        # This measures the full async overhead, not just the request time
        async def run():
            async with httpr.AsyncClient() as client:
                return await client.get(f"{base_url}/get")

        benchmark(lambda: asyncio.run(run()))


class TestResponseSizes:
    """Benchmark different response payload sizes."""

    @pytest.mark.parametrize(
        "size,name",
        [
            (1024, "1KB"),
            (10240, "10KB"),
            (102400, "100KB"),
        ],
        ids=["1KB", "10KB", "100KB"],
    )
    def test_response_size(self, benchmark, base_url, size, name):
        """Benchmark response handling for different sizes."""
        with httpr.Client() as client:

            def fetch():
                return client.get(f"{base_url}/bytes/{size}").content

            benchmark.group = f"Response Size ({name})"
            benchmark(fetch)


class TestHeaders:
    """Benchmark header handling."""

    def test_many_headers(self, benchmark, base_url):
        """Benchmark request with many custom headers."""
        headers = {f"X-Custom-Header-{i}": f"value-{i}" for i in range(20)}
        with httpr.Client(headers=headers) as client:

            def make_request():
                return client.get(f"{base_url}/headers").json()

            benchmark(make_request)


class TestCBORDecoding:
    """Benchmark httpr's CBOR decoding performance.

    Tests the full request -> response -> .cbor() pipeline.
    Requires the benchmark server (benchmark/server.py) to be running.
    """

    @pytest.mark.parametrize(
        "count",
        [1, 10, 100],
        ids=["1_array", "10_arrays", "100_arrays"],
    )
    def test_cbor_request(self, benchmark, bench_server_url, count):
        """Benchmark httpr CBOR request and decoding for different payload sizes."""
        with httpr.Client() as client:

            def fetch_and_decode():
                response = client.get(f"{bench_server_url}/cbor/{count}")
                return response.cbor()

            benchmark.group = f"CBOR Request ({count} arrays)"
            benchmark(fetch_and_decode)

    @pytest.mark.parametrize(
        "count",
        [1, 10, 100],
        ids=["1_array", "10_arrays", "100_arrays"],
    )
    def test_json_request(self, benchmark, bench_server_url, count):
        """Benchmark httpr JSON request and decoding for comparison with CBOR."""
        with httpr.Client() as client:

            def fetch_and_decode():
                response = client.get(f"{bench_server_url}/json/{count}")
                return response.json()

            benchmark.group = f"JSON Request ({count} arrays)"
            benchmark(fetch_and_decode)
