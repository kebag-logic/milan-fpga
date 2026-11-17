### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 140 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-7.held.acmp.if0` (notice-every-7) | 4.483 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-every-7.held.adp.if0` (notice-every-7) | 1.818 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-7.held.aecp.if0` (notice-every-7) | 4.281 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.maap.if0` (notice-burst-5) | 4.044 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-7.held.srp.if0` (notice-every-7) | 11.401 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 1.122 | fits | 0 srp | 4 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 27.143 (27.366) | fits | 1 events | 96 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-1 | 1537 | 0 | 156,092 (1.561) | fits |
| notice-every-3 | 1531 | 0 | 157,414 (1.574) | fits |
| notice-every-5 | 1527 | 0 | 156,216 (1.562) | fits |
| notice-every-7 | 1515 | 0 | 157,614 (1.576) | fits |
| notice-burst-1 | 1069 | 0 | 155,910 (1.559) | fits |
| notice-burst-3 | 1057 | 0 | 159,418 (1.594) | fits |
| notice-burst-5 | 1020 | 0 | 159,577 (1.596) | fits |
| notice-burst-7 | 1057 | 0 | 152,298 (1.523) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-1 | 2.298 | 140 | 16 | 2 | within |
| notice-every-1 | 2.499 | 140 | 16 | 2 | within |
| notice-every-1 | 6.281 | 140 | 16 | 2 | within |
| notice-every-1 | 6.485 | 140 | 16 | 2 | within |
| notice-every-1 | 8.287 | 140 | 16 | 2 | within |
| notice-every-1 | 8.484 | 140 | 16 | 2 | within |
| notice-every-1 | 5.177 | 140 | 16 | 2 | within |
| notice-every-1 | 5.381 | 140 | 16 | 2 | within |
| notice-every-1 | 10.251 | 140 | 16 | 2 | within |
| notice-every-1 | 10.424 | 140 | 16 | 2 | within |
| notice-every-1 | 12.183 | 140 | 16 | 2 | within |
| notice-every-1 | 12.382 | 140 | 16 | 2 | within |
| notice-every-3 | 6.330 | 140 | 16 | 2 | within |
| notice-every-3 | 6.532 | 140 | 16 | 2 | within |
| notice-every-3 | 8.150 | 140 | 16 | 2 | within |
| notice-every-3 | 8.352 | 140 | 16 | 2 | within |
| notice-every-3 | 2.109 | 140 | 16 | 2 | within |
| notice-every-3 | 2.315 | 140 | 16 | 2 | within |
| notice-every-3 | 4.146 | 140 | 16 | 2 | within |
| notice-every-3 | 4.348 | 140 | 16 | 2 | within |
| notice-every-3 | 10.126 | 140 | 16 | 2 | within |
| notice-every-3 | 10.298 | 140 | 16 | 2 | within |
| notice-every-3 | 12.239 | 140 | 16 | 2 | within |
| notice-every-3 | 12.438 | 140 | 16 | 2 | within |
| notice-every-5 | 8.199 | 140 | 16 | 2 | within |
| notice-every-5 | 8.398 | 140 | 16 | 2 | within |
| notice-every-5 | 2.392 | 140 | 16 | 2 | within |
| notice-every-5 | 2.598 | 140 | 16 | 2 | within |
| notice-every-5 | 4.228 | 140 | 16 | 2 | within |
| notice-every-5 | 4.428 | 140 | 16 | 2 | within |
| notice-every-5 | 6.177 | 140 | 16 | 2 | within |
| notice-every-5 | 6.381 | 140 | 16 | 2 | within |
| notice-every-5 | 10.170 | 140 | 16 | 2 | within |
| notice-every-5 | 10.343 | 140 | 16 | 2 | within |
| notice-every-5 | 12.283 | 140 | 16 | 2 | within |
| notice-every-5 | 12.482 | 140 | 16 | 2 | within |
| notice-every-7 | 7.896 | 140 | 16 | 2 | within |
| notice-every-7 | 8.095 | 140 | 16 | 2 | within |
| notice-every-7 | 1.891 | 140 | 16 | 2 | within |
| notice-every-7 | 2.096 | 140 | 16 | 2 | within |
| notice-every-7 | 3.838 | 140 | 16 | 2 | within |
| notice-every-7 | 4.040 | 140 | 16 | 2 | within |
| notice-every-7 | 5.876 | 140 | 16 | 2 | within |
| notice-every-7 | 6.077 | 140 | 16 | 2 | within |
| notice-every-7 | 9.867 | 140 | 16 | 2 | within |
| notice-every-7 | 10.040 | 140 | 16 | 2 | within |
| notice-every-7 | 11.980 | 140 | 16 | 2 | within |
| notice-every-7 | 12.179 | 140 | 16 | 2 | within |
| notice-burst-1 | 8.843 | 140 | 16 | 1 | within |
| notice-burst-1 | 15.934 | 140 | 16 | 1 | within |
| notice-burst-1 | 16.152 | 140 | 16 | 1 | within |
| notice-burst-1 | 17.211 | 140 | 16 | 1 | within |
| notice-burst-1 | 2.219 | 140 | 16 | 1 | within |
| notice-burst-1 | 2.423 | 140 | 16 | 1 | within |
| notice-burst-1 | 2.668 | 140 | 16 | 1 | within |
| notice-burst-1 | 2.869 | 140 | 16 | 1 | within |
| notice-burst-1 | 17.397 | 140 | 16 | 1 | within |
| notice-burst-1 | 19.289 | 140 | 16 | 1 | within |
| notice-burst-1 | 19.486 | 140 | 16 | 1 | within |
| notice-burst-1 | 5.879 | 140 | 16 | 1 | within |
| notice-burst-3 | 13.316 | 140 | 16 | 0 | within |
| notice-burst-3 | 13.520 | 140 | 16 | 0 | within |
| notice-burst-3 | 14.964 | 140 | 16 | 0 | within |
| notice-burst-3 | 15.167 | 140 | 16 | 0 | within |
| notice-burst-3 | 3.559 | 140 | 16 | 0 | within |
| notice-burst-3 | 16.951 | 140 | 16 | 0 | within |
| notice-burst-3 | 17.152 | 140 | 16 | 0 | within |
| notice-burst-3 | 18.926 | 140 | 16 | 0 | within |
| notice-burst-3 | 19.109 | 140 | 16 | 0 | within |
| notice-burst-3 | 20.900 | 140 | 16 | 0 | within |
| notice-burst-3 | 21.097 | 140 | 16 | 0 | within |
| notice-burst-3 | 23.036 | 140 | 16 | 0 | within |
| notice-burst-5 | 7.620 | 140 | 16 | 1 | within |
| notice-burst-5 | 17.411 | 140 | 16 | 1 | within |
| notice-burst-5 | 17.629 | 140 | 16 | 1 | within |
| notice-burst-5 | 19.066 | 140 | 16 | 1 | within |
| notice-burst-5 | 19.269 | 140 | 16 | 1 | within |
| notice-burst-5 | 21.053 | 140 | 16 | 1 | within |
| notice-burst-5 | 21.253 | 140 | 16 | 1 | within |
| notice-burst-5 | 23.210 | 140 | 16 | 1 | within |
| notice-burst-5 | 23.394 | 140 | 16 | 1 | within |
| notice-burst-5 | 25.185 | 140 | 16 | 1 | within |
| notice-burst-5 | 25.383 | 140 | 16 | 1 | within |
| notice-burst-5 | 27.143 | 140 | 16 | 1 | within |
| notice-burst-7 | 9.330 | 140 | 16 | 1 | within |
| notice-burst-7 | 17.439 | 140 | 16 | 1 | within |
| notice-burst-7 | 17.657 | 140 | 16 | 1 | within |
| notice-burst-7 | 19.241 | 140 | 16 | 1 | within |
| notice-burst-7 | 2.222 | 140 | 16 | 1 | within |
| notice-burst-7 | 2.425 | 140 | 16 | 1 | within |
| notice-burst-7 | 2.672 | 140 | 16 | 1 | within |
| notice-burst-7 | 2.874 | 140 | 16 | 1 | within |
| notice-burst-7 | 19.427 | 140 | 16 | 1 | within |
| notice-burst-7 | 21.141 | 140 | 16 | 1 | within |
| notice-burst-7 | 21.338 | 140 | 16 | 1 | within |
| notice-burst-7 | 3.579 | 140 | 16 | 1 | within |

