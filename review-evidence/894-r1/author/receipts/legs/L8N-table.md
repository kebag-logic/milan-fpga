### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 736 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-1.held.acmp.if0` (notice-burst-1) | 9.605 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-1.held.adp.if1` (notice-burst-1) | 8.344 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.aecp.if1` (notice-every-0) | 5.648 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-1.held.maap.if0` (notice-burst-1) | 7.746 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-every-7.held.srp.if1` (notice-every-7) | 13.937 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-3.mrpdu.periodic.if0` (notice-every-3) | 2.290 | fits | 0 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-7.mrpdu.periodic.if1` (notice-every-7) | 3.350 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.36.0.if0` (notice-burst-6) | 53.336 (53.660) | fits | 1 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1133 | 1 | 228,022 (2.280) | OVER the share |
| notice-every-1 | 1129 | 0 | 189,772 (1.898) | fits |
| notice-every-2 | 1139 | 0 | 192,063 (1.921) | fits |
| notice-every-3 | 1133 | 0 | 191,263 (1.913) | fits |
| notice-every-4 | 1133 | 1 | 227,053 (2.271) | OVER the share |
| notice-every-5 | 1128 | 0 | 190,859 (1.909) | fits |
| notice-every-6 | 1127 | 1 | 225,479 (2.255) | OVER the share |
| notice-every-7 | 1129 | 0 | 191,249 (1.912) | fits |
| notice-burst-0 | 980 | 1 | 221,974 (2.220) | OVER the share |
| notice-burst-1 | 975 | 1 | 224,785 (2.248) | OVER the share |
| notice-burst-2 | 979 | 1 | 208,825 (2.088) | OVER the share |
| notice-burst-3 | 984 | 1 | 224,702 (2.247) | OVER the share |
| notice-burst-4 | 982 | 1 | 227,064 (2.271) | OVER the share |
| notice-burst-5 | 973 | 1 | 224,552 (2.246) | OVER the share |
| notice-burst-6 | 980 | 1 | 209,293 (2.093) | OVER the share |
| notice-burst-7 | 970 | 1 | 225,131 (2.251) | OVER the share |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 3.561 | 62 | 32 | 1 | within |
| notice-every-0 | 3.857 | 62 | 32 | 1 | within |
| notice-every-0 | 5.631 | 62 | 32 | 1 | within |
| notice-every-0 | 5.925 | 62 | 32 | 1 | within |
| notice-every-0 | 7.690 | 62 | 32 | 1 | within |
| notice-every-0 | 7.983 | 62 | 32 | 1 | within |
| notice-every-0 | 9.738 | 62 | 32 | 1 | within |
| notice-every-0 | 10.030 | 62 | 32 | 1 | within |
| notice-every-0 | 11.598 | 62 | 32 | 1 | within |
| notice-every-0 | 11.890 | 62 | 32 | 1 | within |
| notice-every-0 | 13.630 | 62 | 32 | 1 | within |
| notice-every-0 | 13.921 | 62 | 32 | 1 | within |
| notice-every-0 | 15.660 | 62 | 32 | 1 | within |
| notice-every-0 | 15.951 | 62 | 32 | 1 | within |
| notice-every-0 | 17.683 | 62 | 32 | 1 | within |
| notice-every-0 | 17.974 | 62 | 32 | 1 | within |
| notice-every-0 | 22.407 | 62 | 32 | 1 | within |
| notice-every-0 | 22.700 | 62 | 32 | 1 | within |
| notice-every-0 | 23.635 | 62 | 32 | 1 | within |
| notice-every-0 | 23.924 | 62 | 32 | 1 | within |
| notice-every-0 | 25.621 | 62 | 32 | 1 | within |
| notice-every-0 | 25.915 | 62 | 32 | 1 | within |
| notice-every-0 | 27.612 | 62 | 32 | 1 | within |
| notice-every-0 | 27.905 | 62 | 32 | 1 | within |
| notice-every-0 | 29.596 | 62 | 32 | 1 | within |
| notice-every-0 | 29.889 | 62 | 32 | 1 | within |
| notice-every-0 | 31.668 | 62 | 32 | 1 | within |
| notice-every-0 | 31.959 | 62 | 32 | 1 | within |
| notice-every-0 | 33.626 | 62 | 32 | 1 | within |
| notice-every-0 | 33.916 | 62 | 32 | 1 | within |
| notice-every-0 | 35.580 | 62 | 32 | 1 | within |
| notice-every-0 | 35.871 | 62 | 32 | 1 | within |
| notice-every-0 | 37.522 | 62 | 32 | 1 | within |
| notice-every-0 | 37.814 | 62 | 32 | 1 | within |
| notice-every-0 | 42.712 | 62 | 32 | 1 | within |
| notice-every-0 | 46.593 | 62 | 32 | 1 | within |
| notice-every-0 | 46.850 | 62 | 32 | 1 | within |
| notice-every-0 | 48.700 | 62 | 32 | 1 | within |
| notice-every-0 | 48.992 | 62 | 32 | 1 | within |
| notice-every-0 | 50.699 | 62 | 32 | 1 | within |
| notice-every-1 | 5.646 | 62 | 32 | 1 | within |
| notice-every-1 | 5.938 | 62 | 32 | 1 | within |
| notice-every-1 | 3.572 | 62 | 32 | 1 | within |
| notice-every-1 | 3.872 | 62 | 32 | 1 | within |
| notice-every-1 | 7.704 | 62 | 32 | 1 | within |
| notice-every-1 | 7.997 | 62 | 32 | 1 | within |
| notice-every-1 | 9.488 | 62 | 32 | 1 | within |
| notice-every-1 | 9.781 | 62 | 32 | 1 | within |
| notice-every-1 | 11.609 | 62 | 32 | 1 | within |
| notice-every-1 | 11.901 | 62 | 32 | 1 | within |
| notice-every-1 | 13.641 | 62 | 32 | 1 | within |
| notice-every-1 | 13.931 | 62 | 32 | 1 | within |
| notice-every-1 | 15.671 | 62 | 32 | 1 | within |
| notice-every-1 | 15.962 | 62 | 32 | 1 | within |
| notice-every-1 | 17.694 | 62 | 32 | 1 | within |
| notice-every-1 | 17.985 | 62 | 32 | 1 | within |
| notice-every-1 | 22.419 | 62 | 32 | 1 | within |
| notice-every-1 | 22.713 | 62 | 32 | 1 | within |
| notice-every-1 | 23.647 | 62 | 32 | 1 | within |
| notice-every-1 | 23.937 | 62 | 32 | 1 | within |
| notice-every-1 | 25.634 | 62 | 32 | 1 | within |
| notice-every-1 | 25.928 | 62 | 32 | 1 | within |
| notice-every-1 | 27.624 | 62 | 32 | 1 | within |
| notice-every-1 | 27.918 | 62 | 32 | 1 | within |
| notice-every-1 | 29.609 | 62 | 32 | 1 | within |
| notice-every-1 | 29.902 | 62 | 32 | 1 | within |
| notice-every-1 | 31.681 | 62 | 32 | 1 | within |
| notice-every-1 | 31.972 | 62 | 32 | 1 | within |
| notice-every-1 | 33.639 | 62 | 32 | 1 | within |
| notice-every-1 | 33.929 | 62 | 32 | 1 | within |
| notice-every-1 | 35.592 | 62 | 32 | 1 | within |
| notice-every-1 | 35.884 | 62 | 32 | 1 | within |
| notice-every-1 | 37.535 | 62 | 32 | 1 | within |
| notice-every-1 | 37.827 | 62 | 32 | 1 | within |
| notice-every-1 | 42.724 | 62 | 32 | 1 | within |
| notice-every-1 | 46.604 | 62 | 32 | 1 | within |
| notice-every-1 | 46.862 | 62 | 32 | 1 | within |
| notice-every-1 | 48.467 | 62 | 32 | 1 | within |
| notice-every-1 | 48.758 | 62 | 32 | 1 | within |
| notice-every-1 | 50.707 | 62 | 32 | 1 | within |
| notice-every-2 | 6.099 | 62 | 32 | 1 | within |
| notice-every-2 | 6.391 | 62 | 32 | 1 | within |
| notice-every-2 | 2.131 | 62 | 32 | 1 | within |
| notice-every-2 | 2.429 | 62 | 32 | 1 | within |
| notice-every-2 | 8.155 | 62 | 32 | 1 | within |
| notice-every-2 | 8.448 | 62 | 32 | 1 | within |
| notice-every-2 | 4.308 | 62 | 32 | 1 | within |
| notice-every-2 | 4.608 | 62 | 32 | 1 | within |
| notice-every-2 | 10.204 | 62 | 32 | 1 | within |
| notice-every-2 | 10.494 | 62 | 32 | 1 | within |
| notice-every-2 | 12.235 | 62 | 32 | 1 | within |
| notice-every-2 | 12.526 | 62 | 32 | 1 | within |
| notice-every-2 | 14.095 | 62 | 32 | 1 | within |
| notice-every-2 | 14.387 | 62 | 32 | 1 | within |
| notice-every-2 | 16.119 | 62 | 32 | 1 | within |
| notice-every-2 | 16.410 | 62 | 32 | 1 | within |
| notice-every-2 | 18.136 | 62 | 32 | 1 | within |
| notice-every-2 | 18.427 | 62 | 32 | 1 | within |
| notice-every-2 | 20.132 | 62 | 32 | 1 | within |
| notice-every-2 | 20.421 | 62 | 32 | 1 | within |
| notice-every-2 | 24.231 | 62 | 32 | 1 | within |
| notice-every-2 | 28.230 | 62 | 32 | 1 | within |
| notice-every-2 | 28.507 | 62 | 32 | 1 | within |
| notice-every-2 | 30.220 | 62 | 32 | 1 | within |
| notice-every-2 | 30.498 | 62 | 32 | 1 | within |
| notice-every-2 | 32.204 | 62 | 32 | 1 | within |
| notice-every-2 | 32.476 | 62 | 32 | 1 | within |
| notice-every-2 | 34.276 | 62 | 32 | 1 | within |
| notice-every-2 | 34.548 | 62 | 32 | 1 | within |
| notice-every-2 | 36.235 | 62 | 32 | 1 | within |
| notice-every-2 | 36.505 | 62 | 32 | 1 | within |
| notice-every-2 | 38.187 | 62 | 32 | 1 | within |
| notice-every-2 | 38.458 | 62 | 32 | 1 | within |
| notice-every-2 | 40.131 | 62 | 32 | 1 | within |
| notice-every-2 | 40.402 | 62 | 32 | 1 | within |
| notice-every-2 | 44.800 | 62 | 32 | 1 | within |
| notice-every-2 | 48.117 | 62 | 32 | 1 | within |
| notice-every-2 | 48.362 | 62 | 32 | 1 | within |
| notice-every-2 | 50.247 | 62 | 32 | 1 | within |
| notice-every-2 | 50.541 | 62 | 32 | 1 | within |
| notice-every-3 | 5.589 | 62 | 32 | 1 | within |
| notice-every-3 | 5.881 | 62 | 32 | 1 | within |
| notice-every-3 | 3.516 | 62 | 32 | 1 | within |
| notice-every-3 | 3.817 | 62 | 32 | 1 | within |
| notice-every-3 | 7.647 | 62 | 32 | 1 | within |
| notice-every-3 | 7.940 | 62 | 32 | 1 | within |
| notice-every-3 | 9.695 | 62 | 32 | 1 | within |
| notice-every-3 | 9.988 | 62 | 32 | 1 | within |
| notice-every-3 | 11.556 | 62 | 32 | 1 | within |
| notice-every-3 | 11.847 | 62 | 32 | 1 | within |
| notice-every-3 | 13.587 | 62 | 32 | 1 | within |
| notice-every-3 | 13.878 | 62 | 32 | 1 | within |
| notice-every-3 | 15.617 | 62 | 32 | 1 | within |
| notice-every-3 | 15.909 | 62 | 32 | 1 | within |
| notice-every-3 | 17.641 | 62 | 32 | 1 | within |
| notice-every-3 | 17.931 | 62 | 32 | 1 | within |
| notice-every-3 | 22.365 | 62 | 32 | 1 | within |
| notice-every-3 | 22.659 | 62 | 32 | 1 | within |
| notice-every-3 | 23.593 | 62 | 32 | 1 | within |
| notice-every-3 | 23.883 | 62 | 32 | 1 | within |
| notice-every-3 | 25.580 | 62 | 32 | 1 | within |
| notice-every-3 | 25.874 | 62 | 32 | 1 | within |
| notice-every-3 | 27.570 | 62 | 32 | 1 | within |
| notice-every-3 | 27.864 | 62 | 32 | 1 | within |
| notice-every-3 | 29.555 | 62 | 32 | 1 | within |
| notice-every-3 | 29.848 | 62 | 32 | 1 | within |
| notice-every-3 | 31.627 | 62 | 32 | 1 | within |
| notice-every-3 | 31.918 | 62 | 32 | 1 | within |
| notice-every-3 | 33.585 | 62 | 32 | 1 | within |
| notice-every-3 | 33.875 | 62 | 32 | 1 | within |
| notice-every-3 | 35.538 | 62 | 32 | 1 | within |
| notice-every-3 | 35.829 | 62 | 32 | 1 | within |
| notice-every-3 | 37.481 | 62 | 32 | 1 | within |
| notice-every-3 | 37.773 | 62 | 32 | 1 | within |
| notice-every-3 | 42.672 | 62 | 32 | 1 | within |
| notice-every-3 | 46.552 | 62 | 32 | 1 | within |
| notice-every-3 | 46.810 | 62 | 32 | 1 | within |
| notice-every-3 | 48.660 | 62 | 32 | 1 | within |
| notice-every-3 | 48.951 | 62 | 32 | 1 | within |
| notice-every-3 | 50.596 | 62 | 32 | 1 | within |
| notice-every-4 | 6.100 | 62 | 32 | 1 | within |
| notice-every-4 | 6.392 | 62 | 32 | 1 | within |
| notice-every-4 | 8.159 | 62 | 32 | 1 | within |
| notice-every-4 | 8.451 | 62 | 32 | 1 | within |
| notice-every-4 | 2.133 | 62 | 32 | 1 | within |
| notice-every-4 | 2.432 | 62 | 32 | 1 | within |
| notice-every-4 | 4.309 | 62 | 32 | 1 | within |
| notice-every-4 | 4.608 | 62 | 32 | 1 | within |
| notice-every-4 | 10.208 | 62 | 32 | 1 | within |
| notice-every-4 | 10.498 | 62 | 32 | 1 | within |
| notice-every-4 | 12.239 | 62 | 32 | 1 | within |
| notice-every-4 | 12.530 | 62 | 32 | 1 | within |
| notice-every-4 | 14.099 | 62 | 32 | 1 | within |
| notice-every-4 | 14.390 | 62 | 32 | 1 | within |
| notice-every-4 | 16.123 | 62 | 32 | 1 | within |
| notice-every-4 | 16.413 | 62 | 32 | 1 | within |
| notice-every-4 | 18.140 | 62 | 32 | 1 | within |
| notice-every-4 | 18.431 | 62 | 32 | 1 | within |
| notice-every-4 | 20.136 | 62 | 32 | 1 | within |
| notice-every-4 | 20.425 | 62 | 32 | 1 | within |
| notice-every-4 | 24.235 | 62 | 32 | 1 | within |
| notice-every-4 | 28.235 | 62 | 32 | 1 | within |
| notice-every-4 | 28.511 | 62 | 32 | 1 | within |
| notice-every-4 | 30.224 | 62 | 32 | 1 | within |
| notice-every-4 | 30.502 | 62 | 32 | 1 | within |
| notice-every-4 | 32.209 | 62 | 32 | 1 | within |
| notice-every-4 | 32.481 | 62 | 32 | 1 | within |
| notice-every-4 | 34.280 | 62 | 32 | 1 | within |
| notice-every-4 | 34.553 | 62 | 32 | 1 | within |
| notice-every-4 | 36.240 | 62 | 32 | 1 | within |
| notice-every-4 | 36.509 | 62 | 32 | 1 | within |
| notice-every-4 | 38.192 | 62 | 32 | 1 | within |
| notice-every-4 | 38.463 | 62 | 32 | 1 | within |
| notice-every-4 | 40.135 | 62 | 32 | 1 | within |
| notice-every-4 | 40.407 | 62 | 32 | 1 | within |
| notice-every-4 | 44.807 | 62 | 32 | 1 | within |
| notice-every-4 | 48.124 | 62 | 32 | 1 | within |
| notice-every-4 | 48.369 | 62 | 32 | 1 | within |
| notice-every-4 | 50.255 | 62 | 32 | 1 | within |
| notice-every-4 | 50.550 | 62 | 32 | 1 | within |
| notice-every-5 | 5.646 | 62 | 32 | 1 | within |
| notice-every-5 | 5.938 | 62 | 32 | 1 | within |
| notice-every-5 | 3.572 | 62 | 32 | 1 | within |
| notice-every-5 | 3.872 | 62 | 32 | 1 | within |
| notice-every-5 | 7.704 | 62 | 32 | 1 | within |
| notice-every-5 | 7.997 | 62 | 32 | 1 | within |
| notice-every-5 | 9.488 | 62 | 32 | 1 | within |
| notice-every-5 | 9.781 | 62 | 32 | 1 | within |
| notice-every-5 | 11.609 | 62 | 32 | 1 | within |
| notice-every-5 | 11.901 | 62 | 32 | 1 | within |
| notice-every-5 | 13.641 | 62 | 32 | 1 | within |
| notice-every-5 | 13.931 | 62 | 32 | 1 | within |
| notice-every-5 | 15.671 | 62 | 32 | 1 | within |
| notice-every-5 | 15.962 | 62 | 32 | 1 | within |
| notice-every-5 | 17.694 | 62 | 32 | 1 | within |
| notice-every-5 | 17.985 | 62 | 32 | 1 | within |
| notice-every-5 | 22.420 | 62 | 32 | 1 | within |
| notice-every-5 | 22.713 | 62 | 32 | 1 | within |
| notice-every-5 | 23.648 | 62 | 32 | 1 | within |
| notice-every-5 | 23.937 | 62 | 32 | 1 | within |
| notice-every-5 | 25.634 | 62 | 32 | 1 | within |
| notice-every-5 | 25.928 | 62 | 32 | 1 | within |
| notice-every-5 | 27.625 | 62 | 32 | 1 | within |
| notice-every-5 | 27.918 | 62 | 32 | 1 | within |
| notice-every-5 | 29.609 | 62 | 32 | 1 | within |
| notice-every-5 | 29.903 | 62 | 32 | 1 | within |
| notice-every-5 | 31.681 | 62 | 32 | 1 | within |
| notice-every-5 | 31.972 | 62 | 32 | 1 | within |
| notice-every-5 | 33.640 | 62 | 32 | 1 | within |
| notice-every-5 | 33.929 | 62 | 32 | 1 | within |
| notice-every-5 | 35.593 | 62 | 32 | 1 | within |
| notice-every-5 | 35.884 | 62 | 32 | 1 | within |
| notice-every-5 | 37.535 | 62 | 32 | 1 | within |
| notice-every-5 | 37.827 | 62 | 32 | 1 | within |
| notice-every-5 | 42.724 | 62 | 32 | 1 | within |
| notice-every-5 | 46.604 | 62 | 32 | 1 | within |
| notice-every-5 | 46.862 | 62 | 32 | 1 | within |
| notice-every-5 | 48.467 | 62 | 32 | 1 | within |
| notice-every-5 | 48.758 | 62 | 32 | 1 | within |
| notice-every-5 | 50.648 | 62 | 32 | 1 | within |
| notice-every-6 | 3.561 | 62 | 32 | 1 | within |
| notice-every-6 | 3.858 | 62 | 32 | 1 | within |
| notice-every-6 | 5.631 | 62 | 32 | 1 | within |
| notice-every-6 | 5.925 | 62 | 32 | 1 | within |
| notice-every-6 | 7.689 | 62 | 32 | 1 | within |
| notice-every-6 | 7.982 | 62 | 32 | 1 | within |
| notice-every-6 | 9.737 | 62 | 32 | 1 | within |
| notice-every-6 | 10.029 | 62 | 32 | 1 | within |
| notice-every-6 | 11.597 | 62 | 32 | 1 | within |
| notice-every-6 | 11.889 | 62 | 32 | 1 | within |
| notice-every-6 | 13.629 | 62 | 32 | 1 | within |
| notice-every-6 | 13.920 | 62 | 32 | 1 | within |
| notice-every-6 | 15.659 | 62 | 32 | 1 | within |
| notice-every-6 | 15.950 | 62 | 32 | 1 | within |
| notice-every-6 | 17.683 | 62 | 32 | 1 | within |
| notice-every-6 | 17.973 | 62 | 32 | 1 | within |
| notice-every-6 | 22.407 | 62 | 32 | 1 | within |
| notice-every-6 | 22.700 | 62 | 32 | 1 | within |
| notice-every-6 | 23.635 | 62 | 32 | 1 | within |
| notice-every-6 | 23.925 | 62 | 32 | 1 | within |
| notice-every-6 | 25.621 | 62 | 32 | 1 | within |
| notice-every-6 | 25.915 | 62 | 32 | 1 | within |
| notice-every-6 | 27.612 | 62 | 32 | 1 | within |
| notice-every-6 | 27.905 | 62 | 32 | 1 | within |
| notice-every-6 | 29.596 | 62 | 32 | 1 | within |
| notice-every-6 | 29.889 | 62 | 32 | 1 | within |
| notice-every-6 | 31.668 | 62 | 32 | 1 | within |
| notice-every-6 | 31.959 | 62 | 32 | 1 | within |
| notice-every-6 | 33.626 | 62 | 32 | 1 | within |
| notice-every-6 | 33.916 | 62 | 32 | 1 | within |
| notice-every-6 | 35.579 | 62 | 32 | 1 | within |
| notice-every-6 | 35.870 | 62 | 32 | 1 | within |
| notice-every-6 | 37.522 | 62 | 32 | 1 | within |
| notice-every-6 | 37.814 | 62 | 32 | 1 | within |
| notice-every-6 | 42.714 | 62 | 32 | 1 | within |
| notice-every-6 | 46.594 | 62 | 32 | 1 | within |
| notice-every-6 | 46.852 | 62 | 32 | 1 | within |
| notice-every-6 | 48.702 | 62 | 32 | 1 | within |
| notice-every-6 | 48.993 | 62 | 32 | 1 | within |
| notice-every-6 | 50.638 | 62 | 32 | 1 | within |
| notice-every-7 | 3.563 | 62 | 32 | 1 | within |
| notice-every-7 | 3.859 | 62 | 32 | 1 | within |
| notice-every-7 | 5.633 | 62 | 32 | 1 | within |
| notice-every-7 | 5.927 | 62 | 32 | 1 | within |
| notice-every-7 | 7.691 | 62 | 32 | 1 | within |
| notice-every-7 | 7.984 | 62 | 32 | 1 | within |
| notice-every-7 | 9.739 | 62 | 32 | 1 | within |
| notice-every-7 | 10.032 | 62 | 32 | 1 | within |
| notice-every-7 | 11.600 | 62 | 32 | 1 | within |
| notice-every-7 | 11.891 | 62 | 32 | 1 | within |
| notice-every-7 | 13.632 | 62 | 32 | 1 | within |
| notice-every-7 | 13.922 | 62 | 32 | 1 | within |
| notice-every-7 | 15.662 | 62 | 32 | 1 | within |
| notice-every-7 | 15.953 | 62 | 32 | 1 | within |
| notice-every-7 | 17.685 | 62 | 32 | 1 | within |
| notice-every-7 | 17.976 | 62 | 32 | 1 | within |
| notice-every-7 | 22.411 | 62 | 32 | 1 | within |
| notice-every-7 | 22.704 | 62 | 32 | 1 | within |
| notice-every-7 | 23.639 | 62 | 32 | 1 | within |
| notice-every-7 | 23.928 | 62 | 32 | 1 | within |
| notice-every-7 | 25.625 | 62 | 32 | 1 | within |
| notice-every-7 | 25.919 | 62 | 32 | 1 | within |
| notice-every-7 | 27.616 | 62 | 32 | 1 | within |
| notice-every-7 | 27.909 | 62 | 32 | 1 | within |
| notice-every-7 | 29.600 | 62 | 32 | 1 | within |
| notice-every-7 | 29.893 | 62 | 32 | 1 | within |
| notice-every-7 | 31.672 | 62 | 32 | 1 | within |
| notice-every-7 | 31.963 | 62 | 32 | 1 | within |
| notice-every-7 | 33.630 | 62 | 32 | 1 | within |
| notice-every-7 | 33.920 | 62 | 32 | 1 | within |
| notice-every-7 | 35.584 | 62 | 32 | 1 | within |
| notice-every-7 | 35.875 | 62 | 32 | 1 | within |
| notice-every-7 | 37.526 | 62 | 32 | 1 | within |
| notice-every-7 | 37.818 | 62 | 32 | 1 | within |
| notice-every-7 | 42.715 | 62 | 32 | 1 | within |
| notice-every-7 | 46.595 | 62 | 32 | 1 | within |
| notice-every-7 | 46.853 | 62 | 32 | 1 | within |
| notice-every-7 | 48.703 | 62 | 32 | 1 | within |
| notice-every-7 | 48.994 | 62 | 32 | 1 | within |
| notice-every-7 | 50.640 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.293 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.588 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.467 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.760 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.745 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.037 | 62 | 32 | 1 | within |
| notice-burst-0 | 19.636 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.323 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.641 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.932 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.605 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.360 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.642 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.131 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.412 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.160 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.441 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.179 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.448 | 62 | 32 | 1 | within |
| notice-burst-0 | 33.269 | 62 | 32 | 1 | within |
| notice-burst-0 | 33.545 | 62 | 32 | 1 | within |
| notice-burst-0 | 35.265 | 62 | 32 | 1 | within |
| notice-burst-0 | 35.540 | 62 | 32 | 1 | within |
| notice-burst-0 | 37.254 | 62 | 32 | 1 | within |
| notice-burst-0 | 37.531 | 62 | 32 | 1 | within |
| notice-burst-0 | 39.239 | 62 | 32 | 1 | within |
| notice-burst-0 | 39.510 | 62 | 32 | 1 | within |
| notice-burst-0 | 41.203 | 62 | 32 | 1 | within |
| notice-burst-0 | 41.474 | 62 | 32 | 1 | within |
| notice-burst-0 | 43.251 | 62 | 32 | 1 | within |
| notice-burst-0 | 43.519 | 62 | 32 | 1 | within |
| notice-burst-0 | 45.201 | 62 | 32 | 1 | within |
| notice-burst-0 | 45.473 | 62 | 32 | 1 | within |
| notice-burst-0 | 47.146 | 62 | 32 | 1 | within |
| notice-burst-0 | 47.417 | 62 | 32 | 1 | within |
| notice-burst-0 | 49.330 | 62 | 32 | 1 | within |
| notice-burst-0 | 49.588 | 62 | 32 | 1 | within |
| notice-burst-0 | 51.276 | 62 | 32 | 1 | within |
| notice-burst-0 | 51.574 | 62 | 32 | 1 | within |
| notice-burst-0 | 53.314 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.852 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.142 | 62 | 32 | 1 | within |
| notice-burst-1 | 6.802 | 62 | 32 | 1 | within |
| notice-burst-1 | 7.092 | 62 | 32 | 1 | within |
| notice-burst-1 | 20.679 | 62 | 32 | 1 | within |
| notice-burst-1 | 24.354 | 62 | 32 | 1 | within |
| notice-burst-1 | 24.636 | 62 | 32 | 1 | within |
| notice-burst-1 | 26.382 | 62 | 32 | 1 | within |
| notice-burst-1 | 6.138 | 62 | 32 | 1 | within |
| notice-burst-1 | 6.435 | 62 | 32 | 1 | within |
| notice-burst-1 | 26.663 | 62 | 32 | 1 | within |
| notice-burst-1 | 28.409 | 62 | 32 | 1 | within |
| notice-burst-1 | 28.691 | 62 | 32 | 1 | within |
| notice-burst-1 | 30.432 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.314 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.621 | 62 | 32 | 1 | within |
| notice-burst-1 | 30.714 | 62 | 32 | 1 | within |
| notice-burst-1 | 32.447 | 62 | 32 | 1 | within |
| notice-burst-1 | 32.716 | 62 | 32 | 1 | within |
| notice-burst-1 | 34.285 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.933 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.248 | 62 | 32 | 1 | within |
| notice-burst-1 | 34.557 | 62 | 32 | 1 | within |
| notice-burst-1 | 36.270 | 62 | 32 | 1 | within |
| notice-burst-1 | 36.548 | 62 | 32 | 1 | within |
| notice-burst-1 | 38.256 | 62 | 32 | 1 | within |
| notice-burst-1 | 38.528 | 62 | 32 | 1 | within |
| notice-burst-1 | 40.474 | 62 | 32 | 1 | within |
| notice-burst-1 | 40.744 | 62 | 32 | 1 | within |
| notice-burst-1 | 42.432 | 62 | 32 | 1 | within |
| notice-burst-1 | 42.700 | 62 | 32 | 1 | within |
| notice-burst-1 | 44.478 | 62 | 32 | 1 | within |
| notice-burst-1 | 44.750 | 62 | 32 | 1 | within |
| notice-burst-1 | 46.422 | 62 | 32 | 1 | within |
| notice-burst-1 | 46.693 | 62 | 32 | 1 | within |
| notice-burst-1 | 48.358 | 62 | 32 | 1 | within |
| notice-burst-1 | 48.616 | 62 | 32 | 1 | within |
| notice-burst-1 | 50.225 | 62 | 32 | 1 | within |
| notice-burst-1 | 50.516 | 62 | 32 | 1 | within |
| notice-burst-1 | 52.572 | 62 | 32 | 1 | within |
| notice-burst-2 | 4.463 | 62 | 32 | 1 | within |
| notice-burst-2 | 4.755 | 62 | 32 | 1 | within |
| notice-burst-2 | 5.354 | 62 | 32 | 1 | within |
| notice-burst-2 | 5.645 | 62 | 32 | 1 | within |
| notice-burst-2 | 19.580 | 62 | 32 | 1 | within |
| notice-burst-2 | 23.529 | 62 | 32 | 1 | within |
| notice-burst-2 | 2.361 | 62 | 32 | 1 | within |
| notice-burst-2 | 2.664 | 62 | 32 | 1 | within |
| notice-burst-2 | 23.814 | 62 | 32 | 1 | within |
| notice-burst-2 | 25.306 | 62 | 32 | 1 | within |
| notice-burst-2 | 25.587 | 62 | 32 | 1 | within |
| notice-burst-2 | 27.339 | 62 | 32 | 1 | within |
| notice-burst-2 | 27.621 | 62 | 32 | 1 | within |
| notice-burst-2 | 29.366 | 62 | 32 | 1 | within |
| notice-burst-2 | 29.647 | 62 | 32 | 1 | within |
| notice-burst-2 | 31.390 | 62 | 32 | 1 | within |
| notice-burst-2 | 31.672 | 62 | 32 | 1 | within |
| notice-burst-2 | 33.500 | 62 | 32 | 1 | within |
| notice-burst-2 | 3.051 | 62 | 32 | 1 | within |
| notice-burst-2 | 3.355 | 62 | 32 | 1 | within |
| notice-burst-2 | 33.777 | 62 | 32 | 1 | within |
| notice-burst-2 | 35.498 | 62 | 32 | 1 | within |
| notice-burst-2 | 35.773 | 62 | 32 | 1 | within |
| notice-burst-2 | 37.488 | 62 | 32 | 1 | within |
| notice-burst-2 | 37.765 | 62 | 32 | 1 | within |
| notice-burst-2 | 39.473 | 62 | 32 | 1 | within |
| notice-burst-2 | 39.744 | 62 | 32 | 1 | within |
| notice-burst-2 | 41.438 | 62 | 32 | 1 | within |
| notice-burst-2 | 41.708 | 62 | 32 | 1 | within |
| notice-burst-2 | 43.485 | 62 | 32 | 1 | within |
| notice-burst-2 | 43.754 | 62 | 32 | 1 | within |
| notice-burst-2 | 45.436 | 62 | 32 | 1 | within |
| notice-burst-2 | 45.708 | 62 | 32 | 1 | within |
| notice-burst-2 | 47.381 | 62 | 32 | 1 | within |
| notice-burst-2 | 47.652 | 62 | 32 | 1 | within |
| notice-burst-2 | 49.317 | 62 | 32 | 1 | within |
| notice-burst-2 | 49.575 | 62 | 32 | 1 | within |
| notice-burst-2 | 51.431 | 62 | 32 | 1 | within |
| notice-burst-2 | 51.722 | 62 | 32 | 1 | within |
| notice-burst-2 | 53.285 | 62 | 32 | 1 | within |
| notice-burst-3 | 6.135 | 62 | 32 | 1 | within |
| notice-burst-3 | 6.426 | 62 | 32 | 1 | within |
| notice-burst-3 | 6.800 | 62 | 32 | 1 | within |
| notice-burst-3 | 7.089 | 62 | 32 | 1 | within |
| notice-burst-3 | 20.679 | 62 | 32 | 1 | within |
| notice-burst-3 | 24.355 | 62 | 32 | 1 | within |
| notice-burst-3 | 24.636 | 62 | 32 | 1 | within |
| notice-burst-3 | 26.382 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.841 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.140 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.929 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.233 | 62 | 32 | 1 | within |
| notice-burst-3 | 26.666 | 62 | 32 | 1 | within |
| notice-burst-3 | 28.410 | 62 | 32 | 1 | within |
| notice-burst-3 | 28.691 | 62 | 32 | 1 | within |
| notice-burst-3 | 30.435 | 62 | 32 | 1 | within |
| notice-burst-3 | 30.716 | 62 | 32 | 1 | within |
| notice-burst-3 | 32.450 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.312 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.623 | 62 | 32 | 1 | within |
| notice-burst-3 | 32.725 | 62 | 32 | 1 | within |
| notice-burst-3 | 34.293 | 62 | 32 | 1 | within |
| notice-burst-3 | 34.571 | 62 | 32 | 1 | within |
| notice-burst-3 | 36.284 | 62 | 32 | 1 | within |
| notice-burst-3 | 36.562 | 62 | 32 | 1 | within |
| notice-burst-3 | 38.270 | 62 | 32 | 1 | within |
| notice-burst-3 | 38.541 | 62 | 32 | 1 | within |
| notice-burst-3 | 40.487 | 62 | 32 | 1 | within |
| notice-burst-3 | 40.758 | 62 | 32 | 1 | within |
| notice-burst-3 | 42.445 | 62 | 32 | 1 | within |
| notice-burst-3 | 42.714 | 62 | 32 | 1 | within |
| notice-burst-3 | 44.492 | 62 | 32 | 1 | within |
| notice-burst-3 | 44.764 | 62 | 32 | 1 | within |
| notice-burst-3 | 46.435 | 62 | 32 | 1 | within |
| notice-burst-3 | 46.707 | 62 | 32 | 1 | within |
| notice-burst-3 | 48.372 | 62 | 32 | 1 | within |
| notice-burst-3 | 48.629 | 62 | 32 | 1 | within |
| notice-burst-3 | 50.238 | 62 | 32 | 1 | within |
| notice-burst-3 | 50.530 | 62 | 32 | 1 | within |
| notice-burst-3 | 52.418 | 62 | 32 | 1 | within |
| notice-burst-4 | 19.262 | 62 | 32 | 0 | within |
| notice-burst-4 | 22.950 | 62 | 32 | 0 | within |
| notice-burst-4 | 23.233 | 62 | 32 | 0 | within |
| notice-burst-4 | 24.722 | 62 | 32 | 0 | within |
| notice-burst-4 | 3.376 | 62 | 32 | 0 | within |
| notice-burst-4 | 3.672 | 62 | 32 | 0 | within |
| notice-burst-4 | 4.676 | 62 | 32 | 0 | within |
| notice-burst-4 | 4.974 | 62 | 32 | 0 | within |
| notice-burst-4 | 5.343 | 62 | 32 | 0 | within |
| notice-burst-4 | 5.635 | 62 | 32 | 0 | within |
| notice-burst-4 | 25.004 | 62 | 32 | 0 | within |
| notice-burst-4 | 26.755 | 62 | 32 | 0 | within |
| notice-burst-4 | 27.037 | 62 | 32 | 0 | within |
| notice-burst-4 | 28.783 | 62 | 32 | 0 | within |
| notice-burst-4 | 29.064 | 62 | 32 | 0 | within |
| notice-burst-4 | 30.808 | 62 | 32 | 0 | within |
| notice-burst-4 | 31.089 | 62 | 32 | 0 | within |
| notice-burst-4 | 32.918 | 62 | 32 | 0 | within |
| notice-burst-4 | 2.449 | 62 | 32 | 0 | within |
| notice-burst-4 | 2.765 | 62 | 32 | 0 | within |
| notice-burst-4 | 33.195 | 62 | 32 | 0 | within |
| notice-burst-4 | 34.916 | 62 | 32 | 0 | within |
| notice-burst-4 | 35.192 | 62 | 32 | 0 | within |
| notice-burst-4 | 36.906 | 62 | 32 | 0 | within |
| notice-burst-4 | 37.184 | 62 | 32 | 0 | within |
| notice-burst-4 | 38.892 | 62 | 32 | 0 | within |
| notice-burst-4 | 39.163 | 62 | 32 | 0 | within |
| notice-burst-4 | 40.857 | 62 | 32 | 0 | within |
| notice-burst-4 | 41.127 | 62 | 32 | 0 | within |
| notice-burst-4 | 42.904 | 62 | 32 | 0 | within |
| notice-burst-4 | 43.173 | 62 | 32 | 0 | within |
| notice-burst-4 | 44.855 | 62 | 32 | 0 | within |
| notice-burst-4 | 45.127 | 62 | 32 | 0 | within |
| notice-burst-4 | 46.800 | 62 | 32 | 0 | within |
| notice-burst-4 | 47.071 | 62 | 32 | 0 | within |
| notice-burst-4 | 48.736 | 62 | 32 | 0 | within |
| notice-burst-4 | 48.995 | 62 | 32 | 0 | within |
| notice-burst-4 | 50.853 | 62 | 32 | 0 | within |
| notice-burst-4 | 51.144 | 62 | 32 | 0 | within |
| notice-burst-4 | 52.876 | 62 | 32 | 0 | within |
| notice-burst-5 | 20.679 | 62 | 32 | 1 | within |
| notice-burst-5 | 24.356 | 62 | 32 | 1 | within |
| notice-burst-5 | 24.640 | 62 | 32 | 1 | within |
| notice-burst-5 | 26.387 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.863 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.159 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.146 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.442 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.810 | 62 | 32 | 1 | within |
| notice-burst-5 | 7.102 | 62 | 32 | 1 | within |
| notice-burst-5 | 26.668 | 62 | 32 | 1 | within |
| notice-burst-5 | 28.414 | 62 | 32 | 1 | within |
| notice-burst-5 | 28.696 | 62 | 32 | 1 | within |
| notice-burst-5 | 30.437 | 62 | 32 | 1 | within |
| notice-burst-5 | 30.718 | 62 | 32 | 1 | within |
| notice-burst-5 | 32.457 | 62 | 32 | 1 | within |
| notice-burst-5 | 32.738 | 62 | 32 | 1 | within |
| notice-burst-5 | 34.313 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.319 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.629 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.936 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.251 | 62 | 32 | 1 | within |
| notice-burst-5 | 34.586 | 62 | 32 | 1 | within |
| notice-burst-5 | 36.302 | 62 | 32 | 1 | within |
| notice-burst-5 | 36.579 | 62 | 32 | 1 | within |
| notice-burst-5 | 38.287 | 62 | 32 | 1 | within |
| notice-burst-5 | 38.559 | 62 | 32 | 1 | within |
| notice-burst-5 | 40.252 | 62 | 32 | 1 | within |
| notice-burst-5 | 40.523 | 62 | 32 | 1 | within |
| notice-burst-5 | 42.462 | 62 | 32 | 1 | within |
| notice-burst-5 | 42.731 | 62 | 32 | 1 | within |
| notice-burst-5 | 44.257 | 62 | 32 | 1 | within |
| notice-burst-5 | 44.529 | 62 | 32 | 1 | within |
| notice-burst-5 | 46.450 | 62 | 32 | 1 | within |
| notice-burst-5 | 46.721 | 62 | 32 | 1 | within |
| notice-burst-5 | 48.386 | 62 | 32 | 1 | within |
| notice-burst-5 | 48.645 | 62 | 32 | 1 | within |
| notice-burst-5 | 50.254 | 62 | 32 | 1 | within |
| notice-burst-5 | 50.545 | 62 | 32 | 1 | within |
| notice-burst-5 | 52.434 | 62 | 32 | 1 | within |
| notice-burst-6 | 19.724 | 62 | 32 | 1 | within |
| notice-burst-6 | 23.411 | 62 | 32 | 1 | within |
| notice-burst-6 | 3.575 | 62 | 32 | 1 | within |
| notice-burst-6 | 3.871 | 62 | 32 | 1 | within |
| notice-burst-6 | 4.854 | 62 | 32 | 1 | within |
| notice-burst-6 | 5.149 | 62 | 32 | 1 | within |
| notice-burst-6 | 5.746 | 62 | 32 | 1 | within |
| notice-burst-6 | 6.039 | 62 | 32 | 1 | within |
| notice-burst-6 | 23.695 | 62 | 32 | 1 | within |
| notice-burst-6 | 25.449 | 62 | 32 | 1 | within |
| notice-burst-6 | 25.730 | 62 | 32 | 1 | within |
| notice-burst-6 | 27.482 | 62 | 32 | 1 | within |
| notice-burst-6 | 27.764 | 62 | 32 | 1 | within |
| notice-burst-6 | 29.249 | 62 | 32 | 1 | within |
| notice-burst-6 | 29.530 | 62 | 32 | 1 | within |
| notice-burst-6 | 31.273 | 62 | 32 | 1 | within |
| notice-burst-6 | 31.554 | 62 | 32 | 1 | within |
| notice-burst-6 | 33.381 | 62 | 32 | 1 | within |
| notice-burst-6 | 2.376 | 62 | 32 | 1 | within |
| notice-burst-6 | 2.689 | 62 | 32 | 1 | within |
| notice-burst-6 | 33.659 | 62 | 32 | 1 | within |
| notice-burst-6 | 35.380 | 62 | 32 | 1 | within |
| notice-burst-6 | 35.655 | 62 | 32 | 1 | within |
| notice-burst-6 | 37.369 | 62 | 32 | 1 | within |
| notice-burst-6 | 37.647 | 62 | 32 | 1 | within |
| notice-burst-6 | 39.354 | 62 | 32 | 1 | within |
| notice-burst-6 | 39.626 | 62 | 32 | 1 | within |
| notice-burst-6 | 41.319 | 62 | 32 | 1 | within |
| notice-burst-6 | 41.590 | 62 | 32 | 1 | within |
| notice-burst-6 | 43.366 | 62 | 32 | 1 | within |
| notice-burst-6 | 43.635 | 62 | 32 | 1 | within |
| notice-burst-6 | 45.317 | 62 | 32 | 1 | within |
| notice-burst-6 | 45.589 | 62 | 32 | 1 | within |
| notice-burst-6 | 47.261 | 62 | 32 | 1 | within |
| notice-burst-6 | 47.533 | 62 | 32 | 1 | within |
| notice-burst-6 | 49.446 | 62 | 32 | 1 | within |
| notice-burst-6 | 49.704 | 62 | 32 | 1 | within |
| notice-burst-6 | 51.312 | 62 | 32 | 1 | within |
| notice-burst-6 | 51.604 | 62 | 32 | 1 | within |
| notice-burst-6 | 53.336 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.039 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.329 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.619 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.910 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.888 | 62 | 32 | 1 | within |
| notice-burst-7 | 6.181 | 62 | 32 | 1 | within |
| notice-burst-7 | 6.539 | 62 | 32 | 1 | within |
| notice-burst-7 | 6.829 | 62 | 32 | 1 | within |
| notice-burst-7 | 20.420 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.099 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.380 | 62 | 32 | 1 | within |
| notice-burst-7 | 26.131 | 62 | 32 | 1 | within |
| notice-burst-7 | 26.413 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.159 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.440 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.183 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.464 | 62 | 32 | 1 | within |
| notice-burst-7 | 32.198 | 62 | 32 | 1 | within |
| notice-burst-7 | 32.467 | 62 | 32 | 1 | within |
| notice-burst-7 | 34.293 | 62 | 32 | 1 | within |
| notice-burst-7 | 3.696 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.011 | 62 | 32 | 1 | within |
| notice-burst-7 | 34.565 | 62 | 32 | 1 | within |
| notice-burst-7 | 36.280 | 62 | 32 | 1 | within |
| notice-burst-7 | 36.558 | 62 | 32 | 1 | within |
| notice-burst-7 | 38.266 | 62 | 32 | 1 | within |
| notice-burst-7 | 38.537 | 62 | 32 | 1 | within |
| notice-burst-7 | 40.231 | 62 | 32 | 1 | within |
| notice-burst-7 | 40.502 | 62 | 32 | 1 | within |
| notice-burst-7 | 42.189 | 62 | 32 | 1 | within |
| notice-burst-7 | 42.458 | 62 | 32 | 1 | within |
| notice-burst-7 | 44.235 | 62 | 32 | 1 | within |
| notice-burst-7 | 44.507 | 62 | 32 | 1 | within |
| notice-burst-7 | 46.179 | 62 | 32 | 1 | within |
| notice-burst-7 | 46.451 | 62 | 32 | 1 | within |
| notice-burst-7 | 48.116 | 62 | 32 | 1 | within |
| notice-burst-7 | 48.373 | 62 | 32 | 1 | within |
| notice-burst-7 | 50.228 | 62 | 32 | 1 | within |
| notice-burst-7 | 50.519 | 62 | 32 | 1 | within |
| notice-burst-7 | 52.164 | 62 | 32 | 1 | within |

