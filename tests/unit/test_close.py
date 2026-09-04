"""
Tests for the client lifecycle: Client.close(), AsyncClient.aclose() and the
context managers (issue #88).

Uses a local HTTP/1.1 keep-alive server that counts its open connections so
the tests can observe pooled sockets actually being released, not just that
`close()` returned.
"""

import asyncio
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

import httpr


class _Server(ThreadingHTTPServer):
    # The default listen backlog is 5. The stress tests below open dozens of
    # connections at once; with a tiny backlog the kernel holds or drops the
    # excess SYNs until the (GIL-contended) accept thread catches up, which
    # would make the *client's* connects complete tens of milliseconds late and
    # turn those tests into a measurement of this server rather than of httpr.
    request_queue_size = 128
    daemon_threads = True


class KeepAliveServer:
    """Minimal HTTP/1.1 keep-alive server that tracks its open connections."""

    def __init__(self) -> None:
        self.open_connections = 0
        self.requests_served = 0
        self._lock = threading.Lock()
        outer = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"  # keep connections alive between requests

            def setup(self) -> None:
                super().setup()
                with outer._lock:
                    outer.open_connections += 1

            def finish(self) -> None:
                super().finish()
                with outer._lock:
                    outer.open_connections -= 1

            def do_GET(self) -> None:
                # /delay/<seconds> lets a test hold a request in flight.
                if self.path.startswith("/delay/"):
                    time.sleep(float(self.path.rsplit("/", 1)[-1]))
                body = b"ok"
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(body)
                with outer._lock:
                    outer.requests_served += 1

            def log_message(self, *args) -> None:
                pass

        self._server = _Server(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}"

    def wait_for_open_connections(self, expected: int, timeout: float = 5.0) -> bool:
        """Poll until the server sees `expected` open connections, or time out."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._lock:
                if self.open_connections == expected:
                    return True
            time.sleep(0.005)
        with self._lock:
            return self.open_connections == expected

    def shutdown(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)


@pytest.fixture
def server():
    srv = KeepAliveServer()
    yield srv
    srv.shutdown()


# =============================================================================
# Client (sync)
# =============================================================================


def test_close_releases_pooled_connections(server):
    client = httpr.Client()
    assert client.get(server.url).status_code == 200
    assert server.wait_for_open_connections(1), "request should leave a pooled connection"

    client.close()

    assert server.wait_for_open_connections(0), "close() must release the pooled connection"


def test_context_manager_exit_releases_pooled_connections(server):
    with httpr.Client() as client:
        assert client.get(server.url).status_code == 200
        assert server.wait_for_open_connections(1)

    assert client.is_closed
    assert server.wait_for_open_connections(0), "__exit__ must release the pooled connection"


def test_request_after_close_raises_client_closed(server):
    client = httpr.Client()
    client.get(server.url)
    client.close()

    with pytest.raises(httpr.ClientClosed, match="client has been closed"):
        client.get(server.url)
    with pytest.raises(httpr.ClientClosed):
        client.request("GET", server.url)
    with pytest.raises(httpr.ClientClosed):
        with client.stream("GET", server.url):
            pass

    # Nothing reached the server.
    assert server.requests_served == 1


def test_client_closed_is_a_runtime_error(server):
    """httpx raises RuntimeError on use-after-close; code written for it keeps working."""
    client = httpr.Client()
    client.close()
    with pytest.raises(RuntimeError):
        client.get(server.url)


def test_close_is_idempotent(server):
    client = httpr.Client()
    client.get(server.url)
    client.close()
    client.close()
    with httpr.Client() as other:
        other.close()  # explicit close inside the block; __exit__ closes again
    assert client.is_closed and other.is_closed


def test_is_closed_property():
    client = httpr.Client()
    assert client.is_closed is False
    client.close()
    assert client.is_closed is True


def test_close_never_used_client():
    client = httpr.Client()
    client.close()
    assert client.is_closed


def test_proxy_setter_after_close_raises():
    client = httpr.Client()
    client.close()
    with pytest.raises(httpr.ClientClosed):
        client.proxy = "http://127.0.0.1:1"


def test_headers_still_readable_after_close():
    client = httpr.Client(headers={"X-Test": "1"})
    client.close()
    assert client.headers["x-test"] == "1"


def test_in_flight_request_completes_when_client_is_closed(server):
    """A request already running keeps its handle to the pool; close() must not break it."""
    client = httpr.Client()
    result: dict = {}

    def slow_request():
        try:
            result["status"] = client.get(f"{server.url}/delay/0.5").status_code
        except Exception as exc:  # pragma: no cover - failure path
            result["error"] = exc

    thread = threading.Thread(target=slow_request)
    thread.start()
    assert server.wait_for_open_connections(1)
    client.close()
    assert client.is_closed
    thread.join(timeout=10)

    assert result == {"status": 200}
    assert server.wait_for_open_connections(0)


def test_module_level_helpers_release_their_temporary_client(server):
    assert httpr.get(server.url).status_code == 200
    assert server.wait_for_open_connections(0)


def test_many_clients_do_not_accumulate_connections(server):
    """The per-tenant / per-credential pattern from the issue: no slow bleed."""
    for _ in range(20):
        with httpr.Client() as client:
            client.get(server.url)
    assert server.wait_for_open_connections(0)


# =============================================================================
# AsyncClient
# =============================================================================


@pytest.mark.asyncio
async def test_aclose_releases_connections_and_shuts_down_executor(server):
    client = httpr.AsyncClient(max_concurrency=4)
    assert (await client.get(server.url)).status_code == 200
    assert server.wait_for_open_connections(1)

    await client.aclose()

    assert client.is_closed
    assert client._executor._shutdown, "aclose() must shut down the client's own thread pool"
    assert server.wait_for_open_connections(0)


@pytest.mark.asyncio
async def test_async_context_manager_exit_closes(server):
    async with httpr.AsyncClient() as client:
        await client.get(server.url)
        assert server.wait_for_open_connections(1)

    assert client.is_closed
    assert client._executor._shutdown
    assert server.wait_for_open_connections(0)


@pytest.mark.asyncio
async def test_async_request_after_aclose_raises_client_closed(server):
    client = httpr.AsyncClient()
    await client.get(server.url)
    await client.aclose()

    with pytest.raises(httpr.ClientClosed, match="client has been closed"):
        await client.get(server.url)
    with pytest.raises(httpr.ClientClosed):
        async with client.stream("GET", server.url):
            pass
    assert server.requests_served == 1


@pytest.mark.asyncio
async def test_aclose_is_idempotent():
    client = httpr.AsyncClient()
    await client.aclose()
    await client.aclose()
    assert client.is_closed


@pytest.mark.asyncio
async def test_aclose_with_shared_default_executor(server):
    """max_concurrency=None dispatches on asyncio's default executor; aclose must leave it alone."""
    client = httpr.AsyncClient(max_concurrency=None)
    await client.get(server.url)
    await client.aclose()
    assert client.is_closed
    assert client._executor is None
    # The loop's default executor still works for other callers.
    loop = asyncio.get_running_loop()
    assert await loop.run_in_executor(None, lambda: 42) == 42


