# Client

The synchronous HTTP client with connection pooling.

## Client

```python
Client(auth: tuple[str, str | None] | None = None, auth_bearer: str | None = None, params: dict[str, str] | None = None, headers: dict[str, str] | None = None, cookies: dict[str, str] | None = None, cookie_store: bool | None = True, referer: bool | None = True, proxy: str | None = None, timeout: float | None = 30, follow_redirects: bool | None = True, max_redirects: int | None = 20, verify: bool | None = True, ca_cert_file: str | None = None, client_pem: str | None = None, https_only: bool | None = False, http2_only: bool | None = False)
```

A synchronous HTTP client with connection pooling.

The Client class provides a high-level interface for making HTTP requests. It supports connection pooling, automatic cookie handling, and various authentication methods.

Example

Basic usage:

```python
import httpr

# Using context manager (recommended)
with httpr.Client() as client:
    response = client.get("https://httpbin.org/get")
    print(response.json())

# Or manually
client = httpr.Client()
response = client.get("https://httpbin.org/get")
client.close()
```

With configuration:

```python
import httpr

client = httpr.Client(
    auth_bearer="your-api-token",
    headers={"User-Agent": "my-app/1.0"},
    timeout=30,
)
```

Attributes:

| Name      | Type              | Description                                                     |
| --------- | ----------------- | --------------------------------------------------------------- |
| `headers` | `dict[str, str]`  | Default headers sent with all requests. Excludes Cookie header. |
| `cookies` | `dict[str, str]`  | Default cookies sent with all requests.                         |
| `auth`    | \`tuple\[str, str | None\]                                                          |
| `params`  | \`dict[str, str]  | None\`                                                          |
| `timeout` | \`float           | None\`                                                          |
| `proxy`   | \`str             | None\`                                                          |

Initialize an HTTP client.

Parameters:

| Name               | Type              | Description | Default                                                                                                                        |
| ------------------ | ----------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `auth`             | \`tuple\[str, str | None\]      | None\`                                                                                                                         |
| `auth_bearer`      | \`str             | None\`      | Bearer token for Authorization header.                                                                                         |
| `params`           | \`dict[str, str]  | None\`      | Default query parameters to include in all requests.                                                                           |
| `headers`          | \`dict[str, str]  | None\`      | Default headers to send with all requests.                                                                                     |
| `cookies`          | \`dict[str, str]  | None\`      | Default cookies to send with all requests.                                                                                     |
| `cookie_store`     | \`bool            | None\`      | Enable persistent cookie store. Cookies from responses will be preserved and included in subsequent requests. Default is True. |
| `referer`          | \`bool            | None\`      | Automatically set Referer header. Default is True.                                                                             |
| `proxy`            | \`str             | None\`      | Proxy URL (e.g., "http://proxy:8080" or "socks5://127.0.0.1:1080"). Falls back to HTTPR_PROXY environment variable.            |
| `timeout`          | \`float           | None\`      | Request timeout in seconds. Default is 30.                                                                                     |
| `follow_redirects` | \`bool            | None\`      | Follow HTTP redirects. Default is True.                                                                                        |
| `max_redirects`    | \`int             | None\`      | Maximum redirects to follow. Default is 20.                                                                                    |
| `verify`           | \`bool            | None\`      | Verify SSL certificates. Default is True.                                                                                      |
| `ca_cert_file`     | \`str             | None\`      | Path to CA certificate bundle (PEM format).                                                                                    |
| `client_pem`       | \`str             | None\`      | Path to client certificate for mTLS (PEM format).                                                                              |
| `https_only`       | \`bool            | None\`      | Only allow HTTPS requests. Default is False.                                                                                   |
| `http2_only`       | \`bool            | None\`      | Use HTTP/2 only (False uses HTTP/1.1). Default is False.                                                                       |

Example

```python
import httpr

# Simple client
client = httpr.Client()

# Client with authentication
client = httpr.Client(
    auth=("username", "password"),
    timeout=60,
)

# Client with bearer token
client = httpr.Client(
    auth_bearer="your-api-token",
    headers={"Accept": "application/json"},
)

