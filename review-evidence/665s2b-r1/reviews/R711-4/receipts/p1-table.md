### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 121 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-F57.adp_available.if0` (backlog-adp@blank-F57) | 5.580 (7.134) | fits | 7 adp | 11 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.960 | fits | 0 acmp | 11 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-F57.service.acmp.last.if0` (backlog-adp@blank-F57) | 9.463 | fits | 11 acmp | 11 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.951 | fits | 0 adp | 11 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-F57.service.adp.last.if0` (backlog-adp@blank-F57) | 7.023 | fits | 7 adp | 11 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.996 | fits | 0 aecp | 11 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@blank-F57.service.aecp.last.if1` (backlog-adp@blank-F57) | 16.275 | fits | 15 aecp | 11 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.986 | fits | 0 maap | 11 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-F57.service.maap.last.if0` (backlog-adp@blank-F57) | 7.059 | fits | 6 maap | 11 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-F48.service.srp.first.if0` (backlog-adp@blank-F48) | 4.205 | fits | 0 srp | 11 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-F54.service.srp.last.if1` (backlog-adp@blank-F54) | 17.365 | fits | 31 srp | 11 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.599 | 19 | 189,276 (1.893) | yes | - |
| backlog-adp@blank-F30 | 1 | 17.577 | 17 | 190,088 (1.901) | yes | - |
| backlog-adp@blank-F33 | 0 | 18.923 | 19 | 189,027 (1.890) | yes | - |
| backlog-adp@blank-F36 | 0 | 18.504 | 20 | 181,201 (1.812) | yes | - |
| backlog-adp@blank-F39 | 0 | 18.085 | 20 | 195,595 (1.956) | yes | - |
| backlog-adp@blank-F42 | 0 | 19.214 | 20 | 189,205 (1.892) | yes | - |
| backlog-adp@blank-F45 | 0 | 17.920 | 18 | 191,046 (1.910) | yes | - |
| backlog-adp@blank-F48 | 0 | 17.862 | 18 | 188,228 (1.882) | yes | - |
| backlog-adp@blank-F51 | 0 | 17.727 | 18 | 166,368 (1.664) | yes | - |
| backlog-adp@blank-F54 | 0 | 18.734 | 19 | 189,119 (1.891) | yes | - |
| backlog-adp@blank-F57 | 0 | 18.640 | 18 | 171,978 (1.720) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 480 | 0 | 189,276 (1.893) | fits |
| backlog-adp@blank-F30 | 622 | 0 | 190,088 (1.901) | fits |
| backlog-adp@blank-F33 | 635 | 0 | 189,027 (1.890) | fits |
| backlog-adp@blank-F36 | 651 | 0 | 181,201 (1.812) | fits |
| backlog-adp@blank-F39 | 665 | 0 | 195,595 (1.956) | fits |
| backlog-adp@blank-F42 | 680 | 0 | 189,205 (1.892) | fits |
| backlog-adp@blank-F45 | 693 | 0 | 191,046 (1.910) | fits |
| backlog-adp@blank-F48 | 708 | 0 | 188,228 (1.882) | fits |
| backlog-adp@blank-F51 | 722 | 0 | 166,368 (1.664) | fits |
| backlog-adp@blank-F54 | 738 | 0 | 189,119 (1.891) | fits |
| backlog-adp@blank-F57 | 752 | 0 | 171,978 (1.720) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-F30 | 338 | 102,374 (1.024) | 76,234 (0.762) |
| backlog-adp@blank-F33 | 339 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-F36 | 338 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-F39 | 338 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-F42 | 339 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-F45 | 338 | 102,374 (1.024) | 76,395 (0.764) |
| backlog-adp@blank-F48 | 338 | 102,374 (1.024) | 76,454 (0.765) |
| backlog-adp@blank-F51 | 338 | 102,374 (1.024) | 76,395 (0.764) |
| backlog-adp@blank-F54 | 339 | 102,374 (1.024) | 76,473 (0.765) |
| backlog-adp@blank-F57 | 339 | 102,374 (1.024) | 76,516 (0.765) |

