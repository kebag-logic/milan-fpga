### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.868 (7.363) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.501 (7.193) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.125 (0.612) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.819 (2.907) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.304 (63.613) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.400 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.557 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 9.975 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.599 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 7.140 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.592 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 64.661 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.582 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 7.177 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.438 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | 17.981 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 12.088 | 19 | 160,127 (1.601) | yes | - |
| backlog-adp | 0 | 18.750 | 18 | 214,236 (2.142) | yes | - |
| backlog-adp-refill | 0 | 40.983 | 26 | 214,236 (2.142) | yes | - |
| backlog-owed | 0 | 360.450 | 63 | 200,832 (2.008) | yes | - |

Composed maximum over the 4 backlog windows: 214,236 CPU cycles (2.142 ms), backlog-adp.
Over the windows that released their whole load only: 214,236 (2.142 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 293 | 0 | 160,127 (1.601) | fits |
| backlog-adp | 309 | 1 | 214,236 (2.142) | OVER the share |
| backlog-adp-refill | 317 | 1 | 214,236 (2.142) | OVER the share |
| backlog-owed | 348 | 1 | 200,832 (2.008) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 181,853 | 1.819 | 20 | 200 | fits | 130,604 | 104 | 0.816 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 686,759 | 6.868 | 20 | 20 | fits | 95,078 | 44 | 0.822 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 159,919 | 1.599 | 20 | 200 | fits | 160,127 | 138 | 0.821 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 545,330 | 5.453 | 20 | 200 | fits | 102,696 | 55 | 0.822 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 155,660 | 1.557 | 20 | 20 | fits | 160,127 | 138 | 0.821 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 731,011 | 7.310 | 20 | 20 | fits | 95,078 | 44 | 0.822 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 159,245 | 1.592 | 20 | 24 | fits | 160,127 | 138 | 0.821 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 1,102,815 | 11.028 | 20 | 24 | fits | 36,176 | 29 | 0.807 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 158,205 | 1.582 | 20 | 50 | fits | 160,127 | 138 | 0.821 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 543,835 | 5.438 | 20 | 50 | fits | 102,696 | 55 | 0.822 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 543,770 | 5.438 | 18 | 18 | fits | 102,696 | 55 | 0.822 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 1,156,525 | 11.565 | 18 | 18 | fits | 18,532 | 17 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 550,091 | 5.501 | 20 | 20 | fits | 172,600 | 81 | 0.819 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 151,228 | 1.512 | 20 | 200 | fits | 155,910 | 135 | 0.823 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 713,982 | 7.140 | 20 | 200 | fits | 172,600 | 81 | 0.819 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 152,140 | 1.521 | 20 | 20 | fits | 155,910 | 135 | 0.823 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 997,545 | 9.975 | 20 | 20 | fits | 145,199 | 54 | 0.817 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 155,725 | 1.557 | 20 | 24 | fits | 155,910 | 135 | 0.823 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,734,439 | 17.344 | 20 | 24 | fits | 72,408 | 29 | 0.802 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 154,685 | 1.547 | 20 | 50 | fits | 155,910 | 135 | 0.823 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 717,658 | 7.177 | 20 | 50 | fits | 172,600 | 81 | 0.819 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 368,466 | 3.685 | 18 | 18 | fits | 214,236 | 154 | 0.817 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,794,634 | 17.946 | 18 | 18 | fits | 62,730 | 29 | 0.799 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,490 | 0.125 | 20 | 20 | fits | 37,230 | 20 | 0.797 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 151,228 | 1.512 | 20 | 200 | fits | 155,910 | 135 | 0.823 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 42,712 | 0.427 | 20 | 200 | fits | 37,230 | 20 | 0.797 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 152,140 | 1.521 | 20 | 20 | fits | 155,910 | 135 | 0.823 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 971,074 | 9.711 | 20 | 20 | fits | 137,542 | 44 | 0.819 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 155,725 | 1.557 | 20 | 24 | fits | 155,910 | 135 | 0.823 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 1,683,348 | 16.833 | 20 | 24 | fits | 72,408 | 29 | 0.802 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 154,685 | 1.547 | 20 | 50 | fits | 155,910 | 135 | 0.823 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 698,970 | 6.990 | 20 | 50 | fits | 153,912 | 71 | 0.821 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 368,466 | 3.685 | 18 | 18 | fits | 214,236 | 154 | 0.817 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,798,093 | 17.981 | 18 | 18 | fits | 62,081 | 27 | 0.798 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,330,441 | 63.304 | 20 | 20 | MISS ceiling | 45,677 | 25 | 0.800 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,039,974 | 360.400 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,039,899 | 360.399 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,039,824 | 360.398 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,039,749 | 360.397 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 150,045 | 1.500 | 20 | 200 | fits | 149,689 | 129 | 0.819 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 660,873 | 6.609 | 20 | 200 | fits | 148,067 | 67 | 0.817 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 145,786 | 1.458 | 20 | 20 | fits | 149,689 | 129 | 0.819 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 847,052 | 8.471 | 20 | 20 | fits | 94,174 | 33 | 0.800 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 149,371 | 1.494 | 20 | 24 | fits | 149,689 | 129 | 0.819 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,466,068 | 64.661 | 20 | 24 | MISS ceiling | 35,352 | 21 | 0.799 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 148,331 | 1.483 | 20 | 50 | fits | 149,689 | 129 | 0.819 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 659,378 | 6.594 | 20 | 50 | fits | 148,067 | 67 | 0.817 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 348,708 | 3.487 | 18 | 18 | fits | 200,832 | 136 | 0.816 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 1,474,107 | 14.741 | 18 | 18 | fits | 37,253 | 17 | 0.795 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
