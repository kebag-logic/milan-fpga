### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 48 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.acmp.if0` (notice-retried-4) | 8.815 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-retried-6.held.adp.if1` (notice-retried-6) | 6.221 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-retried-1.held.aecp.if1` (notice-retried-1) | 16.266 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-1.held.maap.if0` (notice-retried-1) | 5.755 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-retried-2.held.srp.if1` (notice-retried-2) | 16.790 | fits | 31 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-5.stream_info.if0` (notice-retried-5) | 13.318 (13.518) | fits | 2 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 933 | 0 | 194,198 (1.942) | fits |
| notice-retried-1 | 934 | 0 | 194,224 (1.942) | fits |
| notice-retried-2 | 935 | 0 | 194,303 (1.943) | fits |
| notice-retried-3 | 934 | 0 | 194,377 (1.944) | fits |
| notice-retried-4 | 933 | 0 | 195,756 (1.958) | fits |
| notice-retried-5 | 935 | 0 | 188,284 (1.883) | fits |
| notice-retried-6 | 933 | 0 | 194,646 (1.946) | fits |
| notice-retried-7 | 934 | 0 | 194,301 (1.943) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 12.648 | 20 | 32 | 1 | within |
| notice-retried-1 | 12.611 | 20 | 32 | 1 | within |
| notice-retried-2 | 12.650 | 20 | 32 | 1 | within |
| notice-retried-3 | 12.648 | 20 | 32 | 1 | within |
| notice-retried-4 | 13.008 | 20 | 32 | 1 | within |
| notice-retried-5 | 13.318 | 20 | 32 | 2 | within |
| notice-retried-6 | 13.317 | 20 | 32 | 2 | within |
| notice-retried-7 | 12.678 | 20 | 32 | 1 | within |

Latest: 13.318 ms, notice-retried-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 304 | 55,983 (0.560) | 32,394 (0.324) |
| notice-retried-1 | 304 | 64,410 (0.644) | 32,394 (0.324) |
| notice-retried-2 | 304 | 55,983 (0.560) | 32,394 (0.324) |
| notice-retried-3 | 304 | 55,983 (0.560) | 32,394 (0.324) |
| notice-retried-4 | 304 | 55,983 (0.560) | 32,394 (0.324) |
| notice-retried-5 | 304 | 55,983 (0.560) | 32,394 (0.324) |
| notice-retried-6 | 304 | 55,983 (0.560) | 32,394 (0.324) |
| notice-retried-7 | 304 | 55,983 (0.560) | 32,394 (0.324) |

Longest pass that carries a step: 64,410 CPU cycles (0.644 ms), notice-retried-1; longest step: 32,394 (0.324 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 1,264,768 | 12.648 | 20 | 24 | fits | 71,288 | 181 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if1` | 586,287 | 5.863 | 20 | 200 | fits | 108,900 | 75 | 0.614 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 821,186 | 8.212 | 20 | 20 | fits | 127,876 | 53 | 0.706 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if1` | 1,560,696 | 15.607 | 20 | 24 | fits | 72,998 | 37 | 0.730 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 526,544 | 5.265 | 20 | 50 | fits | 108,900 | 75 | 0.614 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if1` | 1,672,446 | 16.724 | 18 | 18 | fits | 45,925 | 30 | 0.757 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 1,261,066 | 12.611 | 20 | 24 | fits | 71,519 | 181 | 0.142 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if1` | 496,384 | 4.964 | 20 | 200 | fits | 152,346 | 104 | 0.633 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 873,809 | 8.738 | 20 | 20 | fits | 128,077 | 53 | 0.708 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if1` | 1,626,624 | 16.266 | 20 | 24 | fits | 73,390 | 37 | 0.731 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 575,540 | 5.755 | 20 | 50 | fits | 138,899 | 77 | 0.680 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if1` | 1,639,593 | 16.396 | 18 | 18 | fits | 54,265 | 26 | 0.754 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 1,265,027 | 12.650 | 20 | 24 | fits | 71,449 | 181 | 0.141 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if1` | 491,777 | 4.918 | 20 | 200 | fits | 152,346 | 104 | 0.633 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 832,564 | 8.326 | 20 | 20 | fits | 126,736 | 59 | 0.685 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if1` | 1,573,053 | 15.731 | 20 | 24 | fits | 73,056 | 37 | 0.730 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 570,681 | 5.707 | 20 | 50 | fits | 138,647 | 75 | 0.681 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if1` | 1,679,025 | 16.790 | 18 | 18 | fits | 40,076 | 21 | 0.788 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 1,264,768 | 12.648 | 20 | 24 | fits | 71,358 | 181 | 0.140 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if1` | 621,828 | 6.218 | 20 | 200 | fits | 141,758 | 82 | 0.653 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 825,543 | 8.255 | 20 | 20 | fits | 95,771 | 45 | 0.678 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if1` | 1,566,897 | 15.669 | 20 | 24 | fits | 72,950 | 37 | 0.730 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 562,085 | 5.621 | 20 | 50 | fits | 141,758 | 82 | 0.653 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if1` | 1,673,035 | 16.730 | 18 | 18 | fits | 40,234 | 21 | 0.788 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 1,300,761 | 13.008 | 20 | 24 | fits | 120,772 | 196 | 0.207 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if1` | 494,898 | 4.949 | 20 | 200 | fits | 152,565 | 105 | 0.632 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 881,538 | 8.815 | 20 | 20 | fits | 127,891 | 52 | 0.708 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if1` | 1,610,126 | 16.101 | 20 | 24 | fits | 73,178 | 38 | 0.727 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 574,021 | 5.740 | 20 | 50 | fits | 138,866 | 76 | 0.680 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if1` | 1,663,941 | 16.639 | 18 | 18 | fits | 40,632 | 22 | 0.786 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 1,331,782 | 13.318 | 20 | 24 | fits | 120,710 | 196 | 0.206 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if1` | 453,227 | 4.532 | 20 | 200 | fits | 188,284 | 111 | 0.647 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 841,452 | 8.415 | 20 | 20 | fits | 127,783 | 58 | 0.699 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if1` | 1,556,072 | 15.561 | 20 | 24 | fits | 78,457 | 46 | 0.716 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 533,768 | 5.338 | 20 | 50 | fits | 140,284 | 76 | 0.690 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if1` | 1,674,964 | 16.750 | 18 | 18 | fits | 52,764 | 25 | 0.726 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 1,331,706 | 13.317 | 20 | 24 | fits | 120,772 | 196 | 0.207 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if1` | 622,113 | 6.221 | 20 | 200 | fits | 142,040 | 83 | 0.652 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 869,948 | 8.699 | 20 | 20 | fits | 127,788 | 58 | 0.699 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if1` | 1,615,989 | 16.160 | 20 | 24 | fits | 73,334 | 38 | 0.730 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 562,370 | 5.624 | 20 | 50 | fits | 142,040 | 83 | 0.652 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if1` | 1,629,110 | 16.291 | 18 | 18 | fits | 54,417 | 27 | 0.746 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 1,267,846 | 12.678 | 20 | 24 | fits | 71,664 | 181 | 0.145 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if1` | 582,269 | 5.823 | 20 | 200 | fits | 141,185 | 89 | 0.637 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 818,671 | 8.187 | 20 | 20 | fits | 128,083 | 53 | 0.707 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if1` | 1,558,374 | 15.584 | 20 | 24 | fits | 73,015 | 37 | 0.730 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 522,526 | 5.225 | 20 | 50 | fits | 141,185 | 89 | 0.637 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if1` | 1,670,888 | 16.709 | 18 | 18 | fits | 40,531 | 22 | 0.781 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
