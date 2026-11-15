### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 92 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.acmp.if0` (notice-every-0) | 6.831 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.adp.if1` (notice-every-0) | 7.034 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.aecp.if1` (notice-every-0) | 6.629 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 6.437 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.srp.if1` (notice-every-0) | 12.529 | fits | 31 srp | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 2.203 | fits | 0 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-0.mrpdu.periodic.if1` (notice-every-0) | 3.396 | fits | 0 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.36.0.if0` (notice-burst-0) | 50.714 (51.227) | fits | 0 events | 80 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1082 | 0 | 170,274 (1.703) | fits |
| notice-burst-0 | 949 | 0 | 166,452 (1.665) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 6.093 | 62 | 32 | 1 | within |
| notice-every-0 | 6.398 | 62 | 32 | 1 | within |
| notice-every-0 | 2.117 | 62 | 32 | 1 | within |
| notice-every-0 | 2.428 | 62 | 32 | 1 | within |
| notice-every-0 | 8.337 | 62 | 32 | 1 | within |
| notice-every-0 | 8.643 | 62 | 32 | 1 | within |
| notice-every-0 | 4.144 | 62 | 32 | 1 | within |
| notice-every-0 | 4.458 | 62 | 32 | 1 | within |
| notice-every-0 | 10.276 | 62 | 32 | 1 | within |
| notice-every-0 | 10.580 | 62 | 32 | 1 | within |
| notice-every-0 | 12.198 | 62 | 32 | 1 | within |
| notice-every-0 | 12.504 | 62 | 32 | 1 | within |
| notice-every-0 | 14.215 | 62 | 32 | 1 | within |
| notice-every-0 | 14.522 | 62 | 32 | 1 | within |
| notice-every-0 | 16.131 | 62 | 32 | 1 | within |
| notice-every-0 | 16.438 | 62 | 32 | 1 | within |
| notice-every-0 | 18.334 | 62 | 32 | 1 | within |
| notice-every-0 | 18.641 | 62 | 32 | 1 | within |
| notice-every-0 | 20.231 | 62 | 32 | 1 | within |
| notice-every-0 | 20.537 | 62 | 32 | 1 | within |
| notice-every-0 | 24.536 | 62 | 32 | 1 | within |
| notice-every-0 | 28.128 | 62 | 32 | 1 | within |
| notice-every-0 | 28.409 | 62 | 32 | 1 | within |
| notice-every-0 | 30.292 | 62 | 32 | 1 | within |
| notice-every-0 | 30.574 | 62 | 32 | 1 | within |
| notice-every-0 | 32.166 | 62 | 32 | 1 | within |
| notice-every-0 | 32.444 | 62 | 32 | 1 | within |
| notice-every-0 | 34.371 | 62 | 32 | 1 | within |
| notice-every-0 | 34.653 | 62 | 32 | 1 | within |
| notice-every-0 | 36.232 | 62 | 32 | 1 | within |
| notice-every-0 | 36.513 | 62 | 32 | 1 | within |
| notice-every-0 | 38.367 | 62 | 32 | 1 | within |
| notice-every-0 | 38.649 | 62 | 32 | 1 | within |
| notice-every-0 | 40.207 | 62 | 32 | 1 | within |
| notice-every-0 | 40.485 | 62 | 32 | 1 | within |
| notice-every-0 | 42.676 | 62 | 32 | 1 | within |
| notice-every-0 | 42.936 | 62 | 32 | 1 | within |
| notice-every-0 | 44.146 | 62 | 32 | 1 | within |
| notice-every-0 | 44.449 | 62 | 32 | 1 | within |
| notice-every-0 | 46.259 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.501 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.800 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.267 | 62 | 32 | 0 | within |
| notice-burst-0 | 4.572 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.178 | 62 | 32 | 0 | within |
| notice-burst-0 | 5.479 | 62 | 32 | 0 | within |
| notice-burst-0 | 17.420 | 62 | 32 | 0 | within |
| notice-burst-0 | 20.528 | 62 | 32 | 0 | within |
| notice-burst-0 | 20.818 | 62 | 32 | 0 | within |
| notice-burst-0 | 22.546 | 62 | 32 | 0 | within |
| notice-burst-0 | 22.839 | 62 | 32 | 0 | within |
| notice-burst-0 | 24.769 | 62 | 32 | 0 | within |
| notice-burst-0 | 25.061 | 62 | 32 | 0 | within |
| notice-burst-0 | 26.691 | 62 | 32 | 0 | within |
| notice-burst-0 | 26.981 | 62 | 32 | 0 | within |
| notice-burst-0 | 28.607 | 62 | 32 | 0 | within |
| notice-burst-0 | 28.904 | 62 | 32 | 0 | within |
| notice-burst-0 | 30.521 | 62 | 32 | 0 | within |
| notice-burst-0 | 1.750 | 62 | 32 | 0 | within |
| notice-burst-0 | 2.086 | 62 | 32 | 0 | within |
| notice-burst-0 | 30.803 | 62 | 32 | 0 | within |
| notice-burst-0 | 32.749 | 62 | 32 | 0 | within |
| notice-burst-0 | 33.030 | 62 | 32 | 0 | within |
| notice-burst-0 | 34.628 | 62 | 32 | 0 | within |
| notice-burst-0 | 34.909 | 62 | 32 | 0 | within |
| notice-burst-0 | 36.787 | 62 | 32 | 0 | within |
| notice-burst-0 | 37.064 | 62 | 32 | 0 | within |
| notice-burst-0 | 38.643 | 62 | 32 | 0 | within |
| notice-burst-0 | 38.923 | 62 | 32 | 0 | within |
| notice-burst-0 | 40.786 | 62 | 32 | 0 | within |
| notice-burst-0 | 41.066 | 62 | 32 | 0 | within |
| notice-burst-0 | 42.734 | 62 | 32 | 0 | within |
| notice-burst-0 | 43.017 | 62 | 32 | 0 | within |
| notice-burst-0 | 44.574 | 62 | 32 | 0 | within |
| notice-burst-0 | 44.851 | 62 | 32 | 0 | within |
| notice-burst-0 | 46.680 | 62 | 32 | 0 | within |
| notice-burst-0 | 46.939 | 62 | 32 | 0 | within |
| notice-burst-0 | 48.702 | 62 | 32 | 0 | within |
| notice-burst-0 | 49.005 | 62 | 32 | 0 | within |
| notice-burst-0 | 50.714 | 62 | 32 | 0 | within |

