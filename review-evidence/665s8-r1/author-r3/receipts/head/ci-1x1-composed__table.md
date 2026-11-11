| Path | N | min us | mean us | max us | min ms | mean ms | max ms | bound ms | margin ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `acmp.bind_rx` | 16 | 727.840 | 1338.959 | 3423.380 | 0.7278 | 1.3390 | 3.4234 | 200.0 | 196.5766 |
| `acmp.bind_to_probe_tx` | 16 | 917.320 | 1528.447 | 3612.880 | 0.9173 | 1.5284 | 3.6129 | - | - |
| `acmp.probe_tx` | 16 | 399.040 | 2945.760 | 5263.340 | 0.3990 | 2.9458 | 5.2633 | 200.0 | 194.7367 |
| `acmp.probe_tx.entity` | 16 | 218.820 | 2495.220 | 4539.250 | 0.2188 | 2.4952 | 4.5393 | - | - |
| `acmp.probe_tx.egress` | 16 | 1.760 | 1.764 | 1.770 | 0.0018 | 0.0018 | 0.0018 | - | - |
| `acmp.probe_tx.turnaround` | 16 | 0.020 | 450.540 | 901.060 | 0.0000 | 0.4505 | 0.9011 | - | - |
| `acmp.probe_tx.ingress` | 16 | 216.260 | 2492.656 | 4536.680 | 0.2163 | 2.4927 | 4.5367 | - | - |
| `aecp.response` | 16 | 3003.420 | 3710.403 | 4151.280 | 3.0034 | 3.7104 | 4.1513 | 240.0 | 235.8487 |
| `aecp.response.read_descriptor_entity` | 3 | 3948.760 | 4030.193 | 4151.280 | 3.9488 | 4.0302 | 4.1513 | - | - |
| `aecp.response.get_configuration` | 3 | 3223.440 | 3532.447 | 4116.220 | 3.2234 | 3.5324 | 4.1162 | - | - |
| `aecp.response.get_counters` | 3 | 3681.360 | 3923.847 | 4059.140 | 3.6814 | 3.9238 | 4.0591 | - | - |
| `aecp.response.get_avb_info` | 3 | 3296.000 | 3550.087 | 3746.020 | 3.2960 | 3.5501 | 3.7460 | - | - |
| `aecp.response.get_name` | 2 | 3468.180 | 3552.320 | 3636.460 | 3.4682 | 3.5523 | 3.6365 | - | - |
| `aecp.response.mvu_get_milan_info` | 2 | 3003.420 | 3576.040 | 4148.660 | 3.0034 | 3.5760 | 4.1487 | - | - |
| `maap.egress` | 4 | 1146.670 | 1546.405 | 1972.330 | 1.1467 | 1.5464 | 1.9723 | 11.0 | 9.0277 |
| `maap.probe_interval` | 3 | 514340.420 | 531270.540 | 560296.860 | 514.3404 | 531.2705 | 560.2969 | 600.0 | 39.7031 |
| `maap.interval_error` | 3 | 174.340 | 937.207 | 1340.420 | 0.1743 | 0.9372 | 1.3404 | 11.0 | 9.6596 |
| `adp.egress` | 1 | 1550.290 | 1550.290 | 1550.290 | 1.5503 | 1.5503 | 1.5503 | 400.0 | 398.4497 |
| `egress.adp.first` | 1 | 0.360 | 0.360 | 0.360 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.adp.last` | 1 | 2.080 | 2.080 | 2.080 | 0.0021 | 0.0021 | 0.0021 | - | - |
| `egress.acmp.first` | 240 | 0.360 | 0.365 | 0.370 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.acmp.last` | 240 | 1.760 | 1.765 | 1.770 | 0.0018 | 0.0018 | 0.0018 | - | - |
| `egress.aecp.first` | 272 | 0.360 | 0.365 | 0.370 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.aecp.last` | 272 | 1.180 | 7.920 | 8.210 | 0.0012 | 0.0079 | 0.0082 | - | - |
| `egress.maap.first` | 12 | 0.360 | 0.367 | 0.370 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.maap.last` | 12 | 1.540 | 1.548 | 1.550 | 0.0015 | 0.0015 | 0.0015 | - | - |
| `egress.srp.first` | 7 | 0.360 | 0.363 | 0.370 | 0.0004 | 0.0004 | 0.0004 | - | - |
| `egress.srp.last` | 7 | 0.820 | 1.874 | 2.670 | 0.0008 | 0.0019 | 0.0027 | - | - |

Margin to a clause's own end, beside its widened bound: none.

Load: acmp: queued 16 offers (0 by a timer's arm), 896 frames, 112 echoes skipped; delivered (reached the MAC or the bench inside the run) 16 offers whole, 0 in part, 896 frames; adp: queued 2 offers (2 by a timer's arm), 64 frames, 14 echoes skipped; delivered (reached the MAC or the bench inside the run) 1 offers whole, 0 in part, 32 frames; expiries met 1; aecp: queued 16 offers (0 by a timer's arm), 839 frames, 105 echoes skipped; delivered (reached the MAC or the bench inside the run) 16 offers whole, 0 in part, 839 frames; maap: queued 5 offers (5 by a timer's arm), 200 frames, 0 echoes skipped; delivered (reached the MAC or the bench inside the run) 3 offers whole, 0 in part, 120 frames; expiries met 3. Simulated 1935 ms. Censored (the log ends within the command's bound, unanswered): none.
