"""Tests for streaming response functionality."""

import asyncio
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import pytest

import httpr  # type: ignore


class _DripHandler(BaseHTTPRequestHandler):
    """Serves ``/drip?chunks=N&pause=S`` as N chunks with S seconds between them.

    ``/sse?events=N&pause=S`` sends N ``data: <i>`` events, each followed by a
    blank line, as text/event-stream. Chunks are flushed one at a time so the
    client really receives them spread out in time.
    """

    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # silence the default stderr logging
        pass

    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        count = int(query.get("chunks", query.get("events", ["10"]))[0])
        pause = float(query.get("pause", ["0.05"])[0])
        sse = url.path == "/sse"
        payload = [f"data: {i}\n\n".encode() if sse else f"chunk-{i}\n".encode() for i in range(count)]
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream" if sse else "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(sum(len(c) for c in payload)))
        self.end_headers()
        for chunk in payload:
            self.wfile.write(chunk)
            self.wfile.flush()
            time.sleep(pause)


@pytest.fixture(scope="module")
def drip_url():
    """Base URL of a multi-threaded server that trickles out responses over time."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _DripHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()


async def _heartbeat(stop: asyncio.Event, interval: float = 0.01) -> int:
    """Count how many times the event loop got to run while ``stop`` is unset."""
    ticks = 0
    while not stop.is_set():
        await asyncio.sleep(interval)
        ticks += 1
    return ticks


class TestStreamingClient:
    """Test streaming functionality with sync Client."""

    def test_stream_iter_bytes(self, base_url_ssl, ca_bundle):
        """Test iterating over response as bytes chunks."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        # Use /get endpoint which returns JSON
        with client.stream("GET", f"{base_url_ssl}/get") as response:
            assert response.status_code == 200
            chunks = list(response.iter_bytes())
            total_bytes = b"".join(chunks)
            assert len(total_bytes) > 0
            assert b"headers" in total_bytes  # JSON response contains 'headers'

    def test_stream_direct_iteration(self, base_url_ssl, ca_bundle):
        """Test iterating directly over StreamingResponse."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/html") as response:
            assert response.status_code == 200
            chunks = list(response)
            total_bytes = b"".join(chunks)
            assert len(total_bytes) > 0
            assert b"html" in total_bytes.lower()

    def test_stream_iter_text(self, base_url_ssl, ca_bundle):
        """Test iterating over response as text chunks."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        # Use /html endpoint which returns HTML text
        with client.stream("GET", f"{base_url_ssl}/html") as response:
            assert response.status_code == 200
            chunks = list(response.iter_text())
            full_text = "".join(chunks)
            # Should contain HTML data
            assert len(full_text) > 0
            assert "html" in full_text.lower()

    def test_stream_iter_lines(self, base_url_ssl, ca_bundle):
        """Test iterating over response line by line."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        # /robots.txt returns multiple lines
        with client.stream("GET", f"{base_url_ssl}/robots.txt") as response:
            assert response.status_code == 200
            lines = list(response.iter_lines())
            # Should have multiple lines
            assert len(lines) >= 1

    def test_stream_read_all(self, base_url_ssl, ca_bundle):
        """Test reading entire response body at once."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/get") as response:
            assert response.status_code == 200
            content = response.read()
            assert len(content) > 0
            assert b"headers" in content

    def test_stream_conditional_read(self, base_url_ssl, ca_bundle):
        """Test conditional reading based on status code."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/status/200") as response:
            if response.status_code == 200:
                # Just close without reading - should work fine
                pass
            else:
                _ = response.read()

    def test_stream_headers_available(self, base_url_ssl, ca_bundle):
        """Test that headers are available before iteration."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/response-headers?X-Test=test-value") as response:
            # Headers should be available immediately
            assert "content-type" in response.headers or "Content-Type" in response.headers
            assert response.status_code == 200

    def test_stream_cookies_available(self, base_url_ssl, ca_bundle):
        """Test that cookies are available before iteration."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/cookies/set/test_cookie/test_value") as response:
            # Note: cookies might be in response.cookies depending on redirect behavior
            assert response.status_code == 200

    def test_stream_url_available(self, base_url_ssl, ca_bundle):
        """Test that URL is available."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/get") as response:
            assert response.url.endswith("/get")
            assert response.status_code == 200

    def test_stream_is_closed(self, base_url_ssl, ca_bundle):
        """Test is_closed property."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/get") as response:
            assert response.is_closed is False

        # After context manager exits, should be closed
        assert response.is_closed is True

    def test_stream_is_consumed(self, base_url_ssl, ca_bundle):
        """Test is_consumed property."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/get") as response:
            assert response.is_consumed is False
            # Consume the stream
            _ = list(response)
            assert response.is_consumed is True

    def test_stream_close_stops_iteration(self, base_url_ssl, ca_bundle):
        """Test that closing the stream stops further iteration."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/html") as response:
            # Read one chunk
            chunk = next(iter(response))
            assert len(chunk) > 0
            # Close explicitly
            response.close()
            # Should raise StreamClosed on next iteration
            with pytest.raises(httpr.StreamClosed):
                next(iter(response))

    def test_stream_consumed_error(self, base_url_ssl, ca_bundle):
        """Test that iterating consumed stream raises StreamConsumed."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/get") as response:
            # Consume the stream
            _ = list(response)
            # Try to iterate again - should raise StreamConsumed
            with pytest.raises(httpr.StreamConsumed):
                next(iter(response))

    def test_stream_with_params(self, base_url_ssl, ca_bundle):
        """Test streaming with query parameters."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/get", params={"key": "value"}) as response:
            assert response.status_code == 200
            content = response.read()
            assert b"key" in content

    def test_stream_with_headers(self, base_url_ssl, ca_bundle):
        """Test streaming with custom headers."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("GET", f"{base_url_ssl}/headers", headers={"X-Custom-Header": "custom-value"}) as response:
            assert response.status_code == 200
            content = response.read()
            assert b"X-Custom-Header" in content

    def test_stream_post_with_json(self, base_url_ssl, ca_bundle):
        """Test streaming POST request with JSON body."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with client.stream("POST", f"{base_url_ssl}/post", json={"test": "data"}) as response:
            assert response.status_code == 200
            content = response.read()
            assert b"test" in content

    def test_stream_invalid_method(self, base_url_ssl, ca_bundle):
        """Test that invalid HTTP method raises ValueError."""
        client = httpr.Client(ca_cert_file=ca_bundle)

        with pytest.raises(ValueError, match="Unsupported HTTP method"):
            with client.stream("INVALID", f"{base_url_ssl}/get") as _:  # type: ignore[arg-type]
                pass


@pytest.mark.asyncio
class TestStreamingAsyncClient:
    """Test streaming functionality with async AsyncClient."""

    async def test_async_stream_aiter_bytes(self, base_url_ssl, ca_bundle):
        """Test async iterating over response as bytes chunks."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/get") as response:
                assert isinstance(response, httpr.AsyncStreamingResponse)
                assert response.status_code == 200
                chunks = [chunk async for chunk in response.aiter_bytes()]
                assert all(isinstance(chunk, bytes) for chunk in chunks)
                assert len(b"".join(chunks)) > 0
                assert response.is_consumed

    async def test_async_stream_direct_async_iteration(self, base_url_ssl, ca_bundle):
        """``async for chunk in response`` is the same as ``aiter_bytes()``."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/html") as response:
                chunks = [chunk async for chunk in response]
                assert len(b"".join(chunks)) > 0

    async def test_async_stream_aiter_text(self, base_url_ssl, ca_bundle):
        """Test async iterating over response as text chunks."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/html") as response:
                assert response.status_code == 200
                chunks = [chunk async for chunk in response.aiter_text()]
                assert all(isinstance(chunk, str) for chunk in chunks)
                assert "<html" in "".join(chunks)

    async def test_async_stream_aiter_lines(self, base_url_ssl, ca_bundle):
        """Test async iterating over response line by line."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/robots.txt") as response:
                assert response.status_code == 200
                lines = [line async for line in response.aiter_lines()]
                assert len(lines) >= 1
                assert lines[0].startswith("User-agent")

    async def test_async_stream_aread(self, base_url_ssl, ca_bundle):
        """Test async reading entire response body at once."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/get", params={"key": "value"}) as response:
                assert response.status_code == 200
                content = await response.aread()
                assert json.loads(content)["args"] == {"key": "value"}
                assert response.is_consumed

    async def test_async_stream_sync_iteration_still_works(self, base_url_ssl, ca_bundle):
        """The synchronous iter_* / read / direct iteration API is kept (additive change)."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/html") as response:
                assert len(b"".join(response.iter_bytes())) > 0
            async with client.stream("GET", f"{base_url_ssl}/html") as response:
                assert len(b"".join(response)) > 0
            async with client.stream("GET", f"{base_url_ssl}/html") as response:
                assert "<html" in "".join(response.iter_text())
            async with client.stream("GET", f"{base_url_ssl}/robots.txt") as response:
                assert len(list(response.iter_lines())) >= 1
            async with client.stream("GET", f"{base_url_ssl}/get") as response:
                assert len(response.read()) > 0

    async def test_async_stream_metadata_available(self, base_url_ssl, ca_bundle):
        """Status, headers, cookies and URL are available before the body is read."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            url = f"{base_url_ssl}/response-headers?X-Test=test-value"
            async with client.stream("GET", url) as response:
                assert response.status_code == 200
                assert response.reason_phrase == "OK"
                assert response.is_success and not response.is_error
                assert response.headers["x-test"] == "test-value"
                assert response.url.startswith(f"{base_url_ssl}/response-headers")
                assert response.raise_for_status() is response
                assert not response.is_consumed
                assert not response.is_closed
            assert response.is_closed

    async def test_async_stream_aclose(self, base_url_ssl, ca_bundle):
        """aclose() closes the stream early; the context manager exit is then a no-op."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/html") as response:
                await response.aclose()
                assert response.is_closed
                with pytest.raises(httpr.StreamClosed):
                    async for _ in response.aiter_bytes():
                        pass

    async def test_async_stream_raise_for_status(self, base_url_ssl, ca_bundle):
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/status/404") as response:
                assert response.is_client_error
                with pytest.raises(httpr.HTTPStatusError):
                    response.raise_for_status()

    async def test_async_stream_invalid_method(self, base_url_ssl, ca_bundle):
        """Test that invalid HTTP method raises ValueError in async."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            with pytest.raises(ValueError, match="Unsupported HTTP method"):
                async with client.stream("INVALID", f"{base_url_ssl}/get") as _:  # type: ignore[arg-type]
                    pass

    async def test_async_stream_survives_client_close(self, base_url_ssl, ca_bundle):
        """An open stream holds its own handle to the pool and reads to the end after aclose()."""
        client = httpr.AsyncClient(ca_cert_file=ca_bundle)
        async with client.stream("GET", f"{base_url_ssl}/html") as response:
            await client.aclose()
            body = b"".join([chunk async for chunk in response.aiter_bytes()])
        assert b"<html" in body.lower()
        assert client.is_closed, "reading an in-flight stream does not reopen the client"

    # -- Issue #85: iteration must not block the event loop ---------------------

    async def test_aiter_bytes_does_not_block_event_loop(self, drip_url):
        """A heartbeat task keeps ticking while an async stream is being consumed."""
        stop = asyncio.Event()
        ticker = asyncio.create_task(_heartbeat(stop))
        async with httpr.AsyncClient() as client:
            async with client.stream("GET", f"{drip_url}/drip?chunks=10&pause=0.05") as response:
                chunks = [chunk async for chunk in response.aiter_bytes()]
        stop.set()
        ticks = await ticker
        assert b"".join(chunks) == b"".join(f"chunk-{i}\n".encode() for i in range(10))
        # The stream takes ~0.5s; a blocked loop would manage one or two ticks.
        assert ticks > 10, f"event loop only ticked {ticks} times during the stream"

    async def test_sync_iteration_blocks_event_loop(self, drip_url):
        """Control for the test above: the sync iterator does block the loop."""
        stop = asyncio.Event()
        ticker = asyncio.create_task(_heartbeat(stop))
        async with httpr.AsyncClient() as client:
            async with client.stream("GET", f"{drip_url}/drip?chunks=10&pause=0.05") as response:
                list(response.iter_bytes())
        stop.set()
        ticks = await ticker
        assert ticks <= 3

    async def test_aiter_lines_sse(self, drip_url):
        """aiter_lines() over a trickled text/event-stream response yields the events."""
        async with httpr.AsyncClient() as client:
            async with client.stream("GET", f"{drip_url}/sse?events=5&pause=0.02") as response:
                assert response.headers["content-type"] == "text/event-stream"
                lines = [line async for line in response.aiter_lines()]
        assert [line.rstrip("\n") for line in lines if line.strip()] == [f"data: {i}" for i in range(5)]

    async def test_concurrent_async_streams_overlap(self, drip_url):
        """Two async streams consumed concurrently overlap instead of running back to back.

        Asserted on the chunk arrival times, not on a wall-clock budget: on the
        GitHub macOS runners ``time.sleep(0.05)`` in the drip server overshoots by
        more than 100%, so a single stream alone takes over a second there.
        """
        arrivals: list[tuple[float, str]] = []

        async def consume(client, tag):
            chunks = []
            async with client.stream("GET", f"{drip_url}/drip?chunks=10&pause=0.05") as response:
                async for chunk in response.aiter_bytes():
                    arrivals.append((time.perf_counter(), tag))
                    chunks.append(chunk)
            return b"".join(chunks)

        async with httpr.AsyncClient() as client:
            bodies = await asyncio.gather(consume(client, "a"), consume(client, "b"))
        assert bodies[0] == bodies[1]
        assert len(bodies[0]) == len(b"".join(f"chunk-{i}\n".encode() for i in range(10)))

        first = {tag: min(t for t, g in arrivals if g == tag) for tag in "ab"}
        last = {tag: max(t for t, g in arrivals if g == tag) for tag in "ab"}
        shortest = min(last[tag] - first[tag] for tag in "ab")
        # The window in which both streams were delivering chunks. Serialised
        # streams give a window <= 0; concurrent ones share most of their lifetime.
        shared = min(last.values()) - max(first.values())
        order = "".join(tag for _, tag in sorted(arrivals))
        assert shared > 0.5 * shortest, f"streams did not overlap: arrival order {order}"


def test_stream_delete_json_body(base_url_ssl, ca_bundle):
    """Issue #83: streaming requests also send bodies on non-POST methods."""
    client = httpr.Client(ca_cert_file=ca_bundle)
    body = {"id": 1}
    with client.stream("DELETE", f"{base_url_ssl}/anything", json=body) as response:
        assert response.status_code == 200
        payload = json.loads(response.read())
    assert payload["method"] == "DELETE"
    assert payload["json"] == body
