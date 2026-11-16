### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-7.held.acmp.if0` (notice-burst-7) | 4.651 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.adp.if0` (notice-burst-0) | 4.775 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-7.held.aecp.if0` (notice-burst-7) | 4.449 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-7.held.maap.if0` (notice-burst-7) | 4.257 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-4.held.srp.if0` (notice-every-4) | 11.420 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 1.171 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 27.236 (27.460) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1532 | 0 | 152,942 (1.529) | fits |
| notice-every-1 | 1539 | 0 | 152,450 (1.524) | fits |
| notice-every-2 | 1530 | 0 | 155,660 (1.557) | fits |
| notice-every-3 | 1530 | 0 | 155,521 (1.555) | fits |
| notice-every-4 | 1528 | 0 | 155,705 (1.557) | fits |
| notice-every-5 | 1524 | 0 | 153,103 (1.531) | fits |
| notice-every-6 | 1527 | 0 | 155,120 (1.551) | fits |
| notice-every-7 | 1519 | 0 | 154,215 (1.542) | fits |
| notice-burst-0 | 1058 | 0 | 152,418 (1.524) | fits |
| notice-burst-1 | 1067 | 0 | 154,010 (1.540) | fits |
| notice-burst-2 | 1086 | 0 | 155,429 (1.554) | fits |
| notice-burst-3 | 1055 | 0 | 156,173 (1.562) | fits |
| notice-burst-4 | 1063 | 0 | 154,692 (1.547) | fits |
| notice-burst-5 | 1040 | 0 | 155,861 (1.559) | fits |
| notice-burst-6 | 1055 | 0 | 155,834 (1.558) | fits |
| notice-burst-7 | 1094 | 0 | 150,822 (1.508) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 7.910 | 140 | 16 | 2 | within |
| notice-every-0 | 8.110 | 140 | 16 | 2 | within |
| notice-every-0 | 1.892 | 140 | 16 | 2 | within |
| notice-every-0 | 2.101 | 140 | 16 | 2 | within |
| notice-every-0 | 3.843 | 140 | 16 | 2 | within |
| notice-every-0 | 4.046 | 140 | 16 | 2 | within |
| notice-every-0 | 5.886 | 140 | 16 | 2 | within |
| notice-every-0 | 6.088 | 140 | 16 | 2 | within |
| notice-every-0 | 9.883 | 140 | 16 | 2 | within |
| notice-every-0 | 10.054 | 140 | 16 | 2 | within |
| notice-every-0 | 11.819 | 140 | 16 | 2 | within |
| notice-every-0 | 12.017 | 140 | 16 | 2 | within |
| notice-every-1 | 2.117 | 140 | 16 | 2 | within |
| notice-every-1 | 2.323 | 140 | 16 | 2 | within |
| notice-every-1 | 4.160 | 140 | 16 | 2 | within |
| notice-every-1 | 4.362 | 140 | 16 | 2 | within |
| notice-every-1 | 6.111 | 140 | 16 | 2 | within |
| notice-every-1 | 6.311 | 140 | 16 | 2 | within |
| notice-every-1 | 8.117 | 140 | 16 | 2 | within |
| notice-every-1 | 8.315 | 140 | 16 | 2 | within |
| notice-every-1 | 10.090 | 140 | 16 | 2 | within |
| notice-every-1 | 10.261 | 140 | 16 | 2 | within |
| notice-every-1 | 12.204 | 140 | 16 | 2 | within |
| notice-every-1 | 12.403 | 140 | 16 | 2 | within |
| notice-every-2 | 2.065 | 140 | 16 | 2 | within |
| notice-every-2 | 2.269 | 140 | 16 | 2 | within |
| notice-every-2 | 3.994 | 140 | 16 | 2 | within |
| notice-every-2 | 4.198 | 140 | 16 | 2 | within |
| notice-every-2 | 5.854 | 140 | 16 | 2 | within |
| notice-every-2 | 6.054 | 140 | 16 | 2 | within |
| notice-every-2 | 7.862 | 140 | 16 | 2 | within |
| notice-every-2 | 8.060 | 140 | 16 | 2 | within |
| notice-every-2 | 9.835 | 140 | 16 | 2 | within |
| notice-every-2 | 10.006 | 140 | 16 | 2 | within |
| notice-every-2 | 11.949 | 140 | 16 | 2 | within |
| notice-every-2 | 12.147 | 140 | 16 | 2 | within |
| notice-every-3 | 6.127 | 140 | 16 | 2 | within |
| notice-every-3 | 6.328 | 140 | 16 | 2 | within |
| notice-every-3 | 8.146 | 140 | 16 | 2 | within |
| notice-every-3 | 8.347 | 140 | 16 | 2 | within |
| notice-every-3 | 2.123 | 140 | 16 | 2 | within |
| notice-every-3 | 2.334 | 140 | 16 | 2 | within |
| notice-every-3 | 4.166 | 140 | 16 | 2 | within |
| notice-every-3 | 4.370 | 140 | 16 | 2 | within |
| notice-every-3 | 10.125 | 140 | 16 | 2 | within |
| notice-every-3 | 10.297 | 140 | 16 | 2 | within |
| notice-every-3 | 12.241 | 140 | 16 | 2 | within |
| notice-every-3 | 12.440 | 140 | 16 | 2 | within |
| notice-every-4 | 6.126 | 140 | 16 | 2 | within |
| notice-every-4 | 6.327 | 140 | 16 | 2 | within |
| notice-every-4 | 8.145 | 140 | 16 | 2 | within |
| notice-every-4 | 8.346 | 140 | 16 | 2 | within |
| notice-every-4 | 2.122 | 140 | 16 | 2 | within |
| notice-every-4 | 2.333 | 140 | 16 | 2 | within |
| notice-every-4 | 4.166 | 140 | 16 | 2 | within |
| notice-every-4 | 4.369 | 140 | 16 | 2 | within |
| notice-every-4 | 10.124 | 140 | 16 | 2 | within |
| notice-every-4 | 10.296 | 140 | 16 | 2 | within |
| notice-every-4 | 12.240 | 140 | 16 | 2 | within |
| notice-every-4 | 12.439 | 140 | 16 | 2 | within |
| notice-every-5 | 8.197 | 140 | 16 | 2 | within |
| notice-every-5 | 8.396 | 140 | 16 | 2 | within |
| notice-every-5 | 2.171 | 140 | 16 | 2 | within |
| notice-every-5 | 2.383 | 140 | 16 | 2 | within |
| notice-every-5 | 4.220 | 140 | 16 | 2 | within |
| notice-every-5 | 4.421 | 140 | 16 | 2 | within |
| notice-every-5 | 6.172 | 140 | 16 | 2 | within |
| notice-every-5 | 6.376 | 140 | 16 | 2 | within |
| notice-every-5 | 10.172 | 140 | 16 | 2 | within |
| notice-every-5 | 10.343 | 140 | 16 | 2 | within |
| notice-every-5 | 12.288 | 140 | 16 | 2 | within |
| notice-every-5 | 12.486 | 140 | 16 | 2 | within |
| notice-every-6 | 8.198 | 140 | 16 | 2 | within |
| notice-every-6 | 8.398 | 140 | 16 | 2 | within |
| notice-every-6 | 2.173 | 140 | 16 | 2 | within |
| notice-every-6 | 2.384 | 140 | 16 | 2 | within |
| notice-every-6 | 4.222 | 140 | 16 | 2 | within |
| notice-every-6 | 4.423 | 140 | 16 | 2 | within |
| notice-every-6 | 6.174 | 140 | 16 | 2 | within |
| notice-every-6 | 6.378 | 140 | 16 | 2 | within |
| notice-every-6 | 10.174 | 140 | 16 | 2 | within |
| notice-every-6 | 10.345 | 140 | 16 | 2 | within |
| notice-every-6 | 12.289 | 140 | 16 | 2 | within |
| notice-every-6 | 12.488 | 140 | 16 | 2 | within |
| notice-every-7 | 2.347 | 140 | 16 | 2 | within |
| notice-every-7 | 2.553 | 140 | 16 | 2 | within |
| notice-every-7 | 4.184 | 140 | 16 | 2 | within |
| notice-every-7 | 4.386 | 140 | 16 | 2 | within |
| notice-every-7 | 6.134 | 140 | 16 | 2 | within |
| notice-every-7 | 6.334 | 140 | 16 | 2 | within |
| notice-every-7 | 8.140 | 140 | 16 | 2 | within |
| notice-every-7 | 8.339 | 140 | 16 | 2 | within |
| notice-every-7 | 10.113 | 140 | 16 | 2 | within |
| notice-every-7 | 10.284 | 140 | 16 | 2 | within |
| notice-every-7 | 12.230 | 140 | 16 | 2 | within |
| notice-every-7 | 12.428 | 140 | 16 | 2 | within |
| notice-burst-0 | 8.377 | 140 | 16 | 0 | within |
| notice-burst-0 | 16.369 | 140 | 16 | 0 | within |
| notice-burst-0 | 16.589 | 140 | 16 | 0 | within |
| notice-burst-0 | 18.000 | 140 | 16 | 0 | within |
| notice-burst-0 | 2.048 | 140 | 16 | 0 | within |
| notice-burst-0 | 2.255 | 140 | 16 | 0 | within |
| notice-burst-0 | 3.220 | 140 | 16 | 0 | within |
| notice-burst-0 | 3.425 | 140 | 16 | 0 | within |
| notice-burst-0 | 18.184 | 140 | 16 | 0 | within |
| notice-burst-0 | 20.078 | 140 | 16 | 0 | within |
| notice-burst-0 | 20.277 | 140 | 16 | 0 | within |
| notice-burst-0 | 5.038 | 140 | 16 | 0 | within |
| notice-burst-1 | 9.707 | 140 | 16 | 1 | within |
| notice-burst-1 | 15.752 | 140 | 16 | 1 | within |
| notice-burst-1 | 15.968 | 140 | 16 | 1 | within |
| notice-burst-1 | 17.196 | 140 | 16 | 1 | within |
| notice-burst-1 | 2.363 | 140 | 16 | 1 | within |
| notice-burst-1 | 2.572 | 140 | 16 | 1 | within |
| notice-burst-1 | 3.031 | 140 | 16 | 1 | within |
| notice-burst-1 | 3.234 | 140 | 16 | 1 | within |
| notice-burst-1 | 17.380 | 140 | 16 | 1 | within |
| notice-burst-1 | 19.095 | 140 | 16 | 1 | within |
| notice-burst-1 | 19.294 | 140 | 16 | 1 | within |
| notice-burst-1 | 7.332 | 140 | 16 | 1 | within |
| notice-burst-2 | 14.267 | 140 | 16 | 0 | within |
| notice-burst-2 | 14.474 | 140 | 16 | 0 | within |
| notice-burst-2 | 16.103 | 140 | 16 | 0 | within |
| notice-burst-2 | 16.304 | 140 | 16 | 0 | within |
| notice-burst-2 | 2.519 | 140 | 16 | 0 | within |
| notice-burst-2 | 2.728 | 140 | 16 | 0 | within |
| notice-burst-2 | 4.562 | 140 | 16 | 0 | within |
| notice-burst-2 | 18.086 | 140 | 16 | 0 | within |
| notice-burst-2 | 18.269 | 140 | 16 | 0 | within |
| notice-burst-2 | 20.010 | 140 | 16 | 0 | within |
| notice-burst-2 | 20.206 | 140 | 16 | 0 | within |
| notice-burst-2 | 22.006 | 140 | 16 | 0 | within |
| notice-burst-3 | 13.405 | 140 | 16 | 2 | within |
| notice-burst-3 | 13.611 | 140 | 16 | 2 | within |
| notice-burst-3 | 15.244 | 140 | 16 | 2 | within |
| notice-burst-3 | 15.445 | 140 | 16 | 2 | within |
| notice-burst-3 | 3.588 | 140 | 16 | 2 | within |
| notice-burst-3 | 17.235 | 140 | 16 | 2 | within |
| notice-burst-3 | 17.437 | 140 | 16 | 2 | within |
| notice-burst-3 | 19.217 | 140 | 16 | 2 | within |
| notice-burst-3 | 19.400 | 140 | 16 | 2 | within |
| notice-burst-3 | 21.187 | 140 | 16 | 2 | within |
| notice-burst-3 | 21.384 | 140 | 16 | 2 | within |
| notice-burst-3 | 23.144 | 140 | 16 | 2 | within |
| notice-burst-4 | 5.736 | 140 | 16 | 1 | within |
| notice-burst-4 | 5.940 | 140 | 16 | 1 | within |
| notice-burst-4 | 17.150 | 140 | 16 | 1 | within |
| notice-burst-4 | 17.360 | 140 | 16 | 1 | within |
| notice-burst-4 | 18.250 | 140 | 16 | 1 | within |
| notice-burst-4 | 18.448 | 140 | 16 | 1 | within |
| notice-burst-4 | 20.226 | 140 | 16 | 1 | within |
| notice-burst-4 | 20.425 | 140 | 16 | 1 | within |
| notice-burst-4 | 22.176 | 140 | 16 | 1 | within |
| notice-burst-4 | 22.347 | 140 | 16 | 1 | within |
| notice-burst-4 | 24.292 | 140 | 16 | 1 | within |
| notice-burst-4 | 24.489 | 140 | 16 | 1 | within |
| notice-burst-5 | 7.557 | 140 | 16 | 1 | within |
| notice-burst-5 | 17.321 | 140 | 16 | 1 | within |
| notice-burst-5 | 17.540 | 140 | 16 | 1 | within |
| notice-burst-5 | 19.163 | 140 | 16 | 1 | within |
| notice-burst-5 | 19.367 | 140 | 16 | 1 | within |
| notice-burst-5 | 21.149 | 140 | 16 | 1 | within |
| notice-burst-5 | 21.352 | 140 | 16 | 1 | within |
| notice-burst-5 | 23.129 | 140 | 16 | 1 | within |
| notice-burst-5 | 23.312 | 140 | 16 | 1 | within |
| notice-burst-5 | 25.099 | 140 | 16 | 1 | within |
| notice-burst-5 | 25.297 | 140 | 16 | 1 | within |
| notice-burst-5 | 27.236 | 140 | 16 | 1 | within |
| notice-burst-6 | 7.683 | 140 | 16 | 1 | within |
| notice-burst-6 | 17.392 | 140 | 16 | 1 | within |
| notice-burst-6 | 17.610 | 140 | 16 | 1 | within |
| notice-burst-6 | 19.234 | 140 | 16 | 1 | within |
| notice-burst-6 | 19.437 | 140 | 16 | 1 | within |
| notice-burst-6 | 21.220 | 140 | 16 | 1 | within |
| notice-burst-6 | 21.422 | 140 | 16 | 1 | within |
| notice-burst-6 | 23.200 | 140 | 16 | 1 | within |
| notice-burst-6 | 23.383 | 140 | 16 | 1 | within |
| notice-burst-6 | 25.172 | 140 | 16 | 1 | within |
| notice-burst-6 | 25.370 | 140 | 16 | 1 | within |
| notice-burst-6 | 27.132 | 140 | 16 | 1 | within |
| notice-burst-7 | 9.440 | 140 | 16 | 1 | within |
| notice-burst-7 | 17.608 | 140 | 16 | 1 | within |
| notice-burst-7 | 17.828 | 140 | 16 | 1 | within |
| notice-burst-7 | 19.240 | 140 | 16 | 1 | within |
| notice-burst-7 | 2.258 | 140 | 16 | 1 | within |
| notice-burst-7 | 2.466 | 140 | 16 | 1 | within |
| notice-burst-7 | 3.123 | 140 | 16 | 1 | within |
| notice-burst-7 | 3.327 | 140 | 16 | 1 | within |
| notice-burst-7 | 19.424 | 140 | 16 | 1 | within |
| notice-burst-7 | 21.137 | 140 | 16 | 1 | within |
| notice-burst-7 | 21.336 | 140 | 16 | 1 | within |
| notice-burst-7 | 7.654 | 140 | 16 | 1 | within |

