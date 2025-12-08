# API Reference

Complete API documentation for httpr.

## Overview

httpr provides a simple, intuitive API for making HTTP requests:

| Component | Description |
|-----------|-------------|
| [`Client`](client.md) | Synchronous HTTP client with connection pooling |
| [`AsyncClient`](async-client.md) | Asynchronous HTTP client for asyncio |
| [`Response`](response.md) | HTTP response with body, headers, and metadata |
| [Module Functions](functions.md) | Convenience functions for one-off requests |

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

::: httpr
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members: false
      show_docstring_description: true
