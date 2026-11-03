### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 11 paths and 11 of 264 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-7.adp_available.if0` (backlog-adp@blank-7) | 5.717 (7.345) | fits | 7 adp | 24 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.969 | fits | 0 acmp | 24 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-7.service.acmp.last.if0` (backlog-adp@blank-7) | 9.601 | fits | 11 acmp | 24 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.960 | fits | 0 adp | 24 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-7.service.adp.last.if0` (backlog-adp@blank-7) | 7.157 | fits | 7 adp | 24 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.005 | fits | 0 aecp | 24 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@verify-6.service.aecp.last.if1` (backlog-adp@verify-6) | 17.425 | fits | 15 aecp | 24 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.994 | fits | 0 maap | 24 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-7.service.maap.last.if0` (backlog-adp@blank-7) | 7.194 | fits | 6 maap | 24 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-3.service.srp.first.if0` (backlog-adp@program-3) | 5.207 | fits | 0 srp | 24 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-1.service.srp.last.if1` (backlog-adp@verify-1) | 19.134 | MISS ceiling | 31 srp | 24 | 11 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.585 | 19 | 189,738 (1.897) | yes | - |
| backlog-adp@blank-1 | 0 | 17.912 | 19 | 189,624 (1.896) | yes | - |
| backlog-adp@blank-2 | 0 | 19.326 | 21 | 204,348 (2.043) | yes | - |
| backlog-adp@blank-3 | 0 | 18.688 | 18 | 204,732 (2.047) | yes | - |
| backlog-adp@blank-4 | 0 | 18.748 | 18 | 204,236 (2.042) | yes | - |
| backlog-adp@blank-5 | 0 | 18.784 | 19 | 236,969 (2.370) | yes | - |
| backlog-adp@blank-6 | 0 | 18.694 | 19 | 264,242 (2.642) | yes | - |
| backlog-adp@blank-7 | 0 | 18.477 | 17 | 271,776 (2.718) | yes | - |
| backlog-adp@program-0 | 1 | 17.742 | 17 | 189,627 (1.896) | yes | - |
| backlog-adp@program-1 | 0 | 18.259 | 20 | 208,874 (2.089) | yes | - |
| backlog-adp@program-2 | 0 | 18.216 | 19 | 242,474 (2.425) | yes | - |
| backlog-adp@program-3 | 0 | 18.162 | 19 | 269,320 (2.693) | yes | - |
| backlog-adp@program-4 | 0 | 17.079 | 18 | 188,761 (1.888) | yes | - |
| backlog-adp@program-5 | 0 | 18.287 | 20 | 188,653 (1.887) | yes | - |
| backlog-adp@program-6 | 0 | 18.210 | 19 | 190,943 (1.909) | yes | - |
| backlog-adp@program-7 | 0 | 18.038 | 19 | 192,119 (1.921) | yes | - |
| backlog-adp@verify-0 | 0 | 18.912 | 20 | 184,223 (1.842) | yes | - |
| backlog-adp@verify-1 | 0 | 19.742 | 21 | 191,599 (1.916) | yes | - |
| backlog-adp@verify-2 | 0 | 19.547 | 21 | 189,429 (1.894) | yes | - |
| backlog-adp@verify-3 | 0 | 19.089 | 19 | 189,429 (1.894) | yes | - |
| backlog-adp@verify-4 | 0 | 19.120 | 20 | 208,401 (2.084) | yes | - |
| backlog-adp@verify-5 | 0 | 18.853 | 18 | 201,170 (2.012) | yes | - |
| backlog-adp@verify-6 | 0 | 19.343 | 19 | 249,253 (2.493) | yes | - |
| backlog-adp@verify-7 | 0 | 19.061 | 19 | 204,825 (2.048) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 502 | 0 | 189,738 (1.897) | fits |
| backlog-adp@blank-1 | 502 | 0 | 189,624 (1.896) | fits |
| backlog-adp@blank-2 | 504 | 1 | 204,348 (2.043) | OVER the share |
| backlog-adp@blank-3 | 501 | 1 | 204,732 (2.047) | OVER the share |
| backlog-adp@blank-4 | 503 | 1 | 204,236 (2.042) | OVER the share |
| backlog-adp@blank-5 | 503 | 1 | 236,969 (2.370) | OVER the share |
| backlog-adp@blank-6 | 503 | 1 | 264,242 (2.642) | OVER the share |
| backlog-adp@blank-7 | 501 | 1 | 271,776 (2.718) | OVER the share |
| backlog-adp@program-0 | 780 | 0 | 189,627 (1.896) | fits |
| backlog-adp@program-1 | 783 | 1 | 208,874 (2.089) | OVER the share |
| backlog-adp@program-2 | 782 | 1 | 242,474 (2.425) | OVER the share |
| backlog-adp@program-3 | 782 | 1 | 269,320 (2.693) | OVER the share |
| backlog-adp@program-4 | 783 | 0 | 188,761 (1.888) | fits |
| backlog-adp@program-5 | 785 | 0 | 188,653 (1.887) | fits |
| backlog-adp@program-6 | 784 | 0 | 190,943 (1.909) | fits |
| backlog-adp@program-7 | 785 | 0 | 192,119 (1.921) | fits |
| backlog-adp@verify-0 | 1079 | 0 | 184,223 (1.842) | fits |
| backlog-adp@verify-1 | 1080 | 0 | 191,599 (1.916) | fits |
| backlog-adp@verify-2 | 1081 | 0 | 189,429 (1.894) | fits |
| backlog-adp@verify-3 | 1079 | 0 | 189,429 (1.894) | fits |
| backlog-adp@verify-4 | 1080 | 1 | 208,401 (2.084) | OVER the share |
| backlog-adp@verify-5 | 1078 | 1 | 201,170 (2.012) | OVER the share |
| backlog-adp@verify-6 | 1079 | 1 | 249,253 (2.493) | OVER the share |
| backlog-adp@verify-7 | 1079 | 1 | 204,825 (2.048) | OVER the share |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 337 | 150,800 (1.508) | 76,508 (0.765) |
| backlog-adp@blank-1 | 337 | 150,487 (1.505) | 76,508 (0.765) |
| backlog-adp@blank-2 | 338 | 204,348 (2.043) | 76,678 (0.767) |
| backlog-adp@blank-3 | 338 | 204,732 (2.047) | 76,780 (0.768) |
| backlog-adp@blank-4 | 338 | 204,236 (2.042) | 76,780 (0.768) |
| backlog-adp@blank-5 | 338 | 236,969 (2.370) | 76,823 (0.768) |
| backlog-adp@blank-6 | 338 | 264,242 (2.642) | 76,823 (0.768) |
| backlog-adp@blank-7 | 338 | 271,776 (2.718) | 76,823 (0.768) |
| backlog-adp@program-0 | 443 | 156,653 (1.567) | 82,515 (0.825) |
| backlog-adp@program-1 | 444 | 208,874 (2.089) | 82,652 (0.827) |
| backlog-adp@program-2 | 444 | 242,474 (2.425) | 82,738 (0.827) |
| backlog-adp@program-3 | 444 | 269,320 (2.693) | 82,738 (0.827) |
| backlog-adp@program-4 | 444 | 150,262 (1.503) | 82,225 (0.822) |
| backlog-adp@program-5 | 445 | 150,262 (1.503) | 82,225 (0.822) |
| backlog-adp@program-6 | 445 | 165,444 (1.654) | 82,423 (0.824) |
| backlog-adp@program-7 | 445 | 192,119 (1.921) | 82,482 (0.825) |
| backlog-adp@verify-0 | 546 | 151,544 (1.515) | 96,094 (0.961) |
| backlog-adp@verify-1 | 547 | 150,262 (1.503) | 96,094 (0.961) |
| backlog-adp@verify-2 | 547 | 176,826 (1.768) | 96,094 (0.961) |
| backlog-adp@verify-3 | 547 | 177,313 (1.773) | 96,094 (0.961) |
| backlog-adp@verify-4 | 547 | 208,401 (2.084) | 96,094 (0.961) |
| backlog-adp@verify-5 | 547 | 201,170 (2.012) | 96,094 (0.961) |
| backlog-adp@verify-6 | 547 | 249,253 (2.493) | 96,094 (0.961) |
| backlog-adp@verify-7 | 547 | 204,825 (2.048) | 96,094 (0.961) |

