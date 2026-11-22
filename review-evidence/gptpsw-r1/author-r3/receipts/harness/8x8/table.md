### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 20 paths and 7 of 59 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.926 (6.243) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.664 (6.432) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.244 (0.709) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.717 (2.280) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.735 (64.144) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.757 (65.160) | MISS ceiling | 11 acmp | 4 | 4 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-slave) | 0.309 (0.735) | fits | 0 gptp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.466 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.460 | MISS ceiling | 11 acmp | 4 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.520 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.367 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.234 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.712 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 62.054 | MISS ceiling | 15 aecp | 4 | 1 |
| GPTP record released under the composed load, first | 0 | `backlog.service.gptp.first.if0` (backlog) | 4.477 | fits | 0 gptp | 4 | 0 |
| GPTP record released under the composed load, last | 1 | `backlog-adp-refill.service.gptp.last.if1` (backlog-adp-refill) | 7.853 | fits | 13 gptp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.503 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.219 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | 7.894 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 13.183 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 10.259 | 9 | 161,043 (1.610) | yes | - |
| backlog-adp | 0 | 14.622 | 15 | 165,516 (1.655) | yes | - |
| backlog-adp-refill | 0 | 41.148 | 31 | 165,516 (1.655) | yes | - |
| backlog-owed | 0 | 65.641 | 25 | 162,097 (1.621) | yes | - |

