| Path (N: min / mean / max ms) | bound ms | unit 0, seed 1, none | unit 1, seed 2, none | unit 2, seed 3, composed | unit 3, seed 4, composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 342: 0.358 / 0.734 / 2.694 | 342: 0.355 / 0.733 / 2.650 | 342: 0.389 / 1.288 / 5.024 | 342: 0.384 / 1.296 / 6.728 |
| `acmp.bind_to_probe_tx` | - | 342: 0.548 / 0.923 / 2.883 | 342: 0.545 / 0.923 / 2.839 | 342: 0.579 / 1.477 / 5.213 | 342: 0.573 / 1.485 / 6.918 |
| `acmp.probe_tx` | 200.0 | 342: 0.399 / 1.045 / 4.487 | 342: 0.399 / 1.167 / 4.490 | 342: 0.399 / 2.959 / 5.593 | 342: 0.399 / 3.039 / 5.591 |
| `acmp.probe_tx.entity` | - | 342: 0.166 / 0.570 / 3.528 | 342: 0.171 / 0.643 / 3.534 | 342: 0.163 / 2.462 / 5.298 | 342: 0.164 / 2.546 / 5.245 |
| `aecp.response` | 240.0 | 342: 0.834 / 1.756 / 3.902 | 342: 0.834 / 1.709 / 3.550 | 342: 2.202 / 3.997 / 7.251 | 342: 2.328 / 4.037 / 6.882 |
| `aecp.response.get_avb_info` | - | 57: 1.353 / 1.731 / 3.716 | 57: 1.362 / 1.672 / 3.550 | 57: 2.825 / 3.964 / 6.214 | 57: 2.831 / 4.032 / 6.637 |
| `maap.egress` | 11.0 | 5: 0.323 / 0.556 / 0.856 | 5: 0.302 / 0.641 / 0.800 | 5: 0.981 / 1.639 / 2.457 | 5: 0.957 / 1.346 / 2.083 |
| `maap.probe_interval` | 600.0 | 3: 513.174 / 530.274 / 558.840 | 3: 513.086 / 530.344 / 559.099 | 3: 513.730 / 531.435 / 559.756 | 3: 513.386 / 531.094 / 560.408 |
| `maap.interval_error` | 11.0 | 4: 0.160 / 0.199 / 0.267 | 4: 0.086 / 0.209 / 0.498 | 4: 0.730 / 1.172 / 1.819 | 4: 0.021 / 0.576 / 1.408 |
| `maap.announce_interval` | 32000.0 | 1: 31957.267 / 31957.267 / 31957.267 | 1: 31956.502 / 31956.502 / 31956.502 | 1: 31958.383 / 31958.383 / 31958.383 | 1: 31957.021 / 31957.021 / 31957.021 |
| `adp.egress` | 400.0 | 6: 0.415 / 0.608 / 0.834 | 6: 0.355 / 0.494 / 0.839 | 6: 0.233 / 0.897 / 1.304 | 6: 0.281 / 1.229 / 2.637 |
| `adp.advertise_period` | 9400.0 | 5: 5362.581 / 6820.423 / 8387.053 | 5: 5363.114 / 6820.105 / 8385.816 | 5: 5362.966 / 6820.604 / 8385.438 | 5: 5364.705 / 6821.437 / 8387.356 |
| `egress.acmp.first` | - | 1026: 0.36 / 0.36 / 0.37 us | 1026: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us |
| `egress.maap.first` | - | 6: 0.36 / 0.36 / 0.37 us | 6: 0.36 / 0.36 / 0.37 us | 1656: 0.36 / 0.36 / 0.37 us | 1656: 0.36 / 0.36 / 0.37 us |

| Run | findings | censored | simulated ms | ready ms | load queued: offers (by an arm) / frames / echoes skipped | delivered: offers whole (in part) / frames | expiries met |
|---|---:|---|---:|---:|---|---|---|
| unit 0, seed 1, none | 0 | none | 34703 | 49.102 | none | none | - |
| unit 1, seed 2, none | 0 | none | 34706 | 49.102 | none | none | - |
| unit 2, seed 3, composed | 0 | none | 34705 | 49.102 | acmp 342 (0) / 21434 / 112, adp 12 (12) / 454 / 14, aecp 342 (0) / 20073 / 105, maap 6 (6) / 240 / 0 | acmp 342 (0) / 21434, adp 11 (0) / 415, aecp 342 (0) / 20073, maap 5 (0) / 200 | adp 11, maap 4 |
| unit 3, seed 4, composed | 0 | none | 34690 | 49.102 | acmp 342 (0) / 21434 / 112, adp 12 (12) / 454 / 14, aecp 342 (0) / 20073 / 105, maap 6 (6) / 240 / 0 | acmp 342 (0) / 21434, adp 11 (0) / 415, aecp 342 (0) / 20073, maap 5 (0) / 200 | adp 11, maap 4 |

unit 0, seed 1, none: delivered 0 + 4 x 342 = 1368; rx_frames 1368 + bench_rx 0 = 1368
  adp.advertise_period: margin 1012.947 ms to 9400.0, strict margin 612.947 ms to 9000.0
unit 1, seed 2, none: delivered 0 + 4 x 342 = 1368; rx_frames 1368 + bench_rx 0 = 1368
  adp.advertise_period: margin 1014.1839 ms to 9400.0, strict margin 614.1839 ms to 9000.0
unit 2, seed 3, composed: delivered 42122 + 4 x 342 = 43490; rx_frames 43490 + bench_rx 0 = 43490
  adp.advertise_period: margin 1014.5621 ms to 9400.0, strict margin 614.5621 ms to 9000.0
unit 3, seed 4, composed: delivered 42122 + 4 x 342 = 43490; rx_frames 43490 + bench_rx 0 = 43490
  adp.advertise_period: margin 1012.6435 ms to 9400.0, strict margin 612.6435 ms to 9000.0
