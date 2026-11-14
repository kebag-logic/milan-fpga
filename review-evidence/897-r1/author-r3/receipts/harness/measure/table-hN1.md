### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 35 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.acmp.if0` (notice-burst-0) | 4.537 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.adp.if0` (notice-burst-0) | 1.481 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.aecp.if0` (notice-burst-0) | 4.335 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.maap.if0` (notice-burst-0) | 4.142 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.srp.if0` (notice-every-0) | 9.572 | fits | 31 srp | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.207 | fits | 0 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.9.0.if0` (notice-burst-0) | 18.383 (18.590) | fits | 1 events | 24 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1633 | 0 | 153,388 (1.534) | fits |
| notice-burst-0 | 1147 | 0 | 149,729 (1.497) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.148 | 130 | 16 | 2 | within |
| notice-every-0 | 8.349 | 130 | 16 | 2 | within |
| notice-every-0 | 1.977 | 130 | 16 | 2 | within |
| notice-every-0 | 2.186 | 130 | 16 | 2 | within |
| notice-every-0 | 4.078 | 130 | 16 | 2 | within |
| notice-every-0 | 4.283 | 130 | 16 | 2 | within |
| notice-every-0 | 6.006 | 130 | 16 | 2 | within |
| notice-every-0 | 6.211 | 130 | 16 | 2 | within |
| notice-every-0 | 10.015 | 130 | 16 | 2 | within |
| notice-every-0 | 10.183 | 130 | 16 | 2 | within |
| notice-every-0 | 12.036 | 130 | 16 | 2 | within |
| notice-every-0 | 12.235 | 130 | 16 | 2 | within |
| notice-burst-0 | 8.460 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.155 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.371 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.208 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.327 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.535 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.204 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.409 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.391 | 130 | 16 | 1 | within |
| notice-burst-0 | 18.183 | 130 | 16 | 1 | within |
| notice-burst-0 | 18.383 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.715 | 130 | 16 | 1 | within |

Latest: 18.383 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 97,586 (0.976) | 75,859 (0.759) |
| notice-burst-0 | 317 | 136,614 (1.366) | 77,696 (0.777) |

Longest pass that carries a step: 136,614 CPU cycles (1.366 ms), notice-burst-0; longest step: 77,696 (0.777 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 814,750 | 8.148 | 130 | 134 | fits | 47,196 | 102 | 0.303 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 834,859 | 8.349 | 130 | 134 | fits | 47,196 | 102 | 0.303 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 197,659 | 1.977 | 130 | 134 | fits | 50,435 | 105 | 0.341 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 218,624 | 2.186 | 130 | 134 | fits | 50,435 | 105 | 0.341 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 407,803 | 4.078 | 130 | 134 | fits | 48,358 | 102 | 0.328 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 428,318 | 4.283 | 130 | 134 | fits | 48,358 | 102 | 0.328 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 600,585 | 6.006 | 130 | 134 | fits | 46,942 | 105 | 0.288 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 621,051 | 6.211 | 130 | 134 | fits | 46,942 | 105 | 0.288 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 1,001,521 | 10.015 | 130 | 134 | fits | 40,927 | 101 | 0.260 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 1,018,315 | 10.183 | 130 | 134 | fits | 40,927 | 101 | 0.260 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 1,203,597 | 12.036 | 130 | 134 | fits | 45,831 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 1,223,530 | 12.235 | 130 | 134 | fits | 45,831 | 103 | 0.273 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 131,718 | 1.317 | 20 | 200 | fits | 129,710 | 160 | 0.384 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 417,977 | 4.180 | 20 | 20 | fits | 131,722 | 128 | 0.461 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 397,773 | 3.978 | 20 | 24 | fits | 131,722 | 128 | 0.461 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 378,502 | 3.785 | 20 | 50 | fits | 131,722 | 128 | 0.461 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 957,248 | 9.572 | 20 | 20 | fits | 39,564 | 25 | 0.808 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 120,655 | 1.207 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 845,973 | 8.460 | 130 | 134 | fits | 26,816 | 52 | 0.431 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,515,486 | 15.155 | 130 | 134 | fits | 49,967 | 103 | 0.378 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,537,070 | 15.371 | 130 | 134 | fits | 49,967 | 103 | 0.378 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,620,845 | 16.208 | 130 | 134 | fits | 44,428 | 102 | 0.289 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 232,729 | 2.327 | 130 | 134 | fits | 62,396 | 111 | 0.349 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 253,515 | 2.535 | 130 | 134 | fits | 62,396 | 111 | 0.349 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 320,399 | 3.204 | 130 | 134 | fits | 136,614 | 112 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 340,911 | 3.409 | 130 | 134 | fits | 136,614 | 112 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,639,098 | 16.391 | 130 | 134 | fits | 44,428 | 102 | 0.289 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,818,318 | 18.183 | 130 | 134 | fits | 42,872 | 102 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,838,341 | 18.383 | 130 | 134 | fits | 42,872 | 102 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 671,474 | 6.715 | 130 | 134 | fits | 28,402 | 52 | 0.424 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 148,120 | 1.481 | 20 | 200 | fits | 149,729 | 273 | 0.361 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 453,666 | 4.537 | 20 | 20 | fits | 123,342 | 125 | 0.464 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 433,462 | 4.335 | 20 | 24 | fits | 123,342 | 125 | 0.464 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 414,191 | 4.142 | 20 | 50 | fits | 123,342 | 125 | 0.464 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 910,221 | 9.102 | 20 | 20 | fits | 79,207 | 34 | 0.595 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
