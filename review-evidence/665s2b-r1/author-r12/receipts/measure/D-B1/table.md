### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.109 (3.434) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.452 (3.274) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.097 (0.315) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.798 (1.314) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.953 (62.147) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.189 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 0.668 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 4.520 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 0.711 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.221 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 0.704 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.765 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 0.694 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.258 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.561 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 9.683 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.139 | 19 | 75,793 (0.758) | yes | - |
| backlog-adp | 0 | 9.951 | 18 | 97,832 (0.978) | yes | - |
| backlog-adp-refill | 0 | 40.579 | 24 | 97,832 (0.978) | yes | - |
| backlog-owed | 0 | 360.240 | 64 | 97,085 (0.971) | yes | - |

Composed maximum over the 4 backlog windows: 97,832 CPU cycles (0.978 ms), backlog-adp.
Over the windows that released their whole load only: 97,832 (0.978 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 293 | 0 | 75,793 (0.758) | fits |
| backlog-adp | 301 | 0 | 97,832 (0.978) | fits |
| backlog-adp-refill | 307 | 0 | 97,832 (0.978) | fits |
| backlog-owed | 349 | 0 | 97,085 (0.971) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 79,788 | 0.798 | 20 | 200 | fits | 60,126 | 104 | 0.499 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 310,879 | 3.109 | 20 | 20 | fits | 42,163 | 44 | 0.494 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 71,079 | 0.711 | 20 | 200 | fits | 71,287 | 138 | 0.514 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 257,633 | 2.576 | 20 | 200 | fits | 51,244 | 55 | 0.547 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 66,820 | 0.668 | 20 | 20 | fits | 71,287 | 138 | 0.514 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 338,140 | 3.381 | 20 | 20 | fits | 42,163 | 44 | 0.494 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 70,405 | 0.704 | 20 | 24 | fits | 71,287 | 138 | 0.514 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 563,136 | 5.631 | 20 | 24 | fits | 22,001 | 29 | 0.467 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 69,365 | 0.694 | 20 | 50 | fits | 71,287 | 138 | 0.514 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 256,138 | 2.561 | 20 | 50 | fits | 51,244 | 55 | 0.547 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 256,073 | 2.561 | 18 | 18 | fits | 51,244 | 55 | 0.547 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 588,958 | 5.890 | 18 | 18 | fits | 9,152 | 17 | 0.314 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 245,201 | 2.452 | 20 | 20 | fits | 84,033 | 81 | 0.665 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 59,911 | 0.599 | 20 | 200 | fits | 64,593 | 135 | 0.481 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 322,084 | 3.221 | 20 | 200 | fits | 84,033 | 81 | 0.665 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 60,823 | 0.608 | 20 | 20 | fits | 64,593 | 135 | 0.481 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 451,997 | 4.520 | 20 | 20 | fits | 53,997 | 33 | 0.719 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 64,408 | 0.644 | 20 | 24 | fits | 64,593 | 135 | 0.481 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 948,263 | 9.483 | 20 | 24 | fits | 44,857 | 29 | 0.743 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 63,368 | 0.634 | 20 | 50 | fits | 64,593 | 135 | 0.481 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 325,760 | 3.258 | 20 | 50 | fits | 84,033 | 81 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 160,745 | 1.607 | 18 | 18 | fits | 97,832 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 968,330 | 9.683 | 18 | 18 | fits | 22,602 | 16 | 0.839 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 9,748 | 0.097 | 20 | 20 | fits | 19,810 | 20 | 0.762 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 59,911 | 0.599 | 20 | 200 | fits | 64,593 | 135 | 0.481 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 23,948 | 0.239 | 20 | 200 | fits | 19,810 | 20 | 0.762 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 60,823 | 0.608 | 20 | 20 | fits | 64,593 | 135 | 0.481 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 446,876 | 4.469 | 20 | 20 | fits | 66,189 | 44 | 0.691 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 64,408 | 0.644 | 20 | 24 | fits | 64,593 | 135 | 0.481 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 905,950 | 9.059 | 20 | 24 | fits | 44,847 | 29 | 0.743 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 63,368 | 0.634 | 20 | 50 | fits | 64,593 | 135 | 0.481 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 316,390 | 3.164 | 20 | 50 | fits | 74,663 | 71 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 160,745 | 1.607 | 18 | 18 | fits | 97,832 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 934,250 | 9.342 | 18 | 18 | fits | 30,835 | 19 | 0.805 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,195,274 | 61.953 | 20 | 20 | MISS ceiling | 26,363 | 25 | 0.572 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,018,910 | 360.189 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,018,835 | 360.188 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,018,760 | 360.188 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,018,685 | 360.187 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 62,812 | 0.628 | 20 | 200 | fits | 62,475 | 129 | 0.486 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 313,034 | 3.130 | 20 | 200 | fits | 74,588 | 67 | 0.679 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 58,553 | 0.586 | 20 | 20 | fits | 62,475 | 129 | 0.486 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 423,428 | 4.234 | 20 | 20 | fits | 55,851 | 33 | 0.773 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 62,138 | 0.621 | 20 | 24 | fits | 62,475 | 129 | 0.486 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,276,528 | 62.765 | 20 | 24 | MISS ceiling | 20,964 | 21 | 0.607 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 61,098 | 0.611 | 20 | 50 | fits | 62,475 | 129 | 0.486 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 311,539 | 3.115 | 20 | 50 | fits | 74,588 | 67 | 0.679 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 157,728 | 1.577 | 18 | 18 | fits | 97,085 | 131 | 0.642 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 764,086 | 7.641 | 18 | 18 | fits | 30,315 | 20 | 0.791 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
