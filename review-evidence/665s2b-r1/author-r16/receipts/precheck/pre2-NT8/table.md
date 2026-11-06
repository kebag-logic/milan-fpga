### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 48 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.acmp.if0` (notice-retried-5) | 9.840 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-retried-3.held.adp.if1` (notice-retried-3) | 7.524 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-retried-1.held.aecp.if1` (notice-retried-1) | 16.428 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.maap.if0` (notice-retried-5) | 5.724 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-retried-4.held.srp.if1` (notice-retried-4) | 17.106 | fits | 31 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-4.stream_info.if0` (notice-retried-4) | 12.990 (13.180) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 943 | 0 | 187,038 (1.870) | fits |
| notice-retried-1 | 941 | 0 | 185,781 (1.858) | fits |
| notice-retried-2 | 942 | 0 | 185,812 (1.858) | fits |
| notice-retried-3 | 941 | 0 | 188,980 (1.890) | fits |
| notice-retried-4 | 944 | 0 | 168,502 (1.685) | fits |
| notice-retried-5 | 943 | 0 | 185,747 (1.857) | fits |
| notice-retried-6 | 944 | 0 | 185,781 (1.858) | fits |
| notice-retried-7 | 942 | 0 | 187,088 (1.871) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 12.755 | 20 | 32 | 1 | within |
| notice-retried-1 | 12.752 | 20 | 32 | 1 | within |
| notice-retried-2 | 12.752 | 20 | 32 | 1 | within |
| notice-retried-3 | 12.540 | 20 | 32 | 1 | within |
| notice-retried-4 | 12.990 | 20 | 32 | 1 | within |
| notice-retried-5 | 12.571 | 20 | 32 | 1 | within |
| notice-retried-6 | 12.990 | 20 | 32 | 1 | within |
| notice-retried-7 | 12.989 | 20 | 32 | 1 | within |

Latest: 12.990 ms, notice-retried-4.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 304 | 60,000 (0.600) | 36,274 (0.363) |
| notice-retried-1 | 304 | 60,000 (0.600) | 36,274 (0.363) |
| notice-retried-2 | 304 | 64,381 (0.644) | 36,274 (0.363) |
| notice-retried-3 | 304 | 60,000 (0.600) | 36,274 (0.363) |
| notice-retried-4 | 304 | 60,000 (0.600) | 36,274 (0.363) |
| notice-retried-5 | 304 | 60,000 (0.600) | 36,274 (0.363) |
| notice-retried-6 | 304 | 60,000 (0.600) | 36,274 (0.363) |
| notice-retried-7 | 304 | 60,000 (0.600) | 36,274 (0.363) |

