### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.734 (7.451) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.192 (5.659) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.230 (0.753) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.447 (2.482) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.929 (64.457) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.413 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.309 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.985 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.351 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.606 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.851 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.344 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.948 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.334 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 5.836 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.289 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 15.959 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 13.903 | 19 | 156,048 (1.560) | yes | - |
| backlog-adp | 0 | 16.511 | 19 | 184,308 (1.843) | yes | - |
| backlog-adp-refill | 0 | 41.277 | 23 | 184,308 (1.843) | yes | - |
| backlog-owed | 0 | 360.464 | 64 | 191,528 (1.915) | yes | - |

Composed maximum over the 4 backlog windows: 191,528 CPU cycles (1.915 ms), backlog-owed.
Over the windows that released their whole load only: 191,528 (1.915 ms), backlog-owed.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 302 | 0 | 156,048 (1.560) | fits |
| backlog-adp | 311 | 0 | 184,308 (1.843) | fits |
| backlog-adp-refill | 315 | 0 | 184,308 (1.843) | fits |
| backlog-owed | 358 | 0 | 191,528 (1.915) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 144,668 | 1.447 | 20 | 200 | fits | 112,839 | 125 | 0.526 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 673,375 | 6.734 | 20 | 20 | fits | 110,842 | 52 | 0.695 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 135,117 | 1.351 | 20 | 200 | fits | 135,325 | 143 | 0.534 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 530,456 | 5.305 | 20 | 200 | fits | 127,061 | 57 | 0.678 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 130,858 | 1.309 | 20 | 20 | fits | 135,325 | 143 | 0.534 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 739,762 | 7.398 | 20 | 20 | fits | 110,842 | 52 | 0.695 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 134,443 | 1.344 | 20 | 24 | fits | 135,325 | 143 | 0.534 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,241,726 | 12.417 | 20 | 24 | fits | 49,808 | 31 | 0.691 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 133,403 | 1.334 | 20 | 50 | fits | 135,325 | 143 | 0.534 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 528,961 | 5.290 | 20 | 50 | fits | 127,061 | 57 | 0.678 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 528,896 | 5.289 | 18 | 18 | fits | 127,061 | 57 | 0.678 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,337,669 | 13.377 | 18 | 18 | fits | 32,424 | 18 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 419,167 | 4.192 | 20 | 20 | fits | 160,430 | 89 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 109,163 | 1.092 | 20 | 200 | fits | 113,845 | 140 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 560,627 | 5.606 | 20 | 200 | fits | 160,430 | 89 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 110,075 | 1.101 | 20 | 20 | fits | 113,845 | 140 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 798,478 | 7.985 | 20 | 20 | fits | 106,522 | 34 | 0.694 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 113,660 | 1.137 | 20 | 24 | fits | 113,845 | 140 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,515,621 | 15.156 | 20 | 24 | fits | 65,046 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 112,620 | 1.126 | 20 | 50 | fits | 113,845 | 140 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 564,303 | 5.643 | 20 | 50 | fits | 160,430 | 89 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 296,473 | 2.965 | 18 | 18 | fits | 184,308 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,595,868 | 15.959 | 18 | 18 | fits | 34,071 | 15 | 0.774 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 22,979 | 0.230 | 20 | 20 | fits | 42,780 | 21 | 0.765 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 109,163 | 1.092 | 20 | 200 | fits | 113,845 | 140 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 58,310 | 0.583 | 20 | 200 | fits | 42,780 | 21 | 0.765 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 110,075 | 1.101 | 20 | 20 | fits | 113,845 | 140 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 777,599 | 7.776 | 20 | 20 | fits | 117,658 | 46 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 113,660 | 1.137 | 20 | 24 | fits | 113,845 | 140 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,444,737 | 14.447 | 20 | 24 | fits | 74,850 | 37 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 112,620 | 1.126 | 20 | 50 | fits | 113,845 | 140 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 543,932 | 5.439 | 20 | 50 | fits | 140,059 | 79 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 296,473 | 2.965 | 18 | 18 | fits | 184,308 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,538,938 | 15.389 | 18 | 18 | fits | 47,844 | 18 | 0.699 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,392,919 | 63.929 | 20 | 20 | MISS ceiling | 49,128 | 27 | 0.553 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,041,311 | 360.413 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,041,236 | 360.412 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,041,161 | 360.412 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,041,086 | 360.411 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 123,483 | 1.235 | 20 | 200 | fits | 111,192 | 134 | 0.496 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 585,075 | 5.851 | 20 | 200 | fits | 130,045 | 69 | 0.654 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 119,224 | 1.192 | 20 | 20 | fits | 111,192 | 134 | 0.496 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 782,104 | 7.821 | 20 | 20 | fits | 98,878 | 35 | 0.739 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 122,809 | 1.228 | 20 | 24 | fits | 111,192 | 134 | 0.496 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,494,820 | 64.948 | 20 | 24 | MISS ceiling | 30,956 | 23 | 0.540 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 121,769 | 1.218 | 20 | 50 | fits | 111,192 | 134 | 0.496 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 583,580 | 5.836 | 20 | 50 | fits | 130,045 | 69 | 0.654 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 312,842 | 3.128 | 18 | 18 | fits | 191,528 | 138 | 0.644 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,326,356 | 13.264 | 18 | 18 | fits | 48,480 | 21 | 0.699 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
