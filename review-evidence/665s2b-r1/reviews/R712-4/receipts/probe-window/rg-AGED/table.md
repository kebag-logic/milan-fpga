### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 88 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-a0.adp_available.if0` (backlog-adp@verify-a0) | 5.000 (6.283) | fits | 7 adp | 8 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-a3.service.acmp.first.if0` (backlog-adp@verify-a3) | 1.264 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-a5.service.acmp.last.if0` (backlog-adp@verify-a5) | 8.771 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-a3.service.adp.first.if0` (backlog-adp@verify-a3) | 1.255 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-a5.service.adp.last.if0` (backlog-adp@verify-a5) | 6.330 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-a3.service.aecp.first.if0` (backlog-adp@verify-a3) | 1.300 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@verify-a5.service.aecp.last.if1` (backlog-adp@verify-a5) | 16.513 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-a3.service.maap.first.if0` (backlog-adp@verify-a3) | 1.290 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-a5.service.maap.last.if0` (backlog-adp@verify-a5) | 6.366 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-a0.service.srp.first.if0` (backlog-adp@verify-a0) | 4.918 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-a4.service.srp.last.if1` (backlog-adp@verify-a4) | 17.651 | fits | 31 srp | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@verify-7 | 0 | 17.898 | 17 | 183,824 (1.838) | yes | - |
| backlog-adp@verify-a0 | 1 | 18.978 | 19 | 183,019 (1.830) | yes | - |
| backlog-adp@verify-a1 | 0 | 19.178 | 21 | 166,431 (1.664) | yes | - |
| backlog-adp@verify-a2 | 1 | 18.602 | 20 | 171,831 (1.718) | yes | - |
| backlog-adp@verify-a3 | 0 | 18.043 | 18 | 195,535 (1.955) | yes | - |
| backlog-adp@verify-a4 | 0 | 18.259 | 19 | 188,866 (1.889) | yes | - |
| backlog-adp@verify-a5 | 0 | 18.120 | 18 | 195,418 (1.954) | yes | - |
| backlog-adp@verify-a6 | 0 | 17.547 | 17 | 188,860 (1.889) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@verify-7 | 1045 | 0 | 183,824 (1.838) | fits |
| backlog-adp@verify-a0 | 1145 | 0 | 183,019 (1.830) | fits |
| backlog-adp@verify-a1 | 1161 | 0 | 166,431 (1.664) | fits |
| backlog-adp@verify-a2 | 1179 | 0 | 171,831 (1.718) | fits |
| backlog-adp@verify-a3 | 1195 | 0 | 195,535 (1.955) | fits |
| backlog-adp@verify-a4 | 1214 | 0 | 188,866 (1.889) | fits |
| backlog-adp@verify-a5 | 1232 | 0 | 195,418 (1.954) | fits |
| backlog-adp@verify-a6 | 1249 | 0 | 188,860 (1.889) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@verify-7 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a0 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a1 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a2 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a3 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a4 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a5 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a6 | 547 | 122,002 (1.220) | 96,031 (0.960) |

