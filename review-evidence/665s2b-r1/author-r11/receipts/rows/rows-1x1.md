Share: 18 ms over 9 passes, 2.000 ms of CPU time.
Legs: D11-A1-100, D11-A1-50, D11-A8-100, D11-A8-50, D11-B1-100, D11-B1-50, D11-B8-100, D11-B8-50, N11-A1-100, N11-A1-50, N11-A8-100, N11-A8-50, N11-B1-100, N11-B1-50, N11-B8-100, N11-B8-50.

| 1x1: row | Bound, ms | CPU 50 MHz (product) | CPU 50 MHz (product), with both drafts | CPU 100 MHz (labelled option) | CPU 100 MHz (labelled option), with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.85 / 1.84 | 1.66 / 1.67 | 1.10 / 1.09 | 1.00 / 1.01 |
| ACMP record, last | 20 | 8.65 / 8.90 | 7.64 / 7.46 | 5.51 / 5.30 | 4.60 / 4.76 |
| ADP record, first | 20 | 1.89 / 1.89 | 1.71 / 1.72 | 1.14 / 1.14 | 1.04 / 1.05 |
| ADP record, last | 20 | 6.08 / 6.38 | 5.51 / 5.36 | 3.93 / 3.77 | 3.28 / 3.41 |
| AECP record, first | 20 | 1.89 / 1.88 | 1.70 / 1.71 | 1.13 / 1.13 | 1.04 / 1.05 |
| AECP record, first, in the owed window | 20 | 1.29 / 1.35 | 1.18 / 1.13 | 0.76 / 0.77 | 0.66 / 0.67 |
| AECP record, last | 20 | 15.95 / 17.05 | 14.87 / 15.76 | 10.25 / 10.43 | 9.36 / 9.98 |
| AECP record, last, in the owed window | 20 | **64.73** / **64.67** | **64.66** / **64.65** | **62.81** / **62.90** | **62.84** / **62.83** |
| MAAP record, first | 20 | 1.88 / 1.87 | 1.69 / 1.70 | 1.12 / 1.12 | 1.03 / 1.04 |
| MAAP record, last | 20 | 6.11 / 6.42 | 5.50 / 5.34 | 3.97 / 3.81 | 3.26 / 3.44 |
| SRP record, first | 18 | 4.39 / 4.31 | 3.36 / 3.40 | 2.22 / 2.21 | 2.05 / 2.09 |
| SRP record, last | 18 | 17.81 / 17.02 | 16.34 / 16.26 | 10.53 / 10.40 | 9.97 / 10.19 |
| a response with 7 frames owed ahead of it | 20 | **63.41** / **63.33** | **63.35** / **63.33** | **61.99** / **62.06** | **62.01** / **62.00** |
| an ACMP command behind a full acmp ring | 20 | 6.83 / 6.78 | 6.01 / 6.09 | 4.07 / 4.04 | 3.64 / 3.70 |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 4.55 / 4.88 | 4.38 / 4.26 | 3.02 / 2.87 | 2.58 / 2.60 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.17 / 0.09 | 0.09 / 0.08 | 0.06 / 0.10 | 0.13 / 0.12 |
| an event behind 15 others | 20 | 2.06 / 2.06 | 1.88 / 1.89 | 1.24 / 1.23 | 1.14 / 1.15 |

