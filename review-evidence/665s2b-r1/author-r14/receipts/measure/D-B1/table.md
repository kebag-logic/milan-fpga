### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 21 paths and 6 of 323 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.218 (3.544) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 3.205 (4.801) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.107 (0.342) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.849 (1.372) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.013 (62.167) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.224 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.848 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.352 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 5.543 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 2.541 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.680 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.323 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 5.293 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.314 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 3.975 | fits | 7 adp | 28 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.359 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.847 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.348 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.011 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.647 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.srp.last.if0` (backlog-adp@blank-0) | 10.319 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.382 | 17 | 100,756 (1.008) | yes | - |
| backlog-adp@blank-1 | 0 | 10.848 | 18 | 100,674 (1.007) | yes | - |
| backlog-adp@blank-2 | 0 | 10.696 | 16 | 100,674 (1.007) | yes | - |
| backlog-adp@blank-3 | 0 | 10.910 | 18 | 100,678 (1.007) | yes | - |
| backlog-adp@blank-4 | 0 | 10.834 | 18 | 100,674 (1.007) | yes | - |
| backlog-adp@blank-5 | 0 | 10.828 | 18 | 100,674 (1.007) | yes | - |
| backlog-adp@blank-6 | 0 | 10.864 | 18 | 100,674 (1.007) | yes | - |
| backlog-adp@blank-7 | 0 | 10.798 | 18 | 96,084 (0.961) | yes | - |
| backlog-adp@program-0 | 0 | 10.799 | 17 | 100,695 (1.007) | yes | - |
| backlog-adp@program-1 | 0 | 10.841 | 18 | 100,695 (1.007) | yes | - |
| backlog-adp@program-2 | 0 | 10.737 | 16 | 100,695 (1.007) | yes | - |
| backlog-adp@program-3 | 0 | 10.826 | 17 | 100,764 (1.008) | yes | - |
| backlog-adp@program-4 | 0 | 10.044 | 17 | 100,607 (1.006) | yes | - |
| backlog-adp@program-5 | 0 | 10.028 | 17 | 100,787 (1.008) | yes | - |
| backlog-adp@program-6 | 0 | 9.995 | 17 | 100,787 (1.008) | yes | - |
| backlog-adp@program-7 | 0 | 10.001 | 16 | 100,787 (1.008) | yes | - |
| backlog-adp@verify-0 | 0 | 11.368 | 17 | 100,589 (1.006) | yes | - |
| backlog-adp@verify-1 | 0 | 10.853 | 18 | 100,738 (1.007) | yes | - |
| backlog-adp@verify-2 | 0 | 10.907 | 18 | 100,729 (1.007) | yes | - |
| backlog-adp@verify-3 | 0 | 10.754 | 17 | 100,738 (1.007) | yes | - |
| backlog-adp@verify-4 | 0 | 10.732 | 17 | 100,729 (1.007) | yes | - |
| backlog-adp@verify-5 | 0 | 10.819 | 18 | 100,738 (1.007) | yes | - |
| backlog-adp@verify-6 | 0 | 10.881 | 18 | 100,729 (1.007) | yes | - |
| backlog-adp@verify-7 | 0 | 10.787 | 18 | 95,872 (0.959) | yes | - |
| backlog | 0 | 6.339 | 19 | 76,630 (0.766) | yes | - |
| backlog-adp | 0 | 9.964 | 17 | 100,934 (1.009) | yes | - |
| backlog-adp-refill | 0 | 40.621 | 24 | 100,934 (1.009) | yes | - |
| backlog-owed | 0 | 360.275 | 65 | 99,398 (0.994) | yes | - |

