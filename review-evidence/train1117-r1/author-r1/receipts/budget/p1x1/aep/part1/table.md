### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 140 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.acmp.if0` (notice-every-5) | 5.780 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.adp.if0` (notice-burst-5) | 5.193 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-3.held.aecp.if0` (notice-every-3) | 4.606 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.maap.if0` (notice-burst-5) | 4.596 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.srp.if0` (notice-every-5) | 11.971 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 1.001 | fits | 0 srp | 4 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-7.notices.29.9.0.if0` (notice-burst-7) | 23.297 (23.532) | fits | 1 events | 96 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-1 | 1509 | 0 | 155,270 (1.553) | fits |
| notice-every-3 | 1504 | 0 | 157,777 (1.578) | fits |
| notice-every-5 | 1509 | 0 | 155,058 (1.551) | fits |
| notice-every-7 | 1502 | 0 | 155,004 (1.550) | fits |
| notice-burst-1 | 1039 | 0 | 156,011 (1.560) | fits |
| notice-burst-3 | 1005 | 0 | 157,268 (1.573) | fits |
| notice-burst-5 | 1078 | 0 | 158,999 (1.590) | fits |
| notice-burst-7 | 1080 | 0 | 154,552 (1.546) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-1 | 4.163 | 140 | 16 | 2 | within |
| notice-every-1 | 4.340 | 140 | 16 | 2 | within |
| notice-every-1 | 6.137 | 140 | 16 | 2 | within |
| notice-every-1 | 6.316 | 140 | 16 | 2 | within |
| notice-every-1 | 8.184 | 140 | 16 | 2 | within |
| notice-every-1 | 8.363 | 140 | 16 | 2 | within |
| notice-every-1 | 2.266 | 140 | 16 | 2 | within |
| notice-every-1 | 2.454 | 140 | 16 | 2 | within |
| notice-every-1 | 10.208 | 140 | 16 | 2 | within |
| notice-every-1 | 10.341 | 140 | 16 | 2 | within |
| notice-every-1 | 12.163 | 140 | 16 | 2 | within |
| notice-every-1 | 12.333 | 140 | 16 | 2 | within |
| notice-every-3 | 6.145 | 140 | 16 | 2 | within |
| notice-every-3 | 6.324 | 140 | 16 | 2 | within |
| notice-every-3 | 8.200 | 140 | 16 | 2 | within |
| notice-every-3 | 8.376 | 140 | 16 | 2 | within |
| notice-every-3 | 2.260 | 140 | 16 | 2 | within |
| notice-every-3 | 2.447 | 140 | 16 | 2 | within |
| notice-every-3 | 4.150 | 140 | 16 | 2 | within |
| notice-every-3 | 4.334 | 140 | 16 | 2 | within |
| notice-every-3 | 10.204 | 140 | 16 | 2 | within |
| notice-every-3 | 10.337 | 140 | 16 | 2 | within |
| notice-every-3 | 12.157 | 140 | 16 | 2 | within |
| notice-every-3 | 12.328 | 140 | 16 | 2 | within |
| notice-every-5 | 8.136 | 140 | 16 | 1 | within |
| notice-every-5 | 8.311 | 140 | 16 | 1 | within |
| notice-every-5 | 2.155 | 140 | 16 | 1 | within |
| notice-every-5 | 2.335 | 140 | 16 | 1 | within |
| notice-every-5 | 4.031 | 140 | 16 | 1 | within |
| notice-every-5 | 4.214 | 140 | 16 | 1 | within |
| notice-every-5 | 6.020 | 140 | 16 | 1 | within |
| notice-every-5 | 6.204 | 140 | 16 | 1 | within |
| notice-every-5 | 9.943 | 140 | 16 | 1 | within |
| notice-every-5 | 10.076 | 140 | 16 | 1 | within |
| notice-every-5 | 11.908 | 140 | 16 | 1 | within |
| notice-every-5 | 12.078 | 140 | 16 | 1 | within |
| notice-every-7 | 8.005 | 140 | 16 | 2 | within |
| notice-every-7 | 8.180 | 140 | 16 | 2 | within |
| notice-every-7 | 2.024 | 140 | 16 | 2 | within |
| notice-every-7 | 2.202 | 140 | 16 | 2 | within |
| notice-every-7 | 3.797 | 140 | 16 | 2 | within |
| notice-every-7 | 3.981 | 140 | 16 | 2 | within |
| notice-every-7 | 5.882 | 140 | 16 | 2 | within |
| notice-every-7 | 6.064 | 140 | 16 | 2 | within |
| notice-every-7 | 9.803 | 140 | 16 | 2 | within |
| notice-every-7 | 9.936 | 140 | 16 | 2 | within |
| notice-every-7 | 11.951 | 140 | 16 | 2 | within |
| notice-every-7 | 12.122 | 140 | 16 | 2 | within |
| notice-burst-1 | 15.292 | 140 | 16 | 1 | within |
| notice-burst-1 | 15.471 | 140 | 16 | 1 | within |
| notice-burst-1 | 17.135 | 140 | 16 | 1 | within |
| notice-burst-1 | 17.313 | 140 | 16 | 1 | within |
| notice-burst-1 | 3.206 | 140 | 16 | 1 | within |
| notice-burst-1 | 3.395 | 140 | 16 | 1 | within |
| notice-burst-1 | 3.622 | 140 | 16 | 1 | within |
| notice-burst-1 | 3.801 | 140 | 16 | 1 | within |
| notice-burst-1 | 19.133 | 140 | 16 | 1 | within |
| notice-burst-1 | 19.266 | 140 | 16 | 1 | within |
| notice-burst-1 | 21.093 | 140 | 16 | 1 | within |
| notice-burst-1 | 21.263 | 140 | 16 | 1 | within |
| notice-burst-3 | 13.472 | 140 | 16 | 0 | within |
| notice-burst-3 | 13.653 | 140 | 16 | 0 | within |
| notice-burst-3 | 14.939 | 140 | 16 | 0 | within |
| notice-burst-3 | 15.116 | 140 | 16 | 0 | within |
| notice-burst-3 | 3.525 | 140 | 16 | 0 | within |
| notice-burst-3 | 16.977 | 140 | 16 | 0 | within |
| notice-burst-3 | 17.149 | 140 | 16 | 0 | within |
| notice-burst-3 | 19.003 | 140 | 16 | 0 | within |
| notice-burst-3 | 19.154 | 140 | 16 | 0 | within |
| notice-burst-3 | 20.811 | 140 | 16 | 0 | within |
| notice-burst-3 | 20.982 | 140 | 16 | 0 | within |
| notice-burst-3 | 22.981 | 140 | 16 | 0 | within |
| notice-burst-5 | 4.918 | 140 | 16 | 0 | within |
| notice-burst-5 | 5.096 | 140 | 16 | 0 | within |
| notice-burst-5 | 16.866 | 140 | 16 | 0 | within |
| notice-burst-5 | 17.048 | 140 | 16 | 0 | within |
| notice-burst-5 | 17.939 | 140 | 16 | 0 | within |
| notice-burst-5 | 18.118 | 140 | 16 | 0 | within |
| notice-burst-5 | 19.975 | 140 | 16 | 0 | within |
| notice-burst-5 | 20.150 | 140 | 16 | 0 | within |
| notice-burst-5 | 5.316 | 140 | 16 | 0 | within |
| notice-burst-5 | 5.456 | 140 | 16 | 0 | within |
| notice-burst-5 | 22.000 | 140 | 16 | 0 | within |
| notice-burst-5 | 22.171 | 140 | 16 | 0 | within |
| notice-burst-7 | 9.319 | 140 | 16 | 1 | within |
| notice-burst-7 | 17.694 | 140 | 16 | 1 | within |
| notice-burst-7 | 17.871 | 140 | 16 | 1 | within |
| notice-burst-7 | 19.148 | 140 | 16 | 1 | within |
| notice-burst-7 | 19.319 | 140 | 16 | 1 | within |
| notice-burst-7 | 21.172 | 140 | 16 | 1 | within |
| notice-burst-7 | 3.293 | 140 | 16 | 1 | within |
| notice-burst-7 | 3.479 | 140 | 16 | 1 | within |
| notice-burst-7 | 21.326 | 140 | 16 | 1 | within |
| notice-burst-7 | 23.126 | 140 | 16 | 1 | within |
| notice-burst-7 | 23.297 | 140 | 16 | 1 | within |
| notice-burst-7 | 5.187 | 140 | 16 | 1 | within |

