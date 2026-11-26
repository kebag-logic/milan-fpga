### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.acmp.if0` (notice-burst-2) | 5.455 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.adp.if0` (notice-burst-2) | 5.658 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-7.held.aecp.if0` (notice-burst-7) | 4.273 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.maap.if0` (notice-burst-2) | 5.060 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.srp.if0` (notice-burst-2) | 10.264 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 1.040 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 20.707 (21.783) | fits | 0 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 2066 | 0 | 150,277 (1.503) | fits |
| notice-every-1 | 2055 | 0 | 151,508 (1.515) | fits |
| notice-every-2 | 2060 | 0 | 150,500 (1.505) | fits |
| notice-every-3 | 2051 | 0 | 150,582 (1.506) | fits |
| notice-every-4 | 2053 | 0 | 150,521 (1.505) | fits |
| notice-every-5 | 2059 | 0 | 150,336 (1.503) | fits |
| notice-every-6 | 2054 | 0 | 150,336 (1.503) | fits |
| notice-every-7 | 2045 | 0 | 150,369 (1.504) | fits |
| notice-burst-0 | 1334 | 0 | 153,339 (1.533) | fits |
| notice-burst-1 | 1315 | 0 | 151,182 (1.512) | fits |
| notice-burst-2 | 1345 | 0 | 153,665 (1.537) | fits |
| notice-burst-3 | 1318 | 0 | 152,390 (1.524) | fits |
| notice-burst-4 | 1319 | 0 | 150,174 (1.502) | fits |
| notice-burst-5 | 1333 | 0 | 151,515 (1.515) | fits |
| notice-burst-6 | 1319 | 0 | 150,608 (1.506) | fits |
| notice-burst-7 | 1326 | 0 | 151,311 (1.513) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 7.955 | 130 | 16 | 2 | within |
| notice-every-0 | 8.129 | 130 | 16 | 2 | within |
| notice-every-0 | 1.900 | 130 | 16 | 2 | within |
| notice-every-0 | 2.076 | 130 | 16 | 2 | within |
| notice-every-0 | 3.787 | 130 | 16 | 2 | within |
| notice-every-0 | 3.966 | 130 | 16 | 2 | within |
| notice-every-0 | 5.886 | 130 | 16 | 2 | within |
| notice-every-0 | 6.062 | 130 | 16 | 2 | within |
| notice-every-0 | 8.260 | 130 | 16 | 2 | within |
| notice-every-0 | 9.855 | 130 | 16 | 2 | within |
| notice-every-0 | 2.251 | 130 | 16 | 2 | within |
| notice-every-0 | 4.142 | 130 | 16 | 2 | within |
| notice-every-1 | 2.125 | 130 | 16 | 2 | within |
| notice-every-1 | 2.302 | 130 | 16 | 2 | within |
| notice-every-1 | 4.146 | 130 | 16 | 2 | within |
| notice-every-1 | 4.321 | 130 | 16 | 2 | within |
| notice-every-1 | 6.104 | 130 | 16 | 2 | within |
| notice-every-1 | 6.279 | 130 | 16 | 2 | within |
| notice-every-1 | 8.111 | 130 | 16 | 2 | within |
| notice-every-1 | 8.282 | 130 | 16 | 2 | within |
| notice-every-1 | 2.443 | 130 | 16 | 2 | within |
| notice-every-1 | 4.453 | 130 | 16 | 2 | within |
| notice-every-1 | 6.450 | 130 | 16 | 2 | within |
| notice-every-1 | 8.448 | 130 | 16 | 2 | within |
| notice-every-2 | 1.844 | 130 | 16 | 2 | within |
| notice-every-2 | 2.020 | 130 | 16 | 2 | within |
| notice-every-2 | 3.825 | 130 | 16 | 2 | within |
| notice-every-2 | 4.000 | 130 | 16 | 2 | within |
| notice-every-2 | 5.818 | 130 | 16 | 2 | within |
| notice-every-2 | 5.991 | 130 | 16 | 2 | within |
| notice-every-2 | 7.821 | 130 | 16 | 2 | within |
| notice-every-2 | 7.992 | 130 | 16 | 2 | within |
| notice-every-2 | 2.158 | 130 | 16 | 2 | within |
| notice-every-2 | 4.133 | 130 | 16 | 2 | within |
| notice-every-2 | 6.162 | 130 | 16 | 2 | within |
| notice-every-2 | 8.158 | 130 | 16 | 2 | within |
| notice-every-3 | 3.912 | 130 | 16 | 2 | within |
| notice-every-3 | 4.088 | 130 | 16 | 2 | within |
| notice-every-3 | 5.767 | 130 | 16 | 2 | within |
| notice-every-3 | 5.942 | 130 | 16 | 2 | within |
| notice-every-3 | 7.904 | 130 | 16 | 2 | within |
| notice-every-3 | 8.078 | 130 | 16 | 2 | within |
| notice-every-3 | 1.843 | 130 | 16 | 2 | within |
| notice-every-3 | 2.024 | 130 | 16 | 2 | within |
| notice-every-3 | 4.224 | 130 | 16 | 2 | within |
| notice-every-3 | 6.072 | 130 | 16 | 2 | within |
| notice-every-3 | 2.198 | 130 | 16 | 2 | within |
| notice-every-3 | 8.246 | 130 | 16 | 2 | within |
| notice-every-4 | 3.874 | 130 | 16 | 2 | within |
| notice-every-4 | 4.050 | 130 | 16 | 2 | within |
| notice-every-4 | 5.912 | 130 | 16 | 2 | within |
| notice-every-4 | 6.088 | 130 | 16 | 2 | within |
| notice-every-4 | 7.904 | 130 | 16 | 2 | within |
| notice-every-4 | 8.078 | 130 | 16 | 2 | within |
| notice-every-4 | 1.842 | 130 | 16 | 2 | within |
| notice-every-4 | 2.023 | 130 | 16 | 2 | within |
| notice-every-4 | 4.186 | 130 | 16 | 2 | within |
| notice-every-4 | 6.217 | 130 | 16 | 2 | within |
| notice-every-4 | 2.198 | 130 | 16 | 2 | within |
| notice-every-4 | 8.247 | 130 | 16 | 2 | within |
| notice-every-5 | 6.046 | 130 | 16 | 2 | within |
| notice-every-5 | 6.222 | 130 | 16 | 2 | within |
| notice-every-5 | 7.874 | 130 | 16 | 2 | within |
| notice-every-5 | 8.049 | 130 | 16 | 2 | within |
| notice-every-5 | 1.980 | 130 | 16 | 2 | within |
| notice-every-5 | 2.161 | 130 | 16 | 2 | within |
| notice-every-5 | 4.046 | 130 | 16 | 2 | within |
| notice-every-5 | 4.225 | 130 | 16 | 2 | within |
| notice-every-5 | 6.355 | 130 | 16 | 2 | within |
| notice-every-5 | 8.177 | 130 | 16 | 2 | within |
| notice-every-5 | 2.338 | 130 | 16 | 2 | within |
| notice-every-5 | 4.399 | 130 | 16 | 2 | within |
| notice-every-6 | 6.011 | 130 | 16 | 2 | within |
| notice-every-6 | 6.186 | 130 | 16 | 2 | within |
| notice-every-6 | 7.841 | 130 | 16 | 2 | within |
| notice-every-6 | 8.016 | 130 | 16 | 2 | within |
| notice-every-6 | 1.842 | 130 | 16 | 2 | within |
| notice-every-6 | 2.024 | 130 | 16 | 2 | within |
| notice-every-6 | 3.872 | 130 | 16 | 2 | within |
| notice-every-6 | 4.052 | 130 | 16 | 2 | within |
| notice-every-6 | 6.320 | 130 | 16 | 2 | within |
| notice-every-6 | 8.144 | 130 | 16 | 2 | within |
| notice-every-6 | 2.200 | 130 | 16 | 2 | within |
| notice-every-6 | 4.226 | 130 | 16 | 2 | within |
| notice-every-7 | 7.976 | 130 | 16 | 2 | within |
| notice-every-7 | 8.150 | 130 | 16 | 2 | within |
| notice-every-7 | 1.762 | 130 | 16 | 2 | within |
| notice-every-7 | 1.938 | 130 | 16 | 2 | within |
| notice-every-7 | 3.789 | 130 | 16 | 2 | within |
| notice-every-7 | 3.968 | 130 | 16 | 2 | within |
| notice-every-7 | 5.921 | 130 | 16 | 2 | within |
| notice-every-7 | 6.096 | 130 | 16 | 2 | within |
| notice-every-7 | 8.281 | 130 | 16 | 2 | within |
| notice-every-7 | 9.743 | 130 | 16 | 2 | within |
| notice-every-7 | 2.113 | 130 | 16 | 2 | within |
| notice-every-7 | 4.143 | 130 | 16 | 2 | within |
| notice-burst-0 | 8.946 | 130 | 16 | 0 | within |
| notice-burst-0 | 15.608 | 130 | 16 | 0 | within |
| notice-burst-0 | 1.891 | 130 | 16 | 0 | within |
| notice-burst-0 | 2.068 | 130 | 16 | 0 | within |
| notice-burst-0 | 2.224 | 130 | 16 | 0 | within |
| notice-burst-0 | 2.500 | 130 | 16 | 0 | within |
| notice-burst-0 | 3.242 | 130 | 16 | 0 | within |
| notice-burst-0 | 3.418 | 130 | 16 | 0 | within |
| notice-burst-0 | 15.746 | 130 | 16 | 0 | within |
| notice-burst-0 | 15.865 | 130 | 16 | 0 | within |
| notice-burst-0 | 16.845 | 130 | 16 | 0 | within |
| notice-burst-0 | 7.153 | 130 | 16 | 0 | within |
| notice-burst-1 | 14.465 | 130 | 16 | 1 | within |
| notice-burst-1 | 14.642 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.861 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.038 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.194 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.468 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.247 | 130 | 16 | 1 | within |
| notice-burst-1 | 14.812 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.050 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.170 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.341 | 130 | 16 | 1 | within |
| notice-burst-1 | 18.105 | 130 | 16 | 1 | within |
| notice-burst-2 | 8.409 | 130 | 16 | 0 | within |
| notice-burst-2 | 13.973 | 130 | 16 | 0 | within |
| notice-burst-2 | 14.145 | 130 | 16 | 0 | within |
| notice-burst-2 | 14.315 | 130 | 16 | 0 | within |
| notice-burst-2 | 1.895 | 130 | 16 | 0 | within |
| notice-burst-2 | 2.077 | 130 | 16 | 0 | within |
| notice-burst-2 | 2.710 | 130 | 16 | 0 | within |
| notice-burst-2 | 2.889 | 130 | 16 | 0 | within |
| notice-burst-2 | 15.799 | 130 | 16 | 0 | within |
| notice-burst-2 | 15.919 | 130 | 16 | 0 | within |
| notice-burst-2 | 16.090 | 130 | 16 | 0 | within |
| notice-burst-2 | 5.476 | 130 | 16 | 0 | within |
| notice-burst-3 | 5.044 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.220 | 130 | 16 | 1 | within |
| notice-burst-3 | 7.761 | 130 | 16 | 1 | within |
| notice-burst-3 | 15.806 | 130 | 16 | 1 | within |
| notice-burst-3 | 15.972 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.141 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.138 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.308 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.359 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.742 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.923 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.475 | 130 | 16 | 1 | within |
| notice-burst-4 | 6.057 | 130 | 16 | 1 | within |
| notice-burst-4 | 6.234 | 130 | 16 | 1 | within |
| notice-burst-4 | 15.913 | 130 | 16 | 1 | within |
| notice-burst-4 | 16.091 | 130 | 16 | 1 | within |
| notice-burst-4 | 16.244 | 130 | 16 | 1 | within |
| notice-burst-4 | 17.129 | 130 | 16 | 1 | within |
| notice-burst-4 | 17.292 | 130 | 16 | 1 | within |
| notice-burst-4 | 17.460 | 130 | 16 | 1 | within |
| notice-burst-4 | 6.373 | 130 | 16 | 1 | within |
| notice-burst-4 | 19.070 | 130 | 16 | 1 | within |
| notice-burst-4 | 19.243 | 130 | 16 | 1 | within |
| notice-burst-4 | 19.409 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.847 | 130 | 16 | 0 | within |
| notice-burst-5 | 15.051 | 130 | 16 | 0 | within |
| notice-burst-5 | 15.223 | 130 | 16 | 0 | within |
| notice-burst-5 | 15.391 | 130 | 16 | 0 | within |
| notice-burst-5 | 16.531 | 130 | 16 | 0 | within |
| notice-burst-5 | 16.704 | 130 | 16 | 0 | within |
| notice-burst-5 | 16.857 | 130 | 16 | 0 | within |
| notice-burst-5 | 18.517 | 130 | 16 | 0 | within |
| notice-burst-5 | 18.653 | 130 | 16 | 0 | within |
| notice-burst-5 | 18.770 | 130 | 16 | 0 | within |
| notice-burst-5 | 20.539 | 130 | 16 | 0 | within |
| notice-burst-5 | 20.707 | 130 | 16 | 0 | within |
| notice-burst-6 | 7.395 | 130 | 16 | 0 | within |
| notice-burst-6 | 15.439 | 130 | 16 | 0 | within |
| notice-burst-6 | 15.612 | 130 | 16 | 0 | within |
| notice-burst-6 | 15.782 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.123 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.306 | 130 | 16 | 0 | within |
| notice-burst-6 | 2.905 | 130 | 16 | 0 | within |
| notice-burst-6 | 3.083 | 130 | 16 | 0 | within |
| notice-burst-6 | 16.491 | 130 | 16 | 0 | within |
| notice-burst-6 | 16.611 | 130 | 16 | 0 | within |
| notice-burst-6 | 16.781 | 130 | 16 | 0 | within |
| notice-burst-6 | 3.543 | 130 | 16 | 0 | within |
| notice-burst-7 | 8.720 | 130 | 16 | 0 | within |
| notice-burst-7 | 15.220 | 130 | 16 | 0 | within |
| notice-burst-7 | 15.394 | 130 | 16 | 0 | within |
| notice-burst-7 | 15.564 | 130 | 16 | 0 | within |
| notice-burst-7 | 1.568 | 130 | 16 | 0 | within |
| notice-burst-7 | 1.749 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.492 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.670 | 130 | 16 | 0 | within |
| notice-burst-7 | 16.400 | 130 | 16 | 0 | within |
| notice-burst-7 | 16.520 | 130 | 16 | 0 | within |
| notice-burst-7 | 1.926 | 130 | 16 | 0 | within |
| notice-burst-7 | 4.312 | 130 | 16 | 0 | within |

