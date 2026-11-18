### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 23 paths and 0 of 144 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.200 (0.424) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.113 (0.491) | fits | 0 adp | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.234 (0.675) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.029 (0.267) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `fixture.link_up.if0` (fixture) | 0.028 (0.278) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.589 (5.360) | fits | 7 adp | 11 | 0 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.329 (0.479) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.181 (0.518) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.091 (0.220) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.110 (0.278) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.156 (0.518) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.183 (0.501) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-3.service.acmp.first.if0` (backlog-adp@blank-3) | 3.667 | fits | 0 acmp | 12 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.acmp.last.if0` (backlog-adp@program-aged2-7) | 5.210 | fits | 11 acmp | 12 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-3.service.adp.first.if0` (backlog-adp@blank-3) | 3.657 | fits | 0 adp | 12 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.203 | fits | 7 adp | 12 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-3.service.aecp.first.if0` (backlog-adp@blank-3) | 2.091 | fits | 0 aecp | 12 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-3.service.aecp.last.if0` (backlog-adp@blank-3) | 3.693 | fits | 15 aecp | 12 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-3.service.maap.first.if0` (backlog-adp@blank-3) | 3.693 | fits | 0 maap | 12 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.240 | fits | 6 maap | 12 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 6.080 | fits | 0 srp | 12 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.srp.last.if0` (backlog-adp@program-aged2-7) | 10.948 | fits | 31 srp | 12 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.222 (0.223) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-3 | 0 | 13.690 | 12 | 153,370 (1.534) | yes | - |
| backlog-adp@blank-7 | 1 | 13.213 | 12 | 146,655 (1.467) | yes | - |
| backlog-adp@program-7 | 0 | 11.581 | 11 | 152,957 (1.530) | yes | - |
| backlog-adp@verify-7 | 0 | 13.413 | 11 | 152,657 (1.527) | yes | - |
| backlog-adp@blank-aged2-7 | 1 | 13.850 | 11 | 145,954 (1.460) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 14.136 | 12 | 149,087 (1.491) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 14.045 | 14 | 151,393 (1.514) | yes | - |
| backlog-adp@program-aged1-7 | 1 | 14.059 | 13 | 149,930 (1.499) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 13.870 | 11 | 150,255 (1.503) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 14.119 | 12 | 151,397 (1.514) | yes | - |
| backlog-adp | 0 | 10.616 | 11 | 151,773 (1.518) | yes | - |
| fixture | 0 | 1.294 | 2 | 80,688 (0.807) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill, backlog-owed not run): 151,773 CPU cycles (1.518 ms), backlog-adp.
Over the windows that released their whole load only: 151,773 (1.518 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-3 | 483 | 0 | 153,370 (1.534) | fits |
| backlog-adp@blank-7 | 484 | 0 | 146,655 (1.467) | fits |
| backlog-adp@program-7 | 493 | 0 | 152,957 (1.530) | fits |
| backlog-adp@verify-7 | 499 | 0 | 152,657 (1.527) | fits |
| backlog-adp@blank-aged2-7 | 796 | 0 | 145,954 (1.460) | fits |
| backlog-adp@blank-aged1-7 | 736 | 0 | 152,282 (1.523) | fits |
| backlog-adp@program-aged2-7 | 826 | 0 | 151,393 (1.514) | fits |
| backlog-adp@program-aged1-7 | 765 | 0 | 151,307 (1.513) | fits |
| backlog-adp@verify-aged2-7 | 840 | 0 | 151,519 (1.515) | fits |
| backlog-adp@verify-aged1-7 | 780 | 0 | 151,397 (1.514) | fits |
| backlog-adp | 315 | 0 | 151,773 (1.518) | fits |
| maap | 182 | 0 | 30,398 (0.304) | fits |
| fixture | 151 | 0 | 80,688 (0.807) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-7 | 2 | +4.230 ms, 77,223 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.888 (20) | 9.112 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.081 (20) | 9.919 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.948 (20) | 9.052 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.067 (20) | 9.933 |
| backlog-adp@verify-aged2-7 | 2 | +4.212 ms, 77,773 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.878 (20) | 9.122 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.207 (20) | 9.793 |

Least margin over the aged windows: 9.052 ms, `backlog-adp@program-aged2-7.service.srp.last.if0` at 10.948 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-3 | 342 | 92,500 (0.925) | 76,179 (0.762) |
| backlog-adp@blank-7 | 342 | 91,668 (0.917) | 76,234 (0.762) |
| backlog-adp@program-7 | 373 | 95,349 (0.953) | 78,491 (0.785) |
| backlog-adp@verify-7 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@blank-aged2-7 | 340 | 91,686 (0.917) | 76,175 (0.762) |
| backlog-adp@blank-aged1-7 | 340 | 93,288 (0.933) | 76,395 (0.764) |
| backlog-adp@program-aged2-7 | 371 | 95,760 (0.958) | 78,604 (0.786) |
| backlog-adp@program-aged1-7 | 371 | 103,443 (1.034) | 78,835 (0.788) |
| backlog-adp@verify-aged2-7 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@verify-aged1-7 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp | 271 | 22,571 (0.226) | 2,593 (0.026) |
| maap | 169 | 22,571 (0.226) | 2,593 (0.026) |
| fixture | 54 | 20,094 (0.201) | 2,593 (0.026) |

Longest pass that carries a step: 103,443 CPU cycles (1.034 ms), backlog-adp@program-aged1-7; longest step: 78,835 (0.788 ms), backlog-adp@program-aged1-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 430,433 | 4.304 | 20 | 20 | fits | 125,344 | 181 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 365,746 | 3.657 | 20 | 200 | fits | 149,967 | 220 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 490,474 | 4.905 | 20 | 200 | fits | 125,344 | 181 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 366,670 | 3.667 | 20 | 20 | fits | 149,967 | 220 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 491,178 | 4.912 | 20 | 20 | fits | 125,344 | 181 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 209,082 | 2.091 | 20 | 24 | fits | 153,370 | 156 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 369,320 | 3.693 | 20 | 24 | fits | 149,967 | 220 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 369,254 | 3.693 | 20 | 50 | fits | 149,967 | 220 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 494,202 | 4.942 | 20 | 50 | fits | 125,344 | 181 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 578,333 | 5.783 | 20 | 20 | fits | 84,197 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,091,749 | 10.917 | 20 | 20 | fits | 81,599 | 31 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 369,128 | 3.691 | 20 | 20 | fits | 132,423 | 202 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 297,344 | 2.973 | 20 | 200 | fits | 146,655 | 208 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 429,151 | 4.292 | 20 | 200 | fits | 132,423 | 202 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 298,268 | 2.983 | 20 | 20 | fits | 146,655 | 208 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 429,855 | 4.299 | 20 | 20 | fits | 132,423 | 202 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 143,842 | 1.438 | 20 | 24 | fits | 145,885 | 146 | 0.447 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 300,918 | 3.009 | 20 | 24 | fits | 146,655 | 208 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 300,852 | 3.009 | 20 | 50 | fits | 146,655 | 208 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 432,879 | 4.329 | 20 | 50 | fits | 132,423 | 202 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 517,010 | 5.170 | 20 | 20 | fits | 84,197 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,024,586 | 10.246 | 20 | 20 | fits | 75,759 | 25 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 368,985 | 3.690 | 20 | 20 | fits | 119,642 | 184 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 302,472 | 3.025 | 20 | 200 | fits | 150,917 | 209 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 421,498 | 4.215 | 20 | 200 | fits | 119,642 | 184 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 303,396 | 3.034 | 20 | 20 | fits | 150,917 | 209 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 422,202 | 4.222 | 20 | 20 | fits | 119,642 | 184 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 156,119 | 1.561 | 20 | 24 | fits | 152,957 | 155 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 306,046 | 3.060 | 20 | 24 | fits | 150,917 | 209 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 305,980 | 3.060 | 20 | 50 | fits | 150,917 | 209 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 425,226 | 4.252 | 20 | 50 | fits | 119,642 | 184 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 509,893 | 5.099 | 20 | 20 | fits | 84,733 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,016,300 | 10.163 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 399,593 | 3.996 | 20 | 20 | fits | 113,487 | 163 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 346,787 | 3.468 | 20 | 200 | fits | 149,259 | 226 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 459,658 | 4.597 | 20 | 200 | fits | 113,487 | 163 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 347,711 | 3.477 | 20 | 20 | fits | 149,259 | 226 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 460,362 | 4.604 | 20 | 20 | fits | 113,487 | 163 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 202,092 | 2.021 | 20 | 24 | fits | 152,657 | 155 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 350,361 | 3.504 | 20 | 24 | fits | 149,259 | 226 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 350,295 | 3.503 | 20 | 50 | fits | 149,259 | 226 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 463,386 | 4.634 | 20 | 50 | fits | 113,487 | 163 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 548,003 | 5.480 | 20 | 20 | fits | 84,683 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,060,895 | 10.609 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 356,782 | 3.568 | 20 | 20 | fits | 140,508 | 208 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 277,727 | 2.777 | 20 | 200 | fits | 145,954 | 208 | 0.443 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 417,619 | 4.176 | 20 | 200 | fits | 140,508 | 208 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 278,651 | 2.787 | 20 | 20 | fits | 145,954 | 208 | 0.443 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 418,323 | 4.183 | 20 | 20 | fits | 140,508 | 208 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 136,337 | 1.363 | 20 | 24 | fits | 142,764 | 147 | 0.434 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 281,301 | 2.813 | 20 | 24 | fits | 145,954 | 208 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 281,235 | 2.812 | 20 | 50 | fits | 145,954 | 208 | 0.443 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 421,347 | 4.213 | 20 | 50 | fits | 140,508 | 208 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 582,395 | 5.824 | 20 | 20 | fits | 83,891 | 25 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,088,838 | 10.888 | 20 | 20 | fits | 73,052 | 24 | 0.641 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 375,494 | 3.755 | 20 | 20 | fits | 126,400 | 198 | 0.480 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 292,574 | 2.926 | 20 | 200 | fits | 149,087 | 234 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 429,682 | 4.297 | 20 | 200 | fits | 126,400 | 198 | 0.480 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 293,498 | 2.935 | 20 | 20 | fits | 149,087 | 234 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 430,386 | 4.304 | 20 | 20 | fits | 126,400 | 198 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 148,051 | 1.481 | 20 | 24 | fits | 152,282 | 120 | 0.434 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 296,148 | 2.961 | 20 | 24 | fits | 149,087 | 234 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 296,082 | 2.961 | 20 | 50 | fits | 149,087 | 234 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 433,410 | 4.334 | 20 | 50 | fits | 126,400 | 198 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 521,053 | 5.211 | 20 | 20 | fits | 87,709 | 30 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,008,095 | 10.081 | 20 | 20 | fits | 59,768 | 20 | 0.683 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 458,887 | 4.589 | 20 | 20 | fits | 129,039 | 181 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 301,148 | 3.011 | 20 | 200 | fits | 148,377 | 221 | 0.447 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 520,288 | 5.203 | 20 | 200 | fits | 129,039 | 181 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 302,072 | 3.021 | 20 | 20 | fits | 148,377 | 221 | 0.447 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 520,992 | 5.210 | 20 | 20 | fits | 129,039 | 181 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 157,335 | 1.573 | 20 | 24 | fits | 151,393 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 304,722 | 3.047 | 20 | 24 | fits | 148,377 | 221 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 304,656 | 3.047 | 20 | 50 | fits | 148,377 | 221 | 0.447 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 524,016 | 5.240 | 20 | 50 | fits | 129,039 | 181 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 607,979 | 6.080 | 20 | 20 | fits | 84,029 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,094,753 | 10.948 | 20 | 20 | fits | 59,768 | 20 | 0.683 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 355,498 | 3.555 | 20 | 20 | fits | 122,370 | 170 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 294,453 | 2.945 | 20 | 200 | fits | 149,930 | 231 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 416,207 | 4.162 | 20 | 200 | fits | 122,370 | 170 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 295,377 | 2.954 | 20 | 20 | fits | 149,930 | 231 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 416,911 | 4.169 | 20 | 20 | fits | 122,370 | 170 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 149,087 | 1.491 | 20 | 24 | fits | 151,307 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 298,027 | 2.980 | 20 | 24 | fits | 149,930 | 231 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 297,961 | 2.980 | 20 | 50 | fits | 149,930 | 231 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 419,935 | 4.199 | 20 | 50 | fits | 122,370 | 170 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 519,798 | 5.198 | 20 | 20 | fits | 88,074 | 31 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,006,722 | 10.067 | 20 | 20 | fits | 59,768 | 20 | 0.683 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 363,042 | 3.630 | 20 | 20 | fits | 122,564 | 169 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 293,859 | 2.939 | 20 | 200 | fits | 150,255 | 231 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 415,807 | 4.158 | 20 | 200 | fits | 122,564 | 169 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 294,783 | 2.948 | 20 | 20 | fits | 150,255 | 231 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 416,511 | 4.165 | 20 | 20 | fits | 122,564 | 169 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 148,168 | 1.482 | 20 | 24 | fits | 151,519 | 152 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 297,433 | 2.974 | 20 | 24 | fits | 150,255 | 231 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 297,367 | 2.974 | 20 | 50 | fits | 150,255 | 231 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 419,535 | 4.195 | 20 | 50 | fits | 122,564 | 169 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 580,936 | 5.809 | 20 | 20 | fits | 83,694 | 26 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,087,775 | 10.878 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 374,585 | 3.746 | 20 | 20 | fits | 120,391 | 187 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 306,037 | 3.060 | 20 | 200 | fits | 149,501 | 205 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 425,812 | 4.258 | 20 | 200 | fits | 120,391 | 187 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 306,961 | 3.070 | 20 | 20 | fits | 149,501 | 205 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 426,516 | 4.265 | 20 | 20 | fits | 120,391 | 187 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 161,100 | 1.611 | 20 | 24 | fits | 151,397 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 309,611 | 3.096 | 20 | 24 | fits | 149,501 | 205 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 309,545 | 3.095 | 20 | 50 | fits | 149,501 | 205 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 429,540 | 4.295 | 20 | 50 | fits | 120,391 | 187 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 513,903 | 5.139 | 20 | 20 | fits | 84,429 | 24 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,020,659 | 10.207 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 373,338 | 3.733 | 20 | 20 | fits | 120,105 | 173 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 295,152 | 2.952 | 20 | 200 | fits | 148,129 | 223 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 425,977 | 4.260 | 20 | 200 | fits | 120,105 | 173 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 296,076 | 2.961 | 20 | 20 | fits | 148,129 | 223 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 426,681 | 4.267 | 20 | 20 | fits | 120,105 | 173 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 151,587 | 1.516 | 20 | 24 | fits | 151,773 | 155 | 0.422 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 298,726 | 2.987 | 20 | 24 | fits | 148,129 | 223 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 298,660 | 2.987 | 20 | 50 | fits | 148,129 | 223 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 429,705 | 4.297 | 20 | 50 | fits | 120,105 | 173 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 513,841 | 5.138 | 20 | 20 | fits | 84,202 | 24 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,007,658 | 10.077 | 20 | 20 | fits | 72,980 | 24 | 0.639 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,034 | 0.110 | 20 | 50 | fits | 27,812 | 43 | 0.720 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 18,262 | 0.183 | 20 | 50 | fits | 24,210 | 35 | 0.691 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 17,399 | 0.174 | 20 | 50 | fits | 24,142 | 35 | 0.691 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 15,584 | 0.156 | 20 | 50 | fits | 29,701 | 61 | 0.622 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 18,123 | 0.181 | 20 | 50 | fits | 29,701 | 61 | 0.622 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,091 | 0.091 | 20 | 50 | fits | 21,998 | 30 | 0.596 |
| LINK_UP | `fixture.link_up.if0` | 2,771 | 0.028 | 20 | 200 | fits | 27,812 | 43 (11) | 0.720 |
| malformed MRPDU discard | `fixture.malformed.if0` | 22,200 | 0.222 | 20 | 20 | fits | 22,266 | 12 | 0.723 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,876 | 0.329 | 20 | 24 | fits | 47,892 | 43 | 0.784 |
| LINK_DOWN | `fixture.link_down.if0` | 2,878 | 0.029 | 20 | 200 | fits | 26,676 | 23 (9) | 0.763 |
| BIND_RX | `fixture.bind_rx.if0` | 20,000 | 0.200 | 20 | 20 | fits | 42,357 | 26 (77) | 0.795 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 23,438 | 0.234 | 20 | 20 | fits | 37,979 | 29 (35) | 0.793 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 11,298 | 0.113 | 20 | 20 | fits | 25,732 | 13 (29) | 0.790 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 80,584 | 0.806 | 20 | 200 | fits | 80,688 | 51 | 0.765 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 80,584 | 0.806 | 20 | 200 | fits | 80,688 | 51 | 0.765 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 80,310 | 0.803 | 20 | 20 | fits | 80,688 | 51 | 0.765 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 80,310 | 0.803 | 20 | 20 | fits | 80,688 | 51 | 0.765 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 80,518 | 0.805 | 20 | 24 | fits | 80,688 | 51 | 0.765 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 80,518 | 0.805 | 20 | 24 | fits | 80,688 | 51 | 0.765 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 80,452 | 0.805 | 20 | 50 | fits | 80,688 | 51 | 0.765 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 80,452 | 0.805 | 20 | 50 | fits | 80,688 | 51 | 0.765 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 80,386 | 0.804 | 20 | 20 | fits | 80,688 | 51 | 0.765 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 80,386 | 0.804 | 20 | 20 | fits | 80,688 | 51 | 0.765 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
