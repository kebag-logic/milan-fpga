### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 47 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.acmp.if0` (notice-every-0) | 6.924 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.adp.if1` (notice-every-0) | 5.807 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.aecp.if1` (notice-every-0) | 4.152 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 5.210 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.srp.if1` (notice-every-0) | 11.313 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.368 | fits | 0 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-0.mrpdu.periodic.if1` (notice-every-0) | 1.867 | fits | 0 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-every-0.notices.29.36.0.if0` (notice-every-0) | 43.114 (43.372) | fits | 1 events | 40 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1036 | 0 | 185,544 (1.855) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 6.184 | 62 | 32 | 1 | within |
| notice-every-0 | 6.480 | 62 | 32 | 1 | within |
| notice-every-0 | 2.281 | 62 | 32 | 1 | within |
| notice-every-0 | 2.585 | 62 | 32 | 1 | within |
| notice-every-0 | 8.298 | 62 | 32 | 1 | within |
| notice-every-0 | 8.597 | 62 | 32 | 1 | within |
| notice-every-0 | 4.401 | 62 | 32 | 1 | within |
| notice-every-0 | 4.708 | 62 | 32 | 1 | within |
| notice-every-0 | 10.408 | 62 | 32 | 1 | within |
| notice-every-0 | 10.706 | 62 | 32 | 1 | within |
| notice-every-0 | 12.162 | 62 | 32 | 1 | within |
| notice-every-0 | 12.461 | 62 | 32 | 1 | within |
| notice-every-0 | 14.304 | 62 | 32 | 1 | within |
| notice-every-0 | 14.603 | 62 | 32 | 1 | within |
| notice-every-0 | 16.382 | 62 | 32 | 1 | within |
| notice-every-0 | 16.681 | 62 | 32 | 1 | within |
| notice-every-0 | 18.133 | 62 | 32 | 1 | within |
| notice-every-0 | 18.433 | 62 | 32 | 1 | within |
| notice-every-0 | 20.196 | 62 | 32 | 1 | within |
| notice-every-0 | 20.496 | 62 | 32 | 1 | within |
| notice-every-0 | 24.491 | 62 | 32 | 1 | within |
| notice-every-0 | 24.792 | 62 | 32 | 1 | within |
| notice-every-0 | 26.217 | 62 | 32 | 1 | within |
| notice-every-0 | 26.515 | 62 | 32 | 1 | within |
| notice-every-0 | 28.261 | 62 | 32 | 1 | within |
| notice-every-0 | 28.558 | 62 | 32 | 1 | within |
| notice-every-0 | 30.291 | 62 | 32 | 1 | within |
| notice-every-0 | 30.591 | 62 | 32 | 1 | within |
| notice-every-0 | 32.330 | 62 | 32 | 1 | within |
| notice-every-0 | 32.630 | 62 | 32 | 1 | within |
| notice-every-0 | 34.346 | 62 | 32 | 1 | within |
| notice-every-0 | 34.647 | 62 | 32 | 1 | within |
| notice-every-0 | 36.378 | 62 | 32 | 1 | within |
| notice-every-0 | 36.675 | 62 | 32 | 1 | within |
| notice-every-0 | 38.390 | 62 | 32 | 1 | within |
| notice-every-0 | 38.686 | 62 | 32 | 1 | within |
| notice-every-0 | 40.373 | 62 | 32 | 1 | within |
| notice-every-0 | 40.621 | 62 | 32 | 1 | within |
| notice-every-0 | 42.815 | 62 | 32 | 1 | within |
| notice-every-0 | 43.114 | 62 | 32 | 1 | within |

Latest: 43.114 ms, notice-every-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 303 | 93,200 (0.932) | 48,462 (0.485) |

