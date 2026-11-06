### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 11 paths and 8 of 88 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-7.adp_available.if0` (backlog-adp@verify-aged2-7) | 7.350 (8.687) | fits | 7 adp | 8 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-2.service.acmp.first.if0` (backlog-adp@verify-aged2-2) | 1.289 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.acmp.last.if0` (backlog-adp@verify-aged2-7) | 10.832 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-2.service.adp.first.if0` (backlog-adp@verify-aged2-2) | 1.280 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.adp.last.if0` (backlog-adp@verify-aged2-7) | 8.658 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-2.service.aecp.first.if0` (backlog-adp@verify-aged2-2) | 1.325 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@verify-aged2-7.service.aecp.last.if1` (backlog-adp@verify-aged2-7) | 17.029 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-2.service.maap.first.if0` (backlog-adp@verify-aged2-2) | 1.314 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.maap.last.if0` (backlog-adp@verify-aged2-7) | 7.287 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.srp.first.if0` (backlog-adp@verify-aged2-6) | 3.566 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-aged2-2.service.srp.last.if1` (backlog-adp@verify-aged2-2) | 18.568 | MISS ceiling | 31 srp | 8 | 8 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@verify-aged2-0 | 0 | 18.763 | 21 | 190,480 (1.905) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 19.786 | 22 | 189,086 (1.891) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 19.958 | 22 | 189,086 (1.891) | yes | - |
| backlog-adp@verify-aged2-3 | 1 | 19.770 | 21 | 189,559 (1.896) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 20.429 | 23 | 188,948 (1.889) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 19.894 | 22 | 189,819 (1.898) | yes | - |
| backlog-adp@verify-aged2-6 | 1 | 19.951 | 22 | 166,250 (1.663) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 19.698 | 21 | 166,262 (1.663) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@verify-aged2-0 | 1497 | 0 | 190,480 (1.905) | fits |
| backlog-adp@verify-aged2-1 | 1505 | 0 | 189,086 (1.891) | fits |
| backlog-adp@verify-aged2-2 | 1512 | 0 | 189,086 (1.891) | fits |
| backlog-adp@verify-aged2-3 | 1518 | 0 | 189,559 (1.896) | fits |
| backlog-adp@verify-aged2-4 | 1527 | 0 | 188,948 (1.889) | fits |
| backlog-adp@verify-aged2-5 | 1533 | 0 | 189,819 (1.898) | fits |
| backlog-adp@verify-aged2-6 | 1540 | 0 | 166,250 (1.663) | fits |
| backlog-adp@verify-aged2-7 | 1545 | 0 | 166,262 (1.663) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@verify-aged2-0 | 2 | +10.194 ms, 159,204 (1.592 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 18.137 (18) | -0.137 |
| backlog-adp@verify-aged2-1 | 2 | +8.932 ms, 159,300 (1.593 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 18.166 (18) | -0.166 |
| backlog-adp@verify-aged2-2 | 2 | +8.070 ms, 159,422 (1.594 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 18.568 (18) | -0.568 |
| backlog-adp@verify-aged2-3 | 2 | +6.940 ms, 159,179 (1.592 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 18.376 (18) | -0.376 |
| backlog-adp@verify-aged2-4 | 2 | +5.702 ms, 159,340 (1.593 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 18.407 (18) | -0.407 |
| backlog-adp@verify-aged2-5 | 2 | +5.187 ms, 166,000 (1.660 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 18.394 (18) | -0.394 |
| backlog-adp@verify-aged2-6 | 2 | +3.583 ms, 166,250 (1.663 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 18.561 (18) | -0.561 |
| backlog-adp@verify-aged2-7 | 2 | +2.536 ms, 166,262 (1.663 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 18.308 (18) | -0.308 |

Least margin over the aged windows: -0.568 ms, `backlog-adp@verify-aged2-2.service.srp.last.if1` at 18.568 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@verify-aged2-0 | 546 | 163,224 (1.632) | 147,663 (1.477) |
| backlog-adp@verify-aged2-1 | 547 | 163,224 (1.632) | 147,663 (1.477) |
| backlog-adp@verify-aged2-2 | 547 | 163,224 (1.632) | 147,785 (1.478) |
| backlog-adp@verify-aged2-3 | 547 | 163,224 (1.632) | 147,616 (1.476) |
| backlog-adp@verify-aged2-4 | 547 | 163,224 (1.632) | 147,616 (1.476) |
| backlog-adp@verify-aged2-5 | 547 | 166,000 (1.660) | 147,616 (1.476) |
| backlog-adp@verify-aged2-6 | 547 | 166,250 (1.663) | 147,664 (1.477) |
| backlog-adp@verify-aged2-7 | 547 | 166,262 (1.663) | 147,664 (1.477) |

Longest pass that carries a step: 166,262 CPU cycles (1.663 ms), backlog-adp@verify-aged2-7; longest step: 147,785 (1.478 ms), backlog-adp@verify-aged2-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 475,284 | 4.753 | 20 | 20 | fits | 152,895 | 83 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 118,513 | 1.185 | 20 | 200 | fits | 118,370 | 135 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 617,034 | 6.170 | 20 | 200 | fits | 152,895 | 83 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 119,425 | 1.194 | 20 | 20 | fits | 118,370 | 135 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 858,010 | 8.580 | 20 | 20 | fits | 119,462 | 46 | 0.696 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 123,010 | 1.230 | 20 | 24 | fits | 118,370 | 135 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 1,661,835 | 16.618 | 20 | 24 | fits | 65,254 | 32 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 121,970 | 1.220 | 20 | 50 | fits | 118,370 | 135 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 620,710 | 6.207 | 20 | 50 | fits | 152,895 | 83 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 311,995 | 3.120 | 18 | 18 | fits | 190,480 | 146 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 1,813,651 | 18.137 | 18 | 18 | MISS ceiling | 46,945 | 18 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 478,772 | 4.788 | 20 | 20 | fits | 153,841 | 83 | 0.673 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 124,197 | 1.242 | 20 | 200 | fits | 118,533 | 135 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 620,995 | 6.210 | 20 | 200 | fits | 153,841 | 83 | 0.673 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 125,109 | 1.251 | 20 | 20 | fits | 118,533 | 135 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 828,937 | 8.289 | 20 | 20 | fits | 86,622 | 37 | 0.654 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 128,694 | 1.287 | 20 | 24 | fits | 118,533 | 135 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 1,688,849 | 16.888 | 20 | 24 | fits | 65,273 | 31 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 127,654 | 1.277 | 20 | 50 | fits | 118,533 | 135 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 624,671 | 6.247 | 20 | 50 | fits | 153,841 | 83 | 0.673 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 316,285 | 3.163 | 18 | 18 | fits | 189,086 | 141 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 1,816,573 | 18.166 | 18 | 18 | MISS ceiling | 34,291 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 482,543 | 4.825 | 20 | 20 | fits | 153,841 | 83 | 0.673 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 127,968 | 1.280 | 20 | 200 | fits | 118,533 | 135 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 624,766 | 6.248 | 20 | 200 | fits | 153,841 | 83 | 0.673 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 128,880 | 1.289 | 20 | 20 | fits | 118,533 | 135 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 1,059,300 | 10.593 | 20 | 20 | fits | 97,510 | 39 | 0.748 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 132,465 | 1.325 | 20 | 24 | fits | 118,533 | 135 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 1,686,912 | 16.869 | 20 | 24 | fits | 65,486 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 131,425 | 1.314 | 20 | 50 | fits | 118,533 | 135 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 628,442 | 6.284 | 20 | 50 | fits | 153,841 | 83 | 0.673 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 320,056 | 3.201 | 18 | 18 | fits | 189,086 | 141 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 1,856,830 | 18.568 | 18 | 18 | MISS ceiling | 34,289 | 15 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 467,247 | 4.672 | 20 | 20 | fits | 139,538 | 79 | 0.682 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 112,175 | 1.122 | 20 | 200 | fits | 118,533 | 135 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 595,264 | 5.953 | 20 | 200 | fits | 139,538 | 79 | 0.682 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 113,087 | 1.131 | 20 | 20 | fits | 118,533 | 135 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 1,033,668 | 10.337 | 20 | 20 | fits | 98,671 | 46 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 116,672 | 1.167 | 20 | 24 | fits | 118,533 | 135 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 1,650,752 | 16.508 | 20 | 24 | fits | 60,160 | 32 | 0.762 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 115,632 | 1.156 | 20 | 50 | fits | 118,533 | 135 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 598,940 | 5.989 | 20 | 50 | fits | 139,538 | 79 | 0.682 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 313,672 | 3.137 | 18 | 18 | fits | 189,559 | 145 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 1,837,629 | 18.376 | 18 | 18 | MISS ceiling | 46,910 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 733,411 | 7.334 | 20 | 20 | fits | 106,274 | 49 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 126,199 | 1.262 | 20 | 200 | fits | 117,999 | 134 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 830,551 | 8.306 | 20 | 200 | fits | 106,274 | 49 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 127,111 | 1.271 | 20 | 20 | fits | 117,999 | 134 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 1,050,077 | 10.501 | 20 | 20 | fits | 97,878 | 40 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 130,696 | 1.307 | 20 | 24 | fits | 117,999 | 134 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 1,665,705 | 16.657 | 20 | 24 | fits | 99,936 | 45 | 0.756 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 129,656 | 1.297 | 20 | 50 | fits | 117,999 | 134 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 568,613 | 5.686 | 20 | 50 | fits | 104,679 | 64 | 0.731 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 318,149 | 3.181 | 18 | 18 | fits | 188,948 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 1,840,736 | 18.407 | 18 | 18 | MISS ceiling | 34,289 | 15 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 691,701 | 6.917 | 20 | 20 | fits | 144,182 | 63 | 0.717 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 110,543 | 1.105 | 20 | 200 | fits | 117,999 | 134 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 823,553 | 8.236 | 20 | 200 | fits | 144,182 | 63 | 0.717 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 111,455 | 1.115 | 20 | 20 | fits | 117,999 | 134 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 1,041,198 | 10.412 | 20 | 20 | fits | 97,211 | 39 | 0.737 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 115,040 | 1.150 | 20 | 24 | fits | 117,999 | 134 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 1,617,095 | 16.171 | 20 | 24 | fits | 100,392 | 46 | 0.757 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 114,000 | 1.140 | 20 | 50 | fits | 117,999 | 134 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 517,047 | 5.170 | 20 | 50 | fits | 102,936 | 64 | 0.712 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 303,364 | 3.034 | 18 | 18 | fits | 189,819 | 145 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 1,839,378 | 18.394 | 18 | 18 | MISS ceiling | 34,358 | 16 | 0.763 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 695,186 | 6.952 | 20 | 20 | fits | 142,129 | 57 | 0.713 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 111,903 | 1.119 | 20 | 200 | fits | 117,999 | 134 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 826,709 | 8.267 | 20 | 200 | fits | 142,129 | 57 | 0.713 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 112,815 | 1.128 | 20 | 20 | fits | 117,999 | 134 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 1,044,163 | 10.442 | 20 | 20 | fits | 97,389 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 116,400 | 1.164 | 20 | 24 | fits | 117,999 | 134 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 1,586,255 | 15.863 | 20 | 24 | fits | 65,380 | 32 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 115,360 | 1.154 | 20 | 50 | fits | 117,999 | 134 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 688,256 | 6.883 | 20 | 50 | fits | 165,319 | 104 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 356,622 | 3.566 | 18 | 18 | fits | 125,701 | 64 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 1,856,062 | 18.561 | 18 | 18 | MISS ceiling | 34,427 | 15 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 735,025 | 7.350 | 20 | 20 | fits | 140,725 | 57 | 0.707 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 115,679 | 1.157 | 20 | 200 | fits | 117,999 | 134 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 865,774 | 8.658 | 20 | 200 | fits | 140,725 | 57 | 0.707 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 116,591 | 1.166 | 20 | 20 | fits | 117,999 | 134 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 1,083,228 | 10.832 | 20 | 20 | fits | 97,249 | 39 | 0.737 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 120,176 | 1.202 | 20 | 24 | fits | 117,999 | 134 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 1,702,926 | 17.029 | 20 | 24 | fits | 100,284 | 45 | 0.759 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 119,136 | 1.191 | 20 | 50 | fits | 117,999 | 134 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 728,725 | 7.287 | 20 | 50 | fits | 145,174 | 98 | 0.625 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 251,911 | 2.519 | 18 | 18 | fits | 133,230 | 105 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 1,830,815 | 18.308 | 18 | 18 | MISS ceiling | 34,291 | 15 | 0.778 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
