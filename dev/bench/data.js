window.BENCHMARK_DATA = {
  "lastUpdate": 1768468105764,
  "repoUrl": "https://github.com/thomasht86/httpr",
  "entries": {
    "httpr Performance": [
      {
        "commit": {
          "author": {
            "name": "Thomas Hjelde Thoresen",
            "username": "thomasht86",
            "email": "thomas@vespa.ai"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "3ad95c1a3810a18878afbaa68237dcd922d015e0",
          "message": "Merge pull request #49 from thomasht86/thomasht86/fix-benchmark-workflow-ordering\n\nfix: run benchmark workflow after mkdocs to preserve data",
          "timestamp": "2026-01-15T09:02:39Z",
          "url": "https://github.com/thomasht86/httpr/commit/3ad95c1a3810a18878afbaa68237dcd922d015e0"
        },
        "date": 1768468105210,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1519.6610170268145,
            "unit": "iter/sec",
            "range": "stddev: 0.00009073462493185641",
            "extra": "mean: 658.0414900399824 usec\nrounds: 502"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1713.062843791684,
            "unit": "iter/sec",
            "range": "stddev: 0.000055507486849183556",
            "extra": "mean: 583.7497460318533 usec\nrounds: 1638"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1883.5696558120367,
            "unit": "iter/sec",
            "range": "stddev: 0.0000730494779910114",
            "extra": "mean: 530.9068326272671 usec\nrounds: 1888"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1517.8079228947809,
            "unit": "iter/sec",
            "range": "stddev: 0.00007260886807542141",
            "extra": "mean: 658.8448939525815 usec\nrounds: 1141"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 760.8218023197414,
            "unit": "iter/sec",
            "range": "stddev: 0.00006387144180455495",
            "extra": "mean: 1.3143682225601392 msec\nrounds: 328"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 908.5132634704269,
            "unit": "iter/sec",
            "range": "stddev: 0.000053438599990687476",
            "extra": "mean: 1.1006993956038718 msec\nrounds: 455"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 202.61337597582565,
            "unit": "iter/sec",
            "range": "stddev: 0.00005603802813147458",
            "extra": "mean: 4.935508305825341 msec\nrounds: 206"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 22.74675152883322,
            "unit": "iter/sec",
            "range": "stddev: 0.0021591681673145575",
            "extra": "mean: 43.96232133333081 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1282.395615909879,
            "unit": "iter/sec",
            "range": "stddev: 0.00007264936406500377",
            "extra": "mean: 779.7905635309622 usec\nrounds: 1031"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1748.1834709139546,
            "unit": "iter/sec",
            "range": "stddev: 0.00004219199942950949",
            "extra": "mean: 572.0223401249741 usec\nrounds: 638"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 940.8739348283611,
            "unit": "iter/sec",
            "range": "stddev: 0.00006690019633351744",
            "extra": "mean: 1.0628416443297741 msec\nrounds: 582"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 134.13625346806347,
            "unit": "iter/sec",
            "range": "stddev: 0.000134893899719706",
            "extra": "mean: 7.45510608910879 msec\nrounds: 101"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1746.5552073414501,
            "unit": "iter/sec",
            "range": "stddev: 0.00004767680388049448",
            "extra": "mean: 572.5556202269539 usec\nrounds: 969"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 804.8696324581888,
            "unit": "iter/sec",
            "range": "stddev: 0.000054315912782682525",
            "extra": "mean: 1.2424372341466714 msec\nrounds: 615"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 97.3362256173449,
            "unit": "iter/sec",
            "range": "stddev: 0.00018432988837918985",
            "extra": "mean: 10.273667318180912 msec\nrounds: 88"
          }
        ]
      }
    ]
  }
}