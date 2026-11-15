### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 12 paths and 7 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.006 (63.283) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.727 (64.002) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 1.784 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.127 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 1.827 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 2.769 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.820 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.880 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 1.809 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 2.754 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 2.753 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 7.577 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 64.831 | 26 | 171,743 (1.717) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 171,743 CPU cycles (1.717 ms), backlog-owed.
Over the windows that released their whole load only: 171,743 (1.717 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-owed | 311 | 0 | 171,743 (1.717) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-owed | 277 | 22,059 (0.221) | 2,259 (0.023) |

Longest pass that carries a step: 22,059 CPU cycles (0.221 ms), backlog-owed; longest step: 2,259 (0.023 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,300,616 | 63.006 | 20 | 20 | MISS ceiling | 18,127 | 13 | 0.658 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,318,750 | 63.188 | 20 | 20 | MISS ceiling | 18,131 | 13 | 0.658 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,336,752 | 63.368 | 20 | 20 | MISS ceiling | 18,059 | 13 | 0.667 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,354,744 | 63.547 | 20 | 20 | MISS ceiling | 18,068 | 13 | 0.667 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,372,697 | 63.727 | 20 | 20 | MISS ceiling | 17,942 | 13 | 0.662 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 182,684 | 1.827 | 20 | 200 | fits | 171,743 | 224 | 0.425 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 276,902 | 2.769 | 20 | 200 | fits | 94,834 | 163 | 0.532 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 178,362 | 1.784 | 20 | 20 | fits | 171,743 | 224 | 0.425 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,212,672 | 62.127 | 20 | 20 | MISS ceiling | 28,129 | 15 | 0.755 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 182,002 | 1.820 | 20 | 24 | fits | 171,743 | 224 | 0.425 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,188,029 | 61.880 | 20 | 24 | MISS ceiling | 144,417 | 106 | 0.469 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 180,946 | 1.809 | 20 | 50 | fits | 171,743 | 224 | 0.425 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 275,384 | 2.754 | 20 | 50 | fits | 94,834 | 163 | 0.532 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 275,318 | 2.753 | 20 | 20 | fits | 94,834 | 163 | 0.532 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 757,726 | 7.577 | 20 | 20 | fits | 44,404 | 16 | 0.760 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
