### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 736 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.acmp.if0` (notice-burst-2) | 15.893 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-7.held.adp.if1` (notice-burst-7) | 13.218 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-burst-6.held.aecp.if1` (notice-burst-6) | 15.982 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.maap.if0` (notice-burst-2) | 12.677 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-burst-2.held.srp.if1` (notice-burst-2) | 8.566 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-7.mrpdu.periodic.if0` (notice-every-7) | 2.170 | fits | 0 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-7.mrpdu.periodic.if1` (notice-every-7) | 3.263 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-4.notices.29.36.0.if0` (notice-burst-4) | 33.228 (33.548) | fits | 1 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 998 | 0 | 180,517 (1.805) | fits |
| notice-every-1 | 1000 | 0 | 178,223 (1.782) | fits |
| notice-every-2 | 1000 | 0 | 186,213 (1.862) | fits |
| notice-every-3 | 997 | 0 | 171,417 (1.714) | fits |
| notice-every-4 | 991 | 0 | 180,886 (1.809) | fits |
| notice-every-5 | 994 | 0 | 173,864 (1.739) | fits |
| notice-every-6 | 989 | 0 | 173,681 (1.737) | fits |
| notice-every-7 | 989 | 0 | 172,358 (1.724) | fits |
| notice-burst-0 | 803 | 0 | 182,143 (1.821) | fits |
| notice-burst-1 | 796 | 0 | 182,092 (1.821) | fits |
| notice-burst-2 | 809 | 0 | 181,222 (1.812) | fits |
| notice-burst-3 | 800 | 0 | 175,887 (1.759) | fits |
| notice-burst-4 | 792 | 0 | 182,096 (1.821) | fits |
| notice-burst-5 | 799 | 0 | 180,272 (1.803) | fits |
| notice-burst-6 | 793 | 0 | 168,483 (1.685) | fits |
| notice-burst-7 | 800 | 0 | 180,317 (1.803) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.462 | 62 | 32 | 1 | within |
| notice-every-0 | 4.752 | 62 | 32 | 1 | within |
| notice-every-0 | 6.246 | 62 | 32 | 1 | within |
| notice-every-0 | 6.533 | 62 | 32 | 1 | within |
| notice-every-0 | 2.322 | 62 | 32 | 1 | within |
| notice-every-0 | 2.619 | 62 | 32 | 1 | within |
| notice-every-0 | 8.255 | 62 | 32 | 1 | within |
| notice-every-0 | 8.542 | 62 | 32 | 1 | within |
| notice-every-0 | 2.890 | 62 | 32 | 1 | within |
| notice-every-0 | 3.177 | 62 | 32 | 1 | within |
| notice-every-0 | 5.019 | 62 | 32 | 1 | within |
| notice-every-0 | 5.303 | 62 | 32 | 1 | within |
| notice-every-0 | 6.798 | 62 | 32 | 1 | within |
| notice-every-0 | 7.081 | 62 | 32 | 1 | within |
| notice-every-0 | 8.803 | 62 | 32 | 1 | within |
| notice-every-0 | 9.083 | 62 | 32 | 1 | within |
| notice-every-0 | 10.252 | 62 | 32 | 1 | within |
| notice-every-0 | 10.538 | 62 | 32 | 1 | within |
| notice-every-0 | 10.790 | 62 | 32 | 1 | within |
| notice-every-0 | 11.070 | 62 | 32 | 1 | within |
| notice-every-0 | 12.541 | 62 | 32 | 1 | within |
| notice-every-0 | 12.834 | 62 | 32 | 1 | within |
| notice-every-0 | 13.093 | 62 | 32 | 1 | within |
| notice-every-0 | 13.376 | 62 | 32 | 1 | within |
| notice-every-0 | 14.271 | 62 | 32 | 1 | within |
| notice-every-0 | 14.561 | 62 | 32 | 1 | within |
| notice-every-0 | 14.816 | 62 | 32 | 1 | within |
| notice-every-0 | 15.095 | 62 | 32 | 1 | within |
| notice-every-0 | 16.446 | 62 | 32 | 1 | within |
| notice-every-0 | 16.732 | 62 | 32 | 1 | within |
| notice-every-0 | 16.985 | 62 | 32 | 1 | within |
| notice-every-0 | 17.266 | 62 | 32 | 1 | within |
| notice-every-0 | 18.372 | 62 | 32 | 1 | within |
| notice-every-0 | 18.661 | 62 | 32 | 1 | within |
| notice-every-0 | 18.915 | 62 | 32 | 1 | within |
| notice-every-0 | 19.198 | 62 | 32 | 1 | within |
| notice-every-0 | 20.275 | 62 | 32 | 1 | within |
| notice-every-0 | 20.520 | 62 | 32 | 1 | within |
| notice-every-0 | 20.806 | 62 | 32 | 1 | within |
| notice-every-0 | 21.093 | 62 | 32 | 1 | within |
| notice-every-1 | 4.462 | 62 | 32 | 1 | within |
| notice-every-1 | 4.751 | 62 | 32 | 1 | within |
| notice-every-1 | 6.559 | 62 | 32 | 1 | within |
| notice-every-1 | 6.846 | 62 | 32 | 1 | within |
| notice-every-1 | 2.322 | 62 | 32 | 1 | within |
| notice-every-1 | 2.619 | 62 | 32 | 1 | within |
| notice-every-1 | 8.306 | 62 | 32 | 1 | within |
| notice-every-1 | 8.594 | 62 | 32 | 1 | within |
| notice-every-1 | 2.890 | 62 | 32 | 1 | within |
| notice-every-1 | 3.177 | 62 | 32 | 1 | within |
| notice-every-1 | 5.018 | 62 | 32 | 1 | within |
| notice-every-1 | 5.303 | 62 | 32 | 1 | within |
| notice-every-1 | 7.111 | 62 | 32 | 1 | within |
| notice-every-1 | 7.394 | 62 | 32 | 1 | within |
| notice-every-1 | 8.855 | 62 | 32 | 1 | within |
| notice-every-1 | 9.135 | 62 | 32 | 1 | within |
| notice-every-1 | 10.305 | 62 | 32 | 1 | within |
| notice-every-1 | 10.590 | 62 | 32 | 1 | within |
| notice-every-1 | 10.842 | 62 | 32 | 1 | within |
| notice-every-1 | 11.121 | 62 | 32 | 1 | within |
| notice-every-1 | 12.258 | 62 | 32 | 1 | within |
| notice-every-1 | 12.550 | 62 | 32 | 1 | within |
| notice-every-1 | 12.808 | 62 | 32 | 1 | within |
| notice-every-1 | 13.091 | 62 | 32 | 1 | within |
| notice-every-1 | 14.321 | 62 | 32 | 1 | within |
| notice-every-1 | 14.612 | 62 | 32 | 1 | within |
| notice-every-1 | 14.868 | 62 | 32 | 1 | within |
| notice-every-1 | 15.147 | 62 | 32 | 1 | within |
| notice-every-1 | 16.263 | 62 | 32 | 1 | within |
| notice-every-1 | 16.549 | 62 | 32 | 1 | within |
| notice-every-1 | 16.802 | 62 | 32 | 1 | within |
| notice-every-1 | 17.083 | 62 | 32 | 1 | within |
| notice-every-1 | 18.422 | 62 | 32 | 1 | within |
| notice-every-1 | 18.710 | 62 | 32 | 1 | within |
| notice-every-1 | 18.965 | 62 | 32 | 1 | within |
| notice-every-1 | 19.248 | 62 | 32 | 1 | within |
| notice-every-1 | 20.324 | 62 | 32 | 1 | within |
| notice-every-1 | 20.568 | 62 | 32 | 1 | within |
| notice-every-1 | 20.855 | 62 | 32 | 1 | within |
| notice-every-1 | 21.142 | 62 | 32 | 1 | within |
| notice-every-2 | 4.211 | 62 | 32 | 1 | within |
| notice-every-2 | 4.501 | 62 | 32 | 1 | within |
| notice-every-2 | 6.244 | 62 | 32 | 1 | within |
| notice-every-2 | 6.531 | 62 | 32 | 1 | within |
| notice-every-2 | 2.071 | 62 | 32 | 1 | within |
| notice-every-2 | 2.368 | 62 | 32 | 1 | within |
| notice-every-2 | 8.252 | 62 | 32 | 1 | within |
| notice-every-2 | 8.540 | 62 | 32 | 1 | within |
| notice-every-2 | 2.640 | 62 | 32 | 1 | within |
| notice-every-2 | 2.927 | 62 | 32 | 1 | within |
| notice-every-2 | 4.768 | 62 | 32 | 1 | within |
| notice-every-2 | 5.053 | 62 | 32 | 1 | within |
| notice-every-2 | 6.796 | 62 | 32 | 1 | within |
| notice-every-2 | 7.079 | 62 | 32 | 1 | within |
| notice-every-2 | 8.801 | 62 | 32 | 1 | within |
| notice-every-2 | 9.081 | 62 | 32 | 1 | within |
| notice-every-2 | 10.247 | 62 | 32 | 1 | within |
| notice-every-2 | 10.533 | 62 | 32 | 1 | within |
| notice-every-2 | 10.785 | 62 | 32 | 1 | within |
| notice-every-2 | 11.064 | 62 | 32 | 1 | within |
| notice-every-2 | 12.201 | 62 | 32 | 1 | within |
| notice-every-2 | 12.492 | 62 | 32 | 1 | within |
| notice-every-2 | 12.751 | 62 | 32 | 1 | within |
| notice-every-2 | 13.034 | 62 | 32 | 1 | within |
| notice-every-2 | 14.264 | 62 | 32 | 1 | within |
| notice-every-2 | 14.555 | 62 | 32 | 1 | within |
| notice-every-2 | 14.810 | 62 | 32 | 1 | within |
| notice-every-2 | 15.090 | 62 | 32 | 1 | within |
| notice-every-2 | 16.206 | 62 | 32 | 1 | within |
| notice-every-2 | 16.492 | 62 | 32 | 1 | within |
| notice-every-2 | 16.745 | 62 | 32 | 1 | within |
| notice-every-2 | 17.026 | 62 | 32 | 1 | within |
| notice-every-2 | 18.132 | 62 | 32 | 1 | within |
| notice-every-2 | 18.420 | 62 | 32 | 1 | within |
| notice-every-2 | 18.674 | 62 | 32 | 1 | within |
| notice-every-2 | 18.958 | 62 | 32 | 1 | within |
| notice-every-2 | 20.035 | 62 | 32 | 1 | within |
| notice-every-2 | 20.279 | 62 | 32 | 1 | within |
| notice-every-2 | 20.566 | 62 | 32 | 1 | within |
| notice-every-2 | 20.852 | 62 | 32 | 1 | within |
| notice-every-3 | 4.530 | 62 | 32 | 1 | within |
| notice-every-3 | 4.820 | 62 | 32 | 1 | within |
| notice-every-3 | 6.301 | 62 | 32 | 1 | within |
| notice-every-3 | 6.588 | 62 | 32 | 1 | within |
| notice-every-3 | 2.322 | 62 | 32 | 1 | within |
| notice-every-3 | 2.619 | 62 | 32 | 1 | within |
| notice-every-3 | 8.311 | 62 | 32 | 1 | within |
| notice-every-3 | 8.598 | 62 | 32 | 1 | within |
| notice-every-3 | 2.891 | 62 | 32 | 1 | within |
| notice-every-3 | 3.178 | 62 | 32 | 1 | within |
| notice-every-3 | 5.087 | 62 | 32 | 1 | within |
| notice-every-3 | 5.371 | 62 | 32 | 1 | within |
| notice-every-3 | 6.853 | 62 | 32 | 1 | within |
| notice-every-3 | 7.137 | 62 | 32 | 1 | within |
| notice-every-3 | 8.860 | 62 | 32 | 1 | within |
| notice-every-3 | 9.139 | 62 | 32 | 1 | within |
| notice-every-3 | 10.309 | 62 | 32 | 1 | within |
| notice-every-3 | 10.595 | 62 | 32 | 1 | within |
| notice-every-3 | 10.847 | 62 | 32 | 1 | within |
| notice-every-3 | 11.126 | 62 | 32 | 1 | within |
| notice-every-3 | 12.263 | 62 | 32 | 1 | within |
| notice-every-3 | 12.554 | 62 | 32 | 1 | within |
| notice-every-3 | 12.813 | 62 | 32 | 1 | within |
| notice-every-3 | 13.096 | 62 | 32 | 1 | within |
| notice-every-3 | 14.326 | 62 | 32 | 1 | within |
| notice-every-3 | 14.617 | 62 | 32 | 1 | within |
| notice-every-3 | 14.872 | 62 | 32 | 1 | within |
| notice-every-3 | 15.151 | 62 | 32 | 1 | within |
| notice-every-3 | 16.268 | 62 | 32 | 1 | within |
| notice-every-3 | 16.554 | 62 | 32 | 1 | within |
| notice-every-3 | 16.807 | 62 | 32 | 1 | within |
| notice-every-3 | 17.088 | 62 | 32 | 1 | within |
| notice-every-3 | 18.426 | 62 | 32 | 1 | within |
| notice-every-3 | 18.715 | 62 | 32 | 1 | within |
| notice-every-3 | 18.969 | 62 | 32 | 1 | within |
| notice-every-3 | 19.253 | 62 | 32 | 1 | within |
| notice-every-3 | 20.328 | 62 | 32 | 1 | within |
| notice-every-3 | 20.572 | 62 | 32 | 1 | within |
| notice-every-3 | 20.859 | 62 | 32 | 1 | within |
| notice-every-3 | 21.146 | 62 | 32 | 1 | within |
| notice-every-4 | 2.316 | 62 | 32 | 1 | within |
| notice-every-4 | 2.606 | 62 | 32 | 1 | within |
| notice-every-4 | 4.183 | 62 | 32 | 1 | within |
| notice-every-4 | 4.473 | 62 | 32 | 1 | within |
| notice-every-4 | 6.226 | 62 | 32 | 1 | within |
| notice-every-4 | 6.515 | 62 | 32 | 1 | within |
| notice-every-4 | 8.237 | 62 | 32 | 1 | within |
| notice-every-4 | 8.524 | 62 | 32 | 1 | within |
| notice-every-4 | 2.878 | 62 | 32 | 1 | within |
| notice-every-4 | 3.165 | 62 | 32 | 1 | within |
| notice-every-4 | 4.739 | 62 | 32 | 1 | within |
| notice-every-4 | 5.024 | 62 | 32 | 1 | within |
| notice-every-4 | 6.780 | 62 | 32 | 1 | within |
| notice-every-4 | 7.063 | 62 | 32 | 1 | within |
| notice-every-4 | 8.786 | 62 | 32 | 1 | within |
| notice-every-4 | 9.065 | 62 | 32 | 1 | within |
| notice-every-4 | 10.235 | 62 | 32 | 1 | within |
| notice-every-4 | 10.520 | 62 | 32 | 1 | within |
| notice-every-4 | 10.772 | 62 | 32 | 1 | within |
| notice-every-4 | 11.051 | 62 | 32 | 1 | within |
| notice-every-4 | 12.189 | 62 | 32 | 1 | within |
| notice-every-4 | 12.479 | 62 | 32 | 1 | within |
| notice-every-4 | 12.738 | 62 | 32 | 1 | within |
| notice-every-4 | 13.021 | 62 | 32 | 1 | within |
| notice-every-4 | 14.250 | 62 | 32 | 1 | within |
| notice-every-4 | 14.541 | 62 | 32 | 1 | within |
| notice-every-4 | 14.796 | 62 | 32 | 1 | within |
| notice-every-4 | 15.076 | 62 | 32 | 1 | within |
| notice-every-4 | 16.192 | 62 | 32 | 1 | within |
| notice-every-4 | 16.478 | 62 | 32 | 1 | within |
| notice-every-4 | 16.731 | 62 | 32 | 1 | within |
| notice-every-4 | 17.012 | 62 | 32 | 1 | within |
| notice-every-4 | 18.351 | 62 | 32 | 1 | within |
| notice-every-4 | 18.639 | 62 | 32 | 1 | within |
| notice-every-4 | 18.893 | 62 | 32 | 1 | within |
| notice-every-4 | 19.177 | 62 | 32 | 1 | within |
| notice-every-4 | 20.252 | 62 | 32 | 1 | within |
| notice-every-4 | 20.497 | 62 | 32 | 1 | within |
| notice-every-4 | 20.783 | 62 | 32 | 1 | within |
| notice-every-4 | 21.070 | 62 | 32 | 1 | within |
| notice-every-5 | 2.317 | 62 | 32 | 1 | within |
| notice-every-5 | 2.608 | 62 | 32 | 1 | within |
| notice-every-5 | 4.182 | 62 | 32 | 1 | within |
| notice-every-5 | 4.471 | 62 | 32 | 1 | within |
| notice-every-5 | 6.225 | 62 | 32 | 1 | within |
| notice-every-5 | 6.514 | 62 | 32 | 1 | within |
| notice-every-5 | 8.236 | 62 | 32 | 1 | within |
| notice-every-5 | 8.523 | 62 | 32 | 1 | within |
| notice-every-5 | 2.879 | 62 | 32 | 1 | within |
| notice-every-5 | 3.166 | 62 | 32 | 1 | within |
| notice-every-5 | 4.738 | 62 | 32 | 1 | within |
| notice-every-5 | 5.022 | 62 | 32 | 1 | within |
| notice-every-5 | 6.779 | 62 | 32 | 1 | within |
| notice-every-5 | 7.062 | 62 | 32 | 1 | within |
| notice-every-5 | 8.784 | 62 | 32 | 1 | within |
| notice-every-5 | 9.064 | 62 | 32 | 1 | within |
| notice-every-5 | 10.234 | 62 | 32 | 1 | within |
| notice-every-5 | 10.519 | 62 | 32 | 1 | within |
| notice-every-5 | 10.771 | 62 | 32 | 1 | within |
| notice-every-5 | 11.051 | 62 | 32 | 1 | within |
| notice-every-5 | 12.188 | 62 | 32 | 1 | within |
| notice-every-5 | 12.478 | 62 | 32 | 1 | within |
| notice-every-5 | 12.737 | 62 | 32 | 1 | within |
| notice-every-5 | 13.020 | 62 | 32 | 1 | within |
| notice-every-5 | 14.249 | 62 | 32 | 1 | within |
| notice-every-5 | 14.540 | 62 | 32 | 1 | within |
| notice-every-5 | 14.796 | 62 | 32 | 1 | within |
| notice-every-5 | 15.075 | 62 | 32 | 1 | within |
| notice-every-5 | 16.191 | 62 | 32 | 1 | within |
| notice-every-5 | 16.477 | 62 | 32 | 1 | within |
| notice-every-5 | 16.730 | 62 | 32 | 1 | within |
| notice-every-5 | 17.011 | 62 | 32 | 1 | within |
| notice-every-5 | 18.117 | 62 | 32 | 1 | within |
| notice-every-5 | 18.405 | 62 | 32 | 1 | within |
| notice-every-5 | 18.660 | 62 | 32 | 1 | within |
| notice-every-5 | 18.943 | 62 | 32 | 1 | within |
| notice-every-5 | 20.250 | 62 | 32 | 1 | within |
| notice-every-5 | 20.494 | 62 | 32 | 1 | within |
| notice-every-5 | 20.781 | 62 | 32 | 1 | within |
| notice-every-5 | 21.067 | 62 | 32 | 1 | within |
| notice-every-6 | 6.247 | 62 | 32 | 1 | within |
| notice-every-6 | 6.533 | 62 | 32 | 1 | within |
| notice-every-6 | 2.071 | 62 | 32 | 1 | within |
| notice-every-6 | 2.364 | 62 | 32 | 1 | within |
| notice-every-6 | 4.211 | 62 | 32 | 1 | within |
| notice-every-6 | 4.505 | 62 | 32 | 1 | within |
| notice-every-6 | 8.319 | 62 | 32 | 1 | within |
| notice-every-6 | 8.606 | 62 | 32 | 1 | within |
| notice-every-6 | 2.636 | 62 | 32 | 1 | within |
| notice-every-6 | 2.923 | 62 | 32 | 1 | within |
| notice-every-6 | 4.772 | 62 | 32 | 1 | within |
| notice-every-6 | 5.057 | 62 | 32 | 1 | within |
| notice-every-6 | 6.798 | 62 | 32 | 1 | within |
| notice-every-6 | 7.081 | 62 | 32 | 1 | within |
| notice-every-6 | 8.867 | 62 | 32 | 1 | within |
| notice-every-6 | 9.147 | 62 | 32 | 1 | within |
| notice-every-6 | 10.059 | 62 | 32 | 1 | within |
| notice-every-6 | 10.344 | 62 | 32 | 1 | within |
| notice-every-6 | 10.596 | 62 | 32 | 1 | within |
| notice-every-6 | 10.876 | 62 | 32 | 1 | within |
| notice-every-6 | 12.347 | 62 | 32 | 1 | within |
| notice-every-6 | 12.639 | 62 | 32 | 1 | within |
| notice-every-6 | 12.898 | 62 | 32 | 1 | within |
| notice-every-6 | 13.182 | 62 | 32 | 1 | within |
| notice-every-6 | 14.076 | 62 | 32 | 1 | within |
| notice-every-6 | 14.366 | 62 | 32 | 1 | within |
| notice-every-6 | 14.621 | 62 | 32 | 1 | within |
| notice-every-6 | 14.900 | 62 | 32 | 1 | within |
| notice-every-6 | 16.015 | 62 | 32 | 1 | within |
| notice-every-6 | 16.301 | 62 | 32 | 1 | within |
| notice-every-6 | 16.554 | 62 | 32 | 1 | within |
| notice-every-6 | 16.835 | 62 | 32 | 1 | within |
| notice-every-6 | 18.172 | 62 | 32 | 1 | within |
| notice-every-6 | 18.460 | 62 | 32 | 1 | within |
| notice-every-6 | 18.715 | 62 | 32 | 1 | within |
| notice-every-6 | 18.998 | 62 | 32 | 1 | within |
| notice-every-6 | 20.075 | 62 | 32 | 1 | within |
| notice-every-6 | 20.320 | 62 | 32 | 1 | within |
| notice-every-6 | 20.606 | 62 | 32 | 1 | within |
| notice-every-6 | 20.893 | 62 | 32 | 1 | within |
| notice-every-7 | 2.317 | 62 | 32 | 1 | within |
| notice-every-7 | 2.608 | 62 | 32 | 1 | within |
| notice-every-7 | 4.182 | 62 | 32 | 1 | within |
| notice-every-7 | 4.471 | 62 | 32 | 1 | within |
| notice-every-7 | 6.225 | 62 | 32 | 1 | within |
| notice-every-7 | 6.514 | 62 | 32 | 1 | within |
| notice-every-7 | 8.236 | 62 | 32 | 1 | within |
| notice-every-7 | 8.523 | 62 | 32 | 1 | within |
| notice-every-7 | 2.879 | 62 | 32 | 1 | within |
| notice-every-7 | 3.166 | 62 | 32 | 1 | within |
| notice-every-7 | 4.738 | 62 | 32 | 1 | within |
| notice-every-7 | 5.022 | 62 | 32 | 1 | within |
| notice-every-7 | 6.778 | 62 | 32 | 1 | within |
| notice-every-7 | 7.062 | 62 | 32 | 1 | within |
| notice-every-7 | 8.784 | 62 | 32 | 1 | within |
| notice-every-7 | 9.064 | 62 | 32 | 1 | within |
| notice-every-7 | 10.234 | 62 | 32 | 1 | within |
| notice-every-7 | 10.519 | 62 | 32 | 1 | within |
| notice-every-7 | 10.771 | 62 | 32 | 1 | within |
| notice-every-7 | 11.051 | 62 | 32 | 1 | within |
| notice-every-7 | 12.188 | 62 | 32 | 1 | within |
| notice-every-7 | 12.478 | 62 | 32 | 1 | within |
| notice-every-7 | 12.737 | 62 | 32 | 1 | within |
| notice-every-7 | 13.020 | 62 | 32 | 1 | within |
| notice-every-7 | 14.249 | 62 | 32 | 1 | within |
| notice-every-7 | 14.540 | 62 | 32 | 1 | within |
| notice-every-7 | 14.795 | 62 | 32 | 1 | within |
| notice-every-7 | 15.075 | 62 | 32 | 1 | within |
| notice-every-7 | 16.191 | 62 | 32 | 1 | within |
| notice-every-7 | 16.477 | 62 | 32 | 1 | within |
| notice-every-7 | 16.730 | 62 | 32 | 1 | within |
| notice-every-7 | 17.011 | 62 | 32 | 1 | within |
| notice-every-7 | 18.350 | 62 | 32 | 1 | within |
| notice-every-7 | 18.638 | 62 | 32 | 1 | within |
| notice-every-7 | 18.892 | 62 | 32 | 1 | within |
| notice-every-7 | 19.176 | 62 | 32 | 1 | within |
| notice-every-7 | 20.251 | 62 | 32 | 1 | within |
| notice-every-7 | 20.496 | 62 | 32 | 1 | within |
| notice-every-7 | 20.782 | 62 | 32 | 1 | within |
| notice-every-7 | 21.069 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.511 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.793 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.263 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.550 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.813 | 62 | 32 | 1 | within |
| notice-burst-0 | 6.097 | 62 | 32 | 1 | within |
| notice-burst-0 | 8.297 | 62 | 32 | 1 | within |
| notice-burst-0 | 13.533 | 62 | 32 | 1 | within |
| notice-burst-0 | 17.191 | 62 | 32 | 1 | within |
| notice-burst-0 | 21.353 | 62 | 32 | 1 | within |
| notice-burst-0 | 21.630 | 62 | 32 | 1 | within |
| notice-burst-0 | 21.913 | 62 | 32 | 1 | within |
| notice-burst-0 | 22.173 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.182 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.455 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.738 | 62 | 32 | 1 | within |
| notice-burst-0 | 24.000 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.174 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.435 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.715 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.971 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.117 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.386 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.671 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.207 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.530 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.817 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.128 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.075 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.384 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.928 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.058 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.324 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.607 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.861 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.217 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.475 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.716 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.997 | 62 | 32 | 1 | within |
| notice-burst-0 | 33.202 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.489 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.771 | 62 | 32 | 1 | within |
| notice-burst-1 | 8.289 | 62 | 32 | 1 | within |
| notice-burst-1 | 13.525 | 62 | 32 | 1 | within |
| notice-burst-1 | 17.174 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.316 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.594 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.879 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.235 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.528 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.796 | 62 | 32 | 1 | within |
| notice-burst-1 | 6.083 | 62 | 32 | 1 | within |
| notice-burst-1 | 22.141 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.148 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.420 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.703 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.965 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.136 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.397 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.677 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.197 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.513 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.795 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.101 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.049 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.353 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.928 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.066 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.331 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.612 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.864 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.227 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.493 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.776 | 62 | 32 | 1 | within |
| notice-burst-1 | 30.030 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.152 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.410 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.651 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.932 | 62 | 32 | 1 | within |
| notice-burst-1 | 33.138 | 62 | 32 | 1 | within |
| notice-burst-2 | 5.288 | 62 | 32 | 1 | within |
| notice-burst-2 | 5.573 | 62 | 32 | 1 | within |
| notice-burst-2 | 5.837 | 62 | 32 | 1 | within |
| notice-burst-2 | 6.118 | 62 | 32 | 1 | within |
| notice-burst-2 | 8.227 | 62 | 32 | 1 | within |
| notice-burst-2 | 11.875 | 62 | 32 | 1 | within |
| notice-burst-2 | 3.544 | 62 | 32 | 1 | within |
| notice-burst-2 | 3.835 | 62 | 32 | 1 | within |
| notice-burst-2 | 15.642 | 62 | 32 | 1 | within |
| notice-burst-2 | 19.531 | 62 | 32 | 1 | within |
| notice-burst-2 | 19.809 | 62 | 32 | 1 | within |
| notice-burst-2 | 20.091 | 62 | 32 | 1 | within |
| notice-burst-2 | 20.352 | 62 | 32 | 1 | within |
| notice-burst-2 | 22.354 | 62 | 32 | 1 | within |
| notice-burst-2 | 22.630 | 62 | 32 | 1 | within |
| notice-burst-2 | 22.913 | 62 | 32 | 1 | within |
| notice-burst-2 | 23.176 | 62 | 32 | 1 | within |
| notice-burst-2 | 24.439 | 62 | 32 | 1 | within |
| notice-burst-2 | 24.700 | 62 | 32 | 1 | within |
| notice-burst-2 | 24.981 | 62 | 32 | 1 | within |
| notice-burst-2 | 2.259 | 62 | 32 | 1 | within |
| notice-burst-2 | 2.575 | 62 | 32 | 1 | within |
| notice-burst-2 | 2.857 | 62 | 32 | 1 | within |
| notice-burst-2 | 3.163 | 62 | 32 | 1 | within |
| notice-burst-2 | 4.112 | 62 | 32 | 1 | within |
| notice-burst-2 | 4.417 | 62 | 32 | 1 | within |
| notice-burst-2 | 25.232 | 62 | 32 | 1 | within |
| notice-burst-2 | 26.370 | 62 | 32 | 1 | within |
| notice-burst-2 | 26.635 | 62 | 32 | 1 | within |
| notice-burst-2 | 26.916 | 62 | 32 | 1 | within |
| notice-burst-2 | 27.168 | 62 | 32 | 1 | within |
| notice-burst-2 | 28.295 | 62 | 32 | 1 | within |
| notice-burst-2 | 28.561 | 62 | 32 | 1 | within |
| notice-burst-2 | 28.844 | 62 | 32 | 1 | within |
| notice-burst-2 | 29.098 | 62 | 32 | 1 | within |
| notice-burst-2 | 30.452 | 62 | 32 | 1 | within |
| notice-burst-2 | 30.710 | 62 | 32 | 1 | within |
| notice-burst-2 | 30.951 | 62 | 32 | 1 | within |
| notice-burst-2 | 31.232 | 62 | 32 | 1 | within |
| notice-burst-2 | 32.341 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.256 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.542 | 62 | 32 | 1 | within |
| notice-burst-3 | 8.216 | 62 | 32 | 1 | within |
| notice-burst-3 | 13.454 | 62 | 32 | 1 | within |
| notice-burst-3 | 17.191 | 62 | 32 | 1 | within |
| notice-burst-3 | 21.335 | 62 | 32 | 1 | within |
| notice-burst-3 | 21.613 | 62 | 32 | 1 | within |
| notice-burst-3 | 21.898 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.509 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.801 | 62 | 32 | 1 | within |
| notice-burst-3 | 22.158 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.164 | 62 | 32 | 1 | within |
| notice-burst-3 | 5.813 | 62 | 32 | 1 | within |
| notice-burst-3 | 6.103 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.437 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.720 | 62 | 32 | 1 | within |
| notice-burst-3 | 23.982 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.153 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.413 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.693 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.207 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.522 | 62 | 32 | 1 | within |
| notice-burst-3 | 2.805 | 62 | 32 | 1 | within |
| notice-burst-3 | 3.111 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.078 | 62 | 32 | 1 | within |
| notice-burst-3 | 4.383 | 62 | 32 | 1 | within |
| notice-burst-3 | 25.945 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.320 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.584 | 62 | 32 | 1 | within |
| notice-burst-3 | 27.866 | 62 | 32 | 1 | within |
| notice-burst-3 | 28.117 | 62 | 32 | 1 | within |
| notice-burst-3 | 29.244 | 62 | 32 | 1 | within |
| notice-burst-3 | 29.510 | 62 | 32 | 1 | within |
| notice-burst-3 | 29.793 | 62 | 32 | 1 | within |
| notice-burst-3 | 30.047 | 62 | 32 | 1 | within |
| notice-burst-3 | 31.169 | 62 | 32 | 1 | within |
| notice-burst-3 | 31.427 | 62 | 32 | 1 | within |
| notice-burst-3 | 31.668 | 62 | 32 | 1 | within |
| notice-burst-3 | 31.949 | 62 | 32 | 1 | within |
| notice-burst-3 | 33.155 | 62 | 32 | 1 | within |
| notice-burst-4 | 8.325 | 62 | 32 | 1 | within |
| notice-burst-4 | 13.566 | 62 | 32 | 1 | within |
| notice-burst-4 | 17.221 | 62 | 32 | 1 | within |
| notice-burst-4 | 21.382 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.510 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.798 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.271 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.562 | 62 | 32 | 1 | within |
| notice-burst-4 | 5.830 | 62 | 32 | 1 | within |
| notice-burst-4 | 6.115 | 62 | 32 | 1 | within |
| notice-burst-4 | 21.661 | 62 | 32 | 1 | within |
| notice-burst-4 | 21.943 | 62 | 32 | 1 | within |
| notice-burst-4 | 22.203 | 62 | 32 | 1 | within |
| notice-burst-4 | 23.213 | 62 | 32 | 1 | within |
| notice-burst-4 | 23.485 | 62 | 32 | 1 | within |
| notice-burst-4 | 23.768 | 62 | 32 | 1 | within |
| notice-burst-4 | 24.030 | 62 | 32 | 1 | within |
| notice-burst-4 | 25.204 | 62 | 32 | 1 | within |
| notice-burst-4 | 25.465 | 62 | 32 | 1 | within |
| notice-burst-4 | 25.745 | 62 | 32 | 1 | within |
| notice-burst-4 | 26.001 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.147 | 62 | 32 | 1 | within |
| notice-burst-4 | 2.201 | 62 | 32 | 1 | within |
| notice-burst-4 | 2.520 | 62 | 32 | 1 | within |
| notice-burst-4 | 2.808 | 62 | 32 | 1 | within |
| notice-burst-4 | 3.119 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.413 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.695 | 62 | 32 | 1 | within |
| notice-burst-4 | 27.948 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.316 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.081 | 62 | 32 | 1 | within |
| notice-burst-4 | 4.393 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.581 | 62 | 32 | 1 | within |
| notice-burst-4 | 29.865 | 62 | 32 | 1 | within |
| notice-burst-4 | 30.119 | 62 | 32 | 1 | within |
| notice-burst-4 | 31.241 | 62 | 32 | 1 | within |
| notice-burst-4 | 31.499 | 62 | 32 | 1 | within |
| notice-burst-4 | 31.740 | 62 | 32 | 1 | within |
| notice-burst-4 | 32.021 | 62 | 32 | 1 | within |
| notice-burst-4 | 33.228 | 62 | 32 | 1 | within |
| notice-burst-5 | 8.303 | 62 | 32 | 1 | within |
| notice-burst-5 | 13.541 | 62 | 32 | 1 | within |
| notice-burst-5 | 17.185 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.370 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.507 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.796 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.269 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.560 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.828 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.113 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.648 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.931 | 62 | 32 | 1 | within |
| notice-burst-5 | 22.191 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.200 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.473 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.756 | 62 | 32 | 1 | within |
| notice-burst-5 | 24.018 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.193 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.453 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.733 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.211 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.527 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.809 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.115 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.990 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.136 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.400 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.681 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.935 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.301 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.078 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.390 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.566 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.850 | 62 | 32 | 1 | within |
| notice-burst-5 | 30.104 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.227 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.485 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.726 | 62 | 32 | 1 | within |
| notice-burst-5 | 32.006 | 62 | 32 | 1 | within |
| notice-burst-5 | 33.212 | 62 | 32 | 1 | within |
| notice-burst-6 | 11.125 | 62 | 32 | 0 | within |
| notice-burst-6 | 14.730 | 62 | 32 | 0 | within |
| notice-burst-6 | 1.580 | 62 | 32 | 0 | within |
| notice-burst-6 | 1.873 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.865 | 62 | 32 | 0 | within |
| notice-burst-6 | 3.154 | 62 | 32 | 0 | within |
| notice-burst-6 | 4.615 | 62 | 32 | 0 | within |
| notice-burst-6 | 4.904 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.170 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.453 | 62 | 32 | 0 | within |
| notice-burst-6 | 7.429 | 62 | 32 | 0 | within |
| notice-burst-6 | 19.983 | 62 | 32 | 0 | within |
| notice-burst-6 | 20.261 | 62 | 32 | 0 | within |
| notice-burst-6 | 20.544 | 62 | 32 | 0 | within |
| notice-burst-6 | 20.804 | 62 | 32 | 0 | within |
| notice-burst-6 | 22.003 | 62 | 32 | 0 | within |
| notice-burst-6 | 22.278 | 62 | 32 | 0 | within |
| notice-burst-6 | 22.561 | 62 | 32 | 0 | within |
| notice-burst-6 | 22.813 | 62 | 32 | 0 | within |
| notice-burst-6 | 23.815 | 62 | 32 | 0 | within |
| notice-burst-6 | 24.082 | 62 | 32 | 0 | within |
| notice-burst-6 | 24.367 | 62 | 32 | 0 | within |
| notice-burst-6 | 3.430 | 62 | 32 | 0 | within |
| notice-burst-6 | 3.736 | 62 | 32 | 0 | within |
| notice-burst-6 | 24.627 | 62 | 32 | 0 | within |
| notice-burst-6 | 25.790 | 62 | 32 | 0 | within |
| notice-burst-6 | 26.055 | 62 | 32 | 0 | within |
| notice-burst-6 | 26.336 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.166 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.481 | 62 | 32 | 0 | within |
| notice-burst-6 | 26.588 | 62 | 32 | 0 | within |
| notice-burst-6 | 27.717 | 62 | 32 | 0 | within |
| notice-burst-6 | 27.983 | 62 | 32 | 0 | within |
| notice-burst-6 | 28.266 | 62 | 32 | 0 | within |
| notice-burst-6 | 28.521 | 62 | 32 | 0 | within |
| notice-burst-6 | 29.644 | 62 | 32 | 0 | within |
| notice-burst-6 | 29.902 | 62 | 32 | 0 | within |
| notice-burst-6 | 30.143 | 62 | 32 | 0 | within |
| notice-burst-6 | 30.424 | 62 | 32 | 0 | within |
| notice-burst-6 | 31.759 | 62 | 32 | 0 | within |
| notice-burst-7 | 3.501 | 62 | 32 | 1 | within |
| notice-burst-7 | 3.783 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.240 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.527 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.790 | 62 | 32 | 1 | within |
| notice-burst-7 | 6.074 | 62 | 32 | 1 | within |
| notice-burst-7 | 8.253 | 62 | 32 | 1 | within |
| notice-burst-7 | 13.490 | 62 | 32 | 1 | within |
| notice-burst-7 | 17.138 | 62 | 32 | 1 | within |
| notice-burst-7 | 21.323 | 62 | 32 | 1 | within |
| notice-burst-7 | 21.601 | 62 | 32 | 1 | within |
| notice-burst-7 | 21.883 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.144 | 62 | 32 | 1 | within |
| notice-burst-7 | 23.153 | 62 | 32 | 1 | within |
| notice-burst-7 | 23.425 | 62 | 32 | 1 | within |
| notice-burst-7 | 23.708 | 62 | 32 | 1 | within |
| notice-burst-7 | 23.970 | 62 | 32 | 1 | within |
| notice-burst-7 | 25.145 | 62 | 32 | 1 | within |
| notice-burst-7 | 25.405 | 62 | 32 | 1 | within |
| notice-burst-7 | 25.685 | 62 | 32 | 1 | within |
| notice-burst-7 | 25.941 | 62 | 32 | 1 | within |
| notice-burst-7 | 27.088 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.200 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.519 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.807 | 62 | 32 | 1 | within |
| notice-burst-7 | 3.118 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.058 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.363 | 62 | 32 | 1 | within |
| notice-burst-7 | 27.358 | 62 | 32 | 1 | within |
| notice-burst-7 | 27.640 | 62 | 32 | 1 | within |
| notice-burst-7 | 27.891 | 62 | 32 | 1 | within |
| notice-burst-7 | 29.258 | 62 | 32 | 1 | within |
| notice-burst-7 | 29.524 | 62 | 32 | 1 | within |
| notice-burst-7 | 29.808 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.061 | 62 | 32 | 1 | within |
| notice-burst-7 | 31.184 | 62 | 32 | 1 | within |
| notice-burst-7 | 31.442 | 62 | 32 | 1 | within |
| notice-burst-7 | 31.683 | 62 | 32 | 1 | within |
| notice-burst-7 | 31.964 | 62 | 32 | 1 | within |
| notice-burst-7 | 33.169 | 62 | 32 | 1 | within |

