# Response Handling

This guide covers how to work with HTTP responses in httpr.

## The Response Object

Every request returns a `Response` object with all the information about the server's response:

```python
import httpr

response = httpr.get("https://httpbin.org/get")

# Access response data
print(response.status_code)  # HTTP status code
print(response.text)         # Body as string
print(response.content)      # Body as bytes
print(response.headers)      # Response headers
print(response.cookies)      # Response cookies
print(response.url)          # Final URL (after redirects)
print(response.encoding)     # Character encoding
```

## Status Codes

Check the HTTP status code to determine if the request succeeded:

```python
import httpr

response = httpr.get("https://httpbin.org/status/200")
print(response.status_code)  # 200

response = httpr.get("https://httpbin.org/status/404")
print(response.status_code)  # 404

# Check for success (2xx status codes)
if 200 <= response.status_code < 300:
    print("Success!")
elif 400 <= response.status_code < 500:
    print("Client error")
elif 500 <= response.status_code < 600:
    print("Server error")
```

## Response Body

### Text Content

Get the response body as a decoded string:

```python
import httpr

response = httpr.get("https://httpbin.org/html")
print(response.text)  # HTML content as string
```

The encoding is automatically detected from:

1. The `Content-Type` header charset
2. HTML meta charset tag (first 2048 bytes)
3. Falls back to UTF-8

Access the detected encoding:

```python
import httpr

response = httpr.get("https://httpbin.org/encoding/utf8")
print(response.encoding)  # "utf-8"
```

### Binary Content

Get the raw response body as bytes:

```python
import httpr

response = httpr.get("https://httpbin.org/bytes/100")
print(type(response.content))  # <class 'bytes'>
print(len(response.content))   # 100

# Useful for binary files
response = httpr.get("https://httpbin.org/image/png")
with open("image.png", "wb") as f:
    f.write(response.content)
```

### JSON Content

Parse the response body as JSON:

```python
import httpr

response = httpr.get("https://httpbin.org/json")
data = response.json()

print(type(data))  # <class 'dict'>
print(data["slideshow"]["title"])
```

!!! note
    `json()` is a method, not a property. Call it with parentheses.

### CBOR Content

Parse the response body as CBOR (Concise Binary Object Representation):

```python
import httpr

# Assuming the server returns CBOR data
response = httpr.get("https://api.example.com/data")
data = response.cbor()

print(type(data))  # <class 'dict'> or <class 'list'>
print(data)
```

CBOR is a binary serialization format that's more compact than JSON, making it ideal for:

- **Large datasets**: Smaller payload sizes compared to JSON
- **IoT applications**: Efficient data transfer for resource-constrained devices
- **High-performance APIs**: Faster serialization/deserialization

!!! note
    Like `json()`, `cbor()` is a method. The server must send CBOR-encoded data (typically with `Content-Type: application/cbor`).

### HTML Conversion

httpr provides built-in HTML-to-text conversion using Rust's `html2text` crate:

```python
import httpr

response = httpr.get("https://example.com")

# Convert HTML to Markdown
markdown = response.text_markdown
print(markdown)

# Convert HTML to plain text (no formatting)
plain = response.text_plain
print(plain)

# Convert HTML to rich text
rich = response.text_rich
print(rich)
```

This is useful for:

- Extracting readable content from web pages
- Processing HTML for text analysis
- Creating plain-text versions of HTML emails

## Response Headers

Access response headers through the `headers` attribute:

```python
import httpr

response = httpr.get("https://httpbin.org/response-headers?X-Custom=test")

# Headers are case-insensitive
print(response.headers["content-type"])
print(response.headers["Content-Type"])  # Same result
print(response.headers["CONTENT-TYPE"])  # Also works

# Check if header exists
if "x-custom" in response.headers:
    print(response.headers["x-custom"])

# Get with default value
value = response.headers.get("x-missing", "default")

# Iterate over headers
for key, value in response.headers.items():
    print(f"{key}: {value}")

# Get all header names
print(list(response.headers.keys()))

# Get all header values
print(list(response.headers.values()))
```

### Common Headers

