### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 21 paths and 6 of 587 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.381 (3.718) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-7.adp_available.if0` (backlog-adp@verify-aged2-7) | 4.139 (4.899) | fits | 7 adp | 49 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.086 (0.334) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.880 (1.424) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.065 (62.329) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.224 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.821 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.371 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 5.641 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.676 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.995 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 1.436 | fits | 0 acmp | 52 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.acmp.last.if0` (backlog-adp@verify-aged2-7) | 6.191 | fits | 11 acmp | 52 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 1.427 | fits | 0 adp | 52 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.adp.last.if0` (backlog-adp@verify-aged2-7) | 4.873 | fits | 7 adp | 52 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 1.472 | fits | 0 aecp | 52 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.907 | MISS ceiling | 15 aecp | 52 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 1.462 | fits | 0 maap | 52 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 4.209 | fits | 6 maap | 52 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.760 | fits | 0 srp | 52 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.srp.last.if0` (backlog-adp@blank-aged2-7) | 11.224 | fits | 31 srp | 52 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.975 | 19 | 103,999 (1.040) | yes | - |
| backlog-adp@blank-1 | 0 | 11.395 | 20 | 104,258 (1.043) | yes | - |
| backlog-adp@blank-2 | 0 | 11.331 | 20 | 104,258 (1.043) | yes | - |
| backlog-adp@blank-3 | 0 | 11.371 | 20 | 104,187 (1.042) | yes | - |
| backlog-adp@blank-4 | 0 | 11.257 | 19 | 104,187 (1.042) | yes | - |
| backlog-adp@blank-5 | 0 | 11.333 | 19 | 105,633 (1.056) | yes | - |
| backlog-adp@blank-6 | 0 | 11.482 | 20 | 103,976 (1.040) | yes | - |
| backlog-adp@blank-7 | 0 | 13.305 | 22 | 112,249 (1.122) | yes | - |
| backlog-adp@program-0 | 0 | 11.436 | 20 | 104,197 (1.042) | yes | - |
| backlog-adp@program-1 | 0 | 11.444 | 20 | 94,850 (0.949) | yes | - |
| backlog-adp@program-2 | 0 | 11.611 | 20 | 103,893 (1.039) | yes | - |
| backlog-adp@program-3 | 0 | 11.377 | 19 | 94,491 (0.945) | yes | - |
| backlog-adp@program-4 | 0 | 10.675 | 20 | 104,324 (1.043) | yes | - |
| backlog-adp@program-5 | 0 | 10.629 | 18 | 103,982 (1.040) | yes | - |
| backlog-adp@program-6 | 0 | 10.800 | 21 | 103,931 (1.039) | yes | - |
| backlog-adp@program-7 | 0 | 10.736 | 20 | 94,438 (0.944) | yes | - |
| backlog-adp@verify-0 | 0 | 12.187 | 21 | 104,277 (1.043) | yes | - |
| backlog-adp@verify-1 | 0 | 11.405 | 21 | 104,310 (1.043) | yes | - |
| backlog-adp@verify-2 | 0 | 11.320 | 19 | 104,381 (1.044) | yes | - |
| backlog-adp@verify-3 | 0 | 11.323 | 19 | 104,381 (1.044) | yes | - |
| backlog-adp@verify-4 | 0 | 11.308 | 19 | 104,310 (1.043) | yes | - |
| backlog-adp@verify-5 | 0 | 11.386 | 19 | 105,756 (1.058) | yes | - |
| backlog-adp@verify-6 | 0 | 11.597 | 21 | 103,980 (1.040) | yes | - |
| backlog-adp@verify-7 | 0 | 12.393 | 21 | 84,644 (0.846) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.921 | 21 | 104,421 (1.044) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.467 | 20 | 104,487 (1.045) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.502 | 20 | 104,487 (1.045) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.545 | 20 | 103,778 (1.038) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.424 | 20 | 103,778 (1.038) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.427 | 20 | 103,778 (1.038) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.495 | 21 | 103,778 (1.038) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.349 | 21 | 86,016 (0.860) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.355 | 19 | 104,384 (1.044) | yes | - |
| backlog-adp@program-aged2-1 | 1 | 11.475 | 19 | 105,378 (1.054) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.626 | 22 | 104,416 (1.044) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.464 | 20 | 103,734 (1.037) | yes | - |
| backlog-adp@program-aged2-4 | 1 | 11.413 | 19 | 104,696 (1.047) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 11.443 | 19 | 104,696 (1.047) | yes | - |
| backlog-adp@program-aged2-6 | 1 | 11.495 | 20 | 104,696 (1.047) | yes | - |
| backlog-adp@program-aged2-7 | 1 | 11.782 | 21 | 89,359 (0.894) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.359 | 20 | 104,424 (1.044) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.381 | 20 | 104,424 (1.044) | yes | - |
| backlog-adp@verify-aged2-2 | 1 | 11.313 | 19 | 105,045 (1.050) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.285 | 19 | 103,954 (1.040) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.348 | 20 | 103,954 (1.040) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.379 | 20 | 103,954 (1.040) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.659 | 22 | 103,954 (1.040) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.494 | 22 | 95,008 (0.950) | yes | - |
| backlog | 0 | 6.787 | 19 | 80,173 (0.802) | yes | - |
| backlog-adp | 0 | 10.572 | 20 | 104,123 (1.041) | yes | - |
| backlog-adp-refill | 0 | 40.538 | 36 | 104,123 (1.041) | yes | - |
| backlog-owed | 0 | 360.275 | 66 | 101,386 (1.014) | yes | - |

