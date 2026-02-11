# API Reference

Complete API documentation for httpr.

## Overview

httpr provides a simple, intuitive API for making HTTP requests:

| Component                                                                     | Description                                     |
| ----------------------------------------------------------------------------- | ----------------------------------------------- |
| [`Client`](https://thomasht86.github.io/httpr/api/client/index.md)            | Synchronous HTTP client with connection pooling |
| [`AsyncClient`](https://thomasht86.github.io/httpr/api/async-client/index.md) | Asynchronous HTTP client for asyncio            |
| [`Response`](https://thomasht86.github.io/httpr/api/response/index.md)        | HTTP response with body, headers, and metadata  |
| [Module Functions](https://thomasht86.github.io/httpr/api/functions/index.md) | Convenience functions for one-off requests      |

## Quick Reference

### Client Configuration

```python
import httpr

client = httpr.Client(
    # Authentication
    auth=("username", "password"),    # Basic auth
    auth_bearer="token",              # Bearer token

    # Request defaults
    headers={"User-Agent": "my-app"},
    cookies={"session": "abc"},
    params={"api_version": "v2"},
    timeout=30,

    # Cookie handling
    cookie_store=True,                # Persistent cookies
    referer=True,                     # Auto Referer header

    # Network
    proxy="http://proxy:8080",
    follow_redirects=True,
    max_redirects=20,

    # SSL/TLS
    verify=True,
    ca_cert_file="/path/to/ca.pem",
    client_pem="/path/to/client.pem", # mTLS

    # Protocol
    https_only=False,
    http2_only=False,
)
```

### Request Parameters

```python
response = client.get(
    "https://api.example.com/data",
    params={"key": "value"},          # Query params
    headers={"Accept": "application/json"},
    cookies={"session": "xyz"},
    auth=("user", "pass"),            # Override client auth
    auth_bearer="token",              # Or bearer token
    timeout=60,                       # Override timeout
)

response = client.post(
    "https://api.example.com/data",
    json={"key": "value"},            # JSON body
    # OR
    data={"field": "value"},          # Form body
    # OR
    content=b"raw bytes",             # Binary body
    # OR
    files={"doc": "/path/to/file"},   # Multipart upload
)
```

### Response Object

```python
response = client.get("https://api.example.com")

# Status
response.status_code      # int: 200, 404, etc.

# Body
response.text             # str: decoded text
response.content          # bytes: raw bytes
response.json()           # Any: parsed JSON

# Headers & Cookies
response.headers          # dict-like, case-insensitive
response.cookies          # dict[str, str]

# Metadata
response.url              # str: final URL (after redirects)
response.encoding         # str: detected encoding

# HTML conversion
response.text_markdown    # HTML to Markdown
response.text_plain       # HTML to plain text
```

## Module Contents

httpr - Blazing fast HTTP client for Python, built in Rust.

httpr is a high-performance HTTP client that can be used as a drop-in replacement for `httpx` and `requests` in most cases.

Example

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
