### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.acmp.if0` (notice-retried-6) | 8.184 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.adp.if0` (notice-retried-6) | 6.944 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-2.held.aecp.if0` (notice-retried-2) | 5.905 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.maap.if0` (notice-retried-3) | 6.875 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.srp.if0` (notice-retried-6) | 10.941 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-3.mrpdu.periodic.if0` (notice-retried-3) | 0.627 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-3.stream_info.if0` (notice-retried-3) | 8.229 (8.336) | fits | 2 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1630 | 0 | 157,092 (1.571) | fits |
| notice-retried-1 | 1630 | 0 | 157,036 (1.570) | fits |
| notice-retried-2 | 1629 | 0 | 154,075 (1.541) | fits |
| notice-retried-3 | 1630 | 0 | 152,631 (1.526) | fits |
| notice-retried-4 | 1630 | 0 | 154,715 (1.547) | fits |
| notice-retried-5 | 1629 | 0 | 154,549 (1.545) | fits |
| notice-retried-6 | 1627 | 0 | 155,987 (1.560) | fits |
| notice-retried-7 | 1628 | 0 | 155,931 (1.559) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 7.966 | 20 | 16 | 1 | within |
| notice-retried-1 | 8.188 | 20 | 16 | 2 | within |
| notice-retried-2 | 8.075 | 20 | 16 | 1 | within |
| notice-retried-3 | 8.229 | 20 | 16 | 2 | within |
| notice-retried-4 | 8.010 | 20 | 16 | 1 | within |
| notice-retried-5 | 8.219 | 20 | 16 | 1 | within |
| notice-retried-6 | 8.172 | 20 | 16 | 2 | within |
| notice-retried-7 | 8.172 | 20 | 16 | 2 | within |

Latest: 8.229 ms, notice-retried-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 667 | 107,714 (1.077) | 78,424 (0.784) |
| notice-retried-1 | 667 | 107,921 (1.079) | 78,424 (0.784) |
| notice-retried-2 | 667 | 108,036 (1.080) | 78,424 (0.784) |
| notice-retried-3 | 667 | 107,956 (1.080) | 78,424 (0.784) |
| notice-retried-4 | 667 | 102,087 (1.021) | 78,424 (0.784) |
| notice-retried-5 | 667 | 107,876 (1.079) | 78,424 (0.784) |
| notice-retried-6 | 668 | 107,714 (1.077) | 78,424 (0.784) |
| notice-retried-7 | 668 | 107,804 (1.078) | 78,424 (0.784) |

Longest pass that carries a step: 108,036 CPU cycles (1.080 ms), notice-retried-2; longest step: 78,424 (0.784 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 796,606 | 7.966 | 20 | 24 | fits | 24,030 | 52 | 0.447 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 643,632 | 6.436 | 20 | 200 | fits | 147,170 | 201 | 0.338 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 765,610 | 7.656 | 20 | 20 | fits | 130,190 | 129 | 0.642 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 517,789 | 5.178 | 20 | 24 | fits | 107,628 | 51 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 583,889 | 5.839 | 20 | 50 | fits | 147,170 | 201 | 0.338 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 1,052,290 | 10.523 | 20 | 20 | fits | 80,972 | 79 | 0.656 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 49,720 | 0.497 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 818,794 | 8.188 | 20 | 24 | fits | 24,108 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 649,029 | 6.490 | 20 | 200 | fits | 153,207 | 203 | 0.332 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 773,390 | 7.734 | 20 | 20 | fits | 132,642 | 138 | 0.654 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 512,982 | 5.130 | 20 | 24 | fits | 107,628 | 51 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 589,286 | 5.893 | 20 | 50 | fits | 153,207 | 203 | 0.332 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 1,049,779 | 10.498 | 20 | 20 | fits | 70,503 | 66 | 0.682 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 62,142 | 0.621 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 807,513 | 8.075 | 20 | 24 | fits | 23,477 | 52 | 0.431 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 169,058 | 1.691 | 20 | 200 | fits | 154,075 | 224 | 0.357 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 745,705 | 7.457 | 20 | 20 | fits | 135,035 | 133 | 0.638 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 590,466 | 5.905 | 20 | 24 | fits | 151,984 | 117 | 0.456 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 571,195 | 5.712 | 20 | 50 | fits | 151,984 | 117 | 0.456 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 1,041,015 | 10.410 | 20 | 20 | fits | 73,578 | 73 | 0.692 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 51,537 | 0.515 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 822,940 | 8.229 | 20 | 24 | fits | 24,411 | 52 | 0.457 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 153,364 | 1.534 | 20 | 200 | fits | 140,841 | 146 | 0.233 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 726,937 | 7.269 | 20 | 20 | fits | 134,202 | 141 | 0.639 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 572,531 | 5.725 | 20 | 24 | fits | 151,877 | 115 | 0.457 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 687,462 | 6.875 | 20 | 50 | fits | 134,202 | 141 | 0.639 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 1,030,404 | 10.304 | 20 | 20 | fits | 85,241 | 92 | 0.657 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 62,674 | 0.627 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 801,034 | 8.010 | 20 | 24 | fits | 24,484 | 52 | 0.460 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 155,873 | 1.559 | 20 | 200 | fits | 149,097 | 201 | 0.335 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 736,221 | 7.362 | 20 | 20 | fits | 134,515 | 130 | 0.626 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 581,502 | 5.815 | 20 | 24 | fits | 154,715 | 136 | 0.472 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 562,231 | 5.622 | 20 | 50 | fits | 154,715 | 136 | 0.472 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 1,022,302 | 10.223 | 20 | 20 | fits | 80,733 | 79 | 0.654 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 50,644 | 0.506 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 821,878 | 8.219 | 20 | 24 | fits | 24,484 | 52 | 0.460 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 152,113 | 1.521 | 20 | 200 | fits | 151,589 | 156 | 0.203 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 720,017 | 7.200 | 20 | 20 | fits | 132,955 | 138 | 0.621 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 566,858 | 5.669 | 20 | 24 | fits | 154,549 | 127 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 680,542 | 6.805 | 20 | 50 | fits | 132,955 | 138 | 0.621 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 1,016,239 | 10.162 | 20 | 20 | fits | 91,040 | 92 | 0.631 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 49,550 | 0.495 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 817,179 | 8.172 | 20 | 24 | fits | 23,990 | 52 | 0.452 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 694,404 | 6.944 | 20 | 200 | fits | 153,604 | 216 | 0.352 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 818,367 | 8.184 | 20 | 20 | fits | 132,344 | 138 | 0.652 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 512,980 | 5.130 | 20 | 24 | fits | 107,621 | 51 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 634,661 | 6.347 | 20 | 50 | fits | 153,604 | 216 | 0.352 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 1,094,061 | 10.941 | 20 | 20 | fits | 70,264 | 66 | 0.680 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 56,860 | 0.569 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 817,179 | 8.172 | 20 | 24 | fits | 23,990 | 52 | 0.452 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 691,484 | 6.915 | 20 | 200 | fits | 153,604 | 216 | 0.352 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 815,531 | 8.155 | 20 | 20 | fits | 132,428 | 138 | 0.652 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 516,792 | 5.168 | 20 | 24 | fits | 107,607 | 51 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 631,741 | 6.317 | 20 | 50 | fits | 153,604 | 216 | 0.352 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 1,091,166 | 10.912 | 20 | 20 | fits | 70,264 | 66 | 0.680 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 55,963 | 0.560 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
