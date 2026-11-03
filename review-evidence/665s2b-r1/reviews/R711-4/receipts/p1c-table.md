### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 132 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 5.419 (7.509) | fits | 7 adp | 12 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.960 | fits | 0 acmp | 12 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 9.021 | fits | 11 acmp | 12 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.951 | fits | 0 adp | 12 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.570 | fits | 7 adp | 12 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.996 | fits | 0 aecp | 12 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@blank-I19.service.aecp.last.if1` (backlog-adp@blank-I19) | 15.976 | fits | 15 aecp | 12 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.986 | fits | 0 maap | 12 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.607 | fits | 6 maap | 12 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.srp.first.if0` (backlog-adp@blank-0) | 3.874 | fits | 0 srp | 12 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-I20.service.srp.last.if1` (backlog-adp@blank-I20) | 17.290 | fits | 31 srp | 12 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.599 | 19 | 189,276 (1.893) | yes | - |
| backlog-adp@blank-I19 | 0 | 17.579 | 18 | 189,036 (1.890) | yes | - |
| backlog-adp@blank-I20 | 0 | 17.895 | 19 | 188,950 (1.889) | yes | - |
| backlog-adp@blank-I21 | 0 | 17.981 | 19 | 188,987 (1.890) | yes | - |
| backlog-adp@blank-I22 | 0 | 17.573 | 18 | 189,027 (1.890) | yes | - |
| backlog-adp@blank-I23 | 0 | 17.926 | 19 | 189,113 (1.891) | yes | - |
| backlog-adp@blank-I24 | 1 | 17.539 | 17 | 189,984 (1.900) | yes | - |
| backlog-adp@blank-I25 | 0 | 17.611 | 18 | 188,950 (1.889) | yes | - |
| backlog-adp@blank-I26 | 0 | 17.935 | 19 | 188,950 (1.889) | yes | - |
| backlog-adp@blank-I27 | 1 | 17.540 | 17 | 190,042 (1.900) | yes | - |
| backlog-adp@blank-I28 | 0 | 17.634 | 18 | 189,036 (1.890) | yes | - |
| backlog-adp@blank-I29 | 0 | 17.941 | 19 | 188,950 (1.889) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 480 | 0 | 189,276 (1.893) | fits |
| backlog-adp@blank-I19 | 568 | 0 | 189,036 (1.890) | fits |
| backlog-adp@blank-I20 | 574 | 0 | 188,950 (1.889) | fits |
| backlog-adp@blank-I21 | 578 | 0 | 188,987 (1.890) | fits |
| backlog-adp@blank-I22 | 581 | 0 | 189,027 (1.890) | fits |
| backlog-adp@blank-I23 | 588 | 0 | 189,113 (1.891) | fits |
| backlog-adp@blank-I24 | 591 | 0 | 189,984 (1.900) | fits |
| backlog-adp@blank-I25 | 596 | 0 | 188,950 (1.889) | fits |
| backlog-adp@blank-I26 | 603 | 0 | 188,950 (1.889) | fits |
| backlog-adp@blank-I27 | 604 | 0 | 190,042 (1.900) | fits |
| backlog-adp@blank-I28 | 610 | 0 | 189,036 (1.890) | fits |
| backlog-adp@blank-I29 | 616 | 0 | 188,950 (1.889) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-I19 | 335 | 102,374 (1.024) | 76,455 (0.765) |
| backlog-adp@blank-I20 | 335 | 102,374 (1.024) | 76,455 (0.765) |
| backlog-adp@blank-I21 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-I22 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-I23 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-I24 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-I25 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-I26 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-I27 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-I28 | 335 | 102,374 (1.024) | 76,232 (0.762) |
| backlog-adp@blank-I29 | 335 | 102,374 (1.024) | 76,232 (0.762) |

