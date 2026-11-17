### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 15 paths and 0 of 116 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.045 (0.170) | fits | 0 adp | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.024 (0.240) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-link) | 0.027 (0.267) | fits | 0 events | 2 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-link) | 0.106 (0.440) | fits | 0 events | 2 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged2-7.adp_available.if0` (backlog-adp@blank-aged2-7) | 4.450 (5.120) | fits | 7 adp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-7.service.acmp.first.if0` (backlog-adp@blank-aged1-7) | 3.104 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.acmp.last.if0` (backlog-adp@blank-aged2-7) | 4.959 | fits | 11 acmp | 10 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-7.service.adp.first.if0` (backlog-adp@blank-aged1-7) | 3.094 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.adp.last.if0` (backlog-adp@blank-aged2-7) | 4.952 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-7.service.aecp.first.if0` (backlog-adp@blank-aged1-7) | 1.632 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-7.service.aecp.last.if0` (backlog-adp@blank-aged1-7) | 3.130 | fits | 15 aecp | 10 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-7.service.maap.first.if0` (backlog-adp@blank-aged1-7) | 3.129 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.maap.last.if0` (backlog-adp@blank-aged2-7) | 4.990 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-7.service.srp.first.if0` (backlog-adp@blank-aged2-7) | 5.823 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.srp.last.if0` (backlog-adp@verify-aged2-7) | 10.724 | fits | 31 srp | 10 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-1 | 0 | 11.276 | 11 | 152,674 (1.527) | yes | - |
| backlog-adp@blank-7 | 0 | 13.055 | 14 | 152,486 (1.525) | yes | - |
| backlog-adp@program-7 | 0 | 11.038 | 13 | 152,479 (1.525) | yes | - |
| backlog-adp@verify-7 | 0 | 12.349 | 12 | 152,846 (1.528) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.610 | 14 | 151,895 (1.519) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.496 | 15 | 152,235 (1.522) | yes | - |
| backlog-adp@program-aged2-7 | 1 | 11.459 | 11 | 150,559 (1.506) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.820 | 13 | 152,316 (1.523) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.217 | 12 | 152,485 (1.525) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.376 | 12 | 152,413 (1.524) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-1 | 416 | 0 | 152,674 (1.527) | fits |
| backlog-adp@blank-7 | 421 | 0 | 152,486 (1.525) | fits |
| backlog-adp@program-7 | 526 | 0 | 152,479 (1.525) | fits |
| backlog-adp@verify-7 | 617 | 0 | 152,846 (1.528) | fits |
| backlog-adp@blank-aged2-7 | 750 | 0 | 151,895 (1.519) | fits |
| backlog-adp@blank-aged1-7 | 695 | 0 | 152,235 (1.522) | fits |
| backlog-adp@program-aged2-7 | 848 | 0 | 153,371 (1.534) | fits |
| backlog-adp@program-aged1-7 | 791 | 0 | 152,316 (1.523) | fits |
| backlog-adp@verify-aged2-7 | 945 | 0 | 152,485 (1.525) | fits |
| backlog-adp@verify-aged1-7 | 887 | 0 | 152,413 (1.524) | fits |
| adp-link | 89 | 0 | 39,491 (0.395) | fits |
| adp-discover | 88 | 0 | 30,145 (0.301) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.669 (20) | 9.331 |
| backlog-adp@blank-aged1-7 | 1 | none | +10.931 ms, 76,683 (0.767 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.686 (20) | 9.314 |
| backlog-adp@program-aged2-7 | 2 | +4.051 ms, 80,470 (0.805 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.689 (20) | 9.311 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.932 (20) | 10.068 |
| backlog-adp@verify-aged2-7 | 2 | +3.056 ms, 77,402 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.724 (20) | 9.276 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.962 (20) | 10.038 |

Least margin over the aged windows: 9.276 ms, `backlog-adp@verify-aged2-7.service.srp.last.if0` at 10.724 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-1 | 299 | 92,937 (0.929) | 76,336 (0.763) |
| backlog-adp@blank-7 | 300 | 96,490 (0.965) | 76,173 (0.762) |
| backlog-adp@program-7 | 329 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-7 | 356 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@blank-aged2-7 | 298 | 92,053 (0.921) | 75,835 (0.758) |
| backlog-adp@blank-aged1-7 | 297 | 76,683 (0.767) | 75,564 (0.756) |
| backlog-adp@program-aged2-7 | 327 | 96,381 (0.964) | 78,319 (0.783) |
| backlog-adp@program-aged1-7 | 327 | 97,083 (0.971) | 78,813 (0.788) |
| backlog-adp@verify-aged2-7 | 356 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-aged1-7 | 356 | 96,381 (0.964) | 78,191 (0.782) |
| adp-link | 79 | 22,142 (0.221) | 2,242 (0.022) |
| adp-discover | 79 | 22,142 (0.221) | 2,242 (0.022) |

Longest pass that carries a step: 97,083 CPU cycles (0.971 ms), backlog-adp@program-aged1-7; longest step: 78,813 (0.788 ms), backlog-adp@program-aged1-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 354,676 | 3.547 | 20 | 20 | fits | 97,297 | 154 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 306,732 | 3.067 | 20 | 200 | fits | 149,602 | 233 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 403,413 | 4.034 | 20 | 200 | fits | 97,297 | 154 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 307,656 | 3.077 | 20 | 20 | fits | 149,602 | 233 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 404,117 | 4.041 | 20 | 20 | fits | 97,297 | 154 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 161,694 | 1.617 | 20 | 24 | fits | 152,674 | 155 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 310,306 | 3.103 | 20 | 24 | fits | 149,602 | 233 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 310,240 | 3.102 | 20 | 50 | fits | 149,602 | 233 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 407,141 | 4.071 | 20 | 50 | fits | 97,297 | 154 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 491,425 | 4.914 | 20 | 20 | fits | 84,350 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 998,556 | 9.986 | 20 | 20 | fits | 85,260 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 346,336 | 3.463 | 20 | 20 | fits | 104,809 | 163 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 298,238 | 2.982 | 20 | 200 | fits | 149,213 | 231 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 402,431 | 4.024 | 20 | 200 | fits | 104,809 | 163 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 299,162 | 2.992 | 20 | 20 | fits | 149,213 | 231 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 403,135 | 4.031 | 20 | 20 | fits | 104,809 | 163 | 0.410 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 153,589 | 1.536 | 20 | 24 | fits | 152,486 | 155 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 301,812 | 3.018 | 20 | 24 | fits | 149,213 | 231 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 301,746 | 3.017 | 20 | 50 | fits | 149,213 | 231 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 406,159 | 4.062 | 20 | 50 | fits | 104,809 | 163 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 490,480 | 4.905 | 20 | 20 | fits | 84,387 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 991,006 | 9.910 | 20 | 20 | fits | 72,762 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 357,140 | 3.571 | 20 | 20 | fits | 109,201 | 169 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 297,216 | 2.972 | 20 | 200 | fits | 149,129 | 232 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 414,469 | 4.145 | 20 | 200 | fits | 109,201 | 169 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 298,140 | 2.981 | 20 | 20 | fits | 149,129 | 232 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 415,173 | 4.152 | 20 | 20 | fits | 109,201 | 169 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 152,651 | 1.527 | 20 | 24 | fits | 152,479 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 300,790 | 3.008 | 20 | 24 | fits | 149,129 | 232 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 300,724 | 3.007 | 20 | 50 | fits | 149,129 | 232 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 418,197 | 4.182 | 20 | 50 | fits | 109,201 | 169 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 501,897 | 5.019 | 20 | 20 | fits | 83,766 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 987,364 | 9.874 | 20 | 20 | fits | 59,857 | 20 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 348,713 | 3.487 | 20 | 20 | fits | 104,581 | 163 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 300,752 | 3.008 | 20 | 200 | fits | 148,790 | 231 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 404,717 | 4.047 | 20 | 200 | fits | 104,581 | 163 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 301,676 | 3.017 | 20 | 20 | fits | 148,790 | 231 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 405,421 | 4.054 | 20 | 20 | fits | 104,581 | 163 | 0.408 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 156,526 | 1.565 | 20 | 24 | fits | 152,846 | 155 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 304,326 | 3.043 | 20 | 24 | fits | 148,790 | 231 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 304,260 | 3.043 | 20 | 50 | fits | 148,790 | 231 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 408,445 | 4.084 | 20 | 50 | fits | 104,581 | 163 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 492,598 | 4.926 | 20 | 20 | fits | 84,219 | 24 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 993,384 | 9.934 | 20 | 20 | fits | 72,767 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 444,954 | 4.450 | 20 | 20 | fits | 109,044 | 169 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 302,126 | 3.021 | 20 | 200 | fits | 149,501 | 232 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 495,225 | 4.952 | 20 | 200 | fits | 109,044 | 169 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 303,050 | 3.030 | 20 | 20 | fits | 149,501 | 232 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 495,929 | 4.959 | 20 | 20 | fits | 109,044 | 169 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 157,189 | 1.572 | 20 | 24 | fits | 151,895 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 305,700 | 3.057 | 20 | 24 | fits | 149,501 | 232 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 305,634 | 3.056 | 20 | 50 | fits | 149,501 | 232 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 498,953 | 4.990 | 20 | 50 | fits | 109,044 | 169 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 582,323 | 5.823 | 20 | 20 | fits | 83,436 | 24 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,066,947 | 10.669 | 20 | 20 | fits | 59,743 | 20 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 365,810 | 3.658 | 20 | 20 | fits | 113,313 | 176 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 309,441 | 3.094 | 20 | 200 | fits | 150,840 | 220 | 0.459 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 422,138 | 4.221 | 20 | 200 | fits | 113,313 | 176 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 310,365 | 3.104 | 20 | 20 | fits | 150,840 | 220 | 0.459 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 422,842 | 4.228 | 20 | 20 | fits | 113,313 | 176 | 0.395 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 163,165 | 1.632 | 20 | 24 | fits | 152,235 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 313,015 | 3.130 | 20 | 24 | fits | 150,840 | 220 | 0.459 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 312,949 | 3.129 | 20 | 50 | fits | 150,840 | 220 | 0.459 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 425,866 | 4.259 | 20 | 50 | fits | 113,313 | 176 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 550,934 | 5.509 | 20 | 20 | fits | 87,073 | 31 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,068,642 | 10.686 | 20 | 20 | fits | 59,729 | 20 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 350,927 | 3.509 | 20 | 20 | fits | 106,418 | 166 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 293,919 | 2.939 | 20 | 200 | fits | 150,559 | 238 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 399,721 | 3.997 | 20 | 200 | fits | 106,418 | 166 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 294,843 | 2.948 | 20 | 20 | fits | 150,559 | 238 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 400,425 | 4.004 | 20 | 20 | fits | 106,418 | 166 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 147,924 | 1.479 | 20 | 24 | fits | 153,371 | 157 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 297,493 | 2.975 | 20 | 24 | fits | 150,559 | 238 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 297,427 | 2.974 | 20 | 50 | fits | 150,559 | 238 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 403,449 | 4.034 | 20 | 50 | fits | 106,418 | 166 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 567,518 | 5.675 | 20 | 20 | fits | 83,665 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,068,918 | 10.689 | 20 | 20 | fits | 72,802 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 370,107 | 3.701 | 20 | 20 | fits | 108,891 | 169 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 303,672 | 3.037 | 20 | 200 | fits | 149,644 | 232 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 420,460 | 4.205 | 20 | 200 | fits | 108,891 | 169 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 304,596 | 3.046 | 20 | 20 | fits | 149,644 | 232 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 421,164 | 4.212 | 20 | 20 | fits | 108,891 | 169 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 158,592 | 1.586 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 307,246 | 3.072 | 20 | 24 | fits | 149,644 | 232 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 307,180 | 3.072 | 20 | 50 | fits | 149,644 | 232 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 424,188 | 4.242 | 20 | 50 | fits | 108,891 | 169 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 507,819 | 5.078 | 20 | 20 | fits | 83,697 | 24 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 993,241 | 9.932 | 20 | 20 | fits | 59,857 | 20 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 432,353 | 4.324 | 20 | 20 | fits | 104,632 | 163 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 300,837 | 3.008 | 20 | 200 | fits | 149,191 | 231 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 482,255 | 4.823 | 20 | 200 | fits | 104,632 | 163 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 301,761 | 3.018 | 20 | 20 | fits | 149,191 | 231 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 482,959 | 4.830 | 20 | 20 | fits | 104,632 | 163 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 156,210 | 1.562 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 304,411 | 3.044 | 20 | 24 | fits | 149,191 | 231 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 304,345 | 3.043 | 20 | 50 | fits | 149,191 | 231 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 485,983 | 4.860 | 20 | 50 | fits | 104,632 | 163 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 570,241 | 5.702 | 20 | 20 | fits | 84,324 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,072,381 | 10.724 | 20 | 20 | fits | 72,855 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 349,769 | 3.498 | 20 | 20 | fits | 104,937 | 163 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 302,108 | 3.021 | 20 | 200 | fits | 148,898 | 231 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 406,429 | 4.064 | 20 | 200 | fits | 104,937 | 163 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 303,032 | 3.030 | 20 | 20 | fits | 148,898 | 231 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 407,133 | 4.071 | 20 | 20 | fits | 104,937 | 163 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 157,774 | 1.578 | 20 | 24 | fits | 152,413 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 305,682 | 3.057 | 20 | 24 | fits | 148,898 | 231 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 305,616 | 3.056 | 20 | 50 | fits | 148,898 | 231 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 410,157 | 4.102 | 20 | 50 | fits | 104,937 | 163 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 494,421 | 4.944 | 20 | 20 | fits | 84,330 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 996,241 | 9.962 | 20 | 20 | fits | 73,119 | 24 | 0.664 |
| LINK_UP | `adp.link_up.if0` | 2,674 | 0.027 | 20 | 200 | fits | 26,711 | 43 (11) | 0.737 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,642 | 0.106 | 20 | 200 | fits | 23,487 | 23 (39) | 0.762 |
| LINK_DOWN | `adp.link_down.if0` | 2,396 | 0.024 | 20 | 200 | fits | 23,994 | 23 (9) | 0.769 |
| LINK_UP | `adp.link_up.if0` | 2,674 | 0.027 | 20 | 200 | fits | 26,711 | 43 (11) | 0.737 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,642 | 0.106 | 20 | 200 | fits | 23,487 | 23 (39) | 0.762 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,546 | 0.045 | 20 | 200 | fits | 17,026 | 16 (31) | 0.663 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
