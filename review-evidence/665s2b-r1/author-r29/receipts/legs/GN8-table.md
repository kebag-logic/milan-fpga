### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 736 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.acmp.if0` (notice-burst-2) | 13.050 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-2.held.adp.if1` (notice-burst-2) | 13.253 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-burst-2.held.aecp.if1` (notice-burst-2) | 13.754 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.maap.if0` (notice-burst-0) | 12.585 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-burst-2.held.srp.if1` (notice-burst-2) | 8.898 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-5.mrpdu.periodic.if0` (notice-every-5) | 2.261 | fits | 0 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-5.mrpdu.periodic.if1` (notice-every-5) | 3.350 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 33.191 (33.279) | fits | 1 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1068 | 0 | 172,837 (1.728) | fits |
| notice-every-1 | 1061 | 0 | 170,953 (1.710) | fits |
| notice-every-2 | 1057 | 0 | 177,446 (1.774) | fits |
| notice-every-3 | 1050 | 0 | 170,473 (1.705) | fits |
| notice-every-4 | 1051 | 0 | 169,911 (1.699) | fits |
| notice-every-5 | 1047 | 0 | 171,888 (1.719) | fits |
| notice-every-6 | 1048 | 0 | 172,133 (1.721) | fits |
| notice-every-7 | 1055 | 0 | 168,684 (1.687) | fits |
| notice-burst-0 | 827 | 0 | 169,713 (1.697) | fits |
| notice-burst-1 | 822 | 0 | 170,837 (1.708) | fits |
| notice-burst-2 | 823 | 0 | 175,146 (1.751) | fits |
| notice-burst-3 | 806 | 0 | 167,595 (1.676) | fits |
| notice-burst-4 | 809 | 0 | 175,936 (1.759) | fits |
| notice-burst-5 | 808 | 0 | 170,350 (1.704) | fits |
| notice-burst-6 | 811 | 0 | 176,080 (1.761) | fits |
| notice-burst-7 | 803 | 0 | 170,193 (1.702) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 2.493 | 62 | 32 | 1 | within |
| notice-every-0 | 2.781 | 62 | 32 | 1 | within |
| notice-every-0 | 4.262 | 62 | 32 | 1 | within |
| notice-every-0 | 4.547 | 62 | 32 | 1 | within |
| notice-every-0 | 6.247 | 62 | 32 | 1 | within |
| notice-every-0 | 6.531 | 62 | 32 | 1 | within |
| notice-every-0 | 8.456 | 62 | 32 | 1 | within |
| notice-every-0 | 8.741 | 62 | 32 | 1 | within |
| notice-every-0 | 3.046 | 62 | 32 | 1 | within |
| notice-every-0 | 3.330 | 62 | 32 | 1 | within |
| notice-every-0 | 4.807 | 62 | 32 | 1 | within |
| notice-every-0 | 5.089 | 62 | 32 | 1 | within |
| notice-every-0 | 6.788 | 62 | 32 | 1 | within |
| notice-every-0 | 7.068 | 62 | 32 | 1 | within |
| notice-every-0 | 8.995 | 62 | 32 | 1 | within |
| notice-every-0 | 9.272 | 62 | 32 | 1 | within |
| notice-every-0 | 10.402 | 62 | 32 | 1 | within |
| notice-every-0 | 10.685 | 62 | 32 | 1 | within |
| notice-every-0 | 10.930 | 62 | 32 | 1 | within |
| notice-every-0 | 11.206 | 62 | 32 | 1 | within |
| notice-every-0 | 12.394 | 62 | 32 | 1 | within |
| notice-every-0 | 12.682 | 62 | 32 | 1 | within |
| notice-every-0 | 12.933 | 62 | 32 | 1 | within |
| notice-every-0 | 13.213 | 62 | 32 | 1 | within |
| notice-every-0 | 14.299 | 62 | 32 | 1 | within |
| notice-every-0 | 14.584 | 62 | 32 | 1 | within |
| notice-every-0 | 14.832 | 62 | 32 | 1 | within |
| notice-every-0 | 15.108 | 62 | 32 | 1 | within |
| notice-every-0 | 16.399 | 62 | 32 | 1 | within |
| notice-every-0 | 16.681 | 62 | 32 | 1 | within |
| notice-every-0 | 16.926 | 62 | 32 | 1 | within |
| notice-every-0 | 17.203 | 62 | 32 | 1 | within |
| notice-every-0 | 18.259 | 62 | 32 | 1 | within |
| notice-every-0 | 18.544 | 62 | 32 | 1 | within |
| notice-every-0 | 18.793 | 62 | 32 | 1 | within |
| notice-every-0 | 19.073 | 62 | 32 | 1 | within |
| notice-every-0 | 20.325 | 62 | 32 | 1 | within |
| notice-every-0 | 20.563 | 62 | 32 | 1 | within |
| notice-every-0 | 20.848 | 62 | 32 | 1 | within |
| notice-every-0 | 21.132 | 62 | 32 | 1 | within |
| notice-every-1 | 2.248 | 62 | 32 | 1 | within |
| notice-every-1 | 2.536 | 62 | 32 | 1 | within |
| notice-every-1 | 4.017 | 62 | 32 | 1 | within |
| notice-every-1 | 4.303 | 62 | 32 | 1 | within |
| notice-every-1 | 6.306 | 62 | 32 | 1 | within |
| notice-every-1 | 6.590 | 62 | 32 | 1 | within |
| notice-every-1 | 8.020 | 62 | 32 | 1 | within |
| notice-every-1 | 8.304 | 62 | 32 | 1 | within |
| notice-every-1 | 2.801 | 62 | 32 | 1 | within |
| notice-every-1 | 3.085 | 62 | 32 | 1 | within |
| notice-every-1 | 4.562 | 62 | 32 | 1 | within |
| notice-every-1 | 4.844 | 62 | 32 | 1 | within |
| notice-every-1 | 6.847 | 62 | 32 | 1 | within |
| notice-every-1 | 7.127 | 62 | 32 | 1 | within |
| notice-every-1 | 8.558 | 62 | 32 | 1 | within |
| notice-every-1 | 8.835 | 62 | 32 | 1 | within |
| notice-every-1 | 10.201 | 62 | 32 | 1 | within |
| notice-every-1 | 10.484 | 62 | 32 | 1 | within |
| notice-every-1 | 10.729 | 62 | 32 | 1 | within |
| notice-every-1 | 11.005 | 62 | 32 | 1 | within |
| notice-every-1 | 12.193 | 62 | 32 | 1 | within |
| notice-every-1 | 12.481 | 62 | 32 | 1 | within |
| notice-every-1 | 12.732 | 62 | 32 | 1 | within |
| notice-every-1 | 13.011 | 62 | 32 | 1 | within |
| notice-every-1 | 14.097 | 62 | 32 | 1 | within |
| notice-every-1 | 14.383 | 62 | 32 | 1 | within |
| notice-every-1 | 14.630 | 62 | 32 | 1 | within |
| notice-every-1 | 14.906 | 62 | 32 | 1 | within |
| notice-every-1 | 16.200 | 62 | 32 | 1 | within |
| notice-every-1 | 16.481 | 62 | 32 | 1 | within |
| notice-every-1 | 16.727 | 62 | 32 | 1 | within |
| notice-every-1 | 17.004 | 62 | 32 | 1 | within |
| notice-every-1 | 18.060 | 62 | 32 | 1 | within |
| notice-every-1 | 18.345 | 62 | 32 | 1 | within |
| notice-every-1 | 18.594 | 62 | 32 | 1 | within |
| notice-every-1 | 18.874 | 62 | 32 | 1 | within |
| notice-every-1 | 20.123 | 62 | 32 | 1 | within |
| notice-every-1 | 20.361 | 62 | 32 | 1 | within |
| notice-every-1 | 20.646 | 62 | 32 | 1 | within |
| notice-every-1 | 20.930 | 62 | 32 | 1 | within |
| notice-every-2 | 2.260 | 62 | 32 | 1 | within |
| notice-every-2 | 2.547 | 62 | 32 | 1 | within |
| notice-every-2 | 4.282 | 62 | 32 | 1 | within |
| notice-every-2 | 4.567 | 62 | 32 | 1 | within |
| notice-every-2 | 6.269 | 62 | 32 | 1 | within |
| notice-every-2 | 6.553 | 62 | 32 | 1 | within |
| notice-every-2 | 8.238 | 62 | 32 | 1 | within |
| notice-every-2 | 8.522 | 62 | 32 | 1 | within |
| notice-every-2 | 2.813 | 62 | 32 | 1 | within |
| notice-every-2 | 3.097 | 62 | 32 | 1 | within |
| notice-every-2 | 4.827 | 62 | 32 | 1 | within |
| notice-every-2 | 5.108 | 62 | 32 | 1 | within |
| notice-every-2 | 6.809 | 62 | 32 | 1 | within |
| notice-every-2 | 7.090 | 62 | 32 | 1 | within |
| notice-every-2 | 8.776 | 62 | 32 | 1 | within |
| notice-every-2 | 9.053 | 62 | 32 | 1 | within |
| notice-every-2 | 10.184 | 62 | 32 | 1 | within |
| notice-every-2 | 10.467 | 62 | 32 | 1 | within |
| notice-every-2 | 10.712 | 62 | 32 | 1 | within |
| notice-every-2 | 10.988 | 62 | 32 | 1 | within |
| notice-every-2 | 12.176 | 62 | 32 | 1 | within |
| notice-every-2 | 12.464 | 62 | 32 | 1 | within |
| notice-every-2 | 12.715 | 62 | 32 | 1 | within |
| notice-every-2 | 12.995 | 62 | 32 | 1 | within |
| notice-every-2 | 14.081 | 62 | 32 | 1 | within |
| notice-every-2 | 14.366 | 62 | 32 | 1 | within |
| notice-every-2 | 14.614 | 62 | 32 | 1 | within |
| notice-every-2 | 14.890 | 62 | 32 | 1 | within |
| notice-every-2 | 16.181 | 62 | 32 | 1 | within |
| notice-every-2 | 16.462 | 62 | 32 | 1 | within |
| notice-every-2 | 16.708 | 62 | 32 | 1 | within |
| notice-every-2 | 16.985 | 62 | 32 | 1 | within |
| notice-every-2 | 18.266 | 62 | 32 | 1 | within |
| notice-every-2 | 18.552 | 62 | 32 | 1 | within |
| notice-every-2 | 18.801 | 62 | 32 | 1 | within |
| notice-every-2 | 19.081 | 62 | 32 | 1 | within |
| notice-every-2 | 20.109 | 62 | 32 | 1 | within |
| notice-every-2 | 20.347 | 62 | 32 | 1 | within |
| notice-every-2 | 20.632 | 62 | 32 | 1 | within |
| notice-every-2 | 20.916 | 62 | 32 | 1 | within |
| notice-every-3 | 4.285 | 62 | 32 | 1 | within |
| notice-every-3 | 4.568 | 62 | 32 | 1 | within |
| notice-every-3 | 2.261 | 62 | 32 | 1 | within |
| notice-every-3 | 2.552 | 62 | 32 | 1 | within |
| notice-every-3 | 6.267 | 62 | 32 | 1 | within |
| notice-every-3 | 6.552 | 62 | 32 | 1 | within |
| notice-every-3 | 8.236 | 62 | 32 | 1 | within |
| notice-every-3 | 8.520 | 62 | 32 | 1 | within |
| notice-every-3 | 2.818 | 62 | 32 | 1 | within |
| notice-every-3 | 3.102 | 62 | 32 | 1 | within |
| notice-every-3 | 4.828 | 62 | 32 | 1 | within |
| notice-every-3 | 5.110 | 62 | 32 | 1 | within |
| notice-every-3 | 6.808 | 62 | 32 | 1 | within |
| notice-every-3 | 7.088 | 62 | 32 | 1 | within |
| notice-every-3 | 8.774 | 62 | 32 | 1 | within |
| notice-every-3 | 9.052 | 62 | 32 | 1 | within |
| notice-every-3 | 10.185 | 62 | 32 | 1 | within |
| notice-every-3 | 10.467 | 62 | 32 | 1 | within |
| notice-every-3 | 10.712 | 62 | 32 | 1 | within |
| notice-every-3 | 10.988 | 62 | 32 | 1 | within |
| notice-every-3 | 12.177 | 62 | 32 | 1 | within |
| notice-every-3 | 12.465 | 62 | 32 | 1 | within |
| notice-every-3 | 12.716 | 62 | 32 | 1 | within |
| notice-every-3 | 12.996 | 62 | 32 | 1 | within |
| notice-every-3 | 14.310 | 62 | 32 | 1 | within |
| notice-every-3 | 14.596 | 62 | 32 | 1 | within |
| notice-every-3 | 14.844 | 62 | 32 | 1 | within |
| notice-every-3 | 15.120 | 62 | 32 | 1 | within |
| notice-every-3 | 16.184 | 62 | 32 | 1 | within |
| notice-every-3 | 16.466 | 62 | 32 | 1 | within |
| notice-every-3 | 16.711 | 62 | 32 | 1 | within |
| notice-every-3 | 16.989 | 62 | 32 | 1 | within |
| notice-every-3 | 18.270 | 62 | 32 | 1 | within |
| notice-every-3 | 18.555 | 62 | 32 | 1 | within |
| notice-every-3 | 18.805 | 62 | 32 | 1 | within |
| notice-every-3 | 19.084 | 62 | 32 | 1 | within |
| notice-every-3 | 20.113 | 62 | 32 | 1 | within |
| notice-every-3 | 20.351 | 62 | 32 | 1 | within |
| notice-every-3 | 20.637 | 62 | 32 | 1 | within |
| notice-every-3 | 20.920 | 62 | 32 | 1 | within |
| notice-every-4 | 4.266 | 62 | 32 | 1 | within |
| notice-every-4 | 4.549 | 62 | 32 | 1 | within |
| notice-every-4 | 2.494 | 62 | 32 | 1 | within |
| notice-every-4 | 2.785 | 62 | 32 | 1 | within |
| notice-every-4 | 6.250 | 62 | 32 | 1 | within |
| notice-every-4 | 6.534 | 62 | 32 | 1 | within |
| notice-every-4 | 8.218 | 62 | 32 | 1 | within |
| notice-every-4 | 8.502 | 62 | 32 | 1 | within |
| notice-every-4 | 3.051 | 62 | 32 | 1 | within |
| notice-every-4 | 3.335 | 62 | 32 | 1 | within |
| notice-every-4 | 4.809 | 62 | 32 | 1 | within |
| notice-every-4 | 5.091 | 62 | 32 | 1 | within |
| notice-every-4 | 6.791 | 62 | 32 | 1 | within |
| notice-every-4 | 7.071 | 62 | 32 | 1 | within |
| notice-every-4 | 8.756 | 62 | 32 | 1 | within |
| notice-every-4 | 9.033 | 62 | 32 | 1 | within |
| notice-every-4 | 10.402 | 62 | 32 | 1 | within |
| notice-every-4 | 10.684 | 62 | 32 | 1 | within |
| notice-every-4 | 10.929 | 62 | 32 | 1 | within |
| notice-every-4 | 11.205 | 62 | 32 | 1 | within |
| notice-every-4 | 12.393 | 62 | 32 | 1 | within |
| notice-every-4 | 12.681 | 62 | 32 | 1 | within |
| notice-every-4 | 12.932 | 62 | 32 | 1 | within |
| notice-every-4 | 13.212 | 62 | 32 | 1 | within |
| notice-every-4 | 14.297 | 62 | 32 | 1 | within |
| notice-every-4 | 14.583 | 62 | 32 | 1 | within |
| notice-every-4 | 14.830 | 62 | 32 | 1 | within |
| notice-every-4 | 15.106 | 62 | 32 | 1 | within |
| notice-every-4 | 16.397 | 62 | 32 | 1 | within |
| notice-every-4 | 16.679 | 62 | 32 | 1 | within |
| notice-every-4 | 16.925 | 62 | 32 | 1 | within |
| notice-every-4 | 17.202 | 62 | 32 | 1 | within |
| notice-every-4 | 18.257 | 62 | 32 | 1 | within |
| notice-every-4 | 18.543 | 62 | 32 | 1 | within |
| notice-every-4 | 18.792 | 62 | 32 | 1 | within |
| notice-every-4 | 19.072 | 62 | 32 | 1 | within |
| notice-every-4 | 20.323 | 62 | 32 | 1 | within |
| notice-every-4 | 20.561 | 62 | 32 | 1 | within |
| notice-every-4 | 20.847 | 62 | 32 | 1 | within |
| notice-every-4 | 21.130 | 62 | 32 | 1 | within |
| notice-every-5 | 2.490 | 62 | 32 | 1 | within |
| notice-every-5 | 2.778 | 62 | 32 | 1 | within |
| notice-every-5 | 4.262 | 62 | 32 | 1 | within |
| notice-every-5 | 4.548 | 62 | 32 | 1 | within |
| notice-every-5 | 6.247 | 62 | 32 | 1 | within |
| notice-every-5 | 6.531 | 62 | 32 | 1 | within |
| notice-every-5 | 8.454 | 62 | 32 | 1 | within |
| notice-every-5 | 8.739 | 62 | 32 | 1 | within |
| notice-every-5 | 3.043 | 62 | 32 | 1 | within |
| notice-every-5 | 3.327 | 62 | 32 | 1 | within |
| notice-every-5 | 4.807 | 62 | 32 | 1 | within |
| notice-every-5 | 5.089 | 62 | 32 | 1 | within |
| notice-every-5 | 6.788 | 62 | 32 | 1 | within |
| notice-every-5 | 7.068 | 62 | 32 | 1 | within |
| notice-every-5 | 8.993 | 62 | 32 | 1 | within |
| notice-every-5 | 9.270 | 62 | 32 | 1 | within |
| notice-every-5 | 10.400 | 62 | 32 | 1 | within |
| notice-every-5 | 10.683 | 62 | 32 | 1 | within |
| notice-every-5 | 10.928 | 62 | 32 | 1 | within |
| notice-every-5 | 11.204 | 62 | 32 | 1 | within |
| notice-every-5 | 12.392 | 62 | 32 | 1 | within |
| notice-every-5 | 12.680 | 62 | 32 | 1 | within |
| notice-every-5 | 12.931 | 62 | 32 | 1 | within |
| notice-every-5 | 13.211 | 62 | 32 | 1 | within |
| notice-every-5 | 14.297 | 62 | 32 | 1 | within |
| notice-every-5 | 14.582 | 62 | 32 | 1 | within |
| notice-every-5 | 14.830 | 62 | 32 | 1 | within |
| notice-every-5 | 15.106 | 62 | 32 | 1 | within |
| notice-every-5 | 16.399 | 62 | 32 | 1 | within |
| notice-every-5 | 16.681 | 62 | 32 | 1 | within |
| notice-every-5 | 16.926 | 62 | 32 | 1 | within |
| notice-every-5 | 17.204 | 62 | 32 | 1 | within |
| notice-every-5 | 18.259 | 62 | 32 | 1 | within |
| notice-every-5 | 18.545 | 62 | 32 | 1 | within |
| notice-every-5 | 18.794 | 62 | 32 | 1 | within |
| notice-every-5 | 19.074 | 62 | 32 | 1 | within |
| notice-every-5 | 20.322 | 62 | 32 | 1 | within |
| notice-every-5 | 20.560 | 62 | 32 | 1 | within |
| notice-every-5 | 20.846 | 62 | 32 | 1 | within |
| notice-every-5 | 21.130 | 62 | 32 | 1 | within |
| notice-every-6 | 2.492 | 62 | 32 | 1 | within |
| notice-every-6 | 2.780 | 62 | 32 | 1 | within |
| notice-every-6 | 4.262 | 62 | 32 | 1 | within |
| notice-every-6 | 4.548 | 62 | 32 | 1 | within |
| notice-every-6 | 6.247 | 62 | 32 | 1 | within |
| notice-every-6 | 6.531 | 62 | 32 | 1 | within |
| notice-every-6 | 8.457 | 62 | 32 | 1 | within |
| notice-every-6 | 8.741 | 62 | 32 | 1 | within |
| notice-every-6 | 3.045 | 62 | 32 | 1 | within |
| notice-every-6 | 3.329 | 62 | 32 | 1 | within |
| notice-every-6 | 4.807 | 62 | 32 | 1 | within |
| notice-every-6 | 5.089 | 62 | 32 | 1 | within |
| notice-every-6 | 6.788 | 62 | 32 | 1 | within |
| notice-every-6 | 7.068 | 62 | 32 | 1 | within |
| notice-every-6 | 8.995 | 62 | 32 | 1 | within |
| notice-every-6 | 9.272 | 62 | 32 | 1 | within |
| notice-every-6 | 10.403 | 62 | 32 | 1 | within |
| notice-every-6 | 10.685 | 62 | 32 | 1 | within |
| notice-every-6 | 10.930 | 62 | 32 | 1 | within |
| notice-every-6 | 11.206 | 62 | 32 | 1 | within |
| notice-every-6 | 12.395 | 62 | 32 | 1 | within |
| notice-every-6 | 12.683 | 62 | 32 | 1 | within |
| notice-every-6 | 12.934 | 62 | 32 | 1 | within |
| notice-every-6 | 13.213 | 62 | 32 | 1 | within |
| notice-every-6 | 14.299 | 62 | 32 | 1 | within |
| notice-every-6 | 14.585 | 62 | 32 | 1 | within |
| notice-every-6 | 14.832 | 62 | 32 | 1 | within |
| notice-every-6 | 15.108 | 62 | 32 | 1 | within |
| notice-every-6 | 16.399 | 62 | 32 | 1 | within |
| notice-every-6 | 16.681 | 62 | 32 | 1 | within |
| notice-every-6 | 16.926 | 62 | 32 | 1 | within |
| notice-every-6 | 17.204 | 62 | 32 | 1 | within |
| notice-every-6 | 18.259 | 62 | 32 | 1 | within |
| notice-every-6 | 18.545 | 62 | 32 | 1 | within |
| notice-every-6 | 18.794 | 62 | 32 | 1 | within |
| notice-every-6 | 19.074 | 62 | 32 | 1 | within |
| notice-every-6 | 20.325 | 62 | 32 | 1 | within |
| notice-every-6 | 20.563 | 62 | 32 | 1 | within |
| notice-every-6 | 20.849 | 62 | 32 | 1 | within |
| notice-every-6 | 21.132 | 62 | 32 | 1 | within |
| notice-every-7 | 2.492 | 62 | 32 | 1 | within |
| notice-every-7 | 2.780 | 62 | 32 | 1 | within |
| notice-every-7 | 4.262 | 62 | 32 | 1 | within |
| notice-every-7 | 4.547 | 62 | 32 | 1 | within |
| notice-every-7 | 6.246 | 62 | 32 | 1 | within |
| notice-every-7 | 6.531 | 62 | 32 | 1 | within |
| notice-every-7 | 8.214 | 62 | 32 | 1 | within |
| notice-every-7 | 8.499 | 62 | 32 | 1 | within |
| notice-every-7 | 3.045 | 62 | 32 | 1 | within |
| notice-every-7 | 3.329 | 62 | 32 | 1 | within |
| notice-every-7 | 4.807 | 62 | 32 | 1 | within |
| notice-every-7 | 5.088 | 62 | 32 | 1 | within |
| notice-every-7 | 6.787 | 62 | 32 | 1 | within |
| notice-every-7 | 7.068 | 62 | 32 | 1 | within |
| notice-every-7 | 8.753 | 62 | 32 | 1 | within |
| notice-every-7 | 9.030 | 62 | 32 | 1 | within |
| notice-every-7 | 10.398 | 62 | 32 | 1 | within |
| notice-every-7 | 10.680 | 62 | 32 | 1 | within |
| notice-every-7 | 10.925 | 62 | 32 | 1 | within |
| notice-every-7 | 11.201 | 62 | 32 | 1 | within |
| notice-every-7 | 12.389 | 62 | 32 | 1 | within |
| notice-every-7 | 12.677 | 62 | 32 | 1 | within |
| notice-every-7 | 12.928 | 62 | 32 | 1 | within |
| notice-every-7 | 13.208 | 62 | 32 | 1 | within |
| notice-every-7 | 14.293 | 62 | 32 | 1 | within |
| notice-every-7 | 14.579 | 62 | 32 | 1 | within |
| notice-every-7 | 14.827 | 62 | 32 | 1 | within |
| notice-every-7 | 15.103 | 62 | 32 | 1 | within |
| notice-every-7 | 16.393 | 62 | 32 | 1 | within |
| notice-every-7 | 16.675 | 62 | 32 | 1 | within |
| notice-every-7 | 16.921 | 62 | 32 | 1 | within |
| notice-every-7 | 17.198 | 62 | 32 | 1 | within |
| notice-every-7 | 18.253 | 62 | 32 | 1 | within |
| notice-every-7 | 18.539 | 62 | 32 | 1 | within |
| notice-every-7 | 18.788 | 62 | 32 | 1 | within |
| notice-every-7 | 19.068 | 62 | 32 | 1 | within |
| notice-every-7 | 20.319 | 62 | 32 | 1 | within |
| notice-every-7 | 20.557 | 62 | 32 | 1 | within |
| notice-every-7 | 20.843 | 62 | 32 | 1 | within |
| notice-every-7 | 21.126 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.482 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.767 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.728 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.009 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.493 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.777 | 62 | 32 | 0 | within |
| notice-burst-0 | 6.646 | 62 | 32 | 0 | within |
| notice-burst-0 | 6.927 | 62 | 32 | 0 | within |
| notice-burst-0 | 7.182 | 62 | 32 | 0 | within |
| notice-burst-0 | 7.459 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.270 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.554 | 62 | 32 | 0 | within |
| notice-burst-0 | 6.035 | 62 | 32 | 0 | within |
| notice-burst-0 | 6.318 | 62 | 32 | 0 | within |
| notice-burst-0 | 9.534 | 62 | 32 | 0 | within |
| notice-burst-0 | 13.219 | 62 | 32 | 0 | within |
| notice-burst-0 | 16.841 | 62 | 32 | 0 | within |
| notice-burst-0 | 20.749 | 62 | 32 | 0 | within |
| notice-burst-0 | 21.004 | 62 | 32 | 0 | within |
| notice-burst-0 | 21.282 | 62 | 32 | 0 | within |
| notice-burst-0 | 21.530 | 62 | 32 | 0 | within |
| notice-burst-0 | 22.745 | 62 | 32 | 0 | within |
| notice-burst-0 | 23.004 | 62 | 32 | 0 | within |
| notice-burst-0 | 23.284 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.047 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.356 | 62 | 32 | 0 | within |
| notice-burst-0 | 23.531 | 62 | 32 | 0 | within |
| notice-burst-0 | 24.854 | 62 | 32 | 0 | within |
| notice-burst-0 | 25.107 | 62 | 32 | 0 | within |
| notice-burst-0 | 25.384 | 62 | 32 | 0 | within |
| notice-burst-0 | 25.627 | 62 | 32 | 0 | within |
| notice-burst-0 | 26.713 | 62 | 32 | 0 | within |
| notice-burst-0 | 26.968 | 62 | 32 | 0 | within |
| notice-burst-0 | 27.249 | 62 | 32 | 0 | within |
| notice-burst-0 | 27.497 | 62 | 32 | 0 | within |
| notice-burst-0 | 28.800 | 62 | 32 | 0 | within |
| notice-burst-0 | 29.047 | 62 | 32 | 0 | within |
| notice-burst-0 | 29.281 | 62 | 32 | 0 | within |
| notice-burst-0 | 29.562 | 62 | 32 | 0 | within |
| notice-burst-0 | 30.845 | 62 | 32 | 0 | within |
| notice-burst-1 | 4.006 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.285 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.186 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.465 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.721 | 62 | 32 | 1 | within |
| notice-burst-1 | 6.000 | 62 | 32 | 1 | within |
| notice-burst-1 | 8.034 | 62 | 32 | 1 | within |
| notice-burst-1 | 11.752 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.754 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.049 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.547 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.831 | 62 | 32 | 1 | within |
| notice-burst-1 | 15.393 | 62 | 32 | 1 | within |
| notice-burst-1 | 19.289 | 62 | 32 | 1 | within |
| notice-burst-1 | 19.557 | 62 | 32 | 1 | within |
| notice-burst-1 | 19.835 | 62 | 32 | 1 | within |
| notice-burst-1 | 20.089 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.220 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.472 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.749 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.997 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.214 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.471 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.752 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.328 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.636 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.999 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.094 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.347 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.624 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.868 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.177 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.433 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.714 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.962 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.266 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.513 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.747 | 62 | 32 | 1 | within |
| notice-burst-1 | 30.027 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.092 | 62 | 32 | 1 | within |
| notice-burst-2 | 3.741 | 62 | 32 | 0 | within |
| notice-burst-2 | 4.020 | 62 | 32 | 0 | within |
| notice-burst-2 | 5.522 | 62 | 32 | 0 | within |
| notice-burst-2 | 5.806 | 62 | 32 | 0 | within |
| notice-burst-2 | 6.062 | 62 | 32 | 0 | within |
| notice-burst-2 | 6.342 | 62 | 32 | 0 | within |
| notice-burst-2 | 6.672 | 62 | 32 | 0 | within |
| notice-burst-2 | 6.953 | 62 | 32 | 0 | within |
| notice-burst-2 | 2.492 | 62 | 32 | 0 | within |
| notice-burst-2 | 2.787 | 62 | 32 | 0 | within |
| notice-burst-2 | 7.206 | 62 | 32 | 0 | within |
| notice-burst-2 | 7.484 | 62 | 32 | 0 | within |
| notice-burst-2 | 9.558 | 62 | 32 | 0 | within |
| notice-burst-2 | 13.245 | 62 | 32 | 0 | within |
| notice-burst-2 | 4.286 | 62 | 32 | 0 | within |
| notice-burst-2 | 4.574 | 62 | 32 | 0 | within |
| notice-burst-2 | 16.934 | 62 | 32 | 0 | within |
| notice-burst-2 | 20.765 | 62 | 32 | 0 | within |
| notice-burst-2 | 21.020 | 62 | 32 | 0 | within |
| notice-burst-2 | 21.298 | 62 | 32 | 0 | within |
| notice-burst-2 | 21.546 | 62 | 32 | 0 | within |
| notice-burst-2 | 22.762 | 62 | 32 | 0 | within |
| notice-burst-2 | 23.020 | 62 | 32 | 0 | within |
| notice-burst-2 | 23.301 | 62 | 32 | 0 | within |
| notice-burst-2 | 23.553 | 62 | 32 | 0 | within |
| notice-burst-2 | 24.656 | 62 | 32 | 0 | within |
| notice-burst-2 | 3.064 | 62 | 32 | 0 | within |
| notice-burst-2 | 3.373 | 62 | 32 | 0 | within |
| notice-burst-2 | 24.914 | 62 | 32 | 0 | within |
| notice-burst-2 | 25.191 | 62 | 32 | 0 | within |
| notice-burst-2 | 25.434 | 62 | 32 | 0 | within |
| notice-burst-2 | 26.746 | 62 | 32 | 0 | within |
| notice-burst-2 | 27.002 | 62 | 32 | 0 | within |
| notice-burst-2 | 27.283 | 62 | 32 | 0 | within |
| notice-burst-2 | 27.530 | 62 | 32 | 0 | within |
| notice-burst-2 | 28.834 | 62 | 32 | 0 | within |
| notice-burst-2 | 29.082 | 62 | 32 | 0 | within |
| notice-burst-2 | 29.316 | 62 | 32 | 0 | within |
| notice-burst-2 | 29.596 | 62 | 32 | 0 | within |
| notice-burst-2 | 30.661 | 62 | 32 | 0 | within |
| notice-burst-3 | 5.163 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.441 | 62 | 32 | 1 | within |
| notice-burst-3 | 7.999 | 62 | 32 | 1 | within |
| notice-burst-3 | 11.708 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.747 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.038 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.001 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.287 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.547 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.829 | 62 | 32 | 1 | within |
| notice-burst-3 | 15.343 | 62 | 32 | 1 | within |
| notice-burst-3 | 19.284 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.698 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.981 | 62 | 32 | 1 | within |
| notice-burst-3 | 19.553 | 62 | 32 | 1 | within |
| notice-burst-3 | 19.830 | 62 | 32 | 1 | within |
| notice-burst-3 | 20.085 | 62 | 32 | 1 | within |
| notice-burst-3 | 21.217 | 62 | 32 | 1 | within |
| notice-burst-3 | 21.470 | 62 | 32 | 1 | within |
| notice-burst-3 | 21.748 | 62 | 32 | 1 | within |
| notice-burst-3 | 21.996 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.213 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.471 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.752 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.317 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.626 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.999 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.094 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.347 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.624 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.867 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.177 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.433 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.714 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.962 | 62 | 32 | 1 | within |
| notice-burst-3 | 29.265 | 62 | 32 | 1 | within |
| notice-burst-3 | 29.512 | 62 | 32 | 1 | within |
| notice-burst-3 | 29.747 | 62 | 32 | 1 | within |
| notice-burst-3 | 30.027 | 62 | 32 | 1 | within |
| notice-burst-3 | 31.092 | 62 | 32 | 1 | within |
| notice-burst-4 | 8.117 | 62 | 32 | 1 | within |
| notice-burst-4 | 13.376 | 62 | 32 | 1 | within |
| notice-burst-4 | 17.124 | 62 | 32 | 1 | within |
| notice-burst-4 | 21.066 | 62 | 32 | 1 | within |
| notice-burst-4 | 2.748 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.039 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.001 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.287 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.547 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.829 | 62 | 32 | 1 | within |
| notice-burst-4 | 21.335 | 62 | 32 | 1 | within |
| notice-burst-4 | 21.613 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.171 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.457 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.716 | 62 | 32 | 1 | within |
| notice-burst-4 | 6.000 | 62 | 32 | 1 | within |
| notice-burst-4 | 21.868 | 62 | 32 | 1 | within |
| notice-burst-4 | 23.094 | 62 | 32 | 1 | within |
| notice-burst-4 | 23.346 | 62 | 32 | 1 | within |
| notice-burst-4 | 23.625 | 62 | 32 | 1 | within |
| notice-burst-4 | 23.873 | 62 | 32 | 1 | within |
| notice-burst-4 | 25.215 | 62 | 32 | 1 | within |
| notice-burst-4 | 25.474 | 62 | 32 | 1 | within |
| notice-burst-4 | 25.754 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.317 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.626 | 62 | 32 | 1 | within |
| notice-burst-4 | 26.001 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.097 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.350 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.627 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.870 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.183 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.439 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.719 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.967 | 62 | 32 | 1 | within |
| notice-burst-4 | 31.576 | 62 | 32 | 1 | within |
| notice-burst-4 | 31.825 | 62 | 32 | 1 | within |
| notice-burst-4 | 32.060 | 62 | 32 | 1 | within |
| notice-burst-4 | 32.340 | 62 | 32 | 1 | within |
| notice-burst-4 | 33.190 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.429 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.712 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.262 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.546 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.803 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.082 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.407 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.687 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.943 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.220 | 62 | 32 | 1 | within |
| notice-burst-5 | 8.232 | 62 | 32 | 1 | within |
| notice-burst-5 | 13.498 | 62 | 32 | 1 | within |
| notice-burst-5 | 17.161 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.271 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.537 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.816 | 62 | 32 | 1 | within |
| notice-burst-5 | 22.071 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.298 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.550 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.828 | 62 | 32 | 1 | within |
| notice-burst-5 | 24.077 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.189 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.447 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.727 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.992 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.300 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.974 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.296 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.549 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.826 | 62 | 32 | 1 | within |
| notice-burst-5 | 28.070 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.155 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.411 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.691 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.938 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.242 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.489 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.723 | 62 | 32 | 1 | within |
| notice-burst-5 | 32.003 | 62 | 32 | 1 | within |
| notice-burst-5 | 33.191 | 62 | 32 | 1 | within |
| notice-burst-6 | 2.739 | 62 | 32 | 1 | within |
| notice-burst-6 | 3.024 | 62 | 32 | 1 | within |
| notice-burst-6 | 3.986 | 62 | 32 | 1 | within |
| notice-burst-6 | 4.266 | 62 | 32 | 1 | within |
| notice-burst-6 | 4.522 | 62 | 32 | 1 | within |
| notice-burst-6 | 4.802 | 62 | 32 | 1 | within |
| notice-burst-6 | 5.154 | 62 | 32 | 1 | within |
| notice-burst-6 | 5.434 | 62 | 32 | 1 | within |
| notice-burst-6 | 5.690 | 62 | 32 | 1 | within |
| notice-burst-6 | 5.967 | 62 | 32 | 1 | within |
| notice-burst-6 | 8.074 | 62 | 32 | 1 | within |
| notice-burst-6 | 13.329 | 62 | 32 | 1 | within |
| notice-burst-6 | 17.079 | 62 | 32 | 1 | within |
| notice-burst-6 | 21.266 | 62 | 32 | 1 | within |
| notice-burst-6 | 21.532 | 62 | 32 | 1 | within |
| notice-burst-6 | 21.811 | 62 | 32 | 1 | within |
| notice-burst-6 | 22.066 | 62 | 32 | 1 | within |
| notice-burst-6 | 23.292 | 62 | 32 | 1 | within |
| notice-burst-6 | 23.544 | 62 | 32 | 1 | within |
| notice-burst-6 | 23.823 | 62 | 32 | 1 | within |
| notice-burst-6 | 24.071 | 62 | 32 | 1 | within |
| notice-burst-6 | 25.183 | 62 | 32 | 1 | within |
| notice-burst-6 | 25.441 | 62 | 32 | 1 | within |
| notice-burst-6 | 25.722 | 62 | 32 | 1 | within |
| notice-burst-6 | 3.305 | 62 | 32 | 1 | within |
| notice-burst-6 | 3.613 | 62 | 32 | 1 | within |
| notice-burst-6 | 25.969 | 62 | 32 | 1 | within |
| notice-burst-6 | 27.293 | 62 | 32 | 1 | within |
| notice-burst-6 | 27.546 | 62 | 32 | 1 | within |
| notice-burst-6 | 27.823 | 62 | 32 | 1 | within |
| notice-burst-6 | 28.066 | 62 | 32 | 1 | within |
| notice-burst-6 | 29.152 | 62 | 32 | 1 | within |
| notice-burst-6 | 29.407 | 62 | 32 | 1 | within |
| notice-burst-6 | 29.688 | 62 | 32 | 1 | within |
| notice-burst-6 | 29.936 | 62 | 32 | 1 | within |
| notice-burst-6 | 31.237 | 62 | 32 | 1 | within |
| notice-burst-6 | 31.484 | 62 | 32 | 1 | within |
| notice-burst-6 | 31.718 | 62 | 32 | 1 | within |
| notice-burst-6 | 31.998 | 62 | 32 | 1 | within |
| notice-burst-6 | 33.186 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.482 | 62 | 32 | 0 | within |
| notice-burst-7 | 2.767 | 62 | 32 | 0 | within |
| notice-burst-7 | 3.728 | 62 | 32 | 0 | within |
| notice-burst-7 | 4.009 | 62 | 32 | 0 | within |
| notice-burst-7 | 4.265 | 62 | 32 | 0 | within |
| notice-burst-7 | 4.544 | 62 | 32 | 0 | within |
| notice-burst-7 | 5.476 | 62 | 32 | 0 | within |
| notice-burst-7 | 5.760 | 62 | 32 | 0 | within |
| notice-burst-7 | 6.633 | 62 | 32 | 0 | within |
| notice-burst-7 | 6.912 | 62 | 32 | 0 | within |
| notice-burst-7 | 9.541 | 62 | 32 | 0 | within |
| notice-burst-7 | 13.226 | 62 | 32 | 0 | within |
| notice-burst-7 | 6.020 | 62 | 32 | 0 | within |
| notice-burst-7 | 6.302 | 62 | 32 | 0 | within |
| notice-burst-7 | 7.166 | 62 | 32 | 0 | within |
| notice-burst-7 | 7.446 | 62 | 32 | 0 | within |
| notice-burst-7 | 16.846 | 62 | 32 | 0 | within |
| notice-burst-7 | 20.754 | 62 | 32 | 0 | within |
| notice-burst-7 | 21.009 | 62 | 32 | 0 | within |
| notice-burst-7 | 21.287 | 62 | 32 | 0 | within |
| notice-burst-7 | 21.535 | 62 | 32 | 0 | within |
| notice-burst-7 | 22.750 | 62 | 32 | 0 | within |
| notice-burst-7 | 23.008 | 62 | 32 | 0 | within |
| notice-burst-7 | 23.289 | 62 | 32 | 0 | within |
| notice-burst-7 | 3.047 | 62 | 32 | 0 | within |
| notice-burst-7 | 3.356 | 62 | 32 | 0 | within |
| notice-burst-7 | 23.536 | 62 | 32 | 0 | within |
| notice-burst-7 | 24.859 | 62 | 32 | 0 | within |
| notice-burst-7 | 25.112 | 62 | 32 | 0 | within |
| notice-burst-7 | 25.389 | 62 | 32 | 0 | within |
| notice-burst-7 | 25.632 | 62 | 32 | 0 | within |
| notice-burst-7 | 26.945 | 62 | 32 | 0 | within |
| notice-burst-7 | 27.201 | 62 | 32 | 0 | within |
| notice-burst-7 | 27.481 | 62 | 32 | 0 | within |
| notice-burst-7 | 27.728 | 62 | 32 | 0 | within |
| notice-burst-7 | 28.808 | 62 | 32 | 0 | within |
| notice-burst-7 | 29.055 | 62 | 32 | 0 | within |
| notice-burst-7 | 29.289 | 62 | 32 | 0 | within |
| notice-burst-7 | 29.569 | 62 | 32 | 0 | within |
| notice-burst-7 | 30.852 | 62 | 32 | 0 | within |

