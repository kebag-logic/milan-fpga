### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 12 paths and 7 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.984 (64.293) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.762 (65.065) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 3.063 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 63.003 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 3.106 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 4.402 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.581 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 63.038 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 3.089 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 3.085 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 4.386 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 7.605 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 65.406 | 23 | 171,589 (1.716) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 171,589 CPU cycles (1.716 ms), backlog-owed.
Over the windows that released their whole load only: 171,589 (1.716 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-owed | 307 | 0 | 171,589 (1.716) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-owed | 277 | 23,226 (0.232) | 3,043 (0.030) |

Longest pass that carries a step: 23,226 CPU cycles (0.232 ms), backlog-owed; longest step: 3,043 (0.030 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,398,379 | 63.984 | 20 | 20 | MISS ceiling | 20,167 | 13 | 0.525 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,418,346 | 64.183 | 20 | 20 | MISS ceiling | 19,447 | 13 | 0.434 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,437,609 | 64.376 | 20 | 20 | MISS ceiling | 19,339 | 13 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,456,875 | 64.569 | 20 | 20 | MISS ceiling | 19,342 | 13 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,476,166 | 64.762 | 20 | 20 | MISS ceiling | 19,354 | 13 | 0.451 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 310,639 | 3.106 | 20 | 200 | fits | 151,824 | 252 | 0.234 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 440,161 | 4.402 | 20 | 200 | fits | 130,138 | 59 | 0.638 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 306,317 | 3.063 | 20 | 20 | fits | 151,824 | 252 | 0.234 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,300,340 | 63.003 | 20 | 20 | MISS ceiling | 92,715 | 42 | 0.518 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,133 | 1.581 | 20 | 24 | fits | 145,932 | 107 | 0.425 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,303,826 | 63.038 | 20 | 24 | MISS ceiling | 92,715 | 42 | 0.518 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 308,901 | 3.089 | 20 | 50 | fits | 151,824 | 252 | 0.234 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 308,505 | 3.085 | 20 | 50 | fits | 151,824 | 252 | 0.234 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 438,577 | 4.386 | 20 | 20 | fits | 130,138 | 59 | 0.638 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 760,470 | 7.605 | 20 | 20 | fits | 62,063 | 24 | 0.707 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
