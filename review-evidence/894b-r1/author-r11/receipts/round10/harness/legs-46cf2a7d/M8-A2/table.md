### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 24 paths and 0 of 103 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.246 (0.705) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.354 (0.633) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.253 (0.593) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.250 (0.593) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.022 (0.309) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-link) | 0.029 (0.336) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-link) | 0.142 (0.533) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged1-1.adp_available.if0` (backlog-adp@verify-aged1-1) | 4.145 (4.831) | fits | 7 adp | 8 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.555 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 3.017 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 3.051 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.421 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.638 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.join.if0` (save-starved) | 2.818 | fits | 0 srp | 3 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-1.service.acmp.first.if0` (backlog-adp@verify-aged1-1) | 3.153 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-1.service.acmp.last.if0` (backlog-adp@blank-aged2-1) | 6.112 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-1.service.adp.first.if0` (backlog-adp@verify-aged1-1) | 3.144 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-1.service.adp.last.if0` (backlog-adp@verify-aged1-1) | 4.661 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-1.service.aecp.first.if0` (backlog-adp@blank-aged2-1) | 1.635 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-1.service.aecp.last.if0` (backlog-adp@verify-aged1-1) | 3.180 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-1.service.maap.first.if0` (backlog-adp@verify-aged1-1) | 3.179 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-1.service.maap.last.if0` (backlog-adp@verify-aged1-1) | 4.698 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-1.service.srp.first.if0` (backlog-adp@blank-aged2-1) | 6.141 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-1.service.srp.last.if0` (backlog-adp@program-1) | 8.518 | fits | 31 srp | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-1 | 0 | 9.963 | 7 | 153,917 (1.539) | yes | - |
| backlog-adp@verify-1 | 0 | 10.034 | 8 | 154,625 (1.546) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 9.945 | 8 | 156,632 (1.566) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 9.784 | 7 | 153,811 (1.538) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.368 | 10 | 153,612 (1.536) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.145 | 8 | 149,672 (1.497) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 9.931 | 8 | 152,750 (1.528) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.546 | 10 | 153,510 (1.535) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-starved | 58666 | 0 | 160,758 (1.608) | fits |
| backlog-adp@program-1 | 937 | 0 | 153,917 (1.539) | fits |
| backlog-adp@verify-1 | 1315 | 0 | 154,625 (1.546) | fits |
| backlog-adp@blank-aged2-1 | 804 | 0 | 156,632 (1.566) | fits |
| backlog-adp@blank-aged1-2 | 758 | 0 | 153,811 (1.538) | fits |
| backlog-adp@program-aged2-1 | 1184 | 0 | 153,612 (1.536) | fits |
| backlog-adp@program-aged1-1 | 1132 | 0 | 149,672 (1.497) | fits |
| backlog-adp@verify-aged2-1 | 1563 | 0 | 152,750 (1.528) | fits |
| backlog-adp@verify-aged1-1 | 1514 | 0 | 153,510 (1.535) | fits |
| acmp-noresp | 1881 | 0 | 46,561 (0.466) | fits |
| adp-link | 89 | 0 | 43,642 (0.436) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-1 | 2 | none | +8.761 ms, 76,449 (0.764 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.491 (20) | 11.509 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 8.384 (20) | 11.616 |
| backlog-adp@program-aged2-1 | 2 | none | +8.598 ms, 80,338 (0.803 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.328 (20) | 11.672 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.472 (20) | 11.528 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.739 ms, 77,458 (0.775 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.469 (20) | 11.531 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.369 (20) | 11.631 |

Least margin over the aged windows: 11.509 ms, `backlog-adp@blank-aged2-1.service.srp.last.if0` at 8.491 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 12447.481 | 12,470 | 382 | - | 33.356 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-starved | 698 | 81,642 (0.816) | 77,822 (0.778) |
| backlog-adp@program-1 | 448 | 100,322 (1.003) | 78,354 (0.784) |
| backlog-adp@verify-1 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@blank-aged2-1 | 337 | 79,120 (0.791) | 75,416 (0.754) |
| backlog-adp@blank-aged1-2 | 337 | 96,119 (0.961) | 75,944 (0.759) |
| backlog-adp@program-aged2-1 | 446 | 100,322 (1.003) | 77,970 (0.780) |
| backlog-adp@program-aged1-1 | 446 | 100,322 (1.003) | 78,303 (0.783) |
| backlog-adp@verify-aged2-1 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@verify-aged1-1 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| acmp-noresp | 615 | 108,070 (1.081) | 77,995 (0.780) |
| adp-link | 79 | 25,989 (0.260) | 2,306 (0.023) |

Longest pass that carries a step: 108,070 CPU cycles (1.081 ms), acmp-noresp; longest step: 78,354 (0.784 ms), backlog-adp@program-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 301,688 | 3.017 | 20 | 200 | fits | 141,870 | 139 | 0.550 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 255,523 | 2.555 | 20 | 20 | fits | 138,791 | 136 | 0.330 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 305,064 | 3.051 | 20 | 24 | fits | 134,092 | 86 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 242,076 | 2.421 | 20 | 50 | fits | 141,870 | 139 | 0.550 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 763,768 | 7.638 | 20 | 20 | fits | 134,092 | 86 | 0.490 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 281,755 | 2.818 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 181,263 | 1.813 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 209,051 | 2.091 | 49 | 49 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 409,038 | 4.090 | 20 | 20 | fits | 153,917 | 210 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 306,842 | 3.068 | 20 | 200 | fits | 149,489 | 176 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 460,143 | 4.601 | 20 | 200 | fits | 153,917 | 210 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 307,766 | 3.078 | 20 | 20 | fits | 149,489 | 176 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 607,716 | 6.077 | 20 | 20 | fits | 136,245 | 62 | 0.645 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 161,917 | 1.619 | 20 | 24 | fits | 148,966 | 145 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 310,416 | 3.104 | 20 | 24 | fits | 149,489 | 176 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 310,350 | 3.103 | 20 | 50 | fits | 149,489 | 176 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 463,871 | 4.639 | 20 | 50 | fits | 153,917 | 210 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 610,674 | 6.107 | 20 | 20 | fits | 136,245 | 62 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 851,816 | 8.518 | 20 | 20 | fits | 110,006 | 48 | 0.506 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 394,768 | 3.948 | 20 | 20 | fits | 154,625 | 196 | 0.329 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 300,904 | 3.009 | 20 | 200 | fits | 149,410 | 192 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 454,913 | 4.549 | 20 | 200 | fits | 154,625 | 196 | 0.329 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 301,828 | 3.018 | 20 | 20 | fits | 149,410 | 192 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 587,752 | 5.878 | 20 | 20 | fits | 132,135 | 55 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 156,058 | 1.561 | 20 | 24 | fits | 148,989 | 145 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 304,478 | 3.045 | 20 | 24 | fits | 149,410 | 192 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 304,412 | 3.044 | 20 | 50 | fits | 149,410 | 192 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 458,641 | 4.586 | 20 | 50 | fits | 154,625 | 196 | 0.329 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 590,710 | 5.907 | 20 | 20 | fits | 132,135 | 55 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 825,784 | 8.258 | 20 | 20 | fits | 109,737 | 49 | 0.497 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 414,153 | 4.142 | 20 | 20 | fits | 156,632 | 211 | 0.361 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 309,866 | 3.099 | 20 | 200 | fits | 150,938 | 180 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 465,882 | 4.659 | 20 | 200 | fits | 156,632 | 211 | 0.361 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 310,790 | 3.108 | 20 | 20 | fits | 150,938 | 180 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 611,159 | 6.112 | 20 | 20 | fits | 134,034 | 56 | 0.641 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 163,492 | 1.635 | 20 | 24 | fits | 147,758 | 142 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 313,440 | 3.134 | 20 | 24 | fits | 150,938 | 180 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 313,374 | 3.134 | 20 | 50 | fits | 150,938 | 180 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 469,610 | 4.696 | 20 | 50 | fits | 156,632 | 211 | 0.361 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 614,117 | 6.141 | 20 | 20 | fits | 134,034 | 56 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 849,143 | 8.491 | 20 | 20 | fits | 109,633 | 48 | 0.497 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 395,569 | 3.956 | 20 | 20 | fits | 153,811 | 210 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 293,479 | 2.935 | 20 | 200 | fits | 149,384 | 176 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 446,674 | 4.467 | 20 | 200 | fits | 153,811 | 210 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 294,403 | 2.944 | 20 | 20 | fits | 149,384 | 176 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 594,751 | 5.948 | 20 | 20 | fits | 136,865 | 62 | 0.647 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 148,659 | 1.487 | 20 | 24 | fits | 147,749 | 142 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 297,053 | 2.971 | 20 | 24 | fits | 149,384 | 176 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 296,987 | 2.970 | 20 | 50 | fits | 149,384 | 176 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 450,402 | 4.504 | 20 | 50 | fits | 153,811 | 210 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 597,709 | 5.977 | 20 | 20 | fits | 136,865 | 62 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 838,408 | 8.384 | 20 | 20 | fits | 115,302 | 54 | 0.551 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 411,917 | 4.119 | 20 | 20 | fits | 153,612 | 209 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 309,744 | 3.097 | 20 | 200 | fits | 152,007 | 181 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 462,740 | 4.627 | 20 | 200 | fits | 153,612 | 209 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 310,668 | 3.107 | 20 | 20 | fits | 152,007 | 181 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 594,950 | 5.949 | 20 | 20 | fits | 131,506 | 55 | 0.621 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 152,672 | 1.527 | 20 | 24 | fits | 147,822 | 143 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 313,318 | 3.133 | 20 | 24 | fits | 152,007 | 181 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 313,252 | 3.133 | 20 | 50 | fits | 152,007 | 181 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 466,468 | 4.665 | 20 | 50 | fits | 153,612 | 209 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 597,908 | 5.979 | 20 | 20 | fits | 131,506 | 55 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 832,825 | 8.328 | 20 | 20 | fits | 109,580 | 48 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 404,870 | 4.049 | 20 | 20 | fits | 149,672 | 194 | 0.360 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 306,684 | 3.067 | 20 | 200 | fits | 149,293 | 192 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 455,740 | 4.557 | 20 | 200 | fits | 149,672 | 194 | 0.360 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 307,608 | 3.076 | 20 | 20 | fits | 149,293 | 192 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 600,512 | 6.005 | 20 | 20 | fits | 133,573 | 62 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 161,955 | 1.620 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 310,258 | 3.103 | 20 | 24 | fits | 149,293 | 192 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 310,192 | 3.102 | 20 | 50 | fits | 149,293 | 192 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 459,468 | 4.595 | 20 | 50 | fits | 149,672 | 194 | 0.360 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 603,470 | 6.035 | 20 | 20 | fits | 133,573 | 62 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 847,219 | 8.472 | 20 | 20 | fits | 118,298 | 52 | 0.483 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 389,889 | 3.899 | 20 | 20 | fits | 152,750 | 205 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 306,753 | 3.068 | 20 | 200 | fits | 150,963 | 180 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 458,887 | 4.589 | 20 | 200 | fits | 152,750 | 205 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 307,677 | 3.077 | 20 | 20 | fits | 150,963 | 180 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 591,726 | 5.917 | 20 | 20 | fits | 132,135 | 55 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 160,354 | 1.604 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 310,327 | 3.103 | 20 | 24 | fits | 150,963 | 180 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 310,261 | 3.103 | 20 | 50 | fits | 150,963 | 180 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 462,615 | 4.626 | 20 | 50 | fits | 152,750 | 205 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 594,684 | 5.947 | 20 | 20 | fits | 132,135 | 55 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 846,923 | 8.469 | 20 | 20 | fits | 115,794 | 55 | 0.578 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 414,488 | 4.145 | 20 | 20 | fits | 152,324 | 204 | 0.341 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 314,407 | 3.144 | 20 | 200 | fits | 153,510 | 185 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 466,115 | 4.661 | 20 | 200 | fits | 152,324 | 204 | 0.341 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 315,331 | 3.153 | 20 | 20 | fits | 153,510 | 185 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 598,950 | 5.989 | 20 | 20 | fits | 132,131 | 55 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 155,832 | 1.558 | 20 | 24 | fits | 147,764 | 143 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 317,981 | 3.180 | 20 | 24 | fits | 153,510 | 185 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 317,915 | 3.179 | 20 | 50 | fits | 153,510 | 185 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 469,843 | 4.698 | 20 | 50 | fits | 152,324 | 204 | 0.341 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 601,908 | 6.019 | 20 | 20 | fits | 132,131 | 55 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 836,926 | 8.369 | 20 | 20 | fits | 109,580 | 48 | 0.495 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 35,367 | 0.354 | 20 | 20 | fits | 38,321 | 27 (35) | 0.811 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 25,270 | 0.253 | 20 | 20 | fits | 34,411 | 23 (14) | 0.845 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 24,994 | 0.250 | 20 | 20 | fits | 34,217 | 24 (14) | 0.834 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 24,582 | 0.246 | 20 | 20 | fits | 40,980 | 27 (35) | 0.811 |
| LINK_UP | `adp.link_up.if0` | 2,856 | 0.029 | 20 | 200 | fits | 33,635 | 43 (11) | 0.730 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,239 | 0.142 | 20 | 200 | fits | 27,591 | 23 (39) | 0.747 |
| LINK_DOWN | `adp.link_down.if0` | 2,247 | 0.022 | 20 | 200 | fits | 30,867 | 23 (9) | 0.784 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
