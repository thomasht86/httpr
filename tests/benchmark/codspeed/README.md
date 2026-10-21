# CodSpeed benchmark suite

These benchmarks are measured with [CodSpeed](https://codspeed.io) using the
[walltime instrument](https://codspeed.io/docs/instruments/walltime), on every
pull request and every push to `main` (`.github/workflows/codspeed.yml`).
Walltime measures elapsed time including system calls and network I/O, which
is most of what an HTTP client does; CPU simulation excludes syscalls and so
reported only a fraction of each request's cost.

They are kept separate from `tests/benchmark/test_performance.py`, which stays on
the wall-clock `github-action-benchmark` pipeline, because the two answer
different questions:

| Suite                                 | Instrument        | Question                                            |
| ------------------------------------- | ----------------- | --------------------------------------------------- |
| `tests/benchmark/codspeed/`           | CodSpeed walltime | Did this PR make an operation slower than on `main`? |
| `tests/benchmark/test_performance.py` | wall clock        | How does request latency trend over time?           |

## Layout

- `bench_server.py` — a stdlib HTTP server serving byte-for-byte deterministic
  payloads. It is started as a **subprocess**, so the server's Python code does
  not share the benchmark process's interpreter and GIL.
- `conftest.py` — the `payload_server` fixture plus response fixtures that fetch
  a payload once, outside the measured region.
- `test_decoding.py` — pure CPU: JSON/CBOR decoding, text decoding across
  charsets, HTML to text/markdown conversion, header-map access.
- `test_transport.py` — the request path: client construction, GET/POST variants,
  transfer decoding, multipart uploads, streaming, async dispatch.

## Running locally

```bash
task test:codspeed          # walltime via the CodSpeed CLI
task test:codspeed:wall     # same benchmarks, wall-clock, no CodSpeed CLI needed
```

## Reading the results

The job runs on a shared GitHub-hosted runner, so walltime results carry that
machine's noise; treat small differences as noise. CodSpeed recommends its
bare-metal [macro runners](https://codspeed.io/docs/features/macro-runners) for
stable walltime numbers, but they are only available to repositories owned by a
GitHub organization. Switching to one is a change of `runs-on` in the workflow.

Do not run the suite with `pytest-xdist` or other parallel runners: concurrent
benchmark processes add noise to walltime measurements.
