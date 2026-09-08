"""Deterministic payload server for the benchmark suite.

The server is started as a *subprocess* by the `payload_server` fixture rather
than in a background thread. That matters when the benchmarks run under
CodSpeed's CPU simulation instrument: only the benchmarked process is
instrumented, so keeping the server out of process keeps its own CPU cost out of
the measurements and leaves just httpr's request/response handling.

Every payload is generated from a fixed seed-free recipe so the byte-for-byte
content (and therefore the instruction count of decoding it) is identical on
every run.

Run standalone with:

    python tests/benchmark/bench_server.py

It binds to an ephemeral port on 127.0.0.1 and prints the port number on the
first line of stdout, then serves until terminated.
"""

from __future__ import annotations

import gzip
import json
import sys
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import cbor2

# --------------------------------------------------------------------------- #
# Payload generation
# --------------------------------------------------------------------------- #

#: Number of records in each named payload size. Roughly 200 B, 20 KB and 200 KB
#: of JSON respectively.
RECORD_COUNTS = {"small": 1, "medium": 100, "large": 1000}

_SENTENCE = "The quick brown fox jumps over the lazy dog. "


def _record(index: int) -> dict:
    """One record of a synthetic API payload: mixed types, nested object, list."""
    return {
        "id": index,
        "name": f"item-{index:06d}",
        "score": index * 1.5,
        "active": index % 2 == 0,
        "tags": ["alpha", "beta", "gamma"],
        "meta": {"created": "2024-01-01T00:00:00Z", "revision": index % 7, "note": None},
    }


def _records(size: str) -> list[dict]:
    return [_record(i) for i in range(RECORD_COUNTS[size])]


def _text(size: str) -> str:
    """ASCII-only text payload, ~200 B / ~20 KB / ~200 KB."""
    repeats = {"small": 5, "medium": 450, "large": 4500}[size]
    return _SENTENCE * repeats


def _accented_text(size: str) -> str:
    """Text with non-ASCII characters, to exercise the decoding path."""
    repeats = {"small": 5, "medium": 450, "large": 4500}[size]
    return "Chaîne accentuée à décoder — ça coûte plus cher. " * repeats


def _html() -> str:
    rows = "".join(
        f"<tr><td>{i}</td><td><a href='/item/{i}'>item {i}</a></td><td><em>{_SENTENCE}</em></td></tr>"
        for i in range(100)
    )
    items = "".join(f"<li><strong>Point {i}</strong>: {_SENTENCE}</li>" for i in range(50))
    return (
        "<!doctype html><html><head><title>Benchmark page</title></head><body>"
        f"<h1>Benchmark page</h1><p>{_SENTENCE * 5}</p>"
        f"<ul>{items}</ul>"
        f"<table>{rows}</table>"
        "</body></html>"
    )


