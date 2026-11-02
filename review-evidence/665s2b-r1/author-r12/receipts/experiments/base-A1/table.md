### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.871 (4.182) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.751 (3.503) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.087 (0.316) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.174 (2.125) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.939 (62.156) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.146 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.041 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 4.961 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.084 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 3.477 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.077 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.726 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.066 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.487 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.102 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 9.951 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.636 | 17 | 108,568 (1.086) | yes | - |
| backlog-adp | 10.224 | 18 | 107,623 (1.076) | yes | - |
| backlog-adp-refill | 40.474 | 29 | 107,623 (1.076) | yes | - |
| backlog-owed | 360.197 | 64 | 104,611 (1.046) | yes | - |

Composed maximum over the 4 backlog windows: 108,568 CPU cycles (1.086 ms), backlog.
Over the windows that released their whole load only: 108,568 (1.086 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 291 | 0 | 108,568 (1.086) | fits |
| backlog-adp | 311 | 0 | 107,623 (1.076) | fits |
| backlog-adp-refill | 322 | 0 | 107,623 (1.076) | fits |
| backlog-owed | 349 | 0 | 104,611 (1.046) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 117,426 | 1.174 | 20 | 200 | fits | 103,978 | 117 | 0.581 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 387,111 | 3.871 | 20 | 20 | fits | 47,544 | 44 | 0.481 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 108,360 | 1.084 | 20 | 200 | fits | 108,568 | 141 | 0.607 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 321,707 | 3.217 | 20 | 200 | fits | 53,437 | 55 | 0.472 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 104,101 | 1.041 | 20 | 20 | fits | 108,568 | 141 | 0.607 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 412,934 | 4.129 | 20 | 20 | fits | 47,544 | 44 | 0.481 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 107,686 | 1.077 | 20 | 24 | fits | 108,568 | 141 | 0.607 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 632,274 | 6.323 | 20 | 24 | fits | 21,535 | 29 | 0.474 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 106,646 | 1.066 | 20 | 50 | fits | 108,568 | 141 | 0.607 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 320,212 | 3.202 | 20 | 50 | fits | 53,437 | 55 | 0.472 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 210,169 | 2.102 | 18 | 18 | fits | 103,978 | 117 | 0.581 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 639,206 | 6.392 | 18 | 18 | fits | 9,467 | 19 | 0.351 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 275,052 | 2.751 | 20 | 20 | fits | 76,880 | 82 | 0.628 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 70,751 | 0.708 | 20 | 200 | fits | 75,433 | 135 | 0.483 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 345,056 | 3.451 | 20 | 200 | fits | 76,880 | 82 | 0.628 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 71,663 | 0.717 | 20 | 20 | fits | 75,433 | 135 | 0.483 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 496,108 | 4.961 | 20 | 20 | fits | 73,232 | 44 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 75,248 | 0.752 | 20 | 24 | fits | 75,433 | 135 | 0.483 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 940,099 | 9.401 | 20 | 24 | fits | 43,354 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 74,208 | 0.742 | 20 | 50 | fits | 75,433 | 135 | 0.483 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 348,732 | 3.487 | 20 | 50 | fits | 76,880 | 82 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 181,376 | 1.814 | 18 | 18 | fits | 107,623 | 138 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 995,070 | 9.951 | 18 | 18 | fits | 28,441 | 17 | 0.770 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,677 | 0.087 | 20 | 20 | fits | 20,860 | 20 | 0.775 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 70,751 | 0.708 | 20 | 200 | fits | 75,433 | 135 | 0.483 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 24,010 | 0.240 | 20 | 200 | fits | 20,860 | 20 | 0.775 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 71,663 | 0.717 | 20 | 20 | fits | 75,433 | 135 | 0.483 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 485,852 | 4.859 | 20 | 20 | fits | 73,205 | 44 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 75,248 | 0.752 | 20 | 24 | fits | 75,433 | 135 | 0.483 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 929,845 | 9.298 | 20 | 24 | fits | 43,354 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 74,208 | 0.742 | 20 | 50 | fits | 75,433 | 135 | 0.483 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 338,779 | 3.388 | 20 | 50 | fits | 66,927 | 72 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 181,376 | 1.814 | 18 | 18 | fits | 107,623 | 138 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 984,816 | 9.848 | 18 | 18 | fits | 28,441 | 17 | 0.770 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,193,943 | 61.939 | 20 | 20 | MISS ceiling | 26,363 | 25 | 0.578 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,014,640 | 360.146 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,014,565 | 360.146 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,014,490 | 360.145 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,014,415 | 360.144 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 77,453 | 0.775 | 20 | 200 | fits | 71,167 | 129 | 0.481 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 347,697 | 3.477 | 20 | 200 | fits | 79,905 | 67 | 0.661 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 73,194 | 0.732 | 20 | 20 | fits | 71,167 | 129 | 0.481 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 457,618 | 4.576 | 20 | 20 | fits | 55,619 | 33 | 0.763 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 76,779 | 0.768 | 20 | 24 | fits | 71,167 | 129 | 0.481 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,272,599 | 62.726 | 20 | 24 | MISS ceiling | 20,101 | 21 | 0.580 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 75,739 | 0.757 | 20 | 50 | fits | 71,167 | 129 | 0.481 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 346,202 | 3.462 | 20 | 50 | fits | 79,905 | 67 | 0.661 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 179,895 | 1.799 | 18 | 18 | fits | 104,611 | 131 | 0.638 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 788,418 | 7.884 | 18 | 18 | fits | 29,344 | 20 | 0.772 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
