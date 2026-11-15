### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 47 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.acmp.if0` (notice-every-0) | 6.831 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.adp.if1` (notice-every-0) | 7.034 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.aecp.if1` (notice-every-0) | 6.629 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 6.437 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.srp.if1` (notice-every-0) | 12.529 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 2.203 | fits | 0 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-0.mrpdu.periodic.if1` (notice-every-0) | 3.396 | fits | 0 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-every-0.notices.29.36.0.if0` (notice-every-0) | 46.259 (46.521) | fits | 1 events | 40 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1082 | 0 | 170,274 (1.703) | fits |

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

Latest: 46.259 ms, notice-every-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 303 | 87,131 (0.871) | 48,288 (0.483) |

Longest pass that carries a step: 87,131 CPU cycles (0.871 ms), notice-every-0; longest step: 48,288 (0.483 ms), notice-every-0.

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

Bounded waits that timed out (the probe is graded on what the log holds):

- none
