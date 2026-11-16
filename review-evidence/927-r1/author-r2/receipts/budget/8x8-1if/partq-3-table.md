### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 23 paths and 0 of 134 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.302 (0.738) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.230 (0.636) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.146 (0.589) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.249 (0.599) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.055 (0.208) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.030 (0.338) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.206 (0.598) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged1-5.adp_available.if0` (backlog-adp@blank-aged1-5) | 4.232 (4.807) | fits | 7 adp | 11 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.176 (0.577) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.113 (0.277) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.142 (0.338) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.156 (0.577) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.230 (0.617) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-5.service.acmp.first.if0` (backlog-adp@blank-aged1-5) | 3.180 | fits | 0 acmp | 11 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.acmp.last.if0` (backlog-adp@verify-aged2-5) | 6.196 | fits | 11 acmp | 11 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-5.service.adp.first.if0` (backlog-adp@blank-aged1-5) | 3.171 | fits | 0 adp | 11 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-5.service.adp.last.if0` (backlog-adp@blank-aged1-5) | 4.669 | fits | 7 adp | 11 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-aged1-1.service.aecp.first.if0` (backlog-adp@program-aged1-1) | 1.624 | fits | 0 aecp | 11 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-5.service.aecp.last.if0` (backlog-adp@blank-aged1-5) | 3.206 | fits | 15 aecp | 11 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-5.service.maap.first.if0` (backlog-adp@blank-aged1-5) | 3.206 | fits | 0 maap | 11 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-5.service.maap.last.if0` (backlog-adp@blank-aged1-5) | 4.706 | fits | 6 maap | 11 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.srp.first.if0` (backlog-adp@verify-aged2-5) | 6.226 | fits | 0 srp | 11 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.srp.last.if0` (backlog-adp@verify-aged2-5) | 10.033 | fits | 31 srp | 11 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-aged1-1 | 0 | 10.764 | 10 | 150,776 (1.508) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.111 | 12 | 152,151 (1.522) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.998 | 11 | 154,537 (1.545) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.677 | 9 | 150,915 (1.509) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.847 | 10 | 153,031 (1.530) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.845 | 10 | 156,189 (1.562) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.472 | 9 | 150,820 (1.508) | yes | - |
| backlog-adp@verify-aged2-5 | 1 | 11.175 | 11 | 152,482 (1.525) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.910 | 12 | 158,124 (1.581) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.652 | 9 | 152,015 (1.520) | yes | - |
| backlog-adp | 0 | 9.911 | 10 | 152,548 (1.525) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill, backlog-owed not run): 152,548 CPU cycles (1.525 ms), backlog-adp.
Over the windows that released their whole load only: 152,548 (1.525 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-aged1-1 | 752 | 0 | 150,776 (1.508) | fits |
| backlog-adp@blank-aged1-5 | 779 | 0 | 152,151 (1.522) | fits |
| backlog-adp@program-aged2-1 | 1183 | 0 | 154,537 (1.545) | fits |
| backlog-adp@program-aged2-5 | 1206 | 0 | 150,915 (1.509) | fits |
| backlog-adp@program-aged1-1 | 1132 | 0 | 153,031 (1.530) | fits |
| backlog-adp@program-aged1-5 | 1157 | 0 | 156,189 (1.562) | fits |
| backlog-adp@verify-aged2-1 | 1561 | 0 | 150,820 (1.508) | fits |
| backlog-adp@verify-aged2-5 | 1588 | 0 | 152,482 (1.525) | fits |
| backlog-adp@verify-aged1-1 | 1513 | 0 | 158,124 (1.581) | fits |
| backlog-adp@verify-aged1-5 | 1536 | 0 | 152,015 (1.520) | fits |
| acmp-noresp | 1881 | 0 | 46,812 (0.468) | fits |
| backlog-adp | 312 | 0 | 152,548 (1.525) | fits |
| maap | 179 | 0 | 34,491 (0.345) | fits |
| control | 88 | 0 | 33,791 (0.338) | fits |
| datapath-events | 118 | 0 | 33,791 (0.338) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.357 (20) | 10.643 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.366 (20) | 10.634 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 9.210 (20) | 10.790 |
| backlog-adp@program-aged2-5 | 2 | +5.433 ms, 80,665 (0.807 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.024 (20) | 9.976 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.390 (20) | 10.610 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.391 (20) | 10.609 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.267 ms, 77,685 (0.777 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.230 (20) | 10.770 |
| backlog-adp@verify-aged2-5 | 2 | +4.613 ms, 77,559 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.033 (20) | 9.967 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.919 (20) | 11.081 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.233 (20) | 10.767 |

Least margin over the aged windows: 9.967 ms, `backlog-adp@verify-aged2-5.service.srp.last.if0` at 10.033 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-aged1-1 | 337 | 96,359 (0.964) | 76,201 (0.762) |
| backlog-adp@blank-aged1-5 | 337 | 95,113 (0.951) | 76,170 (0.762) |
| backlog-adp@program-aged2-1 | 446 | 100,997 (1.010) | 78,509 (0.785) |
| backlog-adp@program-aged2-5 | 446 | 100,997 (1.010) | 78,482 (0.785) |
| backlog-adp@program-aged1-1 | 446 | 100,997 (1.010) | 78,725 (0.787) |
| backlog-adp@program-aged1-5 | 446 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@verify-aged2-1 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-5 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-1 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-5 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| acmp-noresp | 615 | 108,538 (1.085) | 78,338 (0.783) |
| backlog-adp | 271 | 26,388 (0.264) | 2,378 (0.024) |
| maap | 166 | 26,163 (0.262) | 2,374 (0.024) |
| control | 79 | 26,162 (0.262) | 2,374 (0.024) |
| datapath-events | 70 | 26,162 (0.262) | 2,374 (0.024) |

Longest pass that carries a step: 108,538 CPU cycles (1.085 ms), acmp-noresp; longest step: 78,776 (0.788 ms), backlog-adp@program-aged1-5.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 401,937 | 4.019 | 20 | 20 | fits | 150,684 | 185 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 305,037 | 3.050 | 20 | 200 | fits | 150,776 | 192 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 455,105 | 4.551 | 20 | 200 | fits | 150,684 | 185 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 305,961 | 3.060 | 20 | 20 | fits | 150,776 | 192 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 539,612 | 5.396 | 20 | 20 | fits | 83,803 | 38 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 158,825 | 1.588 | 20 | 24 | fits | 148,058 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 308,611 | 3.086 | 20 | 24 | fits | 150,776 | 192 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 308,545 | 3.085 | 20 | 50 | fits | 150,776 | 192 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 458,833 | 4.588 | 20 | 50 | fits | 150,684 | 185 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 542,570 | 5.426 | 20 | 20 | fits | 83,803 | 38 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 935,697 | 9.357 | 20 | 20 | fits | 47,347 | 22 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 423,219 | 4.232 | 20 | 20 | fits | 150,458 | 183 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 317,070 | 3.171 | 20 | 200 | fits | 152,151 | 197 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 466,912 | 4.669 | 20 | 200 | fits | 150,458 | 183 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 317,994 | 3.180 | 20 | 20 | fits | 152,151 | 197 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 552,986 | 5.530 | 20 | 20 | fits | 85,370 | 42 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 159,663 | 1.597 | 20 | 24 | fits | 148,246 | 143 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 320,644 | 3.206 | 20 | 24 | fits | 152,151 | 197 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 320,578 | 3.206 | 20 | 50 | fits | 152,151 | 197 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 470,640 | 4.706 | 20 | 50 | fits | 150,458 | 183 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 555,944 | 5.559 | 20 | 20 | fits | 85,370 | 42 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 936,607 | 9.366 | 20 | 20 | fits | 41,764 | 17 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 394,167 | 3.942 | 20 | 20 | fits | 150,885 | 201 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 306,119 | 3.061 | 20 | 200 | fits | 154,537 | 185 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 456,388 | 4.564 | 20 | 200 | fits | 150,885 | 201 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 307,043 | 3.070 | 20 | 20 | fits | 154,537 | 185 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 540,295 | 5.403 | 20 | 20 | fits | 83,203 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 146,326 | 1.463 | 20 | 24 | fits | 148,241 | 143 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 309,693 | 3.097 | 20 | 24 | fits | 154,537 | 185 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 309,627 | 3.096 | 20 | 50 | fits | 154,537 | 185 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 460,116 | 4.601 | 20 | 50 | fits | 150,885 | 201 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 543,253 | 5.433 | 20 | 20 | fits | 83,203 | 37 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 921,020 | 9.210 | 20 | 20 | fits | 38,868 | 19 | 0.844 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 388,661 | 3.887 | 20 | 20 | fits | 150,915 | 216 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 292,155 | 2.922 | 20 | 200 | fits | 150,466 | 198 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 442,454 | 4.425 | 20 | 200 | fits | 150,915 | 216 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 293,079 | 2.931 | 20 | 20 | fits | 150,466 | 198 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 538,595 | 5.386 | 20 | 20 | fits | 85,034 | 48 | 0.759 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 146,253 | 1.463 | 20 | 24 | fits | 150,129 | 111 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 295,729 | 2.957 | 20 | 24 | fits | 150,466 | 198 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 295,663 | 2.957 | 20 | 50 | fits | 150,466 | 198 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 446,182 | 4.462 | 20 | 50 | fits | 150,915 | 216 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 541,553 | 5.416 | 20 | 20 | fits | 85,034 | 48 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,002,426 | 10.024 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 419,179 | 4.192 | 20 | 20 | fits | 153,031 | 206 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 309,483 | 3.095 | 20 | 200 | fits | 151,635 | 176 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 461,898 | 4.619 | 20 | 200 | fits | 153,031 | 206 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 310,407 | 3.104 | 20 | 20 | fits | 151,635 | 176 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 557,634 | 5.576 | 20 | 20 | fits | 84,456 | 38 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 162,412 | 1.624 | 20 | 24 | fits | 148,071 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 313,057 | 3.131 | 20 | 24 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 312,991 | 3.130 | 20 | 50 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 465,626 | 4.656 | 20 | 50 | fits | 153,031 | 206 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 560,592 | 5.606 | 20 | 20 | fits | 84,456 | 38 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 938,986 | 9.390 | 20 | 20 | fits | 42,114 | 16 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 421,096 | 4.211 | 20 | 20 | fits | 156,189 | 200 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 309,406 | 3.094 | 20 | 200 | fits | 153,320 | 180 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 464,979 | 4.650 | 20 | 200 | fits | 156,189 | 200 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 310,330 | 3.103 | 20 | 20 | fits | 153,320 | 180 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 548,971 | 5.490 | 20 | 20 | fits | 83,288 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 160,650 | 1.607 | 20 | 24 | fits | 148,178 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 312,980 | 3.130 | 20 | 24 | fits | 153,320 | 180 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 312,914 | 3.129 | 20 | 50 | fits | 153,320 | 180 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 468,707 | 4.687 | 20 | 50 | fits | 156,189 | 200 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 551,929 | 5.519 | 20 | 20 | fits | 83,288 | 37 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 939,103 | 9.391 | 20 | 20 | fits | 41,476 | 16 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 389,573 | 3.896 | 20 | 20 | fits | 150,820 | 216 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 292,539 | 2.925 | 20 | 200 | fits | 150,560 | 198 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 442,743 | 4.427 | 20 | 200 | fits | 150,820 | 216 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 293,463 | 2.935 | 20 | 20 | fits | 150,560 | 198 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 527,164 | 5.272 | 20 | 20 | fits | 83,717 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 146,543 | 1.465 | 20 | 24 | fits | 150,170 | 111 | 0.372 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 296,113 | 2.961 | 20 | 24 | fits | 150,560 | 198 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 296,047 | 2.960 | 20 | 50 | fits | 150,560 | 198 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 446,471 | 4.465 | 20 | 50 | fits | 150,820 | 216 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 530,122 | 5.301 | 20 | 20 | fits | 83,717 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 922,965 | 9.230 | 20 | 20 | fits | 47,414 | 22 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 412,550 | 4.125 | 20 | 20 | fits | 152,482 | 189 | 0.481 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 293,957 | 2.940 | 20 | 200 | fits | 152,277 | 198 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 455,949 | 4.559 | 20 | 200 | fits | 152,482 | 189 | 0.481 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 294,881 | 2.949 | 20 | 20 | fits | 152,277 | 198 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 619,639 | 6.196 | 20 | 20 | fits | 85,427 | 43 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 146,244 | 1.462 | 20 | 24 | fits | 148,112 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 297,531 | 2.975 | 20 | 24 | fits | 152,277 | 198 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 297,465 | 2.975 | 20 | 50 | fits | 152,277 | 198 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 459,677 | 4.597 | 20 | 50 | fits | 152,482 | 189 | 0.481 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 622,597 | 6.226 | 20 | 20 | fits | 85,427 | 43 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,003,334 | 10.033 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 394,382 | 3.944 | 20 | 20 | fits | 158,124 | 205 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 309,005 | 3.090 | 20 | 200 | fits | 154,672 | 185 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 466,513 | 4.665 | 20 | 200 | fits | 158,124 | 205 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 309,929 | 3.099 | 20 | 20 | fits | 154,672 | 185 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 550,080 | 5.501 | 20 | 20 | fits | 82,863 | 31 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 149,021 | 1.490 | 20 | 24 | fits | 148,175 | 143 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 312,579 | 3.126 | 20 | 24 | fits | 154,672 | 185 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 312,513 | 3.125 | 20 | 50 | fits | 154,672 | 185 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 470,241 | 4.702 | 20 | 50 | fits | 158,124 | 205 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 553,038 | 5.530 | 20 | 20 | fits | 82,863 | 31 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 891,937 | 8.919 | 20 | 20 | fits | 85,126 | 36 | 0.566 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 389,392 | 3.894 | 20 | 20 | fits | 150,939 | 186 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 292,492 | 2.925 | 20 | 200 | fits | 152,015 | 197 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 442,815 | 4.428 | 20 | 200 | fits | 150,939 | 186 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 293,416 | 2.934 | 20 | 20 | fits | 152,015 | 197 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 539,602 | 5.396 | 20 | 20 | fits | 85,827 | 48 | 0.760 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 145,041 | 1.450 | 20 | 24 | fits | 148,089 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 296,066 | 2.961 | 20 | 24 | fits | 152,015 | 197 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 296,000 | 2.960 | 20 | 50 | fits | 152,015 | 197 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 446,543 | 4.465 | 20 | 50 | fits | 150,939 | 186 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 542,560 | 5.426 | 20 | 20 | fits | 85,827 | 48 | 0.760 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 923,251 | 9.233 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 22,956 | 0.230 | 20 | 20 | fits | 38,679 | 27 (35) | 0.810 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 14,609 | 0.146 | 20 | 20 | fits | 34,000 | 23 (14) | 0.837 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 24,914 | 0.249 | 20 | 20 | fits | 34,476 | 24 (14) | 0.836 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 30,198 | 0.302 | 20 | 20 | fits | 40,612 | 27 (35) | 0.808 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 404,242 | 4.042 | 20 | 20 | fits | 151,361 | 186 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 296,489 | 2.965 | 20 | 200 | fits | 152,548 | 198 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 457,490 | 4.575 | 20 | 200 | fits | 151,361 | 186 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 297,413 | 2.974 | 20 | 20 | fits | 152,548 | 198 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 540,986 | 5.410 | 20 | 20 | fits | 82,792 | 41 | 0.764 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 148,505 | 1.485 | 20 | 24 | fits | 148,691 | 145 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 300,063 | 3.001 | 20 | 24 | fits | 152,548 | 198 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 299,997 | 3.000 | 20 | 50 | fits | 152,548 | 198 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 461,218 | 4.612 | 20 | 50 | fits | 151,361 | 186 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 543,944 | 5.439 | 20 | 20 | fits | 82,792 | 41 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 924,459 | 9.245 | 20 | 20 | fits | 41,669 | 16 | 0.761 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 14,151 | 0.142 | 20 | 50 | fits | 33,791 | 43 | 0.731 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 16,241 | 0.162 | 20 | 50 | fits | 29,408 | 35 | 0.727 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 23,046 | 0.230 | 20 | 50 | fits | 29,333 | 35 | 0.721 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 15,629 | 0.156 | 20 | 50 | fits | 34,491 | 61 | 0.641 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 17,598 | 0.176 | 20 | 50 | fits | 34,491 | 61 | 0.641 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,280 | 0.113 | 20 | 50 | fits | 27,662 | 30 | 0.635 |
| LINK_UP | `adp.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,642 | 0.206 | 20 | 200 | fits | 27,497 | 23 (39) | 0.740 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,491 | 0.055 | 20 | 200 | fits | 20,810 | 16 (31) | 0.655 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
