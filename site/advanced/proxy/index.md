# Proxy Configuration

httpr supports routing requests through HTTP and SOCKS5 proxy servers.

## Basic Proxy Usage

### HTTP Proxy

```python
import httpr

client = httpr.Client(proxy="http://proxy.example.com:8080")
response = client.get("https://httpbin.org/ip")
print(response.json())  # Shows proxy's IP
```

### HTTPS Proxy

```python
import httpr

client = httpr.Client(proxy="https://secure-proxy.example.com:8443")
response = client.get("https://httpbin.org/ip")
```

### SOCKS5 Proxy

```python
import httpr

# SOCKS5 proxy (e.g., Tor, SSH tunnel)
client = httpr.Client(proxy="socks5://127.0.0.1:1080")
response = client.get("https://httpbin.org/ip")
```

## Proxy Authentication

Include credentials in the proxy URL:

```python
import httpr

# HTTP proxy with auth
client = httpr.Client(
    proxy="http://username:password@proxy.example.com:8080"
)

# SOCKS5 proxy with auth
client = httpr.Client(
    proxy="socks5://user:pass@127.0.0.1:1080"
)
```

## Environment Variable

Set a default proxy using the `HTTPR_PROXY` environment variable:

```bash
# Set for HTTP proxy
export HTTPR_PROXY="http://proxy.example.com:8080"

# Set for SOCKS5 proxy
export HTTPR_PROXY="socks5://127.0.0.1:1080"
```

```python
import httpr

# Automatically uses HTTPR_PROXY
client = httpr.Client()
response = client.get("https://httpbin.org/ip")
```

The `proxy` parameter takes precedence over the environment variable:

```python
import httpr

# Uses specified proxy, ignores HTTPR_PROXY
client = httpr.Client(proxy="http://other-proxy:8080")
```

## Changing Proxy at Runtime

You can change the proxy on an existing client:

```python
import httpr

client = httpr.Client()

# Set proxy
client.proxy = "http://proxy.example.com:8080"

# Read current proxy
print(client.proxy)  # "http://proxy.example.com:8080"

# Remove proxy
client.proxy = None
```

Performance Note

Changing the `proxy` property **rebuilds the entire internal HTTP client**. This is an expensive operation. For best performance, create separate clients for different proxy configurations.

```python
import httpr

# Better: Create separate clients
direct_client = httpr.Client()
proxy_client = httpr.Client(proxy="http://proxy:8080")

# Avoid: Changing proxy repeatedly
client = httpr.Client()
for proxy in proxies:
    client.proxy = proxy  # Rebuilds client each time!
    client.get(url)
```

## Use Cases

### Corporate Proxy

Route traffic through a corporate proxy server:

```python
import os
import httpr

def get_corporate_client() -> httpr.Client:
    """Create client configured for corporate network."""
    proxy = os.environ.get("CORPORATE_PROXY", "http://proxy.corp:8080")
    ca_bundle = os.environ.get("CORPORATE_CA", "/etc/ssl/corp-ca.pem")

    return httpr.Client(
        proxy=proxy,
        ca_cert_file=ca_bundle,
        timeout=30,
    )

with get_corporate_client() as client:
    response = client.get("https://api.example.com/data")
```

### Tor Network

Route requests through Tor for anonymity:

```python
import httpr

# Tor SOCKS5 proxy (default port 9050)
tor_client = httpr.Client(proxy="socks5://127.0.0.1:9050")

# Check Tor connection
response = tor_client.get("https://check.torproject.org/api/ip")
print(response.json())  # {"IsTor": true, "IP": "..."}
```

### SSH Tunnel

Use an SSH SOCKS tunnel:

```bash
# Create SSH tunnel (in terminal)
ssh -D 1080 -N user@server.example.com
```

```python
import httpr

# Use SSH tunnel
client = httpr.Client(proxy="socks5://127.0.0.1:1080")
response = client.get("https://httpbin.org/ip")
```

### Rotating Proxies

Use different proxies for different requests:

```python
import httpr

proxies = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
]

def fetch_with_rotation(urls: list[str]) -> list[dict]:
    """Fetch URLs using rotating proxies."""
    results = []

    for i, url in enumerate(urls):
        proxy = proxies[i % len(proxies)]

        with httpr.Client(proxy=proxy) as client:
            response = client.get(url)
            results.append({
                "url": url,
                "proxy": proxy,
                "status": response.status_code
            })

    return results
```

### Conditional Proxy

Use proxy only for certain hosts:

```python
import httpr
from urllib.parse import urlparse

class ProxyRouter:
    """Route requests through proxy based on host."""

    def __init__(self, proxy: str, proxy_hosts: set[str]):
        self.proxy_client = httpr.Client(proxy=proxy)
        self.direct_client = httpr.Client()
        self.proxy_hosts = proxy_hosts

    def get(self, url: str, **kwargs):
        host = urlparse(url).netloc
        if host in self.proxy_hosts:
            return self.proxy_client.get(url, **kwargs)
        return self.direct_client.get(url, **kwargs)

    def close(self):
        self.proxy_client.close()
        self.direct_client.close()

# Usage
router = ProxyRouter(
    proxy="http://proxy:8080",
    proxy_hosts={"api.external.com", "data.external.com"}
)

# Direct connection
router.get("https://api.internal.com/data")

# Through proxy
router.get("https://api.external.com/data")
```

## Async Client with Proxy

Proxy configuration works the same with `AsyncClient`:

```python
import asyncio
import httpr

async def main():
    async with httpr.AsyncClient(proxy="http://proxy:8080") as client:
        response = await client.get("https://httpbin.org/ip")
        print(response.json())

asyncio.run(main())
```

## Supported Proxy Protocols

| Protocol | URL Format           | Notes                      |
| -------- | -------------------- | -------------------------- |
| HTTP     | `http://host:port`   | Most common                |
| HTTPS    | `https://host:port`  | Encrypted proxy connection |
| SOCKS5   | `socks5://host:port` | Supports TCP               |

Note

SOCKS4 and SOCKS4a are not currently supported. Use SOCKS5 instead.

## Troubleshooting

### Connection Refused

```text
connection refused
```

- Verify proxy host and port are correct
- Check if proxy server is running
- Ensure firewall allows connection to proxy

### Authentication Failed

```text
proxy authentication required
```

- Include credentials in proxy URL: `http://user:pass@proxy:8080`
- Verify credentials are correct
- Check if proxy requires specific auth method

### Timeout Through Proxy

- Increase timeout: `httpr.Client(proxy=proxy, timeout=60)`
- Proxy may be slow or overloaded
- Try a different proxy server

### SSL Errors Through Proxy

- Some proxies intercept HTTPS traffic
- May need to add proxy's CA certificate to `ca_cert_file`
- Or use SOCKS5 proxy for end-to-end encryption