Composed maximum over the 4 backlog windows: 165,516 CPU cycles (1.655 ms), backlog-adp.
Over the windows that released their whole load only: 165,516 (1.655 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 961 | 0 | 161,043 (1.610) | fits |
| backlog-adp | 1004 | 0 | 165,516 (1.655) | fits |
| backlog-adp-refill | 1020 | 0 | 165,516 (1.655) | fits |
| backlog-owed | 997 | 0 | 162,097 (1.621) | fits |
| gptp-slave | 613 | 0 | 121,616 (1.216) | fits |
| gptp-master | 602 | 0 | 111,266 (1.113) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 266 | 26,250 (0.263) | 2,888 (0.029) |
| backlog-adp | 271 | 26,250 (0.263) | 2,830 (0.028) |
| backlog-adp-refill | 273 | 26,250 (0.263) | 2,830 (0.028) |
| backlog-owed | 277 | 26,694 (0.267) | 2,830 (0.028) |
| gptp-slave | 165 | 26,250 (0.263) | 2,830 (0.028) |
| gptp-master | 165 | 26,250 (0.263) | 2,830 (0.028) |

Longest pass that carries a step: 26,694 CPU cycles (0.267 ms), backlog-owed; longest step: 2,888 (0.029 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 171,667 | 1.717 | 20 | 200 | fits | 66,993 | 81 | 0.581 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 592,631 | 5.926 | 20 | 20 | fits | 160,606 | 141 | 0.400 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 452,035 | 4.520 | 20 | 200 | fits | 155,528 | 166 | 0.429 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 623,445 | 6.234 | 20 | 200 | fits | 160,606 | 141 | 0.400 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 446,565 | 4.466 | 20 | 20 | fits | 155,528 | 166 | 0.429 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 617,755 | 6.178 | 20 | 20 | fits | 160,606 | 141 | 0.400 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 160,152 | 1.602 | 20 | 24 | fits | 161,043 | 183 | 0.314 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 294,835 | 2.948 | 20 | 24 | fits | 68,680 | 29 | 0.688 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 450,297 | 4.503 | 20 | 50 | fits | 155,528 | 166 | 0.429 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 621,927 | 6.219 | 20 | 50 | fits | 160,606 | 141 | 0.400 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 747,106 | 7.471 | 20 | 20 | fits | 125,245 | 94 | 0.660 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 955,298 | 9.553 | 20 | 20 | fits | 95,194 | 58 | 0.631 |
| GPTP record released under the composed load, first | `backlog.service.gptp.first.if0` | 447,707 | 4.477 | 10 | 10 | fits | 155,528 | 166 | 0.429 |
| GPTP record released under the composed load, last | `backlog.service.gptp.last.if1` | 743,912 | 7.439 | 10 | 10 | fits | 125,245 | 94 | 0.660 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 566,448 | 5.664 | 20 | 20 | fits | 155,498 | 124 | 0.468 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 321,187 | 3.212 | 20 | 200 | fits | 165,516 | 203 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 636,697 | 6.367 | 20 | 200 | fits | 155,498 | 124 | 0.468 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 323,259 | 3.233 | 20 | 20 | fits | 165,516 | 203 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 784,445 | 7.844 | 20 | 20 | fits | 135,185 | 97 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 152,329 | 1.523 | 20 | 24 | fits | 152,515 | 182 | 0.293 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 325,909 | 3.259 | 20 | 24 | fits | 165,516 | 203 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 325,843 | 3.258 | 20 | 50 | fits | 165,516 | 203 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 486,075 | 4.861 | 20 | 50 | fits | 160,628 | 183 | 0.488 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 787,403 | 7.874 | 20 | 20 | fits | 135,185 | 97 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,318,262 | 13.183 | 20 | 20 | fits | 48,316 | 18 | 0.799 |
| GPTP record released under the composed load, first | `backlog-adp.service.gptp.first.if0` | 322,341 | 3.223 | 10 | 10 | fits | 165,516 | 203 | 0.451 |
| GPTP record released under the composed load, last | `backlog-adp.service.gptp.last.if1` | 783,297 | 7.833 | 10 | 10 | fits | 135,185 | 97 | 0.613 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 24,412 | 0.244 | 20 | 20 | fits | 36,344 | 21 | 0.783 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 321,187 | 3.212 | 20 | 200 | fits | 165,516 | 203 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 49,473 | 0.495 | 20 | 200 | fits | 36,344 | 21 | 0.783 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 323,259 | 3.233 | 20 | 20 | fits | 165,516 | 203 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 786,400 | 7.864 | 20 | 20 | fits | 132,620 | 91 | 0.662 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 152,329 | 1.523 | 20 | 24 | fits | 152,515 | 182 | 0.293 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 325,909 | 3.259 | 20 | 24 | fits | 165,516 | 203 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 325,843 | 3.258 | 20 | 50 | fits | 165,516 | 203 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 486,075 | 4.861 | 20 | 50 | fits | 160,628 | 183 | 0.488 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 789,358 | 7.894 | 20 | 20 | fits | 132,620 | 91 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,302,074 | 13.021 | 20 | 20 | fits | 35,745 | 14 | 0.822 |
| GPTP record released under the composed load, first | `backlog-adp-refill.service.gptp.first.if0` | 322,341 | 3.223 | 10 | 10 | fits | 165,516 | 203 | 0.451 |
| GPTP record released under the composed load, last | `backlog-adp-refill.service.gptp.last.if1` | 785,252 | 7.853 | 10 | 10 | fits | 132,620 | 91 | 0.662 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,373,541 | 63.735 | 20 | 20 | MISS ceiling | 26,370 | 15 | 0.554 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,399,589 | 63.996 | 20 | 20 | MISS ceiling | 25,553 | 15 | 0.439 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,424,984 | 64.250 | 20 | 20 | MISS ceiling | 25,452 | 15 | 0.455 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,450,404 | 64.504 | 20 | 20 | MISS ceiling | 25,496 | 15 | 0.455 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,475,702 | 64.757 | 20 | 20 | MISS ceiling | 25,361 | 15 | 0.472 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 171,864 | 1.719 | 20 | 200 | fits | 162,097 | 193 | 0.433 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 484,088 | 4.841 | 20 | 200 | fits | 156,025 | 116 | 0.424 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 166,394 | 1.664 | 20 | 20 | fits | 162,097 | 193 | 0.433 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,245,992 | 62.460 | 20 | 20 | MISS ceiling | 45,207 | 46 | 0.644 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 171,182 | 1.712 | 20 | 24 | fits | 162,097 | 193 | 0.433 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,205,419 | 62.054 | 20 | 24 | MISS ceiling | 154,196 | 165 | 0.378 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 170,126 | 1.701 | 20 | 50 | fits | 162,097 | 193 | 0.433 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 482,570 | 4.826 | 20 | 50 | fits | 156,025 | 116 | 0.424 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 603,560 | 6.036 | 20 | 20 | fits | 121,056 | 39 | 0.793 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 995,807 | 9.958 | 20 | 20 | fits | 47,724 | 18 | 0.801 |
| GPTP record released under the composed load, first | `backlog-owed.service.gptp.first.if0` | 167,536 | 1.675 | 10 | 10 | fits | 162,097 | 193 | 0.433 |
| GPTP record released under the composed load, last | `backlog-owed.service.gptp.last.if1` | 600,366 | 6.004 | 10 | 10 | fits | 121,056 | 39 | 0.793 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 30,891 | 0.309 | 10 | 10 | fits | 37,238 | 18 | 0.748 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 30,537 | 0.305 | 10 | 10 | fits | 37,163 | 18 | 0.737 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