```python
import httpr

response = httpr.get("https://httpbin.org/get")

# Content information
content_type = response.headers.get("content-type")
content_length = response.headers.get("content-length")

# Caching
cache_control = response.headers.get("cache-control")
etag = response.headers.get("etag")

# Server information
server = response.headers.get("server")
date = response.headers.get("date")
```

## Response Cookies

Access cookies set by the server:

```python
import httpr

response = httpr.get("https://httpbin.org/cookies/set?session=abc123")

# Cookies as a dictionary
print(response.cookies)  # {"session": "abc123"}

# Access specific cookie
if "session" in response.cookies:
    print(response.cookies["session"])
```

### Cookie Persistence

With `cookie_store=True` (default), cookies are automatically stored and sent with subsequent requests:

```python
import httpr

client = httpr.Client(cookie_store=True)  # Default

# First request sets a cookie
client.get("https://httpbin.org/cookies/set?token=xyz")

# Cookie is automatically included in next request
response = client.get("https://httpbin.org/cookies")
print(response.json()["cookies"])  # {"token": "xyz"}
```

See the [Cookie Handling](../advanced/cookies.md) guide for more details.

## Final URL

After redirects, check the final URL:

```python
import httpr

response = httpr.get("https://httpbin.org/redirect/3")

# The URL after following all redirects
print(response.url)  # https://httpbin.org/get
```

This is useful for:

- Detecting redirects
- Getting the canonical URL
- Debugging redirect chains

## Complete Example

Here's a comprehensive example of response handling:

```python
import httpr

def fetch_and_process(url: str) -> dict:
    """Fetch a URL and return processed response data."""

    response = httpr.get(url, timeout=10)

    result = {
        "url": response.url,
        "status": response.status_code,
        "success": 200 <= response.status_code < 300,
    }

    # Get content type
    content_type = response.headers.get("content-type", "")
    result["content_type"] = content_type

    # Process based on content type
    if "application/json" in content_type:
        result["data"] = response.json()
    elif "text/html" in content_type:
        result["text"] = response.text_markdown  # Convert HTML to markdown
    else:
        result["text"] = response.text

    # Include cookies if present
    if response.cookies:
        result["cookies"] = response.cookies

    return result


# Usage
result = fetch_and_process("https://httpbin.org/json")
print(f"Status: {result['status']}")
print(f"Data: {result['data']}")
```

## Error Handling

Handle potential errors when processing responses:

```python
import httpr

try:
    response = httpr.get("https://httpbin.org/status/500")

    if response.status_code >= 400:
        print(f"HTTP Error: {response.status_code}")
    else:
        data = response.json()

except Exception as e:
    print(f"Request failed: {e}")
```

## Streaming Responses

For large responses, you can stream the data instead of buffering it entirely in memory. This is useful for downloading large files, processing Server-Sent Events (SSE), or handling large API responses.

### Basic Streaming

Use the `stream()` context manager to get a streaming response:

```python
import httpr

client = httpr.Client()

# Stream response bytes
with client.stream("GET", "https://httpbin.org/stream-bytes/10000") as response:
    print(f"Status: {response.status_code}")

    for chunk in response.iter_bytes():
        print(f"Received {len(chunk)} bytes")
        # Process chunk without loading entire response in memory
```

### Streaming Modes

httpr provides three ways to iterate over streaming responses:

#### 1. Byte Chunks (`iter_bytes()`)

Iterate over raw bytes chunks:

```python
with client.stream("GET", "https://httpbin.org/stream-bytes/1000") as response:
    for chunk in response.iter_bytes():
        # chunk is bytes
        process_binary_data(chunk)
```

Or use direct iteration (equivalent to `iter_bytes()`):

```python
with client.stream("GET", "https://httpbin.org/stream-bytes/1000") as response:
    for chunk in response:  # Same as response.iter_bytes()
        process_binary_data(chunk)
```

#### 2. Text Chunks (`iter_text()`)

Iterate over decoded text chunks:

```python
with client.stream("GET", "https://httpbin.org/html") as response:
    for text_chunk in response.iter_text():
        # text_chunk is str, decoded using response encoding
        print(text_chunk, end="")
```

