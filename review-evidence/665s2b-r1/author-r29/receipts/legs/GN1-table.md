### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 10.582 | fits | 10 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-1.held.adp.if0` (notice-burst-1) | 9.979 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.aecp.if0` (notice-burst-4) | 10.920 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.maap.if0` (notice-burst-5) | 8.655 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-6.held.srp.if0` (notice-burst-6) | 6.943 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 1.004 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-3.notices.29.9.0.if0` (notice-burst-3) | 12.487 (12.709) | fits | 0 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1687 | 0 | 167,054 (1.671) | fits |
| notice-every-1 | 1681 | 0 | 157,097 (1.571) | fits |
| notice-every-2 | 1683 | 0 | 153,268 (1.533) | fits |
| notice-every-3 | 1683 | 0 | 168,216 (1.682) | fits |
| notice-every-4 | 1683 | 0 | 155,672 (1.557) | fits |
| notice-every-5 | 1677 | 0 | 155,601 (1.556) | fits |
| notice-every-6 | 1675 | 0 | 157,234 (1.572) | fits |
| notice-every-7 | 1673 | 0 | 167,054 (1.671) | fits |
| notice-burst-0 | 980 | 0 | 152,953 (1.530) | fits |
| notice-burst-1 | 937 | 0 | 154,686 (1.547) | fits |
| notice-burst-2 | 933 | 0 | 153,375 (1.534) | fits |
| notice-burst-3 | 920 | 0 | 147,579 (1.476) | fits |
| notice-burst-4 | 930 | 0 | 151,180 (1.512) | fits |
| notice-burst-5 | 936 | 0 | 153,196 (1.532) | fits |
| notice-burst-6 | 909 | 0 | 148,736 (1.487) | fits |
| notice-burst-7 | 933 | 0 | 152,107 (1.521) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.396 | 22 | 16 | 2 | within |
| notice-every-0 | 4.598 | 22 | 16 | 2 | within |
| notice-every-0 | 6.345 | 22 | 16 | 2 | within |
| notice-every-0 | 6.549 | 22 | 16 | 2 | within |
| notice-every-0 | 8.260 | 22 | 16 | 2 | within |
| notice-every-0 | 8.461 | 22 | 16 | 2 | within |
| notice-every-0 | 3.122 | 22 | 16 | 2 | within |
| notice-every-0 | 3.333 | 22 | 16 | 2 | within |
| notice-every-0 | 4.787 | 22 | 16 | 2 | within |
| notice-every-0 | 4.956 | 22 | 16 | 2 | within |
| notice-every-0 | 3.544 | 22 | 16 | 2 | within |
| notice-every-0 | 3.756 | 22 | 16 | 2 | within |
| notice-every-1 | 2.171 | 22 | 16 | 2 | within |
| notice-every-1 | 2.374 | 22 | 16 | 2 | within |
| notice-every-1 | 4.620 | 22 | 16 | 2 | within |
| notice-every-1 | 4.825 | 22 | 16 | 2 | within |
| notice-every-1 | 6.326 | 22 | 16 | 2 | within |
| notice-every-1 | 6.528 | 22 | 16 | 2 | within |
| notice-every-1 | 8.265 | 22 | 16 | 2 | within |
| notice-every-1 | 8.466 | 22 | 16 | 2 | within |
| notice-every-1 | 2.563 | 22 | 16 | 2 | within |
| notice-every-1 | 2.736 | 22 | 16 | 2 | within |
| notice-every-1 | 2.939 | 22 | 16 | 2 | within |
| notice-every-1 | 3.149 | 22 | 16 | 2 | within |
| notice-every-2 | 6.232 | 22 | 16 | 2 | within |
| notice-every-2 | 6.435 | 22 | 16 | 2 | within |
| notice-every-2 | 8.292 | 22 | 16 | 2 | within |
| notice-every-2 | 8.496 | 22 | 16 | 2 | within |
| notice-every-2 | 2.160 | 22 | 16 | 2 | within |
| notice-every-2 | 2.368 | 22 | 16 | 2 | within |
| notice-every-2 | 4.240 | 22 | 16 | 2 | within |
| notice-every-2 | 4.449 | 22 | 16 | 2 | within |
| notice-every-2 | 6.621 | 22 | 16 | 2 | within |
| notice-every-2 | 6.789 | 22 | 16 | 2 | within |
| notice-every-2 | 2.580 | 22 | 16 | 2 | within |
| notice-every-2 | 2.792 | 22 | 16 | 2 | within |
| notice-every-3 | 8.258 | 22 | 16 | 2 | within |
| notice-every-3 | 8.460 | 22 | 16 | 2 | within |
| notice-every-3 | 3.048 | 22 | 16 | 2 | within |
| notice-every-3 | 3.258 | 22 | 16 | 2 | within |
| notice-every-3 | 4.316 | 22 | 16 | 2 | within |
| notice-every-3 | 4.521 | 22 | 16 | 2 | within |
| notice-every-3 | 6.288 | 22 | 16 | 2 | within |
| notice-every-3 | 6.492 | 22 | 16 | 2 | within |
| notice-every-3 | 8.645 | 22 | 16 | 2 | within |
| notice-every-3 | 8.810 | 22 | 16 | 2 | within |
| notice-every-3 | 3.472 | 22 | 16 | 2 | within |
| notice-every-3 | 3.684 | 22 | 16 | 2 | within |
| notice-every-4 | 6.371 | 22 | 16 | 2 | within |
| notice-every-4 | 6.574 | 22 | 16 | 2 | within |
| notice-every-4 | 8.275 | 22 | 16 | 2 | within |
| notice-every-4 | 8.479 | 22 | 16 | 2 | within |
| notice-every-4 | 2.298 | 22 | 16 | 2 | within |
| notice-every-4 | 2.506 | 22 | 16 | 2 | within |
| notice-every-4 | 4.380 | 22 | 16 | 2 | within |
| notice-every-4 | 4.589 | 22 | 16 | 2 | within |
| notice-every-4 | 6.760 | 22 | 16 | 2 | within |
| notice-every-4 | 6.928 | 22 | 16 | 2 | within |
| notice-every-4 | 2.718 | 22 | 16 | 2 | within |
| notice-every-4 | 2.930 | 22 | 16 | 2 | within |
| notice-every-5 | 8.226 | 22 | 16 | 2 | within |
| notice-every-5 | 8.428 | 22 | 16 | 2 | within |
| notice-every-5 | 2.227 | 22 | 16 | 2 | within |
| notice-every-5 | 2.437 | 22 | 16 | 2 | within |
| notice-every-5 | 4.313 | 22 | 16 | 2 | within |
| notice-every-5 | 4.520 | 22 | 16 | 2 | within |
| notice-every-5 | 6.287 | 22 | 16 | 2 | within |
| notice-every-5 | 6.491 | 22 | 16 | 2 | within |
| notice-every-5 | 8.613 | 22 | 16 | 2 | within |
| notice-every-5 | 8.778 | 22 | 16 | 2 | within |
| notice-every-5 | 2.650 | 22 | 16 | 2 | within |
| notice-every-5 | 2.862 | 22 | 16 | 2 | within |
| notice-every-6 | 2.170 | 22 | 16 | 2 | within |
| notice-every-6 | 2.374 | 22 | 16 | 2 | within |
| notice-every-6 | 4.618 | 22 | 16 | 2 | within |
| notice-every-6 | 4.823 | 22 | 16 | 2 | within |
| notice-every-6 | 6.164 | 22 | 16 | 2 | within |
| notice-every-6 | 6.366 | 22 | 16 | 2 | within |
| notice-every-6 | 8.240 | 22 | 16 | 2 | within |
| notice-every-6 | 8.441 | 22 | 16 | 2 | within |
| notice-every-6 | 2.562 | 22 | 16 | 2 | within |
| notice-every-6 | 2.734 | 22 | 16 | 2 | within |
| notice-every-6 | 2.937 | 22 | 16 | 2 | within |
| notice-every-6 | 3.148 | 22 | 16 | 2 | within |
| notice-every-7 | 4.393 | 22 | 16 | 2 | within |
| notice-every-7 | 4.595 | 22 | 16 | 2 | within |
| notice-every-7 | 6.342 | 22 | 16 | 2 | within |
| notice-every-7 | 6.547 | 22 | 16 | 2 | within |
| notice-every-7 | 8.257 | 22 | 16 | 2 | within |
| notice-every-7 | 8.458 | 22 | 16 | 2 | within |
| notice-every-7 | 3.119 | 22 | 16 | 2 | within |
| notice-every-7 | 3.330 | 22 | 16 | 2 | within |
| notice-every-7 | 4.784 | 22 | 16 | 2 | within |
| notice-every-7 | 4.953 | 22 | 16 | 2 | within |
| notice-every-7 | 3.541 | 22 | 16 | 2 | within |
| notice-every-7 | 3.753 | 22 | 16 | 2 | within |
| notice-burst-0 | 9.298 | 22 | 16 | 0 | within |
| notice-burst-0 | 9.505 | 22 | 16 | 0 | within |
| notice-burst-0 | 9.709 | 22 | 16 | 0 | within |
| notice-burst-0 | 9.913 | 22 | 16 | 0 | within |
| notice-burst-0 | 2.366 | 22 | 16 | 0 | within |
| notice-burst-0 | 2.573 | 22 | 16 | 0 | within |
| notice-burst-0 | 3.302 | 22 | 16 | 0 | within |
| notice-burst-0 | 3.508 | 22 | 16 | 0 | within |
| notice-burst-0 | 10.098 | 22 | 16 | 0 | within |
| notice-burst-0 | 10.264 | 22 | 16 | 0 | within |
| notice-burst-0 | 10.461 | 22 | 16 | 0 | within |
| notice-burst-0 | 4.073 | 22 | 16 | 0 | within |
| notice-burst-1 | 8.622 | 22 | 16 | 2 | within |
| notice-burst-1 | 8.830 | 22 | 16 | 2 | within |
| notice-burst-1 | 10.656 | 22 | 16 | 2 | within |
| notice-burst-1 | 10.864 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.164 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.371 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.568 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.772 | 22 | 16 | 2 | within |
| notice-burst-1 | 9.017 | 22 | 16 | 2 | within |
| notice-burst-1 | 9.186 | 22 | 16 | 2 | within |
| notice-burst-1 | 9.385 | 22 | 16 | 2 | within |
| notice-burst-1 | 4.238 | 22 | 16 | 2 | within |
| notice-burst-2 | 8.625 | 22 | 16 | 0 | within |
| notice-burst-2 | 8.834 | 22 | 16 | 0 | within |
| notice-burst-2 | 1.943 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.151 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.347 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.548 | 22 | 16 | 0 | within |
| notice-burst-2 | 4.355 | 22 | 16 | 0 | within |
| notice-burst-2 | 4.560 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.018 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.184 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.381 | 22 | 16 | 0 | within |
| notice-burst-2 | 4.769 | 22 | 16 | 0 | within |
| notice-burst-3 | 9.379 | 22 | 16 | 0 | within |
| notice-burst-3 | 9.585 | 22 | 16 | 0 | within |
| notice-burst-3 | 9.792 | 22 | 16 | 0 | within |
| notice-burst-3 | 9.995 | 22 | 16 | 0 | within |
| notice-burst-3 | 10.187 | 22 | 16 | 0 | within |
| notice-burst-3 | 10.386 | 22 | 16 | 0 | within |
| notice-burst-3 | 2.080 | 22 | 16 | 0 | within |
| notice-burst-3 | 2.289 | 22 | 16 | 0 | within |
| notice-burst-3 | 10.570 | 22 | 16 | 0 | within |
| notice-burst-3 | 12.287 | 22 | 16 | 0 | within |
| notice-burst-3 | 12.487 | 22 | 16 | 0 | within |
| notice-burst-3 | 4.062 | 22 | 16 | 0 | within |
| notice-burst-4 | 8.961 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.167 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.373 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.576 | 22 | 16 | 1 | within |
| notice-burst-4 | 2.638 | 22 | 16 | 1 | within |
| notice-burst-4 | 2.845 | 22 | 16 | 1 | within |
| notice-burst-4 | 3.042 | 22 | 16 | 1 | within |
| notice-burst-4 | 3.245 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.761 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.928 | 22 | 16 | 1 | within |
| notice-burst-4 | 10.124 | 22 | 16 | 1 | within |
| notice-burst-4 | 5.035 | 22 | 16 | 1 | within |
| notice-burst-5 | 7.632 | 22 | 16 | 1 | within |
| notice-burst-5 | 7.835 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.039 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.242 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.434 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.635 | 22 | 16 | 1 | within |
| notice-burst-5 | 10.607 | 22 | 16 | 1 | within |
| notice-burst-5 | 10.815 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.822 | 22 | 16 | 1 | within |
| notice-burst-5 | 10.996 | 22 | 16 | 1 | within |
| notice-burst-5 | 11.191 | 22 | 16 | 1 | within |
| notice-burst-5 | 11.393 | 22 | 16 | 1 | within |
| notice-burst-6 | 7.454 | 22 | 16 | 0 | within |
| notice-burst-6 | 7.657 | 22 | 16 | 0 | within |
| notice-burst-6 | 7.861 | 22 | 16 | 0 | within |
| notice-burst-6 | 8.064 | 22 | 16 | 0 | within |
| notice-burst-6 | 10.407 | 22 | 16 | 0 | within |
| notice-burst-6 | 10.613 | 22 | 16 | 0 | within |
| notice-burst-6 | 10.805 | 22 | 16 | 0 | within |
| notice-burst-6 | 11.005 | 22 | 16 | 0 | within |
| notice-burst-6 | 8.253 | 22 | 16 | 0 | within |
| notice-burst-6 | 8.425 | 22 | 16 | 0 | within |
| notice-burst-6 | 8.626 | 22 | 16 | 0 | within |
| notice-burst-6 | 11.207 | 22 | 16 | 0 | within |
| notice-burst-7 | 9.033 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.240 | 22 | 16 | 1 | within |
| notice-burst-7 | 11.411 | 22 | 16 | 1 | within |
| notice-burst-7 | 11.618 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.146 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.352 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.548 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.752 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.427 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.596 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.795 | 22 | 16 | 1 | within |
| notice-burst-7 | 3.251 | 22 | 16 | 1 | within |

