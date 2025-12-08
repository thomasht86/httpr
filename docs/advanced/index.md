# Advanced Features

This section covers advanced httpr features for production use cases.

<div class="grid cards" markdown>

-   :material-shield-lock:{ .lg .middle } **SSL/TLS & mTLS**

    ---

    Configure SSL certificates, CA bundles, and mutual TLS authentication.

    [:octicons-arrow-right-24: SSL/TLS Guide](ssl-tls.md)

-   :material-server-network:{ .lg .middle } **Proxy Configuration**

    ---

    Route requests through HTTP and SOCKS proxies.

    [:octicons-arrow-right-24: Proxy Guide](proxy.md)

-   :material-cookie:{ .lg .middle } **Cookie Handling**

    ---

    Manage cookies with persistent cookie store and manual control.

    [:octicons-arrow-right-24: Cookie Guide](cookies.md)

</div>

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

[:octicons-arrow-right-24: Learn more about SSL/TLS](ssl-tls.md)

### Proxy Support

Route requests through proxy servers:

```python
import httpr

# HTTP proxy
client = httpr.Client(proxy="http://proxy.example.com:8080")

# SOCKS5 proxy
client = httpr.Client(proxy="socks5://127.0.0.1:1080")
```

[:octicons-arrow-right-24: Learn more about proxies](proxy.md)

### Cookie Management

Automatic cookie handling with fine-grained control:

```python
import httpr

# Persistent cookie store (default)
client = httpr.Client(cookie_store=True)

# Manual cookie management
client = httpr.Client(cookies={"session": "abc123"})
```

[:octicons-arrow-right-24: Learn more about cookies](cookies.md)

## Environment Variables

httpr respects these environment variables:

| Variable | Description |
|----------|-------------|
| `HTTPR_PROXY` | Default proxy URL |
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
