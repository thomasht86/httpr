"""Tests for httpr exception hierarchy."""

import pytest
import httpr


def test_exception_imports():
    """Test that all exceptions can be imported."""
    # Base exceptions
    assert hasattr(httpr, 'HTTPError')
    assert hasattr(httpr, 'RequestError')
    assert hasattr(httpr, 'TransportError')
    assert hasattr(httpr, 'NetworkError')
    assert hasattr(httpr, 'TimeoutException')
    assert hasattr(httpr, 'ProtocolError')
    assert hasattr(httpr, 'StreamError')
    
    # Timeout exceptions
    assert hasattr(httpr, 'ConnectTimeout')
    assert hasattr(httpr, 'ReadTimeout')
    assert hasattr(httpr, 'WriteTimeout')
    assert hasattr(httpr, 'PoolTimeout')
    
    # Network exceptions
    assert hasattr(httpr, 'ConnectError')
    assert hasattr(httpr, 'ReadError')
    assert hasattr(httpr, 'WriteError')
    assert hasattr(httpr, 'CloseError')
    
    # Protocol exceptions
    assert hasattr(httpr, 'LocalProtocolError')
    assert hasattr(httpr, 'RemoteProtocolError')
    
    # Other exceptions
    assert hasattr(httpr, 'UnsupportedProtocol')
    assert hasattr(httpr, 'ProxyError')
    assert hasattr(httpr, 'TooManyRedirects')
    assert hasattr(httpr, 'HTTPStatusError')
    assert hasattr(httpr, 'DecodingError')
    assert hasattr(httpr, 'StreamConsumed')
    assert hasattr(httpr, 'ResponseNotRead')
    assert hasattr(httpr, 'RequestNotRead')
    assert hasattr(httpr, 'StreamClosed')
    assert hasattr(httpr, 'InvalidURL')
    assert hasattr(httpr, 'CookieConflict')


def test_exception_hierarchy():
    """Test that exception hierarchy is correct."""
    # RequestError inherits from HTTPError
    assert issubclass(httpr.RequestError, httpr.HTTPError)
    
    # TransportError inherits from RequestError
    assert issubclass(httpr.TransportError, httpr.RequestError)
    
    # NetworkError inherits from TransportError
    assert issubclass(httpr.NetworkError, httpr.TransportError)
    
    # TimeoutException inherits from TransportError
    assert issubclass(httpr.TimeoutException, httpr.TransportError)
    
    # ProtocolError inherits from TransportError
    assert issubclass(httpr.ProtocolError, httpr.TransportError)
    
    # Specific timeout exceptions
    assert issubclass(httpr.ConnectTimeout, httpr.TimeoutException)
    assert issubclass(httpr.ReadTimeout, httpr.TimeoutException)
    assert issubclass(httpr.WriteTimeout, httpr.TimeoutException)
    assert issubclass(httpr.PoolTimeout, httpr.TimeoutException)
    
    # Specific network exceptions
    assert issubclass(httpr.ConnectError, httpr.NetworkError)
    assert issubclass(httpr.ReadError, httpr.NetworkError)
    assert issubclass(httpr.WriteError, httpr.NetworkError)
    assert issubclass(httpr.CloseError, httpr.NetworkError)
    
    # Protocol exceptions
    assert issubclass(httpr.LocalProtocolError, httpr.ProtocolError)
    assert issubclass(httpr.RemoteProtocolError, httpr.ProtocolError)
    
    # Other transport/request exceptions
    assert issubclass(httpr.UnsupportedProtocol, httpr.TransportError)
    assert issubclass(httpr.ProxyError, httpr.TransportError)
    assert issubclass(httpr.TooManyRedirects, httpr.RequestError)
    assert issubclass(httpr.HTTPStatusError, httpr.HTTPError)
    assert issubclass(httpr.DecodingError, httpr.RequestError)


def test_invalid_url_raises_request_error():
    """Test that invalid URLs raise the appropriate exception."""
    client = httpr.Client()
    
    # Invalid URL should raise RequestError or a subclass
    with pytest.raises(httpr.RequestError):
        client.get("not-a-valid-url")


def test_timeout_raises_timeout_exception(base_url_ssl, ca_bundle):
    """Test that timeouts raise ReadTimeout."""
    client = httpr.Client(timeout=0.001, ca_cert_file=ca_bundle)
    
    # Very short timeout should raise a timeout exception
    with pytest.raises(httpr.TimeoutException):
        client.get(f"{base_url_ssl}/delay/5")


def test_connection_error_nonexistent_host():
    """Test that connection to nonexistent host raises ConnectError."""
    client = httpr.Client()
    
    # Connection to nonexistent host should raise ConnectError
    with pytest.raises(httpr.NetworkError):
        client.get("http://thishostdoesnotexist12345.invalid")


def test_invalid_proxy_raises_proxy_error(base_url_ssl, ca_bundle):
    """Test that invalid proxy raises ProxyError when making a request."""
    client = httpr.Client(proxy="http://invalid-proxy-host-12345.invalid:8080", ca_cert_file=ca_bundle)
    
    # Invalid proxy should cause ProxyError or ConnectError when making request
    with pytest.raises((httpr.ProxyError, httpr.ConnectError, httpr.NetworkError)):
        client.get(f"{base_url_ssl}/get")


def test_exception_can_be_caught_by_base_class(base_url_ssl, ca_bundle):
    """Test that specific exceptions can be caught by their base classes."""
    client = httpr.Client(timeout=0.001, ca_cert_file=ca_bundle)
    
    # ReadTimeout should be catchable as TimeoutException
    with pytest.raises(httpr.TimeoutException):
        client.get(f"{base_url_ssl}/delay/5")
    
    # ReadTimeout should also be catchable as TransportError
    with pytest.raises(httpr.TransportError):
        client.get(f"{base_url_ssl}/delay/5")
    
    # ReadTimeout should also be catchable as RequestError
    with pytest.raises(httpr.RequestError):
        client.get(f"{base_url_ssl}/delay/5")
    
    # ReadTimeout should also be catchable as HTTPError
    with pytest.raises(httpr.HTTPError):
        client.get(f"{base_url_ssl}/delay/5")


def test_file_not_found_raises_request_error(base_url_ssl, ca_bundle):
    """Test that uploading a nonexistent file raises RequestError."""
    client = httpr.Client(ca_cert_file=ca_bundle)
    
    with pytest.raises(httpr.RequestError):
        client.post(
            f"{base_url_ssl}/post",
            files={"file": "/nonexistent/file/path.txt"}
        )


@pytest.mark.asyncio
async def test_async_client_exceptions(base_url_ssl, ca_bundle):
    """Test that AsyncClient also raises proper exceptions."""
    async with httpr.AsyncClient(timeout=0.001, ca_cert_file=ca_bundle) as client:
        with pytest.raises(httpr.TimeoutException):
            await client.get(f"{base_url_ssl}/delay/5")
