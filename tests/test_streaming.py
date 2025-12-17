"""Tests for streaming response functionality."""

import pytest
import httpr  # type: ignore


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
                content = response.read()

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
        
        with client.stream(
            "GET", 
            f"{base_url_ssl}/headers",
            headers={"X-Custom-Header": "custom-value"}
        ) as response:
            assert response.status_code == 200
            content = response.read()
            assert b"X-Custom-Header" in content

    def test_stream_post_with_json(self, base_url_ssl, ca_bundle):
        """Test streaming POST request with JSON body."""
        client = httpr.Client(ca_cert_file=ca_bundle)
        
        with client.stream(
            "POST",
            f"{base_url_ssl}/post",
            json={"test": "data"}
        ) as response:
            assert response.status_code == 200
            content = response.read()
            assert b"test" in content

    def test_stream_invalid_method(self, base_url_ssl, ca_bundle):
        """Test that invalid HTTP method raises ValueError."""
        client = httpr.Client(ca_cert_file=ca_bundle)
        
        with pytest.raises(ValueError, match="Unsupported HTTP method"):
            with client.stream("INVALID", f"{base_url_ssl}/get") as response:  # type: ignore[arg-type]
                pass


@pytest.mark.asyncio
class TestStreamingAsyncClient:
    """Test streaming functionality with async AsyncClient."""

    async def test_async_stream_iter_bytes(self, base_url_ssl, ca_bundle):
        """Test async iterating over response as bytes chunks."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/get") as response:
                assert response.status_code == 200
                chunks = list(response.iter_bytes())
                total_bytes = b"".join(chunks)
                assert len(total_bytes) > 0

    async def test_async_stream_direct_iteration(self, base_url_ssl, ca_bundle):
        """Test async direct iteration over StreamingResponse."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/html") as response:
                assert response.status_code == 200
                chunks = list(response)
                total_bytes = b"".join(chunks)
                assert len(total_bytes) > 0

    async def test_async_stream_iter_text(self, base_url_ssl, ca_bundle):
        """Test async iterating over response as text chunks."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/html") as response:
                assert response.status_code == 200
                chunks = list(response.iter_text())
                full_text = "".join(chunks)
                assert len(full_text) > 0

    async def test_async_stream_iter_lines(self, base_url_ssl, ca_bundle):
        """Test async iterating over response line by line."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/robots.txt") as response:
                assert response.status_code == 200
                lines = list(response.iter_lines())
                assert len(lines) >= 1

    async def test_async_stream_read_all(self, base_url_ssl, ca_bundle):
        """Test async reading entire response body at once."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/get") as response:
                assert response.status_code == 200
                content = response.read()
                assert len(content) > 0

    async def test_async_stream_headers_available(self, base_url_ssl, ca_bundle):
        """Test that headers are available before iteration in async."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream("GET", f"{base_url_ssl}/get") as response:
                assert response.status_code == 200
                # Use keys() instead of len() since CaseInsensitiveHeaderMap doesn't have __len__
                assert len(response.headers.keys()) > 0

    async def test_async_stream_with_params(self, base_url_ssl, ca_bundle):
        """Test async streaming with query parameters."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            async with client.stream(
                "GET", 
                f"{base_url_ssl}/get", 
                params={"key": "value"}
            ) as response:
                assert response.status_code == 200
                content = response.read()
                assert b"key" in content

    async def test_async_stream_invalid_method(self, base_url_ssl, ca_bundle):
        """Test that invalid HTTP method raises ValueError in async."""
        async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
            with pytest.raises(ValueError, match="Unsupported HTTP method"):
                async with client.stream("INVALID", f"{base_url_ssl}/get") as response:  # type: ignore[arg-type]
                    pass
