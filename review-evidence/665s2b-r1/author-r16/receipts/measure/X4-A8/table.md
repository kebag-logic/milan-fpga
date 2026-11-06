### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 22 paths and 6 of 587 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.021 (7.745) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 6.619 (8.078) | fits | 7 adp | 49 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.239 (0.763) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.497 (2.539) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.585 (64.140) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.401 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 8.372 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.748 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 11.113 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 5.268 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 14.964 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.728 | fits | 0 acmp | 52 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.acmp.last.if0` (backlog-adp@blank-aged2-7) | 10.076 | fits | 11 acmp | 52 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.719 | fits | 0 adp | 52 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 7.918 | fits | 7 adp | 50 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 6.617 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.764 | fits | 0 aecp | 52 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.852 | MISS ceiling | 15 aecp | 52 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.753 | fits | 0 maap | 52 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 6.550 | fits | 6 maap | 52 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.406 | fits | 0 srp | 52 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-aged2-5.service.srp.last.if1` (backlog-adp@verify-aged2-5) | 17.543 | fits | 31 srp | 52 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.701 | 23 | 187,042 (1.870) | yes | - |
| backlog-adp@blank-1 | 0 | 17.909 | 21 | 186,932 (1.869) | yes | - |
| backlog-adp@blank-2 | 0 | 18.756 | 21 | 187,148 (1.871) | yes | - |
| backlog-adp@blank-3 | 0 | 18.261 | 23 | 181,423 (1.814) | yes | - |
| backlog-adp@blank-4 | 0 | 17.831 | 20 | 188,473 (1.885) | yes | - |
| backlog-adp@blank-5 | 0 | 17.732 | 21 | 186,824 (1.868) | yes | - |
| backlog-adp@blank-6 | 0 | 17.660 | 21 | 161,686 (1.617) | yes | - |
| backlog-adp@blank-7 | 0 | 18.222 | 22 | 161,895 (1.619) | yes | - |
| backlog-adp@program-0 | 0 | 17.729 | 21 | 187,473 (1.875) | yes | - |
| backlog-adp@program-1 | 0 | 17.983 | 20 | 185,362 (1.854) | yes | - |
| backlog-adp@program-2 | 0 | 18.084 | 22 | 185,792 (1.858) | yes | - |
| backlog-adp@program-3 | 0 | 18.080 | 22 | 180,226 (1.802) | yes | - |
| backlog-adp@program-4 | 0 | 16.622 | 20 | 185,760 (1.858) | yes | - |
| backlog-adp@program-5 | 0 | 18.160 | 22 | 185,622 (1.856) | yes | - |
| backlog-adp@program-6 | 0 | 17.417 | 22 | 149,905 (1.499) | yes | - |
| backlog-adp@program-7 | 0 | 16.864 | 20 | 161,741 (1.617) | yes | - |
| backlog-adp@verify-0 | 0 | 18.129 | 21 | 186,893 (1.869) | yes | - |
| backlog-adp@verify-1 | 0 | 19.264 | 23 | 181,287 (1.813) | yes | - |
| backlog-adp@verify-2 | 0 | 18.155 | 21 | 188,121 (1.881) | yes | - |
| backlog-adp@verify-3 | 0 | 18.223 | 22 | 186,541 (1.865) | yes | - |
| backlog-adp@verify-4 | 0 | 18.680 | 23 | 186,626 (1.866) | yes | - |
| backlog-adp@verify-5 | 0 | 18.633 | 23 | 156,467 (1.565) | yes | - |
| backlog-adp@verify-6 | 0 | 18.659 | 23 | 161,487 (1.615) | yes | - |
| backlog-adp@verify-7 | 1 | 18.158 | 20 | 164,999 (1.650) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 17.761 | 22 | 187,408 (1.874) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 17.380 | 20 | 187,408 (1.874) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 18.867 | 22 | 187,046 (1.870) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 18.780 | 21 | 186,865 (1.869) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 19.258 | 23 | 186,865 (1.869) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 18.974 | 23 | 186,947 (1.869) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 18.653 | 22 | 164,387 (1.644) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 18.413 | 20 | 164,470 (1.645) | yes | - |
| backlog-adp@program-aged2-0 | 1 | 18.213 | 21 | 186,357 (1.864) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 17.667 | 20 | 185,457 (1.855) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 18.043 | 20 | 186,328 (1.863) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 18.000 | 21 | 180,161 (1.802) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 17.903 | 21 | 186,853 (1.869) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 17.706 | 20 | 185,854 (1.859) | yes | - |
| backlog-adp@program-aged2-6 | 1 | 17.940 | 21 | 161,446 (1.614) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 18.028 | 22 | 161,483 (1.615) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 18.001 | 21 | 188,263 (1.883) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 18.142 | 22 | 186,808 (1.868) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 18.902 | 21 | 186,808 (1.868) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 18.856 | 21 | 186,270 (1.863) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 18.859 | 20 | 186,482 (1.865) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 19.622 | 24 | 186,482 (1.865) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 19.162 | 22 | 159,861 (1.599) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 19.180 | 22 | 161,508 (1.615) | yes | - |
| backlog | 0 | 14.563 | 21 | 158,934 (1.589) | yes | - |
| backlog-adp | 0 | 17.510 | 24 | 160,777 (1.608) | yes | - |
| backlog-adp-refill | 0 | 41.136 | 34 | 140,167 (1.402) | yes | - |
| backlog-owed | 0 | 360.452 | 66 | 158,631 (1.586) | yes | - |

