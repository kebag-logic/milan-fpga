### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 182 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.acmp.if0` (notice-every-6) | 6.813 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-1.held.adp.if0` (notice-burst-1) | 5.897 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.aecp.if0` (notice-every-0) | 4.635 | fits | 15 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 6.020 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.srp.if0` (notice-every-6) | 10.284 | fits | 31 srp | 4 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-6.mrpdu.periodic.if0` (notice-every-6) | 1.979 | fits | 0 srp | 2 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-3.notices.29.9.0.if0` (notice-burst-3) | 26.195 (26.499) | fits | 1 events | 160 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1385 | 0 | 156,389 (1.564) | fits |
| notice-every-6 | 1366 | 0 | 156,786 (1.568) | fits |
| notice-burst-1 | 1118 | 0 | 154,847 (1.548) | fits |
| notice-burst-3 | 1103 | 0 | 153,919 (1.539) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.193 | 130 | 16 | 2 | within |
| notice-every-0 | 4.372 | 130 | 16 | 2 | within |
| notice-every-0 | 6.141 | 130 | 16 | 2 | within |
| notice-every-0 | 6.322 | 130 | 16 | 2 | within |
| notice-every-0 | 8.335 | 130 | 16 | 2 | within |
| notice-every-0 | 8.516 | 130 | 16 | 2 | within |
| notice-every-0 | 2.130 | 130 | 16 | 2 | within |
| notice-every-0 | 2.324 | 130 | 16 | 2 | within |
| notice-every-0 | 2.493 | 130 | 16 | 2 | within |
| notice-every-0 | 2.673 | 130 | 16 | 2 | within |
| notice-every-0 | 4.539 | 130 | 16 | 2 | within |
| notice-every-0 | 4.714 | 130 | 16 | 2 | within |
| notice-every-0 | 6.490 | 130 | 16 | 2 | within |
| notice-every-0 | 6.663 | 130 | 16 | 2 | within |
| notice-every-0 | 8.683 | 130 | 16 | 2 | within |
| notice-every-0 | 8.856 | 130 | 16 | 2 | within |
| notice-every-0 | 10.232 | 130 | 16 | 2 | within |
| notice-every-0 | 10.414 | 130 | 16 | 2 | within |
| notice-every-0 | 10.566 | 130 | 16 | 2 | within |
| notice-every-0 | 10.736 | 130 | 16 | 2 | within |
| notice-every-0 | 12.331 | 130 | 16 | 2 | within |
| notice-every-0 | 12.516 | 130 | 16 | 2 | within |
| notice-every-0 | 12.675 | 130 | 16 | 2 | within |
| notice-every-0 | 12.851 | 130 | 16 | 2 | within |
| notice-every-0 | 14.179 | 130 | 16 | 2 | within |
| notice-every-0 | 14.364 | 130 | 16 | 2 | within |
| notice-every-0 | 14.518 | 130 | 16 | 2 | within |
| notice-every-0 | 14.688 | 130 | 16 | 2 | within |
| notice-every-0 | 16.200 | 130 | 16 | 2 | within |
| notice-every-0 | 16.380 | 130 | 16 | 2 | within |
| notice-every-0 | 16.534 | 130 | 16 | 2 | within |
| notice-every-0 | 16.709 | 130 | 16 | 2 | within |
| notice-every-0 | 18.200 | 130 | 16 | 2 | within |
| notice-every-0 | 18.386 | 130 | 16 | 2 | within |
| notice-every-0 | 18.540 | 130 | 16 | 2 | within |
| notice-every-0 | 18.716 | 130 | 16 | 2 | within |
| notice-every-0 | 20.173 | 130 | 16 | 2 | within |
| notice-every-0 | 20.314 | 130 | 16 | 2 | within |
| notice-every-0 | 20.491 | 130 | 16 | 2 | within |
| notice-every-0 | 20.669 | 130 | 16 | 2 | within |
| notice-every-6 | 1.560 | 130 | 16 | 2 | within |
| notice-every-6 | 1.742 | 130 | 16 | 2 | within |
| notice-every-6 | 5.692 | 130 | 16 | 2 | within |
| notice-every-6 | 5.873 | 130 | 16 | 2 | within |
| notice-every-6 | 7.606 | 130 | 16 | 2 | within |
| notice-every-6 | 7.787 | 130 | 16 | 2 | within |
| notice-every-6 | 3.527 | 130 | 16 | 2 | within |
| notice-every-6 | 3.716 | 130 | 16 | 2 | within |
| notice-every-6 | 1.912 | 130 | 16 | 2 | within |
| notice-every-6 | 2.092 | 130 | 16 | 2 | within |
| notice-every-6 | 3.881 | 130 | 16 | 2 | within |
| notice-every-6 | 4.057 | 130 | 16 | 2 | within |
| notice-every-6 | 6.040 | 130 | 16 | 2 | within |
| notice-every-6 | 6.214 | 130 | 16 | 2 | within |
| notice-every-6 | 7.954 | 130 | 16 | 2 | within |
| notice-every-6 | 8.127 | 130 | 16 | 2 | within |
| notice-every-6 | 9.716 | 130 | 16 | 2 | within |
| notice-every-6 | 9.898 | 130 | 16 | 2 | within |
| notice-every-6 | 10.049 | 130 | 16 | 2 | within |
| notice-every-6 | 10.220 | 130 | 16 | 2 | within |
| notice-every-6 | 11.606 | 130 | 16 | 2 | within |
| notice-every-6 | 11.791 | 130 | 16 | 2 | within |
| notice-every-6 | 11.949 | 130 | 16 | 2 | within |
| notice-every-6 | 12.125 | 130 | 16 | 2 | within |
| notice-every-6 | 13.659 | 130 | 16 | 2 | within |
| notice-every-6 | 13.844 | 130 | 16 | 2 | within |
| notice-every-6 | 13.998 | 130 | 16 | 2 | within |
| notice-every-6 | 14.168 | 130 | 16 | 2 | within |
| notice-every-6 | 15.679 | 130 | 16 | 2 | within |
| notice-every-6 | 15.859 | 130 | 16 | 2 | within |
| notice-every-6 | 16.013 | 130 | 16 | 2 | within |
| notice-every-6 | 16.189 | 130 | 16 | 2 | within |
| notice-every-6 | 17.680 | 130 | 16 | 2 | within |
| notice-every-6 | 17.865 | 130 | 16 | 2 | within |
| notice-every-6 | 18.019 | 130 | 16 | 2 | within |
| notice-every-6 | 18.195 | 130 | 16 | 2 | within |
| notice-every-6 | 21.322 | 130 | 16 | 2 | within |
| notice-every-6 | 21.464 | 130 | 16 | 2 | within |
| notice-every-6 | 21.640 | 130 | 16 | 2 | within |
| notice-every-6 | 21.817 | 130 | 16 | 2 | within |
| notice-burst-1 | 3.440 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.619 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.264 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.438 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.558 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.738 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.562 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.741 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.789 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.977 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.028 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.220 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.607 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.785 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.905 | 130 | 16 | 1 | within |
| notice-burst-1 | 7.081 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.140 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.312 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.033 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.214 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.370 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.545 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.402 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.604 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.910 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.101 | 130 | 16 | 1 | within |
| notice-burst-1 | 20.056 | 130 | 16 | 1 | within |
| notice-burst-1 | 20.236 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.802 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.002 | 130 | 16 | 1 | within |
| notice-burst-1 | 20.390 | 130 | 16 | 1 | within |
| notice-burst-1 | 20.566 | 130 | 16 | 1 | within |
| notice-burst-1 | 22.056 | 130 | 16 | 1 | within |
| notice-burst-1 | 22.241 | 130 | 16 | 1 | within |
| notice-burst-1 | 22.394 | 130 | 16 | 1 | within |
| notice-burst-1 | 22.571 | 130 | 16 | 1 | within |
| notice-burst-1 | 24.075 | 130 | 16 | 1 | within |
| notice-burst-1 | 24.216 | 130 | 16 | 1 | within |
| notice-burst-1 | 24.392 | 130 | 16 | 1 | within |
| notice-burst-1 | 24.571 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.620 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.798 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.591 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.766 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.922 | 130 | 16 | 1 | within |
| notice-burst-3 | 7.094 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.765 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.954 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.184 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.378 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.131 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.321 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.492 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.673 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.554 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.741 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.968 | 130 | 16 | 1 | within |
| notice-burst-3 | 6.147 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.109 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.280 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.207 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.391 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.550 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.726 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.238 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.422 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.575 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.746 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.030 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.238 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.227 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.411 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.565 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.742 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.257 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.441 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.592 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.727 | 130 | 16 | 1 | within |
| notice-burst-3 | 26.195 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.461 | 130 | 16 | 1 | within |