Latest: 50.714 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 303 | 87,131 (0.871) | 48,288 (0.483) |
| notice-burst-0 | 313 | 117,689 (1.177) | 48,288 (0.483) |

Longest pass that carries a step: 117,689 CPU cycles (1.177 ms), notice-burst-0; longest step: 48,288 (0.483 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 609,294 | 6.093 | 62 | 66 | fits | 69,798 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 639,842 | 6.398 | 62 | 66 | fits | 69,798 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 211,697 | 2.117 | 62 | 66 | fits | 72,461 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 242,791 | 2.428 | 62 | 66 | fits | 72,461 | 203 | 0.193 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 833,724 | 8.337 | 62 | 66 | fits | 69,404 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 864,286 | 8.643 | 62 | 66 | fits | 69,404 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 414,398 | 4.144 | 62 | 66 | fits | 71,479 | 201 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 445,775 | 4.458 | 62 | 66 | fits | 71,479 | 201 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 1,027,600 | 10.276 | 62 | 66 | fits | 69,279 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 1,058,004 | 10.580 | 62 | 66 | fits | 69,279 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 1,219,805 | 12.198 | 62 | 66 | fits | 69,284 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 1,250,432 | 12.504 | 62 | 66 | fits | 69,284 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 1,421,482 | 14.215 | 62 | 66 | fits | 69,350 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 1,452,188 | 14.522 | 62 | 66 | fits | 69,350 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 1,613,131 | 16.131 | 62 | 66 | fits | 69,214 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 1,643,758 | 16.438 | 62 | 66 | fits | 69,214 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,833,448 | 18.334 | 62 | 66 | fits | 69,249 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,864,084 | 18.641 | 62 | 66 | fits | 69,249 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 2,023,081 | 20.231 | 62 | 66 | fits | 68,139 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 2,053,717 | 20.537 | 62 | 66 | fits | 68,139 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 2,453,605 | 24.536 | 62 | 66 | fits | 37,005 | 101 | 0.267 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 2,812,768 | 28.128 | 62 | 66 | fits | 67,663 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 2,840,898 | 28.409 | 62 | 66 | fits | 67,663 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 3,029,222 | 30.292 | 62 | 66 | fits | 67,566 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 3,057,412 | 30.574 | 62 | 66 | fits | 67,566 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 3,216,629 | 32.166 | 62 | 66 | fits | 67,153 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 3,244,428 | 32.444 | 62 | 66 | fits | 67,153 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 3,437,092 | 34.371 | 62 | 66 | fits | 67,821 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 3,465,298 | 34.653 | 62 | 66 | fits | 67,821 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 3,623,215 | 36.232 | 62 | 66 | fits | 67,326 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 3,651,290 | 36.513 | 62 | 66 | fits | 67,326 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 3,836,677 | 38.367 | 62 | 66 | fits | 66,993 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 3,864,944 | 38.649 | 62 | 66 | fits | 66,993 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 4,020,679 | 40.207 | 62 | 66 | fits | 66,340 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 4,048,488 | 40.485 | 62 | 66 | fits | 66,340 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 4,267,632 | 42.676 | 62 | 66 | fits | 65,280 | 200 | 0.159 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 4,293,631 | 42.936 | 62 | 66 | fits | 65,280 | 200 | 0.159 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 4,414,628 | 44.146 | 62 | 66 | fits | 63,387 | 200 | 0.119 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 4,444,894 | 44.449 | 62 | 66 | fits | 63,387 | 200 | 0.119 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 4,625,896 | 46.259 | 62 | 66 | fits | 37,774 | 102 | 0.182 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 703,417 | 7.034 | 20 | 200 | fits | 145,565 | 120 | 0.621 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 683,149 | 6.831 | 20 | 20 | fits | 145,565 | 120 | 0.621 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 662,945 | 6.629 | 20 | 24 | fits | 145,565 | 120 | 0.621 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 643,674 | 6.437 | 20 | 50 | fits | 145,565 | 120 | 0.621 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 1,252,856 | 12.529 | 20 | 20 | fits | 61,172 | 28 | 0.806 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 220,311 | 2.203 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 339,627 | 3.396 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 250,081 | 2.501 | 62 | 66 | fits | 68,763 | 203 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 279,967 | 2.800 | 62 | 66 | fits | 68,763 | 203 | 0.104 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 426,709 | 4.267 | 62 | 66 | fits | 117,689 | 210 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 457,197 | 4.572 | 62 | 66 | fits | 117,689 | 210 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 517,819 | 5.178 | 62 | 66 | fits | 68,883 | 203 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 547,918 | 5.479 | 62 | 66 | fits | 68,883 | 203 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 1,742,027 | 17.420 | 62 | 66 | fits | 41,599 | 100 | 0.353 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 2,052,810 | 20.528 | 62 | 66 | fits | 69,948 | 201 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 2,081,818 | 20.818 | 62 | 66 | fits | 69,948 | 201 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 2,254,647 | 22.546 | 62 | 66 | fits | 69,974 | 201 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 2,283,871 | 22.839 | 62 | 66 | fits | 69,974 | 201 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 2,476,900 | 24.769 | 62 | 66 | fits | 70,059 | 201 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 2,506,103 | 25.061 | 62 | 66 | fits | 70,059 | 201 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 2,669,096 | 26.691 | 62 | 66 | fits | 69,618 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 2,698,089 | 26.981 | 62 | 66 | fits | 69,618 | 201 | 0.162 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 2,860,744 | 28.607 | 62 | 66 | fits | 69,949 | 201 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 2,890,362 | 28.904 | 62 | 66 | fits | 69,949 | 201 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 3,052,149 | 30.521 | 62 | 66 | fits | 68,483 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 174,987 | 1.750 | 62 | 66 | fits | 104,890 | 212 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 208,630 | 2.086 | 62 | 66 | fits | 104,890 | 212 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 3,080,279 | 30.803 | 62 | 66 | fits | 68,483 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 3,274,866 | 32.749 | 62 | 66 | fits | 68,013 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 3,303,039 | 33.030 | 62 | 66 | fits | 68,013 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 3,462,837 | 34.628 | 62 | 66 | fits | 67,599 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 3,490,859 | 34.909 | 62 | 66 | fits | 67,599 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 3,678,679 | 36.787 | 62 | 66 | fits | 67,260 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 3,706,384 | 37.064 | 62 | 66 | fits | 67,260 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 3,864,257 | 38.643 | 62 | 66 | fits | 67,605 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 3,892,323 | 38.923 | 62 | 66 | fits | 67,605 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 4,078,571 | 40.786 | 62 | 66 | fits | 67,433 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 4,106,552 | 41.066 | 62 | 66 | fits | 67,433 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 4,273,449 | 42.734 | 62 | 66 | fits | 67,240 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 4,301,683 | 43.017 | 62 | 66 | fits | 67,240 | 201 | 0.154 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 4,457,424 | 44.574 | 62 | 66 | fits | 66,399 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 4,485,121 | 44.851 | 62 | 66 | fits | 66,399 | 201 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 4,668,038 | 46.680 | 62 | 66 | fits | 64,293 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 4,693,908 | 46.939 | 62 | 66 | fits | 64,293 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 4,870,192 | 48.702 | 62 | 66 | fits | 63,570 | 200 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 4,900,488 | 49.005 | 62 | 66 | fits | 63,570 | 200 | 0.125 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 5,071,398 | 50.714 | 62 | 66 | fits | 39,307 | 102 | 0.231 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 676,283 | 6.763 | 20 | 200 | fits | 151,991 | 80 | 0.601 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 656,015 | 6.560 | 20 | 20 | fits | 151,991 | 80 | 0.601 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 326,130 | 3.261 | 20 | 24 | fits | 162,832 | 113 | 0.448 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 464,549 | 4.645 | 20 | 50 | fits | 157,690 | 243 | 0.379 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 1,106,140 | 11.061 | 20 | 20 | fits | 120,326 | 43 | 0.589 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
