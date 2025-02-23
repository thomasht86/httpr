# httpr

**Blazing fast http-client** for Python in Rust 🦀 that can be used as drop-in replacement for `httpx` in most cases.

- **Fast**: httpr is built on top of `reqwests` which is a blazing fast http client in Rust. Check out the [benchmark](#benchmark).
- **Both async and sync**: httpr provides both a sync and async client.
- **Lightweight**: httpr is a lightweight http client with 0 python-dependencies.
- **Async**: first-class support for async/await. 
- **http2**: httpr supports http2.
- **mTLS**: httpr supports mTLS.
- **Zero python dependencies**: httpr is a pure rust library with no python dependencies.

## Table of Contents

- [httpr](#httpr)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Install with uv](#install-with-uv)
    - [Install from PyPI](#install-from-pypi)
  - [Benchmark](#benchmark)
  - [Usage](#usage)
    - [I. Client](#i-client)
      - [Client methods](#client-methods)
      - [Response object](#response-object)
      - [Examples](#examples)
    - [II. AsyncClient](#ii-asyncclient)
  - [Precompiled wheels](#precompiled-wheels)
  - [Acknowledgements](#acknowledgements)

## Installation

### Install with uv

```python
uv add httpr
```

or

```python
uv pip install httpr
```

### Install from PyPI

```python
pip install -U httpr
```

## Benchmark

![](https://github.com/thomasht86/httpr/blob/main/benchmark.jpg?raw=true)

## Usage

### I. Client

```python
class Client:
    """Initializes an HTTP client.

    Args:
        auth (tuple[str, str| None] | None): Username and password for basic authentication. Default is None.
        auth_bearer (str | None): Bearer token for authentication. Default is None.
        params (dict[str, str] | None): Default query parameters to include in all requests. Default is None.
        headers (dict[str, str] | None): Default headers to send with requests. 
        cookies (dict[str, str] | None): - Map of cookies to send with requests as the `Cookie` header.
        timeout (float | None): HTTP request timeout in seconds. Default is 30.
        cookie_store (bool | None): Enable a persistent cookie store. Received cookies will be preserved and included
            in additional requests. Default is True.
        referer (bool | None): Enable or disable automatic setting of the `Referer` header. Default is True.
        proxy (str | None): Proxy URL for HTTP requests. Example: "socks5://127.0.0.1:9150". Default is None.
        follow_redirects (bool | None): Whether to follow redirects. Default is True.
        max_redirects (int | None): Maximum redirects to follow. Default 20. Applies if `follow_redirects` is True.
        verify (bool | None): Verify SSL certificates. Default is True.
        ca_cert_file (str | None): Path to CA certificate store. Default is None.
        https_only` (bool | None): Restrict the Client to be used with HTTPS only requests. Default is `false`.
        http2_only` (bool | None): If true - use only HTTP/2; if false - use only HTTP/1. Default is `false`.

    """
```

#### Client methods

The `Client` class provides a set of methods for making HTTP requests: `get`, `head`, `options`, `delete`, `post`, `put`, `patch`, each of which internally utilizes the `request()` method for execution. The parameters for these methods closely resemble those in `httpx`.
```python
def get(
    url: str,
    params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    cookies: dict[str, str] | None = None,
    auth: tuple[str, str| None] | None = None,
    auth_bearer: str | None = None,
    timeout: float | None = 30,
):
    """Performs a GET request to the specified URL.

    Args:
        url (str): The URL to which the request will be made.
        params (dict[str, str] | None): A map of query parameters to append to the URL. Default is None.
        headers (dict[str, str] | None): A map of HTTP headers to send with the request. Default is None.
        cookies (dict[str, str] | None): - An optional map of cookies to send with requests as the `Cookie` header.
        auth (tuple[str, str| None] | None): A tuple containing the username and an optional password
            for basic authentication. Default is None.
        auth_bearer (str | None): A string representing the bearer token for bearer token authentication. Default is None.
        timeout (float | None): The timeout for the request in seconds. Default is 30.

    """
```
```python
def post(
    url: str,
    params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    cookies: dict[str, str] | None = None,
    content: bytes | None = None,
    data: dict[str, Any] | None = None,
    json: Any | None = None,
    files: dict[str, str] | None = None,
    auth: tuple[str, str| None] | None = None,
    auth_bearer: str | None = None,
    timeout: float | None = 30,
):
    """Performs a POST request to the specified URL.

    Args:
        url (str): The URL to which the request will be made.
        params (dict[str, str] | None): A map of query parameters to append to the URL. Default is None.
        headers (dict[str, str] | None): A map of HTTP headers to send with the request. Default is None.
        cookies (dict[str, str] | None): - An optional map of cookies to send with requests as the `Cookie` header.
        content (bytes | None): The content to send in the request body as bytes. Default is None.
        data (dict[str, Any] | None): The form data to send in the request body. Default is None.
        json (Any | None): A JSON serializable object to send in the request body. Default is None.
        files (dict[str, str] | None): A map of file fields to file paths to be sent as multipart/form-data. Default is None.
        auth (tuple[str, str| None] | None): A tuple containing the username and an optional password
            for basic authentication. Default is None.
        auth_bearer (str | None): A string representing the bearer token for bearer token authentication. Default is None.
        timeout (float | None): The timeout for the request in seconds. Default is 30.

    """
```

#### Response object

The `Client` class returns a `Response` object that contains the following attributes and methods:

```python
resp.content
resp.cookies
resp.encoding
resp.headers
resp.json()
resp.status_code
resp.text
resp.text_markdown  # html is converted to markdown text using html2text-rs
resp.text_plain  # html is converted to plain text
resp.text_rich  # html is converted to rich text
resp.url
```

#### Examples

```python
import httpr

# Initialize the client
client = httpr.Client() 

# GET request
resp = client.get("https://tls.peet.ws/api/all")
print(resp.json())

# GET request with passing params and setting timeout
params = {"param1": "value1", "param2": "value2"}
resp = client.post(url="https://httpbin.org/anything", params=params, timeout=10)
print(r.text)

# POST Binary Request Data
content = b"some_data"
resp = client.post(url="https://httpbin.org/anything", content=content)
print(r.text)

# POST Form Encoded Data
data = {"key1": "value1", "key2": "value2"}
resp = client.post(url="https://httpbin.org/anything", data=data)
print(r.text)

# POST JSON Encoded Data
json = {"key1": "value1", "key2": "value2"}
resp = client.post(url="https://httpbin.org/anything", json=json)
print(r.text)

# POST Multipart-Encoded Files
files = {'file1': '/home/root/file1.txt', 'file2': 'home/root/file2.txt'}
r = client.post("https://httpbin.org/post", files=files)
print(r.text)

# Authentication using user/password
auth = ("user", "password")
resp = client.post(url="https://httpbin.org/anything", auth=auth)
print(r.text)

# Authentication using auth bearer
auth_bearer = "bearerXXXXXXXXXXXXXXXXXXXX"
resp = client.post(url="https://httpbin.org/anything", auth_bearer=auth_bearer)
print(r.text)

# Using proxy or env var HTTPR_PROXY
resp = httpr.Client(proxy="http://127.0.0.1:8080").get("https://tls.peet.ws/api/all")
print(resp.json())
export HTTPR_PROXY="socks5://127.0.0.1:1080"
resp = httpr.Client().get("https://tls.peet.ws/api/all")
print(resp.json())

# Using custom CA certificate store: env var HTTPR_CA_BUNDLE
resp = httpr.Client(ca_cert_file="/cert/cacert.pem").get("https://tls.peet.ws/api/all")
print(resp.json())
resp = httpr.Client(ca_cert_file=certifi.where()).get("https://tls.peet.ws/api/all")
print(resp.json())
export HTTPR_CA_BUNDLE="/home/user/Downloads/cert.pem"
resp = httpr.Client().get("https://tls.peet.ws/api/all")
print(resp.json())

# You can also use convenience functions that use a default Client instance under the hood:
# httpr.get() | httpr.head() | httpr.options() | httpr.delete() | httpr.post() | httpr.patch() | httpr.put()
resp = httpr.get("https://httpbin.org/anything")
print(r.text)
```

### II. AsyncClient

`httpr.AsyncClient()` is an asynchronous wrapper around the `httpr.Client` class, offering the same functions, behavior, and input arguments.

```python
import asyncio
import logging

import httpr

async def aget_text(url):
    async with httpr.AsyncClient() as client:
        resp = await client.get(url)
        return resp.text

async def main():
    urls = ["https://nytimes.com/", "https://cnn.com/", "https://abcnews.go.com/"]
    tasks = [aget_text(u) for u in urls]
    results = await asyncio.gather(*tasks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
```

## Precompiled wheels

Provides precompiled wheels for the following platforms:

- 🐧 linux: `amd64`, `aarch64`, `armv7` (aarch64 and armv7 builds are `manylinux_2_34` compatible. `ubuntu>=22.04`, `debian>=12`)
- 🐧 musllinux: `amd64`, `aarch64`
- 🪟 windows: `amd64`
- 🍏 macos: `amd64`, `aarch64`.
  
## Acknowledgements

- [PRIMP](https://github.com/deedy5/primp): *A lot* of code is borrowed from PRIMP, that wraps rust library `rquest` for python in a similar way.
- [reqwests](https://github.com/seanmonstar/reqwest): The rust library that powers httpr.
- [pyo3](https://github.com/PyO3/pyo3)
- [maturin](https://github.com/PyO3/maturin)