Latest: 53.336 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 303 | 73,646 (0.736) | 50,437 (0.504) |
| notice-every-1 | 303 | 73,646 (0.736) | 50,437 (0.504) |
| notice-every-2 | 303 | 80,007 (0.800) | 50,437 (0.504) |
| notice-every-3 | 303 | 73,646 (0.736) | 50,437 (0.504) |
| notice-every-4 | 303 | 73,646 (0.736) | 50,437 (0.504) |
| notice-every-5 | 303 | 73,646 (0.736) | 50,437 (0.504) |
| notice-every-6 | 303 | 73,646 (0.736) | 50,437 (0.504) |
| notice-every-7 | 303 | 73,646 (0.736) | 50,437 (0.504) |
| notice-burst-0 | 313 | 114,024 (1.140) | 50,437 (0.504) |
| notice-burst-1 | 313 | 118,302 (1.183) | 50,437 (0.504) |
| notice-burst-2 | 313 | 113,745 (1.137) | 50,437 (0.504) |
| notice-burst-3 | 313 | 116,752 (1.168) | 50,437 (0.504) |
| notice-burst-4 | 313 | 118,818 (1.188) | 50,437 (0.504) |
| notice-burst-5 | 313 | 118,337 (1.183) | 50,437 (0.504) |
| notice-burst-6 | 313 | 113,987 (1.140) | 50,437 (0.504) |
| notice-burst-7 | 313 | 118,256 (1.183) | 50,437 (0.504) |

