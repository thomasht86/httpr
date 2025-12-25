"""E2E streaming tests using httpbun container."""

import pytest

import httpr


@pytest.mark.e2e
class TestDripStreaming:
    """Test streaming with httpbun's /drip endpoint for timed byte delivery."""

    def test_drip_iter_bytes(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test streaming byte chunks from /drip endpoint."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        # Request 5 bytes with minimal delay
        url = f"{e2e_base_url}/drip?numbytes=5&duration=1&delay=0"

        chunks = []
        with client.stream("GET", url) as response:
            assert response.status_code == 200
            for chunk in response.iter_bytes():
                chunks.append(chunk)

        # Verify we received data
        total_bytes = b"".join(chunks)
        assert len(total_bytes) == 5

    def test_drip_iter_text(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test streaming text chunks from /drip endpoint."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        url = f"{e2e_base_url}/drip?numbytes=10&duration=1&delay=0"

        text_chunks = []
        with client.stream("GET", url) as response:
            assert response.status_code == 200
            for chunk in response.iter_text():
                text_chunks.append(chunk)

        # Verify we received text data
        total_text = "".join(text_chunks)
        assert len(total_text) == 10

    def test_stream_read_full(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test reading entire stream at once with read()."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        url = f"{e2e_base_url}/drip?numbytes=20&duration=1&delay=0"

        with client.stream("GET", url) as response:
            assert response.status_code == 200
            content = response.read()

        assert len(content) == 20


@pytest.mark.e2e
class TestSSEStreaming:
    """Test Server-Sent Events streaming with httpbun's /sse endpoint."""

    def test_sse_iter_lines(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test line-by-line streaming from /sse endpoint."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        # Request 3 SSE events with 1 second delay (httpbun expects seconds as int)
        url = f"{e2e_base_url}/sse?count=3&delay=1"

        lines = []
        with client.stream("GET", url) as response:
            assert response.status_code == 200
            for line in response.iter_lines():
                lines.append(line)

        # SSE format: each event has "event:", "id:", "data:", and empty line separator
        # Verify we got SSE-formatted content
        assert any("data:" in line for line in lines)
        assert any("id:" in line for line in lines)

    def test_sse_multiple_events(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test receiving multiple SSE events."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        url = f"{e2e_base_url}/sse?count=5&delay=1"

        data_lines = []
        with client.stream("GET", url) as response:
            assert response.status_code == 200
            for line in response.iter_lines():
                if line.startswith("data:"):
                    data_lines.append(line)

        # Should have received 5 data lines (one per event)
        assert len(data_lines) == 5

    def test_stream_context_manager_closes(self, e2e_base_url: str, e2e_ca_cert: str) -> None:
        """Test that stream is properly closed after context manager exits."""
        client = httpr.Client(ca_cert_file=e2e_ca_cert)
        url = f"{e2e_base_url}/drip?numbytes=100&duration=2&delay=0"

        with client.stream("GET", url) as response:
            assert response.status_code == 200
            # Read just a bit
            next(response.iter_bytes())
            assert not response.is_closed

        # After exiting context, stream should be closed
        assert response.is_closed
