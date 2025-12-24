import asyncio
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # <-- import ThreadingHTTPServer

import httpx
import pytest

# A global list to record connection identifiers from the server.
CONNECTION_IDS = []


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # Enable persistent connections.

    def do_GET(self):
        global CONNECTION_IDS
        # Record an identifier for this underlying socket.
        conn_id = self.connection.fileno()
        CONNECTION_IDS.append(conn_id)

        # If the URL is /delay/<seconds>, sleep before replying.
        if self.path.startswith("/delay/"):
            try:
                delay = float(self.path.split("/delay/")[-1])
            except Exception:
                delay = 0
            time.sleep(delay)

        response_body = b"Hello, world!"
        self.send_response(200)
        self.send_header("Content-Length", str(len(response_body)))
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        # Override to prevent writing to stderr during tests.
        pass


# A pytest fixture that starts a simple HTTP server in a background thread.
@pytest.fixture(scope="module")
def test_server():
    # Use a multithreaded HTTP server.
    server = ThreadingHTTPServer(("127.0.0.1", 0), SimpleHTTPRequestHandler)
    host, port = server.server_address
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield host, port
    server.shutdown()
    thread.join()


# A fixture to clear our connection tracking between tests.
@pytest.fixture(autouse=True)
def clear_connection_ids():
    global CONNECTION_IDS
    CONNECTION_IDS.clear()
    yield
    CONNECTION_IDS.clear()


def test_simple_get(test_server):
    """A basic test to check that a simple GET returns the expected response."""
    host, port = test_server
    url = f"http://{host}:{port}/"
    with httpx.Client() as client:
        response = client.get(url)
        assert response.status_code == 200
        assert response.text == "Hello, world!"


def test_keepalive(test_server):
    """
    Test that a client reuses the same connection.
    Three quick GET requests should be handled on the same underlying socket.
    """
    host, port = test_server
    url = f"http://{host}:{port}/"
    with httpx.Client() as client:
        for _ in range(3):
            response = client.get(url)
            assert response.status_code == 200
            assert response.text == "Hello, world!"
    # Because the client should reuse its connection, all requests
    # should have been handled by the same socket.
    distinct = set(CONNECTION_IDS)
    assert len(distinct) == 1


def test_timeout(test_server):
    """
    Test that the client’s timeout settings take effect.
    A request to a delayed endpoint (1 second delay) with a 0.5-second timeout
    should return (via an exception) in under 1 second.
    """
    host, port = test_server
    url = f"http://{host}:{port}/delay/1"
    with httpx.Client(timeout=httpx.Timeout(0.5)) as client:
        start = time.time()
        try:
            client.get(url)
            # If no exception is raised, fail the test.
            assert False, "Expected timeout behavior"
        except Exception:
            elapsed = time.time() - start
            # The total time taken should be less than 1 second.
            assert elapsed < 1.0


@pytest.mark.asyncio
async def test_max_connections(test_server):
    """
    Test that when the maximum number of connections is set to 1,
    concurrent asynchronous requests are all handled by the same connection.
    """
    host, port = test_server
    url = f"http://{host}:{port}/delay/1"
    limits = httpx.Limits(max_connections=1, max_keepalive_connections=1)
    async with httpx.AsyncClient(limits=limits, timeout=5.0) as client:
        tasks = [client.get(url) for _ in range(3)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for response in responses:
            # If any exception is encountered, fail the test.
            if isinstance(response, Exception):
                assert False, f"Unexpected exception: {response}"
            else:
                assert response.status_code == 200
    # With max_connections=1, all requests should be served on one connection.
    distinct = set(CONNECTION_IDS)
    assert len(distinct) == 1


@pytest.mark.asyncio
async def test_multiple_connections(test_server):
    """
    Test that when the maximum number of connections is raised (to 2),
    concurrent requests may be served on up to two distinct connections.
    """
    host, port = test_server
    url = f"http://{host}:{port}/delay/1"
    limits = httpx.Limits(max_connections=2, max_keepalive_connections=2)
    async with httpx.AsyncClient(limits=limits, timeout=5.0) as client:
        tasks = [client.get(url) for _ in range(4)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for response in responses:
            if isinstance(response, Exception):
                raise AssertionError(f"Unexpected exception: {response}")
            else:
                assert response.status_code == 200
    # We expect no more than 2 distinct connections.
    distinct = set(CONNECTION_IDS)
    assert len(distinct) <= 2
