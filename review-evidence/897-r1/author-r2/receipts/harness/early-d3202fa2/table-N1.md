### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 17 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.acmp.if0` (notice-burst-0) | 10.938 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.adp.if0` (notice-burst-0) | 11.141 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.aecp.if0` (notice-burst-0) | 11.074 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.maap.if0` (notice-burst-0) | 8.962 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.srp.if0` (notice-burst-0) | 7.228 | fits | 31 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.5.1.if0` (notice-burst-0) | 11.360 (11.562) | fits | 1 events | 12 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-burst-0 | 835 | 0 | 158,769 (1.588) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-burst-0 | 8.516 | 22 | 16 | 1 | within |
| notice-burst-0 | 8.725 | 22 | 16 | 1 | within |
| notice-burst-0 | 11.151 | 22 | 16 | 1 | within |
| notice-burst-0 | 11.360 | 22 | 16 | 1 | within |
| notice-burst-0 | 2.350 | 22 | 16 | 1 | within |
| notice-burst-0 | 2.560 | 22 | 16 | 1 | within |
| notice-burst-0 | 2.757 | 22 | 16 | 1 | within |
| notice-burst-0 | 2.961 | 22 | 16 | 1 | within |
| notice-burst-0 | 8.912 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.082 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.283 | 22 | 16 | 1 | within |
| notice-burst-0 | 5.192 | 22 | 16 | 1 | within |

Latest: 11.360 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-burst-0 | 316 | 101,529 (1.015) | 77,848 (0.778) |

Longest pass that carries a step: 101,529 CPU cycles (1.015 ms), notice-burst-0; longest step: 77,848 (0.778 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 851,593 | 8.516 | 22 | 26 | fits | 105,670 | 252 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 872,455 | 8.725 | 22 | 26 | fits | 105,670 | 252 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,115,122 | 11.151 | 22 | 26 | fits | 48,663 | 103 | 0.327 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,136,004 | 11.360 | 22 | 26 | fits | 48,663 | 103 | 0.327 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 234,956 | 2.350 | 22 | 26 | fits | 88,612 | 203 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 256,010 | 2.560 | 22 | 26 | fits | 88,612 | 203 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 275,663 | 2.757 | 22 | 26 | fits | 88,612 | 203 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 296,096 | 2.961 | 22 | 26 | fits | 88,612 | 203 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 891,189 | 8.912 | 22 | 26 | fits | 105,670 | 252 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 908,153 | 9.082 | 22 | 26 | fits | 105,670 | 252 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 928,259 | 9.283 | 22 | 26 | fits | 105,670 | 252 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 519,242 | 5.192 | 22 | 26 | fits | 40,742 | 61 | 0.387 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 1,114,105 | 11.141 | 20 | 200 | fits | 158,155 | 120 | 0.537 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,093,837 | 10.938 | 20 | 20 | fits | 158,155 | 120 | 0.537 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 1,107,353 | 11.074 | 20 | 24 | fits | 33,720 | 23 | 0.723 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 896,207 | 8.962 | 20 | 50 | fits | 151,363 | 163 | 0.571 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 722,819 | 7.228 | 20 | 20 | fits | 151,541 | 63 | 0.532 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
