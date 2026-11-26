### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.acmp.if0` (notice-retried-5) | 3.924 | fits | 10 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.adp.if0` (notice-retried-7) | 1.604 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.aecp.if0` (notice-retried-5) | 3.722 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.maap.if0` (notice-retried-5) | 3.529 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.srp.if0` (notice-retried-7) | 8.678 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-0.mrpdu.periodic.if0` (notice-retried-0) | 0.883 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-3.stream_info.if0` (notice-retried-3) | 8.184 (8.290) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 2262 | 0 | 148,847 (1.488) | fits |
| notice-retried-1 | 2264 | 0 | 147,221 (1.472) | fits |
| notice-retried-2 | 2263 | 0 | 147,118 (1.471) | fits |
| notice-retried-3 | 2261 | 0 | 148,805 (1.488) | fits |
| notice-retried-4 | 2262 | 0 | 148,879 (1.489) | fits |
| notice-retried-5 | 2261 | 0 | 147,131 (1.471) | fits |
| notice-retried-6 | 2261 | 0 | 149,481 (1.495) | fits |
| notice-retried-7 | 2260 | 0 | 147,586 (1.476) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 8.041 | 20 | 16 | 2 | within |
| notice-retried-1 | 8.124 | 20 | 16 | 2 | within |
| notice-retried-2 | 8.126 | 20 | 16 | 3 | within |
| notice-retried-3 | 8.184 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.136 | 20 | 16 | 2 | within |
| notice-retried-5 | 8.159 | 20 | 16 | 2 | within |
| notice-retried-6 | 8.159 | 20 | 16 | 2 | within |
| notice-retried-7 | 8.131 | 20 | 16 | 2 | within |

Latest: 8.184 ms, notice-retried-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 405 | 93,013 (0.930) | 78,139 (0.781) |
| notice-retried-1 | 405 | 93,013 (0.930) | 78,139 (0.781) |
| notice-retried-2 | 405 | 93,013 (0.930) | 78,139 (0.781) |
| notice-retried-3 | 405 | 93,013 (0.930) | 78,139 (0.781) |
| notice-retried-4 | 405 | 93,013 (0.930) | 78,139 (0.781) |
| notice-retried-5 | 405 | 93,013 (0.930) | 78,139 (0.781) |
| notice-retried-6 | 405 | 93,013 (0.930) | 78,139 (0.781) |
| notice-retried-7 | 405 | 93,013 (0.930) | 78,139 (0.781) |

Longest pass that carries a step: 93,013 CPU cycles (0.930 ms), notice-retried-0; longest step: 78,139 (0.781 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 804,125 | 8.041 | 20 | 24 | fits | 23,918 | 52 | 0.448 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 125,166 | 1.252 | 20 | 200 | fits | 120,073 | 157 | 0.168 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 369,851 | 3.699 | 20 | 20 | fits | 94,040 | 92 | 0.488 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 349,647 | 3.496 | 20 | 24 | fits | 94,040 | 92 | 0.488 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 330,376 | 3.304 | 20 | 50 | fits | 94,040 | 92 | 0.488 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 861,879 | 8.619 | 20 | 20 | fits | 55,478 | 26 | 0.757 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 88,272 | 0.883 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 812,390 | 8.124 | 20 | 24 | fits | 24,002 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 151,331 | 1.513 | 20 | 200 | fits | 144,659 | 272 | 0.213 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 375,263 | 3.753 | 20 | 20 | fits | 96,979 | 96 | 0.500 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 355,059 | 3.551 | 20 | 24 | fits | 96,979 | 96 | 0.500 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 335,788 | 3.358 | 20 | 50 | fits | 96,979 | 96 | 0.500 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 864,711 | 8.647 | 20 | 20 | fits | 55,478 | 26 | 0.757 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 74,513 | 0.745 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 812,552 | 8.126 | 20 | 24 | fits | 23,926 | 52 | 0.445 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 152,064 | 1.521 | 20 | 200 | fits | 144,179 | 271 | 0.207 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 375,893 | 3.759 | 20 | 20 | fits | 96,979 | 96 | 0.500 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 355,689 | 3.557 | 20 | 24 | fits | 96,979 | 96 | 0.500 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 336,418 | 3.364 | 20 | 50 | fits | 96,979 | 96 | 0.500 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 865,497 | 8.655 | 20 | 20 | fits | 55,465 | 26 | 0.757 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 75,127 | 0.751 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 818,396 | 8.184 | 20 | 24 | fits | 23,811 | 52 | 0.440 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 125,424 | 1.254 | 20 | 200 | fits | 120,145 | 157 | 0.170 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 388,166 | 3.882 | 20 | 20 | fits | 104,739 | 120 | 0.485 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 367,962 | 3.680 | 20 | 24 | fits | 104,739 | 120 | 0.485 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 348,691 | 3.487 | 20 | 50 | fits | 104,739 | 120 | 0.485 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 859,307 | 8.593 | 20 | 20 | fits | 55,694 | 28 | 0.753 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 74,924 | 0.749 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 813,603 | 8.136 | 20 | 24 | fits | 23,572 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 152,306 | 1.523 | 20 | 200 | fits | 147,534 | 279 | 0.204 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 391,268 | 3.913 | 20 | 20 | fits | 98,606 | 96 | 0.519 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 371,064 | 3.711 | 20 | 24 | fits | 98,606 | 96 | 0.519 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 351,793 | 3.518 | 20 | 50 | fits | 98,606 | 96 | 0.519 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 862,023 | 8.620 | 20 | 20 | fits | 55,696 | 28 | 0.753 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 77,531 | 0.775 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 815,949 | 8.159 | 20 | 24 | fits | 23,803 | 52 | 0.442 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 151,745 | 1.517 | 20 | 200 | fits | 144,060 | 271 | 0.206 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 392,389 | 3.924 | 20 | 20 | fits | 102,107 | 109 | 0.523 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 372,185 | 3.722 | 20 | 24 | fits | 102,107 | 109 | 0.523 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 352,914 | 3.529 | 20 | 50 | fits | 102,107 | 109 | 0.523 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 862,732 | 8.627 | 20 | 20 | fits | 55,483 | 26 | 0.757 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 79,274 | 0.793 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 815,949 | 8.159 | 20 | 24 | fits | 23,803 | 52 | 0.442 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 40,250 | 0.403 | 20 | 200 | fits | 32,852 | 60 | 0.086 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 369,707 | 3.697 | 20 | 20 | fits | 94,427 | 94 | 0.490 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 349,503 | 3.495 | 20 | 24 | fits | 94,427 | 94 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 330,232 | 3.302 | 20 | 50 | fits | 94,427 | 94 | 0.490 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 858,517 | 8.585 | 20 | 20 | fits | 55,499 | 26 | 0.757 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 76,939 | 0.769 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 813,117 | 8.131 | 20 | 24 | fits | 24,589 | 52 | 0.476 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 160,364 | 1.604 | 20 | 200 | fits | 146,407 | 290 | 0.227 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 377,761 | 3.778 | 20 | 20 | fits | 90,079 | 75 | 0.497 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 357,557 | 3.576 | 20 | 24 | fits | 90,079 | 75 | 0.497 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 100,621 | 1.006 | 20 | 50 | fits | 146,407 | 290 | 0.227 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 867,844 | 8.678 | 20 | 20 | fits | 55,214 | 26 | 0.754 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 70,721 | 0.707 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
