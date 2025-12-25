#!/usr/bin/env python3
"""Generate SSL certificates for e2e testing using trustme.

Creates a CA and server certificate for httpbun.local in the .certs/ directory.
"""

import os
from pathlib import Path

import trustme


def main() -> None:
    # Create .certs directory at project root
    certs_dir = Path(__file__).parent.parent / ".certs"
    certs_dir.mkdir(exist_ok=True)

    # Generate CA
    ca = trustme.CA()

    # Generate server certificate for httpbun.local
    server_cert = ca.issue_cert("httpbun.local")

    # Save CA certificate (for client verification)
    ca_cert_path = certs_dir / "ca.pem"
    ca.cert_pem.write_to_path(str(ca_cert_path))
    print(f"CA certificate: {ca_cert_path}")

    # Save server certificate and key (for httpbun container)
    server_cert_path = certs_dir / "server.pem"
    server_key_path = certs_dir / "server.key"

    # trustme bundles cert chain, write it properly
    server_cert.private_key_pem.write_to_path(str(server_key_path))

    # Write server cert (combines all cert blobs)
    with open(server_cert_path, "wb") as f:
        for blob in server_cert.cert_chain_pems:
            f.write(blob.bytes())

    print(f"Server certificate: {server_cert_path}")
    print(f"Server key: {server_key_path}")

    # Make key readable only by owner
    os.chmod(server_key_path, 0o600)

    print("\nCertificates generated successfully!")
    print(f"  CA cert (for httpr client): {ca_cert_path}")
    print(f"  Server cert (for httpbun): {server_cert_path}")
    print(f"  Server key (for httpbun): {server_key_path}")


if __name__ == "__main__":
    main()
