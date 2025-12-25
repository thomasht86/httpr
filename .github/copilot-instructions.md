# httpr - AI Coding Agent Instructions

## Overview

**httpr** is a zero-dependency Python HTTP client with a Rust core (PyO3 + reqwest). Drop-in replacement for `httpx`/`requests` with better performance.

## Architecture

```
src/           → Rust core (lib.rs: RClient, response.rs: Response/StreamingResponse, exceptions.rs)
httpr/         → Python wrapper (__init__.py: Client/AsyncClient, httpr.pyi: type stubs)
tests/unit/    → Unit tests using pytest-httpbin fixtures
tests/e2e/     → E2E tests using httpbun Docker container with SSL
scripts/       → Development scripts (generate_certs.py)
```

**Key decisions:**
- Single-threaded Tokio runtime (`LazyLock<Runtime>` with `new_current_thread()`)
- `AsyncClient` uses `run_in_executor()` wrapping sync Rust—NOT native async
- Headers lowercased internally (HTTP/2 spec); `CaseInsensitiveHeaderMap` for lookups
- Streaming via `Arc<Mutex<Option<reqwest::Response>>>` with `iter_bytes()`/`iter_text()`/`iter_lines()`

## Development Commands

```bash
uv sync --extra dev              # Install dependencies
uv run maturin develop           # Build Rust extension (REQUIRED after any .rs changes)
task test:unit                   # Run unit tests (uses pytest-httpbin)
task e2e                         # Run e2e tests (httpbun Docker with SSL)
task lint                        # Run ruff + mypy
```

### Taskfile Commands

```bash
task --list        # List all available tasks
task test:unit     # Run unit tests only
task e2e           # Full e2e workflow: certs → start httpbun → test → stop
task e2e:local     # Start httpbun and run tests (keep container running)
task dev           # Build Rust extension
task check         # Run all checks (lint + test) - use before committing
task lint:all      # Run all linters (Python + Rust)
task fmt:all       # Format all code (Python + Rust)
```

### Pre-commit Setup

```bash
uv pip install pre-commit && pre-commit install && pre-commit install --hook-type commit-msg
```

Hooks: ruff (lint/format), mypy, cargo fmt/clippy, commitizen/commitlint

## Adding Features

**New request parameter:** Update `httpr.pyi` (TypedDict) → `src/lib.rs` (RClient.request signature) → handle in builder chain

**New response property:** Implement in `src/response.rs` with `#[pymethods]` getter → add to `httpr.pyi`

**New exception:** Add `create_exception!` in `src/exceptions.rs` → map in `map_reqwest_error()`

## Patterns

```python
# Unit tests use pytest-httpbin fixtures (base_url, base_url_ssl, ca_bundle)
def test_feature(base_url_ssl, ca_bundle):
    client = httpr.Client(ca_cert_file=ca_bundle)
    response = client.get(f"{base_url_ssl}/anything")
    assert response.status_code == 200

# E2E tests use httpbun fixtures (e2e_base_url, e2e_ca_cert)
@pytest.mark.e2e
def test_e2e_feature(e2e_base_url, e2e_ca_cert):
    client = httpr.Client(ca_cert_file=e2e_ca_cert)
    response = client.get(f"{e2e_base_url}/any")
    assert response.status_code == 200

# Streaming with context manager
with client.stream("GET", url) as response:
    for chunk in response.iter_bytes():
        process(chunk)
```

## Critical Details

- **Body types mutually exclusive:** `content` (bytes) | `data` (form) | `json` | `files` (multipart)
- **SSL:** `ca_cert_file` sets `HTTPR_CA_BUNDLE` env var; `verify=False` for insecure
- **Proxy:** `proxy` param or `HTTPR_PROXY` env var; changing rebuilds entire client
- **Python types:** `IndexMap<String, String, RandomState>` in Rust ↔ `dict[str, str]` in Python

## Don'ts

- Don't add Python runtime dependencies (zero-dep goal)
- Don't use native async Rust (breaks single-threaded runtime)
- Don't skip `maturin develop` after Rust changes
- Don't modify header case behavior (HTTP/2 requirement)
