### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 21 paths and 6 of 587 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.400 (3.745) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.062 (4.786) | fits | 7 adp | 49 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.054 (0.208) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.885 (1.436) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.133 (62.301) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.211 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 4.037 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.595 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 5.654 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.591 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.940 | fits | 30 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 1.420 | fits | 0 acmp | 52 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.acmp.last.if0` (backlog-adp@program-aged2-7) | 6.018 | fits | 11 acmp | 52 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 1.411 | fits | 0 adp | 52 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 4.778 | fits | 7 adp | 52 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 1.456 | fits | 0 aecp | 52 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.999 | MISS ceiling | 15 aecp | 52 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 1.445 | fits | 0 maap | 52 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.156 | fits | 6 maap | 52 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.775 | fits | 0 srp | 52 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-0.service.srp.last.if0` (backlog-adp@blank-aged2-0) | 11.202 | fits | 31 srp | 52 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.851 | 19 | 103,226 (1.032) | yes | - |
| backlog-adp@blank-1 | 0 | 11.100 | 18 | 103,172 (1.032) | yes | - |
| backlog-adp@blank-2 | 0 | 11.173 | 19 | 103,188 (1.032) | yes | - |
| backlog-adp@blank-3 | 0 | 11.092 | 18 | 103,172 (1.032) | yes | - |
| backlog-adp@blank-4 | 0 | 11.087 | 18 | 103,188 (1.032) | yes | - |
| backlog-adp@blank-5 | 0 | 11.131 | 18 | 103,172 (1.032) | yes | - |
| backlog-adp@blank-6 | 0 | 11.222 | 19 | 103,188 (1.032) | yes | - |
| backlog-adp@blank-7 | 0 | 13.109 | 22 | 111,924 (1.119) | yes | - |
| backlog-adp@program-0 | 0 | 11.159 | 19 | 102,929 (1.029) | yes | - |
| backlog-adp@program-1 | 0 | 11.088 | 17 | 102,929 (1.029) | yes | - |
| backlog-adp@program-2 | 0 | 11.295 | 19 | 103,006 (1.030) | yes | - |
| backlog-adp@program-3 | 0 | 11.209 | 18 | 93,609 (0.936) | yes | - |
| backlog-adp@program-4 | 0 | 10.374 | 18 | 102,881 (1.029) | yes | - |
| backlog-adp@program-5 | 0 | 10.387 | 18 | 102,881 (1.029) | yes | - |
| backlog-adp@program-6 | 0 | 10.434 | 18 | 102,881 (1.029) | yes | - |
| backlog-adp@program-7 | 0 | 10.359 | 17 | 93,593 (0.936) | yes | - |
| backlog-adp@verify-0 | 0 | 11.850 | 19 | 102,735 (1.027) | yes | - |
| backlog-adp@verify-1 | 0 | 11.114 | 18 | 102,791 (1.028) | yes | - |
| backlog-adp@verify-2 | 0 | 11.117 | 18 | 102,900 (1.029) | yes | - |
| backlog-adp@verify-3 | 0 | 11.033 | 17 | 102,775 (1.028) | yes | - |
| backlog-adp@verify-4 | 0 | 11.039 | 18 | 102,791 (1.028) | yes | - |
| backlog-adp@verify-5 | 0 | 11.171 | 19 | 102,775 (1.028) | yes | - |
| backlog-adp@verify-6 | 0 | 11.183 | 19 | 102,791 (1.028) | yes | - |
| backlog-adp@verify-7 | 0 | 12.224 | 20 | 82,531 (0.825) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.559 | 19 | 102,485 (1.025) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.195 | 19 | 102,469 (1.025) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.118 | 18 | 102,469 (1.025) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.105 | 18 | 102,469 (1.025) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.172 | 19 | 102,469 (1.025) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.130 | 18 | 102,469 (1.025) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.201 | 19 | 102,469 (1.025) | yes | - |
| backlog-adp@blank-aged2-7 | 1 | 11.972 | 18 | 83,348 (0.833) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.209 | 19 | 102,815 (1.028) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.120 | 18 | 102,815 (1.028) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.113 | 18 | 102,815 (1.028) | yes | - |
| backlog-adp@program-aged2-3 | 1 | 11.103 | 17 | 103,778 (1.038) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.177 | 18 | 103,778 (1.038) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.287 | 19 | 102,711 (1.027) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.293 | 19 | 102,815 (1.028) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 11.267 | 18 | 83,216 (0.832) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.157 | 19 | 102,793 (1.028) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.067 | 18 | 102,793 (1.028) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.060 | 18 | 102,793 (1.028) | yes | - |
| backlog-adp@verify-aged2-3 | 1 | 11.052 | 17 | 103,756 (1.038) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.126 | 18 | 103,756 (1.038) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.234 | 19 | 102,793 (1.028) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.241 | 19 | 102,793 (1.028) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.068 | 18 | 83,533 (0.835) | yes | - |
| backlog | 0 | 6.927 | 19 | 80,474 (0.805) | yes | - |
| backlog-adp | 0 | 10.272 | 18 | 102,812 (1.028) | yes | - |
| backlog-adp-refill | 0 | 40.593 | 25 | 102,812 (1.028) | yes | - |
| backlog-owed | 0 | 360.262 | 66 | 101,464 (1.015) | yes | - |

