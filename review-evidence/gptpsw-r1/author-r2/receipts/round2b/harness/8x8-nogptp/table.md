### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 12 paths and 7 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.226 (63.419) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.255 (64.463) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 1.582 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.093 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 1.626 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 2.977 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.619 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 61.771 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 1.608 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 2.962 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 2.961 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-owed.service.srp.last.if1` (backlog-owed) | 7.428 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 65.112 | 23 | 158,061 (1.581) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 158,061 CPU cycles (1.581 ms), backlog-owed.
Over the windows that released their whole load only: 158,061 (1.581 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-owed | 317 | 0 | 158,061 (1.581) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-owed | 277 | 26,735 (0.267) | 2,707 (0.027) |

Longest pass that carries a step: 26,735 CPU cycles (0.267 ms), backlog-owed; longest step: 2,707 (0.027 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,322,630 | 63.226 | 20 | 20 | MISS ceiling | 24,741 | 14 | 0.472 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,347,241 | 63.472 | 20 | 20 | MISS ceiling | 24,687 | 14 | 0.446 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,371,724 | 63.717 | 20 | 20 | MISS ceiling | 24,698 | 14 | 0.472 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,402,866 | 64.029 | 20 | 20 | MISS ceiling | 29,448 | 19 | 0.620 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,425,533 | 64.255 | 20 | 20 | MISS ceiling | 25,513 | 14 | 0.476 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 162,569 | 1.626 | 20 | 200 | fits | 158,061 | 231 | 0.357 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 297,699 | 2.977 | 20 | 200 | fits | 135,746 | 170 | 0.462 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 158,247 | 1.582 | 20 | 20 | fits | 158,061 | 231 | 0.357 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,209,343 | 62.093 | 20 | 20 | MISS ceiling | 35,694 | 16 | 0.635 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 161,887 | 1.619 | 20 | 24 | fits | 158,061 | 231 | 0.357 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,177,135 | 61.771 | 20 | 24 | MISS ceiling | 131,681 | 117 | 0.343 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 160,831 | 1.608 | 20 | 50 | fits | 158,061 | 231 | 0.357 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 296,181 | 2.962 | 20 | 50 | fits | 135,746 | 170 | 0.462 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 296,115 | 2.961 | 20 | 20 | fits | 135,746 | 170 | 0.462 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 742,757 | 7.428 | 20 | 20 | fits | 88,966 | 33 | 0.753 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
