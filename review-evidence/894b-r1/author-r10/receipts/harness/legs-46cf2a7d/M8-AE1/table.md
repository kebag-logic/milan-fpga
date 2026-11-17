### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 364 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 7.555 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.adp.if0` (notice-burst-5) | 6.422 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.aecp.if0` (notice-every-5) | 4.835 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.maap.if0` (notice-every-5) | 6.275 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.srp.if0` (notice-burst-5) | 9.508 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-5.mrpdu.periodic.if0` (notice-every-5) | 1.184 | fits | 0 srp | 4 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-1.notices.29.36.0.if0` (notice-burst-1) | 25.625 (25.703) | fits | 1 events | 320 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-1 | 1360 | 0 | 187,062 (1.871) | fits |
| notice-every-3 | 1351 | 0 | 186,733 (1.867) | fits |
| notice-every-5 | 1352 | 0 | 162,829 (1.628) | fits |
| notice-every-7 | 1349 | 0 | 163,109 (1.631) | fits |
| notice-burst-1 | 1111 | 0 | 180,959 (1.810) | fits |
| notice-burst-3 | 1096 | 0 | 167,970 (1.680) | fits |
| notice-burst-5 | 1095 | 0 | 184,898 (1.849) | fits |
| notice-burst-7 | 1094 | 0 | 179,274 (1.793) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-1 | 4.078 | 130 | 16 | 2 | within |
| notice-every-1 | 4.255 | 130 | 16 | 2 | within |
| notice-every-1 | 6.084 | 130 | 16 | 2 | within |
| notice-every-1 | 6.260 | 130 | 16 | 2 | within |
| notice-every-1 | 8.061 | 130 | 16 | 2 | within |
| notice-every-1 | 8.237 | 130 | 16 | 2 | within |
| notice-every-1 | 2.201 | 130 | 16 | 2 | within |
| notice-every-1 | 2.389 | 130 | 16 | 2 | within |
| notice-every-1 | 2.559 | 130 | 16 | 2 | within |
| notice-every-1 | 2.734 | 130 | 16 | 2 | within |
| notice-every-1 | 4.423 | 130 | 16 | 2 | within |
| notice-every-1 | 4.595 | 130 | 16 | 2 | within |
| notice-every-1 | 6.428 | 130 | 16 | 2 | within |
| notice-every-1 | 6.598 | 130 | 16 | 2 | within |
| notice-every-1 | 8.406 | 130 | 16 | 2 | within |
| notice-every-1 | 8.578 | 130 | 16 | 2 | within |
| notice-every-1 | 10.236 | 130 | 16 | 2 | within |
| notice-every-1 | 10.414 | 130 | 16 | 2 | within |
| notice-every-1 | 10.568 | 130 | 16 | 2 | within |
| notice-every-1 | 10.739 | 130 | 16 | 2 | within |
| notice-every-1 | 12.136 | 130 | 16 | 2 | within |
| notice-every-1 | 12.318 | 130 | 16 | 2 | within |
| notice-every-1 | 12.481 | 130 | 16 | 2 | within |
| notice-every-1 | 12.657 | 130 | 16 | 2 | within |
| notice-every-1 | 14.086 | 130 | 16 | 2 | within |
| notice-every-1 | 14.266 | 130 | 16 | 2 | within |
| notice-every-1 | 14.425 | 130 | 16 | 2 | within |
| notice-every-1 | 14.594 | 130 | 16 | 2 | within |
| notice-every-1 | 16.171 | 130 | 16 | 2 | within |
| notice-every-1 | 16.345 | 130 | 16 | 2 | within |
| notice-every-1 | 16.503 | 130 | 16 | 2 | within |
| notice-every-1 | 16.676 | 130 | 16 | 2 | within |
| notice-every-1 | 18.230 | 130 | 16 | 2 | within |
| notice-every-1 | 18.406 | 130 | 16 | 2 | within |
| notice-every-1 | 18.560 | 130 | 16 | 2 | within |
| notice-every-1 | 18.731 | 130 | 16 | 2 | within |
| notice-every-1 | 20.048 | 130 | 16 | 2 | within |
| notice-every-1 | 20.190 | 130 | 16 | 2 | within |
| notice-every-1 | 20.361 | 130 | 16 | 2 | within |
| notice-every-1 | 20.533 | 130 | 16 | 2 | within |
| notice-every-3 | 8.119 | 130 | 16 | 2 | within |
| notice-every-3 | 8.293 | 130 | 16 | 2 | within |
| notice-every-3 | 2.028 | 130 | 16 | 2 | within |
| notice-every-3 | 2.209 | 130 | 16 | 2 | within |
| notice-every-3 | 4.127 | 130 | 16 | 2 | within |
| notice-every-3 | 4.306 | 130 | 16 | 2 | within |
| notice-every-3 | 6.135 | 130 | 16 | 2 | within |
| notice-every-3 | 6.315 | 130 | 16 | 2 | within |
| notice-every-3 | 2.380 | 130 | 16 | 2 | within |
| notice-every-3 | 2.555 | 130 | 16 | 2 | within |
| notice-every-3 | 4.473 | 130 | 16 | 2 | within |
| notice-every-3 | 4.645 | 130 | 16 | 2 | within |
| notice-every-3 | 6.482 | 130 | 16 | 2 | within |
| notice-every-3 | 6.652 | 130 | 16 | 2 | within |
| notice-every-3 | 8.462 | 130 | 16 | 2 | within |
| notice-every-3 | 8.633 | 130 | 16 | 2 | within |
| notice-every-3 | 10.074 | 130 | 16 | 2 | within |
| notice-every-3 | 10.252 | 130 | 16 | 2 | within |
| notice-every-3 | 10.407 | 130 | 16 | 2 | within |
| notice-every-3 | 10.578 | 130 | 16 | 2 | within |
| notice-every-3 | 12.222 | 130 | 16 | 2 | within |
| notice-every-3 | 12.405 | 130 | 16 | 2 | within |
| notice-every-3 | 12.569 | 130 | 16 | 2 | within |
| notice-every-3 | 12.745 | 130 | 16 | 2 | within |
| notice-every-3 | 14.138 | 130 | 16 | 2 | within |
| notice-every-3 | 14.316 | 130 | 16 | 2 | within |
| notice-every-3 | 14.476 | 130 | 16 | 2 | within |
| notice-every-3 | 14.645 | 130 | 16 | 2 | within |
| notice-every-3 | 16.015 | 130 | 16 | 2 | within |
| notice-every-3 | 16.189 | 130 | 16 | 2 | within |
| notice-every-3 | 16.347 | 130 | 16 | 2 | within |
| notice-every-3 | 16.520 | 130 | 16 | 2 | within |
| notice-every-3 | 18.075 | 130 | 16 | 2 | within |
| notice-every-3 | 18.250 | 130 | 16 | 2 | within |
| notice-every-3 | 18.405 | 130 | 16 | 2 | within |
| notice-every-3 | 18.575 | 130 | 16 | 2 | within |
| notice-every-3 | 20.095 | 130 | 16 | 2 | within |
| notice-every-3 | 20.237 | 130 | 16 | 2 | within |
| notice-every-3 | 20.407 | 130 | 16 | 2 | within |
| notice-every-3 | 20.579 | 130 | 16 | 2 | within |
| notice-every-5 | 8.170 | 130 | 16 | 2 | within |
| notice-every-5 | 8.345 | 130 | 16 | 2 | within |
| notice-every-5 | 2.258 | 130 | 16 | 2 | within |
| notice-every-5 | 2.439 | 130 | 16 | 2 | within |
| notice-every-5 | 4.358 | 130 | 16 | 2 | within |
| notice-every-5 | 4.537 | 130 | 16 | 2 | within |
| notice-every-5 | 6.418 | 130 | 16 | 2 | within |
| notice-every-5 | 6.598 | 130 | 16 | 2 | within |
| notice-every-5 | 2.610 | 130 | 16 | 2 | within |
| notice-every-5 | 2.785 | 130 | 16 | 2 | within |
| notice-every-5 | 4.704 | 130 | 16 | 2 | within |
| notice-every-5 | 4.876 | 130 | 16 | 2 | within |
| notice-every-5 | 6.765 | 130 | 16 | 2 | within |
| notice-every-5 | 6.935 | 130 | 16 | 2 | within |
| notice-every-5 | 8.513 | 130 | 16 | 2 | within |
| notice-every-5 | 8.685 | 130 | 16 | 2 | within |
| notice-every-5 | 10.342 | 130 | 16 | 2 | within |
| notice-every-5 | 10.520 | 130 | 16 | 2 | within |
| notice-every-5 | 10.674 | 130 | 16 | 2 | within |
| notice-every-5 | 10.845 | 130 | 16 | 2 | within |
| notice-every-5 | 12.241 | 130 | 16 | 2 | within |
| notice-every-5 | 12.423 | 130 | 16 | 2 | within |
| notice-every-5 | 12.586 | 130 | 16 | 2 | within |
| notice-every-5 | 12.763 | 130 | 16 | 2 | within |
| notice-every-5 | 14.191 | 130 | 16 | 2 | within |
| notice-every-5 | 14.371 | 130 | 16 | 2 | within |
| notice-every-5 | 14.530 | 130 | 16 | 2 | within |
| notice-every-5 | 14.699 | 130 | 16 | 2 | within |
| notice-every-5 | 16.276 | 130 | 16 | 2 | within |
| notice-every-5 | 16.450 | 130 | 16 | 2 | within |
| notice-every-5 | 16.609 | 130 | 16 | 2 | within |
| notice-every-5 | 16.781 | 130 | 16 | 2 | within |
| notice-every-5 | 18.336 | 130 | 16 | 2 | within |
| notice-every-5 | 18.511 | 130 | 16 | 2 | within |
| notice-every-5 | 18.666 | 130 | 16 | 2 | within |
| notice-every-5 | 18.836 | 130 | 16 | 2 | within |
| notice-every-5 | 20.154 | 130 | 16 | 2 | within |
| notice-every-5 | 20.296 | 130 | 16 | 2 | within |
| notice-every-5 | 20.466 | 130 | 16 | 2 | within |
| notice-every-5 | 20.638 | 130 | 16 | 2 | within |
| notice-every-7 | 4.067 | 130 | 16 | 1 | within |
| notice-every-7 | 4.244 | 130 | 16 | 1 | within |
| notice-every-7 | 6.072 | 130 | 16 | 1 | within |
| notice-every-7 | 6.248 | 130 | 16 | 1 | within |
| notice-every-7 | 8.049 | 130 | 16 | 1 | within |
| notice-every-7 | 8.225 | 130 | 16 | 1 | within |
| notice-every-7 | 1.963 | 130 | 16 | 1 | within |
| notice-every-7 | 2.151 | 130 | 16 | 1 | within |
| notice-every-7 | 2.321 | 130 | 16 | 1 | within |
| notice-every-7 | 2.496 | 130 | 16 | 1 | within |
| notice-every-7 | 4.411 | 130 | 16 | 1 | within |
| notice-every-7 | 4.583 | 130 | 16 | 1 | within |
| notice-every-7 | 6.416 | 130 | 16 | 1 | within |
| notice-every-7 | 6.586 | 130 | 16 | 1 | within |
| notice-every-7 | 8.394 | 130 | 16 | 1 | within |
| notice-every-7 | 8.566 | 130 | 16 | 1 | within |
| notice-every-7 | 10.006 | 130 | 16 | 1 | within |
| notice-every-7 | 10.184 | 130 | 16 | 1 | within |
| notice-every-7 | 10.338 | 130 | 16 | 1 | within |
| notice-every-7 | 10.509 | 130 | 16 | 1 | within |
| notice-every-7 | 11.906 | 130 | 16 | 1 | within |
| notice-every-7 | 12.087 | 130 | 16 | 1 | within |
| notice-every-7 | 12.251 | 130 | 16 | 1 | within |
| notice-every-7 | 12.427 | 130 | 16 | 1 | within |
| notice-every-7 | 14.066 | 130 | 16 | 1 | within |
| notice-every-7 | 14.246 | 130 | 16 | 1 | within |
| notice-every-7 | 14.405 | 130 | 16 | 1 | within |
| notice-every-7 | 14.574 | 130 | 16 | 1 | within |
| notice-every-7 | 15.943 | 130 | 16 | 1 | within |
| notice-every-7 | 16.117 | 130 | 16 | 1 | within |
| notice-every-7 | 16.276 | 130 | 16 | 1 | within |
| notice-every-7 | 16.448 | 130 | 16 | 1 | within |
| notice-every-7 | 18.003 | 130 | 16 | 1 | within |
| notice-every-7 | 18.179 | 130 | 16 | 1 | within |
| notice-every-7 | 18.333 | 130 | 16 | 1 | within |
| notice-every-7 | 18.503 | 130 | 16 | 1 | within |
| notice-every-7 | 20.237 | 130 | 16 | 1 | within |
| notice-every-7 | 20.378 | 130 | 16 | 1 | within |
| notice-every-7 | 20.548 | 130 | 16 | 1 | within |
| notice-every-7 | 20.721 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.040 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.210 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.658 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.834 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.649 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.822 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.275 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.459 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.622 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.791 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.005 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.180 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.225 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.399 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.206 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.401 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.581 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.770 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.556 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.727 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.119 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.300 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.463 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.641 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.392 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.590 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.995 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.182 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.223 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.397 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.556 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.729 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.120 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.296 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.451 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.622 | 130 | 16 | 1 | within |
| notice-burst-1 | 25.140 | 130 | 16 | 1 | within |
| notice-burst-1 | 25.283 | 130 | 16 | 1 | within |
| notice-burst-1 | 25.454 | 130 | 16 | 1 | within |
| notice-burst-1 | 25.625 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.871 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.044 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.868 | 130 | 16 | 1 | within |
| notice-burst-3 | 7.041 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.422 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.603 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.766 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.938 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.189 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.371 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.503 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.682 | 130 | 16 | 1 | within |
| notice-burst-3 | 7.208 | 130 | 16 | 1 | within |
| notice-burst-3 | 7.381 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.149 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.328 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.656 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.852 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.851 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.037 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.490 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.666 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.557 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.759 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.036 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.231 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.219 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.405 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.256 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.430 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.590 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.763 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.360 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.537 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.691 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.862 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.180 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.322 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.493 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.665 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.467 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.648 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.810 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.980 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.180 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.357 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.523 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.699 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.624 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.799 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.186 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.361 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.523 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.691 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.770 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.961 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.972 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.154 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.990 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.177 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.820 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.007 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.177 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.364 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.286 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.464 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.623 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.792 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.152 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.352 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.359 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.556 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.143 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.318 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.473 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.644 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.259 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.402 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.575 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.747 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.043 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.224 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.047 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.225 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.182 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.357 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.522 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.696 | 130 | 16 | 1 | within |
| notice-burst-7 | 6.472 | 130 | 16 | 1 | within |
| notice-burst-7 | 6.644 | 130 | 16 | 1 | within |
| notice-burst-7 | 6.805 | 130 | 16 | 1 | within |
| notice-burst-7 | 6.975 | 130 | 16 | 1 | within |
| notice-burst-7 | 5.682 | 130 | 16 | 1 | within |
| notice-burst-7 | 5.863 | 130 | 16 | 1 | within |
| notice-burst-7 | 6.036 | 130 | 16 | 1 | within |
| notice-burst-7 | 6.216 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.391 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.564 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.401 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.592 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.121 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.302 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.465 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.643 | 130 | 16 | 1 | within |
| notice-burst-7 | 19.233 | 130 | 16 | 1 | within |
| notice-burst-7 | 19.410 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.883 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.085 | 130 | 16 | 1 | within |
| notice-burst-7 | 19.571 | 130 | 16 | 1 | within |
| notice-burst-7 | 19.741 | 130 | 16 | 1 | within |
| notice-burst-7 | 21.095 | 130 | 16 | 1 | within |
| notice-burst-7 | 21.271 | 130 | 16 | 1 | within |
| notice-burst-7 | 21.427 | 130 | 16 | 1 | within |
| notice-burst-7 | 21.598 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.274 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.483 | 130 | 16 | 1 | within |
| notice-burst-7 | 23.220 | 130 | 16 | 1 | within |
| notice-burst-7 | 23.363 | 130 | 16 | 1 | within |
| notice-burst-7 | 23.535 | 130 | 16 | 1 | within |
| notice-burst-7 | 23.706 | 130 | 16 | 1 | within |

