### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 728 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 9.636 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.adp.if0` (notice-burst-5) | 8.495 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-1.held.aecp.if0` (notice-every-1) | 6.656 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-1.held.maap.if0` (notice-every-1) | 8.027 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-2.held.srp.if0` (notice-every-2) | 12.734 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-6.mrpdu.periodic.if0` (notice-every-6) | 1.184 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-1.notices.29.36.0.if0` (notice-burst-1) | 30.170 (31.308) | fits | 0 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1385 | 0 | 163,992 (1.640) | fits |
| notice-every-1 | 1385 | 0 | 164,444 (1.644) | fits |
| notice-every-2 | 1384 | 0 | 169,042 (1.690) | fits |
| notice-every-3 | 1381 | 0 | 168,165 (1.682) | fits |
| notice-every-4 | 1385 | 0 | 164,192 (1.642) | fits |
| notice-every-5 | 1375 | 0 | 164,136 (1.641) | fits |
| notice-every-6 | 1387 | 0 | 167,891 (1.679) | fits |
| notice-every-7 | 1382 | 0 | 163,992 (1.640) | fits |
| notice-burst-0 | 1063 | 0 | 171,296 (1.713) | fits |
| notice-burst-1 | 1064 | 0 | 174,608 (1.746) | fits |
| notice-burst-2 | 1069 | 0 | 173,768 (1.738) | fits |
| notice-burst-3 | 1055 | 0 | 173,858 (1.739) | fits |
| notice-burst-4 | 1060 | 0 | 173,712 (1.737) | fits |
| notice-burst-5 | 1050 | 0 | 172,588 (1.726) | fits |
| notice-burst-6 | 1064 | 0 | 170,180 (1.702) | fits |
| notice-burst-7 | 1063 | 0 | 173,442 (1.734) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 7.773 | 130 | 16 | 2 | within |
| notice-every-0 | 7.948 | 130 | 16 | 2 | within |
| notice-every-0 | 1.670 | 130 | 16 | 2 | within |
| notice-every-0 | 1.847 | 130 | 16 | 2 | within |
| notice-every-0 | 3.556 | 130 | 16 | 2 | within |
| notice-every-0 | 3.733 | 130 | 16 | 2 | within |
| notice-every-0 | 5.675 | 130 | 16 | 2 | within |
| notice-every-0 | 5.852 | 130 | 16 | 2 | within |
| notice-every-0 | 2.007 | 130 | 16 | 2 | within |
| notice-every-0 | 2.180 | 130 | 16 | 2 | within |
| notice-every-0 | 3.892 | 130 | 16 | 2 | within |
| notice-every-0 | 4.067 | 130 | 16 | 2 | within |
| notice-every-0 | 6.008 | 130 | 16 | 2 | within |
| notice-every-0 | 6.178 | 130 | 16 | 2 | within |
| notice-every-0 | 8.101 | 130 | 16 | 2 | within |
| notice-every-0 | 8.267 | 130 | 16 | 2 | within |
| notice-every-0 | 9.601 | 130 | 16 | 2 | within |
| notice-every-0 | 9.777 | 130 | 16 | 2 | within |
| notice-every-0 | 9.922 | 130 | 16 | 2 | within |
| notice-every-0 | 10.089 | 130 | 16 | 2 | within |
| notice-every-0 | 11.601 | 130 | 16 | 2 | within |
| notice-every-0 | 11.776 | 130 | 16 | 2 | within |
| notice-every-0 | 11.921 | 130 | 16 | 2 | within |
| notice-every-0 | 12.087 | 130 | 16 | 2 | within |
| notice-every-0 | 13.581 | 130 | 16 | 2 | within |
| notice-every-0 | 13.756 | 130 | 16 | 2 | within |
| notice-every-0 | 13.901 | 130 | 16 | 2 | within |
| notice-every-0 | 14.068 | 130 | 16 | 2 | within |
| notice-every-0 | 15.603 | 130 | 16 | 2 | within |
| notice-every-0 | 15.777 | 130 | 16 | 2 | within |
| notice-every-0 | 15.922 | 130 | 16 | 2 | within |
| notice-every-0 | 16.088 | 130 | 16 | 2 | within |
| notice-every-0 | 17.564 | 130 | 16 | 2 | within |
| notice-every-0 | 17.737 | 130 | 16 | 2 | within |
| notice-every-0 | 17.882 | 130 | 16 | 2 | within |
| notice-every-0 | 18.050 | 130 | 16 | 2 | within |
| notice-every-0 | 23.127 | 130 | 16 | 2 | within |
| notice-every-0 | 23.251 | 130 | 16 | 2 | within |
| notice-every-0 | 23.420 | 130 | 16 | 2 | within |
| notice-every-0 | 23.592 | 130 | 16 | 2 | within |
| notice-every-1 | 7.523 | 130 | 16 | 2 | within |
| notice-every-1 | 7.698 | 130 | 16 | 2 | within |
| notice-every-1 | 1.461 | 130 | 16 | 2 | within |
| notice-every-1 | 1.638 | 130 | 16 | 2 | within |
| notice-every-1 | 3.556 | 130 | 16 | 2 | within |
| notice-every-1 | 3.733 | 130 | 16 | 2 | within |
| notice-every-1 | 5.452 | 130 | 16 | 2 | within |
| notice-every-1 | 5.627 | 130 | 16 | 2 | within |
| notice-every-1 | 1.797 | 130 | 16 | 2 | within |
| notice-every-1 | 1.971 | 130 | 16 | 2 | within |
| notice-every-1 | 3.893 | 130 | 16 | 2 | within |
| notice-every-1 | 4.068 | 130 | 16 | 2 | within |
| notice-every-1 | 5.784 | 130 | 16 | 2 | within |
| notice-every-1 | 5.953 | 130 | 16 | 2 | within |
| notice-every-1 | 7.850 | 130 | 16 | 2 | within |
| notice-every-1 | 8.016 | 130 | 16 | 2 | within |
| notice-every-1 | 9.562 | 130 | 16 | 2 | within |
| notice-every-1 | 9.736 | 130 | 16 | 2 | within |
| notice-every-1 | 9.881 | 130 | 16 | 2 | within |
| notice-every-1 | 10.049 | 130 | 16 | 2 | within |
| notice-every-1 | 11.560 | 130 | 16 | 2 | within |
| notice-every-1 | 11.734 | 130 | 16 | 2 | within |
| notice-every-1 | 11.879 | 130 | 16 | 2 | within |
| notice-every-1 | 12.045 | 130 | 16 | 2 | within |
| notice-every-1 | 13.540 | 130 | 16 | 2 | within |
| notice-every-1 | 13.714 | 130 | 16 | 2 | within |
| notice-every-1 | 13.859 | 130 | 16 | 2 | within |
| notice-every-1 | 14.025 | 130 | 16 | 2 | within |
| notice-every-1 | 15.560 | 130 | 16 | 2 | within |
| notice-every-1 | 15.733 | 130 | 16 | 2 | within |
| notice-every-1 | 15.878 | 130 | 16 | 2 | within |
| notice-every-1 | 16.045 | 130 | 16 | 2 | within |
| notice-every-1 | 17.521 | 130 | 16 | 2 | within |
| notice-every-1 | 17.694 | 130 | 16 | 2 | within |
| notice-every-1 | 17.839 | 130 | 16 | 2 | within |
| notice-every-1 | 18.007 | 130 | 16 | 2 | within |
| notice-every-1 | 23.083 | 130 | 16 | 2 | within |
| notice-every-1 | 23.207 | 130 | 16 | 2 | within |
| notice-every-1 | 23.377 | 130 | 16 | 2 | within |
| notice-every-1 | 23.548 | 130 | 16 | 2 | within |
| notice-every-2 | 7.522 | 130 | 16 | 2 | within |
| notice-every-2 | 7.696 | 130 | 16 | 2 | within |
| notice-every-2 | 1.460 | 130 | 16 | 2 | within |
| notice-every-2 | 1.637 | 130 | 16 | 2 | within |
| notice-every-2 | 3.556 | 130 | 16 | 2 | within |
| notice-every-2 | 3.733 | 130 | 16 | 2 | within |
| notice-every-2 | 5.449 | 130 | 16 | 2 | within |
| notice-every-2 | 5.624 | 130 | 16 | 2 | within |
| notice-every-2 | 1.797 | 130 | 16 | 2 | within |
| notice-every-2 | 1.970 | 130 | 16 | 2 | within |
| notice-every-2 | 3.892 | 130 | 16 | 2 | within |
| notice-every-2 | 4.067 | 130 | 16 | 2 | within |
| notice-every-2 | 5.781 | 130 | 16 | 2 | within |
| notice-every-2 | 5.950 | 130 | 16 | 2 | within |
| notice-every-2 | 7.849 | 130 | 16 | 2 | within |
| notice-every-2 | 8.015 | 130 | 16 | 2 | within |
| notice-every-2 | 9.561 | 130 | 16 | 2 | within |
| notice-every-2 | 9.735 | 130 | 16 | 2 | within |
| notice-every-2 | 9.881 | 130 | 16 | 2 | within |
| notice-every-2 | 10.048 | 130 | 16 | 2 | within |
| notice-every-2 | 11.559 | 130 | 16 | 2 | within |
| notice-every-2 | 11.733 | 130 | 16 | 2 | within |
| notice-every-2 | 11.878 | 130 | 16 | 2 | within |
| notice-every-2 | 12.044 | 130 | 16 | 2 | within |
| notice-every-2 | 13.538 | 130 | 16 | 2 | within |
| notice-every-2 | 13.712 | 130 | 16 | 2 | within |
| notice-every-2 | 13.858 | 130 | 16 | 2 | within |
| notice-every-2 | 14.024 | 130 | 16 | 2 | within |
| notice-every-2 | 15.559 | 130 | 16 | 2 | within |
| notice-every-2 | 15.732 | 130 | 16 | 2 | within |
| notice-every-2 | 15.877 | 130 | 16 | 2 | within |
| notice-every-2 | 16.043 | 130 | 16 | 2 | within |
| notice-every-2 | 17.520 | 130 | 16 | 2 | within |
| notice-every-2 | 17.693 | 130 | 16 | 2 | within |
| notice-every-2 | 17.837 | 130 | 16 | 2 | within |
| notice-every-2 | 18.005 | 130 | 16 | 2 | within |
| notice-every-2 | 23.081 | 130 | 16 | 2 | within |
| notice-every-2 | 23.204 | 130 | 16 | 2 | within |
| notice-every-2 | 23.374 | 130 | 16 | 2 | within |
| notice-every-2 | 23.546 | 130 | 16 | 2 | within |
| notice-every-3 | 7.521 | 130 | 16 | 2 | within |
| notice-every-3 | 7.696 | 130 | 16 | 2 | within |
| notice-every-3 | 1.460 | 130 | 16 | 2 | within |
| notice-every-3 | 1.637 | 130 | 16 | 2 | within |
| notice-every-3 | 3.556 | 130 | 16 | 2 | within |
| notice-every-3 | 3.733 | 130 | 16 | 2 | within |
| notice-every-3 | 5.448 | 130 | 16 | 2 | within |
| notice-every-3 | 5.624 | 130 | 16 | 2 | within |
| notice-every-3 | 1.797 | 130 | 16 | 2 | within |
| notice-every-3 | 1.970 | 130 | 16 | 2 | within |
| notice-every-3 | 3.892 | 130 | 16 | 2 | within |
| notice-every-3 | 4.067 | 130 | 16 | 2 | within |
| notice-every-3 | 5.781 | 130 | 16 | 2 | within |
| notice-every-3 | 5.950 | 130 | 16 | 2 | within |
| notice-every-3 | 7.848 | 130 | 16 | 2 | within |
| notice-every-3 | 8.015 | 130 | 16 | 2 | within |
| notice-every-3 | 9.561 | 130 | 16 | 2 | within |
| notice-every-3 | 9.735 | 130 | 16 | 2 | within |
| notice-every-3 | 9.880 | 130 | 16 | 2 | within |
| notice-every-3 | 10.048 | 130 | 16 | 2 | within |
| notice-every-3 | 11.558 | 130 | 16 | 2 | within |
| notice-every-3 | 11.733 | 130 | 16 | 2 | within |
| notice-every-3 | 11.877 | 130 | 16 | 2 | within |
| notice-every-3 | 12.044 | 130 | 16 | 2 | within |
| notice-every-3 | 13.538 | 130 | 16 | 2 | within |
| notice-every-3 | 13.712 | 130 | 16 | 2 | within |
| notice-every-3 | 13.857 | 130 | 16 | 2 | within |
| notice-every-3 | 14.024 | 130 | 16 | 2 | within |
| notice-every-3 | 15.559 | 130 | 16 | 2 | within |
| notice-every-3 | 15.732 | 130 | 16 | 2 | within |
| notice-every-3 | 15.877 | 130 | 16 | 2 | within |
| notice-every-3 | 16.043 | 130 | 16 | 2 | within |
| notice-every-3 | 17.519 | 130 | 16 | 2 | within |
| notice-every-3 | 17.692 | 130 | 16 | 2 | within |
| notice-every-3 | 17.837 | 130 | 16 | 2 | within |
| notice-every-3 | 18.005 | 130 | 16 | 2 | within |
| notice-every-3 | 23.080 | 130 | 16 | 2 | within |
| notice-every-3 | 23.204 | 130 | 16 | 2 | within |
| notice-every-3 | 23.373 | 130 | 16 | 2 | within |
| notice-every-3 | 23.545 | 130 | 16 | 2 | within |
| notice-every-4 | 7.523 | 130 | 16 | 2 | within |
| notice-every-4 | 7.697 | 130 | 16 | 2 | within |
| notice-every-4 | 1.461 | 130 | 16 | 2 | within |
| notice-every-4 | 1.638 | 130 | 16 | 2 | within |
| notice-every-4 | 5.450 | 130 | 16 | 2 | within |
| notice-every-4 | 5.626 | 130 | 16 | 2 | within |
| notice-every-4 | 3.560 | 130 | 16 | 2 | within |
| notice-every-4 | 3.739 | 130 | 16 | 2 | within |
| notice-every-4 | 1.797 | 130 | 16 | 2 | within |
| notice-every-4 | 1.970 | 130 | 16 | 2 | within |
| notice-every-4 | 3.898 | 130 | 16 | 2 | within |
| notice-every-4 | 4.073 | 130 | 16 | 2 | within |
| notice-every-4 | 5.782 | 130 | 16 | 2 | within |
| notice-every-4 | 5.952 | 130 | 16 | 2 | within |
| notice-every-4 | 7.850 | 130 | 16 | 2 | within |
| notice-every-4 | 8.016 | 130 | 16 | 2 | within |
| notice-every-4 | 9.562 | 130 | 16 | 2 | within |
| notice-every-4 | 9.737 | 130 | 16 | 2 | within |
| notice-every-4 | 9.882 | 130 | 16 | 2 | within |
| notice-every-4 | 10.049 | 130 | 16 | 2 | within |
| notice-every-4 | 11.561 | 130 | 16 | 2 | within |
| notice-every-4 | 11.735 | 130 | 16 | 2 | within |
| notice-every-4 | 11.880 | 130 | 16 | 2 | within |
| notice-every-4 | 12.046 | 130 | 16 | 2 | within |
| notice-every-4 | 13.540 | 130 | 16 | 2 | within |
| notice-every-4 | 13.714 | 130 | 16 | 2 | within |
| notice-every-4 | 13.860 | 130 | 16 | 2 | within |
| notice-every-4 | 14.026 | 130 | 16 | 2 | within |
| notice-every-4 | 15.560 | 130 | 16 | 2 | within |
| notice-every-4 | 15.733 | 130 | 16 | 2 | within |
| notice-every-4 | 15.878 | 130 | 16 | 2 | within |
| notice-every-4 | 16.045 | 130 | 16 | 2 | within |
| notice-every-4 | 17.521 | 130 | 16 | 2 | within |
| notice-every-4 | 17.694 | 130 | 16 | 2 | within |
| notice-every-4 | 17.838 | 130 | 16 | 2 | within |
| notice-every-4 | 18.007 | 130 | 16 | 2 | within |
| notice-every-4 | 23.084 | 130 | 16 | 2 | within |
| notice-every-4 | 23.208 | 130 | 16 | 2 | within |
| notice-every-4 | 23.378 | 130 | 16 | 2 | within |
| notice-every-4 | 23.549 | 130 | 16 | 2 | within |
| notice-every-5 | 7.529 | 130 | 16 | 2 | within |
| notice-every-5 | 7.704 | 130 | 16 | 2 | within |
| notice-every-5 | 1.670 | 130 | 16 | 2 | within |
| notice-every-5 | 1.847 | 130 | 16 | 2 | within |
| notice-every-5 | 5.677 | 130 | 16 | 2 | within |
| notice-every-5 | 5.854 | 130 | 16 | 2 | within |
| notice-every-5 | 3.560 | 130 | 16 | 2 | within |
| notice-every-5 | 3.739 | 130 | 16 | 2 | within |
| notice-every-5 | 2.007 | 130 | 16 | 2 | within |
| notice-every-5 | 2.181 | 130 | 16 | 2 | within |
| notice-every-5 | 3.899 | 130 | 16 | 2 | within |
| notice-every-5 | 4.074 | 130 | 16 | 2 | within |
| notice-every-5 | 6.010 | 130 | 16 | 2 | within |
| notice-every-5 | 6.180 | 130 | 16 | 2 | within |
| notice-every-5 | 7.856 | 130 | 16 | 2 | within |
| notice-every-5 | 8.023 | 130 | 16 | 2 | within |
| notice-every-5 | 9.570 | 130 | 16 | 2 | within |
| notice-every-5 | 9.746 | 130 | 16 | 2 | within |
| notice-every-5 | 9.891 | 130 | 16 | 2 | within |
| notice-every-5 | 10.058 | 130 | 16 | 2 | within |
| notice-every-5 | 11.569 | 130 | 16 | 2 | within |
| notice-every-5 | 11.744 | 130 | 16 | 2 | within |
| notice-every-5 | 11.889 | 130 | 16 | 2 | within |
| notice-every-5 | 12.055 | 130 | 16 | 2 | within |
| notice-every-5 | 13.550 | 130 | 16 | 2 | within |
| notice-every-5 | 13.724 | 130 | 16 | 2 | within |
| notice-every-5 | 13.870 | 130 | 16 | 2 | within |
| notice-every-5 | 14.036 | 130 | 16 | 2 | within |
| notice-every-5 | 15.571 | 130 | 16 | 2 | within |
| notice-every-5 | 15.745 | 130 | 16 | 2 | within |
| notice-every-5 | 15.890 | 130 | 16 | 2 | within |
| notice-every-5 | 16.056 | 130 | 16 | 2 | within |
| notice-every-5 | 17.533 | 130 | 16 | 2 | within |
| notice-every-5 | 17.707 | 130 | 16 | 2 | within |
| notice-every-5 | 17.851 | 130 | 16 | 2 | within |
| notice-every-5 | 18.019 | 130 | 16 | 2 | within |
| notice-every-5 | 23.096 | 130 | 16 | 2 | within |
| notice-every-5 | 23.220 | 130 | 16 | 2 | within |
| notice-every-5 | 23.389 | 130 | 16 | 2 | within |
| notice-every-5 | 23.561 | 130 | 16 | 2 | within |
| notice-every-6 | 1.419 | 130 | 16 | 2 | within |
| notice-every-6 | 1.595 | 130 | 16 | 2 | within |
| notice-every-6 | 7.478 | 130 | 16 | 2 | within |
| notice-every-6 | 7.651 | 130 | 16 | 2 | within |
| notice-every-6 | 5.408 | 130 | 16 | 2 | within |
| notice-every-6 | 5.583 | 130 | 16 | 2 | within |
| notice-every-6 | 3.517 | 130 | 16 | 2 | within |
| notice-every-6 | 3.696 | 130 | 16 | 2 | within |
| notice-every-6 | 1.754 | 130 | 16 | 2 | within |
| notice-every-6 | 1.927 | 130 | 16 | 2 | within |
| notice-every-6 | 3.855 | 130 | 16 | 2 | within |
| notice-every-6 | 4.030 | 130 | 16 | 2 | within |
| notice-every-6 | 5.739 | 130 | 16 | 2 | within |
| notice-every-6 | 5.908 | 130 | 16 | 2 | within |
| notice-every-6 | 7.804 | 130 | 16 | 2 | within |
| notice-every-6 | 7.970 | 130 | 16 | 2 | within |
| notice-every-6 | 9.514 | 130 | 16 | 2 | within |
| notice-every-6 | 9.688 | 130 | 16 | 2 | within |
| notice-every-6 | 9.833 | 130 | 16 | 2 | within |
| notice-every-6 | 10.001 | 130 | 16 | 2 | within |
| notice-every-6 | 11.511 | 130 | 16 | 2 | within |
| notice-every-6 | 11.686 | 130 | 16 | 2 | within |
| notice-every-6 | 11.830 | 130 | 16 | 2 | within |
| notice-every-6 | 11.997 | 130 | 16 | 2 | within |
| notice-every-6 | 13.491 | 130 | 16 | 2 | within |
| notice-every-6 | 13.665 | 130 | 16 | 2 | within |
| notice-every-6 | 13.810 | 130 | 16 | 2 | within |
| notice-every-6 | 13.977 | 130 | 16 | 2 | within |
| notice-every-6 | 15.511 | 130 | 16 | 2 | within |
| notice-every-6 | 15.685 | 130 | 16 | 2 | within |
| notice-every-6 | 15.829 | 130 | 16 | 2 | within |
| notice-every-6 | 15.996 | 130 | 16 | 2 | within |
| notice-every-6 | 17.472 | 130 | 16 | 2 | within |
| notice-every-6 | 17.645 | 130 | 16 | 2 | within |
| notice-every-6 | 17.790 | 130 | 16 | 2 | within |
| notice-every-6 | 17.958 | 130 | 16 | 2 | within |
| notice-every-6 | 23.034 | 130 | 16 | 2 | within |
| notice-every-6 | 23.158 | 130 | 16 | 2 | within |
| notice-every-6 | 23.327 | 130 | 16 | 2 | within |
| notice-every-6 | 23.499 | 130 | 16 | 2 | within |
| notice-every-7 | 7.559 | 130 | 16 | 2 | within |
| notice-every-7 | 7.734 | 130 | 16 | 2 | within |
| notice-every-7 | 1.666 | 130 | 16 | 2 | within |
| notice-every-7 | 1.843 | 130 | 16 | 2 | within |
| notice-every-7 | 4.618 | 130 | 16 | 2 | within |
| notice-every-7 | 4.793 | 130 | 16 | 2 | within |
| notice-every-7 | 5.703 | 130 | 16 | 2 | within |
| notice-every-7 | 5.878 | 130 | 16 | 2 | within |
| notice-every-7 | 2.003 | 130 | 16 | 2 | within |
| notice-every-7 | 2.176 | 130 | 16 | 2 | within |
| notice-every-7 | 4.953 | 130 | 16 | 2 | within |
| notice-every-7 | 6.049 | 130 | 16 | 2 | within |
| notice-every-7 | 6.205 | 130 | 16 | 2 | within |
| notice-every-7 | 7.901 | 130 | 16 | 2 | within |
| notice-every-7 | 8.053 | 130 | 16 | 2 | within |
| notice-every-7 | 9.602 | 130 | 16 | 2 | within |
| notice-every-7 | 9.771 | 130 | 16 | 2 | within |
| notice-every-7 | 9.941 | 130 | 16 | 2 | within |
| notice-every-7 | 10.087 | 130 | 16 | 2 | within |
| notice-every-7 | 11.609 | 130 | 16 | 2 | within |
| notice-every-7 | 11.767 | 130 | 16 | 2 | within |
| notice-every-7 | 11.935 | 130 | 16 | 2 | within |
| notice-every-7 | 12.079 | 130 | 16 | 2 | within |
| notice-every-7 | 13.586 | 130 | 16 | 2 | within |
| notice-every-7 | 13.743 | 130 | 16 | 2 | within |
| notice-every-7 | 13.911 | 130 | 16 | 2 | within |
| notice-every-7 | 14.057 | 130 | 16 | 2 | within |
| notice-every-7 | 15.600 | 130 | 16 | 2 | within |
| notice-every-7 | 15.763 | 130 | 16 | 2 | within |
| notice-every-7 | 15.930 | 130 | 16 | 2 | within |
| notice-every-7 | 16.075 | 130 | 16 | 2 | within |
| notice-every-7 | 17.563 | 130 | 16 | 2 | within |
| notice-every-7 | 17.720 | 130 | 16 | 2 | within |
| notice-every-7 | 17.889 | 130 | 16 | 2 | within |
| notice-every-7 | 18.034 | 130 | 16 | 2 | within |
| notice-every-7 | 23.159 | 130 | 16 | 2 | within |
| notice-every-7 | 23.295 | 130 | 16 | 2 | within |
| notice-every-7 | 23.417 | 130 | 16 | 2 | within |
| notice-every-7 | 23.583 | 130 | 16 | 2 | within |
| notice-every-7 | 24.706 | 130 | 16 | 2 | within |
| notice-burst-0 | 6.607 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.778 | 130 | 16 | 1 | within |
| notice-burst-0 | 18.606 | 130 | 16 | 1 | within |
| notice-burst-0 | 18.783 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.110 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.286 | 130 | 16 | 1 | within |
| notice-burst-0 | 18.936 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.103 | 130 | 16 | 1 | within |
| notice-burst-0 | 20.043 | 130 | 16 | 1 | within |
| notice-burst-0 | 20.217 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.021 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.210 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.374 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.553 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.448 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.624 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.942 | 130 | 16 | 1 | within |
| notice-burst-0 | 7.117 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.800 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.987 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.149 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.334 | 130 | 16 | 1 | within |
| notice-burst-0 | 20.362 | 130 | 16 | 1 | within |
| notice-burst-0 | 20.529 | 130 | 16 | 1 | within |
| notice-burst-0 | 22.027 | 130 | 16 | 1 | within |
| notice-burst-0 | 22.201 | 130 | 16 | 1 | within |
| notice-burst-0 | 22.347 | 130 | 16 | 1 | within |
| notice-burst-0 | 22.514 | 130 | 16 | 1 | within |
| notice-burst-0 | 24.003 | 130 | 16 | 1 | within |
| notice-burst-0 | 24.177 | 130 | 16 | 1 | within |
| notice-burst-0 | 24.322 | 130 | 16 | 1 | within |
| notice-burst-0 | 24.489 | 130 | 16 | 1 | within |
| notice-burst-0 | 26.013 | 130 | 16 | 1 | within |
| notice-burst-0 | 26.185 | 130 | 16 | 1 | within |
| notice-burst-0 | 26.331 | 130 | 16 | 1 | within |
| notice-burst-0 | 26.500 | 130 | 16 | 1 | within |
| notice-burst-0 | 28.148 | 130 | 16 | 1 | within |
| notice-burst-0 | 28.272 | 130 | 16 | 1 | within |
| notice-burst-0 | 28.442 | 130 | 16 | 1 | within |
| notice-burst-0 | 28.614 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.851 | 130 | 16 | 0 | within |
| notice-burst-1 | 5.022 | 130 | 16 | 0 | within |
| notice-burst-1 | 16.899 | 130 | 16 | 0 | within |
| notice-burst-1 | 17.076 | 130 | 16 | 0 | within |
| notice-burst-1 | 5.176 | 130 | 16 | 0 | within |
| notice-burst-1 | 5.346 | 130 | 16 | 0 | within |
| notice-burst-1 | 17.230 | 130 | 16 | 0 | within |
| notice-burst-1 | 17.397 | 130 | 16 | 0 | within |
| notice-burst-1 | 18.138 | 130 | 16 | 0 | within |
| notice-burst-1 | 18.312 | 130 | 16 | 0 | within |
| notice-burst-1 | 18.467 | 130 | 16 | 0 | within |
| notice-burst-1 | 18.637 | 130 | 16 | 0 | within |
| notice-burst-1 | 2.798 | 130 | 16 | 0 | within |
| notice-burst-1 | 2.987 | 130 | 16 | 0 | within |
| notice-burst-1 | 3.155 | 130 | 16 | 0 | within |
| notice-burst-1 | 3.336 | 130 | 16 | 0 | within |
| notice-burst-1 | 20.162 | 130 | 16 | 0 | within |
| notice-burst-1 | 20.337 | 130 | 16 | 0 | within |
| notice-burst-1 | 20.483 | 130 | 16 | 0 | within |
| notice-burst-1 | 20.653 | 130 | 16 | 0 | within |
| notice-burst-1 | 4.076 | 130 | 16 | 0 | within |
| notice-burst-1 | 4.266 | 130 | 16 | 0 | within |
| notice-burst-1 | 4.428 | 130 | 16 | 0 | within |
| notice-burst-1 | 4.614 | 130 | 16 | 0 | within |
| notice-burst-1 | 22.152 | 130 | 16 | 0 | within |
| notice-burst-1 | 22.326 | 130 | 16 | 0 | within |
| notice-burst-1 | 22.471 | 130 | 16 | 0 | within |
| notice-burst-1 | 22.638 | 130 | 16 | 0 | within |
| notice-burst-1 | 25.126 | 130 | 16 | 0 | within |
| notice-burst-1 | 25.297 | 130 | 16 | 0 | within |
| notice-burst-1 | 25.444 | 130 | 16 | 0 | within |
| notice-burst-1 | 26.148 | 130 | 16 | 0 | within |
| notice-burst-1 | 26.305 | 130 | 16 | 0 | within |
| notice-burst-1 | 26.473 | 130 | 16 | 0 | within |
| notice-burst-1 | 26.618 | 130 | 16 | 0 | within |
| notice-burst-1 | 28.289 | 130 | 16 | 0 | within |
| notice-burst-1 | 28.428 | 130 | 16 | 0 | within |
| notice-burst-1 | 28.549 | 130 | 16 | 0 | within |
| notice-burst-1 | 28.716 | 130 | 16 | 0 | within |
| notice-burst-1 | 30.170 | 130 | 16 | 0 | within |
| notice-burst-2 | 18.604 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.782 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.800 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.973 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.095 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.269 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.936 | 130 | 16 | 1 | within |
| notice-burst-2 | 19.103 | 130 | 16 | 1 | within |
| notice-burst-2 | 6.598 | 130 | 16 | 1 | within |
| notice-burst-2 | 6.774 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.136 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.317 | 130 | 16 | 1 | within |
| notice-burst-2 | 6.930 | 130 | 16 | 1 | within |
| notice-burst-2 | 7.103 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.243 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.418 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.575 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.743 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.002 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.196 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.364 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.553 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.427 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.608 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.245 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.419 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.564 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.731 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.221 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.394 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.539 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.706 | 130 | 16 | 1 | within |
| notice-burst-2 | 26.230 | 130 | 16 | 1 | within |
| notice-burst-2 | 26.401 | 130 | 16 | 1 | within |
| notice-burst-2 | 26.547 | 130 | 16 | 1 | within |
| notice-burst-2 | 26.716 | 130 | 16 | 1 | within |
| notice-burst-2 | 28.172 | 130 | 16 | 1 | within |
| notice-burst-2 | 28.296 | 130 | 16 | 1 | within |
| notice-burst-2 | 28.467 | 130 | 16 | 1 | within |
| notice-burst-2 | 28.638 | 130 | 16 | 1 | within |
| notice-burst-3 | 1.902 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.077 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.649 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.820 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.232 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.401 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.973 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.141 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.099 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.276 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.431 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.601 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.945 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.119 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.272 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.439 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.965 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.140 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.129 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.316 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.478 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.663 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.285 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.452 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.950 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.124 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.270 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.437 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.926 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.100 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.245 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.412 | 130 | 16 | 1 | within |
| notice-burst-3 | 26.951 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.125 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.270 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.439 | 130 | 16 | 1 | within |
| notice-burst-3 | 28.884 | 130 | 16 | 1 | within |
| notice-burst-3 | 29.009 | 130 | 16 | 1 | within |
| notice-burst-3 | 29.179 | 130 | 16 | 1 | within |
| notice-burst-3 | 29.350 | 130 | 16 | 1 | within |
| notice-burst-4 | 1.859 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.031 | 130 | 16 | 0 | within |
| notice-burst-4 | 3.368 | 130 | 16 | 0 | within |
| notice-burst-4 | 3.539 | 130 | 16 | 0 | within |
| notice-burst-4 | 18.148 | 130 | 16 | 0 | within |
| notice-burst-4 | 18.326 | 130 | 16 | 0 | within |
| notice-burst-4 | 6.167 | 130 | 16 | 0 | within |
| notice-burst-4 | 6.341 | 130 | 16 | 0 | within |
| notice-burst-4 | 6.494 | 130 | 16 | 0 | within |
| notice-burst-4 | 6.664 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.195 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.375 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.669 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.847 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.007 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.181 | 130 | 16 | 0 | within |
| notice-burst-4 | 18.483 | 130 | 16 | 0 | within |
| notice-burst-4 | 18.651 | 130 | 16 | 0 | within |
| notice-burst-4 | 19.783 | 130 | 16 | 0 | within |
| notice-burst-4 | 19.958 | 130 | 16 | 0 | within |
| notice-burst-4 | 3.702 | 130 | 16 | 0 | within |
| notice-burst-4 | 3.886 | 130 | 16 | 0 | within |
| notice-burst-4 | 20.104 | 130 | 16 | 0 | within |
| notice-burst-4 | 20.271 | 130 | 16 | 0 | within |
| notice-burst-4 | 21.765 | 130 | 16 | 0 | within |
| notice-burst-4 | 21.939 | 130 | 16 | 0 | within |
| notice-burst-4 | 22.084 | 130 | 16 | 0 | within |
| notice-burst-4 | 22.251 | 130 | 16 | 0 | within |
| notice-burst-4 | 23.741 | 130 | 16 | 0 | within |
| notice-burst-4 | 23.914 | 130 | 16 | 0 | within |
| notice-burst-4 | 24.059 | 130 | 16 | 0 | within |
| notice-burst-4 | 24.227 | 130 | 16 | 0 | within |
| notice-burst-4 | 25.750 | 130 | 16 | 0 | within |
| notice-burst-4 | 25.921 | 130 | 16 | 0 | within |
| notice-burst-4 | 26.067 | 130 | 16 | 0 | within |
| notice-burst-4 | 26.236 | 130 | 16 | 0 | within |
| notice-burst-4 | 27.692 | 130 | 16 | 0 | within |
| notice-burst-4 | 27.816 | 130 | 16 | 0 | within |
| notice-burst-4 | 27.987 | 130 | 16 | 0 | within |
| notice-burst-4 | 28.158 | 130 | 16 | 0 | within |
| notice-burst-5 | 3.246 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.420 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.111 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.283 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.435 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.602 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.582 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.753 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.520 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.697 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.852 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.022 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.585 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.764 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.910 | 130 | 16 | 1 | within |
| notice-burst-5 | 8.082 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.167 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.342 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.759 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.946 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.108 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.293 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.487 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.654 | 130 | 16 | 1 | within |
| notice-burst-5 | 23.153 | 130 | 16 | 1 | within |
| notice-burst-5 | 23.327 | 130 | 16 | 1 | within |
| notice-burst-5 | 23.473 | 130 | 16 | 1 | within |
| notice-burst-5 | 23.640 | 130 | 16 | 1 | within |
| notice-burst-5 | 25.128 | 130 | 16 | 1 | within |
| notice-burst-5 | 25.301 | 130 | 16 | 1 | within |
| notice-burst-5 | 25.447 | 130 | 16 | 1 | within |
| notice-burst-5 | 25.614 | 130 | 16 | 1 | within |
| notice-burst-5 | 27.135 | 130 | 16 | 1 | within |
| notice-burst-5 | 27.308 | 130 | 16 | 1 | within |
| notice-burst-5 | 27.452 | 130 | 16 | 1 | within |
| notice-burst-5 | 27.621 | 130 | 16 | 1 | within |
| notice-burst-5 | 29.261 | 130 | 16 | 1 | within |
| notice-burst-5 | 29.385 | 130 | 16 | 1 | within |
| notice-burst-5 | 29.556 | 130 | 16 | 1 | within |
| notice-burst-5 | 29.727 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.893 | 130 | 16 | 0 | within |
| notice-burst-6 | 4.066 | 130 | 16 | 0 | within |
| notice-burst-6 | 5.388 | 130 | 16 | 0 | within |
| notice-burst-6 | 5.559 | 130 | 16 | 0 | within |
| notice-burst-6 | 17.357 | 130 | 16 | 0 | within |
| notice-burst-6 | 17.535 | 130 | 16 | 0 | within |
| notice-burst-6 | 5.713 | 130 | 16 | 0 | within |
| notice-burst-6 | 5.884 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.427 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.606 | 130 | 16 | 0 | within |
| notice-burst-6 | 17.690 | 130 | 16 | 0 | within |
| notice-burst-6 | 17.860 | 130 | 16 | 0 | within |
| notice-burst-6 | 1.631 | 130 | 16 | 0 | within |
| notice-burst-6 | 1.817 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.393 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.568 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.777 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.959 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.714 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.883 | 130 | 16 | 0 | within |
| notice-burst-6 | 1.985 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.174 | 130 | 16 | 0 | within |
| notice-burst-6 | 4.223 | 130 | 16 | 0 | within |
| notice-burst-6 | 4.405 | 130 | 16 | 0 | within |
| notice-burst-6 | 20.391 | 130 | 16 | 0 | within |
| notice-burst-6 | 20.565 | 130 | 16 | 0 | within |
| notice-burst-6 | 20.711 | 130 | 16 | 0 | within |
| notice-burst-6 | 20.878 | 130 | 16 | 0 | within |
| notice-burst-6 | 22.367 | 130 | 16 | 0 | within |
| notice-burst-6 | 22.540 | 130 | 16 | 0 | within |
| notice-burst-6 | 22.686 | 130 | 16 | 0 | within |
| notice-burst-6 | 22.853 | 130 | 16 | 0 | within |
| notice-burst-6 | 24.523 | 130 | 16 | 0 | within |
| notice-burst-6 | 24.696 | 130 | 16 | 0 | within |
| notice-burst-6 | 24.840 | 130 | 16 | 0 | within |
| notice-burst-6 | 25.009 | 130 | 16 | 0 | within |
| notice-burst-6 | 26.518 | 130 | 16 | 0 | within |
| notice-burst-6 | 26.643 | 130 | 16 | 0 | within |
| notice-burst-6 | 26.814 | 130 | 16 | 0 | within |
| notice-burst-6 | 26.985 | 130 | 16 | 0 | within |
| notice-burst-7 | 4.446 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.617 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.724 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.901 | 130 | 16 | 1 | within |
| notice-burst-7 | 1.631 | 130 | 16 | 1 | within |
| notice-burst-7 | 1.808 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.054 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.221 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.932 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.112 | 130 | 16 | 1 | within |
| notice-burst-7 | 18.366 | 130 | 16 | 1 | within |
| notice-burst-7 | 18.543 | 130 | 16 | 1 | within |
| notice-burst-7 | 1.974 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.154 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.776 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.951 | 130 | 16 | 1 | within |
| notice-burst-7 | 18.700 | 130 | 16 | 1 | within |
| notice-burst-7 | 18.868 | 130 | 16 | 1 | within |
| notice-burst-7 | 20.379 | 130 | 16 | 1 | within |
| notice-burst-7 | 20.555 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.274 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.458 | 130 | 16 | 1 | within |
| notice-burst-7 | 20.700 | 130 | 16 | 1 | within |
| notice-burst-7 | 20.868 | 130 | 16 | 1 | within |
| notice-burst-7 | 22.362 | 130 | 16 | 1 | within |
| notice-burst-7 | 22.536 | 130 | 16 | 1 | within |
| notice-burst-7 | 22.681 | 130 | 16 | 1 | within |
| notice-burst-7 | 22.849 | 130 | 16 | 1 | within |
| notice-burst-7 | 24.338 | 130 | 16 | 1 | within |
| notice-burst-7 | 24.511 | 130 | 16 | 1 | within |
| notice-burst-7 | 24.656 | 130 | 16 | 1 | within |
| notice-burst-7 | 24.824 | 130 | 16 | 1 | within |
| notice-burst-7 | 26.361 | 130 | 16 | 1 | within |
| notice-burst-7 | 26.535 | 130 | 16 | 1 | within |
| notice-burst-7 | 26.681 | 130 | 16 | 1 | within |
| notice-burst-7 | 26.849 | 130 | 16 | 1 | within |
| notice-burst-7 | 28.295 | 130 | 16 | 1 | within |
| notice-burst-7 | 28.420 | 130 | 16 | 1 | within |
| notice-burst-7 | 28.590 | 130 | 16 | 1 | within |
| notice-burst-7 | 28.761 | 130 | 16 | 1 | within |

