## Benchmark

Benchmark between `httpr` and other python http clients:

- curl_cffi
- httpx
- httpx2 (the pydantic-maintained continuation of httpx)
- httpr
- pycurl
- python-tls-client
- requests

Server response is gzipped.

#### Run benchmark:
    
- run server: `uvicorn server:app`
- run benchmark: `python benchmark.py`
