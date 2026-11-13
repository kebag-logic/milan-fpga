### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.acmp.if0` (notice-burst-3) | 6.562 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.adp.if0` (notice-burst-5) | 5.652 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.aecp.if0` (notice-every-6) | 4.605 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.maap.if0` (notice-every-6) | 5.677 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.srp.if0` (notice-burst-5) | 9.009 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-6.mrpdu.periodic.if0` (notice-every-6) | 1.052 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 17.228 (17.506) | fits | 0 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1859 | 0 | 154,708 (1.547) | fits |
| notice-every-1 | 1859 | 0 | 155,339 (1.553) | fits |
| notice-every-2 | 1852 | 0 | 155,095 (1.551) | fits |
| notice-every-3 | 1852 | 0 | 154,662 (1.547) | fits |
| notice-every-4 | 1847 | 0 | 154,121 (1.541) | fits |
| notice-every-5 | 1850 | 0 | 155,889 (1.559) | fits |
| notice-every-6 | 1848 | 0 | 153,067 (1.531) | fits |
| notice-every-7 | 1850 | 0 | 155,143 (1.551) | fits |
| notice-burst-0 | 1252 | 0 | 151,960 (1.520) | fits |
| notice-burst-1 | 1219 | 0 | 151,384 (1.514) | fits |
| notice-burst-2 | 1222 | 0 | 156,127 (1.561) | fits |
| notice-burst-3 | 1216 | 0 | 154,058 (1.541) | fits |
| notice-burst-4 | 1202 | 0 | 152,364 (1.524) | fits |
| notice-burst-5 | 1210 | 0 | 151,061 (1.511) | fits |
| notice-burst-6 | 1236 | 0 | 152,553 (1.526) | fits |
| notice-burst-7 | 1209 | 0 | 150,636 (1.506) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 2.157 | 125 | 16 | 2 | within |
| notice-every-0 | 2.337 | 125 | 16 | 2 | within |
| notice-every-0 | 4.277 | 125 | 16 | 2 | within |
| notice-every-0 | 4.461 | 125 | 16 | 2 | within |
| notice-every-0 | 6.269 | 125 | 16 | 2 | within |
| notice-every-0 | 6.448 | 125 | 16 | 2 | within |
| notice-every-0 | 8.282 | 125 | 16 | 2 | within |
| notice-every-0 | 8.460 | 125 | 16 | 2 | within |
| notice-every-0 | 2.496 | 125 | 16 | 2 | within |
| notice-every-0 | 2.637 | 125 | 16 | 2 | within |
| notice-every-0 | 4.648 | 125 | 16 | 2 | within |
| notice-every-0 | 4.834 | 125 | 16 | 2 | within |
| notice-every-1 | 4.329 | 125 | 16 | 2 | within |
| notice-every-1 | 4.511 | 125 | 16 | 2 | within |
| notice-every-1 | 6.222 | 125 | 16 | 2 | within |
| notice-every-1 | 6.405 | 125 | 16 | 2 | within |
| notice-every-1 | 8.223 | 125 | 16 | 2 | within |
| notice-every-1 | 8.401 | 125 | 16 | 2 | within |
| notice-every-1 | 2.150 | 125 | 16 | 2 | within |
| notice-every-1 | 2.336 | 125 | 16 | 2 | within |
| notice-every-1 | 4.667 | 125 | 16 | 2 | within |
| notice-every-1 | 4.806 | 125 | 16 | 2 | within |
| notice-every-1 | 2.523 | 125 | 16 | 2 | within |
| notice-every-1 | 2.713 | 125 | 16 | 2 | within |
| notice-every-2 | 6.245 | 125 | 16 | 2 | within |
| notice-every-2 | 6.426 | 125 | 16 | 2 | within |
| notice-every-2 | 8.292 | 125 | 16 | 2 | within |
| notice-every-2 | 8.474 | 125 | 16 | 2 | within |
| notice-every-2 | 2.155 | 125 | 16 | 2 | within |
| notice-every-2 | 2.337 | 125 | 16 | 2 | within |
| notice-every-2 | 4.326 | 125 | 16 | 2 | within |
| notice-every-2 | 4.510 | 125 | 16 | 2 | within |
| notice-every-2 | 6.580 | 125 | 16 | 2 | within |
| notice-every-2 | 6.717 | 125 | 16 | 2 | within |
| notice-every-2 | 2.525 | 125 | 16 | 2 | within |
| notice-every-2 | 2.715 | 125 | 16 | 2 | within |
| notice-every-3 | 6.249 | 125 | 16 | 2 | within |
| notice-every-3 | 6.430 | 125 | 16 | 2 | within |
| notice-every-3 | 2.162 | 125 | 16 | 2 | within |
| notice-every-3 | 2.347 | 125 | 16 | 2 | within |
| notice-every-3 | 4.332 | 125 | 16 | 2 | within |
| notice-every-3 | 4.513 | 125 | 16 | 2 | within |
| notice-every-3 | 8.116 | 125 | 16 | 2 | within |
| notice-every-3 | 8.293 | 125 | 16 | 2 | within |
| notice-every-3 | 6.585 | 125 | 16 | 2 | within |
| notice-every-3 | 6.721 | 125 | 16 | 2 | within |
| notice-every-3 | 2.536 | 125 | 16 | 2 | within |
| notice-every-3 | 2.726 | 125 | 16 | 2 | within |
| notice-every-4 | 5.853 | 125 | 16 | 2 | within |
| notice-every-4 | 6.034 | 125 | 16 | 2 | within |
| notice-every-4 | 7.912 | 125 | 16 | 2 | within |
| notice-every-4 | 8.093 | 125 | 16 | 2 | within |
| notice-every-4 | 1.799 | 125 | 16 | 2 | within |
| notice-every-4 | 1.982 | 125 | 16 | 2 | within |
| notice-every-4 | 3.965 | 125 | 16 | 2 | within |
| notice-every-4 | 4.149 | 125 | 16 | 2 | within |
| notice-every-4 | 6.188 | 125 | 16 | 2 | within |
| notice-every-4 | 6.325 | 125 | 16 | 2 | within |
| notice-every-4 | 2.170 | 125 | 16 | 2 | within |
| notice-every-4 | 2.361 | 125 | 16 | 2 | within |
| notice-every-5 | 7.811 | 125 | 16 | 2 | within |
| notice-every-5 | 7.991 | 125 | 16 | 2 | within |
| notice-every-5 | 1.716 | 125 | 16 | 2 | within |
| notice-every-5 | 1.901 | 125 | 16 | 2 | within |
| notice-every-5 | 3.881 | 125 | 16 | 2 | within |
| notice-every-5 | 4.062 | 125 | 16 | 2 | within |
| notice-every-5 | 5.756 | 125 | 16 | 2 | within |
| notice-every-5 | 5.936 | 125 | 16 | 2 | within |
| notice-every-5 | 8.143 | 125 | 16 | 2 | within |
| notice-every-5 | 8.278 | 125 | 16 | 2 | within |
| notice-every-5 | 2.090 | 125 | 16 | 2 | within |
| notice-every-5 | 2.281 | 125 | 16 | 2 | within |
| notice-every-6 | 5.853 | 125 | 16 | 2 | within |
| notice-every-6 | 6.034 | 125 | 16 | 2 | within |
| notice-every-6 | 7.912 | 125 | 16 | 2 | within |
| notice-every-6 | 8.094 | 125 | 16 | 2 | within |
| notice-every-6 | 1.800 | 125 | 16 | 2 | within |
| notice-every-6 | 1.982 | 125 | 16 | 2 | within |
| notice-every-6 | 3.965 | 125 | 16 | 2 | within |
| notice-every-6 | 4.149 | 125 | 16 | 2 | within |
| notice-every-6 | 6.188 | 125 | 16 | 2 | within |
| notice-every-6 | 6.325 | 125 | 16 | 2 | within |
| notice-every-6 | 2.170 | 125 | 16 | 2 | within |
| notice-every-6 | 2.361 | 125 | 16 | 2 | within |
| notice-every-7 | 2.155 | 125 | 16 | 2 | within |
| notice-every-7 | 2.336 | 125 | 16 | 2 | within |
| notice-every-7 | 4.241 | 125 | 16 | 2 | within |
| notice-every-7 | 4.425 | 125 | 16 | 2 | within |
| notice-every-7 | 6.245 | 125 | 16 | 2 | within |
| notice-every-7 | 6.424 | 125 | 16 | 2 | within |
| notice-every-7 | 8.258 | 125 | 16 | 2 | within |
| notice-every-7 | 8.436 | 125 | 16 | 2 | within |
| notice-every-7 | 2.494 | 125 | 16 | 2 | within |
| notice-every-7 | 2.635 | 125 | 16 | 2 | within |
| notice-every-7 | 4.612 | 125 | 16 | 2 | within |
| notice-every-7 | 4.797 | 125 | 16 | 2 | within |
| notice-burst-0 | 9.559 | 125 | 16 | 1 | within |
| notice-burst-0 | 14.038 | 125 | 16 | 1 | within |
| notice-burst-0 | 14.220 | 125 | 16 | 1 | within |
| notice-burst-0 | 14.400 | 125 | 16 | 1 | within |
| notice-burst-0 | 2.140 | 125 | 16 | 1 | within |
| notice-burst-0 | 2.322 | 125 | 16 | 1 | within |
| notice-burst-0 | 3.879 | 125 | 16 | 1 | within |
| notice-burst-0 | 4.062 | 125 | 16 | 1 | within |
| notice-burst-0 | 14.553 | 125 | 16 | 1 | within |
| notice-burst-0 | 15.100 | 125 | 16 | 1 | within |
| notice-burst-0 | 15.280 | 125 | 16 | 1 | within |
| notice-burst-0 | 4.650 | 125 | 16 | 1 | within |
| notice-burst-1 | 8.862 | 125 | 16 | 1 | within |
| notice-burst-1 | 13.383 | 125 | 16 | 1 | within |
| notice-burst-1 | 13.567 | 125 | 16 | 1 | within |
| notice-burst-1 | 13.747 | 125 | 16 | 1 | within |
| notice-burst-1 | 13.905 | 125 | 16 | 1 | within |
| notice-burst-1 | 15.204 | 125 | 16 | 1 | within |
| notice-burst-1 | 3.168 | 125 | 16 | 1 | within |
| notice-burst-1 | 3.354 | 125 | 16 | 1 | within |
| notice-burst-1 | 15.357 | 125 | 16 | 1 | within |
| notice-burst-1 | 15.493 | 125 | 16 | 1 | within |
| notice-burst-1 | 15.668 | 125 | 16 | 1 | within |
| notice-burst-1 | 5.665 | 125 | 16 | 1 | within |
| notice-burst-2 | 9.144 | 125 | 16 | 2 | within |
| notice-burst-2 | 12.344 | 125 | 16 | 2 | within |
| notice-burst-2 | 12.527 | 125 | 16 | 2 | within |
| notice-burst-2 | 12.708 | 125 | 16 | 2 | within |
| notice-burst-2 | 2.069 | 125 | 16 | 2 | within |
| notice-burst-2 | 2.251 | 125 | 16 | 2 | within |
| notice-burst-2 | 2.410 | 125 | 16 | 2 | within |
| notice-burst-2 | 2.590 | 125 | 16 | 2 | within |
| notice-burst-2 | 12.861 | 125 | 16 | 2 | within |
| notice-burst-2 | 14.115 | 125 | 16 | 2 | within |
| notice-burst-2 | 14.293 | 125 | 16 | 2 | within |
| notice-burst-2 | 4.655 | 125 | 16 | 2 | within |
| notice-burst-3 | 11.526 | 125 | 16 | 0 | within |
| notice-burst-3 | 11.708 | 125 | 16 | 0 | within |
| notice-burst-3 | 1.903 | 125 | 16 | 0 | within |
| notice-burst-3 | 2.088 | 125 | 16 | 0 | within |
| notice-burst-3 | 2.247 | 125 | 16 | 0 | within |
| notice-burst-3 | 2.424 | 125 | 16 | 0 | within |
| notice-burst-3 | 4.205 | 125 | 16 | 0 | within |
| notice-burst-3 | 11.894 | 125 | 16 | 0 | within |
| notice-burst-3 | 12.046 | 125 | 16 | 0 | within |
| notice-burst-3 | 12.893 | 125 | 16 | 0 | within |
| notice-burst-3 | 13.074 | 125 | 16 | 0 | within |
| notice-burst-3 | 13.253 | 125 | 16 | 0 | within |
| notice-burst-4 | 10.268 | 125 | 16 | 1 | within |
| notice-burst-4 | 10.449 | 125 | 16 | 1 | within |
| notice-burst-4 | 10.617 | 125 | 16 | 1 | within |
| notice-burst-4 | 10.799 | 125 | 16 | 1 | within |
| notice-burst-4 | 2.857 | 125 | 16 | 1 | within |
| notice-burst-4 | 12.132 | 125 | 16 | 1 | within |
| notice-burst-4 | 12.297 | 125 | 16 | 1 | within |
| notice-burst-4 | 12.473 | 125 | 16 | 1 | within |
| notice-burst-4 | 12.624 | 125 | 16 | 1 | within |
| notice-burst-4 | 14.190 | 125 | 16 | 1 | within |
| notice-burst-4 | 14.368 | 125 | 16 | 1 | within |
| notice-burst-4 | 14.548 | 125 | 16 | 1 | within |
| notice-burst-5 | 5.947 | 125 | 16 | 0 | within |
| notice-burst-5 | 6.128 | 125 | 16 | 0 | within |
| notice-burst-5 | 8.368 | 125 | 16 | 0 | within |
| notice-burst-5 | 15.803 | 125 | 16 | 0 | within |
| notice-burst-5 | 15.976 | 125 | 16 | 0 | within |
| notice-burst-5 | 16.152 | 125 | 16 | 0 | within |
| notice-burst-5 | 16.309 | 125 | 16 | 0 | within |
| notice-burst-5 | 17.044 | 125 | 16 | 0 | within |
| notice-burst-5 | 6.287 | 125 | 16 | 0 | within |
| notice-burst-5 | 6.428 | 125 | 16 | 0 | within |
| notice-burst-5 | 6.670 | 125 | 16 | 0 | within |
| notice-burst-5 | 17.228 | 125 | 16 | 0 | within |
| notice-burst-6 | 7.397 | 125 | 16 | 0 | within |
| notice-burst-6 | 14.804 | 125 | 16 | 0 | within |
| notice-burst-6 | 14.987 | 125 | 16 | 0 | within |
| notice-burst-6 | 15.167 | 125 | 16 | 0 | within |
| notice-burst-6 | 15.325 | 125 | 16 | 0 | within |
| notice-burst-6 | 15.915 | 125 | 16 | 0 | within |
| notice-burst-6 | 1.841 | 125 | 16 | 0 | within |
| notice-burst-6 | 2.024 | 125 | 16 | 0 | within |
| notice-burst-6 | 16.069 | 125 | 16 | 0 | within |
| notice-burst-6 | 16.204 | 125 | 16 | 0 | within |
| notice-burst-6 | 16.381 | 125 | 16 | 0 | within |
| notice-burst-6 | 2.928 | 125 | 16 | 0 | within |
| notice-burst-7 | 9.002 | 125 | 16 | 0 | within |
| notice-burst-7 | 14.910 | 125 | 16 | 0 | within |
| notice-burst-7 | 15.093 | 125 | 16 | 0 | within |
| notice-burst-7 | 15.272 | 125 | 16 | 0 | within |
| notice-burst-7 | 2.163 | 125 | 16 | 0 | within |
| notice-burst-7 | 2.345 | 125 | 16 | 0 | within |
| notice-burst-7 | 2.503 | 125 | 16 | 0 | within |
| notice-burst-7 | 2.683 | 125 | 16 | 0 | within |
| notice-burst-7 | 15.425 | 125 | 16 | 0 | within |
| notice-burst-7 | 15.974 | 125 | 16 | 0 | within |
| notice-burst-7 | 16.154 | 125 | 16 | 0 | within |
| notice-burst-7 | 3.100 | 125 | 16 | 0 | within |

