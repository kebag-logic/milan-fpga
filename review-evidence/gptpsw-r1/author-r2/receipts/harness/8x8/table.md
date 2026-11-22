### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 20 paths and 7 of 59 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.978 (6.302) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.511 (6.430) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.296 (0.794) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.742 (2.305) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.852 (64.270) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.892 (65.304) | MISS ceiling | 11 acmp | 4 | 4 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-master) | 0.266 (0.701) | fits | 0 gptp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.515 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.557 | MISS ceiling | 11 acmp | 4 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.571 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.363 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.294 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.774 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 62.225 | MISS ceiling | 15 aecp | 4 | 1 |
| GPTP record released under the composed load, first | 0 | `backlog.service.gptp.first.if0` (backlog) | 4.528 | fits | 0 gptp | 4 | 0 |
| GPTP record released under the composed load, last | 1 | `backlog-adp.service.gptp.last.if1` (backlog-adp) | 7.945 | fits | 15 gptp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.554 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp-refill.service.maap.last.if0` (backlog-adp-refill) | 6.454 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 9.155 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 13.588 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 10.805 | 10 | 163,342 (1.633) | yes | - |
| backlog-adp | 0 | 14.315 | 13 | 163,006 (1.630) | yes | - |
| backlog-adp-refill | 0 | 41.210 | 32 | 163,006 (1.630) | yes | - |
| backlog-owed | 0 | 65.795 | 26 | 163,006 (1.630) | yes | - |

Composed maximum over the 4 backlog windows: 163,342 CPU cycles (1.633 ms), backlog.
Over the windows that released their whole load only: 163,342 (1.633 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 965 | 0 | 163,342 (1.633) | fits |
| backlog-adp | 1005 | 0 | 163,006 (1.630) | fits |
| backlog-adp-refill | 1024 | 0 | 163,006 (1.630) | fits |
| backlog-owed | 1001 | 0 | 163,006 (1.630) | fits |
| gptp-slave | 615 | 0 | 119,838 (1.198) | fits |
| gptp-master | 604 | 0 | 109,583 (1.096) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 266 | 27,383 (0.274) | 3,660 (0.037) |
| backlog-adp | 271 | 27,383 (0.274) | 3,660 (0.037) |
| backlog-adp-refill | 273 | 27,383 (0.274) | 3,660 (0.037) |
| backlog-owed | 277 | 27,859 (0.279) | 3,660 (0.037) |
| gptp-slave | 165 | 27,383 (0.274) | 3,689 (0.037) |
| gptp-master | 165 | 27,383 (0.274) | 3,660 (0.037) |

Longest pass that carries a step: 27,859 CPU cycles (0.279 ms), backlog-owed; longest step: 3,689 (0.037 ms), gptp-slave.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 174,200 | 1.742 | 20 | 200 | fits | 67,122 | 81 | 0.583 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 597,795 | 5.978 | 20 | 20 | fits | 161,660 | 161 | 0.408 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 457,131 | 4.571 | 20 | 200 | fits | 158,448 | 151 | 0.440 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 629,415 | 6.294 | 20 | 200 | fits | 161,660 | 161 | 0.408 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 451,497 | 4.515 | 20 | 20 | fits | 158,448 | 151 | 0.440 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 623,561 | 6.236 | 20 | 20 | fits | 161,660 | 161 | 0.408 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 162,451 | 1.625 | 20 | 24 | fits | 163,342 | 183 | 0.317 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 297,011 | 2.970 | 20 | 24 | fits | 68,428 | 29 | 0.688 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 455,393 | 4.554 | 20 | 50 | fits | 158,448 | 151 | 0.440 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 627,897 | 6.279 | 20 | 50 | fits | 161,660 | 161 | 0.408 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 748,022 | 7.480 | 20 | 20 | fits | 120,191 | 89 | 0.635 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,008,108 | 10.081 | 20 | 20 | fits | 49,321 | 26 | 0.706 |
| GPTP record released under the composed load, first | `backlog.service.gptp.first.if0` | 452,803 | 4.528 | 10 | 10 | fits | 158,448 | 151 | 0.440 |
| GPTP record released under the composed load, last | `backlog.service.gptp.last.if1` | 744,664 | 7.447 | 10 | 10 | fits | 120,191 | 89 | 0.635 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 551,122 | 5.511 | 20 | 20 | fits | 154,826 | 137 | 0.503 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 320,978 | 3.210 | 20 | 200 | fits | 163,006 | 207 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 636,283 | 6.363 | 20 | 200 | fits | 154,826 | 137 | 0.503 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 323,214 | 3.232 | 20 | 20 | fits | 163,006 | 207 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 795,845 | 7.958 | 20 | 20 | fits | 146,596 | 115 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 154,230 | 1.542 | 20 | 24 | fits | 154,416 | 182 | 0.291 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 325,864 | 3.259 | 20 | 24 | fits | 163,006 | 207 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 325,798 | 3.258 | 20 | 50 | fits | 163,006 | 207 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 641,323 | 6.413 | 20 | 50 | fits | 154,826 | 137 | 0.503 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 915,492 | 9.155 | 20 | 20 | fits | 116,689 | 74 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,358,786 | 13.588 | 20 | 20 | fits | 82,098 | 30 | 0.770 |
| GPTP record released under the composed load, first | `backlog-adp.service.gptp.first.if0` | 322,296 | 3.223 | 10 | 10 | fits | 163,006 | 207 | 0.441 |
| GPTP record released under the composed load, last | `backlog-adp.service.gptp.last.if1` | 794,533 | 7.945 | 10 | 10 | fits | 146,596 | 115 | 0.414 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 29,588 | 0.296 | 20 | 20 | fits | 36,003 | 21 | 0.778 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 320,978 | 3.210 | 20 | 200 | fits | 163,006 | 207 | 0.441 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 54,441 | 0.544 | 20 | 200 | fits | 36,003 | 21 | 0.778 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 323,214 | 3.232 | 20 | 20 | fits | 163,006 | 207 | 0.441 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 642,365 | 6.424 | 20 | 20 | fits | 158,892 | 143 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 154,230 | 1.542 | 20 | 24 | fits | 154,416 | 182 | 0.291 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 325,864 | 3.259 | 20 | 24 | fits | 163,006 | 207 | 0.441 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 325,798 | 3.258 | 20 | 50 | fits | 163,006 | 207 | 0.441 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 645,389 | 6.454 | 20 | 50 | fits | 158,892 | 143 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 908,443 | 9.084 | 20 | 20 | fits | 126,781 | 72 | 0.756 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,341,853 | 13.419 | 20 | 20 | fits | 71,459 | 26 | 0.779 |
| GPTP record released under the composed load, first | `backlog-adp-refill.service.gptp.first.if0` | 322,296 | 3.223 | 10 | 10 | fits | 163,006 | 207 | 0.441 |
| GPTP record released under the composed load, last | `backlog-adp-refill.service.gptp.last.if1` | 777,392 | 7.774 | 10 | 10 | fits | 125,329 | 104 | 0.383 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,385,190 | 63.852 | 20 | 20 | MISS ceiling | 26,765 | 15 | 0.554 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,411,698 | 64.117 | 20 | 20 | MISS ceiling | 26,013 | 15 | 0.439 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,437,553 | 64.376 | 20 | 20 | MISS ceiling | 25,912 | 15 | 0.455 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,463,433 | 64.634 | 20 | 20 | MISS ceiling | 25,956 | 15 | 0.455 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,489,191 | 64.892 | 20 | 20 | MISS ceiling | 25,821 | 15 | 0.472 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 178,097 | 1.781 | 20 | 200 | fits | 163,006 | 193 | 0.433 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 494,578 | 4.946 | 20 | 200 | fits | 158,299 | 115 | 0.452 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 172,463 | 1.725 | 20 | 20 | fits | 163,006 | 193 | 0.433 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,255,651 | 62.557 | 20 | 20 | MISS ceiling | 37,981 | 17 | 0.650 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 177,415 | 1.774 | 20 | 24 | fits | 163,006 | 193 | 0.433 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,222,468 | 62.225 | 20 | 24 | MISS ceiling | 151,793 | 148 | 0.374 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 176,359 | 1.764 | 20 | 50 | fits | 163,006 | 193 | 0.433 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 493,060 | 4.931 | 20 | 50 | fits | 158,299 | 115 | 0.452 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 608,098 | 6.081 | 20 | 20 | fits | 115,104 | 41 | 0.751 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,044,285 | 10.443 | 20 | 20 | fits | 82,848 | 30 | 0.779 |
| GPTP record released under the composed load, first | `backlog-owed.service.gptp.first.if0` | 173,769 | 1.738 | 10 | 10 | fits | 163,006 | 193 | 0.433 |
| GPTP record released under the composed load, last | `backlog-owed.service.gptp.last.if1` | 604,740 | 6.047 | 10 | 10 | fits | 115,104 | 41 | 0.751 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 19,030 | 0.190 | 10 | 10 | fits | 37,639 | 18 | 0.752 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 26,560 | 0.266 | 10 | 10 | fits | 37,687 | 18 | 0.745 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
