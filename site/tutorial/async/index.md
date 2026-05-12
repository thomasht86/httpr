# Async Client

httpr provides an `AsyncClient` for use with Python's `asyncio`. This allows you to make concurrent HTTP requests efficiently.

## Basic Usage

Use `AsyncClient` with `async`/`await` syntax:

```python
import asyncio
import httpr

async def main():
    async with httpr.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        print(response.json())

asyncio.run(main())
```

## Creating an AsyncClient

`AsyncClient` accepts all the same parameters as `Client`:

```python
import httpr

client = httpr.AsyncClient(
    auth=("user", "password"),
    auth_bearer="token",
    headers={"User-Agent": "my-app/1.0"},
    cookies={"session": "abc123"},
    timeout=30,
    follow_redirects=True,
    max_redirects=10,
    verify=True,
    ca_cert_file="/path/to/ca-bundle.pem",
    proxy="http://proxy:8080",
)
```

## Context Manager

Always use the async context manager to ensure proper cleanup:

```python
import asyncio
import httpr

async def main():
    async with httpr.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        print(response.status_code)
    # Client is automatically closed

asyncio.run(main())
```

Or manually close the client:

```python
import asyncio
import httpr

async def main():
    client = httpr.AsyncClient()
    try:
        response = await client.get("https://httpbin.org/get")
        print(response.status_code)
    finally:
        await client.aclose()

asyncio.run(main())
```

## HTTP Methods

All HTTP methods are available as async:

```python
import asyncio
import httpr

async def main():
    async with httpr.AsyncClient() as client:
        # GET
        response = await client.get("https://httpbin.org/get")

        # POST
        response = await client.post(
            "https://httpbin.org/post",
            json={"key": "value"}
        )

        # PUT
        response = await client.put(
            "https://httpbin.org/put",
            json={"key": "value"}
        )

        # PATCH
        response = await client.patch(
            "https://httpbin.org/patch",
            json={"key": "value"}
        )

        # DELETE
        response = await client.delete("https://httpbin.org/delete")

        # HEAD
        response = await client.head("https://httpbin.org/get")

        # OPTIONS
        response = await client.options("https://httpbin.org/get")

        # Generic request
        response = await client.request("GET", "https://httpbin.org/get")

asyncio.run(main())
```

## Concurrent Requests

The main benefit of `AsyncClient` is making multiple requests concurrently:

### Using asyncio.gather

```python
import asyncio
import httpr

async def fetch_url(client: httpr.AsyncClient, url: str) -> dict:
    response = await client.get(url)
    return {"url": url, "status": response.status_code}

async def main():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/headers",
    ]

    async with httpr.AsyncClient() as client:
        # Fetch all URLs concurrently
        tasks = [fetch_url(client, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for result in results:
            print(f"{result['url']}: {result['status']}")

asyncio.run(main())
```

### Using asyncio.as_completed

Process results as they complete:

```python
import asyncio
import httpr

async def fetch_url(client: httpr.AsyncClient, url: str) -> dict:
    response = await client.get(url)
    return {"url": url, "status": response.status_code, "data": response.json()}

async def main():
    urls = [
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/get",
    ]

    async with httpr.AsyncClient() as client:
        tasks = [fetch_url(client, url) for url in urls]

        # Process results as they complete (fastest first)
        for coro in asyncio.as_completed(tasks):
            result = await coro
            print(f"Completed: {result['url']}")

asyncio.run(main())
```

### With Semaphore (Rate Limiting)

Limit concurrent requests to avoid overwhelming servers:

```python
import asyncio
import httpr

async def fetch_with_limit(
    client: httpr.AsyncClient,
    url: str,
    semaphore: asyncio.Semaphore
) -> dict:
    async with semaphore:  # Limit concurrent requests
        response = await client.get(url)
        return {"url": url, "status": response.status_code}

async def main():
    urls = [f"https://httpbin.org/get?id={i}" for i in range(20)]

    # Allow max 5 concurrent requests
    semaphore = asyncio.Semaphore(5)

    async with httpr.AsyncClient() as client:
        tasks = [fetch_with_limit(client, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

        print(f"Fetched {len(results)} URLs")

asyncio.run(main())
```

