Original file: budget/stop-regrade/table.md
Original size: 5843 bytes
Original sha256: 727cd99f96b0d204ac36599aed9004fab6d04c84b553513c7146e9aeabc25774

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 12 paths and 7 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.037 (63.332) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.780 (64.074) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 1.506 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.142 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 1.550 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 2.505 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.543 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.885 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 1.532 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 2.490 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 3.359 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 8.379 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 64.440 | 26 | 148,956 (1.490) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 148,956 CPU cycles (1.490 ms), backlog-owed.
Over the windows that released their whole load only: 148,956 (1.490 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-owed | 311 | 0 | 148,956 (1.490) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-owed | 276 | 21,403 (0.214) | 2,467 (0.025) |

Longest pass that carries a step: 21,403 CPU cycles (0.214 ms), backlog-owed; longest step: 2,467 (0.025 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,303,732 | 63.037 | 20 | 20 | MISS ceiling | 18,626 | 13 | 0.622 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,322,358 | 63.224 | 20 | 20 | MISS ceiling | 18,683 | 13 | 0.605 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,340,896 | 63.409 | 20 | 20 | MISS ceiling | 18,614 | 13 | 0.613 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,359,426 | 63.594 | 20 | 20 | MISS ceiling | 18,606 | 13 | 0.622 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,377,957 | 63.780 | 20 | 20 | MISS ceiling | 18,598 | 13 | 0.622 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 154,950 | 1.550 | 20 | 200 | fits | 147,497 | 200 | 0.474 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 250,500 | 2.505 | 20 | 200 | fits | 96,166 | 185 | 0.373 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 150,628 | 1.506 | 20 | 20 | fits | 147,497 | 200 | 0.474 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,214,233 | 62.142 | 20 | 20 | MISS ceiling | 29,236 | 15 | 0.750 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 154,268 | 1.543 | 20 | 24 | fits | 147,497 | 200 | 0.474 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,188,483 | 61.885 | 20 | 24 | MISS ceiling | 148,956 | 106 | 0.488 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 153,212 | 1.532 | 20 | 50 | fits | 147,497 | 200 | 0.474 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 248,982 | 2.490 | 20 | 50 | fits | 96,166 | 185 | 0.373 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 335,914 | 3.359 | 20 | 20 | fits | 86,998 | 24 | 0.769 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 837,946 | 8.379 | 20 | 20 | fits | 74,000 | 24 | 0.627 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
