### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 20 paths and 0 of 231 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.281 (0.772) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.054 (0.206) | fits | 0 adp | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-discover) | 0.030 (0.337) | fits | 0 events | 2 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-discover) | 0.150 (0.535) | fits | 0 events | 2 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.961 (5.563) | fits | 7 adp | 19 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.148 (0.612) | fits | 0 adp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 3.802 | fits | 0 acmp | 20 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.acmp.last.if0` (backlog-adp@program-aged2-7) | 6.239 | fits | 11 acmp | 20 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 3.793 | fits | 0 adp | 20 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.396 | fits | 7 adp | 20 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.340 | fits | 0 aecp | 20 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.aecp.last.if0` (backlog-adp@blank-0) | 3.829 | fits | 15 aecp | 20 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 3.828 | fits | 0 maap | 20 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.434 | fits | 6 maap | 20 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 6.269 | fits | 0 srp | 20 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.srp.last.if0` (backlog-adp@program-aged2-7) | 10.179 | fits | 31 srp | 20 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.787 (0.831) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.441 (0.441) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.230 (0.231) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.797 (0.867) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.420 | 10 | 158,124 (1.581) | yes | - |
| backlog-adp@blank-3 | 0 | 10.622 | 10 | 158,379 (1.584) | yes | - |
| backlog-adp@blank-7 | 0 | 10.625 | 10 | 156,306 (1.563) | yes | - |
| backlog-adp@program-3 | 0 | 10.656 | 10 | 156,306 (1.563) | yes | - |
| backlog-adp@program-7 | 0 | 9.842 | 10 | 156,689 (1.567) | yes | - |
| backlog-adp@verify-3 | 0 | 10.623 | 10 | 158,379 (1.584) | yes | - |
| backlog-adp@verify-7 | 0 | 10.687 | 10 | 156,306 (1.563) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.622 | 10 | 155,880 (1.559) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.586 | 10 | 151,492 (1.515) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 10.528 | 9 | 159,488 (1.595) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 10.657 | 10 | 156,473 (1.565) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.430 | 9 | 158,459 (1.585) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 11.488 | 12 | 149,999 (1.500) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.580 | 9 | 158,847 (1.588) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.698 | 12 | 151,019 (1.510) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.648 | 10 | 158,379 (1.584) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.597 | 10 | 156,548 (1.565) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.685 | 10 | 158,459 (1.585) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.397 | 13 | 149,982 (1.500) | yes | - |
| backlog-adp-refill | 0 | 40.972 | 23 | 155,196 (1.552) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-owed not run): 155,196 CPU cycles (1.552 ms), backlog-adp-refill.
Over the windows that released their whole load only: 155,196 (1.552 ms), backlog-adp-refill.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3605 | 0 | 45,817 (0.458) | fits |
| backlog-adp@blank-0 | 537 | 0 | 158,124 (1.581) | fits |
| backlog-adp@blank-3 | 537 | 0 | 158,379 (1.584) | fits |
| backlog-adp@blank-7 | 539 | 0 | 156,306 (1.563) | fits |
| backlog-adp@program-3 | 895 | 0 | 156,306 (1.563) | fits |
| backlog-adp@program-7 | 898 | 0 | 156,689 (1.567) | fits |
| backlog-adp@verify-3 | 1243 | 0 | 158,379 (1.584) | fits |
| backlog-adp@verify-7 | 1245 | 0 | 156,306 (1.563) | fits |
| backlog-adp@blank-aged2-3 | 798 | 0 | 155,880 (1.559) | fits |
| backlog-adp@blank-aged2-7 | 823 | 0 | 151,492 (1.515) | fits |
| backlog-adp@blank-aged1-3 | 747 | 0 | 159,488 (1.595) | fits |
| backlog-adp@blank-aged1-7 | 773 | 0 | 156,473 (1.565) | fits |
| backlog-adp@program-aged2-3 | 1149 | 0 | 158,459 (1.585) | fits |
| backlog-adp@program-aged2-7 | 1177 | 0 | 149,999 (1.500) | fits |
| backlog-adp@program-aged1-3 | 1099 | 0 | 158,847 (1.588) | fits |
| backlog-adp@program-aged1-7 | 1127 | 0 | 151,019 (1.510) | fits |
| backlog-adp@verify-aged2-3 | 1503 | 0 | 158,379 (1.584) | fits |
| backlog-adp@verify-aged2-7 | 1528 | 0 | 156,548 (1.565) | fits |
| backlog-adp@verify-aged1-3 | 1453 | 0 | 158,459 (1.585) | fits |
| backlog-adp@verify-aged1-7 | 1481 | 0 | 149,982 (1.500) | fits |
| srp | 290 | 0 | 44,123 (0.441) | fits |
| backlog-adp-refill | 327 | 0 | 155,196 (1.552) | fits |
| adp-discover | 88 | 0 | 33,705 (0.337) | fits |
| control | 88 | 0 | 33,705 (0.337) | fits |
| datapath-events | 116 | 0 | 33,705 (0.337) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-3 | 2 | +7.079 ms, 76,795 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.985 (20) | 10.015 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.944 (20) | 10.056 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.128 (20) | 10.872 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.263 (20) | 10.737 |
| backlog-adp@program-aged2-3 | 2 | +7.346 ms, 80,205 (0.802 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.788 (20) | 10.212 |
| backlog-adp@program-aged2-7 | 2 | +3.148 ms, 80,189 (0.802 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.179 (20) | 9.821 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.139 (20) | 10.861 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.299 (20) | 10.701 |
| backlog-adp@verify-aged2-3 | 2 | +7.260 ms, 77,577 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.006 (20) | 9.994 |
| backlog-adp@verify-aged2-7 | 2 | +2.980 ms, 77,717 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.959 (20) | 10.041 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.281 (20) | 10.719 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.262 (20) | 10.738 |

Least margin over the aged windows: 9.821 ms, `backlog-adp@program-aged2-7.service.srp.last.if0` at 10.179 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 108,760 (1.088) | 78,024 (0.780) |
| backlog-adp@blank-0 | 339 | 95,574 (0.956) | 76,095 (0.761) |
| backlog-adp@blank-3 | 339 | 96,110 (0.961) | 76,093 (0.761) |
| backlog-adp@blank-7 | 339 | 95,687 (0.957) | 76,144 (0.761) |
| backlog-adp@program-3 | 448 | 100,633 (1.006) | 78,388 (0.784) |
| backlog-adp@program-7 | 449 | 100,633 (1.006) | 77,865 (0.779) |
| backlog-adp@verify-3 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-7 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@blank-aged2-3 | 337 | 79,331 (0.793) | 75,650 (0.756) |
| backlog-adp@blank-aged2-7 | 337 | 86,224 (0.862) | 75,783 (0.758) |
| backlog-adp@blank-aged1-3 | 337 | 96,251 (0.963) | 76,173 (0.762) |
| backlog-adp@blank-aged1-7 | 337 | 95,767 (0.958) | 76,224 (0.762) |
| backlog-adp@program-aged2-3 | 446 | 100,633 (1.006) | 77,960 (0.780) |
| backlog-adp@program-aged2-7 | 447 | 100,633 (1.006) | 77,865 (0.779) |
| backlog-adp@program-aged1-3 | 446 | 100,633 (1.006) | 78,390 (0.784) |
| backlog-adp@program-aged1-7 | 447 | 100,633 (1.006) | 78,388 (0.784) |
| backlog-adp@verify-aged2-3 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged2-7 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged1-3 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged1-7 | 556 | 104,368 (1.044) | 77,942 (0.779) |
| srp | 271 | 26,258 (0.263) | 2,254 (0.023) |
| backlog-adp-refill | 274 | 26,258 (0.263) | 2,298 (0.023) |
| adp-discover | 79 | 26,196 (0.262) | 2,254 (0.023) |
| control | 79 | 26,196 (0.262) | 2,254 (0.023) |
| datapath-events | 70 | 26,196 (0.262) | 2,254 (0.023) |

Longest pass that carries a step: 108,760 CPU cycles (1.088 ms), acmp-notk; longest step: 78,390 (0.784 ms), backlog-adp@program-aged1-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 28,099 | 0.281 | 20 | 20 | fits | 39,341 | 19 (14) | 0.889 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 474,871 | 4.749 | 20 | 20 | fits | 158,124 | 196 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 379,277 | 3.793 | 20 | 200 | fits | 149,830 | 192 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 536,785 | 5.368 | 20 | 200 | fits | 158,124 | 196 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 380,201 | 3.802 | 20 | 20 | fits | 149,830 | 192 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 619,676 | 6.197 | 20 | 20 | fits | 82,187 | 31 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 234,011 | 2.340 | 20 | 24 | fits | 148,816 | 145 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 382,851 | 3.829 | 20 | 24 | fits | 149,830 | 192 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 382,785 | 3.828 | 20 | 50 | fits | 149,830 | 192 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 540,513 | 5.405 | 20 | 50 | fits | 158,124 | 196 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 622,634 | 6.226 | 20 | 20 | fits | 82,187 | 31 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,002,773 | 10.028 | 20 | 20 | fits | 38,298 | 18 | 0.841 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 395,460 | 3.955 | 20 | 20 | fits | 158,379 | 197 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 299,866 | 2.999 | 20 | 200 | fits | 149,888 | 192 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 457,629 | 4.576 | 20 | 200 | fits | 158,379 | 197 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 300,790 | 3.008 | 20 | 20 | fits | 149,888 | 192 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 555,293 | 5.553 | 20 | 20 | fits | 86,643 | 38 | 0.764 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 154,542 | 1.545 | 20 | 24 | fits | 148,236 | 145 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 303,440 | 3.034 | 20 | 24 | fits | 149,888 | 192 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 303,374 | 3.034 | 20 | 50 | fits | 149,888 | 192 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 461,357 | 4.614 | 20 | 50 | fits | 158,379 | 197 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 558,251 | 5.583 | 20 | 20 | fits | 86,643 | 38 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 922,390 | 9.224 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 401,802 | 4.018 | 20 | 20 | fits | 156,306 | 208 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 298,152 | 2.982 | 20 | 200 | fits | 148,509 | 174 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 453,842 | 4.538 | 20 | 200 | fits | 156,306 | 208 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 299,076 | 2.991 | 20 | 20 | fits | 148,509 | 174 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 537,345 | 5.373 | 20 | 20 | fits | 82,799 | 37 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 154,207 | 1.542 | 20 | 24 | fits | 148,236 | 145 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 301,726 | 3.017 | 20 | 24 | fits | 148,509 | 174 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 301,660 | 3.017 | 20 | 50 | fits | 148,509 | 174 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 457,570 | 4.576 | 20 | 50 | fits | 156,306 | 208 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 540,303 | 5.403 | 20 | 20 | fits | 82,799 | 37 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 923,203 | 9.232 | 20 | 20 | fits | 41,164 | 16 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 401,224 | 4.012 | 20 | 20 | fits | 156,306 | 208 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 297,574 | 2.976 | 20 | 200 | fits | 148,504 | 174 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 453,264 | 4.533 | 20 | 200 | fits | 156,306 | 208 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 298,498 | 2.985 | 20 | 20 | fits | 148,504 | 174 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 536,213 | 5.362 | 20 | 20 | fits | 82,245 | 38 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 153,634 | 1.536 | 20 | 24 | fits | 148,121 | 145 | 0.365 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 301,148 | 3.011 | 20 | 24 | fits | 148,504 | 174 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 301,082 | 3.011 | 20 | 50 | fits | 148,504 | 174 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 456,992 | 4.570 | 20 | 50 | fits | 156,306 | 208 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 539,171 | 5.392 | 20 | 20 | fits | 82,245 | 38 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 921,747 | 9.217 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 395,290 | 3.953 | 20 | 20 | fits | 156,689 | 208 | 0.398 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 291,993 | 2.920 | 20 | 200 | fits | 148,442 | 174 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 448,066 | 4.481 | 20 | 200 | fits | 156,689 | 208 | 0.398 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 292,917 | 2.929 | 20 | 20 | fits | 148,442 | 174 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 545,693 | 5.457 | 20 | 20 | fits | 86,648 | 44 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 148,115 | 1.481 | 20 | 24 | fits | 148,186 | 145 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 295,567 | 2.956 | 20 | 24 | fits | 148,442 | 174 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 295,501 | 2.955 | 20 | 50 | fits | 148,442 | 174 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 451,794 | 4.518 | 20 | 50 | fits | 156,689 | 208 | 0.398 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 548,651 | 5.487 | 20 | 20 | fits | 86,648 | 44 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 914,995 | 9.150 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 394,689 | 3.947 | 20 | 20 | fits | 158,379 | 197 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 299,095 | 2.991 | 20 | 200 | fits | 149,907 | 192 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 456,858 | 4.569 | 20 | 200 | fits | 158,379 | 197 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 300,019 | 3.000 | 20 | 20 | fits | 149,907 | 192 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 554,439 | 5.544 | 20 | 20 | fits | 86,560 | 38 | 0.763 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 153,752 | 1.538 | 20 | 24 | fits | 148,309 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 302,669 | 3.027 | 20 | 24 | fits | 149,907 | 192 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 302,603 | 3.026 | 20 | 50 | fits | 149,907 | 192 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 460,586 | 4.606 | 20 | 50 | fits | 158,379 | 197 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 557,397 | 5.574 | 20 | 20 | fits | 86,560 | 38 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 921,580 | 9.216 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 407,137 | 4.071 | 20 | 20 | fits | 156,306 | 208 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 303,487 | 3.035 | 20 | 200 | fits | 148,506 | 174 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 459,177 | 4.592 | 20 | 200 | fits | 156,306 | 208 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 304,411 | 3.044 | 20 | 20 | fits | 148,506 | 174 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 542,519 | 5.425 | 20 | 20 | fits | 82,638 | 37 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 159,545 | 1.595 | 20 | 24 | fits | 148,417 | 145 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 307,061 | 3.071 | 20 | 24 | fits | 148,506 | 174 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 306,995 | 3.070 | 20 | 50 | fits | 148,506 | 174 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 462,905 | 4.629 | 20 | 50 | fits | 156,306 | 208 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 545,477 | 5.455 | 20 | 20 | fits | 82,638 | 37 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 928,377 | 9.284 | 20 | 20 | fits | 41,164 | 16 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 383,728 | 3.837 | 20 | 20 | fits | 155,880 | 205 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 299,337 | 2.993 | 20 | 200 | fits | 152,308 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 454,601 | 4.546 | 20 | 200 | fits | 155,880 | 205 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 300,261 | 3.003 | 20 | 20 | fits | 152,308 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 537,579 | 5.376 | 20 | 20 | fits | 82,274 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 151,593 | 1.516 | 20 | 24 | fits | 147,246 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 302,911 | 3.029 | 20 | 24 | fits | 152,308 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 302,845 | 3.028 | 20 | 50 | fits | 152,308 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 458,329 | 4.583 | 20 | 50 | fits | 155,880 | 205 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 540,537 | 5.405 | 20 | 20 | fits | 82,274 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 998,530 | 9.985 | 20 | 20 | fits | 41,048 | 16 | 0.753 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 488,009 | 4.880 | 20 | 20 | fits | 151,492 | 204 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 294,496 | 2.945 | 20 | 200 | fits | 149,460 | 175 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 531,596 | 5.316 | 20 | 200 | fits | 151,492 | 204 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 295,420 | 2.954 | 20 | 20 | fits | 149,460 | 175 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 616,548 | 6.165 | 20 | 20 | fits | 84,248 | 42 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 149,600 | 1.496 | 20 | 24 | fits | 147,168 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 298,070 | 2.981 | 20 | 24 | fits | 149,460 | 175 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 298,004 | 2.980 | 20 | 50 | fits | 149,460 | 175 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 535,324 | 5.353 | 20 | 50 | fits | 151,492 | 204 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 619,506 | 6.195 | 20 | 20 | fits | 84,248 | 42 | 0.707 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 994,352 | 9.944 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 408,573 | 4.086 | 20 | 20 | fits | 159,488 | 210 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 293,312 | 2.933 | 20 | 200 | fits | 153,708 | 186 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 462,356 | 4.624 | 20 | 200 | fits | 159,488 | 210 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 294,236 | 2.942 | 20 | 20 | fits | 153,708 | 186 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 545,649 | 5.456 | 20 | 20 | fits | 82,589 | 31 | 0.755 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 144,168 | 1.442 | 20 | 24 | fits | 147,168 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 296,886 | 2.969 | 20 | 24 | fits | 153,708 | 186 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 296,820 | 2.968 | 20 | 50 | fits | 153,708 | 186 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 466,084 | 4.661 | 20 | 50 | fits | 159,488 | 210 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 548,607 | 5.486 | 20 | 20 | fits | 82,589 | 31 | 0.755 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 912,802 | 9.128 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 413,782 | 4.138 | 20 | 20 | fits | 156,473 | 206 | 0.399 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 301,050 | 3.010 | 20 | 200 | fits | 149,292 | 174 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 456,907 | 4.569 | 20 | 200 | fits | 156,473 | 206 | 0.399 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 301,974 | 3.020 | 20 | 20 | fits | 149,292 | 174 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 545,174 | 5.452 | 20 | 20 | fits | 87,563 | 44 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 156,322 | 1.563 | 20 | 24 | fits | 147,121 | 142 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 304,624 | 3.046 | 20 | 24 | fits | 149,292 | 174 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 304,558 | 3.046 | 20 | 50 | fits | 149,292 | 174 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 460,635 | 4.606 | 20 | 50 | fits | 156,473 | 206 | 0.399 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 548,132 | 5.481 | 20 | 20 | fits | 87,563 | 44 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 926,294 | 9.263 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 398,268 | 3.983 | 20 | 20 | fits | 158,459 | 195 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 302,678 | 3.027 | 20 | 200 | fits | 149,823 | 192 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 460,521 | 4.605 | 20 | 200 | fits | 158,459 | 195 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 303,602 | 3.036 | 20 | 20 | fits | 149,823 | 192 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 551,233 | 5.512 | 20 | 20 | fits | 90,008 | 35 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 157,419 | 1.574 | 20 | 24 | fits | 147,000 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 306,252 | 3.063 | 20 | 24 | fits | 149,823 | 192 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 306,186 | 3.062 | 20 | 50 | fits | 149,823 | 192 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 464,249 | 4.642 | 20 | 50 | fits | 158,459 | 195 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 554,191 | 5.542 | 20 | 20 | fits | 90,008 | 35 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 978,819 | 9.788 | 20 | 20 | fits | 83,730 | 36 | 0.536 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 496,079 | 4.961 | 20 | 20 | fits | 149,999 | 206 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 310,063 | 3.101 | 20 | 200 | fits | 149,281 | 174 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 539,635 | 5.396 | 20 | 200 | fits | 149,999 | 206 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 310,987 | 3.110 | 20 | 20 | fits | 149,281 | 174 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 623,898 | 6.239 | 20 | 20 | fits | 83,559 | 42 | 0.704 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 155,671 | 1.557 | 20 | 24 | fits | 147,159 | 143 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 313,637 | 3.136 | 20 | 24 | fits | 149,281 | 174 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 313,571 | 3.136 | 20 | 50 | fits | 149,281 | 174 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 543,363 | 5.434 | 20 | 50 | fits | 149,999 | 206 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 626,856 | 6.269 | 20 | 20 | fits | 83,559 | 42 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,017,940 | 10.179 | 20 | 20 | fits | 50,177 | 20 | 0.703 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 385,828 | 3.858 | 20 | 20 | fits | 158,847 | 225 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 290,188 | 2.902 | 20 | 200 | fits | 149,518 | 198 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 448,419 | 4.484 | 20 | 200 | fits | 158,847 | 225 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 291,112 | 2.911 | 20 | 20 | fits | 149,518 | 198 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 530,801 | 5.308 | 20 | 20 | fits | 81,678 | 31 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 145,234 | 1.452 | 20 | 24 | fits | 152,192 | 122 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 293,762 | 2.938 | 20 | 24 | fits | 149,518 | 198 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 293,696 | 2.937 | 20 | 50 | fits | 149,518 | 198 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 452,147 | 4.521 | 20 | 50 | fits | 158,847 | 225 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 533,759 | 5.338 | 20 | 20 | fits | 81,678 | 31 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 913,933 | 9.139 | 20 | 20 | fits | 41,573 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 424,443 | 4.244 | 20 | 20 | fits | 151,019 | 204 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 307,354 | 3.074 | 20 | 200 | fits | 149,454 | 175 | 0.442 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 467,961 | 4.680 | 20 | 200 | fits | 151,019 | 204 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 308,278 | 3.083 | 20 | 20 | fits | 149,454 | 175 | 0.442 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 552,116 | 5.521 | 20 | 20 | fits | 83,451 | 42 | 0.704 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 162,464 | 1.625 | 20 | 24 | fits | 147,047 | 142 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 310,928 | 3.109 | 20 | 24 | fits | 149,454 | 175 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 310,862 | 3.109 | 20 | 50 | fits | 149,454 | 175 | 0.442 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 471,689 | 4.717 | 20 | 50 | fits | 151,019 | 204 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 555,074 | 5.551 | 20 | 20 | fits | 83,451 | 42 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 929,906 | 9.299 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 396,021 | 3.960 | 20 | 20 | fits | 158,379 | 197 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 300,427 | 3.004 | 20 | 200 | fits | 149,951 | 192 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 458,190 | 4.582 | 20 | 200 | fits | 158,379 | 197 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 301,351 | 3.014 | 20 | 20 | fits | 149,951 | 192 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 555,702 | 5.557 | 20 | 20 | fits | 86,589 | 38 | 0.763 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 155,040 | 1.550 | 20 | 24 | fits | 147,023 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 304,001 | 3.040 | 20 | 24 | fits | 149,951 | 192 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 303,935 | 3.039 | 20 | 50 | fits | 149,951 | 192 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 461,918 | 4.619 | 20 | 50 | fits | 158,379 | 197 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 558,660 | 5.587 | 20 | 20 | fits | 86,589 | 38 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,000,614 | 10.006 | 20 | 20 | fits | 32,539 | 12 | 0.826 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 474,649 | 4.746 | 20 | 20 | fits | 156,548 | 208 | 0.394 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 293,227 | 2.932 | 20 | 200 | fits | 149,018 | 174 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 526,876 | 5.269 | 20 | 200 | fits | 156,548 | 208 | 0.394 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 294,151 | 2.942 | 20 | 20 | fits | 149,018 | 174 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 610,221 | 6.102 | 20 | 20 | fits | 82,641 | 37 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 148,773 | 1.488 | 20 | 24 | fits | 147,000 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 296,801 | 2.968 | 20 | 24 | fits | 149,018 | 174 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 296,735 | 2.967 | 20 | 50 | fits | 149,018 | 174 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 530,604 | 5.306 | 20 | 50 | fits | 156,548 | 208 | 0.394 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 613,179 | 6.132 | 20 | 20 | fits | 82,641 | 37 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 995,949 | 9.959 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 402,846 | 4.028 | 20 | 20 | fits | 158,459 | 195 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 307,256 | 3.073 | 20 | 200 | fits | 149,909 | 192 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 465,099 | 4.651 | 20 | 200 | fits | 158,459 | 195 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 308,180 | 3.082 | 20 | 20 | fits | 149,909 | 192 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 547,847 | 5.478 | 20 | 20 | fits | 82,044 | 31 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 161,911 | 1.619 | 20 | 24 | fits | 146,958 | 142 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 310,830 | 3.108 | 20 | 24 | fits | 149,909 | 192 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 310,764 | 3.108 | 20 | 50 | fits | 149,909 | 192 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 468,827 | 4.688 | 20 | 50 | fits | 158,459 | 195 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 550,805 | 5.508 | 20 | 20 | fits | 82,044 | 31 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 928,058 | 9.281 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 420,528 | 4.205 | 20 | 20 | fits | 149,982 | 205 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 314,406 | 3.144 | 20 | 200 | fits | 149,226 | 174 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 463,772 | 4.638 | 20 | 200 | fits | 149,982 | 205 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 315,330 | 3.153 | 20 | 20 | fits | 149,226 | 174 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 548,404 | 5.484 | 20 | 20 | fits | 83,928 | 42 | 0.704 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 160,068 | 1.601 | 20 | 24 | fits | 147,108 | 143 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 317,980 | 3.180 | 20 | 24 | fits | 149,226 | 174 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 317,914 | 3.179 | 20 | 50 | fits | 149,226 | 174 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 467,500 | 4.675 | 20 | 50 | fits | 149,982 | 205 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 551,362 | 5.514 | 20 | 20 | fits | 83,928 | 42 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 926,194 | 9.262 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 79,708 | 0.797 | 20 | 20 | fits | 26,867 | 8 | 0.784 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,057 | 0.441 | 20 | 20 | fits | 44,123 | 12 | 0.891 |
| malformed MRPDU discard | `srp.malformed.if0` | 22,989 | 0.230 | 20 | 20 | fits | 23,055 | 12 | 0.708 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 78,665 | 0.787 | 220 | 220 | fits | 42,987 | 6 | 0.907 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 14,777 | 0.148 | 20 | 20 | fits | 33,829 | 19 | 0.797 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 294,985 | 2.950 | 20 | 200 | fits | 151,603 | 198 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 37,796 | 0.378 | 20 | 200 | fits | 33,829 | 19 | 0.797 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 295,909 | 2.959 | 20 | 20 | fits | 151,603 | 198 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 460,477 | 4.605 | 20 | 20 | fits | 155,196 | 195 | 0.381 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 147,946 | 1.479 | 20 | 24 | fits | 148,132 | 145 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 298,559 | 2.986 | 20 | 24 | fits | 151,603 | 198 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 298,493 | 2.985 | 20 | 50 | fits | 151,603 | 198 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 463,501 | 4.635 | 20 | 50 | fits | 155,196 | 195 | 0.381 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 548,796 | 5.488 | 20 | 20 | fits | 85,361 | 34 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 873,960 | 8.740 | 20 | 20 | fits | 75,346 | 32 | 0.564 |
| LINK_UP | `adp.link_up.if0` | 2,986 | 0.030 | 20 | 200 | fits | 33,705 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,035 | 0.150 | 20 | 200 | fits | 26,764 | 23 (39) | 0.725 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,448 | 0.054 | 20 | 200 | fits | 20,592 | 16 (31) | 0.646 |
| LINK_UP | `adp.link_up.if0` | 2,986 | 0.030 | 20 | 200 | fits | 33,705 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,035 | 0.150 | 20 | 200 | fits | 26,764 | 23 (39) | 0.725 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,448 | 0.054 | 20 | 200 | fits | 20,592 | 16 (31) | 0.646 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
