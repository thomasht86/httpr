# Advanced Features

This section covers advanced httpr features for production use cases.

- **SSL/TLS & mTLS**

  ______________________________________________________________________

  Configure SSL certificates, CA bundles, and mutual TLS authentication.

  [SSL/TLS Guide](https://thomasht86.github.io/httpr/advanced/ssl-tls/index.md)

- **Proxy Configuration**

  ______________________________________________________________________

  Route requests through HTTP and SOCKS proxies.

  [Proxy Guide](https://thomasht86.github.io/httpr/advanced/proxy/index.md)

- **Cookie Handling**

  ______________________________________________________________________

  Manage cookies with persistent cookie store and manual control.

  [Cookie Guide](https://thomasht86.github.io/httpr/advanced/cookies/index.md)

## Overview

### SSL/TLS

httpr provides full SSL/TLS support:

- **Certificate verification** (enabled by default)
- **Custom CA bundles** for corporate/internal certificates
- **mTLS (mutual TLS)** for client certificate authentication
- **HTTP/2** with TLS

```python
import httpr

# Custom CA certificate
client = httpr.Client(ca_cert_file="/path/to/ca-bundle.pem")

# mTLS with client certificate
client = httpr.Client(
    client_pem="/path/to/client.pem",
    ca_cert_file="/path/to/ca-bundle.pem"
)
```

[Learn more about SSL/TLS](https://thomasht86.github.io/httpr/advanced/ssl-tls/index.md)

### Proxy Support

Route requests through proxy servers:

```python
import httpr

# HTTP proxy
client = httpr.Client(proxy="http://proxy.example.com:8080")

# SOCKS5 proxy
client = httpr.Client(proxy="socks5://127.0.0.1:1080")
```

[Learn more about proxies](https://thomasht86.github.io/httpr/advanced/proxy/index.md)

### Cookie Management

Automatic cookie handling with fine-grained control:

```python
import httpr

# Persistent cookie store (default)
client = httpr.Client(cookie_store=True)

# Manual cookie management
client = httpr.Client(cookies={"session": "abc123"})
```

[Learn more about cookies](https://thomasht86.github.io/httpr/advanced/cookies/index.md)

## Environment Variables

httpr respects these environment variables:

| Variable          | Description                   |
| ----------------- | ----------------------------- |
| `HTTPR_PROXY`     | Default proxy URL             |
| `HTTPR_CA_BUNDLE` | Path to CA certificate bundle |

```bash
# Set proxy for all httpr clients
export HTTPR_PROXY="http://proxy:8080"

# Set CA bundle
export HTTPR_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
```

## Best Practices

### Connection Pooling

Use a single `Client` instance for multiple requests to the same host:

```python
import httpr

# Good: Reuse client
with httpr.Client() as client:
    for url in urls:
        response = client.get(url)

# Bad: New client per request
for url in urls:
    response = httpr.get(url)  # Creates new client each time
```

### Timeout Configuration

Set appropriate timeouts for your use case:

```python
import httpr

# API calls - shorter timeout
api_client = httpr.Client(timeout=10)

# File downloads - longer timeout
download_client = httpr.Client(timeout=300)
```

### Error Handling

```python
import httpr

try:
    response = httpr.get("https://api.example.com/data")
    response_data = response.json()
except Exception as e:
    # Handle connection errors, timeouts, etc.
    print(f"Request failed: {e}")
```

### Resource Cleanup

Always close clients when done:

```python
import httpr

# Best: Context manager
with httpr.Client() as client:
    response = client.get(url)

# Alternative: Manual close
client = httpr.Client()
try:
    response = client.get(url)
finally:
    client.close()
```
