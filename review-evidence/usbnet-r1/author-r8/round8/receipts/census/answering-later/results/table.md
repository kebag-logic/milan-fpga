### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.acmp.if0` (notice-retried-7) | 5.661 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.adp.if0` (notice-retried-7) | 1.598 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.aecp.if0` (notice-retried-4) | 4.365 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.maap.if0` (notice-retried-4) | 4.174 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.srp.if0` (notice-retried-4) | 10.351 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-6.mrpdu.periodic.if0` (notice-retried-6) | 0.982 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-5.stream_info.if0` (notice-retried-5) | 8.252 (8.366) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 2065 | 0 | 120,132 (1.502) | fits |
| notice-retried-1 | 2062 | 0 | 120,314 (1.504) | fits |
| notice-retried-2 | 2064 | 0 | 121,577 (1.520) | fits |
| notice-retried-3 | 2062 | 0 | 121,586 (1.520) | fits |
| notice-retried-4 | 2061 | 0 | 122,476 (1.531) | fits |
| notice-retried-5 | 2061 | 0 | 121,174 (1.515) | fits |
| notice-retried-6 | 2062 | 0 | 124,957 (1.562) | fits |
| notice-retried-7 | 2061 | 0 | 120,401 (1.505) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 7.931 | 20 | 16 | 2 | within |
| notice-retried-1 | 8.194 | 20 | 16 | 2 | within |
| notice-retried-2 | 8.045 | 20 | 16 | 1 | within |
| notice-retried-3 | 8.196 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.196 | 20 | 16 | 1 | within |
| notice-retried-5 | 8.252 | 20 | 16 | 1 | within |
| notice-retried-6 | 8.075 | 20 | 16 | 1 | within |
| notice-retried-7 | 8.251 | 20 | 16 | 1 | within |

Latest: 8.252 ms, notice-retried-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 385 | 90,294 (1.129) | 77,675 (0.971) |
| notice-retried-1 | 385 | 90,294 (1.129) | 77,675 (0.971) |
| notice-retried-2 | 385 | 90,294 (1.129) | 77,675 (0.971) |
| notice-retried-3 | 385 | 90,294 (1.129) | 77,675 (0.971) |
| notice-retried-4 | 385 | 90,294 (1.129) | 77,675 (0.971) |
| notice-retried-5 | 385 | 90,294 (1.129) | 77,675 (0.971) |
| notice-retried-6 | 385 | 90,294 (1.129) | 77,675 (0.971) |
| notice-retried-7 | 385 | 90,294 (1.129) | 77,675 (0.971) |

Longest pass that carries a step: 90,294 CPU cycles (1.129 ms), notice-retried-0; longest step: 77,675 (0.971 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 634,441 | 7.931 | 20 | 24 | fits | 23,244 | 52 | 0.446 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 127,298 | 1.591 | 20 | 200 | fits | 117,931 | 249 | 0.234 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 437,466 | 5.468 | 20 | 20 | fits | 89,029 | 47 | 0.749 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 332,233 | 4.153 | 20 | 24 | fits | 117,275 | 114 | 0.416 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 316,962 | 3.962 | 20 | 50 | fits | 117,275 | 114 | 0.416 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 821,319 | 10.266 | 20 | 20 | fits | 64,430 | 30 | 0.708 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 77,643 | 0.971 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 655,495 | 8.194 | 20 | 24 | fits | 23,262 | 52 | 0.446 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 125,997 | 1.575 | 20 | 200 | fits | 119,030 | 252 | 0.225 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 436,163 | 5.452 | 20 | 20 | fits | 88,836 | 45 | 0.751 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 331,123 | 4.139 | 20 | 24 | fits | 117,284 | 114 | 0.416 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 315,852 | 3.948 | 20 | 50 | fits | 117,284 | 114 | 0.416 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 821,121 | 10.264 | 20 | 20 | fits | 64,270 | 30 | 0.706 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 76,848 | 0.961 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 643,588 | 8.045 | 20 | 24 | fits | 23,262 | 52 | 0.446 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 114,859 | 1.436 | 20 | 200 | fits | 109,987 | 154 | 0.182 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 431,523 | 5.394 | 20 | 20 | fits | 88,795 | 45 | 0.750 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 326,524 | 4.082 | 20 | 24 | fits | 121,577 | 135 | 0.402 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 311,253 | 3.891 | 20 | 50 | fits | 121,577 | 135 | 0.402 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 816,906 | 10.211 | 20 | 20 | fits | 64,493 | 30 | 0.709 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 68,359 | 0.854 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 655,656 | 8.196 | 20 | 24 | fits | 22,522 | 52 | 0.424 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 125,947 | 1.574 | 20 | 200 | fits | 119,060 | 239 | 0.249 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 351,684 | 4.396 | 20 | 20 | fits | 121,586 | 135 | 0.402 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 335,480 | 4.194 | 20 | 24 | fits | 121,586 | 135 | 0.402 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 320,209 | 4.003 | 20 | 50 | fits | 121,586 | 135 | 0.402 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 814,517 | 10.181 | 20 | 20 | fits | 52,410 | 26 | 0.726 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 76,697 | 0.959 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 655,656 | 8.196 | 20 | 24 | fits | 22,522 | 52 | 0.424 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 126,472 | 1.581 | 20 | 200 | fits | 117,549 | 235 | 0.240 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 365,395 | 4.567 | 20 | 20 | fits | 122,476 | 135 | 0.417 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 349,191 | 4.365 | 20 | 24 | fits | 122,476 | 135 | 0.417 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 333,920 | 4.174 | 20 | 50 | fits | 122,476 | 135 | 0.417 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 828,110 | 10.351 | 20 | 20 | fits | 52,410 | 26 | 0.726 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 68,952 | 0.862 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 660,125 | 8.252 | 20 | 24 | fits | 24,220 | 52 | 0.479 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 124,306 | 1.554 | 20 | 200 | fits | 119,001 | 253 | 0.221 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 448,664 | 5.608 | 20 | 20 | fits | 88,866 | 45 | 0.751 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 343,594 | 4.295 | 20 | 24 | fits | 121,174 | 127 | 0.427 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 328,323 | 4.104 | 20 | 50 | fits | 121,174 | 127 | 0.427 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 817,977 | 10.225 | 20 | 20 | fits | 64,661 | 30 | 0.711 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 77,544 | 0.969 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 646,002 | 8.075 | 20 | 24 | fits | 24,046 | 52 | 0.476 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 115,324 | 1.442 | 20 | 200 | fits | 111,389 | 157 | 0.179 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 448,841 | 5.611 | 20 | 20 | fits | 92,012 | 52 | 0.757 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 330,532 | 4.132 | 20 | 24 | fits | 124,957 | 144 | 0.395 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 315,261 | 3.941 | 20 | 50 | fits | 124,957 | 144 | 0.395 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 819,160 | 10.239 | 20 | 20 | fits | 64,659 | 30 | 0.711 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 78,561 | 0.982 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 660,092 | 8.251 | 20 | 24 | fits | 24,220 | 52 | 0.479 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 127,866 | 1.598 | 20 | 200 | fits | 116,673 | 251 | 0.249 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 452,858 | 5.661 | 20 | 20 | fits | 92,897 | 58 | 0.747 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 333,376 | 4.167 | 20 | 24 | fits | 117,581 | 116 | 0.418 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 318,105 | 3.976 | 20 | 50 | fits | 117,581 | 116 | 0.418 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 823,306 | 10.291 | 20 | 20 | fits | 64,646 | 30 | 0.711 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 69,893 | 0.874 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
