"""Request timeouts (issue #81).

The documented default of 30 seconds must actually be applied, and the timeout
must bound how long the server may stall (headers, then each body chunk), not
how long a request may take in total, so a stream that keeps delivering data is
never cut off.

The tests run against a local server whose handlers stall on purpose; every
stalled handler waits on an event the fixture sets at teardown, so nothing
lingers.
"""

from __future__ import annotations

import inspect
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

import httpr

pytestmark = pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")

STALL_LIMIT = 10.0  # upper bound on any deliberate stall, in seconds


class SlowServer:
    """Local HTTP/1.1 server with endpoints that delay in controlled ways.

    /delay/<s>        sleep <s> seconds, then send a complete 200 response
    /stall-body       send the headers and one chunk, then stall
    /trickle/<n>/<s>  send <n> chunks <s> seconds apart, then finish
    """

    def __init__(self) -> None:
        self.stop = threading.Event()
        stop = self.stop

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *_args) -> None:  # keep pytest output quiet
                pass

            def _chunk(self, data: bytes) -> None:
                self.wfile.write(f"{len(data):x}\r\n".encode() + data + b"\r\n")
                self.wfile.flush()

            def do_GET(self) -> None:  # noqa: N802
                parts = self.path.strip("/").split("/")
                try:
                    if parts[0] == "delay":
                        if stop.wait(float(parts[1])):
                            return
                        body = b"slow but fine"
                        self.send_response(200)
                        self.send_header("Content-Length", str(len(body)))
                        self.end_headers()
                        self.wfile.write(body)
                    elif parts[0] == "stall-body":
                        self.send_response(200)
                        self.send_header("Transfer-Encoding", "chunked")
                        self.end_headers()
                        self._chunk(b"first")
                        stop.wait(STALL_LIMIT)
                    elif parts[0] == "trickle":
                        count, gap = int(parts[1]), float(parts[2])
                        self.send_response(200)
                        self.send_header("Transfer-Encoding", "chunked")
                        self.end_headers()
                        for i in range(count):
                            if i and stop.wait(gap):
                                return
                            self._chunk(f"chunk{i}\n".encode())
                        self.wfile.write(b"0\r\n\r\n")
                        self.wfile.flush()
                    else:
                        self.send_response(404)
                        self.send_header("Content-Length", "0")
                        self.end_headers()
                except (BrokenPipeError, ConnectionResetError):
                    pass  # the client gave up (timed out) and hung up first

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def close(self) -> None:
        self.stop.set()
        self.server.shutdown()
        self.server.server_close()


@pytest.fixture
def slow():
    server = SlowServer()
    yield server
    server.close()


# --- defaults -------------------------------------------------------------


def test_default_timeout_is_30_seconds():
    assert httpr.Client().timeout == 30.0
    assert httpr.AsyncClient().timeout == 30.0


def test_explicit_timeout_is_kept():
    assert httpr.Client(timeout=5).timeout == 5.0
    assert httpr.Client(timeout=None).timeout is None


def test_negative_timeout_is_rejected(slow):
    with pytest.raises(ValueError, match="non-negative"):
        httpr.Client(timeout=-1)
    client = httpr.Client()
    client.timeout = -1
    with pytest.raises(ValueError, match="non-negative"):
        client.get(f"{slow.url}/delay/0")
    with pytest.raises(ValueError, match="non-negative"):
        httpr.Client().get(f"{slow.url}/delay/0", timeout=float("nan"))


def test_python_signature_matches_rust_defaults():
    """`Client.__init__` only documents the parameters; PyO3's `RClient.__new__`
    applies them. Their defaults must agree or the docs lie (issue #81)."""
    documented = inspect.signature(httpr.Client.__init__).parameters
    applied = inspect.signature(httpr.RClient).parameters
    assert set(documented) - {"self"} == set(applied)
    for name, param in applied.items():
        assert documented[name].default == param.default, name


# --- the timeout is applied -----------------------------------------------


def test_timeout_waiting_for_headers(slow):
    client = httpr.Client(timeout=0.3)
    start = time.monotonic()
    with pytest.raises(httpr.ReadTimeout, match="response headers"):
        client.get(f"{slow.url}/delay/{STALL_LIMIT}")
    assert time.monotonic() - start < STALL_LIMIT / 2


