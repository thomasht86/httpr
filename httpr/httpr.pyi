from __future__ import annotations

import sys
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

class Response:
    @property
    def content(self) -> bytes: ...
    @property
    def cookies(self) -> dict[str, str]: ...
    @property
    def headers(self) -> dict[str, str]: ...
    @property
    def status_code(self) -> int: ...
    @property
    def url(self) -> str: ...
    @property
    def encoding(self) -> str: ...
    @property
    def text(self) -> str: ...
    def json(self) -> Any: ...
    @property
    def text_markdown(self) -> str: ...
    @property
    def text_plain(self) -> str: ...
    @property
    def text_rich(self) -> str: ...

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
    def headers(self, headers: dict[str, str]) -> None: ...
    @property
    def cookies(self) -> dict[str, str]: ...
    @cookies.setter
    def cookies(self, cookies: dict[str, str]) -> None: ...
    @property
    def proxy(self) -> str | None: ...
    @proxy.setter
    def proxy(self, proxy: str) -> None: ...
    def request(self, method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def get(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def head(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def options(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def delete(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def post(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def put(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...
    def patch(self, url: str, **kwargs: Unpack[RequestParams]) -> Response: ...

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
