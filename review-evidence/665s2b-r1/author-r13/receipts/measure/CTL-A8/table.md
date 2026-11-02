### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 11 paths and 11 of 264 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-5.adp_available.if0` (backlog-adp@verify-5) | 5.697 (7.325) | fits | 7 adp | 24 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.868 | fits | 0 acmp | 24 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-5.service.acmp.last.if0` (backlog-adp@verify-5) | 9.571 | fits | 11 acmp | 24 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.859 | fits | 0 adp | 24 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-5.service.adp.last.if0` (backlog-adp@verify-5) | 7.135 | fits | 7 adp | 24 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.904 | fits | 0 aecp | 24 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@verify-4.service.aecp.last.if1` (backlog-adp@verify-4) | 17.237 | fits | 15 aecp | 24 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.893 | fits | 0 maap | 24 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-5.service.maap.last.if0` (backlog-adp@verify-5) | 7.172 | fits | 6 maap | 24 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-3.service.srp.first.if0` (backlog-adp@program-3) | 5.216 | fits | 0 srp | 24 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-1.service.srp.last.if1` (backlog-adp@verify-1) | 19.002 | MISS ceiling | 31 srp | 24 | 11 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.276 | 18 | 188,039 (1.880) | yes | - |
| backlog-adp@blank-1 | 0 | 17.626 | 18 | 188,010 (1.880) | yes | - |
| backlog-adp@blank-2 | 0 | 18.766 | 19 | 203,943 (2.039) | yes | - |
| backlog-adp@blank-3 | 0 | 18.843 | 19 | 203,966 (2.040) | yes | - |
| backlog-adp@blank-4 | 0 | 18.570 | 18 | 237,279 (2.373) | yes | - |
| backlog-adp@blank-5 | 0 | 18.898 | 20 | 236,347 (2.363) | yes | - |
| backlog-adp@blank-6 | 0 | 18.889 | 20 | 262,881 (2.629) | yes | - |
| backlog-adp@blank-7 | 0 | 18.961 | 20 | 270,522 (2.705) | yes | - |
| backlog-adp@program-0 | 0 | 17.919 | 18 | 189,562 (1.896) | yes | - |
| backlog-adp@program-1 | 0 | 17.776 | 18 | 210,860 (2.109) | yes | - |
| backlog-adp@program-2 | 0 | 17.889 | 18 | 244,655 (2.447) | yes | - |
| backlog-adp@program-3 | 0 | 17.824 | 18 | 210,011 (2.100) | yes | - |
| backlog-adp@program-4 | 0 | 17.167 | 19 | 186,861 (1.869) | yes | - |
| backlog-adp@program-5 | 0 | 17.963 | 19 | 186,891 (1.869) | yes | - |
| backlog-adp@program-6 | 0 | 18.669 | 20 | 186,317 (1.863) | yes | - |
| backlog-adp@program-7 | 0 | 17.834 | 18 | 198,241 (1.982) | yes | - |
| backlog-adp@verify-0 | 0 | 18.123 | 18 | 194,828 (1.948) | yes | - |
| backlog-adp@verify-1 | 0 | 19.615 | 21 | 182,971 (1.830) | yes | - |
| backlog-adp@verify-2 | 0 | 19.195 | 19 | 203,428 (2.034) | yes | - |
| backlog-adp@verify-3 | 0 | 18.770 | 18 | 203,952 (2.040) | yes | - |
| backlog-adp@verify-4 | 0 | 18.848 | 18 | 237,227 (2.372) | yes | - |
| backlog-adp@verify-5 | 0 | 18.951 | 18 | 229,620 (2.296) | yes | - |
| backlog-adp@verify-6 | 0 | 19.194 | 20 | 240,801 (2.408) | yes | - |
| backlog-adp@verify-7 | 0 | 19.133 | 19 | 204,670 (2.047) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 486 | 0 | 188,039 (1.880) | fits |
| backlog-adp@blank-1 | 486 | 0 | 188,010 (1.880) | fits |
| backlog-adp@blank-2 | 487 | 1 | 203,943 (2.039) | OVER the share |
| backlog-adp@blank-3 | 487 | 1 | 203,966 (2.040) | OVER the share |
| backlog-adp@blank-4 | 486 | 1 | 237,279 (2.373) | OVER the share |
| backlog-adp@blank-5 | 489 | 1 | 236,347 (2.363) | OVER the share |
| backlog-adp@blank-6 | 489 | 1 | 262,881 (2.629) | OVER the share |
| backlog-adp@blank-7 | 489 | 1 | 270,522 (2.705) | OVER the share |
| backlog-adp@program-0 | 766 | 0 | 189,562 (1.896) | fits |
| backlog-adp@program-1 | 767 | 1 | 210,860 (2.109) | OVER the share |
| backlog-adp@program-2 | 767 | 1 | 244,655 (2.447) | OVER the share |
| backlog-adp@program-3 | 767 | 1 | 210,011 (2.100) | OVER the share |
| backlog-adp@program-4 | 770 | 0 | 186,861 (1.869) | fits |
| backlog-adp@program-5 | 770 | 0 | 186,891 (1.869) | fits |
| backlog-adp@program-6 | 771 | 0 | 186,317 (1.863) | fits |
| backlog-adp@program-7 | 770 | 0 | 198,241 (1.982) | fits |
| backlog-adp@verify-0 | 1024 | 0 | 194,828 (1.948) | fits |
| backlog-adp@verify-1 | 1027 | 0 | 182,971 (1.830) | fits |
| backlog-adp@verify-2 | 1025 | 1 | 203,428 (2.034) | OVER the share |
| backlog-adp@verify-3 | 1026 | 1 | 203,952 (2.040) | OVER the share |
| backlog-adp@verify-4 | 1026 | 1 | 237,227 (2.372) | OVER the share |
| backlog-adp@verify-5 | 1026 | 1 | 229,620 (2.296) | OVER the share |
| backlog-adp@verify-6 | 1028 | 1 | 240,801 (2.408) | OVER the share |
| backlog-adp@verify-7 | 1027 | 1 | 204,670 (2.047) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 530,856 | 5.309 | 20 | 20 | fits | 126,545 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 185,889 | 1.859 | 20 | 200 | fits | 119,706 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 646,190 | 6.462 | 20 | 200 | fits | 126,545 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 186,801 | 1.868 | 20 | 20 | fits | 119,706 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 890,918 | 8.909 | 20 | 20 | fits | 121,257 | 46 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 190,386 | 1.904 | 20 | 24 | fits | 119,706 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,666,258 | 16.663 | 20 | 24 | fits | 67,658 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 189,346 | 1.893 | 20 | 50 | fits | 119,706 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 649,866 | 6.499 | 20 | 50 | fits | 126,545 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 376,930 | 3.769 | 18 | 18 | fits | 188,039 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,765,922 | 17.659 | 18 | 18 | fits | 50,487 | 18 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 472,294 | 4.723 | 20 | 20 | fits | 157,621 | 89 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 117,338 | 1.173 | 20 | 200 | fits | 119,406 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 615,701 | 6.157 | 20 | 200 | fits | 157,621 | 89 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 118,250 | 1.183 | 20 | 20 | fits | 119,406 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 859,000 | 8.590 | 20 | 20 | fits | 120,845 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 121,835 | 1.218 | 20 | 24 | fits | 119,406 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,600,919 | 16.009 | 20 | 24 | fits | 67,714 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 120,795 | 1.208 | 20 | 50 | fits | 119,406 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 619,377 | 6.194 | 20 | 50 | fits | 157,621 | 89 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 308,350 | 3.083 | 18 | 18 | fits | 188,010 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,700,973 | 17.010 | 18 | 18 | fits | 50,682 | 18 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 480,314 | 4.803 | 20 | 20 | fits | 154,722 | 83 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 124,092 | 1.241 | 20 | 200 | fits | 119,406 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 623,825 | 6.238 | 20 | 200 | fits | 154,722 | 83 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 125,004 | 1.250 | 20 | 20 | fits | 119,406 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 936,640 | 9.366 | 20 | 20 | fits | 203,943 | 52 | 0.558 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 128,589 | 1.286 | 20 | 24 | fits | 119,406 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,615,356 | 16.154 | 20 | 24 | fits | 67,613 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 127,549 | 1.275 | 20 | 50 | fits | 119,406 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 627,501 | 6.275 | 20 | 50 | fits | 154,722 | 83 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 315,104 | 3.151 | 18 | 18 | fits | 188,010 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,714,806 | 17.148 | 18 | 18 | fits | 50,409 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 446,585 | 4.466 | 20 | 20 | fits | 156,290 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 130,846 | 1.308 | 20 | 200 | fits | 119,406 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 591,068 | 5.911 | 20 | 200 | fits | 156,290 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 131,758 | 1.318 | 20 | 20 | fits | 119,406 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 916,944 | 9.169 | 20 | 20 | fits | 121,214 | 46 | 0.692 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 135,343 | 1.353 | 20 | 24 | fits | 119,406 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,610,698 | 16.107 | 20 | 24 | fits | 67,612 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 134,303 | 1.343 | 20 | 50 | fits | 119,406 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 594,744 | 5.947 | 20 | 50 | fits | 156,290 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 438,389 | 4.384 | 18 | 18 | fits | 183,229 | 104 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,800,400 | 18.004 | 18 | 18 | MISS ceiling | 58,636 | 29 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 478,709 | 4.787 | 20 | 20 | fits | 237,279 | 89 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 124,627 | 1.246 | 20 | 200 | fits | 125,255 | 151 | 0.536 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 698,052 | 6.981 | 20 | 200 | fits | 237,279 | 89 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 125,539 | 1.255 | 20 | 20 | fits | 125,255 | 151 | 0.536 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 914,425 | 9.144 | 20 | 20 | fits | 94,072 | 48 | 0.660 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 129,124 | 1.291 | 20 | 24 | fits | 125,255 | 151 | 0.536 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,690,316 | 16.903 | 20 | 24 | fits | 75,683 | 42 | 0.737 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 128,084 | 1.281 | 20 | 50 | fits | 125,255 | 151 | 0.536 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 701,728 | 7.017 | 20 | 50 | fits | 237,279 | 89 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 318,080 | 3.181 | 18 | 18 | fits | 190,451 | 145 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,795,394 | 17.954 | 18 | 18 | fits | 50,894 | 18 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 434,018 | 4.340 | 20 | 20 | fits | 236,347 | 89 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 116,097 | 1.161 | 20 | 200 | fits | 119,262 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 651,918 | 6.519 | 20 | 200 | fits | 236,347 | 89 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 117,009 | 1.170 | 20 | 20 | fits | 119,262 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 892,203 | 8.922 | 20 | 20 | fits | 123,738 | 52 | 0.702 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 120,594 | 1.206 | 20 | 24 | fits | 119,262 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,641,831 | 16.418 | 20 | 24 | fits | 71,022 | 37 | 0.722 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 119,554 | 1.196 | 20 | 50 | fits | 119,262 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 655,594 | 6.556 | 20 | 50 | fits | 236,347 | 89 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 307,196 | 3.072 | 18 | 18 | fits | 188,097 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,828,833 | 18.288 | 18 | 18 | MISS ceiling | 36,968 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 512,388 | 5.124 | 20 | 20 | fits | 149,706 | 90 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 122,851 | 1.229 | 20 | 200 | fits | 119,262 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 650,622 | 6.506 | 20 | 200 | fits | 149,706 | 90 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 123,763 | 1.238 | 20 | 20 | fits | 119,262 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 896,914 | 8.969 | 20 | 20 | fits | 121,157 | 46 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 127,348 | 1.273 | 20 | 24 | fits | 119,262 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,640,761 | 16.408 | 20 | 24 | fits | 67,939 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 126,308 | 1.263 | 20 | 50 | fits | 119,262 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 654,298 | 6.543 | 20 | 50 | fits | 149,706 | 90 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 504,527 | 5.045 | 18 | 18 | fits | 262,881 | 104 | 0.568 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,828,001 | 18.280 | 18 | 18 | MISS ceiling | 37,022 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 530,428 | 5.304 | 20 | 20 | fits | 155,998 | 89 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 129,605 | 1.296 | 20 | 200 | fits | 119,262 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 673,685 | 6.737 | 20 | 200 | fits | 155,998 | 89 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 130,517 | 1.305 | 20 | 20 | fits | 119,262 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 917,250 | 9.172 | 20 | 20 | fits | 120,975 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 134,102 | 1.341 | 20 | 24 | fits | 119,262 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,648,502 | 16.485 | 20 | 24 | fits | 67,904 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 133,062 | 1.331 | 20 | 50 | fits | 119,262 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 677,361 | 6.774 | 20 | 50 | fits | 155,998 | 89 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 403,129 | 4.031 | 18 | 18 | fits | 270,522 | 145 | 0.548 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,835,166 | 18.352 | 18 | 18 | MISS ceiling | 36,878 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 512,751 | 5.128 | 20 | 20 | fits | 143,793 | 60 | 0.682 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 175,071 | 1.751 | 20 | 200 | fits | 126,200 | 153 | 0.535 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 645,339 | 6.453 | 20 | 200 | fits | 143,793 | 60 | 0.682 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 175,983 | 1.760 | 20 | 20 | fits | 126,200 | 153 | 0.535 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 887,711 | 8.877 | 20 | 20 | fits | 120,610 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 53,368 | 0.534 | 20 | 24 | fits | 54,519 | 65 | 0.544 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,601,410 | 16.014 | 20 | 24 | fits | 67,612 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 52,328 | 0.523 | 20 | 50 | fits | 54,519 | 65 | 0.544 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 505,222 | 5.052 | 20 | 50 | fits | 137,522 | 76 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 367,635 | 3.676 | 18 | 18 | fits | 189,562 | 145 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,708,151 | 17.082 | 18 | 18 | fits | 57,556 | 29 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 461,443 | 4.614 | 20 | 20 | fits | 154,412 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 117,344 | 1.173 | 20 | 200 | fits | 119,815 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 604,741 | 6.047 | 20 | 200 | fits | 154,412 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 118,256 | 1.183 | 20 | 20 | fits | 119,815 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 911,153 | 9.112 | 20 | 20 | fits | 210,860 | 58 | 0.196 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 121,841 | 1.218 | 20 | 24 | fits | 119,815 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,605,166 | 16.052 | 20 | 24 | fits | 68,198 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 120,801 | 1.208 | 20 | 50 | fits | 119,815 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 608,417 | 6.084 | 20 | 50 | fits | 154,412 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 307,594 | 3.076 | 18 | 18 | fits | 187,248 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,715,512 | 17.155 | 18 | 18 | fits | 60,974 | 24 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 455,527 | 4.555 | 20 | 20 | fits | 244,655 | 95 | 0.226 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 130,852 | 1.309 | 20 | 200 | fits | 119,815 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 679,940 | 6.799 | 20 | 200 | fits | 244,655 | 95 | 0.226 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 131,764 | 1.318 | 20 | 20 | fits | 119,815 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 923,595 | 9.236 | 20 | 20 | fits | 121,008 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 135,349 | 1.353 | 20 | 24 | fits | 119,815 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,627,773 | 16.278 | 20 | 24 | fits | 67,703 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 134,309 | 1.343 | 20 | 50 | fits | 119,815 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 683,616 | 6.836 | 20 | 50 | fits | 244,655 | 95 | 0.226 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 321,102 | 3.211 | 18 | 18 | fits | 187,248 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,727,223 | 17.272 | 18 | 18 | fits | 50,409 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 529,859 | 5.299 | 20 | 20 | fits | 156,305 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 125,538 | 1.255 | 20 | 200 | fits | 119,815 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 674,292 | 6.743 | 20 | 200 | fits | 156,305 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 126,450 | 1.264 | 20 | 20 | fits | 119,815 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 917,067 | 9.171 | 20 | 20 | fits | 120,663 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 130,035 | 1.300 | 20 | 24 | fits | 119,815 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,621,279 | 16.213 | 20 | 24 | fits | 67,613 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 128,995 | 1.290 | 20 | 50 | fits | 119,815 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 677,968 | 6.780 | 20 | 50 | fits | 156,305 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 521,598 | 5.216 | 18 | 18 | fits | 183,047 | 104 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,720,729 | 17.207 | 18 | 18 | fits | 50,409 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 464,838 | 4.648 | 20 | 20 | fits | 154,277 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 121,152 | 1.212 | 20 | 200 | fits | 120,204 | 140 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 607,910 | 6.079 | 20 | 200 | fits | 154,277 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 122,064 | 1.221 | 20 | 20 | fits | 120,204 | 140 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 825,430 | 8.254 | 20 | 20 | fits | 122,166 | 52 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 125,649 | 1.256 | 20 | 24 | fits | 120,204 | 140 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,513,861 | 15.139 | 20 | 24 | fits | 61,959 | 38 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 124,609 | 1.246 | 20 | 50 | fits | 120,204 | 140 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 611,586 | 6.116 | 20 | 50 | fits | 154,277 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 311,015 | 3.110 | 18 | 18 | fits | 186,861 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,655,736 | 16.557 | 18 | 18 | fits | 37,022 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 470,290 | 4.703 | 20 | 20 | fits | 157,686 | 89 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 116,485 | 1.165 | 20 | 200 | fits | 119,772 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 613,697 | 6.137 | 20 | 200 | fits | 157,686 | 89 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 117,397 | 1.174 | 20 | 20 | fits | 119,772 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 834,524 | 8.345 | 20 | 20 | fits | 131,308 | 52 | 0.657 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 120,982 | 1.210 | 20 | 24 | fits | 119,772 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,528,242 | 15.282 | 20 | 24 | fits | 67,669 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 119,942 | 1.199 | 20 | 50 | fits | 119,772 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 617,373 | 6.174 | 20 | 50 | fits | 157,686 | 89 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 306,378 | 3.064 | 18 | 18 | fits | 186,891 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,628,160 | 16.282 | 18 | 18 | fits | 50,682 | 18 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 421,932 | 4.219 | 20 | 20 | fits | 186,317 | 89 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 129,993 | 1.300 | 20 | 200 | fits | 119,772 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 589,501 | 5.895 | 20 | 200 | fits | 186,317 | 89 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 130,905 | 1.309 | 20 | 20 | fits | 119,772 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 833,897 | 8.339 | 20 | 20 | fits | 120,860 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 134,490 | 1.345 | 20 | 24 | fits | 119,772 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,619,824 | 16.198 | 20 | 24 | fits | 69,506 | 31 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 133,450 | 1.335 | 20 | 50 | fits | 119,772 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 593,177 | 5.932 | 20 | 50 | fits | 186,317 | 89 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 406,795 | 4.068 | 18 | 18 | fits | 152,583 | 100 | 0.656 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,756,438 | 17.564 | 18 | 18 | fits | 36,968 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 470,833 | 4.708 | 20 | 20 | fits | 154,440 | 83 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 115,610 | 1.156 | 20 | 200 | fits | 120,158 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 614,088 | 6.141 | 20 | 200 | fits | 154,440 | 83 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 116,522 | 1.165 | 20 | 20 | fits | 120,158 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 868,870 | 8.689 | 20 | 20 | fits | 132,628 | 64 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 120,107 | 1.201 | 20 | 24 | fits | 120,158 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,636,417 | 16.364 | 20 | 24 | fits | 70,911 | 37 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 119,067 | 1.191 | 20 | 50 | fits | 120,158 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 617,764 | 6.178 | 20 | 50 | fits | 154,440 | 83 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 316,853 | 3.169 | 18 | 18 | fits | 198,241 | 145 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,722,394 | 17.224 | 18 | 18 | fits | 36,936 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 480,268 | 4.803 | 20 | 20 | fits | 154,641 | 83 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 125,964 | 1.260 | 20 | 200 | fits | 120,170 | 140 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 623,698 | 6.237 | 20 | 200 | fits | 154,641 | 83 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 126,876 | 1.269 | 20 | 20 | fits | 120,170 | 140 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 866,800 | 8.668 | 20 | 20 | fits | 120,845 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 130,461 | 1.305 | 20 | 24 | fits | 120,170 | 140 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,651,230 | 16.512 | 20 | 24 | fits | 67,613 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 129,421 | 1.294 | 20 | 50 | fits | 120,170 | 140 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 627,374 | 6.274 | 20 | 50 | fits | 154,641 | 83 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 323,794 | 3.238 | 18 | 18 | fits | 194,828 | 151 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,750,651 | 17.507 | 18 | 18 | fits | 50,409 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 448,193 | 4.482 | 20 | 20 | fits | 156,355 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 132,690 | 1.327 | 20 | 200 | fits | 119,954 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 592,741 | 5.927 | 20 | 200 | fits | 156,355 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 133,602 | 1.336 | 20 | 20 | fits | 119,954 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 802,717 | 8.027 | 20 | 20 | fits | 87,749 | 37 | 0.640 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 137,187 | 1.372 | 20 | 24 | fits | 119,954 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,567,993 | 15.680 | 20 | 24 | fits | 68,657 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 136,147 | 1.361 | 20 | 50 | fits | 119,954 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 596,417 | 5.964 | 20 | 50 | fits | 156,355 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 439,997 | 4.400 | 18 | 18 | fits | 182,971 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,900,164 | 19.002 | 18 | 18 | MISS ceiling | 131,783 | 39 | 0.553 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 474,105 | 4.741 | 20 | 20 | fits | 154,353 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 126,648 | 1.266 | 20 | 200 | fits | 125,888 | 151 | 0.542 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 617,318 | 6.173 | 20 | 200 | fits | 154,353 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 127,560 | 1.276 | 20 | 20 | fits | 125,888 | 151 | 0.542 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 909,888 | 9.099 | 20 | 20 | fits | 203,428 | 52 | 0.542 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 131,145 | 1.311 | 20 | 24 | fits | 125,888 | 151 | 0.542 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,639,020 | 16.390 | 20 | 24 | fits | 68,454 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 130,105 | 1.301 | 20 | 50 | fits | 125,888 | 151 | 0.542 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 620,994 | 6.210 | 20 | 50 | fits | 154,353 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 320,290 | 3.203 | 18 | 18 | fits | 190,640 | 145 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,858,536 | 18.585 | 18 | 18 | MISS ceiling | 38,030 | 15 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 461,545 | 4.615 | 20 | 20 | fits | 120,385 | 74 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 116,973 | 1.170 | 20 | 200 | fits | 119,781 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 570,790 | 5.708 | 20 | 200 | fits | 120,385 | 74 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 117,885 | 1.179 | 20 | 20 | fits | 119,781 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 908,367 | 9.084 | 20 | 20 | fits | 132,929 | 64 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 121,470 | 1.215 | 20 | 24 | fits | 119,781 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,715,421 | 17.154 | 20 | 24 | fits | 153,627 | 43 | 0.544 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 120,430 | 1.204 | 20 | 50 | fits | 119,781 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 574,466 | 5.745 | 20 | 50 | fits | 120,385 | 74 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 307,740 | 3.077 | 18 | 18 | fits | 187,765 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,815,594 | 18.156 | 18 | 18 | MISS ceiling | 50,400 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 441,319 | 4.413 | 20 | 20 | fits | 237,227 | 89 | 0.553 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 123,727 | 1.237 | 20 | 200 | fits | 119,781 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 660,008 | 6.600 | 20 | 200 | fits | 237,227 | 89 | 0.553 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 124,639 | 1.246 | 20 | 20 | fits | 119,781 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 915,913 | 9.159 | 20 | 20 | fits | 121,424 | 46 | 0.690 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 128,224 | 1.282 | 20 | 24 | fits | 119,781 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,723,668 | 17.237 | 20 | 24 | fits | 67,542 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 127,184 | 1.272 | 20 | 50 | fits | 119,781 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 663,684 | 6.637 | 20 | 50 | fits | 237,227 | 89 | 0.553 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 314,494 | 3.145 | 18 | 18 | fits | 187,765 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,823,167 | 18.232 | 18 | 18 | MISS ceiling | 50,487 | 18 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 569,661 | 5.697 | 20 | 20 | fits | 166,254 | 101 | 0.682 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 130,481 | 1.305 | 20 | 200 | fits | 119,781 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 713,511 | 7.135 | 20 | 200 | fits | 166,254 | 101 | 0.682 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 131,393 | 1.314 | 20 | 20 | fits | 119,781 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 957,104 | 9.571 | 20 | 20 | fits | 120,875 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 134,978 | 1.350 | 20 | 24 | fits | 119,781 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,699,996 | 17.000 | 20 | 24 | fits | 35,789 | 22 | 0.655 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 133,938 | 1.339 | 20 | 50 | fits | 119,781 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 717,187 | 7.172 | 20 | 50 | fits | 166,254 | 101 | 0.682 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 321,248 | 3.212 | 18 | 18 | fits | 187,765 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,833,481 | 18.335 | 18 | 18 | MISS ceiling | 50,924 | 18 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 487,165 | 4.872 | 20 | 20 | fits | 176,240 | 89 | 0.707 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 118,413 | 1.184 | 20 | 200 | fits | 119,781 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 650,026 | 6.500 | 20 | 200 | fits | 176,240 | 89 | 0.707 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 119,325 | 1.193 | 20 | 20 | fits | 119,781 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 894,336 | 8.943 | 20 | 20 | fits | 120,869 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 122,910 | 1.229 | 20 | 24 | fits | 119,781 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,671,578 | 16.716 | 20 | 24 | fits | 99,607 | 45 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 121,870 | 1.219 | 20 | 50 | fits | 119,781 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 653,702 | 6.537 | 20 | 50 | fits | 176,240 | 89 | 0.707 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 477,397 | 4.774 | 18 | 18 | fits | 240,801 | 111 | 0.570 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,858,482 | 18.585 | 18 | 18 | MISS ceiling | 36,878 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 524,729 | 5.247 | 20 | 20 | fits | 156,240 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 125,167 | 1.252 | 20 | 200 | fits | 119,781 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 669,162 | 6.692 | 20 | 200 | fits | 156,240 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 126,079 | 1.261 | 20 | 20 | fits | 119,781 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 911,776 | 9.118 | 20 | 20 | fits | 120,663 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 129,664 | 1.297 | 20 | 24 | fits | 119,781 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,721,010 | 17.210 | 20 | 24 | fits | 68,398 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 128,624 | 1.286 | 20 | 50 | fits | 119,781 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 672,838 | 6.728 | 20 | 50 | fits | 156,240 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 516,533 | 5.165 | 18 | 18 | fits | 183,694 | 104 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,820,797 | 18.208 | 18 | 18 | MISS ceiling | 50,631 | 18 | 0.723 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
