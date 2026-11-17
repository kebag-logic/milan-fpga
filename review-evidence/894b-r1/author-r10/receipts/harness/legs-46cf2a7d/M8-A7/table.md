### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 23 paths and 0 of 144 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.218 (0.469) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.194 (0.615) | fits | 0 adp | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.146 (0.670) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.027 (0.322) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `fixture.link_up.if0` (fixture) | 0.029 (0.336) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-5.adp_available.if0` (backlog-adp@program-aged2-5) | 4.177 (4.699) | fits | 7 adp | 11 | 0 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.345 (0.495) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.241 (0.640) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.121 (0.284) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.141 (0.336) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.223 (0.640) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.198 (0.584) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-5.service.acmp.first.if0` (backlog-adp@program-5) | 3.146 | fits | 0 acmp | 12 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.acmp.last.if0` (backlog-adp@program-aged2-5) | 6.868 | fits | 11 acmp | 12 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-5.service.adp.first.if0` (backlog-adp@program-5) | 3.137 | fits | 0 adp | 12 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.adp.last.if0` (backlog-adp@verify-aged2-5) | 4.681 | fits | 7 adp | 12 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-aged2-5.service.aecp.first.if0` (backlog-adp@program-aged2-5) | 1.623 | fits | 0 aecp | 12 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@program-5.service.aecp.last.if0` (backlog-adp@program-5) | 3.173 | fits | 15 aecp | 12 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-5.service.maap.first.if0` (backlog-adp@program-5) | 3.172 | fits | 0 maap | 12 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.maap.last.if0` (backlog-adp@verify-aged2-5) | 4.718 | fits | 6 maap | 12 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-5.service.srp.first.if0` (backlog-adp@program-aged2-5) | 6.897 | fits | 0 srp | 12 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.srp.last.if0` (backlog-adp@program-aged2-5) | 9.334 | fits | 31 srp | 12 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.240 (0.241) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-3 | 0 | 9.849 | 7 | 154,558 (1.546) | yes | - |
| backlog-adp@blank-7 | 0 | 10.033 | 8 | 153,315 (1.533) | yes | - |
| backlog-adp@program-5 | 0 | 9.131 | 7 | 154,757 (1.548) | yes | - |
| backlog-adp@verify-5 | 0 | 9.819 | 7 | 150,471 (1.505) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 9.911 | 7 | 152,744 (1.527) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 9.927 | 7 | 153,058 (1.531) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 9.977 | 7 | 153,328 (1.533) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 9.897 | 7 | 153,519 (1.535) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 9.900 | 7 | 155,868 (1.559) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 9.780 | 6 | 152,988 (1.530) | yes | - |
| backlog-adp | 0 | 9.036 | 7 | 154,127 (1.541) | yes | - |
| fixture | 0 | 1.424 | 2 | 83,472 (0.835) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill, backlog-owed not run): 154,127 CPU cycles (1.541 ms), backlog-adp.
Over the windows that released their whole load only: 154,127 (1.541 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-3 | 554 | 0 | 154,558 (1.546) | fits |
| backlog-adp@blank-7 | 557 | 0 | 153,315 (1.533) | fits |
| backlog-adp@program-5 | 940 | 0 | 154,757 (1.548) | fits |
| backlog-adp@verify-5 | 1314 | 0 | 150,471 (1.505) | fits |
| backlog-adp@blank-aged2-5 | 828 | 0 | 152,744 (1.527) | fits |
| backlog-adp@blank-aged1-6 | 784 | 0 | 153,058 (1.531) | fits |
| backlog-adp@program-aged2-5 | 1207 | 0 | 153,328 (1.533) | fits |
| backlog-adp@program-aged1-5 | 1156 | 0 | 153,519 (1.535) | fits |
| backlog-adp@verify-aged2-5 | 1587 | 0 | 155,868 (1.559) | fits |
| backlog-adp@verify-aged1-5 | 1536 | 0 | 152,988 (1.530) | fits |
| backlog-adp | 309 | 0 | 154,127 (1.541) | fits |
| maap | 179 | 0 | 34,872 (0.349) | fits |
| fixture | 151 | 0 | 83,472 (0.835) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-5 | 2 | +5.979 ms, 76,738 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.270 (20) | 10.730 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 8.529 (20) | 11.471 |
| backlog-adp@program-aged2-5 | 2 | none | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.334 (20) | 10.666 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.454 (20) | 11.546 |
| backlog-adp@verify-aged2-5 | 2 | +4.734 ms, 77,749 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.255 (20) | 10.745 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.373 (20) | 11.627 |

Least margin over the aged windows: 10.666 ms, `backlog-adp@program-aged2-5.service.srp.last.if0` at 9.334 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-3 | 339 | 95,632 (0.956) | 75,943 (0.759) |
| backlog-adp@blank-7 | 339 | 94,603 (0.946) | 75,929 (0.759) |
| backlog-adp@program-5 | 449 | 100,322 (1.003) | 77,944 (0.779) |
| backlog-adp@verify-5 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@blank-aged2-5 | 337 | 79,120 (0.791) | 75,467 (0.755) |
| backlog-adp@blank-aged1-6 | 337 | 95,893 (0.959) | 75,944 (0.759) |
| backlog-adp@program-aged2-5 | 446 | 100,322 (1.003) | 78,131 (0.781) |
| backlog-adp@program-aged1-5 | 446 | 100,322 (1.003) | 78,354 (0.784) |
| backlog-adp@verify-aged2-5 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@verify-aged1-5 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp | 271 | 25,989 (0.260) | 2,306 (0.023) |
| maap | 166 | 25,989 (0.260) | 2,306 (0.023) |
| fixture | 54 | 20,829 (0.208) | 2,306 (0.023) |

Longest pass that carries a step: 104,189 CPU cycles (1.042 ms), backlog-adp@verify-5; longest step: 78,354 (0.784 ms), backlog-adp@program-aged1-5.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 393,151 | 3.932 | 20 | 20 | fits | 154,558 | 196 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 299,356 | 2.994 | 20 | 200 | fits | 149,354 | 192 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 453,298 | 4.533 | 20 | 200 | fits | 154,558 | 196 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 300,280 | 3.003 | 20 | 20 | fits | 149,354 | 192 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 586,442 | 5.864 | 20 | 20 | fits | 132,440 | 56 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 154,566 | 1.546 | 20 | 24 | fits | 149,260 | 145 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 302,930 | 3.029 | 20 | 24 | fits | 149,354 | 192 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 302,864 | 3.029 | 20 | 50 | fits | 149,354 | 192 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 457,026 | 4.570 | 20 | 50 | fits | 154,558 | 196 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 589,400 | 5.894 | 20 | 20 | fits | 132,440 | 56 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 845,340 | 8.453 | 20 | 20 | fits | 110,153 | 48 | 0.509 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 399,367 | 3.994 | 20 | 20 | fits | 153,315 | 208 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 297,370 | 2.974 | 20 | 200 | fits | 148,109 | 174 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 450,069 | 4.501 | 20 | 200 | fits | 153,315 | 208 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 298,294 | 2.983 | 20 | 20 | fits | 148,109 | 174 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 583,258 | 5.833 | 20 | 20 | fits | 132,485 | 61 | 0.600 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 153,825 | 1.538 | 20 | 24 | fits | 148,720 | 145 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 300,944 | 3.009 | 20 | 24 | fits | 148,109 | 174 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 300,878 | 3.009 | 20 | 50 | fits | 148,109 | 174 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 453,797 | 4.538 | 20 | 50 | fits | 153,315 | 208 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 586,216 | 5.862 | 20 | 20 | fits | 132,485 | 61 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 829,955 | 8.300 | 20 | 20 | fits | 118,402 | 53 | 0.483 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 407,603 | 4.076 | 20 | 20 | fits | 154,757 | 196 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 313,685 | 3.137 | 20 | 200 | fits | 151,981 | 197 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 467,826 | 4.678 | 20 | 200 | fits | 154,757 | 196 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 314,609 | 3.146 | 20 | 20 | fits | 151,981 | 197 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 600,036 | 6.000 | 20 | 20 | fits | 131,506 | 55 | 0.621 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 156,573 | 1.566 | 20 | 24 | fits | 149,234 | 146 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 317,259 | 3.173 | 20 | 24 | fits | 151,981 | 197 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 317,193 | 3.172 | 20 | 50 | fits | 151,981 | 197 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 471,554 | 4.716 | 20 | 50 | fits | 154,757 | 196 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 602,994 | 6.030 | 20 | 20 | fits | 131,506 | 55 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 843,682 | 8.437 | 20 | 20 | fits | 115,351 | 54 | 0.552 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 402,749 | 4.027 | 20 | 20 | fits | 150,471 | 193 | 0.385 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 294,025 | 2.940 | 20 | 200 | fits | 149,556 | 193 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 454,020 | 4.540 | 20 | 200 | fits | 150,471 | 193 | 0.385 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 294,949 | 2.949 | 20 | 20 | fits | 149,556 | 193 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 585,678 | 5.857 | 20 | 20 | fits | 130,954 | 65 | 0.625 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 149,033 | 1.490 | 20 | 24 | fits | 149,055 | 145 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 297,599 | 2.976 | 20 | 24 | fits | 149,556 | 193 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 297,533 | 2.975 | 20 | 50 | fits | 149,556 | 193 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 457,748 | 4.577 | 20 | 50 | fits | 150,471 | 193 | 0.385 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 588,636 | 5.886 | 20 | 20 | fits | 130,954 | 65 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 840,714 | 8.407 | 20 | 20 | fits | 126,468 | 56 | 0.471 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 384,733 | 3.847 | 20 | 20 | fits | 152,744 | 205 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 301,560 | 3.016 | 20 | 200 | fits | 150,938 | 180 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 453,688 | 4.537 | 20 | 200 | fits | 152,744 | 205 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 302,484 | 3.025 | 20 | 20 | fits | 150,938 | 180 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 593,250 | 5.933 | 20 | 20 | fits | 138,858 | 63 | 0.630 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 155,186 | 1.552 | 20 | 24 | fits | 147,816 | 142 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 305,134 | 3.051 | 20 | 24 | fits | 150,938 | 180 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 305,068 | 3.051 | 20 | 50 | fits | 150,938 | 180 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 457,416 | 4.574 | 20 | 50 | fits | 152,744 | 205 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 596,208 | 5.962 | 20 | 20 | fits | 138,858 | 63 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 927,018 | 9.270 | 20 | 20 | fits | 112,168 | 49 | 0.549 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 414,102 | 4.141 | 20 | 20 | fits | 153,058 | 205 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 303,479 | 3.035 | 20 | 200 | fits | 149,384 | 176 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 455,921 | 4.559 | 20 | 200 | fits | 153,058 | 205 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 304,403 | 3.044 | 20 | 20 | fits | 149,384 | 176 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 588,998 | 5.890 | 20 | 20 | fits | 132,373 | 61 | 0.600 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 158,659 | 1.587 | 20 | 24 | fits | 147,758 | 142 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 307,053 | 3.071 | 20 | 24 | fits | 149,384 | 176 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 306,987 | 3.070 | 20 | 50 | fits | 149,384 | 176 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 459,649 | 4.596 | 20 | 50 | fits | 153,058 | 205 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 591,956 | 5.920 | 20 | 20 | fits | 132,373 | 61 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 852,881 | 8.529 | 20 | 20 | fits | 124,485 | 59 | 0.562 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 417,740 | 4.177 | 20 | 20 | fits | 153,328 | 206 | 0.381 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 307,048 | 3.070 | 20 | 200 | fits | 149,289 | 176 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 459,760 | 4.598 | 20 | 200 | fits | 153,328 | 206 | 0.381 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 307,972 | 3.080 | 20 | 20 | fits | 149,289 | 176 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 686,792 | 6.868 | 20 | 20 | fits | 136,502 | 68 | 0.621 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 162,323 | 1.623 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 310,622 | 3.106 | 20 | 24 | fits | 149,289 | 176 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 310,556 | 3.106 | 20 | 50 | fits | 149,289 | 176 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 463,488 | 4.635 | 20 | 50 | fits | 153,328 | 206 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 689,750 | 6.897 | 20 | 20 | fits | 136,502 | 68 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 933,377 | 9.334 | 20 | 20 | fits | 118,437 | 52 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 400,481 | 4.005 | 20 | 20 | fits | 153,519 | 209 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 298,322 | 2.983 | 20 | 200 | fits | 149,247 | 176 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 451,225 | 4.512 | 20 | 200 | fits | 153,519 | 209 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 299,246 | 2.992 | 20 | 20 | fits | 149,247 | 176 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 590,195 | 5.902 | 20 | 20 | fits | 138,266 | 63 | 0.629 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 153,639 | 1.536 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 301,896 | 3.019 | 20 | 24 | fits | 149,247 | 176 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 301,830 | 3.018 | 20 | 50 | fits | 149,247 | 176 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 454,953 | 4.550 | 20 | 50 | fits | 153,519 | 209 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 593,153 | 5.932 | 20 | 20 | fits | 138,266 | 63 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 845,397 | 8.454 | 20 | 20 | fits | 115,663 | 55 | 0.576 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 407,951 | 4.080 | 20 | 20 | fits | 155,868 | 208 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 302,549 | 3.025 | 20 | 200 | fits | 151,159 | 181 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 468,051 | 4.681 | 20 | 200 | fits | 155,868 | 208 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 303,473 | 3.035 | 20 | 20 | fits | 151,159 | 181 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 678,680 | 6.787 | 20 | 20 | fits | 132,176 | 62 | 0.594 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 155,954 | 1.560 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 306,123 | 3.061 | 20 | 24 | fits | 151,159 | 181 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 306,057 | 3.061 | 20 | 50 | fits | 151,159 | 181 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 471,779 | 4.718 | 20 | 50 | fits | 155,868 | 208 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 681,638 | 6.816 | 20 | 20 | fits | 132,176 | 62 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 925,464 | 9.255 | 20 | 20 | fits | 118,245 | 52 | 0.482 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 376,394 | 3.764 | 20 | 20 | fits | 152,988 | 206 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 293,258 | 2.933 | 20 | 200 | fits | 152,047 | 185 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 445,630 | 4.456 | 20 | 200 | fits | 152,988 | 206 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 294,182 | 2.942 | 20 | 20 | fits | 152,047 | 185 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 590,344 | 5.903 | 20 | 20 | fits | 133,656 | 66 | 0.654 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 145,775 | 1.458 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 296,832 | 2.968 | 20 | 24 | fits | 152,047 | 185 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 296,766 | 2.968 | 20 | 50 | fits | 152,047 | 185 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 449,358 | 4.494 | 20 | 50 | fits | 152,988 | 206 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 593,302 | 5.933 | 20 | 20 | fits | 133,656 | 66 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 837,324 | 8.373 | 20 | 20 | fits | 118,384 | 52 | 0.485 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 391,435 | 3.914 | 20 | 20 | fits | 154,127 | 205 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 296,579 | 2.966 | 20 | 200 | fits | 152,872 | 186 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 460,546 | 4.605 | 20 | 200 | fits | 154,127 | 205 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 297,503 | 2.975 | 20 | 20 | fits | 152,872 | 186 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 599,959 | 6.000 | 20 | 20 | fits | 138,709 | 63 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 148,271 | 1.483 | 20 | 24 | fits | 148,457 | 145 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 300,153 | 3.002 | 20 | 24 | fits | 152,872 | 186 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 300,087 | 3.001 | 20 | 50 | fits | 152,872 | 186 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 464,274 | 4.643 | 20 | 50 | fits | 154,127 | 205 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 602,917 | 6.029 | 20 | 20 | fits | 138,709 | 63 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 838,082 | 8.381 | 20 | 20 | fits | 109,575 | 48 | 0.495 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 14,059 | 0.141 | 20 | 50 | fits | 33,635 | 43 | 0.730 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 19,765 | 0.198 | 20 | 50 | fits | 30,015 | 35 | 0.737 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 17,477 | 0.175 | 20 | 50 | fits | 30,196 | 35 | 0.738 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 22,325 | 0.223 | 20 | 50 | fits | 34,872 | 61 | 0.649 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 24,149 | 0.241 | 20 | 50 | fits | 34,872 | 61 | 0.649 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 12,057 | 0.121 | 20 | 50 | fits | 28,419 | 30 | 0.661 |
| LINK_UP | `fixture.link_up.if0` | 2,856 | 0.029 | 20 | 200 | fits | 33,635 | 43 (11) | 0.730 |
| malformed MRPDU discard | `fixture.malformed.if0` | 24,000 | 0.240 | 20 | 20 | fits | 24,066 | 12 | 0.770 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 34,531 | 0.345 | 20 | 24 | fits | 49,479 | 41 | 0.790 |
| LINK_DOWN | `fixture.link_down.if0` | 2,710 | 0.027 | 20 | 200 | fits | 32,185 | 23 (9) | 0.798 |
| BIND_RX | `fixture.bind_rx.if0` | 21,771 | 0.218 | 20 | 20 | fits | 46,880 | 26 (77) | 0.795 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 14,615 | 0.146 | 20 | 20 | fits | 45,101 | 29 (35) | 0.792 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 19,354 | 0.194 | 20 | 20 | fits | 31,466 | 13 (29) | 0.822 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 83,368 | 0.834 | 20 | 200 | fits | 83,472 | 51 | 0.754 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 83,368 | 0.834 | 20 | 200 | fits | 83,472 | 51 | 0.754 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 83,094 | 0.831 | 20 | 20 | fits | 83,472 | 51 | 0.754 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 83,094 | 0.831 | 20 | 20 | fits | 83,472 | 51 | 0.754 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 83,302 | 0.833 | 20 | 24 | fits | 83,472 | 51 | 0.754 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 83,302 | 0.833 | 20 | 24 | fits | 83,472 | 51 | 0.754 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 83,236 | 0.832 | 20 | 50 | fits | 83,472 | 51 | 0.754 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 83,236 | 0.832 | 20 | 50 | fits | 83,472 | 51 | 0.754 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 83,170 | 0.832 | 20 | 20 | fits | 83,472 | 51 | 0.754 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 83,170 | 0.832 | 20 | 20 | fits | 83,472 | 51 | 0.754 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
