### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 140 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.acmp.if0` (notice-burst-4) | 4.558 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.adp.if0` (notice-burst-4) | 4.761 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-4.held.aecp.if0` (notice-every-4) | 4.256 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.maap.if0` (notice-burst-4) | 4.163 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-4.held.srp.if0` (notice-every-4) | 11.398 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-4.mrpdu.periodic.if0` (notice-every-4) | 0.971 | fits | 0 srp | 4 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.36.0.if0` (notice-burst-6) | 27.279 (27.498) | fits | 1 events | 96 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1533 | 0 | 157,778 (1.578) | fits |
| notice-every-2 | 1530 | 0 | 156,595 (1.566) | fits |
| notice-every-4 | 1530 | 0 | 154,560 (1.546) | fits |
| notice-every-6 | 1523 | 0 | 154,835 (1.548) | fits |
| notice-burst-0 | 1072 | 0 | 152,285 (1.523) | fits |
| notice-burst-2 | 1089 | 0 | 157,183 (1.572) | fits |
| notice-burst-4 | 1052 | 0 | 156,263 (1.563) | fits |
| notice-burst-6 | 1049 | 0 | 151,480 (1.515) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 2.294 | 140 | 16 | 2 | within |
| notice-every-0 | 2.495 | 140 | 16 | 2 | within |
| notice-every-0 | 5.183 | 140 | 16 | 2 | within |
| notice-every-0 | 5.387 | 140 | 16 | 2 | within |
| notice-every-0 | 6.278 | 140 | 16 | 2 | within |
| notice-every-0 | 6.477 | 140 | 16 | 2 | within |
| notice-every-0 | 8.275 | 140 | 16 | 2 | within |
| notice-every-0 | 8.473 | 140 | 16 | 2 | within |
| notice-every-0 | 10.238 | 140 | 16 | 2 | within |
| notice-every-0 | 10.410 | 140 | 16 | 2 | within |
| notice-every-0 | 12.168 | 140 | 16 | 2 | within |
| notice-every-0 | 12.367 | 140 | 16 | 2 | within |
| notice-every-2 | 1.837 | 140 | 16 | 2 | within |
| notice-every-2 | 2.037 | 140 | 16 | 2 | within |
| notice-every-2 | 3.968 | 140 | 16 | 2 | within |
| notice-every-2 | 4.173 | 140 | 16 | 2 | within |
| notice-every-2 | 5.823 | 140 | 16 | 2 | within |
| notice-every-2 | 6.022 | 140 | 16 | 2 | within |
| notice-every-2 | 7.823 | 140 | 16 | 2 | within |
| notice-every-2 | 8.020 | 140 | 16 | 2 | within |
| notice-every-2 | 9.790 | 140 | 16 | 2 | within |
| notice-every-2 | 9.962 | 140 | 16 | 2 | within |
| notice-every-2 | 11.901 | 140 | 16 | 2 | within |
| notice-every-2 | 12.100 | 140 | 16 | 2 | within |
| notice-every-4 | 6.330 | 140 | 16 | 2 | within |
| notice-every-4 | 6.532 | 140 | 16 | 2 | within |
| notice-every-4 | 8.149 | 140 | 16 | 2 | within |
| notice-every-4 | 8.352 | 140 | 16 | 2 | within |
| notice-every-4 | 2.109 | 140 | 16 | 2 | within |
| notice-every-4 | 2.315 | 140 | 16 | 2 | within |
| notice-every-4 | 4.146 | 140 | 16 | 2 | within |
| notice-every-4 | 4.348 | 140 | 16 | 2 | within |
| notice-every-4 | 10.126 | 140 | 16 | 2 | within |
| notice-every-4 | 10.298 | 140 | 16 | 2 | within |
| notice-every-4 | 12.239 | 140 | 16 | 2 | within |
| notice-every-4 | 12.437 | 140 | 16 | 2 | within |
| notice-every-6 | 5.863 | 140 | 16 | 2 | within |
| notice-every-6 | 6.062 | 140 | 16 | 2 | within |
| notice-every-6 | 7.881 | 140 | 16 | 2 | within |
| notice-every-6 | 8.083 | 140 | 16 | 2 | within |
| notice-every-6 | 1.839 | 140 | 16 | 2 | within |
| notice-every-6 | 2.044 | 140 | 16 | 2 | within |
| notice-every-6 | 4.030 | 140 | 16 | 2 | within |
| notice-every-6 | 4.234 | 140 | 16 | 2 | within |
| notice-every-6 | 9.856 | 140 | 16 | 2 | within |
| notice-every-6 | 10.028 | 140 | 16 | 2 | within |
| notice-every-6 | 11.968 | 140 | 16 | 2 | within |
| notice-every-6 | 12.167 | 140 | 16 | 2 | within |
| notice-burst-0 | 8.318 | 140 | 16 | 1 | within |
| notice-burst-0 | 16.427 | 140 | 16 | 1 | within |
| notice-burst-0 | 16.646 | 140 | 16 | 1 | within |
| notice-burst-0 | 18.231 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.221 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.425 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.670 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.872 | 140 | 16 | 1 | within |
| notice-burst-0 | 18.416 | 140 | 16 | 1 | within |
| notice-burst-0 | 20.131 | 140 | 16 | 1 | within |
| notice-burst-0 | 20.328 | 140 | 16 | 1 | within |
| notice-burst-0 | 4.589 | 140 | 16 | 1 | within |
| notice-burst-2 | 14.503 | 140 | 16 | 1 | within |
| notice-burst-2 | 14.707 | 140 | 16 | 1 | within |
| notice-burst-2 | 16.147 | 140 | 16 | 1 | within |
| notice-burst-2 | 16.350 | 140 | 16 | 1 | within |
| notice-burst-2 | 2.680 | 140 | 16 | 1 | within |
| notice-burst-2 | 2.885 | 140 | 16 | 1 | within |
| notice-burst-2 | 4.655 | 140 | 16 | 1 | within |
| notice-burst-2 | 18.128 | 140 | 16 | 1 | within |
| notice-burst-2 | 18.311 | 140 | 16 | 1 | within |
| notice-burst-2 | 20.232 | 140 | 16 | 1 | within |
| notice-burst-2 | 20.427 | 140 | 16 | 1 | within |
| notice-burst-2 | 22.235 | 140 | 16 | 1 | within |
| notice-burst-4 | 5.640 | 140 | 16 | 1 | within |
| notice-burst-4 | 5.839 | 140 | 16 | 1 | within |
| notice-burst-4 | 17.661 | 140 | 16 | 1 | within |
| notice-burst-4 | 17.869 | 140 | 16 | 1 | within |
| notice-burst-4 | 19.295 | 140 | 16 | 1 | within |
| notice-burst-4 | 19.492 | 140 | 16 | 1 | within |
| notice-burst-4 | 21.268 | 140 | 16 | 1 | within |
| notice-burst-4 | 21.466 | 140 | 16 | 1 | within |
| notice-burst-4 | 6.284 | 140 | 16 | 1 | within |
| notice-burst-4 | 6.461 | 140 | 16 | 1 | within |
| notice-burst-4 | 23.228 | 140 | 16 | 1 | within |
| notice-burst-4 | 23.427 | 140 | 16 | 1 | within |
| notice-burst-6 | 7.743 | 140 | 16 | 1 | within |
| notice-burst-6 | 17.544 | 140 | 16 | 1 | within |
| notice-burst-6 | 17.762 | 140 | 16 | 1 | within |
| notice-burst-6 | 19.201 | 140 | 16 | 1 | within |
| notice-burst-6 | 19.404 | 140 | 16 | 1 | within |
| notice-burst-6 | 21.188 | 140 | 16 | 1 | within |
| notice-burst-6 | 21.388 | 140 | 16 | 1 | within |
| notice-burst-6 | 23.345 | 140 | 16 | 1 | within |
| notice-burst-6 | 23.528 | 140 | 16 | 1 | within |
| notice-burst-6 | 25.320 | 140 | 16 | 1 | within |
| notice-burst-6 | 25.517 | 140 | 16 | 1 | within |
| notice-burst-6 | 27.279 | 140 | 16 | 1 | within |

