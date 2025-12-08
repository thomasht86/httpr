# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**httpr** is a high-performance HTTP client for Python built in Rust using PyO3 and reqwest. It's designed as a drop-in replacement for `httpx` and `requests` with significantly better performance.

## Build & Development Commands

```bash
# Install development dependencies
uv sync --extra dev

# Build Rust extension (required after any Rust code changes)
uv run maturin develop

# Run tests (depends on httpbin.org)
uv run pytest tests/

# Type checking
uv run mypy httpr/

# Linting
uv run ruff check httpr/
```

### Benchmarking

```bash
cd benchmark/
uv run uvicorn server:app  # Terminal 1: Start test server
uv run python benchmark.py  # Terminal 2: Run benchmarks
```

## Architecture

### Rust Core (`src/`)
- `lib.rs`: Main `RClient` class with sync request handling via single-threaded Tokio runtime (`LazyLock<Runtime>` with `new_current_thread()`)
- `response.rs`: `Response` object with `CaseInsensitiveHeaderMap` for HTTP/2 compliant header handling
- `traits.rs`: Conversion traits between Python/Rust types (IndexMap ↔ HeaderMap)
- `utils.rs`: CA certificate loading, encoding detection

### Python Wrapper (`httpr/`)
- `__init__.py`: `Client` (sync) and `AsyncClient` classes with context manager support
- `AsyncClient` uses `asyncio.run_in_executor()` to wrap sync Rust calls - NOT native async
- `httpr.pyi`: Type stubs for IDE support

### Key Design Decisions
1. **Single Tokio Runtime**: All async Rust operations run on one thread
2. **Async is Sync**: `AsyncClient` runs sync Rust code in thread executor
3. **Zero Python Dependencies**: All functionality in Rust
4. **Case-Insensitive Headers**: Custom struct maintains original casing while allowing case-insensitive lookups (HTTP/2 requirement)

## Critical Implementation Details

### Python-Rust Interface
- All Python params converted to strings before passing to Rust
- HTTP method validation happens in Python wrapper
- Rust uses `IndexMap<String, String, RandomState>` (foldhash) for dicts
- Use `Unpack` for `**kwargs` typing (via typing_extensions for Python ≤3.11)

### SSL/TLS
- CA certs loaded via `HTTPR_CA_BUNDLE` env var
- `ca_cert_file` param sets `HTTPR_CA_BUNDLE` internally
- mTLS via `client_pem` parameter (PEM format)
- `verify=False` enables `danger_accept_invalid_certs()`

### Headers Behavior
- Headers are lowercased internally (HTTP/2 spec)
- `client.headers` getter excludes `Cookie` header
- `client.cookies` getter/setter extracts from `Cookie` header

### Request Body
- Mutually exclusive: `content` (bytes), `data` (form), `json` (JSON), `files` (multipart)
- `data` and `json` use `pythonize::depythonize()` for Python → Rust conversion
- `files` dict maps field names to file paths

### Proxy
- Set via `proxy` param or `HTTPR_PROXY` env var
- Changing `client.proxy` rebuilds entire reqwest client (expensive)

## What NOT to Do

- Don't add Python dependencies (defeats "zero dependencies" goal)
- Don't use native async Rust in request path (breaks single-threaded runtime model)
- Don't modify headers case-sensitivity behavior (HTTP/2 spec requirement)
- Don't skip `maturin develop` after Rust changes
