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
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.115 (5.639) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.386 (6.201) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.110 (0.510) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.631 (2.164) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.703 (63.892) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.672 (64.863) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.344 (0.481) | fits | 0 aecp | 1 | 0 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-slave) | 0.186 (0.534) | fits | 0 gptp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.256 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.640 | MISS ceiling | 11 acmp | 5 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.312 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.134 | fits | 7 adp | 5 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.678 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.889 | MISS ceiling | 15 aecp | 5 | 1 |
| GPTP record released under the composed load, first | 0 | `backlog.service.gptp.first.if0` (backlog) | 4.269 | fits | 0 gptp | 5 | 0 |
| GPTP record released under the composed load, last | 0 | `backlog-adp-refill.service.gptp.last.if0` (backlog-adp-refill) | 7.491 | fits | 15 gptp | 5 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.295 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.185 | fits | 6 maap | 5 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 8.953 | fits | 0 srp | 5 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 12.271 | fits | 31 srp | 5 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.222 (0.223) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.766 | 8 | 151,956 (1.520) | yes | - |
| backlog-adp | 0 | 12.871 | 12 | 157,356 (1.574) | yes | - |
| backlog-adp-refill | 0 | 40.880 | 32 | 152,204 (1.522) | yes | - |
| backlog-owed | 0 | 65.429 | 25 | 163,835 (1.638) | yes | - |
| fixture | 0 | 1.877 | 3 | 103,772 (1.038) | yes | - |

