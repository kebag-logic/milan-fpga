Share: 18 ms over 9 passes, 2.000 ms of CPU time.
Legs: D11-A1-100, D11-A1-50, D11-A8-100, D11-A8-50, D11-B1-100, D11-B1-50, D11-B8-100, D11-B8-50, N11-A1-100, N11-A1-50, N11-A8-100, N11-A8-50, N11-B1-100, N11-B1-50, N11-B8-100, N11-B8-50.

| 8x8: row | Bound, ms | CPU 50 MHz (product) | CPU 50 MHz (product), with both drafts | CPU 100 MHz (labelled option) | CPU 100 MHz (labelled option), with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 3.41 / 3.42 | 3.24 / 3.25 | 1.95 / 1.96 | 1.86 / 1.87 |
| ACMP record, last | 20 | 14.37 / 14.72 | 13.79 / 13.80 | 8.79 / 8.82 | 8.30 / 8.12 |
| ADP record, first | 20 | 3.45 / 3.46 | 3.28 / 3.29 | 1.99 / 2.00 | 1.91 / 1.92 |
| ADP record, last | 20 | 11.20 / 11.23 | 10.59 / 10.61 | 6.67 / 6.69 | 6.31 / 6.33 |
| AECP record, first | 20 | 3.45 / 3.46 | 3.27 / 3.29 | 1.98 / 1.99 | 1.90 / 1.91 |
| AECP record, first, in the owed window | 20 | 2.14 / 2.20 | 2.02 / 0.86 | 1.17 / 1.17 | 1.12 / 1.07 |
| AECP record, last | 20 | **25.02** / **25.61** | **24.02** / **24.11** | 15.10 / 15.84 | 13.74 / 14.61 |
| AECP record, last, in the owed window | 20 | **68.53** / **68.46** | **68.71** / **68.75** | **65.03** / **64.94** | **65.02** / **65.09** |
| MAAP record, first | 20 | 3.44 / 3.45 | 3.26 / 3.28 | 1.97 / 1.98 | 1.89 / 1.90 |
| MAAP record, last | 20 | 11.19 / 11.21 | 10.57 / 10.59 | 6.65 / 6.68 | 6.29 / 6.32 |
| SRP record, first | 18 | 9.23 / 9.26 | 8.78 / 8.79 | 4.26 / 4.28 | 5.12 / 4.10 |
| SRP record, last | 18 | **28.25** / **27.25** | **25.66** / **25.45** | 16.95 / 16.32 | 15.60 / 15.40 |
| a response with 7 frames owed ahead of it | 20 | **66.26** / **66.20** | **66.41** / **66.45** | **63.70** / **63.64** | **63.69** / **63.74** |
| an ACMP command behind a full acmp ring | 20 | 13.57 / 13.60 | 12.71 / 12.72 | 8.13 / 8.15 | 7.64 / 7.45 |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 7.63 / 7.87 | 7.32 / 7.23 | 4.13 / 4.32 | 3.33 / 4.03 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.38 / 0.41 | 0.27 / 0.17 | 0.09 / 0.23 | 0.18 / 0.12 |
| an event behind 15 others | 20 | 3.63 / 3.64 | 3.46 / 3.48 | 2.09 / 2.10 | 2.01 / 2.02 |