Latest: 26.195 ms, notice-burst-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 303 | 101,373 (1.014) | 70,329 (0.703) |
| notice-every-6 | 303 | 101,373 (1.014) | 70,329 (0.703) |
| notice-burst-1 | 313 | 119,731 (1.197) | 70,329 (0.703) |
| notice-burst-3 | 313 | 116,049 (1.160) | 70,329 (0.703) |

Longest pass that carries a step: 119,731 CPU cycles (1.197 ms), notice-burst-1; longest step: 70,329 (0.703 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 419,290 | 4.193 | 130 | 134 | fits | 76,767 | 205 | 0.211 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 437,243 | 4.372 | 130 | 134 | fits | 76,767 | 205 | 0.211 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 614,140 | 6.141 | 130 | 134 | fits | 75,574 | 205 | 0.198 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 632,207 | 6.322 | 130 | 134 | fits | 75,574 | 205 | 0.198 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 833,503 | 8.335 | 130 | 134 | fits | 75,085 | 203 | 0.198 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 851,610 | 8.516 | 130 | 134 | fits | 75,085 | 203 | 0.198 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 212,998 | 2.130 | 130 | 134 | fits | 80,711 | 205 | 0.231 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 232,438 | 2.324 | 130 | 134 | fits | 80,711 | 205 | 0.231 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 249,323 | 2.493 | 130 | 134 | fits | 80,711 | 205 | 0.231 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 267,304 | 2.673 | 130 | 134 | fits | 80,711 | 205 | 0.231 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 453,861 | 4.539 | 130 | 134 | fits | 76,767 | 205 | 0.211 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 471,432 | 4.714 | 130 | 134 | fits | 76,767 | 205 | 0.211 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 648,992 | 6.490 | 130 | 134 | fits | 75,574 | 205 | 0.198 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 666,332 | 6.663 | 130 | 134 | fits | 75,574 | 205 | 0.198 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 868,293 | 8.683 | 130 | 134 | fits | 75,085 | 203 | 0.198 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 885,560 | 8.856 | 130 | 134 | fits | 75,085 | 203 | 0.198 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,023,231 | 10.232 | 130 | 134 | fits | 73,458 | 203 | 0.199 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,041,367 | 10.414 | 130 | 134 | fits | 73,458 | 203 | 0.199 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 1,056,562 | 10.566 | 130 | 134 | fits | 73,458 | 203 | 0.199 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,073,583 | 10.736 | 130 | 134 | fits | 73,458 | 203 | 0.199 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,233,096 | 12.331 | 130 | 134 | fits | 74,983 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,251,586 | 12.516 | 130 | 134 | fits | 74,983 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,267,524 | 12.675 | 130 | 134 | fits | 74,983 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,285,099 | 12.851 | 130 | 134 | fits | 74,983 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,417,914 | 14.179 | 130 | 134 | fits | 72,709 | 203 | 0.196 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,436,404 | 14.364 | 130 | 134 | fits | 72,709 | 203 | 0.196 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,451,820 | 14.518 | 130 | 134 | fits | 72,709 | 203 | 0.196 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,468,841 | 14.688 | 130 | 134 | fits | 72,709 | 203 | 0.196 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,619,954 | 16.200 | 130 | 134 | fits | 72,395 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,637,985 | 16.380 | 130 | 134 | fits | 72,395 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,653,413 | 16.534 | 130 | 134 | fits | 72,395 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,670,940 | 16.709 | 130 | 134 | fits | 72,395 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,820,014 | 18.200 | 130 | 134 | fits | 73,047 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,838,575 | 18.386 | 130 | 134 | fits | 73,047 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,853,975 | 18.540 | 130 | 134 | fits | 73,047 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,871,574 | 18.716 | 130 | 134 | fits | 73,047 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,017,261 | 20.173 | 130 | 134 | fits | 68,622 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,031,401 | 20.314 | 130 | 134 | fits | 68,622 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,049,093 | 20.491 | 130 | 134 | fits | 68,622 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,066,853 | 20.669 | 130 | 134 | fits | 68,622 | 203 | 0.193 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 322,333 | 3.223 | 20 | 200 | fits | 94,058 | 105 | 0.369 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 641,481 | 6.415 | 20 | 20 | fits | 138,946 | 76 | 0.674 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 463,510 | 4.635 | 20 | 24 | fits | 156,389 | 154 | 0.443 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 602,006 | 6.020 | 20 | 50 | fits | 138,946 | 76 | 0.674 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 987,114 | 9.871 | 20 | 20 | fits | 97,380 | 45 | 0.561 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 191,410 | 1.914 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 155,980 | 1.560 | 130 | 134 | fits | 78,647 | 205 | 0.231 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 174,171 | 1.742 | 130 | 134 | fits | 78,647 | 205 | 0.231 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 569,223 | 5.692 | 130 | 134 | fits | 75,489 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 587,265 | 5.873 | 130 | 134 | fits | 75,489 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 760,626 | 7.606 | 130 | 134 | fits | 75,293 | 205 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 778,733 | 7.787 | 130 | 134 | fits | 75,293 | 205 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 352,696 | 3.527 | 130 | 134 | fits | 77,614 | 205 | 0.196 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 371,637 | 3.716 | 130 | 134 | fits | 77,614 | 205 | 0.196 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 191,184 | 1.912 | 130 | 134 | fits | 78,647 | 205 | 0.231 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 209,165 | 2.092 | 130 | 134 | fits | 78,647 | 205 | 0.231 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 388,081 | 3.881 | 130 | 134 | fits | 77,614 | 205 | 0.196 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 405,652 | 4.057 | 130 | 134 | fits | 77,614 | 205 | 0.196 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 604,050 | 6.040 | 130 | 134 | fits | 75,489 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 621,390 | 6.214 | 130 | 134 | fits | 75,489 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 795,416 | 7.954 | 130 | 134 | fits | 75,293 | 205 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 812,683 | 8.127 | 130 | 134 | fits | 75,293 | 205 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 971,642 | 9.716 | 130 | 134 | fits | 73,534 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 989,753 | 9.898 | 130 | 134 | fits | 73,534 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 1,004,948 | 10.049 | 130 | 134 | fits | 73,534 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,021,969 | 10.220 | 130 | 134 | fits | 73,534 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,160,568 | 11.606 | 130 | 134 | fits | 74,939 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,179,058 | 11.791 | 130 | 134 | fits | 74,939 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,194,917 | 11.949 | 130 | 134 | fits | 74,939 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,212,492 | 12.125 | 130 | 134 | fits | 74,939 | 203 | 0.200 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,365,929 | 13.659 | 130 | 134 | fits | 72,630 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,384,419 | 13.844 | 130 | 134 | fits | 72,630 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,399,756 | 13.998 | 130 | 134 | fits | 72,630 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,416,777 | 14.168 | 130 | 134 | fits | 72,630 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,567,890 | 15.679 | 130 | 134 | fits | 72,395 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,585,921 | 15.859 | 130 | 134 | fits | 72,395 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,601,349 | 16.013 | 130 | 134 | fits | 72,395 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,618,876 | 16.189 | 130 | 134 | fits | 72,395 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,767,950 | 17.680 | 130 | 134 | fits | 73,047 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,786,511 | 17.865 | 130 | 134 | fits | 73,047 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,801,911 | 18.019 | 130 | 134 | fits | 73,047 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,819,510 | 18.195 | 130 | 134 | fits | 73,047 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,132,226 | 21.322 | 130 | 134 | fits | 68,687 | 202 | 0.199 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,146,372 | 21.464 | 130 | 134 | fits | 68,687 | 202 | 0.199 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,163,985 | 21.640 | 130 | 134 | fits | 68,687 | 202 | 0.199 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,181,745 | 21.817 | 130 | 134 | fits | 68,687 | 202 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 536,568 | 5.366 | 20 | 200 | fits | 156,786 | 224 | 0.354 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 681,325 | 6.813 | 20 | 20 | fits | 142,007 | 62 | 0.675 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 331,851 | 3.319 | 20 | 24 | fits | 71,376 | 57 | 0.515 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 476,825 | 4.768 | 20 | 50 | fits | 156,786 | 224 | 0.354 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,028,405 | 10.284 | 20 | 20 | fits | 87,915 | 41 | 0.636 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 197,931 | 1.979 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 343,977 | 3.440 | 130 | 134 | fits | 102,912 | 211 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 361,858 | 3.619 | 130 | 134 | fits | 102,912 | 211 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 426,377 | 4.264 | 130 | 134 | fits | 76,601 | 205 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 443,838 | 4.438 | 130 | 134 | fits | 76,601 | 205 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 555,763 | 5.558 | 130 | 134 | fits | 119,731 | 211 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 573,800 | 5.738 | 130 | 134 | fits | 119,731 | 211 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 656,167 | 6.562 | 130 | 134 | fits | 75,292 | 205 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 674,065 | 6.741 | 130 | 134 | fits | 75,292 | 205 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 1,678,867 | 16.789 | 130 | 134 | fits | 78,640 | 203 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 1,697,651 | 16.977 | 130 | 134 | fits | 78,640 | 203 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 202,783 | 2.028 | 130 | 134 | fits | 86,937 | 205 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 222,050 | 2.220 | 130 | 134 | fits | 86,937 | 205 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 460,656 | 4.607 | 130 | 134 | fits | 76,601 | 205 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 478,531 | 4.785 | 130 | 134 | fits | 76,601 | 205 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 690,505 | 6.905 | 130 | 134 | fits | 75,292 | 205 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 708,076 | 7.081 | 130 | 134 | fits | 75,292 | 205 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 1,714,039 | 17.140 | 130 | 134 | fits | 78,640 | 203 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 1,731,212 | 17.312 | 130 | 134 | fits | 78,640 | 203 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 1,803,330 | 18.033 | 130 | 134 | fits | 73,183 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 1,821,368 | 18.214 | 130 | 134 | fits | 73,183 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 1,837,031 | 18.370 | 130 | 134 | fits | 73,183 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 1,854,505 | 18.545 | 130 | 134 | fits | 73,183 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 240,237 | 2.402 | 130 | 134 | fits | 86,937 | 205 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 260,352 | 2.604 | 130 | 134 | fits | 86,937 | 205 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 591,037 | 5.910 | 130 | 134 | fits | 119,731 | 211 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 610,055 | 6.101 | 130 | 134 | fits | 119,731 | 211 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 2,005,632 | 20.056 | 130 | 134 | fits | 71,911 | 203 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 2,023,591 | 20.236 | 130 | 134 | fits | 71,911 | 203 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 380,245 | 3.802 | 130 | 134 | fits | 102,912 | 211 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 400,195 | 4.002 | 130 | 134 | fits | 102,912 | 211 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 2,039,019 | 20.390 | 130 | 134 | fits | 71,911 | 203 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 2,056,618 | 20.566 | 130 | 134 | fits | 71,911 | 203 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,205,614 | 22.056 | 130 | 134 | fits | 72,982 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 2,224,103 | 22.241 | 130 | 134 | fits | 72,982 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 2,239,438 | 22.394 | 130 | 134 | fits | 72,982 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 2,257,109 | 22.571 | 130 | 134 | fits | 72,982 | 203 | 0.197 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 2,407,508 | 24.075 | 130 | 134 | fits | 68,790 | 202 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 2,421,630 | 24.216 | 130 | 134 | fits | 68,790 | 202 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 2,439,250 | 24.392 | 130 | 134 | fits | 68,790 | 202 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 2,457,067 | 24.571 | 130 | 134 | fits | 68,790 | 202 | 0.196 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 589,723 | 5.897 | 20 | 200 | fits | 147,036 | 201 | 0.350 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 569,455 | 5.695 | 20 | 20 | fits | 147,036 | 201 | 0.350 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 402,215 | 4.022 | 20 | 24 | fits | 154,847 | 174 | 0.424 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 529,980 | 5.300 | 20 | 50 | fits | 147,036 | 201 | 0.350 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 995,109 | 9.951 | 20 | 20 | fits | 72,734 | 30 | 0.637 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 561,951 | 5.620 | 130 | 134 | fits | 116,049 | 211 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 579,754 | 5.798 | 130 | 134 | fits | 116,049 | 211 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 659,094 | 6.591 | 130 | 134 | fits | 72,539 | 205 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 676,634 | 6.766 | 130 | 134 | fits | 72,539 | 205 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 692,224 | 6.922 | 130 | 134 | fits | 72,539 | 205 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 709,394 | 7.094 | 130 | 134 | fits | 72,539 | 205 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 1,676,495 | 16.765 | 130 | 134 | fits | 77,723 | 203 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 1,695,412 | 16.954 | 130 | 134 | fits | 77,723 | 203 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 218,392 | 2.184 | 130 | 134 | fits | 105,335 | 213 | 0.258 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 237,763 | 2.378 | 130 | 134 | fits | 105,335 | 213 | 0.258 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 413,145 | 4.131 | 130 | 134 | fits | 79,581 | 205 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 432,143 | 4.321 | 130 | 134 | fits | 79,581 | 205 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 449,154 | 4.492 | 130 | 134 | fits | 79,581 | 205 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 467,260 | 4.673 | 130 | 134 | fits | 79,581 | 205 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 255,407 | 2.554 | 130 | 134 | fits | 105,335 | 213 | 0.258 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 274,132 | 2.741 | 130 | 134 | fits | 105,335 | 213 | 0.258 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 596,814 | 5.968 | 130 | 134 | fits | 116,049 | 211 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 614,680 | 6.147 | 130 | 134 | fits | 116,049 | 211 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,710,928 | 17.109 | 130 | 134 | fits | 77,723 | 203 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,728,021 | 17.280 | 130 | 134 | fits | 77,723 | 203 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 1,820,713 | 18.207 | 130 | 134 | fits | 74,428 | 203 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,839,131 | 18.391 | 130 | 134 | fits | 74,428 | 203 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 1,854,976 | 18.550 | 130 | 134 | fits | 74,428 | 203 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 1,872,623 | 18.726 | 130 | 134 | fits | 74,428 | 203 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 2,023,826 | 20.238 | 130 | 134 | fits | 72,191 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 2,042,244 | 20.422 | 130 | 134 | fits | 72,191 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 2,057,502 | 20.575 | 130 | 134 | fits | 72,191 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 2,074,595 | 20.746 | 130 | 134 | fits | 72,191 | 203 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 302,959 | 3.030 | 130 | 134 | fits | 71,373 | 153 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 323,818 | 3.238 | 130 | 134 | fits | 71,373 | 153 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,222,696 | 22.227 | 130 | 134 | fits | 72,615 | 203 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,241,113 | 22.411 | 130 | 134 | fits | 72,615 | 203 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,256,540 | 22.565 | 130 | 134 | fits | 72,615 | 203 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 2,274,211 | 22.742 | 130 | 134 | fits | 72,615 | 203 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 2,425,656 | 24.257 | 130 | 134 | fits | 68,056 | 201 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 2,444,145 | 24.441 | 130 | 134 | fits | 68,056 | 201 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 2,459,240 | 24.592 | 130 | 134 | fits | 68,056 | 201 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,472,726 | 24.727 | 130 | 134 | fits | 68,056 | 201 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,619,517 | 26.195 | 130 | 134 | fits | 22,788 | 53 | 0.323 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 346,050 | 3.461 | 130 | 134 | fits | 71,373 | 153 | 0.174 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 575,511 | 5.755 | 20 | 200 | fits | 146,781 | 201 | 0.349 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 555,243 | 5.552 | 20 | 20 | fits | 146,781 | 201 | 0.349 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 388,258 | 3.883 | 20 | 24 | fits | 153,858 | 174 | 0.418 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 515,768 | 5.158 | 20 | 50 | fits | 146,781 | 201 | 0.349 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 979,586 | 9.796 | 20 | 20 | fits | 72,386 | 30 | 0.637 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
