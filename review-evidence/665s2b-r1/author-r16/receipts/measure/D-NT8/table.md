### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 48 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.acmp.if0` (notice-retried-7) | 9.044 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-retried-3.held.adp.if1` (notice-retried-3) | 6.948 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-retried-3.held.aecp.if1` (notice-retried-3) | 15.526 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.maap.if0` (notice-retried-7) | 5.167 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-retried-6.held.srp.if1` (notice-retried-6) | 16.462 | fits | 31 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-6.stream_info.if0` (notice-retried-6) | 13.507 (13.709) | fits | 2 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 902 | 0 | 162,427 (1.624) | fits |
| notice-retried-1 | 902 | 0 | 162,496 (1.625) | fits |
| notice-retried-2 | 902 | 0 | 162,535 (1.625) | fits |
| notice-retried-3 | 901 | 0 | 153,771 (1.538) | fits |
| notice-retried-4 | 902 | 0 | 162,577 (1.626) | fits |
| notice-retried-5 | 900 | 0 | 161,930 (1.619) | fits |
| notice-retried-6 | 901 | 0 | 152,262 (1.523) | fits |
| notice-retried-7 | 901 | 0 | 162,843 (1.628) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 12.697 | 20 | 32 | 1 | within |
| notice-retried-1 | 12.473 | 20 | 32 | 1 | within |
| notice-retried-2 | 12.732 | 20 | 32 | 1 | within |
| notice-retried-3 | 12.716 | 20 | 32 | 1 | within |
| notice-retried-4 | 13.184 | 20 | 32 | 1 | within |
| notice-retried-5 | 13.507 | 20 | 32 | 2 | within |
| notice-retried-6 | 13.507 | 20 | 32 | 2 | within |
| notice-retried-7 | 12.707 | 20 | 32 | 1 | within |

Latest: 13.507 ms, notice-retried-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 304 | 57,535 (0.575) | 31,936 (0.319) |
| notice-retried-1 | 304 | 65,365 (0.654) | 31,936 (0.319) |
| notice-retried-2 | 304 | 57,535 (0.575) | 31,936 (0.319) |
| notice-retried-3 | 304 | 57,535 (0.575) | 31,936 (0.319) |
| notice-retried-4 | 304 | 57,535 (0.575) | 31,936 (0.319) |
| notice-retried-5 | 304 | 57,535 (0.575) | 31,936 (0.319) |
| notice-retried-6 | 304 | 57,535 (0.575) | 31,936 (0.319) |
| notice-retried-7 | 304 | 57,535 (0.575) | 31,936 (0.319) |

