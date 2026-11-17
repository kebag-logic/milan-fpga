### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 14 paths and 0 of 113 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.026 (0.205) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.029 (0.336) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.142 (0.533) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.709 (6.250) | fits | 7 adp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 3.780 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 6.641 | fits | 11 acmp | 10 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 3.771 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 5.311 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.204 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.aecp.last.if0` (backlog-adp@blank-0) | 3.806 | fits | 15 aecp | 10 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 3.806 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 5.348 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.srp.first.if0` (backlog-adp@blank-0) | 6.670 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.srp.last.if0` (backlog-adp@blank-0) | 9.020 | fits | 31 srp | 10 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.335 | 9 | 154,609 (1.546) | yes | - |
| backlog-adp@blank-4 | 0 | 9.789 | 6 | 156,532 (1.565) | yes | - |
| backlog-adp@program-2 | 0 | 10.362 | 8 | 155,264 (1.553) | yes | - |
| backlog-adp@verify-2 | 0 | 9.808 | 7 | 155,147 (1.551) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 9.708 | 7 | 150,023 (1.500) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 9.939 | 7 | 150,749 (1.507) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 10.014 | 7 | 158,312 (1.583) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 9.913 | 7 | 150,786 (1.508) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 9.709 | 7 | 152,277 (1.523) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 9.963 | 7 | 153,638 (1.536) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 554 | 0 | 154,609 (1.546) | fits |
| backlog-adp@blank-4 | 554 | 0 | 156,532 (1.565) | fits |
| backlog-adp@program-2 | 939 | 0 | 155,264 (1.553) | fits |
| backlog-adp@verify-2 | 1314 | 0 | 155,147 (1.551) | fits |
| backlog-adp@blank-aged2-2 | 809 | 0 | 150,023 (1.500) | fits |
| backlog-adp@blank-aged1-3 | 765 | 0 | 150,749 (1.507) | fits |
| backlog-adp@program-aged2-2 | 1189 | 0 | 158,312 (1.583) | fits |
| backlog-adp@program-aged1-2 | 1137 | 0 | 150,786 (1.508) | fits |
| backlog-adp@verify-aged2-2 | 1568 | 0 | 152,277 (1.523) | fits |
| backlog-adp@verify-aged1-2 | 1519 | 0 | 153,638 (1.536) | fits |
| save | 610 | 0 | 48,009 (0.480) | fits |
| adp-gm | 88 | 0 | 33,635 (0.336) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-2 | 2 | none | +8.515 ms, 76,576 (0.766 ms), read-back | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 8.478 (20) | 11.522 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 8.537 (20) | 11.463 |
| backlog-adp@program-aged2-2 | 2 | none | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 8.239 (20) | 11.761 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.464 (20) | 11.536 |
| backlog-adp@verify-aged2-2 | 2 | none | +8.511 ms, 77,585 (0.776 ms), read-back | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 8.474 (20) | 11.526 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.221 (20) | 11.779 |

Least margin over the aged windows: 11.463 ms, `backlog-adp@blank-aged1-3.service.srp.last.if0` at 8.537 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save | 4817.951 | 12,470 | 382 | - | 10.850 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 339 | 94,609 (0.946) | 75,904 (0.759) |
| backlog-adp@blank-4 | 339 | 95,984 (0.960) | 75,943 (0.759) |
| backlog-adp@program-2 | 448 | 100,322 (1.003) | 78,354 (0.784) |
| backlog-adp@verify-2 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@blank-aged2-2 | 337 | 79,120 (0.791) | 75,467 (0.755) |
| backlog-adp@blank-aged1-3 | 337 | 96,265 (0.963) | 75,944 (0.759) |
| backlog-adp@program-aged2-2 | 446 | 100,322 (1.003) | 78,221 (0.782) |
| backlog-adp@program-aged1-2 | 446 | 100,322 (1.003) | 78,354 (0.784) |
| backlog-adp@verify-aged2-2 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@verify-aged1-2 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| save | 585 | 100,012 (1.000) | 77,753 (0.778) |
| adp-gm | 79 | 25,989 (0.260) | 2,306 (0.023) |

