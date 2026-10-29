### 1x1

4 of 16 paths and 8 of 49 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.911 (4.201) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.878 (3.823) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.112 (0.305) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.216 (2.195) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.702 (61.863) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.121 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.090 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 5.089 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.133 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.770 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.126 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.403 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.116 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.807 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.171 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 10.405 | MISS T_svc | 31 srp | 4 | 2 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.415 | 17 | 113,515 (1.135) | yes | - |
| backlog-adp | 10.621 | 19 | 114,686 (1.147) | yes | - |
| backlog-adp-refill | 40.424 | 30 | 114,686 (1.147) | yes | - |
| backlog-owed | 360.172 | 65 | 111,076 (1.111) | yes | - |

Composed maximum over the 4 backlog windows: 114,686 CPU cycles (1.147 ms), backlog-adp.
Over the windows that released their whole load only: 114,686 (1.147 ms), backlog-adp.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 121,625 | 1.216 | 10 | 200 | fits | 105,961 | 116 | 0.523 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 391,084 | 3.911 | 10 | 20 | fits | 45,935 | 43 | 0.388 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 113,307 | 1.133 | 10 | 200 | fits | 113,515 | 140 | 0.564 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 327,096 | 3.271 | 10 | 200 | fits | 52,122 | 54 | 0.364 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 109,048 | 1.090 | 10 | 20 | fits | 113,515 | 140 | 0.564 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 414,759 | 4.148 | 10 | 20 | fits | 45,935 | 43 | 0.388 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 112,633 | 1.126 | 10 | 24 | fits | 113,515 | 140 | 0.564 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 616,313 | 6.163 | 10 | 24 | fits | 19,712 | 28 | 0.331 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 111,593 | 1.116 | 10 | 50 | fits | 113,515 | 140 | 0.564 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 325,601 | 3.256 | 10 | 50 | fits | 52,122 | 54 | 0.364 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 217,099 | 2.171 | 10 | 18 | fits | 105,961 | 116 | 0.523 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 621,871 | 6.219 | 10 | 18 | fits | 8,093 | 19 | 0.093 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 287,848 | 2.878 | 10 | 20 | fits | 96,897 | 80 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 70,572 | 0.706 | 10 | 200 | fits | 75,254 | 134 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 376,997 | 3.770 | 10 | 200 | fits | 96,897 | 80 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 71,484 | 0.715 | 10 | 20 | fits | 75,254 | 134 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 508,854 | 5.089 | 10 | 20 | fits | 76,573 | 49 | 0.658 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 75,069 | 0.751 | 10 | 24 | fits | 75,254 | 134 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 948,747 | 9.487 | 10 | 24 | fits | 45,369 | 28 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 74,029 | 0.740 | 10 | 50 | fits | 75,254 | 134 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 380,673 | 3.807 | 10 | 50 | fits | 96,897 | 80 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 188,260 | 1.883 | 10 | 18 | fits | 114,686 | 137 | 0.598 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,040,548 | 10.405 | 10 | 18 | MISS T_svc | 31,210 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,201 | 0.112 | 10 | 20 | fits | 19,257 | 20 | 0.726 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 70,572 | 0.706 | 10 | 200 | fits | 75,254 | 134 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 24,704 | 0.247 | 10 | 200 | fits | 19,257 | 20 | 0.726 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 71,484 | 0.715 | 10 | 20 | fits | 75,254 | 134 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 498,373 | 4.984 | 10 | 20 | fits | 76,550 | 49 | 0.657 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 75,069 | 0.751 | 10 | 24 | fits | 75,254 | 134 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 955,732 | 9.557 | 10 | 24 | fits | 45,602 | 28 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 74,029 | 0.740 | 10 | 50 | fits | 75,254 | 134 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 370,344 | 3.703 | 10 | 50 | fits | 86,568 | 70 | 0.635 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 188,260 | 1.883 | 10 | 18 | fits | 114,686 | 137 | 0.598 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,039,582 | 10.396 | 10 | 18 | MISS T_svc | 23,091 | 18 | 0.707 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,170,150 | 61.702 | 10 | 20 | MISS ceiling | 23,666 | 24 | 0.393 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,012,117 | 360.121 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,012,042 | 360.120 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,011,967 | 360.120 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,011,892 | 360.119 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 73,715 | 0.737 | 10 | 200 | fits | 72,343 | 128 | 0.442 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 360,171 | 3.602 | 10 | 200 | fits | 84,182 | 66 | 0.645 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 69,456 | 0.695 | 10 | 20 | fits | 72,343 | 128 | 0.442 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 447,151 | 4.472 | 10 | 20 | fits | 31,424 | 23 | 0.673 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 73,041 | 0.730 | 10 | 24 | fits | 72,343 | 128 | 0.442 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,240,337 | 62.403 | 10 | 24 | MISS ceiling | 17,938 | 20 | 0.438 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 72,001 | 0.720 | 10 | 50 | fits | 72,343 | 128 | 0.442 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 358,676 | 3.587 | 10 | 50 | fits | 84,182 | 66 | 0.645 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 182,622 | 1.826 | 10 | 18 | fits | 111,076 | 130 | 0.618 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 849,022 | 8.490 | 10 | 18 | fits | 32,783 | 20 | 0.781 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
