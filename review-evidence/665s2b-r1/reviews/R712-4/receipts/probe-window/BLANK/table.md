### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 44 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-b1.adp_available.if0` (backlog-adp@blank-b1) | 5.253 (6.837) | fits | 7 adp | 4 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-b2.service.acmp.first.if0` (backlog-adp@blank-b2) | 1.282 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-b1.service.acmp.last.if0` (backlog-adp@blank-b1) | 9.143 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-b2.service.adp.first.if0` (backlog-adp@blank-b2) | 1.273 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-b1.service.adp.last.if0` (backlog-adp@blank-b1) | 6.700 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-b2.service.aecp.first.if0` (backlog-adp@blank-b2) | 1.318 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@blank-b0.service.aecp.last.if1` (backlog-adp@blank-b0) | 16.030 | fits | 15 aecp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-b2.service.maap.first.if0` (backlog-adp@blank-b2) | 1.307 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-b1.service.maap.last.if0` (backlog-adp@blank-b1) | 6.737 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-b1.service.srp.first.if0` (backlog-adp@blank-b1) | 4.406 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-b1.service.srp.last.if1` (backlog-adp@blank-b1) | 17.276 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-b0 | 0 | 18.485 | 20 | 184,027 (1.840) | yes | - |
| backlog-adp@blank-b1 | 0 | 19.136 | 20 | 190,446 (1.904) | yes | - |
| backlog-adp@blank-b2 | 0 | 17.859 | 18 | 166,368 (1.664) | yes | - |
| backlog-adp@blank-b3 | 1 | 18.882 | 18 | 190,076 (1.901) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-b0 | 576 | 0 | 184,027 (1.840) | fits |
| backlog-adp@blank-b1 | 613 | 0 | 190,446 (1.904) | fits |
| backlog-adp@blank-b2 | 644 | 0 | 166,368 (1.664) | fits |
| backlog-adp@blank-b3 | 681 | 0 | 190,076 (1.901) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-b0 | 337 | 102,374 (1.024) | 76,395 (0.764) |
| backlog-adp@blank-b1 | 338 | 102,374 (1.024) | 76,516 (0.765) |
| backlog-adp@blank-b2 | 338 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-b3 | 339 | 102,374 (1.024) | 76,231 (0.762) |

Longest pass that carries a step: 102,374 CPU cycles (1.024 ms), backlog-adp@blank-b0; longest step: 76,516 (0.765 ms), backlog-adp@blank-b1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-b0.adp_available.if0` | 442,509 | 4.425 | 20 | 20 | fits | 156,407 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-b0.service.adp.first.if0` | 125,976 | 1.260 | 20 | 200 | fits | 118,759 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-b0.service.adp.last.if0` | 587,210 | 5.872 | 20 | 200 | fits | 156,407 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-b0.service.acmp.first.if0` | 126,888 | 1.269 | 20 | 20 | fits | 118,759 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-b0.service.acmp.last.if0` | 831,363 | 8.314 | 20 | 20 | fits | 121,100 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-b0.service.aecp.first.if0` | 130,473 | 1.305 | 20 | 24 | fits | 118,759 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-b0.service.aecp.last.if1` | 1,602,986 | 16.030 | 20 | 24 | fits | 67,358 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@blank-b0.service.maap.first.if0` | 129,433 | 1.294 | 20 | 50 | fits | 118,759 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-b0.service.maap.last.if0` | 590,886 | 5.909 | 20 | 50 | fits | 156,407 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-b0.service.srp.first.if0` | 434,414 | 4.344 | 18 | 18 | fits | 184,027 | 104 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@blank-b0.service.srp.last.if1` | 1,702,577 | 17.026 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-b1.adp_available.if0` | 525,278 | 5.253 | 20 | 20 | fits | 156,120 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-b1.service.adp.first.if0` | 125,745 | 1.257 | 20 | 200 | fits | 118,748 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-b1.service.adp.last.if0` | 670,038 | 6.700 | 20 | 200 | fits | 156,120 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-b1.service.acmp.first.if0` | 126,657 | 1.267 | 20 | 20 | fits | 118,748 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-b1.service.acmp.last.if0` | 914,316 | 9.143 | 20 | 20 | fits | 121,158 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-b1.service.aecp.first.if0` | 130,242 | 1.302 | 20 | 24 | fits | 118,748 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-b1.service.aecp.last.if1` | 1,577,704 | 15.777 | 20 | 24 | fits | 67,441 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-b1.service.maap.first.if0` | 129,202 | 1.292 | 20 | 50 | fits | 118,748 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-b1.service.maap.last.if0` | 673,714 | 6.737 | 20 | 50 | fits | 156,120 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-b1.service.srp.first.if0` | 440,608 | 4.406 | 18 | 18 | fits | 190,446 | 110 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp@blank-b1.service.srp.last.if1` | 1,727,626 | 17.276 | 18 | 18 | fits | 50,155 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-b2.adp_available.if0` | 476,875 | 4.769 | 20 | 20 | fits | 161,915 | 89 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@blank-b2.service.adp.first.if0` | 127,270 | 1.273 | 20 | 200 | fits | 118,665 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-b2.service.adp.last.if0` | 620,585 | 6.206 | 20 | 200 | fits | 161,915 | 89 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@blank-b2.service.acmp.first.if0` | 128,182 | 1.282 | 20 | 20 | fits | 118,665 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-b2.service.acmp.last.if0` | 864,231 | 8.642 | 20 | 20 | fits | 120,938 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@blank-b2.service.aecp.first.if0` | 131,767 | 1.318 | 20 | 24 | fits | 118,665 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-b2.service.aecp.last.if1` | 1,549,088 | 15.491 | 20 | 24 | fits | 74,633 | 37 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@blank-b2.service.maap.first.if0` | 130,727 | 1.307 | 20 | 50 | fits | 118,665 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-b2.service.maap.last.if0` | 624,261 | 6.243 | 20 | 50 | fits | 161,915 | 89 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@blank-b2.service.srp.first.if0` | 295,913 | 2.959 | 18 | 18 | fits | 165,641 | 147 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-b2.service.srp.last.if1` | 1,648,991 | 16.490 | 18 | 18 | fits | 50,387 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-b3.adp_available.if0` | 471,404 | 4.714 | 20 | 20 | fits | 154,955 | 83 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@blank-b3.service.adp.first.if0` | 112,565 | 1.126 | 20 | 200 | fits | 118,595 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-b3.service.adp.last.if0` | 615,006 | 6.150 | 20 | 200 | fits | 154,955 | 83 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@blank-b3.service.acmp.first.if0` | 113,477 | 1.135 | 20 | 20 | fits | 118,595 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-b3.service.acmp.last.if0` | 854,020 | 8.540 | 20 | 20 | fits | 129,336 | 52 | 0.697 |
| AECP record released under the composed load, first | `backlog-adp@blank-b3.service.aecp.first.if0` | 117,062 | 1.171 | 20 | 24 | fits | 118,595 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-b3.service.aecp.last.if1` | 1,545,043 | 15.450 | 20 | 24 | fits | 67,573 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@blank-b3.service.maap.first.if0` | 116,022 | 1.160 | 20 | 50 | fits | 118,595 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-b3.service.maap.last.if0` | 618,682 | 6.187 | 20 | 50 | fits | 154,955 | 83 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@blank-b3.service.srp.first.if0` | 305,643 | 3.056 | 18 | 18 | fits | 190,076 | 145 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-b3.service.srp.last.if1` | 1,631,651 | 16.317 | 18 | 18 | fits | 36,987 | 15 | 0.774 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
