### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 11.333 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.adp.if0` (notice-burst-5) | 10.350 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.aecp.if0` (notice-burst-4) | 11.651 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-6.held.maap.if0` (notice-burst-6) | 10.009 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-6.held.srp.if0` (notice-burst-6) | 6.865 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-6.mrpdu.periodic.if0` (notice-every-6) | 1.080 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-3.notices.29.9.0.if0` (notice-burst-3) | 12.586 (12.759) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1799 | 0 | 154,944 (1.549) | fits |
| notice-every-1 | 1793 | 0 | 154,181 (1.542) | fits |
| notice-every-2 | 1799 | 0 | 155,488 (1.555) | fits |
| notice-every-3 | 1785 | 0 | 154,185 (1.542) | fits |
| notice-every-4 | 1790 | 0 | 157,227 (1.572) | fits |
| notice-every-5 | 1783 | 0 | 154,891 (1.549) | fits |
| notice-every-6 | 1792 | 0 | 153,462 (1.535) | fits |
| notice-every-7 | 1788 | 0 | 154,853 (1.549) | fits |
| notice-burst-0 | 987 | 0 | 158,037 (1.580) | fits |
| notice-burst-1 | 965 | 0 | 154,789 (1.548) | fits |
| notice-burst-2 | 950 | 0 | 157,108 (1.571) | fits |
| notice-burst-3 | 979 | 0 | 160,134 (1.601) | fits |
| notice-burst-4 | 972 | 0 | 154,501 (1.545) | fits |
| notice-burst-5 | 980 | 0 | 146,876 (1.469) | fits |
| notice-burst-6 | 977 | 0 | 160,222 (1.602) | fits |
| notice-burst-7 | 975 | 0 | 155,659 (1.557) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.318 | 22 | 16 | 2 | within |
| notice-every-0 | 4.531 | 22 | 16 | 2 | within |
| notice-every-0 | 6.324 | 22 | 16 | 2 | within |
| notice-every-0 | 6.536 | 22 | 16 | 2 | within |
| notice-every-0 | 2.232 | 22 | 16 | 2 | within |
| notice-every-0 | 2.449 | 22 | 16 | 2 | within |
| notice-every-0 | 8.269 | 22 | 16 | 2 | within |
| notice-every-0 | 8.478 | 22 | 16 | 2 | within |
| notice-every-0 | 4.725 | 22 | 16 | 2 | within |
| notice-every-0 | 4.904 | 22 | 16 | 2 | within |
| notice-every-0 | 2.666 | 22 | 16 | 2 | within |
| notice-every-0 | 2.884 | 22 | 16 | 2 | within |
| notice-every-1 | 4.322 | 22 | 16 | 2 | within |
| notice-every-1 | 4.535 | 22 | 16 | 2 | within |
| notice-every-1 | 6.179 | 22 | 16 | 2 | within |
| notice-every-1 | 6.392 | 22 | 16 | 2 | within |
| notice-every-1 | 8.250 | 22 | 16 | 2 | within |
| notice-every-1 | 8.459 | 22 | 16 | 2 | within |
| notice-every-1 | 2.110 | 22 | 16 | 2 | within |
| notice-every-1 | 2.330 | 22 | 16 | 2 | within |
| notice-every-1 | 4.729 | 22 | 16 | 2 | within |
| notice-every-1 | 4.907 | 22 | 16 | 2 | within |
| notice-every-1 | 2.547 | 22 | 16 | 2 | within |
| notice-every-1 | 2.765 | 22 | 16 | 2 | within |
| notice-every-2 | 4.002 | 22 | 16 | 2 | within |
| notice-every-2 | 4.212 | 22 | 16 | 2 | within |
| notice-every-2 | 6.002 | 22 | 16 | 2 | within |
| notice-every-2 | 6.214 | 22 | 16 | 2 | within |
| notice-every-2 | 7.946 | 22 | 16 | 2 | within |
| notice-every-2 | 8.155 | 22 | 16 | 2 | within |
| notice-every-2 | 1.900 | 22 | 16 | 2 | within |
| notice-every-2 | 2.120 | 22 | 16 | 2 | within |
| notice-every-2 | 4.406 | 22 | 16 | 2 | within |
| notice-every-2 | 4.584 | 22 | 16 | 2 | within |
| notice-every-2 | 2.336 | 22 | 16 | 2 | within |
| notice-every-2 | 2.554 | 22 | 16 | 2 | within |
| notice-every-3 | 8.303 | 22 | 16 | 2 | within |
| notice-every-3 | 8.512 | 22 | 16 | 2 | within |
| notice-every-3 | 2.181 | 22 | 16 | 2 | within |
| notice-every-3 | 2.399 | 22 | 16 | 2 | within |
| notice-every-3 | 4.227 | 22 | 16 | 2 | within |
| notice-every-3 | 4.442 | 22 | 16 | 2 | within |
| notice-every-3 | 6.332 | 22 | 16 | 2 | within |
| notice-every-3 | 6.544 | 22 | 16 | 2 | within |
| notice-every-3 | 8.701 | 22 | 16 | 2 | within |
| notice-every-3 | 8.875 | 22 | 16 | 2 | within |
| notice-every-3 | 2.617 | 22 | 16 | 2 | within |
| notice-every-3 | 2.835 | 22 | 16 | 2 | within |
| notice-every-4 | 2.114 | 22 | 16 | 2 | within |
| notice-every-4 | 2.325 | 22 | 16 | 2 | within |
| notice-every-4 | 4.578 | 22 | 16 | 2 | within |
| notice-every-4 | 4.794 | 22 | 16 | 2 | within |
| notice-every-4 | 6.162 | 22 | 16 | 2 | within |
| notice-every-4 | 6.371 | 22 | 16 | 2 | within |
| notice-every-4 | 8.226 | 22 | 16 | 2 | within |
| notice-every-4 | 8.435 | 22 | 16 | 2 | within |
| notice-every-4 | 2.520 | 22 | 16 | 2 | within |
| notice-every-4 | 2.701 | 22 | 16 | 2 | within |
| notice-every-4 | 2.913 | 22 | 16 | 2 | within |
| notice-every-4 | 3.128 | 22 | 16 | 2 | within |
| notice-every-5 | 2.114 | 22 | 16 | 2 | within |
| notice-every-5 | 2.326 | 22 | 16 | 2 | within |
| notice-every-5 | 4.573 | 22 | 16 | 2 | within |
| notice-every-5 | 4.789 | 22 | 16 | 2 | within |
| notice-every-5 | 6.155 | 22 | 16 | 2 | within |
| notice-every-5 | 6.364 | 22 | 16 | 2 | within |
| notice-every-5 | 8.220 | 22 | 16 | 2 | within |
| notice-every-5 | 8.429 | 22 | 16 | 2 | within |
| notice-every-5 | 2.521 | 22 | 16 | 2 | within |
| notice-every-5 | 2.702 | 22 | 16 | 2 | within |
| notice-every-5 | 2.913 | 22 | 16 | 2 | within |
| notice-every-5 | 3.129 | 22 | 16 | 2 | within |
| notice-every-6 | 2.116 | 22 | 16 | 2 | within |
| notice-every-6 | 2.328 | 22 | 16 | 2 | within |
| notice-every-6 | 4.576 | 22 | 16 | 2 | within |
| notice-every-6 | 4.792 | 22 | 16 | 2 | within |
| notice-every-6 | 6.159 | 22 | 16 | 2 | within |
| notice-every-6 | 6.368 | 22 | 16 | 2 | within |
| notice-every-6 | 8.223 | 22 | 16 | 2 | within |
| notice-every-6 | 8.432 | 22 | 16 | 2 | within |
| notice-every-6 | 2.523 | 22 | 16 | 2 | within |
| notice-every-6 | 2.704 | 22 | 16 | 2 | within |
| notice-every-6 | 2.915 | 22 | 16 | 2 | within |
| notice-every-6 | 3.131 | 22 | 16 | 2 | within |
| notice-every-7 | 2.113 | 22 | 16 | 2 | within |
| notice-every-7 | 2.325 | 22 | 16 | 2 | within |
| notice-every-7 | 4.574 | 22 | 16 | 2 | within |
| notice-every-7 | 4.790 | 22 | 16 | 2 | within |
| notice-every-7 | 6.157 | 22 | 16 | 2 | within |
| notice-every-7 | 6.366 | 22 | 16 | 2 | within |
| notice-every-7 | 8.220 | 22 | 16 | 2 | within |
| notice-every-7 | 8.430 | 22 | 16 | 2 | within |
| notice-every-7 | 2.520 | 22 | 16 | 2 | within |
| notice-every-7 | 2.701 | 22 | 16 | 2 | within |
| notice-every-7 | 2.912 | 22 | 16 | 2 | within |
| notice-every-7 | 3.128 | 22 | 16 | 2 | within |
| notice-burst-0 | 8.983 | 22 | 16 | 0 | within |
| notice-burst-0 | 9.195 | 22 | 16 | 0 | within |
| notice-burst-0 | 9.402 | 22 | 16 | 0 | within |
| notice-burst-0 | 9.609 | 22 | 16 | 0 | within |
| notice-burst-0 | 11.360 | 22 | 16 | 0 | within |
| notice-burst-0 | 11.573 | 22 | 16 | 0 | within |
| notice-burst-0 | 3.164 | 22 | 16 | 0 | within |
| notice-burst-0 | 3.385 | 22 | 16 | 0 | within |
| notice-burst-0 | 9.801 | 22 | 16 | 0 | within |
| notice-burst-0 | 9.977 | 22 | 16 | 0 | within |
| notice-burst-0 | 10.184 | 22 | 16 | 0 | within |
| notice-burst-0 | 4.097 | 22 | 16 | 0 | within |
| notice-burst-1 | 8.335 | 22 | 16 | 0 | within |
| notice-burst-1 | 8.548 | 22 | 16 | 0 | within |
| notice-burst-1 | 10.307 | 22 | 16 | 0 | within |
| notice-burst-1 | 10.523 | 22 | 16 | 0 | within |
| notice-burst-1 | 2.166 | 22 | 16 | 0 | within |
| notice-burst-1 | 2.381 | 22 | 16 | 0 | within |
| notice-burst-1 | 2.582 | 22 | 16 | 0 | within |
| notice-burst-1 | 2.790 | 22 | 16 | 0 | within |
| notice-burst-1 | 8.739 | 22 | 16 | 0 | within |
| notice-burst-1 | 8.915 | 22 | 16 | 0 | within |
| notice-burst-1 | 9.122 | 22 | 16 | 0 | within |
| notice-burst-1 | 4.063 | 22 | 16 | 0 | within |
| notice-burst-2 | 8.494 | 22 | 16 | 0 | within |
| notice-burst-2 | 8.707 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.053 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.268 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.469 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.675 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.873 | 22 | 16 | 0 | within |
| notice-burst-2 | 3.079 | 22 | 16 | 0 | within |
| notice-burst-2 | 8.898 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.072 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.277 | 22 | 16 | 0 | within |
| notice-burst-2 | 4.946 | 22 | 16 | 0 | within |
| notice-burst-3 | 9.315 | 22 | 16 | 1 | within |
| notice-burst-3 | 9.529 | 22 | 16 | 1 | within |
| notice-burst-3 | 9.737 | 22 | 16 | 1 | within |
| notice-burst-3 | 9.944 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.141 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.345 | 22 | 16 | 1 | within |
| notice-burst-3 | 2.172 | 22 | 16 | 1 | within |
| notice-burst-3 | 2.389 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.532 | 22 | 16 | 1 | within |
| notice-burst-3 | 12.375 | 22 | 16 | 1 | within |
| notice-burst-3 | 12.586 | 22 | 16 | 1 | within |
| notice-burst-3 | 4.237 | 22 | 16 | 1 | within |
| notice-burst-4 | 8.558 | 22 | 16 | 1 | within |
| notice-burst-4 | 8.772 | 22 | 16 | 1 | within |
| notice-burst-4 | 8.980 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.187 | 22 | 16 | 1 | within |
| notice-burst-4 | 11.496 | 22 | 16 | 1 | within |
| notice-burst-4 | 11.709 | 22 | 16 | 1 | within |
| notice-burst-4 | 2.878 | 22 | 16 | 1 | within |
| notice-burst-4 | 3.097 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.378 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.554 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.760 | 22 | 16 | 1 | within |
| notice-burst-4 | 4.766 | 22 | 16 | 1 | within |
| notice-burst-5 | 6.043 | 22 | 16 | 0 | within |
| notice-burst-5 | 6.256 | 22 | 16 | 0 | within |
| notice-burst-5 | 6.462 | 22 | 16 | 0 | within |
| notice-burst-5 | 6.669 | 22 | 16 | 0 | within |
| notice-burst-5 | 7.293 | 22 | 16 | 0 | within |
| notice-burst-5 | 7.500 | 22 | 16 | 0 | within |
| notice-burst-5 | 9.374 | 22 | 16 | 0 | within |
| notice-burst-5 | 9.585 | 22 | 16 | 0 | within |
| notice-burst-5 | 6.863 | 22 | 16 | 0 | within |
| notice-burst-5 | 7.043 | 22 | 16 | 0 | within |
| notice-burst-5 | 7.712 | 22 | 16 | 0 | within |
| notice-burst-5 | 9.795 | 22 | 16 | 0 | within |
| notice-burst-6 | 7.833 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.043 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.249 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.455 | 22 | 16 | 1 | within |
| notice-burst-6 | 10.690 | 22 | 16 | 1 | within |
| notice-burst-6 | 10.903 | 22 | 16 | 1 | within |
| notice-burst-6 | 11.100 | 22 | 16 | 1 | within |
| notice-burst-6 | 11.304 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.649 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.829 | 22 | 16 | 1 | within |
| notice-burst-6 | 9.037 | 22 | 16 | 1 | within |
| notice-burst-6 | 11.511 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.003 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.215 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.422 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.629 | 22 | 16 | 1 | within |
| notice-burst-7 | 11.702 | 22 | 16 | 1 | within |
| notice-burst-7 | 11.914 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.167 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.384 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.822 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.998 | 22 | 16 | 1 | within |
| notice-burst-7 | 10.204 | 22 | 16 | 1 | within |
| notice-burst-7 | 3.929 | 22 | 16 | 1 | within |

