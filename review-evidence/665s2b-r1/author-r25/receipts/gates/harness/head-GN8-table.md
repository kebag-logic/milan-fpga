### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 736 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.acmp.if0` (notice-burst-2) | 16.907 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-5.held.adp.if1` (notice-burst-5) | 14.679 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-burst-2.held.aecp.if1` (notice-burst-2) | 18.715 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.maap.if0` (notice-burst-2) | 13.480 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-every-2.held.srp.if1` (notice-every-2) | 8.266 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-3.mrpdu.periodic.if0` (notice-every-3) | 2.347 | fits | 0 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-3.mrpdu.periodic.if1` (notice-every-3) | 3.441 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-1.notices.29.36.0.if0` (notice-burst-1) | 33.474 (33.804) | fits | 1 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 994 | 0 | 179,159 (1.792) | fits |
| notice-every-1 | 985 | 0 | 176,508 (1.765) | fits |
| notice-every-2 | 992 | 0 | 188,021 (1.880) | fits |
| notice-every-3 | 987 | 0 | 174,985 (1.750) | fits |
| notice-every-4 | 990 | 0 | 179,317 (1.793) | fits |
| notice-every-5 | 984 | 0 | 179,356 (1.794) | fits |
| notice-every-6 | 986 | 0 | 172,309 (1.723) | fits |
| notice-every-7 | 986 | 0 | 176,385 (1.764) | fits |
| notice-burst-0 | 788 | 0 | 178,128 (1.781) | fits |
| notice-burst-1 | 792 | 0 | 177,725 (1.777) | fits |
| notice-burst-2 | 791 | 0 | 177,339 (1.773) | fits |
| notice-burst-3 | 794 | 0 | 178,623 (1.786) | fits |
| notice-burst-4 | 792 | 0 | 178,241 (1.782) | fits |
| notice-burst-5 | 777 | 0 | 177,736 (1.777) | fits |
| notice-burst-6 | 773 | 0 | 177,058 (1.771) | fits |
| notice-burst-7 | 791 | 0 | 176,398 (1.764) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 2.370 | 62 | 32 | 1 | within |
| notice-every-0 | 2.712 | 62 | 32 | 1 | within |
| notice-every-0 | 4.438 | 62 | 32 | 1 | within |
| notice-every-0 | 4.780 | 62 | 32 | 1 | within |
| notice-every-0 | 6.191 | 62 | 32 | 1 | within |
| notice-every-0 | 6.531 | 62 | 32 | 1 | within |
| notice-every-0 | 8.173 | 62 | 32 | 1 | within |
| notice-every-0 | 8.512 | 62 | 32 | 1 | within |
| notice-every-0 | 3.045 | 62 | 32 | 1 | within |
| notice-every-0 | 3.381 | 62 | 32 | 1 | within |
| notice-every-0 | 5.104 | 62 | 32 | 1 | within |
| notice-every-0 | 5.439 | 62 | 32 | 1 | within |
| notice-every-0 | 6.856 | 62 | 32 | 1 | within |
| notice-every-0 | 7.189 | 62 | 32 | 1 | within |
| notice-every-0 | 8.832 | 62 | 32 | 1 | within |
| notice-every-0 | 9.162 | 62 | 32 | 1 | within |
| notice-every-0 | 10.386 | 62 | 32 | 1 | within |
| notice-every-0 | 10.723 | 62 | 32 | 1 | within |
| notice-every-0 | 11.035 | 62 | 32 | 1 | within |
| notice-every-0 | 11.364 | 62 | 32 | 1 | within |
| notice-every-0 | 12.316 | 62 | 32 | 1 | within |
| notice-every-0 | 12.659 | 62 | 32 | 1 | within |
| notice-every-0 | 12.978 | 62 | 32 | 1 | within |
| notice-every-0 | 13.311 | 62 | 32 | 1 | within |
| notice-every-0 | 14.351 | 62 | 32 | 1 | within |
| notice-every-0 | 14.693 | 62 | 32 | 1 | within |
| notice-every-0 | 15.009 | 62 | 32 | 1 | within |
| notice-every-0 | 15.338 | 62 | 32 | 1 | within |
| notice-every-0 | 16.264 | 62 | 32 | 1 | within |
| notice-every-0 | 16.602 | 62 | 32 | 1 | within |
| notice-every-0 | 16.915 | 62 | 32 | 1 | within |
| notice-every-0 | 17.246 | 62 | 32 | 1 | within |
| notice-every-0 | 18.165 | 62 | 32 | 1 | within |
| notice-every-0 | 18.507 | 62 | 32 | 1 | within |
| notice-every-0 | 18.822 | 62 | 32 | 1 | within |
| notice-every-0 | 19.155 | 62 | 32 | 1 | within |
| notice-every-0 | 20.270 | 62 | 32 | 1 | within |
| notice-every-0 | 20.566 | 62 | 32 | 1 | within |
| notice-every-0 | 20.903 | 62 | 32 | 1 | within |
| notice-every-0 | 21.239 | 62 | 32 | 1 | within |
| notice-every-1 | 3.689 | 62 | 32 | 1 | within |
| notice-every-1 | 4.033 | 62 | 32 | 1 | within |
| notice-every-1 | 4.358 | 62 | 32 | 1 | within |
| notice-every-1 | 4.690 | 62 | 32 | 1 | within |
| notice-every-1 | 5.691 | 62 | 32 | 1 | within |
| notice-every-1 | 6.030 | 62 | 32 | 1 | within |
| notice-every-1 | 7.676 | 62 | 32 | 1 | within |
| notice-every-1 | 8.015 | 62 | 32 | 1 | within |
| notice-every-1 | 6.357 | 62 | 32 | 1 | within |
| notice-every-1 | 6.689 | 62 | 32 | 1 | within |
| notice-every-1 | 8.335 | 62 | 32 | 1 | within |
| notice-every-1 | 8.665 | 62 | 32 | 1 | within |
| notice-every-1 | 9.651 | 62 | 32 | 1 | within |
| notice-every-1 | 9.988 | 62 | 32 | 1 | within |
| notice-every-1 | 10.309 | 62 | 32 | 1 | within |
| notice-every-1 | 10.639 | 62 | 32 | 1 | within |
| notice-every-1 | 11.698 | 62 | 32 | 1 | within |
| notice-every-1 | 12.036 | 62 | 32 | 1 | within |
| notice-every-1 | 12.348 | 62 | 32 | 1 | within |
| notice-every-1 | 12.677 | 62 | 32 | 1 | within |
| notice-every-1 | 13.626 | 62 | 32 | 1 | within |
| notice-every-1 | 13.969 | 62 | 32 | 1 | within |
| notice-every-1 | 14.288 | 62 | 32 | 1 | within |
| notice-every-1 | 14.621 | 62 | 32 | 1 | within |
| notice-every-1 | 15.799 | 62 | 32 | 1 | within |
| notice-every-1 | 16.140 | 62 | 32 | 1 | within |
| notice-every-1 | 16.456 | 62 | 32 | 1 | within |
| notice-every-1 | 16.785 | 62 | 32 | 1 | within |
| notice-every-1 | 17.709 | 62 | 32 | 1 | within |
| notice-every-1 | 18.047 | 62 | 32 | 1 | within |
| notice-every-1 | 18.360 | 62 | 32 | 1 | within |
| notice-every-1 | 18.691 | 62 | 32 | 1 | within |
| notice-every-1 | 20.672 | 62 | 32 | 1 | within |
| notice-every-1 | 24.581 | 62 | 32 | 1 | within |
| notice-every-1 | 24.908 | 62 | 32 | 1 | within |
| notice-every-1 | 25.241 | 62 | 32 | 1 | within |
| notice-every-1 | 25.544 | 62 | 32 | 1 | within |
| notice-every-1 | 26.659 | 62 | 32 | 1 | within |
| notice-every-1 | 27.000 | 62 | 32 | 1 | within |
| notice-every-1 | 27.337 | 62 | 32 | 1 | within |
| notice-every-2 | 4.445 | 62 | 32 | 1 | within |
| notice-every-2 | 4.786 | 62 | 32 | 1 | within |
| notice-every-2 | 2.376 | 62 | 32 | 1 | within |
| notice-every-2 | 2.723 | 62 | 32 | 1 | within |
| notice-every-2 | 6.198 | 62 | 32 | 1 | within |
| notice-every-2 | 6.539 | 62 | 32 | 1 | within |
| notice-every-2 | 8.488 | 62 | 32 | 1 | within |
| notice-every-2 | 8.827 | 62 | 32 | 1 | within |
| notice-every-2 | 3.054 | 62 | 32 | 1 | within |
| notice-every-2 | 3.391 | 62 | 32 | 1 | within |
| notice-every-2 | 5.112 | 62 | 32 | 1 | within |
| notice-every-2 | 5.447 | 62 | 32 | 1 | within |
| notice-every-2 | 6.864 | 62 | 32 | 1 | within |
| notice-every-2 | 7.197 | 62 | 32 | 1 | within |
| notice-every-2 | 9.147 | 62 | 32 | 1 | within |
| notice-every-2 | 9.477 | 62 | 32 | 1 | within |
| notice-every-2 | 10.193 | 62 | 32 | 1 | within |
| notice-every-2 | 10.530 | 62 | 32 | 1 | within |
| notice-every-2 | 10.842 | 62 | 32 | 1 | within |
| notice-every-2 | 11.172 | 62 | 32 | 1 | within |
| notice-every-2 | 12.364 | 62 | 32 | 1 | within |
| notice-every-2 | 12.707 | 62 | 32 | 1 | within |
| notice-every-2 | 13.025 | 62 | 32 | 1 | within |
| notice-every-2 | 13.359 | 62 | 32 | 1 | within |
| notice-every-2 | 14.398 | 62 | 32 | 1 | within |
| notice-every-2 | 14.741 | 62 | 32 | 1 | within |
| notice-every-2 | 15.056 | 62 | 32 | 1 | within |
| notice-every-2 | 15.386 | 62 | 32 | 1 | within |
| notice-every-2 | 16.312 | 62 | 32 | 1 | within |
| notice-every-2 | 16.650 | 62 | 32 | 1 | within |
| notice-every-2 | 16.963 | 62 | 32 | 1 | within |
| notice-every-2 | 17.294 | 62 | 32 | 1 | within |
| notice-every-2 | 18.213 | 62 | 32 | 1 | within |
| notice-every-2 | 18.555 | 62 | 32 | 1 | within |
| notice-every-2 | 18.870 | 62 | 32 | 1 | within |
| notice-every-2 | 19.203 | 62 | 32 | 1 | within |
| notice-every-2 | 20.318 | 62 | 32 | 1 | within |
| notice-every-2 | 20.614 | 62 | 32 | 1 | within |
| notice-every-2 | 20.951 | 62 | 32 | 1 | within |
| notice-every-2 | 21.287 | 62 | 32 | 1 | within |
| notice-every-3 | 2.370 | 62 | 32 | 1 | within |
| notice-every-3 | 2.712 | 62 | 32 | 1 | within |
| notice-every-3 | 4.437 | 62 | 32 | 1 | within |
| notice-every-3 | 4.779 | 62 | 32 | 1 | within |
| notice-every-3 | 6.190 | 62 | 32 | 1 | within |
| notice-every-3 | 6.530 | 62 | 32 | 1 | within |
| notice-every-3 | 8.172 | 62 | 32 | 1 | within |
| notice-every-3 | 8.511 | 62 | 32 | 1 | within |
| notice-every-3 | 3.045 | 62 | 32 | 1 | within |
| notice-every-3 | 3.381 | 62 | 32 | 1 | within |
| notice-every-3 | 5.103 | 62 | 32 | 1 | within |
| notice-every-3 | 5.439 | 62 | 32 | 1 | within |
| notice-every-3 | 6.855 | 62 | 32 | 1 | within |
| notice-every-3 | 7.189 | 62 | 32 | 1 | within |
| notice-every-3 | 8.831 | 62 | 32 | 1 | within |
| notice-every-3 | 9.161 | 62 | 32 | 1 | within |
| notice-every-3 | 10.385 | 62 | 32 | 1 | within |
| notice-every-3 | 10.723 | 62 | 32 | 1 | within |
| notice-every-3 | 11.035 | 62 | 32 | 1 | within |
| notice-every-3 | 11.364 | 62 | 32 | 1 | within |
| notice-every-3 | 12.315 | 62 | 32 | 1 | within |
| notice-every-3 | 12.658 | 62 | 32 | 1 | within |
| notice-every-3 | 12.977 | 62 | 32 | 1 | within |
| notice-every-3 | 13.310 | 62 | 32 | 1 | within |
| notice-every-3 | 14.350 | 62 | 32 | 1 | within |
| notice-every-3 | 14.692 | 62 | 32 | 1 | within |
| notice-every-3 | 15.008 | 62 | 32 | 1 | within |
| notice-every-3 | 15.337 | 62 | 32 | 1 | within |
| notice-every-3 | 16.263 | 62 | 32 | 1 | within |
| notice-every-3 | 16.601 | 62 | 32 | 1 | within |
| notice-every-3 | 16.914 | 62 | 32 | 1 | within |
| notice-every-3 | 17.245 | 62 | 32 | 1 | within |
| notice-every-3 | 18.164 | 62 | 32 | 1 | within |
| notice-every-3 | 18.506 | 62 | 32 | 1 | within |
| notice-every-3 | 18.821 | 62 | 32 | 1 | within |
| notice-every-3 | 19.154 | 62 | 32 | 1 | within |
| notice-every-3 | 20.269 | 62 | 32 | 1 | within |
| notice-every-3 | 20.565 | 62 | 32 | 1 | within |
| notice-every-3 | 20.901 | 62 | 32 | 1 | within |
| notice-every-3 | 21.238 | 62 | 32 | 1 | within |
| notice-every-4 | 6.453 | 62 | 32 | 2 | within |
| notice-every-4 | 6.789 | 62 | 32 | 2 | within |
| notice-every-4 | 4.124 | 62 | 32 | 2 | within |
| notice-every-4 | 4.462 | 62 | 32 | 2 | within |
| notice-every-4 | 8.168 | 62 | 32 | 2 | within |
| notice-every-4 | 8.510 | 62 | 32 | 2 | within |
| notice-every-4 | 2.691 | 62 | 32 | 2 | within |
| notice-every-4 | 3.043 | 62 | 32 | 2 | within |
| notice-every-4 | 3.376 | 62 | 32 | 2 | within |
| notice-every-4 | 3.713 | 62 | 32 | 2 | within |
| notice-every-4 | 4.785 | 62 | 32 | 2 | within |
| notice-every-4 | 5.120 | 62 | 32 | 2 | within |
| notice-every-4 | 7.114 | 62 | 32 | 2 | within |
| notice-every-4 | 7.447 | 62 | 32 | 2 | within |
| notice-every-4 | 8.831 | 62 | 32 | 2 | within |
| notice-every-4 | 9.161 | 62 | 32 | 2 | within |
| notice-every-4 | 10.146 | 62 | 32 | 2 | within |
| notice-every-4 | 10.483 | 62 | 32 | 2 | within |
| notice-every-4 | 10.795 | 62 | 32 | 2 | within |
| notice-every-4 | 11.125 | 62 | 32 | 2 | within |
| notice-every-4 | 12.315 | 62 | 32 | 2 | within |
| notice-every-4 | 12.658 | 62 | 32 | 2 | within |
| notice-every-4 | 12.977 | 62 | 32 | 2 | within |
| notice-every-4 | 13.310 | 62 | 32 | 2 | within |
| notice-every-4 | 14.350 | 62 | 32 | 2 | within |
| notice-every-4 | 14.692 | 62 | 32 | 2 | within |
| notice-every-4 | 15.008 | 62 | 32 | 2 | within |
| notice-every-4 | 15.337 | 62 | 32 | 2 | within |
| notice-every-4 | 16.263 | 62 | 32 | 2 | within |
| notice-every-4 | 16.601 | 62 | 32 | 2 | within |
| notice-every-4 | 16.914 | 62 | 32 | 2 | within |
| notice-every-4 | 17.245 | 62 | 32 | 2 | within |
| notice-every-4 | 18.164 | 62 | 32 | 2 | within |
| notice-every-4 | 18.506 | 62 | 32 | 2 | within |
| notice-every-4 | 18.821 | 62 | 32 | 2 | within |
| notice-every-4 | 19.154 | 62 | 32 | 2 | within |
| notice-every-4 | 20.269 | 62 | 32 | 2 | within |
| notice-every-4 | 20.566 | 62 | 32 | 2 | within |
| notice-every-4 | 20.902 | 62 | 32 | 2 | within |
| notice-every-4 | 21.239 | 62 | 32 | 2 | within |
| notice-every-5 | 4.461 | 62 | 32 | 1 | within |
| notice-every-5 | 4.802 | 62 | 32 | 1 | within |
| notice-every-5 | 6.537 | 62 | 32 | 1 | within |
| notice-every-5 | 6.876 | 62 | 32 | 1 | within |
| notice-every-5 | 2.372 | 62 | 32 | 1 | within |
| notice-every-5 | 2.719 | 62 | 32 | 1 | within |
| notice-every-5 | 8.251 | 62 | 32 | 1 | within |
| notice-every-5 | 8.591 | 62 | 32 | 1 | within |
| notice-every-5 | 3.051 | 62 | 32 | 1 | within |
| notice-every-5 | 3.388 | 62 | 32 | 1 | within |
| notice-every-5 | 5.127 | 62 | 32 | 1 | within |
| notice-every-5 | 5.463 | 62 | 32 | 1 | within |
| notice-every-5 | 7.200 | 62 | 32 | 1 | within |
| notice-every-5 | 7.534 | 62 | 32 | 1 | within |
| notice-every-5 | 8.911 | 62 | 32 | 1 | within |
| notice-every-5 | 9.242 | 62 | 32 | 1 | within |
| notice-every-5 | 10.469 | 62 | 32 | 1 | within |
| notice-every-5 | 10.806 | 62 | 32 | 1 | within |
| notice-every-5 | 11.119 | 62 | 32 | 1 | within |
| notice-every-5 | 11.449 | 62 | 32 | 1 | within |
| notice-every-5 | 12.400 | 62 | 32 | 1 | within |
| notice-every-5 | 12.743 | 62 | 32 | 1 | within |
| notice-every-5 | 13.062 | 62 | 32 | 1 | within |
| notice-every-5 | 13.396 | 62 | 32 | 1 | within |
| notice-every-5 | 14.436 | 62 | 32 | 1 | within |
| notice-every-5 | 14.780 | 62 | 32 | 1 | within |
| notice-every-5 | 15.095 | 62 | 32 | 1 | within |
| notice-every-5 | 15.425 | 62 | 32 | 1 | within |
| notice-every-5 | 16.351 | 62 | 32 | 1 | within |
| notice-every-5 | 16.690 | 62 | 32 | 1 | within |
| notice-every-5 | 17.003 | 62 | 32 | 1 | within |
| notice-every-5 | 17.335 | 62 | 32 | 1 | within |
| notice-every-5 | 18.254 | 62 | 32 | 1 | within |
| notice-every-5 | 18.596 | 62 | 32 | 1 | within |
| notice-every-5 | 18.912 | 62 | 32 | 1 | within |
| notice-every-5 | 19.245 | 62 | 32 | 1 | within |
| notice-every-5 | 20.360 | 62 | 32 | 1 | within |
| notice-every-5 | 20.656 | 62 | 32 | 1 | within |
| notice-every-5 | 20.993 | 62 | 32 | 1 | within |
| notice-every-5 | 21.330 | 62 | 32 | 1 | within |
| notice-every-6 | 4.444 | 62 | 32 | 1 | within |
| notice-every-6 | 4.786 | 62 | 32 | 1 | within |
| notice-every-6 | 6.198 | 62 | 32 | 1 | within |
| notice-every-6 | 6.537 | 62 | 32 | 1 | within |
| notice-every-6 | 2.376 | 62 | 32 | 1 | within |
| notice-every-6 | 2.722 | 62 | 32 | 1 | within |
| notice-every-6 | 8.486 | 62 | 32 | 1 | within |
| notice-every-6 | 8.826 | 62 | 32 | 1 | within |
| notice-every-6 | 3.055 | 62 | 32 | 1 | within |
| notice-every-6 | 3.391 | 62 | 32 | 1 | within |
| notice-every-6 | 5.111 | 62 | 32 | 1 | within |
| notice-every-6 | 5.446 | 62 | 32 | 1 | within |
| notice-every-6 | 6.861 | 62 | 32 | 1 | within |
| notice-every-6 | 7.195 | 62 | 32 | 1 | within |
| notice-every-6 | 9.146 | 62 | 32 | 1 | within |
| notice-every-6 | 9.476 | 62 | 32 | 1 | within |
| notice-every-6 | 10.192 | 62 | 32 | 1 | within |
| notice-every-6 | 10.530 | 62 | 32 | 1 | within |
| notice-every-6 | 10.842 | 62 | 32 | 1 | within |
| notice-every-6 | 11.172 | 62 | 32 | 1 | within |
| notice-every-6 | 12.364 | 62 | 32 | 1 | within |
| notice-every-6 | 12.708 | 62 | 32 | 1 | within |
| notice-every-6 | 13.026 | 62 | 32 | 1 | within |
| notice-every-6 | 13.360 | 62 | 32 | 1 | within |
| notice-every-6 | 14.400 | 62 | 32 | 1 | within |
| notice-every-6 | 14.743 | 62 | 32 | 1 | within |
| notice-every-6 | 15.059 | 62 | 32 | 1 | within |
| notice-every-6 | 15.389 | 62 | 32 | 1 | within |
| notice-every-6 | 16.315 | 62 | 32 | 1 | within |
| notice-every-6 | 16.654 | 62 | 32 | 1 | within |
| notice-every-6 | 16.967 | 62 | 32 | 1 | within |
| notice-every-6 | 17.298 | 62 | 32 | 1 | within |
| notice-every-6 | 18.218 | 62 | 32 | 1 | within |
| notice-every-6 | 18.560 | 62 | 32 | 1 | within |
| notice-every-6 | 18.876 | 62 | 32 | 1 | within |
| notice-every-6 | 19.209 | 62 | 32 | 1 | within |
| notice-every-6 | 20.324 | 62 | 32 | 1 | within |
| notice-every-6 | 20.620 | 62 | 32 | 1 | within |
| notice-every-6 | 20.957 | 62 | 32 | 1 | within |
| notice-every-6 | 21.294 | 62 | 32 | 1 | within |
| notice-every-7 | 4.446 | 62 | 32 | 1 | within |
| notice-every-7 | 4.787 | 62 | 32 | 1 | within |
| notice-every-7 | 6.451 | 62 | 32 | 1 | within |
| notice-every-7 | 6.791 | 62 | 32 | 1 | within |
| notice-every-7 | 2.372 | 62 | 32 | 1 | within |
| notice-every-7 | 2.719 | 62 | 32 | 1 | within |
| notice-every-7 | 8.434 | 62 | 32 | 1 | within |
| notice-every-7 | 8.774 | 62 | 32 | 1 | within |
| notice-every-7 | 3.051 | 62 | 32 | 1 | within |
| notice-every-7 | 3.388 | 62 | 32 | 1 | within |
| notice-every-7 | 5.113 | 62 | 32 | 1 | within |
| notice-every-7 | 5.448 | 62 | 32 | 1 | within |
| notice-every-7 | 7.115 | 62 | 32 | 1 | within |
| notice-every-7 | 7.448 | 62 | 32 | 1 | within |
| notice-every-7 | 9.094 | 62 | 32 | 1 | within |
| notice-every-7 | 9.425 | 62 | 32 | 1 | within |
| notice-every-7 | 10.404 | 62 | 32 | 1 | within |
| notice-every-7 | 10.741 | 62 | 32 | 1 | within |
| notice-every-7 | 11.053 | 62 | 32 | 1 | within |
| notice-every-7 | 11.384 | 62 | 32 | 1 | within |
| notice-every-7 | 12.334 | 62 | 32 | 1 | within |
| notice-every-7 | 12.678 | 62 | 32 | 1 | within |
| notice-every-7 | 12.996 | 62 | 32 | 1 | within |
| notice-every-7 | 13.330 | 62 | 32 | 1 | within |
| notice-every-7 | 14.370 | 62 | 32 | 1 | within |
| notice-every-7 | 14.714 | 62 | 32 | 1 | within |
| notice-every-7 | 15.029 | 62 | 32 | 1 | within |
| notice-every-7 | 15.359 | 62 | 32 | 1 | within |
| notice-every-7 | 16.286 | 62 | 32 | 1 | within |
| notice-every-7 | 16.624 | 62 | 32 | 1 | within |
| notice-every-7 | 16.938 | 62 | 32 | 1 | within |
| notice-every-7 | 17.269 | 62 | 32 | 1 | within |
| notice-every-7 | 18.421 | 62 | 32 | 1 | within |
| notice-every-7 | 18.764 | 62 | 32 | 1 | within |
| notice-every-7 | 19.079 | 62 | 32 | 1 | within |
| notice-every-7 | 19.412 | 62 | 32 | 1 | within |
| notice-every-7 | 20.297 | 62 | 32 | 1 | within |
| notice-every-7 | 20.593 | 62 | 32 | 1 | within |
| notice-every-7 | 20.931 | 62 | 32 | 1 | within |
| notice-every-7 | 21.268 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.839 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.171 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.303 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.637 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.958 | 62 | 32 | 1 | within |
| notice-burst-0 | 6.291 | 62 | 32 | 1 | within |
| notice-burst-0 | 8.381 | 62 | 32 | 1 | within |
| notice-burst-0 | 13.649 | 62 | 32 | 1 | within |
| notice-burst-0 | 17.347 | 62 | 32 | 1 | within |
| notice-burst-0 | 21.849 | 62 | 32 | 1 | within |
| notice-burst-0 | 22.184 | 62 | 32 | 1 | within |
| notice-burst-0 | 22.516 | 62 | 32 | 1 | within |
| notice-burst-0 | 22.835 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.234 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.557 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.889 | 62 | 32 | 1 | within |
| notice-burst-0 | 24.210 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.283 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.604 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.935 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.327 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.695 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.037 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.393 | 62 | 32 | 1 | within |
| notice-burst-0 | 26.251 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.213 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.538 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.870 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.514 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.872 | 62 | 32 | 1 | within |
| notice-burst-0 | 28.180 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.349 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.674 | 62 | 32 | 1 | within |
| notice-burst-0 | 30.010 | 62 | 32 | 1 | within |
| notice-burst-0 | 30.324 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.252 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.560 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.853 | 62 | 32 | 1 | within |
| notice-burst-0 | 32.185 | 62 | 32 | 1 | within |
| notice-burst-0 | 33.202 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.838 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.170 | 62 | 32 | 1 | within |
| notice-burst-1 | 8.372 | 62 | 32 | 1 | within |
| notice-burst-1 | 13.648 | 62 | 32 | 1 | within |
| notice-burst-1 | 17.328 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.888 | 62 | 32 | 1 | within |
| notice-burst-1 | 22.224 | 62 | 32 | 1 | within |
| notice-burst-1 | 22.558 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.298 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.638 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.966 | 62 | 32 | 1 | within |
| notice-burst-1 | 6.303 | 62 | 32 | 1 | within |
| notice-burst-1 | 22.879 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.277 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.601 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.932 | 62 | 32 | 1 | within |
| notice-burst-1 | 24.252 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.325 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.646 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.976 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.330 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.699 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.041 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.397 | 62 | 32 | 1 | within |
| notice-burst-1 | 26.292 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.491 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.505 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.860 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.820 | 62 | 32 | 1 | within |
| notice-burst-1 | 28.151 | 62 | 32 | 1 | within |
| notice-burst-1 | 28.462 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.395 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.721 | 62 | 32 | 1 | within |
| notice-burst-1 | 30.055 | 62 | 32 | 1 | within |
| notice-burst-1 | 30.369 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.297 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.605 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.898 | 62 | 32 | 1 | within |
| notice-burst-1 | 32.229 | 62 | 32 | 1 | within |
| notice-burst-1 | 33.474 | 62 | 32 | 1 | within |
| notice-burst-2 | 4.468 | 62 | 32 | 1 | within |
| notice-burst-2 | 4.806 | 62 | 32 | 1 | within |
| notice-burst-2 | 5.877 | 62 | 32 | 1 | within |
| notice-burst-2 | 6.209 | 62 | 32 | 1 | within |
| notice-burst-2 | 8.986 | 62 | 32 | 1 | within |
| notice-burst-2 | 12.685 | 62 | 32 | 1 | within |
| notice-burst-2 | 5.131 | 62 | 32 | 1 | within |
| notice-burst-2 | 5.468 | 62 | 32 | 1 | within |
| notice-burst-2 | 6.534 | 62 | 32 | 1 | within |
| notice-burst-2 | 6.866 | 62 | 32 | 1 | within |
| notice-burst-2 | 16.570 | 62 | 32 | 1 | within |
| notice-burst-2 | 20.373 | 62 | 32 | 1 | within |
| notice-burst-2 | 20.709 | 62 | 32 | 1 | within |
| notice-burst-2 | 21.041 | 62 | 32 | 1 | within |
| notice-burst-2 | 21.361 | 62 | 32 | 1 | within |
| notice-burst-2 | 23.404 | 62 | 32 | 1 | within |
| notice-burst-2 | 23.739 | 62 | 32 | 1 | within |
| notice-burst-2 | 24.073 | 62 | 32 | 1 | within |
| notice-burst-2 | 24.385 | 62 | 32 | 1 | within |
| notice-burst-2 | 25.631 | 62 | 32 | 1 | within |
| notice-burst-2 | 2.274 | 62 | 32 | 1 | within |
| notice-burst-2 | 2.637 | 62 | 32 | 1 | within |
| notice-burst-2 | 2.980 | 62 | 32 | 1 | within |
| notice-burst-2 | 3.336 | 62 | 32 | 1 | within |
| notice-burst-2 | 25.956 | 62 | 32 | 1 | within |
| notice-burst-2 | 26.293 | 62 | 32 | 1 | within |
| notice-burst-2 | 26.608 | 62 | 32 | 1 | within |
| notice-burst-2 | 27.319 | 62 | 32 | 1 | within |
| notice-burst-2 | 27.643 | 62 | 32 | 1 | within |
| notice-burst-2 | 27.977 | 62 | 32 | 1 | within |
| notice-burst-2 | 28.288 | 62 | 32 | 1 | within |
| notice-burst-2 | 29.461 | 62 | 32 | 1 | within |
| notice-burst-2 | 29.787 | 62 | 32 | 1 | within |
| notice-burst-2 | 30.122 | 62 | 32 | 1 | within |
| notice-burst-2 | 30.436 | 62 | 32 | 1 | within |
| notice-burst-2 | 31.364 | 62 | 32 | 1 | within |
| notice-burst-2 | 31.672 | 62 | 32 | 1 | within |
| notice-burst-2 | 31.965 | 62 | 32 | 1 | within |
| notice-burst-2 | 32.297 | 62 | 32 | 1 | within |
| notice-burst-2 | 33.315 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.327 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.660 | 62 | 32 | 1 | within |
| notice-burst-3 | 8.432 | 62 | 32 | 1 | within |
| notice-burst-3 | 13.703 | 62 | 32 | 1 | within |
| notice-burst-3 | 17.402 | 62 | 32 | 1 | within |
| notice-burst-3 | 21.925 | 62 | 32 | 1 | within |
| notice-burst-3 | 22.260 | 62 | 32 | 1 | within |
| notice-burst-3 | 22.594 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.867 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.209 | 62 | 32 | 1 | within |
| notice-burst-3 | 22.912 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.310 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.991 | 62 | 32 | 1 | within |
| notice-burst-3 | 6.331 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.631 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.963 | 62 | 32 | 1 | within |
| notice-burst-3 | 24.282 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.354 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.675 | 62 | 32 | 1 | within |
| notice-burst-3 | 26.006 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.339 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.708 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.050 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.406 | 62 | 32 | 1 | within |
| notice-burst-3 | 26.321 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.283 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.543 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.898 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.612 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.943 | 62 | 32 | 1 | within |
| notice-burst-3 | 28.255 | 62 | 32 | 1 | within |
| notice-burst-3 | 29.424 | 62 | 32 | 1 | within |
| notice-burst-3 | 29.749 | 62 | 32 | 1 | within |
| notice-burst-3 | 30.084 | 62 | 32 | 1 | within |
| notice-burst-3 | 30.398 | 62 | 32 | 1 | within |
| notice-burst-3 | 31.326 | 62 | 32 | 1 | within |
| notice-burst-3 | 31.633 | 62 | 32 | 1 | within |
| notice-burst-3 | 31.927 | 62 | 32 | 1 | within |
| notice-burst-3 | 32.257 | 62 | 32 | 1 | within |
| notice-burst-3 | 33.275 | 62 | 32 | 1 | within |
| notice-burst-4 | 8.702 | 62 | 32 | 1 | within |
| notice-burst-4 | 12.417 | 62 | 32 | 1 | within |
| notice-burst-4 | 17.870 | 62 | 32 | 1 | within |
| notice-burst-4 | 21.563 | 62 | 32 | 1 | within |
| notice-burst-4 | 21.901 | 62 | 32 | 1 | within |
| notice-burst-4 | 22.236 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.047 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.389 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.517 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.857 | 62 | 32 | 1 | within |
| notice-burst-4 | 6.185 | 62 | 32 | 1 | within |
| notice-burst-4 | 6.521 | 62 | 32 | 1 | within |
| notice-burst-4 | 22.559 | 62 | 32 | 1 | within |
| notice-burst-4 | 23.808 | 62 | 32 | 1 | within |
| notice-burst-4 | 24.142 | 62 | 32 | 1 | within |
| notice-burst-4 | 24.477 | 62 | 32 | 1 | within |
| notice-burst-4 | 24.797 | 62 | 32 | 1 | within |
| notice-burst-4 | 25.520 | 62 | 32 | 1 | within |
| notice-burst-4 | 25.841 | 62 | 32 | 1 | within |
| notice-burst-4 | 26.175 | 62 | 32 | 1 | within |
| notice-burst-4 | 2.527 | 62 | 32 | 1 | within |
| notice-burst-4 | 2.895 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.238 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.594 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.726 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.079 | 62 | 32 | 1 | within |
| notice-burst-4 | 26.485 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.432 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.756 | 62 | 32 | 1 | within |
| notice-burst-4 | 28.087 | 62 | 32 | 1 | within |
| notice-burst-4 | 28.398 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.331 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.656 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.991 | 62 | 32 | 1 | within |
| notice-burst-4 | 30.306 | 62 | 32 | 1 | within |
| notice-burst-4 | 31.467 | 62 | 32 | 1 | within |
| notice-burst-4 | 31.774 | 62 | 32 | 1 | within |
| notice-burst-4 | 32.068 | 62 | 32 | 1 | within |
| notice-burst-4 | 32.399 | 62 | 32 | 1 | within |
| notice-burst-4 | 33.420 | 62 | 32 | 1 | within |
| notice-burst-5 | 8.386 | 62 | 32 | 1 | within |
| notice-burst-5 | 13.662 | 62 | 32 | 1 | within |
| notice-burst-5 | 17.341 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.902 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.859 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.198 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.319 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.659 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.986 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.321 | 62 | 32 | 1 | within |
| notice-burst-5 | 22.238 | 62 | 32 | 1 | within |
| notice-burst-5 | 22.569 | 62 | 32 | 1 | within |
| notice-burst-5 | 22.888 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.287 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.610 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.941 | 62 | 32 | 1 | within |
| notice-burst-5 | 24.262 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.335 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.656 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.987 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.347 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.715 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.057 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.413 | 62 | 32 | 1 | within |
| notice-burst-5 | 26.302 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.263 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.532 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.887 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.592 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.923 | 62 | 32 | 1 | within |
| notice-burst-5 | 28.234 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.403 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.728 | 62 | 32 | 1 | within |
| notice-burst-5 | 30.063 | 62 | 32 | 1 | within |
| notice-burst-5 | 30.377 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.305 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.612 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.906 | 62 | 32 | 1 | within |
| notice-burst-5 | 32.236 | 62 | 32 | 1 | within |
| notice-burst-5 | 33.254 | 62 | 32 | 1 | within |
| notice-burst-6 | 8.291 | 62 | 32 | 0 | within |
| notice-burst-6 | 11.903 | 62 | 32 | 0 | within |
| notice-burst-6 | 1.660 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.005 | 62 | 32 | 0 | within |
| notice-burst-6 | 3.171 | 62 | 32 | 0 | within |
| notice-burst-6 | 3.508 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.128 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.469 | 62 | 32 | 0 | within |
| notice-burst-6 | 17.407 | 62 | 32 | 0 | within |
| notice-burst-6 | 21.101 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.794 | 62 | 32 | 0 | within |
| notice-burst-6 | 6.129 | 62 | 32 | 0 | within |
| notice-burst-6 | 21.437 | 62 | 32 | 0 | within |
| notice-burst-6 | 21.769 | 62 | 32 | 0 | within |
| notice-burst-6 | 22.089 | 62 | 32 | 0 | within |
| notice-burst-6 | 23.340 | 62 | 32 | 0 | within |
| notice-burst-6 | 23.674 | 62 | 32 | 0 | within |
| notice-burst-6 | 24.009 | 62 | 32 | 0 | within |
| notice-burst-6 | 24.320 | 62 | 32 | 0 | within |
| notice-burst-6 | 24.723 | 62 | 32 | 0 | within |
| notice-burst-6 | 25.040 | 62 | 32 | 0 | within |
| notice-burst-6 | 25.376 | 62 | 32 | 0 | within |
| notice-burst-6 | 3.844 | 62 | 32 | 0 | within |
| notice-burst-6 | 4.200 | 62 | 32 | 0 | within |
| notice-burst-6 | 25.696 | 62 | 32 | 0 | within |
| notice-burst-6 | 26.683 | 62 | 32 | 0 | within |
| notice-burst-6 | 27.007 | 62 | 32 | 0 | within |
| notice-burst-6 | 27.339 | 62 | 32 | 0 | within |
| notice-burst-6 | 27.651 | 62 | 32 | 0 | within |
| notice-burst-6 | 28.821 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.357 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.727 | 62 | 32 | 0 | within |
| notice-burst-6 | 29.147 | 62 | 32 | 0 | within |
| notice-burst-6 | 29.482 | 62 | 32 | 0 | within |
| notice-burst-6 | 29.797 | 62 | 32 | 0 | within |
| notice-burst-6 | 30.725 | 62 | 32 | 0 | within |
| notice-burst-6 | 31.033 | 62 | 32 | 0 | within |
| notice-burst-6 | 31.326 | 62 | 32 | 0 | within |
| notice-burst-6 | 31.658 | 62 | 32 | 0 | within |
| notice-burst-6 | 32.678 | 62 | 32 | 0 | within |
| notice-burst-7 | 2.320 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.662 | 62 | 32 | 1 | within |
| notice-burst-7 | 3.803 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.137 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.270 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.606 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.926 | 62 | 32 | 1 | within |
| notice-burst-7 | 6.258 | 62 | 32 | 1 | within |
| notice-burst-7 | 8.439 | 62 | 32 | 1 | within |
| notice-burst-7 | 13.714 | 62 | 32 | 1 | within |
| notice-burst-7 | 17.369 | 62 | 32 | 1 | within |
| notice-burst-7 | 21.797 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.132 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.465 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.784 | 62 | 32 | 1 | within |
| notice-burst-7 | 23.827 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.161 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.493 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.805 | 62 | 32 | 1 | within |
| notice-burst-7 | 25.529 | 62 | 32 | 1 | within |
| notice-burst-7 | 25.856 | 62 | 32 | 1 | within |
| notice-burst-7 | 26.190 | 62 | 32 | 1 | within |
| notice-burst-7 | 3.003 | 62 | 32 | 1 | within |
| notice-burst-7 | 3.361 | 62 | 32 | 1 | within |
| notice-burst-7 | 26.511 | 62 | 32 | 1 | within |
| notice-burst-7 | 27.461 | 62 | 32 | 1 | within |
| notice-burst-7 | 27.786 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.117 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.480 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.840 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.427 | 62 | 32 | 1 | within |
| notice-burst-7 | 29.360 | 62 | 32 | 1 | within |
| notice-burst-7 | 29.686 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.020 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.335 | 62 | 32 | 1 | within |
| notice-burst-7 | 31.263 | 62 | 32 | 1 | within |
| notice-burst-7 | 31.571 | 62 | 32 | 1 | within |
| notice-burst-7 | 31.864 | 62 | 32 | 1 | within |
| notice-burst-7 | 32.195 | 62 | 32 | 1 | within |
| notice-burst-7 | 33.441 | 62 | 32 | 1 | within |

