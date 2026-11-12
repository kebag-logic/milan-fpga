### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 736 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.acmp.if0` (notice-burst-4) | 11.579 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-6.held.adp.if1` (notice-burst-6) | 11.734 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-burst-4.held.aecp.if1` (notice-burst-4) | 12.121 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.maap.if0` (notice-burst-4) | 11.184 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-burst-2.held.srp.if1` (notice-burst-2) | 6.372 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.392 | fits | 0 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-0.mrpdu.periodic.if1` (notice-every-0) | 1.856 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 33.058 (33.388) | fits | 1 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1049 | 0 | 170,083 (1.701) | fits |
| notice-every-1 | 1046 | 0 | 172,712 (1.727) | fits |
| notice-every-2 | 1057 | 0 | 167,670 (1.677) | fits |
| notice-every-3 | 1053 | 0 | 170,395 (1.704) | fits |
| notice-every-4 | 1045 | 0 | 171,635 (1.716) | fits |
| notice-every-5 | 1043 | 0 | 173,458 (1.735) | fits |
| notice-every-6 | 1045 | 0 | 166,987 (1.670) | fits |
| notice-every-7 | 1043 | 0 | 173,242 (1.732) | fits |
| notice-burst-0 | 823 | 0 | 167,108 (1.671) | fits |
| notice-burst-1 | 824 | 0 | 169,597 (1.696) | fits |
| notice-burst-2 | 827 | 0 | 169,762 (1.698) | fits |
| notice-burst-3 | 829 | 0 | 169,462 (1.695) | fits |
| notice-burst-4 | 825 | 0 | 167,487 (1.675) | fits |
| notice-burst-5 | 820 | 0 | 172,545 (1.725) | fits |
| notice-burst-6 | 826 | 0 | 167,357 (1.674) | fits |
| notice-burst-7 | 816 | 0 | 169,680 (1.697) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 2.282 | 62 | 32 | 1 | within |
| notice-every-0 | 2.570 | 62 | 32 | 1 | within |
| notice-every-0 | 4.076 | 62 | 32 | 1 | within |
| notice-every-0 | 4.360 | 62 | 32 | 1 | within |
| notice-every-0 | 6.098 | 62 | 32 | 1 | within |
| notice-every-0 | 6.382 | 62 | 32 | 1 | within |
| notice-every-0 | 8.101 | 62 | 32 | 1 | within |
| notice-every-0 | 8.385 | 62 | 32 | 1 | within |
| notice-every-0 | 2.839 | 62 | 32 | 1 | within |
| notice-every-0 | 3.121 | 62 | 32 | 1 | within |
| notice-every-0 | 4.626 | 62 | 32 | 1 | within |
| notice-every-0 | 4.905 | 62 | 32 | 1 | within |
| notice-every-0 | 6.645 | 62 | 32 | 1 | within |
| notice-every-0 | 6.922 | 62 | 32 | 1 | within |
| notice-every-0 | 8.647 | 62 | 32 | 1 | within |
| notice-every-0 | 8.921 | 62 | 32 | 1 | within |
| notice-every-0 | 10.092 | 62 | 32 | 1 | within |
| notice-every-0 | 10.374 | 62 | 32 | 1 | within |
| notice-every-0 | 10.625 | 62 | 32 | 1 | within |
| notice-every-0 | 10.900 | 62 | 32 | 1 | within |
| notice-every-0 | 12.094 | 62 | 32 | 1 | within |
| notice-every-0 | 12.383 | 62 | 32 | 1 | within |
| notice-every-0 | 12.642 | 62 | 32 | 1 | within |
| notice-every-0 | 12.920 | 62 | 32 | 1 | within |
| notice-every-0 | 14.046 | 62 | 32 | 1 | within |
| notice-every-0 | 14.332 | 62 | 32 | 1 | within |
| notice-every-0 | 14.587 | 62 | 32 | 1 | within |
| notice-every-0 | 14.861 | 62 | 32 | 1 | within |
| notice-every-0 | 16.203 | 62 | 32 | 1 | within |
| notice-every-0 | 16.486 | 62 | 32 | 1 | within |
| notice-every-0 | 16.738 | 62 | 32 | 1 | within |
| notice-every-0 | 17.014 | 62 | 32 | 1 | within |
| notice-every-0 | 18.111 | 62 | 32 | 1 | within |
| notice-every-0 | 18.395 | 62 | 32 | 1 | within |
| notice-every-0 | 18.650 | 62 | 32 | 1 | within |
| notice-every-0 | 18.927 | 62 | 32 | 1 | within |
| notice-every-0 | 20.524 | 62 | 32 | 1 | within |
| notice-every-0 | 24.085 | 62 | 32 | 1 | within |
| notice-every-0 | 24.372 | 62 | 32 | 1 | within |
| notice-every-0 | 24.655 | 62 | 32 | 1 | within |
| notice-every-1 | 2.295 | 62 | 32 | 1 | within |
| notice-every-1 | 2.584 | 62 | 32 | 1 | within |
| notice-every-1 | 4.098 | 62 | 32 | 1 | within |
| notice-every-1 | 4.382 | 62 | 32 | 1 | within |
| notice-every-1 | 6.121 | 62 | 32 | 1 | within |
| notice-every-1 | 6.405 | 62 | 32 | 1 | within |
| notice-every-1 | 8.124 | 62 | 32 | 1 | within |
| notice-every-1 | 8.408 | 62 | 32 | 1 | within |
| notice-every-1 | 2.853 | 62 | 32 | 1 | within |
| notice-every-1 | 3.135 | 62 | 32 | 1 | within |
| notice-every-1 | 4.648 | 62 | 32 | 1 | within |
| notice-every-1 | 4.927 | 62 | 32 | 1 | within |
| notice-every-1 | 6.668 | 62 | 32 | 1 | within |
| notice-every-1 | 6.945 | 62 | 32 | 1 | within |
| notice-every-1 | 8.670 | 62 | 32 | 1 | within |
| notice-every-1 | 8.944 | 62 | 32 | 1 | within |
| notice-every-1 | 10.115 | 62 | 32 | 1 | within |
| notice-every-1 | 10.397 | 62 | 32 | 1 | within |
| notice-every-1 | 10.648 | 62 | 32 | 1 | within |
| notice-every-1 | 10.923 | 62 | 32 | 1 | within |
| notice-every-1 | 12.117 | 62 | 32 | 1 | within |
| notice-every-1 | 12.406 | 62 | 32 | 1 | within |
| notice-every-1 | 12.665 | 62 | 32 | 1 | within |
| notice-every-1 | 12.943 | 62 | 32 | 1 | within |
| notice-every-1 | 14.069 | 62 | 32 | 1 | within |
| notice-every-1 | 14.354 | 62 | 32 | 1 | within |
| notice-every-1 | 14.610 | 62 | 32 | 1 | within |
| notice-every-1 | 14.884 | 62 | 32 | 1 | within |
| notice-every-1 | 16.226 | 62 | 32 | 1 | within |
| notice-every-1 | 16.509 | 62 | 32 | 1 | within |
| notice-every-1 | 16.761 | 62 | 32 | 1 | within |
| notice-every-1 | 17.037 | 62 | 32 | 1 | within |
| notice-every-1 | 18.134 | 62 | 32 | 1 | within |
| notice-every-1 | 18.418 | 62 | 32 | 1 | within |
| notice-every-1 | 18.673 | 62 | 32 | 1 | within |
| notice-every-1 | 18.950 | 62 | 32 | 1 | within |
| notice-every-1 | 20.248 | 62 | 32 | 1 | within |
| notice-every-1 | 20.487 | 62 | 32 | 1 | within |
| notice-every-1 | 20.770 | 62 | 32 | 1 | within |
| notice-every-1 | 21.053 | 62 | 32 | 1 | within |
| notice-every-2 | 4.109 | 62 | 32 | 2 | within |
| notice-every-2 | 4.392 | 62 | 32 | 2 | within |
| notice-every-2 | 6.126 | 62 | 32 | 2 | within |
| notice-every-2 | 6.410 | 62 | 32 | 2 | within |
| notice-every-2 | 8.134 | 62 | 32 | 2 | within |
| notice-every-2 | 8.419 | 62 | 32 | 2 | within |
| notice-every-2 | 2.314 | 62 | 32 | 2 | within |
| notice-every-2 | 2.611 | 62 | 32 | 2 | within |
| notice-every-2 | 2.880 | 62 | 32 | 2 | within |
| notice-every-2 | 3.162 | 62 | 32 | 2 | within |
| notice-every-2 | 4.656 | 62 | 32 | 2 | within |
| notice-every-2 | 4.936 | 62 | 32 | 2 | within |
| notice-every-2 | 6.674 | 62 | 32 | 2 | within |
| notice-every-2 | 6.951 | 62 | 32 | 2 | within |
| notice-every-2 | 8.681 | 62 | 32 | 2 | within |
| notice-every-2 | 8.956 | 62 | 32 | 2 | within |
| notice-every-2 | 10.127 | 62 | 32 | 2 | within |
| notice-every-2 | 10.409 | 62 | 32 | 2 | within |
| notice-every-2 | 10.660 | 62 | 32 | 2 | within |
| notice-every-2 | 10.935 | 62 | 32 | 2 | within |
| notice-every-2 | 12.129 | 62 | 32 | 2 | within |
| notice-every-2 | 12.418 | 62 | 32 | 2 | within |
| notice-every-2 | 12.676 | 62 | 32 | 2 | within |
| notice-every-2 | 12.955 | 62 | 32 | 2 | within |
| notice-every-2 | 14.317 | 62 | 32 | 2 | within |
| notice-every-2 | 14.603 | 62 | 32 | 2 | within |
| notice-every-2 | 14.858 | 62 | 32 | 2 | within |
| notice-every-2 | 15.132 | 62 | 32 | 2 | within |
| notice-every-2 | 16.239 | 62 | 32 | 2 | within |
| notice-every-2 | 16.521 | 62 | 32 | 2 | within |
| notice-every-2 | 16.774 | 62 | 32 | 2 | within |
| notice-every-2 | 17.050 | 62 | 32 | 2 | within |
| notice-every-2 | 18.146 | 62 | 32 | 2 | within |
| notice-every-2 | 18.430 | 62 | 32 | 2 | within |
| notice-every-2 | 18.685 | 62 | 32 | 2 | within |
| notice-every-2 | 18.962 | 62 | 32 | 2 | within |
| notice-every-2 | 20.262 | 62 | 32 | 2 | within |
| notice-every-2 | 20.501 | 62 | 32 | 2 | within |
| notice-every-2 | 20.785 | 62 | 32 | 2 | within |
| notice-every-2 | 21.068 | 62 | 32 | 2 | within |
| notice-every-3 | 2.295 | 62 | 32 | 1 | within |
| notice-every-3 | 2.582 | 62 | 32 | 1 | within |
| notice-every-3 | 4.099 | 62 | 32 | 1 | within |
| notice-every-3 | 4.383 | 62 | 32 | 1 | within |
| notice-every-3 | 6.114 | 62 | 32 | 1 | within |
| notice-every-3 | 6.398 | 62 | 32 | 1 | within |
| notice-every-3 | 8.118 | 62 | 32 | 1 | within |
| notice-every-3 | 8.402 | 62 | 32 | 1 | within |
| notice-every-3 | 2.851 | 62 | 32 | 1 | within |
| notice-every-3 | 3.133 | 62 | 32 | 1 | within |
| notice-every-3 | 4.649 | 62 | 32 | 1 | within |
| notice-every-3 | 4.928 | 62 | 32 | 1 | within |
| notice-every-3 | 6.661 | 62 | 32 | 1 | within |
| notice-every-3 | 6.938 | 62 | 32 | 1 | within |
| notice-every-3 | 8.663 | 62 | 32 | 1 | within |
| notice-every-3 | 8.938 | 62 | 32 | 1 | within |
| notice-every-3 | 10.109 | 62 | 32 | 1 | within |
| notice-every-3 | 10.390 | 62 | 32 | 1 | within |
| notice-every-3 | 10.642 | 62 | 32 | 1 | within |
| notice-every-3 | 10.916 | 62 | 32 | 1 | within |
| notice-every-3 | 12.110 | 62 | 32 | 1 | within |
| notice-every-3 | 12.399 | 62 | 32 | 1 | within |
| notice-every-3 | 12.658 | 62 | 32 | 1 | within |
| notice-every-3 | 12.936 | 62 | 32 | 1 | within |
| notice-every-3 | 14.299 | 62 | 32 | 1 | within |
| notice-every-3 | 14.584 | 62 | 32 | 1 | within |
| notice-every-3 | 14.839 | 62 | 32 | 1 | within |
| notice-every-3 | 15.114 | 62 | 32 | 1 | within |
| notice-every-3 | 16.220 | 62 | 32 | 1 | within |
| notice-every-3 | 16.502 | 62 | 32 | 1 | within |
| notice-every-3 | 16.755 | 62 | 32 | 1 | within |
| notice-every-3 | 17.031 | 62 | 32 | 1 | within |
| notice-every-3 | 18.128 | 62 | 32 | 1 | within |
| notice-every-3 | 18.412 | 62 | 32 | 1 | within |
| notice-every-3 | 18.667 | 62 | 32 | 1 | within |
| notice-every-3 | 18.943 | 62 | 32 | 1 | within |
| notice-every-3 | 20.244 | 62 | 32 | 1 | within |
| notice-every-3 | 20.482 | 62 | 32 | 1 | within |
| notice-every-3 | 20.765 | 62 | 32 | 1 | within |
| notice-every-3 | 21.048 | 62 | 32 | 1 | within |
| notice-every-4 | 2.295 | 62 | 32 | 1 | within |
| notice-every-4 | 2.583 | 62 | 32 | 1 | within |
| notice-every-4 | 4.100 | 62 | 32 | 1 | within |
| notice-every-4 | 4.385 | 62 | 32 | 1 | within |
| notice-every-4 | 6.124 | 62 | 32 | 1 | within |
| notice-every-4 | 6.407 | 62 | 32 | 1 | within |
| notice-every-4 | 8.127 | 62 | 32 | 1 | within |
| notice-every-4 | 8.410 | 62 | 32 | 1 | within |
| notice-every-4 | 2.852 | 62 | 32 | 1 | within |
| notice-every-4 | 3.134 | 62 | 32 | 1 | within |
| notice-every-4 | 4.650 | 62 | 32 | 1 | within |
| notice-every-4 | 4.930 | 62 | 32 | 1 | within |
| notice-every-4 | 6.671 | 62 | 32 | 1 | within |
| notice-every-4 | 6.948 | 62 | 32 | 1 | within |
| notice-every-4 | 8.672 | 62 | 32 | 1 | within |
| notice-every-4 | 8.947 | 62 | 32 | 1 | within |
| notice-every-4 | 10.117 | 62 | 32 | 1 | within |
| notice-every-4 | 10.399 | 62 | 32 | 1 | within |
| notice-every-4 | 10.651 | 62 | 32 | 1 | within |
| notice-every-4 | 10.925 | 62 | 32 | 1 | within |
| notice-every-4 | 12.120 | 62 | 32 | 1 | within |
| notice-every-4 | 12.408 | 62 | 32 | 1 | within |
| notice-every-4 | 12.667 | 62 | 32 | 1 | within |
| notice-every-4 | 12.945 | 62 | 32 | 1 | within |
| notice-every-4 | 14.072 | 62 | 32 | 1 | within |
| notice-every-4 | 14.357 | 62 | 32 | 1 | within |
| notice-every-4 | 14.612 | 62 | 32 | 1 | within |
| notice-every-4 | 14.887 | 62 | 32 | 1 | within |
| notice-every-4 | 16.226 | 62 | 32 | 1 | within |
| notice-every-4 | 16.508 | 62 | 32 | 1 | within |
| notice-every-4 | 16.761 | 62 | 32 | 1 | within |
| notice-every-4 | 17.037 | 62 | 32 | 1 | within |
| notice-every-4 | 18.134 | 62 | 32 | 1 | within |
| notice-every-4 | 18.418 | 62 | 32 | 1 | within |
| notice-every-4 | 18.673 | 62 | 32 | 1 | within |
| notice-every-4 | 18.950 | 62 | 32 | 1 | within |
| notice-every-4 | 20.548 | 62 | 32 | 1 | within |
| notice-every-4 | 24.111 | 62 | 32 | 1 | within |
| notice-every-4 | 24.399 | 62 | 32 | 1 | within |
| notice-every-4 | 24.681 | 62 | 32 | 1 | within |
| notice-every-5 | 4.102 | 62 | 32 | 1 | within |
| notice-every-5 | 4.385 | 62 | 32 | 1 | within |
| notice-every-5 | 2.298 | 62 | 32 | 1 | within |
| notice-every-5 | 2.589 | 62 | 32 | 1 | within |
| notice-every-5 | 6.125 | 62 | 32 | 1 | within |
| notice-every-5 | 6.409 | 62 | 32 | 1 | within |
| notice-every-5 | 8.128 | 62 | 32 | 1 | within |
| notice-every-5 | 8.412 | 62 | 32 | 1 | within |
| notice-every-5 | 2.859 | 62 | 32 | 1 | within |
| notice-every-5 | 3.141 | 62 | 32 | 1 | within |
| notice-every-5 | 4.650 | 62 | 32 | 1 | within |
| notice-every-5 | 4.929 | 62 | 32 | 1 | within |
| notice-every-5 | 6.672 | 62 | 32 | 1 | within |
| notice-every-5 | 6.949 | 62 | 32 | 1 | within |
| notice-every-5 | 8.673 | 62 | 32 | 1 | within |
| notice-every-5 | 8.948 | 62 | 32 | 1 | within |
| notice-every-5 | 10.119 | 62 | 32 | 1 | within |
| notice-every-5 | 10.400 | 62 | 32 | 1 | within |
| notice-every-5 | 10.652 | 62 | 32 | 1 | within |
| notice-every-5 | 10.926 | 62 | 32 | 1 | within |
| notice-every-5 | 12.121 | 62 | 32 | 1 | within |
| notice-every-5 | 12.410 | 62 | 32 | 1 | within |
| notice-every-5 | 12.669 | 62 | 32 | 1 | within |
| notice-every-5 | 12.947 | 62 | 32 | 1 | within |
| notice-every-5 | 14.309 | 62 | 32 | 1 | within |
| notice-every-5 | 14.595 | 62 | 32 | 1 | within |
| notice-every-5 | 14.850 | 62 | 32 | 1 | within |
| notice-every-5 | 15.124 | 62 | 32 | 1 | within |
| notice-every-5 | 16.232 | 62 | 32 | 1 | within |
| notice-every-5 | 16.514 | 62 | 32 | 1 | within |
| notice-every-5 | 16.766 | 62 | 32 | 1 | within |
| notice-every-5 | 17.042 | 62 | 32 | 1 | within |
| notice-every-5 | 18.139 | 62 | 32 | 1 | within |
| notice-every-5 | 18.423 | 62 | 32 | 1 | within |
| notice-every-5 | 18.678 | 62 | 32 | 1 | within |
| notice-every-5 | 18.955 | 62 | 32 | 1 | within |
| notice-every-5 | 20.255 | 62 | 32 | 1 | within |
| notice-every-5 | 20.494 | 62 | 32 | 1 | within |
| notice-every-5 | 20.777 | 62 | 32 | 1 | within |
| notice-every-5 | 21.060 | 62 | 32 | 1 | within |
| notice-every-6 | 4.102 | 62 | 32 | 1 | within |
| notice-every-6 | 4.384 | 62 | 32 | 1 | within |
| notice-every-6 | 6.125 | 62 | 32 | 1 | within |
| notice-every-6 | 6.408 | 62 | 32 | 1 | within |
| notice-every-6 | 2.300 | 62 | 32 | 1 | within |
| notice-every-6 | 2.593 | 62 | 32 | 1 | within |
| notice-every-6 | 8.128 | 62 | 32 | 1 | within |
| notice-every-6 | 8.412 | 62 | 32 | 1 | within |
| notice-every-6 | 2.860 | 62 | 32 | 1 | within |
| notice-every-6 | 3.143 | 62 | 32 | 1 | within |
| notice-every-6 | 4.649 | 62 | 32 | 1 | within |
| notice-every-6 | 4.928 | 62 | 32 | 1 | within |
| notice-every-6 | 6.672 | 62 | 32 | 1 | within |
| notice-every-6 | 6.949 | 62 | 32 | 1 | within |
| notice-every-6 | 8.674 | 62 | 32 | 1 | within |
| notice-every-6 | 8.948 | 62 | 32 | 1 | within |
| notice-every-6 | 10.120 | 62 | 32 | 1 | within |
| notice-every-6 | 10.402 | 62 | 32 | 1 | within |
| notice-every-6 | 10.653 | 62 | 32 | 1 | within |
| notice-every-6 | 10.928 | 62 | 32 | 1 | within |
| notice-every-6 | 12.122 | 62 | 32 | 1 | within |
| notice-every-6 | 12.411 | 62 | 32 | 1 | within |
| notice-every-6 | 12.669 | 62 | 32 | 1 | within |
| notice-every-6 | 12.948 | 62 | 32 | 1 | within |
| notice-every-6 | 14.074 | 62 | 32 | 1 | within |
| notice-every-6 | 14.359 | 62 | 32 | 1 | within |
| notice-every-6 | 14.614 | 62 | 32 | 1 | within |
| notice-every-6 | 14.889 | 62 | 32 | 1 | within |
| notice-every-6 | 16.231 | 62 | 32 | 1 | within |
| notice-every-6 | 16.513 | 62 | 32 | 1 | within |
| notice-every-6 | 16.766 | 62 | 32 | 1 | within |
| notice-every-6 | 17.042 | 62 | 32 | 1 | within |
| notice-every-6 | 18.139 | 62 | 32 | 1 | within |
| notice-every-6 | 18.423 | 62 | 32 | 1 | within |
| notice-every-6 | 18.678 | 62 | 32 | 1 | within |
| notice-every-6 | 18.955 | 62 | 32 | 1 | within |
| notice-every-6 | 20.551 | 62 | 32 | 1 | within |
| notice-every-6 | 24.115 | 62 | 32 | 1 | within |
| notice-every-6 | 24.402 | 62 | 32 | 1 | within |
| notice-every-6 | 24.685 | 62 | 32 | 1 | within |
| notice-every-7 | 2.296 | 62 | 32 | 1 | within |
| notice-every-7 | 2.584 | 62 | 32 | 1 | within |
| notice-every-7 | 4.101 | 62 | 32 | 1 | within |
| notice-every-7 | 4.385 | 62 | 32 | 1 | within |
| notice-every-7 | 6.124 | 62 | 32 | 1 | within |
| notice-every-7 | 6.408 | 62 | 32 | 1 | within |
| notice-every-7 | 8.127 | 62 | 32 | 1 | within |
| notice-every-7 | 8.411 | 62 | 32 | 1 | within |
| notice-every-7 | 2.853 | 62 | 32 | 1 | within |
| notice-every-7 | 3.135 | 62 | 32 | 1 | within |
| notice-every-7 | 4.651 | 62 | 32 | 1 | within |
| notice-every-7 | 4.930 | 62 | 32 | 1 | within |
| notice-every-7 | 6.671 | 62 | 32 | 1 | within |
| notice-every-7 | 6.948 | 62 | 32 | 1 | within |
| notice-every-7 | 8.673 | 62 | 32 | 1 | within |
| notice-every-7 | 8.947 | 62 | 32 | 1 | within |
| notice-every-7 | 10.118 | 62 | 32 | 1 | within |
| notice-every-7 | 10.400 | 62 | 32 | 1 | within |
| notice-every-7 | 10.651 | 62 | 32 | 1 | within |
| notice-every-7 | 10.926 | 62 | 32 | 1 | within |
| notice-every-7 | 12.120 | 62 | 32 | 1 | within |
| notice-every-7 | 12.409 | 62 | 32 | 1 | within |
| notice-every-7 | 12.668 | 62 | 32 | 1 | within |
| notice-every-7 | 12.946 | 62 | 32 | 1 | within |
| notice-every-7 | 14.072 | 62 | 32 | 1 | within |
| notice-every-7 | 14.357 | 62 | 32 | 1 | within |
| notice-every-7 | 14.613 | 62 | 32 | 1 | within |
| notice-every-7 | 14.887 | 62 | 32 | 1 | within |
| notice-every-7 | 16.227 | 62 | 32 | 1 | within |
| notice-every-7 | 16.509 | 62 | 32 | 1 | within |
| notice-every-7 | 16.761 | 62 | 32 | 1 | within |
| notice-every-7 | 17.037 | 62 | 32 | 1 | within |
| notice-every-7 | 18.135 | 62 | 32 | 1 | within |
| notice-every-7 | 18.418 | 62 | 32 | 1 | within |
| notice-every-7 | 18.674 | 62 | 32 | 1 | within |
| notice-every-7 | 18.950 | 62 | 32 | 1 | within |
| notice-every-7 | 20.550 | 62 | 32 | 1 | within |
| notice-every-7 | 24.112 | 62 | 32 | 1 | within |
| notice-every-7 | 24.400 | 62 | 32 | 1 | within |
| notice-every-7 | 24.682 | 62 | 32 | 1 | within |
| notice-burst-0 | 1.581 | 62 | 32 | 0 | within |
| notice-burst-0 | 1.866 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.845 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.127 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.667 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.950 | 62 | 32 | 0 | within |
| notice-burst-0 | 8.727 | 62 | 32 | 0 | within |
| notice-burst-0 | 13.672 | 62 | 32 | 0 | within |
| notice-burst-0 | 17.949 | 62 | 32 | 0 | within |
| notice-burst-0 | 21.580 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.394 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.676 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.215 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.494 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.841 | 62 | 32 | 0 | within |
| notice-burst-0 | 6.126 | 62 | 32 | 0 | within |
| notice-burst-0 | 6.387 | 62 | 32 | 0 | within |
| notice-burst-0 | 6.667 | 62 | 32 | 0 | within |
| notice-burst-0 | 21.845 | 62 | 32 | 0 | within |
| notice-burst-0 | 22.121 | 62 | 32 | 0 | within |
| notice-burst-0 | 22.377 | 62 | 32 | 0 | within |
| notice-burst-0 | 23.526 | 62 | 32 | 0 | within |
| notice-burst-0 | 23.797 | 62 | 32 | 0 | within |
| notice-burst-0 | 24.076 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.152 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.459 | 62 | 32 | 0 | within |
| notice-burst-0 | 24.330 | 62 | 32 | 0 | within |
| notice-burst-0 | 25.697 | 62 | 32 | 0 | within |
| notice-burst-0 | 25.961 | 62 | 32 | 0 | within |
| notice-burst-0 | 26.236 | 62 | 32 | 0 | within |
| notice-burst-0 | 26.487 | 62 | 32 | 0 | within |
| notice-burst-0 | 27.606 | 62 | 32 | 0 | within |
| notice-burst-0 | 27.873 | 62 | 32 | 0 | within |
| notice-burst-0 | 28.151 | 62 | 32 | 0 | within |
| notice-burst-0 | 28.405 | 62 | 32 | 0 | within |
| notice-burst-0 | 29.748 | 62 | 32 | 0 | within |
| notice-burst-0 | 29.999 | 62 | 32 | 0 | within |
| notice-burst-0 | 30.235 | 62 | 32 | 0 | within |
| notice-burst-0 | 30.512 | 62 | 32 | 0 | within |
| notice-burst-0 | 31.675 | 62 | 32 | 0 | within |
| notice-burst-1 | 4.113 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.396 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.656 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.932 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.282 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.563 | 62 | 32 | 1 | within |
| notice-burst-1 | 8.112 | 62 | 32 | 1 | within |
| notice-burst-1 | 12.967 | 62 | 32 | 1 | within |
| notice-burst-1 | 16.585 | 62 | 32 | 1 | within |
| notice-burst-1 | 20.352 | 62 | 32 | 1 | within |
| notice-burst-1 | 20.628 | 62 | 32 | 1 | within |
| notice-burst-1 | 20.902 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.161 | 62 | 32 | 1 | within |
| notice-burst-1 | 22.147 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.265 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.567 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.842 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.133 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.824 | 62 | 32 | 1 | within |
| notice-burst-1 | 6.108 | 62 | 32 | 1 | within |
| notice-burst-1 | 22.418 | 62 | 32 | 1 | within |
| notice-burst-1 | 22.699 | 62 | 32 | 1 | within |
| notice-burst-1 | 22.957 | 62 | 32 | 1 | within |
| notice-burst-1 | 24.107 | 62 | 32 | 1 | within |
| notice-burst-1 | 24.378 | 62 | 32 | 1 | within |
| notice-burst-1 | 24.657 | 62 | 32 | 1 | within |
| notice-burst-1 | 24.911 | 62 | 32 | 1 | within |
| notice-burst-1 | 26.271 | 62 | 32 | 1 | within |
| notice-burst-1 | 26.535 | 62 | 32 | 1 | within |
| notice-burst-1 | 26.809 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.061 | 62 | 32 | 1 | within |
| notice-burst-1 | 28.180 | 62 | 32 | 1 | within |
| notice-burst-1 | 28.447 | 62 | 32 | 1 | within |
| notice-burst-1 | 28.724 | 62 | 32 | 1 | within |
| notice-burst-1 | 28.978 | 62 | 32 | 1 | within |
| notice-burst-1 | 30.323 | 62 | 32 | 1 | within |
| notice-burst-1 | 30.575 | 62 | 32 | 1 | within |
| notice-burst-1 | 30.811 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.088 | 62 | 32 | 1 | within |
| notice-burst-1 | 32.266 | 62 | 32 | 1 | within |
| notice-burst-2 | 4.517 | 62 | 32 | 0 | within |
| notice-burst-2 | 4.799 | 62 | 32 | 0 | within |
| notice-burst-2 | 5.060 | 62 | 32 | 0 | within |
| notice-burst-2 | 5.336 | 62 | 32 | 0 | within |
| notice-burst-2 | 7.406 | 62 | 32 | 0 | within |
| notice-burst-2 | 10.945 | 62 | 32 | 0 | within |
| notice-burst-2 | 15.996 | 62 | 32 | 0 | within |
| notice-burst-2 | 19.600 | 62 | 32 | 0 | within |
| notice-burst-2 | 19.877 | 62 | 32 | 0 | within |
| notice-burst-2 | 20.152 | 62 | 32 | 0 | within |
| notice-burst-2 | 20.410 | 62 | 32 | 0 | within |
| notice-burst-2 | 21.640 | 62 | 32 | 0 | within |
| notice-burst-2 | 21.918 | 62 | 32 | 0 | within |
| notice-burst-2 | 22.194 | 62 | 32 | 0 | within |
| notice-burst-2 | 1.595 | 62 | 32 | 0 | within |
| notice-burst-2 | 1.896 | 62 | 32 | 0 | within |
| notice-burst-2 | 2.890 | 62 | 32 | 0 | within |
| notice-burst-2 | 3.187 | 62 | 32 | 0 | within |
| notice-burst-2 | 3.453 | 62 | 32 | 0 | within |
| notice-burst-2 | 3.744 | 62 | 32 | 0 | within |
| notice-burst-2 | 22.451 | 62 | 32 | 0 | within |
| notice-burst-2 | 23.600 | 62 | 32 | 0 | within |
| notice-burst-2 | 23.871 | 62 | 32 | 0 | within |
| notice-burst-2 | 24.150 | 62 | 32 | 0 | within |
| notice-burst-2 | 24.408 | 62 | 32 | 0 | within |
| notice-burst-2 | 25.545 | 62 | 32 | 0 | within |
| notice-burst-2 | 2.181 | 62 | 32 | 0 | within |
| notice-burst-2 | 2.489 | 62 | 32 | 0 | within |
| notice-burst-2 | 25.814 | 62 | 32 | 0 | within |
| notice-burst-2 | 26.088 | 62 | 32 | 0 | within |
| notice-burst-2 | 26.340 | 62 | 32 | 0 | within |
| notice-burst-2 | 27.696 | 62 | 32 | 0 | within |
| notice-burst-2 | 27.963 | 62 | 32 | 0 | within |
| notice-burst-2 | 28.241 | 62 | 32 | 0 | within |
| notice-burst-2 | 28.495 | 62 | 32 | 0 | within |
| notice-burst-2 | 29.608 | 62 | 32 | 0 | within |
| notice-burst-2 | 29.859 | 62 | 32 | 0 | within |
| notice-burst-2 | 30.096 | 62 | 32 | 0 | within |
| notice-burst-2 | 30.372 | 62 | 32 | 0 | within |
| notice-burst-2 | 31.533 | 62 | 32 | 0 | within |
| notice-burst-3 | 5.329 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.609 | 62 | 32 | 1 | within |
| notice-burst-3 | 8.181 | 62 | 32 | 1 | within |
| notice-burst-3 | 13.030 | 62 | 32 | 1 | within |
| notice-burst-3 | 16.617 | 62 | 32 | 1 | within |
| notice-burst-3 | 20.131 | 62 | 32 | 1 | within |
| notice-burst-3 | 20.405 | 62 | 32 | 1 | within |
| notice-burst-3 | 20.682 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.266 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.561 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.139 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.431 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.698 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.982 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.873 | 62 | 32 | 1 | within |
| notice-burst-3 | 6.155 | 62 | 32 | 1 | within |
| notice-burst-3 | 20.944 | 62 | 32 | 1 | within |
| notice-burst-3 | 22.161 | 62 | 32 | 1 | within |
| notice-burst-3 | 22.425 | 62 | 32 | 1 | within |
| notice-burst-3 | 22.701 | 62 | 32 | 1 | within |
| notice-burst-3 | 22.957 | 62 | 32 | 1 | within |
| notice-burst-3 | 24.340 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.843 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.146 | 62 | 32 | 1 | within |
| notice-burst-3 | 24.612 | 62 | 32 | 1 | within |
| notice-burst-3 | 24.891 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.145 | 62 | 32 | 1 | within |
| notice-burst-3 | 26.277 | 62 | 32 | 1 | within |
| notice-burst-3 | 26.541 | 62 | 32 | 1 | within |
| notice-burst-3 | 26.815 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.067 | 62 | 32 | 1 | within |
| notice-burst-3 | 28.185 | 62 | 32 | 1 | within |
| notice-burst-3 | 28.451 | 62 | 32 | 1 | within |
| notice-burst-3 | 28.729 | 62 | 32 | 1 | within |
| notice-burst-3 | 28.983 | 62 | 32 | 1 | within |
| notice-burst-3 | 30.329 | 62 | 32 | 1 | within |
| notice-burst-3 | 30.580 | 62 | 32 | 1 | within |
| notice-burst-3 | 30.817 | 62 | 32 | 1 | within |
| notice-burst-3 | 31.094 | 62 | 32 | 1 | within |
| notice-burst-3 | 32.270 | 62 | 32 | 1 | within |
| notice-burst-4 | 6.610 | 62 | 32 | 1 | within |
| notice-burst-4 | 6.890 | 62 | 32 | 1 | within |
| notice-burst-4 | 9.511 | 62 | 32 | 1 | within |
| notice-burst-4 | 14.478 | 62 | 32 | 1 | within |
| notice-burst-4 | 18.771 | 62 | 32 | 1 | within |
| notice-burst-4 | 22.412 | 62 | 32 | 1 | within |
| notice-burst-4 | 22.688 | 62 | 32 | 1 | within |
| notice-burst-4 | 22.965 | 62 | 32 | 1 | within |
| notice-burst-4 | 2.280 | 62 | 32 | 1 | within |
| notice-burst-4 | 2.573 | 62 | 32 | 1 | within |
| notice-burst-4 | 23.226 | 62 | 32 | 1 | within |
| notice-burst-4 | 24.378 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.563 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.855 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.124 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.410 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.417 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.710 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.973 | 62 | 32 | 1 | within |
| notice-burst-4 | 6.259 | 62 | 32 | 1 | within |
| notice-burst-4 | 7.155 | 62 | 32 | 1 | within |
| notice-burst-4 | 7.443 | 62 | 32 | 1 | within |
| notice-burst-4 | 24.646 | 62 | 32 | 1 | within |
| notice-burst-4 | 24.925 | 62 | 32 | 1 | within |
| notice-burst-4 | 2.859 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.166 | 62 | 32 | 1 | within |
| notice-burst-4 | 25.179 | 62 | 32 | 1 | within |
| notice-burst-4 | 26.311 | 62 | 32 | 1 | within |
| notice-burst-4 | 26.575 | 62 | 32 | 1 | within |
| notice-burst-4 | 26.850 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.101 | 62 | 32 | 1 | within |
| notice-burst-4 | 28.455 | 62 | 32 | 1 | within |
| notice-burst-4 | 28.722 | 62 | 32 | 1 | within |
| notice-burst-4 | 28.999 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.253 | 62 | 32 | 1 | within |
| notice-burst-4 | 30.367 | 62 | 32 | 1 | within |
| notice-burst-4 | 30.618 | 62 | 32 | 1 | within |
| notice-burst-4 | 30.855 | 62 | 32 | 1 | within |
| notice-burst-4 | 31.131 | 62 | 32 | 1 | within |
| notice-burst-4 | 32.292 | 62 | 32 | 1 | within |
| notice-burst-5 | 8.248 | 62 | 32 | 1 | within |
| notice-burst-5 | 13.106 | 62 | 32 | 1 | within |
| notice-burst-5 | 17.551 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.167 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.266 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.557 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.125 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.413 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.680 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.959 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.444 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.719 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.312 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.599 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.862 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.144 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.979 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.194 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.458 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.734 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.990 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.136 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.839 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.142 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.408 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.687 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.941 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.073 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.337 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.611 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.863 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.214 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.481 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.758 | 62 | 32 | 1 | within |
| notice-burst-5 | 30.012 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.126 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.377 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.614 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.891 | 62 | 32 | 1 | within |
| notice-burst-5 | 33.058 | 62 | 32 | 1 | within |
| notice-burst-6 | 8.768 | 62 | 32 | 0 | within |
| notice-burst-6 | 13.729 | 62 | 32 | 0 | within |
| notice-burst-6 | 1.641 | 62 | 32 | 0 | within |
| notice-burst-6 | 1.929 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.908 | 62 | 32 | 0 | within |
| notice-burst-6 | 3.192 | 62 | 32 | 0 | within |
| notice-burst-6 | 3.451 | 62 | 32 | 0 | within |
| notice-burst-6 | 3.730 | 62 | 32 | 0 | within |
| notice-burst-6 | 4.725 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.009 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.271 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.548 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.890 | 62 | 32 | 0 | within |
| notice-burst-6 | 6.173 | 62 | 32 | 0 | within |
| notice-burst-6 | 6.431 | 62 | 32 | 0 | within |
| notice-burst-6 | 6.708 | 62 | 32 | 0 | within |
| notice-burst-6 | 18.009 | 62 | 32 | 0 | within |
| notice-burst-6 | 21.639 | 62 | 32 | 0 | within |
| notice-burst-6 | 21.903 | 62 | 32 | 0 | within |
| notice-burst-6 | 22.179 | 62 | 32 | 0 | within |
| notice-burst-6 | 22.435 | 62 | 32 | 0 | within |
| notice-burst-6 | 23.582 | 62 | 32 | 0 | within |
| notice-burst-6 | 23.853 | 62 | 32 | 0 | within |
| notice-burst-6 | 24.132 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.215 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.522 | 62 | 32 | 0 | within |
| notice-burst-6 | 24.386 | 62 | 32 | 0 | within |
| notice-burst-6 | 25.517 | 62 | 32 | 0 | within |
| notice-burst-6 | 25.781 | 62 | 32 | 0 | within |
| notice-burst-6 | 26.055 | 62 | 32 | 0 | within |
| notice-burst-6 | 26.307 | 62 | 32 | 0 | within |
| notice-burst-6 | 27.660 | 62 | 32 | 0 | within |
| notice-burst-6 | 27.928 | 62 | 32 | 0 | within |
| notice-burst-6 | 28.205 | 62 | 32 | 0 | within |
| notice-burst-6 | 28.459 | 62 | 32 | 0 | within |
| notice-burst-6 | 29.573 | 62 | 32 | 0 | within |
| notice-burst-6 | 29.824 | 62 | 32 | 0 | within |
| notice-burst-6 | 30.060 | 62 | 32 | 0 | within |
| notice-burst-6 | 30.336 | 62 | 32 | 0 | within |
| notice-burst-6 | 31.723 | 62 | 32 | 0 | within |
| notice-burst-7 | 12.975 | 62 | 32 | 1 | within |
| notice-burst-7 | 16.615 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.304 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.592 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.125 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.411 | 62 | 32 | 1 | within |
| notice-burst-7 | 8.141 | 62 | 32 | 1 | within |
| notice-burst-7 | 20.114 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.862 | 62 | 32 | 1 | within |
| notice-burst-7 | 3.144 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.677 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.956 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.303 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.587 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.848 | 62 | 32 | 1 | within |
| notice-burst-7 | 6.127 | 62 | 32 | 1 | within |
| notice-burst-7 | 20.395 | 62 | 32 | 1 | within |
| notice-burst-7 | 20.670 | 62 | 32 | 1 | within |
| notice-burst-7 | 20.921 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.140 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.410 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.690 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.948 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.329 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.600 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.879 | 62 | 32 | 1 | within |
| notice-burst-7 | 25.133 | 62 | 32 | 1 | within |
| notice-burst-7 | 26.260 | 62 | 32 | 1 | within |
| notice-burst-7 | 26.524 | 62 | 32 | 1 | within |
| notice-burst-7 | 26.799 | 62 | 32 | 1 | within |
| notice-burst-7 | 27.050 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.168 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.435 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.713 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.967 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.313 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.564 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.801 | 62 | 32 | 1 | within |
| notice-burst-7 | 31.077 | 62 | 32 | 1 | within |
| notice-burst-7 | 32.254 | 62 | 32 | 1 | within |

