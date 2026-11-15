### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 5.802 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.adp.if0` (notice-burst-5) | 6.005 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.aecp.if0` (notice-burst-0) | 4.652 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.maap.if0` (notice-burst-5) | 5.407 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.srp.if0` (notice-burst-2) | 10.579 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 1.288 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.9.0.if0` (notice-burst-6) | 20.438 (20.655) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1575 | 0 | 156,563 (1.566) | fits |
| notice-every-1 | 1569 | 0 | 157,012 (1.570) | fits |
| notice-every-2 | 1571 | 0 | 156,866 (1.569) | fits |
| notice-every-3 | 1565 | 0 | 156,257 (1.563) | fits |
| notice-every-4 | 1568 | 0 | 156,536 (1.565) | fits |
| notice-every-5 | 1569 | 0 | 156,612 (1.566) | fits |
| notice-every-6 | 1564 | 0 | 156,645 (1.566) | fits |
| notice-every-7 | 1561 | 0 | 156,532 (1.565) | fits |
| notice-burst-0 | 1121 | 0 | 155,076 (1.551) | fits |
| notice-burst-1 | 1091 | 0 | 156,810 (1.568) | fits |
| notice-burst-2 | 1078 | 0 | 151,091 (1.511) | fits |
| notice-burst-3 | 1067 | 0 | 151,127 (1.511) | fits |
| notice-burst-4 | 1038 | 0 | 152,316 (1.523) | fits |
| notice-burst-5 | 1069 | 0 | 156,769 (1.568) | fits |
| notice-burst-6 | 1113 | 0 | 157,520 (1.575) | fits |
| notice-burst-7 | 1076 | 0 | 153,651 (1.537) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.028 | 130 | 16 | 2 | within |
| notice-every-0 | 8.237 | 130 | 16 | 2 | within |
| notice-every-0 | 1.862 | 130 | 16 | 2 | within |
| notice-every-0 | 2.075 | 130 | 16 | 2 | within |
| notice-every-0 | 6.068 | 130 | 16 | 2 | within |
| notice-every-0 | 6.278 | 130 | 16 | 2 | within |
| notice-every-0 | 3.869 | 130 | 16 | 2 | within |
| notice-every-0 | 4.082 | 130 | 16 | 2 | within |
| notice-every-0 | 8.422 | 130 | 16 | 2 | within |
| notice-every-0 | 9.925 | 130 | 16 | 2 | within |
| notice-every-0 | 2.286 | 130 | 16 | 2 | within |
| notice-every-0 | 4.295 | 130 | 16 | 2 | within |
| notice-every-1 | 6.367 | 130 | 16 | 2 | within |
| notice-every-1 | 6.578 | 130 | 16 | 2 | within |
| notice-every-1 | 8.138 | 130 | 16 | 2 | within |
| notice-every-1 | 8.347 | 130 | 16 | 2 | within |
| notice-every-1 | 2.151 | 130 | 16 | 2 | within |
| notice-every-1 | 2.365 | 130 | 16 | 2 | within |
| notice-every-1 | 4.141 | 130 | 16 | 2 | within |
| notice-every-1 | 4.355 | 130 | 16 | 2 | within |
| notice-every-1 | 6.765 | 130 | 16 | 2 | within |
| notice-every-1 | 8.527 | 130 | 16 | 2 | within |
| notice-every-1 | 2.576 | 130 | 16 | 2 | within |
| notice-every-1 | 4.568 | 130 | 16 | 2 | within |
| notice-every-2 | 1.804 | 130 | 16 | 2 | within |
| notice-every-2 | 2.015 | 130 | 16 | 2 | within |
| notice-every-2 | 3.786 | 130 | 16 | 2 | within |
| notice-every-2 | 3.996 | 130 | 16 | 2 | within |
| notice-every-2 | 5.779 | 130 | 16 | 2 | within |
| notice-every-2 | 5.986 | 130 | 16 | 2 | within |
| notice-every-2 | 7.772 | 130 | 16 | 2 | within |
| notice-every-2 | 7.978 | 130 | 16 | 2 | within |
| notice-every-2 | 2.205 | 130 | 16 | 2 | within |
| notice-every-2 | 4.183 | 130 | 16 | 2 | within |
| notice-every-2 | 6.192 | 130 | 16 | 2 | within |
| notice-every-2 | 8.181 | 130 | 16 | 2 | within |
| notice-every-3 | 6.368 | 130 | 16 | 2 | within |
| notice-every-3 | 6.578 | 130 | 16 | 2 | within |
| notice-every-3 | 8.139 | 130 | 16 | 2 | within |
| notice-every-3 | 8.347 | 130 | 16 | 2 | within |
| notice-every-3 | 2.151 | 130 | 16 | 2 | within |
| notice-every-3 | 2.365 | 130 | 16 | 2 | within |
| notice-every-3 | 4.142 | 130 | 16 | 2 | within |
| notice-every-3 | 4.356 | 130 | 16 | 2 | within |
| notice-every-3 | 6.766 | 130 | 16 | 2 | within |
| notice-every-3 | 8.528 | 130 | 16 | 2 | within |
| notice-every-3 | 2.577 | 130 | 16 | 2 | within |
| notice-every-3 | 4.568 | 130 | 16 | 2 | within |
| notice-every-4 | 8.352 | 130 | 16 | 2 | within |
| notice-every-4 | 8.562 | 130 | 16 | 2 | within |
| notice-every-4 | 4.203 | 130 | 16 | 2 | within |
| notice-every-4 | 4.415 | 130 | 16 | 2 | within |
| notice-every-4 | 6.207 | 130 | 16 | 2 | within |
| notice-every-4 | 6.417 | 130 | 16 | 2 | within |
| notice-every-4 | 2.202 | 130 | 16 | 2 | within |
| notice-every-4 | 2.419 | 130 | 16 | 2 | within |
| notice-every-4 | 8.747 | 130 | 16 | 2 | within |
| notice-every-4 | 10.079 | 130 | 16 | 2 | within |
| notice-every-4 | 2.629 | 130 | 16 | 2 | within |
| notice-every-4 | 4.629 | 130 | 16 | 2 | within |
| notice-every-5 | 6.021 | 130 | 16 | 2 | within |
| notice-every-5 | 6.232 | 130 | 16 | 2 | within |
| notice-every-5 | 7.792 | 130 | 16 | 2 | within |
| notice-every-5 | 8.000 | 130 | 16 | 2 | within |
| notice-every-5 | 1.804 | 130 | 16 | 2 | within |
| notice-every-5 | 2.017 | 130 | 16 | 2 | within |
| notice-every-5 | 3.808 | 130 | 16 | 2 | within |
| notice-every-5 | 4.022 | 130 | 16 | 2 | within |
| notice-every-5 | 6.419 | 130 | 16 | 2 | within |
| notice-every-5 | 8.181 | 130 | 16 | 2 | within |
| notice-every-5 | 2.229 | 130 | 16 | 2 | within |
| notice-every-5 | 4.234 | 130 | 16 | 2 | within |
| notice-every-6 | 8.348 | 130 | 16 | 2 | within |
| notice-every-6 | 8.557 | 130 | 16 | 2 | within |
| notice-every-6 | 2.206 | 130 | 16 | 2 | within |
| notice-every-6 | 2.420 | 130 | 16 | 2 | within |
| notice-every-6 | 6.202 | 130 | 16 | 2 | within |
| notice-every-6 | 6.411 | 130 | 16 | 2 | within |
| notice-every-6 | 4.198 | 130 | 16 | 2 | within |
| notice-every-6 | 4.411 | 130 | 16 | 2 | within |
| notice-every-6 | 8.743 | 130 | 16 | 2 | within |
| notice-every-6 | 10.075 | 130 | 16 | 2 | within |
| notice-every-6 | 2.631 | 130 | 16 | 2 | within |
| notice-every-6 | 4.624 | 130 | 16 | 2 | within |
| notice-every-7 | 8.028 | 130 | 16 | 2 | within |
| notice-every-7 | 8.238 | 130 | 16 | 2 | within |
| notice-every-7 | 1.863 | 130 | 16 | 2 | within |
| notice-every-7 | 2.075 | 130 | 16 | 2 | within |
| notice-every-7 | 6.069 | 130 | 16 | 2 | within |
| notice-every-7 | 6.278 | 130 | 16 | 2 | within |
| notice-every-7 | 3.870 | 130 | 16 | 2 | within |
| notice-every-7 | 4.083 | 130 | 16 | 2 | within |
| notice-every-7 | 8.423 | 130 | 16 | 2 | within |
| notice-every-7 | 9.925 | 130 | 16 | 2 | within |
| notice-every-7 | 2.287 | 130 | 16 | 2 | within |
| notice-every-7 | 4.295 | 130 | 16 | 2 | within |
| notice-burst-0 | 8.475 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.568 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.789 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.990 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.210 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.422 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.107 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.319 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.178 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.356 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.559 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.640 | 130 | 16 | 1 | within |
| notice-burst-1 | 9.446 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.298 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.597 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.811 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.006 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.461 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.281 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.489 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.488 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.662 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.187 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.347 | 130 | 16 | 1 | within |
| notice-burst-2 | 8.897 | 130 | 16 | 2 | within |
| notice-burst-2 | 14.795 | 130 | 16 | 2 | within |
| notice-burst-2 | 15.016 | 130 | 16 | 2 | within |
| notice-burst-2 | 15.217 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.235 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.448 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.643 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.914 | 130 | 16 | 2 | within |
| notice-burst-2 | 16.215 | 130 | 16 | 2 | within |
| notice-burst-2 | 16.391 | 130 | 16 | 2 | within |
| notice-burst-2 | 16.594 | 130 | 16 | 2 | within |
| notice-burst-2 | 5.661 | 130 | 16 | 2 | within |
| notice-burst-3 | 12.288 | 130 | 16 | 0 | within |
| notice-burst-3 | 12.500 | 130 | 16 | 0 | within |
| notice-burst-3 | 3.324 | 130 | 16 | 0 | within |
| notice-burst-3 | 12.705 | 130 | 16 | 0 | within |
| notice-burst-3 | 13.937 | 130 | 16 | 0 | within |
| notice-burst-3 | 14.143 | 130 | 16 | 0 | within |
| notice-burst-3 | 14.336 | 130 | 16 | 0 | within |
| notice-burst-3 | 15.900 | 130 | 16 | 0 | within |
| notice-burst-3 | 16.087 | 130 | 16 | 0 | within |
| notice-burst-3 | 16.259 | 130 | 16 | 0 | within |
| notice-burst-3 | 17.809 | 130 | 16 | 0 | within |
| notice-burst-3 | 18.016 | 130 | 16 | 0 | within |
| notice-burst-4 | 10.896 | 130 | 16 | 1 | within |
| notice-burst-4 | 11.108 | 130 | 16 | 1 | within |
| notice-burst-4 | 11.308 | 130 | 16 | 1 | within |
| notice-burst-4 | 12.373 | 130 | 16 | 1 | within |
| notice-burst-4 | 3.424 | 130 | 16 | 1 | within |
| notice-burst-4 | 12.582 | 130 | 16 | 1 | within |
| notice-burst-4 | 12.783 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.348 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.535 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.707 | 130 | 16 | 1 | within |
| notice-burst-4 | 16.257 | 130 | 16 | 1 | within |
| notice-burst-4 | 16.464 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.075 | 130 | 16 | 0 | within |
| notice-burst-5 | 6.286 | 130 | 16 | 0 | within |
| notice-burst-5 | 8.719 | 130 | 16 | 0 | within |
| notice-burst-5 | 17.542 | 130 | 16 | 0 | within |
| notice-burst-5 | 17.750 | 130 | 16 | 0 | within |
| notice-burst-5 | 17.951 | 130 | 16 | 0 | within |
| notice-burst-5 | 18.985 | 130 | 16 | 0 | within |
| notice-burst-5 | 19.192 | 130 | 16 | 0 | within |
| notice-burst-5 | 6.477 | 130 | 16 | 0 | within |
| notice-burst-5 | 6.725 | 130 | 16 | 0 | within |
| notice-burst-5 | 6.935 | 130 | 16 | 0 | within |
| notice-burst-5 | 19.396 | 130 | 16 | 0 | within |
| notice-burst-6 | 7.792 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.546 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.765 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.967 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.334 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.541 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.270 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.485 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.726 | 130 | 16 | 1 | within |
| notice-burst-6 | 20.231 | 130 | 16 | 1 | within |
| notice-burst-6 | 20.438 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.327 | 130 | 16 | 1 | within |
| notice-burst-7 | 9.175 | 130 | 16 | 0 | within |
| notice-burst-7 | 16.382 | 130 | 16 | 0 | within |
| notice-burst-7 | 16.602 | 130 | 16 | 0 | within |
| notice-burst-7 | 16.802 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.021 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.233 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.428 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.698 | 130 | 16 | 0 | within |
| notice-burst-7 | 17.976 | 130 | 16 | 0 | within |
| notice-burst-7 | 18.155 | 130 | 16 | 0 | within |
| notice-burst-7 | 18.358 | 130 | 16 | 0 | within |
| notice-burst-7 | 3.450 | 130 | 16 | 0 | within |