| 1x1: row over its bound | Leg | Bound, ms | Worst instance | ms | Over by, ms |
|---|---|---:|---|---:|---:|
| AECP record, last, in the owed window | D11-A1-100 | 20 | `backlog-owed.service.aecp.last.if0` | 62.84 | 42.84 |
| a response with 7 frames owed ahead of it | D11-A1-100 | 20 | `backlog.owed.if0` | 62.01 | 42.01 |
| an ACMP command behind the owed input | D11-A1-100 | 20 | `backlog.owed_behind0.if0` | at least 360.21 | unbounded |
| AECP record, last, in the owed window | D11-A1-50 | 20 | `backlog-owed.service.aecp.last.if0` | 64.66 | 44.66 |
| a response with 7 frames owed ahead of it | D11-A1-50 | 20 | `backlog.owed.if0` | 63.35 | 43.35 |
| an ACMP command behind the owed input | D11-A1-50 | 20 | `backlog.owed_behind0.if0` | at least 360.29 | unbounded |
| AECP record, last, in the owed window | D11-B1-100 | 20 | `backlog-owed.service.aecp.last.if0` | 62.83 | 42.83 |
| a response with 7 frames owed ahead of it | D11-B1-100 | 20 | `backlog.owed.if0` | 62.00 | 42.00 |
| an ACMP command behind the owed input | D11-B1-100 | 20 | `backlog.owed_behind0.if0` | at least 360.20 | unbounded |
| AECP record, last, in the owed window | D11-B1-50 | 20 | `backlog-owed.service.aecp.last.if0` | 64.65 | 44.65 |
| a response with 7 frames owed ahead of it | D11-B1-50 | 20 | `backlog.owed.if0` | 63.33 | 43.33 |
| an ACMP command behind the owed input | D11-B1-50 | 20 | `backlog.owed_behind0.if0` | at least 360.38 | unbounded |
| AECP record, last, in the owed window | N11-A1-100 | 20 | `backlog-owed.service.aecp.last.if0` | 62.81 | 42.81 |
| a response with 7 frames owed ahead of it | N11-A1-100 | 20 | `backlog.owed.if0` | 61.99 | 41.99 |
| an ACMP command behind the owed input | N11-A1-100 | 20 | `backlog.owed_behind0.if0` | at least 360.16 | unbounded |
| AECP record, last, in the owed window | N11-A1-50 | 20 | `backlog-owed.service.aecp.last.if0` | 64.73 | 44.73 |
| a response with 7 frames owed ahead of it | N11-A1-50 | 20 | `backlog.owed.if0` | 63.41 | 43.41 |
| an ACMP command behind the owed input | N11-A1-50 | 20 | `backlog.owed_behind0.if0` | at least 360.36 | unbounded |
| AECP record, last, in the owed window | N11-B1-100 | 20 | `backlog-owed.service.aecp.last.if0` | 62.90 | 42.90 |
| a response with 7 frames owed ahead of it | N11-B1-100 | 20 | `backlog.owed.if0` | 62.06 | 42.06 |
| an ACMP command behind the owed input | N11-B1-100 | 20 | `backlog.owed_behind0.if0` | at least 360.21 | unbounded |
| AECP record, last, in the owed window | N11-B1-50 | 20 | `backlog-owed.service.aecp.last.if0` | 64.67 | 44.67 |
| a response with 7 frames owed ahead of it | N11-B1-50 | 20 | `backlog.owed.if0` | 63.33 | 43.33 |
| an ACMP command behind the owed input | N11-B1-50 | 20 | `backlog.owed_behind0.if0` | at least 360.41 | unbounded |