Latest: 12.586 ms, notice-burst-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 306 | 97,366 (0.974) | 76,561 (0.766) |
| notice-every-1 | 306 | 102,209 (1.022) | 76,561 (0.766) |
| notice-every-2 | 306 | 106,679 (1.067) | 76,493 (0.765) |
| notice-every-3 | 306 | 87,085 (0.871) | 76,126 (0.761) |
| notice-every-4 | 306 | 93,195 (0.932) | 76,441 (0.764) |
| notice-every-5 | 306 | 93,087 (0.931) | 76,441 (0.764) |
| notice-every-6 | 306 | 88,716 (0.887) | 76,441 (0.764) |
| notice-every-7 | 306 | 88,716 (0.887) | 76,441 (0.764) |
| notice-burst-0 | 316 | 99,444 (0.994) | 78,418 (0.784) |
| notice-burst-1 | 316 | 102,209 (1.022) | 78,476 (0.785) |
| notice-burst-2 | 316 | 106,679 (1.067) | 78,476 (0.785) |
| notice-burst-3 | 316 | 96,291 (0.963) | 78,476 (0.785) |
| notice-burst-4 | 316 | 97,155 (0.972) | 78,418 (0.784) |
| notice-burst-5 | 316 | 94,299 (0.943) | 78,476 (0.785) |
| notice-burst-6 | 316 | 92,152 (0.922) | 78,476 (0.785) |
| notice-burst-7 | 316 | 99,270 (0.993) | 78,476 (0.785) |

