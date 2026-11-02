### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 16 paths and 9 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.059 (7.528) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.938 (7.828) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.150 (0.642) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.839 (2.929) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.446 (63.893) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.512 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.576 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 10.449 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.619 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 7.776 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.612 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 64.813 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.601 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 7.812 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.629 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 21.627 | MISS ceiling | 31 srp | 4 | 3 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 12.479 | 20 | 169,629 (1.696) | yes | - |
| backlog-adp | 0 | 22.226 | 19 | 234,580 (2.346) | yes | - |
| backlog-adp-refill | 0 | 41.019 | 23 | 234,580 (2.346) | yes | - |
| backlog-owed | 0 | 360.562 | 63 | 223,345 (2.233) | yes | - |

Composed maximum over the 4 backlog windows: 234,580 CPU cycles (2.346 ms), backlog-adp.
Over the windows that released their whole load only: 234,580 (2.346 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 294 | 0 | 169,629 (1.696) | fits |
| backlog-adp | 312 | 1 | 234,580 (2.346) | OVER the share |
| backlog-adp-refill | 316 | 1 | 234,580 (2.346) | OVER the share |
| backlog-owed | 348 | 1 | 223,345 (2.233) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 183,896 | 1.839 | 20 | 200 | fits | 130,783 | 104 | 0.816 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 705,879 | 7.059 | 20 | 20 | fits | 92,404 | 35 | 0.821 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 161,862 | 1.619 | 20 | 200 | fits | 162,070 | 138 | 0.820 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 564,428 | 5.644 | 20 | 200 | fits | 102,763 | 55 | 0.822 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 157,603 | 1.576 | 20 | 20 | fits | 162,070 | 138 | 0.820 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 747,497 | 7.475 | 20 | 20 | fits | 92,404 | 35 | 0.821 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 161,188 | 1.612 | 20 | 24 | fits | 162,070 | 138 | 0.820 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 1,122,639 | 11.226 | 20 | 24 | fits | 36,298 | 29 | 0.808 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 160,148 | 1.601 | 20 | 50 | fits | 162,070 | 138 | 0.820 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 562,933 | 5.629 | 20 | 50 | fits | 102,763 | 55 | 0.822 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 562,868 | 5.629 | 18 | 18 | fits | 102,763 | 55 | 0.822 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 1,195,288 | 11.953 | 18 | 18 | fits | 18,627 | 17 | 0.805 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 593,827 | 5.938 | 20 | 20 | fits | 192,463 | 81 | 0.831 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 152,537 | 1.525 | 20 | 200 | fits | 157,219 | 135 | 0.823 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 777,551 | 7.776 | 20 | 200 | fits | 192,463 | 81 | 0.831 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 153,449 | 1.534 | 20 | 20 | fits | 157,219 | 135 | 0.823 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 1,044,913 | 10.449 | 20 | 20 | fits | 109,160 | 45 | 0.821 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 157,034 | 1.570 | 20 | 24 | fits | 157,219 | 135 | 0.823 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,968,434 | 19.684 | 20 | 24 | fits | 92,306 | 29 | 0.831 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 155,994 | 1.560 | 20 | 50 | fits | 157,219 | 135 | 0.823 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 781,227 | 7.812 | 20 | 50 | fits | 192,463 | 81 | 0.831 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 390,119 | 3.901 | 18 | 18 | fits | 234,580 | 154 | 0.827 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 2,162,748 | 21.627 | 18 | 18 | MISS ceiling | 47,351 | 14 | 0.826 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,029 | 0.150 | 20 | 20 | fits | 37,496 | 20 | 0.798 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 152,537 | 1.525 | 20 | 200 | fits | 157,219 | 135 | 0.823 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 45,487 | 0.455 | 20 | 200 | fits | 37,496 | 20 | 0.798 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 153,449 | 1.534 | 20 | 20 | fits | 157,219 | 135 | 0.823 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 1,025,958 | 10.260 | 20 | 20 | fits | 109,034 | 45 | 0.821 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 157,034 | 1.570 | 20 | 24 | fits | 157,219 | 135 | 0.823 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 1,976,008 | 19.760 | 20 | 24 | fits | 92,306 | 29 | 0.831 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 155,994 | 1.560 | 20 | 50 | fits | 157,219 | 135 | 0.823 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 762,524 | 7.625 | 20 | 50 | fits | 173,760 | 71 | 0.833 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 390,119 | 3.901 | 18 | 18 | fits | 234,580 | 154 | 0.827 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 2,124,672 | 21.247 | 18 | 18 | MISS ceiling | 76,112 | 21 | 0.835 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,344,595 | 63.446 | 20 | 20 | MISS ceiling | 45,946 | 25 | 0.800 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,051,177 | 360.512 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,051,102 | 360.511 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,051,027 | 360.510 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,050,952 | 360.510 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 159,553 | 1.596 | 20 | 200 | fits | 150,999 | 129 | 0.820 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 732,548 | 7.325 | 20 | 200 | fits | 167,889 | 67 | 0.831 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 155,294 | 1.553 | 20 | 20 | fits | 150,999 | 129 | 0.820 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 958,371 | 9.584 | 20 | 20 | fits | 113,996 | 33 | 0.823 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,879 | 1.589 | 20 | 24 | fits | 150,999 | 129 | 0.820 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,481,318 | 64.813 | 20 | 24 | MISS ceiling | 35,626 | 21 | 0.799 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 157,839 | 1.578 | 20 | 50 | fits | 150,999 | 129 | 0.820 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 731,053 | 7.311 | 20 | 50 | fits | 167,889 | 67 | 0.831 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 380,729 | 3.807 | 18 | 18 | fits | 223,345 | 136 | 0.827 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 1,806,365 | 18.064 | 18 | 18 | MISS ceiling | 47,315 | 17 | 0.824 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
