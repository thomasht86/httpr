import asyncio
import pytest

import certifi
import httpr


def async_retry(max_retries=3, delay=1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay)
                        continue
                    else:
                        raise e

        return wrapper

    return decorator


@pytest.mark.asyncio
@async_retry()
async def test_asyncclient_init():
    auth = ("user", "password")
    headers = {"X-Test": "test"}
    cookies = {"ccc": "ddd", "cccc": "dddd"}
    params = {"x": "aaa", "y": "bbb"}
    client = httpr.AsyncClient(
        auth=auth,
        params=params,
        headers=headers,
        cookies=cookies,
        ca_cert_file=certifi.where(),
    )
    response = await client.get("https://httpbin.org/anything")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["headers"]["X-Test"] == "test"
    assert json_data["headers"]["Cookie"] == "ccc=ddd; cccc=dddd"
    assert json_data["headers"]["Authorization"] == "Basic dXNlcjpwYXNzd29yZA=="
    assert json_data["args"] == {"x": "aaa", "y": "bbb"}