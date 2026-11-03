### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 176 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-F59.adp_available.if0` (backlog-adp@verify-F59) | 5.542 (7.147) | fits | 7 adp | 16 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-F59.service.acmp.first.if0` (backlog-adp@verify-F59) | 2.084 | fits | 0 acmp | 16 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-F53.service.acmp.last.if0` (backlog-adp@verify-F53) | 9.297 | fits | 11 acmp | 16 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-F59.service.adp.first.if0` (backlog-adp@verify-F59) | 2.075 | fits | 0 adp | 16 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-F59.service.adp.last.if0` (backlog-adp@verify-F59) | 6.977 | fits | 7 adp | 16 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-F59.service.aecp.first.if0` (backlog-adp@verify-F59) | 2.120 | fits | 0 aecp | 16 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@verify-F49.service.aecp.last.if1` (backlog-adp@verify-F49) | 16.417 | fits | 15 aecp | 16 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-F59.service.maap.first.if0` (backlog-adp@verify-F59) | 2.109 | fits | 0 maap | 16 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-F59.service.maap.last.if0` (backlog-adp@verify-F59) | 7.013 | fits | 6 maap | 16 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-F47.service.srp.first.if0` (backlog-adp@program-F47) | 4.383 | fits | 0 srp | 16 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-F47.service.srp.last.if1` (backlog-adp@verify-F47) | 17.840 | fits | 31 srp | 16 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-F45 | 0 | 17.019 | 18 | 188,311 (1.883) | yes | - |
| backlog-adp@program-F47 | 0 | 17.008 | 18 | 189,475 (1.895) | yes | - |
| backlog-adp@program-F49 | 0 | 16.989 | 18 | 188,287 (1.883) | yes | - |
| backlog-adp@program-F51 | 0 | 17.214 | 19 | 188,287 (1.883) | yes | - |
| backlog-adp@program-F53 | 0 | 17.780 | 18 | 188,287 (1.883) | yes | - |
| backlog-adp@program-F55 | 0 | 18.545 | 20 | 181,263 (1.813) | yes | - |
| backlog-adp@program-F57 | 0 | 18.275 | 20 | 187,414 (1.874) | yes | - |
| backlog-adp@program-F59 | 0 | 17.773 | 18 | 188,486 (1.885) | yes | - |
| backlog-adp@verify-F45 | 0 | 18.297 | 19 | 188,866 (1.889) | yes | - |
| backlog-adp@verify-F47 | 0 | 18.444 | 20 | 175,718 (1.757) | yes | - |
| backlog-adp@verify-F49 | 0 | 18.691 | 20 | 183,766 (1.838) | yes | - |
| backlog-adp@verify-F51 | 0 | 19.366 | 20 | 188,860 (1.889) | yes | - |
| backlog-adp@verify-F53 | 0 | 19.094 | 19 | 188,860 (1.889) | yes | - |
| backlog-adp@verify-F55 | 0 | 19.016 | 19 | 188,860 (1.889) | yes | - |
| backlog-adp@verify-F57 | 0 | 19.789 | 20 | 190,408 (1.904) | yes | - |
| backlog-adp@verify-F59 | 0 | 18.519 | 18 | 189,162 (1.892) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@program-F45 | 979 | 0 | 188,311 (1.883) | fits |
| backlog-adp@program-F47 | 989 | 0 | 189,475 (1.895) | fits |
| backlog-adp@program-F49 | 998 | 0 | 188,287 (1.883) | fits |
| backlog-adp@program-F51 | 1009 | 0 | 188,287 (1.883) | fits |
| backlog-adp@program-F53 | 1018 | 0 | 188,287 (1.883) | fits |
| backlog-adp@program-F55 | 1030 | 0 | 181,263 (1.813) | fits |
| backlog-adp@program-F57 | 1040 | 0 | 187,414 (1.874) | fits |
| backlog-adp@program-F59 | 1047 | 0 | 188,486 (1.885) | fits |
| backlog-adp@verify-F45 | 1262 | 0 | 188,866 (1.889) | fits |
| backlog-adp@verify-F47 | 1273 | 0 | 175,718 (1.757) | fits |
| backlog-adp@verify-F49 | 1283 | 0 | 183,766 (1.838) | fits |
| backlog-adp@verify-F51 | 1292 | 0 | 188,860 (1.889) | fits |
| backlog-adp@verify-F53 | 1301 | 0 | 188,860 (1.889) | fits |
| backlog-adp@verify-F55 | 1311 | 0 | 188,860 (1.889) | fits |
| backlog-adp@verify-F57 | 1322 | 0 | 190,408 (1.904) | fits |
| backlog-adp@verify-F59 | 1330 | 0 | 189,162 (1.892) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@program-F45 | 444 | 122,002 (1.220) | 82,162 (0.822) |
| backlog-adp@program-F47 | 444 | 122,002 (1.220) | 82,162 (0.822) |
| backlog-adp@program-F49 | 444 | 122,002 (1.220) | 82,162 (0.822) |
| backlog-adp@program-F51 | 444 | 122,002 (1.220) | 82,162 (0.822) |
| backlog-adp@program-F53 | 445 | 122,002 (1.220) | 82,353 (0.824) |
| backlog-adp@program-F55 | 445 | 122,002 (1.220) | 82,237 (0.822) |
| backlog-adp@program-F57 | 445 | 122,002 (1.220) | 82,172 (0.822) |
| backlog-adp@program-F59 | 445 | 122,002 (1.220) | 82,237 (0.822) |
| backlog-adp@verify-F45 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-F47 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-F49 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-F51 | 548 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-F53 | 548 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-F55 | 548 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-F57 | 548 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-F59 | 548 | 122,002 (1.220) | 96,031 (0.960) |

