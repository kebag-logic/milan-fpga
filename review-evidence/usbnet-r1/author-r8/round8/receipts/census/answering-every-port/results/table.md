### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

0 of 7 paths and 0 of 248 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 7.055 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.adp.if0` (notice-burst-5) | 6.034 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-7.held.aecp.if0` (notice-burst-7) | 4.916 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.maap.if0` (notice-burst-4) | 5.566 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.srp.if0` (notice-burst-5) | 11.719 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 1.273 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.36.0.if0` (notice-burst-6) | 20.760 (20.998) | fits | 0 events | 160 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1887 | 0 | 120,187 (1.502) | fits |
| notice-every-1 | 1897 | 0 | 121,298 (1.516) | fits |
| notice-every-2 | 1893 | 0 | 120,099 (1.501) | fits |
| notice-every-3 | 1886 | 0 | 121,911 (1.524) | fits |
| notice-every-4 | 1886 | 0 | 120,249 (1.503) | fits |
| notice-every-5 | 1892 | 0 | 120,415 (1.505) | fits |
| notice-every-6 | 1885 | 0 | 120,362 (1.505) | fits |
| notice-every-7 | 1879 | 0 | 122,471 (1.531) | fits |
| notice-burst-0 | 1244 | 0 | 126,736 (1.584) | fits |
| notice-burst-1 | 1261 | 0 | 136,518 (1.706) | fits |
| notice-burst-2 | 1200 | 0 | 124,307 (1.554) | fits |
| notice-burst-3 | 1232 | 0 | 121,731 (1.522) | fits |
| notice-burst-4 | 1268 | 0 | 119,764 (1.497) | fits |
| notice-burst-5 | 1244 | 0 | 123,024 (1.538) | fits |
| notice-burst-6 | 1230 | 0 | 121,926 (1.524) | fits |
| notice-burst-7 | 1246 | 0 | 143,391 (1.792) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.105 | 125 | 16 | 1 | within |
| notice-every-0 | 8.325 | 125 | 16 | 1 | within |
| notice-every-0 | 2.042 | 125 | 16 | 1 | within |
| notice-every-0 | 2.270 | 125 | 16 | 1 | within |
| notice-every-0 | 4.190 | 125 | 16 | 1 | within |
| notice-every-0 | 4.413 | 125 | 16 | 1 | within |
| notice-every-0 | 8.489 | 125 | 16 | 1 | within |
| notice-every-0 | 8.631 | 125 | 16 | 1 | within |
| notice-every-0 | 2.489 | 125 | 16 | 1 | within |
| notice-every-0 | 2.707 | 125 | 16 | 1 | within |
| notice-every-1 | 4.171 | 125 | 16 | 2 | within |
| notice-every-1 | 4.393 | 125 | 16 | 2 | within |
| notice-every-1 | 6.285 | 125 | 16 | 2 | within |
| notice-every-1 | 6.507 | 125 | 16 | 2 | within |
| notice-every-1 | 8.364 | 125 | 16 | 2 | within |
| notice-every-1 | 8.580 | 125 | 16 | 2 | within |
| notice-every-1 | 4.565 | 125 | 16 | 2 | within |
| notice-every-1 | 4.716 | 125 | 16 | 2 | within |
| notice-every-1 | 6.726 | 125 | 16 | 2 | within |
| notice-every-1 | 7.151 | 125 | 16 | 2 | within |
| notice-every-2 | 4.010 | 125 | 16 | 1 | within |
| notice-every-2 | 4.231 | 125 | 16 | 1 | within |
| notice-every-2 | 6.128 | 125 | 16 | 1 | within |
| notice-every-2 | 6.349 | 125 | 16 | 1 | within |
| notice-every-2 | 8.207 | 125 | 16 | 1 | within |
| notice-every-2 | 8.423 | 125 | 16 | 1 | within |
| notice-every-2 | 4.404 | 125 | 16 | 1 | within |
| notice-every-2 | 4.555 | 125 | 16 | 1 | within |
| notice-every-2 | 6.567 | 125 | 16 | 1 | within |
| notice-every-2 | 6.994 | 125 | 16 | 1 | within |
| notice-every-3 | 6.125 | 125 | 16 | 2 | within |
| notice-every-3 | 6.345 | 125 | 16 | 2 | within |
| notice-every-3 | 8.045 | 125 | 16 | 2 | within |
| notice-every-3 | 8.265 | 125 | 16 | 2 | within |
| notice-every-3 | 2.049 | 125 | 16 | 2 | within |
| notice-every-3 | 2.277 | 125 | 16 | 2 | within |
| notice-every-3 | 6.514 | 125 | 16 | 2 | within |
| notice-every-3 | 6.667 | 125 | 16 | 2 | within |
| notice-every-3 | 2.496 | 125 | 16 | 2 | within |
| notice-every-3 | 2.713 | 125 | 16 | 2 | within |
| notice-every-4 | 2.128 | 125 | 16 | 2 | within |
| notice-every-4 | 2.353 | 125 | 16 | 2 | within |
| notice-every-4 | 4.092 | 125 | 16 | 2 | within |
| notice-every-4 | 4.312 | 125 | 16 | 2 | within |
| notice-every-4 | 8.175 | 125 | 16 | 2 | within |
| notice-every-4 | 8.393 | 125 | 16 | 2 | within |
| notice-every-4 | 2.525 | 125 | 16 | 2 | within |
| notice-every-4 | 2.676 | 125 | 16 | 2 | within |
| notice-every-4 | 4.529 | 125 | 16 | 2 | within |
| notice-every-4 | 4.995 | 125 | 16 | 2 | within |
| notice-every-5 | 8.064 | 125 | 16 | 2 | within |
| notice-every-5 | 8.283 | 125 | 16 | 2 | within |
| notice-every-5 | 1.915 | 125 | 16 | 2 | within |
| notice-every-5 | 2.144 | 125 | 16 | 2 | within |
| notice-every-5 | 6.030 | 125 | 16 | 2 | within |
| notice-every-5 | 6.254 | 125 | 16 | 2 | within |
| notice-every-5 | 8.448 | 125 | 16 | 2 | within |
| notice-every-5 | 8.589 | 125 | 16 | 2 | within |
| notice-every-5 | 2.364 | 125 | 16 | 2 | within |
| notice-every-5 | 2.844 | 125 | 16 | 2 | within |
| notice-every-6 | 5.982 | 125 | 16 | 2 | within |
| notice-every-6 | 6.202 | 125 | 16 | 2 | within |
| notice-every-6 | 1.860 | 125 | 16 | 2 | within |
| notice-every-6 | 2.089 | 125 | 16 | 2 | within |
| notice-every-6 | 7.845 | 125 | 16 | 2 | within |
| notice-every-6 | 8.062 | 125 | 16 | 2 | within |
| notice-every-6 | 6.372 | 125 | 16 | 2 | within |
| notice-every-6 | 6.524 | 125 | 16 | 2 | within |
| notice-every-6 | 2.308 | 125 | 16 | 2 | within |
| notice-every-6 | 2.785 | 125 | 16 | 2 | within |
| notice-every-7 | 2.152 | 125 | 16 | 2 | within |
| notice-every-7 | 2.374 | 125 | 16 | 2 | within |
| notice-every-7 | 4.109 | 125 | 16 | 2 | within |
| notice-every-7 | 4.330 | 125 | 16 | 2 | within |
| notice-every-7 | 8.159 | 125 | 16 | 2 | within |
| notice-every-7 | 8.375 | 125 | 16 | 2 | within |
| notice-every-7 | 2.546 | 125 | 16 | 2 | within |
| notice-every-7 | 2.697 | 125 | 16 | 2 | within |
| notice-every-7 | 4.548 | 125 | 16 | 2 | within |
| notice-every-7 | 4.973 | 125 | 16 | 2 | within |
| notice-burst-0 | 8.502 | 125 | 16 | 1 | within |
| notice-burst-0 | 16.742 | 125 | 16 | 1 | within |
| notice-burst-0 | 2.775 | 125 | 16 | 1 | within |
| notice-burst-0 | 3.004 | 125 | 16 | 1 | within |
| notice-burst-0 | 3.203 | 125 | 16 | 1 | within |
| notice-burst-0 | 3.421 | 125 | 16 | 1 | within |
| notice-burst-0 | 16.912 | 125 | 16 | 1 | within |
| notice-burst-0 | 17.054 | 125 | 16 | 1 | within |
| notice-burst-0 | 17.462 | 125 | 16 | 1 | within |
| notice-burst-0 | 5.100 | 125 | 16 | 1 | within |
| notice-burst-1 | 8.907 | 125 | 16 | 0 | within |
| notice-burst-1 | 15.725 | 125 | 16 | 0 | within |
| notice-burst-1 | 1.794 | 125 | 16 | 0 | within |
| notice-burst-1 | 2.023 | 125 | 16 | 0 | within |
| notice-burst-1 | 3.395 | 125 | 16 | 0 | within |
| notice-burst-1 | 3.620 | 125 | 16 | 0 | within |
| notice-burst-1 | 15.894 | 125 | 16 | 0 | within |
| notice-burst-1 | 16.036 | 125 | 16 | 0 | within |
| notice-burst-1 | 16.441 | 125 | 16 | 0 | within |
| notice-burst-1 | 5.431 | 125 | 16 | 0 | within |
| notice-burst-2 | 14.683 | 125 | 16 | 0 | within |
| notice-burst-2 | 14.907 | 125 | 16 | 0 | within |
| notice-burst-2 | 2.732 | 125 | 16 | 0 | within |
| notice-burst-2 | 2.961 | 125 | 16 | 0 | within |
| notice-burst-2 | 4.828 | 125 | 16 | 0 | within |
| notice-burst-2 | 15.126 | 125 | 16 | 0 | within |
| notice-burst-2 | 15.286 | 125 | 16 | 0 | within |
| notice-burst-2 | 15.913 | 125 | 16 | 0 | within |
| notice-burst-2 | 16.125 | 125 | 16 | 0 | within |
| notice-burst-2 | 16.330 | 125 | 16 | 0 | within |
| notice-burst-3 | 13.757 | 125 | 16 | 0 | within |
| notice-burst-3 | 13.980 | 125 | 16 | 0 | within |
| notice-burst-3 | 3.879 | 125 | 16 | 0 | within |
| notice-burst-3 | 14.199 | 125 | 16 | 0 | within |
| notice-burst-3 | 14.392 | 125 | 16 | 0 | within |
| notice-burst-3 | 15.788 | 125 | 16 | 0 | within |
| notice-burst-3 | 15.955 | 125 | 16 | 0 | within |
| notice-burst-3 | 16.097 | 125 | 16 | 0 | within |
| notice-burst-3 | 16.491 | 125 | 16 | 0 | within |
| notice-burst-3 | 17.803 | 125 | 16 | 0 | within |
| notice-burst-4 | 11.858 | 125 | 16 | 0 | within |
| notice-burst-4 | 12.082 | 125 | 16 | 0 | within |
| notice-burst-4 | 3.381 | 125 | 16 | 0 | within |
| notice-burst-4 | 12.302 | 125 | 16 | 0 | within |
| notice-burst-4 | 12.496 | 125 | 16 | 0 | within |
| notice-burst-4 | 13.195 | 125 | 16 | 0 | within |
| notice-burst-4 | 13.361 | 125 | 16 | 0 | within |
| notice-burst-4 | 13.504 | 125 | 16 | 0 | within |
| notice-burst-4 | 13.895 | 125 | 16 | 0 | within |
| notice-burst-4 | 15.206 | 125 | 16 | 0 | within |
| notice-burst-5 | 5.216 | 125 | 16 | 1 | within |
| notice-burst-5 | 5.438 | 125 | 16 | 1 | within |
| notice-burst-5 | 7.897 | 125 | 16 | 1 | within |
| notice-burst-5 | 17.726 | 125 | 16 | 1 | within |
| notice-burst-5 | 17.938 | 125 | 16 | 1 | within |
| notice-burst-5 | 18.361 | 125 | 16 | 1 | within |
| notice-burst-5 | 5.610 | 125 | 16 | 1 | within |
| notice-burst-5 | 5.760 | 125 | 16 | 1 | within |
| notice-burst-5 | 6.051 | 125 | 16 | 1 | within |
| notice-burst-5 | 19.139 | 125 | 16 | 1 | within |
| notice-burst-6 | 6.943 | 125 | 16 | 0 | within |
| notice-burst-6 | 16.776 | 125 | 16 | 0 | within |
| notice-burst-6 | 17.004 | 125 | 16 | 0 | within |
| notice-burst-6 | 17.440 | 125 | 16 | 0 | within |
| notice-burst-6 | 18.379 | 125 | 16 | 0 | within |
| notice-burst-6 | 18.598 | 125 | 16 | 0 | within |
| notice-burst-6 | 18.759 | 125 | 16 | 0 | within |
| notice-burst-6 | 18.900 | 125 | 16 | 0 | within |
| notice-burst-6 | 20.373 | 125 | 16 | 0 | within |
| notice-burst-6 | 20.760 | 125 | 16 | 0 | within |
| notice-burst-7 | 9.431 | 125 | 16 | 1 | within |
| notice-burst-7 | 17.961 | 125 | 16 | 1 | within |
| notice-burst-7 | 3.517 | 125 | 16 | 1 | within |
| notice-burst-7 | 3.746 | 125 | 16 | 1 | within |
| notice-burst-7 | 3.945 | 125 | 16 | 1 | within |
| notice-burst-7 | 4.391 | 125 | 16 | 1 | within |
| notice-burst-7 | 18.131 | 125 | 16 | 1 | within |
| notice-burst-7 | 18.273 | 125 | 16 | 1 | within |
| notice-burst-7 | 18.681 | 125 | 16 | 1 | within |
| notice-burst-7 | 7.668 | 125 | 16 | 1 | within |

Latest: 20.760 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 385 | 91,904 (1.149) | 78,034 (0.975) |
| notice-every-1 | 385 | 91,904 (1.149) | 78,034 (0.975) |
| notice-every-2 | 385 | 91,904 (1.149) | 78,034 (0.975) |
| notice-every-3 | 385 | 91,904 (1.149) | 78,034 (0.975) |
| notice-every-4 | 385 | 91,904 (1.149) | 78,034 (0.975) |
| notice-every-5 | 385 | 91,904 (1.149) | 78,034 (0.975) |
| notice-every-6 | 385 | 91,904 (1.149) | 78,034 (0.975) |
| notice-every-7 | 385 | 91,904 (1.149) | 78,034 (0.975) |
| notice-burst-0 | 451 | 95,594 (1.195) | 78,141 (0.977) |
| notice-burst-1 | 450 | 114,926 (1.437) | 78,083 (0.976) |
| notice-burst-2 | 451 | 100,290 (1.254) | 78,154 (0.977) |
| notice-burst-3 | 452 | 99,377 (1.242) | 78,312 (0.979) |
| notice-burst-4 | 440 | 99,770 (1.247) | 78,325 (0.979) |
| notice-burst-5 | 440 | 99,368 (1.242) | 78,325 (0.979) |
| notice-burst-6 | 442 | 102,160 (1.277) | 78,325 (0.979) |
| notice-burst-7 | 440 | 95,374 (1.192) | 78,325 (0.979) |

Longest pass that carries a step: 114,926 CPU cycles (1.437 ms), notice-burst-1; longest step: 78,325 (0.979 ms), notice-burst-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 648,431 | 8.105 | 125 | 129 | fits | 64,768 | 204 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 665,994 | 8.325 | 125 | 129 | fits | 64,768 | 204 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 163,369 | 2.042 | 125 | 129 | fits | 78,318 | 208 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 181,622 | 2.270 | 125 | 129 | fits | 78,318 | 208 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 335,191 | 4.190 | 125 | 129 | fits | 42,094 | 103 | 0.251 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 353,054 | 4.413 | 125 | 129 | fits | 42,094 | 103 | 0.251 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 679,147 | 8.489 | 125 | 129 | fits | 64,768 | 204 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 690,490 | 8.631 | 125 | 129 | fits | 64,768 | 204 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 199,128 | 2.489 | 125 | 129 | fits | 78,318 | 208 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 216,533 | 2.707 | 125 | 129 | fits | 78,318 | 208 | 0.134 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 130,166 | 1.627 | 20 | 200 | fits | 118,403 | 251 | 0.250 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 444,935 | 5.562 | 20 | 20 | fits | 99,323 | 83 | 0.651 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 329,408 | 4.118 | 20 | 24 | fits | 114,532 | 83 | 0.388 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 413,460 | 5.168 | 20 | 50 | fits | 99,323 | 83 | 0.651 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 905,518 | 11.319 | 20 | 20 | fits | 80,509 | 41 | 0.698 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 76,480 | 0.956 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 333,669 | 4.171 | 125 | 129 | fits | 67,900 | 206 | 0.176 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 351,401 | 4.393 | 125 | 129 | fits | 67,900 | 206 | 0.176 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 502,837 | 6.285 | 125 | 129 | fits | 70,846 | 190 | 0.152 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 520,538 | 6.507 | 125 | 129 | fits | 70,846 | 190 | 0.152 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 669,123 | 8.364 | 125 | 129 | fits | 39,128 | 103 | 0.223 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 686,435 | 8.580 | 125 | 129 | fits | 39,128 | 103 | 0.223 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 365,166 | 4.565 | 125 | 129 | fits | 67,900 | 206 | 0.176 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 377,269 | 4.716 | 125 | 129 | fits | 67,900 | 206 | 0.176 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 538,055 | 6.726 | 125 | 129 | fits | 70,846 | 190 | 0.152 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 572,093 | 7.151 | 125 | 129 | fits | 26,823 | 54 | 0.462 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 120,169 | 1.502 | 20 | 200 | fits | 114,586 | 151 | 0.188 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 438,192 | 5.477 | 20 | 20 | fits | 91,694 | 98 | 0.628 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 330,294 | 4.129 | 20 | 24 | fits | 114,516 | 83 | 0.391 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 406,717 | 5.084 | 20 | 50 | fits | 91,694 | 98 | 0.628 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 919,805 | 11.498 | 20 | 20 | fits | 29,842 | 19 | 0.777 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 101,839 | 1.273 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 320,813 | 4.010 | 125 | 129 | fits | 67,936 | 206 | 0.176 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 338,515 | 4.231 | 125 | 129 | fits | 67,936 | 206 | 0.176 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 490,237 | 6.128 | 125 | 129 | fits | 72,221 | 196 | 0.148 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 507,938 | 6.349 | 125 | 129 | fits | 72,221 | 196 | 0.148 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 656,526 | 8.207 | 125 | 129 | fits | 39,128 | 103 | 0.223 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 673,838 | 8.423 | 125 | 129 | fits | 39,128 | 103 | 0.223 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 352,280 | 4.404 | 125 | 129 | fits | 67,936 | 206 | 0.176 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 364,383 | 4.555 | 125 | 129 | fits | 67,936 | 206 | 0.176 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 525,382 | 6.567 | 125 | 129 | fits | 72,221 | 196 | 0.148 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 559,482 | 6.994 | 125 | 129 | fits | 25,438 | 48 | 0.517 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 128,727 | 1.609 | 20 | 200 | fits | 118,255 | 246 | 0.240 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 460,937 | 5.762 | 20 | 20 | fits | 99,478 | 82 | 0.654 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 345,255 | 4.316 | 20 | 24 | fits | 117,944 | 96 | 0.392 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 429,462 | 5.368 | 20 | 50 | fits | 99,478 | 82 | 0.654 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 920,425 | 11.505 | 20 | 20 | fits | 82,525 | 47 | 0.698 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 82,161 | 1.027 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 490,032 | 6.125 | 125 | 129 | fits | 67,258 | 203 | 0.187 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 507,617 | 6.345 | 125 | 129 | fits | 67,258 | 203 | 0.187 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 643,574 | 8.045 | 125 | 129 | fits | 40,784 | 104 | 0.244 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 661,210 | 8.265 | 125 | 129 | fits | 40,784 | 104 | 0.244 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 163,918 | 2.049 | 125 | 129 | fits | 77,079 | 206 | 0.118 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 182,165 | 2.277 | 125 | 129 | fits | 77,079 | 206 | 0.118 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 521,151 | 6.514 | 125 | 129 | fits | 67,258 | 203 | 0.187 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 533,335 | 6.667 | 125 | 129 | fits | 67,258 | 203 | 0.187 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 199,671 | 2.496 | 125 | 129 | fits | 77,079 | 206 | 0.118 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 217,076 | 2.713 | 125 | 129 | fits | 77,079 | 206 | 0.118 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 121,962 | 1.525 | 20 | 200 | fits | 121,911 | 242 | 0.232 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 465,441 | 5.818 | 20 | 20 | fits | 91,965 | 99 | 0.629 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 357,272 | 4.466 | 20 | 24 | fits | 117,712 | 96 | 0.392 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 433,966 | 5.425 | 20 | 50 | fits | 91,965 | 99 | 0.629 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 922,875 | 11.536 | 20 | 20 | fits | 98,424 | 54 | 0.701 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 93,086 | 1.164 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 170,205 | 2.128 | 125 | 129 | fits | 68,784 | 206 | 0.198 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 188,216 | 2.353 | 125 | 129 | fits | 68,784 | 206 | 0.198 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 327,348 | 4.092 | 125 | 129 | fits | 72,415 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 344,984 | 4.312 | 125 | 129 | fits | 72,415 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 654,005 | 8.175 | 125 | 129 | fits | 39,848 | 104 | 0.238 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 671,455 | 8.393 | 125 | 129 | fits | 39,848 | 104 | 0.238 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 201,981 | 2.525 | 125 | 129 | fits | 68,784 | 206 | 0.198 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 214,084 | 2.676 | 125 | 129 | fits | 68,784 | 206 | 0.198 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 362,355 | 4.529 | 125 | 129 | fits | 72,415 | 200 | 0.139 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 399,621 | 4.995 | 125 | 129 | fits | 27,832 | 51 | 0.539 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 124,731 | 1.559 | 20 | 200 | fits | 118,088 | 235 | 0.256 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 469,816 | 5.873 | 20 | 20 | fits | 92,838 | 105 | 0.620 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 360,774 | 4.510 | 20 | 24 | fits | 118,812 | 104 | 0.388 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 438,341 | 5.479 | 20 | 50 | fits | 92,838 | 105 | 0.620 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 924,074 | 11.551 | 20 | 20 | fits | 94,720 | 51 | 0.696 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 94,339 | 1.179 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 645,159 | 8.064 | 125 | 129 | fits | 64,688 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 662,649 | 8.283 | 125 | 129 | fits | 64,688 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 153,226 | 1.915 | 125 | 129 | fits | 74,411 | 199 | 0.140 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 171,548 | 2.144 | 125 | 129 | fits | 74,411 | 199 | 0.140 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 482,383 | 6.030 | 125 | 129 | fits | 41,830 | 104 | 0.242 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 500,285 | 6.254 | 125 | 129 | fits | 41,830 | 104 | 0.242 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 675,802 | 8.448 | 125 | 129 | fits | 64,688 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 687,145 | 8.589 | 125 | 129 | fits | 64,688 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 189,127 | 2.364 | 125 | 129 | fits | 74,411 | 199 | 0.140 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 227,481 | 2.844 | 125 | 129 | fits | 28,816 | 51 | 0.561 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 122,965 | 1.537 | 20 | 200 | fits | 118,271 | 234 | 0.237 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 462,815 | 5.785 | 20 | 20 | fits | 91,939 | 101 | 0.626 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 354,672 | 4.433 | 20 | 24 | fits | 118,870 | 102 | 0.394 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 431,340 | 5.392 | 20 | 50 | fits | 91,939 | 101 | 0.626 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 916,182 | 11.452 | 20 | 20 | fits | 96,943 | 54 | 0.684 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 90,486 | 1.131 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 478,587 | 5.982 | 125 | 129 | fits | 67,228 | 204 | 0.184 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 496,181 | 6.202 | 125 | 129 | fits | 67,228 | 204 | 0.184 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 148,800 | 1.860 | 125 | 129 | fits | 74,147 | 198 | 0.135 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 167,092 | 2.089 | 125 | 129 | fits | 74,147 | 198 | 0.135 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 627,600 | 7.845 | 125 | 129 | fits | 39,304 | 103 | 0.233 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 644,946 | 8.062 | 125 | 129 | fits | 39,304 | 103 | 0.233 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 509,788 | 6.372 | 125 | 129 | fits | 67,228 | 204 | 0.184 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 521,899 | 6.524 | 125 | 129 | fits | 67,228 | 204 | 0.184 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 184,671 | 2.308 | 125 | 129 | fits | 74,147 | 198 | 0.135 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 222,824 | 2.785 | 125 | 129 | fits | 28,741 | 51 | 0.559 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 133,943 | 1.674 | 20 | 200 | fits | 119,316 | 256 | 0.253 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 471,575 | 5.895 | 20 | 20 | fits | 100,298 | 82 | 0.664 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 355,073 | 4.438 | 20 | 24 | fits | 118,108 | 96 | 0.402 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 440,100 | 5.501 | 20 | 50 | fits | 100,298 | 82 | 0.664 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 918,215 | 11.478 | 20 | 20 | fits | 83,200 | 49 | 0.705 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 77,236 | 0.965 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 172,141 | 2.152 | 125 | 129 | fits | 68,938 | 206 | 0.189 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 189,908 | 2.374 | 125 | 129 | fits | 68,938 | 206 | 0.189 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 328,688 | 4.109 | 125 | 129 | fits | 71,980 | 197 | 0.146 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 346,389 | 4.330 | 125 | 129 | fits | 71,980 | 197 | 0.146 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 652,680 | 8.159 | 125 | 129 | fits | 39,128 | 103 | 0.223 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 669,992 | 8.375 | 125 | 129 | fits | 39,128 | 103 | 0.223 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 203,673 | 2.546 | 125 | 129 | fits | 68,938 | 206 | 0.189 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 215,776 | 2.697 | 125 | 129 | fits | 68,938 | 206 | 0.189 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 363,833 | 4.548 | 125 | 129 | fits | 71,980 | 197 | 0.146 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 397,832 | 4.973 | 125 | 129 | fits | 25,341 | 48 | 0.506 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 120,594 | 1.507 | 20 | 200 | fits | 114,660 | 151 | 0.193 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 460,933 | 5.762 | 20 | 20 | fits | 91,883 | 101 | 0.624 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 352,846 | 4.411 | 20 | 24 | fits | 116,743 | 90 | 0.398 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 429,458 | 5.368 | 20 | 50 | fits | 91,883 | 101 | 0.624 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 932,001 | 11.650 | 20 | 20 | fits | 92,200 | 45 | 0.687 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 79,985 | 1.000 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 680,174 | 8.502 | 125 | 129 | fits | 25,010 | 52 | 0.476 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,339,347 | 16.742 | 125 | 129 | fits | 59,870 | 180 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 221,970 | 2.775 | 125 | 129 | fits | 77,134 | 207 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 240,286 | 3.004 | 125 | 129 | fits | 77,134 | 207 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 256,210 | 3.203 | 125 | 129 | fits | 77,134 | 207 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 273,658 | 3.421 | 125 | 129 | fits | 77,134 | 207 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,352,940 | 16.912 | 125 | 129 | fits | 59,870 | 180 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,364,358 | 17.054 | 125 | 129 | fits | 59,870 | 180 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,396,993 | 17.462 | 125 | 129 | fits | 27,384 | 52 | 0.500 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 408,003 | 5.100 | 125 | 129 | fits | 24,701 | 53 | 0.277 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 139,694 | 1.746 | 20 | 200 | fits | 119,833 | 249 | 0.270 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 498,671 | 6.233 | 20 | 20 | fits | 96,950 | 41 | 0.761 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 385,517 | 4.819 | 20 | 24 | fits | 126,736 | 129 | 0.449 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 370,246 | 4.628 | 20 | 50 | fits | 126,736 | 129 | 0.449 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 859,190 | 10.740 | 20 | 20 | fits | 52,578 | 26 | 0.711 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 712,550 | 8.907 | 125 | 129 | fits | 25,280 | 52 | 0.485 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,257,962 | 15.725 | 125 | 129 | fits | 60,264 | 182 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 143,552 | 1.794 | 125 | 129 | fits | 114,926 | 112 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 161,875 | 2.023 | 125 | 129 | fits | 114,926 | 112 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 271,634 | 3.395 | 125 | 129 | fits | 42,460 | 104 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 289,561 | 3.620 | 125 | 129 | fits | 42,460 | 104 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,271,555 | 15.894 | 125 | 129 | fits | 60,264 | 182 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,282,900 | 16.036 | 125 | 129 | fits | 60,264 | 182 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,315,317 | 16.441 | 125 | 129 | fits | 26,695 | 48 | 0.519 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 434,480 | 5.431 | 125 | 129 | fits | 25,468 | 53 | 0.355 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 129,012 | 1.613 | 20 | 200 | fits | 118,711 | 249 | 0.304 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 513,382 | 6.417 | 20 | 20 | fits | 97,372 | 62 | 0.728 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 374,526 | 4.682 | 20 | 24 | fits | 136,518 | 124 | 0.428 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 359,255 | 4.491 | 20 | 50 | fits | 136,518 | 124 | 0.428 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 886,529 | 11.082 | 20 | 20 | fits | 64,344 | 30 | 0.693 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 1,174,666 | 14.683 | 125 | 129 | fits | 73,730 | 206 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,192,539 | 14.907 | 125 | 129 | fits | 73,730 | 206 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 218,565 | 2.732 | 125 | 129 | fits | 44,427 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 236,888 | 2.961 | 125 | 129 | fits | 44,427 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 386,270 | 4.828 | 125 | 129 | fits | 23,867 | 52 | 0.437 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 1,210,092 | 15.126 | 125 | 129 | fits | 73,730 | 206 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,222,884 | 15.286 | 125 | 129 | fits | 73,730 | 206 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,273,013 | 15.913 | 125 | 129 | fits | 51,343 | 158 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,289,997 | 16.125 | 125 | 129 | fits | 51,343 | 158 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 1,306,420 | 16.330 | 125 | 129 | fits | 51,343 | 158 | 0.127 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 413,769 | 5.172 | 20 | 200 | fits | 120,555 | 266 | 0.234 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 496,945 | 6.212 | 20 | 20 | fits | 99,444 | 62 | 0.659 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 260,742 | 3.259 | 20 | 24 | fits | 118,514 | 98 | 0.409 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 366,026 | 4.575 | 20 | 50 | fits | 120,555 | 266 | 0.234 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 871,280 | 10.891 | 20 | 20 | fits | 64,841 | 30 | 0.693 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,100,563 | 13.757 | 125 | 129 | fits | 76,801 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,118,409 | 13.980 | 125 | 129 | fits | 76,801 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 310,292 | 3.879 | 125 | 129 | fits | 25,069 | 51 | 0.455 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,135,954 | 14.199 | 125 | 129 | fits | 76,801 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,151,368 | 14.392 | 125 | 129 | fits | 76,801 | 204 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,263,070 | 15.788 | 125 | 129 | fits | 57,620 | 181 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,276,381 | 15.955 | 125 | 129 | fits | 57,620 | 181 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,287,799 | 16.097 | 125 | 129 | fits | 57,620 | 181 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,319,264 | 16.491 | 125 | 129 | fits | 25,785 | 52 | 0.423 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 1,424,205 | 17.803 | 125 | 129 | fits | 22,289 | 53 | 0.257 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 438,619 | 5.483 | 20 | 200 | fits | 120,321 | 263 | 0.233 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 520,525 | 6.507 | 20 | 20 | fits | 98,174 | 58 | 0.658 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 285,826 | 3.573 | 20 | 24 | fits | 120,389 | 105 | 0.411 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 390,876 | 4.886 | 20 | 50 | fits | 120,321 | 263 | 0.233 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 896,101 | 11.201 | 20 | 20 | fits | 64,902 | 30 | 0.693 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 948,644 | 11.858 | 125 | 129 | fits | 76,911 | 207 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 966,563 | 12.082 | 125 | 129 | fits | 76,911 | 207 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 270,448 | 3.381 | 125 | 129 | fits | 25,788 | 51 | 0.474 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 984,181 | 12.302 | 125 | 129 | fits | 76,911 | 207 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 999,662 | 12.496 | 125 | 129 | fits | 76,911 | 207 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,055,561 | 13.195 | 125 | 129 | fits | 57,573 | 180 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,068,872 | 13.361 | 125 | 129 | fits | 57,573 | 180 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,080,290 | 13.504 | 125 | 129 | fits | 57,573 | 180 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,111,604 | 13.895 | 125 | 129 | fits | 25,776 | 52 | 0.433 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,216,511 | 15.206 | 125 | 129 | fits | 22,186 | 53 | 0.254 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 134,644 | 1.683 | 20 | 200 | fits | 119,608 | 250 | 0.271 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 476,774 | 5.960 | 20 | 20 | fits | 94,730 | 74 | 0.669 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 365,840 | 4.573 | 20 | 24 | fits | 119,764 | 99 | 0.417 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 445,299 | 5.566 | 20 | 50 | fits | 94,730 | 74 | 0.669 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 864,694 | 10.809 | 20 | 20 | fits | 76,853 | 34 | 0.682 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 417,276 | 5.216 | 125 | 129 | fits | 80,943 | 211 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 435,075 | 5.438 | 125 | 129 | fits | 80,943 | 211 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 631,747 | 7.897 | 125 | 129 | fits | 24,511 | 52 | 0.457 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,418,053 | 17.726 | 125 | 129 | fits | 54,576 | 137 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,435,074 | 17.938 | 125 | 129 | fits | 54,576 | 137 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,468,855 | 18.361 | 125 | 129 | fits | 26,628 | 45 | 0.555 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 448,768 | 5.610 | 125 | 129 | fits | 80,943 | 211 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 460,798 | 5.760 | 125 | 129 | fits | 80,943 | 211 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 484,116 | 6.051 | 125 | 129 | fits | 21,563 | 54 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 1,531,097 | 19.139 | 125 | 129 | fits | 22,302 | 53 | 0.260 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 482,717 | 6.034 | 20 | 200 | fits | 121,326 | 270 | 0.236 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 564,381 | 7.055 | 20 | 20 | fits | 97,932 | 56 | 0.663 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 328,919 | 4.111 | 20 | 24 | fits | 118,841 | 103 | 0.415 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 434,974 | 5.437 | 20 | 50 | fits | 121,326 | 270 | 0.236 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 937,506 | 11.719 | 20 | 20 | fits | 64,589 | 30 | 0.693 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 555,420 | 6.943 | 125 | 129 | fits | 24,692 | 51 | 0.453 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,342,078 | 16.776 | 125 | 129 | fits | 59,564 | 151 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,360,324 | 17.004 | 125 | 129 | fits | 59,564 | 151 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,395,192 | 17.440 | 125 | 129 | fits | 24,457 | 33 | 0.688 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,470,304 | 18.379 | 125 | 129 | fits | 63,889 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,487,802 | 18.598 | 125 | 129 | fits | 63,889 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 1,500,686 | 18.759 | 125 | 129 | fits | 63,889 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 1,512,028 | 18.900 | 125 | 129 | fits | 63,889 | 203 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 1,629,857 | 20.373 | 125 | 129 | fits | 35,522 | 94 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 1,660,788 | 20.760 | 125 | 129 | fits | 21,892 | 39 | 0.489 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 469,886 | 5.874 | 20 | 200 | fits | 121,862 | 276 | 0.229 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 552,622 | 6.908 | 20 | 20 | fits | 99,004 | 62 | 0.654 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 315,552 | 3.944 | 20 | 24 | fits | 116,262 | 97 | 0.416 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 422,143 | 5.277 | 20 | 50 | fits | 121,862 | 276 | 0.229 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 926,670 | 11.583 | 20 | 20 | fits | 64,760 | 30 | 0.693 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 754,513 | 9.431 | 125 | 129 | fits | 24,467 | 51 | 0.457 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,436,857 | 17.961 | 125 | 129 | fits | 59,846 | 180 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 281,357 | 3.517 | 125 | 129 | fits | 71,986 | 189 | 0.195 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 299,681 | 3.746 | 125 | 129 | fits | 71,986 | 189 | 0.195 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 315,638 | 3.945 | 125 | 129 | fits | 71,986 | 189 | 0.195 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 351,288 | 4.391 | 125 | 129 | fits | 27,898 | 39 | 0.547 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,450,450 | 18.131 | 125 | 129 | fits | 59,846 | 180 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,461,868 | 18.273 | 125 | 129 | fits | 59,846 | 180 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,494,520 | 18.681 | 125 | 129 | fits | 27,401 | 52 | 0.500 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 613,437 | 7.668 | 125 | 129 | fits | 25,911 | 53 | 0.373 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 115,844 | 1.448 | 20 | 200 | fits | 118,643 | 229 | 0.283 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 500,951 | 6.262 | 20 | 20 | fits | 91,480 | 47 | 0.715 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 393,267 | 4.916 | 20 | 24 | fits | 143,391 | 159 | 0.428 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 377,996 | 4.725 | 20 | 50 | fits | 143,391 | 159 | 0.428 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 873,643 | 10.921 | 20 | 20 | fits | 64,485 | 30 | 0.693 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