Latest: 25.625 ms, notice-burst-1.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-1 | 303 | 79,727 (0.797) | 47,423 (0.474) |
| notice-every-3 | 303 | 79,727 (0.797) | 47,423 (0.474) |
| notice-every-5 | 303 | 79,727 (0.797) | 47,423 (0.474) |
| notice-every-7 | 303 | 79,727 (0.797) | 47,423 (0.474) |
| notice-burst-1 | 313 | 120,363 (1.204) | 47,423 (0.474) |
| notice-burst-3 | 313 | 121,330 (1.213) | 47,423 (0.474) |
| notice-burst-5 | 313 | 79,727 (0.797) | 47,423 (0.474) |
| notice-burst-7 | 313 | 79,727 (0.797) | 47,423 (0.474) |

Longest pass that carries a step: 121,330 CPU cycles (1.213 ms), notice-burst-3; longest step: 47,423 (0.474 ms), notice-every-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 407,810 | 4.078 | 130 | 134 | fits | 78,679 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 425,521 | 4.255 | 130 | 134 | fits | 78,679 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 608,371 | 6.084 | 130 | 134 | fits | 77,365 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 625,960 | 6.260 | 130 | 134 | fits | 77,365 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 806,131 | 8.061 | 130 | 134 | fits | 77,099 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 823,706 | 8.237 | 130 | 134 | fits | 77,099 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 220,112 | 2.201 | 130 | 134 | fits | 80,979 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 238,915 | 2.389 | 130 | 134 | fits | 80,979 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 255,864 | 2.559 | 130 | 134 | fits | 80,979 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 273,374 | 2.734 | 130 | 134 | fits | 80,979 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 442,260 | 4.423 | 130 | 134 | fits | 78,679 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 459,460 | 4.595 | 130 | 134 | fits | 78,679 | 205 | 0.170 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 642,808 | 6.428 | 130 | 134 | fits | 77,365 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 659,777 | 6.598 | 130 | 134 | fits | 77,365 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 840,638 | 8.406 | 130 | 134 | fits | 77,099 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 857,812 | 8.578 | 130 | 134 | fits | 77,099 | 205 | 0.155 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 1,023,584 | 10.236 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 1,041,382 | 10.414 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 1,056,788 | 10.568 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 1,073,893 | 10.739 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 1,213,590 | 12.136 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 1,231,769 | 12.318 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 1,248,084 | 12.481 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 1,265,728 | 12.657 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 1,408,551 | 14.086 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 1,426,569 | 14.266 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 1,442,503 | 14.425 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 1,459,399 | 14.594 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 1,617,064 | 16.171 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 1,634,483 | 16.345 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 1,650,336 | 16.503 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 1,667,599 | 16.676 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 1,823,034 | 18.230 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 1,840,594 | 18.406 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 1,856,031 | 18.560 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 1,873,069 | 18.731 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 2,004,834 | 20.048 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 2,019,034 | 20.190 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 2,036,051 | 20.361 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 2,053,271 | 20.533 | 130 | 134 | fits | 68,670 | 203 | 0.109 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 552,178 | 5.522 | 20 | 200 | fits | 151,778 | 219 | 0.338 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 694,594 | 6.946 | 20 | 20 | fits | 142,154 | 81 | 0.596 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 366,652 | 3.667 | 20 | 24 | fits | 104,622 | 75 | 0.464 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 492,435 | 4.924 | 20 | 50 | fits | 151,778 | 219 | 0.338 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 934,156 | 9.342 | 20 | 20 | fits | 135,949 | 69 | 0.513 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 103,135 | 1.031 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 811,870 | 8.119 | 130 | 134 | fits | 77,165 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 829,301 | 8.293 | 130 | 134 | fits | 77,165 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 202,789 | 2.028 | 130 | 134 | fits | 79,998 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 220,879 | 2.209 | 130 | 134 | fits | 79,998 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 412,685 | 4.127 | 130 | 134 | fits | 78,756 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 430,627 | 4.306 | 130 | 134 | fits | 78,756 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 613,506 | 6.135 | 130 | 134 | fits | 77,737 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 631,535 | 6.315 | 130 | 134 | fits | 77,737 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 237,999 | 2.380 | 130 | 134 | fits | 79,998 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 255,509 | 2.555 | 130 | 134 | fits | 79,998 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 447,260 | 4.473 | 130 | 134 | fits | 78,756 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 464,460 | 4.645 | 130 | 134 | fits | 78,756 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 648,239 | 6.482 | 130 | 134 | fits | 77,737 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 665,208 | 6.652 | 130 | 134 | fits | 77,737 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 846,154 | 8.462 | 130 | 134 | fits | 77,165 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 863,328 | 8.633 | 130 | 134 | fits | 77,165 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 1,007,447 | 10.074 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 1,025,245 | 10.252 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 1,040,678 | 10.407 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 1,057,783 | 10.578 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 1,222,223 | 12.222 | 130 | 134 | fits | 76,781 | 203 | 0.148 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 1,240,541 | 12.405 | 130 | 134 | fits | 76,781 | 203 | 0.148 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 1,256,856 | 12.569 | 130 | 134 | fits | 76,781 | 203 | 0.148 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 1,274,500 | 12.745 | 130 | 134 | fits | 76,781 | 203 | 0.148 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 1,413,761 | 14.138 | 130 | 134 | fits | 74,517 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 1,431,640 | 14.316 | 130 | 134 | fits | 74,517 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 1,447,574 | 14.476 | 130 | 134 | fits | 74,517 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 1,464,470 | 14.645 | 130 | 134 | fits | 74,517 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 1,601,474 | 16.015 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 1,618,893 | 16.189 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 1,634,746 | 16.347 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 1,652,009 | 16.520 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 1,807,483 | 18.075 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 1,825,043 | 18.250 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 1,840,480 | 18.405 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 1,857,518 | 18.575 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 2,009,471 | 20.095 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 2,023,704 | 20.237 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 2,040,721 | 20.407 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 2,057,941 | 20.579 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 546,333 | 5.463 | 20 | 200 | fits | 151,879 | 220 | 0.337 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 688,491 | 6.885 | 20 | 20 | fits | 141,918 | 79 | 0.596 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 382,574 | 3.826 | 20 | 24 | fits | 104,578 | 75 | 0.463 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 486,590 | 4.866 | 20 | 50 | fits | 151,879 | 220 | 0.337 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 918,934 | 9.189 | 20 | 20 | fits | 134,263 | 63 | 0.508 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 107,421 | 1.074 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 817,021 | 8.170 | 130 | 134 | fits | 77,225 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 834,452 | 8.345 | 130 | 134 | fits | 77,225 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 225,829 | 2.258 | 130 | 134 | fits | 79,998 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 243,919 | 2.439 | 130 | 134 | fits | 79,998 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 435,778 | 4.358 | 130 | 134 | fits | 78,756 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 453,720 | 4.537 | 130 | 134 | fits | 78,756 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 641,764 | 6.418 | 130 | 134 | fits | 77,733 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 659,793 | 6.598 | 130 | 134 | fits | 77,733 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 261,039 | 2.610 | 130 | 134 | fits | 79,998 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 278,549 | 2.785 | 130 | 134 | fits | 79,998 | 205 | 0.171 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 470,353 | 4.704 | 130 | 134 | fits | 78,756 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 487,553 | 4.876 | 130 | 134 | fits | 78,756 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 676,497 | 6.765 | 130 | 134 | fits | 77,733 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 693,466 | 6.935 | 130 | 134 | fits | 77,733 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 851,278 | 8.513 | 130 | 134 | fits | 77,225 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 868,452 | 8.685 | 130 | 134 | fits | 77,225 | 205 | 0.153 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 1,034,207 | 10.342 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 1,052,005 | 10.520 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 1,067,411 | 10.674 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 1,084,516 | 10.845 | 130 | 134 | fits | 75,482 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 1,224,134 | 12.241 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 1,242,313 | 12.423 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 1,258,628 | 12.586 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 1,276,272 | 12.763 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 1,419,081 | 14.191 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 1,437,099 | 14.371 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 1,453,033 | 14.530 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 1,469,929 | 14.699 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 1,627,594 | 16.276 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 1,645,013 | 16.450 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 1,660,866 | 16.609 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 1,678,129 | 16.781 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 1,833,564 | 18.336 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 1,851,124 | 18.511 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 1,866,561 | 18.666 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 1,883,599 | 18.836 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 2,015,364 | 20.154 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 2,029,597 | 20.296 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 2,046,614 | 20.466 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 2,063,834 | 20.638 | 130 | 134 | fits | 68,703 | 203 | 0.110 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 353,354 | 3.534 | 20 | 200 | fits | 127,464 | 123 | 0.363 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 666,989 | 6.670 | 20 | 20 | fits | 142,596 | 97 | 0.590 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 483,482 | 4.835 | 20 | 24 | fits | 162,600 | 130 | 0.502 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 627,514 | 6.275 | 20 | 50 | fits | 142,596 | 97 | 0.590 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 937,394 | 9.374 | 20 | 20 | fits | 39,288 | 19 | 0.818 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 118,407 | 1.184 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 406,716 | 4.067 | 130 | 134 | fits | 78,565 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 424,427 | 4.244 | 130 | 134 | fits | 78,565 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 607,186 | 6.072 | 130 | 134 | fits | 77,231 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 624,775 | 6.248 | 130 | 134 | fits | 77,231 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 804,924 | 8.049 | 130 | 134 | fits | 76,965 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 822,499 | 8.225 | 130 | 134 | fits | 76,965 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 196,295 | 1.963 | 130 | 134 | fits | 81,210 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 215,098 | 2.151 | 130 | 134 | fits | 81,210 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 232,120 | 2.321 | 130 | 134 | fits | 81,210 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 249,630 | 2.496 | 130 | 134 | fits | 81,210 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 441,139 | 4.411 | 130 | 134 | fits | 78,565 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 458,339 | 4.583 | 130 | 134 | fits | 78,565 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 641,623 | 6.416 | 130 | 134 | fits | 77,231 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 658,592 | 6.586 | 130 | 134 | fits | 77,231 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 839,431 | 8.394 | 130 | 134 | fits | 76,965 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 856,605 | 8.566 | 130 | 134 | fits | 76,965 | 203 | 0.154 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 1,000,572 | 10.006 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 1,018,370 | 10.184 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 1,033,803 | 10.338 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 1,050,908 | 10.509 | 130 | 134 | fits | 75,462 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 1,190,565 | 11.906 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 1,208,744 | 12.087 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 1,225,059 | 12.251 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 1,242,703 | 12.427 | 130 | 134 | fits | 76,402 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 1,406,556 | 14.066 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 1,424,574 | 14.246 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 1,440,508 | 14.405 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 1,457,404 | 14.574 | 130 | 134 | fits | 74,835 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 1,594,290 | 15.943 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 1,611,709 | 16.117 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 1,627,562 | 16.276 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 1,644,825 | 16.448 | 130 | 134 | fits | 73,912 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 1,800,299 | 18.003 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 1,817,859 | 18.179 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 1,833,296 | 18.333 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 1,850,334 | 18.503 | 130 | 134 | fits | 72,902 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 2,023,719 | 20.237 | 130 | 134 | fits | 68,943 | 203 | 0.117 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 2,037,832 | 20.378 | 130 | 134 | fits | 68,943 | 203 | 0.117 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 2,054,849 | 20.548 | 130 | 134 | fits | 68,943 | 203 | 0.117 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 2,072,069 | 20.721 | 130 | 134 | fits | 68,943 | 203 | 0.117 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 171,275 | 1.713 | 20 | 200 | fits | 155,340 | 226 | 0.327 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 662,572 | 6.626 | 20 | 20 | fits | 142,663 | 97 | 0.591 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 478,998 | 4.790 | 20 | 24 | fits | 160,149 | 118 | 0.510 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 623,097 | 6.231 | 20 | 50 | fits | 142,663 | 97 | 0.591 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 941,657 | 9.417 | 20 | 20 | fits | 40,693 | 25 | 0.798 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 111,573 | 1.116 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 303,973 | 3.040 | 130 | 134 | fits | 81,121 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 321,005 | 3.210 | 130 | 134 | fits | 81,121 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 465,833 | 4.658 | 130 | 134 | fits | 120,363 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 483,404 | 4.834 | 130 | 134 | fits | 120,363 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 564,876 | 5.649 | 130 | 134 | fits | 78,298 | 205 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 582,193 | 5.822 | 130 | 134 | fits | 78,298 | 205 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 1,527,509 | 15.275 | 130 | 134 | fits | 79,140 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 1,545,855 | 15.459 | 130 | 134 | fits | 79,140 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 1,562,166 | 15.622 | 130 | 134 | fits | 79,140 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 1,579,055 | 15.791 | 130 | 134 | fits | 79,140 | 203 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 500,462 | 5.005 | 130 | 134 | fits | 120,363 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 517,965 | 5.180 | 130 | 134 | fits | 120,363 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 1,722,546 | 17.225 | 130 | 134 | fits | 74,884 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 1,739,905 | 17.399 | 130 | 134 | fits | 74,884 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 220,591 | 2.206 | 130 | 134 | fits | 108,620 | 213 | 0.195 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 240,054 | 2.401 | 130 | 134 | fits | 108,620 | 213 | 0.195 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 258,080 | 2.581 | 130 | 134 | fits | 108,620 | 213 | 0.195 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 276,953 | 2.770 | 130 | 134 | fits | 108,620 | 213 | 0.195 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 1,755,570 | 17.556 | 130 | 134 | fits | 74,884 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 1,772,747 | 17.727 | 130 | 134 | fits | 74,884 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 1,911,925 | 19.119 | 130 | 134 | fits | 76,190 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 1,930,032 | 19.300 | 130 | 134 | fits | 76,190 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 1,946,342 | 19.463 | 130 | 134 | fits | 76,190 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 1,964,058 | 19.641 | 130 | 134 | fits | 76,190 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 339,243 | 3.392 | 130 | 134 | fits | 81,121 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 358,987 | 3.590 | 130 | 134 | fits | 81,121 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 599,489 | 5.995 | 130 | 134 | fits | 78,298 | 205 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 618,238 | 6.182 | 130 | 134 | fits | 78,298 | 205 | 0.089 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 2,122,304 | 21.223 | 130 | 134 | fits | 74,054 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 2,139,651 | 21.397 | 130 | 134 | fits | 74,054 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 2,155,578 | 21.556 | 130 | 134 | fits | 74,054 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 2,172,913 | 21.729 | 130 | 134 | fits | 74,054 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,311,999 | 23.120 | 130 | 134 | fits | 73,166 | 203 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 2,329,626 | 23.296 | 130 | 134 | fits | 73,166 | 203 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 2,345,072 | 23.451 | 130 | 134 | fits | 73,166 | 203 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 2,362,182 | 23.622 | 130 | 134 | fits | 73,166 | 203 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 2,514,048 | 25.140 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 2,528,281 | 25.283 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 2,545,359 | 25.454 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 2,562,507 | 25.625 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 529,089 | 5.291 | 20 | 200 | fits | 155,064 | 229 | 0.258 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 645,664 | 6.457 | 20 | 20 | fits | 136,843 | 61 | 0.624 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 333,553 | 3.336 | 20 | 24 | fits | 180,959 | 161 | 0.452 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 469,346 | 4.693 | 20 | 50 | fits | 155,064 | 229 | 0.258 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 836,749 | 8.367 | 20 | 20 | fits | 115,773 | 54 | 0.534 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 587,052 | 5.871 | 130 | 134 | fits | 121,330 | 211 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 604,447 | 6.044 | 130 | 134 | fits | 121,330 | 211 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 686,794 | 6.868 | 130 | 134 | fits | 75,606 | 205 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 704,125 | 7.041 | 130 | 134 | fits | 75,606 | 205 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 1,642,151 | 16.422 | 130 | 134 | fits | 79,159 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 1,660,262 | 16.603 | 130 | 134 | fits | 79,159 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 1,676,572 | 16.766 | 130 | 134 | fits | 79,159 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 1,693,828 | 16.938 | 130 | 134 | fits | 79,159 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 218,921 | 2.189 | 130 | 134 | fits | 86,121 | 205 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 237,110 | 2.371 | 130 | 134 | fits | 86,121 | 205 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 450,326 | 4.503 | 130 | 134 | fits | 78,683 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 468,237 | 4.682 | 130 | 134 | fits | 78,683 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 720,805 | 7.208 | 130 | 134 | fits | 75,606 | 205 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 738,077 | 7.381 | 130 | 134 | fits | 75,606 | 205 | 0.087 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 1,814,912 | 18.149 | 130 | 134 | fits | 76,750 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 1,832,801 | 18.328 | 130 | 134 | fits | 76,750 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 365,566 | 3.656 | 130 | 134 | fits | 108,476 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 385,176 | 3.852 | 130 | 134 | fits | 108,476 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 485,136 | 4.851 | 130 | 134 | fits | 78,683 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 503,699 | 5.037 | 130 | 134 | fits | 78,683 | 205 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 1,849,034 | 18.490 | 130 | 134 | fits | 76,750 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,866,592 | 18.666 | 130 | 134 | fits | 76,750 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 255,726 | 2.557 | 130 | 134 | fits | 86,121 | 205 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 275,910 | 2.759 | 130 | 134 | fits | 86,121 | 205 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 403,554 | 4.036 | 130 | 134 | fits | 108,476 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 423,140 | 4.231 | 130 | 134 | fits | 108,476 | 211 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 621,895 | 6.219 | 130 | 134 | fits | 121,330 | 211 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 640,486 | 6.405 | 130 | 134 | fits | 121,330 | 211 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 2,025,597 | 20.256 | 130 | 134 | fits | 74,145 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 2,043,035 | 20.430 | 130 | 134 | fits | 74,145 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,058,962 | 20.590 | 130 | 134 | fits | 74,145 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,076,297 | 20.763 | 130 | 134 | fits | 74,145 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,236,031 | 22.360 | 130 | 134 | fits | 73,305 | 203 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 2,253,658 | 22.537 | 130 | 134 | fits | 73,305 | 203 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 2,269,104 | 22.691 | 130 | 134 | fits | 73,305 | 203 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 2,286,214 | 22.862 | 130 | 134 | fits | 73,305 | 203 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 2,418,002 | 24.180 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,432,235 | 24.322 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,449,313 | 24.493 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,466,461 | 24.665 | 130 | 134 | fits | 68,692 | 202 | 0.112 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 635,410 | 6.354 | 20 | 200 | fits | 152,760 | 216 | 0.265 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 748,306 | 7.483 | 20 | 20 | fits | 133,164 | 65 | 0.632 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 442,178 | 4.422 | 20 | 24 | fits | 165,038 | 153 | 0.452 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 575,667 | 5.757 | 20 | 50 | fits | 152,760 | 216 | 0.265 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 943,411 | 9.434 | 20 | 20 | fits | 124,105 | 58 | 0.520 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 1,646,656 | 16.467 | 130 | 134 | fits | 79,087 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,664,767 | 16.648 | 130 | 134 | fits | 79,087 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,681,002 | 16.810 | 130 | 134 | fits | 79,087 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,697,970 | 16.980 | 130 | 134 | fits | 79,087 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 217,971 | 2.180 | 130 | 134 | fits | 80,859 | 205 | 0.123 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 235,698 | 2.357 | 130 | 134 | fits | 80,859 | 205 | 0.123 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 252,292 | 2.523 | 130 | 134 | fits | 80,859 | 205 | 0.123 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 269,931 | 2.699 | 130 | 134 | fits | 80,859 | 205 | 0.123 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 462,409 | 4.624 | 130 | 134 | fits | 78,861 | 205 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 479,858 | 4.799 | 130 | 134 | fits | 78,861 | 205 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 1,818,612 | 18.186 | 130 | 134 | fits | 74,912 | 203 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 1,836,054 | 18.361 | 130 | 134 | fits | 74,912 | 203 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 1,852,272 | 18.523 | 130 | 134 | fits | 74,912 | 203 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 1,869,082 | 18.691 | 130 | 134 | fits | 74,912 | 203 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 376,966 | 3.770 | 130 | 134 | fits | 108,735 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 396,125 | 3.961 | 130 | 134 | fits | 108,735 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 497,221 | 4.972 | 130 | 134 | fits | 78,861 | 205 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 515,401 | 5.154 | 130 | 134 | fits | 78,861 | 205 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 599,034 | 5.990 | 130 | 134 | fits | 103,794 | 211 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 617,720 | 6.177 | 130 | 134 | fits | 103,794 | 211 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 682,045 | 6.820 | 130 | 134 | fits | 78,767 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 700,702 | 7.007 | 130 | 134 | fits | 78,767 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 717,719 | 7.177 | 130 | 134 | fits | 78,767 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 736,359 | 7.364 | 130 | 134 | fits | 78,767 | 205 | 0.068 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 2,028,590 | 20.286 | 130 | 134 | fits | 74,273 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 2,046,409 | 20.464 | 130 | 134 | fits | 74,273 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 2,062,273 | 20.623 | 130 | 134 | fits | 74,273 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 2,079,241 | 20.792 | 130 | 134 | fits | 74,273 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 415,183 | 4.152 | 130 | 134 | fits | 108,735 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 435,166 | 4.352 | 130 | 134 | fits | 108,735 | 211 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 635,909 | 6.359 | 130 | 134 | fits | 103,794 | 211 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 655,566 | 6.556 | 130 | 134 | fits | 103,794 | 211 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 2,214,332 | 22.143 | 130 | 134 | fits | 72,911 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 2,231,820 | 22.318 | 130 | 134 | fits | 72,911 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 2,247,266 | 22.473 | 130 | 134 | fits | 72,911 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 2,264,376 | 22.644 | 130 | 134 | fits | 72,911 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,425,931 | 24.259 | 130 | 134 | fits | 69,404 | 202 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,440,220 | 24.402 | 130 | 134 | fits | 69,404 | 202 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,457,521 | 24.575 | 130 | 134 | fits | 69,404 | 202 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,474,669 | 24.747 | 130 | 134 | fits | 69,404 | 202 | 0.132 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 642,184 | 6.422 | 20 | 200 | fits | 152,897 | 216 | 0.269 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 755,531 | 7.555 | 20 | 20 | fits | 133,615 | 65 | 0.633 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 448,815 | 4.488 | 20 | 24 | fits | 184,898 | 166 | 0.449 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 582,441 | 5.824 | 20 | 50 | fits | 152,897 | 216 | 0.269 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 950,794 | 9.508 | 20 | 20 | fits | 123,985 | 58 | 0.516 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 1,604,295 | 16.043 | 130 | 134 | fits | 79,852 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,622,406 | 16.224 | 130 | 134 | fits | 79,852 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 204,671 | 2.047 | 130 | 134 | fits | 105,501 | 213 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 222,539 | 2.225 | 130 | 134 | fits | 105,501 | 213 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 418,165 | 4.182 | 130 | 134 | fits | 78,220 | 203 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 435,722 | 4.357 | 130 | 134 | fits | 78,220 | 203 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 452,225 | 4.522 | 130 | 134 | fits | 78,220 | 203 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 469,633 | 4.696 | 130 | 134 | fits | 78,220 | 203 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 647,206 | 6.472 | 130 | 134 | fits | 74,491 | 205 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 664,424 | 6.644 | 130 | 134 | fits | 74,491 | 205 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 680,487 | 6.805 | 130 | 134 | fits | 74,491 | 205 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 697,528 | 6.975 | 130 | 134 | fits | 74,491 | 205 | 0.067 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 568,243 | 5.682 | 130 | 134 | fits | 101,281 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 586,337 | 5.863 | 130 | 134 | fits | 101,281 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 603,642 | 6.036 | 130 | 134 | fits | 101,281 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 621,581 | 6.216 | 130 | 134 | fits | 101,281 | 211 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 1,639,112 | 16.391 | 130 | 134 | fits | 79,852 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 1,656,447 | 16.564 | 130 | 134 | fits | 79,852 | 203 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 240,137 | 2.401 | 130 | 134 | fits | 105,501 | 213 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 259,162 | 2.592 | 130 | 134 | fits | 105,501 | 213 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 1,712,131 | 17.121 | 130 | 134 | fits | 76,033 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 1,730,232 | 17.302 | 130 | 134 | fits | 76,033 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 1,746,542 | 17.465 | 130 | 134 | fits | 76,033 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 1,764,258 | 17.643 | 130 | 134 | fits | 76,033 | 203 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 1,923,311 | 19.233 | 130 | 134 | fits | 74,403 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 1,941,039 | 19.410 | 130 | 134 | fits | 74,403 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 288,253 | 2.883 | 130 | 134 | fits | 89,038 | 203 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 308,458 | 3.085 | 130 | 134 | fits | 89,038 | 203 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 1,957,134 | 19.571 | 130 | 134 | fits | 74,403 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 1,974,102 | 19.741 | 130 | 134 | fits | 74,403 | 203 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 2,109,479 | 21.095 | 130 | 134 | fits | 73,503 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 2,127,125 | 21.271 | 130 | 134 | fits | 73,503 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 2,142,686 | 21.427 | 130 | 134 | fits | 73,503 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 2,159,796 | 21.598 | 130 | 134 | fits | 73,503 | 203 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 327,424 | 3.274 | 130 | 134 | fits | 89,038 | 203 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 348,309 | 3.483 | 130 | 134 | fits | 89,038 | 203 | 0.065 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 2,321,970 | 23.220 | 130 | 134 | fits | 69,343 | 202 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,336,259 | 23.363 | 130 | 134 | fits | 69,343 | 202 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,353,499 | 23.535 | 130 | 134 | fits | 69,343 | 202 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 2,370,647 | 23.706 | 130 | 134 | fits | 69,343 | 202 | 0.130 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 605,067 | 6.051 | 20 | 200 | fits | 153,930 | 222 | 0.263 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 718,234 | 7.182 | 20 | 20 | fits | 133,435 | 65 | 0.633 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 410,665 | 4.107 | 20 | 24 | fits | 179,274 | 159 | 0.441 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 545,324 | 5.453 | 20 | 50 | fits | 153,930 | 222 | 0.263 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 913,226 | 9.132 | 20 | 20 | fits | 123,891 | 58 | 0.514 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
