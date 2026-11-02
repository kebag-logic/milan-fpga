### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 44 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-7.adp_available.if0` (backlog-adp@blank-7) | 4.907 (6.530) | fits | 7 adp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-1.service.acmp.first.if0` (backlog-adp@verify-1) | 1.318 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-7.service.acmp.last.if0` (backlog-adp@blank-7) | 8.768 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-1.service.adp.first.if0` (backlog-adp@verify-1) | 1.308 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-7.service.adp.last.if0` (backlog-adp@blank-7) | 6.339 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-1.service.aecp.first.if0` (backlog-adp@verify-1) | 1.353 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@blank-7.service.aecp.last.if1` (backlog-adp@blank-7) | 15.743 | fits | 15 aecp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-1.service.maap.first.if0` (backlog-adp@verify-1) | 1.343 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-7.service.maap.last.if0` (backlog-adp@blank-7) | 6.375 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 5.425 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-1.service.srp.last.if1` (backlog-adp@verify-1) | 16.848 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-7 | 0 | 17.611 | 17 | 194,404 (1.944) | yes | - |
| backlog-adp@program-3 | 0 | 18.265 | 19 | 181,494 (1.815) | yes | - |
| backlog-adp@verify-1 | 0 | 19.553 | 20 | 182,735 (1.827) | yes | - |
| backlog-adp | 0 | 17.190 | 20 | 196,295 (1.963) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill, backlog-owed not run): 196,295 CPU cycles (1.963 ms), backlog-adp.
Over the windows that released their whole load only: 196,295 (1.963 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-7 | 484 | 0 | 194,404 (1.944) | fits |
| backlog-adp@program-3 | 760 | 0 | 181,494 (1.815) | fits |
| backlog-adp@verify-1 | 1016 | 0 | 182,735 (1.827) | fits |
| save | 617 | 0 | 132,078 (1.321) | fits |
| backlog-adp | 322 | 0 | 196,295 (1.963) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 490,676 | 4.907 | 20 | 20 | fits | 166,102 | 101 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 127,819 | 1.278 | 20 | 200 | fits | 118,805 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 633,870 | 6.339 | 20 | 200 | fits | 166,102 | 101 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 128,731 | 1.287 | 20 | 20 | fits | 118,805 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 876,812 | 8.768 | 20 | 20 | fits | 120,656 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 132,316 | 1.323 | 20 | 24 | fits | 118,805 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,574,251 | 15.743 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 131,276 | 1.313 | 20 | 50 | fits | 118,805 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 637,546 | 6.375 | 20 | 50 | fits | 166,102 | 101 | 0.681 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 325,225 | 3.252 | 18 | 18 | fits | 194,404 | 145 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,623,188 | 16.232 | 18 | 18 | fits | 51,472 | 20 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 447,470 | 4.475 | 20 | 20 | fits | 156,056 | 83 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 130,547 | 1.305 | 20 | 200 | fits | 125,381 | 151 | 0.534 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 591,440 | 5.914 | 20 | 200 | fits | 156,056 | 83 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 131,459 | 1.315 | 20 | 20 | fits | 125,381 | 151 | 0.534 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 834,059 | 8.341 | 20 | 20 | fits | 120,636 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 135,044 | 1.350 | 20 | 24 | fits | 125,381 | 151 | 0.534 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,533,567 | 15.336 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 134,004 | 1.340 | 20 | 50 | fits | 125,381 | 151 | 0.534 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 595,116 | 5.951 | 20 | 50 | fits | 156,056 | 83 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 438,995 | 4.390 | 18 | 18 | fits | 181,494 | 104 | 0.660 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,633,081 | 16.331 | 18 | 18 | fits | 50,433 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 446,183 | 4.462 | 20 | 20 | fits | 156,124 | 83 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 130,841 | 1.308 | 20 | 200 | fits | 119,500 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 590,286 | 5.903 | 20 | 200 | fits | 156,124 | 83 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 131,753 | 1.318 | 20 | 20 | fits | 119,500 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 800,037 | 8.000 | 20 | 20 | fits | 87,607 | 37 | 0.639 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 135,338 | 1.353 | 20 | 24 | fits | 119,500 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,534,890 | 15.349 | 20 | 24 | fits | 68,213 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 134,298 | 1.343 | 20 | 50 | fits | 119,500 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 593,962 | 5.940 | 20 | 50 | fits | 156,124 | 83 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 437,773 | 4.378 | 18 | 18 | fits | 182,735 | 104 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,684,771 | 16.848 | 18 | 18 | fits | 50,294 | 18 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 360,180 | 3.602 | 20 | 20 | fits | 196,295 | 89 | 0.701 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 111,586 | 1.116 | 20 | 200 | fits | 116,268 | 140 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 538,849 | 5.388 | 20 | 200 | fits | 196,295 | 89 | 0.701 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 112,498 | 1.125 | 20 | 20 | fits | 116,268 | 140 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 783,380 | 7.834 | 20 | 20 | fits | 120,750 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 116,083 | 1.161 | 20 | 24 | fits | 116,268 | 140 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,469,482 | 14.695 | 20 | 24 | fits | 67,690 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 115,043 | 1.150 | 20 | 50 | fits | 116,268 | 140 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 542,525 | 5.425 | 20 | 50 | fits | 196,295 | 89 | 0.701 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 542,460 | 5.425 | 18 | 18 | fits | 196,295 | 89 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,655,570 | 16.556 | 18 | 18 | fits | 36,739 | 15 | 0.776 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
