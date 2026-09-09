"""
httpr - Blazing fast HTTP client for Python, built in Rust.

httpr is a high-performance HTTP client that can be used as a drop-in replacement
for `httpx` and `requests` in most cases.

Example:
    Simple GET request:

    ```python
    import httpr

    response = httpr.get("https://httpbin.org/get")
    print(response.json())
    ```

    Using a client for connection pooling:

    ```python
    import httpr

    with httpr.Client() as client:
        response = client.get("https://httpbin.org/get")
        print(response.status_code)
    ```
"""

from __future__ import annotations

import asyncio
import sys
from collections.abc import AsyncIterator, Generator, Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager, contextmanager
from functools import partial
from typing import TYPE_CHECKING, TypedDict, TypeVar

if sys.version_info <= (3, 11):
    from typing_extensions import Unpack
else:
    from typing import Unpack


from .httpr import (
    _CLIENT_CLOSED_MSG,
    CaseInsensitiveHeaderMap,
    ClientClosed,
    RClient,
    Response,
    StreamingResponse,
)

#: Default number of requests an :class:`AsyncClient` keeps in flight. Threads are
#: created lazily, so an idle client costs nothing.
DEFAULT_MAX_CONCURRENCY = 64

_T = TypeVar("_T")


class CaseInsensitiveDict(dict[str, str]):
    """A dict subclass that provides case-insensitive key access."""

    def __getitem__(self, key: str) -> str:
        return super().__getitem__(key.lower())

    def __setitem__(self, key: str, value: str) -> None:
        super().__setitem__(key.lower(), value)

    def __delitem__(self, key: str) -> None:
        super().__delitem__(key.lower())

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False
        return super().__contains__(key.lower())

    def get(self, key: str, default: str | None = None) -> str | None:  # type: ignore[override]
        return super().get(key.lower(), default)

    def pop(self, key: str, *args: str) -> str:  # type: ignore[override]
        return super().pop(key.lower(), *args)

    def setdefault(self, key: str, default: str | None = None) -> str | None:  # type: ignore[override]
        return super().setdefault(key.lower(), default)  # type: ignore[arg-type]

    def update(self, other: dict[str, str] | None = None, **kwargs: str) -> None:  # type: ignore[override]
        if other is not None:
            super().update({k.lower(): v for k, v in other.items()})
        if kwargs:
            super().update({k.lower(): v for k, v in kwargs.items()})


class _ClientHeaders(CaseInsensitiveDict):
    """Case-insensitive headers view that writes changes back to the client."""

    def __init__(self, client: RClient, data: dict[str, str]) -> None:
        self._client = client
        super().__init__(data)

    def __setitem__(self, key: str, value: str) -> None:
        super().__setitem__(key, value)
        self._client.set_header(key, value)

    def __delitem__(self, key: str) -> None:
        super().__delitem__(key)
        self._client.del_header(key)

    def pop(self, key: str, *args: str) -> str:  # type: ignore[override]
        existed = key in self
        result = super().pop(key, *args)
        if existed:
            self._client.del_header(key)
        return result

    def popitem(self) -> tuple[str, str]:
        key, value = super().popitem()
        self._client.del_header(key)
        return key, value

    def setdefault(self, key: str, default: str | None = None) -> str | None:  # type: ignore[override]
        existed = key in self
        result = super().setdefault(key, default)
        if not existed and result is not None:
            self._client.set_header(key, result)
        return result

    def update(self, other: dict[str, str] | None = None, **kwargs: str) -> None:  # type: ignore[override]
        other = dict(other) if other is not None else None
        super().update(other, **kwargs)
        if other:
            for k, v in other.items():
                self._client.set_header(k, v)
        for k, v in kwargs.items():
            self._client.set_header(k, v)

    def clear(self) -> None:
        keys = list(self.keys())
        super().clear()
        for k in keys:
            self._client.del_header(k)


if TYPE_CHECKING:
    from .httpr import ClientRequestParams, HttpMethod, QueryParamTypes, RequestParams
else:

    class _Unpack:
        @staticmethod
        def __getitem__(*args, **kwargs):
            pass

    Unpack = _Unpack()
    RequestParams = ClientRequestParams = TypedDict
    QueryParamTypes = dict


