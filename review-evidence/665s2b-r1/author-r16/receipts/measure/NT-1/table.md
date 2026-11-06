### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 48 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.acmp.if0` (notice-retried-3) | 6.144 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.adp.if0` (notice-retried-3) | 4.000 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.aecp.if0` (notice-retried-6) | 10.814 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.maap.if0` (notice-retried-3) | 3.403 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-2.held.srp.if0` (notice-retried-2) | 10.882 | fits | 30 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-3.stream_info.if0` (notice-retried-3) | 12.410 (12.530) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1571 | 0 | 115,261 (1.153) | fits |
| notice-retried-1 | 1571 | 0 | 115,261 (1.153) | fits |
| notice-retried-2 | 1572 | 0 | 115,348 (1.153) | fits |
| notice-retried-3 | 1571 | 0 | 115,328 (1.153) | fits |
| notice-retried-4 | 1574 | 0 | 115,328 (1.153) | fits |
| notice-retried-5 | 1572 | 0 | 115,328 (1.153) | fits |
| notice-retried-6 | 1574 | 0 | 115,328 (1.153) | fits |
| notice-retried-7 | 1573 | 0 | 115,819 (1.158) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 12.409 | 20 | 16 | 1 | within |
| notice-retried-1 | 12.302 | 20 | 16 | 1 | within |
| notice-retried-2 | 12.409 | 20 | 16 | 1 | within |
| notice-retried-3 | 12.410 | 20 | 16 | 1 | within |
| notice-retried-4 | 12.401 | 20 | 16 | 1 | within |
| notice-retried-5 | 12.401 | 20 | 16 | 1 | within |
| notice-retried-6 | 12.376 | 20 | 16 | 1 | within |
| notice-retried-7 | 12.376 | 20 | 16 | 1 | within |

Latest: 12.410 ms, notice-retried-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 308 | 115,261 (1.153) | 76,363 (0.764) |
| notice-retried-1 | 308 | 115,261 (1.153) | 76,363 (0.764) |
| notice-retried-2 | 308 | 115,348 (1.153) | 76,363 (0.764) |
| notice-retried-3 | 308 | 115,328 (1.153) | 76,363 (0.764) |
| notice-retried-4 | 308 | 115,328 (1.153) | 76,363 (0.764) |
| notice-retried-5 | 308 | 115,328 (1.153) | 76,363 (0.764) |
| notice-retried-6 | 308 | 115,328 (1.153) | 76,363 (0.764) |
| notice-retried-7 | 308 | 115,819 (1.158) | 76,363 (0.764) |

Longest pass that carries a step: 115,819 CPU cycles (1.158 ms), notice-retried-7; longest step: 76,363 (0.764 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 1,240,892 | 12.409 | 20 | 24 | fits | 38,283 | 100 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 392,442 | 3.924 | 20 | 200 | fits | 97,184 | 99 | 0.627 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 599,200 | 5.992 | 20 | 20 | fits | 62,831 | 41 | 0.753 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 1,066,482 | 10.665 | 20 | 24 | fits | 54,221 | 41 | 0.709 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 332,699 | 3.327 | 20 | 50 | fits | 97,184 | 99 | 0.627 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 1,084,965 | 10.850 | 18 | 18 | fits | 25,327 | 20 | 0.766 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 1,230,236 | 12.302 | 20 | 24 | fits | 38,283 | 100 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 395,469 | 3.955 | 20 | 200 | fits | 97,211 | 99 | 0.628 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 602,227 | 6.022 | 20 | 20 | fits | 62,831 | 41 | 0.753 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 1,069,509 | 10.695 | 20 | 24 | fits | 54,221 | 41 | 0.709 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 335,726 | 3.357 | 20 | 50 | fits | 97,211 | 99 | 0.628 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 1,087,992 | 10.880 | 18 | 18 | fits | 25,327 | 20 | 0.766 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 1,240,892 | 12.409 | 20 | 24 | fits | 38,283 | 100 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 392,542 | 3.925 | 20 | 200 | fits | 97,211 | 99 | 0.628 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 606,878 | 6.069 | 20 | 20 | fits | 70,469 | 43 | 0.738 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 1,056,719 | 10.567 | 20 | 24 | fits | 52,891 | 36 | 0.716 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 332,799 | 3.328 | 20 | 50 | fits | 97,211 | 99 | 0.628 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 1,088,201 | 10.882 | 18 | 18 | fits | 28,482 | 26 | 0.784 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 1,241,049 | 12.410 | 20 | 24 | fits | 38,283 | 100 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 400,032 | 4.000 | 20 | 200 | fits | 97,211 | 99 | 0.628 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 614,428 | 6.144 | 20 | 20 | fits | 70,469 | 43 | 0.738 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 1,048,071 | 10.481 | 20 | 24 | fits | 52,729 | 36 | 0.714 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 340,289 | 3.403 | 20 | 50 | fits | 97,211 | 99 | 0.628 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 1,074,358 | 10.744 | 18 | 18 | fits | 32,919 | 24 | 0.703 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 1,240,073 | 12.401 | 20 | 24 | fits | 41,139 | 106 | 0.174 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 236,810 | 2.368 | 20 | 200 | fits | 73,729 | 100 | 0.510 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 535,107 | 5.351 | 20 | 20 | fits | 70,495 | 44 | 0.734 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 1,002,599 | 10.026 | 20 | 24 | fits | 52,922 | 35 | 0.720 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 259,778 | 2.598 | 20 | 50 | fits | 82,711 | 66 | 0.739 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 1,087,081 | 10.871 | 18 | 18 | fits | 25,175 | 20 | 0.760 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 1,240,073 | 12.401 | 20 | 24 | fits | 41,139 | 106 | 0.174 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 376,257 | 3.763 | 20 | 200 | fits | 97,232 | 100 | 0.624 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 591,007 | 5.910 | 20 | 20 | fits | 70,607 | 44 | 0.735 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 1,058,517 | 10.585 | 20 | 24 | fits | 52,922 | 35 | 0.720 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 316,514 | 3.165 | 20 | 50 | fits | 97,232 | 100 | 0.624 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 1,077,262 | 10.773 | 18 | 18 | fits | 25,334 | 20 | 0.766 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 1,237,618 | 12.376 | 20 | 24 | fits | 41,185 | 106 | 0.177 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 225,706 | 2.257 | 20 | 200 | fits | 90,912 | 98 | 0.622 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 613,484 | 6.135 | 20 | 20 | fits | 70,675 | 44 | 0.736 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 1,081,365 | 10.814 | 20 | 24 | fits | 52,922 | 35 | 0.720 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 338,989 | 3.390 | 20 | 50 | fits | 99,717 | 104 | 0.630 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 1,074,776 | 10.748 | 18 | 18 | fits | 34,707 | 25 | 0.741 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 1,237,618 | 12.376 | 20 | 24 | fits | 41,185 | 106 | 0.177 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 372,491 | 3.725 | 20 | 200 | fits | 96,972 | 99 | 0.625 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 562,663 | 5.627 | 20 | 20 | fits | 70,626 | 44 | 0.736 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 1,030,266 | 10.303 | 20 | 24 | fits | 52,922 | 35 | 0.720 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 312,748 | 3.127 | 20 | 50 | fits | 96,972 | 99 | 0.625 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 1,081,865 | 10.819 | 18 | 18 | fits | 25,226 | 20 | 0.762 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