Composed maximum over the 4 backlog windows: 100,934 CPU cycles (1.009 ms), backlog-adp.
Over the windows that released their whole load only: 100,934 (1.009 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 330 | 0 | 100,756 (1.008) | fits |
| backlog-adp@blank-1 | 331 | 0 | 100,674 (1.007) | fits |
| backlog-adp@blank-2 | 330 | 0 | 100,674 (1.007) | fits |
| backlog-adp@blank-3 | 332 | 0 | 100,678 (1.007) | fits |
| backlog-adp@blank-4 | 331 | 0 | 100,674 (1.007) | fits |
| backlog-adp@blank-5 | 331 | 0 | 100,674 (1.007) | fits |
| backlog-adp@blank-6 | 331 | 0 | 100,674 (1.007) | fits |
| backlog-adp@blank-7 | 331 | 0 | 96,084 (0.961) | fits |
| backlog-adp@program-0 | 360 | 0 | 117,463 (1.175) | fits |
| backlog-adp@program-1 | 361 | 0 | 117,463 (1.175) | fits |
| backlog-adp@program-2 | 360 | 0 | 117,463 (1.175) | fits |
| backlog-adp@program-3 | 360 | 0 | 117,463 (1.175) | fits |
| backlog-adp@program-4 | 361 | 0 | 117,463 (1.175) | fits |
| backlog-adp@program-5 | 361 | 0 | 117,463 (1.175) | fits |
| backlog-adp@program-6 | 361 | 0 | 117,463 (1.175) | fits |
| backlog-adp@program-7 | 361 | 0 | 117,463 (1.175) | fits |
| backlog-adp@verify-0 | 387 | 0 | 117,463 (1.175) | fits |
| backlog-adp@verify-1 | 388 | 0 | 117,463 (1.175) | fits |
| backlog-adp@verify-2 | 388 | 0 | 117,463 (1.175) | fits |
| backlog-adp@verify-3 | 387 | 0 | 117,463 (1.175) | fits |
| backlog-adp@verify-4 | 387 | 0 | 117,463 (1.175) | fits |
| backlog-adp@verify-5 | 388 | 0 | 117,463 (1.175) | fits |
| backlog-adp@verify-6 | 388 | 0 | 117,463 (1.175) | fits |
| backlog-adp@verify-7 | 388 | 0 | 117,463 (1.175) | fits |
| save-held | 3421 | 0 | 76,491 (0.765) | fits |
| save-starved | 43670 | 0 | 79,352 (0.794) | fits |
| save | 602 | 0 | 117,691 (1.177) | fits |
| backlog | 293 | 0 | 76,630 (0.766) | fits |
| backlog-adp | 300 | 0 | 100,934 (1.009) | fits |
| backlog-adp-refill | 307 | 0 | 100,934 (1.009) | fits |
| backlog-owed | 350 | 0 | 99,398 (0.994) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---|---|
| save-held | 2018.110 | 4,070 | 102 | 14.141 | no | within |
| save-starved | 4048.039 | 4,070 | 102 | 31.047 | yes | within |
| save | 2018.303 | 4,070 | 102 | 10.910 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 299 | 85,483 (0.855) | 76,242 (0.762) |
| backlog-adp@blank-1 | 299 | 84,511 (0.845) | 76,142 (0.761) |
| backlog-adp@blank-2 | 299 | 85,463 (0.855) | 76,271 (0.763) |
| backlog-adp@blank-3 | 299 | 84,585 (0.846) | 76,142 (0.761) |
| backlog-adp@blank-4 | 299 | 84,525 (0.845) | 76,142 (0.761) |
| backlog-adp@blank-5 | 299 | 84,532 (0.845) | 76,081 (0.761) |
| backlog-adp@blank-6 | 299 | 84,487 (0.845) | 76,118 (0.761) |
| backlog-adp@blank-7 | 299 | 84,569 (0.846) | 76,118 (0.761) |
| backlog-adp@program-0 | 328 | 117,463 (1.175) | 81,646 (0.816) |
| backlog-adp@program-1 | 328 | 117,463 (1.175) | 81,546 (0.815) |
| backlog-adp@program-2 | 328 | 117,463 (1.175) | 81,675 (0.817) |
| backlog-adp@program-3 | 328 | 117,463 (1.175) | 81,675 (0.817) |
| backlog-adp@program-4 | 329 | 117,463 (1.175) | 80,618 (0.806) |
| backlog-adp@program-5 | 329 | 117,463 (1.175) | 80,618 (0.806) |
| backlog-adp@program-6 | 329 | 117,463 (1.175) | 80,618 (0.806) |
| backlog-adp@program-7 | 329 | 117,463 (1.175) | 80,618 (0.806) |
| backlog-adp@verify-0 | 355 | 117,463 (1.175) | 95,379 (0.954) |
| backlog-adp@verify-1 | 355 | 117,463 (1.175) | 95,379 (0.954) |
| backlog-adp@verify-2 | 355 | 117,463 (1.175) | 95,379 (0.954) |
| backlog-adp@verify-3 | 355 | 117,463 (1.175) | 95,379 (0.954) |
| backlog-adp@verify-4 | 355 | 117,463 (1.175) | 95,379 (0.954) |
| backlog-adp@verify-5 | 355 | 117,463 (1.175) | 95,379 (0.954) |
| backlog-adp@verify-6 | 355 | 117,463 (1.175) | 95,379 (0.954) |
| backlog-adp@verify-7 | 355 | 117,463 (1.175) | 95,379 (0.954) |
| save-held | 722 | 103,143 (1.031) | 95,362 (0.954) |
| save-starved | 418 | 96,864 (0.969) | 96,244 (0.962) |
| save | 585 | 117,691 (1.177) | 95,427 (0.954) |
| backlog | 265 | 44,221 (0.442) | 2,788 (0.028) |
| backlog-adp | 271 | 44,221 (0.442) | 2,788 (0.028) |
| backlog-adp-refill | 274 | 44,221 (0.442) | 2,788 (0.028) |
| backlog-owed | 306 | 45,657 (0.457) | 2,788 (0.028) |

Longest pass that carries a step: 117,691 CPU cycles (1.177 ms), save; longest step: 96,244 (0.962 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 320,516 | 3.205 | 20 | 20 | fits | 84,857 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 131,376 | 1.314 | 20 | 200 | fits | 68,812 | 135 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 397,464 | 3.975 | 20 | 200 | fits | 84,857 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 132,288 | 1.323 | 20 | 20 | fits | 68,812 | 135 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 529,347 | 5.293 | 20 | 20 | fits | 54,920 | 33 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 135,873 | 1.359 | 20 | 24 | fits | 68,812 | 135 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,034,437 | 10.344 | 20 | 24 | fits | 50,010 | 35 | 0.751 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 134,833 | 1.348 | 20 | 50 | fits | 68,812 | 135 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 401,140 | 4.011 | 20 | 50 | fits | 84,857 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 235,134 | 2.351 | 18 | 18 | fits | 100,756 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,031,902 | 10.319 | 18 | 18 | fits | 50,010 | 35 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 253,288 | 2.533 | 20 | 20 | fits | 84,857 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 64,215 | 0.642 | 20 | 200 | fits | 68,174 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 330,236 | 3.302 | 20 | 200 | fits | 84,857 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 65,127 | 0.651 | 20 | 20 | fits | 68,174 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 462,117 | 4.621 | 20 | 20 | fits | 54,920 | 33 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 68,712 | 0.687 | 20 | 24 | fits | 68,174 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 959,173 | 9.592 | 20 | 24 | fits | 45,149 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 67,672 | 0.677 | 20 | 50 | fits | 68,174 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 333,912 | 3.339 | 20 | 50 | fits | 84,857 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 167,891 | 1.679 | 18 | 18 | fits | 100,674 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 979,465 | 9.795 | 18 | 18 | fits | 22,827 | 16 | 0.819 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 252,473 | 2.525 | 20 | 20 | fits | 84,857 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 63,400 | 0.634 | 20 | 200 | fits | 68,204 | 135 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 329,421 | 3.294 | 20 | 200 | fits | 84,857 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 64,312 | 0.643 | 20 | 20 | fits | 68,204 | 135 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 461,302 | 4.613 | 20 | 20 | fits | 54,920 | 33 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 67,897 | 0.679 | 20 | 24 | fits | 68,204 | 135 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 965,801 | 9.658 | 20 | 24 | fits | 44,812 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 66,857 | 0.669 | 20 | 50 | fits | 68,204 | 135 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 333,097 | 3.331 | 20 | 50 | fits | 84,857 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 167,076 | 1.671 | 18 | 18 | fits | 100,674 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 963,266 | 9.633 | 18 | 18 | fits | 44,812 | 29 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 282,786 | 2.828 | 20 | 20 | fits | 78,727 | 58 | 0.674 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 97,614 | 0.976 | 20 | 200 | fits | 68,064 | 137 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 353,604 | 3.536 | 20 | 200 | fits | 78,727 | 58 | 0.674 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 98,526 | 0.985 | 20 | 20 | fits | 68,064 | 137 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 485,064 | 4.851 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 34,047 | 0.340 | 20 | 24 | fits | 35,199 | 63 | 0.568 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 935,685 | 9.357 | 20 | 24 | fits | 44,812 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 33,007 | 0.330 | 20 | 50 | fits | 35,199 | 63 | 0.568 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 278,553 | 2.786 | 20 | 50 | fits | 77,194 | 74 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 201,294 | 2.013 | 18 | 18 | fits | 100,678 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 985,638 | 9.856 | 18 | 18 | fits | 21,637 | 14 | 0.814 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 259,030 | 2.590 | 20 | 20 | fits | 84,857 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 69,957 | 0.700 | 20 | 200 | fits | 68,174 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 335,978 | 3.360 | 20 | 200 | fits | 84,857 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 70,869 | 0.709 | 20 | 20 | fits | 68,174 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 467,859 | 4.679 | 20 | 20 | fits | 54,920 | 33 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 74,454 | 0.745 | 20 | 24 | fits | 68,174 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 949,722 | 9.497 | 20 | 24 | fits | 44,942 | 29 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 73,414 | 0.734 | 20 | 50 | fits | 68,174 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 339,654 | 3.397 | 20 | 50 | fits | 84,857 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 173,633 | 1.736 | 18 | 18 | fits | 100,674 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 978,168 | 9.782 | 18 | 18 | fits | 30,981 | 19 | 0.792 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 258,215 | 2.582 | 20 | 20 | fits | 84,857 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 69,142 | 0.691 | 20 | 200 | fits | 68,204 | 135 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 335,163 | 3.352 | 20 | 200 | fits | 84,857 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 70,054 | 0.701 | 20 | 20 | fits | 68,204 | 135 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 448,428 | 4.484 | 20 | 20 | fits | 58,621 | 39 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 73,639 | 0.736 | 20 | 24 | fits | 68,204 | 135 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 948,731 | 9.487 | 20 | 24 | fits | 45,024 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 72,599 | 0.726 | 20 | 50 | fits | 68,204 | 135 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 338,839 | 3.388 | 20 | 50 | fits | 84,857 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 172,818 | 1.728 | 18 | 18 | fits | 100,674 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 977,522 | 9.775 | 18 | 18 | fits | 31,326 | 19 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 253,018 | 2.530 | 20 | 20 | fits | 89,356 | 87 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 68,267 | 0.683 | 20 | 200 | fits | 68,174 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 330,679 | 3.307 | 20 | 200 | fits | 89,356 | 87 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 69,179 | 0.692 | 20 | 20 | fits | 68,174 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 462,651 | 4.627 | 20 | 20 | fits | 54,882 | 33 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 72,764 | 0.728 | 20 | 24 | fits | 68,174 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 960,753 | 9.608 | 20 | 24 | fits | 44,817 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 71,724 | 0.717 | 20 | 50 | fits | 68,174 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 334,355 | 3.344 | 20 | 50 | fits | 89,356 | 87 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 171,943 | 1.719 | 18 | 18 | fits | 100,674 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 981,086 | 9.811 | 18 | 18 | fits | 22,868 | 16 | 0.821 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 236,343 | 2.363 | 20 | 20 | fits | 85,222 | 81 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 67,452 | 0.675 | 20 | 200 | fits | 68,204 | 135 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 313,485 | 3.135 | 20 | 200 | fits | 85,222 | 81 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 68,364 | 0.684 | 20 | 20 | fits | 68,204 | 135 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 445,462 | 4.455 | 20 | 20 | fits | 54,920 | 33 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 71,949 | 0.719 | 20 | 24 | fits | 68,204 | 135 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 945,856 | 9.459 | 20 | 24 | fits | 45,034 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 70,909 | 0.709 | 20 | 50 | fits | 68,204 | 135 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 317,161 | 3.172 | 20 | 50 | fits | 85,222 | 81 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 231,874 | 2.319 | 18 | 18 | fits | 96,084 | 102 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 974,426 | 9.744 | 18 | 18 | fits | 31,105 | 19 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 256,420 | 2.564 | 20 | 20 | fits | 84,799 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 67,395 | 0.674 | 20 | 200 | fits | 69,172 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 333,343 | 3.333 | 20 | 200 | fits | 84,799 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 68,307 | 0.683 | 20 | 20 | fits | 69,172 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 465,311 | 4.653 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 71,892 | 0.719 | 20 | 24 | fits | 69,172 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 970,318 | 9.703 | 20 | 24 | fits | 50,010 | 35 | 0.751 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 70,852 | 0.709 | 20 | 50 | fits | 69,172 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 337,019 | 3.370 | 20 | 50 | fits | 84,799 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 171,092 | 1.711 | 18 | 18 | fits | 100,695 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 967,783 | 9.678 | 18 | 18 | fits | 50,010 | 35 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 254,730 | 2.547 | 20 | 20 | fits | 84,799 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 65,705 | 0.657 | 20 | 200 | fits | 69,172 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 331,653 | 3.317 | 20 | 200 | fits | 84,799 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 66,617 | 0.666 | 20 | 20 | fits | 69,172 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 463,621 | 4.636 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 70,202 | 0.702 | 20 | 24 | fits | 69,172 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 944,816 | 9.448 | 20 | 24 | fits | 44,729 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 69,162 | 0.692 | 20 | 50 | fits | 69,172 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 335,329 | 3.353 | 20 | 50 | fits | 84,799 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 169,402 | 1.694 | 18 | 18 | fits | 100,695 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 973,051 | 9.731 | 18 | 18 | fits | 30,770 | 19 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 253,040 | 2.530 | 20 | 20 | fits | 84,799 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 64,015 | 0.640 | 20 | 200 | fits | 69,172 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 329,963 | 3.300 | 20 | 200 | fits | 84,799 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 64,927 | 0.649 | 20 | 20 | fits | 69,172 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 466,256 | 4.663 | 20 | 20 | fits | 59,330 | 39 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 68,512 | 0.685 | 20 | 24 | fits | 69,172 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 964,164 | 9.642 | 20 | 24 | fits | 44,833 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 67,472 | 0.675 | 20 | 50 | fits | 69,172 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 333,639 | 3.336 | 20 | 50 | fits | 84,799 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 167,712 | 1.677 | 18 | 18 | fits | 100,695 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 961,629 | 9.616 | 18 | 18 | fits | 44,833 | 29 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 263,960 | 2.640 | 20 | 20 | fits | 84,910 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 70,572 | 0.706 | 20 | 200 | fits | 69,142 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 340,915 | 3.409 | 20 | 200 | fits | 84,910 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 71,484 | 0.715 | 20 | 20 | fits | 69,142 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 472,953 | 4.730 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 75,069 | 0.751 | 20 | 24 | fits | 69,142 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 972,994 | 9.730 | 20 | 24 | fits | 45,044 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 74,029 | 0.740 | 20 | 50 | fits | 69,142 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 344,591 | 3.446 | 20 | 50 | fits | 84,910 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 174,338 | 1.743 | 18 | 18 | fits | 100,764 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 970,459 | 9.705 | 18 | 18 | fits | 45,044 | 29 | 0.733 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 257,353 | 2.574 | 20 | 20 | fits | 84,799 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 68,672 | 0.687 | 20 | 200 | fits | 69,717 | 135 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 334,276 | 3.343 | 20 | 200 | fits | 84,799 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 69,584 | 0.696 | 20 | 20 | fits | 69,717 | 135 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 466,242 | 4.662 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 73,169 | 0.732 | 20 | 24 | fits | 69,717 | 135 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 971,249 | 9.712 | 20 | 24 | fits | 50,010 | 35 | 0.751 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 72,129 | 0.721 | 20 | 50 | fits | 69,717 | 135 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 337,952 | 3.380 | 20 | 50 | fits | 84,799 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 172,281 | 1.723 | 18 | 18 | fits | 100,607 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 968,714 | 9.687 | 18 | 18 | fits | 50,010 | 35 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 256,960 | 2.570 | 20 | 20 | fits | 84,799 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 67,843 | 0.678 | 20 | 200 | fits | 69,236 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 333,883 | 3.339 | 20 | 200 | fits | 84,799 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 68,755 | 0.688 | 20 | 20 | fits | 69,236 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 465,851 | 4.659 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 72,340 | 0.723 | 20 | 24 | fits | 69,236 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 969,803 | 9.698 | 20 | 24 | fits | 44,812 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 71,300 | 0.713 | 20 | 50 | fits | 69,236 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 337,559 | 3.376 | 20 | 50 | fits | 84,799 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 171,632 | 1.716 | 18 | 18 | fits | 100,787 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 967,268 | 9.673 | 18 | 18 | fits | 44,812 | 29 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 255,270 | 2.553 | 20 | 20 | fits | 84,799 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 66,153 | 0.662 | 20 | 200 | fits | 69,236 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 332,193 | 3.322 | 20 | 200 | fits | 84,799 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 67,065 | 0.671 | 20 | 20 | fits | 69,236 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 468,486 | 4.685 | 20 | 20 | fits | 59,330 | 39 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 70,650 | 0.707 | 20 | 24 | fits | 69,236 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 966,394 | 9.664 | 20 | 24 | fits | 44,833 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 69,610 | 0.696 | 20 | 50 | fits | 69,236 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 335,869 | 3.359 | 20 | 50 | fits | 84,799 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 169,942 | 1.699 | 18 | 18 | fits | 100,787 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 963,859 | 9.639 | 18 | 18 | fits | 44,833 | 29 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 257,874 | 2.579 | 20 | 20 | fits | 84,910 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 64,463 | 0.645 | 20 | 200 | fits | 69,236 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 334,829 | 3.348 | 20 | 200 | fits | 84,910 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 65,375 | 0.654 | 20 | 20 | fits | 69,236 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 466,867 | 4.669 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 68,960 | 0.690 | 20 | 24 | fits | 69,236 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 966,908 | 9.669 | 20 | 24 | fits | 45,044 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 67,920 | 0.679 | 20 | 50 | fits | 69,236 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 338,505 | 3.385 | 20 | 50 | fits | 84,910 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 168,252 | 1.683 | 18 | 18 | fits | 100,787 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 964,373 | 9.644 | 18 | 18 | fits | 45,044 | 29 | 0.733 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 318,502 | 3.185 | 20 | 20 | fits | 84,721 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 129,631 | 1.296 | 20 | 200 | fits | 69,684 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 395,347 | 3.953 | 20 | 200 | fits | 84,721 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 130,543 | 1.305 | 20 | 20 | fits | 69,684 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 527,313 | 5.273 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 134,128 | 1.341 | 20 | 24 | fits | 69,684 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,032,320 | 10.323 | 20 | 24 | fits | 50,010 | 35 | 0.751 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 133,088 | 1.331 | 20 | 50 | fits | 69,684 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 399,023 | 3.990 | 20 | 50 | fits | 84,721 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 233,222 | 2.332 | 18 | 18 | fits | 100,589 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,029,785 | 10.298 | 18 | 18 | fits | 50,010 | 35 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 260,031 | 2.600 | 20 | 20 | fits | 84,799 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 70,963 | 0.710 | 20 | 200 | fits | 69,323 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 336,954 | 3.370 | 20 | 200 | fits | 84,799 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 71,875 | 0.719 | 20 | 20 | fits | 69,323 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 468,922 | 4.689 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 75,460 | 0.755 | 20 | 24 | fits | 69,323 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 951,214 | 9.512 | 20 | 24 | fits | 45,244 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 74,420 | 0.744 | 20 | 50 | fits | 69,323 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 340,630 | 3.406 | 20 | 50 | fits | 84,799 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 174,703 | 1.747 | 18 | 18 | fits | 100,738 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 979,449 | 9.794 | 18 | 18 | fits | 30,770 | 19 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 259,323 | 2.593 | 20 | 20 | fits | 84,683 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 70,148 | 0.701 | 20 | 200 | fits | 69,353 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 336,130 | 3.361 | 20 | 200 | fits | 84,683 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 71,060 | 0.711 | 20 | 20 | fits | 69,353 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 468,098 | 4.681 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 74,645 | 0.746 | 20 | 24 | fits | 69,353 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 964,375 | 9.644 | 20 | 24 | fits | 44,812 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 73,605 | 0.736 | 20 | 50 | fits | 69,353 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 339,806 | 3.398 | 20 | 50 | fits | 84,683 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 173,879 | 1.739 | 18 | 18 | fits | 100,729 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 984,667 | 9.847 | 18 | 18 | fits | 22,827 | 16 | 0.819 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 258,341 | 2.583 | 20 | 20 | fits | 84,799 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 69,273 | 0.693 | 20 | 200 | fits | 69,323 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 335,264 | 3.353 | 20 | 200 | fits | 84,799 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 70,185 | 0.702 | 20 | 20 | fits | 69,323 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 467,232 | 4.672 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 73,770 | 0.738 | 20 | 24 | fits | 69,323 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 970,952 | 9.710 | 20 | 24 | fits | 44,812 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 72,730 | 0.727 | 20 | 50 | fits | 69,323 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 338,940 | 3.389 | 20 | 50 | fits | 84,799 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 173,013 | 1.730 | 18 | 18 | fits | 100,738 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 968,417 | 9.684 | 18 | 18 | fits | 44,812 | 29 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 257,633 | 2.576 | 20 | 20 | fits | 84,683 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 68,458 | 0.685 | 20 | 200 | fits | 69,353 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 334,440 | 3.344 | 20 | 200 | fits | 84,683 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 69,370 | 0.694 | 20 | 20 | fits | 69,353 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 466,408 | 4.664 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 72,955 | 0.730 | 20 | 24 | fits | 69,353 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 968,765 | 9.688 | 20 | 24 | fits | 44,814 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 71,915 | 0.719 | 20 | 50 | fits | 69,353 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 338,116 | 3.381 | 20 | 50 | fits | 84,683 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 172,189 | 1.722 | 18 | 18 | fits | 100,729 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 966,230 | 9.662 | 18 | 18 | fits | 44,814 | 29 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 256,651 | 2.567 | 20 | 20 | fits | 84,799 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 67,583 | 0.676 | 20 | 200 | fits | 69,323 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 333,574 | 3.336 | 20 | 200 | fits | 84,799 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 68,495 | 0.685 | 20 | 20 | fits | 69,323 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 446,924 | 4.469 | 20 | 20 | fits | 58,706 | 39 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 72,080 | 0.721 | 20 | 24 | fits | 69,323 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 947,144 | 9.471 | 20 | 24 | fits | 45,024 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 71,040 | 0.710 | 20 | 50 | fits | 69,323 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 337,250 | 3.373 | 20 | 50 | fits | 84,799 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 171,323 | 1.713 | 18 | 18 | fits | 100,738 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 975,935 | 9.759 | 18 | 18 | fits | 31,326 | 19 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 251,670 | 2.517 | 20 | 20 | fits | 89,259 | 87 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 66,768 | 0.668 | 20 | 200 | fits | 69,353 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 329,218 | 3.292 | 20 | 200 | fits | 89,259 | 87 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 67,680 | 0.677 | 20 | 20 | fits | 69,353 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 461,339 | 4.613 | 20 | 20 | fits | 55,027 | 33 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 71,265 | 0.713 | 20 | 24 | fits | 69,353 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 961,380 | 9.614 | 20 | 24 | fits | 45,044 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 70,225 | 0.702 | 20 | 50 | fits | 69,353 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 332,894 | 3.329 | 20 | 50 | fits | 89,259 | 87 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 170,499 | 1.705 | 18 | 18 | fits | 100,729 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 981,932 | 9.819 | 18 | 18 | fits | 23,087 | 16 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 234,898 | 2.349 | 20 | 20 | fits | 85,087 | 81 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 65,893 | 0.659 | 20 | 200 | fits | 69,323 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 311,817 | 3.118 | 20 | 200 | fits | 85,087 | 81 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 66,805 | 0.668 | 20 | 20 | fits | 69,323 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 443,903 | 4.439 | 20 | 20 | fits | 55,005 | 33 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 70,390 | 0.704 | 20 | 24 | fits | 69,323 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 943,962 | 9.440 | 20 | 24 | fits | 45,042 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 69,350 | 0.694 | 20 | 50 | fits | 69,323 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 315,493 | 3.155 | 20 | 50 | fits | 85,087 | 81 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 230,341 | 2.303 | 18 | 18 | fits | 95,872 | 102 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 972,540 | 9.725 | 18 | 18 | fits | 31,113 | 19 | 0.794 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 225,975 | 2.260 | 20 | 200 | fits | 64,074 | 84 | 0.587 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 363,186 | 3.632 | 20 | 20 | fits | 50,218 | 32 | 0.692 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 496,292 | 4.963 | 20 | 24 | fits | 21,778 | 21 | 0.589 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 254,113 | 2.541 | 20 | 50 | fits | 48,511 | 52 | 0.659 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 708,541 | 7.085 | 18 | 18 | fits | 45,227 | 29 | 0.735 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 235,217 | 2.352 | 20 | 200 | fits | 67,655 | 90 | 0.613 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 384,787 | 3.848 | 20 | 20 | fits | 52,363 | 38 | 0.698 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 554,339 | 5.543 | 20 | 24 | fits | 24,282 | 27 | 0.634 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 239,909 | 2.399 | 20 | 50 | fits | 59,844 | 61 | 0.681 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 767,962 | 7.680 | 18 | 18 | fits | 50,359 | 41 | 0.732 |
| an event behind 15 others | `backlog.event.if0` | 84,919 | 0.849 | 20 | 200 | fits | 62,009 | 104 | 0.493 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 321,810 | 3.218 | 20 | 20 | fits | 43,249 | 44 | 0.493 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 74,968 | 0.750 | 20 | 200 | fits | 75,176 | 138 | 0.511 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 266,220 | 2.662 | 20 | 200 | fits | 53,222 | 55 | 0.547 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 70,709 | 0.707 | 20 | 20 | fits | 75,176 | 138 | 0.511 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 349,108 | 3.491 | 20 | 20 | fits | 43,249 | 44 | 0.493 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 74,294 | 0.743 | 20 | 24 | fits | 75,176 | 138 | 0.511 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 579,695 | 5.797 | 20 | 24 | fits | 22,652 | 29 | 0.466 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 73,254 | 0.733 | 20 | 50 | fits | 75,176 | 138 | 0.511 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 264,725 | 2.647 | 20 | 50 | fits | 53,222 | 55 | 0.547 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 264,660 | 2.647 | 18 | 18 | fits | 53,222 | 55 | 0.547 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 606,538 | 6.065 | 18 | 18 | fits | 9,420 | 17 | 0.291 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 251,951 | 2.520 | 20 | 20 | fits | 84,887 | 81 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 62,394 | 0.624 | 20 | 200 | fits | 67,076 | 135 | 0.483 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 328,933 | 3.289 | 20 | 200 | fits | 84,887 | 81 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 63,306 | 0.633 | 20 | 20 | fits | 67,076 | 135 | 0.483 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 460,842 | 4.608 | 20 | 20 | fits | 54,915 | 33 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 66,891 | 0.669 | 20 | 24 | fits | 67,076 | 135 | 0.483 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 966,703 | 9.667 | 20 | 24 | fits | 44,978 | 29 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 65,851 | 0.659 | 20 | 50 | fits | 67,076 | 135 | 0.483 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 332,609 | 3.326 | 20 | 50 | fits | 84,887 | 81 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 166,330 | 1.663 | 18 | 18 | fits | 100,934 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 964,168 | 9.642 | 18 | 18 | fits | 44,978 | 29 | 0.732 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 10,738 | 0.107 | 20 | 20 | fits | 20,025 | 20 | 0.740 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 62,394 | 0.624 | 20 | 200 | fits | 67,076 | 135 | 0.483 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 24,535 | 0.245 | 20 | 200 | fits | 20,025 | 20 | 0.740 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 63,306 | 0.633 | 20 | 20 | fits | 67,076 | 135 | 0.483 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 454,585 | 4.546 | 20 | 20 | fits | 66,890 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 66,891 | 0.669 | 20 | 24 | fits | 67,076 | 135 | 0.483 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 916,845 | 9.168 | 20 | 24 | fits | 45,136 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 65,851 | 0.659 | 20 | 50 | fits | 67,076 | 135 | 0.483 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 322,826 | 3.228 | 20 | 50 | fits | 75,104 | 71 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 166,330 | 1.663 | 18 | 18 | fits | 100,934 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 945,242 | 9.452 | 18 | 18 | fits | 30,932 | 19 | 0.791 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,201,294 | 62.013 | 20 | 20 | MISS ceiling | 27,407 | 25 | 0.566 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,022,447 | 360.224 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,022,372 | 360.224 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,022,297 | 360.223 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,022,222 | 360.222 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 69,334 | 0.693 | 20 | 200 | fits | 65,254 | 129 | 0.489 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 321,936 | 3.219 | 20 | 200 | fits | 74,545 | 67 | 0.665 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 65,075 | 0.651 | 20 | 20 | fits | 65,254 | 129 | 0.489 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 424,950 | 4.250 | 20 | 20 | fits | 47,986 | 29 | 0.769 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 68,660 | 0.687 | 20 | 24 | fits | 65,254 | 129 | 0.489 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,284,701 | 62.847 | 20 | 24 | MISS ceiling | 21,783 | 21 | 0.589 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 67,620 | 0.676 | 20 | 50 | fits | 65,254 | 129 | 0.489 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 320,441 | 3.204 | 20 | 50 | fits | 74,545 | 67 | 0.665 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 166,563 | 1.666 | 18 | 18 | fits | 99,398 | 131 | 0.641 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 788,388 | 7.884 | 18 | 18 | fits | 22,616 | 17 | 0.814 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
