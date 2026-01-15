# SSL/TLS & mTLS

This guide covers SSL/TLS configuration in httpr, including certificate verification, custom CA bundles, and mutual TLS (mTLS) authentication.

## Overview

By default, httpr verifies SSL/TLS certificates using the system's certificate store. You can customize this behavior for:

- Corporate/internal certificates
- Self-signed certificates (development)
- Client certificate authentication (mTLS)

## Certificate Verification

### Default Behavior

SSL certificate verification is enabled by default:

```python
import httpr

# Verification enabled (default)
client = httpr.Client(verify=True)
response = client.get("https://example.com")  # Certificate is verified
```

### Disabling Verification

Security Warning

Disabling certificate verification exposes you to man-in-the-middle attacks. Only use this for local development or testing.

```python
import httpr

# Disable verification (insecure!)
client = httpr.Client(verify=False)
response = client.get("https://self-signed.badssl.com/")
```

## Custom CA Certificates

### Using a Custom CA Bundle

For corporate environments or internal services with custom certificate authorities:

```python
import httpr

# Specify custom CA bundle
client = httpr.Client(ca_cert_file="/path/to/ca-bundle.pem")
response = client.get("https://internal.company.com/api")
```

### Using certifi

The popular `certifi` package provides Mozilla's CA bundle:

```python
import certifi
import httpr

client = httpr.Client(ca_cert_file=certifi.where())
response = client.get("https://example.com")
```

### Environment Variable

Set the CA bundle via environment variable:

```bash
export HTTPR_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
```

```python
import httpr

# Automatically uses HTTPR_CA_BUNDLE
client = httpr.Client()
```

Note

The `ca_cert_file` parameter internally sets the `HTTPR_CA_BUNDLE` environment variable.

## mTLS (Mutual TLS)

Mutual TLS requires both the server and client to present certificates. This is common in:

- Zero-trust architectures
- Service mesh communication
- Banking and financial APIs
- IoT device authentication

### Configuration

```python
import httpr

client = httpr.Client(
    client_pem="/path/to/client-cert.pem",  # Client certificate + key
    ca_cert_file="/path/to/ca-bundle.pem"    # CA to verify server
)

response = client.get("https://mtls.example.com/api")
```

### Certificate Format

The `client_pem` file should contain both the certificate and private key in PEM format:

```text
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiUMA0Gcq...
-----END CERTIFICATE-----
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwgg...
-----END PRIVATE KEY-----
```

### Complete mTLS Example

```python
import httpr

def create_mtls_client(
    client_cert: str,
    ca_bundle: str,
    timeout: float = 30
) -> httpr.Client:
    """Create a client configured for mTLS."""
    return httpr.Client(
        client_pem=client_cert,
        ca_cert_file=ca_bundle,
        timeout=timeout,
        verify=True,  # Must be True for mTLS
    )

# Usage
client = create_mtls_client(
    client_cert="/certs/client.pem",
    ca_bundle="/certs/ca.pem"
)

with client:
    response = client.get("https://secure-api.example.com/data")
    print(response.json())
```

## HTTP/2

httpr supports HTTP/2 over TLS:

```python
import httpr

# HTTP/2 only mode
client = httpr.Client(http2_only=True)
response = client.get("https://http2.example.com")
```

Note

HTTP/2 requires TLS. The `http2_only` option forces HTTP/2 protocol. When `http2_only=False` (default), httpr uses HTTP/1.1.

## HTTPS Only Mode

Restrict the client to HTTPS connections only:

```python
import httpr

client = httpr.Client(https_only=True)

# Works
response = client.get("https://example.com")

# Raises an error
# response = client.get("http://example.com")
```

This is useful for ensuring all traffic is encrypted, especially when handling sensitive data.

## Testing with Self-Signed Certificates

For local development with self-signed certificates:

### Using trustme (Python testing)

```python
import trustme
import httpr

# Generate test CA and certificates
ca = trustme.CA()
server_cert = ca.issue_cert("localhost")

# Export certificates
ca.cert_pem.write_to_path("test-ca.pem")
server_cert.private_key_and_cert_chain_pem.write_to_path("server.pem")

# Use in httpr
client = httpr.Client(ca_cert_file="test-ca.pem")
```

### Development Configuration

```python
import os
import httpr

def get_client() -> httpr.Client:
    """Get configured client based on environment."""
    if os.environ.get("ENVIRONMENT") == "development":
        # Development: Use test CA or disable verification
        return httpr.Client(
            ca_cert_file=os.environ.get("DEV_CA_BUNDLE"),
            verify=bool(os.environ.get("DEV_CA_BUNDLE"))
        )
    else:
        # Production: Use system CA bundle
        return httpr.Client(verify=True)
```

## Troubleshooting

### Certificate Errors

**"certificate verify failed"**

The server's certificate is not trusted:

1. Check if the certificate is expired
1. Verify the CA bundle includes the issuing CA
1. For internal CAs, specify the correct `ca_cert_file`

```python
import httpr

# Try with certifi's CA bundle
import certifi
client = httpr.Client(ca_cert_file=certifi.where())
```

**"unable to get local issuer certificate"**

The CA certificate chain is incomplete:

1. Ensure your CA bundle includes intermediate certificates
1. Try using a complete CA bundle

**"wrong version number" or "SSL handshake failed"**

Protocol mismatch:

1. Server may not support modern TLS versions
1. Try `http2_only=False` if using HTTP/2

### mTLS Errors

**"no client certificate presented"**

1. Verify `client_pem` file path is correct
1. Check the PEM file contains both cert and key
1. Ensure `verify=True` is set

**"certificate signature failure"**

1. Client certificate not signed by expected CA
1. Certificate may have been revoked

## Security Recommendations

1. **Always verify certificates in production** - Never use `verify=False`
1. **Keep CA bundles updated** - Use system CA or update certifi regularly
1. **Protect private keys** - Secure `client_pem` files with appropriate permissions
1. **Use HTTPS everywhere** - Consider `https_only=True` for sensitive applications
1. **Rotate certificates** - Implement certificate rotation for mTLS

```python
import httpr

# Production-ready client
client = httpr.Client(
    verify=True,           # Always verify
    https_only=True,       # HTTPS only
    timeout=30,            # Reasonable timeout
    # ca_cert_file=...,    # Custom CA if needed
    # client_pem=...,      # mTLS if required
)
```
