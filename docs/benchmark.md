# Benchmarks

httpr's performance is tracked three ways. All of them run in GitHub Actions.

## Comparison with other clients

Every Monday, [`benchmark/benchmark.py`](https://github.com/thomasht86/httpr/blob/main/benchmark/benchmark.py)
runs httpr against the latest release of requests, httpx, httpx2, aiohttp,
curl_cffi, pycurl and tls_client: 400 requests per cell against a local uvicorn
server with gzip responses, in sync, async and multi-threaded modes. Wall-clock
seconds, lower is better.

[![HTTP client comparison](https://thomasht86.github.io/httpr/dev/bench/compare/comparison.png)](https://thomasht86.github.io/httpr/dev/bench/compare/)

The [full tables and raw CSVs](https://thomasht86.github.io/httpr/dev/bench/compare/)
are published with the chart. Absolute numbers depend on the GitHub runner, so
compare rows within a chart rather than charts across weeks.

## httpr over time

On every push to `main`, `tests/benchmark/test_performance.py` runs under
pytest-benchmark and the results are appended to the
[live trend chart](https://thomasht86.github.io/httpr/dev/bench/).
The runners are shared, so a single run can swing by 1.5x; look at the trend,
not at individual points.

## CPU cost per pull request

[CodSpeed](https://app.codspeed.io/thomasht86/httpr) measures the CPU
instructions of `tests/benchmark/codspeed/` on every pull request and reports
the difference against `main` on the PR. This is deterministic to about one
percent and is what catches regressions before they merge.

## Running locally

See [benchmark/README.md](https://github.com/thomasht86/httpr/blob/main/benchmark/README.md).
