### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 44 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-b2.adp_available.if0` (backlog-adp@blank-b2) | 4.796 (6.327) | fits | 7 adp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-b2.service.acmp.first.if0` (backlog-adp@blank-b2) | 1.309 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-b2.service.acmp.last.if0` (backlog-adp@blank-b2) | 8.669 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-b2.service.adp.first.if0` (backlog-adp@blank-b2) | 1.300 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-b2.service.adp.last.if0` (backlog-adp@blank-b2) | 6.233 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-b2.service.aecp.first.if0` (backlog-adp@blank-b2) | 1.345 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@blank-b2.service.aecp.last.if1` (backlog-adp@blank-b2) | 15.518 | fits | 15 aecp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-b2.service.maap.first.if0` (backlog-adp@blank-b2) | 1.334 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-b2.service.maap.last.if0` (backlog-adp@blank-b2) | 6.269 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-b1.service.srp.first.if0` (backlog-adp@blank-b1) | 4.406 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-b1.service.srp.last.if1` (backlog-adp@blank-b1) | 16.586 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-b0 | 0 | 18.474 | 20 | 184,027 (1.840) | yes | - |
| backlog-adp@blank-b1 | 0 | 17.955 | 19 | 190,446 (1.904) | yes | - |
| backlog-adp@blank-b2 | 0 | 17.886 | 18 | 166,368 (1.664) | yes | - |
| backlog-adp@blank-b3 | 0 | 18.903 | 19 | 189,205 (1.892) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-b0 | 576 | 0 | 184,027 (1.840) | fits |
| backlog-adp@blank-b1 | 612 | 0 | 190,446 (1.904) | fits |
| backlog-adp@blank-b2 | 648 | 0 | 166,368 (1.664) | fits |
| backlog-adp@blank-b3 | 685 | 0 | 189,205 (1.892) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-b0 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-b1 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-b2 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-b3 | 338 | 102,374 (1.024) | 76,231 (0.762) |

Longest pass that carries a step: 102,374 CPU cycles (1.024 ms), backlog-adp@blank-b0; longest step: 76,231 (0.762 ms), backlog-adp@blank-b0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-b0.adp_available.if0` | 442,509 | 4.425 | 20 | 20 | fits | 156,407 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-b0.service.adp.first.if0` | 125,976 | 1.260 | 20 | 200 | fits | 118,759 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-b0.service.adp.last.if0` | 587,210 | 5.872 | 20 | 200 | fits | 156,407 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-b0.service.acmp.first.if0` | 126,888 | 1.269 | 20 | 20 | fits | 118,759 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-b0.service.acmp.last.if0` | 831,363 | 8.314 | 20 | 20 | fits | 121,100 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-b0.service.aecp.first.if0` | 130,473 | 1.305 | 20 | 24 | fits | 118,759 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-b0.service.aecp.last.if1` | 1,525,617 | 15.256 | 20 | 24 | fits | 67,358 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@blank-b0.service.maap.first.if0` | 129,433 | 1.294 | 20 | 50 | fits | 118,759 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-b0.service.maap.last.if0` | 590,886 | 5.909 | 20 | 50 | fits | 156,407 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-b0.service.srp.first.if0` | 434,414 | 4.344 | 18 | 18 | fits | 184,027 | 104 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@blank-b0.service.srp.last.if1` | 1,625,208 | 16.252 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-b1.adp_available.if0` | 448,703 | 4.487 | 20 | 20 | fits | 156,407 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-b1.service.adp.first.if0` | 125,745 | 1.257 | 20 | 200 | fits | 118,748 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-b1.service.adp.last.if0` | 593,404 | 5.934 | 20 | 200 | fits | 156,407 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-b1.service.acmp.first.if0` | 126,657 | 1.267 | 20 | 20 | fits | 118,748 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-b1.service.acmp.last.if0` | 837,557 | 8.376 | 20 | 20 | fits | 121,100 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-b1.service.aecp.first.if0` | 130,242 | 1.302 | 20 | 24 | fits | 118,748 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-b1.service.aecp.last.if1` | 1,508,608 | 15.086 | 20 | 24 | fits | 67,363 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@blank-b1.service.maap.first.if0` | 129,202 | 1.292 | 20 | 50 | fits | 118,748 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-b1.service.maap.last.if0` | 597,080 | 5.971 | 20 | 50 | fits | 156,407 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-b1.service.srp.first.if0` | 440,608 | 4.406 | 18 | 18 | fits | 190,446 | 110 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp@blank-b1.service.srp.last.if1` | 1,658,594 | 16.586 | 18 | 18 | fits | 50,214 | 18 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-b2.adp_available.if0` | 479,564 | 4.796 | 20 | 20 | fits | 161,915 | 89 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@blank-b2.service.adp.first.if0` | 129,959 | 1.300 | 20 | 200 | fits | 118,758 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-b2.service.adp.last.if0` | 623,274 | 6.233 | 20 | 200 | fits | 161,915 | 89 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@blank-b2.service.acmp.first.if0` | 130,871 | 1.309 | 20 | 20 | fits | 118,758 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-b2.service.acmp.last.if0` | 866,920 | 8.669 | 20 | 20 | fits | 120,938 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@blank-b2.service.aecp.first.if0` | 134,456 | 1.345 | 20 | 24 | fits | 118,758 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-b2.service.aecp.last.if1` | 1,551,777 | 15.518 | 20 | 24 | fits | 74,633 | 37 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@blank-b2.service.maap.first.if0` | 133,416 | 1.334 | 20 | 50 | fits | 118,758 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-b2.service.maap.last.if0` | 626,950 | 6.269 | 20 | 50 | fits | 161,915 | 89 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@blank-b2.service.srp.first.if0` | 298,602 | 2.986 | 18 | 18 | fits | 165,641 | 147 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-b2.service.srp.last.if1` | 1,651,680 | 16.517 | 18 | 18 | fits | 50,387 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-b3.adp_available.if0` | 473,567 | 4.736 | 20 | 20 | fits | 154,955 | 83 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@blank-b3.service.adp.first.if0` | 115,599 | 1.156 | 20 | 200 | fits | 118,760 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-b3.service.adp.last.if0` | 617,169 | 6.172 | 20 | 200 | fits | 154,955 | 83 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@blank-b3.service.acmp.first.if0` | 116,511 | 1.165 | 20 | 20 | fits | 118,760 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-b3.service.acmp.last.if0` | 856,183 | 8.562 | 20 | 20 | fits | 129,336 | 52 | 0.697 |
| AECP record released under the composed load, first | `backlog-adp@blank-b3.service.aecp.first.if0` | 120,096 | 1.201 | 20 | 24 | fits | 118,760 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-b3.service.aecp.last.if1` | 1,547,206 | 15.472 | 20 | 24 | fits | 67,573 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@blank-b3.service.maap.first.if0` | 119,056 | 1.191 | 20 | 50 | fits | 118,760 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-b3.service.maap.last.if0` | 620,845 | 6.208 | 20 | 50 | fits | 154,955 | 83 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@blank-b3.service.srp.first.if0` | 307,806 | 3.078 | 18 | 18 | fits | 189,205 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-b3.service.srp.last.if1` | 1,633,814 | 16.338 | 18 | 18 | fits | 36,987 | 15 | 0.774 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
