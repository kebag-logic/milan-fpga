### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 48 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.acmp.if0` (notice-retried-6) | 9.932 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-retried-5.held.adp.if1` (notice-retried-5) | 7.627 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-retried-1.held.aecp.if1` (notice-retried-1) | 16.452 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.maap.if0` (notice-retried-6) | 5.781 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-retried-4.held.srp.if1` (notice-retried-4) | 17.101 | fits | 31 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-0.stream_info.if0` (notice-retried-0) | 12.838 (13.030) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 922 | 0 | 186,118 (1.861) | fits |
| notice-retried-1 | 921 | 0 | 186,871 (1.869) | fits |
| notice-retried-2 | 923 | 0 | 186,354 (1.864) | fits |
| notice-retried-3 | 921 | 0 | 189,156 (1.892) | fits |
| notice-retried-4 | 922 | 0 | 170,774 (1.708) | fits |
| notice-retried-5 | 922 | 0 | 186,928 (1.869) | fits |
| notice-retried-6 | 922 | 0 | 186,175 (1.862) | fits |
| notice-retried-7 | 924 | 0 | 186,243 (1.862) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 12.838 | 20 | 32 | 1 | within |
| notice-retried-1 | 12.780 | 20 | 32 | 1 | within |
| notice-retried-2 | 12.780 | 20 | 32 | 1 | within |
| notice-retried-3 | 12.780 | 20 | 32 | 1 | within |
| notice-retried-4 | 12.807 | 20 | 32 | 1 | within |
| notice-retried-5 | 12.770 | 20 | 32 | 1 | within |
| notice-retried-6 | 12.770 | 20 | 32 | 1 | within |
| notice-retried-7 | 12.809 | 20 | 32 | 1 | within |

Latest: 12.838 ms, notice-retried-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 304 | 61,292 (0.613) | 36,777 (0.368) |
| notice-retried-1 | 304 | 61,292 (0.613) | 36,777 (0.368) |
| notice-retried-2 | 304 | 65,770 (0.658) | 36,777 (0.368) |
| notice-retried-3 | 304 | 61,292 (0.613) | 36,777 (0.368) |
| notice-retried-4 | 304 | 61,292 (0.613) | 36,777 (0.368) |
| notice-retried-5 | 304 | 61,292 (0.613) | 36,777 (0.368) |
| notice-retried-6 | 304 | 61,292 (0.613) | 36,777 (0.368) |
| notice-retried-7 | 304 | 61,292 (0.613) | 36,777 (0.368) |

Longest pass that carries a step: 65,770 CPU cycles (0.658 ms), notice-retried-2; longest step: 36,777 (0.368 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 1,283,800 | 12.838 | 20 | 24 | fits | 76,893 | 181 | 0.120 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if1` | 599,392 | 5.994 | 20 | 200 | fits | 117,118 | 94 | 0.590 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 940,759 | 9.408 | 20 | 20 | fits | 106,321 | 46 | 0.742 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if1` | 1,616,096 | 16.161 | 20 | 24 | fits | 73,593 | 37 | 0.728 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 539,649 | 5.396 | 20 | 50 | fits | 117,118 | 94 | 0.590 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if1` | 1,688,539 | 16.885 | 18 | 18 | fits | 59,317 | 33 | 0.706 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 1,278,049 | 12.780 | 20 | 24 | fits | 76,740 | 181 | 0.117 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if1` | 756,645 | 7.566 | 20 | 200 | fits | 136,021 | 65 | 0.689 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 970,549 | 9.705 | 20 | 20 | fits | 106,075 | 46 | 0.740 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if1` | 1,645,227 | 16.452 | 20 | 24 | fits | 73,604 | 37 | 0.728 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 560,881 | 5.609 | 20 | 50 | fits | 151,535 | 104 | 0.620 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if1` | 1,658,277 | 16.583 | 18 | 18 | fits | 54,346 | 26 | 0.740 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 1,278,049 | 12.780 | 20 | 24 | fits | 76,740 | 181 | 0.117 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if1` | 624,265 | 6.243 | 20 | 200 | fits | 150,328 | 101 | 0.634 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 954,279 | 9.543 | 20 | 20 | fits | 106,329 | 46 | 0.743 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if1` | 1,629,261 | 16.293 | 20 | 24 | fits | 73,783 | 37 | 0.726 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 564,522 | 5.645 | 20 | 50 | fits | 150,328 | 101 | 0.634 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if1` | 1,682,600 | 16.826 | 18 | 18 | fits | 39,944 | 21 | 0.775 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 1,278,049 | 12.780 | 20 | 24 | fits | 76,823 | 181 | 0.118 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if1` | 746,777 | 7.468 | 20 | 200 | fits | 130,708 | 56 | 0.700 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 925,049 | 9.250 | 20 | 20 | fits | 103,913 | 52 | 0.717 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if1` | 1,589,668 | 15.897 | 20 | 24 | fits | 73,699 | 37 | 0.726 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 556,326 | 5.563 | 20 | 50 | fits | 151,439 | 104 | 0.620 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if1` | 1,696,106 | 16.961 | 18 | 18 | fits | 40,046 | 21 | 0.777 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 1,280,676 | 12.807 | 20 | 24 | fits | 83,647 | 187 | 0.128 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if1` | 696,330 | 6.963 | 20 | 200 | fits | 131,519 | 62 | 0.695 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 909,033 | 9.090 | 20 | 20 | fits | 105,435 | 45 | 0.741 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if1` | 1,575,199 | 15.752 | 20 | 24 | fits | 73,793 | 38 | 0.725 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 492,515 | 4.925 | 20 | 50 | fits | 170,774 | 105 | 0.666 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if1` | 1,710,057 | 17.101 | 18 | 18 | fits | 56,361 | 30 | 0.762 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 1,276,966 | 12.770 | 20 | 24 | fits | 83,647 | 187 | 0.128 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if1` | 762,736 | 7.627 | 20 | 200 | fits | 130,833 | 62 | 0.692 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 975,422 | 9.754 | 20 | 20 | fits | 105,543 | 45 | 0.741 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if1` | 1,604,369 | 16.044 | 20 | 24 | fits | 73,716 | 38 | 0.724 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 559,550 | 5.596 | 20 | 50 | fits | 151,965 | 105 | 0.619 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if1` | 1,671,001 | 16.710 | 18 | 18 | fits | 53,228 | 25 | 0.722 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 1,277,049 | 12.770 | 20 | 24 | fits | 83,647 | 187 | 0.128 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if1` | 637,870 | 6.379 | 20 | 200 | fits | 150,803 | 102 | 0.633 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 993,192 | 9.932 | 20 | 20 | fits | 106,077 | 45 | 0.745 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if1` | 1,643,243 | 16.432 | 20 | 24 | fits | 74,300 | 38 | 0.726 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 578,127 | 5.781 | 20 | 50 | fits | 150,803 | 102 | 0.633 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if1` | 1,697,339 | 16.973 | 18 | 18 | fits | 40,398 | 22 | 0.771 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 1,280,853 | 12.809 | 20 | 24 | fits | 83,745 | 187 | 0.129 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if1` | 594,304 | 5.943 | 20 | 200 | fits | 148,367 | 108 | 0.606 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 949,995 | 9.500 | 20 | 20 | fits | 106,312 | 51 | 0.737 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if1` | 1,578,972 | 15.790 | 20 | 24 | fits | 73,405 | 37 | 0.726 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 534,561 | 5.346 | 20 | 50 | fits | 148,367 | 108 | 0.606 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if1` | 1,704,975 | 17.050 | 18 | 18 | fits | 52,886 | 25 | 0.714 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