Latest: 30.170 ms, notice-burst-1.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 660 | 122,700 (1.227) | 78,591 (0.786) |
| notice-every-1 | 660 | 122,779 (1.228) | 78,591 (0.786) |
| notice-every-2 | 661 | 122,927 (1.229) | 78,591 (0.786) |
| notice-every-3 | 661 | 122,970 (1.230) | 78,591 (0.786) |
| notice-every-4 | 661 | 115,682 (1.157) | 78,591 (0.786) |
| notice-every-5 | 667 | 122,795 (1.228) | 78,591 (0.786) |
| notice-every-6 | 667 | 122,988 (1.230) | 78,591 (0.786) |
| notice-every-7 | 667 | 136,538 (1.365) | 78,591 (0.786) |
| notice-burst-0 | 780 | 171,296 (1.713) | 78,591 (0.786) |
| notice-burst-1 | 780 | 131,146 (1.311) | 78,591 (0.786) |
| notice-burst-2 | 779 | 171,211 (1.712) | 78,591 (0.786) |
| notice-burst-3 | 780 | 173,858 (1.739) | 78,591 (0.786) |
| notice-burst-4 | 781 | 172,515 (1.725) | 78,591 (0.786) |
| notice-burst-5 | 783 | 172,588 (1.726) | 78,591 (0.786) |
| notice-burst-6 | 781 | 170,180 (1.702) | 78,591 (0.786) |
| notice-burst-7 | 781 | 173,442 (1.734) | 78,591 (0.786) |

