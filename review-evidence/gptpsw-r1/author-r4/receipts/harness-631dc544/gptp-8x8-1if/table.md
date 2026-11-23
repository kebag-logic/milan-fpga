### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 19 paths and 7 of 59 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.086 (5.491) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.267 (6.167) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.152 (0.557) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.657 (2.174) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.495 (63.720) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.426 (64.667) | MISS ceiling | 11 acmp | 4 | 4 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-master) | 0.309 (0.652) | fits | 0 gptp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.277 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.453 | MISS ceiling | 11 acmp | 4 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.326 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.108 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.669 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.123 | MISS ceiling | 15 aecp | 4 | 1 |
| GPTP record released under the composed load, first | 0 | `backlog.service.gptp.first.if0` (backlog) | 4.283 | fits | 0 gptp | 4 | 0 |
| GPTP record released under the composed load, last | 0 | `backlog-adp.service.gptp.last.if0` (backlog-adp) | 6.115 | fits | 6 gptp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.309 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.151 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 7.463 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 10.193 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.623 | 8 | 154,075 (1.541) | yes | - |
| backlog-adp | 0 | 10.793 | 9 | 155,472 (1.555) | yes | - |
| backlog-adp-refill | 0 | 40.913 | 32 | 155,472 (1.555) | yes | - |
| backlog-owed | 0 | 65.189 | 23 | 167,518 (1.675) | yes | - |