class Client(RClient):
    """
    A synchronous HTTP client with connection pooling.

    The Client class provides a high-level interface for making HTTP requests.
    It supports connection pooling, automatic cookie handling, and various
    authentication methods.

    Example:
        Basic usage:

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

        With configuration:

        ```python
        import httpr

        client = httpr.Client(
            auth_bearer="your-api-token",
            headers={"User-Agent": "my-app/1.0"},
            timeout=30,
        )
        ```

    Attributes:
        headers: Default headers sent with all requests. Excludes Cookie header.
        cookies: Default cookies sent with all requests.
        auth: Basic auth credentials as (username, password) tuple.
        params: Default query parameters added to all requests, as a dict; a key
            given more than once maps to a list of values.
        timeout: Default timeout in seconds.
        proxy: Proxy URL for requests.
    """

    def __init__(
        self,
        auth: tuple[str, str | None] | None = None,
        auth_bearer: str | None = None,
        params: QueryParamTypes | None = None,
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
        client_pem_data: bytes | None = None,
        https_only: bool | None = False,
        http2_only: bool | None = False,
    ):
        """
        Initialize an HTTP client.

        Args:
            auth: Basic auth credentials as (username, password). Password can be None.
            auth_bearer: Bearer token for Authorization header.
            params: Default query parameters to include in all requests. Merged with
                each request's own `params`; a key the request supplies wins. Values
                may be str, int, float, bool (sent as `true`/`false`), None (sent
                empty) or a list/tuple of those (the key is repeated).
            headers: Default headers to send with all requests.
            cookies: Default cookies to send with all requests.
            cookie_store: Enable persistent cookie store. Cookies from responses will be
                preserved and included in subsequent requests. Default is True.
            referer: Automatically set Referer header. Default is True.
            proxy: Proxy URL (e.g., "http://proxy:8080" or "socks5://127.0.0.1:1080").
                Falls back to HTTPR_PROXY environment variable.
            timeout: Request timeout in seconds. Default is 30.
            follow_redirects: Follow HTTP redirects. Default is True.
            max_redirects: Maximum redirects to follow. Default is 20.
            verify: Verify SSL certificates. Default is True.
            ca_cert_file: Path to CA certificate bundle (PEM format).
            client_pem: Path to client certificate for mTLS (PEM format).
            client_pem_data: Client certificate and key as bytes for mTLS (PEM format).
                Use this instead of client_pem when you have the certificate in memory.
            https_only: Only allow HTTPS requests. Default is False.
            http2_only: Use HTTP/2 only (False uses HTTP/1.1). Default is False.

        Example:
            ```python
            import httpr

            # Simple client
            client = httpr.Client()

            # Client with authentication
            client = httpr.Client(
                auth=("username", "password"),
                timeout=60,
            )

            # Client with bearer token
            client = httpr.Client(
                auth_bearer="your-api-token",
                headers={"Accept": "application/json"},
            )

            # Client with proxy
            client = httpr.Client(proxy="http://proxy.example.com:8080")

            # Client with mTLS using file path
            client = httpr.Client(
                client_pem="/path/to/client.pem",
                ca_cert_file="/path/to/ca.pem",
            )

            # Client with mTLS using direct certificate data
            cert_data = b"-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----"
            client = httpr.Client(
                client_pem_data=cert_data,
                ca_cert_file="/path/to/ca.pem",
            )
            ```
        """
        super().__init__()

    def __enter__(self) -> Client:
        """Enter context manager."""
        return self

    def __exit__(self, *args):
        """Exit context manager and close client."""
        self.close()

    def close(self) -> None:
        """
        Close the client and release its connection pool.

        Idle pooled connections are shut down before this returns. Requests
        that are already in flight (including open `stream()` responses) finish
        normally and keep the pool alive until the last of them completes, at
        which point it is released. Any request made after `close()` raises
        `httpr.ClientClosed` (a `RuntimeError`, as in httpx). Calling `close()`
        more than once is a no-op.

        Example:
            ```python
            client = httpr.Client()
            try:
                response = client.get("https://example.com")
            finally:
                client.close()
            ```
        """
        super().close()

    @property
    def headers(self) -> dict[str, str]:
        """Headers configured for this client (case-insensitive, live view).

        Mutating the returned mapping in place (e.g. ``client.headers["Accept"] =
        "application/json"``) updates the client. Cookies are never affected.
        """
        return _ClientHeaders(self, super().headers)

    @headers.setter
    def headers(self, value: dict[str, str] | None) -> None:
        RClient.headers.__set__(self, value)  # type: ignore[attr-defined]

    def request(
        self,
        method: HttpMethod,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """
        Make an HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS).
            url: Request URL.
            **kwargs: Request parameters (see below).

        Keyword Args:
            params (Optional[QueryParamTypes]): Query parameters to append to the URL, merged
                with the client's (the request wins for a key both supply). Values may be
                str, int, float, bool (sent as `true`/`false`), None (sent empty) or a
                list/tuple of those, which repeats the key.
            headers (Optional[dict[str, str]]): Request headers (merged with client defaults).
            cookies (Optional[dict[str, str]]): Request cookies, merged with the client's into a
                single `Cookie` header (the request wins for a name both supply).
            auth (Optional[tuple[str, Optional[str]]]): Basic auth credentials (overrides client default).
            auth_bearer (Optional[str]): Bearer token (overrides client default).
            timeout (Optional[float]): Request timeout in seconds (overrides client default).
            content (Optional[bytes]): Raw bytes for request body.
            data (Optional[dict[str, Any]]): Form data for request body (application/x-www-form-urlencoded).
                Values are converted like `params`; a list/tuple repeats the field.
            json (Optional[Any]): JSON data for request body (application/json).
            files (Optional[dict[str, str]]): Files for multipart upload (dict mapping field names to file paths).

        Returns:
            Response object with status, headers, and body.

        Raises:
            ValueError: If method is not a valid HTTP method.
            Exception: If request fails (timeout, connection error, etc.).

        Example:
            ```python
            response = client.request("GET", "https://httpbin.org/get")
            response = client.request("POST", "https://httpbin.org/post", json={"key": "value"})
            ```

        Note:
            Only one of `content`, `data`, `json`, or `files` can be specified per request.
        """
        if method not in ["GET", "HEAD", "OPTIONS", "DELETE", "POST", "PUT", "PATCH"]:
            raise ValueError(f"Unsupported HTTP method: {method}")
        return super().request(method=method, url=url, **kwargs)

    def get(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Make a GET request.

        Args:
            url: Request URL.
            **kwargs: Request parameters (params, headers, cookies, auth, auth_bearer, timeout).

        Returns:
            Response object.

        Example:
            ```python
            response = client.get(
                "https://httpbin.org/get",
                params={"key": "value"},
                headers={"Accept": "application/json"},
            )
            print(response.json())
            ```
        """
        return self.request(method="GET", url=url, **kwargs)

    def head(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Make a HEAD request.

        Returns only headers, no response body.

        Args:
            url: Request URL.
            **kwargs: Request parameters (params, headers, cookies, auth, auth_bearer, timeout).

        Returns:
            Response object (body will be empty).

        Example:
            ```python
            response = client.head("https://httpbin.org/get")
            print(response.headers["content-length"])
            ```
        """
        return self.request(method="HEAD", url=url, **kwargs)

    def options(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Make an OPTIONS request.

        Args:
            url: Request URL.
            **kwargs: Request parameters (params, headers, cookies, auth, auth_bearer, timeout).

        Returns:
            Response object.

        Example:
            ```python
            response = client.options("https://httpbin.org/get")
            print(response.headers.get("allow"))
            ```
        """
        return self.request(method="OPTIONS", url=url, **kwargs)

    def delete(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Make a DELETE request.

        Args:
            url: Request URL.
            **kwargs: Request parameters (params, headers, cookies, auth, auth_bearer, timeout).

        Returns:
            Response object.

        Example:
            ```python
            response = client.delete("https://httpbin.org/delete")
            print(response.status_code)
            ```
        """
        return self.request(method="DELETE", url=url, **kwargs)

    def post(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Make a POST request.

        Args:
            url: Request URL.
            **kwargs: Request parameters including body options.

        Keyword Args:
            params (Optional[dict[str, str]]): Query parameters.
            headers (Optional[dict[str, str]]): Request headers.
            cookies (Optional[dict[str, str]]): Request cookies.
            auth (Optional[tuple[str, Optional[str]]]): Basic auth credentials.
            auth_bearer (Optional[str]): Bearer token.
            timeout (Optional[float]): Request timeout.
            content (Optional[bytes]): Raw bytes body.
            data (Optional[dict[str, Any]]): Form-encoded body.
            json (Optional[Any]): JSON body.
            files (Optional[dict[str, str]]): Multipart file uploads.

        Returns:
            Response object.

        Example:
            ```python
            # JSON body
            response = client.post(
                "https://httpbin.org/post",
                json={"name": "httpr", "fast": True},
            )

            # Form data
            response = client.post(
                "https://httpbin.org/post",
                data={"username": "user", "password": "pass"},
            )

            # File upload
            response = client.post(
                "https://httpbin.org/post",
                files={"document": "/path/to/file.pdf"},
            )
            ```
        """
        return self.request(method="POST", url=url, **kwargs)

    def put(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Make a PUT request.

        Args:
            url: Request URL.
            **kwargs: Request parameters including body options.

        Returns:
            Response object.

        Example:
            ```python
            response = client.put(
                "https://httpbin.org/put",
                json={"key": "updated_value"},
            )
            ```
        """
        return self.request(method="PUT", url=url, **kwargs)

    def patch(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        """
        Make a PATCH request.

        Args:
            url: Request URL.
            **kwargs: Request parameters including body options.

        Returns:
            Response object.

        Example:
            ```python
            response = client.patch(
                "https://httpbin.org/patch",
                json={"field": "new_value"},
            )
            ```
        """
        return self.request(method="PATCH", url=url, **kwargs)

    @contextmanager
    def stream(
        self,
        method: HttpMethod,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Generator[StreamingResponse, None, None]:
        """
        Make a streaming HTTP request.

        Returns a context manager that yields a StreamingResponse for iterating
        over the response body in chunks without buffering the entire response
        in memory.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS).
            url: Request URL.
            **kwargs: Request parameters (same as request()).

        Yields:
            StreamingResponse: A response object that can be iterated to receive chunks.

        Example:
            Basic streaming:

            ```python
            with client.stream("GET", "https://example.com/large-file") as response:
                for chunk in response.iter_bytes():
                    process(chunk)
            ```

            Streaming text:

            ```python
            with client.stream("GET", "https://example.com/text") as response:
                for text in response.iter_text():
                    print(text, end="")
            ```

            Streaming lines (e.g., Server-Sent Events):

            ```python
            with client.stream("GET", "https://example.com/events") as response:
                for line in response.iter_lines():
                    print(line.strip())
            ```

            Conditional reading:

            ```python
            with client.stream("GET", url) as response:
                if response.status_code == 200:
                    content = response.read()  # Read all remaining content
                else:
                    pass  # Don't read the body
            ```

        Note:
            The response body is only read when you iterate over it or call read().
            Always use this as a context manager to ensure proper cleanup.
        """
        if method not in ["GET", "HEAD", "OPTIONS", "DELETE", "POST", "PUT", "PATCH"]:
            raise ValueError(f"Unsupported HTTP method: {method}")
        response = super()._stream(method=method, url=url, **kwargs)
        try:
            yield response
        finally:
            response.close()


class AsyncStreamingResponse:
    """
    The streaming response yielded by `AsyncClient.stream()`.

    Wraps the `StreamingResponse` produced by the Rust core and adds async
    iteration: `aiter_bytes()`, `aiter_text()`, `aiter_lines()` and `aread()`
    fetch each chunk on the client's thread pool, so the event loop keeps
    running other tasks while the server is producing the next one. Status,
    headers, cookies and URL are available as soon as the context manager is
    entered, before any of the body has been read.

    The synchronous `iter_bytes()`, `iter_text()`, `iter_lines()` and `read()`
    are still available, but each step blocks the event loop for as long as the
    server takes to send the next chunk; use the async variants in async code.

    Example:
        ```python
        async with client.stream("GET", "https://example.com/events") as response:
            async for line in response.aiter_lines():
                handle(line)
        ```
    """

    __slots__ = ("_client", "_response")

    def __init__(self, response: StreamingResponse, client: AsyncClient) -> None:
        self._response = response
        self._client = client

    # -- Metadata, available before the body is read ---------------------------

    @property
    def status_code(self) -> int:
        """HTTP status code."""
        return self._response.status_code

    @property
    def reason_phrase(self) -> str:
        """Canonical reason phrase for the status code (e.g. "OK")."""
        return self._response.reason_phrase

    @property
    def headers(self) -> CaseInsensitiveHeaderMap:
        """Response headers (case-insensitive access)."""
        return self._response.headers

    @property
    def cookies(self) -> dict[str, str]:
        """Response cookies."""
        return self._response.cookies

    @property
    def url(self) -> str:
        """Final URL after any redirects."""
        return self._response.url

    @property
    def is_informational(self) -> bool:
        """True for 1xx status codes."""
        return self._response.is_informational

    @property
    def is_success(self) -> bool:
        """True for 2xx status codes."""
        return self._response.is_success

    @property
    def is_redirect(self) -> bool:
        """True for 3xx status codes."""
        return self._response.is_redirect

    @property
    def is_client_error(self) -> bool:
        """True for 4xx status codes."""
        return self._response.is_client_error

    @property
    def is_server_error(self) -> bool:
        """True for 5xx status codes."""
        return self._response.is_server_error

    @property
    def is_error(self) -> bool:
        """True for 4xx and 5xx status codes."""
        return self._response.is_error

    @property
    def has_redirect_location(self) -> bool:
        """True for 3xx responses that carry a `Location` header."""
        return self._response.has_redirect_location

    @property
    def is_closed(self) -> bool:
        """Whether the stream has been closed."""
        return self._response.is_closed

    @property
    def is_consumed(self) -> bool:
        """Whether the stream has been fully consumed."""
        return self._response.is_consumed

    def raise_for_status(self) -> AsyncStreamingResponse:
        """Raise `HTTPStatusError` on a non-2xx status; returns self on success."""
        self._response.raise_for_status()
        return self

    # -- Async body access -----------------------------------------------------

    async def _aiter(self, it: Iterator[_T]) -> AsyncIterator[_T]:
        # Each `next()` does a blocking read on the Rust side, so it goes through
        # the client's executor like a request does. `_run_sync_asyncio` maps a
        # closed client to ClientClosed.
        sentinel: object = object()
        while True:
            item = await self._client._run_sync_asyncio(next, it, sentinel)
            if item is sentinel:
                return
            yield item

    def aiter_bytes(self) -> AsyncIterator[bytes]:
        """
        Iterate over the response body as bytes chunks without blocking the event loop.

        Example:
            ```python
            async for chunk in response.aiter_bytes():
                process(chunk)
            ```
        """
        return self._aiter(self._response.iter_bytes())

    def aiter_text(self) -> AsyncIterator[str]:
        """Iterate over the response body as text chunks, decoded with the response encoding."""
        return self._aiter(self._response.iter_text())

    def aiter_lines(self) -> AsyncIterator[str]:
        """
        Iterate over the response body line by line, e.g. for Server-Sent Events.

        Example:
            ```python
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    handle(line[5:].strip())
            ```
        """
        return self._aiter(self._response.iter_lines())

    def __aiter__(self) -> AsyncIterator[bytes]:
        """`async for chunk in response` is the same as `aiter_bytes()`."""
        return self.aiter_bytes()

    async def aread(self) -> bytes:
        """Read the entire remaining response body without blocking the event loop."""
        return await self._client._run_sync_asyncio(self._response.read)

    async def aclose(self) -> None:
        """
        Close the streaming response and release its connection.

        `AsyncClient.stream()` calls this when the `async with` block exits.
        Closing never waits on I/O, so it runs on the event-loop thread.
        """
        self._response.close()

    # -- Synchronous body access (blocks the event loop) -----------------------

    def iter_bytes(self) -> Iterator[bytes]:
        """Synchronous `aiter_bytes()`; blocks the event loop while waiting for chunks."""
        return self._response.iter_bytes()

    def iter_text(self) -> Iterator[str]:
        """Synchronous `aiter_text()`; blocks the event loop while waiting for chunks."""
        return self._response.iter_text()

    def iter_lines(self) -> Iterator[str]:
        """Synchronous `aiter_lines()`; blocks the event loop while waiting for chunks."""
        return self._response.iter_lines()

    def __iter__(self) -> Iterator[bytes]:
        return self._response.iter_bytes()

    def read(self) -> bytes:
        """Synchronous `aread()`; blocks the event loop until the body has arrived."""
        return self._response.read()

    def close(self) -> None:
        """Synchronous `aclose()`."""
        self._response.close()


class AsyncClient(Client):
    """
    An asynchronous HTTP client for use with asyncio.

    AsyncClient wraps the synchronous Client using asyncio.run_in_executor(),
    providing an async interface while leveraging the Rust implementation's
    performance.

    Example:
        Basic usage:

        ```python
        import asyncio
        import httpr

        async def main():
            async with httpr.AsyncClient() as client:
                response = await client.get("https://httpbin.org/get")
                print(response.json())

        asyncio.run(main())
        ```

        Concurrent requests:

        ```python
        import asyncio
        import httpr

        async def main():
            async with httpr.AsyncClient() as client:
                tasks = [
                    client.get("https://httpbin.org/get"),
                    client.get("https://httpbin.org/ip"),
                ]
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    print(response.json())

        asyncio.run(main())
        ```

    Note:
        AsyncClient runs synchronous Rust code in a thread executor.
        It provides concurrency benefits for I/O-bound tasks but is not
        native async I/O. `max_concurrency` sizes that executor and therefore
        caps how many requests can be in flight at once.
    """

    def __new__(cls, *args, max_concurrency: int | None = None, **kwargs):
        # Client inherits from the Rust-backed RClient, whose __new__ consumes the
        # constructor keyword arguments, so max_concurrency has to be stripped here
        # as well as in __init__.
        return super().__new__(cls, *args, **kwargs)

    def __init__(
        self,
        *args,
        max_concurrency: int | None = DEFAULT_MAX_CONCURRENCY,
        **kwargs,
    ):
        """
        Initialize an async HTTP client.

        Accepts the same parameters as Client, plus:

        Args:
            max_concurrency: Maximum number of requests in flight at once, i.e. the
                size of this client's thread pool. Defaults to 64. Threads are
                created lazily, so an idle client costs nothing. Pass ``None`` to
                dispatch on asyncio's default executor instead -- note that this
                shares a pool with `asyncio.to_thread` and every other
                ``run_in_executor(None)`` caller in the application, and that
                CPython sizes it at ``min(32, cpu_count + 4)``.
        """
        super().__init__(*args, **kwargs)
        self.max_concurrency = max_concurrency
        # Threads are created on demand; `close()`/`aclose()` shut the pool down.
        self._executor = (
            None
            if max_concurrency is None
            else ThreadPoolExecutor(max_workers=max_concurrency, thread_name_prefix="httpr")
        )

    async def __aenter__(self) -> AsyncClient:
        """Enter async context manager."""
        return self

    async def __aexit__(self, *args):
        """Exit async context manager and close client."""
        await self.aclose()

    def close(self) -> None:
        """
        Close the client synchronously.

        Releases the connection pool and shuts down this client's thread pool.
        Prefer `aclose()` from async code; this exists so `AsyncClient` honours
        the `Client` contract too.
        """
        super().close()
        if self._executor is not None:
            # Requests still running on the pool keep their handle to the reqwest
            # client and finish normally; queued ones raise ClientClosed when they
            # run. Not waiting keeps this safe to call from the event-loop thread.
            self._executor.shutdown(wait=False)

    async def aclose(self) -> None:
        """
        Close the async client.

        Releases the connection pool and shuts down this client's thread pool.
        Any request made after `aclose()` raises `httpr.ClientClosed`. Calling it
        more than once is a no-op.

        Example:
            ```python
            client = httpr.AsyncClient()
            try:
                response = await client.get("https://example.com")
            finally:
                await client.aclose()
            ```
        """
        # Runs on the event-loop thread on purpose: closing never waits on I/O
        # (pending connects are cancelled, not awaited) and takes well under a
        # millisecond, less than a hop through the executor would cost.
        self.close()

    async def _run_sync_asyncio(self, fn, *args, **kwargs):
        """Run a synchronous function on this client's executor."""
        if self.is_closed:
            # Checked here rather than left to the Rust side so a closed client
            # raises ClientClosed instead of the executor's own "cannot schedule
            # new futures after shutdown" RuntimeError.
            raise ClientClosed(_CLIENT_CLOSED_MSG)
        loop = asyncio.get_running_loop()
        try:
            future = loop.run_in_executor(self._executor, partial(fn, *args, **kwargs))
        except RuntimeError:
            # The executor is only ever shut down by close()/aclose(), so if one
            # landed between the check above and submit (from another thread),
            # report it as the client being closed rather than leaking the
            # executor's own error.
            if self.is_closed:
                raise ClientClosed(_CLIENT_CLOSED_MSG) from None
            raise
        return await future

    async def request(  # type: ignore[override]
        self,
        method: HttpMethod,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """
        Make an async HTTP request.

        Args:
            method: HTTP method.
            url: Request URL.
            **kwargs: Request parameters.

        Returns:
            Response object.

        Example:
            ```python
            response = await client.request("GET", "https://httpbin.org/get")
            ```
        """
        if method not in ["GET", "HEAD", "OPTIONS", "DELETE", "POST", "PUT", "PATCH"]:
            raise ValueError(f"Unsupported HTTP method: {method}")
        return await self._run_sync_asyncio(super().request, method=method, url=url, **kwargs)

    async def get(  # type: ignore[override]
        self,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """
        Make an async GET request.

        Args:
            url: Request URL.
            **kwargs: Request parameters.

        Returns:
            Response object.

        Example:
            ```python
            response = await client.get("https://httpbin.org/get")
            ```
        """
        return await self.request(method="GET", url=url, **kwargs)

    async def head(  # type: ignore[override]
        self,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """
        Make an async HEAD request.

        Args:
            url: Request URL.
            **kwargs: Request parameters.

        Returns:
            Response object.
        """
        return await self.request(method="HEAD", url=url, **kwargs)

    async def options(  # type: ignore[override]
        self,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """
        Make an async OPTIONS request.

        Args:
            url: Request URL.
            **kwargs: Request parameters.

        Returns:
            Response object.
        """
        return await self.request(method="OPTIONS", url=url, **kwargs)

    async def delete(  # type: ignore[override]
        self,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """
        Make an async DELETE request.

        Args:
            url: Request URL.
            **kwargs: Request parameters.

        Returns:
            Response object.
        """
        return await self.request(method="DELETE", url=url, **kwargs)

    async def post(  # type: ignore[override]
        self,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """
        Make an async POST request.

        Args:
            url: Request URL.
            **kwargs: Request parameters including body options.

        Returns:
            Response object.

        Example:
            ```python
            response = await client.post(
                "https://httpbin.org/post",
                json={"key": "value"},
            )
            ```
        """
        return await self.request(method="POST", url=url, **kwargs)

    async def put(  # type: ignore[override]
        self,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """
        Make an async PUT request.

        Args:
            url: Request URL.
            **kwargs: Request parameters including body options.

        Returns:
            Response object.
        """
        return await self.request(method="PUT", url=url, **kwargs)

    async def patch(  # type: ignore[override]
        self,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> Response:
        """
        Make an async PATCH request.

        Args:
            url: Request URL.
            **kwargs: Request parameters including body options.

        Returns:
            Response object.
        """
        return await self.request(method="PATCH", url=url, **kwargs)

    @asynccontextmanager
    async def stream(  # type: ignore[override]
        self,
        method: HttpMethod,
        url: str,
        **kwargs: Unpack[RequestParams],
    ) -> AsyncIterator[AsyncStreamingResponse]:
        """
        Make an async streaming HTTP request.

        Returns an async context manager that yields an `AsyncStreamingResponse`
        for iterating over the response body in chunks. Status, headers and
        cookies are available as soon as the block is entered; the body is
        read as you iterate.

        Args:
            method: HTTP method.
            url: Request URL.
            **kwargs: Request parameters.

        Yields:
            AsyncStreamingResponse: A response object that can be iterated with
            `async for`.

        Example:
            ```python
            async with client.stream("GET", "https://example.com/large-file") as response:
                async for chunk in response.aiter_bytes():
                    process(chunk)

            async with client.stream("GET", "https://example.com/events") as response:
                async for line in response.aiter_lines():
                    handle(line)
            ```

        Note:
            `aiter_bytes()`, `aiter_text()`, `aiter_lines()` and `aread()` read
            each chunk on the client's thread pool, so other tasks keep running
            while the server is producing data. The synchronous `iter_*()` and
            `read()` methods are still available but block the event loop.
        """
        if method not in ["GET", "HEAD", "OPTIONS", "DELETE", "POST", "PUT", "PATCH"]:
            raise ValueError(f"Unsupported HTTP method: {method}")
        # Run the sync _stream in executor
        response = await self._run_sync_asyncio(super(Client, self)._stream, method=method, url=url, **kwargs)
        try:
            yield AsyncStreamingResponse(response, self)
        finally:
            response.close()


def request(
    method: HttpMethod,
    url: str,
    verify: bool | None = True,
    ca_cert_file: str | None = None,
    client_pem: str | None = None,
    client_pem_data: bytes | None = None,
    **kwargs: Unpack[RequestParams],
) -> Response:
    """
    Make an HTTP request using a temporary client.

    This is a convenience function for one-off requests. For multiple requests,
    use a Client instance for better performance (connection pooling).

    Args:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS).
        url: Request URL.
        verify: Verify SSL certificates. Default is True.
        ca_cert_file: Path to CA certificate bundle.
        client_pem: Path to client certificate for mTLS.
        client_pem_data: Client certificate and key as bytes for mTLS.
        **kwargs: Additional request parameters.

    Returns:
        Response object.

    Example:
        ```python
        import httpr

        response = httpr.request("GET", "https://httpbin.org/get")
        response = httpr.request("POST", "https://httpbin.org/post", json={"key": "value"})
        ```
    """
    with Client(
        verify=verify,
        ca_cert_file=ca_cert_file,
        client_pem=client_pem,
        client_pem_data=client_pem_data,
    ) as client:
        return client.request(method, url, **kwargs)


def get(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response:
    """
    Make a GET request using a temporary client.

    Args:
        url: Request URL.
        **kwargs: Request parameters (params, headers, cookies, auth, timeout, etc.).

    Returns:
        Response object.

    Example:
        ```python
        import httpr

        response = httpr.get("https://httpbin.org/get", params={"key": "value"})
        print(response.json())
        ```
    """
    return request(method="GET", url=url, **kwargs)


def head(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response:
    """
    Make a HEAD request using a temporary client.

    Args:
        url: Request URL.
        **kwargs: Request parameters.

    Returns:
        Response object (body will be empty).

    Example:
        ```python
        import httpr

        response = httpr.head("https://httpbin.org/get")
        print(response.headers)
        ```
    """
    return request(method="HEAD", url=url, **kwargs)


def options(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response:
    """
    Make an OPTIONS request using a temporary client.

    Args:
        url: Request URL.
        **kwargs: Request parameters.

    Returns:
        Response object.

    Example:
        ```python
        import httpr

        response = httpr.options("https://httpbin.org/get")
        ```
    """
    return request(method="OPTIONS", url=url, **kwargs)


def delete(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response:
    """
    Make a DELETE request using a temporary client.

    Args:
        url: Request URL.
        **kwargs: Request parameters.

    Returns:
        Response object.

    Example:
        ```python
        import httpr

        response = httpr.delete("https://httpbin.org/delete")
        ```
    """
    return request(method="DELETE", url=url, **kwargs)


def post(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response:
    """
    Make a POST request using a temporary client.

    Args:
        url: Request URL.
        **kwargs: Request parameters (json, data, content, files, etc.).

    Returns:
        Response object.

    Example:
        ```python
        import httpr

        # JSON body
        response = httpr.post("https://httpbin.org/post", json={"key": "value"})

        # Form data
        response = httpr.post("https://httpbin.org/post", data={"field": "value"})
        ```
    """
    return request(method="POST", url=url, **kwargs)


def put(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response:
    """
    Make a PUT request using a temporary client.

    Args:
        url: Request URL.
        **kwargs: Request parameters.

    Returns:
        Response object.

    Example:
        ```python
        import httpr

        response = httpr.put("https://httpbin.org/put", json={"key": "value"})
        ```
    """
    return request(method="PUT", url=url, **kwargs)


def patch(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response:
    """
    Make a PATCH request using a temporary client.

    Args:
        url: Request URL.
        **kwargs: Request parameters.

    Returns:
        Response object.

    Example:
        ```python
        import httpr

        response = httpr.patch("https://httpbin.org/patch", json={"field": "new_value"})
        ```
    """
    return request(method="PATCH", url=url, **kwargs)


# Import exceptions from the Rust module
from .httpr import (  # noqa: E402
    CloseError,
    # Network exceptions
    ConnectError,
    # Timeout exceptions
    ConnectTimeout,
    CookieConflict,
    DecodingError,
    # Base exceptions
    HTTPError,
    HTTPStatusError,
    # Other exceptions
    InvalidURL,
    # Protocol exceptions
    LocalProtocolError,
    NetworkError,
    PoolTimeout,
    ProtocolError,
    ProxyError,
    ReadError,
    ReadTimeout,
    RemoteProtocolError,
    RequestError,
    RequestNotRead,
    ResponseNotRead,
    StreamClosed,
    # Stream exceptions
    StreamConsumed,
    StreamError,
    TimeoutException,
    TooManyRedirects,
    TransportError,
    # Other transport/request exceptions
    UnsupportedProtocol,
    WriteError,
    WriteTimeout,
)

__all__ = [
    # Client and request functions
    "Client",
    "AsyncClient",
    "request",
    "get",
    "head",
    "options",
    "delete",
    "post",
    "put",
    "patch",
    # Response classes
    "Response",
    "StreamingResponse",
    "AsyncStreamingResponse",
    "CaseInsensitiveHeaderMap",
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
    # Other exceptions
    "UnsupportedProtocol",
    "ProxyError",
    "TooManyRedirects",
    "HTTPStatusError",
    "DecodingError",
    "StreamConsumed",
    "ResponseNotRead",
    "RequestNotRead",
    "StreamClosed",
    # Client lifecycle exceptions
    "ClientClosed",
    "InvalidURL",
    "CookieConflict",
]
