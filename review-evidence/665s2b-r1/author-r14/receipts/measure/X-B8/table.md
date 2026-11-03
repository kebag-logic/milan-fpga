### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 14 paths and 0 of 23 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record released under the composed load, first | 0 | `x-links-same.service.acmp.first.if0` (x-links-same) | 1.406 | fits | 0 acmp | 2 | 0 |
| ACMP record released under the composed load, last | 0 | `y-links.service.acmp.last.if0` (y-links) | 7.627 | fits | 11 acmp | 2 | 0 |
| ADP record released under the composed load, first | 0 | `x-links-same.service.adp.first.if0` (x-links-same) | 1.448 | fits | 0 adp | 2 | 0 |
| ADP record released under the composed load, last | 0 | `y-links.service.adp.last.if0` (y-links) | 5.859 | fits | 7 adp | 1 | 0 |
| ADP record released under the composed load, last | 1 | `x-links-same.service.adp.last.if1` (x-links-same) | 5.631 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `x-links-same.service.aecp.first.if0` (x-links-same) | 1.442 | fits | 0 aecp | 2 | 0 |
| AECP record released under the composed load, last | 1 | `y-links.service.aecp.last.if1` (y-links) | 11.184 | fits | 15 aecp | 2 | 0 |
| MAAP record released under the composed load, first | 0 | `x-links-same.service.maap.first.if0` (x-links-same) | 1.431 | fits | 0 maap | 2 | 0 |
| MAAP record released under the composed load, last | 0 | `y-links.service.maap.last.if0` (y-links) | 5.896 | fits | 6 maap | 2 | 0 |
| SRP record released under the composed load, first | 0 | `x-links-same.service.srp.first.if0` (x-links-same) | 7.367 | fits | 0 srp | 2 | 0 |
| SRP record released under the composed load, last | 1 | `y-links.service.srp.last.if1` (y-links) | 11.708 | fits | 31 srp | 2 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-links-same.acmp_command.if0` (x-links-same) | 6.851 (7.390) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-links-same.event.if0` (x-links-same) | 1.551 (2.615) | fits | 14 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `y-links.adp_available.if0` (y-links) | 4.216 (5.912) | fits | 7 adp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| x-links-same | 0 | 11.994 | 21 | 155,632 (1.556) | yes | - |
| y-links | 0 | 12.245 | 20 | 180,863 (1.809) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| x-links-same | 304 | 0 | 155,632 (1.556) | fits |
| y-links | 312 | 0 | 180,863 (1.809) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| x-links-same | 266 | 47,159 (0.472) | 2,743 (0.027) |
| y-links | 271 | 47,159 (0.472) | 2,743 (0.027) |

Longest pass that carries a step: 47,159 CPU cycles (0.472 ms), x-links-same; longest step: 2,743 (0.027 ms), x-links-same.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `x-links-same.event.if0` | 155,148 | 1.551 | 20 | 200 | fits | 116,417 | 115 | 0.520 |
| an ACMP command behind a full acmp ring | `x-links-same.acmp_command.if0` | 685,062 | 6.851 | 20 | 20 | fits | 90,948 | 52 | 0.569 |
| ADP record released under the composed load, first | `x-links-same.service.adp.first.if0` | 144,833 | 1.448 | 20 | 200 | fits | 145,033 | 146 | 0.520 |
| ADP record released under the composed load, last | `x-links-same.service.adp.last.if1` | 563,098 | 5.631 | 20 | 200 | fits | 155,632 | 50 | 0.674 |
| ACMP record released under the composed load, first | `x-links-same.service.acmp.first.if0` | 140,574 | 1.406 | 20 | 20 | fits | 145,033 | 146 | 0.520 |
| ACMP record released under the composed load, last | `x-links-same.service.acmp.last.if0` | 733,765 | 7.338 | 20 | 20 | fits | 90,948 | 52 | 0.569 |
| AECP record released under the composed load, first | `x-links-same.service.aecp.first.if0` | 144,159 | 1.442 | 20 | 24 | fits | 145,033 | 146 | 0.520 |
| AECP record released under the composed load, last | `x-links-same.service.aecp.last.if1` | 1,056,796 | 10.568 | 20 | 24 | fits | 31,819 | 31 | 0.479 |
| MAAP record released under the composed load, first | `x-links-same.service.maap.first.if0` | 143,119 | 1.431 | 20 | 50 | fits | 145,033 | 146 | 0.520 |
| MAAP record released under the composed load, last | `x-links-same.service.maap.last.if0` | 561,603 | 5.616 | 20 | 50 | fits | 155,632 | 50 | 0.674 |
| SRP record released under the composed load, first | `x-links-same.service.srp.first.if0` | 736,680 | 7.367 | 18 | 18 | fits | 90,948 | 52 | 0.569 |
| SRP record released under the composed load, last | `x-links-same.service.srp.last.if1` | 1,144,967 | 11.450 | 18 | 18 | fits | 17,827 | 18 | 0.170 |
| an ENTITY_AVAILABLE behind a full adp ring | `y-links.adp_available.if0` | 421,646 | 4.216 | 20 | 20 | fits | 180,863 | 63 | 0.697 |
| ADP record released under the composed load, first | `y-links.service.adp.first.if0` | 139,304 | 1.393 | 20 | 200 | fits | 143,970 | 146 | 0.507 |
| ADP record released under the composed load, last | `y-links.service.adp.last.if0` | 585,944 | 5.859 | 20 | 200 | fits | 180,863 | 63 | 0.697 |
| ACMP record released under the composed load, first | `y-links.service.acmp.first.if0` | 140,216 | 1.402 | 20 | 20 | fits | 143,970 | 146 | 0.507 |
| ACMP record released under the composed load, last | `y-links.service.acmp.last.if0` | 762,661 | 7.627 | 20 | 20 | fits | 76,510 | 34 | 0.573 |
| AECP record released under the composed load, first | `y-links.service.aecp.first.if0` | 143,801 | 1.438 | 20 | 24 | fits | 143,970 | 146 | 0.507 |
| AECP record released under the composed load, last | `y-links.service.aecp.last.if1` | 1,118,402 | 11.184 | 20 | 24 | fits | 31,868 | 31 | 0.482 |
| MAAP record released under the composed load, first | `y-links.service.maap.first.if0` | 142,761 | 1.428 | 20 | 50 | fits | 143,970 | 146 | 0.507 |
| MAAP record released under the composed load, last | `y-links.service.maap.last.if0` | 589,620 | 5.896 | 20 | 50 | fits | 180,863 | 63 | 0.697 |
| SRP record released under the composed load, first | `y-links.service.srp.first.if0` | 689,066 | 6.891 | 18 | 18 | fits | 99,511 | 46 | 0.663 |
| SRP record released under the composed load, last | `y-links.service.srp.last.if1` | 1,170,829 | 11.708 | 18 | 18 | fits | 17,822 | 18 | 0.170 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
