---
hide:
  - navigation
  - toc
---

# httpr

<p style="font-size: 1.3rem; color: #666;">
<strong>Blazing fast HTTP client</strong> for Python, built in Rust.
</p>

<p>
<a href="https://pypi.org/project/httpr/"><img src="https://img.shields.io/pypi/v/httpr.svg" alt="PyPI version"></a>
<a href="https://pypi.org/project/httpr/"><img src="https://img.shields.io/pypi/pyversions/httpr.svg" alt="Python versions"></a>
<a href="https://github.com/thomasht86/httpr/blob/main/LICENSE"><img src="https://img.shields.io/github/license/thomasht86/httpr.svg" alt="License"></a>
</p>

---

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

---

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Fast**

    ---

    Built on Rust's `reqwest` - one of the fastest HTTP clients available.
    See the [benchmarks](https://github.com/thomasht86/httpr#benchmark).

-   :material-swap-horizontal:{ .lg .middle } **Sync & Async**

    ---

    Both synchronous `Client` and `AsyncClient` with identical APIs.
    First-class async support.

-   :material-feather:{ .lg .middle } **Lightweight**

    ---

    Zero Python dependencies. Everything is implemented in Rust.
    Just install and use.

-   :material-shield-check:{ .lg .middle } **Secure**

    ---

    Full SSL/TLS support including mTLS (mutual TLS) for
    enterprise authentication.

-   :material-protocol:{ .lg .middle } **HTTP/2**

    ---

    Native HTTP/2 support for better performance with
    multiplexed connections.

-   :material-cookie:{ .lg .middle } **Cookie Store**

    ---

    Automatic cookie handling with persistent cookie store
    across requests.

</div>

---

## Installation

=== "uv (recommended)"

    ```bash
    uv add httpr
    ```

=== "pip"

    ```bash
    pip install httpr
    ```

---

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

---

## Features

-   :material-water:{ .lg .middle } **Streaming**

    ---

    Stream large responses efficiently without buffering entire
    response in memory. Iterate bytes, text, or lines.

## Not Yet Implemented

- **Fine-grained error handling**: Detailed error types are in development

---

## LLM-Friendly Documentation

This documentation is available in LLM-optimized formats:

- **[llms.txt](/llms.txt)** - Documentation index for LLMs
- **[llms-full.txt](/llms-full.txt)** - Complete documentation in a single file

---

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Learn**

    ---

    New to httpr? Start with the [Quickstart](quickstart.md) guide.

    [:octicons-arrow-right-24: Quickstart](quickstart.md)

-   :material-school:{ .lg .middle } **Tutorial**

    ---

    Step-by-step guides covering all features.

    [:octicons-arrow-right-24: Tutorial](tutorial/index.md)

-   :material-cog:{ .lg .middle } **Advanced**

    ---

    SSL/TLS, proxies, cookies, and more.

    [:octicons-arrow-right-24: Advanced](advanced/index.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete API documentation.

    [:octicons-arrow-right-24: API Reference](api/index.md)

</div>
