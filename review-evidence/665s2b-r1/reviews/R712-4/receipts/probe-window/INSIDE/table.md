### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 88 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 5.419 (7.509) | fits | 7 adp | 8 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.960 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 9.021 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.951 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.570 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.996 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@blank-c2.service.aecp.last.if1` (backlog-adp@blank-c2) | 15.989 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.986 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.607 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.srp.first.if0` (backlog-adp@blank-0) | 3.874 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-c2.service.srp.last.if1` (backlog-adp@blank-c2) | 17.357 | fits | 31 srp | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.599 | 19 | 189,276 (1.893) | yes | - |
| backlog-adp@blank-c0 | 0 | 17.905 | 19 | 188,950 (1.889) | yes | - |
| backlog-adp@blank-c1 | 0 | 17.934 | 19 | 188,950 (1.889) | yes | - |
| backlog-adp@blank-c2 | 0 | 17.962 | 19 | 189,036 (1.890) | yes | - |
| backlog-adp@blank-c3 | 0 | 17.981 | 19 | 188,987 (1.890) | yes | - |
| backlog-adp@blank-c4 | 1 | 17.539 | 17 | 189,984 (1.900) | yes | - |
| backlog-adp@blank-c5 | 1 | 17.540 | 17 | 190,042 (1.900) | yes | - |
| backlog-adp@blank-c6 | 0 | 17.578 | 18 | 189,051 (1.891) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 480 | 0 | 189,276 (1.893) | fits |
| backlog-adp@blank-c0 | 536 | 0 | 188,950 (1.889) | fits |
| backlog-adp@blank-c1 | 551 | 0 | 188,950 (1.889) | fits |
| backlog-adp@blank-c2 | 566 | 0 | 189,036 (1.890) | fits |
| backlog-adp@blank-c3 | 578 | 0 | 188,987 (1.890) | fits |
| backlog-adp@blank-c4 | 591 | 0 | 189,984 (1.900) | fits |
| backlog-adp@blank-c5 | 604 | 0 | 190,042 (1.900) | fits |
| backlog-adp@blank-c6 | 620 | 0 | 189,051 (1.891) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-c0 | 335 | 102,374 (1.024) | 76,455 (0.765) |
| backlog-adp@blank-c1 | 335 | 102,374 (1.024) | 76,455 (0.765) |
| backlog-adp@blank-c2 | 335 | 102,374 (1.024) | 76,455 (0.765) |
| backlog-adp@blank-c3 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-c4 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-c5 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-c6 | 335 | 102,374 (1.024) | 76,232 (0.762) |

