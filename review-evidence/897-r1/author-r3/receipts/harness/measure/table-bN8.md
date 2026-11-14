### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 92 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.acmp.if0` (notice-every-0) | 6.540 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-0.held.adp.if1` (notice-burst-0) | 6.728 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.aecp.if1` (notice-every-0) | 4.763 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 6.145 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.srp.if1` (notice-every-0) | 12.227 | fits | 31 srp | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.945 | fits | 0 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-0.mrpdu.periodic.if1` (notice-every-0) | 3.381 | fits | 0 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.36.0.if0` (notice-burst-0) | 50.718 (51.227) | fits | 0 events | 80 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1092 | 0 | 169,441 (1.694) | fits |
| notice-burst-0 | 955 | 0 | 164,291 (1.643) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 6.034 | 62 | 32 | 1 | within |
| notice-every-0 | 6.337 | 62 | 32 | 1 | within |
| notice-every-0 | 2.119 | 62 | 32 | 1 | within |
| notice-every-0 | 2.427 | 62 | 32 | 1 | within |
| notice-every-0 | 8.244 | 62 | 32 | 1 | within |
| notice-every-0 | 8.548 | 62 | 32 | 1 | within |
| notice-every-0 | 4.116 | 62 | 32 | 1 | within |
| notice-every-0 | 4.426 | 62 | 32 | 1 | within |
| notice-every-0 | 10.154 | 62 | 32 | 1 | within |
| notice-every-0 | 10.455 | 62 | 32 | 1 | within |
| notice-every-0 | 12.046 | 62 | 32 | 1 | within |
| notice-every-0 | 12.350 | 62 | 32 | 1 | within |
| notice-every-0 | 14.033 | 62 | 32 | 1 | within |
| notice-every-0 | 14.338 | 62 | 32 | 1 | within |
| notice-every-0 | 16.210 | 62 | 32 | 1 | within |
| notice-every-0 | 16.516 | 62 | 32 | 1 | within |
| notice-every-0 | 18.097 | 62 | 32 | 1 | within |
| notice-every-0 | 18.401 | 62 | 32 | 1 | within |
| notice-every-0 | 20.251 | 62 | 32 | 1 | within |
| notice-every-0 | 20.555 | 62 | 32 | 1 | within |
| notice-every-0 | 24.523 | 62 | 32 | 1 | within |
| notice-every-0 | 28.066 | 62 | 32 | 1 | within |
| notice-every-0 | 28.343 | 62 | 32 | 1 | within |
| notice-every-0 | 30.198 | 62 | 32 | 1 | within |
| notice-every-0 | 30.475 | 62 | 32 | 1 | within |
| notice-every-0 | 32.042 | 62 | 32 | 1 | within |
| notice-every-0 | 32.316 | 62 | 32 | 1 | within |
| notice-every-0 | 34.215 | 62 | 32 | 1 | within |
| notice-every-0 | 34.493 | 62 | 32 | 1 | within |
| notice-every-0 | 36.045 | 62 | 32 | 1 | within |
| notice-every-0 | 36.322 | 62 | 32 | 1 | within |
| notice-every-0 | 38.147 | 62 | 32 | 1 | within |
| notice-every-0 | 38.423 | 62 | 32 | 1 | within |
| notice-every-0 | 40.231 | 62 | 32 | 1 | within |
| notice-every-0 | 40.504 | 62 | 32 | 1 | within |
| notice-every-0 | 42.667 | 62 | 32 | 1 | within |
| notice-every-0 | 42.929 | 62 | 32 | 1 | within |
| notice-every-0 | 44.124 | 62 | 32 | 1 | within |
| notice-every-0 | 44.421 | 62 | 32 | 1 | within |
| notice-every-0 | 46.208 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.897 | 62 | 32 | 0 | within |
| notice-burst-0 | 3.191 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.256 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.558 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.146 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.444 | 62 | 32 | 0 | within |
| notice-burst-0 | 17.373 | 62 | 32 | 0 | within |
| notice-burst-0 | 20.739 | 62 | 32 | 0 | within |
| notice-burst-0 | 21.022 | 62 | 32 | 0 | within |
| notice-burst-0 | 22.731 | 62 | 32 | 0 | within |
| notice-burst-0 | 23.015 | 62 | 32 | 0 | within |
| notice-burst-0 | 24.630 | 62 | 32 | 0 | within |
| notice-burst-0 | 24.914 | 62 | 32 | 0 | within |
| notice-burst-0 | 26.517 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.182 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.510 | 62 | 32 | 0 | within |
| notice-burst-0 | 26.802 | 62 | 32 | 0 | within |
| notice-burst-0 | 28.687 | 62 | 32 | 0 | within |
| notice-burst-0 | 28.964 | 62 | 32 | 0 | within |
| notice-burst-0 | 30.552 | 62 | 32 | 0 | within |
| notice-burst-0 | 30.828 | 62 | 32 | 0 | within |
| notice-burst-0 | 32.748 | 62 | 32 | 0 | within |
| notice-burst-0 | 33.023 | 62 | 32 | 0 | within |
| notice-burst-0 | 34.596 | 62 | 32 | 0 | within |
| notice-burst-0 | 34.871 | 62 | 32 | 0 | within |
| notice-burst-0 | 36.721 | 62 | 32 | 0 | within |
| notice-burst-0 | 36.993 | 62 | 32 | 0 | within |
| notice-burst-0 | 38.550 | 62 | 32 | 0 | within |
| notice-burst-0 | 38.825 | 62 | 32 | 0 | within |
| notice-burst-0 | 40.657 | 62 | 32 | 0 | within |
| notice-burst-0 | 40.932 | 62 | 32 | 0 | within |
| notice-burst-0 | 42.566 | 62 | 32 | 0 | within |
| notice-burst-0 | 42.841 | 62 | 32 | 0 | within |
| notice-burst-0 | 44.650 | 62 | 32 | 0 | within |
| notice-burst-0 | 44.922 | 62 | 32 | 0 | within |
| notice-burst-0 | 46.724 | 62 | 32 | 0 | within |
| notice-burst-0 | 46.984 | 62 | 32 | 0 | within |
| notice-burst-0 | 48.451 | 62 | 32 | 0 | within |
| notice-burst-0 | 48.747 | 62 | 32 | 0 | within |
| notice-burst-0 | 50.718 | 62 | 32 | 0 | within |

