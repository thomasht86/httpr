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

## Next Steps

- [Authentication](authentication.md) - Add authentication to requests
- [Async Client](async.md) - Use async/await for concurrent requests
