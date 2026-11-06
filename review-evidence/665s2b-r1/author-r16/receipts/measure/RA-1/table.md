### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 6 paths and 8 of 48 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.acmp.if0` (notice-retried-3) | 6.073 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.adp.if0` (notice-retried-3) | 3.945 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.aecp.if0` (notice-retried-4) | 10.627 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.maap.if0` (notice-retried-3) | 3.348 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-1.held.srp.if0` (notice-retried-1) | 10.741 | fits | 31 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-0.stream_info.if0` (notice-retried-0) | 30.322 (31.209) | MISS ceiling | 1 events | 8 | 8 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1561 | 0 | 116,000 (1.160) | fits |
| notice-retried-1 | 1560 | 0 | 116,000 (1.160) | fits |
| notice-retried-2 | 1561 | 0 | 116,069 (1.161) | fits |
| notice-retried-3 | 1561 | 0 | 115,980 (1.160) | fits |
| notice-retried-4 | 1561 | 0 | 116,000 (1.160) | fits |
| notice-retried-5 | 1560 | 0 | 116,000 (1.160) | fits |
| notice-retried-6 | 1562 | 0 | 116,000 (1.160) | fits |
| notice-retried-7 | 1560 | 0 | 116,461 (1.165) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 30.322 | 20 | 16 | 1 | OVER |
| notice-retried-1 | 30.296 | 20 | 16 | 1 | OVER |
| notice-retried-2 | 30.320 | 20 | 16 | 1 | OVER |
| notice-retried-3 | 30.294 | 20 | 16 | 1 | OVER |
| notice-retried-4 | 30.321 | 20 | 16 | 1 | OVER |
| notice-retried-5 | 30.318 | 20 | 16 | 1 | OVER |
| notice-retried-6 | 30.320 | 20 | 16 | 1 | OVER |
| notice-retried-7 | 30.295 | 20 | 16 | 1 | OVER |

Latest: 30.322 ms, notice-retried-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 308 | 116,000 (1.160) | 76,313 (0.763) |
| notice-retried-1 | 308 | 116,000 (1.160) | 76,313 (0.763) |
| notice-retried-2 | 308 | 116,069 (1.161) | 76,313 (0.763) |
| notice-retried-3 | 308 | 115,980 (1.160) | 76,313 (0.763) |
| notice-retried-4 | 308 | 116,000 (1.160) | 76,313 (0.763) |
| notice-retried-5 | 308 | 116,000 (1.160) | 76,313 (0.763) |
| notice-retried-6 | 308 | 116,000 (1.160) | 76,313 (0.763) |
| notice-retried-7 | 308 | 116,461 (1.165) | 76,313 (0.763) |

Longest pass that carries a step: 116,461 CPU cycles (1.165 ms), notice-retried-7; longest step: 76,313 (0.763 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 3,032,176 | 30.322 | 20 | 24 | MISS ceiling | 38,958 | 100 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 369,457 | 3.695 | 20 | 200 | fits | 96,241 | 99 | 0.615 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 582,265 | 5.823 | 20 | 20 | fits | 69,996 | 43 | 0.733 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 1,044,532 | 10.445 | 20 | 24 | fits | 53,019 | 35 | 0.723 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 309,714 | 3.097 | 20 | 50 | fits | 96,241 | 99 | 0.615 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 1,063,532 | 10.635 | 18 | 18 | fits | 25,432 | 20 | 0.760 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 3,029,610 | 30.296 | 20 | 24 | MISS ceiling | 38,914 | 100 | 0.197 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 391,579 | 3.916 | 20 | 200 | fits | 96,287 | 99 | 0.615 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 596,516 | 5.965 | 20 | 20 | fits | 62,125 | 41 | 0.746 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 1,055,071 | 10.551 | 20 | 24 | fits | 53,031 | 35 | 0.723 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 331,836 | 3.318 | 20 | 50 | fits | 96,287 | 99 | 0.615 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 1,074,064 | 10.741 | 18 | 18 | fits | 25,432 | 20 | 0.760 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 3,031,994 | 30.320 | 20 | 24 | MISS ceiling | 38,914 | 100 | 0.197 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 390,021 | 3.900 | 20 | 200 | fits | 96,287 | 99 | 0.615 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 602,733 | 6.027 | 20 | 20 | fits | 69,900 | 43 | 0.732 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 1,053,396 | 10.534 | 20 | 24 | fits | 53,031 | 35 | 0.723 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 330,278 | 3.303 | 20 | 50 | fits | 96,287 | 99 | 0.615 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 1,072,418 | 10.724 | 18 | 18 | fits | 25,391 | 20 | 0.760 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 3,029,420 | 30.294 | 20 | 24 | MISS ceiling | 38,959 | 100 | 0.201 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 394,543 | 3.945 | 20 | 200 | fits | 96,287 | 99 | 0.615 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 607,255 | 6.073 | 20 | 20 | fits | 69,900 | 43 | 0.732 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 1,041,852 | 10.419 | 20 | 24 | fits | 52,935 | 35 | 0.723 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 334,800 | 3.348 | 20 | 50 | fits | 96,287 | 99 | 0.615 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 1,068,519 | 10.685 | 18 | 18 | fits | 33,082 | 23 | 0.708 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 3,032,059 | 30.321 | 20 | 24 | MISS ceiling | 38,915 | 100 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 392,626 | 3.926 | 20 | 200 | fits | 96,300 | 99 | 0.615 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 605,377 | 6.054 | 20 | 20 | fits | 69,913 | 43 | 0.732 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 1,062,693 | 10.627 | 20 | 24 | fits | 53,031 | 35 | 0.723 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 332,883 | 3.329 | 20 | 50 | fits | 96,300 | 99 | 0.615 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 1,056,254 | 10.563 | 18 | 18 | fits | 34,857 | 25 | 0.746 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 3,031,787 | 30.318 | 20 | 24 | MISS ceiling | 38,958 | 100 | 0.199 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 374,408 | 3.744 | 20 | 200 | fits | 96,266 | 99 | 0.616 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 587,288 | 5.873 | 20 | 20 | fits | 70,020 | 43 | 0.733 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 1,044,569 | 10.446 | 20 | 24 | fits | 52,935 | 35 | 0.723 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 314,665 | 3.147 | 20 | 50 | fits | 96,266 | 99 | 0.616 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 1,063,586 | 10.636 | 18 | 18 | fits | 25,432 | 20 | 0.760 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 3,031,978 | 30.320 | 20 | 24 | MISS ceiling | 38,914 | 100 | 0.197 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 345,993 | 3.460 | 20 | 200 | fits | 73,377 | 92 | 0.561 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 558,133 | 5.581 | 20 | 20 | fits | 69,879 | 43 | 0.732 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 1,015,239 | 10.152 | 20 | 24 | fits | 53,031 | 35 | 0.723 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 286,250 | 2.862 | 20 | 50 | fits | 73,377 | 92 | 0.561 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 1,067,136 | 10.671 | 18 | 18 | fits | 25,225 | 20 | 0.754 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 3,029,533 | 30.295 | 20 | 24 | MISS ceiling | 38,959 | 100 | 0.201 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 390,233 | 3.902 | 20 | 200 | fits | 96,287 | 99 | 0.615 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 579,034 | 5.790 | 20 | 20 | fits | 70,199 | 43 | 0.735 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 1,036,149 | 10.361 | 20 | 24 | fits | 52,935 | 35 | 0.723 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 330,490 | 3.305 | 20 | 50 | fits | 96,287 | 99 | 0.615 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 1,062,816 | 10.628 | 18 | 18 | fits | 33,082 | 23 | 0.708 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