Latest: 12.487 ms, notice-burst-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 306 | 167,054 (1.671) | 76,427 (0.764) |
| notice-every-1 | 306 | 101,188 (1.012) | 76,434 (0.764) |
| notice-every-2 | 306 | 102,575 (1.026) | 76,184 (0.762) |
| notice-every-3 | 306 | 168,216 (1.682) | 76,239 (0.762) |
| notice-every-4 | 306 | 88,012 (0.880) | 76,184 (0.762) |
| notice-every-5 | 306 | 88,012 (0.880) | 76,184 (0.762) |
| notice-every-6 | 306 | 88,012 (0.880) | 76,184 (0.762) |
| notice-every-7 | 306 | 167,054 (1.671) | 76,239 (0.762) |
| notice-burst-0 | 316 | 108,088 (1.081) | 78,599 (0.786) |
| notice-burst-1 | 316 | 101,188 (1.012) | 78,599 (0.786) |
| notice-burst-2 | 316 | 102,575 (1.026) | 78,599 (0.786) |
| notice-burst-3 | 316 | 96,109 (0.961) | 78,599 (0.786) |
| notice-burst-4 | 316 | 96,136 (0.961) | 78,599 (0.786) |
| notice-burst-5 | 316 | 98,944 (0.989) | 78,599 (0.786) |
| notice-burst-6 | 316 | 94,577 (0.946) | 78,599 (0.786) |
| notice-burst-7 | 316 | 97,650 (0.977) | 78,497 (0.785) |

