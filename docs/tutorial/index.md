# Tutorial

Welcome to the httpr tutorial! This guide will take you through all the features of httpr step by step.

## What You'll Learn

This tutorial is organized into sections that build on each other:

<div class="grid cards" markdown>

-   :material-send:{ .lg .middle } **Making Requests**

    ---

    Learn how to make HTTP requests with different methods, headers, and data.

    [:octicons-arrow-right-24: Making Requests](making-requests.md)

-   :material-download:{ .lg .middle } **Response Handling**

    ---

    Work with response data, headers, cookies, and status codes.

    [:octicons-arrow-right-24: Response Handling](response-handling.md)

-   :material-key:{ .lg .middle } **Authentication**

    ---

    Use Basic Auth, Bearer tokens, and other authentication methods.

    [:octicons-arrow-right-24: Authentication](authentication.md)

-   :material-lightning-bolt:{ .lg .middle } **Async Client**

    ---

    Use async/await for concurrent requests.

    [:octicons-arrow-right-24: Async Client](async.md)

</div>

## Prerequisites

Before starting, make sure you have httpr installed:

```bash
uv add httpr
# or
pip install httpr
```

Verify the installation:

```python
import httpr
print(httpr.__version__ if hasattr(httpr, '__version__') else "httpr installed!")
```

## Module-Level Functions vs Client

httpr provides two ways to make requests:

### Module-Level Functions

For quick, one-off requests:

```python
import httpr

response = httpr.get("https://httpbin.org/get")
```

Each call creates a new client internally, which is convenient but not efficient for multiple requests.

### Client Instance

For applications making multiple requests:

```python
import httpr

with httpr.Client() as client:
    response1 = client.get("https://httpbin.org/get")
    response2 = client.get("https://httpbin.org/ip")
```

Benefits of using a `Client`:

- **Connection pooling**: Reuses connections for better performance
- **Default configuration**: Set headers, auth, timeout once
- **Cookie persistence**: Cookies are automatically stored and sent
- **Resource management**: Proper cleanup with context manager

## Next Steps

Start with [Making Requests](making-requests.md) to learn the basics of sending HTTP requests.
