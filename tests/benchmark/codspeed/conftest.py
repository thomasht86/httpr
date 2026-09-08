"""Fixtures shared by the benchmark suite.

`payload_server` starts `bench_server.py` in a subprocess and yields its base
URL. Serving the payloads from another process keeps the server's own CPU cost
out of the measurements when the suite runs under CodSpeed's CPU simulation
instrument.

The `*_response` fixtures fetch a payload once, outside the measured region, so
the decoding benchmarks measure only httpr's decoding work.
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

import httpr

SERVER_SCRIPT = Path(__file__).with_name("bench_server.py")
STARTUP_TIMEOUT_S = 30.0


@pytest.fixture(scope="session")
def payload_server() -> Iterator[str]:
    """Base URL of the deterministic payload server (stdlib only, no network)."""
    process = subprocess.Popen(
        [sys.executable, str(SERVER_SCRIPT)],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert process.stdout is not None
        port_line = process.stdout.readline().strip()
        if not port_line:
            process.kill()
            raise RuntimeError("benchmark payload server exited before reporting its port")
        yield f"http://127.0.0.1:{int(port_line)}"
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        if process.stdout is not None:
            process.stdout.close()


@pytest.fixture(scope="session")
def bench_client(payload_server: str) -> Iterator[httpr.Client]:
    """A single warm client, so connection setup is not part of any measurement."""
    with httpr.Client() as client:
        client.get(f"{payload_server}/get")
        yield client


def _fetch(client: httpr.Client, url: str) -> httpr.Response:
    response = client.get(url)
    assert response.status_code == 200
    return response


@pytest.fixture(scope="session")
def json_responses(bench_client: httpr.Client, payload_server: str) -> dict[str, httpr.Response]:
    """JSON responses of each payload size, already fetched."""
    return {size: _fetch(bench_client, f"{payload_server}/json/{size}") for size in ("small", "medium", "large")}


@pytest.fixture(scope="session")
def cbor_responses(bench_client: httpr.Client, payload_server: str) -> dict[str, httpr.Response]:
    """CBOR responses of each payload size, already fetched."""
    return {size: _fetch(bench_client, f"{payload_server}/cbor/{size}") for size in ("small", "medium", "large")}


@pytest.fixture(scope="session")
def text_responses(bench_client: httpr.Client, payload_server: str) -> dict[str, httpr.Response]:
    """Text responses covering the ASCII, utf-8, latin-1 and sniffed-charset paths."""
    paths = {
        "ascii": "/text/large",
        "utf8": "/text-utf8/large",
        "latin1": "/text-latin1/large",
        "nocharset": "/text-nocharset/large",
    }
    responses = {name: _fetch(bench_client, f"{payload_server}{path}") for name, path in paths.items()}
    for response in responses.values():
        # httpr caches the resolved encoding on first access. Resolve it here so
        # every measured iteration decodes with a warm encoding.
        _ = response.encoding
    return responses


@pytest.fixture(scope="session")
def html_response(bench_client: httpr.Client, payload_server: str) -> httpr.Response:
    """An HTML page, for the html2text conversion benchmarks."""
    return _fetch(bench_client, f"{payload_server}/html")


@pytest.fixture(scope="session")
def headers_response(bench_client: httpr.Client, payload_server: str) -> httpr.Response:
    """A response carrying 30 custom headers, for the header-map benchmarks."""
    return _fetch(bench_client, f"{payload_server}/headers")
