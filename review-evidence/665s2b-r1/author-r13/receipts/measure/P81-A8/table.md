### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.804 (6.284) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.900 (5.014) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.241 (0.763) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.318 (2.269) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.495 (64.020) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.336 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.171 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.252 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.213 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 5.009 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.207 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 64.744 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.196 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 4.998 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.683 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 14.906 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 10.102 | 19 | 152,542 (1.525) | yes | - |
| backlog-adp | 0 | 15.466 | 20 | 155,706 (1.557) | yes | - |
| backlog-adp-refill | 0 | 41.082 | 28 | 155,706 (1.557) | yes | - |
| backlog-owed | 0 | 360.387 | 63 | 154,343 (1.543) | yes | - |

Composed maximum over the 4 backlog windows: 155,706 CPU cycles (1.557 ms), backlog-adp.
Over the windows that released their whole load only: 155,706 (1.557 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 293 | 0 | 152,542 (1.525) | fits |
| backlog-adp | 311 | 0 | 155,706 (1.557) | fits |
| backlog-adp-refill | 319 | 0 | 155,706 (1.557) | fits |
| backlog-owed | 348 | 0 | 154,343 (1.543) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 131,803 | 1.318 | 20 | 200 | fits | 105,386 | 104 | 0.510 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 580,395 | 5.804 | 20 | 20 | fits | 78,684 | 44 | 0.512 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 121,341 | 1.213 | 20 | 200 | fits | 121,549 | 138 | 0.516 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 469,814 | 4.698 | 20 | 200 | fits | 91,154 | 55 | 0.553 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 117,082 | 1.171 | 20 | 20 | fits | 121,549 | 138 | 0.516 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 623,132 | 6.231 | 20 | 20 | fits | 78,684 | 44 | 0.512 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 120,667 | 1.207 | 20 | 24 | fits | 121,549 | 138 | 0.516 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 914,869 | 9.149 | 20 | 24 | fits | 28,089 | 29 | 0.477 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 119,627 | 1.196 | 20 | 50 | fits | 121,549 | 138 | 0.516 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 468,319 | 4.683 | 20 | 50 | fits | 91,154 | 55 | 0.553 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 468,254 | 4.683 | 18 | 18 | fits | 91,154 | 55 | 0.553 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 961,369 | 9.614 | 18 | 18 | fits | 16,131 | 17 | 0.377 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 390,031 | 3.900 | 20 | 20 | fits | 117,218 | 72 | 0.608 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 107,055 | 1.071 | 20 | 200 | fits | 111,737 | 135 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 496,121 | 4.961 | 20 | 200 | fits | 117,218 | 72 | 0.608 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 107,967 | 1.080 | 20 | 20 | fits | 111,737 | 135 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 725,151 | 7.252 | 20 | 20 | fits | 111,827 | 44 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 111,552 | 1.116 | 20 | 24 | fits | 111,737 | 135 | 0.485 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,320,814 | 13.208 | 20 | 24 | fits | 59,060 | 29 | 0.723 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 110,512 | 1.105 | 20 | 50 | fits | 111,737 | 135 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 499,797 | 4.998 | 20 | 50 | fits | 117,218 | 72 | 0.608 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 382,514 | 3.825 | 18 | 18 | fits | 155,706 | 102 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,490,565 | 14.906 | 18 | 18 | fits | 34,668 | 14 | 0.826 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 24,088 | 0.241 | 20 | 20 | fits | 43,578 | 20 | 0.778 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 107,055 | 1.071 | 20 | 200 | fits | 111,737 | 135 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 58,139 | 0.581 | 20 | 200 | fits | 43,578 | 20 | 0.778 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 107,967 | 1.080 | 20 | 20 | fits | 111,737 | 135 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 703,595 | 7.036 | 20 | 20 | fits | 111,815 | 44 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 111,552 | 1.116 | 20 | 24 | fits | 111,737 | 135 | 0.485 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 1,310,487 | 13.105 | 20 | 24 | fits | 59,060 | 29 | 0.723 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 110,512 | 1.105 | 20 | 50 | fits | 111,737 | 135 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 478,839 | 4.788 | 20 | 50 | fits | 96,260 | 62 | 0.598 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 382,514 | 3.825 | 18 | 18 | fits | 155,706 | 102 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,445,570 | 14.456 | 18 | 18 | fits | 48,156 | 23 | 0.783 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,349,505 | 63.495 | 20 | 20 | MISS ceiling | 48,180 | 25 | 0.640 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,033,643 | 360.336 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,033,568 | 360.336 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,033,493 | 360.335 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,033,418 | 360.334 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 116,298 | 1.163 | 20 | 200 | fits | 108,663 | 129 | 0.491 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 500,868 | 5.009 | 20 | 200 | fits | 122,991 | 67 | 0.667 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 112,039 | 1.120 | 20 | 20 | fits | 108,663 | 129 | 0.491 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 683,405 | 6.834 | 20 | 20 | fits | 92,022 | 33 | 0.763 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 115,624 | 1.156 | 20 | 24 | fits | 108,663 | 129 | 0.491 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,474,408 | 64.744 | 20 | 24 | MISS ceiling | 28,357 | 21 | 0.592 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 114,584 | 1.146 | 20 | 50 | fits | 108,663 | 129 | 0.491 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 499,373 | 4.994 | 20 | 50 | fits | 122,991 | 67 | 0.667 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 376,317 | 3.763 | 18 | 18 | fits | 154,343 | 95 | 0.667 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 1,224,757 | 12.248 | 18 | 18 | fits | 49,164 | 26 | 0.787 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
