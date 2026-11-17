Original file: <scratch>/r4/budget/r4-lt1/results/table.md
Original size: 12728 bytes
Original sha256: 323172d61503b6afd803c7b4748e717ee888b4ce2dac7923698f9ae16c274bd4

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.acmp.if0` (notice-retried-5) | 4.291 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.adp.if0` (notice-retried-3) | 1.660 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.aecp.if0` (notice-retried-5) | 4.089 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.maap.if0` (notice-retried-5) | 3.896 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.srp.if0` (notice-retried-4) | 10.399 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-1.mrpdu.periodic.if0` (notice-retried-1) | 1.065 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-6.stream_info.if0` (notice-retried-6) | 8.392 (8.487) | fits | 2 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1566 | 0 | 153,541 (1.535) | fits |
| notice-retried-1 | 1565 | 0 | 153,767 (1.538) | fits |
| notice-retried-2 | 1566 | 0 | 153,441 (1.534) | fits |
| notice-retried-3 | 1562 | 0 | 155,980 (1.560) | fits |
| notice-retried-4 | 1562 | 0 | 157,365 (1.574) | fits |
| notice-retried-5 | 1563 | 0 | 153,898 (1.539) | fits |
| notice-retried-6 | 1563 | 0 | 153,889 (1.539) | fits |
| notice-retried-7 | 1562 | 0 | 155,437 (1.554) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 8.107 | 20 | 16 | 2 | within |
| notice-retried-1 | 8.088 | 20 | 16 | 1 | within |
| notice-retried-2 | 8.285 | 20 | 16 | 2 | within |
| notice-retried-3 | 8.383 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.151 | 20 | 16 | 1 | within |
| notice-retried-5 | 8.169 | 20 | 16 | 2 | within |
| notice-retried-6 | 8.392 | 20 | 16 | 2 | within |
| notice-retried-7 | 8.061 | 20 | 16 | 2 | within |

Latest: 8.392 ms, notice-retried-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 307 | 92,531 (0.925) | 75,894 (0.759) |
| notice-retried-1 | 307 | 92,757 (0.928) | 75,972 (0.760) |
| notice-retried-2 | 307 | 92,531 (0.925) | 75,894 (0.759) |
| notice-retried-3 | 307 | 95,623 (0.956) | 75,945 (0.759) |
| notice-retried-4 | 307 | 102,588 (1.026) | 75,991 (0.760) |
| notice-retried-5 | 307 | 91,865 (0.919) | 75,790 (0.758) |
| notice-retried-6 | 307 | 91,865 (0.919) | 75,790 (0.758) |
| notice-retried-7 | 307 | 91,865 (0.919) | 75,790 (0.758) |

Longest pass that carries a step: 102,588 CPU cycles (1.026 ms), notice-retried-4; longest step: 75,991 (0.760 ms), notice-retried-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 810,689 | 8.107 | 20 | 24 | fits | 27,458 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 132,304 | 1.323 | 20 | 200 | fits | 122,540 | 154 | 0.335 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 411,228 | 4.112 | 20 | 20 | fits | 124,918 | 108 | 0.506 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 391,024 | 3.910 | 20 | 24 | fits | 124,918 | 108 | 0.506 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 371,753 | 3.718 | 20 | 50 | fits | 124,918 | 108 | 0.506 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 1,024,524 | 10.245 | 20 | 20 | fits | 37,346 | 18 | 0.804 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 80,239 | 0.802 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 808,762 | 8.088 | 20 | 24 | fits | 27,458 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 129,016 | 1.290 | 20 | 200 | fits | 126,728 | 163 | 0.315 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 404,916 | 4.049 | 20 | 20 | fits | 124,180 | 122 | 0.495 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 384,712 | 3.847 | 20 | 24 | fits | 124,180 | 122 | 0.495 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 365,441 | 3.654 | 20 | 50 | fits | 124,180 | 122 | 0.495 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 1,018,454 | 10.185 | 20 | 20 | fits | 37,346 | 18 | 0.804 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 106,527 | 1.065 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 828,549 | 8.285 | 20 | 24 | fits | 27,458 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 132,914 | 1.329 | 20 | 200 | fits | 122,540 | 154 | 0.335 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 407,830 | 4.078 | 20 | 20 | fits | 124,969 | 108 | 0.507 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 387,626 | 3.876 | 20 | 24 | fits | 124,969 | 108 | 0.507 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 368,355 | 3.684 | 20 | 50 | fits | 124,969 | 108 | 0.507 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 1,021,239 | 10.212 | 20 | 20 | fits | 37,346 | 18 | 0.804 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 92,405 | 0.924 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 838,288 | 8.383 | 20 | 24 | fits | 27,339 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 165,973 | 1.660 | 20 | 200 | fits | 150,865 | 270 | 0.353 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 419,065 | 4.191 | 20 | 20 | fits | 119,556 | 101 | 0.518 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 398,861 | 3.989 | 20 | 24 | fits | 119,556 | 101 | 0.518 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 379,590 | 3.796 | 20 | 50 | fits | 119,556 | 101 | 0.518 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 1,032,746 | 10.327 | 20 | 20 | fits | 37,346 | 18 | 0.804 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 85,918 | 0.859 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 815,086 | 8.151 | 20 | 24 | fits | 27,359 | 52 | 0.439 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 160,109 | 1.601 | 20 | 200 | fits | 151,582 | 271 | 0.338 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 426,675 | 4.267 | 20 | 20 | fits | 119,845 | 101 | 0.522 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 406,471 | 4.065 | 20 | 24 | fits | 119,845 | 101 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 387,200 | 3.872 | 20 | 50 | fits | 119,845 | 101 | 0.522 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 1,039,873 | 10.399 | 20 | 20 | fits | 37,425 | 18 | 0.805 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 92,908 | 0.929 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 816,911 | 8.169 | 20 | 24 | fits | 27,319 | 52 | 0.431 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 162,309 | 1.623 | 20 | 200 | fits | 147,931 | 263 | 0.344 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 429,079 | 4.291 | 20 | 20 | fits | 123,507 | 114 | 0.522 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 408,875 | 4.089 | 20 | 24 | fits | 123,507 | 114 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 389,604 | 3.896 | 20 | 50 | fits | 123,507 | 114 | 0.522 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 1,025,361 | 10.254 | 20 | 20 | fits | 37,346 | 18 | 0.804 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 81,822 | 0.818 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 839,176 | 8.392 | 20 | 24 | fits | 27,529 | 52 | 0.439 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 159,037 | 1.590 | 20 | 200 | fits | 147,816 | 263 | 0.342 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 425,729 | 4.257 | 20 | 20 | fits | 123,507 | 114 | 0.522 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 405,525 | 4.055 | 20 | 24 | fits | 123,507 | 114 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 386,254 | 3.863 | 20 | 50 | fits | 123,507 | 114 | 0.522 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 1,022,003 | 10.220 | 20 | 20 | fits | 37,346 | 18 | 0.804 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 78,521 | 0.785 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 806,051 | 8.061 | 20 | 24 | fits | 27,319 | 52 | 0.431 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 129,617 | 1.296 | 20 | 200 | fits | 117,900 | 146 | 0.348 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 421,423 | 4.214 | 20 | 20 | fits | 125,394 | 108 | 0.511 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 401,219 | 4.012 | 20 | 24 | fits | 125,394 | 108 | 0.511 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 381,948 | 3.819 | 20 | 50 | fits | 125,394 | 108 | 0.511 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 1,034,892 | 10.349 | 20 | 20 | fits | 37,346 | 18 | 0.804 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 90,824 | 0.908 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
