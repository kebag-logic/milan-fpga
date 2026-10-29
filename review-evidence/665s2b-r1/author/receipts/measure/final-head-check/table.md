### 1x1

0 of 12 paths and 0 of 12 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.072 (4.398) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.237 (2.244) | fits | 15 events | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.096 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 4.345 | fits | 11 acmp | 1 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.139 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 3.390 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.132 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 6.648 | fits | 15 aecp | 1 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.122 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 3.375 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.220 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog.service.srp.last.if0` (backlog) | 6.719 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.962 | 17 | 114,107 (1.141) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 114,107 CPU cycles (1.141 ms), backlog.
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

Bounded waits that timed out (the probe is graded on what the log holds):

- none