Latest: 17.228 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 104,564 (1.046) | 77,345 (0.773) |
| notice-every-1 | 307 | 100,162 (1.002) | 77,345 (0.773) |
| notice-every-2 | 307 | 104,514 (1.045) | 77,345 (0.773) |
| notice-every-3 | 307 | 109,168 (1.092) | 77,258 (0.773) |
| notice-every-4 | 307 | 89,271 (0.893) | 76,872 (0.769) |
| notice-every-5 | 307 | 89,271 (0.893) | 76,872 (0.769) |
| notice-every-6 | 307 | 89,271 (0.893) | 76,872 (0.769) |
| notice-every-7 | 307 | 89,271 (0.893) | 76,872 (0.769) |
| notice-burst-0 | 317 | 104,564 (1.046) | 78,769 (0.788) |
| notice-burst-1 | 317 | 112,023 (1.120) | 78,828 (0.788) |
| notice-burst-2 | 317 | 104,514 (1.045) | 78,769 (0.788) |
| notice-burst-3 | 317 | 109,168 (1.092) | 78,828 (0.788) |
| notice-burst-4 | 317 | 98,565 (0.986) | 78,828 (0.788) |
| notice-burst-5 | 317 | 100,149 (1.001) | 78,828 (0.788) |
| notice-burst-6 | 317 | 100,579 (1.006) | 78,769 (0.788) |
| notice-burst-7 | 317 | 104,673 (1.047) | 78,828 (0.788) |

