### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 728 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-2.held.acmp.if0` (notice-every-2) | 9.069 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-every-2.held.adp.if0` (notice-every-2) | 7.917 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-7.held.aecp.if0` (notice-every-7) | 6.618 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-7.held.maap.if0` (notice-every-7) | 7.989 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-2.held.srp.if0` (notice-every-2) | 12.595 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-6.mrpdu.periodic.if0` (notice-every-6) | 1.163 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-3.notices.29.36.0.if0` (notice-burst-3) | 27.647 (27.899) | fits | 1 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1499 | 0 | 165,747 (1.657) | fits |
| notice-every-1 | 1501 | 0 | 165,747 (1.657) | fits |
| notice-every-2 | 1496 | 0 | 166,209 (1.662) | fits |
| notice-every-3 | 1500 | 0 | 165,754 (1.658) | fits |
| notice-every-4 | 1497 | 0 | 165,754 (1.658) | fits |
| notice-every-5 | 1503 | 0 | 165,747 (1.657) | fits |
| notice-every-6 | 1495 | 0 | 165,754 (1.658) | fits |
| notice-every-7 | 1503 | 0 | 165,747 (1.657) | fits |
| notice-burst-0 | 1172 | 0 | 170,182 (1.702) | fits |
| notice-burst-1 | 1168 | 0 | 165,773 (1.658) | fits |
| notice-burst-2 | 1186 | 0 | 165,773 (1.658) | fits |
| notice-burst-3 | 1172 | 0 | 170,338 (1.703) | fits |
| notice-burst-4 | 1187 | 0 | 170,574 (1.706) | fits |
| notice-burst-5 | 1163 | 0 | 165,773 (1.658) | fits |
| notice-burst-6 | 1163 | 0 | 165,802 (1.658) | fits |
| notice-burst-7 | 1187 | 0 | 170,209 (1.702) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 7.621 | 130 | 16 | 2 | within |
| notice-every-0 | 7.794 | 130 | 16 | 2 | within |
| notice-every-0 | 1.560 | 130 | 16 | 2 | within |
| notice-every-0 | 1.738 | 130 | 16 | 2 | within |
| notice-every-0 | 3.547 | 130 | 16 | 2 | within |
| notice-every-0 | 3.724 | 130 | 16 | 2 | within |
| notice-every-0 | 5.487 | 130 | 16 | 2 | within |
| notice-every-0 | 5.664 | 130 | 16 | 2 | within |
| notice-every-0 | 1.898 | 130 | 16 | 2 | within |
| notice-every-0 | 2.072 | 130 | 16 | 2 | within |
| notice-every-0 | 3.884 | 130 | 16 | 2 | within |
| notice-every-0 | 4.060 | 130 | 16 | 2 | within |
| notice-every-0 | 5.821 | 130 | 16 | 2 | within |
| notice-every-0 | 5.991 | 130 | 16 | 2 | within |
| notice-every-0 | 7.948 | 130 | 16 | 2 | within |
| notice-every-0 | 8.115 | 130 | 16 | 2 | within |
| notice-every-0 | 9.551 | 130 | 16 | 2 | within |
| notice-every-0 | 9.725 | 130 | 16 | 2 | within |
| notice-every-0 | 9.871 | 130 | 16 | 2 | within |
| notice-every-0 | 10.039 | 130 | 16 | 2 | within |
| notice-every-0 | 11.621 | 130 | 16 | 2 | within |
| notice-every-0 | 11.795 | 130 | 16 | 2 | within |
| notice-every-0 | 11.942 | 130 | 16 | 2 | within |
| notice-every-0 | 12.108 | 130 | 16 | 2 | within |
| notice-every-0 | 13.493 | 130 | 16 | 2 | within |
| notice-every-0 | 13.667 | 130 | 16 | 2 | within |
| notice-every-0 | 13.814 | 130 | 16 | 2 | within |
| notice-every-0 | 13.981 | 130 | 16 | 2 | within |
| notice-every-0 | 15.577 | 130 | 16 | 2 | within |
| notice-every-0 | 15.750 | 130 | 16 | 2 | within |
| notice-every-0 | 15.897 | 130 | 16 | 2 | within |
| notice-every-0 | 16.064 | 130 | 16 | 2 | within |
| notice-every-0 | 17.606 | 130 | 16 | 2 | within |
| notice-every-0 | 17.779 | 130 | 16 | 2 | within |
| notice-every-0 | 17.926 | 130 | 16 | 2 | within |
| notice-every-0 | 18.093 | 130 | 16 | 2 | within |
| notice-every-0 | 23.053 | 130 | 16 | 2 | within |
| notice-every-0 | 23.177 | 130 | 16 | 2 | within |
| notice-every-0 | 23.347 | 130 | 16 | 2 | within |
| notice-every-0 | 23.518 | 130 | 16 | 2 | within |
| notice-every-1 | 7.667 | 130 | 16 | 2 | within |
| notice-every-1 | 7.841 | 130 | 16 | 2 | within |
| notice-every-1 | 1.560 | 130 | 16 | 2 | within |
| notice-every-1 | 1.738 | 130 | 16 | 2 | within |
| notice-every-1 | 3.552 | 130 | 16 | 2 | within |
| notice-every-1 | 3.729 | 130 | 16 | 2 | within |
| notice-every-1 | 5.491 | 130 | 16 | 2 | within |
| notice-every-1 | 5.667 | 130 | 16 | 2 | within |
| notice-every-1 | 1.899 | 130 | 16 | 2 | within |
| notice-every-1 | 2.072 | 130 | 16 | 2 | within |
| notice-every-1 | 3.888 | 130 | 16 | 2 | within |
| notice-every-1 | 4.064 | 130 | 16 | 2 | within |
| notice-every-1 | 5.824 | 130 | 16 | 2 | within |
| notice-every-1 | 5.994 | 130 | 16 | 2 | within |
| notice-every-1 | 7.994 | 130 | 16 | 2 | within |
| notice-every-1 | 8.161 | 130 | 16 | 2 | within |
| notice-every-1 | 9.589 | 130 | 16 | 2 | within |
| notice-every-1 | 9.763 | 130 | 16 | 2 | within |
| notice-every-1 | 9.909 | 130 | 16 | 2 | within |
| notice-every-1 | 10.076 | 130 | 16 | 2 | within |
| notice-every-1 | 11.478 | 130 | 16 | 2 | within |
| notice-every-1 | 11.653 | 130 | 16 | 2 | within |
| notice-every-1 | 11.799 | 130 | 16 | 2 | within |
| notice-every-1 | 11.965 | 130 | 16 | 2 | within |
| notice-every-1 | 13.531 | 130 | 16 | 2 | within |
| notice-every-1 | 13.704 | 130 | 16 | 2 | within |
| notice-every-1 | 13.851 | 130 | 16 | 2 | within |
| notice-every-1 | 14.018 | 130 | 16 | 2 | within |
| notice-every-1 | 15.615 | 130 | 16 | 2 | within |
| notice-every-1 | 15.788 | 130 | 16 | 2 | within |
| notice-every-1 | 15.935 | 130 | 16 | 2 | within |
| notice-every-1 | 16.101 | 130 | 16 | 2 | within |
| notice-every-1 | 17.468 | 130 | 16 | 2 | within |
| notice-every-1 | 17.641 | 130 | 16 | 2 | within |
| notice-every-1 | 17.787 | 130 | 16 | 2 | within |
| notice-every-1 | 17.954 | 130 | 16 | 2 | within |
| notice-every-1 | 22.916 | 130 | 16 | 2 | within |
| notice-every-1 | 23.040 | 130 | 16 | 2 | within |
| notice-every-1 | 23.210 | 130 | 16 | 2 | within |
| notice-every-1 | 23.381 | 130 | 16 | 2 | within |
| notice-every-2 | 1.703 | 130 | 16 | 2 | within |
| notice-every-2 | 1.880 | 130 | 16 | 2 | within |
| notice-every-2 | 3.687 | 130 | 16 | 2 | within |
| notice-every-2 | 3.862 | 130 | 16 | 2 | within |
| notice-every-2 | 7.536 | 130 | 16 | 2 | within |
| notice-every-2 | 7.710 | 130 | 16 | 2 | within |
| notice-every-2 | 5.590 | 130 | 16 | 2 | within |
| notice-every-2 | 5.766 | 130 | 16 | 2 | within |
| notice-every-2 | 2.039 | 130 | 16 | 2 | within |
| notice-every-2 | 2.213 | 130 | 16 | 2 | within |
| notice-every-2 | 4.021 | 130 | 16 | 2 | within |
| notice-every-2 | 4.196 | 130 | 16 | 2 | within |
| notice-every-2 | 5.922 | 130 | 16 | 2 | within |
| notice-every-2 | 6.092 | 130 | 16 | 2 | within |
| notice-every-2 | 7.862 | 130 | 16 | 2 | within |
| notice-every-2 | 8.029 | 130 | 16 | 2 | within |
| notice-every-2 | 9.652 | 130 | 16 | 2 | within |
| notice-every-2 | 9.826 | 130 | 16 | 2 | within |
| notice-every-2 | 9.972 | 130 | 16 | 2 | within |
| notice-every-2 | 10.140 | 130 | 16 | 2 | within |
| notice-every-2 | 11.543 | 130 | 16 | 2 | within |
| notice-every-2 | 11.717 | 130 | 16 | 2 | within |
| notice-every-2 | 11.863 | 130 | 16 | 2 | within |
| notice-every-2 | 12.030 | 130 | 16 | 2 | within |
| notice-every-2 | 13.594 | 130 | 16 | 2 | within |
| notice-every-2 | 13.768 | 130 | 16 | 2 | within |
| notice-every-2 | 13.914 | 130 | 16 | 2 | within |
| notice-every-2 | 14.081 | 130 | 16 | 2 | within |
| notice-every-2 | 15.678 | 130 | 16 | 2 | within |
| notice-every-2 | 15.850 | 130 | 16 | 2 | within |
| notice-every-2 | 15.997 | 130 | 16 | 2 | within |
| notice-every-2 | 16.164 | 130 | 16 | 2 | within |
| notice-every-2 | 17.531 | 130 | 16 | 2 | within |
| notice-every-2 | 17.704 | 130 | 16 | 2 | within |
| notice-every-2 | 17.851 | 130 | 16 | 2 | within |
| notice-every-2 | 18.017 | 130 | 16 | 2 | within |
| notice-every-2 | 22.980 | 130 | 16 | 2 | within |
| notice-every-2 | 23.104 | 130 | 16 | 2 | within |
| notice-every-2 | 23.274 | 130 | 16 | 2 | within |
| notice-every-2 | 23.445 | 130 | 16 | 2 | within |
| notice-every-3 | 7.591 | 130 | 16 | 2 | within |
| notice-every-3 | 7.765 | 130 | 16 | 2 | within |
| notice-every-3 | 1.560 | 130 | 16 | 2 | within |
| notice-every-3 | 1.738 | 130 | 16 | 2 | within |
| notice-every-3 | 5.459 | 130 | 16 | 2 | within |
| notice-every-3 | 5.635 | 130 | 16 | 2 | within |
| notice-every-3 | 3.553 | 130 | 16 | 2 | within |
| notice-every-3 | 3.732 | 130 | 16 | 2 | within |
| notice-every-3 | 1.898 | 130 | 16 | 2 | within |
| notice-every-3 | 2.072 | 130 | 16 | 2 | within |
| notice-every-3 | 3.893 | 130 | 16 | 2 | within |
| notice-every-3 | 4.068 | 130 | 16 | 2 | within |
| notice-every-3 | 5.792 | 130 | 16 | 2 | within |
| notice-every-3 | 5.962 | 130 | 16 | 2 | within |
| notice-every-3 | 7.918 | 130 | 16 | 2 | within |
| notice-every-3 | 8.085 | 130 | 16 | 2 | within |
| notice-every-3 | 9.521 | 130 | 16 | 2 | within |
| notice-every-3 | 9.695 | 130 | 16 | 2 | within |
| notice-every-3 | 9.842 | 130 | 16 | 2 | within |
| notice-every-3 | 10.010 | 130 | 16 | 2 | within |
| notice-every-3 | 11.591 | 130 | 16 | 2 | within |
| notice-every-3 | 11.765 | 130 | 16 | 2 | within |
| notice-every-3 | 11.912 | 130 | 16 | 2 | within |
| notice-every-3 | 12.078 | 130 | 16 | 2 | within |
| notice-every-3 | 13.463 | 130 | 16 | 2 | within |
| notice-every-3 | 13.637 | 130 | 16 | 2 | within |
| notice-every-3 | 13.784 | 130 | 16 | 2 | within |
| notice-every-3 | 13.951 | 130 | 16 | 2 | within |
| notice-every-3 | 15.547 | 130 | 16 | 2 | within |
| notice-every-3 | 15.719 | 130 | 16 | 2 | within |
| notice-every-3 | 15.867 | 130 | 16 | 2 | within |
| notice-every-3 | 16.034 | 130 | 16 | 2 | within |
| notice-every-3 | 17.575 | 130 | 16 | 2 | within |
| notice-every-3 | 17.748 | 130 | 16 | 2 | within |
| notice-every-3 | 17.895 | 130 | 16 | 2 | within |
| notice-every-3 | 18.062 | 130 | 16 | 2 | within |
| notice-every-3 | 23.023 | 130 | 16 | 2 | within |
| notice-every-3 | 23.147 | 130 | 16 | 2 | within |
| notice-every-3 | 23.317 | 130 | 16 | 2 | within |
| notice-every-3 | 23.487 | 130 | 16 | 2 | within |
| notice-every-4 | 1.705 | 130 | 16 | 2 | within |
| notice-every-4 | 1.882 | 130 | 16 | 2 | within |
| notice-every-4 | 7.544 | 130 | 16 | 2 | within |
| notice-every-4 | 7.717 | 130 | 16 | 2 | within |
| notice-every-4 | 3.693 | 130 | 16 | 2 | within |
| notice-every-4 | 3.870 | 130 | 16 | 2 | within |
| notice-every-4 | 5.600 | 130 | 16 | 2 | within |
| notice-every-4 | 5.776 | 130 | 16 | 2 | within |
| notice-every-4 | 2.041 | 130 | 16 | 2 | within |
| notice-every-4 | 2.215 | 130 | 16 | 2 | within |
| notice-every-4 | 4.031 | 130 | 16 | 2 | within |
| notice-every-4 | 4.206 | 130 | 16 | 2 | within |
| notice-every-4 | 5.933 | 130 | 16 | 2 | within |
| notice-every-4 | 6.103 | 130 | 16 | 2 | within |
| notice-every-4 | 7.870 | 130 | 16 | 2 | within |
| notice-every-4 | 8.037 | 130 | 16 | 2 | within |
| notice-every-4 | 9.657 | 130 | 16 | 2 | within |
| notice-every-4 | 9.831 | 130 | 16 | 2 | within |
| notice-every-4 | 9.977 | 130 | 16 | 2 | within |
| notice-every-4 | 10.145 | 130 | 16 | 2 | within |
| notice-every-4 | 11.546 | 130 | 16 | 2 | within |
| notice-every-4 | 11.721 | 130 | 16 | 2 | within |
| notice-every-4 | 11.867 | 130 | 16 | 2 | within |
| notice-every-4 | 12.034 | 130 | 16 | 2 | within |
| notice-every-4 | 13.597 | 130 | 16 | 2 | within |
| notice-every-4 | 13.771 | 130 | 16 | 2 | within |
| notice-every-4 | 13.918 | 130 | 16 | 2 | within |
| notice-every-4 | 14.085 | 130 | 16 | 2 | within |
| notice-every-4 | 15.680 | 130 | 16 | 2 | within |
| notice-every-4 | 15.853 | 130 | 16 | 2 | within |
| notice-every-4 | 16.000 | 130 | 16 | 2 | within |
| notice-every-4 | 16.167 | 130 | 16 | 2 | within |
| notice-every-4 | 17.709 | 130 | 16 | 2 | within |
| notice-every-4 | 17.882 | 130 | 16 | 2 | within |
| notice-every-4 | 18.029 | 130 | 16 | 2 | within |
| notice-every-4 | 18.196 | 130 | 16 | 2 | within |
| notice-every-4 | 23.156 | 130 | 16 | 2 | within |
| notice-every-4 | 23.280 | 130 | 16 | 2 | within |
| notice-every-4 | 23.450 | 130 | 16 | 2 | within |
| notice-every-4 | 23.621 | 130 | 16 | 2 | within |
| notice-every-5 | 7.638 | 130 | 16 | 2 | within |
| notice-every-5 | 7.812 | 130 | 16 | 2 | within |
| notice-every-5 | 1.560 | 130 | 16 | 2 | within |
| notice-every-5 | 1.738 | 130 | 16 | 2 | within |
| notice-every-5 | 3.552 | 130 | 16 | 2 | within |
| notice-every-5 | 3.729 | 130 | 16 | 2 | within |
| notice-every-5 | 5.655 | 130 | 16 | 2 | within |
| notice-every-5 | 5.831 | 130 | 16 | 2 | within |
| notice-every-5 | 1.898 | 130 | 16 | 2 | within |
| notice-every-5 | 2.072 | 130 | 16 | 2 | within |
| notice-every-5 | 3.888 | 130 | 16 | 2 | within |
| notice-every-5 | 4.064 | 130 | 16 | 2 | within |
| notice-every-5 | 5.988 | 130 | 16 | 2 | within |
| notice-every-5 | 6.158 | 130 | 16 | 2 | within |
| notice-every-5 | 7.965 | 130 | 16 | 2 | within |
| notice-every-5 | 8.131 | 130 | 16 | 2 | within |
| notice-every-5 | 9.558 | 130 | 16 | 2 | within |
| notice-every-5 | 9.732 | 130 | 16 | 2 | within |
| notice-every-5 | 9.879 | 130 | 16 | 2 | within |
| notice-every-5 | 10.046 | 130 | 16 | 2 | within |
| notice-every-5 | 11.451 | 130 | 16 | 2 | within |
| notice-every-5 | 11.625 | 130 | 16 | 2 | within |
| notice-every-5 | 11.771 | 130 | 16 | 2 | within |
| notice-every-5 | 11.938 | 130 | 16 | 2 | within |
| notice-every-5 | 13.504 | 130 | 16 | 2 | within |
| notice-every-5 | 13.677 | 130 | 16 | 2 | within |
| notice-every-5 | 13.824 | 130 | 16 | 2 | within |
| notice-every-5 | 13.991 | 130 | 16 | 2 | within |
| notice-every-5 | 15.592 | 130 | 16 | 2 | within |
| notice-every-5 | 15.764 | 130 | 16 | 2 | within |
| notice-every-5 | 15.911 | 130 | 16 | 2 | within |
| notice-every-5 | 16.078 | 130 | 16 | 2 | within |
| notice-every-5 | 17.446 | 130 | 16 | 2 | within |
| notice-every-5 | 17.618 | 130 | 16 | 2 | within |
| notice-every-5 | 17.765 | 130 | 16 | 2 | within |
| notice-every-5 | 17.932 | 130 | 16 | 2 | within |
| notice-every-5 | 22.896 | 130 | 16 | 2 | within |
| notice-every-5 | 23.020 | 130 | 16 | 2 | within |
| notice-every-5 | 23.190 | 130 | 16 | 2 | within |
| notice-every-5 | 23.360 | 130 | 16 | 2 | within |
| notice-every-6 | 1.705 | 130 | 16 | 2 | within |
| notice-every-6 | 1.882 | 130 | 16 | 2 | within |
| notice-every-6 | 7.702 | 130 | 16 | 2 | within |
| notice-every-6 | 7.875 | 130 | 16 | 2 | within |
| notice-every-6 | 5.571 | 130 | 16 | 2 | within |
| notice-every-6 | 5.747 | 130 | 16 | 2 | within |
| notice-every-6 | 3.698 | 130 | 16 | 2 | within |
| notice-every-6 | 3.877 | 130 | 16 | 2 | within |
| notice-every-6 | 2.041 | 130 | 16 | 2 | within |
| notice-every-6 | 2.215 | 130 | 16 | 2 | within |
| notice-every-6 | 4.037 | 130 | 16 | 2 | within |
| notice-every-6 | 4.213 | 130 | 16 | 2 | within |
| notice-every-6 | 5.904 | 130 | 16 | 2 | within |
| notice-every-6 | 6.073 | 130 | 16 | 2 | within |
| notice-every-6 | 8.029 | 130 | 16 | 2 | within |
| notice-every-6 | 8.196 | 130 | 16 | 2 | within |
| notice-every-6 | 9.630 | 130 | 16 | 2 | within |
| notice-every-6 | 9.804 | 130 | 16 | 2 | within |
| notice-every-6 | 9.951 | 130 | 16 | 2 | within |
| notice-every-6 | 10.118 | 130 | 16 | 2 | within |
| notice-every-6 | 11.702 | 130 | 16 | 2 | within |
| notice-every-6 | 11.876 | 130 | 16 | 2 | within |
| notice-every-6 | 12.023 | 130 | 16 | 2 | within |
| notice-every-6 | 12.190 | 130 | 16 | 2 | within |
| notice-every-6 | 13.575 | 130 | 16 | 2 | within |
| notice-every-6 | 13.748 | 130 | 16 | 2 | within |
| notice-every-6 | 13.896 | 130 | 16 | 2 | within |
| notice-every-6 | 14.063 | 130 | 16 | 2 | within |
| notice-every-6 | 15.662 | 130 | 16 | 2 | within |
| notice-every-6 | 15.835 | 130 | 16 | 2 | within |
| notice-every-6 | 15.982 | 130 | 16 | 2 | within |
| notice-every-6 | 16.149 | 130 | 16 | 2 | within |
| notice-every-6 | 17.692 | 130 | 16 | 2 | within |
| notice-every-6 | 17.864 | 130 | 16 | 2 | within |
| notice-every-6 | 18.012 | 130 | 16 | 2 | within |
| notice-every-6 | 18.179 | 130 | 16 | 2 | within |
| notice-every-6 | 23.139 | 130 | 16 | 2 | within |
| notice-every-6 | 23.263 | 130 | 16 | 2 | within |
| notice-every-6 | 23.433 | 130 | 16 | 2 | within |
| notice-every-6 | 23.604 | 130 | 16 | 2 | within |
| notice-every-7 | 1.506 | 130 | 16 | 2 | within |
| notice-every-7 | 1.682 | 130 | 16 | 2 | within |
| notice-every-7 | 3.489 | 130 | 16 | 2 | within |
| notice-every-7 | 3.664 | 130 | 16 | 2 | within |
| notice-every-7 | 5.545 | 130 | 16 | 2 | within |
| notice-every-7 | 5.719 | 130 | 16 | 2 | within |
| notice-every-7 | 7.491 | 130 | 16 | 2 | within |
| notice-every-7 | 7.664 | 130 | 16 | 2 | within |
| notice-every-7 | 1.842 | 130 | 16 | 2 | within |
| notice-every-7 | 2.015 | 130 | 16 | 2 | within |
| notice-every-7 | 3.824 | 130 | 16 | 2 | within |
| notice-every-7 | 3.999 | 130 | 16 | 2 | within |
| notice-every-7 | 5.875 | 130 | 16 | 2 | within |
| notice-every-7 | 6.045 | 130 | 16 | 2 | within |
| notice-every-7 | 7.818 | 130 | 16 | 2 | within |
| notice-every-7 | 7.985 | 130 | 16 | 2 | within |
| notice-every-7 | 9.603 | 130 | 16 | 2 | within |
| notice-every-7 | 9.777 | 130 | 16 | 2 | within |
| notice-every-7 | 9.924 | 130 | 16 | 2 | within |
| notice-every-7 | 10.091 | 130 | 16 | 2 | within |
| notice-every-7 | 11.494 | 130 | 16 | 2 | within |
| notice-every-7 | 11.668 | 130 | 16 | 2 | within |
| notice-every-7 | 11.815 | 130 | 16 | 2 | within |
| notice-every-7 | 11.982 | 130 | 16 | 2 | within |
| notice-every-7 | 13.546 | 130 | 16 | 2 | within |
| notice-every-7 | 13.719 | 130 | 16 | 2 | within |
| notice-every-7 | 13.867 | 130 | 16 | 2 | within |
| notice-every-7 | 14.034 | 130 | 16 | 2 | within |
| notice-every-7 | 15.456 | 130 | 16 | 2 | within |
| notice-every-7 | 15.629 | 130 | 16 | 2 | within |
| notice-every-7 | 15.776 | 130 | 16 | 2 | within |
| notice-every-7 | 15.943 | 130 | 16 | 2 | within |
| notice-every-7 | 17.485 | 130 | 16 | 2 | within |
| notice-every-7 | 17.658 | 130 | 16 | 2 | within |
| notice-every-7 | 17.806 | 130 | 16 | 2 | within |
| notice-every-7 | 17.972 | 130 | 16 | 2 | within |
| notice-every-7 | 22.933 | 130 | 16 | 2 | within |
| notice-every-7 | 23.058 | 130 | 16 | 2 | within |
| notice-every-7 | 23.228 | 130 | 16 | 2 | within |
| notice-every-7 | 23.398 | 130 | 16 | 2 | within |
| notice-burst-0 | 3.448 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.619 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.631 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.809 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.962 | 130 | 16 | 1 | within |
| notice-burst-0 | 18.130 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.660 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.835 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.196 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.370 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.627 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.815 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.742 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.925 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.523 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.691 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.100 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.274 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.421 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.591 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.088 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.272 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.784 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.973 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.994 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.176 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.150 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.322 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.995 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.193 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.469 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.636 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.178 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.350 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.497 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.664 | 130 | 16 | 1 | within |
| notice-burst-0 | 27.139 | 130 | 16 | 1 | within |
| notice-burst-0 | 27.263 | 130 | 16 | 1 | within |
| notice-burst-0 | 27.434 | 130 | 16 | 1 | within |
| notice-burst-0 | 27.604 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.480 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.651 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.557 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.735 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.382 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.557 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.702 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.874 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.888 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.056 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.722 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.902 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.811 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.986 | 130 | 16 | 1 | within |
| notice-burst-1 | 7.032 | 130 | 16 | 1 | within |
| notice-burst-1 | 7.204 | 130 | 16 | 1 | within |
| notice-burst-1 | 20.118 | 130 | 16 | 1 | within |
| notice-burst-1 | 20.293 | 130 | 16 | 1 | within |
| notice-burst-1 | 20.439 | 130 | 16 | 1 | within |
| notice-burst-1 | 20.609 | 130 | 16 | 1 | within |
| notice-burst-1 | 22.171 | 130 | 16 | 1 | within |
| notice-burst-1 | 22.344 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.671 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.863 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.779 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.967 | 130 | 16 | 1 | within |
| notice-burst-1 | 22.490 | 130 | 16 | 1 | within |
| notice-burst-1 | 22.658 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.038 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.231 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.132 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.318 | 130 | 16 | 1 | within |
| notice-burst-1 | 24.199 | 130 | 16 | 1 | within |
| notice-burst-1 | 24.371 | 130 | 16 | 1 | within |
| notice-burst-1 | 24.518 | 130 | 16 | 1 | within |
| notice-burst-1 | 24.686 | 130 | 16 | 1 | within |
| notice-burst-1 | 26.061 | 130 | 16 | 1 | within |
| notice-burst-1 | 26.184 | 130 | 16 | 1 | within |
| notice-burst-1 | 26.355 | 130 | 16 | 1 | within |
| notice-burst-1 | 26.525 | 130 | 16 | 1 | within |
| notice-burst-2 | 6.500 | 130 | 16 | 1 | within |
| notice-burst-2 | 6.671 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.333 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.509 | 130 | 16 | 1 | within |
| notice-burst-2 | 2.195 | 130 | 16 | 1 | within |
| notice-burst-2 | 2.371 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.664 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.831 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.069 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.242 | 130 | 16 | 1 | within |
| notice-burst-2 | 2.535 | 130 | 16 | 1 | within |
| notice-burst-2 | 2.715 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.478 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.660 | 130 | 16 | 1 | within |
| notice-burst-2 | 6.831 | 130 | 16 | 1 | within |
| notice-burst-2 | 7.006 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.399 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.568 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.282 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.465 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.626 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.808 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.597 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.782 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.943 | 130 | 16 | 1 | within |
| notice-burst-2 | 6.124 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.129 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.301 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.833 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.026 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.448 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.615 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.156 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.328 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.475 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.642 | 130 | 16 | 1 | within |
| notice-burst-2 | 26.017 | 130 | 16 | 1 | within |
| notice-burst-2 | 26.141 | 130 | 16 | 1 | within |
| notice-burst-2 | 26.312 | 130 | 16 | 1 | within |
| notice-burst-2 | 26.482 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.699 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.870 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.669 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.847 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.001 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.168 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.237 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.411 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.564 | 130 | 16 | 1 | within |
| notice-burst-3 | 19.731 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.633 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.821 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.467 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.649 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.133 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.306 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.465 | 130 | 16 | 1 | within |
| notice-burst-3 | 21.633 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.194 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.366 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.815 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.001 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.770 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.961 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.032 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.215 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.128 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.317 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.001 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.199 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.513 | 130 | 16 | 1 | within |
| notice-burst-3 | 23.680 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.222 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.394 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.541 | 130 | 16 | 1 | within |
| notice-burst-3 | 25.708 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.183 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.306 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.477 | 130 | 16 | 1 | within |
| notice-burst-3 | 27.647 | 130 | 16 | 1 | within |
| notice-burst-4 | 17.613 | 130 | 16 | 1 | within |
| notice-burst-4 | 17.791 | 130 | 16 | 1 | within |
| notice-burst-4 | 17.943 | 130 | 16 | 1 | within |
| notice-burst-4 | 18.110 | 130 | 16 | 1 | within |
| notice-burst-4 | 2.606 | 130 | 16 | 1 | within |
| notice-burst-4 | 2.783 | 130 | 16 | 1 | within |
| notice-burst-4 | 19.179 | 130 | 16 | 1 | within |
| notice-burst-4 | 19.353 | 130 | 16 | 1 | within |
| notice-burst-4 | 19.506 | 130 | 16 | 1 | within |
| notice-burst-4 | 19.674 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.428 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.611 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.773 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.950 | 130 | 16 | 1 | within |
| notice-burst-4 | 4.719 | 130 | 16 | 1 | within |
| notice-burst-4 | 4.901 | 130 | 16 | 1 | within |
| notice-burst-4 | 21.080 | 130 | 16 | 1 | within |
| notice-burst-4 | 21.254 | 130 | 16 | 1 | within |
| notice-burst-4 | 5.058 | 130 | 16 | 1 | within |
| notice-burst-4 | 5.237 | 130 | 16 | 1 | within |
| notice-burst-4 | 5.625 | 130 | 16 | 1 | within |
| notice-burst-4 | 5.807 | 130 | 16 | 1 | within |
| notice-burst-4 | 21.400 | 130 | 16 | 1 | within |
| notice-burst-4 | 21.568 | 130 | 16 | 1 | within |
| notice-burst-4 | 5.967 | 130 | 16 | 1 | within |
| notice-burst-4 | 6.148 | 130 | 16 | 1 | within |
| notice-burst-4 | 23.126 | 130 | 16 | 1 | within |
| notice-burst-4 | 23.298 | 130 | 16 | 1 | within |
| notice-burst-4 | 2.962 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.159 | 130 | 16 | 1 | within |
| notice-burst-4 | 23.445 | 130 | 16 | 1 | within |
| notice-burst-4 | 23.612 | 130 | 16 | 1 | within |
| notice-burst-4 | 25.154 | 130 | 16 | 1 | within |
| notice-burst-4 | 25.326 | 130 | 16 | 1 | within |
| notice-burst-4 | 25.473 | 130 | 16 | 1 | within |
| notice-burst-4 | 25.640 | 130 | 16 | 1 | within |
| notice-burst-4 | 27.115 | 130 | 16 | 1 | within |
| notice-burst-4 | 27.238 | 130 | 16 | 1 | within |
| notice-burst-4 | 27.409 | 130 | 16 | 1 | within |
| notice-burst-4 | 27.579 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.271 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.450 | 130 | 16 | 1 | within |
| notice-burst-5 | 1.850 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.023 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.265 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.437 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.605 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.772 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.834 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.008 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.599 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.777 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.400 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.578 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.738 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.913 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.165 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.334 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.894 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.066 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.194 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.383 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.328 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.520 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.688 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.876 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.568 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.757 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.921 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.105 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.212 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.380 | 130 | 16 | 1 | within |
| notice-burst-5 | 23.921 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.093 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.240 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.407 | 130 | 16 | 1 | within |
| notice-burst-5 | 25.956 | 130 | 16 | 1 | within |
| notice-burst-5 | 26.079 | 130 | 16 | 1 | within |
| notice-burst-5 | 26.250 | 130 | 16 | 1 | within |
| notice-burst-5 | 26.420 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.050 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.224 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.377 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.544 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.469 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.639 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.492 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.668 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.821 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.989 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.018 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.198 | 130 | 16 | 1 | within |
| notice-burst-6 | 4.506 | 130 | 16 | 1 | within |
| notice-burst-6 | 4.687 | 130 | 16 | 1 | within |
| notice-burst-6 | 4.847 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.021 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.061 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.235 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.382 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.551 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.126 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.300 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.446 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.614 | 130 | 16 | 1 | within |
| notice-burst-6 | 23.166 | 130 | 16 | 1 | within |
| notice-burst-6 | 23.338 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.367 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.557 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.803 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.986 | 130 | 16 | 1 | within |
| notice-burst-6 | 23.485 | 130 | 16 | 1 | within |
| notice-burst-6 | 23.652 | 130 | 16 | 1 | within |
| notice-burst-6 | 25.453 | 130 | 16 | 1 | within |
| notice-burst-6 | 25.625 | 130 | 16 | 1 | within |
| notice-burst-6 | 25.771 | 130 | 16 | 1 | within |
| notice-burst-6 | 25.938 | 130 | 16 | 1 | within |
| notice-burst-6 | 27.098 | 130 | 16 | 1 | within |
| notice-burst-6 | 27.221 | 130 | 16 | 1 | within |
| notice-burst-6 | 27.392 | 130 | 16 | 1 | within |
| notice-burst-6 | 27.562 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.162 | 130 | 16 | 0 | within |
| notice-burst-7 | 17.341 | 130 | 16 | 0 | within |
| notice-burst-7 | 4.199 | 130 | 16 | 0 | within |
| notice-burst-7 | 4.373 | 130 | 16 | 0 | within |
| notice-burst-7 | 17.495 | 130 | 16 | 0 | within |
| notice-burst-7 | 17.662 | 130 | 16 | 0 | within |
| notice-burst-7 | 18.729 | 130 | 16 | 0 | within |
| notice-burst-7 | 18.903 | 130 | 16 | 0 | within |
| notice-burst-7 | 19.056 | 130 | 16 | 0 | within |
| notice-burst-7 | 19.224 | 130 | 16 | 0 | within |
| notice-burst-7 | 20.807 | 130 | 16 | 0 | within |
| notice-burst-7 | 20.983 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.781 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.967 | 130 | 16 | 0 | within |
| notice-burst-7 | 5.189 | 130 | 16 | 0 | within |
| notice-burst-7 | 5.371 | 130 | 16 | 0 | within |
| notice-burst-7 | 1.690 | 130 | 16 | 0 | within |
| notice-burst-7 | 1.885 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.050 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.236 | 130 | 16 | 0 | within |
| notice-burst-7 | 3.131 | 130 | 16 | 0 | within |
| notice-burst-7 | 3.316 | 130 | 16 | 0 | within |
| notice-burst-7 | 5.528 | 130 | 16 | 0 | within |
| notice-burst-7 | 5.707 | 130 | 16 | 0 | within |
| notice-burst-7 | 21.129 | 130 | 16 | 0 | within |
| notice-burst-7 | 21.297 | 130 | 16 | 0 | within |
| notice-burst-7 | 4.538 | 130 | 16 | 0 | within |
| notice-burst-7 | 4.724 | 130 | 16 | 0 | within |
| notice-burst-7 | 22.678 | 130 | 16 | 0 | within |
| notice-burst-7 | 22.850 | 130 | 16 | 0 | within |
| notice-burst-7 | 22.997 | 130 | 16 | 0 | within |
| notice-burst-7 | 23.164 | 130 | 16 | 0 | within |
| notice-burst-7 | 24.707 | 130 | 16 | 0 | within |
| notice-burst-7 | 24.879 | 130 | 16 | 0 | within |
| notice-burst-7 | 25.026 | 130 | 16 | 0 | within |
| notice-burst-7 | 25.193 | 130 | 16 | 0 | within |
| notice-burst-7 | 26.643 | 130 | 16 | 0 | within |
| notice-burst-7 | 26.767 | 130 | 16 | 0 | within |
| notice-burst-7 | 26.938 | 130 | 16 | 0 | within |
| notice-burst-7 | 27.108 | 130 | 16 | 0 | within |

