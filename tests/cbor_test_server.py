"""Simple test server that handles CBOR requests and responses."""
import cbor2
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route


def cbor_echo(request):
    """Echo back CBOR data."""
    # Return some CBOR-encoded data
    data = {
        "message": "CBOR response from server",
        "count": 42,
        "items": [1, 2, 3, 4, 5],
    }
    cbor_bytes = cbor2.dumps(data)
    
    return Response(
        cbor_bytes,
        media_type="application/cbor",
        headers={"Content-Type": "application/cbor"},
    )


def cbor_large(request):
    """Return large CBOR data for benchmarking."""
    # Create large vector data similar to what the benchmark will use
    data = [[i + j * 0.1 for j in range(1024)] for i in range(10)]
    cbor_bytes = cbor2.dumps(data)
    
    return Response(
        cbor_bytes,
        media_type="application/cbor",
        headers={"Content-Type": "application/cbor"},
    )


app = Starlette(
    routes=[
        Route("/cbor/echo", cbor_echo),
        Route("/cbor/large", cbor_large),
    ],
)