Longest pass that carries a step: 65,365 CPU cycles (0.654 ms), notice-retried-1; longest step: 31,936 (0.319 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 1,269,658 | 12.697 | 20 | 24 | fits | 72,389 | 181 | 0.119 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if1` | 538,450 | 5.385 | 20 | 200 | fits | 111,545 | 94 | 0.600 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 854,273 | 8.543 | 20 | 20 | fits | 99,715 | 46 | 0.741 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if1` | 1,509,097 | 15.091 | 20 | 24 | fits | 71,576 | 37 | 0.733 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 478,707 | 4.787 | 20 | 50 | fits | 111,545 | 94 | 0.600 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if1` | 1,623,411 | 16.234 | 18 | 18 | fits | 51,089 | 24 | 0.723 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 1,247,334 | 12.473 | 20 | 24 | fits | 72,314 | 181 | 0.117 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if1` | 651,525 | 6.515 | 20 | 200 | fits | 91,019 | 49 | 0.659 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 848,918 | 8.489 | 20 | 20 | fits | 99,815 | 46 | 0.743 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if1` | 1,503,700 | 15.037 | 20 | 24 | fits | 71,446 | 37 | 0.731 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 500,763 | 5.008 | 20 | 50 | fits | 141,871 | 104 | 0.621 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if1` | 1,618,034 | 16.180 | 18 | 18 | fits | 51,024 | 24 | 0.723 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 1,273,238 | 12.732 | 20 | 24 | fits | 72,314 | 181 | 0.117 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if1` | 682,184 | 6.822 | 20 | 200 | fits | 119,962 | 56 | 0.694 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 850,701 | 8.507 | 20 | 20 | fits | 99,485 | 52 | 0.726 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if1` | 1,476,829 | 14.768 | 20 | 24 | fits | 71,498 | 37 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 502,479 | 5.025 | 20 | 50 | fits | 141,871 | 104 | 0.621 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if1` | 1,642,076 | 16.421 | 18 | 18 | fits | 51,089 | 24 | 0.723 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 1,271,616 | 12.716 | 20 | 24 | fits | 72,314 | 181 | 0.117 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if1` | 694,807 | 6.948 | 20 | 200 | fits | 120,008 | 56 | 0.694 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 897,657 | 8.977 | 20 | 20 | fits | 105,283 | 54 | 0.735 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if1` | 1,552,554 | 15.526 | 20 | 24 | fits | 71,392 | 37 | 0.730 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 515,056 | 5.151 | 20 | 50 | fits | 140,836 | 104 | 0.617 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if1` | 1,604,224 | 16.042 | 18 | 18 | fits | 39,706 | 21 | 0.770 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 1,318,380 | 13.184 | 20 | 24 | fits | 114,587 | 196 | 0.193 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if1` | 566,184 | 5.662 | 20 | 200 | fits | 141,068 | 102 | 0.634 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 893,990 | 8.940 | 20 | 20 | fits | 99,571 | 45 | 0.744 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if1` | 1,509,496 | 15.095 | 20 | 24 | fits | 71,463 | 38 | 0.728 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 506,441 | 5.064 | 20 | 50 | fits | 141,068 | 102 | 0.634 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if1` | 1,624,193 | 16.242 | 18 | 18 | fits | 51,143 | 25 | 0.719 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 1,350,699 | 13.507 | 20 | 24 | fits | 114,541 | 196 | 0.192 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if1` | 679,042 | 6.790 | 20 | 200 | fits | 120,146 | 57 | 0.692 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 888,439 | 8.884 | 20 | 20 | fits | 99,750 | 45 | 0.746 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if1` | 1,534,608 | 15.346 | 20 | 24 | fits | 71,768 | 38 | 0.732 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 499,153 | 4.992 | 20 | 50 | fits | 142,222 | 105 | 0.622 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if1` | 1,598,060 | 15.981 | 18 | 18 | fits | 51,501 | 25 | 0.722 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 1,350,710 | 13.507 | 20 | 24 | fits | 114,541 | 196 | 0.192 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if1` | 665,782 | 6.658 | 20 | 200 | fits | 120,064 | 57 | 0.690 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 875,162 | 8.752 | 20 | 20 | fits | 100,815 | 51 | 0.737 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if1` | 1,489,428 | 14.894 | 20 | 24 | fits | 43,299 | 30 | 0.699 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 485,975 | 4.860 | 20 | 50 | fits | 140,270 | 111 | 0.599 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if1` | 1,646,216 | 16.462 | 18 | 18 | fits | 39,611 | 22 | 0.761 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 1,270,696 | 12.707 | 20 | 24 | fits | 72,314 | 181 | 0.117 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if1` | 576,447 | 5.764 | 20 | 200 | fits | 142,850 | 108 | 0.629 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 904,450 | 9.044 | 20 | 20 | fits | 100,667 | 51 | 0.736 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if1` | 1,535,064 | 15.351 | 20 | 24 | fits | 71,522 | 37 | 0.731 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 516,704 | 5.167 | 20 | 50 | fits | 142,850 | 108 | 0.629 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if1` | 1,640,584 | 16.406 | 18 | 18 | fits | 39,621 | 22 | 0.761 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
