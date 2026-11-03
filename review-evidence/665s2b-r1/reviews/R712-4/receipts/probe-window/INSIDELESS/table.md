### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 33 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-c5.adp_available.if0` (backlog-adp@blank-c5) | 4.737 (6.014) | fits | 7 adp | 3 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-c1.service.acmp.first.if0` (backlog-adp@blank-c1) | 1.279 | fits | 0 acmp | 3 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-c5.service.acmp.last.if0` (backlog-adp@blank-c5) | 8.340 | fits | 11 acmp | 3 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-c1.service.adp.first.if0` (backlog-adp@blank-c1) | 1.270 | fits | 0 adp | 3 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-c5.service.adp.last.if0` (backlog-adp@blank-c5) | 5.889 | fits | 7 adp | 3 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-c1.service.aecp.first.if0` (backlog-adp@blank-c1) | 1.315 | fits | 0 aecp | 3 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@blank-c3.service.aecp.last.if1` (backlog-adp@blank-c3) | 15.289 | fits | 15 aecp | 3 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-c1.service.maap.first.if0` (backlog-adp@blank-c1) | 1.305 | fits | 0 maap | 3 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-c5.service.maap.last.if0` (backlog-adp@blank-c5) | 5.926 | fits | 6 maap | 3 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-c1.service.srp.first.if0` (backlog-adp@blank-c1) | 3.190 | fits | 0 srp | 3 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-c5.service.srp.last.if1` (backlog-adp@blank-c5) | 16.550 | fits | 31 srp | 3 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-c1 | 0 | 17.914 | 19 | 188,950 (1.889) | yes | - |
| backlog-adp@blank-c3 | 0 | 16.944 | 18 | 188,969 (1.890) | yes | - |
| backlog-adp@blank-c5 | 0 | 17.206 | 19 | 189,190 (1.892) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-c1 | 551 | 0 | 188,950 (1.889) | fits |
| backlog-adp@blank-c3 | 577 | 0 | 188,969 (1.890) | fits |
| backlog-adp@blank-c5 | 606 | 0 | 189,190 (1.892) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-c1 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-c3 | 334 | 102,374 (1.024) | 35,020 (0.350) |
| backlog-adp@blank-c5 | 334 | 102,374 (1.024) | 35,020 (0.350) |

Longest pass that carries a step: 102,374 CPU cycles (1.024 ms), backlog-adp@blank-c1; longest step: 76,232 (0.762 ms), backlog-adp@blank-c1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c1.adp_available.if0` | 473,582 | 4.736 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-c1.service.adp.first.if0` | 127,011 | 1.270 | 20 | 200 | fits | 118,677 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-c1.service.adp.last.if0` | 588,660 | 5.887 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c1.service.acmp.first.if0` | 127,923 | 1.279 | 20 | 20 | fits | 118,677 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c1.service.acmp.last.if0` | 833,879 | 8.339 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c1.service.aecp.first.if0` | 131,508 | 1.315 | 20 | 24 | fits | 118,677 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-c1.service.aecp.last.if1` | 1,518,097 | 15.181 | 20 | 24 | fits | 67,827 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c1.service.maap.first.if0` | 130,468 | 1.305 | 20 | 50 | fits | 118,677 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c1.service.maap.last.if0` | 592,336 | 5.923 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-c1.service.srp.first.if0` | 318,963 | 3.190 | 18 | 18 | fits | 188,950 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-c1.service.srp.last.if1` | 1,654,866 | 16.549 | 18 | 18 | fits | 36,745 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c3.adp_available.if0` | 471,668 | 4.717 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-c3.service.adp.first.if0` | 125,038 | 1.250 | 20 | 200 | fits | 118,640 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-c3.service.adp.last.if0` | 586,746 | 5.867 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c3.service.acmp.first.if0` | 125,950 | 1.260 | 20 | 20 | fits | 118,640 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c3.service.acmp.last.if0` | 831,965 | 8.320 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c3.service.aecp.first.if0` | 129,535 | 1.295 | 20 | 24 | fits | 118,640 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-c3.service.aecp.last.if1` | 1,528,918 | 15.289 | 20 | 24 | fits | 67,625 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c3.service.maap.first.if0` | 128,495 | 1.285 | 20 | 50 | fits | 118,640 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c3.service.maap.last.if0` | 590,422 | 5.904 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-c3.service.srp.first.if0` | 317,009 | 3.170 | 18 | 18 | fits | 188,969 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-c3.service.srp.last.if1` | 1,628,487 | 16.285 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c5.adp_available.if0` | 473,746 | 4.737 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-c5.service.adp.first.if0` | 126,761 | 1.268 | 20 | 200 | fits | 118,638 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-c5.service.adp.last.if0` | 588,901 | 5.889 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c5.service.acmp.first.if0` | 127,673 | 1.277 | 20 | 20 | fits | 118,638 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c5.service.acmp.last.if0` | 833,969 | 8.340 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c5.service.aecp.first.if0` | 131,258 | 1.313 | 20 | 24 | fits | 118,638 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-c5.service.aecp.last.if1` | 1,518,225 | 15.182 | 20 | 24 | fits | 67,827 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c5.service.maap.first.if0` | 130,218 | 1.302 | 20 | 50 | fits | 118,638 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c5.service.maap.last.if0` | 592,577 | 5.926 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-c5.service.srp.first.if0` | 318,953 | 3.190 | 18 | 18 | fits | 189,190 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-c5.service.srp.last.if1` | 1,654,994 | 16.550 | 18 | 18 | fits | 36,745 | 15 | 0.766 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
