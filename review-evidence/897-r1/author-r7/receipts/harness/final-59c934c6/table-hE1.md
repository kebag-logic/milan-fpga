### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 18 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.acmp.if0` (notice-every-0) | 4.275 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.adp.if0` (notice-every-0) | 1.740 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.aecp.if0` (notice-every-0) | 4.073 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 1.143 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.srp.if0` (notice-every-0) | 11.262 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 0.980 | fits | 0 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-every-0.notices.29.36.0.if0` (notice-every-0) | 12.378 (12.462) | fits | 2 events | 12 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1548 | 0 | 154,715 (1.547) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 2.348 | 140 | 16 | 2 | within |
| notice-every-0 | 2.551 | 140 | 16 | 2 | within |
| notice-every-0 | 4.161 | 140 | 16 | 2 | within |
| notice-every-0 | 4.364 | 140 | 16 | 2 | within |
| notice-every-0 | 6.329 | 140 | 16 | 2 | within |
| notice-every-0 | 6.532 | 140 | 16 | 2 | within |
| notice-every-0 | 8.337 | 140 | 16 | 2 | within |
| notice-every-0 | 8.535 | 140 | 16 | 2 | within |
| notice-every-0 | 10.261 | 140 | 16 | 2 | within |
| notice-every-0 | 10.429 | 140 | 16 | 2 | within |
| notice-every-0 | 12.181 | 140 | 16 | 2 | within |
| notice-every-0 | 12.378 | 140 | 16 | 2 | within |

Latest: 12.378 ms, notice-every-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 98,897 (0.989) | 76,375 (0.764) |

Longest pass that carries a step: 98,897 CPU cycles (0.989 ms), notice-every-0; longest step: 76,375 (0.764 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 234,793 | 2.348 | 140 | 144 | fits | 49,679 | 103 | 0.317 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 255,137 | 2.551 | 140 | 144 | fits | 49,679 | 103 | 0.317 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 416,094 | 4.161 | 140 | 144 | fits | 48,953 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 436,388 | 4.364 | 140 | 144 | fits | 48,953 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 632,928 | 6.329 | 140 | 144 | fits | 48,004 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 653,160 | 6.532 | 140 | 144 | fits | 48,004 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 833,716 | 8.337 | 140 | 144 | fits | 46,650 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 853,487 | 8.535 | 140 | 144 | fits | 46,650 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 1,026,131 | 10.261 | 140 | 144 | fits | 40,966 | 101 | 0.218 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 1,042,902 | 10.429 | 140 | 144 | fits | 40,966 | 101 | 0.218 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 1,218,131 | 12.181 | 140 | 144 | fits | 45,022 | 104 | 0.181 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 1,237,800 | 12.378 | 140 | 144 | fits | 45,022 | 104 | 0.181 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 174,013 | 1.740 | 20 | 200 | fits | 151,699 | 290 | 0.340 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 427,516 | 4.275 | 20 | 20 | fits | 119,056 | 86 | 0.494 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 407,312 | 4.073 | 20 | 24 | fits | 119,056 | 86 | 0.494 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 114,270 | 1.143 | 20 | 50 | fits | 151,699 | 290 | 0.340 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,126,198 | 11.262 | 20 | 20 | fits | 43,683 | 25 | 0.835 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 98,013 | 0.980 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
