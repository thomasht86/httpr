from __future__ import annotations

import sys
from collections.abc import Iterator
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from typing import Any, Literal, TypedDict

if sys.version_info <= (3, 11):
    from typing_extensions import Unpack
else:
    from typing import Unpack

HttpMethod = Literal["GET", "HEAD", "OPTIONS", "DELETE", "POST", "PUT", "PATCH"]

class RequestParams(TypedDict, total=False):
    auth: tuple[str, str | None] | None
    auth_bearer: str | None
    params: dict[str, str] | None
    headers: dict[str, str] | None
    cookies: dict[str, str] | None
    timeout: float | None
    content: bytes | None
    data: dict[str, Any] | None
    json: Any | None
    files: dict[str, str] | None

class ClientRequestParams(RequestParams):
    verify: bool | None
    ca_cert_file: str | None
    client_pem: str | None

class CaseInsensitiveHeaderMap:
    """
    A case-insensitive dictionary-like class for HTTP headers.

    HTTP headers are case-insensitive per the HTTP specification.
    This class allows accessing headers using any case while preserving
    the original case for iteration.

    Example:
        ```python
        headers = response.headers
        content_type = headers["Content-Type"]  # Works
        content_type = headers["content-type"]  # Also works

        if "Content-Type" in headers:
            print("Has content type")

        for key, value in headers.items():
            print(f"{key}: {value}")
        ```
    """
    def __getitem__(self, key: str) -> str:
        """Get a header value by name (case-insensitive)."""
        ...
    def __contains__(self, key: str) -> bool:
        """Check if a header exists (case-insensitive)."""
        ...
    def __iter__(self) -> Iterator[str]:
        """Iterate over header names."""
        ...
    def items(self) -> list[tuple[str, str]]:
        """Return a list of (name, value) tuples."""
        ...
    def keys(self) -> list[str]:
        """Return a list of header names."""
        ...
    def values(self) -> list[str]:
        """Return a list of header values."""
        ...
    def get(self, key: str, default: str | None = None) -> str:
        """
        Get a header value by name (case-insensitive).

        Args:
            key: Header name to look up.
            default: Value to return if header is not found. Defaults to None.

        Returns:
            The header value, or the default if not found.
        """
        ...

class Response:
    """
    An HTTP response object.

    This class provides access to the response status, headers, cookies,
    and body content. The body can be accessed as bytes, text, JSON, or CBOR.

    Example:
        ```python
        response = client.get("https://httpbin.org/get")

        # Status
        print(response.status_code)  # 200
        print(response.url)  # Final URL after redirects

        # Headers (case-insensitive access)
        print(response.headers["content-type"])

        # Body
        print(response.text)  # Decoded text
        print(response.json())  # Parsed JSON
        print(response.content)  # Raw bytes
        ```
    """
    @property
    def content(self) -> bytes:
        """Raw response body as bytes."""
        ...
    @property
    def cookies(self) -> dict[str, str]:
        """Response cookies as a dictionary."""
        ...
    @property
    def headers(self) -> CaseInsensitiveHeaderMap:
        """
        Response headers as a case-insensitive dictionary-like object.

        Headers can be accessed using any case (e.g., "Content-Type" or "content-type").
        """
        ...
    @property
    def status_code(self) -> int:
        """HTTP status code (e.g., 200, 404, 500)."""
        ...
    @property
    def url(self) -> str:
        """Final URL after any redirects."""
        ...
    @property
    def encoding(self) -> str:
        """
        Character encoding of the response.

        Detected from Content-Type header or response body.
        Can be set to override auto-detection.
        """
        ...
    @encoding.setter
    def encoding(self, value: str) -> None: ...
    @property
    def text(self) -> str:
        """Response body decoded as text using the detected encoding."""
        ...
    def json(self) -> Any:
        """
        Parse response body as JSON.

        If Content-Type is application/cbor, automatically deserializes as CBOR.

        Returns:
            Parsed JSON/CBOR data as Python objects.
        """
        ...
    def cbor(self) -> Any:
        """
        Parse response body as CBOR (Concise Binary Object Representation).

        Returns:
            Parsed CBOR data as Python objects.
        """
        ...
    @property
    def text_markdown(self) -> str:
        """
        Response body converted from HTML to Markdown format.

        Useful for reading HTML content as plain text.
        """
        ...
    @property
    def text_plain(self) -> str:
        """
        Response body converted from HTML to plain text.

        Strips all formatting and returns only the text content.
        """
        ...
    @property
    def text_rich(self) -> str:
        """
        Response body converted from HTML to rich text format.

        Preserves some formatting using Unicode characters.
        """
        ...

