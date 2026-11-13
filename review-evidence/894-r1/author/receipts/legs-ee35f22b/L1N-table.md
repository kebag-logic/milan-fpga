### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 6.472 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.adp.if0` (notice-burst-3) | 5.659 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.aecp.if0` (notice-every-6) | 4.605 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.maap.if0` (notice-every-6) | 5.592 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.srp.if0` (notice-burst-5) | 9.220 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.156 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.9.0.if0` (notice-burst-6) | 19.288 (19.483) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1855 | 0 | 153,598 (1.536) | fits |
| notice-every-1 | 1857 | 0 | 154,690 (1.547) | fits |
| notice-every-2 | 1854 | 0 | 155,565 (1.556) | fits |
| notice-every-3 | 1846 | 0 | 152,974 (1.530) | fits |
| notice-every-4 | 1846 | 0 | 154,121 (1.541) | fits |
| notice-every-5 | 1847 | 0 | 154,799 (1.548) | fits |
| notice-every-6 | 1850 | 0 | 153,046 (1.530) | fits |
| notice-every-7 | 1841 | 0 | 154,993 (1.550) | fits |
| notice-burst-0 | 1251 | 0 | 151,960 (1.520) | fits |
| notice-burst-1 | 1219 | 0 | 151,384 (1.514) | fits |
| notice-burst-2 | 1223 | 0 | 156,754 (1.568) | fits |
| notice-burst-3 | 1216 | 0 | 154,214 (1.542) | fits |
| notice-burst-4 | 1201 | 0 | 152,364 (1.524) | fits |
| notice-burst-5 | 1209 | 0 | 151,035 (1.510) | fits |
| notice-burst-6 | 1234 | 0 | 152,527 (1.525) | fits |
| notice-burst-7 | 1209 | 0 | 150,384 (1.504) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 7.813 | 125 | 16 | 2 | within |
| notice-every-0 | 7.993 | 125 | 16 | 2 | within |
| notice-every-0 | 1.866 | 125 | 16 | 2 | within |
| notice-every-0 | 2.050 | 125 | 16 | 2 | within |
| notice-every-0 | 3.827 | 125 | 16 | 2 | within |
| notice-every-0 | 4.008 | 125 | 16 | 2 | within |
| notice-every-0 | 5.942 | 125 | 16 | 2 | within |
| notice-every-0 | 6.123 | 125 | 16 | 2 | within |
| notice-every-0 | 8.146 | 125 | 16 | 2 | within |
| notice-every-0 | 9.832 | 125 | 16 | 2 | within |
| notice-every-0 | 2.240 | 125 | 16 | 2 | within |
| notice-every-0 | 4.198 | 125 | 16 | 2 | within |
| notice-every-1 | 2.157 | 125 | 16 | 2 | within |
| notice-every-1 | 2.338 | 125 | 16 | 2 | within |
| notice-every-1 | 4.080 | 125 | 16 | 2 | within |
| notice-every-1 | 4.265 | 125 | 16 | 2 | within |
| notice-every-1 | 6.052 | 125 | 16 | 2 | within |
| notice-every-1 | 6.230 | 125 | 16 | 2 | within |
| notice-every-1 | 8.191 | 125 | 16 | 2 | within |
| notice-every-1 | 8.370 | 125 | 16 | 2 | within |
| notice-every-1 | 2.496 | 125 | 16 | 2 | within |
| notice-every-1 | 4.420 | 125 | 16 | 2 | within |
| notice-every-1 | 6.413 | 125 | 16 | 2 | within |
| notice-every-1 | 8.550 | 125 | 16 | 2 | within |
| notice-every-2 | 4.115 | 125 | 16 | 1 | within |
| notice-every-2 | 4.297 | 125 | 16 | 1 | within |
| notice-every-2 | 6.083 | 125 | 16 | 1 | within |
| notice-every-2 | 6.265 | 125 | 16 | 1 | within |
| notice-every-2 | 8.017 | 125 | 16 | 1 | within |
| notice-every-2 | 8.195 | 125 | 16 | 1 | within |
| notice-every-2 | 1.991 | 125 | 16 | 1 | within |
| notice-every-2 | 2.177 | 125 | 16 | 1 | within |
| notice-every-2 | 4.453 | 125 | 16 | 1 | within |
| notice-every-2 | 6.417 | 125 | 16 | 1 | within |
| notice-every-2 | 2.364 | 125 | 16 | 1 | within |
| notice-every-2 | 8.378 | 125 | 16 | 1 | within |
| notice-every-3 | 3.767 | 125 | 16 | 2 | within |
| notice-every-3 | 3.949 | 125 | 16 | 2 | within |
| notice-every-3 | 5.738 | 125 | 16 | 2 | within |
| notice-every-3 | 5.920 | 125 | 16 | 2 | within |
| notice-every-3 | 7.851 | 125 | 16 | 2 | within |
| notice-every-3 | 8.030 | 125 | 16 | 2 | within |
| notice-every-3 | 1.799 | 125 | 16 | 2 | within |
| notice-every-3 | 1.983 | 125 | 16 | 2 | within |
| notice-every-3 | 4.106 | 125 | 16 | 2 | within |
| notice-every-3 | 6.071 | 125 | 16 | 2 | within |
| notice-every-3 | 2.171 | 125 | 16 | 2 | within |
| notice-every-3 | 8.213 | 125 | 16 | 2 | within |
| notice-every-4 | 6.239 | 125 | 16 | 2 | within |
| notice-every-4 | 6.420 | 125 | 16 | 2 | within |
| notice-every-4 | 8.177 | 125 | 16 | 2 | within |
| notice-every-4 | 8.359 | 125 | 16 | 2 | within |
| notice-every-4 | 2.155 | 125 | 16 | 2 | within |
| notice-every-4 | 2.338 | 125 | 16 | 2 | within |
| notice-every-4 | 4.101 | 125 | 16 | 2 | within |
| notice-every-4 | 4.285 | 125 | 16 | 2 | within |
| notice-every-4 | 6.574 | 125 | 16 | 2 | within |
| notice-every-4 | 8.508 | 125 | 16 | 2 | within |
| notice-every-4 | 2.525 | 125 | 16 | 2 | within |
| notice-every-4 | 4.474 | 125 | 16 | 2 | within |
| notice-every-5 | 5.885 | 125 | 16 | 2 | within |
| notice-every-5 | 6.066 | 125 | 16 | 2 | within |
| notice-every-5 | 7.794 | 125 | 16 | 2 | within |
| notice-every-5 | 7.976 | 125 | 16 | 2 | within |
| notice-every-5 | 1.800 | 125 | 16 | 2 | within |
| notice-every-5 | 1.982 | 125 | 16 | 2 | within |
| notice-every-5 | 3.756 | 125 | 16 | 2 | within |
| notice-every-5 | 3.940 | 125 | 16 | 2 | within |
| notice-every-5 | 6.220 | 125 | 16 | 2 | within |
| notice-every-5 | 8.125 | 125 | 16 | 2 | within |
| notice-every-5 | 2.171 | 125 | 16 | 2 | within |
| notice-every-5 | 4.129 | 125 | 16 | 2 | within |
| notice-every-6 | 5.858 | 125 | 16 | 2 | within |
| notice-every-6 | 6.039 | 125 | 16 | 2 | within |
| notice-every-6 | 7.777 | 125 | 16 | 2 | within |
| notice-every-6 | 7.960 | 125 | 16 | 2 | within |
| notice-every-6 | 1.800 | 125 | 16 | 2 | within |
| notice-every-6 | 1.982 | 125 | 16 | 2 | within |
| notice-every-6 | 3.760 | 125 | 16 | 2 | within |
| notice-every-6 | 3.944 | 125 | 16 | 2 | within |
| notice-every-6 | 6.194 | 125 | 16 | 2 | within |
| notice-every-6 | 8.109 | 125 | 16 | 2 | within |
| notice-every-6 | 2.170 | 125 | 16 | 2 | within |
| notice-every-6 | 4.133 | 125 | 16 | 2 | within |
| notice-every-7 | 2.155 | 125 | 16 | 2 | within |
| notice-every-7 | 2.336 | 125 | 16 | 2 | within |
| notice-every-7 | 4.276 | 125 | 16 | 2 | within |
| notice-every-7 | 4.461 | 125 | 16 | 2 | within |
| notice-every-7 | 6.073 | 125 | 16 | 2 | within |
| notice-every-7 | 6.252 | 125 | 16 | 2 | within |
| notice-every-7 | 8.181 | 125 | 16 | 2 | within |
| notice-every-7 | 8.360 | 125 | 16 | 2 | within |
| notice-every-7 | 2.494 | 125 | 16 | 2 | within |
| notice-every-7 | 4.616 | 125 | 16 | 2 | within |
| notice-every-7 | 6.435 | 125 | 16 | 2 | within |
| notice-every-7 | 8.540 | 125 | 16 | 2 | within |
| notice-burst-0 | 9.559 | 125 | 16 | 1 | within |
| notice-burst-0 | 14.243 | 125 | 16 | 1 | within |
| notice-burst-0 | 14.425 | 125 | 16 | 1 | within |
| notice-burst-0 | 14.606 | 125 | 16 | 1 | within |
| notice-burst-0 | 2.140 | 125 | 16 | 1 | within |
| notice-burst-0 | 2.322 | 125 | 16 | 1 | within |
| notice-burst-0 | 3.879 | 125 | 16 | 1 | within |
| notice-burst-0 | 4.062 | 125 | 16 | 1 | within |
| notice-burst-0 | 16.152 | 125 | 16 | 1 | within |
| notice-burst-0 | 16.289 | 125 | 16 | 1 | within |
| notice-burst-0 | 16.467 | 125 | 16 | 1 | within |
| notice-burst-0 | 4.650 | 125 | 16 | 1 | within |
| notice-burst-1 | 8.862 | 125 | 16 | 1 | within |
| notice-burst-1 | 13.587 | 125 | 16 | 1 | within |
| notice-burst-1 | 13.771 | 125 | 16 | 1 | within |
| notice-burst-1 | 13.952 | 125 | 16 | 1 | within |
| notice-burst-1 | 15.236 | 125 | 16 | 1 | within |
| notice-burst-1 | 15.414 | 125 | 16 | 1 | within |
| notice-burst-1 | 3.168 | 125 | 16 | 1 | within |
| notice-burst-1 | 3.354 | 125 | 16 | 1 | within |
| notice-burst-1 | 15.565 | 125 | 16 | 1 | within |
| notice-burst-1 | 17.100 | 125 | 16 | 1 | within |
| notice-burst-1 | 17.278 | 125 | 16 | 1 | within |
| notice-burst-1 | 5.665 | 125 | 16 | 1 | within |
| notice-burst-2 | 8.923 | 125 | 16 | 2 | within |
| notice-burst-2 | 12.520 | 125 | 16 | 2 | within |
| notice-burst-2 | 12.703 | 125 | 16 | 2 | within |
| notice-burst-2 | 12.884 | 125 | 16 | 2 | within |
| notice-burst-2 | 2.069 | 125 | 16 | 2 | within |
| notice-burst-2 | 2.251 | 125 | 16 | 2 | within |
| notice-burst-2 | 2.410 | 125 | 16 | 2 | within |
| notice-burst-2 | 2.644 | 125 | 16 | 2 | within |
| notice-burst-2 | 14.144 | 125 | 16 | 2 | within |
| notice-burst-2 | 14.282 | 125 | 16 | 2 | within |
| notice-burst-2 | 14.459 | 125 | 16 | 2 | within |
| notice-burst-2 | 4.603 | 125 | 16 | 2 | within |
| notice-burst-3 | 11.780 | 125 | 16 | 0 | within |
| notice-burst-3 | 11.963 | 125 | 16 | 0 | within |
| notice-burst-3 | 1.903 | 125 | 16 | 0 | within |
| notice-burst-3 | 2.088 | 125 | 16 | 0 | within |
| notice-burst-3 | 2.247 | 125 | 16 | 0 | within |
| notice-burst-3 | 2.475 | 125 | 16 | 0 | within |
| notice-burst-3 | 4.250 | 125 | 16 | 0 | within |
| notice-burst-3 | 12.149 | 125 | 16 | 0 | within |
| notice-burst-3 | 12.855 | 125 | 16 | 0 | within |
| notice-burst-3 | 12.992 | 125 | 16 | 0 | within |
| notice-burst-3 | 13.170 | 125 | 16 | 0 | within |
| notice-burst-3 | 14.903 | 125 | 16 | 0 | within |
| notice-burst-4 | 10.479 | 125 | 16 | 1 | within |
| notice-burst-4 | 10.662 | 125 | 16 | 1 | within |
| notice-burst-4 | 10.830 | 125 | 16 | 1 | within |
| notice-burst-4 | 12.168 | 125 | 16 | 1 | within |
| notice-burst-4 | 2.857 | 125 | 16 | 1 | within |
| notice-burst-4 | 12.355 | 125 | 16 | 1 | within |
| notice-burst-4 | 12.519 | 125 | 16 | 1 | within |
| notice-burst-4 | 14.271 | 125 | 16 | 1 | within |
| notice-burst-4 | 14.425 | 125 | 16 | 1 | within |
| notice-burst-4 | 14.560 | 125 | 16 | 1 | within |
| notice-burst-4 | 16.149 | 125 | 16 | 1 | within |
| notice-burst-4 | 16.331 | 125 | 16 | 1 | within |
| notice-burst-5 | 5.947 | 125 | 16 | 0 | within |
| notice-burst-5 | 6.128 | 125 | 16 | 0 | within |
| notice-burst-5 | 8.371 | 125 | 16 | 0 | within |
| notice-burst-5 | 16.014 | 125 | 16 | 0 | within |
| notice-burst-5 | 16.188 | 125 | 16 | 0 | within |
| notice-burst-5 | 16.365 | 125 | 16 | 0 | within |
| notice-burst-5 | 17.957 | 125 | 16 | 0 | within |
| notice-burst-5 | 18.134 | 125 | 16 | 0 | within |
| notice-burst-5 | 6.287 | 125 | 16 | 0 | within |
| notice-burst-5 | 6.490 | 125 | 16 | 0 | within |
| notice-burst-5 | 6.673 | 125 | 16 | 0 | within |
| notice-burst-5 | 18.315 | 125 | 16 | 0 | within |
| notice-burst-6 | 7.658 | 125 | 16 | 1 | within |
| notice-burst-6 | 15.281 | 125 | 16 | 1 | within |
| notice-burst-6 | 15.464 | 125 | 16 | 1 | within |
| notice-burst-6 | 15.645 | 125 | 16 | 1 | within |
| notice-burst-6 | 17.085 | 125 | 16 | 1 | within |
| notice-burst-6 | 17.263 | 125 | 16 | 1 | within |
| notice-burst-6 | 2.418 | 125 | 16 | 1 | within |
| notice-burst-6 | 2.602 | 125 | 16 | 1 | within |
| notice-burst-6 | 17.416 | 125 | 16 | 1 | within |
| notice-burst-6 | 19.108 | 125 | 16 | 1 | within |
| notice-burst-6 | 19.288 | 125 | 16 | 1 | within |
| notice-burst-6 | 3.185 | 125 | 16 | 1 | within |
| notice-burst-7 | 8.953 | 125 | 16 | 0 | within |
| notice-burst-7 | 15.078 | 125 | 16 | 0 | within |
| notice-burst-7 | 15.261 | 125 | 16 | 0 | within |
| notice-burst-7 | 15.441 | 125 | 16 | 0 | within |
| notice-burst-7 | 2.163 | 125 | 16 | 0 | within |
| notice-burst-7 | 2.345 | 125 | 16 | 0 | within |
| notice-burst-7 | 2.503 | 125 | 16 | 0 | within |
| notice-burst-7 | 2.907 | 125 | 16 | 0 | within |
| notice-burst-7 | 17.001 | 125 | 16 | 0 | within |
| notice-burst-7 | 17.139 | 125 | 16 | 0 | within |
| notice-burst-7 | 17.317 | 125 | 16 | 0 | within |
| notice-burst-7 | 3.523 | 125 | 16 | 0 | within |

