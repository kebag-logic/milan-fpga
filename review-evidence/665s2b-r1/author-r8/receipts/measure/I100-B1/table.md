### 1x1

4 of 16 paths and 10 of 49 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.141 (4.459) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.970 (3.935) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.073 (0.254) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.259 (2.289) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.892 (62.059) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.152 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.130 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 5.435 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.173 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.882 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.166 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.682 | MISS ceiling | 15 aecp | 4 | 3 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.155 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.919 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.265 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 10.714 | MISS T_svc | 31 srp | 4 | 2 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.959 | 17 | 117,470 (1.175) | yes | - |
| backlog-adp | 10.917 | 18 | 116,361 (1.164) | yes | - |
| backlog-adp-refill | 40.502 | 24 | 116,361 (1.164) | yes | - |
| backlog-owed | 360.203 | 64 | 113,091 (1.131) | yes | - |

Composed maximum over the 4 backlog windows: 117,470 CPU cycles (1.175 ms), backlog.
Over the windows that released their whole load only: 117,470 (1.175 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 125,920 | 1.259 | 10 | 200 | fits | 111,425 | 394 | 0.418 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 414,107 | 4.141 | 10 | 20 | fits | 49,582 | 249 | 0.266 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 117,262 | 1.173 | 10 | 200 | fits | 117,470 | 388 | 0.457 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 345,719 | 3.457 | 10 | 200 | fits | 56,561 | 317 | 0.254 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 113,003 | 1.130 | 10 | 20 | fits | 117,470 | 388 | 0.457 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 440,594 | 4.406 | 10 | 20 | fits | 49,582 | 249 | 0.266 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 116,588 | 1.166 | 10 | 24 | fits | 117,470 | 388 | 0.457 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 670,470 | 6.705 | 10 | 24 | fits | 22,550 | 162 | 0.214 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 115,548 | 1.155 | 10 | 50 | fits | 117,470 | 388 | 0.457 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 344,224 | 3.442 | 10 | 50 | fits | 56,561 | 317 | 0.254 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 226,518 | 2.265 | 10 | 18 | fits | 111,425 | 394 | 0.418 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 676,778 | 6.768 | 10 | 18 | fits | 8,843 | 49 | 0.140 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 296,956 | 2.970 | 10 | 20 | fits | 99,556 | 343 | 0.511 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 74,692 | 0.747 | 10 | 200 | fits | 79,374 | 382 | 0.338 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 388,217 | 3.882 | 10 | 200 | fits | 99,556 | 343 | 0.511 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 75,604 | 0.756 | 10 | 20 | fits | 79,374 | 382 | 0.338 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 543,460 | 5.435 | 10 | 20 | fits | 66,167 | 135 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 79,189 | 0.792 | 10 | 24 | fits | 79,374 | 382 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,042,451 | 10.425 | 10 | 24 | MISS T_svc | 46,438 | 162 | 0.525 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 78,149 | 0.781 | 10 | 50 | fits | 79,374 | 382 | 0.338 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 391,893 | 3.919 | 10 | 50 | fits | 99,556 | 343 | 0.511 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 194,055 | 1.941 | 10 | 18 | fits | 116,361 | 415 | 0.475 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,071,382 | 10.714 | 10 | 18 | MISS T_svc | 31,466 | 49 | 0.718 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 7,340 | 0.073 | 10 | 20 | fits | 18,569 | 41 | 0.637 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 74,692 | 0.747 | 10 | 200 | fits | 79,374 | 382 | 0.338 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 20,034 | 0.200 | 10 | 200 | fits | 18,569 | 41 | 0.637 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 75,604 | 0.756 | 10 | 20 | fits | 79,374 | 382 | 0.338 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 533,841 | 5.338 | 10 | 20 | fits | 77,647 | 249 | 0.509 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 79,189 | 0.792 | 10 | 24 | fits | 79,374 | 382 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 1,000,707 | 10.007 | 10 | 24 | MISS T_svc | 46,438 | 162 | 0.525 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 78,149 | 0.781 | 10 | 50 | fits | 79,374 | 382 | 0.338 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 380,759 | 3.808 | 10 | 50 | fits | 88,422 | 312 | 0.493 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 194,055 | 1.941 | 10 | 18 | fits | 116,361 | 415 | 0.475 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,053,210 | 10.532 | 10 | 18 | MISS T_svc | 21,446 | 29 | 0.758 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,189,219 | 61.892 | 10 | 20 | MISS ceiling | 26,124 | 146 | 0.247 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,015,226 | 360.152 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,015,151 | 360.152 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,015,076 | 360.151 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,015,001 | 360.150 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 79,803 | 0.798 | 10 | 200 | fits | 76,161 | 340 | 0.340 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 374,709 | 3.747 | 10 | 200 | fits | 87,245 | 293 | 0.508 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 75,544 | 0.755 | 10 | 20 | fits | 76,161 | 340 | 0.340 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 496,585 | 4.966 | 10 | 20 | fits | 64,230 | 119 | 0.697 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 79,129 | 0.791 | 10 | 24 | fits | 76,161 | 340 | 0.340 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,268,227 | 62.682 | 10 | 24 | MISS ceiling | 19,941 | 124 | 0.266 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 78,089 | 0.781 | 10 | 50 | fits | 76,161 | 340 | 0.340 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 373,214 | 3.732 | 10 | 50 | fits | 87,245 | 293 | 0.508 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 190,725 | 1.907 | 10 | 18 | fits | 113,091 | 372 | 0.505 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 854,917 | 8.549 | 10 | 18 | fits | 32,468 | 50 | 0.719 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