| 8x8: row over its bound | Leg | Bound, ms | Worst instance | ms | Over by, ms |
|---|---|---:|---|---:|---:|
| AECP record, last, in the owed window | D11-A8-100 | 20 | `backlog-owed.service.aecp.last.if1` | 65.02 | 45.02 |
| a response with 7 frames owed ahead of it | D11-A8-100 | 20 | `backlog.owed.if0` | 63.69 | 43.69 |
| an ACMP command behind the owed input | D11-A8-100 | 20 | `backlog.owed_behind0.if0` | at least 360.43 | unbounded |
| AECP record, last | D11-A8-50 | 20 | `backlog-adp.service.aecp.last.if1` | 24.02 | 4.02 |
| AECP record, last, in the owed window | D11-A8-50 | 20 | `backlog-owed.service.aecp.last.if1` | 68.71 | 48.71 |
| SRP record, last | D11-A8-50 | 18 | `backlog-adp-refill.service.srp.last.if1` | 25.66 | 7.66 |
| a response with 7 frames owed ahead of it | D11-A8-50 | 20 | `backlog.owed.if0` | 66.41 | 46.41 |
| an ACMP command behind the owed input | D11-A8-50 | 20 | `backlog.owed_behind0.if0` | at least 360.75 | unbounded |
| AECP record, last, in the owed window | D11-B8-100 | 20 | `backlog-owed.service.aecp.last.if1` | 65.09 | 45.09 |
| a response with 7 frames owed ahead of it | D11-B8-100 | 20 | `backlog.owed.if0` | 63.74 | 43.74 |
| an ACMP command behind the owed input | D11-B8-100 | 20 | `backlog.owed_behind0.if0` | at least 360.48 | unbounded |
| AECP record, last | D11-B8-50 | 20 | `backlog-adp.service.aecp.last.if1` | 24.11 | 4.11 |
| AECP record, last, in the owed window | D11-B8-50 | 20 | `backlog-owed.service.aecp.last.if1` | 68.75 | 48.75 |
| SRP record, last | D11-B8-50 | 18 | `backlog-adp.service.srp.last.if1` | 25.45 | 7.45 |
| a response with 7 frames owed ahead of it | D11-B8-50 | 20 | `backlog.owed.if0` | 66.45 | 46.45 |
| an ACMP command behind the owed input | D11-B8-50 | 20 | `backlog.owed_behind0.if0` | at least 360.67 | unbounded |
| AECP record, last, in the owed window | N11-A8-100 | 20 | `backlog-owed.service.aecp.last.if1` | 65.03 | 45.03 |
| a response with 7 frames owed ahead of it | N11-A8-100 | 20 | `backlog.owed.if0` | 63.70 | 43.70 |
| an ACMP command behind the owed input | N11-A8-100 | 20 | `backlog.owed_behind0.if0` | at least 360.38 | unbounded |
| AECP record, last | N11-A8-50 | 20 | `backlog-adp.service.aecp.last.if1` | 25.02 | 5.02 |
| AECP record, last, in the owed window | N11-A8-50 | 20 | `backlog-owed.service.aecp.last.if1` | 68.53 | 48.53 |
| SRP record, last | N11-A8-50 | 18 | `backlog-adp.service.srp.last.if1` | 28.25 | 10.25 |
| a response with 7 frames owed ahead of it | N11-A8-50 | 20 | `backlog.owed.if0` | 66.26 | 46.26 |
| an ACMP command behind the owed input | N11-A8-50 | 20 | `backlog.owed_behind0.if0` | at least 360.78 | unbounded |
| AECP record, last, in the owed window | N11-B8-100 | 20 | `backlog-owed.service.aecp.last.if1` | 64.94 | 44.94 |
| a response with 7 frames owed ahead of it | N11-B8-100 | 20 | `backlog.owed.if0` | 63.64 | 43.64 |
| an ACMP command behind the owed input | N11-B8-100 | 20 | `backlog.owed_behind0.if0` | at least 360.49 | unbounded |
| AECP record, last | N11-B8-50 | 20 | `backlog-adp.service.aecp.last.if1` | 25.61 | 5.61 |
| AECP record, last, in the owed window | N11-B8-50 | 20 | `backlog-owed.service.aecp.last.if1` | 68.46 | 48.46 |
| SRP record, last | N11-B8-50 | 18 | `backlog-adp.service.srp.last.if1` | 27.25 | 9.25 |
| a response with 7 frames owed ahead of it | N11-B8-50 | 20 | `backlog.owed.if0` | 66.20 | 46.20 |
| an ACMP command behind the owed input | N11-B8-50 | 20 | `backlog.owed_behind0.if0` | at least 360.92 | unbounded |

