### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 140 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.acmp.if0` (notice-burst-2) | 4.974 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.adp.if0` (notice-burst-2) | 5.176 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.aecp.if0` (notice-every-6) | 4.661 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.maap.if0` (notice-burst-2) | 4.579 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-6.held.srp.if0` (notice-every-6) | 11.925 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 0.973 | fits | 0 srp | 4 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.9.0.if0` (notice-burst-6) | 23.369 (23.605) | fits | 1 events | 96 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1516 | 0 | 155,178 (1.552) | fits |
| notice-every-2 | 1515 | 0 | 157,156 (1.572) | fits |
| notice-every-4 | 1510 | 0 | 157,650 (1.577) | fits |
| notice-every-6 | 1505 | 0 | 156,620 (1.566) | fits |
| notice-burst-0 | 1107 | 0 | 154,621 (1.546) | fits |
| notice-burst-2 | 1074 | 0 | 155,972 (1.560) | fits |
| notice-burst-4 | 1074 | 0 | 157,794 (1.578) | fits |
| notice-burst-6 | 1071 | 0 | 157,110 (1.571) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.005 | 140 | 16 | 2 | within |
| notice-every-0 | 8.180 | 140 | 16 | 2 | within |
| notice-every-0 | 2.024 | 140 | 16 | 2 | within |
| notice-every-0 | 2.202 | 140 | 16 | 2 | within |
| notice-every-0 | 3.796 | 140 | 16 | 2 | within |
| notice-every-0 | 3.981 | 140 | 16 | 2 | within |
| notice-every-0 | 5.882 | 140 | 16 | 2 | within |
| notice-every-0 | 6.064 | 140 | 16 | 2 | within |
| notice-every-0 | 9.803 | 140 | 16 | 2 | within |
| notice-every-0 | 9.936 | 140 | 16 | 2 | within |
| notice-every-0 | 11.951 | 140 | 16 | 2 | within |
| notice-every-0 | 12.121 | 140 | 16 | 2 | within |
| notice-every-2 | 1.915 | 140 | 16 | 2 | within |
| notice-every-2 | 2.092 | 140 | 16 | 2 | within |
| notice-every-2 | 3.894 | 140 | 16 | 2 | within |
| notice-every-2 | 4.069 | 140 | 16 | 2 | within |
| notice-every-2 | 5.995 | 140 | 16 | 2 | within |
| notice-every-2 | 6.175 | 140 | 16 | 2 | within |
| notice-every-2 | 7.844 | 140 | 16 | 2 | within |
| notice-every-2 | 8.021 | 140 | 16 | 2 | within |
| notice-every-2 | 9.870 | 140 | 16 | 2 | within |
| notice-every-2 | 10.003 | 140 | 16 | 2 | within |
| notice-every-2 | 11.838 | 140 | 16 | 2 | within |
| notice-every-2 | 12.009 | 140 | 16 | 2 | within |
| notice-every-4 | 5.802 | 140 | 16 | 2 | within |
| notice-every-4 | 5.979 | 140 | 16 | 2 | within |
| notice-every-4 | 7.861 | 140 | 16 | 2 | within |
| notice-every-4 | 8.037 | 140 | 16 | 2 | within |
| notice-every-4 | 1.917 | 140 | 16 | 2 | within |
| notice-every-4 | 2.103 | 140 | 16 | 2 | within |
| notice-every-4 | 3.914 | 140 | 16 | 2 | within |
| notice-every-4 | 4.099 | 140 | 16 | 2 | within |
| notice-every-4 | 9.874 | 140 | 16 | 2 | within |
| notice-every-4 | 10.007 | 140 | 16 | 2 | within |
| notice-every-4 | 11.830 | 140 | 16 | 2 | within |
| notice-every-4 | 12.001 | 140 | 16 | 2 | within |
| notice-every-6 | 8.136 | 140 | 16 | 1 | within |
| notice-every-6 | 8.311 | 140 | 16 | 1 | within |
| notice-every-6 | 2.155 | 140 | 16 | 1 | within |
| notice-every-6 | 2.335 | 140 | 16 | 1 | within |
| notice-every-6 | 4.030 | 140 | 16 | 1 | within |
| notice-every-6 | 4.214 | 140 | 16 | 1 | within |
| notice-every-6 | 6.020 | 140 | 16 | 1 | within |
| notice-every-6 | 6.203 | 140 | 16 | 1 | within |
| notice-every-6 | 9.943 | 140 | 16 | 1 | within |
| notice-every-6 | 10.076 | 140 | 16 | 1 | within |
| notice-every-6 | 12.101 | 140 | 16 | 1 | within |
| notice-every-6 | 12.272 | 140 | 16 | 1 | within |
| notice-burst-0 | 8.450 | 140 | 16 | 1 | within |
| notice-burst-0 | 16.880 | 140 | 16 | 1 | within |
| notice-burst-0 | 17.058 | 140 | 16 | 1 | within |
| notice-burst-0 | 18.137 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.138 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.323 | 140 | 16 | 1 | within |
| notice-burst-0 | 3.182 | 140 | 16 | 1 | within |
| notice-burst-0 | 3.365 | 140 | 16 | 1 | within |
| notice-burst-0 | 18.288 | 140 | 16 | 1 | within |
| notice-burst-0 | 20.085 | 140 | 16 | 1 | within |
| notice-burst-0 | 20.256 | 140 | 16 | 1 | within |
| notice-burst-0 | 6.669 | 140 | 16 | 1 | within |
| notice-burst-2 | 8.356 | 140 | 16 | 1 | within |
| notice-burst-2 | 15.436 | 140 | 16 | 1 | within |
| notice-burst-2 | 15.615 | 140 | 16 | 1 | within |
| notice-burst-2 | 17.283 | 140 | 16 | 1 | within |
| notice-burst-2 | 17.454 | 140 | 16 | 1 | within |
| notice-burst-2 | 19.308 | 140 | 16 | 1 | within |
| notice-burst-2 | 3.136 | 140 | 16 | 1 | within |
| notice-burst-2 | 3.323 | 140 | 16 | 1 | within |
| notice-burst-2 | 19.461 | 140 | 16 | 1 | within |
| notice-burst-2 | 21.306 | 140 | 16 | 1 | within |
| notice-burst-2 | 21.476 | 140 | 16 | 1 | within |
| notice-burst-2 | 6.681 | 140 | 16 | 1 | within |
| notice-burst-4 | 12.607 | 140 | 16 | 1 | within |
| notice-burst-4 | 12.788 | 140 | 16 | 1 | within |
| notice-burst-4 | 2.585 | 140 | 16 | 1 | within |
| notice-burst-4 | 14.076 | 140 | 16 | 1 | within |
| notice-burst-4 | 14.247 | 140 | 16 | 1 | within |
| notice-burst-4 | 16.113 | 140 | 16 | 1 | within |
| notice-burst-4 | 16.283 | 140 | 16 | 1 | within |
| notice-burst-4 | 18.139 | 140 | 16 | 1 | within |
| notice-burst-4 | 18.290 | 140 | 16 | 1 | within |
| notice-burst-4 | 20.136 | 140 | 16 | 1 | within |
| notice-burst-4 | 20.308 | 140 | 16 | 1 | within |
| notice-burst-4 | 22.117 | 140 | 16 | 1 | within |
| notice-burst-6 | 7.631 | 140 | 16 | 1 | within |
| notice-burst-6 | 17.574 | 140 | 16 | 1 | within |
| notice-burst-6 | 17.751 | 140 | 16 | 1 | within |
| notice-burst-6 | 19.222 | 140 | 16 | 1 | within |
| notice-burst-6 | 19.393 | 140 | 16 | 1 | within |
| notice-burst-6 | 21.245 | 140 | 16 | 1 | within |
| notice-burst-6 | 2.307 | 140 | 16 | 1 | within |
| notice-burst-6 | 2.494 | 140 | 16 | 1 | within |
| notice-burst-6 | 21.398 | 140 | 16 | 1 | within |
| notice-burst-6 | 23.198 | 140 | 16 | 1 | within |
| notice-burst-6 | 23.369 | 140 | 16 | 1 | within |
| notice-burst-6 | 4.192 | 140 | 16 | 1 | within |