Latest: 27.279 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 125,067 (1.251) | 76,244 (0.762) |
| notice-every-2 | 307 | 101,311 (1.013) | 76,244 (0.762) |
| notice-every-4 | 307 | 110,660 (1.107) | 76,308 (0.763) |
| notice-every-6 | 307 | 91,589 (0.916) | 75,718 (0.757) |
| notice-burst-0 | 317 | 101,221 (1.012) | 77,969 (0.780) |
| notice-burst-2 | 317 | 101,311 (1.013) | 77,969 (0.780) |
| notice-burst-4 | 317 | 110,660 (1.107) | 78,048 (0.780) |
| notice-burst-6 | 317 | 101,309 (1.013) | 78,048 (0.780) |

Longest pass that carries a step: 125,067 CPU cycles (1.251 ms), notice-every-0; longest step: 78,048 (0.780 ms), notice-burst-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 229,425 | 2.294 | 140 | 144 | fits | 49,004 | 103 | 0.306 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 249,523 | 2.495 | 140 | 144 | fits | 49,004 | 103 | 0.306 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 518,277 | 5.183 | 140 | 144 | fits | 125,067 | 102 | 0.245 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 538,745 | 5.387 | 140 | 144 | fits | 125,067 | 102 | 0.245 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 627,781 | 6.278 | 140 | 144 | fits | 46,301 | 103 | 0.257 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 647,682 | 6.477 | 140 | 144 | fits | 46,301 | 103 | 0.257 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 827,535 | 8.275 | 140 | 144 | fits | 45,809 | 102 | 0.253 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 847,285 | 8.473 | 140 | 144 | fits | 45,809 | 102 | 0.253 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 1,023,781 | 10.238 | 140 | 144 | fits | 41,045 | 101 | 0.226 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 1,041,009 | 10.410 | 140 | 144 | fits | 41,045 | 101 | 0.226 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 1,216,812 | 12.168 | 140 | 144 | fits | 44,622 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 1,236,688 | 12.367 | 140 | 144 | fits | 44,622 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 163,234 | 1.632 | 20 | 200 | fits | 148,596 | 287 | 0.311 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 423,945 | 4.239 | 20 | 20 | fits | 113,868 | 79 | 0.524 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 403,741 | 4.037 | 20 | 24 | fits | 113,868 | 79 | 0.524 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 103,491 | 1.035 | 20 | 50 | fits | 148,596 | 287 | 0.311 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,119,815 | 11.198 | 20 | 20 | fits | 43,686 | 25 | 0.831 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 96,550 | 0.966 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 183,691 | 1.837 | 140 | 144 | fits | 48,784 | 105 | 0.292 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 203,659 | 2.037 | 140 | 144 | fits | 48,784 | 105 | 0.292 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 396,809 | 3.968 | 140 | 144 | fits | 50,766 | 109 | 0.299 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 417,277 | 4.173 | 140 | 144 | fits | 50,766 | 109 | 0.299 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 582,323 | 5.823 | 140 | 144 | fits | 46,514 | 105 | 0.258 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 602,224 | 6.022 | 140 | 144 | fits | 46,514 | 105 | 0.258 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 782,288 | 7.823 | 140 | 144 | fits | 45,947 | 104 | 0.254 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 802,038 | 8.020 | 140 | 144 | fits | 45,947 | 104 | 0.254 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 978,950 | 9.790 | 140 | 144 | fits | 41,181 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 996,178 | 9.962 | 140 | 144 | fits | 41,181 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 1,190,083 | 11.901 | 140 | 144 | fits | 44,622 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 1,209,959 | 12.100 | 140 | 144 | fits | 44,622 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 167,660 | 1.677 | 20 | 200 | fits | 151,857 | 293 | 0.311 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 443,665 | 4.437 | 20 | 20 | fits | 116,867 | 92 | 0.515 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 423,461 | 4.235 | 20 | 24 | fits | 116,867 | 92 | 0.515 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 107,917 | 1.079 | 20 | 50 | fits | 151,857 | 293 | 0.311 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,136,353 | 11.364 | 20 | 20 | fits | 45,451 | 31 | 0.812 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 88,992 | 0.890 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 633,003 | 6.330 | 140 | 144 | fits | 48,504 | 103 | 0.300 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 653,185 | 6.532 | 140 | 144 | fits | 48,504 | 103 | 0.300 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 814,945 | 8.149 | 140 | 144 | fits | 48,069 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 835,205 | 8.352 | 140 | 144 | fits | 48,069 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 210,921 | 2.109 | 140 | 144 | fits | 49,242 | 105 | 0.294 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 231,481 | 2.315 | 140 | 144 | fits | 49,242 | 105 | 0.294 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 414,552 | 4.146 | 140 | 144 | fits | 47,663 | 104 | 0.261 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 434,764 | 4.348 | 140 | 144 | fits | 47,663 | 104 | 0.261 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 1,012,573 | 10.126 | 140 | 144 | fits | 41,102 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 1,029,801 | 10.298 | 140 | 144 | fits | 41,102 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 1,223,854 | 12.239 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 1,243,730 | 12.437 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 162,768 | 1.628 | 20 | 200 | fits | 150,882 | 293 | 0.317 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 445,811 | 4.458 | 20 | 20 | fits | 130,440 | 103 | 0.505 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 425,607 | 4.256 | 20 | 24 | fits | 130,440 | 103 | 0.505 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 103,025 | 1.030 | 20 | 50 | fits | 150,882 | 293 | 0.317 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,139,769 | 11.398 | 20 | 20 | fits | 45,450 | 31 | 0.813 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 97,103 | 0.971 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 586,255 | 5.863 | 140 | 144 | fits | 47,872 | 105 | 0.279 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 606,238 | 6.062 | 140 | 144 | fits | 47,872 | 105 | 0.279 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 788,071 | 7.881 | 140 | 144 | fits | 48,166 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 808,331 | 8.083 | 140 | 144 | fits | 48,166 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 183,937 | 1.839 | 140 | 144 | fits | 49,015 | 105 | 0.281 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 204,367 | 2.044 | 140 | 144 | fits | 49,015 | 105 | 0.281 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 403,028 | 4.030 | 140 | 144 | fits | 48,305 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 423,439 | 4.234 | 140 | 144 | fits | 48,305 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 985,585 | 9.856 | 140 | 144 | fits | 41,102 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 1,002,813 | 10.028 | 140 | 144 | fits | 41,102 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 1,196,843 | 11.968 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 1,216,719 | 12.167 | 140 | 144 | fits | 44,747 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 126,420 | 1.264 | 20 | 200 | fits | 121,481 | 157 | 0.286 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 439,201 | 4.392 | 20 | 20 | fits | 142,237 | 144 | 0.490 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 418,997 | 4.190 | 20 | 24 | fits | 142,237 | 144 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 399,726 | 3.997 | 20 | 50 | fits | 142,237 | 144 | 0.490 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,131,425 | 11.314 | 20 | 20 | fits | 46,021 | 31 | 0.819 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 85,526 | 0.855 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 831,769 | 8.318 | 140 | 144 | fits | 28,098 | 52 | 0.474 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,642,747 | 16.427 | 140 | 144 | fits | 50,416 | 103 | 0.363 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,664,583 | 16.646 | 140 | 144 | fits | 50,416 | 103 | 0.363 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,823,064 | 18.231 | 140 | 144 | fits | 44,174 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 222,118 | 2.221 | 140 | 144 | fits | 63,379 | 111 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 242,457 | 2.425 | 140 | 144 | fits | 63,379 | 111 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 267,034 | 2.670 | 140 | 144 | fits | 44,480 | 103 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 287,185 | 2.872 | 140 | 144 | fits | 44,480 | 103 | 0.129 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,841,616 | 18.416 | 140 | 144 | fits | 44,174 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,013,057 | 20.131 | 140 | 144 | fits | 42,603 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,032,766 | 20.328 | 140 | 144 | fits | 42,603 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 458,901 | 4.589 | 140 | 144 | fits | 27,940 | 52 | 0.323 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 161,703 | 1.617 | 20 | 200 | fits | 151,286 | 290 | 0.312 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 438,676 | 4.387 | 20 | 20 | fits | 116,858 | 96 | 0.530 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 418,472 | 4.185 | 20 | 24 | fits | 116,858 | 96 | 0.530 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 101,960 | 1.020 | 20 | 50 | fits | 151,286 | 290 | 0.312 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 1,024,152 | 10.242 | 20 | 20 | fits | 78,766 | 30 | 0.682 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 1,450,308 | 14.503 | 140 | 144 | fits | 50,908 | 103 | 0.374 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,470,740 | 14.707 | 140 | 144 | fits | 50,908 | 103 | 0.374 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,614,725 | 16.147 | 140 | 144 | fits | 48,097 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,634,962 | 16.350 | 140 | 144 | fits | 48,097 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 268,034 | 2.680 | 140 | 144 | fits | 49,245 | 102 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 288,511 | 2.885 | 140 | 144 | fits | 49,245 | 102 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 465,465 | 4.655 | 140 | 144 | fits | 27,787 | 52 | 0.450 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 1,812,777 | 18.128 | 140 | 144 | fits | 43,833 | 103 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,831,055 | 18.311 | 140 | 144 | fits | 43,833 | 103 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,023,150 | 20.232 | 140 | 144 | fits | 42,941 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,042,685 | 20.427 | 140 | 144 | fits | 42,941 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 2,223,540 | 22.235 | 140 | 144 | fits | 25,620 | 52 | 0.309 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 149,702 | 1.497 | 20 | 200 | fits | 148,181 | 275 | 0.341 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 440,991 | 4.410 | 20 | 20 | fits | 126,587 | 114 | 0.502 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 420,787 | 4.208 | 20 | 24 | fits | 126,587 | 114 | 0.502 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 401,516 | 4.015 | 20 | 50 | fits | 126,587 | 114 | 0.502 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,031,483 | 10.315 | 20 | 20 | fits | 79,057 | 30 | 0.681 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 563,988 | 5.640 | 140 | 144 | fits | 48,942 | 102 | 0.303 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 583,913 | 5.839 | 140 | 144 | fits | 48,942 | 102 | 0.303 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,766,073 | 17.661 | 140 | 144 | fits | 51,444 | 102 | 0.373 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,786,916 | 17.869 | 140 | 144 | fits | 51,444 | 102 | 0.373 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,929,465 | 19.295 | 140 | 144 | fits | 45,914 | 102 | 0.255 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,949,216 | 19.492 | 140 | 144 | fits | 45,914 | 102 | 0.255 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 2,126,776 | 21.268 | 140 | 144 | fits | 45,767 | 103 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 2,146,599 | 21.466 | 140 | 144 | fits | 45,767 | 103 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 628,409 | 6.284 | 140 | 144 | fits | 62,180 | 116 | 0.337 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 646,139 | 6.461 | 140 | 144 | fits | 62,180 | 116 | 0.337 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,322,816 | 23.228 | 140 | 144 | fits | 44,641 | 103 | 0.181 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,342,702 | 23.427 | 140 | 144 | fits | 44,641 | 103 | 0.181 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 476,071 | 4.761 | 20 | 200 | fits | 113,979 | 201 | 0.317 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 455,803 | 4.558 | 20 | 20 | fits | 113,979 | 201 | 0.317 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 321,620 | 3.216 | 20 | 24 | fits | 152,572 | 184 | 0.457 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 416,328 | 4.163 | 20 | 50 | fits | 113,979 | 201 | 0.317 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 1,041,559 | 10.416 | 20 | 20 | fits | 79,057 | 30 | 0.681 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 774,335 | 7.743 | 140 | 144 | fits | 28,915 | 52 | 0.485 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,754,360 | 17.544 | 140 | 144 | fits | 50,905 | 102 | 0.374 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,776,152 | 17.762 | 140 | 144 | fits | 50,905 | 102 | 0.374 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,920,063 | 19.201 | 140 | 144 | fits | 46,588 | 103 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,940,351 | 19.404 | 140 | 144 | fits | 46,588 | 103 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,118,755 | 21.188 | 140 | 144 | fits | 45,647 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,138,770 | 21.388 | 140 | 144 | fits | 45,647 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,334,489 | 23.345 | 140 | 144 | fits | 43,964 | 103 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,352,849 | 23.528 | 140 | 144 | fits | 43,964 | 103 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,531,978 | 25.320 | 140 | 144 | fits | 43,785 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,551,701 | 25.517 | 140 | 144 | fits | 43,785 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,727,862 | 27.279 | 140 | 144 | fits | 25,233 | 52 | 0.294 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 152,556 | 1.526 | 20 | 200 | fits | 151,480 | 281 | 0.294 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 444,464 | 4.445 | 20 | 20 | fits | 136,689 | 124 | 0.499 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 424,260 | 4.243 | 20 | 24 | fits | 136,689 | 124 | 0.499 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 404,989 | 4.050 | 20 | 50 | fits | 136,689 | 124 | 0.499 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 1,031,820 | 10.318 | 20 | 20 | fits | 79,048 | 30 | 0.680 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
