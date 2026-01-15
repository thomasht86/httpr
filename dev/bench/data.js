window.BENCHMARK_DATA = {
  "lastUpdate": 1768473165748,
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
      },
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
          "id": "6e9ffd4686e1636c8b65e1a588695218d11b149d",
          "message": "Merge pull request #50 from thomasht86/thomasht86/fix-benchmark-persistence\n\nfix: preserve benchmark data across mkdocs deployments",
          "timestamp": "2026-01-15T10:26:30Z",
          "url": "https://github.com/thomasht86/httpr/commit/6e9ffd4686e1636c8b65e1a588695218d11b149d"
        },
        "date": 1768473159510,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1748.771671649341,
            "unit": "iter/sec",
            "range": "stddev: 0.000050142867257295636",
            "extra": "mean: 571.8299399582894 usec\nrounds: 483"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1665.0064157796164,
            "unit": "iter/sec",
            "range": "stddev: 0.00006312800762621897",
            "extra": "mean: 600.5982863025567 usec\nrounds: 1701"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 2069.1686071758386,
            "unit": "iter/sec",
            "range": "stddev: 0.00006313652981882976",
            "extra": "mean: 483.2858939247476 usec\nrounds: 2074"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1545.0231500000937,
            "unit": "iter/sec",
            "range": "stddev: 0.0000671117438703737",
            "extra": "mean: 647.2394928192108 usec\nrounds: 1323"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 773.9268475136139,
            "unit": "iter/sec",
            "range": "stddev: 0.00005538501341496127",
            "extra": "mean: 1.2921117844828471 msec\nrounds: 348"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 931.0385091271374,
            "unit": "iter/sec",
            "range": "stddev: 0.000023476137886179214",
            "extra": "mean: 1.0740694291340485 msec\nrounds: 508"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 200.7814590193437,
            "unit": "iter/sec",
            "range": "stddev: 0.00008949771410287823",
            "extra": "mean: 4.9805395621896436 msec\nrounds: 201"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.034597827731503,
            "unit": "iter/sec",
            "range": "stddev: 0.00034088918772748865",
            "extra": "mean: 43.41295678260523 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1441.4850960841509,
            "unit": "iter/sec",
            "range": "stddev: 0.00006414885714530368",
            "extra": "mean: 693.728990134229 usec\nrounds: 1115"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1848.8132121906528,
            "unit": "iter/sec",
            "range": "stddev: 0.000037148949485545333",
            "extra": "mean: 540.8875236320403 usec\nrounds: 804"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 945.4603796704623,
            "unit": "iter/sec",
            "range": "stddev: 0.00009708637385842448",
            "extra": "mean: 1.0576857809192888 msec\nrounds: 566"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 133.0267340334116,
            "unit": "iter/sec",
            "range": "stddev: 0.0002629732878853682",
            "extra": "mean: 7.517285959593921 msec\nrounds: 99"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1743.0643747317952,
            "unit": "iter/sec",
            "range": "stddev: 0.000046988350146446984",
            "extra": "mean: 573.7022765747648 usec\nrounds: 1016"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 816.15240063313,
            "unit": "iter/sec",
            "range": "stddev: 0.00006041189411104257",
            "extra": "mean: 1.2252613595503123 msec\nrounds: 623"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 104.54753688289608,
            "unit": "iter/sec",
            "range": "stddev: 0.0008781225678422608",
            "extra": "mean: 9.565026875000433 msec\nrounds: 88"
          }
        ]
      }
    ]
  }
}