Latest: 27.647 ms, notice-burst-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 668 | 121,559 (1.216) | 78,910 (0.789) |
| notice-every-1 | 668 | 121,509 (1.215) | 78,910 (0.789) |
| notice-every-2 | 669 | 121,559 (1.216) | 78,910 (0.789) |
| notice-every-3 | 669 | 121,444 (1.214) | 78,910 (0.789) |
| notice-every-4 | 669 | 114,499 (1.145) | 78,910 (0.789) |
| notice-every-5 | 670 | 121,500 (1.215) | 78,910 (0.789) |
| notice-every-6 | 670 | 121,680 (1.217) | 78,910 (0.789) |
| notice-every-7 | 670 | 121,624 (1.216) | 78,910 (0.789) |
| notice-burst-0 | 735 | 129,339 (1.293) | 78,910 (0.789) |
| notice-burst-1 | 735 | 131,801 (1.318) | 78,910 (0.789) |
| notice-burst-2 | 735 | 126,720 (1.267) | 78,910 (0.789) |
| notice-burst-3 | 736 | 129,290 (1.293) | 78,910 (0.789) |
| notice-burst-4 | 736 | 129,098 (1.291) | 78,910 (0.789) |
| notice-burst-5 | 737 | 131,489 (1.315) | 78,910 (0.789) |
| notice-burst-6 | 725 | 131,248 (1.312) | 78,910 (0.789) |
| notice-burst-7 | 724 | 129,567 (1.296) | 78,910 (0.789) |

