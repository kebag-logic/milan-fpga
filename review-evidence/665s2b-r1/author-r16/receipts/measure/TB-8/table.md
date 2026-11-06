### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 6 paths and 8 of 48 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.acmp.if0` (notice-retried-5) | 10.162 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-retried-3.held.adp.if1` (notice-retried-3) | 7.741 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-retried-5.held.aecp.if1` (notice-retried-5) | 19.172 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.maap.if0` (notice-retried-5) | 5.921 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-retried-4.held.srp.if1` (notice-retried-4) | 20.108 | MISS ceiling | 31 srp | 8 | 8 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-5.stream_info.if0` (notice-retried-5) | 13.080 (13.277) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 930 | 0 | 190,467 (1.905) | fits |
| notice-retried-1 | 928 | 0 | 190,534 (1.905) | fits |
| notice-retried-2 | 928 | 0 | 190,311 (1.903) | fits |
| notice-retried-3 | 927 | 0 | 192,691 (1.927) | fits |
| notice-retried-4 | 928 | 0 | 173,977 (1.740) | fits |
| notice-retried-5 | 927 | 0 | 190,376 (1.904) | fits |
| notice-retried-6 | 928 | 0 | 190,459 (1.905) | fits |
| notice-retried-7 | 927 | 0 | 191,070 (1.911) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 12.554 | 20 | 32 | 1 | within |
| notice-retried-1 | 12.554 | 20 | 32 | 1 | within |
| notice-retried-2 | 12.804 | 20 | 32 | 1 | within |
| notice-retried-3 | 12.553 | 20 | 32 | 1 | within |
| notice-retried-4 | 12.614 | 20 | 32 | 1 | within |
| notice-retried-5 | 13.080 | 20 | 32 | 1 | within |
| notice-retried-6 | 12.827 | 20 | 32 | 1 | within |
| notice-retried-7 | 12.578 | 20 | 32 | 1 | within |

Latest: 13.080 ms, notice-retried-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 304 | 53,374 (0.534) | 31,115 (0.311) |
| notice-retried-1 | 304 | 53,374 (0.534) | 31,115 (0.311) |
| notice-retried-2 | 304 | 60,351 (0.604) | 31,115 (0.311) |
| notice-retried-3 | 304 | 53,374 (0.534) | 31,115 (0.311) |
| notice-retried-4 | 304 | 53,374 (0.534) | 31,115 (0.311) |
| notice-retried-5 | 304 | 53,374 (0.534) | 31,115 (0.311) |
| notice-retried-6 | 304 | 53,374 (0.534) | 31,115 (0.311) |
| notice-retried-7 | 304 | 53,374 (0.534) | 31,115 (0.311) |

