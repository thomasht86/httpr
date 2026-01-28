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
from collections.abc import AsyncIterator, Generator, Iterator, MutableMapping
from contextlib import asynccontextmanager, contextmanager
from functools import partial
from typing import TYPE_CHECKING, TypedDict

if sys.version_info <= (3, 11):
    from typing_extensions import Unpack
else:
    from typing import Unpack


from .httpr import CaseInsensitiveHeaderMap, RClient, Response, StreamingResponse


class CaseInsensitiveDict(MutableMapping):
    """Case-insensitive dict for HTTP headers. Keys stored as lowercase.

    When bound to a client, mutations automatically sync back to the client.
    """

    __slots__ = ("_store", "_client")

    def __init__(
        self,
        data: dict[str, str] | None = None,
        *,
        _client: RClient | None = None,
        **kwargs: str,
    ) -> None:
        self._store: dict[str, str] = {}
        self._client = _client
        if data:
            for key, value in data.items():
                self._store[key.lower()] = value
        for key, value in kwargs.items():
            self._store[key.lower()] = value

    def _sync_to_client(self) -> None:
        """Push current state back to the bound client."""
        if self._client is not None:
            RClient.headers.__set__(self._client, dict(self._store))  # type: ignore[attr-defined]

    def __getitem__(self, key: str) -> str:
        return self._store[key.lower()]

    def __setitem__(self, key: str, value: str) -> None:
        self._store[key.lower()] = value
        self._sync_to_client()

    def __delitem__(self, key: str) -> None:
        del self._store[key.lower()]
        self._sync_to_client()

    def __iter__(self) -> Iterator[str]:
        return iter(self._store)

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and key.lower() in self._store

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CaseInsensitiveDict):
            return self._store == other._store
        if isinstance(other, dict):
            return self._store == {k.lower(): v for k, v in other.items()}
        return NotImplemented

    def __repr__(self) -> str:
        return f"CaseInsensitiveDict({self._store!r})"

    def copy(self) -> CaseInsensitiveDict:
        """Return an unbound copy of this dict."""
        return CaseInsensitiveDict(self._store.copy())

    def lower_items(self) -> Iterator[tuple[str, str]]:
        """Iterator of (lowercase_key, value) - requests compatibility."""
        return iter(self._store.items())

    def clear(self) -> None:
        """Remove all items."""
        self._store.clear()
        self._sync_to_client()

    def pop(self, key: str, *args: str) -> str:  # type: ignore[override]
        """Remove and return value for key."""
        lowered = key.lower()
        had_key = lowered in self._store
        result = self._store.pop(lowered, *args)
        if had_key:
            self._sync_to_client()
        return result

    def popitem(self) -> tuple[str, str]:
        """Remove and return an arbitrary (key, value) pair."""
        result = self._store.popitem()
        self._sync_to_client()
        return result

    def setdefault(self, key: str, default: str = "") -> str:  # type: ignore[override]
        """Set key to default if not present, return value."""
        lowered = key.lower()
        if lowered not in self._store:
            self._store[lowered] = default
            self._sync_to_client()
        return self._store[lowered]

    def update(  # type: ignore[override]
        self, other: dict[str, str] | list[tuple[str, str]] | None = None, /, **kwargs: str
    ) -> None:
        """Update from dict and/or kwargs."""
        changed = False
        if other is not None:
            if hasattr(other, "items"):
                for k, v in other.items():  # type: ignore[union-attr]
                    self._store[k.lower()] = v
                    changed = True
            else:
                for k, v in other:  # type: ignore[union-attr]
                    self._store[k.lower()] = v
                    changed = True
        for k, v in kwargs.items():
            self._store[k.lower()] = v
            changed = True
        if changed:
            self._sync_to_client()


if TYPE_CHECKING:
    from .httpr import ClientRequestParams, HttpMethod, RequestParams
