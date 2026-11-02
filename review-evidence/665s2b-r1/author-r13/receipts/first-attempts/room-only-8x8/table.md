### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 11 paths and 4 of 154 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 5.284 (6.788) | fits | 7 adp | 14 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.853 | fits | 0 acmp | 14 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 8.879 | fits | 11 acmp | 14 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.843 | fits | 0 adp | 14 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.437 | fits | 7 adp | 14 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.888 | fits | 0 aecp | 14 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@blank-4.service.aecp.last.if1` (backlog-adp@blank-4) | 16.983 | fits | 15 aecp | 14 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.878 | fits | 0 maap | 14 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.474 | fits | 6 maap | 14 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-3.service.srp.first.if0` (backlog-adp@program-3) | 4.391 | fits | 0 srp | 14 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-5.service.srp.last.if1` (backlog-adp@blank-5) | 18.211 | MISS ceiling | 31 srp | 14 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.282 | 18 | 187,980 (1.880) | yes | - |
| backlog-adp@blank-1 | 0 | 17.614 | 18 | 187,945 (1.879) | yes | - |
| backlog-adp@blank-2 | 0 | 18.777 | 19 | 187,945 (1.879) | yes | - |
| backlog-adp@blank-3 | 0 | 18.832 | 19 | 182,387 (1.824) | yes | - |
| backlog-adp@blank-4 | 0 | 18.649 | 18 | 190,435 (1.904) | yes | - |
| backlog-adp@blank-5 | 0 | 18.820 | 20 | 187,688 (1.877) | yes | - |
| backlog-adp@blank-6 | 0 | 18.638 | 19 | 187,269 (1.873) | yes | - |
| backlog-adp@blank-7 | 0 | 18.804 | 19 | 194,957 (1.950) | yes | - |
| backlog-adp@program-0 | 0 | 17.906 | 18 | 189,406 (1.894) | yes | - |
| backlog-adp@program-1 | 0 | 18.020 | 19 | 187,090 (1.871) | yes | - |
| backlog-adp@program-2 | 0 | 18.152 | 19 | 187,090 (1.871) | yes | - |
| backlog-adp@program-3 | 0 | 17.840 | 18 | 182,328 (1.823) | yes | - |
| backlog-adp@program-5 | 0 | 17.970 | 19 | 187,317 (1.873) | yes | - |
| backlog-adp@program-6 | 0 | 18.656 | 20 | 181,618 (1.816) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 489 | 0 | 187,980 (1.880) | fits |
| backlog-adp@blank-1 | 489 | 0 | 187,945 (1.879) | fits |
| backlog-adp@blank-2 | 490 | 0 | 187,945 (1.879) | fits |
| backlog-adp@blank-3 | 490 | 0 | 182,387 (1.824) | fits |
| backlog-adp@blank-4 | 489 | 0 | 190,435 (1.904) | fits |
| backlog-adp@blank-5 | 492 | 0 | 187,688 (1.877) | fits |
| backlog-adp@blank-6 | 491 | 0 | 187,269 (1.873) | fits |
| backlog-adp@blank-7 | 491 | 0 | 194,957 (1.950) | fits |
| backlog-adp@program-0 | 762 | 0 | 189,406 (1.894) | fits |
| backlog-adp@program-1 | 764 | 0 | 187,090 (1.871) | fits |
| backlog-adp@program-2 | 764 | 0 | 187,090 (1.871) | fits |
| backlog-adp@program-3 | 763 | 0 | 182,328 (1.823) | fits |
| backlog-adp@program-5 | 765 | 0 | 187,317 (1.873) | fits |
| backlog-adp@program-6 | 766 | 0 | 181,618 (1.816) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 528,428 | 5.284 | 20 | 20 | fits | 126,295 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 184,345 | 1.843 | 20 | 200 | fits | 119,135 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 643,679 | 6.437 | 20 | 200 | fits | 126,295 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 185,257 | 1.853 | 20 | 20 | fits | 119,135 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 887,898 | 8.879 | 20 | 20 | fits | 120,826 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 188,842 | 1.888 | 20 | 24 | fits | 119,135 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,666,465 | 16.665 | 20 | 24 | fits | 67,993 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 187,802 | 1.878 | 20 | 50 | fits | 119,135 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 647,355 | 6.474 | 20 | 50 | fits | 126,295 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 375,327 | 3.753 | 18 | 18 | fits | 187,980 | 140 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,766,612 | 17.666 | 18 | 18 | fits | 50,775 | 18 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 469,494 | 4.695 | 20 | 20 | fits | 157,214 | 89 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 115,637 | 1.156 | 20 | 200 | fits | 118,701 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 612,586 | 6.126 | 20 | 200 | fits | 157,214 | 89 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 116,549 | 1.165 | 20 | 20 | fits | 118,701 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 855,214 | 8.552 | 20 | 20 | fits | 120,435 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 120,134 | 1.201 | 20 | 24 | fits | 118,701 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,599,655 | 15.997 | 20 | 24 | fits | 68,125 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 119,094 | 1.191 | 20 | 50 | fits | 118,701 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 616,262 | 6.163 | 20 | 50 | fits | 157,214 | 89 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 306,584 | 3.066 | 18 | 18 | fits | 187,945 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,699,802 | 16.998 | 18 | 18 | fits | 50,775 | 18 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 477,368 | 4.774 | 20 | 20 | fits | 154,597 | 83 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 122,349 | 1.223 | 20 | 200 | fits | 118,701 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 620,898 | 6.209 | 20 | 200 | fits | 154,597 | 83 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 123,261 | 1.233 | 20 | 20 | fits | 118,701 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 857,922 | 8.579 | 20 | 20 | fits | 128,318 | 52 | 0.690 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 126,846 | 1.268 | 20 | 24 | fits | 118,701 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,629,323 | 16.293 | 20 | 24 | fits | 68,014 | 31 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 125,806 | 1.258 | 20 | 50 | fits | 118,701 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 624,574 | 6.246 | 20 | 50 | fits | 154,597 | 83 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 313,296 | 3.133 | 18 | 18 | fits | 187,945 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,715,738 | 17.157 | 18 | 18 | fits | 37,239 | 15 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 443,806 | 4.438 | 20 | 20 | fits | 156,003 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 129,061 | 1.291 | 20 | 200 | fits | 118,701 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 588,119 | 5.881 | 20 | 200 | fits | 156,003 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 129,973 | 1.300 | 20 | 20 | fits | 118,701 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 838,614 | 8.386 | 20 | 20 | fits | 121,055 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 133,558 | 1.336 | 20 | 24 | fits | 118,701 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,609,255 | 16.093 | 20 | 24 | fits | 67,789 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 132,518 | 1.325 | 20 | 50 | fits | 118,701 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 591,795 | 5.918 | 20 | 50 | fits | 156,003 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 435,727 | 4.357 | 18 | 18 | fits | 182,387 | 104 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,791,386 | 17.914 | 18 | 18 | fits | 51,456 | 18 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 476,325 | 4.763 | 20 | 20 | fits | 162,173 | 89 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 122,758 | 1.228 | 20 | 200 | fits | 124,502 | 151 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 620,449 | 6.204 | 20 | 200 | fits | 162,173 | 89 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 123,670 | 1.237 | 20 | 20 | fits | 124,502 | 151 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 863,598 | 8.636 | 20 | 20 | fits | 120,967 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 127,255 | 1.273 | 20 | 24 | fits | 124,502 | 151 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,698,282 | 16.983 | 20 | 24 | fits | 61,772 | 38 | 0.762 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 126,215 | 1.262 | 20 | 50 | fits | 124,502 | 151 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 624,125 | 6.241 | 20 | 50 | fits | 162,173 | 89 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 316,195 | 3.162 | 18 | 18 | fits | 190,435 | 145 | 0.638 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,803,314 | 18.033 | 18 | 18 | MISS ceiling | 50,947 | 18 | 0.733 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 430,968 | 4.310 | 20 | 20 | fits | 161,109 | 89 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 114,092 | 1.141 | 20 | 200 | fits | 118,546 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 573,652 | 5.737 | 20 | 200 | fits | 161,109 | 89 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 115,004 | 1.150 | 20 | 20 | fits | 118,546 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 865,190 | 8.652 | 20 | 20 | fits | 169,188 | 48 | 0.503 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 118,589 | 1.186 | 20 | 24 | fits | 118,546 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,634,218 | 16.342 | 20 | 24 | fits | 71,251 | 37 | 0.723 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 117,549 | 1.175 | 20 | 50 | fits | 118,546 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 577,328 | 5.773 | 20 | 50 | fits | 161,109 | 89 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 304,782 | 3.048 | 18 | 18 | fits | 187,688 | 140 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,821,142 | 18.211 | 18 | 18 | MISS ceiling | 36,991 | 15 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 434,309 | 4.343 | 20 | 20 | fits | 156,550 | 83 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 120,804 | 1.208 | 20 | 200 | fits | 118,546 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 579,468 | 5.795 | 20 | 200 | fits | 156,550 | 83 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 121,716 | 1.217 | 20 | 20 | fits | 118,546 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 872,697 | 8.727 | 20 | 20 | fits | 122,938 | 52 | 0.695 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 125,301 | 1.253 | 20 | 24 | fits | 118,546 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,651,417 | 16.514 | 20 | 24 | fits | 68,212 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 124,261 | 1.243 | 20 | 50 | fits | 118,546 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 583,144 | 5.831 | 20 | 50 | fits | 156,550 | 83 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 426,529 | 4.265 | 18 | 18 | fits | 187,269 | 104 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,802,174 | 18.022 | 18 | 18 | MISS ceiling | 50,685 | 18 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 478,782 | 4.788 | 20 | 20 | fits | 126,680 | 85 | 0.629 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 127,516 | 1.275 | 20 | 200 | fits | 118,546 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 594,752 | 5.948 | 20 | 200 | fits | 126,680 | 85 | 0.629 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 128,428 | 1.284 | 20 | 20 | fits | 118,546 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 839,828 | 8.398 | 20 | 20 | fits | 121,320 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 132,013 | 1.320 | 20 | 24 | fits | 118,546 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,668,013 | 16.680 | 20 | 24 | fits | 67,993 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 130,973 | 1.310 | 20 | 50 | fits | 118,546 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 598,428 | 5.984 | 20 | 50 | fits | 126,680 | 85 | 0.629 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 325,475 | 3.255 | 18 | 18 | fits | 194,957 | 145 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,818,845 | 18.188 | 18 | 18 | MISS ceiling | 50,685 | 18 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 482,903 | 4.829 | 20 | 20 | fits | 154,432 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 137,442 | 1.374 | 20 | 200 | fits | 125,431 | 151 | 0.535 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 626,196 | 6.262 | 20 | 200 | fits | 154,432 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 138,354 | 1.384 | 20 | 20 | fits | 125,431 | 151 | 0.535 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 868,149 | 8.681 | 20 | 20 | fits | 120,324 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 141,939 | 1.419 | 20 | 24 | fits | 125,431 | 151 | 0.535 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,650,923 | 16.509 | 20 | 24 | fits | 67,824 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 140,899 | 1.409 | 20 | 50 | fits | 125,431 | 151 | 0.535 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 629,872 | 6.299 | 20 | 50 | fits | 154,432 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 329,850 | 3.299 | 18 | 18 | fits | 189,406 | 145 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,706,843 | 17.068 | 18 | 18 | fits | 58,455 | 31 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 459,886 | 4.599 | 20 | 20 | fits | 154,429 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 116,645 | 1.166 | 20 | 200 | fits | 119,355 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 603,119 | 6.031 | 20 | 200 | fits | 154,429 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 117,557 | 1.176 | 20 | 20 | fits | 119,355 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 827,899 | 8.279 | 20 | 20 | fits | 129,773 | 58 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 121,142 | 1.211 | 20 | 24 | fits | 119,355 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,592,208 | 15.922 | 20 | 24 | fits | 68,336 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 120,102 | 1.201 | 20 | 50 | fits | 119,355 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 606,795 | 6.068 | 20 | 50 | fits | 154,429 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 306,737 | 3.067 | 18 | 18 | fits | 187,090 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,741,179 | 17.412 | 18 | 18 | fits | 38,622 | 15 | 0.821 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 454,030 | 4.540 | 20 | 20 | fits | 163,534 | 95 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 130,069 | 1.301 | 20 | 200 | fits | 119,355 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 597,459 | 5.975 | 20 | 200 | fits | 163,534 | 95 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 130,981 | 1.310 | 20 | 20 | fits | 119,355 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 840,831 | 8.408 | 20 | 20 | fits | 121,008 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 134,566 | 1.346 | 20 | 24 | fits | 119,355 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,617,408 | 16.174 | 20 | 24 | fits | 68,038 | 31 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 133,526 | 1.335 | 20 | 50 | fits | 119,355 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 601,135 | 6.011 | 20 | 50 | fits | 163,534 | 95 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 320,161 | 3.202 | 18 | 18 | fits | 187,090 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,754,361 | 17.544 | 18 | 18 | fits | 37,224 | 15 | 0.787 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 446,960 | 4.470 | 20 | 20 | fits | 156,581 | 83 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 124,677 | 1.247 | 20 | 200 | fits | 119,355 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 592,085 | 5.921 | 20 | 200 | fits | 156,581 | 83 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 125,589 | 1.256 | 20 | 20 | fits | 119,355 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 835,015 | 8.350 | 20 | 20 | fits | 120,856 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 129,174 | 1.292 | 20 | 24 | fits | 119,355 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,622,463 | 16.225 | 20 | 24 | fits | 67,824 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 128,134 | 1.281 | 20 | 50 | fits | 119,355 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 595,761 | 5.958 | 20 | 50 | fits | 156,581 | 83 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 439,115 | 4.391 | 18 | 18 | fits | 182,328 | 104 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,722,421 | 17.224 | 18 | 18 | fits | 50,700 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 470,134 | 4.701 | 20 | 20 | fits | 157,279 | 89 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 116,831 | 1.168 | 20 | 200 | fits | 119,542 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 613,226 | 6.132 | 20 | 200 | fits | 157,279 | 89 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 117,743 | 1.177 | 20 | 20 | fits | 119,542 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 863,649 | 8.636 | 20 | 20 | fits | 121,029 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 121,328 | 1.213 | 20 | 24 | fits | 119,542 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,528,494 | 15.285 | 20 | 24 | fits | 67,991 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 120,288 | 1.203 | 20 | 50 | fits | 119,542 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 616,902 | 6.169 | 20 | 50 | fits | 157,279 | 89 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 307,150 | 3.071 | 18 | 18 | fits | 187,317 | 140 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,628,566 | 16.286 | 18 | 18 | fits | 50,700 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 421,949 | 4.219 | 20 | 20 | fits | 181,618 | 89 | 0.709 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 130,255 | 1.303 | 20 | 200 | fits | 119,542 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 584,634 | 5.846 | 20 | 200 | fits | 181,618 | 89 | 0.709 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 131,167 | 1.312 | 20 | 20 | fits | 119,542 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 828,532 | 8.285 | 20 | 20 | fits | 120,708 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 134,752 | 1.348 | 20 | 24 | fits | 119,542 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,619,122 | 16.191 | 20 | 24 | fits | 69,587 | 31 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 133,712 | 1.337 | 20 | 50 | fits | 119,542 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 588,310 | 5.883 | 20 | 50 | fits | 181,618 | 89 | 0.709 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 406,627 | 4.066 | 18 | 18 | fits | 151,965 | 100 | 0.656 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,755,525 | 17.555 | 18 | 18 | fits | 36,991 | 15 | 0.783 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
