"""CPU-bound benchmarks for httpr's response decoding paths.

Every benchmark here operates on a response that was fetched once during fixture
setup, so no socket work happens inside the measured region. That makes them a
good fit for CodSpeed's CPU simulation instrument: the instruction count maps
directly onto the Rust decoding code (`serde_json`, `serde_cbor`, `encoding_rs`,
`html2text`) and the pyo3 conversion layer.
"""

from __future__ import annotations

import pytest

import httpr

SIZES = ["small", "medium", "large"]


@pytest.mark.parametrize("size", SIZES)
def test_json_decode(benchmark, json_responses: dict[str, httpr.Response], size: str) -> None:
    """`Response.json()`: serde_json parse plus pythonize conversion."""
    response = json_responses[size]
    benchmark.group = f"JSON decode ({size})"
    result = benchmark(lambda: response.json())
    assert isinstance(result, list)


@pytest.mark.parametrize("size", SIZES)
def test_cbor_decode(benchmark, cbor_responses: dict[str, httpr.Response], size: str) -> None:
    """`Response.cbor()`: serde_cbor parse plus pythonize conversion."""
    response = cbor_responses[size]
    benchmark.group = f"CBOR decode ({size})"
    result = benchmark(lambda: response.cbor())
    assert isinstance(result, list)


@pytest.mark.parametrize("charset", ["ascii", "utf8", "latin1"])
def test_text_decode(benchmark, text_responses: dict[str, httpr.Response], charset: str) -> None:
    """`Response.text` for a ~200 KB body: encoding_rs decode to a Python str."""
    response = text_responses[charset]
    benchmark.group = f"Text decode ({charset})"
    result = benchmark(lambda: response.text)
    assert result


def test_text_encoding_sniffing(benchmark, text_responses: dict[str, httpr.Response]) -> None:
    """Decoding a body whose charset is declared nowhere, so it has to be sniffed."""
    response = text_responses["nocharset"]

    def decode_without_cached_encoding() -> str:
        response.encoding = ""  # drop the cached encoding to force a fresh sniff
        return response.text

    benchmark.group = "Text decode (sniffed)"
    result = benchmark(decode_without_cached_encoding)
    assert result


def test_html_to_plaintext(benchmark, html_response: httpr.Response) -> None:
    """`Response.text_plain`: html2text with the trivial decorator."""
    benchmark.group = "HTML conversion"
    result = benchmark(lambda: html_response.text_plain)
    assert result


def test_html_to_markdown(benchmark, html_response: httpr.Response) -> None:
    """`Response.text_markdown`: html2text with markdown output."""
    benchmark.group = "HTML conversion"
    result = benchmark(lambda: html_response.text_markdown)
    assert result


def test_html_to_rich(benchmark, html_response: httpr.Response) -> None:
    """`Response.text_rich`: html2text with the rich (terminal) decorator."""
    benchmark.group = "HTML conversion"
    result = benchmark(lambda: html_response.text_rich)
    assert result


class TestHeaderMap:
    """`CaseInsensitiveHeaderMap` over a response carrying 30 custom headers.

    A single lookup is a few hundred nanoseconds, which is too small to track on
    its own, so each benchmark walks the whole header set once.
    """

    N_HEADERS = 30

    def test_lookup_hits(self, benchmark, headers_response: httpr.Response) -> None:
        headers = headers_response.headers
        # Mixed case on purpose: lookups have to go through the lowercase index.
        names = [f"X-RESPONSE-header-{i}" for i in range(self.N_HEADERS)]
        benchmark.group = "Header map"

        def lookup_all() -> int:
            return sum(len(headers[name]) for name in names)

        assert benchmark(lookup_all) > 0

    def test_lookup_misses(self, benchmark, headers_response: httpr.Response) -> None:
        headers = headers_response.headers
        names = [f"X-Absent-Header-{i}" for i in range(self.N_HEADERS)]
        benchmark.group = "Header map"

        def get_all_with_default() -> int:
            return sum(len(headers.get(name, "fallback")) for name in names)

        assert benchmark(get_all_with_default) > 0

    def test_items(self, benchmark, headers_response: httpr.Response) -> None:
        """Materialising every header as Python tuples."""
        headers = headers_response.headers
        benchmark.group = "Header map"
        assert len(benchmark(lambda: headers.items())) > self.N_HEADERS
