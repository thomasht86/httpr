# AsyncClient

The asynchronous HTTP client for use with asyncio.

## AsyncClient

```python
AsyncClient(*args, **kwargs)
```

An asynchronous HTTP client for use with asyncio.

AsyncClient wraps the synchronous Client using asyncio.run_in_executor(), providing an async interface while leveraging the Rust implementation's performance.

Example

Basic usage:

```python
import asyncio
import httpr

async def main():
    async with httpr.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        print(response.json())

asyncio.run(main())
```

Concurrent requests:

```python
import asyncio
import httpr

async def main():
    async with httpr.AsyncClient() as client:
        tasks = [
            client.get("https://httpbin.org/get"),
            client.get("https://httpbin.org/ip"),
        ]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response.json())

asyncio.run(main())
```

Note

AsyncClient runs synchronous Rust code in a thread executor. It provides concurrency benefits for I/O-bound tasks but is not native async I/O.

Initialize an async HTTP client.

Accepts the same parameters as Client.

### request

```python
request(method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an async HTTP request.

Parameters:

| Name       | Type                    | Description         | Default    |
| ---------- | ----------------------- | ------------------- | ---------- |
| `method`   | `HttpMethod`            | HTTP method.        | *required* |
| `url`      | `str`                   | Request URL.        | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
response = await client.request("GET", "https://httpbin.org/get")
```

### get

```python
get(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an async GET request.

Parameters:

| Name       | Type                    | Description         | Default    |
| ---------- | ----------------------- | ------------------- | ---------- |
| `url`      | `str`                   | Request URL.        | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

Example

```python
response = await client.get("https://httpbin.org/get")
```

### head

```python
head(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an async HEAD request.

Parameters:

| Name       | Type                    | Description         | Default    |
| ---------- | ----------------------- | ------------------- | ---------- |
| `url`      | `str`                   | Request URL.        | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

### options

```python
options(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an async OPTIONS request.

Parameters:

| Name       | Type                    | Description         | Default    |
| ---------- | ----------------------- | ------------------- | ---------- |
| `url`      | `str`                   | Request URL.        | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

### delete

```python
delete(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an async DELETE request.

Parameters:

| Name       | Type                    | Description         | Default    |
| ---------- | ----------------------- | ------------------- | ---------- |
| `url`      | `str`                   | Request URL.        | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

### post

```python
post(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an async POST request.

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
response = await client.post(
    "https://httpbin.org/post",
    json={"key": "value"},
)
```

### put

```python
put(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an async PUT request.

Parameters:

| Name       | Type                    | Description                                | Default    |
| ---------- | ----------------------- | ------------------------------------------ | ---------- |
| `url`      | `str`                   | Request URL.                               | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters including body options. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

### patch

```python
patch(url: str, **kwargs: Unpack[RequestParams]) -> Response
```

Make an async PATCH request.

Parameters:

| Name       | Type                    | Description                                | Default    |
| ---------- | ----------------------- | ------------------------------------------ | ---------- |
| `url`      | `str`                   | Request URL.                               | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters including body options. | `{}`       |

Returns:

| Type       | Description      |
| ---------- | ---------------- |
| `Response` | Response object. |

### stream

```python
stream(method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]) -> AsyncIterator[StreamingResponse]
```

Make an async streaming HTTP request.

Returns an async context manager that yields a StreamingResponse for iterating over the response body in chunks.

Parameters:

| Name       | Type                    | Description         | Default    |
| ---------- | ----------------------- | ------------------- | ---------- |
| `method`   | `HttpMethod`            | HTTP method.        | *required* |
| `url`      | `str`                   | Request URL.        | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters. | `{}`       |

Yields:

| Name                | Type                               | Description                             |
| ------------------- | ---------------------------------- | --------------------------------------- |
| `StreamingResponse` | `AsyncIterator[StreamingResponse]` | A response object that can be iterated. |

Example

```python
async with client.stream("GET", "https://example.com/large-file") as response:
    for chunk in response.iter_bytes():
        process(chunk)
```

Note

Iteration over the response is synchronous (uses iter_bytes, iter_text, iter_lines). The async part is initiating the request and entering the context manager.

### aclose

```python
aclose()
```

Close the async client.

Example

```python
client = httpr.AsyncClient()
try:
    response = await client.get("https://example.com")
finally:
    await client.aclose()
```
