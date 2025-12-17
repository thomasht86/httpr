"""Tests for transparent CBOR serialization/deserialization support."""
import pytest
import httpr
import cbor2


def test_cbor_serialization_transparent(base_url_ssl, ca_bundle):
    """Test transparent CBOR serialization when Accept header is set."""
    client = httpr.Client(ca_cert_file=ca_bundle)
    
    # Create test data
    test_data = {
        "name": "httpr",
        "version": "0.1.0",
        "numbers": [1, 2, 3, 4, 5],
        "nested": {
            "key1": "value1",
            "key2": 42,
        }
    }
    
    # Send with Accept: application/cbor header - should use CBOR automatically
    response = client.post(
        f"{base_url_ssl}/anything",
        json=test_data,
        headers={"Accept": "application/cbor"}
    )
    
    assert response.status_code == 200
    json_data = response.json()
    
    # httpbin echoes the request, check that Content-Type was set correctly
    assert json_data["headers"]["Content-Type"] == "application/cbor"
    
    # Verify the CBOR data was sent by checking the data field exists
    assert "data" in json_data


def test_json_serialization_default(base_url_ssl, ca_bundle):
    """Test that JSON is used by default when Accept header is not set."""
    client = httpr.Client(ca_cert_file=ca_bundle)
    
    test_data = {"test": "data"}
    
    # Send without Accept header - should use JSON (default)
    response = client.post(
        f"{base_url_ssl}/anything",
        json=test_data,
    )
    
    assert response.status_code == 200
    json_data = response.json()
    
    # Should use JSON by default
    assert json_data["headers"]["Content-Type"] == "application/json"
    assert json_data["json"] == test_data


def test_cbor_types():
    """Test various CBOR data types in serialization."""
    test_data = {
        "string": "test",
        "int": 42,
        "float": 3.14159,
        "bool_true": True,
        "bool_false": False,
        "null": None,
        "array": [1, 2, 3],
        "object": {"nested": "value"},
    }
    
    cbor_bytes = cbor2.dumps(test_data)
    decoded = cbor2.loads(cbor_bytes)
    
    assert decoded["string"] == "test"
    assert decoded["int"] == 42
    assert decoded["float"] == pytest.approx(3.14159)
    assert decoded["bool_true"] is True
    assert decoded["bool_false"] is False
    assert decoded["null"] is None
    assert decoded["array"] == [1, 2, 3]
    assert decoded["object"]["nested"] == "value"


@pytest.mark.asyncio
async def test_cbor_async_transparent(base_url_ssl, ca_bundle):
    """Test transparent CBOR with async client."""
    async with httpr.AsyncClient(ca_cert_file=ca_bundle) as client:
        test_data = {"async": True, "value": 999}
        
        # Use Accept header to trigger CBOR serialization
        response = await client.post(
            f"{base_url_ssl}/anything",
            json=test_data,
            headers={"Accept": "application/cbor"}
        )
        
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["headers"]["Content-Type"] == "application/cbor"
