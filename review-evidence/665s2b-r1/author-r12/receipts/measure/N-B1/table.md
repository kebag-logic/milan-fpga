### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.467 (3.780) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.737 (3.647) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.122 (0.345) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.887 (1.455) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.934 (62.117) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.182 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 0.754 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 5.058 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 0.797 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.594 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 0.790 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.735 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 0.779 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.631 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.800 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 9.996 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.407 | 19 | 80,478 (0.805) | yes | - |
| backlog-adp | 0 | 10.270 | 17 | 107,398 (1.074) | yes | - |
| backlog-adp-refill | 0 | 40.635 | 25 | 107,398 (1.074) | yes | - |
| backlog-owed | 0 | 360.233 | 64 | 104,601 (1.046) | yes | - |

Composed maximum over the 4 backlog windows: 107,398 CPU cycles (1.074 ms), backlog-adp.
Over the windows that released their whole load only: 107,398 (1.074 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 293 | 0 | 80,478 (0.805) | fits |
| backlog-adp | 300 | 0 | 107,398 (1.074) | fits |
| backlog-adp-refill | 308 | 0 | 107,398 (1.074) | fits |
| backlog-owed | 349 | 0 | 104,601 (1.046) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 88,722 | 0.887 | 20 | 200 | fits | 65,628 | 104 | 0.499 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 346,690 | 3.467 | 20 | 20 | fits | 47,575 | 44 | 0.494 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 79,662 | 0.797 | 20 | 200 | fits | 79,870 | 138 | 0.518 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 281,561 | 2.816 | 20 | 200 | fits | 56,402 | 55 | 0.550 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 75,403 | 0.754 | 20 | 20 | fits | 79,870 | 138 | 0.518 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 372,686 | 3.727 | 20 | 20 | fits | 47,575 | 44 | 0.494 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 78,988 | 0.790 | 20 | 24 | fits | 79,870 | 138 | 0.518 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 590,988 | 5.910 | 20 | 24 | fits | 21,441 | 29 | 0.487 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 77,948 | 0.779 | 20 | 50 | fits | 79,870 | 138 | 0.518 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 280,066 | 2.801 | 20 | 50 | fits | 56,402 | 55 | 0.550 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 280,001 | 2.800 | 18 | 18 | fits | 56,402 | 55 | 0.550 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 615,468 | 6.155 | 18 | 18 | fits | 8,645 | 17 | 0.340 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 273,737 | 2.737 | 20 | 20 | fits | 92,733 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 70,307 | 0.703 | 20 | 200 | fits | 74,989 | 135 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 359,374 | 3.594 | 20 | 200 | fits | 92,733 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 71,219 | 0.712 | 20 | 20 | fits | 74,989 | 135 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 505,831 | 5.058 | 20 | 20 | fits | 61,605 | 33 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 74,804 | 0.748 | 20 | 24 | fits | 74,989 | 135 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,002,122 | 10.021 | 20 | 24 | fits | 44,143 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 73,764 | 0.738 | 20 | 50 | fits | 74,989 | 135 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 363,050 | 3.631 | 20 | 50 | fits | 92,733 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 180,707 | 1.807 | 18 | 18 | fits | 107,398 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 999,587 | 9.996 | 18 | 18 | fits | 44,143 | 29 | 0.733 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,219 | 0.122 | 20 | 20 | fits | 20,633 | 20 | 0.778 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 70,307 | 0.703 | 20 | 200 | fits | 74,989 | 135 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 27,114 | 0.271 | 20 | 200 | fits | 20,633 | 20 | 0.778 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 71,219 | 0.712 | 20 | 20 | fits | 74,989 | 135 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 496,712 | 4.967 | 20 | 20 | fits | 72,979 | 44 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 74,804 | 0.748 | 20 | 24 | fits | 74,989 | 135 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 923,891 | 9.239 | 20 | 24 | fits | 43,908 | 29 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 73,764 | 0.738 | 20 | 50 | fits | 74,989 | 135 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 352,571 | 3.526 | 20 | 50 | fits | 82,254 | 71 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 180,707 | 1.807 | 18 | 18 | fits | 107,398 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 979,361 | 9.794 | 18 | 18 | fits | 28,455 | 17 | 0.778 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,193,426 | 61.934 | 20 | 20 | MISS ceiling | 26,823 | 25 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,018,212 | 360.182 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,018,137 | 360.181 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,018,062 | 360.181 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,017,987 | 360.180 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 72,892 | 0.729 | 20 | 200 | fits | 71,456 | 129 | 0.497 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 342,967 | 3.430 | 20 | 200 | fits | 80,026 | 67 | 0.667 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 68,633 | 0.686 | 20 | 20 | fits | 71,456 | 129 | 0.497 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 459,211 | 4.592 | 20 | 20 | fits | 62,227 | 39 | 0.782 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 72,218 | 0.722 | 20 | 24 | fits | 71,456 | 129 | 0.497 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,273,463 | 62.735 | 20 | 24 | MISS ceiling | 20,542 | 21 | 0.596 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 71,178 | 0.712 | 20 | 50 | fits | 71,456 | 129 | 0.497 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 341,472 | 3.415 | 20 | 50 | fits | 80,026 | 67 | 0.667 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 175,324 | 1.753 | 18 | 18 | fits | 104,601 | 131 | 0.637 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 784,520 | 7.845 | 18 | 18 | fits | 29,487 | 20 | 0.780 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