@pytest.mark.asyncio
async def test_aclose_while_requests_are_in_flight(server):
    """Requests already dispatched finish; aclose() does not block the event loop on them."""
    client = httpr.AsyncClient(max_concurrency=4)
    tasks = [asyncio.create_task(client.get(f"{server.url}/delay/0.3")) for _ in range(3)]
    await asyncio.sleep(0.05)  # let them reach the executor

    started = time.monotonic()
    await client.aclose()
    assert time.monotonic() - started < 0.25, "aclose() must not wait for in-flight requests"

    responses = await asyncio.gather(*tasks)
    assert [r.status_code for r in responses] == [200, 200, 200]
    assert server.wait_for_open_connections(0)


# =============================================================================
# Connections still being established at close time
# =============================================================================
#
# When two requests overlap, hyper races a fresh connect against the idle-pool
# checkout and, if the checkout wins, finishes the connect in the background so
# the socket is not wasted. Such a connect holds the pool alive until it
# resolves, which needs I/O readiness -- so close() has to drive the runtime
# for real, not just yield. These tests stagger many overlapping requests so
# that some connects are usually still pending when the client is closed.


def _staggered_burst(client, url, workers=16, rounds=4):
    """Run `workers` threads, each doing `rounds` requests with tiny jitter."""
    import random

    def worker(seed):
        rng = random.Random(seed)
        for _ in range(rounds):
            time.sleep(rng.random() * 0.003)
            assert client.get(url).status_code == 200

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def test_close_releases_connections_that_were_still_connecting(server):
    client = httpr.Client()
    _staggered_burst(client, f"{server.url}/delay/0.005")
    client.close()
    assert server.wait_for_open_connections(0), f"{server.open_connections} sockets left open"


@pytest.mark.asyncio
async def test_aclose_releases_connections_that_were_still_connecting(server):
    import random

    client = httpr.AsyncClient(max_concurrency=64)

    async def worker(seed):
        rng = random.Random(seed)
        for _ in range(4):
            await asyncio.sleep(rng.random() * 0.003)
            assert (await client.get(f"{server.url}/delay/0.005")).status_code == 200

    await asyncio.gather(*[worker(i) for i in range(32)])
    await client.aclose()
    assert server.wait_for_open_connections(0), f"{server.open_connections} sockets left open"