Longest pass that carries a step: 122,002 CPU cycles (1.220 ms), backlog-adp@verify-7; longest step: 96,031 (0.960 ms), backlog-adp@verify-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 434,500 | 4.345 | 20 | 20 | fits | 156,453 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 117,538 | 1.175 | 20 | 200 | fits | 123,888 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 579,247 | 5.792 | 20 | 200 | fits | 156,453 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 118,450 | 1.185 | 20 | 20 | fits | 123,888 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 823,400 | 8.234 | 20 | 20 | fits | 121,100 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 122,035 | 1.220 | 20 | 24 | fits | 123,888 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,517,639 | 15.176 | 20 | 24 | fits | 67,358 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 120,995 | 1.210 | 20 | 50 | fits | 123,888 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 582,923 | 5.829 | 20 | 50 | fits | 156,453 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 426,405 | 4.264 | 18 | 18 | fits | 183,824 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,651,864 | 16.519 | 18 | 18 | fits | 50,594 | 18 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a0.adp_available.if0` | 499,993 | 5.000 | 20 | 20 | fits | 127,445 | 85 | 0.640 |
| ADP record released under the composed load, first | `backlog-adp@verify-a0.service.adp.first.if0` | 111,225 | 1.112 | 20 | 200 | fits | 123,216 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-a0.service.adp.last.if0` | 615,670 | 6.157 | 20 | 200 | fits | 127,445 | 85 | 0.640 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a0.service.acmp.first.if0` | 112,137 | 1.121 | 20 | 20 | fits | 123,216 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a0.service.acmp.last.if0` | 861,609 | 8.616 | 20 | 20 | fits | 121,593 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@verify-a0.service.aecp.first.if0` | 115,722 | 1.157 | 20 | 24 | fits | 123,216 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@verify-a0.service.aecp.last.if1` | 1,559,914 | 15.599 | 20 | 24 | fits | 67,698 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a0.service.maap.first.if0` | 114,682 | 1.147 | 20 | 50 | fits | 123,216 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a0.service.maap.last.if0` | 619,346 | 6.193 | 20 | 50 | fits | 127,445 | 85 | 0.640 |
| SRP record released under the composed load, first | `backlog-adp@verify-a0.service.srp.first.if0` | 491,836 | 4.918 | 18 | 18 | fits | 183,019 | 104 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp@verify-a0.service.srp.last.if1` | 1,759,921 | 17.599 | 18 | 18 | fits | 50,155 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a1.adp_available.if0` | 462,090 | 4.621 | 20 | 20 | fits | 155,471 | 83 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@verify-a1.service.adp.first.if0` | 119,458 | 1.195 | 20 | 200 | fits | 118,815 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-a1.service.adp.last.if0` | 606,301 | 6.063 | 20 | 200 | fits | 155,471 | 83 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a1.service.acmp.first.if0` | 120,370 | 1.204 | 20 | 20 | fits | 118,815 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a1.service.acmp.last.if0` | 823,851 | 8.239 | 20 | 20 | fits | 127,774 | 52 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@verify-a1.service.aecp.first.if0` | 123,955 | 1.240 | 20 | 24 | fits | 118,815 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-a1.service.aecp.last.if1` | 1,550,982 | 15.510 | 20 | 24 | fits | 67,661 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a1.service.maap.first.if0` | 122,915 | 1.229 | 20 | 50 | fits | 118,815 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a1.service.maap.last.if0` | 609,977 | 6.100 | 20 | 50 | fits | 155,471 | 83 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@verify-a1.service.srp.first.if0` | 288,010 | 2.880 | 18 | 18 | fits | 165,550 | 147 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@verify-a1.service.srp.last.if1` | 1,694,888 | 16.949 | 18 | 18 | fits | 57,272 | 24 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a2.adp_available.if0` | 454,865 | 4.549 | 20 | 20 | fits | 155,810 | 83 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@verify-a2.service.adp.first.if0` | 112,854 | 1.129 | 20 | 200 | fits | 118,884 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-a2.service.adp.last.if0` | 599,353 | 5.994 | 20 | 200 | fits | 155,810 | 83 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a2.service.acmp.first.if0` | 113,766 | 1.138 | 20 | 20 | fits | 118,884 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a2.service.acmp.last.if0` | 817,705 | 8.177 | 20 | 20 | fits | 122,564 | 52 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@verify-a2.service.aecp.first.if0` | 117,351 | 1.174 | 20 | 24 | fits | 118,884 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-a2.service.aecp.last.if1` | 1,479,176 | 14.792 | 20 | 24 | fits | 41,680 | 33 | 0.679 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a2.service.maap.first.if0` | 116,311 | 1.163 | 20 | 50 | fits | 118,884 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a2.service.maap.last.if0` | 603,029 | 6.030 | 20 | 50 | fits | 155,810 | 83 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@verify-a2.service.srp.first.if0` | 275,323 | 2.753 | 18 | 18 | fits | 159,467 | 141 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-a2.service.srp.last.if1` | 1,722,650 | 17.227 | 18 | 18 | fits | 36,735 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a3.adp_available.if0` | 480,801 | 4.808 | 20 | 20 | fits | 154,381 | 83 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@verify-a3.service.adp.first.if0` | 125,512 | 1.255 | 20 | 200 | fits | 118,819 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-a3.service.adp.last.if0` | 623,931 | 6.239 | 20 | 200 | fits | 154,381 | 83 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a3.service.acmp.first.if0` | 126,424 | 1.264 | 20 | 20 | fits | 118,819 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a3.service.acmp.last.if0` | 867,840 | 8.678 | 20 | 20 | fits | 121,031 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-a3.service.aecp.first.if0` | 130,009 | 1.300 | 20 | 24 | fits | 118,819 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-a3.service.aecp.last.if1` | 1,566,419 | 15.664 | 20 | 24 | fits | 67,825 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a3.service.maap.first.if0` | 128,969 | 1.290 | 20 | 50 | fits | 118,819 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a3.service.maap.last.if0` | 627,607 | 6.276 | 20 | 50 | fits | 154,381 | 83 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-a3.service.srp.first.if0` | 324,049 | 3.240 | 18 | 18 | fits | 195,535 | 151 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@verify-a3.service.srp.last.if1` | 1,666,320 | 16.663 | 18 | 18 | fits | 50,451 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a4.adp_available.if0` | 466,324 | 4.663 | 20 | 20 | fits | 120,483 | 74 | 0.622 |
| ADP record released under the composed load, first | `backlog-adp@verify-a4.service.adp.first.if0` | 119,780 | 1.198 | 20 | 200 | fits | 118,808 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-a4.service.adp.last.if0` | 575,494 | 5.755 | 20 | 200 | fits | 120,483 | 74 | 0.622 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a4.service.acmp.first.if0` | 120,692 | 1.207 | 20 | 20 | fits | 118,808 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a4.service.acmp.last.if0` | 837,120 | 8.371 | 20 | 20 | fits | 132,990 | 64 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@verify-a4.service.aecp.first.if0` | 124,277 | 1.243 | 20 | 24 | fits | 118,808 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-a4.service.aecp.last.if1` | 1,525,654 | 15.257 | 20 | 24 | fits | 41,593 | 33 | 0.675 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a4.service.maap.first.if0` | 123,237 | 1.232 | 20 | 50 | fits | 118,808 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a4.service.maap.last.if0` | 579,170 | 5.792 | 20 | 50 | fits | 120,483 | 74 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp@verify-a4.service.srp.first.if0` | 311,648 | 3.116 | 18 | 18 | fits | 188,866 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@verify-a4.service.srp.last.if1` | 1,765,117 | 17.651 | 18 | 18 | fits | 50,155 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a5.adp_available.if0` | 489,388 | 4.894 | 20 | 20 | fits | 154,924 | 83 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@verify-a5.service.adp.first.if0` | 125,217 | 1.252 | 20 | 200 | fits | 118,808 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-a5.service.adp.last.if0` | 632,959 | 6.330 | 20 | 200 | fits | 154,924 | 83 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a5.service.acmp.first.if0` | 126,129 | 1.261 | 20 | 20 | fits | 118,808 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a5.service.acmp.last.if0` | 877,091 | 8.771 | 20 | 20 | fits | 121,144 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-a5.service.aecp.first.if0` | 129,714 | 1.297 | 20 | 24 | fits | 118,808 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-a5.service.aecp.last.if1` | 1,651,295 | 16.513 | 20 | 24 | fits | 67,356 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a5.service.maap.first.if0` | 128,674 | 1.287 | 20 | 50 | fits | 118,808 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a5.service.maap.last.if0` | 636,635 | 6.366 | 20 | 50 | fits | 154,924 | 83 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@verify-a5.service.srp.first.if0` | 323,637 | 3.236 | 18 | 18 | fits | 195,418 | 145 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-a5.service.srp.last.if1` | 1,751,214 | 17.512 | 18 | 18 | fits | 50,451 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a6.adp_available.if0` | 471,918 | 4.719 | 20 | 20 | fits | 154,870 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-a6.service.adp.first.if0` | 125,437 | 1.254 | 20 | 200 | fits | 118,884 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-a6.service.adp.last.if0` | 615,475 | 6.155 | 20 | 200 | fits | 154,870 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a6.service.acmp.first.if0` | 126,349 | 1.263 | 20 | 20 | fits | 118,884 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a6.service.acmp.last.if0` | 876,400 | 8.764 | 20 | 20 | fits | 137,987 | 70 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp@verify-a6.service.aecp.first.if0` | 129,934 | 1.299 | 20 | 24 | fits | 118,884 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-a6.service.aecp.last.if1` | 1,644,451 | 16.445 | 20 | 24 | fits | 70,865 | 37 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a6.service.maap.first.if0` | 128,894 | 1.289 | 20 | 50 | fits | 118,884 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a6.service.maap.last.if0` | 619,151 | 6.192 | 20 | 50 | fits | 154,870 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-a6.service.srp.first.if0` | 317,299 | 3.173 | 18 | 18 | fits | 188,860 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-a6.service.srp.last.if1` | 1,693,800 | 16.938 | 18 | 18 | fits | 51,884 | 20 | 0.737 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