Longest pass that carries a step: 102,374 CPU cycles (1.024 ms), backlog-adp@blank-0; longest step: 76,455 (0.765 ms), backlog-adp@blank-c0.

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
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c0.adp_available.if0` | 470,698 | 4.707 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-c0.service.adp.first.if0` | 124,127 | 1.241 | 20 | 200 | fits | 118,677 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-c0.service.adp.last.if0` | 585,776 | 5.858 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c0.service.acmp.first.if0` | 125,039 | 1.250 | 20 | 20 | fits | 118,677 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c0.service.acmp.last.if0` | 830,995 | 8.310 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c0.service.aecp.first.if0` | 128,624 | 1.286 | 20 | 24 | fits | 118,677 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-c0.service.aecp.last.if1` | 1,593,192 | 15.932 | 20 | 24 | fits | 67,800 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c0.service.maap.first.if0` | 127,584 | 1.276 | 20 | 50 | fits | 118,677 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c0.service.maap.last.if0` | 589,452 | 5.895 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-c0.service.srp.first.if0` | 316,079 | 3.161 | 18 | 18 | fits | 188,950 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-c0.service.srp.last.if1` | 1,730,020 | 17.300 | 18 | 18 | fits | 36,804 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c1.adp_available.if0` | 473,582 | 4.736 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-c1.service.adp.first.if0` | 127,011 | 1.270 | 20 | 200 | fits | 118,677 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-c1.service.adp.last.if0` | 588,660 | 5.887 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c1.service.acmp.first.if0` | 127,923 | 1.279 | 20 | 20 | fits | 118,677 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c1.service.acmp.last.if0` | 833,879 | 8.339 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c1.service.aecp.first.if0` | 131,508 | 1.315 | 20 | 24 | fits | 118,677 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-c1.service.aecp.last.if1` | 1,596,076 | 15.961 | 20 | 24 | fits | 67,800 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c1.service.maap.first.if0` | 130,468 | 1.305 | 20 | 50 | fits | 118,677 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c1.service.maap.last.if0` | 592,336 | 5.923 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-c1.service.srp.first.if0` | 318,963 | 3.190 | 18 | 18 | fits | 188,950 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-c1.service.srp.last.if1` | 1,732,904 | 17.329 | 18 | 18 | fits | 36,804 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c2.adp_available.if0` | 476,362 | 4.764 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-c2.service.adp.first.if0` | 129,705 | 1.297 | 20 | 200 | fits | 118,677 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-c2.service.adp.last.if0` | 591,440 | 5.914 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c2.service.acmp.first.if0` | 130,617 | 1.306 | 20 | 20 | fits | 118,677 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c2.service.acmp.last.if0` | 836,659 | 8.367 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c2.service.aecp.first.if0` | 134,202 | 1.342 | 20 | 24 | fits | 118,677 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-c2.service.aecp.last.if1` | 1,598,856 | 15.989 | 20 | 24 | fits | 67,800 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c2.service.maap.first.if0` | 133,162 | 1.332 | 20 | 50 | fits | 118,677 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c2.service.maap.last.if0` | 595,116 | 5.951 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-c2.service.srp.first.if0` | 321,743 | 3.217 | 18 | 18 | fits | 189,036 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-c2.service.srp.last.if1` | 1,735,684 | 17.357 | 18 | 18 | fits | 36,804 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c3.adp_available.if0` | 506,217 | 5.062 | 20 | 20 | fits | 116,426 | 62 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@blank-c3.service.adp.first.if0` | 168,680 | 1.687 | 20 | 200 | fits | 119,258 | 136 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-c3.service.adp.last.if0` | 611,330 | 6.113 | 20 | 200 | fits | 116,426 | 62 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c3.service.acmp.first.if0` | 169,592 | 1.696 | 20 | 20 | fits | 119,258 | 136 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c3.service.acmp.last.if0` | 856,014 | 8.560 | 20 | 20 | fits | 121,305 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c3.service.aecp.first.if0` | 53,919 | 0.539 | 20 | 24 | fits | 56,614 | 71 | 0.547 |
| AECP record released under the composed load, last | `backlog-adp@blank-c3.service.aecp.last.if1` | 1,461,360 | 14.614 | 20 | 24 | fits | 70,962 | 37 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c3.service.maap.first.if0` | 52,879 | 0.529 | 20 | 50 | fits | 56,614 | 71 | 0.547 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c3.service.maap.last.if0` | 498,580 | 4.986 | 20 | 50 | fits | 137,846 | 76 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-c3.service.srp.first.if0` | 360,669 | 3.607 | 18 | 18 | fits | 188,987 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-c3.service.srp.last.if1` | 1,661,217 | 16.612 | 18 | 18 | fits | 50,105 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c4.adp_available.if0` | 460,291 | 4.603 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-c4.service.adp.first.if0` | 112,796 | 1.128 | 20 | 200 | fits | 118,826 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-c4.service.adp.last.if0` | 575,446 | 5.754 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c4.service.acmp.first.if0` | 113,708 | 1.137 | 20 | 20 | fits | 118,826 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c4.service.acmp.last.if0` | 820,514 | 8.205 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c4.service.aecp.first.if0` | 117,293 | 1.173 | 20 | 24 | fits | 118,826 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-c4.service.aecp.last.if1` | 1,517,505 | 15.175 | 20 | 24 | fits | 67,625 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c4.service.maap.first.if0` | 116,253 | 1.163 | 20 | 50 | fits | 118,826 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c4.service.maap.last.if0` | 579,122 | 5.791 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-c4.service.srp.first.if0` | 305,782 | 3.058 | 18 | 18 | fits | 189,984 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-c4.service.srp.last.if1` | 1,617,074 | 16.171 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c5.adp_available.if0` | 460,327 | 4.603 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-c5.service.adp.first.if0` | 112,717 | 1.127 | 20 | 200 | fits | 118,747 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-c5.service.adp.last.if0` | 575,482 | 5.755 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c5.service.acmp.first.if0` | 113,629 | 1.136 | 20 | 20 | fits | 118,747 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c5.service.acmp.last.if0` | 820,550 | 8.206 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c5.service.aecp.first.if0` | 117,214 | 1.172 | 20 | 24 | fits | 118,747 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-c5.service.aecp.last.if1` | 1,517,541 | 15.175 | 20 | 24 | fits | 67,625 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c5.service.maap.first.if0` | 116,174 | 1.162 | 20 | 50 | fits | 118,747 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c5.service.maap.last.if0` | 579,158 | 5.792 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-c5.service.srp.first.if0` | 305,761 | 3.058 | 18 | 18 | fits | 190,042 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-c5.service.srp.last.if1` | 1,617,110 | 16.171 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-c6.adp_available.if0` | 464,108 | 4.641 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-c6.service.adp.first.if0` | 117,546 | 1.175 | 20 | 200 | fits | 118,872 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-c6.service.adp.last.if0` | 579,263 | 5.793 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-c6.service.acmp.first.if0` | 118,458 | 1.185 | 20 | 20 | fits | 118,872 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-c6.service.acmp.last.if0` | 824,331 | 8.243 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-c6.service.aecp.first.if0` | 122,043 | 1.220 | 20 | 24 | fits | 118,872 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-c6.service.aecp.last.if1` | 1,521,322 | 15.213 | 20 | 24 | fits | 67,625 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-c6.service.maap.first.if0` | 121,003 | 1.210 | 20 | 50 | fits | 118,872 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-c6.service.maap.last.if0` | 582,939 | 5.829 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-c6.service.srp.first.if0` | 309,599 | 3.096 | 18 | 18 | fits | 189,051 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-c6.service.srp.last.if1` | 1,620,891 | 16.209 | 18 | 18 | fits | 50,334 | 18 | 0.713 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
