# httpr

**Blazing fast HTTP client** for Python, built in Rust.

______________________________________________________________________

**httpr** is a drop-in replacement for `httpx` and `requests` with significantly better performance. Built on top of Rust's `reqwest` library with zero Python dependencies.

```python
import httpr

# Simple as requests
response = httpr.get("https://httpbin.org/get")
print(response.json())

# Or use a client for connection pooling
with httpr.Client() as client:
    response = client.get("https://httpbin.org/get")
    print(response.status_code)  # 200
```

______________________________________________________________________

- **Fast**

  ______________________________________________________________________

  Built on Rust's `reqwest` - one of the fastest HTTP clients available. See the [benchmarks](https://github.com/thomasht86/httpr#benchmark).

- **Sync & Async**

  ______________________________________________________________________

  Both synchronous `Client` and `AsyncClient` with identical APIs. First-class async support.

- **Lightweight**

  ______________________________________________________________________

  Zero Python dependencies. Everything is implemented in Rust. Just install and use.

- **Secure**

  ______________________________________________________________________

  Full SSL/TLS support including mTLS (mutual TLS) for enterprise authentication.

- **HTTP/2**

  ______________________________________________________________________

  Native HTTP/2 support for better performance with multiplexed connections.

- **Cookie Store**

  ______________________________________________________________________

  Automatic cookie handling with persistent cookie store across requests.

______________________________________________________________________

## Installation

```bash
uv add httpr
```

```bash
pip install httpr
```

______________________________________________________________________

## Quick Example

```python
import httpr

# Create a client with default settings
client = httpr.Client(
    timeout=30,
    follow_redirects=True,
)

# Make requests
response = client.get("https://httpbin.org/get", params={"key": "value"})
print(response.status_code)  # 200
print(response.json())       # {"args": {"key": "value"}, ...}

# POST with JSON
response = client.post(
    "https://httpbin.org/post",
    json={"name": "httpr", "fast": True}
)

# Response properties
print(response.text)         # Response body as text
print(response.content)      # Response body as bytes
print(response.headers)      # Response headers (case-insensitive)
print(response.cookies)      # Response cookies
```

______________________________________________________________________

## Features

- **Streaming**

  ______________________________________________________________________

  Stream large responses efficiently without buffering entire response in memory. Iterate bytes, text, or lines.

## Not Yet Implemented

- **Fine-grained error handling**: Detailed error types are in development

______________________________________________________________________

## LLM-Friendly Documentation

This documentation is available in LLM-optimized formats:

- **[llms.txt](https://thomasht86.github.io/httpr/llms.txt)** - Documentation index for LLMs
- **[llms-full.txt](https://thomasht86.github.io/httpr/llms-full.txt)** - Complete documentation in a single file

______________________________________________________________________

- **Learn**

  ______________________________________________________________________

  New to httpr? Start with the [Quickstart](https://thomasht86.github.io/httpr/quickstart/index.md) guide.

  [Quickstart](https://thomasht86.github.io/httpr/quickstart/index.md)

- **Tutorial**

  ______________________________________________________________________

  Step-by-step guides covering all features.

  [Tutorial](https://thomasht86.github.io/httpr/tutorial/index.md)

- **Advanced**

  ______________________________________________________________________

  SSL/TLS, proxies, cookies, and more.

  [Advanced](https://thomasht86.github.io/httpr/advanced/index.md)

- **API Reference**

  ______________________________________________________________________

  Complete API documentation.

  [API Reference](https://thomasht86.github.io/httpr/api/index.md)
