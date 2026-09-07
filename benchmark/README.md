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

#### Run in CI:

The comparison is not run on every push. Trigger the `Benchmark` workflow manually
(Actions → Benchmark → Run workflow) with `compare` ticked; the tables land in the
job summary and the logs/CSVs are uploaded as the `client-comparison-<sha>` artifact.
