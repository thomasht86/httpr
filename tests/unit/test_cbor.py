"""Tests for CBOR response deserialization support."""

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import cbor2
import pytest

import httpr


class CborHandler(BaseHTTPRequestHandler):
    """Serves CBOR responses for testing."""

    def do_GET(self):
        if self.path == "/cbor/echo":
            data = {"message": "CBOR response", "count": 42, "items": [1, 2, 3, 4, 5]}
        elif self.path == "/cbor/large":
            data = [[i + j * 0.1 for j in range(1024)] for i in range(10)]
        else:
            self.send_error(404)
            return
        body = cbor2.dumps(data)
        self.send_response(200)
        self.send_header("Content-Type", "application/cbor")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # Suppress logs during tests


@pytest.fixture(scope="module")
def cbor_server():
    """Start a simple CBOR test server on a random free port."""
    server = HTTPServer(("127.0.0.1", 0), CborHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


def test_json_serialization_default(base_url_ssl, ca_bundle):
    """Test that JSON is used by default when Accept header is not set."""
    client = httpr.Client(ca_cert_file=ca_bundle)

    test_data = {"test": "data"}

    # Send without Accept header - should use JSON (default)
    response = client.post(
        f"{base_url_ssl}/anything",
        json=test_data,
    )

    assert response.status_code == 200
    json_data = response.json()

    # Should use JSON by default
    assert json_data["headers"]["Content-Type"] == "application/json"
    assert json_data["json"] == test_data


def test_cbor_response_json_auto_detect(cbor_server):
    """Test that response.json() auto-detects CBOR from Content-Type."""
    client = httpr.Client()
    response = client.get(f"{cbor_server}/cbor/echo")

    assert response.status_code == 200
    assert "application/cbor" in response.headers["content-type"]

    # json() should transparently deserialize CBOR
    data = response.json()
    assert data["message"] == "CBOR response"
    assert data["count"] == 42
    assert data["items"] == [1, 2, 3, 4, 5]


def test_cbor_response_explicit(cbor_server):
    """Test that response.cbor() explicitly deserializes CBOR."""
    client = httpr.Client()
    response = client.get(f"{cbor_server}/cbor/echo")

    assert response.status_code == 200

    # cbor() should explicitly deserialize
    data = response.cbor()
    assert data["message"] == "CBOR response"
    assert data["count"] == 42
    assert data["items"] == [1, 2, 3, 4, 5]


def test_cbor_response_large_data(cbor_server):
    """Test CBOR deserialization with large dataset."""
    client = httpr.Client()
    response = client.get(f"{cbor_server}/cbor/large")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10
    assert len(data[0]) == 1024