Latest: 33.228 ms, notice-burst-4.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 302 | 67,784 (0.678) | 29,806 (0.298) |
| notice-every-1 | 302 | 67,190 (0.672) | 29,806 (0.298) |
| notice-every-2 | 302 | 78,165 (0.782) | 29,806 (0.298) |
| notice-every-3 | 302 | 52,403 (0.524) | 29,806 (0.298) |
| notice-every-4 | 302 | 52,403 (0.524) | 29,806 (0.298) |
| notice-every-5 | 302 | 52,403 (0.524) | 29,806 (0.298) |
| notice-every-6 | 302 | 52,403 (0.524) | 29,806 (0.298) |
| notice-every-7 | 302 | 52,403 (0.524) | 29,806 (0.298) |
| notice-burst-0 | 311 | 67,784 (0.678) | 29,806 (0.298) |
| notice-burst-1 | 311 | 67,341 (0.673) | 29,806 (0.298) |
| notice-burst-2 | 311 | 78,165 (0.782) | 29,806 (0.298) |
| notice-burst-3 | 311 | 67,114 (0.671) | 29,806 (0.298) |
| notice-burst-4 | 311 | 67,476 (0.675) | 29,806 (0.298) |
| notice-burst-5 | 311 | 67,049 (0.670) | 29,806 (0.298) |
| notice-burst-6 | 311 | 66,895 (0.669) | 29,806 (0.298) |
| notice-burst-7 | 311 | 67,310 (0.673) | 29,806 (0.298) |