def _build_payloads() -> dict[str, tuple[bytes, dict[str, str]]]:
    """Precompute every response body and its headers, keyed by request path."""
    payloads: dict[str, tuple[bytes, dict[str, str]]] = {
        "/get": (b'{"ok":true}', {"Content-Type": "application/json"}),
    }

    for size in RECORD_COUNTS:
        records = _records(size)
        payloads[f"/json/{size}"] = (
            json.dumps(records).encode(),
            {"Content-Type": "application/json"},
        )
        payloads[f"/cbor/{size}"] = (
            cbor2.dumps(records),
            {"Content-Type": "application/cbor"},
        )
        payloads[f"/text/{size}"] = (
            _text(size).encode(),
            {"Content-Type": "text/plain; charset=utf-8"},
        )
        # Declared charset, non-ASCII content: the fast utf-8 path.
        payloads[f"/text-utf8/{size}"] = (
            _accented_text(size).encode("utf-8"),
            {"Content-Type": "text/plain; charset=utf-8"},
        )
        # Legacy single-byte charset: forces a transcoding decode.
        payloads[f"/text-latin1/{size}"] = (
            _accented_text(size).encode("iso-8859-1", errors="replace"),
            {"Content-Type": "text/plain; charset=iso-8859-1"},
        )
        # No charset anywhere: httpr has to sniff the encoding from the body.
        payloads[f"/text-nocharset/{size}"] = (
            _accented_text(size).encode("utf-8"),
            {"Content-Type": "text/plain"},
        )

    html = _html().encode()
    payloads["/html"] = (html, {"Content-Type": "text/html; charset=utf-8"})

    json_medium = payloads["/json/medium"][0]
    payloads["/gzip/medium"] = (
        gzip.compress(json_medium),
        {"Content-Type": "application/json", "Content-Encoding": "gzip"},
    )
    payloads["/deflate/medium"] = (
        zlib.compress(json_medium),
        {"Content-Type": "application/json", "Content-Encoding": "deflate"},
    )

    for n_bytes in (1024, 102400):
        payloads[f"/bytes/{n_bytes}"] = (
            bytes(range(256)) * (n_bytes // 256),
            {"Content-Type": "application/octet-stream"},
        )

    many_headers = {f"X-Response-Header-{i}": f"value-{i}" for i in range(30)}
    many_headers["Content-Type"] = "application/json"
    payloads["/headers"] = (b'{"ok":true}', many_headers)

    return payloads


PAYLOADS = _build_payloads()

#: 10 cookies, to exercise the cookie-store code path.
COOKIES = [(f"session-{i}", f"value-{i}") for i in range(10)]


def _raw_response(status_line: bytes, headers: list[tuple[str, str]], body: bytes) -> bytes:
    """Serialise a whole response so it can go out in a single `write()`.

    Writing the head and the body separately makes Nagle's algorithm hold the
    second segment until the client ACKs the first, which adds ~40 ms of delayed
    ACK to every request on a reused connection and completely swamps the CPU
    cost we are trying to measure.
    """
    head = b"".join(f"{name}: {value}\r\n".encode() for name, value in headers)
    return status_line + b"\r\n" + head + b"\r\n" + body


def _build_raw_responses() -> dict[str, bytes]:
    """Fully serialised responses, keyed by request path."""
    raw: dict[str, bytes] = {}

    for path, (body, headers) in PAYLOADS.items():
        header_list = [*headers.items(), ("Content-Length", str(len(body)))]
        raw[path] = _raw_response(b"HTTP/1.1 200 OK", header_list, body)

    cookie_headers = [("Content-Type", "application/json")]
    cookie_headers += [("Set-Cookie", f"{name}={value}; Path=/") for name, value in COOKIES]
    cookie_headers.append(("Content-Length", "11"))
    raw["/cookies"] = _raw_response(b"HTTP/1.1 200 OK", cookie_headers, b'{"ok":true}')

    for remaining in range(1, 11):
        raw[f"/redirect/{remaining}"] = _raw_response(
            b"HTTP/1.1 302 Found",
            [("Location", f"/redirect/{remaining - 1}"), ("Content-Length", "0")],
            b"",
        )
    raw["/redirect/0"] = raw["/get"]

    chunk = (_SENTENCE * 23).encode()  # ~1 KB per chunk
    chunk_frame = b"%x\r\n" % len(chunk) + chunk + b"\r\n"
    for n_chunks in (8, 32, 128):
        raw[f"/stream/{n_chunks}"] = _raw_response(
            b"HTTP/1.1 200 OK",
            [("Content-Type", "text/plain; charset=utf-8"), ("Transfer-Encoding", "chunked")],
            chunk_frame * n_chunks + b"0\r\n\r\n",
        )

    raw["__not_found__"] = _raw_response(
        b"HTTP/1.1 404 Not Found",
        [("Content-Type", "application/json"), ("Content-Length", "21")],
        b'{"error":"not found"}',
    )
    return raw


RAW_RESPONSES = _build_raw_responses()


# --------------------------------------------------------------------------- #
# Server
# --------------------------------------------------------------------------- #


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    # Small responses must not wait on a delayed ACK from the client.
    disable_nagle_algorithm = True

    def log_message(self, fmt: str, *args: object) -> None:
        """Silence per-request logging: it would dominate the server's cost."""

    def _read_body(self) -> bytes:
        """Read the request body, honouring chunked transfer encoding.

        httpr streams multipart uploads with `Transfer-Encoding: chunked`, and
        leaving those bytes unread would desynchronise the connection.
        """
        if "chunked" in (self.headers.get("Transfer-Encoding") or "").lower():
            body = bytearray()
            while True:
                size = int(self.rfile.readline().split(b";", 1)[0] or b"0", 16)
                if size == 0:
                    self.rfile.readline()  # trailing CRLF of the terminating chunk
                    return bytes(body)
                body += self.rfile.read(size)
                self.rfile.readline()  # CRLF after the chunk data
        length = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(length) if length else b""

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        self.wfile.write(RAW_RESPONSES.get(path) or RAW_RESPONSES["__not_found__"])

    def do_POST(self) -> None:
        body = self._read_body()
        if self.path.split("?", 1)[0] == "/echo":
            content_type = self.headers.get("Content-Type") or "application/octet-stream"
            self.wfile.write(
                _raw_response(
                    b"HTTP/1.1 200 OK",
                    [("Content-Type", content_type), ("Content-Length", str(len(body)))],
                    body,
                )
            )
        else:
            self.wfile.write(RAW_RESPONSES["/get"])

    do_PUT = do_POST
    do_PATCH = do_POST


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    print(server.server_address[1], flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    sys.exit(main())
