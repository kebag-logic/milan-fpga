### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 16 paths and 0 of 125 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.100 (0.337) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.087 (0.308) | fits | 0 adp | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.260 (0.628) | fits | 0 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.712 (5.096) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-6.adp_available.if0` (backlog-adp@blank-6) | 4.218 (4.638) | fits | 7 adp | 10 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.643 (2.107) | fits | 15 events | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.244 | fits | 0 acmp | 11 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-4.service.acmp.last.if0` (backlog-adp@verify-aged2-4) | 6.060 | fits | 11 acmp | 11 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.287 | fits | 0 adp | 11 | 0 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 5.088 | fits | 7 adp | 11 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-4.service.aecp.first.if0` (backlog-adp@verify-aged2-4) | 1.620 | fits | 0 aecp | 11 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.270 | fits | 15 aecp | 11 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.270 | fits | 0 maap | 11 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-6.service.maap.last.if0` (backlog-adp@blank-6) | 4.674 | fits | 6 maap | 11 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-4.service.srp.first.if0` (backlog-adp@verify-aged2-4) | 6.089 | fits | 0 srp | 11 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-4.service.srp.last.if0` (backlog-adp@blank-aged2-4) | 9.326 | fits | 31 srp | 11 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-2 | 0 | 9.905 | 7 | 153,569 (1.536) | yes | - |
| backlog-adp@blank-6 | 0 | 10.384 | 9 | 153,073 (1.531) | yes | - |
| backlog-adp@program-4 | 0 | 9.665 | 8 | 153,090 (1.531) | yes | - |
| backlog-adp@verify-4 | 0 | 9.857 | 7 | 153,917 (1.539) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 9.968 | 7 | 155,150 (1.552) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 10.349 | 9 | 153,477 (1.535) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 9.852 | 7 | 152,670 (1.527) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.127 | 8 | 152,154 (1.522) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 9.948 | 7 | 155,434 (1.554) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 9.864 | 7 | 155,110 (1.551) | yes | - |
| backlog | 0 | 6.276 | 7 | 155,069 (1.551) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 155,069 CPU cycles (1.551 ms), backlog.
Over the windows that released their whole load only: 155,069 (1.551 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-2 | 554 | 0 | 153,569 (1.536) | fits |
| backlog-adp@blank-6 | 556 | 0 | 153,073 (1.531) | fits |
| backlog-adp@program-4 | 941 | 0 | 153,090 (1.531) | fits |
| backlog-adp@verify-4 | 1314 | 0 | 153,917 (1.539) | fits |
| backlog-adp@blank-aged2-4 | 822 | 0 | 155,150 (1.552) | fits |
| backlog-adp@blank-aged1-5 | 779 | 0 | 153,477 (1.535) | fits |
| backlog-adp@program-aged2-4 | 1200 | 0 | 152,670 (1.527) | fits |
| backlog-adp@program-aged1-4 | 1151 | 0 | 152,154 (1.522) | fits |
| backlog-adp@verify-aged2-4 | 1581 | 0 | 155,434 (1.554) | fits |
| backlog-adp@verify-aged1-4 | 1530 | 0 | 155,110 (1.551) | fits |
| backlog | 286 | 0 | 155,069 (1.551) | fits |
| acmp-disc | 873 | 0 | 46,561 (0.466) | fits |
| datapath-events | 118 | 0 | 33,635 (0.336) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-4 | 2 | +6.047 ms, 76,738 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.326 (20) | 10.674 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 8.399 (20) | 11.601 |
| backlog-adp@program-aged2-4 | 2 | none | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.212 (20) | 10.788 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.347 (20) | 11.653 |
| backlog-adp@verify-aged2-4 | 2 | +6.106 ms, 77,676 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.306 (20) | 10.694 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.461 (20) | 11.539 |

Least margin over the aged windows: 10.674 ms, `backlog-adp@blank-aged2-4.service.srp.last.if0` at 9.326 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-2 | 339 | 95,910 (0.959) | 75,943 (0.759) |
| backlog-adp@blank-6 | 339 | 96,255 (0.963) | 76,025 (0.760) |
| backlog-adp@program-4 | 449 | 100,322 (1.003) | 77,944 (0.779) |
| backlog-adp@verify-4 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@blank-aged2-4 | 337 | 79,120 (0.791) | 75,467 (0.755) |
| backlog-adp@blank-aged1-5 | 337 | 96,256 (0.963) | 76,026 (0.760) |
| backlog-adp@program-aged2-4 | 446 | 100,322 (1.003) | 78,221 (0.782) |
| backlog-adp@program-aged1-4 | 446 | 100,322 (1.003) | 78,340 (0.783) |
| backlog-adp@verify-aged2-4 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@verify-aged1-4 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog | 265 | 25,989 (0.260) | 2,306 (0.023) |
| acmp-disc | 306 | 108,018 (1.080) | 75,448 (0.754) |
| datapath-events | 70 | 25,989 (0.260) | 2,306 (0.023) |

Longest pass that carries a step: 108,018 CPU cycles (1.080 ms), acmp-disc; longest step: 78,340 (0.783 ms), backlog-adp@program-aged1-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 408,208 | 4.082 | 20 | 20 | fits | 153,569 | 209 | 0.330 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 306,081 | 3.061 | 20 | 200 | fits | 149,405 | 176 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 459,034 | 4.590 | 20 | 200 | fits | 153,569 | 209 | 0.330 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 307,005 | 3.070 | 20 | 20 | fits | 149,405 | 176 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 591,985 | 5.920 | 20 | 20 | fits | 132,247 | 55 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 161,240 | 1.612 | 20 | 24 | fits | 149,260 | 145 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 309,655 | 3.097 | 20 | 24 | fits | 149,405 | 176 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 309,589 | 3.096 | 20 | 50 | fits | 149,405 | 176 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 462,762 | 4.628 | 20 | 50 | fits | 153,569 | 209 | 0.330 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 594,943 | 5.949 | 20 | 20 | fits | 132,247 | 55 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 850,663 | 8.507 | 20 | 20 | fits | 119,318 | 61 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 421,817 | 4.218 | 20 | 20 | fits | 153,073 | 205 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 311,181 | 3.112 | 20 | 200 | fits | 151,839 | 181 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 463,638 | 4.636 | 20 | 200 | fits | 153,073 | 205 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 312,105 | 3.121 | 20 | 20 | fits | 151,839 | 181 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 596,850 | 5.968 | 20 | 20 | fits | 132,508 | 61 | 0.601 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 154,510 | 1.545 | 20 | 24 | fits | 149,505 | 146 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 314,755 | 3.148 | 20 | 24 | fits | 151,839 | 181 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 314,689 | 3.147 | 20 | 50 | fits | 151,839 | 181 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 467,366 | 4.674 | 20 | 50 | fits | 153,073 | 205 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 599,808 | 5.998 | 20 | 20 | fits | 132,508 | 61 | 0.601 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 843,390 | 8.434 | 20 | 20 | fits | 118,245 | 52 | 0.482 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 379,681 | 3.797 | 20 | 20 | fits | 153,090 | 206 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 296,508 | 2.965 | 20 | 200 | fits | 150,865 | 180 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 448,982 | 4.490 | 20 | 200 | fits | 153,090 | 206 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 297,432 | 2.974 | 20 | 20 | fits | 150,865 | 180 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 596,865 | 5.969 | 20 | 20 | fits | 136,524 | 62 | 0.647 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 150,207 | 1.502 | 20 | 24 | fits | 149,866 | 145 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 300,082 | 3.001 | 20 | 24 | fits | 150,865 | 180 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 300,016 | 3.000 | 20 | 50 | fits | 150,865 | 180 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 452,710 | 4.527 | 20 | 50 | fits | 153,090 | 206 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 599,823 | 5.998 | 20 | 20 | fits | 136,524 | 62 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 835,162 | 8.352 | 20 | 20 | fits | 109,772 | 48 | 0.500 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 402,737 | 4.027 | 20 | 20 | fits | 153,917 | 210 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 300,541 | 3.005 | 20 | 200 | fits | 149,386 | 176 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 453,842 | 4.538 | 20 | 200 | fits | 153,917 | 210 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 301,465 | 3.015 | 20 | 20 | fits | 149,386 | 176 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 598,242 | 5.982 | 20 | 20 | fits | 133,373 | 66 | 0.654 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 155,719 | 1.557 | 20 | 24 | fits | 149,055 | 145 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 304,115 | 3.041 | 20 | 24 | fits | 149,386 | 176 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 304,049 | 3.040 | 20 | 50 | fits | 149,386 | 176 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 457,570 | 4.576 | 20 | 50 | fits | 153,917 | 210 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 601,200 | 6.012 | 20 | 20 | fits | 133,373 | 66 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 845,092 | 8.451 | 20 | 20 | fits | 118,384 | 52 | 0.485 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 400,042 | 4.000 | 20 | 20 | fits | 155,150 | 195 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 305,949 | 3.059 | 20 | 200 | fits | 149,271 | 192 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 460,483 | 4.605 | 20 | 200 | fits | 155,150 | 195 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 306,873 | 3.069 | 20 | 20 | fits | 149,271 | 192 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 600,023 | 6.000 | 20 | 20 | fits | 138,836 | 63 | 0.629 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 161,242 | 1.612 | 20 | 24 | fits | 147,816 | 142 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 309,523 | 3.095 | 20 | 24 | fits | 149,271 | 192 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 309,457 | 3.095 | 20 | 50 | fits | 149,271 | 192 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 464,211 | 4.642 | 20 | 50 | fits | 155,150 | 195 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 602,981 | 6.030 | 20 | 20 | fits | 138,836 | 63 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 932,555 | 9.326 | 20 | 20 | fits | 115,702 | 55 | 0.576 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 417,481 | 4.175 | 20 | 20 | fits | 151,678 | 200 | 0.389 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 309,044 | 3.090 | 20 | 200 | fits | 153,477 | 185 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 460,106 | 4.601 | 20 | 200 | fits | 151,678 | 200 | 0.389 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 309,968 | 3.100 | 20 | 20 | fits | 153,477 | 185 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 593,226 | 5.932 | 20 | 20 | fits | 132,416 | 61 | 0.601 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 150,502 | 1.505 | 20 | 24 | fits | 147,936 | 143 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 312,618 | 3.126 | 20 | 24 | fits | 153,477 | 185 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 312,552 | 3.126 | 20 | 50 | fits | 153,477 | 185 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 463,834 | 4.638 | 20 | 50 | fits | 151,678 | 200 | 0.389 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 596,184 | 5.962 | 20 | 20 | fits | 132,416 | 61 | 0.601 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 839,867 | 8.399 | 20 | 20 | fits | 118,245 | 52 | 0.482 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 377,970 | 3.780 | 20 | 20 | fits | 152,670 | 205 | 0.346 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 294,834 | 2.948 | 20 | 200 | fits | 150,843 | 180 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 446,888 | 4.469 | 20 | 200 | fits | 152,670 | 205 | 0.346 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 295,758 | 2.958 | 20 | 20 | fits | 150,843 | 180 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 586,153 | 5.862 | 20 | 20 | fits | 138,561 | 64 | 0.630 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 148,555 | 1.486 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 298,408 | 2.984 | 20 | 24 | fits | 150,843 | 180 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 298,342 | 2.983 | 20 | 50 | fits | 150,843 | 180 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 450,616 | 4.506 | 20 | 50 | fits | 152,670 | 205 | 0.346 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 589,111 | 5.891 | 20 | 20 | fits | 138,561 | 64 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 921,243 | 9.212 | 20 | 20 | fits | 110,235 | 48 | 0.509 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 405,964 | 4.060 | 20 | 20 | fits | 152,154 | 204 | 0.340 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 305,974 | 3.060 | 20 | 200 | fits | 150,843 | 180 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 457,512 | 4.575 | 20 | 200 | fits | 152,154 | 204 | 0.340 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 306,898 | 3.069 | 20 | 20 | fits | 150,843 | 180 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 596,400 | 5.964 | 20 | 20 | fits | 138,184 | 63 | 0.627 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 159,695 | 1.597 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 309,548 | 3.095 | 20 | 24 | fits | 150,843 | 180 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 309,482 | 3.095 | 20 | 50 | fits | 150,843 | 180 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 461,240 | 4.612 | 20 | 50 | fits | 152,154 | 204 | 0.340 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 599,358 | 5.994 | 20 | 20 | fits | 138,184 | 63 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 834,674 | 8.347 | 20 | 20 | fits | 109,737 | 49 | 0.497 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 400,753 | 4.008 | 20 | 20 | fits | 155,434 | 196 | 0.341 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 306,700 | 3.067 | 20 | 200 | fits | 149,254 | 192 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 461,518 | 4.615 | 20 | 200 | fits | 155,434 | 196 | 0.341 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 307,624 | 3.076 | 20 | 20 | fits | 149,254 | 192 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 605,980 | 6.060 | 20 | 20 | fits | 133,435 | 66 | 0.654 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 162,010 | 1.620 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 310,274 | 3.103 | 20 | 24 | fits | 149,254 | 192 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 310,208 | 3.102 | 20 | 50 | fits | 149,254 | 192 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 465,246 | 4.652 | 20 | 50 | fits | 155,434 | 196 | 0.341 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 608,938 | 6.089 | 20 | 20 | fits | 133,435 | 66 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 930,569 | 9.306 | 20 | 20 | fits | 118,453 | 52 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 390,574 | 3.906 | 20 | 20 | fits | 155,110 | 195 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 296,521 | 2.965 | 20 | 200 | fits | 149,254 | 192 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 451,015 | 4.510 | 20 | 200 | fits | 155,110 | 195 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 297,445 | 2.974 | 20 | 20 | fits | 149,254 | 192 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 590,625 | 5.906 | 20 | 20 | fits | 138,906 | 64 | 0.627 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 151,831 | 1.518 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 300,095 | 3.001 | 20 | 24 | fits | 149,254 | 192 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 300,029 | 3.000 | 20 | 50 | fits | 149,254 | 192 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 454,743 | 4.547 | 20 | 50 | fits | 155,110 | 195 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 593,583 | 5.936 | 20 | 20 | fits | 138,906 | 64 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 846,058 | 8.461 | 20 | 20 | fits | 110,153 | 48 | 0.509 |
| an event behind 15 others | `backlog.event.if0` | 164,272 | 1.643 | 20 | 200 | fits | 59,812 | 79 | 0.551 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 471,174 | 4.712 | 20 | 20 | fits | 80,704 | 103 | 0.262 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 428,706 | 4.287 | 20 | 200 | fits | 155,069 | 129 | 0.388 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 508,794 | 5.088 | 20 | 200 | fits | 80,704 | 103 | 0.262 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 424,384 | 4.244 | 20 | 20 | fits | 155,069 | 129 | 0.388 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 504,252 | 5.043 | 20 | 20 | fits | 80,704 | 103 | 0.262 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 149,997 | 1.500 | 20 | 24 | fits | 150,888 | 148 | 0.361 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 427,034 | 4.270 | 20 | 24 | fits | 155,069 | 129 | 0.388 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 426,968 | 4.270 | 20 | 50 | fits | 155,069 | 129 | 0.388 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 426,572 | 4.266 | 20 | 50 | fits | 155,069 | 129 | 0.388 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 507,210 | 5.072 | 20 | 20 | fits | 80,704 | 103 | 0.262 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 565,869 | 5.659 | 20 | 20 | fits | 25,901 | 41 | 0.187 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 8,695 | 0.087 | 20 | 20 | fits | 30,788 | 13 (29) | 0.812 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 10,046 | 0.100 | 20 | 20 | fits | 33,684 | 19 (35) | 0.805 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 25,978 | 0.260 | 20 | 20 | fits | 38,074 | 27 (12) | 0.808 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