| 8x8: leg | CPU clock | Share, CPU cycles | Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Over by, ms | Its largest modules, CPU cycles |
|---|---|---:|---|---:|---:|---:|---:|---|
| D11-A8-100 | 100 MHz | 200,000 | backlog | 304 | 1 | 220,017 (2.200) | 0.200 | ctrl_mem 52,019, acmp 37,253, mrp_mad 32,868, srp_mbx 21,503 |
| D11-A8-100 | 100 MHz | 200,000 | backlog-adp | 328 | 0 | 194,299 (1.943) | - | acmp 45,301, ctrl_mem 40,030, mrp_mad 28,518, srp_mbx 17,756 |
| D11-A8-100 | 100 MHz | 200,000 | backlog-adp-refill | 337 | 0 | 174,835 (1.748) | - | ctrl_mem 35,842, acmp 33,910, mrp_mad 28,332, srp_mbx 17,700 |
| D11-A8-100 | 100 MHz | 200,000 | backlog-owed | 363 | 0 | 189,781 (1.898) | - | ctrl_mem 39,069, acmp 35,609, mrp_mad 28,378, srp_mbx 18,357 |
| D11-A8-50 | 50 MHz | 100,000 | backlog | 301 | 6 | 164,096 (3.282) | 1.282 | ctrl_mem 39,856, acmp 33,129, mrp_mad 18,874, srp_mbx 13,101 |
| D11-A8-50 | 50 MHz | 100,000 | backlog-adp | 320 | 6 | 151,157 (3.023) | 1.023 | ctrl_mem 34,473, acmp 32,291, mrp_mad 19,776, srp_mbx 13,659 |
| D11-A8-50 | 50 MHz | 100,000 | backlog-adp-refill | 327 | 6 | 151,157 (3.023) | 1.023 | ctrl_mem 34,473, acmp 32,291, mrp_mad 19,776, srp_mbx 13,659 |
| D11-A8-50 | 50 MHz | 100,000 | backlog-owed | 359 | 6 | 150,069 (3.001) | 1.001 | ctrl_mem 35,016, acmp 32,648, mrp_mad 19,756, srp_mbx 13,647 |
| D11-B8-100 | 100 MHz | 200,000 | backlog | 304 | 1 | 220,440 (2.204) | 0.204 | ctrl_mem 51,533, acmp 37,251, mrp_mad 34,241, srp_mbx 21,357 |
| D11-B8-100 | 100 MHz | 200,000 | backlog-adp | 314 | 0 | 180,366 (1.804) | - | ctrl_mem 38,127, acmp 34,212, mrp_mad 27,684, srp_mbx 16,575 |
| D11-B8-100 | 100 MHz | 200,000 | backlog-adp-refill | 318 | 0 | 180,366 (1.804) | - | ctrl_mem 38,127, acmp 34,212, mrp_mad 27,684, srp_mbx 16,575 |
| D11-B8-100 | 100 MHz | 200,000 | backlog-owed | 362 | 0 | 190,337 (1.903) | - | ctrl_mem 39,106, acmp 35,513, mrp_mad 28,443, srp_mbx 18,427 |
| D11-B8-50 | 50 MHz | 100,000 | backlog | 301 | 6 | 164,764 (3.295) | 1.295 | ctrl_mem 39,799, acmp 33,208, mrp_mad 19,573, srp_mbx 13,218 |
| D11-B8-50 | 50 MHz | 100,000 | backlog-adp | 311 | 6 | 150,199 (3.004) | 1.004 | ctrl_mem 34,476, acmp 32,142, mrp_mad 19,475, srp_mbx 13,781 |
| D11-B8-50 | 50 MHz | 100,000 | backlog-adp-refill | 314 | 6 | 150,199 (3.004) | 1.004 | ctrl_mem 34,476, acmp 32,142, mrp_mad 19,475, srp_mbx 13,781 |
| D11-B8-50 | 50 MHz | 100,000 | backlog-owed | 359 | 5 | 150,389 (3.008) | 1.008 | ctrl_mem 34,983, acmp 32,698, mrp_mad 19,798, srp_mbx 13,762 |
| N11-A8-100 | 100 MHz | 200,000 | backlog | 300 | 1 | 228,766 (2.288) | 0.288 | ctrl_mem 52,412, acmp 38,369, mrp_mad 31,570, srp_mbx 22,133 |
| N11-A8-100 | 100 MHz | 200,000 | backlog-adp | 322 | 0 | 184,481 (1.845) | - | acmp 47,078, ctrl_mem 31,378, mrp_mad 22,708, srp_mbx 15,664 |
| N11-A8-100 | 100 MHz | 200,000 | backlog-adp-refill | 331 | 0 | 167,403 (1.674) | - | acmp 35,670, ctrl_mem 29,948, mrp_mad 18,010, mbx 16,612 |
| N11-A8-100 | 100 MHz | 200,000 | backlog-owed | 358 | 0 | 197,674 (1.977) | - | ctrl_mem 39,818, acmp 36,792, mrp_mad 28,032, srp_mbx 18,423 |
| N11-A8-50 | 50 MHz | 100,000 | backlog | 302 | 6 | 172,758 (3.455) | 1.455 | ctrl_mem 39,443, acmp 34,805, mrp_mad 17,320, srp_mbx 13,711 |
| N11-A8-50 | 50 MHz | 100,000 | backlog-adp | 323 | 9 | 160,502 (3.210) | 1.210 | ctrl_mem 34,852, acmp 33,759, mrp_mad 19,291, srp_mbx 13,736 |
| N11-A8-50 | 50 MHz | 100,000 | backlog-adp-refill | 327 | 9 | 160,502 (3.210) | 1.210 | ctrl_mem 34,852, acmp 33,759, mrp_mad 19,291, srp_mbx 13,736 |
| N11-A8-50 | 50 MHz | 100,000 | backlog-owed | 358 | 8 | 158,290 (3.166) | 1.166 | ctrl_mem 35,429, acmp 33,838, mrp_mad 19,364, srp_mbx 13,766 |
| N11-B8-100 | 100 MHz | 200,000 | backlog | 300 | 2 | 230,298 (2.303) | 0.303 | ctrl_mem 52,596, acmp 38,652, mrp_mad 32,442, srp_mbx 21,418 |
| N11-B8-100 | 100 MHz | 200,000 | backlog-adp | 310 | 0 | 190,427 (1.904) | - | ctrl_mem 38,730, acmp 35,501, mrp_mad 28,401, mbx 16,677 |
| N11-B8-100 | 100 MHz | 200,000 | backlog-adp-refill | 316 | 0 | 190,427 (1.904) | - | ctrl_mem 38,730, acmp 35,501, mrp_mad 28,401, mbx 16,677 |
| N11-B8-100 | 100 MHz | 200,000 | backlog-owed | 358 | 0 | 198,166 (1.982) | - | ctrl_mem 39,700, acmp 36,576, mrp_mad 28,845, srp_mbx 18,423 |
| N11-B8-50 | 50 MHz | 100,000 | backlog | 302 | 6 | 173,282 (3.466) | 1.466 | ctrl_mem 39,673, acmp 34,644, mrp_mad 17,964, srp_mbx 13,287 |
| N11-B8-50 | 50 MHz | 100,000 | backlog-adp | 311 | 8 | 160,133 (3.203) | 1.203 | ctrl_mem 34,965, acmp 33,596, mrp_mad 19,642, srp_mbx 13,737 |
| N11-B8-50 | 50 MHz | 100,000 | backlog-adp-refill | 315 | 8 | 160,133 (3.203) | 1.203 | ctrl_mem 34,965, acmp 33,596, mrp_mad 19,642, srp_mbx 13,737 |
| N11-B8-50 | 50 MHz | 100,000 | backlog-owed | 358 | 8 | 158,772 (3.175) | 1.175 | ctrl_mem 35,482, acmp 33,756, mrp_mad 19,919, srp_mbx 13,766 |