Longest pass that carries a step: 122,002 CPU cycles (1.220 ms), backlog-adp@program-F45; longest step: 96,031 (0.960 ms), backlog-adp@verify-F45.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-F45.adp_available.if0` | 449,618 | 4.496 | 20 | 20 | fits | 162,739 | 95 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@program-F45.service.adp.first.if0` | 124,048 | 1.240 | 20 | 200 | fits | 118,909 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-F45.service.adp.last.if0` | 592,467 | 5.925 | 20 | 200 | fits | 162,739 | 95 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@program-F45.service.acmp.first.if0` | 124,960 | 1.250 | 20 | 20 | fits | 118,909 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-F45.service.acmp.last.if0` | 836,491 | 8.365 | 20 | 20 | fits | 121,084 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-F45.service.aecp.first.if0` | 128,545 | 1.285 | 20 | 24 | fits | 118,909 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-F45.service.aecp.last.if1` | 1,541,298 | 15.413 | 20 | 24 | fits | 68,726 | 31 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp@program-F45.service.maap.first.if0` | 127,505 | 1.275 | 20 | 50 | fits | 118,909 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-F45.service.maap.last.if0` | 596,143 | 5.961 | 20 | 50 | fits | 162,739 | 95 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@program-F45.service.srp.first.if0` | 315,361 | 3.154 | 18 | 18 | fits | 188,311 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-F45.service.srp.last.if1` | 1,641,158 | 16.412 | 18 | 18 | fits | 50,387 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-F47.adp_available.if0` | 446,397 | 4.464 | 20 | 20 | fits | 156,319 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@program-F47.service.adp.first.if0` | 124,278 | 1.243 | 20 | 200 | fits | 118,909 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-F47.service.adp.last.if0` | 591,010 | 5.910 | 20 | 200 | fits | 156,319 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@program-F47.service.acmp.first.if0` | 125,190 | 1.252 | 20 | 20 | fits | 118,909 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-F47.service.acmp.last.if0` | 835,012 | 8.350 | 20 | 20 | fits | 121,026 | 46 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@program-F47.service.aecp.first.if0` | 128,775 | 1.288 | 20 | 24 | fits | 118,909 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-F47.service.aecp.last.if1` | 1,540,202 | 15.402 | 20 | 24 | fits | 67,444 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@program-F47.service.maap.first.if0` | 127,735 | 1.277 | 20 | 50 | fits | 118,909 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-F47.service.maap.last.if0` | 594,686 | 5.947 | 20 | 50 | fits | 156,319 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@program-F47.service.srp.first.if0` | 438,302 | 4.383 | 18 | 18 | fits | 189,475 | 110 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp@program-F47.service.srp.last.if1` | 1,640,022 | 16.400 | 18 | 18 | fits | 50,387 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-F49.adp_available.if0` | 465,296 | 4.653 | 20 | 20 | fits | 154,947 | 83 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@program-F49.service.adp.first.if0` | 119,311 | 1.193 | 20 | 200 | fits | 119,128 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-F49.service.adp.last.if0` | 608,930 | 6.089 | 20 | 200 | fits | 154,947 | 83 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@program-F49.service.acmp.first.if0` | 120,223 | 1.202 | 20 | 20 | fits | 119,128 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-F49.service.acmp.last.if0` | 826,190 | 8.262 | 20 | 20 | fits | 94,245 | 48 | 0.655 |
| AECP record released under the composed load, first | `backlog-adp@program-F49.service.aecp.first.if0` | 123,808 | 1.238 | 20 | 24 | fits | 119,128 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-F49.service.aecp.last.if1` | 1,524,564 | 15.246 | 20 | 24 | fits | 67,587 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@program-F49.service.maap.first.if0` | 122,768 | 1.228 | 20 | 50 | fits | 119,128 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-F49.service.maap.last.if0` | 612,606 | 6.126 | 20 | 50 | fits | 154,947 | 83 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@program-F49.service.srp.first.if0` | 310,600 | 3.106 | 18 | 18 | fits | 188,287 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-F49.service.srp.last.if1` | 1,637,944 | 16.379 | 18 | 18 | fits | 64,198 | 36 | 0.782 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-F51.adp_available.if0` | 465,526 | 4.655 | 20 | 20 | fits | 147,530 | 90 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@program-F51.service.adp.first.if0` | 119,541 | 1.195 | 20 | 200 | fits | 119,128 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-F51.service.adp.last.if0` | 601,743 | 6.017 | 20 | 200 | fits | 147,530 | 90 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@program-F51.service.acmp.first.if0` | 120,453 | 1.205 | 20 | 20 | fits | 119,128 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-F51.service.acmp.last.if0` | 814,672 | 8.147 | 20 | 20 | fits | 88,069 | 37 | 0.640 |
| AECP record released under the composed load, first | `backlog-adp@program-F51.service.aecp.first.if0` | 124,038 | 1.240 | 20 | 24 | fits | 119,128 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-F51.service.aecp.last.if1` | 1,523,931 | 15.239 | 20 | 24 | fits | 68,059 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-F51.service.maap.first.if0` | 122,998 | 1.230 | 20 | 50 | fits | 119,128 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-F51.service.maap.last.if0` | 605,419 | 6.054 | 20 | 50 | fits | 147,530 | 90 | 0.681 |
| SRP record released under the composed load, first | `backlog-adp@program-F51.service.srp.first.if0` | 310,830 | 3.108 | 18 | 18 | fits | 188,287 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-F51.service.srp.last.if1` | 1,660,944 | 16.609 | 18 | 18 | fits | 36,791 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-F53.adp_available.if0` | 438,120 | 4.381 | 20 | 20 | fits | 155,720 | 89 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@program-F53.service.adp.first.if0` | 119,771 | 1.198 | 20 | 200 | fits | 119,128 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-F53.service.adp.last.if0` | 581,090 | 5.811 | 20 | 200 | fits | 155,720 | 89 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@program-F53.service.acmp.first.if0` | 120,683 | 1.207 | 20 | 20 | fits | 119,128 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-F53.service.acmp.last.if0` | 837,807 | 8.378 | 20 | 20 | fits | 121,350 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-F53.service.aecp.first.if0` | 124,268 | 1.243 | 20 | 24 | fits | 119,128 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-F53.service.aecp.last.if1` | 1,528,418 | 15.284 | 20 | 24 | fits | 67,444 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@program-F53.service.maap.first.if0` | 123,228 | 1.232 | 20 | 50 | fits | 119,128 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-F53.service.maap.last.if0` | 584,766 | 5.848 | 20 | 50 | fits | 155,720 | 89 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@program-F53.service.srp.first.if0` | 311,060 | 3.111 | 18 | 18 | fits | 188,287 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-F53.service.srp.last.if1` | 1,634,607 | 16.346 | 18 | 18 | fits | 56,756 | 24 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-F55.adp_available.if0` | 412,283 | 4.123 | 20 | 20 | fits | 181,263 | 89 | 0.707 |
| ADP record released under the composed load, first | `backlog-adp@program-F55.service.adp.first.if0` | 120,001 | 1.200 | 20 | 200 | fits | 119,128 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-F55.service.adp.last.if0` | 574,867 | 5.749 | 20 | 200 | fits | 181,263 | 89 | 0.707 |
| ACMP record released under the composed load, first | `backlog-adp@program-F55.service.acmp.first.if0` | 120,913 | 1.209 | 20 | 20 | fits | 119,128 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-F55.service.acmp.last.if0` | 825,073 | 8.251 | 20 | 20 | fits | 120,971 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@program-F55.service.aecp.first.if0` | 124,498 | 1.245 | 20 | 24 | fits | 119,128 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-F55.service.aecp.last.if1` | 1,525,633 | 15.256 | 20 | 24 | fits | 67,979 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-F55.service.maap.first.if0` | 123,458 | 1.235 | 20 | 50 | fits | 119,128 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-F55.service.maap.last.if0` | 578,543 | 5.785 | 20 | 50 | fits | 181,263 | 89 | 0.707 |
| SRP record released under the composed load, first | `backlog-adp@program-F55.service.srp.first.if0` | 397,215 | 3.972 | 18 | 18 | fits | 152,689 | 100 | 0.657 |
| SRP record released under the composed load, last | `backlog-adp@program-F55.service.srp.last.if1` | 1,662,648 | 16.626 | 18 | 18 | fits | 36,745 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-F57.adp_available.if0` | 448,757 | 4.488 | 20 | 20 | fits | 156,275 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@program-F57.service.adp.first.if0` | 129,149 | 1.291 | 20 | 200 | fits | 119,052 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-F57.service.adp.last.if0` | 593,764 | 5.938 | 20 | 200 | fits | 156,275 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@program-F57.service.acmp.first.if0` | 130,061 | 1.301 | 20 | 20 | fits | 119,052 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-F57.service.acmp.last.if0` | 810,859 | 8.109 | 20 | 20 | fits | 94,166 | 48 | 0.653 |
| AECP record released under the composed load, first | `backlog-adp@program-F57.service.aecp.first.if0` | 133,646 | 1.336 | 20 | 24 | fits | 119,052 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-F57.service.aecp.last.if1` | 1,470,169 | 14.702 | 20 | 24 | fits | 67,580 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@program-F57.service.maap.first.if0` | 132,606 | 1.326 | 20 | 50 | fits | 119,052 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-F57.service.maap.last.if0` | 597,440 | 5.974 | 20 | 50 | fits | 156,275 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@program-F57.service.srp.first.if0` | 435,395 | 4.354 | 18 | 18 | fits | 187,414 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@program-F57.service.srp.last.if1` | 1,684,344 | 16.843 | 18 | 18 | fits | 50,343 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-F59.adp_available.if0` | 466,405 | 4.664 | 20 | 20 | fits | 147,343 | 90 | 0.680 |
| ADP record released under the composed load, first | `backlog-adp@program-F59.service.adp.first.if0` | 120,311 | 1.203 | 20 | 200 | fits | 119,503 | 134 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@program-F59.service.adp.last.if0` | 602,435 | 6.024 | 20 | 200 | fits | 147,343 | 90 | 0.680 |
| ACMP record released under the composed load, first | `backlog-adp@program-F59.service.acmp.first.if0` | 121,223 | 1.212 | 20 | 20 | fits | 119,503 | 134 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@program-F59.service.acmp.last.if0` | 848,662 | 8.487 | 20 | 20 | fits | 121,367 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-F59.service.aecp.first.if0` | 124,808 | 1.248 | 20 | 24 | fits | 119,503 | 134 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@program-F59.service.aecp.last.if1` | 1,548,202 | 15.482 | 20 | 24 | fits | 67,987 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-F59.service.maap.first.if0` | 123,768 | 1.238 | 20 | 50 | fits | 119,503 | 134 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@program-F59.service.maap.last.if0` | 606,111 | 6.061 | 20 | 50 | fits | 147,343 | 90 | 0.680 |
| SRP record released under the composed load, first | `backlog-adp@program-F59.service.srp.first.if0` | 311,799 | 3.118 | 18 | 18 | fits | 188,486 | 140 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@program-F59.service.srp.last.if1` | 1,634,428 | 16.344 | 18 | 18 | fits | 36,811 | 15 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-F45.adp_available.if0` | 438,857 | 4.389 | 20 | 20 | fits | 160,651 | 89 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@verify-F45.service.adp.first.if0` | 120,324 | 1.203 | 20 | 200 | fits | 118,808 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-F45.service.adp.last.if0` | 581,244 | 5.812 | 20 | 200 | fits | 160,651 | 89 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@verify-F45.service.acmp.first.if0` | 121,236 | 1.212 | 20 | 20 | fits | 118,808 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-F45.service.acmp.last.if0` | 836,569 | 8.366 | 20 | 20 | fits | 121,339 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-F45.service.aecp.first.if0` | 124,821 | 1.248 | 20 | 24 | fits | 118,808 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-F45.service.aecp.last.if1` | 1,632,379 | 16.324 | 20 | 24 | fits | 68,720 | 31 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp@verify-F45.service.maap.first.if0` | 123,781 | 1.238 | 20 | 50 | fits | 118,808 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-F45.service.maap.last.if0` | 584,920 | 5.849 | 20 | 50 | fits | 160,651 | 89 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@verify-F45.service.srp.first.if0` | 312,192 | 3.122 | 18 | 18 | fits | 188,866 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@verify-F45.service.srp.last.if1` | 1,769,248 | 17.692 | 18 | 18 | fits | 36,745 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-F47.adp_available.if0` | 414,107 | 4.141 | 20 | 20 | fits | 175,718 | 89 | 0.704 |
| ADP record released under the composed load, first | `backlog-adp@verify-F47.service.adp.first.if0` | 120,554 | 1.206 | 20 | 200 | fits | 118,808 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-F47.service.adp.last.if0` | 575,953 | 5.760 | 20 | 200 | fits | 175,718 | 89 | 0.704 |
| ACMP record released under the composed load, first | `backlog-adp@verify-F47.service.acmp.first.if0` | 121,466 | 1.215 | 20 | 20 | fits | 118,808 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-F47.service.acmp.last.if0` | 820,498 | 8.205 | 20 | 20 | fits | 120,916 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@verify-F47.service.aecp.first.if0` | 125,051 | 1.251 | 20 | 24 | fits | 118,808 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-F47.service.aecp.last.if1` | 1,596,630 | 15.966 | 20 | 24 | fits | 67,691 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@verify-F47.service.maap.first.if0` | 124,011 | 1.240 | 20 | 50 | fits | 118,808 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-F47.service.maap.last.if0` | 579,629 | 5.796 | 20 | 50 | fits | 175,718 | 89 | 0.704 |
| SRP record released under the composed load, first | `backlog-adp@verify-F47.service.srp.first.if0` | 403,846 | 4.038 | 18 | 18 | fits | 164,688 | 111 | 0.665 |
| SRP record released under the composed load, last | `backlog-adp@verify-F47.service.srp.last.if1` | 1,783,962 | 17.840 | 18 | 18 | fits | 36,682 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-F49.adp_available.if0` | 442,809 | 4.428 | 20 | 20 | fits | 156,453 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-F49.service.adp.first.if0` | 126,743 | 1.267 | 20 | 200 | fits | 118,743 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-F49.service.adp.last.if0` | 587,556 | 5.876 | 20 | 200 | fits | 156,453 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-F49.service.acmp.first.if0` | 127,655 | 1.277 | 20 | 20 | fits | 118,743 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-F49.service.acmp.last.if0` | 831,709 | 8.317 | 20 | 20 | fits | 121,100 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-F49.service.aecp.first.if0` | 131,240 | 1.312 | 20 | 24 | fits | 118,743 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-F49.service.aecp.last.if1` | 1,641,671 | 16.417 | 20 | 24 | fits | 67,441 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@verify-F49.service.maap.first.if0` | 130,200 | 1.302 | 20 | 50 | fits | 118,743 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-F49.service.maap.last.if0` | 591,232 | 5.912 | 20 | 50 | fits | 156,453 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@verify-F49.service.srp.first.if0` | 434,714 | 4.347 | 18 | 18 | fits | 183,766 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@verify-F49.service.srp.last.if1` | 1,741,438 | 17.414 | 18 | 18 | fits | 50,387 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-F51.adp_available.if0` | 462,501 | 4.625 | 20 | 20 | fits | 154,870 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-F51.service.adp.first.if0` | 116,020 | 1.160 | 20 | 200 | fits | 118,884 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-F51.service.adp.last.if0` | 606,058 | 6.061 | 20 | 200 | fits | 154,870 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-F51.service.acmp.first.if0` | 116,932 | 1.169 | 20 | 20 | fits | 118,884 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-F51.service.acmp.last.if0` | 823,167 | 8.232 | 20 | 20 | fits | 94,171 | 48 | 0.654 |
| AECP record released under the composed load, first | `backlog-adp@verify-F51.service.aecp.first.if0` | 120,517 | 1.205 | 20 | 24 | fits | 118,884 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-F51.service.aecp.last.if1` | 1,599,534 | 15.995 | 20 | 24 | fits | 73,872 | 42 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-F51.service.maap.first.if0` | 119,477 | 1.195 | 20 | 50 | fits | 118,884 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-F51.service.maap.last.if0` | 609,734 | 6.097 | 20 | 50 | fits | 154,870 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-F51.service.srp.first.if0` | 307,882 | 3.079 | 18 | 18 | fits | 188,860 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-F51.service.srp.last.if1` | 1,754,726 | 17.547 | 18 | 18 | fits | 50,156 | 18 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-F53.adp_available.if0` | 462,731 | 4.627 | 20 | 20 | fits | 147,453 | 90 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@verify-F53.service.adp.first.if0` | 116,250 | 1.163 | 20 | 200 | fits | 118,884 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-F53.service.adp.last.if0` | 598,871 | 5.989 | 20 | 200 | fits | 147,453 | 90 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@verify-F53.service.acmp.first.if0` | 117,162 | 1.172 | 20 | 20 | fits | 118,884 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-F53.service.acmp.last.if0` | 929,658 | 9.297 | 20 | 20 | fits | 121,487 | 46 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-F53.service.aecp.first.if0` | 120,747 | 1.207 | 20 | 24 | fits | 118,884 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-F53.service.aecp.last.if1` | 1,593,269 | 15.933 | 20 | 24 | fits | 54,783 | 27 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@verify-F53.service.maap.first.if0` | 119,707 | 1.197 | 20 | 50 | fits | 118,884 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-F53.service.maap.last.if0` | 602,547 | 6.025 | 20 | 50 | fits | 147,453 | 90 | 0.681 |
| SRP record released under the composed load, first | `backlog-adp@verify-F53.service.srp.first.if0` | 308,112 | 3.081 | 18 | 18 | fits | 188,860 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-F53.service.srp.last.if1` | 1,771,240 | 17.712 | 18 | 18 | fits | 84,182 | 32 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-F55.adp_available.if0` | 442,465 | 4.425 | 20 | 20 | fits | 162,816 | 95 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@verify-F55.service.adp.first.if0` | 116,480 | 1.165 | 20 | 200 | fits | 118,884 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-F55.service.adp.last.if0` | 585,391 | 5.854 | 20 | 200 | fits | 162,816 | 95 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@verify-F55.service.acmp.first.if0` | 117,392 | 1.174 | 20 | 20 | fits | 118,884 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-F55.service.acmp.last.if0` | 907,262 | 9.073 | 20 | 20 | fits | 121,100 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-F55.service.aecp.first.if0` | 120,977 | 1.210 | 20 | 24 | fits | 118,884 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-F55.service.aecp.last.if1` | 1,605,520 | 16.055 | 20 | 24 | fits | 67,363 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@verify-F55.service.maap.first.if0` | 119,937 | 1.199 | 20 | 50 | fits | 118,884 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-F55.service.maap.last.if0` | 589,067 | 5.891 | 20 | 50 | fits | 162,816 | 95 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@verify-F55.service.srp.first.if0` | 308,342 | 3.083 | 18 | 18 | fits | 188,860 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-F55.service.srp.last.if1` | 1,763,659 | 17.637 | 18 | 18 | fits | 70,697 | 29 | 0.813 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-F57.adp_available.if0` | 516,864 | 5.169 | 20 | 20 | fits | 156,166 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-F57.service.adp.first.if0` | 116,710 | 1.167 | 20 | 200 | fits | 118,884 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-F57.service.adp.last.if0` | 661,670 | 6.617 | 20 | 200 | fits | 156,166 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-F57.service.acmp.first.if0` | 117,622 | 1.176 | 20 | 20 | fits | 118,884 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-F57.service.acmp.last.if0` | 905,948 | 9.059 | 20 | 20 | fits | 121,158 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-F57.service.aecp.first.if0` | 121,207 | 1.212 | 20 | 24 | fits | 118,884 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-F57.service.aecp.last.if1` | 1,604,303 | 16.043 | 20 | 24 | fits | 67,363 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@verify-F57.service.maap.first.if0` | 120,167 | 1.202 | 20 | 50 | fits | 118,884 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-F57.service.maap.last.if0` | 665,346 | 6.653 | 20 | 50 | fits | 156,166 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@verify-F57.service.srp.first.if0` | 431,317 | 4.313 | 18 | 18 | fits | 190,408 | 110 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp@verify-F57.service.srp.last.if1` | 1,704,070 | 17.041 | 18 | 18 | fits | 50,387 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-F59.adp_available.if0` | 554,221 | 5.542 | 20 | 20 | fits | 154,760 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-F59.service.adp.first.if0` | 207,491 | 2.075 | 20 | 200 | fits | 119,197 | 134 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-F59.service.adp.last.if0` | 697,668 | 6.977 | 20 | 200 | fits | 154,760 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-F59.service.acmp.first.if0` | 208,403 | 2.084 | 20 | 20 | fits | 119,197 | 134 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-F59.service.acmp.last.if0` | 915,696 | 9.157 | 20 | 20 | fits | 122,141 | 52 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-F59.service.aecp.first.if0` | 211,988 | 2.120 | 20 | 24 | fits | 119,197 | 134 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-F59.service.aecp.last.if1` | 1,609,243 | 16.092 | 20 | 24 | fits | 74,156 | 42 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@verify-F59.service.maap.first.if0` | 210,948 | 2.109 | 20 | 50 | fits | 119,197 | 134 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-F59.service.maap.last.if0` | 701,344 | 7.013 | 20 | 50 | fits | 154,760 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-F59.service.srp.first.if0` | 399,655 | 3.997 | 18 | 18 | fits | 189,162 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@verify-F59.service.srp.last.if1` | 1,713,914 | 17.139 | 18 | 18 | fits | 50,507 | 18 | 0.723 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
