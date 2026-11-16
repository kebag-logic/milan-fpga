### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 253 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged2-7.adp_available.if0` (backlog-adp@blank-aged2-7) | 4.385 (5.106) | fits | 7 adp | 23 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-5.service.acmp.first.if0` (backlog-adp@blank-5) | 3.194 | fits | 0 acmp | 23 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.acmp.last.if0` (backlog-adp@blank-aged2-7) | 4.968 | fits | 11 acmp | 23 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-5.service.adp.first.if0` (backlog-adp@blank-5) | 3.185 | fits | 0 adp | 23 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.adp.last.if0` (backlog-adp@blank-aged2-7) | 4.961 | fits | 7 adp | 23 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.aecp.first.if0` (backlog-adp@verify-5) | 1.681 | fits | 0 aecp | 23 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-5.service.aecp.last.if0` (backlog-adp@blank-5) | 3.221 | fits | 15 aecp | 23 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-5.service.maap.first.if0` (backlog-adp@blank-5) | 3.220 | fits | 0 maap | 23 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.maap.last.if0` (backlog-adp@blank-aged2-7) | 4.998 | fits | 6 maap | 23 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-7.service.srp.first.if0` (backlog-adp@blank-aged2-7) | 5.854 | fits | 0 srp | 23 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-1.service.srp.last.if0` (backlog-adp@program-aged2-1) | 10.858 | fits | 31 srp | 23 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-1 | 0 | 11.224 | 11 | 150,857 (1.509) | yes | - |
| backlog-adp@blank-3 | 0 | 11.743 | 13 | 150,857 (1.509) | yes | - |
| backlog-adp@blank-5 | 0 | 11.477 | 12 | 150,924 (1.509) | yes | - |
| backlog-adp@blank-7 | 0 | 13.217 | 14 | 150,996 (1.510) | yes | - |
| backlog-adp@program-1 | 0 | 11.553 | 12 | 151,676 (1.517) | yes | - |
| backlog-adp@program-3 | 0 | 11.323 | 11 | 151,138 (1.511) | yes | - |
| backlog-adp@program-5 | 0 | 10.614 | 11 | 151,060 (1.511) | yes | - |
| backlog-adp@program-7 | 0 | 11.147 | 13 | 151,093 (1.511) | yes | - |
| backlog-adp@verify-1 | 0 | 11.364 | 11 | 151,263 (1.513) | yes | - |
| backlog-adp@verify-3 | 0 | 11.723 | 13 | 151,230 (1.512) | yes | - |
| backlog-adp@verify-5 | 0 | 11.429 | 11 | 151,343 (1.513) | yes | - |
| backlog-adp@verify-7 | 0 | 12.454 | 12 | 151,138 (1.511) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.385 | 12 | 150,846 (1.508) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.277 | 11 | 150,575 (1.506) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.270 | 11 | 150,622 (1.506) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.684 | 14 | 150,575 (1.506) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.481 | 15 | 150,624 (1.506) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.128 | 14 | 152,213 (1.522) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 12.022 | 13 | 150,359 (1.504) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.524 | 15 | 152,323 (1.523) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.390 | 11 | 150,602 (1.506) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.273 | 10 | 151,428 (1.514) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 11.426 | 11 | 151,667 (1.517) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 45182 | 0 | 49,833 (0.498) | fits |
| backlog-adp@blank-1 | 416 | 0 | 150,857 (1.509) | fits |
| backlog-adp@blank-3 | 418 | 0 | 150,857 (1.509) | fits |
| backlog-adp@blank-5 | 417 | 0 | 150,924 (1.509) | fits |
| backlog-adp@blank-7 | 421 | 0 | 150,996 (1.510) | fits |
| backlog-adp@program-1 | 520 | 0 | 151,676 (1.517) | fits |
| backlog-adp@program-3 | 521 | 0 | 151,138 (1.511) | fits |
| backlog-adp@program-5 | 524 | 0 | 151,060 (1.511) | fits |
| backlog-adp@program-7 | 526 | 0 | 151,093 (1.511) | fits |
| backlog-adp@verify-1 | 614 | 0 | 151,263 (1.513) | fits |
| backlog-adp@verify-3 | 616 | 0 | 151,230 (1.512) | fits |
| backlog-adp@verify-5 | 615 | 0 | 151,343 (1.513) | fits |
| backlog-adp@verify-7 | 617 | 0 | 151,138 (1.511) | fits |
| backlog-adp@blank-aged2-1 | 709 | 0 | 150,846 (1.508) | fits |
| backlog-adp@blank-aged2-3 | 723 | 0 | 150,575 (1.506) | fits |
| backlog-adp@blank-aged2-5 | 738 | 0 | 150,622 (1.506) | fits |
| backlog-adp@blank-aged2-7 | 756 | 0 | 150,575 (1.506) | fits |
| backlog-adp@blank-aged1-1 | 655 | 0 | 150,624 (1.506) | fits |
| backlog-adp@blank-aged1-3 | 669 | 0 | 152,213 (1.522) | fits |
| backlog-adp@blank-aged1-5 | 683 | 0 | 150,359 (1.504) | fits |
| backlog-adp@blank-aged1-7 | 700 | 0 | 152,323 (1.523) | fits |
| backlog-adp@program-aged2-1 | 810 | 0 | 150,602 (1.506) | fits |
| backlog-adp@program-aged2-3 | 824 | 0 | 151,428 (1.514) | fits |
| backlog-adp@program-aged2-5 | 840 | 0 | 151,667 (1.517) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-1 | 2 | none | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.854 (20) | 9.146 |
| backlog-adp@blank-aged2-3 | 2 | +6.531 ms, 76,752 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.748 (20) | 9.252 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.743 (20) | 9.257 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.746 (20) | 9.254 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.376 (20) | 9.624 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.847 (20) | 9.153 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.740 (20) | 9.260 |
| backlog-adp@blank-aged1-7 | 1 | none | +10.954 ms, 76,554 (0.766 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.714 (20) | 9.286 |
| backlog-adp@program-aged2-1 | 2 | +9.223 ms, 80,587 (0.806 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.858 (20) | 9.142 |
| backlog-adp@program-aged2-3 | 2 | +6.513 ms, 80,587 (0.806 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.741 (20) | 9.259 |
| backlog-adp@program-aged2-5 | 2 | +4.185 ms, 80,394 (0.804 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.770 (20) | 9.230 |

Least margin over the aged windows: 9.142 ms, `backlog-adp@program-aged2-1.service.srp.last.if0` at 10.858 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.388 | 6,070 | 102 | 2 | 30.862 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 520 | 80,088 (0.801) | 77,700 (0.777) |
| backlog-adp@blank-1 | 299 | 92,207 (0.922) | 76,302 (0.763) |
| backlog-adp@blank-3 | 299 | 92,426 (0.924) | 76,302 (0.763) |
| backlog-adp@blank-5 | 299 | 94,904 (0.949) | 76,361 (0.764) |
| backlog-adp@blank-7 | 300 | 97,074 (0.971) | 76,254 (0.763) |
| backlog-adp@program-1 | 328 | 98,599 (0.986) | 78,822 (0.788) |
| backlog-adp@program-3 | 328 | 97,240 (0.972) | 78,891 (0.789) |
| backlog-adp@program-5 | 329 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@program-7 | 329 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-1 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-3 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-5 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-7 | 356 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@blank-aged2-1 | 297 | 85,829 (0.858) | 75,956 (0.760) |
| backlog-adp@blank-aged2-3 | 297 | 76,752 (0.768) | 75,703 (0.757) |
| backlog-adp@blank-aged2-5 | 297 | 85,780 (0.858) | 75,956 (0.760) |
| backlog-adp@blank-aged2-7 | 298 | 91,760 (0.918) | 76,104 (0.761) |
| backlog-adp@blank-aged1-1 | 297 | 97,853 (0.979) | 76,156 (0.762) |
| backlog-adp@blank-aged1-3 | 297 | 92,041 (0.920) | 76,255 (0.763) |
| backlog-adp@blank-aged1-5 | 297 | 92,100 (0.921) | 76,255 (0.763) |
| backlog-adp@blank-aged1-7 | 297 | 76,554 (0.766) | 75,587 (0.756) |
| backlog-adp@program-aged2-1 | 326 | 97,240 (0.972) | 78,467 (0.785) |
| backlog-adp@program-aged2-3 | 326 | 97,240 (0.972) | 78,467 (0.785) |
| backlog-adp@program-aged2-5 | 326 | 97,240 (0.972) | 78,381 (0.784) |

Longest pass that carries a step: 98,599 CPU cycles (0.986 ms), backlog-adp@program-1; longest step: 78,891 (0.789 ms), backlog-adp@program-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 342,914 | 3.429 | 20 | 20 | fits | 97,135 | 154 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 295,141 | 2.951 | 20 | 200 | fits | 148,781 | 233 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 391,660 | 3.917 | 20 | 200 | fits | 97,135 | 154 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 296,065 | 2.961 | 20 | 20 | fits | 148,781 | 233 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 392,364 | 3.924 | 20 | 20 | fits | 97,135 | 154 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 150,924 | 1.509 | 20 | 24 | fits | 150,857 | 155 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 298,715 | 2.987 | 20 | 24 | fits | 148,781 | 233 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 298,649 | 2.986 | 20 | 50 | fits | 148,781 | 233 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 395,388 | 3.954 | 20 | 50 | fits | 97,135 | 154 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 481,836 | 4.818 | 20 | 20 | fits | 86,514 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 993,950 | 9.940 | 20 | 20 | fits | 86,485 | 28 | 0.643 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 356,381 | 3.564 | 20 | 20 | fits | 104,298 | 149 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 300,650 | 3.006 | 20 | 200 | fits | 147,458 | 249 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 413,403 | 4.134 | 20 | 200 | fits | 104,298 | 149 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 301,574 | 3.016 | 20 | 20 | fits | 147,458 | 249 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 414,107 | 4.141 | 20 | 20 | fits | 104,298 | 149 | 0.458 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 157,756 | 1.578 | 20 | 24 | fits | 150,857 | 155 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 304,224 | 3.042 | 20 | 24 | fits | 147,458 | 249 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 304,158 | 3.042 | 20 | 50 | fits | 147,458 | 249 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 417,131 | 4.171 | 20 | 50 | fits | 104,298 | 149 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 503,387 | 5.034 | 20 | 20 | fits | 86,322 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 999,691 | 9.997 | 20 | 20 | fits | 73,609 | 24 | 0.671 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 361,364 | 3.614 | 20 | 20 | fits | 100,069 | 142 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 318,478 | 3.185 | 20 | 200 | fits | 149,766 | 253 | 0.374 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 417,931 | 4.179 | 20 | 200 | fits | 100,069 | 142 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 319,402 | 3.194 | 20 | 20 | fits | 149,766 | 253 | 0.374 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 418,635 | 4.186 | 20 | 20 | fits | 100,069 | 142 | 0.431 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 164,655 | 1.647 | 20 | 24 | fits | 150,924 | 156 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 322,052 | 3.221 | 20 | 24 | fits | 149,766 | 253 | 0.374 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 321,986 | 3.220 | 20 | 50 | fits | 149,766 | 253 | 0.374 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 421,659 | 4.217 | 20 | 50 | fits | 100,069 | 142 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 499,964 | 5.000 | 20 | 20 | fits | 78,371 | 26 | 0.822 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,006,658 | 10.067 | 20 | 20 | fits | 77,653 | 31 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 353,993 | 3.540 | 20 | 20 | fits | 105,260 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 306,212 | 3.062 | 20 | 200 | fits | 147,917 | 231 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 410,856 | 4.109 | 20 | 200 | fits | 105,260 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 307,136 | 3.071 | 20 | 20 | fits | 147,917 | 231 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 411,560 | 4.116 | 20 | 20 | fits | 105,260 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 162,859 | 1.629 | 20 | 24 | fits | 150,996 | 155 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 309,786 | 3.098 | 20 | 24 | fits | 147,917 | 231 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 309,720 | 3.097 | 20 | 50 | fits | 147,917 | 231 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 414,584 | 4.146 | 20 | 50 | fits | 105,260 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 500,885 | 5.009 | 20 | 20 | fits | 86,367 | 24 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,007,300 | 10.073 | 20 | 20 | fits | 73,764 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 362,126 | 3.621 | 20 | 20 | fits | 104,137 | 160 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 315,948 | 3.159 | 20 | 200 | fits | 146,468 | 235 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 419,469 | 4.195 | 20 | 200 | fits | 104,137 | 160 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 316,872 | 3.169 | 20 | 20 | fits | 146,468 | 235 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 420,173 | 4.202 | 20 | 20 | fits | 104,137 | 160 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 165,499 | 1.655 | 20 | 24 | fits | 151,676 | 156 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 319,522 | 3.195 | 20 | 24 | fits | 146,468 | 235 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 319,456 | 3.195 | 20 | 50 | fits | 146,468 | 235 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 423,197 | 4.232 | 20 | 50 | fits | 104,137 | 160 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 509,063 | 5.091 | 20 | 20 | fits | 85,932 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,009,207 | 10.092 | 20 | 20 | fits | 77,614 | 31 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 352,725 | 3.527 | 20 | 20 | fits | 104,762 | 163 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 298,406 | 2.984 | 20 | 200 | fits | 148,468 | 231 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 402,552 | 4.026 | 20 | 200 | fits | 104,762 | 163 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 299,330 | 2.993 | 20 | 20 | fits | 148,468 | 231 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 403,256 | 4.033 | 20 | 20 | fits | 104,762 | 163 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 154,502 | 1.545 | 20 | 24 | fits | 151,138 | 155 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 301,980 | 3.020 | 20 | 24 | fits | 148,468 | 231 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 301,914 | 3.019 | 20 | 50 | fits | 148,468 | 231 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 406,280 | 4.063 | 20 | 50 | fits | 104,762 | 163 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 492,225 | 4.922 | 20 | 20 | fits | 86,011 | 25 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 998,829 | 9.988 | 20 | 20 | fits | 73,812 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 353,177 | 3.532 | 20 | 20 | fits | 97,229 | 154 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 305,352 | 3.054 | 20 | 200 | fits | 148,756 | 233 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 401,965 | 4.020 | 20 | 200 | fits | 97,229 | 154 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 306,276 | 3.063 | 20 | 20 | fits | 148,756 | 233 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 402,669 | 4.027 | 20 | 20 | fits | 97,229 | 154 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 161,160 | 1.612 | 20 | 24 | fits | 151,060 | 155 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 308,926 | 3.089 | 20 | 24 | fits | 148,756 | 233 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 308,860 | 3.089 | 20 | 50 | fits | 148,756 | 233 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 405,693 | 4.057 | 20 | 50 | fits | 97,229 | 154 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 491,791 | 4.918 | 20 | 20 | fits | 86,164 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,003,878 | 10.039 | 20 | 20 | fits | 86,449 | 28 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 363,172 | 3.632 | 20 | 20 | fits | 109,430 | 169 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 302,206 | 3.022 | 20 | 200 | fits | 147,965 | 232 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 420,236 | 4.202 | 20 | 200 | fits | 109,430 | 169 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 303,130 | 3.031 | 20 | 20 | fits | 147,965 | 232 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 420,940 | 4.209 | 20 | 20 | fits | 109,430 | 169 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 158,805 | 1.588 | 20 | 24 | fits | 151,093 | 155 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 305,780 | 3.058 | 20 | 24 | fits | 147,965 | 232 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 305,714 | 3.057 | 20 | 50 | fits | 147,965 | 232 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 423,964 | 4.240 | 20 | 50 | fits | 109,430 | 169 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 509,806 | 5.098 | 20 | 20 | fits | 85,908 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 999,313 | 9.993 | 20 | 20 | fits | 60,416 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 356,534 | 3.565 | 20 | 20 | fits | 97,229 | 154 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 308,709 | 3.087 | 20 | 200 | fits | 148,898 | 233 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 405,322 | 4.053 | 20 | 200 | fits | 97,229 | 154 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 309,633 | 3.096 | 20 | 20 | fits | 148,898 | 233 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 406,026 | 4.060 | 20 | 20 | fits | 97,229 | 154 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 164,375 | 1.644 | 20 | 24 | fits | 151,263 | 155 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 312,283 | 3.123 | 20 | 24 | fits | 148,898 | 233 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 312,217 | 3.122 | 20 | 50 | fits | 148,898 | 233 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 409,050 | 4.090 | 20 | 50 | fits | 97,229 | 154 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 495,191 | 4.952 | 20 | 20 | fits | 86,207 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,007,229 | 10.072 | 20 | 20 | fits | 86,485 | 28 | 0.643 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 361,055 | 3.611 | 20 | 20 | fits | 102,083 | 161 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 300,174 | 3.002 | 20 | 200 | fits | 149,061 | 234 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 410,731 | 4.107 | 20 | 200 | fits | 102,083 | 161 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 301,098 | 3.011 | 20 | 20 | fits | 149,061 | 234 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 411,435 | 4.114 | 20 | 20 | fits | 102,083 | 161 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 155,677 | 1.557 | 20 | 24 | fits | 151,230 | 155 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 303,748 | 3.037 | 20 | 24 | fits | 149,061 | 234 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 303,682 | 3.037 | 20 | 50 | fits | 149,061 | 234 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 414,459 | 4.145 | 20 | 50 | fits | 102,083 | 161 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 500,510 | 5.005 | 20 | 20 | fits | 86,117 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 996,917 | 9.969 | 20 | 20 | fits | 73,609 | 24 | 0.671 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 362,107 | 3.621 | 20 | 20 | fits | 107,159 | 148 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 312,073 | 3.121 | 20 | 200 | fits | 148,498 | 253 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 418,616 | 4.186 | 20 | 200 | fits | 107,159 | 148 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 312,997 | 3.130 | 20 | 20 | fits | 148,498 | 253 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 419,320 | 4.193 | 20 | 20 | fits | 107,159 | 148 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 168,139 | 1.681 | 20 | 24 | fits | 151,343 | 155 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 315,647 | 3.156 | 20 | 24 | fits | 148,498 | 253 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 315,581 | 3.156 | 20 | 50 | fits | 148,498 | 253 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 422,344 | 4.223 | 20 | 50 | fits | 107,159 | 148 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 508,432 | 5.084 | 20 | 20 | fits | 86,154 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,014,073 | 10.141 | 20 | 20 | fits | 74,080 | 24 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 352,845 | 3.528 | 20 | 20 | fits | 104,632 | 163 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 305,005 | 3.050 | 20 | 200 | fits | 147,898 | 231 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 409,021 | 4.090 | 20 | 200 | fits | 104,632 | 163 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 305,929 | 3.059 | 20 | 20 | fits | 147,898 | 231 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 409,725 | 4.097 | 20 | 20 | fits | 104,632 | 163 | 0.416 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 161,671 | 1.617 | 20 | 24 | fits | 151,138 | 155 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 308,579 | 3.086 | 20 | 24 | fits | 147,898 | 231 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 308,513 | 3.085 | 20 | 50 | fits | 147,898 | 231 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 412,749 | 4.127 | 20 | 50 | fits | 104,632 | 163 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 498,752 | 4.988 | 20 | 20 | fits | 86,069 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,005,449 | 10.054 | 20 | 20 | fits | 73,812 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 339,625 | 3.396 | 20 | 20 | fits | 104,011 | 160 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 305,853 | 3.059 | 20 | 200 | fits | 146,198 | 235 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 409,248 | 4.092 | 20 | 200 | fits | 104,011 | 160 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 306,777 | 3.068 | 20 | 20 | fits | 146,198 | 235 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 409,952 | 4.100 | 20 | 20 | fits | 104,011 | 160 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 154,726 | 1.547 | 20 | 24 | fits | 150,846 | 153 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 309,427 | 3.094 | 20 | 24 | fits | 146,198 | 235 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 309,361 | 3.094 | 20 | 50 | fits | 146,198 | 235 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 412,976 | 4.130 | 20 | 50 | fits | 104,011 | 160 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 498,840 | 4.988 | 20 | 20 | fits | 85,930 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,085,427 | 10.854 | 20 | 20 | fits | 78,827 | 31 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 340,143 | 3.401 | 20 | 20 | fits | 99,936 | 142 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 297,268 | 2.973 | 20 | 200 | fits | 147,268 | 248 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 396,588 | 3.966 | 20 | 200 | fits | 99,936 | 142 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 298,192 | 2.982 | 20 | 20 | fits | 147,268 | 248 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 397,292 | 3.973 | 20 | 20 | fits | 99,936 | 142 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 154,564 | 1.546 | 20 | 24 | fits | 150,575 | 152 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 300,842 | 3.008 | 20 | 24 | fits | 147,268 | 248 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 300,776 | 3.008 | 20 | 50 | fits | 147,268 | 248 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 400,316 | 4.003 | 20 | 50 | fits | 99,936 | 142 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 485,873 | 4.859 | 20 | 20 | fits | 85,623 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,074,850 | 10.748 | 20 | 20 | fits | 86,159 | 28 | 0.636 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 341,966 | 3.420 | 20 | 20 | fits | 99,936 | 142 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 299,091 | 2.991 | 20 | 200 | fits | 147,344 | 248 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 398,411 | 3.984 | 20 | 200 | fits | 99,936 | 142 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 300,015 | 3.000 | 20 | 20 | fits | 147,344 | 248 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 399,115 | 3.991 | 20 | 20 | fits | 99,936 | 142 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 156,311 | 1.563 | 20 | 24 | fits | 150,622 | 152 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 302,665 | 3.027 | 20 | 24 | fits | 147,344 | 248 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 302,599 | 3.026 | 20 | 50 | fits | 147,344 | 248 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 402,139 | 4.021 | 20 | 50 | fits | 99,936 | 142 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 492,944 | 4.929 | 20 | 20 | fits | 90,871 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,074,301 | 10.743 | 20 | 20 | fits | 73,561 | 24 | 0.671 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 438,462 | 4.385 | 20 | 20 | fits | 110,211 | 169 | 0.457 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 301,546 | 3.015 | 20 | 200 | fits | 148,146 | 232 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 496,078 | 4.961 | 20 | 200 | fits | 110,211 | 169 | 0.457 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 302,470 | 3.025 | 20 | 20 | fits | 148,146 | 232 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 496,782 | 4.968 | 20 | 20 | fits | 110,211 | 169 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 157,964 | 1.580 | 20 | 24 | fits | 150,575 | 152 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 305,120 | 3.051 | 20 | 24 | fits | 148,146 | 232 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 305,054 | 3.051 | 20 | 50 | fits | 148,146 | 232 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 499,806 | 4.998 | 20 | 50 | fits | 110,211 | 169 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 585,418 | 5.854 | 20 | 20 | fits | 85,678 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,074,605 | 10.746 | 20 | 20 | fits | 60,376 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 347,761 | 3.478 | 20 | 20 | fits | 96,544 | 152 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 302,126 | 3.021 | 20 | 200 | fits | 150,066 | 237 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 398,054 | 3.981 | 20 | 200 | fits | 96,544 | 152 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 303,050 | 3.030 | 20 | 20 | fits | 150,066 | 237 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 398,758 | 3.988 | 20 | 20 | fits | 96,544 | 152 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 156,624 | 1.566 | 20 | 24 | fits | 150,624 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 305,700 | 3.057 | 20 | 24 | fits | 150,066 | 237 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 305,634 | 3.056 | 20 | 50 | fits | 150,066 | 237 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 401,782 | 4.018 | 20 | 50 | fits | 96,544 | 152 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 500,917 | 5.009 | 20 | 20 | fits | 89,878 | 31 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,037,633 | 10.376 | 20 | 20 | fits | 76,414 | 25 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 360,803 | 3.608 | 20 | 20 | fits | 96,334 | 151 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 314,848 | 3.148 | 20 | 200 | fits | 152,213 | 242 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 410,566 | 4.106 | 20 | 200 | fits | 96,334 | 151 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 315,772 | 3.158 | 20 | 20 | fits | 152,213 | 242 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 411,270 | 4.113 | 20 | 20 | fits | 96,334 | 151 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 158,578 | 1.586 | 20 | 24 | fits | 150,638 | 153 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 318,422 | 3.184 | 20 | 24 | fits | 152,213 | 242 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 318,356 | 3.184 | 20 | 50 | fits | 152,213 | 242 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 414,294 | 4.143 | 20 | 50 | fits | 96,334 | 151 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 500,502 | 5.005 | 20 | 20 | fits | 86,274 | 24 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,084,709 | 10.847 | 20 | 20 | fits | 86,862 | 28 | 0.662 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 336,062 | 3.361 | 20 | 20 | fits | 97,294 | 151 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 301,875 | 3.019 | 20 | 200 | fits | 149,890 | 237 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 398,553 | 3.986 | 20 | 200 | fits | 97,294 | 151 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 302,799 | 3.028 | 20 | 20 | fits | 149,890 | 237 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 399,257 | 3.993 | 20 | 20 | fits | 97,294 | 151 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 156,549 | 1.565 | 20 | 24 | fits | 150,359 | 152 | 0.346 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 305,449 | 3.054 | 20 | 24 | fits | 149,890 | 237 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 305,383 | 3.054 | 20 | 50 | fits | 149,890 | 237 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 402,281 | 4.023 | 20 | 50 | fits | 97,294 | 151 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 485,831 | 4.858 | 20 | 20 | fits | 83,616 | 26 | 0.833 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,074,000 | 10.740 | 20 | 20 | fits | 86,590 | 28 | 0.652 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 353,951 | 3.540 | 20 | 20 | fits | 111,587 | 185 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 306,055 | 3.061 | 20 | 200 | fits | 152,323 | 209 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 417,026 | 4.170 | 20 | 200 | fits | 111,587 | 185 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 306,979 | 3.070 | 20 | 20 | fits | 152,323 | 209 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 417,730 | 4.177 | 20 | 20 | fits | 111,587 | 185 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 158,296 | 1.583 | 20 | 24 | fits | 150,406 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 309,629 | 3.096 | 20 | 24 | fits | 152,323 | 209 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 309,563 | 3.096 | 20 | 50 | fits | 152,323 | 209 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 420,754 | 4.208 | 20 | 50 | fits | 111,587 | 185 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 549,093 | 5.491 | 20 | 20 | fits | 89,891 | 31 | 0.793 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,071,402 | 10.714 | 20 | 20 | fits | 60,471 | 20 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 353,852 | 3.539 | 20 | 20 | fits | 96,433 | 151 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 308,105 | 3.081 | 20 | 200 | fits | 150,109 | 237 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 403,922 | 4.039 | 20 | 200 | fits | 96,433 | 151 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 309,029 | 3.090 | 20 | 20 | fits | 150,109 | 237 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 404,626 | 4.046 | 20 | 20 | fits | 96,433 | 151 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 162,560 | 1.626 | 20 | 24 | fits | 150,602 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 311,679 | 3.117 | 20 | 24 | fits | 150,109 | 237 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 311,613 | 3.116 | 20 | 50 | fits | 150,109 | 237 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 407,650 | 4.077 | 20 | 50 | fits | 96,433 | 151 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 493,443 | 4.934 | 20 | 20 | fits | 85,859 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,085,799 | 10.858 | 20 | 20 | fits | 86,682 | 29 | 0.662 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 328,823 | 3.288 | 20 | 20 | fits | 97,553 | 151 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 294,568 | 2.946 | 20 | 200 | fits | 151,428 | 242 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 391,505 | 3.915 | 20 | 200 | fits | 97,553 | 151 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 295,492 | 2.955 | 20 | 20 | fits | 151,428 | 242 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 392,209 | 3.922 | 20 | 20 | fits | 97,553 | 151 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 147,704 | 1.477 | 20 | 24 | fits | 150,602 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 298,142 | 2.981 | 20 | 24 | fits | 151,428 | 242 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 298,076 | 2.981 | 20 | 50 | fits | 151,428 | 242 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 395,233 | 3.952 | 20 | 50 | fits | 97,553 | 151 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 481,163 | 4.812 | 20 | 20 | fits | 85,996 | 25 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,074,146 | 10.741 | 20 | 20 | fits | 86,466 | 28 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 349,538 | 3.495 | 20 | 20 | fits | 109,218 | 163 | 0.494 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 295,698 | 2.957 | 20 | 200 | fits | 151,667 | 243 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 413,147 | 4.131 | 20 | 200 | fits | 109,218 | 163 | 0.494 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 296,622 | 2.966 | 20 | 20 | fits | 151,667 | 243 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 413,851 | 4.139 | 20 | 20 | fits | 109,218 | 163 | 0.494 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 148,595 | 1.486 | 20 | 24 | fits | 150,649 | 152 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 299,272 | 2.993 | 20 | 24 | fits | 151,667 | 243 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 299,206 | 2.992 | 20 | 50 | fits | 151,667 | 243 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 416,875 | 4.169 | 20 | 50 | fits | 109,218 | 163 | 0.494 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 582,721 | 5.827 | 20 | 20 | fits | 85,518 | 25 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,077,018 | 10.770 | 20 | 20 | fits | 65,027 | 27 | 0.728 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