Latest: 50.718 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 303 | 87,120 (0.871) | 48,228 (0.482) |
| notice-burst-0 | 313 | 116,533 (1.165) | 48,228 (0.482) |

Longest pass that carries a step: 116,533 CPU cycles (1.165 ms), notice-burst-0; longest step: 48,228 (0.482 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 603,378 | 6.034 | 62 | 66 | fits | 68,584 | 203 | 0.144 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 633,660 | 6.337 | 62 | 66 | fits | 68,584 | 203 | 0.144 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 211,917 | 2.119 | 62 | 66 | fits | 71,106 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 242,672 | 2.427 | 62 | 66 | fits | 71,106 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 824,426 | 8.244 | 62 | 66 | fits | 68,158 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 854,793 | 8.548 | 62 | 66 | fits | 68,158 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 411,583 | 4.116 | 62 | 66 | fits | 70,085 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 442,649 | 4.426 | 62 | 66 | fits | 70,085 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 1,015,376 | 10.154 | 62 | 66 | fits | 67,879 | 201 | 0.142 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 1,045,514 | 10.455 | 62 | 66 | fits | 67,879 | 201 | 0.142 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 1,204,591 | 12.046 | 62 | 66 | fits | 68,050 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 1,234,959 | 12.350 | 62 | 66 | fits | 68,050 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 1,403,347 | 14.033 | 62 | 66 | fits | 68,217 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 1,433,789 | 14.338 | 62 | 66 | fits | 68,217 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 1,620,972 | 16.210 | 62 | 66 | fits | 68,226 | 201 | 0.140 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 1,651,629 | 16.516 | 62 | 66 | fits | 68,226 | 201 | 0.140 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,809,735 | 18.097 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,840,093 | 18.401 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 2,025,073 | 20.251 | 62 | 66 | fits | 66,925 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 2,055,491 | 20.555 | 62 | 66 | fits | 66,925 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 2,452,273 | 24.523 | 62 | 66 | fits | 36,313 | 101 | 0.245 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 2,806,624 | 28.066 | 62 | 66 | fits | 66,484 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 2,834,273 | 28.343 | 62 | 66 | fits | 66,484 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 3,019,794 | 30.198 | 62 | 66 | fits | 66,198 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 3,047,530 | 30.475 | 62 | 66 | fits | 66,198 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 3,204,224 | 32.042 | 62 | 66 | fits | 65,648 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 3,231,561 | 32.316 | 62 | 66 | fits | 65,648 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 3,421,534 | 34.215 | 62 | 66 | fits | 67,000 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 3,449,330 | 34.493 | 62 | 66 | fits | 67,000 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 3,604,539 | 36.045 | 62 | 66 | fits | 65,962 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 3,632,236 | 36.322 | 62 | 66 | fits | 65,962 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 3,814,725 | 38.147 | 62 | 66 | fits | 65,458 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 3,842,312 | 38.423 | 62 | 66 | fits | 65,458 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 4,023,066 | 40.231 | 62 | 66 | fits | 64,865 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 4,050,403 | 40.504 | 62 | 66 | fits | 64,865 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 4,266,748 | 42.667 | 62 | 66 | fits | 65,158 | 200 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 4,292,852 | 42.929 | 62 | 66 | fits | 65,158 | 200 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 4,412,362 | 44.124 | 62 | 66 | fits | 62,383 | 200 | 0.108 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 4,442,086 | 44.421 | 62 | 66 | fits | 62,383 | 200 | 0.108 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 4,620,810 | 46.208 | 62 | 66 | fits | 37,463 | 102 | 0.159 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 449,133 | 4.491 | 20 | 200 | fits | 40,650 | 37 | 0.487 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 654,017 | 6.540 | 20 | 20 | fits | 134,990 | 127 | 0.619 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 476,251 | 4.763 | 20 | 24 | fits | 168,350 | 106 | 0.464 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 614,542 | 6.145 | 20 | 50 | fits | 134,990 | 127 | 0.619 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 1,222,688 | 12.227 | 20 | 20 | fits | 73,773 | 30 | 0.762 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 194,492 | 1.945 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 338,083 | 3.381 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 289,686 | 2.897 | 62 | 66 | fits | 66,215 | 203 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 319,079 | 3.191 | 62 | 66 | fits | 66,215 | 203 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 425,601 | 4.256 | 62 | 66 | fits | 116,533 | 210 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 455,754 | 4.558 | 62 | 66 | fits | 116,533 | 210 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 514,605 | 5.146 | 62 | 66 | fits | 66,628 | 203 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 544,360 | 5.444 | 62 | 66 | fits | 66,628 | 203 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 1,737,304 | 17.373 | 62 | 66 | fits | 40,930 | 100 | 0.336 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 2,073,895 | 20.739 | 62 | 66 | fits | 68,388 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 2,102,225 | 21.022 | 62 | 66 | fits | 68,388 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 2,273,141 | 22.731 | 62 | 66 | fits | 68,341 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 2,301,528 | 23.015 | 62 | 66 | fits | 68,341 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 2,462,982 | 24.630 | 62 | 66 | fits | 68,151 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 2,491,356 | 24.914 | 62 | 66 | fits | 68,151 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 2,651,700 | 26.517 | 62 | 66 | fits | 67,793 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 218,193 | 2.182 | 62 | 66 | fits | 102,949 | 210 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 251,046 | 2.510 | 62 | 66 | fits | 102,949 | 210 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 2,680,235 | 26.802 | 62 | 66 | fits | 67,793 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 2,868,688 | 28.687 | 62 | 66 | fits | 66,971 | 201 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 2,896,389 | 28.964 | 62 | 66 | fits | 66,971 | 201 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 3,055,235 | 30.552 | 62 | 66 | fits | 66,765 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 3,082,813 | 30.828 | 62 | 66 | fits | 66,765 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 3,274,756 | 32.748 | 62 | 66 | fits | 66,808 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 3,302,347 | 33.023 | 62 | 66 | fits | 66,808 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 3,459,611 | 34.596 | 62 | 66 | fits | 66,040 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 3,487,080 | 34.871 | 62 | 66 | fits | 66,040 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 3,672,136 | 36.721 | 62 | 66 | fits | 65,517 | 201 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 3,699,271 | 36.993 | 62 | 66 | fits | 65,517 | 201 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 3,854,962 | 38.550 | 62 | 66 | fits | 66,017 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 3,882,482 | 38.825 | 62 | 66 | fits | 66,017 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 4,065,671 | 40.657 | 62 | 66 | fits | 65,708 | 201 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 4,093,157 | 40.932 | 62 | 66 | fits | 65,708 | 201 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 4,256,615 | 42.566 | 62 | 66 | fits | 65,805 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 4,284,149 | 42.841 | 62 | 66 | fits | 65,805 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 4,465,042 | 44.650 | 62 | 66 | fits | 64,725 | 201 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 4,492,168 | 44.922 | 62 | 66 | fits | 64,725 | 201 | 0.128 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 4,672,357 | 46.724 | 62 | 66 | fits | 63,474 | 201 | 0.118 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 4,698,382 | 46.984 | 62 | 66 | fits | 63,474 | 201 | 0.118 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 4,845,100 | 48.451 | 62 | 66 | fits | 62,266 | 200 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 4,874,743 | 48.747 | 62 | 66 | fits | 62,266 | 200 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 5,071,820 | 50.718 | 62 | 66 | fits | 39,099 | 102 | 0.216 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 672,847 | 6.728 | 20 | 200 | fits | 152,367 | 83 | 0.581 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 652,579 | 6.526 | 20 | 20 | fits | 152,367 | 83 | 0.581 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 322,923 | 3.229 | 20 | 24 | fits | 161,755 | 113 | 0.462 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 460,737 | 4.607 | 20 | 50 | fits | 157,085 | 239 | 0.396 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 1,106,375 | 11.064 | 20 | 20 | fits | 121,035 | 43 | 0.582 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
