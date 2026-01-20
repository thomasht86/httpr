# Module Functions

Convenience functions for making one-off HTTP requests.

These functions create a temporary `Client` internally for each request. For multiple requests, use a [`Client`](https://thomasht86.github.io/httpr/api/client/index.md) instance for better performance.

## Functions

### request

```python
request(method: HttpMethod, url: str, verify: bool | None = True, ca_cert_file: str | None = None, client_pem: str | None = None, client_pem_data: bytes | None = None, **kwargs: Unpack[RequestParams]) -> Response
```

Make an HTTP request using a temporary client.

This is a convenience function for one-off requests. For multiple requests, use a Client instance for better performance (connection pooling).

Parameters:

| Name              | Type                    | Description                                                 | Default                                       |
| ----------------- | ----------------------- | ----------------------------------------------------------- | --------------------------------------------- |
| `method`          | `HttpMethod`            | HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS). | *required*                                    |
| `url`             | `str`                   | Request URL.                                                | *required*                                    |
| `verify`          | \`bool                  | None\`                                                      | Verify SSL certificates. Default is True.     |
| `ca_cert_file`    | \`str                   | None\`                                                      | Path to CA certificate bundle.                |
| `client_pem`      | \`str                   | None\`                                                      | Path to client certificate for mTLS.          |
| `client_pem_data` | \`bytes                 | None\`                                                      | Client certificate and key as bytes for mTLS. |
| `**kwargs`        | `Unpack[RequestParams]` | Additional request parameters.                              | `{}`                                          |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
import httpr

response = httpr.request("GET", "https://httpbin.org/get")
response = httpr.request("POST", "https://httpbin.org/post", json={"key": "value"})
```

### get

```python
get(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response
```

Make a GET request using a temporary client.

Parameters:

| Name       | Type                          | Description                                                         | Default    |
| ---------- | ----------------------------- | ------------------------------------------------------------------- | ---------- |
| `url`      | `str`                         | Request URL.                                                        | *required* |
| `**kwargs` | `Unpack[ClientRequestParams]` | Request parameters (params, headers, cookies, auth, timeout, etc.). | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
import httpr

response = httpr.get("https://httpbin.org/get", params={"key": "value"})
print(response.json())
```

### post

```python
post(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response
```

Make a POST request using a temporary client.

Parameters:

| Name       | Type                          | Description                                            | Default    |
| ---------- | ----------------------------- | ------------------------------------------------------ | ---------- |
| `url`      | `str`                         | Request URL.                                           | *required* |
| `**kwargs` | `Unpack[ClientRequestParams]` | Request parameters (json, data, content, files, etc.). | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
import httpr

# JSON body
response = httpr.post("https://httpbin.org/post", json={"key": "value"})

# Form data
response = httpr.post("https://httpbin.org/post", data={"field": "value"})
```

### put

```python
put(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response
```

Make a PUT request using a temporary client.

Parameters:

| Name       | Type                          | Description         | Default    |
| ---------- | ----------------------------- | ------------------- | ---------- |
| `url`      | `str`                         | Request URL.        | *required* |
| `**kwargs` | `Unpack[ClientRequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
import httpr

response = httpr.put("https://httpbin.org/put", json={"key": "value"})
```

### patch

```python
patch(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response
```

Make a PATCH request using a temporary client.

Parameters:

| Name       | Type                          | Description         | Default    |
| ---------- | ----------------------------- | ------------------- | ---------- |
| `url`      | `str`                         | Request URL.        | *required* |
| `**kwargs` | `Unpack[ClientRequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
import httpr

response = httpr.patch("https://httpbin.org/patch", json={"field": "new_value"})
```

### delete

```python
delete(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response
```

Make a DELETE request using a temporary client.

Parameters:

| Name       | Type                          | Description         | Default    |
| ---------- | ----------------------------- | ------------------- | ---------- |
| `url`      | `str`                         | Request URL.        | *required* |
| `**kwargs` | `Unpack[ClientRequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
import httpr

response = httpr.delete("https://httpbin.org/delete")
```

### head

```python
head(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response
```

Make a HEAD request using a temporary client.

Parameters:

| Name       | Type                          | Description         | Default    |
| ---------- | ----------------------------- | ------------------- | ---------- |
| `url`      | `str`                         | Request URL.        | *required* |
| `**kwargs` | `Unpack[ClientRequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description                           |
| ---------- | ------------------------------------- |
| `Response` | Response object (body will be empty). |

Example

```python
import httpr

response = httpr.head("https://httpbin.org/get")
print(response.headers)
```

### options

```python
options(url: str, **kwargs: Unpack[ClientRequestParams]) -> Response
```

Make an OPTIONS request using a temporary client.

Parameters:

| Name       | Type                          | Description         | Default    |
| ---------- | ----------------------------- | ------------------- | ---------- |
| `url`      | `str`                         | Request URL.        | *required* |
| `**kwargs` | `Unpack[ClientRequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
import httpr

response = httpr.options("https://httpbin.org/get")
```
