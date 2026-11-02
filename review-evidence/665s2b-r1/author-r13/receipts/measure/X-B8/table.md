### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 14 paths and 0 of 23 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record released under the composed load, first | 0 | `x-links-same.service.acmp.first.if0` (x-links-same) | 1.462 | fits | 0 acmp | 2 | 0 |
| ACMP record released under the composed load, last | 0 | `y-links.service.acmp.last.if0` (y-links) | 7.816 | fits | 11 acmp | 2 | 0 |
| ADP record released under the composed load, first | 0 | `x-links-same.service.adp.first.if0` (x-links-same) | 1.504 | fits | 0 adp | 2 | 0 |
| ADP record released under the composed load, last | 0 | `y-links.service.adp.last.if0` (y-links) | 6.044 | fits | 7 adp | 1 | 0 |
| ADP record released under the composed load, last | 1 | `x-links-same.service.adp.last.if1` (x-links-same) | 5.822 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `x-links-same.service.aecp.first.if0` (x-links-same) | 1.498 | fits | 0 aecp | 2 | 0 |
| AECP record released under the composed load, last | 1 | `y-links.service.aecp.last.if1` (y-links) | 11.613 | fits | 15 aecp | 2 | 0 |
| MAAP record released under the composed load, first | 0 | `x-links-same.service.maap.first.if0` (x-links-same) | 1.487 | fits | 0 maap | 2 | 0 |
| MAAP record released under the composed load, last | 0 | `y-links.service.maap.last.if0` (y-links) | 6.080 | fits | 6 maap | 2 | 0 |
| SRP record released under the composed load, first | 0 | `y-links.service.srp.first.if0` (y-links) | 7.074 | fits | 0 srp | 2 | 0 |
| SRP record released under the composed load, last | 1 | `y-links.service.srp.last.if1` (y-links) | 12.201 | fits | 31 srp | 2 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-links-same.acmp_command.if0` (x-links-same) | 6.995 (7.515) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-links-same.event.if0` (x-links-same) | 1.604 (2.757) | fits | 14 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `y-links.adp_available.if0` (y-links) | 4.393 (6.096) | fits | 7 adp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| x-links-same | 0 | 12.585 | 21 | 156,041 (1.560) | yes | - |
| y-links | 0 | 12.800 | 20 | 181,734 (1.817) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| x-links-same | 304 | 0 | 156,041 (1.560) | fits |
| y-links | 312 | 0 | 181,734 (1.817) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `x-links-same.event.if0` | 160,409 | 1.604 | 20 | 200 | fits | 125,075 | 115 | 0.503 |
| an ACMP command behind a full acmp ring | `x-links-same.acmp_command.if0` | 699,456 | 6.995 | 20 | 20 | fits | 80,742 | 37 | 0.577 |
| ADP record released under the composed load, first | `x-links-same.service.adp.first.if0` | 150,449 | 1.504 | 20 | 200 | fits | 150,649 | 146 | 0.520 |
| ADP record released under the composed load, last | `x-links-same.service.adp.last.if1` | 582,207 | 5.822 | 20 | 200 | fits | 156,041 | 50 | 0.666 |
| ACMP record released under the composed load, first | `x-links-same.service.acmp.first.if0` | 146,190 | 1.462 | 20 | 20 | fits | 150,649 | 146 | 0.520 |
| ACMP record released under the composed load, last | `x-links-same.service.acmp.last.if0` | 746,174 | 7.462 | 20 | 20 | fits | 80,742 | 37 | 0.577 |
| AECP record released under the composed load, first | `x-links-same.service.aecp.first.if0` | 149,775 | 1.498 | 20 | 24 | fits | 150,649 | 146 | 0.520 |
| AECP record released under the composed load, last | `x-links-same.service.aecp.last.if1` | 1,099,102 | 10.991 | 20 | 24 | fits | 34,082 | 31 | 0.435 |
| MAAP record released under the composed load, first | `x-links-same.service.maap.first.if0` | 148,735 | 1.487 | 20 | 50 | fits | 150,649 | 146 | 0.520 |
| MAAP record released under the composed load, last | `x-links-same.service.maap.last.if0` | 580,712 | 5.807 | 20 | 50 | fits | 156,041 | 50 | 0.666 |
| SRP record released under the composed load, first | `x-links-same.service.srp.first.if0` | 668,347 | 6.683 | 18 | 18 | fits | 87,700 | 46 | 0.603 |
| SRP record released under the composed load, last | `x-links-same.service.srp.last.if1` | 1,198,040 | 11.980 | 18 | 18 | fits | 20,064 | 18 | 0.049 |
| an ENTITY_AVAILABLE behind a full adp ring | `y-links.adp_available.if0` | 439,306 | 4.393 | 20 | 20 | fits | 181,734 | 63 | 0.694 |
| ADP record released under the composed load, first | `y-links.service.adp.first.if0` | 143,741 | 1.437 | 20 | 200 | fits | 148,407 | 146 | 0.491 |
| ADP record released under the composed load, last | `y-links.service.adp.last.if0` | 604,354 | 6.044 | 20 | 200 | fits | 181,734 | 63 | 0.694 |
| ACMP record released under the composed load, first | `y-links.service.acmp.first.if0` | 144,653 | 1.447 | 20 | 20 | fits | 148,407 | 146 | 0.491 |
| ACMP record released under the composed load, last | `y-links.service.acmp.last.if0` | 781,620 | 7.816 | 20 | 20 | fits | 77,109 | 34 | 0.560 |
| AECP record released under the composed load, first | `y-links.service.aecp.first.if0` | 148,238 | 1.482 | 20 | 24 | fits | 148,407 | 146 | 0.491 |
| AECP record released under the composed load, last | `y-links.service.aecp.last.if1` | 1,161,324 | 11.613 | 20 | 24 | fits | 34,056 | 31 | 0.435 |
| MAAP record released under the composed load, first | `y-links.service.maap.first.if0` | 147,198 | 1.472 | 20 | 50 | fits | 148,407 | 146 | 0.491 |
| MAAP record released under the composed load, last | `y-links.service.maap.last.if0` | 608,030 | 6.080 | 20 | 50 | fits | 181,734 | 63 | 0.694 |
| SRP record released under the composed load, first | `y-links.service.srp.first.if0` | 707,426 | 7.074 | 18 | 18 | fits | 99,461 | 46 | 0.650 |
| SRP record released under the composed load, last | `y-links.service.srp.last.if1` | 1,220,075 | 12.201 | 18 | 18 | fits | 20,059 | 18 | 0.049 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
