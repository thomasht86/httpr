"""Performance benchmarks for httpr using pytest-benchmark.

These benchmarks track httpr's performance over time to detect regressions.
Results are published to GitHub Pages via github-action-benchmark.
"""

import asyncio
import random

import cbor2
import pytest

import httpr


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

        async def run():
            async with httpr.AsyncClient() as client:
                # Warmup and then benchmark a single request
                await client.get(f"{base_url}/get")
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


# Pre-generate CBOR test data (similar to benchmark/benchmark_cbor.py)
# Each payload is a list of arrays containing 1024 random floats
random.seed(42)  # Reproducible data
CBOR_PAYLOADS = {
    1: cbor2.dumps([[random.random() for _ in range(1024)] for _ in range(1)]),
    10: cbor2.dumps([[random.random() for _ in range(1024)] for _ in range(10)]),
    100: cbor2.dumps([[random.random() for _ in range(1024)] for _ in range(100)]),
}


class TestCBORDecoding:
    """Benchmark CBOR decoding performance.

    Tests httpr's CBOR decoding against different payload sizes.
    Mirrors the benchmark/benchmark_cbor.py scenarios.
    """

    @pytest.mark.parametrize(
        "count",
        [1, 10, 100],
        ids=["1_array", "10_arrays", "100_arrays"],
    )
    def test_cbor_decode(self, benchmark, count):
        """Benchmark CBOR decoding for different payload sizes."""
        data = CBOR_PAYLOADS[count]

        def decode():
            return cbor2.loads(data)

        benchmark.group = f"CBOR Decode ({count} arrays)"
        benchmark(decode)
