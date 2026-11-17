### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 364 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.acmp.if0` (notice-every-0) | 6.968 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.adp.if0` (notice-every-6) | 7.000 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.aecp.if0` (notice-every-0) | 5.144 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-2.held.maap.if0` (notice-every-2) | 5.981 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.srp.if0` (notice-every-6) | 9.892 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.123 | fits | 0 srp | 4 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.36.0.if0` (notice-burst-0) | 25.541 (25.848) | fits | 1 events | 320 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1359 | 0 | 171,233 (1.712) | fits |
| notice-every-2 | 1355 | 0 | 155,783 (1.558) | fits |
| notice-every-4 | 1347 | 0 | 161,088 (1.611) | fits |
| notice-every-6 | 1345 | 0 | 158,222 (1.582) | fits |
| notice-burst-0 | 1115 | 0 | 167,944 (1.679) | fits |
| notice-burst-2 | 1112 | 0 | 171,432 (1.714) | fits |
| notice-burst-4 | 1109 | 0 | 164,481 (1.645) | fits |
| notice-burst-6 | 1101 | 0 | 186,808 (1.868) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.303 | 130 | 16 | 2 | within |
| notice-every-0 | 4.481 | 130 | 16 | 2 | within |
| notice-every-0 | 6.308 | 130 | 16 | 2 | within |
| notice-every-0 | 6.484 | 130 | 16 | 2 | within |
| notice-every-0 | 8.286 | 130 | 16 | 2 | within |
| notice-every-0 | 8.461 | 130 | 16 | 2 | within |
| notice-every-0 | 2.199 | 130 | 16 | 2 | within |
| notice-every-0 | 2.387 | 130 | 16 | 2 | within |
| notice-every-0 | 2.557 | 130 | 16 | 2 | within |
| notice-every-0 | 2.732 | 130 | 16 | 2 | within |
| notice-every-0 | 4.648 | 130 | 16 | 2 | within |
| notice-every-0 | 4.820 | 130 | 16 | 2 | within |
| notice-every-0 | 6.653 | 130 | 16 | 2 | within |
| notice-every-0 | 6.822 | 130 | 16 | 2 | within |
| notice-every-0 | 8.631 | 130 | 16 | 2 | within |
| notice-every-0 | 8.802 | 130 | 16 | 2 | within |
| notice-every-0 | 10.242 | 130 | 16 | 2 | within |
| notice-every-0 | 10.420 | 130 | 16 | 2 | within |
| notice-every-0 | 10.574 | 130 | 16 | 2 | within |
| notice-every-0 | 10.745 | 130 | 16 | 2 | within |
| notice-every-0 | 12.390 | 130 | 16 | 2 | within |
| notice-every-0 | 12.573 | 130 | 16 | 2 | within |
| notice-every-0 | 12.736 | 130 | 16 | 2 | within |
| notice-every-0 | 12.913 | 130 | 16 | 2 | within |
| notice-every-0 | 14.305 | 130 | 16 | 2 | within |
| notice-every-0 | 14.484 | 130 | 16 | 2 | within |
| notice-every-0 | 14.643 | 130 | 16 | 2 | within |
| notice-every-0 | 14.812 | 130 | 16 | 2 | within |
| notice-every-0 | 16.182 | 130 | 16 | 2 | within |
| notice-every-0 | 16.357 | 130 | 16 | 2 | within |
| notice-every-0 | 16.515 | 130 | 16 | 2 | within |
| notice-every-0 | 16.688 | 130 | 16 | 2 | within |
| notice-every-0 | 18.242 | 130 | 16 | 2 | within |
| notice-every-0 | 18.418 | 130 | 16 | 2 | within |
| notice-every-0 | 18.572 | 130 | 16 | 2 | within |
| notice-every-0 | 18.743 | 130 | 16 | 2 | within |
| notice-every-0 | 20.262 | 130 | 16 | 2 | within |
| notice-every-0 | 20.404 | 130 | 16 | 2 | within |
| notice-every-0 | 20.574 | 130 | 16 | 2 | within |
| notice-every-0 | 20.747 | 130 | 16 | 2 | within |
| notice-every-2 | 8.124 | 130 | 16 | 2 | within |
| notice-every-2 | 8.298 | 130 | 16 | 2 | within |
| notice-every-2 | 2.258 | 130 | 16 | 2 | within |
| notice-every-2 | 2.439 | 130 | 16 | 2 | within |
| notice-every-2 | 4.131 | 130 | 16 | 2 | within |
| notice-every-2 | 4.310 | 130 | 16 | 2 | within |
| notice-every-2 | 6.140 | 130 | 16 | 2 | within |
| notice-every-2 | 6.320 | 130 | 16 | 2 | within |
| notice-every-2 | 2.610 | 130 | 16 | 2 | within |
| notice-every-2 | 2.785 | 130 | 16 | 2 | within |
| notice-every-2 | 4.477 | 130 | 16 | 2 | within |
| notice-every-2 | 4.649 | 130 | 16 | 2 | within |
| notice-every-2 | 6.487 | 130 | 16 | 2 | within |
| notice-every-2 | 6.657 | 130 | 16 | 2 | within |
| notice-every-2 | 8.467 | 130 | 16 | 2 | within |
| notice-every-2 | 8.638 | 130 | 16 | 2 | within |
| notice-every-2 | 10.081 | 130 | 16 | 2 | within |
| notice-every-2 | 10.259 | 130 | 16 | 2 | within |
| notice-every-2 | 10.414 | 130 | 16 | 2 | within |
| notice-every-2 | 10.585 | 130 | 16 | 2 | within |
| notice-every-2 | 12.193 | 130 | 16 | 2 | within |
| notice-every-2 | 12.375 | 130 | 16 | 2 | within |
| notice-every-2 | 12.538 | 130 | 16 | 2 | within |
| notice-every-2 | 12.714 | 130 | 16 | 2 | within |
| notice-every-2 | 14.142 | 130 | 16 | 2 | within |
| notice-every-2 | 14.322 | 130 | 16 | 2 | within |
| notice-every-2 | 14.482 | 130 | 16 | 2 | within |
| notice-every-2 | 14.651 | 130 | 16 | 2 | within |
| notice-every-2 | 16.227 | 130 | 16 | 2 | within |
| notice-every-2 | 16.402 | 130 | 16 | 2 | within |
| notice-every-2 | 16.560 | 130 | 16 | 2 | within |
| notice-every-2 | 16.733 | 130 | 16 | 2 | within |
| notice-every-2 | 18.082 | 130 | 16 | 2 | within |
| notice-every-2 | 18.258 | 130 | 16 | 2 | within |
| notice-every-2 | 18.412 | 130 | 16 | 2 | within |
| notice-every-2 | 18.582 | 130 | 16 | 2 | within |
| notice-every-2 | 20.102 | 130 | 16 | 2 | within |
| notice-every-2 | 20.245 | 130 | 16 | 2 | within |
| notice-every-2 | 20.415 | 130 | 16 | 2 | within |
| notice-every-2 | 20.587 | 130 | 16 | 2 | within |
| notice-every-4 | 8.176 | 130 | 16 | 2 | within |
| notice-every-4 | 8.350 | 130 | 16 | 2 | within |
| notice-every-4 | 4.420 | 130 | 16 | 2 | within |
| notice-every-4 | 4.601 | 130 | 16 | 2 | within |
| notice-every-4 | 6.197 | 130 | 16 | 2 | within |
| notice-every-4 | 6.373 | 130 | 16 | 2 | within |
| notice-every-4 | 2.263 | 130 | 16 | 2 | within |
| notice-every-4 | 2.451 | 130 | 16 | 2 | within |
| notice-every-4 | 2.620 | 130 | 16 | 2 | within |
| notice-every-4 | 2.795 | 130 | 16 | 2 | within |
| notice-every-4 | 4.768 | 130 | 16 | 2 | within |
| notice-every-4 | 4.940 | 130 | 16 | 2 | within |
| notice-every-4 | 6.540 | 130 | 16 | 2 | within |
| notice-every-4 | 6.710 | 130 | 16 | 2 | within |
| notice-every-4 | 8.519 | 130 | 16 | 2 | within |
| notice-every-4 | 8.690 | 130 | 16 | 2 | within |
| notice-every-4 | 10.348 | 130 | 16 | 2 | within |
| notice-every-4 | 10.526 | 130 | 16 | 2 | within |
| notice-every-4 | 10.680 | 130 | 16 | 2 | within |
| notice-every-4 | 10.851 | 130 | 16 | 2 | within |
| notice-every-4 | 12.248 | 130 | 16 | 2 | within |
| notice-every-4 | 12.430 | 130 | 16 | 2 | within |
| notice-every-4 | 12.593 | 130 | 16 | 2 | within |
| notice-every-4 | 12.770 | 130 | 16 | 2 | within |
| notice-every-4 | 14.198 | 130 | 16 | 2 | within |
| notice-every-4 | 14.378 | 130 | 16 | 2 | within |
| notice-every-4 | 14.537 | 130 | 16 | 2 | within |
| notice-every-4 | 14.706 | 130 | 16 | 2 | within |
| notice-every-4 | 16.283 | 130 | 16 | 2 | within |
| notice-every-4 | 16.457 | 130 | 16 | 2 | within |
| notice-every-4 | 16.616 | 130 | 16 | 2 | within |
| notice-every-4 | 16.788 | 130 | 16 | 2 | within |
| notice-every-4 | 18.343 | 130 | 16 | 2 | within |
| notice-every-4 | 18.518 | 130 | 16 | 2 | within |
| notice-every-4 | 18.673 | 130 | 16 | 2 | within |
| notice-every-4 | 18.843 | 130 | 16 | 2 | within |
| notice-every-4 | 20.161 | 130 | 16 | 2 | within |
| notice-every-4 | 20.303 | 130 | 16 | 2 | within |
| notice-every-4 | 20.473 | 130 | 16 | 2 | within |
| notice-every-4 | 20.645 | 130 | 16 | 2 | within |
| notice-every-6 | 2.194 | 130 | 16 | 2 | within |
| notice-every-6 | 2.371 | 130 | 16 | 2 | within |
| notice-every-6 | 4.059 | 130 | 16 | 2 | within |
| notice-every-6 | 4.237 | 130 | 16 | 2 | within |
| notice-every-6 | 6.061 | 130 | 16 | 2 | within |
| notice-every-6 | 6.235 | 130 | 16 | 2 | within |
| notice-every-6 | 8.299 | 130 | 16 | 2 | within |
| notice-every-6 | 8.477 | 130 | 16 | 2 | within |
| notice-every-6 | 2.542 | 130 | 16 | 2 | within |
| notice-every-6 | 2.717 | 130 | 16 | 2 | within |
| notice-every-6 | 4.405 | 130 | 16 | 2 | within |
| notice-every-6 | 4.577 | 130 | 16 | 2 | within |
| notice-every-6 | 6.402 | 130 | 16 | 2 | within |
| notice-every-6 | 6.572 | 130 | 16 | 2 | within |
| notice-every-6 | 8.645 | 130 | 16 | 2 | within |
| notice-every-6 | 8.817 | 130 | 16 | 2 | within |
| notice-every-6 | 10.245 | 130 | 16 | 2 | within |
| notice-every-6 | 10.423 | 130 | 16 | 2 | within |
| notice-every-6 | 10.578 | 130 | 16 | 2 | within |
| notice-every-6 | 10.749 | 130 | 16 | 2 | within |
| notice-every-6 | 12.146 | 130 | 16 | 2 | within |
| notice-every-6 | 12.328 | 130 | 16 | 2 | within |
| notice-every-6 | 12.491 | 130 | 16 | 2 | within |
| notice-every-6 | 12.667 | 130 | 16 | 2 | within |
| notice-every-6 | 14.096 | 130 | 16 | 2 | within |
| notice-every-6 | 14.276 | 130 | 16 | 2 | within |
| notice-every-6 | 14.435 | 130 | 16 | 2 | within |
| notice-every-6 | 14.604 | 130 | 16 | 2 | within |
| notice-every-6 | 16.181 | 130 | 16 | 2 | within |
| notice-every-6 | 16.355 | 130 | 16 | 2 | within |
| notice-every-6 | 16.514 | 130 | 16 | 2 | within |
| notice-every-6 | 16.686 | 130 | 16 | 2 | within |
| notice-every-6 | 18.241 | 130 | 16 | 2 | within |
| notice-every-6 | 18.416 | 130 | 16 | 2 | within |
| notice-every-6 | 18.570 | 130 | 16 | 2 | within |
| notice-every-6 | 18.741 | 130 | 16 | 2 | within |
| notice-every-6 | 20.059 | 130 | 16 | 2 | within |
| notice-every-6 | 20.201 | 130 | 16 | 2 | within |
| notice-every-6 | 20.371 | 130 | 16 | 2 | within |
| notice-every-6 | 20.543 | 130 | 16 | 2 | within |
| notice-burst-0 | 2.650 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.826 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.506 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.678 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.759 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.931 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.093 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.265 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.341 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.522 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.682 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.850 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.929 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.112 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.063 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.241 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.407 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.581 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.180 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.357 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.517 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.693 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.067 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.248 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.863 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.062 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.018 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.220 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.296 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.490 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.411 | 130 | 16 | 1 | within |
| notice-burst-0 | 21.585 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.034 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.212 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.366 | 130 | 16 | 1 | within |
| notice-burst-0 | 23.537 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.056 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.198 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.369 | 130 | 16 | 1 | within |
| notice-burst-0 | 25.541 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.397 | 130 | 16 | 0 | within |
| notice-burst-2 | 4.571 | 130 | 16 | 0 | within |
| notice-burst-2 | 5.209 | 130 | 16 | 0 | within |
| notice-burst-2 | 5.381 | 130 | 16 | 0 | within |
| notice-burst-2 | 14.855 | 130 | 16 | 0 | within |
| notice-burst-2 | 15.037 | 130 | 16 | 0 | within |
| notice-burst-2 | 15.200 | 130 | 16 | 0 | within |
| notice-burst-2 | 15.372 | 130 | 16 | 0 | within |
| notice-burst-2 | 16.810 | 130 | 16 | 0 | within |
| notice-burst-2 | 16.984 | 130 | 16 | 0 | within |
| notice-burst-2 | 1.727 | 130 | 16 | 0 | within |
| notice-burst-2 | 1.914 | 130 | 16 | 0 | within |
| notice-burst-2 | 17.147 | 130 | 16 | 0 | within |
| notice-burst-2 | 17.315 | 130 | 16 | 0 | within |
| notice-burst-2 | 18.722 | 130 | 16 | 0 | within |
| notice-burst-2 | 18.900 | 130 | 16 | 0 | within |
| notice-burst-2 | 19.067 | 130 | 16 | 0 | within |
| notice-burst-2 | 19.240 | 130 | 16 | 0 | within |
| notice-burst-2 | 5.550 | 130 | 16 | 0 | within |
| notice-burst-2 | 5.735 | 130 | 16 | 0 | within |
| notice-burst-2 | 2.989 | 130 | 16 | 0 | within |
| notice-burst-2 | 3.192 | 130 | 16 | 0 | within |
| notice-burst-2 | 20.620 | 130 | 16 | 0 | within |
| notice-burst-2 | 20.802 | 130 | 16 | 0 | within |
| notice-burst-2 | 3.380 | 130 | 16 | 0 | within |
| notice-burst-2 | 3.578 | 130 | 16 | 0 | within |
| notice-burst-2 | 2.103 | 130 | 16 | 0 | within |
| notice-burst-2 | 2.305 | 130 | 16 | 0 | within |
| notice-burst-2 | 4.754 | 130 | 16 | 0 | within |
| notice-burst-2 | 4.947 | 130 | 16 | 0 | within |
| notice-burst-2 | 20.965 | 130 | 16 | 0 | within |
| notice-burst-2 | 21.138 | 130 | 16 | 0 | within |
| notice-burst-2 | 22.793 | 130 | 16 | 0 | within |
| notice-burst-2 | 22.970 | 130 | 16 | 0 | within |
| notice-burst-2 | 23.125 | 130 | 16 | 0 | within |
| notice-burst-2 | 23.296 | 130 | 16 | 0 | within |
| notice-burst-2 | 24.613 | 130 | 16 | 0 | within |
| notice-burst-2 | 24.756 | 130 | 16 | 0 | within |
| notice-burst-2 | 24.926 | 130 | 16 | 0 | within |
| notice-burst-2 | 25.097 | 130 | 16 | 0 | within |
| notice-burst-4 | 14.700 | 130 | 16 | 0 | within |
| notice-burst-4 | 14.880 | 130 | 16 | 0 | within |
| notice-burst-4 | 15.043 | 130 | 16 | 0 | within |
| notice-burst-4 | 15.212 | 130 | 16 | 0 | within |
| notice-burst-4 | 16.647 | 130 | 16 | 0 | within |
| notice-burst-4 | 16.821 | 130 | 16 | 0 | within |
| notice-burst-4 | 16.984 | 130 | 16 | 0 | within |
| notice-burst-4 | 17.157 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.576 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.756 | 130 | 16 | 0 | within |
| notice-burst-4 | 18.774 | 130 | 16 | 0 | within |
| notice-burst-4 | 18.948 | 130 | 16 | 0 | within |
| notice-burst-4 | 1.708 | 130 | 16 | 0 | within |
| notice-burst-4 | 1.897 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.931 | 130 | 16 | 0 | within |
| notice-burst-4 | 3.115 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.201 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.390 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.555 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.738 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.007 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.197 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.370 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.558 | 130 | 16 | 0 | within |
| notice-burst-4 | 19.109 | 130 | 16 | 0 | within |
| notice-burst-4 | 19.283 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.086 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.288 | 130 | 16 | 0 | within |
| notice-burst-4 | 20.664 | 130 | 16 | 0 | within |
| notice-burst-4 | 20.838 | 130 | 16 | 0 | within |
| notice-burst-4 | 20.998 | 130 | 16 | 0 | within |
| notice-burst-4 | 21.171 | 130 | 16 | 0 | within |
| notice-burst-4 | 22.617 | 130 | 16 | 0 | within |
| notice-burst-4 | 22.795 | 130 | 16 | 0 | within |
| notice-burst-4 | 22.949 | 130 | 16 | 0 | within |
| notice-burst-4 | 23.121 | 130 | 16 | 0 | within |
| notice-burst-4 | 24.640 | 130 | 16 | 0 | within |
| notice-burst-4 | 24.782 | 130 | 16 | 0 | within |
| notice-burst-4 | 24.953 | 130 | 16 | 0 | within |
| notice-burst-4 | 25.124 | 130 | 16 | 0 | within |
| notice-burst-6 | 14.976 | 130 | 16 | 0 | within |
| notice-burst-6 | 15.156 | 130 | 16 | 0 | within |
| notice-burst-6 | 15.319 | 130 | 16 | 0 | within |
| notice-burst-6 | 15.488 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.935 | 130 | 16 | 0 | within |
| notice-burst-6 | 3.110 | 130 | 16 | 0 | within |
| notice-burst-6 | 3.275 | 130 | 16 | 0 | within |
| notice-burst-6 | 3.452 | 130 | 16 | 0 | within |
| notice-burst-6 | 4.304 | 130 | 16 | 0 | within |
| notice-burst-6 | 4.482 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.067 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.255 | 130 | 16 | 0 | within |
| notice-burst-6 | 4.648 | 130 | 16 | 0 | within |
| notice-burst-6 | 4.821 | 130 | 16 | 0 | within |
| notice-burst-6 | 5.298 | 130 | 16 | 0 | within |
| notice-burst-6 | 5.479 | 130 | 16 | 0 | within |
| notice-burst-6 | 5.646 | 130 | 16 | 0 | within |
| notice-burst-6 | 5.824 | 130 | 16 | 0 | within |
| notice-burst-6 | 16.692 | 130 | 16 | 0 | within |
| notice-burst-6 | 16.869 | 130 | 16 | 0 | within |
| notice-burst-6 | 17.030 | 130 | 16 | 0 | within |
| notice-burst-6 | 17.205 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.594 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.776 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.941 | 130 | 16 | 0 | within |
| notice-burst-6 | 19.114 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.445 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.647 | 130 | 16 | 0 | within |
| notice-burst-6 | 20.695 | 130 | 16 | 0 | within |
| notice-burst-6 | 20.868 | 130 | 16 | 0 | within |
| notice-burst-6 | 21.028 | 130 | 16 | 0 | within |
| notice-burst-6 | 21.201 | 130 | 16 | 0 | within |
| notice-burst-6 | 22.591 | 130 | 16 | 0 | within |
| notice-burst-6 | 22.767 | 130 | 16 | 0 | within |
| notice-burst-6 | 22.922 | 130 | 16 | 0 | within |
| notice-burst-6 | 23.093 | 130 | 16 | 0 | within |
| notice-burst-6 | 24.611 | 130 | 16 | 0 | within |
| notice-burst-6 | 24.754 | 130 | 16 | 0 | within |
| notice-burst-6 | 24.924 | 130 | 16 | 0 | within |
| notice-burst-6 | 25.095 | 130 | 16 | 0 | within |