Longest pass that carries a step: 112,023 CPU cycles (1.120 ms), notice-burst-1; longest step: 78,828 (0.788 ms), notice-burst-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 215,665 | 2.157 | 125 | 129 | fits | 73,470 | 204 | 0.229 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 233,743 | 2.337 | 125 | 129 | fits | 73,470 | 204 | 0.229 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 427,696 | 4.277 | 125 | 129 | fits | 80,588 | 204 | 0.214 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 446,138 | 4.461 | 125 | 129 | fits | 80,588 | 204 | 0.214 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 626,917 | 6.269 | 125 | 129 | fits | 39,777 | 102 | 0.262 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 644,762 | 6.448 | 125 | 129 | fits | 39,777 | 102 | 0.262 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 828,246 | 8.282 | 125 | 129 | fits | 39,285 | 102 | 0.254 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 845,982 | 8.460 | 125 | 129 | fits | 39,285 | 102 | 0.254 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 249,569 | 2.496 | 125 | 129 | fits | 73,470 | 204 | 0.229 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 263,715 | 2.637 | 125 | 129 | fits | 73,470 | 204 | 0.229 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 464,788 | 4.648 | 125 | 129 | fits | 80,588 | 204 | 0.214 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 483,361 | 4.834 | 125 | 129 | fits | 80,588 | 204 | 0.214 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 482,025 | 4.820 | 20 | 200 | fits | 145,134 | 134 | 0.409 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 578,498 | 5.785 | 20 | 20 | fits | 116,741 | 75 | 0.647 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 441,553 | 4.416 | 20 | 24 | fits | 145,134 | 134 | 0.409 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 539,023 | 5.390 | 20 | 50 | fits | 116,741 | 75 | 0.647 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 855,847 | 8.558 | 20 | 20 | fits | 76,568 | 53 | 0.592 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 84,071 | 0.841 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 432,935 | 4.329 | 125 | 129 | fits | 72,141 | 201 | 0.223 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 451,095 | 4.511 | 125 | 129 | fits | 72,141 | 201 | 0.223 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 622,223 | 6.222 | 125 | 129 | fits | 41,573 | 103 | 0.263 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 640,460 | 6.405 | 125 | 129 | fits | 41,573 | 103 | 0.263 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 822,310 | 8.223 | 125 | 129 | fits | 39,453 | 102 | 0.260 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 840,084 | 8.401 | 125 | 129 | fits | 39,453 | 102 | 0.260 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 214,992 | 2.150 | 125 | 129 | fits | 81,085 | 206 | 0.212 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 233,567 | 2.336 | 125 | 129 | fits | 81,085 | 206 | 0.212 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 466,690 | 4.667 | 125 | 129 | fits | 72,141 | 201 | 0.223 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 480,603 | 4.806 | 125 | 129 | fits | 72,141 | 201 | 0.223 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 252,277 | 2.523 | 125 | 129 | fits | 81,085 | 206 | 0.212 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 271,312 | 2.713 | 125 | 129 | fits | 81,085 | 206 | 0.212 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 474,944 | 4.749 | 20 | 200 | fits | 145,591 | 148 | 0.404 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 567,220 | 5.672 | 20 | 20 | fits | 112,544 | 74 | 0.643 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 434,472 | 4.345 | 20 | 24 | fits | 145,591 | 148 | 0.404 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 527,745 | 5.277 | 20 | 50 | fits | 112,544 | 74 | 0.643 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 844,758 | 8.448 | 20 | 20 | fits | 90,338 | 49 | 0.521 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 103,953 | 1.040 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 624,481 | 6.245 | 125 | 129 | fits | 70,329 | 202 | 0.213 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 642,551 | 6.426 | 125 | 129 | fits | 70,329 | 202 | 0.213 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 829,234 | 8.292 | 125 | 129 | fits | 41,061 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 847,400 | 8.474 | 125 | 129 | fits | 41,061 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 215,458 | 2.155 | 125 | 129 | fits | 80,500 | 204 | 0.211 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 233,730 | 2.337 | 125 | 129 | fits | 80,500 | 204 | 0.211 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 432,567 | 4.326 | 125 | 129 | fits | 42,514 | 102 | 0.279 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 450,959 | 4.510 | 125 | 129 | fits | 42,514 | 102 | 0.279 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 657,995 | 6.580 | 125 | 129 | fits | 70,329 | 202 | 0.213 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 671,677 | 6.717 | 125 | 129 | fits | 70,329 | 202 | 0.213 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 252,505 | 2.525 | 125 | 129 | fits | 80,500 | 204 | 0.211 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 271,540 | 2.715 | 125 | 129 | fits | 80,500 | 204 | 0.211 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 486,422 | 4.864 | 20 | 200 | fits | 146,450 | 148 | 0.410 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 579,923 | 5.799 | 20 | 20 | fits | 113,769 | 75 | 0.650 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 445,950 | 4.460 | 20 | 24 | fits | 146,450 | 148 | 0.410 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 540,448 | 5.404 | 20 | 50 | fits | 113,769 | 75 | 0.650 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 868,916 | 8.689 | 20 | 20 | fits | 94,207 | 61 | 0.559 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 86,150 | 0.862 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 624,943 | 6.249 | 125 | 129 | fits | 70,303 | 202 | 0.210 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 643,011 | 6.430 | 125 | 129 | fits | 70,303 | 202 | 0.210 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 216,154 | 2.162 | 125 | 129 | fits | 81,966 | 204 | 0.218 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 234,716 | 2.347 | 125 | 129 | fits | 81,966 | 204 | 0.218 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 433,163 | 4.332 | 125 | 129 | fits | 42,027 | 102 | 0.280 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 451,324 | 4.513 | 125 | 129 | fits | 42,027 | 102 | 0.280 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 811,552 | 8.116 | 125 | 129 | fits | 39,457 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 829,326 | 8.293 | 125 | 129 | fits | 39,457 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 658,455 | 6.585 | 125 | 129 | fits | 70,303 | 202 | 0.210 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 672,137 | 6.721 | 125 | 129 | fits | 70,303 | 202 | 0.210 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 253,570 | 2.536 | 125 | 129 | fits | 81,966 | 204 | 0.218 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 272,605 | 2.726 | 125 | 129 | fits | 81,966 | 204 | 0.218 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 487,349 | 4.873 | 20 | 200 | fits | 150,011 | 155 | 0.410 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 579,836 | 5.798 | 20 | 20 | fits | 112,755 | 57 | 0.642 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 446,877 | 4.469 | 20 | 24 | fits | 150,011 | 155 | 0.410 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 427,606 | 4.276 | 20 | 50 | fits | 150,011 | 155 | 0.410 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 863,449 | 8.634 | 20 | 20 | fits | 85,806 | 55 | 0.582 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 94,814 | 0.948 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 585,302 | 5.853 | 125 | 129 | fits | 70,250 | 202 | 0.213 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 603,372 | 6.034 | 125 | 129 | fits | 70,250 | 202 | 0.213 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 791,179 | 7.912 | 125 | 129 | fits | 41,061 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 809,345 | 8.093 | 125 | 129 | fits | 41,061 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 179,920 | 1.799 | 125 | 129 | fits | 80,523 | 206 | 0.208 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 198,192 | 1.982 | 125 | 129 | fits | 80,523 | 206 | 0.208 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 396,514 | 3.965 | 125 | 129 | fits | 42,418 | 102 | 0.277 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 414,906 | 4.149 | 125 | 129 | fits | 42,418 | 102 | 0.277 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 618,816 | 6.188 | 125 | 129 | fits | 70,250 | 202 | 0.213 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 632,498 | 6.325 | 125 | 129 | fits | 70,250 | 202 | 0.213 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 217,036 | 2.170 | 125 | 129 | fits | 80,523 | 206 | 0.208 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 236,071 | 2.361 | 125 | 129 | fits | 80,523 | 206 | 0.208 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 155,503 | 1.555 | 20 | 200 | fits | 144,488 | 189 | 0.323 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 572,291 | 5.723 | 20 | 20 | fits | 118,727 | 86 | 0.618 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 433,360 | 4.334 | 20 | 24 | fits | 144,941 | 147 | 0.413 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 532,816 | 5.328 | 20 | 50 | fits | 118,727 | 86 | 0.618 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 867,183 | 8.672 | 20 | 20 | fits | 107,609 | 57 | 0.491 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 102,985 | 1.030 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 781,110 | 7.811 | 125 | 129 | fits | 69,453 | 201 | 0.209 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 799,069 | 7.991 | 125 | 129 | fits | 69,453 | 201 | 0.209 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 171,610 | 1.716 | 125 | 129 | fits | 82,418 | 206 | 0.221 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 190,090 | 1.901 | 125 | 129 | fits | 82,418 | 206 | 0.221 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 388,056 | 3.881 | 125 | 129 | fits | 41,931 | 102 | 0.279 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 406,217 | 4.062 | 125 | 129 | fits | 41,931 | 102 | 0.279 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 575,571 | 5.756 | 125 | 129 | fits | 40,659 | 103 | 0.262 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 593,647 | 5.936 | 125 | 129 | fits | 40,659 | 103 | 0.262 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 814,347 | 8.143 | 125 | 129 | fits | 69,453 | 201 | 0.209 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 827,798 | 8.278 | 125 | 129 | fits | 69,453 | 201 | 0.209 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 209,026 | 2.090 | 125 | 129 | fits | 82,418 | 206 | 0.221 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 228,061 | 2.281 | 125 | 129 | fits | 82,418 | 206 | 0.221 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 159,747 | 1.597 | 20 | 200 | fits | 152,581 | 123 | 0.261 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 580,740 | 5.807 | 20 | 20 | fits | 113,171 | 59 | 0.645 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 447,365 | 4.474 | 20 | 24 | fits | 154,799 | 172 | 0.400 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 428,094 | 4.281 | 20 | 50 | fits | 154,799 | 172 | 0.400 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 858,745 | 8.587 | 20 | 20 | fits | 84,130 | 49 | 0.579 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 92,291 | 0.923 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 585,304 | 5.853 | 125 | 129 | fits | 70,248 | 202 | 0.211 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 603,372 | 6.034 | 125 | 129 | fits | 70,248 | 202 | 0.211 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 791,189 | 7.912 | 125 | 129 | fits | 41,061 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 809,355 | 8.094 | 125 | 129 | fits | 41,061 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 179,990 | 1.800 | 125 | 129 | fits | 80,455 | 206 | 0.207 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 198,194 | 1.982 | 125 | 129 | fits | 80,455 | 206 | 0.207 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 396,516 | 3.965 | 125 | 129 | fits | 42,418 | 102 | 0.277 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 414,908 | 4.149 | 125 | 129 | fits | 42,418 | 102 | 0.277 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 618,816 | 6.188 | 125 | 129 | fits | 70,248 | 202 | 0.211 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 632,498 | 6.325 | 125 | 129 | fits | 70,248 | 202 | 0.211 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 217,038 | 2.170 | 125 | 129 | fits | 80,455 | 206 | 0.207 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 236,073 | 2.361 | 125 | 129 | fits | 80,455 | 206 | 0.207 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 500,935 | 5.009 | 20 | 200 | fits | 149,303 | 148 | 0.429 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 607,210 | 6.072 | 20 | 20 | fits | 112,198 | 88 | 0.664 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 460,463 | 4.605 | 20 | 24 | fits | 149,303 | 148 | 0.429 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 567,735 | 5.677 | 20 | 50 | fits | 112,198 | 88 | 0.664 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 868,870 | 8.689 | 20 | 20 | fits | 81,784 | 43 | 0.547 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 105,175 | 1.052 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 215,490 | 2.155 | 125 | 129 | fits | 73,470 | 204 | 0.229 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 233,568 | 2.336 | 125 | 129 | fits | 73,470 | 204 | 0.229 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 424,081 | 4.241 | 125 | 129 | fits | 80,578 | 204 | 0.214 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 442,523 | 4.425 | 125 | 129 | fits | 80,578 | 204 | 0.214 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 624,546 | 6.245 | 125 | 129 | fits | 39,777 | 102 | 0.262 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 642,391 | 6.424 | 125 | 129 | fits | 39,777 | 102 | 0.262 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 825,845 | 8.258 | 125 | 129 | fits | 39,285 | 102 | 0.254 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 843,581 | 8.436 | 125 | 129 | fits | 39,285 | 102 | 0.254 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 249,394 | 2.494 | 125 | 129 | fits | 73,470 | 204 | 0.229 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 263,540 | 2.635 | 125 | 129 | fits | 73,470 | 204 | 0.229 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 461,173 | 4.612 | 125 | 129 | fits | 80,578 | 204 | 0.214 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 479,746 | 4.797 | 125 | 129 | fits | 80,578 | 204 | 0.214 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 488,484 | 4.885 | 20 | 200 | fits | 154,993 | 168 | 0.396 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 585,743 | 5.857 | 20 | 20 | fits | 117,527 | 62 | 0.646 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 448,012 | 4.480 | 20 | 24 | fits | 154,993 | 168 | 0.396 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 428,741 | 4.287 | 20 | 50 | fits | 154,993 | 168 | 0.396 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 852,584 | 8.526 | 20 | 20 | fits | 67,013 | 41 | 0.632 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 95,514 | 0.955 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 955,927 | 9.559 | 125 | 129 | fits | 24,685 | 51 | 0.462 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,403,792 | 14.038 | 125 | 129 | fits | 77,063 | 203 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,422,025 | 14.220 | 125 | 129 | fits | 77,063 | 203 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,439,995 | 14.400 | 125 | 129 | fits | 77,063 | 203 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 214,042 | 2.140 | 125 | 129 | fits | 55,293 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 232,175 | 2.322 | 125 | 129 | fits | 55,293 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 387,949 | 3.879 | 125 | 129 | fits | 42,843 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 406,244 | 4.062 | 125 | 129 | fits | 42,843 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,455,272 | 14.553 | 125 | 129 | fits | 77,063 | 203 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,509,966 | 15.100 | 125 | 129 | fits | 37,563 | 102 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,527,991 | 15.280 | 125 | 129 | fits | 37,563 | 102 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 464,987 | 4.650 | 125 | 129 | fits | 37,991 | 60 | 0.366 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 152,060 | 1.521 | 20 | 200 | fits | 151,960 | 191 | 0.322 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 567,480 | 5.675 | 20 | 20 | fits | 116,040 | 71 | 0.645 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 406,551 | 4.066 | 20 | 24 | fits | 146,336 | 157 | 0.400 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 387,280 | 3.873 | 20 | 50 | fits | 146,336 | 157 | 0.400 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 812,321 | 8.123 | 20 | 20 | fits | 80,538 | 42 | 0.540 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 886,223 | 8.862 | 125 | 129 | fits | 24,997 | 52 | 0.465 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,338,270 | 13.383 | 125 | 129 | fits | 77,656 | 203 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,356,693 | 13.567 | 125 | 129 | fits | 77,656 | 203 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,374,715 | 13.747 | 125 | 129 | fits | 77,656 | 203 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 1,390,490 | 13.905 | 125 | 129 | fits | 77,656 | 203 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 1,520,415 | 15.204 | 125 | 129 | fits | 69,900 | 202 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 316,819 | 3.168 | 125 | 129 | fits | 56,500 | 111 | 0.329 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 335,399 | 3.354 | 125 | 129 | fits | 56,500 | 111 | 0.329 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,535,666 | 15.357 | 125 | 129 | fits | 69,900 | 202 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,549,252 | 15.493 | 125 | 129 | fits | 69,900 | 202 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,566,845 | 15.668 | 125 | 129 | fits | 69,900 | 202 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 566,523 | 5.665 | 125 | 129 | fits | 25,983 | 53 | 0.340 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 151,182 | 1.512 | 20 | 200 | fits | 151,384 | 196 | 0.328 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 587,655 | 5.877 | 20 | 20 | fits | 111,339 | 76 | 0.661 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 431,115 | 4.311 | 20 | 24 | fits | 143,567 | 150 | 0.395 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 411,844 | 4.118 | 20 | 50 | fits | 143,567 | 150 | 0.395 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 841,368 | 8.414 | 20 | 20 | fits | 89,101 | 46 | 0.519 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 914,380 | 9.144 | 125 | 129 | fits | 26,048 | 53 | 0.485 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,234,380 | 12.344 | 125 | 129 | fits | 76,643 | 203 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,252,672 | 12.527 | 125 | 129 | fits | 76,643 | 203 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,270,829 | 12.708 | 125 | 129 | fits | 76,643 | 203 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 206,859 | 2.069 | 125 | 129 | fits | 90,221 | 212 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 225,060 | 2.251 | 125 | 129 | fits | 90,221 | 212 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 241,030 | 2.410 | 125 | 129 | fits | 90,221 | 212 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 259,030 | 2.590 | 125 | 129 | fits | 90,221 | 212 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,286,106 | 12.861 | 125 | 129 | fits | 76,643 | 203 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,411,459 | 14.115 | 125 | 129 | fits | 37,207 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,429,284 | 14.293 | 125 | 129 | fits | 37,207 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 465,522 | 4.655 | 125 | 129 | fits | 25,836 | 52 | 0.344 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 154,967 | 1.550 | 20 | 200 | fits | 144,101 | 183 | 0.343 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 583,306 | 5.833 | 20 | 20 | fits | 115,612 | 57 | 0.646 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 447,490 | 4.475 | 20 | 24 | fits | 156,127 | 155 | 0.379 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 428,219 | 4.282 | 20 | 50 | fits | 156,127 | 155 | 0.379 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 842,653 | 8.427 | 20 | 20 | fits | 72,045 | 38 | 0.567 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,152,591 | 11.526 | 125 | 129 | fits | 78,157 | 203 | 0.261 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,170,822 | 11.708 | 125 | 129 | fits | 78,157 | 203 | 0.261 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 190,306 | 1.903 | 125 | 129 | fits | 90,312 | 212 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 208,781 | 2.088 | 125 | 129 | fits | 90,312 | 212 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 224,669 | 2.247 | 125 | 129 | fits | 90,312 | 212 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 242,438 | 2.424 | 125 | 129 | fits | 90,312 | 212 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 420,510 | 4.205 | 125 | 129 | fits | 22,207 | 52 | 0.380 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,189,358 | 11.894 | 125 | 129 | fits | 78,157 | 203 | 0.261 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,204,563 | 12.046 | 125 | 129 | fits | 78,157 | 203 | 0.261 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,289,334 | 12.893 | 125 | 129 | fits | 55,555 | 152 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,307,359 | 13.074 | 125 | 129 | fits | 55,555 | 152 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 1,325,349 | 13.253 | 125 | 129 | fits | 55,555 | 152 | 0.205 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 561,600 | 5.616 | 20 | 200 | fits | 147,248 | 172 | 0.314 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 656,208 | 6.562 | 20 | 20 | fits | 114,876 | 57 | 0.636 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 373,880 | 3.739 | 20 | 24 | fits | 153,161 | 178 | 0.403 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 501,857 | 5.019 | 20 | 50 | fits | 147,248 | 172 | 0.314 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 885,281 | 8.853 | 20 | 20 | fits | 63,754 | 34 | 0.595 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,026,759 | 10.268 | 125 | 129 | fits | 79,955 | 203 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,044,911 | 10.449 | 125 | 129 | fits | 79,955 | 203 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,061,694 | 10.617 | 125 | 129 | fits | 79,955 | 203 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,079,854 | 10.799 | 125 | 129 | fits | 79,955 | 203 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 285,665 | 2.857 | 125 | 129 | fits | 24,477 | 52 | 0.445 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,213,235 | 12.132 | 125 | 129 | fits | 73,143 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,229,738 | 12.297 | 125 | 129 | fits | 73,143 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,247,329 | 12.473 | 125 | 129 | fits | 73,143 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,262,448 | 12.624 | 125 | 129 | fits | 73,143 | 203 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,419,020 | 14.190 | 125 | 129 | fits | 55,269 | 152 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,436,845 | 14.368 | 125 | 129 | fits | 55,269 | 152 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,454,835 | 14.548 | 125 | 129 | fits | 55,269 | 152 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 487,719 | 4.877 | 20 | 200 | fits | 146,932 | 154 | 0.380 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 579,739 | 5.797 | 20 | 20 | fits | 112,288 | 56 | 0.644 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 447,247 | 4.472 | 20 | 24 | fits | 146,932 | 154 | 0.380 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 427,976 | 4.280 | 20 | 50 | fits | 146,932 | 154 | 0.380 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 827,953 | 8.280 | 20 | 20 | fits | 81,856 | 48 | 0.533 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 594,679 | 5.947 | 125 | 129 | fits | 86,571 | 210 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 612,832 | 6.128 | 125 | 129 | fits | 86,571 | 210 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 836,760 | 8.368 | 125 | 129 | fits | 23,359 | 52 | 0.404 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,580,270 | 15.803 | 125 | 129 | fits | 76,509 | 203 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,597,612 | 15.976 | 125 | 129 | fits | 76,509 | 203 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,615,244 | 16.152 | 125 | 129 | fits | 76,509 | 203 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,630,895 | 16.309 | 125 | 129 | fits | 76,509 | 203 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,704,425 | 17.044 | 125 | 129 | fits | 41,995 | 103 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 628,659 | 6.287 | 125 | 129 | fits | 86,571 | 210 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 642,805 | 6.428 | 125 | 129 | fits | 86,571 | 210 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 667,042 | 6.670 | 125 | 129 | fits | 23,494 | 53 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 1,722,790 | 17.228 | 125 | 129 | fits | 41,995 | 103 | 0.238 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 565,248 | 5.652 | 20 | 200 | fits | 149,172 | 181 | 0.307 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 655,544 | 6.555 | 20 | 20 | fits | 110,564 | 56 | 0.629 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 375,604 | 3.756 | 20 | 24 | fits | 151,061 | 172 | 0.407 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 505,505 | 5.055 | 20 | 50 | fits | 149,172 | 181 | 0.307 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 900,868 | 9.009 | 20 | 20 | fits | 80,840 | 42 | 0.540 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 739,733 | 7.397 | 125 | 129 | fits | 24,946 | 52 | 0.455 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,480,427 | 14.804 | 125 | 129 | fits | 77,653 | 203 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,498,668 | 14.987 | 125 | 129 | fits | 77,653 | 203 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,516,709 | 15.167 | 125 | 129 | fits | 77,653 | 203 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,532,484 | 15.325 | 125 | 129 | fits | 77,653 | 203 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,591,478 | 15.915 | 125 | 129 | fits | 70,112 | 202 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 184,078 | 1.841 | 125 | 129 | fits | 55,895 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 202,442 | 2.024 | 125 | 129 | fits | 55,895 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 1,606,880 | 16.069 | 125 | 129 | fits | 70,112 | 202 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 1,620,441 | 16.204 | 125 | 129 | fits | 70,112 | 202 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 1,638,105 | 16.381 | 125 | 129 | fits | 70,112 | 202 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 292,775 | 2.928 | 125 | 129 | fits | 37,995 | 62 | 0.347 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 152,548 | 1.525 | 20 | 200 | fits | 147,621 | 189 | 0.325 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 565,719 | 5.657 | 20 | 20 | fits | 110,792 | 56 | 0.634 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 434,723 | 4.347 | 20 | 24 | fits | 145,148 | 158 | 0.392 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 415,452 | 4.155 | 20 | 50 | fits | 145,148 | 158 | 0.392 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 810,932 | 8.109 | 20 | 20 | fits | 80,782 | 42 | 0.543 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 900,209 | 9.002 | 125 | 129 | fits | 23,922 | 53 | 0.433 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,490,953 | 14.910 | 125 | 129 | fits | 77,142 | 203 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,509,265 | 15.093 | 125 | 129 | fits | 77,142 | 203 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,527,235 | 15.272 | 125 | 129 | fits | 77,142 | 203 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 216,330 | 2.163 | 125 | 129 | fits | 76,873 | 203 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 234,501 | 2.345 | 125 | 129 | fits | 76,873 | 203 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 250,263 | 2.503 | 125 | 129 | fits | 76,873 | 203 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 268,263 | 2.683 | 125 | 129 | fits | 76,873 | 203 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,542,512 | 15.425 | 125 | 129 | fits | 77,142 | 203 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,597,403 | 15.974 | 125 | 129 | fits | 37,563 | 102 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,615,428 | 16.154 | 125 | 129 | fits | 37,563 | 102 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 310,029 | 3.100 | 125 | 129 | fits | 41,856 | 68 | 0.441 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 153,241 | 1.532 | 20 | 200 | fits | 147,670 | 187 | 0.325 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 564,451 | 5.645 | 20 | 20 | fits | 111,193 | 56 | 0.638 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 433,054 | 4.331 | 20 | 24 | fits | 147,333 | 167 | 0.405 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 413,783 | 4.138 | 20 | 50 | fits | 147,333 | 167 | 0.405 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 809,415 | 8.094 | 20 | 20 | fits | 80,703 | 42 | 0.543 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
