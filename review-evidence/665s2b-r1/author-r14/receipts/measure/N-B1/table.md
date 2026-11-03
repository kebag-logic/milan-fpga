### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 21 paths and 6 of 323 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.537 (3.863) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-0.adp_available.if0` (backlog-adp@verify-0) | 3.532 (5.230) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.116 (0.364) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.915 (1.485) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.102 (62.354) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.246 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 4.473 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.818 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 6.086 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 3.014 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.686 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 1.443 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.acmp.last.if0` (backlog-adp@verify-0) | 5.893 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 1.434 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.adp.last.if0` (backlog-adp@verify-0) | 4.396 | fits | 7 adp | 28 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 1.479 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.948 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 1.469 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 4.433 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.851 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.srp.last.if0` (backlog-adp@verify-0) | 11.220 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.257 | 18 | 109,779 (1.098) | yes | - |
| backlog-adp@blank-1 | 0 | 11.505 | 17 | 109,834 (1.098) | yes | - |
| backlog-adp@blank-2 | 0 | 11.572 | 18 | 109,690 (1.097) | yes | - |
| backlog-adp@blank-3 | 0 | 11.654 | 18 | 109,915 (1.099) | yes | - |
| backlog-adp@blank-4 | 0 | 11.638 | 18 | 109,834 (1.098) | yes | - |
| backlog-adp@blank-5 | 0 | 11.692 | 18 | 109,690 (1.097) | yes | - |
| backlog-adp@blank-6 | 0 | 11.589 | 18 | 109,834 (1.098) | yes | - |
| backlog-adp@blank-7 | 0 | 13.405 | 20 | 123,127 (1.231) | yes | - |
| backlog-adp@program-0 | 0 | 11.577 | 17 | 109,743 (1.097) | yes | - |
| backlog-adp@program-1 | 0 | 11.548 | 17 | 109,743 (1.097) | yes | - |
| backlog-adp@program-2 | 0 | 11.690 | 18 | 109,898 (1.099) | yes | - |
| backlog-adp@program-3 | 0 | 11.955 | 19 | 100,285 (1.003) | yes | - |
| backlog-adp@program-4 | 0 | 10.854 | 17 | 109,734 (1.097) | yes | - |
| backlog-adp@program-5 | 0 | 10.833 | 17 | 109,898 (1.099) | yes | - |
| backlog-adp@program-6 | 0 | 10.891 | 18 | 109,898 (1.099) | yes | - |
| backlog-adp@program-7 | 0 | 10.916 | 17 | 100,285 (1.003) | yes | - |
| backlog-adp@verify-0 | 0 | 12.281 | 18 | 109,911 (1.099) | yes | - |
| backlog-adp@verify-1 | 0 | 11.528 | 17 | 109,977 (1.100) | yes | - |
| backlog-adp@verify-2 | 0 | 11.596 | 18 | 109,822 (1.098) | yes | - |
| backlog-adp@verify-3 | 0 | 11.500 | 17 | 109,977 (1.100) | yes | - |
| backlog-adp@verify-4 | 0 | 11.567 | 17 | 109,623 (1.096) | yes | - |
| backlog-adp@verify-5 | 0 | 11.716 | 18 | 109,822 (1.098) | yes | - |
| backlog-adp@verify-6 | 0 | 11.612 | 18 | 109,977 (1.100) | yes | - |
| backlog-adp@verify-7 | 0 | 12.538 | 19 | 105,667 (1.057) | yes | - |
| backlog | 0 | 6.723 | 19 | 81,912 (0.819) | yes | - |
| backlog-adp | 0 | 10.902 | 18 | 110,257 (1.103) | yes | - |
| backlog-adp-refill | 0 | 40.661 | 24 | 110,257 (1.103) | yes | - |
| backlog-owed | 0 | 360.297 | 65 | 107,445 (1.074) | yes | - |