Longest pass that carries a step: 168,216 CPU cycles (1.682 ms), notice-every-3; longest step: 78,599 (0.786 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 439,583 | 4.396 | 22 | 26 | fits | 83,264 | 201 | 0.217 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 459,798 | 4.598 | 22 | 26 | fits | 83,264 | 201 | 0.217 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 634,452 | 6.345 | 22 | 26 | fits | 47,580 | 103 | 0.286 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 654,925 | 6.549 | 22 | 26 | fits | 47,580 | 103 | 0.286 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 825,955 | 8.260 | 22 | 26 | fits | 45,488 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 846,076 | 8.461 | 22 | 26 | fits | 45,488 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 312,189 | 3.122 | 22 | 26 | fits | 167,054 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 333,292 | 3.333 | 22 | 26 | fits | 167,054 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 478,687 | 4.787 | 22 | 26 | fits | 83,264 | 201 | 0.217 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 495,647 | 4.956 | 22 | 26 | fits | 83,264 | 201 | 0.217 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 354,408 | 3.544 | 22 | 26 | fits | 167,054 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 375,617 | 3.756 | 22 | 26 | fits | 167,054 | 204 | 0.206 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 710,757 | 7.108 | 20 | 200 | fits | 160,206 | 198 | 0.522 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 847,686 | 8.477 | 20 | 20 | fits | 144,104 | 122 | 0.496 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 859,472 | 8.595 | 20 | 24 | fits | 31,990 | 30 | 0.678 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 651,014 | 6.510 | 20 | 50 | fits | 160,206 | 198 | 0.522 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 450,979 | 4.510 | 20 | 20 | fits | 88,217 | 44 | 0.503 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 85,269 | 0.853 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 217,074 | 2.171 | 22 | 26 | fits | 126,793 | 305 | 0.199 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 237,431 | 2.374 | 22 | 26 | fits | 126,793 | 305 | 0.199 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 461,997 | 4.620 | 22 | 26 | fits | 48,890 | 102 | 0.315 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 482,513 | 4.825 | 22 | 26 | fits | 48,890 | 102 | 0.315 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 632,565 | 6.326 | 22 | 26 | fits | 46,147 | 103 | 0.294 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 652,757 | 6.528 | 22 | 26 | fits | 46,147 | 103 | 0.294 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 826,461 | 8.265 | 22 | 26 | fits | 45,275 | 102 | 0.272 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 846,582 | 8.466 | 22 | 26 | fits | 45,275 | 102 | 0.272 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 256,287 | 2.563 | 22 | 26 | fits | 126,793 | 305 | 0.199 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 273,551 | 2.736 | 22 | 26 | fits | 126,793 | 305 | 0.199 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 293,859 | 2.939 | 22 | 26 | fits | 126,793 | 305 | 0.199 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 314,916 | 3.149 | 22 | 26 | fits | 126,793 | 305 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 694,069 | 6.941 | 20 | 200 | fits | 148,682 | 168 | 0.531 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 848,672 | 8.487 | 20 | 20 | fits | 157,097 | 136 | 0.511 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 875,285 | 8.753 | 20 | 24 | fits | 33,705 | 37 | 0.674 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 634,326 | 6.343 | 20 | 50 | fits | 148,682 | 168 | 0.531 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 463,619 | 4.636 | 20 | 20 | fits | 88,220 | 42 | 0.507 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 100,447 | 1.004 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 623,153 | 6.232 | 22 | 26 | fits | 82,684 | 202 | 0.220 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 643,475 | 6.435 | 22 | 26 | fits | 82,684 | 202 | 0.220 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 829,172 | 8.292 | 22 | 26 | fits | 47,163 | 102 | 0.282 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 849,574 | 8.496 | 22 | 26 | fits | 47,163 | 102 | 0.282 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 215,970 | 2.160 | 22 | 26 | fits | 91,138 | 204 | 0.232 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 236,789 | 2.368 | 22 | 26 | fits | 91,138 | 204 | 0.232 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 423,998 | 4.240 | 22 | 26 | fits | 48,369 | 102 | 0.295 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 444,856 | 4.449 | 22 | 26 | fits | 48,369 | 102 | 0.295 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 662,062 | 6.621 | 22 | 26 | fits | 82,684 | 202 | 0.220 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 678,862 | 6.789 | 22 | 26 | fits | 82,684 | 202 | 0.220 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 258,040 | 2.580 | 22 | 26 | fits | 91,138 | 204 | 0.232 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 279,249 | 2.792 | 22 | 26 | fits | 91,138 | 204 | 0.232 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 149,856 | 1.499 | 20 | 200 | fits | 145,196 | 181 | 0.506 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 853,677 | 8.537 | 20 | 20 | fits | 153,056 | 125 | 0.513 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 879,974 | 8.800 | 20 | 24 | fits | 46,501 | 38 | 0.590 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 643,589 | 6.436 | 20 | 50 | fits | 151,448 | 181 | 0.544 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 457,346 | 4.573 | 20 | 20 | fits | 88,565 | 43 | 0.508 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 93,273 | 0.933 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 825,792 | 8.258 | 22 | 26 | fits | 81,479 | 201 | 0.215 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 846,043 | 8.460 | 22 | 26 | fits | 81,479 | 201 | 0.215 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 304,823 | 3.048 | 22 | 26 | fits | 168,216 | 204 | 0.214 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 325,845 | 3.258 | 22 | 26 | fits | 168,216 | 204 | 0.214 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 431,636 | 4.316 | 22 | 26 | fits | 47,467 | 102 | 0.295 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 452,118 | 4.521 | 22 | 26 | fits | 47,467 | 102 | 0.295 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 628,822 | 6.288 | 22 | 26 | fits | 46,578 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 649,245 | 6.492 | 22 | 26 | fits | 46,578 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 864,453 | 8.645 | 22 | 26 | fits | 81,479 | 201 | 0.215 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 880,951 | 8.810 | 22 | 26 | fits | 81,479 | 201 | 0.215 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 347,175 | 3.472 | 22 | 26 | fits | 168,216 | 204 | 0.214 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 368,384 | 3.684 | 22 | 26 | fits | 168,216 | 204 | 0.214 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 149,654 | 1.497 | 20 | 200 | fits | 148,668 | 173 | 0.507 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 850,920 | 8.509 | 20 | 20 | fits | 144,061 | 130 | 0.524 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 877,318 | 8.773 | 20 | 24 | fits | 46,602 | 38 | 0.589 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 811,445 | 8.114 | 20 | 50 | fits | 144,061 | 130 | 0.524 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 462,859 | 4.629 | 20 | 20 | fits | 88,539 | 43 | 0.507 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 81,761 | 0.818 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 637,107 | 6.371 | 22 | 26 | fits | 82,550 | 202 | 0.217 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 657,429 | 6.574 | 22 | 26 | fits | 82,550 | 202 | 0.217 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 827,498 | 8.275 | 22 | 26 | fits | 47,252 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 847,900 | 8.479 | 22 | 26 | fits | 47,252 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 229,763 | 2.298 | 22 | 26 | fits | 91,138 | 204 | 0.232 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 250,582 | 2.506 | 22 | 26 | fits | 91,138 | 204 | 0.232 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 438,016 | 4.380 | 22 | 26 | fits | 48,369 | 102 | 0.295 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 458,874 | 4.589 | 22 | 26 | fits | 48,369 | 102 | 0.295 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 675,964 | 6.760 | 22 | 26 | fits | 82,550 | 202 | 0.217 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 692,764 | 6.928 | 22 | 26 | fits | 82,550 | 202 | 0.217 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 271,833 | 2.718 | 22 | 26 | fits | 91,138 | 204 | 0.232 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 293,042 | 2.930 | 22 | 26 | fits | 91,138 | 204 | 0.232 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 717,056 | 7.171 | 20 | 200 | fits | 144,179 | 181 | 0.535 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 853,019 | 8.530 | 20 | 20 | fits | 143,238 | 117 | 0.499 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 879,155 | 8.792 | 20 | 24 | fits | 46,340 | 38 | 0.586 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 657,313 | 6.573 | 20 | 50 | fits | 144,179 | 181 | 0.535 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 478,268 | 4.783 | 20 | 20 | fits | 89,569 | 49 | 0.498 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 83,831 | 0.838 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 822,567 | 8.226 | 22 | 26 | fits | 81,613 | 201 | 0.218 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 842,818 | 8.428 | 22 | 26 | fits | 81,613 | 201 | 0.218 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 222,696 | 2.227 | 22 | 26 | fits | 92,856 | 204 | 0.242 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 243,665 | 2.437 | 22 | 26 | fits | 92,856 | 204 | 0.242 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 431,330 | 4.313 | 22 | 26 | fits | 48,107 | 102 | 0.309 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 451,957 | 4.520 | 22 | 26 | fits | 48,107 | 102 | 0.309 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 628,665 | 6.287 | 22 | 26 | fits | 46,649 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 649,088 | 6.491 | 22 | 26 | fits | 46,649 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 861,280 | 8.613 | 22 | 26 | fits | 81,613 | 201 | 0.218 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 877,778 | 8.778 | 22 | 26 | fits | 81,613 | 201 | 0.218 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 265,017 | 2.650 | 22 | 26 | fits | 92,856 | 204 | 0.242 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 286,226 | 2.862 | 22 | 26 | fits | 92,856 | 204 | 0.242 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 701,097 | 7.011 | 20 | 200 | fits | 144,214 | 183 | 0.540 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 838,708 | 8.387 | 20 | 20 | fits | 144,926 | 113 | 0.536 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 879,992 | 8.800 | 20 | 24 | fits | 61,488 | 48 | 0.537 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 641,354 | 6.414 | 20 | 50 | fits | 144,214 | 183 | 0.540 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 462,043 | 4.620 | 20 | 20 | fits | 88,744 | 45 | 0.508 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 83,803 | 0.838 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 217,013 | 2.170 | 22 | 26 | fits | 126,568 | 303 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 237,370 | 2.374 | 22 | 26 | fits | 126,568 | 303 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 461,780 | 4.618 | 22 | 26 | fits | 48,851 | 102 | 0.313 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 482,296 | 4.823 | 22 | 26 | fits | 48,851 | 102 | 0.313 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 616,402 | 6.164 | 22 | 26 | fits | 46,229 | 103 | 0.296 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 636,594 | 6.366 | 22 | 26 | fits | 46,229 | 103 | 0.296 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 823,955 | 8.240 | 22 | 26 | fits | 45,193 | 102 | 0.270 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 844,076 | 8.441 | 22 | 26 | fits | 45,193 | 102 | 0.270 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 256,174 | 2.562 | 22 | 26 | fits | 126,568 | 303 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 273,438 | 2.734 | 22 | 26 | fits | 126,568 | 303 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 293,746 | 2.937 | 22 | 26 | fits | 126,568 | 303 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 314,803 | 3.148 | 22 | 26 | fits | 126,568 | 303 | 0.197 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 148,537 | 1.485 | 20 | 200 | fits | 150,120 | 186 | 0.495 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 849,986 | 8.500 | 20 | 20 | fits | 144,881 | 114 | 0.533 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 875,989 | 8.760 | 20 | 24 | fits | 46,207 | 36 | 0.588 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 652,761 | 6.528 | 20 | 50 | fits | 157,234 | 189 | 0.528 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 460,430 | 4.604 | 20 | 20 | fits | 88,819 | 45 | 0.510 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 93,243 | 0.932 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 439,259 | 4.393 | 22 | 26 | fits | 83,264 | 201 | 0.217 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 459,474 | 4.595 | 22 | 26 | fits | 83,264 | 201 | 0.217 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 634,226 | 6.342 | 22 | 26 | fits | 47,580 | 103 | 0.286 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 654,699 | 6.547 | 22 | 26 | fits | 47,580 | 103 | 0.286 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 825,653 | 8.257 | 22 | 26 | fits | 45,488 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 845,774 | 8.458 | 22 | 26 | fits | 45,488 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 311,902 | 3.119 | 22 | 26 | fits | 167,054 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 333,005 | 3.330 | 22 | 26 | fits | 167,054 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 478,363 | 4.784 | 22 | 26 | fits | 83,264 | 201 | 0.217 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 495,323 | 4.953 | 22 | 26 | fits | 83,264 | 201 | 0.217 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 354,121 | 3.541 | 22 | 26 | fits | 167,054 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 375,330 | 3.753 | 22 | 26 | fits | 167,054 | 204 | 0.206 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 734,220 | 7.342 | 20 | 200 | fits | 147,834 | 191 | 0.536 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 879,087 | 8.791 | 20 | 20 | fits | 151,858 | 123 | 0.508 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 904,077 | 9.041 | 20 | 24 | fits | 32,220 | 31 | 0.683 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 674,477 | 6.745 | 20 | 50 | fits | 147,834 | 191 | 0.536 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 487,611 | 4.876 | 20 | 20 | fits | 89,591 | 51 | 0.495 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 89,191 | 0.892 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 929,813 | 9.298 | 22 | 26 | fits | 145,466 | 353 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 950,536 | 9.505 | 22 | 26 | fits | 145,466 | 353 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 970,935 | 9.709 | 22 | 26 | fits | 145,466 | 353 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 991,262 | 9.913 | 22 | 26 | fits | 145,466 | 353 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 236,650 | 2.366 | 22 | 26 | fits | 48,513 | 102 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 257,267 | 2.573 | 22 | 26 | fits | 48,513 | 102 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 330,164 | 3.302 | 22 | 26 | fits | 58,652 | 111 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 350,818 | 3.508 | 22 | 26 | fits | 58,652 | 111 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,009,806 | 10.098 | 22 | 26 | fits | 145,466 | 353 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,026,426 | 10.264 | 22 | 26 | fits | 145,466 | 353 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,046,112 | 10.461 | 22 | 26 | fits | 145,466 | 353 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 407,274 | 4.073 | 22 | 26 | fits | 37,859 | 61 | 0.366 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 157,735 | 1.577 | 20 | 200 | fits | 152,953 | 186 | 0.506 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 936,472 | 9.365 | 20 | 20 | fits | 143,821 | 112 | 0.498 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 960,672 | 9.607 | 20 | 24 | fits | 44,404 | 35 | 0.594 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 753,176 | 7.532 | 20 | 50 | fits | 147,989 | 172 | 0.565 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 583,162 | 5.832 | 20 | 20 | fits | 95,429 | 57 | 0.583 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 862,227 | 8.622 | 22 | 26 | fits | 105,921 | 252 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 882,972 | 8.830 | 22 | 26 | fits | 105,921 | 252 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,065,586 | 10.656 | 22 | 26 | fits | 49,366 | 103 | 0.345 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,086,362 | 10.864 | 22 | 26 | fits | 49,366 | 103 | 0.345 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 216,432 | 2.164 | 22 | 26 | fits | 98,957 | 212 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 237,063 | 2.371 | 22 | 26 | fits | 98,957 | 212 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 256,816 | 2.568 | 22 | 26 | fits | 98,957 | 212 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 277,199 | 2.772 | 22 | 26 | fits | 98,957 | 212 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 901,715 | 9.017 | 22 | 26 | fits | 105,921 | 252 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 918,637 | 9.186 | 22 | 26 | fits | 105,921 | 252 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 938,483 | 9.385 | 22 | 26 | fits | 105,921 | 252 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 423,791 | 4.238 | 22 | 26 | fits | 38,394 | 61 | 0.387 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 997,899 | 9.979 | 20 | 200 | fits | 154,686 | 120 | 0.513 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 977,631 | 9.776 | 20 | 20 | fits | 154,686 | 120 | 0.513 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 987,498 | 9.875 | 20 | 24 | fits | 30,071 | 23 | 0.709 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 783,470 | 7.835 | 20 | 50 | fits | 149,028 | 172 | 0.556 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 563,051 | 5.631 | 20 | 20 | fits | 98,111 | 66 | 0.574 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 862,546 | 8.625 | 22 | 26 | fits | 104,308 | 253 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 883,377 | 8.834 | 22 | 26 | fits | 104,308 | 253 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 194,319 | 1.943 | 22 | 26 | fits | 100,162 | 212 | 0.253 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 215,089 | 2.151 | 22 | 26 | fits | 100,162 | 212 | 0.253 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 234,669 | 2.347 | 22 | 26 | fits | 100,162 | 212 | 0.253 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 254,821 | 2.548 | 22 | 26 | fits | 100,162 | 212 | 0.253 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 435,518 | 4.355 | 22 | 26 | fits | 68,875 | 153 | 0.268 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 456,003 | 4.560 | 22 | 26 | fits | 68,875 | 153 | 0.268 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 901,799 | 9.018 | 22 | 26 | fits | 104,308 | 253 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 918,419 | 9.184 | 22 | 26 | fits | 104,308 | 253 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 938,105 | 9.381 | 22 | 26 | fits | 104,308 | 253 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 476,866 | 4.769 | 22 | 26 | fits | 68,875 | 153 | 0.268 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 147,939 | 1.479 | 20 | 200 | fits | 152,304 | 190 | 0.503 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 960,624 | 9.606 | 20 | 20 | fits | 153,375 | 119 | 0.510 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 984,963 | 9.850 | 20 | 24 | fits | 44,543 | 35 | 0.594 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 767,774 | 7.678 | 20 | 50 | fits | 150,607 | 187 | 0.559 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 490,834 | 4.908 | 20 | 20 | fits | 87,660 | 44 | 0.507 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 937,933 | 9.379 | 22 | 26 | fits | 147,579 | 353 | 0.220 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 958,492 | 9.585 | 22 | 26 | fits | 147,579 | 353 | 0.220 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 979,205 | 9.792 | 22 | 26 | fits | 147,579 | 353 | 0.220 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 999,461 | 9.995 | 22 | 26 | fits | 147,579 | 353 | 0.220 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,018,697 | 10.187 | 22 | 26 | fits | 147,579 | 353 | 0.220 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,038,633 | 10.386 | 22 | 26 | fits | 147,579 | 353 | 0.220 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 208,026 | 2.080 | 22 | 26 | fits | 59,720 | 111 | 0.319 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 228,871 | 2.289 | 22 | 26 | fits | 59,720 | 111 | 0.319 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,056,954 | 10.570 | 22 | 26 | fits | 147,579 | 353 | 0.220 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,228,670 | 12.287 | 22 | 26 | fits | 43,995 | 102 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,248,675 | 12.487 | 22 | 26 | fits | 43,995 | 102 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 406,160 | 4.062 | 22 | 26 | fits | 29,915 | 53 | 0.426 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 730,939 | 7.309 | 20 | 200 | fits | 147,431 | 169 | 0.530 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 1,005,531 | 10.055 | 20 | 20 | fits | 147,281 | 128 | 0.543 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 1,076,831 | 10.768 | 20 | 24 | fits | 47,509 | 44 | 0.603 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 671,196 | 6.712 | 20 | 50 | fits | 147,431 | 169 | 0.530 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 501,740 | 5.017 | 20 | 20 | fits | 87,757 | 42 | 0.508 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 896,149 | 8.961 | 22 | 26 | fits | 144,559 | 352 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 916,695 | 9.167 | 22 | 26 | fits | 144,559 | 352 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 937,260 | 9.373 | 22 | 26 | fits | 144,559 | 352 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 957,587 | 9.576 | 22 | 26 | fits | 144,559 | 352 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 263,757 | 2.638 | 22 | 26 | fits | 89,391 | 202 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 284,532 | 2.845 | 22 | 26 | fits | 89,391 | 202 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 304,186 | 3.042 | 22 | 26 | fits | 89,391 | 202 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 324,498 | 3.245 | 22 | 26 | fits | 89,391 | 202 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 976,060 | 9.761 | 22 | 26 | fits | 144,559 | 352 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 992,751 | 9.928 | 22 | 26 | fits | 144,559 | 352 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,012,366 | 10.124 | 22 | 26 | fits | 144,559 | 352 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 503,483 | 5.035 | 22 | 26 | fits | 30,214 | 53 | 0.441 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 151,819 | 1.518 | 20 | 200 | fits | 151,180 | 191 | 0.499 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 1,052,640 | 10.526 | 20 | 20 | fits | 145,748 | 123 | 0.537 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 1,091,957 | 10.920 | 20 | 24 | fits | 59,521 | 47 | 0.538 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 722,858 | 7.229 | 20 | 50 | fits | 148,018 | 175 | 0.559 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 552,815 | 5.528 | 20 | 20 | fits | 88,174 | 42 | 0.520 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 763,162 | 7.632 | 22 | 26 | fits | 147,861 | 353 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 783,511 | 7.835 | 22 | 26 | fits | 147,861 | 353 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 803,853 | 8.039 | 22 | 26 | fits | 147,861 | 353 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 824,151 | 8.242 | 22 | 26 | fits | 147,861 | 353 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 843,406 | 8.434 | 22 | 26 | fits | 147,861 | 353 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 863,522 | 8.635 | 22 | 26 | fits | 147,861 | 353 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,060,734 | 10.607 | 22 | 26 | fits | 106,384 | 253 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,081,511 | 10.815 | 22 | 26 | fits | 106,384 | 253 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 882,202 | 8.822 | 22 | 26 | fits | 147,861 | 353 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 1,099,561 | 10.996 | 22 | 26 | fits | 106,384 | 253 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 1,119,122 | 11.191 | 22 | 26 | fits | 106,384 | 253 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 1,139,292 | 11.393 | 22 | 26 | fits | 106,384 | 253 | 0.240 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 147,039 | 1.470 | 20 | 200 | fits | 149,145 | 183 | 0.493 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 1,058,209 | 10.582 | 20 | 20 | fits | 153,196 | 118 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 1,067,774 | 10.678 | 20 | 24 | fits | 29,769 | 23 | 0.699 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 865,538 | 8.655 | 20 | 50 | fits | 152,618 | 175 | 0.535 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 690,895 | 6.909 | 20 | 20 | fits | 93,031 | 48 | 0.546 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 745,400 | 7.454 | 22 | 26 | fits | 146,835 | 352 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 765,742 | 7.657 | 22 | 26 | fits | 146,835 | 352 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 786,084 | 7.861 | 22 | 26 | fits | 146,835 | 352 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 806,382 | 8.064 | 22 | 26 | fits | 146,835 | 352 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,040,698 | 10.407 | 22 | 26 | fits | 108,205 | 253 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,061,324 | 10.613 | 22 | 26 | fits | 108,205 | 253 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,080,542 | 10.805 | 22 | 26 | fits | 108,205 | 253 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 1,100,478 | 11.005 | 22 | 26 | fits | 108,205 | 253 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 825,320 | 8.253 | 22 | 26 | fits | 146,835 | 352 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 842,481 | 8.425 | 22 | 26 | fits | 146,835 | 352 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 862,629 | 8.626 | 22 | 26 | fits | 146,835 | 352 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 1,120,738 | 11.207 | 22 | 26 | fits | 108,205 | 253 | 0.245 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 150,803 | 1.508 | 20 | 200 | fits | 145,551 | 180 | 0.510 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 1,046,013 | 10.460 | 20 | 20 | fits | 144,299 | 111 | 0.503 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 1,070,138 | 10.701 | 20 | 24 | fits | 44,329 | 35 | 0.589 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 862,239 | 8.622 | 20 | 50 | fits | 145,951 | 173 | 0.538 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 694,263 | 6.943 | 20 | 20 | fits | 92,881 | 48 | 0.542 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 903,269 | 9.033 | 22 | 26 | fits | 106,002 | 252 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 923,951 | 9.240 | 22 | 26 | fits | 106,002 | 252 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,141,103 | 11.411 | 22 | 26 | fits | 49,266 | 102 | 0.346 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,161,808 | 11.618 | 22 | 26 | fits | 49,266 | 102 | 0.346 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 214,586 | 2.146 | 22 | 26 | fits | 98,866 | 212 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 235,217 | 2.352 | 22 | 26 | fits | 98,866 | 212 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 254,826 | 2.548 | 22 | 26 | fits | 98,866 | 212 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 275,209 | 2.752 | 22 | 26 | fits | 98,866 | 212 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 942,713 | 9.427 | 22 | 26 | fits | 106,002 | 252 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 959,564 | 9.596 | 22 | 26 | fits | 106,002 | 252 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 979,481 | 9.795 | 22 | 26 | fits | 106,002 | 252 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 325,083 | 3.251 | 22 | 26 | fits | 28,301 | 52 | 0.359 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 144,880 | 1.449 | 20 | 200 | fits | 147,155 | 182 | 0.485 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 944,359 | 9.444 | 20 | 20 | fits | 152,107 | 118 | 0.508 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 968,507 | 9.685 | 20 | 24 | fits | 44,352 | 35 | 0.591 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 752,777 | 7.528 | 20 | 50 | fits | 147,441 | 173 | 0.562 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 583,311 | 5.833 | 20 | 20 | fits | 92,917 | 51 | 0.584 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
