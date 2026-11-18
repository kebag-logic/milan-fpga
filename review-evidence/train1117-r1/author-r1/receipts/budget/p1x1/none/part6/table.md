### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 17 paths and 0 of 126 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.079 (0.268) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.074 (0.253) | fits | 0 adp | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.247 (0.605) | fits | 0 events | 1 | 0 |
| READ_DESCRIPTOR held for a token (#917) | 0 | `aecp.held.read_descriptor.if0` (aecp-held) | 5.235 (5.547) | fits | 16 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.249 (4.613) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-2.adp_available.if0` (backlog-adp@blank-2) | 4.429 (5.941) | fits | 7 adp | 10 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.692 (2.112) | fits | 15 events | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.162 | fits | 0 acmp | 11 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-2.service.acmp.last.if0` (backlog-adp@blank-2) | 5.037 | fits | 11 acmp | 11 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.205 | fits | 0 adp | 11 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-2.service.adp.last.if0` (backlog-adp@blank-2) | 5.030 | fits | 7 adp | 11 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-2.service.aecp.first.if0` (backlog-adp@blank-2) | 2.216 | fits | 0 aecp | 11 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.188 | fits | 15 aecp | 11 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.188 | fits | 0 maap | 11 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-2.service.maap.last.if0` (backlog-adp@blank-2) | 5.067 | fits | 6 maap | 11 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 6.061 | fits | 0 srp | 11 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-6.service.srp.last.if0` (backlog-adp@blank-aged2-6) | 11.121 | fits | 31 srp | 11 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-2 | 0 | 13.815 | 12 | 153,370 (1.534) | yes | - |
| backlog-adp@blank-6 | 1 | 13.213 | 12 | 146,655 (1.467) | yes | - |
| backlog-adp@program-6 | 0 | 11.831 | 11 | 152,957 (1.530) | yes | - |
| backlog-adp@verify-6 | 0 | 13.538 | 11 | 152,657 (1.527) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 14.992 | 13 | 151,725 (1.517) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 15.250 | 14 | 151,466 (1.515) | yes | - |
| backlog-adp@program-aged2-6 | 1 | 13.971 | 13 | 150,379 (1.504) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 12.364 | 11 | 151,307 (1.513) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 14.865 | 12 | 151,519 (1.515) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 15.124 | 13 | 151,825 (1.518) | yes | - |
| backlog | 0 | 5.721 | 7 | 154,987 (1.550) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 154,987 CPU cycles (1.550 ms), backlog.
Over the windows that released their whole load only: 154,987 (1.550 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-2 | 483 | 0 | 153,370 (1.534) | fits |
| backlog-adp@blank-6 | 484 | 0 | 146,655 (1.467) | fits |
| backlog-adp@program-6 | 493 | 0 | 152,957 (1.530) | fits |
| backlog-adp@verify-6 | 499 | 0 | 152,657 (1.527) | fits |
| backlog-adp@blank-aged2-6 | 790 | 0 | 151,725 (1.517) | fits |
| backlog-adp@blank-aged1-6 | 730 | 0 | 151,466 (1.515) | fits |
| backlog-adp@program-aged2-6 | 818 | 0 | 151,393 (1.514) | fits |
| backlog-adp@program-aged1-6 | 755 | 0 | 151,307 (1.513) | fits |
| backlog-adp@verify-aged2-6 | 833 | 0 | 151,519 (1.515) | fits |
| backlog-adp@verify-aged1-6 | 773 | 0 | 151,825 (1.518) | fits |
| backlog | 286 | 0 | 154,987 (1.550) | fits |
| acmp-disc | 901 | 0 | 101,783 (1.018) | fits |
| aecp-held | 109 | 0 | 35,134 (0.351) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-6 | 2 | +4.467 ms, 77,223 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.121 (20) | 8.879 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.138 (20) | 9.862 |
| backlog-adp@program-aged2-6 | 2 | +4.381 ms, 80,520 (0.805 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.874 (20) | 9.126 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.210 (20) | 9.790 |
| backlog-adp@verify-aged2-6 | 2 | +4.289 ms, 77,773 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.950 (20) | 9.050 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.293 (20) | 9.707 |

Least margin over the aged windows: 8.879 ms, `backlog-adp@blank-aged2-6.service.srp.last.if0` at 11.121 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-2 | 342 | 92,500 (0.925) | 76,179 (0.762) |
| backlog-adp@blank-6 | 342 | 91,668 (0.917) | 76,234 (0.762) |
| backlog-adp@program-6 | 373 | 95,349 (0.953) | 78,491 (0.785) |
| backlog-adp@verify-6 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@blank-aged2-6 | 341 | 92,162 (0.922) | 76,166 (0.762) |
| backlog-adp@blank-aged1-6 | 341 | 93,285 (0.933) | 76,454 (0.765) |
| backlog-adp@program-aged2-6 | 371 | 95,496 (0.955) | 78,485 (0.785) |
| backlog-adp@program-aged1-6 | 368 | 95,708 (0.957) | 78,835 (0.788) |
| backlog-adp@verify-aged2-6 | 399 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@verify-aged1-6 | 399 | 94,984 (0.950) | 78,276 (0.783) |
| backlog | 265 | 22,571 (0.226) | 2,593 (0.026) |
| acmp-disc | 398 | 101,783 (1.018) | 78,276 (0.783) |
| aecp-held | 98 | 22,571 (0.226) | 2,593 (0.026) |

Longest pass that carries a step: 101,783 CPU cycles (1.018 ms), acmp-disc; longest step: 78,835 (0.788 ms), backlog-adp@program-aged1-6.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 442,933 | 4.429 | 20 | 20 | fits | 125,344 | 181 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 378,246 | 3.782 | 20 | 200 | fits | 149,967 | 220 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 502,974 | 5.030 | 20 | 200 | fits | 125,344 | 181 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 379,170 | 3.792 | 20 | 20 | fits | 149,967 | 220 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 503,678 | 5.037 | 20 | 20 | fits | 125,344 | 181 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 221,582 | 2.216 | 20 | 24 | fits | 153,370 | 156 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 381,820 | 3.818 | 20 | 24 | fits | 149,967 | 220 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 381,754 | 3.818 | 20 | 50 | fits | 149,967 | 220 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 506,702 | 5.067 | 20 | 50 | fits | 125,344 | 181 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 590,833 | 5.908 | 20 | 20 | fits | 84,197 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,104,249 | 11.042 | 20 | 20 | fits | 81,599 | 31 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 369,128 | 3.691 | 20 | 20 | fits | 132,423 | 202 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 297,344 | 2.973 | 20 | 200 | fits | 146,655 | 208 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 429,151 | 4.292 | 20 | 200 | fits | 132,423 | 202 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 298,268 | 2.983 | 20 | 20 | fits | 146,655 | 208 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 429,855 | 4.299 | 20 | 20 | fits | 132,423 | 202 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 143,842 | 1.438 | 20 | 24 | fits | 145,885 | 146 | 0.447 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 300,918 | 3.009 | 20 | 24 | fits | 146,655 | 208 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 300,852 | 3.009 | 20 | 50 | fits | 146,655 | 208 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 432,879 | 4.329 | 20 | 50 | fits | 132,423 | 202 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 517,010 | 5.170 | 20 | 20 | fits | 84,197 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,024,586 | 10.246 | 20 | 20 | fits | 75,759 | 25 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 393,985 | 3.940 | 20 | 20 | fits | 119,642 | 184 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 327,472 | 3.275 | 20 | 200 | fits | 150,917 | 209 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 446,498 | 4.465 | 20 | 200 | fits | 119,642 | 184 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 328,396 | 3.284 | 20 | 20 | fits | 150,917 | 209 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 447,202 | 4.472 | 20 | 20 | fits | 119,642 | 184 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 181,119 | 1.811 | 20 | 24 | fits | 152,957 | 155 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 331,046 | 3.310 | 20 | 24 | fits | 150,917 | 209 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 330,980 | 3.310 | 20 | 50 | fits | 150,917 | 209 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 450,226 | 4.502 | 20 | 50 | fits | 119,642 | 184 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 534,893 | 5.349 | 20 | 20 | fits | 84,733 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,041,300 | 10.413 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 412,093 | 4.121 | 20 | 20 | fits | 113,487 | 163 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 359,287 | 3.593 | 20 | 200 | fits | 149,259 | 226 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 472,158 | 4.722 | 20 | 200 | fits | 113,487 | 163 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 360,211 | 3.602 | 20 | 20 | fits | 149,259 | 226 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 472,862 | 4.729 | 20 | 20 | fits | 113,487 | 163 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 214,592 | 2.146 | 20 | 24 | fits | 152,657 | 155 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 362,861 | 3.629 | 20 | 24 | fits | 149,259 | 226 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 362,795 | 3.628 | 20 | 50 | fits | 149,259 | 226 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 475,886 | 4.759 | 20 | 50 | fits | 113,487 | 163 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 560,503 | 5.605 | 20 | 20 | fits | 84,683 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,073,395 | 10.734 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 372,847 | 3.728 | 20 | 20 | fits | 130,092 | 178 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 311,870 | 3.119 | 20 | 200 | fits | 144,845 | 224 | 0.439 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 441,346 | 4.413 | 20 | 200 | fits | 130,092 | 178 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 312,794 | 3.128 | 20 | 20 | fits | 144,845 | 224 | 0.439 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 442,050 | 4.420 | 20 | 20 | fits | 130,092 | 178 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 160,980 | 1.610 | 20 | 24 | fits | 151,725 | 153 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 315,444 | 3.154 | 20 | 24 | fits | 144,845 | 224 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 315,378 | 3.154 | 20 | 50 | fits | 144,845 | 224 | 0.439 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 445,074 | 4.451 | 20 | 50 | fits | 130,092 | 178 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 606,069 | 6.061 | 20 | 20 | fits | 83,838 | 25 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,112,109 | 11.121 | 20 | 20 | fits | 73,298 | 24 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 377,438 | 3.774 | 20 | 20 | fits | 127,069 | 176 | 0.484 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 301,141 | 3.011 | 20 | 200 | fits | 148,620 | 227 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 438,918 | 4.389 | 20 | 200 | fits | 127,069 | 176 | 0.484 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 302,065 | 3.021 | 20 | 20 | fits | 148,620 | 227 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 439,622 | 4.396 | 20 | 20 | fits | 127,069 | 176 | 0.484 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 157,085 | 1.571 | 20 | 24 | fits | 151,466 | 152 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 304,715 | 3.047 | 20 | 24 | fits | 148,620 | 227 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 304,649 | 3.046 | 20 | 50 | fits | 148,620 | 227 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 442,646 | 4.426 | 20 | 50 | fits | 127,069 | 176 | 0.484 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 526,941 | 5.269 | 20 | 20 | fits | 84,361 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,013,843 | 10.138 | 20 | 20 | fits | 59,768 | 20 | 0.683 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 378,975 | 3.790 | 20 | 20 | fits | 127,010 | 175 | 0.484 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 294,988 | 2.950 | 20 | 200 | fits | 150,379 | 232 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 432,736 | 4.327 | 20 | 200 | fits | 127,010 | 175 | 0.484 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 295,912 | 2.959 | 20 | 20 | fits | 150,379 | 232 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 433,440 | 4.334 | 20 | 20 | fits | 127,010 | 175 | 0.484 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 149,173 | 1.492 | 20 | 24 | fits | 151,393 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 298,562 | 2.986 | 20 | 24 | fits | 150,379 | 232 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 298,496 | 2.985 | 20 | 50 | fits | 150,379 | 232 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 436,464 | 4.365 | 20 | 50 | fits | 127,010 | 175 | 0.484 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 600,316 | 6.003 | 20 | 20 | fits | 83,398 | 25 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,087,398 | 10.874 | 20 | 20 | fits | 59,768 | 20 | 0.683 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 374,945 | 3.749 | 20 | 20 | fits | 122,233 | 172 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 305,002 | 3.050 | 20 | 200 | fits | 147,807 | 222 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 426,619 | 4.266 | 20 | 200 | fits | 122,233 | 172 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 305,926 | 3.059 | 20 | 20 | fits | 147,807 | 222 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 427,323 | 4.273 | 20 | 20 | fits | 122,233 | 172 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 161,759 | 1.618 | 20 | 24 | fits | 151,307 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 308,576 | 3.086 | 20 | 24 | fits | 147,807 | 222 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 308,510 | 3.085 | 20 | 50 | fits | 147,807 | 222 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 430,347 | 4.303 | 20 | 50 | fits | 122,233 | 172 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 514,560 | 5.146 | 20 | 20 | fits | 84,279 | 25 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,020,986 | 10.210 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 362,999 | 3.630 | 20 | 20 | fits | 122,326 | 169 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 301,796 | 3.018 | 20 | 200 | fits | 148,342 | 226 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 423,506 | 4.235 | 20 | 200 | fits | 122,326 | 169 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 302,720 | 3.027 | 20 | 20 | fits | 148,342 | 226 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 424,210 | 4.242 | 20 | 20 | fits | 122,326 | 169 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 158,018 | 1.580 | 20 | 24 | fits | 151,519 | 152 | 0.421 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 305,370 | 3.054 | 20 | 24 | fits | 148,342 | 226 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 305,304 | 3.053 | 20 | 50 | fits | 148,342 | 226 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 427,234 | 4.272 | 20 | 50 | fits | 122,326 | 169 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 588,409 | 5.884 | 20 | 20 | fits | 83,468 | 25 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,094,950 | 10.950 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 367,124 | 3.671 | 20 | 20 | fits | 129,524 | 190 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 305,876 | 3.059 | 20 | 200 | fits | 146,020 | 209 | 0.450 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 434,784 | 4.348 | 20 | 200 | fits | 129,524 | 190 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 306,800 | 3.068 | 20 | 20 | fits | 146,020 | 209 | 0.450 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 435,488 | 4.355 | 20 | 20 | fits | 129,524 | 190 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 153,650 | 1.536 | 20 | 24 | fits | 151,825 | 153 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 309,450 | 3.095 | 20 | 24 | fits | 146,020 | 209 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 309,384 | 3.094 | 20 | 50 | fits | 146,020 | 209 | 0.450 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 438,512 | 4.385 | 20 | 50 | fits | 129,524 | 190 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 522,804 | 5.228 | 20 | 20 | fits | 84,358 | 24 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,029,254 | 10.293 | 20 | 20 | fits | 66,490 | 27 | 0.756 |
| an event behind 15 others | `backlog.event.if0` | 169,181 | 1.692 | 20 | 200 | fits | 56,240 | 78 | 0.578 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 424,854 | 4.249 | 20 | 20 | fits | 40,609 | 63 | 0.297 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 420,515 | 4.205 | 20 | 200 | fits | 148,859 | 158 | 0.406 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 419,899 | 4.199 | 20 | 200 | fits | 148,859 | 158 | 0.406 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 416,193 | 4.162 | 20 | 20 | fits | 148,859 | 158 | 0.406 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 455,966 | 4.560 | 20 | 20 | fits | 40,609 | 63 | 0.297 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 154,096 | 1.541 | 20 | 24 | fits | 154,987 | 158 | 0.441 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 418,843 | 4.188 | 20 | 24 | fits | 148,859 | 158 | 0.406 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 418,777 | 4.188 | 20 | 50 | fits | 148,859 | 158 | 0.406 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 418,381 | 4.184 | 20 | 50 | fits | 148,859 | 158 | 0.406 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 458,924 | 4.589 | 20 | 20 | fits | 40,609 | 63 | 0.297 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 519,757 | 5.198 | 20 | 20 | fits | 24,886 | 41 | 0.158 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,424 | 0.074 | 20 | 20 | fits | 25,334 | 13 (29) | 0.785 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,917 | 0.079 | 20 | 20 | fits | 26,832 | 19 (35) | 0.781 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 24,721 | 0.247 | 20 | 20 | fits | 30,420 | 21 (12) | 0.821 |
| READ_DESCRIPTOR held for a token (#917) | `aecp.held.read_descriptor.if0` | 523,517 | 5.235 | 20 | 24 | fits | 30,695 | 17 | 0.714 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
