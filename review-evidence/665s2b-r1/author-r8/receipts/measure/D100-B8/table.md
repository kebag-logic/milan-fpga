### 8x8

4 of 17 paths and 13 of 49 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.632 (8.333) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.381 (5.782) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.235 (0.722) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.115 (4.308) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.418 (63.798) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.402 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.979 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.280 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.021 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.730 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.516 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.015 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.677 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.004 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.501 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.284 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 15.195 | MISS T_svc | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.310 | 18 | 228,409 (2.284) | yes | - |
| backlog-adp | 15.735 | 17 | 182,689 (1.827) | yes | - |
| backlog-adp-refill | 41.215 | 22 | 182,689 (1.827) | yes | - |
| backlog-owed | 360.453 | 66 | 184,947 (1.849) | yes | - |

Composed maximum over the 4 backlog windows: 228,409 CPU cycles (2.284 ms), backlog.
Over the windows that released their whole load only: 228,409 (2.284 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 211,509 | 2.115 | 10 | 200 | fits | 228,409 | 136 | 0.701 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 763,179 | 7.632 | 10 | 20 | fits | 104,347 | 50 | 0.651 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 202,146 | 2.021 | 10 | 200 | fits | 202,354 | 144 | 0.642 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 651,639 | 6.516 | 10 | 200 | fits | 104,706 | 55 | 0.615 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 197,887 | 1.979 | 10 | 20 | fits | 202,354 | 144 | 0.642 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 827,971 | 8.280 | 10 | 20 | fits | 104,347 | 50 | 0.651 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 201,472 | 2.015 | 10 | 24 | fits | 202,354 | 144 | 0.642 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,315,722 | 13.157 | 10 | 24 | MISS T_svc | 48,379 | 29 | 0.685 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 200,432 | 2.004 | 10 | 50 | fits | 202,354 | 144 | 0.642 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 650,144 | 6.501 | 10 | 50 | fits | 104,706 | 55 | 0.615 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 428,386 | 4.284 | 10 | 18 | fits | 228,409 | 136 | 0.701 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,380,374 | 13.804 | 10 | 18 | MISS T_svc | 33,268 | 18 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 438,078 | 4.381 | 10 | 20 | fits | 154,185 | 87 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 101,154 | 1.012 | 10 | 200 | fits | 105,836 | 138 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 572,951 | 5.730 | 10 | 200 | fits | 154,185 | 87 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 102,066 | 1.021 | 10 | 20 | fits | 105,836 | 138 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 798,517 | 7.985 | 10 | 20 | fits | 102,569 | 34 | 0.719 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 105,651 | 1.057 | 10 | 24 | fits | 105,836 | 138 | 0.450 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,522,003 | 15.220 | 10 | 24 | MISS T_svc | 74,442 | 35 | 0.751 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 104,611 | 1.046 | 10 | 50 | fits | 105,836 | 138 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 576,627 | 5.766 | 10 | 50 | fits | 154,185 | 87 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 286,845 | 2.868 | 10 | 18 | fits | 182,689 | 138 | 0.640 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,519,468 | 15.195 | 10 | 18 | MISS T_svc | 74,442 | 35 | 0.751 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 23,455 | 0.235 | 10 | 20 | fits | 41,232 | 21 | 0.713 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 101,154 | 1.012 | 10 | 200 | fits | 105,836 | 138 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 55,894 | 0.559 | 10 | 200 | fits | 41,232 | 21 | 0.713 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 102,066 | 1.021 | 10 | 20 | fits | 105,836 | 138 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 777,311 | 7.773 | 10 | 20 | fits | 111,489 | 44 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 105,651 | 1.057 | 10 | 24 | fits | 105,836 | 138 | 0.450 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,427,258 | 14.273 | 10 | 24 | MISS T_svc | 64,259 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 104,611 | 1.046 | 10 | 50 | fits | 105,836 | 138 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 556,187 | 5.562 | 10 | 50 | fits | 133,745 | 77 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 286,845 | 2.868 | 10 | 18 | fits | 182,689 | 138 | 0.640 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,482,887 | 14.829 | 10 | 18 | MISS T_svc | 58,164 | 26 | 0.790 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,341,771 | 63.418 | 10 | 20 | MISS ceiling | 46,426 | 25 | 0.454 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,040,206 | 360.402 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,040,131 | 360.401 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,040,056 | 360.401 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,039,981 | 360.400 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 104,905 | 1.049 | 10 | 200 | fits | 103,752 | 132 | 0.450 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 517,095 | 5.171 | 10 | 200 | fits | 126,399 | 67 | 0.686 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 100,646 | 1.006 | 10 | 20 | fits | 103,752 | 132 | 0.450 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 713,147 | 7.131 | 10 | 20 | fits | 98,604 | 33 | 0.758 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 104,231 | 1.042 | 10 | 24 | fits | 103,752 | 132 | 0.450 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,467,725 | 64.677 | 10 | 24 | MISS ceiling | 29,127 | 21 | 0.495 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 103,191 | 1.032 | 10 | 50 | fits | 103,752 | 132 | 0.450 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 515,600 | 5.156 | 10 | 50 | fits | 126,399 | 67 | 0.686 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 389,136 | 3.891 | 10 | 18 | fits | 184,947 | 95 | 0.701 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,343,097 | 13.431 | 10 | 18 | MISS T_svc | 35,637 | 18 | 0.791 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