Composed maximum over the 4 backlog windows: 104,123 CPU cycles (1.041 ms), backlog-adp.
Over the windows that released their whole load only: 104,123 (1.041 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 81075 | 0 | 47,053 (0.471) | fits |
| backlog-adp@blank-0 | 424 | 0 | 103,999 (1.040) | fits |
| backlog-adp@blank-1 | 425 | 0 | 104,258 (1.043) | fits |
| backlog-adp@blank-2 | 425 | 0 | 104,258 (1.043) | fits |
| backlog-adp@blank-3 | 425 | 0 | 104,187 (1.042) | fits |
| backlog-adp@blank-4 | 424 | 0 | 104,187 (1.042) | fits |
| backlog-adp@blank-5 | 424 | 0 | 105,633 (1.056) | fits |
| backlog-adp@blank-6 | 427 | 0 | 103,976 (1.040) | fits |
| backlog-adp@blank-7 | 430 | 0 | 112,249 (1.122) | fits |
| backlog-adp@program-0 | 529 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-1 | 528 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-2 | 530 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-3 | 529 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-4 | 531 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-5 | 532 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-6 | 535 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-7 | 533 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-0 | 624 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-1 | 624 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-2 | 622 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-3 | 623 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-4 | 622 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-5 | 622 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-6 | 626 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-7 | 626 | 0 | 113,084 (1.131) | fits |
| backlog-adp@blank-aged2-0 | 931 | 0 | 104,421 (1.044) | fits |
| backlog-adp@blank-aged2-1 | 939 | 0 | 104,487 (1.045) | fits |
| backlog-adp@blank-aged2-2 | 952 | 0 | 104,487 (1.045) | fits |
| backlog-adp@blank-aged2-3 | 965 | 0 | 103,778 (1.038) | fits |
| backlog-adp@blank-aged2-4 | 978 | 0 | 103,778 (1.038) | fits |
| backlog-adp@blank-aged2-5 | 991 | 0 | 103,778 (1.038) | fits |
| backlog-adp@blank-aged2-6 | 1005 | 0 | 103,778 (1.038) | fits |
| backlog-adp@blank-aged2-7 | 1018 | 0 | 86,016 (0.860) | fits |
| backlog-adp@program-aged2-0 | 1028 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-aged2-1 | 1041 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-aged2-2 | 1056 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-aged2-3 | 1067 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-aged2-4 | 1080 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-aged2-5 | 1093 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-aged2-6 | 1107 | 0 | 113,084 (1.131) | fits |
| backlog-adp@program-aged2-7 | 1121 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-aged2-0 | 1122 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-aged2-1 | 1135 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-aged2-2 | 1148 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-aged2-3 | 1160 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-aged2-4 | 1174 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-aged2-5 | 1187 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-aged2-6 | 1202 | 0 | 113,084 (1.131) | fits |
| backlog-adp@verify-aged2-7 | 1215 | 0 | 113,084 (1.131) | fits |
| save-held | 3439 | 0 | 111,370 (1.114) | fits |
| save-starved | 43204 | 0 | 79,519 (0.795) | fits |
| save | 610 | 0 | 110,613 (1.106) | fits |
| backlog | 298 | 0 | 80,173 (0.802) | fits |
| backlog-adp | 324 | 0 | 104,123 (1.041) | fits |
| backlog-adp-refill | 340 | 0 | 104,123 (1.041) | fits |
| backlog-owed | 356 | 0 | 101,386 (1.014) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +9.852 ms, 77,654 (0.777 ms), read-back | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.893 (18) | 7.107 |
| backlog-adp@blank-aged2-1 | 2 | +8.706 ms, 77,860 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.932 (18) | 7.068 |
| backlog-adp@blank-aged2-2 | 2 | +7.317 ms, 77,860 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.966 (18) | 7.034 |
| backlog-adp@blank-aged2-3 | 2 | +6.209 ms, 77,860 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 11.010 (18) | 6.990 |
| backlog-adp@blank-aged2-4 | 2 | +5.126 ms, 77,860 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.057 (18) | 6.943 |
| backlog-adp@blank-aged2-5 | 2 | +3.850 ms, 77,942 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.061 (18) | 6.939 |
| backlog-adp@blank-aged2-6 | 2 | +3.047 ms, 78,007 (0.780 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.128 (18) | 6.872 |
| backlog-adp@blank-aged2-7 | 2 | +1.576 ms, 78,007 (0.780 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 11.224 (18) | 6.776 |
| backlog-adp@program-aged2-0 | 2 | +9.684 ms, 83,306 (0.833 ms), issue | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.989 (18) | 7.011 |
| backlog-adp@program-aged2-1 | 2 | +8.663 ms, 83,543 (0.835 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.941 (18) | 7.059 |
| backlog-adp@program-aged2-2 | 2 | +7.503 ms, 83,469 (0.835 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.091 (18) | 6.909 |
| backlog-adp@program-aged2-3 | 2 | +6.231 ms, 83,543 (0.835 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.931 (18) | 7.069 |
| backlog-adp@program-aged2-4 | 2 | +5.060 ms, 83,543 (0.835 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.046 (18) | 6.954 |
| backlog-adp@program-aged2-5 | 2 | +3.948 ms, 83,625 (0.836 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.076 (18) | 6.924 |
| backlog-adp@program-aged2-6 | 2 | +2.990 ms, 83,625 (0.836 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.127 (18) | 6.873 |
| backlog-adp@program-aged2-7 | 2 | +2.128 ms, 89,359 (0.894 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.196 (18) | 6.804 |
| backlog-adp@verify-aged2-0 | 2 | +9.842 ms, 84,567 (0.846 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.991 (18) | 7.009 |
| backlog-adp@verify-aged2-1 | 2 | +8.700 ms, 84,432 (0.844 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.014 (18) | 6.986 |
| backlog-adp@verify-aged2-2 | 2 | +7.406 ms, 84,432 (0.844 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.948 (18) | 7.052 |
| backlog-adp@verify-aged2-3 | 2 | +6.182 ms, 84,432 (0.844 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.919 (18) | 7.081 |
| backlog-adp@verify-aged2-4 | 2 | +5.099 ms, 84,432 (0.844 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.982 (18) | 7.018 |
| backlog-adp@verify-aged2-5 | 2 | +3.824 ms, 84,601 (0.846 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.014 (18) | 6.986 |
| backlog-adp@verify-aged2-6 | 2 | +3.024 ms, 84,583 (0.846 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 11.015 (18) | 6.985 |
| backlog-adp@verify-aged2-7 | 2 | +1.552 ms, 84,564 (0.846 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.196 (18) | 6.804 |

Least margin over the aged windows: 6.776 ms, `backlog-adp@blank-aged2-7.service.srp.last.if0` at 11.224 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6029.852 | 6,070 | 102 | 2 | 30.895 | yes | within |
| save-held | 2018.185 | 4,070 | 102 | - | 13.966 | no | within |
| save-starved | 4048.088 | 4,070 | 102 | - | 30.893 | yes | within |
| save | 2018.403 | 4,070 | 102 | - | 10.946 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 520 | 96,561 (0.966) | 95,604 (0.956) |
| backlog-adp@blank-0 | 299 | 89,091 (0.891) | 76,188 (0.762) |
| backlog-adp@blank-1 | 299 | 88,269 (0.883) | 76,316 (0.763) |
| backlog-adp@blank-2 | 299 | 88,204 (0.882) | 76,251 (0.763) |
| backlog-adp@blank-3 | 299 | 88,288 (0.883) | 76,251 (0.763) |
| backlog-adp@blank-4 | 299 | 88,150 (0.881) | 76,251 (0.763) |
| backlog-adp@blank-5 | 299 | 88,088 (0.881) | 76,105 (0.761) |
| backlog-adp@blank-6 | 299 | 94,262 (0.943) | 76,292 (0.763) |
| backlog-adp@blank-7 | 300 | 112,249 (1.122) | 76,164 (0.762) |
| backlog-adp@program-0 | 328 | 113,084 (1.131) | 81,852 (0.819) |
| backlog-adp@program-1 | 328 | 113,084 (1.131) | 81,955 (0.820) |
| backlog-adp@program-2 | 328 | 113,084 (1.131) | 81,955 (0.820) |
| backlog-adp@program-3 | 328 | 113,084 (1.131) | 81,955 (0.820) |
| backlog-adp@program-4 | 329 | 113,084 (1.131) | 81,241 (0.812) |
| backlog-adp@program-5 | 329 | 113,084 (1.131) | 81,241 (0.812) |
| backlog-adp@program-6 | 329 | 113,084 (1.131) | 81,241 (0.812) |
| backlog-adp@program-7 | 329 | 113,084 (1.131) | 81,241 (0.812) |
| backlog-adp@verify-0 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-1 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-2 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-3 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-4 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-5 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-6 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-7 | 356 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@blank-aged2-0 | 297 | 77,654 (0.777) | 76,187 (0.762) |
| backlog-adp@blank-aged2-1 | 297 | 77,860 (0.779) | 76,382 (0.764) |
| backlog-adp@blank-aged2-2 | 297 | 77,860 (0.779) | 76,382 (0.764) |
| backlog-adp@blank-aged2-3 | 297 | 77,860 (0.779) | 76,382 (0.764) |
| backlog-adp@blank-aged2-4 | 297 | 77,860 (0.779) | 76,382 (0.764) |
| backlog-adp@blank-aged2-5 | 297 | 77,942 (0.779) | 76,464 (0.765) |
| backlog-adp@blank-aged2-6 | 297 | 78,007 (0.780) | 76,529 (0.765) |
| backlog-adp@blank-aged2-7 | 298 | 88,159 (0.882) | 76,529 (0.765) |
| backlog-adp@program-aged2-0 | 326 | 113,084 (1.131) | 81,754 (0.818) |
| backlog-adp@program-aged2-1 | 326 | 113,084 (1.131) | 81,991 (0.820) |
| backlog-adp@program-aged2-2 | 326 | 113,084 (1.131) | 81,991 (0.820) |
| backlog-adp@program-aged2-3 | 326 | 113,084 (1.131) | 81,991 (0.820) |
| backlog-adp@program-aged2-4 | 326 | 113,084 (1.131) | 81,991 (0.820) |
| backlog-adp@program-aged2-5 | 326 | 113,084 (1.131) | 82,073 (0.821) |
| backlog-adp@program-aged2-6 | 326 | 113,084 (1.131) | 82,073 (0.821) |
| backlog-adp@program-aged2-7 | 327 | 113,084 (1.131) | 82,073 (0.821) |
| backlog-adp@verify-aged2-0 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-aged2-1 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-aged2-2 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-aged2-3 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-aged2-4 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-aged2-5 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-aged2-6 | 355 | 113,084 (1.131) | 95,665 (0.957) |
| backlog-adp@verify-aged2-7 | 356 | 113,084 (1.131) | 95,665 (0.957) |
| save-held | 722 | 111,370 (1.114) | 95,713 (0.957) |
| save-starved | 418 | 97,035 (0.970) | 96,078 (0.961) |
| save | 585 | 110,613 (1.106) | 95,713 (0.957) |
| backlog | 265 | 47,053 (0.471) | 3,018 (0.030) |
| backlog-adp | 271 | 47,053 (0.471) | 3,018 (0.030) |
| backlog-adp-refill | 274 | 47,053 (0.471) | 3,018 (0.030) |
| backlog-owed | 306 | 47,053 (0.471) | 3,018 (0.030) |

Longest pass that carries a step: 113,084 CPU cycles (1.131 ms), backlog-adp@program-0; longest step: 96,078 (0.961 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 334,280 | 3.343 | 20 | 20 | fits | 86,713 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 138,846 | 1.388 | 20 | 200 | fits | 71,438 | 135 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 413,066 | 4.131 | 20 | 200 | fits | 86,713 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 139,758 | 1.398 | 20 | 20 | fits | 71,438 | 135 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 554,510 | 5.545 | 20 | 20 | fits | 69,967 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 143,343 | 1.433 | 20 | 24 | fits | 71,438 | 135 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,018,155 | 10.182 | 20 | 24 | fits | 42,728 | 31 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 142,303 | 1.423 | 20 | 50 | fits | 71,438 | 135 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 416,742 | 4.167 | 20 | 50 | fits | 86,713 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 245,847 | 2.458 | 18 | 18 | fits | 103,999 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,075,975 | 10.760 | 18 | 18 | fits | 29,488 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 268,883 | 2.689 | 20 | 20 | fits | 86,713 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 73,140 | 0.731 | 20 | 200 | fits | 70,641 | 135 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 347,669 | 3.477 | 20 | 200 | fits | 86,713 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 74,052 | 0.741 | 20 | 20 | fits | 70,641 | 135 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 489,113 | 4.891 | 20 | 20 | fits | 69,967 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 77,637 | 0.776 | 20 | 24 | fits | 70,641 | 135 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 937,770 | 9.378 | 20 | 24 | fits | 46,942 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 76,597 | 0.766 | 20 | 50 | fits | 70,641 | 135 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 351,345 | 3.513 | 20 | 50 | fits | 86,713 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 180,400 | 1.804 | 18 | 18 | fits | 104,258 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,027,016 | 10.270 | 18 | 18 | fits | 21,329 | 14 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 263,223 | 2.632 | 20 | 20 | fits | 86,713 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 67,480 | 0.675 | 20 | 200 | fits | 70,641 | 135 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 342,009 | 3.420 | 20 | 200 | fits | 86,713 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 68,392 | 0.684 | 20 | 20 | fits | 70,641 | 135 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 460,634 | 4.606 | 20 | 20 | fits | 47,148 | 36 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 71,977 | 0.720 | 20 | 24 | fits | 70,641 | 135 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 933,327 | 9.333 | 20 | 24 | fits | 47,040 | 29 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 70,937 | 0.709 | 20 | 50 | fits | 70,641 | 135 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 345,685 | 3.457 | 20 | 50 | fits | 86,713 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 174,740 | 1.747 | 18 | 18 | fits | 104,258 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,020,425 | 10.204 | 18 | 18 | fits | 29,267 | 17 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 267,437 | 2.674 | 20 | 20 | fits | 64,561 | 73 | 0.599 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 71,765 | 0.718 | 20 | 200 | fits | 70,641 | 135 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 324,071 | 3.241 | 20 | 200 | fits | 64,561 | 73 | 0.599 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 72,677 | 0.727 | 20 | 20 | fits | 70,641 | 135 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 467,366 | 4.674 | 20 | 20 | fits | 70,369 | 45 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 76,262 | 0.763 | 20 | 24 | fits | 70,641 | 135 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 945,293 | 9.453 | 20 | 24 | fits | 46,856 | 29 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 75,222 | 0.752 | 20 | 50 | fits | 70,641 | 135 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 327,747 | 3.277 | 20 | 50 | fits | 64,561 | 73 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 178,954 | 1.790 | 18 | 18 | fits | 104,187 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,024,325 | 10.243 | 18 | 18 | fits | 21,206 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 266,658 | 2.667 | 20 | 20 | fits | 87,152 | 82 | 0.647 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 66,105 | 0.661 | 20 | 200 | fits | 70,641 | 135 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 345,500 | 3.455 | 20 | 200 | fits | 87,152 | 82 | 0.647 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 67,017 | 0.670 | 20 | 20 | fits | 70,641 | 135 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 487,454 | 4.875 | 20 | 20 | fits | 70,202 | 45 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 70,602 | 0.706 | 20 | 24 | fits | 70,641 | 135 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 963,720 | 9.637 | 20 | 24 | fits | 46,627 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 69,562 | 0.696 | 20 | 50 | fits | 70,641 | 135 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 349,176 | 3.492 | 20 | 50 | fits | 87,152 | 82 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 173,294 | 1.733 | 18 | 18 | fits | 104,187 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,013,145 | 10.131 | 18 | 18 | fits | 21,164 | 14 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 268,027 | 2.680 | 20 | 20 | fits | 86,944 | 82 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 70,479 | 0.705 | 20 | 200 | fits | 70,730 | 136 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 346,799 | 3.468 | 20 | 200 | fits | 86,944 | 82 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 71,391 | 0.714 | 20 | 20 | fits | 70,730 | 136 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 547,387 | 5.474 | 20 | 20 | fits | 62,354 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 74,976 | 0.750 | 20 | 24 | fits | 70,730 | 136 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 971,428 | 9.714 | 20 | 24 | fits | 46,627 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 73,936 | 0.739 | 20 | 50 | fits | 70,730 | 136 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 350,475 | 3.505 | 20 | 50 | fits | 86,944 | 82 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 179,114 | 1.791 | 18 | 18 | fits | 105,633 | 144 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,020,873 | 10.209 | 18 | 18 | fits | 21,184 | 14 | 0.784 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 306,120 | 3.061 | 20 | 20 | fits | 79,979 | 55 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 70,636 | 0.706 | 20 | 200 | fits | 70,384 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 379,405 | 3.794 | 20 | 200 | fits | 79,979 | 55 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 71,548 | 0.715 | 20 | 20 | fits | 70,384 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 511,083 | 5.111 | 20 | 20 | fits | 61,161 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 75,133 | 0.751 | 20 | 24 | fits | 70,384 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 931,767 | 9.318 | 20 | 24 | fits | 46,993 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 74,093 | 0.741 | 20 | 50 | fits | 70,384 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 303,102 | 3.031 | 20 | 50 | fits | 63,597 | 62 | 0.694 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 177,614 | 1.776 | 18 | 18 | fits | 103,976 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,019,054 | 10.191 | 18 | 18 | fits | 29,367 | 18 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 298,930 | 2.989 | 20 | 20 | fits | 79,890 | 55 | 0.689 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 64,976 | 0.650 | 20 | 200 | fits | 70,384 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 372,181 | 3.722 | 20 | 200 | fits | 79,890 | 55 | 0.689 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 65,888 | 0.659 | 20 | 20 | fits | 70,384 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 503,873 | 5.039 | 20 | 20 | fits | 61,168 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 69,473 | 0.695 | 20 | 24 | fits | 70,384 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 934,436 | 9.344 | 20 | 24 | fits | 46,934 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 68,433 | 0.684 | 20 | 50 | fits | 70,384 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 295,967 | 2.960 | 20 | 50 | fits | 84,711 | 96 | 0.604 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 211,191 | 2.112 | 18 | 18 | fits | 75,700 | 62 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,013,662 | 10.137 | 18 | 18 | fits | 21,306 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 292,639 | 2.926 | 20 | 20 | fits | 81,204 | 58 | 0.675 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 101,531 | 1.015 | 20 | 200 | fits | 70,674 | 137 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 365,916 | 3.659 | 20 | 200 | fits | 81,204 | 58 | 0.675 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 102,443 | 1.024 | 20 | 20 | fits | 70,674 | 137 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 485,970 | 4.860 | 20 | 20 | fits | 72,036 | 51 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 35,354 | 0.354 | 20 | 24 | fits | 36,705 | 63 | 0.559 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 913,133 | 9.131 | 20 | 24 | fits | 38,502 | 25 | 0.737 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 34,314 | 0.343 | 20 | 50 | fits | 36,705 | 63 | 0.559 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 288,388 | 2.884 | 20 | 50 | fits | 79,593 | 74 | 0.636 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 208,730 | 2.087 | 18 | 18 | fits | 104,197 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,025,052 | 10.251 | 18 | 18 | fits | 29,267 | 17 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 264,265 | 2.643 | 20 | 20 | fits | 87,049 | 82 | 0.646 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 74,112 | 0.741 | 20 | 200 | fits | 71,390 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 343,113 | 3.431 | 20 | 200 | fits | 87,049 | 82 | 0.646 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 75,024 | 0.750 | 20 | 20 | fits | 71,390 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 485,006 | 4.850 | 20 | 20 | fits | 70,252 | 45 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 78,609 | 0.786 | 20 | 24 | fits | 71,390 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 938,805 | 9.388 | 20 | 24 | fits | 46,800 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 77,569 | 0.776 | 20 | 50 | fits | 71,390 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 346,789 | 3.468 | 20 | 50 | fits | 87,049 | 82 | 0.646 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 171,964 | 1.720 | 18 | 18 | fits | 94,850 | 135 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,025,903 | 10.259 | 18 | 18 | fits | 29,267 | 17 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 264,848 | 2.648 | 20 | 20 | fits | 86,782 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 69,401 | 0.694 | 20 | 200 | fits | 71,470 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 343,703 | 3.437 | 20 | 200 | fits | 86,782 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 70,313 | 0.703 | 20 | 20 | fits | 71,470 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 526,602 | 5.266 | 20 | 20 | fits | 61,479 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 73,898 | 0.739 | 20 | 24 | fits | 71,470 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 946,267 | 9.463 | 20 | 24 | fits | 46,945 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 72,858 | 0.729 | 20 | 50 | fits | 71,470 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 347,379 | 3.474 | 20 | 50 | fits | 86,782 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 176,296 | 1.763 | 18 | 18 | fits | 103,893 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,025,517 | 10.255 | 18 | 18 | fits | 21,314 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 318,626 | 3.186 | 20 | 20 | fits | 80,131 | 55 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 68,026 | 0.680 | 20 | 200 | fits | 71,470 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 392,118 | 3.921 | 20 | 200 | fits | 80,131 | 55 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 68,938 | 0.689 | 20 | 20 | fits | 71,470 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 527,246 | 5.272 | 20 | 20 | fits | 64,504 | 44 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 72,523 | 0.725 | 20 | 24 | fits | 71,470 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 961,441 | 9.614 | 20 | 24 | fits | 46,930 | 29 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 71,483 | 0.715 | 20 | 50 | fits | 71,470 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 315,663 | 3.157 | 20 | 50 | fits | 83,500 | 96 | 0.594 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 165,519 | 1.655 | 18 | 18 | fits | 94,491 | 134 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,018,927 | 10.189 | 18 | 18 | fits | 29,225 | 17 | 0.732 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 247,683 | 2.477 | 20 | 20 | fits | 88,519 | 88 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 71,920 | 0.719 | 20 | 200 | fits | 72,266 | 135 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 325,996 | 3.260 | 20 | 200 | fits | 88,519 | 88 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 72,832 | 0.728 | 20 | 20 | fits | 72,266 | 135 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 468,636 | 4.686 | 20 | 20 | fits | 70,469 | 45 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 76,417 | 0.764 | 20 | 24 | fits | 72,266 | 135 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 946,351 | 9.464 | 20 | 24 | fits | 42,740 | 30 | 0.752 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 75,377 | 0.754 | 20 | 50 | fits | 72,266 | 135 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 329,672 | 3.297 | 20 | 50 | fits | 88,519 | 88 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 179,246 | 1.792 | 18 | 18 | fits | 104,324 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,025,330 | 10.253 | 18 | 18 | fits | 21,206 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 261,684 | 2.617 | 20 | 20 | fits | 86,798 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 66,166 | 0.662 | 20 | 200 | fits | 70,889 | 135 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 340,597 | 3.406 | 20 | 200 | fits | 86,798 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 67,078 | 0.671 | 20 | 20 | fits | 70,889 | 135 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 482,211 | 4.822 | 20 | 20 | fits | 70,052 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 70,663 | 0.707 | 20 | 24 | fits | 70,889 | 135 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 946,275 | 9.463 | 20 | 24 | fits | 46,958 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 69,623 | 0.696 | 20 | 50 | fits | 70,889 | 135 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 344,273 | 3.443 | 20 | 50 | fits | 86,798 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 173,150 | 1.732 | 18 | 18 | fits | 103,982 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,004,084 | 10.041 | 18 | 18 | fits | 29,488 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 291,417 | 2.914 | 20 | 20 | fits | 81,253 | 58 | 0.675 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 100,568 | 1.006 | 20 | 200 | fits | 70,584 | 137 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 364,785 | 3.648 | 20 | 200 | fits | 81,253 | 58 | 0.675 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 101,480 | 1.015 | 20 | 20 | fits | 70,584 | 137 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 507,646 | 5.076 | 20 | 20 | fits | 38,409 | 29 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 34,481 | 0.345 | 20 | 24 | fits | 36,082 | 63 | 0.540 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 890,175 | 8.902 | 20 | 24 | fits | 46,945 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 33,441 | 0.334 | 20 | 50 | fits | 36,082 | 63 | 0.540 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 287,208 | 2.872 | 20 | 50 | fits | 79,642 | 74 | 0.636 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 207,501 | 2.075 | 18 | 18 | fits | 103,931 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,037,919 | 10.379 | 18 | 18 | fits | 21,206 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 304,105 | 3.041 | 20 | 20 | fits | 81,382 | 62 | 0.682 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 73,361 | 0.734 | 20 | 200 | fits | 70,889 | 135 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 376,552 | 3.766 | 20 | 200 | fits | 81,382 | 62 | 0.682 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 74,273 | 0.743 | 20 | 20 | fits | 70,889 | 135 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 509,427 | 5.094 | 20 | 20 | fits | 61,702 | 38 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 77,858 | 0.779 | 20 | 24 | fits | 70,889 | 135 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 944,537 | 9.445 | 20 | 24 | fits | 46,800 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 76,818 | 0.768 | 20 | 50 | fits | 70,889 | 135 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 298,846 | 2.988 | 20 | 50 | fits | 61,393 | 88 | 0.527 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 170,801 | 1.708 | 18 | 18 | fits | 94,438 | 134 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,031,635 | 10.316 | 18 | 18 | fits | 29,267 | 17 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 338,441 | 3.384 | 20 | 20 | fits | 86,749 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 142,693 | 1.427 | 20 | 200 | fits | 71,735 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 417,263 | 4.173 | 20 | 200 | fits | 86,749 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 143,605 | 1.436 | 20 | 20 | fits | 71,735 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 558,870 | 5.589 | 20 | 20 | fits | 70,094 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 147,190 | 1.472 | 20 | 24 | fits | 71,735 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 989,731 | 9.897 | 20 | 24 | fits | 24,781 | 21 | 0.655 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 146,150 | 1.462 | 20 | 50 | fits | 71,735 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 420,939 | 4.209 | 20 | 50 | fits | 86,749 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 249,972 | 2.500 | 18 | 18 | fits | 104,277 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,105,322 | 11.053 | 18 | 18 | fits | 23,296 | 14 | 0.835 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 263,094 | 2.631 | 20 | 20 | fits | 86,749 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 67,263 | 0.673 | 20 | 200 | fits | 71,159 | 135 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 341,916 | 3.419 | 20 | 200 | fits | 86,749 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 68,175 | 0.682 | 20 | 20 | fits | 71,159 | 135 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 483,523 | 4.835 | 20 | 20 | fits | 70,094 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 71,760 | 0.718 | 20 | 24 | fits | 71,159 | 135 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 908,770 | 9.088 | 20 | 24 | fits | 41,323 | 31 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 70,720 | 0.707 | 20 | 50 | fits | 71,159 | 135 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 345,592 | 3.456 | 20 | 50 | fits | 86,749 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 174,575 | 1.746 | 18 | 18 | fits | 104,310 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,027,294 | 10.273 | 18 | 18 | fits | 21,329 | 14 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 267,450 | 2.675 | 20 | 20 | fits | 86,749 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 71,548 | 0.715 | 20 | 200 | fits | 71,159 | 135 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 346,272 | 3.463 | 20 | 200 | fits | 86,749 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 72,460 | 0.725 | 20 | 20 | fits | 71,159 | 135 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 492,538 | 4.925 | 20 | 20 | fits | 74,753 | 51 | 0.697 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 76,045 | 0.760 | 20 | 24 | fits | 71,159 | 135 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 969,322 | 9.693 | 20 | 24 | fits | 46,691 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 75,005 | 0.750 | 20 | 50 | fits | 71,159 | 135 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 349,948 | 3.499 | 20 | 50 | fits | 86,749 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 178,931 | 1.789 | 18 | 18 | fits | 104,381 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,018,727 | 10.187 | 18 | 18 | fits | 21,164 | 14 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 261,790 | 2.618 | 20 | 20 | fits | 64,511 | 73 | 0.598 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 65,888 | 0.659 | 20 | 200 | fits | 71,159 | 135 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 318,374 | 3.184 | 20 | 200 | fits | 64,511 | 73 | 0.598 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 66,800 | 0.668 | 20 | 20 | fits | 71,159 | 135 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 461,906 | 4.619 | 20 | 20 | fits | 70,488 | 45 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 70,385 | 0.704 | 20 | 24 | fits | 71,159 | 135 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 939,847 | 9.398 | 20 | 24 | fits | 46,856 | 29 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 69,345 | 0.693 | 20 | 50 | fits | 71,159 | 135 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 322,050 | 3.220 | 20 | 50 | fits | 64,511 | 73 | 0.598 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 173,271 | 1.733 | 18 | 18 | fits | 104,381 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,018,879 | 10.189 | 18 | 18 | fits | 21,206 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 270,877 | 2.709 | 20 | 20 | fits | 87,188 | 82 | 0.647 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 70,173 | 0.702 | 20 | 200 | fits | 71,159 | 135 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 349,755 | 3.498 | 20 | 200 | fits | 87,188 | 82 | 0.647 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 71,085 | 0.711 | 20 | 20 | fits | 71,159 | 135 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 483,582 | 4.836 | 20 | 20 | fits | 62,047 | 41 | 0.694 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 74,670 | 0.747 | 20 | 24 | fits | 71,159 | 135 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 959,974 | 9.600 | 20 | 24 | fits | 46,627 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 73,630 | 0.736 | 20 | 50 | fits | 71,159 | 135 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 353,431 | 3.534 | 20 | 50 | fits | 87,188 | 82 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 177,485 | 1.775 | 18 | 18 | fits | 104,310 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,017,455 | 10.175 | 18 | 18 | fits | 29,220 | 17 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 272,155 | 2.722 | 20 | 20 | fits | 86,980 | 82 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 74,456 | 0.745 | 20 | 200 | fits | 71,248 | 136 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 350,963 | 3.510 | 20 | 200 | fits | 86,980 | 82 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 75,368 | 0.754 | 20 | 20 | fits | 71,248 | 136 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 551,770 | 5.518 | 20 | 20 | fits | 62,481 | 37 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 78,953 | 0.790 | 20 | 24 | fits | 71,248 | 136 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 975,926 | 9.759 | 20 | 24 | fits | 46,627 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 77,913 | 0.779 | 20 | 50 | fits | 71,248 | 136 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 354,639 | 3.546 | 20 | 50 | fits | 86,980 | 82 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 183,214 | 1.832 | 18 | 18 | fits | 105,756 | 144 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,025,356 | 10.254 | 18 | 18 | fits | 21,169 | 14 | 0.782 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 310,014 | 3.100 | 20 | 20 | fits | 80,081 | 55 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 74,391 | 0.744 | 20 | 200 | fits | 70,759 | 135 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 383,401 | 3.834 | 20 | 200 | fits | 80,081 | 55 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 75,303 | 0.753 | 20 | 20 | fits | 70,759 | 135 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 515,159 | 5.152 | 20 | 20 | fits | 61,230 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 78,888 | 0.789 | 20 | 24 | fits | 70,759 | 135 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 921,015 | 9.210 | 20 | 24 | fits | 46,942 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 77,848 | 0.778 | 20 | 50 | fits | 70,759 | 135 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 306,996 | 3.070 | 20 | 50 | fits | 63,723 | 62 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 181,373 | 1.814 | 18 | 18 | fits | 103,980 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,029,635 | 10.296 | 18 | 18 | fits | 21,314 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 302,971 | 3.030 | 20 | 20 | fits | 79,992 | 55 | 0.689 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 68,822 | 0.688 | 20 | 200 | fits | 70,759 | 135 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 376,324 | 3.763 | 20 | 200 | fits | 79,992 | 55 | 0.689 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 69,734 | 0.697 | 20 | 20 | fits | 70,759 | 135 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 508,096 | 5.081 | 20 | 20 | fits | 61,237 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 73,319 | 0.733 | 20 | 24 | fits | 70,759 | 135 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 937,867 | 9.379 | 20 | 24 | fits | 46,945 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 72,279 | 0.723 | 20 | 50 | fits | 70,759 | 135 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 300,008 | 3.000 | 20 | 50 | fits | 84,644 | 96 | 0.602 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 215,299 | 2.153 | 18 | 18 | fits | 75,858 | 62 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,027,008 | 10.270 | 18 | 18 | fits | 23,306 | 14 | 0.835 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 265,229 | 2.652 | 20 | 20 | fits | 86,966 | 82 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 68,827 | 0.688 | 20 | 200 | fits | 72,571 | 133 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 344,073 | 3.441 | 20 | 200 | fits | 86,966 | 82 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 69,739 | 0.697 | 20 | 20 | fits | 72,571 | 133 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 494,914 | 4.949 | 20 | 20 | fits | 70,097 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 73,324 | 0.733 | 20 | 24 | fits | 72,571 | 133 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 957,304 | 9.573 | 20 | 24 | fits | 38,222 | 25 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 72,284 | 0.723 | 20 | 50 | fits | 72,571 | 133 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 347,749 | 3.477 | 20 | 50 | fits | 86,966 | 82 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 176,250 | 1.762 | 18 | 18 | fits | 104,421 | 139 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,089,312 | 10.893 | 18 | 18 | fits | 30,194 | 17 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 274,120 | 2.741 | 20 | 20 | fits | 88,003 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 69,484 | 0.695 | 20 | 200 | fits | 70,379 | 133 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 353,827 | 3.538 | 20 | 200 | fits | 88,003 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 70,396 | 0.704 | 20 | 20 | fits | 70,379 | 133 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 495,425 | 4.954 | 20 | 20 | fits | 70,044 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 73,981 | 0.740 | 20 | 24 | fits | 70,379 | 133 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 1,033,378 | 10.334 | 20 | 24 | fits | 38,498 | 26 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 72,941 | 0.729 | 20 | 50 | fits | 70,379 | 133 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 357,503 | 3.575 | 20 | 50 | fits | 88,003 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 176,973 | 1.770 | 18 | 18 | fits | 104,487 | 139 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,093,228 | 10.932 | 18 | 18 | fits | 29,480 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 275,843 | 2.758 | 20 | 20 | fits | 86,833 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 70,727 | 0.707 | 20 | 200 | fits | 70,379 | 133 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 354,799 | 3.548 | 20 | 200 | fits | 86,833 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 71,639 | 0.716 | 20 | 20 | fits | 70,379 | 133 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 496,397 | 4.964 | 20 | 20 | fits | 70,044 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 75,224 | 0.752 | 20 | 24 | fits | 70,379 | 133 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 1,046,756 | 10.468 | 20 | 24 | fits | 47,095 | 30 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 74,184 | 0.742 | 20 | 50 | fits | 70,379 | 133 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 358,475 | 3.585 | 20 | 50 | fits | 86,833 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 178,216 | 1.782 | 18 | 18 | fits | 104,487 | 139 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,096,615 | 10.966 | 18 | 18 | fits | 21,424 | 15 | 0.773 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 266,764 | 2.668 | 20 | 20 | fits | 86,888 | 81 | 0.646 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 71,466 | 0.715 | 20 | 200 | fits | 69,659 | 132 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 345,775 | 3.458 | 20 | 200 | fits | 86,888 | 81 | 0.646 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 72,378 | 0.724 | 20 | 20 | fits | 69,659 | 132 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 487,373 | 4.874 | 20 | 20 | fits | 70,044 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 75,963 | 0.760 | 20 | 24 | fits | 69,659 | 132 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 1,021,756 | 10.218 | 20 | 24 | fits | 47,095 | 30 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 74,923 | 0.749 | 20 | 50 | fits | 69,659 | 132 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 349,451 | 3.495 | 20 | 50 | fits | 86,888 | 81 | 0.646 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 178,246 | 1.782 | 18 | 18 | fits | 103,778 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,100,977 | 11.010 | 18 | 18 | fits | 21,306 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 266,538 | 2.665 | 20 | 20 | fits | 86,888 | 81 | 0.646 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 71,240 | 0.712 | 20 | 200 | fits | 69,659 | 132 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 345,549 | 3.455 | 20 | 200 | fits | 86,888 | 81 | 0.646 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 72,152 | 0.722 | 20 | 20 | fits | 69,659 | 132 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 464,156 | 4.642 | 20 | 20 | fits | 47,053 | 35 | 0.622 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 75,737 | 0.757 | 20 | 24 | fits | 69,659 | 132 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 1,016,593 | 10.166 | 20 | 24 | fits | 46,950 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 74,697 | 0.747 | 20 | 50 | fits | 69,659 | 132 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 349,225 | 3.492 | 20 | 50 | fits | 86,888 | 81 | 0.646 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 178,020 | 1.780 | 18 | 18 | fits | 103,778 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,105,685 | 11.057 | 18 | 18 | fits | 21,321 | 14 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 266,221 | 2.662 | 20 | 20 | fits | 64,561 | 72 | 0.599 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 70,923 | 0.709 | 20 | 200 | fits | 69,659 | 132 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 322,905 | 3.229 | 20 | 200 | fits | 64,561 | 72 | 0.599 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 71,835 | 0.718 | 20 | 20 | fits | 69,659 | 132 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 593,494 | 5.935 | 20 | 20 | fits | 64,338 | 44 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 75,420 | 0.754 | 20 | 24 | fits | 69,659 | 132 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 1,027,574 | 10.276 | 20 | 24 | fits | 46,856 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 74,380 | 0.744 | 20 | 50 | fits | 69,659 | 132 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 326,581 | 3.266 | 20 | 50 | fits | 64,561 | 72 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 177,703 | 1.777 | 18 | 18 | fits | 103,778 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,106,070 | 11.061 | 18 | 18 | fits | 21,026 | 14 | 0.774 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 383,791 | 3.838 | 20 | 20 | fits | 57,343 | 47 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 70,606 | 0.706 | 20 | 200 | fits | 69,659 | 132 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 434,784 | 4.348 | 20 | 200 | fits | 57,343 | 47 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 71,518 | 0.715 | 20 | 20 | fits | 69,659 | 132 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 569,007 | 5.690 | 20 | 20 | fits | 61,612 | 38 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 75,103 | 0.751 | 20 | 24 | fits | 69,659 | 132 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 1,004,661 | 10.047 | 20 | 24 | fits | 46,944 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 74,063 | 0.741 | 20 | 50 | fits | 69,659 | 132 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 303,110 | 3.031 | 20 | 50 | fits | 63,808 | 62 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 177,386 | 1.774 | 18 | 18 | fits | 103,778 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,112,791 | 11.128 | 18 | 18 | fits | 21,198 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 385,340 | 3.853 | 20 | 20 | fits | 80,603 | 56 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 70,289 | 0.703 | 20 | 200 | fits | 69,659 | 132 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 459,012 | 4.590 | 20 | 200 | fits | 80,603 | 56 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 71,201 | 0.712 | 20 | 20 | fits | 69,659 | 132 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 591,252 | 5.913 | 20 | 20 | fits | 61,451 | 38 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 74,786 | 0.748 | 20 | 24 | fits | 69,659 | 132 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 1,026,120 | 10.261 | 20 | 24 | fits | 46,790 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 73,746 | 0.737 | 20 | 50 | fits | 69,659 | 132 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 382,085 | 3.821 | 20 | 50 | fits | 86,016 | 103 | 0.596 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 155,937 | 1.559 | 18 | 18 | fits | 82,646 | 103 | 0.689 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,122,430 | 11.224 | 18 | 18 | fits | 21,198 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 292,760 | 2.928 | 20 | 20 | fits | 81,435 | 59 | 0.673 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 101,043 | 1.010 | 20 | 200 | fits | 70,065 | 135 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 366,023 | 3.660 | 20 | 200 | fits | 81,435 | 59 | 0.673 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 101,955 | 1.020 | 20 | 20 | fits | 70,065 | 135 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 516,269 | 5.163 | 20 | 20 | fits | 70,143 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 35,475 | 0.355 | 20 | 24 | fits | 38,284 | 70 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 940,421 | 9.404 | 20 | 24 | fits | 46,625 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 34,435 | 0.344 | 20 | 50 | fits | 38,284 | 70 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 288,264 | 2.883 | 20 | 50 | fits | 79,770 | 75 | 0.634 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 208,429 | 2.084 | 18 | 18 | fits | 104,384 | 139 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,098,867 | 10.989 | 18 | 18 | fits | 21,009 | 14 | 0.774 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 269,953 | 2.700 | 20 | 20 | fits | 88,090 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 64,461 | 0.645 | 20 | 200 | fits | 70,666 | 133 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 349,682 | 3.497 | 20 | 200 | fits | 88,090 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 65,373 | 0.654 | 20 | 20 | fits | 70,666 | 133 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 491,264 | 4.913 | 20 | 20 | fits | 70,036 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 68,958 | 0.690 | 20 | 24 | fits | 70,666 | 133 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 1,034,184 | 10.342 | 20 | 24 | fits | 38,415 | 26 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 67,918 | 0.679 | 20 | 50 | fits | 70,666 | 133 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 353,358 | 3.534 | 20 | 50 | fits | 88,090 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 172,841 | 1.728 | 18 | 18 | fits | 105,378 | 144 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,094,074 | 10.941 | 18 | 18 | fits | 29,488 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 271,187 | 2.712 | 20 | 20 | fits | 86,782 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 66,054 | 0.661 | 20 | 200 | fits | 70,666 | 133 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 350,042 | 3.500 | 20 | 200 | fits | 86,782 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 66,966 | 0.670 | 20 | 20 | fits | 70,666 | 133 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 491,624 | 4.916 | 20 | 20 | fits | 70,036 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 70,551 | 0.706 | 20 | 24 | fits | 70,666 | 133 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 1,000,527 | 10.005 | 20 | 24 | fits | 47,079 | 30 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 69,511 | 0.695 | 20 | 50 | fits | 70,666 | 133 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 353,718 | 3.537 | 20 | 50 | fits | 86,782 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 173,472 | 1.735 | 18 | 18 | fits | 104,416 | 139 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,109,132 | 11.091 | 18 | 18 | fits | 21,314 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 260,806 | 2.608 | 20 | 20 | fits | 86,782 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 65,510 | 0.655 | 20 | 200 | fits | 70,027 | 132 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 339,661 | 3.397 | 20 | 200 | fits | 86,782 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 66,422 | 0.664 | 20 | 20 | fits | 70,027 | 132 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 481,243 | 4.812 | 20 | 20 | fits | 70,036 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 70,007 | 0.700 | 20 | 24 | fits | 70,027 | 132 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 1,013,883 | 10.139 | 20 | 24 | fits | 46,942 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 68,967 | 0.690 | 20 | 50 | fits | 70,027 | 132 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 343,337 | 3.433 | 20 | 50 | fits | 86,782 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 172,246 | 1.722 | 18 | 18 | fits | 103,734 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,093,128 | 10.931 | 18 | 18 | fits | 21,314 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 260,277 | 2.603 | 20 | 20 | fits | 86,782 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 64,019 | 0.640 | 20 | 200 | fits | 70,027 | 132 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 339,132 | 3.391 | 20 | 200 | fits | 86,782 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 64,931 | 0.649 | 20 | 20 | fits | 70,027 | 132 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 457,723 | 4.577 | 20 | 20 | fits | 47,045 | 35 | 0.622 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 68,516 | 0.685 | 20 | 24 | fits | 70,027 | 132 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 1,015,422 | 10.154 | 20 | 24 | fits | 46,942 | 30 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 67,476 | 0.675 | 20 | 50 | fits | 70,027 | 132 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 342,808 | 3.428 | 20 | 50 | fits | 86,782 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 171,717 | 1.717 | 18 | 18 | fits | 104,696 | 143 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,104,613 | 11.046 | 18 | 18 | fits | 21,329 | 14 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 260,277 | 2.603 | 20 | 20 | fits | 78,510 | 77 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 64,019 | 0.640 | 20 | 200 | fits | 70,027 | 132 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 330,860 | 3.309 | 20 | 200 | fits | 78,510 | 77 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 64,931 | 0.649 | 20 | 20 | fits | 70,027 | 132 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 584,817 | 5.848 | 20 | 20 | fits | 62,955 | 44 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 68,516 | 0.685 | 20 | 24 | fits | 70,027 | 132 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 1,020,457 | 10.205 | 20 | 24 | fits | 46,915 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 67,476 | 0.675 | 20 | 50 | fits | 70,027 | 132 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 334,536 | 3.345 | 20 | 50 | fits | 78,510 | 77 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 171,717 | 1.717 | 18 | 18 | fits | 104,696 | 143 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,107,555 | 11.076 | 18 | 18 | fits | 29,267 | 17 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 383,491 | 3.835 | 20 | 20 | fits | 57,241 | 47 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 64,019 | 0.640 | 20 | 200 | fits | 70,027 | 132 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 434,538 | 4.345 | 20 | 200 | fits | 57,241 | 47 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 64,931 | 0.649 | 20 | 20 | fits | 70,027 | 132 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 568,815 | 5.688 | 20 | 20 | fits | 61,604 | 38 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 68,516 | 0.685 | 20 | 24 | fits | 70,027 | 132 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 1,004,416 | 10.044 | 20 | 24 | fits | 46,936 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 67,476 | 0.675 | 20 | 50 | fits | 70,027 | 132 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 297,348 | 2.973 | 20 | 50 | fits | 63,723 | 62 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 171,717 | 1.717 | 18 | 18 | fits | 104,696 | 143 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,112,700 | 11.127 | 18 | 18 | fits | 21,206 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 392,780 | 3.928 | 20 | 20 | fits | 80,435 | 55 | 0.694 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 64,019 | 0.640 | 20 | 200 | fits | 70,027 | 132 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 466,445 | 4.664 | 20 | 200 | fits | 80,435 | 55 | 0.694 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 64,931 | 0.649 | 20 | 20 | fits | 70,027 | 132 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 598,323 | 5.983 | 20 | 20 | fits | 61,241 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 68,516 | 0.685 | 20 | 24 | fits | 70,027 | 132 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 1,022,439 | 10.224 | 20 | 24 | fits | 46,627 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 67,476 | 0.675 | 20 | 50 | fits | 70,027 | 132 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 389,686 | 3.897 | 20 | 50 | fits | 89,160 | 102 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 211,102 | 2.111 | 18 | 18 | fits | 75,574 | 62 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,119,596 | 11.196 | 18 | 18 | fits | 21,204 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 272,362 | 2.724 | 20 | 20 | fits | 88,082 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 67,795 | 0.678 | 20 | 200 | fits | 70,517 | 133 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 352,083 | 3.521 | 20 | 200 | fits | 88,082 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 68,707 | 0.687 | 20 | 20 | fits | 70,517 | 133 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 493,746 | 4.937 | 20 | 20 | fits | 70,052 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 72,292 | 0.723 | 20 | 24 | fits | 70,517 | 133 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 956,277 | 9.563 | 20 | 24 | fits | 38,228 | 25 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 71,252 | 0.713 | 20 | 50 | fits | 70,517 | 133 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 355,759 | 3.558 | 20 | 50 | fits | 88,082 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 175,221 | 1.752 | 18 | 18 | fits | 104,424 | 139 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,099,060 | 10.991 | 18 | 18 | fits | 34,032 | 23 | 0.785 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 274,352 | 2.744 | 20 | 20 | fits | 86,904 | 81 | 0.647 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 69,142 | 0.691 | 20 | 200 | fits | 70,517 | 133 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 353,265 | 3.533 | 20 | 200 | fits | 86,904 | 81 | 0.647 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 70,054 | 0.701 | 20 | 20 | fits | 70,517 | 133 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 494,879 | 4.949 | 20 | 20 | fits | 70,052 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 73,639 | 0.736 | 20 | 24 | fits | 70,517 | 133 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 1,051,729 | 10.517 | 20 | 24 | fits | 47,095 | 29 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 72,599 | 0.726 | 20 | 50 | fits | 70,517 | 133 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 356,941 | 3.569 | 20 | 50 | fits | 86,904 | 81 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 176,568 | 1.766 | 18 | 18 | fits | 104,424 | 139 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,101,377 | 11.014 | 18 | 18 | fits | 21,336 | 14 | 0.782 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 261,348 | 2.613 | 20 | 20 | fits | 86,798 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 64,775 | 0.648 | 20 | 200 | fits | 70,907 | 132 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 340,261 | 3.403 | 20 | 200 | fits | 86,798 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 65,687 | 0.657 | 20 | 20 | fits | 70,907 | 132 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 481,875 | 4.819 | 20 | 20 | fits | 70,052 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 69,272 | 0.693 | 20 | 24 | fits | 70,907 | 132 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 1,015,891 | 10.159 | 20 | 24 | fits | 46,954 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 68,232 | 0.682 | 20 | 50 | fits | 70,907 | 132 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 343,937 | 3.439 | 20 | 50 | fits | 86,798 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 172,822 | 1.728 | 18 | 18 | fits | 105,045 | 143 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,094,806 | 10.948 | 18 | 18 | fits | 21,206 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 264,235 | 2.642 | 20 | 20 | fits | 86,798 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 68,745 | 0.687 | 20 | 200 | fits | 69,878 | 132 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 343,148 | 3.431 | 20 | 200 | fits | 86,798 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 69,657 | 0.697 | 20 | 20 | fits | 69,878 | 132 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 484,762 | 4.848 | 20 | 20 | fits | 70,052 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 73,242 | 0.732 | 20 | 24 | fits | 69,878 | 132 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 1,034,237 | 10.342 | 20 | 24 | fits | 46,816 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 72,202 | 0.722 | 20 | 50 | fits | 69,878 | 132 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 346,824 | 3.468 | 20 | 50 | fits | 86,798 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 175,701 | 1.757 | 18 | 18 | fits | 103,954 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,091,941 | 10.919 | 18 | 18 | fits | 29,392 | 17 | 0.732 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 264,022 | 2.640 | 20 | 20 | fits | 86,798 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 68,532 | 0.685 | 20 | 200 | fits | 69,878 | 132 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 342,935 | 3.429 | 20 | 200 | fits | 86,798 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 69,444 | 0.694 | 20 | 20 | fits | 69,878 | 132 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 461,558 | 4.616 | 20 | 20 | fits | 47,061 | 35 | 0.622 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 73,029 | 0.730 | 20 | 24 | fits | 69,878 | 132 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 1,019,307 | 10.193 | 20 | 24 | fits | 46,816 | 29 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 71,989 | 0.720 | 20 | 50 | fits | 69,878 | 132 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 346,611 | 3.466 | 20 | 50 | fits | 86,798 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 175,488 | 1.755 | 18 | 18 | fits | 103,954 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,098,222 | 10.982 | 18 | 18 | fits | 21,206 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 263,809 | 2.638 | 20 | 20 | fits | 64,471 | 72 | 0.598 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 68,319 | 0.683 | 20 | 200 | fits | 69,878 | 132 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 320,395 | 3.204 | 20 | 200 | fits | 64,471 | 72 | 0.598 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 69,231 | 0.692 | 20 | 20 | fits | 69,878 | 132 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 598,614 | 5.986 | 20 | 20 | fits | 61,811 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 72,816 | 0.728 | 20 | 24 | fits | 69,878 | 132 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 1,022,982 | 10.230 | 20 | 24 | fits | 46,641 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 71,776 | 0.718 | 20 | 50 | fits | 69,878 | 132 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 324,071 | 3.241 | 20 | 50 | fits | 64,471 | 72 | 0.598 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 175,275 | 1.753 | 18 | 18 | fits | 103,954 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,101,380 | 11.014 | 18 | 18 | fits | 21,034 | 14 | 0.774 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 391,259 | 3.913 | 20 | 20 | fits | 84,412 | 61 | 0.706 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 68,106 | 0.681 | 20 | 200 | fits | 69,878 | 132 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 466,133 | 4.661 | 20 | 200 | fits | 84,412 | 61 | 0.706 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 69,018 | 0.690 | 20 | 20 | fits | 69,878 | 132 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 598,686 | 5.987 | 20 | 20 | fits | 61,421 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 72,603 | 0.726 | 20 | 24 | fits | 69,878 | 132 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 1,022,855 | 10.229 | 20 | 24 | fits | 46,627 | 29 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 71,563 | 0.716 | 20 | 50 | fits | 69,878 | 132 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 300,814 | 3.008 | 20 | 50 | fits | 63,828 | 63 | 0.694 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 175,062 | 1.751 | 18 | 18 | fits | 103,954 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,101,453 | 11.015 | 18 | 18 | fits | 21,112 | 14 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 413,861 | 4.139 | 20 | 20 | fits | 80,015 | 55 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 67,893 | 0.679 | 20 | 200 | fits | 69,878 | 132 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 487,279 | 4.873 | 20 | 200 | fits | 80,015 | 55 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 68,805 | 0.688 | 20 | 20 | fits | 69,878 | 132 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 619,141 | 6.191 | 20 | 20 | fits | 61,253 | 37 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 72,390 | 0.724 | 20 | 24 | fits | 69,878 | 132 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 1,023,558 | 10.236 | 20 | 24 | fits | 48,688 | 36 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 71,350 | 0.714 | 20 | 50 | fits | 69,878 | 132 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 410,940 | 4.109 | 20 | 50 | fits | 83,474 | 96 | 0.594 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 153,539 | 1.535 | 18 | 18 | fits | 82,644 | 103 | 0.689 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,119,582 | 11.196 | 18 | 18 | fits | 21,314 | 15 | 0.768 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 229,240 | 2.292 | 20 | 200 | fits | 64,754 | 84 | 0.549 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 367,537 | 3.675 | 20 | 20 | fits | 50,649 | 32 | 0.675 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 501,459 | 5.015 | 20 | 24 | fits | 22,023 | 21 | 0.553 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 250,043 | 2.500 | 20 | 50 | fits | 48,344 | 52 | 0.630 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 710,782 | 7.108 | 18 | 18 | fits | 45,873 | 29 | 0.711 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 237,139 | 2.371 | 20 | 200 | fits | 67,652 | 90 | 0.577 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 382,118 | 3.821 | 20 | 20 | fits | 52,398 | 38 | 0.679 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 564,074 | 5.641 | 20 | 24 | fits | 24,552 | 27 | 0.604 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 267,627 | 2.676 | 20 | 50 | fits | 59,322 | 61 | 0.650 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 799,532 | 7.995 | 18 | 18 | fits | 40,339 | 32 | 0.737 |
| an event behind 15 others | `backlog.event.if0` | 87,952 | 0.880 | 20 | 200 | fits | 64,989 | 104 | 0.511 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 338,095 | 3.381 | 20 | 20 | fits | 46,480 | 44 | 0.522 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 77,177 | 0.772 | 20 | 200 | fits | 77,385 | 138 | 0.516 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 277,591 | 2.776 | 20 | 200 | fits | 55,861 | 55 | 0.558 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 72,918 | 0.729 | 20 | 20 | fits | 77,385 | 138 | 0.516 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 366,526 | 3.665 | 20 | 20 | fits | 46,480 | 44 | 0.522 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 76,503 | 0.765 | 20 | 24 | fits | 77,385 | 138 | 0.516 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 614,818 | 6.148 | 20 | 24 | fits | 24,411 | 29 | 0.485 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 75,463 | 0.755 | 20 | 50 | fits | 77,385 | 138 | 0.516 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 276,096 | 2.761 | 20 | 50 | fits | 55,861 | 55 | 0.558 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 276,031 | 2.760 | 18 | 18 | fits | 55,861 | 55 | 0.558 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 644,243 | 6.442 | 18 | 18 | fits | 10,234 | 17 | 0.245 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 260,883 | 2.609 | 20 | 20 | fits | 64,596 | 73 | 0.600 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 65,355 | 0.654 | 20 | 200 | fits | 70,037 | 135 | 0.487 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 317,552 | 3.176 | 20 | 200 | fits | 64,596 | 73 | 0.600 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 66,267 | 0.663 | 20 | 20 | fits | 70,037 | 135 | 0.487 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 460,895 | 4.609 | 20 | 20 | fits | 70,364 | 45 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 69,852 | 0.699 | 20 | 24 | fits | 70,037 | 135 | 0.487 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 939,019 | 9.390 | 20 | 24 | fits | 46,931 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 68,812 | 0.688 | 20 | 50 | fits | 70,037 | 135 | 0.487 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 321,228 | 3.212 | 20 | 50 | fits | 64,596 | 73 | 0.600 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 172,480 | 1.725 | 18 | 18 | fits | 104,123 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,018,016 | 10.180 | 18 | 18 | fits | 21,201 | 14 | 0.776 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,581 | 0.086 | 20 | 20 | fits | 21,442 | 20 | 0.767 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 65,355 | 0.654 | 20 | 200 | fits | 70,037 | 135 | 0.487 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 23,366 | 0.234 | 20 | 200 | fits | 21,442 | 20 | 0.767 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 66,267 | 0.663 | 20 | 20 | fits | 70,037 | 135 | 0.487 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 451,834 | 4.518 | 20 | 20 | fits | 70,327 | 45 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 69,852 | 0.699 | 20 | 24 | fits | 70,037 | 135 | 0.487 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 906,677 | 9.067 | 20 | 24 | fits | 46,933 | 29 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 68,812 | 0.688 | 20 | 50 | fits | 70,037 | 135 | 0.487 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 312,274 | 3.123 | 20 | 50 | fits | 55,642 | 63 | 0.589 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 172,480 | 1.725 | 18 | 18 | fits | 104,123 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,014,941 | 10.149 | 18 | 18 | fits | 21,201 | 14 | 0.776 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,206,545 | 62.065 | 20 | 20 | MISS ceiling | 28,511 | 25 | 0.562 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,022,448 | 360.224 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,022,373 | 360.224 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,022,298 | 360.223 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,022,223 | 360.222 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 73,322 | 0.733 | 20 | 200 | fits | 67,975 | 129 | 0.498 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 332,165 | 3.322 | 20 | 200 | fits | 76,376 | 67 | 0.657 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 69,063 | 0.691 | 20 | 20 | fits | 67,975 | 129 | 0.498 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 437,104 | 4.371 | 20 | 20 | fits | 48,756 | 29 | 0.788 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 72,648 | 0.726 | 20 | 24 | fits | 67,975 | 129 | 0.498 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,290,713 | 62.907 | 20 | 24 | MISS ceiling | 21,930 | 21 | 0.553 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 71,608 | 0.716 | 20 | 50 | fits | 67,975 | 129 | 0.498 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 330,670 | 3.307 | 20 | 50 | fits | 76,376 | 67 | 0.657 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 172,539 | 1.725 | 18 | 18 | fits | 101,386 | 131 | 0.636 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 791,755 | 7.918 | 18 | 18 | fits | 29,712 | 20 | 0.716 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
