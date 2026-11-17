### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 16 paths and 7 of 117 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.027 (0.267) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.081 (0.249) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.106 (0.440) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-0.adp_available.if0` (backlog-adp@verify-0) | 3.822 (5.236) | fits | 7 adp | 9 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.896 (63.199) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.643 (63.944) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 3.371 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.995 | MISS ceiling | 11 acmp | 10 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 3.362 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.adp.last.if0` (backlog-adp@verify-0) | 4.322 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 1.900 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.730 | MISS ceiling | 15 aecp | 10 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 3.397 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 4.359 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.srp.first.if0` (backlog-adp@verify-0) | 5.202 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.srp.last.if0` (backlog-adp@verify-0) | 10.276 | fits | 31 srp | 10 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-2 | 0 | 11.318 | 11 | 152,674 (1.527) | yes | - |
| backlog-adp@program-0 | 0 | 11.287 | 11 | 152,873 (1.529) | yes | - |
| backlog-adp@verify-0 | 0 | 11.572 | 11 | 153,477 (1.535) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 11.475 | 12 | 148,420 (1.484) | yes | - |
| backlog-adp@blank-aged1-0 | 1 | 12.038 | 13 | 150,972 (1.510) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.362 | 13 | 152,396 (1.524) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.888 | 14 | 152,184 (1.522) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.233 | 12 | 152,485 (1.525) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.441 | 12 | 152,433 (1.524) | yes | - |
| backlog-owed | 0 | 64.293 | 26 | 148,437 (1.484) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 148,437 CPU cycles (1.484 ms), backlog-owed.
Over the windows that released their whole load only: 148,437 (1.484 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-2 | 416 | 0 | 152,674 (1.527) | fits |
| backlog-adp@program-0 | 519 | 0 | 152,873 (1.529) | fits |
| backlog-adp@verify-0 | 614 | 0 | 153,477 (1.535) | fits |
| backlog-adp@blank-aged2-0 | 699 | 0 | 148,420 (1.484) | fits |
| backlog-adp@blank-aged1-0 | 642 | 0 | 152,191 (1.522) | fits |
| backlog-adp@program-aged2-0 | 798 | 0 | 152,396 (1.524) | fits |
| backlog-adp@program-aged1-0 | 741 | 0 | 152,184 (1.522) | fits |
| backlog-adp@verify-aged2-0 | 894 | 0 | 152,485 (1.525) | fits |
| backlog-adp@verify-aged1-0 | 836 | 0 | 152,433 (1.524) | fits |
| adp-advertise | 598 | 0 | 30,145 (0.301) | fits |
| backlog-owed | 311 | 0 | 148,437 (1.484) | fits |
| datapath-events | 116 | 0 | 30,145 (0.301) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.905 ms, 76,864 (0.769 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.868 (20) | 10.132 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.816 (20) | 10.184 |
| backlog-adp@program-aged2-0 | 2 | none | +10.215 ms, 80,610 (0.806 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.833 (20) | 10.167 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.899 (20) | 10.101 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.124 ms, 77,326 (0.773 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.882 (20) | 10.118 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.023 (20) | 9.977 |

Least margin over the aged windows: 9.977 ms, `backlog-adp@verify-aged1-0.service.srp.last.if0` at 10.023 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-2 | 299 | 92,767 (0.928) | 76,221 (0.762) |
| backlog-adp@program-0 | 328 | 97,007 (0.970) | 78,878 (0.789) |
| backlog-adp@verify-0 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@blank-aged2-0 | 297 | 76,864 (0.769) | 75,765 (0.758) |
| backlog-adp@blank-aged1-0 | 297 | 97,171 (0.972) | 76,108 (0.761) |
| backlog-adp@program-aged2-0 | 326 | 96,381 (0.964) | 78,324 (0.783) |
| backlog-adp@program-aged1-0 | 326 | 96,381 (0.964) | 78,619 (0.786) |
| backlog-adp@verify-aged2-0 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-aged1-0 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| adp-advertise | 577 | 22,268 (0.223) | 2,242 (0.022) |
| backlog-owed | 276 | 22,268 (0.223) | 2,358 (0.024) |
| datapath-events | 69 | 22,142 (0.221) | 2,242 (0.022) |

Longest pass that carries a step: 97,171 CPU cycles (0.972 ms), backlog-adp@blank-aged1-0; longest step: 78,878 (0.789 ms), backlog-adp@program-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 345,149 | 3.451 | 20 | 20 | fits | 97,327 | 151 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 310,768 | 3.108 | 20 | 200 | fits | 150,878 | 237 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 407,479 | 4.075 | 20 | 200 | fits | 97,327 | 151 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 311,692 | 3.117 | 20 | 20 | fits | 150,878 | 237 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 408,183 | 4.082 | 20 | 20 | fits | 97,327 | 151 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 164,454 | 1.645 | 20 | 24 | fits | 152,674 | 155 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 314,342 | 3.143 | 20 | 24 | fits | 150,878 | 237 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 314,276 | 3.143 | 20 | 50 | fits | 150,878 | 237 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 411,207 | 4.112 | 20 | 50 | fits | 97,327 | 151 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 499,828 | 4.998 | 20 | 20 | fits | 88,687 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,002,912 | 10.029 | 20 | 20 | fits | 72,767 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 353,070 | 3.531 | 20 | 20 | fits | 96,803 | 152 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 307,074 | 3.071 | 20 | 200 | fits | 150,470 | 237 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 403,261 | 4.033 | 20 | 200 | fits | 96,803 | 152 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 307,998 | 3.080 | 20 | 20 | fits | 150,470 | 237 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 403,965 | 4.040 | 20 | 20 | fits | 96,803 | 152 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 161,168 | 1.612 | 20 | 24 | fits | 152,873 | 155 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 310,648 | 3.106 | 20 | 24 | fits | 150,470 | 237 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 310,582 | 3.106 | 20 | 50 | fits | 150,470 | 237 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 406,989 | 4.070 | 20 | 50 | fits | 96,803 | 152 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 502,801 | 5.028 | 20 | 20 | fits | 86,881 | 31 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 994,374 | 9.944 | 20 | 20 | fits | 66,326 | 26 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 382,168 | 3.822 | 20 | 20 | fits | 96,648 | 151 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 336,152 | 3.362 | 20 | 200 | fits | 150,704 | 237 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 432,184 | 4.322 | 20 | 200 | fits | 96,648 | 151 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 337,076 | 3.371 | 20 | 20 | fits | 150,704 | 237 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 432,888 | 4.329 | 20 | 20 | fits | 96,648 | 151 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 190,012 | 1.900 | 20 | 24 | fits | 153,477 | 155 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 339,726 | 3.397 | 20 | 24 | fits | 150,704 | 237 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 339,660 | 3.397 | 20 | 50 | fits | 150,704 | 237 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 435,912 | 4.359 | 20 | 50 | fits | 96,648 | 151 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 520,213 | 5.202 | 20 | 20 | fits | 84,367 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,027,581 | 10.276 | 20 | 20 | fits | 78,826 | 30 | 0.699 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 358,973 | 3.590 | 20 | 20 | fits | 115,735 | 199 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 283,481 | 2.835 | 20 | 200 | fits | 148,420 | 216 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 407,962 | 4.080 | 20 | 200 | fits | 115,735 | 199 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 284,405 | 2.844 | 20 | 20 | fits | 148,420 | 216 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 408,666 | 4.087 | 20 | 20 | fits | 115,735 | 199 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 139,625 | 1.396 | 20 | 24 | fits | 145,421 | 147 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 287,055 | 2.871 | 20 | 24 | fits | 148,420 | 216 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 286,989 | 2.870 | 20 | 50 | fits | 148,420 | 216 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 411,690 | 4.117 | 20 | 50 | fits | 115,735 | 199 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 495,173 | 4.952 | 20 | 20 | fits | 83,549 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 986,755 | 9.868 | 20 | 20 | fits | 66,373 | 26 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 344,416 | 3.444 | 20 | 20 | fits | 97,325 | 154 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 296,494 | 2.965 | 20 | 200 | fits | 150,972 | 238 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 393,203 | 3.932 | 20 | 200 | fits | 97,325 | 154 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 297,418 | 2.974 | 20 | 20 | fits | 150,972 | 238 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 393,907 | 3.939 | 20 | 20 | fits | 97,325 | 154 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 150,086 | 1.501 | 20 | 24 | fits | 152,191 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 300,068 | 3.001 | 20 | 24 | fits | 150,972 | 238 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 300,002 | 3.000 | 20 | 50 | fits | 150,972 | 238 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 396,931 | 3.969 | 20 | 50 | fits | 97,325 | 154 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 481,322 | 4.813 | 20 | 20 | fits | 84,457 | 25 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 981,582 | 9.816 | 20 | 20 | fits | 72,807 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 353,561 | 3.536 | 20 | 20 | fits | 99,062 | 142 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 311,185 | 3.112 | 20 | 200 | fits | 150,232 | 253 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 409,631 | 4.096 | 20 | 200 | fits | 99,062 | 142 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 312,109 | 3.121 | 20 | 20 | fits | 150,232 | 253 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 410,335 | 4.103 | 20 | 20 | fits | 99,062 | 142 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 157,646 | 1.576 | 20 | 24 | fits | 152,396 | 153 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 314,759 | 3.148 | 20 | 24 | fits | 150,232 | 253 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 314,693 | 3.147 | 20 | 50 | fits | 150,232 | 253 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 413,359 | 4.134 | 20 | 50 | fits | 99,062 | 142 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 497,247 | 4.972 | 20 | 20 | fits | 83,954 | 24 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 983,272 | 9.833 | 20 | 20 | fits | 60,026 | 21 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 367,027 | 3.670 | 20 | 20 | fits | 100,593 | 158 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 308,915 | 3.089 | 20 | 200 | fits | 150,875 | 238 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 417,521 | 4.175 | 20 | 200 | fits | 100,593 | 158 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 309,839 | 3.098 | 20 | 20 | fits | 150,875 | 238 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 418,225 | 4.182 | 20 | 20 | fits | 100,593 | 158 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 162,604 | 1.626 | 20 | 24 | fits | 152,184 | 152 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 312,489 | 3.125 | 20 | 24 | fits | 150,875 | 238 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 312,423 | 3.124 | 20 | 50 | fits | 150,875 | 238 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 421,249 | 4.212 | 20 | 50 | fits | 100,593 | 158 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 504,912 | 5.049 | 20 | 20 | fits | 83,729 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 989,935 | 9.899 | 20 | 20 | fits | 59,783 | 20 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 348,937 | 3.489 | 20 | 20 | fits | 96,490 | 151 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 302,941 | 3.029 | 20 | 200 | fits | 150,660 | 237 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 398,815 | 3.988 | 20 | 200 | fits | 96,490 | 151 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 303,865 | 3.039 | 20 | 20 | fits | 150,660 | 237 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 399,519 | 3.995 | 20 | 20 | fits | 96,490 | 151 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 156,845 | 1.568 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 306,515 | 3.065 | 20 | 24 | fits | 150,660 | 237 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 306,449 | 3.064 | 20 | 50 | fits | 150,660 | 237 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 402,543 | 4.025 | 20 | 50 | fits | 96,490 | 151 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 486,844 | 4.868 | 20 | 20 | fits | 84,367 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 988,222 | 9.882 | 20 | 20 | fits | 72,898 | 24 | 0.656 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 348,806 | 3.488 | 20 | 20 | fits | 104,338 | 160 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 314,640 | 3.146 | 20 | 200 | fits | 146,459 | 235 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 418,362 | 4.184 | 20 | 200 | fits | 104,338 | 160 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 315,564 | 3.156 | 20 | 20 | fits | 146,459 | 235 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 419,066 | 4.191 | 20 | 20 | fits | 104,338 | 160 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 164,808 | 1.648 | 20 | 24 | fits | 152,433 | 153 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 318,214 | 3.182 | 20 | 24 | fits | 146,459 | 235 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 318,148 | 3.181 | 20 | 50 | fits | 146,459 | 235 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 422,090 | 4.221 | 20 | 50 | fits | 104,338 | 160 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 506,348 | 5.063 | 20 | 20 | fits | 84,324 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,002,265 | 10.023 | 20 | 20 | fits | 69,855 | 33 | 0.735 |
| LINK_UP | `adp.link_up.if0` | 2,674 | 0.027 | 20 | 200 | fits | 26,711 | 43 (11) | 0.737 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,642 | 0.106 | 20 | 200 | fits | 23,487 | 23 (39) | 0.762 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 8,085 | 0.081 | 20 | 200 | fits | 2,794 | 10 (11) | 0.613 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,289,573 | 62.896 | 20 | 20 | MISS ceiling | 18,929 | 14 | 0.659 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,308,368 | 63.084 | 20 | 20 | MISS ceiling | 18,823 | 13 | 0.643 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,327,118 | 63.271 | 20 | 20 | MISS ceiling | 18,778 | 13 | 0.639 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,345,751 | 63.458 | 20 | 20 | MISS ceiling | 18,709 | 13 | 0.646 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,364,305 | 63.643 | 20 | 20 | MISS ceiling | 18,543 | 13 | 0.658 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 161,186 | 1.612 | 20 | 200 | fits | 148,437 | 204 | 0.442 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 246,138 | 2.461 | 20 | 200 | fits | 85,568 | 179 | 0.361 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 156,864 | 1.569 | 20 | 20 | fits | 148,437 | 204 | 0.442 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,199,512 | 61.995 | 20 | 20 | MISS ceiling | 29,973 | 15 | 0.777 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 160,504 | 1.605 | 20 | 24 | fits | 148,437 | 204 | 0.442 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,173,025 | 61.730 | 20 | 24 | MISS ceiling | 140,830 | 106 | 0.434 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 159,448 | 1.594 | 20 | 50 | fits | 148,437 | 204 | 0.442 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 244,620 | 2.446 | 20 | 50 | fits | 85,568 | 179 | 0.361 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 328,223 | 3.282 | 20 | 20 | fits | 83,669 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 826,269 | 8.263 | 20 | 20 | fits | 73,987 | 24 | 0.668 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