Longest pass that carries a step: 131,801 CPU cycles (1.318 ms), notice-burst-1; longest step: 78,910 (0.789 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 762,058 | 7.621 | 130 | 134 | fits | 73,572 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 779,447 | 7.794 | 130 | 134 | fits | 73,572 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 156,006 | 1.560 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 173,804 | 1.738 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 354,713 | 3.547 | 130 | 134 | fits | 76,539 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 372,407 | 3.724 | 130 | 134 | fits | 76,539 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 548,745 | 5.487 | 130 | 134 | fits | 76,163 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 566,388 | 5.664 | 130 | 134 | fits | 76,163 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 189,831 | 1.898 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 207,203 | 2.072 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 388,434 | 3.884 | 130 | 134 | fits | 76,539 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 405,956 | 4.060 | 130 | 134 | fits | 76,539 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 582,062 | 5.821 | 130 | 134 | fits | 76,163 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 599,051 | 5.991 | 130 | 134 | fits | 76,163 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 794,829 | 7.948 | 130 | 134 | fits | 73,572 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 811,508 | 8.115 | 130 | 134 | fits | 73,572 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 955,069 | 9.551 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 972,463 | 9.725 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 987,133 | 9.871 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,003,891 | 10.039 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,162,057 | 11.621 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,179,484 | 11.795 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,194,166 | 11.942 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,210,845 | 12.108 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,349,331 | 13.493 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,366,679 | 13.667 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,381,426 | 13.814 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,398,105 | 13.981 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,557,683 | 15.577 | 130 | 134 | fits | 71,842 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,574,952 | 15.750 | 130 | 134 | fits | 71,842 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,589,699 | 15.897 | 130 | 134 | fits | 71,842 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,606,378 | 16.064 | 130 | 134 | fits | 71,842 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,760,609 | 17.606 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,777,878 | 17.779 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,792,625 | 17.926 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,809,304 | 18.093 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,305,320 | 23.053 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,317,727 | 23.177 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,334,726 | 23.347 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,351,804 | 23.518 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 731,547 | 7.315 | 20 | 200 | fits | 149,598 | 207 | 0.232 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 872,948 | 8.729 | 20 | 20 | fits | 139,156 | 77 | 0.700 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 521,106 | 5.211 | 20 | 24 | fits | 103,456 | 58 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 671,804 | 6.718 | 20 | 50 | fits | 149,598 | 207 | 0.232 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,198,430 | 11.984 | 20 | 20 | fits | 103,011 | 45 | 0.720 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 85,654 | 0.857 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 766,717 | 7.667 | 130 | 134 | fits | 73,533 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 784,106 | 7.841 | 130 | 134 | fits | 73,533 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 156,037 | 1.560 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 173,835 | 1.738 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 355,183 | 3.552 | 130 | 134 | fits | 76,398 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 372,877 | 3.729 | 130 | 134 | fits | 76,398 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 549,096 | 5.491 | 130 | 134 | fits | 76,074 | 205 | 0.180 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 566,711 | 5.667 | 130 | 134 | fits | 76,074 | 205 | 0.180 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 189,862 | 1.899 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 207,234 | 2.072 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 388,846 | 3.888 | 130 | 134 | fits | 76,398 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 406,368 | 4.064 | 130 | 134 | fits | 76,398 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 582,385 | 5.824 | 130 | 134 | fits | 76,074 | 205 | 0.180 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 599,374 | 5.994 | 130 | 134 | fits | 76,074 | 205 | 0.180 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 799,404 | 7.994 | 130 | 134 | fits | 73,533 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 816,083 | 8.161 | 130 | 134 | fits | 73,533 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 958,858 | 9.589 | 130 | 134 | fits | 73,308 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 976,252 | 9.763 | 130 | 134 | fits | 73,308 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 990,864 | 9.909 | 130 | 134 | fits | 73,308 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 1,007,622 | 10.076 | 130 | 134 | fits | 73,308 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 1,147,836 | 11.478 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 1,165,263 | 11.653 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 1,179,861 | 11.799 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 1,196,540 | 11.965 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 1,353,065 | 13.531 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 1,370,413 | 13.704 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 1,385,076 | 13.851 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 1,401,755 | 14.018 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 1,561,525 | 15.615 | 130 | 134 | fits | 71,803 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 1,578,794 | 15.788 | 130 | 134 | fits | 71,803 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 1,593,457 | 15.935 | 130 | 134 | fits | 71,803 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 1,610,136 | 16.101 | 130 | 134 | fits | 71,803 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 1,746,803 | 17.468 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 1,764,072 | 17.641 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 1,778,735 | 17.787 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 1,795,414 | 17.954 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 2,291,628 | 22.916 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 2,304,035 | 23.040 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 2,321,034 | 23.210 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 2,338,112 | 23.381 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 158,234 | 1.582 | 20 | 200 | fits | 155,493 | 210 | 0.281 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 802,898 | 8.029 | 20 | 20 | fits | 131,359 | 100 | 0.642 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 651,335 | 6.513 | 20 | 24 | fits | 154,040 | 99 | 0.509 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 763,423 | 7.634 | 20 | 50 | fits | 131,359 | 100 | 0.642 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,177,614 | 11.776 | 20 | 20 | fits | 129,166 | 63 | 0.725 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 98,911 | 0.989 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 170,333 | 1.703 | 130 | 134 | fits | 76,823 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 187,979 | 1.880 | 130 | 134 | fits | 76,823 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 368,688 | 3.687 | 130 | 134 | fits | 75,636 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 386,151 | 3.862 | 130 | 134 | fits | 75,636 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 753,642 | 7.536 | 130 | 134 | fits | 73,558 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 770,952 | 7.710 | 130 | 134 | fits | 73,558 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 559,023 | 5.590 | 130 | 134 | fits | 75,860 | 205 | 0.178 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 576,564 | 5.766 | 130 | 134 | fits | 75,860 | 205 | 0.178 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 203,922 | 2.039 | 130 | 134 | fits | 76,823 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 221,294 | 2.213 | 130 | 134 | fits | 76,823 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 402,120 | 4.021 | 130 | 134 | fits | 75,636 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 419,642 | 4.196 | 130 | 134 | fits | 75,636 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 592,238 | 5.922 | 130 | 134 | fits | 75,860 | 205 | 0.178 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 609,227 | 6.092 | 130 | 134 | fits | 75,860 | 205 | 0.178 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 786,250 | 7.862 | 130 | 134 | fits | 73,558 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 802,929 | 8.029 | 130 | 134 | fits | 73,558 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 965,197 | 9.652 | 130 | 134 | fits | 73,362 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 982,591 | 9.826 | 130 | 134 | fits | 73,362 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 997,203 | 9.972 | 130 | 134 | fits | 73,362 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 1,013,961 | 10.140 | 130 | 134 | fits | 73,362 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 1,154,272 | 11.543 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 1,171,699 | 11.717 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 1,186,297 | 11.863 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 1,202,976 | 12.030 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 1,359,422 | 13.594 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 1,376,770 | 13.768 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 1,391,433 | 13.914 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 1,408,112 | 14.081 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 1,567,754 | 15.678 | 130 | 134 | fits | 71,758 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 1,585,023 | 15.850 | 130 | 134 | fits | 71,758 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 1,599,686 | 15.997 | 130 | 134 | fits | 71,758 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 1,616,365 | 16.164 | 130 | 134 | fits | 71,758 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 1,753,129 | 17.531 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 1,770,398 | 17.704 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 1,785,061 | 17.851 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 1,801,740 | 18.017 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 2,297,971 | 22.980 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 2,310,378 | 23.104 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 2,327,377 | 23.274 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 2,344,455 | 23.445 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 791,700 | 7.917 | 20 | 200 | fits | 152,468 | 210 | 0.273 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 906,945 | 9.069 | 20 | 20 | fits | 135,513 | 65 | 0.693 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 579,921 | 5.799 | 20 | 24 | fits | 158,041 | 127 | 0.469 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 731,957 | 7.320 | 20 | 50 | fits | 152,468 | 210 | 0.273 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,259,481 | 12.595 | 20 | 20 | fits | 107,411 | 55 | 0.733 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 82,610 | 0.826 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 759,065 | 7.591 | 130 | 134 | fits | 73,546 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 776,454 | 7.765 | 130 | 134 | fits | 73,546 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 156,000 | 1.560 | 130 | 134 | fits | 77,034 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 173,798 | 1.738 | 130 | 134 | fits | 77,034 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 545,948 | 5.459 | 130 | 134 | fits | 75,713 | 205 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 563,489 | 5.635 | 130 | 134 | fits | 75,713 | 205 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 355,325 | 3.553 | 130 | 134 | fits | 76,913 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 373,250 | 3.732 | 130 | 134 | fits | 76,913 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 189,825 | 1.898 | 130 | 134 | fits | 77,034 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 207,197 | 2.072 | 130 | 134 | fits | 77,034 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 389,277 | 3.893 | 130 | 134 | fits | 76,913 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 406,799 | 4.068 | 130 | 134 | fits | 76,913 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 579,172 | 5.792 | 130 | 134 | fits | 75,713 | 205 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 596,161 | 5.962 | 130 | 134 | fits | 75,713 | 205 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 791,810 | 7.918 | 130 | 134 | fits | 73,546 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 808,489 | 8.085 | 130 | 134 | fits | 73,546 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 952,129 | 9.521 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 969,523 | 9.695 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 984,193 | 9.842 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 1,000,951 | 10.010 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 1,159,056 | 11.591 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 1,176,483 | 11.765 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 1,191,165 | 11.912 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 1,207,844 | 12.078 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 1,346,330 | 13.463 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 1,363,678 | 13.637 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 1,378,425 | 13.784 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 1,395,104 | 13.951 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 1,554,660 | 15.547 | 130 | 134 | fits | 71,842 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 1,571,929 | 15.719 | 130 | 134 | fits | 71,842 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 1,586,676 | 15.867 | 130 | 134 | fits | 71,842 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 1,603,355 | 16.034 | 130 | 134 | fits | 71,842 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 1,757,525 | 17.575 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 1,774,794 | 17.748 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 1,789,541 | 17.895 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 1,806,220 | 18.062 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 2,302,258 | 23.023 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 2,314,665 | 23.147 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 2,331,664 | 23.317 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 2,348,742 | 23.487 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 727,676 | 7.277 | 20 | 200 | fits | 153,169 | 213 | 0.282 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 864,617 | 8.646 | 20 | 20 | fits | 138,358 | 77 | 0.697 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 521,124 | 5.211 | 20 | 24 | fits | 96,643 | 52 | 0.514 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 667,933 | 6.679 | 20 | 50 | fits | 153,169 | 213 | 0.282 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,193,823 | 11.938 | 20 | 20 | fits | 102,772 | 43 | 0.722 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 85,430 | 0.854 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 170,509 | 1.705 | 130 | 134 | fits | 76,834 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 188,155 | 1.882 | 130 | 134 | fits | 76,834 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 754,360 | 7.544 | 130 | 134 | fits | 73,360 | 205 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 771,670 | 7.717 | 130 | 134 | fits | 73,360 | 205 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 369,347 | 3.693 | 130 | 134 | fits | 76,440 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 387,041 | 3.870 | 130 | 134 | fits | 76,440 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 560,025 | 5.600 | 130 | 134 | fits | 75,952 | 205 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 577,566 | 5.776 | 130 | 134 | fits | 75,952 | 205 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 204,098 | 2.041 | 130 | 134 | fits | 76,834 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 221,470 | 2.215 | 130 | 134 | fits | 76,834 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 403,094 | 4.031 | 130 | 134 | fits | 76,440 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 420,616 | 4.206 | 130 | 134 | fits | 76,440 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 593,298 | 5.933 | 130 | 134 | fits | 75,952 | 205 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 610,287 | 6.103 | 130 | 134 | fits | 75,952 | 205 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 787,026 | 7.870 | 130 | 134 | fits | 73,360 | 205 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 803,705 | 8.037 | 130 | 134 | fits | 73,360 | 205 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 965,683 | 9.657 | 130 | 134 | fits | 73,375 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 983,077 | 9.831 | 130 | 134 | fits | 73,375 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 997,747 | 9.977 | 130 | 134 | fits | 73,375 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 1,014,505 | 10.145 | 130 | 134 | fits | 73,375 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 1,154,637 | 11.546 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 1,172,064 | 11.721 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 1,186,746 | 11.867 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 1,203,425 | 12.034 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 1,359,740 | 13.597 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 1,377,088 | 13.771 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 1,391,835 | 13.918 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 1,408,514 | 14.085 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 1,568,025 | 15.680 | 130 | 134 | fits | 71,797 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 1,585,294 | 15.853 | 130 | 134 | fits | 71,797 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 1,600,041 | 16.000 | 130 | 134 | fits | 71,797 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 1,616,720 | 16.167 | 130 | 134 | fits | 71,797 | 203 | 0.163 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 1,770,890 | 17.709 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 1,788,159 | 17.882 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 1,802,906 | 18.029 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 1,819,585 | 18.196 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 2,315,619 | 23.156 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 2,328,026 | 23.280 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 2,345,025 | 23.450 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 2,362,103 | 23.621 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 717,995 | 7.180 | 20 | 200 | fits | 153,299 | 212 | 0.282 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 854,968 | 8.550 | 20 | 20 | fits | 138,267 | 77 | 0.697 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 524,188 | 5.242 | 20 | 24 | fits | 96,643 | 52 | 0.514 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 658,252 | 6.583 | 20 | 50 | fits | 153,299 | 212 | 0.282 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,179,353 | 11.794 | 20 | 20 | fits | 102,930 | 45 | 0.720 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 73,523 | 0.735 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 763,775 | 7.638 | 130 | 134 | fits | 73,533 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 781,164 | 7.812 | 130 | 134 | fits | 73,533 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 155,984 | 1.560 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 173,782 | 1.738 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 355,168 | 3.552 | 130 | 134 | fits | 76,398 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 372,862 | 3.729 | 130 | 134 | fits | 76,398 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 565,544 | 5.655 | 130 | 134 | fits | 75,736 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 583,126 | 5.831 | 130 | 134 | fits | 75,736 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 189,809 | 1.898 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 207,181 | 2.072 | 130 | 134 | fits | 77,023 | 203 | 0.186 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 388,831 | 3.888 | 130 | 134 | fits | 76,398 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 406,353 | 4.064 | 130 | 134 | fits | 76,398 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 598,800 | 5.988 | 130 | 134 | fits | 75,736 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 615,789 | 6.158 | 130 | 134 | fits | 75,736 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 796,462 | 7.965 | 130 | 134 | fits | 73,533 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 813,141 | 8.131 | 130 | 134 | fits | 73,533 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 955,845 | 9.558 | 130 | 134 | fits | 73,308 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 973,239 | 9.732 | 130 | 134 | fits | 73,308 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 987,851 | 9.879 | 130 | 134 | fits | 73,308 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 1,004,609 | 10.046 | 130 | 134 | fits | 73,308 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 1,145,114 | 11.451 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 1,162,541 | 11.625 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 1,177,139 | 11.771 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 1,193,818 | 11.938 | 130 | 134 | fits | 71,731 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 1,350,386 | 13.504 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 1,367,734 | 13.677 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 1,382,397 | 13.824 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 1,399,076 | 13.991 | 130 | 134 | fits | 71,379 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 1,559,168 | 15.592 | 130 | 134 | fits | 71,827 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 1,576,437 | 15.764 | 130 | 134 | fits | 71,827 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 1,591,100 | 15.911 | 130 | 134 | fits | 71,827 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 1,607,779 | 16.078 | 130 | 134 | fits | 71,827 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 1,744,574 | 17.446 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 1,761,843 | 17.618 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 1,776,506 | 17.765 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 1,793,185 | 17.932 | 130 | 134 | fits | 71,114 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 2,289,561 | 22.896 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 2,301,968 | 23.020 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 2,318,967 | 23.190 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 2,336,045 | 23.360 | 130 | 134 | fits | 66,598 | 202 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 785,609 | 7.856 | 20 | 200 | fits | 153,942 | 216 | 0.276 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 900,401 | 9.004 | 20 | 20 | fits | 135,060 | 65 | 0.692 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 572,371 | 5.724 | 20 | 24 | fits | 158,582 | 129 | 0.477 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 725,866 | 7.259 | 20 | 50 | fits | 153,942 | 216 | 0.276 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,253,000 | 12.530 | 20 | 20 | fits | 107,374 | 55 | 0.734 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 75,484 | 0.755 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 170,520 | 1.705 | 130 | 134 | fits | 76,845 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 188,166 | 1.882 | 130 | 134 | fits | 76,845 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 770,222 | 7.702 | 130 | 134 | fits | 73,178 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 787,532 | 7.875 | 130 | 134 | fits | 73,178 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 557,089 | 5.571 | 130 | 134 | fits | 75,563 | 205 | 0.176 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 574,671 | 5.747 | 130 | 134 | fits | 75,563 | 205 | 0.176 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 369,788 | 3.698 | 130 | 134 | fits | 76,916 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 387,713 | 3.877 | 130 | 134 | fits | 76,916 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 204,109 | 2.041 | 130 | 134 | fits | 76,845 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 221,481 | 2.215 | 130 | 134 | fits | 76,845 | 203 | 0.182 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 403,740 | 4.037 | 130 | 134 | fits | 76,916 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 421,262 | 4.213 | 130 | 134 | fits | 76,916 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 590,354 | 5.904 | 130 | 134 | fits | 75,563 | 205 | 0.176 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 607,343 | 6.073 | 130 | 134 | fits | 75,563 | 205 | 0.176 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 802,888 | 8.029 | 130 | 134 | fits | 73,178 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 819,567 | 8.196 | 130 | 134 | fits | 73,178 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 962,994 | 9.630 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 980,388 | 9.804 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 995,058 | 9.951 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,011,816 | 10.118 | 130 | 134 | fits | 73,321 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,170,201 | 11.702 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,187,628 | 11.876 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,202,310 | 12.023 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,218,989 | 12.190 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,357,500 | 13.575 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,374,848 | 13.748 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,389,595 | 13.896 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,406,274 | 14.063 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,566,190 | 15.662 | 130 | 134 | fits | 71,821 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,583,459 | 15.835 | 130 | 134 | fits | 71,821 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,598,206 | 15.982 | 130 | 134 | fits | 71,821 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,614,885 | 16.149 | 130 | 134 | fits | 71,821 | 203 | 0.164 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,769,170 | 17.692 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,786,439 | 17.864 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,801,186 | 18.012 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,817,865 | 18.179 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,313,889 | 23.139 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,326,296 | 23.263 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,343,295 | 23.433 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,360,373 | 23.604 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 738,933 | 7.389 | 20 | 200 | fits | 149,571 | 206 | 0.231 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 880,208 | 8.802 | 20 | 20 | fits | 138,991 | 79 | 0.698 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 523,645 | 5.236 | 20 | 24 | fits | 96,643 | 52 | 0.514 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 679,190 | 6.792 | 20 | 50 | fits | 149,571 | 206 | 0.231 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,232,043 | 12.320 | 20 | 20 | fits | 111,684 | 58 | 0.736 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 116,276 | 1.163 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 150,588 | 1.506 | 130 | 134 | fits | 76,951 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 168,234 | 1.682 | 130 | 134 | fits | 76,951 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 348,899 | 3.489 | 130 | 134 | fits | 75,820 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 366,362 | 3.664 | 130 | 134 | fits | 75,820 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 554,509 | 5.545 | 130 | 134 | fits | 74,973 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 571,860 | 5.719 | 130 | 134 | fits | 74,973 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 749,106 | 7.491 | 130 | 134 | fits | 73,715 | 205 | 0.168 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 766,416 | 7.664 | 130 | 134 | fits | 73,715 | 205 | 0.168 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 184,177 | 1.842 | 130 | 134 | fits | 76,951 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 201,549 | 2.015 | 130 | 134 | fits | 76,951 | 205 | 0.183 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 382,389 | 3.824 | 130 | 134 | fits | 75,820 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 399,911 | 3.999 | 130 | 134 | fits | 75,820 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 587,543 | 5.875 | 130 | 134 | fits | 74,973 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 604,532 | 6.045 | 130 | 134 | fits | 74,973 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 781,772 | 7.818 | 130 | 134 | fits | 73,715 | 205 | 0.168 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 798,451 | 7.985 | 130 | 134 | fits | 73,715 | 205 | 0.168 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 960,319 | 9.603 | 130 | 134 | fits | 73,375 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 977,713 | 9.777 | 130 | 134 | fits | 73,375 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 992,383 | 9.924 | 130 | 134 | fits | 73,375 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 1,009,141 | 10.091 | 130 | 134 | fits | 73,375 | 203 | 0.167 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 1,149,388 | 11.494 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 1,166,815 | 11.668 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 1,181,497 | 11.815 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 1,198,176 | 11.982 | 130 | 134 | fits | 71,722 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 1,354,600 | 13.546 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 1,371,948 | 13.719 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 1,386,695 | 13.867 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 1,403,374 | 14.034 | 130 | 134 | fits | 71,418 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 1,545,629 | 15.456 | 130 | 134 | fits | 71,866 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 1,562,898 | 15.629 | 130 | 134 | fits | 71,866 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 1,577,645 | 15.776 | 130 | 134 | fits | 71,866 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 1,594,324 | 15.943 | 130 | 134 | fits | 71,866 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 1,748,548 | 17.485 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 1,765,817 | 17.658 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 1,780,564 | 17.806 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 1,797,243 | 17.972 | 130 | 134 | fits | 71,153 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 2,293,347 | 22.933 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 2,305,754 | 23.058 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 2,322,753 | 23.228 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 2,339,831 | 23.398 | 130 | 134 | fits | 66,508 | 202 | 0.136 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 162,353 | 1.624 | 20 | 200 | fits | 152,917 | 204 | 0.292 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 838,340 | 8.383 | 20 | 20 | fits | 137,352 | 89 | 0.683 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 661,805 | 6.618 | 20 | 24 | fits | 156,978 | 125 | 0.498 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 798,865 | 7.989 | 20 | 50 | fits | 137,352 | 89 | 0.683 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,196,994 | 11.970 | 20 | 20 | fits | 117,243 | 55 | 0.733 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 113,055 | 1.131 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 344,831 | 3.448 | 130 | 134 | fits | 76,049 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 361,896 | 3.619 | 130 | 134 | fits | 76,049 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,763,076 | 17.631 | 130 | 134 | fits | 75,886 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,780,876 | 17.809 | 130 | 134 | fits | 75,886 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 1,796,218 | 17.962 | 130 | 134 | fits | 75,886 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 1,812,970 | 18.130 | 130 | 134 | fits | 75,886 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 566,048 | 5.660 | 130 | 134 | fits | 75,499 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 583,496 | 5.835 | 130 | 134 | fits | 75,499 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 1,919,634 | 19.196 | 130 | 134 | fits | 73,464 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 1,937,033 | 19.370 | 130 | 134 | fits | 73,464 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 262,720 | 2.627 | 130 | 134 | fits | 104,184 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 281,479 | 2.815 | 130 | 134 | fits | 104,184 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 474,212 | 4.742 | 130 | 134 | fits | 111,730 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 492,452 | 4.925 | 130 | 134 | fits | 111,730 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 1,952,340 | 19.523 | 130 | 134 | fits | 73,464 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 1,969,092 | 19.691 | 130 | 134 | fits | 73,464 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 2,110,035 | 21.100 | 130 | 134 | fits | 73,388 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 2,127,435 | 21.274 | 130 | 134 | fits | 73,388 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 2,142,121 | 21.421 | 130 | 134 | fits | 73,388 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 2,159,096 | 21.591 | 130 | 134 | fits | 73,388 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 508,786 | 5.088 | 130 | 134 | fits | 111,730 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 527,234 | 5.272 | 130 | 134 | fits | 111,730 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 378,425 | 3.784 | 130 | 134 | fits | 76,049 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 397,256 | 3.973 | 130 | 134 | fits | 76,049 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 599,428 | 5.994 | 130 | 134 | fits | 75,499 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 617,566 | 6.176 | 130 | 134 | fits | 75,499 | 205 | 0.109 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 2,315,026 | 23.150 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 2,332,222 | 23.322 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 299,497 | 2.995 | 130 | 134 | fits | 104,184 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 319,252 | 3.193 | 130 | 134 | fits | 104,184 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,346,885 | 23.469 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,363,637 | 23.636 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,517,809 | 25.178 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,535,005 | 25.350 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 2,549,668 | 25.497 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 2,566,420 | 25.664 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 2,713,930 | 27.139 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,726,289 | 27.263 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,743,384 | 27.434 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 2,760,389 | 27.604 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 666,172 | 6.662 | 20 | 200 | fits | 150,129 | 207 | 0.195 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 780,918 | 7.809 | 20 | 20 | fits | 135,014 | 59 | 0.728 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 475,571 | 4.756 | 20 | 24 | fits | 152,442 | 120 | 0.465 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 606,429 | 6.064 | 20 | 50 | fits | 150,129 | 207 | 0.195 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 1,072,277 | 10.723 | 20 | 20 | fits | 90,329 | 38 | 0.725 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 448,036 | 4.480 | 130 | 134 | fits | 73,748 | 205 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 465,101 | 4.651 | 130 | 134 | fits | 73,748 | 205 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,855,671 | 18.557 | 130 | 134 | fits | 75,649 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,873,471 | 18.735 | 130 | 134 | fits | 75,649 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 238,193 | 2.382 | 130 | 134 | fits | 78,724 | 205 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 255,738 | 2.557 | 130 | 134 | fits | 78,724 | 205 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 670,230 | 6.702 | 130 | 134 | fits | 73,709 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 687,447 | 6.874 | 130 | 134 | fits | 73,709 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 1,888,813 | 18.888 | 130 | 134 | fits | 75,649 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 1,905,565 | 19.056 | 130 | 134 | fits | 75,649 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 272,192 | 2.722 | 130 | 134 | fits | 78,724 | 205 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 290,170 | 2.902 | 130 | 134 | fits | 78,724 | 205 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 481,050 | 4.811 | 130 | 134 | fits | 73,748 | 205 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 498,574 | 4.986 | 130 | 134 | fits | 73,748 | 205 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 703,227 | 7.032 | 130 | 134 | fits | 73,709 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 720,441 | 7.204 | 130 | 134 | fits | 73,709 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 2,011,824 | 20.118 | 130 | 134 | fits | 73,499 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 2,029,307 | 20.293 | 130 | 134 | fits | 73,499 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 2,043,928 | 20.439 | 130 | 134 | fits | 73,499 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 2,060,903 | 20.609 | 130 | 134 | fits | 73,499 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 2,217,079 | 22.171 | 130 | 134 | fits | 71,491 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 2,234,354 | 22.344 | 130 | 134 | fits | 71,491 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 367,056 | 3.671 | 130 | 134 | fits | 102,905 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 386,331 | 3.863 | 130 | 134 | fits | 102,905 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 577,906 | 5.779 | 130 | 134 | fits | 112,047 | 211 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 596,719 | 5.967 | 130 | 134 | fits | 112,047 | 211 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 2,249,017 | 22.490 | 130 | 134 | fits | 71,491 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 2,265,769 | 22.658 | 130 | 134 | fits | 71,491 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 403,824 | 4.038 | 130 | 134 | fits | 102,905 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 423,117 | 4.231 | 130 | 134 | fits | 102,905 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 613,230 | 6.132 | 130 | 134 | fits | 112,047 | 211 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 631,830 | 6.318 | 130 | 134 | fits | 112,047 | 211 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,419,946 | 24.199 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 2,437,142 | 24.371 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 2,451,805 | 24.518 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 2,468,557 | 24.686 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 2,606,090 | 26.061 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 2,618,416 | 26.184 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 2,635,511 | 26.355 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 2,652,516 | 26.525 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 757,538 | 7.575 | 20 | 200 | fits | 149,713 | 206 | 0.194 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 871,851 | 8.719 | 20 | 20 | fits | 134,581 | 59 | 0.724 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 567,353 | 5.674 | 20 | 24 | fits | 150,578 | 114 | 0.465 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 697,795 | 6.978 | 20 | 50 | fits | 149,713 | 206 | 0.194 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,162,989 | 11.630 | 20 | 20 | fits | 90,176 | 38 | 0.725 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 650,032 | 6.500 | 130 | 134 | fits | 73,477 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 667,097 | 6.671 | 130 | 134 | fits | 73,477 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,833,294 | 18.333 | 130 | 134 | fits | 75,584 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,850,902 | 18.509 | 130 | 134 | fits | 75,584 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 219,517 | 2.195 | 130 | 134 | fits | 78,713 | 205 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 237,062 | 2.371 | 130 | 134 | fits | 78,713 | 205 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 1,866,371 | 18.664 | 130 | 134 | fits | 75,584 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 1,883,123 | 18.831 | 130 | 134 | fits | 75,584 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 2,006,851 | 20.069 | 130 | 134 | fits | 73,770 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 2,024,167 | 20.242 | 130 | 134 | fits | 73,770 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 253,516 | 2.535 | 130 | 134 | fits | 78,713 | 205 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 271,494 | 2.715 | 130 | 134 | fits | 78,713 | 205 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 347,793 | 3.478 | 130 | 134 | fits | 101,333 | 211 | 0.181 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 366,033 | 3.660 | 130 | 134 | fits | 101,333 | 211 | 0.181 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 683,108 | 6.831 | 130 | 134 | fits | 73,477 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 700,553 | 7.006 | 130 | 134 | fits | 73,477 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 2,039,942 | 20.399 | 130 | 134 | fits | 73,770 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 2,056,773 | 20.568 | 130 | 134 | fits | 73,770 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 428,160 | 4.282 | 130 | 134 | fits | 76,303 | 205 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 446,532 | 4.465 | 130 | 134 | fits | 76,303 | 205 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 462,649 | 4.626 | 130 | 134 | fits | 76,303 | 205 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 480,798 | 4.808 | 130 | 134 | fits | 76,303 | 205 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 559,659 | 5.597 | 130 | 134 | fits | 110,275 | 211 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 578,241 | 5.782 | 130 | 134 | fits | 110,275 | 211 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 594,300 | 5.943 | 130 | 134 | fits | 110,275 | 211 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 612,438 | 6.124 | 130 | 134 | fits | 110,275 | 211 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 2,212,931 | 22.129 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 2,230,127 | 22.301 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 383,347 | 3.833 | 130 | 134 | fits | 101,333 | 211 | 0.181 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 402,640 | 4.026 | 130 | 134 | fits | 101,333 | 211 | 0.181 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 2,244,790 | 22.448 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 2,261,542 | 22.615 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 2,415,639 | 24.156 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 2,432,835 | 24.328 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 2,447,498 | 24.475 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 2,464,250 | 24.642 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 2,601,730 | 26.017 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,614,056 | 26.141 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,631,151 | 26.312 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 2,648,156 | 26.482 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 742,476 | 7.425 | 20 | 200 | fits | 149,922 | 207 | 0.193 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 856,870 | 8.569 | 20 | 20 | fits | 134,662 | 59 | 0.726 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 552,082 | 5.521 | 20 | 24 | fits | 151,226 | 120 | 0.460 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 682,733 | 6.827 | 20 | 50 | fits | 149,922 | 207 | 0.193 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,147,824 | 11.478 | 20 | 20 | fits | 90,171 | 38 | 0.725 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 569,949 | 5.699 | 130 | 134 | fits | 75,163 | 205 | 0.111 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 587,014 | 5.870 | 130 | 134 | fits | 75,163 | 205 | 0.111 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,766,944 | 17.669 | 130 | 134 | fits | 75,886 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,784,744 | 17.847 | 130 | 134 | fits | 75,886 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 1,800,086 | 18.001 | 130 | 134 | fits | 75,886 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 1,816,838 | 18.168 | 130 | 134 | fits | 75,886 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 1,923,687 | 19.237 | 130 | 134 | fits | 73,571 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 1,941,086 | 19.411 | 130 | 134 | fits | 73,571 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 1,956,394 | 19.564 | 130 | 134 | fits | 73,571 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 1,973,146 | 19.731 | 130 | 134 | fits | 73,571 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 263,291 | 2.633 | 130 | 134 | fits | 104,265 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 282,050 | 2.821 | 130 | 134 | fits | 104,265 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 346,703 | 3.467 | 130 | 134 | fits | 78,267 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 364,923 | 3.649 | 130 | 134 | fits | 78,267 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 2,113,326 | 21.133 | 130 | 134 | fits | 73,722 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 2,130,642 | 21.306 | 130 | 134 | fits | 73,722 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 2,146,463 | 21.465 | 130 | 134 | fits | 73,722 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 2,163,294 | 21.633 | 130 | 134 | fits | 73,722 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 2,319,418 | 23.194 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 2,336,614 | 23.366 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 381,461 | 3.815 | 130 | 134 | fits | 78,267 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 400,140 | 4.001 | 130 | 134 | fits | 78,267 | 205 | 0.099 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 477,026 | 4.770 | 130 | 134 | fits | 113,160 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 496,070 | 4.961 | 130 | 134 | fits | 113,160 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 603,177 | 6.032 | 130 | 134 | fits | 75,163 | 205 | 0.111 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 621,546 | 6.215 | 130 | 134 | fits | 75,163 | 205 | 0.111 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 512,821 | 5.128 | 130 | 134 | fits | 113,160 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 531,652 | 5.317 | 130 | 134 | fits | 113,160 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 300,149 | 3.001 | 130 | 134 | fits | 104,265 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 319,904 | 3.199 | 130 | 134 | fits | 104,265 | 211 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,351,277 | 23.513 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,368,029 | 23.680 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,522,219 | 25.222 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 2,539,415 | 25.394 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 2,554,078 | 25.541 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 2,570,830 | 25.708 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 2,718,270 | 27.183 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,730,629 | 27.306 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,747,724 | 27.477 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,764,729 | 27.647 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 667,182 | 6.672 | 20 | 200 | fits | 149,722 | 206 | 0.188 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 781,805 | 7.818 | 20 | 20 | fits | 134,891 | 59 | 0.727 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 476,988 | 4.770 | 20 | 24 | fits | 152,578 | 120 | 0.466 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 607,439 | 6.074 | 20 | 50 | fits | 149,722 | 206 | 0.188 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,073,279 | 10.733 | 20 | 20 | fits | 90,316 | 38 | 0.725 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,761,270 | 17.613 | 130 | 134 | fits | 75,868 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,779,131 | 17.791 | 130 | 134 | fits | 75,868 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,794,298 | 17.943 | 130 | 134 | fits | 75,868 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,811,050 | 18.110 | 130 | 134 | fits | 75,868 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 260,553 | 2.606 | 130 | 134 | fits | 102,177 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 278,317 | 2.783 | 130 | 134 | fits | 102,177 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 1,917,912 | 19.179 | 130 | 134 | fits | 73,571 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 1,935,311 | 19.353 | 130 | 134 | fits | 73,571 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 1,950,619 | 19.506 | 130 | 134 | fits | 73,571 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 1,967,371 | 19.674 | 130 | 134 | fits | 73,571 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 342,805 | 3.428 | 130 | 134 | fits | 77,140 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 361,101 | 3.611 | 130 | 134 | fits | 77,140 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 377,281 | 3.773 | 130 | 134 | fits | 77,140 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 395,036 | 3.950 | 130 | 134 | fits | 77,140 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 471,945 | 4.719 | 130 | 134 | fits | 110,514 | 211 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 490,106 | 4.901 | 130 | 134 | fits | 110,514 | 211 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 2,108,045 | 21.080 | 130 | 134 | fits | 72,956 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 2,125,445 | 21.254 | 130 | 134 | fits | 72,956 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 505,817 | 5.058 | 130 | 134 | fits | 110,514 | 211 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 523,724 | 5.237 | 130 | 134 | fits | 110,514 | 211 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 562,498 | 5.625 | 130 | 134 | fits | 76,171 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 580,718 | 5.807 | 130 | 134 | fits | 76,171 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 2,140,001 | 21.400 | 130 | 134 | fits | 72,956 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 2,156,753 | 21.568 | 130 | 134 | fits | 72,956 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 596,691 | 5.967 | 130 | 134 | fits | 76,171 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 614,761 | 6.148 | 130 | 134 | fits | 76,171 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 2,312,617 | 23.126 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 2,329,813 | 23.298 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 296,172 | 2.962 | 130 | 134 | fits | 102,177 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 315,927 | 3.159 | 130 | 134 | fits | 102,177 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 2,344,476 | 23.445 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 2,361,228 | 23.612 | 130 | 134 | fits | 71,334 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 2,515,418 | 25.154 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 2,532,614 | 25.326 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 2,547,277 | 25.473 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 2,564,029 | 25.640 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 2,711,469 | 27.115 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 2,723,828 | 27.238 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,740,923 | 27.409 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,757,928 | 27.579 | 130 | 134 | fits | 67,099 | 202 | 0.139 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 664,983 | 6.650 | 20 | 200 | fits | 149,899 | 207 | 0.192 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 779,920 | 7.799 | 20 | 20 | fits | 135,205 | 59 | 0.728 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 474,612 | 4.746 | 20 | 24 | fits | 153,012 | 120 | 0.465 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 605,240 | 6.052 | 20 | 50 | fits | 149,899 | 207 | 0.192 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 1,071,284 | 10.713 | 20 | 20 | fits | 90,316 | 38 | 0.725 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 1,827,150 | 18.271 | 130 | 134 | fits | 75,933 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,845,011 | 18.450 | 130 | 134 | fits | 75,933 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 185,031 | 1.850 | 130 | 134 | fits | 79,543 | 205 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 202,345 | 2.023 | 130 | 134 | fits | 79,543 | 205 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 426,486 | 4.265 | 130 | 134 | fits | 75,595 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 443,703 | 4.437 | 130 | 134 | fits | 75,595 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 1,860,480 | 18.605 | 130 | 134 | fits | 75,933 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 1,877,232 | 18.772 | 130 | 134 | fits | 75,933 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 1,983,367 | 19.834 | 130 | 134 | fits | 73,853 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 2,000,766 | 20.008 | 130 | 134 | fits | 73,853 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 459,923 | 4.599 | 130 | 134 | fits | 75,595 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 477,749 | 4.777 | 130 | 134 | fits | 75,595 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 640,024 | 6.400 | 130 | 134 | fits | 74,988 | 205 | 0.118 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 657,815 | 6.578 | 130 | 134 | fits | 74,988 | 205 | 0.118 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 673,826 | 6.738 | 130 | 134 | fits | 74,988 | 205 | 0.118 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 691,271 | 6.913 | 130 | 134 | fits | 74,988 | 205 | 0.118 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 2,016,541 | 20.165 | 130 | 134 | fits | 73,853 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 2,033,372 | 20.334 | 130 | 134 | fits | 73,853 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 2,189,386 | 21.894 | 130 | 134 | fits | 71,269 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,206,582 | 22.066 | 130 | 134 | fits | 71,269 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 219,385 | 2.194 | 130 | 134 | fits | 79,543 | 205 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 238,295 | 2.383 | 130 | 134 | fits | 79,543 | 205 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 332,753 | 3.328 | 130 | 134 | fits | 113,558 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 352,028 | 3.520 | 130 | 134 | fits | 113,558 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 368,780 | 3.688 | 130 | 134 | fits | 113,558 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 387,611 | 3.876 | 130 | 134 | fits | 113,558 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 556,845 | 5.568 | 130 | 134 | fits | 102,811 | 211 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 575,658 | 5.757 | 130 | 134 | fits | 102,811 | 211 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 592,148 | 5.921 | 130 | 134 | fits | 102,811 | 211 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 610,517 | 6.105 | 130 | 134 | fits | 102,811 | 211 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 2,221,245 | 22.212 | 130 | 134 | fits | 71,269 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 2,237,997 | 22.380 | 130 | 134 | fits | 71,269 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 2,392,125 | 23.921 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 2,409,321 | 24.093 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 2,423,984 | 24.240 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 2,440,736 | 24.407 | 130 | 134 | fits | 71,180 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,595,594 | 25.956 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,607,920 | 26.079 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,625,015 | 26.250 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,642,020 | 26.420 | 130 | 134 | fits | 66,740 | 202 | 0.131 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 754,960 | 7.550 | 20 | 200 | fits | 149,806 | 205 | 0.197 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 869,563 | 8.696 | 20 | 20 | fits | 134,871 | 59 | 0.725 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 564,682 | 5.647 | 20 | 24 | fits | 150,600 | 114 | 0.466 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 695,217 | 6.952 | 20 | 50 | fits | 149,806 | 205 | 0.197 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,160,569 | 11.606 | 20 | 20 | fits | 90,079 | 38 | 0.725 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 205,008 | 2.050 | 130 | 134 | fits | 117,438 | 213 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 222,363 | 2.224 | 130 | 134 | fits | 117,438 | 213 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 237,686 | 2.377 | 130 | 134 | fits | 117,438 | 213 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 254,438 | 2.544 | 130 | 134 | fits | 117,438 | 213 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 546,920 | 5.469 | 130 | 134 | fits | 74,899 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 563,906 | 5.639 | 130 | 134 | fits | 74,899 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 1,749,188 | 17.492 | 130 | 134 | fits | 75,992 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 1,766,796 | 17.668 | 130 | 134 | fits | 75,992 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 1,782,138 | 17.821 | 130 | 134 | fits | 75,992 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 1,798,890 | 17.989 | 130 | 134 | fits | 75,992 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 301,758 | 3.018 | 130 | 134 | fits | 78,949 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 319,823 | 3.198 | 130 | 134 | fits | 78,949 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 450,648 | 4.506 | 130 | 134 | fits | 116,279 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 468,657 | 4.687 | 130 | 134 | fits | 116,279 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 484,657 | 4.847 | 130 | 134 | fits | 116,279 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 502,102 | 5.021 | 130 | 134 | fits | 116,279 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 1,906,076 | 19.061 | 130 | 134 | fits | 73,639 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 1,923,476 | 19.235 | 130 | 134 | fits | 73,639 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,938,162 | 19.382 | 130 | 134 | fits | 73,639 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,955,137 | 19.551 | 130 | 134 | fits | 73,639 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,112,638 | 21.126 | 130 | 134 | fits | 71,669 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,129,992 | 21.300 | 130 | 134 | fits | 71,669 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 2,144,599 | 21.446 | 130 | 134 | fits | 71,669 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 2,161,351 | 21.614 | 130 | 134 | fits | 71,669 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 2,316,630 | 23.166 | 130 | 134 | fits | 71,220 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 2,333,826 | 23.338 | 130 | 134 | fits | 71,220 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 336,651 | 3.367 | 130 | 134 | fits | 78,949 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 355,713 | 3.557 | 130 | 134 | fits | 78,949 | 205 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 580,267 | 5.803 | 130 | 134 | fits | 74,899 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 598,636 | 5.986 | 130 | 134 | fits | 74,899 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 2,348,489 | 23.485 | 130 | 134 | fits | 71,220 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 2,365,241 | 23.652 | 130 | 134 | fits | 71,220 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 2,545,288 | 25.453 | 130 | 134 | fits | 93,331 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 2,562,484 | 25.625 | 130 | 134 | fits | 93,331 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 2,577,082 | 25.771 | 130 | 134 | fits | 93,331 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 2,593,834 | 25.938 | 130 | 134 | fits | 93,331 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,709,824 | 27.098 | 130 | 134 | fits | 66,385 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,722,150 | 27.221 | 130 | 134 | fits | 66,385 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,739,245 | 27.392 | 130 | 134 | fits | 66,385 | 202 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,756,250 | 27.562 | 130 | 134 | fits | 66,385 | 202 | 0.129 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 634,019 | 6.340 | 20 | 200 | fits | 149,416 | 114 | 0.439 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 747,256 | 7.473 | 20 | 20 | fits | 133,505 | 69 | 0.659 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 593,547 | 5.935 | 20 | 24 | fits | 149,416 | 114 | 0.439 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 574,276 | 5.743 | 20 | 50 | fits | 149,416 | 114 | 0.439 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 1,060,957 | 10.610 | 20 | 20 | fits | 112,448 | 46 | 0.718 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 1,716,249 | 17.162 | 130 | 134 | fits | 76,037 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,734,110 | 17.341 | 130 | 134 | fits | 76,037 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 419,865 | 4.199 | 130 | 134 | fits | 117,085 | 211 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 437,333 | 4.373 | 130 | 134 | fits | 117,085 | 211 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 1,749,452 | 17.495 | 130 | 134 | fits | 76,037 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 1,766,204 | 17.662 | 130 | 134 | fits | 76,037 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 1,872,893 | 18.729 | 130 | 134 | fits | 73,565 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 1,890,292 | 18.903 | 130 | 134 | fits | 73,565 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 1,905,600 | 19.056 | 130 | 134 | fits | 73,565 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 1,922,352 | 19.224 | 130 | 134 | fits | 73,565 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 2,080,659 | 20.807 | 130 | 134 | fits | 72,979 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 2,098,282 | 20.983 | 130 | 134 | fits | 72,979 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 278,051 | 2.781 | 130 | 134 | fits | 81,830 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 296,741 | 2.967 | 130 | 134 | fits | 81,830 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 518,926 | 5.189 | 130 | 134 | fits | 75,800 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 537,067 | 5.371 | 130 | 134 | fits | 75,800 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 169,023 | 1.690 | 130 | 134 | fits | 103,033 | 213 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 188,480 | 1.885 | 130 | 134 | fits | 103,033 | 213 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 204,963 | 2.050 | 130 | 134 | fits | 103,033 | 213 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 223,563 | 2.236 | 130 | 134 | fits | 103,033 | 213 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 313,112 | 3.131 | 130 | 134 | fits | 81,830 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 331,560 | 3.316 | 130 | 134 | fits | 81,830 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 552,751 | 5.528 | 130 | 134 | fits | 75,800 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 570,658 | 5.707 | 130 | 134 | fits | 75,800 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 2,112,904 | 21.129 | 130 | 134 | fits | 72,979 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 2,129,656 | 21.297 | 130 | 134 | fits | 72,979 | 203 | 0.168 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 453,793 | 4.538 | 130 | 134 | fits | 117,085 | 211 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 472,393 | 4.724 | 130 | 134 | fits | 117,085 | 211 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 2,267,822 | 22.678 | 130 | 134 | fits | 71,477 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 2,285,018 | 22.850 | 130 | 134 | fits | 71,477 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 2,299,681 | 22.997 | 130 | 134 | fits | 71,477 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 2,316,433 | 23.164 | 130 | 134 | fits | 71,477 | 203 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 2,470,706 | 24.707 | 130 | 134 | fits | 71,259 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 2,487,902 | 24.879 | 130 | 134 | fits | 71,259 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 2,502,565 | 25.026 | 130 | 134 | fits | 71,259 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 2,519,317 | 25.193 | 130 | 134 | fits | 71,259 | 203 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 2,664,340 | 26.643 | 130 | 134 | fits | 66,726 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,676,666 | 26.767 | 130 | 134 | fits | 66,726 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,693,761 | 26.938 | 130 | 134 | fits | 66,726 | 202 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 2,710,766 | 27.108 | 130 | 134 | fits | 66,726 | 202 | 0.131 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 658,076 | 6.581 | 20 | 200 | fits | 150,097 | 207 | 0.193 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 772,845 | 7.728 | 20 | 20 | fits | 135,037 | 59 | 0.728 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 467,507 | 4.675 | 20 | 24 | fits | 152,369 | 120 | 0.464 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 598,333 | 5.983 | 20 | 50 | fits | 150,097 | 207 | 0.193 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 1,064,218 | 10.642 | 20 | 20 | fits | 90,323 | 38 | 0.725 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
