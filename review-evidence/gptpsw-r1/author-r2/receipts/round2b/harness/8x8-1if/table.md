### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 26 paths and 7 of 78 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.202 (0.447) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.228 (0.629) | fits | 0 adp | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.309 (0.840) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.023 (0.387) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `fixture.link_up.if0` (fixture) | 0.022 (0.456) | fits | 0 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.018 (5.420) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.393 (6.093) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.092 (0.323) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.631 (2.164) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.597 (63.779) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.563 (64.752) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.344 (0.481) | fits | 0 aecp | 1 | 0 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-slave) | 0.186 (0.534) | fits | 0 gptp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.263 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.535 | MISS ceiling | 11 acmp | 5 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.312 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.033 | fits | 7 adp | 5 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.678 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.851 | MISS ceiling | 15 aecp | 5 | 1 |
| GPTP record released under the composed load, first | 0 | `backlog.service.gptp.first.if0` (backlog) | 4.269 | fits | 0 gptp | 5 | 0 |
| GPTP record released under the composed load, last | 0 | `backlog-adp.service.gptp.last.if0` (backlog-adp) | 6.040 | fits | 6 gptp | 5 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.295 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.076 | fits | 6 maap | 5 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 7.381 | fits | 0 srp | 5 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 10.691 | fits | 31 srp | 5 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.222 (0.223) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.542 | 8 | 151,956 (1.520) | yes | - |
| backlog-adp | 0 | 11.739 | 12 | 152,204 (1.522) | yes | - |
| backlog-adp-refill | 0 | 40.863 | 33 | 152,204 (1.522) | yes | - |
| backlog-owed | 0 | 65.317 | 24 | 163,835 (1.638) | yes | - |
| fixture | 0 | 1.877 | 3 | 103,772 (1.038) | yes | - |

