### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 22 paths and 6 of 323 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.292 (6.967) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.865 (7.079) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.225 (0.780) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.383 (2.363) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.693 (64.074) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.400 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 7.283 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.527 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 10.350 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 4.972 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 13.892 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.686 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 8.322 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.677 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.147 | fits | 7 adp | 26 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 5.076 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.722 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.040 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.712 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.184 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.061 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-3.service.srp.last.if1` (backlog-adp@verify-3) | 15.561 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 16.648 | 17 | 178,348 (1.783) | yes | - |
| backlog-adp@blank-1 | 0 | 16.140 | 17 | 178,321 (1.783) | yes | - |
| backlog-adp@blank-2 | 0 | 16.159 | 17 | 178,321 (1.783) | yes | - |
| backlog-adp@blank-3 | 0 | 17.412 | 19 | 178,321 (1.783) | yes | - |
| backlog-adp@blank-4 | 0 | 16.345 | 18 | 178,321 (1.783) | yes | - |
| backlog-adp@blank-5 | 0 | 16.399 | 18 | 178,321 (1.783) | yes | - |
| backlog-adp@blank-6 | 0 | 16.347 | 18 | 157,470 (1.575) | yes | - |
| backlog-adp@blank-7 | 0 | 16.124 | 17 | 185,058 (1.851) | yes | - |
| backlog-adp@program-0 | 0 | 16.072 | 17 | 177,718 (1.777) | yes | - |
| backlog-adp@program-1 | 0 | 16.333 | 18 | 177,718 (1.777) | yes | - |
| backlog-adp@program-2 | 0 | 16.392 | 18 | 177,718 (1.777) | yes | - |
| backlog-adp@program-3 | 0 | 16.475 | 18 | 184,455 (1.845) | yes | - |
| backlog-adp@program-4 | 0 | 15.674 | 18 | 177,754 (1.778) | yes | - |
| backlog-adp@program-5 | 0 | 15.569 | 18 | 177,754 (1.778) | yes | - |
| backlog-adp@program-6 | 0 | 15.698 | 18 | 177,754 (1.778) | yes | - |
| backlog-adp@program-7 | 0 | 15.658 | 18 | 184,532 (1.845) | yes | - |
| backlog-adp@verify-0 | 0 | 16.321 | 17 | 178,467 (1.785) | yes | - |
| backlog-adp@verify-1 | 0 | 16.542 | 18 | 178,481 (1.785) | yes | - |
| backlog-adp@verify-2 | 0 | 18.006 | 19 | 178,481 (1.785) | yes | - |
| backlog-adp@verify-3 | 0 | 16.926 | 19 | 178,481 (1.785) | yes | - |
| backlog-adp@verify-4 | 0 | 16.626 | 18 | 178,481 (1.785) | yes | - |
| backlog-adp@verify-5 | 0 | 16.445 | 17 | 178,481 (1.785) | yes | - |
| backlog-adp@verify-6 | 0 | 16.645 | 18 | 177,567 (1.776) | yes | - |
| backlog-adp@verify-7 | 0 | 16.777 | 18 | 185,218 (1.852) | yes | - |
| backlog | 0 | 13.497 | 19 | 149,609 (1.496) | yes | - |
| backlog-adp | 0 | 15.487 | 18 | 177,483 (1.775) | yes | - |
| backlog-adp-refill | 0 | 41.301 | 23 | 177,483 (1.775) | yes | - |
| backlog-owed | 0 | 360.451 | 66 | 177,129 (1.771) | yes | - |

