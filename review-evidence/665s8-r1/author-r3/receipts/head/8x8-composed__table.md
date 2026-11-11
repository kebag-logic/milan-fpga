| Path | N | min us | mean us | max us | min ms | mean ms | max ms | bound ms | margin ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `acmp.bind_rx` | 16 | 758.420 | 11940.055 | 18276.820 | 0.7584 | 11.9401 | 18.2768 | 200.0 | 181.7232 |
| `acmp.bind_to_probe_tx` | 16 | 965.140 | 12146.766 | 18483.540 | 0.9651 | 12.1468 | 18.4835 | - | - |
| `acmp.probe_tx` | 16 | 841.260 | 1921.071 | 5763.410 | 0.8413 | 1.9211 | 5.7634 | 200.0 | 194.2366 |
| `acmp.probe_tx.entity` | 16 | 180.480 | 1470.531 | 5042.550 | 0.1805 | 1.4705 | 5.0426 | - | - |
| `acmp.probe_tx.egress` | 16 | 1.760 | 1.766 | 1.770 | 0.0018 | 0.0018 | 0.0018 | - | - |
| `acmp.probe_tx.turnaround` | 16 | 0.020 | 450.540 | 901.060 | 0.0000 | 0.4505 | 0.9011 | - | - |
| `acmp.probe_tx.ingress` | 16 | 177.910 | 1467.966 | 5039.990 | 0.1779 | 1.4680 | 5.0400 | - | - |
| `aecp.response` | 16 | 4053.140 | 9819.575 | 24504.440 | 4.0531 | 9.8196 | 24.5044 | 240.0 | 215.4956 |
| `aecp.response.read_descriptor_entity` | 3 | 4556.280 | 8832.967 | 16617.120 | 4.5563 | 8.8330 | 16.6171 | - | - |
| `aecp.response.get_configuration` | 3 | 4569.920 | 9034.747 | 12294.920 | 4.5699 | 9.0347 | 12.2949 | - | - |
| `aecp.response.get_counters` | 3 | 5615.460 | 10135.913 | 14270.480 | 5.6155 | 10.1359 | 14.2705 | - | - |
| `aecp.response.get_avb_info` | 3 | 8543.160 | 15044.107 | 24504.440 | 8.5432 | 15.0441 | 24.5044 | - | - |
| `aecp.response.get_name` | 2 | 4602.320 | 8182.120 | 11761.920 | 4.6023 | 8.1821 | 11.7619 | - | - |
| `aecp.response.mvu_get_milan_info` | 2 | 4053.140 | 5802.880 | 7552.620 | 4.0531 | 5.8029 | 7.5526 | - | - |
| `maap.egress` | 4 | 1771.070 | 2036.200 | 2472.250 | 1.7711 | 2.0362 | 2.4722 | 11.0 | 8.5278 |
| `maap.probe_interval` | 3 | 516570.920 | 540662.647 | 583689.120 | 516.5709 | 540.6626 | 583.6891 | 600.0 | 16.3109 |
| `maap.interval_error` | 3 | 727.900 | 1329.313 | 1689.120 | 0.7279 | 1.3293 | 1.6891 | 11.0 | 9.3109 |
| `adp.egress` | 1 | 2207.210 | 2207.210 | 2207.210 | 2.2072 | 2.2072 | 2.2072 | 400.0 | 397.7928 |
| `egress.adp.first` | 1 | 0.370 | 0.370 | 0.370 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.adp.last` | 1 | 2.090 | 2.090 | 2.090 | 0.0021 | 0.0021 | 0.0021 | - | - |
| `egress.acmp.first` | 240 | 0.360 | 0.366 | 0.370 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.acmp.last` | 240 | 1.760 | 1.766 | 1.770 | 0.0018 | 0.0018 | 0.0018 | - | - |
| `egress.aecp.first` | 144 | 0.360 | 0.365 | 0.370 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.aecp.last` | 144 | 1.180 | 7.666 | 8.210 | 0.0012 | 0.0077 | 0.0082 | - | - |
| `egress.maap.first` | 9 | 0.360 | 0.363 | 0.370 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.maap.last` | 9 | 1.540 | 1.543 | 1.550 | 0.0015 | 0.0015 | 0.0015 | - | - |
| `egress.srp.first` | 7 | 0.360 | 0.364 | 0.370 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.srp.last` | 7 | 0.820 | 5.247 | 8.570 | 0.0008 | 0.0052 | 0.0086 | - | - |

Margin to a clause's own end, beside its widened bound: none.

Load: acmp: queued 16 offers (0 by a timer's arm), 896 frames, 112 echoes skipped; delivered (reached the MAC or the bench inside the run) 16 offers whole, 0 in part, 896 frames; adp: queued 2 offers (2 by a timer's arm), 64 frames, 14 echoes skipped; delivered (reached the MAC or the bench inside the run) 1 offers whole, 0 in part, 32 frames; expiries met 1; aecp: queued 16 offers (0 by a timer's arm), 839 frames, 105 echoes skipped; delivered (reached the MAC or the bench inside the run) 16 offers whole, 0 in part, 839 frames; maap: queued 5 offers (5 by a timer's arm), 200 frames, 0 echoes skipped; delivered (reached the MAC or the bench inside the run) 3 offers whole, 0 in part, 120 frames; expiries met 3. Simulated 2001 ms. Censored (the log ends within the command's bound, unanswered): none.
