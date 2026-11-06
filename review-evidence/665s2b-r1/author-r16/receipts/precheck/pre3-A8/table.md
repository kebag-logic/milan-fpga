### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 313 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.106 (7.840) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-4.adp_available.if0` (backlog-adp@program-aged2-4) | 6.666 (8.069) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.089 (0.457) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.505 (2.559) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.552 (63.918) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.408 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.344 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.acmp.last.if0` (backlog-adp@program-aged2-4) | 10.165 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.387 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.adp.last.if0` (backlog-adp@program-aged2-4) | 7.971 | fits | 7 adp | 26 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 6.580 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.380 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.811 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.370 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.maap.last.if0` (backlog-adp@blank-aged2-7) | 6.511 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.487 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-aged2-4.service.srp.last.if1` (backlog-adp@verify-aged2-4) | 17.665 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-aged2-0 | 0 | 17.764 | 22 | 188,833 (1.888) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 17.356 | 19 | 189,582 (1.896) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 18.743 | 22 | 187,582 (1.876) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 18.499 | 21 | 188,481 (1.885) | yes | - |
| backlog-adp@blank-aged2-4 | 1 | 19.199 | 22 | 189,452 (1.895) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 18.613 | 22 | 188,481 (1.885) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 18.648 | 22 | 165,531 (1.655) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 18.357 | 20 | 165,382 (1.654) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 17.741 | 20 | 188,325 (1.883) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 17.715 | 21 | 187,354 (1.874) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 18.150 | 22 | 181,644 (1.816) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 18.118 | 21 | 189,048 (1.890) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 18.003 | 21 | 187,561 (1.876) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 17.876 | 21 | 188,532 (1.885) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 17.858 | 22 | 162,365 (1.624) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 17.810 | 21 | 162,269 (1.623) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 18.209 | 23 | 190,113 (1.901) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 18.107 | 22 | 188,626 (1.886) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 18.854 | 20 | 189,597 (1.896) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 18.861 | 21 | 187,525 (1.875) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 19.048 | 21 | 188,274 (1.883) | yes | - |
| backlog-adp@verify-aged2-5 | 1 | 19.554 | 23 | 189,245 (1.892) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 19.052 | 22 | 160,299 (1.603) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 19.179 | 22 | 162,560 (1.626) | yes | - |
| backlog | 0 | 14.728 | 21 | 162,846 (1.628) | yes | - |
| backlog-adp | 0 | 17.342 | 23 | 160,997 (1.610) | yes | - |
| backlog-adp-refill | 0 | 40.947 | 32 | 140,480 (1.405) | yes | - |
| backlog-owed | 0 | 360.458 | 66 | 160,340 (1.603) | yes | - |

