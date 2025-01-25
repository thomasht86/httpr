# Reqwest-powered HTTP Client for Python

High-performance Python HTTP client with sync/async support, powered by Rust's reqwest library.

## Features

- **Sync & Async APIs** - Choose between blocking or non-blocking requests
- **Rust Core** - Native speed through pyo3 bindings
- **Simple Interface** - Straightforward `get()` method for both clients

## Installation

```bash
pip install .
```

**Requirements**: Python 3.7+, Rust toolchain, maturin

## Usage

```python
# Synchronous
from your_module import Client
print(Client().get("https://httpbin.org/get"))

# Asynchronous
from your_module import AsyncClient
import asyncio

async def main():
    client = AsyncClient()
    print(await client.get("https://httpbin.org/get"))

asyncio.run(main())
```

## Development

```bash
maturin develop --release
```

License: Apache-2.0
