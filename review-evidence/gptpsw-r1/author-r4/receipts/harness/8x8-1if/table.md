### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 19 paths and 7 of 59 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.054 (5.475) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.423 (6.121) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.181 (0.574) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.655 (2.192) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.576 (63.925) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.541 (64.894) | MISS ceiling | 11 acmp | 4 | 4 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-slave) | 0.289 (0.644) | fits | 0 gptp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.298 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.510 | MISS ceiling | 11 acmp | 4 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.347 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.061 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.787 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.182 | MISS ceiling | 15 aecp | 4 | 1 |
| GPTP record released under the composed load, first | 0 | `backlog.service.gptp.first.if0` (backlog) | 4.304 | fits | 0 gptp | 4 | 0 |
| GPTP record released under the composed load, last | 0 | `backlog-adp.service.gptp.last.if0` (backlog-adp) | 6.068 | fits | 6 gptp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.330 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.104 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 7.401 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 10.630 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.605 | 8 | 154,398 (1.544) | yes | - |
| backlog-adp | 0 | 11.836 | 12 | 152,764 (1.528) | yes | - |
| backlog-adp-refill | 0 | 40.938 | 32 | 152,764 (1.528) | yes | - |
| backlog-owed | 0 | 65.295 | 24 | 166,641 (1.666) | yes | - |

