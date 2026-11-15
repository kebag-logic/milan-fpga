### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 18 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.acmp.if0` (notice-every-0) | 5.362 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.adp.if0` (notice-every-0) | 1.484 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.aecp.if0` (notice-every-0) | 4.224 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 4.031 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.srp.if0` (notice-every-0) | 9.993 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.267 | fits | 0 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-every-0.notices.29.36.0.if0` (notice-every-0) | 8.646 (8.783) | fits | 2 events | 12 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1637 | 0 | 156,596 (1.566) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.170 | 130 | 16 | 2 | within |
| notice-every-0 | 4.379 | 130 | 16 | 2 | within |
| notice-every-0 | 6.123 | 130 | 16 | 2 | within |
| notice-every-0 | 6.335 | 130 | 16 | 2 | within |
| notice-every-0 | 8.236 | 130 | 16 | 2 | within |
| notice-every-0 | 8.443 | 130 | 16 | 2 | within |
| notice-every-0 | 2.203 | 130 | 16 | 2 | within |
| notice-every-0 | 2.420 | 130 | 16 | 2 | within |
| notice-every-0 | 4.567 | 130 | 16 | 2 | within |
| notice-every-0 | 6.511 | 130 | 16 | 2 | within |
| notice-every-0 | 2.628 | 130 | 16 | 2 | within |
| notice-every-0 | 8.646 | 130 | 16 | 2 | within |

Latest: 8.646 ms, notice-every-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 101,105 (1.011) | 76,094 (0.761) |

Longest pass that carries a step: 101,105 CPU cycles (1.011 ms), notice-every-0; longest step: 76,094 (0.761 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 417,004 | 4.170 | 130 | 134 | fits | 69,540 | 160 | 0.283 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 437,919 | 4.379 | 130 | 134 | fits | 69,540 | 160 | 0.283 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 612,311 | 6.123 | 130 | 134 | fits | 66,215 | 153 | 0.258 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 633,452 | 6.335 | 130 | 134 | fits | 66,215 | 153 | 0.258 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 823,552 | 8.236 | 130 | 134 | fits | 66,629 | 153 | 0.249 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 844,263 | 8.443 | 130 | 134 | fits | 66,629 | 153 | 0.249 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 220,321 | 2.203 | 130 | 134 | fits | 71,880 | 153 | 0.291 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 242,017 | 2.420 | 130 | 134 | fits | 71,880 | 153 | 0.291 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 456,690 | 4.567 | 130 | 134 | fits | 69,540 | 160 | 0.283 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 651,124 | 6.511 | 130 | 134 | fits | 66,215 | 153 | 0.258 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 262,834 | 2.628 | 130 | 134 | fits | 71,880 | 153 | 0.291 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 864,622 | 8.646 | 130 | 134 | fits | 66,629 | 153 | 0.249 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 148,358 | 1.484 | 20 | 200 | fits | 150,153 | 252 | 0.365 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 536,155 | 5.362 | 20 | 20 | fits | 93,575 | 39 | 0.744 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 422,376 | 4.224 | 20 | 24 | fits | 147,987 | 147 | 0.496 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 403,105 | 4.031 | 20 | 50 | fits | 147,987 | 147 | 0.496 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 999,263 | 9.993 | 20 | 20 | fits | 48,492 | 23 | 0.755 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 126,690 | 1.267 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