Composed maximum over the 4 backlog windows: 160,777 CPU cycles (1.608 ms), backlog-adp.
Over the windows that released their whole load only: 160,777 (1.608 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 8631 | 0 | 165,605 (1.656) | fits |
| save-starved | 55521 | 0 | 168,439 (1.684) | fits |
| backlog-adp@blank-0 | 555 | 0 | 187,042 (1.870) | fits |
| backlog-adp@blank-1 | 553 | 0 | 186,932 (1.869) | fits |
| backlog-adp@blank-2 | 553 | 0 | 187,148 (1.871) | fits |
| backlog-adp@blank-3 | 555 | 0 | 181,423 (1.814) | fits |
| backlog-adp@blank-4 | 552 | 0 | 188,473 (1.885) | fits |
| backlog-adp@blank-5 | 555 | 0 | 186,824 (1.868) | fits |
| backlog-adp@blank-6 | 555 | 0 | 161,686 (1.617) | fits |
| backlog-adp@blank-7 | 556 | 0 | 161,895 (1.619) | fits |
| backlog-adp@program-0 | 901 | 0 | 187,473 (1.875) | fits |
| backlog-adp@program-1 | 903 | 0 | 185,362 (1.854) | fits |
| backlog-adp@program-2 | 904 | 0 | 185,792 (1.858) | fits |
| backlog-adp@program-3 | 904 | 0 | 180,226 (1.802) | fits |
| backlog-adp@program-4 | 904 | 0 | 185,760 (1.858) | fits |
| backlog-adp@program-5 | 906 | 0 | 185,622 (1.856) | fits |
| backlog-adp@program-6 | 906 | 0 | 149,905 (1.499) | fits |
| backlog-adp@program-7 | 906 | 0 | 161,741 (1.617) | fits |
| backlog-adp@verify-0 | 1240 | 0 | 186,893 (1.869) | fits |
| backlog-adp@verify-1 | 1242 | 0 | 181,287 (1.813) | fits |
| backlog-adp@verify-2 | 1240 | 0 | 188,121 (1.881) | fits |
| backlog-adp@verify-3 | 1243 | 0 | 186,541 (1.865) | fits |
| backlog-adp@verify-4 | 1244 | 0 | 186,626 (1.866) | fits |
| backlog-adp@verify-5 | 1244 | 0 | 156,467 (1.565) | fits |
| backlog-adp@verify-6 | 1244 | 0 | 161,487 (1.615) | fits |
| backlog-adp@verify-7 | 1242 | 0 | 164,999 (1.650) | fits |
| backlog-adp@blank-aged2-0 | 803 | 0 | 187,408 (1.874) | fits |
| backlog-adp@blank-aged2-1 | 807 | 0 | 187,408 (1.874) | fits |
| backlog-adp@blank-aged2-2 | 816 | 0 | 187,046 (1.870) | fits |
| backlog-adp@blank-aged2-3 | 822 | 0 | 186,865 (1.869) | fits |
| backlog-adp@blank-aged2-4 | 830 | 0 | 186,865 (1.869) | fits |
| backlog-adp@blank-aged2-5 | 837 | 0 | 186,947 (1.869) | fits |
| backlog-adp@blank-aged2-6 | 842 | 0 | 164,387 (1.644) | fits |
| backlog-adp@blank-aged2-7 | 847 | 0 | 164,470 (1.645) | fits |
| backlog-adp@program-aged2-0 | 1149 | 0 | 186,357 (1.864) | fits |
| backlog-adp@program-aged2-1 | 1154 | 0 | 185,457 (1.855) | fits |
| backlog-adp@program-aged2-2 | 1161 | 0 | 186,328 (1.863) | fits |
| backlog-adp@program-aged2-3 | 1168 | 0 | 180,161 (1.802) | fits |
| backlog-adp@program-aged2-4 | 1175 | 0 | 186,853 (1.869) | fits |
| backlog-adp@program-aged2-5 | 1180 | 0 | 185,854 (1.859) | fits |
| backlog-adp@program-aged2-6 | 1188 | 0 | 161,446 (1.614) | fits |
| backlog-adp@program-aged2-7 | 1195 | 0 | 161,483 (1.615) | fits |
| backlog-adp@verify-aged2-0 | 1490 | 0 | 188,263 (1.883) | fits |
| backlog-adp@verify-aged2-1 | 1498 | 0 | 186,808 (1.868) | fits |
| backlog-adp@verify-aged2-2 | 1503 | 0 | 186,808 (1.868) | fits |
| backlog-adp@verify-aged2-3 | 1510 | 0 | 186,270 (1.863) | fits |
| backlog-adp@verify-aged2-4 | 1516 | 0 | 186,482 (1.865) | fits |
| backlog-adp@verify-aged2-5 | 1526 | 0 | 186,482 (1.865) | fits |
| backlog-adp@verify-aged2-6 | 1531 | 0 | 159,861 (1.599) | fits |
| backlog-adp@verify-aged2-7 | 1537 | 0 | 161,508 (1.615) | fits |
| save | 625 | 0 | 126,668 (1.267) | fits |
| backlog | 309 | 0 | 158,934 (1.589) | fits |
| backlog-adp | 337 | 0 | 160,777 (1.608) | fits |
| backlog-adp-refill | 347 | 0 | 140,167 (1.402) | fits |
| backlog-owed | 365 | 0 | 158,631 (1.586) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +10.200 ms, 78,639 (0.786 ms), read-back | none | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 17.112 (18) | 0.888 |
| backlog-adp@blank-aged2-1 | 2 | +9.010 ms, 78,671 (0.787 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 16.727 (18) | 1.273 |
| backlog-adp@blank-aged2-2 | 2 | +7.995 ms, 79,119 (0.791 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 17.467 (18) | 0.533 |
| backlog-adp@blank-aged2-3 | 2 | +6.935 ms, 85,709 (0.857 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 17.103 (18) | 0.897 |
| backlog-adp@blank-aged2-4 | 2 | +5.559 ms, 79,011 (0.790 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 17.020 (18) | 0.980 |
| backlog-adp@blank-aged2-5 | 2 | +4.223 ms, 79,026 (0.790 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 17.086 (18) | 0.914 |
| backlog-adp@blank-aged2-6 | 2 | +3.582 ms, 85,488 (0.855 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 17.241 (18) | 0.759 |
| backlog-adp@blank-aged2-7 | 2 | +2.613 ms, 85,695 (0.857 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 16.998 (18) | 1.002 |
| backlog-adp@program-aged2-0 | 2 | +10.081 ms, 84,782 (0.848 ms), issue | none | `backlog-adp@program-aged2-0.service.srp.last.if1` | 16.742 (18) | 1.258 |
| backlog-adp@program-aged2-1 | 2 | +9.085 ms, 84,756 (0.848 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if1` | 16.747 (18) | 1.253 |
| backlog-adp@program-aged2-2 | 2 | +8.130 ms, 85,135 (0.851 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if1` | 16.789 (18) | 1.211 |
| backlog-adp@program-aged2-3 | 2 | +6.761 ms, 85,080 (0.851 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if1` | 17.024 (18) | 0.976 |
| backlog-adp@program-aged2-4 | 2 | +5.612 ms, 85,080 (0.851 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if1` | 17.194 (18) | 0.806 |
| backlog-adp@program-aged2-5 | 2 | +4.276 ms, 84,988 (0.850 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if1` | 16.997 (18) | 1.003 |
| backlog-adp@program-aged2-6 | 2 | +3.629 ms, 85,032 (0.850 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if1` | 17.234 (18) | 0.766 |
| backlog-adp@program-aged2-7 | 2 | +2.664 ms, 85,033 (0.850 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if1` | 17.322 (18) | 0.678 |
| backlog-adp@verify-aged2-0 | 2 | +10.332 ms, 79,625 (0.796 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 17.350 (18) | 0.650 |
| backlog-adp@verify-aged2-1 | 2 | +8.923 ms, 79,678 (0.797 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 17.491 (18) | 0.509 |
| backlog-adp@verify-aged2-2 | 2 | +8.150 ms, 79,964 (0.800 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 17.482 (18) | 0.518 |
| backlog-adp@verify-aged2-3 | 2 | +6.987 ms, 80,076 (0.801 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 17.433 (18) | 0.567 |
| backlog-adp@verify-aged2-4 | 2 | +5.665 ms, 79,909 (0.799 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 17.434 (18) | 0.566 |
| backlog-adp@verify-aged2-5 | 2 | +5.207 ms, 79,992 (0.800 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 17.543 (18) | 0.457 |
| backlog-adp@verify-aged2-6 | 2 | +3.674 ms, 79,827 (0.798 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 17.472 (18) | 0.528 |
| backlog-adp@verify-aged2-7 | 2 | +2.508 ms, 79,909 (0.799 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 17.492 (18) | 0.508 |

Least margin over the aged windows: 0.457 ms, `backlog-adp@verify-aged2-5.service.srp.last.if1` at 17.543 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4696.875 | 12,110 | 370 | - | 19.075 | no | within |
| save-starved | 12086.944 | 12,110 | 370 | - | 31.006 | yes | within |
| save | 4697.241 | 12,110 | 370 | - | 11.185 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1526 | 127,657 (1.277) | 96,080 (0.961) |
| save-starved | 686 | 98,174 (0.982) | 96,168 (0.962) |
| backlog-adp@blank-0 | 337 | 99,862 (0.999) | 76,139 (0.761) |
| backlog-adp@blank-1 | 337 | 100,248 (1.002) | 76,139 (0.761) |
| backlog-adp@blank-2 | 338 | 107,249 (1.072) | 76,139 (0.761) |
| backlog-adp@blank-3 | 337 | 106,812 (1.068) | 76,139 (0.761) |
| backlog-adp@blank-4 | 337 | 107,249 (1.072) | 76,139 (0.761) |
| backlog-adp@blank-5 | 337 | 99,862 (0.999) | 76,139 (0.761) |
| backlog-adp@blank-6 | 337 | 100,248 (1.002) | 76,139 (0.761) |
| backlog-adp@blank-7 | 337 | 100,248 (1.002) | 76,139 (0.761) |
| backlog-adp@program-0 | 443 | 123,393 (1.234) | 82,112 (0.821) |
| backlog-adp@program-1 | 444 | 123,393 (1.234) | 82,137 (0.821) |
| backlog-adp@program-2 | 443 | 123,393 (1.234) | 82,112 (0.821) |
| backlog-adp@program-3 | 443 | 123,393 (1.234) | 82,112 (0.821) |
| backlog-adp@program-4 | 444 | 123,393 (1.234) | 81,828 (0.818) |
| backlog-adp@program-5 | 445 | 123,393 (1.234) | 81,828 (0.818) |
| backlog-adp@program-6 | 444 | 123,393 (1.234) | 81,828 (0.818) |
| backlog-adp@program-7 | 444 | 123,393 (1.234) | 81,828 (0.818) |
| backlog-adp@verify-0 | 546 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-1 | 547 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-2 | 546 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-3 | 546 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-4 | 546 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-5 | 546 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-6 | 546 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-7 | 546 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@blank-aged2-0 | 335 | 78,639 (0.786) | 76,245 (0.762) |
| backlog-adp@blank-aged2-1 | 335 | 78,671 (0.787) | 76,189 (0.762) |
| backlog-adp@blank-aged2-2 | 336 | 98,762 (0.988) | 76,502 (0.765) |
| backlog-adp@blank-aged2-3 | 336 | 106,863 (1.069) | 76,477 (0.765) |
| backlog-adp@blank-aged2-4 | 336 | 100,248 (1.002) | 76,477 (0.765) |
| backlog-adp@blank-aged2-5 | 336 | 101,809 (1.018) | 76,477 (0.765) |
| backlog-adp@blank-aged2-6 | 336 | 99,927 (0.999) | 76,477 (0.765) |
| backlog-adp@blank-aged2-7 | 336 | 100,248 (1.002) | 76,477 (0.765) |
| backlog-adp@program-aged2-0 | 441 | 123,393 (1.234) | 82,028 (0.820) |
| backlog-adp@program-aged2-1 | 441 | 123,393 (1.234) | 81,972 (0.820) |
| backlog-adp@program-aged2-2 | 442 | 123,393 (1.234) | 82,285 (0.823) |
| backlog-adp@program-aged2-3 | 442 | 123,393 (1.234) | 82,260 (0.823) |
| backlog-adp@program-aged2-4 | 442 | 123,393 (1.234) | 82,260 (0.823) |
| backlog-adp@program-aged2-5 | 442 | 123,393 (1.234) | 82,260 (0.823) |
| backlog-adp@program-aged2-6 | 442 | 123,393 (1.234) | 82,260 (0.823) |
| backlog-adp@program-aged2-7 | 442 | 123,393 (1.234) | 82,260 (0.823) |
| backlog-adp@verify-aged2-0 | 546 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-aged2-1 | 546 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-aged2-2 | 547 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-aged2-3 | 547 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-aged2-4 | 547 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-aged2-5 | 547 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-aged2-6 | 547 | 123,393 (1.234) | 95,894 (0.959) |
| backlog-adp@verify-aged2-7 | 547 | 123,393 (1.234) | 95,894 (0.959) |
| save | 585 | 126,668 (1.267) | 95,725 (0.957) |
| backlog | 266 | 50,296 (0.503) | 2,805 (0.028) |
| backlog-adp | 271 | 50,296 (0.503) | 2,673 (0.027) |
| backlog-adp-refill | 273 | 50,296 (0.503) | 2,673 (0.027) |
| backlog-owed | 305 | 50,296 (0.503) | 2,740 (0.027) |

Longest pass that carries a step: 127,657 CPU cycles (1.277 ms), save-held; longest step: 96,168 (0.962 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 466,272 | 4.663 | 20 | 200 | fits | 121,224 | 85 | 0.559 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 818,283 | 8.183 | 20 | 20 | fits | 94,384 | 39 | 0.730 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 1,051,750 | 10.518 | 20 | 24 | fits | 30,041 | 23 | 0.561 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 515,341 | 5.153 | 20 | 50 | fits | 108,681 | 56 | 0.644 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 1,448,300 | 14.483 | 18 | 18 | fits | 51,359 | 28 | 0.736 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 474,759 | 4.748 | 20 | 200 | fits | 124,061 | 91 | 0.579 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 837,157 | 8.372 | 20 | 20 | fits | 97,241 | 45 | 0.736 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 1,111,332 | 11.113 | 20 | 24 | fits | 38,778 | 35 | 0.586 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 526,815 | 5.268 | 20 | 50 | fits | 111,668 | 62 | 0.660 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,496,428 | 14.964 | 18 | 18 | fits | 54,000 | 34 | 0.741 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 514,682 | 5.147 | 20 | 20 | fits | 119,600 | 75 | 0.624 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 171,856 | 1.719 | 20 | 200 | fits | 119,479 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 622,122 | 6.221 | 20 | 200 | fits | 119,600 | 75 | 0.624 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 172,768 | 1.728 | 20 | 20 | fits | 119,479 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 863,294 | 8.633 | 20 | 20 | fits | 119,298 | 47 | 0.691 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 176,353 | 1.764 | 20 | 24 | fits | 119,479 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,490,538 | 14.905 | 20 | 24 | fits | 64,995 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 175,313 | 1.753 | 20 | 50 | fits | 119,479 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 625,798 | 6.258 | 20 | 50 | fits | 119,600 | 75 | 0.624 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 361,900 | 3.619 | 18 | 18 | fits | 187,042 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,663,208 | 16.632 | 18 | 18 | fits | 34,053 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 451,030 | 4.510 | 20 | 20 | fits | 155,217 | 90 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 119,393 | 1.194 | 20 | 200 | fits | 118,258 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 591,628 | 5.916 | 20 | 200 | fits | 155,217 | 90 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 120,305 | 1.203 | 20 | 20 | fits | 118,258 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 832,226 | 8.322 | 20 | 20 | fits | 119,192 | 47 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 123,890 | 1.239 | 20 | 24 | fits | 118,258 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,492,050 | 14.921 | 20 | 24 | fits | 65,095 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 122,850 | 1.228 | 20 | 50 | fits | 118,258 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 595,304 | 5.953 | 20 | 50 | fits | 155,217 | 90 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 309,327 | 3.093 | 18 | 18 | fits | 186,932 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,583,860 | 15.839 | 18 | 18 | fits | 46,518 | 18 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 468,485 | 4.685 | 20 | 20 | fits | 153,200 | 84 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 121,702 | 1.217 | 20 | 200 | fits | 118,258 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 609,126 | 6.091 | 20 | 200 | fits | 153,200 | 84 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 122,614 | 1.226 | 20 | 20 | fits | 118,258 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 915,566 | 9.156 | 20 | 20 | fits | 97,094 | 39 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 126,199 | 1.262 | 20 | 24 | fits | 118,258 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,507,729 | 15.077 | 20 | 24 | fits | 65,559 | 32 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 125,159 | 1.252 | 20 | 50 | fits | 118,258 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 612,802 | 6.128 | 20 | 50 | fits | 153,200 | 84 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 311,852 | 3.119 | 18 | 18 | fits | 187,148 | 141 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,603,702 | 16.037 | 18 | 18 | fits | 46,821 | 19 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 432,100 | 4.321 | 20 | 20 | fits | 154,400 | 84 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 124,011 | 1.240 | 20 | 200 | fits | 118,258 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 573,487 | 5.735 | 20 | 200 | fits | 154,400 | 84 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 124,923 | 1.249 | 20 | 20 | fits | 118,258 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 892,784 | 8.928 | 20 | 20 | fits | 97,047 | 39 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 128,508 | 1.285 | 20 | 24 | fits | 118,258 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,454,889 | 14.549 | 20 | 24 | fits | 67,036 | 38 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 127,468 | 1.275 | 20 | 50 | fits | 118,258 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 577,163 | 5.772 | 20 | 50 | fits | 154,400 | 84 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 422,698 | 4.227 | 18 | 18 | fits | 181,423 | 105 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,658,201 | 16.582 | 18 | 18 | fits | 34,804 | 16 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 583,916 | 5.839 | 20 | 20 | fits | 140,110 | 57 | 0.702 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 126,481 | 1.265 | 20 | 200 | fits | 118,419 | 141 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 713,794 | 7.138 | 20 | 200 | fits | 140,110 | 57 | 0.702 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 127,393 | 1.274 | 20 | 20 | fits | 118,419 | 141 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 930,998 | 9.310 | 20 | 20 | fits | 97,214 | 39 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 130,978 | 1.310 | 20 | 24 | fits | 118,419 | 141 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,522,165 | 15.222 | 20 | 24 | fits | 59,051 | 33 | 0.758 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 129,938 | 1.299 | 20 | 50 | fits | 118,419 | 141 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 577,360 | 5.774 | 20 | 50 | fits | 104,342 | 64 | 0.722 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 317,956 | 3.180 | 18 | 18 | fits | 188,473 | 146 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,614,854 | 16.149 | 18 | 18 | fits | 46,880 | 19 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 562,010 | 5.620 | 20 | 20 | fits | 140,689 | 57 | 0.703 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 118,174 | 1.182 | 20 | 200 | fits | 117,764 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 692,073 | 6.921 | 20 | 200 | fits | 140,689 | 57 | 0.703 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 119,086 | 1.191 | 20 | 20 | fits | 117,764 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 876,621 | 8.766 | 20 | 20 | fits | 97,322 | 46 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 122,671 | 1.227 | 20 | 24 | fits | 117,764 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,459,463 | 14.595 | 20 | 24 | fits | 65,130 | 31 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 121,631 | 1.216 | 20 | 50 | fits | 117,764 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 555,060 | 5.551 | 20 | 50 | fits | 142,026 | 98 | 0.609 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 308,000 | 3.080 | 18 | 18 | fits | 186,824 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,632,202 | 16.322 | 18 | 18 | fits | 34,053 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 530,164 | 5.302 | 20 | 20 | fits | 108,009 | 49 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 120,483 | 1.205 | 20 | 200 | fits | 117,764 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 627,047 | 6.270 | 20 | 200 | fits | 108,009 | 49 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 121,395 | 1.214 | 20 | 20 | fits | 117,764 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 845,017 | 8.450 | 20 | 20 | fits | 97,683 | 40 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 124,980 | 1.250 | 20 | 24 | fits | 117,764 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,439,727 | 14.397 | 20 | 24 | fits | 65,095 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 123,940 | 1.239 | 20 | 50 | fits | 117,764 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 522,714 | 5.227 | 20 | 50 | fits | 161,686 | 98 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 360,963 | 3.610 | 18 | 18 | fits | 123,585 | 64 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,624,586 | 16.246 | 18 | 18 | fits | 46,453 | 18 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 537,678 | 5.377 | 20 | 20 | fits | 140,358 | 64 | 0.686 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 122,792 | 1.228 | 20 | 200 | fits | 117,764 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 666,305 | 6.663 | 20 | 200 | fits | 140,358 | 64 | 0.686 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 123,704 | 1.237 | 20 | 20 | fits | 117,764 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 883,799 | 8.838 | 20 | 20 | fits | 97,331 | 40 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 127,289 | 1.273 | 20 | 24 | fits | 117,764 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,476,713 | 14.767 | 20 | 24 | fits | 65,040 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 126,249 | 1.262 | 20 | 50 | fits | 117,764 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 529,623 | 5.296 | 20 | 50 | fits | 110,367 | 90 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 257,296 | 2.573 | 18 | 18 | fits | 131,502 | 105 | 0.695 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,615,191 | 16.152 | 18 | 18 | fits | 46,596 | 18 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 462,083 | 4.621 | 20 | 20 | fits | 153,279 | 84 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 117,875 | 1.179 | 20 | 200 | fits | 118,552 | 141 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 602,815 | 6.028 | 20 | 200 | fits | 153,279 | 84 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 118,787 | 1.188 | 20 | 20 | fits | 118,552 | 141 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 853,065 | 8.531 | 20 | 20 | fits | 119,262 | 46 | 0.696 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 122,372 | 1.224 | 20 | 24 | fits | 118,552 | 141 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,459,438 | 14.594 | 20 | 24 | fits | 67,726 | 38 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 121,332 | 1.213 | 20 | 50 | fits | 118,552 | 141 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 606,491 | 6.065 | 20 | 50 | fits | 153,279 | 84 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 308,350 | 3.083 | 18 | 18 | fits | 187,473 | 146 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,598,593 | 15.986 | 18 | 18 | fits | 46,691 | 19 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 497,820 | 4.978 | 20 | 20 | fits | 142,597 | 60 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 165,757 | 1.658 | 20 | 200 | fits | 118,940 | 142 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 628,257 | 6.283 | 20 | 200 | fits | 142,597 | 60 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 166,669 | 1.667 | 20 | 20 | fits | 118,940 | 142 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 938,489 | 9.385 | 20 | 20 | fits | 97,293 | 40 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 51,314 | 0.513 | 20 | 24 | fits | 52,727 | 65 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,474,022 | 14.740 | 20 | 24 | fits | 65,050 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 50,274 | 0.503 | 20 | 50 | fits | 52,727 | 65 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 489,336 | 4.893 | 20 | 50 | fits | 135,150 | 76 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 354,121 | 3.541 | 18 | 18 | fits | 185,362 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,599,889 | 15.999 | 18 | 18 | fits | 33,989 | 15 | 0.762 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 527,523 | 5.275 | 20 | 20 | fits | 140,474 | 58 | 0.701 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 117,194 | 1.172 | 20 | 200 | fits | 118,486 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 657,537 | 6.575 | 20 | 200 | fits | 140,474 | 58 | 0.701 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 118,106 | 1.181 | 20 | 20 | fits | 118,486 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 884,718 | 8.847 | 20 | 20 | fits | 96,882 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 121,691 | 1.217 | 20 | 24 | fits | 118,486 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,457,186 | 14.572 | 20 | 24 | fits | 58,779 | 32 | 0.758 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 120,651 | 1.207 | 20 | 50 | fits | 118,486 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 520,739 | 5.207 | 20 | 50 | fits | 104,167 | 71 | 0.701 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 305,988 | 3.060 | 18 | 18 | fits | 185,792 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,634,013 | 16.340 | 18 | 18 | fits | 49,813 | 25 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 555,317 | 5.553 | 20 | 20 | fits | 140,325 | 57 | 0.702 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 121,812 | 1.218 | 20 | 200 | fits | 118,486 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 685,854 | 6.859 | 20 | 200 | fits | 140,325 | 57 | 0.702 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 122,724 | 1.227 | 20 | 20 | fits | 118,486 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 903,035 | 9.030 | 20 | 20 | fits | 97,073 | 39 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 126,309 | 1.263 | 20 | 24 | fits | 118,486 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,460,243 | 14.602 | 20 | 24 | fits | 65,488 | 32 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 125,269 | 1.253 | 20 | 50 | fits | 118,486 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 538,969 | 5.390 | 20 | 50 | fits | 144,429 | 99 | 0.616 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 394,475 | 3.945 | 18 | 18 | fits | 180,226 | 105 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,634,141 | 16.341 | 18 | 18 | fits | 34,291 | 16 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 457,787 | 4.578 | 20 | 20 | fits | 152,728 | 83 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 116,205 | 1.162 | 20 | 200 | fits | 119,465 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 598,355 | 5.984 | 20 | 200 | fits | 152,728 | 83 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 117,117 | 1.171 | 20 | 20 | fits | 119,465 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 805,429 | 8.054 | 20 | 20 | fits | 119,522 | 53 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 120,702 | 1.207 | 20 | 24 | fits | 119,465 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,465,730 | 14.657 | 20 | 24 | fits | 64,995 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 119,662 | 1.197 | 20 | 50 | fits | 119,465 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 602,031 | 6.020 | 20 | 50 | fits | 152,728 | 83 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 304,967 | 3.050 | 18 | 18 | fits | 185,760 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,591,669 | 15.917 | 18 | 18 | fits | 33,989 | 15 | 0.762 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 451,688 | 4.517 | 20 | 20 | fits | 155,325 | 90 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 121,343 | 1.213 | 20 | 200 | fits | 118,365 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 592,394 | 5.924 | 20 | 200 | fits | 155,325 | 90 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 122,255 | 1.223 | 20 | 20 | fits | 118,365 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 866,474 | 8.665 | 20 | 20 | fits | 97,021 | 40 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 125,840 | 1.258 | 20 | 24 | fits | 118,365 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,466,995 | 14.670 | 20 | 24 | fits | 65,095 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 124,800 | 1.248 | 20 | 50 | fits | 118,365 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 596,070 | 5.961 | 20 | 50 | fits | 155,325 | 90 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 309,967 | 3.100 | 18 | 18 | fits | 185,622 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,605,401 | 16.054 | 18 | 18 | fits | 46,596 | 18 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 523,639 | 5.236 | 20 | 20 | fits | 141,923 | 58 | 0.706 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 125,961 | 1.260 | 20 | 200 | fits | 118,365 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 654,414 | 6.544 | 20 | 200 | fits | 141,923 | 58 | 0.706 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 126,873 | 1.269 | 20 | 20 | fits | 118,365 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 881,722 | 8.817 | 20 | 20 | fits | 97,556 | 39 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 130,458 | 1.305 | 20 | 24 | fits | 118,365 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,458,059 | 14.581 | 20 | 24 | fits | 62,153 | 39 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 129,418 | 1.294 | 20 | 50 | fits | 118,365 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 516,167 | 5.162 | 20 | 50 | fits | 123,240 | 65 | 0.756 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 392,862 | 3.929 | 18 | 18 | fits | 149,905 | 101 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,644,096 | 16.441 | 18 | 18 | fits | 46,691 | 19 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 566,440 | 5.664 | 20 | 20 | fits | 140,542 | 57 | 0.701 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 120,589 | 1.206 | 20 | 200 | fits | 118,325 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 696,356 | 6.964 | 20 | 200 | fits | 140,542 | 57 | 0.701 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 121,501 | 1.215 | 20 | 20 | fits | 118,325 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 880,941 | 8.809 | 20 | 20 | fits | 97,398 | 46 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 125,086 | 1.251 | 20 | 24 | fits | 118,325 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,476,985 | 14.770 | 20 | 24 | fits | 65,040 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 124,046 | 1.240 | 20 | 50 | fits | 118,325 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 559,490 | 5.595 | 20 | 50 | fits | 143,587 | 98 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 254,097 | 2.541 | 18 | 18 | fits | 130,506 | 105 | 0.694 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,615,463 | 16.155 | 18 | 18 | fits | 46,596 | 18 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 470,980 | 4.710 | 20 | 20 | fits | 153,291 | 84 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 124,496 | 1.245 | 20 | 200 | fits | 119,430 | 140 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 611,712 | 6.117 | 20 | 200 | fits | 153,291 | 84 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 125,408 | 1.254 | 20 | 20 | fits | 119,430 | 140 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 862,312 | 8.623 | 20 | 20 | fits | 118,876 | 46 | 0.695 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 128,993 | 1.290 | 20 | 24 | fits | 119,430 | 140 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,500,705 | 15.007 | 20 | 24 | fits | 98,486 | 46 | 0.751 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 127,953 | 1.280 | 20 | 50 | fits | 119,430 | 140 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 615,388 | 6.154 | 20 | 50 | fits | 153,291 | 84 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 314,391 | 3.144 | 18 | 18 | fits | 186,893 | 141 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,643,768 | 16.438 | 18 | 18 | fits | 46,691 | 19 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 434,078 | 4.341 | 20 | 20 | fits | 154,345 | 84 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 126,548 | 1.265 | 20 | 200 | fits | 118,126 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 575,410 | 5.754 | 20 | 200 | fits | 154,345 | 84 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 127,460 | 1.275 | 20 | 20 | fits | 118,126 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 792,951 | 7.930 | 20 | 20 | fits | 86,371 | 37 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 131,045 | 1.310 | 20 | 24 | fits | 118,126 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,477,910 | 14.779 | 20 | 24 | fits | 100,450 | 52 | 0.744 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 130,005 | 1.300 | 20 | 50 | fits | 118,126 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 579,086 | 5.791 | 20 | 50 | fits | 154,345 | 84 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 424,676 | 4.247 | 18 | 18 | fits | 181,287 | 105 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,652,438 | 16.524 | 18 | 18 | fits | 34,291 | 16 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 482,940 | 4.829 | 20 | 20 | fits | 151,780 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 129,018 | 1.290 | 20 | 200 | fits | 118,287 | 141 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 623,281 | 6.233 | 20 | 200 | fits | 151,780 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 129,930 | 1.299 | 20 | 20 | fits | 118,287 | 141 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 930,228 | 9.302 | 20 | 20 | fits | 96,976 | 39 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 133,515 | 1.335 | 20 | 24 | fits | 118,287 | 141 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,546,694 | 15.467 | 20 | 24 | fits | 98,912 | 46 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 132,475 | 1.325 | 20 | 50 | fits | 118,287 | 141 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 626,957 | 6.270 | 20 | 50 | fits | 151,780 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 320,141 | 3.201 | 18 | 18 | fits | 188,121 | 146 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,639,649 | 16.396 | 18 | 18 | fits | 46,756 | 19 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 463,035 | 4.630 | 20 | 20 | fits | 119,427 | 74 | 0.625 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 120,754 | 1.208 | 20 | 200 | fits | 118,013 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 570,302 | 5.703 | 20 | 200 | fits | 119,427 | 74 | 0.625 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 121,666 | 1.217 | 20 | 20 | fits | 118,013 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 843,639 | 8.436 | 20 | 20 | fits | 97,399 | 46 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 125,251 | 1.253 | 20 | 24 | fits | 118,013 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,431,836 | 14.318 | 20 | 24 | fits | 52,393 | 27 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 124,211 | 1.242 | 20 | 50 | fits | 118,013 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 573,978 | 5.740 | 20 | 50 | fits | 119,427 | 74 | 0.625 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 310,297 | 3.103 | 18 | 18 | fits | 186,541 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,680,384 | 16.804 | 18 | 18 | fits | 33,989 | 15 | 0.762 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 531,711 | 5.317 | 20 | 20 | fits | 106,350 | 49 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 123,063 | 1.231 | 20 | 200 | fits | 118,013 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 627,926 | 6.279 | 20 | 200 | fits | 106,350 | 49 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 123,975 | 1.240 | 20 | 20 | fits | 118,013 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 846,476 | 8.465 | 20 | 20 | fits | 97,826 | 40 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 127,560 | 1.276 | 20 | 24 | fits | 118,013 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,441,049 | 14.410 | 20 | 24 | fits | 58,548 | 32 | 0.761 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 126,520 | 1.265 | 20 | 50 | fits | 118,013 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 525,252 | 5.253 | 20 | 50 | fits | 102,173 | 64 | 0.706 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 312,691 | 3.127 | 18 | 18 | fits | 186,626 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,661,292 | 16.613 | 18 | 18 | fits | 46,453 | 18 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 525,843 | 5.258 | 20 | 20 | fits | 141,360 | 64 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 125,372 | 1.254 | 20 | 200 | fits | 118,013 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 655,472 | 6.555 | 20 | 200 | fits | 141,360 | 64 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 126,284 | 1.263 | 20 | 20 | fits | 118,013 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 873,527 | 8.735 | 20 | 20 | fits | 97,557 | 40 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 129,869 | 1.299 | 20 | 24 | fits | 118,013 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,467,999 | 14.680 | 20 | 24 | fits | 65,050 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 128,829 | 1.288 | 20 | 50 | fits | 118,013 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 517,788 | 5.178 | 20 | 50 | fits | 109,645 | 90 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 284,841 | 2.848 | 18 | 18 | fits | 156,467 | 136 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,675,464 | 16.755 | 18 | 18 | fits | 34,162 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 540,854 | 5.409 | 20 | 20 | fits | 141,852 | 58 | 0.705 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 127,681 | 1.277 | 20 | 200 | fits | 118,013 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 671,336 | 6.713 | 20 | 200 | fits | 141,852 | 58 | 0.705 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 128,593 | 1.286 | 20 | 20 | fits | 118,013 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 898,458 | 8.985 | 20 | 20 | fits | 96,882 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 132,178 | 1.322 | 20 | 24 | fits | 118,013 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,471,199 | 14.712 | 20 | 24 | fits | 65,238 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 131,138 | 1.311 | 20 | 50 | fits | 118,013 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 533,160 | 5.332 | 20 | 50 | fits | 161,487 | 105 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 262,037 | 2.620 | 18 | 18 | fits | 131,354 | 105 | 0.694 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,647,353 | 16.474 | 18 | 18 | fits | 46,756 | 19 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 562,047 | 5.620 | 20 | 20 | fits | 141,010 | 58 | 0.700 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 85,121 | 0.851 | 20 | 200 | fits | 91,388 | 105 | 0.604 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 692,044 | 6.920 | 20 | 200 | fits | 141,010 | 58 | 0.700 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 86,033 | 0.860 | 20 | 20 | fits | 91,388 | 105 | 0.604 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 919,361 | 9.194 | 20 | 20 | fits | 97,512 | 39 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 89,618 | 0.896 | 20 | 24 | fits | 91,388 | 105 | 0.604 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,470,876 | 14.709 | 20 | 24 | fits | 65,040 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 88,578 | 0.886 | 20 | 50 | fits | 91,388 | 105 | 0.604 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 554,710 | 5.547 | 20 | 50 | fits | 144,054 | 99 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 245,592 | 2.456 | 18 | 18 | fits | 157,469 | 142 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,646,850 | 16.468 | 18 | 18 | fits | 47,227 | 19 | 0.708 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 477,720 | 4.777 | 20 | 20 | fits | 151,797 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 124,692 | 1.247 | 20 | 200 | fits | 117,647 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 618,078 | 6.181 | 20 | 200 | fits | 151,797 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 125,604 | 1.256 | 20 | 20 | fits | 117,647 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 857,784 | 8.578 | 20 | 20 | fits | 118,740 | 46 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 129,189 | 1.292 | 20 | 24 | fits | 117,647 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 1,525,326 | 15.253 | 20 | 24 | fits | 65,425 | 32 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 128,149 | 1.281 | 20 | 50 | fits | 117,647 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 621,754 | 6.218 | 20 | 50 | fits | 151,797 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 315,102 | 3.151 | 18 | 18 | fits | 187,408 | 141 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 1,711,192 | 17.112 | 18 | 18 | fits | 36,502 | 15 | 0.833 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 468,705 | 4.687 | 20 | 20 | fits | 152,857 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 115,870 | 1.159 | 20 | 200 | fits | 117,647 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 609,402 | 6.094 | 20 | 200 | fits | 152,857 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 116,782 | 1.168 | 20 | 20 | fits | 117,647 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 836,071 | 8.361 | 20 | 20 | fits | 105,570 | 42 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 120,367 | 1.204 | 20 | 24 | fits | 117,647 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 1,580,856 | 15.809 | 20 | 24 | fits | 65,533 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 119,327 | 1.193 | 20 | 50 | fits | 117,647 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 613,078 | 6.131 | 20 | 50 | fits | 152,857 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 306,280 | 3.063 | 18 | 18 | fits | 187,408 | 141 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 1,672,666 | 16.727 | 18 | 18 | fits | 46,518 | 18 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 478,289 | 4.783 | 20 | 20 | fits | 152,609 | 83 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 126,480 | 1.265 | 20 | 200 | fits | 117,716 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 618,738 | 6.187 | 20 | 200 | fits | 152,609 | 83 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 127,392 | 1.274 | 20 | 20 | fits | 117,716 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 937,344 | 9.373 | 20 | 20 | fits | 63,367 | 31 | 0.695 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 130,977 | 1.310 | 20 | 24 | fits | 117,716 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 1,542,937 | 15.429 | 20 | 24 | fits | 64,995 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 129,937 | 1.299 | 20 | 50 | fits | 117,716 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 622,414 | 6.224 | 20 | 50 | fits | 152,609 | 83 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 325,566 | 3.256 | 18 | 18 | fits | 187,046 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 1,746,684 | 17.467 | 18 | 18 | fits | 40,461 | 19 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 469,021 | 4.690 | 20 | 20 | fits | 139,187 | 79 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 126,488 | 1.265 | 20 | 200 | fits | 117,358 | 134 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 596,048 | 5.960 | 20 | 200 | fits | 139,187 | 79 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 127,400 | 1.274 | 20 | 20 | fits | 117,358 | 134 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 994,217 | 9.942 | 20 | 20 | fits | 97,454 | 39 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 130,985 | 1.310 | 20 | 24 | fits | 117,358 | 134 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 1,586,318 | 15.863 | 20 | 24 | fits | 65,559 | 32 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 129,945 | 1.299 | 20 | 50 | fits | 117,358 | 134 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 599,724 | 5.997 | 20 | 50 | fits | 139,187 | 79 | 0.672 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 316,355 | 3.164 | 18 | 18 | fits | 186,865 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 1,710,253 | 17.103 | 18 | 18 | fits | 34,291 | 16 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 639,090 | 6.391 | 20 | 20 | fits | 106,047 | 49 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 116,556 | 1.166 | 20 | 200 | fits | 117,358 | 134 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 735,681 | 7.357 | 20 | 200 | fits | 106,047 | 49 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 117,468 | 1.175 | 20 | 20 | fits | 117,358 | 134 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 954,001 | 9.540 | 20 | 20 | fits | 97,767 | 40 | 0.737 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 121,053 | 1.211 | 20 | 24 | fits | 117,358 | 134 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 1,516,920 | 15.169 | 20 | 24 | fits | 58,309 | 32 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 120,013 | 1.200 | 20 | 50 | fits | 117,358 | 134 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 554,299 | 5.543 | 20 | 50 | fits | 103,694 | 64 | 0.721 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 306,423 | 3.064 | 18 | 18 | fits | 186,865 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 1,702,018 | 17.020 | 18 | 18 | fits | 46,453 | 18 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 616,214 | 6.162 | 20 | 20 | fits | 140,326 | 64 | 0.684 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 125,733 | 1.257 | 20 | 200 | fits | 117,289 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 744,958 | 7.450 | 20 | 200 | fits | 140,326 | 64 | 0.684 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 126,645 | 1.266 | 20 | 20 | fits | 117,289 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 962,458 | 9.625 | 20 | 20 | fits | 97,262 | 40 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 130,230 | 1.302 | 20 | 24 | fits | 117,289 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 1,523,661 | 15.237 | 20 | 24 | fits | 64,907 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 129,190 | 1.292 | 20 | 50 | fits | 117,289 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 608,308 | 6.083 | 20 | 50 | fits | 108,612 | 90 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 315,682 | 3.157 | 18 | 18 | fits | 186,947 | 140 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 1,708,592 | 17.086 | 18 | 18 | fits | 46,453 | 18 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 613,936 | 6.139 | 20 | 20 | fits | 141,467 | 57 | 0.705 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 115,801 | 1.158 | 20 | 200 | fits | 117,289 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 744,265 | 7.443 | 20 | 200 | fits | 141,467 | 57 | 0.705 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 116,713 | 1.167 | 20 | 20 | fits | 117,289 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 961,334 | 9.613 | 20 | 20 | fits | 97,154 | 39 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 120,298 | 1.203 | 20 | 24 | fits | 117,289 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 1,539,137 | 15.391 | 20 | 24 | fits | 65,437 | 32 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 119,258 | 1.193 | 20 | 50 | fits | 117,289 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 606,474 | 6.065 | 20 | 50 | fits | 164,387 | 104 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 356,534 | 3.565 | 18 | 18 | fits | 123,610 | 64 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 1,724,112 | 17.241 | 18 | 18 | fits | 33,874 | 15 | 0.760 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 660,531 | 6.605 | 20 | 20 | fits | 140,602 | 57 | 0.701 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 125,116 | 1.251 | 20 | 200 | fits | 117,358 | 134 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 790,447 | 7.904 | 20 | 200 | fits | 140,602 | 57 | 0.701 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 126,028 | 1.260 | 20 | 20 | fits | 117,358 | 134 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 1,007,576 | 10.076 | 20 | 20 | fits | 97,214 | 39 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 129,613 | 1.296 | 20 | 24 | fits | 117,358 | 134 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 1,608,040 | 16.080 | 20 | 24 | fits | 65,533 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 128,573 | 1.286 | 20 | 50 | fits | 117,358 | 134 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 653,521 | 6.535 | 20 | 50 | fits | 143,632 | 98 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 259,659 | 2.597 | 18 | 18 | fits | 131,541 | 105 | 0.697 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 1,699,850 | 16.998 | 18 | 18 | fits | 46,518 | 18 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 454,167 | 4.542 | 20 | 20 | fits | 119,696 | 75 | 0.625 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 112,180 | 1.122 | 20 | 200 | fits | 118,702 | 134 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 561,703 | 5.617 | 20 | 200 | fits | 119,696 | 75 | 0.625 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 113,092 | 1.131 | 20 | 20 | fits | 118,702 | 134 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 802,632 | 8.026 | 20 | 20 | fits | 119,220 | 47 | 0.690 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 116,677 | 1.167 | 20 | 24 | fits | 118,702 | 134 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 1,548,242 | 15.482 | 20 | 24 | fits | 64,995 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 115,637 | 1.156 | 20 | 50 | fits | 118,702 | 134 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 565,379 | 5.654 | 20 | 50 | fits | 119,696 | 75 | 0.625 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 301,539 | 3.015 | 18 | 18 | fits | 186,357 | 145 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if1` | 1,674,181 | 16.742 | 18 | 18 | fits | 33,989 | 15 | 0.762 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 452,466 | 4.525 | 20 | 20 | fits | 155,217 | 90 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 122,414 | 1.224 | 20 | 200 | fits | 118,132 | 134 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 593,064 | 5.931 | 20 | 200 | fits | 155,217 | 90 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 123,326 | 1.233 | 20 | 20 | fits | 118,132 | 134 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 833,587 | 8.336 | 20 | 20 | fits | 119,192 | 47 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 126,911 | 1.269 | 20 | 24 | fits | 118,132 | 134 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 1,578,972 | 15.790 | 20 | 24 | fits | 65,095 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 125,871 | 1.259 | 20 | 50 | fits | 118,132 | 134 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 596,740 | 5.967 | 20 | 50 | fits | 155,217 | 90 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 310,873 | 3.109 | 18 | 18 | fits | 185,457 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if1` | 1,674,706 | 16.747 | 18 | 18 | fits | 50,249 | 25 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 458,477 | 4.585 | 20 | 20 | fits | 153,284 | 84 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 111,675 | 1.117 | 20 | 200 | fits | 118,132 | 134 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 599,202 | 5.992 | 20 | 200 | fits | 153,284 | 84 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 112,587 | 1.126 | 20 | 20 | fits | 118,132 | 134 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 990,709 | 9.907 | 20 | 20 | fits | 97,216 | 39 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 116,172 | 1.162 | 20 | 24 | fits | 118,132 | 134 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 1,586,476 | 15.865 | 20 | 24 | fits | 68,740 | 38 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 115,132 | 1.151 | 20 | 50 | fits | 118,132 | 134 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 602,878 | 6.029 | 20 | 50 | fits | 153,284 | 84 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 301,005 | 3.010 | 18 | 18 | fits | 186,328 | 145 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if1` | 1,678,868 | 16.789 | 18 | 18 | fits | 46,756 | 19 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 426,814 | 4.268 | 20 | 20 | fits | 154,446 | 84 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 120,281 | 1.203 | 20 | 200 | fits | 118,063 | 134 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 568,247 | 5.682 | 20 | 200 | fits | 154,446 | 84 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 121,193 | 1.212 | 20 | 20 | fits | 118,063 | 134 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 972,804 | 9.728 | 20 | 20 | fits | 97,355 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 124,778 | 1.248 | 20 | 24 | fits | 118,063 | 134 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 1,569,790 | 15.698 | 20 | 24 | fits | 65,640 | 32 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 123,738 | 1.237 | 20 | 50 | fits | 118,063 | 134 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 571,923 | 5.719 | 20 | 50 | fits | 154,446 | 84 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 417,412 | 4.174 | 18 | 18 | fits | 180,161 | 105 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if1` | 1,702,364 | 17.024 | 18 | 18 | fits | 46,691 | 19 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 650,263 | 6.503 | 20 | 20 | fits | 139,052 | 57 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 166,037 | 1.660 | 20 | 200 | fits | 118,571 | 137 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 780,062 | 7.801 | 20 | 200 | fits | 139,052 | 57 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 166,949 | 1.669 | 20 | 20 | fits | 118,571 | 137 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 996,815 | 9.968 | 20 | 20 | fits | 96,982 | 39 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 51,963 | 0.520 | 20 | 24 | fits | 55,816 | 72 | 0.562 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 1,521,139 | 15.211 | 20 | 24 | fits | 58,925 | 33 | 0.756 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 50,923 | 0.509 | 20 | 50 | fits | 55,816 | 72 | 0.562 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 458,053 | 4.581 | 20 | 50 | fits | 102,096 | 68 | 0.605 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 355,892 | 3.559 | 18 | 18 | fits | 186,853 | 146 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if1` | 1,719,428 | 17.194 | 18 | 18 | fits | 49,451 | 18 | 0.777 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 659,809 | 6.598 | 20 | 20 | fits | 140,587 | 57 | 0.701 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 121,904 | 1.219 | 20 | 200 | fits | 118,300 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 789,872 | 7.899 | 20 | 200 | fits | 140,587 | 57 | 0.701 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 122,816 | 1.228 | 20 | 20 | fits | 118,300 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 1,007,140 | 10.071 | 20 | 20 | fits | 97,214 | 39 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 126,401 | 1.264 | 20 | 24 | fits | 118,300 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 1,607,850 | 16.078 | 20 | 24 | fits | 65,326 | 31 | 0.724 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 125,361 | 1.254 | 20 | 50 | fits | 118,300 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 652,961 | 6.530 | 20 | 50 | fits | 141,949 | 98 | 0.609 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 310,760 | 3.108 | 18 | 18 | fits | 185,854 | 141 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if1` | 1,699,678 | 16.997 | 18 | 18 | fits | 46,633 | 18 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 615,236 | 6.152 | 20 | 20 | fits | 141,435 | 57 | 0.704 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 111,516 | 1.115 | 20 | 200 | fits | 118,300 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 745,545 | 7.455 | 20 | 200 | fits | 141,435 | 57 | 0.704 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 112,428 | 1.124 | 20 | 20 | fits | 118,300 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 962,674 | 9.627 | 20 | 20 | fits | 97,214 | 39 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 116,013 | 1.160 | 20 | 24 | fits | 118,300 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 1,550,789 | 15.508 | 20 | 24 | fits | 65,558 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 114,973 | 1.150 | 20 | 50 | fits | 118,300 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 607,786 | 6.078 | 20 | 50 | fits | 161,446 | 98 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 361,243 | 3.612 | 18 | 18 | fits | 122,885 | 64 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if1` | 1,723,387 | 17.234 | 18 | 18 | fits | 34,053 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 661,903 | 6.619 | 20 | 20 | fits | 140,573 | 57 | 0.701 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 122,176 | 1.222 | 20 | 200 | fits | 118,231 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 791,850 | 7.918 | 20 | 200 | fits | 140,573 | 57 | 0.701 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 123,088 | 1.231 | 20 | 20 | fits | 118,231 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 976,441 | 9.764 | 20 | 20 | fits | 97,398 | 46 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 126,673 | 1.267 | 20 | 24 | fits | 118,231 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 1,559,515 | 15.595 | 20 | 24 | fits | 64,995 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 125,633 | 1.256 | 20 | 50 | fits | 118,231 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 654,953 | 6.550 | 20 | 50 | fits | 143,651 | 98 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 264,721 | 2.647 | 18 | 18 | fits | 130,505 | 105 | 0.694 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if1` | 1,732,185 | 17.322 | 18 | 18 | fits | 34,053 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 470,468 | 4.705 | 20 | 20 | fits | 151,797 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 116,540 | 1.165 | 20 | 200 | fits | 117,863 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 610,826 | 6.108 | 20 | 200 | fits | 151,797 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 117,452 | 1.175 | 20 | 20 | fits | 117,863 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 850,532 | 8.505 | 20 | 20 | fits | 118,740 | 46 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 121,037 | 1.210 | 20 | 24 | fits | 117,863 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 1,595,958 | 15.960 | 20 | 24 | fits | 65,668 | 32 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 119,997 | 1.200 | 20 | 50 | fits | 117,863 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 614,502 | 6.145 | 20 | 50 | fits | 151,797 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 307,805 | 3.078 | 18 | 18 | fits | 188,263 | 146 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 1,734,977 | 17.350 | 18 | 18 | fits | 34,026 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 480,522 | 4.805 | 20 | 20 | fits | 152,857 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 128,287 | 1.283 | 20 | 200 | fits | 117,865 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 621,219 | 6.212 | 20 | 200 | fits | 152,857 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 129,199 | 1.292 | 20 | 20 | fits | 117,865 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 828,033 | 8.280 | 20 | 20 | fits | 85,715 | 37 | 0.636 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 132,784 | 1.328 | 20 | 24 | fits | 117,865 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 1,564,252 | 15.643 | 20 | 24 | fits | 65,425 | 32 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 131,744 | 1.317 | 20 | 50 | fits | 117,865 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 624,895 | 6.249 | 20 | 50 | fits | 152,857 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 318,097 | 3.181 | 18 | 18 | fits | 186,808 | 141 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 1,749,110 | 17.491 | 18 | 18 | fits | 34,025 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 471,156 | 4.712 | 20 | 20 | fits | 152,857 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 118,921 | 1.189 | 20 | 200 | fits | 117,865 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 611,853 | 6.119 | 20 | 200 | fits | 152,857 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 119,833 | 1.198 | 20 | 20 | fits | 117,865 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 986,958 | 9.870 | 20 | 20 | fits | 96,611 | 39 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 123,418 | 1.234 | 20 | 24 | fits | 117,865 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 1,627,619 | 16.276 | 20 | 24 | fits | 65,533 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 122,378 | 1.224 | 20 | 50 | fits | 117,865 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 615,529 | 6.155 | 20 | 50 | fits | 152,857 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 308,731 | 3.087 | 18 | 18 | fits | 186,808 | 141 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 1,748,231 | 17.482 | 18 | 18 | fits | 40,460 | 19 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 506,955 | 5.070 | 20 | 20 | fits | 108,941 | 51 | 0.647 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 165,062 | 1.651 | 20 | 200 | fits | 118,034 | 137 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 603,736 | 6.037 | 20 | 200 | fits | 108,941 | 51 | 0.647 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 165,974 | 1.660 | 20 | 20 | fits | 118,034 | 137 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 989,839 | 9.898 | 20 | 20 | fits | 97,138 | 40 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 51,525 | 0.515 | 20 | 24 | fits | 55,430 | 72 | 0.557 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 1,565,049 | 15.650 | 20 | 24 | fits | 65,957 | 31 | 0.726 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 50,485 | 0.505 | 20 | 50 | fits | 55,430 | 72 | 0.557 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 498,471 | 4.985 | 20 | 50 | fits | 135,166 | 76 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 363,240 | 3.632 | 18 | 18 | fits | 186,270 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 1,743,253 | 17.433 | 18 | 18 | fits | 46,596 | 18 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 650,607 | 6.506 | 20 | 20 | fits | 126,314 | 54 | 0.712 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 127,558 | 1.276 | 20 | 200 | fits | 117,360 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 767,465 | 7.675 | 20 | 200 | fits | 126,314 | 54 | 0.712 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 128,470 | 1.285 | 20 | 20 | fits | 117,360 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 987,964 | 9.880 | 20 | 20 | fits | 97,570 | 40 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 132,055 | 1.321 | 20 | 24 | fits | 117,360 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 1,570,289 | 15.703 | 20 | 24 | fits | 52,839 | 27 | 0.751 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 131,015 | 1.310 | 20 | 50 | fits | 117,360 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 564,918 | 5.649 | 20 | 50 | fits | 103,694 | 64 | 0.721 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 317,042 | 3.170 | 18 | 18 | fits | 186,482 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 1,743,444 | 17.434 | 18 | 18 | fits | 46,453 | 18 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 604,641 | 6.046 | 20 | 20 | fits | 105,751 | 49 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 117,082 | 1.171 | 20 | 200 | fits | 117,360 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 701,122 | 7.011 | 20 | 200 | fits | 105,751 | 49 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 117,994 | 1.180 | 20 | 20 | fits | 117,360 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 919,851 | 9.199 | 20 | 20 | fits | 97,826 | 40 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 121,579 | 1.216 | 20 | 24 | fits | 117,360 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 1,534,780 | 15.348 | 20 | 24 | fits | 98,311 | 45 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 120,539 | 1.205 | 20 | 50 | fits | 117,360 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 519,055 | 5.191 | 20 | 50 | fits | 102,127 | 64 | 0.706 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 306,566 | 3.066 | 18 | 18 | fits | 186,482 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 1,754,312 | 17.543 | 18 | 18 | fits | 33,989 | 15 | 0.762 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 562,828 | 5.628 | 20 | 20 | fits | 159,861 | 64 | 0.728 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 125,655 | 1.257 | 20 | 200 | fits | 117,429 | 134 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 711,025 | 7.110 | 20 | 200 | fits | 159,861 | 64 | 0.728 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 126,567 | 1.266 | 20 | 20 | fits | 117,429 | 134 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 929,857 | 9.299 | 20 | 20 | fits | 97,408 | 40 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 130,152 | 1.302 | 20 | 24 | fits | 117,429 | 134 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 1,557,259 | 15.573 | 20 | 24 | fits | 65,626 | 31 | 0.723 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 129,112 | 1.291 | 20 | 50 | fits | 117,429 | 134 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 554,840 | 5.548 | 20 | 50 | fits | 109,179 | 90 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 365,769 | 3.658 | 18 | 18 | fits | 123,459 | 64 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 1,747,236 | 17.472 | 18 | 18 | fits | 51,358 | 25 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 607,424 | 6.074 | 20 | 20 | fits | 141,959 | 58 | 0.706 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 115,087 | 1.151 | 20 | 200 | fits | 117,429 | 134 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 737,988 | 7.380 | 20 | 200 | fits | 141,959 | 58 | 0.706 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 115,999 | 1.160 | 20 | 20 | fits | 117,429 | 134 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 965,110 | 9.651 | 20 | 20 | fits | 96,882 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 119,584 | 1.196 | 20 | 24 | fits | 117,429 | 134 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 1,570,932 | 15.709 | 20 | 24 | fits | 98,489 | 45 | 0.752 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 118,544 | 1.185 | 20 | 50 | fits | 117,429 | 134 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 599,705 | 5.997 | 20 | 50 | fits | 161,508 | 105 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 249,162 | 2.492 | 18 | 18 | fits | 131,073 | 105 | 0.693 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 1,749,233 | 17.492 | 18 | 18 | fits | 34,356 | 16 | 0.755 |
| an event behind 15 others | `backlog.event.if0` | 149,716 | 1.497 | 20 | 200 | fits | 115,377 | 125 | 0.536 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 702,123 | 7.021 | 20 | 20 | fits | 79,442 | 39 | 0.713 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 138,309 | 1.383 | 20 | 200 | fits | 138,517 | 143 | 0.534 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 542,206 | 5.422 | 20 | 200 | fits | 130,195 | 57 | 0.693 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 134,050 | 1.341 | 20 | 20 | fits | 138,517 | 143 | 0.534 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 769,185 | 7.692 | 20 | 20 | fits | 79,442 | 39 | 0.713 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 137,635 | 1.376 | 20 | 24 | fits | 138,517 | 143 | 0.534 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,231,694 | 12.317 | 20 | 24 | fits | 50,942 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 136,595 | 1.366 | 20 | 50 | fits | 138,517 | 143 | 0.534 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 540,711 | 5.407 | 20 | 50 | fits | 130,195 | 57 | 0.693 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 540,646 | 5.406 | 18 | 18 | fits | 130,195 | 57 | 0.693 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,393,783 | 13.938 | 18 | 18 | fits | 31,776 | 15 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 467,511 | 4.675 | 20 | 20 | fits | 160,777 | 58 | 0.744 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 111,152 | 1.112 | 20 | 200 | fits | 115,834 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 617,367 | 6.174 | 20 | 200 | fits | 160,777 | 58 | 0.744 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 112,064 | 1.121 | 20 | 20 | fits | 115,834 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 845,512 | 8.455 | 20 | 20 | fits | 97,424 | 39 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 115,649 | 1.156 | 20 | 24 | fits | 115,834 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,386,446 | 13.864 | 20 | 24 | fits | 52,769 | 28 | 0.747 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 114,609 | 1.146 | 20 | 50 | fits | 115,834 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 460,266 | 4.603 | 20 | 50 | fits | 123,334 | 65 | 0.737 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 460,201 | 4.602 | 18 | 18 | fits | 123,334 | 65 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,657,200 | 16.572 | 18 | 18 | fits | 34,286 | 16 | 0.752 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 23,878 | 0.239 | 20 | 20 | fits | 42,822 | 21 | 0.763 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 111,152 | 1.112 | 20 | 200 | fits | 115,834 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 57,895 | 0.579 | 20 | 200 | fits | 42,822 | 21 | 0.763 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 112,064 | 1.121 | 20 | 20 | fits | 115,834 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 824,671 | 8.247 | 20 | 20 | fits | 97,258 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 115,649 | 1.156 | 20 | 24 | fits | 115,834 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,380,491 | 13.805 | 20 | 24 | fits | 33,382 | 23 | 0.651 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 114,609 | 1.146 | 20 | 50 | fits | 115,834 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 460,266 | 4.603 | 20 | 50 | fits | 123,334 | 65 | 0.737 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 460,201 | 4.602 | 18 | 18 | fits | 123,334 | 65 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,617,512 | 16.175 | 18 | 18 | fits | 46,686 | 19 | 0.681 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,358,497 | 63.585 | 20 | 20 | MISS ceiling | 48,088 | 27 | 0.570 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,040,138 | 360.401 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,040,063 | 360.401 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,039,988 | 360.400 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,039,913 | 360.399 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 122,709 | 1.227 | 20 | 200 | fits | 111,946 | 134 | 0.508 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 661,721 | 6.617 | 20 | 200 | fits | 112,489 | 43 | 0.723 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 118,450 | 1.185 | 20 | 20 | fits | 111,946 | 134 | 0.508 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 823,609 | 8.236 | 20 | 20 | fits | 67,791 | 25 | 0.714 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 122,035 | 1.220 | 20 | 24 | fits | 111,946 | 134 | 0.508 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,485,183 | 64.852 | 20 | 24 | MISS ceiling | 29,796 | 23 | 0.547 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 120,995 | 1.210 | 20 | 50 | fits | 111,946 | 134 | 0.508 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 547,737 | 5.477 | 20 | 50 | fits | 140,172 | 91 | 0.632 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 248,869 | 2.489 | 18 | 18 | fits | 128,329 | 102 | 0.703 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,318,542 | 13.185 | 18 | 18 | fits | 45,400 | 21 | 0.630 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