# Client with proxy
client = httpr.Client(proxy="http://proxy.example.com:8080")

# Client with mTLS
client = httpr.Client(
    client_pem="/path/to/client.pem",
    ca_cert_file="/path/to/ca.pem",
)
```

### request

```python
request(method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an HTTP request.

Parameters:

| Name       | Type                    | Description                                                 | Default    |
| ---------- | ----------------------- | ----------------------------------------------------------- | ---------- |
| `method`   | `HttpMethod`            | HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS). | *required* |
| `url`      | `str`                   | Request URL.                                                | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters (see below).                             | `{}`       |

Other Parameters:

| Name          | Type                                  | Description                                                          |
| ------------- | ------------------------------------- | -------------------------------------------------------------------- |
| `params`      | `Optional[dict[str, str]]`            | Query parameters to append to URL.                                   |
| `headers`     | `Optional[dict[str, str]]`            | Request headers (merged with client defaults).                       |
| `cookies`     | `Optional[dict[str, str]]`            | Request cookies (merged with client defaults).                       |
| `auth`        | `Optional[tuple[str, Optional[str]]]` | Basic auth credentials (overrides client default).                   |
| `auth_bearer` | `Optional[str]`                       | Bearer token (overrides client default).                             |
| `timeout`     | `Optional[float]`                     | Request timeout in seconds (overrides client default).               |
| `content`     | `Optional[bytes]`                     | Raw bytes for request body.                                          |
| `data`        | `Optional[dict[str, Any]]`            | Form data for request body (application/x-www-form-urlencoded).      |
| `json`        | `Optional[Any]`                       | JSON data for request body (application/json).                       |
| `files`       | `Optional[dict[str, str]]`            | Files for multipart upload (dict mapping field names to file paths). |

Returns:

| Type       | Description                                     |
| ---------- | ----------------------------------------------- |
| `Response` | Response object with status, headers, and body. |

Raises:

| Type         | Description                                         |
| ------------ | --------------------------------------------------- |
| `ValueError` | If method is not a valid HTTP method.               |
| `Exception`  | If request fails (timeout, connection error, etc.). |

Example

```python
response = client.request("GET", "https://httpbin.org/get")
response = client.request("POST", "https://httpbin.org/post", json={"key": "value"})
```

Note

Only one of `content`, `data`, `json`, or `files` can be specified per request.

### get

```python
get(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make a GET request.

Parameters:

| Name       | Type                    | Description                                                                | Default    |
| ---------- | ----------------------- | -------------------------------------------------------------------------- | ---------- |
| `url`      | `str`                   | Request URL.                                                               | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters (params, headers, cookies, auth, auth_bearer, timeout). | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
response = client.get(
    "https://httpbin.org/get",
    params={"key": "value"},
    headers={"Accept": "application/json"},
)
print(response.json())
```

### head

