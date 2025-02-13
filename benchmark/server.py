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


def json_response(data, use_gzip=False):
    body = json.dumps(data).encode("utf-8")
    if use_gzip:
        gzipped_body = gzip.compress(body)
        headers = {
            "Content-Encoding": "gzip",
            "Content-Length": str(len(gzipped_body)),
            "Content-Type": "application/json",
        }
        return Response(gzipped_body, headers=headers)
    else:
        headers = {"Content-Type": "application/json"}
        return Response(body, headers=headers)


def make_json_vectors(request, count):
    # Determine if the response should be gzipped
    use_gzip = request.query_params.get("gzip", "false").lower() in ("true", "1", "yes")
    # Generate a list of 'count' vectors of length 1024 filled with random floats.
    data = [[random.random() for _ in range(1024)] for _ in range(count)]
    return json_response(data, use_gzip)


app = Starlette(
    routes=[
        Route("/5k", lambda r: gzip_response(random_5k)),
        Route("/50k", lambda r: gzip_response(random_50k)),
        Route("/200k", lambda r: gzip_response(random_200k)),
        # JSON endpoints:
        Route("/json/1", lambda request: make_json_vectors(request, 1)),
        Route("/json/10", lambda request: make_json_vectors(request, 10)),
        Route("/json/100", lambda request: make_json_vectors(request, 100)),
    ],
)

# Run server: uvicorn server:app