Longest pass that carries a step: 104,189 CPU cycles (1.042 ms), backlog-adp@verify-2; longest step: 78,354 (0.784 ms), backlog-adp@program-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 470,918 | 4.709 | 20 | 20 | fits | 154,609 | 196 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 377,069 | 3.771 | 20 | 200 | fits | 151,604 | 197 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 531,062 | 5.311 | 20 | 200 | fits | 154,609 | 196 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 377,993 | 3.780 | 20 | 20 | fits | 151,604 | 197 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 664,089 | 6.641 | 20 | 20 | fits | 132,323 | 55 | 0.625 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 220,363 | 2.204 | 20 | 24 | fits | 149,339 | 146 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 380,643 | 3.806 | 20 | 24 | fits | 151,604 | 197 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 380,577 | 3.806 | 20 | 50 | fits | 151,604 | 197 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 534,790 | 5.348 | 20 | 50 | fits | 154,609 | 196 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 667,047 | 6.670 | 20 | 20 | fits | 132,323 | 55 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 901,964 | 9.020 | 20 | 20 | fits | 109,580 | 48 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 386,296 | 3.863 | 20 | 20 | fits | 156,532 | 226 | 0.363 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 291,526 | 2.915 | 20 | 200 | fits | 149,771 | 201 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 447,442 | 4.474 | 20 | 200 | fits | 156,532 | 226 | 0.363 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 292,450 | 2.925 | 20 | 20 | fits | 149,771 | 201 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 592,123 | 5.921 | 20 | 20 | fits | 133,677 | 66 | 0.656 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 146,319 | 1.463 | 20 | 24 | fits | 147,687 | 105 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 295,100 | 2.951 | 20 | 24 | fits | 149,771 | 201 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 295,034 | 2.950 | 20 | 50 | fits | 149,771 | 201 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 451,170 | 4.512 | 20 | 50 | fits | 156,532 | 226 | 0.363 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 595,081 | 5.951 | 20 | 20 | fits | 133,677 | 66 | 0.656 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 839,085 | 8.391 | 20 | 20 | fits | 118,384 | 52 | 0.485 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 399,498 | 3.995 | 20 | 20 | fits | 155,264 | 195 | 0.340 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 305,333 | 3.053 | 20 | 200 | fits | 151,821 | 197 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 459,981 | 4.600 | 20 | 200 | fits | 155,264 | 195 | 0.340 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 306,257 | 3.063 | 20 | 20 | fits | 151,821 | 197 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 598,911 | 5.989 | 20 | 20 | fits | 138,226 | 63 | 0.628 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 148,381 | 1.484 | 20 | 24 | fits | 149,186 | 146 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 308,907 | 3.089 | 20 | 24 | fits | 151,821 | 197 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 308,841 | 3.088 | 20 | 50 | fits | 151,821 | 197 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 463,709 | 4.637 | 20 | 50 | fits | 155,264 | 195 | 0.340 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 601,869 | 6.019 | 20 | 20 | fits | 138,226 | 63 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 837,028 | 8.370 | 20 | 20 | fits | 109,580 | 48 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 388,221 | 3.882 | 20 | 20 | fits | 155,147 | 195 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 294,131 | 2.941 | 20 | 200 | fits | 149,323 | 192 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 448,662 | 4.487 | 20 | 200 | fits | 155,147 | 195 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 295,055 | 2.951 | 20 | 20 | fits | 149,323 | 192 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 581,515 | 5.815 | 20 | 20 | fits | 132,149 | 55 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 149,372 | 1.494 | 20 | 24 | fits | 149,055 | 145 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 297,705 | 2.977 | 20 | 24 | fits | 149,323 | 192 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 297,639 | 2.976 | 20 | 50 | fits | 149,323 | 192 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 452,390 | 4.524 | 20 | 50 | fits | 155,147 | 195 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 584,473 | 5.845 | 20 | 20 | fits | 132,149 | 55 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 840,216 | 8.402 | 20 | 20 | fits | 119,240 | 61 | 0.583 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 419,827 | 4.198 | 20 | 20 | fits | 150,023 | 208 | 0.390 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 302,434 | 3.024 | 20 | 200 | fits | 149,562 | 177 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 462,192 | 4.622 | 20 | 200 | fits | 150,023 | 208 | 0.390 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 303,358 | 3.034 | 20 | 20 | fits | 149,562 | 177 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 595,338 | 5.953 | 20 | 20 | fits | 132,442 | 61 | 0.601 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 157,436 | 1.574 | 20 | 24 | fits | 147,758 | 142 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 306,008 | 3.060 | 20 | 24 | fits | 149,562 | 177 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 305,942 | 3.059 | 20 | 50 | fits | 149,562 | 177 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 465,920 | 4.659 | 20 | 50 | fits | 150,023 | 208 | 0.390 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 598,296 | 5.983 | 20 | 20 | fits | 132,442 | 61 | 0.601 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 847,781 | 8.478 | 20 | 20 | fits | 124,016 | 58 | 0.537 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 416,066 | 4.161 | 20 | 20 | fits | 150,749 | 192 | 0.390 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 307,347 | 3.073 | 20 | 200 | fits | 149,484 | 193 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 467,721 | 4.677 | 20 | 200 | fits | 150,749 | 192 | 0.390 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 308,271 | 3.083 | 20 | 20 | fits | 149,484 | 193 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 600,965 | 6.010 | 20 | 20 | fits | 132,540 | 61 | 0.602 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 162,427 | 1.624 | 20 | 24 | fits | 147,749 | 142 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 310,921 | 3.109 | 20 | 24 | fits | 149,484 | 193 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 310,855 | 3.109 | 20 | 50 | fits | 149,484 | 193 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 471,449 | 4.714 | 20 | 50 | fits | 150,749 | 192 | 0.390 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 603,923 | 6.039 | 20 | 20 | fits | 132,540 | 61 | 0.602 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 853,671 | 8.537 | 20 | 20 | fits | 118,532 | 52 | 0.489 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 387,298 | 3.873 | 20 | 20 | fits | 158,312 | 202 | 0.356 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 290,052 | 2.901 | 20 | 200 | fits | 150,502 | 197 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 447,748 | 4.477 | 20 | 200 | fits | 158,312 | 202 | 0.356 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 290,976 | 2.910 | 20 | 20 | fits | 150,502 | 197 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 580,009 | 5.800 | 20 | 20 | fits | 131,557 | 55 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 144,114 | 1.441 | 20 | 24 | fits | 149,579 | 147 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 293,626 | 2.936 | 20 | 24 | fits | 150,502 | 197 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 293,560 | 2.936 | 20 | 50 | fits | 150,502 | 197 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 451,476 | 4.515 | 20 | 50 | fits | 158,312 | 202 | 0.356 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 582,967 | 5.830 | 20 | 20 | fits | 131,557 | 55 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 823,867 | 8.239 | 20 | 20 | fits | 115,563 | 55 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 409,584 | 4.096 | 20 | 20 | fits | 150,786 | 192 | 0.391 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 300,828 | 3.008 | 20 | 200 | fits | 149,493 | 193 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 461,239 | 4.612 | 20 | 200 | fits | 150,786 | 192 | 0.391 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 301,752 | 3.018 | 20 | 20 | fits | 149,493 | 193 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 593,930 | 5.939 | 20 | 20 | fits | 131,987 | 61 | 0.600 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 155,899 | 1.559 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 304,402 | 3.044 | 20 | 24 | fits | 149,493 | 193 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 304,336 | 3.043 | 20 | 50 | fits | 149,493 | 193 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 464,967 | 4.650 | 20 | 50 | fits | 150,786 | 192 | 0.391 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 596,888 | 5.969 | 20 | 20 | fits | 131,987 | 61 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 846,425 | 8.464 | 20 | 20 | fits | 124,083 | 58 | 0.538 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 400,687 | 4.007 | 20 | 20 | fits | 152,277 | 204 | 0.341 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 300,697 | 3.007 | 20 | 200 | fits | 150,963 | 180 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 452,358 | 4.524 | 20 | 200 | fits | 152,277 | 204 | 0.341 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 301,621 | 3.016 | 20 | 20 | fits | 150,963 | 180 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 585,109 | 5.851 | 20 | 20 | fits | 132,047 | 55 | 0.621 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 154,298 | 1.543 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 304,271 | 3.043 | 20 | 24 | fits | 150,963 | 180 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 304,205 | 3.042 | 20 | 50 | fits | 150,963 | 180 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 456,086 | 4.561 | 20 | 50 | fits | 152,277 | 204 | 0.341 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 588,067 | 5.881 | 20 | 20 | fits | 132,047 | 55 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 847,397 | 8.474 | 20 | 20 | fits | 117,625 | 55 | 0.586 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 394,490 | 3.945 | 20 | 20 | fits | 153,638 | 209 | 0.331 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 292,294 | 2.923 | 20 | 200 | fits | 150,490 | 181 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 445,316 | 4.453 | 20 | 200 | fits | 153,638 | 209 | 0.331 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 293,218 | 2.932 | 20 | 20 | fits | 150,490 | 181 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 578,200 | 5.782 | 20 | 20 | fits | 132,180 | 55 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 146,368 | 1.464 | 20 | 24 | fits | 149,655 | 147 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 295,868 | 2.959 | 20 | 24 | fits | 150,490 | 181 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 295,802 | 2.958 | 20 | 50 | fits | 150,490 | 181 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 449,044 | 4.490 | 20 | 50 | fits | 153,638 | 209 | 0.331 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 581,158 | 5.812 | 20 | 20 | fits | 132,180 | 55 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 822,125 | 8.221 | 20 | 20 | fits | 115,630 | 55 | 0.555 |
| LINK_UP | `adp.link_up.if0` | 2,856 | 0.029 | 20 | 200 | fits | 33,635 | 43 (11) | 0.730 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,239 | 0.142 | 20 | 200 | fits | 27,591 | 23 (39) | 0.747 |
| GM_CHANGE | `adp.gm_change.if0` | 2,590 | 0.026 | 20 | 200 | fits | 20,503 | 17 (11) | 0.747 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
