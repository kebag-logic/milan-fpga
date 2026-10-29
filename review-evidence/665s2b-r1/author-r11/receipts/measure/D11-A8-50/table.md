### 8x8

Clock: CPU 50 MHz, the product's split CPU clock (the Milan clock), bus 100 MHz.

4 of 17 paths and 13 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 12.706 (13.846) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 7.317 (9.650) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.270 (1.234) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 3.462 (6.417) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 66.412 (67.398) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.746 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 3.237 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 13.793 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 3.280 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 9.597 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 10.587 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 3.273 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 68.706 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 3.263 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 10.572 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 8.777 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | 25.662 | MISS ceiling | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 24.149 | 18 | 164,096 (3.282) | yes | - |
| backlog-adp | 26.607 | 18 | 151,157 (3.023) | yes | - |
| backlog-adp-refill | 41.897 | 25 | 151,157 (3.023) | yes | - |
| backlog-owed | 360.797 | 65 | 150,069 (3.001) | yes | - |

Composed maximum over the 4 backlog windows: 164,096 CPU cycles (3.282 ms), backlog.
Over the windows that released their whole load only: 164,096 (3.282 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 100,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 301 | 6 | 164,096 (3.282) | OVER the share |
| backlog-adp | 320 | 6 | 151,157 (3.023) | OVER the share |
| backlog-adp-refill | 327 | 6 | 151,157 (3.023) | OVER the share |
| backlog-owed | 359 | 6 | 150,069 (3.001) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 173,083 | 3.462 | 20 | 200 | fits | 156,748 | 129 | 0.623 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 635,321 | 12.706 | 20 | 20 | fits | 81,122 | 46 | 0.693 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 163,992 | 3.280 | 20 | 200 | fits | 164,096 | 146 | 0.618 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 529,338 | 10.587 | 20 | 200 | fits | 89,685 | 57 | 0.665 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 161,863 | 3.237 | 20 | 20 | fits | 164,096 | 146 | 0.618 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 689,636 | 13.793 | 20 | 20 | fits | 81,122 | 46 | 0.693 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 163,655 | 3.273 | 20 | 24 | fits | 164,096 | 146 | 0.618 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,104,504 | 22.090 | 20 | 24 | MISS T_svc | 40,466 | 31 | 0.728 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 163,135 | 3.263 | 20 | 50 | fits | 164,096 | 146 | 0.618 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 528,590 | 10.572 | 20 | 50 | fits | 89,685 | 57 | 0.665 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 438,873 | 8.777 | 18 | 18 | fits | 119,217 | 85 | 0.685 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,159,929 | 23.199 | 18 | 18 | MISS ceiling | 28,042 | 18 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 365,834 | 7.317 | 20 | 20 | fits | 130,166 | 95 | 0.684 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 92,179 | 1.844 | 20 | 200 | fits | 94,520 | 140 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 479,875 | 9.597 | 20 | 200 | fits | 130,166 | 95 | 0.684 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 92,635 | 1.853 | 20 | 20 | fits | 94,520 | 140 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 667,356 | 13.347 | 20 | 20 | fits | 93,214 | 46 | 0.702 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 94,428 | 1.889 | 20 | 24 | fits | 94,520 | 140 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,201,199 | 24.024 | 20 | 24 | MISS ceiling | 54,029 | 37 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 93,908 | 1.878 | 20 | 50 | fits | 94,520 | 140 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 481,713 | 9.634 | 20 | 50 | fits | 130,166 | 95 | 0.684 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 244,837 | 4.897 | 18 | 18 | fits | 151,157 | 140 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,278,803 | 25.576 | 18 | 18 | MISS ceiling | 39,110 | 18 | 0.765 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 13,503 | 0.270 | 20 | 20 | fits | 37,505 | 21 | 0.762 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 92,179 | 1.844 | 20 | 200 | fits | 94,520 | 140 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 45,155 | 0.903 | 20 | 200 | fits | 37,505 | 21 | 0.762 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 92,635 | 1.853 | 20 | 20 | fits | 94,520 | 140 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 650,822 | 13.016 | 20 | 20 | fits | 94,497 | 50 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 94,428 | 1.889 | 20 | 24 | fits | 94,520 | 140 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,176,167 | 23.523 | 20 | 24 | MISS T_svc | 59,342 | 48 | 0.755 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 93,908 | 1.878 | 20 | 50 | fits | 94,520 | 140 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 464,082 | 9.282 | 20 | 50 | fits | 112,535 | 85 | 0.683 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 244,837 | 4.897 | 18 | 18 | fits | 151,157 | 140 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,283,078 | 25.662 | 18 | 18 | MISS ceiling | 28,912 | 15 | 0.805 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 3,320,608 | 66.412 | 20 | 20 | MISS ceiling | 51,722 | 33 | 0.674 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,037,319 | 360.746 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,037,281 | 360.746 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,037,244 | 360.745 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,037,206 | 360.744 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 101,400 | 2.028 | 20 | 200 | fits | 93,383 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 448,417 | 8.968 | 20 | 200 | fits | 110,767 | 75 | 0.695 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 99,271 | 1.985 | 20 | 20 | fits | 93,383 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 614,003 | 12.280 | 20 | 20 | fits | 82,817 | 35 | 0.773 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 101,063 | 2.021 | 20 | 24 | fits | 93,383 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 3,435,291 | 68.706 | 20 | 24 | MISS ceiling | 26,349 | 23 | 0.587 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 100,543 | 2.011 | 20 | 50 | fits | 93,383 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 447,669 | 8.953 | 20 | 50 | fits | 110,767 | 75 | 0.695 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 250,385 | 5.008 | 18 | 18 | fits | 150,069 | 133 | 0.659 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,092,380 | 21.848 | 18 | 18 | MISS ceiling | 39,166 | 21 | 0.765 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