Longest pass that carries a step: 106,679 CPU cycles (1.067 ms), notice-every-2; longest step: 78,476 (0.785 ms), notice-burst-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 431,824 | 4.318 | 22 | 26 | fits | 85,853 | 201 | 0.215 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 453,111 | 4.531 | 22 | 26 | fits | 85,853 | 201 | 0.215 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 632,367 | 6.324 | 22 | 26 | fits | 48,360 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 653,647 | 6.536 | 22 | 26 | fits | 48,360 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 223,203 | 2.232 | 22 | 26 | fits | 93,011 | 204 | 0.210 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 244,887 | 2.449 | 22 | 26 | fits | 93,011 | 204 | 0.210 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 826,922 | 8.269 | 22 | 26 | fits | 45,978 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 847,812 | 8.478 | 22 | 26 | fits | 45,978 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 472,528 | 4.725 | 22 | 26 | fits | 85,853 | 201 | 0.215 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 490,369 | 4.904 | 22 | 26 | fits | 85,853 | 201 | 0.215 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 266,648 | 2.666 | 22 | 26 | fits | 93,011 | 204 | 0.210 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 288,441 | 2.884 | 22 | 26 | fits | 93,011 | 204 | 0.210 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 831,130 | 8.311 | 20 | 200 | fits | 146,543 | 115 | 0.535 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 810,862 | 8.109 | 20 | 20 | fits | 146,543 | 115 | 0.535 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 912,869 | 9.129 | 20 | 24 | fits | 108,978 | 100 | 0.419 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 771,387 | 7.714 | 20 | 50 | fits | 146,543 | 115 | 0.535 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 429,438 | 4.294 | 20 | 20 | fits | 81,128 | 44 | 0.473 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 103,513 | 1.035 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 432,187 | 4.322 | 22 | 26 | fits | 85,693 | 201 | 0.210 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 453,474 | 4.535 | 22 | 26 | fits | 85,693 | 201 | 0.210 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 617,893 | 6.179 | 22 | 26 | fits | 48,281 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 639,173 | 6.392 | 22 | 26 | fits | 48,281 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 824,983 | 8.250 | 22 | 26 | fits | 46,004 | 102 | 0.261 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 845,873 | 8.459 | 22 | 26 | fits | 46,004 | 102 | 0.261 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 211,044 | 2.110 | 22 | 26 | fits | 93,481 | 206 | 0.211 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 232,959 | 2.330 | 22 | 26 | fits | 93,481 | 206 | 0.211 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 472,891 | 4.729 | 22 | 26 | fits | 85,693 | 201 | 0.210 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 490,732 | 4.907 | 22 | 26 | fits | 85,693 | 201 | 0.210 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 254,666 | 2.547 | 22 | 26 | fits | 93,481 | 206 | 0.211 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 276,459 | 2.765 | 22 | 26 | fits | 93,481 | 206 | 0.211 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 660,100 | 6.601 | 20 | 200 | fits | 148,811 | 142 | 0.545 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 810,837 | 8.108 | 20 | 20 | fits | 152,249 | 141 | 0.516 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 929,518 | 9.295 | 20 | 24 | fits | 125,011 | 112 | 0.406 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 771,362 | 7.714 | 20 | 50 | fits | 152,249 | 141 | 0.516 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 429,521 | 4.295 | 20 | 20 | fits | 83,605 | 49 | 0.514 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 86,112 | 0.861 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 400,223 | 4.002 | 22 | 26 | fits | 84,668 | 201 | 0.194 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 421,192 | 4.212 | 22 | 26 | fits | 84,668 | 201 | 0.194 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 600,168 | 6.002 | 22 | 26 | fits | 48,012 | 103 | 0.267 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 621,448 | 6.214 | 22 | 26 | fits | 48,012 | 103 | 0.267 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 794,588 | 7.946 | 22 | 26 | fits | 45,818 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 815,478 | 8.155 | 22 | 26 | fits | 45,818 | 102 | 0.256 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 189,997 | 1.900 | 22 | 26 | fits | 93,290 | 204 | 0.200 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 211,976 | 2.120 | 22 | 26 | fits | 93,290 | 204 | 0.200 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 440,552 | 4.406 | 22 | 26 | fits | 84,668 | 201 | 0.194 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 458,393 | 4.584 | 22 | 26 | fits | 84,668 | 201 | 0.194 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 233,625 | 2.336 | 22 | 26 | fits | 93,290 | 204 | 0.200 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 255,418 | 2.554 | 22 | 26 | fits | 93,290 | 204 | 0.200 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 670,630 | 6.706 | 20 | 200 | fits | 155,488 | 163 | 0.530 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 810,164 | 8.102 | 20 | 20 | fits | 145,667 | 113 | 0.547 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 931,842 | 9.318 | 20 | 24 | fits | 124,516 | 112 | 0.408 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 770,689 | 7.707 | 20 | 50 | fits | 145,667 | 113 | 0.547 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 433,374 | 4.334 | 20 | 20 | fits | 83,767 | 49 | 0.517 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 99,117 | 0.991 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 830,260 | 8.303 | 22 | 26 | fits | 83,094 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 851,229 | 8.512 | 22 | 26 | fits | 83,094 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 218,146 | 2.181 | 22 | 26 | fits | 94,588 | 206 | 0.220 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 239,851 | 2.399 | 22 | 26 | fits | 94,588 | 206 | 0.220 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 422,705 | 4.227 | 22 | 26 | fits | 48,482 | 102 | 0.286 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 444,223 | 4.442 | 22 | 26 | fits | 48,482 | 102 | 0.286 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 633,161 | 6.332 | 22 | 26 | fits | 47,297 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 654,353 | 6.544 | 22 | 26 | fits | 47,297 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 870,129 | 8.701 | 22 | 26 | fits | 83,094 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 887,508 | 8.875 | 22 | 26 | fits | 83,094 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 261,691 | 2.617 | 22 | 26 | fits | 94,588 | 206 | 0.220 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 283,484 | 2.835 | 22 | 26 | fits | 94,588 | 206 | 0.220 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 152,426 | 1.524 | 20 | 200 | fits | 154,140 | 155 | 0.489 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 810,613 | 8.106 | 20 | 20 | fits | 149,267 | 124 | 0.515 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 926,343 | 9.263 | 20 | 24 | fits | 123,105 | 106 | 0.406 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 771,138 | 7.711 | 20 | 50 | fits | 149,267 | 124 | 0.515 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 438,072 | 4.381 | 20 | 20 | fits | 81,402 | 43 | 0.477 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 101,438 | 1.014 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 211,379 | 2.114 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 232,534 | 2.325 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 457,823 | 4.578 | 22 | 26 | fits | 49,591 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 479,421 | 4.794 | 22 | 26 | fits | 49,591 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 616,244 | 6.162 | 22 | 26 | fits | 46,316 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 637,134 | 6.371 | 22 | 26 | fits | 46,316 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 822,580 | 8.226 | 22 | 26 | fits | 45,863 | 103 | 0.251 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 843,541 | 8.435 | 22 | 26 | fits | 45,863 | 103 | 0.251 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 252,046 | 2.520 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 270,120 | 2.701 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 291,257 | 2.913 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 312,849 | 3.128 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 694,691 | 6.947 | 20 | 200 | fits | 148,740 | 151 | 0.514 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 948,295 | 9.483 | 20 | 20 | fits | 110,919 | 89 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 928,091 | 9.281 | 20 | 24 | fits | 110,919 | 89 | 0.509 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 785,142 | 7.851 | 20 | 50 | fits | 150,194 | 126 | 0.516 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 450,550 | 4.505 | 20 | 20 | fits | 82,469 | 49 | 0.465 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 104,099 | 1.041 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 211,412 | 2.114 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 232,567 | 2.326 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 457,320 | 4.573 | 22 | 26 | fits | 49,591 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 478,918 | 4.789 | 22 | 26 | fits | 49,591 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 615,540 | 6.155 | 22 | 26 | fits | 46,316 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 636,430 | 6.364 | 22 | 26 | fits | 46,316 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 821,981 | 8.220 | 22 | 26 | fits | 45,864 | 103 | 0.253 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 842,942 | 8.429 | 22 | 26 | fits | 45,864 | 103 | 0.253 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 252,079 | 2.521 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 270,153 | 2.702 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 291,290 | 2.913 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 312,882 | 3.129 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 700,515 | 7.005 | 20 | 200 | fits | 154,891 | 161 | 0.527 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 839,599 | 8.396 | 20 | 20 | fits | 145,641 | 111 | 0.545 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 926,118 | 9.261 | 20 | 24 | fits | 106,723 | 85 | 0.419 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 800,124 | 8.001 | 20 | 50 | fits | 145,641 | 111 | 0.545 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 450,035 | 4.500 | 20 | 20 | fits | 82,704 | 51 | 0.466 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 86,236 | 0.862 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 211,641 | 2.116 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 232,796 | 2.328 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 457,559 | 4.576 | 22 | 26 | fits | 49,591 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 479,157 | 4.792 | 22 | 26 | fits | 49,591 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 615,868 | 6.159 | 22 | 26 | fits | 46,382 | 102 | 0.265 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 636,824 | 6.368 | 22 | 26 | fits | 46,382 | 102 | 0.265 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 822,252 | 8.223 | 22 | 26 | fits | 45,863 | 103 | 0.251 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 843,213 | 8.432 | 22 | 26 | fits | 45,863 | 103 | 0.251 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 252,308 | 2.523 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 270,382 | 2.704 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 291,519 | 2.915 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 313,111 | 3.131 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 854,728 | 8.547 | 20 | 200 | fits | 153,414 | 143 | 0.510 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 834,460 | 8.345 | 20 | 20 | fits | 153,414 | 143 | 0.510 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 936,949 | 9.369 | 20 | 24 | fits | 108,799 | 92 | 0.429 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 794,985 | 7.950 | 20 | 50 | fits | 153,414 | 143 | 0.510 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 453,840 | 4.538 | 20 | 20 | fits | 84,981 | 55 | 0.518 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 107,988 | 1.080 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 211,312 | 2.113 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 232,467 | 2.325 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 457,436 | 4.574 | 22 | 26 | fits | 49,591 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 479,034 | 4.790 | 22 | 26 | fits | 49,591 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 615,656 | 6.157 | 22 | 26 | fits | 46,382 | 102 | 0.265 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 636,612 | 6.366 | 22 | 26 | fits | 46,382 | 102 | 0.265 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 822,040 | 8.220 | 22 | 26 | fits | 45,863 | 103 | 0.251 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 843,001 | 8.430 | 22 | 26 | fits | 45,863 | 103 | 0.251 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 251,979 | 2.520 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 270,053 | 2.701 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 291,190 | 2.912 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 312,782 | 3.128 | 22 | 26 | fits | 130,036 | 305 | 0.181 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 868,779 | 8.688 | 20 | 200 | fits | 148,149 | 120 | 0.540 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 848,511 | 8.485 | 20 | 20 | fits | 148,149 | 120 | 0.540 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 935,141 | 9.351 | 20 | 24 | fits | 106,834 | 85 | 0.423 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 809,036 | 8.090 | 20 | 50 | fits | 148,149 | 120 | 0.540 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 451,765 | 4.518 | 20 | 20 | fits | 82,603 | 51 | 0.467 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 88,604 | 0.886 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 898,270 | 8.983 | 22 | 26 | fits | 149,351 | 353 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 919,535 | 9.195 | 22 | 26 | fits | 149,351 | 353 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 940,250 | 9.402 | 22 | 26 | fits | 149,351 | 353 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 960,935 | 9.609 | 22 | 26 | fits | 149,351 | 353 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 1,135,997 | 11.360 | 22 | 26 | fits | 48,190 | 102 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 1,157,253 | 11.573 | 22 | 26 | fits | 48,190 | 102 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 316,426 | 3.164 | 22 | 26 | fits | 51,059 | 102 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 338,456 | 3.385 | 22 | 26 | fits | 51,059 | 102 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 980,085 | 9.801 | 22 | 26 | fits | 149,351 | 353 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 997,697 | 9.977 | 22 | 26 | fits | 149,351 | 353 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,018,350 | 10.184 | 22 | 26 | fits | 149,351 | 353 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 409,724 | 4.097 | 22 | 26 | fits | 38,152 | 62 | 0.340 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 839,689 | 8.397 | 20 | 200 | fits | 158,037 | 156 | 0.554 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,085,287 | 10.853 | 20 | 20 | fits | 119,610 | 91 | 0.473 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 1,065,083 | 10.651 | 20 | 24 | fits | 119,610 | 91 | 0.473 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 926,202 | 9.262 | 20 | 50 | fits | 146,256 | 125 | 0.511 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 551,694 | 5.517 | 20 | 20 | fits | 90,434 | 66 | 0.536 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 833,547 | 8.335 | 22 | 26 | fits | 107,898 | 252 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 854,820 | 8.548 | 22 | 26 | fits | 107,898 | 252 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,030,686 | 10.307 | 22 | 26 | fits | 49,859 | 102 | 0.326 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,052,257 | 10.523 | 22 | 26 | fits | 49,859 | 102 | 0.326 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 216,602 | 2.166 | 22 | 26 | fits | 90,464 | 203 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 238,128 | 2.381 | 22 | 26 | fits | 90,464 | 203 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 258,170 | 2.582 | 22 | 26 | fits | 90,464 | 203 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 279,014 | 2.790 | 22 | 26 | fits | 90,464 | 203 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 873,922 | 8.739 | 22 | 26 | fits | 107,898 | 252 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 891,534 | 8.915 | 22 | 26 | fits | 107,898 | 252 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 912,242 | 9.122 | 22 | 26 | fits | 107,898 | 252 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 406,287 | 4.063 | 22 | 26 | fits | 37,493 | 61 | 0.338 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 967,288 | 9.673 | 20 | 200 | fits | 144,082 | 107 | 0.549 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 1,066,187 | 10.662 | 20 | 20 | fits | 119,167 | 91 | 0.467 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 1,045,983 | 10.460 | 20 | 24 | fits | 119,167 | 91 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 907,545 | 9.075 | 20 | 50 | fits | 144,082 | 107 | 0.549 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 545,177 | 5.452 | 20 | 20 | fits | 89,956 | 66 | 0.534 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 849,387 | 8.494 | 22 | 26 | fits | 106,507 | 252 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 870,685 | 8.707 | 22 | 26 | fits | 106,507 | 252 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 205,265 | 2.053 | 22 | 26 | fits | 141,697 | 312 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 226,777 | 2.268 | 22 | 26 | fits | 141,697 | 312 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 246,887 | 2.469 | 22 | 26 | fits | 141,697 | 312 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 267,500 | 2.675 | 22 | 26 | fits | 141,697 | 312 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 287,251 | 2.873 | 22 | 26 | fits | 141,697 | 312 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 307,872 | 3.079 | 22 | 26 | fits | 141,697 | 312 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 889,808 | 8.898 | 22 | 26 | fits | 106,507 | 252 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 907,189 | 9.072 | 22 | 26 | fits | 106,507 | 252 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 927,688 | 9.277 | 22 | 26 | fits | 106,507 | 252 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 494,581 | 4.946 | 22 | 26 | fits | 29,023 | 53 | 0.390 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 949,490 | 9.495 | 20 | 200 | fits | 144,508 | 107 | 0.550 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 1,048,575 | 10.486 | 20 | 20 | fits | 119,353 | 91 | 0.470 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 1,028,371 | 10.284 | 20 | 24 | fits | 119,353 | 91 | 0.470 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 889,747 | 8.897 | 20 | 50 | fits | 144,508 | 107 | 0.550 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 467,917 | 4.679 | 20 | 20 | fits | 80,360 | 44 | 0.466 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 931,455 | 9.315 | 22 | 26 | fits | 150,266 | 353 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 952,887 | 9.529 | 22 | 26 | fits | 150,266 | 353 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 973,673 | 9.737 | 22 | 26 | fits | 150,266 | 353 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 994,358 | 9.944 | 22 | 26 | fits | 150,266 | 353 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,014,097 | 10.141 | 22 | 26 | fits | 150,266 | 353 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,034,479 | 10.345 | 22 | 26 | fits | 150,266 | 353 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 217,171 | 2.172 | 22 | 26 | fits | 60,605 | 111 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 238,893 | 2.389 | 22 | 26 | fits | 60,605 | 111 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,053,171 | 10.532 | 22 | 26 | fits | 150,266 | 353 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,237,534 | 12.375 | 22 | 26 | fits | 45,228 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,258,618 | 12.586 | 22 | 26 | fits | 45,228 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 423,712 | 4.237 | 22 | 26 | fits | 30,007 | 53 | 0.390 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 1,022,384 | 10.224 | 20 | 200 | fits | 160,134 | 134 | 0.564 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 1,002,116 | 10.021 | 20 | 20 | fits | 160,134 | 134 | 0.564 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 1,133,419 | 11.334 | 20 | 24 | fits | 106,279 | 93 | 0.438 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 962,641 | 9.626 | 20 | 50 | fits | 160,134 | 134 | 0.564 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 478,766 | 4.788 | 20 | 20 | fits | 80,419 | 42 | 0.465 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 855,846 | 8.558 | 22 | 26 | fits | 149,195 | 353 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 877,215 | 8.772 | 22 | 26 | fits | 149,195 | 353 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 898,005 | 8.980 | 22 | 26 | fits | 149,195 | 353 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 918,690 | 9.187 | 22 | 26 | fits | 149,195 | 353 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,149,637 | 11.496 | 22 | 26 | fits | 48,095 | 103 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,170,864 | 11.709 | 22 | 26 | fits | 48,095 | 103 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 287,834 | 2.878 | 22 | 26 | fits | 51,358 | 102 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 309,734 | 3.097 | 22 | 26 | fits | 51,358 | 102 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 937,761 | 9.378 | 22 | 26 | fits | 149,195 | 353 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 955,373 | 9.554 | 22 | 26 | fits | 149,195 | 353 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 976,048 | 9.760 | 22 | 26 | fits | 149,195 | 353 | 0.187 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 476,607 | 4.766 | 22 | 26 | fits | 30,564 | 53 | 0.406 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 740,004 | 7.400 | 20 | 200 | fits | 151,261 | 149 | 0.523 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 1,015,283 | 10.153 | 20 | 20 | fits | 146,352 | 124 | 0.574 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 1,165,147 | 11.651 | 20 | 24 | fits | 121,973 | 105 | 0.434 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 975,808 | 9.758 | 20 | 50 | fits | 146,352 | 124 | 0.574 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 506,975 | 5.070 | 20 | 20 | fits | 81,069 | 42 | 0.488 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 604,347 | 6.043 | 22 | 26 | fits | 138,590 | 311 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 625,557 | 6.256 | 22 | 26 | fits | 138,590 | 311 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 646,209 | 6.462 | 22 | 26 | fits | 138,590 | 311 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 666,910 | 6.669 | 22 | 26 | fits | 138,590 | 311 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 729,343 | 7.293 | 22 | 26 | fits | 66,466 | 155 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 749,964 | 7.500 | 22 | 26 | fits | 66,466 | 155 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 937,381 | 9.374 | 22 | 26 | fits | 69,439 | 153 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 958,474 | 9.585 | 22 | 26 | fits | 69,439 | 153 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 686,348 | 6.863 | 22 | 26 | fits | 138,590 | 311 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 704,270 | 7.043 | 22 | 26 | fits | 138,590 | 311 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 771,232 | 7.712 | 22 | 26 | fits | 66,466 | 155 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 979,465 | 9.795 | 22 | 26 | fits | 69,439 | 153 | 0.266 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 1,034,954 | 10.350 | 20 | 200 | fits | 143,127 | 111 | 0.521 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 1,133,330 | 11.333 | 20 | 20 | fits | 118,644 | 91 | 0.461 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 1,113,126 | 11.131 | 20 | 24 | fits | 118,644 | 91 | 0.461 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 975,211 | 9.752 | 20 | 50 | fits | 143,127 | 111 | 0.521 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 520,025 | 5.200 | 20 | 20 | fits | 80,657 | 42 | 0.484 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 783,300 | 7.833 | 22 | 26 | fits | 149,253 | 352 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 804,296 | 8.043 | 22 | 26 | fits | 149,253 | 352 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 824,874 | 8.249 | 22 | 26 | fits | 149,253 | 352 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 845,504 | 8.455 | 22 | 26 | fits | 149,253 | 352 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,069,014 | 10.690 | 22 | 26 | fits | 109,577 | 253 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,090,270 | 10.903 | 22 | 26 | fits | 109,577 | 253 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,109,959 | 11.100 | 22 | 26 | fits | 109,577 | 253 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 1,130,396 | 11.304 | 22 | 26 | fits | 109,577 | 253 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 864,942 | 8.649 | 22 | 26 | fits | 149,253 | 352 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 882,864 | 8.829 | 22 | 26 | fits | 149,253 | 352 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 903,748 | 9.037 | 22 | 26 | fits | 149,253 | 352 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 1,151,150 | 11.511 | 22 | 26 | fits | 109,577 | 253 | 0.209 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 915,125 | 9.151 | 20 | 200 | fits | 146,856 | 143 | 0.530 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 1,040,352 | 10.404 | 20 | 20 | fits | 145,495 | 123 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 1,122,848 | 11.228 | 20 | 24 | fits | 102,700 | 84 | 0.418 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 1,000,877 | 10.009 | 20 | 50 | fits | 145,495 | 123 | 0.509 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 686,501 | 6.865 | 20 | 20 | fits | 85,356 | 48 | 0.505 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 900,265 | 9.003 | 22 | 26 | fits | 149,234 | 352 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 921,508 | 9.215 | 22 | 26 | fits | 149,234 | 352 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 942,221 | 9.422 | 22 | 26 | fits | 149,234 | 352 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 962,906 | 9.629 | 22 | 26 | fits | 149,234 | 352 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 1,170,183 | 11.702 | 22 | 26 | fits | 48,286 | 102 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 1,191,439 | 11.914 | 22 | 26 | fits | 48,286 | 102 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 216,695 | 2.167 | 22 | 26 | fits | 60,454 | 111 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 238,417 | 2.384 | 22 | 26 | fits | 60,454 | 111 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 982,170 | 9.822 | 22 | 26 | fits | 149,234 | 352 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 999,782 | 9.998 | 22 | 26 | fits | 149,234 | 352 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,020,435 | 10.204 | 22 | 26 | fits | 149,234 | 352 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 392,866 | 3.929 | 22 | 26 | fits | 29,149 | 53 | 0.328 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 151,784 | 1.518 | 20 | 200 | fits | 150,838 | 151 | 0.505 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 974,829 | 9.748 | 20 | 20 | fits | 155,659 | 112 | 0.525 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 1,058,108 | 10.581 | 20 | 24 | fits | 103,483 | 84 | 0.429 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 935,354 | 9.354 | 20 | 50 | fits | 155,659 | 112 | 0.525 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 607,240 | 6.072 | 20 | 20 | fits | 88,851 | 57 | 0.542 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
