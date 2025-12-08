# Authentication

httpr supports multiple authentication methods for securing your HTTP requests.

## Basic Authentication

HTTP Basic Authentication sends username and password encoded in the request header.

### Per-Request Authentication

```python
import httpr

response = httpr.get(
    "https://httpbin.org/basic-auth/user/pass",
    auth=("user", "pass")
)
print(response.status_code)  # 200
```

### Client Default Authentication

Set authentication for all requests from a client:

```python
import httpr

client = httpr.Client(auth=("username", "password"))

# All requests include Basic Auth header
response = client.get("https://api.example.com/protected")
response = client.get("https://api.example.com/another-endpoint")
```

### Password-less Basic Auth

Some APIs require only a username (API key) without a password:

```python
import httpr

# Password can be None
response = httpr.get(
    "https://api.example.com/data",
    auth=("api_key_here", None)
)
```

### How It Works

Basic auth creates an `Authorization` header with base64-encoded credentials:

```python
import httpr

response = httpr.get(
    "https://httpbin.org/headers",
    auth=("user", "password")
)

# The Authorization header is automatically set
auth_header = response.json()["headers"]["Authorization"]
print(auth_header)  # "Basic dXNlcjpwYXNzd29yZA=="
```

## Bearer Token Authentication

Bearer tokens are commonly used for OAuth 2.0 and API authentication.

### Per-Request Bearer Token

```python
import httpr

response = httpr.get(
    "https://api.example.com/data",
    auth_bearer="your-token-here"
)
```

### Client Default Bearer Token

```python
import httpr

client = httpr.Client(auth_bearer="your-api-token")

# All requests include the Bearer token
response = client.get("https://api.example.com/users")
response = client.get("https://api.example.com/posts")
```

### How It Works

Bearer auth creates an `Authorization: Bearer <token>` header:

```python
import httpr

response = httpr.get(
    "https://httpbin.org/headers",
    auth_bearer="my-secret-token"
)

auth_header = response.json()["headers"]["Authorization"]
print(auth_header)  # "Bearer my-secret-token"
```

## Custom Authentication Headers

For APIs that use non-standard authentication headers:

```python
import httpr

# API key in custom header
response = httpr.get(
    "https://api.example.com/data",
    headers={"X-API-Key": "your-api-key"}
)

# Multiple auth headers
client = httpr.Client(
    headers={
        "X-API-Key": "key123",
        "X-API-Secret": "secret456"
    }
)
```

## Updating Authentication

You can update client authentication after creation:

```python
import httpr

client = httpr.Client()

# Set auth via property
client.auth = ("new-user", "new-pass")
print(client.auth)  # ("new-user", "new-pass")

# Or use headers directly for bearer tokens
client.headers = {"Authorization": "Bearer new-token"}
```

## Authentication Patterns

### API with Token Refresh

```python
import httpr

class ApiClient:
    def __init__(self, token: str):
        self.client = httpr.Client(auth_bearer=token)

    def refresh_token(self, new_token: str):
        """Update the bearer token."""
        self.client = httpr.Client(auth_bearer=new_token)

    def get_users(self):
        return self.client.get("https://api.example.com/users").json()

# Usage
api = ApiClient("initial-token")
users = api.get_users()

# When token expires
api.refresh_token("refreshed-token")
users = api.get_users()
```

### Environment-Based Auth

```python
import os
import httpr

# Load credentials from environment
api_token = os.environ.get("API_TOKEN")
if not api_token:
    raise ValueError("API_TOKEN environment variable required")

client = httpr.Client(auth_bearer=api_token)
```

### Different Auth per Endpoint

```python
import httpr

# Public API - no auth
public_client = httpr.Client()
public_data = public_client.get("https://api.example.com/public").json()

# Authenticated API
auth_client = httpr.Client(auth_bearer="secret-token")
private_data = auth_client.get("https://api.example.com/private").json()
```

## mTLS Authentication

For mutual TLS (client certificate authentication), see the [SSL/TLS Guide](../advanced/ssl-tls.md#mtls-mutual-tls).

```python
import httpr

# Client certificate authentication
client = httpr.Client(
    client_pem="/path/to/client-cert.pem",
    ca_cert_file="/path/to/ca-bundle.pem"
)
```

## Security Best Practices

!!! warning "Security Tips"

    1. **Never hardcode credentials** in source code
    2. **Use environment variables** or secure vaults for secrets
    3. **Use HTTPS** for all authenticated requests
    4. **Rotate tokens** regularly
    5. **Use short-lived tokens** when possible

```python
import os
import httpr

# Good: Load from environment
client = httpr.Client(
    auth_bearer=os.environ["API_TOKEN"],
    https_only=True  # Enforce HTTPS
)

# Bad: Hardcoded credentials (don't do this!)
# client = httpr.Client(auth=("admin", "password123"))
```

## Complete Example

```python
import os
import httpr

def create_api_client() -> httpr.Client:
    """Create an authenticated API client."""

    # Get token from environment
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not set")

    return httpr.Client(
        auth_bearer=token,
        headers={"Accept": "application/vnd.github.v3+json"},
        timeout=30,
    )

def get_user_repos(client: httpr.Client, username: str) -> list:
    """Get repositories for a GitHub user."""
    response = client.get(
        f"https://api.github.com/users/{username}/repos",
        params={"per_page": 10, "sort": "updated"}
    )

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise ValueError("Invalid or expired token")
    else:
        raise Exception(f"API error: {response.status_code}")

# Usage
if __name__ == "__main__":
    client = create_api_client()
    repos = get_user_repos(client, "thomasht86")
    for repo in repos:
        print(f"- {repo['name']}: {repo['description']}")
```

## Next Steps

- [Async Client](async.md) - Make concurrent authenticated requests
- [SSL/TLS](../advanced/ssl-tls.md) - Client certificate authentication (mTLS)