Longest pass that carries a step: 102,374 CPU cycles (1.024 ms), backlog-adp@blank-0; longest step: 76,455 (0.765 ms), backlog-adp@blank-I19.

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
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I19.adp_available.if0` | 462,943 | 4.629 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-I19.service.adp.first.if0` | 116,286 | 1.163 | 20 | 200 | fits | 118,677 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-I19.service.adp.last.if0` | 578,021 | 5.780 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I19.service.acmp.first.if0` | 117,198 | 1.172 | 20 | 20 | fits | 118,677 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I19.service.acmp.last.if0` | 823,240 | 8.232 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I19.service.aecp.first.if0` | 120,783 | 1.208 | 20 | 24 | fits | 118,677 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-I19.service.aecp.last.if1` | 1,597,637 | 15.976 | 20 | 24 | fits | 67,553 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I19.service.maap.first.if0` | 119,743 | 1.197 | 20 | 50 | fits | 118,677 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I19.service.maap.last.if0` | 581,697 | 5.817 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-I19.service.srp.first.if0` | 308,324 | 3.083 | 18 | 18 | fits | 189,036 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-I19.service.srp.last.if1` | 1,697,153 | 16.972 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I20.adp_available.if0` | 469,692 | 4.697 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-I20.service.adp.first.if0` | 123,121 | 1.231 | 20 | 200 | fits | 118,677 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-I20.service.adp.last.if0` | 584,770 | 5.848 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I20.service.acmp.first.if0` | 124,033 | 1.240 | 20 | 20 | fits | 118,677 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I20.service.acmp.last.if0` | 829,989 | 8.300 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I20.service.aecp.first.if0` | 127,618 | 1.276 | 20 | 24 | fits | 118,677 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-I20.service.aecp.last.if1` | 1,592,186 | 15.922 | 20 | 24 | fits | 67,800 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I20.service.maap.first.if0` | 126,578 | 1.266 | 20 | 50 | fits | 118,677 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I20.service.maap.last.if0` | 588,446 | 5.884 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-I20.service.srp.first.if0` | 315,073 | 3.151 | 18 | 18 | fits | 188,950 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-I20.service.srp.last.if1` | 1,729,014 | 17.290 | 18 | 18 | fits | 36,804 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I21.adp_available.if0` | 506,217 | 5.062 | 20 | 20 | fits | 116,426 | 62 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@blank-I21.service.adp.first.if0` | 168,680 | 1.687 | 20 | 200 | fits | 119,258 | 136 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-I21.service.adp.last.if0` | 611,330 | 6.113 | 20 | 200 | fits | 116,426 | 62 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I21.service.acmp.first.if0` | 169,592 | 1.696 | 20 | 20 | fits | 119,258 | 136 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I21.service.acmp.last.if0` | 856,014 | 8.560 | 20 | 20 | fits | 121,305 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I21.service.aecp.first.if0` | 53,919 | 0.539 | 20 | 24 | fits | 56,614 | 71 | 0.547 |
| AECP record released under the composed load, last | `backlog-adp@blank-I21.service.aecp.last.if1` | 1,461,360 | 14.614 | 20 | 24 | fits | 70,962 | 37 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I21.service.maap.first.if0` | 52,879 | 0.529 | 20 | 50 | fits | 56,614 | 71 | 0.547 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I21.service.maap.last.if0` | 498,580 | 4.986 | 20 | 50 | fits | 137,846 | 76 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-I21.service.srp.first.if0` | 360,669 | 3.607 | 18 | 18 | fits | 188,987 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-I21.service.srp.last.if1` | 1,661,217 | 16.612 | 18 | 18 | fits | 50,105 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I22.adp_available.if0` | 463,618 | 4.636 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-I22.service.adp.first.if0` | 117,080 | 1.171 | 20 | 200 | fits | 118,826 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-I22.service.adp.last.if0` | 578,773 | 5.788 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I22.service.acmp.first.if0` | 117,992 | 1.180 | 20 | 20 | fits | 118,826 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I22.service.acmp.last.if0` | 823,841 | 8.238 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I22.service.aecp.first.if0` | 121,577 | 1.216 | 20 | 24 | fits | 118,826 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-I22.service.aecp.last.if1` | 1,520,832 | 15.208 | 20 | 24 | fits | 67,625 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I22.service.maap.first.if0` | 120,537 | 1.205 | 20 | 50 | fits | 118,826 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I22.service.maap.last.if0` | 582,449 | 5.824 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-I22.service.srp.first.if0` | 309,109 | 3.091 | 18 | 18 | fits | 189,027 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-I22.service.srp.last.if1` | 1,620,401 | 16.204 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I23.adp_available.if0` | 474,815 | 4.748 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-I23.service.adp.first.if0` | 128,191 | 1.282 | 20 | 200 | fits | 118,887 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-I23.service.adp.last.if0` | 589,970 | 5.900 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I23.service.acmp.first.if0` | 129,103 | 1.291 | 20 | 20 | fits | 118,887 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I23.service.acmp.last.if0` | 835,038 | 8.350 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I23.service.aecp.first.if0` | 132,688 | 1.327 | 20 | 24 | fits | 118,887 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-I23.service.aecp.last.if1` | 1,519,294 | 15.193 | 20 | 24 | fits | 67,827 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I23.service.maap.first.if0` | 131,648 | 1.316 | 20 | 50 | fits | 118,887 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I23.service.maap.last.if0` | 593,646 | 5.936 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-I23.service.srp.first.if0` | 320,306 | 3.203 | 18 | 18 | fits | 189,113 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-I23.service.srp.last.if1` | 1,656,063 | 16.561 | 18 | 18 | fits | 36,745 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I24.adp_available.if0` | 460,291 | 4.603 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-I24.service.adp.first.if0` | 112,796 | 1.128 | 20 | 200 | fits | 118,826 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-I24.service.adp.last.if0` | 575,446 | 5.754 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I24.service.acmp.first.if0` | 113,708 | 1.137 | 20 | 20 | fits | 118,826 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I24.service.acmp.last.if0` | 820,514 | 8.205 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I24.service.aecp.first.if0` | 117,293 | 1.173 | 20 | 24 | fits | 118,826 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-I24.service.aecp.last.if1` | 1,517,505 | 15.175 | 20 | 24 | fits | 67,625 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I24.service.maap.first.if0` | 116,253 | 1.163 | 20 | 50 | fits | 118,826 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I24.service.maap.last.if0` | 579,122 | 5.791 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-I24.service.srp.first.if0` | 305,782 | 3.058 | 18 | 18 | fits | 189,984 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-I24.service.srp.last.if1` | 1,617,074 | 16.171 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I25.adp_available.if0` | 467,380 | 4.674 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-I25.service.adp.first.if0` | 120,996 | 1.210 | 20 | 200 | fits | 118,749 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-I25.service.adp.last.if0` | 582,458 | 5.825 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I25.service.acmp.first.if0` | 121,908 | 1.219 | 20 | 20 | fits | 118,749 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I25.service.acmp.last.if0` | 827,677 | 8.277 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I25.service.aecp.first.if0` | 125,493 | 1.255 | 20 | 24 | fits | 118,749 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-I25.service.aecp.last.if1` | 1,524,630 | 15.246 | 20 | 24 | fits | 67,625 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I25.service.maap.first.if0` | 124,453 | 1.245 | 20 | 50 | fits | 118,749 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I25.service.maap.last.if0` | 586,134 | 5.861 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-I25.service.srp.first.if0` | 312,948 | 3.129 | 18 | 18 | fits | 188,950 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-I25.service.srp.last.if1` | 1,624,199 | 16.242 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I26.adp_available.if0` | 475,704 | 4.757 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-I26.service.adp.first.if0` | 129,320 | 1.293 | 20 | 200 | fits | 118,749 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-I26.service.adp.last.if0` | 590,782 | 5.908 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I26.service.acmp.first.if0` | 130,232 | 1.302 | 20 | 20 | fits | 118,749 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I26.service.acmp.last.if0` | 836,001 | 8.360 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I26.service.aecp.first.if0` | 133,817 | 1.338 | 20 | 24 | fits | 118,749 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-I26.service.aecp.last.if1` | 1,520,219 | 15.202 | 20 | 24 | fits | 67,827 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I26.service.maap.first.if0` | 132,777 | 1.328 | 20 | 50 | fits | 118,749 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I26.service.maap.last.if0` | 594,458 | 5.945 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-I26.service.srp.first.if0` | 321,272 | 3.213 | 18 | 18 | fits | 188,950 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-I26.service.srp.last.if1` | 1,656,988 | 16.570 | 18 | 18 | fits | 36,745 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I27.adp_available.if0` | 460,327 | 4.603 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-I27.service.adp.first.if0` | 112,717 | 1.127 | 20 | 200 | fits | 118,747 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-I27.service.adp.last.if0` | 575,482 | 5.755 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I27.service.acmp.first.if0` | 113,629 | 1.136 | 20 | 20 | fits | 118,747 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I27.service.acmp.last.if0` | 820,550 | 8.206 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I27.service.aecp.first.if0` | 117,214 | 1.172 | 20 | 24 | fits | 118,747 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-I27.service.aecp.last.if1` | 1,517,541 | 15.175 | 20 | 24 | fits | 67,625 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I27.service.maap.first.if0` | 116,174 | 1.162 | 20 | 50 | fits | 118,747 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I27.service.maap.last.if0` | 579,158 | 5.792 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-I27.service.srp.first.if0` | 305,761 | 3.058 | 18 | 18 | fits | 190,042 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-I27.service.srp.last.if1` | 1,617,110 | 16.171 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I28.adp_available.if0` | 469,718 | 4.697 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-I28.service.adp.first.if0` | 123,248 | 1.232 | 20 | 200 | fits | 118,749 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-I28.service.adp.last.if0` | 584,796 | 5.848 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I28.service.acmp.first.if0` | 124,160 | 1.242 | 20 | 20 | fits | 118,749 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I28.service.acmp.last.if0` | 830,015 | 8.300 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I28.service.aecp.first.if0` | 127,745 | 1.277 | 20 | 24 | fits | 118,749 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-I28.service.aecp.last.if1` | 1,526,968 | 15.270 | 20 | 24 | fits | 67,625 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I28.service.maap.first.if0` | 126,705 | 1.267 | 20 | 50 | fits | 118,749 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I28.service.maap.last.if0` | 588,472 | 5.885 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-I28.service.srp.first.if0` | 315,286 | 3.153 | 18 | 18 | fits | 189,036 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-I28.service.srp.last.if1` | 1,626,537 | 16.265 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-I29.adp_available.if0` | 476,210 | 4.762 | 20 | 20 | fits | 126,391 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@blank-I29.service.adp.first.if0` | 129,826 | 1.298 | 20 | 200 | fits | 118,749 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-I29.service.adp.last.if0` | 591,288 | 5.913 | 20 | 200 | fits | 126,391 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@blank-I29.service.acmp.first.if0` | 130,738 | 1.307 | 20 | 20 | fits | 118,749 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-I29.service.acmp.last.if0` | 836,507 | 8.365 | 20 | 20 | fits | 121,480 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-I29.service.aecp.first.if0` | 134,323 | 1.343 | 20 | 24 | fits | 118,749 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-I29.service.aecp.last.if1` | 1,520,725 | 15.207 | 20 | 24 | fits | 67,827 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-I29.service.maap.first.if0` | 133,283 | 1.333 | 20 | 50 | fits | 118,749 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-I29.service.maap.last.if0` | 594,964 | 5.950 | 20 | 50 | fits | 126,391 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-I29.service.srp.first.if0` | 321,778 | 3.218 | 18 | 18 | fits | 188,950 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-I29.service.srp.last.if1` | 1,657,494 | 16.575 | 18 | 18 | fits | 36,745 | 15 | 0.766 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