Latest: 33.474 ms, notice-burst-1.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 302 | 165,401 (1.654) | 35,881 (0.359) |
| notice-every-1 | 302 | 67,502 (0.675) | 35,881 (0.359) |
| notice-every-2 | 302 | 165,115 (1.651) | 35,881 (0.359) |
| notice-every-3 | 302 | 165,340 (1.653) | 35,881 (0.359) |
| notice-every-4 | 302 | 168,799 (1.688) | 35,881 (0.359) |
| notice-every-5 | 302 | 58,504 (0.585) | 35,881 (0.359) |
| notice-every-6 | 302 | 165,165 (1.652) | 35,881 (0.359) |
| notice-every-7 | 302 | 165,208 (1.652) | 35,881 (0.359) |
| notice-burst-0 | 311 | 67,719 (0.677) | 35,881 (0.359) |
| notice-burst-1 | 311 | 67,502 (0.675) | 35,881 (0.359) |
| notice-burst-2 | 311 | 161,703 (1.617) | 35,881 (0.359) |
| notice-burst-3 | 311 | 67,612 (0.676) | 35,881 (0.359) |
| notice-burst-4 | 311 | 163,204 (1.632) | 35,881 (0.359) |
| notice-burst-5 | 311 | 67,445 (0.674) | 35,881 (0.359) |
| notice-burst-6 | 311 | 162,424 (1.624) | 35,881 (0.359) |
| notice-burst-7 | 311 | 162,344 (1.623) | 35,881 (0.359) |

