### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 12 paths and 7 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.149 (64.490) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.998 (65.338) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 3.094 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 63.085 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 3.137 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 4.408 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.593 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 63.120 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 3.120 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 3.116 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 4.392 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 7.981 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 65.716 | 23 | 175,951 (1.760) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 175,951 CPU cycles (1.760 ms), backlog-owed.
Over the windows that released their whole load only: 175,951 (1.760 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-owed | 308 | 0 | 175,951 (1.760) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-owed | 277 | 25,321 (0.253) | 3,141 (0.031) |

Longest pass that carries a step: 25,321 CPU cycles (0.253 ms), backlog-owed; longest step: 3,141 (0.031 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,414,943 | 64.149 | 20 | 20 | MISS ceiling | 21,314 | 13 | 0.451 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,436,261 | 64.363 | 20 | 20 | MISS ceiling | 21,375 | 13 | 0.434 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,457,373 | 64.574 | 20 | 20 | MISS ceiling | 21,188 | 13 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,478,567 | 64.786 | 20 | 20 | MISS ceiling | 21,270 | 13 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,499,786 | 64.998 | 20 | 20 | MISS ceiling | 21,282 | 13 | 0.451 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 313,689 | 3.137 | 20 | 200 | fits | 153,737 | 252 | 0.239 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 440,813 | 4.408 | 20 | 200 | fits | 127,740 | 55 | 0.681 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 309,367 | 3.094 | 20 | 20 | fits | 153,737 | 252 | 0.239 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,308,474 | 63.085 | 20 | 20 | MISS ceiling | 95,597 | 42 | 0.519 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 159,270 | 1.593 | 20 | 24 | fits | 149,793 | 107 | 0.423 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,311,960 | 63.120 | 20 | 24 | MISS ceiling | 95,597 | 42 | 0.519 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 311,951 | 3.120 | 20 | 50 | fits | 153,737 | 252 | 0.239 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 311,555 | 3.116 | 20 | 50 | fits | 153,737 | 252 | 0.239 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 439,229 | 4.392 | 20 | 20 | fits | 127,740 | 55 | 0.681 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 798,052 | 7.981 | 20 | 20 | fits | 99,731 | 36 | 0.706 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