Longest pass that carries a step: 102,374 CPU cycles (1.024 ms), backlog-adp@blank-0; longest step: 76,516 (0.765 ms), backlog-adp@blank-F57.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 541,888 | 5.419 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 195,101 | 1.951 | 20 | 200 | fits | 120,046 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 657,043 | 6.570 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 196,013 | 1.960 | 20 | 20 | fits | 120,046 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 902,111 | 9.021 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 199,598 | 1.996 | 20 | 24 | fits | 120,046 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,586,544 | 15.865 | 20 | 24 | fits | 67,834 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 198,558 | 1.986 | 20 | 50 | fits | 120,046 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 660,719 | 6.607 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 387,379 | 3.874 | 18 | 18 | fits | 189,276 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,723,372 | 17.234 | 18 | 18 | fits | 36,804 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F30.adp_available.if0` | 461,154 | 4.612 | 20 | 20 | fits | 154,714 | 83 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@blank-F30.service.adp.first.if0` | 113,555 | 1.136 | 20 | 200 | fits | 119,198 | 134 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-F30.service.adp.last.if0` | 604,555 | 6.046 | 20 | 200 | fits | 154,714 | 83 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F30.service.acmp.first.if0` | 114,467 | 1.145 | 20 | 20 | fits | 119,198 | 134 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F30.service.acmp.last.if0` | 822,583 | 8.226 | 20 | 20 | fits | 122,141 | 52 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-F30.service.aecp.first.if0` | 118,052 | 1.181 | 20 | 24 | fits | 119,198 | 134 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-F30.service.aecp.last.if1` | 1,516,130 | 15.161 | 20 | 24 | fits | 74,156 | 42 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F30.service.maap.first.if0` | 117,012 | 1.170 | 20 | 50 | fits | 119,198 | 134 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F30.service.maap.last.if0` | 608,231 | 6.082 | 20 | 50 | fits | 154,714 | 83 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@blank-F30.service.srp.first.if0` | 306,645 | 3.066 | 18 | 18 | fits | 190,088 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-F30.service.srp.last.if1` | 1,620,801 | 16.208 | 18 | 18 | fits | 50,507 | 18 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F33.adp_available.if0` | 484,942 | 4.849 | 20 | 20 | fits | 165,850 | 101 | 0.677 |
| ADP record released under the composed load, first | `backlog-adp@blank-F33.service.adp.first.if0` | 127,040 | 1.270 | 20 | 200 | fits | 118,665 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-F33.service.adp.last.if0` | 628,115 | 6.281 | 20 | 200 | fits | 165,850 | 101 | 0.677 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F33.service.acmp.first.if0` | 127,952 | 1.280 | 20 | 20 | fits | 118,665 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F33.service.acmp.last.if0` | 845,470 | 8.455 | 20 | 20 | fits | 127,518 | 52 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-F33.service.aecp.first.if0` | 131,537 | 1.315 | 20 | 24 | fits | 118,665 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-F33.service.aecp.last.if1` | 1,535,858 | 15.359 | 20 | 24 | fits | 67,434 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F33.service.maap.first.if0` | 130,497 | 1.305 | 20 | 50 | fits | 118,665 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F33.service.maap.last.if0` | 631,791 | 6.318 | 20 | 50 | fits | 165,850 | 101 | 0.677 |
| SRP record released under the composed load, first | `backlog-adp@blank-F33.service.srp.first.if0` | 319,069 | 3.191 | 18 | 18 | fits | 189,027 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-F33.service.srp.last.if1` | 1,635,753 | 16.358 | 18 | 18 | fits | 50,451 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F36.adp_available.if0` | 420,425 | 4.204 | 20 | 20 | fits | 181,201 | 89 | 0.707 |
| ADP record released under the composed load, first | `backlog-adp@blank-F36.service.adp.first.if0` | 127,385 | 1.274 | 20 | 200 | fits | 118,665 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-F36.service.adp.last.if0` | 582,890 | 5.829 | 20 | 200 | fits | 181,201 | 89 | 0.707 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F36.service.acmp.first.if0` | 128,297 | 1.283 | 20 | 20 | fits | 118,665 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F36.service.acmp.last.if0` | 827,090 | 8.271 | 20 | 20 | fits | 120,782 | 46 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@blank-F36.service.aecp.first.if0` | 131,882 | 1.319 | 20 | 24 | fits | 118,665 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-F36.service.aecp.last.if1` | 1,527,602 | 15.276 | 20 | 24 | fits | 67,979 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F36.service.maap.first.if0` | 130,842 | 1.308 | 20 | 50 | fits | 118,665 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F36.service.maap.last.if0` | 586,566 | 5.866 | 20 | 50 | fits | 181,201 | 89 | 0.707 |
| SRP record released under the composed load, first | `backlog-adp@blank-F36.service.srp.first.if0` | 405,300 | 4.053 | 18 | 18 | fits | 153,452 | 100 | 0.656 |
| SRP record released under the composed load, last | `backlog-adp@blank-F36.service.srp.last.if1` | 1,664,617 | 16.646 | 18 | 18 | fits | 36,745 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F39.adp_available.if0` | 470,108 | 4.701 | 20 | 20 | fits | 154,901 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@blank-F39.service.adp.first.if0` | 116,758 | 1.168 | 20 | 200 | fits | 118,660 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-F39.service.adp.last.if0` | 613,696 | 6.137 | 20 | 200 | fits | 154,901 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F39.service.acmp.first.if0` | 117,670 | 1.177 | 20 | 20 | fits | 118,660 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F39.service.acmp.last.if0` | 831,724 | 8.317 | 20 | 20 | fits | 122,141 | 52 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-F39.service.aecp.first.if0` | 121,255 | 1.213 | 20 | 24 | fits | 118,660 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-F39.service.aecp.last.if1` | 1,479,826 | 14.798 | 20 | 24 | fits | 61,420 | 38 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F39.service.maap.first.if0` | 120,215 | 1.202 | 20 | 50 | fits | 118,660 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F39.service.maap.last.if0` | 617,372 | 6.174 | 20 | 50 | fits | 154,901 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@blank-F39.service.srp.first.if0` | 315,355 | 3.154 | 18 | 18 | fits | 195,595 | 145 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-F39.service.srp.last.if1` | 1,672,004 | 16.720 | 18 | 18 | fits | 36,725 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F42.adp_available.if0` | 442,242 | 4.422 | 20 | 20 | fits | 155,674 | 89 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@blank-F42.service.adp.first.if0` | 122,918 | 1.229 | 20 | 200 | fits | 118,595 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-F42.service.adp.last.if0` | 585,166 | 5.852 | 20 | 200 | fits | 155,674 | 89 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F42.service.acmp.first.if0` | 123,830 | 1.238 | 20 | 20 | fits | 118,595 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F42.service.acmp.last.if0` | 796,254 | 7.963 | 20 | 20 | fits | 88,148 | 37 | 0.637 |
| AECP record released under the composed load, first | `backlog-adp@blank-F42.service.aecp.first.if0` | 127,415 | 1.274 | 20 | 24 | fits | 118,595 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-F42.service.aecp.last.if1` | 1,496,120 | 14.961 | 20 | 24 | fits | 67,415 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F42.service.maap.first.if0` | 126,375 | 1.264 | 20 | 50 | fits | 118,595 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F42.service.maap.last.if0` | 588,842 | 5.888 | 20 | 50 | fits | 155,674 | 89 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@blank-F42.service.srp.first.if0` | 315,125 | 3.151 | 18 | 18 | fits | 189,205 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-F42.service.srp.last.if1` | 1,646,312 | 16.463 | 18 | 18 | fits | 50,217 | 18 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F45.adp_available.if0` | 484,489 | 4.845 | 20 | 20 | fits | 161,357 | 89 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@blank-F45.service.adp.first.if0` | 129,082 | 1.291 | 20 | 200 | fits | 124,414 | 145 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@blank-F45.service.adp.last.if0` | 627,769 | 6.278 | 20 | 200 | fits | 161,357 | 89 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F45.service.acmp.first.if0` | 129,994 | 1.300 | 20 | 20 | fits | 124,414 | 145 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F45.service.acmp.last.if0` | 878,332 | 8.783 | 20 | 20 | fits | 127,782 | 57 | 0.693 |
| AECP record released under the composed load, first | `backlog-adp@blank-F45.service.aecp.first.if0` | 133,579 | 1.336 | 20 | 24 | fits | 124,414 | 145 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@blank-F45.service.aecp.last.if1` | 1,555,684 | 15.557 | 20 | 24 | fits | 75,217 | 37 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F45.service.maap.first.if0` | 132,539 | 1.325 | 20 | 50 | fits | 124,414 | 145 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F45.service.maap.last.if0` | 631,445 | 6.314 | 20 | 50 | fits | 161,357 | 89 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@blank-F45.service.srp.first.if0` | 323,130 | 3.231 | 18 | 18 | fits | 191,046 | 145 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-F45.service.srp.last.if1` | 1,731,040 | 17.310 | 18 | 18 | fits | 55,295 | 24 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F48.adp_available.if0` | 428,618 | 4.286 | 20 | 20 | fits | 162,964 | 94 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@blank-F48.service.adp.first.if0` | 112,591 | 1.126 | 20 | 200 | fits | 118,736 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-F48.service.adp.last.if0` | 579,814 | 5.798 | 20 | 200 | fits | 162,964 | 94 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F48.service.acmp.first.if0` | 113,503 | 1.135 | 20 | 20 | fits | 118,736 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F48.service.acmp.last.if0` | 826,840 | 8.268 | 20 | 20 | fits | 121,306 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@blank-F48.service.aecp.first.if0` | 117,088 | 1.171 | 20 | 24 | fits | 118,736 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-F48.service.aecp.last.if1` | 1,588,864 | 15.889 | 20 | 24 | fits | 67,859 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F48.service.maap.first.if0` | 116,048 | 1.160 | 20 | 50 | fits | 118,736 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F48.service.maap.last.if0` | 583,490 | 5.835 | 20 | 50 | fits | 162,964 | 94 | 0.681 |
| SRP record released under the composed load, first | `backlog-adp@blank-F48.service.srp.first.if0` | 420,461 | 4.205 | 18 | 18 | fits | 188,228 | 104 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp@blank-F48.service.srp.last.if1` | 1,725,745 | 17.257 | 18 | 18 | fits | 36,804 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F51.adp_available.if0` | 461,332 | 4.613 | 20 | 20 | fits | 155,348 | 83 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@blank-F51.service.adp.first.if0` | 118,672 | 1.187 | 20 | 200 | fits | 118,671 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-F51.service.adp.last.if0` | 605,420 | 6.054 | 20 | 200 | fits | 155,348 | 83 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F51.service.acmp.first.if0` | 119,584 | 1.196 | 20 | 20 | fits | 118,671 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F51.service.acmp.last.if0` | 849,217 | 8.492 | 20 | 20 | fits | 120,938 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@blank-F51.service.aecp.first.if0` | 123,169 | 1.232 | 20 | 24 | fits | 118,671 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-F51.service.aecp.last.if1` | 1,625,552 | 16.256 | 20 | 24 | fits | 67,705 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F51.service.maap.first.if0` | 122,129 | 1.221 | 20 | 50 | fits | 118,671 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F51.service.maap.last.if0` | 609,096 | 6.091 | 20 | 50 | fits | 155,348 | 83 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@blank-F51.service.srp.first.if0` | 287,315 | 2.873 | 18 | 18 | fits | 165,641 | 147 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-F51.service.srp.last.if1` | 1,712,177 | 17.122 | 18 | 18 | fits | 36,914 | 15 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F54.adp_available.if0` | 474,663 | 4.747 | 20 | 20 | fits | 120,514 | 74 | 0.622 |
| ADP record released under the composed load, first | `backlog-adp@blank-F54.service.adp.first.if0` | 127,789 | 1.278 | 20 | 200 | fits | 118,660 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-F54.service.adp.last.if0` | 583,864 | 5.839 | 20 | 200 | fits | 120,514 | 74 | 0.622 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F54.service.acmp.first.if0` | 128,701 | 1.287 | 20 | 20 | fits | 118,660 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F54.service.acmp.last.if0` | 922,723 | 9.227 | 20 | 20 | fits | 133,268 | 64 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@blank-F54.service.aecp.first.if0` | 132,286 | 1.323 | 20 | 24 | fits | 118,660 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-F54.service.aecp.last.if1` | 1,575,375 | 15.754 | 20 | 24 | fits | 41,694 | 33 | 0.676 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F54.service.maap.first.if0` | 131,246 | 1.312 | 20 | 50 | fits | 118,660 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F54.service.maap.last.if0` | 587,540 | 5.875 | 20 | 50 | fits | 120,514 | 74 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp@blank-F54.service.srp.first.if0` | 319,910 | 3.199 | 18 | 18 | fits | 189,119 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-F54.service.srp.last.if1` | 1,736,529 | 17.365 | 18 | 18 | fits | 50,155 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-F57.adp_available.if0` | 558,049 | 5.580 | 20 | 20 | fits | 167,002 | 101 | 0.683 |
| ADP record released under the composed load, first | `backlog-adp@blank-F57.service.adp.first.if0` | 128,134 | 1.281 | 20 | 200 | fits | 118,660 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-F57.service.adp.last.if0` | 702,267 | 7.023 | 20 | 200 | fits | 167,002 | 101 | 0.683 |
| ACMP record released under the composed load, first | `backlog-adp@blank-F57.service.acmp.first.if0` | 129,046 | 1.290 | 20 | 20 | fits | 118,660 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-F57.service.acmp.last.if0` | 946,335 | 9.463 | 20 | 20 | fits | 121,085 | 46 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@blank-F57.service.aecp.first.if0` | 132,631 | 1.326 | 20 | 24 | fits | 118,660 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-F57.service.aecp.last.if1` | 1,627,531 | 16.275 | 20 | 24 | fits | 67,251 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@blank-F57.service.maap.first.if0` | 131,591 | 1.316 | 20 | 50 | fits | 118,660 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-F57.service.maap.last.if0` | 705,943 | 7.059 | 20 | 50 | fits | 167,002 | 101 | 0.683 |
| SRP record released under the composed load, first | `backlog-adp@blank-F57.service.srp.first.if0` | 289,977 | 2.900 | 18 | 18 | fits | 158,841 | 136 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@blank-F57.service.srp.last.if1` | 1,727,110 | 17.271 | 18 | 18 | fits | 50,334 | 18 | 0.713 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