## Error Handling

Handle errors in async code:

```python
import asyncio
import httpr

async def safe_fetch(client: httpr.AsyncClient, url: str) -> dict | None:
    try:
        response = await client.get(url, timeout=5)
        return {"url": url, "status": response.status_code, "data": response.json()}
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def main():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/delay/10",  # Will timeout
        "https://invalid.url.example",    # Will fail
    ]

    async with httpr.AsyncClient(timeout=2) as client:
        tasks = [safe_fetch(client, url) for url in urls]
        results = await asyncio.gather(*tasks)

        successful = [r for r in results if r is not None]
        print(f"Successful: {len(successful)}/{len(urls)}")

asyncio.run(main())
```

## Real-World Example: API Aggregator

```python
import asyncio
import httpr

class ApiAggregator:
    """Fetch data from multiple APIs concurrently."""

    def __init__(self, timeout: float = 10):
        self.client = httpr.AsyncClient(timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.client.aclose()

    async def fetch_user(self, user_id: int) -> dict:
        """Fetch user from API."""
        response = await self.client.get(
            f"https://jsonplaceholder.typicode.com/users/{user_id}"
        )
        return response.json()

    async def fetch_posts(self, user_id: int) -> list:
        """Fetch posts for a user."""
        response = await self.client.get(
            "https://jsonplaceholder.typicode.com/posts",
            params={"userId": user_id}
        )
        return response.json()

    async def fetch_user_with_posts(self, user_id: int) -> dict:
        """Fetch user and their posts concurrently."""
        user, posts = await asyncio.gather(
            self.fetch_user(user_id),
            self.fetch_posts(user_id)
        )
        return {"user": user, "posts": posts}

async def main():
    async with ApiAggregator() as api:
        # Fetch data for multiple users concurrently
        user_ids = [1, 2, 3]
        tasks = [api.fetch_user_with_posts(uid) for uid in user_ids]
        results = await asyncio.gather(*tasks)

        for result in results:
            user = result["user"]
            posts = result["posts"]
            print(f"{user['name']}: {len(posts)} posts")

asyncio.run(main())
```

## Implementation Note

How AsyncClient Works

`AsyncClient` wraps the synchronous Rust client using `asyncio.run_in_executor()`. This means:

- Requests run in a thread pool, not native async I/O
- Still provides concurrency benefits for I/O-bound tasks
- Compatible with asyncio event loops
- Same performance as sync client for individual requests

This design keeps the implementation simple while providing async compatibility.

## Comparison: Sync vs Async

```python
import time
import asyncio
import httpr

# Synchronous - sequential requests
def sync_fetch():
    with httpr.Client() as client:
        for i in range(5):
            client.get(f"https://httpbin.org/delay/1")

# Asynchronous - concurrent requests
async def async_fetch():
    async with httpr.AsyncClient() as client:
        tasks = [
            client.get(f"https://httpbin.org/delay/1")
            for i in range(5)
        ]
        await asyncio.gather(*tasks)

# Sync: ~5 seconds (sequential)
start = time.time()
sync_fetch()
print(f"Sync: {time.time() - start:.2f}s")

# Async: ~1 second (concurrent)
start = time.time()
asyncio.run(async_fetch())
print(f"Async: {time.time() - start:.2f}s")
```

## Next Steps

- [SSL/TLS](https://thomasht86.github.io/httpr/advanced/ssl-tls/index.md) - Secure connections with async
- [Proxy Configuration](https://thomasht86.github.io/httpr/advanced/proxy/index.md) - Use proxies with AsyncClient
- [API Reference](https://thomasht86.github.io/httpr/api/async-client/index.md) - Complete AsyncClient API
