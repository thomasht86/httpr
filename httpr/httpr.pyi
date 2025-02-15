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
