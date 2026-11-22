### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 19 paths and 7 of 59 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.928 (5.344) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.273 (6.050) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.219 (0.621) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.711 (2.240) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.476 (63.825) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.430 (64.792) | MISS ceiling | 11 acmp | 4 | 4 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-master) | 0.223 (0.578) | fits | 0 gptp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.329 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.411 | MISS ceiling | 11 acmp | 4 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.378 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.991 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.781 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.082 | MISS ceiling | 15 aecp | 4 | 1 |
| GPTP record released under the composed load, first | 0 | `backlog.service.gptp.first.if0` (backlog) | 4.335 | fits | 0 gptp | 4 | 0 |
| GPTP record released under the composed load, last | 0 | `backlog-adp.service.gptp.last.if0` (backlog-adp) | 5.998 | fits | 6 gptp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.361 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.034 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 7.407 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 10.512 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.471 | 8 | 159,844 (1.598) | yes | - |
| backlog-adp | 0 | 11.577 | 12 | 152,203 (1.522) | yes | - |
| backlog-adp-refill | 0 | 40.982 | 33 | 152,203 (1.522) | yes | - |
| backlog-owed | 0 | 65.196 | 23 | 163,367 (1.634) | yes | - |

Composed maximum over the 4 backlog windows: 163,367 CPU cycles (1.634 ms), backlog-owed.
Over the windows that released their whole load only: 163,367 (1.634 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 951 | 0 | 159,844 (1.598) | fits |
| backlog-adp | 992 | 0 | 152,203 (1.522) | fits |
| backlog-adp-refill | 1013 | 0 | 152,203 (1.522) | fits |
| backlog-owed | 986 | 0 | 163,367 (1.634) | fits |
| gptp-slave | 605 | 0 | 92,666 (0.927) | fits |
| gptp-master | 595 | 0 | 83,535 (0.835) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 265 | 30,502 (0.305) | 2,549 (0.025) |
| backlog-adp | 271 | 30,502 (0.305) | 2,549 (0.025) |
| backlog-adp-refill | 274 | 30,502 (0.305) | 2,549 (0.025) |
| backlog-owed | 277 | 30,502 (0.305) | 2,549 (0.025) |
| gptp-slave | 165 | 30,551 (0.306) | 2,549 (0.025) |
| gptp-master | 165 | 30,489 (0.305) | 2,549 (0.025) |

Longest pass that carries a step: 30,551 CPU cycles (0.306 ms), gptp-slave; longest step: 2,549 (0.025 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 171,116 | 1.711 | 20 | 200 | fits | 64,133 | 78 | 0.590 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 492,779 | 4.928 | 20 | 20 | fits | 86,684 | 119 | 0.289 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 437,813 | 4.378 | 20 | 200 | fits | 150,225 | 135 | 0.291 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 533,570 | 5.336 | 20 | 200 | fits | 86,684 | 119 | 0.289 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 432,917 | 4.329 | 20 | 20 | fits | 150,225 | 135 | 0.291 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 528,454 | 5.285 | 20 | 20 | fits | 86,684 | 119 | 0.289 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 158,953 | 1.590 | 20 | 24 | fits | 159,844 | 167 | 0.390 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 285,916 | 2.859 | 20 | 24 | fits | 63,820 | 26 | 0.707 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 436,075 | 4.361 | 20 | 50 | fits | 150,225 | 135 | 0.291 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 435,679 | 4.357 | 20 | 50 | fits | 150,225 | 135 | 0.291 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 531,986 | 5.320 | 20 | 20 | fits | 86,684 | 119 | 0.289 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 589,547 | 5.895 | 20 | 20 | fits | 25,439 | 42 | 0.107 |
| GPTP record released under the composed load, first | `backlog.service.gptp.first.if0` | 433,485 | 4.335 | 10 | 10 | fits | 150,225 | 135 | 0.291 |
| GPTP record released under the composed load, last | `backlog.service.gptp.last.if0` | 529,366 | 5.294 | 10 | 10 | fits | 86,684 | 119 | 0.289 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 527,307 | 5.273 | 20 | 20 | fits | 146,619 | 157 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 291,026 | 2.910 | 20 | 200 | fits | 149,991 | 175 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 599,053 | 5.991 | 20 | 200 | fits | 146,619 | 157 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 292,524 | 2.925 | 20 | 20 | fits | 149,991 | 175 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 600,331 | 6.003 | 20 | 20 | fits | 146,619 | 157 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 146,173 | 1.462 | 20 | 24 | fits | 146,359 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 295,174 | 2.952 | 20 | 24 | fits | 149,991 | 175 | 0.467 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 295,108 | 2.951 | 20 | 50 | fits | 149,991 | 175 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 603,355 | 6.034 | 20 | 50 | fits | 146,619 | 157 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 740,690 | 7.407 | 20 | 20 | fits | 137,401 | 56 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,051,209 | 10.512 | 20 | 20 | fits | 41,778 | 17 | 0.796 |
| GPTP record released under the composed load, first | `backlog-adp.service.gptp.first.if0` | 291,606 | 2.916 | 10 | 10 | fits | 149,991 | 175 | 0.467 |
| GPTP record released under the composed load, last | `backlog-adp.service.gptp.last.if0` | 599,757 | 5.998 | 10 | 10 | fits | 146,619 | 157 | 0.449 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 21,898 | 0.219 | 20 | 20 | fits | 32,568 | 20 | 0.761 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 291,026 | 2.910 | 20 | 200 | fits | 149,991 | 175 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 44,212 | 0.442 | 20 | 200 | fits | 32,568 | 20 | 0.761 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 292,524 | 2.925 | 20 | 20 | fits | 149,991 | 175 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 584,732 | 5.847 | 20 | 20 | fits | 131,020 | 147 | 0.393 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 146,173 | 1.462 | 20 | 24 | fits | 146,359 | 155 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 295,174 | 2.952 | 20 | 24 | fits | 149,991 | 175 | 0.467 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 295,108 | 2.951 | 20 | 50 | fits | 149,991 | 175 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 587,756 | 5.878 | 20 | 50 | fits | 131,020 | 147 | 0.393 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 724,242 | 7.242 | 20 | 20 | fits | 136,552 | 56 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,034,567 | 10.346 | 20 | 20 | fits | 41,778 | 17 | 0.796 |
| GPTP record released under the composed load, first | `backlog-adp-refill.service.gptp.first.if0` | 291,606 | 2.916 | 10 | 10 | fits | 149,991 | 175 | 0.467 |
| GPTP record released under the composed load, last | `backlog-adp-refill.service.gptp.last.if0` | 584,158 | 5.842 | 10 | 10 | fits | 131,020 | 147 | 0.393 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,347,630 | 63.476 | 20 | 20 | MISS ceiling | 22,570 | 14 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,370,140 | 63.701 | 20 | 20 | MISS ceiling | 22,586 | 14 | 0.426 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,392,638 | 63.926 | 20 | 20 | MISS ceiling | 22,555 | 14 | 0.434 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,421,151 | 64.212 | 20 | 20 | MISS ceiling | 28,138 | 20 | 0.718 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,443,003 | 64.430 | 20 | 20 | MISS ceiling | 23,673 | 14 | 0.537 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 178,763 | 1.788 | 20 | 200 | fits | 163,367 | 183 | 0.480 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 465,172 | 4.652 | 20 | 200 | fits | 136,596 | 86 | 0.652 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 173,867 | 1.739 | 20 | 20 | fits | 163,367 | 183 | 0.480 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,241,063 | 62.411 | 20 | 20 | MISS ceiling | 36,963 | 16 | 0.675 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 178,081 | 1.781 | 20 | 24 | fits | 163,367 | 183 | 0.480 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,208,160 | 62.082 | 20 | 24 | MISS ceiling | 156,753 | 149 | 0.443 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 177,025 | 1.770 | 20 | 50 | fits | 163,367 | 183 | 0.480 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 463,654 | 4.637 | 20 | 50 | fits | 136,596 | 86 | 0.652 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 463,588 | 4.636 | 20 | 20 | fits | 136,596 | 86 | 0.652 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 819,218 | 8.192 | 20 | 20 | fits | 95,440 | 45 | 0.745 |
| GPTP record released under the composed load, first | `backlog-owed.service.gptp.first.if0` | 174,435 | 1.744 | 10 | 10 | fits | 163,367 | 183 | 0.480 |
| GPTP record released under the composed load, last | `backlog-owed.service.gptp.last.if0` | 460,968 | 4.610 | 10 | 10 | fits | 136,596 | 86 | 0.652 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 16,244 | 0.162 | 10 | 10 | fits | 31,778 | 16 | 0.734 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 22,255 | 0.223 | 10 | 10 | fits | 32,257 | 16 | 0.748 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
