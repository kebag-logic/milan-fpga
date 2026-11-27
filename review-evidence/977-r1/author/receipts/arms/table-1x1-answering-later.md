### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.acmp.if0` (notice-retried-4) | 3.791 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.adp.if0` (notice-retried-4) | 1.576 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.aecp.if0` (notice-retried-4) | 3.589 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.maap.if0` (notice-retried-4) | 3.397 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.srp.if0` (notice-retried-7) | 8.232 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-1.mrpdu.periodic.if0` (notice-retried-1) | 0.719 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-6.stream_info.if0` (notice-retried-6) | 8.246 (8.343) | fits | 2 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 2178 | 0 | 147,874 (1.479) | fits |
| notice-retried-1 | 2178 | 0 | 146,984 (1.470) | fits |
| notice-retried-2 | 2178 | 0 | 147,153 (1.472) | fits |
| notice-retried-3 | 2177 | 0 | 150,225 (1.502) | fits |
| notice-retried-4 | 2175 | 0 | 150,259 (1.503) | fits |
| notice-retried-5 | 2176 | 0 | 147,435 (1.474) | fits |
| notice-retried-6 | 2176 | 0 | 147,172 (1.472) | fits |
| notice-retried-7 | 2176 | 0 | 147,172 (1.472) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 8.041 | 20 | 16 | 2 | within |
| notice-retried-1 | 8.155 | 20 | 16 | 1 | within |
| notice-retried-2 | 8.155 | 20 | 16 | 1 | within |
| notice-retried-3 | 8.227 | 20 | 16 | 2 | within |
| notice-retried-4 | 8.053 | 20 | 16 | 1 | within |
| notice-retried-5 | 8.053 | 20 | 16 | 1 | within |
| notice-retried-6 | 8.246 | 20 | 16 | 2 | within |
| notice-retried-7 | 8.145 | 20 | 16 | 1 | within |

Latest: 8.246 ms, notice-retried-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 403 | 92,844 (0.928) | 78,077 (0.781) |
| notice-retried-1 | 403 | 92,844 (0.928) | 78,077 (0.781) |
| notice-retried-2 | 403 | 92,844 (0.928) | 78,077 (0.781) |
| notice-retried-3 | 403 | 92,844 (0.928) | 78,077 (0.781) |
| notice-retried-4 | 403 | 92,844 (0.928) | 78,077 (0.781) |
| notice-retried-5 | 403 | 92,844 (0.928) | 78,077 (0.781) |
| notice-retried-6 | 403 | 92,844 (0.928) | 78,077 (0.781) |
| notice-retried-7 | 403 | 92,844 (0.928) | 78,077 (0.781) |

Longest pass that carries a step: 92,844 CPU cycles (0.928 ms), notice-retried-0; longest step: 78,077 (0.781 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 804,075 | 8.041 | 20 | 24 | fits | 22,568 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 154,786 | 1.548 | 20 | 200 | fits | 147,874 | 269 | 0.326 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 361,885 | 3.619 | 20 | 20 | fits | 80,413 | 83 | 0.488 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 341,681 | 3.417 | 20 | 24 | fits | 80,413 | 83 | 0.488 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 322,410 | 3.224 | 20 | 50 | fits | 80,413 | 83 | 0.488 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 820,560 | 8.206 | 20 | 20 | fits | 89,676 | 92 | 0.651 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 46,972 | 0.470 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 815,501 | 8.155 | 20 | 24 | fits | 22,568 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 148,995 | 1.490 | 20 | 200 | fits | 143,460 | 264 | 0.325 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 361,724 | 3.617 | 20 | 20 | fits | 86,013 | 90 | 0.471 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 341,520 | 3.415 | 20 | 24 | fits | 86,013 | 90 | 0.471 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 322,249 | 3.222 | 20 | 50 | fits | 86,013 | 90 | 0.471 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 820,007 | 8.200 | 20 | 20 | fits | 89,676 | 92 | 0.651 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 71,928 | 0.719 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 815,501 | 8.155 | 20 | 24 | fits | 22,568 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 146,288 | 1.463 | 20 | 200 | fits | 146,062 | 269 | 0.311 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 359,160 | 3.592 | 20 | 20 | fits | 85,987 | 90 | 0.471 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 338,956 | 3.390 | 20 | 24 | fits | 85,987 | 90 | 0.471 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 319,685 | 3.197 | 20 | 50 | fits | 85,987 | 90 | 0.471 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 817,742 | 8.177 | 20 | 20 | fits | 78,903 | 79 | 0.678 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 52,066 | 0.521 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 822,668 | 8.227 | 20 | 24 | fits | 22,329 | 52 | 0.424 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 127,088 | 1.271 | 20 | 200 | fits | 123,202 | 160 | 0.245 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 371,644 | 3.716 | 20 | 20 | fits | 85,889 | 104 | 0.484 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 351,440 | 3.514 | 20 | 24 | fits | 85,889 | 104 | 0.484 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 332,169 | 3.322 | 20 | 50 | fits | 85,889 | 104 | 0.484 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 813,283 | 8.133 | 20 | 20 | fits | 67,261 | 66 | 0.692 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 53,949 | 0.539 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 805,323 | 8.053 | 20 | 24 | fits | 22,329 | 52 | 0.424 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 157,639 | 1.576 | 20 | 200 | fits | 147,859 | 270 | 0.325 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 379,146 | 3.791 | 20 | 20 | fits | 81,073 | 83 | 0.505 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 358,942 | 3.589 | 20 | 24 | fits | 81,073 | 83 | 0.505 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 339,671 | 3.397 | 20 | 50 | fits | 81,073 | 83 | 0.505 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 821,100 | 8.211 | 20 | 20 | fits | 67,286 | 66 | 0.692 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 51,044 | 0.510 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 805,323 | 8.053 | 20 | 24 | fits | 22,329 | 52 | 0.424 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 125,599 | 1.256 | 20 | 200 | fits | 123,299 | 160 | 0.246 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 372,738 | 3.727 | 20 | 20 | fits | 89,588 | 103 | 0.488 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 352,534 | 3.525 | 20 | 24 | fits | 89,588 | 103 | 0.488 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 333,263 | 3.333 | 20 | 50 | fits | 89,588 | 103 | 0.488 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 814,369 | 8.144 | 20 | 20 | fits | 67,275 | 66 | 0.692 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 43,949 | 0.439 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 824,599 | 8.246 | 20 | 24 | fits | 22,329 | 52 | 0.424 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 126,786 | 1.268 | 20 | 200 | fits | 121,816 | 157 | 0.253 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 358,215 | 3.582 | 20 | 20 | fits | 86,269 | 92 | 0.471 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 338,011 | 3.380 | 20 | 24 | fits | 86,269 | 92 | 0.471 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 318,740 | 3.187 | 20 | 50 | fits | 86,269 | 92 | 0.471 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 815,180 | 8.152 | 20 | 20 | fits | 78,635 | 79 | 0.669 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 55,218 | 0.552 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 814,525 | 8.145 | 20 | 24 | fits | 22,764 | 52 | 0.442 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 151,055 | 1.511 | 20 | 200 | fits | 143,696 | 266 | 0.348 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 363,982 | 3.640 | 20 | 20 | fits | 86,023 | 90 | 0.475 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 343,778 | 3.438 | 20 | 24 | fits | 86,023 | 90 | 0.475 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 324,507 | 3.245 | 20 | 50 | fits | 86,023 | 90 | 0.475 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 823,227 | 8.232 | 20 | 20 | fits | 78,632 | 79 | 0.669 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 52,064 | 0.521 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