Longest pass that carries a step: 93,200 CPU cycles (0.932 ms), notice-every-0; longest step: 48,462 (0.485 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 618,423 | 6.184 | 62 | 66 | fits | 69,538 | 203 | 0.151 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 648,039 | 6.480 | 62 | 66 | fits | 69,538 | 203 | 0.151 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 228,137 | 2.281 | 62 | 66 | fits | 71,298 | 203 | 0.162 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 258,548 | 2.585 | 62 | 66 | fits | 71,298 | 203 | 0.162 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 829,754 | 8.298 | 62 | 66 | fits | 69,410 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 859,658 | 8.597 | 62 | 66 | fits | 69,410 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 440,143 | 4.401 | 62 | 66 | fits | 71,460 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 470,845 | 4.708 | 62 | 66 | fits | 71,460 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 1,040,816 | 10.408 | 62 | 66 | fits | 69,413 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 1,070,641 | 10.706 | 62 | 66 | fits | 69,413 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 1,216,225 | 12.162 | 62 | 66 | fits | 68,718 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 1,246,134 | 12.461 | 62 | 66 | fits | 68,718 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 1,430,433 | 14.304 | 62 | 66 | fits | 69,058 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 1,460,337 | 14.603 | 62 | 66 | fits | 69,058 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 1,638,249 | 16.382 | 62 | 66 | fits | 68,401 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 1,668,074 | 16.681 | 62 | 66 | fits | 68,401 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,813,271 | 18.133 | 62 | 66 | fits | 69,006 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,843,319 | 18.433 | 62 | 66 | fits | 69,006 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 2,019,572 | 20.196 | 62 | 66 | fits | 67,458 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 2,049,620 | 20.496 | 62 | 66 | fits | 67,458 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 2,449,125 | 24.491 | 62 | 66 | fits | 68,455 | 201 | 0.163 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 2,479,153 | 24.792 | 62 | 66 | fits | 68,455 | 201 | 0.163 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 2,621,723 | 26.217 | 62 | 66 | fits | 66,699 | 201 | 0.132 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 2,651,460 | 26.515 | 62 | 66 | fits | 66,699 | 201 | 0.132 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 2,826,060 | 28.261 | 62 | 66 | fits | 67,138 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 2,855,797 | 28.558 | 62 | 66 | fits | 67,138 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 3,029,125 | 30.291 | 62 | 66 | fits | 66,912 | 201 | 0.132 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 3,059,071 | 30.591 | 62 | 66 | fits | 66,912 | 201 | 0.132 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 3,233,030 | 32.330 | 62 | 66 | fits | 67,221 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 3,262,976 | 32.630 | 62 | 66 | fits | 67,221 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 3,434,627 | 34.346 | 62 | 66 | fits | 67,671 | 201 | 0.145 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 3,464,720 | 34.647 | 62 | 66 | fits | 67,671 | 201 | 0.145 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 3,637,822 | 36.378 | 62 | 66 | fits | 66,492 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 3,667,481 | 36.675 | 62 | 66 | fits | 66,492 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 3,838,969 | 38.390 | 62 | 66 | fits | 66,019 | 201 | 0.132 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 3,868,628 | 38.686 | 62 | 66 | fits | 66,019 | 201 | 0.132 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 4,037,301 | 40.373 | 62 | 66 | fits | 57,932 | 198 | 0.126 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 4,062,143 | 40.621 | 62 | 66 | fits | 57,932 | 198 | 0.126 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 4,281,491 | 42.815 | 62 | 66 | fits | 67,503 | 202 | 0.114 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 4,311,393 | 43.114 | 62 | 66 | fits | 67,503 | 202 | 0.114 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 580,708 | 5.807 | 20 | 200 | fits | 159,783 | 214 | 0.341 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 692,413 | 6.924 | 20 | 20 | fits | 131,973 | 60 | 0.666 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 415,234 | 4.152 | 20 | 24 | fits | 117,097 | 83 | 0.441 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 520,965 | 5.210 | 20 | 50 | fits | 159,783 | 214 | 0.341 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 1,131,275 | 11.313 | 20 | 20 | fits | 53,177 | 25 | 0.833 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 136,771 | 1.368 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 186,667 | 1.867 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
