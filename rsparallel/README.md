## gen key and cert

```bash
openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout key.pem \
  -out cert.pem \
  -days 365 \
  -subj "/CN=localhost" \
  -addext "subjectAltName = DNS:localhost, DNS:rsparallel"
```

## running the server

```bash
uv run hypercorn server:app --bind 0.0.0.0:8000 --keyfile=./ssl/key.pem --certfile=./ssl/cert.pem --log-level info --access-log - 
```

## test with curl

```bash
curl --http2-prior-knowledge -v --cacert ./ssl/cert.pem --resolve rsparallel:8000:127.0.0.1 "https://rsparallel:8000/test?"
```