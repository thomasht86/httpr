"""CBOR vs JSON benchmark for httpr.

This benchmark compares JSON and CBOR serialization/deserialization
performance for large vector data using httpr only.
"""

import asyncio
import time

import httpr


async def benchmark_cbor_vs_json():
    """Compare CBOR vs JSON performance for httpr."""
    print("\n" + "=" * 60)
    print("CBOR vs JSON Benchmark (httpr only)")
    print("=" * 60)

    url = "http://127.0.0.1:8000"
    requests_number = 100

    results = []

    # Test both JSON and CBOR endpoints with different payload sizes
    for endpoint_type in ["json", "cbor"]:
        for data_count in [1, 10, 100]:
            for gzip_param in ["false", "true"]:
                endpoint_url = f"{url}/{endpoint_type}/{data_count}?gzip={gzip_param}"
                print(f"\n{endpoint_type.upper()} - {data_count} arrays, gzip={gzip_param}, {requests_number} requests")

                async with httpr.AsyncClient() as client:
                    start = time.perf_counter()
                    cpu_start = time.process_time()

                    tasks = []
                    for _ in range(requests_number):
                        task = client.get(endpoint_url)
                        tasks.append(task)

                    responses = await asyncio.gather(*tasks)

                    # Decode responses
                    for response in responses:
                        if endpoint_type == "json":
                            _ = response.json()
                        else:  # cbor
                            _ = response.cbor()

                    dur = round(time.perf_counter() - start, 2)
                    cpu_dur = round(time.process_time() - cpu_start, 2)

                    results.append(
                        {
                            "format": endpoint_type.upper(),
                            "count": data_count,
                            "gzip": gzip_param,
                            "time": dur,
                            "cpu_time": cpu_dur,
                        }
                    )

                    print(f"    Time: {dur}s, CPU time: {cpu_dur}s")

    # Print summary comparison
    print("\n" + "=" * 60)
    print("Summary: CBOR vs JSON")
    print("=" * 60)

    # Group by count and gzip for comparison
    for data_count in [1, 10, 100]:
        for gzip_param in ["false", "true"]:
            json_result = next(
                r for r in results if r["format"] == "JSON" and r["count"] == data_count and r["gzip"] == gzip_param
            )
            cbor_result = next(
                r for r in results if r["format"] == "CBOR" and r["count"] == data_count and r["gzip"] == gzip_param
            )

            speedup = json_result["time"] / cbor_result["time"] if cbor_result["time"] > 0 else 0

            print(f"\n{data_count} arrays, gzip={gzip_param}:")
            print(f"  JSON: {json_result['time']}s (CPU: {json_result['cpu_time']}s)")
            print(f"  CBOR: {cbor_result['time']}s (CPU: {cbor_result['cpu_time']}s)")
            if speedup > 1:
                print(f"  → CBOR is {speedup:.2f}x faster")
            else:
                print(f"  → JSON is {1 / speedup:.2f}x faster")


if __name__ == "__main__":
    print("Starting CBOR vs JSON benchmark...")
    print("Make sure the benchmark server is running:")
    print("  cd benchmark && uvicorn server:app")
    print("\nWaiting 2 seconds for you to start the server...")
    time.sleep(2)

    asyncio.run(benchmark_cbor_vs_json())