Composed maximum over the 4 backlog windows: 163,835 CPU cycles (1.638 ms), backlog-owed.
Over the windows that released their whole load only: 163,835 (1.638 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 951 | 0 | 151,956 (1.520) | fits |
| backlog-adp | 992 | 0 | 157,356 (1.574) | fits |
| backlog-adp-refill | 1012 | 0 | 152,204 (1.522) | fits |
| backlog-owed | 988 | 0 | 163,835 (1.638) | fits |
| gptp-slave | 604 | 0 | 92,913 (0.929) | fits |
| gptp-master | 595 | 0 | 84,012 (0.840) | fits |
| fixture | 299 | 0 | 103,772 (1.038) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 265 | 30,621 (0.306) | 2,483 (0.025) |
| backlog-adp | 271 | 30,621 (0.306) | 2,483 (0.025) |
| backlog-adp-refill | 274 | 30,621 (0.306) | 2,483 (0.025) |
| backlog-owed | 277 | 30,621 (0.306) | 2,483 (0.025) |
| gptp-slave | 165 | 30,487 (0.305) | 2,531 (0.025) |
| gptp-master | 165 | 30,483 (0.305) | 2,531 (0.025) |
| fixture | 54 | 22,514 (0.225) | 2,432 (0.024) |

Longest pass that carries a step: 30,621 CPU cycles (0.306 ms), backlog; longest step: 2,531 (0.025 ms), gptp-slave.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 163,137 | 1.631 | 20 | 200 | fits | 64,472 | 78 | 0.585 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 511,491 | 5.115 | 20 | 20 | fits | 122,811 | 172 | 0.233 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 431,190 | 4.312 | 20 | 200 | fits | 151,696 | 134 | 0.355 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 563,121 | 5.631 | 20 | 200 | fits | 122,811 | 172 | 0.233 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 425,556 | 4.256 | 20 | 20 | fits | 151,696 | 134 | 0.355 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 557,267 | 5.573 | 20 | 20 | fits | 122,811 | 172 | 0.233 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 151,065 | 1.511 | 20 | 24 | fits | 151,956 | 158 | 0.396 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 429,518 | 4.295 | 20 | 24 | fits | 151,696 | 134 | 0.355 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 429,452 | 4.295 | 20 | 50 | fits | 151,696 | 134 | 0.355 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 561,603 | 5.616 | 20 | 50 | fits | 122,811 | 172 | 0.233 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 561,537 | 5.615 | 20 | 20 | fits | 122,811 | 172 | 0.233 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 619,101 | 6.191 | 20 | 20 | fits | 25,506 | 42 | 0.125 |
| GPTP record released under the composed load, first | `backlog.service.gptp.first.if0` | 426,862 | 4.269 | 10 | 10 | fits | 151,696 | 134 | 0.355 |
| GPTP record released under the composed load, last | `backlog.service.gptp.last.if0` | 558,179 | 5.582 | 10 | 10 | fits | 122,811 | 172 | 0.233 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 538,579 | 5.386 | 20 | 20 | fits | 157,356 | 140 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 294,475 | 2.945 | 20 | 200 | fits | 150,907 | 175 | 0.458 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 613,430 | 6.134 | 20 | 200 | fits | 157,356 | 140 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 296,711 | 2.967 | 20 | 20 | fits | 150,907 | 175 | 0.458 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 743,645 | 7.436 | 20 | 20 | fits | 128,199 | 112 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,444 | 1.494 | 20 | 24 | fits | 149,630 | 155 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 299,361 | 2.994 | 20 | 24 | fits | 150,907 | 175 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 299,295 | 2.993 | 20 | 50 | fits | 150,907 | 175 | 0.458 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 618,470 | 6.185 | 20 | 50 | fits | 157,356 | 140 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 895,287 | 8.953 | 20 | 20 | fits | 139,000 | 92 | 0.756 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,227,147 | 12.271 | 20 | 20 | fits | 69,576 | 32 | 0.800 |
| GPTP record released under the composed load, first | `backlog-adp.service.gptp.first.if0` | 295,793 | 2.958 | 10 | 10 | fits | 150,907 | 175 | 0.458 |
| GPTP record released under the composed load, last | `backlog-adp.service.gptp.last.if0` | 742,333 | 7.423 | 10 | 10 | fits | 128,199 | 112 | 0.460 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,014 | 0.110 | 20 | 20 | fits | 32,311 | 20 | 0.759 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 294,475 | 2.945 | 20 | 200 | fits | 150,907 | 175 | 0.458 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 32,931 | 0.329 | 20 | 200 | fits | 32,311 | 20 | 0.759 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 296,711 | 2.967 | 20 | 20 | fits | 150,907 | 175 | 0.458 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 750,449 | 7.504 | 20 | 20 | fits | 140,315 | 112 | 0.582 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,444 | 1.494 | 20 | 24 | fits | 149,630 | 155 | 0.386 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 299,361 | 2.994 | 20 | 24 | fits | 150,907 | 175 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 299,295 | 2.993 | 20 | 50 | fits | 150,907 | 175 | 0.458 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 613,158 | 6.132 | 20 | 50 | fits | 152,044 | 138 | 0.468 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 753,407 | 7.534 | 20 | 20 | fits | 140,315 | 112 | 0.582 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,215,860 | 12.159 | 20 | 20 | fits | 59,094 | 28 | 0.812 |
| GPTP record released under the composed load, first | `backlog-adp-refill.service.gptp.first.if0` | 295,793 | 2.958 | 10 | 10 | fits | 150,907 | 175 | 0.458 |
| GPTP record released under the composed load, last | `backlog-adp-refill.service.gptp.last.if0` | 749,137 | 7.491 | 10 | 10 | fits | 140,315 | 112 | 0.582 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,370,306 | 63.703 | 20 | 20 | MISS ceiling | 22,570 | 14 | 0.460 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,398,743 | 63.987 | 20 | 20 | MISS ceiling | 27,850 | 20 | 0.692 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,420,438 | 64.204 | 20 | 20 | MISS ceiling | 23,711 | 14 | 0.500 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,444,281 | 64.443 | 20 | 20 | MISS ceiling | 23,181 | 14 | 0.547 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,467,170 | 64.672 | 20 | 20 | MISS ceiling | 22,394 | 14 | 0.460 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 168,483 | 1.685 | 20 | 200 | fits | 163,835 | 183 | 0.474 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 475,013 | 4.750 | 20 | 200 | fits | 157,245 | 137 | 0.372 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 162,849 | 1.628 | 20 | 20 | fits | 163,835 | 183 | 0.474 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,264,048 | 62.640 | 20 | 20 | MISS ceiling | 35,785 | 16 | 0.640 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 167,801 | 1.678 | 20 | 24 | fits | 163,835 | 183 | 0.474 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,188,856 | 61.889 | 20 | 24 | MISS ceiling | 159,040 | 155 | 0.433 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 166,745 | 1.667 | 20 | 50 | fits | 163,835 | 183 | 0.474 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 473,495 | 4.735 | 20 | 50 | fits | 157,245 | 137 | 0.372 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 610,830 | 6.108 | 20 | 20 | fits | 137,401 | 58 | 0.768 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 939,237 | 9.392 | 20 | 20 | fits | 73,695 | 29 | 0.769 |
| GPTP record released under the composed load, first | `backlog-owed.service.gptp.first.if0` | 164,155 | 1.642 | 10 | 10 | fits | 163,835 | 183 | 0.474 |
| GPTP record released under the composed load, last | `backlog-owed.service.gptp.last.if0` | 607,472 | 6.075 | 10 | 10 | fits | 137,401 | 58 | 0.768 |
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
