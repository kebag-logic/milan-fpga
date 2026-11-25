### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.acmp.if0` (notice-retried-5) | 3.840 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.adp.if0` (notice-retried-7) | 1.546 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.aecp.if0` (notice-retried-5) | 3.638 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.maap.if0` (notice-retried-5) | 3.445 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.srp.if0` (notice-retried-7) | 8.147 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-0.mrpdu.periodic.if0` (notice-retried-0) | 0.858 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-2.stream_info.if0` (notice-retried-2) | 8.243 (8.346) | fits | 3 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 2288 | 0 | 151,722 (1.517) | fits |
| notice-retried-1 | 2289 | 0 | 151,623 (1.516) | fits |
| notice-retried-2 | 2288 | 0 | 151,485 (1.515) | fits |
| notice-retried-3 | 2286 | 0 | 151,658 (1.517) | fits |
| notice-retried-4 | 2288 | 0 | 151,821 (1.518) | fits |
| notice-retried-5 | 2287 | 0 | 151,673 (1.517) | fits |
| notice-retried-6 | 2286 | 0 | 151,526 (1.515) | fits |
| notice-retried-7 | 2286 | 0 | 151,272 (1.513) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 8.125 | 20 | 16 | 2 | within |
| notice-retried-1 | 8.242 | 20 | 16 | 2 | within |
| notice-retried-2 | 8.243 | 20 | 16 | 3 | within |
| notice-retried-3 | 8.158 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.135 | 20 | 16 | 2 | within |
| notice-retried-5 | 8.194 | 20 | 16 | 2 | within |
| notice-retried-6 | 8.024 | 20 | 16 | 1 | within |
| notice-retried-7 | 8.108 | 20 | 16 | 1 | within |

Latest: 8.243 ms, notice-retried-2.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 403 | 92,645 (0.926) | 77,965 (0.780) |
| notice-retried-1 | 403 | 92,645 (0.926) | 77,965 (0.780) |
| notice-retried-2 | 403 | 92,645 (0.926) | 77,965 (0.780) |
| notice-retried-3 | 403 | 92,645 (0.926) | 77,965 (0.780) |
| notice-retried-4 | 403 | 92,645 (0.926) | 77,965 (0.780) |
| notice-retried-5 | 403 | 92,645 (0.926) | 77,965 (0.780) |
| notice-retried-6 | 403 | 92,645 (0.926) | 77,965 (0.780) |
| notice-retried-7 | 403 | 92,645 (0.926) | 77,965 (0.780) |

Longest pass that carries a step: 92,645 CPU cycles (0.926 ms), notice-retried-0; longest step: 77,965 (0.780 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 812,461 | 8.125 | 20 | 24 | fits | 23,831 | 52 | 0.442 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 151,354 | 1.514 | 20 | 200 | fits | 147,779 | 279 | 0.201 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 365,726 | 3.657 | 20 | 20 | fits | 92,085 | 92 | 0.485 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 345,522 | 3.455 | 20 | 24 | fits | 92,085 | 92 | 0.485 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 326,251 | 3.263 | 20 | 50 | fits | 92,085 | 92 | 0.485 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 811,879 | 8.119 | 20 | 20 | fits | 75,369 | 34 | 0.712 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 85,827 | 0.858 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 824,166 | 8.242 | 20 | 24 | fits | 23,915 | 52 | 0.445 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 38,720 | 0.387 | 20 | 200 | fits | 32,530 | 60 | 0.077 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 361,635 | 3.616 | 20 | 20 | fits | 96,701 | 113 | 0.459 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 341,431 | 3.414 | 20 | 24 | fits | 96,701 | 113 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 322,160 | 3.222 | 20 | 50 | fits | 96,701 | 113 | 0.459 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 807,794 | 8.078 | 20 | 20 | fits | 75,526 | 34 | 0.714 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 76,720 | 0.767 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 824,314 | 8.243 | 20 | 24 | fits | 24,155 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 125,475 | 1.255 | 20 | 200 | fits | 124,515 | 166 | 0.160 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 361,457 | 3.615 | 20 | 20 | fits | 96,701 | 113 | 0.459 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 341,253 | 3.413 | 20 | 24 | fits | 96,701 | 113 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 321,982 | 3.220 | 20 | 50 | fits | 96,701 | 113 | 0.459 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 807,217 | 8.072 | 20 | 20 | fits | 75,502 | 34 | 0.715 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 76,143 | 0.761 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 815,843 | 8.158 | 20 | 24 | fits | 23,945 | 52 | 0.445 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 153,831 | 1.538 | 20 | 200 | fits | 146,398 | 278 | 0.231 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 371,034 | 3.710 | 20 | 20 | fits | 94,519 | 96 | 0.490 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 350,830 | 3.508 | 20 | 24 | fits | 94,519 | 96 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 331,559 | 3.316 | 20 | 50 | fits | 94,519 | 96 | 0.490 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 813,865 | 8.139 | 20 | 20 | fits | 58,776 | 39 | 0.752 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 70,938 | 0.709 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 813,504 | 8.135 | 20 | 24 | fits | 23,733 | 52 | 0.440 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 150,905 | 1.509 | 20 | 200 | fits | 143,590 | 274 | 0.207 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 382,129 | 3.821 | 20 | 20 | fits | 95,352 | 96 | 0.502 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 361,925 | 3.619 | 20 | 24 | fits | 95,352 | 96 | 0.502 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 342,654 | 3.427 | 20 | 50 | fits | 95,352 | 96 | 0.502 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 806,314 | 8.063 | 20 | 20 | fits | 52,506 | 26 | 0.738 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 72,622 | 0.726 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 819,447 | 8.194 | 20 | 24 | fits | 23,943 | 52 | 0.445 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 150,579 | 1.506 | 20 | 200 | fits | 146,495 | 278 | 0.203 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 383,994 | 3.840 | 20 | 20 | fits | 99,667 | 109 | 0.512 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 363,790 | 3.638 | 20 | 24 | fits | 99,667 | 109 | 0.512 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 344,519 | 3.445 | 20 | 50 | fits | 99,667 | 109 | 0.512 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 807,960 | 8.080 | 20 | 20 | fits | 52,506 | 26 | 0.738 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 74,358 | 0.744 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 802,448 | 8.024 | 20 | 24 | fits | 24,155 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 125,709 | 1.257 | 20 | 200 | fits | 123,008 | 163 | 0.163 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 363,621 | 3.636 | 20 | 20 | fits | 92,159 | 94 | 0.482 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 343,417 | 3.434 | 20 | 24 | fits | 92,159 | 94 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 324,146 | 3.241 | 20 | 50 | fits | 92,159 | 94 | 0.482 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 807,412 | 8.074 | 20 | 20 | fits | 63,954 | 30 | 0.724 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 73,410 | 0.734 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 810,811 | 8.108 | 20 | 24 | fits | 25,179 | 52 | 0.489 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 154,557 | 1.546 | 20 | 200 | fits | 144,329 | 274 | 0.230 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 371,177 | 3.712 | 20 | 20 | fits | 94,470 | 96 | 0.488 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 350,973 | 3.510 | 20 | 24 | fits | 94,470 | 96 | 0.488 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 331,702 | 3.317 | 20 | 50 | fits | 94,470 | 96 | 0.488 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 814,662 | 8.147 | 20 | 20 | fits | 63,965 | 30 | 0.724 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 67,224 | 0.672 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
