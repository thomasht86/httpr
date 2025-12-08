# Quickstart

This guide will get you up and running with httpr in minutes.

## Installation

=== "uv (recommended)"

    ```bash
    uv add httpr
    ```

=== "pip"

    ```bash
    pip install httpr
    ```

## Your First Request

The simplest way to make a request is using the module-level functions:

```python
import httpr

response = httpr.get("https://httpbin.org/get")
print(response.status_code)  # 200
print(response.json())
```

httpr provides functions for all common HTTP methods:

```python
import httpr

# GET
response = httpr.get("https://httpbin.org/get")

# POST
response = httpr.post("https://httpbin.org/post", json={"key": "value"})

# PUT
response = httpr.put("https://httpbin.org/put", json={"key": "value"})

# PATCH
response = httpr.patch("https://httpbin.org/patch", json={"key": "value"})

# DELETE
response = httpr.delete("https://httpbin.org/delete")

# HEAD
response = httpr.head("https://httpbin.org/get")

# OPTIONS
response = httpr.options("https://httpbin.org/get")
```

## Using a Client

For multiple requests, use a `Client` instance. This provides connection pooling and allows you to configure default settings:

```python
import httpr

# Create a client
client = httpr.Client()

# Make multiple requests
response1 = client.get("https://httpbin.org/get")
response2 = client.post("https://httpbin.org/post", json={"key": "value"})

# Always close when done (or use context manager)
client.close()
```

### Context Manager (Recommended)

Use the context manager to ensure the client is properly closed:

```python
import httpr

with httpr.Client() as client:
    response = client.get("https://httpbin.org/get")
    print(response.json())
# Client is automatically closed here
```

## Query Parameters

Add query parameters using the `params` argument:

```python
import httpr

# These are equivalent:
response = httpr.get("https://httpbin.org/get?name=httpr&version=1")
response = httpr.get("https://httpbin.org/get", params={"name": "httpr", "version": "1"})

print(response.json()["args"])  # {"name": "httpr", "version": "1"}
```

Numeric parameters are automatically converted to strings:

```python
import httpr

response = httpr.get("https://httpbin.org/get", params={"page": 1, "limit": 10})
print(response.json()["args"])  # {"page": "1", "limit": "10"}
```

## Request Headers

Set custom headers using the `headers` argument:

```python
import httpr

response = httpr.get(
    "https://httpbin.org/headers",
    headers={
        "X-Custom-Header": "my-value",
        "Accept": "application/json"
    }
)
print(response.json()["headers"]["X-Custom-Header"])  # "my-value"
```

## Sending Data

### JSON Data

Send JSON data using the `json` argument:

```python
import httpr

response = httpr.post(
    "https://httpbin.org/post",
    json={"name": "httpr", "version": 1, "fast": True}
)
print(response.json()["json"])  # {"name": "httpr", "version": 1, "fast": true}
```

### Form Data

Send form-encoded data using the `data` argument:

```python
import httpr

response = httpr.post(
    "https://httpbin.org/post",
    data={"username": "user", "password": "secret"}
)
print(response.json()["form"])  # {"username": "user", "password": "secret"}
```

### Binary Data

Send raw bytes using the `content` argument:

```python
import httpr

response = httpr.post(
    "https://httpbin.org/post",
    content=b"raw binary data"
)
print(response.json()["data"])  # "raw binary data"
```

### File Uploads

Upload files using the `files` argument:

```python
import httpr

response = httpr.post(
    "https://httpbin.org/post",
    files={
        "document": "/path/to/file.txt",
        "image": "/path/to/image.png"
    }
)
```

!!! note
    The `files` argument takes a dictionary mapping field names to file paths.

## Response Handling

The response object provides several ways to access the response data:

```python
import httpr

response = httpr.get("https://httpbin.org/get")

# Status code
print(response.status_code)  # 200

# Response body as text
print(response.text)

# Response body as bytes
print(response.content)

# Parse JSON response
data = response.json()

# Response headers (case-insensitive)
print(response.headers["content-type"])
print(response.headers["Content-Type"])  # Same result

# Response cookies
print(response.cookies)

# Final URL (after redirects)
print(response.url)

# Detected encoding
print(response.encoding)
```

### HTML to Text Conversion

httpr can convert HTML responses to plain text or markdown:

```python
import httpr

response = httpr.get("https://example.com")

# Convert HTML to Markdown
print(response.text_markdown)

# Convert HTML to plain text
print(response.text_plain)

# Convert HTML to rich text
print(response.text_rich)
```

## Timeouts

Set a timeout in seconds to limit how long to wait for a response:

```python
import httpr

# Request-level timeout
response = httpr.get("https://httpbin.org/delay/1", timeout=5)

# Client-level default timeout
client = httpr.Client(timeout=10)
response = client.get("https://httpbin.org/get")

# Override client timeout for specific request
response = client.get("https://httpbin.org/delay/5", timeout=30)
```

## Redirects

By default, httpr follows redirects automatically:

```python
import httpr

# Follows redirects by default
response = httpr.get("https://httpbin.org/redirect/3")
print(response.url)  # Final URL after redirects

# Disable redirects
client = httpr.Client(follow_redirects=False)

# Limit number of redirects
client = httpr.Client(max_redirects=5)
```

## What's Next?

- **[Tutorial](tutorial/index.md)**: Learn httpr step by step
- **[Authentication](tutorial/authentication.md)**: Basic auth, bearer tokens
- **[Async Client](tutorial/async.md)**: Async/await support
- **[SSL/TLS](advanced/ssl-tls.md)**: Certificate configuration, mTLS
- **[API Reference](api/index.md)**: Complete API documentation