Latest: 23.297 ms, notice-burst-7.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-1 | 402 | 96,652 (0.967) | 78,332 (0.783) |
| notice-every-3 | 402 | 96,652 (0.967) | 78,332 (0.783) |
| notice-every-5 | 402 | 96,652 (0.967) | 78,332 (0.783) |
| notice-every-7 | 402 | 96,652 (0.967) | 78,332 (0.783) |
| notice-burst-1 | 412 | 96,652 (0.967) | 78,332 (0.783) |
| notice-burst-3 | 412 | 96,652 (0.967) | 78,332 (0.783) |
| notice-burst-5 | 412 | 96,652 (0.967) | 78,332 (0.783) |
| notice-burst-7 | 412 | 96,652 (0.967) | 78,332 (0.783) |

Longest pass that carries a step: 96,652 CPU cycles (0.967 ms), notice-every-1; longest step: 78,332 (0.783 ms), notice-every-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 416,310 | 4.163 | 140 | 144 | fits | 43,334 | 104 | 0.281 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 433,964 | 4.340 | 140 | 144 | fits | 43,334 | 104 | 0.281 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 613,745 | 6.137 | 140 | 144 | fits | 43,105 | 105 | 0.276 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 631,618 | 6.316 | 140 | 144 | fits | 43,105 | 105 | 0.276 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 818,405 | 8.184 | 140 | 144 | fits | 42,505 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 836,321 | 8.363 | 140 | 144 | fits | 42,505 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 226,575 | 2.266 | 140 | 144 | fits | 44,859 | 103 | 0.280 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 245,353 | 2.454 | 140 | 144 | fits | 44,859 | 103 | 0.280 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 1,020,758 | 10.208 | 140 | 144 | fits | 34,492 | 101 | 0.239 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 1,034,119 | 10.341 | 140 | 144 | fits | 34,492 | 101 | 0.239 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 1,216,264 | 12.163 | 140 | 144 | fits | 39,824 | 104 | 0.161 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 1,233,319 | 12.333 | 140 | 144 | fits | 39,824 | 104 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 141,751 | 1.418 | 20 | 200 | fits | 135,005 | 154 | 0.359 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 548,087 | 5.481 | 20 | 20 | fits | 92,039 | 42 | 0.768 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 435,844 | 4.358 | 20 | 24 | fits | 149,358 | 142 | 0.484 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 416,573 | 4.166 | 20 | 50 | fits | 149,358 | 142 | 0.484 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,171,136 | 11.711 | 20 | 20 | fits | 40,214 | 19 | 0.822 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 100,125 | 1.001 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 614,528 | 6.145 | 140 | 144 | fits | 43,672 | 105 | 0.300 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 632,428 | 6.324 | 140 | 144 | fits | 43,672 | 105 | 0.300 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 819,962 | 8.200 | 140 | 144 | fits | 42,042 | 102 | 0.261 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 837,623 | 8.376 | 140 | 144 | fits | 42,042 | 102 | 0.261 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 226,028 | 2.260 | 140 | 144 | fits | 45,028 | 103 | 0.280 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 244,675 | 2.447 | 140 | 144 | fits | 45,028 | 103 | 0.280 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 415,026 | 4.150 | 140 | 144 | fits | 43,368 | 104 | 0.249 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 433,351 | 4.334 | 140 | 144 | fits | 43,368 | 104 | 0.249 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 1,020,394 | 10.204 | 140 | 144 | fits | 34,200 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 1,033,695 | 10.337 | 140 | 144 | fits | 34,200 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 1,215,734 | 12.157 | 140 | 144 | fits | 39,809 | 104 | 0.161 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 1,232,789 | 12.328 | 140 | 144 | fits | 39,809 | 104 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 173,145 | 1.731 | 20 | 200 | fits | 152,485 | 252 | 0.400 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 480,764 | 4.808 | 20 | 20 | fits | 140,377 | 130 | 0.489 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 460,560 | 4.606 | 20 | 24 | fits | 140,377 | 130 | 0.489 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 441,289 | 4.413 | 20 | 50 | fits | 140,377 | 130 | 0.489 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,181,921 | 11.819 | 20 | 20 | fits | 40,097 | 19 | 0.821 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 92,376 | 0.924 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 813,635 | 8.136 | 140 | 144 | fits | 42,031 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 831,135 | 8.311 | 140 | 144 | fits | 42,031 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 215,462 | 2.155 | 140 | 144 | fits | 44,130 | 103 | 0.293 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 233,488 | 2.335 | 140 | 144 | fits | 44,130 | 103 | 0.293 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 403,060 | 4.031 | 140 | 144 | fits | 43,703 | 102 | 0.259 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 421,377 | 4.214 | 140 | 144 | fits | 43,703 | 102 | 0.259 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 602,010 | 6.020 | 140 | 144 | fits | 42,762 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 620,350 | 6.204 | 140 | 144 | fits | 42,762 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 994,315 | 9.943 | 140 | 144 | fits | 34,164 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 1,007,616 | 10.076 | 140 | 144 | fits | 34,164 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 1,190,752 | 11.908 | 140 | 144 | fits | 39,842 | 104 | 0.163 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 1,207,807 | 12.078 | 140 | 144 | fits | 39,842 | 104 | 0.163 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 172,711 | 1.727 | 20 | 200 | fits | 150,241 | 247 | 0.396 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 578,023 | 5.780 | 20 | 20 | fits | 83,377 | 50 | 0.783 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 459,323 | 4.593 | 20 | 24 | fits | 147,478 | 133 | 0.504 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 440,052 | 4.401 | 20 | 50 | fits | 147,478 | 133 | 0.504 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,197,137 | 11.971 | 20 | 20 | fits | 54,229 | 23 | 0.773 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 86,730 | 0.867 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 800,501 | 8.005 | 140 | 144 | fits | 42,159 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 818,001 | 8.180 | 140 | 144 | fits | 42,159 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 202,423 | 2.024 | 140 | 144 | fits | 43,630 | 103 | 0.278 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 220,194 | 2.202 | 140 | 144 | fits | 43,630 | 103 | 0.278 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 379,658 | 3.797 | 140 | 144 | fits | 44,244 | 104 | 0.271 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 398,115 | 3.981 | 140 | 144 | fits | 44,244 | 104 | 0.271 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 588,200 | 5.882 | 140 | 144 | fits | 42,493 | 103 | 0.252 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 606,400 | 6.064 | 140 | 144 | fits | 42,493 | 103 | 0.252 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 980,315 | 9.803 | 140 | 144 | fits | 34,216 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 993,616 | 9.936 | 140 | 144 | fits | 34,216 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 1,195,131 | 11.951 | 140 | 144 | fits | 39,795 | 104 | 0.159 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 1,212,186 | 12.122 | 140 | 144 | fits | 39,795 | 104 | 0.159 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 495,689 | 4.957 | 20 | 200 | fits | 149,808 | 234 | 0.398 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 475,421 | 4.754 | 20 | 20 | fits | 149,808 | 234 | 0.398 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 336,917 | 3.369 | 20 | 24 | fits | 82,798 | 60 | 0.499 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 435,946 | 4.359 | 20 | 50 | fits | 149,808 | 234 | 0.398 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,182,680 | 11.827 | 20 | 20 | fits | 40,191 | 19 | 0.821 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 97,398 | 0.974 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 1,529,176 | 15.292 | 140 | 144 | fits | 44,734 | 102 | 0.352 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,547,147 | 15.471 | 140 | 144 | fits | 44,734 | 102 | 0.352 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,713,529 | 17.135 | 140 | 144 | fits | 42,108 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,731,262 | 17.313 | 140 | 144 | fits | 42,108 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 320,624 | 3.206 | 140 | 144 | fits | 60,413 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 339,452 | 3.395 | 140 | 144 | fits | 60,413 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 362,178 | 3.622 | 140 | 144 | fits | 39,986 | 103 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 380,112 | 3.801 | 140 | 144 | fits | 39,986 | 103 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,913,262 | 19.133 | 140 | 144 | fits | 34,484 | 101 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,926,563 | 19.266 | 140 | 144 | fits | 34,484 | 101 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 2,109,312 | 21.093 | 140 | 144 | fits | 39,708 | 103 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 2,126,295 | 21.263 | 140 | 144 | fits | 39,708 | 103 | 0.159 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 152,767 | 1.528 | 20 | 200 | fits | 156,011 | 247 | 0.394 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 424,817 | 4.248 | 20 | 20 | fits | 140,935 | 140 | 0.472 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 404,613 | 4.046 | 20 | 24 | fits | 140,935 | 140 | 0.472 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 385,342 | 3.853 | 20 | 50 | fits | 140,935 | 140 | 0.472 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,016,177 | 10.162 | 20 | 20 | fits | 79,021 | 30 | 0.675 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,347,206 | 13.472 | 140 | 144 | fits | 45,041 | 102 | 0.352 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,365,302 | 13.653 | 140 | 144 | fits | 45,041 | 102 | 0.352 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,493,866 | 14.939 | 140 | 144 | fits | 42,007 | 103 | 0.256 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,511,610 | 15.116 | 140 | 144 | fits | 42,007 | 103 | 0.256 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 352,462 | 3.525 | 140 | 144 | fits | 26,638 | 52 | 0.485 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,697,711 | 16.977 | 140 | 144 | fits | 41,153 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 1,714,887 | 17.149 | 140 | 144 | fits | 41,153 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,900,318 | 19.003 | 140 | 144 | fits | 38,773 | 103 | 0.222 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,915,428 | 19.154 | 140 | 144 | fits | 38,773 | 103 | 0.222 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,081,070 | 20.811 | 140 | 144 | fits | 37,090 | 102 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,098,230 | 20.982 | 140 | 144 | fits | 37,090 | 102 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,298,138 | 22.981 | 140 | 144 | fits | 22,703 | 52 | 0.262 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 164,389 | 1.644 | 20 | 200 | fits | 149,785 | 247 | 0.395 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 465,323 | 4.653 | 20 | 20 | fits | 137,296 | 117 | 0.500 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 445,119 | 4.451 | 20 | 24 | fits | 137,296 | 117 | 0.500 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 425,848 | 4.258 | 20 | 50 | fits | 137,296 | 117 | 0.500 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,056,466 | 10.565 | 20 | 20 | fits | 79,160 | 30 | 0.675 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 491,822 | 4.918 | 140 | 144 | fits | 59,083 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 509,568 | 5.096 | 140 | 144 | fits | 59,083 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,686,554 | 16.866 | 140 | 144 | fits | 45,099 | 102 | 0.349 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,704,765 | 17.048 | 140 | 144 | fits | 45,099 | 102 | 0.349 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,793,868 | 17.939 | 140 | 144 | fits | 42,043 | 102 | 0.253 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,811,784 | 18.118 | 140 | 144 | fits | 42,043 | 102 | 0.253 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,997,459 | 19.975 | 140 | 144 | fits | 40,874 | 103 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 2,015,036 | 20.150 | 140 | 144 | fits | 40,874 | 103 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 531,588 | 5.316 | 140 | 144 | fits | 35,036 | 101 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 545,646 | 5.456 | 140 | 144 | fits | 35,036 | 101 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,200,016 | 22.000 | 140 | 144 | fits | 39,952 | 103 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,217,080 | 22.171 | 140 | 144 | fits | 39,952 | 103 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 519,345 | 5.193 | 20 | 200 | fits | 129,948 | 203 | 0.374 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 499,077 | 4.991 | 20 | 20 | fits | 129,948 | 203 | 0.374 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 348,925 | 3.489 | 20 | 24 | fits | 153,200 | 175 | 0.455 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 459,602 | 4.596 | 20 | 50 | fits | 129,948 | 203 | 0.374 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,088,908 | 10.889 | 20 | 20 | fits | 79,081 | 30 | 0.675 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 931,868 | 9.319 | 140 | 144 | fits | 26,107 | 52 | 0.489 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,769,376 | 17.694 | 140 | 144 | fits | 44,321 | 102 | 0.347 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,787,149 | 17.871 | 140 | 144 | fits | 44,321 | 102 | 0.347 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,914,789 | 19.148 | 140 | 144 | fits | 41,076 | 103 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 1,931,917 | 19.319 | 140 | 144 | fits | 41,076 | 103 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 2,117,217 | 21.172 | 140 | 144 | fits | 39,228 | 102 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 329,302 | 3.293 | 140 | 144 | fits | 60,031 | 111 | 0.307 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 347,941 | 3.479 | 140 | 144 | fits | 60,031 | 111 | 0.307 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 2,132,590 | 21.326 | 140 | 144 | fits | 39,228 | 102 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,312,570 | 23.126 | 140 | 144 | fits | 36,862 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,329,651 | 23.297 | 140 | 144 | fits | 36,862 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 518,720 | 5.187 | 140 | 144 | fits | 41,100 | 62 | 0.329 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 162,068 | 1.621 | 20 | 200 | fits | 151,353 | 250 | 0.376 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 462,206 | 4.622 | 20 | 20 | fits | 142,177 | 138 | 0.496 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 442,002 | 4.420 | 20 | 24 | fits | 142,177 | 138 | 0.496 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 422,731 | 4.227 | 20 | 50 | fits | 142,177 | 138 | 0.496 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 1,049,408 | 10.494 | 20 | 20 | fits | 78,989 | 30 | 0.675 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