Latest: 20.707 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 404 | 93,660 (0.937) | 78,364 (0.784) |
| notice-every-1 | 404 | 93,660 (0.937) | 78,364 (0.784) |
| notice-every-2 | 404 | 93,660 (0.937) | 78,364 (0.784) |
| notice-every-3 | 404 | 93,660 (0.937) | 78,364 (0.784) |
| notice-every-4 | 404 | 93,660 (0.937) | 78,364 (0.784) |
| notice-every-5 | 404 | 93,660 (0.937) | 78,364 (0.784) |
| notice-every-6 | 404 | 93,660 (0.937) | 78,364 (0.784) |
| notice-every-7 | 404 | 93,660 (0.937) | 78,364 (0.784) |
| notice-burst-0 | 473 | 131,677 (1.317) | 79,126 (0.791) |
| notice-burst-1 | 473 | 107,341 (1.073) | 79,137 (0.791) |
| notice-burst-2 | 473 | 133,203 (1.332) | 78,904 (0.789) |
| notice-burst-3 | 474 | 103,464 (1.035) | 79,314 (0.793) |
| notice-burst-4 | 460 | 103,180 (1.032) | 78,496 (0.785) |
| notice-burst-5 | 462 | 105,594 (1.056) | 78,853 (0.789) |
| notice-burst-6 | 460 | 119,705 (1.197) | 78,974 (0.790) |
| notice-burst-7 | 460 | 106,481 (1.065) | 78,853 (0.789) |