Longest pass that carries a step: 173,858 CPU cycles (1.739 ms), notice-burst-3; longest step: 78,591 (0.786 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 777,297 | 7.773 | 130 | 134 | fits | 73,310 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 794,829 | 7.948 | 130 | 134 | fits | 73,310 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 166,996 | 1.670 | 130 | 134 | fits | 76,826 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 184,704 | 1.847 | 130 | 134 | fits | 76,826 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 355,623 | 3.556 | 130 | 134 | fits | 76,168 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 373,307 | 3.733 | 130 | 134 | fits | 76,168 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 567,461 | 5.675 | 130 | 134 | fits | 76,015 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 585,227 | 5.852 | 130 | 134 | fits | 76,015 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 200,680 | 2.007 | 130 | 134 | fits | 76,826 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 218,019 | 2.180 | 130 | 134 | fits | 76,826 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 389,243 | 3.892 | 130 | 134 | fits | 76,168 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 406,749 | 4.067 | 130 | 134 | fits | 76,168 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 600,815 | 6.008 | 130 | 134 | fits | 76,015 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 617,771 | 6.178 | 130 | 134 | fits | 76,015 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 810,056 | 8.101 | 130 | 134 | fits | 73,310 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 826,702 | 8.267 | 130 | 134 | fits | 73,310 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 960,122 | 9.601 | 130 | 134 | fits | 73,123 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 977,654 | 9.777 | 130 | 134 | fits | 73,123 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 992,183 | 9.922 | 130 | 134 | fits | 73,123 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,008,908 | 10.089 | 130 | 134 | fits | 73,123 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,160,061 | 11.601 | 130 | 134 | fits | 71,450 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,177,597 | 11.776 | 130 | 134 | fits | 71,450 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,192,061 | 11.921 | 130 | 134 | fits | 71,450 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,208,707 | 12.087 | 130 | 134 | fits | 71,450 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,358,129 | 13.581 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,375,604 | 13.756 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,390,133 | 13.901 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,406,779 | 14.068 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,560,276 | 15.603 | 130 | 134 | fits | 71,864 | 203 | 0.165 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,577,672 | 15.777 | 130 | 134 | fits | 71,864 | 203 | 0.165 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,592,166 | 15.922 | 130 | 134 | fits | 71,864 | 203 | 0.165 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,608,812 | 16.088 | 130 | 134 | fits | 71,864 | 203 | 0.165 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,756,351 | 17.564 | 130 | 134 | fits | 70,913 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,773,747 | 17.737 | 130 | 134 | fits | 70,913 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,788,211 | 17.882 | 130 | 134 | fits | 70,913 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,805,015 | 18.050 | 130 | 134 | fits | 70,913 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,312,710 | 23.127 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,325,104 | 23.251 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,342,043 | 23.420 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,359,227 | 23.592 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 726,134 | 7.261 | 20 | 200 | fits | 152,576 | 212 | 0.281 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 867,029 | 8.670 | 20 | 20 | fits | 139,091 | 77 | 0.692 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 533,577 | 5.336 | 20 | 24 | fits | 120,347 | 61 | 0.501 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 666,391 | 6.664 | 20 | 50 | fits | 152,576 | 212 | 0.281 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,193,434 | 11.934 | 20 | 20 | fits | 92,546 | 39 | 0.721 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 86,110 | 0.861 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 752,331 | 7.523 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 769,774 | 7.698 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 146,062 | 1.461 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 163,770 | 1.638 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 355,633 | 3.556 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 373,317 | 3.733 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 545,154 | 5.452 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 562,710 | 5.627 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 179,746 | 1.797 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 197,085 | 1.971 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 389,253 | 3.893 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 406,759 | 4.068 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 578,379 | 5.784 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 595,335 | 5.953 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 785,003 | 7.850 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 801,649 | 8.016 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 956,159 | 9.562 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 973,602 | 9.736 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 988,129 | 9.881 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 1,004,854 | 10.049 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 1,155,992 | 11.560 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 1,173,439 | 11.734 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 1,187,903 | 11.879 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 1,204,549 | 12.045 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 1,353,984 | 13.540 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 1,371,370 | 13.714 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 1,385,899 | 13.859 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 1,402,545 | 14.025 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 1,556,024 | 15.560 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 1,573,331 | 15.733 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 1,587,825 | 15.878 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 1,604,471 | 16.045 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 1,752,107 | 17.521 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 1,769,414 | 17.694 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 1,783,878 | 17.839 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 1,800,682 | 18.007 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 2,308,318 | 23.083 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 2,320,712 | 23.207 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 2,337,651 | 23.377 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 2,354,835 | 23.548 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 165,912 | 1.659 | 20 | 200 | fits | 157,045 | 213 | 0.287 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 842,159 | 8.422 | 20 | 20 | fits | 137,635 | 91 | 0.678 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 665,558 | 6.656 | 20 | 24 | fits | 156,788 | 113 | 0.514 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 802,684 | 8.027 | 20 | 50 | fits | 137,635 | 91 | 0.678 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,186,081 | 11.861 | 20 | 20 | fits | 104,591 | 49 | 0.706 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 92,357 | 0.924 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 752,179 | 7.522 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 769,622 | 7.696 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 146,025 | 1.460 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 163,733 | 1.637 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 355,583 | 3.556 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 373,267 | 3.733 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 544,862 | 5.449 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 562,418 | 5.624 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 179,709 | 1.797 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 197,048 | 1.970 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 389,203 | 3.892 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 406,709 | 4.067 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 578,087 | 5.781 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 595,043 | 5.950 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 784,851 | 7.849 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 801,497 | 8.015 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 956,104 | 9.561 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 973,547 | 9.735 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 988,074 | 9.881 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 1,004,799 | 10.048 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 1,155,858 | 11.559 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 1,173,305 | 11.733 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 1,187,769 | 11.878 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 1,204,415 | 12.044 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 1,353,837 | 13.538 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 1,371,223 | 13.712 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 1,385,752 | 13.858 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 1,402,398 | 14.024 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 1,555,890 | 15.559 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 1,573,197 | 15.732 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 1,587,691 | 15.877 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 1,604,337 | 16.043 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 1,751,955 | 17.520 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 1,769,262 | 17.693 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 1,783,726 | 17.837 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 1,800,530 | 18.005 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 2,308,051 | 23.081 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 2,320,445 | 23.204 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 2,337,384 | 23.374 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 2,354,568 | 23.546 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 804,834 | 8.048 | 20 | 200 | fits | 152,412 | 210 | 0.281 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 940,554 | 9.406 | 20 | 20 | fits | 137,559 | 73 | 0.693 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 593,674 | 5.937 | 20 | 24 | fits | 159,653 | 127 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 745,091 | 7.451 | 20 | 50 | fits | 152,412 | 210 | 0.281 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,273,414 | 12.734 | 20 | 20 | fits | 93,818 | 45 | 0.712 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 101,030 | 1.010 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 752,146 | 7.521 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 769,589 | 7.696 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 146,025 | 1.460 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 163,733 | 1.637 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 355,583 | 3.556 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 373,267 | 3.733 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 544,829 | 5.448 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 562,385 | 5.624 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 179,709 | 1.797 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 197,048 | 1.970 | 130 | 134 | fits | 76,963 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 389,203 | 3.892 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 406,709 | 4.067 | 130 | 134 | fits | 76,031 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 578,054 | 5.781 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 595,010 | 5.950 | 130 | 134 | fits | 77,608 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 784,818 | 7.848 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 801,464 | 8.015 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 956,071 | 9.561 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 973,514 | 9.735 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 988,041 | 9.880 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 1,004,766 | 10.048 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 1,155,825 | 11.558 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 1,173,272 | 11.733 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 1,187,736 | 11.877 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 1,204,382 | 12.044 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 1,353,804 | 13.538 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 1,371,190 | 13.712 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 1,385,719 | 13.857 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 1,402,365 | 14.024 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 1,555,857 | 15.559 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 1,573,164 | 15.732 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 1,587,658 | 15.877 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 1,604,304 | 16.043 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 1,751,922 | 17.519 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 1,769,229 | 17.692 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 1,783,693 | 17.837 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 1,800,497 | 18.005 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 2,307,958 | 23.080 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 2,320,352 | 23.204 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 2,337,291 | 23.373 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 2,354,475 | 23.545 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 719,495 | 7.195 | 20 | 200 | fits | 152,398 | 211 | 0.274 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 855,797 | 8.558 | 20 | 20 | fits | 137,790 | 71 | 0.695 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 529,027 | 5.290 | 20 | 24 | fits | 127,149 | 67 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 659,752 | 6.598 | 20 | 50 | fits | 152,398 | 211 | 0.274 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,186,249 | 11.862 | 20 | 20 | fits | 92,677 | 39 | 0.721 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 91,641 | 0.916 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 752,300 | 7.523 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 769,743 | 7.697 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 146,067 | 1.461 | 130 | 134 | fits | 76,895 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 163,775 | 1.638 | 130 | 134 | fits | 76,895 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 545,007 | 5.450 | 130 | 134 | fits | 77,347 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 562,563 | 5.626 | 130 | 134 | fits | 77,347 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 355,954 | 3.560 | 130 | 134 | fits | 76,551 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 373,869 | 3.739 | 130 | 134 | fits | 76,551 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 179,672 | 1.797 | 130 | 134 | fits | 76,895 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 197,011 | 1.970 | 130 | 134 | fits | 76,895 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 389,784 | 3.898 | 130 | 134 | fits | 76,551 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 407,290 | 4.073 | 130 | 134 | fits | 76,551 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 578,208 | 5.782 | 130 | 134 | fits | 77,347 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 595,164 | 5.952 | 130 | 134 | fits | 77,347 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 784,972 | 7.850 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 801,618 | 8.016 | 130 | 134 | fits | 73,294 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 956,220 | 9.562 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 973,663 | 9.737 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 988,190 | 9.882 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 1,004,915 | 10.049 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 1,156,053 | 11.561 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 1,173,500 | 11.735 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 1,187,964 | 11.880 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 1,204,610 | 12.046 | 130 | 134 | fits | 71,361 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 1,354,050 | 13.540 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 1,371,436 | 13.714 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 1,385,965 | 13.860 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 1,402,611 | 14.026 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 1,556,011 | 15.560 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 1,573,318 | 15.733 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 1,587,812 | 15.878 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 1,604,458 | 16.045 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 1,752,076 | 17.521 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 1,769,383 | 17.694 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 1,783,847 | 17.838 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 1,800,651 | 18.007 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 2,308,418 | 23.084 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 2,320,812 | 23.208 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 2,337,751 | 23.378 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 2,354,935 | 23.549 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 697,055 | 6.971 | 20 | 200 | fits | 158,982 | 122 | 0.505 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 811,622 | 8.116 | 20 | 20 | fits | 134,835 | 70 | 0.654 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 656,583 | 6.566 | 20 | 24 | fits | 158,982 | 122 | 0.505 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 637,312 | 6.373 | 20 | 50 | fits | 158,982 | 122 | 0.505 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,176,127 | 11.761 | 20 | 20 | fits | 108,366 | 55 | 0.728 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 99,131 | 0.991 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 752,875 | 7.529 | 130 | 134 | fits | 73,447 | 205 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 770,407 | 7.704 | 130 | 134 | fits | 73,447 | 205 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 167,031 | 1.670 | 130 | 134 | fits | 76,837 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 184,739 | 1.847 | 130 | 134 | fits | 76,837 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 567,665 | 5.677 | 130 | 134 | fits | 75,754 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 585,431 | 5.854 | 130 | 134 | fits | 75,754 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 356,029 | 3.560 | 130 | 134 | fits | 76,688 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 373,944 | 3.739 | 130 | 134 | fits | 76,688 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 200,715 | 2.007 | 130 | 134 | fits | 76,837 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 218,054 | 2.181 | 130 | 134 | fits | 76,837 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 389,859 | 3.899 | 130 | 134 | fits | 76,688 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 407,365 | 4.074 | 130 | 134 | fits | 76,688 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 600,995 | 6.010 | 130 | 134 | fits | 75,754 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 617,951 | 6.180 | 130 | 134 | fits | 75,754 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 785,634 | 7.856 | 130 | 134 | fits | 73,447 | 205 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 802,280 | 8.023 | 130 | 134 | fits | 73,447 | 205 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 957,025 | 9.570 | 130 | 134 | fits | 73,183 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 974,557 | 9.746 | 130 | 134 | fits | 73,183 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 989,084 | 9.891 | 130 | 134 | fits | 73,183 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 1,005,809 | 10.058 | 130 | 134 | fits | 73,183 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 1,156,903 | 11.569 | 130 | 134 | fits | 71,450 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 1,174,439 | 11.744 | 130 | 134 | fits | 71,450 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 1,188,903 | 11.889 | 130 | 134 | fits | 71,450 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 1,205,549 | 12.055 | 130 | 134 | fits | 71,450 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 1,354,971 | 13.550 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 1,372,446 | 13.724 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 1,386,975 | 13.870 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 1,403,621 | 14.036 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 1,557,113 | 15.571 | 130 | 134 | fits | 71,864 | 203 | 0.165 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 1,574,509 | 15.745 | 130 | 134 | fits | 71,864 | 203 | 0.165 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 1,589,003 | 15.890 | 130 | 134 | fits | 71,864 | 203 | 0.165 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 1,605,649 | 16.056 | 130 | 134 | fits | 71,864 | 203 | 0.165 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 1,753,267 | 17.533 | 130 | 134 | fits | 70,913 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 1,770,663 | 17.707 | 130 | 134 | fits | 70,913 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 1,785,127 | 17.851 | 130 | 134 | fits | 70,913 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 1,801,931 | 18.019 | 130 | 134 | fits | 70,913 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 2,309,570 | 23.096 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 2,321,964 | 23.220 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 2,338,903 | 23.389 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 2,356,087 | 23.561 | 130 | 134 | fits | 66,850 | 202 | 0.144 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 794,694 | 7.947 | 20 | 200 | fits | 153,142 | 211 | 0.284 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 909,696 | 9.097 | 20 | 20 | fits | 135,270 | 65 | 0.685 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 582,529 | 5.825 | 20 | 24 | fits | 160,196 | 127 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 734,951 | 7.350 | 20 | 50 | fits | 153,142 | 211 | 0.284 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,263,496 | 12.635 | 20 | 20 | fits | 97,651 | 51 | 0.736 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 84,359 | 0.844 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 141,927 | 1.419 | 130 | 134 | fits | 76,828 | 205 | 0.179 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 159,483 | 1.595 | 130 | 134 | fits | 76,828 | 205 | 0.179 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 747,769 | 7.478 | 130 | 134 | fits | 72,925 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 765,133 | 7.651 | 130 | 134 | fits | 72,925 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 540,754 | 5.408 | 130 | 134 | fits | 77,381 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 558,310 | 5.583 | 130 | 134 | fits | 77,381 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 351,714 | 3.517 | 130 | 134 | fits | 76,554 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 369,629 | 3.696 | 130 | 134 | fits | 76,554 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 175,364 | 1.754 | 130 | 134 | fits | 76,828 | 205 | 0.179 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 192,703 | 1.927 | 130 | 134 | fits | 76,828 | 205 | 0.179 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 385,544 | 3.855 | 130 | 134 | fits | 76,554 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 403,050 | 4.030 | 130 | 134 | fits | 76,554 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 573,876 | 5.739 | 130 | 134 | fits | 77,381 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 590,832 | 5.908 | 130 | 134 | fits | 77,381 | 210 | 0.177 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 780,362 | 7.804 | 130 | 134 | fits | 72,925 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 797,008 | 7.970 | 130 | 134 | fits | 72,925 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 951,359 | 9.514 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 968,802 | 9.688 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 983,329 | 9.833 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,000,054 | 10.001 | 130 | 134 | fits | 73,032 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,151,113 | 11.511 | 130 | 134 | fits | 71,282 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,168,560 | 11.686 | 130 | 134 | fits | 71,282 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,183,024 | 11.830 | 130 | 134 | fits | 71,282 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,199,670 | 11.997 | 130 | 134 | fits | 71,282 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,349,105 | 13.491 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,366,491 | 13.665 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,381,020 | 13.810 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,397,666 | 13.977 | 130 | 134 | fits | 70,996 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,551,145 | 15.511 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,568,452 | 15.685 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,582,946 | 15.829 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,599,592 | 15.996 | 130 | 134 | fits | 71,775 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,747,228 | 17.472 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,764,535 | 17.645 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,778,999 | 17.790 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,795,803 | 17.958 | 130 | 134 | fits | 70,824 | 203 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,303,389 | 23.034 | 130 | 134 | fits | 66,801 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,315,783 | 23.158 | 130 | 134 | fits | 66,801 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,332,722 | 23.327 | 130 | 134 | fits | 66,801 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,349,906 | 23.499 | 130 | 134 | fits | 66,801 | 202 | 0.143 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 738,460 | 7.385 | 20 | 200 | fits | 150,198 | 208 | 0.233 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 880,081 | 8.801 | 20 | 20 | fits | 139,335 | 77 | 0.694 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 530,193 | 5.302 | 20 | 24 | fits | 107,395 | 51 | 0.483 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 678,717 | 6.787 | 20 | 50 | fits | 150,198 | 208 | 0.233 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,232,520 | 12.325 | 20 | 20 | fits | 101,985 | 56 | 0.738 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 118,444 | 1.184 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 755,906 | 7.559 | 130 | 134 | fits | 73,603 | 205 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 773,355 | 7.734 | 130 | 134 | fits | 73,603 | 205 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 166,625 | 1.666 | 130 | 134 | fits | 76,826 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 184,333 | 1.843 | 130 | 134 | fits | 76,826 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 461,771 | 4.618 | 130 | 134 | fits | 136,538 | 153 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 479,327 | 4.793 | 130 | 134 | fits | 136,538 | 153 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 570,270 | 5.703 | 130 | 134 | fits | 75,182 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 587,756 | 5.878 | 130 | 134 | fits | 75,182 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 200,309 | 2.003 | 130 | 134 | fits | 76,826 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 217,648 | 2.176 | 130 | 134 | fits | 76,826 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 495,252 | 4.953 | 130 | 134 | fits | 136,538 | 153 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 604,941 | 6.049 | 130 | 134 | fits | 75,182 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 620,547 | 6.205 | 130 | 134 | fits | 75,182 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 790,069 | 7.901 | 130 | 134 | fits | 73,603 | 205 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 805,296 | 8.053 | 130 | 134 | fits | 73,603 | 205 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 960,180 | 9.602 | 130 | 134 | fits | 72,510 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 977,141 | 9.771 | 130 | 134 | fits | 72,510 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 994,084 | 9.941 | 130 | 134 | fits | 72,510 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 1,008,652 | 10.087 | 130 | 134 | fits | 72,510 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 1,160,882 | 11.609 | 130 | 134 | fits | 70,555 | 203 | 0.156 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 1,176,715 | 11.767 | 130 | 134 | fits | 70,555 | 203 | 0.156 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 1,193,513 | 11.935 | 130 | 134 | fits | 70,555 | 203 | 0.156 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 1,207,949 | 12.079 | 130 | 134 | fits | 70,555 | 203 | 0.156 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 1,358,577 | 13.586 | 130 | 134 | fits | 70,393 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 1,374,266 | 13.743 | 130 | 134 | fits | 70,393 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 1,391,130 | 13.911 | 130 | 134 | fits | 70,393 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 1,405,707 | 14.057 | 130 | 134 | fits | 70,393 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 1,559,992 | 15.600 | 130 | 134 | fits | 71,217 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 1,576,288 | 15.763 | 130 | 134 | fits | 71,217 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 1,593,007 | 15.930 | 130 | 134 | fits | 71,217 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 1,607,508 | 16.075 | 130 | 134 | fits | 71,217 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 1,756,347 | 17.563 | 130 | 134 | fits | 70,036 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 1,772,036 | 17.720 | 130 | 134 | fits | 70,036 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 1,788,900 | 17.889 | 130 | 134 | fits | 70,036 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 1,803,412 | 18.034 | 130 | 134 | fits | 70,036 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 2,315,852 | 23.159 | 130 | 134 | fits | 66,049 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 2,329,530 | 23.295 | 130 | 134 | fits | 66,049 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 2,341,749 | 23.417 | 130 | 134 | fits | 66,049 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 2,358,298 | 23.583 | 130 | 134 | fits | 66,049 | 202 | 0.144 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 2,470,636 | 24.706 | 130 | 134 | fits | 23,303 | 53 | 0.283 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 173,899 | 1.739 | 20 | 200 | fits | 155,208 | 222 | 0.289 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 817,546 | 8.175 | 20 | 20 | fits | 141,431 | 85 | 0.646 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 655,911 | 6.559 | 20 | 24 | fits | 156,954 | 115 | 0.518 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 636,640 | 6.366 | 20 | 50 | fits | 156,954 | 115 | 0.518 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,179,945 | 11.799 | 20 | 20 | fits | 103,562 | 45 | 0.712 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 83,966 | 0.840 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 660,677 | 6.607 | 130 | 134 | fits | 73,086 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 677,845 | 6.778 | 130 | 134 | fits | 73,086 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,860,560 | 18.606 | 130 | 134 | fits | 76,007 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,878,292 | 18.783 | 130 | 134 | fits | 76,007 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 510,961 | 5.110 | 130 | 134 | fits | 171,296 | 213 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 528,593 | 5.286 | 130 | 134 | fits | 171,296 | 213 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 1,893,624 | 18.936 | 130 | 134 | fits | 76,007 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 1,910,343 | 19.103 | 130 | 134 | fits | 76,007 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 2,004,250 | 20.043 | 130 | 134 | fits | 72,356 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 2,021,709 | 20.217 | 130 | 134 | fits | 72,356 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 302,133 | 3.021 | 130 | 134 | fits | 101,138 | 213 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 320,958 | 3.210 | 130 | 134 | fits | 101,138 | 213 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 337,392 | 3.374 | 130 | 134 | fits | 101,138 | 213 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 355,345 | 3.553 | 130 | 134 | fits | 101,138 | 213 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 544,753 | 5.448 | 130 | 134 | fits | 171,296 | 213 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 562,396 | 5.624 | 130 | 134 | fits | 171,296 | 213 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 694,204 | 6.942 | 130 | 134 | fits | 73,086 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 711,750 | 7.117 | 130 | 134 | fits | 73,086 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 380,022 | 3.800 | 130 | 134 | fits | 76,336 | 203 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 398,704 | 3.987 | 130 | 134 | fits | 76,336 | 203 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 414,918 | 4.149 | 130 | 134 | fits | 76,336 | 203 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 433,388 | 4.334 | 130 | 134 | fits | 76,336 | 203 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 2,036,173 | 20.362 | 130 | 134 | fits | 72,356 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 2,052,892 | 20.529 | 130 | 134 | fits | 72,356 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 2,202,745 | 22.027 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 2,220,147 | 22.201 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 2,234,676 | 22.347 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 2,251,395 | 22.514 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 2,400,331 | 24.003 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 2,417,654 | 24.177 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,432,183 | 24.322 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,448,902 | 24.489 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,601,334 | 26.013 | 130 | 134 | fits | 73,405 | 208 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,618,504 | 26.185 | 130 | 134 | fits | 73,405 | 208 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 2,633,087 | 26.331 | 130 | 134 | fits | 73,405 | 208 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 2,649,964 | 26.500 | 130 | 134 | fits | 73,405 | 208 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 2,814,784 | 28.148 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,827,204 | 28.272 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,844,244 | 28.442 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 2,861,355 | 28.614 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 769,372 | 7.694 | 20 | 200 | fits | 150,786 | 207 | 0.198 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 883,491 | 8.835 | 20 | 20 | fits | 134,387 | 59 | 0.716 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 578,114 | 5.781 | 20 | 24 | fits | 153,686 | 114 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 709,629 | 7.096 | 20 | 50 | fits | 150,786 | 207 | 0.198 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 1,174,952 | 11.750 | 20 | 20 | fits | 90,953 | 38 | 0.717 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 485,105 | 4.851 | 130 | 134 | fits | 71,576 | 205 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 502,191 | 5.022 | 130 | 134 | fits | 71,576 | 205 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,689,862 | 16.899 | 130 | 134 | fits | 76,055 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,707,594 | 17.076 | 130 | 134 | fits | 76,055 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 517,575 | 5.176 | 130 | 134 | fits | 71,576 | 205 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 534,580 | 5.346 | 130 | 134 | fits | 71,576 | 205 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 1,722,961 | 17.230 | 130 | 134 | fits | 76,055 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 1,739,680 | 17.397 | 130 | 134 | fits | 76,055 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 1,813,833 | 18.138 | 130 | 134 | fits | 73,788 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 1,831,213 | 18.312 | 130 | 134 | fits | 73,788 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 1,846,677 | 18.467 | 130 | 134 | fits | 73,788 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 1,863,715 | 18.637 | 130 | 134 | fits | 73,788 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 279,835 | 2.798 | 130 | 134 | fits | 80,654 | 205 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 298,729 | 2.987 | 130 | 134 | fits | 80,654 | 205 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 315,488 | 3.155 | 130 | 134 | fits | 80,654 | 205 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 333,648 | 3.336 | 130 | 134 | fits | 80,654 | 205 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 2,016,180 | 20.162 | 130 | 134 | fits | 73,274 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 2,033,718 | 20.337 | 130 | 134 | fits | 73,274 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 2,048,321 | 20.483 | 130 | 134 | fits | 73,274 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 2,065,263 | 20.653 | 130 | 134 | fits | 73,274 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 407,638 | 4.076 | 130 | 134 | fits | 100,842 | 211 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 426,609 | 4.266 | 130 | 134 | fits | 100,842 | 211 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 442,840 | 4.428 | 130 | 134 | fits | 100,842 | 211 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 461,407 | 4.614 | 130 | 134 | fits | 100,842 | 211 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 2,215,192 | 22.152 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 2,232,594 | 22.326 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 2,247,123 | 22.471 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 2,263,842 | 22.638 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 2,512,604 | 25.126 | 130 | 134 | fits | 131,146 | 152 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 2,529,717 | 25.297 | 130 | 134 | fits | 131,146 | 152 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 2,544,365 | 25.444 | 130 | 134 | fits | 131,146 | 152 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 2,614,835 | 26.148 | 130 | 134 | fits | 70,105 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,630,526 | 26.305 | 130 | 134 | fits | 70,105 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 2,647,317 | 26.473 | 130 | 134 | fits | 70,105 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 2,661,831 | 26.618 | 130 | 134 | fits | 70,105 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 2,828,885 | 28.289 | 130 | 134 | fits | 65,772 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 2,842,785 | 28.428 | 130 | 134 | fits | 65,772 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 2,854,931 | 28.549 | 130 | 134 | fits | 65,772 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 2,871,553 | 28.716 | 130 | 134 | fits | 65,772 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 3,017,035 | 30.170 | 130 | 134 | fits | 22,740 | 52 | 0.263 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 684,189 | 6.842 | 20 | 200 | fits | 151,529 | 212 | 0.195 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 798,811 | 7.988 | 20 | 20 | fits | 134,890 | 59 | 0.716 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 492,188 | 4.922 | 20 | 24 | fits | 155,672 | 122 | 0.476 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 624,446 | 6.244 | 20 | 50 | fits | 151,529 | 212 | 0.195 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,090,549 | 10.905 | 20 | 20 | fits | 80,263 | 34 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 1,860,378 | 18.604 | 130 | 134 | fits | 76,268 | 203 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,878,195 | 18.782 | 130 | 134 | fits | 76,268 | 203 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 379,962 | 3.800 | 130 | 134 | fits | 74,588 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 397,256 | 3.973 | 130 | 134 | fits | 74,588 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 509,500 | 5.095 | 130 | 134 | fits | 171,211 | 211 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 526,901 | 5.269 | 130 | 134 | fits | 171,211 | 211 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 1,893,562 | 18.936 | 130 | 134 | fits | 76,268 | 203 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 1,910,281 | 19.103 | 130 | 134 | fits | 76,268 | 203 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 659,825 | 6.598 | 130 | 134 | fits | 73,266 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 677,376 | 6.774 | 130 | 134 | fits | 73,266 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 413,607 | 4.136 | 130 | 134 | fits | 74,588 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 431,703 | 4.317 | 130 | 134 | fits | 74,588 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 692,955 | 6.930 | 130 | 134 | fits | 73,266 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 710,270 | 7.103 | 130 | 134 | fits | 73,266 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 2,024,291 | 20.243 | 130 | 134 | fits | 73,720 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 2,041,750 | 20.418 | 130 | 134 | fits | 73,720 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 2,057,501 | 20.575 | 130 | 134 | fits | 73,720 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 2,074,299 | 20.743 | 130 | 134 | fits | 73,720 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 300,183 | 3.002 | 130 | 134 | fits | 104,073 | 211 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 319,624 | 3.196 | 130 | 134 | fits | 104,073 | 211 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 336,435 | 3.364 | 130 | 134 | fits | 104,073 | 211 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 355,312 | 3.553 | 130 | 134 | fits | 104,073 | 211 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 542,670 | 5.427 | 130 | 134 | fits | 171,211 | 211 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 560,775 | 5.608 | 130 | 134 | fits | 171,211 | 211 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 2,224,477 | 22.245 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 2,241,879 | 22.419 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 2,256,408 | 22.564 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 2,273,127 | 22.731 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 2,422,050 | 24.221 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 2,439,373 | 24.394 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 2,453,902 | 24.539 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 2,470,621 | 24.706 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 2,622,979 | 26.230 | 130 | 134 | fits | 73,405 | 208 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 2,640,149 | 26.401 | 130 | 134 | fits | 73,405 | 208 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 2,654,732 | 26.547 | 130 | 134 | fits | 73,405 | 208 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 2,671,609 | 26.716 | 130 | 134 | fits | 73,405 | 208 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 2,817,216 | 28.172 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,829,636 | 28.296 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,846,676 | 28.467 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 2,863,787 | 28.638 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 756,344 | 7.563 | 20 | 200 | fits | 150,519 | 207 | 0.192 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 870,864 | 8.709 | 20 | 20 | fits | 134,788 | 59 | 0.716 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 565,353 | 5.654 | 20 | 24 | fits | 154,834 | 120 | 0.477 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 696,601 | 6.966 | 20 | 50 | fits | 150,519 | 207 | 0.192 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,162,167 | 11.622 | 20 | 20 | fits | 80,105 | 34 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 190,215 | 1.902 | 130 | 134 | fits | 76,648 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 207,698 | 2.077 | 130 | 134 | fits | 76,648 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 464,938 | 4.649 | 130 | 134 | fits | 71,853 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 482,025 | 4.820 | 130 | 134 | fits | 71,853 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 223,174 | 2.232 | 130 | 134 | fits | 76,648 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 240,124 | 2.401 | 130 | 134 | fits | 76,648 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 497,300 | 4.973 | 130 | 134 | fits | 71,853 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 514,074 | 5.141 | 130 | 134 | fits | 71,853 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 1,709,870 | 17.099 | 130 | 134 | fits | 76,609 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 1,727,600 | 17.276 | 130 | 134 | fits | 76,609 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 1,743,060 | 17.431 | 130 | 134 | fits | 76,609 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 1,760,098 | 17.601 | 130 | 134 | fits | 76,609 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 1,894,505 | 18.945 | 130 | 134 | fits | 73,267 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 1,911,946 | 19.119 | 130 | 134 | fits | 73,267 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 1,927,184 | 19.272 | 130 | 134 | fits | 73,267 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 1,943,903 | 19.439 | 130 | 134 | fits | 73,267 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 2,096,478 | 20.965 | 130 | 134 | fits | 72,768 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 2,114,016 | 21.140 | 130 | 134 | fits | 72,768 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 312,858 | 3.129 | 130 | 134 | fits | 173,858 | 211 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 331,552 | 3.316 | 130 | 134 | fits | 173,858 | 211 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 347,842 | 3.478 | 130 | 134 | fits | 173,858 | 211 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 366,257 | 3.663 | 130 | 134 | fits | 173,858 | 211 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 2,128,480 | 21.285 | 130 | 134 | fits | 72,768 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 2,145,199 | 21.452 | 130 | 134 | fits | 72,768 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 2,295,045 | 22.950 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 2,312,447 | 23.124 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 2,326,976 | 23.270 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 2,343,695 | 23.437 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 2,492,645 | 24.926 | 130 | 134 | fits | 71,148 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 2,509,968 | 25.100 | 130 | 134 | fits | 71,148 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,524,497 | 25.245 | 130 | 134 | fits | 71,148 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,541,216 | 25.412 | 130 | 134 | fits | 71,148 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,695,070 | 26.951 | 130 | 134 | fits | 72,218 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 2,712,450 | 27.125 | 130 | 134 | fits | 72,218 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 2,727,033 | 27.270 | 130 | 134 | fits | 72,218 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 2,743,910 | 27.439 | 130 | 134 | fits | 72,218 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 2,888,436 | 28.884 | 130 | 134 | fits | 66,415 | 202 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,900,889 | 29.009 | 130 | 134 | fits | 66,415 | 202 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,917,929 | 29.179 | 130 | 134 | fits | 66,415 | 202 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,935,040 | 29.350 | 130 | 134 | fits | 66,415 | 202 | 0.130 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 152,234 | 1.522 | 20 | 200 | fits | 154,795 | 198 | 0.249 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 733,664 | 7.337 | 20 | 20 | fits | 133,868 | 82 | 0.666 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 579,592 | 5.796 | 20 | 24 | fits | 150,619 | 108 | 0.463 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 694,189 | 6.942 | 20 | 50 | fits | 133,868 | 82 | 0.666 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,047,110 | 10.471 | 20 | 20 | fits | 105,664 | 48 | 0.710 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 185,895 | 1.859 | 130 | 134 | fits | 172,515 | 211 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 203,132 | 2.031 | 130 | 134 | fits | 172,515 | 211 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 336,812 | 3.368 | 130 | 134 | fits | 75,170 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 353,901 | 3.539 | 130 | 134 | fits | 75,170 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 1,814,832 | 18.148 | 130 | 134 | fits | 76,628 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 1,832,562 | 18.326 | 130 | 134 | fits | 76,628 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 616,736 | 6.167 | 130 | 134 | fits | 72,253 | 205 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 634,056 | 6.341 | 130 | 134 | fits | 72,253 | 205 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 649,442 | 6.494 | 130 | 134 | fits | 72,253 | 205 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 666,447 | 6.664 | 130 | 134 | fits | 72,253 | 205 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 219,534 | 2.195 | 130 | 134 | fits | 172,515 | 211 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 237,496 | 2.375 | 130 | 134 | fits | 172,515 | 211 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 466,859 | 4.669 | 130 | 134 | fits | 171,204 | 211 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 484,747 | 4.847 | 130 | 134 | fits | 171,204 | 211 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 500,676 | 5.007 | 130 | 134 | fits | 171,204 | 211 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 518,088 | 5.181 | 130 | 134 | fits | 171,204 | 211 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 1,848,296 | 18.483 | 130 | 134 | fits | 76,628 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 1,865,094 | 18.651 | 130 | 134 | fits | 76,628 | 203 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,978,269 | 19.783 | 130 | 134 | fits | 71,601 | 203 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,995,815 | 19.958 | 130 | 134 | fits | 71,601 | 203 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 370,158 | 3.702 | 130 | 134 | fits | 75,170 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 388,628 | 3.886 | 130 | 134 | fits | 75,170 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 2,010,358 | 20.104 | 130 | 134 | fits | 71,601 | 203 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 2,027,077 | 20.271 | 130 | 134 | fits | 71,601 | 203 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 2,176,475 | 21.765 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 2,193,877 | 21.939 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 2,208,406 | 22.084 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 2,225,125 | 22.251 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 2,374,087 | 23.741 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 2,391,410 | 23.914 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 2,405,939 | 24.059 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 2,422,658 | 24.227 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 2,575,016 | 25.750 | 130 | 134 | fits | 73,348 | 208 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 2,592,129 | 25.921 | 130 | 134 | fits | 73,348 | 208 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 2,606,712 | 26.067 | 130 | 134 | fits | 73,348 | 208 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 2,623,589 | 26.236 | 130 | 134 | fits | 73,348 | 208 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 2,769,196 | 27.692 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 2,781,616 | 27.816 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,798,656 | 27.987 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,815,767 | 28.158 | 130 | 134 | fits | 66,434 | 202 | 0.129 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 751,617 | 7.516 | 20 | 200 | fits | 150,481 | 207 | 0.192 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 865,981 | 8.660 | 20 | 20 | fits | 134,632 | 59 | 0.716 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 560,664 | 5.607 | 20 | 24 | fits | 153,621 | 114 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 691,874 | 6.919 | 20 | 50 | fits | 150,481 | 207 | 0.192 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 1,157,348 | 11.573 | 20 | 20 | fits | 80,099 | 34 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 324,594 | 3.246 | 130 | 134 | fits | 172,588 | 213 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 342,041 | 3.420 | 130 | 134 | fits | 172,588 | 213 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 611,130 | 6.111 | 130 | 134 | fits | 168,855 | 213 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 628,264 | 6.283 | 130 | 134 | fits | 168,855 | 213 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 643,467 | 6.435 | 130 | 134 | fits | 168,855 | 213 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 660,186 | 6.602 | 130 | 134 | fits | 168,855 | 213 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 758,219 | 7.582 | 130 | 134 | fits | 72,064 | 205 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 775,308 | 7.753 | 130 | 134 | fits | 72,064 | 205 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 1,951,988 | 19.520 | 130 | 134 | fits | 76,594 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 1,969,718 | 19.697 | 130 | 134 | fits | 76,594 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 1,985,178 | 19.852 | 130 | 134 | fits | 76,594 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 2,002,216 | 20.022 | 130 | 134 | fits | 76,594 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 358,451 | 3.585 | 130 | 134 | fits | 172,588 | 213 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 376,404 | 3.764 | 130 | 134 | fits | 172,588 | 213 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 790,964 | 7.910 | 130 | 134 | fits | 72,064 | 205 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 808,200 | 8.082 | 130 | 134 | fits | 72,064 | 205 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 2,116,663 | 21.167 | 130 | 134 | fits | 72,926 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 2,134,201 | 21.342 | 130 | 134 | fits | 72,926 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 475,880 | 4.759 | 130 | 134 | fits | 77,044 | 203 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 494,583 | 4.946 | 130 | 134 | fits | 77,044 | 203 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 510,849 | 5.108 | 130 | 134 | fits | 77,044 | 203 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 529,319 | 5.293 | 130 | 134 | fits | 77,044 | 203 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 2,148,665 | 21.487 | 130 | 134 | fits | 72,926 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 2,165,384 | 21.654 | 130 | 134 | fits | 72,926 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 2,315,325 | 23.153 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 2,332,727 | 23.327 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 2,347,256 | 23.473 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 2,363,975 | 23.640 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 2,512,819 | 25.128 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 2,530,142 | 25.301 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 2,544,671 | 25.447 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 2,561,390 | 25.614 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 2,713,479 | 27.135 | 130 | 134 | fits | 71,773 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 2,730,802 | 27.308 | 130 | 134 | fits | 71,773 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 2,745,231 | 27.452 | 130 | 134 | fits | 71,773 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 2,762,108 | 27.621 | 130 | 134 | fits | 71,773 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,926,075 | 29.261 | 130 | 134 | fits | 66,468 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,938,528 | 29.385 | 130 | 134 | fits | 66,468 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,955,568 | 29.556 | 130 | 134 | fits | 66,468 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,972,679 | 29.727 | 130 | 134 | fits | 66,468 | 202 | 0.131 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 849,501 | 8.495 | 20 | 200 | fits | 150,269 | 207 | 0.192 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 963,617 | 9.636 | 20 | 20 | fits | 134,384 | 59 | 0.714 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 658,760 | 6.588 | 20 | 24 | fits | 153,783 | 114 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 789,758 | 7.898 | 20 | 50 | fits | 150,269 | 207 | 0.192 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,255,152 | 12.552 | 20 | 20 | fits | 90,958 | 38 | 0.717 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 389,332 | 3.893 | 130 | 134 | fits | 170,180 | 211 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 406,581 | 4.066 | 130 | 134 | fits | 170,180 | 211 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 538,833 | 5.388 | 130 | 134 | fits | 71,754 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 555,922 | 5.559 | 130 | 134 | fits | 71,754 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 1,735,730 | 17.357 | 130 | 134 | fits | 76,709 | 203 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 1,753,460 | 17.535 | 130 | 134 | fits | 76,709 | 203 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 571,349 | 5.713 | 130 | 134 | fits | 71,754 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 588,354 | 5.884 | 130 | 134 | fits | 71,754 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 242,716 | 2.427 | 130 | 134 | fits | 76,694 | 205 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 260,649 | 2.606 | 130 | 134 | fits | 76,694 | 205 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 1,768,957 | 17.690 | 130 | 134 | fits | 76,709 | 203 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 1,785,995 | 17.860 | 130 | 134 | fits | 76,709 | 203 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 163,090 | 1.631 | 130 | 134 | fits | 102,669 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 181,695 | 1.817 | 130 | 134 | fits | 102,669 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 1,839,342 | 18.393 | 130 | 134 | fits | 72,773 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 1,856,801 | 18.568 | 130 | 134 | fits | 72,773 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 277,699 | 2.777 | 130 | 134 | fits | 76,694 | 205 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 295,938 | 2.959 | 130 | 134 | fits | 76,694 | 205 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,871,404 | 18.714 | 130 | 134 | fits | 72,773 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,888,346 | 18.883 | 130 | 134 | fits | 72,773 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 198,476 | 1.985 | 130 | 134 | fits | 102,669 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 217,353 | 2.174 | 130 | 134 | fits | 102,669 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 422,350 | 4.223 | 130 | 134 | fits | 170,180 | 211 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 440,455 | 4.405 | 130 | 134 | fits | 170,180 | 211 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 2,039,125 | 20.391 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 2,056,527 | 20.565 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 2,071,056 | 20.711 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 2,087,775 | 20.878 | 130 | 134 | fits | 71,150 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 2,236,698 | 22.367 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 2,254,021 | 22.540 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 2,268,550 | 22.686 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 2,285,269 | 22.853 | 130 | 134 | fits | 71,213 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 2,452,256 | 24.523 | 130 | 134 | fits | 71,057 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 2,469,579 | 24.696 | 130 | 134 | fits | 71,057 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 2,484,043 | 24.840 | 130 | 134 | fits | 71,057 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 2,500,920 | 25.009 | 130 | 134 | fits | 71,057 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,651,834 | 26.518 | 130 | 134 | fits | 67,113 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,664,346 | 26.643 | 130 | 134 | fits | 67,113 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,681,386 | 26.814 | 130 | 134 | fits | 67,113 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,698,497 | 26.985 | 130 | 134 | fits | 67,113 | 202 | 0.139 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 707,166 | 7.072 | 20 | 200 | fits | 150,403 | 207 | 0.191 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 821,505 | 8.215 | 20 | 20 | fits | 134,607 | 59 | 0.715 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 516,291 | 5.163 | 20 | 24 | fits | 154,750 | 120 | 0.477 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 647,423 | 6.474 | 20 | 50 | fits | 150,403 | 207 | 0.191 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 1,112,771 | 11.128 | 20 | 20 | fits | 80,105 | 34 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 444,559 | 4.446 | 130 | 134 | fits | 73,253 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 461,727 | 4.617 | 130 | 134 | fits | 73,253 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,672,359 | 16.724 | 130 | 134 | fits | 75,948 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,690,091 | 16.901 | 130 | 134 | fits | 75,948 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 163,081 | 1.631 | 130 | 134 | fits | 78,189 | 205 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 180,843 | 1.808 | 130 | 134 | fits | 78,189 | 205 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 1,705,421 | 17.054 | 130 | 134 | fits | 75,948 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 1,722,140 | 17.221 | 130 | 134 | fits | 75,948 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 293,215 | 2.932 | 130 | 134 | fits | 173,442 | 211 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 311,163 | 3.112 | 130 | 134 | fits | 173,442 | 211 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 1,836,633 | 18.366 | 130 | 134 | fits | 74,352 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 1,854,332 | 18.543 | 130 | 134 | fits | 74,352 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 197,374 | 1.974 | 130 | 134 | fits | 78,189 | 205 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 215,382 | 2.154 | 130 | 134 | fits | 78,189 | 205 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 477,599 | 4.776 | 130 | 134 | fits | 73,253 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 495,066 | 4.951 | 130 | 134 | fits | 73,253 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 1,870,018 | 18.700 | 130 | 134 | fits | 74,352 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 1,886,816 | 18.868 | 130 | 134 | fits | 74,352 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 2,037,949 | 20.379 | 130 | 134 | fits | 71,443 | 203 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 2,055,495 | 20.555 | 130 | 134 | fits | 71,443 | 203 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 327,403 | 3.274 | 130 | 134 | fits | 173,442 | 211 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 345,818 | 3.458 | 130 | 134 | fits | 173,442 | 211 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 2,070,038 | 20.700 | 130 | 134 | fits | 71,443 | 203 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 2,086,757 | 20.868 | 130 | 134 | fits | 71,443 | 203 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 2,236,209 | 22.362 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 2,253,611 | 22.536 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 2,268,140 | 22.681 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 2,284,859 | 22.849 | 130 | 134 | fits | 71,085 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 2,433,796 | 24.338 | 130 | 134 | fits | 71,148 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 2,451,119 | 24.511 | 130 | 134 | fits | 71,148 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 2,465,648 | 24.656 | 130 | 134 | fits | 71,148 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 2,482,367 | 24.824 | 130 | 134 | fits | 71,148 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 2,636,094 | 26.361 | 130 | 134 | fits | 72,218 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 2,653,474 | 26.535 | 130 | 134 | fits | 72,218 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 2,668,057 | 26.681 | 130 | 134 | fits | 72,218 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 2,684,934 | 26.849 | 130 | 134 | fits | 72,218 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 2,829,539 | 28.295 | 130 | 134 | fits | 66,415 | 202 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,841,992 | 28.420 | 130 | 134 | fits | 66,415 | 202 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,859,032 | 28.590 | 130 | 134 | fits | 66,415 | 202 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 2,876,143 | 28.761 | 130 | 134 | fits | 66,415 | 202 | 0.130 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 147,915 | 1.479 | 20 | 200 | fits | 158,997 | 196 | 0.318 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 743,434 | 7.434 | 20 | 20 | fits | 133,363 | 82 | 0.663 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 589,867 | 5.899 | 20 | 24 | fits | 161,135 | 129 | 0.442 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 703,959 | 7.040 | 20 | 50 | fits | 133,363 | 82 | 0.663 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 1,056,949 | 10.569 | 20 | 20 | fits | 101,860 | 42 | 0.711 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
