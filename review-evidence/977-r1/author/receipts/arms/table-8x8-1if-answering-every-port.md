### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 728 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.acmp.if0` (notice-burst-0) | 9.632 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.adp.if0` (notice-burst-0) | 8.525 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-4.held.aecp.if0` (notice-every-4) | 6.676 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.maap.if0` (notice-every-5) | 8.086 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-1.held.srp.if0` (notice-every-1) | 12.587 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 0.875 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.36.0.if0` (notice-burst-6) | 29.716 (29.980) | fits | 1 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1442 | 0 | 162,679 (1.627) | fits |
| notice-every-1 | 1438 | 0 | 163,741 (1.637) | fits |
| notice-every-2 | 1439 | 0 | 163,726 (1.637) | fits |
| notice-every-3 | 1435 | 0 | 163,671 (1.637) | fits |
| notice-every-4 | 1440 | 0 | 162,778 (1.628) | fits |
| notice-every-5 | 1428 | 0 | 163,236 (1.632) | fits |
| notice-every-6 | 1425 | 0 | 166,135 (1.661) | fits |
| notice-every-7 | 1429 | 0 | 165,011 (1.650) | fits |
| notice-burst-0 | 1102 | 0 | 172,521 (1.725) | fits |
| notice-burst-1 | 1092 | 0 | 174,923 (1.749) | fits |
| notice-burst-2 | 1090 | 0 | 173,557 (1.736) | fits |
| notice-burst-3 | 1093 | 0 | 174,779 (1.748) | fits |
| notice-burst-4 | 1102 | 0 | 172,472 (1.725) | fits |
| notice-burst-5 | 1096 | 0 | 170,894 (1.709) | fits |
| notice-burst-6 | 1087 | 0 | 175,250 (1.752) | fits |
| notice-burst-7 | 1079 | 0 | 174,949 (1.749) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 7.636 | 130 | 16 | 2 | within |
| notice-every-0 | 7.824 | 130 | 16 | 2 | within |
| notice-every-0 | 1.623 | 130 | 16 | 2 | within |
| notice-every-0 | 1.814 | 130 | 16 | 2 | within |
| notice-every-0 | 5.795 | 130 | 16 | 2 | within |
| notice-every-0 | 5.983 | 130 | 16 | 2 | within |
| notice-every-0 | 3.693 | 130 | 16 | 2 | within |
| notice-every-0 | 3.885 | 130 | 16 | 2 | within |
| notice-every-0 | 1.981 | 130 | 16 | 2 | within |
| notice-every-0 | 2.160 | 130 | 16 | 2 | within |
| notice-every-0 | 4.047 | 130 | 16 | 2 | within |
| notice-every-0 | 4.227 | 130 | 16 | 2 | within |
| notice-every-0 | 6.143 | 130 | 16 | 2 | within |
| notice-every-0 | 6.318 | 130 | 16 | 2 | within |
| notice-every-0 | 7.982 | 130 | 16 | 2 | within |
| notice-every-0 | 8.155 | 130 | 16 | 2 | within |
| notice-every-0 | 9.643 | 130 | 16 | 2 | within |
| notice-every-0 | 9.829 | 130 | 16 | 2 | within |
| notice-every-0 | 9.979 | 130 | 16 | 2 | within |
| notice-every-0 | 10.152 | 130 | 16 | 2 | within |
| notice-every-0 | 11.608 | 130 | 16 | 2 | within |
| notice-every-0 | 11.797 | 130 | 16 | 2 | within |
| notice-every-0 | 11.944 | 130 | 16 | 2 | within |
| notice-every-0 | 12.118 | 130 | 16 | 2 | within |
| notice-every-0 | 13.741 | 130 | 16 | 2 | within |
| notice-every-0 | 13.928 | 130 | 16 | 2 | within |
| notice-every-0 | 14.076 | 130 | 16 | 2 | within |
| notice-every-0 | 14.248 | 130 | 16 | 2 | within |
| notice-every-0 | 15.710 | 130 | 16 | 2 | within |
| notice-every-0 | 15.896 | 130 | 16 | 2 | within |
| notice-every-0 | 16.045 | 130 | 16 | 2 | within |
| notice-every-0 | 16.218 | 130 | 16 | 2 | within |
| notice-every-0 | 17.638 | 130 | 16 | 2 | within |
| notice-every-0 | 17.824 | 130 | 16 | 2 | within |
| notice-every-0 | 17.971 | 130 | 16 | 2 | within |
| notice-every-0 | 18.144 | 130 | 16 | 2 | within |
| notice-every-0 | 23.166 | 130 | 16 | 2 | within |
| notice-every-0 | 23.303 | 130 | 16 | 2 | within |
| notice-every-0 | 23.480 | 130 | 16 | 2 | within |
| notice-every-0 | 23.663 | 130 | 16 | 2 | within |
| notice-every-1 | 7.633 | 130 | 16 | 2 | within |
| notice-every-1 | 7.821 | 130 | 16 | 2 | within |
| notice-every-1 | 1.624 | 130 | 16 | 2 | within |
| notice-every-1 | 1.815 | 130 | 16 | 2 | within |
| notice-every-1 | 5.600 | 130 | 16 | 2 | within |
| notice-every-1 | 5.788 | 130 | 16 | 2 | within |
| notice-every-1 | 3.497 | 130 | 16 | 2 | within |
| notice-every-1 | 3.689 | 130 | 16 | 2 | within |
| notice-every-1 | 1.981 | 130 | 16 | 2 | within |
| notice-every-1 | 2.161 | 130 | 16 | 2 | within |
| notice-every-1 | 3.851 | 130 | 16 | 2 | within |
| notice-every-1 | 4.031 | 130 | 16 | 2 | within |
| notice-every-1 | 5.947 | 130 | 16 | 2 | within |
| notice-every-1 | 6.122 | 130 | 16 | 2 | within |
| notice-every-1 | 7.978 | 130 | 16 | 2 | within |
| notice-every-1 | 8.152 | 130 | 16 | 2 | within |
| notice-every-1 | 9.638 | 130 | 16 | 2 | within |
| notice-every-1 | 9.824 | 130 | 16 | 2 | within |
| notice-every-1 | 9.974 | 130 | 16 | 2 | within |
| notice-every-1 | 10.147 | 130 | 16 | 2 | within |
| notice-every-1 | 11.603 | 130 | 16 | 2 | within |
| notice-every-1 | 11.792 | 130 | 16 | 2 | within |
| notice-every-1 | 11.940 | 130 | 16 | 2 | within |
| notice-every-1 | 12.113 | 130 | 16 | 2 | within |
| notice-every-1 | 13.551 | 130 | 16 | 2 | within |
| notice-every-1 | 13.738 | 130 | 16 | 2 | within |
| notice-every-1 | 13.885 | 130 | 16 | 2 | within |
| notice-every-1 | 14.058 | 130 | 16 | 2 | within |
| notice-every-1 | 15.519 | 130 | 16 | 2 | within |
| notice-every-1 | 15.706 | 130 | 16 | 2 | within |
| notice-every-1 | 15.855 | 130 | 16 | 2 | within |
| notice-every-1 | 16.028 | 130 | 16 | 2 | within |
| notice-every-1 | 17.630 | 130 | 16 | 2 | within |
| notice-every-1 | 17.816 | 130 | 16 | 2 | within |
| notice-every-1 | 17.964 | 130 | 16 | 2 | within |
| notice-every-1 | 18.136 | 130 | 16 | 2 | within |
| notice-every-1 | 23.158 | 130 | 16 | 2 | within |
| notice-every-1 | 23.295 | 130 | 16 | 2 | within |
| notice-every-1 | 23.472 | 130 | 16 | 2 | within |
| notice-every-1 | 23.655 | 130 | 16 | 2 | within |
| notice-every-2 | 7.629 | 130 | 16 | 2 | within |
| notice-every-2 | 7.816 | 130 | 16 | 2 | within |
| notice-every-2 | 1.624 | 130 | 16 | 2 | within |
| notice-every-2 | 1.816 | 130 | 16 | 2 | within |
| notice-every-2 | 3.495 | 130 | 16 | 2 | within |
| notice-every-2 | 3.684 | 130 | 16 | 2 | within |
| notice-every-2 | 5.595 | 130 | 16 | 2 | within |
| notice-every-2 | 5.784 | 130 | 16 | 2 | within |
| notice-every-2 | 1.982 | 130 | 16 | 2 | within |
| notice-every-2 | 2.162 | 130 | 16 | 2 | within |
| notice-every-2 | 3.847 | 130 | 16 | 2 | within |
| notice-every-2 | 4.027 | 130 | 16 | 2 | within |
| notice-every-2 | 5.943 | 130 | 16 | 2 | within |
| notice-every-2 | 6.118 | 130 | 16 | 2 | within |
| notice-every-2 | 7.974 | 130 | 16 | 2 | within |
| notice-every-2 | 8.147 | 130 | 16 | 2 | within |
| notice-every-2 | 9.634 | 130 | 16 | 2 | within |
| notice-every-2 | 9.820 | 130 | 16 | 2 | within |
| notice-every-2 | 9.969 | 130 | 16 | 2 | within |
| notice-every-2 | 10.143 | 130 | 16 | 2 | within |
| notice-every-2 | 11.599 | 130 | 16 | 2 | within |
| notice-every-2 | 11.787 | 130 | 16 | 2 | within |
| notice-every-2 | 11.935 | 130 | 16 | 2 | within |
| notice-every-2 | 12.109 | 130 | 16 | 2 | within |
| notice-every-2 | 13.547 | 130 | 16 | 2 | within |
| notice-every-2 | 13.733 | 130 | 16 | 2 | within |
| notice-every-2 | 13.881 | 130 | 16 | 2 | within |
| notice-every-2 | 14.054 | 130 | 16 | 2 | within |
| notice-every-2 | 15.515 | 130 | 16 | 2 | within |
| notice-every-2 | 15.702 | 130 | 16 | 2 | within |
| notice-every-2 | 15.850 | 130 | 16 | 2 | within |
| notice-every-2 | 16.024 | 130 | 16 | 2 | within |
| notice-every-2 | 17.626 | 130 | 16 | 2 | within |
| notice-every-2 | 17.811 | 130 | 16 | 2 | within |
| notice-every-2 | 17.959 | 130 | 16 | 2 | within |
| notice-every-2 | 18.132 | 130 | 16 | 2 | within |
| notice-every-2 | 23.154 | 130 | 16 | 2 | within |
| notice-every-2 | 23.291 | 130 | 16 | 2 | within |
| notice-every-2 | 23.468 | 130 | 16 | 2 | within |
| notice-every-2 | 23.650 | 130 | 16 | 2 | within |
| notice-every-3 | 7.629 | 130 | 16 | 2 | within |
| notice-every-3 | 7.817 | 130 | 16 | 2 | within |
| notice-every-3 | 1.624 | 130 | 16 | 2 | within |
| notice-every-3 | 1.815 | 130 | 16 | 2 | within |
| notice-every-3 | 3.495 | 130 | 16 | 2 | within |
| notice-every-3 | 3.684 | 130 | 16 | 2 | within |
| notice-every-3 | 5.596 | 130 | 16 | 2 | within |
| notice-every-3 | 5.784 | 130 | 16 | 2 | within |
| notice-every-3 | 1.981 | 130 | 16 | 2 | within |
| notice-every-3 | 2.161 | 130 | 16 | 2 | within |
| notice-every-3 | 3.846 | 130 | 16 | 2 | within |
| notice-every-3 | 4.027 | 130 | 16 | 2 | within |
| notice-every-3 | 5.943 | 130 | 16 | 2 | within |
| notice-every-3 | 6.118 | 130 | 16 | 2 | within |
| notice-every-3 | 7.974 | 130 | 16 | 2 | within |
| notice-every-3 | 8.148 | 130 | 16 | 2 | within |
| notice-every-3 | 9.634 | 130 | 16 | 2 | within |
| notice-every-3 | 9.820 | 130 | 16 | 2 | within |
| notice-every-3 | 9.970 | 130 | 16 | 2 | within |
| notice-every-3 | 10.143 | 130 | 16 | 2 | within |
| notice-every-3 | 11.599 | 130 | 16 | 2 | within |
| notice-every-3 | 11.788 | 130 | 16 | 2 | within |
| notice-every-3 | 11.935 | 130 | 16 | 2 | within |
| notice-every-3 | 12.109 | 130 | 16 | 2 | within |
| notice-every-3 | 13.547 | 130 | 16 | 2 | within |
| notice-every-3 | 13.733 | 130 | 16 | 2 | within |
| notice-every-3 | 13.881 | 130 | 16 | 2 | within |
| notice-every-3 | 14.054 | 130 | 16 | 2 | within |
| notice-every-3 | 15.515 | 130 | 16 | 2 | within |
| notice-every-3 | 15.702 | 130 | 16 | 2 | within |
| notice-every-3 | 15.851 | 130 | 16 | 2 | within |
| notice-every-3 | 16.024 | 130 | 16 | 2 | within |
| notice-every-3 | 17.626 | 130 | 16 | 2 | within |
| notice-every-3 | 17.812 | 130 | 16 | 2 | within |
| notice-every-3 | 17.959 | 130 | 16 | 2 | within |
| notice-every-3 | 18.132 | 130 | 16 | 2 | within |
| notice-every-3 | 23.154 | 130 | 16 | 2 | within |
| notice-every-3 | 23.291 | 130 | 16 | 2 | within |
| notice-every-3 | 23.468 | 130 | 16 | 2 | within |
| notice-every-3 | 23.650 | 130 | 16 | 2 | within |
| notice-every-4 | 7.667 | 130 | 16 | 2 | within |
| notice-every-4 | 7.855 | 130 | 16 | 2 | within |
| notice-every-4 | 1.624 | 130 | 16 | 2 | within |
| notice-every-4 | 1.815 | 130 | 16 | 2 | within |
| notice-every-4 | 5.638 | 130 | 16 | 2 | within |
| notice-every-4 | 5.825 | 130 | 16 | 2 | within |
| notice-every-4 | 3.739 | 130 | 16 | 2 | within |
| notice-every-4 | 3.930 | 130 | 16 | 2 | within |
| notice-every-4 | 1.981 | 130 | 16 | 2 | within |
| notice-every-4 | 2.161 | 130 | 16 | 2 | within |
| notice-every-4 | 4.092 | 130 | 16 | 2 | within |
| notice-every-4 | 4.273 | 130 | 16 | 2 | within |
| notice-every-4 | 5.983 | 130 | 16 | 2 | within |
| notice-every-4 | 6.157 | 130 | 16 | 2 | within |
| notice-every-4 | 8.013 | 130 | 16 | 2 | within |
| notice-every-4 | 8.186 | 130 | 16 | 2 | within |
| notice-every-4 | 9.672 | 130 | 16 | 2 | within |
| notice-every-4 | 9.859 | 130 | 16 | 2 | within |
| notice-every-4 | 10.008 | 130 | 16 | 2 | within |
| notice-every-4 | 10.182 | 130 | 16 | 2 | within |
| notice-every-4 | 11.637 | 130 | 16 | 2 | within |
| notice-every-4 | 11.825 | 130 | 16 | 2 | within |
| notice-every-4 | 11.973 | 130 | 16 | 2 | within |
| notice-every-4 | 12.147 | 130 | 16 | 2 | within |
| notice-every-4 | 13.584 | 130 | 16 | 2 | within |
| notice-every-4 | 13.771 | 130 | 16 | 2 | within |
| notice-every-4 | 13.919 | 130 | 16 | 2 | within |
| notice-every-4 | 14.092 | 130 | 16 | 2 | within |
| notice-every-4 | 15.553 | 130 | 16 | 2 | within |
| notice-every-4 | 15.740 | 130 | 16 | 2 | within |
| notice-every-4 | 15.888 | 130 | 16 | 2 | within |
| notice-every-4 | 16.062 | 130 | 16 | 2 | within |
| notice-every-4 | 17.663 | 130 | 16 | 2 | within |
| notice-every-4 | 17.849 | 130 | 16 | 2 | within |
| notice-every-4 | 17.997 | 130 | 16 | 2 | within |
| notice-every-4 | 18.170 | 130 | 16 | 2 | within |
| notice-every-4 | 23.192 | 130 | 16 | 2 | within |
| notice-every-4 | 23.329 | 130 | 16 | 2 | within |
| notice-every-4 | 23.506 | 130 | 16 | 2 | within |
| notice-every-4 | 23.688 | 130 | 16 | 2 | within |
| notice-every-5 | 1.573 | 130 | 16 | 2 | within |
| notice-every-5 | 1.763 | 130 | 16 | 2 | within |
| notice-every-5 | 7.569 | 130 | 16 | 2 | within |
| notice-every-5 | 7.756 | 130 | 16 | 2 | within |
| notice-every-5 | 3.638 | 130 | 16 | 2 | within |
| notice-every-5 | 3.827 | 130 | 16 | 2 | within |
| notice-every-5 | 5.542 | 130 | 16 | 2 | within |
| notice-every-5 | 5.730 | 130 | 16 | 2 | within |
| notice-every-5 | 1.930 | 130 | 16 | 2 | within |
| notice-every-5 | 2.109 | 130 | 16 | 2 | within |
| notice-every-5 | 3.990 | 130 | 16 | 2 | within |
| notice-every-5 | 4.170 | 130 | 16 | 2 | within |
| notice-every-5 | 5.887 | 130 | 16 | 2 | within |
| notice-every-5 | 6.062 | 130 | 16 | 2 | within |
| notice-every-5 | 7.913 | 130 | 16 | 2 | within |
| notice-every-5 | 8.086 | 130 | 16 | 2 | within |
| notice-every-5 | 9.573 | 130 | 16 | 2 | within |
| notice-every-5 | 9.760 | 130 | 16 | 2 | within |
| notice-every-5 | 9.909 | 130 | 16 | 2 | within |
| notice-every-5 | 10.083 | 130 | 16 | 2 | within |
| notice-every-5 | 11.538 | 130 | 16 | 2 | within |
| notice-every-5 | 11.727 | 130 | 16 | 2 | within |
| notice-every-5 | 11.874 | 130 | 16 | 2 | within |
| notice-every-5 | 12.048 | 130 | 16 | 2 | within |
| notice-every-5 | 13.485 | 130 | 16 | 2 | within |
| notice-every-5 | 13.672 | 130 | 16 | 2 | within |
| notice-every-5 | 13.820 | 130 | 16 | 2 | within |
| notice-every-5 | 13.993 | 130 | 16 | 2 | within |
| notice-every-5 | 15.638 | 130 | 16 | 2 | within |
| notice-every-5 | 15.825 | 130 | 16 | 2 | within |
| notice-every-5 | 15.973 | 130 | 16 | 2 | within |
| notice-every-5 | 16.147 | 130 | 16 | 2 | within |
| notice-every-5 | 17.566 | 130 | 16 | 2 | within |
| notice-every-5 | 17.752 | 130 | 16 | 2 | within |
| notice-every-5 | 17.900 | 130 | 16 | 2 | within |
| notice-every-5 | 18.072 | 130 | 16 | 2 | within |
| notice-every-5 | 23.092 | 130 | 16 | 2 | within |
| notice-every-5 | 23.230 | 130 | 16 | 2 | within |
| notice-every-5 | 23.407 | 130 | 16 | 2 | within |
| notice-every-5 | 23.589 | 130 | 16 | 2 | within |
| notice-every-6 | 5.539 | 130 | 16 | 2 | within |
| notice-every-6 | 5.725 | 130 | 16 | 2 | within |
| notice-every-6 | 3.637 | 130 | 16 | 2 | within |
| notice-every-6 | 3.826 | 130 | 16 | 2 | within |
| notice-every-6 | 1.572 | 130 | 16 | 2 | within |
| notice-every-6 | 1.764 | 130 | 16 | 2 | within |
| notice-every-6 | 7.567 | 130 | 16 | 2 | within |
| notice-every-6 | 7.754 | 130 | 16 | 2 | within |
| notice-every-6 | 1.929 | 130 | 16 | 2 | within |
| notice-every-6 | 2.109 | 130 | 16 | 2 | within |
| notice-every-6 | 3.988 | 130 | 16 | 2 | within |
| notice-every-6 | 4.169 | 130 | 16 | 2 | within |
| notice-every-6 | 5.883 | 130 | 16 | 2 | within |
| notice-every-6 | 6.058 | 130 | 16 | 2 | within |
| notice-every-6 | 7.911 | 130 | 16 | 2 | within |
| notice-every-6 | 8.084 | 130 | 16 | 2 | within |
| notice-every-6 | 9.570 | 130 | 16 | 2 | within |
| notice-every-6 | 9.757 | 130 | 16 | 2 | within |
| notice-every-6 | 9.906 | 130 | 16 | 2 | within |
| notice-every-6 | 10.080 | 130 | 16 | 2 | within |
| notice-every-6 | 11.535 | 130 | 16 | 2 | within |
| notice-every-6 | 11.724 | 130 | 16 | 2 | within |
| notice-every-6 | 11.871 | 130 | 16 | 2 | within |
| notice-every-6 | 12.045 | 130 | 16 | 2 | within |
| notice-every-6 | 13.483 | 130 | 16 | 2 | within |
| notice-every-6 | 13.669 | 130 | 16 | 2 | within |
| notice-every-6 | 13.817 | 130 | 16 | 2 | within |
| notice-every-6 | 13.990 | 130 | 16 | 2 | within |
| notice-every-6 | 15.635 | 130 | 16 | 2 | within |
| notice-every-6 | 15.822 | 130 | 16 | 2 | within |
| notice-every-6 | 15.970 | 130 | 16 | 2 | within |
| notice-every-6 | 16.144 | 130 | 16 | 2 | within |
| notice-every-6 | 17.563 | 130 | 16 | 2 | within |
| notice-every-6 | 17.749 | 130 | 16 | 2 | within |
| notice-every-6 | 17.897 | 130 | 16 | 2 | within |
| notice-every-6 | 18.070 | 130 | 16 | 2 | within |
| notice-every-6 | 23.091 | 130 | 16 | 2 | within |
| notice-every-6 | 23.228 | 130 | 16 | 2 | within |
| notice-every-6 | 23.405 | 130 | 16 | 2 | within |
| notice-every-6 | 23.588 | 130 | 16 | 2 | within |
| notice-every-7 | 7.661 | 130 | 16 | 2 | within |
| notice-every-7 | 7.849 | 130 | 16 | 2 | within |
| notice-every-7 | 1.624 | 130 | 16 | 2 | within |
| notice-every-7 | 1.815 | 130 | 16 | 2 | within |
| notice-every-7 | 3.736 | 130 | 16 | 2 | within |
| notice-every-7 | 3.925 | 130 | 16 | 2 | within |
| notice-every-7 | 5.632 | 130 | 16 | 2 | within |
| notice-every-7 | 5.820 | 130 | 16 | 2 | within |
| notice-every-7 | 1.981 | 130 | 16 | 2 | within |
| notice-every-7 | 2.161 | 130 | 16 | 2 | within |
| notice-every-7 | 4.087 | 130 | 16 | 2 | within |
| notice-every-7 | 4.268 | 130 | 16 | 2 | within |
| notice-every-7 | 5.977 | 130 | 16 | 2 | within |
| notice-every-7 | 6.152 | 130 | 16 | 2 | within |
| notice-every-7 | 8.006 | 130 | 16 | 2 | within |
| notice-every-7 | 8.180 | 130 | 16 | 2 | within |
| notice-every-7 | 9.666 | 130 | 16 | 2 | within |
| notice-every-7 | 9.853 | 130 | 16 | 2 | within |
| notice-every-7 | 10.002 | 130 | 16 | 2 | within |
| notice-every-7 | 10.175 | 130 | 16 | 2 | within |
| notice-every-7 | 11.631 | 130 | 16 | 2 | within |
| notice-every-7 | 11.819 | 130 | 16 | 2 | within |
| notice-every-7 | 11.967 | 130 | 16 | 2 | within |
| notice-every-7 | 12.140 | 130 | 16 | 2 | within |
| notice-every-7 | 13.578 | 130 | 16 | 2 | within |
| notice-every-7 | 13.765 | 130 | 16 | 2 | within |
| notice-every-7 | 13.913 | 130 | 16 | 2 | within |
| notice-every-7 | 14.085 | 130 | 16 | 2 | within |
| notice-every-7 | 15.547 | 130 | 16 | 2 | within |
| notice-every-7 | 15.734 | 130 | 16 | 2 | within |
| notice-every-7 | 15.882 | 130 | 16 | 2 | within |
| notice-every-7 | 16.055 | 130 | 16 | 2 | within |
| notice-every-7 | 17.657 | 130 | 16 | 2 | within |
| notice-every-7 | 17.843 | 130 | 16 | 2 | within |
| notice-every-7 | 17.991 | 130 | 16 | 2 | within |
| notice-every-7 | 18.164 | 130 | 16 | 2 | within |
| notice-every-7 | 23.183 | 130 | 16 | 2 | within |
| notice-every-7 | 23.320 | 130 | 16 | 2 | within |
| notice-every-7 | 23.497 | 130 | 16 | 2 | within |
| notice-every-7 | 23.680 | 130 | 16 | 2 | within |
| notice-burst-0 | 4.734 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.911 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.461 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.649 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.597 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.786 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.020 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.205 | 130 | 16 | 1 | within |
| notice-burst-0 | 7.541 | 130 | 16 | 1 | within |
| notice-burst-0 | 7.719 | 130 | 16 | 1 | within |
| notice-burst-0 | 7.878 | 130 | 16 | 1 | within |
| notice-burst-0 | 8.056 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.806 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.979 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.273 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.457 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.963 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.155 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.935 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.135 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.301 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.492 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.072 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.259 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.366 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.551 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.605 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.778 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.215 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.399 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.547 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.720 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.140 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.324 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.470 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.643 | 130 | 16 | 1 | within |
| notice-burst-0 | 27.123 | 130 | 16 | 1 | within |
| notice-burst-0 | 27.257 | 130 | 16 | 1 | within |
| notice-burst-0 | 27.435 | 130 | 16 | 1 | within |
| notice-burst-0 | 27.616 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.209 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.386 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.133 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.322 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.480 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.652 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.369 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.559 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.673 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.866 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.548 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.729 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.258 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.460 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.631 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.819 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.206 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.392 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.541 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.717 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.725 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.914 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.029 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.217 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.161 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.347 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.494 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.666 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.282 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.468 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.616 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.789 | 130 | 16 | 1 | within |
| notice-burst-1 | 25.209 | 130 | 16 | 1 | within |
| notice-burst-1 | 25.394 | 130 | 16 | 1 | within |
| notice-burst-1 | 25.541 | 130 | 16 | 1 | within |
| notice-burst-1 | 25.714 | 130 | 16 | 1 | within |
| notice-burst-1 | 27.192 | 130 | 16 | 1 | within |
| notice-burst-1 | 27.329 | 130 | 16 | 1 | within |
| notice-burst-1 | 27.506 | 130 | 16 | 1 | within |
| notice-burst-1 | 27.688 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.148 | 130 | 16 | 2 | within |
| notice-burst-2 | 18.339 | 130 | 16 | 2 | within |
| notice-burst-2 | 2.276 | 130 | 16 | 2 | within |
| notice-burst-2 | 2.466 | 130 | 16 | 2 | within |
| notice-burst-2 | 4.684 | 130 | 16 | 2 | within |
| notice-burst-2 | 4.871 | 130 | 16 | 2 | within |
| notice-burst-2 | 18.497 | 130 | 16 | 2 | within |
| notice-burst-2 | 18.671 | 130 | 16 | 2 | within |
| notice-burst-2 | 19.223 | 130 | 16 | 2 | within |
| notice-burst-2 | 19.407 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.376 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.572 | 130 | 16 | 2 | within |
| notice-burst-2 | 6.214 | 130 | 16 | 2 | within |
| notice-burst-2 | 6.398 | 130 | 16 | 2 | within |
| notice-burst-2 | 6.559 | 130 | 16 | 2 | within |
| notice-burst-2 | 6.739 | 130 | 16 | 2 | within |
| notice-burst-2 | 19.567 | 130 | 16 | 2 | within |
| notice-burst-2 | 19.741 | 130 | 16 | 2 | within |
| notice-burst-2 | 2.635 | 130 | 16 | 2 | within |
| notice-burst-2 | 2.827 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.738 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.929 | 130 | 16 | 2 | within |
| notice-burst-2 | 5.033 | 130 | 16 | 2 | within |
| notice-burst-2 | 5.220 | 130 | 16 | 2 | within |
| notice-burst-2 | 21.187 | 130 | 16 | 2 | within |
| notice-burst-2 | 21.374 | 130 | 16 | 2 | within |
| notice-burst-2 | 21.521 | 130 | 16 | 2 | within |
| notice-burst-2 | 21.694 | 130 | 16 | 2 | within |
| notice-burst-2 | 23.310 | 130 | 16 | 2 | within |
| notice-burst-2 | 23.495 | 130 | 16 | 2 | within |
| notice-burst-2 | 23.643 | 130 | 16 | 2 | within |
| notice-burst-2 | 23.816 | 130 | 16 | 2 | within |
| notice-burst-2 | 25.235 | 130 | 16 | 2 | within |
| notice-burst-2 | 25.421 | 130 | 16 | 2 | within |
| notice-burst-2 | 25.568 | 130 | 16 | 2 | within |
| notice-burst-2 | 25.741 | 130 | 16 | 2 | within |
| notice-burst-2 | 27.221 | 130 | 16 | 2 | within |
| notice-burst-2 | 27.357 | 130 | 16 | 2 | within |
| notice-burst-2 | 27.535 | 130 | 16 | 2 | within |
| notice-burst-2 | 27.716 | 130 | 16 | 2 | within |
| notice-burst-3 | 17.376 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.566 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.573 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.751 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.415 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.594 | 130 | 16 | 1 | within |
| notice-burst-3 | 1.772 | 130 | 16 | 1 | within |
| notice-burst-3 | 1.968 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.753 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.928 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.881 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.075 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.723 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.897 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.200 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.386 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.546 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.720 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.137 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.329 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.917 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.107 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.237 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.424 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.168 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.355 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.502 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.675 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.291 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.476 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.624 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.796 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.216 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.402 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.549 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.722 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.209 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.345 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.523 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.704 | 130 | 16 | 1 | within |
| notice-burst-4 | 18.700 | 130 | 16 | 1 | within |
| notice-burst-4 | 18.890 | 130 | 16 | 1 | within |
| notice-burst-4 | 5.214 | 130 | 16 | 1 | within |
| notice-burst-4 | 5.402 | 130 | 16 | 1 | within |
| notice-burst-4 | 6.735 | 130 | 16 | 1 | within |
| notice-burst-4 | 6.914 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.113 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.308 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.473 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.654 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.907 | 130 | 16 | 1 | within |
| notice-burst-4 | 4.092 | 130 | 16 | 1 | within |
| notice-burst-4 | 5.563 | 130 | 16 | 1 | within |
| notice-burst-4 | 5.742 | 130 | 16 | 1 | within |
| notice-burst-4 | 7.071 | 130 | 16 | 1 | within |
| notice-burst-4 | 7.246 | 130 | 16 | 1 | within |
| notice-burst-4 | 19.051 | 130 | 16 | 1 | within |
| notice-burst-4 | 19.225 | 130 | 16 | 1 | within |
| notice-burst-4 | 20.148 | 130 | 16 | 1 | within |
| notice-burst-4 | 20.336 | 130 | 16 | 1 | within |
| notice-burst-4 | 4.258 | 130 | 16 | 1 | within |
| notice-burst-4 | 4.448 | 130 | 16 | 1 | within |
| notice-burst-4 | 20.484 | 130 | 16 | 1 | within |
| notice-burst-4 | 20.657 | 130 | 16 | 1 | within |
| notice-burst-4 | 22.281 | 130 | 16 | 1 | within |
| notice-burst-4 | 22.467 | 130 | 16 | 1 | within |
| notice-burst-4 | 22.613 | 130 | 16 | 1 | within |
| notice-burst-4 | 22.786 | 130 | 16 | 1 | within |
| notice-burst-4 | 24.218 | 130 | 16 | 1 | within |
| notice-burst-4 | 24.404 | 130 | 16 | 1 | within |
| notice-burst-4 | 24.552 | 130 | 16 | 1 | within |
| notice-burst-4 | 24.725 | 130 | 16 | 1 | within |
| notice-burst-4 | 26.145 | 130 | 16 | 1 | within |
| notice-burst-4 | 26.330 | 130 | 16 | 1 | within |
| notice-burst-4 | 26.477 | 130 | 16 | 1 | within |
| notice-burst-4 | 26.649 | 130 | 16 | 1 | within |
| notice-burst-4 | 28.136 | 130 | 16 | 1 | within |
| notice-burst-4 | 28.272 | 130 | 16 | 1 | within |
| notice-burst-4 | 28.450 | 130 | 16 | 1 | within |
| notice-burst-4 | 28.631 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.592 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.780 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.716 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.892 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.737 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.925 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.081 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.255 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.189 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.373 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.530 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.706 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.929 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.124 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.171 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.356 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.517 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.691 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.289 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.478 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.951 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.146 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.054 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.241 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.139 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.323 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.470 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.643 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.259 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.443 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.591 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.764 | 130 | 16 | 1 | within |
| notice-burst-5 | 26.269 | 130 | 16 | 1 | within |
| notice-burst-5 | 26.453 | 130 | 16 | 1 | within |
| notice-burst-5 | 26.599 | 130 | 16 | 1 | within |
| notice-burst-5 | 26.772 | 130 | 16 | 1 | within |
| notice-burst-5 | 28.175 | 130 | 16 | 1 | within |
| notice-burst-5 | 28.308 | 130 | 16 | 1 | within |
| notice-burst-5 | 28.487 | 130 | 16 | 1 | within |
| notice-burst-5 | 28.668 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.595 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.782 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.444 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.632 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.790 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.963 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.945 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.123 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.896 | 130 | 16 | 1 | within |
| notice-burst-6 | 4.084 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.440 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.624 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.783 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.960 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.272 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.456 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.616 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.790 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.250 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.437 | 130 | 16 | 1 | within |
| notice-burst-6 | 4.250 | 130 | 16 | 1 | within |
| notice-burst-6 | 4.441 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.584 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.758 | 130 | 16 | 1 | within |
| notice-burst-6 | 23.196 | 130 | 16 | 1 | within |
| notice-burst-6 | 23.381 | 130 | 16 | 1 | within |
| notice-burst-6 | 23.527 | 130 | 16 | 1 | within |
| notice-burst-6 | 23.700 | 130 | 16 | 1 | within |
| notice-burst-6 | 25.132 | 130 | 16 | 1 | within |
| notice-burst-6 | 25.317 | 130 | 16 | 1 | within |
| notice-burst-6 | 25.464 | 130 | 16 | 1 | within |
| notice-burst-6 | 25.638 | 130 | 16 | 1 | within |
| notice-burst-6 | 27.149 | 130 | 16 | 1 | within |
| notice-burst-6 | 27.333 | 130 | 16 | 1 | within |
| notice-burst-6 | 27.480 | 130 | 16 | 1 | within |
| notice-burst-6 | 27.653 | 130 | 16 | 1 | within |
| notice-burst-6 | 29.223 | 130 | 16 | 1 | within |
| notice-burst-6 | 29.356 | 130 | 16 | 1 | within |
| notice-burst-6 | 29.535 | 130 | 16 | 1 | within |
| notice-burst-6 | 29.716 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.641 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.826 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.539 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.727 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.884 | 130 | 16 | 1 | within |
| notice-burst-7 | 18.057 | 130 | 16 | 1 | within |
| notice-burst-7 | 19.178 | 130 | 16 | 1 | within |
| notice-burst-7 | 19.363 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.975 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.166 | 130 | 16 | 1 | within |
| notice-burst-7 | 5.515 | 130 | 16 | 1 | within |
| notice-burst-7 | 5.701 | 130 | 16 | 1 | within |
| notice-burst-7 | 19.518 | 130 | 16 | 1 | within |
| notice-burst-7 | 19.692 | 130 | 16 | 1 | within |
| notice-burst-7 | 21.342 | 130 | 16 | 1 | within |
| notice-burst-7 | 21.526 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.003 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.195 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.328 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.516 | 130 | 16 | 1 | within |
| notice-burst-7 | 5.862 | 130 | 16 | 1 | within |
| notice-burst-7 | 6.047 | 130 | 16 | 1 | within |
| notice-burst-7 | 21.674 | 130 | 16 | 1 | within |
| notice-burst-7 | 21.847 | 130 | 16 | 1 | within |
| notice-burst-7 | 23.291 | 130 | 16 | 1 | within |
| notice-burst-7 | 23.477 | 130 | 16 | 1 | within |
| notice-burst-7 | 23.623 | 130 | 16 | 1 | within |
| notice-burst-7 | 23.797 | 130 | 16 | 1 | within |
| notice-burst-7 | 25.229 | 130 | 16 | 1 | within |
| notice-burst-7 | 25.413 | 130 | 16 | 1 | within |
| notice-burst-7 | 25.560 | 130 | 16 | 1 | within |
| notice-burst-7 | 25.733 | 130 | 16 | 1 | within |
| notice-burst-7 | 27.246 | 130 | 16 | 1 | within |
| notice-burst-7 | 27.431 | 130 | 16 | 1 | within |
| notice-burst-7 | 27.578 | 130 | 16 | 1 | within |
| notice-burst-7 | 27.751 | 130 | 16 | 1 | within |
| notice-burst-7 | 29.141 | 130 | 16 | 1 | within |
| notice-burst-7 | 29.275 | 130 | 16 | 1 | within |
| notice-burst-7 | 29.453 | 130 | 16 | 1 | within |
| notice-burst-7 | 29.634 | 130 | 16 | 1 | within |