Longest pass that carries a step: 133,203 CPU cycles (1.332 ms), notice-burst-2; longest step: 79,314 (0.793 ms), notice-burst-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 795,494 | 7.955 | 130 | 134 | fits | 54,580 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 812,868 | 8.129 | 130 | 134 | fits | 54,580 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 189,968 | 1.900 | 130 | 134 | fits | 60,817 | 153 | 0.194 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 207,618 | 2.076 | 130 | 134 | fits | 60,817 | 153 | 0.194 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 378,730 | 3.787 | 130 | 134 | fits | 60,289 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 396,640 | 3.966 | 130 | 134 | fits | 60,289 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 588,600 | 5.886 | 130 | 134 | fits | 41,360 | 103 | 0.243 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 606,164 | 6.062 | 130 | 134 | fits | 41,360 | 103 | 0.243 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 826,037 | 8.260 | 130 | 134 | fits | 54,580 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 985,529 | 9.855 | 130 | 134 | fits | 19,369 | 51 | 0.350 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 225,145 | 2.251 | 130 | 134 | fits | 60,817 | 153 | 0.194 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 414,208 | 4.142 | 130 | 134 | fits | 60,289 | 155 | 0.188 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 136,747 | 1.367 | 20 | 200 | fits | 131,712 | 157 | 0.165 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 414,985 | 4.150 | 20 | 20 | fits | 126,648 | 129 | 0.449 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 394,781 | 3.948 | 20 | 24 | fits | 126,648 | 129 | 0.449 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 375,510 | 3.755 | 20 | 50 | fits | 126,648 | 129 | 0.449 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 953,273 | 9.533 | 20 | 20 | fits | 60,958 | 39 | 0.755 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 80,263 | 0.803 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 212,452 | 2.125 | 130 | 134 | fits | 57,911 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 230,179 | 2.302 | 130 | 134 | fits | 57,911 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 414,572 | 4.146 | 130 | 134 | fits | 55,027 | 151 | 0.223 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 432,082 | 4.321 | 130 | 134 | fits | 55,027 | 151 | 0.223 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 610,438 | 6.104 | 130 | 134 | fits | 58,364 | 153 | 0.186 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 627,867 | 6.279 | 130 | 134 | fits | 58,364 | 153 | 0.186 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 811,059 | 8.111 | 130 | 134 | fits | 56,446 | 153 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 828,211 | 8.282 | 130 | 134 | fits | 56,446 | 153 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 244,279 | 2.443 | 130 | 134 | fits | 57,911 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 445,309 | 4.453 | 130 | 134 | fits | 55,027 | 151 | 0.223 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 644,967 | 6.450 | 130 | 134 | fits | 58,364 | 153 | 0.186 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 844,803 | 8.448 | 130 | 134 | fits | 56,446 | 153 | 0.174 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 135,433 | 1.354 | 20 | 200 | fits | 131,551 | 157 | 0.165 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 433,508 | 4.335 | 20 | 20 | fits | 127,976 | 136 | 0.452 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 413,304 | 4.133 | 20 | 24 | fits | 127,976 | 136 | 0.452 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 394,033 | 3.940 | 20 | 50 | fits | 127,976 | 136 | 0.452 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 955,415 | 9.554 | 20 | 20 | fits | 55,980 | 27 | 0.749 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 103,994 | 1.040 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 184,439 | 1.844 | 130 | 134 | fits | 56,717 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 202,036 | 2.020 | 130 | 134 | fits | 56,717 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 382,489 | 3.825 | 130 | 134 | fits | 55,210 | 151 | 0.227 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 400,007 | 4.000 | 130 | 134 | fits | 55,210 | 151 | 0.227 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 581,777 | 5.818 | 130 | 134 | fits | 57,969 | 153 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 599,132 | 5.991 | 130 | 134 | fits | 57,969 | 153 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 782,056 | 7.821 | 130 | 134 | fits | 56,446 | 153 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 799,208 | 7.992 | 130 | 134 | fits | 56,446 | 153 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 215,841 | 2.158 | 130 | 134 | fits | 56,717 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 413,287 | 4.133 | 130 | 134 | fits | 55,210 | 151 | 0.227 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 616,232 | 6.162 | 130 | 134 | fits | 57,969 | 153 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 815,800 | 8.158 | 130 | 134 | fits | 56,446 | 153 | 0.174 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 164,700 | 1.647 | 20 | 200 | fits | 146,908 | 261 | 0.243 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 443,134 | 4.431 | 20 | 20 | fits | 123,524 | 121 | 0.465 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 422,930 | 4.229 | 20 | 24 | fits | 123,524 | 121 | 0.465 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 403,659 | 4.037 | 20 | 50 | fits | 123,524 | 121 | 0.465 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 960,678 | 9.607 | 20 | 20 | fits | 44,104 | 23 | 0.772 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 82,131 | 0.821 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 391,223 | 3.912 | 130 | 134 | fits | 56,510 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 408,849 | 4.088 | 130 | 134 | fits | 56,510 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 576,689 | 5.767 | 130 | 134 | fits | 54,835 | 153 | 0.226 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 594,240 | 5.942 | 130 | 134 | fits | 54,835 | 153 | 0.226 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 790,378 | 7.904 | 130 | 134 | fits | 57,257 | 153 | 0.180 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 807,766 | 8.078 | 130 | 134 | fits | 57,257 | 153 | 0.180 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 184,266 | 1.843 | 130 | 134 | fits | 60,718 | 153 | 0.183 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 202,352 | 2.024 | 130 | 134 | fits | 60,718 | 153 | 0.183 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 422,423 | 4.224 | 130 | 134 | fits | 56,510 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 607,234 | 6.072 | 130 | 134 | fits | 54,835 | 153 | 0.226 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 219,814 | 2.198 | 130 | 134 | fits | 60,718 | 153 | 0.183 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 824,641 | 8.246 | 130 | 134 | fits | 57,257 | 153 | 0.180 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 163,303 | 1.633 | 20 | 200 | fits | 147,080 | 260 | 0.244 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 445,530 | 4.455 | 20 | 20 | fits | 124,638 | 127 | 0.467 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 425,326 | 4.253 | 20 | 24 | fits | 124,638 | 127 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 406,055 | 4.061 | 20 | 50 | fits | 124,638 | 127 | 0.467 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 978,118 | 9.781 | 20 | 20 | fits | 56,284 | 27 | 0.756 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 73,593 | 0.736 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 387,357 | 3.874 | 130 | 134 | fits | 56,457 | 153 | 0.234 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 404,983 | 4.050 | 130 | 134 | fits | 56,457 | 153 | 0.234 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 591,201 | 5.912 | 130 | 134 | fits | 54,689 | 151 | 0.226 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 608,752 | 6.088 | 130 | 134 | fits | 54,689 | 151 | 0.226 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 790,389 | 7.904 | 130 | 134 | fits | 57,257 | 153 | 0.180 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 807,777 | 8.078 | 130 | 134 | fits | 57,257 | 153 | 0.180 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 184,233 | 1.842 | 130 | 134 | fits | 60,665 | 153 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 202,319 | 2.023 | 130 | 134 | fits | 60,665 | 153 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 418,557 | 4.186 | 130 | 134 | fits | 56,457 | 153 | 0.234 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 621,746 | 6.217 | 130 | 134 | fits | 54,689 | 151 | 0.226 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 219,781 | 2.198 | 130 | 134 | fits | 60,665 | 153 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 824,652 | 8.247 | 130 | 134 | fits | 57,257 | 153 | 0.180 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 158,604 | 1.586 | 20 | 200 | fits | 148,171 | 263 | 0.235 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 445,495 | 4.455 | 20 | 20 | fits | 123,819 | 123 | 0.472 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 425,291 | 4.253 | 20 | 24 | fits | 123,819 | 123 | 0.472 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 406,020 | 4.060 | 20 | 50 | fits | 123,819 | 123 | 0.472 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 982,579 | 9.826 | 20 | 20 | fits | 56,342 | 27 | 0.756 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 78,795 | 0.788 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 604,631 | 6.046 | 130 | 134 | fits | 55,482 | 153 | 0.228 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 622,159 | 6.222 | 130 | 134 | fits | 55,482 | 153 | 0.228 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 787,352 | 7.874 | 130 | 134 | fits | 54,055 | 153 | 0.225 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 804,862 | 8.049 | 130 | 134 | fits | 54,055 | 153 | 0.225 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 198,026 | 1.980 | 130 | 134 | fits | 60,898 | 153 | 0.183 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 216,149 | 2.161 | 130 | 134 | fits | 60,898 | 153 | 0.183 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 404,574 | 4.046 | 130 | 134 | fits | 60,020 | 153 | 0.187 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 422,489 | 4.225 | 130 | 134 | fits | 60,020 | 153 | 0.187 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 635,502 | 6.355 | 130 | 134 | fits | 55,482 | 153 | 0.228 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 817,678 | 8.177 | 130 | 134 | fits | 54,055 | 153 | 0.225 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 233,755 | 2.338 | 130 | 134 | fits | 60,898 | 153 | 0.183 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 439,913 | 4.399 | 130 | 134 | fits | 60,020 | 153 | 0.187 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 163,835 | 1.638 | 20 | 200 | fits | 146,551 | 260 | 0.235 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 446,014 | 4.460 | 20 | 20 | fits | 125,000 | 129 | 0.472 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 425,810 | 4.258 | 20 | 24 | fits | 125,000 | 129 | 0.472 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 406,539 | 4.065 | 20 | 50 | fits | 125,000 | 129 | 0.472 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 976,631 | 9.766 | 20 | 20 | fits | 56,294 | 27 | 0.755 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 78,126 | 0.781 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 601,117 | 6.011 | 130 | 134 | fits | 55,472 | 153 | 0.229 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 618,645 | 6.186 | 130 | 134 | fits | 55,472 | 153 | 0.229 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 784,060 | 7.841 | 130 | 134 | fits | 54,088 | 153 | 0.226 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 801,603 | 8.016 | 130 | 134 | fits | 54,088 | 153 | 0.226 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 184,247 | 1.842 | 130 | 134 | fits | 61,097 | 155 | 0.185 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 202,370 | 2.024 | 130 | 134 | fits | 61,097 | 155 | 0.185 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 387,242 | 3.872 | 130 | 134 | fits | 60,020 | 153 | 0.187 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 405,157 | 4.052 | 130 | 134 | fits | 60,020 | 153 | 0.187 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 632,045 | 6.320 | 130 | 134 | fits | 55,472 | 153 | 0.229 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 814,419 | 8.144 | 130 | 134 | fits | 54,088 | 153 | 0.226 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 219,976 | 2.200 | 130 | 134 | fits | 61,097 | 155 | 0.185 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 422,581 | 4.226 | 130 | 134 | fits | 60,020 | 153 | 0.187 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 160,263 | 1.603 | 20 | 200 | fits | 148,820 | 266 | 0.235 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 432,921 | 4.329 | 20 | 20 | fits | 124,367 | 127 | 0.470 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 412,717 | 4.127 | 20 | 24 | fits | 124,367 | 127 | 0.470 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 393,446 | 3.934 | 20 | 50 | fits | 124,367 | 127 | 0.470 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 962,642 | 9.626 | 20 | 20 | fits | 59,810 | 33 | 0.768 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 77,478 | 0.775 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 797,591 | 7.976 | 130 | 134 | fits | 54,590 | 152 | 0.225 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 814,965 | 8.150 | 130 | 134 | fits | 54,590 | 152 | 0.225 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 176,152 | 1.762 | 130 | 134 | fits | 61,016 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 193,802 | 1.938 | 130 | 134 | fits | 61,016 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 378,870 | 3.789 | 130 | 134 | fits | 60,289 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 396,780 | 3.968 | 130 | 134 | fits | 60,289 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 592,070 | 5.921 | 130 | 134 | fits | 41,360 | 103 | 0.243 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 609,634 | 6.096 | 130 | 134 | fits | 41,360 | 103 | 0.243 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 828,077 | 8.281 | 130 | 134 | fits | 54,590 | 152 | 0.225 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 974,307 | 9.743 | 130 | 134 | fits | 19,336 | 51 | 0.346 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 211,329 | 2.113 | 130 | 134 | fits | 61,016 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 414,348 | 4.143 | 130 | 134 | fits | 60,289 | 155 | 0.188 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 161,212 | 1.612 | 20 | 200 | fits | 146,592 | 261 | 0.235 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 440,920 | 4.409 | 20 | 20 | fits | 122,697 | 117 | 0.474 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 420,716 | 4.207 | 20 | 24 | fits | 122,697 | 117 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 401,445 | 4.014 | 20 | 50 | fits | 122,697 | 117 | 0.474 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 978,223 | 9.782 | 20 | 20 | fits | 56,288 | 27 | 0.755 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 78,360 | 0.784 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 894,611 | 8.946 | 130 | 134 | fits | 26,084 | 52 | 0.496 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,560,820 | 15.608 | 130 | 134 | fits | 51,551 | 152 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 189,070 | 1.891 | 130 | 134 | fits | 74,941 | 162 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 206,786 | 2.068 | 130 | 134 | fits | 74,941 | 162 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 222,384 | 2.224 | 130 | 134 | fits | 74,941 | 162 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 249,996 | 2.500 | 130 | 134 | fits | 23,036 | 53 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 324,190 | 3.242 | 130 | 134 | fits | 131,677 | 110 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 341,802 | 3.418 | 130 | 134 | fits | 131,677 | 110 | 0.069 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,574,649 | 15.746 | 130 | 134 | fits | 51,551 | 152 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,586,515 | 15.865 | 130 | 134 | fits | 51,551 | 152 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,684,507 | 16.845 | 130 | 134 | fits | 23,893 | 52 | 0.269 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 715,333 | 7.153 | 130 | 134 | fits | 25,136 | 53 | 0.303 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 551,643 | 5.516 | 20 | 200 | fits | 117,777 | 201 | 0.295 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 531,375 | 5.314 | 20 | 20 | fits | 117,777 | 201 | 0.295 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 367,310 | 3.673 | 20 | 24 | fits | 153,339 | 184 | 0.416 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 491,900 | 4.919 | 20 | 50 | fits | 117,777 | 201 | 0.295 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 977,981 | 9.780 | 20 | 20 | fits | 89,288 | 38 | 0.713 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 1,446,521 | 14.465 | 130 | 134 | fits | 60,404 | 153 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,464,180 | 14.642 | 130 | 134 | fits | 60,404 | 153 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 286,090 | 2.861 | 130 | 134 | fits | 74,909 | 160 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 303,806 | 3.038 | 130 | 134 | fits | 74,909 | 160 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 319,404 | 3.194 | 130 | 134 | fits | 74,909 | 160 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 346,772 | 3.468 | 130 | 134 | fits | 23,007 | 53 | 0.122 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 624,684 | 6.247 | 130 | 134 | fits | 23,985 | 52 | 0.440 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 1,481,168 | 14.812 | 130 | 134 | fits | 60,404 | 153 | 0.229 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,604,964 | 16.050 | 130 | 134 | fits | 49,568 | 152 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,617,045 | 16.170 | 130 | 134 | fits | 49,568 | 152 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,634,093 | 16.341 | 130 | 134 | fits | 49,568 | 152 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 1,810,493 | 18.105 | 130 | 134 | fits | 23,512 | 52 | 0.259 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 509,307 | 5.093 | 20 | 200 | fits | 119,465 | 197 | 0.216 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 489,039 | 4.890 | 20 | 20 | fits | 119,465 | 197 | 0.216 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 349,370 | 3.494 | 20 | 24 | fits | 146,771 | 175 | 0.435 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 449,564 | 4.496 | 20 | 50 | fits | 119,465 | 197 | 0.216 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 957,185 | 9.572 | 20 | 20 | fits | 31,110 | 18 | 0.802 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 840,903 | 8.409 | 130 | 134 | fits | 26,180 | 51 | 0.494 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,397,322 | 13.973 | 130 | 134 | fits | 60,048 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,414,537 | 14.145 | 130 | 134 | fits | 60,048 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,431,502 | 14.315 | 130 | 134 | fits | 60,048 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 189,512 | 1.895 | 130 | 134 | fits | 43,751 | 102 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 207,731 | 2.077 | 130 | 134 | fits | 43,751 | 102 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 271,034 | 2.710 | 130 | 134 | fits | 133,203 | 112 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 288,896 | 2.889 | 130 | 134 | fits | 133,203 | 112 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,579,876 | 15.799 | 130 | 134 | fits | 49,556 | 152 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,591,906 | 15.919 | 130 | 134 | fits | 49,556 | 152 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,609,035 | 16.090 | 130 | 134 | fits | 49,556 | 152 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 547,577 | 5.476 | 130 | 134 | fits | 24,953 | 52 | 0.286 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 565,791 | 5.658 | 20 | 200 | fits | 118,376 | 194 | 0.221 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 545,523 | 5.455 | 20 | 20 | fits | 118,376 | 194 | 0.221 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 406,943 | 4.069 | 20 | 24 | fits | 148,998 | 180 | 0.419 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 506,048 | 5.060 | 20 | 50 | fits | 118,376 | 194 | 0.221 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,026,386 | 10.264 | 20 | 20 | fits | 89,367 | 38 | 0.713 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 504,381 | 5.044 | 130 | 134 | fits | 57,123 | 152 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 522,044 | 5.220 | 130 | 134 | fits | 57,123 | 152 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 776,093 | 7.761 | 130 | 134 | fits | 25,991 | 52 | 0.487 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,580,562 | 15.806 | 130 | 134 | fits | 59,515 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,597,204 | 15.972 | 130 | 134 | fits | 59,515 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,614,123 | 16.141 | 130 | 134 | fits | 59,515 | 153 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 1,713,765 | 17.138 | 130 | 134 | fits | 56,500 | 153 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,730,849 | 17.308 | 130 | 134 | fits | 56,500 | 153 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 535,906 | 5.359 | 130 | 134 | fits | 57,123 | 152 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 574,172 | 5.742 | 130 | 134 | fits | 61,406 | 117 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 592,343 | 5.923 | 130 | 134 | fits | 61,406 | 117 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 1,747,523 | 17.475 | 130 | 134 | fits | 56,500 | 153 | 0.177 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 163,120 | 1.631 | 20 | 200 | fits | 152,390 | 264 | 0.272 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 438,154 | 4.382 | 20 | 20 | fits | 121,073 | 114 | 0.472 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 417,950 | 4.179 | 20 | 24 | fits | 121,073 | 114 | 0.472 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 398,679 | 3.987 | 20 | 50 | fits | 121,073 | 114 | 0.472 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 885,584 | 8.856 | 20 | 20 | fits | 78,583 | 34 | 0.727 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 605,730 | 6.057 | 130 | 134 | fits | 57,270 | 152 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 623,393 | 6.234 | 130 | 134 | fits | 57,270 | 152 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,591,317 | 15.913 | 130 | 134 | fits | 58,599 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,609,064 | 16.091 | 130 | 134 | fits | 58,599 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,624,366 | 16.244 | 130 | 134 | fits | 58,599 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,712,894 | 17.129 | 130 | 134 | fits | 57,004 | 153 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,729,226 | 17.292 | 130 | 134 | fits | 57,004 | 153 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,745,975 | 17.460 | 130 | 134 | fits | 57,004 | 153 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 637,270 | 6.373 | 130 | 134 | fits | 57,270 | 152 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,906,969 | 19.070 | 130 | 134 | fits | 53,330 | 152 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,924,260 | 19.243 | 130 | 134 | fits | 53,330 | 152 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,940,861 | 19.409 | 130 | 134 | fits | 53,330 | 152 | 0.152 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 471,654 | 4.717 | 20 | 200 | fits | 121,606 | 204 | 0.200 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 451,386 | 4.514 | 20 | 20 | fits | 121,606 | 204 | 0.200 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 309,576 | 3.096 | 20 | 24 | fits | 147,330 | 179 | 0.419 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 411,911 | 4.119 | 20 | 50 | fits | 121,606 | 204 | 0.200 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 899,338 | 8.993 | 20 | 20 | fits | 78,662 | 34 | 0.727 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 684,664 | 6.847 | 130 | 134 | fits | 25,480 | 52 | 0.457 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,505,118 | 15.051 | 130 | 134 | fits | 60,427 | 153 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,522,298 | 15.223 | 130 | 134 | fits | 60,427 | 153 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,539,146 | 15.391 | 130 | 134 | fits | 60,427 | 153 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,653,114 | 16.531 | 130 | 134 | fits | 56,042 | 152 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,670,421 | 16.704 | 130 | 134 | fits | 56,042 | 152 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,685,661 | 16.857 | 130 | 134 | fits | 56,042 | 152 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,851,683 | 18.517 | 130 | 134 | fits | 49,282 | 152 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 1,865,304 | 18.653 | 130 | 134 | fits | 49,282 | 152 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 1,877,045 | 18.770 | 130 | 134 | fits | 49,282 | 152 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,053,937 | 20.539 | 130 | 134 | fits | 40,204 | 103 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,070,705 | 20.707 | 130 | 134 | fits | 40,204 | 103 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 526,591 | 5.266 | 20 | 200 | fits | 120,279 | 203 | 0.205 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 506,323 | 5.063 | 20 | 20 | fits | 120,279 | 203 | 0.205 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 365,840 | 3.658 | 20 | 24 | fits | 149,068 | 183 | 0.431 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 466,848 | 4.668 | 20 | 50 | fits | 120,279 | 203 | 0.205 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 955,123 | 9.551 | 20 | 20 | fits | 90,014 | 38 | 0.717 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 739,476 | 7.395 | 130 | 134 | fits | 25,305 | 52 | 0.460 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,543,863 | 15.439 | 130 | 134 | fits | 60,296 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,561,186 | 15.612 | 130 | 134 | fits | 60,296 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,578,183 | 15.782 | 130 | 134 | fits | 60,296 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 212,343 | 2.123 | 130 | 134 | fits | 43,672 | 102 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 230,562 | 2.306 | 130 | 134 | fits | 43,672 | 102 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 290,458 | 2.905 | 130 | 134 | fits | 58,524 | 111 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 308,281 | 3.083 | 130 | 134 | fits | 58,524 | 111 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 1,649,067 | 16.491 | 130 | 134 | fits | 49,468 | 152 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 1,661,097 | 16.611 | 130 | 134 | fits | 49,468 | 152 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 1,678,145 | 16.781 | 130 | 134 | fits | 49,468 | 152 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 354,326 | 3.543 | 130 | 134 | fits | 119,705 | 63 | 0.085 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 486,558 | 4.866 | 20 | 200 | fits | 119,056 | 195 | 0.208 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 466,290 | 4.663 | 20 | 20 | fits | 119,056 | 195 | 0.208 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 327,030 | 3.270 | 20 | 24 | fits | 150,608 | 190 | 0.431 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 426,815 | 4.268 | 20 | 50 | fits | 119,056 | 195 | 0.208 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 913,364 | 9.134 | 20 | 20 | fits | 78,504 | 34 | 0.727 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 872,006 | 8.720 | 130 | 134 | fits | 25,616 | 52 | 0.474 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,522,036 | 15.220 | 130 | 134 | fits | 60,291 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,539,370 | 15.394 | 130 | 134 | fits | 60,291 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,556,448 | 15.564 | 130 | 134 | fits | 60,291 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 156,776 | 1.568 | 130 | 134 | fits | 61,041 | 153 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 174,930 | 1.749 | 130 | 134 | fits | 61,041 | 153 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 249,237 | 2.492 | 130 | 134 | fits | 57,980 | 111 | 0.267 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 267,038 | 2.670 | 130 | 134 | fits | 57,980 | 111 | 0.267 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,640,018 | 16.400 | 130 | 134 | fits | 32,090 | 101 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,652,046 | 16.520 | 130 | 134 | fits | 32,090 | 101 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 192,609 | 1.926 | 130 | 134 | fits | 61,041 | 153 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 431,168 | 4.312 | 130 | 134 | fits | 25,760 | 53 | 0.286 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 181,810 | 1.818 | 20 | 200 | fits | 151,311 | 274 | 0.241 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 447,535 | 4.475 | 20 | 20 | fits | 116,016 | 107 | 0.472 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 427,331 | 4.273 | 20 | 24 | fits | 116,016 | 107 | 0.472 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 122,067 | 1.221 | 20 | 50 | fits | 151,311 | 274 | 0.241 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 893,943 | 8.939 | 20 | 20 | fits | 78,381 | 34 | 0.725 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