Latest: 20.438 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 98,092 (0.981) | 75,890 (0.759) |
| notice-every-1 | 307 | 101,125 (1.011) | 75,890 (0.759) |
| notice-every-2 | 307 | 101,702 (1.017) | 75,890 (0.759) |
| notice-every-3 | 307 | 105,903 (1.059) | 76,056 (0.761) |
| notice-every-4 | 307 | 91,125 (0.911) | 75,718 (0.757) |
| notice-every-5 | 307 | 91,125 (0.911) | 75,718 (0.757) |
| notice-every-6 | 307 | 91,125 (0.911) | 75,718 (0.757) |
| notice-every-7 | 307 | 91,125 (0.911) | 75,555 (0.756) |
| notice-burst-0 | 317 | 138,696 (1.387) | 77,815 (0.778) |
| notice-burst-1 | 317 | 101,125 (1.011) | 77,735 (0.777) |
| notice-burst-2 | 317 | 101,702 (1.017) | 77,815 (0.778) |
| notice-burst-3 | 317 | 105,903 (1.059) | 77,815 (0.778) |
| notice-burst-4 | 317 | 101,450 (1.014) | 77,815 (0.778) |
| notice-burst-5 | 317 | 101,103 (1.011) | 77,735 (0.777) |
| notice-burst-6 | 317 | 103,282 (1.033) | 77,735 (0.777) |
| notice-burst-7 | 317 | 118,344 (1.183) | 77,815 (0.778) |