Latest: 27.143 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-1 | 307 | 123,777 (1.238) | 76,244 (0.762) |
| notice-every-3 | 307 | 101,711 (1.017) | 76,244 (0.762) |
| notice-every-5 | 307 | 91,589 (0.916) | 75,718 (0.757) |
| notice-every-7 | 307 | 91,589 (0.916) | 75,718 (0.757) |
| notice-burst-1 | 317 | 103,454 (1.035) | 78,048 (0.780) |
| notice-burst-3 | 317 | 101,711 (1.017) | 77,969 (0.780) |
| notice-burst-5 | 317 | 101,389 (1.014) | 78,048 (0.780) |
| notice-burst-7 | 317 | 100,648 (1.006) | 77,969 (0.780) |

Longest pass that carries a step: 123,777 CPU cycles (1.238 ms), notice-every-1; longest step: 78,048 (0.780 ms), notice-burst-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 229,804 | 2.298 | 140 | 144 | fits | 49,015 | 103 | 0.306 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 249,902 | 2.499 | 140 | 144 | fits | 49,015 | 103 | 0.306 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 628,143 | 6.281 | 140 | 144 | fits | 48,239 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 648,452 | 6.485 | 140 | 144 | fits | 48,239 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 828,688 | 8.287 | 140 | 144 | fits | 45,923 | 102 | 0.258 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 848,438 | 8.484 | 140 | 144 | fits | 45,923 | 102 | 0.258 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 517,694 | 5.177 | 140 | 144 | fits | 123,777 | 102 | 0.225 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 538,091 | 5.381 | 140 | 144 | fits | 123,777 | 102 | 0.225 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 1,025,140 | 10.251 | 140 | 144 | fits | 41,045 | 101 | 0.226 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 1,042,368 | 10.424 | 140 | 144 | fits | 41,045 | 101 | 0.226 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 1,218,296 | 12.183 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 1,238,172 | 12.382 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 181,238 | 1.812 | 20 | 200 | fits | 152,713 | 297 | 0.320 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 442,601 | 4.426 | 20 | 20 | fits | 116,440 | 92 | 0.511 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 422,397 | 4.224 | 20 | 24 | fits | 116,440 | 92 | 0.511 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 121,495 | 1.215 | 20 | 50 | fits | 152,713 | 297 | 0.320 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,121,835 | 11.218 | 20 | 20 | fits | 41,961 | 25 | 0.804 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 112,161 | 1.122 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 633,017 | 6.330 | 140 | 144 | fits | 48,504 | 103 | 0.300 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 653,199 | 6.532 | 140 | 144 | fits | 48,504 | 103 | 0.300 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 814,973 | 8.150 | 140 | 144 | fits | 48,069 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 835,233 | 8.352 | 140 | 144 | fits | 48,069 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 210,921 | 2.109 | 140 | 144 | fits | 49,242 | 105 | 0.294 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 231,481 | 2.315 | 140 | 144 | fits | 49,242 | 105 | 0.294 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 414,566 | 4.146 | 140 | 144 | fits | 47,663 | 104 | 0.261 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 434,778 | 4.348 | 140 | 144 | fits | 47,663 | 104 | 0.261 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 1,012,587 | 10.126 | 140 | 144 | fits | 41,102 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 1,029,815 | 10.298 | 140 | 144 | fits | 41,102 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 1,223,882 | 12.239 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 1,243,758 | 12.438 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 179,926 | 1.799 | 20 | 200 | fits | 152,696 | 300 | 0.317 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 446,108 | 4.461 | 20 | 20 | fits | 116,888 | 92 | 0.519 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 425,904 | 4.259 | 20 | 24 | fits | 116,888 | 92 | 0.519 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 120,183 | 1.202 | 20 | 50 | fits | 152,696 | 300 | 0.317 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,138,180 | 11.382 | 20 | 20 | fits | 45,455 | 31 | 0.813 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 92,364 | 0.924 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 819,903 | 8.199 | 140 | 144 | fits | 47,728 | 104 | 0.284 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 839,837 | 8.398 | 140 | 144 | fits | 47,728 | 104 | 0.284 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 239,207 | 2.392 | 140 | 144 | fits | 50,102 | 103 | 0.304 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 259,815 | 2.598 | 140 | 144 | fits | 50,102 | 103 | 0.304 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 422,790 | 4.228 | 140 | 144 | fits | 47,301 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 442,771 | 4.428 | 140 | 144 | fits | 47,301 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 617,684 | 6.177 | 140 | 144 | fits | 47,907 | 105 | 0.277 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 638,066 | 6.381 | 140 | 144 | fits | 47,907 | 105 | 0.277 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 1,017,013 | 10.170 | 140 | 144 | fits | 41,153 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 1,034,292 | 10.343 | 140 | 144 | fits | 41,153 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 1,228,345 | 12.283 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 1,248,221 | 12.482 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 175,618 | 1.756 | 20 | 200 | fits | 152,611 | 298 | 0.318 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 444,557 | 4.446 | 20 | 20 | fits | 117,555 | 94 | 0.525 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 424,353 | 4.244 | 20 | 24 | fits | 117,555 | 94 | 0.525 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 115,875 | 1.159 | 20 | 50 | fits | 152,611 | 298 | 0.318 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,135,809 | 11.358 | 20 | 20 | fits | 45,992 | 31 | 0.818 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 90,170 | 0.902 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 789,592 | 7.896 | 140 | 144 | fits | 47,728 | 104 | 0.284 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 809,526 | 8.095 | 140 | 144 | fits | 47,728 | 104 | 0.284 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 189,075 | 1.891 | 140 | 144 | fits | 50,037 | 105 | 0.294 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 209,623 | 2.096 | 140 | 144 | fits | 50,037 | 105 | 0.294 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 383,803 | 3.838 | 140 | 144 | fits | 49,435 | 109 | 0.278 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 404,034 | 4.040 | 140 | 144 | fits | 49,435 | 109 | 0.278 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 587,574 | 5.876 | 140 | 144 | fits | 47,066 | 105 | 0.253 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 607,706 | 6.077 | 140 | 144 | fits | 47,066 | 105 | 0.253 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 986,741 | 9.867 | 140 | 144 | fits | 41,153 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 1,004,020 | 10.040 | 140 | 144 | fits | 41,153 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 1,198,050 | 11.980 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 1,217,926 | 12.179 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 181,764 | 1.818 | 20 | 200 | fits | 152,790 | 301 | 0.318 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 448,320 | 4.483 | 20 | 20 | fits | 117,100 | 94 | 0.519 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 428,116 | 4.281 | 20 | 24 | fits | 117,100 | 94 | 0.519 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 122,021 | 1.220 | 20 | 50 | fits | 152,790 | 301 | 0.318 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,140,100 | 11.401 | 20 | 20 | fits | 43,643 | 25 | 0.830 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 83,458 | 0.835 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 884,335 | 8.843 | 140 | 144 | fits | 28,258 | 51 | 0.469 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,593,418 | 15.934 | 140 | 144 | fits | 50,231 | 103 | 0.358 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,615,237 | 16.152 | 140 | 144 | fits | 50,231 | 103 | 0.358 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,721,133 | 17.211 | 140 | 144 | fits | 44,248 | 102 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 221,923 | 2.219 | 140 | 144 | fits | 63,230 | 111 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 242,264 | 2.423 | 140 | 144 | fits | 63,230 | 111 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 266,798 | 2.668 | 140 | 144 | fits | 44,437 | 103 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 286,949 | 2.869 | 140 | 144 | fits | 44,437 | 103 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,739,685 | 17.397 | 140 | 144 | fits | 44,248 | 102 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,928,866 | 19.289 | 140 | 144 | fits | 42,648 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,948,575 | 19.486 | 140 | 144 | fits | 42,648 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 587,878 | 5.879 | 140 | 144 | fits | 28,641 | 52 | 0.427 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 168,811 | 1.688 | 20 | 200 | fits | 149,366 | 287 | 0.321 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 445,201 | 4.452 | 20 | 20 | fits | 112,107 | 82 | 0.526 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 424,997 | 4.250 | 20 | 24 | fits | 112,107 | 82 | 0.526 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 109,068 | 1.091 | 20 | 50 | fits | 149,366 | 287 | 0.321 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,092,653 | 10.927 | 20 | 20 | fits | 39,019 | 18 | 0.827 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,331,611 | 13.316 | 140 | 144 | fits | 50,792 | 102 | 0.373 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,352,008 | 13.520 | 140 | 144 | fits | 50,792 | 102 | 0.373 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,496,420 | 14.964 | 140 | 144 | fits | 48,187 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,516,654 | 15.167 | 140 | 144 | fits | 48,187 | 103 | 0.277 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 355,925 | 3.559 | 140 | 144 | fits | 28,093 | 52 | 0.460 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,695,120 | 16.951 | 140 | 144 | fits | 45,665 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 1,715,202 | 17.152 | 140 | 144 | fits | 45,665 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,892,610 | 18.926 | 140 | 144 | fits | 43,696 | 103 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,910,888 | 19.109 | 140 | 144 | fits | 43,696 | 103 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,089,956 | 20.900 | 140 | 144 | fits | 43,785 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,109,679 | 21.097 | 140 | 144 | fits | 43,785 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,303,587 | 23.036 | 140 | 144 | fits | 25,233 | 52 | 0.294 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 162,448 | 1.624 | 20 | 200 | fits | 149,928 | 288 | 0.315 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 444,532 | 4.445 | 20 | 20 | fits | 114,841 | 85 | 0.517 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 424,328 | 4.243 | 20 | 24 | fits | 114,841 | 85 | 0.517 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 102,705 | 1.027 | 20 | 50 | fits | 149,928 | 288 | 0.315 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,035,292 | 10.353 | 20 | 20 | fits | 79,135 | 30 | 0.681 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 761,958 | 7.620 | 140 | 144 | fits | 28,918 | 52 | 0.485 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,741,067 | 17.411 | 140 | 144 | fits | 50,868 | 102 | 0.374 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,762,861 | 17.629 | 140 | 144 | fits | 50,868 | 102 | 0.374 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,906,614 | 19.066 | 140 | 144 | fits | 46,588 | 103 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,926,902 | 19.269 | 140 | 144 | fits | 46,588 | 103 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,105,306 | 21.053 | 140 | 144 | fits | 45,647 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 2,125,321 | 21.253 | 140 | 144 | fits | 45,647 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 2,321,040 | 23.210 | 140 | 144 | fits | 43,964 | 103 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,339,400 | 23.394 | 140 | 144 | fits | 43,964 | 103 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,518,529 | 25.185 | 140 | 144 | fits | 43,785 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,538,252 | 25.383 | 140 | 144 | fits | 43,785 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,714,264 | 27.143 | 140 | 144 | fits | 25,233 | 52 | 0.294 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 153,046 | 1.530 | 20 | 200 | fits | 150,181 | 280 | 0.295 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 443,867 | 4.439 | 20 | 20 | fits | 122,594 | 109 | 0.522 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 423,663 | 4.237 | 20 | 24 | fits | 122,594 | 109 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 404,392 | 4.044 | 20 | 50 | fits | 122,594 | 109 | 0.522 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,031,383 | 10.314 | 20 | 20 | fits | 79,048 | 30 | 0.680 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 933,014 | 9.330 | 140 | 144 | fits | 28,088 | 52 | 0.474 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,743,894 | 17.439 | 140 | 144 | fits | 50,461 | 103 | 0.365 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,765,730 | 17.657 | 140 | 144 | fits | 50,461 | 103 | 0.365 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,924,125 | 19.241 | 140 | 144 | fits | 44,219 | 102 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 222,206 | 2.222 | 140 | 144 | fits | 63,319 | 111 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 242,547 | 2.425 | 140 | 144 | fits | 63,319 | 111 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 267,235 | 2.672 | 140 | 144 | fits | 44,591 | 103 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 287,386 | 2.874 | 140 | 144 | fits | 44,591 | 103 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,942,677 | 19.427 | 140 | 144 | fits | 44,219 | 102 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,114,062 | 21.141 | 140 | 144 | fits | 42,648 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,133,771 | 21.338 | 140 | 144 | fits | 42,648 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 357,866 | 3.579 | 140 | 144 | fits | 42,840 | 60 | 0.369 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 160,942 | 1.609 | 20 | 200 | fits | 149,330 | 286 | 0.313 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 439,313 | 4.393 | 20 | 20 | fits | 118,253 | 100 | 0.527 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 419,109 | 4.191 | 20 | 24 | fits | 118,253 | 100 | 0.527 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 101,199 | 1.012 | 20 | 50 | fits | 149,330 | 286 | 0.313 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 1,023,314 | 10.233 | 20 | 20 | fits | 78,761 | 30 | 0.682 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
