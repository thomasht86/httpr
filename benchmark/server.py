import base64
import gzip
import json
import os
import random  # used to generate random floats

from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route

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


# Precompute JSON payloads.
json_precomputed = {}
for count in (1, 10, 100):
    data = [[random.random() for _ in range(1024)] for _ in range(count)]
    json_precomputed[count] = make_precomputed_json(data)


def precomputed_json_route(count, request):
    # Determine if the response should be gzipped
    use_gzip = request.query_params.get("gzip", "false").lower() in ("true", "1", "yes")
    # Return the precomputed response: index 1 is gzipped; index 0 isn't.
    return json_precomputed[count][1] if use_gzip else json_precomputed[count][0]


app = Starlette(
    routes=[
        Route("/5k", lambda r: gzip_response(random_5k)),
        Route("/50k", lambda r: gzip_response(random_50k)),
        Route("/200k", lambda r: gzip_response(random_200k)),
        # JSON endpoints using precomputed responses:
        Route("/json/1", lambda request: precomputed_json_route(1, request)),
        Route("/json/10", lambda request: precomputed_json_route(10, request)),
        Route("/json/100", lambda request: precomputed_json_route(100, request)),
    ],
)

# Run server: uvicorn server:app
