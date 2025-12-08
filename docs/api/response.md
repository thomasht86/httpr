# Response

The HTTP response object returned by all request methods.

## Overview

The `Response` class provides access to all aspects of an HTTP response:

```python
import httpr

response = httpr.get("https://httpbin.org/get")

# Status
print(response.status_code)  # 200

# Body
print(response.text)         # Decoded text
print(response.content)      # Raw bytes
data = response.json()       # Parsed JSON

# Headers (case-insensitive)
print(response.headers["content-type"])
print(response.headers["Content-Type"])  # Same result

# Cookies
print(response.cookies)      # {"session": "value"}

# Metadata
print(response.url)          # Final URL after redirects
print(response.encoding)     # Detected encoding
```

## Properties

### status_code

```python
@property
def status_code(self) -> int
```

HTTP status code (e.g., 200, 404, 500).

**Example:**
```python
response = httpr.get("https://httpbin.org/status/201")
print(response.status_code)  # 201
```

---

### text

```python
@property
def text(self) -> str
```

Response body decoded as text.

Encoding is automatically detected from:

1. `Content-Type` header charset
2. HTML meta charset tag
3. Falls back to UTF-8

**Example:**
```python
response = httpr.get("https://httpbin.org/html")
print(response.text)  # HTML content
```

---

### content

```python
@property
def content(self) -> bytes
```

Response body as raw bytes.

**Example:**
```python
response = httpr.get("https://httpbin.org/bytes/100")
print(len(response.content))  # 100

# Save binary file
response = httpr.get("https://httpbin.org/image/png")
with open("image.png", "wb") as f:
    f.write(response.content)
```

---

### headers

```python
@property
def headers(self) -> CaseInsensitiveHeaderMap
```

Response headers as a case-insensitive dict-like object.

Supports:

- `response.headers["Content-Type"]` - get by key
- `response.headers.get("content-type", "default")` - get with default
- `"content-type" in response.headers` - check existence
- `response.headers.keys()` - all header names
- `response.headers.values()` - all header values
- `response.headers.items()` - key-value pairs

**Example:**
```python
response = httpr.get("https://httpbin.org/get")

# Case-insensitive access
print(response.headers["content-type"])
print(response.headers["Content-Type"])  # Same

# Iteration
for name, value in response.headers.items():
    print(f"{name}: {value}")
```

---

### cookies

```python
@property
def cookies(self) -> dict[str, str]
```

Cookies set by the server via `Set-Cookie` headers.

**Example:**
```python
response = httpr.get("https://httpbin.org/cookies/set?name=value")
print(response.cookies)  # {"name": "value"}
```

---

### url

```python
@property
def url(self) -> str
```

Final URL after following any redirects.

**Example:**
```python
response = httpr.get("https://httpbin.org/redirect/3")
print(response.url)  # https://httpbin.org/get
```

---

### encoding

```python
@property
def encoding(self) -> str
```

Character encoding detected from response headers or content.

**Example:**
```python
response = httpr.get("https://httpbin.org/encoding/utf8")
print(response.encoding)  # "utf-8"
```

---

### text_markdown

```python
@property
def text_markdown(self) -> str
```

HTML response body converted to Markdown format.

Uses Rust's `html2text` crate for conversion.

**Example:**
```python
response = httpr.get("https://example.com")
print(response.text_markdown)
# # Example Domain
#
# This domain is for use in illustrative examples...
```

---

### text_plain

```python
@property
def text_plain(self) -> str
```

HTML response body converted to plain text (no formatting).

**Example:**
```python
response = httpr.get("https://example.com")
print(response.text_plain)
```

---

### text_rich

```python
@property
def text_rich(self) -> str
```

HTML response body converted to rich text format.

---

## Methods

### json

```python
def json(self) -> Any
```

Parse response body as JSON.

**Returns:** Parsed JSON (dict, list, str, int, float, bool, or None)

**Raises:** Exception if body is not valid JSON

**Example:**
```python
response = httpr.get("https://httpbin.org/json")
data = response.json()
print(data["slideshow"]["title"])
```

!!! note
    `json()` is a method, not a property. Call it with parentheses.