Latest: 33.058 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 302 | 145,046 (1.450) | 32,565 (0.326) |
| notice-every-1 | 302 | 78,295 (0.783) | 32,565 (0.326) |
| notice-every-2 | 302 | 55,462 (0.555) | 32,565 (0.326) |
| notice-every-3 | 302 | 55,462 (0.555) | 32,565 (0.326) |
| notice-every-4 | 302 | 55,462 (0.555) | 32,565 (0.326) |
| notice-every-5 | 302 | 55,462 (0.555) | 32,565 (0.326) |
| notice-every-6 | 302 | 55,462 (0.555) | 32,565 (0.326) |
| notice-every-7 | 302 | 55,462 (0.555) | 32,565 (0.326) |
| notice-burst-0 | 311 | 67,959 (0.680) | 32,565 (0.326) |
| notice-burst-1 | 312 | 78,295 (0.783) | 32,565 (0.326) |
| notice-burst-2 | 311 | 68,292 (0.683) | 32,565 (0.326) |
| notice-burst-3 | 312 | 68,262 (0.683) | 32,565 (0.326) |
| notice-burst-4 | 311 | 68,475 (0.685) | 32,565 (0.326) |
| notice-burst-5 | 312 | 63,971 (0.640) | 32,565 (0.326) |
| notice-burst-6 | 311 | 64,133 (0.641) | 32,565 (0.326) |
| notice-burst-7 | 312 | 68,395 (0.684) | 32,565 (0.326) |

