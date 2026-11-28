### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 12 paths and 7 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.165 (64.543) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 65.091 (65.452) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 3.113 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 63.063 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 3.157 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 4.487 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.586 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 63.098 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 3.139 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 3.135 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 4.472 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 7.773 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 65.846 | 23 | 173,642 (1.736) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 173,642 CPU cycles (1.736 ms), backlog-owed.
Over the windows that released their whole load only: 173,642 (1.736 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-owed | 308 | 0 | 173,642 (1.736) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-owed | 277 | 26,540 (0.265) | 3,064 (0.031) |

Longest pass that carries a step: 26,540 CPU cycles (0.265 ms), backlog-owed; longest step: 3,064 (0.031 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,416,493 | 64.165 | 20 | 20 | MISS ceiling | 24,339 | 13 | 0.579 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,441,025 | 64.410 | 20 | 20 | MISS ceiling | 23,476 | 13 | 0.610 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,464,140 | 64.641 | 20 | 20 | MISS ceiling | 22,688 | 13 | 0.551 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,486,682 | 64.867 | 20 | 20 | MISS ceiling | 22,594 | 13 | 0.561 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,509,121 | 65.091 | 20 | 20 | MISS ceiling | 22,424 | 13 | 0.571 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 315,660 | 3.157 | 20 | 200 | fits | 156,342 | 256 | 0.283 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 448,747 | 4.487 | 20 | 200 | fits | 133,703 | 129 | 0.586 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 311,338 | 3.113 | 20 | 20 | fits | 156,342 | 256 | 0.283 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,306,334 | 63.063 | 20 | 20 | MISS ceiling | 95,744 | 42 | 0.531 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,636 | 1.586 | 20 | 24 | fits | 146,802 | 107 | 0.393 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,309,820 | 63.098 | 20 | 24 | MISS ceiling | 95,744 | 42 | 0.531 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 313,922 | 3.139 | 20 | 50 | fits | 156,342 | 256 | 0.283 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 313,526 | 3.135 | 20 | 50 | fits | 156,342 | 256 | 0.283 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 447,163 | 4.472 | 20 | 20 | fits | 133,703 | 129 | 0.586 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 777,336 | 7.773 | 20 | 20 | fits | 67,174 | 60 | 0.673 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
