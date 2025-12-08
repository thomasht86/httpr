# Cookie Handling

httpr provides automatic cookie management with a persistent cookie store. This guide covers how cookies work and how to control them.

## Cookie Store

By default, httpr maintains a persistent cookie store that:

- Automatically stores cookies from `Set-Cookie` response headers
- Sends stored cookies with subsequent requests to matching domains
- Handles cookie expiration and path matching

### Default Behavior

```python
import httpr

client = httpr.Client(cookie_store=True)  # Default

# First request - server sets a cookie
client.get("https://httpbin.org/cookies/set?session=abc123")

# Second request - cookie is automatically included
response = client.get("https://httpbin.org/cookies")
print(response.json())  # {"cookies": {"session": "abc123"}}
```

### Disabling Cookie Store

For stateless requests, disable the cookie store:

```python
import httpr

client = httpr.Client(cookie_store=False)

# Cookie is set but not persisted
client.get("https://httpbin.org/cookies/set?session=abc123")

# Cookie not sent in subsequent request
response = client.get("https://httpbin.org/cookies")
print(response.json())  # {"cookies": {}}
```

## Sending Cookies

### Initial Cookies

Set cookies when creating the client:

```python
import httpr

client = httpr.Client(
    cookies={
        "session": "abc123",
        "user_id": "456"
    }
)

response = client.get("https://httpbin.org/cookies")
print(response.json())  # {"cookies": {"session": "abc123", "user_id": "456"}}
```

### Per-Request Cookies

Send cookies with specific requests:

```python
import httpr

client = httpr.Client()

response = client.get(
    "https://httpbin.org/cookies",
    cookies={"temporary": "cookie-value"}
)
print(response.json())  # {"cookies": {"temporary": "cookie-value"}}
```

Per-request cookies are merged with client-level cookies:

```python
import httpr

client = httpr.Client(cookies={"persistent": "value1"})

response = client.get(
    "https://httpbin.org/cookies",
    cookies={"temporary": "value2"}
)
# Both cookies sent
print(response.json())  # {"cookies": {"persistent": "value1", "temporary": "value2"}}
```

## Reading Cookies

### From Response

Access cookies set by the server:

```python
import httpr

response = httpr.get("https://httpbin.org/cookies/set?name=value")
print(response.cookies)  # {"name": "value"}
```

### From Client

Get the current cookies on a client:

```python
import httpr

client = httpr.Client(cookies={"initial": "cookie"})
print(client.cookies)  # {"initial": "cookie"}

# After server sets more cookies
client.get("https://httpbin.org/cookies/set?new=cookie")
# Note: client.cookies may not reflect all cookies from cookie_store
```

## Updating Cookies

### Set Cookies

Update client cookies after creation:

```python
import httpr

client = httpr.Client()

# Set new cookies
client.cookies = {"session": "new-session-id"}

# Read current cookies
print(client.cookies)  # {"session": "new-session-id"}
```

### Clear Cookies

Clear all client cookies:

```python
import httpr

client = httpr.Client(cookies={"old": "cookie"})

# Clear cookies
client.cookies = {}
```

## Cookie Header Format

Cookies are sent as a single `Cookie` header:

```python
import httpr

response = httpr.get(
    "https://httpbin.org/headers",
    cookies={"name1": "value1", "name2": "value2"}
)

# Check the Cookie header that was sent
headers = response.json()["headers"]
print(headers["Cookie"])  # "name1=value1; name2=value2"
```

!!! note
    The `client.headers` getter excludes the `Cookie` header.
    Use `client.cookies` to access cookies separately.

## Use Cases

### Session Management

Maintain authenticated sessions:

```python
import httpr

class ApiSession:
    """Manage API session with cookies."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpr.Client(cookie_store=True)

    def login(self, username: str, password: str) -> bool:
        """Login and store session cookie."""
        response = self.client.post(
            f"{self.base_url}/login",
            data={"username": username, "password": password}
        )
        return response.status_code == 200

    def get_profile(self) -> dict:
        """Get user profile (requires login)."""
        response = self.client.get(f"{self.base_url}/profile")
        return response.json()

    def logout(self):
        """Logout and clear session."""
        self.client.post(f"{self.base_url}/logout")
        self.client.cookies = {}

    def close(self):
        self.client.close()

# Usage
session = ApiSession("https://api.example.com")
session.login("user", "password")
profile = session.get_profile()
session.logout()
session.close()
```

### Testing with Specific Cookies

```python
import httpr

def test_authenticated_endpoint():
    """Test endpoint with mock session cookie."""
    client = httpr.Client(
        cookies={"session": "test-session-token"},
        cookie_store=False  # Don't persist new cookies
    )

    response = client.get("https://api.example.com/protected")
    assert response.status_code == 200
```

### Multiple Sessions

Handle multiple user sessions:

```python
import httpr

class MultiUserClient:
    """Manage multiple user sessions."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.sessions: dict[str, httpr.Client] = {}

    def get_session(self, user_id: str) -> httpr.Client:
        """Get or create session for user."""
        if user_id not in self.sessions:
            self.sessions[user_id] = httpr.Client(cookie_store=True)
        return self.sessions[user_id]

    def login(self, user_id: str, credentials: dict) -> bool:
        """Login as specific user."""
        client = self.get_session(user_id)
        response = client.post(f"{self.base_url}/login", data=credentials)
        return response.status_code == 200

    def request(self, user_id: str, method: str, path: str, **kwargs):
        """Make request as specific user."""
        client = self.get_session(user_id)
        return client.request(method, f"{self.base_url}{path}", **kwargs)

    def close(self):
        """Close all sessions."""
        for client in self.sessions.values():
            client.close()
```

### Cookie Debugging

Inspect cookies for debugging:

```python
import httpr

def debug_cookies(url: str):
    """Debug cookie flow for a URL."""
    client = httpr.Client(cookie_store=True)

    print(f"Initial cookies: {client.cookies}")

    response = client.get(url)

    print(f"Response cookies: {response.cookies}")
    print(f"Client cookies after: {client.cookies}")

    return response

debug_cookies("https://httpbin.org/cookies/set?debug=true")
```

## Cookie Behavior Details

### Cookie Store vs Manual Cookies

| Feature | `cookie_store=True` | `cookie_store=False` |
|---------|---------------------|----------------------|
| Store response cookies | Yes | No |
| Send stored cookies | Yes | No |
| Use `cookies` param | Yes | Yes |
| Session persistence | Yes | No |

### Header Exclusion

The `client.headers` property excludes the `Cookie` header:

```python
import httpr

client = httpr.Client(
    headers={"X-Custom": "header"},
    cookies={"session": "abc"}
)

print(client.headers)   # {"x-custom": "header"} - no Cookie header
print(client.cookies)   # {"session": "abc"}
```

This separation allows independent management of headers and cookies.

## Async Client

Cookie handling works identically with `AsyncClient`:

```python
import asyncio
import httpr

async def main():
    async with httpr.AsyncClient(cookie_store=True) as client:
        # Set cookie
        await client.get("https://httpbin.org/cookies/set?async=cookie")

        # Cookie persists
        response = await client.get("https://httpbin.org/cookies")
        print(response.json())  # {"cookies": {"async": "cookie"}}

asyncio.run(main())
```
