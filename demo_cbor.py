#!/usr/bin/env python3
"""Demo script showing transparent CBOR functionality in httpr."""

import httpr
import cbor2
import json

print("="*60)
print("CBOR Transparent Serialization/Deserialization Demo")
print("="*60)

# Example 1: Transparent CBOR Sending
print("\nExample 1: Transparent CBOR Serialization")
print("-" * 60)

test_data = {
    "name": "httpr",
    "version": "0.1.0",
    "features": ["fast", "async", "cbor"],
}

print("Sending data with Accept: application/cbor header")
print(f"Data: {test_data}")
print("\n→ Just set Accept header - CBOR is used automatically!")
print("→ Use json parameter as normal - no cbor parameter needed")

# Example 2: Default JSON behavior
print("\n\nExample 2: Default JSON Behavior")
print("-" * 60)
print("Without Accept header, JSON is used (default):")
print("→ client.post(url, json=data)  # Uses JSON")
print("→ client.post(url, json=data, headers={'Accept': 'application/cbor'})  # Uses CBOR!")

# Example 3: Transparent deserialization
print("\n\nExample 3: Transparent Deserialization")
print("-" * 60)
print("response.json() automatically detects Content-Type:")
print("→ If Content-Type is application/json → deserializes as JSON")
print("→ If Content-Type is application/cbor → deserializes as CBOR")
print("→ You don't need to know which format the server uses!")

# Example 4: Size comparison
print("\n\nExample 4: JSON vs CBOR Size Comparison")
print("-" * 60)

large_data = [[i * 1000 + j for j in range(100)] for i in range(10)]
json_bytes = json.dumps(large_data).encode('utf-8')
cbor_bytes = cbor2.dumps(large_data)

print(f"Data: 10 arrays of 100 large integers each")
print(f"JSON size:  {len(json_bytes):,} bytes")
print(f"CBOR size:  {len(cbor_bytes):,} bytes")
if len(cbor_bytes) < len(json_bytes):
    print(f"→ CBOR is {len(json_bytes) / len(cbor_bytes):.2f}x smaller!")

print("\n\n" + "="*60)
print("Key Takeaways")
print("="*60)
print("✓ Set Accept: application/cbor to use CBOR automatically")
print("✓ Use json parameter - httpr handles encoding transparently")
print("✓ response.json() automatically detects and decodes CBOR/JSON")
print("✓ No API changes needed - completely transparent!")
print("="*60)