Longest pass that carries a step: 145,046 CPU cycles (1.450 ms), notice-every-0; longest step: 32,565 (0.326 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 228,184 | 2.282 | 62 | 66 | fits | 145,046 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 256,998 | 2.570 | 62 | 66 | fits | 145,046 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 407,608 | 4.076 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 436,027 | 4.360 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 609,820 | 6.098 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 638,180 | 6.382 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 810,130 | 8.101 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 838,523 | 8.385 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 283,911 | 2.839 | 62 | 66 | fits | 145,046 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 312,137 | 3.121 | 62 | 66 | fits | 145,046 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 462,586 | 4.626 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 490,511 | 4.905 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 664,525 | 6.645 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 692,219 | 6.922 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 864,687 | 8.647 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 892,150 | 8.921 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,009,227 | 10.092 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,037,397 | 10.374 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 1,062,532 | 10.625 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,089,991 | 10.900 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,209,439 | 12.094 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,238,318 | 12.383 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,264,182 | 12.642 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,292,011 | 12.920 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,404,633 | 14.046 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,433,154 | 14.332 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,458,684 | 14.587 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,486,142 | 14.861 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,620,350 | 16.203 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,648,560 | 16.486 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,673,805 | 16.738 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,701,418 | 17.014 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,811,135 | 18.111 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,839,514 | 18.395 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,865,033 | 18.650 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,892,711 | 18.927 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,052,370 | 20.524 | 62 | 66 | fits | 31,684 | 100 | 0.211 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,408,462 | 24.085 | 62 | 66 | fits | 87,891 | 300 | 0.076 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,437,208 | 24.372 | 62 | 66 | fits | 87,891 | 300 | 0.076 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,465,452 | 24.655 | 62 | 66 | fits | 87,891 | 300 | 0.076 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 997,169 | 9.972 | 20 | 200 | fits | 169,261 | 153 | 0.496 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 976,901 | 9.769 | 20 | 20 | fits | 169,261 | 153 | 0.496 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 1,081,303 | 10.813 | 20 | 24 | fits | 98,842 | 77 | 0.484 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 937,426 | 9.374 | 20 | 50 | fits | 169,261 | 153 | 0.496 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 576,057 | 5.761 | 20 | 20 | fits | 134,453 | 59 | 0.529 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 139,188 | 1.392 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 185,584 | 1.856 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 229,544 | 2.295 | 62 | 66 | fits | 122,646 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 258,358 | 2.584 | 62 | 66 | fits | 122,646 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 409,816 | 4.098 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 438,235 | 4.382 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 612,122 | 6.121 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 640,482 | 6.405 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 812,408 | 8.124 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 840,801 | 8.408 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 285,271 | 2.853 | 62 | 66 | fits | 122,646 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 313,497 | 3.135 | 62 | 66 | fits | 122,646 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 464,794 | 4.648 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 492,719 | 4.927 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 666,827 | 6.668 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 694,521 | 6.945 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 866,965 | 8.670 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 894,428 | 8.944 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 1,011,505 | 10.115 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 1,039,675 | 10.397 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 1,064,810 | 10.648 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 1,092,269 | 10.923 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 1,211,720 | 12.117 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 1,240,599 | 12.406 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 1,266,463 | 12.665 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 1,294,292 | 12.943 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 1,406,911 | 14.069 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 1,435,432 | 14.354 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 1,460,962 | 14.610 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 1,488,420 | 14.884 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 1,622,642 | 16.226 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 1,650,852 | 16.509 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 1,676,097 | 16.761 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 1,703,710 | 17.037 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 1,813,427 | 18.134 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 1,841,806 | 18.418 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 1,867,325 | 18.673 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 1,895,003 | 18.950 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 2,024,761 | 20.248 | 62 | 66 | fits | 111,776 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 2,048,669 | 20.487 | 62 | 66 | fits | 111,776 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 2,076,977 | 20.770 | 62 | 66 | fits | 111,776 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 2,105,291 | 21.053 | 62 | 66 | fits | 111,776 | 399 | 0.065 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if1` | 854,499 | 8.545 | 20 | 200 | fits | 164,496 | 185 | 0.520 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 1,001,879 | 10.019 | 20 | 20 | fits | 167,648 | 127 | 0.492 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if1` | 1,088,564 | 10.886 | 20 | 24 | fits | 81,606 | 64 | 0.523 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 794,756 | 7.948 | 20 | 50 | fits | 164,496 | 185 | 0.520 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if1` | 587,213 | 5.872 | 20 | 20 | fits | 131,040 | 52 | 0.475 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 111,972 | 1.120 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if1` | 158,505 | 1.585 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 410,875 | 4.109 | 62 | 66 | fits | 119,202 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 439,167 | 4.392 | 62 | 66 | fits | 119,202 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 612,649 | 6.126 | 62 | 66 | fits | 118,965 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 640,977 | 6.410 | 62 | 66 | fits | 118,965 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 813,437 | 8.134 | 62 | 66 | fits | 118,161 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 841,941 | 8.419 | 62 | 66 | fits | 118,161 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 231,428 | 2.314 | 62 | 66 | fits | 123,982 | 401 | 0.096 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 261,079 | 2.611 | 62 | 66 | fits | 123,982 | 401 | 0.096 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 287,977 | 2.880 | 62 | 66 | fits | 123,982 | 401 | 0.096 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 316,203 | 3.162 | 62 | 66 | fits | 123,982 | 401 | 0.096 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 465,647 | 4.656 | 62 | 66 | fits | 119,202 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 493,572 | 4.936 | 62 | 66 | fits | 119,202 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 667,372 | 6.674 | 62 | 66 | fits | 118,965 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 695,066 | 6.951 | 62 | 66 | fits | 118,965 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 868,105 | 8.681 | 62 | 66 | fits | 118,161 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 895,568 | 8.956 | 62 | 66 | fits | 118,161 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 1,012,724 | 10.127 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 1,040,894 | 10.409 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 1,066,029 | 10.660 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 1,093,488 | 10.935 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 1,212,905 | 12.129 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 1,241,784 | 12.418 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 1,267,648 | 12.676 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 1,295,477 | 12.955 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 1,431,732 | 14.317 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 1,460,253 | 14.603 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 1,485,783 | 14.858 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 1,513,241 | 15.132 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 1,623,897 | 16.239 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 1,652,107 | 16.521 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 1,677,352 | 16.774 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 1,704,965 | 17.050 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 1,814,637 | 18.146 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 1,843,016 | 18.430 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 1,868,535 | 18.685 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 1,896,213 | 18.962 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 2,026,235 | 20.262 | 62 | 66 | fits | 111,777 | 399 | 0.064 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 2,050,144 | 20.501 | 62 | 66 | fits | 111,777 | 399 | 0.064 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 2,078,452 | 20.785 | 62 | 66 | fits | 111,777 | 399 | 0.064 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 2,106,766 | 21.068 | 62 | 66 | fits | 111,777 | 399 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if1` | 439,637 | 4.396 | 20 | 200 | fits | 144,626 | 122 | 0.375 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 971,145 | 9.711 | 20 | 20 | fits | 167,628 | 145 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if1` | 1,075,336 | 10.753 | 20 | 24 | fits | 98,700 | 77 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 931,670 | 9.317 | 20 | 50 | fits | 167,628 | 145 | 0.509 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if1` | 578,262 | 5.783 | 20 | 20 | fits | 134,301 | 57 | 0.531 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 129,399 | 1.294 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if1` | 175,795 | 1.758 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 229,465 | 2.295 | 62 | 66 | fits | 122,565 | 403 | 0.096 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 258,198 | 2.582 | 62 | 66 | fits | 122,565 | 403 | 0.096 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 409,901 | 4.099 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 438,320 | 4.383 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 611,432 | 6.114 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 639,792 | 6.398 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 811,762 | 8.118 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 840,155 | 8.402 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 285,111 | 2.851 | 62 | 66 | fits | 122,565 | 403 | 0.096 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 313,337 | 3.133 | 62 | 66 | fits | 122,565 | 403 | 0.096 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 464,879 | 4.649 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 492,804 | 4.928 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 666,137 | 6.661 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 693,831 | 6.938 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 866,319 | 8.663 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 893,782 | 8.938 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 1,010,859 | 10.109 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 1,039,029 | 10.390 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 1,064,164 | 10.642 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 1,091,623 | 10.916 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 1,211,040 | 12.110 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 1,239,919 | 12.399 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 1,265,783 | 12.658 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 1,293,612 | 12.936 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 1,429,867 | 14.299 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 1,458,388 | 14.584 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 1,483,918 | 14.839 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 1,511,376 | 15.114 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 1,622,032 | 16.220 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 1,650,242 | 16.502 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 1,675,487 | 16.755 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 1,703,100 | 17.031 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 1,812,772 | 18.128 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 1,841,151 | 18.412 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 1,866,670 | 18.667 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 1,894,348 | 18.943 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 2,024,370 | 20.244 | 62 | 66 | fits | 111,698 | 399 | 0.064 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 2,048,200 | 20.482 | 62 | 66 | fits | 111,698 | 399 | 0.064 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 2,076,508 | 20.765 | 62 | 66 | fits | 111,698 | 399 | 0.064 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 2,104,822 | 21.048 | 62 | 66 | fits | 111,698 | 399 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if1` | 1,040,301 | 10.403 | 20 | 200 | fits | 161,933 | 129 | 0.513 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 1,138,517 | 11.385 | 20 | 20 | fits | 93,230 | 71 | 0.580 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if1` | 1,118,313 | 11.183 | 20 | 24 | fits | 93,230 | 71 | 0.580 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 980,558 | 9.806 | 20 | 50 | fits | 161,933 | 129 | 0.513 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if1` | 604,849 | 6.048 | 20 | 20 | fits | 131,154 | 52 | 0.477 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 97,191 | 0.972 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if1` | 143,613 | 1.436 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 229,544 | 2.295 | 62 | 66 | fits | 122,593 | 403 | 0.095 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 258,305 | 2.583 | 62 | 66 | fits | 122,593 | 403 | 0.095 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 410,027 | 4.100 | 62 | 66 | fits | 119,807 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 438,477 | 4.385 | 62 | 66 | fits | 119,807 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 612,364 | 6.124 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 640,724 | 6.407 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 812,650 | 8.127 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 841,043 | 8.410 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 285,218 | 2.852 | 62 | 66 | fits | 122,593 | 403 | 0.095 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 313,444 | 3.134 | 62 | 66 | fits | 122,593 | 403 | 0.095 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 465,036 | 4.650 | 62 | 66 | fits | 119,807 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 492,961 | 4.930 | 62 | 66 | fits | 119,807 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 667,069 | 6.671 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 694,763 | 6.948 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 867,207 | 8.672 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 894,670 | 8.947 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 1,011,747 | 10.117 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 1,039,917 | 10.399 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 1,065,052 | 10.651 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 1,092,511 | 10.925 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 1,211,962 | 12.120 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 1,240,841 | 12.408 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 1,266,705 | 12.667 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 1,294,534 | 12.945 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 1,407,153 | 14.072 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 1,435,674 | 14.357 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 1,461,204 | 14.612 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 1,488,662 | 14.887 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 1,622,620 | 16.226 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 1,650,830 | 16.508 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 1,676,075 | 16.761 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 1,703,688 | 17.037 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 1,813,405 | 18.134 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 1,841,784 | 18.418 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 1,867,303 | 18.673 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 1,894,981 | 18.950 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 2,054,824 | 20.548 | 62 | 66 | fits | 31,684 | 100 | 0.211 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 2,411,119 | 24.111 | 62 | 66 | fits | 87,826 | 300 | 0.076 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 2,439,865 | 24.399 | 62 | 66 | fits | 87,826 | 300 | 0.076 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 2,468,109 | 24.681 | 62 | 66 | fits | 87,826 | 300 | 0.076 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if1` | 868,785 | 8.688 | 20 | 200 | fits | 164,762 | 181 | 0.526 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 1,014,167 | 10.142 | 20 | 20 | fits | 165,650 | 115 | 0.499 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if1` | 1,100,809 | 11.008 | 20 | 24 | fits | 81,567 | 64 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 809,042 | 8.090 | 20 | 50 | fits | 164,762 | 181 | 0.526 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if1` | 600,908 | 6.009 | 20 | 20 | fits | 131,116 | 52 | 0.475 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 103,318 | 1.033 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if1` | 149,851 | 1.499 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 410,162 | 4.102 | 62 | 66 | fits | 119,451 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 438,454 | 4.385 | 62 | 66 | fits | 119,451 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 229,754 | 2.298 | 62 | 66 | fits | 123,328 | 403 | 0.095 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 258,904 | 2.589 | 62 | 66 | fits | 123,328 | 403 | 0.095 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 612,493 | 6.125 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 640,853 | 6.409 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 812,782 | 8.128 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 841,175 | 8.412 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 285,867 | 2.859 | 62 | 66 | fits | 123,328 | 403 | 0.095 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 314,093 | 3.141 | 62 | 66 | fits | 123,328 | 403 | 0.095 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 465,013 | 4.650 | 62 | 66 | fits | 119,451 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 492,938 | 4.929 | 62 | 66 | fits | 119,451 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 667,198 | 6.672 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 694,892 | 6.949 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 867,339 | 8.673 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 894,802 | 8.948 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 1,011,879 | 10.119 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 1,040,049 | 10.400 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 1,065,184 | 10.652 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 1,092,643 | 10.926 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 1,212,115 | 12.121 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 1,240,994 | 12.410 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 1,266,858 | 12.669 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 1,294,687 | 12.947 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 1,430,939 | 14.309 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 1,459,460 | 14.595 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 1,484,990 | 14.850 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 1,512,448 | 15.124 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 1,623,154 | 16.232 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 1,651,364 | 16.514 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 1,676,609 | 16.766 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 1,704,222 | 17.042 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 1,813,908 | 18.139 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 1,842,287 | 18.423 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 1,867,806 | 18.678 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 1,895,484 | 18.955 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 2,025,506 | 20.255 | 62 | 66 | fits | 111,776 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 2,049,414 | 20.494 | 62 | 66 | fits | 111,776 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 2,077,722 | 20.777 | 62 | 66 | fits | 111,776 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 2,106,036 | 21.060 | 62 | 66 | fits | 111,776 | 399 | 0.065 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if1` | 1,050,641 | 10.506 | 20 | 200 | fits | 161,938 | 125 | 0.531 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 1,030,373 | 10.304 | 20 | 20 | fits | 161,938 | 125 | 0.531 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if1` | 1,110,530 | 11.105 | 20 | 24 | fits | 79,902 | 58 | 0.521 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 990,898 | 9.909 | 20 | 50 | fits | 161,938 | 125 | 0.531 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if1` | 607,187 | 6.072 | 20 | 20 | fits | 131,139 | 54 | 0.471 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 111,295 | 1.113 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if1` | 157,717 | 1.577 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 410,158 | 4.102 | 62 | 66 | fits | 119,341 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 438,419 | 4.384 | 62 | 66 | fits | 119,341 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 612,500 | 6.125 | 62 | 66 | fits | 118,965 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 640,828 | 6.408 | 62 | 66 | fits | 118,965 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 229,999 | 2.300 | 62 | 66 | fits | 123,491 | 403 | 0.096 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 259,264 | 2.593 | 62 | 66 | fits | 123,491 | 403 | 0.096 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 812,804 | 8.128 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 841,197 | 8.412 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 286,033 | 2.860 | 62 | 66 | fits | 123,491 | 403 | 0.096 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 314,259 | 3.143 | 62 | 66 | fits | 123,491 | 403 | 0.096 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 464,899 | 4.649 | 62 | 66 | fits | 119,341 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 492,824 | 4.928 | 62 | 66 | fits | 119,341 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 667,223 | 6.672 | 62 | 66 | fits | 118,965 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 694,917 | 6.949 | 62 | 66 | fits | 118,965 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 867,361 | 8.674 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 894,824 | 8.948 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 1,011,995 | 10.120 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 1,040,165 | 10.402 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 1,065,300 | 10.653 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,092,759 | 10.928 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,212,207 | 12.122 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,241,086 | 12.411 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,266,950 | 12.669 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,294,779 | 12.948 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,407,398 | 14.074 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,435,919 | 14.359 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,461,449 | 14.614 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,488,907 | 14.889 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,623,115 | 16.231 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,651,325 | 16.513 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,676,570 | 16.766 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,704,183 | 17.042 | 62 | 66 | fits | 114,856 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,813,900 | 18.139 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,842,279 | 18.423 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,867,798 | 18.678 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,895,476 | 18.955 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,055,129 | 20.551 | 62 | 66 | fits | 31,684 | 100 | 0.211 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,411,470 | 24.115 | 62 | 66 | fits | 87,891 | 300 | 0.076 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,440,216 | 24.402 | 62 | 66 | fits | 87,891 | 300 | 0.076 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,468,460 | 24.685 | 62 | 66 | fits | 87,891 | 300 | 0.076 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if1` | 835,921 | 8.359 | 20 | 200 | fits | 166,987 | 157 | 0.539 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 981,252 | 9.813 | 20 | 20 | fits | 165,599 | 141 | 0.500 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if1` | 1,078,648 | 10.786 | 20 | 24 | fits | 96,817 | 71 | 0.473 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 941,777 | 9.418 | 20 | 50 | fits | 165,599 | 141 | 0.500 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if1` | 587,166 | 5.872 | 20 | 20 | fits | 136,758 | 63 | 0.539 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 103,630 | 1.036 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if1` | 150,081 | 1.501 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 229,582 | 2.296 | 62 | 66 | fits | 122,646 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 258,396 | 2.584 | 62 | 66 | fits | 122,646 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 410,118 | 4.101 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 438,537 | 4.385 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 612,424 | 6.124 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 640,784 | 6.408 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 812,710 | 8.127 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 841,103 | 8.411 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 285,309 | 2.853 | 62 | 66 | fits | 122,646 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 313,535 | 3.135 | 62 | 66 | fits | 122,646 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 465,096 | 4.651 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 493,021 | 4.930 | 62 | 66 | fits | 119,776 | 401 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 667,129 | 6.671 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 694,823 | 6.948 | 62 | 66 | fits | 118,735 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 867,267 | 8.673 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 894,730 | 8.947 | 62 | 66 | fits | 117,695 | 402 | 0.073 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 1,011,807 | 10.118 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 1,039,977 | 10.400 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 1,065,112 | 10.651 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 1,092,571 | 10.926 | 62 | 66 | fits | 116,440 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 1,212,022 | 12.120 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 1,240,901 | 12.409 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 1,266,765 | 12.668 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 1,294,594 | 12.946 | 62 | 66 | fits | 117,737 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 1,407,213 | 14.072 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 1,435,734 | 14.357 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 1,461,264 | 14.613 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 1,488,722 | 14.887 | 62 | 66 | fits | 115,752 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 1,622,680 | 16.227 | 62 | 66 | fits | 114,853 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 1,650,887 | 16.509 | 62 | 66 | fits | 114,853 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 1,676,132 | 16.761 | 62 | 66 | fits | 114,853 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 1,703,745 | 17.037 | 62 | 66 | fits | 114,853 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 1,813,462 | 18.135 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 1,841,841 | 18.418 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 1,867,360 | 18.674 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 1,895,038 | 18.950 | 62 | 66 | fits | 115,320 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 2,054,952 | 20.550 | 62 | 66 | fits | 31,684 | 100 | 0.211 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 2,411,228 | 24.112 | 62 | 66 | fits | 87,826 | 300 | 0.076 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 2,439,974 | 24.400 | 62 | 66 | fits | 87,826 | 300 | 0.076 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 2,468,218 | 24.682 | 62 | 66 | fits | 87,826 | 300 | 0.076 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if1` | 900,101 | 9.001 | 20 | 200 | fits | 173,242 | 175 | 0.535 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 1,039,304 | 10.393 | 20 | 20 | fits | 159,471 | 122 | 0.528 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if1` | 1,097,157 | 10.972 | 20 | 24 | fits | 78,057 | 53 | 0.506 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 999,829 | 9.998 | 20 | 50 | fits | 159,471 | 122 | 0.528 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if1` | 619,094 | 6.191 | 20 | 20 | fits | 131,159 | 54 | 0.474 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 115,828 | 1.158 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if1` | 162,195 | 1.622 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 158,114 | 1.581 | 62 | 66 | fits | 152,353 | 411 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 186,621 | 1.866 | 62 | 66 | fits | 152,353 | 411 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 284,472 | 2.845 | 62 | 66 | fits | 118,418 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 312,715 | 3.127 | 62 | 66 | fits | 118,418 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 466,664 | 4.667 | 62 | 66 | fits | 142,572 | 411 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 494,995 | 4.950 | 62 | 66 | fits | 142,572 | 411 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 872,722 | 8.727 | 62 | 66 | fits | 37,545 | 103 | 0.308 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 1,367,205 | 13.672 | 62 | 66 | fits | 36,818 | 102 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 1,794,854 | 17.949 | 62 | 66 | fits | 35,875 | 101 | 0.258 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 2,158,018 | 21.580 | 62 | 66 | fits | 117,102 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 339,440 | 3.394 | 62 | 66 | fits | 118,418 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 367,615 | 3.676 | 62 | 66 | fits | 118,418 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 521,515 | 5.215 | 62 | 66 | fits | 142,572 | 411 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 549,440 | 5.494 | 62 | 66 | fits | 142,572 | 411 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 584,083 | 5.841 | 62 | 66 | fits | 116,865 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 612,576 | 6.126 | 62 | 66 | fits | 116,865 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 638,735 | 6.387 | 62 | 66 | fits | 116,865 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 666,660 | 6.667 | 62 | 66 | fits | 116,865 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 2,184,540 | 21.845 | 62 | 66 | fits | 117,102 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 2,212,138 | 22.121 | 62 | 66 | fits | 117,102 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 2,237,742 | 22.377 | 62 | 66 | fits | 117,102 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 2,352,576 | 23.526 | 62 | 66 | fits | 116,410 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 2,379,697 | 23.797 | 62 | 66 | fits | 116,410 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 2,407,593 | 24.076 | 62 | 66 | fits | 116,410 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 215,186 | 2.152 | 62 | 66 | fits | 152,353 | 411 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 245,872 | 2.459 | 62 | 66 | fits | 152,353 | 411 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 2,432,990 | 24.330 | 62 | 66 | fits | 116,410 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 2,569,711 | 25.697 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 2,596,113 | 25.961 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 2,623,579 | 26.236 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,648,749 | 26.487 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,760,607 | 27.606 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,787,312 | 27.873 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,815,057 | 28.151 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 2,840,458 | 28.405 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 2,974,817 | 29.748 | 62 | 66 | fits | 111,694 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 2,999,941 | 29.999 | 62 | 66 | fits | 111,694 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 3,023,540 | 30.235 | 62 | 66 | fits | 111,694 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 3,051,196 | 30.512 | 62 | 66 | fits | 111,694 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 3,167,538 | 31.675 | 62 | 66 | fits | 35,039 | 103 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 1,167,088 | 11.671 | 20 | 200 | fits | 153,620 | 113 | 0.523 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,146,820 | 11.468 | 20 | 20 | fits | 153,620 | 113 | 0.523 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 1,200,979 | 12.010 | 20 | 24 | fits | 74,363 | 52 | 0.503 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 953,725 | 9.537 | 20 | 50 | fits | 163,498 | 172 | 0.502 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 566,343 | 5.663 | 20 | 20 | fits | 136,259 | 58 | 0.500 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 411,302 | 4.113 | 62 | 66 | fits | 142,103 | 411 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 439,553 | 4.396 | 62 | 66 | fits | 142,103 | 411 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 465,609 | 4.656 | 62 | 66 | fits | 142,103 | 411 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 493,230 | 4.932 | 62 | 66 | fits | 142,103 | 411 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 528,173 | 5.282 | 62 | 66 | fits | 117,063 | 402 | 0.041 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 556,331 | 5.563 | 62 | 66 | fits | 117,063 | 402 | 0.041 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 811,198 | 8.112 | 62 | 66 | fits | 36,841 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 1,296,702 | 12.967 | 62 | 66 | fits | 38,715 | 102 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 1,658,476 | 16.585 | 62 | 66 | fits | 35,967 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 2,035,210 | 20.352 | 62 | 66 | fits | 117,954 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 2,062,755 | 20.628 | 62 | 66 | fits | 117,954 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 2,090,239 | 20.902 | 62 | 66 | fits | 117,954 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 2,116,066 | 21.161 | 62 | 66 | fits | 117,954 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 2,214,697 | 22.147 | 62 | 66 | fits | 117,809 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 226,533 | 2.265 | 62 | 66 | fits | 126,209 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 256,696 | 2.567 | 62 | 66 | fits | 126,209 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 284,211 | 2.842 | 62 | 66 | fits | 126,209 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 313,310 | 3.133 | 62 | 66 | fits | 126,209 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 582,416 | 5.824 | 62 | 66 | fits | 117,063 | 402 | 0.041 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 610,799 | 6.108 | 62 | 66 | fits | 117,063 | 402 | 0.041 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 2,241,842 | 22.418 | 62 | 66 | fits | 117,809 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 2,269,870 | 22.699 | 62 | 66 | fits | 117,809 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 2,295,675 | 22.957 | 62 | 66 | fits | 117,809 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 2,410,651 | 24.107 | 62 | 66 | fits | 116,417 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 2,437,770 | 24.378 | 62 | 66 | fits | 116,417 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 2,465,666 | 24.657 | 62 | 66 | fits | 116,417 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 2,491,072 | 24.911 | 62 | 66 | fits | 116,417 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 2,627,060 | 26.271 | 62 | 66 | fits | 114,611 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 2,653,462 | 26.535 | 62 | 66 | fits | 114,611 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 2,680,924 | 26.809 | 62 | 66 | fits | 114,611 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 2,706,060 | 27.061 | 62 | 66 | fits | 114,611 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 2,818,045 | 28.180 | 62 | 66 | fits | 115,361 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,844,651 | 28.447 | 62 | 66 | fits | 115,361 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 2,872,396 | 28.724 | 62 | 66 | fits | 115,361 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 2,897,797 | 28.978 | 62 | 66 | fits | 115,361 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 3,032,326 | 30.323 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 3,057,450 | 30.575 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 3,081,128 | 30.811 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 3,108,784 | 31.088 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 3,226,569 | 32.266 | 62 | 66 | fits | 35,030 | 102 | 0.134 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if1` | 1,046,656 | 10.467 | 20 | 200 | fits | 157,275 | 125 | 0.529 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 1,026,388 | 10.264 | 20 | 20 | fits | 157,275 | 125 | 0.529 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if1` | 1,137,111 | 11.371 | 20 | 24 | fits | 94,960 | 75 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 986,913 | 9.869 | 20 | 50 | fits | 157,275 | 125 | 0.529 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if1` | 600,714 | 6.007 | 20 | 20 | fits | 125,818 | 54 | 0.518 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 451,739 | 4.517 | 62 | 66 | fits | 118,918 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 479,909 | 4.799 | 62 | 66 | fits | 118,918 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 505,965 | 5.060 | 62 | 66 | fits | 118,918 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 533,586 | 5.336 | 62 | 66 | fits | 118,918 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 740,625 | 7.406 | 62 | 66 | fits | 36,263 | 101 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 1,094,517 | 10.945 | 62 | 66 | fits | 38,855 | 102 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 1,599,576 | 15.996 | 62 | 66 | fits | 36,001 | 100 | 0.270 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 1,959,980 | 19.600 | 62 | 66 | fits | 117,988 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 1,987,684 | 19.877 | 62 | 66 | fits | 117,988 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 2,015,168 | 20.152 | 62 | 66 | fits | 117,988 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 2,040,998 | 20.410 | 62 | 66 | fits | 117,988 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 2,163,982 | 21.640 | 62 | 66 | fits | 118,056 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 2,191,826 | 21.918 | 62 | 66 | fits | 118,056 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 2,219,391 | 22.194 | 62 | 66 | fits | 118,056 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 159,516 | 1.595 | 62 | 66 | fits | 155,596 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 189,640 | 1.896 | 62 | 66 | fits | 155,596 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 288,951 | 2.890 | 62 | 66 | fits | 122,308 | 402 | 0.038 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 318,653 | 3.187 | 62 | 66 | fits | 122,308 | 402 | 0.038 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 345,296 | 3.453 | 62 | 66 | fits | 122,308 | 402 | 0.038 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 374,371 | 3.744 | 62 | 66 | fits | 122,308 | 402 | 0.038 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 2,245,056 | 22.451 | 62 | 66 | fits | 118,056 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 2,359,979 | 23.600 | 62 | 66 | fits | 117,298 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 2,387,100 | 23.871 | 62 | 66 | fits | 117,298 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 2,415,049 | 24.150 | 62 | 66 | fits | 117,298 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 2,440,847 | 24.408 | 62 | 66 | fits | 117,298 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 2,554,497 | 25.545 | 62 | 66 | fits | 115,216 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 218,113 | 2.181 | 62 | 66 | fits | 155,596 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 248,896 | 2.489 | 62 | 66 | fits | 155,596 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 2,581,356 | 25.814 | 62 | 66 | fits | 115,216 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 2,608,818 | 26.088 | 62 | 66 | fits | 115,216 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 2,633,954 | 26.340 | 62 | 66 | fits | 115,216 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 2,769,637 | 27.696 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 2,796,342 | 27.963 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 2,824,087 | 28.241 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 2,849,488 | 28.495 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 2,960,767 | 29.608 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 2,985,891 | 29.859 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 3,009,569 | 30.096 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 3,037,225 | 30.372 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 3,153,313 | 31.533 | 62 | 66 | fits | 34,943 | 102 | 0.127 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if1` | 1,046,948 | 10.469 | 20 | 200 | fits | 163,201 | 133 | 0.517 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 1,026,680 | 10.267 | 20 | 20 | fits | 163,201 | 133 | 0.517 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if1` | 1,121,621 | 11.216 | 20 | 24 | fits | 79,144 | 62 | 0.534 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 987,205 | 9.872 | 20 | 50 | fits | 163,201 | 133 | 0.517 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if1` | 637,214 | 6.372 | 20 | 20 | fits | 140,372 | 65 | 0.546 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 532,912 | 5.329 | 62 | 66 | fits | 116,941 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 560,895 | 5.609 | 62 | 66 | fits | 116,941 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 818,115 | 8.181 | 62 | 66 | fits | 37,110 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,303,035 | 13.030 | 62 | 66 | fits | 38,556 | 102 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 1,661,686 | 16.617 | 62 | 66 | fits | 35,481 | 101 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 2,013,056 | 20.131 | 62 | 66 | fits | 118,163 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 2,040,457 | 20.405 | 62 | 66 | fits | 118,163 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 2,068,164 | 20.682 | 62 | 66 | fits | 118,163 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 226,618 | 2.266 | 62 | 66 | fits | 127,153 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 256,060 | 2.561 | 62 | 66 | fits | 127,153 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 413,877 | 4.139 | 62 | 66 | fits | 145,550 | 411 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 443,064 | 4.431 | 62 | 66 | fits | 145,550 | 411 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 469,808 | 4.698 | 62 | 66 | fits | 145,550 | 411 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 498,195 | 4.982 | 62 | 66 | fits | 145,550 | 411 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 587,339 | 5.873 | 62 | 66 | fits | 116,941 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 615,495 | 6.155 | 62 | 66 | fits | 116,941 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 2,094,358 | 20.944 | 62 | 66 | fits | 118,163 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 2,216,081 | 22.161 | 62 | 66 | fits | 116,221 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 2,242,536 | 22.425 | 62 | 66 | fits | 116,221 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 2,270,130 | 22.701 | 62 | 66 | fits | 116,221 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 2,295,700 | 22.957 | 62 | 66 | fits | 116,221 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 2,434,008 | 24.340 | 62 | 66 | fits | 116,575 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 284,263 | 2.843 | 62 | 66 | fits | 127,153 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 314,560 | 3.146 | 62 | 66 | fits | 127,153 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 2,461,206 | 24.612 | 62 | 66 | fits | 116,575 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 2,489,102 | 24.891 | 62 | 66 | fits | 116,575 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 2,514,508 | 25.145 | 62 | 66 | fits | 116,575 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 2,627,675 | 26.277 | 62 | 66 | fits | 114,611 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 2,654,077 | 26.541 | 62 | 66 | fits | 114,611 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 2,681,539 | 26.815 | 62 | 66 | fits | 114,611 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,706,675 | 27.067 | 62 | 66 | fits | 114,611 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,818,521 | 28.185 | 62 | 66 | fits | 115,361 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,845,127 | 28.451 | 62 | 66 | fits | 115,361 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 2,872,872 | 28.729 | 62 | 66 | fits | 115,361 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 2,898,273 | 28.983 | 62 | 66 | fits | 115,361 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 3,032,910 | 30.329 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 3,058,034 | 30.580 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 3,081,712 | 30.817 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 3,109,368 | 31.094 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 3,226,981 | 32.270 | 62 | 66 | fits | 35,030 | 102 | 0.134 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if1` | 894,997 | 8.950 | 20 | 200 | fits | 167,778 | 170 | 0.530 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 1,029,787 | 10.298 | 20 | 20 | fits | 155,058 | 123 | 0.530 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if1` | 1,139,796 | 11.398 | 20 | 24 | fits | 94,732 | 75 | 0.479 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 990,312 | 9.903 | 20 | 50 | fits | 155,058 | 123 | 0.530 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if1` | 606,895 | 6.069 | 20 | 20 | fits | 125,674 | 54 | 0.518 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 660,982 | 6.610 | 62 | 66 | fits | 117,476 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 689,013 | 6.890 | 62 | 66 | fits | 117,476 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 951,094 | 9.511 | 62 | 66 | fits | 37,812 | 101 | 0.308 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,447,816 | 14.478 | 62 | 66 | fits | 36,982 | 102 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 1,877,140 | 18.771 | 62 | 66 | fits | 35,651 | 101 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 2,241,209 | 22.412 | 62 | 66 | fits | 118,534 | 400 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 2,268,755 | 22.688 | 62 | 66 | fits | 118,534 | 400 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 2,296,543 | 22.965 | 62 | 66 | fits | 118,534 | 400 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 227,998 | 2.280 | 62 | 66 | fits | 154,461 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 257,346 | 2.573 | 62 | 66 | fits | 154,461 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 2,322,605 | 23.226 | 62 | 66 | fits | 118,534 | 400 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 2,437,767 | 24.378 | 62 | 66 | fits | 116,236 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 356,293 | 3.563 | 62 | 66 | fits | 121,147 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 385,533 | 3.855 | 62 | 66 | fits | 121,147 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 412,353 | 4.124 | 62 | 66 | fits | 121,147 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 440,990 | 4.410 | 62 | 66 | fits | 121,147 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 541,703 | 5.417 | 62 | 66 | fits | 146,184 | 411 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 570,999 | 5.710 | 62 | 66 | fits | 146,184 | 411 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 597,303 | 5.973 | 62 | 66 | fits | 146,184 | 411 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 625,917 | 6.259 | 62 | 66 | fits | 146,184 | 411 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 715,528 | 7.155 | 62 | 66 | fits | 117,476 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 744,282 | 7.443 | 62 | 66 | fits | 117,476 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 2,464,576 | 24.646 | 62 | 66 | fits | 116,236 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 2,492,472 | 24.925 | 62 | 66 | fits | 116,236 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 285,911 | 2.859 | 62 | 66 | fits | 154,461 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 316,597 | 3.166 | 62 | 66 | fits | 154,461 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 2,517,869 | 25.179 | 62 | 66 | fits | 116,236 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 2,631,088 | 26.311 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 2,657,490 | 26.575 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 2,684,956 | 26.850 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 2,710,126 | 27.101 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 2,845,459 | 28.455 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 2,872,164 | 28.722 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 2,899,909 | 28.999 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 2,925,310 | 29.253 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 3,036,683 | 30.367 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 3,061,807 | 30.618 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 3,085,485 | 30.855 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 3,113,141 | 31.131 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 3,229,246 | 32.292 | 62 | 66 | fits | 35,039 | 103 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if1` | 1,023,790 | 10.238 | 20 | 200 | fits | 164,762 | 171 | 0.512 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 1,157,919 | 11.579 | 20 | 20 | fits | 154,397 | 124 | 0.526 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if1` | 1,212,091 | 12.121 | 20 | 24 | fits | 74,376 | 52 | 0.503 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 1,118,444 | 11.184 | 20 | 50 | fits | 154,397 | 124 | 0.526 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if1` | 572,791 | 5.728 | 20 | 20 | fits | 136,482 | 58 | 0.500 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 824,779 | 8.248 | 62 | 66 | fits | 36,281 | 101 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,310,585 | 13.106 | 62 | 66 | fits | 38,894 | 102 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,755,062 | 17.551 | 62 | 66 | fits | 35,708 | 101 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 2,116,699 | 21.167 | 62 | 66 | fits | 118,265 | 400 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 226,631 | 2.266 | 62 | 66 | fits | 125,934 | 402 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 255,656 | 2.557 | 62 | 66 | fits | 125,934 | 402 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 412,479 | 4.125 | 62 | 66 | fits | 143,791 | 411 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 441,336 | 4.413 | 62 | 66 | fits | 143,791 | 411 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 468,009 | 4.680 | 62 | 66 | fits | 143,791 | 411 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 495,934 | 4.959 | 62 | 66 | fits | 143,791 | 411 | 0.095 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 2,144,429 | 21.444 | 62 | 66 | fits | 118,265 | 400 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 2,171,915 | 21.719 | 62 | 66 | fits | 118,265 | 400 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 531,237 | 5.312 | 62 | 66 | fits | 118,205 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 559,913 | 5.599 | 62 | 66 | fits | 118,205 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 586,222 | 5.862 | 62 | 66 | fits | 118,205 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 614,378 | 6.144 | 62 | 66 | fits | 118,205 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 2,197,886 | 21.979 | 62 | 66 | fits | 118,265 | 400 | 0.081 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 2,319,375 | 23.194 | 62 | 66 | fits | 116,335 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 2,345,830 | 23.458 | 62 | 66 | fits | 116,335 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,373,428 | 23.734 | 62 | 66 | fits | 116,335 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 2,399,032 | 23.990 | 62 | 66 | fits | 116,335 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 2,513,629 | 25.136 | 62 | 66 | fits | 116,575 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 283,859 | 2.839 | 62 | 66 | fits | 125,934 | 402 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 314,156 | 3.142 | 62 | 66 | fits | 125,934 | 402 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 2,540,827 | 25.408 | 62 | 66 | fits | 116,575 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 2,568,723 | 25.687 | 62 | 66 | fits | 116,575 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 2,594,129 | 25.941 | 62 | 66 | fits | 116,575 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 2,707,269 | 27.073 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 2,733,671 | 27.337 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 2,761,137 | 27.611 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 2,786,307 | 27.863 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 2,921,376 | 29.214 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 2,948,081 | 29.481 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 2,975,826 | 29.758 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 3,001,227 | 30.012 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 3,112,600 | 31.126 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 3,137,724 | 31.377 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 3,161,402 | 31.614 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 3,189,058 | 31.891 | 62 | 66 | fits | 111,773 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 3,305,759 | 33.058 | 62 | 66 | fits | 35,024 | 102 | 0.134 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if1` | 1,071,722 | 10.717 | 20 | 200 | fits | 165,342 | 133 | 0.523 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 1,051,454 | 10.515 | 20 | 20 | fits | 165,342 | 133 | 0.523 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if1` | 1,108,001 | 11.080 | 20 | 24 | fits | 76,751 | 52 | 0.519 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 1,011,979 | 10.120 | 20 | 50 | fits | 165,342 | 133 | 0.523 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if1` | 619,542 | 6.195 | 20 | 20 | fits | 125,897 | 54 | 0.518 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 876,849 | 8.768 | 62 | 66 | fits | 37,595 | 101 | 0.312 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,372,949 | 13.729 | 62 | 66 | fits | 36,729 | 102 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 164,075 | 1.641 | 62 | 66 | fits | 153,173 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 192,890 | 1.929 | 62 | 66 | fits | 153,173 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 290,781 | 2.908 | 62 | 66 | fits | 117,822 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 319,193 | 3.192 | 62 | 66 | fits | 117,822 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 345,089 | 3.451 | 62 | 66 | fits | 117,822 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 373,025 | 3.730 | 62 | 66 | fits | 117,822 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 472,516 | 4.725 | 62 | 66 | fits | 142,345 | 411 | 0.096 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 500,888 | 5.009 | 62 | 66 | fits | 142,345 | 411 | 0.096 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 527,081 | 5.271 | 62 | 66 | fits | 142,345 | 411 | 0.096 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 554,775 | 5.548 | 62 | 66 | fits | 142,345 | 411 | 0.096 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 589,020 | 5.890 | 62 | 66 | fits | 115,949 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 617,282 | 6.173 | 62 | 66 | fits | 115,949 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 643,129 | 6.431 | 62 | 66 | fits | 115,949 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 670,823 | 6.708 | 62 | 66 | fits | 115,949 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 1,800,879 | 18.009 | 62 | 66 | fits | 35,726 | 101 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 2,163,921 | 21.639 | 62 | 66 | fits | 116,797 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 2,190,299 | 21.903 | 62 | 66 | fits | 116,797 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,217,897 | 22.179 | 62 | 66 | fits | 116,797 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,243,501 | 22.435 | 62 | 66 | fits | 116,797 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,358,200 | 23.582 | 62 | 66 | fits | 116,410 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 2,385,321 | 23.853 | 62 | 66 | fits | 116,410 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 2,413,217 | 24.132 | 62 | 66 | fits | 116,410 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 221,505 | 2.215 | 62 | 66 | fits | 153,173 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 252,191 | 2.522 | 62 | 66 | fits | 153,173 | 411 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 2,438,614 | 24.386 | 62 | 66 | fits | 116,410 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 2,551,675 | 25.517 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 2,578,077 | 25.781 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 2,605,543 | 26.055 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 2,630,713 | 26.307 | 62 | 66 | fits | 114,649 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 2,766,046 | 27.660 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 2,792,751 | 27.928 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 2,820,496 | 28.205 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 2,845,897 | 28.459 | 62 | 66 | fits | 115,460 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 2,957,270 | 29.573 | 62 | 66 | fits | 111,694 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,982,394 | 29.824 | 62 | 66 | fits | 111,694 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 3,005,993 | 30.060 | 62 | 66 | fits | 111,694 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 3,033,649 | 30.336 | 62 | 66 | fits | 111,694 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 3,172,312 | 31.723 | 62 | 66 | fits | 35,039 | 103 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if1` | 1,173,425 | 11.734 | 20 | 200 | fits | 155,072 | 127 | 0.515 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 1,153,157 | 11.532 | 20 | 20 | fits | 155,072 | 127 | 0.515 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if1` | 1,207,430 | 12.074 | 20 | 24 | fits | 74,477 | 52 | 0.506 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 1,113,682 | 11.137 | 20 | 50 | fits | 155,072 | 127 | 0.515 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if1` | 569,996 | 5.700 | 20 | 20 | fits | 136,289 | 58 | 0.501 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 1,297,534 | 12.975 | 62 | 66 | fits | 37,338 | 100 | 0.309 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,661,534 | 16.615 | 62 | 66 | fits | 36,460 | 102 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 230,401 | 2.304 | 62 | 66 | fits | 122,291 | 402 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 259,176 | 2.592 | 62 | 66 | fits | 122,291 | 402 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 412,511 | 4.125 | 62 | 66 | fits | 142,654 | 411 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 441,104 | 4.411 | 62 | 66 | fits | 142,654 | 411 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 814,052 | 8.141 | 62 | 66 | fits | 36,979 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 2,011,414 | 20.114 | 62 | 66 | fits | 117,005 | 400 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 286,223 | 2.862 | 62 | 66 | fits | 122,291 | 402 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 314,398 | 3.144 | 62 | 66 | fits | 122,291 | 402 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 467,672 | 4.677 | 62 | 66 | fits | 142,654 | 411 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 495,597 | 4.956 | 62 | 66 | fits | 142,654 | 411 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 530,291 | 5.303 | 62 | 66 | fits | 117,450 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 558,736 | 5.587 | 62 | 66 | fits | 117,450 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 584,814 | 5.848 | 62 | 66 | fits | 117,450 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 612,739 | 6.127 | 62 | 66 | fits | 117,450 | 402 | 0.036 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 2,039,470 | 20.395 | 62 | 66 | fits | 117,005 | 400 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 2,066,954 | 20.670 | 62 | 66 | fits | 117,005 | 400 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 2,092,053 | 20.921 | 62 | 66 | fits | 117,005 | 400 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 2,213,988 | 22.140 | 62 | 66 | fits | 117,361 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 2,241,014 | 22.410 | 62 | 66 | fits | 117,361 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 2,269,042 | 22.690 | 62 | 66 | fits | 117,361 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 2,294,768 | 22.948 | 62 | 66 | fits | 117,361 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 2,432,871 | 24.329 | 62 | 66 | fits | 116,388 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 2,460,015 | 24.600 | 62 | 66 | fits | 116,388 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 2,487,911 | 24.879 | 62 | 66 | fits | 116,388 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 2,513,317 | 25.133 | 62 | 66 | fits | 116,388 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 2,625,990 | 26.260 | 62 | 66 | fits | 114,582 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 2,652,417 | 26.524 | 62 | 66 | fits | 114,582 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 2,679,879 | 26.799 | 62 | 66 | fits | 114,582 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 2,705,015 | 27.050 | 62 | 66 | fits | 114,582 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 2,816,807 | 28.168 | 62 | 66 | fits | 115,431 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 2,843,537 | 28.435 | 62 | 66 | fits | 115,431 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 2,871,282 | 28.713 | 62 | 66 | fits | 115,431 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 2,896,683 | 28.967 | 62 | 66 | fits | 115,431 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 3,031,252 | 30.313 | 62 | 66 | fits | 111,719 | 398 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 3,056,376 | 30.564 | 62 | 66 | fits | 111,719 | 398 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 3,080,054 | 30.801 | 62 | 66 | fits | 111,719 | 398 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 3,107,710 | 31.077 | 62 | 66 | fits | 111,719 | 398 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 3,225,442 | 32.254 | 62 | 66 | fits | 35,100 | 103 | 0.134 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if1` | 1,048,852 | 10.489 | 20 | 200 | fits | 157,626 | 125 | 0.529 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 1,028,584 | 10.286 | 20 | 20 | fits | 157,626 | 125 | 0.529 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if1` | 1,138,568 | 11.386 | 20 | 24 | fits | 93,728 | 75 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 989,109 | 9.891 | 20 | 50 | fits | 157,626 | 125 | 0.529 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if1` | 602,440 | 6.024 | 20 | 20 | fits | 125,532 | 54 | 0.515 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