Latest: 27.236 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 99,074 (0.991) | 76,617 (0.766) |
| notice-every-1 | 307 | 102,514 (1.025) | 76,617 (0.766) |
| notice-every-2 | 307 | 102,354 (1.024) | 76,561 (0.766) |
| notice-every-3 | 307 | 102,493 (1.025) | 76,617 (0.766) |
| notice-every-4 | 307 | 111,762 (1.118) | 76,636 (0.766) |
| notice-every-5 | 307 | 91,885 (0.919) | 75,775 (0.758) |
| notice-every-6 | 307 | 91,885 (0.919) | 75,775 (0.758) |
| notice-every-7 | 307 | 91,885 (0.919) | 75,775 (0.758) |
| notice-burst-0 | 317 | 108,475 (1.085) | 77,790 (0.778) |
| notice-burst-1 | 317 | 142,096 (1.421) | 77,790 (0.778) |
| notice-burst-2 | 317 | 102,354 (1.024) | 77,790 (0.778) |
| notice-burst-3 | 317 | 102,493 (1.025) | 77,790 (0.778) |
| notice-burst-4 | 317 | 111,762 (1.118) | 77,790 (0.778) |
| notice-burst-5 | 317 | 101,753 (1.018) | 77,790 (0.778) |
| notice-burst-6 | 317 | 102,212 (1.022) | 77,790 (0.778) |
| notice-burst-7 | 317 | 108,759 (1.088) | 77,790 (0.778) |