Composed maximum over the 4 backlog windows: 162,846 CPU cycles (1.628 ms), backlog.
Over the windows that released their whole load only: 162,846 (1.628 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-aged2-0 | 832 | 0 | 188,833 (1.888) | fits |
| backlog-adp@blank-aged2-1 | 836 | 0 | 189,582 (1.896) | fits |
| backlog-adp@blank-aged2-2 | 845 | 0 | 187,582 (1.876) | fits |
| backlog-adp@blank-aged2-3 | 852 | 0 | 188,481 (1.885) | fits |
| backlog-adp@blank-aged2-4 | 860 | 0 | 189,452 (1.895) | fits |
| backlog-adp@blank-aged2-5 | 866 | 0 | 188,481 (1.885) | fits |
| backlog-adp@blank-aged2-6 | 873 | 0 | 165,531 (1.655) | fits |
| backlog-adp@blank-aged2-7 | 878 | 0 | 165,382 (1.654) | fits |
| backlog-adp@program-aged2-0 | 1202 | 0 | 188,325 (1.883) | fits |
| backlog-adp@program-aged2-1 | 1209 | 0 | 187,354 (1.874) | fits |
| backlog-adp@program-aged2-2 | 1217 | 0 | 181,644 (1.816) | fits |
| backlog-adp@program-aged2-3 | 1223 | 0 | 189,048 (1.890) | fits |
| backlog-adp@program-aged2-4 | 1230 | 0 | 187,561 (1.876) | fits |
| backlog-adp@program-aged2-5 | 1237 | 0 | 188,532 (1.885) | fits |
| backlog-adp@program-aged2-6 | 1244 | 0 | 162,365 (1.624) | fits |
| backlog-adp@program-aged2-7 | 1251 | 0 | 162,269 (1.623) | fits |
| backlog-adp@verify-aged2-0 | 1572 | 0 | 190,113 (1.901) | fits |
| backlog-adp@verify-aged2-1 | 1578 | 0 | 188,626 (1.886) | fits |
| backlog-adp@verify-aged2-2 | 1583 | 0 | 189,597 (1.896) | fits |
| backlog-adp@verify-aged2-3 | 1590 | 0 | 187,525 (1.875) | fits |
| backlog-adp@verify-aged2-4 | 1598 | 0 | 188,274 (1.883) | fits |
| backlog-adp@verify-aged2-5 | 1607 | 0 | 189,245 (1.892) | fits |
| backlog-adp@verify-aged2-6 | 1612 | 0 | 160,299 (1.603) | fits |
| backlog-adp@verify-aged2-7 | 1619 | 0 | 162,560 (1.626) | fits |
| backlog | 309 | 0 | 162,846 (1.628) | fits |
| backlog-adp | 336 | 0 | 160,997 (1.610) | fits |
| backlog-adp-refill | 345 | 0 | 140,480 (1.405) | fits |
| backlog-owed | 365 | 0 | 160,340 (1.603) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +10.248 ms, 77,900 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 17.146 (18) | 0.854 |
| backlog-adp@blank-aged2-1 | 2 | +9.013 ms, 77,835 (0.778 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 16.733 (18) | 1.267 |
| backlog-adp@blank-aged2-2 | 2 | +8.139 ms, 85,052 (0.851 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 16.805 (18) | 1.195 |
| backlog-adp@blank-aged2-3 | 2 | +6.743 ms, 78,182 (0.782 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 17.118 (18) | 0.882 |
| backlog-adp@blank-aged2-4 | 2 | +5.549 ms, 78,231 (0.782 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 17.034 (18) | 0.966 |
| backlog-adp@blank-aged2-5 | 2 | +5.203 ms, 85,111 (0.851 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 17.132 (18) | 0.868 |
| backlog-adp@blank-aged2-6 | 2 | +3.614 ms, 85,164 (0.852 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 17.274 (18) | 0.726 |
| backlog-adp@blank-aged2-7 | 2 | +2.578 ms, 85,100 (0.851 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 16.976 (18) | 1.024 |
| backlog-adp@program-aged2-0 | 2 | +10.168 ms, 84,075 (0.841 ms), issue | none | `backlog-adp@program-aged2-0.service.srp.last.if1` | 16.871 (18) | 1.129 |
| backlog-adp@program-aged2-1 | 2 | +8.823 ms, 84,076 (0.841 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if1` | 16.835 (18) | 1.165 |
| backlog-adp@program-aged2-2 | 2 | +7.965 ms, 84,314 (0.843 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if1` | 16.991 (18) | 1.009 |
| backlog-adp@program-aged2-3 | 2 | +7.029 ms, 84,249 (0.842 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if1` | 17.186 (18) | 0.814 |
| backlog-adp@program-aged2-4 | 2 | +5.784 ms, 84,246 (0.842 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if1` | 17.338 (18) | 0.662 |
| backlog-adp@program-aged2-5 | 2 | +4.195 ms, 84,246 (0.842 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if1` | 17.203 (18) | 0.797 |
| backlog-adp@program-aged2-6 | 2 | +3.676 ms, 84,275 (0.843 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if1` | 17.185 (18) | 0.815 |
| backlog-adp@program-aged2-7 | 2 | +3.539 ms, 84,275 (0.843 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if1` | 17.137 (18) | 0.863 |
| backlog-adp@verify-aged2-0 | 2 | +10.202 ms, 78,733 (0.787 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 17.592 (18) | 0.408 |
| backlog-adp@verify-aged2-1 | 2 | +8.930 ms, 78,733 (0.787 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 17.489 (18) | 0.511 |
| backlog-adp@verify-aged2-2 | 2 | +8.122 ms, 78,999 (0.790 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 17.467 (18) | 0.533 |
| backlog-adp@verify-aged2-3 | 2 | +6.935 ms, 78,950 (0.789 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 17.477 (18) | 0.523 |
| backlog-adp@verify-aged2-4 | 2 | +5.693 ms, 79,064 (0.791 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 17.665 (18) | 0.335 |
| backlog-adp@verify-aged2-5 | 2 | +5.178 ms, 79,064 (0.791 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 17.540 (18) | 0.460 |
| backlog-adp@verify-aged2-6 | 2 | +3.586 ms, 79,027 (0.790 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 17.406 (18) | 0.594 |
| backlog-adp@verify-aged2-7 | 2 | +2.548 ms, 79,027 (0.790 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 17.539 (18) | 0.461 |

Least margin over the aged windows: 0.335 ms, `backlog-adp@verify-aged2-4.service.srp.last.if1` at 17.665 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-aged2-0 | 335 | 77,900 (0.779) | 75,557 (0.756) |
| backlog-adp@blank-aged2-1 | 335 | 77,835 (0.778) | 75,557 (0.756) |
| backlog-adp@blank-aged2-2 | 336 | 96,667 (0.967) | 75,773 (0.758) |
| backlog-adp@blank-aged2-3 | 336 | 99,270 (0.993) | 75,773 (0.758) |
| backlog-adp@blank-aged2-4 | 336 | 99,234 (0.992) | 75,773 (0.758) |
| backlog-adp@blank-aged2-5 | 336 | 99,853 (0.999) | 75,773 (0.758) |
| backlog-adp@blank-aged2-6 | 336 | 98,650 (0.987) | 75,829 (0.758) |
| backlog-adp@blank-aged2-7 | 336 | 99,270 (0.993) | 75,829 (0.758) |
| backlog-adp@program-aged2-0 | 441 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-aged2-1 | 441 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-aged2-2 | 442 | 122,291 (1.223) | 81,755 (0.818) |
| backlog-adp@program-aged2-3 | 442 | 122,291 (1.223) | 81,755 (0.818) |
| backlog-adp@program-aged2-4 | 442 | 122,291 (1.223) | 81,755 (0.818) |
| backlog-adp@program-aged2-5 | 442 | 122,291 (1.223) | 81,755 (0.818) |
| backlog-adp@program-aged2-6 | 442 | 122,291 (1.223) | 81,811 (0.818) |
| backlog-adp@program-aged2-7 | 442 | 122,291 (1.223) | 81,811 (0.818) |
| backlog-adp@verify-aged2-0 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-1 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-2 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-3 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-4 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-5 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-6 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-7 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog | 266 | 50,112 (0.501) | 2,240 (0.022) |
| backlog-adp | 271 | 50,112 (0.501) | 2,224 (0.022) |
| backlog-adp-refill | 273 | 50,112 (0.501) | 2,303 (0.023) |
| backlog-owed | 305 | 50,112 (0.501) | 2,255 (0.023) |

Longest pass that carries a step: 122,291 CPU cycles (1.223 ms), backlog-adp@program-aged2-0; longest step: 95,651 (0.957 ms), backlog-adp@verify-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 479,386 | 4.794 | 20 | 20 | fits | 152,020 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 124,979 | 1.250 | 20 | 200 | fits | 117,370 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 620,384 | 6.204 | 20 | 200 | fits | 152,020 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 125,891 | 1.259 | 20 | 20 | fits | 117,370 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 862,321 | 8.623 | 20 | 20 | fits | 120,356 | 46 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 129,476 | 1.295 | 20 | 24 | fits | 117,370 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 1,529,390 | 15.294 | 20 | 24 | fits | 65,334 | 32 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 128,436 | 1.284 | 20 | 50 | fits | 117,370 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 624,060 | 6.241 | 20 | 50 | fits | 152,020 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 316,814 | 3.168 | 18 | 18 | fits | 188,833 | 141 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 1,714,608 | 17.146 | 18 | 18 | fits | 36,750 | 15 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 464,812 | 4.648 | 20 | 20 | fits | 153,533 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 110,373 | 1.104 | 20 | 200 | fits | 117,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 606,400 | 6.064 | 20 | 200 | fits | 153,533 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 111,285 | 1.113 | 20 | 20 | fits | 117,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 834,585 | 8.346 | 20 | 20 | fits | 106,503 | 42 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 114,870 | 1.149 | 20 | 24 | fits | 117,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 1,581,632 | 15.816 | 20 | 24 | fits | 65,789 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 113,830 | 1.138 | 20 | 50 | fits | 117,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 610,076 | 6.101 | 20 | 50 | fits | 153,533 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 302,957 | 3.030 | 18 | 18 | fits | 189,582 | 146 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 1,673,302 | 16.733 | 18 | 18 | fits | 46,452 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 466,813 | 4.668 | 20 | 20 | fits | 153,419 | 83 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 114,166 | 1.142 | 20 | 200 | fits | 117,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 608,378 | 6.084 | 20 | 200 | fits | 153,419 | 83 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 115,078 | 1.151 | 20 | 20 | fits | 117,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 995,105 | 9.951 | 20 | 20 | fits | 100,740 | 45 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 118,663 | 1.187 | 20 | 24 | fits | 117,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 1,588,806 | 15.888 | 20 | 24 | fits | 65,642 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 117,623 | 1.176 | 20 | 50 | fits | 117,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 612,054 | 6.121 | 20 | 50 | fits | 153,419 | 83 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 313,346 | 3.133 | 18 | 18 | fits | 187,582 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 1,680,476 | 16.805 | 18 | 18 | fits | 46,452 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 471,434 | 4.714 | 20 | 20 | fits | 118,999 | 74 | 0.630 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 126,616 | 1.266 | 20 | 200 | fits | 117,098 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 578,579 | 5.786 | 20 | 200 | fits | 118,999 | 74 | 0.630 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 127,528 | 1.275 | 20 | 20 | fits | 117,098 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 931,151 | 9.312 | 20 | 20 | fits | 98,588 | 46 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 131,113 | 1.311 | 20 | 24 | fits | 117,098 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 1,532,846 | 15.328 | 20 | 24 | fits | 65,452 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 130,073 | 1.301 | 20 | 50 | fits | 117,098 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 582,255 | 5.823 | 20 | 50 | fits | 118,999 | 74 | 0.630 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 318,099 | 3.181 | 18 | 18 | fits | 188,481 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 1,711,799 | 17.118 | 18 | 18 | fits | 46,311 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 637,156 | 6.372 | 20 | 20 | fits | 105,641 | 49 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 110,936 | 1.109 | 20 | 200 | fits | 117,051 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 733,465 | 7.335 | 20 | 200 | fits | 105,641 | 49 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 111,848 | 1.118 | 20 | 20 | fits | 117,051 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 953,555 | 9.536 | 20 | 20 | fits | 98,313 | 40 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 115,433 | 1.154 | 20 | 24 | fits | 117,051 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 1,519,019 | 15.190 | 20 | 24 | fits | 59,159 | 32 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 114,393 | 1.144 | 20 | 50 | fits | 117,051 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 553,269 | 5.533 | 20 | 50 | fits | 104,640 | 64 | 0.729 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 303,390 | 3.034 | 18 | 18 | fits | 189,452 | 145 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 1,703,362 | 17.034 | 18 | 18 | fits | 46,344 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 612,791 | 6.128 | 20 | 20 | fits | 143,466 | 63 | 0.712 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 114,335 | 1.143 | 20 | 200 | fits | 117,051 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 743,543 | 7.435 | 20 | 200 | fits | 143,466 | 63 | 0.712 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 115,247 | 1.152 | 20 | 20 | fits | 117,051 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 962,794 | 9.628 | 20 | 20 | fits | 98,171 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 118,832 | 1.188 | 20 | 24 | fits | 117,051 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 1,539,963 | 15.400 | 20 | 24 | fits | 65,486 | 32 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 117,792 | 1.178 | 20 | 50 | fits | 117,051 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 518,642 | 5.186 | 20 | 50 | fits | 102,929 | 64 | 0.711 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 305,818 | 3.058 | 18 | 18 | fits | 188,481 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 1,713,232 | 17.132 | 18 | 18 | fits | 34,341 | 16 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 617,511 | 6.175 | 20 | 20 | fits | 141,986 | 57 | 0.715 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 117,288 | 1.173 | 20 | 200 | fits | 117,051 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 748,766 | 7.488 | 20 | 200 | fits | 141,986 | 57 | 0.715 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 118,200 | 1.182 | 20 | 20 | fits | 117,051 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 967,572 | 9.676 | 20 | 20 | fits | 97,957 | 39 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 121,785 | 1.218 | 20 | 24 | fits | 117,051 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 1,543,100 | 15.431 | 20 | 24 | fits | 65,295 | 32 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 120,745 | 1.207 | 20 | 50 | fits | 117,051 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 610,456 | 6.105 | 20 | 50 | fits | 165,531 | 104 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 359,696 | 3.597 | 18 | 18 | fits | 125,195 | 64 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 1,727,374 | 17.274 | 18 | 18 | fits | 33,961 | 15 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 657,791 | 6.578 | 20 | 20 | fits | 140,887 | 57 | 0.709 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 120,241 | 1.202 | 20 | 200 | fits | 117,051 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 788,314 | 7.883 | 20 | 200 | fits | 140,887 | 57 | 0.709 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 121,153 | 1.212 | 20 | 20 | fits | 117,051 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 1,007,235 | 10.072 | 20 | 20 | fits | 97,980 | 39 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 124,738 | 1.247 | 20 | 24 | fits | 117,051 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 1,606,202 | 16.062 | 20 | 24 | fits | 65,598 | 31 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 123,698 | 1.237 | 20 | 50 | fits | 117,051 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 651,103 | 6.511 | 20 | 50 | fits | 144,456 | 98 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 256,100 | 2.561 | 18 | 18 | fits | 132,857 | 105 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 1,697,592 | 16.976 | 18 | 18 | fits | 46,312 | 18 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 461,103 | 4.611 | 20 | 20 | fits | 157,365 | 90 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 111,823 | 1.118 | 20 | 200 | fits | 118,164 | 134 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 602,190 | 6.022 | 20 | 200 | fits | 157,365 | 90 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 112,735 | 1.127 | 20 | 20 | fits | 118,164 | 134 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 844,681 | 8.447 | 20 | 20 | fits | 120,570 | 47 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 116,320 | 1.163 | 20 | 24 | fits | 118,164 | 134 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 1,556,384 | 15.564 | 20 | 24 | fits | 65,268 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 115,280 | 1.153 | 20 | 50 | fits | 118,164 | 134 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 605,866 | 6.059 | 20 | 50 | fits | 157,365 | 90 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 303,150 | 3.031 | 18 | 18 | fits | 188,325 | 145 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if1` | 1,687,078 | 16.871 | 18 | 18 | fits | 38,890 | 22 | 0.775 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 425,396 | 4.254 | 20 | 20 | fits | 153,519 | 90 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 115,222 | 1.152 | 20 | 200 | fits | 117,607 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 565,449 | 5.654 | 20 | 200 | fits | 153,519 | 90 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 116,134 | 1.161 | 20 | 20 | fits | 117,607 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 807,682 | 8.077 | 20 | 20 | fits | 120,371 | 47 | 0.702 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 119,719 | 1.197 | 20 | 24 | fits | 117,607 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 1,553,797 | 15.538 | 20 | 24 | fits | 65,447 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 118,679 | 1.187 | 20 | 50 | fits | 117,607 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 569,125 | 5.691 | 20 | 50 | fits | 153,519 | 90 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 305,578 | 3.056 | 18 | 18 | fits | 187,354 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if1` | 1,683,481 | 16.835 | 18 | 18 | fits | 50,229 | 25 | 0.720 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 426,033 | 4.260 | 20 | 20 | fits | 155,370 | 84 | 0.679 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 118,175 | 1.182 | 20 | 200 | fits | 117,607 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 568,823 | 5.688 | 20 | 200 | fits | 155,370 | 84 | 0.679 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 119,087 | 1.191 | 20 | 20 | fits | 117,607 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 973,477 | 9.735 | 20 | 20 | fits | 97,236 | 39 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 122,672 | 1.227 | 20 | 24 | fits | 117,607 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 1,572,071 | 15.721 | 20 | 24 | fits | 70,427 | 38 | 0.725 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 121,632 | 1.216 | 20 | 50 | fits | 117,607 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 572,499 | 5.725 | 20 | 50 | fits | 155,370 | 84 | 0.679 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 417,064 | 4.171 | 18 | 18 | fits | 181,644 | 105 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if1` | 1,699,113 | 16.991 | 18 | 18 | fits | 34,354 | 16 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 467,128 | 4.671 | 20 | 20 | fits | 139,593 | 80 | 0.679 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 121,215 | 1.212 | 20 | 200 | fits | 117,694 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 594,600 | 5.946 | 20 | 200 | fits | 139,593 | 80 | 0.679 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 122,127 | 1.221 | 20 | 20 | fits | 117,694 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 1,000,259 | 10.003 | 20 | 20 | fits | 98,414 | 39 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 125,712 | 1.257 | 20 | 24 | fits | 117,694 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 1,584,646 | 15.846 | 20 | 24 | fits | 52,158 | 28 | 0.738 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 124,672 | 1.247 | 20 | 50 | fits | 117,694 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 598,276 | 5.983 | 20 | 50 | fits | 139,593 | 80 | 0.679 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 313,265 | 3.133 | 18 | 18 | fits | 189,048 | 146 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if1` | 1,718,555 | 17.186 | 18 | 18 | fits | 46,551 | 19 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 666,649 | 6.666 | 20 | 20 | fits | 139,796 | 57 | 0.705 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 127,189 | 1.272 | 20 | 200 | fits | 117,864 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 797,142 | 7.971 | 20 | 200 | fits | 139,796 | 57 | 0.705 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 128,101 | 1.281 | 20 | 20 | fits | 117,864 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 1,016,481 | 10.165 | 20 | 20 | fits | 98,171 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 131,686 | 1.317 | 20 | 24 | fits | 117,864 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 1,595,260 | 15.953 | 20 | 24 | fits | 65,740 | 32 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 130,646 | 1.306 | 20 | 50 | fits | 117,864 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 576,776 | 5.768 | 20 | 50 | fits | 103,798 | 64 | 0.723 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 317,752 | 3.178 | 18 | 18 | fits | 187,561 | 141 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if1` | 1,733,753 | 17.338 | 18 | 18 | fits | 34,192 | 15 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 651,281 | 6.513 | 20 | 20 | fits | 141,118 | 57 | 0.710 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 111,487 | 1.115 | 20 | 200 | fits | 117,864 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 781,990 | 7.820 | 20 | 200 | fits | 141,118 | 57 | 0.710 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 112,399 | 1.124 | 20 | 20 | fits | 117,864 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 1,001,271 | 10.013 | 20 | 20 | fits | 98,182 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 115,984 | 1.160 | 20 | 24 | fits | 117,864 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 1,535,880 | 15.359 | 20 | 24 | fits | 65,867 | 31 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 114,944 | 1.149 | 20 | 50 | fits | 117,864 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 644,548 | 6.445 | 20 | 50 | fits | 142,386 | 98 | 0.614 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 303,021 | 3.030 | 18 | 18 | fits | 188,532 | 146 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if1` | 1,720,277 | 17.203 | 18 | 18 | fits | 46,290 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 619,673 | 6.197 | 20 | 20 | fits | 141,916 | 57 | 0.714 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 116,376 | 1.164 | 20 | 200 | fits | 117,864 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 750,858 | 7.509 | 20 | 200 | fits | 141,916 | 57 | 0.714 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 117,288 | 1.173 | 20 | 20 | fits | 117,864 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 936,097 | 9.361 | 20 | 20 | fits | 64,390 | 31 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 120,873 | 1.209 | 20 | 24 | fits | 117,864 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 1,534,851 | 15.349 | 20 | 24 | fits | 65,276 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 119,833 | 1.198 | 20 | 50 | fits | 117,864 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 612,618 | 6.126 | 20 | 50 | fits | 162,365 | 98 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 365,913 | 3.659 | 18 | 18 | fits | 124,350 | 64 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if1` | 1,718,541 | 17.185 | 18 | 18 | fits | 46,150 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 605,898 | 6.059 | 20 | 20 | fits | 141,896 | 57 | 0.715 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 110,333 | 1.103 | 20 | 200 | fits | 117,216 | 134 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 737,063 | 7.371 | 20 | 200 | fits | 141,896 | 57 | 0.715 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 111,245 | 1.112 | 20 | 20 | fits | 117,216 | 134 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 922,611 | 9.226 | 20 | 20 | fits | 98,136 | 46 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 114,830 | 1.148 | 20 | 24 | fits | 117,216 | 134 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 1,483,881 | 14.839 | 20 | 24 | fits | 65,109 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 113,790 | 1.138 | 20 | 50 | fits | 117,216 | 134 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 598,843 | 5.988 | 20 | 50 | fits | 162,269 | 98 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 352,234 | 3.522 | 18 | 18 | fits | 123,963 | 64 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if1` | 1,713,721 | 17.137 | 18 | 18 | fits | 46,150 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 474,788 | 4.748 | 20 | 20 | fits | 152,006 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 119,019 | 1.190 | 20 | 200 | fits | 117,341 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 615,772 | 6.158 | 20 | 200 | fits | 152,006 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 119,931 | 1.199 | 20 | 20 | fits | 117,341 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 857,709 | 8.577 | 20 | 20 | fits | 120,356 | 46 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 123,516 | 1.235 | 20 | 24 | fits | 117,341 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 1,527,311 | 15.273 | 20 | 24 | fits | 65,615 | 32 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 122,476 | 1.225 | 20 | 50 | fits | 117,341 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 619,448 | 6.194 | 20 | 50 | fits | 152,006 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 312,134 | 3.121 | 18 | 18 | fits | 190,113 | 146 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 1,759,228 | 17.592 | 18 | 18 | fits | 34,250 | 15 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 478,622 | 4.786 | 20 | 20 | fits | 153,519 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 125,225 | 1.252 | 20 | 200 | fits | 117,464 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 620,196 | 6.202 | 20 | 200 | fits | 153,519 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 126,137 | 1.261 | 20 | 20 | fits | 117,464 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 828,252 | 8.283 | 20 | 20 | fits | 86,418 | 37 | 0.652 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 129,722 | 1.297 | 20 | 24 | fits | 117,464 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 1,564,332 | 15.643 | 20 | 24 | fits | 65,362 | 32 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 128,682 | 1.287 | 20 | 50 | fits | 117,464 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 623,872 | 6.239 | 20 | 50 | fits | 153,519 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 316,853 | 3.169 | 18 | 18 | fits | 188,626 | 141 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 1,748,937 | 17.489 | 18 | 18 | fits | 34,080 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 465,069 | 4.651 | 20 | 20 | fits | 153,519 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 110,619 | 1.106 | 20 | 200 | fits | 117,464 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 606,643 | 6.066 | 20 | 200 | fits | 153,519 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 111,531 | 1.115 | 20 | 20 | fits | 117,464 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 983,954 | 9.840 | 20 | 20 | fits | 97,315 | 39 | 0.741 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 115,116 | 1.151 | 20 | 24 | fits | 117,464 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 1,626,221 | 16.262 | 20 | 24 | fits | 65,789 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 114,076 | 1.141 | 20 | 50 | fits | 117,464 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 610,319 | 6.103 | 20 | 50 | fits | 153,519 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 303,218 | 3.032 | 18 | 18 | fits | 189,597 | 146 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 1,746,735 | 17.467 | 18 | 18 | fits | 41,101 | 19 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 467,002 | 4.670 | 20 | 20 | fits | 139,186 | 79 | 0.678 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 114,412 | 1.144 | 20 | 200 | fits | 117,464 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 594,334 | 5.943 | 20 | 200 | fits | 139,186 | 79 | 0.678 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 115,324 | 1.153 | 20 | 20 | fits | 117,464 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 989,674 | 9.897 | 20 | 20 | fits | 102,330 | 46 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 118,909 | 1.189 | 20 | 24 | fits | 117,464 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 1,620,768 | 16.208 | 20 | 24 | fits | 58,832 | 32 | 0.757 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 117,869 | 1.179 | 20 | 50 | fits | 117,464 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 598,010 | 5.980 | 20 | 50 | fits | 139,186 | 79 | 0.678 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 313,535 | 3.135 | 18 | 18 | fits | 187,525 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 1,747,678 | 17.477 | 18 | 18 | fits | 34,101 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 652,424 | 6.524 | 20 | 20 | fits | 126,825 | 54 | 0.717 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 126,631 | 1.266 | 20 | 200 | fits | 117,165 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 769,917 | 7.699 | 20 | 200 | fits | 126,825 | 54 | 0.717 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 127,543 | 1.275 | 20 | 20 | fits | 117,165 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 993,007 | 9.930 | 20 | 20 | fits | 98,515 | 40 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 131,128 | 1.311 | 20 | 24 | fits | 117,165 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 1,557,820 | 15.578 | 20 | 24 | fits | 33,463 | 22 | 0.672 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 130,088 | 1.301 | 20 | 50 | fits | 117,165 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 567,704 | 5.677 | 20 | 50 | fits | 104,640 | 64 | 0.729 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 317,907 | 3.179 | 18 | 18 | fits | 188,274 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 1,766,473 | 17.665 | 18 | 18 | fits | 34,113 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 600,761 | 6.008 | 20 | 20 | fits | 105,368 | 49 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 111,003 | 1.110 | 20 | 200 | fits | 117,118 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 696,913 | 6.969 | 20 | 200 | fits | 105,368 | 49 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 111,915 | 1.119 | 20 | 20 | fits | 117,118 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 916,706 | 9.167 | 20 | 20 | fits | 98,110 | 40 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 115,500 | 1.155 | 20 | 24 | fits | 117,118 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 1,534,741 | 15.347 | 20 | 24 | fits | 99,715 | 45 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 114,460 | 1.145 | 20 | 50 | fits | 117,118 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 516,157 | 5.162 | 20 | 50 | fits | 102,929 | 64 | 0.711 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 303,250 | 3.033 | 18 | 18 | fits | 189,245 | 145 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 1,754,031 | 17.540 | 18 | 18 | fits | 34,080 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 553,075 | 5.531 | 20 | 20 | fits | 160,299 | 64 | 0.736 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 114,350 | 1.143 | 20 | 200 | fits | 117,118 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 701,399 | 7.014 | 20 | 200 | fits | 160,299 | 64 | 0.736 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 115,262 | 1.153 | 20 | 20 | fits | 117,118 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 922,087 | 9.221 | 20 | 20 | fits | 98,465 | 40 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 118,847 | 1.188 | 20 | 24 | fits | 117,118 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 1,551,664 | 15.517 | 20 | 24 | fits | 65,719 | 31 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 117,807 | 1.178 | 20 | 50 | fits | 117,118 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 544,776 | 5.448 | 20 | 50 | fits | 108,792 | 90 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 356,892 | 3.569 | 18 | 18 | fits | 125,229 | 64 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 1,740,604 | 17.406 | 18 | 18 | fits | 51,312 | 25 | 0.720 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 610,929 | 6.109 | 20 | 20 | fits | 142,240 | 58 | 0.714 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 117,303 | 1.173 | 20 | 200 | fits | 117,118 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 742,093 | 7.421 | 20 | 200 | fits | 142,240 | 58 | 0.714 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 118,215 | 1.182 | 20 | 20 | fits | 117,118 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 969,754 | 9.698 | 20 | 20 | fits | 96,760 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 121,800 | 1.218 | 20 | 24 | fits | 117,118 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 1,576,183 | 15.762 | 20 | 24 | fits | 99,566 | 45 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 120,760 | 1.208 | 20 | 50 | fits | 117,118 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 603,529 | 6.035 | 20 | 50 | fits | 162,560 | 105 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 253,113 | 2.531 | 18 | 18 | fits | 132,808 | 105 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 1,753,862 | 17.539 | 18 | 18 | fits | 34,324 | 16 | 0.759 |
| an event behind 15 others | `backlog.event.if0` | 150,513 | 1.505 | 20 | 200 | fits | 116,968 | 125 | 0.541 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 710,630 | 7.106 | 20 | 20 | fits | 80,418 | 39 | 0.713 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 138,707 | 1.387 | 20 | 200 | fits | 138,915 | 143 | 0.529 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 550,213 | 5.502 | 20 | 200 | fits | 132,301 | 57 | 0.695 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 134,448 | 1.344 | 20 | 20 | fits | 138,915 | 143 | 0.529 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 778,734 | 7.787 | 20 | 20 | fits | 80,418 | 39 | 0.713 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 138,033 | 1.380 | 20 | 24 | fits | 138,915 | 143 | 0.529 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,248,697 | 12.487 | 20 | 24 | fits | 51,735 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 136,993 | 1.370 | 20 | 50 | fits | 138,915 | 143 | 0.529 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 548,718 | 5.487 | 20 | 50 | fits | 132,301 | 57 | 0.695 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 548,653 | 5.487 | 18 | 18 | fits | 132,301 | 57 | 0.695 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,414,026 | 14.140 | 18 | 18 | fits | 32,236 | 15 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 468,610 | 4.686 | 20 | 20 | fits | 160,997 | 58 | 0.750 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 111,058 | 1.111 | 20 | 200 | fits | 115,740 | 140 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 618,902 | 6.189 | 20 | 200 | fits | 160,997 | 58 | 0.750 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 111,970 | 1.120 | 20 | 20 | fits | 115,740 | 140 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 847,333 | 8.473 | 20 | 20 | fits | 98,060 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 115,555 | 1.156 | 20 | 24 | fits | 115,740 | 140 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,421,336 | 14.213 | 20 | 24 | fits | 51,943 | 28 | 0.741 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 114,515 | 1.145 | 20 | 50 | fits | 115,740 | 140 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 461,581 | 4.616 | 20 | 50 | fits | 124,785 | 65 | 0.741 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 461,516 | 4.615 | 18 | 18 | fits | 124,785 | 65 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,644,714 | 16.447 | 18 | 18 | fits | 34,175 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,904 | 0.089 | 20 | 20 | fits | 45,742 | 27 | 0.780 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 111,058 | 1.111 | 20 | 200 | fits | 115,740 | 140 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 42,854 | 0.429 | 20 | 200 | fits | 45,742 | 27 | 0.780 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 111,970 | 1.120 | 20 | 20 | fits | 115,740 | 140 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 826,736 | 8.267 | 20 | 20 | fits | 98,091 | 39 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 115,555 | 1.156 | 20 | 24 | fits | 115,740 | 140 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,416,171 | 14.162 | 20 | 24 | fits | 65,292 | 32 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 114,515 | 1.145 | 20 | 50 | fits | 115,740 | 140 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 461,581 | 4.616 | 20 | 50 | fits | 124,785 | 65 | 0.741 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 461,516 | 4.615 | 18 | 18 | fits | 124,785 | 65 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,604,560 | 16.046 | 18 | 18 | fits | 46,385 | 19 | 0.682 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,355,246 | 63.552 | 20 | 20 | MISS ceiling | 48,040 | 27 | 0.586 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,040,782 | 360.408 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,040,707 | 360.407 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,040,632 | 360.406 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,040,557 | 360.406 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 114,586 | 1.146 | 20 | 200 | fits | 112,944 | 134 | 0.519 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 657,978 | 6.580 | 20 | 200 | fits | 112,730 | 43 | 0.725 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 110,327 | 1.103 | 20 | 20 | fits | 112,944 | 134 | 0.519 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 821,724 | 8.217 | 20 | 20 | fits | 68,724 | 25 | 0.732 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 113,912 | 1.139 | 20 | 24 | fits | 112,944 | 134 | 0.519 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,481,074 | 64.811 | 20 | 24 | MISS ceiling | 29,461 | 23 | 0.556 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 112,872 | 1.129 | 20 | 50 | fits | 112,944 | 134 | 0.519 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 543,753 | 5.438 | 20 | 50 | fits | 140,962 | 91 | 0.642 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 242,386 | 2.424 | 18 | 18 | fits | 129,969 | 102 | 0.705 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,318,573 | 13.186 | 18 | 18 | fits | 45,473 | 21 | 0.653 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
