### 1x1

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.438 (3.715) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.460 (3.270) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.068 (0.240) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.099 (1.999) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.596 (61.732) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.140 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 0.971 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 4.411 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.013 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.217 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.006 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.253 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 0.996 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.254 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 1.975 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 9.115 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 5.711 | 17 | 101,531 (1.015) | yes | - |
| backlog-adp | 9.321 | 18 | 99,823 (0.998) | yes | - |
| backlog-adp-refill | 40.358 | 29 | 99,823 (0.998) | yes | - |
| backlog-owed | 360.190 | 65 | 97,138 (0.971) | yes | - |

Composed maximum over the 4 backlog windows: 101,531 CPU cycles (1.015 ms), backlog.
Over the windows that released their whole load only: 101,531 (1.015 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 109,877 | 1.099 | 20 | 200 | fits | 98,325 | 116 | 0.534 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 343,794 | 3.438 | 20 | 20 | fits | 39,442 | 43 | 0.416 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 101,323 | 1.013 | 20 | 200 | fits | 101,531 | 140 | 0.561 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 291,742 | 2.917 | 20 | 200 | fits | 44,590 | 54 | 0.381 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 97,064 | 0.971 | 20 | 20 | fits | 101,531 | 140 | 0.561 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 366,163 | 3.662 | 20 | 20 | fits | 39,442 | 43 | 0.416 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 100,649 | 1.006 | 20 | 24 | fits | 101,531 | 140 | 0.561 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 547,209 | 5.472 | 20 | 24 | fits | 17,647 | 28 | 0.336 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 99,609 | 0.996 | 20 | 50 | fits | 101,531 | 140 | 0.561 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 290,247 | 2.902 | 20 | 50 | fits | 44,590 | 54 | 0.381 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 197,479 | 1.975 | 18 | 18 | fits | 98,325 | 116 | 0.534 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 552,080 | 5.521 | 18 | 18 | fits | 7,406 | 19 | 0.133 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 245,970 | 2.460 | 20 | 20 | fits | 83,234 | 80 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 58,379 | 0.584 | 20 | 200 | fits | 63,061 | 134 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 321,741 | 3.217 | 20 | 200 | fits | 83,234 | 80 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 59,291 | 0.593 | 20 | 20 | fits | 63,061 | 134 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 434,650 | 4.346 | 20 | 20 | fits | 46,088 | 36 | 0.599 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 62,876 | 0.629 | 20 | 24 | fits | 63,061 | 134 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 858,421 | 8.584 | 20 | 24 | fits | 40,715 | 28 | 0.660 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 61,836 | 0.618 | 20 | 50 | fits | 63,061 | 134 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 325,417 | 3.254 | 20 | 50 | fits | 83,234 | 80 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 161,204 | 1.612 | 18 | 18 | fits | 99,823 | 137 | 0.582 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 911,482 | 9.115 | 18 | 18 | fits | 27,490 | 17 | 0.728 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 6,756 | 0.068 | 20 | 20 | fits | 17,399 | 20 | 0.699 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 58,379 | 0.584 | 20 | 200 | fits | 63,061 | 134 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 18,354 | 0.184 | 20 | 200 | fits | 17,399 | 20 | 0.699 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 59,291 | 0.593 | 20 | 20 | fits | 63,061 | 134 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 441,113 | 4.411 | 20 | 20 | fits | 61,821 | 41 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 62,876 | 0.629 | 20 | 24 | fits | 63,061 | 134 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 863,681 | 8.637 | 20 | 24 | fits | 40,674 | 28 | 0.660 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 61,836 | 0.618 | 20 | 50 | fits | 63,061 | 134 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 316,198 | 3.162 | 20 | 50 | fits | 74,015 | 70 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 161,204 | 1.612 | 18 | 18 | fits | 99,823 | 137 | 0.582 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 907,925 | 9.079 | 18 | 18 | fits | 18,589 | 14 | 0.755 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,159,598 | 61.596 | 20 | 20 | MISS ceiling | 22,385 | 24 | 0.426 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,013,980 | 360.140 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,013,905 | 360.139 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,013,830 | 360.138 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,013,755 | 360.138 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 64,038 | 0.640 | 20 | 200 | fits | 60,439 | 128 | 0.429 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 310,786 | 3.108 | 20 | 200 | fits | 72,078 | 66 | 0.627 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 59,779 | 0.598 | 20 | 20 | fits | 60,439 | 128 | 0.429 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 414,163 | 4.142 | 20 | 20 | fits | 52,246 | 32 | 0.733 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 63,364 | 0.634 | 20 | 24 | fits | 60,439 | 128 | 0.429 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,225,302 | 62.253 | 20 | 24 | MISS ceiling | 16,419 | 20 | 0.422 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 62,324 | 0.623 | 20 | 50 | fits | 60,439 | 128 | 0.429 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 309,291 | 3.093 | 20 | 50 | fits | 72,078 | 66 | 0.627 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 159,007 | 1.590 | 18 | 18 | fits | 97,138 | 130 | 0.605 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 741,809 | 7.418 | 18 | 18 | fits | 19,179 | 17 | 0.754 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