```python
head(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make a HEAD request.

Returns only headers, no response body.

Parameters:

| Name       | Type                    | Description                                                                | Default    |
| ---------- | ----------------------- | -------------------------------------------------------------------------- | ---------- |
| `url`      | `str`                   | Request URL.                                                               | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters (params, headers, cookies, auth, auth_bearer, timeout). | `{}`       |

Returns:

| Type       | Description                           |
| ---------- | ------------------------------------- |
| `Response` | Response object (body will be empty). |

Example

```python
response = client.head("https://httpbin.org/get")
print(response.headers["content-length"])
```

### options

```python
options(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an OPTIONS request.

Parameters:

| Name       | Type                    | Description                                                                | Default    |
| ---------- | ----------------------- | -------------------------------------------------------------------------- | ---------- |
| `url`      | `str`                   | Request URL.                                                               | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters (params, headers, cookies, auth, auth_bearer, timeout). | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
response = client.options("https://httpbin.org/get")
print(response.headers.get("allow"))
```

### delete

```python
delete(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make a DELETE request.

Parameters:

| Name       | Type                    | Description                                                                | Default    |
| ---------- | ----------------------- | -------------------------------------------------------------------------- | ---------- |
| `url`      | `str`                   | Request URL.                                                               | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters (params, headers, cookies, auth, auth_bearer, timeout). | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
response = client.delete("https://httpbin.org/delete")
print(response.status_code)
```

### post

```python
post(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make a POST request.

Parameters:

| Name       | Type                    | Description                                | Default    |
| ---------- | ----------------------- | ------------------------------------------ | ---------- |
| `url`      | `str`                   | Request URL.                               | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters including body options. | `{}`       |

Other Parameters:

| Name          | Type                                  | Description             |
| ------------- | ------------------------------------- | ----------------------- |
| `params`      | `Optional[dict[str, str]]`            | Query parameters.       |
| `headers`     | `Optional[dict[str, str]]`            | Request headers.        |
| `cookies`     | `Optional[dict[str, str]]`            | Request cookies.        |
| `auth`        | `Optional[tuple[str, Optional[str]]]` | Basic auth credentials. |
| `auth_bearer` | `Optional[str]`                       | Bearer token.           |
| `timeout`     | `Optional[float]`                     | Request timeout.        |
| `content`     | `Optional[bytes]`                     | Raw bytes body.         |
| `data`        | `Optional[dict[str, Any]]`            | Form-encoded body.      |
| `json`        | `Optional[Any]`                       | JSON body.              |
| `files`       | `Optional[dict[str, str]]`            | Multipart file uploads. |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
# JSON body
response = client.post(
    "https://httpbin.org/post",
    json={"name": "httpr", "fast": True},
)

# Form data
response = client.post(
    "https://httpbin.org/post",
    data={"username": "user", "password": "pass"},
)

# File upload
response = client.post(
    "https://httpbin.org/post",
    files={"document": "/path/to/file.pdf"},
)
```

### put

```python
put(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make a PUT request.

Parameters:

| Name       | Type                    | Description                                | Default    |
| ---------- | ----------------------- | ------------------------------------------ | ---------- |
| `url`      | `str`                   | Request URL.                               | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters including body options. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
response = client.put(
    "https://httpbin.org/put",
    json={"key": "updated_value"},
)
```

### patch

```python
patch(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make a PATCH request.

Parameters:

| Name       | Type                    | Description                                | Default    |
| ---------- | ----------------------- | ------------------------------------------ | ---------- |
| `url`      | `str`                   | Request URL.                               | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters including body options. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
response = client.patch(
    "https://httpbin.org/patch",
    json={"field": "new_value"},
)
```

### stream

```python
stream(method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]) -> Generator[StreamingResponse, None, None]
```

Make a streaming HTTP request.

Returns a context manager that yields a StreamingResponse for iterating over the response body in chunks without buffering the entire response in memory.

Parameters:

| Name       | Type                    | Description                                                 | Default    |
| ---------- | ----------------------- | ----------------------------------------------------------- | ---------- |
| `method`   | `HttpMethod`            | HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS). | *required* |
| `url`      | `str`                   | Request URL.                                                | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters (same as request()).                     | `{}`       |

Yields:

| Name                | Type                | Description                                               |
| ------------------- | ------------------- | --------------------------------------------------------- |
| `StreamingResponse` | `StreamingResponse` | A response object that can be iterated to receive chunks. |

Example

Basic streaming:

```python
with client.stream("GET", "https://example.com/large-file") as response:
    for chunk in response.iter_bytes():
        process(chunk)
```

Streaming text:

```python
with client.stream("GET", "https://example.com/text") as response:
    for text in response.iter_text():
        print(text, end="")
```

Streaming lines (e.g., Server-Sent Events):

```python
with client.stream("GET", "https://example.com/events") as response:
    for line in response.iter_lines():
        print(line.strip())
```

Conditional reading:

```python
with client.stream("GET", url) as response:
    if response.status_code == 200:
        content = response.read()  # Read all remaining content
    else:
        pass  # Don't read the body
```

Note

The response body is only read when you iterate over it or call read(). Always use this as a context manager to ensure proper cleanup.

### close

```python
close() -> None
```

Close the client and release resources.

Example

```python
client = httpr.Client()
try:
    response = client.get("https://example.com")
finally:
    client.close()
```