class TextIterator:
    """Iterator for text chunks from a streaming response."""
    def __iter__(self) -> TextIterator: ...
    def __next__(self) -> str: ...

class LineIterator:
    """Iterator for lines from a streaming response."""
    def __iter__(self) -> LineIterator: ...
    def __next__(self) -> str: ...

class StreamingResponse:
    """
    A streaming HTTP response that allows iterating over chunks of data.

    This class provides methods to iterate over the response body in chunks
    without buffering the entire response in memory.
    """

    @property
    def cookies(self) -> dict[str, str]:
        """Response cookies."""
        ...
    @property
    def headers(self) -> CaseInsensitiveHeaderMap:
        """Response headers (case-insensitive access)."""
        ...
    @property
    def status_code(self) -> int:
        """HTTP status code."""
        ...
    @property
    def url(self) -> str:
        """Final URL after any redirects."""
        ...
    @property
    def is_closed(self) -> bool:
        """Whether the stream has been closed."""
        ...
    @property
    def is_consumed(self) -> bool:
        """Whether the stream has been fully consumed."""
        ...
    def __iter__(self) -> Iterator[bytes]:
        """Iterate over the response body as bytes chunks."""
        ...
    def __next__(self) -> bytes:
        """Get the next chunk of bytes."""
        ...
    def iter_bytes(self) -> Iterator[bytes]:
        """
        Iterate over the response body as bytes chunks.

        Yields chunks of bytes as they are received from the server.
        """
        ...
    def iter_text(self) -> TextIterator:
        """
        Iterate over the response body as text chunks.

        Decodes each chunk using the response's encoding.
        """
        ...
    def iter_lines(self) -> LineIterator:
        """
        Iterate over the response body line by line.

        Yields complete lines including newline characters.
        """
        ...
    def read(self) -> bytes:
        """
        Read the entire remaining response body into memory.

        This consumes the stream.
        """
        ...
    def close(self) -> None:
        """
        Close the streaming response and release resources.
        """
        ...

