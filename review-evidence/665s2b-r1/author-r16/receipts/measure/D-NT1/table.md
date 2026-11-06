### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 48 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-1.held.acmp.if0` (notice-retried-1) | 5.161 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.adp.if0` (notice-retried-3) | 3.881 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.aecp.if0` (notice-retried-5) | 9.771 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.maap.if0` (notice-retried-3) | 3.284 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-1.held.srp.if0` (notice-retried-1) | 10.415 | fits | 31 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-6.stream_info.if0` (notice-retried-6) | 13.196 (13.327) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1561 | 0 | 115,866 (1.159) | fits |
| notice-retried-1 | 1562 | 0 | 115,868 (1.159) | fits |
| notice-retried-2 | 1562 | 0 | 115,933 (1.159) | fits |
| notice-retried-3 | 1561 | 0 | 115,750 (1.157) | fits |
| notice-retried-4 | 1563 | 0 | 115,790 (1.158) | fits |
| notice-retried-5 | 1561 | 0 | 115,819 (1.158) | fits |
| notice-retried-6 | 1563 | 0 | 115,821 (1.158) | fits |
| notice-retried-7 | 1562 | 0 | 115,948 (1.159) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 12.404 | 20 | 16 | 1 | within |
| notice-retried-1 | 12.404 | 20 | 16 | 1 | within |
| notice-retried-2 | 12.317 | 20 | 16 | 1 | within |
| notice-retried-3 | 12.316 | 20 | 16 | 1 | within |
| notice-retried-4 | 13.172 | 20 | 16 | 1 | within |
| notice-retried-5 | 12.415 | 20 | 16 | 1 | within |
| notice-retried-6 | 13.196 | 20 | 16 | 1 | within |
| notice-retried-7 | 13.196 | 20 | 16 | 1 | within |

Latest: 13.196 ms, notice-retried-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 308 | 115,866 (1.159) | 76,124 (0.761) |
| notice-retried-1 | 308 | 115,868 (1.159) | 76,124 (0.761) |
| notice-retried-2 | 308 | 115,933 (1.159) | 76,124 (0.761) |
| notice-retried-3 | 308 | 115,750 (1.157) | 76,124 (0.761) |
| notice-retried-4 | 308 | 115,790 (1.158) | 76,082 (0.761) |
| notice-retried-5 | 308 | 115,819 (1.158) | 76,082 (0.761) |
| notice-retried-6 | 308 | 115,821 (1.158) | 76,082 (0.761) |
| notice-retried-7 | 308 | 115,948 (1.159) | 76,082 (0.761) |

Longest pass that carries a step: 115,948 CPU cycles (1.159 ms), notice-retried-7; longest step: 76,124 (0.761 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 1,240,435 | 12.404 | 20 | 24 | fits | 38,471 | 100 | 0.197 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 251,917 | 2.519 | 20 | 200 | fits | 66,593 | 93 | 0.565 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 512,421 | 5.124 | 20 | 20 | fits | 66,063 | 43 | 0.743 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 943,349 | 9.433 | 20 | 24 | fits | 52,585 | 36 | 0.737 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 257,503 | 2.575 | 20 | 50 | fits | 65,329 | 65 | 0.710 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 1,039,634 | 10.396 | 18 | 18 | fits | 24,870 | 20 | 0.784 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 1,240,435 | 12.404 | 20 | 24 | fits | 38,471 | 100 | 0.197 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 191,352 | 1.914 | 20 | 200 | fits | 100,231 | 102 | 0.656 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 516,117 | 5.161 | 20 | 20 | fits | 65,994 | 43 | 0.743 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 945,829 | 9.458 | 20 | 24 | fits | 52,433 | 36 | 0.736 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 261,406 | 2.614 | 20 | 50 | fits | 65,355 | 65 | 0.710 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 1,041,539 | 10.415 | 18 | 18 | fits | 24,751 | 20 | 0.781 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 1,231,651 | 12.317 | 20 | 24 | fits | 38,472 | 100 | 0.197 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 252,163 | 2.522 | 20 | 200 | fits | 66,617 | 93 | 0.566 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 512,367 | 5.124 | 20 | 20 | fits | 65,994 | 43 | 0.743 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 942,333 | 9.423 | 20 | 24 | fits | 52,294 | 36 | 0.734 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 257,656 | 2.577 | 20 | 50 | fits | 65,236 | 65 | 0.709 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 1,026,549 | 10.265 | 18 | 18 | fits | 24,785 | 21 | 0.772 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 1,231,586 | 12.316 | 20 | 24 | fits | 38,534 | 100 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 388,147 | 3.881 | 20 | 200 | fits | 86,738 | 99 | 0.628 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 509,051 | 5.091 | 20 | 20 | fits | 65,994 | 43 | 0.743 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 939,104 | 9.391 | 20 | 24 | fits | 52,413 | 36 | 0.736 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 328,404 | 3.284 | 20 | 50 | fits | 86,738 | 99 | 0.628 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 1,023,207 | 10.232 | 18 | 18 | fits | 24,785 | 21 | 0.772 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 1,317,235 | 13.172 | 20 | 24 | fits | 38,731 | 100 | 0.201 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 156,624 | 1.566 | 20 | 200 | fits | 64,318 | 95 | 0.523 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 493,381 | 4.934 | 20 | 20 | fits | 66,095 | 44 | 0.740 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 955,906 | 9.559 | 20 | 24 | fits | 52,423 | 35 | 0.739 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 237,623 | 2.376 | 20 | 50 | fits | 77,963 | 66 | 0.748 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 1,040,041 | 10.400 | 18 | 18 | fits | 24,751 | 20 | 0.781 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 1,241,474 | 12.415 | 20 | 24 | fits | 40,973 | 106 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 252,420 | 2.524 | 20 | 200 | fits | 66,696 | 95 | 0.564 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 513,966 | 5.140 | 20 | 20 | fits | 66,095 | 44 | 0.740 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 977,073 | 9.771 | 20 | 24 | fits | 52,423 | 35 | 0.739 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 259,162 | 2.592 | 20 | 50 | fits | 66,485 | 72 | 0.698 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 1,028,436 | 10.284 | 18 | 18 | fits | 24,751 | 20 | 0.781 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 1,319,580 | 13.196 | 20 | 24 | fits | 38,802 | 100 | 0.203 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 252,749 | 2.527 | 20 | 200 | fits | 66,617 | 93 | 0.566 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 514,089 | 5.141 | 20 | 20 | fits | 66,045 | 44 | 0.739 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 976,983 | 9.770 | 20 | 24 | fits | 52,423 | 35 | 0.739 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 258,308 | 2.583 | 20 | 50 | fits | 65,302 | 67 | 0.706 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 1,028,346 | 10.283 | 18 | 18 | fits | 24,751 | 20 | 0.781 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 1,319,580 | 13.196 | 20 | 24 | fits | 38,802 | 100 | 0.203 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 236,624 | 2.366 | 20 | 200 | fits | 66,617 | 93 | 0.566 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 485,263 | 4.853 | 20 | 20 | fits | 65,632 | 50 | 0.716 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 948,189 | 9.482 | 20 | 24 | fits | 52,481 | 35 | 0.739 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 327,622 | 3.276 | 20 | 50 | fits | 85,505 | 95 | 0.642 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 1,032,169 | 10.322 | 18 | 18 | fits | 24,751 | 20 | 0.781 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
