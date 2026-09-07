import asyncio
import os
import threading

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


def test_default_max_concurrency():
    client = httpr.AsyncClient()
    assert client.max_concurrency == httpr.DEFAULT_MAX_CONCURRENCY
    assert client._executor._max_workers == httpr.DEFAULT_MAX_CONCURRENCY


def test_max_concurrency_sizes_the_pool():
    client = httpr.AsyncClient(max_concurrency=7)
    assert client._executor._max_workers == 7


@pytest.mark.asyncio
async def test_requests_run_on_the_clients_own_pool(base_url):
    """Requests must not land on asyncio's default executor, which is shared with
    asyncio.to_thread and sized min(32, cpu_count + 4)."""
    client = httpr.AsyncClient(max_concurrency=4)
    thread_name = await client._run_sync_asyncio(lambda: threading.current_thread().name)
    assert thread_name.startswith("httpr"), f"ran on {thread_name!r}, not on the client's own pool"
    # and a real request still works
    response = await client.get(f"{base_url}/anything")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_max_concurrency_none_uses_default_executor():
    client = httpr.AsyncClient(max_concurrency=None)
    assert client._executor is None
    thread_name = await client._run_sync_asyncio(lambda: threading.current_thread().name)
    assert thread_name.startswith("asyncio_")


@pytest.mark.asyncio
async def test_concurrency_is_not_capped_by_the_default_executor():
    """Regression guard for the bug this feature fixes.

    Dispatching on asyncio's default executor caps in-flight requests at
    ``min(32, cpu_count + 4)``, so `max_concurrency` above that was silently
    ignored. Asserts on observed peak concurrency rather than on wall-clock:
    against a localhost server there is no latency for concurrency to hide, so a
    throughput measurement would *not* catch a regression here.
    """
    default_executor_cap = min(32, (os.cpu_count() or 1) + 4)
    concurrency = default_executor_cap + 16

    in_flight = 0
    peak = 0
    lock = threading.Lock()
    all_admitted = threading.Barrier(concurrency, timeout=30)

    def occupy():
        nonlocal in_flight, peak
        with lock:
            in_flight += 1
            peak = max(peak, in_flight)
        # Block until every task has been admitted. If the pool were smaller than
        # `concurrency` this would time out rather than merely being slow.
        all_admitted.wait()
        with lock:
            in_flight -= 1

    client = httpr.AsyncClient(max_concurrency=concurrency)
    await asyncio.gather(*[client._run_sync_asyncio(occupy) for _ in range(concurrency)])

    assert peak == concurrency
    assert peak > default_executor_cap


@pytest.mark.asyncio
async def test_client_stays_reusable_across_contexts(base_url):
    """Reuse across several `async with` blocks must keep working -- downstream
    users (pyvespa) hold one client and scope it with repeated `async with`."""
    client = httpr.AsyncClient(max_concurrency=2)

    async with client:
        assert (await client.get(f"{base_url}/anything")).status_code == 200
    async with client:
        assert (await client.get(f"{base_url}/anything")).status_code == 200

    await client.aclose()
    assert (await client.get(f"{base_url}/anything")).status_code == 200
