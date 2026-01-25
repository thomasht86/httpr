window.BENCHMARK_DATA = {
  "lastUpdate": 1769353074851,
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
          "id": "1a92887695411b5692374efb7e4c840cc356fe98",
          "message": "Merge pull request #52 from thomasht86/thomasht86/fix-mkdocs-site-backup\n\nfix: backup site/ directory before branch switch in mkdocs workflow",
          "timestamp": "2026-01-20T13:14:43Z",
          "url": "https://github.com/thomasht86/httpr/commit/1a92887695411b5692374efb7e4c840cc356fe98"
        },
        "date": 1768915211807,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1760.5006115276185,
            "unit": "iter/sec",
            "range": "stddev: 0.00004399985157768306",
            "extra": "mean: 568.0202514285309 usec\nrounds: 525"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1766.7579197132727,
            "unit": "iter/sec",
            "range": "stddev: 0.00005447921784876486",
            "extra": "mean: 566.0084999999831 usec\nrounds: 1680"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1983.3480676399954,
            "unit": "iter/sec",
            "range": "stddev: 0.00007608649595638972",
            "extra": "mean: 504.1979349544579 usec\nrounds: 1645"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1474.5350474247944,
            "unit": "iter/sec",
            "range": "stddev: 0.00007997886315072013",
            "extra": "mean: 678.1798789702914 usec\nrounds: 1165"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 789.790223818565,
            "unit": "iter/sec",
            "range": "stddev: 0.00005686442697939086",
            "extra": "mean: 1.2661590000001388 msec\nrounds: 339"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 828.3351057726621,
            "unit": "iter/sec",
            "range": "stddev: 0.00002003803389722607",
            "extra": "mean: 1.2072408775518582 msec\nrounds: 49"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 200.08024826644606,
            "unit": "iter/sec",
            "range": "stddev: 0.00002708864628252151",
            "extra": "mean: 4.997994597989023 msec\nrounds: 199"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.44865739328847,
            "unit": "iter/sec",
            "range": "stddev: 0.0006767262641628061",
            "extra": "mean: 42.646364916663515 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1456.7545808697566,
            "unit": "iter/sec",
            "range": "stddev: 0.00006030057488258305",
            "extra": "mean: 686.4574260703193 usec\nrounds: 1028"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1762.7916855919411,
            "unit": "iter/sec",
            "range": "stddev: 0.000044093119607911824",
            "extra": "mean: 567.2820039789344 usec\nrounds: 754"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 970.8620325687085,
            "unit": "iter/sec",
            "range": "stddev: 0.000025539979288974033",
            "extra": "mean: 1.030012469798822 msec\nrounds: 596"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 133.81075334111839,
            "unit": "iter/sec",
            "range": "stddev: 0.00017093060361639525",
            "extra": "mean: 7.473240939394012 msec\nrounds: 99"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1739.8131349728997,
            "unit": "iter/sec",
            "range": "stddev: 0.00002639389611062501",
            "extra": "mean: 574.7743708209081 usec\nrounds: 987"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 821.7595018698684,
            "unit": "iter/sec",
            "range": "stddev: 0.000046046108504582",
            "extra": "mean: 1.2169010491811232 msec\nrounds: 610"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 101.46846831891094,
            "unit": "iter/sec",
            "range": "stddev: 0.00013678803573646185",
            "extra": "mean: 9.85527835954953 msec\nrounds: 89"
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
          "id": "5b3c3948bc6d27847815874992ee6804e99076ed",
          "message": "Merge pull request #53 from thomasht86/thomasht86/make-headers-accessible\n\nfix: expose constructor headers via Client.headers property",
          "timestamp": "2026-01-25T14:52:06Z",
          "url": "https://github.com/thomasht86/httpr/commit/5b3c3948bc6d27847815874992ee6804e99076ed"
        },
        "date": 1769353068933,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1408.0132341843457,
            "unit": "iter/sec",
            "range": "stddev: 0.000057363708857594414",
            "extra": "mean: 710.2205971659737 usec\nrounds: 494"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1606.9745058580124,
            "unit": "iter/sec",
            "range": "stddev: 0.00007620073218976781",
            "extra": "mean: 622.2874080171357 usec\nrounds: 1397"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 2079.2052202526247,
            "unit": "iter/sec",
            "range": "stddev: 0.00006631909399910977",
            "extra": "mean: 480.9530056289967 usec\nrounds: 1954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1422.7436319876174,
            "unit": "iter/sec",
            "range": "stddev: 0.0000739906805718617",
            "extra": "mean: 702.8673174259571 usec\nrounds: 1383"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 783.911705093995,
            "unit": "iter/sec",
            "range": "stddev: 0.00006388605677560211",
            "extra": "mean: 1.2756538695644235 msec\nrounds: 345"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 857.3611101665173,
            "unit": "iter/sec",
            "range": "stddev: 0.00006878383686367904",
            "extra": "mean: 1.1663696756735085 msec\nrounds: 37"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 205.6276360165241,
            "unit": "iter/sec",
            "range": "stddev: 0.00007822271731516805",
            "extra": "mean: 4.8631595410630535 msec\nrounds: 207"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.26819804605748,
            "unit": "iter/sec",
            "range": "stddev: 0.0005624095805504049",
            "extra": "mean: 42.97711400000045 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1457.1594009536834,
            "unit": "iter/sec",
            "range": "stddev: 0.00006670200807799063",
            "extra": "mean: 686.2667182090846 usec\nrounds: 983"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1887.0393043790616,
            "unit": "iter/sec",
            "range": "stddev: 0.000023499199794451396",
            "extra": "mean: 529.9306684706571 usec\nrounds: 739"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 962.9758131936612,
            "unit": "iter/sec",
            "range": "stddev: 0.00003776046731795703",
            "extra": "mean: 1.0384476809272603 msec\nrounds: 561"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 130.87341495735362,
            "unit": "iter/sec",
            "range": "stddev: 0.00022526699543184734",
            "extra": "mean: 7.640971241759527 msec\nrounds: 91"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1710.0569233003066,
            "unit": "iter/sec",
            "range": "stddev: 0.000042410634258386645",
            "extra": "mean: 584.7758553382307 usec\nrounds: 871"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 801.369372952258,
            "unit": "iter/sec",
            "range": "stddev: 0.00006982781306106087",
            "extra": "mean: 1.2478640109691035 msec\nrounds: 547"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 97.97001388589,
            "unit": "iter/sec",
            "range": "stddev: 0.00023176383913888166",
            "extra": "mean: 10.207204840909222 msec\nrounds: 88"
          }
        ]
      }
    ]
  }
}