Composed maximum over the 4 backlog windows: 167,518 CPU cycles (1.675 ms), backlog-owed.
Over the windows that released their whole load only: 167,518 (1.675 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 951 | 0 | 154,075 (1.541) | fits |
| backlog-adp | 989 | 0 | 155,472 (1.555) | fits |
| backlog-adp-refill | 1012 | 0 | 155,472 (1.555) | fits |
| backlog-owed | 986 | 0 | 167,518 (1.675) | fits |
| gptp-slave | 606 | 0 | 93,555 (0.936) | fits |
| gptp-master | 595 | 0 | 84,490 (0.845) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 265 | 30,503 (0.305) | 2,532 (0.025) |
| backlog-adp | 271 | 30,503 (0.305) | 2,532 (0.025) |
| backlog-adp-refill | 274 | 30,503 (0.305) | 2,532 (0.025) |
| backlog-owed | 277 | 30,503 (0.305) | 2,532 (0.025) |
| gptp-slave | 165 | 30,220 (0.302) | 2,484 (0.025) |
| gptp-master | 165 | 30,221 (0.302) | 2,532 (0.025) |

Longest pass that carries a step: 30,503 CPU cycles (0.305 ms), backlog; longest step: 2,532 (0.025 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 165,704 | 1.657 | 20 | 200 | fits | 63,321 | 78 | 0.568 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 508,589 | 5.086 | 20 | 20 | fits | 108,108 | 136 | 0.359 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 432,595 | 4.326 | 20 | 200 | fits | 152,854 | 130 | 0.427 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 548,243 | 5.482 | 20 | 200 | fits | 108,108 | 136 | 0.359 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 427,699 | 4.277 | 20 | 20 | fits | 152,854 | 130 | 0.427 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 543,127 | 5.431 | 20 | 20 | fits | 108,108 | 136 | 0.359 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 153,184 | 1.532 | 20 | 24 | fits | 154,075 | 158 | 0.389 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 430,923 | 4.309 | 20 | 24 | fits | 152,854 | 130 | 0.427 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 430,857 | 4.309 | 20 | 50 | fits | 152,854 | 130 | 0.427 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 546,725 | 5.467 | 20 | 50 | fits | 108,108 | 136 | 0.359 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 546,659 | 5.467 | 20 | 20 | fits | 108,108 | 136 | 0.359 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 605,300 | 6.053 | 20 | 20 | fits | 26,086 | 42 | 0.158 |
| GPTP record released under the composed load, first | `backlog.service.gptp.first.if0` | 428,267 | 4.283 | 10 | 10 | fits | 152,854 | 130 | 0.427 |
| GPTP record released under the composed load, last | `backlog.service.gptp.last.if0` | 544,039 | 5.440 | 10 | 10 | fits | 108,108 | 136 | 0.359 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 526,695 | 5.267 | 20 | 20 | fits | 149,476 | 164 | 0.523 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 296,589 | 2.966 | 20 | 200 | fits | 152,217 | 175 | 0.469 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 610,801 | 6.108 | 20 | 200 | fits | 149,476 | 164 | 0.523 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 298,087 | 2.981 | 20 | 20 | fits | 152,217 | 175 | 0.469 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 612,079 | 6.121 | 20 | 20 | fits | 149,476 | 164 | 0.523 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,510 | 1.495 | 20 | 24 | fits | 149,696 | 155 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 300,737 | 3.007 | 20 | 24 | fits | 152,217 | 175 | 0.469 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 300,671 | 3.007 | 20 | 50 | fits | 152,217 | 175 | 0.469 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 615,103 | 6.151 | 20 | 50 | fits | 149,476 | 164 | 0.523 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 746,306 | 7.463 | 20 | 20 | fits | 131,269 | 56 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,019,311 | 10.193 | 20 | 20 | fits | 134,941 | 57 | 0.694 |
| GPTP record released under the composed load, first | `backlog-adp.service.gptp.first.if0` | 297,169 | 2.972 | 10 | 10 | fits | 152,217 | 175 | 0.469 |
| GPTP record released under the composed load, last | `backlog-adp.service.gptp.last.if0` | 611,505 | 6.115 | 10 | 10 | fits | 149,476 | 164 | 0.523 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,191 | 0.152 | 20 | 20 | fits | 32,019 | 20 | 0.755 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 296,589 | 2.966 | 20 | 200 | fits | 152,217 | 175 | 0.469 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 37,494 | 0.375 | 20 | 200 | fits | 32,019 | 20 | 0.755 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 298,087 | 2.981 | 20 | 20 | fits | 152,217 | 175 | 0.469 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 597,768 | 5.978 | 20 | 20 | fits | 135,165 | 155 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,510 | 1.495 | 20 | 24 | fits | 149,696 | 155 | 0.377 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 300,737 | 3.007 | 20 | 24 | fits | 152,217 | 175 | 0.469 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 300,671 | 3.007 | 20 | 50 | fits | 152,217 | 175 | 0.469 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 600,792 | 6.008 | 20 | 50 | fits | 135,165 | 155 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 731,476 | 7.315 | 20 | 20 | fits | 130,750 | 56 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,004,545 | 10.045 | 20 | 20 | fits | 134,941 | 57 | 0.694 |
| GPTP record released under the composed load, first | `backlog-adp-refill.service.gptp.first.if0` | 297,169 | 2.972 | 10 | 10 | fits | 152,217 | 175 | 0.469 |
| GPTP record released under the composed load, last | `backlog-adp-refill.service.gptp.last.if0` | 597,194 | 5.972 | 10 | 10 | fits | 135,165 | 155 | 0.480 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,349,458 | 63.495 | 20 | 20 | MISS ceiling | 22,166 | 14 | 0.386 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,371,558 | 63.716 | 20 | 20 | MISS ceiling | 22,164 | 14 | 0.362 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,393,642 | 63.936 | 20 | 20 | MISS ceiling | 22,141 | 14 | 0.354 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,421,684 | 64.217 | 20 | 20 | MISS ceiling | 27,436 | 20 | 0.688 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,442,611 | 64.426 | 20 | 20 | MISS ceiling | 22,958 | 14 | 0.377 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 167,593 | 1.676 | 20 | 200 | fits | 167,518 | 183 | 0.500 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 459,048 | 4.590 | 20 | 200 | fits | 136,796 | 100 | 0.661 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 162,697 | 1.627 | 20 | 20 | fits | 167,518 | 183 | 0.500 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,245,305 | 62.453 | 20 | 20 | MISS ceiling | 37,107 | 16 | 0.687 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 166,911 | 1.669 | 20 | 24 | fits | 167,518 | 183 | 0.500 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,212,258 | 62.123 | 20 | 24 | MISS ceiling | 159,557 | 149 | 0.431 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 165,855 | 1.659 | 20 | 50 | fits | 167,518 | 183 | 0.500 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 457,530 | 4.575 | 20 | 50 | fits | 136,796 | 100 | 0.661 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 457,464 | 4.575 | 20 | 20 | fits | 136,796 | 100 | 0.661 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 798,186 | 7.982 | 20 | 20 | fits | 72,923 | 37 | 0.732 |
| GPTP record released under the composed load, first | `backlog-owed.service.gptp.first.if0` | 163,265 | 1.633 | 10 | 10 | fits | 167,518 | 183 | 0.500 |
| GPTP record released under the composed load, last | `backlog-owed.service.gptp.last.if0` | 454,844 | 4.548 | 10 | 10 | fits | 136,796 | 100 | 0.661 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 21,682 | 0.217 | 10 | 10 | fits | 31,109 | 16 | 0.715 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 30,882 | 0.309 | 10 | 10 | fits | 31,360 | 16 | 0.729 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
