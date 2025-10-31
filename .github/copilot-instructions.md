# httpr - AI Coding Agent Instructions

## Project Overview

**httpr** is a high-performance HTTP client for Python built in Rust using PyO3 and reqwest. It's designed as a drop-in replacement for `httpx` and `requests` with significantly better performance through Rust's native speed.

### Architecture

- **Rust Core** (`src/`): PyO3-based HTTP client wrapping reqwest
  - `lib.rs`: Main `RClient` class with sync request handling via Tokio single-threaded runtime
  - `response.rs`: `Response` object with `CaseInsensitiveHeaderMap` for HTTP headers
  - `traits.rs`: Conversion traits between Python/Rust types (IndexMap ↔ HeaderMap)
  - `utils.rs`: CA certificate loading, encoding detection
- **Python Wrapper** (`httpr/`): Thin Python layer over Rust bindings
  - `__init__.py`: `Client` (sync) and `AsyncClient` classes with context manager support
  - `AsyncClient` uses `asyncio.run_in_executor()` to wrap sync Rust calls - NOT native async
  - `httpr.pyi`: Type stubs for IDE support
- **Build System**: Maturin (PyO3 build tool) compiles Rust → Python wheels

### Key Architectural Decisions

1. **Single Tokio Runtime**: Uses `LazyLock<Runtime>` with `new_current_thread()` - all async operations run on one thread
2. **Async is Sync**: `AsyncClient` runs sync Rust code in thread executor, NOT native async Rust
3. **Case-Insensitive Headers**: Custom `CaseInsensitiveHeaderMap` struct maintains original casing while allowing case-insensitive lookups (required for HTTP/2)
4. **Zero Python Dependencies**: All functionality in Rust; no runtime Python dependencies

## Development Workflows

### Building & Testing

```bash
# Install development dependencies (includes maturin)
uv sync --extra dev

# Build Rust extension in development mode (fast compilation)
uv run maturin develop

# Run tests (requires httpbin.org access)
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

The benchmark compares httpr against requests, httpx, curl_cffi, pycurl, tls_client, and aiohttp.

### Release Process

1. Tag with version: `git tag v0.1.x`
2. Push tag: `git push origin v0.1.x`
3. CI auto-builds wheels for Linux (x86_64, aarch64, armv7), macOS (Intel/ARM), Windows
4. Maturin publishes to PyPI

## Project-Specific Conventions

### Python-Rust Interface Patterns

- **All Python params converted to strings**: `Client.request()` converts param values to strings before passing to Rust
- **Method validation in Python**: HTTP method validation happens in Python wrapper, not Rust
- **Optional chaining**: Client stores default `auth`, `params`, `headers` - per-request values override via `.or()`

### Type System

- Rust uses `IndexMap<String, String, RandomState>` (foldhash) for dicts
- Python type hints via `TypedDict` (`RequestParams`, `ClientRequestParams`)
- Use `Unpack` for `**kwargs` typing (supports Python 3.9+ via typing_extensions)

### Error Handling

- Rust errors bubble up via `anyhow::Result` → PyO3 exceptions
- No fine-grained error types yet (all raise generic `Exception`)
- Tests use `@retry()` decorator to handle flaky httpbin.org responses

### Testing Patterns

```python
# Sync tests
def test_client_feature():
    client = httpr.Client(auth=("user", "pass"))
    response = client.get("https://httpbin.org/anything")
    assert response.status_code == 200

# Async tests
@pytest.mark.asyncio
async def test_asyncclient_feature():
    async with httpr.AsyncClient() as client:
        response = await client.get("https://httpbin.org/anything")
        assert response.status_code == 200
```

Tests depend on httpbin.org for validation - use `@retry()` wrapper for flaky network requests.

## Critical Implementation Details

### SSL/TLS Configuration

- CA certs loaded via `HTTPR_CA_BUNDLE` env var (set before client init)
- `ca_cert_file` param internally sets `HTTPR_CA_BUNDLE`
- mTLS via `client_pem` parameter (PEM format identity file)
- `verify=False` enables `danger_accept_invalid_certs()`

### Headers Behavior

- Headers are **lowercased** internally (HTTP/2 requirement)
- `client.headers` getter excludes `Cookie` header
- `client.cookies` getter/setter extracts from `Cookie` header
- Use `CaseInsensitiveHeaderMap` in Rust for lookups

### Request Body Handling

- Mutually exclusive: `content` (bytes), `data` (form), `json` (JSON), `files` (multipart)
- `data` and `json` use `pythonize::depythonize()` for Python → Rust serde_json::Value
- `files` dict maps field names to file paths (auto-reads and sends as multipart)

### Proxy Support

- Set via `proxy` param or `HTTPR_PROXY` env var
- Changing `client.proxy` rebuilds entire reqwest client (expensive operation)

## Common Tasks

### Adding New Request Parameters

1. Add to `RequestParams` TypedDict in `httpr.pyi`
2. Add parameter to `RClient.request()` signature in `src/lib.rs`
3. Handle parameter in request builder chain
4. Update docstrings in both Python and Rust

### Modifying Response Properties

1. Add Rust implementation in `src/response.rs`
2. Add `#[pymethods]` getter/method
3. Add type hint to `Response` class in `httpr.pyi`

### Performance Optimization

- Check `Cargo.toml` for reqwest feature flags (enable compression codecs, http2, etc.)
- Profile with `cargo flamegraph` on Rust side
- Benchmark against other clients using `benchmark/benchmark.py`

## What NOT to Do

- Don't add Python dependencies (defeats "zero dependencies" goal)
- Don't use native async Rust in request path (breaks single-threaded runtime model)
- Don't modify headers case-sensitivity behavior (HTTP/2 spec requirement)
- Don't remove reqwest compression features (users expect automatic gzip/brotli)
- Don't skip `maturin develop` after Rust changes (Python won't see updates)

## Resources

- [PyO3 User Guide](https://pyo3.rs/)
- [reqwest docs](https://docs.rs/reqwest/)
- [Maturin Guide](https://www.maturin.rs/)
- Benchmark results: `benchmark.jpg` in repo root