Longest pass that carries a step: 142,096 CPU cycles (1.421 ms), notice-burst-1; longest step: 77,790 (0.778 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 791,034 | 7.910 | 140 | 144 | fits | 47,581 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 810,956 | 8.110 | 140 | 144 | fits | 47,581 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 189,171 | 1.892 | 140 | 144 | fits | 50,573 | 105 | 0.318 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 210,104 | 2.101 | 140 | 144 | fits | 50,573 | 105 | 0.318 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 384,294 | 3.843 | 140 | 144 | fits | 49,671 | 109 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 404,590 | 4.046 | 140 | 144 | fits | 49,671 | 109 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 588,590 | 5.886 | 140 | 144 | fits | 47,493 | 105 | 0.264 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 608,803 | 6.088 | 140 | 144 | fits | 47,493 | 105 | 0.264 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 988,332 | 9.883 | 140 | 144 | fits | 41,275 | 101 | 0.226 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 1,005,439 | 10.054 | 140 | 144 | fits | 41,275 | 101 | 0.226 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 1,181,909 | 11.819 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 1,201,733 | 12.017 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 158,297 | 1.583 | 20 | 200 | fits | 147,510 | 270 | 0.340 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 422,965 | 4.230 | 20 | 20 | fits | 122,083 | 114 | 0.490 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 402,761 | 4.028 | 20 | 24 | fits | 122,083 | 114 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 383,490 | 3.835 | 20 | 50 | fits | 122,083 | 114 | 0.490 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,116,752 | 11.168 | 20 | 20 | fits | 45,011 | 31 | 0.809 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 93,708 | 0.937 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 211,704 | 2.117 | 140 | 144 | fits | 49,861 | 105 | 0.327 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 232,287 | 2.323 | 140 | 144 | fits | 49,861 | 105 | 0.327 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 416,031 | 4.160 | 140 | 144 | fits | 48,729 | 104 | 0.289 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 436,198 | 4.362 | 140 | 144 | fits | 48,729 | 104 | 0.289 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 611,056 | 6.111 | 140 | 144 | fits | 47,708 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 631,094 | 6.311 | 140 | 144 | fits | 47,708 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 811,711 | 8.117 | 140 | 144 | fits | 46,355 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 831,542 | 8.315 | 140 | 144 | fits | 46,355 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 1,008,987 | 10.090 | 140 | 144 | fits | 41,472 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 1,026,094 | 10.261 | 140 | 144 | fits | 41,472 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 1,220,448 | 12.204 | 140 | 144 | fits | 45,159 | 104 | 0.184 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 1,240,272 | 12.403 | 140 | 144 | fits | 45,159 | 104 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 164,934 | 1.649 | 20 | 200 | fits | 147,053 | 291 | 0.336 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 425,766 | 4.258 | 20 | 20 | fits | 118,869 | 93 | 0.483 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 405,562 | 4.056 | 20 | 24 | fits | 118,869 | 93 | 0.483 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 105,191 | 1.052 | 20 | 50 | fits | 147,053 | 291 | 0.336 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,107,793 | 11.078 | 20 | 20 | fits | 39,997 | 19 | 0.832 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 117,090 | 1.171 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 206,478 | 2.065 | 140 | 144 | fits | 49,152 | 103 | 0.310 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 226,854 | 2.269 | 140 | 144 | fits | 49,152 | 103 | 0.310 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 399,391 | 3.994 | 140 | 144 | fits | 50,611 | 109 | 0.302 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 419,800 | 4.198 | 140 | 144 | fits | 50,611 | 109 | 0.302 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 585,441 | 5.854 | 140 | 144 | fits | 47,025 | 105 | 0.269 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 605,402 | 6.054 | 140 | 144 | fits | 47,025 | 105 | 0.269 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 786,176 | 7.862 | 140 | 144 | fits | 46,355 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 806,007 | 8.060 | 140 | 144 | fits | 46,355 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 983,489 | 9.835 | 140 | 144 | fits | 41,495 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 1,000,596 | 10.006 | 140 | 144 | fits | 41,495 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 1,194,913 | 11.949 | 140 | 144 | fits | 45,159 | 104 | 0.184 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 1,214,737 | 12.147 | 140 | 144 | fits | 45,159 | 104 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 129,761 | 1.298 | 20 | 200 | fits | 125,120 | 160 | 0.320 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 431,653 | 4.317 | 20 | 20 | fits | 126,067 | 135 | 0.469 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 411,449 | 4.114 | 20 | 24 | fits | 126,067 | 135 | 0.469 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 392,178 | 3.922 | 20 | 50 | fits | 126,067 | 135 | 0.469 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,121,476 | 11.215 | 20 | 20 | fits | 44,957 | 31 | 0.808 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 97,257 | 0.973 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 612,661 | 6.127 | 140 | 144 | fits | 48,839 | 105 | 0.306 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 632,797 | 6.328 | 140 | 144 | fits | 48,839 | 105 | 0.306 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 814,561 | 8.146 | 140 | 144 | fits | 48,114 | 104 | 0.282 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 834,726 | 8.347 | 140 | 144 | fits | 48,114 | 104 | 0.282 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 212,311 | 2.123 | 140 | 144 | fits | 50,229 | 105 | 0.319 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 233,356 | 2.334 | 140 | 144 | fits | 50,229 | 105 | 0.319 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 416,637 | 4.166 | 140 | 144 | fits | 48,097 | 104 | 0.272 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 437,010 | 4.370 | 140 | 144 | fits | 48,097 | 104 | 0.272 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 1,012,547 | 10.125 | 140 | 144 | fits | 41,393 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 1,029,654 | 10.297 | 140 | 144 | fits | 41,393 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 1,224,133 | 12.241 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 1,243,957 | 12.440 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 150,335 | 1.503 | 20 | 200 | fits | 147,855 | 274 | 0.327 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 442,088 | 4.421 | 20 | 20 | fits | 128,070 | 121 | 0.487 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 421,884 | 4.219 | 20 | 24 | fits | 128,070 | 121 | 0.487 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 402,613 | 4.026 | 20 | 50 | fits | 128,070 | 121 | 0.487 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,130,022 | 11.300 | 20 | 20 | fits | 44,985 | 31 | 0.810 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 84,609 | 0.846 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 612,576 | 6.126 | 140 | 144 | fits | 48,839 | 105 | 0.306 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 632,712 | 6.327 | 140 | 144 | fits | 48,839 | 105 | 0.306 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 814,476 | 8.145 | 140 | 144 | fits | 48,114 | 104 | 0.282 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 834,641 | 8.346 | 140 | 144 | fits | 48,114 | 104 | 0.282 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 212,212 | 2.122 | 140 | 144 | fits | 50,229 | 105 | 0.319 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 233,257 | 2.333 | 140 | 144 | fits | 50,229 | 105 | 0.319 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 416,552 | 4.166 | 140 | 144 | fits | 48,097 | 104 | 0.272 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 436,925 | 4.369 | 140 | 144 | fits | 48,097 | 104 | 0.272 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 1,012,448 | 10.124 | 140 | 144 | fits | 41,393 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 1,029,555 | 10.296 | 140 | 144 | fits | 41,393 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 1,224,034 | 12.240 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 1,243,858 | 12.439 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 173,413 | 1.734 | 20 | 200 | fits | 152,553 | 292 | 0.334 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 452,823 | 4.528 | 20 | 20 | fits | 115,652 | 94 | 0.498 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 432,619 | 4.326 | 20 | 24 | fits | 115,652 | 94 | 0.498 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 113,670 | 1.137 | 20 | 50 | fits | 152,553 | 292 | 0.334 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,141,952 | 11.420 | 20 | 20 | fits | 44,921 | 31 | 0.809 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 96,278 | 0.963 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 819,671 | 8.197 | 140 | 144 | fits | 47,719 | 104 | 0.284 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 839,593 | 8.396 | 140 | 144 | fits | 47,719 | 104 | 0.284 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 217,149 | 2.171 | 140 | 144 | fits | 51,127 | 105 | 0.334 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 238,270 | 2.383 | 140 | 144 | fits | 51,127 | 105 | 0.334 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 422,009 | 4.220 | 140 | 144 | fits | 47,831 | 104 | 0.276 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 442,130 | 4.421 | 140 | 144 | fits | 47,831 | 104 | 0.276 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 617,193 | 6.172 | 140 | 144 | fits | 48,259 | 105 | 0.286 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 637,570 | 6.376 | 140 | 144 | fits | 48,259 | 105 | 0.286 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 1,017,204 | 10.172 | 140 | 144 | fits | 41,358 | 101 | 0.229 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 1,034,311 | 10.343 | 140 | 144 | fits | 41,358 | 101 | 0.229 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 1,228,776 | 12.288 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 1,248,600 | 12.486 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 158,589 | 1.586 | 20 | 200 | fits | 150,704 | 277 | 0.334 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 430,828 | 4.308 | 20 | 20 | fits | 123,203 | 116 | 0.503 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 410,624 | 4.106 | 20 | 24 | fits | 123,203 | 116 | 0.503 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 391,353 | 3.914 | 20 | 50 | fits | 123,203 | 116 | 0.503 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,118,196 | 11.182 | 20 | 20 | fits | 45,357 | 31 | 0.813 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 90,975 | 0.910 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 819,849 | 8.198 | 140 | 144 | fits | 47,719 | 104 | 0.284 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 839,771 | 8.398 | 140 | 144 | fits | 47,719 | 104 | 0.284 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 217,313 | 2.173 | 140 | 144 | fits | 51,127 | 105 | 0.334 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 238,434 | 2.384 | 140 | 144 | fits | 51,127 | 105 | 0.334 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 422,187 | 4.222 | 140 | 144 | fits | 47,831 | 104 | 0.276 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 442,308 | 4.423 | 140 | 144 | fits | 47,831 | 104 | 0.276 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 617,385 | 6.174 | 140 | 144 | fits | 48,259 | 105 | 0.286 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 637,762 | 6.378 | 140 | 144 | fits | 48,259 | 105 | 0.286 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 1,017,368 | 10.174 | 140 | 144 | fits | 41,358 | 101 | 0.229 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 1,034,475 | 10.345 | 140 | 144 | fits | 41,358 | 101 | 0.229 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 1,228,940 | 12.289 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 1,248,764 | 12.488 | 140 | 144 | fits | 45,284 | 104 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 160,622 | 1.606 | 20 | 200 | fits | 150,662 | 276 | 0.336 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 445,932 | 4.459 | 20 | 20 | fits | 122,493 | 116 | 0.496 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 425,728 | 4.257 | 20 | 24 | fits | 122,493 | 116 | 0.496 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 406,457 | 4.065 | 20 | 50 | fits | 122,493 | 116 | 0.496 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,135,605 | 11.356 | 20 | 20 | fits | 45,257 | 31 | 0.812 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 90,102 | 0.901 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 234,747 | 2.347 | 140 | 144 | fits | 49,677 | 103 | 0.327 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 255,253 | 2.553 | 140 | 144 | fits | 49,677 | 103 | 0.327 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 418,396 | 4.184 | 140 | 144 | fits | 48,662 | 104 | 0.289 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 438,563 | 4.386 | 140 | 144 | fits | 48,662 | 104 | 0.289 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 613,392 | 6.134 | 140 | 144 | fits | 47,682 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 633,430 | 6.334 | 140 | 144 | fits | 47,682 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 814,036 | 8.140 | 140 | 144 | fits | 46,400 | 104 | 0.267 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 833,867 | 8.339 | 140 | 144 | fits | 46,400 | 104 | 0.267 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 1,011,265 | 10.113 | 140 | 144 | fits | 41,472 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 1,028,372 | 10.284 | 140 | 144 | fits | 41,472 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 1,222,962 | 12.230 | 140 | 144 | fits | 45,159 | 104 | 0.184 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 1,242,786 | 12.428 | 140 | 144 | fits | 45,159 | 104 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 161,763 | 1.618 | 20 | 200 | fits | 149,657 | 281 | 0.342 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 429,105 | 4.291 | 20 | 20 | fits | 120,765 | 110 | 0.499 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 408,901 | 4.089 | 20 | 24 | fits | 120,765 | 110 | 0.499 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 389,630 | 3.896 | 20 | 50 | fits | 120,765 | 110 | 0.499 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,117,076 | 11.171 | 20 | 20 | fits | 43,191 | 25 | 0.829 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 94,258 | 0.943 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 837,690 | 8.377 | 140 | 144 | fits | 28,280 | 51 | 0.485 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,636,940 | 16.369 | 140 | 144 | fits | 51,128 | 103 | 0.372 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,658,942 | 16.589 | 140 | 144 | fits | 51,128 | 103 | 0.372 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,800,043 | 18.000 | 140 | 144 | fits | 44,403 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 204,760 | 2.048 | 140 | 144 | fits | 64,428 | 111 | 0.329 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 225,498 | 2.255 | 140 | 144 | fits | 64,428 | 111 | 0.329 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 322,024 | 3.220 | 140 | 144 | fits | 48,461 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 342,543 | 3.425 | 140 | 144 | fits | 48,461 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,818,432 | 18.184 | 140 | 144 | fits | 44,403 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,007,827 | 20.078 | 140 | 144 | fits | 42,913 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,027,671 | 20.277 | 140 | 144 | fits | 42,913 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 503,801 | 5.038 | 140 | 144 | fits | 42,695 | 61 | 0.364 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 477,544 | 4.775 | 20 | 200 | fits | 111,936 | 198 | 0.387 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 457,276 | 4.573 | 20 | 20 | fits | 111,936 | 198 | 0.387 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 296,856 | 2.969 | 20 | 24 | fits | 151,775 | 180 | 0.428 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 417,801 | 4.178 | 20 | 50 | fits | 111,936 | 198 | 0.387 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 1,035,452 | 10.355 | 20 | 20 | fits | 77,911 | 30 | 0.692 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 970,702 | 9.707 | 140 | 144 | fits | 29,743 | 51 | 0.508 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,575,167 | 15.752 | 140 | 144 | fits | 49,616 | 103 | 0.333 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,596,768 | 15.968 | 140 | 144 | fits | 49,616 | 103 | 0.333 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,719,640 | 17.196 | 140 | 144 | fits | 44,455 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 236,339 | 2.363 | 140 | 144 | fits | 49,508 | 102 | 0.314 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 257,179 | 2.572 | 140 | 144 | fits | 49,508 | 102 | 0.314 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 303,134 | 3.031 | 140 | 144 | fits | 142,096 | 118 | 0.282 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 323,413 | 3.234 | 140 | 144 | fits | 142,096 | 118 | 0.282 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,737,994 | 17.380 | 140 | 144 | fits | 44,455 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,909,520 | 19.095 | 140 | 144 | fits | 42,829 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,929,364 | 19.294 | 140 | 144 | fits | 42,829 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 733,154 | 7.332 | 140 | 144 | fits | 28,530 | 52 | 0.408 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 169,419 | 1.694 | 20 | 200 | fits | 154,010 | 288 | 0.350 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 443,253 | 4.433 | 20 | 20 | fits | 114,859 | 97 | 0.501 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 423,049 | 4.230 | 20 | 24 | fits | 114,859 | 97 | 0.501 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 109,676 | 1.097 | 20 | 50 | fits | 154,010 | 288 | 0.350 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,061,827 | 10.618 | 20 | 20 | fits | 77,911 | 30 | 0.692 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 1,426,707 | 14.267 | 140 | 144 | fits | 51,234 | 103 | 0.382 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,447,390 | 14.474 | 140 | 144 | fits | 51,234 | 103 | 0.382 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,610,266 | 16.103 | 140 | 144 | fits | 47,941 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,630,431 | 16.304 | 140 | 144 | fits | 47,941 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 251,857 | 2.519 | 140 | 144 | fits | 50,145 | 102 | 0.320 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 272,792 | 2.728 | 140 | 144 | fits | 50,145 | 102 | 0.320 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 456,203 | 4.562 | 140 | 144 | fits | 27,935 | 52 | 0.455 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 1,808,620 | 18.086 | 140 | 144 | fits | 44,279 | 103 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,826,895 | 18.269 | 140 | 144 | fits | 44,279 | 103 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,001,001 | 20.010 | 140 | 144 | fits | 43,339 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,020,608 | 20.206 | 140 | 144 | fits | 43,339 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 2,200,609 | 22.006 | 140 | 144 | fits | 25,866 | 52 | 0.306 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 156,308 | 1.563 | 20 | 200 | fits | 153,998 | 280 | 0.347 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 438,344 | 4.383 | 20 | 20 | fits | 118,940 | 107 | 0.487 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 418,140 | 4.181 | 20 | 24 | fits | 118,940 | 107 | 0.487 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 398,869 | 3.989 | 20 | 50 | fits | 118,940 | 107 | 0.487 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,023,619 | 10.236 | 20 | 20 | fits | 78,289 | 30 | 0.692 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,340,475 | 13.405 | 140 | 144 | fits | 51,026 | 102 | 0.381 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,361,123 | 13.611 | 140 | 144 | fits | 51,026 | 102 | 0.381 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,524,385 | 15.244 | 140 | 144 | fits | 48,028 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,544,544 | 15.445 | 140 | 144 | fits | 48,028 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 358,799 | 3.588 | 140 | 144 | fits | 28,464 | 52 | 0.469 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,723,456 | 17.235 | 140 | 144 | fits | 46,447 | 102 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 1,743,670 | 17.437 | 140 | 144 | fits | 46,447 | 102 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,921,684 | 19.217 | 140 | 144 | fits | 44,453 | 103 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,939,959 | 19.400 | 140 | 144 | fits | 44,453 | 103 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,118,736 | 21.187 | 140 | 144 | fits | 43,804 | 102 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,138,422 | 21.384 | 140 | 144 | fits | 43,804 | 102 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,314,373 | 23.144 | 140 | 144 | fits | 25,642 | 52 | 0.298 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 148,702 | 1.487 | 20 | 200 | fits | 148,612 | 274 | 0.326 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 438,757 | 4.388 | 20 | 20 | fits | 125,686 | 114 | 0.483 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 418,553 | 4.186 | 20 | 24 | fits | 125,686 | 114 | 0.483 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 399,282 | 3.993 | 20 | 50 | fits | 125,686 | 114 | 0.483 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,027,665 | 10.277 | 20 | 20 | fits | 78,368 | 30 | 0.692 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 573,556 | 5.736 | 140 | 144 | fits | 49,652 | 102 | 0.324 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 594,029 | 5.940 | 140 | 144 | fits | 49,652 | 102 | 0.324 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,714,990 | 17.150 | 140 | 144 | fits | 51,266 | 102 | 0.376 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,735,988 | 17.360 | 140 | 144 | fits | 51,266 | 102 | 0.376 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,824,961 | 18.250 | 140 | 144 | fits | 46,382 | 102 | 0.260 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,844,850 | 18.448 | 140 | 144 | fits | 46,382 | 102 | 0.260 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 2,022,620 | 20.226 | 140 | 144 | fits | 46,064 | 103 | 0.257 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 2,042,523 | 20.425 | 140 | 144 | fits | 46,064 | 103 | 0.257 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 2,217,639 | 22.176 | 140 | 144 | fits | 41,262 | 101 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 2,234,746 | 22.347 | 140 | 144 | fits | 41,262 | 101 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,429,153 | 24.292 | 140 | 144 | fits | 45,096 | 103 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,448,914 | 24.489 | 140 | 144 | fits | 45,096 | 103 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 157,262 | 1.573 | 20 | 200 | fits | 154,692 | 283 | 0.339 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 410,410 | 4.104 | 20 | 20 | fits | 120,813 | 114 | 0.486 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 390,206 | 3.902 | 20 | 24 | fits | 120,813 | 114 | 0.486 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 370,935 | 3.709 | 20 | 50 | fits | 120,813 | 114 | 0.486 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 991,654 | 9.917 | 20 | 20 | fits | 78,289 | 30 | 0.692 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 755,679 | 7.557 | 140 | 144 | fits | 28,809 | 52 | 0.480 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,732,095 | 17.321 | 140 | 144 | fits | 51,442 | 102 | 0.376 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,753,960 | 17.540 | 140 | 144 | fits | 51,442 | 102 | 0.376 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,916,318 | 19.163 | 140 | 144 | fits | 46,969 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,936,662 | 19.367 | 140 | 144 | fits | 46,969 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,114,937 | 21.149 | 140 | 144 | fits | 46,413 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 2,135,151 | 21.352 | 140 | 144 | fits | 46,413 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 2,312,925 | 23.129 | 140 | 144 | fits | 44,446 | 103 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,331,200 | 23.312 | 140 | 144 | fits | 44,446 | 103 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,509,869 | 25.099 | 140 | 144 | fits | 43,880 | 102 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,529,667 | 25.297 | 140 | 144 | fits | 43,880 | 102 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,723,636 | 27.236 | 140 | 144 | fits | 25,692 | 52 | 0.302 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 144,898 | 1.449 | 20 | 200 | fits | 146,759 | 274 | 0.302 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 436,008 | 4.360 | 20 | 20 | fits | 126,708 | 122 | 0.474 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 415,804 | 4.158 | 20 | 24 | fits | 126,708 | 122 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 396,533 | 3.965 | 20 | 50 | fits | 126,708 | 122 | 0.474 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,019,787 | 10.198 | 20 | 20 | fits | 78,368 | 30 | 0.692 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 768,345 | 7.683 | 140 | 144 | fits | 29,012 | 52 | 0.489 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,739,169 | 17.392 | 140 | 144 | fits | 51,578 | 102 | 0.379 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,761,034 | 17.610 | 140 | 144 | fits | 51,578 | 102 | 0.379 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,923,392 | 19.234 | 140 | 144 | fits | 46,969 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,943,736 | 19.437 | 140 | 144 | fits | 46,969 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,122,011 | 21.220 | 140 | 144 | fits | 46,413 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,142,225 | 21.422 | 140 | 144 | fits | 46,413 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,319,999 | 23.200 | 140 | 144 | fits | 44,446 | 103 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,338,274 | 23.383 | 140 | 144 | fits | 44,446 | 103 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,517,213 | 25.172 | 140 | 144 | fits | 43,820 | 102 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,537,011 | 25.370 | 140 | 144 | fits | 43,820 | 102 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,713,189 | 27.132 | 140 | 144 | fits | 25,692 | 52 | 0.302 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 155,343 | 1.553 | 20 | 200 | fits | 151,940 | 278 | 0.320 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 440,644 | 4.406 | 20 | 20 | fits | 120,723 | 113 | 0.482 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 420,440 | 4.204 | 20 | 24 | fits | 120,723 | 113 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 401,169 | 4.012 | 20 | 50 | fits | 120,723 | 113 | 0.482 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 1,024,749 | 10.247 | 20 | 20 | fits | 78,368 | 30 | 0.692 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 944,035 | 9.440 | 140 | 144 | fits | 27,288 | 52 | 0.437 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,760,847 | 17.608 | 140 | 144 | fits | 50,941 | 103 | 0.368 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,782,849 | 17.828 | 140 | 144 | fits | 50,941 | 103 | 0.368 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,924,031 | 19.240 | 140 | 144 | fits | 44,356 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 225,842 | 2.258 | 140 | 144 | fits | 64,909 | 111 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 246,608 | 2.466 | 140 | 144 | fits | 64,909 | 111 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 312,337 | 3.123 | 140 | 144 | fits | 63,609 | 112 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 332,724 | 3.327 | 140 | 144 | fits | 63,609 | 112 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,942,420 | 19.424 | 140 | 144 | fits | 44,356 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,113,746 | 21.137 | 140 | 144 | fits | 42,913 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,133,590 | 21.336 | 140 | 144 | fits | 42,913 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 765,350 | 7.654 | 140 | 144 | fits | 29,086 | 52 | 0.421 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 149,047 | 1.490 | 20 | 200 | fits | 148,555 | 275 | 0.327 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 465,132 | 4.651 | 20 | 20 | fits | 129,157 | 129 | 0.495 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 444,928 | 4.449 | 20 | 24 | fits | 129,157 | 129 | 0.495 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 425,657 | 4.257 | 20 | 50 | fits | 129,157 | 129 | 0.495 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 1,043,947 | 10.439 | 20 | 20 | fits | 77,911 | 30 | 0.692 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
