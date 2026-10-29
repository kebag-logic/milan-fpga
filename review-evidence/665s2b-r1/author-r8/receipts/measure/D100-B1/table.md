### 1x1

3 of 16 paths and 6 of 49 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.439 (3.719) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.477 (3.288) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.086 (0.252) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.097 (1.989) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.680 (61.821) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.161 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 0.969 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 4.548 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.012 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.235 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.005 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.359 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 0.995 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.272 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 1.966 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 9.261 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 5.768 | 17 | 101,398 (1.014) | yes | - |
| backlog-adp | 9.459 | 18 | 100,024 (1.000) | yes | - |
| backlog-adp-refill | 40.487 | 25 | 100,024 (1.000) | yes | - |
| backlog-owed | 360.212 | 64 | 99,094 (0.991) | yes | - |

Composed maximum over the 4 backlog windows: 101,398 CPU cycles (1.014 ms), backlog.
Over the windows that released their whole load only: 101,398 (1.014 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 109,652 | 1.097 | 10 | 200 | fits | 97,531 | 116 | 0.533 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 343,892 | 3.439 | 10 | 20 | fits | 39,735 | 43 | 0.417 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 101,190 | 1.012 | 10 | 200 | fits | 101,398 | 140 | 0.561 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 291,598 | 2.916 | 10 | 200 | fits | 44,961 | 54 | 0.384 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 96,931 | 0.969 | 10 | 20 | fits | 101,398 | 140 | 0.561 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 366,627 | 3.666 | 10 | 20 | fits | 39,735 | 43 | 0.417 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 100,516 | 1.005 | 10 | 24 | fits | 101,398 | 140 | 0.561 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 552,850 | 5.529 | 10 | 24 | fits | 18,175 | 28 | 0.336 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 99,476 | 0.995 | 10 | 50 | fits | 101,398 | 140 | 0.561 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 290,103 | 2.901 | 10 | 50 | fits | 44,961 | 54 | 0.384 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 196,552 | 1.966 | 10 | 18 | fits | 97,531 | 116 | 0.533 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 557,721 | 5.577 | 10 | 18 | fits | 7,406 | 19 | 0.133 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 247,681 | 2.477 | 10 | 20 | fits | 84,019 | 80 | 0.628 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 58,694 | 0.587 | 10 | 200 | fits | 63,376 | 134 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 323,529 | 3.235 | 10 | 200 | fits | 84,019 | 80 | 0.628 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 59,606 | 0.596 | 10 | 20 | fits | 63,376 | 134 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 454,790 | 4.548 | 10 | 20 | fits | 55,799 | 33 | 0.693 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 63,191 | 0.632 | 10 | 24 | fits | 63,376 | 134 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 899,807 | 8.998 | 10 | 24 | fits | 41,619 | 28 | 0.661 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 62,151 | 0.622 | 10 | 50 | fits | 63,376 | 134 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 327,205 | 3.272 | 10 | 50 | fits | 84,019 | 80 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 161,720 | 1.617 | 10 | 18 | fits | 100,024 | 137 | 0.579 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 926,111 | 9.261 | 10 | 18 | fits | 28,839 | 19 | 0.738 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,628 | 0.086 | 10 | 20 | fits | 17,033 | 20 | 0.684 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 58,694 | 0.587 | 10 | 200 | fits | 63,376 | 134 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 19,882 | 0.199 | 10 | 200 | fits | 17,033 | 20 | 0.684 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 59,606 | 0.596 | 10 | 20 | fits | 63,376 | 134 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 445,403 | 4.454 | 10 | 20 | fits | 65,317 | 43 | 0.638 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 63,191 | 0.632 | 10 | 24 | fits | 63,376 | 134 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 863,521 | 8.635 | 10 | 24 | fits | 41,619 | 28 | 0.661 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 62,151 | 0.622 | 10 | 50 | fits | 63,376 | 134 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 317,087 | 3.171 | 10 | 50 | fits | 73,901 | 70 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 161,720 | 1.617 | 10 | 18 | fits | 100,024 | 137 | 0.579 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 908,885 | 9.089 | 10 | 18 | fits | 19,060 | 14 | 0.760 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,167,986 | 61.680 | 10 | 20 | MISS ceiling | 23,093 | 24 | 0.426 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,016,147 | 360.161 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,016,072 | 360.161 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,015,997 | 360.160 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,015,922 | 360.159 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 65,217 | 0.652 | 10 | 200 | fits | 61,935 | 128 | 0.427 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 318,828 | 3.188 | 10 | 200 | fits | 74,519 | 66 | 0.630 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 60,958 | 0.610 | 10 | 20 | fits | 61,935 | 128 | 0.427 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 426,294 | 4.263 | 10 | 20 | fits | 54,325 | 32 | 0.733 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 64,543 | 0.645 | 10 | 24 | fits | 61,935 | 128 | 0.427 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,235,943 | 62.359 | 10 | 24 | MISS ceiling | 17,141 | 20 | 0.427 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 63,503 | 0.635 | 10 | 50 | fits | 61,935 | 128 | 0.427 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 317,333 | 3.173 | 10 | 50 | fits | 74,519 | 66 | 0.630 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 162,142 | 1.621 | 10 | 18 | fits | 99,094 | 130 | 0.609 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 756,897 | 7.569 | 10 | 18 | fits | 29,374 | 20 | 0.733 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
