# CodSpeed benchmark suite

These benchmarks are measured with [CodSpeed](https://codspeed.io) using the CPU
simulation instrument, on every pull request and every push to `main`
(`.github/workflows/codspeed.yml`).

They are kept separate from `tests/benchmark/test_performance.py`, which stays on
the wall-clock `github-action-benchmark` pipeline, because the two answer
different questions:

| Suite                            | Instrument            | Question                                    |
| -------------------------------- | --------------------- | ------------------------------------------- |
| `tests/benchmark/codspeed/`      | CodSpeed CPU simulation | How much CPU work does httpr itself do?     |
| `tests/benchmark/test_performance.py` | wall clock       | How long does a request take end to end?    |

## Layout

- `bench_server.py` — a stdlib HTTP server serving byte-for-byte deterministic
  payloads. It is started as a **subprocess**, so under CPU simulation only the
  httpr side of the exchange is instrumented and the server's own cost stays out
  of the measurements.
- `conftest.py` — the `payload_server` fixture plus response fixtures that fetch
  a payload once, outside the measured region.
- `test_decoding.py` — pure CPU: JSON/CBOR decoding, text decoding across
  charsets, HTML to text/markdown conversion, header-map access.
- `test_transport.py` — the request path: client construction, GET/POST variants,
  transfer decoding, multipart uploads, streaming, async dispatch.

## Running locally

```bash
task test:codspeed          # CPU simulation via the CodSpeed CLI
task test:codspeed:wall     # same benchmarks, wall-clock, no CodSpeed CLI needed
```

## Reading the results

The transport benchmarks are reported with a "dominated by syscalls" note. That
is expected for an HTTP client: the socket syscalls are excluded from the
reported value, so the number tracks the CPU httpr spends per request (request
building, header handling, transfer decoding, response materialisation) and
understates the total wall-clock cost. The `test_performance.py` suite is what
covers the wall-clock side.
