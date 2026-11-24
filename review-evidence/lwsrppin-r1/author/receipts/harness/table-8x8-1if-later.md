### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.acmp.if0` (notice-retried-5) | 4.506 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.adp.if0` (notice-retried-3) | 1.699 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.aecp.if0` (notice-retried-5) | 4.304 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.maap.if0` (notice-retried-5) | 4.111 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.srp.if0` (notice-retried-7) | 7.464 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-6.mrpdu.periodic.if0` (notice-retried-6) | 0.880 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-7.stream_info.if0` (notice-retried-7) | 8.275 (8.364) | fits | 3 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1698 | 0 | 151,820 (1.518) | fits |
| notice-retried-1 | 1696 | 0 | 153,693 (1.537) | fits |
| notice-retried-2 | 1697 | 0 | 153,837 (1.538) | fits |
| notice-retried-3 | 1697 | 0 | 151,840 (1.518) | fits |
| notice-retried-4 | 1696 | 0 | 152,903 (1.529) | fits |
| notice-retried-5 | 1696 | 0 | 153,530 (1.535) | fits |
| notice-retried-6 | 1696 | 0 | 154,995 (1.550) | fits |
| notice-retried-7 | 1695 | 0 | 153,291 (1.533) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 7.709 | 20 | 16 | 2 | within |
| notice-retried-1 | 7.976 | 20 | 16 | 1 | within |
| notice-retried-2 | 7.976 | 20 | 16 | 1 | within |
| notice-retried-3 | 8.217 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.007 | 20 | 16 | 1 | within |
| notice-retried-5 | 8.214 | 20 | 16 | 1 | within |
| notice-retried-6 | 8.004 | 20 | 16 | 1 | within |
| notice-retried-7 | 8.275 | 20 | 16 | 3 | within |

Latest: 8.275 ms, notice-retried-7.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 656 | 97,791 (0.978) | 77,779 (0.778) |
| notice-retried-1 | 656 | 97,791 (0.978) | 77,779 (0.778) |
| notice-retried-2 | 656 | 97,791 (0.978) | 77,779 (0.778) |
| notice-retried-3 | 656 | 97,791 (0.978) | 77,779 (0.778) |
| notice-retried-4 | 656 | 97,791 (0.978) | 77,779 (0.778) |
| notice-retried-5 | 656 | 97,791 (0.978) | 77,779 (0.778) |
| notice-retried-6 | 656 | 97,791 (0.978) | 77,779 (0.778) |
| notice-retried-7 | 656 | 97,791 (0.978) | 77,779 (0.778) |

Longest pass that carries a step: 97,791 CPU cycles (0.978 ms), notice-retried-0; longest step: 77,779 (0.778 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 770,881 | 7.709 | 20 | 24 | fits | 22,713 | 52 | 0.444 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 164,382 | 1.644 | 20 | 200 | fits | 150,996 | 219 | 0.252 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 438,396 | 4.384 | 20 | 20 | fits | 142,462 | 145 | 0.417 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 418,192 | 4.182 | 20 | 24 | fits | 142,462 | 145 | 0.417 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 398,921 | 3.989 | 20 | 50 | fits | 142,462 | 145 | 0.417 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 742,556 | 7.426 | 20 | 20 | fits | 91,017 | 46 | 0.524 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 76,839 | 0.768 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 797,554 | 7.976 | 20 | 24 | fits | 22,601 | 52 | 0.442 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 161,260 | 1.613 | 20 | 200 | fits | 153,693 | 225 | 0.240 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 435,348 | 4.353 | 20 | 20 | fits | 142,405 | 145 | 0.417 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 415,144 | 4.151 | 20 | 24 | fits | 142,405 | 145 | 0.417 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 395,873 | 3.959 | 20 | 50 | fits | 142,405 | 145 | 0.417 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 739,546 | 7.395 | 20 | 20 | fits | 95,564 | 59 | 0.569 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 72,826 | 0.728 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 797,554 | 7.976 | 20 | 24 | fits | 22,601 | 52 | 0.442 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 161,121 | 1.611 | 20 | 200 | fits | 153,837 | 225 | 0.243 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 435,418 | 4.354 | 20 | 20 | fits | 142,489 | 145 | 0.417 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 415,214 | 4.152 | 20 | 24 | fits | 142,489 | 145 | 0.417 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 395,943 | 3.959 | 20 | 50 | fits | 142,489 | 145 | 0.417 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 739,616 | 7.396 | 20 | 20 | fits | 95,564 | 59 | 0.569 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 72,896 | 0.729 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 821,749 | 8.217 | 20 | 24 | fits | 22,713 | 52 | 0.444 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 169,947 | 1.699 | 20 | 200 | fits | 151,263 | 222 | 0.273 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 443,850 | 4.439 | 20 | 20 | fits | 142,331 | 145 | 0.415 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 423,646 | 4.236 | 20 | 24 | fits | 142,331 | 145 | 0.415 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 404,375 | 4.044 | 20 | 50 | fits | 142,331 | 145 | 0.415 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 732,162 | 7.322 | 20 | 20 | fits | 90,901 | 48 | 0.516 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 83,383 | 0.834 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 800,731 | 8.007 | 20 | 24 | fits | 22,713 | 52 | 0.444 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 163,098 | 1.631 | 20 | 200 | fits | 152,174 | 223 | 0.247 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 449,309 | 4.493 | 20 | 20 | fits | 143,294 | 145 | 0.427 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 429,105 | 4.291 | 20 | 24 | fits | 143,294 | 145 | 0.427 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 409,834 | 4.098 | 20 | 50 | fits | 143,294 | 145 | 0.427 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 737,334 | 7.373 | 20 | 20 | fits | 90,669 | 46 | 0.514 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 87,559 | 0.876 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 821,372 | 8.214 | 20 | 24 | fits | 22,713 | 52 | 0.444 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 162,778 | 1.628 | 20 | 200 | fits | 153,530 | 224 | 0.244 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 450,619 | 4.506 | 20 | 20 | fits | 146,427 | 158 | 0.438 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 430,415 | 4.304 | 20 | 24 | fits | 146,427 | 158 | 0.438 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 411,144 | 4.111 | 20 | 50 | fits | 146,427 | 158 | 0.438 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 738,911 | 7.389 | 20 | 20 | fits | 90,670 | 46 | 0.516 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 87,476 | 0.875 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 800,424 | 8.004 | 20 | 24 | fits | 22,713 | 52 | 0.444 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 161,552 | 1.616 | 20 | 200 | fits | 154,995 | 227 | 0.240 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 449,397 | 4.494 | 20 | 20 | fits | 146,427 | 158 | 0.438 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 429,193 | 4.292 | 20 | 24 | fits | 146,427 | 158 | 0.438 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 409,922 | 4.099 | 20 | 50 | fits | 146,427 | 158 | 0.438 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 737,689 | 7.377 | 20 | 20 | fits | 90,670 | 46 | 0.516 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 87,975 | 0.880 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 827,500 | 8.275 | 20 | 24 | fits | 22,713 | 52 | 0.444 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 143,206 | 1.432 | 20 | 200 | fits | 140,847 | 160 | 0.150 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 442,265 | 4.423 | 20 | 20 | fits | 151,170 | 162 | 0.416 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 422,061 | 4.221 | 20 | 24 | fits | 151,170 | 162 | 0.416 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 402,790 | 4.028 | 20 | 50 | fits | 151,170 | 162 | 0.416 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 746,383 | 7.464 | 20 | 20 | fits | 90,941 | 46 | 0.524 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 79,942 | 0.799 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
