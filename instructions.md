# HTTPX-RS Development Guidelines

## Core Principles
1. **API Parity** - Mirror httpx's API surface exactly
2. **Rust-Python Symbiosis** - Lever Rust's performance where it matters most
3. **Testing Rigor** - 100% test coverage with property-based testing
4. **Safety First** - Strict error handling and resource management

## Development Practices

### Rust Layer
```rust
// Error handling example
fn convert_error(e: reqwest::Error) -> PyErr {
    PyValueError::new_err(format!("Request failed: {}", e))
}

// Resource management
#[pyclass(unsendable)]  // For async safety
struct Response {
    inner: Pin<Box<dyn Stream<Item = Result<Bytes, reqwest::Error>> + Send>>,
}
```

- Use `thiserror` for Rust-side error variants
- Annotate all PyO3 signatures with `#[pyo3(text_signature)]`
- Prefer zero-copy data passing between Rust/Python

### Python Layer
```python
# Test case pattern
async def test_async_redirects():
    client = AsyncClient(follow_redirects=True)
    response = await client.get("http://example.com/redirect")
    assert response.status_code == 200
```

- Mirror httpx's exception hierarchy
- Use `unittest.mock` for Python-side mocks
- Validate all public API docstrings

## Testing Strategy

1. **Layered Tests**
   - Rust: Unit tests with `#[cfg(test)]`
   - Integration: `pytest` with `maturin develop`
   - Property-based: `hypothesis` for edge cases

2. Coverage Enforcement
```yaml
# .github/workflows/ci.yml
- name: Test Coverage
  run: |
    grcov . --binary-path target/debug/ -s . -t lcov
    genhtml -o coverage/ lcov.info
```

3. Test Patterns
```rust
#[cfg(test)]
mod tests {
    #[tokio::test]
    async fn test_async_get() {
        // Test async client with mock server
    }
}
```

## Performance Critical Paths
1. Connection pooling
2. Header parsing
3. Streaming responses
4. TLS handshakes

Use `criterion` for microbenchmarks:
```rust
c.bench_function("json_parsing", |b| {
    b.iter(|| serde_json::from_slice::<Value>(&big_json));
});
```

## Maintenance Checklist
- [ ] Weekly dependency updates (cargo update/pip audit)
- [ ] Biweekly API parity check vs httpx
- [ ] Monthly fuzzing session
- [ ] Quarterly performance review

## PR Requirements
✅ Matching httpx test cases  
✅ Rust/Python coverage reports  
✅ Benchmark comparison  
✅ Panic-free error paths  
✅ Resource leak check (Valgrind/miri)

## Setup Verification
```bash
python -m pytest --cov=httprs --cov-report=term-missing
cargo tarpaulin --ignore-tests --out Html
```

Pre-commit hooks enforce:
- Rust fmt/clippy
- Python black/flake8
- Test coverage guard
