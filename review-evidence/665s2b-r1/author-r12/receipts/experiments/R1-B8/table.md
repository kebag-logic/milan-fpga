### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.634 (7.343) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.539 (6.014) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.185 (0.709) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.447 (2.482) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.929 (64.457) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.414 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.309 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 8.344 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.351 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.961 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.487 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.344 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.948 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.334 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 5.998 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.289 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 15.615 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 13.903 | 19 | 156,048 (1.560) | yes | - |
| backlog-adp | 16.175 | 17 | 184,308 (1.843) | yes | - |
| backlog-adp-refill | 41.232 | 23 | 184,308 (1.843) | yes | - |
| backlog-owed | 360.464 | 66 | 185,049 (1.850) | yes | - |

Composed maximum over the 4 backlog windows: 185,049 CPU cycles (1.850 ms), backlog-owed.
Over the windows that released their whole load only: 185,049 (1.850 ms), backlog-owed.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 302 | 0 | 156,048 (1.560) | fits |
| backlog-adp | 309 | 0 | 184,308 (1.843) | fits |
| backlog-adp-refill | 315 | 0 | 184,308 (1.843) | fits |
| backlog-owed | 360 | 0 | 185,049 (1.850) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 144,668 | 1.447 | 20 | 200 | fits | 112,839 | 125 | 0.526 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 663,447 | 6.634 | 20 | 20 | fits | 100,061 | 46 | 0.665 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 135,117 | 1.351 | 20 | 200 | fits | 135,325 | 143 | 0.534 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 530,456 | 5.305 | 20 | 200 | fits | 127,061 | 57 | 0.678 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 130,858 | 1.309 | 20 | 20 | fits | 135,325 | 143 | 0.534 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 728,981 | 7.290 | 20 | 20 | fits | 100,061 | 46 | 0.665 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 134,443 | 1.344 | 20 | 24 | fits | 135,325 | 143 | 0.534 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,241,877 | 12.419 | 20 | 24 | fits | 49,781 | 31 | 0.691 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 133,403 | 1.334 | 20 | 50 | fits | 135,325 | 143 | 0.534 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 528,961 | 5.290 | 20 | 50 | fits | 127,061 | 57 | 0.678 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 528,896 | 5.289 | 18 | 18 | fits | 127,061 | 57 | 0.678 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,337,675 | 13.377 | 18 | 18 | fits | 32,424 | 18 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 453,908 | 4.539 | 20 | 20 | fits | 160,656 | 89 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 109,163 | 1.092 | 20 | 200 | fits | 113,845 | 140 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 596,110 | 5.961 | 20 | 200 | fits | 160,656 | 89 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 110,075 | 1.101 | 20 | 20 | fits | 113,845 | 140 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 834,445 | 8.344 | 20 | 20 | fits | 106,751 | 34 | 0.697 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 113,660 | 1.137 | 20 | 24 | fits | 113,845 | 140 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,564,011 | 15.640 | 20 | 24 | fits | 65,056 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 112,620 | 1.126 | 20 | 50 | fits | 113,845 | 140 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 599,786 | 5.998 | 20 | 50 | fits | 160,656 | 89 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 296,473 | 2.965 | 18 | 18 | fits | 184,308 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,561,476 | 15.615 | 18 | 18 | fits | 65,056 | 31 | 0.698 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 18,474 | 0.185 | 20 | 20 | fits | 42,860 | 21 | 0.767 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 109,163 | 1.092 | 20 | 200 | fits | 113,845 | 140 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 53,833 | 0.538 | 20 | 200 | fits | 42,860 | 21 | 0.767 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 110,075 | 1.101 | 20 | 20 | fits | 113,845 | 140 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 813,589 | 8.136 | 20 | 20 | fits | 117,989 | 46 | 0.671 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 113,660 | 1.137 | 20 | 24 | fits | 113,845 | 140 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,461,226 | 14.612 | 20 | 24 | fits | 52,840 | 27 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 112,620 | 1.126 | 20 | 50 | fits | 113,845 | 140 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 579,536 | 5.795 | 20 | 50 | fits | 140,406 | 79 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 296,473 | 2.965 | 18 | 18 | fits | 184,308 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,552,134 | 15.521 | 18 | 18 | fits | 34,169 | 15 | 0.780 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,392,915 | 63.929 | 20 | 20 | MISS ceiling | 49,128 | 27 | 0.553 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,041,368 | 360.414 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,041,293 | 360.413 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,041,218 | 360.412 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,041,143 | 360.411 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 123,483 | 1.235 | 20 | 200 | fits | 111,192 | 134 | 0.496 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 548,658 | 5.487 | 20 | 200 | fits | 131,634 | 69 | 0.669 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 119,224 | 1.192 | 20 | 20 | fits | 111,192 | 134 | 0.496 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 745,579 | 7.456 | 20 | 20 | fits | 98,803 | 35 | 0.738 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 122,809 | 1.228 | 20 | 24 | fits | 111,192 | 134 | 0.496 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,494,816 | 64.948 | 20 | 24 | MISS ceiling | 30,956 | 23 | 0.544 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 121,769 | 1.218 | 20 | 50 | fits | 111,192 | 134 | 0.496 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 547,163 | 5.472 | 20 | 50 | fits | 131,634 | 69 | 0.669 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 415,464 | 4.155 | 18 | 18 | fits | 185,049 | 97 | 0.679 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,361,220 | 13.612 | 18 | 18 | fits | 34,719 | 18 | 0.765 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