Longest pass that carries a step: 271,776 CPU cycles (2.718 ms), backlog-adp@blank-7; longest step: 96,094 (0.961 ms), backlog-adp@verify-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 515,901 | 5.159 | 20 | 20 | fits | 156,267 | 89 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 195,969 | 1.960 | 20 | 200 | fits | 120,284 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 659,355 | 6.594 | 20 | 200 | fits | 156,267 | 89 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 196,881 | 1.969 | 20 | 20 | fits | 120,284 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 904,052 | 9.041 | 20 | 20 | fits | 121,366 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 200,466 | 2.005 | 20 | 24 | fits | 120,284 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,646,780 | 16.468 | 20 | 24 | fits | 67,672 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 199,426 | 1.994 | 20 | 50 | fits | 120,284 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 663,031 | 6.630 | 20 | 50 | fits | 156,267 | 89 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 388,709 | 3.887 | 18 | 18 | fits | 189,738 | 140 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,798,001 | 17.980 | 18 | 18 | fits | 50,621 | 18 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 446,390 | 4.464 | 20 | 20 | fits | 156,267 | 89 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 126,572 | 1.266 | 20 | 200 | fits | 119,531 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 589,844 | 5.898 | 20 | 200 | fits | 156,267 | 89 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 127,484 | 1.275 | 20 | 20 | fits | 119,531 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 834,541 | 8.345 | 20 | 20 | fits | 121,366 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 131,069 | 1.311 | 20 | 24 | fits | 119,531 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,579,367 | 15.794 | 20 | 24 | fits | 67,665 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 130,029 | 1.300 | 20 | 50 | fits | 119,531 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 593,520 | 5.935 | 20 | 50 | fits | 156,267 | 89 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 319,198 | 3.192 | 18 | 18 | fits | 189,624 | 140 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,730,681 | 17.307 | 18 | 18 | fits | 50,562 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 449,153 | 4.492 | 20 | 20 | fits | 156,523 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 131,764 | 1.318 | 20 | 200 | fits | 119,531 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 594,108 | 5.941 | 20 | 200 | fits | 156,523 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 132,676 | 1.327 | 20 | 20 | fits | 119,531 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 921,567 | 9.216 | 20 | 20 | fits | 204,348 | 52 | 0.562 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 136,261 | 1.363 | 20 | 24 | fits | 119,531 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,603,100 | 16.031 | 20 | 24 | fits | 67,917 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 135,221 | 1.352 | 20 | 50 | fits | 119,531 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 597,784 | 5.978 | 20 | 50 | fits | 156,523 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 441,196 | 4.412 | 18 | 18 | fits | 184,394 | 104 | 0.667 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,741,156 | 17.412 | 18 | 18 | fits | 36,949 | 14 | 0.779 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 473,566 | 4.736 | 20 | 20 | fits | 154,777 | 83 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 124,306 | 1.243 | 20 | 200 | fits | 125,309 | 151 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 617,230 | 6.172 | 20 | 200 | fits | 154,777 | 83 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 125,218 | 1.252 | 20 | 20 | fits | 125,309 | 151 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 937,723 | 9.377 | 20 | 20 | fits | 115,065 | 53 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 128,803 | 1.288 | 20 | 24 | fits | 125,309 | 151 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,625,251 | 16.253 | 20 | 24 | fits | 67,880 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 127,763 | 1.278 | 20 | 50 | fits | 125,309 | 151 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 620,906 | 6.209 | 20 | 50 | fits | 154,777 | 83 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 319,016 | 3.190 | 18 | 18 | fits | 191,708 | 145 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,808,371 | 18.084 | 18 | 18 | MISS ceiling | 51,081 | 33 | 0.825 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 462,311 | 4.623 | 20 | 20 | fits | 120,578 | 74 | 0.622 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 114,722 | 1.147 | 20 | 200 | fits | 119,533 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 571,714 | 5.717 | 20 | 200 | fits | 120,578 | 74 | 0.622 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 115,634 | 1.156 | 20 | 20 | fits | 119,533 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 910,362 | 9.104 | 20 | 20 | fits | 133,716 | 64 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 119,219 | 1.192 | 20 | 24 | fits | 119,533 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,662,131 | 16.621 | 20 | 24 | fits | 151,271 | 37 | 0.535 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 118,179 | 1.182 | 20 | 50 | fits | 119,533 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 575,390 | 5.754 | 20 | 50 | fits | 120,578 | 74 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 307,354 | 3.074 | 18 | 18 | fits | 189,630 | 140 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,814,562 | 18.146 | 18 | 18 | MISS ceiling | 36,928 | 15 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 439,479 | 4.395 | 20 | 20 | fits | 236,969 | 89 | 0.559 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 120,059 | 1.201 | 20 | 200 | fits | 119,440 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 658,233 | 6.582 | 20 | 200 | fits | 236,969 | 89 | 0.559 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 120,971 | 1.210 | 20 | 20 | fits | 119,440 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 914,418 | 9.144 | 20 | 20 | fits | 121,524 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 124,556 | 1.246 | 20 | 24 | fits | 119,440 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,680,313 | 16.803 | 20 | 24 | fits | 68,530 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 123,516 | 1.235 | 20 | 50 | fits | 119,440 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 661,909 | 6.619 | 20 | 50 | fits | 236,969 | 89 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 312,691 | 3.127 | 18 | 18 | fits | 189,630 | 140 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,818,133 | 18.181 | 18 | 18 | MISS ceiling | 36,994 | 15 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 516,741 | 5.167 | 20 | 20 | fits | 127,575 | 85 | 0.641 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 125,343 | 1.253 | 20 | 200 | fits | 119,440 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 632,805 | 6.328 | 20 | 200 | fits | 127,575 | 85 | 0.641 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 126,255 | 1.263 | 20 | 20 | fits | 119,440 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 879,838 | 8.798 | 20 | 20 | fits | 121,955 | 46 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 129,840 | 1.298 | 20 | 24 | fits | 119,440 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,657,963 | 16.580 | 20 | 24 | fits | 67,818 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 128,800 | 1.288 | 20 | 50 | fits | 119,440 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 636,481 | 6.365 | 20 | 50 | fits | 127,575 | 85 | 0.641 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 508,841 | 5.088 | 18 | 18 | fits | 264,242 | 104 | 0.570 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,808,874 | 18.089 | 18 | 18 | MISS ceiling | 50,562 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 571,737 | 5.717 | 20 | 20 | fits | 155,203 | 83 | 0.665 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 130,627 | 1.306 | 20 | 200 | fits | 119,440 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 715,737 | 7.157 | 20 | 200 | fits | 155,203 | 83 | 0.665 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 131,539 | 1.315 | 20 | 20 | fits | 119,440 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 960,121 | 9.601 | 20 | 20 | fits | 121,255 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 135,124 | 1.351 | 20 | 24 | fits | 119,440 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,737,239 | 17.372 | 20 | 24 | fits | 67,672 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 134,084 | 1.341 | 20 | 50 | fits | 119,440 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 719,413 | 7.194 | 20 | 50 | fits | 155,203 | 83 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 405,405 | 4.054 | 18 | 18 | fits | 271,776 | 145 | 0.549 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,787,045 | 17.870 | 18 | 18 | fits | 52,341 | 20 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 462,377 | 4.624 | 20 | 20 | fits | 155,258 | 83 | 0.665 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 114,848 | 1.148 | 20 | 200 | fits | 120,660 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 606,460 | 6.065 | 20 | 200 | fits | 155,258 | 83 | 0.665 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 115,760 | 1.158 | 20 | 20 | fits | 120,660 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 823,969 | 8.240 | 20 | 20 | fits | 94,243 | 48 | 0.655 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 119,345 | 1.193 | 20 | 24 | fits | 120,660 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,608,278 | 16.083 | 20 | 24 | fits | 74,455 | 42 | 0.722 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 118,305 | 1.183 | 20 | 50 | fits | 120,660 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 610,136 | 6.101 | 20 | 50 | fits | 155,258 | 83 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 307,477 | 3.075 | 18 | 18 | fits | 189,627 | 145 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,713,654 | 17.137 | 18 | 18 | fits | 50,828 | 18 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 468,331 | 4.683 | 20 | 20 | fits | 126,552 | 85 | 0.633 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 121,650 | 1.216 | 20 | 200 | fits | 119,908 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 583,708 | 5.837 | 20 | 200 | fits | 126,552 | 85 | 0.633 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 122,562 | 1.226 | 20 | 20 | fits | 119,908 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 883,043 | 8.830 | 20 | 20 | fits | 208,874 | 52 | 0.188 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 126,147 | 1.261 | 20 | 24 | fits | 119,908 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,577,055 | 15.771 | 20 | 24 | fits | 67,811 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 125,107 | 1.251 | 20 | 50 | fits | 119,908 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 587,384 | 5.874 | 20 | 50 | fits | 126,552 | 85 | 0.633 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 313,431 | 3.134 | 18 | 18 | fits | 188,779 | 140 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,765,619 | 17.656 | 18 | 18 | fits | 38,238 | 15 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 459,685 | 4.597 | 20 | 20 | fits | 242,474 | 89 | 0.224 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 132,126 | 1.321 | 20 | 200 | fits | 119,908 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 684,249 | 6.842 | 20 | 200 | fits | 242,474 | 89 | 0.224 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 133,038 | 1.330 | 20 | 20 | fits | 119,908 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 929,072 | 9.291 | 20 | 20 | fits | 121,561 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 136,623 | 1.366 | 20 | 24 | fits | 119,908 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,623,161 | 16.232 | 20 | 24 | fits | 68,054 | 31 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 135,583 | 1.356 | 20 | 50 | fits | 119,908 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 687,925 | 6.879 | 20 | 50 | fits | 242,474 | 89 | 0.224 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 330,676 | 3.307 | 18 | 18 | fits | 195,548 | 151 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,761,368 | 17.614 | 18 | 18 | fits | 37,100 | 15 | 0.774 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 528,276 | 5.283 | 20 | 20 | fits | 156,536 | 83 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 129,843 | 1.298 | 20 | 200 | fits | 125,577 | 151 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 673,582 | 6.736 | 20 | 200 | fits | 156,536 | 83 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 130,755 | 1.308 | 20 | 20 | fits | 125,577 | 151 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 891,271 | 8.913 | 20 | 20 | fits | 94,311 | 48 | 0.655 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 134,340 | 1.343 | 20 | 24 | fits | 125,577 | 151 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,590,597 | 15.906 | 20 | 24 | fits | 67,672 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 133,300 | 1.333 | 20 | 50 | fits | 125,577 | 151 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 677,258 | 6.773 | 20 | 50 | fits | 156,536 | 83 | 0.672 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 520,657 | 5.207 | 18 | 18 | fits | 269,320 | 104 | 0.243 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,755,659 | 17.557 | 18 | 18 | fits | 50,805 | 18 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 466,885 | 4.669 | 20 | 20 | fits | 161,482 | 94 | 0.674 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 120,312 | 1.203 | 20 | 200 | fits | 120,534 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 617,192 | 6.172 | 20 | 200 | fits | 161,482 | 94 | 0.674 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 121,224 | 1.212 | 20 | 20 | fits | 120,534 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 864,898 | 8.649 | 20 | 20 | fits | 121,732 | 46 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 124,809 | 1.248 | 20 | 24 | fits | 120,534 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,560,769 | 15.608 | 20 | 24 | fits | 68,249 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 123,769 | 1.238 | 20 | 50 | fits | 120,534 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 620,868 | 6.209 | 20 | 50 | fits | 161,482 | 94 | 0.674 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 312,075 | 3.121 | 18 | 18 | fits | 188,761 | 140 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,647,709 | 16.477 | 18 | 18 | fits | 37,107 | 15 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 449,956 | 4.500 | 20 | 20 | fits | 156,313 | 89 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 131,052 | 1.311 | 20 | 200 | fits | 119,873 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 593,456 | 5.935 | 20 | 200 | fits | 156,313 | 89 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 131,964 | 1.320 | 20 | 20 | fits | 119,873 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 815,759 | 8.158 | 20 | 20 | fits | 132,554 | 52 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 135,549 | 1.355 | 20 | 24 | fits | 119,873 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,509,689 | 15.097 | 20 | 24 | fits | 67,665 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 134,509 | 1.345 | 20 | 50 | fits | 119,873 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 597,132 | 5.971 | 20 | 50 | fits | 156,313 | 89 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 322,707 | 3.227 | 18 | 18 | fits | 188,653 | 140 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,661,044 | 16.610 | 18 | 18 | fits | 50,624 | 18 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 449,540 | 4.495 | 20 | 20 | fits | 165,444 | 89 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 128,846 | 1.288 | 20 | 200 | fits | 125,711 | 151 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 596,815 | 5.968 | 20 | 200 | fits | 165,444 | 89 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 129,758 | 1.298 | 20 | 20 | fits | 125,711 | 151 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 841,481 | 8.415 | 20 | 20 | fits | 121,403 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 133,343 | 1.333 | 20 | 24 | fits | 125,711 | 151 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,623,807 | 16.238 | 20 | 24 | fits | 69,301 | 31 | 0.724 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 132,303 | 1.323 | 20 | 50 | fits | 125,711 | 151 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 600,491 | 6.005 | 20 | 50 | fits | 165,444 | 89 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 322,791 | 3.228 | 18 | 18 | fits | 190,943 | 145 | 0.638 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,760,651 | 17.607 | 18 | 18 | fits | 41,184 | 21 | 0.805 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 443,857 | 4.439 | 20 | 20 | fits | 156,761 | 83 | 0.673 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 124,705 | 1.247 | 20 | 200 | fits | 120,073 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 589,261 | 5.893 | 20 | 200 | fits | 156,761 | 83 | 0.673 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 125,617 | 1.256 | 20 | 20 | fits | 120,073 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 807,812 | 8.078 | 20 | 20 | fits | 122,693 | 52 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 129,202 | 1.292 | 20 | 24 | fits | 120,073 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,592,463 | 15.925 | 20 | 24 | fits | 68,137 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 128,162 | 1.282 | 20 | 50 | fits | 120,073 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 592,937 | 5.929 | 20 | 50 | fits | 156,761 | 83 | 0.673 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 436,111 | 4.361 | 18 | 18 | fits | 192,119 | 104 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,743,224 | 17.432 | 18 | 18 | fits | 50,512 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 442,114 | 4.421 | 20 | 20 | fits | 156,569 | 83 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 125,065 | 1.251 | 20 | 200 | fits | 119,735 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 587,115 | 5.871 | 20 | 200 | fits | 156,569 | 83 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 125,977 | 1.260 | 20 | 20 | fits | 119,735 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 831,347 | 8.313 | 20 | 20 | fits | 121,121 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 129,562 | 1.296 | 20 | 24 | fits | 119,735 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,644,519 | 16.445 | 20 | 24 | fits | 67,672 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 128,522 | 1.285 | 20 | 50 | fits | 119,735 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 590,791 | 5.908 | 20 | 50 | fits | 156,569 | 83 | 0.672 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 434,157 | 4.342 | 18 | 18 | fits | 184,223 | 104 | 0.666 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,745,119 | 17.451 | 18 | 18 | fits | 50,794 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 485,327 | 4.853 | 20 | 20 | fits | 154,823 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 136,176 | 1.362 | 20 | 200 | fits | 125,562 | 151 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 629,037 | 6.290 | 20 | 200 | fits | 154,823 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 137,088 | 1.371 | 20 | 20 | fits | 125,562 | 151 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 840,249 | 8.402 | 20 | 20 | fits | 88,172 | 37 | 0.637 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 140,673 | 1.407 | 20 | 24 | fits | 125,562 | 151 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,605,106 | 16.051 | 20 | 24 | fits | 101,992 | 45 | 0.748 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 139,633 | 1.396 | 20 | 50 | fits | 125,562 | 151 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 632,713 | 6.327 | 20 | 50 | fits | 154,823 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 330,777 | 3.308 | 18 | 18 | fits | 191,599 | 145 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,913,371 | 19.134 | 18 | 18 | MISS ceiling | 120,043 | 21 | 0.427 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 473,968 | 4.740 | 20 | 20 | fits | 155,258 | 83 | 0.665 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 126,637 | 1.266 | 20 | 200 | fits | 119,860 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 618,051 | 6.181 | 20 | 200 | fits | 155,258 | 83 | 0.665 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 127,549 | 1.275 | 20 | 20 | fits | 119,860 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 884,502 | 8.845 | 20 | 20 | fits | 176,826 | 54 | 0.501 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 131,134 | 1.311 | 20 | 24 | fits | 119,860 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,578,662 | 15.787 | 20 | 24 | fits | 107,274 | 56 | 0.746 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 130,094 | 1.301 | 20 | 50 | fits | 119,860 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 621,727 | 6.217 | 20 | 50 | fits | 155,258 | 83 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 319,068 | 3.191 | 18 | 18 | fits | 189,429 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,894,432 | 18.944 | 18 | 18 | MISS ceiling | 37,008 | 15 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 479,160 | 4.792 | 20 | 20 | fits | 120,624 | 74 | 0.623 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 131,829 | 1.318 | 20 | 200 | fits | 119,860 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 588,609 | 5.886 | 20 | 200 | fits | 120,624 | 74 | 0.623 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 132,741 | 1.327 | 20 | 20 | fits | 119,860 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 889,430 | 8.894 | 20 | 20 | fits | 122,812 | 52 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 136,326 | 1.363 | 20 | 24 | fits | 119,860 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,696,971 | 16.970 | 20 | 24 | fits | 151,731 | 37 | 0.542 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 135,286 | 1.353 | 20 | 50 | fits | 119,860 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 592,285 | 5.923 | 20 | 50 | fits | 120,624 | 74 | 0.623 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 324,260 | 3.243 | 18 | 18 | fits | 189,429 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,848,401 | 18.484 | 18 | 18 | MISS ceiling | 50,562 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 437,755 | 4.378 | 20 | 20 | fits | 208,401 | 91 | 0.513 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 118,593 | 1.186 | 20 | 200 | fits | 119,860 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 627,941 | 6.279 | 20 | 200 | fits | 208,401 | 91 | 0.513 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 119,505 | 1.195 | 20 | 20 | fits | 119,860 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 874,301 | 8.743 | 20 | 20 | fits | 121,792 | 46 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 123,090 | 1.231 | 20 | 24 | fits | 119,860 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,649,987 | 16.500 | 20 | 24 | fits | 68,913 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 122,050 | 1.220 | 20 | 50 | fits | 119,860 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 631,617 | 6.316 | 20 | 50 | fits | 208,401 | 91 | 0.513 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 311,024 | 3.110 | 18 | 18 | fits | 189,429 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,851,479 | 18.515 | 18 | 18 | MISS ceiling | 50,562 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 526,377 | 5.264 | 20 | 20 | fits | 156,295 | 89 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 123,877 | 1.239 | 20 | 200 | fits | 119,860 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 670,162 | 6.702 | 20 | 200 | fits | 156,295 | 89 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 124,789 | 1.248 | 20 | 20 | fits | 119,860 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 914,552 | 9.146 | 20 | 20 | fits | 121,179 | 46 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 128,374 | 1.284 | 20 | 24 | fits | 119,860 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,724,177 | 17.242 | 20 | 24 | fits | 67,565 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 127,334 | 1.273 | 20 | 50 | fits | 119,860 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 673,838 | 6.738 | 20 | 50 | fits | 156,295 | 89 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 316,308 | 3.163 | 18 | 18 | fits | 189,429 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,824,765 | 18.248 | 18 | 18 | MISS ceiling | 50,794 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 555,402 | 5.554 | 20 | 20 | fits | 155,965 | 83 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 129,161 | 1.292 | 20 | 200 | fits | 119,860 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 700,245 | 7.002 | 20 | 200 | fits | 155,965 | 83 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 130,073 | 1.301 | 20 | 20 | fits | 119,860 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 945,035 | 9.450 | 20 | 20 | fits | 121,424 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 133,658 | 1.337 | 20 | 24 | fits | 119,860 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,742,519 | 17.425 | 20 | 24 | fits | 101,870 | 45 | 0.747 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 132,618 | 1.326 | 20 | 50 | fits | 119,860 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 703,921 | 7.039 | 20 | 50 | fits | 155,965 | 83 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 381,416 | 3.814 | 18 | 18 | fits | 249,253 | 152 | 0.552 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,843,293 | 18.433 | 18 | 18 | MISS ceiling | 50,744 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 516,096 | 5.161 | 20 | 20 | fits | 156,567 | 83 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 115,833 | 1.158 | 20 | 200 | fits | 119,860 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 661,095 | 6.611 | 20 | 200 | fits | 156,567 | 83 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 116,745 | 1.167 | 20 | 20 | fits | 119,860 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 905,327 | 9.053 | 20 | 20 | fits | 121,121 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 120,330 | 1.203 | 20 | 24 | fits | 119,860 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,714,582 | 17.146 | 20 | 24 | fits | 68,169 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 119,290 | 1.193 | 20 | 50 | fits | 119,860 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 664,771 | 6.648 | 20 | 50 | fits | 156,567 | 83 | 0.672 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 508,139 | 5.081 | 18 | 18 | fits | 184,479 | 104 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,814,953 | 18.150 | 18 | 18 | MISS ceiling | 50,741 | 18 | 0.723 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