Longest pass that carries a step: 118,818 CPU cycles (1.188 ms), notice-burst-4; longest step: 50,437 (0.504 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 356,090 | 3.561 | 62 | 66 | fits | 68,690 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 385,743 | 3.857 | 62 | 66 | fits | 68,690 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 563,126 | 5.631 | 62 | 66 | fits | 67,685 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 592,522 | 5.925 | 62 | 66 | fits | 67,685 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 768,958 | 7.690 | 62 | 66 | fits | 66,963 | 200 | 0.140 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 798,266 | 7.983 | 62 | 66 | fits | 66,963 | 200 | 0.140 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 973,756 | 9.738 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 1,002,996 | 10.030 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 1,159,837 | 11.598 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 1,188,980 | 11.890 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 1,362,977 | 13.630 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 1,392,055 | 13.921 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 1,565,955 | 15.660 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 1,595,112 | 15.951 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 1,768,323 | 17.683 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 1,797,401 | 17.974 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 2,240,699 | 22.407 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 2,270,032 | 22.700 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 2,363,481 | 23.635 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 2,392,449 | 23.924 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 2,562,104 | 25.621 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 2,591,512 | 25.915 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 2,761,156 | 27.612 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 2,790,485 | 27.905 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 2,959,584 | 29.596 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 2,988,913 | 29.889 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 3,166,776 | 31.668 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 3,195,886 | 31.959 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 3,362,617 | 33.626 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 3,391,565 | 33.916 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 3,557,957 | 35.580 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 3,587,071 | 35.871 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 3,752,217 | 37.522 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 3,781,396 | 37.814 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 4,271,217 | 42.712 | 62 | 66 | fits | 37,980 | 101 | 0.315 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 4,659,259 | 46.593 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 4,685,019 | 46.850 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 4,870,037 | 48.700 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 4,899,151 | 48.992 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 5,069,888 | 50.699 | 62 | 66 | fits | 38,958 | 103 | 0.226 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 791,056 | 7.911 | 20 | 200 | fits | 158,397 | 116 | 0.487 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 893,172 | 8.932 | 20 | 20 | fits | 122,384 | 45 | 0.748 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 564,754 | 5.648 | 20 | 24 | fits | 228,022 | 170 | 0.462 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 731,313 | 7.313 | 20 | 50 | fits | 158,397 | 116 | 0.487 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 1,361,277 | 13.613 | 20 | 20 | fits | 119,530 | 52 | 0.560 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 198,635 | 1.986 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 281,202 | 2.812 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 564,602 | 5.646 | 62 | 66 | fits | 67,073 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 593,822 | 5.938 | 62 | 66 | fits | 67,073 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 357,156 | 3.572 | 62 | 66 | fits | 69,954 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 387,216 | 3.872 | 62 | 66 | fits | 69,954 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 770,373 | 7.704 | 62 | 66 | fits | 66,995 | 200 | 0.141 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 799,681 | 7.997 | 62 | 66 | fits | 66,995 | 200 | 0.141 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 948,825 | 9.488 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 978,065 | 9.781 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 1,160,918 | 11.609 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 1,190,061 | 11.901 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 1,364,072 | 13.641 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 1,393,150 | 13.931 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 1,567,064 | 15.671 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 1,596,221 | 15.962 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 1,769,446 | 17.694 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 1,798,524 | 17.985 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 2,241,939 | 22.419 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 2,271,272 | 22.713 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 2,364,735 | 23.647 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 2,393,703 | 23.937 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 2,563,372 | 25.634 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 2,592,780 | 25.928 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 2,762,438 | 27.624 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 2,791,767 | 27.918 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 2,960,880 | 29.609 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 2,990,209 | 29.902 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 3,168,086 | 31.681 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 3,197,196 | 31.972 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 3,363,913 | 33.639 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 3,392,861 | 33.929 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 3,559,239 | 35.592 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 3,588,353 | 35.884 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 3,753,485 | 37.535 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 3,782,664 | 37.827 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 4,272,350 | 42.724 | 62 | 66 | fits | 37,980 | 101 | 0.315 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 4,660,392 | 46.604 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 4,686,152 | 46.862 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 4,846,663 | 48.467 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 4,875,777 | 48.758 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 5,070,654 | 50.707 | 62 | 66 | fits | 39,010 | 103 | 0.226 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if1` | 787,950 | 7.880 | 20 | 200 | fits | 168,152 | 128 | 0.464 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 914,701 | 9.147 | 20 | 20 | fits | 147,019 | 52 | 0.697 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if1` | 440,608 | 4.406 | 20 | 24 | fits | 169,730 | 97 | 0.505 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 728,207 | 7.282 | 20 | 50 | fits | 168,152 | 128 | 0.464 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if1` | 1,390,016 | 13.900 | 20 | 20 | fits | 121,878 | 50 | 0.515 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 228,977 | 2.290 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if1` | 334,747 | 3.347 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 609,851 | 6.099 | 62 | 66 | fits | 67,261 | 202 | 0.141 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 639,080 | 6.391 | 62 | 66 | fits | 67,261 | 202 | 0.141 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 213,084 | 2.131 | 62 | 66 | fits | 70,199 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 242,950 | 2.429 | 62 | 66 | fits | 70,199 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 815,492 | 8.155 | 62 | 66 | fits | 67,127 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 844,800 | 8.448 | 62 | 66 | fits | 67,127 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 430,777 | 4.308 | 62 | 66 | fits | 69,543 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 460,792 | 4.608 | 62 | 66 | fits | 69,543 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 1,020,366 | 10.204 | 62 | 66 | fits | 67,046 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 1,049,444 | 10.494 | 62 | 66 | fits | 67,046 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 1,223,505 | 12.235 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 1,252,583 | 12.526 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 1,409,495 | 14.095 | 62 | 66 | fits | 67,248 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 1,438,717 | 14.387 | 62 | 66 | fits | 67,248 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 1,611,880 | 16.119 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 1,640,958 | 16.410 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 1,813,628 | 18.136 | 62 | 66 | fits | 66,727 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 1,842,706 | 18.427 | 62 | 66 | fits | 66,727 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 2,013,188 | 20.132 | 62 | 66 | fits | 65,180 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 2,042,139 | 20.421 | 62 | 66 | fits | 65,180 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 2,423,143 | 24.231 | 62 | 66 | fits | 37,358 | 101 | 0.269 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 2,823,048 | 28.230 | 62 | 66 | fits | 66,787 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 2,850,700 | 28.507 | 62 | 66 | fits | 66,787 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 3,021,955 | 30.220 | 62 | 66 | fits | 66,629 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 3,049,786 | 30.498 | 62 | 66 | fits | 66,629 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 3,220,444 | 32.204 | 62 | 66 | fits | 65,553 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 3,247,578 | 32.476 | 62 | 66 | fits | 65,553 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 3,427,553 | 34.276 | 62 | 66 | fits | 66,068 | 201 | 0.165 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 3,454,788 | 34.548 | 62 | 66 | fits | 66,068 | 201 | 0.165 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 3,623,514 | 36.235 | 62 | 66 | fits | 65,023 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 3,650,451 | 36.505 | 62 | 66 | fits | 65,023 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 3,818,693 | 38.187 | 62 | 66 | fits | 65,242 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 3,845,820 | 38.458 | 62 | 66 | fits | 65,242 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 4,013,057 | 40.131 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 4,040,213 | 40.402 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 4,480,018 | 44.800 | 62 | 66 | fits | 39,095 | 102 | 0.227 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 4,811,721 | 48.117 | 62 | 66 | fits | 58,251 | 198 | 0.133 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 4,836,193 | 48.362 | 62 | 66 | fits | 58,251 | 198 | 0.133 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 5,024,652 | 50.247 | 62 | 66 | fits | 66,702 | 203 | 0.103 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 5,054,120 | 50.541 | 62 | 66 | fits | 66,702 | 203 | 0.103 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if1` | 762,770 | 7.628 | 20 | 200 | fits | 166,674 | 125 | 0.433 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 912,787 | 9.128 | 20 | 20 | fits | 148,363 | 53 | 0.718 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if1` | 468,807 | 4.688 | 20 | 24 | fits | 173,420 | 102 | 0.497 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 703,027 | 7.030 | 20 | 50 | fits | 166,674 | 125 | 0.433 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if1` | 1,389,333 | 13.893 | 20 | 20 | fits | 131,230 | 52 | 0.500 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 194,467 | 1.945 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if1` | 300,153 | 3.002 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 558,878 | 5.589 | 62 | 66 | fits | 67,187 | 203 | 0.144 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 588,098 | 5.881 | 62 | 66 | fits | 67,187 | 203 | 0.144 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 351,633 | 3.516 | 62 | 66 | fits | 69,954 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 381,693 | 3.817 | 62 | 66 | fits | 69,954 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 764,715 | 7.647 | 62 | 66 | fits | 66,995 | 200 | 0.141 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 794,023 | 7.940 | 62 | 66 | fits | 66,995 | 200 | 0.141 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 969,513 | 9.695 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 998,753 | 9.988 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 1,155,580 | 11.556 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 1,184,723 | 11.847 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 1,358,720 | 13.587 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 1,387,798 | 13.878 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 1,561,698 | 15.617 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 1,590,855 | 15.909 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 1,764,066 | 17.641 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 1,793,144 | 17.931 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 2,236,545 | 22.365 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 2,265,878 | 22.659 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 2,359,327 | 23.593 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 2,388,295 | 23.883 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 2,557,964 | 25.580 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 2,587,372 | 25.874 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 2,757,030 | 27.570 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 2,786,359 | 27.864 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 2,955,472 | 29.555 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 2,984,801 | 29.848 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 3,162,678 | 31.627 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 3,191,788 | 31.918 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 3,358,505 | 33.585 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 3,387,453 | 33.875 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 3,553,831 | 35.538 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 3,582,945 | 35.829 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 3,748,077 | 37.481 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 3,777,256 | 37.773 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 4,267,193 | 42.672 | 62 | 66 | fits | 37,980 | 101 | 0.315 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 4,655,235 | 46.552 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 4,680,995 | 46.810 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 4,866,013 | 48.660 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 4,895,127 | 48.951 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 5,059,649 | 50.596 | 62 | 66 | fits | 37,703 | 103 | 0.176 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if1` | 784,591 | 7.846 | 20 | 200 | fits | 157,550 | 105 | 0.487 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 910,015 | 9.100 | 20 | 20 | fits | 145,692 | 46 | 0.705 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if1` | 467,142 | 4.671 | 20 | 24 | fits | 171,834 | 98 | 0.505 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 724,848 | 7.248 | 20 | 50 | fits | 157,550 | 105 | 0.487 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if1` | 1,385,055 | 13.851 | 20 | 20 | fits | 121,878 | 50 | 0.515 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 229,025 | 2.290 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if1` | 334,753 | 3.348 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 610,003 | 6.100 | 62 | 66 | fits | 67,275 | 202 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 639,165 | 6.392 | 62 | 66 | fits | 67,275 | 202 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 815,871 | 8.159 | 62 | 66 | fits | 67,332 | 203 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 845,058 | 8.451 | 62 | 66 | fits | 67,332 | 203 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 213,255 | 2.133 | 62 | 66 | fits | 70,140 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 243,205 | 2.432 | 62 | 66 | fits | 70,140 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 430,901 | 4.309 | 62 | 66 | fits | 69,557 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 460,849 | 4.608 | 62 | 66 | fits | 69,557 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 1,020,807 | 10.208 | 62 | 66 | fits | 67,028 | 201 | 0.140 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 1,049,818 | 10.498 | 62 | 66 | fits | 67,028 | 201 | 0.140 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 1,223,940 | 12.239 | 62 | 66 | fits | 66,919 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 1,252,951 | 12.530 | 62 | 66 | fits | 66,919 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 1,409,883 | 14.099 | 62 | 66 | fits | 67,262 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 1,439,038 | 14.390 | 62 | 66 | fits | 67,262 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 1,612,282 | 16.123 | 62 | 66 | fits | 66,768 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 1,641,293 | 16.413 | 62 | 66 | fits | 66,768 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 1,814,044 | 18.140 | 62 | 66 | fits | 66,741 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 1,843,055 | 18.431 | 62 | 66 | fits | 66,741 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 2,013,618 | 20.136 | 62 | 66 | fits | 65,194 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 2,042,502 | 20.425 | 62 | 66 | fits | 65,194 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 2,423,484 | 24.235 | 62 | 66 | fits | 37,423 | 101 | 0.269 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 2,823,497 | 28.235 | 62 | 66 | fits | 66,787 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 2,851,149 | 28.511 | 62 | 66 | fits | 66,787 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 3,022,418 | 30.224 | 62 | 66 | fits | 66,629 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 3,050,249 | 30.502 | 62 | 66 | fits | 66,629 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 3,220,921 | 32.209 | 62 | 66 | fits | 65,553 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 3,248,055 | 32.481 | 62 | 66 | fits | 65,553 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 3,428,034 | 34.280 | 62 | 66 | fits | 66,068 | 201 | 0.165 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 3,455,269 | 34.553 | 62 | 66 | fits | 66,068 | 201 | 0.165 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 3,623,995 | 36.240 | 62 | 66 | fits | 65,023 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 3,650,932 | 36.509 | 62 | 66 | fits | 65,023 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 3,819,174 | 38.192 | 62 | 66 | fits | 65,242 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 3,846,301 | 38.463 | 62 | 66 | fits | 65,242 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 4,013,538 | 40.135 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 4,040,694 | 40.407 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 4,480,701 | 44.807 | 62 | 66 | fits | 39,095 | 102 | 0.227 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 4,812,404 | 48.124 | 62 | 66 | fits | 58,251 | 198 | 0.133 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 4,836,876 | 48.369 | 62 | 66 | fits | 58,251 | 198 | 0.133 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 5,025,498 | 50.255 | 62 | 66 | fits | 66,702 | 203 | 0.103 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 5,054,966 | 50.550 | 62 | 66 | fits | 66,702 | 203 | 0.103 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if1` | 785,768 | 7.858 | 20 | 200 | fits | 159,355 | 110 | 0.491 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 913,603 | 9.136 | 20 | 20 | fits | 148,103 | 41 | 0.740 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if1` | 558,567 | 5.586 | 20 | 24 | fits | 227,053 | 170 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 726,025 | 7.260 | 20 | 50 | fits | 159,355 | 110 | 0.491 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if1` | 1,352,005 | 13.520 | 20 | 20 | fits | 90,110 | 38 | 0.584 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 211,528 | 2.115 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if1` | 293,534 | 2.935 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 564,602 | 5.646 | 62 | 66 | fits | 67,073 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 593,822 | 5.938 | 62 | 66 | fits | 67,073 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 357,156 | 3.572 | 62 | 66 | fits | 69,954 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 387,216 | 3.872 | 62 | 66 | fits | 69,954 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 770,373 | 7.704 | 62 | 66 | fits | 66,995 | 200 | 0.141 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 799,681 | 7.997 | 62 | 66 | fits | 66,995 | 200 | 0.141 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 948,825 | 9.488 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 978,065 | 9.781 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 1,160,918 | 11.609 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 1,190,061 | 11.901 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 1,364,072 | 13.641 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 1,393,150 | 13.931 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 1,567,064 | 15.671 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 1,596,221 | 15.962 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 1,769,446 | 17.694 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 1,798,524 | 17.985 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 2,241,985 | 22.420 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 2,271,318 | 22.713 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 2,364,781 | 23.648 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 2,393,749 | 23.937 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 2,563,418 | 25.634 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 2,592,826 | 25.928 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 2,762,484 | 27.625 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 2,791,813 | 27.918 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 2,960,926 | 29.609 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 2,990,255 | 29.903 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 3,168,132 | 31.681 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 3,197,242 | 31.972 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 3,363,959 | 33.640 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 3,392,907 | 33.929 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 3,559,285 | 35.593 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 3,588,399 | 35.884 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 3,753,531 | 37.535 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 3,782,710 | 37.827 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 4,272,396 | 42.724 | 62 | 66 | fits | 37,980 | 101 | 0.315 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 4,660,438 | 46.604 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 4,686,198 | 46.862 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 4,846,709 | 48.467 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 4,875,823 | 48.758 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 5,064,794 | 50.648 | 62 | 66 | fits | 37,703 | 103 | 0.176 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if1` | 757,200 | 7.572 | 20 | 200 | fits | 165,291 | 122 | 0.435 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 914,623 | 9.146 | 20 | 20 | fits | 150,191 | 57 | 0.717 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if1` | 439,980 | 4.400 | 20 | 24 | fits | 169,869 | 97 | 0.504 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 697,457 | 6.975 | 20 | 50 | fits | 165,291 | 122 | 0.435 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if1` | 1,381,220 | 13.812 | 20 | 20 | fits | 110,846 | 44 | 0.538 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 192,473 | 1.925 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if1` | 298,250 | 2.982 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 356,101 | 3.561 | 62 | 66 | fits | 68,690 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 385,754 | 3.858 | 62 | 66 | fits | 68,690 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 563,055 | 5.631 | 62 | 66 | fits | 67,685 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 592,451 | 5.925 | 62 | 66 | fits | 67,685 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 768,873 | 7.689 | 62 | 66 | fits | 66,963 | 200 | 0.140 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 798,181 | 7.982 | 62 | 66 | fits | 66,963 | 200 | 0.140 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 973,657 | 9.737 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 1,002,897 | 10.029 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 1,159,724 | 11.597 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 1,188,867 | 11.889 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 1,362,878 | 13.629 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 1,391,956 | 13.920 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 1,565,870 | 15.659 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 1,595,027 | 15.950 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 1,768,252 | 17.683 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 1,797,330 | 17.973 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 2,240,688 | 22.407 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 2,270,021 | 22.700 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 2,363,484 | 23.635 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 2,392,452 | 23.925 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 2,562,107 | 25.621 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 2,591,515 | 25.915 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 2,761,159 | 27.612 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 2,790,488 | 27.905 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 2,959,587 | 29.596 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 2,988,916 | 29.889 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 3,166,779 | 31.668 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 3,195,889 | 31.959 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 3,362,606 | 33.626 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 3,391,554 | 33.916 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 3,557,932 | 35.579 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 3,587,046 | 35.870 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 3,752,178 | 37.522 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 3,781,357 | 37.814 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 4,271,350 | 42.714 | 62 | 66 | fits | 37,980 | 101 | 0.315 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 4,659,392 | 46.594 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 4,685,152 | 46.852 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 4,870,184 | 48.702 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 4,899,298 | 48.993 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 5,063,820 | 50.638 | 62 | 66 | fits | 37,703 | 103 | 0.176 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if1` | 778,156 | 7.782 | 20 | 200 | fits | 157,315 | 108 | 0.498 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 906,380 | 9.064 | 20 | 20 | fits | 148,492 | 41 | 0.744 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if1` | 552,761 | 5.528 | 20 | 24 | fits | 225,479 | 164 | 0.461 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 718,413 | 7.184 | 20 | 50 | fits | 157,315 | 108 | 0.498 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if1` | 1,378,507 | 13.785 | 20 | 20 | fits | 95,155 | 47 | 0.643 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 203,246 | 2.032 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if1` | 315,189 | 3.152 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 356,266 | 3.563 | 62 | 66 | fits | 68,690 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 385,919 | 3.859 | 62 | 66 | fits | 68,690 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 563,301 | 5.633 | 62 | 66 | fits | 67,685 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 592,697 | 5.927 | 62 | 66 | fits | 67,685 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 769,137 | 7.691 | 62 | 66 | fits | 66,963 | 200 | 0.140 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 798,445 | 7.984 | 62 | 66 | fits | 66,963 | 200 | 0.140 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 973,939 | 9.739 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 1,003,179 | 10.032 | 62 | 66 | fits | 66,893 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 1,160,006 | 11.600 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 1,189,149 | 11.891 | 62 | 66 | fits | 67,328 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 1,363,160 | 13.632 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 1,392,238 | 13.922 | 62 | 66 | fits | 66,914 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 1,566,152 | 15.662 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 1,595,309 | 15.953 | 62 | 66 | fits | 66,999 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 1,768,534 | 17.685 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 1,797,612 | 17.976 | 62 | 66 | fits | 66,754 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 2,241,075 | 22.411 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 2,270,408 | 22.704 | 62 | 66 | fits | 67,269 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 2,363,871 | 23.639 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 2,392,839 | 23.928 | 62 | 66 | fits | 65,531 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 2,562,508 | 25.625 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 2,591,916 | 25.919 | 62 | 66 | fits | 66,525 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 2,761,574 | 27.616 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 2,790,903 | 27.909 | 62 | 66 | fits | 66,080 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 2,960,016 | 29.600 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 2,989,345 | 29.893 | 62 | 66 | fits | 66,180 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 3,167,222 | 31.672 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 3,196,332 | 31.963 | 62 | 66 | fits | 65,642 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 3,363,049 | 33.630 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 3,391,997 | 33.920 | 62 | 66 | fits | 64,942 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 3,558,375 | 35.584 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 3,587,489 | 35.875 | 62 | 66 | fits | 65,024 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 3,752,621 | 37.526 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 3,781,800 | 37.818 | 62 | 66 | fits | 64,888 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 4,271,486 | 42.715 | 62 | 66 | fits | 37,980 | 101 | 0.315 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 4,659,528 | 46.595 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 4,685,288 | 46.853 | 62 | 66 | fits | 63,813 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 4,870,320 | 48.703 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 4,899,434 | 48.994 | 62 | 66 | fits | 62,495 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 5,063,956 | 50.640 | 62 | 66 | fits | 37,703 | 103 | 0.176 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if1` | 801,854 | 8.019 | 20 | 200 | fits | 169,584 | 132 | 0.467 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 927,241 | 9.272 | 20 | 20 | fits | 145,655 | 46 | 0.704 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if1` | 436,352 | 4.364 | 20 | 24 | fits | 169,694 | 97 | 0.504 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 742,111 | 7.421 | 20 | 50 | fits | 169,584 | 132 | 0.467 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if1` | 1,393,666 | 13.937 | 20 | 20 | fits | 121,848 | 50 | 0.514 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 223,015 | 2.230 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if1` | 334,963 | 3.350 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 229,326 | 2.293 | 62 | 66 | fits | 97,069 | 212 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 258,770 | 2.588 | 62 | 66 | fits | 97,069 | 212 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 346,660 | 3.467 | 62 | 66 | fits | 70,089 | 201 | 0.145 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 375,986 | 3.760 | 62 | 66 | fits | 70,089 | 201 | 0.145 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 474,501 | 4.745 | 62 | 66 | fits | 114,024 | 210 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 503,744 | 5.037 | 62 | 66 | fits | 114,024 | 210 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 1,963,629 | 19.636 | 62 | 66 | fits | 41,455 | 101 | 0.349 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 2,332,293 | 23.323 | 62 | 66 | fits | 67,775 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 564,093 | 5.641 | 62 | 66 | fits | 65,236 | 203 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 593,204 | 5.932 | 62 | 66 | fits | 65,236 | 203 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 2,360,475 | 23.605 | 62 | 66 | fits | 67,775 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 2,535,972 | 25.360 | 62 | 66 | fits | 67,480 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 2,564,187 | 25.642 | 62 | 66 | fits | 67,480 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 2,713,100 | 27.131 | 62 | 66 | fits | 67,056 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 2,741,190 | 27.412 | 62 | 66 | fits | 67,056 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 2,915,967 | 29.160 | 62 | 66 | fits | 67,116 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 2,944,099 | 29.441 | 62 | 66 | fits | 67,116 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 3,117,911 | 31.179 | 62 | 66 | fits | 65,811 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 3,144,813 | 31.448 | 62 | 66 | fits | 65,811 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 3,326,874 | 33.269 | 62 | 66 | fits | 67,154 | 201 | 0.165 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 3,354,500 | 33.545 | 62 | 66 | fits | 67,154 | 201 | 0.165 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 3,526,467 | 35.265 | 62 | 66 | fits | 66,413 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 3,553,953 | 35.540 | 62 | 66 | fits | 66,413 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 3,725,362 | 37.254 | 62 | 66 | fits | 66,585 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 3,753,137 | 37.531 | 62 | 66 | fits | 66,585 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 3,923,867 | 39.239 | 62 | 66 | fits | 65,568 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 3,951,010 | 39.510 | 62 | 66 | fits | 65,568 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 4,120,322 | 41.203 | 62 | 66 | fits | 65,277 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 4,147,403 | 41.474 | 62 | 66 | fits | 65,277 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 4,325,060 | 43.251 | 62 | 66 | fits | 65,352 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 4,351,932 | 43.519 | 62 | 66 | fits | 65,352 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 4,520,128 | 45.201 | 62 | 66 | fits | 65,321 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 4,547,334 | 45.473 | 62 | 66 | fits | 65,321 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 4,714,571 | 47.146 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 4,741,727 | 47.417 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 4,933,003 | 49.330 | 62 | 66 | fits | 63,572 | 200 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 4,958,847 | 49.588 | 62 | 66 | fits | 63,572 | 200 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 5,127,573 | 51.276 | 62 | 66 | fits | 64,292 | 200 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 5,157,401 | 51.574 | 62 | 66 | fits | 64,292 | 200 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 5,331,440 | 53.314 | 62 | 66 | fits | 37,992 | 103 | 0.181 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 756,815 | 7.568 | 20 | 200 | fits | 179,863 | 108 | 0.438 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 869,577 | 8.696 | 20 | 20 | fits | 133,030 | 38 | 0.782 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 536,480 | 5.365 | 20 | 24 | fits | 221,974 | 166 | 0.443 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 697,072 | 6.971 | 20 | 50 | fits | 179,863 | 108 | 0.438 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 1,267,771 | 12.678 | 20 | 20 | fits | 68,031 | 27 | 0.663 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 485,194 | 4.852 | 62 | 66 | fits | 65,208 | 203 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 514,156 | 5.142 | 62 | 66 | fits | 65,208 | 203 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 680,228 | 6.802 | 62 | 66 | fits | 64,248 | 203 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 709,164 | 7.092 | 62 | 66 | fits | 64,248 | 203 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 2,067,897 | 20.679 | 62 | 66 | fits | 41,438 | 101 | 0.347 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 2,435,424 | 24.354 | 62 | 66 | fits | 67,838 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 2,463,583 | 24.636 | 62 | 66 | fits | 67,838 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 2,638,165 | 26.382 | 62 | 66 | fits | 67,067 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 613,798 | 6.138 | 62 | 66 | fits | 92,267 | 210 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 643,518 | 6.435 | 62 | 66 | fits | 92,267 | 210 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 2,666,263 | 26.663 | 62 | 66 | fits | 67,067 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 2,840,864 | 28.409 | 62 | 66 | fits | 67,349 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 2,869,144 | 28.691 | 62 | 66 | fits | 67,349 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 3,043,239 | 30.432 | 62 | 66 | fits | 66,978 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 231,432 | 2.314 | 62 | 66 | fits | 72,183 | 203 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 262,064 | 2.621 | 62 | 66 | fits | 72,183 | 203 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 3,071,403 | 30.714 | 62 | 66 | fits | 66,978 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 3,244,712 | 32.447 | 62 | 66 | fits | 65,817 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 3,271,614 | 32.716 | 62 | 66 | fits | 65,817 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 3,428,460 | 34.285 | 62 | 66 | fits | 66,575 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 393,299 | 3.933 | 62 | 66 | fits | 118,302 | 210 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 424,765 | 4.248 | 62 | 66 | fits | 118,302 | 210 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 3,455,653 | 34.557 | 62 | 66 | fits | 66,575 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 3,627,038 | 36.270 | 62 | 66 | fits | 66,665 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 3,654,845 | 36.548 | 62 | 66 | fits | 66,665 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 3,825,625 | 38.256 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 3,852,768 | 38.528 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 4,047,367 | 40.474 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 4,074,448 | 40.744 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 4,243,154 | 42.432 | 62 | 66 | fits | 64,925 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 4,270,035 | 42.700 | 62 | 66 | fits | 64,925 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 4,447,799 | 44.478 | 62 | 66 | fits | 65,684 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 4,475,005 | 44.750 | 62 | 66 | fits | 65,684 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 4,642,170 | 46.422 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 4,669,326 | 46.693 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 4,835,827 | 48.358 | 62 | 66 | fits | 63,536 | 200 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 4,861,556 | 48.616 | 62 | 66 | fits | 63,536 | 200 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 5,022,469 | 50.225 | 62 | 66 | fits | 62,540 | 200 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 5,051,630 | 50.516 | 62 | 66 | fits | 62,540 | 200 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 5,257,233 | 52.572 | 62 | 66 | fits | 39,365 | 103 | 0.237 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if1` | 834,370 | 8.344 | 20 | 200 | fits | 164,956 | 100 | 0.480 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 960,533 | 9.605 | 20 | 20 | fits | 146,431 | 40 | 0.743 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if1` | 461,113 | 4.611 | 20 | 24 | fits | 224,785 | 167 | 0.469 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 774,627 | 7.746 | 20 | 50 | fits | 164,956 | 100 | 0.480 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if1` | 1,358,410 | 13.584 | 20 | 20 | fits | 67,808 | 27 | 0.663 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 446,344 | 4.463 | 62 | 66 | fits | 113,745 | 212 | 0.181 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 475,515 | 4.755 | 62 | 66 | fits | 113,745 | 212 | 0.181 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 535,450 | 5.354 | 62 | 66 | fits | 66,430 | 203 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 564,545 | 5.645 | 62 | 66 | fits | 66,430 | 203 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 1,957,994 | 19.580 | 62 | 66 | fits | 41,526 | 101 | 0.347 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 2,352,944 | 23.529 | 62 | 66 | fits | 68,041 | 201 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 236,072 | 2.361 | 62 | 66 | fits | 96,924 | 212 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 266,369 | 2.664 | 62 | 66 | fits | 96,924 | 212 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 2,381,431 | 23.814 | 62 | 66 | fits | 68,041 | 201 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 2,530,587 | 25.306 | 62 | 66 | fits | 67,369 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 2,558,691 | 25.587 | 62 | 66 | fits | 67,369 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 2,733,864 | 27.339 | 62 | 66 | fits | 67,390 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 2,762,112 | 27.621 | 62 | 66 | fits | 67,390 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 2,936,631 | 29.366 | 62 | 66 | fits | 66,977 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 2,964,721 | 29.647 | 62 | 66 | fits | 66,977 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 3,139,034 | 31.390 | 62 | 66 | fits | 67,041 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 3,167,166 | 31.672 | 62 | 66 | fits | 67,041 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 3,349,955 | 33.500 | 62 | 66 | fits | 67,347 | 201 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 305,087 | 3.051 | 62 | 66 | fits | 69,985 | 201 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 335,524 | 3.355 | 62 | 66 | fits | 69,985 | 201 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 3,377,689 | 33.777 | 62 | 66 | fits | 67,347 | 201 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 3,549,785 | 35.498 | 62 | 66 | fits | 66,487 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 3,577,345 | 35.773 | 62 | 66 | fits | 66,487 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 3,748,768 | 37.488 | 62 | 66 | fits | 66,585 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 3,776,543 | 37.765 | 62 | 66 | fits | 66,585 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 3,947,287 | 39.473 | 62 | 66 | fits | 65,568 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 3,974,430 | 39.744 | 62 | 66 | fits | 65,568 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 4,143,756 | 41.438 | 62 | 66 | fits | 65,277 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 4,170,837 | 41.708 | 62 | 66 | fits | 65,277 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 4,348,537 | 43.485 | 62 | 66 | fits | 65,352 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 4,375,409 | 43.754 | 62 | 66 | fits | 65,352 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 4,543,619 | 45.436 | 62 | 66 | fits | 65,321 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 4,570,825 | 45.708 | 62 | 66 | fits | 65,321 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 4,738,076 | 47.381 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 4,765,232 | 47.652 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 4,931,747 | 49.317 | 62 | 66 | fits | 63,544 | 200 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 4,957,484 | 49.575 | 62 | 66 | fits | 63,544 | 200 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 5,143,057 | 51.431 | 62 | 66 | fits | 62,581 | 200 | 0.121 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 5,172,218 | 51.722 | 62 | 66 | fits | 62,581 | 200 | 0.121 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 5,328,480 | 53.285 | 62 | 66 | fits | 39,155 | 103 | 0.233 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if1` | 734,691 | 7.347 | 20 | 200 | fits | 177,100 | 106 | 0.438 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 847,248 | 8.472 | 20 | 20 | fits | 132,825 | 38 | 0.781 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if1` | 517,119 | 5.171 | 20 | 24 | fits | 208,825 | 162 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 674,948 | 6.749 | 20 | 50 | fits | 177,100 | 106 | 0.438 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if1` | 1,245,358 | 12.454 | 20 | 20 | fits | 68,037 | 27 | 0.663 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 613,526 | 6.135 | 62 | 66 | fits | 91,255 | 210 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 642,553 | 6.426 | 62 | 66 | fits | 91,255 | 210 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 679,995 | 6.800 | 62 | 66 | fits | 64,737 | 203 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 708,931 | 7.089 | 62 | 66 | fits | 64,737 | 203 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 2,067,923 | 20.679 | 62 | 66 | fits | 41,447 | 101 | 0.347 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 2,435,450 | 24.355 | 62 | 66 | fits | 67,838 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 2,463,609 | 24.636 | 62 | 66 | fits | 67,838 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 2,638,191 | 26.382 | 62 | 66 | fits | 67,431 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 484,075 | 4.841 | 62 | 66 | fits | 68,007 | 203 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 513,961 | 5.140 | 62 | 66 | fits | 68,007 | 203 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 392,890 | 3.929 | 62 | 66 | fits | 116,752 | 210 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 423,290 | 4.233 | 62 | 66 | fits | 116,752 | 210 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 2,666,574 | 26.666 | 62 | 66 | fits | 67,431 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 2,840,999 | 28.410 | 62 | 66 | fits | 66,983 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 2,869,089 | 28.691 | 62 | 66 | fits | 66,983 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 3,043,452 | 30.435 | 62 | 66 | fits | 67,047 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 3,071,584 | 30.716 | 62 | 66 | fits | 67,047 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 3,244,976 | 32.450 | 62 | 66 | fits | 66,553 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 231,238 | 2.312 | 62 | 66 | fits | 71,632 | 203 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 262,250 | 2.623 | 62 | 66 | fits | 71,632 | 203 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 3,272,468 | 32.725 | 62 | 66 | fits | 66,553 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 3,429,336 | 34.293 | 62 | 66 | fits | 67,168 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 3,457,055 | 34.571 | 62 | 66 | fits | 67,168 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 3,628,426 | 36.284 | 62 | 66 | fits | 66,633 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 3,656,201 | 36.562 | 62 | 66 | fits | 66,633 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 3,826,981 | 38.270 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 3,854,124 | 38.541 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 4,048,723 | 40.487 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 4,075,804 | 40.758 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 4,244,510 | 42.445 | 62 | 66 | fits | 64,925 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 4,271,391 | 42.714 | 62 | 66 | fits | 64,925 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 4,449,155 | 44.492 | 62 | 66 | fits | 65,684 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 4,476,361 | 44.764 | 62 | 66 | fits | 65,684 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 4,643,526 | 46.435 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 4,670,682 | 46.707 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 4,837,183 | 48.372 | 62 | 66 | fits | 63,536 | 200 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 4,862,912 | 48.629 | 62 | 66 | fits | 63,536 | 200 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 5,023,825 | 50.238 | 62 | 66 | fits | 62,540 | 200 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 5,052,986 | 50.530 | 62 | 66 | fits | 62,540 | 200 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 5,241,842 | 52.418 | 62 | 66 | fits | 37,600 | 103 | 0.172 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if1` | 832,556 | 8.326 | 20 | 200 | fits | 165,067 | 100 | 0.482 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 958,694 | 9.587 | 20 | 20 | fits | 146,406 | 40 | 0.743 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if1` | 459,234 | 4.592 | 20 | 24 | fits | 224,702 | 167 | 0.468 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 772,813 | 7.728 | 20 | 50 | fits | 165,067 | 100 | 0.482 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if1` | 1,356,595 | 13.566 | 20 | 20 | fits | 67,814 | 27 | 0.663 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,926,201 | 19.262 | 62 | 66 | fits | 41,572 | 101 | 0.349 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 2,294,962 | 22.950 | 62 | 66 | fits | 67,981 | 201 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 2,323,342 | 23.233 | 62 | 66 | fits | 67,981 | 201 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 2,472,245 | 24.722 | 62 | 66 | fits | 67,332 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 337,580 | 3.376 | 62 | 66 | fits | 67,873 | 203 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 367,174 | 3.672 | 62 | 66 | fits | 67,873 | 203 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 467,599 | 4.676 | 62 | 66 | fits | 91,831 | 212 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 497,401 | 4.974 | 62 | 66 | fits | 91,831 | 212 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 534,304 | 5.343 | 62 | 66 | fits | 65,368 | 201 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 563,501 | 5.635 | 62 | 66 | fits | 65,368 | 201 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 2,500,352 | 25.004 | 62 | 66 | fits | 67,332 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 2,675,460 | 26.755 | 62 | 66 | fits | 67,419 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 2,703,731 | 27.037 | 62 | 66 | fits | 67,419 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 2,878,300 | 28.783 | 62 | 66 | fits | 66,983 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 2,906,390 | 29.064 | 62 | 66 | fits | 66,983 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 3,080,753 | 30.808 | 62 | 66 | fits | 67,047 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 3,108,885 | 31.089 | 62 | 66 | fits | 67,047 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 3,291,768 | 32.918 | 62 | 66 | fits | 67,353 | 201 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 244,931 | 2.449 | 62 | 66 | fits | 118,818 | 210 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 276,487 | 2.765 | 62 | 66 | fits | 118,818 | 210 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 3,319,502 | 33.195 | 62 | 66 | fits | 67,353 | 201 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 3,491,620 | 34.916 | 62 | 66 | fits | 66,493 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 3,519,180 | 35.192 | 62 | 66 | fits | 66,493 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 3,690,625 | 36.906 | 62 | 66 | fits | 66,591 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 3,718,400 | 37.184 | 62 | 66 | fits | 66,591 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 3,889,166 | 38.892 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 3,916,309 | 39.163 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 4,085,657 | 40.857 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 4,112,738 | 41.127 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 4,290,431 | 42.904 | 62 | 66 | fits | 65,361 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 4,317,312 | 43.173 | 62 | 66 | fits | 65,361 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 4,485,508 | 44.855 | 62 | 66 | fits | 65,321 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 4,512,714 | 45.127 | 62 | 66 | fits | 65,321 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 4,679,951 | 46.800 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 4,707,107 | 47.071 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 4,873,608 | 48.736 | 62 | 66 | fits | 63,651 | 200 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 4,899,452 | 48.995 | 62 | 66 | fits | 63,651 | 200 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 5,085,276 | 50.853 | 62 | 66 | fits | 62,581 | 200 | 0.121 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 5,114,437 | 51.144 | 62 | 66 | fits | 62,581 | 200 | 0.121 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 5,287,575 | 52.876 | 62 | 66 | fits | 37,917 | 103 | 0.181 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if1` | 758,644 | 7.586 | 20 | 200 | fits | 179,222 | 109 | 0.436 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 871,033 | 8.710 | 20 | 20 | fits | 132,657 | 38 | 0.779 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if1` | 371,542 | 3.715 | 20 | 24 | fits | 227,064 | 172 | 0.472 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 698,901 | 6.989 | 20 | 50 | fits | 179,222 | 109 | 0.436 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if1` | 1,269,900 | 12.699 | 20 | 20 | fits | 68,203 | 27 | 0.663 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 2,067,918 | 20.679 | 62 | 66 | fits | 41,493 | 101 | 0.349 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 2,435,630 | 24.356 | 62 | 66 | fits | 68,027 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 2,464,010 | 24.640 | 62 | 66 | fits | 68,027 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 2,638,682 | 26.387 | 62 | 66 | fits | 67,171 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 486,321 | 4.863 | 62 | 66 | fits | 66,281 | 203 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 515,916 | 5.159 | 62 | 66 | fits | 66,281 | 203 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 614,592 | 6.146 | 62 | 66 | fits | 91,568 | 210 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 644,243 | 6.442 | 62 | 66 | fits | 91,568 | 210 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 681,001 | 6.810 | 62 | 66 | fits | 65,212 | 203 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 710,198 | 7.102 | 62 | 66 | fits | 65,212 | 203 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 2,666,780 | 26.668 | 62 | 66 | fits | 67,171 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 2,841,367 | 28.414 | 62 | 66 | fits | 67,349 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 2,869,647 | 28.696 | 62 | 66 | fits | 67,349 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 3,043,728 | 30.437 | 62 | 66 | fits | 66,904 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 3,071,818 | 30.718 | 62 | 66 | fits | 66,904 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 3,245,693 | 32.457 | 62 | 66 | fits | 67,047 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 3,273,825 | 32.738 | 62 | 66 | fits | 67,047 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 3,431,296 | 34.313 | 62 | 66 | fits | 66,804 | 201 | 0.165 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 231,884 | 2.319 | 62 | 66 | fits | 71,635 | 203 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 262,896 | 2.629 | 62 | 66 | fits | 71,635 | 203 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 393,612 | 3.936 | 62 | 66 | fits | 118,337 | 210 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 425,128 | 4.251 | 62 | 66 | fits | 118,337 | 210 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 3,458,639 | 34.586 | 62 | 66 | fits | 66,804 | 201 | 0.165 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 3,630,174 | 36.302 | 62 | 66 | fits | 66,633 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 3,657,949 | 36.579 | 62 | 66 | fits | 66,633 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 3,828,729 | 38.287 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 3,855,872 | 38.559 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 4,025,234 | 40.252 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 4,052,315 | 40.523 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 4,246,203 | 42.462 | 62 | 66 | fits | 64,925 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 4,273,084 | 42.731 | 62 | 66 | fits | 64,925 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 4,425,672 | 44.257 | 62 | 66 | fits | 65,684 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 4,452,878 | 44.529 | 62 | 66 | fits | 65,684 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 4,644,967 | 46.450 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 4,672,123 | 46.721 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 4,838,614 | 48.386 | 62 | 66 | fits | 63,651 | 200 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 4,864,458 | 48.645 | 62 | 66 | fits | 63,651 | 200 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 5,025,371 | 50.254 | 62 | 66 | fits | 62,540 | 200 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 5,054,532 | 50.545 | 62 | 66 | fits | 62,540 | 200 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 5,243,388 | 52.434 | 62 | 66 | fits | 37,600 | 103 | 0.172 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if1` | 833,001 | 8.330 | 20 | 200 | fits | 155,401 | 83 | 0.508 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 959,340 | 9.593 | 20 | 20 | fits | 146,607 | 40 | 0.744 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if1` | 461,916 | 4.619 | 20 | 24 | fits | 224,552 | 167 | 0.468 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 773,258 | 7.733 | 20 | 50 | fits | 155,401 | 83 | 0.508 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if1` | 1,357,911 | 13.579 | 20 | 20 | fits | 67,980 | 27 | 0.663 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 1,972,393 | 19.724 | 62 | 66 | fits | 41,628 | 101 | 0.349 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 2,341,142 | 23.411 | 62 | 66 | fits | 68,049 | 201 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 357,456 | 3.575 | 62 | 66 | fits | 70,609 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 387,108 | 3.871 | 62 | 66 | fits | 70,609 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 485,427 | 4.854 | 62 | 66 | fits | 113,987 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 514,901 | 5.149 | 62 | 66 | fits | 113,987 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 574,589 | 5.746 | 62 | 66 | fits | 65,543 | 203 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 603,941 | 6.039 | 62 | 66 | fits | 65,543 | 203 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 2,369,550 | 23.695 | 62 | 66 | fits | 68,049 | 201 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 2,544,913 | 25.449 | 62 | 66 | fits | 67,360 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 2,573,008 | 25.730 | 62 | 66 | fits | 67,360 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 2,748,191 | 27.482 | 62 | 66 | fits | 67,390 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 2,776,439 | 27.764 | 62 | 66 | fits | 67,390 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 2,924,864 | 29.249 | 62 | 66 | fits | 66,977 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 2,952,954 | 29.530 | 62 | 66 | fits | 66,977 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 3,127,271 | 31.273 | 62 | 66 | fits | 67,041 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 3,155,403 | 31.554 | 62 | 66 | fits | 67,041 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 3,338,139 | 33.381 | 62 | 66 | fits | 67,347 | 201 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 237,554 | 2.376 | 62 | 66 | fits | 100,330 | 212 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 268,945 | 2.689 | 62 | 66 | fits | 100,330 | 212 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 3,365,873 | 33.659 | 62 | 66 | fits | 67,347 | 201 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 3,537,955 | 35.380 | 62 | 66 | fits | 66,487 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 3,565,515 | 35.655 | 62 | 66 | fits | 66,487 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 3,736,924 | 37.369 | 62 | 66 | fits | 66,585 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 3,764,699 | 37.647 | 62 | 66 | fits | 66,585 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 3,935,429 | 39.354 | 62 | 66 | fits | 65,568 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 3,962,572 | 39.626 | 62 | 66 | fits | 65,568 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 4,131,884 | 41.319 | 62 | 66 | fits | 65,277 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 4,158,965 | 41.590 | 62 | 66 | fits | 65,277 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 4,336,622 | 43.366 | 62 | 66 | fits | 65,352 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 4,363,494 | 43.635 | 62 | 66 | fits | 65,352 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 4,531,690 | 45.317 | 62 | 66 | fits | 65,321 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 4,558,896 | 45.589 | 62 | 66 | fits | 65,321 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 4,726,133 | 47.261 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 4,753,289 | 47.533 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 4,944,565 | 49.446 | 62 | 66 | fits | 63,606 | 200 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 4,970,364 | 49.704 | 62 | 66 | fits | 63,606 | 200 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 5,131,197 | 51.312 | 62 | 66 | fits | 62,581 | 200 | 0.121 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 5,160,358 | 51.604 | 62 | 66 | fits | 62,581 | 200 | 0.121 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 5,333,570 | 53.336 | 62 | 66 | fits | 37,917 | 103 | 0.181 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if1` | 726,619 | 7.266 | 20 | 200 | fits | 163,086 | 117 | 0.445 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 836,791 | 8.368 | 20 | 20 | fits | 130,440 | 44 | 0.742 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if1` | 523,061 | 5.231 | 20 | 24 | fits | 209,293 | 161 | 0.460 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 666,876 | 6.669 | 20 | 50 | fits | 163,086 | 117 | 0.445 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if1` | 1,264,082 | 12.641 | 20 | 20 | fits | 99,872 | 39 | 0.560 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 203,888 | 2.039 | 62 | 66 | fits | 68,846 | 203 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 232,903 | 2.329 | 62 | 66 | fits | 68,846 | 203 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 461,905 | 4.619 | 62 | 66 | fits | 65,087 | 203 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 491,043 | 4.910 | 62 | 66 | fits | 65,087 | 203 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 588,837 | 5.888 | 62 | 66 | fits | 90,448 | 210 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 618,094 | 6.181 | 62 | 66 | fits | 90,448 | 210 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 653,914 | 6.539 | 62 | 66 | fits | 64,012 | 203 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 682,890 | 6.829 | 62 | 66 | fits | 64,012 | 203 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 2,041,953 | 20.420 | 62 | 66 | fits | 41,763 | 101 | 0.347 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 2,409,919 | 24.099 | 62 | 66 | fits | 67,854 | 201 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 2,438,023 | 24.380 | 62 | 66 | fits | 67,854 | 201 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 2,613,073 | 26.131 | 62 | 66 | fits | 67,440 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 2,641,321 | 26.413 | 62 | 66 | fits | 67,440 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 2,815,876 | 28.159 | 62 | 66 | fits | 66,983 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 2,843,966 | 28.440 | 62 | 66 | fits | 66,983 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 3,018,315 | 30.183 | 62 | 66 | fits | 67,043 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 3,046,447 | 30.464 | 62 | 66 | fits | 67,043 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 3,219,821 | 32.198 | 62 | 66 | fits | 65,817 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 3,246,723 | 32.467 | 62 | 66 | fits | 65,817 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 3,429,270 | 34.293 | 62 | 66 | fits | 66,575 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 369,588 | 3.696 | 62 | 66 | fits | 118,256 | 210 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 401,104 | 4.011 | 62 | 66 | fits | 118,256 | 210 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 3,456,463 | 34.565 | 62 | 66 | fits | 66,575 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 3,627,982 | 36.280 | 62 | 66 | fits | 66,665 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 3,655,789 | 36.558 | 62 | 66 | fits | 66,665 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 3,826,569 | 38.266 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 3,853,712 | 38.537 | 62 | 66 | fits | 65,574 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 4,023,074 | 40.231 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 4,050,155 | 40.502 | 62 | 66 | fits | 65,283 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 4,218,885 | 42.189 | 62 | 66 | fits | 64,925 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 4,245,766 | 42.458 | 62 | 66 | fits | 64,925 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 4,423,530 | 44.235 | 62 | 66 | fits | 65,684 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 4,450,736 | 44.507 | 62 | 66 | fits | 65,684 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 4,617,915 | 46.179 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 4,645,071 | 46.451 | 62 | 66 | fits | 65,202 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 4,811,586 | 48.116 | 62 | 66 | fits | 63,536 | 200 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 4,837,315 | 48.373 | 62 | 66 | fits | 63,536 | 200 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 5,022,763 | 50.228 | 62 | 66 | fits | 62,540 | 200 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 5,051,924 | 50.519 | 62 | 66 | fits | 62,540 | 200 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 5,216,416 | 52.164 | 62 | 66 | fits | 37,600 | 103 | 0.172 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if1` | 827,704 | 8.277 | 20 | 200 | fits | 165,200 | 101 | 0.475 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 953,977 | 9.540 | 20 | 20 | fits | 146,541 | 40 | 0.744 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if1` | 454,677 | 4.547 | 20 | 24 | fits | 225,131 | 167 | 0.470 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 767,961 | 7.680 | 20 | 50 | fits | 165,200 | 101 | 0.475 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if1` | 1,351,712 | 13.517 | 20 | 20 | fits | 67,814 | 27 | 0.663 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
