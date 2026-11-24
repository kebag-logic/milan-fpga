### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.acmp.if0` (notice-retried-6) | 4.251 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.adp.if0` (notice-retried-3) | 1.633 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.aecp.if0` (notice-retried-6) | 4.048 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.maap.if0` (notice-retried-6) | 3.856 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.srp.if0` (notice-retried-7) | 8.345 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-7.mrpdu.periodic.if0` (notice-retried-7) | 0.952 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-3.stream_info.if0` (notice-retried-3) | 8.292 (8.409) | fits | 2 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 2027 | 0 | 152,850 (1.528) | fits |
| notice-retried-1 | 2028 | 0 | 152,772 (1.528) | fits |
| notice-retried-2 | 2028 | 0 | 153,114 (1.531) | fits |
| notice-retried-3 | 2027 | 0 | 155,174 (1.552) | fits |
| notice-retried-4 | 2026 | 0 | 155,023 (1.550) | fits |
| notice-retried-5 | 2026 | 0 | 152,568 (1.526) | fits |
| notice-retried-6 | 2025 | 0 | 152,616 (1.526) | fits |
| notice-retried-7 | 2024 | 0 | 154,163 (1.542) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 7.910 | 20 | 16 | 2 | within |
| notice-retried-1 | 8.038 | 20 | 16 | 1 | within |
| notice-retried-2 | 7.964 | 20 | 16 | 1 | within |
| notice-retried-3 | 8.292 | 20 | 16 | 2 | within |
| notice-retried-4 | 7.960 | 20 | 16 | 1 | within |
| notice-retried-5 | 7.989 | 20 | 16 | 1 | within |
| notice-retried-6 | 8.169 | 20 | 16 | 1 | within |
| notice-retried-7 | 7.910 | 20 | 16 | 2 | within |

Latest: 8.292 ms, notice-retried-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 402 | 94,460 (0.945) | 77,979 (0.780) |
| notice-retried-1 | 402 | 94,460 (0.945) | 77,979 (0.780) |
| notice-retried-2 | 402 | 94,460 (0.945) | 77,979 (0.780) |
| notice-retried-3 | 402 | 94,460 (0.945) | 77,979 (0.780) |
| notice-retried-4 | 402 | 94,460 (0.945) | 77,979 (0.780) |
| notice-retried-5 | 402 | 94,460 (0.945) | 77,979 (0.780) |
| notice-retried-6 | 402 | 94,460 (0.945) | 77,979 (0.780) |
| notice-retried-7 | 402 | 94,460 (0.945) | 77,979 (0.780) |

Longest pass that carries a step: 94,460 CPU cycles (0.945 ms), notice-retried-0; longest step: 77,979 (0.780 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 790,976 | 7.910 | 20 | 24 | fits | 25,055 | 52 | 0.462 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 153,287 | 1.533 | 20 | 200 | fits | 148,050 | 274 | 0.209 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 406,506 | 4.065 | 20 | 20 | fits | 120,637 | 105 | 0.474 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 386,302 | 3.863 | 20 | 24 | fits | 120,637 | 105 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 367,031 | 3.670 | 20 | 50 | fits | 120,637 | 105 | 0.474 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 820,260 | 8.203 | 20 | 20 | fits | 51,045 | 26 | 0.696 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 95,060 | 0.951 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 803,830 | 8.038 | 20 | 24 | fits | 25,055 | 52 | 0.462 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 154,323 | 1.543 | 20 | 200 | fits | 146,478 | 271 | 0.210 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 407,504 | 4.075 | 20 | 20 | fits | 120,677 | 105 | 0.475 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 387,300 | 3.873 | 20 | 24 | fits | 120,677 | 105 | 0.475 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 368,029 | 3.680 | 20 | 50 | fits | 120,677 | 105 | 0.475 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 821,170 | 8.212 | 20 | 20 | fits | 51,045 | 26 | 0.696 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 77,678 | 0.777 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 796,383 | 7.964 | 20 | 24 | fits | 25,062 | 52 | 0.462 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 125,945 | 1.259 | 20 | 200 | fits | 118,937 | 154 | 0.168 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 404,870 | 4.049 | 20 | 20 | fits | 127,765 | 115 | 0.453 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 384,666 | 3.847 | 20 | 24 | fits | 127,765 | 115 | 0.453 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 365,395 | 3.654 | 20 | 50 | fits | 127,765 | 115 | 0.453 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 818,662 | 8.187 | 20 | 20 | fits | 51,398 | 26 | 0.703 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 74,958 | 0.750 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 829,184 | 8.292 | 20 | 24 | fits | 24,994 | 52 | 0.460 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 163,342 | 1.633 | 20 | 200 | fits | 149,536 | 291 | 0.227 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 409,420 | 4.094 | 20 | 20 | fits | 113,239 | 84 | 0.467 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 389,216 | 3.892 | 20 | 24 | fits | 113,239 | 84 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 103,599 | 1.036 | 20 | 50 | fits | 149,536 | 291 | 0.227 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 822,363 | 8.224 | 20 | 20 | fits | 56,437 | 39 | 0.714 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 79,046 | 0.790 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 795,996 | 7.960 | 20 | 24 | fits | 24,994 | 52 | 0.460 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 143,342 | 1.433 | 20 | 200 | fits | 144,118 | 273 | 0.208 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 419,311 | 4.193 | 20 | 20 | fits | 128,907 | 115 | 0.468 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 399,107 | 3.991 | 20 | 24 | fits | 128,907 | 115 | 0.468 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 379,836 | 3.798 | 20 | 50 | fits | 128,907 | 115 | 0.468 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 814,014 | 8.140 | 20 | 20 | fits | 51,032 | 26 | 0.694 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 78,808 | 0.788 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 798,934 | 7.989 | 20 | 24 | fits | 25,055 | 52 | 0.462 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 152,195 | 1.522 | 20 | 200 | fits | 148,294 | 274 | 0.209 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 421,024 | 4.210 | 20 | 20 | fits | 124,902 | 118 | 0.487 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 400,820 | 4.008 | 20 | 24 | fits | 124,902 | 118 | 0.487 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 381,549 | 3.815 | 20 | 50 | fits | 124,902 | 118 | 0.487 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 815,472 | 8.155 | 20 | 20 | fits | 51,032 | 26 | 0.694 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 80,266 | 0.803 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 816,909 | 8.169 | 20 | 24 | fits | 25,055 | 52 | 0.462 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 156,017 | 1.560 | 20 | 200 | fits | 146,164 | 270 | 0.206 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 425,053 | 4.251 | 20 | 20 | fits | 125,014 | 118 | 0.490 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 404,849 | 4.048 | 20 | 24 | fits | 125,014 | 118 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 385,578 | 3.856 | 20 | 50 | fits | 125,014 | 118 | 0.490 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 819,577 | 8.196 | 20 | 20 | fits | 51,045 | 26 | 0.696 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 84,330 | 0.843 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 790,976 | 7.910 | 20 | 24 | fits | 25,055 | 52 | 0.462 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 145,898 | 1.459 | 20 | 200 | fits | 145,998 | 276 | 0.210 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 421,048 | 4.210 | 20 | 20 | fits | 128,805 | 115 | 0.467 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 400,844 | 4.008 | 20 | 24 | fits | 128,805 | 115 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 381,573 | 3.816 | 20 | 50 | fits | 128,805 | 115 | 0.467 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 834,539 | 8.345 | 20 | 20 | fits | 51,029 | 26 | 0.696 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 95,183 | 0.952 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