Composed maximum over the 4 backlog windows: 177,483 CPU cycles (1.775 ms), backlog-adp.
Over the windows that released their whole load only: 177,483 (1.775 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 8499 | 0 | 162,677 (1.627) | fits |
| save-starved | 53926 | 0 | 166,293 (1.663) | fits |
| backlog-adp@blank-0 | 380 | 0 | 178,348 (1.783) | fits |
| backlog-adp@blank-1 | 380 | 0 | 178,321 (1.783) | fits |
| backlog-adp@blank-2 | 381 | 0 | 178,321 (1.783) | fits |
| backlog-adp@blank-3 | 382 | 0 | 178,321 (1.783) | fits |
| backlog-adp@blank-4 | 381 | 0 | 178,321 (1.783) | fits |
| backlog-adp@blank-5 | 381 | 0 | 178,321 (1.783) | fits |
| backlog-adp@blank-6 | 381 | 0 | 157,470 (1.575) | fits |
| backlog-adp@blank-7 | 380 | 0 | 185,058 (1.851) | fits |
| backlog-adp@program-0 | 489 | 0 | 177,718 (1.777) | fits |
| backlog-adp@program-1 | 490 | 0 | 177,718 (1.777) | fits |
| backlog-adp@program-2 | 490 | 0 | 177,718 (1.777) | fits |
| backlog-adp@program-3 | 490 | 0 | 184,455 (1.845) | fits |
| backlog-adp@program-4 | 491 | 0 | 177,754 (1.778) | fits |
| backlog-adp@program-5 | 491 | 0 | 177,754 (1.778) | fits |
| backlog-adp@program-6 | 491 | 0 | 177,754 (1.778) | fits |
| backlog-adp@program-7 | 491 | 0 | 184,532 (1.845) | fits |
| backlog-adp@verify-0 | 595 | 0 | 178,467 (1.785) | fits |
| backlog-adp@verify-1 | 596 | 0 | 178,481 (1.785) | fits |
| backlog-adp@verify-2 | 597 | 0 | 178,481 (1.785) | fits |
| backlog-adp@verify-3 | 597 | 0 | 178,481 (1.785) | fits |
| backlog-adp@verify-4 | 596 | 0 | 178,481 (1.785) | fits |
| backlog-adp@verify-5 | 595 | 0 | 178,481 (1.785) | fits |
| backlog-adp@verify-6 | 596 | 0 | 177,567 (1.776) | fits |
| backlog-adp@verify-7 | 596 | 0 | 185,218 (1.852) | fits |
| save | 617 | 0 | 132,187 (1.322) | fits |
| backlog | 302 | 0 | 149,609 (1.496) | fits |
| backlog-adp | 310 | 0 | 177,483 (1.775) | fits |
| backlog-adp-refill | 315 | 0 | 177,483 (1.775) | fits |
| backlog-owed | 360 | 0 | 177,129 (1.771) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---|---|
| save-held | 4731.145 | 12,110 | 370 | 17.659 | no | within |
| save-starved | 12088.002 | 12,110 | 370 | 31.417 | yes | within |
| save | 4698.271 | 12,110 | 370 | 12.536 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1514 | 124,882 (1.249) | 95,673 (0.957) |
| save-starved | 686 | 96,278 (0.963) | 95,857 (0.959) |
| backlog-adp@blank-0 | 337 | 95,459 (0.955) | 76,082 (0.761) |
| backlog-adp@blank-1 | 337 | 95,459 (0.955) | 76,082 (0.761) |
| backlog-adp@blank-2 | 337 | 94,766 (0.948) | 76,077 (0.761) |
| backlog-adp@blank-3 | 338 | 94,716 (0.947) | 76,082 (0.761) |
| backlog-adp@blank-4 | 337 | 94,662 (0.947) | 76,059 (0.761) |
| backlog-adp@blank-5 | 337 | 94,769 (0.948) | 76,082 (0.761) |
| backlog-adp@blank-6 | 337 | 94,637 (0.946) | 76,082 (0.761) |
| backlog-adp@blank-7 | 337 | 95,459 (0.955) | 76,082 (0.761) |
| backlog-adp@program-0 | 443 | 118,917 (1.189) | 82,074 (0.821) |
| backlog-adp@program-1 | 443 | 118,917 (1.189) | 82,009 (0.820) |
| backlog-adp@program-2 | 443 | 118,917 (1.189) | 82,009 (0.820) |
| backlog-adp@program-3 | 443 | 118,917 (1.189) | 82,009 (0.820) |
| backlog-adp@program-4 | 444 | 118,917 (1.189) | 81,473 (0.815) |
| backlog-adp@program-5 | 444 | 118,917 (1.189) | 81,473 (0.815) |
| backlog-adp@program-6 | 444 | 118,917 (1.189) | 81,473 (0.815) |
| backlog-adp@program-7 | 444 | 118,917 (1.189) | 81,473 (0.815) |
| backlog-adp@verify-0 | 546 | 118,917 (1.189) | 95,453 (0.955) |
| backlog-adp@verify-1 | 546 | 118,917 (1.189) | 95,453 (0.955) |
| backlog-adp@verify-2 | 547 | 118,917 (1.189) | 95,453 (0.955) |
| backlog-adp@verify-3 | 546 | 118,917 (1.189) | 95,453 (0.955) |
| backlog-adp@verify-4 | 546 | 118,917 (1.189) | 95,453 (0.955) |
| backlog-adp@verify-5 | 546 | 118,917 (1.189) | 95,453 (0.955) |
| backlog-adp@verify-6 | 546 | 118,917 (1.189) | 95,453 (0.955) |
| backlog-adp@verify-7 | 546 | 118,917 (1.189) | 95,453 (0.955) |
| save | 585 | 124,690 (1.247) | 95,501 (0.955) |
| backlog | 266 | 45,570 (0.456) | 3,079 (0.031) |
| backlog-adp | 271 | 45,570 (0.456) | 3,079 (0.031) |
| backlog-adp-refill | 273 | 45,570 (0.456) | 3,079 (0.031) |
| backlog-owed | 305 | 45,693 (0.457) | 3,079 (0.031) |

Longest pass that carries a step: 124,882 CPU cycles (1.249 ms), save-held; longest step: 95,857 (0.959 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 443,893 | 4.439 | 20 | 200 | fits | 110,891 | 85 | 0.561 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 709,232 | 7.092 | 20 | 20 | fits | 77,892 | 37 | 0.610 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 976,041 | 9.760 | 20 | 24 | fits | 31,471 | 23 | 0.528 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 485,074 | 4.851 | 20 | 50 | fits | 100,793 | 56 | 0.643 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 1,338,458 | 13.385 | 18 | 18 | fits | 61,828 | 31 | 0.698 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 452,697 | 4.527 | 20 | 200 | fits | 114,111 | 91 | 0.588 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 728,274 | 7.283 | 20 | 20 | fits | 81,411 | 43 | 0.646 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 1,034,994 | 10.350 | 20 | 24 | fits | 34,190 | 29 | 0.595 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 497,224 | 4.972 | 20 | 50 | fits | 104,139 | 62 | 0.665 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,389,247 | 13.892 | 18 | 18 | fits | 64,940 | 37 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 486,504 | 4.865 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 167,707 | 1.677 | 20 | 200 | fits | 108,385 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 614,711 | 6.147 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 168,619 | 1.686 | 20 | 20 | fits | 108,385 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 832,162 | 8.322 | 20 | 20 | fits | 98,721 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 172,204 | 1.722 | 20 | 24 | fits | 108,385 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,530,632 | 15.306 | 20 | 24 | fits | 62,297 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 171,164 | 1.712 | 20 | 50 | fits | 108,385 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 618,387 | 6.184 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 349,057 | 3.491 | 18 | 18 | fits | 178,348 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,528,097 | 15.281 | 18 | 18 | fits | 62,297 | 31 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 435,644 | 4.356 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 116,874 | 1.169 | 20 | 200 | fits | 108,113 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 563,851 | 5.639 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 117,786 | 1.178 | 20 | 20 | fits | 108,113 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 781,302 | 7.813 | 20 | 20 | fits | 98,721 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 121,371 | 1.214 | 20 | 24 | fits | 108,113 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,479,833 | 14.798 | 20 | 24 | fits | 62,297 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 120,331 | 1.203 | 20 | 50 | fits | 108,113 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 567,527 | 5.675 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 298,197 | 2.982 | 18 | 18 | fits | 178,321 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,477,298 | 14.773 | 18 | 18 | fits | 62,297 | 31 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 421,896 | 4.219 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 103,126 | 1.031 | 20 | 200 | fits | 108,113 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 550,103 | 5.501 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 104,038 | 1.040 | 20 | 20 | fits | 108,113 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 738,898 | 7.389 | 20 | 20 | fits | 70,065 | 25 | 0.658 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 107,623 | 1.076 | 20 | 24 | fits | 108,113 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,434,467 | 14.345 | 20 | 24 | fits | 61,863 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 106,583 | 1.066 | 20 | 50 | fits | 108,113 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 553,779 | 5.538 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 284,449 | 2.844 | 18 | 18 | fits | 178,321 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,479,919 | 14.799 | 18 | 18 | fits | 47,987 | 20 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 426,734 | 4.267 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 107,964 | 1.080 | 20 | 200 | fits | 108,157 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 554,941 | 5.549 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 108,876 | 1.089 | 20 | 20 | fits | 108,157 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 751,385 | 7.514 | 20 | 20 | fits | 106,921 | 40 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 112,461 | 1.125 | 20 | 24 | fits | 108,157 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,440,409 | 14.404 | 20 | 24 | fits | 62,212 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 111,421 | 1.114 | 20 | 50 | fits | 108,157 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 558,617 | 5.586 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 289,287 | 2.893 | 18 | 18 | fits | 178,321 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,485,790 | 14.858 | 18 | 18 | fits | 47,916 | 20 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 431,484 | 4.315 | 20 | 20 | fits | 109,922 | 74 | 0.607 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 112,714 | 1.127 | 20 | 200 | fits | 108,113 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 530,303 | 5.303 | 20 | 200 | fits | 109,922 | 74 | 0.607 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 113,626 | 1.136 | 20 | 20 | fits | 108,113 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 755,991 | 7.560 | 20 | 20 | fits | 98,942 | 34 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 117,211 | 1.172 | 20 | 24 | fits | 108,113 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,445,543 | 14.455 | 20 | 24 | fits | 62,297 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 116,171 | 1.162 | 20 | 50 | fits | 108,113 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 533,979 | 5.340 | 20 | 50 | fits | 109,922 | 74 | 0.607 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 294,037 | 2.940 | 18 | 18 | fits | 178,321 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,498,648 | 14.986 | 18 | 18 | fits | 55,640 | 26 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 413,898 | 4.139 | 20 | 20 | fits | 147,356 | 89 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 117,552 | 1.176 | 20 | 200 | fits | 108,157 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 542,296 | 5.423 | 20 | 200 | fits | 147,356 | 89 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 118,464 | 1.185 | 20 | 20 | fits | 108,157 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 759,713 | 7.597 | 20 | 20 | fits | 98,862 | 34 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 122,049 | 1.220 | 20 | 24 | fits | 108,157 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,458,328 | 14.583 | 20 | 24 | fits | 62,361 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 121,009 | 1.210 | 20 | 50 | fits | 108,157 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 545,972 | 5.460 | 20 | 50 | fits | 147,356 | 89 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 298,875 | 2.989 | 18 | 18 | fits | 178,321 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,503,897 | 15.039 | 18 | 18 | fits | 48,104 | 20 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 420,028 | 4.200 | 20 | 20 | fits | 140,655 | 83 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 103,804 | 1.038 | 20 | 200 | fits | 108,157 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 549,162 | 5.492 | 20 | 200 | fits | 140,655 | 83 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 104,716 | 1.047 | 20 | 20 | fits | 108,157 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 767,104 | 7.671 | 20 | 20 | fits | 99,035 | 34 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 108,301 | 1.083 | 20 | 24 | fits | 108,157 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,465,549 | 14.655 | 20 | 24 | fits | 62,266 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 107,261 | 1.073 | 20 | 50 | fits | 108,157 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 552,838 | 5.528 | 20 | 50 | fits | 140,655 | 83 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 254,648 | 2.546 | 18 | 18 | fits | 147,842 | 136 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,498,875 | 14.989 | 18 | 18 | fits | 35,861 | 17 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 434,080 | 4.341 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 108,554 | 1.086 | 20 | 200 | fits | 108,113 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 562,287 | 5.623 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 109,466 | 1.095 | 20 | 20 | fits | 108,113 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 779,738 | 7.797 | 20 | 20 | fits | 98,721 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 113,051 | 1.131 | 20 | 24 | fits | 108,113 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,478,293 | 14.783 | 20 | 24 | fits | 62,297 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 112,011 | 1.120 | 20 | 50 | fits | 108,113 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 565,963 | 5.660 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 296,614 | 2.966 | 18 | 18 | fits | 185,058 | 145 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,475,758 | 14.758 | 18 | 18 | fits | 62,297 | 31 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 422,501 | 4.225 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 104,259 | 1.043 | 20 | 200 | fits | 108,597 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 550,708 | 5.507 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 105,171 | 1.052 | 20 | 20 | fits | 108,597 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 768,224 | 7.682 | 20 | 20 | fits | 98,786 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 108,756 | 1.088 | 20 | 24 | fits | 108,597 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,466,779 | 14.668 | 20 | 24 | fits | 62,297 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 107,716 | 1.077 | 20 | 50 | fits | 108,597 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 554,384 | 5.544 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 284,979 | 2.850 | 18 | 18 | fits | 177,718 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,464,244 | 14.642 | 18 | 18 | fits | 62,297 | 31 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 432,089 | 4.321 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 113,847 | 1.138 | 20 | 200 | fits | 108,597 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 560,296 | 5.603 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 114,759 | 1.148 | 20 | 20 | fits | 108,597 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 756,805 | 7.568 | 20 | 20 | fits | 106,986 | 40 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 118,344 | 1.183 | 20 | 24 | fits | 108,597 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,445,829 | 14.458 | 20 | 24 | fits | 62,212 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 117,304 | 1.173 | 20 | 50 | fits | 108,597 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 563,972 | 5.640 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 294,567 | 2.946 | 18 | 18 | fits | 177,718 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,491,210 | 14.912 | 18 | 18 | fits | 47,916 | 20 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 418,679 | 4.187 | 20 | 20 | fits | 148,433 | 89 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 104,849 | 1.048 | 20 | 200 | fits | 108,553 | 140 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 547,975 | 5.480 | 20 | 200 | fits | 148,433 | 89 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 105,761 | 1.058 | 20 | 20 | fits | 108,553 | 140 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 765,811 | 7.658 | 20 | 20 | fits | 98,940 | 34 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 109,346 | 1.093 | 20 | 24 | fits | 108,553 | 140 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,463,797 | 14.638 | 20 | 24 | fits | 71,098 | 37 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 108,306 | 1.083 | 20 | 50 | fits | 108,553 | 140 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 551,651 | 5.517 | 20 | 50 | fits | 148,433 | 89 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 285,569 | 2.856 | 18 | 18 | fits | 177,718 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,497,184 | 14.972 | 18 | 18 | fits | 35,922 | 17 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 439,435 | 4.394 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 114,437 | 1.144 | 20 | 200 | fits | 108,553 | 140 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 567,642 | 5.676 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 115,349 | 1.153 | 20 | 20 | fits | 108,553 | 140 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 785,158 | 7.852 | 20 | 20 | fits | 98,786 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 118,934 | 1.189 | 20 | 24 | fits | 108,553 | 140 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,472,184 | 14.722 | 20 | 24 | fits | 62,266 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 117,894 | 1.179 | 20 | 50 | fits | 108,553 | 140 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 571,318 | 5.713 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 301,894 | 3.019 | 18 | 18 | fits | 184,455 | 145 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,505,510 | 15.055 | 18 | 18 | fits | 35,861 | 17 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 436,314 | 4.363 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 118,036 | 1.180 | 20 | 200 | fits | 108,625 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 564,521 | 5.645 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 118,948 | 1.189 | 20 | 20 | fits | 108,625 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 782,037 | 7.820 | 20 | 20 | fits | 98,786 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 122,533 | 1.225 | 20 | 24 | fits | 108,625 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,469,175 | 14.692 | 20 | 24 | fits | 62,266 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 121,493 | 1.215 | 20 | 50 | fits | 108,625 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 568,197 | 5.682 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 298,792 | 2.988 | 18 | 18 | fits | 177,754 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,502,501 | 15.025 | 18 | 18 | fits | 35,861 | 17 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 427,404 | 4.274 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 109,126 | 1.091 | 20 | 200 | fits | 108,669 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 555,611 | 5.556 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 110,038 | 1.100 | 20 | 20 | fits | 108,669 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 769,765 | 7.698 | 20 | 20 | fits | 107,245 | 40 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 113,623 | 1.136 | 20 | 24 | fits | 108,669 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,458,852 | 14.589 | 20 | 24 | fits | 62,204 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 112,583 | 1.126 | 20 | 50 | fits | 108,669 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 559,287 | 5.593 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 289,882 | 2.899 | 18 | 18 | fits | 177,754 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,491,990 | 14.920 | 18 | 18 | fits | 35,673 | 17 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 414,568 | 4.146 | 20 | 20 | fits | 147,432 | 89 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 118,714 | 1.187 | 20 | 200 | fits | 108,669 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 543,042 | 5.430 | 20 | 200 | fits | 147,432 | 89 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 119,626 | 1.196 | 20 | 20 | fits | 108,669 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 760,524 | 7.605 | 20 | 20 | fits | 98,927 | 34 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 123,211 | 1.232 | 20 | 24 | fits | 108,669 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,459,075 | 14.591 | 20 | 24 | fits | 71,237 | 37 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 122,171 | 1.222 | 20 | 50 | fits | 108,669 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 546,718 | 5.467 | 20 | 50 | fits | 147,432 | 89 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 299,470 | 2.995 | 18 | 18 | fits | 177,754 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,504,708 | 15.047 | 18 | 18 | fits | 48,168 | 20 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 434,791 | 4.348 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 109,716 | 1.097 | 20 | 200 | fits | 108,625 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 562,998 | 5.630 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 110,628 | 1.106 | 20 | 20 | fits | 108,625 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 780,514 | 7.805 | 20 | 20 | fits | 98,786 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 114,213 | 1.142 | 20 | 24 | fits | 108,625 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,467,540 | 14.675 | 20 | 24 | fits | 62,266 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 113,173 | 1.132 | 20 | 50 | fits | 108,625 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 566,674 | 5.667 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 297,250 | 2.973 | 18 | 18 | fits | 184,532 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,500,866 | 15.009 | 18 | 18 | fits | 35,861 | 17 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 422,808 | 4.228 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 103,892 | 1.039 | 20 | 200 | fits | 108,472 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 551,015 | 5.510 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 104,804 | 1.048 | 20 | 20 | fits | 108,472 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 768,531 | 7.685 | 20 | 20 | fits | 98,786 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 108,389 | 1.084 | 20 | 24 | fits | 108,472 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,497,009 | 14.970 | 20 | 24 | fits | 92,220 | 45 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 107,349 | 1.073 | 20 | 50 | fits | 108,472 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 554,691 | 5.547 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 285,361 | 2.854 | 18 | 18 | fits | 178,467 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,494,474 | 14.945 | 18 | 18 | fits | 92,220 | 45 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 427,492 | 4.275 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 108,562 | 1.086 | 20 | 200 | fits | 108,156 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 555,699 | 5.557 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 109,474 | 1.095 | 20 | 20 | fits | 108,156 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 773,215 | 7.732 | 20 | 20 | fits | 98,786 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 113,059 | 1.131 | 20 | 24 | fits | 108,156 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,471,785 | 14.718 | 20 | 24 | fits | 91,098 | 45 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 112,019 | 1.120 | 20 | 50 | fits | 108,156 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 559,375 | 5.594 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 290,045 | 2.900 | 18 | 18 | fits | 178,481 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,517,503 | 15.175 | 18 | 18 | fits | 48,253 | 20 | 0.763 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 432,330 | 4.323 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 113,400 | 1.134 | 20 | 200 | fits | 108,200 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 560,537 | 5.605 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 114,312 | 1.143 | 20 | 20 | fits | 108,200 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 774,691 | 7.747 | 20 | 20 | fits | 107,245 | 40 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 117,897 | 1.179 | 20 | 24 | fits | 108,200 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,451,257 | 14.513 | 20 | 24 | fits | 49,683 | 27 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 116,857 | 1.169 | 20 | 50 | fits | 108,200 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 564,213 | 5.642 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 294,883 | 2.949 | 18 | 18 | fits | 178,481 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,525,648 | 15.256 | 18 | 18 | fits | 76,926 | 34 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 437,080 | 4.371 | 20 | 20 | fits | 109,922 | 74 | 0.607 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 118,150 | 1.181 | 20 | 200 | fits | 108,156 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 535,899 | 5.359 | 20 | 200 | fits | 109,922 | 74 | 0.607 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 119,062 | 1.191 | 20 | 20 | fits | 108,156 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 761,652 | 7.617 | 20 | 20 | fits | 99,007 | 34 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 122,647 | 1.226 | 20 | 24 | fits | 108,156 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,439,781 | 14.398 | 20 | 24 | fits | 50,874 | 27 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 121,607 | 1.216 | 20 | 50 | fits | 108,156 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 539,575 | 5.396 | 20 | 50 | fits | 109,922 | 74 | 0.607 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 299,633 | 2.996 | 18 | 18 | fits | 178,481 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,556,111 | 15.561 | 18 | 18 | fits | 41,709 | 21 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 418,920 | 4.189 | 20 | 20 | fits | 148,433 | 89 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 104,402 | 1.044 | 20 | 200 | fits | 108,156 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 548,216 | 5.482 | 20 | 200 | fits | 148,433 | 89 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 105,314 | 1.053 | 20 | 20 | fits | 108,156 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 766,052 | 7.661 | 20 | 20 | fits | 98,940 | 34 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 108,899 | 1.089 | 20 | 24 | fits | 108,156 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,492,096 | 14.921 | 20 | 24 | fits | 99,156 | 51 | 0.746 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 107,859 | 1.079 | 20 | 50 | fits | 108,156 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 551,892 | 5.519 | 20 | 50 | fits | 148,433 | 89 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 285,885 | 2.859 | 18 | 18 | fits | 178,481 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,525,918 | 15.259 | 18 | 18 | fits | 36,357 | 17 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 435,438 | 4.354 | 20 | 20 | fits | 139,322 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 109,240 | 1.092 | 20 | 200 | fits | 108,200 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 563,683 | 5.637 | 20 | 200 | fits | 139,322 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 110,152 | 1.102 | 20 | 20 | fits | 108,200 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 781,199 | 7.812 | 20 | 20 | fits | 98,786 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 113,737 | 1.137 | 20 | 24 | fits | 108,200 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,509,643 | 15.096 | 20 | 24 | fits | 62,515 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 112,697 | 1.127 | 20 | 50 | fits | 108,200 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 567,359 | 5.674 | 20 | 50 | fits | 139,322 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 290,723 | 2.907 | 18 | 18 | fits | 178,481 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,507,108 | 15.071 | 18 | 18 | fits | 62,515 | 31 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 407,412 | 4.074 | 20 | 20 | fits | 141,264 | 83 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 113,990 | 1.140 | 20 | 200 | fits | 108,156 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 537,064 | 5.371 | 20 | 200 | fits | 141,264 | 83 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 114,902 | 1.149 | 20 | 20 | fits | 108,156 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 754,606 | 7.546 | 20 | 20 | fits | 98,770 | 34 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 118,487 | 1.185 | 20 | 24 | fits | 108,156 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,452,990 | 14.530 | 20 | 24 | fits | 62,297 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 117,447 | 1.174 | 20 | 50 | fits | 108,156 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 540,740 | 5.407 | 20 | 50 | fits | 141,264 | 83 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 399,411 | 3.994 | 18 | 18 | fits | 177,567 | 104 | 0.653 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,527,646 | 15.276 | 18 | 18 | fits | 77,191 | 34 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 444,514 | 4.445 | 20 | 20 | fits | 139,310 | 83 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 118,828 | 1.188 | 20 | 200 | fits | 108,200 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 572,721 | 5.727 | 20 | 200 | fits | 139,310 | 83 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 119,740 | 1.197 | 20 | 20 | fits | 108,200 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 790,237 | 7.902 | 20 | 20 | fits | 98,786 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 123,325 | 1.233 | 20 | 24 | fits | 108,200 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,507,446 | 15.074 | 20 | 24 | fits | 92,308 | 45 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 122,285 | 1.223 | 20 | 50 | fits | 108,200 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 576,397 | 5.764 | 20 | 50 | fits | 139,310 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 307,048 | 3.070 | 18 | 18 | fits | 185,218 | 145 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,541,080 | 15.411 | 18 | 18 | fits | 36,169 | 17 | 0.807 |
| an event behind 15 others | `backlog.event.if0` | 138,263 | 1.383 | 20 | 200 | fits | 108,819 | 125 | 0.543 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 629,158 | 6.292 | 20 | 20 | fits | 93,028 | 46 | 0.647 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 127,248 | 1.272 | 20 | 200 | fits | 127,456 | 143 | 0.529 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 507,614 | 5.076 | 20 | 200 | fits | 122,547 | 57 | 0.673 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 122,989 | 1.230 | 20 | 20 | fits | 127,456 | 143 | 0.529 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 691,457 | 6.915 | 20 | 20 | fits | 93,028 | 46 | 0.647 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 126,574 | 1.266 | 20 | 24 | fits | 127,456 | 143 | 0.529 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,191,476 | 11.915 | 20 | 24 | fits | 48,762 | 31 | 0.681 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 125,534 | 1.255 | 20 | 50 | fits | 127,456 | 143 | 0.529 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 506,119 | 5.061 | 20 | 50 | fits | 122,547 | 57 | 0.673 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 506,054 | 5.061 | 18 | 18 | fits | 122,547 | 57 | 0.673 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,290,370 | 12.904 | 18 | 18 | fits | 33,106 | 18 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 426,672 | 4.267 | 20 | 20 | fits | 148,148 | 89 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 100,751 | 1.008 | 20 | 200 | fits | 105,433 | 140 | 0.492 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 555,653 | 5.557 | 20 | 200 | fits | 148,148 | 89 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 101,663 | 1.017 | 20 | 20 | fits | 105,433 | 140 | 0.492 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 772,297 | 7.723 | 20 | 20 | fits | 98,173 | 34 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 105,248 | 1.052 | 20 | 24 | fits | 105,433 | 140 | 0.492 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,432,891 | 14.329 | 20 | 24 | fits | 33,506 | 22 | 0.635 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 104,208 | 1.042 | 20 | 50 | fits | 105,433 | 140 | 0.492 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 559,329 | 5.593 | 20 | 50 | fits | 148,148 | 89 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 281,236 | 2.812 | 18 | 18 | fits | 177,483 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,486,744 | 14.867 | 18 | 18 | fits | 56,388 | 26 | 0.780 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 22,485 | 0.225 | 20 | 20 | fits | 43,983 | 21 | 0.768 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 100,751 | 1.008 | 20 | 200 | fits | 105,433 | 140 | 0.492 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 57,843 | 0.578 | 20 | 200 | fits | 43,983 | 21 | 0.768 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 101,663 | 1.017 | 20 | 20 | fits | 105,433 | 140 | 0.492 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 751,927 | 7.519 | 20 | 20 | fits | 107,279 | 46 | 0.661 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 105,248 | 1.052 | 20 | 24 | fits | 105,433 | 140 | 0.492 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,378,461 | 13.785 | 20 | 24 | fits | 62,085 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 104,208 | 1.042 | 20 | 50 | fits | 105,433 | 140 | 0.492 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 539,591 | 5.396 | 20 | 50 | fits | 128,410 | 79 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 281,236 | 2.812 | 18 | 18 | fits | 177,483 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,423,987 | 14.240 | 18 | 18 | fits | 48,061 | 20 | 0.756 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,369,327 | 63.693 | 20 | 20 | MISS ceiling | 50,142 | 27 | 0.571 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,040,013 | 360.400 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,039,938 | 360.399 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,039,863 | 360.399 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,039,788 | 360.398 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 105,892 | 1.059 | 20 | 200 | fits | 103,377 | 134 | 0.496 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 507,068 | 5.071 | 20 | 200 | fits | 121,700 | 69 | 0.672 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 101,633 | 1.016 | 20 | 20 | fits | 103,377 | 134 | 0.496 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 696,174 | 6.962 | 20 | 20 | fits | 95,024 | 35 | 0.737 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 105,218 | 1.052 | 20 | 24 | fits | 103,377 | 134 | 0.496 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,503,976 | 65.040 | 20 | 24 | MISS ceiling | 31,460 | 23 | 0.528 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 104,178 | 1.042 | 20 | 50 | fits | 103,377 | 134 | 0.496 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 505,573 | 5.056 | 20 | 50 | fits | 121,700 | 69 | 0.672 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 383,808 | 3.838 | 18 | 18 | fits | 177,129 | 97 | 0.681 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,269,564 | 12.696 | 18 | 18 | fits | 47,060 | 21 | 0.738 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