Composed maximum over the 4 backlog windows: 166,641 CPU cycles (1.666 ms), backlog-owed.
Over the windows that released their whole load only: 166,641 (1.666 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 951 | 0 | 154,398 (1.544) | fits |
| backlog-adp | 992 | 0 | 152,764 (1.528) | fits |
| backlog-adp-refill | 1012 | 0 | 152,764 (1.528) | fits |
| backlog-owed | 987 | 0 | 166,641 (1.666) | fits |
| gptp-slave | 604 | 0 | 93,588 (0.936) | fits |
| gptp-master | 595 | 0 | 84,346 (0.843) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 265 | 31,006 (0.310) | 2,552 (0.026) |
| backlog-adp | 271 | 31,006 (0.310) | 2,552 (0.026) |
| backlog-adp-refill | 274 | 31,006 (0.310) | 2,552 (0.026) |
| backlog-owed | 277 | 31,006 (0.310) | 2,552 (0.026) |
| gptp-slave | 165 | 31,151 (0.312) | 2,600 (0.026) |
| gptp-master | 165 | 31,000 (0.310) | 2,600 (0.026) |

Longest pass that carries a step: 31,151 CPU cycles (0.312 ms), gptp-slave; longest step: 2,600 (0.026 ms), gptp-slave.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 165,533 | 1.655 | 20 | 200 | fits | 64,829 | 78 | 0.586 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 505,422 | 5.054 | 20 | 20 | fits | 103,041 | 133 | 0.295 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 434,746 | 4.347 | 20 | 200 | fits | 151,430 | 134 | 0.350 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 546,661 | 5.467 | 20 | 200 | fits | 103,041 | 133 | 0.295 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 429,850 | 4.298 | 20 | 20 | fits | 151,430 | 134 | 0.350 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 541,545 | 5.415 | 20 | 20 | fits | 103,041 | 133 | 0.295 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 153,507 | 1.535 | 20 | 24 | fits | 154,398 | 158 | 0.398 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 433,074 | 4.331 | 20 | 24 | fits | 151,430 | 134 | 0.350 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 433,008 | 4.330 | 20 | 50 | fits | 151,430 | 134 | 0.350 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 545,143 | 5.451 | 20 | 50 | fits | 103,041 | 133 | 0.295 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 545,077 | 5.451 | 20 | 20 | fits | 103,041 | 133 | 0.295 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 602,951 | 6.030 | 20 | 20 | fits | 25,600 | 42 | 0.131 |
| GPTP record released under the composed load, first | `backlog.service.gptp.first.if0` | 430,418 | 4.304 | 10 | 10 | fits | 151,430 | 134 | 0.350 |
| GPTP record released under the composed load, last | `backlog.service.gptp.last.if0` | 542,457 | 5.425 | 10 | 10 | fits | 103,041 | 133 | 0.295 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 542,341 | 5.423 | 20 | 20 | fits | 146,839 | 144 | 0.502 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 297,182 | 2.972 | 20 | 200 | fits | 152,280 | 175 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 606,125 | 6.061 | 20 | 200 | fits | 146,839 | 144 | 0.502 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 298,680 | 2.987 | 20 | 20 | fits | 152,280 | 175 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 607,403 | 6.074 | 20 | 20 | fits | 146,839 | 144 | 0.502 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 150,040 | 1.500 | 20 | 24 | fits | 150,226 | 155 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 301,330 | 3.013 | 20 | 24 | fits | 152,280 | 175 | 0.467 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 301,264 | 3.013 | 20 | 50 | fits | 152,280 | 175 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 610,427 | 6.104 | 20 | 50 | fits | 146,839 | 144 | 0.502 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 740,123 | 7.401 | 20 | 20 | fits | 129,762 | 58 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,063,020 | 10.630 | 20 | 20 | fits | 52,194 | 21 | 0.781 |
| GPTP record released under the composed load, first | `backlog-adp.service.gptp.first.if0` | 297,762 | 2.978 | 10 | 10 | fits | 152,280 | 175 | 0.467 |
| GPTP record released under the composed load, last | `backlog-adp.service.gptp.last.if0` | 606,829 | 6.068 | 10 | 10 | fits | 146,839 | 144 | 0.502 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 18,123 | 0.181 | 20 | 20 | fits | 32,365 | 20 | 0.761 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 297,182 | 2.972 | 20 | 200 | fits | 152,280 | 175 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 39,641 | 0.396 | 20 | 200 | fits | 32,365 | 20 | 0.761 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 298,680 | 2.987 | 20 | 20 | fits | 152,280 | 175 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 592,608 | 5.926 | 20 | 20 | fits | 132,044 | 134 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 150,040 | 1.500 | 20 | 24 | fits | 150,226 | 155 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 301,330 | 3.013 | 20 | 24 | fits | 152,280 | 175 | 0.467 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 301,264 | 3.013 | 20 | 50 | fits | 152,280 | 175 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 595,632 | 5.956 | 20 | 50 | fits | 132,044 | 134 | 0.457 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 724,704 | 7.247 | 20 | 20 | fits | 129,138 | 58 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,049,717 | 10.497 | 20 | 20 | fits | 54,307 | 25 | 0.747 |
| GPTP record released under the composed load, first | `backlog-adp-refill.service.gptp.first.if0` | 297,762 | 2.978 | 10 | 10 | fits | 152,280 | 175 | 0.467 |
| GPTP record released under the composed load, last | `backlog-adp-refill.service.gptp.last.if0` | 592,034 | 5.920 | 10 | 10 | fits | 132,044 | 134 | 0.457 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,357,597 | 63.576 | 20 | 20 | MISS ceiling | 22,570 | 14 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,380,107 | 63.801 | 20 | 20 | MISS ceiling | 22,586 | 14 | 0.426 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,408,786 | 64.088 | 20 | 20 | MISS ceiling | 27,975 | 20 | 0.709 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,430,229 | 64.302 | 20 | 20 | MISS ceiling | 23,650 | 14 | 0.492 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,454,103 | 64.541 | 20 | 20 | MISS ceiling | 23,015 | 14 | 0.550 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 179,421 | 1.794 | 20 | 200 | fits | 166,641 | 183 | 0.486 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 467,741 | 4.677 | 20 | 200 | fits | 138,916 | 89 | 0.637 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 174,525 | 1.745 | 20 | 20 | fits | 166,641 | 183 | 0.486 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,251,027 | 62.510 | 20 | 20 | MISS ceiling | 36,899 | 16 | 0.661 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 178,739 | 1.787 | 20 | 24 | fits | 166,641 | 183 | 0.486 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,218,188 | 62.182 | 20 | 24 | MISS ceiling | 148,126 | 110 | 0.417 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 177,683 | 1.777 | 20 | 50 | fits | 166,641 | 183 | 0.486 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 466,223 | 4.662 | 20 | 50 | fits | 138,916 | 89 | 0.637 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 466,157 | 4.662 | 20 | 20 | fits | 138,916 | 89 | 0.637 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 824,002 | 8.240 | 20 | 20 | fits | 96,318 | 45 | 0.748 |
| GPTP record released under the composed load, first | `backlog-owed.service.gptp.first.if0` | 175,093 | 1.751 | 10 | 10 | fits | 166,641 | 183 | 0.486 |
| GPTP record released under the composed load, last | `backlog-owed.service.gptp.last.if0` | 463,537 | 4.635 | 10 | 10 | fits | 138,916 | 89 | 0.637 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 28,899 | 0.289 | 10 | 10 | fits | 32,444 | 16 | 0.742 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 18,536 | 0.185 | 10 | 10 | fits | 32,734 | 16 | 0.752 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
