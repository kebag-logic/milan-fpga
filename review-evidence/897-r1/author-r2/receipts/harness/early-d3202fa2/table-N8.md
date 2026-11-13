### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 45 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.acmp.if0` (notice-burst-0) | 13.095 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-0.held.adp.if1` (notice-burst-0) | 11.546 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-burst-0.held.aecp.if1` (notice-burst-0) | 12.893 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.maap.if0` (notice-burst-0) | 9.233 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-burst-0.held.srp.if1` (notice-burst-0) | 7.386 | fits | 31 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.36.0.if0` (notice-burst-0) | 32.734 (33.240) | fits | 0 events | 40 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-burst-0 | 780 | 0 | 171,541 (1.715) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-burst-0 | 1.709 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.005 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.992 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.288 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.558 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.848 | 62 | 32 | 0 | within |
| notice-burst-0 | 7.958 | 62 | 32 | 0 | within |
| notice-burst-0 | 11.713 | 62 | 32 | 0 | within |
| notice-burst-0 | 17.167 | 62 | 32 | 0 | within |
| notice-burst-0 | 20.637 | 62 | 32 | 0 | within |
| notice-burst-0 | 20.921 | 62 | 32 | 0 | within |
| notice-burst-0 | 21.211 | 62 | 32 | 0 | within |
| notice-burst-0 | 21.476 | 62 | 32 | 0 | within |
| notice-burst-0 | 22.787 | 62 | 32 | 0 | within |
| notice-burst-0 | 23.066 | 62 | 32 | 0 | within |
| notice-burst-0 | 23.356 | 62 | 32 | 0 | within |
| notice-burst-0 | 23.626 | 62 | 32 | 0 | within |
| notice-burst-0 | 24.689 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.049 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.367 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.651 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.968 | 62 | 32 | 0 | within |
| notice-burst-0 | 24.958 | 62 | 32 | 0 | within |
| notice-burst-0 | 25.247 | 62 | 32 | 0 | within |
| notice-burst-0 | 25.505 | 62 | 32 | 0 | within |
| notice-burst-0 | 26.807 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.301 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.632 | 62 | 32 | 0 | within |
| notice-burst-0 | 27.077 | 62 | 32 | 0 | within |
| notice-burst-0 | 27.366 | 62 | 32 | 0 | within |
| notice-burst-0 | 27.624 | 62 | 32 | 0 | within |
| notice-burst-0 | 28.632 | 62 | 32 | 0 | within |
| notice-burst-0 | 28.904 | 62 | 32 | 0 | within |
| notice-burst-0 | 29.192 | 62 | 32 | 0 | within |
| notice-burst-0 | 29.447 | 62 | 32 | 0 | within |
| notice-burst-0 | 30.706 | 62 | 32 | 0 | within |
| notice-burst-0 | 30.963 | 62 | 32 | 0 | within |
| notice-burst-0 | 31.206 | 62 | 32 | 0 | within |
| notice-burst-0 | 31.493 | 62 | 32 | 0 | within |
| notice-burst-0 | 32.734 | 62 | 32 | 0 | within |

Latest: 32.734 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-burst-0 | 311 | 88,444 (0.884) | 40,148 (0.401) |

Longest pass that carries a step: 88,444 CPU cycles (0.884 ms), notice-burst-0; longest step: 40,148 (0.401 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 170,937 | 1.709 | 62 | 66 | fits | 161,939 | 411 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 200,454 | 2.005 | 62 | 66 | fits | 161,939 | 411 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 499,218 | 4.992 | 62 | 66 | fits | 126,284 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 528,819 | 5.288 | 62 | 66 | fits | 126,284 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 555,795 | 5.558 | 62 | 66 | fits | 126,284 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 584,799 | 5.848 | 62 | 66 | fits | 126,284 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 795,809 | 7.958 | 62 | 66 | fits | 39,443 | 101 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 1,171,337 | 11.713 | 62 | 66 | fits | 42,298 | 102 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 1,716,680 | 17.167 | 62 | 66 | fits | 40,225 | 100 | 0.309 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 2,063,690 | 20.637 | 62 | 66 | fits | 124,526 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 2,092,076 | 20.921 | 62 | 66 | fits | 124,526 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 2,121,069 | 21.211 | 62 | 66 | fits | 124,526 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 2,147,603 | 21.476 | 62 | 66 | fits | 124,526 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 2,278,743 | 22.787 | 62 | 66 | fits | 123,494 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 2,306,595 | 23.066 | 62 | 66 | fits | 123,494 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 2,335,638 | 23.356 | 62 | 66 | fits | 123,494 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 2,362,551 | 23.626 | 62 | 66 | fits | 123,494 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 2,468,917 | 24.689 | 62 | 66 | fits | 121,275 | 401 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 304,874 | 3.049 | 62 | 66 | fits | 131,786 | 402 | 0.024 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 336,692 | 3.367 | 62 | 66 | fits | 131,786 | 402 | 0.024 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 365,076 | 3.651 | 62 | 66 | fits | 131,786 | 402 | 0.024 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 396,833 | 3.968 | 62 | 66 | fits | 131,786 | 402 | 0.024 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 2,495,831 | 24.958 | 62 | 66 | fits | 121,275 | 401 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 2,524,651 | 25.247 | 62 | 66 | fits | 121,275 | 401 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 2,550,492 | 25.505 | 62 | 66 | fits | 121,275 | 401 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 2,680,656 | 26.807 | 62 | 66 | fits | 120,822 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 230,143 | 2.301 | 62 | 66 | fits | 161,939 | 411 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 263,220 | 2.632 | 62 | 66 | fits | 161,939 | 411 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 2,707,695 | 27.077 | 62 | 66 | fits | 120,822 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 2,736,578 | 27.366 | 62 | 66 | fits | 120,822 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,762,369 | 27.624 | 62 | 66 | fits | 120,822 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,863,193 | 28.632 | 62 | 66 | fits | 120,064 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,890,410 | 28.904 | 62 | 66 | fits | 120,064 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,919,225 | 29.192 | 62 | 66 | fits | 120,064 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 2,944,728 | 29.447 | 62 | 66 | fits | 120,064 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 3,070,569 | 30.706 | 62 | 66 | fits | 116,985 | 399 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 3,096,297 | 30.963 | 62 | 66 | fits | 116,985 | 399 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 3,120,600 | 31.206 | 62 | 66 | fits | 116,985 | 399 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 3,149,348 | 31.493 | 62 | 66 | fits | 116,985 | 399 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 3,273,373 | 32.734 | 62 | 66 | fits | 37,406 | 102 | 0.158 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 1,154,618 | 11.546 | 20 | 200 | fits | 171,541 | 114 | 0.544 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,309,478 | 13.095 | 20 | 20 | fits | 134,903 | 95 | 0.516 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 1,289,274 | 12.893 | 20 | 24 | fits | 134,903 | 95 | 0.516 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 923,334 | 9.233 | 20 | 50 | fits | 162,756 | 149 | 0.558 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 738,553 | 7.386 | 20 | 20 | fits | 170,639 | 67 | 0.453 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