Longest pass that carries a step: 60,351 CPU cycles (0.604 ms), notice-retried-2; longest step: 31,115 (0.311 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 1,255,418 | 12.554 | 20 | 24 | fits | 76,061 | 181 | 0.132 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if1` | 608,447 | 6.084 | 20 | 200 | fits | 117,170 | 94 | 0.595 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 959,582 | 9.596 | 20 | 20 | fits | 110,103 | 46 | 0.756 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if1` | 1,897,913 | 18.979 | 20 | 24 | fits | 78,364 | 38 | 0.752 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 548,704 | 5.487 | 20 | 50 | fits | 117,170 | 94 | 0.595 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if1` | 1,969,861 | 19.699 | 18 | 18 | MISS ceiling | 55,708 | 25 | 0.734 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 1,255,379 | 12.554 | 20 | 24 | fits | 76,061 | 181 | 0.132 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if1` | 640,920 | 6.409 | 20 | 200 | fits | 153,520 | 103 | 0.643 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 996,633 | 9.966 | 20 | 20 | fits | 110,092 | 46 | 0.756 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if1` | 1,887,235 | 18.872 | 20 | 24 | fits | 80,201 | 44 | 0.745 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 581,177 | 5.812 | 20 | 50 | fits | 153,520 | 103 | 0.643 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if1` | 2,003,406 | 20.034 | 18 | 18 | MISS ceiling | 44,065 | 22 | 0.791 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 1,280,353 | 12.804 | 20 | 24 | fits | 76,061 | 181 | 0.132 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if1` | 649,006 | 6.490 | 20 | 200 | fits | 153,179 | 101 | 0.643 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 963,747 | 9.637 | 20 | 20 | fits | 110,440 | 46 | 0.760 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if1` | 1,896,427 | 18.964 | 20 | 24 | fits | 78,104 | 39 | 0.747 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 589,263 | 5.893 | 20 | 50 | fits | 153,179 | 101 | 0.643 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if1` | 1,970,355 | 19.704 | 18 | 18 | MISS ceiling | 55,650 | 25 | 0.736 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 1,255,339 | 12.553 | 20 | 24 | fits | 76,061 | 181 | 0.132 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if1` | 774,069 | 7.741 | 20 | 200 | fits | 133,331 | 56 | 0.708 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 956,864 | 9.569 | 20 | 20 | fits | 107,193 | 52 | 0.730 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if1` | 1,891,075 | 18.911 | 20 | 24 | fits | 77,744 | 37 | 0.749 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 580,995 | 5.810 | 20 | 50 | fits | 154,202 | 104 | 0.629 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if1` | 1,997,492 | 19.975 | 18 | 18 | MISS ceiling | 46,125 | 28 | 0.778 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 1,261,391 | 12.614 | 20 | 24 | fits | 86,940 | 187 | 0.151 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if1` | 696,411 | 6.964 | 20 | 200 | fits | 133,800 | 62 | 0.704 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 917,434 | 9.174 | 20 | 20 | fits | 109,758 | 45 | 0.757 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if1` | 1,839,862 | 18.399 | 20 | 24 | fits | 79,371 | 43 | 0.750 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 490,834 | 4.908 | 20 | 50 | fits | 173,977 | 105 | 0.676 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if1` | 2,010,845 | 20.108 | 18 | 18 | MISS ceiling | 43,706 | 21 | 0.796 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 1,307,990 | 13.080 | 20 | 24 | fits | 77,330 | 181 | 0.141 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if1` | 651,794 | 6.518 | 20 | 200 | fits | 153,466 | 102 | 0.642 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 1,016,212 | 10.162 | 20 | 20 | fits | 109,739 | 45 | 0.757 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if1` | 1,917,153 | 19.172 | 20 | 24 | fits | 78,596 | 43 | 0.745 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 592,051 | 5.921 | 20 | 50 | fits | 153,466 | 102 | 0.642 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if1` | 1,988,805 | 19.888 | 18 | 18 | MISS ceiling | 55,474 | 24 | 0.738 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 1,282,742 | 12.827 | 20 | 24 | fits | 87,004 | 187 | 0.152 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if1` | 642,164 | 6.422 | 20 | 200 | fits | 153,515 | 102 | 0.642 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 1,007,076 | 10.071 | 20 | 20 | fits | 109,893 | 45 | 0.758 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if1` | 1,899,151 | 18.992 | 20 | 24 | fits | 77,881 | 38 | 0.747 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 582,421 | 5.824 | 20 | 50 | fits | 153,515 | 102 | 0.642 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if1` | 1,985,953 | 19.860 | 18 | 18 | MISS ceiling | 55,821 | 24 | 0.744 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 1,257,808 | 12.578 | 20 | 24 | fits | 86,940 | 187 | 0.151 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if1` | 727,937 | 7.279 | 20 | 200 | fits | 133,949 | 57 | 0.711 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 960,984 | 9.610 | 20 | 20 | fits | 109,715 | 51 | 0.750 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if1` | 1,886,752 | 18.868 | 20 | 24 | fits | 77,906 | 38 | 0.748 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 534,245 | 5.342 | 20 | 50 | fits | 151,835 | 111 | 0.605 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if1` | 1,958,729 | 19.587 | 18 | 18 | MISS ceiling | 55,773 | 25 | 0.734 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
