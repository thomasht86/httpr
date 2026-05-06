window.BENCHMARK_DATA = {
  "lastUpdate": 1778057060531,
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
          "id": "b2555766397f0e2e275e70f67334239027c8d813",
          "message": "Merge pull request #55 from thomasht86/andreer/dont-serialize-as-cbor\n\ndon't serialize as cbor",
          "timestamp": "2026-02-10T16:14:26Z",
          "url": "https://github.com/thomasht86/httpr/commit/b2555766397f0e2e275e70f67334239027c8d813"
        },
        "date": 1770740476179,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1722.3682183651208,
            "unit": "iter/sec",
            "range": "stddev: 0.00006215805896825882",
            "extra": "mean: 580.5959430377809 usec\nrounds: 474"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1783.2251881153309,
            "unit": "iter/sec",
            "range": "stddev: 0.00004188077355770343",
            "extra": "mean: 560.7816705734668 usec\nrounds: 1621"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 2175.3564232315834,
            "unit": "iter/sec",
            "range": "stddev: 0.000049347652773243744",
            "extra": "mean: 459.6947834941264 usec\nrounds: 1866"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1532.5856854196115,
            "unit": "iter/sec",
            "range": "stddev: 0.00007097584940944915",
            "extra": "mean: 652.4920658685435 usec\nrounds: 1169"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 753.0005257706284,
            "unit": "iter/sec",
            "range": "stddev: 0.00006555414460489033",
            "extra": "mean: 1.3280203210702806 msec\nrounds: 299"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 918.2968668329235,
            "unit": "iter/sec",
            "range": "stddev: 0.00003397035307544344",
            "extra": "mean: 1.088972462085011 msec\nrounds: 422"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 187.30265318041364,
            "unit": "iter/sec",
            "range": "stddev: 0.00007919693374740704",
            "extra": "mean: 5.338952668421521 msec\nrounds: 190"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.33471445674605,
            "unit": "iter/sec",
            "range": "stddev: 0.00032565704601909525",
            "extra": "mean: 42.85460624999852 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1401.3867729254705,
            "unit": "iter/sec",
            "range": "stddev: 0.00007216868140059111",
            "extra": "mean: 713.5788772377565 usec\nrounds: 782"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 2007.6116766873129,
            "unit": "iter/sec",
            "range": "stddev: 0.000031663478695808285",
            "extra": "mean: 498.10429557276916 usec\nrounds: 768"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 962.7671951332579,
            "unit": "iter/sec",
            "range": "stddev: 0.00008688164905214459",
            "extra": "mean: 1.038672697880601 msec\nrounds: 566"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 124.41076384841531,
            "unit": "iter/sec",
            "range": "stddev: 0.00025581507725526073",
            "extra": "mean: 8.037889721651585 msec\nrounds: 97"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1752.2055329291102,
            "unit": "iter/sec",
            "range": "stddev: 0.000035844269542363165",
            "extra": "mean: 570.7093039070193 usec\nrounds: 691"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 796.5988703794679,
            "unit": "iter/sec",
            "range": "stddev: 0.00005029550138782219",
            "extra": "mean: 1.2553369546251552 msec\nrounds: 573"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 91.08843720550765,
            "unit": "iter/sec",
            "range": "stddev: 0.00014337756444282032",
            "extra": "mean: 10.978341825580635 msec\nrounds: 86"
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
          "id": "a0b456d603e9fb10f0c33989958d757b3d20a04c",
          "message": "Merge pull request #54 from thomasht86/thomasht86/make-headers-insensitive\n\nfeat: make Client.headers case-insensitive",
          "timestamp": "2026-02-11T04:08:16Z",
          "url": "https://github.com/thomasht86/httpr/commit/a0b456d603e9fb10f0c33989958d757b3d20a04c"
        },
        "date": 1770783268815,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1541.9571030219054,
            "unit": "iter/sec",
            "range": "stddev: 0.00007858162172958688",
            "extra": "mean: 648.5264720012083 usec\nrounds: 500"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1711.083407264429,
            "unit": "iter/sec",
            "range": "stddev: 0.00006263155783479094",
            "extra": "mean: 584.42504658422 usec\nrounds: 1610"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 2212.9849474364323,
            "unit": "iter/sec",
            "range": "stddev: 0.00004948814942489411",
            "extra": "mean: 451.87835604504255 usec\nrounds: 1952"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1561.8052677622147,
            "unit": "iter/sec",
            "range": "stddev: 0.00006871573794329255",
            "extra": "mean: 640.2846889054355 usec\nrounds: 1334"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 777.1618313472927,
            "unit": "iter/sec",
            "range": "stddev: 0.00004901595190892687",
            "extra": "mean: 1.2867332898559798 msec\nrounds: 345"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 935.6524275786169,
            "unit": "iter/sec",
            "range": "stddev: 0.000043691724322338455",
            "extra": "mean: 1.0687729444446683 msec\nrounds: 450"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 200.44361862561462,
            "unit": "iter/sec",
            "range": "stddev: 0.00014767153315436437",
            "extra": "mean: 4.988934079601626 msec\nrounds: 201"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 22.468902001664755,
            "unit": "iter/sec",
            "range": "stddev: 0.0007317131728538524",
            "extra": "mean: 44.50595760869439 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1433.746040533417,
            "unit": "iter/sec",
            "range": "stddev: 0.00006705992647462576",
            "extra": "mean: 697.4735913676566 usec\nrounds: 1089"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 2015.2760864156137,
            "unit": "iter/sec",
            "range": "stddev: 0.000031957035439529924",
            "extra": "mean: 496.2099271363895 usec\nrounds: 796"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 1023.7259138731441,
            "unit": "iter/sec",
            "range": "stddev: 0.00001905588456601088",
            "extra": "mean: 976.8239588823342 usec\nrounds: 608"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 134.867322331221,
            "unit": "iter/sec",
            "range": "stddev: 0.00012791138142503894",
            "extra": "mean: 7.41469455102028 msec\nrounds: 98"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1794.253782344167,
            "unit": "iter/sec",
            "range": "stddev: 0.00003471673589021909",
            "extra": "mean: 557.3347593524447 usec\nrounds: 989"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 825.002314759234,
            "unit": "iter/sec",
            "range": "stddev: 0.00004209631201881135",
            "extra": "mean: 1.2121178111989137 msec\nrounds: 625"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 107.0558766645635,
            "unit": "iter/sec",
            "range": "stddev: 0.00039125400005826227",
            "extra": "mean: 9.34091645555605 msec\nrounds: 90"
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
          "id": "99df119fb9012f7c20ded16a066691d4890b15f0",
          "message": "Merge pull request #58 from thomasht86/copilot/update-lockfile-dependencies\n\nchore(deps): update uv.lock to resolve dependabot security issues",
          "timestamp": "2026-03-21T06:32:15Z",
          "url": "https://github.com/thomasht86/httpr/commit/99df119fb9012f7c20ded16a066691d4890b15f0"
        },
        "date": 1774075142637,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1754.623918194267,
            "unit": "iter/sec",
            "range": "stddev: 0.000032323372955933574",
            "extra": "mean: 569.922699463215 usec\nrounds: 559"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1794.7652856136242,
            "unit": "iter/sec",
            "range": "stddev: 0.00003511852670267797",
            "extra": "mean: 557.175920448062 usec\nrounds: 1785"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1897.8845046422673,
            "unit": "iter/sec",
            "range": "stddev: 0.00007855479546679548",
            "extra": "mean: 526.902452469567 usec\nrounds: 2146"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1553.7593716022802,
            "unit": "iter/sec",
            "range": "stddev: 0.00006909406513268032",
            "extra": "mean: 643.6003014860481 usec\nrounds: 1413"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 769.1375964531782,
            "unit": "iter/sec",
            "range": "stddev: 0.00006307140512557277",
            "extra": "mean: 1.3001574810689622 msec\nrounds: 449"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 886.3360100131562,
            "unit": "iter/sec",
            "range": "stddev: 0.00009224026382203166",
            "extra": "mean: 1.128240293413281 msec\nrounds: 167"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 203.94152357372795,
            "unit": "iter/sec",
            "range": "stddev: 0.00006634837867061938",
            "extra": "mean: 4.903366330096504 msec\nrounds: 206"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.776940555373592,
            "unit": "iter/sec",
            "range": "stddev: 0.00036536252509169",
            "extra": "mean: 42.05755562500239 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1420.3065856094272,
            "unit": "iter/sec",
            "range": "stddev: 0.0000853766188076895",
            "extra": "mean: 704.0733389058521 usec\nrounds: 1316"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1728.9470687663686,
            "unit": "iter/sec",
            "range": "stddev: 0.00011469919336146499",
            "extra": "mean: 578.3867060276842 usec\nrounds: 813"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 1035.7340562642312,
            "unit": "iter/sec",
            "range": "stddev: 0.000028432058764651265",
            "extra": "mean: 965.4988111589962 usec\nrounds: 699"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 142.6558450741012,
            "unit": "iter/sec",
            "range": "stddev: 0.00014786248186726458",
            "extra": "mean: 7.009877509614553 msec\nrounds: 104"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1642.6825255977715,
            "unit": "iter/sec",
            "range": "stddev: 0.000026879908372897397",
            "extra": "mean: 608.760356561351 usec\nrounds: 1105"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 769.7078315172137,
            "unit": "iter/sec",
            "range": "stddev: 0.00004337643763258683",
            "extra": "mean: 1.2991942644377734 msec\nrounds: 658"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 106.50563335959987,
            "unit": "iter/sec",
            "range": "stddev: 0.0003113904119283279",
            "extra": "mean: 9.389174717394093 msec\nrounds: 92"
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
          "id": "fdf29b29abde8ec990c77ed6e0adb60760142e58",
          "message": "Merge pull request #56 from thomasht86/dependabot/uv/cairosvg-2.9.0\n\nchore(deps): bump cairosvg from 2.7.1 to 2.9.0",
          "timestamp": "2026-03-21T06:52:28Z",
          "url": "https://github.com/thomasht86/httpr/commit/fdf29b29abde8ec990c77ed6e0adb60760142e58"
        },
        "date": 1774076334912,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1651.4807478601863,
            "unit": "iter/sec",
            "range": "stddev: 0.00007356555185969266",
            "extra": "mean: 605.5172010304656 usec\nrounds: 582"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1826.9182527668872,
            "unit": "iter/sec",
            "range": "stddev: 0.000038709976263629086",
            "extra": "mean: 547.3698664324412 usec\nrounds: 1707"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 2275.734056346904,
            "unit": "iter/sec",
            "range": "stddev: 0.00001641792680434869",
            "extra": "mean: 439.41865580077433 usec\nrounds: 2086"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1584.8192827301336,
            "unit": "iter/sec",
            "range": "stddev: 0.00006969084369265902",
            "extra": "mean: 630.9867698462892 usec\nrounds: 1373"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 774.6670020739743,
            "unit": "iter/sec",
            "range": "stddev: 0.00005806406157077052",
            "extra": "mean: 1.2908772379909739 msec\nrounds: 458"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 854.8102816402887,
            "unit": "iter/sec",
            "range": "stddev: 0.000052520797224619286",
            "extra": "mean: 1.169850224638276 msec\nrounds: 138"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 205.22838703071253,
            "unit": "iter/sec",
            "range": "stddev: 0.00005185443339602019",
            "extra": "mean: 4.87262027669861 msec\nrounds: 206"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.02551703820067,
            "unit": "iter/sec",
            "range": "stddev: 0.0004519913906109542",
            "extra": "mean: 43.43007795833387 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1419.4284802664931,
            "unit": "iter/sec",
            "range": "stddev: 0.00007309554997348367",
            "extra": "mean: 704.5089019294958 usec\nrounds: 1244"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1807.5616415131506,
            "unit": "iter/sec",
            "range": "stddev: 0.000040114746609783955",
            "extra": "mean: 553.231478824079 usec\nrounds: 850"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 985.0000227838393,
            "unit": "iter/sec",
            "range": "stddev: 0.00003636427302808061",
            "extra": "mean: 1.0152284029128924 msec\nrounds: 618"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 138.40540239176622,
            "unit": "iter/sec",
            "range": "stddev: 0.00025195927114564826",
            "extra": "mean: 7.225151494949812 msec\nrounds: 99"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1781.5244179244005,
            "unit": "iter/sec",
            "range": "stddev: 0.000024019322281952917",
            "extra": "mean: 561.3170327269885 usec\nrounds: 1100"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 823.8668776165329,
            "unit": "iter/sec",
            "range": "stddev: 0.00003953816060961227",
            "extra": "mean: 1.213788328149597 msec\nrounds: 643"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 106.12386111697136,
            "unit": "iter/sec",
            "range": "stddev: 0.0003697203938826492",
            "extra": "mean: 9.422951534884172 msec\nrounds: 86"
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
          "id": "b84a0556b41e7cf68c8fdbe5151094b3481bdf96",
          "message": "Merge pull request #60 from thomasht86/copilot/bump-dependencies-to-mitigate-vulnerabilities\n\nfix: bump dependencies to mitigate high-severity vulnerabilities",
          "timestamp": "2026-04-14T06:38:21Z",
          "url": "https://github.com/thomasht86/httpr/commit/b84a0556b41e7cf68c8fdbe5151094b3481bdf96"
        },
        "date": 1776149114579,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1711.655489354247,
            "unit": "iter/sec",
            "range": "stddev: 0.000040544417784008374",
            "extra": "mean: 584.2297157457007 usec\nrounds: 489"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1504.8872764862945,
            "unit": "iter/sec",
            "range": "stddev: 0.00006892251267258699",
            "extra": "mean: 664.5015979767355 usec\nrounds: 1582"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1978.3934969517445,
            "unit": "iter/sec",
            "range": "stddev: 0.00007511668881792512",
            "extra": "mean: 505.4606181938896 usec\nrounds: 1506"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1631.8916809849848,
            "unit": "iter/sec",
            "range": "stddev: 0.000037921108472688194",
            "extra": "mean: 612.7857698229183 usec\nrounds: 1299"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 721.4012482893063,
            "unit": "iter/sec",
            "range": "stddev: 0.00009065704058052993",
            "extra": "mean: 1.386191113990097 msec\nrounds: 386"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 814.618965129624,
            "unit": "iter/sec",
            "range": "stddev: 0.00003249120933720266",
            "extra": "mean: 1.2275677866656072 msec\nrounds: 75"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 192.79774244351339,
            "unit": "iter/sec",
            "range": "stddev: 0.00006124210226403838",
            "extra": "mean: 5.186782725388934 msec\nrounds: 193"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.257202219160103,
            "unit": "iter/sec",
            "range": "stddev: 0.0002668912476303",
            "extra": "mean: 42.9974332499962 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1310.425164402754,
            "unit": "iter/sec",
            "range": "stddev: 0.0011004109433835495",
            "extra": "mean: 763.1111086421827 usec\nrounds: 1215"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1852.106376611191,
            "unit": "iter/sec",
            "range": "stddev: 0.000020522231369515206",
            "extra": "mean: 539.925790779742 usec\nrounds: 846"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 935.3803705785124,
            "unit": "iter/sec",
            "range": "stddev: 0.000045379697994479706",
            "extra": "mean: 1.0690837989058095 msec\nrounds: 731"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 128.38992635982365,
            "unit": "iter/sec",
            "range": "stddev: 0.00018514320140009593",
            "extra": "mean: 7.788773063062713 msec\nrounds: 111"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1714.5733512056847,
            "unit": "iter/sec",
            "range": "stddev: 0.000032760584028486764",
            "extra": "mean: 583.2354733011579 usec\nrounds: 824"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 796.1302207539437,
            "unit": "iter/sec",
            "range": "stddev: 0.00005813692448832706",
            "extra": "mean: 1.2560759206615588 msec\nrounds: 605"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 95.31950376811223,
            "unit": "iter/sec",
            "range": "stddev: 0.00024726042308657957",
            "extra": "mean: 10.491032374997904 msec\nrounds: 88"
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
          "id": "aa34934415b1b193cbfbdca57fe93d0f8782d15f",
          "message": "Merge pull request #61 from thomasht86/copilot/change-log-level-to-debug\n\nLower log level for missing `HTTPR_CA_BUNDLE` in `load_ca_certs`",
          "timestamp": "2026-04-23T11:35:32Z",
          "url": "https://github.com/thomasht86/httpr/commit/aa34934415b1b193cbfbdca57fe93d0f8782d15f"
        },
        "date": 1776944532309,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1790.7135690208468,
            "unit": "iter/sec",
            "range": "stddev: 0.0000593579943147884",
            "extra": "mean: 558.4366016429948 usec\nrounds: 487"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1817.798245869078,
            "unit": "iter/sec",
            "range": "stddev: 0.00008181909838478519",
            "extra": "mean: 550.1160551081433 usec\nrounds: 1615"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 2197.8142486097404,
            "unit": "iter/sec",
            "range": "stddev: 0.00005980568769250301",
            "extra": "mean: 454.9975051952478 usec\nrounds: 1540"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1686.4662226396301,
            "unit": "iter/sec",
            "range": "stddev: 0.00005429595892971758",
            "extra": "mean: 592.9558425634021 usec\nrounds: 1264"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 798.8164396856562,
            "unit": "iter/sec",
            "range": "stddev: 0.00004965325966311162",
            "extra": "mean: 1.2518520530117179 msec\nrounds: 415"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 935.9699501230984,
            "unit": "iter/sec",
            "range": "stddev: 0.000029839757588459756",
            "extra": "mean: 1.0684103692308502 msec\nrounds: 65"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 191.22196010723349,
            "unit": "iter/sec",
            "range": "stddev: 0.004153656776529888",
            "extra": "mean: 5.229524890547194 msec\nrounds: 201"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.31395171994784,
            "unit": "iter/sec",
            "range": "stddev: 0.000358916542941038",
            "extra": "mean: 42.892771333329215 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1580.8056518477947,
            "unit": "iter/sec",
            "range": "stddev: 0.0000229423767292851",
            "extra": "mean: 632.5888314171358 usec\nrounds: 1044"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1873.379440690769,
            "unit": "iter/sec",
            "range": "stddev: 0.00004488464496679245",
            "extra": "mean: 533.7946911765356 usec\nrounds: 748"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 996.9598578195984,
            "unit": "iter/sec",
            "range": "stddev: 0.00004512565425631376",
            "extra": "mean: 1.0030494128289684 msec\nrounds: 608"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 120.6506404996063,
            "unit": "iter/sec",
            "range": "stddev: 0.00020002885882533367",
            "extra": "mean: 8.288393628571438 msec\nrounds: 105"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1877.8765409233968,
            "unit": "iter/sec",
            "range": "stddev: 0.00004355147926480127",
            "extra": "mean: 532.5163705960543 usec\nrounds: 823"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 827.857187310001,
            "unit": "iter/sec",
            "range": "stddev: 0.00006218940184815054",
            "extra": "mean: 1.2079378126188063 msec\nrounds: 523"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 88.08610190961943,
            "unit": "iter/sec",
            "range": "stddev: 0.0005241091822729701",
            "extra": "mean: 11.352528699999098 msec\nrounds: 80"
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
          "id": "bfcdec234d3f26b8393edf731083bd2abde456e6",
          "message": "Merge pull request #62 from greggdonovan/fix/reproducible-wheel-sbom\n\nDisable automatic SBOMs for reproducible wheels",
          "timestamp": "2026-04-24T10:49:47Z",
          "url": "https://github.com/thomasht86/httpr/commit/bfcdec234d3f26b8393edf731083bd2abde456e6"
        },
        "date": 1777028141085,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1984.874184260363,
            "unit": "iter/sec",
            "range": "stddev: 0.00003257264349622967",
            "extra": "mean: 503.8102706608765 usec\nrounds: 484"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 2040.5138410039544,
            "unit": "iter/sec",
            "range": "stddev: 0.000021666653543015057",
            "extra": "mean: 490.07263754113495 usec\nrounds: 1854"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 2785.2639327289858,
            "unit": "iter/sec",
            "range": "stddev: 0.000027326276141205333",
            "extra": "mean: 359.03240201017707 usec\nrounds: 2189"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1592.6990242022678,
            "unit": "iter/sec",
            "range": "stddev: 0.001133374722418482",
            "extra": "mean: 627.8650170586174 usec\nrounds: 1407"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 841.8346106945203,
            "unit": "iter/sec",
            "range": "stddev: 0.00004682662366863434",
            "extra": "mean: 1.187881784968418 msec\nrounds: 479"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 904.3157868064301,
            "unit": "iter/sec",
            "range": "stddev: 0.00003779306973329682",
            "extra": "mean: 1.1058084074054226 msec\nrounds: 54"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 205.97977751535834,
            "unit": "iter/sec",
            "range": "stddev: 0.00004863142735304801",
            "extra": "mean: 4.8548455196065925 msec\nrounds: 204"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.15544841246364,
            "unit": "iter/sec",
            "range": "stddev: 0.0004689384717913839",
            "extra": "mean: 43.18638025000373 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1693.0216208759643,
            "unit": "iter/sec",
            "range": "stddev: 0.000021943641679061428",
            "extra": "mean: 590.659911054534 usec\nrounds: 1158"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 2252.537295086027,
            "unit": "iter/sec",
            "range": "stddev: 0.0000358893378726845",
            "extra": "mean: 443.94381490665126 usec\nrounds: 805"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 1121.4928901811554,
            "unit": "iter/sec",
            "range": "stddev: 0.000038222588036244346",
            "extra": "mean: 891.6686041928178 usec\nrounds: 811"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 168.49515476032747,
            "unit": "iter/sec",
            "range": "stddev: 0.00011954306252030922",
            "extra": "mean: 5.934888759397443 msec\nrounds: 133"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 2039.6346882916152,
            "unit": "iter/sec",
            "range": "stddev: 0.000044337442924369164",
            "extra": "mean: 490.2838757059939 usec\nrounds: 1062"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 897.733563374382,
            "unit": "iter/sec",
            "range": "stddev: 0.00003873175522762412",
            "extra": "mean: 1.113916245084144 msec\nrounds: 661"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 124.5064937378513,
            "unit": "iter/sec",
            "range": "stddev: 0.0006579895983838812",
            "extra": "mean: 8.031709591834641 msec\nrounds: 98"
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
          "id": "f98c49ec5666c83693850223d14e19d47aca6d09",
          "message": "Merge pull request #63 from thomasht86/thomasht86/dependencies\n\nchore(deps): move benchmark deps to PEP 723 scripts, patch vulns",
          "timestamp": "2026-05-06T08:36:28Z",
          "url": "https://github.com/thomasht86/httpr/commit/f98c49ec5666c83693850223d14e19d47aca6d09"
        },
        "date": 1778057012817,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1690.2493624880187,
            "unit": "iter/sec",
            "range": "stddev: 0.00002857579559535593",
            "extra": "mean: 591.628680473523 usec\nrounds: 507"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1699.8631198326625,
            "unit": "iter/sec",
            "range": "stddev: 0.00003112446669669811",
            "extra": "mean: 588.2826613112483 usec\nrounds: 1556"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1839.4152444107049,
            "unit": "iter/sec",
            "range": "stddev: 0.00008089433212759169",
            "extra": "mean: 543.6510342287453 usec\nrounds: 1899"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1560.5354861410744,
            "unit": "iter/sec",
            "range": "stddev: 0.00006694396115891404",
            "extra": "mean: 640.8056778464047 usec\nrounds: 1133"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 731.444904842192,
            "unit": "iter/sec",
            "range": "stddev: 0.00006014009096012533",
            "extra": "mean: 1.3671569702378996 msec\nrounds: 336"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 804.6904180477796,
            "unit": "iter/sec",
            "range": "stddev: 0.0000237243853263321",
            "extra": "mean: 1.242713940133712 msec\nrounds: 451"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 196.8750989043635,
            "unit": "iter/sec",
            "range": "stddev: 0.00032077307025239575",
            "extra": "mean: 5.079362527638766 msec\nrounds: 199"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.59722514830354,
            "unit": "iter/sec",
            "range": "stddev: 0.0003156107313481307",
            "extra": "mean: 42.37786408000147 msec\nrounds: 25"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1429.7908963933048,
            "unit": "iter/sec",
            "range": "stddev: 0.00004012127599300756",
            "extra": "mean: 699.4029704081438 usec\nrounds: 980"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1684.709636005097,
            "unit": "iter/sec",
            "range": "stddev: 0.0000442678707799243",
            "extra": "mean: 593.5740964664219 usec\nrounds: 736"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 970.0209442213401,
            "unit": "iter/sec",
            "range": "stddev: 0.000053245915374789845",
            "extra": "mean: 1.0309055757581862 msec\nrounds: 594"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 135.28074637832876,
            "unit": "iter/sec",
            "range": "stddev: 0.0002275550645414185",
            "extra": "mean: 7.39203491089102 msec\nrounds: 101"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1712.6443997768695,
            "unit": "iter/sec",
            "range": "stddev: 0.000019870093303591268",
            "extra": "mean: 583.8923714288175 usec\nrounds: 945"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 819.4986319685786,
            "unit": "iter/sec",
            "range": "stddev: 0.00004880280359417642",
            "extra": "mean: 1.2202582908501332 msec\nrounds: 612"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 101.14016183920334,
            "unit": "iter/sec",
            "range": "stddev: 0.00033529810336047154",
            "extra": "mean: 9.887269130435442 msec\nrounds: 92"
          }
        ]
      }
    ]
  }
}