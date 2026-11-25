### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.acmp.if0` (notice-retried-3) | 7.490 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-2.held.adp.if0` (notice-retried-2) | 6.471 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-1.held.aecp.if0` (notice-retried-1) | 5.986 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.maap.if0` (notice-retried-6) | 6.930 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.srp.if0` (notice-retried-3) | 10.268 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-2.mrpdu.periodic.if0` (notice-retried-2) | 0.858 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-0.stream_info.if0` (notice-retried-0) | 8.279 (8.387) | fits | 2 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1721 | 0 | 151,149 (1.511) | fits |
| notice-retried-1 | 1720 | 0 | 155,638 (1.556) | fits |
| notice-retried-2 | 1719 | 0 | 155,403 (1.554) | fits |
| notice-retried-3 | 1717 | 0 | 151,691 (1.517) | fits |
| notice-retried-4 | 1719 | 0 | 154,159 (1.542) | fits |
| notice-retried-5 | 1717 | 0 | 153,164 (1.532) | fits |
| notice-retried-6 | 1729 | 0 | 154,127 (1.541) | fits |
| notice-retried-7 | 1729 | 0 | 155,434 (1.554) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 8.279 | 20 | 16 | 2 | within |
| notice-retried-1 | 8.279 | 20 | 16 | 2 | within |
| notice-retried-2 | 8.133 | 20 | 16 | 2 | within |
| notice-retried-3 | 8.189 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.225 | 20 | 16 | 2 | within |
| notice-retried-5 | 8.133 | 20 | 16 | 2 | within |
| notice-retried-6 | 7.981 | 20 | 16 | 1 | within |
| notice-retried-7 | 7.980 | 20 | 16 | 1 | within |

Latest: 8.279 ms, notice-retried-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 678 | 115,771 (1.158) | 78,241 (0.782) |
| notice-retried-1 | 678 | 115,955 (1.160) | 78,241 (0.782) |
| notice-retried-2 | 679 | 115,712 (1.157) | 78,241 (0.782) |
| notice-retried-3 | 679 | 115,722 (1.157) | 78,241 (0.782) |
| notice-retried-4 | 678 | 115,820 (1.158) | 78,241 (0.782) |
| notice-retried-5 | 679 | 113,016 (1.130) | 78,241 (0.782) |
| notice-retried-6 | 671 | 97,403 (0.974) | 78,241 (0.782) |
| notice-retried-7 | 671 | 97,403 (0.974) | 78,241 (0.782) |

Longest pass that carries a step: 115,955 CPU cycles (1.160 ms), notice-retried-1; longest step: 78,241 (0.782 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 827,904 | 8.279 | 20 | 24 | fits | 23,335 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 179,658 | 1.797 | 20 | 200 | fits | 151,000 | 214 | 0.261 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 745,980 | 7.460 | 20 | 20 | fits | 129,853 | 70 | 0.735 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 584,341 | 5.843 | 20 | 24 | fits | 151,149 | 119 | 0.435 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 565,070 | 5.651 | 20 | 50 | fits | 151,149 | 119 | 0.435 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 1,014,538 | 10.145 | 20 | 20 | fits | 75,555 | 34 | 0.707 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 80,912 | 0.809 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 827,904 | 8.279 | 20 | 24 | fits | 23,335 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 639,092 | 6.391 | 20 | 200 | fits | 154,530 | 98 | 0.387 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 618,824 | 6.188 | 20 | 20 | fits | 154,530 | 98 | 0.387 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 598,620 | 5.986 | 20 | 24 | fits | 154,530 | 98 | 0.387 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 130,710 | 1.307 | 20 | 50 | fits | 155,638 | 246 | 0.252 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 1,014,225 | 10.142 | 20 | 20 | fits | 54,963 | 26 | 0.742 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 79,846 | 0.798 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 813,294 | 8.133 | 20 | 24 | fits | 23,144 | 52 | 0.444 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 647,100 | 6.471 | 20 | 200 | fits | 154,683 | 217 | 0.193 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 626,832 | 6.268 | 20 | 20 | fits | 154,683 | 217 | 0.193 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 523,339 | 5.233 | 20 | 24 | fits | 117,846 | 61 | 0.501 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 587,357 | 5.874 | 20 | 50 | fits | 154,683 | 217 | 0.193 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 1,024,073 | 10.241 | 20 | 20 | fits | 54,894 | 26 | 0.741 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 85,797 | 0.858 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 818,860 | 8.189 | 20 | 24 | fits | 23,335 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 173,829 | 1.738 | 20 | 200 | fits | 151,093 | 217 | 0.257 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 749,035 | 7.490 | 20 | 20 | fits | 136,000 | 61 | 0.722 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 592,831 | 5.928 | 20 | 24 | fits | 151,691 | 115 | 0.454 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 573,560 | 5.736 | 20 | 50 | fits | 151,691 | 115 | 0.454 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 1,026,821 | 10.268 | 20 | 20 | fits | 68,825 | 37 | 0.750 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 78,935 | 0.789 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 822,481 | 8.225 | 20 | 24 | fits | 24,725 | 52 | 0.491 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 148,440 | 1.484 | 20 | 200 | fits | 147,952 | 198 | 0.264 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 725,650 | 7.256 | 20 | 20 | fits | 135,112 | 84 | 0.676 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 570,334 | 5.703 | 20 | 24 | fits | 154,159 | 121 | 0.468 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 686,175 | 6.862 | 20 | 50 | fits | 135,112 | 84 | 0.676 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 1,004,595 | 10.046 | 20 | 20 | fits | 85,706 | 38 | 0.694 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 77,560 | 0.776 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 813,281 | 8.133 | 20 | 24 | fits | 23,144 | 52 | 0.444 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 169,882 | 1.699 | 20 | 200 | fits | 153,164 | 216 | 0.252 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 747,412 | 7.474 | 20 | 20 | fits | 136,337 | 61 | 0.725 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 590,871 | 5.909 | 20 | 24 | fits | 151,943 | 115 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 571,600 | 5.716 | 20 | 50 | fits | 151,943 | 115 | 0.459 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 1,005,684 | 10.057 | 20 | 20 | fits | 65,114 | 30 | 0.721 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 84,739 | 0.847 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 798,080 | 7.981 | 20 | 24 | fits | 24,790 | 52 | 0.491 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 156,011 | 1.560 | 20 | 200 | fits | 147,885 | 199 | 0.249 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 732,434 | 7.324 | 20 | 20 | fits | 135,154 | 78 | 0.707 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 577,076 | 5.771 | 20 | 24 | fits | 154,127 | 122 | 0.465 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 692,959 | 6.930 | 20 | 50 | fits | 135,154 | 78 | 0.707 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 1,000,961 | 10.010 | 20 | 20 | fits | 75,405 | 34 | 0.706 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 81,262 | 0.813 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 798,049 | 7.980 | 20 | 24 | fits | 24,790 | 52 | 0.491 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 167,847 | 1.678 | 20 | 200 | fits | 152,426 | 221 | 0.267 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 744,808 | 7.448 | 20 | 20 | fits | 136,324 | 61 | 0.726 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 588,280 | 5.883 | 20 | 24 | fits | 155,434 | 130 | 0.460 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 569,009 | 5.690 | 20 | 50 | fits | 155,434 | 130 | 0.460 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 1,003,184 | 10.032 | 20 | 20 | fits | 65,188 | 30 | 0.721 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 81,292 | 0.813 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
