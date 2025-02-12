#!/bin/bash

# Exit on any error
set -e

# Set paths
CERT_DIR="./certs"
mkdir -p "$CERT_DIR"

# Files
CA_KEY="$CERT_DIR/ca.key"
CA_CERT="$CERT_DIR/ca.pem"
SERVER_KEY="$CERT_DIR/server.key"
SERVER_CERT="$CERT_DIR/server.pem"
SERVER_CSR="$CERT_DIR/server.csr"
CLIENT_KEY="$CERT_DIR/client.key"
CLIENT_CERT="$CERT_DIR/client.pem"
CLIENT_CSR="$CERT_DIR/client.csr"

echo "Generating CA (Certificate Authority)..."
openssl req -x509 -newkey rsa:4096 -days 365 -nodes -keyout "$CA_KEY" -out "$CA_CERT" -subj "/CN=MyTestCA"

echo "Generating Server Certificate..."
openssl req -newkey rsa:4096 -nodes -keyout "$SERVER_KEY" -out "$SERVER_CSR" -subj "/CN=localhost"
openssl x509 -req -in "$SERVER_CSR" -CA "$CA_CERT" -CAkey "$CA_KEY" -CAcreateserial -out "$SERVER_CERT" -days 365

echo "Generating Client Certificate..."
openssl req -newkey rsa:4096 -nodes -keyout "$CLIENT_KEY" -out "$CLIENT_CSR" -subj "/CN=client"
openssl x509 -req -in "$CLIENT_CSR" -CA "$CA_CERT" -CAkey "$CA_KEY" -CAcreateserial -out "$CLIENT_CERT" -days 365

echo "Certificates successfully created in $CERT_DIR"

# Clean up CSR and ca.srl files
rm -f "$SERVER_CSR" "$CLIENT_CSR" "$CERT_DIR/ca.srl"

# Create Starlette app
cat > app.py <<EOF
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.requests import Request

async def homepage(request: Request):
    return PlainTextResponse("Hello, world!")

app = Starlette(routes=[Route("/", homepage)])
EOF

echo "Starting Gunicorn with mutual TLS..."

# Run the server with mutual TLS in the background - save PID

gunicorn --keyfile "$SERVER_KEY" \
         --certfile "$SERVER_CERT" \
         --ca-certs "$CA_CERT" \
         app:app -k uvicorn.workers.UvicornWorker & 

# Wait for the server to start
sleep 5
# Run curl to test the server
curl --cacert ./certs/server.pem --key ./certs/client.pem https://localhost:8000/

# Kill the server
kill %1