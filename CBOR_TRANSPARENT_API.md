# CBOR Transparent API

## Overview
CBOR serialization/deserialization is now completely transparent based on HTTP headers. Users don't need a separate `cbor` parameter.

## How It Works

### Sending Data (Serialization)
Set the `Accept: application/cbor` header and use the `json` parameter as normal:

```python
import httpr

# CBOR is used automatically when Accept header is set
response = httpr.post(
    "https://api.example.com/data",
    json={"values": [1, 2, 3, 4, 5]},  # Use json parameter
    headers={"Accept": "application/cbor"}  # Triggers CBOR
)
```

**Without the Accept header, JSON is used by default:**

```python
# Uses JSON (default behavior)
response = httpr.post(url, json=data)
```

### Receiving Data (Deserialization)
The `response.json()` method automatically detects the Content-Type:

```python
import httpr

response = httpr.get("https://api.example.com/data")

# Automatically uses CBOR if Content-Type is application/cbor
# Automatically uses JSON if Content-Type is application/json
data = response.json()  # Works transparently!
```

You can still explicitly use `response.cbor()` if needed, but it's not required.

## Benefits

1. **No API changes needed** - Just set headers
2. **Transparent** - Users don't need to know what format is used
3. **Backward compatible** - JSON is still the default
4. **Simple** - One method (`json()`) handles both formats

## Migration from Old API

**Before (explicit cbor parameter - no longer supported):**
```python
response = client.post(url, cbor=data)
data = response.cbor()
```

**After (transparent with headers):**
```python
response = client.post(url, json=data, headers={"Accept": "application/cbor"})
data = response.json()  # Auto-detects CBOR from Content-Type
```

## Implementation Details

### Request Side
1. Check if `Accept` header contains `application/cbor`
2. If yes: serialize `json` parameter data as CBOR and set `Content-Type: application/cbor`
3. If no: serialize as JSON (default behavior)

### Response Side
1. Check response `Content-Type` header
2. If `application/cbor`: deserialize using CBOR decoder
3. Otherwise: deserialize using JSON decoder (default)

## Testing
All tests updated to use transparent API:
- `test_cbor_serialization_transparent`: Tests CBOR with Accept header
- `test_json_serialization_default`: Tests default JSON behavior
- `test_cbor_async_transparent`: Tests async support

```bash
$ uv run pytest tests/test_cbor.py -v
4 passed in 0.54s
```