else:

    class _Unpack:
        @staticmethod
        def __getitem__(*args, **kwargs):
            pass

    Unpack = _Unpack()
    RequestParams = ClientRequestParams = TypedDict


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
        client_pem_data: bytes | None = None,
        https_only: bool | None = False,
        http2_only: bool | None = False,
    ):
        """
        Initialize an HTTP client.

        Args:
            auth: Basic auth credentials as (username, password). Password can be None.
            auth_bearer: Bearer token for Authorization header.
            params: Default query parameters to include in all requests.
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

    @property  # type: ignore[override]
    def headers(self) -> CaseInsensitiveDict:
        """Default headers (case-insensitive, mutations sync to client). Cookie header excluded."""
        return CaseInsensitiveDict(RClient.headers.__get__(self), _client=self)

    @headers.setter
    def headers(self, value: dict[str, str] | CaseInsensitiveDict | None) -> None:
        if isinstance(value, CaseInsensitiveDict):
            RClient.headers.__set__(self, dict(value._store))  # type: ignore[attr-defined]
        else:
            RClient.headers.__set__(self, value)  # type: ignore[attr-defined]

    def __enter__(self) -> Client:
        """Enter context manager."""
        return self

    def __exit__(self, *args):
        """Exit context manager and close client."""
        del self

    def close(self) -> None:
        """
        Close the client and release resources.

        Example:
            ```python
            client = httpr.Client()
            try:
                response = client.get("https://example.com")
            finally:
                client.close()
            ```
        """
        del self

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
            params (Optional[dict[str, str]]): Query parameters to append to URL.
            headers (Optional[dict[str, str]]): Request headers (merged with client defaults).
            cookies (Optional[dict[str, str]]): Request cookies (merged with client defaults).
            auth (Optional[tuple[str, Optional[str]]]): Basic auth credentials (overrides client default).
            auth_bearer (Optional[str]): Bearer token (overrides client default).
            timeout (Optional[float]): Request timeout in seconds (overrides client default).
            content (Optional[bytes]): Raw bytes for request body.
            data (Optional[dict[str, Any]]): Form data for request body (application/x-www-form-urlencoded).
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
        if "params" in kwargs and kwargs["params"] is not None:
            kwargs["params"] = {k: str(v) for k, v in kwargs["params"].items()}

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
        if "params" in kwargs and kwargs["params"] is not None:
            kwargs["params"] = {k: str(v) for k, v in kwargs["params"].items()}

        response = super()._stream(method=method, url=url, **kwargs)
        try:
            yield response
        finally:
            response.close()


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
        native async I/O.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize an async HTTP client.

        Accepts the same parameters as Client.
        """
        super().__init__(*args, **kwargs)

    async def __aenter__(self) -> AsyncClient:
        """Enter async context manager."""
        return self

    async def __aexit__(self, *args):
        """Exit async context manager and close client."""
        del self

    async def aclose(self):
        """
        Close the async client.

        Example:
            ```python
            client = httpr.AsyncClient()
            try:
                response = await client.get("https://example.com")
            finally:
                await client.aclose()
            ```
        """
        del self
        return

    async def _run_sync_asyncio(self, fn, *args, **kwargs):
        """Run a synchronous function in an executor."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(fn, *args, **kwargs))

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
        if "params" in kwargs and kwargs["params"] is not None:
            kwargs["params"] = {k: str(v) for k, v in kwargs["params"].items()}

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
    ) -> AsyncIterator[StreamingResponse]:
        """
        Make an async streaming HTTP request.

        Returns an async context manager that yields a StreamingResponse for
        iterating over the response body in chunks.

        Args:
            method: HTTP method.
            url: Request URL.
            **kwargs: Request parameters.

        Yields:
            StreamingResponse: A response object that can be iterated.

        Example:
            ```python
            async with client.stream("GET", "https://example.com/large-file") as response:
                for chunk in response.iter_bytes():
                    process(chunk)
            ```

        Note:
            Iteration over the response is synchronous (uses iter_bytes, iter_text,
            iter_lines). The async part is initiating the request and entering
            the context manager.
        """
        if method not in ["GET", "HEAD", "OPTIONS", "DELETE", "POST", "PUT", "PATCH"]:
            raise ValueError(f"Unsupported HTTP method: {method}")
        if "params" in kwargs and kwargs["params"] is not None:
            kwargs["params"] = {k: str(v) for k, v in kwargs["params"].items()}

        # Run the sync _stream in executor
        response = await self._run_sync_asyncio(super(Client, self)._stream, method=method, url=url, **kwargs)
        try:
            yield response
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
    "CaseInsensitiveDict",
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
    "InvalidURL",
    "CookieConflict",
]
