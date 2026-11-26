### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.acmp.if0` (notice-retried-7) | 8.338 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.adp.if0` (notice-retried-6) | 7.049 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-2.held.aecp.if0` (notice-retried-2) | 6.059 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-2.held.maap.if0` (notice-retried-2) | 7.203 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.srp.if0` (notice-retried-7) | 11.372 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-7.mrpdu.periodic.if0` (notice-retried-7) | 1.061 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-7.stream_info.if0` (notice-retried-7) | 8.157 (8.266) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1427 | 0 | 169,178 (1.692) | fits |
| notice-retried-1 | 1426 | 0 | 169,207 (1.692) | fits |
| notice-retried-2 | 1427 | 0 | 169,207 (1.692) | fits |
| notice-retried-3 | 1425 | 0 | 169,207 (1.692) | fits |
| notice-retried-4 | 1427 | 0 | 169,178 (1.692) | fits |
| notice-retried-5 | 1427 | 0 | 169,178 (1.692) | fits |
| notice-retried-6 | 1423 | 0 | 169,178 (1.692) | fits |
| notice-retried-7 | 1423 | 0 | 169,178 (1.692) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 8.138 | 20 | 16 | 2 | within |
| notice-retried-1 | 7.905 | 20 | 16 | 1 | within |
| notice-retried-2 | 7.905 | 20 | 16 | 1 | within |
| notice-retried-3 | 7.905 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.122 | 20 | 16 | 2 | within |
| notice-retried-5 | 7.561 | 20 | 16 | 2 | within |
| notice-retried-6 | 7.525 | 20 | 16 | 2 | within |
| notice-retried-7 | 8.157 | 20 | 16 | 1 | within |

Latest: 8.157 ms, notice-retried-7.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 657 | 110,146 (1.101) | 78,109 (0.781) |
| notice-retried-1 | 657 | 110,095 (1.101) | 78,109 (0.781) |
| notice-retried-2 | 657 | 110,016 (1.100) | 78,109 (0.781) |
| notice-retried-3 | 657 | 110,016 (1.100) | 78,109 (0.781) |
| notice-retried-4 | 657 | 104,580 (1.046) | 78,109 (0.781) |
| notice-retried-5 | 657 | 110,141 (1.101) | 78,109 (0.781) |
| notice-retried-6 | 658 | 110,146 (1.101) | 78,109 (0.781) |
| notice-retried-7 | 658 | 110,215 (1.102) | 78,109 (0.781) |

Longest pass that carries a step: 110,215 CPU cycles (1.102 ms), notice-retried-7; longest step: 78,109 (0.781 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 813,787 | 8.138 | 20 | 24 | fits | 24,076 | 52 | 0.460 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 668,582 | 6.686 | 20 | 200 | fits | 156,804 | 204 | 0.230 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 799,943 | 7.999 | 20 | 20 | fits | 139,441 | 77 | 0.687 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 534,580 | 5.346 | 20 | 24 | fits | 100,049 | 52 | 0.514 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 608,839 | 6.088 | 20 | 50 | fits | 156,804 | 204 | 0.230 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 1,103,077 | 11.031 | 20 | 20 | fits | 92,265 | 38 | 0.707 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 81,025 | 0.810 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 790,538 | 7.905 | 20 | 24 | fits | 23,452 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 162,038 | 1.620 | 20 | 200 | fits | 161,080 | 204 | 0.275 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 748,806 | 7.488 | 20 | 20 | fits | 133,177 | 80 | 0.692 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 595,425 | 5.954 | 20 | 24 | fits | 159,929 | 115 | 0.449 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 709,331 | 7.093 | 20 | 50 | fits | 133,177 | 80 | 0.692 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 1,083,137 | 10.831 | 20 | 20 | fits | 118,465 | 53 | 0.721 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 80,306 | 0.803 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 790,477 | 7.905 | 20 | 24 | fits | 23,452 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 173,129 | 1.731 | 20 | 200 | fits | 158,947 | 203 | 0.271 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 759,812 | 7.598 | 20 | 20 | fits | 133,677 | 74 | 0.722 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 605,931 | 6.059 | 20 | 24 | fits | 159,568 | 116 | 0.446 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 720,337 | 7.203 | 20 | 50 | fits | 133,677 | 74 | 0.722 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 1,080,824 | 10.808 | 20 | 20 | fits | 103,292 | 42 | 0.702 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 80,117 | 0.801 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 790,538 | 7.905 | 20 | 24 | fits | 23,452 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 157,224 | 1.572 | 20 | 200 | fits | 155,338 | 146 | 0.176 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 748,439 | 7.484 | 20 | 20 | fits | 133,344 | 80 | 0.693 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 594,891 | 5.949 | 20 | 24 | fits | 159,914 | 115 | 0.449 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 708,964 | 7.090 | 20 | 50 | fits | 133,344 | 80 | 0.693 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 1,082,662 | 10.827 | 20 | 20 | fits | 118,414 | 53 | 0.721 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 79,832 | 0.798 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 812,165 | 8.122 | 20 | 24 | fits | 23,452 | 52 | 0.450 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 167,003 | 1.670 | 20 | 200 | fits | 154,617 | 194 | 0.254 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 756,253 | 7.563 | 20 | 20 | fits | 133,722 | 74 | 0.724 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 602,327 | 6.023 | 20 | 24 | fits | 159,790 | 116 | 0.448 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 716,778 | 7.168 | 20 | 50 | fits | 133,722 | 74 | 0.724 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 1,059,496 | 10.595 | 20 | 20 | fits | 92,500 | 40 | 0.704 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 92,898 | 0.929 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 756,145 | 7.561 | 20 | 24 | fits | 23,960 | 52 | 0.457 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 166,605 | 1.666 | 20 | 200 | fits | 151,110 | 143 | 0.182 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 749,894 | 7.499 | 20 | 20 | fits | 133,231 | 80 | 0.692 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 596,459 | 5.965 | 20 | 24 | fits | 160,104 | 115 | 0.452 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 710,419 | 7.104 | 20 | 50 | fits | 133,231 | 80 | 0.692 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 1,063,807 | 10.638 | 20 | 20 | fits | 103,299 | 44 | 0.698 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 74,524 | 0.745 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 752,500 | 7.525 | 20 | 24 | fits | 24,076 | 52 | 0.460 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 704,898 | 7.049 | 20 | 200 | fits | 152,598 | 208 | 0.299 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 818,973 | 8.190 | 20 | 20 | fits | 134,343 | 69 | 0.644 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 535,165 | 5.352 | 20 | 24 | fits | 100,297 | 52 | 0.514 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 645,155 | 6.452 | 20 | 50 | fits | 152,598 | 208 | 0.299 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 1,132,680 | 11.327 | 20 | 20 | fits | 103,227 | 42 | 0.702 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 86,268 | 0.863 | 49 | 49 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 815,663 | 8.157 | 20 | 24 | fits | 24,076 | 52 | 0.460 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 702,372 | 7.024 | 20 | 200 | fits | 156,730 | 205 | 0.228 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 833,751 | 8.338 | 20 | 20 | fits | 139,490 | 77 | 0.688 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 535,563 | 5.356 | 20 | 24 | fits | 87,435 | 42 | 0.495 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 642,629 | 6.426 | 20 | 50 | fits | 156,730 | 205 | 0.228 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 1,137,217 | 11.372 | 20 | 20 | fits | 92,390 | 38 | 0.707 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 106,079 | 1.061 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
