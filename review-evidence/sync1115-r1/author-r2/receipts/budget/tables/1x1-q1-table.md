### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 12 paths and 0 of 254 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.195 (0.630) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 3.970 (5.436) | fits | 7 adp | 23 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 3.555 | fits | 0 acmp | 23 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 4.538 | fits | 11 acmp | 23 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 3.545 | fits | 0 adp | 23 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.531 | fits | 7 adp | 23 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.118 | fits | 0 aecp | 23 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.aecp.last.if0` (backlog-adp@blank-0) | 3.581 | fits | 15 aecp | 23 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 3.581 | fits | 0 maap | 23 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.568 | fits | 6 maap | 23 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 5.773 | fits | 0 srp | 23 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-2.service.srp.last.if0` (backlog-adp@program-aged2-2) | 10.791 | fits | 31 srp | 23 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.837 | 11 | 151,219 (1.512) | yes | - |
| backlog-adp@blank-2 | 0 | 11.282 | 11 | 150,857 (1.509) | yes | - |
| backlog-adp@blank-4 | 0 | 11.591 | 13 | 151,023 (1.510) | yes | - |
| backlog-adp@blank-6 | 0 | 11.324 | 11 | 150,996 (1.510) | yes | - |
| backlog-adp@program-0 | 0 | 11.329 | 11 | 151,519 (1.515) | yes | - |
| backlog-adp@program-2 | 0 | 11.388 | 11 | 151,077 (1.511) | yes | - |
| backlog-adp@program-4 | 0 | 10.616 | 11 | 151,991 (1.520) | yes | - |
| backlog-adp@program-6 | 0 | 10.527 | 11 | 151,093 (1.511) | yes | - |
| backlog-adp@verify-0 | 0 | 11.651 | 11 | 151,683 (1.517) | yes | - |
| backlog-adp@verify-2 | 0 | 11.229 | 11 | 151,230 (1.512) | yes | - |
| backlog-adp@verify-4 | 0 | 11.455 | 12 | 151,378 (1.514) | yes | - |
| backlog-adp@verify-6 | 0 | 11.327 | 11 | 151,138 (1.511) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 11.843 | 12 | 151,801 (1.518) | yes | - |
| backlog-adp@blank-aged2-2 | 1 | 11.207 | 10 | 149,918 (1.499) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.186 | 10 | 151,427 (1.514) | yes | - |
| backlog-adp@blank-aged2-6 | 1 | 11.658 | 12 | 151,514 (1.515) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.088 | 13 | 148,695 (1.487) | yes | - |
| backlog-adp@blank-aged1-2 | 1 | 12.386 | 14 | 148,786 (1.488) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.920 | 12 | 149,983 (1.500) | yes | - |
| backlog-adp@blank-aged1-6 | 1 | 11.918 | 11 | 150,059 (1.501) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.403 | 13 | 150,931 (1.509) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.322 | 11 | 150,649 (1.506) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.319 | 11 | 150,602 (1.506) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3608 | 0 | 41,099 (0.411) | fits |
| backlog-adp@blank-0 | 416 | 0 | 151,219 (1.512) | fits |
| backlog-adp@blank-2 | 416 | 0 | 150,857 (1.509) | fits |
| backlog-adp@blank-4 | 418 | 0 | 151,023 (1.510) | fits |
| backlog-adp@blank-6 | 418 | 0 | 150,996 (1.510) | fits |
| backlog-adp@program-0 | 519 | 0 | 151,519 (1.515) | fits |
| backlog-adp@program-2 | 521 | 0 | 151,077 (1.511) | fits |
| backlog-adp@program-4 | 522 | 0 | 151,991 (1.520) | fits |
| backlog-adp@program-6 | 524 | 0 | 151,093 (1.511) | fits |
| backlog-adp@verify-0 | 614 | 0 | 151,683 (1.517) | fits |
| backlog-adp@verify-2 | 614 | 0 | 151,230 (1.512) | fits |
| backlog-adp@verify-4 | 615 | 0 | 151,378 (1.514) | fits |
| backlog-adp@verify-6 | 616 | 0 | 151,138 (1.511) | fits |
| backlog-adp@blank-aged2-0 | 705 | 0 | 155,019 (1.550) | fits |
| backlog-adp@blank-aged2-2 | 716 | 0 | 151,696 (1.517) | fits |
| backlog-adp@blank-aged2-4 | 730 | 0 | 151,427 (1.514) | fits |
| backlog-adp@blank-aged2-6 | 747 | 0 | 151,514 (1.515) | fits |
| backlog-adp@blank-aged1-0 | 646 | 0 | 150,624 (1.506) | fits |
| backlog-adp@blank-aged1-2 | 662 | 0 | 150,577 (1.506) | fits |
| backlog-adp@blank-aged1-4 | 675 | 0 | 150,359 (1.504) | fits |
| backlog-adp@blank-aged1-6 | 689 | 0 | 150,406 (1.504) | fits |
| backlog-adp@program-aged2-0 | 804 | 0 | 150,931 (1.509) | fits |
| backlog-adp@program-aged2-2 | 817 | 0 | 150,649 (1.506) | fits |
| backlog-adp@program-aged2-4 | 832 | 0 | 150,602 (1.506) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.995 ms, 76,752 (0.768 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.957 (20) | 10.043 |
| backlog-adp@blank-aged2-2 | 2 | none | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.679 (20) | 9.321 |
| backlog-adp@blank-aged2-4 | 2 | none | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.658 (20) | 9.342 |
| backlog-adp@blank-aged2-6 | 2 | +4.170 ms, 76,923 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.667 (20) | 9.333 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.865 (20) | 10.135 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.631 (20) | 9.369 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.638 (20) | 9.362 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.635 (20) | 9.365 |
| backlog-adp@program-aged2-0 | 2 | none | +10.260 ms, 80,158 (0.802 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.877 (20) | 10.123 |
| backlog-adp@program-aged2-2 | 2 | +8.290 ms, 80,587 (0.806 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.791 (20) | 9.209 |
| backlog-adp@program-aged2-4 | 2 | +5.824 ms, 80,587 (0.806 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.790 (20) | 9.210 |

Least margin over the aged windows: 9.209 ms, `backlog-adp@program-aged2-2.service.srp.last.if0` at 10.791 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 97,377 (0.974) | 78,248 (0.782) |
| backlog-adp@blank-0 | 299 | 92,285 (0.923) | 76,347 (0.763) |
| backlog-adp@blank-2 | 299 | 92,402 (0.924) | 76,302 (0.763) |
| backlog-adp@blank-4 | 299 | 91,206 (0.912) | 76,204 (0.762) |
| backlog-adp@blank-6 | 299 | 91,973 (0.920) | 76,254 (0.763) |
| backlog-adp@program-0 | 328 | 97,240 (0.972) | 78,936 (0.789) |
| backlog-adp@program-2 | 328 | 97,240 (0.972) | 78,891 (0.789) |
| backlog-adp@program-4 | 329 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@program-6 | 329 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-0 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-2 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-4 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-6 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@blank-aged2-0 | 297 | 76,752 (0.768) | 75,703 (0.757) |
| backlog-adp@blank-aged2-2 | 297 | 85,711 (0.857) | 75,956 (0.760) |
| backlog-adp@blank-aged2-4 | 297 | 85,735 (0.857) | 75,956 (0.760) |
| backlog-adp@blank-aged2-6 | 297 | 76,923 (0.769) | 75,579 (0.756) |
| backlog-adp@blank-aged1-0 | 297 | 97,635 (0.976) | 76,049 (0.760) |
| backlog-adp@blank-aged1-2 | 297 | 92,754 (0.928) | 76,255 (0.763) |
| backlog-adp@blank-aged1-4 | 297 | 92,100 (0.921) | 76,255 (0.763) |
| backlog-adp@blank-aged1-6 | 297 | 92,109 (0.921) | 76,255 (0.763) |
| backlog-adp@program-aged2-0 | 326 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@program-aged2-2 | 326 | 97,240 (0.972) | 78,467 (0.785) |
| backlog-adp@program-aged2-4 | 326 | 97,240 (0.972) | 78,467 (0.785) |

Longest pass that carries a step: 97,635 CPU cycles (0.976 ms), backlog-adp@blank-aged1-0; longest step: 78,936 (0.789 ms), backlog-adp@program-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 19,526 | 0.195 | 20 | 20 | fits | 34,487 | 19 (14) | 0.890 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 396,953 | 3.970 | 20 | 20 | fits | 99,159 | 142 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 354,544 | 3.545 | 20 | 200 | fits | 147,295 | 248 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 453,087 | 4.531 | 20 | 200 | fits | 99,159 | 142 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 355,468 | 3.555 | 20 | 20 | fits | 147,295 | 248 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 453,791 | 4.538 | 20 | 20 | fits | 99,159 | 142 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 211,813 | 2.118 | 20 | 24 | fits | 151,219 | 155 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 358,118 | 3.581 | 20 | 24 | fits | 147,295 | 248 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 358,052 | 3.581 | 20 | 50 | fits | 147,295 | 248 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 456,815 | 4.568 | 20 | 50 | fits | 99,159 | 142 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 543,196 | 5.432 | 20 | 20 | fits | 86,447 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,055,144 | 10.551 | 20 | 20 | fits | 79,240 | 30 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 333,961 | 3.340 | 20 | 20 | fits | 97,544 | 151 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 299,758 | 2.998 | 20 | 200 | fits | 149,982 | 237 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 396,686 | 3.967 | 20 | 200 | fits | 97,544 | 151 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 300,682 | 3.007 | 20 | 20 | fits | 149,982 | 237 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 397,390 | 3.974 | 20 | 20 | fits | 97,544 | 151 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 154,340 | 1.543 | 20 | 24 | fits | 150,857 | 155 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 303,332 | 3.033 | 20 | 24 | fits | 149,982 | 237 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 303,266 | 3.033 | 20 | 50 | fits | 149,982 | 237 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 400,414 | 4.004 | 20 | 50 | fits | 97,544 | 151 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 478,052 | 4.781 | 20 | 20 | fits | 77,704 | 27 | 0.819 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 999,568 | 9.996 | 20 | 20 | fits | 86,207 | 28 | 0.636 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 357,944 | 3.579 | 20 | 20 | fits | 104,079 | 160 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 311,842 | 3.118 | 20 | 200 | fits | 146,447 | 235 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 415,305 | 4.153 | 20 | 200 | fits | 104,079 | 160 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 312,766 | 3.128 | 20 | 20 | fits | 146,447 | 235 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 416,009 | 4.160 | 20 | 20 | fits | 104,079 | 160 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 161,338 | 1.613 | 20 | 24 | fits | 151,023 | 156 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 315,416 | 3.154 | 20 | 24 | fits | 146,447 | 235 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 315,350 | 3.154 | 20 | 50 | fits | 146,447 | 235 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 419,033 | 4.190 | 20 | 50 | fits | 104,079 | 160 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 505,378 | 5.054 | 20 | 20 | fits | 86,411 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,001,581 | 10.016 | 20 | 20 | fits | 73,603 | 25 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 358,045 | 3.580 | 20 | 20 | fits | 104,123 | 157 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 304,922 | 3.049 | 20 | 200 | fits | 150,043 | 237 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 408,429 | 4.084 | 20 | 200 | fits | 104,123 | 157 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 305,846 | 3.058 | 20 | 20 | fits | 150,043 | 237 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 409,133 | 4.091 | 20 | 20 | fits | 104,123 | 157 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 159,443 | 1.594 | 20 | 24 | fits | 150,996 | 155 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 308,496 | 3.085 | 20 | 24 | fits | 150,043 | 237 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 308,430 | 3.084 | 20 | 50 | fits | 150,043 | 237 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 412,157 | 4.122 | 20 | 50 | fits | 104,123 | 157 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 498,639 | 4.986 | 20 | 20 | fits | 86,548 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,004,376 | 10.044 | 20 | 20 | fits | 73,747 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 337,566 | 3.376 | 20 | 20 | fits | 97,917 | 152 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 303,433 | 3.034 | 20 | 200 | fits | 150,079 | 237 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 400,734 | 4.007 | 20 | 200 | fits | 97,917 | 152 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 304,357 | 3.044 | 20 | 20 | fits | 150,079 | 237 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 401,438 | 4.014 | 20 | 20 | fits | 97,917 | 152 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 157,918 | 1.579 | 20 | 24 | fits | 151,519 | 155 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 307,007 | 3.070 | 20 | 24 | fits | 150,079 | 237 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 306,941 | 3.069 | 20 | 50 | fits | 150,079 | 237 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 404,462 | 4.045 | 20 | 50 | fits | 97,917 | 152 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 503,133 | 5.031 | 20 | 20 | fits | 89,437 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 999,223 | 9.992 | 20 | 20 | fits | 66,736 | 26 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 354,832 | 3.548 | 20 | 20 | fits | 96,386 | 151 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 309,085 | 3.091 | 20 | 200 | fits | 149,988 | 237 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 404,855 | 4.049 | 20 | 200 | fits | 96,386 | 151 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 310,009 | 3.100 | 20 | 20 | fits | 149,988 | 237 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 405,559 | 4.056 | 20 | 20 | fits | 96,386 | 151 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 163,661 | 1.637 | 20 | 24 | fits | 151,077 | 155 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 312,659 | 3.127 | 20 | 24 | fits | 149,988 | 237 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 312,593 | 3.126 | 20 | 50 | fits | 149,988 | 237 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 408,583 | 4.086 | 20 | 50 | fits | 96,386 | 151 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 499,409 | 4.994 | 20 | 20 | fits | 90,892 | 30 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,005,363 | 10.054 | 20 | 20 | fits | 73,795 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 368,131 | 3.681 | 20 | 20 | fits | 102,083 | 161 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 307,250 | 3.072 | 20 | 200 | fits | 149,156 | 234 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 417,807 | 4.178 | 20 | 200 | fits | 102,083 | 161 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 308,174 | 3.082 | 20 | 20 | fits | 149,156 | 234 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 418,511 | 4.185 | 20 | 20 | fits | 102,083 | 161 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 162,658 | 1.627 | 20 | 24 | fits | 151,991 | 155 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 310,824 | 3.108 | 20 | 24 | fits | 149,156 | 234 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 310,758 | 3.108 | 20 | 50 | fits | 149,156 | 234 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 421,535 | 4.215 | 20 | 50 | fits | 102,083 | 161 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 507,526 | 5.075 | 20 | 20 | fits | 86,057 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,003,597 | 10.036 | 20 | 20 | fits | 66,815 | 26 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 343,990 | 3.440 | 20 | 20 | fits | 97,229 | 154 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 296,165 | 2.962 | 20 | 200 | fits | 148,756 | 233 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 392,778 | 3.928 | 20 | 200 | fits | 97,229 | 154 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 297,089 | 2.971 | 20 | 20 | fits | 148,756 | 233 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 393,482 | 3.935 | 20 | 20 | fits | 97,229 | 154 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 151,973 | 1.520 | 20 | 24 | fits | 151,093 | 155 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 299,739 | 2.997 | 20 | 24 | fits | 148,756 | 233 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 299,673 | 2.997 | 20 | 50 | fits | 148,756 | 233 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 396,506 | 3.965 | 20 | 50 | fits | 97,229 | 154 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 487,559 | 4.876 | 20 | 20 | fits | 91,119 | 30 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 995,095 | 9.951 | 20 | 20 | fits | 73,765 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 384,327 | 3.843 | 20 | 20 | fits | 96,386 | 151 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 338,580 | 3.386 | 20 | 200 | fits | 150,206 | 237 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 434,350 | 4.343 | 20 | 200 | fits | 96,386 | 151 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 339,504 | 3.395 | 20 | 20 | fits | 150,206 | 237 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 435,054 | 4.351 | 20 | 20 | fits | 96,386 | 151 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 192,938 | 1.929 | 20 | 24 | fits | 151,683 | 155 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 342,154 | 3.422 | 20 | 24 | fits | 150,206 | 237 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 342,088 | 3.421 | 20 | 50 | fits | 150,206 | 237 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 438,078 | 4.381 | 20 | 50 | fits | 96,386 | 151 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 524,023 | 5.240 | 20 | 20 | fits | 86,011 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,035,830 | 10.358 | 20 | 20 | fits | 79,240 | 30 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 337,779 | 3.378 | 20 | 20 | fits | 100,610 | 143 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 294,825 | 2.948 | 20 | 200 | fits | 147,424 | 248 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 394,819 | 3.948 | 20 | 200 | fits | 100,610 | 143 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 295,749 | 2.957 | 20 | 20 | fits | 147,424 | 248 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 395,523 | 3.955 | 20 | 20 | fits | 100,610 | 143 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 151,965 | 1.520 | 20 | 24 | fits | 151,230 | 155 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 298,399 | 2.984 | 20 | 24 | fits | 147,424 | 248 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 298,333 | 2.983 | 20 | 50 | fits | 147,424 | 248 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 398,547 | 3.985 | 20 | 50 | fits | 100,610 | 143 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 497,468 | 4.975 | 20 | 20 | fits | 89,687 | 31 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 993,811 | 9.938 | 20 | 20 | fits | 73,648 | 24 | 0.673 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 343,908 | 3.439 | 20 | 20 | fits | 104,496 | 160 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 309,975 | 3.100 | 20 | 200 | fits | 146,457 | 235 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 413,855 | 4.139 | 20 | 200 | fits | 104,496 | 160 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 310,899 | 3.109 | 20 | 20 | fits | 146,457 | 235 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 414,559 | 4.146 | 20 | 20 | fits | 104,496 | 160 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 159,537 | 1.595 | 20 | 24 | fits | 151,378 | 156 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 313,549 | 3.135 | 20 | 24 | fits | 146,457 | 235 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 313,483 | 3.135 | 20 | 50 | fits | 146,457 | 235 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 417,583 | 4.176 | 20 | 50 | fits | 104,496 | 160 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 503,664 | 5.037 | 20 | 20 | fits | 86,147 | 24 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,003,739 | 10.037 | 20 | 20 | fits | 77,614 | 31 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 345,284 | 3.453 | 20 | 20 | fits | 105,186 | 157 | 0.476 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 303,744 | 3.037 | 20 | 200 | fits | 150,053 | 237 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 408,314 | 4.083 | 20 | 200 | fits | 105,186 | 157 | 0.476 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 304,668 | 3.047 | 20 | 20 | fits | 150,053 | 237 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 409,018 | 4.090 | 20 | 20 | fits | 105,186 | 157 | 0.476 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 158,255 | 1.583 | 20 | 24 | fits | 151,138 | 155 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 307,318 | 3.073 | 20 | 24 | fits | 150,053 | 237 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 307,252 | 3.073 | 20 | 50 | fits | 150,053 | 237 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 412,042 | 4.120 | 20 | 50 | fits | 105,186 | 157 | 0.476 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 498,070 | 4.981 | 20 | 20 | fits | 86,094 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,003,825 | 10.038 | 20 | 20 | fits | 73,795 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 347,254 | 3.473 | 20 | 20 | fits | 102,259 | 157 | 0.480 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 299,339 | 2.993 | 20 | 200 | fits | 151,801 | 243 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 410,689 | 4.107 | 20 | 200 | fits | 102,259 | 157 | 0.480 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 300,263 | 3.003 | 20 | 20 | fits | 151,801 | 243 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 411,393 | 4.114 | 20 | 20 | fits | 102,259 | 157 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 152,102 | 1.521 | 20 | 24 | fits | 155,019 | 157 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 302,913 | 3.029 | 20 | 24 | fits | 151,801 | 243 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 302,847 | 3.028 | 20 | 50 | fits | 151,801 | 243 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 414,417 | 4.144 | 20 | 50 | fits | 102,259 | 157 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 500,211 | 5.002 | 20 | 20 | fits | 85,860 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 995,732 | 9.957 | 20 | 20 | fits | 66,693 | 26 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 342,331 | 3.423 | 20 | 20 | fits | 100,230 | 160 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 291,726 | 2.917 | 20 | 200 | fits | 149,918 | 238 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 391,340 | 3.913 | 20 | 200 | fits | 100,230 | 160 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 292,650 | 2.926 | 20 | 20 | fits | 149,918 | 238 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 392,044 | 3.920 | 20 | 20 | fits | 100,230 | 160 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 146,372 | 1.464 | 20 | 24 | fits | 151,696 | 157 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 295,300 | 2.953 | 20 | 24 | fits | 149,918 | 238 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 295,234 | 2.952 | 20 | 50 | fits | 149,918 | 238 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 395,068 | 3.951 | 20 | 50 | fits | 100,230 | 160 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 480,889 | 4.809 | 20 | 20 | fits | 85,887 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,067,905 | 10.679 | 20 | 20 | fits | 86,579 | 28 | 0.647 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 339,649 | 3.396 | 20 | 20 | fits | 96,273 | 151 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 293,934 | 2.939 | 20 | 200 | fits | 151,427 | 242 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 389,591 | 3.896 | 20 | 200 | fits | 96,273 | 151 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 294,858 | 2.949 | 20 | 20 | fits | 151,427 | 242 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 390,295 | 3.903 | 20 | 20 | fits | 96,273 | 151 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 147,071 | 1.471 | 20 | 24 | fits | 150,622 | 152 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 297,508 | 2.975 | 20 | 24 | fits | 151,427 | 242 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 297,442 | 2.974 | 20 | 50 | fits | 151,427 | 242 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 393,319 | 3.933 | 20 | 50 | fits | 96,273 | 151 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 478,747 | 4.787 | 20 | 20 | fits | 85,494 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,065,771 | 10.658 | 20 | 20 | fits | 86,159 | 28 | 0.636 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 360,874 | 3.609 | 20 | 20 | fits | 107,921 | 163 | 0.479 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 295,479 | 2.955 | 20 | 200 | fits | 151,514 | 243 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 411,657 | 4.117 | 20 | 200 | fits | 107,921 | 163 | 0.479 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 296,403 | 2.964 | 20 | 20 | fits | 151,514 | 243 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 412,361 | 4.124 | 20 | 20 | fits | 107,921 | 163 | 0.479 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 148,529 | 1.485 | 20 | 24 | fits | 150,575 | 152 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 299,053 | 2.991 | 20 | 24 | fits | 151,514 | 243 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 298,987 | 2.990 | 20 | 50 | fits | 151,514 | 243 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 415,385 | 4.154 | 20 | 50 | fits | 107,921 | 163 | 0.479 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 577,348 | 5.773 | 20 | 20 | fits | 85,106 | 25 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,066,747 | 10.667 | 20 | 20 | fits | 60,423 | 20 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 333,866 | 3.339 | 20 | 20 | fits | 99,179 | 142 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 291,387 | 2.914 | 20 | 200 | fits | 148,695 | 253 | 0.366 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 389,950 | 3.900 | 20 | 200 | fits | 99,179 | 142 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 292,311 | 2.923 | 20 | 20 | fits | 148,695 | 253 | 0.366 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 390,654 | 3.907 | 20 | 20 | fits | 99,179 | 142 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 147,256 | 1.473 | 20 | 24 | fits | 150,624 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 294,961 | 2.950 | 20 | 24 | fits | 148,695 | 253 | 0.366 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 294,895 | 2.949 | 20 | 50 | fits | 148,695 | 253 | 0.366 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 393,678 | 3.937 | 20 | 50 | fits | 99,179 | 142 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 479,997 | 4.800 | 20 | 20 | fits | 86,385 | 25 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 986,479 | 9.865 | 20 | 20 | fits | 73,764 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 348,344 | 3.483 | 20 | 20 | fits | 103,962 | 148 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 292,745 | 2.927 | 20 | 200 | fits | 148,786 | 254 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 405,230 | 4.052 | 20 | 200 | fits | 103,962 | 148 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 293,669 | 2.937 | 20 | 20 | fits | 148,786 | 254 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 405,934 | 4.059 | 20 | 20 | fits | 103,962 | 148 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 148,523 | 1.485 | 20 | 24 | fits | 150,577 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 296,319 | 2.963 | 20 | 24 | fits | 148,786 | 254 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 296,253 | 2.963 | 20 | 50 | fits | 148,786 | 254 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 408,958 | 4.090 | 20 | 50 | fits | 103,962 | 148 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 495,305 | 4.953 | 20 | 20 | fits | 86,413 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,063,108 | 10.631 | 20 | 20 | fits | 75,076 | 25 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 340,453 | 3.405 | 20 | 20 | fits | 96,925 | 154 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 292,728 | 2.927 | 20 | 200 | fits | 149,983 | 238 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 389,037 | 3.890 | 20 | 200 | fits | 96,925 | 154 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 293,652 | 2.937 | 20 | 20 | fits | 149,983 | 238 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 389,741 | 3.897 | 20 | 20 | fits | 96,925 | 154 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 147,309 | 1.473 | 20 | 24 | fits | 150,359 | 152 | 0.346 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 296,302 | 2.963 | 20 | 24 | fits | 149,983 | 238 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 296,236 | 2.962 | 20 | 50 | fits | 149,983 | 238 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 392,765 | 3.928 | 20 | 50 | fits | 96,925 | 154 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 479,076 | 4.791 | 20 | 20 | fits | 86,377 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,063,782 | 10.638 | 20 | 20 | fits | 86,573 | 28 | 0.652 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 355,849 | 3.558 | 20 | 20 | fits | 113,323 | 160 | 0.495 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 293,855 | 2.939 | 20 | 200 | fits | 150,059 | 238 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 406,562 | 4.066 | 20 | 200 | fits | 113,323 | 160 | 0.495 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 294,779 | 2.948 | 20 | 20 | fits | 150,059 | 238 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 407,266 | 4.073 | 20 | 20 | fits | 113,323 | 160 | 0.495 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 148,360 | 1.484 | 20 | 24 | fits | 150,406 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 297,429 | 2.974 | 20 | 24 | fits | 150,059 | 238 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 297,363 | 2.974 | 20 | 50 | fits | 150,059 | 238 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 410,290 | 4.103 | 20 | 50 | fits | 113,323 | 160 | 0.495 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 525,530 | 5.255 | 20 | 20 | fits | 86,068 | 26 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,063,470 | 10.635 | 20 | 20 | fits | 73,897 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 351,826 | 3.518 | 20 | 20 | fits | 100,103 | 142 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 308,888 | 3.089 | 20 | 200 | fits | 149,606 | 253 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 408,375 | 4.084 | 20 | 200 | fits | 100,103 | 142 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 309,812 | 3.098 | 20 | 20 | fits | 149,606 | 253 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 409,079 | 4.091 | 20 | 20 | fits | 100,103 | 142 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 155,285 | 1.553 | 20 | 24 | fits | 150,931 | 153 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 312,462 | 3.125 | 20 | 24 | fits | 149,606 | 253 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 312,396 | 3.124 | 20 | 50 | fits | 149,606 | 253 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 412,103 | 4.121 | 20 | 50 | fits | 100,103 | 142 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 498,078 | 4.981 | 20 | 20 | fits | 86,041 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 987,678 | 9.877 | 20 | 20 | fits | 60,509 | 21 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 340,538 | 3.405 | 20 | 20 | fits | 99,273 | 142 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 298,007 | 2.980 | 20 | 200 | fits | 147,392 | 248 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 396,664 | 3.967 | 20 | 200 | fits | 99,273 | 142 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 298,931 | 2.989 | 20 | 20 | fits | 147,392 | 248 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 397,368 | 3.974 | 20 | 20 | fits | 99,273 | 142 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 155,179 | 1.552 | 20 | 24 | fits | 150,649 | 152 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 301,581 | 3.016 | 20 | 24 | fits | 147,392 | 248 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 301,515 | 3.015 | 20 | 50 | fits | 147,392 | 248 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 400,392 | 4.004 | 20 | 50 | fits | 99,273 | 142 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 486,314 | 4.863 | 20 | 20 | fits | 85,988 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,079,060 | 10.791 | 20 | 20 | fits | 86,517 | 28 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 342,355 | 3.424 | 20 | 20 | fits | 99,674 | 143 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 299,824 | 2.998 | 20 | 200 | fits | 147,316 | 248 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 398,882 | 3.989 | 20 | 200 | fits | 99,674 | 143 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 300,748 | 3.007 | 20 | 20 | fits | 147,316 | 248 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 399,586 | 3.996 | 20 | 20 | fits | 99,674 | 143 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 157,072 | 1.571 | 20 | 24 | fits | 150,602 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 303,398 | 3.034 | 20 | 24 | fits | 147,316 | 248 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 303,332 | 3.033 | 20 | 50 | fits | 147,316 | 248 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 402,610 | 4.026 | 20 | 50 | fits | 99,674 | 143 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 501,229 | 5.012 | 20 | 20 | fits | 89,624 | 31 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,078,950 | 10.790 | 20 | 20 | fits | 73,812 | 24 | 0.682 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
