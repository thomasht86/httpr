# Making Requests

This guide covers everything you need to know about making HTTP requests with httpr.

## HTTP Methods

httpr supports all standard HTTP methods:

```python
import httpr

client = httpr.Client()

# GET - Retrieve data
response = client.get("https://httpbin.org/get")

# POST - Create/submit data
response = client.post("https://httpbin.org/post", json={"key": "value"})

# PUT - Update/replace data
response = client.put("https://httpbin.org/put", json={"key": "value"})

# PATCH - Partial update
response = client.patch("https://httpbin.org/patch", json={"key": "value"})

# DELETE - Remove data
response = client.delete("https://httpbin.org/delete")

# HEAD - Get headers only (no body)
response = client.head("https://httpbin.org/get")

# OPTIONS - Get supported methods
response = client.options("https://httpbin.org/get")
```

You can also use the generic `request()` method:

```python
import httpr

client = httpr.Client()
response = client.request("GET", "https://httpbin.org/get")
response = client.request("POST", "https://httpbin.org/post", json={"key": "value"})
```

## Query Parameters

Add query parameters to the URL using the `params` argument:

```python
import httpr

# Using params dict
response = httpr.get(
    "https://httpbin.org/get",
    params={"search": "python", "page": 1, "limit": 10}
)

# Result: https://httpbin.org/get?search=python&page=1&limit=10
print(response.json()["args"])
# {"search": "python", "page": "1", "limit": "10"}
```

!!! note "Automatic String Conversion"
    All parameter values are automatically converted to strings. Numbers, booleans, and other types work seamlessly.

### Default Parameters

Set default query parameters on the client that are included in every request:

```python
import httpr

# API key included in all requests
client = httpr.Client(params={"api_key": "your-api-key"})

response = client.get("https://api.example.com/users")
# URL: https://api.example.com/users?api_key=your-api-key

response = client.get("https://api.example.com/posts", params={"page": 1})
# URL: https://api.example.com/posts?api_key=your-api-key&page=1
```

## Request Headers

Set custom headers for individual requests or as client defaults:

### Per-Request Headers

```python
import httpr

response = httpr.get(
    "https://httpbin.org/headers",
    headers={
        "X-Custom-Header": "my-value",
        "Accept": "application/json",
        "User-Agent": "my-app/1.0"
    }
)
```

### Default Headers

Set headers that are sent with every request:

```python
import httpr

client = httpr.Client(
    headers={
        "Authorization": "Bearer token123",
        "Accept": "application/json"
    }
)

# All requests include these headers
response = client.get("https://api.example.com/data")
```

### Modifying Client Headers

Update headers after client creation:

```python
import httpr

client = httpr.Client()

# Set new headers
client.headers = {"X-Api-Key": "secret"}

# Read current headers
print(client.headers)  # {"x-api-key": "secret"}
```

!!! info "Header Case"
    Headers are stored in lowercase internally (HTTP/2 requirement) but can be accessed case-insensitively.

## Request Body

httpr supports multiple ways to send data in the request body. These options are **mutually exclusive** - use only one per request.

### JSON Data

The most common way to send structured data:

```python
import httpr

response = httpr.post(
    "https://httpbin.org/post",
    json={
        "name": "John Doe",
        "email": "john@example.com",
        "tags": ["python", "rust"],
        "metadata": {"version": 1}
    }
)

# Content-Type is automatically set to application/json
print(response.json()["json"])
```

### CBOR Data

Send data as CBOR (Concise Binary Object Representation):

```python
import httpr

response = httpr.post(
    "https://api.example.com/data",
    cbor={
        "name": "John Doe",
        "values": [1, 2, 3, 4, 5],
        "metadata": {"version": 1}
    }
)

# Content-Type is automatically set to application/cbor
```

CBOR offers several advantages over JSON:

- **Smaller size**: Binary encoding is more compact than text
- **Faster processing**: No text parsing overhead
- **Better for binary data**: Native support for byte arrays
- **Type preservation**: Maintains exact numeric types

Use CBOR when:

- Working with large arrays or datasets
- Building high-performance APIs
- Developing IoT or embedded applications
- Reducing bandwidth usage is critical

!!! note
    The server must support CBOR requests. Check the API documentation to confirm CBOR is accepted.

### Form Data

Send URL-encoded form data:

```python
import httpr

response = httpr.post(
    "https://httpbin.org/post",
    data={
        "username": "john",
        "password": "secret",
        "remember": "true"
    }
)

# Content-Type: application/x-www-form-urlencoded
print(response.json()["form"])
# {"username": "john", "password": "secret", "remember": "true"}
```

### Binary Data

Send raw bytes directly:

```python
import httpr

# Send raw bytes
response = httpr.post(
    "https://httpbin.org/post",
    content=b"raw binary data"
)

# Send string as bytes
response = httpr.post(
    "https://httpbin.org/post",
    content="text data".encode("utf-8")
)
```

### File Uploads

Upload files using multipart/form-data:

```python
import httpr

response = httpr.post(
    "https://httpbin.org/post",
    files={
        "document": "/path/to/document.pdf",
        "image": "/path/to/photo.jpg"
    }
)
```

The `files` dictionary maps form field names to file paths. Files are read and uploaded automatically.

!!! warning "File Paths"
    The `files` argument expects file paths as strings, not file objects. The files must exist on disk.

## Timeouts

Control how long to wait for responses:

### Request Timeout

```python
import httpr

# Wait up to 10 seconds for this request
response = httpr.get("https://httpbin.org/delay/2", timeout=10)
```

### Client Default Timeout

```python
import httpr

# Default timeout for all requests
client = httpr.Client(timeout=30)

# Uses 30 second timeout
response = client.get("https://httpbin.org/get")

# Override for specific request
response = client.get("https://httpbin.org/delay/5", timeout=60)
```

### Timeout Behavior

- Default timeout is 30 seconds
- Timeout of `0` or very small values may cause immediate timeout
- If the server doesn't respond within the timeout, an exception is raised

```python
import httpr

try:
    response = httpr.get("https://httpbin.org/delay/10", timeout=1)
except Exception as e:
    print(f"Request timed out: {e}")
```

## Redirects

By default, httpr follows HTTP redirects automatically:

```python
import httpr

# Follows up to 20 redirects by default
response = httpr.get("https://httpbin.org/redirect/3")
print(response.url)  # Final URL after redirects
```

### Configuring Redirects

```python
import httpr

# Disable redirects
client = httpr.Client(follow_redirects=False)
response = client.get("https://httpbin.org/redirect/1")
print(response.status_code)  # 302

# Limit number of redirects
client = httpr.Client(max_redirects=5)
```

## Protocol Options

### HTTPS Only

Restrict to secure connections only:

```python
import httpr

client = httpr.Client(https_only=True)

# Works
response = client.get("https://example.com")

# Fails - HTTP not allowed
# response = client.get("http://example.com")
```

### HTTP/2

Enable HTTP/2 only mode:

```python
import httpr

# Use only HTTP/2
client = httpr.Client(http2_only=True)
response = client.get("https://example.com")
```

!!! note
    When `http2_only=False` (default), httpr uses HTTP/1.1. Set to `True` for HTTP/2.

## Complete Example

Here's a complete example showing various request options:

```python
import httpr

# Create a configured client
client = httpr.Client(
    headers={"User-Agent": "my-app/1.0"},
    params={"api_version": "v2"},
    timeout=30,
    follow_redirects=True,
    max_redirects=10,
)

# GET request with query params
response = client.get(
    "https://httpbin.org/get",
    params={"search": "python"},
    headers={"Accept": "application/json"}
)
print(f"Status: {response.status_code}")
print(f"URL: {response.url}")

# POST with JSON
response = client.post(
    "https://httpbin.org/post",
    json={"message": "Hello, World!"},
    timeout=60  # Override timeout for this request
)
print(response.json())

# Cleanup
client.close()
```

## Next Steps

- [Response Handling](response-handling.md) - Learn to work with response data
- [Authentication](authentication.md) - Add authentication to your requests
