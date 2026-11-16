### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 20 paths and 0 of 231 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.139 (0.605) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.048 (0.191) | fits | 0 adp | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-discover) | 0.027 (0.307) | fits | 0 events | 2 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-discover) | 0.174 (0.521) | fits | 0 events | 2 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.525 (5.469) | fits | 7 adp | 19 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.202 (0.597) | fits | 0 adp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-7.service.acmp.first.if0` (backlog-adp@verify-aged1-7) | 3.121 | fits | 0 acmp | 20 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.acmp.last.if0` (backlog-adp@program-aged2-7) | 5.329 | fits | 11 acmp | 20 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-7.service.adp.first.if0` (backlog-adp@verify-aged1-7) | 3.111 | fits | 0 adp | 20 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.322 | fits | 7 adp | 20 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-7.service.aecp.first.if0` (backlog-adp@program-7) | 1.605 | fits | 0 aecp | 20 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-7.service.aecp.last.if0` (backlog-adp@verify-aged1-7) | 3.147 | fits | 15 aecp | 20 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-7.service.maap.first.if0` (backlog-adp@verify-aged1-7) | 3.147 | fits | 0 maap | 20 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.359 | fits | 6 maap | 20 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 6.249 | fits | 0 srp | 20 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.srp.last.if0` (backlog-adp@program-aged2-7) | 10.626 | fits | 31 srp | 20 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.710 (1.855) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.525 (0.526) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.235 (0.236) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.458 (1.531) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.121 | 11 | 147,893 (1.479) | yes | - |
| backlog-adp@blank-3 | 0 | 11.034 | 10 | 147,472 (1.475) | yes | - |
| backlog-adp@blank-7 | 0 | 12.409 | 11 | 153,871 (1.539) | yes | - |
| backlog-adp@program-3 | 0 | 11.019 | 10 | 153,659 (1.537) | yes | - |
| backlog-adp@program-7 | 0 | 10.408 | 10 | 147,878 (1.479) | yes | - |
| backlog-adp@verify-3 | 0 | 10.949 | 9 | 147,650 (1.476) | yes | - |
| backlog-adp@verify-7 | 0 | 12.164 | 11 | 155,454 (1.555) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.060 | 10 | 148,026 (1.480) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.606 | 13 | 151,260 (1.513) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.483 | 12 | 148,896 (1.489) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.111 | 10 | 148,849 (1.488) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.978 | 9 | 148,842 (1.488) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 11.452 | 12 | 149,059 (1.491) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.132 | 10 | 147,795 (1.478) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.637 | 12 | 151,077 (1.511) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.973 | 10 | 147,732 (1.477) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.216 | 11 | 155,026 (1.550) | yes | - |
| backlog-adp@verify-aged1-3 | 1 | 10.936 | 9 | 148,617 (1.486) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.315 | 12 | 154,941 (1.549) | yes | - |
| backlog-adp-refill | 0 | 40.943 | 25 | 147,788 (1.478) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-owed not run): 147,788 CPU cycles (1.478 ms), backlog-adp-refill.
Over the windows that released their whole load only: 147,788 (1.478 ms), backlog-adp-refill.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3352 | 0 | 94,822 (0.948) | fits |
| backlog-adp@blank-0 | 537 | 0 | 147,893 (1.479) | fits |
| backlog-adp@blank-3 | 536 | 0 | 147,472 (1.475) | fits |
| backlog-adp@blank-7 | 539 | 0 | 153,871 (1.539) | fits |
| backlog-adp@program-3 | 894 | 0 | 153,659 (1.537) | fits |
| backlog-adp@program-7 | 897 | 0 | 147,878 (1.479) | fits |
| backlog-adp@verify-3 | 1242 | 0 | 147,650 (1.476) | fits |
| backlog-adp@verify-7 | 1245 | 0 | 155,454 (1.555) | fits |
| backlog-adp@blank-aged2-3 | 833 | 0 | 148,026 (1.480) | fits |
| backlog-adp@blank-aged2-7 | 864 | 0 | 151,260 (1.513) | fits |
| backlog-adp@blank-aged1-3 | 778 | 0 | 148,896 (1.489) | fits |
| backlog-adp@blank-aged1-7 | 805 | 0 | 148,849 (1.488) | fits |
| backlog-adp@program-aged2-3 | 1184 | 0 | 148,842 (1.488) | fits |
| backlog-adp@program-aged2-7 | 1215 | 0 | 149,059 (1.491) | fits |
| backlog-adp@program-aged1-3 | 1128 | 0 | 147,795 (1.478) | fits |
| backlog-adp@program-aged1-7 | 1158 | 0 | 151,077 (1.511) | fits |
| backlog-adp@verify-aged2-3 | 1536 | 0 | 147,732 (1.477) | fits |
| backlog-adp@verify-aged2-7 | 1566 | 0 | 155,026 (1.550) | fits |
| backlog-adp@verify-aged1-3 | 1479 | 0 | 148,617 (1.486) | fits |
| backlog-adp@verify-aged1-7 | 1510 | 0 | 154,941 (1.549) | fits |
| srp | 288 | 0 | 139,264 (1.393) | fits |
| backlog-adp-refill | 325 | 0 | 147,788 (1.478) | fits |
| adp-discover | 87 | 0 | 94,822 (0.948) | fits |
| control | 87 | 0 | 94,822 (0.948) | fits |
| datapath-events | 117 | 0 | 94,822 (0.948) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-3 | 2 | +7.145 ms, 75,987 (0.760 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.496 (20) | 9.504 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.414 (20) | 9.586 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.679 (20) | 10.321 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.651 (20) | 10.349 |
| backlog-adp@program-aged2-3 | 2 | +7.065 ms, 80,626 (0.806 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.411 (20) | 9.589 |
| backlog-adp@program-aged2-7 | 2 | +3.077 ms, 80,741 (0.807 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.626 (20) | 9.374 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.756 (20) | 10.244 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.674 (20) | 10.326 |
| backlog-adp@verify-aged2-3 | 2 | +7.206 ms, 77,176 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.404 (20) | 9.596 |
| backlog-adp@verify-aged2-7 | 2 | +3.072 ms, 77,374 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.497 (20) | 9.503 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.603 (20) | 10.397 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.833 (20) | 10.167 |

Least margin over the aged windows: 9.374 ms, `backlog-adp@program-aged2-7.service.srp.last.if0` at 10.626 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 104,785 (1.048) | 78,536 (0.785) |
| backlog-adp@blank-0 | 338 | 92,541 (0.925) | 75,436 (0.754) |
| backlog-adp@blank-3 | 339 | 93,943 (0.939) | 75,712 (0.757) |
| backlog-adp@blank-7 | 340 | 93,366 (0.934) | 75,585 (0.756) |
| backlog-adp@program-3 | 448 | 100,309 (1.003) | 78,216 (0.782) |
| backlog-adp@program-7 | 449 | 100,309 (1.003) | 77,865 (0.779) |
| backlog-adp@verify-3 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-7 | 556 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@blank-aged2-3 | 337 | 77,166 (0.772) | 75,321 (0.753) |
| backlog-adp@blank-aged2-7 | 338 | 91,936 (0.919) | 75,586 (0.756) |
| backlog-adp@blank-aged1-3 | 337 | 93,634 (0.936) | 75,532 (0.755) |
| backlog-adp@blank-aged1-7 | 338 | 93,367 (0.934) | 75,586 (0.756) |
| backlog-adp@program-aged2-3 | 446 | 100,309 (1.003) | 78,038 (0.780) |
| backlog-adp@program-aged2-7 | 447 | 100,309 (1.003) | 78,194 (0.782) |
| backlog-adp@program-aged1-3 | 446 | 100,309 (1.003) | 78,213 (0.782) |
| backlog-adp@program-aged1-7 | 447 | 100,309 (1.003) | 78,302 (0.783) |
| backlog-adp@verify-aged2-3 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged2-7 | 556 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged1-3 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged1-7 | 556 | 104,105 (1.041) | 78,512 (0.785) |
| srp | 271 | 25,967 (0.260) | 2,512 (0.025) |
| backlog-adp-refill | 274 | 25,967 (0.260) | 2,512 (0.025) |
| adp-discover | 79 | 25,733 (0.257) | 2,512 (0.025) |
| control | 79 | 25,733 (0.257) | 2,512 (0.025) |
| datapath-events | 70 | 25,733 (0.257) | 2,512 (0.025) |

Longest pass that carries a step: 104,785 CPU cycles (1.048 ms), acmp-notk; longest step: 78,536 (0.785 ms), acmp-notk.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 13,938 | 0.139 | 20 | 20 | fits | 39,121 | 19 (14) | 0.881 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 355,339 | 3.553 | 20 | 20 | fits | 138,929 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 289,270 | 2.893 | 20 | 200 | fits | 147,893 | 217 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 427,583 | 4.276 | 20 | 200 | fits | 138,929 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 290,194 | 2.902 | 20 | 20 | fits | 147,893 | 217 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 428,287 | 4.283 | 20 | 20 | fits | 138,929 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 145,941 | 1.459 | 20 | 24 | fits | 145,389 | 164 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 292,844 | 2.928 | 20 | 24 | fits | 147,893 | 217 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 292,778 | 2.928 | 20 | 50 | fits | 147,893 | 217 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 431,311 | 4.313 | 20 | 50 | fits | 138,929 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 520,898 | 5.209 | 20 | 20 | fits | 89,653 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 958,874 | 9.589 | 20 | 20 | fits | 67,885 | 24 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 363,998 | 3.640 | 20 | 20 | fits | 139,066 | 164 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 297,348 | 2.973 | 20 | 200 | fits | 147,472 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 435,798 | 4.358 | 20 | 200 | fits | 139,066 | 164 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 298,272 | 2.983 | 20 | 20 | fits | 147,472 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 436,502 | 4.365 | 20 | 20 | fits | 139,066 | 164 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 154,440 | 1.544 | 20 | 24 | fits | 145,582 | 164 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 300,922 | 3.009 | 20 | 24 | fits | 147,472 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 300,856 | 3.009 | 20 | 50 | fits | 147,472 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 439,526 | 4.395 | 20 | 50 | fits | 139,066 | 164 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 541,440 | 5.414 | 20 | 20 | fits | 93,130 | 31 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 970,559 | 9.706 | 20 | 20 | fits | 67,647 | 24 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 384,495 | 3.845 | 20 | 20 | fits | 140,138 | 166 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 306,836 | 3.068 | 20 | 200 | fits | 153,871 | 218 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 446,358 | 4.464 | 20 | 200 | fits | 140,138 | 166 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 307,760 | 3.078 | 20 | 20 | fits | 153,871 | 218 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 447,062 | 4.471 | 20 | 20 | fits | 140,138 | 166 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 157,529 | 1.575 | 20 | 24 | fits | 145,298 | 164 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 310,410 | 3.104 | 20 | 24 | fits | 153,871 | 218 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 310,344 | 3.103 | 20 | 50 | fits | 153,871 | 218 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 450,086 | 4.501 | 20 | 50 | fits | 140,138 | 166 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 539,591 | 5.396 | 20 | 20 | fits | 89,571 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 977,488 | 9.775 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 372,025 | 3.720 | 20 | 20 | fits | 140,130 | 166 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 294,374 | 2.944 | 20 | 200 | fits | 153,659 | 218 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 433,888 | 4.339 | 20 | 200 | fits | 140,130 | 166 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 295,298 | 2.953 | 20 | 20 | fits | 153,659 | 218 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 434,592 | 4.346 | 20 | 20 | fits | 140,130 | 166 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 145,279 | 1.453 | 20 | 24 | fits | 145,298 | 164 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 297,948 | 2.979 | 20 | 24 | fits | 153,659 | 218 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 297,882 | 2.979 | 20 | 50 | fits | 153,659 | 218 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 437,616 | 4.376 | 20 | 50 | fits | 140,130 | 166 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 526,506 | 5.265 | 20 | 20 | fits | 88,956 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 964,490 | 9.645 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 387,145 | 3.871 | 20 | 20 | fits | 147,076 | 185 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 303,776 | 3.038 | 20 | 200 | fits | 147,878 | 200 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 450,236 | 4.502 | 20 | 200 | fits | 147,076 | 185 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 304,700 | 3.047 | 20 | 20 | fits | 147,878 | 200 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 450,940 | 4.509 | 20 | 20 | fits | 147,076 | 185 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 160,462 | 1.605 | 20 | 24 | fits | 145,298 | 164 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 307,350 | 3.074 | 20 | 24 | fits | 147,878 | 200 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 307,284 | 3.073 | 20 | 50 | fits | 147,878 | 200 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 453,964 | 4.540 | 20 | 50 | fits | 147,076 | 185 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 555,059 | 5.551 | 20 | 20 | fits | 92,301 | 31 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 978,439 | 9.784 | 20 | 20 | fits | 67,647 | 24 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 354,126 | 3.541 | 20 | 20 | fits | 139,106 | 164 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 287,975 | 2.880 | 20 | 200 | fits | 147,650 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 426,465 | 4.265 | 20 | 200 | fits | 139,106 | 164 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 288,899 | 2.889 | 20 | 20 | fits | 147,650 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 427,169 | 4.272 | 20 | 20 | fits | 139,106 | 164 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 144,889 | 1.449 | 20 | 24 | fits | 145,450 | 164 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 291,549 | 2.915 | 20 | 24 | fits | 147,650 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 291,483 | 2.915 | 20 | 50 | fits | 147,650 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 430,193 | 4.302 | 20 | 50 | fits | 139,106 | 164 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 532,081 | 5.321 | 20 | 20 | fits | 93,101 | 31 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 961,135 | 9.611 | 20 | 20 | fits | 67,647 | 24 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 365,422 | 3.654 | 20 | 20 | fits | 138,963 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 299,145 | 2.991 | 20 | 200 | fits | 155,454 | 222 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 437,492 | 4.375 | 20 | 200 | fits | 138,963 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 300,069 | 3.001 | 20 | 20 | fits | 155,454 | 222 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 438,196 | 4.382 | 20 | 20 | fits | 138,963 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 148,255 | 1.483 | 20 | 24 | fits | 145,244 | 164 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 302,719 | 3.027 | 20 | 24 | fits | 155,454 | 222 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 302,653 | 3.027 | 20 | 50 | fits | 155,454 | 222 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 441,220 | 4.412 | 20 | 50 | fits | 138,963 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 530,609 | 5.306 | 20 | 20 | fits | 89,455 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 968,470 | 9.685 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 363,678 | 3.637 | 20 | 20 | fits | 138,354 | 163 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 297,502 | 2.975 | 20 | 200 | fits | 148,026 | 217 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 435,240 | 4.352 | 20 | 200 | fits | 138,354 | 163 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 298,426 | 2.984 | 20 | 20 | fits | 148,026 | 217 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 435,944 | 4.359 | 20 | 20 | fits | 138,354 | 163 | 0.416 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 154,040 | 1.540 | 20 | 24 | fits | 144,759 | 161 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 301,076 | 3.011 | 20 | 24 | fits | 148,026 | 217 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 301,010 | 3.010 | 20 | 50 | fits | 148,026 | 217 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 438,968 | 4.390 | 20 | 50 | fits | 138,354 | 163 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 528,493 | 5.285 | 20 | 20 | fits | 89,591 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,049,554 | 10.496 | 20 | 20 | fits | 67,737 | 24 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 445,468 | 4.455 | 20 | 20 | fits | 151,260 | 186 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 290,050 | 2.901 | 20 | 200 | fits | 148,068 | 201 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 525,404 | 5.254 | 20 | 200 | fits | 151,260 | 186 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 290,974 | 2.910 | 20 | 20 | fits | 148,068 | 201 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 526,108 | 5.261 | 20 | 20 | fits | 151,260 | 186 | 0.458 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 146,546 | 1.465 | 20 | 24 | fits | 144,644 | 161 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 293,624 | 2.936 | 20 | 24 | fits | 148,068 | 201 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 293,558 | 2.936 | 20 | 50 | fits | 148,068 | 201 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 529,132 | 5.291 | 20 | 50 | fits | 151,260 | 186 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 619,347 | 6.193 | 20 | 20 | fits | 90,281 | 24 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,041,400 | 10.414 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 384,404 | 3.844 | 20 | 20 | fits | 141,063 | 166 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 297,478 | 2.975 | 20 | 200 | fits | 148,896 | 219 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 446,594 | 4.466 | 20 | 200 | fits | 141,063 | 166 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 298,402 | 2.984 | 20 | 20 | fits | 148,896 | 219 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 447,298 | 4.473 | 20 | 20 | fits | 141,063 | 166 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 153,146 | 1.531 | 20 | 24 | fits | 144,254 | 161 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 301,052 | 3.011 | 20 | 24 | fits | 148,896 | 219 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 300,986 | 3.010 | 20 | 50 | fits | 148,896 | 219 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 450,322 | 4.503 | 20 | 50 | fits | 141,063 | 166 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 540,042 | 5.400 | 20 | 20 | fits | 89,786 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 967,931 | 9.679 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 362,583 | 3.626 | 20 | 20 | fits | 147,916 | 168 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 287,118 | 2.871 | 20 | 200 | fits | 148,849 | 222 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 434,418 | 4.344 | 20 | 200 | fits | 147,916 | 168 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 288,042 | 2.880 | 20 | 20 | fits | 148,849 | 222 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 435,122 | 4.351 | 20 | 20 | fits | 147,916 | 168 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 142,833 | 1.428 | 20 | 24 | fits | 144,590 | 161 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 290,692 | 2.907 | 20 | 24 | fits | 148,849 | 222 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 290,626 | 2.906 | 20 | 50 | fits | 148,849 | 222 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 438,146 | 4.381 | 20 | 50 | fits | 147,916 | 168 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 527,728 | 5.277 | 20 | 20 | fits | 89,648 | 25 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 965,099 | 9.651 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 362,270 | 3.623 | 20 | 20 | fits | 138,692 | 163 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 286,831 | 2.868 | 20 | 200 | fits | 148,842 | 222 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 424,907 | 4.249 | 20 | 200 | fits | 138,692 | 163 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 287,755 | 2.878 | 20 | 20 | fits | 148,842 | 222 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 425,611 | 4.256 | 20 | 20 | fits | 138,692 | 163 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 142,553 | 1.426 | 20 | 24 | fits | 144,630 | 161 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 290,405 | 2.904 | 20 | 24 | fits | 148,842 | 222 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 290,339 | 2.903 | 20 | 50 | fits | 148,842 | 222 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 428,635 | 4.286 | 20 | 50 | fits | 138,692 | 163 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 517,524 | 5.175 | 20 | 20 | fits | 88,955 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,041,074 | 10.411 | 20 | 20 | fits | 78,408 | 28 | 0.544 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 452,482 | 4.525 | 20 | 20 | fits | 149,059 | 186 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 302,983 | 3.030 | 20 | 200 | fits | 147,354 | 200 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 532,167 | 5.322 | 20 | 200 | fits | 149,059 | 186 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 303,907 | 3.039 | 20 | 20 | fits | 147,354 | 200 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 532,871 | 5.329 | 20 | 20 | fits | 149,059 | 186 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 152,631 | 1.526 | 20 | 24 | fits | 144,575 | 162 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 306,557 | 3.066 | 20 | 24 | fits | 147,354 | 200 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 306,491 | 3.065 | 20 | 50 | fits | 147,354 | 200 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 535,895 | 5.359 | 20 | 50 | fits | 149,059 | 186 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 624,855 | 6.249 | 20 | 20 | fits | 89,026 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,062,614 | 10.626 | 20 | 20 | fits | 67,821 | 24 | 0.604 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 376,803 | 3.768 | 20 | 20 | fits | 138,580 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 301,378 | 3.014 | 20 | 200 | fits | 147,795 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 439,342 | 4.393 | 20 | 200 | fits | 138,580 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 302,302 | 3.023 | 20 | 20 | fits | 147,795 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 440,046 | 4.400 | 20 | 20 | fits | 138,580 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 158,147 | 1.581 | 20 | 24 | fits | 144,777 | 161 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 304,952 | 3.050 | 20 | 24 | fits | 147,795 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 304,886 | 3.049 | 20 | 50 | fits | 147,795 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 443,070 | 4.431 | 20 | 50 | fits | 138,580 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 531,959 | 5.320 | 20 | 20 | fits | 88,955 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 975,635 | 9.756 | 20 | 20 | fits | 67,885 | 24 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 371,506 | 3.715 | 20 | 20 | fits | 151,077 | 174 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 293,502 | 2.935 | 20 | 200 | fits | 147,409 | 216 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 452,563 | 4.526 | 20 | 200 | fits | 151,077 | 174 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 294,426 | 2.944 | 20 | 20 | fits | 147,409 | 216 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 453,267 | 4.533 | 20 | 20 | fits | 151,077 | 174 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 150,657 | 1.507 | 20 | 24 | fits | 144,700 | 161 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 297,076 | 2.971 | 20 | 24 | fits | 147,409 | 216 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 297,010 | 2.970 | 20 | 50 | fits | 147,409 | 216 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 456,291 | 4.563 | 20 | 50 | fits | 151,077 | 174 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 545,471 | 5.455 | 20 | 20 | fits | 89,246 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 967,371 | 9.674 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 356,229 | 3.562 | 20 | 20 | fits | 139,138 | 164 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 290,092 | 2.901 | 20 | 200 | fits | 147,732 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 428,614 | 4.286 | 20 | 200 | fits | 139,138 | 164 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 291,016 | 2.910 | 20 | 20 | fits | 147,732 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 429,318 | 4.293 | 20 | 20 | fits | 139,138 | 164 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 146,924 | 1.469 | 20 | 24 | fits | 144,644 | 161 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 293,666 | 2.937 | 20 | 24 | fits | 147,732 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 293,600 | 2.936 | 20 | 50 | fits | 147,732 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 432,342 | 4.323 | 20 | 50 | fits | 139,138 | 164 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 533,963 | 5.340 | 20 | 20 | fits | 92,994 | 31 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,040,359 | 10.404 | 20 | 20 | fits | 67,451 | 24 | 0.593 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 446,711 | 4.467 | 20 | 20 | fits | 139,618 | 163 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 302,413 | 3.024 | 20 | 200 | fits | 155,026 | 222 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 518,789 | 5.188 | 20 | 200 | fits | 139,618 | 163 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 303,337 | 3.033 | 20 | 20 | fits | 155,026 | 222 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 519,493 | 5.195 | 20 | 20 | fits | 139,618 | 163 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 151,951 | 1.520 | 20 | 24 | fits | 144,319 | 161 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 305,987 | 3.060 | 20 | 24 | fits | 155,026 | 222 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 305,921 | 3.059 | 20 | 50 | fits | 155,026 | 222 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 522,517 | 5.225 | 20 | 50 | fits | 139,618 | 163 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 612,009 | 6.120 | 20 | 20 | fits | 89,558 | 24 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,049,748 | 10.497 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 353,079 | 3.531 | 20 | 20 | fits | 138,744 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 286,964 | 2.870 | 20 | 200 | fits | 148,617 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 425,092 | 4.251 | 20 | 200 | fits | 138,744 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 287,888 | 2.879 | 20 | 20 | fits | 148,617 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 425,796 | 4.258 | 20 | 20 | fits | 138,744 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 142,911 | 1.429 | 20 | 24 | fits | 144,520 | 161 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 290,538 | 2.905 | 20 | 24 | fits | 148,617 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 290,472 | 2.905 | 20 | 50 | fits | 148,617 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 428,820 | 4.288 | 20 | 50 | fits | 138,744 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 518,298 | 5.183 | 20 | 20 | fits | 89,544 | 24 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 960,277 | 9.603 | 20 | 20 | fits | 78,408 | 28 | 0.544 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 381,228 | 3.812 | 20 | 20 | fits | 142,508 | 169 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 311,144 | 3.111 | 20 | 200 | fits | 154,941 | 222 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 453,036 | 4.530 | 20 | 200 | fits | 142,508 | 169 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 312,068 | 3.121 | 20 | 20 | fits | 154,941 | 222 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 453,740 | 4.537 | 20 | 20 | fits | 142,508 | 169 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 153,253 | 1.533 | 20 | 24 | fits | 144,465 | 162 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 314,718 | 3.147 | 20 | 24 | fits | 154,941 | 222 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 314,652 | 3.147 | 20 | 50 | fits | 154,941 | 222 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 456,764 | 4.568 | 20 | 50 | fits | 142,508 | 169 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 546,081 | 5.461 | 20 | 20 | fits | 89,383 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 983,283 | 9.833 | 20 | 20 | fits | 72,849 | 31 | 0.676 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 145,808 | 1.458 | 20 | 20 | fits | 27,612 | 8 | 0.826 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 52,495 | 0.525 | 20 | 20 | fits | 52,561 | 12 | 0.877 |
| malformed MRPDU discard | `srp.malformed.if0` | 23,493 | 0.235 | 20 | 20 | fits | 23,559 | 12 | 0.640 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 170,957 | 1.710 | 220 | 220 | fits | 139,264 | 7 | 0.819 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 20,169 | 0.202 | 20 | 20 | fits | 32,598 | 19 | 0.792 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 288,277 | 2.883 | 20 | 200 | fits | 147,788 | 218 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 42,368 | 0.424 | 20 | 200 | fits | 32,598 | 19 | 0.792 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 289,201 | 2.892 | 20 | 20 | fits | 147,788 | 218 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 425,035 | 4.250 | 20 | 20 | fits | 128,137 | 160 | 0.402 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 145,053 | 1.451 | 20 | 24 | fits | 145,239 | 164 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 291,851 | 2.919 | 20 | 24 | fits | 147,788 | 218 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 291,785 | 2.918 | 20 | 50 | fits | 147,788 | 218 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 428,059 | 4.281 | 20 | 50 | fits | 128,137 | 160 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 522,008 | 5.220 | 20 | 20 | fits | 94,015 | 30 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 944,088 | 9.441 | 20 | 20 | fits | 67,412 | 24 | 0.591 |
| LINK_UP | `adp.link_up.if0` | 2,690 | 0.027 | 20 | 200 | fits | 30,690 | 43 (11) | 0.710 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,416 | 0.174 | 20 | 200 | fits | 24,384 | 23 (39) | 0.726 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,762 | 0.048 | 20 | 200 | fits | 19,133 | 16 (31) | 0.605 |
| LINK_UP | `adp.link_up.if0` | 2,690 | 0.027 | 20 | 200 | fits | 30,690 | 43 (11) | 0.710 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,416 | 0.174 | 20 | 200 | fits | 24,384 | 23 (39) | 0.726 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,762 | 0.048 | 20 | 200 | fits | 19,133 | 16 (31) | 0.605 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
