### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 77 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-a5.adp_available.if0` (backlog-adp@verify-a5) | 4.910 (6.471) | fits | 7 adp | 7 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-a3.service.acmp.first.if0` (backlog-adp@verify-a3) | 1.279 | fits | 0 acmp | 7 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-a5.service.acmp.last.if0` (backlog-adp@verify-a5) | 8.787 | fits | 11 acmp | 7 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-a3.service.adp.first.if0` (backlog-adp@verify-a3) | 1.270 | fits | 0 adp | 7 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-a5.service.adp.last.if0` (backlog-adp@verify-a5) | 6.345 | fits | 7 adp | 7 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-a3.service.aecp.first.if0` (backlog-adp@verify-a3) | 1.315 | fits | 0 aecp | 7 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-adp@verify-a5.service.aecp.last.if1` (backlog-adp@verify-a5) | 15.746 | fits | 15 aecp | 7 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-a3.service.maap.first.if0` (backlog-adp@verify-a3) | 1.305 | fits | 0 maap | 7 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-a5.service.maap.last.if0` (backlog-adp@verify-a5) | 6.382 | fits | 6 maap | 7 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-a1.service.srp.first.if0` (backlog-adp@verify-a1) | 4.292 | fits | 0 srp | 7 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-a2.service.srp.last.if1` (backlog-adp@verify-a2) | 17.246 | fits | 31 srp | 7 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@verify-7 | 0 | 17.898 | 17 | 183,824 (1.838) | yes | - |
| backlog-adp@verify-a0 | 1 | 18.284 | 19 | 182,927 (1.829) | yes | - |
| backlog-adp@verify-a1 | 0 | 19.199 | 22 | 183,766 (1.838) | yes | - |
| backlog-adp@verify-a2 | 0 | 18.620 | 21 | 171,831 (1.718) | yes | - |
| backlog-adp@verify-a3 | 0 | 18.057 | 18 | 195,535 (1.955) | yes | - |
| backlog-adp@verify-a4 | 0 | 18.263 | 19 | 188,866 (1.889) | yes | - |
| backlog-adp@verify-a5 | 0 | 18.121 | 18 | 195,418 (1.954) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@verify-7 | 1045 | 0 | 183,824 (1.838) | fits |
| backlog-adp@verify-a0 | 1145 | 0 | 182,927 (1.829) | fits |
| backlog-adp@verify-a1 | 1166 | 0 | 183,766 (1.838) | fits |
| backlog-adp@verify-a2 | 1183 | 0 | 171,831 (1.718) | fits |
| backlog-adp@verify-a3 | 1199 | 0 | 195,535 (1.955) | fits |
| backlog-adp@verify-a4 | 1218 | 0 | 188,866 (1.889) | fits |
| backlog-adp@verify-a5 | 1236 | 0 | 195,418 (1.954) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@verify-7 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a0 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a1 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a2 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a3 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a4 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-a5 | 546 | 122,002 (1.220) | 96,031 (0.960) |

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
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a0.adp_available.if0` | 421,784 | 4.218 | 20 | 20 | fits | 156,398 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-a0.service.adp.first.if0` | 111,225 | 1.112 | 20 | 200 | fits | 123,216 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-a0.service.adp.last.if0` | 566,414 | 5.664 | 20 | 200 | fits | 156,398 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a0.service.acmp.first.if0` | 112,137 | 1.121 | 20 | 20 | fits | 123,216 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a0.service.acmp.last.if0` | 784,514 | 7.845 | 20 | 20 | fits | 122,359 | 52 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-a0.service.aecp.first.if0` | 115,722 | 1.157 | 20 | 24 | fits | 123,216 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@verify-a0.service.aecp.last.if1` | 1,503,588 | 15.036 | 20 | 24 | fits | 71,032 | 37 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a0.service.maap.first.if0` | 114,682 | 1.147 | 20 | 50 | fits | 123,216 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a0.service.maap.last.if0` | 570,090 | 5.701 | 20 | 50 | fits | 156,398 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@verify-a0.service.srp.first.if0` | 413,627 | 4.136 | 18 | 18 | fits | 182,927 | 104 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp@verify-a0.service.srp.last.if1` | 1,690,900 | 16.909 | 18 | 18 | fits | 36,682 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a1.adp_available.if0` | 437,273 | 4.373 | 20 | 20 | fits | 156,453 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-a1.service.adp.first.if0` | 121,207 | 1.212 | 20 | 200 | fits | 118,660 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-a1.service.adp.last.if0` | 582,020 | 5.820 | 20 | 200 | fits | 156,453 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a1.service.acmp.first.if0` | 122,119 | 1.221 | 20 | 20 | fits | 118,660 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a1.service.acmp.last.if0` | 799,524 | 7.995 | 20 | 20 | fits | 127,692 | 52 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-a1.service.aecp.first.if0` | 125,704 | 1.257 | 20 | 24 | fits | 118,660 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@verify-a1.service.aecp.last.if1` | 1,490,428 | 14.904 | 20 | 24 | fits | 67,356 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a1.service.maap.first.if0` | 124,664 | 1.247 | 20 | 50 | fits | 118,660 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a1.service.maap.last.if0` | 585,696 | 5.857 | 20 | 50 | fits | 156,453 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@verify-a1.service.srp.first.if0` | 429,178 | 4.292 | 18 | 18 | fits | 183,766 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@verify-a1.service.srp.last.if1` | 1,697,174 | 16.972 | 18 | 18 | fits | 56,696 | 24 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a2.adp_available.if0` | 456,767 | 4.568 | 20 | 20 | fits | 155,810 | 83 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@verify-a2.service.adp.first.if0` | 115,627 | 1.156 | 20 | 200 | fits | 118,801 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-a2.service.adp.last.if0` | 601,255 | 6.013 | 20 | 200 | fits | 155,810 | 83 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a2.service.acmp.first.if0` | 116,539 | 1.165 | 20 | 20 | fits | 118,801 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a2.service.acmp.last.if0` | 819,607 | 8.196 | 20 | 20 | fits | 122,564 | 52 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@verify-a2.service.aecp.first.if0` | 120,124 | 1.201 | 20 | 24 | fits | 118,801 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-a2.service.aecp.last.if1` | 1,481,078 | 14.811 | 20 | 24 | fits | 41,680 | 33 | 0.679 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a2.service.maap.first.if0` | 119,084 | 1.191 | 20 | 50 | fits | 118,801 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a2.service.maap.last.if0` | 604,931 | 6.049 | 20 | 50 | fits | 155,810 | 83 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@verify-a2.service.srp.first.if0` | 277,225 | 2.772 | 18 | 18 | fits | 158,596 | 136 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-a2.service.srp.last.if1` | 1,724,552 | 17.246 | 18 | 18 | fits | 36,735 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a3.adp_available.if0` | 482,312 | 4.823 | 20 | 20 | fits | 154,381 | 83 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@verify-a3.service.adp.first.if0` | 127,023 | 1.270 | 20 | 200 | fits | 118,736 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-a3.service.adp.last.if0` | 625,442 | 6.254 | 20 | 200 | fits | 154,381 | 83 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a3.service.acmp.first.if0` | 127,935 | 1.279 | 20 | 20 | fits | 118,736 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a3.service.acmp.last.if0` | 869,351 | 8.694 | 20 | 20 | fits | 121,031 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-a3.service.aecp.first.if0` | 131,520 | 1.315 | 20 | 24 | fits | 118,736 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-a3.service.aecp.last.if1` | 1,567,930 | 15.679 | 20 | 24 | fits | 67,825 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a3.service.maap.first.if0` | 130,480 | 1.305 | 20 | 50 | fits | 118,736 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a3.service.maap.last.if0` | 629,118 | 6.291 | 20 | 50 | fits | 154,381 | 83 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-a3.service.srp.first.if0` | 325,560 | 3.256 | 18 | 18 | fits | 195,535 | 151 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@verify-a3.service.srp.last.if1` | 1,667,831 | 16.678 | 18 | 18 | fits | 50,451 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a4.adp_available.if0` | 467,899 | 4.679 | 20 | 20 | fits | 120,483 | 74 | 0.622 |
| ADP record released under the composed load, first | `backlog-adp@verify-a4.service.adp.first.if0` | 121,355 | 1.214 | 20 | 200 | fits | 118,725 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-a4.service.adp.last.if0` | 577,069 | 5.771 | 20 | 200 | fits | 120,483 | 74 | 0.622 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a4.service.acmp.first.if0` | 122,267 | 1.223 | 20 | 20 | fits | 118,725 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a4.service.acmp.last.if0` | 838,695 | 8.387 | 20 | 20 | fits | 132,990 | 64 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@verify-a4.service.aecp.first.if0` | 125,852 | 1.259 | 20 | 24 | fits | 118,725 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@verify-a4.service.aecp.last.if1` | 1,527,229 | 15.272 | 20 | 24 | fits | 41,593 | 33 | 0.675 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a4.service.maap.first.if0` | 124,812 | 1.248 | 20 | 50 | fits | 118,725 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a4.service.maap.last.if0` | 580,745 | 5.807 | 20 | 50 | fits | 120,483 | 74 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp@verify-a4.service.srp.first.if0` | 313,223 | 3.132 | 18 | 18 | fits | 188,866 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@verify-a4.service.srp.last.if1` | 1,688,514 | 16.885 | 18 | 18 | fits | 50,155 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-a5.adp_available.if0` | 490,963 | 4.910 | 20 | 20 | fits | 154,924 | 83 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@verify-a5.service.adp.first.if0` | 126,792 | 1.268 | 20 | 200 | fits | 118,725 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-a5.service.adp.last.if0` | 634,534 | 6.345 | 20 | 200 | fits | 154,924 | 83 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@verify-a5.service.acmp.first.if0` | 127,704 | 1.277 | 20 | 20 | fits | 118,725 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-a5.service.acmp.last.if0` | 878,666 | 8.787 | 20 | 20 | fits | 121,144 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-a5.service.aecp.first.if0` | 131,289 | 1.313 | 20 | 24 | fits | 118,725 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@verify-a5.service.aecp.last.if1` | 1,574,565 | 15.746 | 20 | 24 | fits | 67,351 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@verify-a5.service.maap.first.if0` | 130,249 | 1.302 | 20 | 50 | fits | 118,725 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@verify-a5.service.maap.last.if0` | 638,210 | 6.382 | 20 | 50 | fits | 154,924 | 83 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@verify-a5.service.srp.first.if0` | 325,212 | 3.252 | 18 | 18 | fits | 195,418 | 145 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-a5.service.srp.last.if1` | 1,674,286 | 16.743 | 18 | 18 | fits | 50,398 | 18 | 0.715 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
