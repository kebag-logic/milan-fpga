### 1x1

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.643 (3.971) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.580 (3.247) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.129 (0.373) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.140 (2.078) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.007 (62.198) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.207 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.000 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 4.604 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.043 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 3.275 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.036 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.841 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.026 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 3.260 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.054 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 9.967 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.536 | 17 | 104,480 (1.045) | yes | - |
| backlog-adp | 10.267 | 18 | 103,816 (1.038) | yes | - |
| backlog-adp-refill | 40.550 | 29 | 103,816 (1.038) | yes | - |
| backlog-owed | 360.258 | 64 | 102,306 (1.023) | yes | - |

Composed maximum over the 4 backlog windows: 104,480 CPU cycles (1.045 ms), backlog.
Over the windows that released their whole load only: 104,480 (1.045 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 113,972 | 1.140 | 20 | 200 | fits | 103,310 | 117 | 0.609 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 364,346 | 3.643 | 20 | 20 | fits | 43,359 | 44 | 0.523 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 104,272 | 1.043 | 20 | 200 | fits | 104,480 | 141 | 0.620 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 309,043 | 3.090 | 20 | 200 | fits | 49,295 | 55 | 0.504 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 100,013 | 1.000 | 20 | 20 | fits | 104,480 | 141 | 0.620 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 391,771 | 3.918 | 20 | 20 | fits | 43,359 | 44 | 0.523 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 103,598 | 1.036 | 20 | 24 | fits | 104,480 | 141 | 0.620 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 618,562 | 6.186 | 20 | 24 | fits | 22,186 | 29 | 0.500 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 102,558 | 1.026 | 20 | 50 | fits | 104,480 | 141 | 0.620 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 307,548 | 3.075 | 20 | 50 | fits | 49,295 | 55 | 0.504 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 205,413 | 2.054 | 18 | 18 | fits | 103,310 | 117 | 0.609 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 626,496 | 6.265 | 18 | 18 | fits | 10,469 | 19 | 0.514 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 257,996 | 2.580 | 20 | 20 | fits | 68,343 | 82 | 0.622 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 63,538 | 0.635 | 20 | 200 | fits | 68,220 | 135 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 319,381 | 3.194 | 20 | 200 | fits | 68,343 | 82 | 0.622 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 64,450 | 0.644 | 20 | 20 | fits | 68,220 | 135 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 460,420 | 4.604 | 20 | 20 | fits | 68,477 | 44 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 68,035 | 0.680 | 20 | 24 | fits | 68,220 | 135 | 0.496 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 935,925 | 9.359 | 20 | 24 | fits | 46,429 | 29 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 66,995 | 0.670 | 20 | 50 | fits | 68,220 | 135 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 323,057 | 3.231 | 20 | 50 | fits | 68,343 | 82 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 170,356 | 1.704 | 18 | 18 | fits | 103,816 | 138 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 996,664 | 9.967 | 18 | 18 | fits | 30,881 | 17 | 0.812 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,875 | 0.129 | 20 | 20 | fits | 21,314 | 20 | 0.781 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 63,538 | 0.635 | 20 | 200 | fits | 68,220 | 135 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 28,714 | 0.287 | 20 | 200 | fits | 21,314 | 20 | 0.781 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 64,450 | 0.644 | 20 | 20 | fits | 68,220 | 135 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 451,003 | 4.510 | 20 | 20 | fits | 68,638 | 44 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 68,035 | 0.680 | 20 | 24 | fits | 68,220 | 135 | 0.496 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 926,681 | 9.267 | 20 | 24 | fits | 46,429 | 29 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 66,995 | 0.670 | 20 | 50 | fits | 68,220 | 135 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 313,719 | 3.137 | 20 | 50 | fits | 59,005 | 72 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 170,356 | 1.704 | 18 | 18 | fits | 103,816 | 138 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 987,420 | 9.874 | 18 | 18 | fits | 30,881 | 17 | 0.812 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,200,690 | 62.007 | 20 | 20 | MISS ceiling | 27,191 | 25 | 0.592 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,020,712 | 360.207 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,020,637 | 360.206 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,020,562 | 360.206 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,020,487 | 360.205 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 66,912 | 0.669 | 20 | 200 | fits | 65,168 | 129 | 0.496 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 327,509 | 3.275 | 20 | 200 | fits | 76,739 | 67 | 0.685 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 62,653 | 0.627 | 20 | 20 | fits | 65,168 | 129 | 0.496 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 440,775 | 4.408 | 20 | 20 | fits | 56,997 | 33 | 0.782 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 66,238 | 0.662 | 20 | 24 | fits | 65,168 | 129 | 0.496 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,284,061 | 62.841 | 20 | 24 | MISS ceiling | 21,322 | 21 | 0.622 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 65,198 | 0.652 | 20 | 50 | fits | 65,168 | 129 | 0.496 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 326,014 | 3.260 | 20 | 50 | fits | 76,739 | 67 | 0.685 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 167,049 | 1.670 | 18 | 18 | fits | 102,306 | 131 | 0.656 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 794,235 | 7.942 | 18 | 18 | fits | 31,460 | 20 | 0.812 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
