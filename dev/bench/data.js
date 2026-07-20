window.BENCHMARK_DATA = {
  "lastUpdate": 1784533636998,
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
          "id": "04d05b109f9be871ca9b605ddbe197b4233cdc15",
          "message": "Merge pull request #64 from thomasht86/claude/fix-ci-failure-OwPVI\n\nfix(deps): pin cbor2&lt;6 to restore Windows x86 wheel coverage",
          "timestamp": "2026-05-06T09:31:19Z",
          "url": "https://github.com/thomasht86/httpr/commit/04d05b109f9be871ca9b605ddbe197b4233cdc15"
        },
        "date": 1778060288861,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1502.6693850593147,
            "unit": "iter/sec",
            "range": "stddev: 0.00008323422017600835",
            "extra": "mean: 665.4823808502142 usec\nrounds: 470"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1573.3110928991755,
            "unit": "iter/sec",
            "range": "stddev: 0.00007286548310088739",
            "extra": "mean: 635.6022051285977 usec\nrounds: 1599"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1942.7897664905395,
            "unit": "iter/sec",
            "range": "stddev: 0.00007282960477399413",
            "extra": "mean: 514.7237324635505 usec\nrounds: 1839"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1500.7201779100508,
            "unit": "iter/sec",
            "range": "stddev: 0.00007014639421725835",
            "extra": "mean: 666.3467411977033 usec\nrounds: 1136"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 738.4142134280887,
            "unit": "iter/sec",
            "range": "stddev: 0.000052006970783162445",
            "extra": "mean: 1.3542534553303072 msec\nrounds: 347"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 896.0204123883306,
            "unit": "iter/sec",
            "range": "stddev: 0.000055892933406707476",
            "extra": "mean: 1.1160460031647195 msec\nrounds: 316"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 205.65163232248392,
            "unit": "iter/sec",
            "range": "stddev: 0.00004653683787556086",
            "extra": "mean: 4.862592086951648 msec\nrounds: 207"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.27260818467647,
            "unit": "iter/sec",
            "range": "stddev: 0.0004661432887690585",
            "extra": "mean: 42.96896987499821 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1368.6613797854714,
            "unit": "iter/sec",
            "range": "stddev: 0.00010581428144918686",
            "extra": "mean: 730.6409129164902 usec\nrounds: 1022"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1710.249846106709,
            "unit": "iter/sec",
            "range": "stddev: 0.0000383032513626095",
            "extra": "mean: 584.709890356924 usec\nrounds: 757"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 916.3570256549436,
            "unit": "iter/sec",
            "range": "stddev: 0.000029623717543735713",
            "extra": "mean: 1.0912777138204126 msec\nrounds: 615"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 135.07581449679654,
            "unit": "iter/sec",
            "range": "stddev: 0.0009146542533016897",
            "extra": "mean: 7.40324982473984 msec\nrounds: 97"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1621.265812189407,
            "unit": "iter/sec",
            "range": "stddev: 0.00003584175826095385",
            "extra": "mean: 616.8020027817458 usec\nrounds: 719"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 778.4544749821922,
            "unit": "iter/sec",
            "range": "stddev: 0.0000644402765609131",
            "extra": "mean: 1.2845966362039039 msec\nrounds: 569"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 118.46878619958869,
            "unit": "iter/sec",
            "range": "stddev: 0.0006200792628474032",
            "extra": "mean: 8.441042000002122 msec\nrounds: 90"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Andreas Eriksen",
            "username": "andreer",
            "email": "andreer@vespa.ai"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "f8c99983609440e5ad40c372170c323a4ad88e81",
          "message": "Merge pull request #66 from thomasht86/claude/fix-issue-65-ZAw2L\n\nfix(tls): apply client identity even when verify=False",
          "timestamp": "2026-05-12T08:30:02Z",
          "url": "https://github.com/thomasht86/httpr/commit/f8c99983609440e5ad40c372170c323a4ad88e81"
        },
        "date": 1778574999231,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1675.1810337955685,
            "unit": "iter/sec",
            "range": "stddev: 0.00004323988629358037",
            "extra": "mean: 596.9504070459977 usec\nrounds: 511"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1548.9084482318015,
            "unit": "iter/sec",
            "range": "stddev: 0.00009746781022875925",
            "extra": "mean: 645.6159504724616 usec\nrounds: 1696"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1960.556715719556,
            "unit": "iter/sec",
            "range": "stddev: 0.0000702375601706041",
            "extra": "mean: 510.05920511357607 usec\nrounds: 1682"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1572.3744252752285,
            "unit": "iter/sec",
            "range": "stddev: 0.00004784528646868266",
            "extra": "mean: 635.9808350513969 usec\nrounds: 1261"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 734.2396863317977,
            "unit": "iter/sec",
            "range": "stddev: 0.00005432392791686836",
            "extra": "mean: 1.3619530769249473 msec\nrounds: 351"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 818.7744173310525,
            "unit": "iter/sec",
            "range": "stddev: 0.000025141353081551615",
            "extra": "mean: 1.2213376222228411 msec\nrounds: 90"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 201.4930250117107,
            "unit": "iter/sec",
            "range": "stddev: 0.0003625908195488077",
            "extra": "mean: 4.962950950495087 msec\nrounds: 202"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.68328045896743,
            "unit": "iter/sec",
            "range": "stddev: 0.0004332490962573383",
            "extra": "mean: 42.22388033332436 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1470.5665111813626,
            "unit": "iter/sec",
            "range": "stddev: 0.000024732643086770077",
            "extra": "mean: 680.0100453781323 usec\nrounds: 1168"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1929.1367708220782,
            "unit": "iter/sec",
            "range": "stddev: 0.00003999843473953808",
            "extra": "mean: 518.3665643228925 usec\nrounds: 824"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 1018.5571932349253,
            "unit": "iter/sec",
            "range": "stddev: 0.00002198321351993545",
            "extra": "mean: 981.7809020856375 usec\nrounds: 623"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 139.10897198961922,
            "unit": "iter/sec",
            "range": "stddev: 0.00024955033567061356",
            "extra": "mean: 7.188608942309079 msec\nrounds: 104"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1684.4252577304314,
            "unit": "iter/sec",
            "range": "stddev: 0.00010502050058888406",
            "extra": "mean: 593.674308438823 usec\nrounds: 1031"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 830.2055862374999,
            "unit": "iter/sec",
            "range": "stddev: 0.00003102315721009808",
            "extra": "mean: 1.2045209241869959 msec\nrounds: 554"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 104.0049095402083,
            "unit": "iter/sec",
            "range": "stddev: 0.00041042088193506723",
            "extra": "mean: 9.61493072222134 msec\nrounds: 90"
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
          "id": "26b57de5cb1c38742e72ff1e240112272485eb22",
          "message": "Merge pull request #67 from thomasht86/andreer/fix-ca-bundle-silent-fallback\n\nfix ca bundle silent fallback",
          "timestamp": "2026-05-12T10:53:44Z",
          "url": "https://github.com/thomasht86/httpr/commit/26b57de5cb1c38742e72ff1e240112272485eb22"
        },
        "date": 1778583634566,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1603.291843740641,
            "unit": "iter/sec",
            "range": "stddev: 0.00006529612223019104",
            "extra": "mean: 623.7167636722329 usec\nrounds: 512"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1496.7091419103706,
            "unit": "iter/sec",
            "range": "stddev: 0.00007173523444382914",
            "extra": "mean: 668.1324861312862 usec\nrounds: 1370"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1936.2873743348205,
            "unit": "iter/sec",
            "range": "stddev: 0.00007693844537229175",
            "extra": "mean: 516.4522649142065 usec\nrounds: 1978"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1612.6138386089863,
            "unit": "iter/sec",
            "range": "stddev: 0.000027933700151370026",
            "extra": "mean: 620.1112604010539 usec\nrounds: 1298"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 740.1061768616601,
            "unit": "iter/sec",
            "range": "stddev: 0.00007545862774203448",
            "extra": "mean: 1.3511574842415064 msec\nrounds: 349"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 806.2973235520161,
            "unit": "iter/sec",
            "range": "stddev: 0.000027455862739106437",
            "extra": "mean: 1.2402372807026782 msec\nrounds: 114"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 199.4536864807488,
            "unit": "iter/sec",
            "range": "stddev: 0.00010640674395125293",
            "extra": "mean: 5.013695247475506 msec\nrounds: 198"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.829215464693412,
            "unit": "iter/sec",
            "range": "stddev: 0.0002526917775112306",
            "extra": "mean: 41.96529262499856 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1186.2478788754597,
            "unit": "iter/sec",
            "range": "stddev: 0.000025266147830183236",
            "extra": "mean: 842.9941311658915 usec\nrounds: 892"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1737.2595583409093,
            "unit": "iter/sec",
            "range": "stddev: 0.00004192144235980895",
            "extra": "mean: 575.6192246569099 usec\nrounds: 730"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 946.9012106064775,
            "unit": "iter/sec",
            "range": "stddev: 0.00009223089500932924",
            "extra": "mean: 1.0560763771328516 msec\nrounds: 586"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 63.96757307651383,
            "unit": "iter/sec",
            "range": "stddev: 0.04065416396454668",
            "extra": "mean: 15.632920742574763 msec\nrounds: 101"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1713.5057132526892,
            "unit": "iter/sec",
            "range": "stddev: 0.00007302136874162537",
            "extra": "mean: 583.5988711713918 usec\nrounds: 947"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 776.3161620042357,
            "unit": "iter/sec",
            "range": "stddev: 0.0000677652856264567",
            "extra": "mean: 1.288134975083185 msec\nrounds: 602"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 101.79692145541404,
            "unit": "iter/sec",
            "range": "stddev: 0.0007988043331205834",
            "extra": "mean: 9.8234797840914 msec\nrounds: 88"
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
          "id": "d2641dc0d0c9d2128232c57951ab7b452c6c3922",
          "message": "Merge pull request #68 from thomasht86/dependabot/uv/urllib3-2.7.0\n\nchore(deps): bump urllib3 from 2.6.3 to 2.7.0",
          "timestamp": "2026-05-12T11:45:04Z",
          "url": "https://github.com/thomasht86/httpr/commit/d2641dc0d0c9d2128232c57951ab7b452c6c3922"
        },
        "date": 1778586689884,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 2238.6189909119644,
            "unit": "iter/sec",
            "range": "stddev: 0.000049286305809270805",
            "extra": "mean: 446.7039742178824 usec\nrounds: 543"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 2384.3969939813956,
            "unit": "iter/sec",
            "range": "stddev: 0.00004010556932061073",
            "extra": "mean: 419.39324807243173 usec\nrounds: 2205"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 2777.0417268828846,
            "unit": "iter/sec",
            "range": "stddev: 0.00004792824273662986",
            "extra": "mean: 360.09541747954177 usec\nrounds: 2563"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 2222.810307337946,
            "unit": "iter/sec",
            "range": "stddev: 0.0000438383436333007",
            "extra": "mean: 449.880944270772 usec\nrounds: 1597"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 1025.8597069674088,
            "unit": "iter/sec",
            "range": "stddev: 0.00004446741417833662",
            "extra": "mean: 974.7921603784852 usec\nrounds: 424"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 1094.4572479944445,
            "unit": "iter/sec",
            "range": "stddev: 0.000024832061561621637",
            "extra": "mean: 913.6948947366064 usec\nrounds: 76"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 261.33734299416597,
            "unit": "iter/sec",
            "range": "stddev: 0.00005239196149133531",
            "extra": "mean: 3.826471902342421 msec\nrounds: 256"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 30.20656273647563,
            "unit": "iter/sec",
            "range": "stddev: 0.00019169888375492164",
            "extra": "mean: 33.1053886774234 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1796.7758338723745,
            "unit": "iter/sec",
            "range": "stddev: 0.0000545190590650844",
            "extra": "mean: 556.5524542061657 usec\nrounds: 1343"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 2564.211046274331,
            "unit": "iter/sec",
            "range": "stddev: 0.00003071913856106446",
            "extra": "mean: 389.98350055973344 usec\nrounds: 895"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 1304.3763365746322,
            "unit": "iter/sec",
            "range": "stddev: 0.00003333162076623912",
            "extra": "mean: 766.6499092018627 usec\nrounds: 826"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 169.68444801308414,
            "unit": "iter/sec",
            "range": "stddev: 0.00017592878715240839",
            "extra": "mean: 5.893292000000445 msec\nrounds: 118"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 2559.346959394193,
            "unit": "iter/sec",
            "range": "stddev: 0.00002333022866593265",
            "extra": "mean: 390.72467151413645 usec\nrounds: 1169"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 1092.0627294656695,
            "unit": "iter/sec",
            "range": "stddev: 0.000030774441848916146",
            "extra": "mean: 915.6983138590267 usec\nrounds: 736"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 125.0598930302365,
            "unit": "iter/sec",
            "range": "stddev: 0.00023308143493645352",
            "extra": "mean: 7.99616868181891 msec\nrounds: 110"
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
          "id": "396a53d18813d15f14c6a32890730fe42b9c89b7",
          "message": "Merge pull request #70 from Bing-su/feat/response-methods\n\nfeat(response): add HTTP status helpers",
          "timestamp": "2026-07-18T08:24:58Z",
          "url": "https://github.com/thomasht86/httpr/commit/396a53d18813d15f14c6a32890730fe42b9c89b7"
        },
        "date": 1784363541138,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1810.832613865317,
            "unit": "iter/sec",
            "range": "stddev: 0.000025150085190878103",
            "extra": "mean: 552.2321568228483 usec\nrounds: 491"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1676.531391843631,
            "unit": "iter/sec",
            "range": "stddev: 0.00006673036876149076",
            "extra": "mean: 596.4695948223972 usec\nrounds: 1661"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1916.6450321494335,
            "unit": "iter/sec",
            "range": "stddev: 0.000053017820811922334",
            "extra": "mean: 521.7450196704101 usec\nrounds: 1576"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1495.663513745479,
            "unit": "iter/sec",
            "range": "stddev: 0.00006515660570614043",
            "extra": "mean: 668.5995819312155 usec\nrounds: 1129"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 782.5169341322446,
            "unit": "iter/sec",
            "range": "stddev: 0.00005494181342351895",
            "extra": "mean: 1.2779276158527209 msec\nrounds: 328"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 837.3449903043518,
            "unit": "iter/sec",
            "range": "stddev: 0.000041238288135166186",
            "extra": "mean: 1.194250890109855 msec\nrounds: 91"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 197.12303135741195,
            "unit": "iter/sec",
            "range": "stddev: 0.00011472512726390391",
            "extra": "mean: 5.0729739346736125 msec\nrounds: 199"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.259503724508825,
            "unit": "iter/sec",
            "range": "stddev: 0.00028072401660713384",
            "extra": "mean: 42.99317869565238 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1537.064952158283,
            "unit": "iter/sec",
            "range": "stddev: 0.00004254951747362695",
            "extra": "mean: 650.5905938430523 usec\nrounds: 1007"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 2227.810904848118,
            "unit": "iter/sec",
            "range": "stddev: 0.000025514009282057395",
            "extra": "mean: 448.8711307695908 usec\nrounds: 780"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 954.9616448313427,
            "unit": "iter/sec",
            "range": "stddev: 0.00005045829566440137",
            "extra": "mean: 1.0471624754904283 msec\nrounds: 612"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 111.0673798370152,
            "unit": "iter/sec",
            "range": "stddev: 0.00026810392993038796",
            "extra": "mean: 9.003543627908039 msec\nrounds: 86"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1901.505946713155,
            "unit": "iter/sec",
            "range": "stddev: 0.000053091464160641967",
            "extra": "mean: 525.8989600997821 usec\nrounds: 802"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 846.661499854548,
            "unit": "iter/sec",
            "range": "stddev: 0.00003921232081362392",
            "extra": "mean: 1.181109569966031 msec\nrounds: 586"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 92.75293845890744,
            "unit": "iter/sec",
            "range": "stddev: 0.0009215696880617402",
            "extra": "mean: 10.781329590361521 msec\nrounds: 83"
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
          "id": "38f8d68c01e2ecf70f05a5ba2fd890b037733440",
          "message": "Merge pull request #72 from thomasht86/fix/mutable-client-headers\n\nfeat(client): make client.headers mutable in place (#69)",
          "timestamp": "2026-07-18T09:04:45Z",
          "url": "https://github.com/thomasht86/httpr/commit/38f8d68c01e2ecf70f05a5ba2fd890b037733440"
        },
        "date": 1784365915067,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1513.3568581066745,
            "unit": "iter/sec",
            "range": "stddev: 0.0000822988701262992",
            "extra": "mean: 660.7826796721804 usec\nrounds: 487"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1646.8360179628908,
            "unit": "iter/sec",
            "range": "stddev: 0.00006203979362731475",
            "extra": "mean: 607.2249993882109 usec\nrounds: 1635"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 2014.6194386816812,
            "unit": "iter/sec",
            "range": "stddev: 0.00006468520489671165",
            "extra": "mean: 496.3716624586806 usec\nrounds: 1505"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1554.0113675280181,
            "unit": "iter/sec",
            "range": "stddev: 0.00005051185674492817",
            "extra": "mean: 643.4959363204083 usec\nrounds: 1272"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 737.7319615669197,
            "unit": "iter/sec",
            "range": "stddev: 0.000060643759806400816",
            "extra": "mean: 1.3555058640485511 msec\nrounds: 331"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 862.734596107778,
            "unit": "iter/sec",
            "range": "stddev: 0.00009232009406572686",
            "extra": "mean: 1.1591050185207525 msec\nrounds: 54"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 202.03349765699613,
            "unit": "iter/sec",
            "range": "stddev: 0.00006539272505287141",
            "extra": "mean: 4.949674245098491 msec\nrounds: 204"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.24367672263434,
            "unit": "iter/sec",
            "range": "stddev: 0.0004401414467936068",
            "extra": "mean: 43.022453458329814 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1194.8098136774995,
            "unit": "iter/sec",
            "range": "stddev: 0.000018501914099232327",
            "extra": "mean: 836.9532862490513 usec\nrounds: 1069"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1809.3078247173346,
            "unit": "iter/sec",
            "range": "stddev: 0.000034218502380998174",
            "extra": "mean: 552.6975489404234 usec\nrounds: 756"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 906.6622046659103,
            "unit": "iter/sec",
            "range": "stddev: 0.0001298707921583982",
            "extra": "mean: 1.1029466044285845 msec\nrounds: 632"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 127.67112331477519,
            "unit": "iter/sec",
            "range": "stddev: 0.00020303951676413245",
            "extra": "mean: 7.832624747371291 msec\nrounds: 95"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1636.5229359619757,
            "unit": "iter/sec",
            "range": "stddev: 0.00003223899399868652",
            "extra": "mean: 611.0516253853682 usec\nrounds: 969"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 819.7816152465567,
            "unit": "iter/sec",
            "range": "stddev: 0.00004578225592465313",
            "extra": "mean: 1.2198370656302666 msec\nrounds: 579"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 105.8715590654289,
            "unit": "iter/sec",
            "range": "stddev: 0.00045064216955867956",
            "extra": "mean: 9.445407329668182 msec\nrounds: 91"
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
          "id": "618eb911e4ce39f4023e48b7f07c9ad4ebcf4667",
          "message": "Merge pull request #74 from thomasht86/fix/ci-freethreaded-abi3\n\nfix(ci): drop free-threaded 3.13t wheel build (abi3 incompatible)",
          "timestamp": "2026-07-18T09:48:00Z",
          "url": "https://github.com/thomasht86/httpr/commit/618eb911e4ce39f4023e48b7f07c9ad4ebcf4667"
        },
        "date": 1784368259004,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1682.8455497481873,
            "unit": "iter/sec",
            "range": "stddev: 0.00003329230662373713",
            "extra": "mean: 594.2315978728025 usec\nrounds: 470"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1639.5810684377882,
            "unit": "iter/sec",
            "range": "stddev: 0.00006639555658377498",
            "extra": "mean: 609.9118971609081 usec\nrounds: 1585"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1663.5741081730016,
            "unit": "iter/sec",
            "range": "stddev: 0.000020343470140197384",
            "extra": "mean: 601.1153907043173 usec\nrounds: 1592"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1557.435949611409,
            "unit": "iter/sec",
            "range": "stddev: 0.00005820589443377317",
            "extra": "mean: 642.0809794775232 usec\nrounds: 1072"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 740.2068286355385,
            "unit": "iter/sec",
            "range": "stddev: 0.00005483163965691318",
            "extra": "mean: 1.3509737566773758 msec\nrounds: 337"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 896.8564198838774,
            "unit": "iter/sec",
            "range": "stddev: 0.00003237369404242889",
            "extra": "mean: 1.115005677418775 msec\nrounds: 93"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 195.7464461364928,
            "unit": "iter/sec",
            "range": "stddev: 0.00009648174007266285",
            "extra": "mean: 5.108649580808768 msec\nrounds: 198"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 22.504704204797537,
            "unit": "iter/sec",
            "range": "stddev: 0.0007621023427978749",
            "extra": "mean: 44.435154130433794 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1378.2005758865253,
            "unit": "iter/sec",
            "range": "stddev: 0.00006348096093225362",
            "extra": "mean: 725.5837920084684 usec\nrounds: 976"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1782.876698639074,
            "unit": "iter/sec",
            "range": "stddev: 0.00003887573442628406",
            "extra": "mean: 560.8912835998875 usec\nrounds: 811"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 911.6321330247291,
            "unit": "iter/sec",
            "range": "stddev: 0.00005440570610563035",
            "extra": "mean: 1.0969336904372522 msec\nrounds: 617"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 119.61201237502664,
            "unit": "iter/sec",
            "range": "stddev: 0.0007723677174964973",
            "extra": "mean: 8.360364315789962 msec\nrounds: 95"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1648.9895444476333,
            "unit": "iter/sec",
            "range": "stddev: 0.00008687043421908613",
            "extra": "mean: 606.4319833725647 usec\nrounds: 842"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 809.448626361756,
            "unit": "iter/sec",
            "range": "stddev: 0.000057625729163456",
            "extra": "mean: 1.2354088541662227 msec\nrounds: 528"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 99.00063059687494,
            "unit": "iter/sec",
            "range": "stddev: 0.0003833824178061712",
            "extra": "mean: 10.100945761365342 msec\nrounds: 88"
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
          "id": "618eb911e4ce39f4023e48b7f07c9ad4ebcf4667",
          "message": "Merge pull request #74 from thomasht86/fix/ci-freethreaded-abi3\n\nfix(ci): drop free-threaded 3.13t wheel build (abi3 incompatible)",
          "timestamp": "2026-07-18T09:48:00Z",
          "url": "https://github.com/thomasht86/httpr/commit/618eb911e4ce39f4023e48b7f07c9ad4ebcf4667"
        },
        "date": 1784368405410,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1624.340332293619,
            "unit": "iter/sec",
            "range": "stddev: 0.000055203471240258586",
            "extra": "mean: 615.6345318274335 usec\nrounds: 487"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1699.6965095309724,
            "unit": "iter/sec",
            "range": "stddev: 0.000048521287719243035",
            "extra": "mean: 588.3403268716178 usec\nrounds: 1496"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1737.4626126787705,
            "unit": "iter/sec",
            "range": "stddev: 0.00006038782397751089",
            "extra": "mean: 575.5519530047488 usec\nrounds: 1298"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1444.0270964887955,
            "unit": "iter/sec",
            "range": "stddev: 0.00007774130295593151",
            "extra": "mean: 692.5077807968676 usec\nrounds: 1104"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 729.7984378932634,
            "unit": "iter/sec",
            "range": "stddev: 0.000059845285975932897",
            "extra": "mean: 1.370241354430324 msec\nrounds: 316"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 798.5035152764752,
            "unit": "iter/sec",
            "range": "stddev: 0.00004637415344712603",
            "extra": "mean: 1.252342639535855 msec\nrounds: 86"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 189.36654313557787,
            "unit": "iter/sec",
            "range": "stddev: 0.000788811117375489",
            "extra": "mean: 5.280763874345244 msec\nrounds: 191"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 23.673985591762836,
            "unit": "iter/sec",
            "range": "stddev: 0.0002821272498981823",
            "extra": "mean: 42.2404582500017 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1265.247600302486,
            "unit": "iter/sec",
            "range": "stddev: 0.00007305334852372113",
            "extra": "mean: 790.3591358410223 usec\nrounds: 957"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1893.1801708692526,
            "unit": "iter/sec",
            "range": "stddev: 0.00004143434151986318",
            "extra": "mean: 528.2117441262078 usec\nrounds: 766"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 947.184508997928,
            "unit": "iter/sec",
            "range": "stddev: 0.00003177439874225933",
            "extra": "mean: 1.0557605097004257 msec\nrounds: 567"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 115.68503099705295,
            "unit": "iter/sec",
            "range": "stddev: 0.0004524241168880864",
            "extra": "mean: 8.644160712767366 msec\nrounds: 94"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1904.9132380634537,
            "unit": "iter/sec",
            "range": "stddev: 0.000027098401748813647",
            "extra": "mean: 524.9582920724547 usec\nrounds: 719"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 833.911734719479,
            "unit": "iter/sec",
            "range": "stddev: 0.000059275272995113146",
            "extra": "mean: 1.199167679702207 msec\nrounds: 537"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 93.0050397527123,
            "unit": "iter/sec",
            "range": "stddev: 0.000270867829590167",
            "extra": "mean: 10.752105505882943 msec\nrounds: 85"
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
          "id": "3a08dd9962f72854ea5185c6ac3704d6fb92dc1e",
          "message": "Merge pull request #76 from thomasht86/fix/windows-x86-ci-and-benchmark-cleanup\n\nfix(ci): skip pytest on Windows x86 and remove legacy benchmark.jpg p…",
          "timestamp": "2026-07-20T07:11:45Z",
          "url": "https://github.com/thomasht86/httpr/commit/3a08dd9962f72854ea5185c6ac3704d6fb92dc1e"
        },
        "date": 1784531768726,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 3185.427289039834,
            "unit": "iter/sec",
            "range": "stddev: 0.000023325070491767786",
            "extra": "mean: 313.9296267853047 usec\nrounds: 560"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 3073.459829905604,
            "unit": "iter/sec",
            "range": "stddev: 0.0000451962597517531",
            "extra": "mean: 325.3662176644467 usec\nrounds: 2706"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 3571.3825668827176,
            "unit": "iter/sec",
            "range": "stddev: 0.00004982276865731486",
            "extra": "mean: 280.0036068028552 usec\nrounds: 2940"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 2817.7655922663616,
            "unit": "iter/sec",
            "range": "stddev: 0.00006629082173335221",
            "extra": "mean: 354.8911246359881 usec\nrounds: 1717"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 1209.385328426248,
            "unit": "iter/sec",
            "range": "stddev: 0.00004425032804109086",
            "extra": "mean: 826.8663233258193 usec\nrounds: 433"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 1397.587111458948,
            "unit": "iter/sec",
            "range": "stddev: 0.000022240783349070967",
            "extra": "mean: 715.5189052624386 usec\nrounds: 95"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 369.28642805637827,
            "unit": "iter/sec",
            "range": "stddev: 0.00007886014699708246",
            "extra": "mean: 2.7079251335154177 msec\nrounds: 367"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 43.16904715773704,
            "unit": "iter/sec",
            "range": "stddev: 0.0005584903922313092",
            "extra": "mean: 23.16474571111245 msec\nrounds: 45"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 2755.703549479995,
            "unit": "iter/sec",
            "range": "stddev: 0.000015908625630091882",
            "extra": "mean: 362.88373623813834 usec\nrounds: 1308"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 3971.723471132039,
            "unit": "iter/sec",
            "range": "stddev: 0.00004265283200399135",
            "extra": "mean: 251.77986515636636 usec\nrounds: 927"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 1895.77132116557,
            "unit": "iter/sec",
            "range": "stddev: 0.00003318394546327059",
            "extra": "mean: 527.4897815128745 usec\nrounds: 952"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 225.69561660548257,
            "unit": "iter/sec",
            "range": "stddev: 0.00016298163754325197",
            "extra": "mean: 4.4307462193561635 msec\nrounds: 155"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 4058.7757902429094,
            "unit": "iter/sec",
            "range": "stddev: 0.000012439622307181212",
            "extra": "mean: 246.37970946903476 usec\nrounds: 1394"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 1589.0759390990659,
            "unit": "iter/sec",
            "range": "stddev: 0.00004107398696295811",
            "extra": "mean: 629.2965461216126 usec\nrounds: 954"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 164.57087721329003,
            "unit": "iter/sec",
            "range": "stddev: 0.00033045843480688397",
            "extra": "mean: 6.0764092464790265 msec\nrounds: 142"
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
          "id": "48d9b7de47371195125f14ed11e171f12b87ef67",
          "message": "Merge pull request #79 from thomasht86/chore/drop-py39\n\nchore(deps): drop Python 3.9 support",
          "timestamp": "2026-07-20T07:41:38Z",
          "url": "https://github.com/thomasht86/httpr/commit/48d9b7de47371195125f14ed11e171f12b87ef67"
        },
        "date": 1784533306704,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 2678.199976910195,
            "unit": "iter/sec",
            "range": "stddev: 0.00006032695086572733",
            "extra": "mean: 373.38511262093556 usec\nrounds: 515"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 2686.86546408462,
            "unit": "iter/sec",
            "range": "stddev: 0.00006401203084351712",
            "extra": "mean: 372.18089754288724 usec\nrounds: 2157"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 3719.899702157101,
            "unit": "iter/sec",
            "range": "stddev: 0.00004528023031778878",
            "extra": "mean: 268.82445228835564 usec\nrounds: 2054"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1964.1574459218923,
            "unit": "iter/sec",
            "range": "stddev: 0.00003819587279179501",
            "extra": "mean: 509.12415502955895 usec\nrounds: 1690"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 998.9041064776671,
            "unit": "iter/sec",
            "range": "stddev: 0.00003658830896373615",
            "extra": "mean: 1.001097095822538 msec\nrounds: 407"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 1506.8380395825714,
            "unit": "iter/sec",
            "range": "stddev: 0.000025038505616364484",
            "extra": "mean: 663.64132954662 usec\nrounds: 88"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 344.89433161343703,
            "unit": "iter/sec",
            "range": "stddev: 0.0000609907169567544",
            "extra": "mean: 2.8994387797617263 msec\nrounds: 336"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 40.37013720675547,
            "unit": "iter/sec",
            "range": "stddev: 0.0002015882280253479",
            "extra": "mean: 24.770785268291377 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 2297.6572705443577,
            "unit": "iter/sec",
            "range": "stddev: 0.00005355880898370152",
            "extra": "mean: 435.2259202535813 usec\nrounds: 1580"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 3014.050854238306,
            "unit": "iter/sec",
            "range": "stddev: 0.00003946371523106079",
            "extra": "mean: 331.7794053122287 usec\nrounds: 866"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 1433.025301505028,
            "unit": "iter/sec",
            "range": "stddev: 0.00005367335100851608",
            "extra": "mean: 697.8243852008438 usec\nrounds: 919"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 204.70856962954952,
            "unit": "iter/sec",
            "range": "stddev: 0.0001742823145687732",
            "extra": "mean: 4.884993343510963 msec\nrounds: 131"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 3237.721025705189,
            "unit": "iter/sec",
            "range": "stddev: 0.000012535031486958483",
            "extra": "mean: 308.8592229104099 usec\nrounds: 1292"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 1291.8207039376248,
            "unit": "iter/sec",
            "range": "stddev: 0.000045773442138642054",
            "extra": "mean: 774.1012332066515 usec\nrounds: 789"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 165.71237747278496,
            "unit": "iter/sec",
            "range": "stddev: 0.00011696520735485605",
            "extra": "mean: 6.034552248001091 msec\nrounds: 125"
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
          "id": "48d9b7de47371195125f14ed11e171f12b87ef67",
          "message": "Merge pull request #79 from thomasht86/chore/drop-py39\n\nchore(deps): drop Python 3.9 support",
          "timestamp": "2026-07-20T07:41:38Z",
          "url": "https://github.com/thomasht86/httpr/commit/48d9b7de47371195125f14ed11e171f12b87ef67"
        },
        "date": 1784533585469,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_single_request",
            "value": 1697.3917653357062,
            "unit": "iter/sec",
            "range": "stddev: 0.000032241230051177454",
            "extra": "mean: 589.1391842602832 usec\nrounds: 521"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_session_reuse",
            "value": 1740.5845725718623,
            "unit": "iter/sec",
            "range": "stddev: 0.00003549410004253028",
            "extra": "mean: 574.5196273470439 usec\nrounds: 1704"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_json_parsing",
            "value": 1935.6768352476843,
            "unit": "iter/sec",
            "range": "stddev: 0.00006931719927064746",
            "extra": "mean: 516.6151610591768 usec\nrounds: 1813"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestSyncClient::test_post_json",
            "value": 1377.8527324217127,
            "unit": "iter/sec",
            "range": "stddev: 0.000059637318331727174",
            "extra": "mean: 725.7669680288698 usec\nrounds: 1126"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestAsyncClient::test_full_overhead",
            "value": 731.8800028342663,
            "unit": "iter/sec",
            "range": "stddev: 0.000054481091311443686",
            "extra": "mean: 1.3663442041419587 msec\nrounds: 338"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[1KB]",
            "value": 819.9802127316902,
            "unit": "iter/sec",
            "range": "stddev: 0.00010080367554839894",
            "extra": "mean: 1.219541623655271 msec\nrounds: 93"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[10KB]",
            "value": 197.66174465933537,
            "unit": "iter/sec",
            "range": "stddev: 0.00023478761387502777",
            "extra": "mean: 5.059147897958064 msec\nrounds: 196"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestResponseSizes::test_response_size[100KB]",
            "value": 22.968087954849654,
            "unit": "iter/sec",
            "range": "stddev: 0.0005211811773428716",
            "extra": "mean: 43.5386699130457 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestHeaders::test_many_headers",
            "value": 1398.7581789801686,
            "unit": "iter/sec",
            "range": "stddev: 0.00006542512471152699",
            "extra": "mean: 714.9198589345142 usec\nrounds: 957"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[1_array]",
            "value": 1997.7216737228139,
            "unit": "iter/sec",
            "range": "stddev: 0.000021824524834083314",
            "extra": "mean: 500.5702311556095 usec\nrounds: 796"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[10_arrays]",
            "value": 985.2450373450926,
            "unit": "iter/sec",
            "range": "stddev: 0.00002188922400118989",
            "extra": "mean: 1.014975931971875 msec\nrounds: 588"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_cbor_request[100_arrays]",
            "value": 121.64352315559633,
            "unit": "iter/sec",
            "range": "stddev: 0.0006229352466950834",
            "extra": "mean: 8.220741836956522 msec\nrounds: 92"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[1_array]",
            "value": 1791.8477041382173,
            "unit": "iter/sec",
            "range": "stddev: 0.00003553329926150757",
            "extra": "mean: 558.0831438355674 usec\nrounds: 876"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[10_arrays]",
            "value": 833.7012039887428,
            "unit": "iter/sec",
            "range": "stddev: 0.00004218940057079571",
            "extra": "mean: 1.1994705000012242 msec\nrounds: 548"
          },
          {
            "name": "tests/benchmark/test_performance.py::TestCBORDecoding::test_json_request[100_arrays]",
            "value": 97.11768291986989,
            "unit": "iter/sec",
            "range": "stddev: 0.00021548679235838686",
            "extra": "mean: 10.296786022222983 msec\nrounds: 90"
          }
        ]
      }
    ]
  }
}