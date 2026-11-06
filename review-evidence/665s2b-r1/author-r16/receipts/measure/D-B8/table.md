### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 22 paths and 6 of 587 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.886 (7.590) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged2-7.adp_available.if0` (backlog-adp@blank-aged2-7) | 6.219 (7.491) | fits | 7 adp | 49 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.092 (0.660) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.497 (2.529) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.663 (64.241) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.494 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 7.905 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.625 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 10.379 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 4.945 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 14.261 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.871 | fits | 0 acmp | 52 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.acmp.last.if0` (backlog-adp@blank-aged2-7) | 9.339 | fits | 11 acmp | 52 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.861 | fits | 0 adp | 52 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.adp.last.if0` (backlog-adp@blank-aged2-7) | 7.390 | fits | 7 adp | 50 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 6.334 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.906 | fits | 0 aecp | 52 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.958 | MISS ceiling | 15 aecp | 52 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.896 | fits | 0 maap | 52 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.410 | fits | 6 maap | 52 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.361 | fits | 0 srp | 52 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-aged2-7.service.srp.last.if1` (backlog-adp@verify-aged2-7) | 16.307 | fits | 31 srp | 52 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 16.867 | 18 | 181,272 (1.813) | yes | - |
| backlog-adp@blank-1 | 0 | 16.153 | 18 | 181,374 (1.814) | yes | - |
| backlog-adp@blank-2 | 0 | 16.270 | 19 | 181,374 (1.814) | yes | - |
| backlog-adp@blank-3 | 0 | 17.512 | 20 | 181,374 (1.814) | yes | - |
| backlog-adp@blank-4 | 0 | 16.353 | 18 | 181,374 (1.814) | yes | - |
| backlog-adp@blank-5 | 0 | 16.671 | 20 | 181,374 (1.814) | yes | - |
| backlog-adp@blank-6 | 0 | 16.680 | 20 | 151,229 (1.512) | yes | - |
| backlog-adp@blank-7 | 0 | 16.401 | 18 | 151,063 (1.511) | yes | - |
| backlog-adp@program-0 | 0 | 16.278 | 18 | 180,450 (1.804) | yes | - |
| backlog-adp@program-1 | 0 | 17.112 | 20 | 180,450 (1.804) | yes | - |
| backlog-adp@program-2 | 0 | 16.647 | 20 | 180,450 (1.804) | yes | - |
| backlog-adp@program-3 | 0 | 16.361 | 18 | 151,158 (1.512) | yes | - |
| backlog-adp@program-4 | 0 | 15.389 | 18 | 180,212 (1.802) | yes | - |
| backlog-adp@program-5 | 0 | 15.706 | 19 | 180,312 (1.803) | yes | - |
| backlog-adp@program-6 | 0 | 15.951 | 20 | 180,411 (1.804) | yes | - |
| backlog-adp@program-7 | 0 | 15.860 | 19 | 150,997 (1.510) | yes | - |
| backlog-adp@verify-0 | 0 | 16.526 | 18 | 181,162 (1.812) | yes | - |
| backlog-adp@verify-1 | 0 | 16.486 | 18 | 181,264 (1.813) | yes | - |
| backlog-adp@verify-2 | 0 | 17.892 | 20 | 181,264 (1.813) | yes | - |
| backlog-adp@verify-3 | 0 | 16.896 | 20 | 181,264 (1.813) | yes | - |
| backlog-adp@verify-4 | 0 | 16.936 | 20 | 181,264 (1.813) | yes | - |
| backlog-adp@verify-5 | 0 | 16.791 | 19 | 181,264 (1.813) | yes | - |
| backlog-adp@verify-6 | 0 | 17.210 | 20 | 151,071 (1.511) | yes | - |
| backlog-adp@verify-7 | 0 | 17.120 | 20 | 151,114 (1.511) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 16.184 | 18 | 181,279 (1.813) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 16.138 | 18 | 181,279 (1.813) | yes | - |
| backlog-adp@blank-aged2-2 | 1 | 16.233 | 18 | 182,362 (1.824) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 17.306 | 19 | 181,358 (1.814) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 17.222 | 19 | 181,358 (1.814) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 17.195 | 19 | 181,358 (1.814) | yes | - |
| backlog-adp@blank-aged2-6 | 1 | 17.169 | 18 | 150,609 (1.506) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 17.343 | 19 | 150,443 (1.504) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 16.446 | 19 | 180,374 (1.804) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 16.294 | 18 | 180,330 (1.803) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 16.286 | 18 | 180,330 (1.803) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 16.537 | 19 | 180,330 (1.803) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 16.618 | 19 | 181,413 (1.814) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 16.633 | 19 | 180,251 (1.803) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 16.611 | 19 | 150,521 (1.505) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 16.578 | 19 | 150,518 (1.505) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 16.557 | 18 | 181,183 (1.812) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 16.513 | 18 | 181,183 (1.812) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 16.599 | 19 | 181,183 (1.812) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 17.489 | 18 | 182,266 (1.823) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 17.676 | 19 | 181,104 (1.811) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 17.570 | 19 | 181,104 (1.811) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 17.690 | 20 | 150,451 (1.505) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 17.709 | 19 | 150,451 (1.505) | yes | - |
| backlog | 0 | 14.213 | 21 | 158,375 (1.584) | yes | - |
| backlog-adp | 0 | 15.807 | 20 | 180,985 (1.810) | yes | - |
| backlog-adp-refill | 0 | 41.098 | 24 | 180,985 (1.810) | yes | - |
| backlog-owed | 0 | 360.544 | 66 | 151,196 (1.512) | yes | - |

