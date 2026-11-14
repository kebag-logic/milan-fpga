### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 35 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.acmp.if0` (notice-burst-0) | 4.746 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.adp.if0` (notice-burst-0) | 1.789 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.aecp.if0` (notice-burst-0) | 4.544 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 4.181 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.srp.if0` (notice-every-0) | 9.982 | fits | 31 srp | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.310 | fits | 0 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.9.0.if0` (notice-burst-0) | 19.341 (19.606) | fits | 0 events | 24 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1583 | 0 | 153,136 (1.531) | fits |
| notice-burst-0 | 1081 | 0 | 156,376 (1.564) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 7.994 | 130 | 16 | 2 | within |
| notice-every-0 | 8.201 | 130 | 16 | 2 | within |
| notice-every-0 | 1.849 | 130 | 16 | 2 | within |
| notice-every-0 | 2.065 | 130 | 16 | 2 | within |
| notice-every-0 | 4.023 | 130 | 16 | 2 | within |
| notice-every-0 | 4.233 | 130 | 16 | 2 | within |
| notice-every-0 | 5.801 | 130 | 16 | 2 | within |
| notice-every-0 | 6.012 | 130 | 16 | 2 | within |
| notice-every-0 | 9.911 | 130 | 16 | 2 | within |
| notice-every-0 | 10.091 | 130 | 16 | 2 | within |
| notice-every-0 | 11.809 | 130 | 16 | 2 | within |
| notice-every-0 | 12.017 | 130 | 16 | 2 | within |
| notice-burst-0 | 8.373 | 130 | 16 | 0 | within |
| notice-burst-0 | 15.161 | 130 | 16 | 0 | within |
| notice-burst-0 | 15.384 | 130 | 16 | 0 | within |
| notice-burst-0 | 17.096 | 130 | 16 | 0 | within |
| notice-burst-0 | 3.523 | 130 | 16 | 0 | within |
| notice-burst-0 | 3.739 | 130 | 16 | 0 | within |
| notice-burst-0 | 4.185 | 130 | 16 | 0 | within |
| notice-burst-0 | 4.397 | 130 | 16 | 0 | within |
| notice-burst-0 | 17.289 | 130 | 16 | 0 | within |
| notice-burst-0 | 19.133 | 130 | 16 | 0 | within |
| notice-burst-0 | 19.341 | 130 | 16 | 0 | within |
| notice-burst-0 | 5.036 | 130 | 16 | 0 | within |

Latest: 19.341 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 100,808 (1.008) | 76,101 (0.761) |
| notice-burst-0 | 317 | 111,450 (1.115) | 77,814 (0.778) |

Longest pass that carries a step: 111,450 CPU cycles (1.115 ms), notice-burst-0; longest step: 77,814 (0.778 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 799,385 | 7.994 | 130 | 134 | fits | 48,074 | 102 | 0.294 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 820,100 | 8.201 | 130 | 134 | fits | 48,074 | 102 | 0.294 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 184,913 | 1.849 | 130 | 134 | fits | 51,262 | 105 | 0.338 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 206,531 | 2.065 | 130 | 134 | fits | 51,262 | 105 | 0.338 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 402,295 | 4.023 | 130 | 134 | fits | 49,129 | 102 | 0.318 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 423,309 | 4.233 | 130 | 134 | fits | 49,129 | 102 | 0.318 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 580,100 | 5.801 | 130 | 134 | fits | 48,033 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 601,178 | 6.012 | 130 | 134 | fits | 48,033 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 991,066 | 9.911 | 130 | 134 | fits | 42,717 | 101 | 0.281 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 1,009,089 | 10.091 | 130 | 134 | fits | 42,717 | 101 | 0.281 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 1,180,911 | 11.809 | 130 | 134 | fits | 46,990 | 103 | 0.268 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 1,201,659 | 12.017 | 130 | 134 | fits | 46,990 | 103 | 0.268 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 171,761 | 1.718 | 20 | 200 | fits | 150,477 | 267 | 0.385 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 457,546 | 4.575 | 20 | 20 | fits | 151,229 | 132 | 0.474 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 437,342 | 4.373 | 20 | 24 | fits | 151,229 | 132 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 418,071 | 4.181 | 20 | 50 | fits | 151,229 | 132 | 0.474 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 998,224 | 9.982 | 20 | 20 | fits | 47,807 | 23 | 0.726 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 131,033 | 1.310 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 837,256 | 8.373 | 130 | 134 | fits | 27,570 | 52 | 0.439 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,516,093 | 15.161 | 130 | 134 | fits | 51,279 | 103 | 0.385 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,538,390 | 15.384 | 130 | 134 | fits | 51,279 | 103 | 0.385 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,709,590 | 17.096 | 130 | 134 | fits | 45,730 | 102 | 0.295 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 352,259 | 3.523 | 130 | 134 | fits | 49,862 | 102 | 0.337 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 373,910 | 3.739 | 130 | 134 | fits | 49,862 | 102 | 0.337 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 418,479 | 4.185 | 130 | 134 | fits | 66,351 | 118 | 0.369 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 439,666 | 4.397 | 130 | 134 | fits | 66,351 | 118 | 0.369 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,728,859 | 17.289 | 130 | 134 | fits | 45,730 | 102 | 0.295 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,913,315 | 19.133 | 130 | 134 | fits | 44,653 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,934,146 | 19.341 | 130 | 134 | fits | 44,653 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 503,605 | 5.036 | 130 | 134 | fits | 42,456 | 61 | 0.410 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 178,941 | 1.789 | 20 | 200 | fits | 148,083 | 274 | 0.395 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 474,639 | 4.746 | 20 | 20 | fits | 132,020 | 112 | 0.489 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 454,435 | 4.544 | 20 | 24 | fits | 132,020 | 112 | 0.489 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 119,198 | 1.192 | 20 | 50 | fits | 148,083 | 274 | 0.395 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 931,125 | 9.311 | 20 | 20 | fits | 79,148 | 34 | 0.580 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