def test_timeout_waiting_for_body(slow):
    client = httpr.Client(timeout=0.3)
    start = time.monotonic()
    with pytest.raises(httpr.ReadTimeout, match="body"):
        client.get(f"{slow.url}/stall-body")
    assert time.monotonic() - start < STALL_LIMIT / 2


def test_timeout_is_a_timeout_exception(slow):
    with pytest.raises(httpr.TimeoutException):
        httpr.Client(timeout=0.3).get(f"{slow.url}/delay/{STALL_LIMIT}")


def test_per_request_timeout_overrides_client(slow):
    client = httpr.Client(timeout=None)
    with pytest.raises(httpr.ReadTimeout):
        client.get(f"{slow.url}/delay/{STALL_LIMIT}", timeout=0.3)


def test_none_disables_the_timeout(slow):
    response = httpr.Client(timeout=None).get(f"{slow.url}/delay/0.5")
    assert response.status_code == 200
    assert response.text == "slow but fine"


def test_timeout_setter_takes_effect(slow):
    """Assigning `client.timeout` changes what the next request waits for,
    in both directions, without rebuilding the client."""
    client = httpr.Client(timeout=0.2)
    with pytest.raises(httpr.ReadTimeout):
        client.get(f"{slow.url}/delay/0.6")
    client.timeout = None
    assert client.get(f"{slow.url}/delay/0.6").status_code == 200
    client.timeout = 0.2
    with pytest.raises(httpr.ReadTimeout):
        client.get(f"{slow.url}/delay/0.6")


def test_timeout_survives_proxy_rebuild(slow):
    client = httpr.Client(timeout=0.2)
    client.proxy = None  # rebuilds the reqwest client
    with pytest.raises(httpr.ReadTimeout):
        client.get(f"{slow.url}/delay/0.6")


# --- the timeout is per chunk, not total ---------------------------------


def test_slow_stream_is_not_cut_off(slow):
    """Five chunks 0.3 s apart take 1.2 s in total, longer than the 0.5 s
    timeout, but no single wait exceeds it."""
    client = httpr.Client(timeout=0.5)
    with client.stream("GET", f"{slow.url}/trickle/5/0.3") as response:
        chunks = list(response.iter_bytes())
    assert b"".join(chunks) == b"".join(f"chunk{i}\n".encode() for i in range(5))


def test_slow_buffered_body_is_not_cut_off(slow):
    client = httpr.Client(timeout=0.5)
    response = client.get(f"{slow.url}/trickle/5/0.3")
    assert response.text == "".join(f"chunk{i}\n" for i in range(5))


def test_stalled_stream_times_out(slow):
    client = httpr.Client(timeout=0.3)
    with client.stream("GET", f"{slow.url}/stall-body") as response:
        it = response.iter_bytes()
        assert next(it) == b"first"
        start = time.monotonic()
        with pytest.raises(httpr.ReadTimeout):
            next(it)
        assert time.monotonic() - start < STALL_LIMIT / 2


def test_stalled_iter_text_times_out(slow):
    client = httpr.Client(timeout=0.3)
    with client.stream("GET", f"{slow.url}/stall-body") as response:
        it = response.iter_text()
        assert next(it) == "first"
        with pytest.raises(httpr.ReadTimeout):
            next(it)


def test_stalled_iter_lines_times_out(slow):
    # "first" has no newline, so the line iterator is still waiting for the
    # rest of the line when the server stalls.
    client = httpr.Client(timeout=0.3)
    with client.stream("GET", f"{slow.url}/stall-body") as response:
        with pytest.raises(httpr.ReadTimeout):
            next(response.iter_lines())


def test_stalled_stream_read_times_out(slow):
    client = httpr.Client(timeout=0.3)
    with client.stream("GET", f"{slow.url}/stall-body") as response:
        with pytest.raises(httpr.ReadTimeout):
            response.read()


@pytest.mark.asyncio
async def test_async_slow_stream_is_not_cut_off(slow):
    async with httpr.AsyncClient(timeout=0.5) as client:
        async with client.stream("GET", f"{slow.url}/trickle/5/0.3") as response:
            lines = [line async for line in response.aiter_lines()]
    assert lines == [f"chunk{i}\n" for i in range(5)]


@pytest.mark.asyncio
async def test_async_timeout_waiting_for_headers(slow):
    async with httpr.AsyncClient(timeout=0.3) as client:
        with pytest.raises(httpr.ReadTimeout):
            await client.get(f"{slow.url}/delay/{STALL_LIMIT}")
