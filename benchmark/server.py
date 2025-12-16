import base64
import gzip
import json
import os
import random  # used to generate random floats

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route

# Try to import cbor2, if not available skip CBOR endpoints
try:
    import cbor2
    CBOR_AVAILABLE = True
except ImportError:
    CBOR_AVAILABLE = False

random_5k = base64.b64encode(os.urandom(5 * 1024)).decode("utf-8")
random_5k = gzip.compress(random_5k.encode("utf-8"))

random_50k = base64.b64encode(os.urandom(50 * 1024)).decode("utf-8")
random_50k = gzip.compress(random_50k.encode("utf-8"))

random_200k = base64.b64encode(os.urandom(200 * 1024)).decode("utf-8")
random_200k = gzip.compress(random_200k.encode("utf-8"))


def gzip_response(gzipped_content):
    headers = {
        "Content-Encoding": "gzip",
        "Content-Length": str(len(gzipped_content)),
    }
    return Response(gzipped_content, headers=headers)


def json_response_body(data):
    # Return the JSON body encoded as bytes without compression.
    return json.dumps(data).encode("utf-8")


def make_precomputed_json(data):
    # Precompute both non-gzipped and gzipped responses.
    body = json_response_body(data)
    resp_plain = Response(body, headers={"Content-Type": "application/json"})
    gzipped_body = gzip.compress(body)
    headers = {
        "Content-Encoding": "gzip",
        "Content-Length": str(len(gzipped_body)),
        "Content-Type": "application/json",
    }
    resp_gzip = Response(gzipped_body, headers=headers)
    return resp_plain, resp_gzip


def make_precomputed_cbor(data):
    """Precompute CBOR responses (with and without gzip)."""
    if not CBOR_AVAILABLE:
        return None, None
    
    body = cbor2.dumps(data)
    resp_plain = Response(body, headers={"Content-Type": "application/cbor"})
    gzipped_body = gzip.compress(body)
    headers = {
        "Content-Encoding": "gzip",
        "Content-Length": str(len(gzipped_body)),
        "Content-Type": "application/cbor",
    }
    resp_gzip = Response(gzipped_body, headers=headers)
    return resp_plain, resp_gzip


# Precompute JSON payloads.
json_precomputed = {}
cbor_precomputed = {}
for count in (1, 10, 100):
    data = [[random.random() for _ in range(1024)] for _ in range(count)]
    json_precomputed[count] = make_precomputed_json(data)
    if CBOR_AVAILABLE:
        cbor_precomputed[count] = make_precomputed_cbor(data)


def precomputed_json_route(count, request):
    # Determine if the response should be gzipped
    use_gzip = request.query_params.get("gzip", "false").lower() in ("true", "1", "yes")
    # Return the precomputed response: index 1 is gzipped; index 0 isn't.
    return json_precomputed[count][1] if use_gzip else json_precomputed[count][0]


def precomputed_cbor_route(count, request):
    """Return precomputed CBOR response."""
    if not CBOR_AVAILABLE:
        return Response("CBOR not available", status_code=501)
    
    use_gzip = request.query_params.get("gzip", "false").lower() in ("true", "1", "yes")
    return cbor_precomputed[count][1] if use_gzip else cbor_precomputed[count][0]


routes = [
    Route("/5k", lambda r: gzip_response(random_5k)),
    Route("/50k", lambda r: gzip_response(random_50k)),
    Route("/200k", lambda r: gzip_response(random_200k)),
    # JSON endpoints using precomputed responses:
    Route("/json/1", lambda request: precomputed_json_route(1, request)),
    Route("/json/10", lambda request: precomputed_json_route(10, request)),
    Route("/json/100", lambda request: precomputed_json_route(100, request)),
]

# Add CBOR routes if available
if CBOR_AVAILABLE:
    routes.extend([
        Route("/cbor/1", lambda request: precomputed_cbor_route(1, request)),
        Route("/cbor/10", lambda request: precomputed_cbor_route(10, request)),
        Route("/cbor/100", lambda request: precomputed_cbor_route(100, request)),
    ])

app = Starlette(routes=routes)

# Run server: uvicorn server:app