Longest pass that carries a step: 64,381 CPU cycles (0.644 ms), notice-retried-2; longest step: 36,274 (0.363 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 1,275,460 | 12.755 | 20 | 24 | fits | 75,433 | 181 | 0.124 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if1` | 703,627 | 7.036 | 20 | 200 | fits | 127,673 | 63 | 0.677 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 916,659 | 9.167 | 20 | 20 | fits | 105,651 | 46 | 0.746 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if1` | 1,576,285 | 15.763 | 20 | 24 | fits | 73,513 | 37 | 0.730 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 516,211 | 5.162 | 20 | 50 | fits | 116,433 | 97 | 0.572 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if1` | 1,683,156 | 16.832 | 18 | 18 | fits | 41,804 | 28 | 0.742 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 1,275,236 | 12.752 | 20 | 24 | fits | 75,389 | 181 | 0.123 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if1` | 627,907 | 6.279 | 20 | 200 | fits | 149,360 | 103 | 0.636 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 970,612 | 9.706 | 20 | 20 | fits | 105,772 | 46 | 0.747 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if1` | 1,642,753 | 16.428 | 20 | 24 | fits | 73,598 | 37 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 568,164 | 5.682 | 20 | 50 | fits | 149,360 | 103 | 0.636 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if1` | 1,655,220 | 16.552 | 18 | 18 | fits | 53,763 | 26 | 0.728 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 1,275,227 | 12.752 | 20 | 24 | fits | 75,389 | 181 | 0.123 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if1` | 625,104 | 6.251 | 20 | 200 | fits | 149,032 | 101 | 0.636 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 953,940 | 9.539 | 20 | 20 | fits | 105,665 | 46 | 0.747 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if1` | 1,625,432 | 16.254 | 20 | 24 | fits | 73,568 | 37 | 0.731 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 565,361 | 5.654 | 20 | 50 | fits | 149,032 | 101 | 0.636 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if1` | 1,677,715 | 16.777 | 18 | 18 | fits | 39,756 | 21 | 0.770 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 1,253,970 | 12.540 | 20 | 24 | fits | 75,389 | 181 | 0.123 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if1` | 752,358 | 7.524 | 20 | 200 | fits | 129,404 | 56 | 0.701 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 929,970 | 9.300 | 20 | 20 | fits | 103,784 | 52 | 0.722 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if1` | 1,590,860 | 15.909 | 20 | 24 | fits | 73,513 | 37 | 0.730 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 563,211 | 5.632 | 20 | 50 | fits | 150,067 | 104 | 0.622 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if1` | 1,695,146 | 16.951 | 18 | 18 | fits | 39,477 | 21 | 0.761 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 1,298,987 | 12.990 | 20 | 24 | fits | 75,624 | 181 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if1` | 561,377 | 5.614 | 20 | 200 | fits | 168,502 | 102 | 0.684 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 914,482 | 9.145 | 20 | 20 | fits | 105,223 | 45 | 0.747 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if1` | 1,578,100 | 15.781 | 20 | 24 | fits | 73,551 | 38 | 0.729 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 501,634 | 5.016 | 20 | 50 | fits | 168,502 | 102 | 0.684 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if1` | 1,710,621 | 17.106 | 18 | 18 | fits | 55,824 | 30 | 0.757 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 1,257,136 | 12.571 | 20 | 24 | fits | 82,333 | 187 | 0.134 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if1` | 632,151 | 6.322 | 20 | 200 | fits | 149,248 | 102 | 0.635 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 983,998 | 9.840 | 20 | 20 | fits | 105,404 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if1` | 1,610,526 | 16.105 | 20 | 24 | fits | 73,433 | 38 | 0.728 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 572,408 | 5.724 | 20 | 50 | fits | 149,248 | 102 | 0.635 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if1` | 1,675,558 | 16.756 | 18 | 18 | fits | 52,398 | 25 | 0.707 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 1,298,987 | 12.990 | 20 | 24 | fits | 75,624 | 181 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if1` | 622,521 | 6.225 | 20 | 200 | fits | 149,235 | 102 | 0.635 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 975,022 | 9.750 | 20 | 20 | fits | 105,359 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if1` | 1,635,325 | 16.353 | 20 | 24 | fits | 73,506 | 38 | 0.728 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 562,778 | 5.628 | 20 | 50 | fits | 149,235 | 102 | 0.635 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if1` | 1,647,959 | 16.480 | 18 | 18 | fits | 53,930 | 27 | 0.723 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 1,298,943 | 12.989 | 20 | 24 | fits | 75,580 | 181 | 0.124 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if1` | 707,217 | 7.072 | 20 | 200 | fits | 129,719 | 57 | 0.701 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 932,031 | 9.320 | 20 | 20 | fits | 105,585 | 51 | 0.740 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if1` | 1,578,706 | 15.787 | 20 | 24 | fits | 73,513 | 37 | 0.730 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 517,755 | 5.178 | 20 | 50 | fits | 147,884 | 111 | 0.594 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if1` | 1,689,900 | 16.899 | 18 | 18 | fits | 39,785 | 22 | 0.757 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
