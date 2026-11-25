### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 12 paths and 7 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.100 (64.252) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.864 (65.019) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 2.986 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 63.130 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 3.029 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 4.314 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.496 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.848 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 3.012 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 4.299 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 4.299 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 7.503 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 65.503 | 24 | 174,737 (1.747) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 174,737 CPU cycles (1.747 ms), backlog-owed.
Over the windows that released their whole load only: 174,737 (1.747 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-owed | 308 | 0 | 174,737 (1.747) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-owed | 277 | 23,540 (0.235) | 2,974 (0.030) |

Longest pass that carries a step: 23,540 CPU cycles (0.235 ms), backlog-owed; longest step: 2,974 (0.030 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,409,994 | 64.100 | 20 | 20 | MISS ceiling | 19,260 | 13 | 0.451 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,429,245 | 64.292 | 20 | 20 | MISS ceiling | 19,258 | 13 | 0.412 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,448,319 | 64.483 | 20 | 20 | MISS ceiling | 19,150 | 13 | 0.438 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,467,393 | 64.674 | 20 | 20 | MISS ceiling | 19,150 | 13 | 0.438 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,486,397 | 64.864 | 20 | 20 | MISS ceiling | 19,067 | 13 | 0.429 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 302,896 | 3.029 | 20 | 200 | fits | 152,597 | 238 | 0.231 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 431,442 | 4.314 | 20 | 200 | fits | 129,162 | 72 | 0.649 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 298,574 | 2.986 | 20 | 20 | fits | 152,597 | 238 | 0.231 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,312,992 | 63.130 | 20 | 20 | MISS ceiling | 31,715 | 15 | 0.649 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 149,617 | 1.496 | 20 | 24 | fits | 146,518 | 107 | 0.438 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,284,763 | 62.848 | 20 | 24 | MISS ceiling | 92,905 | 41 | 0.528 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 301,158 | 3.012 | 20 | 50 | fits | 152,597 | 238 | 0.231 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 429,924 | 4.299 | 20 | 50 | fits | 129,162 | 72 | 0.649 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 429,858 | 4.299 | 20 | 20 | fits | 129,162 | 72 | 0.649 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 750,301 | 7.503 | 20 | 20 | fits | 61,101 | 24 | 0.693 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
