Original file: <scratch>/budget/final/later-8x8-1if/table.md
Original size: 12699 bytes
Original sha256: 646b4fee482e0c3ed4efae8cda35745cca7cd283dc9f596347ed409dd5aa7cd9

### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.acmp.if0` (notice-retried-5) | 5.403 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.adp.if0` (notice-retried-7) | 4.724 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.aecp.if0` (notice-retried-4) | 4.457 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.maap.if0` (notice-retried-4) | 4.264 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-1.held.srp.if0` (notice-retried-1) | 8.638 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-5.mrpdu.periodic.if0` (notice-retried-5) | 1.075 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-3.stream_info.if0` (notice-retried-3) | 8.246 (8.354) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1418 | 0 | 158,543 (1.585) | fits |
| notice-retried-1 | 1417 | 0 | 158,543 (1.585) | fits |
| notice-retried-2 | 1419 | 0 | 158,489 (1.585) | fits |
| notice-retried-3 | 1418 | 0 | 154,811 (1.548) | fits |
| notice-retried-4 | 1416 | 0 | 158,651 (1.587) | fits |
| notice-retried-5 | 1416 | 0 | 158,305 (1.583) | fits |
| notice-retried-6 | 1416 | 0 | 158,449 (1.584) | fits |
| notice-retried-7 | 1416 | 0 | 158,507 (1.585) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 7.798 | 20 | 16 | 3 | within |
| notice-retried-1 | 7.948 | 20 | 16 | 1 | within |
| notice-retried-2 | 7.948 | 20 | 16 | 1 | within |
| notice-retried-3 | 8.246 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.243 | 20 | 16 | 2 | within |
| notice-retried-5 | 8.230 | 20 | 16 | 1 | within |
| notice-retried-6 | 7.971 | 20 | 16 | 1 | within |
| notice-retried-7 | 8.005 | 20 | 16 | 1 | within |

Latest: 8.246 ms, notice-retried-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 303 | 81,289 (0.813) | 47,868 (0.479) |
| notice-retried-1 | 303 | 81,289 (0.813) | 47,868 (0.479) |
| notice-retried-2 | 303 | 81,289 (0.813) | 47,868 (0.479) |
| notice-retried-3 | 303 | 81,289 (0.813) | 47,868 (0.479) |
| notice-retried-4 | 303 | 81,289 (0.813) | 47,868 (0.479) |
| notice-retried-5 | 303 | 81,289 (0.813) | 47,868 (0.479) |
| notice-retried-6 | 303 | 81,289 (0.813) | 47,868 (0.479) |
| notice-retried-7 | 303 | 81,289 (0.813) | 47,868 (0.479) |

Longest pass that carries a step: 81,289 CPU cycles (0.813 ms), notice-retried-0; longest step: 47,868 (0.479 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 779,795 | 7.798 | 20 | 24 | fits | 24,943 | 52 | 0.440 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 159,268 | 1.593 | 20 | 200 | fits | 146,450 | 146 | 0.347 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 446,761 | 4.468 | 20 | 20 | fits | 152,698 | 142 | 0.420 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 426,557 | 4.266 | 20 | 24 | fits | 152,698 | 142 | 0.420 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 407,286 | 4.073 | 20 | 50 | fits | 152,698 | 142 | 0.420 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 837,833 | 8.378 | 20 | 20 | fits | 88,897 | 42 | 0.585 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 84,804 | 0.848 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 794,839 | 7.948 | 20 | 24 | fits | 24,781 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 157,996 | 1.580 | 20 | 200 | fits | 150,611 | 151 | 0.333 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 522,665 | 5.227 | 20 | 20 | fits | 87,694 | 37 | 0.756 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 363,239 | 3.632 | 20 | 24 | fits | 97,044 | 70 | 0.422 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 395,496 | 3.955 | 20 | 50 | fits | 151,090 | 156 | 0.415 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 863,793 | 8.638 | 20 | 20 | fits | 46,076 | 22 | 0.769 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 92,053 | 0.921 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 794,842 | 7.948 | 20 | 24 | fits | 24,781 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 160,972 | 1.610 | 20 | 200 | fits | 156,167 | 223 | 0.355 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 445,507 | 4.455 | 20 | 20 | fits | 152,546 | 142 | 0.419 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 425,303 | 4.253 | 20 | 24 | fits | 152,546 | 142 | 0.419 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 406,032 | 4.060 | 20 | 50 | fits | 152,546 | 142 | 0.419 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 836,459 | 8.365 | 20 | 20 | fits | 89,343 | 42 | 0.594 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 83,939 | 0.839 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 824,574 | 8.246 | 20 | 24 | fits | 24,781 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 162,969 | 1.630 | 20 | 200 | fits | 154,539 | 208 | 0.375 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 447,940 | 4.479 | 20 | 20 | fits | 150,998 | 155 | 0.416 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 427,736 | 4.277 | 20 | 24 | fits | 150,998 | 155 | 0.416 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 408,465 | 4.085 | 20 | 50 | fits | 150,998 | 155 | 0.416 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 837,891 | 8.379 | 20 | 20 | fits | 85,557 | 51 | 0.625 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 89,783 | 0.898 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 824,281 | 8.243 | 20 | 24 | fits | 24,781 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 165,599 | 1.656 | 20 | 200 | fits | 151,955 | 217 | 0.373 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 465,888 | 4.659 | 20 | 20 | fits | 152,948 | 144 | 0.417 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 445,684 | 4.457 | 20 | 24 | fits | 152,948 | 144 | 0.417 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 426,413 | 4.264 | 20 | 50 | fits | 152,948 | 144 | 0.417 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 839,269 | 8.393 | 20 | 20 | fits | 80,520 | 40 | 0.609 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 90,525 | 0.905 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 822,959 | 8.230 | 20 | 24 | fits | 24,781 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 159,941 | 1.599 | 20 | 200 | fits | 148,851 | 147 | 0.339 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 540,292 | 5.403 | 20 | 20 | fits | 87,742 | 37 | 0.756 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 432,346 | 4.323 | 20 | 24 | fits | 155,943 | 169 | 0.426 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 413,075 | 4.131 | 20 | 50 | fits | 155,943 | 169 | 0.426 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 862,857 | 8.629 | 20 | 20 | fits | 37,240 | 18 | 0.825 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 107,536 | 1.075 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 797,096 | 7.971 | 20 | 24 | fits | 24,871 | 52 | 0.438 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 162,081 | 1.621 | 20 | 200 | fits | 149,071 | 146 | 0.344 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 461,266 | 4.613 | 20 | 20 | fits | 156,822 | 157 | 0.420 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 441,062 | 4.411 | 20 | 24 | fits | 156,822 | 157 | 0.420 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 421,791 | 4.218 | 20 | 50 | fits | 156,822 | 157 | 0.420 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 833,997 | 8.340 | 20 | 20 | fits | 80,251 | 38 | 0.610 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 99,332 | 0.993 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 800,522 | 8.005 | 20 | 24 | fits | 25,605 | 52 | 0.460 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 472,421 | 4.724 | 20 | 200 | fits | 154,720 | 150 | 0.414 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 452,153 | 4.522 | 20 | 20 | fits | 154,720 | 150 | 0.414 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 431,949 | 4.319 | 20 | 24 | fits | 154,720 | 150 | 0.414 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 412,678 | 4.127 | 20 | 50 | fits | 154,720 | 150 | 0.414 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 840,385 | 8.404 | 20 | 20 | fits | 88,897 | 42 | 0.585 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 87,662 | 0.877 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