Longest pass that carries a step: 78,165 CPU cycles (0.782 ms), notice-every-2; longest step: 29,806 (0.298 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 446,232 | 4.462 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 475,172 | 4.752 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 624,595 | 6.246 | 62 | 66 | fits | 120,524 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 653,288 | 6.533 | 62 | 66 | fits | 120,524 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 232,183 | 2.322 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 261,892 | 2.619 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 825,459 | 8.255 | 62 | 66 | fits | 119,028 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 854,217 | 8.542 | 62 | 66 | fits | 119,028 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 289,011 | 2.890 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 317,733 | 3.177 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 501,886 | 5.019 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 530,341 | 5.303 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 679,800 | 6.798 | 62 | 66 | fits | 120,524 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 708,129 | 7.081 | 62 | 66 | fits | 120,524 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 880,326 | 8.803 | 62 | 66 | fits | 119,028 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 908,319 | 9.083 | 62 | 66 | fits | 119,028 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,025,240 | 10.252 | 62 | 66 | fits | 117,825 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,053,801 | 10.538 | 62 | 66 | fits | 117,825 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 1,079,018 | 10.790 | 62 | 66 | fits | 117,825 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,106,951 | 11.070 | 62 | 66 | fits | 117,825 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,254,126 | 12.541 | 62 | 66 | fits | 119,616 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,283,384 | 12.834 | 62 | 66 | fits | 119,616 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,309,299 | 13.093 | 62 | 66 | fits | 119,616 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,337,613 | 13.376 | 62 | 66 | fits | 119,616 | 400 | 0.079 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,427,108 | 14.271 | 62 | 66 | fits | 117,638 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,456,091 | 14.561 | 62 | 66 | fits | 117,638 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,481,611 | 14.816 | 62 | 66 | fits | 117,638 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,509,544 | 15.095 | 62 | 66 | fits | 117,638 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,644,640 | 16.446 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,673,220 | 16.732 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,698,517 | 16.985 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,726,633 | 17.266 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,837,223 | 18.372 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,866,060 | 18.661 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,891,501 | 18.915 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,919,840 | 19.198 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,027,527 | 20.275 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,051,952 | 20.520 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,080,625 | 20.806 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,109,280 | 21.093 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 1,051,063 | 10.511 | 20 | 200 | fits | 166,098 | 109 | 0.563 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 1,389,360 | 13.894 | 20 | 20 | fits | 157,137 | 92 | 0.547 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 1,454,841 | 14.548 | 20 | 24 | fits | 64,610 | 51 | 0.597 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 1,192,748 | 11.927 | 20 | 50 | fits | 174,457 | 101 | 0.610 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 622,680 | 6.227 | 20 | 20 | fits | 162,025 | 67 | 0.534 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 208,918 | 2.089 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 318,224 | 3.182 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 446,173 | 4.462 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 475,113 | 4.751 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 655,875 | 6.559 | 62 | 66 | fits | 120,319 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 684,568 | 6.846 | 62 | 66 | fits | 120,319 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 232,152 | 2.322 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 261,861 | 2.619 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 830,606 | 8.306 | 62 | 66 | fits | 118,904 | 402 | 0.065 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 859,364 | 8.594 | 62 | 66 | fits | 118,904 | 402 | 0.065 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 288,980 | 2.890 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 317,702 | 3.177 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 501,827 | 5.018 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 530,282 | 5.303 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 711,080 | 7.111 | 62 | 66 | fits | 120,319 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 739,409 | 7.394 | 62 | 66 | fits | 120,319 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 885,473 | 8.855 | 62 | 66 | fits | 118,904 | 402 | 0.065 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 913,466 | 9.135 | 62 | 66 | fits | 118,904 | 402 | 0.065 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 1,030,466 | 10.305 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 1,059,027 | 10.590 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 1,084,205 | 10.842 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 1,112,138 | 11.121 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 1,225,839 | 12.258 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 1,254,953 | 12.550 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 1,280,789 | 12.808 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 1,309,103 | 13.091 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 1,432,114 | 14.321 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 1,461,241 | 14.612 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 1,486,761 | 14.868 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 1,514,694 | 15.147 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 1,626,307 | 16.263 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 1,654,887 | 16.549 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 1,680,184 | 16.802 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 1,708,300 | 17.083 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 1,842,202 | 18.422 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 1,871,039 | 18.710 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 1,896,480 | 18.965 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 1,924,819 | 19.248 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 2,032,398 | 20.324 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 2,056,823 | 20.568 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 2,085,496 | 20.855 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 2,114,151 | 21.142 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if1` | 1,068,748 | 10.687 | 20 | 200 | fits | 178,223 | 133 | 0.544 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 1,401,938 | 14.019 | 20 | 20 | fits | 160,688 | 100 | 0.559 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if1` | 1,427,208 | 14.272 | 20 | 24 | fits | 45,474 | 27 | 0.696 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 1,181,068 | 11.811 | 20 | 50 | fits | 172,063 | 91 | 0.613 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if1` | 618,871 | 6.189 | 20 | 20 | fits | 159,424 | 60 | 0.499 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 206,330 | 2.063 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if1` | 315,699 | 3.157 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 421,145 | 4.211 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 450,085 | 4.501 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 624,414 | 6.244 | 62 | 66 | fits | 120,278 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 653,107 | 6.531 | 62 | 66 | fits | 120,278 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 207,124 | 2.071 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 236,833 | 2.368 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 825,202 | 8.252 | 62 | 66 | fits | 118,809 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 853,960 | 8.540 | 62 | 66 | fits | 118,809 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 263,952 | 2.640 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 292,674 | 2.927 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 476,799 | 4.768 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 505,254 | 5.053 | 62 | 66 | fits | 121,862 | 400 | 0.083 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 679,619 | 6.796 | 62 | 66 | fits | 120,278 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 707,948 | 7.079 | 62 | 66 | fits | 120,278 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 880,069 | 8.801 | 62 | 66 | fits | 118,809 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 908,062 | 9.081 | 62 | 66 | fits | 118,809 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 1,024,691 | 10.247 | 62 | 66 | fits | 117,802 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 1,053,252 | 10.533 | 62 | 66 | fits | 117,802 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 1,078,469 | 10.785 | 62 | 66 | fits | 117,802 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 1,106,402 | 11.064 | 62 | 66 | fits | 117,802 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 1,220,131 | 12.201 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 1,249,245 | 12.492 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 1,275,081 | 12.751 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 1,303,395 | 13.034 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 1,426,373 | 14.264 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 1,455,500 | 14.555 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 1,481,020 | 14.810 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 1,508,953 | 15.090 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 1,620,594 | 16.206 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 1,649,174 | 16.492 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 1,674,471 | 16.745 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 1,702,587 | 17.026 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 1,813,164 | 18.132 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 1,842,001 | 18.420 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 1,867,442 | 18.674 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 1,895,781 | 18.958 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 2,003,463 | 20.035 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 2,027,888 | 20.279 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 2,056,561 | 20.566 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 2,085,216 | 20.852 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if1` | 873,387 | 8.734 | 20 | 200 | fits | 186,213 | 107 | 0.618 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 1,370,829 | 13.708 | 20 | 20 | fits | 159,628 | 89 | 0.567 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if1` | 1,433,118 | 14.331 | 20 | 24 | fits | 82,493 | 59 | 0.559 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 1,171,726 | 11.717 | 20 | 50 | fits | 166,556 | 110 | 0.596 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if1` | 791,619 | 7.916 | 20 | 20 | fits | 186,213 | 107 | 0.618 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 207,428 | 2.074 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if1` | 316,646 | 3.166 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 453,015 | 4.530 | 62 | 66 | fits | 121,917 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 481,955 | 4.820 | 62 | 66 | fits | 121,917 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 630,126 | 6.301 | 62 | 66 | fits | 120,457 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 658,819 | 6.588 | 62 | 66 | fits | 120,457 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 232,226 | 2.322 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 261,935 | 2.619 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 831,083 | 8.311 | 62 | 66 | fits | 119,028 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 859,841 | 8.598 | 62 | 66 | fits | 119,028 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 289,054 | 2.891 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 317,776 | 3.178 | 62 | 66 | fits | 124,622 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 508,669 | 5.087 | 62 | 66 | fits | 121,917 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 537,124 | 5.371 | 62 | 66 | fits | 121,917 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 685,331 | 6.853 | 62 | 66 | fits | 120,457 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 713,660 | 7.137 | 62 | 66 | fits | 120,457 | 402 | 0.070 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 885,950 | 8.860 | 62 | 66 | fits | 119,028 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 913,943 | 9.139 | 62 | 66 | fits | 119,028 | 402 | 0.067 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 1,030,897 | 10.309 | 62 | 66 | fits | 117,825 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 1,059,458 | 10.595 | 62 | 66 | fits | 117,825 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 1,084,675 | 10.847 | 62 | 66 | fits | 117,825 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 1,112,608 | 11.126 | 62 | 66 | fits | 117,825 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 1,226,309 | 12.263 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 1,255,423 | 12.554 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 1,281,259 | 12.813 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 1,309,573 | 13.096 | 62 | 66 | fits | 119,058 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 1,432,551 | 14.326 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 1,461,678 | 14.617 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 1,487,198 | 14.872 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 1,515,131 | 15.151 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 1,626,777 | 16.268 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 1,655,357 | 16.554 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 1,680,654 | 16.807 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 1,708,770 | 17.088 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 1,842,639 | 18.426 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 1,871,476 | 18.715 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 1,896,917 | 18.969 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 1,925,256 | 19.253 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 2,032,802 | 20.328 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 2,057,227 | 20.572 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 2,085,900 | 20.859 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 2,114,555 | 21.146 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if1` | 1,225,967 | 12.260 | 20 | 200 | fits | 159,059 | 92 | 0.592 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 1,394,561 | 13.946 | 20 | 20 | fits | 161,862 | 71 | 0.648 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if1` | 1,475,093 | 14.751 | 20 | 24 | fits | 100,736 | 68 | 0.551 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 1,166,224 | 11.662 | 20 | 50 | fits | 159,059 | 92 | 0.592 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if1` | 826,856 | 8.269 | 20 | 20 | fits | 159,580 | 107 | 0.625 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 209,801 | 2.098 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if1` | 319,062 | 3.191 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 231,610 | 2.316 | 62 | 66 | fits | 123,579 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 260,630 | 2.606 | 62 | 66 | fits | 123,579 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 418,311 | 4.183 | 62 | 66 | fits | 121,498 | 403 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 447,262 | 4.473 | 62 | 66 | fits | 121,498 | 403 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 622,622 | 6.226 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 651,533 | 6.515 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 823,684 | 8.237 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 852,442 | 8.524 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 287,804 | 2.878 | 62 | 66 | fits | 123,579 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 316,516 | 3.165 | 62 | 66 | fits | 123,579 | 402 | 0.089 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 473,911 | 4.739 | 62 | 66 | fits | 121,498 | 403 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 502,366 | 5.024 | 62 | 66 | fits | 121,498 | 403 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 677,961 | 6.780 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 706,300 | 7.063 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 878,551 | 8.786 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 906,544 | 9.065 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 1,023,465 | 10.235 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 1,052,026 | 10.520 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 1,077,204 | 10.772 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 1,105,137 | 11.051 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 1,218,871 | 12.189 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 1,247,933 | 12.479 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 1,273,769 | 12.738 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 1,302,083 | 13.021 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 1,424,982 | 14.250 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 1,454,109 | 14.541 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 1,479,629 | 14.796 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 1,507,562 | 15.076 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 1,619,208 | 16.192 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 1,647,788 | 16.478 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 1,673,085 | 16.731 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 1,701,201 | 17.012 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 1,835,070 | 18.351 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 1,863,907 | 18.639 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 1,889,348 | 18.893 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 1,917,687 | 19.177 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 2,025,233 | 20.252 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 2,049,658 | 20.497 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 2,078,331 | 20.783 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 2,106,986 | 21.070 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if1` | 1,119,446 | 11.194 | 20 | 200 | fits | 180,886 | 138 | 0.557 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 1,434,860 | 14.349 | 20 | 20 | fits | 164,279 | 98 | 0.551 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if1` | 1,487,002 | 14.870 | 20 | 24 | fits | 46,298 | 32 | 0.709 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 1,231,106 | 12.311 | 20 | 50 | fits | 171,403 | 89 | 0.608 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if1` | 835,164 | 8.352 | 20 | 20 | fits | 178,644 | 112 | 0.603 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 214,975 | 2.150 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if1` | 324,186 | 3.242 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 231,743 | 2.317 | 62 | 66 | fits | 123,301 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 260,763 | 2.608 | 62 | 66 | fits | 123,301 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 418,179 | 4.182 | 62 | 66 | fits | 121,484 | 403 | 0.071 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 447,130 | 4.471 | 62 | 66 | fits | 121,484 | 403 | 0.071 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 622,511 | 6.225 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 651,422 | 6.514 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 823,573 | 8.236 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 852,331 | 8.523 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 287,937 | 2.879 | 62 | 66 | fits | 123,301 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 316,649 | 3.166 | 62 | 66 | fits | 123,301 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 473,779 | 4.738 | 62 | 66 | fits | 121,484 | 403 | 0.071 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 502,234 | 5.022 | 62 | 66 | fits | 121,484 | 403 | 0.071 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 677,850 | 6.779 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 706,189 | 7.062 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 878,440 | 8.784 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 906,433 | 9.064 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 1,023,387 | 10.234 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 1,051,948 | 10.519 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 1,077,126 | 10.771 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 1,105,059 | 11.051 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 1,218,760 | 12.188 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 1,247,822 | 12.478 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 1,273,658 | 12.737 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 1,301,972 | 13.020 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 1,424,904 | 14.249 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 1,454,031 | 14.540 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 1,479,551 | 14.796 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 1,507,484 | 15.075 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 1,619,097 | 16.191 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 1,647,677 | 16.477 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 1,672,974 | 16.730 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 1,701,090 | 17.011 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 1,811,672 | 18.117 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 1,840,509 | 18.405 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 1,865,950 | 18.660 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 1,894,289 | 18.943 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 2,024,969 | 20.250 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 2,049,394 | 20.494 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 2,078,067 | 20.781 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 2,106,722 | 21.067 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if1` | 1,085,932 | 10.859 | 20 | 200 | fits | 169,974 | 111 | 0.563 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 1,416,783 | 14.168 | 20 | 20 | fits | 158,512 | 92 | 0.560 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if1` | 1,459,591 | 14.596 | 20 | 24 | fits | 63,012 | 40 | 0.613 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 1,197,715 | 11.977 | 20 | 50 | fits | 171,526 | 88 | 0.611 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if1` | 834,190 | 8.342 | 20 | 20 | fits | 162,242 | 113 | 0.625 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 211,430 | 2.114 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if1` | 320,648 | 3.206 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 624,708 | 6.247 | 62 | 66 | fits | 120,208 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 653,269 | 6.533 | 62 | 66 | fits | 120,208 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 207,105 | 2.071 | 62 | 66 | fits | 124,293 | 402 | 0.087 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 236,382 | 2.364 | 62 | 66 | fits | 124,293 | 402 | 0.087 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 421,117 | 4.211 | 62 | 66 | fits | 122,546 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 450,515 | 4.505 | 62 | 66 | fits | 122,546 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 831,880 | 8.319 | 62 | 66 | fits | 118,865 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 860,638 | 8.606 | 62 | 66 | fits | 118,865 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 263,585 | 2.636 | 62 | 66 | fits | 124,293 | 402 | 0.087 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 292,297 | 2.923 | 62 | 66 | fits | 124,293 | 402 | 0.087 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 477,203 | 4.772 | 62 | 66 | fits | 122,546 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 505,657 | 5.057 | 62 | 66 | fits | 122,546 | 400 | 0.084 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 679,785 | 6.798 | 62 | 66 | fits | 120,208 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 708,114 | 7.081 | 62 | 66 | fits | 120,208 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 886,747 | 8.867 | 62 | 66 | fits | 118,865 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 914,740 | 9.147 | 62 | 66 | fits | 118,865 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 1,005,857 | 10.059 | 62 | 66 | fits | 117,701 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 1,034,418 | 10.344 | 62 | 66 | fits | 117,701 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 1,059,642 | 10.596 | 62 | 66 | fits | 117,701 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,087,575 | 10.876 | 62 | 66 | fits | 117,701 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,234,714 | 12.347 | 62 | 66 | fits | 119,530 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,263,920 | 12.639 | 62 | 66 | fits | 119,530 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,289,842 | 12.898 | 62 | 66 | fits | 119,530 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,318,156 | 13.182 | 62 | 66 | fits | 119,530 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,407,605 | 14.076 | 62 | 66 | fits | 117,604 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,436,588 | 14.366 | 62 | 66 | fits | 117,604 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,462,115 | 14.621 | 62 | 66 | fits | 117,604 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,490,048 | 14.900 | 62 | 66 | fits | 117,604 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,601,517 | 16.015 | 62 | 66 | fits | 116,704 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,630,097 | 16.301 | 62 | 66 | fits | 116,704 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,655,401 | 16.554 | 62 | 66 | fits | 116,704 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,683,517 | 16.835 | 62 | 66 | fits | 116,704 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,817,184 | 18.172 | 62 | 66 | fits | 117,149 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,846,021 | 18.460 | 62 | 66 | fits | 117,149 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,871,475 | 18.715 | 62 | 66 | fits | 117,149 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,899,814 | 18.998 | 62 | 66 | fits | 117,149 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,007,533 | 20.075 | 62 | 66 | fits | 114,181 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,031,958 | 20.320 | 62 | 66 | fits | 114,181 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,060,631 | 20.606 | 62 | 66 | fits | 114,181 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,089,286 | 20.893 | 62 | 66 | fits | 114,181 | 398 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if1` | 1,251,235 | 12.512 | 20 | 200 | fits | 158,064 | 86 | 0.601 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 1,397,216 | 13.972 | 20 | 20 | fits | 166,249 | 85 | 0.584 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if1` | 1,468,006 | 14.680 | 20 | 24 | fits | 64,926 | 51 | 0.606 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 1,191,492 | 11.915 | 20 | 50 | fits | 158,064 | 86 | 0.601 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if1` | 658,345 | 6.583 | 20 | 20 | fits | 165,157 | 73 | 0.543 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 216,838 | 2.168 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if1` | 326,207 | 3.262 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 231,741 | 2.317 | 62 | 66 | fits | 123,301 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 260,761 | 2.608 | 62 | 66 | fits | 123,301 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 418,187 | 4.182 | 62 | 66 | fits | 121,484 | 403 | 0.071 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 447,138 | 4.471 | 62 | 66 | fits | 121,484 | 403 | 0.071 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 622,488 | 6.225 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 651,399 | 6.514 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 823,583 | 8.236 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 852,341 | 8.523 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 287,935 | 2.879 | 62 | 66 | fits | 123,301 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 316,647 | 3.166 | 62 | 66 | fits | 123,301 | 400 | 0.087 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 473,787 | 4.738 | 62 | 66 | fits | 121,484 | 403 | 0.071 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 502,242 | 5.022 | 62 | 66 | fits | 121,484 | 403 | 0.071 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 677,827 | 6.778 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 706,166 | 7.062 | 62 | 66 | fits | 120,659 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 878,450 | 8.784 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 906,443 | 9.064 | 62 | 66 | fits | 119,099 | 402 | 0.068 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 1,023,382 | 10.234 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 1,051,943 | 10.519 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 1,077,121 | 10.771 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 1,105,054 | 11.051 | 62 | 66 | fits | 117,786 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 1,218,783 | 12.188 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 1,247,845 | 12.478 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 1,273,681 | 12.737 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 1,301,995 | 13.020 | 62 | 66 | fits | 119,006 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 1,424,894 | 14.249 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 1,454,021 | 14.540 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 1,479,541 | 14.795 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 1,507,474 | 15.075 | 62 | 66 | fits | 118,077 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 1,619,082 | 16.191 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 1,647,662 | 16.477 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 1,672,959 | 16.730 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 1,701,075 | 17.011 | 62 | 66 | fits | 116,738 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 1,834,972 | 18.350 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 1,863,809 | 18.638 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 1,889,250 | 18.892 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 1,917,589 | 19.176 | 62 | 66 | fits | 117,177 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 2,025,140 | 20.251 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 2,049,565 | 20.496 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 2,078,238 | 20.782 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 2,106,893 | 21.069 | 62 | 66 | fits | 114,144 | 398 | 0.064 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if1` | 1,081,076 | 10.811 | 20 | 200 | fits | 169,873 | 111 | 0.563 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 1,412,244 | 14.122 | 20 | 20 | fits | 158,978 | 93 | 0.559 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if1` | 1,454,841 | 14.548 | 20 | 24 | fits | 62,801 | 40 | 0.610 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 1,192,710 | 11.927 | 20 | 50 | fits | 171,377 | 89 | 0.609 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if1` | 829,435 | 8.294 | 20 | 20 | fits | 162,028 | 113 | 0.617 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 216,997 | 2.170 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if1` | 326,258 | 3.263 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 351,070 | 3.511 | 62 | 66 | fits | 124,526 | 402 | 0.033 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 379,287 | 3.793 | 62 | 66 | fits | 124,526 | 402 | 0.033 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 526,296 | 5.263 | 62 | 66 | fits | 120,457 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 555,013 | 5.550 | 62 | 66 | fits | 120,457 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 581,303 | 5.813 | 62 | 66 | fits | 120,457 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 609,672 | 6.097 | 62 | 66 | fits | 120,457 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 829,656 | 8.297 | 62 | 66 | fits | 37,752 | 101 | 0.291 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 1,353,327 | 13.533 | 62 | 66 | fits | 40,609 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 1,719,114 | 17.191 | 62 | 66 | fits | 38,162 | 100 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 2,135,267 | 21.353 | 62 | 66 | fits | 120,524 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 2,163,037 | 21.630 | 62 | 66 | fits | 120,524 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 2,191,282 | 21.913 | 62 | 66 | fits | 120,524 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 2,217,318 | 22.173 | 62 | 66 | fits | 120,524 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 2,318,247 | 23.182 | 62 | 66 | fits | 119,427 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 2,345,463 | 23.455 | 62 | 66 | fits | 119,427 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 2,373,787 | 23.738 | 62 | 66 | fits | 119,427 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 2,399,956 | 24.000 | 62 | 66 | fits | 119,427 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 2,517,425 | 25.174 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 2,543,458 | 25.435 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 2,571,461 | 25.715 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 2,597,067 | 25.971 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 2,711,723 | 27.117 | 62 | 66 | fits | 117,944 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 2,738,573 | 27.386 | 62 | 66 | fits | 117,944 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 2,767,110 | 27.671 | 62 | 66 | fits | 117,944 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 220,661 | 2.207 | 62 | 66 | fits | 158,431 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 253,020 | 2.530 | 62 | 66 | fits | 158,431 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 281,710 | 2.817 | 62 | 66 | fits | 158,431 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 312,809 | 3.128 | 62 | 66 | fits | 158,431 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 407,547 | 4.075 | 62 | 66 | fits | 124,526 | 402 | 0.033 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 438,415 | 4.384 | 62 | 66 | fits | 124,526 | 402 | 0.033 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,792,767 | 27.928 | 62 | 66 | fits | 117,944 | 400 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,905,810 | 29.058 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,932,411 | 29.324 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,960,749 | 29.607 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 2,986,133 | 29.861 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 3,121,660 | 31.217 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 3,147,484 | 31.475 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 3,171,571 | 31.716 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 3,199,658 | 31.997 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 3,320,220 | 33.202 | 62 | 66 | fits | 36,529 | 102 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 1,111,998 | 11.120 | 20 | 200 | fits | 167,680 | 111 | 0.565 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,463,458 | 14.635 | 20 | 20 | fits | 159,703 | 93 | 0.540 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 1,487,368 | 14.874 | 20 | 24 | fits | 44,114 | 26 | 0.714 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 1,264,280 | 12.643 | 20 | 50 | fits | 173,863 | 99 | 0.618 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 662,226 | 6.622 | 20 | 20 | fits | 158,932 | 60 | 0.495 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 348,866 | 3.489 | 62 | 66 | fits | 123,409 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 377,083 | 3.771 | 62 | 66 | fits | 123,409 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 828,941 | 8.289 | 62 | 66 | fits | 37,831 | 101 | 0.291 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,352,461 | 13.525 | 62 | 66 | fits | 40,609 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 1,717,416 | 17.174 | 62 | 66 | fits | 37,838 | 100 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 2,131,622 | 21.316 | 62 | 66 | fits | 120,832 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 2,159,407 | 21.594 | 62 | 66 | fits | 120,832 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 2,187,875 | 21.879 | 62 | 66 | fits | 120,832 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 523,492 | 5.235 | 62 | 66 | fits | 123,051 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 552,770 | 5.528 | 62 | 66 | fits | 123,051 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 579,619 | 5.796 | 62 | 66 | fits | 123,051 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 608,305 | 6.083 | 62 | 66 | fits | 123,051 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 2,214,139 | 22.141 | 62 | 66 | fits | 120,832 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 2,314,759 | 23.148 | 62 | 66 | fits | 119,348 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 2,341,975 | 23.420 | 62 | 66 | fits | 119,348 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 2,370,299 | 23.703 | 62 | 66 | fits | 119,348 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 2,396,468 | 23.965 | 62 | 66 | fits | 119,348 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 2,513,621 | 25.136 | 62 | 66 | fits | 116,141 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 2,539,654 | 25.397 | 62 | 66 | fits | 116,141 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 2,567,657 | 25.677 | 62 | 66 | fits | 116,141 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 219,696 | 2.197 | 62 | 66 | fits | 156,209 | 411 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 251,298 | 2.513 | 62 | 66 | fits | 156,209 | 411 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 279,512 | 2.795 | 62 | 66 | fits | 156,209 | 411 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 310,135 | 3.101 | 62 | 66 | fits | 156,209 | 411 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 404,866 | 4.049 | 62 | 66 | fits | 123,409 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 435,295 | 4.353 | 62 | 66 | fits | 123,409 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 2,592,789 | 25.928 | 62 | 66 | fits | 116,141 | 400 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 2,706,616 | 27.066 | 62 | 66 | fits | 116,473 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 2,733,063 | 27.331 | 62 | 66 | fits | 116,473 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 2,761,245 | 27.612 | 62 | 66 | fits | 116,473 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 2,786,423 | 27.864 | 62 | 66 | fits | 116,473 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 2,922,705 | 29.227 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,949,306 | 29.493 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 2,977,644 | 29.776 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 3,003,028 | 30.030 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 3,115,210 | 31.152 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 3,141,034 | 31.410 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 3,165,121 | 31.651 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 3,193,208 | 31.932 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 3,313,849 | 33.138 | 62 | 66 | fits | 36,529 | 102 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if1` | 1,109,028 | 11.090 | 20 | 200 | fits | 167,368 | 111 | 0.565 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 1,458,616 | 14.586 | 20 | 20 | fits | 158,733 | 93 | 0.540 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if1` | 1,482,356 | 14.824 | 20 | 24 | fits | 43,944 | 26 | 0.714 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 1,260,408 | 12.604 | 20 | 50 | fits | 173,285 | 99 | 0.618 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if1` | 659,835 | 6.598 | 20 | 20 | fits | 158,853 | 60 | 0.495 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 528,754 | 5.288 | 62 | 66 | fits | 120,294 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 557,287 | 5.573 | 62 | 66 | fits | 120,294 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 583,681 | 5.837 | 62 | 66 | fits | 120,294 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 611,832 | 6.118 | 62 | 66 | fits | 120,294 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 822,746 | 8.227 | 62 | 66 | fits | 37,958 | 103 | 0.289 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 1,187,540 | 11.875 | 62 | 66 | fits | 40,609 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 354,353 | 3.544 | 62 | 66 | fits | 124,903 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 383,460 | 3.835 | 62 | 66 | fits | 124,903 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 1,564,206 | 15.642 | 62 | 66 | fits | 38,399 | 101 | 0.279 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 1,953,121 | 19.531 | 62 | 66 | fits | 119,844 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 1,980,915 | 19.809 | 62 | 66 | fits | 119,844 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 2,009,090 | 20.091 | 62 | 66 | fits | 119,844 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 2,035,198 | 20.352 | 62 | 66 | fits | 119,844 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 2,235,444 | 22.354 | 62 | 66 | fits | 119,853 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 2,262,979 | 22.630 | 62 | 66 | fits | 119,853 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 2,291,303 | 22.913 | 62 | 66 | fits | 119,853 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 2,317,564 | 23.176 | 62 | 66 | fits | 119,853 | 400 | 0.092 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 2,443,880 | 24.439 | 62 | 66 | fits | 117,265 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 2,470,026 | 24.700 | 62 | 66 | fits | 117,265 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 2,498,058 | 24.981 | 62 | 66 | fits | 117,265 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 225,882 | 2.259 | 62 | 66 | fits | 155,009 | 411 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 257,484 | 2.575 | 62 | 66 | fits | 155,009 | 411 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 285,698 | 2.857 | 62 | 66 | fits | 155,009 | 411 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 316,321 | 3.163 | 62 | 66 | fits | 155,009 | 411 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 411,248 | 4.112 | 62 | 66 | fits | 124,903 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 441,677 | 4.417 | 62 | 66 | fits | 124,903 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 2,523,190 | 25.232 | 62 | 66 | fits | 117,265 | 400 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 2,637,017 | 26.370 | 62 | 66 | fits | 116,436 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 2,663,464 | 26.635 | 62 | 66 | fits | 116,436 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 2,691,646 | 26.916 | 62 | 66 | fits | 116,436 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 2,716,824 | 27.168 | 62 | 66 | fits | 116,436 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 2,829,473 | 28.295 | 62 | 66 | fits | 116,950 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 2,856,074 | 28.561 | 62 | 66 | fits | 116,950 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 2,884,412 | 28.844 | 62 | 66 | fits | 116,950 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 2,909,796 | 29.098 | 62 | 66 | fits | 116,950 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 3,045,155 | 30.452 | 62 | 66 | fits | 114,761 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 3,070,979 | 30.710 | 62 | 66 | fits | 114,761 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 3,095,066 | 30.951 | 62 | 66 | fits | 114,761 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 3,123,153 | 31.232 | 62 | 66 | fits | 114,761 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 3,234,130 | 32.341 | 62 | 66 | fits | 36,021 | 102 | 0.146 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if1` | 1,158,006 | 11.580 | 20 | 200 | fits | 181,222 | 142 | 0.555 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 1,589,268 | 15.893 | 20 | 20 | fits | 162,276 | 103 | 0.552 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if1` | 1,569,064 | 15.691 | 20 | 24 | fits | 162,276 | 103 | 0.552 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 1,267,673 | 12.677 | 20 | 50 | fits | 169,410 | 89 | 0.612 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if1` | 856,617 | 8.566 | 20 | 20 | fits | 175,967 | 112 | 0.601 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 525,625 | 5.256 | 62 | 66 | fits | 122,462 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 554,158 | 5.542 | 62 | 66 | fits | 122,462 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 821,642 | 8.216 | 62 | 66 | fits | 38,036 | 103 | 0.291 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,345,410 | 13.454 | 62 | 66 | fits | 40,609 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 1,719,095 | 17.191 | 62 | 66 | fits | 37,838 | 100 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 2,133,501 | 21.335 | 62 | 66 | fits | 120,569 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 2,161,286 | 21.613 | 62 | 66 | fits | 120,569 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 2,189,754 | 21.898 | 62 | 66 | fits | 120,569 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 350,914 | 3.509 | 62 | 66 | fits | 125,416 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 380,055 | 3.801 | 62 | 66 | fits | 125,416 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 2,215,840 | 22.158 | 62 | 66 | fits | 120,569 | 400 | 0.091 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 2,316,448 | 23.164 | 62 | 66 | fits | 119,295 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 581,311 | 5.813 | 62 | 66 | fits | 122,462 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 610,333 | 6.103 | 62 | 66 | fits | 122,462 | 400 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 2,343,681 | 23.437 | 62 | 66 | fits | 119,295 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 2,372,005 | 23.720 | 62 | 66 | fits | 119,295 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 2,398,174 | 23.982 | 62 | 66 | fits | 119,295 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 2,515,263 | 25.153 | 62 | 66 | fits | 116,170 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 2,541,325 | 25.413 | 62 | 66 | fits | 116,170 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 2,569,328 | 25.693 | 62 | 66 | fits | 116,170 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 220,668 | 2.207 | 62 | 66 | fits | 156,199 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 252,249 | 2.522 | 62 | 66 | fits | 156,199 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 280,463 | 2.805 | 62 | 66 | fits | 156,199 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 311,086 | 3.111 | 62 | 66 | fits | 156,199 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 407,838 | 4.078 | 62 | 66 | fits | 125,416 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 438,267 | 4.383 | 62 | 66 | fits | 125,416 | 402 | 0.034 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 2,594,460 | 25.945 | 62 | 66 | fits | 116,170 | 400 | 0.066 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 2,731,963 | 27.320 | 62 | 66 | fits | 116,447 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 2,758,410 | 27.584 | 62 | 66 | fits | 116,447 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 2,786,566 | 27.866 | 62 | 66 | fits | 116,447 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,811,744 | 28.117 | 62 | 66 | fits | 116,447 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,924,397 | 29.244 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,950,998 | 29.510 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 2,979,336 | 29.793 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 3,004,720 | 30.047 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 3,116,902 | 31.169 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 3,142,726 | 31.427 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 3,166,813 | 31.668 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 3,194,900 | 31.949 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 3,315,538 | 33.155 | 62 | 66 | fits | 36,529 | 102 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if1` | 1,106,455 | 11.065 | 20 | 200 | fits | 175,887 | 133 | 0.544 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 1,456,150 | 14.562 | 20 | 20 | fits | 158,807 | 94 | 0.538 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if1` | 1,479,983 | 14.800 | 20 | 24 | fits | 44,037 | 26 | 0.712 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 1,257,868 | 12.579 | 20 | 50 | fits | 173,318 | 99 | 0.619 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if1` | 648,532 | 6.485 | 20 | 20 | fits | 158,853 | 60 | 0.495 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 832,525 | 8.325 | 62 | 66 | fits | 38,018 | 101 | 0.291 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,356,566 | 13.566 | 62 | 66 | fits | 40,753 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,722,066 | 17.221 | 62 | 66 | fits | 37,931 | 100 | 0.298 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 2,138,209 | 21.382 | 62 | 66 | fits | 120,597 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 350,971 | 3.510 | 62 | 66 | fits | 125,682 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 379,844 | 3.798 | 62 | 66 | fits | 125,682 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 527,070 | 5.271 | 62 | 66 | fits | 122,418 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 556,183 | 5.562 | 62 | 66 | fits | 122,418 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 583,044 | 5.830 | 62 | 66 | fits | 122,418 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 611,525 | 6.115 | 62 | 66 | fits | 122,418 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 2,166,058 | 21.661 | 62 | 66 | fits | 120,597 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 2,194,303 | 21.943 | 62 | 66 | fits | 120,597 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 2,220,339 | 22.203 | 62 | 66 | fits | 120,597 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 2,321,256 | 23.213 | 62 | 66 | fits | 119,418 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 2,348,463 | 23.485 | 62 | 66 | fits | 119,418 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 2,376,787 | 23.768 | 62 | 66 | fits | 119,418 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 2,402,956 | 24.030 | 62 | 66 | fits | 119,418 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 2,520,425 | 25.204 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 2,546,458 | 25.465 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 2,574,461 | 25.745 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 2,600,067 | 26.001 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 2,714,723 | 27.147 | 62 | 66 | fits | 117,092 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 220,129 | 2.201 | 62 | 66 | fits | 157,717 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 252,012 | 2.520 | 62 | 66 | fits | 157,717 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 280,837 | 2.808 | 62 | 66 | fits | 157,717 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 311,886 | 3.119 | 62 | 66 | fits | 157,717 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 2,741,311 | 27.413 | 62 | 66 | fits | 117,092 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 2,769,467 | 27.695 | 62 | 66 | fits | 117,092 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 2,794,836 | 27.948 | 62 | 66 | fits | 117,092 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 2,931,554 | 29.316 | 62 | 66 | fits | 117,034 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 408,132 | 4.081 | 62 | 66 | fits | 125,682 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 439,319 | 4.393 | 62 | 66 | fits | 125,682 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 2,958,140 | 29.581 | 62 | 66 | fits | 117,034 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 2,986,478 | 29.865 | 62 | 66 | fits | 117,034 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 3,011,933 | 30.119 | 62 | 66 | fits | 117,034 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 3,124,115 | 31.241 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 3,149,939 | 31.499 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 3,174,026 | 31.740 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 3,202,113 | 32.021 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 3,322,754 | 33.228 | 62 | 66 | fits | 36,529 | 102 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if1` | 1,109,739 | 11.097 | 20 | 200 | fits | 167,680 | 111 | 0.565 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 1,460,976 | 14.610 | 20 | 20 | fits | 159,661 | 93 | 0.540 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if1` | 1,484,874 | 14.849 | 20 | 24 | fits | 44,102 | 26 | 0.714 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 1,261,840 | 12.618 | 20 | 50 | fits | 173,913 | 99 | 0.619 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if1` | 659,885 | 6.599 | 20 | 20 | fits | 158,932 | 60 | 0.495 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 830,253 | 8.303 | 62 | 66 | fits | 38,034 | 101 | 0.289 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,354,069 | 13.541 | 62 | 66 | fits | 40,753 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,718,468 | 17.185 | 62 | 66 | fits | 37,806 | 100 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 2,136,972 | 21.370 | 62 | 66 | fits | 120,594 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 350,687 | 3.507 | 62 | 66 | fits | 125,789 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 379,560 | 3.796 | 62 | 66 | fits | 125,789 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 526,851 | 5.269 | 62 | 66 | fits | 122,173 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 555,964 | 5.560 | 62 | 66 | fits | 122,173 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 582,825 | 5.828 | 62 | 66 | fits | 122,173 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 611,306 | 6.113 | 62 | 66 | fits | 122,173 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 2,164,821 | 21.648 | 62 | 66 | fits | 120,594 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 2,193,066 | 21.931 | 62 | 66 | fits | 120,594 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 2,219,093 | 22.191 | 62 | 66 | fits | 120,594 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 2,320,048 | 23.200 | 62 | 66 | fits | 119,461 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 2,347,299 | 23.473 | 62 | 66 | fits | 119,461 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 2,375,623 | 23.756 | 62 | 66 | fits | 119,461 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 2,401,792 | 24.018 | 62 | 66 | fits | 119,461 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 2,519,294 | 25.193 | 62 | 66 | fits | 116,996 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 2,545,327 | 25.453 | 62 | 66 | fits | 116,996 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,573,330 | 25.733 | 62 | 66 | fits | 116,996 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 221,077 | 2.211 | 62 | 66 | fits | 156,199 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 252,658 | 2.527 | 62 | 66 | fits | 156,199 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 280,872 | 2.809 | 62 | 66 | fits | 156,199 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 311,495 | 3.115 | 62 | 66 | fits | 156,199 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 2,599,015 | 25.990 | 62 | 66 | fits | 116,996 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 2,713,559 | 27.136 | 62 | 66 | fits | 116,934 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 2,739,989 | 27.400 | 62 | 66 | fits | 116,934 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 2,768,145 | 27.681 | 62 | 66 | fits | 116,934 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 2,793,514 | 27.935 | 62 | 66 | fits | 116,934 | 400 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 2,930,056 | 29.301 | 62 | 66 | fits | 117,034 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 407,848 | 4.078 | 62 | 66 | fits | 125,789 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 439,035 | 4.390 | 62 | 66 | fits | 125,789 | 402 | 0.031 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 2,956,642 | 29.566 | 62 | 66 | fits | 117,034 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 2,984,980 | 29.850 | 62 | 66 | fits | 117,034 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 3,010,435 | 30.104 | 62 | 66 | fits | 117,034 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 3,122,650 | 31.227 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 3,148,474 | 31.485 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 3,172,561 | 31.726 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 3,200,648 | 32.006 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 3,321,187 | 33.212 | 62 | 66 | fits | 36,529 | 102 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if1` | 1,319,574 | 13.196 | 20 | 200 | fits | 177,155 | 107 | 0.603 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 1,458,287 | 14.583 | 20 | 20 | fits | 158,981 | 95 | 0.534 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if1` | 1,481,984 | 14.820 | 20 | 24 | fits | 43,901 | 26 | 0.709 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 1,259,831 | 12.598 | 20 | 50 | fits | 177,155 | 107 | 0.603 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if1` | 655,735 | 6.557 | 20 | 20 | fits | 158,932 | 60 | 0.495 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 1,112,547 | 11.125 | 62 | 66 | fits | 39,399 | 101 | 0.306 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,472,996 | 14.730 | 62 | 66 | fits | 39,565 | 102 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 158,034 | 1.580 | 62 | 66 | fits | 154,471 | 411 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 187,276 | 1.873 | 62 | 66 | fits | 154,471 | 411 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 286,451 | 2.865 | 62 | 66 | fits | 124,232 | 402 | 0.030 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 315,390 | 3.154 | 62 | 66 | fits | 124,232 | 402 | 0.030 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 461,479 | 4.615 | 62 | 66 | fits | 120,991 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 490,413 | 4.904 | 62 | 66 | fits | 120,991 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 517,043 | 5.170 | 62 | 66 | fits | 120,991 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 545,293 | 5.453 | 62 | 66 | fits | 120,991 | 402 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 742,947 | 7.429 | 62 | 66 | fits | 38,161 | 100 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 1,998,317 | 19.983 | 62 | 66 | fits | 119,886 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 2,026,095 | 20.261 | 62 | 66 | fits | 119,886 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 2,054,375 | 20.544 | 62 | 66 | fits | 119,886 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 2,080,388 | 20.804 | 62 | 66 | fits | 119,886 | 400 | 0.090 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 2,200,258 | 22.003 | 62 | 66 | fits | 118,084 | 400 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 2,227,792 | 22.278 | 62 | 66 | fits | 118,084 | 400 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 2,256,113 | 22.561 | 62 | 66 | fits | 118,084 | 400 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 2,281,269 | 22.813 | 62 | 66 | fits | 118,084 | 400 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,381,513 | 23.815 | 62 | 66 | fits | 118,933 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,408,225 | 24.082 | 62 | 66 | fits | 118,933 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,436,664 | 24.367 | 62 | 66 | fits | 118,933 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 343,050 | 3.430 | 62 | 66 | fits | 124,232 | 402 | 0.030 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 373,600 | 3.736 | 62 | 66 | fits | 124,232 | 402 | 0.030 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 2,462,720 | 24.627 | 62 | 66 | fits | 118,933 | 401 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 2,578,986 | 25.790 | 62 | 66 | fits | 116,678 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 2,605,476 | 26.055 | 62 | 66 | fits | 116,678 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 2,633,632 | 26.336 | 62 | 66 | fits | 116,678 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 216,569 | 2.166 | 62 | 66 | fits | 154,471 | 411 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 248,137 | 2.481 | 62 | 66 | fits | 154,471 | 411 | 0.100 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 2,658,764 | 26.588 | 62 | 66 | fits | 116,678 | 400 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 2,771,668 | 27.717 | 62 | 66 | fits | 117,058 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 2,798,269 | 27.983 | 62 | 66 | fits | 117,058 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 2,826,607 | 28.266 | 62 | 66 | fits | 117,058 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 2,852,062 | 28.521 | 62 | 66 | fits | 117,058 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 2,964,380 | 29.644 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,990,204 | 29.902 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 3,014,291 | 30.143 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 3,042,378 | 30.424 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 3,175,931 | 31.759 | 62 | 66 | fits | 36,058 | 102 | 0.146 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if1` | 1,272,820 | 12.728 | 20 | 200 | fits | 165,936 | 108 | 0.571 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 1,415,866 | 14.159 | 20 | 20 | fits | 163,314 | 88 | 0.534 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if1` | 1,598,187 | 15.982 | 20 | 24 | fits | 82,639 | 61 | 0.596 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 1,213,077 | 12.131 | 20 | 50 | fits | 165,936 | 108 | 0.571 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if1` | 670,640 | 6.706 | 20 | 20 | fits | 163,657 | 67 | 0.554 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 350,106 | 3.501 | 62 | 66 | fits | 123,137 | 402 | 0.030 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 378,323 | 3.783 | 62 | 66 | fits | 123,137 | 402 | 0.030 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 524,006 | 5.240 | 62 | 66 | fits | 120,186 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 552,723 | 5.527 | 62 | 66 | fits | 120,186 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 579,013 | 5.790 | 62 | 66 | fits | 120,186 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 607,382 | 6.074 | 62 | 66 | fits | 120,186 | 400 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 825,330 | 8.253 | 62 | 66 | fits | 37,765 | 101 | 0.289 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 1,348,955 | 13.490 | 62 | 66 | fits | 40,615 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 1,713,759 | 17.138 | 62 | 66 | fits | 38,110 | 100 | 0.295 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 2,132,312 | 21.323 | 62 | 66 | fits | 120,524 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 2,160,082 | 21.601 | 62 | 66 | fits | 120,524 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 2,188,327 | 21.883 | 62 | 66 | fits | 120,524 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 2,214,363 | 22.144 | 62 | 66 | fits | 120,524 | 400 | 0.093 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 2,315,253 | 23.153 | 62 | 66 | fits | 119,461 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 2,342,504 | 23.425 | 62 | 66 | fits | 119,461 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 2,370,828 | 23.708 | 62 | 66 | fits | 119,461 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 2,396,997 | 23.970 | 62 | 66 | fits | 119,461 | 401 | 0.076 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 2,514,499 | 25.145 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 2,540,532 | 25.405 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 2,568,535 | 25.685 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 2,594,141 | 25.941 | 62 | 66 | fits | 116,917 | 400 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 2,708,764 | 27.088 | 62 | 66 | fits | 117,272 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 219,972 | 2.200 | 62 | 66 | fits | 157,592 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 251,876 | 2.519 | 62 | 66 | fits | 157,592 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 280,701 | 2.807 | 62 | 66 | fits | 157,592 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 311,750 | 3.118 | 62 | 66 | fits | 157,592 | 411 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 405,790 | 4.058 | 62 | 66 | fits | 123,137 | 402 | 0.030 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 436,269 | 4.363 | 62 | 66 | fits | 123,137 | 402 | 0.030 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 2,735,802 | 27.358 | 62 | 66 | fits | 117,272 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 2,763,958 | 27.640 | 62 | 66 | fits | 117,272 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 2,789,136 | 27.891 | 62 | 66 | fits | 117,272 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 2,925,817 | 29.258 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 2,952,418 | 29.524 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 2,980,756 | 29.808 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 3,006,140 | 30.061 | 62 | 66 | fits | 116,987 | 400 | 0.071 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 3,118,355 | 31.184 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 3,144,179 | 31.442 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 3,168,266 | 31.683 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 3,196,353 | 31.964 | 62 | 66 | fits | 114,798 | 399 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 3,316,892 | 33.169 | 62 | 66 | fits | 36,529 | 102 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if1` | 1,321,802 | 13.218 | 20 | 200 | fits | 177,144 | 107 | 0.602 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 1,460,557 | 14.606 | 20 | 20 | fits | 159,023 | 95 | 0.534 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if1` | 1,484,266 | 14.843 | 20 | 24 | fits | 43,913 | 26 | 0.709 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 1,262,059 | 12.621 | 20 | 50 | fits | 177,144 | 107 | 0.602 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if1` | 657,707 | 6.577 | 20 | 20 | fits | 158,938 | 60 | 0.495 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