Composed maximum over the 4 backlog windows: 102,812 CPU cycles (1.028 ms), backlog-adp.
Over the windows that released their whole load only: 102,812 (1.028 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 78972 | 0 | 47,373 (0.474) | fits |
| backlog-adp@blank-0 | 337 | 0 | 103,226 (1.032) | fits |
| backlog-adp@blank-1 | 336 | 0 | 103,172 (1.032) | fits |
| backlog-adp@blank-2 | 337 | 0 | 103,188 (1.032) | fits |
| backlog-adp@blank-3 | 336 | 0 | 103,172 (1.032) | fits |
| backlog-adp@blank-4 | 336 | 0 | 103,188 (1.032) | fits |
| backlog-adp@blank-5 | 336 | 0 | 103,172 (1.032) | fits |
| backlog-adp@blank-6 | 337 | 0 | 103,188 (1.032) | fits |
| backlog-adp@blank-7 | 340 | 0 | 111,924 (1.119) | fits |
| backlog-adp@program-0 | 368 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-1 | 367 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-2 | 369 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-3 | 367 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-4 | 368 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-5 | 368 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-6 | 368 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-7 | 368 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-0 | 395 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-1 | 394 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-2 | 395 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-3 | 394 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-4 | 394 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-5 | 395 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-6 | 395 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-7 | 396 | 0 | 112,416 (1.124) | fits |
| backlog-adp@blank-aged2-0 | 856 | 0 | 102,485 (1.025) | fits |
| backlog-adp@blank-aged2-1 | 865 | 0 | 102,469 (1.025) | fits |
| backlog-adp@blank-aged2-2 | 877 | 0 | 102,469 (1.025) | fits |
| backlog-adp@blank-aged2-3 | 890 | 0 | 102,469 (1.025) | fits |
| backlog-adp@blank-aged2-4 | 904 | 0 | 102,469 (1.025) | fits |
| backlog-adp@blank-aged2-5 | 916 | 0 | 102,469 (1.025) | fits |
| backlog-adp@blank-aged2-6 | 930 | 0 | 102,469 (1.025) | fits |
| backlog-adp@blank-aged2-7 | 943 | 0 | 83,348 (0.833) | fits |
| backlog-adp@program-aged2-0 | 882 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-aged2-1 | 894 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-aged2-2 | 907 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-aged2-3 | 920 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-aged2-4 | 934 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-aged2-5 | 948 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-aged2-6 | 961 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-aged2-7 | 973 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-aged2-0 | 904 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-aged2-1 | 916 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-aged2-2 | 929 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-aged2-3 | 942 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-aged2-4 | 956 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-aged2-5 | 970 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-aged2-6 | 983 | 0 | 112,416 (1.124) | fits |
| backlog-adp@verify-aged2-7 | 995 | 0 | 112,416 (1.124) | fits |
| save-held | 3433 | 0 | 112,162 (1.122) | fits |
| save-starved | 41993 | 0 | 85,852 (0.859) | fits |
| save | 610 | 0 | 111,816 (1.118) | fits |
| backlog | 298 | 0 | 80,474 (0.805) | fits |
| backlog-adp | 306 | 0 | 102,812 (1.028) | fits |
| backlog-adp-refill | 313 | 0 | 102,812 (1.028) | fits |
| backlog-owed | 356 | 0 | 101,464 (1.015) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +9.939 ms, 77,870 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 11.202 (18) | 6.798 |
| backlog-adp@blank-aged2-1 | 2 | +8.658 ms, 77,870 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.840 (18) | 7.160 |
| backlog-adp@blank-aged2-2 | 2 | +7.505 ms, 77,870 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.759 (18) | 7.241 |
| backlog-adp@blank-aged2-3 | 2 | +6.124 ms, 77,870 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.747 (18) | 7.253 |
| backlog-adp@blank-aged2-4 | 2 | +4.985 ms, 77,870 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.817 (18) | 7.183 |
| backlog-adp@blank-aged2-5 | 2 | +3.988 ms, 77,626 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.771 (18) | 7.229 |
| backlog-adp@blank-aged2-6 | 2 | +2.966 ms, 77,816 (0.778 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.842 (18) | 7.158 |
| backlog-adp@blank-aged2-7 | 2 | +2.109 ms, 77,816 (0.778 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.861 (18) | 7.139 |
| backlog-adp@program-aged2-0 | 2 | +9.846 ms, 82,991 (0.830 ms), issue | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.855 (18) | 7.145 |
| backlog-adp@program-aged2-1 | 2 | +8.746 ms, 83,413 (0.834 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.762 (18) | 7.238 |
| backlog-adp@program-aged2-2 | 2 | +7.455 ms, 83,413 (0.834 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.755 (18) | 7.245 |
| backlog-adp@program-aged2-3 | 2 | +6.081 ms, 83,413 (0.834 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.745 (18) | 7.255 |
| backlog-adp@program-aged2-4 | 2 | +4.955 ms, 83,413 (0.834 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.822 (18) | 7.178 |
| backlog-adp@program-aged2-5 | 2 | +4.076 ms, 83,095 (0.831 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.929 (18) | 7.071 |
| backlog-adp@program-aged2-6 | 2 | +3.024 ms, 83,261 (0.833 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.935 (18) | 7.065 |
| backlog-adp@program-aged2-7 | 2 | +1.561 ms, 83,177 (0.832 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.856 (18) | 7.144 |
| backlog-adp@verify-aged2-0 | 2 | +9.843 ms, 78,049 (0.780 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.803 (18) | 7.197 |
| backlog-adp@verify-aged2-1 | 2 | +8.743 ms, 78,397 (0.784 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 10.709 (18) | 7.291 |
| backlog-adp@verify-aged2-2 | 2 | +7.452 ms, 78,397 (0.784 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.702 (18) | 7.298 |
| backlog-adp@verify-aged2-3 | 2 | +6.079 ms, 78,397 (0.784 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.694 (18) | 7.306 |
| backlog-adp@verify-aged2-4 | 2 | +4.951 ms, 78,397 (0.784 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.771 (18) | 7.229 |
| backlog-adp@verify-aged2-5 | 2 | +3.896 ms, 78,153 (0.782 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.876 (18) | 7.124 |
| backlog-adp@verify-aged2-6 | 2 | +3.021 ms, 78,284 (0.783 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.883 (18) | 7.117 |
| backlog-adp@verify-aged2-7 | 2 | +1.560 ms, 78,284 (0.783 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.961 (18) | 7.039 |

Least margin over the aged windows: 6.798 ms, `backlog-adp@blank-aged2-0.service.srp.last.if0` at 11.202 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6029.787 | 6,070 | 102 | 2 | 30.927 | yes | within |
| save-held | 2018.280 | 4,070 | 102 | - | 13.935 | no | within |
| save-starved | 4048.183 | 4,070 | 102 | - | 30.959 | yes | within |
| save | 2018.490 | 4,070 | 102 | - | 10.843 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 520 | 96,409 (0.964) | 95,307 (0.953) |
| backlog-adp@blank-0 | 299 | 87,941 (0.879) | 76,346 (0.763) |
| backlog-adp@blank-1 | 299 | 87,892 (0.879) | 76,276 (0.763) |
| backlog-adp@blank-2 | 299 | 87,941 (0.879) | 76,346 (0.763) |
| backlog-adp@blank-3 | 299 | 87,892 (0.879) | 76,276 (0.763) |
| backlog-adp@blank-4 | 299 | 87,892 (0.879) | 76,276 (0.763) |
| backlog-adp@blank-5 | 299 | 87,975 (0.880) | 76,269 (0.763) |
| backlog-adp@blank-6 | 299 | 87,868 (0.879) | 76,252 (0.763) |
| backlog-adp@blank-7 | 300 | 111,924 (1.119) | 76,252 (0.763) |
| backlog-adp@program-0 | 328 | 112,416 (1.124) | 82,065 (0.821) |
| backlog-adp@program-1 | 328 | 112,416 (1.124) | 81,973 (0.820) |
| backlog-adp@program-2 | 328 | 112,416 (1.124) | 81,973 (0.820) |
| backlog-adp@program-3 | 328 | 112,416 (1.124) | 82,065 (0.821) |
| backlog-adp@program-4 | 329 | 112,416 (1.124) | 80,935 (0.809) |
| backlog-adp@program-5 | 329 | 112,416 (1.124) | 80,935 (0.809) |
| backlog-adp@program-6 | 329 | 112,416 (1.124) | 80,935 (0.809) |
| backlog-adp@program-7 | 329 | 112,416 (1.124) | 80,935 (0.809) |
| backlog-adp@verify-0 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-1 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-2 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-3 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-4 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-5 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-6 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-7 | 356 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@blank-aged2-0 | 297 | 77,870 (0.779) | 76,531 (0.765) |
| backlog-adp@blank-aged2-1 | 297 | 77,870 (0.779) | 76,531 (0.765) |
| backlog-adp@blank-aged2-2 | 297 | 77,870 (0.779) | 76,531 (0.765) |
| backlog-adp@blank-aged2-3 | 297 | 77,870 (0.779) | 76,531 (0.765) |
| backlog-adp@blank-aged2-4 | 297 | 77,870 (0.779) | 76,531 (0.765) |
| backlog-adp@blank-aged2-5 | 297 | 77,626 (0.776) | 76,531 (0.765) |
| backlog-adp@blank-aged2-6 | 297 | 77,816 (0.778) | 76,477 (0.765) |
| backlog-adp@blank-aged2-7 | 298 | 87,642 (0.876) | 76,477 (0.765) |
| backlog-adp@program-aged2-0 | 326 | 112,416 (1.124) | 81,788 (0.818) |
| backlog-adp@program-aged2-1 | 326 | 112,416 (1.124) | 82,000 (0.820) |
| backlog-adp@program-aged2-2 | 326 | 112,416 (1.124) | 82,000 (0.820) |
| backlog-adp@program-aged2-3 | 326 | 112,416 (1.124) | 82,000 (0.820) |
| backlog-adp@program-aged2-4 | 326 | 112,416 (1.124) | 82,000 (0.820) |
| backlog-adp@program-aged2-5 | 326 | 112,416 (1.124) | 82,000 (0.820) |
| backlog-adp@program-aged2-6 | 326 | 112,416 (1.124) | 81,848 (0.818) |
| backlog-adp@program-aged2-7 | 327 | 112,416 (1.124) | 81,848 (0.818) |
| backlog-adp@verify-aged2-0 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-aged2-1 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-aged2-2 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-aged2-3 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-aged2-4 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-aged2-5 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-aged2-6 | 355 | 112,416 (1.124) | 95,369 (0.954) |
| backlog-adp@verify-aged2-7 | 356 | 112,416 (1.124) | 95,369 (0.954) |
| save-held | 722 | 112,162 (1.122) | 95,496 (0.955) |
| save-starved | 418 | 97,160 (0.972) | 96,030 (0.960) |
| save | 585 | 111,816 (1.118) | 95,415 (0.954) |
| backlog | 265 | 47,373 (0.474) | 2,793 (0.028) |
| backlog-adp | 271 | 47,373 (0.474) | 2,793 (0.028) |
| backlog-adp-refill | 274 | 47,373 (0.474) | 2,793 (0.028) |
| backlog-owed | 306 | 47,373 (0.474) | 2,793 (0.028) |

Longest pass that carries a step: 112,416 CPU cycles (1.124 ms), backlog-adp@program-0; longest step: 96,030 (0.960 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 334,279 | 3.343 | 20 | 20 | fits | 85,712 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 140,787 | 1.408 | 20 | 200 | fits | 70,657 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 411,903 | 4.119 | 20 | 200 | fits | 85,712 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 141,699 | 1.417 | 20 | 20 | fits | 70,657 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 544,872 | 5.449 | 20 | 20 | fits | 55,306 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 145,284 | 1.453 | 20 | 24 | fits | 70,657 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,024,776 | 10.248 | 20 | 24 | fits | 41,229 | 30 | 0.742 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 144,244 | 1.442 | 20 | 50 | fits | 70,657 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 415,579 | 4.156 | 20 | 50 | fits | 85,712 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 247,015 | 2.470 | 18 | 18 | fits | 103,226 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,073,545 | 10.735 | 18 | 18 | fits | 21,117 | 14 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 266,528 | 2.665 | 20 | 20 | fits | 85,632 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 73,118 | 0.731 | 20 | 200 | fits | 70,326 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 344,072 | 3.441 | 20 | 200 | fits | 85,632 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 74,030 | 0.740 | 20 | 20 | fits | 70,326 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 477,041 | 4.770 | 20 | 20 | fits | 55,306 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 77,615 | 0.776 | 20 | 24 | fits | 70,326 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 978,945 | 9.789 | 20 | 24 | fits | 45,441 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 76,575 | 0.766 | 20 | 50 | fits | 70,326 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 347,748 | 3.477 | 20 | 50 | fits | 85,632 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 179,292 | 1.793 | 18 | 18 | fits | 103,172 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 998,578 | 9.986 | 18 | 18 | fits | 22,168 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 266,402 | 2.664 | 20 | 20 | fits | 85,632 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 72,918 | 0.729 | 20 | 200 | fits | 70,326 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 343,946 | 3.439 | 20 | 200 | fits | 85,632 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 73,830 | 0.738 | 20 | 20 | fits | 70,326 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 476,915 | 4.769 | 20 | 20 | fits | 55,306 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 77,415 | 0.774 | 20 | 24 | fits | 70,326 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 957,094 | 9.571 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 76,375 | 0.764 | 20 | 50 | fits | 70,326 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 347,622 | 3.476 | 20 | 50 | fits | 85,632 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 179,108 | 1.791 | 18 | 18 | fits | 103,188 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,005,758 | 10.058 | 18 | 18 | fits | 21,038 | 14 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 266,037 | 2.660 | 20 | 20 | fits | 85,632 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 72,627 | 0.726 | 20 | 200 | fits | 70,326 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 343,581 | 3.436 | 20 | 200 | fits | 85,632 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 73,539 | 0.735 | 20 | 20 | fits | 70,326 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 476,550 | 4.766 | 20 | 20 | fits | 55,306 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 77,124 | 0.771 | 20 | 24 | fits | 70,326 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 970,219 | 9.702 | 20 | 24 | fits | 45,441 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 76,084 | 0.761 | 20 | 50 | fits | 70,326 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 347,257 | 3.473 | 20 | 50 | fits | 85,632 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 178,801 | 1.788 | 18 | 18 | fits | 103,172 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 997,824 | 9.978 | 18 | 18 | fits | 30,140 | 19 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 265,820 | 2.658 | 20 | 20 | fits | 85,632 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 72,336 | 0.723 | 20 | 200 | fits | 70,326 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 343,364 | 3.434 | 20 | 200 | fits | 85,632 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 73,248 | 0.732 | 20 | 20 | fits | 70,326 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 476,333 | 4.763 | 20 | 20 | fits | 55,306 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 76,833 | 0.768 | 20 | 24 | fits | 70,326 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 977,708 | 9.777 | 20 | 24 | fits | 45,439 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 75,793 | 0.758 | 20 | 50 | fits | 70,326 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 347,040 | 3.470 | 20 | 50 | fits | 85,632 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 178,526 | 1.785 | 18 | 18 | fits | 103,188 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 997,341 | 9.973 | 18 | 18 | fits | 22,168 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 265,455 | 2.655 | 20 | 20 | fits | 85,632 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 72,045 | 0.720 | 20 | 200 | fits | 70,326 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 342,999 | 3.430 | 20 | 200 | fits | 85,632 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 72,957 | 0.730 | 20 | 20 | fits | 70,326 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 522,830 | 5.228 | 20 | 20 | fits | 59,067 | 35 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 76,542 | 0.765 | 20 | 24 | fits | 70,326 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 981,730 | 9.817 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 75,502 | 0.755 | 20 | 50 | fits | 70,326 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 346,675 | 3.467 | 20 | 50 | fits | 85,632 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 178,219 | 1.782 | 18 | 18 | fits | 103,172 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,001,384 | 10.014 | 18 | 18 | fits | 22,189 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 305,030 | 3.050 | 20 | 20 | fits | 78,634 | 55 | 0.693 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 71,754 | 0.718 | 20 | 200 | fits | 70,326 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 376,820 | 3.768 | 20 | 200 | fits | 78,634 | 55 | 0.693 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 72,666 | 0.727 | 20 | 20 | fits | 70,326 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 500,793 | 5.008 | 20 | 20 | fits | 46,898 | 26 | 0.789 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 76,251 | 0.763 | 20 | 24 | fits | 70,326 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 961,917 | 9.619 | 20 | 24 | fits | 45,610 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 75,211 | 0.752 | 20 | 50 | fits | 70,326 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 301,862 | 3.019 | 20 | 50 | fits | 62,598 | 62 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 177,944 | 1.779 | 18 | 18 | fits | 103,188 | 138 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,010,699 | 10.107 | 18 | 18 | fits | 21,030 | 14 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 302,324 | 3.023 | 20 | 20 | fits | 78,675 | 55 | 0.694 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 71,463 | 0.715 | 20 | 200 | fits | 70,326 | 135 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 373,971 | 3.740 | 20 | 200 | fits | 78,675 | 55 | 0.694 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 72,375 | 0.724 | 20 | 20 | fits | 70,326 | 135 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 497,771 | 4.978 | 20 | 20 | fits | 46,830 | 26 | 0.788 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 75,960 | 0.760 | 20 | 24 | fits | 70,326 | 135 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 956,462 | 9.565 | 20 | 24 | fits | 45,344 | 29 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 74,920 | 0.749 | 20 | 50 | fits | 70,326 | 135 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 298,972 | 2.990 | 20 | 50 | fits | 82,643 | 96 | 0.603 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 216,264 | 2.163 | 18 | 18 | fits | 74,831 | 62 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,004,991 | 10.050 | 18 | 18 | fits | 21,021 | 14 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 259,460 | 2.595 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 66,235 | 0.662 | 20 | 200 | fits | 70,808 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 337,148 | 3.371 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 67,147 | 0.671 | 20 | 20 | fits | 70,808 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 470,206 | 4.702 | 20 | 20 | fits | 55,395 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 70,732 | 0.707 | 20 | 24 | fits | 70,808 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 949,541 | 9.495 | 20 | 24 | fits | 41,170 | 30 | 0.742 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 69,692 | 0.697 | 20 | 50 | fits | 70,808 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 340,824 | 3.408 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 172,166 | 1.722 | 18 | 18 | fits | 102,929 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 998,310 | 9.983 | 18 | 18 | fits | 21,117 | 14 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 258,878 | 2.589 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 65,653 | 0.657 | 20 | 200 | fits | 70,808 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 336,566 | 3.366 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 66,565 | 0.666 | 20 | 20 | fits | 70,808 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 469,624 | 4.696 | 20 | 20 | fits | 55,395 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 70,150 | 0.702 | 20 | 24 | fits | 70,808 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 971,554 | 9.716 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 69,110 | 0.691 | 20 | 50 | fits | 70,808 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 340,242 | 3.402 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 171,584 | 1.716 | 18 | 18 | fits | 102,929 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 991,208 | 9.912 | 18 | 18 | fits | 22,189 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 290,523 | 2.905 | 20 | 20 | fits | 79,877 | 58 | 0.678 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 101,973 | 1.020 | 20 | 200 | fits | 70,448 | 137 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 362,312 | 3.623 | 20 | 200 | fits | 79,877 | 58 | 0.678 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 102,885 | 1.029 | 20 | 20 | fits | 70,448 | 137 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 519,518 | 5.195 | 20 | 20 | fits | 59,463 | 35 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 36,022 | 0.360 | 20 | 24 | fits | 37,262 | 63 | 0.577 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 934,182 | 9.342 | 20 | 24 | fits | 45,597 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 34,982 | 0.350 | 20 | 50 | fits | 37,262 | 63 | 0.577 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 286,111 | 2.861 | 20 | 50 | fits | 78,065 | 74 | 0.639 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 207,981 | 2.080 | 18 | 18 | fits | 103,006 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,011,899 | 10.119 | 18 | 18 | fits | 20,908 | 14 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 320,754 | 3.208 | 20 | 20 | fits | 78,771 | 55 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 73,991 | 0.740 | 20 | 200 | fits | 70,808 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 392,490 | 3.925 | 20 | 200 | fits | 78,771 | 55 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 74,903 | 0.749 | 20 | 20 | fits | 70,808 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 516,461 | 5.165 | 20 | 20 | fits | 46,911 | 26 | 0.789 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 78,488 | 0.785 | 20 | 24 | fits | 70,808 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 975,589 | 9.756 | 20 | 24 | fits | 45,441 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 77,448 | 0.774 | 20 | 50 | fits | 70,808 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 317,395 | 3.174 | 20 | 50 | fits | 82,012 | 96 | 0.597 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 170,602 | 1.706 | 18 | 18 | fits | 93,609 | 134 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,003,194 | 10.032 | 18 | 18 | fits | 30,140 | 19 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 264,079 | 2.641 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 70,960 | 0.710 | 20 | 200 | fits | 70,953 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 341,767 | 3.418 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 71,872 | 0.719 | 20 | 20 | fits | 70,953 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 474,825 | 4.748 | 20 | 20 | fits | 55,395 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 75,457 | 0.755 | 20 | 24 | fits | 70,953 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 976,601 | 9.766 | 20 | 24 | fits | 45,535 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 74,417 | 0.744 | 20 | 50 | fits | 70,953 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 345,443 | 3.454 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 176,843 | 1.768 | 18 | 18 | fits | 102,881 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 996,334 | 9.963 | 18 | 18 | fits | 22,268 | 16 | 0.817 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 265,476 | 2.655 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 72,357 | 0.724 | 20 | 200 | fits | 70,953 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 343,164 | 3.432 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 73,269 | 0.733 | 20 | 20 | fits | 70,953 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 476,222 | 4.762 | 20 | 20 | fits | 55,395 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 76,854 | 0.769 | 20 | 24 | fits | 70,953 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 969,992 | 9.700 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 75,814 | 0.758 | 20 | 50 | fits | 70,953 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 346,840 | 3.468 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 178,240 | 1.782 | 18 | 18 | fits | 102,881 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 997,618 | 9.976 | 18 | 18 | fits | 30,161 | 19 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 266,779 | 2.668 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 73,660 | 0.737 | 20 | 200 | fits | 70,953 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 344,467 | 3.445 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 74,572 | 0.746 | 20 | 20 | fits | 70,953 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 516,164 | 5.162 | 20 | 20 | fits | 59,419 | 35 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 78,157 | 0.782 | 20 | 24 | fits | 70,953 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 974,799 | 9.748 | 20 | 24 | fits | 45,441 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 77,117 | 0.771 | 20 | 50 | fits | 70,953 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 348,143 | 3.481 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 179,543 | 1.795 | 18 | 18 | fits | 102,881 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,002,404 | 10.024 | 18 | 18 | fits | 30,140 | 19 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 312,281 | 3.123 | 20 | 20 | fits | 78,771 | 55 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 65,476 | 0.655 | 20 | 200 | fits | 70,953 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 384,017 | 3.840 | 20 | 200 | fits | 78,771 | 55 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 66,388 | 0.664 | 20 | 20 | fits | 70,953 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 507,988 | 5.080 | 20 | 20 | fits | 46,911 | 26 | 0.789 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 69,973 | 0.700 | 20 | 24 | fits | 70,953 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 967,116 | 9.671 | 20 | 24 | fits | 45,441 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 68,933 | 0.689 | 20 | 50 | fits | 70,953 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 308,922 | 3.089 | 20 | 50 | fits | 82,012 | 96 | 0.597 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 162,071 | 1.621 | 18 | 18 | fits | 93,593 | 134 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 994,721 | 9.947 | 18 | 18 | fits | 30,140 | 19 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 334,092 | 3.341 | 20 | 20 | fits | 85,696 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 141,061 | 1.411 | 20 | 200 | fits | 71,103 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 411,700 | 4.117 | 20 | 200 | fits | 85,696 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 141,973 | 1.420 | 20 | 20 | fits | 71,103 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 544,758 | 5.448 | 20 | 20 | fits | 55,395 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 145,558 | 1.456 | 20 | 24 | fits | 71,103 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,024,093 | 10.241 | 20 | 24 | fits | 41,170 | 30 | 0.742 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 144,518 | 1.445 | 20 | 50 | fits | 71,103 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 415,376 | 4.154 | 20 | 50 | fits | 85,696 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 246,798 | 2.468 | 18 | 18 | fits | 102,735 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,072,862 | 10.729 | 18 | 18 | fits | 21,117 | 14 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 266,974 | 2.670 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 73,887 | 0.739 | 20 | 200 | fits | 70,814 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 344,662 | 3.447 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 74,799 | 0.748 | 20 | 20 | fits | 70,814 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 477,720 | 4.777 | 20 | 20 | fits | 55,395 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 78,384 | 0.784 | 20 | 24 | fits | 70,814 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 979,534 | 9.795 | 20 | 24 | fits | 45,549 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 77,344 | 0.773 | 20 | 50 | fits | 70,814 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 348,338 | 3.483 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 179,680 | 1.797 | 18 | 18 | fits | 102,791 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 999,188 | 9.992 | 18 | 18 | fits | 22,189 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 290,270 | 2.903 | 20 | 20 | fits | 79,877 | 58 | 0.678 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 101,826 | 1.018 | 20 | 200 | fits | 70,383 | 137 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 362,059 | 3.621 | 20 | 200 | fits | 79,877 | 58 | 0.678 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 102,738 | 1.027 | 20 | 20 | fits | 70,383 | 137 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 494,505 | 4.945 | 20 | 20 | fits | 55,367 | 33 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 35,940 | 0.359 | 20 | 24 | fits | 37,251 | 63 | 0.577 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 950,937 | 9.509 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 34,900 | 0.349 | 20 | 50 | fits | 37,251 | 63 | 0.577 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 285,858 | 2.859 | 20 | 50 | fits | 78,065 | 74 | 0.639 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 207,728 | 2.077 | 18 | 18 | fits | 102,900 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 999,601 | 9.996 | 18 | 18 | fits | 21,038 | 14 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 258,716 | 2.587 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 65,703 | 0.657 | 20 | 200 | fits | 70,814 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 336,404 | 3.364 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 66,615 | 0.666 | 20 | 20 | fits | 70,814 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 469,462 | 4.695 | 20 | 20 | fits | 55,395 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 70,200 | 0.702 | 20 | 24 | fits | 70,814 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 971,491 | 9.715 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 69,160 | 0.692 | 20 | 50 | fits | 70,814 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 340,080 | 3.401 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 171,480 | 1.715 | 18 | 18 | fits | 102,775 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 991,145 | 9.911 | 18 | 18 | fits | 22,189 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 259,487 | 2.595 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 66,400 | 0.664 | 20 | 200 | fits | 70,814 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 337,175 | 3.372 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 67,312 | 0.673 | 20 | 20 | fits | 70,814 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 470,233 | 4.702 | 20 | 20 | fits | 55,395 | 33 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 70,897 | 0.709 | 20 | 24 | fits | 70,814 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 972,099 | 9.721 | 20 | 24 | fits | 45,468 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 69,857 | 0.699 | 20 | 50 | fits | 70,814 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 340,851 | 3.409 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 172,193 | 1.722 | 18 | 18 | fits | 102,791 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 991,753 | 9.918 | 18 | 18 | fits | 22,189 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 260,110 | 2.601 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 67,097 | 0.671 | 20 | 200 | fits | 70,814 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 337,798 | 3.378 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 68,009 | 0.680 | 20 | 20 | fits | 70,814 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 495,582 | 4.956 | 20 | 20 | fits | 59,476 | 35 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 71,594 | 0.716 | 20 | 24 | fits | 70,814 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 955,899 | 9.559 | 20 | 24 | fits | 45,597 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 70,554 | 0.706 | 20 | 50 | fits | 70,814 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 341,474 | 3.415 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 172,874 | 1.729 | 18 | 18 | fits | 102,775 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,004,755 | 10.048 | 18 | 18 | fits | 21,117 | 14 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 300,741 | 3.007 | 20 | 20 | fits | 78,698 | 55 | 0.694 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 67,794 | 0.678 | 20 | 200 | fits | 70,814 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 372,595 | 3.726 | 20 | 200 | fits | 78,698 | 55 | 0.694 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 68,706 | 0.687 | 20 | 20 | fits | 70,814 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 496,601 | 4.966 | 20 | 20 | fits | 46,931 | 26 | 0.787 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 72,291 | 0.723 | 20 | 24 | fits | 70,814 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 957,289 | 9.573 | 20 | 24 | fits | 45,597 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 71,251 | 0.713 | 20 | 50 | fits | 70,814 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 297,573 | 2.976 | 20 | 50 | fits | 62,598 | 62 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 173,587 | 1.736 | 18 | 18 | fits | 102,791 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,006,145 | 10.061 | 18 | 18 | fits | 21,117 | 14 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 299,119 | 2.991 | 20 | 20 | fits | 78,819 | 55 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 68,491 | 0.685 | 20 | 200 | fits | 70,814 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 370,910 | 3.709 | 20 | 200 | fits | 78,819 | 55 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 69,403 | 0.694 | 20 | 20 | fits | 70,814 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 494,799 | 4.948 | 20 | 20 | fits | 46,919 | 26 | 0.788 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 72,988 | 0.730 | 20 | 24 | fits | 70,814 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 953,410 | 9.534 | 20 | 24 | fits | 45,352 | 29 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 71,948 | 0.719 | 20 | 50 | fits | 70,814 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 295,767 | 2.958 | 20 | 50 | fits | 82,531 | 96 | 0.601 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 213,171 | 2.132 | 18 | 18 | fits | 74,598 | 62 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,001,955 | 10.020 | 18 | 18 | fits | 21,029 | 14 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 300,918 | 3.009 | 20 | 20 | fits | 85,961 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 107,975 | 1.080 | 20 | 200 | fits | 71,395 | 132 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 378,642 | 3.786 | 20 | 200 | fits | 85,961 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 108,887 | 1.089 | 20 | 20 | fits | 71,395 | 132 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 511,904 | 5.119 | 20 | 20 | fits | 55,538 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 112,472 | 1.125 | 20 | 24 | fits | 71,395 | 132 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 992,748 | 9.927 | 20 | 24 | fits | 41,391 | 30 | 0.743 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 111,432 | 1.114 | 20 | 50 | fits | 71,395 | 132 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 382,318 | 3.823 | 20 | 50 | fits | 85,961 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 213,462 | 2.135 | 18 | 18 | fits | 102,485 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,120,190 | 11.202 | 18 | 18 | fits | 21,192 | 14 | 0.806 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 264,070 | 2.641 | 20 | 20 | fits | 85,881 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 71,171 | 0.712 | 20 | 200 | fits | 69,684 | 132 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 341,714 | 3.417 | 20 | 200 | fits | 85,881 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 72,083 | 0.721 | 20 | 20 | fits | 69,684 | 132 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 475,002 | 4.750 | 20 | 20 | fits | 55,564 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 75,668 | 0.757 | 20 | 24 | fits | 69,684 | 132 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 1,035,050 | 10.351 | 20 | 24 | fits | 45,875 | 29 | 0.722 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 74,628 | 0.746 | 20 | 50 | fits | 69,684 | 132 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 345,390 | 3.454 | 20 | 50 | fits | 85,881 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 176,642 | 1.766 | 18 | 18 | fits | 102,469 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,083,969 | 10.840 | 18 | 18 | fits | 21,149 | 14 | 0.805 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 263,023 | 2.630 | 20 | 20 | fits | 85,881 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 70,124 | 0.701 | 20 | 200 | fits | 69,734 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 340,667 | 3.407 | 20 | 200 | fits | 85,881 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 71,036 | 0.710 | 20 | 20 | fits | 69,734 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 473,955 | 4.740 | 20 | 20 | fits | 55,564 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 74,621 | 0.746 | 20 | 24 | fits | 69,734 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 1,056,174 | 10.562 | 20 | 24 | fits | 45,614 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 73,581 | 0.736 | 20 | 50 | fits | 69,734 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 344,343 | 3.443 | 20 | 50 | fits | 85,881 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 175,595 | 1.756 | 18 | 18 | fits | 102,469 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,075,939 | 10.759 | 18 | 18 | fits | 22,300 | 16 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 261,785 | 2.618 | 20 | 20 | fits | 85,881 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 68,886 | 0.689 | 20 | 200 | fits | 69,684 | 132 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 339,429 | 3.394 | 20 | 200 | fits | 85,881 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 69,798 | 0.698 | 20 | 20 | fits | 69,684 | 132 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 472,717 | 4.727 | 20 | 20 | fits | 55,564 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 73,383 | 0.734 | 20 | 24 | fits | 69,684 | 132 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 1,054,953 | 10.550 | 20 | 24 | fits | 45,614 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 72,343 | 0.723 | 20 | 50 | fits | 69,684 | 132 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 343,105 | 3.431 | 20 | 50 | fits | 85,881 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 174,357 | 1.744 | 18 | 18 | fits | 102,469 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,074,718 | 10.747 | 18 | 18 | fits | 22,300 | 16 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 260,647 | 2.606 | 20 | 20 | fits | 85,881 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 67,748 | 0.677 | 20 | 200 | fits | 69,734 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 338,291 | 3.383 | 20 | 200 | fits | 85,881 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 68,660 | 0.687 | 20 | 20 | fits | 69,734 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 450,140 | 4.501 | 20 | 20 | fits | 34,125 | 24 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 72,245 | 0.722 | 20 | 24 | fits | 69,734 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 1,032,732 | 10.327 | 20 | 24 | fits | 45,612 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 71,205 | 0.712 | 20 | 50 | fits | 69,734 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 341,967 | 3.420 | 20 | 50 | fits | 85,881 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 173,219 | 1.732 | 18 | 18 | fits | 102,469 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,081,651 | 10.817 | 18 | 18 | fits | 21,149 | 14 | 0.805 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 259,409 | 2.594 | 20 | 20 | fits | 77,512 | 77 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 66,510 | 0.665 | 20 | 200 | fits | 69,684 | 132 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 328,684 | 3.287 | 20 | 200 | fits | 77,512 | 77 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 67,422 | 0.674 | 20 | 20 | fits | 69,684 | 132 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 587,725 | 5.877 | 20 | 20 | fits | 59,543 | 35 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 71,007 | 0.710 | 20 | 24 | fits | 69,684 | 132 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 1,049,221 | 10.492 | 20 | 24 | fits | 45,741 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 69,967 | 0.700 | 20 | 50 | fits | 69,684 | 132 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 332,360 | 3.324 | 20 | 50 | fits | 77,512 | 77 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 171,981 | 1.720 | 18 | 18 | fits | 102,469 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,077,104 | 10.771 | 18 | 18 | fits | 30,418 | 19 | 0.777 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 375,588 | 3.756 | 20 | 20 | fits | 79,072 | 55 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 65,372 | 0.654 | 20 | 200 | fits | 69,734 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 448,205 | 4.482 | 20 | 200 | fits | 79,072 | 55 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 66,284 | 0.663 | 20 | 20 | fits | 69,734 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 572,718 | 5.727 | 20 | 20 | fits | 47,257 | 26 | 0.789 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 69,869 | 0.699 | 20 | 24 | fits | 69,734 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 1,035,194 | 10.352 | 20 | 24 | fits | 45,770 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 68,829 | 0.688 | 20 | 50 | fits | 69,734 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 294,993 | 2.950 | 20 | 50 | fits | 62,732 | 62 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 170,843 | 1.708 | 18 | 18 | fits | 102,469 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,084,247 | 10.842 | 18 | 18 | fits | 21,149 | 14 | 0.805 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 373,846 | 3.738 | 20 | 20 | fits | 78,752 | 55 | 0.694 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 63,558 | 0.636 | 20 | 200 | fits | 69,684 | 132 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 445,546 | 4.455 | 20 | 200 | fits | 78,752 | 55 | 0.694 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 64,470 | 0.645 | 20 | 20 | fits | 69,684 | 132 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 569,902 | 5.699 | 20 | 20 | fits | 47,128 | 26 | 0.789 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 68,055 | 0.681 | 20 | 24 | fits | 69,684 | 132 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 1,032,378 | 10.324 | 20 | 24 | fits | 45,770 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 67,015 | 0.670 | 20 | 50 | fits | 69,684 | 132 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 370,470 | 3.705 | 20 | 50 | fits | 83,348 | 96 | 0.603 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 209,241 | 2.092 | 18 | 18 | fits | 74,569 | 62 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,086,074 | 10.861 | 18 | 18 | fits | 25,792 | 18 | 0.828 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 261,180 | 2.612 | 20 | 20 | fits | 85,858 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 67,975 | 0.680 | 20 | 200 | fits | 70,048 | 132 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 338,868 | 3.389 | 20 | 200 | fits | 85,858 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 68,887 | 0.689 | 20 | 20 | fits | 70,048 | 132 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 472,034 | 4.720 | 20 | 20 | fits | 55,503 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 72,472 | 0.725 | 20 | 24 | fits | 70,048 | 132 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 955,640 | 9.556 | 20 | 24 | fits | 24,422 | 20 | 0.657 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 71,432 | 0.714 | 20 | 50 | fits | 70,048 | 132 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 342,544 | 3.425 | 20 | 50 | fits | 85,858 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 173,792 | 1.738 | 18 | 18 | fits | 102,815 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,085,532 | 10.855 | 18 | 18 | fits | 21,630 | 14 | 0.808 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 260,046 | 2.600 | 20 | 20 | fits | 85,858 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 66,841 | 0.668 | 20 | 200 | fits | 69,998 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 337,734 | 3.377 | 20 | 200 | fits | 85,858 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 67,753 | 0.678 | 20 | 20 | fits | 69,998 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 470,900 | 4.709 | 20 | 20 | fits | 55,503 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 71,338 | 0.713 | 20 | 24 | fits | 69,998 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 1,048,572 | 10.486 | 20 | 24 | fits | 45,472 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 70,298 | 0.703 | 20 | 50 | fits | 69,998 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 341,410 | 3.414 | 20 | 50 | fits | 85,858 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 172,658 | 1.727 | 18 | 18 | fits | 102,815 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,076,198 | 10.762 | 18 | 18 | fits | 30,161 | 19 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 259,012 | 2.590 | 20 | 20 | fits | 85,858 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 65,807 | 0.658 | 20 | 200 | fits | 70,048 | 132 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 336,700 | 3.367 | 20 | 200 | fits | 85,858 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 66,719 | 0.667 | 20 | 20 | fits | 70,048 | 132 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 469,866 | 4.699 | 20 | 20 | fits | 55,503 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 70,304 | 0.703 | 20 | 24 | fits | 70,048 | 132 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 1,055,855 | 10.559 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 69,264 | 0.693 | 20 | 50 | fits | 70,048 | 132 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 340,376 | 3.404 | 20 | 50 | fits | 85,858 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 171,624 | 1.716 | 18 | 18 | fits | 102,815 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,075,509 | 10.755 | 18 | 18 | fits | 22,189 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 258,032 | 2.580 | 20 | 20 | fits | 85,858 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 63,864 | 0.639 | 20 | 200 | fits | 69,998 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 335,720 | 3.357 | 20 | 200 | fits | 85,858 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 64,776 | 0.648 | 20 | 20 | fits | 69,998 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 468,886 | 4.689 | 20 | 20 | fits | 55,503 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 68,361 | 0.684 | 20 | 24 | fits | 69,998 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 1,054,892 | 10.549 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 67,321 | 0.673 | 20 | 50 | fits | 69,998 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 339,396 | 3.394 | 20 | 50 | fits | 85,858 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 170,644 | 1.706 | 18 | 18 | fits | 103,778 | 143 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,074,546 | 10.745 | 18 | 18 | fits | 22,189 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 257,807 | 2.578 | 20 | 20 | fits | 85,858 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 63,639 | 0.636 | 20 | 200 | fits | 70,048 | 132 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 335,495 | 3.355 | 20 | 200 | fits | 85,858 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 64,551 | 0.646 | 20 | 20 | fits | 70,048 | 132 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 447,315 | 4.473 | 20 | 20 | fits | 34,157 | 24 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 68,136 | 0.681 | 20 | 24 | fits | 70,048 | 132 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 1,033,542 | 10.335 | 20 | 24 | fits | 45,468 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 67,096 | 0.671 | 20 | 50 | fits | 70,048 | 132 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 339,171 | 3.392 | 20 | 50 | fits | 85,858 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 170,419 | 1.704 | 18 | 18 | fits | 103,778 | 143 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,082,206 | 10.822 | 18 | 18 | fits | 21,038 | 14 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 289,259 | 2.893 | 20 | 20 | fits | 57,975 | 49 | 0.627 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 100,834 | 1.008 | 20 | 200 | fits | 69,511 | 134 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 339,064 | 3.391 | 20 | 200 | fits | 57,975 | 49 | 0.627 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 101,746 | 1.017 | 20 | 20 | fits | 69,511 | 134 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 601,668 | 6.017 | 20 | 20 | fits | 59,357 | 35 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 35,820 | 0.358 | 20 | 24 | fits | 38,816 | 69 | 0.570 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 1,015,339 | 10.153 | 20 | 24 | fits | 45,508 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 34,780 | 0.348 | 20 | 50 | fits | 38,816 | 69 | 0.570 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 284,765 | 2.848 | 20 | 50 | fits | 78,153 | 74 | 0.640 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 206,547 | 2.065 | 18 | 18 | fits | 102,711 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,092,879 | 10.929 | 18 | 18 | fits | 20,908 | 14 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 386,856 | 3.869 | 20 | 20 | fits | 78,876 | 55 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 70,953 | 0.710 | 20 | 200 | fits | 69,998 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 459,277 | 4.593 | 20 | 200 | fits | 78,876 | 55 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 71,865 | 0.719 | 20 | 20 | fits | 69,998 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 583,670 | 5.837 | 20 | 20 | fits | 47,198 | 26 | 0.790 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 75,450 | 0.754 | 20 | 24 | fits | 69,998 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 1,044,706 | 10.447 | 20 | 24 | fits | 45,626 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 74,410 | 0.744 | 20 | 50 | fits | 69,998 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 300,816 | 3.008 | 20 | 50 | fits | 62,570 | 62 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 176,770 | 1.768 | 18 | 18 | fits | 102,815 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,093,504 | 10.935 | 18 | 18 | fits | 21,038 | 14 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 406,199 | 4.062 | 20 | 20 | fits | 78,742 | 55 | 0.694 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 69,919 | 0.699 | 20 | 200 | fits | 70,048 | 132 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 477,831 | 4.778 | 20 | 200 | fits | 78,742 | 55 | 0.694 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 70,831 | 0.708 | 20 | 20 | fits | 70,048 | 132 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 601,845 | 6.018 | 20 | 20 | fits | 47,019 | 26 | 0.789 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 74,416 | 0.744 | 20 | 24 | fits | 70,048 | 132 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 1,061,321 | 10.613 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 73,376 | 0.734 | 20 | 50 | fits | 70,048 | 132 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 402,765 | 4.028 | 20 | 50 | fits | 81,846 | 96 | 0.597 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 154,461 | 1.545 | 18 | 18 | fits | 81,540 | 103 | 0.687 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,085,637 | 10.856 | 18 | 18 | fits | 26,851 | 20 | 0.835 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 260,859 | 2.609 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 67,904 | 0.679 | 20 | 200 | fits | 70,101 | 132 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 338,547 | 3.385 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 68,816 | 0.688 | 20 | 20 | fits | 70,101 | 132 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 471,713 | 4.717 | 20 | 20 | fits | 55,503 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 72,401 | 0.724 | 20 | 24 | fits | 70,101 | 132 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 955,319 | 9.553 | 20 | 24 | fits | 24,422 | 20 | 0.657 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 71,361 | 0.714 | 20 | 50 | fits | 70,101 | 132 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 342,223 | 3.422 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 173,699 | 1.737 | 18 | 18 | fits | 102,793 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,080,317 | 10.803 | 18 | 18 | fits | 21,678 | 14 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 259,725 | 2.597 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 66,770 | 0.668 | 20 | 200 | fits | 70,051 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 337,413 | 3.374 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 67,682 | 0.677 | 20 | 20 | fits | 70,051 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 470,579 | 4.706 | 20 | 20 | fits | 55,503 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 71,267 | 0.713 | 20 | 24 | fits | 70,051 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 1,043,283 | 10.433 | 20 | 24 | fits | 45,478 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 70,227 | 0.702 | 20 | 50 | fits | 70,051 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 341,089 | 3.411 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 172,565 | 1.726 | 18 | 18 | fits | 102,793 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,070,909 | 10.709 | 18 | 18 | fits | 30,161 | 19 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 258,691 | 2.587 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 65,736 | 0.657 | 20 | 200 | fits | 70,101 | 132 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 336,379 | 3.364 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 66,648 | 0.666 | 20 | 20 | fits | 70,101 | 132 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 469,545 | 4.695 | 20 | 20 | fits | 55,503 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 70,233 | 0.702 | 20 | 24 | fits | 70,101 | 132 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 1,050,566 | 10.506 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 69,193 | 0.692 | 20 | 50 | fits | 70,101 | 132 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 340,055 | 3.401 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 171,531 | 1.715 | 18 | 18 | fits | 102,793 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,070,220 | 10.702 | 18 | 18 | fits | 22,189 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 257,835 | 2.578 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 63,917 | 0.639 | 20 | 200 | fits | 70,051 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 335,523 | 3.355 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 64,829 | 0.648 | 20 | 20 | fits | 70,051 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 468,689 | 4.687 | 20 | 20 | fits | 55,503 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 68,414 | 0.684 | 20 | 24 | fits | 70,051 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 1,049,727 | 10.497 | 20 | 24 | fits | 45,470 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 67,374 | 0.674 | 20 | 50 | fits | 70,051 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 339,199 | 3.392 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 170,675 | 1.707 | 18 | 18 | fits | 103,756 | 143 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,069,381 | 10.694 | 18 | 18 | fits | 22,189 | 16 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 257,486 | 2.575 | 20 | 20 | fits | 85,776 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 63,568 | 0.636 | 20 | 200 | fits | 70,101 | 132 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 335,174 | 3.352 | 20 | 200 | fits | 85,776 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 64,480 | 0.645 | 20 | 20 | fits | 70,101 | 132 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 446,994 | 4.470 | 20 | 20 | fits | 34,157 | 24 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 68,065 | 0.681 | 20 | 24 | fits | 70,101 | 132 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 1,028,447 | 10.284 | 20 | 24 | fits | 45,468 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 67,025 | 0.670 | 20 | 50 | fits | 70,101 | 132 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 338,850 | 3.389 | 20 | 50 | fits | 85,776 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 170,326 | 1.703 | 18 | 18 | fits | 103,756 | 143 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,077,111 | 10.771 | 18 | 18 | fits | 21,038 | 14 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 264,880 | 2.649 | 20 | 20 | fits | 64,176 | 72 | 0.603 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 71,925 | 0.719 | 20 | 200 | fits | 70,101 | 132 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 320,968 | 3.210 | 20 | 200 | fits | 64,176 | 72 | 0.603 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 72,837 | 0.728 | 20 | 20 | fits | 70,101 | 132 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 578,730 | 5.787 | 20 | 20 | fits | 59,510 | 35 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 76,422 | 0.764 | 20 | 24 | fits | 70,101 | 132 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 1,038,786 | 10.388 | 20 | 24 | fits | 45,597 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 75,382 | 0.754 | 20 | 50 | fits | 70,101 | 132 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 324,644 | 3.246 | 20 | 50 | fits | 64,176 | 72 | 0.603 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 177,720 | 1.777 | 18 | 18 | fits | 102,793 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,087,642 | 10.876 | 18 | 18 | fits | 21,117 | 14 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 381,504 | 3.815 | 20 | 20 | fits | 79,047 | 55 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 70,882 | 0.709 | 20 | 200 | fits | 70,051 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 454,184 | 4.542 | 20 | 200 | fits | 79,047 | 55 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 71,794 | 0.718 | 20 | 20 | fits | 70,051 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 578,501 | 5.785 | 20 | 20 | fits | 47,039 | 26 | 0.788 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 75,379 | 0.754 | 20 | 24 | fits | 70,051 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 1,039,537 | 10.395 | 20 | 24 | fits | 45,626 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 74,339 | 0.743 | 20 | 50 | fits | 70,051 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 300,529 | 3.005 | 20 | 50 | fits | 62,522 | 62 | 0.694 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 176,677 | 1.767 | 18 | 18 | fits | 102,793 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,088,335 | 10.883 | 18 | 18 | fits | 21,038 | 14 | 0.802 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 401,472 | 4.015 | 20 | 20 | fits | 78,815 | 55 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 69,848 | 0.698 | 20 | 200 | fits | 70,101 | 132 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 473,177 | 4.732 | 20 | 200 | fits | 78,815 | 55 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 70,760 | 0.708 | 20 | 20 | fits | 70,101 | 132 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 597,291 | 5.973 | 20 | 20 | fits | 47,069 | 26 | 0.789 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 74,345 | 0.743 | 20 | 24 | fits | 70,101 | 132 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 1,058,327 | 10.583 | 20 | 24 | fits | 45,626 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 73,305 | 0.733 | 20 | 50 | fits | 70,101 | 132 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 398,038 | 3.980 | 20 | 50 | fits | 81,788 | 96 | 0.595 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 154,368 | 1.544 | 18 | 18 | fits | 81,518 | 103 | 0.687 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,096,138 | 10.961 | 18 | 18 | fits | 26,547 | 18 | 0.844 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 228,178 | 2.282 | 20 | 200 | fits | 63,582 | 84 | 0.557 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 363,886 | 3.639 | 20 | 20 | fits | 49,872 | 32 | 0.687 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 502,940 | 5.029 | 20 | 24 | fits | 22,654 | 21 | 0.566 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 254,754 | 2.548 | 20 | 50 | fits | 47,675 | 52 | 0.642 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 705,346 | 7.053 | 18 | 18 | fits | 45,465 | 29 | 0.716 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 259,529 | 2.595 | 20 | 200 | fits | 65,954 | 90 | 0.575 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 403,671 | 4.037 | 20 | 20 | fits | 52,055 | 38 | 0.692 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 565,371 | 5.654 | 20 | 24 | fits | 25,353 | 27 | 0.620 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 259,085 | 2.591 | 20 | 50 | fits | 59,168 | 61 | 0.666 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 793,953 | 7.940 | 18 | 18 | fits | 40,588 | 32 | 0.746 |
| an event behind 15 others | `backlog.event.if0` | 88,503 | 0.885 | 20 | 200 | fits | 65,917 | 104 | 0.526 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 339,984 | 3.400 | 20 | 20 | fits | 47,150 | 44 | 0.545 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 77,519 | 0.775 | 20 | 200 | fits | 77,727 | 138 | 0.525 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 279,104 | 2.791 | 20 | 200 | fits | 55,803 | 55 | 0.566 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 73,260 | 0.733 | 20 | 20 | fits | 77,727 | 138 | 0.525 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 369,196 | 3.692 | 20 | 20 | fits | 47,150 | 44 | 0.545 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 76,845 | 0.768 | 20 | 24 | fits | 77,727 | 138 | 0.525 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 625,995 | 6.260 | 20 | 24 | fits | 25,284 | 29 | 0.506 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 75,805 | 0.758 | 20 | 50 | fits | 77,727 | 138 | 0.525 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 277,609 | 2.776 | 20 | 50 | fits | 55,803 | 55 | 0.566 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 277,544 | 2.775 | 18 | 18 | fits | 55,803 | 55 | 0.566 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 656,961 | 6.570 | 18 | 18 | fits | 10,760 | 17 | 0.339 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 257,517 | 2.575 | 20 | 20 | fits | 85,511 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 64,521 | 0.645 | 20 | 200 | fits | 69,203 | 135 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 334,940 | 3.349 | 20 | 200 | fits | 85,511 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 65,433 | 0.654 | 20 | 20 | fits | 69,203 | 135 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 467,987 | 4.680 | 20 | 20 | fits | 55,389 | 33 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 69,018 | 0.690 | 20 | 24 | fits | 69,203 | 135 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 961,646 | 9.616 | 20 | 24 | fits | 45,465 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 67,978 | 0.680 | 20 | 50 | fits | 69,203 | 135 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 338,616 | 3.386 | 20 | 50 | fits | 85,511 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 170,335 | 1.703 | 18 | 18 | fits | 102,812 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 989,267 | 9.893 | 18 | 18 | fits | 30,156 | 19 | 0.772 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 5,400 | 0.054 | 20 | 20 | fits | 20,824 | 20 | 0.767 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 64,521 | 0.645 | 20 | 200 | fits | 69,203 | 135 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 19,670 | 0.197 | 20 | 200 | fits | 20,824 | 20 | 0.767 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 65,433 | 0.654 | 20 | 20 | fits | 69,203 | 135 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 463,795 | 4.638 | 20 | 20 | fits | 68,319 | 44 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 69,018 | 0.690 | 20 | 24 | fits | 69,203 | 135 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 919,714 | 9.197 | 20 | 24 | fits | 45,465 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 67,978 | 0.680 | 20 | 50 | fits | 69,203 | 135 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 329,240 | 3.292 | 20 | 50 | fits | 76,135 | 71 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 170,335 | 1.703 | 18 | 18 | fits | 102,812 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 968,368 | 9.684 | 18 | 18 | fits | 21,033 | 14 | 0.802 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,213,323 | 62.133 | 20 | 20 | MISS ceiling | 28,947 | 25 | 0.562 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,021,120 | 360.211 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,021,045 | 360.210 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,020,970 | 360.210 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,020,895 | 360.209 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 70,721 | 0.707 | 20 | 200 | fits | 67,839 | 129 | 0.503 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 328,370 | 3.284 | 20 | 200 | fits | 75,887 | 67 | 0.661 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 66,462 | 0.665 | 20 | 20 | fits | 67,839 | 129 | 0.503 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 442,141 | 4.421 | 20 | 20 | fits | 57,280 | 33 | 0.768 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 70,047 | 0.700 | 20 | 24 | fits | 67,839 | 129 | 0.503 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,299,872 | 62.999 | 20 | 24 | MISS ceiling | 22,646 | 21 | 0.566 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 69,007 | 0.690 | 20 | 50 | fits | 67,839 | 129 | 0.503 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 326,875 | 3.269 | 20 | 50 | fits | 75,887 | 67 | 0.661 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 170,016 | 1.700 | 18 | 18 | fits | 101,464 | 131 | 0.639 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 786,906 | 7.869 | 18 | 18 | fits | 21,478 | 17 | 0.779 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
