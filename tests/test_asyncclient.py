import pytest
import httpr


@pytest.mark.asyncio
async def test_asyncclient_init(base_url_ssl, ca_bundle):
    auth = ("user", "password")
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    client = httpr.AsyncClient(
        auth=auth,
        params=params,
        headers=headers,
        cookies=cookies,
        ca_cert_file=ca_bundle,
    )
    response = await client.get(f"{base_url_ssl}/anything")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Basic dXNlcjpwYXNzd29yZA=="
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}