Longest pass that carries a step: 138,696 CPU cycles (1.387 ms), notice-burst-0; longest step: 77,815 (0.778 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 802,789 | 8.028 | 130 | 134 | fits | 67,021 | 152 | 0.251 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 823,727 | 8.237 | 130 | 134 | fits | 67,021 | 152 | 0.251 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 186,233 | 1.862 | 130 | 134 | fits | 72,844 | 155 | 0.270 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 207,498 | 2.075 | 130 | 134 | fits | 72,844 | 155 | 0.270 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 606,822 | 6.068 | 130 | 134 | fits | 48,104 | 103 | 0.291 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 627,779 | 6.278 | 130 | 134 | fits | 48,104 | 103 | 0.291 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 386,911 | 3.869 | 130 | 134 | fits | 71,698 | 155 | 0.262 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 408,238 | 4.082 | 130 | 134 | fits | 71,698 | 155 | 0.262 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 842,239 | 8.422 | 130 | 134 | fits | 67,021 | 152 | 0.251 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 992,491 | 9.925 | 130 | 134 | fits | 23,661 | 51 | 0.346 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 228,623 | 2.286 | 130 | 134 | fits | 72,844 | 155 | 0.270 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 429,485 | 4.295 | 130 | 134 | fits | 71,698 | 155 | 0.262 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 159,339 | 1.593 | 20 | 200 | fits | 148,945 | 249 | 0.413 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 537,992 | 5.380 | 20 | 20 | fits | 95,506 | 39 | 0.749 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 422,282 | 4.223 | 20 | 24 | fits | 149,461 | 134 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 403,011 | 4.030 | 20 | 50 | fits | 149,461 | 134 | 0.490 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,012,913 | 10.129 | 20 | 20 | fits | 60,826 | 27 | 0.709 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 120,426 | 1.204 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 636,723 | 6.367 | 130 | 134 | fits | 67,899 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 657,781 | 6.578 | 130 | 134 | fits | 67,899 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 813,797 | 8.138 | 130 | 134 | fits | 65,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 834,651 | 8.347 | 130 | 134 | fits | 65,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 215,091 | 2.151 | 130 | 134 | fits | 72,391 | 155 | 0.270 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 236,463 | 2.365 | 130 | 134 | fits | 72,391 | 155 | 0.270 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 414,132 | 4.141 | 130 | 134 | fits | 73,053 | 160 | 0.253 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 435,524 | 4.355 | 130 | 134 | fits | 73,053 | 160 | 0.253 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 676,501 | 6.765 | 130 | 134 | fits | 67,899 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 852,740 | 8.527 | 130 | 134 | fits | 65,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 257,611 | 2.576 | 130 | 134 | fits | 72,391 | 155 | 0.270 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 456,771 | 4.568 | 130 | 134 | fits | 73,053 | 160 | 0.253 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 157,770 | 1.578 | 20 | 200 | fits | 151,123 | 254 | 0.402 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 454,706 | 4.547 | 20 | 20 | fits | 147,173 | 139 | 0.502 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 434,502 | 4.345 | 20 | 24 | fits | 147,173 | 139 | 0.502 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 415,231 | 4.152 | 20 | 50 | fits | 147,173 | 139 | 0.502 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,011,540 | 10.115 | 20 | 20 | fits | 60,801 | 27 | 0.709 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 128,752 | 1.288 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 180,442 | 1.804 | 130 | 134 | fits | 69,550 | 155 | 0.272 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 201,485 | 2.015 | 130 | 134 | fits | 69,550 | 155 | 0.272 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 378,637 | 3.786 | 130 | 134 | fits | 69,165 | 153 | 0.279 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 399,631 | 3.996 | 130 | 134 | fits | 69,165 | 153 | 0.279 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 577,910 | 5.779 | 130 | 134 | fits | 68,484 | 155 | 0.237 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 598,626 | 5.986 | 130 | 134 | fits | 68,484 | 155 | 0.237 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 777,151 | 7.772 | 130 | 134 | fits | 67,501 | 155 | 0.231 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 797,806 | 7.978 | 130 | 134 | fits | 67,501 | 155 | 0.231 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 220,542 | 2.205 | 130 | 134 | fits | 69,550 | 155 | 0.272 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 418,332 | 4.183 | 130 | 134 | fits | 69,165 | 153 | 0.279 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 619,247 | 6.192 | 130 | 134 | fits | 68,484 | 155 | 0.237 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 818,142 | 8.181 | 130 | 134 | fits | 67,501 | 155 | 0.231 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 168,501 | 1.685 | 20 | 200 | fits | 148,287 | 252 | 0.417 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 473,520 | 4.735 | 20 | 20 | fits | 145,630 | 133 | 0.506 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 453,316 | 4.533 | 20 | 24 | fits | 145,630 | 133 | 0.506 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 434,045 | 4.340 | 20 | 50 | fits | 145,630 | 133 | 0.506 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,035,688 | 10.357 | 20 | 20 | fits | 60,927 | 29 | 0.704 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 117,072 | 1.171 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 636,780 | 6.368 | 130 | 134 | fits | 67,899 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 657,838 | 6.578 | 130 | 134 | fits | 67,899 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 813,854 | 8.139 | 130 | 134 | fits | 65,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 834,708 | 8.347 | 130 | 134 | fits | 65,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 215,091 | 2.151 | 130 | 134 | fits | 72,448 | 155 | 0.272 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 236,520 | 2.365 | 130 | 134 | fits | 72,448 | 155 | 0.272 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 414,189 | 4.142 | 130 | 134 | fits | 73,053 | 160 | 0.253 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 435,581 | 4.356 | 130 | 134 | fits | 73,053 | 160 | 0.253 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 676,558 | 6.766 | 130 | 134 | fits | 67,899 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 852,797 | 8.528 | 130 | 134 | fits | 65,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 257,668 | 2.577 | 130 | 134 | fits | 72,448 | 155 | 0.272 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 456,828 | 4.568 | 130 | 134 | fits | 73,053 | 160 | 0.253 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 149,766 | 1.498 | 20 | 200 | fits | 148,139 | 240 | 0.411 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 546,088 | 5.461 | 20 | 20 | fits | 92,037 | 44 | 0.727 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 433,847 | 4.338 | 20 | 24 | fits | 150,017 | 152 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 414,576 | 4.146 | 20 | 50 | fits | 150,017 | 152 | 0.480 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,028,812 | 10.288 | 20 | 20 | fits | 72,241 | 31 | 0.669 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 127,867 | 1.279 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 835,245 | 8.352 | 130 | 134 | fits | 67,104 | 152 | 0.252 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 856,183 | 8.562 | 130 | 134 | fits | 67,104 | 152 | 0.252 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 420,289 | 4.203 | 130 | 134 | fits | 73,948 | 160 | 0.263 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 441,529 | 4.415 | 130 | 134 | fits | 73,948 | 160 | 0.263 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 620,693 | 6.207 | 130 | 134 | fits | 47,966 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 641,650 | 6.417 | 130 | 134 | fits | 47,966 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 220,190 | 2.202 | 130 | 134 | fits | 72,912 | 155 | 0.273 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 241,864 | 2.419 | 130 | 134 | fits | 72,912 | 155 | 0.273 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 874,695 | 8.747 | 130 | 134 | fits | 67,104 | 152 | 0.252 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 1,007,918 | 10.079 | 130 | 134 | fits | 23,763 | 51 | 0.350 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 262,947 | 2.629 | 130 | 134 | fits | 72,912 | 155 | 0.273 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 462,920 | 4.629 | 130 | 134 | fits | 73,948 | 160 | 0.263 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 161,018 | 1.610 | 20 | 200 | fits | 149,116 | 251 | 0.412 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 550,266 | 5.503 | 20 | 20 | fits | 84,752 | 36 | 0.776 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 445,310 | 4.453 | 20 | 24 | fits | 151,986 | 140 | 0.499 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 426,039 | 4.260 | 20 | 50 | fits | 151,986 | 140 | 0.499 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,028,572 | 10.286 | 20 | 20 | fits | 72,174 | 31 | 0.668 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 114,330 | 1.143 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 602,120 | 6.021 | 130 | 134 | fits | 67,874 | 153 | 0.253 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 623,178 | 6.232 | 130 | 134 | fits | 67,874 | 153 | 0.253 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 779,194 | 7.792 | 130 | 134 | fits | 65,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 800,048 | 8.000 | 130 | 134 | fits | 65,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 180,397 | 1.804 | 130 | 134 | fits | 71,775 | 155 | 0.257 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 201,743 | 2.017 | 130 | 134 | fits | 71,775 | 155 | 0.257 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 380,773 | 3.808 | 130 | 134 | fits | 71,813 | 155 | 0.262 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 402,165 | 4.022 | 130 | 134 | fits | 71,813 | 155 | 0.262 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 641,898 | 6.419 | 130 | 134 | fits | 67,874 | 153 | 0.253 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 818,137 | 8.181 | 130 | 134 | fits | 65,946 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 222,891 | 2.229 | 130 | 134 | fits | 71,775 | 155 | 0.257 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 423,412 | 4.234 | 130 | 134 | fits | 71,813 | 155 | 0.262 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 149,584 | 1.496 | 20 | 200 | fits | 149,915 | 244 | 0.409 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 549,003 | 5.490 | 20 | 20 | fits | 91,675 | 58 | 0.734 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 437,124 | 4.371 | 20 | 24 | fits | 152,632 | 139 | 0.504 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 509,528 | 5.095 | 20 | 50 | fits | 91,675 | 58 | 0.734 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,027,502 | 10.275 | 20 | 20 | fits | 72,174 | 31 | 0.668 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 113,146 | 1.131 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 834,807 | 8.348 | 130 | 134 | fits | 67,177 | 152 | 0.254 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 855,745 | 8.557 | 130 | 134 | fits | 67,177 | 152 | 0.254 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 220,572 | 2.206 | 130 | 134 | fits | 73,166 | 155 | 0.282 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 241,954 | 2.420 | 130 | 134 | fits | 73,166 | 155 | 0.282 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 620,182 | 6.202 | 130 | 134 | fits | 47,966 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 641,139 | 6.411 | 130 | 134 | fits | 47,966 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 419,788 | 4.198 | 130 | 134 | fits | 72,988 | 160 | 0.253 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 441,115 | 4.411 | 130 | 134 | fits | 72,988 | 160 | 0.253 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 874,257 | 8.743 | 130 | 134 | fits | 67,177 | 152 | 0.254 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 1,007,480 | 10.075 | 130 | 134 | fits | 23,763 | 51 | 0.350 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 263,102 | 2.631 | 130 | 134 | fits | 73,166 | 155 | 0.282 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 462,362 | 4.624 | 130 | 134 | fits | 72,988 | 160 | 0.253 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 151,158 | 1.512 | 20 | 200 | fits | 148,897 | 242 | 0.412 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 549,215 | 5.492 | 20 | 20 | fits | 91,613 | 58 | 0.732 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 437,398 | 4.374 | 20 | 24 | fits | 151,074 | 132 | 0.506 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 509,740 | 5.097 | 20 | 50 | fits | 91,613 | 58 | 0.732 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,027,718 | 10.277 | 20 | 20 | fits | 72,185 | 31 | 0.668 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 113,340 | 1.133 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 802,839 | 8.028 | 130 | 134 | fits | 67,021 | 152 | 0.251 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 823,777 | 8.238 | 130 | 134 | fits | 67,021 | 152 | 0.251 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 186,283 | 1.863 | 130 | 134 | fits | 72,844 | 155 | 0.270 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 207,548 | 2.075 | 130 | 134 | fits | 72,844 | 155 | 0.270 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 606,872 | 6.069 | 130 | 134 | fits | 48,104 | 103 | 0.291 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 627,829 | 6.278 | 130 | 134 | fits | 48,104 | 103 | 0.291 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 386,961 | 3.870 | 130 | 134 | fits | 71,698 | 155 | 0.262 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 408,288 | 4.083 | 130 | 134 | fits | 71,698 | 155 | 0.262 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 842,289 | 8.423 | 130 | 134 | fits | 67,021 | 152 | 0.251 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 992,541 | 9.925 | 130 | 134 | fits | 23,661 | 51 | 0.346 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 228,673 | 2.287 | 130 | 134 | fits | 72,844 | 155 | 0.270 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 429,535 | 4.295 | 130 | 134 | fits | 71,698 | 155 | 0.262 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 493,649 | 4.936 | 20 | 200 | fits | 146,477 | 237 | 0.432 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 559,144 | 5.591 | 20 | 20 | fits | 85,763 | 40 | 0.765 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 350,102 | 3.501 | 20 | 24 | fits | 99,155 | 69 | 0.495 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 433,906 | 4.339 | 20 | 50 | fits | 146,477 | 237 | 0.432 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,042,072 | 10.421 | 20 | 20 | fits | 72,168 | 31 | 0.668 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 125,969 | 1.260 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 847,526 | 8.475 | 130 | 134 | fits | 28,129 | 52 | 0.442 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,556,816 | 15.568 | 130 | 134 | fits | 71,972 | 153 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,578,859 | 15.789 | 130 | 134 | fits | 71,972 | 153 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,598,956 | 15.990 | 130 | 134 | fits | 71,972 | 153 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 220,968 | 2.210 | 130 | 134 | fits | 64,230 | 111 | 0.358 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 242,189 | 2.422 | 130 | 134 | fits | 64,230 | 111 | 0.358 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 310,685 | 3.107 | 130 | 134 | fits | 138,696 | 112 | 0.273 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 331,938 | 3.319 | 130 | 134 | fits | 138,696 | 112 | 0.273 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,717,755 | 17.178 | 130 | 134 | fits | 62,424 | 152 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,735,593 | 17.356 | 130 | 134 | fits | 62,424 | 152 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,755,872 | 17.559 | 130 | 134 | fits | 62,424 | 152 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 664,010 | 6.640 | 130 | 134 | fits | 29,415 | 52 | 0.429 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 148,851 | 1.489 | 20 | 200 | fits | 148,348 | 241 | 0.414 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 485,397 | 4.854 | 20 | 20 | fits | 144,194 | 155 | 0.494 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 465,193 | 4.652 | 20 | 24 | fits | 144,194 | 155 | 0.494 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 445,922 | 4.459 | 20 | 50 | fits | 144,194 | 155 | 0.494 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 959,242 | 9.592 | 20 | 20 | fits | 82,041 | 34 | 0.628 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 944,584 | 9.446 | 130 | 134 | fits | 29,693 | 52 | 0.491 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,529,791 | 15.298 | 130 | 134 | fits | 65,218 | 152 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 259,715 | 2.597 | 130 | 134 | fits | 70,535 | 152 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 281,131 | 2.811 | 130 | 134 | fits | 70,535 | 152 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 300,556 | 3.006 | 130 | 134 | fits | 70,535 | 152 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 346,104 | 3.461 | 130 | 134 | fits | 46,860 | 68 | 0.473 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 428,100 | 4.281 | 130 | 134 | fits | 62,199 | 111 | 0.333 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 448,932 | 4.489 | 130 | 134 | fits | 62,199 | 111 | 0.333 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,548,840 | 15.488 | 130 | 134 | fits | 65,218 | 152 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,566,155 | 15.662 | 130 | 134 | fits | 65,218 | 152 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,718,709 | 17.187 | 130 | 134 | fits | 26,650 | 52 | 0.342 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 634,727 | 6.347 | 130 | 134 | fits | 27,695 | 53 | 0.366 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 523,542 | 5.235 | 20 | 200 | fits | 132,626 | 219 | 0.415 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 503,274 | 5.033 | 20 | 20 | fits | 132,626 | 219 | 0.415 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 350,444 | 3.504 | 20 | 24 | fits | 147,674 | 158 | 0.477 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 463,799 | 4.638 | 20 | 50 | fits | 132,626 | 219 | 0.415 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,009,066 | 10.091 | 20 | 20 | fits | 92,869 | 38 | 0.595 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 889,695 | 8.897 | 130 | 134 | fits | 29,817 | 51 | 0.498 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,479,546 | 14.795 | 130 | 134 | fits | 71,415 | 153 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,501,604 | 15.016 | 130 | 134 | fits | 71,415 | 153 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,521,701 | 15.217 | 130 | 134 | fits | 71,415 | 153 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 323,515 | 3.235 | 130 | 134 | fits | 83,099 | 161 | 0.288 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 344,793 | 3.448 | 130 | 134 | fits | 83,099 | 161 | 0.288 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 364,339 | 3.643 | 130 | 134 | fits | 83,099 | 161 | 0.288 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 391,375 | 3.914 | 130 | 134 | fits | 26,951 | 53 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,621,480 | 16.215 | 130 | 134 | fits | 62,177 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,639,138 | 16.391 | 130 | 134 | fits | 62,177 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,659,417 | 16.594 | 130 | 134 | fits | 62,177 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 566,099 | 5.661 | 130 | 134 | fits | 28,031 | 52 | 0.365 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 567,871 | 5.679 | 20 | 200 | fits | 142,811 | 231 | 0.411 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 547,603 | 5.476 | 20 | 20 | fits | 142,811 | 231 | 0.411 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 384,588 | 3.846 | 20 | 24 | fits | 150,985 | 157 | 0.473 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 508,128 | 5.081 | 20 | 50 | fits | 142,811 | 231 | 0.411 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,057,858 | 10.579 | 20 | 20 | fits | 92,980 | 38 | 0.595 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,228,829 | 12.288 | 130 | 134 | fits | 72,960 | 153 | 0.319 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,250,020 | 12.500 | 130 | 134 | fits | 72,960 | 153 | 0.319 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 332,432 | 3.324 | 130 | 134 | fits | 30,258 | 52 | 0.498 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,270,515 | 12.705 | 130 | 134 | fits | 72,960 | 153 | 0.319 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,393,687 | 13.937 | 130 | 134 | fits | 66,756 | 152 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,414,349 | 14.143 | 130 | 134 | fits | 66,756 | 152 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 1,433,563 | 14.336 | 130 | 134 | fits | 66,756 | 152 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,589,972 | 15.900 | 130 | 134 | fits | 62,969 | 152 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,608,692 | 16.087 | 130 | 134 | fits | 62,969 | 152 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,625,935 | 16.259 | 130 | 134 | fits | 62,969 | 152 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,780,912 | 17.809 | 130 | 134 | fits | 47,199 | 103 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 1,801,571 | 18.016 | 130 | 134 | fits | 47,199 | 103 | 0.246 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 149,866 | 1.499 | 20 | 200 | fits | 150,008 | 245 | 0.410 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 547,425 | 5.474 | 20 | 20 | fits | 94,322 | 37 | 0.747 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 432,899 | 4.329 | 20 | 24 | fits | 146,677 | 141 | 0.479 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 413,628 | 4.136 | 20 | 50 | fits | 146,677 | 141 | 0.479 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 963,256 | 9.633 | 20 | 20 | fits | 37,112 | 18 | 0.816 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,089,634 | 10.896 | 130 | 134 | fits | 72,526 | 152 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,110,825 | 11.108 | 130 | 134 | fits | 72,526 | 152 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,130,842 | 11.308 | 130 | 134 | fits | 72,526 | 152 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,237,293 | 12.373 | 130 | 134 | fits | 68,396 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 342,374 | 3.424 | 130 | 134 | fits | 28,467 | 52 | 0.457 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,258,214 | 12.582 | 130 | 134 | fits | 68,396 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,278,270 | 12.783 | 130 | 134 | fits | 68,396 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,434,782 | 14.348 | 130 | 134 | fits | 62,898 | 152 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,453,502 | 14.535 | 130 | 134 | fits | 62,898 | 152 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,470,674 | 14.707 | 130 | 134 | fits | 62,898 | 152 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,625,707 | 16.257 | 130 | 134 | fits | 47,199 | 103 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,646,366 | 16.464 | 130 | 134 | fits | 47,199 | 103 | 0.246 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 174,687 | 1.747 | 20 | 200 | fits | 150,230 | 260 | 0.416 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 480,661 | 4.807 | 20 | 20 | fits | 152,316 | 138 | 0.493 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 460,457 | 4.605 | 20 | 24 | fits | 152,316 | 138 | 0.493 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 441,186 | 4.412 | 20 | 50 | fits | 152,316 | 138 | 0.493 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 982,825 | 9.828 | 20 | 20 | fits | 37,099 | 18 | 0.816 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 607,538 | 6.075 | 130 | 134 | fits | 83,784 | 161 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 628,568 | 6.286 | 130 | 134 | fits | 83,784 | 161 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 871,853 | 8.719 | 130 | 134 | fits | 27,865 | 52 | 0.429 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,754,211 | 17.542 | 130 | 134 | fits | 70,564 | 153 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,774,966 | 17.750 | 130 | 134 | fits | 70,564 | 153 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,795,056 | 17.951 | 130 | 134 | fits | 70,564 | 153 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,898,511 | 18.985 | 130 | 134 | fits | 67,430 | 153 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,919,165 | 19.192 | 130 | 134 | fits | 67,430 | 153 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 647,671 | 6.477 | 130 | 134 | fits | 83,784 | 161 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 672,514 | 6.725 | 130 | 134 | fits | 45,362 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 693,509 | 6.935 | 130 | 134 | fits | 45,362 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 1,939,582 | 19.396 | 130 | 134 | fits | 67,430 | 153 | 0.230 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 600,486 | 6.005 | 20 | 200 | fits | 142,499 | 229 | 0.410 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 580,218 | 5.802 | 20 | 20 | fits | 142,499 | 229 | 0.410 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 417,515 | 4.175 | 20 | 24 | fits | 156,769 | 165 | 0.486 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 540,743 | 5.407 | 20 | 50 | fits | 142,499 | 229 | 0.410 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,053,374 | 10.534 | 20 | 20 | fits | 93,250 | 38 | 0.595 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 779,224 | 7.792 | 130 | 134 | fits | 29,242 | 52 | 0.487 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,654,590 | 16.546 | 130 | 134 | fits | 71,502 | 153 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,676,518 | 16.765 | 130 | 134 | fits | 71,502 | 153 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,696,687 | 16.967 | 130 | 134 | fits | 71,502 | 153 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,833,414 | 18.334 | 130 | 134 | fits | 65,537 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,854,068 | 18.541 | 130 | 134 | fits | 65,537 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 227,037 | 2.270 | 130 | 134 | fits | 64,589 | 111 | 0.356 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 248,489 | 2.485 | 130 | 134 | fits | 64,589 | 111 | 0.356 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 1,872,557 | 18.726 | 130 | 134 | fits | 65,537 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,023,072 | 20.231 | 130 | 134 | fits | 44,358 | 102 | 0.251 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,043,770 | 20.438 | 130 | 134 | fits | 44,358 | 102 | 0.251 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 332,669 | 3.327 | 130 | 134 | fits | 43,293 | 62 | 0.416 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 156,404 | 1.564 | 20 | 200 | fits | 150,229 | 255 | 0.411 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 459,304 | 4.593 | 20 | 20 | fits | 136,406 | 129 | 0.494 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 439,100 | 4.391 | 20 | 24 | fits | 136,406 | 129 | 0.494 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 419,829 | 4.198 | 20 | 50 | fits | 136,406 | 129 | 0.494 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 931,262 | 9.313 | 20 | 20 | fits | 93,027 | 38 | 0.595 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 917,499 | 9.175 | 130 | 134 | fits | 28,757 | 52 | 0.469 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,638,218 | 16.382 | 130 | 134 | fits | 71,595 | 153 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,660,153 | 16.602 | 130 | 134 | fits | 71,595 | 153 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,680,250 | 16.802 | 130 | 134 | fits | 71,595 | 153 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 202,103 | 2.021 | 130 | 134 | fits | 82,939 | 161 | 0.286 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 223,312 | 2.233 | 130 | 134 | fits | 82,939 | 161 | 0.286 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 242,779 | 2.428 | 130 | 134 | fits | 82,939 | 161 | 0.286 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 269,842 | 2.698 | 130 | 134 | fits | 26,978 | 53 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,797,645 | 17.976 | 130 | 134 | fits | 62,424 | 152 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,815,483 | 18.155 | 130 | 134 | fits | 62,424 | 152 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,835,762 | 18.358 | 130 | 134 | fits | 62,424 | 152 | 0.211 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 345,013 | 3.450 | 130 | 134 | fits | 118,344 | 60 | 0.299 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 162,269 | 1.623 | 20 | 200 | fits | 149,060 | 249 | 0.418 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 463,760 | 4.638 | 20 | 20 | fits | 139,351 | 138 | 0.505 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 443,556 | 4.436 | 20 | 24 | fits | 139,351 | 138 | 0.505 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 424,285 | 4.243 | 20 | 50 | fits | 139,351 | 138 | 0.505 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 935,628 | 9.356 | 20 | 20 | fits | 92,918 | 38 | 0.595 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