Latest: 33.191 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 302 | 143,886 (1.439) | 26,973 (0.270) |
| notice-every-1 | 302 | 143,886 (1.439) | 26,973 (0.270) |
| notice-every-2 | 302 | 51,693 (0.517) | 26,973 (0.270) |
| notice-every-3 | 302 | 51,693 (0.517) | 26,973 (0.270) |
| notice-every-4 | 302 | 144,510 (1.445) | 26,973 (0.270) |
| notice-every-5 | 302 | 143,909 (1.439) | 26,973 (0.270) |
| notice-every-6 | 302 | 143,909 (1.439) | 26,973 (0.270) |
| notice-every-7 | 302 | 143,909 (1.439) | 26,973 (0.270) |
| notice-burst-0 | 312 | 67,712 (0.677) | 26,973 (0.270) |
| notice-burst-1 | 312 | 77,116 (0.771) | 26,973 (0.270) |
| notice-burst-2 | 312 | 63,394 (0.634) | 26,973 (0.270) |
| notice-burst-3 | 312 | 66,149 (0.661) | 26,973 (0.270) |
| notice-burst-4 | 312 | 134,194 (1.342) | 26,973 (0.270) |
| notice-burst-5 | 312 | 65,732 (0.657) | 26,973 (0.270) |
| notice-burst-6 | 312 | 65,837 (0.658) | 26,973 (0.270) |
| notice-burst-7 | 312 | 66,526 (0.665) | 26,973 (0.270) |

