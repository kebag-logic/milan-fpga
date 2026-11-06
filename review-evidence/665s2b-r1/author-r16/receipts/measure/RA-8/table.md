### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 6 paths and 8 of 48 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-1.held.acmp.if0` (notice-retried-1) | 9.655 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-retried-6.held.adp.if1` (notice-retried-6) | 7.470 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-retried-1.held.aecp.if1` (notice-retried-1) | 16.220 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.maap.if0` (notice-retried-5) | 5.660 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-retried-0.held.srp.if1` (notice-retried-0) | 16.783 | fits | 31 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-7.stream_info.if0` (notice-retried-7) | 30.876 (31.279) | MISS ceiling | 1 events | 8 | 8 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 941 | 0 | 185,957 (1.860) | fits |
| notice-retried-1 | 939 | 0 | 186,209 (1.862) | fits |
| notice-retried-2 | 941 | 0 | 186,238 (1.862) | fits |
| notice-retried-3 | 940 | 0 | 188,627 (1.886) | fits |
| notice-retried-4 | 940 | 0 | 167,392 (1.674) | fits |
| notice-retried-5 | 938 | 0 | 185,701 (1.857) | fits |
| notice-retried-6 | 939 | 0 | 186,853 (1.869) | fits |
| notice-retried-7 | 938 | 0 | 185,717 (1.857) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 30.872 | 20 | 32 | 1 | OVER |
| notice-retried-1 | 30.872 | 20 | 32 | 1 | OVER |
| notice-retried-2 | 30.839 | 20 | 32 | 1 | OVER |
| notice-retried-3 | 30.872 | 20 | 32 | 1 | OVER |
| notice-retried-4 | 30.661 | 20 | 32 | 1 | OVER |
| notice-retried-5 | 30.871 | 20 | 32 | 1 | OVER |
| notice-retried-6 | 30.843 | 20 | 32 | 1 | OVER |
| notice-retried-7 | 30.876 | 20 | 32 | 1 | OVER |

Latest: 30.876 ms, notice-retried-7.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 304 | 60,148 (0.601) | 36,138 (0.361) |
| notice-retried-1 | 304 | 60,148 (0.601) | 36,138 (0.361) |
| notice-retried-2 | 304 | 64,241 (0.642) | 36,138 (0.361) |
| notice-retried-3 | 304 | 60,148 (0.601) | 36,138 (0.361) |
| notice-retried-4 | 304 | 60,148 (0.601) | 36,138 (0.361) |
| notice-retried-5 | 304 | 60,148 (0.601) | 36,138 (0.361) |
| notice-retried-6 | 304 | 60,148 (0.601) | 36,138 (0.361) |
| notice-retried-7 | 304 | 60,148 (0.601) | 36,138 (0.361) |

Longest pass that carries a step: 64,241 CPU cycles (0.642 ms), notice-retried-2; longest step: 36,138 (0.361 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 3,087,163 | 30.872 | 20 | 24 | MISS ceiling | 75,793 | 181 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if1` | 593,866 | 5.939 | 20 | 200 | fits | 115,203 | 94 | 0.588 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 931,098 | 9.311 | 20 | 20 | fits | 104,977 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if1` | 1,573,555 | 15.736 | 20 | 24 | fits | 73,099 | 37 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 534,123 | 5.341 | 20 | 50 | fits | 115,203 | 94 | 0.588 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if1` | 1,678,339 | 16.783 | 18 | 18 | fits | 39,773 | 21 | 0.773 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 3,087,155 | 30.872 | 20 | 24 | MISS ceiling | 75,793 | 181 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if1` | 624,862 | 6.249 | 20 | 200 | fits | 148,781 | 103 | 0.636 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 965,541 | 9.655 | 20 | 20 | fits | 105,039 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if1` | 1,621,960 | 16.220 | 20 | 24 | fits | 73,307 | 37 | 0.733 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 565,119 | 5.651 | 20 | 50 | fits | 148,781 | 103 | 0.636 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if1` | 1,634,321 | 16.343 | 18 | 18 | fits | 53,657 | 26 | 0.728 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 3,083,949 | 30.839 | 20 | 24 | MISS ceiling | 75,793 | 181 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if1` | 615,604 | 6.156 | 20 | 200 | fits | 148,476 | 101 | 0.636 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 943,114 | 9.431 | 20 | 20 | fits | 105,115 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if1` | 1,567,001 | 15.670 | 20 | 24 | fits | 73,099 | 37 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 555,861 | 5.559 | 20 | 50 | fits | 148,476 | 101 | 0.636 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if1` | 1,671,850 | 16.718 | 18 | 18 | fits | 39,840 | 21 | 0.773 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 3,087,227 | 30.872 | 20 | 24 | MISS ceiling | 75,793 | 181 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if1` | 741,688 | 7.417 | 20 | 200 | fits | 129,187 | 56 | 0.702 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 918,573 | 9.186 | 20 | 20 | fits | 103,023 | 51 | 0.722 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if1` | 1,572,952 | 15.730 | 20 | 24 | fits | 73,135 | 37 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 552,758 | 5.528 | 20 | 50 | fits | 149,470 | 104 | 0.622 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if1` | 1,637,712 | 16.377 | 18 | 18 | fits | 52,361 | 24 | 0.721 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 3,066,077 | 30.661 | 20 | 24 | MISS ceiling | 76,365 | 181 | 0.134 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if1` | 551,371 | 5.514 | 20 | 200 | fits | 167,392 | 101 | 0.682 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 890,960 | 8.910 | 20 | 20 | fits | 104,986 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if1` | 1,545,491 | 15.455 | 20 | 24 | fits | 73,135 | 37 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 491,628 | 4.916 | 20 | 50 | fits | 167,392 | 101 | 0.682 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if1` | 1,662,435 | 16.624 | 18 | 18 | fits | 52,182 | 24 | 0.719 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 3,087,127 | 30.871 | 20 | 24 | MISS ceiling | 75,793 | 181 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if1` | 625,743 | 6.257 | 20 | 200 | fits | 148,456 | 101 | 0.636 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 964,586 | 9.646 | 20 | 20 | fits | 105,000 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if1` | 1,619,230 | 16.192 | 20 | 24 | fits | 73,135 | 37 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 566,000 | 5.660 | 20 | 50 | fits | 148,456 | 101 | 0.636 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if1` | 1,631,591 | 16.316 | 18 | 18 | fits | 53,657 | 26 | 0.728 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 3,084,283 | 30.843 | 20 | 24 | MISS ceiling | 76,221 | 181 | 0.133 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if1` | 746,994 | 7.470 | 20 | 200 | fits | 129,173 | 56 | 0.702 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 958,200 | 9.582 | 20 | 20 | fits | 104,972 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if1` | 1,613,350 | 16.134 | 20 | 24 | fits | 73,135 | 37 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 558,078 | 5.581 | 20 | 50 | fits | 149,535 | 104 | 0.623 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if1` | 1,625,776 | 16.258 | 18 | 18 | fits | 53,722 | 26 | 0.728 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 3,087,563 | 30.876 | 20 | 24 | MISS ceiling | 75,793 | 181 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if1` | 590,695 | 5.907 | 20 | 200 | fits | 146,713 | 107 | 0.614 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 929,554 | 9.296 | 20 | 20 | fits | 104,972 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if1` | 1,571,962 | 15.720 | 20 | 24 | fits | 73,099 | 37 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 530,952 | 5.310 | 20 | 50 | fits | 146,713 | 107 | 0.614 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if1` | 1,676,719 | 16.767 | 18 | 18 | fits | 39,773 | 21 | 0.773 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
