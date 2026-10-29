### 1x1

Clock: CPU 100 MHz, a labelled option: not the product's split CPU clock, 50 MHz, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.043 (4.372) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.873 (3.824) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.100 (0.337) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.232 (2.234) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.059 (62.235) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.209 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.094 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 5.296 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.137 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.771 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.130 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.904 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.120 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.808 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.210 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 10.401 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.968 | 17 | 113,895 (1.139) | yes | - |
| backlog-adp | 10.686 | 17 | 112,649 (1.126) | yes | - |
| backlog-adp-refill | 40.650 | 24 | 112,649 (1.126) | yes | - |
| backlog-owed | 360.260 | 65 | 110,059 (1.101) | yes | - |

Composed maximum over the 4 backlog windows: 113,895 CPU cycles (1.139 ms), backlog.
Over the windows that released their whole load only: 113,895 (1.139 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 291 | 0 | 113,895 (1.139) | fits |
| backlog-adp | 300 | 0 | 112,649 (1.126) | fits |
| backlog-adp-refill | 307 | 0 | 112,649 (1.126) | fits |
| backlog-owed | 350 | 0 | 110,059 (1.101) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 123,155 | 1.232 | 20 | 200 | fits | 109,504 | 117 | 0.589 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 404,312 | 4.043 | 20 | 20 | fits | 49,384 | 44 | 0.494 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 113,687 | 1.137 | 20 | 200 | fits | 113,895 | 141 | 0.614 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 336,925 | 3.369 | 20 | 200 | fits | 55,576 | 55 | 0.490 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 109,428 | 1.094 | 20 | 20 | fits | 113,895 | 141 | 0.614 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 431,895 | 4.319 | 20 | 20 | fits | 49,384 | 44 | 0.494 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 113,013 | 1.130 | 20 | 24 | fits | 113,895 | 141 | 0.614 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 662,975 | 6.630 | 20 | 24 | fits | 22,651 | 29 | 0.493 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 111,973 | 1.120 | 20 | 50 | fits | 113,895 | 141 | 0.614 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 335,430 | 3.354 | 20 | 50 | fits | 55,576 | 55 | 0.490 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 221,022 | 2.210 | 18 | 18 | fits | 109,504 | 117 | 0.589 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 670,337 | 6.703 | 18 | 18 | fits | 9,897 | 19 | 0.386 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 287,251 | 2.873 | 20 | 20 | fits | 96,908 | 81 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 74,195 | 0.742 | 20 | 200 | fits | 78,877 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 377,076 | 3.771 | 20 | 200 | fits | 96,908 | 81 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 75,107 | 0.751 | 20 | 20 | fits | 78,877 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 529,563 | 5.296 | 20 | 20 | fits | 64,113 | 33 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 78,692 | 0.787 | 20 | 24 | fits | 78,877 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,042,621 | 10.426 | 20 | 24 | fits | 45,517 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 77,652 | 0.777 | 20 | 50 | fits | 78,877 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 380,752 | 3.808 | 20 | 50 | fits | 96,908 | 81 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 189,846 | 1.898 | 18 | 18 | fits | 112,649 | 138 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,040,086 | 10.401 | 18 | 18 | fits | 45,517 | 29 | 0.728 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 10,036 | 0.100 | 20 | 20 | fits | 21,508 | 20 | 0.778 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 74,195 | 0.742 | 20 | 200 | fits | 78,877 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 25,939 | 0.259 | 20 | 200 | fits | 21,508 | 20 | 0.778 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 75,107 | 0.751 | 20 | 20 | fits | 78,877 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 520,261 | 5.203 | 20 | 20 | fits | 75,876 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 78,692 | 0.787 | 20 | 24 | fits | 78,877 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 987,378 | 9.874 | 20 | 24 | fits | 45,577 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 77,652 | 0.777 | 20 | 50 | fits | 78,877 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 370,369 | 3.704 | 20 | 50 | fits | 86,525 | 71 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 189,846 | 1.898 | 18 | 18 | fits | 112,649 | 138 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,015,303 | 10.153 | 18 | 18 | fits | 30,460 | 19 | 0.784 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,205,916 | 62.059 | 20 | 20 | MISS ceiling | 28,320 | 25 | 0.604 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,020,912 | 360.209 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,020,837 | 360.208 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,020,762 | 360.208 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,020,687 | 360.207 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 77,246 | 0.772 | 20 | 200 | fits | 74,271 | 129 | 0.491 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 361,003 | 3.610 | 20 | 200 | fits | 84,099 | 67 | 0.671 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 72,987 | 0.730 | 20 | 20 | fits | 74,271 | 129 | 0.491 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 468,383 | 4.684 | 20 | 20 | fits | 50,388 | 29 | 0.788 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 76,572 | 0.766 | 20 | 24 | fits | 74,271 | 129 | 0.491 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,290,407 | 62.904 | 20 | 24 | MISS ceiling | 21,653 | 21 | 0.603 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 75,532 | 0.755 | 20 | 50 | fits | 74,271 | 129 | 0.491 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 359,508 | 3.595 | 20 | 50 | fits | 84,099 | 67 | 0.671 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 185,136 | 1.851 | 18 | 18 | fits | 110,059 | 131 | 0.647 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 836,640 | 8.366 | 18 | 18 | fits | 23,156 | 17 | 0.821 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
