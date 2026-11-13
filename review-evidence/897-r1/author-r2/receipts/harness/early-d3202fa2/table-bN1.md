### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 17 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.acmp.if0` (notice-burst-0) | 10.965 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.adp.if0` (notice-burst-0) | 9.645 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.aecp.if0` (notice-burst-0) | 11.093 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.maap.if0` (notice-burst-0) | 9.048 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.srp.if0` (notice-burst-0) | 6.878 | fits | 31 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.6.0.if0` (notice-burst-0) | 12.064 (12.268) | fits | 1 events | 12 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-burst-0 | 835 | 0 | 153,657 (1.537) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-burst-0 | 8.992 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.199 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.402 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.604 | 22 | 16 | 1 | within |
| notice-burst-0 | 11.858 | 22 | 16 | 1 | within |
| notice-burst-0 | 12.064 | 22 | 16 | 1 | within |
| notice-burst-0 | 3.336 | 22 | 16 | 1 | within |
| notice-burst-0 | 3.549 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.792 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.962 | 22 | 16 | 1 | within |
| notice-burst-0 | 10.163 | 22 | 16 | 1 | within |
| notice-burst-0 | 4.172 | 22 | 16 | 1 | within |

Latest: 12.064 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-burst-0 | 316 | 103,210 (1.032) | 77,755 (0.778) |

Longest pass that carries a step: 103,210 CPU cycles (1.032 ms), notice-burst-0; longest step: 77,755 (0.778 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 899,245 | 8.992 | 22 | 26 | fits | 146,089 | 352 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 919,893 | 9.199 | 22 | 26 | fits | 146,089 | 352 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 940,191 | 9.402 | 22 | 26 | fits | 146,089 | 352 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 960,375 | 9.604 | 22 | 26 | fits | 146,089 | 352 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 1,185,784 | 11.858 | 22 | 26 | fits | 47,670 | 103 | 0.345 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 1,206,389 | 12.064 | 22 | 26 | fits | 47,670 | 103 | 0.345 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 333,575 | 3.336 | 22 | 26 | fits | 49,736 | 102 | 0.313 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 354,939 | 3.549 | 22 | 26 | fits | 49,736 | 102 | 0.313 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 979,196 | 9.792 | 22 | 26 | fits | 146,089 | 352 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 996,229 | 9.962 | 22 | 26 | fits | 146,089 | 352 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,016,284 | 10.163 | 22 | 26 | fits | 146,089 | 352 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 417,215 | 4.172 | 22 | 26 | fits | 41,188 | 62 | 0.380 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 964,508 | 9.645 | 20 | 200 | fits | 147,316 | 183 | 0.551 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,096,523 | 10.965 | 20 | 20 | fits | 152,283 | 118 | 0.516 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 1,109,263 | 11.093 | 20 | 24 | fits | 32,944 | 23 | 0.710 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 904,765 | 9.048 | 20 | 50 | fits | 147,316 | 183 | 0.551 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 687,754 | 6.878 | 20 | 20 | fits | 142,187 | 74 | 0.542 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
