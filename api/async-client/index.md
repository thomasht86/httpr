# AsyncClient

The asynchronous HTTP client for use with asyncio.

## AsyncClient

```python
AsyncClient(*args, max_concurrency: int | None = DEFAULT_MAX_CONCURRENCY, **kwargs)
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

AsyncClient runs synchronous Rust code in a thread executor. It provides concurrency benefits for I/O-bound tasks but is not native async I/O. `max_concurrency` sizes that executor and therefore caps how many requests can be in flight at once.

Initialize an async HTTP client.

Accepts the same parameters as Client, plus:

Parameters:

| Name              | Type  | Description | Default                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------- | ----- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `max_concurrency` | \`int | None\`      | Maximum number of requests in flight at once, i.e. the size of this client's thread pool. Defaults to 64. Threads are created lazily, so an idle client costs nothing. Pass None to dispatch on asyncio's default executor instead -- note that this shares a pool with asyncio.to_thread and every other run_in_executor(None) caller in the application, and that CPython sizes it at min(32, cpu_count + 4). |

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
stream(method: HttpMethod, url: str, **kwargs: Unpack[RequestParams]) -> AsyncIterator[AsyncStreamingResponse]
```

Make an async streaming HTTP request.

Returns an async context manager that yields an `AsyncStreamingResponse` for iterating over the response body in chunks. Status, headers and cookies are available as soon as the block is entered; the body is read as you iterate.

Parameters:

| Name       | Type                    | Description         | Default    |
| ---------- | ----------------------- | ------------------- | ---------- |
| `method`   | `HttpMethod`            | HTTP method.        | *required* |
| `url`      | `str`                   | Request URL.        | *required* |
| `**kwargs` | `Unpack[RequestParams]` | Request parameters. | `{}`       |

Yields:

| Name                     | Type                                    | Description                                 |
| ------------------------ | --------------------------------------- | ------------------------------------------- |
| `AsyncStreamingResponse` | `AsyncIterator[AsyncStreamingResponse]` | A response object that can be iterated with |
|                          | `AsyncIterator[AsyncStreamingResponse]` | async for.                                  |

Example

```python
async with client.stream("GET", "https://example.com/large-file") as response:
    async for chunk in response.aiter_bytes():
        process(chunk)

async with client.stream("GET", "https://example.com/events") as response:
    async for line in response.aiter_lines():
        handle(line)
```

Note

`aiter_bytes()`, `aiter_text()`, `aiter_lines()` and `aread()` read each chunk on the client's thread pool, so other tasks keep running while the server is producing data. The synchronous `iter_*()` and `read()` methods are still available but block the event loop.

### aclose

```python
aclose() -> None
```

Close the async client.

Releases the connection pool and shuts down this client's thread pool. Any request made after `aclose()` raises `httpr.ClientClosed`. Calling it more than once is a no-op.

Example

```python
client = httpr.AsyncClient()
try:
    response = await client.get("https://example.com")
finally:
    await client.aclose()
```

## AsyncStreamingResponse

```python
AsyncStreamingResponse(response: StreamingResponse, client: AsyncClient)
```

The streaming response yielded by `AsyncClient.stream()`.

Wraps the `StreamingResponse` produced by the Rust core and adds async iteration: `aiter_bytes()`, `aiter_text()`, `aiter_lines()` and `aread()` fetch each chunk on the client's thread pool, so the event loop keeps running other tasks while the server is producing the next one. Status, headers, cookies and URL are available as soon as the context manager is entered, before any of the body has been read.

The synchronous `iter_bytes()`, `iter_text()`, `iter_lines()` and `read()` are still available, but each step blocks the event loop for as long as the server takes to send the next chunk; use the async variants in async code.

Example

```python
async with client.stream("GET", "https://example.com/events") as response:
    async for line in response.aiter_lines():
        handle(line)
```

### aiter_bytes

```python
aiter_bytes() -> AsyncIterator[bytes]
```

Iterate over the response body as bytes chunks without blocking the event loop.

Example

```python
async for chunk in response.aiter_bytes():
    process(chunk)
```

### aiter_text

```python
aiter_text() -> AsyncIterator[str]
```

Iterate over the response body as text chunks, decoded with the response encoding.

### aiter_lines

```python
aiter_lines() -> AsyncIterator[str]
```

Iterate over the response body line by line, e.g. for Server-Sent Events.

Example

```python
async for line in response.aiter_lines():
    if line.startswith("data:"):
        handle(line[5:].strip())
```

### aread

```python
aread() -> bytes
```

Read the entire remaining response body without blocking the event loop.

### aclose

```python
aclose() -> None
```

Close the streaming response and release its connection.

`AsyncClient.stream()` calls this when the `async with` block exits. Closing never waits on I/O, so it runs on the event-loop thread.

### raise_for_status

```python
raise_for_status() -> AsyncStreamingResponse
```

Raise `HTTPStatusError` on a non-2xx status; returns self on success.