Composed maximum over the 4 backlog windows: 163,835 CPU cycles (1.638 ms), backlog-owed.
Over the windows that released their whole load only: 163,835 (1.638 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 951 | 0 | 151,956 (1.520) | fits |
| backlog-adp | 992 | 0 | 152,204 (1.522) | fits |
| backlog-adp-refill | 1013 | 0 | 152,204 (1.522) | fits |
| backlog-owed | 987 | 0 | 163,835 (1.638) | fits |
| gptp-slave | 604 | 0 | 92,913 (0.929) | fits |
| gptp-master | 595 | 0 | 84,012 (0.840) | fits |
| fixture | 299 | 0 | 103,772 (1.038) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 265 | 30,621 (0.306) | 2,483 (0.025) |
| backlog-adp | 271 | 30,621 (0.306) | 2,574 (0.026) |
| backlog-adp-refill | 274 | 30,621 (0.306) | 2,574 (0.026) |
| backlog-owed | 277 | 30,621 (0.306) | 2,483 (0.025) |
| gptp-slave | 165 | 30,487 (0.305) | 2,531 (0.025) |
| gptp-master | 165 | 30,483 (0.305) | 2,531 (0.025) |
| fixture | 54 | 22,514 (0.225) | 2,432 (0.024) |

Longest pass that carries a step: 30,621 CPU cycles (0.306 ms), backlog; longest step: 2,574 (0.026 ms), backlog-adp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 163,137 | 1.631 | 20 | 200 | fits | 64,472 | 78 | 0.585 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 501,812 | 5.018 | 20 | 20 | fits | 100,816 | 132 | 0.261 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 431,190 | 4.312 | 20 | 200 | fits | 151,696 | 134 | 0.355 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 541,126 | 5.411 | 20 | 200 | fits | 100,816 | 132 | 0.261 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 426,294 | 4.263 | 20 | 20 | fits | 151,696 | 134 | 0.355 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 536,010 | 5.360 | 20 | 20 | fits | 100,816 | 132 | 0.261 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 151,065 | 1.511 | 20 | 24 | fits | 151,956 | 158 | 0.396 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 429,518 | 4.295 | 20 | 24 | fits | 151,696 | 134 | 0.355 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 429,452 | 4.295 | 20 | 50 | fits | 151,696 | 134 | 0.355 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 539,608 | 5.396 | 20 | 50 | fits | 100,816 | 132 | 0.261 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 539,542 | 5.395 | 20 | 20 | fits | 100,816 | 132 | 0.261 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 596,677 | 5.967 | 20 | 20 | fits | 25,442 | 42 | 0.119 |
| GPTP record released under the composed load, first | `backlog.service.gptp.first.if0` | 426,862 | 4.269 | 10 | 10 | fits | 151,696 | 134 | 0.355 |
| GPTP record released under the composed load, last | `backlog.service.gptp.last.if0` | 426,370 | 4.264 | 10 | 10 | fits | 151,696 | 134 | 0.355 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 539,317 | 5.393 | 20 | 20 | fits | 146,512 | 144 | 0.493 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 295,213 | 2.952 | 20 | 200 | fits | 150,907 | 175 | 0.458 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 603,324 | 6.033 | 20 | 200 | fits | 146,512 | 144 | 0.493 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 296,711 | 2.967 | 20 | 20 | fits | 150,907 | 175 | 0.458 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 604,602 | 6.046 | 20 | 20 | fits | 146,512 | 144 | 0.493 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,444 | 1.494 | 20 | 24 | fits | 149,630 | 155 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 299,361 | 2.994 | 20 | 24 | fits | 150,907 | 175 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 299,295 | 2.993 | 20 | 50 | fits | 150,907 | 175 | 0.458 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 607,626 | 6.076 | 20 | 50 | fits | 146,512 | 144 | 0.493 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 738,115 | 7.381 | 20 | 20 | fits | 130,555 | 58 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,069,119 | 10.691 | 20 | 20 | fits | 63,995 | 25 | 0.783 |
| GPTP record released under the composed load, first | `backlog-adp.service.gptp.first.if0` | 295,793 | 2.958 | 10 | 10 | fits | 150,907 | 175 | 0.458 |
| GPTP record released under the composed load, last | `backlog-adp.service.gptp.last.if0` | 604,028 | 6.040 | 10 | 10 | fits | 146,512 | 144 | 0.493 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 9,161 | 0.092 | 20 | 20 | fits | 32,311 | 20 | 0.759 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 295,213 | 2.952 | 20 | 200 | fits | 150,907 | 175 | 0.458 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 31,126 | 0.311 | 20 | 200 | fits | 32,311 | 20 | 0.759 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 296,711 | 2.967 | 20 | 20 | fits | 150,907 | 175 | 0.458 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 589,642 | 5.896 | 20 | 20 | fits | 131,552 | 134 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,444 | 1.494 | 20 | 24 | fits | 149,630 | 155 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 299,361 | 2.994 | 20 | 24 | fits | 150,907 | 175 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 299,295 | 2.993 | 20 | 50 | fits | 150,907 | 175 | 0.458 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 592,666 | 5.927 | 20 | 50 | fits | 131,552 | 134 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 722,146 | 7.221 | 20 | 20 | fits | 129,546 | 58 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,053,164 | 10.532 | 20 | 20 | fits | 63,995 | 25 | 0.783 |
| GPTP record released under the composed load, first | `backlog-adp-refill.service.gptp.first.if0` | 295,793 | 2.958 | 10 | 10 | fits | 150,907 | 175 | 0.458 |
| GPTP record released under the composed load, last | `backlog-adp-refill.service.gptp.last.if0` | 589,068 | 5.891 | 10 | 10 | fits | 131,552 | 134 | 0.444 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,359,718 | 63.597 | 20 | 20 | MISS ceiling | 22,570 | 14 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,382,228 | 63.822 | 20 | 20 | MISS ceiling | 22,586 | 14 | 0.426 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,410,821 | 64.108 | 20 | 20 | MISS ceiling | 28,012 | 20 | 0.706 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,432,461 | 64.325 | 20 | 20 | MISS ceiling | 23,650 | 14 | 0.515 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,456,261 | 64.563 | 20 | 20 | MISS ceiling | 23,059 | 14 | 0.557 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 168,483 | 1.685 | 20 | 200 | fits | 163,835 | 183 | 0.474 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 453,714 | 4.537 | 20 | 200 | fits | 135,946 | 100 | 0.645 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 163,587 | 1.636 | 20 | 20 | fits | 163,835 | 183 | 0.474 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,253,484 | 62.535 | 20 | 20 | MISS ceiling | 35,587 | 16 | 0.619 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 167,801 | 1.678 | 20 | 24 | fits | 163,835 | 183 | 0.474 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,185,113 | 61.851 | 20 | 24 | MISS ceiling | 158,227 | 150 | 0.444 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 166,745 | 1.667 | 20 | 50 | fits | 163,835 | 183 | 0.474 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 452,196 | 4.522 | 20 | 50 | fits | 135,946 | 100 | 0.645 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 452,130 | 4.521 | 20 | 20 | fits | 135,946 | 100 | 0.645 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 818,659 | 8.187 | 20 | 20 | fits | 98,366 | 45 | 0.759 |
| GPTP record released under the composed load, first | `backlog-owed.service.gptp.first.if0` | 164,155 | 1.642 | 10 | 10 | fits | 163,835 | 183 | 0.474 |
| GPTP record released under the composed load, last | `backlog-owed.service.gptp.last.if0` | 449,510 | 4.495 | 10 | 10 | fits | 135,946 | 100 | 0.645 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 18,584 | 0.186 | 10 | 10 | fits | 31,412 | 16 | 0.715 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 13,045 | 0.130 | 10 | 10 | fits | 31,608 | 16 | 0.724 |
| LINK_UP | `fixture.link_up.if0` | 2,160 | 0.022 | 20 | 200 | fits | 45,638 | 53 (11) | 0.735 |
| malformed MRPDU discard | `fixture.malformed.if0` | 22,206 | 0.222 | 20 | 20 | fits | 22,272 | 13 | 0.671 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 34,411 | 0.344 | 20 | 24 | fits | 48,133 | 43 | 0.760 |
| LINK_DOWN | `fixture.link_down.if0` | 2,340 | 0.023 | 20 | 200 | fits | 38,684 | 24 (9) | 0.813 |
| BIND_RX | `fixture.bind_rx.if0` | 20,164 | 0.202 | 20 | 20 | fits | 44,685 | 27 (77) | 0.764 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 30,884 | 0.309 | 20 | 20 | fits | 50,519 | 40 (35) | 0.732 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 22,756 | 0.228 | 20 | 20 | fits | 29,039 | 14 (29) | 0.748 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 103,668 | 1.037 | 20 | 200 | fits | 103,772 | 83 | 0.738 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 103,668 | 1.037 | 20 | 200 | fits | 103,772 | 83 | 0.738 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 103,394 | 1.034 | 20 | 20 | fits | 103,772 | 83 | 0.738 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 103,394 | 1.034 | 20 | 20 | fits | 103,772 | 83 | 0.738 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 103,602 | 1.036 | 20 | 24 | fits | 103,772 | 83 | 0.738 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 103,602 | 1.036 | 20 | 24 | fits | 103,772 | 83 | 0.738 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 103,536 | 1.035 | 20 | 50 | fits | 103,772 | 83 | 0.738 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 103,536 | 1.035 | 20 | 50 | fits | 103,772 | 83 | 0.738 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 103,470 | 1.035 | 20 | 20 | fits | 103,772 | 83 | 0.738 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 103,470 | 1.035 | 20 | 20 | fits | 103,772 | 83 | 0.738 |
| GPTP record released under the composed load, first | `fixture.service.gptp.first.if0` | 103,312 | 1.033 | 10 | 10 | fits | 103,772 | 83 | 0.738 |
| GPTP record released under the composed load, last | `fixture.service.gptp.last.if0` | 103,312 | 1.033 | 10 | 10 | fits | 103,772 | 83 | 0.738 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