Longest pass that carries a step: 168,799 CPU cycles (1.688 ms), notice-every-4; longest step: 35,881 (0.359 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 236,966 | 2.370 | 62 | 66 | fits | 145,139 | 400 | 0.110 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 271,198 | 2.712 | 62 | 66 | fits | 145,139 | 400 | 0.110 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 443,774 | 4.438 | 62 | 66 | fits | 165,401 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 478,028 | 4.780 | 62 | 66 | fits | 165,401 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 619,072 | 6.191 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 653,085 | 6.531 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 817,272 | 8.173 | 62 | 66 | fits | 141,069 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 851,205 | 8.512 | 62 | 66 | fits | 141,069 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 304,453 | 3.045 | 62 | 66 | fits | 145,139 | 400 | 0.110 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 338,140 | 3.381 | 62 | 66 | fits | 145,139 | 400 | 0.110 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 510,413 | 5.104 | 62 | 66 | fits | 165,401 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 543,939 | 5.439 | 62 | 66 | fits | 165,401 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 685,617 | 6.856 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 718,921 | 7.189 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 883,193 | 8.832 | 62 | 66 | fits | 141,069 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 916,187 | 9.162 | 62 | 66 | fits | 141,069 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,038,565 | 10.386 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,072,275 | 10.723 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 1,103,490 | 11.035 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,136,424 | 11.364 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,231,649 | 12.316 | 62 | 66 | fits | 140,998 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,265,916 | 12.659 | 62 | 66 | fits | 140,998 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,297,776 | 12.978 | 62 | 66 | fits | 140,998 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,331,091 | 13.311 | 62 | 66 | fits | 140,998 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,435,056 | 14.351 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,469,333 | 14.693 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,500,851 | 15.009 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,533,785 | 15.338 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,626,396 | 16.264 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,660,203 | 16.602 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,691,524 | 16.915 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,724,613 | 17.246 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,816,512 | 18.165 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,850,684 | 18.507 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,882,228 | 18.822 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,915,461 | 19.155 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,026,998 | 20.270 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,056,608 | 20.566 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,090,270 | 20.903 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,123,924 | 21.239 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 1,067,200 | 10.672 | 20 | 200 | fits | 176,963 | 135 | 0.514 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 1,398,679 | 13.987 | 20 | 20 | fits | 158,860 | 94 | 0.539 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 1,440,924 | 14.409 | 20 | 24 | fits | 62,449 | 40 | 0.590 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 1,178,848 | 11.788 | 20 | 50 | fits | 171,391 | 95 | 0.571 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 808,469 | 8.085 | 20 | 20 | fits | 161,359 | 119 | 0.592 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 218,833 | 2.188 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 328,087 | 3.281 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 368,927 | 3.689 | 62 | 66 | fits | 144,440 | 402 | 0.117 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 403,310 | 4.033 | 62 | 66 | fits | 144,440 | 402 | 0.117 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 435,834 | 4.358 | 62 | 66 | fits | 144,440 | 402 | 0.117 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 468,986 | 4.690 | 62 | 66 | fits | 144,440 | 402 | 0.117 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 569,061 | 5.691 | 62 | 66 | fits | 142,968 | 402 | 0.096 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 603,014 | 6.030 | 62 | 66 | fits | 142,968 | 402 | 0.096 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 767,621 | 7.676 | 62 | 66 | fits | 141,150 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 801,475 | 8.015 | 62 | 66 | fits | 141,150 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 635,651 | 6.357 | 62 | 66 | fits | 142,968 | 402 | 0.096 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 668,876 | 6.689 | 62 | 66 | fits | 142,968 | 402 | 0.096 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 833,477 | 8.335 | 62 | 66 | fits | 141,150 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 866,471 | 8.665 | 62 | 66 | fits | 141,150 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 965,053 | 9.651 | 62 | 66 | fits | 141,175 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 998,842 | 9.988 | 62 | 66 | fits | 141,175 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 1,030,892 | 10.309 | 62 | 66 | fits | 141,175 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 1,063,886 | 10.639 | 62 | 66 | fits | 141,175 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 1,169,754 | 11.698 | 62 | 66 | fits | 140,036 | 400 | 0.094 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 1,203,553 | 12.036 | 62 | 66 | fits | 140,036 | 400 | 0.094 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 1,234,768 | 12.348 | 62 | 66 | fits | 140,036 | 400 | 0.094 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 1,267,702 | 12.677 | 62 | 66 | fits | 140,036 | 400 | 0.094 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 1,362,628 | 13.626 | 62 | 66 | fits | 140,807 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 1,396,895 | 13.969 | 62 | 66 | fits | 140,807 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 1,428,755 | 14.288 | 62 | 66 | fits | 140,807 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 1,462,070 | 14.621 | 62 | 66 | fits | 140,807 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 1,579,862 | 15.799 | 62 | 66 | fits | 139,413 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 1,614,050 | 16.140 | 62 | 66 | fits | 139,413 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 1,645,568 | 16.456 | 62 | 66 | fits | 139,413 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 1,678,502 | 16.785 | 62 | 66 | fits | 139,413 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 1,770,919 | 17.709 | 62 | 66 | fits | 138,524 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 1,804,726 | 18.047 | 62 | 66 | fits | 138,524 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 1,836,047 | 18.360 | 62 | 66 | fits | 138,524 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 1,869,136 | 18.691 | 62 | 66 | fits | 138,524 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 2,067,182 | 20.672 | 62 | 66 | fits | 40,684 | 101 | 0.252 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 2,458,114 | 24.581 | 62 | 66 | fits | 138,404 | 399 | 0.107 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 2,490,772 | 24.908 | 62 | 66 | fits | 138,404 | 399 | 0.107 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 2,524,072 | 25.241 | 62 | 66 | fits | 138,404 | 399 | 0.107 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 2,554,390 | 25.544 | 62 | 66 | fits | 138,404 | 399 | 0.107 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 2,665,881 | 26.659 | 62 | 66 | fits | 104,772 | 300 | 0.099 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 2,700,030 | 27.000 | 62 | 66 | fits | 104,772 | 300 | 0.099 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 2,733,684 | 27.337 | 62 | 66 | fits | 104,772 | 300 | 0.099 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if1` | 1,073,645 | 10.736 | 20 | 200 | fits | 169,143 | 113 | 0.545 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 1,405,592 | 14.056 | 20 | 20 | fits | 159,397 | 92 | 0.547 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if1` | 1,448,232 | 14.482 | 20 | 24 | fits | 62,844 | 40 | 0.599 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 1,185,178 | 11.852 | 20 | 50 | fits | 171,276 | 94 | 0.571 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if1` | 822,734 | 8.227 | 20 | 20 | fits | 160,487 | 113 | 0.600 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 216,027 | 2.160 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if1` | 325,383 | 3.254 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 444,529 | 4.445 | 62 | 66 | fits | 165,115 | 402 | 0.109 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 478,625 | 4.786 | 62 | 66 | fits | 165,115 | 402 | 0.109 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 237,630 | 2.376 | 62 | 66 | fits | 145,977 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 272,251 | 2.723 | 62 | 66 | fits | 145,977 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 619,843 | 6.198 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 653,856 | 6.539 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 848,836 | 8.488 | 62 | 66 | fits | 140,954 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 882,719 | 8.827 | 62 | 66 | fits | 140,954 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 305,392 | 3.054 | 62 | 66 | fits | 145,977 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 339,079 | 3.391 | 62 | 66 | fits | 145,977 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 511,151 | 5.112 | 62 | 66 | fits | 165,115 | 402 | 0.109 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 544,677 | 5.447 | 62 | 66 | fits | 165,115 | 402 | 0.109 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 686,388 | 6.864 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 719,692 | 7.197 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 914,707 | 9.147 | 62 | 66 | fits | 140,954 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 947,701 | 9.477 | 62 | 66 | fits | 140,954 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 1,019,323 | 10.193 | 62 | 66 | fits | 139,443 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 1,053,033 | 10.530 | 62 | 66 | fits | 139,443 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 1,084,248 | 10.842 | 62 | 66 | fits | 139,443 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 1,117,182 | 11.172 | 62 | 66 | fits | 139,443 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 1,236,414 | 12.364 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 1,270,681 | 12.707 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 1,302,541 | 13.025 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 1,335,856 | 13.359 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 1,439,844 | 14.398 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 1,474,121 | 14.741 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 1,505,639 | 15.056 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 1,538,573 | 15.386 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 1,631,222 | 16.312 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 1,665,029 | 16.650 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 1,696,350 | 16.963 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 1,729,439 | 17.294 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 1,821,325 | 18.213 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 1,855,497 | 18.555 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 1,887,041 | 18.870 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 1,920,274 | 19.203 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 2,031,783 | 20.318 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 2,061,393 | 20.614 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 2,095,055 | 20.951 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 2,128,709 | 21.287 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if1` | 1,232,959 | 12.330 | 20 | 200 | fits | 164,528 | 107 | 0.553 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 1,399,365 | 13.994 | 20 | 20 | fits | 159,714 | 100 | 0.539 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if1` | 1,441,583 | 14.416 | 20 | 24 | fits | 62,422 | 40 | 0.592 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 1,173,216 | 11.732 | 20 | 50 | fits | 164,528 | 107 | 0.553 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if1` | 826,563 | 8.266 | 20 | 20 | fits | 188,021 | 116 | 0.603 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 218,879 | 2.189 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if1` | 328,199 | 3.282 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 236,971 | 2.370 | 62 | 66 | fits | 145,139 | 400 | 0.110 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 271,203 | 2.712 | 62 | 66 | fits | 145,139 | 400 | 0.110 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 443,685 | 4.437 | 62 | 66 | fits | 165,340 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 477,939 | 4.779 | 62 | 66 | fits | 165,340 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 619,001 | 6.190 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 653,014 | 6.530 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 817,183 | 8.172 | 62 | 66 | fits | 141,069 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 851,116 | 8.511 | 62 | 66 | fits | 141,069 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 304,458 | 3.045 | 62 | 66 | fits | 145,139 | 400 | 0.110 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 338,145 | 3.381 | 62 | 66 | fits | 145,139 | 400 | 0.110 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 510,324 | 5.103 | 62 | 66 | fits | 165,340 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 543,850 | 5.439 | 62 | 66 | fits | 165,340 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 685,546 | 6.855 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 718,850 | 7.189 | 62 | 66 | fits | 142,448 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 883,104 | 8.831 | 62 | 66 | fits | 141,069 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 916,098 | 9.161 | 62 | 66 | fits | 141,069 | 402 | 0.085 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 1,038,545 | 10.385 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 1,072,255 | 10.723 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 1,103,470 | 11.035 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 1,136,404 | 11.364 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 1,231,542 | 12.315 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 1,265,809 | 12.658 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 1,297,669 | 12.977 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 1,330,984 | 13.310 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 1,434,962 | 14.350 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 1,469,239 | 14.692 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 1,500,757 | 15.008 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 1,533,691 | 15.337 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 1,626,294 | 16.263 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 1,660,101 | 16.601 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 1,691,422 | 16.914 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 1,724,511 | 17.245 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 1,816,410 | 18.164 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 1,850,582 | 18.506 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 1,882,126 | 18.821 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 1,915,359 | 19.154 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 2,026,863 | 20.269 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 2,056,473 | 20.565 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 2,090,135 | 20.901 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 2,123,789 | 21.238 | 62 | 66 | fits | 134,236 | 398 | 0.080 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if1` | 1,042,464 | 10.425 | 20 | 200 | fits | 174,985 | 129 | 0.539 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 1,376,643 | 13.766 | 20 | 20 | fits | 166,516 | 85 | 0.566 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if1` | 1,420,820 | 14.208 | 20 | 24 | fits | 64,381 | 46 | 0.589 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 982,721 | 9.827 | 20 | 50 | fits | 174,985 | 129 | 0.539 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if1` | 625,485 | 6.255 | 20 | 20 | fits | 158,696 | 65 | 0.513 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 234,700 | 2.347 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if1` | 344,056 | 3.441 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 645,259 | 6.453 | 62 | 66 | fits | 142,312 | 400 | 0.094 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 678,888 | 6.789 | 62 | 66 | fits | 142,312 | 400 | 0.094 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 412,446 | 4.124 | 62 | 66 | fits | 140,288 | 403 | 0.049 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 446,156 | 4.462 | 62 | 66 | fits | 140,288 | 403 | 0.049 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 816,820 | 8.168 | 62 | 66 | fits | 141,435 | 402 | 0.087 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 850,986 | 8.510 | 62 | 66 | fits | 141,435 | 402 | 0.087 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 269,126 | 2.691 | 62 | 66 | fits | 168,799 | 400 | 0.124 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 304,346 | 3.043 | 62 | 66 | fits | 168,799 | 400 | 0.124 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 337,624 | 3.376 | 62 | 66 | fits | 168,799 | 400 | 0.124 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 371,311 | 3.713 | 62 | 66 | fits | 168,799 | 400 | 0.124 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 478,541 | 4.785 | 62 | 66 | fits | 140,288 | 403 | 0.049 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 511,997 | 5.120 | 62 | 66 | fits | 140,288 | 403 | 0.049 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 711,420 | 7.114 | 62 | 66 | fits | 142,312 | 400 | 0.094 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 744,724 | 7.447 | 62 | 66 | fits | 142,312 | 400 | 0.094 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 883,115 | 8.831 | 62 | 66 | fits | 141,435 | 402 | 0.087 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 916,109 | 9.161 | 62 | 66 | fits | 141,435 | 402 | 0.087 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 1,014,592 | 10.146 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 1,048,302 | 10.483 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 1,079,517 | 10.795 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 1,112,451 | 11.125 | 62 | 66 | fits | 140,004 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 1,231,543 | 12.315 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 1,265,810 | 12.658 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 1,297,670 | 12.977 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 1,330,985 | 13.310 | 62 | 66 | fits | 140,895 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 1,434,968 | 14.350 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 1,469,245 | 14.692 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 1,500,763 | 15.008 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 1,533,697 | 15.337 | 62 | 66 | fits | 139,851 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 1,626,308 | 16.263 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 1,660,115 | 16.601 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 1,691,436 | 16.914 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 1,724,525 | 17.245 | 62 | 66 | fits | 138,612 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 1,816,424 | 18.164 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 1,850,596 | 18.506 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 1,882,140 | 18.821 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 1,915,373 | 19.154 | 62 | 66 | fits | 139,117 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 2,026,877 | 20.269 | 62 | 66 | fits | 134,315 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 2,056,566 | 20.566 | 62 | 66 | fits | 134,315 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 2,090,228 | 20.902 | 62 | 66 | fits | 134,315 | 398 | 0.080 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 2,123,882 | 21.239 | 62 | 66 | fits | 134,315 | 398 | 0.080 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if1` | 1,066,528 | 10.665 | 20 | 200 | fits | 169,171 | 111 | 0.545 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 1,396,984 | 13.970 | 20 | 20 | fits | 157,302 | 89 | 0.537 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if1` | 1,467,815 | 14.678 | 20 | 24 | fits | 65,011 | 51 | 0.597 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 1,200,207 | 12.002 | 20 | 50 | fits | 171,388 | 93 | 0.587 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if1` | 815,589 | 8.156 | 20 | 20 | fits | 170,438 | 106 | 0.578 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 225,503 | 2.255 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if1` | 334,859 | 3.349 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 446,060 | 4.461 | 62 | 66 | fits | 143,617 | 403 | 0.101 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 480,206 | 4.802 | 62 | 66 | fits | 143,617 | 403 | 0.101 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 653,720 | 6.537 | 62 | 66 | fits | 142,519 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 687,608 | 6.876 | 62 | 66 | fits | 142,519 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 237,189 | 2.372 | 62 | 66 | fits | 146,141 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 271,881 | 2.719 | 62 | 66 | fits | 146,141 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 825,063 | 8.251 | 62 | 66 | fits | 140,920 | 402 | 0.086 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 859,135 | 8.591 | 62 | 66 | fits | 140,920 | 402 | 0.086 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 305,086 | 3.051 | 62 | 66 | fits | 146,141 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 338,773 | 3.388 | 62 | 66 | fits | 146,141 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 512,732 | 5.127 | 62 | 66 | fits | 143,617 | 403 | 0.101 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 546,258 | 5.463 | 62 | 66 | fits | 143,617 | 403 | 0.101 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 719,999 | 7.200 | 62 | 66 | fits | 142,519 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 753,373 | 7.534 | 62 | 66 | fits | 142,519 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 891,123 | 8.911 | 62 | 66 | fits | 140,920 | 402 | 0.086 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 924,187 | 9.242 | 62 | 66 | fits | 140,920 | 402 | 0.086 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 1,046,859 | 10.469 | 62 | 66 | fits | 140,144 | 400 | 0.095 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 1,080,639 | 10.806 | 62 | 66 | fits | 140,144 | 400 | 0.095 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 1,111,854 | 11.119 | 62 | 66 | fits | 140,144 | 400 | 0.095 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 1,144,858 | 11.449 | 62 | 66 | fits | 140,144 | 400 | 0.095 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 1,240,001 | 12.400 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 1,274,338 | 12.743 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 1,306,198 | 13.062 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 1,339,583 | 13.396 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 1,443,604 | 14.436 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 1,477,951 | 14.780 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 1,509,469 | 15.095 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 1,542,473 | 15.425 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 1,635,122 | 16.351 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 1,668,999 | 16.690 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 1,700,320 | 17.003 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 1,733,479 | 17.335 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 1,825,365 | 18.254 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 1,859,607 | 18.596 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 1,891,151 | 18.912 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 1,924,454 | 19.245 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 2,035,963 | 20.360 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 2,065,573 | 20.656 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 2,099,304 | 20.993 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 2,133,018 | 21.330 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if1` | 1,236,299 | 12.363 | 20 | 200 | fits | 161,720 | 75 | 0.564 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 1,397,945 | 13.979 | 20 | 20 | fits | 160,480 | 70 | 0.625 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if1` | 1,460,022 | 14.600 | 20 | 24 | fits | 82,281 | 53 | 0.565 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 1,014,836 | 10.148 | 20 | 50 | fits | 167,016 | 132 | 0.515 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if1` | 825,795 | 8.258 | 20 | 20 | fits | 160,070 | 113 | 0.601 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 230,294 | 2.303 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if1` | 339,576 | 3.396 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 444,432 | 4.444 | 62 | 66 | fits | 165,165 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 478,578 | 4.786 | 62 | 66 | fits | 165,165 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 619,797 | 6.198 | 62 | 66 | fits | 142,336 | 402 | 0.088 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 653,735 | 6.537 | 62 | 66 | fits | 142,336 | 402 | 0.088 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 237,556 | 2.376 | 62 | 66 | fits | 146,057 | 400 | 0.109 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 272,248 | 2.722 | 62 | 66 | fits | 146,057 | 400 | 0.109 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 848,618 | 8.486 | 62 | 66 | fits | 141,094 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 882,571 | 8.826 | 62 | 66 | fits | 141,094 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 305,453 | 3.055 | 62 | 66 | fits | 146,057 | 400 | 0.109 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 339,140 | 3.391 | 62 | 66 | fits | 146,057 | 400 | 0.109 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 511,104 | 5.111 | 62 | 66 | fits | 165,165 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 544,630 | 5.446 | 62 | 66 | fits | 165,165 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 686,126 | 6.861 | 62 | 66 | fits | 142,336 | 402 | 0.088 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 719,500 | 7.195 | 62 | 66 | fits | 142,336 | 402 | 0.088 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 914,559 | 9.146 | 62 | 66 | fits | 141,094 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 947,623 | 9.476 | 62 | 66 | fits | 141,094 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 1,019,230 | 10.192 | 62 | 66 | fits | 139,550 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 1,053,010 | 10.530 | 62 | 66 | fits | 139,550 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 1,084,225 | 10.842 | 62 | 66 | fits | 139,550 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,117,229 | 11.172 | 62 | 66 | fits | 139,550 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,236,425 | 12.364 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,270,762 | 12.708 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,302,622 | 13.026 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,336,007 | 13.360 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,439,998 | 14.400 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,474,345 | 14.743 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,505,863 | 15.059 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,538,867 | 15.389 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,631,483 | 16.315 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,665,360 | 16.654 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,696,681 | 16.967 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,729,840 | 17.298 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,821,767 | 18.218 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,856,009 | 18.560 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,887,553 | 18.876 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,920,856 | 19.209 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,032,357 | 20.324 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,061,967 | 20.620 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,095,698 | 20.957 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,129,412 | 21.294 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if1` | 1,074,777 | 10.748 | 20 | 200 | fits | 167,975 | 111 | 0.536 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 1,404,102 | 14.041 | 20 | 20 | fits | 158,759 | 93 | 0.543 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if1` | 1,446,104 | 14.461 | 20 | 24 | fits | 62,206 | 40 | 0.589 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 1,184,403 | 11.844 | 20 | 50 | fits | 169,369 | 89 | 0.569 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if1` | 825,034 | 8.250 | 20 | 20 | fits | 160,667 | 113 | 0.597 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 220,309 | 2.203 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if1` | 329,629 | 3.296 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 444,601 | 4.446 | 62 | 66 | fits | 165,208 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 478,747 | 4.787 | 62 | 66 | fits | 165,208 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 645,131 | 6.451 | 62 | 66 | fits | 142,569 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 679,069 | 6.791 | 62 | 66 | fits | 142,569 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 237,229 | 2.372 | 62 | 66 | fits | 146,141 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 271,921 | 2.719 | 62 | 66 | fits | 146,141 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 843,423 | 8.434 | 62 | 66 | fits | 141,144 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 877,426 | 8.774 | 62 | 66 | fits | 141,144 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 305,126 | 3.051 | 62 | 66 | fits | 146,141 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 338,813 | 3.388 | 62 | 66 | fits | 146,141 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 511,273 | 5.113 | 62 | 66 | fits | 165,208 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 544,799 | 5.448 | 62 | 66 | fits | 165,208 | 402 | 0.110 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 711,460 | 7.115 | 62 | 66 | fits | 142,569 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 744,834 | 7.448 | 62 | 66 | fits | 142,569 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 909,414 | 9.094 | 62 | 66 | fits | 141,144 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 942,478 | 9.425 | 62 | 66 | fits | 141,144 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 1,040,354 | 10.404 | 62 | 66 | fits | 139,958 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 1,074,134 | 10.741 | 62 | 66 | fits | 139,958 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 1,105,349 | 11.053 | 62 | 66 | fits | 139,958 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 1,138,353 | 11.384 | 62 | 66 | fits | 139,958 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 1,233,440 | 12.334 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 1,267,777 | 12.678 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 1,299,637 | 12.996 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 1,333,022 | 13.330 | 62 | 66 | fits | 141,035 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 1,437,043 | 14.370 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 1,471,390 | 14.714 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 1,502,908 | 15.029 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 1,535,912 | 15.359 | 62 | 66 | fits | 139,991 | 400 | 0.096 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 1,628,561 | 16.286 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 1,662,438 | 16.624 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 1,693,759 | 16.938 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 1,726,918 | 17.269 | 62 | 66 | fits | 138,752 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 1,842,111 | 18.421 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 1,876,353 | 18.764 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 1,907,897 | 19.079 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 1,941,200 | 19.412 | 62 | 66 | fits | 139,257 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 2,029,724 | 20.297 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 2,059,334 | 20.593 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 2,093,065 | 20.931 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 2,126,779 | 21.268 | 62 | 66 | fits | 134,365 | 398 | 0.083 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if1` | 1,247,623 | 12.476 | 20 | 200 | fits | 173,936 | 97 | 0.566 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 1,407,073 | 14.071 | 20 | 20 | fits | 157,807 | 95 | 0.531 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if1` | 1,449,429 | 14.494 | 20 | 24 | fits | 62,560 | 40 | 0.593 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 1,187,880 | 11.879 | 20 | 50 | fits | 173,936 | 97 | 0.566 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if1` | 825,134 | 8.251 | 20 | 20 | fits | 160,359 | 113 | 0.599 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 213,226 | 2.132 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if1` | 322,544 | 3.225 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 383,905 | 3.839 | 62 | 66 | fits | 146,880 | 402 | 0.060 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 417,103 | 4.171 | 62 | 66 | fits | 146,880 | 402 | 0.060 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 530,267 | 5.303 | 62 | 66 | fits | 138,613 | 403 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 563,735 | 5.637 | 62 | 66 | fits | 138,613 | 403 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 595,825 | 5.958 | 62 | 66 | fits | 138,613 | 403 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 629,076 | 6.291 | 62 | 66 | fits | 138,613 | 403 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 838,089 | 8.381 | 62 | 66 | fits | 43,560 | 101 | 0.293 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 1,364,938 | 13.649 | 62 | 66 | fits | 45,028 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 1,734,731 | 17.347 | 62 | 66 | fits | 43,856 | 100 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 2,184,944 | 21.849 | 62 | 66 | fits | 141,525 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 2,218,398 | 22.184 | 62 | 66 | fits | 141,525 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 2,251,599 | 22.516 | 62 | 66 | fits | 141,525 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 2,283,475 | 22.835 | 62 | 66 | fits | 141,525 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 2,323,395 | 23.234 | 62 | 66 | fits | 137,186 | 401 | 0.051 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 2,355,716 | 23.557 | 62 | 66 | fits | 137,186 | 401 | 0.051 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 2,388,929 | 23.889 | 62 | 66 | fits | 137,186 | 401 | 0.051 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 2,420,977 | 24.210 | 62 | 66 | fits | 137,186 | 401 | 0.051 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 2,528,286 | 25.283 | 62 | 66 | fits | 139,530 | 401 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 2,560,359 | 25.604 | 62 | 66 | fits | 139,530 | 401 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 2,593,500 | 25.935 | 62 | 66 | fits | 139,530 | 401 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 232,700 | 2.327 | 62 | 66 | fits | 178,128 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 269,520 | 2.695 | 62 | 66 | fits | 178,128 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 303,720 | 3.037 | 62 | 66 | fits | 178,128 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 339,345 | 3.393 | 62 | 66 | fits | 178,128 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 2,625,064 | 26.251 | 62 | 66 | fits | 139,530 | 401 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 2,721,326 | 27.213 | 62 | 66 | fits | 138,515 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 2,753,819 | 27.538 | 62 | 66 | fits | 138,515 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 2,786,960 | 27.870 | 62 | 66 | fits | 138,515 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 451,370 | 4.514 | 62 | 66 | fits | 146,880 | 402 | 0.060 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 487,161 | 4.872 | 62 | 66 | fits | 146,880 | 402 | 0.060 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,817,971 | 28.180 | 62 | 66 | fits | 138,515 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,934,891 | 29.349 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,967,450 | 29.674 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 3,000,969 | 30.010 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 3,032,400 | 30.324 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 3,125,228 | 31.252 | 62 | 66 | fits | 134,997 | 399 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 3,155,982 | 31.560 | 62 | 66 | fits | 134,997 | 399 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 3,185,323 | 31.853 | 62 | 66 | fits | 134,997 | 399 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 3,218,452 | 32.185 | 62 | 66 | fits | 134,997 | 399 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 3,320,152 | 33.202 | 62 | 66 | fits | 41,476 | 102 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 1,323,783 | 13.238 | 20 | 200 | fits | 166,064 | 113 | 0.561 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,466,661 | 14.667 | 20 | 20 | fits | 163,146 | 87 | 0.512 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 1,524,132 | 15.241 | 20 | 24 | fits | 77,675 | 52 | 0.538 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 1,264,040 | 12.640 | 20 | 50 | fits | 166,064 | 113 | 0.561 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 661,236 | 6.612 | 20 | 20 | fits | 155,758 | 60 | 0.465 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 383,835 | 3.838 | 62 | 66 | fits | 145,930 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 417,033 | 4.170 | 62 | 66 | fits | 145,930 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 837,175 | 8.372 | 62 | 66 | fits | 43,988 | 103 | 0.295 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,364,808 | 13.648 | 62 | 66 | fits | 45,162 | 102 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 1,732,838 | 17.328 | 62 | 66 | fits | 43,619 | 100 | 0.299 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 2,188,811 | 21.888 | 62 | 66 | fits | 141,988 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 2,222,420 | 22.224 | 62 | 66 | fits | 141,988 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 2,255,774 | 22.558 | 62 | 66 | fits | 141,988 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 529,802 | 5.298 | 62 | 66 | fits | 141,370 | 403 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 563,805 | 5.638 | 62 | 66 | fits | 141,370 | 403 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 596,571 | 5.966 | 62 | 66 | fits | 141,370 | 403 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 630,258 | 6.303 | 62 | 66 | fits | 141,370 | 403 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 2,287,878 | 22.879 | 62 | 66 | fits | 141,988 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 2,327,730 | 23.277 | 62 | 66 | fits | 137,048 | 401 | 0.047 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 2,360,051 | 23.601 | 62 | 66 | fits | 137,048 | 401 | 0.047 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 2,393,194 | 23.932 | 62 | 66 | fits | 137,048 | 401 | 0.047 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 2,425,242 | 24.252 | 62 | 66 | fits | 137,048 | 401 | 0.047 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 2,532,503 | 25.325 | 62 | 66 | fits | 139,522 | 401 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 2,564,576 | 25.646 | 62 | 66 | fits | 139,522 | 401 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 2,597,647 | 25.976 | 62 | 66 | fits | 139,522 | 401 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 233,042 | 2.330 | 62 | 66 | fits | 177,725 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 269,862 | 2.699 | 62 | 66 | fits | 177,725 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 304,062 | 3.041 | 62 | 66 | fits | 177,725 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 339,687 | 3.397 | 62 | 66 | fits | 177,725 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 2,629,211 | 26.292 | 62 | 66 | fits | 139,522 | 401 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 2,749,096 | 27.491 | 62 | 66 | fits | 138,905 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 450,494 | 4.505 | 62 | 66 | fits | 145,930 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 485,975 | 4.860 | 62 | 66 | fits | 145,930 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 2,782,006 | 27.820 | 62 | 66 | fits | 138,905 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 2,815,077 | 28.151 | 62 | 66 | fits | 138,905 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 2,846,166 | 28.462 | 62 | 66 | fits | 138,905 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 2,939,510 | 29.395 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,972,069 | 29.721 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 3,005,518 | 30.055 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 3,036,949 | 30.369 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 3,129,750 | 31.297 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 3,160,504 | 31.605 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 3,189,845 | 31.898 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 3,222,914 | 32.229 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 3,347,442 | 33.474 | 62 | 66 | fits | 41,476 | 102 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if1` | 1,463,164 | 14.632 | 20 | 200 | fits | 159,422 | 73 | 0.579 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 1,442,896 | 14.429 | 20 | 20 | fits | 159,422 | 73 | 0.579 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if1` | 1,517,693 | 15.177 | 20 | 24 | fits | 95,001 | 65 | 0.504 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 1,243,999 | 12.440 | 20 | 50 | fits | 158,366 | 118 | 0.554 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if1` | 650,545 | 6.505 | 20 | 20 | fits | 155,758 | 60 | 0.465 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 446,758 | 4.468 | 62 | 66 | fits | 165,802 | 411 | 0.111 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 480,621 | 4.806 | 62 | 66 | fits | 165,802 | 411 | 0.111 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 587,662 | 5.877 | 62 | 66 | fits | 140,619 | 402 | 0.043 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 620,939 | 6.209 | 62 | 66 | fits | 140,619 | 402 | 0.043 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 898,564 | 8.986 | 62 | 66 | fits | 44,910 | 101 | 0.310 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 1,268,542 | 12.685 | 62 | 66 | fits | 44,920 | 102 | 0.257 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 513,077 | 5.131 | 62 | 66 | fits | 165,802 | 411 | 0.111 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 546,756 | 5.468 | 62 | 66 | fits | 165,802 | 411 | 0.111 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 653,356 | 6.534 | 62 | 66 | fits | 140,619 | 402 | 0.043 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 686,581 | 6.866 | 62 | 66 | fits | 140,619 | 402 | 0.043 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 1,657,046 | 16.570 | 62 | 66 | fits | 43,806 | 101 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 2,037,330 | 20.373 | 62 | 66 | fits | 141,682 | 400 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 2,070,937 | 20.709 | 62 | 66 | fits | 141,682 | 400 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 2,104,128 | 21.041 | 62 | 66 | fits | 141,682 | 400 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 2,136,122 | 21.361 | 62 | 66 | fits | 141,682 | 400 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 2,340,408 | 23.404 | 62 | 66 | fits | 140,662 | 400 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 2,373,929 | 23.739 | 62 | 66 | fits | 140,662 | 400 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 2,407,252 | 24.073 | 62 | 66 | fits | 140,662 | 400 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 2,438,476 | 24.385 | 62 | 66 | fits | 140,662 | 400 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 2,563,088 | 25.631 | 62 | 66 | fits | 161,703 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 227,371 | 2.274 | 62 | 66 | fits | 153,302 | 402 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 263,727 | 2.637 | 62 | 66 | fits | 153,302 | 402 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 297,999 | 2.980 | 62 | 66 | fits | 153,302 | 402 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 333,624 | 3.336 | 62 | 66 | fits | 153,302 | 402 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 2,595,642 | 25.956 | 62 | 66 | fits | 161,703 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 2,629,347 | 26.293 | 62 | 66 | fits | 161,703 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 2,660,787 | 26.608 | 62 | 66 | fits | 161,703 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 2,731,938 | 27.319 | 62 | 66 | fits | 138,492 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 2,764,330 | 27.643 | 62 | 66 | fits | 138,492 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 2,797,654 | 27.977 | 62 | 66 | fits | 138,492 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 2,828,806 | 28.288 | 62 | 66 | fits | 138,492 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 2,946,091 | 29.461 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 2,978,650 | 29.787 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 3,012,169 | 30.122 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 3,043,600 | 30.436 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 3,136,441 | 31.364 | 62 | 66 | fits | 134,999 | 399 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 3,167,197 | 31.672 | 62 | 66 | fits | 134,999 | 399 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 3,196,538 | 31.965 | 62 | 66 | fits | 134,999 | 399 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 3,229,667 | 32.297 | 62 | 66 | fits | 134,999 | 399 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 3,331,520 | 33.315 | 62 | 66 | fits | 41,476 | 102 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if1` | 1,239,666 | 12.397 | 20 | 200 | fits | 168,809 | 119 | 0.547 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 1,690,706 | 16.907 | 20 | 20 | fits | 161,534 | 101 | 0.529 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if1` | 1,871,539 | 18.715 | 20 | 24 | fits | 60,375 | 44 | 0.688 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 1,348,015 | 13.480 | 20 | 50 | fits | 168,092 | 89 | 0.576 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if1` | 777,813 | 7.778 | 20 | 20 | fits | 177,339 | 116 | 0.629 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 532,691 | 5.327 | 62 | 66 | fits | 140,651 | 403 | 0.052 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 566,001 | 5.660 | 62 | 66 | fits | 140,651 | 403 | 0.052 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 843,228 | 8.432 | 62 | 66 | fits | 43,751 | 101 | 0.293 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,370,253 | 13.703 | 62 | 66 | fits | 45,110 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 1,740,234 | 17.402 | 62 | 66 | fits | 43,619 | 100 | 0.299 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 2,192,475 | 21.925 | 62 | 66 | fits | 141,623 | 400 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 2,226,008 | 22.260 | 62 | 66 | fits | 141,623 | 400 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 2,259,362 | 22.594 | 62 | 66 | fits | 141,623 | 400 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 386,746 | 3.867 | 62 | 66 | fits | 147,899 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 420,868 | 4.209 | 62 | 66 | fits | 147,899 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 2,291,224 | 22.912 | 62 | 66 | fits | 141,623 | 400 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 2,330,991 | 23.310 | 62 | 66 | fits | 136,714 | 401 | 0.044 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 599,091 | 5.991 | 62 | 66 | fits | 140,651 | 403 | 0.052 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 633,088 | 6.331 | 62 | 66 | fits | 140,651 | 403 | 0.052 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 2,363,136 | 23.631 | 62 | 66 | fits | 136,714 | 401 | 0.044 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 2,396,279 | 23.963 | 62 | 66 | fits | 136,714 | 401 | 0.044 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 2,428,169 | 24.282 | 62 | 66 | fits | 136,714 | 401 | 0.044 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 2,535,426 | 25.354 | 62 | 66 | fits | 139,367 | 401 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 2,567,499 | 25.675 | 62 | 66 | fits | 139,367 | 401 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 2,600,570 | 26.006 | 62 | 66 | fits | 139,367 | 401 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 233,949 | 2.339 | 62 | 66 | fits | 178,623 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 270,769 | 2.708 | 62 | 66 | fits | 178,623 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 304,969 | 3.050 | 62 | 66 | fits | 178,623 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 340,594 | 3.406 | 62 | 66 | fits | 178,623 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 2,632,134 | 26.321 | 62 | 66 | fits | 139,367 | 401 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 2,728,333 | 27.283 | 62 | 66 | fits | 138,935 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 454,338 | 4.543 | 62 | 66 | fits | 147,899 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 489,819 | 4.898 | 62 | 66 | fits | 147,899 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 2,761,243 | 27.612 | 62 | 66 | fits | 138,935 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 2,794,314 | 27.943 | 62 | 66 | fits | 138,935 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,825,466 | 28.255 | 62 | 66 | fits | 138,935 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,942,351 | 29.424 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,974,910 | 29.749 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 3,008,359 | 30.084 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 3,039,790 | 30.398 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 3,132,558 | 31.326 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 3,163,312 | 31.633 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 3,192,653 | 31.927 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 3,225,722 | 32.257 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 3,327,534 | 33.275 | 62 | 66 | fits | 41,476 | 102 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if1` | 1,327,348 | 13.273 | 20 | 200 | fits | 165,318 | 112 | 0.561 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 1,472,888 | 14.729 | 20 | 20 | fits | 165,808 | 86 | 0.536 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if1` | 1,530,577 | 15.306 | 20 | 24 | fits | 77,893 | 52 | 0.536 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 1,267,605 | 12.676 | 20 | 50 | fits | 165,318 | 112 | 0.561 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if1` | 665,351 | 6.654 | 20 | 20 | fits | 155,758 | 60 | 0.465 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 870,227 | 8.702 | 62 | 66 | fits | 43,984 | 101 | 0.306 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,241,670 | 12.417 | 62 | 66 | fits | 45,096 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,787,018 | 17.870 | 62 | 66 | fits | 43,822 | 101 | 0.292 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 2,156,261 | 21.563 | 62 | 66 | fits | 142,751 | 400 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 2,190,082 | 21.901 | 62 | 66 | fits | 142,751 | 400 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 2,223,587 | 22.236 | 62 | 66 | fits | 142,751 | 400 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 404,737 | 4.047 | 62 | 66 | fits | 147,348 | 402 | 0.054 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 438,851 | 4.389 | 62 | 66 | fits | 147,348 | 402 | 0.054 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 551,686 | 5.517 | 62 | 66 | fits | 141,376 | 403 | 0.050 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 585,689 | 5.857 | 62 | 66 | fits | 141,376 | 403 | 0.050 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 618,455 | 6.185 | 62 | 66 | fits | 141,376 | 403 | 0.050 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 652,142 | 6.521 | 62 | 66 | fits | 141,376 | 403 | 0.050 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 2,255,902 | 22.559 | 62 | 66 | fits | 142,751 | 400 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 2,380,844 | 23.808 | 62 | 66 | fits | 163,204 | 400 | 0.117 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 2,414,196 | 24.142 | 62 | 66 | fits | 163,204 | 400 | 0.117 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 2,447,659 | 24.477 | 62 | 66 | fits | 163,204 | 400 | 0.117 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 2,479,707 | 24.797 | 62 | 66 | fits | 163,204 | 400 | 0.117 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 2,552,028 | 25.520 | 62 | 66 | fits | 138,197 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 2,584,140 | 25.841 | 62 | 66 | fits | 138,197 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 2,617,464 | 26.175 | 62 | 66 | fits | 138,197 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 252,689 | 2.527 | 62 | 66 | fits | 178,241 | 411 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 289,509 | 2.895 | 62 | 66 | fits | 178,241 | 411 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 323,752 | 3.238 | 62 | 66 | fits | 178,241 | 411 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 359,377 | 3.594 | 62 | 66 | fits | 178,241 | 411 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 472,550 | 4.726 | 62 | 66 | fits | 147,348 | 402 | 0.054 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 507,944 | 5.079 | 62 | 66 | fits | 147,348 | 402 | 0.054 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 2,648,475 | 26.485 | 62 | 66 | fits | 138,197 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 2,743,184 | 27.432 | 62 | 66 | fits | 138,308 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 2,775,585 | 27.756 | 62 | 66 | fits | 138,308 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 2,808,726 | 28.087 | 62 | 66 | fits | 138,308 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 2,839,815 | 28.398 | 62 | 66 | fits | 138,308 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 2,933,050 | 29.331 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 2,965,609 | 29.656 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 2,999,128 | 29.991 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 3,030,559 | 30.306 | 62 | 66 | fits | 139,217 | 400 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 3,146,662 | 31.467 | 62 | 66 | fits | 134,997 | 399 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 3,177,416 | 31.774 | 62 | 66 | fits | 134,997 | 399 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 3,206,757 | 32.068 | 62 | 66 | fits | 134,997 | 399 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 3,239,886 | 32.399 | 62 | 66 | fits | 134,997 | 399 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 3,342,008 | 33.420 | 62 | 66 | fits | 41,476 | 102 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if1` | 1,361,514 | 13.615 | 20 | 200 | fits | 162,800 | 83 | 0.578 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 1,504,231 | 15.042 | 20 | 20 | fits | 162,985 | 88 | 0.513 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if1` | 1,687,286 | 16.873 | 20 | 24 | fits | 60,508 | 44 | 0.685 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 1,095,149 | 10.951 | 20 | 50 | fits | 165,357 | 132 | 0.532 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if1` | 739,628 | 7.396 | 20 | 20 | fits | 167,935 | 73 | 0.514 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 838,573 | 8.386 | 62 | 66 | fits | 43,826 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,366,235 | 13.662 | 62 | 66 | fits | 45,227 | 102 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,734,082 | 17.341 | 62 | 66 | fits | 43,566 | 100 | 0.299 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 2,190,202 | 21.902 | 62 | 66 | fits | 141,607 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 385,945 | 3.859 | 62 | 66 | fits | 146,974 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 419,783 | 4.198 | 62 | 66 | fits | 146,974 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 531,913 | 5.319 | 62 | 66 | fits | 140,286 | 403 | 0.046 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 565,908 | 5.659 | 62 | 66 | fits | 140,286 | 403 | 0.046 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 598,644 | 5.986 | 62 | 66 | fits | 140,286 | 403 | 0.046 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 632,100 | 6.321 | 62 | 66 | fits | 140,286 | 403 | 0.046 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 2,223,802 | 22.238 | 62 | 66 | fits | 141,607 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 2,256,933 | 22.569 | 62 | 66 | fits | 141,607 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 2,288,809 | 22.888 | 62 | 66 | fits | 141,607 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 2,328,661 | 23.287 | 62 | 66 | fits | 137,048 | 401 | 0.047 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 2,360,982 | 23.610 | 62 | 66 | fits | 137,048 | 401 | 0.047 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 2,394,125 | 23.941 | 62 | 66 | fits | 137,048 | 401 | 0.047 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 2,426,173 | 24.262 | 62 | 66 | fits | 137,048 | 401 | 0.047 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 2,533,513 | 25.335 | 62 | 66 | fits | 139,522 | 401 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 2,565,586 | 25.656 | 62 | 66 | fits | 139,522 | 401 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,598,657 | 25.987 | 62 | 66 | fits | 139,522 | 401 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 234,678 | 2.347 | 62 | 66 | fits | 177,736 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 271,498 | 2.715 | 62 | 66 | fits | 177,736 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 305,698 | 3.057 | 62 | 66 | fits | 177,736 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 341,323 | 3.413 | 62 | 66 | fits | 177,736 | 411 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 2,630,221 | 26.302 | 62 | 66 | fits | 139,522 | 401 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 2,726,283 | 27.263 | 62 | 66 | fits | 138,935 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 453,244 | 4.532 | 62 | 66 | fits | 146,974 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 488,725 | 4.887 | 62 | 66 | fits | 146,974 | 402 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 2,759,193 | 27.592 | 62 | 66 | fits | 138,935 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 2,792,264 | 27.923 | 62 | 66 | fits | 138,935 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 2,823,416 | 28.234 | 62 | 66 | fits | 138,935 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 2,940,268 | 29.403 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 2,972,827 | 29.728 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 3,006,276 | 30.063 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 3,037,707 | 30.377 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 3,130,475 | 31.305 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 3,161,229 | 31.612 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 3,190,570 | 31.906 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 3,223,639 | 32.236 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 3,325,418 | 33.254 | 62 | 66 | fits | 41,476 | 102 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if1` | 1,467,876 | 14.679 | 20 | 200 | fits | 159,422 | 73 | 0.579 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 1,447,608 | 14.476 | 20 | 20 | fits | 159,422 | 73 | 0.579 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if1` | 1,522,405 | 15.224 | 20 | 24 | fits | 95,001 | 65 | 0.504 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 1,248,711 | 12.487 | 20 | 50 | fits | 158,369 | 118 | 0.555 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if1` | 655,307 | 6.553 | 20 | 20 | fits | 155,758 | 60 | 0.465 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 829,133 | 8.291 | 62 | 66 | fits | 44,979 | 101 | 0.310 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,190,315 | 11.903 | 62 | 66 | fits | 44,914 | 102 | 0.257 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 165,977 | 1.660 | 62 | 66 | fits | 177,058 | 411 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 200,509 | 2.005 | 62 | 66 | fits | 177,058 | 411 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 317,112 | 3.171 | 62 | 66 | fits | 145,752 | 402 | 0.050 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 350,787 | 3.508 | 62 | 66 | fits | 145,752 | 402 | 0.050 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 512,782 | 5.128 | 62 | 66 | fits | 143,143 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 546,937 | 5.469 | 62 | 66 | fits | 143,143 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 1,740,709 | 17.407 | 62 | 66 | fits | 44,074 | 101 | 0.304 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 2,110,107 | 21.101 | 62 | 66 | fits | 141,788 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 579,410 | 5.794 | 62 | 66 | fits | 143,143 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 612,866 | 6.129 | 62 | 66 | fits | 143,143 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 2,143,670 | 21.437 | 62 | 66 | fits | 141,788 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 2,176,861 | 21.769 | 62 | 66 | fits | 141,788 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 2,208,855 | 22.089 | 62 | 66 | fits | 141,788 | 400 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 2,334,007 | 23.340 | 62 | 66 | fits | 162,424 | 400 | 0.116 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 2,367,404 | 23.674 | 62 | 66 | fits | 162,424 | 400 | 0.116 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 2,400,867 | 24.009 | 62 | 66 | fits | 162,424 | 400 | 0.116 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 2,432,021 | 24.320 | 62 | 66 | fits | 162,424 | 400 | 0.116 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,472,252 | 24.723 | 62 | 66 | fits | 137,312 | 401 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,504,020 | 25.040 | 62 | 66 | fits | 137,312 | 401 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,537,559 | 25.376 | 62 | 66 | fits | 137,312 | 401 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 384,433 | 3.844 | 62 | 66 | fits | 145,752 | 402 | 0.050 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 419,985 | 4.200 | 62 | 66 | fits | 145,752 | 402 | 0.050 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 2,569,631 | 25.696 | 62 | 66 | fits | 137,312 | 401 | 0.057 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 2,668,310 | 26.683 | 62 | 66 | fits | 138,753 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 2,700,725 | 27.007 | 62 | 66 | fits | 138,753 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 2,733,866 | 27.339 | 62 | 66 | fits | 138,753 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 2,765,114 | 27.651 | 62 | 66 | fits | 138,753 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 2,882,086 | 28.821 | 62 | 66 | fits | 139,215 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 235,724 | 2.357 | 62 | 66 | fits | 177,058 | 411 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 272,679 | 2.727 | 62 | 66 | fits | 177,058 | 411 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 2,914,722 | 29.147 | 62 | 66 | fits | 139,215 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 2,948,241 | 29.482 | 62 | 66 | fits | 139,215 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 2,979,672 | 29.797 | 62 | 66 | fits | 139,215 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 3,072,541 | 30.725 | 62 | 66 | fits | 134,999 | 399 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 3,103,297 | 31.033 | 62 | 66 | fits | 134,999 | 399 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 3,132,638 | 31.326 | 62 | 66 | fits | 134,999 | 399 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 3,165,767 | 31.658 | 62 | 66 | fits | 134,999 | 399 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 3,267,848 | 32.678 | 62 | 66 | fits | 41,476 | 102 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if1` | 1,377,492 | 13.775 | 20 | 200 | fits | 161,996 | 82 | 0.568 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 1,521,099 | 15.211 | 20 | 20 | fits | 163,875 | 88 | 0.513 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if1` | 1,703,411 | 17.034 | 20 | 24 | fits | 60,728 | 44 | 0.687 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 1,111,679 | 11.117 | 20 | 50 | fits | 175,248 | 133 | 0.518 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if1` | 748,733 | 7.487 | 20 | 20 | fits | 165,589 | 90 | 0.664 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 232,028 | 2.320 | 62 | 66 | fits | 174,551 | 411 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 266,171 | 2.662 | 62 | 66 | fits | 174,551 | 411 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 380,302 | 3.803 | 62 | 66 | fits | 146,850 | 402 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 413,726 | 4.137 | 62 | 66 | fits | 146,850 | 402 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 527,042 | 5.270 | 62 | 66 | fits | 138,548 | 403 | 0.049 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 560,601 | 5.606 | 62 | 66 | fits | 138,548 | 403 | 0.049 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 592,595 | 5.926 | 62 | 66 | fits | 138,548 | 403 | 0.049 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 625,812 | 6.258 | 62 | 66 | fits | 138,548 | 403 | 0.049 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 843,942 | 8.439 | 62 | 66 | fits | 44,437 | 103 | 0.307 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 1,371,385 | 13.714 | 62 | 66 | fits | 45,107 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 1,736,949 | 17.369 | 62 | 66 | fits | 43,388 | 101 | 0.288 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 2,179,712 | 21.797 | 62 | 66 | fits | 141,366 | 400 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 2,213,227 | 22.132 | 62 | 66 | fits | 141,366 | 400 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 2,246,488 | 22.465 | 62 | 66 | fits | 141,366 | 400 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 2,278,412 | 22.784 | 62 | 66 | fits | 141,366 | 400 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 2,382,660 | 23.827 | 62 | 66 | fits | 162,344 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 2,416,107 | 24.161 | 62 | 66 | fits | 162,344 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 2,449,317 | 24.493 | 62 | 66 | fits | 162,344 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 2,480,471 | 24.805 | 62 | 66 | fits | 162,344 | 400 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 2,552,930 | 25.529 | 62 | 66 | fits | 140,193 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 2,585,572 | 25.856 | 62 | 66 | fits | 140,193 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 2,619,024 | 26.190 | 62 | 66 | fits | 140,193 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 300,282 | 3.003 | 62 | 66 | fits | 174,551 | 411 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 336,065 | 3.361 | 62 | 66 | fits | 174,551 | 411 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 2,651,096 | 26.511 | 62 | 66 | fits | 140,193 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 2,746,098 | 27.461 | 62 | 66 | fits | 138,375 | 400 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 2,778,591 | 27.786 | 62 | 66 | fits | 138,375 | 400 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 2,811,662 | 28.117 | 62 | 66 | fits | 138,375 | 400 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 448,010 | 4.480 | 62 | 66 | fits | 146,850 | 402 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 483,959 | 4.840 | 62 | 66 | fits | 146,850 | 402 | 0.048 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 2,842,673 | 28.427 | 62 | 66 | fits | 138,375 | 400 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 2,936,020 | 29.360 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 2,968,579 | 29.686 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 3,002,028 | 30.020 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 3,033,459 | 30.335 | 62 | 66 | fits | 139,079 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 3,126,298 | 31.263 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 3,157,052 | 31.571 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 3,186,393 | 31.864 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 3,219,462 | 32.195 | 62 | 66 | fits | 134,869 | 399 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 3,344,129 | 33.441 | 62 | 66 | fits | 41,476 | 102 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if1` | 1,316,981 | 13.170 | 20 | 200 | fits | 165,146 | 86 | 0.571 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 1,453,366 | 14.534 | 20 | 20 | fits | 156,653 | 68 | 0.580 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if1` | 1,511,095 | 15.111 | 20 | 24 | fits | 77,933 | 52 | 0.538 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 1,048,704 | 10.487 | 20 | 50 | fits | 163,764 | 132 | 0.517 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if1` | 659,550 | 6.596 | 20 | 20 | fits | 155,758 | 60 | 0.465 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
