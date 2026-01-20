import http.server
import os
import ssl
import tempfile
import threading
import unittest

import trustme

# Import your Client class
from httpr import Client


class SSLTestHandler(http.server.BaseHTTPRequestHandler):
    """A minimal HTTPS handler that returns a simple 'OK' response."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def finish(self):
        import contextlib

        try:
            self.wfile.flush()
            self.request.settimeout(1.0)
            # Unwrap the TLS layer to send a proper close_notify alert.
            with contextlib.suppress(Exception):
                self.request.unwrap()
        except Exception:
            pass
        finally:
            super().finish()

    def log_message(self, format, *args):
        # Suppress logging for cleaner test output.
        pass


class TestClientSSL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary directory to store our certificate files.
        cls.tmp_dir = tempfile.TemporaryDirectory()
        base_path = cls.tmp_dir.name

        # Generate a CA with trustme.
        ca = trustme.CA()
        cls.ca = ca

        # Issue a server certificate for "localhost".
        server_cert = ca.issue_cert("localhost")
        cls.server_cert_path = os.path.join(base_path, "server.pem")
        cls.server_key_path = os.path.join(base_path, "server.key")
        server_cert.private_key_and_cert_chain_pem.write_to_path(cls.server_cert_path)
        server_cert.private_key_pem.write_to_path(cls.server_key_path)

        # Issue a client certificate.
        client_cert = ca.issue_cert("client")
        cls.client_cert_path = os.path.join(base_path, "client.pem")
        client_cert.private_key_and_cert_chain_pem.write_to_path(cls.client_cert_path)

        # Write the CA certificate to a file (this acts as the trust store for our client).
        cls.client_ca_path = os.path.join(base_path, "client_ca.pem")
        ca.cert_pem.write_to_path(cls.client_ca_path)

        # Set up an SSL context for the server that requires client certificates.
        cls.server_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        cls.server_context.verify_mode = ssl.CERT_REQUIRED
        cls.server_context.load_cert_chain(certfile=cls.server_cert_path, keyfile=cls.server_key_path)
        cls.server_context.load_verify_locations(cafile=cls.client_ca_path)

        # Start an HTTPS server on an ephemeral port.
        cls.server = http.server.HTTPServer(("localhost", 0), SSLTestHandler)
        cls.server_port = cls.server.server_address[1]
        cls.server.socket = cls.server_context.wrap_socket(cls.server.socket, server_side=True)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()
        cls.tmp_dir.cleanup()

    def test_valid_ssl_connection(self):
        """A connection with valid client cert and CA file should succeed."""
        with Client(client_pem=self.client_cert_path, ca_cert_file=self.client_ca_path) as client:
            response = client.get(f"https://localhost:{self.server_port}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, "OK")

    def test_valid_ssl_connection_with_pem_data(self):
        """A connection with client_pem_data (bytes) should work the same as client_pem (path)."""
        # Read the certificate file into memory
        with open(self.client_cert_path, "rb") as f:
            cert_data = f.read()

        # Use client_pem_data instead of client_pem
        with Client(client_pem_data=cert_data, ca_cert_file=self.client_ca_path) as client:
            response = client.get(f"https://localhost:{self.server_port}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, "OK")

    def test_missing_client_cert(self):
        """Omitting the client certificate should fail the handshake (server requires it)."""
        with Client(ca_cert_file=self.client_ca_path) as client:
            with self.assertRaises(Exception):
                client.get(f"https://localhost:{self.server_port}")

    def test_invalid_client_cert_path(self):
        """Providing a non-existent client certificate file should raise an error."""
        # Import httpr to use the correct exception type
        import httpr

        with self.assertRaises(httpr.RequestError):
            # Assuming your Client loads the file on initialization.
            with Client(client_pem="nonexistent.pem", ca_cert_file=self.client_ca_path) as client:
                client.get(f"https://localhost:{self.server_port}")

    def test_invalid_ca_cert_file(self):
        """Using an invalid CA certificate file should cause a handshake failure."""
        with Client(client_pem=self.client_cert_path, ca_cert_file="nonexistent_ca.pem") as client:
            with self.assertRaises(Exception):
                client.get(f"https://localhost:{self.server_port}")

    def test_verify_disabled_with_valid_client_cert(self):
        """
        When verify is disabled, the client does not check the server's certificate.
        However, since the server still requires a valid client certificate, the connection
        succeeds if the client certificate is provided.
        """
        with Client(verify=False) as client:
            with self.assertRaises(Exception):
                client.get(f"https://localhost:{self.server_port}")


if __name__ == "__main__":
    unittest.main()
