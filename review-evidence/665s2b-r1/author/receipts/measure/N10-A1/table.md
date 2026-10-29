### 1x1

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.072 (4.398) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.016 (3.987) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.063 (0.296) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.237 (2.244) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.988 (62.160) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.164 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.096 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 5.508 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.139 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.934 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.132 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.813 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.122 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.971 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.220 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 10.532 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.962 | 17 | 114,107 (1.141) | yes | - |
| backlog-adp | 10.805 | 17 | 113,923 (1.139) | yes | - |
| backlog-adp-refill | 40.452 | 28 | 113,923 (1.139) | yes | - |
| backlog-owed | 360.215 | 65 | 110,518 (1.105) | yes | - |

Composed maximum over the 4 backlog windows: 114,107 CPU cycles (1.141 ms), backlog.
Over the windows that released their whole load only: 114,107 (1.141 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 123,708 | 1.237 | 20 | 200 | fits | 110,308 | 117 | 0.593 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 407,154 | 4.072 | 20 | 20 | fits | 49,693 | 44 | 0.490 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 113,899 | 1.139 | 20 | 200 | fits | 114,107 | 141 | 0.612 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 339,043 | 3.390 | 20 | 200 | fits | 56,083 | 55 | 0.483 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 109,640 | 1.096 | 20 | 20 | fits | 114,107 | 141 | 0.612 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 434,509 | 4.345 | 20 | 20 | fits | 49,693 | 44 | 0.490 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 113,225 | 1.132 | 20 | 24 | fits | 114,107 | 141 | 0.612 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 664,802 | 6.648 | 20 | 24 | fits | 22,593 | 29 | 0.473 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 112,185 | 1.122 | 20 | 50 | fits | 114,107 | 141 | 0.612 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 337,548 | 3.375 | 20 | 50 | fits | 56,083 | 55 | 0.483 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 222,038 | 2.220 | 18 | 18 | fits | 110,308 | 117 | 0.593 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 671,941 | 6.719 | 18 | 18 | fits | 9,674 | 19 | 0.314 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 301,593 | 3.016 | 20 | 20 | fits | 109,963 | 98 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 74,806 | 0.748 | 20 | 200 | fits | 79,488 | 135 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 393,413 | 3.934 | 20 | 200 | fits | 109,963 | 98 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 75,718 | 0.757 | 20 | 20 | fits | 79,488 | 135 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 550,789 | 5.508 | 20 | 20 | fits | 77,673 | 44 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 79,303 | 0.793 | 20 | 24 | fits | 79,488 | 135 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,024,760 | 10.248 | 20 | 24 | fits | 46,172 | 29 | 0.724 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 78,263 | 0.783 | 20 | 50 | fits | 79,488 | 135 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 397,089 | 3.971 | 20 | 50 | fits | 109,963 | 98 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 191,731 | 1.917 | 18 | 18 | fits | 113,923 | 138 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,053,226 | 10.532 | 18 | 18 | fits | 31,001 | 19 | 0.776 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 6,287 | 0.063 | 20 | 20 | fits | 21,704 | 20 | 0.774 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 74,806 | 0.748 | 20 | 200 | fits | 79,488 | 135 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 22,068 | 0.221 | 20 | 200 | fits | 21,704 | 20 | 0.774 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 75,718 | 0.757 | 20 | 20 | fits | 79,488 | 135 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 540,507 | 5.405 | 20 | 20 | fits | 77,666 | 44 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 79,303 | 0.793 | 20 | 24 | fits | 79,488 | 135 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 990,483 | 9.905 | 20 | 24 | fits | 46,172 | 29 | 0.724 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 78,263 | 0.783 | 20 | 50 | fits | 79,488 | 135 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 386,870 | 3.869 | 20 | 50 | fits | 99,744 | 88 | 0.694 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 191,731 | 1.917 | 18 | 18 | fits | 113,923 | 138 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,050,728 | 10.507 | 18 | 18 | fits | 31,816 | 21 | 0.722 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,198,758 | 61.988 | 20 | 20 | MISS ceiling | 27,725 | 25 | 0.579 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,016,415 | 360.164 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,016,340 | 360.163 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,016,265 | 360.163 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,016,190 | 360.162 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 76,952 | 0.770 | 20 | 200 | fits | 74,186 | 129 | 0.489 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 362,062 | 3.621 | 20 | 200 | fits | 84,338 | 67 | 0.669 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 72,693 | 0.727 | 20 | 20 | fits | 74,186 | 129 | 0.489 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 470,715 | 4.707 | 20 | 20 | fits | 50,869 | 29 | 0.790 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 76,278 | 0.763 | 20 | 24 | fits | 74,186 | 129 | 0.489 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,281,318 | 62.813 | 20 | 24 | MISS ceiling | 21,143 | 21 | 0.581 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 75,238 | 0.752 | 20 | 50 | fits | 74,186 | 129 | 0.489 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 360,567 | 3.606 | 20 | 50 | fits | 84,338 | 67 | 0.669 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 185,301 | 1.853 | 18 | 18 | fits | 110,518 | 131 | 0.645 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 840,441 | 8.404 | 18 | 18 | fits | 23,176 | 17 | 0.816 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