Longest pass that carries a step: 144,510 CPU cycles (1.445 ms), notice-every-4; longest step: 26,973 (0.270 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 249,328 | 2.493 | 62 | 66 | fits | 143,886 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 278,087 | 2.781 | 62 | 66 | fits | 143,886 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 426,208 | 4.262 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 454,736 | 4.547 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 624,682 | 6.247 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 653,113 | 6.531 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 845,636 | 8.456 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 874,085 | 8.741 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 304,594 | 3.046 | 62 | 66 | fits | 143,886 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 332,999 | 3.330 | 62 | 66 | fits | 143,886 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 480,689 | 4.807 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 508,863 | 5.089 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 678,773 | 6.788 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 706,795 | 7.068 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 899,497 | 8.995 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 927,209 | 9.272 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,040,241 | 10.402 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,068,467 | 10.685 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 1,092,961 | 10.930 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,120,562 | 11.206 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,239,442 | 12.394 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,268,240 | 12.682 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,293,317 | 12.933 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,321,299 | 13.213 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,429,857 | 14.299 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,458,430 | 14.584 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,483,191 | 14.832 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,510,792 | 15.108 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,639,879 | 16.399 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,668,053 | 16.681 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,692,591 | 16.926 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,720,347 | 17.203 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,825,877 | 18.259 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,854,440 | 18.544 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,879,345 | 18.793 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,907,324 | 19.073 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,032,461 | 20.325 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,056,265 | 20.563 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,084,820 | 20.848 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,113,183 | 21.132 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 1,080,757 | 10.808 | 20 | 200 | fits | 164,097 | 127 | 0.547 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 1,060,489 | 10.605 | 20 | 20 | fits | 164,097 | 127 | 0.547 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 1,119,747 | 11.197 | 20 | 24 | fits | 79,462 | 59 | 0.533 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 1,021,014 | 10.210 | 20 | 50 | fits | 164,097 | 127 | 0.547 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 635,199 | 6.352 | 20 | 20 | fits | 162,329 | 62 | 0.375 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 224,077 | 2.241 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 332,920 | 3.329 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 224,827 | 2.248 | 62 | 66 | fits | 143,886 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 253,586 | 2.536 | 62 | 66 | fits | 143,886 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 401,724 | 4.017 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 430,252 | 4.303 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 630,580 | 6.306 | 62 | 66 | fits | 118,181 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 659,011 | 6.590 | 62 | 66 | fits | 118,181 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 801,962 | 8.020 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 830,411 | 8.304 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 280,093 | 2.801 | 62 | 66 | fits | 143,886 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 308,498 | 3.085 | 62 | 66 | fits | 143,886 | 402 | 0.105 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 456,205 | 4.562 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 484,379 | 4.844 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 684,671 | 6.847 | 62 | 66 | fits | 118,181 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 712,693 | 7.127 | 62 | 66 | fits | 118,181 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 855,823 | 8.558 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 883,535 | 8.835 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 1,020,138 | 10.201 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 1,048,364 | 10.484 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 1,072,858 | 10.729 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 1,100,459 | 11.005 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 1,219,287 | 12.193 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 1,248,085 | 12.481 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 1,273,162 | 12.732 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 1,301,144 | 13.011 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 1,409,707 | 14.097 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 1,438,280 | 14.383 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 1,463,041 | 14.630 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 1,490,642 | 14.906 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 1,619,965 | 16.200 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 1,648,139 | 16.481 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 1,672,677 | 16.727 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 1,700,433 | 17.004 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 1,805,958 | 18.060 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 1,834,521 | 18.345 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 1,859,426 | 18.594 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 1,887,405 | 18.874 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 2,012,314 | 20.123 | 62 | 66 | fits | 111,720 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 2,036,086 | 20.361 | 62 | 66 | fits | 111,720 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 2,064,641 | 20.646 | 62 | 66 | fits | 111,720 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 2,093,004 | 20.930 | 62 | 66 | fits | 111,720 | 398 | 0.062 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if1` | 1,079,378 | 10.794 | 20 | 200 | fits | 166,964 | 137 | 0.526 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 1,174,971 | 11.750 | 20 | 20 | fits | 115,861 | 86 | 0.529 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if1` | 1,154,767 | 11.548 | 20 | 24 | fits | 115,861 | 86 | 0.529 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 1,019,635 | 10.196 | 20 | 50 | fits | 166,964 | 137 | 0.526 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if1` | 830,646 | 8.306 | 20 | 20 | fits | 160,991 | 156 | 0.575 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 211,463 | 2.115 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if1` | 320,369 | 3.204 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 225,971 | 2.260 | 62 | 66 | fits | 122,010 | 403 | 0.098 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 254,730 | 2.547 | 62 | 66 | fits | 122,010 | 403 | 0.098 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 428,182 | 4.282 | 62 | 66 | fits | 118,910 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 456,710 | 4.567 | 62 | 66 | fits | 118,910 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 626,851 | 6.269 | 62 | 66 | fits | 118,185 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 655,282 | 6.553 | 62 | 66 | fits | 118,185 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 823,773 | 8.238 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 852,222 | 8.522 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 281,260 | 2.813 | 62 | 66 | fits | 122,010 | 403 | 0.098 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 309,665 | 3.097 | 62 | 66 | fits | 122,010 | 403 | 0.098 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 482,663 | 4.827 | 62 | 66 | fits | 118,910 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 510,837 | 5.108 | 62 | 66 | fits | 118,910 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 680,942 | 6.809 | 62 | 66 | fits | 118,185 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 708,964 | 7.090 | 62 | 66 | fits | 118,185 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 877,634 | 8.776 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 905,346 | 9.053 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 1,018,435 | 10.184 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 1,046,661 | 10.467 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 1,071,155 | 10.712 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 1,098,756 | 10.988 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 1,217,636 | 12.176 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 1,246,434 | 12.464 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 1,271,511 | 12.715 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 1,299,493 | 12.995 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 1,408,051 | 14.081 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 1,436,624 | 14.366 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 1,461,385 | 14.614 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 1,488,986 | 14.890 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 1,618,073 | 16.181 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 1,646,247 | 16.462 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 1,670,785 | 16.708 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 1,698,541 | 16.985 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 1,826,603 | 18.266 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 1,855,166 | 18.552 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 1,880,071 | 18.801 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 1,908,050 | 19.081 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 2,010,884 | 20.109 | 62 | 66 | fits | 111,716 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 2,034,688 | 20.347 | 62 | 66 | fits | 111,716 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 2,063,243 | 20.632 | 62 | 66 | fits | 111,716 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 2,091,606 | 20.916 | 62 | 66 | fits | 111,716 | 398 | 0.062 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if1` | 1,086,259 | 10.863 | 20 | 200 | fits | 156,696 | 146 | 0.543 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 1,173,348 | 11.733 | 20 | 20 | fits | 107,357 | 73 | 0.544 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if1` | 1,153,144 | 11.531 | 20 | 24 | fits | 107,357 | 73 | 0.544 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 1,026,516 | 10.265 | 20 | 50 | fits | 156,696 | 146 | 0.543 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if1` | 821,758 | 8.218 | 20 | 20 | fits | 177,446 | 157 | 0.548 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 218,724 | 2.187 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if1` | 327,628 | 3.276 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 428,454 | 4.285 | 62 | 66 | fits | 118,727 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 456,824 | 4.568 | 62 | 66 | fits | 118,727 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 226,115 | 2.261 | 62 | 66 | fits | 122,588 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 255,244 | 2.552 | 62 | 66 | fits | 122,588 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 626,730 | 6.267 | 62 | 66 | fits | 118,285 | 402 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 655,161 | 6.552 | 62 | 66 | fits | 118,285 | 402 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 823,588 | 8.236 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 852,037 | 8.520 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 281,835 | 2.818 | 62 | 66 | fits | 122,588 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 310,240 | 3.102 | 62 | 66 | fits | 122,588 | 403 | 0.097 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 482,777 | 4.828 | 62 | 66 | fits | 118,727 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 510,951 | 5.110 | 62 | 66 | fits | 118,727 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 680,821 | 6.808 | 62 | 66 | fits | 118,285 | 402 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 708,843 | 7.088 | 62 | 66 | fits | 118,285 | 402 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 877,449 | 8.774 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 905,161 | 9.052 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 1,018,500 | 10.185 | 62 | 66 | fits | 115,419 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 1,046,726 | 10.467 | 62 | 66 | fits | 115,419 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 1,071,220 | 10.712 | 62 | 66 | fits | 115,419 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 1,098,821 | 10.988 | 62 | 66 | fits | 115,419 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 1,217,698 | 12.177 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 1,246,496 | 12.465 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 1,271,573 | 12.716 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 1,299,555 | 12.996 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 1,431,030 | 14.310 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 1,459,603 | 14.596 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 1,484,364 | 14.844 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 1,511,965 | 15.120 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 1,618,395 | 16.184 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 1,646,569 | 16.466 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 1,671,107 | 16.711 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 1,698,863 | 16.989 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 1,826,982 | 18.270 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 1,855,545 | 18.555 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 1,880,450 | 18.805 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 1,908,429 | 19.084 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 2,011,291 | 20.113 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 2,035,095 | 20.351 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 2,063,650 | 20.637 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 2,092,013 | 20.920 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if1` | 1,060,642 | 10.606 | 20 | 200 | fits | 158,070 | 123 | 0.554 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 1,040,374 | 10.404 | 20 | 20 | fits | 158,070 | 123 | 0.554 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if1` | 1,153,392 | 11.534 | 20 | 24 | fits | 133,222 | 99 | 0.466 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 1,000,899 | 10.009 | 20 | 50 | fits | 158,070 | 123 | 0.554 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if1` | 820,804 | 8.208 | 20 | 20 | fits | 160,614 | 152 | 0.572 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 217,102 | 2.171 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if1` | 326,055 | 3.261 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 426,570 | 4.266 | 62 | 66 | fits | 118,922 | 402 | 0.078 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 454,940 | 4.549 | 62 | 66 | fits | 118,922 | 402 | 0.078 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 249,376 | 2.494 | 62 | 66 | fits | 144,510 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 278,505 | 2.785 | 62 | 66 | fits | 144,510 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 624,990 | 6.250 | 62 | 66 | fits | 118,285 | 402 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 653,421 | 6.534 | 62 | 66 | fits | 118,285 | 402 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 821,755 | 8.218 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 850,204 | 8.502 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 305,119 | 3.051 | 62 | 66 | fits | 144,510 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 333,524 | 3.335 | 62 | 66 | fits | 144,510 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 480,893 | 4.809 | 62 | 66 | fits | 118,922 | 402 | 0.078 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 509,067 | 5.091 | 62 | 66 | fits | 118,922 | 402 | 0.078 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 679,081 | 6.791 | 62 | 66 | fits | 118,285 | 402 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 707,103 | 7.071 | 62 | 66 | fits | 118,285 | 402 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 875,616 | 8.756 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 903,328 | 9.033 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 1,040,164 | 10.402 | 62 | 66 | fits | 115,419 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 1,068,390 | 10.684 | 62 | 66 | fits | 115,419 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 1,092,884 | 10.929 | 62 | 66 | fits | 115,419 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 1,120,485 | 11.205 | 62 | 66 | fits | 115,419 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 1,239,305 | 12.393 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 1,268,103 | 12.681 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 1,293,180 | 12.932 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 1,321,162 | 13.212 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 1,429,712 | 14.297 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 1,458,285 | 14.583 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 1,483,046 | 14.830 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 1,510,647 | 15.106 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 1,639,742 | 16.397 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 1,667,916 | 16.679 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 1,692,454 | 16.925 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 1,720,210 | 17.202 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 1,825,740 | 18.257 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 1,854,303 | 18.543 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 1,879,208 | 18.792 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 1,907,187 | 19.072 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 2,032,316 | 20.323 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 2,056,120 | 20.561 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 2,084,675 | 20.847 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 2,113,038 | 21.130 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if1` | 441,656 | 4.417 | 20 | 200 | fits | 158,122 | 129 | 0.399 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 1,024,644 | 10.246 | 20 | 20 | fits | 169,911 | 142 | 0.519 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if1` | 1,139,270 | 11.393 | 20 | 24 | fits | 114,216 | 84 | 0.476 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 985,169 | 9.852 | 20 | 50 | fits | 169,911 | 142 | 0.519 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if1` | 793,233 | 7.932 | 20 | 20 | fits | 165,400 | 145 | 0.574 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 182,538 | 1.825 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if1` | 291,386 | 2.914 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 249,008 | 2.490 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 277,767 | 2.778 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 426,230 | 4.262 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 454,758 | 4.548 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 624,701 | 6.247 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 653,132 | 6.531 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 845,430 | 8.454 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 873,879 | 8.739 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 304,297 | 3.043 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 332,702 | 3.327 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 480,711 | 4.807 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 508,885 | 5.089 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 678,792 | 6.788 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 706,814 | 7.068 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 899,291 | 8.993 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 927,003 | 9.270 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 1,040,038 | 10.400 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 1,068,264 | 10.683 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 1,092,758 | 10.928 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 1,120,359 | 11.204 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 1,239,241 | 12.392 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 1,268,039 | 12.680 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 1,293,116 | 12.931 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 1,321,098 | 13.211 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 1,429,661 | 14.297 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 1,458,234 | 14.582 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 1,482,995 | 14.830 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 1,510,596 | 15.106 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 1,639,919 | 16.399 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 1,668,093 | 16.681 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 1,692,631 | 16.926 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 1,720,387 | 17.204 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 1,825,912 | 18.259 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 1,854,475 | 18.545 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 1,879,380 | 18.794 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 1,907,359 | 19.074 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 2,032,232 | 20.322 | 62 | 66 | fits | 111,716 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 2,056,036 | 20.560 | 62 | 66 | fits | 111,716 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 2,084,591 | 20.846 | 62 | 66 | fits | 111,716 | 398 | 0.062 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 2,112,954 | 21.130 | 62 | 66 | fits | 111,716 | 398 | 0.062 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if1` | 1,067,469 | 10.675 | 20 | 200 | fits | 158,822 | 122 | 0.564 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 1,047,201 | 10.472 | 20 | 20 | fits | 158,822 | 122 | 0.564 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if1` | 1,140,868 | 11.409 | 20 | 24 | fits | 113,871 | 79 | 0.484 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 1,007,726 | 10.077 | 20 | 50 | fits | 158,822 | 122 | 0.564 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if1` | 826,879 | 8.269 | 20 | 20 | fits | 162,728 | 158 | 0.573 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 226,075 | 2.261 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if1` | 334,953 | 3.350 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 249,246 | 2.492 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 278,005 | 2.780 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 426,242 | 4.262 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 454,770 | 4.548 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 624,716 | 6.247 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 653,147 | 6.531 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 845,670 | 8.457 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 874,119 | 8.741 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 304,535 | 3.045 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 332,940 | 3.329 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 480,723 | 4.807 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 508,897 | 5.089 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 678,807 | 6.788 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 706,829 | 7.068 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 899,531 | 8.995 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 927,243 | 9.272 | 62 | 66 | fits | 116,814 | 400 | 0.075 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 1,040,275 | 10.403 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 1,068,501 | 10.685 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 1,092,995 | 10.930 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,120,596 | 11.206 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,239,476 | 12.395 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,268,274 | 12.683 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,293,351 | 12.934 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,321,333 | 13.213 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,429,891 | 14.299 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,458,464 | 14.585 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,483,225 | 14.832 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,510,826 | 15.108 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,639,913 | 16.399 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,668,087 | 16.681 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,692,625 | 16.926 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,720,381 | 17.204 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,825,911 | 18.259 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,854,474 | 18.545 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,879,379 | 18.794 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,907,358 | 19.074 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,032,495 | 20.325 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,056,299 | 20.563 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,084,854 | 20.849 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,113,217 | 21.132 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if1` | 1,084,282 | 10.843 | 20 | 200 | fits | 163,857 | 125 | 0.547 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 1,064,014 | 10.640 | 20 | 20 | fits | 163,857 | 125 | 0.547 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if1` | 1,121,552 | 11.216 | 20 | 24 | fits | 77,742 | 53 | 0.525 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 1,024,539 | 10.245 | 20 | 50 | fits | 163,857 | 125 | 0.547 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if1` | 639,623 | 6.396 | 20 | 20 | fits | 163,657 | 68 | 0.378 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 225,436 | 2.254 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if1` | 334,281 | 3.343 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 249,237 | 2.492 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 277,996 | 2.780 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 426,173 | 4.262 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 454,701 | 4.547 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 624,644 | 6.246 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 653,075 | 6.531 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 821,409 | 8.214 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 849,858 | 8.499 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 304,526 | 3.045 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 332,931 | 3.329 | 62 | 66 | fits | 143,909 | 402 | 0.106 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 480,654 | 4.807 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 508,828 | 5.088 | 62 | 66 | fits | 119,105 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 678,735 | 6.787 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 706,757 | 7.068 | 62 | 66 | fits | 118,380 | 402 | 0.079 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 875,270 | 8.753 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 902,982 | 9.030 | 62 | 66 | fits | 117,009 | 402 | 0.075 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 1,039,772 | 10.398 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 1,067,998 | 10.680 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 1,092,492 | 10.925 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 1,120,093 | 11.201 | 62 | 66 | fits | 115,373 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 1,238,913 | 12.389 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 1,267,711 | 12.677 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 1,292,788 | 12.928 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 1,320,770 | 13.208 | 62 | 66 | fits | 116,394 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 1,429,320 | 14.293 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 1,457,893 | 14.579 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 1,482,654 | 14.827 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 1,510,255 | 15.103 | 62 | 66 | fits | 114,547 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 1,639,350 | 16.393 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 1,667,524 | 16.675 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 1,692,062 | 16.921 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 1,719,818 | 17.198 | 62 | 66 | fits | 113,624 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 1,825,348 | 18.253 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 1,853,911 | 18.539 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 1,878,816 | 18.788 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 1,906,795 | 19.068 | 62 | 66 | fits | 114,656 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 2,031,924 | 20.319 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 2,055,728 | 20.557 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 2,084,283 | 20.843 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 2,112,646 | 21.126 | 62 | 66 | fits | 111,752 | 398 | 0.063 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if1` | 1,058,372 | 10.584 | 20 | 200 | fits | 163,813 | 144 | 0.530 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 1,038,104 | 10.381 | 20 | 20 | fits | 163,813 | 144 | 0.530 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if1` | 1,114,863 | 11.149 | 20 | 24 | fits | 96,963 | 66 | 0.517 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 998,629 | 9.986 | 20 | 50 | fits | 163,813 | 144 | 0.530 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if1` | 626,422 | 6.264 | 20 | 20 | fits | 162,012 | 60 | 0.383 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 212,898 | 2.129 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if1` | 321,715 | 3.217 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 248,164 | 2.482 | 62 | 66 | fits | 149,640 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 276,668 | 2.767 | 62 | 66 | fits | 149,640 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 372,812 | 3.728 | 62 | 66 | fits | 115,448 | 402 | 0.020 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 400,876 | 4.009 | 62 | 66 | fits | 115,448 | 402 | 0.020 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 549,251 | 5.493 | 62 | 66 | fits | 140,203 | 409 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 577,682 | 5.777 | 62 | 66 | fits | 140,203 | 409 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 664,622 | 6.646 | 62 | 66 | fits | 113,048 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 692,716 | 6.927 | 62 | 66 | fits | 113,048 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 718,231 | 7.182 | 62 | 66 | fits | 113,048 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 745,943 | 7.459 | 62 | 66 | fits | 113,048 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 427,038 | 4.270 | 62 | 66 | fits | 115,448 | 402 | 0.020 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 455,443 | 4.554 | 62 | 66 | fits | 115,448 | 402 | 0.020 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 603,508 | 6.035 | 62 | 66 | fits | 140,203 | 409 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 631,761 | 6.318 | 62 | 66 | fits | 140,203 | 409 | 0.094 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 953,383 | 9.534 | 62 | 66 | fits | 37,763 | 101 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 1,321,879 | 13.219 | 62 | 66 | fits | 39,588 | 102 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 1,684,064 | 16.841 | 62 | 66 | fits | 36,967 | 101 | 0.306 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 2,074,869 | 20.749 | 62 | 66 | fits | 115,685 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 2,100,367 | 21.004 | 62 | 66 | fits | 115,685 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 2,128,163 | 21.282 | 62 | 66 | fits | 115,685 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 2,152,977 | 21.530 | 62 | 66 | fits | 115,685 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 2,274,504 | 22.745 | 62 | 66 | fits | 115,263 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 2,300,356 | 23.004 | 62 | 66 | fits | 115,263 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 2,328,432 | 23.284 | 62 | 66 | fits | 115,263 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 304,711 | 3.047 | 62 | 66 | fits | 149,640 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 335,550 | 3.356 | 62 | 66 | fits | 149,640 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 2,353,145 | 23.531 | 62 | 66 | fits | 115,263 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 2,485,406 | 24.854 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 2,510,727 | 25.107 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 2,538,398 | 25.384 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,562,744 | 25.627 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,671,259 | 26.713 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,696,850 | 26.968 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,724,899 | 27.249 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 2,749,668 | 27.497 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 2,880,004 | 28.800 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 2,904,713 | 29.047 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,928,149 | 29.281 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,956,164 | 29.562 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 3,084,498 | 30.845 | 62 | 66 | fits | 35,100 | 102 | 0.147 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 1,113,082 | 11.131 | 20 | 200 | fits | 163,338 | 164 | 0.516 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,297,939 | 12.979 | 20 | 20 | fits | 168,158 | 136 | 0.560 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 1,368,059 | 13.681 | 20 | 24 | fits | 90,324 | 65 | 0.485 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 1,258,464 | 12.585 | 20 | 50 | fits | 168,158 | 136 | 0.560 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 867,976 | 8.680 | 20 | 20 | fits | 161,709 | 157 | 0.567 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 400,617 | 4.006 | 62 | 66 | fits | 116,773 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 428,490 | 4.285 | 62 | 66 | fits | 116,773 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 518,551 | 5.186 | 62 | 66 | fits | 114,725 | 403 | 0.028 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 546,528 | 5.465 | 62 | 66 | fits | 114,725 | 403 | 0.028 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 572,070 | 5.721 | 62 | 66 | fits | 114,725 | 403 | 0.028 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 600,019 | 6.000 | 62 | 66 | fits | 114,725 | 403 | 0.028 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 803,390 | 8.034 | 62 | 66 | fits | 37,010 | 101 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 1,175,228 | 11.752 | 62 | 66 | fits | 39,911 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 275,449 | 2.754 | 62 | 66 | fits | 151,890 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 304,877 | 3.049 | 62 | 66 | fits | 151,890 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 454,652 | 4.547 | 62 | 66 | fits | 116,773 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 483,057 | 4.831 | 62 | 66 | fits | 116,773 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 1,539,264 | 15.393 | 62 | 66 | fits | 37,990 | 100 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 1,928,907 | 19.289 | 62 | 66 | fits | 117,757 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 1,955,691 | 19.557 | 62 | 66 | fits | 117,757 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 1,983,473 | 19.835 | 62 | 66 | fits | 117,757 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 2,008,917 | 20.089 | 62 | 66 | fits | 117,757 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 2,121,961 | 21.220 | 62 | 66 | fits | 114,499 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 2,147,154 | 21.472 | 62 | 66 | fits | 114,499 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 2,174,904 | 21.749 | 62 | 66 | fits | 114,499 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 2,199,720 | 21.997 | 62 | 66 | fits | 114,499 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 2,321,353 | 23.214 | 62 | 66 | fits | 115,125 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 2,347,138 | 23.471 | 62 | 66 | fits | 115,125 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 2,375,214 | 23.752 | 62 | 66 | fits | 115,125 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 332,766 | 3.328 | 62 | 66 | fits | 151,890 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 363,605 | 3.636 | 62 | 66 | fits | 151,890 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 2,399,918 | 23.999 | 62 | 66 | fits | 115,125 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 2,509,413 | 25.094 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 2,534,734 | 25.347 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 2,562,405 | 25.624 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 2,586,751 | 25.868 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 2,717,750 | 27.177 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,743,341 | 27.433 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 2,771,390 | 27.714 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 2,796,159 | 27.962 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 2,926,552 | 29.266 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 2,951,261 | 29.513 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 2,974,697 | 29.747 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 3,002,712 | 30.027 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 3,109,216 | 31.092 | 62 | 66 | fits | 35,100 | 102 | 0.147 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if1` | 929,544 | 9.295 | 20 | 200 | fits | 160,282 | 151 | 0.554 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 1,118,103 | 11.181 | 20 | 20 | fits | 170,837 | 137 | 0.562 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if1` | 1,206,190 | 12.062 | 20 | 24 | fits | 108,291 | 79 | 0.462 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 1,078,628 | 10.786 | 20 | 50 | fits | 170,837 | 137 | 0.562 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if1` | 847,776 | 8.478 | 20 | 20 | fits | 160,282 | 151 | 0.554 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 374,135 | 3.741 | 62 | 66 | fits | 116,338 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 402,008 | 4.020 | 62 | 66 | fits | 116,338 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 552,167 | 5.522 | 62 | 66 | fits | 139,874 | 409 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 580,551 | 5.806 | 62 | 66 | fits | 139,874 | 409 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 606,217 | 6.062 | 62 | 66 | fits | 139,874 | 409 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 634,166 | 6.342 | 62 | 66 | fits | 139,874 | 409 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 667,201 | 6.672 | 62 | 66 | fits | 112,788 | 402 | 0.020 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 695,295 | 6.953 | 62 | 66 | fits | 112,788 | 402 | 0.020 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 249,222 | 2.492 | 62 | 66 | fits | 151,562 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 278,650 | 2.787 | 62 | 66 | fits | 151,562 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 720,641 | 7.206 | 62 | 66 | fits | 112,788 | 402 | 0.020 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 748,353 | 7.484 | 62 | 66 | fits | 112,788 | 402 | 0.020 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 955,829 | 9.558 | 62 | 66 | fits | 38,147 | 101 | 0.306 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 1,324,469 | 13.245 | 62 | 66 | fits | 39,538 | 102 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 428,555 | 4.286 | 62 | 66 | fits | 116,338 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 457,422 | 4.574 | 62 | 66 | fits | 116,338 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 1,693,358 | 16.934 | 62 | 66 | fits | 37,369 | 101 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 2,076,514 | 20.765 | 62 | 66 | fits | 115,687 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 2,102,014 | 21.020 | 62 | 66 | fits | 115,687 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 2,129,810 | 21.298 | 62 | 66 | fits | 115,687 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 2,154,624 | 21.546 | 62 | 66 | fits | 115,687 | 400 | 0.085 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 2,276,174 | 22.762 | 62 | 66 | fits | 116,125 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 2,302,026 | 23.020 | 62 | 66 | fits | 116,125 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 2,330,102 | 23.301 | 62 | 66 | fits | 116,125 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 2,355,297 | 23.553 | 62 | 66 | fits | 116,125 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 2,465,605 | 24.656 | 62 | 66 | fits | 113,734 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 306,352 | 3.064 | 62 | 66 | fits | 151,562 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 337,278 | 3.373 | 62 | 66 | fits | 151,562 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 2,491,393 | 24.914 | 62 | 66 | fits | 113,734 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 2,519,064 | 25.191 | 62 | 66 | fits | 113,734 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 2,543,410 | 25.434 | 62 | 66 | fits | 113,734 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 2,674,640 | 26.746 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 2,700,231 | 27.002 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 2,728,280 | 27.283 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 2,753,049 | 27.530 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 2,883,442 | 28.834 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 2,908,151 | 29.082 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,931,587 | 29.316 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,959,602 | 29.596 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 3,066,098 | 30.661 | 62 | 66 | fits | 35,100 | 102 | 0.147 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if1` | 1,325,297 | 13.253 | 20 | 200 | fits | 160,002 | 119 | 0.563 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 1,305,029 | 13.050 | 20 | 20 | fits | 160,002 | 119 | 0.563 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if1` | 1,375,366 | 13.754 | 20 | 24 | fits | 90,541 | 65 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 1,068,183 | 10.682 | 20 | 50 | fits | 156,400 | 176 | 0.504 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if1` | 889,758 | 8.898 | 20 | 20 | fits | 175,146 | 163 | 0.561 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 516,280 | 5.163 | 62 | 66 | fits | 114,768 | 403 | 0.027 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 544,099 | 5.441 | 62 | 66 | fits | 114,768 | 403 | 0.027 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 799,865 | 7.999 | 62 | 66 | fits | 37,314 | 101 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,170,824 | 11.708 | 62 | 66 | fits | 39,758 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 274,672 | 2.747 | 62 | 66 | fits | 151,005 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 303,770 | 3.038 | 62 | 66 | fits | 151,005 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 400,108 | 4.001 | 62 | 66 | fits | 115,904 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 428,699 | 4.287 | 62 | 66 | fits | 115,904 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 454,734 | 4.547 | 62 | 66 | fits | 115,904 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 482,908 | 4.829 | 62 | 66 | fits | 115,904 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 1,534,336 | 15.343 | 62 | 66 | fits | 37,716 | 100 | 0.314 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 1,928,421 | 19.284 | 62 | 66 | fits | 117,896 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 569,836 | 5.698 | 62 | 66 | fits | 114,768 | 403 | 0.027 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 598,089 | 5.981 | 62 | 66 | fits | 114,768 | 403 | 0.027 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 1,955,282 | 19.553 | 62 | 66 | fits | 117,896 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 1,983,013 | 19.830 | 62 | 66 | fits | 117,896 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 2,008,522 | 20.085 | 62 | 66 | fits | 117,896 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 2,121,712 | 21.217 | 62 | 66 | fits | 114,671 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 2,146,965 | 21.470 | 62 | 66 | fits | 114,671 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 2,174,761 | 21.748 | 62 | 66 | fits | 114,671 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 2,199,577 | 21.996 | 62 | 66 | fits | 114,671 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 2,321,331 | 23.213 | 62 | 66 | fits | 115,134 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 2,347,116 | 23.471 | 62 | 66 | fits | 115,134 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 2,375,192 | 23.752 | 62 | 66 | fits | 115,134 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 331,733 | 3.317 | 62 | 66 | fits | 151,005 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 362,572 | 3.626 | 62 | 66 | fits | 151,005 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 2,399,905 | 23.999 | 62 | 66 | fits | 115,134 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 2,509,400 | 25.094 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 2,534,721 | 25.347 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 2,562,392 | 25.624 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,586,738 | 25.867 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,717,745 | 27.177 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,743,336 | 27.433 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 2,771,385 | 27.714 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 2,796,154 | 27.962 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 2,926,539 | 29.265 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 2,951,248 | 29.512 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,974,684 | 29.747 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 3,002,699 | 30.027 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 3,109,203 | 31.092 | 62 | 66 | fits | 35,100 | 102 | 0.147 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if1` | 1,121,942 | 11.219 | 20 | 200 | fits | 157,606 | 130 | 0.568 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 1,101,674 | 11.017 | 20 | 20 | fits | 157,606 | 130 | 0.568 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if1` | 1,207,793 | 12.078 | 20 | 24 | fits | 126,323 | 92 | 0.462 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 1,062,199 | 10.622 | 20 | 50 | fits | 157,606 | 130 | 0.568 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if1` | 844,852 | 8.449 | 20 | 20 | fits | 160,255 | 151 | 0.553 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 811,742 | 8.117 | 62 | 66 | fits | 36,812 | 103 | 0.290 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,337,601 | 13.376 | 62 | 66 | fits | 40,068 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,712,417 | 17.124 | 62 | 66 | fits | 37,441 | 101 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 2,106,614 | 21.066 | 62 | 66 | fits | 117,671 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 274,758 | 2.748 | 62 | 66 | fits | 150,925 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 303,856 | 3.039 | 62 | 66 | fits | 150,925 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 400,120 | 4.001 | 62 | 66 | fits | 115,904 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 428,711 | 4.287 | 62 | 66 | fits | 115,904 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 454,746 | 4.547 | 62 | 66 | fits | 115,904 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 482,920 | 4.829 | 62 | 66 | fits | 115,904 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 2,133,458 | 21.335 | 62 | 66 | fits | 117,671 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 2,161,269 | 21.613 | 62 | 66 | fits | 117,671 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 517,137 | 5.171 | 62 | 66 | fits | 116,934 | 403 | 0.028 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 545,728 | 5.457 | 62 | 66 | fits | 116,934 | 403 | 0.028 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 571,609 | 5.716 | 62 | 66 | fits | 116,934 | 403 | 0.028 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 600,014 | 6.000 | 62 | 66 | fits | 116,934 | 403 | 0.028 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 2,186,769 | 21.868 | 62 | 66 | fits | 117,671 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 2,309,380 | 23.094 | 62 | 66 | fits | 115,060 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 2,334,633 | 23.346 | 62 | 66 | fits | 115,060 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 2,362,453 | 23.625 | 62 | 66 | fits | 115,060 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 2,387,267 | 23.873 | 62 | 66 | fits | 115,060 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 2,521,523 | 25.215 | 62 | 66 | fits | 114,750 | 400 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 2,547,375 | 25.474 | 62 | 66 | fits | 114,750 | 400 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 2,575,427 | 25.754 | 62 | 66 | fits | 114,750 | 400 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 331,745 | 3.317 | 62 | 66 | fits | 150,925 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 362,584 | 3.626 | 62 | 66 | fits | 150,925 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 2,600,140 | 26.001 | 62 | 66 | fits | 114,750 | 400 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 2,709,697 | 27.097 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 2,735,018 | 27.350 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 2,762,689 | 27.627 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 2,787,035 | 27.870 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 2,918,270 | 29.183 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 2,943,861 | 29.439 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 2,971,910 | 29.719 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 2,996,679 | 29.967 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 3,157,631 | 31.576 | 62 | 66 | fits | 134,194 | 399 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 3,182,518 | 31.825 | 62 | 66 | fits | 134,194 | 399 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 3,205,954 | 32.060 | 62 | 66 | fits | 134,194 | 399 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 3,233,969 | 32.340 | 62 | 66 | fits | 134,194 | 399 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 3,318,987 | 33.190 | 62 | 66 | fits | 35,100 | 102 | 0.147 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if1` | 1,104,972 | 11.050 | 20 | 200 | fits | 161,159 | 144 | 0.533 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 1,084,704 | 10.847 | 20 | 20 | fits | 161,159 | 144 | 0.533 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if1` | 1,197,189 | 11.972 | 20 | 24 | fits | 95,248 | 74 | 0.519 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 1,045,229 | 10.452 | 20 | 50 | fits | 161,159 | 144 | 0.533 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if1` | 862,045 | 8.620 | 20 | 20 | fits | 175,936 | 164 | 0.559 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 242,868 | 2.429 | 62 | 66 | fits | 124,966 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 271,202 | 2.712 | 62 | 66 | fits | 124,966 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 426,190 | 4.262 | 62 | 66 | fits | 139,714 | 411 | 0.096 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 454,601 | 4.546 | 62 | 66 | fits | 139,714 | 411 | 0.096 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 480,267 | 4.803 | 62 | 66 | fits | 139,714 | 411 | 0.096 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 508,216 | 5.082 | 62 | 66 | fits | 139,714 | 411 | 0.096 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 540,724 | 5.407 | 62 | 66 | fits | 115,132 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 568,739 | 5.687 | 62 | 66 | fits | 115,132 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 594,254 | 5.943 | 62 | 66 | fits | 115,132 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 621,966 | 6.220 | 62 | 66 | fits | 115,132 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 823,170 | 8.232 | 62 | 66 | fits | 37,160 | 103 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 1,349,849 | 13.498 | 62 | 66 | fits | 39,869 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 1,716,124 | 17.161 | 62 | 66 | fits | 37,005 | 100 | 0.312 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 2,127,090 | 21.271 | 62 | 66 | fits | 117,238 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 2,153,699 | 21.537 | 62 | 66 | fits | 117,238 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 2,181,624 | 21.816 | 62 | 66 | fits | 117,238 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 2,207,068 | 22.071 | 62 | 66 | fits | 117,238 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 2,329,802 | 23.298 | 62 | 66 | fits | 115,030 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 2,354,995 | 23.550 | 62 | 66 | fits | 115,030 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,382,849 | 23.828 | 62 | 66 | fits | 115,030 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 2,407,665 | 24.077 | 62 | 66 | fits | 115,030 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 2,518,885 | 25.189 | 62 | 66 | fits | 114,674 | 400 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 2,544,670 | 25.447 | 62 | 66 | fits | 114,674 | 400 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 2,572,722 | 25.727 | 62 | 66 | fits | 114,674 | 400 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 299,166 | 2.992 | 62 | 66 | fits | 124,966 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 330,005 | 3.300 | 62 | 66 | fits | 124,966 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 2,597,426 | 25.974 | 62 | 66 | fits | 114,674 | 400 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 2,729,625 | 27.296 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 2,754,946 | 27.549 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 2,782,617 | 27.826 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 2,806,963 | 28.070 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 2,915,478 | 29.155 | 62 | 66 | fits | 114,111 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 2,941,069 | 29.411 | 62 | 66 | fits | 114,111 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 2,969,118 | 29.691 | 62 | 66 | fits | 114,111 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 2,993,822 | 29.938 | 62 | 66 | fits | 114,111 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 3,124,158 | 31.242 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 3,148,867 | 31.489 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 3,172,303 | 31.723 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 3,200,318 | 32.003 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 3,319,102 | 33.191 | 62 | 66 | fits | 35,725 | 102 | 0.162 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if1` | 1,100,993 | 11.010 | 20 | 200 | fits | 170,350 | 134 | 0.546 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 1,080,725 | 10.807 | 20 | 20 | fits | 170,350 | 134 | 0.546 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if1` | 1,208,865 | 12.089 | 20 | 24 | fits | 111,339 | 88 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 1,041,250 | 10.412 | 20 | 50 | fits | 170,350 | 134 | 0.546 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if1` | 848,875 | 8.489 | 20 | 20 | fits | 158,562 | 154 | 0.573 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 273,932 | 2.739 | 62 | 66 | fits | 149,692 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 302,436 | 3.024 | 62 | 66 | fits | 149,692 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 398,568 | 3.986 | 62 | 66 | fits | 116,202 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 426,632 | 4.266 | 62 | 66 | fits | 116,202 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 452,232 | 4.522 | 62 | 66 | fits | 116,202 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 480,181 | 4.802 | 62 | 66 | fits | 116,202 | 402 | 0.021 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 515,396 | 5.154 | 62 | 66 | fits | 113,895 | 403 | 0.027 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 543,438 | 5.434 | 62 | 66 | fits | 113,895 | 403 | 0.027 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 568,953 | 5.690 | 62 | 66 | fits | 113,895 | 403 | 0.027 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 596,665 | 5.967 | 62 | 66 | fits | 113,895 | 403 | 0.027 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 807,355 | 8.074 | 62 | 66 | fits | 36,650 | 103 | 0.281 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 1,332,948 | 13.329 | 62 | 66 | fits | 39,913 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 1,707,882 | 17.079 | 62 | 66 | fits | 37,436 | 101 | 0.319 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 2,126,576 | 21.266 | 62 | 66 | fits | 117,238 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 2,153,185 | 21.532 | 62 | 66 | fits | 117,238 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 2,181,110 | 21.811 | 62 | 66 | fits | 117,238 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 2,206,554 | 22.066 | 62 | 66 | fits | 117,238 | 400 | 0.088 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 2,329,239 | 23.292 | 62 | 66 | fits | 115,030 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 2,354,432 | 23.544 | 62 | 66 | fits | 115,030 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,382,286 | 23.823 | 62 | 66 | fits | 115,030 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,407,102 | 24.071 | 62 | 66 | fits | 115,030 | 400 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,518,327 | 25.183 | 62 | 66 | fits | 114,674 | 400 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 2,544,112 | 25.441 | 62 | 66 | fits | 114,674 | 400 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 2,572,164 | 25.722 | 62 | 66 | fits | 114,674 | 400 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 330,469 | 3.305 | 62 | 66 | fits | 149,692 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 361,308 | 3.613 | 62 | 66 | fits | 149,692 | 409 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 2,596,868 | 25.969 | 62 | 66 | fits | 114,674 | 400 | 0.061 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 2,729,295 | 27.293 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 2,754,616 | 27.546 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 2,782,287 | 27.823 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 2,806,633 | 28.066 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 2,915,151 | 29.152 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 2,940,742 | 29.407 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 2,968,791 | 29.688 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 2,993,560 | 29.936 | 62 | 66 | fits | 114,176 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 3,123,668 | 31.237 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 3,148,377 | 31.484 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 3,171,813 | 31.718 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 3,199,828 | 31.998 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 3,318,607 | 33.186 | 62 | 66 | fits | 35,725 | 102 | 0.162 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if1` | 1,099,118 | 10.991 | 20 | 200 | fits | 161,224 | 144 | 0.533 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 1,078,850 | 10.789 | 20 | 20 | fits | 161,224 | 144 | 0.533 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if1` | 1,191,330 | 11.913 | 20 | 24 | fits | 95,248 | 74 | 0.518 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 1,039,375 | 10.394 | 20 | 50 | fits | 161,224 | 144 | 0.533 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if1` | 856,126 | 8.561 | 20 | 20 | fits | 176,080 | 164 | 0.559 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 248,164 | 2.482 | 62 | 66 | fits | 149,640 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 276,668 | 2.767 | 62 | 66 | fits | 149,640 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 372,812 | 3.728 | 62 | 66 | fits | 114,443 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 400,876 | 4.009 | 62 | 66 | fits | 114,443 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 426,476 | 4.265 | 62 | 66 | fits | 114,443 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 454,425 | 4.544 | 62 | 66 | fits | 114,443 | 402 | 0.022 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 547,611 | 5.476 | 62 | 66 | fits | 139,889 | 409 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 575,981 | 5.760 | 62 | 66 | fits | 139,889 | 409 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 663,338 | 6.633 | 62 | 66 | fits | 114,749 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 691,209 | 6.912 | 62 | 66 | fits | 114,749 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 954,102 | 9.541 | 62 | 66 | fits | 37,904 | 101 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 1,322,570 | 13.226 | 62 | 66 | fits | 39,473 | 102 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 601,970 | 6.020 | 62 | 66 | fits | 139,889 | 409 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 630,223 | 6.302 | 62 | 66 | fits | 139,889 | 409 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 716,619 | 7.166 | 62 | 66 | fits | 114,749 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 744,562 | 7.446 | 62 | 66 | fits | 114,749 | 402 | 0.023 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 1,684,647 | 16.846 | 62 | 66 | fits | 36,961 | 101 | 0.306 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 2,075,356 | 20.754 | 62 | 66 | fits | 115,679 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 2,100,854 | 21.009 | 62 | 66 | fits | 115,679 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 2,128,650 | 21.287 | 62 | 66 | fits | 115,679 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 2,153,464 | 21.535 | 62 | 66 | fits | 115,679 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 2,274,967 | 22.750 | 62 | 66 | fits | 115,254 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 2,300,819 | 23.008 | 62 | 66 | fits | 115,254 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 2,328,895 | 23.289 | 62 | 66 | fits | 115,254 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 304,711 | 3.047 | 62 | 66 | fits | 149,640 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 335,550 | 3.356 | 62 | 66 | fits | 149,640 | 409 | 0.102 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 2,353,599 | 23.536 | 62 | 66 | fits | 115,254 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 2,485,860 | 24.859 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 2,511,181 | 25.112 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 2,538,852 | 25.389 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 2,563,198 | 25.632 | 62 | 66 | fits | 113,113 | 400 | 0.064 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 2,694,482 | 26.945 | 62 | 66 | fits | 114,111 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 2,720,073 | 27.201 | 62 | 66 | fits | 114,111 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 2,748,122 | 27.481 | 62 | 66 | fits | 114,111 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 2,772,826 | 27.728 | 62 | 66 | fits | 114,111 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 2,880,755 | 28.808 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 2,905,464 | 29.055 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,928,900 | 29.289 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,956,915 | 29.569 | 62 | 66 | fits | 111,835 | 399 | 0.062 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 3,085,192 | 30.852 | 62 | 66 | fits | 35,100 | 102 | 0.147 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if1` | 1,110,761 | 11.108 | 20 | 200 | fits | 163,308 | 164 | 0.516 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 1,295,576 | 12.956 | 20 | 20 | fits | 168,122 | 136 | 0.560 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if1` | 1,365,666 | 13.657 | 20 | 24 | fits | 90,294 | 65 | 0.485 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 1,256,101 | 12.561 | 20 | 50 | fits | 168,122 | 136 | 0.560 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if1` | 865,685 | 8.657 | 20 | 20 | fits | 161,593 | 157 | 0.566 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