Latest: 25.541 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 303 | 79,727 (0.797) | 47,423 (0.474) |
| notice-every-2 | 303 | 79,727 (0.797) | 47,423 (0.474) |
| notice-every-4 | 303 | 79,727 (0.797) | 47,423 (0.474) |
| notice-every-6 | 303 | 79,727 (0.797) | 47,423 (0.474) |
| notice-burst-0 | 313 | 79,727 (0.797) | 47,423 (0.474) |
| notice-burst-2 | 313 | 79,727 (0.797) | 47,423 (0.474) |
| notice-burst-4 | 313 | 79,727 (0.797) | 47,423 (0.474) |
| notice-burst-6 | 313 | 120,923 (1.209) | 47,423 (0.474) |

Longest pass that carries a step: 120,923 CPU cycles (1.209 ms), notice-burst-6; longest step: 47,423 (0.474 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 430,349 | 4.303 | 130 | 134 | fits | 78,565 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 448,060 | 4.481 | 130 | 134 | fits | 78,565 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 630,819 | 6.308 | 130 | 134 | fits | 77,231 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 648,408 | 6.484 | 130 | 134 | fits | 77,231 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 828,557 | 8.286 | 130 | 134 | fits | 76,965 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 846,132 | 8.461 | 130 | 134 | fits | 76,965 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 219,935 | 2.199 | 130 | 134 | fits | 81,093 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 238,738 | 2.387 | 130 | 134 | fits | 81,093 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 255,714 | 2.557 | 130 | 134 | fits | 81,093 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 273,224 | 2.732 | 130 | 134 | fits | 81,093 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 464,772 | 4.648 | 130 | 134 | fits | 78,565 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 481,972 | 4.820 | 130 | 134 | fits | 78,565 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 665,256 | 6.653 | 130 | 134 | fits | 77,231 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 682,225 | 6.822 | 130 | 134 | fits | 77,231 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 863,064 | 8.631 | 130 | 134 | fits | 76,965 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 880,238 | 8.802 | 130 | 134 | fits | 76,965 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,024,205 | 10.242 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,042,003 | 10.420 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 1,057,436 | 10.574 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,074,541 | 10.745 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,238,981 | 12.390 | 130 | 134 | fits | 76,781 | 203 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,257,299 | 12.573 | 130 | 134 | fits | 76,781 | 203 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,273,614 | 12.736 | 130 | 134 | fits | 76,781 | 203 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,291,258 | 12.913 | 130 | 134 | fits | 76,781 | 203 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,430,519 | 14.305 | 130 | 134 | fits | 74,517 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,448,398 | 14.484 | 130 | 134 | fits | 74,517 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,464,332 | 14.643 | 130 | 134 | fits | 74,517 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,481,228 | 14.812 | 130 | 134 | fits | 74,517 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,618,232 | 16.182 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,635,651 | 16.357 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,651,504 | 16.515 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,668,767 | 16.688 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,824,241 | 18.242 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,841,801 | 18.418 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,857,238 | 18.572 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,874,276 | 18.743 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,026,229 | 20.262 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,040,429 | 20.404 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,057,446 | 20.574 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,074,666 | 20.747 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 554,903 | 5.549 | 20 | 200 | fits | 171,233 | 117 | 0.470 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 696,838 | 6.968 | 20 | 20 | fits | 142,407 | 81 | 0.600 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 514,431 | 5.144 | 20 | 24 | fits | 171,233 | 117 | 0.470 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 129,838 | 1.298 | 20 | 50 | fits | 157,813 | 249 | 0.322 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 934,992 | 9.350 | 20 | 20 | fits | 134,502 | 65 | 0.509 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 112,342 | 1.123 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 812,369 | 8.124 | 130 | 134 | fits | 77,299 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 829,800 | 8.298 | 130 | 134 | fits | 77,299 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 225,787 | 2.258 | 130 | 134 | fits | 79,884 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 243,877 | 2.439 | 130 | 134 | fits | 79,884 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 413,077 | 4.131 | 130 | 134 | fits | 78,870 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 431,019 | 4.310 | 130 | 134 | fits | 78,870 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 613,975 | 6.140 | 130 | 134 | fits | 77,871 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 632,004 | 6.320 | 130 | 134 | fits | 77,871 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 260,970 | 2.610 | 130 | 134 | fits | 79,884 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 278,480 | 2.785 | 130 | 134 | fits | 79,884 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 447,679 | 4.477 | 130 | 134 | fits | 78,870 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 464,879 | 4.649 | 130 | 134 | fits | 78,870 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 648,708 | 6.487 | 130 | 134 | fits | 77,871 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 665,677 | 6.657 | 130 | 134 | fits | 77,871 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 846,653 | 8.467 | 130 | 134 | fits | 77,299 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 863,827 | 8.638 | 130 | 134 | fits | 77,299 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 1,008,127 | 10.081 | 130 | 134 | fits | 75,509 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 1,025,925 | 10.259 | 130 | 134 | fits | 75,509 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 1,041,358 | 10.414 | 130 | 134 | fits | 75,509 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 1,058,463 | 10.585 | 130 | 134 | fits | 75,509 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 1,219,310 | 12.193 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 1,237,489 | 12.375 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 1,253,804 | 12.538 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 1,271,448 | 12.714 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 1,414,232 | 14.142 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 1,432,250 | 14.322 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 1,448,184 | 14.482 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 1,465,080 | 14.651 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 1,622,745 | 16.227 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 1,640,164 | 16.402 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 1,656,017 | 16.560 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 1,673,280 | 16.733 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 1,808,200 | 18.082 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 1,825,760 | 18.258 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 1,841,197 | 18.412 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 1,858,235 | 18.582 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 2,010,227 | 20.102 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 2,024,460 | 20.245 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 2,041,477 | 20.415 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 2,058,697 | 20.587 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 403,758 | 4.038 | 20 | 200 | fits | 48,509 | 71 | 0.340 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 637,590 | 6.376 | 20 | 20 | fits | 140,945 | 136 | 0.551 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 457,767 | 4.578 | 20 | 24 | fits | 153,608 | 108 | 0.464 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 598,115 | 5.981 | 20 | 50 | fits | 140,945 | 136 | 0.551 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 963,691 | 9.637 | 20 | 20 | fits | 70,011 | 43 | 0.692 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 97,182 | 0.972 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 817,575 | 8.176 | 130 | 134 | fits | 77,299 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 835,006 | 8.350 | 130 | 134 | fits | 77,299 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 441,969 | 4.420 | 130 | 134 | fits | 78,969 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 460,079 | 4.601 | 130 | 134 | fits | 78,969 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 619,660 | 6.197 | 130 | 134 | fits | 77,546 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 637,322 | 6.373 | 130 | 134 | fits | 77,546 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 226,301 | 2.263 | 130 | 134 | fits | 81,086 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 245,062 | 2.451 | 130 | 134 | fits | 81,086 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 262,011 | 2.620 | 130 | 134 | fits | 81,086 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 279,521 | 2.795 | 130 | 134 | fits | 81,086 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 476,791 | 4.768 | 130 | 134 | fits | 78,969 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 493,991 | 4.940 | 130 | 134 | fits | 78,969 | 203 | 0.166 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 654,029 | 6.540 | 130 | 134 | fits | 77,546 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 670,998 | 6.710 | 130 | 134 | fits | 77,546 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 851,859 | 8.519 | 130 | 134 | fits | 77,299 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 869,033 | 8.690 | 130 | 134 | fits | 77,299 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 1,034,827 | 10.348 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 1,052,625 | 10.526 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 1,068,031 | 10.680 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 1,085,136 | 10.851 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 1,224,833 | 12.248 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 1,243,012 | 12.430 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 1,259,327 | 12.593 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 1,276,971 | 12.770 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 1,419,780 | 14.198 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 1,437,798 | 14.378 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 1,453,732 | 14.537 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 1,470,628 | 14.706 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 1,628,293 | 16.283 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 1,645,712 | 16.457 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 1,661,565 | 16.616 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 1,678,828 | 16.788 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 1,834,263 | 18.343 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 1,851,823 | 18.518 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 1,867,260 | 18.673 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 1,884,298 | 18.843 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 2,016,063 | 20.161 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 2,030,296 | 20.303 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 2,047,313 | 20.473 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 2,064,533 | 20.645 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 354,276 | 3.543 | 20 | 200 | fits | 127,464 | 123 | 0.363 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 612,747 | 6.127 | 20 | 20 | fits | 136,971 | 135 | 0.562 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 455,572 | 4.556 | 20 | 24 | fits | 153,072 | 102 | 0.475 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 573,272 | 5.733 | 20 | 50 | fits | 136,971 | 135 | 0.562 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 939,533 | 9.395 | 20 | 20 | fits | 76,346 | 41 | 0.660 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 80,879 | 0.809 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 219,388 | 2.194 | 130 | 134 | fits | 79,409 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 237,121 | 2.371 | 130 | 134 | fits | 79,409 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 405,869 | 4.059 | 130 | 134 | fits | 78,572 | 205 | 0.166 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 423,748 | 4.237 | 130 | 134 | fits | 78,572 | 205 | 0.166 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 606,072 | 6.061 | 130 | 134 | fits | 76,927 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 623,503 | 6.235 | 130 | 134 | fits | 76,927 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 829,923 | 8.299 | 130 | 134 | fits | 76,927 | 203 | 0.149 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 847,721 | 8.477 | 130 | 134 | fits | 76,927 | 203 | 0.149 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 254,179 | 2.542 | 130 | 134 | fits | 79,409 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 271,689 | 2.717 | 130 | 134 | fits | 79,409 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 440,487 | 4.405 | 130 | 134 | fits | 78,572 | 205 | 0.166 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 457,687 | 4.577 | 130 | 134 | fits | 78,572 | 205 | 0.166 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 640,237 | 6.402 | 130 | 134 | fits | 76,927 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 657,206 | 6.572 | 130 | 134 | fits | 76,927 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 864,482 | 8.645 | 130 | 134 | fits | 76,927 | 203 | 0.149 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 881,656 | 8.817 | 130 | 134 | fits | 76,927 | 203 | 0.149 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 1,024,536 | 10.245 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 1,042,334 | 10.423 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 1,057,767 | 10.578 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,074,872 | 10.749 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,214,608 | 12.146 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,232,787 | 12.328 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,249,102 | 12.491 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,266,746 | 12.667 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,409,569 | 14.096 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,427,587 | 14.276 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,443,521 | 14.435 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,460,417 | 14.604 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,618,082 | 16.181 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,635,501 | 16.355 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,651,354 | 16.514 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,668,617 | 16.686 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,824,052 | 18.241 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,841,612 | 18.416 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,857,049 | 18.570 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,874,087 | 18.741 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,005,852 | 20.059 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,020,052 | 20.201 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,037,069 | 20.371 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,054,289 | 20.543 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 700,009 | 7.000 | 20 | 200 | fits | 138,262 | 95 | 0.568 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 679,741 | 6.797 | 20 | 20 | fits | 138,262 | 95 | 0.568 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 366,548 | 3.665 | 20 | 24 | fits | 104,633 | 75 | 0.464 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 477,028 | 4.770 | 20 | 50 | fits | 158,222 | 252 | 0.325 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 989,242 | 9.892 | 20 | 20 | fits | 59,043 | 33 | 0.726 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 81,379 | 0.814 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 265,035 | 2.650 | 130 | 134 | fits | 108,067 | 211 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 282,608 | 2.826 | 130 | 134 | fits | 108,067 | 211 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 350,574 | 3.506 | 130 | 134 | fits | 83,213 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 367,798 | 3.678 | 130 | 134 | fits | 83,213 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 575,876 | 5.759 | 130 | 134 | fits | 74,967 | 205 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 593,086 | 5.931 | 130 | 134 | fits | 74,967 | 205 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 609,285 | 6.093 | 130 | 134 | fits | 74,967 | 205 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 626,462 | 6.265 | 130 | 134 | fits | 74,967 | 205 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 1,534,135 | 15.341 | 130 | 134 | fits | 78,219 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 1,552,183 | 15.522 | 130 | 134 | fits | 78,219 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 1,568,205 | 15.682 | 130 | 134 | fits | 78,219 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 1,585,015 | 15.850 | 130 | 134 | fits | 78,219 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 492,916 | 4.929 | 130 | 134 | fits | 106,146 | 211 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 511,176 | 5.112 | 130 | 134 | fits | 106,146 | 211 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 1,706,294 | 17.063 | 130 | 134 | fits | 76,628 | 203 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 1,724,100 | 17.241 | 130 | 134 | fits | 76,628 | 203 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 1,740,746 | 17.407 | 130 | 134 | fits | 76,628 | 203 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 1,758,081 | 17.581 | 130 | 134 | fits | 76,628 | 203 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 1,917,957 | 19.180 | 130 | 134 | fits | 74,712 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 1,935,683 | 19.357 | 130 | 134 | fits | 74,712 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 1,951,706 | 19.517 | 130 | 134 | fits | 74,712 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 1,969,264 | 19.693 | 130 | 134 | fits | 74,712 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 2,106,740 | 21.067 | 130 | 134 | fits | 75,025 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 2,124,835 | 21.248 | 130 | 134 | fits | 75,025 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 386,267 | 3.863 | 130 | 134 | fits | 83,213 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 406,242 | 4.062 | 130 | 134 | fits | 83,213 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 301,803 | 3.018 | 130 | 134 | fits | 108,067 | 211 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 322,017 | 3.220 | 130 | 134 | fits | 108,067 | 211 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 529,588 | 5.296 | 130 | 134 | fits | 106,146 | 211 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 549,030 | 5.490 | 130 | 134 | fits | 106,146 | 211 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,141,134 | 21.411 | 130 | 134 | fits | 75,025 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,158,469 | 21.585 | 130 | 134 | fits | 75,025 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,303,398 | 23.034 | 130 | 134 | fits | 73,581 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,321,166 | 23.212 | 130 | 134 | fits | 73,581 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 2,336,612 | 23.366 | 130 | 134 | fits | 73,581 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 2,353,722 | 23.537 | 130 | 134 | fits | 73,581 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 2,505,597 | 25.056 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,519,830 | 25.198 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,536,908 | 25.369 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 2,554,056 | 25.541 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 539,329 | 5.393 | 20 | 200 | fits | 154,020 | 222 | 0.265 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 655,916 | 6.559 | 20 | 20 | fits | 136,855 | 61 | 0.624 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 344,837 | 3.448 | 20 | 24 | fits | 167,222 | 155 | 0.457 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 479,586 | 4.796 | 20 | 50 | fits | 154,020 | 222 | 0.265 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 846,671 | 8.467 | 20 | 20 | fits | 115,472 | 54 | 0.531 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 439,671 | 4.397 | 130 | 134 | fits | 103,365 | 211 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 457,072 | 4.571 | 130 | 134 | fits | 103,365 | 211 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 520,860 | 5.209 | 130 | 134 | fits | 77,250 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 538,084 | 5.381 | 130 | 134 | fits | 77,250 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 1,485,538 | 14.855 | 130 | 134 | fits | 79,215 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 1,503,661 | 15.037 | 130 | 134 | fits | 79,215 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 1,520,050 | 15.200 | 130 | 134 | fits | 79,215 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 1,537,227 | 15.372 | 130 | 134 | fits | 79,215 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 1,681,006 | 16.810 | 130 | 134 | fits | 75,186 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 1,698,444 | 16.984 | 130 | 134 | fits | 75,186 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 172,719 | 1.727 | 130 | 134 | fits | 109,544 | 213 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 191,353 | 1.914 | 130 | 134 | fits | 109,544 | 213 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 1,714,654 | 17.147 | 130 | 134 | fits | 75,186 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 1,731,464 | 17.315 | 130 | 134 | fits | 75,186 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 1,872,187 | 18.722 | 130 | 134 | fits | 76,520 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 1,889,993 | 18.900 | 130 | 134 | fits | 76,520 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 1,906,666 | 19.067 | 130 | 134 | fits | 76,520 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 1,924,001 | 19.240 | 130 | 134 | fits | 76,520 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 554,983 | 5.550 | 130 | 134 | fits | 77,250 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 573,546 | 5.735 | 130 | 134 | fits | 77,250 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 298,885 | 2.989 | 130 | 134 | fits | 89,607 | 203 | 0.145 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 319,158 | 3.192 | 130 | 134 | fits | 89,607 | 203 | 0.145 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 2,061,999 | 20.620 | 130 | 134 | fits | 75,139 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 2,080,185 | 20.802 | 130 | 134 | fits | 75,139 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 337,967 | 3.380 | 130 | 134 | fits | 89,607 | 203 | 0.145 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 357,784 | 3.578 | 130 | 134 | fits | 89,607 | 203 | 0.145 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 210,272 | 2.103 | 130 | 134 | fits | 109,544 | 213 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 230,486 | 2.305 | 130 | 134 | fits | 109,544 | 213 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 475,435 | 4.754 | 130 | 134 | fits | 103,365 | 211 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 494,719 | 4.947 | 130 | 134 | fits | 103,365 | 211 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 2,096,484 | 20.965 | 130 | 134 | fits | 75,139 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 2,113,819 | 21.138 | 130 | 134 | fits | 75,139 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 2,279,281 | 22.793 | 130 | 134 | fits | 73,590 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 2,297,049 | 22.970 | 130 | 134 | fits | 73,590 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 2,312,495 | 23.125 | 130 | 134 | fits | 73,590 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 2,329,605 | 23.296 | 130 | 134 | fits | 73,590 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 2,461,343 | 24.613 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,475,576 | 24.756 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,492,593 | 24.926 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 2,509,741 | 25.097 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 531,219 | 5.312 | 20 | 200 | fits | 153,989 | 222 | 0.264 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 647,877 | 6.479 | 20 | 20 | fits | 136,926 | 61 | 0.622 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 336,758 | 3.368 | 20 | 24 | fits | 171,432 | 158 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 471,476 | 4.715 | 20 | 50 | fits | 153,989 | 222 | 0.264 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 838,835 | 8.388 | 20 | 20 | fits | 115,495 | 54 | 0.531 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,469,976 | 14.700 | 130 | 134 | fits | 79,169 | 203 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,487,954 | 14.880 | 130 | 134 | fits | 79,169 | 203 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,504,269 | 15.043 | 130 | 134 | fits | 79,169 | 203 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,521,237 | 15.212 | 130 | 134 | fits | 79,169 | 203 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 1,664,747 | 16.647 | 130 | 134 | fits | 75,807 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 1,682,106 | 16.821 | 130 | 134 | fits | 75,807 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 1,698,443 | 16.984 | 130 | 134 | fits | 75,807 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 1,715,699 | 17.157 | 130 | 134 | fits | 75,807 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 257,626 | 2.576 | 130 | 134 | fits | 80,600 | 205 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 275,582 | 2.756 | 130 | 134 | fits | 80,600 | 205 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 1,877,405 | 18.774 | 130 | 134 | fits | 75,307 | 203 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 1,894,764 | 18.948 | 130 | 134 | fits | 75,307 | 203 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 170,830 | 1.708 | 130 | 134 | fits | 110,762 | 213 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 189,695 | 1.897 | 130 | 134 | fits | 110,762 | 213 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 293,080 | 2.931 | 130 | 134 | fits | 80,600 | 205 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 311,481 | 3.115 | 130 | 134 | fits | 80,600 | 205 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 420,070 | 4.201 | 130 | 134 | fits | 103,263 | 211 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 439,021 | 4.390 | 130 | 134 | fits | 103,263 | 211 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 455,512 | 4.555 | 130 | 134 | fits | 103,263 | 211 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 473,844 | 4.738 | 130 | 134 | fits | 103,263 | 211 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 500,736 | 5.007 | 130 | 134 | fits | 80,391 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 519,703 | 5.197 | 130 | 134 | fits | 80,391 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 536,951 | 5.370 | 130 | 134 | fits | 80,391 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 555,822 | 5.558 | 130 | 134 | fits | 80,391 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 1,910,929 | 19.109 | 130 | 134 | fits | 75,307 | 203 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 1,928,278 | 19.283 | 130 | 134 | fits | 75,307 | 203 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 208,614 | 2.086 | 130 | 134 | fits | 110,762 | 213 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 228,828 | 2.288 | 130 | 134 | fits | 110,762 | 213 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 2,066,392 | 20.664 | 130 | 134 | fits | 74,067 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 2,083,830 | 20.838 | 130 | 134 | fits | 74,067 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 2,099,757 | 20.998 | 130 | 134 | fits | 74,067 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 2,117,092 | 21.171 | 130 | 134 | fits | 74,067 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 2,261,727 | 22.617 | 130 | 134 | fits | 73,535 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 2,279,495 | 22.795 | 130 | 134 | fits | 73,535 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 2,294,941 | 22.949 | 130 | 134 | fits | 73,535 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 2,312,051 | 23.121 | 130 | 134 | fits | 73,535 | 203 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 2,464,000 | 24.640 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 2,478,233 | 24.782 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,495,250 | 24.953 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,512,398 | 25.124 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 509,549 | 5.095 | 20 | 200 | fits | 164,481 | 150 | 0.441 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 626,624 | 6.266 | 20 | 20 | fits | 137,343 | 67 | 0.602 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 469,077 | 4.691 | 20 | 24 | fits | 164,481 | 150 | 0.441 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 449,806 | 4.498 | 20 | 50 | fits | 164,481 | 150 | 0.441 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 826,421 | 8.264 | 20 | 20 | fits | 124,205 | 58 | 0.516 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 1,497,584 | 14.976 | 130 | 134 | fits | 79,212 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,515,553 | 15.156 | 130 | 134 | fits | 79,212 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,531,853 | 15.319 | 130 | 134 | fits | 79,212 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,548,821 | 15.488 | 130 | 134 | fits | 79,212 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 293,462 | 2.935 | 130 | 134 | fits | 78,110 | 205 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 310,956 | 3.110 | 130 | 134 | fits | 78,110 | 205 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 327,538 | 3.275 | 130 | 134 | fits | 78,110 | 205 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 345,177 | 3.452 | 130 | 134 | fits | 78,110 | 205 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 430,394 | 4.304 | 130 | 134 | fits | 120,923 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 448,208 | 4.482 | 130 | 134 | fits | 120,923 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 206,734 | 2.067 | 130 | 134 | fits | 110,251 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 225,462 | 2.255 | 130 | 134 | fits | 110,251 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 464,788 | 4.648 | 130 | 134 | fits | 120,923 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 482,060 | 4.821 | 130 | 134 | fits | 120,923 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 529,812 | 5.298 | 130 | 134 | fits | 78,226 | 205 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 547,883 | 5.479 | 130 | 134 | fits | 78,226 | 205 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 564,640 | 5.646 | 130 | 134 | fits | 78,226 | 205 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 582,358 | 5.824 | 130 | 134 | fits | 78,226 | 205 | 0.083 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,669,221 | 16.692 | 130 | 134 | fits | 75,196 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,686,947 | 16.869 | 130 | 134 | fits | 75,196 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,702,970 | 17.030 | 130 | 134 | fits | 75,196 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 1,720,528 | 17.205 | 130 | 134 | fits | 75,196 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 1,859,406 | 18.594 | 130 | 134 | fits | 75,862 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 1,877,580 | 18.776 | 130 | 134 | fits | 75,862 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 1,894,084 | 18.941 | 130 | 134 | fits | 75,862 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 1,911,433 | 19.114 | 130 | 134 | fits | 75,862 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 244,499 | 2.445 | 130 | 134 | fits | 110,251 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 264,713 | 2.647 | 130 | 134 | fits | 110,251 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 2,069,479 | 20.695 | 130 | 134 | fits | 73,936 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 2,086,826 | 20.868 | 130 | 134 | fits | 73,936 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 2,102,753 | 21.028 | 130 | 134 | fits | 73,936 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 2,120,088 | 21.201 | 130 | 134 | fits | 73,936 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 2,259,095 | 22.591 | 130 | 134 | fits | 73,166 | 203 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 2,276,722 | 22.767 | 130 | 134 | fits | 73,166 | 203 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 2,292,168 | 22.922 | 130 | 134 | fits | 73,166 | 203 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 2,309,278 | 23.093 | 130 | 134 | fits | 73,166 | 203 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,461,144 | 24.611 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,475,377 | 24.754 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,492,394 | 24.924 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,509,542 | 25.095 | 130 | 134 | fits | 68,631 | 202 | 0.110 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 550,482 | 5.505 | 20 | 200 | fits | 154,050 | 223 | 0.260 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 666,949 | 6.669 | 20 | 20 | fits | 136,735 | 61 | 0.622 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 355,960 | 3.560 | 20 | 24 | fits | 186,808 | 168 | 0.445 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 490,739 | 4.907 | 20 | 50 | fits | 154,050 | 223 | 0.260 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 858,046 | 8.580 | 20 | 20 | fits | 115,742 | 54 | 0.536 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