Composed maximum over the 4 backlog windows: 110,257 CPU cycles (1.103 ms), backlog-adp.
Over the windows that released their whole load only: 110,257 (1.103 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 331 | 0 | 109,779 (1.098) | fits |
| backlog-adp@blank-1 | 330 | 0 | 109,834 (1.098) | fits |
| backlog-adp@blank-2 | 331 | 0 | 109,690 (1.097) | fits |
| backlog-adp@blank-3 | 332 | 0 | 109,915 (1.099) | fits |
| backlog-adp@blank-4 | 331 | 0 | 109,834 (1.098) | fits |
| backlog-adp@blank-5 | 331 | 0 | 109,690 (1.097) | fits |
| backlog-adp@blank-6 | 331 | 0 | 109,834 (1.098) | fits |
| backlog-adp@blank-7 | 333 | 0 | 123,127 (1.231) | fits |
| backlog-adp@program-0 | 360 | 0 | 121,244 (1.212) | fits |
| backlog-adp@program-1 | 360 | 0 | 121,244 (1.212) | fits |
| backlog-adp@program-2 | 361 | 0 | 121,244 (1.212) | fits |
| backlog-adp@program-3 | 362 | 0 | 121,244 (1.212) | fits |
| backlog-adp@program-4 | 362 | 0 | 121,244 (1.212) | fits |
| backlog-adp@program-5 | 361 | 0 | 121,244 (1.212) | fits |
| backlog-adp@program-6 | 362 | 0 | 121,244 (1.212) | fits |
| backlog-adp@program-7 | 362 | 0 | 121,244 (1.212) | fits |
| backlog-adp@verify-0 | 388 | 0 | 121,244 (1.212) | fits |
| backlog-adp@verify-1 | 387 | 0 | 121,244 (1.212) | fits |
| backlog-adp@verify-2 | 388 | 0 | 121,244 (1.212) | fits |
| backlog-adp@verify-3 | 387 | 0 | 121,244 (1.212) | fits |
| backlog-adp@verify-4 | 388 | 0 | 121,244 (1.212) | fits |
| backlog-adp@verify-5 | 388 | 0 | 121,244 (1.212) | fits |
| backlog-adp@verify-6 | 388 | 0 | 121,244 (1.212) | fits |
| backlog-adp@verify-7 | 389 | 0 | 121,244 (1.212) | fits |
| save-held | 3395 | 0 | 89,106 (0.891) | fits |
| save-starved | 43629 | 0 | 91,373 (0.914) | fits |
| save | 602 | 0 | 120,990 (1.210) | fits |
| backlog | 293 | 0 | 81,912 (0.819) | fits |
| backlog-adp | 301 | 0 | 110,257 (1.103) | fits |
| backlog-adp-refill | 307 | 0 | 110,257 (1.103) | fits |
| backlog-owed | 350 | 0 | 107,445 (1.074) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---|---|
| save-held | 2018.119 | 4,070 | 102 | 14.630 | no | within |
| save-starved | 4048.086 | 4,070 | 102 | 30.970 | yes | within |
| save | 2018.397 | 4,070 | 102 | 10.942 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 299 | 84,823 (0.848) | 76,101 (0.761) |
| backlog-adp@blank-1 | 299 | 85,578 (0.856) | 76,101 (0.761) |
| backlog-adp@blank-2 | 299 | 84,823 (0.848) | 76,101 (0.761) |
| backlog-adp@blank-3 | 299 | 84,766 (0.848) | 76,101 (0.761) |
| backlog-adp@blank-4 | 299 | 84,811 (0.848) | 76,101 (0.761) |
| backlog-adp@blank-5 | 299 | 84,703 (0.847) | 76,077 (0.761) |
| backlog-adp@blank-6 | 299 | 84,787 (0.848) | 76,077 (0.761) |
| backlog-adp@blank-7 | 300 | 123,127 (1.231) | 76,193 (0.762) |
| backlog-adp@program-0 | 328 | 121,244 (1.212) | 81,652 (0.817) |
| backlog-adp@program-1 | 328 | 121,244 (1.212) | 81,652 (0.817) |
| backlog-adp@program-2 | 328 | 121,244 (1.212) | 81,652 (0.817) |
| backlog-adp@program-3 | 329 | 121,244 (1.212) | 81,652 (0.817) |
| backlog-adp@program-4 | 329 | 121,244 (1.212) | 80,626 (0.806) |
| backlog-adp@program-5 | 329 | 121,244 (1.212) | 80,626 (0.806) |
| backlog-adp@program-6 | 329 | 121,244 (1.212) | 80,626 (0.806) |
| backlog-adp@program-7 | 329 | 121,244 (1.212) | 80,626 (0.806) |
| backlog-adp@verify-0 | 355 | 121,244 (1.212) | 95,071 (0.951) |
| backlog-adp@verify-1 | 355 | 121,244 (1.212) | 95,071 (0.951) |
| backlog-adp@verify-2 | 355 | 121,244 (1.212) | 95,071 (0.951) |
| backlog-adp@verify-3 | 355 | 121,244 (1.212) | 95,071 (0.951) |
| backlog-adp@verify-4 | 355 | 121,244 (1.212) | 95,071 (0.951) |
| backlog-adp@verify-5 | 355 | 121,244 (1.212) | 95,071 (0.951) |
| backlog-adp@verify-6 | 355 | 121,244 (1.212) | 95,071 (0.951) |
| backlog-adp@verify-7 | 356 | 121,244 (1.212) | 95,071 (0.951) |
| save-held | 722 | 102,871 (1.029) | 95,054 (0.951) |
| save-starved | 418 | 96,640 (0.966) | 96,123 (0.961) |
| save | 585 | 120,990 (1.210) | 95,119 (0.951) |
| backlog | 265 | 47,870 (0.479) | 3,047 (0.030) |
| backlog-adp | 271 | 47,870 (0.479) | 3,047 (0.030) |
| backlog-adp-refill | 274 | 47,870 (0.479) | 3,047 (0.030) |
| backlog-owed | 306 | 50,434 (0.504) | 3,047 (0.030) |

Longest pass that carries a step: 123,127 CPU cycles (1.231 ms), backlog-adp@blank-7; longest step: 96,123 (0.961 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 351,440 | 3.514 | 20 | 20 | fits | 94,268 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 141,841 | 1.418 | 20 | 200 | fits | 77,607 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 437,780 | 4.378 | 20 | 200 | fits | 94,268 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 142,753 | 1.428 | 20 | 20 | fits | 77,607 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 587,459 | 5.875 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 146,338 | 1.463 | 20 | 24 | fits | 77,607 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,089,873 | 10.899 | 20 | 24 | fits | 47,341 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 145,298 | 1.453 | 20 | 50 | fits | 77,607 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 441,456 | 4.415 | 20 | 50 | fits | 94,268 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 254,622 | 2.546 | 18 | 18 | fits | 109,779 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,120,141 | 11.201 | 18 | 18 | fits | 32,803 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 284,002 | 2.840 | 20 | 20 | fits | 94,268 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 74,348 | 0.743 | 20 | 200 | fits | 77,049 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 370,342 | 3.703 | 20 | 200 | fits | 94,268 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 75,260 | 0.753 | 20 | 20 | fits | 77,049 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 520,021 | 5.200 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 78,845 | 0.788 | 20 | 24 | fits | 77,049 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 1,046,696 | 10.467 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 77,805 | 0.778 | 20 | 50 | fits | 77,049 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 374,018 | 3.740 | 20 | 50 | fits | 94,268 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 187,184 | 1.872 | 18 | 18 | fits | 109,834 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,044,161 | 10.442 | 18 | 18 | fits | 47,081 | 29 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 282,428 | 2.824 | 20 | 20 | fits | 94,268 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 72,918 | 0.729 | 20 | 200 | fits | 77,049 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 368,768 | 3.688 | 20 | 200 | fits | 94,268 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 73,830 | 0.738 | 20 | 20 | fits | 77,049 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 518,447 | 5.184 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 77,415 | 0.774 | 20 | 24 | fits | 77,049 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 1,021,405 | 10.214 | 20 | 24 | fits | 47,217 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 76,375 | 0.764 | 20 | 50 | fits | 77,049 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 372,444 | 3.724 | 20 | 50 | fits | 94,268 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 185,610 | 1.856 | 18 | 18 | fits | 109,690 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,051,673 | 10.517 | 18 | 18 | fits | 32,803 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 313,716 | 3.137 | 20 | 20 | fits | 87,021 | 58 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 109,512 | 1.095 | 20 | 200 | fits | 77,012 | 137 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 392,809 | 3.928 | 20 | 200 | fits | 87,021 | 58 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 110,424 | 1.104 | 20 | 20 | fits | 77,012 | 137 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 541,449 | 5.414 | 20 | 20 | fits | 63,609 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 36,997 | 0.370 | 20 | 24 | fits | 38,061 | 63 | 0.578 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 997,511 | 9.975 | 20 | 24 | fits | 47,217 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 35,957 | 0.360 | 20 | 50 | fits | 38,061 | 63 | 0.578 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 309,464 | 3.095 | 20 | 50 | fits | 86,970 | 74 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 222,429 | 2.224 | 18 | 18 | fits | 109,915 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,059,873 | 10.599 | 18 | 18 | fits | 32,094 | 17 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 287,950 | 2.880 | 20 | 20 | fits | 94,268 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 78,296 | 0.783 | 20 | 200 | fits | 77,049 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 374,290 | 3.743 | 20 | 200 | fits | 94,268 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 79,208 | 0.792 | 20 | 20 | fits | 77,049 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 500,770 | 5.008 | 20 | 20 | fits | 40,468 | 24 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 82,793 | 0.828 | 20 | 24 | fits | 77,049 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 1,028,047 | 10.280 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 81,753 | 0.818 | 20 | 50 | fits | 77,049 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 377,966 | 3.780 | 20 | 50 | fits | 94,268 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 191,132 | 1.911 | 18 | 18 | fits | 109,834 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,058,322 | 10.583 | 18 | 18 | fits | 32,810 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 286,376 | 2.864 | 20 | 20 | fits | 86,040 | 77 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 76,866 | 0.769 | 20 | 200 | fits | 77,049 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 364,488 | 3.645 | 20 | 200 | fits | 86,040 | 77 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 77,778 | 0.778 | 20 | 20 | fits | 77,049 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 518,702 | 5.187 | 20 | 20 | fits | 63,904 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 81,363 | 0.814 | 20 | 24 | fits | 77,049 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 1,041,651 | 10.417 | 20 | 24 | fits | 47,265 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 80,323 | 0.803 | 20 | 50 | fits | 77,049 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 368,164 | 3.682 | 20 | 50 | fits | 86,040 | 77 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 189,558 | 1.896 | 18 | 18 | fits | 109,690 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,063,912 | 10.639 | 18 | 18 | fits | 24,796 | 16 | 0.825 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 263,915 | 2.639 | 20 | 20 | fits | 96,990 | 87 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 75,436 | 0.754 | 20 | 200 | fits | 77,049 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 349,947 | 3.499 | 20 | 200 | fits | 96,990 | 87 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 76,348 | 0.763 | 20 | 20 | fits | 77,049 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 500,127 | 5.001 | 20 | 20 | fits | 63,840 | 33 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 79,933 | 0.799 | 20 | 24 | fits | 77,049 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 1,023,009 | 10.230 | 20 | 24 | fits | 47,117 | 29 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 78,893 | 0.789 | 20 | 50 | fits | 77,049 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 353,623 | 3.536 | 20 | 50 | fits | 96,990 | 87 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 188,272 | 1.883 | 18 | 18 | fits | 109,834 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,053,478 | 10.535 | 18 | 18 | fits | 33,004 | 19 | 0.792 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 260,785 | 2.608 | 20 | 20 | fits | 95,404 | 81 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 74,006 | 0.740 | 20 | 200 | fits | 77,049 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 347,856 | 3.479 | 20 | 200 | fits | 95,404 | 81 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 74,918 | 0.749 | 20 | 20 | fits | 77,049 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 497,947 | 4.979 | 20 | 20 | fits | 63,748 | 33 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 78,503 | 0.785 | 20 | 24 | fits | 77,049 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 1,020,364 | 10.204 | 20 | 24 | fits | 47,073 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 77,463 | 0.775 | 20 | 50 | fits | 77,049 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 351,532 | 3.515 | 20 | 50 | fits | 95,404 | 81 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 256,063 | 2.561 | 18 | 18 | fits | 105,519 | 102 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,050,631 | 10.506 | 18 | 18 | fits | 32,802 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 285,693 | 2.857 | 20 | 20 | fits | 94,302 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 76,053 | 0.761 | 20 | 200 | fits | 77,211 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 372,067 | 3.721 | 20 | 200 | fits | 94,302 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 76,965 | 0.770 | 20 | 20 | fits | 77,211 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 521,746 | 5.217 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 80,550 | 0.805 | 20 | 24 | fits | 77,211 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 1,048,440 | 10.484 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 79,510 | 0.795 | 20 | 50 | fits | 77,211 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 375,743 | 3.757 | 20 | 50 | fits | 94,302 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 188,798 | 1.888 | 18 | 18 | fits | 109,743 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,045,905 | 10.459 | 18 | 18 | fits | 47,081 | 29 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 282,833 | 2.828 | 20 | 20 | fits | 94,302 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 73,193 | 0.732 | 20 | 200 | fits | 77,211 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 369,207 | 3.692 | 20 | 200 | fits | 94,302 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 74,105 | 0.741 | 20 | 20 | fits | 77,211 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 518,886 | 5.189 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 77,690 | 0.777 | 20 | 24 | fits | 77,211 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 1,045,561 | 10.456 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 76,650 | 0.766 | 20 | 50 | fits | 77,211 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 372,883 | 3.729 | 20 | 50 | fits | 94,302 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 185,938 | 1.859 | 18 | 18 | fits | 109,743 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,043,026 | 10.430 | 18 | 18 | fits | 47,081 | 29 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 288,289 | 2.883 | 20 | 20 | fits | 94,268 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 78,571 | 0.786 | 20 | 200 | fits | 77,211 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 374,629 | 3.746 | 20 | 200 | fits | 94,268 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 79,483 | 0.795 | 20 | 20 | fits | 77,211 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 503,481 | 5.035 | 20 | 20 | fits | 67,027 | 39 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 83,068 | 0.831 | 20 | 24 | fits | 77,211 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 1,027,795 | 10.278 | 20 | 24 | fits | 47,250 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 82,028 | 0.820 | 20 | 50 | fits | 77,211 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 378,305 | 3.783 | 20 | 50 | fits | 94,268 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 191,471 | 1.915 | 18 | 18 | fits | 109,898 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,058,070 | 10.581 | 18 | 18 | fits | 32,810 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 280,016 | 2.800 | 20 | 20 | fits | 94,457 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 75,711 | 0.757 | 20 | 200 | fits | 77,211 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 366,490 | 3.665 | 20 | 200 | fits | 94,457 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 76,623 | 0.766 | 20 | 20 | fits | 77,211 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 516,169 | 5.162 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 80,208 | 0.802 | 20 | 24 | fits | 77,211 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 1,038,551 | 10.386 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 79,168 | 0.792 | 20 | 50 | fits | 77,211 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 370,166 | 3.702 | 20 | 50 | fits | 94,457 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 178,998 | 1.790 | 18 | 18 | fits | 100,285 | 134 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,060,659 | 10.607 | 18 | 18 | fits | 24,643 | 16 | 0.823 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 282,107 | 2.821 | 20 | 20 | fits | 94,302 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 72,526 | 0.725 | 20 | 200 | fits | 77,487 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 368,481 | 3.685 | 20 | 200 | fits | 94,302 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 73,438 | 0.734 | 20 | 20 | fits | 77,487 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 518,160 | 5.182 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 77,023 | 0.770 | 20 | 24 | fits | 77,487 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 1,020,574 | 10.206 | 20 | 24 | fits | 47,341 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 75,983 | 0.760 | 20 | 50 | fits | 77,487 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 372,157 | 3.722 | 20 | 50 | fits | 94,302 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 185,262 | 1.853 | 18 | 18 | fits | 109,734 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,050,842 | 10.508 | 18 | 18 | fits | 32,803 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 287,716 | 2.877 | 20 | 20 | fits | 94,268 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 78,048 | 0.780 | 20 | 200 | fits | 77,211 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 374,056 | 3.741 | 20 | 200 | fits | 94,268 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 78,960 | 0.790 | 20 | 20 | fits | 77,211 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 523,735 | 5.237 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 82,545 | 0.825 | 20 | 24 | fits | 77,211 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 1,050,410 | 10.504 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 81,505 | 0.815 | 20 | 50 | fits | 77,211 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 377,732 | 3.777 | 20 | 50 | fits | 94,268 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 190,948 | 1.909 | 18 | 18 | fits | 109,898 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,047,875 | 10.479 | 18 | 18 | fits | 47,081 | 29 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 284,856 | 2.849 | 20 | 20 | fits | 94,268 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 75,188 | 0.752 | 20 | 200 | fits | 77,211 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 371,196 | 3.712 | 20 | 200 | fits | 94,268 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 76,100 | 0.761 | 20 | 20 | fits | 77,211 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 500,048 | 5.000 | 20 | 20 | fits | 67,027 | 39 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 79,685 | 0.797 | 20 | 24 | fits | 77,211 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 1,024,362 | 10.244 | 20 | 24 | fits | 47,250 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 78,645 | 0.786 | 20 | 50 | fits | 77,211 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 374,872 | 3.749 | 20 | 50 | fits | 94,268 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 188,088 | 1.881 | 18 | 18 | fits | 109,898 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,054,637 | 10.546 | 18 | 18 | fits | 32,810 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 276,583 | 2.766 | 20 | 20 | fits | 94,457 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 72,328 | 0.723 | 20 | 200 | fits | 77,211 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 363,057 | 3.631 | 20 | 200 | fits | 94,457 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 73,240 | 0.732 | 20 | 20 | fits | 77,211 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 512,736 | 5.127 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 76,825 | 0.768 | 20 | 24 | fits | 77,211 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 1,035,118 | 10.351 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 75,785 | 0.758 | 20 | 50 | fits | 77,211 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 366,733 | 3.667 | 20 | 50 | fits | 94,457 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 175,615 | 1.756 | 18 | 18 | fits | 100,285 | 134 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,057,226 | 10.572 | 18 | 18 | fits | 24,643 | 16 | 0.823 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 353,245 | 3.532 | 20 | 20 | fits | 94,302 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 143,437 | 1.434 | 20 | 200 | fits | 77,839 | 135 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 439,619 | 4.396 | 20 | 200 | fits | 94,302 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 144,349 | 1.443 | 20 | 20 | fits | 77,839 | 135 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 589,298 | 5.893 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 147,934 | 1.479 | 20 | 24 | fits | 77,839 | 135 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,091,712 | 10.917 | 20 | 24 | fits | 47,341 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 146,894 | 1.469 | 20 | 50 | fits | 77,839 | 135 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 443,295 | 4.433 | 20 | 50 | fits | 94,302 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 256,350 | 2.563 | 18 | 18 | fits | 109,911 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,121,980 | 11.220 | 18 | 18 | fits | 32,803 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 285,783 | 2.858 | 20 | 20 | fits | 94,268 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 75,986 | 0.760 | 20 | 200 | fits | 77,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 372,123 | 3.721 | 20 | 200 | fits | 94,268 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 76,898 | 0.769 | 20 | 20 | fits | 77,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 521,802 | 5.218 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 80,483 | 0.805 | 20 | 24 | fits | 77,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 1,048,477 | 10.485 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 79,443 | 0.794 | 20 | 50 | fits | 77,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 375,799 | 3.758 | 20 | 50 | fits | 94,268 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 188,965 | 1.890 | 18 | 18 | fits | 109,977 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,045,942 | 10.459 | 18 | 18 | fits | 47,081 | 29 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 284,275 | 2.843 | 20 | 20 | fits | 94,302 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 74,556 | 0.746 | 20 | 200 | fits | 77,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 370,649 | 3.706 | 20 | 200 | fits | 94,302 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 75,468 | 0.755 | 20 | 20 | fits | 77,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 520,328 | 5.203 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 79,053 | 0.791 | 20 | 24 | fits | 77,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 1,023,286 | 10.233 | 20 | 24 | fits | 47,217 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 78,013 | 0.780 | 20 | 50 | fits | 77,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 374,325 | 3.743 | 20 | 50 | fits | 94,302 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 187,380 | 1.874 | 18 | 18 | fits | 109,822 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,053,554 | 10.536 | 18 | 18 | fits | 32,803 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 282,923 | 2.829 | 20 | 20 | fits | 94,268 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 73,126 | 0.731 | 20 | 200 | fits | 77,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 369,263 | 3.693 | 20 | 200 | fits | 94,268 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 74,038 | 0.740 | 20 | 20 | fits | 77,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 518,942 | 5.189 | 20 | 20 | fits | 63,667 | 33 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 77,623 | 0.776 | 20 | 24 | fits | 77,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 1,045,636 | 10.456 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 76,583 | 0.766 | 20 | 50 | fits | 77,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 372,939 | 3.729 | 20 | 50 | fits | 94,268 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 186,105 | 1.861 | 18 | 18 | fits | 109,977 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,043,101 | 10.431 | 18 | 18 | fits | 47,081 | 29 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 313,324 | 3.133 | 20 | 20 | fits | 87,021 | 58 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 109,386 | 1.094 | 20 | 200 | fits | 76,797 | 137 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 392,417 | 3.924 | 20 | 200 | fits | 87,021 | 58 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 110,298 | 1.103 | 20 | 20 | fits | 76,797 | 137 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 544,911 | 5.449 | 20 | 20 | fits | 67,463 | 39 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 37,086 | 0.371 | 20 | 24 | fits | 38,216 | 63 | 0.587 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 1,020,407 | 10.204 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 36,046 | 0.360 | 20 | 50 | fits | 38,216 | 63 | 0.587 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 309,072 | 3.091 | 20 | 50 | fits | 86,996 | 74 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 222,011 | 2.220 | 18 | 18 | fits | 109,623 | 138 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,050,682 | 10.507 | 18 | 18 | fits | 32,810 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 288,223 | 2.882 | 20 | 20 | fits | 86,074 | 77 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 78,504 | 0.785 | 20 | 200 | fits | 77,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 366,369 | 3.664 | 20 | 200 | fits | 86,074 | 77 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 79,416 | 0.794 | 20 | 20 | fits | 77,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 520,583 | 5.206 | 20 | 20 | fits | 63,904 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 83,001 | 0.830 | 20 | 24 | fits | 77,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 1,043,392 | 10.434 | 20 | 24 | fits | 47,125 | 29 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 81,961 | 0.820 | 20 | 50 | fits | 77,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 370,045 | 3.700 | 20 | 50 | fits | 86,074 | 77 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 191,328 | 1.913 | 18 | 18 | fits | 109,822 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,065,669 | 10.657 | 18 | 18 | fits | 24,812 | 16 | 0.825 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 265,696 | 2.657 | 20 | 20 | fits | 97,030 | 87 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 77,074 | 0.771 | 20 | 200 | fits | 77,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 351,768 | 3.518 | 20 | 200 | fits | 97,030 | 87 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 77,986 | 0.780 | 20 | 20 | fits | 77,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 501,948 | 5.019 | 20 | 20 | fits | 63,840 | 33 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 81,571 | 0.816 | 20 | 24 | fits | 77,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 1,024,706 | 10.247 | 20 | 24 | fits | 47,125 | 29 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 80,531 | 0.805 | 20 | 50 | fits | 77,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 355,444 | 3.554 | 20 | 50 | fits | 97,030 | 87 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 190,053 | 1.901 | 18 | 18 | fits | 109,977 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,055,183 | 10.552 | 18 | 18 | fits | 33,012 | 19 | 0.792 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 262,628 | 2.626 | 20 | 20 | fits | 95,404 | 81 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 75,644 | 0.756 | 20 | 200 | fits | 77,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 349,699 | 3.497 | 20 | 200 | fits | 95,404 | 81 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 76,556 | 0.766 | 20 | 20 | fits | 77,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 499,790 | 4.998 | 20 | 20 | fits | 63,748 | 33 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 80,141 | 0.801 | 20 | 24 | fits | 77,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 1,022,115 | 10.221 | 20 | 24 | fits | 47,081 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 79,101 | 0.791 | 20 | 50 | fits | 77,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 353,375 | 3.534 | 20 | 50 | fits | 95,404 | 81 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 257,906 | 2.579 | 18 | 18 | fits | 105,667 | 102 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,052,390 | 10.524 | 18 | 18 | fits | 32,810 | 19 | 0.790 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 273,387 | 2.734 | 20 | 200 | fits | 71,891 | 84 | 0.568 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 432,225 | 4.322 | 20 | 20 | fits | 57,268 | 32 | 0.699 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 540,737 | 5.407 | 20 | 24 | fits | 21,734 | 21 | 0.597 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 301,433 | 3.014 | 20 | 50 | fits | 64,073 | 55 | 0.655 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 801,192 | 8.012 | 18 | 18 | fits | 46,759 | 29 | 0.728 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 281,811 | 2.818 | 20 | 200 | fits | 74,890 | 90 | 0.593 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 447,264 | 4.473 | 20 | 20 | fits | 58,653 | 38 | 0.692 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 608,597 | 6.086 | 20 | 24 | fits | 24,506 | 27 | 0.638 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 289,269 | 2.893 | 20 | 50 | fits | 67,070 | 61 | 0.675 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 868,630 | 8.686 | 18 | 18 | fits | 41,329 | 32 | 0.744 |
| an event behind 15 others | `backlog.event.if0` | 91,535 | 0.915 | 20 | 200 | fits | 66,895 | 104 | 0.515 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 353,699 | 3.537 | 20 | 20 | fits | 49,095 | 44 | 0.525 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 81,368 | 0.814 | 20 | 200 | fits | 81,576 | 138 | 0.512 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 286,669 | 2.867 | 20 | 200 | fits | 57,103 | 55 | 0.542 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 77,109 | 0.771 | 20 | 20 | fits | 81,576 | 138 | 0.512 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 381,023 | 3.810 | 20 | 20 | fits | 49,095 | 44 | 0.525 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 80,694 | 0.807 | 20 | 24 | fits | 81,576 | 138 | 0.512 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 617,980 | 6.180 | 20 | 24 | fits | 23,279 | 29 | 0.500 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 79,654 | 0.797 | 20 | 50 | fits | 81,576 | 138 | 0.512 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 285,174 | 2.852 | 20 | 50 | fits | 57,103 | 55 | 0.542 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 285,109 | 2.851 | 18 | 18 | fits | 57,103 | 55 | 0.542 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 644,499 | 6.445 | 18 | 18 | fits | 9,347 | 17 | 0.291 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 280,404 | 2.804 | 20 | 20 | fits | 94,059 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 70,573 | 0.706 | 20 | 200 | fits | 75,255 | 135 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 366,614 | 3.666 | 20 | 200 | fits | 94,059 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 71,485 | 0.715 | 20 | 20 | fits | 75,255 | 135 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 516,470 | 5.165 | 20 | 20 | fits | 63,754 | 33 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 75,070 | 0.751 | 20 | 24 | fits | 75,255 | 135 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,036,648 | 10.366 | 20 | 24 | fits | 47,245 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 74,030 | 0.740 | 20 | 50 | fits | 75,255 | 135 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 370,290 | 3.703 | 20 | 50 | fits | 94,059 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 183,832 | 1.838 | 18 | 18 | fits | 110,257 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,058,751 | 10.588 | 18 | 18 | fits | 24,638 | 16 | 0.823 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,603 | 0.116 | 20 | 20 | fits | 21,306 | 20 | 0.757 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 70,573 | 0.706 | 20 | 200 | fits | 75,255 | 135 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 26,770 | 0.268 | 20 | 200 | fits | 21,306 | 20 | 0.757 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 71,485 | 0.715 | 20 | 20 | fits | 75,255 | 135 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 508,798 | 5.088 | 20 | 20 | fits | 74,910 | 44 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 75,070 | 0.751 | 20 | 24 | fits | 75,255 | 135 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 975,378 | 9.754 | 20 | 24 | fits | 46,657 | 29 | 0.726 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 74,030 | 0.740 | 20 | 50 | fits | 75,255 | 135 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 360,752 | 3.608 | 20 | 50 | fits | 84,521 | 71 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 183,832 | 1.838 | 18 | 18 | fits | 110,257 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,030,085 | 10.301 | 18 | 18 | fits | 24,717 | 18 | 0.753 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,210,195 | 62.102 | 20 | 20 | MISS ceiling | 28,519 | 25 | 0.619 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,024,644 | 360.246 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,024,569 | 360.246 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,024,494 | 360.245 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,024,419 | 360.244 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 77,413 | 0.774 | 20 | 200 | fits | 71,787 | 129 | 0.490 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 356,883 | 3.569 | 20 | 200 | fits | 82,956 | 67 | 0.665 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 73,154 | 0.732 | 20 | 20 | fits | 71,787 | 129 | 0.490 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 467,836 | 4.678 | 20 | 20 | fits | 62,436 | 39 | 0.770 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 76,739 | 0.767 | 20 | 24 | fits | 71,787 | 129 | 0.490 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,294,779 | 62.948 | 20 | 24 | MISS ceiling | 21,739 | 21 | 0.597 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 75,699 | 0.757 | 20 | 50 | fits | 71,787 | 129 | 0.490 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 355,388 | 3.554 | 20 | 50 | fits | 82,956 | 67 | 0.665 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 182,689 | 1.827 | 18 | 18 | fits | 107,445 | 131 | 0.640 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 851,166 | 8.512 | 18 | 18 | fits | 24,328 | 17 | 0.818 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
