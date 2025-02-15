from __future__ import annotations

import asyncio
import sys
from functools import partial
from typing import TYPE_CHECKING, TypedDict

if sys.version_info <= (3, 11):
    from typing_extensions import Unpack
else:
    from typing import Unpack


from .httpr import RClient

if TYPE_CHECKING:
    from .httpr import ClientRequestParams, HttpMethod, RequestParams, Response
else:

    class _Unpack:
        @staticmethod
        def __getitem__(*args, **kwargs):
            pass

    Unpack = _Unpack()
    RequestParams = ClientRequestParams = TypedDict


class Client(RClient):
    """Initializes an HTTP client"""

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
        # http2_only: bool | None = False,
    ):
        """
        Args:
            auth: a tuple containing the username and an optional password for basic authentication. Default is None.
            auth_bearer: a string representing the bearer token for bearer token authentication. Default is None.
            params: a map of query parameters to append to the URL. Default is None.
            headers: an optional map of HTTP headers to send with requests. Ignored if `impersonate` is set.
            cookies: an optional map of cookies to send with requests as the `Cookie` header.
            cookie_store: enable a persistent cookie store. Received cookies will be preserved and included
                 in additional requests. Default is True.
            referer: automatic setting of the `Referer` header. Default is True.
            proxy: proxy URL for HTTP requests, example: "socks5://127.0.0.1:9150". Default is None.
            timeout: timeout for HTTP requests in seconds. Default is 30.
            follow_redirects: a boolean to enable or disable following redirects. Default is True.
            max_redirects: the maximum number of redirects if `follow_redirects` is True. Default is 20.
            verify: an optional boolean indicating whether to verify SSL certificates. Default is True.
            ca_cert_file: path to CA certificate store. Default is None.
            client_pem: path to client certificate file. Default is None.
            https_only: restrict the Client to be used with HTTPS only requests. Default is False.
            http2_only: if true - use only HTTP/2, if false - use only HTTP/1. Default is False.
        """
        super().__init__()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *args):
        del self

    def request(self, method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        return super().request(method=method, url=url, **kwargs)

    def get(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        return self.request(method="GET", url=url, **kwargs)

    def head(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        return self.request(method="HEAD", url=url, **kwargs)

    def options(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        return self.request(method="OPTIONS", url=url, **kwargs)

    def delete(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        return self.request(method="DELETE", url=url, **kwargs)

    def post(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        return self.request(method="POST", url=url, **kwargs)

    def put(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        return self.request(method="PUT", url=url, **kwargs)

    def patch(self, url: str, **kwargs: Unpack[RequestParams]) -> Response:
        return self.request(method="PATCH", url=url, **kwargs)


class AsyncClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __aenter__(self) -> AsyncClient:
        return self

    async def __aexit__(self, *args):
        del self

    async def _run_sync_asyncio(self, fn, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(fn, *args, **kwargs))

    async def request(self, method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]):  # type: ignore
        return await self._run_sync_asyncio(super().request, method=method, url=url, **kwargs)

    async def get(self, url: str, **kwargs: Unpack[RequestParams]):  # type: ignore
        return await self.request(method="GET", url=url, **kwargs)

    async def head(self, url: str, **kwargs: Unpack[RequestParams]):  # type: ignore
        return await self.request(method="HEAD", url=url, **kwargs)

    async def options(self, url: str, **kwargs: Unpack[RequestParams]):  # type: ignore
        return await self.request(method="OPTIONS", url=url, **kwargs)

    async def delete(self, url: str, **kwargs: Unpack[RequestParams]):  # type: ignore
        return await self.request(method="DELETE", url=url, **kwargs)

    async def post(self, url: str, **kwargs: Unpack[RequestParams]):  # type: ignore
        return await self.request(method="POST", url=url, **kwargs)

    async def put(self, url: str, **kwargs: Unpack[RequestParams]):  # type: ignore
        return await self.request(method="PUT", url=url, **kwargs)

    async def patch(self, url: str, **kwargs: Unpack[RequestParams]):  # type: ignore
        return await self.request(method="PATCH", url=url, **kwargs)


def request(
    method: HttpMethod,
    url: str,
    verify: bool | None = True,
    ca_cert_file: str | None = None,
    client_pem: str | None = None,
    **kwargs: Unpack[RequestParams],
):
    """
    Args:
        method: the HTTP method to use (e.g., "GET", "POST").
        url: the URL to which the request will be made.
        verify: an optional boolean indicating whether to verify SSL certificates. Default is True.
        ca_cert_file: path to CA certificate store. Default is None.
        client_pem: path to client certificate file. Default is None.
        auth: a tuple containing the username and an optional password for basic authentication. Default is None.
        auth_bearer: a string representing the bearer token for bearer token authentication. Default is None.
        params: a map of query parameters to append to the URL. Default is None.
        headers: an optional map of HTTP headers to send with requests. If `impersonate` is set, this will be ignored.
        cookies: an optional map of cookies to send with requests as the `Cookie` header.
        timeout: the timeout for the request in seconds. Default is 30.
        content: the content to send in the request body as bytes. Default is None.
        data: the form data to send in the request body. Default is None.
        json: a JSON serializable object to send in the request body. Default is None.
        files: a map of file fields to file paths to be sent as multipart/form-data. Default is None.
    """
    with Client(
        verify=verify,
        ca_cert_file=ca_cert_file,
        client_pem=client_pem,
    ) as client:
        return client.request(method, url, **kwargs)


def get(url: str, **kwargs: Unpack[ClientRequestParams]):
    return request(method="GET", url=url, **kwargs)


def head(url: str, **kwargs: Unpack[ClientRequestParams]):
    return request(method="HEAD", url=url, **kwargs)


def options(url: str, **kwargs: Unpack[ClientRequestParams]):
    return request(method="OPTIONS", url=url, **kwargs)


def delete(url: str, **kwargs: Unpack[ClientRequestParams]):
    return request(method="DELETE", url=url, **kwargs)


def post(url: str, **kwargs: Unpack[ClientRequestParams]):
    return request(method="POST", url=url, **kwargs)


def put(url: str, **kwargs: Unpack[ClientRequestParams]):
    return request(method="PUT", url=url, **kwargs)


def patch(url: str, **kwargs: Unpack[ClientRequestParams]):
    return request(method="PATCH", url=url, **kwargs)