Composed maximum over the 4 backlog windows: 180,985 CPU cycles (1.810 ms), backlog-adp.
Over the windows that released their whole load only: 180,985 (1.810 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 8665 | 0 | 160,975 (1.610) | fits |
| save-starved | 52030 | 0 | 163,735 (1.637) | fits |
| backlog-adp@blank-0 | 387 | 0 | 181,272 (1.813) | fits |
| backlog-adp@blank-1 | 387 | 0 | 181,374 (1.814) | fits |
| backlog-adp@blank-2 | 388 | 0 | 181,374 (1.814) | fits |
| backlog-adp@blank-3 | 389 | 0 | 181,374 (1.814) | fits |
| backlog-adp@blank-4 | 388 | 0 | 181,374 (1.814) | fits |
| backlog-adp@blank-5 | 389 | 0 | 181,374 (1.814) | fits |
| backlog-adp@blank-6 | 389 | 0 | 151,229 (1.512) | fits |
| backlog-adp@blank-7 | 387 | 0 | 151,063 (1.511) | fits |
| backlog-adp@program-0 | 497 | 0 | 180,450 (1.804) | fits |
| backlog-adp@program-1 | 499 | 0 | 180,450 (1.804) | fits |
| backlog-adp@program-2 | 499 | 0 | 180,450 (1.804) | fits |
| backlog-adp@program-3 | 497 | 0 | 151,158 (1.512) | fits |
| backlog-adp@program-4 | 498 | 0 | 180,212 (1.802) | fits |
| backlog-adp@program-5 | 500 | 0 | 180,312 (1.803) | fits |
| backlog-adp@program-6 | 500 | 0 | 180,411 (1.804) | fits |
| backlog-adp@program-7 | 499 | 0 | 150,997 (1.510) | fits |
| backlog-adp@verify-0 | 604 | 0 | 181,162 (1.812) | fits |
| backlog-adp@verify-1 | 604 | 0 | 181,264 (1.813) | fits |
| backlog-adp@verify-2 | 606 | 0 | 181,264 (1.813) | fits |
| backlog-adp@verify-3 | 606 | 0 | 181,264 (1.813) | fits |
| backlog-adp@verify-4 | 606 | 0 | 181,264 (1.813) | fits |
| backlog-adp@verify-5 | 605 | 0 | 181,264 (1.813) | fits |
| backlog-adp@verify-6 | 607 | 0 | 151,071 (1.511) | fits |
| backlog-adp@verify-7 | 606 | 0 | 151,114 (1.511) | fits |
| backlog-adp@blank-aged2-0 | 631 | 0 | 181,279 (1.813) | fits |
| backlog-adp@blank-aged2-1 | 637 | 0 | 181,279 (1.813) | fits |
| backlog-adp@blank-aged2-2 | 644 | 0 | 182,362 (1.824) | fits |
| backlog-adp@blank-aged2-3 | 651 | 0 | 181,358 (1.814) | fits |
| backlog-adp@blank-aged2-4 | 657 | 0 | 181,358 (1.814) | fits |
| backlog-adp@blank-aged2-5 | 663 | 0 | 181,358 (1.814) | fits |
| backlog-adp@blank-aged2-6 | 669 | 0 | 150,609 (1.506) | fits |
| backlog-adp@blank-aged2-7 | 676 | 0 | 150,443 (1.504) | fits |
| backlog-adp@program-aged2-0 | 739 | 0 | 180,374 (1.804) | fits |
| backlog-adp@program-aged2-1 | 744 | 0 | 180,330 (1.803) | fits |
| backlog-adp@program-aged2-2 | 750 | 0 | 180,330 (1.803) | fits |
| backlog-adp@program-aged2-3 | 757 | 0 | 180,330 (1.803) | fits |
| backlog-adp@program-aged2-4 | 764 | 0 | 181,413 (1.814) | fits |
| backlog-adp@program-aged2-5 | 770 | 0 | 180,251 (1.803) | fits |
| backlog-adp@program-aged2-6 | 776 | 0 | 150,521 (1.505) | fits |
| backlog-adp@program-aged2-7 | 782 | 0 | 150,518 (1.505) | fits |
| backlog-adp@verify-aged2-0 | 843 | 0 | 181,183 (1.812) | fits |
| backlog-adp@verify-aged2-1 | 849 | 0 | 181,183 (1.812) | fits |
| backlog-adp@verify-aged2-2 | 856 | 0 | 181,183 (1.812) | fits |
| backlog-adp@verify-aged2-3 | 862 | 0 | 182,266 (1.823) | fits |
| backlog-adp@verify-aged2-4 | 869 | 0 | 181,104 (1.811) | fits |
| backlog-adp@verify-aged2-5 | 875 | 0 | 181,104 (1.811) | fits |
| backlog-adp@verify-aged2-6 | 882 | 0 | 150,451 (1.505) | fits |
| backlog-adp@verify-aged2-7 | 888 | 0 | 150,451 (1.505) | fits |
| save | 625 | 0 | 126,478 (1.265) | fits |
| backlog | 309 | 0 | 158,375 (1.584) | fits |
| backlog-adp | 317 | 0 | 180,985 (1.810) | fits |
| backlog-adp-refill | 321 | 0 | 180,985 (1.810) | fits |
| backlog-owed | 365 | 0 | 151,196 (1.512) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +10.251 ms, 77,782 (0.778 ms), read-back | none | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 15.552 (18) | 2.448 |
| backlog-adp@blank-aged2-1 | 2 | +9.000 ms, 77,782 (0.778 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 15.506 (18) | 2.494 |
| backlog-adp@blank-aged2-2 | 2 | +8.076 ms, 77,815 (0.778 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 15.600 (18) | 2.400 |
| backlog-adp@blank-aged2-3 | 2 | +6.731 ms, 77,253 (0.773 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 15.661 (18) | 2.339 |
| backlog-adp@blank-aged2-4 | 2 | +6.378 ms, 77,342 (0.773 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 15.830 (18) | 2.170 |
| backlog-adp@blank-aged2-5 | 2 | +4.972 ms, 77,931 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 15.803 (18) | 2.197 |
| backlog-adp@blank-aged2-6 | 2 | +3.413 ms, 78,009 (0.780 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 15.777 (18) | 2.223 |
| backlog-adp@blank-aged2-7 | 2 | +2.580 ms, 78,009 (0.780 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 15.950 (18) | 2.050 |
| backlog-adp@program-aged2-0 | 2 | +10.192 ms, 83,807 (0.838 ms), issue | none | `backlog-adp@program-aged2-0.service.srp.last.if1` | 15.814 (18) | 2.186 |
| backlog-adp@program-aged2-1 | 2 | +8.976 ms, 83,728 (0.837 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if1` | 15.658 (18) | 2.342 |
| backlog-adp@program-aged2-2 | 2 | +7.622 ms, 84,117 (0.841 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if1` | 15.653 (18) | 2.347 |
| backlog-adp@program-aged2-3 | 2 | +6.613 ms, 83,029 (0.830 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if1` | 15.602 (18) | 2.398 |
| backlog-adp@program-aged2-4 | 2 | +6.272 ms, 83,029 (0.830 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if1` | 15.936 (18) | 2.064 |
| backlog-adp@program-aged2-5 | 2 | +5.055 ms, 83,980 (0.840 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if1` | 15.949 (18) | 2.051 |
| backlog-adp@program-aged2-6 | 2 | +3.505 ms, 84,058 (0.841 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if1` | 15.927 (18) | 2.073 |
| backlog-adp@program-aged2-7 | 2 | +2.464 ms, 84,058 (0.841 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if1` | 15.894 (18) | 2.106 |
| backlog-adp@verify-aged2-0 | 2 | +10.179 ms, 78,569 (0.786 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 15.920 (18) | 2.080 |
| backlog-adp@verify-aged2-1 | 2 | +8.930 ms, 78,569 (0.786 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 15.876 (18) | 2.124 |
| backlog-adp@verify-aged2-2 | 2 | +8.107 ms, 78,648 (0.786 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 15.965 (18) | 2.035 |
| backlog-adp@verify-aged2-3 | 2 | +6.578 ms, 78,086 (0.781 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 15.832 (18) | 2.168 |
| backlog-adp@verify-aged2-4 | 2 | +5.366 ms, 78,764 (0.788 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 16.275 (18) | 1.725 |
| backlog-adp@verify-aged2-5 | 2 | +5.008 ms, 78,764 (0.788 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 16.165 (18) | 1.835 |
| backlog-adp@verify-aged2-6 | 2 | +3.459 ms, 78,842 (0.788 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 16.285 (18) | 1.715 |
| backlog-adp@verify-aged2-7 | 2 | +3.415 ms, 78,842 (0.788 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 16.307 (18) | 1.693 |

Least margin over the aged windows: 1.693 ms, `backlog-adp@verify-aged2-7.service.srp.last.if1` at 16.307 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4696.920 | 12,110 | 370 | - | 18.348 | no | within |
| save-starved | 12086.709 | 12,110 | 370 | - | 31.106 | yes | within |
| save | 4697.337 | 12,110 | 370 | - | 11.280 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1527 | 127,428 (1.274) | 96,034 (0.960) |
| save-starved | 687 | 97,806 (0.978) | 95,745 (0.957) |
| backlog-adp@blank-0 | 337 | 99,308 (0.993) | 75,960 (0.760) |
| backlog-adp@blank-1 | 337 | 99,161 (0.992) | 75,881 (0.759) |
| backlog-adp@blank-2 | 337 | 98,993 (0.990) | 75,881 (0.759) |
| backlog-adp@blank-3 | 338 | 99,141 (0.991) | 75,881 (0.759) |
| backlog-adp@blank-4 | 337 | 99,502 (0.995) | 76,078 (0.761) |
| backlog-adp@blank-5 | 337 | 99,230 (0.992) | 75,960 (0.760) |
| backlog-adp@blank-6 | 337 | 99,230 (0.992) | 75,960 (0.760) |
| backlog-adp@blank-7 | 337 | 99,308 (0.993) | 75,960 (0.760) |
| backlog-adp@program-0 | 443 | 120,667 (1.207) | 81,946 (0.819) |
| backlog-adp@program-1 | 444 | 120,667 (1.207) | 81,867 (0.819) |
| backlog-adp@program-2 | 443 | 120,667 (1.207) | 81,921 (0.819) |
| backlog-adp@program-3 | 443 | 120,667 (1.207) | 81,946 (0.819) |
| backlog-adp@program-4 | 444 | 120,667 (1.207) | 81,435 (0.814) |
| backlog-adp@program-5 | 444 | 120,667 (1.207) | 81,435 (0.814) |
| backlog-adp@program-6 | 444 | 120,667 (1.207) | 81,435 (0.814) |
| backlog-adp@program-7 | 444 | 120,667 (1.207) | 81,435 (0.814) |
| backlog-adp@verify-0 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-1 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-2 | 547 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-3 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-4 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-5 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-6 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-7 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@blank-aged2-0 | 335 | 77,782 (0.778) | 75,864 (0.759) |
| backlog-adp@blank-aged2-1 | 335 | 77,782 (0.778) | 75,864 (0.759) |
| backlog-adp@blank-aged2-2 | 335 | 77,815 (0.778) | 75,864 (0.759) |
| backlog-adp@blank-aged2-3 | 336 | 98,340 (0.983) | 75,864 (0.759) |
| backlog-adp@blank-aged2-4 | 336 | 99,165 (0.992) | 75,881 (0.759) |
| backlog-adp@blank-aged2-5 | 336 | 99,244 (0.992) | 75,960 (0.760) |
| backlog-adp@blank-aged2-6 | 336 | 99,244 (0.992) | 75,960 (0.760) |
| backlog-adp@blank-aged2-7 | 336 | 99,230 (0.992) | 75,960 (0.760) |
| backlog-adp@program-aged2-0 | 441 | 120,667 (1.207) | 81,784 (0.818) |
| backlog-adp@program-aged2-1 | 441 | 120,667 (1.207) | 81,784 (0.818) |
| backlog-adp@program-aged2-2 | 441 | 120,667 (1.207) | 81,910 (0.819) |
| backlog-adp@program-aged2-3 | 442 | 120,667 (1.207) | 81,784 (0.818) |
| backlog-adp@program-aged2-4 | 442 | 120,667 (1.207) | 81,784 (0.818) |
| backlog-adp@program-aged2-5 | 442 | 120,667 (1.207) | 81,845 (0.818) |
| backlog-adp@program-aged2-6 | 442 | 120,667 (1.207) | 81,845 (0.818) |
| backlog-adp@program-aged2-7 | 442 | 120,667 (1.207) | 81,845 (0.818) |
| backlog-adp@verify-aged2-0 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-aged2-1 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-aged2-2 | 546 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-aged2-3 | 547 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-aged2-4 | 547 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-aged2-5 | 547 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-aged2-6 | 547 | 120,667 (1.207) | 95,348 (0.953) |
| backlog-adp@verify-aged2-7 | 547 | 120,667 (1.207) | 95,348 (0.953) |
| save | 585 | 126,478 (1.265) | 95,396 (0.954) |
| backlog | 266 | 49,079 (0.491) | 2,499 (0.025) |
| backlog-adp | 271 | 49,079 (0.491) | 2,479 (0.025) |
| backlog-adp-refill | 273 | 49,079 (0.491) | 2,479 (0.025) |
| backlog-owed | 305 | 49,079 (0.491) | 2,479 (0.025) |

Longest pass that carries a step: 127,428 CPU cycles (1.274 ms), save-held; longest step: 96,034 (0.960 ms), save-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 441,658 | 4.417 | 20 | 200 | fits | 111,488 | 85 | 0.556 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 769,527 | 7.695 | 20 | 20 | fits | 87,480 | 39 | 0.724 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 963,428 | 9.634 | 20 | 24 | fits | 30,382 | 23 | 0.576 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 482,346 | 4.823 | 20 | 50 | fits | 100,300 | 56 | 0.648 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 1,359,284 | 13.593 | 18 | 18 | fits | 49,071 | 28 | 0.723 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 462,538 | 4.625 | 20 | 200 | fits | 105,419 | 69 | 0.618 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 790,540 | 7.905 | 20 | 20 | fits | 91,282 | 45 | 0.737 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 1,037,859 | 10.379 | 20 | 24 | fits | 34,091 | 29 | 0.633 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 494,494 | 4.945 | 20 | 50 | fits | 103,416 | 62 | 0.665 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,426,116 | 14.261 | 18 | 18 | fits | 53,300 | 34 | 0.746 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 509,538 | 5.095 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 186,147 | 1.861 | 20 | 200 | fits | 114,356 | 140 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 637,296 | 6.373 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 187,059 | 1.871 | 20 | 20 | fits | 114,356 | 140 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 850,997 | 8.510 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 190,644 | 1.906 | 20 | 24 | fits | 114,356 | 140 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,505,247 | 15.052 | 20 | 24 | fits | 60,318 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 189,604 | 1.896 | 20 | 50 | fits | 114,356 | 140 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 640,972 | 6.410 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 370,421 | 3.704 | 18 | 18 | fits | 181,272 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,547,346 | 15.473 | 18 | 18 | fits | 44,634 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 437,839 | 4.378 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 114,413 | 1.144 | 20 | 200 | fits | 113,758 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 565,597 | 5.656 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 115,325 | 1.153 | 20 | 20 | fits | 113,758 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 779,298 | 7.793 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 118,910 | 1.189 | 20 | 24 | fits | 113,758 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,444,823 | 14.448 | 20 | 24 | fits | 60,443 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 117,870 | 1.179 | 20 | 50 | fits | 113,758 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 569,273 | 5.693 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 298,789 | 2.988 | 18 | 18 | fits | 181,374 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,476,132 | 14.761 | 18 | 18 | fits | 33,844 | 17 | 0.763 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 436,032 | 4.360 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 112,606 | 1.126 | 20 | 200 | fits | 113,758 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 563,790 | 5.638 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 113,518 | 1.135 | 20 | 20 | fits | 113,758 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 748,853 | 7.489 | 20 | 20 | fits | 68,003 | 25 | 0.651 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 117,103 | 1.171 | 20 | 24 | fits | 113,758 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,413,360 | 14.134 | 20 | 24 | fits | 60,157 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 116,063 | 1.161 | 20 | 50 | fits | 113,758 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 567,466 | 5.675 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 296,982 | 2.970 | 18 | 18 | fits | 181,374 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,487,979 | 14.880 | 18 | 18 | fits | 32,427 | 15 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 434,225 | 4.342 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 110,799 | 1.108 | 20 | 200 | fits | 113,758 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 561,983 | 5.620 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 111,711 | 1.117 | 20 | 20 | fits | 113,758 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 810,989 | 8.110 | 20 | 20 | fits | 87,153 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 115,296 | 1.153 | 20 | 24 | fits | 113,758 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,416,132 | 14.161 | 20 | 24 | fits | 60,182 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 114,256 | 1.143 | 20 | 50 | fits | 113,758 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 565,659 | 5.657 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 295,175 | 2.952 | 18 | 18 | fits | 181,374 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,490,259 | 14.903 | 18 | 18 | fits | 32,227 | 15 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 432,418 | 4.324 | 20 | 20 | fits | 110,274 | 74 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 108,992 | 1.090 | 20 | 200 | fits | 113,758 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 531,392 | 5.314 | 20 | 200 | fits | 110,274 | 74 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 109,904 | 1.099 | 20 | 20 | fits | 113,758 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 808,826 | 8.088 | 20 | 20 | fits | 88,095 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 113,489 | 1.135 | 20 | 24 | fits | 113,758 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,413,906 | 14.139 | 20 | 24 | fits | 60,182 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 112,449 | 1.124 | 20 | 50 | fits | 113,758 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 535,068 | 5.351 | 20 | 50 | fits | 110,274 | 74 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 293,368 | 2.934 | 18 | 18 | fits | 181,374 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,495,719 | 14.957 | 18 | 18 | fits | 39,913 | 19 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 513,312 | 5.133 | 20 | 20 | fits | 126,165 | 57 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 124,692 | 1.247 | 20 | 200 | fits | 113,758 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 629,907 | 6.299 | 20 | 200 | fits | 126,165 | 57 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 125,604 | 1.256 | 20 | 20 | fits | 113,758 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 824,854 | 8.249 | 20 | 20 | fits | 78,481 | 27 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 129,189 | 1.292 | 20 | 24 | fits | 113,758 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,399,693 | 13.997 | 20 | 24 | fits | 55,649 | 32 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 128,149 | 1.281 | 20 | 50 | fits | 113,758 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 507,418 | 5.074 | 20 | 50 | fits | 95,807 | 64 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 309,068 | 3.091 | 18 | 18 | fits | 181,374 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,527,878 | 15.279 | 18 | 18 | fits | 42,930 | 18 | 0.678 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 513,306 | 5.133 | 20 | 20 | fits | 127,651 | 57 | 0.693 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 122,977 | 1.230 | 20 | 200 | fits | 113,758 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 630,494 | 6.305 | 20 | 200 | fits | 127,651 | 57 | 0.693 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 123,889 | 1.239 | 20 | 20 | fits | 113,758 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 825,364 | 8.254 | 20 | 20 | fits | 78,374 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 127,474 | 1.275 | 20 | 24 | fits | 113,758 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,400,541 | 14.005 | 20 | 24 | fits | 60,318 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 126,434 | 1.264 | 20 | 50 | fits | 113,758 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 506,519 | 5.065 | 20 | 50 | fits | 151,229 | 98 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 355,225 | 3.552 | 18 | 18 | fits | 120,673 | 64 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,528,704 | 15.287 | 18 | 18 | fits | 42,930 | 18 | 0.678 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 542,180 | 5.422 | 20 | 20 | fits | 127,074 | 57 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 121,170 | 1.212 | 20 | 200 | fits | 113,758 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 659,252 | 6.593 | 20 | 200 | fits | 127,074 | 57 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 122,082 | 1.221 | 20 | 20 | fits | 113,758 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 854,120 | 8.541 | 20 | 20 | fits | 78,374 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 125,667 | 1.257 | 20 | 24 | fits | 113,758 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,458,859 | 14.589 | 20 | 24 | fits | 60,420 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 124,627 | 1.246 | 20 | 50 | fits | 113,758 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 535,854 | 5.359 | 20 | 50 | fits | 130,622 | 98 | 0.597 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 254,104 | 2.541 | 18 | 18 | fits | 129,932 | 105 | 0.694 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,500,856 | 15.009 | 18 | 18 | fits | 44,532 | 20 | 0.705 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 444,181 | 4.442 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 121,659 | 1.217 | 20 | 200 | fits | 114,335 | 140 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 571,939 | 5.719 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 122,571 | 1.226 | 20 | 20 | fits | 114,335 | 140 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 785,640 | 7.856 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 126,156 | 1.262 | 20 | 24 | fits | 114,335 | 140 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,439,890 | 14.399 | 20 | 24 | fits | 60,318 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 125,116 | 1.251 | 20 | 50 | fits | 114,335 | 140 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 575,615 | 5.756 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 305,111 | 3.051 | 18 | 18 | fits | 180,450 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,481,989 | 14.820 | 18 | 18 | fits | 44,634 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 440,567 | 4.406 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 118,045 | 1.180 | 20 | 200 | fits | 114,335 | 140 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 568,325 | 5.683 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 118,957 | 1.190 | 20 | 20 | fits | 114,335 | 140 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 817,331 | 8.173 | 20 | 20 | fits | 87,153 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 122,542 | 1.225 | 20 | 24 | fits | 114,335 | 140 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,422,474 | 14.225 | 20 | 24 | fits | 60,182 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 121,502 | 1.215 | 20 | 50 | fits | 114,335 | 140 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 572,001 | 5.720 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 301,497 | 3.015 | 18 | 18 | fits | 180,450 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,496,601 | 14.966 | 18 | 18 | fits | 32,227 | 15 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 502,195 | 5.022 | 20 | 20 | fits | 126,165 | 57 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 114,431 | 1.144 | 20 | 200 | fits | 114,335 | 140 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 618,790 | 6.188 | 20 | 200 | fits | 126,165 | 57 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 115,343 | 1.153 | 20 | 20 | fits | 114,335 | 140 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 813,737 | 8.137 | 20 | 20 | fits | 78,481 | 27 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 118,928 | 1.189 | 20 | 24 | fits | 114,335 | 140 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,393,186 | 13.932 | 20 | 24 | fits | 32,868 | 22 | 0.653 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 117,888 | 1.179 | 20 | 50 | fits | 114,335 | 140 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 496,301 | 4.963 | 20 | 50 | fits | 95,855 | 64 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 297,883 | 2.979 | 18 | 18 | fits | 180,450 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,518,999 | 15.190 | 18 | 18 | fits | 42,962 | 18 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 531,169 | 5.312 | 20 | 20 | fits | 127,074 | 57 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 110,817 | 1.108 | 20 | 200 | fits | 114,335 | 140 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 648,241 | 6.482 | 20 | 200 | fits | 127,074 | 57 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 111,729 | 1.117 | 20 | 20 | fits | 114,335 | 140 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 843,142 | 8.431 | 20 | 20 | fits | 78,407 | 27 | 0.770 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 115,314 | 1.153 | 20 | 24 | fits | 114,335 | 140 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,447,938 | 14.479 | 20 | 24 | fits | 60,395 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 114,274 | 1.143 | 20 | 50 | fits | 114,335 | 140 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 524,843 | 5.248 | 20 | 50 | fits | 130,705 | 98 | 0.598 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 242,915 | 2.429 | 18 | 18 | fits | 129,096 | 105 | 0.695 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,490,227 | 14.902 | 18 | 18 | fits | 44,824 | 20 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 433,123 | 4.331 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 110,839 | 1.108 | 20 | 200 | fits | 115,214 | 140 | 0.539 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 560,881 | 5.609 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 111,751 | 1.118 | 20 | 20 | fits | 115,214 | 140 | 0.539 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 774,582 | 7.746 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 115,336 | 1.153 | 20 | 24 | fits | 115,214 | 140 | 0.539 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,439,617 | 14.396 | 20 | 24 | fits | 60,264 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 114,296 | 1.143 | 20 | 50 | fits | 115,214 | 140 | 0.539 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 564,557 | 5.646 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 294,053 | 2.941 | 18 | 18 | fits | 180,212 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,470,734 | 14.707 | 18 | 18 | fits | 33,652 | 17 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 474,055 | 4.741 | 20 | 20 | fits | 128,374 | 60 | 0.676 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 160,860 | 1.609 | 20 | 200 | fits | 113,962 | 142 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 591,129 | 5.911 | 20 | 200 | fits | 128,374 | 60 | 0.676 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 161,772 | 1.618 | 20 | 20 | fits | 113,962 | 142 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 840,085 | 8.401 | 20 | 20 | fits | 87,153 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 51,395 | 0.514 | 20 | 24 | fits | 52,896 | 65 | 0.553 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,385,170 | 13.852 | 20 | 24 | fits | 60,080 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 50,355 | 0.504 | 20 | 50 | fits | 52,896 | 65 | 0.553 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 466,431 | 4.664 | 20 | 50 | fits | 122,192 | 76 | 0.637 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 344,174 | 3.442 | 18 | 18 | fits | 180,312 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,502,354 | 15.024 | 18 | 18 | fits | 32,023 | 15 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 509,942 | 5.099 | 20 | 20 | fits | 126,165 | 57 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 122,217 | 1.222 | 20 | 200 | fits | 114,230 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 626,537 | 6.265 | 20 | 200 | fits | 126,165 | 57 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 123,129 | 1.231 | 20 | 20 | fits | 114,230 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 821,484 | 8.215 | 20 | 20 | fits | 78,481 | 27 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 126,714 | 1.267 | 20 | 24 | fits | 114,230 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,400,933 | 14.009 | 20 | 24 | fits | 32,868 | 22 | 0.653 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 125,674 | 1.257 | 20 | 50 | fits | 114,230 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 504,048 | 5.040 | 20 | 50 | fits | 95,855 | 64 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 305,630 | 3.056 | 18 | 18 | fits | 180,411 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,526,746 | 15.267 | 18 | 18 | fits | 42,962 | 18 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 538,936 | 5.389 | 20 | 20 | fits | 127,074 | 57 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 118,603 | 1.186 | 20 | 200 | fits | 114,230 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 656,008 | 6.560 | 20 | 200 | fits | 127,074 | 57 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 119,515 | 1.195 | 20 | 20 | fits | 114,230 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 850,876 | 8.509 | 20 | 20 | fits | 78,374 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 123,100 | 1.231 | 20 | 24 | fits | 114,230 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,443,449 | 14.434 | 20 | 24 | fits | 60,264 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 122,060 | 1.221 | 20 | 50 | fits | 114,230 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 532,610 | 5.326 | 20 | 50 | fits | 130,772 | 98 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 250,776 | 2.508 | 18 | 18 | fits | 129,171 | 105 | 0.695 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,517,829 | 15.178 | 18 | 18 | fits | 32,227 | 15 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 442,295 | 4.423 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 118,966 | 1.190 | 20 | 200 | fits | 114,563 | 140 | 0.534 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 570,053 | 5.701 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 119,878 | 1.199 | 20 | 20 | fits | 114,563 | 140 | 0.534 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 783,821 | 7.838 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 123,463 | 1.235 | 20 | 24 | fits | 114,563 | 140 | 0.534 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,469,296 | 14.693 | 20 | 24 | fits | 91,543 | 45 | 0.748 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 122,423 | 1.224 | 20 | 50 | fits | 114,563 | 140 | 0.534 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 573,729 | 5.737 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 303,130 | 3.031 | 18 | 18 | fits | 181,162 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,512,146 | 15.121 | 18 | 18 | fits | 45,385 | 20 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 440,949 | 4.409 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 117,585 | 1.176 | 20 | 200 | fits | 113,979 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 568,707 | 5.687 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 118,497 | 1.185 | 20 | 20 | fits | 113,979 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 782,475 | 7.825 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 122,082 | 1.221 | 20 | 24 | fits | 113,979 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,465,399 | 14.654 | 20 | 24 | fits | 91,160 | 45 | 0.747 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 121,042 | 1.210 | 20 | 50 | fits | 113,979 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 572,383 | 5.724 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 301,851 | 3.019 | 18 | 18 | fits | 181,264 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,508,170 | 15.082 | 18 | 18 | fits | 45,306 | 20 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 439,142 | 4.391 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 115,778 | 1.158 | 20 | 200 | fits | 113,979 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 566,900 | 5.669 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 116,690 | 1.167 | 20 | 20 | fits | 113,979 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 816,030 | 8.160 | 20 | 20 | fits | 87,153 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 120,275 | 1.203 | 20 | 24 | fits | 113,979 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,421,173 | 14.212 | 20 | 24 | fits | 60,182 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 119,235 | 1.192 | 20 | 50 | fits | 113,979 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 570,576 | 5.706 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 300,044 | 3.000 | 18 | 18 | fits | 181,264 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,526,026 | 15.260 | 18 | 18 | fits | 73,977 | 32 | 0.771 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 437,335 | 4.373 | 20 | 20 | fits | 110,274 | 74 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 113,971 | 1.140 | 20 | 200 | fits | 113,979 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 536,309 | 5.363 | 20 | 200 | fits | 110,274 | 74 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 114,883 | 1.149 | 20 | 20 | fits | 113,979 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 813,810 | 8.138 | 20 | 20 | fits | 88,095 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 118,468 | 1.185 | 20 | 24 | fits | 113,979 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,418,890 | 14.189 | 20 | 24 | fits | 60,182 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 117,428 | 1.174 | 20 | 50 | fits | 113,979 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 539,985 | 5.400 | 20 | 50 | fits | 110,274 | 74 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 298,237 | 2.982 | 18 | 18 | fits | 181,264 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,524,607 | 15.246 | 18 | 18 | fits | 32,994 | 14 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 500,770 | 5.008 | 20 | 20 | fits | 126,165 | 57 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 112,164 | 1.122 | 20 | 200 | fits | 113,979 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 617,365 | 6.174 | 20 | 200 | fits | 126,165 | 57 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 113,076 | 1.131 | 20 | 20 | fits | 113,979 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 812,379 | 8.124 | 20 | 20 | fits | 78,481 | 27 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 116,661 | 1.167 | 20 | 24 | fits | 113,979 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,408,035 | 14.080 | 20 | 24 | fits | 49,075 | 27 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 115,621 | 1.156 | 20 | 50 | fits | 113,979 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 494,876 | 4.949 | 20 | 50 | fits | 95,855 | 64 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 296,430 | 2.964 | 18 | 18 | fits | 181,264 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,552,992 | 15.530 | 18 | 18 | fits | 62,751 | 29 | 0.796 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 528,689 | 5.287 | 20 | 20 | fits | 126,995 | 57 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 110,357 | 1.104 | 20 | 200 | fits | 113,979 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 645,682 | 6.457 | 20 | 200 | fits | 126,995 | 57 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 111,269 | 1.113 | 20 | 20 | fits | 113,979 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 840,617 | 8.406 | 20 | 20 | fits | 78,448 | 27 | 0.770 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 114,854 | 1.149 | 20 | 24 | fits | 113,979 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,445,015 | 14.450 | 20 | 24 | fits | 60,395 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 113,814 | 1.138 | 20 | 50 | fits | 113,979 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 522,363 | 5.224 | 20 | 50 | fits | 129,035 | 98 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 294,623 | 2.946 | 18 | 18 | fits | 181,264 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,538,789 | 15.388 | 18 | 18 | fits | 62,890 | 29 | 0.798 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 498,846 | 4.988 | 20 | 20 | fits | 127,651 | 57 | 0.693 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 108,550 | 1.085 | 20 | 200 | fits | 113,979 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 616,034 | 6.160 | 20 | 200 | fits | 127,651 | 57 | 0.693 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 109,462 | 1.095 | 20 | 20 | fits | 113,979 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 810,971 | 8.110 | 20 | 20 | fits | 78,374 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 113,047 | 1.130 | 20 | 24 | fits | 113,979 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,386,678 | 13.867 | 20 | 24 | fits | 60,497 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 112,007 | 1.120 | 20 | 50 | fits | 113,979 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 492,059 | 4.921 | 20 | 50 | fits | 151,071 | 98 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 340,923 | 3.409 | 18 | 18 | fits | 120,750 | 64 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,515,161 | 15.152 | 18 | 18 | fits | 42,962 | 18 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 545,392 | 5.454 | 20 | 20 | fits | 127,074 | 57 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 124,342 | 1.243 | 20 | 200 | fits | 113,979 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 662,464 | 6.625 | 20 | 200 | fits | 127,074 | 57 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 125,254 | 1.253 | 20 | 20 | fits | 113,979 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 857,432 | 8.574 | 20 | 20 | fits | 78,407 | 27 | 0.770 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 128,839 | 1.288 | 20 | 24 | fits | 113,979 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,450,219 | 14.502 | 20 | 24 | fits | 60,264 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 127,799 | 1.278 | 20 | 50 | fits | 113,979 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 539,066 | 5.391 | 20 | 50 | fits | 130,670 | 98 | 0.597 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 257,217 | 2.572 | 18 | 18 | fits | 129,873 | 105 | 0.693 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,524,507 | 15.245 | 18 | 18 | fits | 32,135 | 14 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 439,445 | 4.394 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 116,114 | 1.161 | 20 | 200 | fits | 113,045 | 134 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 567,203 | 5.672 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 117,026 | 1.170 | 20 | 20 | fits | 113,045 | 134 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 780,904 | 7.809 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 120,611 | 1.206 | 20 | 24 | fits | 113,045 | 134 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 1,524,039 | 15.240 | 20 | 24 | fits | 60,264 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 119,571 | 1.196 | 20 | 50 | fits | 113,045 | 134 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 570,879 | 5.709 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 300,395 | 3.004 | 18 | 18 | fits | 181,279 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 1,555,156 | 15.552 | 18 | 18 | fits | 33,652 | 17 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 434,793 | 4.348 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 111,462 | 1.115 | 20 | 200 | fits | 113,045 | 134 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 562,551 | 5.626 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 112,374 | 1.124 | 20 | 20 | fits | 113,045 | 134 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 776,252 | 7.763 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 115,959 | 1.160 | 20 | 24 | fits | 113,045 | 134 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 1,519,489 | 15.195 | 20 | 24 | fits | 60,264 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 114,919 | 1.149 | 20 | 50 | fits | 113,045 | 134 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 566,227 | 5.662 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 295,743 | 2.957 | 18 | 18 | fits | 181,279 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 1,550,606 | 15.506 | 18 | 18 | fits | 33,652 | 17 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 430,841 | 4.308 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 106,427 | 1.064 | 20 | 200 | fits | 113,045 | 134 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 558,599 | 5.586 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 107,339 | 1.073 | 20 | 20 | fits | 113,045 | 134 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 743,662 | 7.437 | 20 | 20 | fits | 68,003 | 25 | 0.651 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 110,924 | 1.109 | 20 | 24 | fits | 113,045 | 134 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 1,485,837 | 14.858 | 20 | 24 | fits | 60,182 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 109,884 | 1.099 | 20 | 50 | fits | 113,045 | 134 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 562,275 | 5.623 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 291,791 | 2.918 | 18 | 18 | fits | 182,362 | 145 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 1,559,964 | 15.600 | 18 | 18 | fits | 32,227 | 15 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 445,626 | 4.456 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 122,216 | 1.222 | 20 | 200 | fits | 113,045 | 134 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 573,384 | 5.734 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 123,128 | 1.231 | 20 | 20 | fits | 113,045 | 134 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 929,419 | 9.294 | 20 | 20 | fits | 87,920 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 126,713 | 1.267 | 20 | 24 | fits | 113,045 | 134 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 1,534,978 | 15.350 | 20 | 24 | fits | 60,157 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 125,673 | 1.257 | 20 | 50 | fits | 113,045 | 134 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 577,060 | 5.771 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 306,576 | 3.066 | 18 | 18 | fits | 181,358 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 1,566,134 | 15.661 | 18 | 18 | fits | 33,691 | 17 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 440,974 | 4.410 | 20 | 20 | fits | 110,274 | 74 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 117,564 | 1.176 | 20 | 200 | fits | 113,045 | 134 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 539,948 | 5.399 | 20 | 200 | fits | 110,274 | 74 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 118,476 | 1.185 | 20 | 20 | fits | 113,045 | 134 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 894,542 | 8.945 | 20 | 20 | fits | 88,106 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 122,061 | 1.221 | 20 | 24 | fits | 113,045 | 134 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 1,497,315 | 14.973 | 20 | 24 | fits | 57,432 | 32 | 0.756 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 121,021 | 1.210 | 20 | 50 | fits | 113,045 | 134 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 543,624 | 5.436 | 20 | 50 | fits | 110,274 | 74 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 301,924 | 3.019 | 18 | 18 | fits | 181,358 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 1,582,977 | 15.830 | 18 | 18 | fits | 43,334 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 578,675 | 5.787 | 20 | 20 | fits | 125,839 | 57 | 0.689 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 112,912 | 1.129 | 20 | 200 | fits | 113,045 | 134 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 695,716 | 6.957 | 20 | 200 | fits | 125,839 | 57 | 0.689 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 113,824 | 1.138 | 20 | 20 | fits | 113,045 | 134 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 890,384 | 8.904 | 20 | 20 | fits | 78,287 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 117,409 | 1.174 | 20 | 24 | fits | 113,045 | 134 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 1,494,657 | 14.947 | 20 | 24 | fits | 60,395 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 116,369 | 1.164 | 20 | 50 | fits | 113,045 | 134 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 495,622 | 4.956 | 20 | 50 | fits | 95,807 | 64 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 297,272 | 2.973 | 18 | 18 | fits | 181,358 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 1,580,280 | 15.803 | 18 | 18 | fits | 43,334 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 575,140 | 5.751 | 20 | 20 | fits | 127,679 | 57 | 0.693 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 106,427 | 1.064 | 20 | 200 | fits | 113,045 | 134 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 692,356 | 6.924 | 20 | 200 | fits | 127,679 | 57 | 0.693 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 107,339 | 1.073 | 20 | 20 | fits | 113,045 | 134 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 887,226 | 8.872 | 20 | 20 | fits | 78,374 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 110,924 | 1.109 | 20 | 24 | fits | 113,045 | 134 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 1,492,085 | 14.921 | 20 | 24 | fits | 60,395 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 109,884 | 1.099 | 20 | 50 | fits | 113,045 | 134 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 568,353 | 5.684 | 20 | 50 | fits | 150,609 | 98 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 339,670 | 3.397 | 18 | 18 | fits | 120,705 | 64 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 1,577,708 | 15.777 | 18 | 18 | fits | 43,334 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 621,938 | 6.219 | 20 | 20 | fits | 127,074 | 57 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 123,574 | 1.236 | 20 | 200 | fits | 113,045 | 134 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 739,010 | 7.390 | 20 | 200 | fits | 127,074 | 57 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 124,486 | 1.245 | 20 | 20 | fits | 113,045 | 134 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 933,878 | 9.339 | 20 | 20 | fits | 78,374 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 128,071 | 1.281 | 20 | 24 | fits | 113,045 | 134 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 1,509,762 | 15.098 | 20 | 24 | fits | 60,318 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 127,031 | 1.270 | 20 | 50 | fits | 113,045 | 134 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 615,612 | 6.156 | 20 | 50 | fits | 130,754 | 98 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 256,341 | 2.563 | 18 | 18 | fits | 129,765 | 105 | 0.693 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 1,594,995 | 15.950 | 18 | 18 | fits | 43,134 | 18 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 474,113 | 4.741 | 20 | 20 | fits | 128,374 | 60 | 0.676 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 160,923 | 1.609 | 20 | 200 | fits | 113,007 | 136 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 591,187 | 5.912 | 20 | 200 | fits | 128,374 | 60 | 0.676 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 161,835 | 1.618 | 20 | 20 | fits | 113,007 | 136 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 804,337 | 8.043 | 20 | 20 | fits | 96,715 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 52,413 | 0.524 | 20 | 24 | fits | 57,080 | 71 | 0.585 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 1,464,209 | 14.642 | 20 | 24 | fits | 60,366 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 51,373 | 0.514 | 20 | 50 | fits | 57,080 | 71 | 0.585 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 466,489 | 4.665 | 20 | 50 | fits | 122,125 | 76 | 0.636 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 344,299 | 3.443 | 18 | 18 | fits | 180,374 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if1` | 1,581,442 | 15.814 | 18 | 18 | fits | 32,023 | 15 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 443,203 | 4.432 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 120,801 | 1.208 | 20 | 200 | fits | 113,632 | 134 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 570,961 | 5.710 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 121,713 | 1.217 | 20 | 20 | fits | 113,632 | 134 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 784,662 | 7.847 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 125,298 | 1.253 | 20 | 24 | fits | 113,632 | 134 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 1,523,745 | 15.237 | 20 | 24 | fits | 60,318 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 124,258 | 1.243 | 20 | 50 | fits | 113,632 | 134 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 574,637 | 5.746 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 304,133 | 3.041 | 18 | 18 | fits | 180,330 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if1` | 1,565,844 | 15.658 | 18 | 18 | fits | 44,634 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 438,551 | 4.386 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 116,149 | 1.161 | 20 | 200 | fits | 113,632 | 134 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 566,309 | 5.663 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 117,061 | 1.171 | 20 | 20 | fits | 113,632 | 134 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 929,147 | 9.291 | 20 | 20 | fits | 87,409 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 120,646 | 1.206 | 20 | 24 | fits | 113,632 | 134 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 1,534,349 | 15.343 | 20 | 24 | fits | 60,182 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 119,606 | 1.196 | 20 | 50 | fits | 113,632 | 134 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 569,985 | 5.700 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 299,481 | 2.995 | 18 | 18 | fits | 180,330 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if1` | 1,565,317 | 15.653 | 18 | 18 | fits | 33,503 | 17 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 433,899 | 4.339 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 111,497 | 1.115 | 20 | 200 | fits | 113,632 | 134 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 561,657 | 5.617 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 112,409 | 1.124 | 20 | 20 | fits | 113,632 | 134 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 923,523 | 9.235 | 20 | 20 | fits | 87,860 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 115,994 | 1.160 | 20 | 24 | fits | 113,632 | 134 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 1,529,082 | 15.291 | 20 | 24 | fits | 60,157 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 114,954 | 1.150 | 20 | 50 | fits | 113,632 | 134 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 565,333 | 5.653 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 294,829 | 2.948 | 18 | 18 | fits | 180,330 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if1` | 1,560,238 | 15.602 | 18 | 18 | fits | 33,691 | 17 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 430,330 | 4.303 | 20 | 20 | fits | 110,274 | 74 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 106,845 | 1.068 | 20 | 200 | fits | 113,632 | 134 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 529,304 | 5.293 | 20 | 200 | fits | 110,274 | 74 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 107,757 | 1.078 | 20 | 20 | fits | 113,632 | 134 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 889,492 | 8.895 | 20 | 20 | fits | 87,972 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 111,342 | 1.113 | 20 | 24 | fits | 113,632 | 134 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 1,467,701 | 14.677 | 20 | 24 | fits | 32,868 | 22 | 0.653 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 110,302 | 1.103 | 20 | 50 | fits | 113,632 | 134 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 532,980 | 5.330 | 20 | 50 | fits | 110,274 | 74 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 291,260 | 2.913 | 18 | 18 | fits | 181,413 | 145 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if1` | 1,593,559 | 15.936 | 18 | 18 | fits | 42,962 | 18 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 593,045 | 5.930 | 20 | 20 | fits | 126,011 | 57 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 122,251 | 1.223 | 20 | 200 | fits | 113,632 | 134 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 710,237 | 7.102 | 20 | 200 | fits | 126,011 | 57 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 123,163 | 1.232 | 20 | 20 | fits | 113,632 | 134 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 905,041 | 9.050 | 20 | 20 | fits | 78,435 | 27 | 0.770 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 126,748 | 1.267 | 20 | 24 | fits | 113,632 | 134 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 1,509,322 | 15.093 | 20 | 24 | fits | 60,395 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 125,708 | 1.257 | 20 | 50 | fits | 113,632 | 134 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 503,922 | 5.039 | 20 | 50 | fits | 95,855 | 64 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 305,504 | 3.055 | 18 | 18 | fits | 180,251 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if1` | 1,594,945 | 15.949 | 18 | 18 | fits | 43,334 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 590,292 | 5.903 | 20 | 20 | fits | 127,612 | 57 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 117,599 | 1.176 | 20 | 200 | fits | 113,632 | 134 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 707,441 | 7.074 | 20 | 200 | fits | 127,612 | 57 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 118,511 | 1.185 | 20 | 20 | fits | 113,632 | 134 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 902,311 | 9.023 | 20 | 20 | fits | 78,374 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 122,096 | 1.221 | 20 | 24 | fits | 113,632 | 134 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 1,507,107 | 15.071 | 20 | 24 | fits | 60,395 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 121,056 | 1.211 | 20 | 50 | fits | 113,632 | 134 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 583,505 | 5.835 | 20 | 50 | fits | 150,521 | 98 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 348,861 | 3.489 | 18 | 18 | fits | 119,838 | 64 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if1` | 1,592,730 | 15.927 | 18 | 18 | fits | 43,334 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 616,413 | 6.164 | 20 | 20 | fits | 127,074 | 57 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 112,947 | 1.129 | 20 | 200 | fits | 113,632 | 134 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 733,485 | 7.335 | 20 | 200 | fits | 127,074 | 57 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 113,859 | 1.139 | 20 | 20 | fits | 113,632 | 134 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 928,386 | 9.284 | 20 | 20 | fits | 78,407 | 27 | 0.770 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 117,444 | 1.174 | 20 | 24 | fits | 113,632 | 134 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 1,504,207 | 15.042 | 20 | 24 | fits | 60,318 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 116,404 | 1.164 | 20 | 50 | fits | 113,632 | 134 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 610,087 | 6.101 | 20 | 50 | fits | 130,735 | 98 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 244,711 | 2.447 | 18 | 18 | fits | 128,762 | 105 | 0.692 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if1` | 1,589,440 | 15.894 | 18 | 18 | fits | 43,134 | 18 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 443,165 | 4.432 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 119,882 | 1.199 | 20 | 200 | fits | 113,196 | 134 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 570,923 | 5.709 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 120,794 | 1.208 | 20 | 20 | fits | 113,196 | 134 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 784,691 | 7.847 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 124,379 | 1.244 | 20 | 24 | fits | 113,196 | 134 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 1,549,802 | 15.498 | 20 | 24 | fits | 60,230 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 123,339 | 1.233 | 20 | 50 | fits | 113,196 | 134 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 574,599 | 5.746 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 304,067 | 3.041 | 18 | 18 | fits | 181,183 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 1,591,959 | 15.920 | 18 | 18 | fits | 44,692 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 438,513 | 4.385 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 115,230 | 1.152 | 20 | 200 | fits | 113,196 | 134 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 566,271 | 5.663 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 116,142 | 1.161 | 20 | 20 | fits | 113,196 | 134 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 780,039 | 7.800 | 20 | 20 | fits | 96,641 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 119,727 | 1.197 | 20 | 24 | fits | 113,196 | 134 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 1,545,443 | 15.454 | 20 | 24 | fits | 60,230 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 118,687 | 1.187 | 20 | 50 | fits | 113,196 | 134 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 569,947 | 5.699 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 299,415 | 2.994 | 18 | 18 | fits | 181,183 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 1,587,600 | 15.876 | 18 | 18 | fits | 44,692 | 20 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 433,861 | 4.339 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 110,578 | 1.106 | 20 | 200 | fits | 113,196 | 134 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 561,619 | 5.616 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 111,490 | 1.115 | 20 | 20 | fits | 113,196 | 134 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 746,749 | 7.467 | 20 | 20 | fits | 68,003 | 25 | 0.651 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 115,075 | 1.151 | 20 | 24 | fits | 113,196 | 134 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 1,521,921 | 15.219 | 20 | 24 | fits | 60,247 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 114,035 | 1.140 | 20 | 50 | fits | 113,196 | 134 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 565,295 | 5.653 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 294,763 | 2.948 | 18 | 18 | fits | 181,183 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 1,596,540 | 15.965 | 18 | 18 | fits | 32,427 | 15 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 430,292 | 4.303 | 20 | 20 | fits | 139,058 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 105,926 | 1.059 | 20 | 200 | fits | 113,196 | 134 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 558,050 | 5.580 | 20 | 200 | fits | 139,058 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 106,838 | 1.068 | 20 | 20 | fits | 113,196 | 134 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 915,105 | 9.151 | 20 | 20 | fits | 87,920 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 110,423 | 1.104 | 20 | 24 | fits | 113,196 | 134 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 1,552,090 | 15.521 | 20 | 24 | fits | 60,259 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 109,383 | 1.094 | 20 | 50 | fits | 113,196 | 134 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 561,726 | 5.617 | 20 | 50 | fits | 139,058 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 291,194 | 2.912 | 18 | 18 | fits | 182,266 | 145 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 1,583,156 | 15.832 | 18 | 18 | fits | 33,601 | 16 | 0.765 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 618,901 | 6.189 | 20 | 20 | fits | 125,523 | 57 | 0.686 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 121,332 | 1.213 | 20 | 200 | fits | 113,196 | 134 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 735,547 | 7.355 | 20 | 200 | fits | 125,523 | 57 | 0.686 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 122,244 | 1.222 | 20 | 20 | fits | 113,196 | 134 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 930,369 | 9.304 | 20 | 20 | fits | 78,387 | 27 | 0.770 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 125,829 | 1.258 | 20 | 24 | fits | 113,196 | 134 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 1,551,303 | 15.513 | 20 | 24 | fits | 85,750 | 46 | 0.762 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 124,789 | 1.248 | 20 | 50 | fits | 113,196 | 134 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 534,936 | 5.349 | 20 | 50 | fits | 98,024 | 64 | 0.711 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 305,438 | 3.054 | 18 | 18 | fits | 181,104 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 1,627,458 | 16.275 | 18 | 18 | fits | 32,427 | 15 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 583,118 | 5.831 | 20 | 20 | fits | 125,680 | 57 | 0.687 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 116,680 | 1.167 | 20 | 200 | fits | 113,196 | 134 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 700,000 | 7.000 | 20 | 200 | fits | 125,680 | 57 | 0.687 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 117,592 | 1.176 | 20 | 20 | fits | 113,196 | 134 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 894,752 | 8.948 | 20 | 20 | fits | 78,315 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 121,177 | 1.212 | 20 | 24 | fits | 113,196 | 134 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 1,530,225 | 15.302 | 20 | 24 | fits | 91,595 | 45 | 0.748 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 120,137 | 1.201 | 20 | 50 | fits | 113,196 | 134 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 499,232 | 4.992 | 20 | 50 | fits | 95,855 | 64 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 300,786 | 3.008 | 18 | 18 | fits | 181,104 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 1,616,520 | 16.165 | 18 | 18 | fits | 43,258 | 18 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 580,350 | 5.803 | 20 | 20 | fits | 127,679 | 57 | 0.693 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 112,028 | 1.120 | 20 | 200 | fits | 113,196 | 134 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 697,566 | 6.976 | 20 | 200 | fits | 127,679 | 57 | 0.693 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 112,940 | 1.129 | 20 | 20 | fits | 113,196 | 134 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 892,503 | 8.925 | 20 | 20 | fits | 78,374 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 116,525 | 1.165 | 20 | 24 | fits | 113,196 | 134 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 1,499,164 | 14.992 | 20 | 24 | fits | 89,810 | 45 | 0.737 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 115,485 | 1.155 | 20 | 50 | fits | 113,196 | 134 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 573,563 | 5.736 | 20 | 50 | fits | 150,451 | 98 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 344,205 | 3.442 | 18 | 18 | fits | 120,753 | 64 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 1,628,541 | 16.285 | 18 | 18 | fits | 42,930 | 18 | 0.678 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 575,983 | 5.760 | 20 | 20 | fits | 127,679 | 57 | 0.693 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 106,578 | 1.066 | 20 | 200 | fits | 113,196 | 134 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 693,199 | 6.932 | 20 | 200 | fits | 127,679 | 57 | 0.693 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 107,490 | 1.075 | 20 | 20 | fits | 113,196 | 134 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 888,136 | 8.881 | 20 | 20 | fits | 78,374 | 27 | 0.769 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 111,075 | 1.111 | 20 | 24 | fits | 113,196 | 134 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 1,481,929 | 14.819 | 20 | 24 | fits | 48,916 | 27 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 110,035 | 1.100 | 20 | 50 | fits | 113,196 | 134 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 569,196 | 5.692 | 20 | 50 | fits | 150,451 | 98 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 339,838 | 3.398 | 18 | 18 | fits | 120,753 | 64 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 1,630,696 | 16.307 | 18 | 18 | fits | 31,979 | 15 | 0.735 |
| an event behind 15 others | `backlog.event.if0` | 149,683 | 1.497 | 20 | 200 | fits | 116,529 | 125 | 0.545 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 688,646 | 6.886 | 20 | 20 | fits | 74,367 | 39 | 0.698 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 136,198 | 1.362 | 20 | 200 | fits | 136,406 | 143 | 0.543 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 537,634 | 5.376 | 20 | 200 | fits | 127,141 | 57 | 0.690 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 131,939 | 1.319 | 20 | 20 | fits | 136,406 | 143 | 0.543 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 753,707 | 7.537 | 20 | 20 | fits | 74,367 | 39 | 0.698 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 135,524 | 1.355 | 20 | 24 | fits | 136,406 | 143 | 0.543 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,197,837 | 11.978 | 20 | 24 | fits | 48,850 | 31 | 0.688 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 134,484 | 1.345 | 20 | 50 | fits | 136,406 | 143 | 0.543 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 536,139 | 5.361 | 20 | 50 | fits | 127,141 | 57 | 0.690 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 536,074 | 5.361 | 18 | 18 | fits | 127,141 | 57 | 0.690 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,357,155 | 13.572 | 18 | 18 | fits | 31,169 | 15 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 494,540 | 4.945 | 20 | 20 | fits | 126,237 | 57 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 106,501 | 1.065 | 20 | 200 | fits | 111,183 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 611,207 | 6.112 | 20 | 200 | fits | 126,237 | 57 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 107,413 | 1.074 | 20 | 20 | fits | 111,183 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 805,823 | 8.058 | 20 | 20 | fits | 78,157 | 27 | 0.772 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 110,998 | 1.110 | 20 | 24 | fits | 111,183 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,397,806 | 13.978 | 20 | 24 | fits | 56,633 | 32 | 0.752 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 109,958 | 1.100 | 20 | 50 | fits | 111,183 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 488,646 | 4.886 | 20 | 50 | fits | 95,697 | 64 | 0.693 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 290,488 | 2.905 | 18 | 18 | fits | 180,985 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,515,466 | 15.155 | 18 | 18 | fits | 32,018 | 15 | 0.735 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 9,188 | 0.092 | 20 | 20 | fits | 42,475 | 21 | 0.759 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 106,501 | 1.065 | 20 | 200 | fits | 111,183 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 42,934 | 0.429 | 20 | 200 | fits | 42,475 | 21 | 0.759 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 107,413 | 1.074 | 20 | 20 | fits | 111,183 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 788,445 | 7.884 | 20 | 20 | fits | 88,805 | 39 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 110,998 | 1.110 | 20 | 24 | fits | 111,183 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,335,898 | 13.359 | 20 | 24 | fits | 60,175 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 109,958 | 1.100 | 20 | 50 | fits | 111,183 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 488,646 | 4.886 | 20 | 50 | fits | 95,697 | 64 | 0.693 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 290,488 | 2.905 | 18 | 18 | fits | 180,985 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,460,676 | 14.607 | 18 | 18 | fits | 42,925 | 18 | 0.678 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,366,256 | 63.663 | 20 | 20 | MISS ceiling | 49,493 | 27 | 0.602 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,049,379 | 360.494 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,049,304 | 360.493 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,049,229 | 360.492 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,049,154 | 360.492 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 117,427 | 1.174 | 20 | 200 | fits | 109,618 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 633,444 | 6.334 | 20 | 200 | fits | 105,562 | 43 | 0.711 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 113,168 | 1.132 | 20 | 20 | fits | 109,618 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 790,354 | 7.904 | 20 | 20 | fits | 66,288 | 25 | 0.732 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 116,753 | 1.168 | 20 | 24 | fits | 109,618 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,495,779 | 64.958 | 20 | 24 | MISS ceiling | 30,120 | 23 | 0.566 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 115,713 | 1.157 | 20 | 50 | fits | 109,618 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 526,387 | 5.264 | 20 | 50 | fits | 130,233 | 91 | 0.624 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 244,893 | 2.449 | 18 | 18 | fits | 129,635 | 102 | 0.706 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,268,034 | 12.680 | 18 | 18 | fits | 43,569 | 21 | 0.656 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
