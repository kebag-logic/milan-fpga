### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 15 paths and 0 of 91 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.057 (0.212) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.029 (0.336) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.142 (0.533) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged1-6.adp_available.if0` (backlog-adp@verify-aged1-6) | 4.291 (4.841) | fits | 7 adp | 7 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.121 (0.557) | fits | 0 adp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-6.service.acmp.first.if0` (backlog-adp@verify-6) | 3.216 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.acmp.last.if0` (backlog-adp@program-aged2-6) | 6.811 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-6.service.adp.first.if0` (backlog-adp@verify-6) | 3.207 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-6.service.adp.last.if0` (backlog-adp@verify-6) | 4.724 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-6.service.aecp.first.if0` (backlog-adp@verify-6) | 1.623 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-6.service.aecp.last.if0` (backlog-adp@verify-6) | 3.242 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-6.service.maap.first.if0` (backlog-adp@verify-6) | 3.242 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-6.service.maap.last.if0` (backlog-adp@verify-6) | 4.761 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 6.840 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.srp.last.if0` (backlog-adp@program-aged2-6) | 9.276 | fits | 31 srp | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-6 | 0 | 9.120 | 7 | 152,787 (1.528) | yes | - |
| backlog-adp@verify-6 | 0 | 10.480 | 9 | 153,507 (1.535) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 9.840 | 7 | 151,559 (1.516) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 9.921 | 7 | 157,555 (1.576) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 9.865 | 7 | 153,882 (1.539) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.150 | 9 | 153,552 (1.536) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 9.921 | 7 | 156,872 (1.569) | yes | - |
| backlog-adp-refill | 0 | 40.957 | 22 | 152,872 (1.529) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-owed not run): 152,872 CPU cycles (1.529 ms), backlog-adp-refill.
Over the windows that released their whole load only: 152,872 (1.529 ms), backlog-adp-refill.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 122351 | 0 | 53,680 (0.537) | fits |
| backlog-adp@program-6 | 942 | 0 | 152,787 (1.528) | fits |
| backlog-adp@verify-6 | 1316 | 0 | 153,507 (1.535) | fits |
| backlog-adp@blank-aged2-6 | 834 | 0 | 151,559 (1.516) | fits |
| backlog-adp@program-aged2-6 | 1213 | 0 | 157,555 (1.576) | fits |
| backlog-adp@program-aged1-6 | 1162 | 0 | 153,882 (1.539) | fits |
| backlog-adp@verify-aged2-6 | 1595 | 0 | 153,552 (1.536) | fits |
| backlog-adp@verify-aged1-6 | 1543 | 0 | 156,872 (1.569) | fits |
| backlog-adp-refill | 324 | 0 | 152,872 (1.529) | fits |
| control | 88 | 0 | 33,635 (0.336) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-6 | 2 | +4.518 ms, 76,819 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.201 (20) | 10.799 |
| backlog-adp@program-aged2-6 | 2 | +4.737 ms, 80,442 (0.804 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.276 (20) | 10.724 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.424 (20) | 11.576 |
| backlog-adp@verify-aged2-6 | 2 | +4.651 ms, 77,749 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.172 (20) | 10.828 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.509 (20) | 11.491 |

Least margin over the aged windows: 10.724 ms, `backlog-adp@program-aged2-6.service.srp.last.if0` at 9.276 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.610 | 22,870 | 382 | 2 | 31.260 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 80,687 (0.807) | 77,410 (0.774) |
| backlog-adp@program-6 | 449 | 100,322 (1.003) | 77,944 (0.779) |
| backlog-adp@verify-6 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@blank-aged2-6 | 337 | 79,120 (0.791) | 75,465 (0.755) |
| backlog-adp@program-aged2-6 | 446 | 100,322 (1.003) | 77,944 (0.779) |
| backlog-adp@program-aged1-6 | 446 | 100,322 (1.003) | 78,354 (0.784) |
| backlog-adp@verify-aged2-6 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@verify-aged1-6 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp-refill | 274 | 25,989 (0.260) | 2,306 (0.023) |
| control | 79 | 25,989 (0.260) | 2,306 (0.023) |

Longest pass that carries a step: 104,189 CPU cycles (1.042 ms), backlog-adp@verify-6; longest step: 78,354 (0.784 ms), backlog-adp@program-aged1-6.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 379,838 | 3.798 | 20 | 20 | fits | 152,787 | 205 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 296,665 | 2.967 | 20 | 200 | fits | 151,024 | 180 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 448,836 | 4.488 | 20 | 200 | fits | 152,787 | 205 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 297,589 | 2.976 | 20 | 20 | fits | 151,024 | 180 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 587,908 | 5.879 | 20 | 20 | fits | 138,368 | 63 | 0.630 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 150,205 | 1.502 | 20 | 24 | fits | 148,783 | 145 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 300,239 | 3.002 | 20 | 24 | fits | 151,024 | 180 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 300,173 | 3.002 | 20 | 50 | fits | 151,024 | 180 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 452,564 | 4.526 | 20 | 50 | fits | 152,787 | 205 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 590,866 | 5.909 | 20 | 20 | fits | 138,368 | 63 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 843,107 | 8.431 | 20 | 20 | fits | 115,617 | 55 | 0.576 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 412,444 | 4.124 | 20 | 20 | fits | 152,305 | 201 | 0.394 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 320,672 | 3.207 | 20 | 200 | fits | 153,507 | 185 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 472,361 | 4.724 | 20 | 200 | fits | 152,305 | 201 | 0.394 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 321,596 | 3.216 | 20 | 20 | fits | 153,507 | 185 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 605,478 | 6.055 | 20 | 20 | fits | 132,413 | 61 | 0.601 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 162,304 | 1.623 | 20 | 24 | fits | 149,293 | 146 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 324,246 | 3.242 | 20 | 24 | fits | 153,507 | 185 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 324,180 | 3.242 | 20 | 50 | fits | 153,507 | 185 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 476,089 | 4.761 | 20 | 50 | fits | 152,305 | 201 | 0.394 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 608,436 | 6.084 | 20 | 20 | fits | 132,413 | 61 | 0.601 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 852,061 | 8.521 | 20 | 20 | fits | 118,245 | 52 | 0.482 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 403,824 | 4.038 | 20 | 20 | fits | 151,559 | 200 | 0.388 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 295,504 | 2.955 | 20 | 200 | fits | 150,938 | 180 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 446,447 | 4.464 | 20 | 200 | fits | 151,559 | 200 | 0.388 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 296,428 | 2.964 | 20 | 20 | fits | 150,938 | 180 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 659,984 | 6.600 | 20 | 20 | fits | 136,014 | 69 | 0.604 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 149,130 | 1.491 | 20 | 24 | fits | 147,816 | 142 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 299,078 | 2.991 | 20 | 24 | fits | 150,938 | 180 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 299,012 | 2.990 | 20 | 50 | fits | 150,938 | 180 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 450,175 | 4.502 | 20 | 50 | fits | 151,559 | 200 | 0.388 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 662,942 | 6.629 | 20 | 20 | fits | 136,014 | 69 | 0.604 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 920,053 | 9.201 | 20 | 20 | fits | 118,502 | 52 | 0.488 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 416,972 | 4.170 | 20 | 20 | fits | 157,555 | 199 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 301,209 | 3.012 | 20 | 200 | fits | 149,506 | 193 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 468,288 | 4.683 | 20 | 200 | fits | 157,555 | 199 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 302,133 | 3.021 | 20 | 20 | fits | 149,506 | 193 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 681,061 | 6.811 | 20 | 20 | fits | 131,627 | 62 | 0.592 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 156,267 | 1.563 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 304,783 | 3.048 | 20 | 24 | fits | 149,506 | 193 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 304,717 | 3.047 | 20 | 50 | fits | 149,506 | 193 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 472,016 | 4.720 | 20 | 50 | fits | 157,555 | 199 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 684,019 | 6.840 | 20 | 20 | fits | 131,627 | 62 | 0.592 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 927,567 | 9.276 | 20 | 20 | fits | 118,384 | 52 | 0.485 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 394,610 | 3.946 | 20 | 20 | fits | 153,882 | 192 | 0.376 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 292,270 | 2.923 | 20 | 200 | fits | 149,251 | 192 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 445,536 | 4.455 | 20 | 200 | fits | 153,882 | 192 | 0.376 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 293,194 | 2.932 | 20 | 20 | fits | 149,251 | 192 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 578,353 | 5.784 | 20 | 20 | fits | 132,113 | 62 | 0.600 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 147,583 | 1.476 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 295,844 | 2.958 | 20 | 24 | fits | 149,251 | 192 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 295,778 | 2.958 | 20 | 50 | fits | 149,251 | 192 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 449,264 | 4.493 | 20 | 50 | fits | 153,882 | 192 | 0.376 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 581,311 | 5.813 | 20 | 20 | fits | 132,113 | 62 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 842,361 | 8.424 | 20 | 20 | fits | 118,818 | 52 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 417,100 | 4.171 | 20 | 20 | fits | 151,714 | 200 | 0.389 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 308,627 | 3.086 | 20 | 200 | fits | 153,552 | 185 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 459,725 | 4.597 | 20 | 200 | fits | 151,714 | 200 | 0.389 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 309,551 | 3.096 | 20 | 20 | fits | 153,552 | 185 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 670,357 | 6.704 | 20 | 20 | fits | 132,179 | 62 | 0.593 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 150,136 | 1.501 | 20 | 24 | fits | 147,746 | 143 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 312,201 | 3.122 | 20 | 24 | fits | 153,552 | 185 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 312,135 | 3.121 | 20 | 50 | fits | 153,552 | 185 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 463,453 | 4.635 | 20 | 50 | fits | 151,714 | 200 | 0.389 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 673,315 | 6.733 | 20 | 20 | fits | 132,179 | 62 | 0.593 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 917,221 | 9.172 | 20 | 20 | fits | 118,541 | 53 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 429,058 | 4.291 | 20 | 20 | fits | 156,872 | 212 | 0.403 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 304,559 | 3.046 | 20 | 200 | fits | 149,580 | 177 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 471,065 | 4.711 | 20 | 200 | fits | 156,872 | 212 | 0.403 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 305,483 | 3.055 | 20 | 20 | fits | 149,580 | 177 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 604,244 | 6.042 | 20 | 20 | fits | 132,475 | 61 | 0.601 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 159,543 | 1.595 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 308,133 | 3.081 | 20 | 24 | fits | 149,580 | 177 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 308,067 | 3.081 | 20 | 50 | fits | 149,580 | 177 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 474,793 | 4.748 | 20 | 50 | fits | 156,872 | 212 | 0.403 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 607,202 | 6.072 | 20 | 20 | fits | 132,475 | 61 | 0.601 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 850,916 | 8.509 | 20 | 20 | fits | 118,245 | 52 | 0.482 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,126 | 0.121 | 20 | 20 | fits | 34,938 | 19 | 0.815 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 296,579 | 2.966 | 20 | 200 | fits | 152,872 | 186 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 35,959 | 0.360 | 20 | 200 | fits | 34,938 | 19 | 0.815 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 297,503 | 2.975 | 20 | 20 | fits | 152,872 | 186 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 455,803 | 4.558 | 20 | 20 | fits | 148,680 | 204 | 0.298 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 148,271 | 1.483 | 20 | 24 | fits | 148,457 | 145 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 300,153 | 3.002 | 20 | 24 | fits | 152,872 | 186 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 300,087 | 3.001 | 20 | 50 | fits | 152,872 | 186 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 458,827 | 4.588 | 20 | 50 | fits | 148,680 | 204 | 0.298 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 594,714 | 5.947 | 20 | 20 | fits | 135,953 | 58 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 820,695 | 8.207 | 20 | 20 | fits | 101,088 | 44 | 0.514 |
| LINK_UP | `adp.link_up.if0` | 2,856 | 0.029 | 20 | 200 | fits | 33,635 | 43 (11) | 0.730 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,239 | 0.142 | 20 | 200 | fits | 27,591 | 23 (39) | 0.747 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,719 | 0.057 | 20 | 200 | fits | 21,167 | 16 (31) | 0.674 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
