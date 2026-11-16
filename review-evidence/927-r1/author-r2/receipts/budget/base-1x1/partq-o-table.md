### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 12 paths and 7 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.905 (63.201) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.652 (63.948) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 1.559 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.002 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 1.602 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 2.469 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.595 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.736 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 1.585 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 2.453 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 3.312 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 8.266 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 64.307 | 26 | 149,154 (1.492) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 149,154 CPU cycles (1.492 ms), backlog-owed.
Over the windows that released their whole load only: 149,154 (1.492 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-owed | 311 | 0 | 149,154 (1.492) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-owed | 276 | 22,507 (0.225) | 2,414 (0.024) |

Longest pass that carries a step: 22,507 CPU cycles (0.225 ms), backlog-owed; longest step: 2,414 (0.024 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,290,483 | 62.905 | 20 | 20 | MISS ceiling | 18,812 | 14 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,309,229 | 63.092 | 20 | 20 | MISS ceiling | 18,822 | 13 | 0.630 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,327,978 | 63.280 | 20 | 20 | MISS ceiling | 18,806 | 13 | 0.630 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,346,639 | 63.466 | 20 | 20 | MISS ceiling | 18,737 | 13 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,365,221 | 63.652 | 20 | 20 | MISS ceiling | 18,645 | 13 | 0.654 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 160,211 | 1.602 | 20 | 200 | fits | 149,154 | 204 | 0.437 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 246,865 | 2.469 | 20 | 200 | fits | 87,270 | 179 | 0.395 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 155,889 | 1.559 | 20 | 20 | fits | 149,154 | 204 | 0.437 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,200,208 | 62.002 | 20 | 20 | MISS ceiling | 30,113 | 15 | 0.781 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 159,529 | 1.595 | 20 | 24 | fits | 149,154 | 204 | 0.437 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,173,581 | 61.736 | 20 | 24 | MISS ceiling | 141,054 | 106 | 0.415 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 158,473 | 1.585 | 20 | 50 | fits | 149,154 | 204 | 0.437 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 245,347 | 2.453 | 20 | 50 | fits | 87,270 | 179 | 0.395 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 331,191 | 3.312 | 20 | 20 | fits | 85,910 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 826,591 | 8.266 | 20 | 20 | fits | 73,553 | 24 | 0.673 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