Latest: 29.716 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 667 | 124,795 (1.248) | 78,642 (0.786) |
| notice-every-1 | 667 | 124,821 (1.248) | 78,642 (0.786) |
| notice-every-2 | 667 | 124,933 (1.249) | 78,642 (0.786) |
| notice-every-3 | 667 | 124,907 (1.249) | 78,642 (0.786) |
| notice-every-4 | 667 | 124,933 (1.249) | 78,642 (0.786) |
| notice-every-5 | 667 | 118,238 (1.182) | 78,642 (0.786) |
| notice-every-6 | 666 | 125,122 (1.251) | 78,642 (0.786) |
| notice-every-7 | 666 | 125,199 (1.252) | 78,642 (0.786) |
| notice-burst-0 | 778 | 172,521 (1.725) | 78,642 (0.786) |
| notice-burst-1 | 778 | 174,923 (1.749) | 78,642 (0.786) |
| notice-burst-2 | 779 | 173,557 (1.736) | 78,642 (0.786) |
| notice-burst-3 | 779 | 174,779 (1.748) | 78,642 (0.786) |
| notice-burst-4 | 779 | 172,472 (1.725) | 78,642 (0.786) |
| notice-burst-5 | 780 | 132,694 (1.327) | 78,642 (0.786) |
| notice-burst-6 | 781 | 175,250 (1.752) | 78,642 (0.786) |
| notice-burst-7 | 782 | 174,949 (1.749) | 78,642 (0.786) |