Latest: 19.288 ms, notice-burst-6.

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
| notice-every-7 | 307 | 92,983 (0.930) | 76,872 (0.769) |
| notice-burst-0 | 317 | 104,564 (1.046) | 78,769 (0.788) |
| notice-burst-1 | 317 | 112,023 (1.120) | 78,828 (0.788) |
| notice-burst-2 | 317 | 104,514 (1.045) | 78,769 (0.788) |
| notice-burst-3 | 317 | 109,168 (1.092) | 78,769 (0.788) |
| notice-burst-4 | 317 | 98,565 (0.986) | 78,769 (0.788) |
| notice-burst-5 | 317 | 100,149 (1.001) | 78,828 (0.788) |
| notice-burst-6 | 317 | 100,931 (1.009) | 78,828 (0.788) |
| notice-burst-7 | 317 | 113,129 (1.131) | 78,828 (0.788) |

Longest pass that carries a step: 113,129 CPU cycles (1.131 ms), notice-burst-7; longest step: 78,828 (0.788 ms), notice-burst-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 781,349 | 7.813 | 125 | 129 | fits | 56,271 | 152 | 0.246 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 799,346 | 7.993 | 125 | 129 | fits | 56,271 | 152 | 0.246 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 186,620 | 1.866 | 125 | 129 | fits | 63,493 | 153 | 0.246 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 205,026 | 2.050 | 125 | 129 | fits | 63,493 | 153 | 0.246 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 382,672 | 3.827 | 125 | 129 | fits | 61,029 | 153 | 0.228 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 400,825 | 4.008 | 125 | 129 | fits | 61,029 | 153 | 0.228 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 594,241 | 5.942 | 125 | 129 | fits | 40,662 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 612,317 | 6.123 | 125 | 129 | fits | 40,662 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 814,624 | 8.146 | 125 | 129 | fits | 56,271 | 152 | 0.246 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 983,167 | 9.832 | 125 | 129 | fits | 19,505 | 51 | 0.346 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 223,962 | 2.240 | 125 | 129 | fits | 63,493 | 153 | 0.246 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 419,767 | 4.198 | 125 | 129 | fits | 61,029 | 153 | 0.228 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 482,025 | 4.820 | 20 | 200 | fits | 145,134 | 134 | 0.409 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 561,396 | 5.614 | 20 | 20 | fits | 99,639 | 67 | 0.683 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 441,553 | 4.416 | 20 | 24 | fits | 145,134 | 134 | 0.409 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 521,921 | 5.219 | 20 | 50 | fits | 99,639 | 67 | 0.683 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 897,388 | 8.974 | 20 | 20 | fits | 50,890 | 39 | 0.686 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 115,631 | 1.156 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 215,722 | 2.157 | 125 | 129 | fits | 59,132 | 153 | 0.267 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 233,764 | 2.338 | 125 | 129 | fits | 59,132 | 153 | 0.267 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 408,039 | 4.080 | 125 | 129 | fits | 59,734 | 158 | 0.252 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 426,480 | 4.265 | 125 | 129 | fits | 59,734 | 158 | 0.252 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 605,174 | 6.052 | 125 | 129 | fits | 58,954 | 155 | 0.221 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 622,981 | 6.230 | 125 | 129 | fits | 58,954 | 155 | 0.221 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 819,128 | 8.191 | 125 | 129 | fits | 57,477 | 153 | 0.213 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 836,973 | 8.370 | 125 | 129 | fits | 57,477 | 153 | 0.213 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 249,590 | 2.496 | 125 | 129 | fits | 59,132 | 153 | 0.267 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 442,044 | 4.420 | 125 | 129 | fits | 59,734 | 158 | 0.252 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 641,332 | 6.413 | 125 | 129 | fits | 58,954 | 155 | 0.221 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 854,967 | 8.550 | 125 | 129 | fits | 57,477 | 153 | 0.213 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 474,944 | 4.749 | 20 | 200 | fits | 145,591 | 148 | 0.404 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 558,669 | 5.587 | 20 | 20 | fits | 103,993 | 70 | 0.660 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 434,472 | 4.345 | 20 | 24 | fits | 145,591 | 148 | 0.404 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 519,194 | 5.192 | 20 | 50 | fits | 103,993 | 70 | 0.660 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 889,353 | 8.894 | 20 | 20 | fits | 62,459 | 46 | 0.654 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 88,687 | 0.887 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 411,465 | 4.115 | 125 | 129 | fits | 58,920 | 153 | 0.259 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 429,655 | 4.297 | 125 | 129 | fits | 58,920 | 153 | 0.259 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 608,299 | 6.083 | 125 | 129 | fits | 56,800 | 151 | 0.236 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 626,536 | 6.265 | 125 | 129 | fits | 56,800 | 151 | 0.236 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 801,673 | 8.017 | 125 | 129 | fits | 58,122 | 155 | 0.218 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 819,480 | 8.195 | 125 | 129 | fits | 58,122 | 155 | 0.218 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 199,110 | 1.991 | 125 | 129 | fits | 62,448 | 155 | 0.241 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 217,651 | 2.177 | 125 | 129 | fits | 62,448 | 155 | 0.241 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 445,329 | 4.453 | 125 | 129 | fits | 58,920 | 153 | 0.259 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 641,659 | 6.417 | 125 | 129 | fits | 56,800 | 151 | 0.236 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 236,361 | 2.364 | 125 | 129 | fits | 62,448 | 155 | 0.241 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 837,760 | 8.378 | 125 | 129 | fits | 58,122 | 155 | 0.218 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 486,422 | 4.864 | 20 | 200 | fits | 146,450 | 148 | 0.410 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 571,372 | 5.714 | 20 | 20 | fits | 105,218 | 71 | 0.667 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 445,950 | 4.460 | 20 | 24 | fits | 146,450 | 148 | 0.410 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 531,897 | 5.319 | 20 | 50 | fits | 105,218 | 71 | 0.667 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 894,175 | 8.942 | 20 | 20 | fits | 56,954 | 37 | 0.622 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 96,126 | 0.961 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 376,730 | 3.767 | 125 | 129 | fits | 58,929 | 155 | 0.256 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 394,882 | 3.949 | 125 | 129 | fits | 58,929 | 155 | 0.256 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 573,782 | 5.738 | 125 | 129 | fits | 57,027 | 153 | 0.238 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 592,019 | 5.920 | 125 | 129 | fits | 57,027 | 153 | 0.238 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 785,135 | 7.851 | 125 | 129 | fits | 57,929 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 802,980 | 8.030 | 125 | 129 | fits | 57,929 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 179,893 | 1.799 | 125 | 129 | fits | 62,025 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 198,328 | 1.983 | 125 | 129 | fits | 62,025 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 410,556 | 4.106 | 125 | 129 | fits | 58,929 | 155 | 0.256 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 607,142 | 6.071 | 125 | 129 | fits | 57,027 | 153 | 0.238 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 217,120 | 2.171 | 125 | 129 | fits | 62,025 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 821,260 | 8.213 | 125 | 129 | fits | 57,929 | 153 | 0.217 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 487,349 | 4.873 | 20 | 200 | fits | 150,011 | 155 | 0.410 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 562,734 | 5.627 | 20 | 20 | fits | 95,653 | 49 | 0.681 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 446,877 | 4.469 | 20 | 24 | fits | 150,011 | 155 | 0.410 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 427,606 | 4.276 | 20 | 50 | fits | 150,011 | 155 | 0.410 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 900,927 | 9.009 | 20 | 20 | fits | 50,564 | 33 | 0.712 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 101,094 | 1.011 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 623,921 | 6.239 | 125 | 129 | fits | 56,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 641,991 | 6.420 | 125 | 129 | fits | 56,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 817,671 | 8.177 | 125 | 129 | fits | 55,660 | 151 | 0.233 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 835,908 | 8.359 | 125 | 129 | fits | 55,660 | 151 | 0.233 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 215,458 | 2.155 | 125 | 129 | fits | 61,931 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 233,764 | 2.338 | 125 | 129 | fits | 61,931 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 410,134 | 4.101 | 125 | 129 | fits | 62,173 | 160 | 0.221 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 428,518 | 4.285 | 125 | 129 | fits | 62,173 | 160 | 0.221 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 657,435 | 6.574 | 125 | 129 | fits | 56,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 850,812 | 8.508 | 125 | 129 | fits | 55,660 | 151 | 0.233 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 252,539 | 2.525 | 125 | 129 | fits | 61,931 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 447,395 | 4.474 | 125 | 129 | fits | 62,173 | 160 | 0.221 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 155,503 | 1.555 | 20 | 200 | fits | 144,488 | 189 | 0.323 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 562,623 | 5.626 | 20 | 20 | fits | 109,059 | 82 | 0.625 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 433,360 | 4.334 | 20 | 24 | fits | 144,941 | 147 | 0.413 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 523,148 | 5.231 | 20 | 50 | fits | 109,059 | 82 | 0.625 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 910,278 | 9.103 | 20 | 20 | fits | 60,124 | 43 | 0.662 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 86,034 | 0.860 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 588,530 | 5.885 | 125 | 129 | fits | 56,944 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 606,598 | 6.066 | 125 | 129 | fits | 56,944 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 779,406 | 7.794 | 125 | 129 | fits | 55,581 | 151 | 0.233 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 797,643 | 7.976 | 125 | 129 | fits | 55,581 | 151 | 0.233 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 180,030 | 1.800 | 125 | 129 | fits | 61,654 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 198,234 | 1.982 | 125 | 129 | fits | 61,654 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 375,632 | 3.756 | 125 | 129 | fits | 61,605 | 155 | 0.227 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 394,016 | 3.940 | 125 | 129 | fits | 61,605 | 155 | 0.227 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 622,042 | 6.220 | 125 | 129 | fits | 56,944 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 812,547 | 8.125 | 125 | 129 | fits | 55,581 | 151 | 0.233 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 217,078 | 2.171 | 125 | 129 | fits | 61,654 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 412,893 | 4.129 | 125 | 129 | fits | 61,605 | 155 | 0.227 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 152,624 | 1.526 | 20 | 200 | fits | 149,770 | 191 | 0.307 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 563,638 | 5.636 | 20 | 20 | fits | 96,069 | 51 | 0.683 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 447,365 | 4.474 | 20 | 24 | fits | 154,799 | 172 | 0.400 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 428,094 | 4.281 | 20 | 50 | fits | 154,799 | 172 | 0.400 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 896,455 | 8.965 | 20 | 20 | fits | 49,912 | 33 | 0.701 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 102,028 | 1.020 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 585,842 | 5.858 | 125 | 129 | fits | 56,944 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 603,910 | 6.039 | 125 | 129 | fits | 56,944 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 777,750 | 7.777 | 125 | 129 | fits | 55,826 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 795,987 | 7.960 | 125 | 129 | fits | 55,826 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 179,990 | 1.800 | 125 | 129 | fits | 61,852 | 155 | 0.235 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 198,194 | 1.982 | 125 | 129 | fits | 61,852 | 155 | 0.235 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 375,994 | 3.760 | 125 | 129 | fits | 61,649 | 155 | 0.228 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 394,378 | 3.944 | 125 | 129 | fits | 61,649 | 155 | 0.228 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 619,354 | 6.194 | 125 | 129 | fits | 56,944 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 810,891 | 8.109 | 125 | 129 | fits | 55,826 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 217,038 | 2.170 | 125 | 129 | fits | 61,852 | 155 | 0.235 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 413,255 | 4.133 | 125 | 129 | fits | 61,649 | 155 | 0.228 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 500,935 | 5.009 | 20 | 200 | fits | 149,303 | 148 | 0.429 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 598,659 | 5.987 | 20 | 20 | fits | 103,647 | 84 | 0.681 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 460,463 | 4.605 | 20 | 24 | fits | 149,303 | 148 | 0.429 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 559,184 | 5.592 | 20 | 50 | fits | 103,647 | 84 | 0.681 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 906,790 | 9.068 | 20 | 20 | fits | 41,536 | 29 | 0.748 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 86,462 | 0.865 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 215,490 | 2.155 | 125 | 129 | fits | 59,380 | 155 | 0.269 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 233,614 | 2.336 | 125 | 129 | fits | 59,380 | 155 | 0.269 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 427,599 | 4.276 | 125 | 129 | fits | 59,038 | 151 | 0.260 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 446,078 | 4.461 | 125 | 129 | fits | 59,038 | 151 | 0.260 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 607,316 | 6.073 | 125 | 129 | fits | 58,913 | 155 | 0.222 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 625,161 | 6.252 | 125 | 129 | fits | 58,913 | 155 | 0.222 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 818,113 | 8.181 | 125 | 129 | fits | 57,553 | 153 | 0.214 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 835,958 | 8.360 | 125 | 129 | fits | 57,553 | 153 | 0.214 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 249,440 | 2.494 | 125 | 129 | fits | 59,380 | 155 | 0.269 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 461,642 | 4.616 | 125 | 129 | fits | 59,038 | 151 | 0.260 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 643,512 | 6.435 | 125 | 129 | fits | 58,913 | 155 | 0.222 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 853,952 | 8.540 | 125 | 129 | fits | 57,553 | 153 | 0.214 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 488,484 | 4.885 | 20 | 200 | fits | 154,993 | 168 | 0.396 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 568,641 | 5.686 | 20 | 20 | fits | 100,425 | 54 | 0.684 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 448,012 | 4.480 | 20 | 24 | fits | 154,993 | 168 | 0.396 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 428,741 | 4.287 | 20 | 50 | fits | 154,993 | 168 | 0.396 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 890,144 | 8.901 | 20 | 20 | fits | 32,672 | 25 | 0.794 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 108,570 | 1.086 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 955,927 | 9.559 | 125 | 129 | fits | 24,685 | 51 | 0.462 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,424,302 | 14.243 | 125 | 129 | fits | 62,241 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,442,535 | 14.425 | 125 | 129 | fits | 62,241 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,460,558 | 14.606 | 125 | 129 | fits | 62,241 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 214,042 | 2.140 | 125 | 129 | fits | 55,293 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 232,175 | 2.322 | 125 | 129 | fits | 55,293 | 111 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 387,949 | 3.879 | 125 | 129 | fits | 42,843 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 406,244 | 4.062 | 125 | 129 | fits | 42,843 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,615,213 | 16.152 | 125 | 129 | fits | 51,636 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,628,898 | 16.289 | 125 | 129 | fits | 51,636 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,646,669 | 16.467 | 125 | 129 | fits | 51,636 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 464,987 | 4.650 | 125 | 129 | fits | 37,991 | 60 | 0.366 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 152,060 | 1.521 | 20 | 200 | fits | 151,960 | 191 | 0.322 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 550,394 | 5.504 | 20 | 20 | fits | 98,954 | 63 | 0.681 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 406,551 | 4.066 | 20 | 24 | fits | 146,336 | 157 | 0.400 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 387,280 | 3.873 | 20 | 50 | fits | 146,336 | 157 | 0.400 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 832,831 | 8.328 | 20 | 20 | fits | 54,909 | 30 | 0.629 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 886,223 | 8.862 | 125 | 129 | fits | 24,997 | 52 | 0.465 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,358,725 | 13.587 | 125 | 129 | fits | 62,364 | 153 | 0.273 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,377,148 | 13.771 | 125 | 129 | fits | 62,364 | 153 | 0.273 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,395,223 | 13.952 | 125 | 129 | fits | 62,364 | 153 | 0.273 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 1,523,608 | 15.236 | 125 | 129 | fits | 55,003 | 152 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 1,541,415 | 15.414 | 125 | 129 | fits | 55,003 | 152 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 316,819 | 3.168 | 125 | 129 | fits | 56,500 | 111 | 0.329 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 335,399 | 3.354 | 125 | 129 | fits | 56,500 | 111 | 0.329 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,556,542 | 15.565 | 125 | 129 | fits | 55,003 | 152 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,709,999 | 17.100 | 125 | 129 | fits | 37,334 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,727,810 | 17.278 | 125 | 129 | fits | 37,334 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 566,523 | 5.665 | 125 | 129 | fits | 25,983 | 53 | 0.340 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 151,182 | 1.512 | 20 | 200 | fits | 151,384 | 196 | 0.328 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 579,112 | 5.791 | 20 | 20 | fits | 102,796 | 72 | 0.679 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 431,115 | 4.311 | 20 | 24 | fits | 143,567 | 150 | 0.395 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 411,844 | 4.118 | 20 | 50 | fits | 143,567 | 150 | 0.395 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 861,823 | 8.618 | 20 | 20 | fits | 55,001 | 30 | 0.631 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 892,288 | 8.923 | 125 | 129 | fits | 25,808 | 51 | 0.483 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,251,973 | 12.520 | 125 | 129 | fits | 61,524 | 153 | 0.261 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,270,265 | 12.703 | 125 | 129 | fits | 61,524 | 153 | 0.261 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,288,369 | 12.884 | 125 | 129 | fits | 61,524 | 153 | 0.261 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 206,859 | 2.069 | 125 | 129 | fits | 71,735 | 161 | 0.289 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 225,060 | 2.251 | 125 | 129 | fits | 71,735 | 161 | 0.289 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 241,030 | 2.410 | 125 | 129 | fits | 71,735 | 161 | 0.289 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 264,402 | 2.644 | 125 | 129 | fits | 23,124 | 53 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,414,422 | 14.144 | 125 | 129 | fits | 51,569 | 152 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,428,158 | 14.282 | 125 | 129 | fits | 51,569 | 152 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,445,859 | 14.459 | 125 | 129 | fits | 51,569 | 152 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 460,266 | 4.603 | 125 | 129 | fits | 25,819 | 52 | 0.342 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 149,728 | 1.497 | 20 | 200 | fits | 150,150 | 192 | 0.325 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 561,214 | 5.612 | 20 | 20 | fits | 98,432 | 49 | 0.683 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 442,578 | 4.426 | 20 | 24 | fits | 156,754 | 153 | 0.390 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 423,307 | 4.233 | 20 | 50 | fits | 156,754 | 153 | 0.390 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 860,330 | 8.603 | 20 | 20 | fits | 46,383 | 26 | 0.673 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,178,020 | 11.780 | 125 | 129 | fits | 63,225 | 153 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,196,345 | 11.963 | 125 | 129 | fits | 63,225 | 153 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 190,306 | 1.903 | 125 | 129 | fits | 71,722 | 161 | 0.279 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 208,781 | 2.088 | 125 | 129 | fits | 71,722 | 161 | 0.279 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 224,669 | 2.247 | 125 | 129 | fits | 71,722 | 161 | 0.279 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 247,506 | 2.475 | 125 | 129 | fits | 22,821 | 53 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 424,950 | 4.250 | 125 | 129 | fits | 22,260 | 52 | 0.383 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,214,881 | 12.149 | 125 | 129 | fits | 63,225 | 153 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,285,506 | 12.855 | 125 | 129 | fits | 52,314 | 152 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,299,191 | 12.992 | 125 | 129 | fits | 52,314 | 152 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,316,962 | 13.170 | 125 | 129 | fits | 52,314 | 152 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 1,490,346 | 14.903 | 125 | 129 | fits | 23,735 | 52 | 0.304 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 565,913 | 5.659 | 20 | 200 | fits | 147,295 | 172 | 0.314 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 643,540 | 6.435 | 20 | 20 | fits | 97,895 | 49 | 0.676 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 378,146 | 3.781 | 20 | 24 | fits | 152,987 | 178 | 0.401 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 506,170 | 5.062 | 20 | 50 | fits | 147,295 | 172 | 0.314 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 910,710 | 9.107 | 20 | 20 | fits | 38,197 | 22 | 0.725 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,047,935 | 10.479 | 125 | 129 | fits | 61,574 | 152 | 0.287 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,066,181 | 10.662 | 125 | 129 | fits | 61,574 | 152 | 0.287 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,083,030 | 10.830 | 125 | 129 | fits | 61,574 | 152 | 0.287 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,216,824 | 12.168 | 125 | 129 | fits | 59,322 | 153 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 285,665 | 2.857 | 125 | 129 | fits | 24,477 | 52 | 0.445 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,235,471 | 12.355 | 125 | 129 | fits | 59,322 | 153 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,251,874 | 12.519 | 125 | 129 | fits | 59,322 | 153 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,427,073 | 14.271 | 125 | 129 | fits | 52,957 | 152 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,442,467 | 14.425 | 125 | 129 | fits | 52,957 | 152 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,456,028 | 14.560 | 125 | 129 | fits | 52,957 | 152 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,614,864 | 16.149 | 125 | 129 | fits | 41,462 | 103 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,633,102 | 16.331 | 125 | 129 | fits | 41,462 | 103 | 0.230 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 487,719 | 4.877 | 20 | 200 | fits | 146,932 | 154 | 0.380 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 562,653 | 5.627 | 20 | 20 | fits | 95,202 | 48 | 0.684 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 447,247 | 4.472 | 20 | 24 | fits | 146,932 | 154 | 0.380 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 427,976 | 4.280 | 20 | 50 | fits | 146,932 | 154 | 0.380 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 849,129 | 8.491 | 20 | 20 | fits | 56,227 | 36 | 0.617 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 594,679 | 5.947 | 125 | 129 | fits | 72,435 | 161 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 612,832 | 6.128 | 125 | 129 | fits | 72,435 | 161 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 837,072 | 8.371 | 125 | 129 | fits | 23,107 | 52 | 0.392 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,601,436 | 16.014 | 125 | 129 | fits | 61,334 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,618,778 | 16.188 | 125 | 129 | fits | 61,334 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,636,463 | 16.365 | 125 | 129 | fits | 61,334 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,795,665 | 17.957 | 125 | 129 | fits | 57,676 | 153 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,813,401 | 18.134 | 125 | 129 | fits | 57,676 | 153 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 628,659 | 6.287 | 125 | 129 | fits | 72,435 | 161 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 648,967 | 6.490 | 125 | 129 | fits | 38,001 | 102 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 667,337 | 6.673 | 125 | 129 | fits | 38,001 | 102 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 1,831,462 | 18.315 | 125 | 129 | fits | 57,676 | 153 | 0.216 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 565,458 | 5.655 | 20 | 200 | fits | 149,172 | 181 | 0.307 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 647,211 | 6.472 | 20 | 20 | fits | 102,021 | 52 | 0.648 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 375,814 | 3.758 | 20 | 24 | fits | 151,035 | 172 | 0.407 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 505,715 | 5.057 | 20 | 50 | fits | 149,172 | 181 | 0.307 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 922,034 | 9.220 | 20 | 20 | fits | 38,197 | 22 | 0.725 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 765,752 | 7.658 | 125 | 129 | fits | 24,946 | 52 | 0.455 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,528,122 | 15.281 | 125 | 129 | fits | 62,361 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,546,363 | 15.464 | 125 | 129 | fits | 62,361 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,564,457 | 15.645 | 125 | 129 | fits | 62,361 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,708,507 | 17.085 | 125 | 129 | fits | 55,090 | 152 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,726,281 | 17.263 | 125 | 129 | fits | 55,090 | 152 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 241,770 | 2.418 | 125 | 129 | fits | 56,149 | 110 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 260,172 | 2.602 | 125 | 129 | fits | 56,149 | 110 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 1,741,559 | 17.416 | 125 | 129 | fits | 55,090 | 152 | 0.240 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 1,910,800 | 19.108 | 125 | 129 | fits | 37,550 | 102 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 1,928,812 | 19.288 | 125 | 129 | fits | 37,550 | 102 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 318,519 | 3.185 | 125 | 129 | fits | 38,037 | 62 | 0.357 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 152,498 | 1.525 | 20 | 200 | fits | 147,721 | 189 | 0.327 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 558,003 | 5.580 | 20 | 20 | fits | 102,824 | 52 | 0.661 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 434,975 | 4.350 | 20 | 24 | fits | 145,476 | 157 | 0.397 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 415,704 | 4.157 | 20 | 50 | fits | 145,476 | 157 | 0.397 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 832,558 | 8.326 | 20 | 20 | fits | 46,610 | 26 | 0.674 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 895,320 | 8.953 | 125 | 129 | fits | 23,786 | 53 | 0.433 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,507,777 | 15.078 | 125 | 129 | fits | 62,322 | 153 | 0.272 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,526,089 | 15.261 | 125 | 129 | fits | 62,322 | 153 | 0.272 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,544,114 | 15.441 | 125 | 129 | fits | 62,322 | 153 | 0.272 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 216,330 | 2.163 | 125 | 129 | fits | 58,297 | 152 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 234,501 | 2.345 | 125 | 129 | fits | 58,297 | 152 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 250,263 | 2.503 | 125 | 129 | fits | 58,297 | 152 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 290,744 | 2.907 | 125 | 129 | fits | 41,479 | 68 | 0.436 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,700,112 | 17.001 | 125 | 129 | fits | 51,833 | 152 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,713,881 | 17.139 | 125 | 129 | fits | 51,833 | 152 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,731,652 | 17.317 | 125 | 129 | fits | 51,833 | 152 | 0.208 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 352,286 | 3.523 | 125 | 129 | fits | 113,129 | 60 | 0.262 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 148,178 | 1.482 | 20 | 200 | fits | 149,951 | 188 | 0.302 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 551,940 | 5.519 | 20 | 20 | fits | 103,227 | 52 | 0.665 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 428,509 | 4.285 | 20 | 24 | fits | 147,732 | 166 | 0.411 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 409,238 | 4.092 | 20 | 50 | fits | 147,732 | 166 | 0.411 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 826,239 | 8.262 | 20 | 20 | fits | 38,060 | 22 | 0.728 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
