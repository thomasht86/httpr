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

The comparison runs every Monday in the `Client comparison` workflow
(`.github/workflows/compare.yml`) against the latest PyPI release of every
library, httpr included, and is published to
https://thomasht86.github.io/httpr/dev/bench/compare/ (chart, tables, CSVs, and a
dated copy under `history/`). Trigger it by hand from Actions → Client comparison
→ Run workflow; choose `httpr_source: main` to benchmark a wheel built from the
current commit instead of the release, and untick `publish` for a dry run. The
tables also land in the job summary and the logs/CSVs in the run artifact.

#### Render the chart locally:

    uv run --script benchmark/render_comparison.py --results <dir with the CSVs> --out <dir>