Latest: 23.369 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 402 | 96,652 (0.967) | 78,332 (0.783) |
| notice-every-2 | 402 | 96,652 (0.967) | 78,332 (0.783) |
| notice-every-4 | 402 | 96,652 (0.967) | 78,332 (0.783) |
| notice-every-6 | 402 | 96,652 (0.967) | 78,332 (0.783) |
| notice-burst-0 | 412 | 96,652 (0.967) | 78,332 (0.783) |
| notice-burst-2 | 412 | 96,652 (0.967) | 78,332 (0.783) |
| notice-burst-4 | 412 | 96,652 (0.967) | 78,332 (0.783) |
| notice-burst-6 | 412 | 96,652 (0.967) | 78,332 (0.783) |

Longest pass that carries a step: 96,652 CPU cycles (0.967 ms), notice-every-0; longest step: 78,332 (0.783 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 800,473 | 8.005 | 140 | 144 | fits | 42,159 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 817,973 | 8.180 | 140 | 144 | fits | 42,159 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 202,409 | 2.024 | 140 | 144 | fits | 43,630 | 103 | 0.278 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 220,180 | 2.202 | 140 | 144 | fits | 43,630 | 103 | 0.278 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 379,644 | 3.796 | 140 | 144 | fits | 44,244 | 104 | 0.271 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 398,101 | 3.981 | 140 | 144 | fits | 44,244 | 104 | 0.271 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 588,186 | 5.882 | 140 | 144 | fits | 42,493 | 103 | 0.252 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 606,386 | 6.064 | 140 | 144 | fits | 42,493 | 103 | 0.252 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 980,287 | 9.803 | 140 | 144 | fits | 34,216 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 993,588 | 9.936 | 140 | 144 | fits | 34,216 | 101 | 0.234 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 1,195,089 | 11.951 | 140 | 144 | fits | 39,795 | 104 | 0.159 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 1,212,144 | 12.121 | 140 | 144 | fits | 39,795 | 104 | 0.159 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 168,429 | 1.684 | 20 | 200 | fits | 152,155 | 250 | 0.399 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 451,419 | 4.514 | 20 | 20 | fits | 138,433 | 130 | 0.470 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 431,215 | 4.312 | 20 | 24 | fits | 138,433 | 130 | 0.470 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 411,944 | 4.119 | 20 | 50 | fits | 138,433 | 130 | 0.470 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,163,263 | 11.633 | 20 | 20 | fits | 40,284 | 19 | 0.823 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 97,289 | 0.973 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 191,536 | 1.915 | 140 | 144 | fits | 43,342 | 103 | 0.282 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 209,222 | 2.092 | 140 | 144 | fits | 43,342 | 103 | 0.282 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 389,356 | 3.894 | 140 | 144 | fits | 42,689 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 406,900 | 4.069 | 140 | 144 | fits | 42,689 | 102 | 0.273 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 599,488 | 5.995 | 140 | 144 | fits | 42,667 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 617,476 | 6.175 | 140 | 144 | fits | 42,667 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 784,418 | 7.844 | 140 | 144 | fits | 41,228 | 104 | 0.247 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 802,111 | 8.021 | 140 | 144 | fits | 41,228 | 104 | 0.247 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 986,966 | 9.870 | 140 | 144 | fits | 34,670 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 1,000,267 | 10.003 | 140 | 144 | fits | 34,670 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 1,183,803 | 11.838 | 140 | 144 | fits | 39,926 | 104 | 0.165 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 1,200,858 | 12.009 | 140 | 144 | fits | 39,926 | 104 | 0.165 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 169,722 | 1.697 | 20 | 200 | fits | 152,494 | 252 | 0.399 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 477,694 | 4.777 | 20 | 20 | fits | 141,160 | 130 | 0.493 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 457,490 | 4.575 | 20 | 24 | fits | 141,160 | 130 | 0.493 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 438,219 | 4.382 | 20 | 50 | fits | 141,160 | 130 | 0.493 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,180,642 | 11.806 | 20 | 20 | fits | 40,200 | 19 | 0.822 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 88,035 | 0.880 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 580,153 | 5.802 | 140 | 144 | fits | 43,002 | 105 | 0.280 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 597,913 | 5.979 | 140 | 144 | fits | 43,002 | 105 | 0.280 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 786,083 | 7.861 | 140 | 144 | fits | 42,233 | 104 | 0.262 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 803,744 | 8.037 | 140 | 144 | fits | 42,233 | 104 | 0.262 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 191,708 | 1.917 | 140 | 144 | fits | 44,666 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 210,288 | 2.103 | 140 | 144 | fits | 44,666 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 391,410 | 3.914 | 140 | 144 | fits | 43,673 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 409,875 | 4.099 | 140 | 144 | fits | 43,673 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 987,368 | 9.874 | 140 | 144 | fits | 34,536 | 101 | 0.243 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 1,000,669 | 10.007 | 140 | 144 | fits | 34,536 | 101 | 0.243 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 1,183,017 | 11.830 | 140 | 144 | fits | 39,864 | 104 | 0.161 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 1,200,072 | 12.001 | 140 | 144 | fits | 39,864 | 104 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 149,480 | 1.495 | 20 | 200 | fits | 150,836 | 240 | 0.358 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 467,354 | 4.674 | 20 | 20 | fits | 146,836 | 155 | 0.470 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 447,150 | 4.471 | 20 | 24 | fits | 146,836 | 155 | 0.470 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 427,879 | 4.279 | 20 | 50 | fits | 146,836 | 155 | 0.470 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,174,343 | 11.743 | 20 | 20 | fits | 40,215 | 19 | 0.822 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 88,155 | 0.882 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 813,632 | 8.136 | 140 | 144 | fits | 42,031 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 831,132 | 8.311 | 140 | 144 | fits | 42,031 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 215,459 | 2.155 | 140 | 144 | fits | 44,130 | 103 | 0.293 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 233,485 | 2.335 | 140 | 144 | fits | 44,130 | 103 | 0.293 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 403,043 | 4.030 | 140 | 144 | fits | 43,703 | 102 | 0.259 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 421,360 | 4.214 | 140 | 144 | fits | 43,703 | 102 | 0.259 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 601,993 | 6.020 | 140 | 144 | fits | 42,762 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 620,333 | 6.203 | 140 | 144 | fits | 42,762 | 103 | 0.260 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 994,312 | 9.943 | 140 | 144 | fits | 34,164 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 1,007,613 | 10.076 | 140 | 144 | fits | 34,164 | 101 | 0.231 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 1,210,110 | 12.101 | 140 | 144 | fits | 39,842 | 104 | 0.163 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 1,227,165 | 12.272 | 140 | 144 | fits | 39,842 | 104 | 0.163 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 173,471 | 1.735 | 20 | 200 | fits | 152,542 | 251 | 0.399 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 486,291 | 4.863 | 20 | 20 | fits | 141,984 | 132 | 0.503 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 466,087 | 4.661 | 20 | 24 | fits | 141,984 | 132 | 0.503 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 446,816 | 4.468 | 20 | 50 | fits | 141,984 | 132 | 0.503 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,192,549 | 11.925 | 20 | 20 | fits | 40,507 | 19 | 0.825 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 86,177 | 0.862 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 845,043 | 8.450 | 140 | 144 | fits | 25,663 | 52 | 0.476 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,687,957 | 16.880 | 140 | 144 | fits | 44,314 | 103 | 0.346 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,705,802 | 17.058 | 140 | 144 | fits | 44,314 | 103 | 0.346 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,813,717 | 18.137 | 140 | 144 | fits | 38,776 | 102 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 213,762 | 2.138 | 140 | 144 | fits | 60,639 | 111 | 0.313 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 232,304 | 2.323 | 140 | 144 | fits | 60,639 | 111 | 0.313 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 318,162 | 3.182 | 140 | 144 | fits | 58,891 | 112 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 336,534 | 3.365 | 140 | 144 | fits | 58,891 | 112 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,828,819 | 18.288 | 140 | 144 | fits | 38,776 | 102 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,008,535 | 20.085 | 140 | 144 | fits | 36,935 | 102 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,025,616 | 20.256 | 140 | 144 | fits | 36,935 | 102 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 666,883 | 6.669 | 140 | 144 | fits | 26,381 | 52 | 0.377 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 151,392 | 1.514 | 20 | 200 | fits | 151,693 | 244 | 0.369 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 482,856 | 4.829 | 20 | 20 | fits | 147,238 | 154 | 0.499 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 462,652 | 4.627 | 20 | 24 | fits | 147,238 | 154 | 0.499 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 443,381 | 4.434 | 20 | 50 | fits | 147,238 | 154 | 0.499 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 1,070,648 | 10.706 | 20 | 20 | fits | 78,929 | 30 | 0.675 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 835,619 | 8.356 | 140 | 144 | fits | 26,405 | 52 | 0.487 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,543,644 | 15.436 | 140 | 144 | fits | 43,683 | 103 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,561,466 | 15.615 | 140 | 144 | fits | 43,683 | 103 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,728,328 | 17.283 | 140 | 144 | fits | 40,910 | 102 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 1,745,426 | 17.454 | 140 | 144 | fits | 40,910 | 102 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 1,930,784 | 19.308 | 140 | 144 | fits | 39,228 | 102 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 313,645 | 3.136 | 140 | 144 | fits | 60,300 | 111 | 0.313 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 332,320 | 3.323 | 140 | 144 | fits | 60,300 | 111 | 0.313 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,946,085 | 19.461 | 140 | 144 | fits | 39,228 | 102 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,130,559 | 21.306 | 140 | 144 | fits | 37,041 | 102 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,147,647 | 21.476 | 140 | 144 | fits | 37,041 | 102 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 668,111 | 6.681 | 140 | 144 | fits | 26,456 | 52 | 0.367 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 517,646 | 5.176 | 20 | 200 | fits | 141,232 | 228 | 0.410 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 497,378 | 4.974 | 20 | 20 | fits | 141,232 | 228 | 0.410 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 309,486 | 3.095 | 20 | 24 | fits | 151,158 | 153 | 0.479 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 457,903 | 4.579 | 20 | 50 | fits | 141,232 | 228 | 0.410 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,144,447 | 11.444 | 20 | 20 | fits | 38,742 | 18 | 0.813 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,260,738 | 12.607 | 140 | 144 | fits | 45,084 | 102 | 0.351 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,278,834 | 12.788 | 140 | 144 | fits | 45,084 | 102 | 0.351 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 258,478 | 2.585 | 140 | 144 | fits | 26,679 | 52 | 0.494 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,407,560 | 14.076 | 140 | 144 | fits | 40,994 | 103 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,424,728 | 14.247 | 140 | 144 | fits | 40,994 | 103 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,611,305 | 16.113 | 140 | 144 | fits | 41,023 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,628,349 | 16.283 | 140 | 144 | fits | 41,023 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,813,941 | 18.139 | 140 | 144 | fits | 38,724 | 103 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,829,031 | 18.290 | 140 | 144 | fits | 38,724 | 103 | 0.217 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 2,013,616 | 20.136 | 140 | 144 | fits | 37,090 | 102 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,030,776 | 20.308 | 140 | 144 | fits | 37,090 | 102 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,211,653 | 22.117 | 140 | 144 | fits | 22,703 | 52 | 0.262 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 147,257 | 1.473 | 20 | 200 | fits | 150,178 | 241 | 0.354 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 455,547 | 4.555 | 20 | 20 | fits | 144,085 | 144 | 0.478 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 435,343 | 4.353 | 20 | 24 | fits | 144,085 | 144 | 0.478 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 416,072 | 4.161 | 20 | 50 | fits | 144,085 | 144 | 0.478 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 1,047,024 | 10.470 | 20 | 20 | fits | 79,160 | 30 | 0.675 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 763,057 | 7.631 | 140 | 144 | fits | 26,691 | 52 | 0.506 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,757,370 | 17.574 | 140 | 144 | fits | 44,321 | 102 | 0.347 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,775,143 | 17.751 | 140 | 144 | fits | 44,321 | 102 | 0.347 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,922,224 | 19.222 | 140 | 144 | fits | 41,098 | 103 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,939,321 | 19.393 | 140 | 144 | fits | 41,098 | 103 | 0.249 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,124,462 | 21.245 | 140 | 144 | fits | 39,228 | 102 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 230,726 | 2.307 | 140 | 144 | fits | 44,927 | 102 | 0.280 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 249,365 | 2.494 | 140 | 144 | fits | 44,927 | 102 | 0.280 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,139,835 | 21.398 | 140 | 144 | fits | 39,228 | 102 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,319,829 | 23.198 | 140 | 144 | fits | 36,862 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,336,910 | 23.369 | 140 | 144 | fits | 36,862 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 419,210 | 4.192 | 140 | 144 | fits | 40,741 | 62 | 0.316 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 152,180 | 1.522 | 20 | 200 | fits | 147,831 | 236 | 0.374 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 458,059 | 4.581 | 20 | 20 | fits | 142,346 | 144 | 0.473 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 437,855 | 4.379 | 20 | 24 | fits | 142,346 | 144 | 0.473 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 418,584 | 4.186 | 20 | 50 | fits | 142,346 | 144 | 0.473 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 1,044,842 | 10.448 | 20 | 20 | fits | 79,021 | 30 | 0.675 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