Longest pass that carries a step: 175,250 CPU cycles (1.752 ms), notice-burst-6; longest step: 78,642 (0.786 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 763,645 | 7.636 | 130 | 134 | fits | 77,451 | 205 | 0.192 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 782,420 | 7.824 | 130 | 134 | fits | 77,451 | 205 | 0.192 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 162,264 | 1.623 | 130 | 134 | fits | 80,595 | 205 | 0.203 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 181,421 | 1.814 | 130 | 134 | fits | 80,595 | 205 | 0.203 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 579,460 | 5.795 | 130 | 134 | fits | 80,840 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 598,346 | 5.983 | 130 | 134 | fits | 80,840 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 369,312 | 3.693 | 130 | 134 | fits | 80,048 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 388,460 | 3.885 | 130 | 134 | fits | 80,048 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 198,051 | 1.981 | 130 | 134 | fits | 80,595 | 205 | 0.203 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 216,013 | 2.160 | 130 | 134 | fits | 80,595 | 205 | 0.203 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 404,681 | 4.047 | 130 | 134 | fits | 80,048 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 422,716 | 4.227 | 130 | 134 | fits | 80,048 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 614,310 | 6.143 | 130 | 134 | fits | 80,840 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 631,810 | 6.318 | 130 | 134 | fits | 80,840 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 798,179 | 7.982 | 130 | 134 | fits | 77,451 | 205 | 0.192 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 815,518 | 8.155 | 130 | 134 | fits | 77,451 | 205 | 0.192 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 964,271 | 9.643 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 982,945 | 9.829 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 997,864 | 9.979 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,015,212 | 10.152 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,160,819 | 11.608 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,179,663 | 11.797 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,194,447 | 11.944 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,211,786 | 12.118 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,374,106 | 13.741 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,392,780 | 13.928 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,407,564 | 14.076 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,424,833 | 14.248 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,570,963 | 15.710 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,589,649 | 15.896 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,604,498 | 16.045 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,621,837 | 16.218 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,763,762 | 17.638 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,782,357 | 17.824 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,797,141 | 17.971 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,814,410 | 18.144 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,316,623 | 23.166 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,330,345 | 23.303 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,348,046 | 23.480 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,366,254 | 23.663 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 171,702 | 1.717 | 20 | 200 | fits | 152,042 | 229 | 0.388 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 801,654 | 8.017 | 20 | 20 | fits | 136,430 | 135 | 0.600 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 645,020 | 6.450 | 20 | 24 | fits | 153,018 | 116 | 0.486 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 625,749 | 6.257 | 20 | 50 | fits | 153,018 | 116 | 0.486 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,162,828 | 11.628 | 20 | 20 | fits | 109,048 | 118 | 0.625 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 58,186 | 0.582 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 763,295 | 7.633 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 782,070 | 7.821 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 162,414 | 1.624 | 130 | 134 | fits | 80,447 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 181,481 | 1.815 | 130 | 134 | fits | 80,447 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 559,955 | 5.600 | 130 | 134 | fits | 80,840 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 578,841 | 5.788 | 130 | 134 | fits | 80,840 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 349,726 | 3.497 | 130 | 134 | fits | 80,106 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 368,874 | 3.689 | 130 | 134 | fits | 80,106 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 198,111 | 1.981 | 130 | 134 | fits | 80,447 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 216,073 | 2.161 | 130 | 134 | fits | 80,447 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 385,095 | 3.851 | 130 | 134 | fits | 80,106 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 403,130 | 4.031 | 130 | 134 | fits | 80,106 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 594,726 | 5.947 | 130 | 134 | fits | 80,840 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 612,226 | 6.122 | 130 | 134 | fits | 80,840 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 797,829 | 7.978 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 815,168 | 8.152 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 963,775 | 9.638 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 982,449 | 9.824 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 997,368 | 9.974 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 1,014,716 | 10.147 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 1,160,323 | 11.603 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 1,179,167 | 11.792 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 1,193,951 | 11.940 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 1,211,290 | 12.113 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 1,355,077 | 13.551 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 1,373,751 | 13.738 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 1,388,535 | 13.885 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 1,405,804 | 14.058 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 1,551,934 | 15.519 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 1,570,620 | 15.706 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 1,585,469 | 15.855 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 1,602,808 | 16.028 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 1,762,974 | 17.630 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 1,781,569 | 17.816 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 1,796,353 | 17.964 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 1,813,622 | 18.136 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 2,315,824 | 23.158 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 2,329,546 | 23.295 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 2,347,247 | 23.472 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 2,365,455 | 23.655 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 788,594 | 7.886 | 20 | 200 | fits | 150,480 | 217 | 0.393 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 908,054 | 9.081 | 20 | 20 | fits | 139,728 | 134 | 0.597 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 577,337 | 5.773 | 20 | 24 | fits | 156,830 | 123 | 0.483 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 728,851 | 7.289 | 20 | 50 | fits | 150,480 | 217 | 0.393 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,258,722 | 12.587 | 20 | 20 | fits | 97,595 | 99 | 0.651 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 87,525 | 0.875 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 762,874 | 7.629 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 781,649 | 7.816 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 162,403 | 1.624 | 130 | 134 | fits | 80,526 | 203 | 0.204 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 181,560 | 1.816 | 130 | 134 | fits | 80,526 | 203 | 0.204 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 349,525 | 3.495 | 130 | 134 | fits | 79,712 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 368,442 | 3.684 | 130 | 134 | fits | 79,712 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 559,534 | 5.595 | 130 | 134 | fits | 80,851 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 578,420 | 5.784 | 130 | 134 | fits | 80,851 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 198,190 | 1.982 | 130 | 134 | fits | 80,526 | 203 | 0.204 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 216,152 | 2.162 | 130 | 134 | fits | 80,526 | 203 | 0.204 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 384,663 | 3.847 | 130 | 134 | fits | 79,712 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 402,698 | 4.027 | 130 | 134 | fits | 79,712 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 594,305 | 5.943 | 130 | 134 | fits | 80,851 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 611,805 | 6.118 | 130 | 134 | fits | 80,851 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 797,408 | 7.974 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 814,747 | 8.147 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 963,354 | 9.634 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 982,028 | 9.820 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 996,947 | 9.969 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 1,014,295 | 10.143 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 1,159,902 | 11.599 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 1,178,746 | 11.787 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 1,193,530 | 11.935 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 1,210,869 | 12.109 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 1,354,656 | 13.547 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 1,373,330 | 13.733 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 1,388,114 | 13.881 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 1,405,383 | 14.054 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 1,551,513 | 15.515 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 1,570,199 | 15.702 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 1,585,048 | 15.850 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 1,602,387 | 16.024 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 1,762,553 | 17.626 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 1,781,148 | 17.811 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 1,795,932 | 17.959 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 1,813,201 | 18.132 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 2,315,403 | 23.154 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 2,329,125 | 23.291 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 2,346,826 | 23.468 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 2,365,034 | 23.650 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 157,262 | 1.573 | 20 | 200 | fits | 146,079 | 151 | 0.220 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 802,772 | 8.028 | 20 | 20 | fits | 135,926 | 137 | 0.618 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 646,642 | 6.466 | 20 | 24 | fits | 152,819 | 114 | 0.487 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 763,297 | 7.633 | 20 | 50 | fits | 135,926 | 137 | 0.618 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,175,650 | 11.757 | 20 | 20 | fits | 120,191 | 133 | 0.612 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 62,341 | 0.623 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 762,882 | 7.629 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 781,657 | 7.817 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 162,403 | 1.624 | 130 | 134 | fits | 80,436 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 181,470 | 1.815 | 130 | 134 | fits | 80,436 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 349,486 | 3.495 | 130 | 134 | fits | 79,712 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 368,403 | 3.684 | 130 | 134 | fits | 79,712 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 559,560 | 5.596 | 130 | 134 | fits | 80,772 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 578,446 | 5.784 | 130 | 134 | fits | 80,772 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 198,100 | 1.981 | 130 | 134 | fits | 80,436 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 216,062 | 2.161 | 130 | 134 | fits | 80,436 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 384,624 | 3.846 | 130 | 134 | fits | 79,712 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 402,659 | 4.027 | 130 | 134 | fits | 79,712 | 205 | 0.191 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 594,331 | 5.943 | 130 | 134 | fits | 80,772 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 611,831 | 6.118 | 130 | 134 | fits | 80,772 | 210 | 0.197 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 797,416 | 7.974 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 814,755 | 8.148 | 130 | 134 | fits | 77,393 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 963,362 | 9.634 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 982,036 | 9.820 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 996,955 | 9.970 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 1,014,303 | 10.143 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 1,159,910 | 11.599 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 1,178,754 | 11.788 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 1,193,538 | 11.935 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 1,210,877 | 12.109 | 130 | 134 | fits | 75,232 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 1,354,664 | 13.547 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 1,373,338 | 13.733 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 1,388,122 | 13.881 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 1,405,391 | 14.054 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 1,551,521 | 15.515 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 1,570,207 | 15.702 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 1,585,056 | 15.851 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 1,602,395 | 16.024 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 1,762,561 | 17.626 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 1,781,156 | 17.812 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 1,795,940 | 17.959 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 1,813,209 | 18.132 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 2,315,408 | 23.154 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 2,329,130 | 23.291 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 2,346,831 | 23.468 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 2,365,039 | 23.650 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 785,077 | 7.851 | 20 | 200 | fits | 150,165 | 212 | 0.396 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 904,133 | 9.041 | 20 | 20 | fits | 139,324 | 134 | 0.595 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 574,077 | 5.741 | 20 | 24 | fits | 157,574 | 127 | 0.476 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 725,334 | 7.253 | 20 | 50 | fits | 150,165 | 212 | 0.396 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,255,452 | 12.555 | 20 | 20 | fits | 98,916 | 107 | 0.642 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 86,714 | 0.867 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 766,740 | 7.667 | 130 | 134 | fits | 77,350 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 785,515 | 7.855 | 130 | 134 | fits | 77,350 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 162,414 | 1.624 | 130 | 134 | fits | 80,447 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 181,481 | 1.815 | 130 | 134 | fits | 80,447 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 563,767 | 5.638 | 130 | 134 | fits | 80,392 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 582,517 | 5.825 | 130 | 134 | fits | 80,392 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 373,859 | 3.739 | 130 | 134 | fits | 80,048 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 393,007 | 3.930 | 130 | 134 | fits | 80,048 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 198,111 | 1.981 | 130 | 134 | fits | 80,447 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 216,073 | 2.161 | 130 | 134 | fits | 80,447 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 409,228 | 4.092 | 130 | 134 | fits | 80,048 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 427,263 | 4.273 | 130 | 134 | fits | 80,048 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 598,300 | 5.983 | 130 | 134 | fits | 80,392 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 615,732 | 6.157 | 130 | 134 | fits | 80,392 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 801,274 | 8.013 | 130 | 134 | fits | 77,350 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 818,613 | 8.186 | 130 | 134 | fits | 77,350 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 967,220 | 9.672 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 985,894 | 9.859 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 1,000,813 | 10.008 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 1,018,161 | 10.182 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 1,163,689 | 11.637 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 1,182,533 | 11.825 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 1,197,317 | 11.973 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 1,214,656 | 12.147 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 1,358,443 | 13.584 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 1,377,117 | 13.771 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 1,391,901 | 13.919 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 1,409,170 | 14.092 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 1,555,300 | 15.553 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 1,573,986 | 15.740 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 1,588,835 | 15.888 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 1,606,174 | 16.062 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 1,766,340 | 17.663 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 1,784,935 | 17.849 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 1,799,719 | 17.997 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 1,816,988 | 18.170 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 2,319,190 | 23.192 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 2,332,912 | 23.329 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 2,350,613 | 23.506 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 2,368,821 | 23.688 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 708,104 | 7.081 | 20 | 200 | fits | 155,003 | 118 | 0.484 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 847,840 | 8.478 | 20 | 20 | fits | 139,792 | 139 | 0.638 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 667,632 | 6.676 | 20 | 24 | fits | 155,003 | 118 | 0.484 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 648,361 | 6.484 | 20 | 50 | fits | 155,003 | 118 | 0.484 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,170,594 | 11.706 | 20 | 20 | fits | 84,604 | 86 | 0.641 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 85,486 | 0.855 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 157,290 | 1.573 | 130 | 134 | fits | 80,566 | 205 | 0.201 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 176,305 | 1.763 | 130 | 134 | fits | 80,566 | 205 | 0.201 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 756,885 | 7.569 | 130 | 134 | fits | 77,098 | 205 | 0.192 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 775,571 | 7.756 | 130 | 134 | fits | 77,098 | 205 | 0.192 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 363,827 | 3.638 | 130 | 134 | fits | 79,578 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 382,744 | 3.827 | 130 | 134 | fits | 79,578 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 554,211 | 5.542 | 130 | 134 | fits | 80,352 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 572,961 | 5.730 | 130 | 134 | fits | 80,352 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 192,987 | 1.930 | 130 | 134 | fits | 80,566 | 205 | 0.201 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 210,949 | 2.109 | 130 | 134 | fits | 80,566 | 205 | 0.201 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 398,965 | 3.990 | 130 | 134 | fits | 79,578 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 417,000 | 4.170 | 130 | 134 | fits | 79,578 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 588,744 | 5.887 | 130 | 134 | fits | 80,352 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 606,176 | 6.062 | 130 | 134 | fits | 80,352 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 791,251 | 7.913 | 130 | 134 | fits | 77,098 | 205 | 0.192 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 808,590 | 8.086 | 130 | 134 | fits | 77,098 | 205 | 0.192 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 957,343 | 9.573 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 976,017 | 9.760 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 990,936 | 9.909 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 1,008,284 | 10.083 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 1,153,812 | 11.538 | 130 | 134 | fits | 75,134 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 1,172,656 | 11.727 | 130 | 134 | fits | 75,134 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 1,187,421 | 11.874 | 130 | 134 | fits | 75,134 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 1,204,760 | 12.048 | 130 | 134 | fits | 75,134 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 1,348,547 | 13.485 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 1,367,221 | 13.672 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 1,382,005 | 13.820 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 1,399,274 | 13.993 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 1,563,791 | 15.638 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 1,582,477 | 15.825 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 1,597,326 | 15.973 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 1,614,665 | 16.147 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 1,756,590 | 17.566 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 1,775,185 | 17.752 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 1,789,969 | 17.900 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 1,807,238 | 18.072 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 2,309,245 | 23.092 | 130 | 134 | fits | 70,820 | 202 | 0.168 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 2,322,967 | 23.230 | 130 | 134 | fits | 70,820 | 202 | 0.168 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 2,340,668 | 23.407 | 130 | 134 | fits | 70,820 | 202 | 0.168 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 2,358,876 | 23.589 | 130 | 134 | fits | 70,820 | 202 | 0.168 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 162,918 | 1.629 | 20 | 200 | fits | 157,104 | 211 | 0.377 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 848,064 | 8.481 | 20 | 20 | fits | 140,774 | 151 | 0.644 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 666,824 | 6.668 | 20 | 24 | fits | 154,237 | 120 | 0.488 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 808,589 | 8.086 | 20 | 50 | fits | 140,774 | 151 | 0.644 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,180,136 | 11.801 | 20 | 20 | fits | 95,348 | 99 | 0.622 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 86,241 | 0.862 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 553,852 | 5.539 | 130 | 134 | fits | 79,918 | 210 | 0.191 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 572,460 | 5.725 | 130 | 134 | fits | 79,918 | 210 | 0.191 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 363,705 | 3.637 | 130 | 134 | fits | 79,391 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 382,622 | 3.826 | 130 | 134 | fits | 79,391 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 157,170 | 1.572 | 130 | 134 | fits | 80,950 | 205 | 0.198 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 176,384 | 1.764 | 130 | 134 | fits | 80,950 | 205 | 0.198 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 756,731 | 7.567 | 130 | 134 | fits | 77,278 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 775,417 | 7.754 | 130 | 134 | fits | 77,278 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 192,947 | 1.929 | 130 | 134 | fits | 80,950 | 205 | 0.198 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 210,909 | 2.109 | 130 | 134 | fits | 80,950 | 205 | 0.198 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 398,843 | 3.988 | 130 | 134 | fits | 79,391 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 416,878 | 4.169 | 130 | 134 | fits | 79,391 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 588,322 | 5.883 | 130 | 134 | fits | 79,918 | 210 | 0.191 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 605,754 | 6.058 | 130 | 134 | fits | 79,918 | 210 | 0.191 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 791,097 | 7.911 | 130 | 134 | fits | 77,278 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 808,436 | 8.084 | 130 | 134 | fits | 77,278 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 957,043 | 9.570 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 975,717 | 9.757 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 990,636 | 9.906 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,007,984 | 10.080 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,153,512 | 11.535 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,172,356 | 11.724 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,187,140 | 11.871 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,204,479 | 12.045 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,348,266 | 13.483 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,366,940 | 13.669 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,381,724 | 13.817 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,398,993 | 13.990 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,563,510 | 15.635 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,582,196 | 15.822 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,597,045 | 15.970 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,614,384 | 16.144 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,756,309 | 17.563 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,774,904 | 17.749 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,789,688 | 17.897 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,806,957 | 18.070 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,309,121 | 23.091 | 130 | 134 | fits | 70,820 | 202 | 0.168 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,322,843 | 23.228 | 130 | 134 | fits | 70,820 | 202 | 0.168 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,340,544 | 23.405 | 130 | 134 | fits | 70,820 | 202 | 0.168 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,358,752 | 23.588 | 130 | 134 | fits | 70,820 | 202 | 0.168 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 736,899 | 7.369 | 20 | 200 | fits | 149,399 | 211 | 0.335 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 882,580 | 8.826 | 20 | 20 | fits | 140,963 | 143 | 0.635 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 516,260 | 5.163 | 20 | 24 | fits | 108,123 | 51 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 677,156 | 6.772 | 20 | 50 | fits | 149,399 | 211 | 0.335 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,225,899 | 12.259 | 20 | 20 | fits | 87,009 | 86 | 0.670 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 83,564 | 0.836 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 766,108 | 7.661 | 130 | 134 | fits | 77,350 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 784,883 | 7.849 | 130 | 134 | fits | 77,350 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 162,403 | 1.624 | 130 | 134 | fits | 80,436 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 181,470 | 1.815 | 130 | 134 | fits | 80,436 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 373,591 | 3.736 | 130 | 134 | fits | 79,654 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 392,508 | 3.925 | 130 | 134 | fits | 79,654 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 563,214 | 5.632 | 130 | 134 | fits | 80,245 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 581,964 | 5.820 | 130 | 134 | fits | 80,245 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 198,100 | 1.981 | 130 | 134 | fits | 80,436 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 216,062 | 2.161 | 130 | 134 | fits | 80,436 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 408,729 | 4.087 | 130 | 134 | fits | 79,654 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 426,764 | 4.268 | 130 | 134 | fits | 79,654 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 597,747 | 5.977 | 130 | 134 | fits | 80,245 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 615,179 | 6.152 | 130 | 134 | fits | 80,245 | 210 | 0.192 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 800,642 | 8.006 | 130 | 134 | fits | 77,350 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 817,981 | 8.180 | 130 | 134 | fits | 77,350 | 203 | 0.191 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 966,588 | 9.666 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 985,262 | 9.853 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 1,000,181 | 10.002 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 1,017,529 | 10.175 | 130 | 134 | fits | 76,443 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 1,163,057 | 11.631 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 1,181,901 | 11.819 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 1,196,685 | 11.967 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 1,214,024 | 12.140 | 130 | 134 | fits | 75,153 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 1,357,811 | 13.578 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 1,376,485 | 13.765 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 1,391,269 | 13.913 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 1,408,538 | 14.085 | 130 | 134 | fits | 74,569 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 1,554,668 | 15.547 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 1,573,354 | 15.734 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 1,588,203 | 15.882 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 1,605,542 | 16.055 | 130 | 134 | fits | 74,725 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 1,765,708 | 17.657 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 1,784,303 | 17.843 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 1,799,087 | 17.991 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 1,816,356 | 18.164 | 130 | 134 | fits | 74,315 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 2,318,322 | 23.183 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 2,332,044 | 23.320 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 2,349,745 | 23.497 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 2,367,953 | 23.680 | 130 | 134 | fits | 70,700 | 202 | 0.166 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 712,909 | 7.129 | 20 | 200 | fits | 151,132 | 215 | 0.362 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 858,061 | 8.581 | 20 | 20 | fits | 140,971 | 143 | 0.635 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 521,785 | 5.218 | 20 | 24 | fits | 108,142 | 51 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 653,166 | 6.532 | 20 | 50 | fits | 151,132 | 215 | 0.362 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,177,963 | 11.780 | 20 | 20 | fits | 83,687 | 82 | 0.648 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 83,162 | 0.832 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 473,375 | 4.734 | 130 | 134 | fits | 76,027 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 491,063 | 4.911 | 130 | 134 | fits | 76,027 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,946,114 | 19.461 | 130 | 134 | fits | 79,177 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,964,917 | 19.649 | 130 | 134 | fits | 79,177 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 259,718 | 2.597 | 130 | 134 | fits | 82,676 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 278,622 | 2.786 | 130 | 134 | fits | 82,676 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 601,987 | 6.020 | 130 | 134 | fits | 172,521 | 211 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 620,542 | 6.205 | 130 | 134 | fits | 172,521 | 211 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 754,066 | 7.541 | 130 | 134 | fits | 74,610 | 205 | 0.116 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 771,947 | 7.719 | 130 | 134 | fits | 74,610 | 205 | 0.116 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 787,812 | 7.878 | 130 | 134 | fits | 74,610 | 205 | 0.116 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 805,630 | 8.056 | 130 | 134 | fits | 74,610 | 205 | 0.116 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 1,980,585 | 19.806 | 130 | 134 | fits | 79,177 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 1,997,929 | 19.979 | 130 | 134 | fits | 79,177 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 2,127,277 | 21.273 | 130 | 134 | fits | 75,319 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 2,145,726 | 21.457 | 130 | 134 | fits | 75,319 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 296,277 | 2.963 | 130 | 134 | fits | 82,676 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 315,481 | 3.155 | 130 | 134 | fits | 82,676 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 393,480 | 3.935 | 130 | 134 | fits | 101,736 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 413,512 | 4.135 | 130 | 134 | fits | 101,736 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 430,088 | 4.301 | 130 | 134 | fits | 101,736 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 449,196 | 4.492 | 130 | 134 | fits | 101,736 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 507,195 | 5.072 | 130 | 134 | fits | 76,027 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 525,855 | 5.259 | 130 | 134 | fits | 76,027 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 636,568 | 6.366 | 130 | 134 | fits | 172,521 | 211 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 655,065 | 6.551 | 130 | 134 | fits | 172,521 | 211 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 2,160,478 | 21.605 | 130 | 134 | fits | 75,319 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 2,177,752 | 21.778 | 130 | 134 | fits | 75,319 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 2,321,481 | 23.215 | 130 | 134 | fits | 74,511 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 2,339,942 | 23.399 | 130 | 134 | fits | 74,511 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,354,689 | 23.547 | 130 | 134 | fits | 74,511 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,372,033 | 23.720 | 130 | 134 | fits | 74,511 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,513,988 | 25.140 | 130 | 134 | fits | 73,993 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,532,358 | 25.324 | 130 | 134 | fits | 73,993 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 2,547,040 | 25.470 | 130 | 134 | fits | 73,993 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 2,564,314 | 25.643 | 130 | 134 | fits | 73,993 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 2,712,254 | 27.123 | 130 | 134 | fits | 72,674 | 207 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,725,717 | 27.257 | 130 | 134 | fits | 72,674 | 207 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,743,484 | 27.435 | 130 | 134 | fits | 72,674 | 207 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 2,761,619 | 27.616 | 130 | 134 | fits | 72,674 | 207 | 0.176 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 852,467 | 8.525 | 20 | 200 | fits | 157,315 | 215 | 0.335 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 963,206 | 9.632 | 20 | 20 | fits | 131,007 | 125 | 0.646 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 654,680 | 6.547 | 20 | 24 | fits | 151,883 | 114 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 792,724 | 7.927 | 20 | 50 | fits | 157,315 | 215 | 0.335 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 1,249,626 | 12.496 | 20 | 20 | fits | 72,079 | 66 | 0.680 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 620,910 | 6.209 | 130 | 134 | fits | 75,075 | 205 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 638,650 | 6.386 | 130 | 134 | fits | 75,075 | 205 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,813,264 | 18.133 | 130 | 134 | fits | 79,568 | 203 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,832,218 | 18.322 | 130 | 134 | fits | 79,568 | 203 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 1,847,965 | 18.480 | 130 | 134 | fits | 79,568 | 203 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 1,865,239 | 18.652 | 130 | 134 | fits | 79,568 | 203 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 336,932 | 3.369 | 130 | 134 | fits | 82,442 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 355,921 | 3.559 | 130 | 134 | fits | 82,442 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 467,347 | 4.673 | 130 | 134 | fits | 174,923 | 211 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 486,607 | 4.866 | 130 | 134 | fits | 174,923 | 211 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 654,825 | 6.548 | 130 | 134 | fits | 75,075 | 205 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 672,874 | 6.729 | 130 | 134 | fits | 75,075 | 205 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 225,757 | 2.258 | 130 | 134 | fits | 103,754 | 213 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 245,957 | 2.460 | 130 | 134 | fits | 103,754 | 213 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 263,114 | 2.631 | 130 | 134 | fits | 103,754 | 213 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 281,912 | 2.819 | 130 | 134 | fits | 103,754 | 213 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 1,920,599 | 19.206 | 130 | 134 | fits | 76,420 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 1,939,190 | 19.392 | 130 | 134 | fits | 76,420 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 1,954,081 | 19.541 | 130 | 134 | fits | 76,420 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 1,971,659 | 19.717 | 130 | 134 | fits | 76,420 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 372,451 | 3.725 | 130 | 134 | fits | 82,442 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 391,421 | 3.914 | 130 | 134 | fits | 82,442 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 502,880 | 5.029 | 130 | 134 | fits | 174,923 | 211 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 521,678 | 5.217 | 130 | 134 | fits | 174,923 | 211 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 2,116,090 | 21.161 | 130 | 134 | fits | 74,442 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 2,134,691 | 21.347 | 130 | 134 | fits | 74,442 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 2,149,373 | 21.494 | 130 | 134 | fits | 74,442 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 2,166,647 | 21.666 | 130 | 134 | fits | 74,442 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 2,328,226 | 23.282 | 130 | 134 | fits | 74,555 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 2,346,839 | 23.468 | 130 | 134 | fits | 74,555 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 2,361,586 | 23.616 | 130 | 134 | fits | 74,555 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 2,378,930 | 23.789 | 130 | 134 | fits | 74,555 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,520,885 | 25.209 | 130 | 134 | fits | 74,145 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 2,539,407 | 25.394 | 130 | 134 | fits | 74,145 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 2,554,089 | 25.541 | 130 | 134 | fits | 74,145 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 2,571,363 | 25.714 | 130 | 134 | fits | 74,145 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 2,719,205 | 27.192 | 130 | 134 | fits | 72,740 | 207 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 2,732,888 | 27.329 | 130 | 134 | fits | 72,740 | 207 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 2,750,615 | 27.506 | 130 | 134 | fits | 72,740 | 207 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 2,768,750 | 27.688 | 130 | 134 | fits | 72,740 | 207 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 716,348 | 7.163 | 20 | 200 | fits | 156,845 | 216 | 0.320 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 826,885 | 8.269 | 20 | 20 | fits | 130,805 | 125 | 0.645 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 496,652 | 4.967 | 20 | 24 | fits | 107,834 | 50 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 656,605 | 6.566 | 20 | 50 | fits | 156,845 | 216 | 0.320 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,113,199 | 11.132 | 20 | 20 | fits | 75,749 | 72 | 0.676 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 1,814,779 | 18.148 | 130 | 134 | fits | 80,095 | 203 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,833,913 | 18.339 | 130 | 134 | fits | 80,095 | 203 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 227,565 | 2.276 | 130 | 134 | fits | 101,215 | 213 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 246,603 | 2.466 | 130 | 134 | fits | 101,215 | 213 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 468,352 | 4.684 | 130 | 134 | fits | 173,557 | 211 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 487,059 | 4.871 | 130 | 134 | fits | 173,557 | 211 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 1,849,717 | 18.497 | 130 | 134 | fits | 80,095 | 203 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 1,867,061 | 18.671 | 130 | 134 | fits | 80,095 | 203 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 1,922,265 | 19.223 | 130 | 134 | fits | 77,001 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 1,940,686 | 19.407 | 130 | 134 | fits | 77,001 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 337,648 | 3.376 | 130 | 134 | fits | 83,401 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 357,192 | 3.572 | 130 | 134 | fits | 83,401 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 621,412 | 6.214 | 130 | 134 | fits | 75,890 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 639,755 | 6.398 | 130 | 134 | fits | 75,890 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 655,926 | 6.559 | 130 | 134 | fits | 75,890 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 673,893 | 6.739 | 130 | 134 | fits | 75,890 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 1,956,736 | 19.567 | 130 | 134 | fits | 77,001 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 1,974,089 | 19.741 | 130 | 134 | fits | 77,001 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 263,504 | 2.635 | 130 | 134 | fits | 101,215 | 213 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 282,694 | 2.827 | 130 | 134 | fits | 101,215 | 213 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 373,822 | 3.738 | 130 | 134 | fits | 83,401 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 392,862 | 3.929 | 130 | 134 | fits | 83,401 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 503,253 | 5.033 | 130 | 134 | fits | 173,557 | 211 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 521,981 | 5.220 | 130 | 134 | fits | 173,557 | 211 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 2,118,716 | 21.187 | 130 | 134 | fits | 74,536 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 2,137,408 | 21.374 | 130 | 134 | fits | 74,536 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 2,152,090 | 21.521 | 130 | 134 | fits | 74,536 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 2,169,434 | 21.694 | 130 | 134 | fits | 74,536 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 2,331,013 | 23.310 | 130 | 134 | fits | 74,394 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 2,349,535 | 23.495 | 130 | 134 | fits | 74,394 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 2,364,282 | 23.643 | 130 | 134 | fits | 74,394 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 2,381,556 | 23.816 | 130 | 134 | fits | 74,394 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 2,523,511 | 25.235 | 130 | 134 | fits | 74,306 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 2,542,124 | 25.421 | 130 | 134 | fits | 74,306 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 2,556,806 | 25.568 | 130 | 134 | fits | 74,306 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 2,574,150 | 25.741 | 130 | 134 | fits | 74,306 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 2,722,063 | 27.221 | 130 | 134 | fits | 72,740 | 207 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,735,746 | 27.357 | 130 | 134 | fits | 72,740 | 207 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,753,473 | 27.535 | 130 | 134 | fits | 72,740 | 207 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 2,771,608 | 27.716 | 130 | 134 | fits | 72,740 | 207 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 707,028 | 7.070 | 20 | 200 | fits | 148,150 | 209 | 0.332 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 826,818 | 8.268 | 20 | 20 | fits | 140,058 | 135 | 0.616 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 490,764 | 4.908 | 20 | 24 | fits | 107,839 | 50 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 647,285 | 6.473 | 20 | 50 | fits | 148,150 | 209 | 0.332 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,113,246 | 11.132 | 20 | 20 | fits | 75,749 | 72 | 0.676 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,737,576 | 17.376 | 130 | 134 | fits | 79,921 | 203 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,756,620 | 17.566 | 130 | 134 | fits | 79,921 | 203 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 257,265 | 2.573 | 130 | 134 | fits | 76,812 | 205 | 0.097 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 275,094 | 2.751 | 130 | 134 | fits | 76,812 | 205 | 0.097 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 541,544 | 5.415 | 130 | 134 | fits | 74,397 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 559,425 | 5.594 | 130 | 134 | fits | 74,397 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 177,213 | 1.772 | 130 | 134 | fits | 102,531 | 211 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 196,804 | 1.968 | 130 | 134 | fits | 102,531 | 211 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 575,309 | 5.753 | 130 | 134 | fits | 74,397 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 592,814 | 5.928 | 130 | 134 | fits | 74,397 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 388,113 | 3.881 | 130 | 134 | fits | 174,779 | 211 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 407,515 | 4.075 | 130 | 134 | fits | 174,779 | 211 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 1,772,340 | 17.723 | 130 | 134 | fits | 79,921 | 203 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 1,789,684 | 17.897 | 130 | 134 | fits | 79,921 | 203 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 1,919,969 | 19.200 | 130 | 134 | fits | 77,178 | 203 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 1,938,570 | 19.386 | 130 | 134 | fits | 77,178 | 203 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 1,954,620 | 19.546 | 130 | 134 | fits | 77,178 | 203 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 1,971,973 | 19.720 | 130 | 134 | fits | 77,178 | 203 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 213,672 | 2.137 | 130 | 134 | fits | 102,531 | 211 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 232,932 | 2.329 | 130 | 134 | fits | 102,531 | 211 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 291,724 | 2.917 | 130 | 134 | fits | 76,812 | 205 | 0.097 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 310,694 | 3.107 | 130 | 134 | fits | 76,812 | 205 | 0.097 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 423,676 | 4.237 | 130 | 134 | fits | 174,779 | 211 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 442,404 | 4.424 | 130 | 134 | fits | 174,779 | 211 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 2,116,787 | 21.168 | 130 | 134 | fits | 74,536 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 2,135,479 | 21.355 | 130 | 134 | fits | 74,536 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 2,150,161 | 21.502 | 130 | 134 | fits | 74,536 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 2,167,505 | 21.675 | 130 | 134 | fits | 74,536 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 2,329,084 | 23.291 | 130 | 134 | fits | 74,394 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 2,347,606 | 23.476 | 130 | 134 | fits | 74,394 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,362,353 | 23.624 | 130 | 134 | fits | 74,394 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,379,627 | 23.796 | 130 | 134 | fits | 74,394 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,521,582 | 25.216 | 130 | 134 | fits | 74,306 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 2,540,195 | 25.402 | 130 | 134 | fits | 74,306 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 2,554,877 | 25.549 | 130 | 134 | fits | 74,306 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 2,572,221 | 25.722 | 130 | 134 | fits | 74,306 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 2,720,902 | 27.209 | 130 | 134 | fits | 70,768 | 202 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,734,496 | 27.345 | 130 | 134 | fits | 70,768 | 202 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,752,270 | 27.523 | 130 | 134 | fits | 70,768 | 202 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,770,405 | 27.704 | 130 | 134 | fits | 70,768 | 202 | 0.169 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 738,290 | 7.383 | 20 | 200 | fits | 156,744 | 216 | 0.319 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 849,022 | 8.490 | 20 | 20 | fits | 131,000 | 125 | 0.646 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 541,074 | 5.411 | 20 | 24 | fits | 154,082 | 120 | 0.475 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 678,547 | 6.785 | 20 | 50 | fits | 156,744 | 216 | 0.319 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,135,336 | 11.353 | 20 | 20 | fits | 72,069 | 66 | 0.678 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,870,033 | 18.700 | 130 | 134 | fits | 80,265 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,888,986 | 18.890 | 130 | 134 | fits | 80,265 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 521,393 | 5.214 | 130 | 134 | fits | 172,472 | 213 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 540,191 | 5.402 | 130 | 134 | fits | 172,472 | 213 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 673,498 | 6.735 | 130 | 134 | fits | 74,121 | 205 | 0.119 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 691,379 | 6.914 | 130 | 134 | fits | 74,121 | 205 | 0.119 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 311,336 | 3.113 | 130 | 134 | fits | 101,172 | 211 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 330,784 | 3.308 | 130 | 134 | fits | 101,172 | 211 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 347,332 | 3.473 | 130 | 134 | fits | 101,172 | 211 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 365,367 | 3.654 | 130 | 134 | fits | 101,172 | 211 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 390,703 | 3.907 | 130 | 134 | fits | 78,385 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 409,228 | 4.092 | 130 | 134 | fits | 78,385 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 556,281 | 5.563 | 130 | 134 | fits | 172,472 | 213 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 574,155 | 5.742 | 130 | 134 | fits | 172,472 | 213 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 707,100 | 7.071 | 130 | 134 | fits | 74,121 | 205 | 0.119 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 724,605 | 7.246 | 130 | 134 | fits | 74,121 | 205 | 0.119 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 1,905,138 | 19.051 | 130 | 134 | fits | 80,265 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 1,922,491 | 19.225 | 130 | 134 | fits | 80,265 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 2,014,759 | 20.148 | 130 | 134 | fits | 75,076 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 2,033,605 | 20.336 | 130 | 134 | fits | 75,076 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 425,831 | 4.258 | 130 | 134 | fits | 78,385 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 444,801 | 4.448 | 130 | 134 | fits | 78,385 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 2,048,366 | 20.484 | 130 | 134 | fits | 75,076 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 2,065,710 | 20.657 | 130 | 134 | fits | 75,076 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 2,228,065 | 22.281 | 130 | 134 | fits | 74,399 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 2,246,666 | 22.467 | 130 | 134 | fits | 74,399 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 2,261,348 | 22.613 | 130 | 134 | fits | 74,399 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 2,278,622 | 22.786 | 130 | 134 | fits | 74,399 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 2,421,809 | 24.218 | 130 | 134 | fits | 74,555 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 2,440,422 | 24.404 | 130 | 134 | fits | 74,555 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 2,455,169 | 24.552 | 130 | 134 | fits | 74,555 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 2,472,513 | 24.725 | 130 | 134 | fits | 74,555 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 2,614,468 | 26.145 | 130 | 134 | fits | 74,145 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 2,632,990 | 26.330 | 130 | 134 | fits | 74,145 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 2,647,672 | 26.477 | 130 | 134 | fits | 74,145 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 2,664,946 | 26.649 | 130 | 134 | fits | 74,145 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 2,813,602 | 28.136 | 130 | 134 | fits | 70,809 | 202 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 2,827,196 | 28.272 | 130 | 134 | fits | 70,809 | 202 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,844,970 | 28.450 | 130 | 134 | fits | 70,809 | 202 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,863,105 | 28.631 | 130 | 134 | fits | 70,809 | 202 | 0.170 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 764,419 | 7.644 | 20 | 200 | fits | 148,762 | 209 | 0.339 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 884,332 | 8.843 | 20 | 20 | fits | 140,181 | 135 | 0.616 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 575,185 | 5.752 | 20 | 24 | fits | 152,872 | 114 | 0.478 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 704,676 | 7.047 | 20 | 50 | fits | 148,762 | 209 | 0.339 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 1,171,338 | 11.713 | 20 | 20 | fits | 72,239 | 66 | 0.680 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 259,174 | 2.592 | 130 | 134 | fits | 82,307 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 277,950 | 2.780 | 130 | 134 | fits | 82,307 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 471,610 | 4.716 | 130 | 134 | fits | 75,488 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 489,208 | 4.892 | 130 | 134 | fits | 75,488 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 1,673,735 | 16.737 | 130 | 134 | fits | 79,590 | 203 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 1,692,538 | 16.925 | 130 | 134 | fits | 79,590 | 203 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 1,708,138 | 17.081 | 130 | 134 | fits | 79,590 | 203 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 1,725,482 | 17.255 | 130 | 134 | fits | 79,590 | 203 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 1,818,923 | 18.189 | 130 | 134 | fits | 77,236 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 1,837,293 | 18.373 | 130 | 134 | fits | 77,236 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 1,853,024 | 18.530 | 130 | 134 | fits | 77,236 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 1,870,611 | 18.706 | 130 | 134 | fits | 77,236 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 392,898 | 3.929 | 130 | 134 | fits | 101,290 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 412,377 | 4.124 | 130 | 134 | fits | 101,290 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 2,017,067 | 20.171 | 130 | 134 | fits | 77,115 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 2,035,607 | 20.356 | 130 | 134 | fits | 77,115 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 2,051,657 | 20.517 | 130 | 134 | fits | 77,115 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 2,069,080 | 20.691 | 130 | 134 | fits | 77,115 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 428,890 | 4.289 | 130 | 134 | fits | 101,290 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 447,849 | 4.478 | 130 | 134 | fits | 101,290 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 295,110 | 2.951 | 130 | 134 | fits | 82,307 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 314,612 | 3.146 | 130 | 134 | fits | 82,307 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 505,419 | 5.054 | 130 | 134 | fits | 75,488 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 524,079 | 5.241 | 130 | 134 | fits | 75,488 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 2,213,894 | 22.139 | 130 | 134 | fits | 74,223 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 2,232,343 | 22.323 | 130 | 134 | fits | 74,223 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 2,247,025 | 22.470 | 130 | 134 | fits | 74,223 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 2,264,299 | 22.643 | 130 | 134 | fits | 74,223 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 2,425,878 | 24.259 | 130 | 134 | fits | 74,403 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 2,444,339 | 24.443 | 130 | 134 | fits | 74,403 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 2,459,086 | 24.591 | 130 | 134 | fits | 74,403 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 2,476,430 | 24.764 | 130 | 134 | fits | 74,403 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 2,626,855 | 26.269 | 130 | 134 | fits | 76,077 | 208 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 2,645,285 | 26.453 | 130 | 134 | fits | 76,077 | 208 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 2,659,910 | 26.599 | 130 | 134 | fits | 76,077 | 208 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 2,677,184 | 26.772 | 130 | 134 | fits | 76,077 | 208 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,817,468 | 28.175 | 130 | 134 | fits | 70,666 | 202 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,830,842 | 28.308 | 130 | 134 | fits | 70,666 | 202 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,848,656 | 28.487 | 130 | 134 | fits | 70,666 | 202 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,866,791 | 28.668 | 130 | 134 | fits | 70,666 | 202 | 0.168 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 670,138 | 6.701 | 20 | 200 | fits | 149,362 | 214 | 0.336 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 790,231 | 7.902 | 20 | 20 | fits | 140,361 | 135 | 0.616 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 501,566 | 5.016 | 20 | 24 | fits | 107,827 | 50 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 610,395 | 6.104 | 20 | 50 | fits | 149,362 | 214 | 0.336 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,077,087 | 10.771 | 20 | 20 | fits | 75,921 | 72 | 0.676 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 259,463 | 2.595 | 130 | 134 | fits | 79,442 | 205 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 278,241 | 2.782 | 130 | 134 | fits | 79,442 | 205 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,744,440 | 17.444 | 130 | 134 | fits | 79,560 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,763,243 | 17.632 | 130 | 134 | fits | 79,560 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 1,778,990 | 17.790 | 130 | 134 | fits | 79,560 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 1,796,334 | 17.963 | 130 | 134 | fits | 79,560 | 203 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 294,460 | 2.945 | 130 | 134 | fits | 79,442 | 205 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 312,266 | 3.123 | 130 | 134 | fits | 79,442 | 205 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 389,595 | 3.896 | 130 | 134 | fits | 175,250 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 408,381 | 4.084 | 130 | 134 | fits | 175,250 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 544,010 | 5.440 | 130 | 134 | fits | 76,001 | 205 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 562,356 | 5.624 | 130 | 134 | fits | 76,001 | 205 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 578,260 | 5.783 | 130 | 134 | fits | 76,001 | 205 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 595,996 | 5.960 | 130 | 134 | fits | 76,001 | 205 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 1,927,208 | 19.272 | 130 | 134 | fits | 77,181 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 1,945,578 | 19.456 | 130 | 134 | fits | 77,181 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 1,961,628 | 19.616 | 130 | 134 | fits | 77,181 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 1,978,981 | 19.790 | 130 | 134 | fits | 77,181 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 2,124,994 | 21.250 | 130 | 134 | fits | 74,852 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,143,688 | 21.437 | 130 | 134 | fits | 74,852 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 425,013 | 4.250 | 130 | 134 | fits | 175,250 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 444,051 | 4.441 | 130 | 134 | fits | 175,250 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 2,158,449 | 21.584 | 130 | 134 | fits | 74,852 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 2,175,793 | 21.758 | 130 | 134 | fits | 74,852 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 2,319,610 | 23.196 | 130 | 134 | fits | 74,247 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 2,338,059 | 23.381 | 130 | 134 | fits | 74,247 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 2,352,741 | 23.527 | 130 | 134 | fits | 74,247 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 2,370,015 | 23.700 | 130 | 134 | fits | 74,247 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 2,513,202 | 25.132 | 130 | 134 | fits | 74,403 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 2,531,663 | 25.317 | 130 | 134 | fits | 74,403 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 2,546,410 | 25.464 | 130 | 134 | fits | 74,403 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 2,563,754 | 25.638 | 130 | 134 | fits | 74,403 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 2,714,931 | 27.149 | 130 | 134 | fits | 74,182 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 2,733,301 | 27.333 | 130 | 134 | fits | 74,182 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 2,747,983 | 27.480 | 130 | 134 | fits | 74,182 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 2,765,257 | 27.653 | 130 | 134 | fits | 74,182 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,922,262 | 29.223 | 130 | 134 | fits | 70,582 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,935,636 | 29.356 | 130 | 134 | fits | 70,582 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,953,450 | 29.535 | 130 | 134 | fits | 70,582 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,971,585 | 29.716 | 130 | 134 | fits | 70,582 | 202 | 0.166 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 749,085 | 7.491 | 20 | 200 | fits | 156,965 | 216 | 0.319 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 859,894 | 8.599 | 20 | 20 | fits | 131,077 | 125 | 0.646 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 551,648 | 5.516 | 20 | 24 | fits | 155,458 | 126 | 0.469 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 689,342 | 6.893 | 20 | 50 | fits | 156,965 | 216 | 0.319 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 1,146,750 | 11.467 | 20 | 20 | fits | 72,221 | 66 | 0.678 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 264,067 | 2.641 | 130 | 134 | fits | 82,111 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 282,627 | 2.826 | 130 | 134 | fits | 82,111 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,753,945 | 17.539 | 130 | 134 | fits | 79,399 | 203 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,772,657 | 17.727 | 130 | 134 | fits | 79,399 | 203 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 1,788,404 | 17.884 | 130 | 134 | fits | 79,399 | 203 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 1,805,678 | 18.057 | 130 | 134 | fits | 79,399 | 203 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 1,917,847 | 19.178 | 130 | 134 | fits | 76,835 | 203 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 1,936,308 | 19.363 | 130 | 134 | fits | 76,835 | 203 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 397,454 | 3.975 | 130 | 134 | fits | 174,949 | 211 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 416,562 | 4.166 | 130 | 134 | fits | 174,949 | 211 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 551,491 | 5.515 | 130 | 134 | fits | 77,408 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 570,068 | 5.701 | 130 | 134 | fits | 77,408 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 1,951,847 | 19.518 | 130 | 134 | fits | 76,835 | 203 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 1,969,191 | 19.692 | 130 | 134 | fits | 76,835 | 203 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 2,134,183 | 21.342 | 130 | 134 | fits | 75,393 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 2,152,632 | 21.526 | 130 | 134 | fits | 75,393 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 300,342 | 3.003 | 130 | 134 | fits | 82,111 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 319,546 | 3.195 | 130 | 134 | fits | 82,111 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 432,811 | 4.328 | 130 | 134 | fits | 174,949 | 211 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 451,609 | 4.516 | 130 | 134 | fits | 174,949 | 211 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 586,152 | 5.862 | 130 | 134 | fits | 77,408 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 604,660 | 6.047 | 130 | 134 | fits | 77,408 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 2,167,384 | 21.674 | 130 | 134 | fits | 75,393 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 2,184,658 | 21.847 | 130 | 134 | fits | 75,393 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 2,329,110 | 23.291 | 130 | 134 | fits | 74,451 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 2,347,650 | 23.477 | 130 | 134 | fits | 74,451 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 2,362,332 | 23.623 | 130 | 134 | fits | 74,451 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 2,379,676 | 23.797 | 130 | 134 | fits | 74,451 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 2,522,928 | 25.229 | 130 | 134 | fits | 74,307 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 2,541,298 | 25.413 | 130 | 134 | fits | 74,307 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 2,556,045 | 25.560 | 130 | 134 | fits | 74,307 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 2,573,319 | 25.733 | 130 | 134 | fits | 74,307 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 2,724,616 | 27.246 | 130 | 134 | fits | 74,343 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 2,743,077 | 27.431 | 130 | 134 | fits | 74,343 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 2,757,759 | 27.578 | 130 | 134 | fits | 74,343 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 2,775,103 | 27.751 | 130 | 134 | fits | 74,343 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 2,914,081 | 29.141 | 130 | 134 | fits | 70,582 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,927,455 | 29.275 | 130 | 134 | fits | 70,582 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,945,269 | 29.453 | 130 | 134 | fits | 70,582 | 202 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 2,963,404 | 29.634 | 130 | 134 | fits | 70,582 | 202 | 0.166 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 755,225 | 7.552 | 20 | 200 | fits | 157,754 | 215 | 0.336 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 865,934 | 8.659 | 20 | 20 | fits | 130,977 | 125 | 0.645 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 556,999 | 5.570 | 20 | 24 | fits | 155,214 | 126 | 0.464 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 695,482 | 6.955 | 20 | 50 | fits | 157,754 | 215 | 0.336 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 1,152,851 | 11.529 | 20 | 20 | fits | 72,221 | 66 | 0.678 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