class RClient:
    def __init__(
        self,
        auth: tuple[str, str | None] | None = None,
        auth_bearer: str | None = None,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        timeout: float | None = None,
        cookie_store: bool | None = True,
        referer: bool | None = True,
        proxy: str | None = None,
        follow_redirects: bool | None = True,
        max_redirects: int | None = 20,
        verify: bool | None = True,
        ca_cert_file: str | None = None,
        client_pem: str | None = None,
        https_only: bool | None = False,
        http2_only: bool | None = False,
    ): ...
    @property
    def headers(self) -> dict[str, str]: ...
    @headers.setter
    def headers(self, headers: dict[str, str] | None) -> None: ...
    @property
    def cookies(self) -> dict[str, str]: ...
    @cookies.setter
    def cookies(self, cookies: dict[str, str] | None) -> None: ...
    @property
    def proxy(self) -> str | None: ...
    @proxy.setter
    def proxy(self, proxy: str) -> None: ...
    @property
    def auth(self) -> tuple[str, str | None] | None: ...
    @auth.setter
    def auth(self, auth: tuple[str, str | None] | None) -> None: ...
    @property
    def auth_bearer(self) -> str | None: ...
    @auth_bearer.setter
    def auth_bearer(self, auth_bearer: str | None) -> None: ...
    @property
    def params(self) -> dict[str, str] | None: ...
    @params.setter
    def params(self, params: dict[str, str] | None) -> None: ...
    @property
    def timeout(self) -> float | None: ...
    @timeout.setter
    def timeout(self, timeout: float | None) -> None: ...
    def request(self, method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def _stream(self, method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]) -> StreamingResponse: ...
    def get(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def head(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def options(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def delete(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def post(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def put(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def patch(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...

class Client(RClient):
    """
    A synchronous HTTP client with connection pooling.

    The Client class provides a high-level interface for making HTTP requests.
    It supports connection pooling, automatic cookie handling, and various
    authentication methods.

    Example:
        ```python
        import httpr

        # Using context manager (recommended)
        with httpr.Client() as client:
            response = client.get("https://httpbin.org/get")
            print(response.json())

        # Or manually
        client = httpr.Client()
        response = client.get("https://httpbin.org/get")
        client.close()
        ```

    Attributes:
        headers: Default headers sent with all requests. Excludes Cookie header.
        cookies: Default cookies sent with all requests.
        auth: Basic auth credentials as (username, password) tuple.
        params: Default query parameters added to all requests.
        timeout: Default timeout in seconds.
        proxy: Proxy URL for requests.
    """
    def __init__(
        self,
        auth: tuple[str, str | None] | None = None,
        auth_bearer: str | None = None,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        cookie_store: bool | None = True,
        referer: bool | None = True,
        proxy: str | None = None,
        timeout: float | None = 30,
        follow_redirects: bool | None = True,
        max_redirects: int | None = 20,
        verify: bool | None = True,
        ca_cert_file: str | None = None,
        client_pem: str | None = None,
        https_only: bool | None = False,
        http2_only: bool | None = False,
    ) -> None:
        """
        Initialize an HTTP client.

        Args:
            auth: Basic auth credentials as (username, password). Password can be None.
            auth_bearer: Bearer token for Authorization header.
            params: Default query parameters to include in all requests.
            headers: Default headers to send with all requests.
            cookies: Default cookies to send with all requests.
            cookie_store: Enable persistent cookie store. Default is True.
            referer: Automatically set Referer header. Default is True.
            proxy: Proxy URL (e.g., "http://proxy:8080" or "socks5://127.0.0.1:1080").
            timeout: Request timeout in seconds. Default is 30.
            follow_redirects: Follow HTTP redirects. Default is True.
            max_redirects: Maximum redirects to follow. Default is 20.
            verify: Verify SSL certificates. Default is True.
            ca_cert_file: Path to CA certificate bundle (PEM format).
            client_pem: Path to client certificate for mTLS (PEM format).
            https_only: Only allow HTTPS requests. Default is False.
            http2_only: Use HTTP/2 only. Default is False.
        """
        ...
    def __enter__(self) -> Client: ...
    def __exit__(self, *args: Any) -> None: ...
    def close(self) -> None:
        """Close the client and release resources."""
        ...
    def stream(
        self, method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]
    ) -> AbstractContextManager[StreamingResponse]:
        """
        Make a streaming HTTP request.

        Returns a context manager that yields a StreamingResponse for iterating
        over the response body in chunks.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS).
            url: Request URL.
            **kwargs: Request parameters.

        Yields:
            StreamingResponse: A response object that can be iterated.

        Example:
            ```python
            with client.stream("GET", "https://example.com/large-file") as response:
                for chunk in response.iter_bytes():
                    process(chunk)
            ```
        """
        ...

class AsyncClient(Client):
    """
    An asynchronous HTTP client for use with asyncio.

    AsyncClient wraps the synchronous Client using asyncio.run_in_executor(),
    providing an async interface while leveraging the Rust implementation's
    performance.

    Example:
        ```python
        import asyncio
        import httpr

        async def main():
            async with httpr.AsyncClient() as client:
                response = await client.get("https://httpbin.org/get")
                print(response.json())

        asyncio.run(main())
        ```

    Note:
        AsyncClient runs synchronous Rust code in a thread executor.
        It provides concurrency benefits for I/O-bound tasks but is not
        native async I/O.
    """
    def __init__(
        self,
        auth: tuple[str, str | None] | None = None,
        auth_bearer: str | None = None,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        cookie_store: bool | None = True,
        referer: bool | None = True,
        proxy: str | None = None,
        timeout: float | None = 30,
        follow_redirects: bool | None = True,
        max_redirects: int | None = 20,
        verify: bool | None = True,
        ca_cert_file: str | None = None,
        client_pem: str | None = None,
        https_only: bool | None = False,
        http2_only: bool | None = False,
    ) -> None:
        """Initialize an async HTTP client. Accepts the same parameters as Client."""
        ...
    async def __aenter__(self) -> AsyncClient: ...
    async def __aexit__(self, *args: Any) -> None: ...
    async def aclose(self) -> None:
        """Close the async client."""
        ...
    async def request(  # type: ignore[override]
        self, method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]
    ) -> Response:
        """Make an async HTTP request."""
        ...
    async def get(  # type: ignore[override]
        self, url: str, **kwargs: Unpack[RequestParams]
    ) -> Response:
        """Make an async GET request."""
        ...
    async def head(  # type: ignore[override]
        self, url: str, **kwargs: Unpack[RequestParams]
    ) -> Response:
        """Make an async HEAD request."""
        ...
    async def options(  # type: ignore[override]
        self, url: str, **kwargs: Unpack[RequestParams]
    ) -> Response:
        """Make an async OPTIONS request."""
        ...
    async def delete(  # type: ignore[override]
        self, url: str, **kwargs: Unpack[RequestParams]
    ) -> Response:
        """Make an async DELETE request."""
        ...
    async def post(  # type: ignore[override]
        self, url: str, **kwargs: Unpack[RequestParams]
    ) -> Response:
        """Make an async POST request."""
        ...
    async def put(  # type: ignore[override]
        self, url: str, **kwargs: Unpack[RequestParams]
    ) -> Response:
        """Make an async PUT request."""
        ...
    async def patch(  # type: ignore[override]
        self, url: str, **kwargs: Unpack[RequestParams]
    ) -> Response:
        """Make an async PATCH request."""
        ...
    def stream(  # type: ignore[override]
        self, method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]
    ) -> AbstractAsyncContextManager[StreamingResponse]:
        """
        Make an async streaming HTTP request.

        Returns an async context manager that yields a StreamingResponse.

        Example:
            ```python
            async with client.stream("GET", "https://example.com/large-file") as response:
                for chunk in response.iter_bytes():
                    process(chunk)
            ```
        """
        ...

def request(method: HttpMethod, url: str, **kwargs: Unpack[ClientRequestParams]) -> Response: ...
def get(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response: ...
def head(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response: ...
def options(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response: ...
def delete(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response: ...
def post(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response: ...
def put(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response: ...
def patch(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response: ...

# Exception hierarchy - Base exceptions
class HTTPError(Exception):
    """Base class for all httpr exceptions."""

class RequestError(HTTPError):
    """Base class for all exceptions that may occur when issuing a .request()."""

class TransportError(RequestError):
    """Base class for all exceptions that occur at the level of the Transport API."""

class NetworkError(TransportError):
    """The base class for network-related errors."""

class TimeoutException(TransportError):
    """The base class for timeout errors."""

class ProtocolError(TransportError):
    """The protocol was violated."""

class StreamError(Exception):
    """The base class for stream exceptions."""

# Timeout exceptions
class ConnectTimeout(TimeoutException):
    """Timed out while connecting to the host."""

class ReadTimeout(TimeoutException):
    """Timed out while receiving data from the host."""

class WriteTimeout(TimeoutException):
    """Timed out while sending data to the host."""

class PoolTimeout(TimeoutException):
    """Timed out waiting to acquire a connection from the pool."""

# Network exceptions
class ConnectError(NetworkError):
    """Failed to establish a connection."""

class ReadError(NetworkError):
    """Failed to receive data from the network."""

class WriteError(NetworkError):
    """Failed to send data through the network."""

class CloseError(NetworkError):
    """Failed to close a connection."""

# Protocol exceptions
class LocalProtocolError(ProtocolError):
    """A protocol was violated by the client."""

class RemoteProtocolError(ProtocolError):
    """The protocol was violated by the server."""

# Other transport/request exceptions
class UnsupportedProtocol(TransportError):
    """Attempted to make a request to an unsupported protocol."""

class ProxyError(TransportError):
    """An error occurred while establishing a proxy connection."""

class TooManyRedirects(RequestError):
    """Too many redirects."""

class HTTPStatusError(HTTPError):
    """The response had an error HTTP status of 4xx or 5xx."""

class DecodingError(RequestError):
    """Decoding of the response failed, due to a malformed encoding."""

# Stream exceptions
class StreamConsumed(StreamError):
    """Attempted to read or stream content, but the content has already been consumed."""

class ResponseNotRead(StreamError):
    """Attempted to access streaming response content, without having called read()."""

class RequestNotRead(StreamError):
    """Attempted to access streaming request content, without having called read()."""

class StreamClosed(StreamError):
    """Attempted to read or stream response content, but the request has been closed."""

# Other exceptions
class InvalidURL(Exception):
    """URL is improperly formed or cannot be parsed."""

class CookieConflict(Exception):
    """Attempted to lookup a cookie by name, but multiple cookies existed."""

__all__ = [
    # Type aliases
    "HttpMethod",
    "RequestParams",
    "ClientRequestParams",
    # Response types
    "Response",
    "StreamingResponse",
    "CaseInsensitiveHeaderMap",
    "TextIterator",
    "LineIterator",
    # Client classes
    "RClient",
    "Client",
    "AsyncClient",
    # Module-level functions
    "request",
    "get",
    "head",
    "options",
    "delete",
    "post",
    "put",
    "patch",
    # Base exceptions
    "HTTPError",
    "RequestError",
    "TransportError",
    "NetworkError",
    "TimeoutException",
    "ProtocolError",
    "StreamError",
    # Timeout exceptions
    "ConnectTimeout",
    "ReadTimeout",
    "WriteTimeout",
    "PoolTimeout",
    # Network exceptions
    "ConnectError",
    "ReadError",
    "WriteError",
    "CloseError",
    # Protocol exceptions
    "LocalProtocolError",
    "RemoteProtocolError",
    # Other transport/request exceptions
    "UnsupportedProtocol",
    "ProxyError",
    "TooManyRedirects",
    "HTTPStatusError",
    "DecodingError",
    # Stream exceptions
    "StreamConsumed",
    "ResponseNotRead",
    "RequestNotRead",
    "StreamClosed",
    # Other exceptions
    "InvalidURL",
    "CookieConflict",
]
