#!/usr/bin/env python3
"""Demo script showing CBOR functionality in httpr."""

import httpr
import cbor2

# Example 1: Sending CBOR data
print("="*60)
print("Example 1: Sending CBOR Data")
print("="*60)

client = httpr.Client()
test_data = {
    "name": "httpr",
    "version": "0.1.0",
    "features": ["fast", "async", "cbor"],
    "metadata": {
        "author": "thomasht86",
        "rust": True
    }
}

print(f"\nSending CBOR data to httpbin.org:")
print(f"Data: {test_data}")

try:
    response = client.post(
        "https://httpbin.org/anything",
        cbor=test_data,
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Request succeeded!")
        print(f"  Content-Type sent: {result['headers'].get('Content-Type', 'N/A')}")
        print(f"  Server received: {len(result.get('data', ''))} bytes of CBOR data")
    else:
        print(f"\n✗ Request failed with status {response.status_code}")
except Exception as e:
    print(f"\n✗ Error: {e}")

# Example 2: Round-trip CBOR encoding/decoding
print("\n" + "="*60)
print("Example 2: CBOR Encoding/Decoding Round-Trip")
print("="*60)

data = {
    "integers": [1, 2, 3, 4, 5],
    "floats": [1.1, 2.2, 3.3],
    "strings": ["hello", "world"],
    "nested": {"key": "value"}
}

print(f"\nOriginal data: {data}")

# Encode to CBOR
cbor_bytes = cbor2.dumps(data)
print(f"CBOR encoded size: {len(cbor_bytes)} bytes")

# Decode from CBOR
decoded = cbor2.loads(cbor_bytes)
print(f"Decoded data: {decoded}")
print(f"✓ Round-trip successful: {data == decoded}")

# Example 3: Compare JSON vs CBOR size
print("\n" + "="*60)
print("Example 3: JSON vs CBOR Size Comparison")
print("="*60)

import json

# Example with large integers (where CBOR excels)
large_data_integers = [[i * 1000 + j for j in range(100)] for i in range(10)]

json_bytes_int = json.dumps(large_data_integers).encode('utf-8')
cbor_bytes_int = cbor2.dumps(large_data_integers)

print(f"\nData: 10 arrays of 100 large integers each")
print(f"JSON size:  {len(json_bytes_int):,} bytes")
print(f"CBOR size:  {len(cbor_bytes_int):,} bytes")
if len(cbor_bytes_int) < len(json_bytes_int):
    print(f"CBOR is {len(json_bytes_int) / len(cbor_bytes_int):.2f}x smaller!")
else:
    print(f"JSON is {len(cbor_bytes_int) / len(json_bytes_int):.2f}x smaller for this data")

# Example with strings (where CBOR is comparable)
string_data = {f"key_{i}": f"value_{i}" * 10 for i in range(100)}

json_bytes_str = json.dumps(string_data).encode('utf-8')
cbor_bytes_str = cbor2.dumps(string_data)

print(f"\nData: 100 string key-value pairs")
print(f"JSON size:  {len(json_bytes_str):,} bytes")
print(f"CBOR size:  {len(cbor_bytes_str):,} bytes")
if len(cbor_bytes_str) < len(json_bytes_str):
    print(f"CBOR is {len(json_bytes_str) / len(cbor_bytes_str):.2f}x smaller!")
else:
    print(f"Sizes are comparable (CBOR excels more with binary data)")

print("\n💡 CBOR advantages:")
print("  - Binary format = faster serialization/deserialization")
print("  - Better for integers and binary data")
print("  - Preserves exact numeric types")
print("  - Designed for constrained environments")


print("\n" + "="*60)
print("CBOR Demo Complete!")
print("="*60)