The text is automatically decoded using the response's character encoding (from `Content-Type` header or detected from content).

#### 3. Line by Line (`iter_lines()`)

Iterate over the response line by line:

```python
with client.stream("GET", "https://httpbin.org/stream/10") as response:
    for line in response.iter_lines():
        # line is str
        print(line.strip())
```

This is particularly useful for:

- **Server-Sent Events (SSE)**: Process events as they arrive
- **JSONL/NDJSON**: Parse newline-delimited JSON
- **Log streaming**: Process log lines in real-time

```python
# Example: Processing Server-Sent Events
with client.stream("GET", "https://example.com/events") as response:
    for line in response.iter_lines():
        if line.startswith("data:"):
            data = line[5:].strip()  # Remove "data:" prefix
            process_event(data)
```

### Conditional Reading

You can check headers before deciding whether to read the body:

```python
with client.stream("GET", "https://httpbin.org/get") as response:
    # Headers are available immediately
    content_type = response.headers.get("content-type")
    content_length = response.headers.get("content-length")

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return  # Don't read body

    if content_length and int(content_length) > 1_000_000:
        print("File too large!")
        return  # Don't read body

    # Only read if checks pass
    for chunk in response.iter_bytes():
        process(chunk)
```

### Reading All at Once

If you need to read the entire response after starting a stream:

```python
with client.stream("GET", "https://httpbin.org/get") as response:
    # Check headers first
    if response.status_code == 200:
        # Read entire remaining response
        content = response.read()
        print(f"Total size: {len(content)} bytes")
```

### Downloading Large Files

Streaming is ideal for downloading large files:

```python
import httpr

client = httpr.Client()

with client.stream("GET", "https://example.com/large-file.zip") as response:
    if response.status_code == 200:
        with open("large-file.zip", "wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
        print("Download complete!")
```

With progress tracking:

```python
with client.stream("GET", "https://example.com/large-file.zip") as response:
    total_size = int(response.headers.get("content-length", 0))
    downloaded = 0

    with open("large-file.zip", "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
            downloaded += len(chunk)
            if total_size:
                percent = (downloaded / total_size) * 100
                print(f"Downloaded: {percent:.1f}%", end="\r")
```

### Streaming with POST

Streaming works with all HTTP methods:

```python
with client.stream(
    "POST",
    "https://api.example.com/process",
    json={"input": "data"}
) as response:
    # Stream the API response
    for line in response.iter_lines():
        result = json.loads(line)
        print(result)
```

### Stream State

The streaming response tracks its state:

```python
with client.stream("GET", "https://httpbin.org/get") as response:
    print(response.is_closed)    # False
    print(response.is_consumed)  # False

    content = response.read()

    print(response.is_consumed)  # True (after reading)

print(response.is_closed)  # True (after context manager exits)
```

### Exception Handling

Streaming raises specific exceptions:

```python
import httpr

try:
    with client.stream("GET", "https://httpbin.org/get") as response:
        content = response.read()

        # This will raise StreamConsumed
        more = response.read()

except httpr.StreamConsumed:
    print("Cannot read stream twice")

except httpr.StreamClosed:
    print("Stream was closed")
```

### Async Streaming

The `AsyncClient` also supports streaming with the same API:

```python
import asyncio
import httpr

async def stream_data():
    async with httpr.AsyncClient() as client:
        async with client.stream("GET", "https://httpbin.org/stream-bytes/1000") as response:
            # Note: iteration is sync, but context manager is async
            for chunk in response.iter_bytes():
                process(chunk)

asyncio.run(stream_data())
```

!!! note
    With `AsyncClient`, the context manager is async (`async with`), but the iteration over chunks remains synchronous (regular `for` loop, not `async for`).

### Important Notes

- **Always use context manager**: The `with` statement ensures proper cleanup
- **Headers available immediately**: You can check status, headers, and cookies before reading the body
- **Cannot re-read**: Once the stream is consumed, you cannot read it again
- **Automatic cleanup**: The stream is automatically closed when the context manager exits

## Next Steps

- [Authentication](authentication.md) - Add authentication to requests
- [Async Client](async.md) - Use async/await for concurrent requests