| 1x1: leg | CPU clock | Share, CPU cycles | Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Over by, ms | Its largest modules, CPU cycles |
|---|---|---:|---|---:|---:|---:|---:|---|
| D11-A1-100 | 100 MHz | 200,000 | backlog | 291 | 0 | 104,480 (1.045) | - | ctrl_mem 20,061, mbx 15,728, acmp 15,666, mrp_mad 11,853 |
| D11-A1-100 | 100 MHz | 200,000 | backlog-adp | 311 | 0 | 103,816 (1.038) | - | ctrl_mem 16,137, mbx 15,808, acmp 14,560, mrp_mad 13,488 |
| D11-A1-100 | 100 MHz | 200,000 | backlog-adp-refill | 322 | 0 | 103,816 (1.038) | - | ctrl_mem 16,137, mbx 15,808, acmp 14,560, mrp_mad 13,488 |
| D11-A1-100 | 100 MHz | 200,000 | backlog-owed | 349 | 0 | 102,306 (1.023) | - | ctrl_mem 16,755, acmp 14,564, mbx 14,310, mrp_mad 13,599 |
| D11-A1-50 | 50 MHz | 100,000 | backlog | 292 | 0 | 85,384 (1.708) | - | ctrl_mem 17,342, acmp 13,480, mbx 12,432, mrp_mad 8,946 |
| D11-A1-50 | 50 MHz | 100,000 | backlog-adp | 309 | 0 | 83,962 (1.679) | - | ctrl_mem 14,098, acmp 13,116, mbx 12,707, mrp_mad 9,294 |
| D11-A1-50 | 50 MHz | 100,000 | backlog-adp-refill | 316 | 0 | 83,962 (1.679) | - | ctrl_mem 14,098, acmp 13,116, mbx 12,707, mrp_mad 9,294 |
| D11-A1-50 | 50 MHz | 100,000 | backlog-owed | 347 | 0 | 82,933 (1.659) | - | ctrl_mem 14,677, acmp 12,904, mbx 11,724, mrp_mad 9,355 |
| D11-B1-100 | 100 MHz | 200,000 | backlog | 291 | 0 | 105,646 (1.056) | - | ctrl_mem 20,958, mbx 16,186, acmp 15,477, mrp_mad 11,687 |
| D11-B1-100 | 100 MHz | 200,000 | backlog-adp | 301 | 0 | 104,083 (1.041) | - | mbx 17,046, ctrl_mem 15,937, acmp 14,636, mrp_mad 13,336 |
| D11-B1-100 | 100 MHz | 200,000 | backlog-adp-refill | 308 | 0 | 104,083 (1.041) | - | mbx 17,046, ctrl_mem 15,937, acmp 14,636, mrp_mad 13,336 |
| D11-B1-100 | 100 MHz | 200,000 | backlog-owed | 349 | 0 | 102,817 (1.028) | - | ctrl_mem 16,603, mbx 15,414, acmp 14,633, mrp_mad 13,659 |
| D11-B1-50 | 50 MHz | 100,000 | backlog | 291 | 0 | 85,875 (1.718) | - | ctrl_mem 17,880, acmp 13,270, mbx 12,719, mrp_mad 8,739 |
| D11-B1-50 | 50 MHz | 100,000 | backlog-adp | 301 | 0 | 84,199 (1.684) | - | ctrl_mem 14,088, mbx 13,461, acmp 13,141, mrp_mad 9,242 |
| D11-B1-50 | 50 MHz | 100,000 | backlog-adp-refill | 306 | 0 | 84,199 (1.684) | - | ctrl_mem 14,088, mbx 13,461, acmp 13,141, mrp_mad 9,242 |
| D11-B1-50 | 50 MHz | 100,000 | backlog-owed | 348 | 0 | 75,366 (1.507) | - | acmp 12,893, ctrl_mem 12,601, mbx 11,589, mrp_mad 7,493 |
| N11-A1-100 | 100 MHz | 200,000 | backlog | 291 | 0 | 114,107 (1.141) | - | ctrl_mem 20,051, acmp 17,443, mbx 16,584, mrp_mad 11,787 |
| N11-A1-100 | 100 MHz | 200,000 | backlog-adp | 310 | 0 | 113,923 (1.139) | - | mbx 17,447, acmp 17,159, ctrl_mem 15,577, mrp_mad 12,220 |
| N11-A1-100 | 100 MHz | 200,000 | backlog-adp-refill | 321 | 0 | 113,923 (1.139) | - | mbx 17,447, acmp 17,159, ctrl_mem 15,577, mrp_mad 12,220 |
| N11-A1-100 | 100 MHz | 200,000 | backlog-owed | 350 | 0 | 110,518 (1.105) | - | acmp 16,826, ctrl_mem 16,229, mbx 15,590, mrp_mad 12,653 |
| N11-A1-50 | 50 MHz | 100,000 | backlog | 291 | 0 | 94,732 (1.895) | - | ctrl_mem 17,461, acmp 14,979, mbx 13,052, mrp_mad 8,826 |
| N11-A1-50 | 50 MHz | 100,000 | backlog-adp | 314 | 0 | 86,029 (1.721) | - | acmp 20,085, ctrl_mem 11,608, mbx 10,688, rt_lshrdi3 6,694 |
| N11-A1-50 | 50 MHz | 100,000 | backlog-adp-refill | 320 | 0 | 81,294 (1.626) | - | acmp 15,613, mbx 11,490, ctrl_mem 11,175, rt_lshrdi3 7,096 |
| N11-A1-50 | 50 MHz | 100,000 | backlog-owed | 348 | 0 | 86,613 (1.732) | - | acmp 14,687, ctrl_mem 13,668, mbx 10,694, mrp_mad 8,759 |
| N11-B1-100 | 100 MHz | 200,000 | backlog | 291 | 0 | 113,895 (1.139) | - | ctrl_mem 20,397, acmp 17,233, mbx 16,129, mrp_mad 11,472 |
| N11-B1-100 | 100 MHz | 200,000 | backlog-adp | 300 | 0 | 112,649 (1.126) | - | acmp 16,916, mbx 16,642, ctrl_mem 15,367, mrp_mad 12,313 |
| N11-B1-100 | 100 MHz | 200,000 | backlog-adp-refill | 307 | 0 | 112,649 (1.126) | - | acmp 16,916, mbx 16,642, ctrl_mem 15,367, mrp_mad 12,313 |
| N11-B1-100 | 100 MHz | 200,000 | backlog-owed | 350 | 0 | 110,059 (1.101) | - | acmp 16,614, ctrl_mem 16,006, mbx 15,025, mrp_mad 12,605 |
| N11-B1-50 | 50 MHz | 100,000 | backlog | 292 | 0 | 94,463 (1.889) | - | ctrl_mem 17,647, acmp 14,936, mbx 12,721, mrp_mad 8,659 |
| N11-B1-50 | 50 MHz | 100,000 | backlog-adp | 300 | 0 | 92,382 (1.848) | - | acmp 15,215, ctrl_mem 13,857, mbx 13,182, mrp_mad 8,417 |
| N11-B1-50 | 50 MHz | 100,000 | backlog-adp-refill | 305 | 0 | 92,382 (1.848) | - | acmp 15,215, ctrl_mem 13,857, mbx 13,182, mrp_mad 8,417 |
| N11-B1-50 | 50 MHz | 100,000 | backlog-owed | 348 | 0 | 85,996 (1.720) | - | acmp 14,612, ctrl_mem 13,577, mbx 10,432, mrp_mad 8,598 |
