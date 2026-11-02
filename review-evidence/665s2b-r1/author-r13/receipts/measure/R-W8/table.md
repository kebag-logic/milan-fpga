### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 264 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 5.292 (6.734) | fits | 7 adp | 24 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.854 | fits | 0 acmp | 24 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 8.886 | fits | 11 acmp | 24 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.845 | fits | 0 adp | 24 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.442 | fits | 7 adp | 24 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.890 | fits | 0 aecp | 24 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@blank-0.service.aecp.last.if1` (backlog-adp@blank-0) | 15.861 | fits | 15 aecp | 24 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.879 | fits | 0 maap | 24 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.478 | fits | 6 maap | 24 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-3.service.srp.first.if0` (backlog-adp@program-3) | 4.390 | fits | 0 srp | 24 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-2.service.srp.last.if1` (backlog-adp@verify-2) | 16.985 | fits | 31 srp | 24 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.234 | 21 | 187,825 (1.878) | yes | - |
| backlog-adp@blank-1 | 0 | 17.640 | 21 | 187,796 (1.878) | yes | - |
| backlog-adp@blank-2 | 0 | 18.837 | 23 | 194,879 (1.949) | yes | - |
| backlog-adp@blank-3 | 0 | 18.613 | 25 | 183,130 (1.831) | yes | - |
| backlog-adp@blank-4 | 0 | 18.019 | 22 | 190,467 (1.905) | yes | - |
| backlog-adp@blank-5 | 0 | 17.805 | 22 | 187,848 (1.878) | yes | - |
| backlog-adp@blank-6 | 0 | 17.864 | 22 | 186,612 (1.866) | yes | - |
| backlog-adp@blank-7 | 0 | 17.611 | 20 | 194,404 (1.944) | yes | - |
| backlog-adp@program-0 | 0 | 18.081 | 22 | 189,881 (1.899) | yes | - |
| backlog-adp@program-1 | 0 | 17.741 | 21 | 187,164 (1.872) | yes | - |
| backlog-adp@program-2 | 0 | 18.049 | 22 | 187,164 (1.872) | yes | - |
| backlog-adp@program-3 | 0 | 18.265 | 23 | 181,494 (1.815) | yes | - |
| backlog-adp@program-4 | 0 | 17.174 | 22 | 186,918 (1.869) | yes | - |
| backlog-adp@program-5 | 0 | 17.170 | 22 | 186,918 (1.869) | yes | - |
| backlog-adp@program-6 | 0 | 17.318 | 22 | 181,327 (1.813) | yes | - |
| backlog-adp@program-7 | 0 | 17.079 | 21 | 193,751 (1.938) | yes | - |
| backlog-adp@verify-0 | 0 | 18.257 | 22 | 194,663 (1.947) | yes | - |
| backlog-adp@verify-1 | 0 | 19.553 | 24 | 182,735 (1.827) | yes | - |
| backlog-adp@verify-2 | 0 | 18.365 | 22 | 190,406 (1.904) | yes | - |
| backlog-adp@verify-3 | 0 | 18.222 | 22 | 187,709 (1.877) | yes | - |
| backlog-adp@verify-4 | 0 | 18.047 | 21 | 187,709 (1.877) | yes | - |
| backlog-adp@verify-5 | 0 | 18.230 | 21 | 170,885 (1.709) | yes | - |
| backlog-adp@verify-6 | 0 | 18.214 | 22 | 194,376 (1.944) | yes | - |
| backlog-adp@verify-7 | 1 | 18.841 | 24 | 183,083 (1.831) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 18162 | 0 | 187,825 (1.878) | fits |
| backlog-adp@blank-1 | 18165 | 0 | 187,796 (1.878) | fits |
| backlog-adp@blank-2 | 18174 | 0 | 194,879 (1.949) | fits |
| backlog-adp@blank-3 | 18183 | 0 | 183,130 (1.831) | fits |
| backlog-adp@blank-4 | 18186 | 0 | 190,467 (1.905) | fits |
| backlog-adp@blank-5 | 18192 | 0 | 187,848 (1.878) | fits |
| backlog-adp@blank-6 | 18199 | 0 | 186,612 (1.866) | fits |
| backlog-adp@blank-7 | 18204 | 0 | 194,404 (1.944) | fits |
| backlog-adp@program-0 | 23274 | 0 | 189,881 (1.899) | fits |
| backlog-adp@program-1 | 23285 | 0 | 187,164 (1.872) | fits |
| backlog-adp@program-2 | 23300 | 0 | 187,164 (1.872) | fits |
| backlog-adp@program-3 | 23314 | 0 | 181,494 (1.815) | fits |
| backlog-adp@program-4 | 23321 | 0 | 186,918 (1.869) | fits |
| backlog-adp@program-5 | 23334 | 0 | 186,918 (1.869) | fits |
| backlog-adp@program-6 | 23348 | 0 | 181,327 (1.813) | fits |
| backlog-adp@program-7 | 23360 | 0 | 193,751 (1.938) | fits |
| backlog-adp@verify-0 | 28396 | 0 | 194,663 (1.947) | fits |
| backlog-adp@verify-1 | 28405 | 0 | 182,735 (1.827) | fits |
| backlog-adp@verify-2 | 28409 | 0 | 190,406 (1.904) | fits |
| backlog-adp@verify-3 | 28415 | 0 | 187,709 (1.877) | fits |
| backlog-adp@verify-4 | 28421 | 0 | 187,709 (1.877) | fits |
| backlog-adp@verify-5 | 28428 | 0 | 170,885 (1.709) | fits |
| backlog-adp@verify-6 | 28435 | 0 | 194,376 (1.944) | fits |
| backlog-adp@verify-7 | 28445 | 0 | 183,083 (1.831) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 529,195 | 5.292 | 20 | 20 | fits | 126,383 | 85 | 0.630 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 184,488 | 1.845 | 20 | 200 | fits | 119,368 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 644,153 | 6.442 | 20 | 200 | fits | 126,383 | 85 | 0.630 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 185,400 | 1.854 | 20 | 20 | fits | 119,368 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 888,560 | 8.886 | 20 | 20 | fits | 121,026 | 46 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 188,985 | 1.890 | 20 | 24 | fits | 119,368 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,586,147 | 15.861 | 20 | 24 | fits | 67,554 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 187,945 | 1.879 | 20 | 50 | fits | 119,368 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 647,829 | 6.478 | 20 | 50 | fits | 126,383 | 85 | 0.630 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 375,315 | 3.753 | 18 | 18 | fits | 187,825 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,685,509 | 16.855 | 18 | 18 | fits | 50,289 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 456,465 | 4.565 | 20 | 20 | fits | 156,675 | 89 | 0.665 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 115,875 | 1.159 | 20 | 200 | fits | 119,024 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 599,259 | 5.993 | 20 | 200 | fits | 156,675 | 89 | 0.665 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 116,787 | 1.168 | 20 | 20 | fits | 119,024 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 842,533 | 8.425 | 20 | 20 | fits | 120,730 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 120,372 | 1.204 | 20 | 24 | fits | 119,024 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,526,656 | 15.267 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 119,332 | 1.193 | 20 | 50 | fits | 119,024 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 602,935 | 6.029 | 20 | 50 | fits | 156,675 | 89 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 306,673 | 3.067 | 18 | 18 | fits | 187,796 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,626,092 | 16.261 | 18 | 18 | fits | 50,355 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 477,012 | 4.770 | 20 | 20 | fits | 154,496 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 122,594 | 1.226 | 20 | 200 | fits | 119,024 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 620,083 | 6.201 | 20 | 200 | fits | 154,496 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 123,506 | 1.235 | 20 | 20 | fits | 119,024 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 835,741 | 8.357 | 20 | 20 | fits | 126,410 | 52 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 127,091 | 1.271 | 20 | 24 | fits | 119,024 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,527,700 | 15.277 | 20 | 24 | fits | 67,565 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 126,051 | 1.261 | 20 | 50 | fits | 119,024 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 623,759 | 6.238 | 20 | 50 | fits | 154,496 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 320,475 | 3.205 | 18 | 18 | fits | 194,879 | 151 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,627,028 | 16.270 | 18 | 18 | fits | 50,340 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 445,031 | 4.450 | 20 | 20 | fits | 156,174 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 129,313 | 1.293 | 20 | 200 | fits | 119,024 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 589,184 | 5.892 | 20 | 200 | fits | 156,174 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 130,225 | 1.302 | 20 | 20 | fits | 119,024 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 838,746 | 8.387 | 20 | 20 | fits | 120,821 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 133,810 | 1.338 | 20 | 24 | fits | 119,024 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,531,569 | 15.316 | 20 | 24 | fits | 67,508 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 132,770 | 1.328 | 20 | 50 | fits | 119,024 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 592,860 | 5.929 | 20 | 50 | fits | 156,174 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 436,621 | 4.366 | 18 | 18 | fits | 183,130 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,637,175 | 16.372 | 18 | 18 | fits | 56,525 | 24 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 477,347 | 4.773 | 20 | 20 | fits | 161,253 | 89 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 123,064 | 1.231 | 20 | 200 | fits | 124,873 | 151 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 620,449 | 6.204 | 20 | 200 | fits | 161,253 | 89 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 123,976 | 1.240 | 20 | 20 | fits | 124,873 | 151 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 870,296 | 8.703 | 20 | 20 | fits | 127,692 | 57 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 127,561 | 1.276 | 20 | 24 | fits | 124,873 | 151 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,548,115 | 15.481 | 20 | 24 | fits | 74,295 | 37 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 126,521 | 1.265 | 20 | 50 | fits | 124,873 | 151 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 624,125 | 6.241 | 20 | 50 | fits | 161,253 | 89 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 316,533 | 3.165 | 18 | 18 | fits | 190,467 | 145 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,633,955 | 16.340 | 18 | 18 | fits | 36,794 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 431,923 | 4.319 | 20 | 20 | fits | 160,006 | 89 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 114,381 | 1.144 | 20 | 200 | fits | 118,805 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 573,352 | 5.734 | 20 | 200 | fits | 160,006 | 89 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 115,293 | 1.153 | 20 | 20 | fits | 118,805 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 789,602 | 7.896 | 20 | 20 | fits | 93,952 | 48 | 0.658 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 118,878 | 1.189 | 20 | 24 | fits | 118,805 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,480,855 | 14.809 | 20 | 24 | fits | 67,935 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 117,838 | 1.178 | 20 | 50 | fits | 118,805 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 577,028 | 5.770 | 20 | 50 | fits | 160,006 | 89 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 305,231 | 3.052 | 18 | 18 | fits | 187,848 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,642,756 | 16.428 | 18 | 18 | fits | 50,771 | 18 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 434,580 | 4.346 | 20 | 20 | fits | 155,967 | 83 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 121,100 | 1.211 | 20 | 200 | fits | 118,805 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 578,617 | 5.786 | 20 | 200 | fits | 155,967 | 83 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 122,012 | 1.220 | 20 | 20 | fits | 118,805 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 833,749 | 8.337 | 20 | 20 | fits | 121,064 | 46 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 125,597 | 1.256 | 20 | 24 | fits | 118,805 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,498,644 | 14.986 | 20 | 24 | fits | 71,314 | 37 | 0.724 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 124,557 | 1.246 | 20 | 50 | fits | 118,805 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 582,293 | 5.823 | 20 | 50 | fits | 155,967 | 83 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 426,261 | 4.263 | 18 | 18 | fits | 186,612 | 104 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,648,498 | 16.485 | 18 | 18 | fits | 50,209 | 18 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 490,676 | 4.907 | 20 | 20 | fits | 166,102 | 101 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 127,819 | 1.278 | 20 | 200 | fits | 118,805 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 633,870 | 6.339 | 20 | 200 | fits | 166,102 | 101 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 128,731 | 1.287 | 20 | 20 | fits | 118,805 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 876,812 | 8.768 | 20 | 20 | fits | 120,656 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 132,316 | 1.323 | 20 | 24 | fits | 118,805 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,574,251 | 15.743 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 131,276 | 1.313 | 20 | 50 | fits | 118,805 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 637,546 | 6.375 | 20 | 50 | fits | 166,102 | 101 | 0.681 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 325,225 | 3.252 | 18 | 18 | fits | 194,404 | 145 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,623,188 | 16.232 | 18 | 18 | fits | 51,472 | 20 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 484,393 | 4.844 | 20 | 20 | fits | 154,359 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 137,424 | 1.374 | 20 | 200 | fits | 125,718 | 151 | 0.537 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 627,330 | 6.273 | 20 | 200 | fits | 154,359 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 138,336 | 1.383 | 20 | 20 | fits | 125,718 | 151 | 0.537 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 877,166 | 8.772 | 20 | 20 | fits | 127,692 | 57 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 141,921 | 1.419 | 20 | 24 | fits | 125,718 | 151 | 0.537 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,565,763 | 15.658 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 140,881 | 1.409 | 20 | 50 | fits | 125,718 | 151 | 0.537 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 631,006 | 6.310 | 20 | 50 | fits | 154,359 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 330,307 | 3.303 | 18 | 18 | fits | 189,881 | 145 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,614,700 | 16.147 | 18 | 18 | fits | 51,472 | 20 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 460,757 | 4.608 | 20 | 20 | fits | 154,223 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 116,717 | 1.167 | 20 | 200 | fits | 119,610 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 603,581 | 6.036 | 20 | 200 | fits | 154,223 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 117,629 | 1.176 | 20 | 20 | fits | 119,610 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 863,986 | 8.640 | 20 | 20 | fits | 121,090 | 46 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 121,214 | 1.212 | 20 | 24 | fits | 119,610 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,556,244 | 15.562 | 20 | 24 | fits | 68,113 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 120,174 | 1.202 | 20 | 50 | fits | 119,610 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 607,257 | 6.073 | 20 | 50 | fits | 154,223 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 306,883 | 3.069 | 18 | 18 | fits | 187,164 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,605,325 | 16.053 | 18 | 18 | fits | 51,616 | 20 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 454,707 | 4.547 | 20 | 20 | fits | 162,842 | 95 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 130,155 | 1.302 | 20 | 200 | fits | 119,610 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 597,109 | 5.971 | 20 | 200 | fits | 162,842 | 95 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 131,067 | 1.311 | 20 | 20 | fits | 119,610 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 840,262 | 8.403 | 20 | 20 | fits | 120,833 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 134,652 | 1.347 | 20 | 24 | fits | 119,610 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,525,981 | 15.260 | 20 | 24 | fits | 68,024 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 133,612 | 1.336 | 20 | 50 | fits | 119,610 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 600,785 | 6.008 | 20 | 50 | fits | 162,842 | 95 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 320,321 | 3.203 | 18 | 18 | fits | 187,164 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,661,515 | 16.615 | 18 | 18 | fits | 36,663 | 15 | 0.774 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 447,470 | 4.475 | 20 | 20 | fits | 156,056 | 83 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 130,547 | 1.305 | 20 | 200 | fits | 125,381 | 151 | 0.534 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 591,440 | 5.914 | 20 | 200 | fits | 156,056 | 83 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 131,459 | 1.315 | 20 | 20 | fits | 125,381 | 151 | 0.534 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 834,059 | 8.341 | 20 | 20 | fits | 120,636 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 135,044 | 1.350 | 20 | 24 | fits | 125,381 | 151 | 0.534 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,533,567 | 15.336 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 134,004 | 1.340 | 20 | 50 | fits | 125,381 | 151 | 0.534 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 595,116 | 5.951 | 20 | 50 | fits | 156,056 | 83 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 438,995 | 4.390 | 18 | 18 | fits | 181,494 | 104 | 0.660 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,633,081 | 16.331 | 18 | 18 | fits | 50,433 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 465,933 | 4.659 | 20 | 20 | fits | 154,203 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 122,050 | 1.220 | 20 | 200 | fits | 119,626 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 608,646 | 6.086 | 20 | 200 | fits | 154,203 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 122,962 | 1.230 | 20 | 20 | fits | 119,626 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 825,751 | 8.258 | 20 | 20 | fits | 121,844 | 52 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 126,547 | 1.265 | 20 | 24 | fits | 119,626 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,496,058 | 14.961 | 20 | 24 | fits | 60,888 | 38 | 0.750 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 125,507 | 1.255 | 20 | 50 | fits | 119,626 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 612,322 | 6.123 | 20 | 50 | fits | 154,203 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 311,970 | 3.120 | 18 | 18 | fits | 186,918 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,650,546 | 16.505 | 18 | 18 | fits | 50,294 | 18 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 456,662 | 4.567 | 20 | 20 | fits | 156,808 | 89 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 116,724 | 1.167 | 20 | 200 | fits | 119,626 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 599,456 | 5.995 | 20 | 200 | fits | 156,808 | 89 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 117,636 | 1.176 | 20 | 20 | fits | 119,626 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 849,182 | 8.492 | 20 | 20 | fits | 120,858 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 121,221 | 1.212 | 20 | 24 | fits | 119,626 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,508,155 | 15.082 | 20 | 24 | fits | 67,800 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 120,181 | 1.202 | 20 | 50 | fits | 119,626 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 603,132 | 6.031 | 20 | 50 | fits | 156,808 | 89 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 306,644 | 3.066 | 18 | 18 | fits | 186,918 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,650,675 | 16.507 | 18 | 18 | fits | 43,039 | 21 | 0.787 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 422,123 | 4.221 | 20 | 20 | fits | 181,327 | 89 | 0.710 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 130,162 | 1.302 | 20 | 200 | fits | 119,626 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 584,490 | 5.845 | 20 | 200 | fits | 181,327 | 89 | 0.710 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 131,074 | 1.311 | 20 | 20 | fits | 119,626 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 828,414 | 8.284 | 20 | 20 | fits | 120,726 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 134,659 | 1.347 | 20 | 24 | fits | 119,626 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,529,554 | 15.296 | 20 | 24 | fits | 68,009 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 133,619 | 1.336 | 20 | 50 | fits | 119,626 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 588,166 | 5.882 | 20 | 50 | fits | 181,327 | 89 | 0.710 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 406,774 | 4.068 | 18 | 18 | fits | 152,347 | 100 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,665,394 | 16.654 | 18 | 18 | fits | 36,748 | 15 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 510,817 | 5.108 | 20 | 20 | fits | 143,555 | 60 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 169,054 | 1.691 | 20 | 200 | fits | 120,207 | 142 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 642,950 | 6.429 | 20 | 200 | fits | 143,555 | 60 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 169,966 | 1.700 | 20 | 20 | fits | 120,207 | 142 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 859,274 | 8.593 | 20 | 20 | fits | 121,521 | 52 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 53,344 | 0.533 | 20 | 24 | fits | 54,354 | 65 | 0.544 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,479,048 | 14.790 | 20 | 24 | fits | 67,610 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 52,304 | 0.523 | 20 | 50 | fits | 54,354 | 65 | 0.544 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 503,071 | 5.031 | 20 | 50 | fits | 137,199 | 76 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 365,807 | 3.658 | 18 | 18 | fits | 193,751 | 145 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,641,006 | 16.410 | 18 | 18 | fits | 50,771 | 18 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 478,267 | 4.783 | 20 | 20 | fits | 154,496 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 124,058 | 1.241 | 20 | 200 | fits | 119,716 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 621,338 | 6.213 | 20 | 200 | fits | 154,496 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 124,970 | 1.250 | 20 | 20 | fits | 119,716 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 864,156 | 8.642 | 20 | 20 | fits | 120,703 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 128,555 | 1.286 | 20 | 24 | fits | 119,716 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,504,061 | 15.041 | 20 | 24 | fits | 54,028 | 27 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 127,515 | 1.275 | 20 | 50 | fits | 119,716 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 625,014 | 6.250 | 20 | 50 | fits | 154,496 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 321,723 | 3.217 | 18 | 18 | fits | 194,663 | 151 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,686,958 | 16.870 | 18 | 18 | fits | 50,150 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 446,183 | 4.462 | 20 | 20 | fits | 156,124 | 83 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 130,841 | 1.308 | 20 | 200 | fits | 119,500 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 590,286 | 5.903 | 20 | 200 | fits | 156,124 | 83 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 131,753 | 1.318 | 20 | 20 | fits | 119,500 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 800,037 | 8.000 | 20 | 20 | fits | 87,607 | 37 | 0.639 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 135,338 | 1.353 | 20 | 24 | fits | 119,500 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,534,890 | 15.349 | 20 | 24 | fits | 68,213 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 134,298 | 1.343 | 20 | 50 | fits | 119,500 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 593,962 | 5.940 | 20 | 50 | fits | 156,124 | 83 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 437,773 | 4.378 | 18 | 18 | fits | 182,735 | 104 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,684,771 | 16.848 | 18 | 18 | fits | 50,294 | 18 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 472,169 | 4.722 | 20 | 20 | fits | 154,211 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 124,873 | 1.249 | 20 | 200 | fits | 125,630 | 151 | 0.541 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 615,023 | 6.150 | 20 | 200 | fits | 154,211 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 125,785 | 1.258 | 20 | 20 | fits | 125,630 | 151 | 0.541 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 830,440 | 8.304 | 20 | 20 | fits | 126,368 | 52 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 129,370 | 1.294 | 20 | 24 | fits | 125,630 | 151 | 0.541 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,557,103 | 15.571 | 20 | 24 | fits | 101,046 | 45 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 128,330 | 1.283 | 20 | 50 | fits | 125,630 | 151 | 0.541 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 618,699 | 6.187 | 20 | 50 | fits | 154,211 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 318,281 | 3.183 | 18 | 18 | fits | 190,406 | 145 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,698,524 | 16.985 | 18 | 18 | fits | 46,940 | 27 | 0.800 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 460,855 | 4.609 | 20 | 20 | fits | 120,271 | 74 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 116,314 | 1.163 | 20 | 200 | fits | 119,599 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 569,701 | 5.697 | 20 | 200 | fits | 120,271 | 74 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 117,226 | 1.172 | 20 | 20 | fits | 119,599 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 829,881 | 8.299 | 20 | 20 | fits | 132,598 | 64 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 120,811 | 1.208 | 20 | 24 | fits | 119,599 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,537,180 | 15.372 | 20 | 24 | fits | 107,731 | 56 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 119,771 | 1.198 | 20 | 50 | fits | 119,599 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 573,377 | 5.734 | 20 | 50 | fits | 120,271 | 74 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 307,025 | 3.070 | 18 | 18 | fits | 187,709 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,684,167 | 16.842 | 18 | 18 | fits | 36,826 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 440,342 | 4.403 | 20 | 20 | fits | 159,964 | 89 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 123,033 | 1.230 | 20 | 200 | fits | 119,599 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 581,660 | 5.817 | 20 | 200 | fits | 159,964 | 89 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 123,945 | 1.239 | 20 | 20 | fits | 119,599 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 837,159 | 8.372 | 20 | 20 | fits | 121,154 | 46 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 127,530 | 1.275 | 20 | 24 | fits | 119,599 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,566,344 | 15.663 | 20 | 24 | fits | 68,070 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 126,490 | 1.265 | 20 | 50 | fits | 119,599 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 585,336 | 5.853 | 20 | 50 | fits | 159,964 | 89 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 313,744 | 3.137 | 18 | 18 | fits | 187,709 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,665,888 | 16.659 | 18 | 18 | fits | 50,433 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 481,274 | 4.813 | 20 | 20 | fits | 166,478 | 101 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 129,752 | 1.298 | 20 | 200 | fits | 119,599 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 624,538 | 6.245 | 20 | 200 | fits | 166,478 | 101 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 130,664 | 1.307 | 20 | 20 | fits | 119,599 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 867,669 | 8.677 | 20 | 20 | fits | 120,615 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 134,249 | 1.342 | 20 | 24 | fits | 119,599 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,584,624 | 15.846 | 20 | 24 | fits | 100,278 | 45 | 0.738 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 133,209 | 1.332 | 20 | 50 | fits | 119,599 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 628,214 | 6.282 | 20 | 50 | fits | 166,478 | 101 | 0.681 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 290,786 | 2.908 | 18 | 18 | fits | 158,032 | 136 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,684,145 | 16.841 | 18 | 18 | fits | 50,211 | 18 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 441,860 | 4.419 | 20 | 20 | fits | 155,457 | 89 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 117,654 | 1.177 | 20 | 200 | fits | 119,599 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 584,443 | 5.844 | 20 | 200 | fits | 155,457 | 89 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 118,566 | 1.186 | 20 | 20 | fits | 119,599 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 827,560 | 8.276 | 20 | 20 | fits | 120,833 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 122,151 | 1.222 | 20 | 24 | fits | 119,599 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,512,668 | 15.127 | 20 | 24 | fits | 67,699 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 121,111 | 1.211 | 20 | 50 | fits | 119,599 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 588,119 | 5.881 | 20 | 50 | fits | 155,457 | 89 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 315,032 | 3.150 | 18 | 18 | fits | 194,376 | 145 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,682,571 | 16.826 | 18 | 18 | fits | 50,690 | 18 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 435,356 | 4.354 | 20 | 20 | fits | 156,124 | 83 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 118,711 | 1.187 | 20 | 200 | fits | 124,360 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 579,459 | 5.795 | 20 | 200 | fits | 156,124 | 83 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 119,623 | 1.196 | 20 | 20 | fits | 124,360 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 822,239 | 8.222 | 20 | 20 | fits | 120,636 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 123,208 | 1.232 | 20 | 24 | fits | 124,360 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,507,975 | 15.080 | 20 | 24 | fits | 67,699 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 122,168 | 1.222 | 20 | 50 | fits | 124,360 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 583,135 | 5.831 | 20 | 50 | fits | 156,124 | 83 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 426,946 | 4.269 | 18 | 18 | fits | 183,083 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,677,266 | 16.773 | 18 | 18 | fits | 36,663 | 15 | 0.774 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
