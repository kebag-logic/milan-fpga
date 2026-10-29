### 1x1

0 of 12 paths and 0 of 12 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.911 (4.201) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.216 (2.195) | fits | 15 events | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.090 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 4.148 | fits | 11 acmp | 1 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.133 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 3.271 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.126 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 6.163 | fits | 15 aecp | 1 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.116 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 3.256 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.171 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog.service.srp.last.if0` (backlog) | 6.219 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.415 | 17 | 113,515 (1.135) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 113,515 CPU cycles (1.135 ms), backlog.
Over the windows that released their whole load only: 113,515 (1.135 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 121,625 | 1.216 | 20 | 200 | fits | 105,961 | 116 | 0.523 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 391,084 | 3.911 | 20 | 20 | fits | 45,935 | 43 | 0.388 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 113,307 | 1.133 | 20 | 200 | fits | 113,515 | 140 | 0.564 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 327,096 | 3.271 | 20 | 200 | fits | 52,122 | 54 | 0.364 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 109,048 | 1.090 | 20 | 20 | fits | 113,515 | 140 | 0.564 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 414,759 | 4.148 | 20 | 20 | fits | 45,935 | 43 | 0.388 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 112,633 | 1.126 | 20 | 24 | fits | 113,515 | 140 | 0.564 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 616,313 | 6.163 | 20 | 24 | fits | 19,712 | 28 | 0.331 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 111,593 | 1.116 | 20 | 50 | fits | 113,515 | 140 | 0.564 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 325,601 | 3.256 | 20 | 50 | fits | 52,122 | 54 | 0.364 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 217,099 | 2.171 | 18 | 18 | fits | 105,961 | 116 | 0.523 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 621,871 | 6.219 | 18 | 18 | fits | 8,093 | 19 | 0.093 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
