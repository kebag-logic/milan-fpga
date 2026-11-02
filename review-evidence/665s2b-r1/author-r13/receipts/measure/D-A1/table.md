### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 313 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.274 (3.597) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-0.adp_available.if0` (backlog-adp@verify-0) | 3.318 (4.946) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.130 (0.389) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.851 (1.375) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.029 (62.211) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.187 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 1.405 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.acmp.last.if0` (backlog-adp@verify-0) | 5.473 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 1.396 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.adp.last.if0` (backlog-adp@verify-0) | 4.099 | fits | 7 adp | 28 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 1.441 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.904 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 1.431 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 4.136 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.683 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.srp.last.if0` (backlog-adp@blank-0) | 10.597 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.669 | 18 | 101,625 (1.016) | yes | - |
| backlog-adp@blank-1 | 0 | 10.855 | 17 | 101,615 (1.016) | yes | - |
| backlog-adp@blank-2 | 0 | 10.936 | 18 | 101,615 (1.016) | yes | - |
| backlog-adp@blank-3 | 0 | 10.930 | 18 | 101,615 (1.016) | yes | - |
| backlog-adp@blank-4 | 0 | 11.231 | 20 | 101,615 (1.016) | yes | - |
| backlog-adp@blank-5 | 0 | 10.947 | 17 | 103,252 (1.033) | yes | - |
| backlog-adp@blank-6 | 0 | 10.988 | 18 | 101,756 (1.018) | yes | - |
| backlog-adp@blank-7 | 0 | 10.985 | 19 | 97,322 (0.973) | yes | - |
| backlog-adp@program-0 | 0 | 10.896 | 17 | 101,272 (1.013) | yes | - |
| backlog-adp@program-1 | 0 | 10.987 | 17 | 106,965 (1.070) | yes | - |
| backlog-adp@program-2 | 0 | 10.894 | 16 | 101,485 (1.015) | yes | - |
| backlog-adp@program-3 | 0 | 11.025 | 18 | 101,485 (1.015) | yes | - |
| backlog-adp@program-4 | 0 | 10.546 | 20 | 101,610 (1.016) | yes | - |
| backlog-adp@program-5 | 0 | 10.155 | 17 | 101,455 (1.015) | yes | - |
| backlog-adp@program-6 | 0 | 10.239 | 18 | 101,455 (1.015) | yes | - |
| backlog-adp@program-7 | 0 | 10.298 | 18 | 95,860 (0.959) | yes | - |
| backlog-adp@verify-0 | 0 | 11.592 | 17 | 101,597 (1.016) | yes | - |
| backlog-adp@verify-1 | 0 | 11.013 | 18 | 101,487 (1.015) | yes | - |
| backlog-adp@verify-2 | 0 | 10.955 | 18 | 101,487 (1.015) | yes | - |
| backlog-adp@verify-3 | 0 | 10.950 | 18 | 101,487 (1.015) | yes | - |
| backlog-adp@verify-4 | 0 | 11.054 | 18 | 101,487 (1.015) | yes | - |
| backlog-adp@verify-5 | 0 | 10.958 | 17 | 103,131 (1.031) | yes | - |
| backlog-adp@verify-6 | 0 | 10.951 | 18 | 101,565 (1.016) | yes | - |
| backlog-adp@verify-7 | 0 | 10.946 | 18 | 97,218 (0.972) | yes | - |
| backlog | 0 | 6.488 | 19 | 78,902 (0.789) | yes | - |
| backlog-adp | 0 | 10.071 | 17 | 101,382 (1.014) | yes | - |
| backlog-adp-refill | 0 | 40.556 | 30 | 101,382 (1.014) | yes | - |
| backlog-owed | 0 | 360.238 | 65 | 99,645 (0.996) | yes | - |

Composed maximum over the 4 backlog windows: 101,382 CPU cycles (1.014 ms), backlog-adp.
Over the windows that released their whole load only: 101,382 (1.014 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 387 | 0 | 101,625 (1.016) | fits |
| backlog-adp@blank-1 | 386 | 0 | 101,615 (1.016) | fits |
| backlog-adp@blank-2 | 387 | 0 | 101,615 (1.016) | fits |
| backlog-adp@blank-3 | 387 | 0 | 101,615 (1.016) | fits |
| backlog-adp@blank-4 | 389 | 0 | 101,615 (1.016) | fits |
| backlog-adp@blank-5 | 386 | 0 | 103,252 (1.033) | fits |
| backlog-adp@blank-6 | 389 | 0 | 101,756 (1.018) | fits |
| backlog-adp@blank-7 | 390 | 0 | 97,322 (0.973) | fits |
| backlog-adp@program-0 | 462 | 0 | 118,022 (1.180) | fits |
| backlog-adp@program-1 | 462 | 0 | 118,022 (1.180) | fits |
| backlog-adp@program-2 | 464 | 0 | 118,022 (1.180) | fits |
| backlog-adp@program-3 | 465 | 0 | 118,022 (1.180) | fits |
| backlog-adp@program-4 | 468 | 0 | 118,022 (1.180) | fits |
| backlog-adp@program-5 | 466 | 0 | 118,022 (1.180) | fits |
| backlog-adp@program-6 | 467 | 0 | 118,022 (1.180) | fits |
| backlog-adp@program-7 | 467 | 0 | 118,022 (1.180) | fits |
| backlog-adp@verify-0 | 538 | 0 | 118,022 (1.180) | fits |
| backlog-adp@verify-1 | 539 | 0 | 118,022 (1.180) | fits |
| backlog-adp@verify-2 | 539 | 0 | 118,022 (1.180) | fits |
| backlog-adp@verify-3 | 539 | 0 | 118,022 (1.180) | fits |
| backlog-adp@verify-4 | 539 | 0 | 118,022 (1.180) | fits |
| backlog-adp@verify-5 | 538 | 0 | 118,022 (1.180) | fits |
| backlog-adp@verify-6 | 540 | 0 | 118,022 (1.180) | fits |
| backlog-adp@verify-7 | 540 | 0 | 118,022 (1.180) | fits |
| save | 602 | 0 | 117,232 (1.172) | fits |
| backlog | 293 | 0 | 78,902 (0.789) | fits |
| backlog-adp | 310 | 0 | 101,382 (1.014) | fits |
| backlog-adp-refill | 323 | 0 | 101,382 (1.014) | fits |
| backlog-owed | 350 | 0 | 99,645 (0.996) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 330,449 | 3.304 | 20 | 20 | fits | 86,315 | 81 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 138,284 | 1.383 | 20 | 200 | fits | 68,850 | 135 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 408,618 | 4.086 | 20 | 200 | fits | 86,315 | 81 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 139,196 | 1.392 | 20 | 20 | fits | 68,850 | 135 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 545,929 | 5.459 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 142,781 | 1.428 | 20 | 24 | fits | 68,850 | 135 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 995,693 | 9.957 | 20 | 24 | fits | 24,821 | 20 | 0.694 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 141,741 | 1.417 | 20 | 50 | fits | 68,850 | 135 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 412,294 | 4.123 | 20 | 50 | fits | 86,315 | 81 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 242,911 | 2.429 | 18 | 18 | fits | 101,625 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,059,717 | 10.597 | 18 | 18 | fits | 30,516 | 17 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 258,901 | 2.589 | 20 | 20 | fits | 86,315 | 81 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 66,693 | 0.667 | 20 | 200 | fits | 68,332 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 337,070 | 3.371 | 20 | 200 | fits | 86,315 | 81 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 67,605 | 0.676 | 20 | 20 | fits | 68,332 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 474,381 | 4.744 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 71,190 | 0.712 | 20 | 24 | fits | 68,332 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 948,937 | 9.489 | 20 | 24 | fits | 45,937 | 29 | 0.740 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 70,150 | 0.702 | 20 | 50 | fits | 68,332 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 340,746 | 3.407 | 20 | 50 | fits | 86,315 | 81 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 171,310 | 1.713 | 18 | 18 | fits | 101,615 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 978,169 | 9.782 | 18 | 18 | fits | 31,767 | 19 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 259,103 | 2.591 | 20 | 20 | fits | 86,315 | 81 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 66,895 | 0.669 | 20 | 200 | fits | 68,332 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 337,272 | 3.373 | 20 | 200 | fits | 86,315 | 81 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 67,807 | 0.678 | 20 | 20 | fits | 68,332 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 458,105 | 4.581 | 20 | 20 | fits | 51,367 | 46 | 0.638 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 71,392 | 0.714 | 20 | 24 | fits | 68,332 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 926,667 | 9.267 | 20 | 24 | fits | 45,872 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 70,352 | 0.704 | 20 | 50 | fits | 68,332 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 340,948 | 3.409 | 20 | 50 | fits | 86,315 | 81 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 171,512 | 1.715 | 18 | 18 | fits | 101,615 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 986,365 | 9.864 | 18 | 18 | fits | 30,466 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 259,305 | 2.593 | 20 | 20 | fits | 69,381 | 83 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 67,097 | 0.671 | 20 | 200 | fits | 68,332 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 320,540 | 3.205 | 20 | 200 | fits | 69,381 | 83 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 68,009 | 0.680 | 20 | 20 | fits | 68,332 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 460,206 | 4.602 | 20 | 20 | fits | 68,079 | 44 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 71,594 | 0.716 | 20 | 24 | fits | 68,332 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 926,107 | 9.261 | 20 | 24 | fits | 45,903 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 70,554 | 0.706 | 20 | 50 | fits | 68,332 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 324,216 | 3.242 | 20 | 50 | fits | 69,381 | 83 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 171,714 | 1.717 | 18 | 18 | fits | 101,615 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 985,831 | 9.858 | 18 | 18 | fits | 30,466 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 244,405 | 2.444 | 20 | 20 | fits | 87,753 | 87 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 67,299 | 0.673 | 20 | 200 | fits | 68,332 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 322,268 | 3.223 | 20 | 200 | fits | 87,753 | 87 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 68,211 | 0.682 | 20 | 20 | fits | 68,332 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 459,616 | 4.596 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 71,796 | 0.718 | 20 | 24 | fits | 68,332 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 903,393 | 9.034 | 20 | 24 | fits | 45,903 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 70,756 | 0.708 | 20 | 50 | fits | 68,332 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 325,944 | 3.259 | 20 | 50 | fits | 87,753 | 87 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 171,916 | 1.719 | 18 | 18 | fits | 101,615 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,015,902 | 10.159 | 18 | 18 | fits | 24,364 | 20 | 0.813 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 266,564 | 2.666 | 20 | 20 | fits | 86,313 | 81 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 72,708 | 0.727 | 20 | 200 | fits | 73,539 | 146 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 344,731 | 3.447 | 20 | 200 | fits | 86,313 | 81 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 73,620 | 0.736 | 20 | 20 | fits | 73,539 | 146 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 486,610 | 4.866 | 20 | 20 | fits | 67,936 | 44 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 77,205 | 0.772 | 20 | 24 | fits | 73,539 | 146 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 958,112 | 9.581 | 20 | 24 | fits | 46,231 | 29 | 0.743 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 76,165 | 0.762 | 20 | 50 | fits | 73,539 | 146 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 348,407 | 3.484 | 20 | 50 | fits | 86,313 | 81 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 178,962 | 1.790 | 18 | 18 | fits | 103,252 | 143 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 987,371 | 9.874 | 18 | 18 | fits | 31,794 | 19 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 253,418 | 2.534 | 20 | 20 | fits | 90,190 | 87 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 66,092 | 0.661 | 20 | 200 | fits | 68,042 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 332,010 | 3.320 | 20 | 200 | fits | 90,190 | 87 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 67,004 | 0.670 | 20 | 20 | fits | 68,042 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 469,354 | 4.694 | 20 | 20 | fits | 67,903 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 70,589 | 0.706 | 20 | 24 | fits | 68,042 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 931,822 | 9.318 | 20 | 24 | fits | 45,926 | 29 | 0.740 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 69,549 | 0.695 | 20 | 50 | fits | 68,042 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 335,686 | 3.357 | 20 | 50 | fits | 90,190 | 87 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 170,850 | 1.708 | 18 | 18 | fits | 101,756 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 991,504 | 9.915 | 18 | 18 | fits | 30,458 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 237,527 | 2.375 | 20 | 20 | fits | 86,816 | 81 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 66,294 | 0.663 | 20 | 200 | fits | 68,042 | 135 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 315,697 | 3.157 | 20 | 200 | fits | 86,816 | 81 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 67,206 | 0.672 | 20 | 20 | fits | 68,042 | 135 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 453,036 | 4.530 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 70,791 | 0.708 | 20 | 24 | fits | 68,042 | 135 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 901,087 | 9.011 | 20 | 24 | fits | 45,864 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 69,751 | 0.698 | 20 | 50 | fits | 68,042 | 135 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 319,373 | 3.194 | 20 | 50 | fits | 86,816 | 81 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 232,492 | 2.325 | 18 | 18 | fits | 97,322 | 102 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 991,148 | 9.911 | 18 | 18 | fits | 30,379 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 256,643 | 2.566 | 20 | 20 | fits | 86,357 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 64,823 | 0.648 | 20 | 200 | fits | 69,248 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 334,812 | 3.348 | 20 | 200 | fits | 86,357 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 65,735 | 0.657 | 20 | 20 | fits | 69,248 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 481,370 | 4.814 | 20 | 20 | fits | 70,943 | 50 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 69,320 | 0.693 | 20 | 24 | fits | 69,248 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 947,186 | 9.472 | 20 | 24 | fits | 49,756 | 35 | 0.747 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 68,280 | 0.683 | 20 | 50 | fits | 69,248 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 338,488 | 3.385 | 20 | 50 | fits | 86,357 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 169,097 | 1.691 | 18 | 18 | fits | 101,272 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 976,571 | 9.766 | 18 | 18 | fits | 31,920 | 19 | 0.796 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 265,147 | 2.651 | 20 | 20 | fits | 86,432 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 65,227 | 0.652 | 20 | 200 | fits | 69,248 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 343,313 | 3.433 | 20 | 200 | fits | 86,432 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 66,139 | 0.661 | 20 | 20 | fits | 69,248 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 480,822 | 4.808 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 69,724 | 0.697 | 20 | 24 | fits | 69,248 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 947,126 | 9.471 | 20 | 24 | fits | 45,903 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 68,684 | 0.687 | 20 | 50 | fits | 69,248 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 346,989 | 3.470 | 20 | 50 | fits | 86,432 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 175,194 | 1.752 | 18 | 18 | fits | 106,965 | 149 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 985,587 | 9.856 | 18 | 18 | fits | 40,996 | 37 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 256,302 | 2.563 | 20 | 20 | fits | 86,357 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 64,205 | 0.642 | 20 | 200 | fits | 69,093 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 334,471 | 3.345 | 20 | 200 | fits | 86,357 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 65,117 | 0.651 | 20 | 20 | fits | 69,093 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 476,437 | 4.764 | 20 | 20 | fits | 72,416 | 50 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 68,702 | 0.687 | 20 | 24 | fits | 69,093 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 947,032 | 9.470 | 20 | 24 | fits | 45,903 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 67,662 | 0.677 | 20 | 50 | fits | 69,093 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 338,147 | 3.381 | 20 | 50 | fits | 86,357 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 168,692 | 1.687 | 18 | 18 | fits | 101,485 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 976,290 | 9.763 | 18 | 18 | fits | 31,793 | 19 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 260,351 | 2.604 | 20 | 20 | fits | 86,405 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 64,609 | 0.646 | 20 | 200 | fits | 69,093 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 338,457 | 3.385 | 20 | 200 | fits | 86,405 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 65,521 | 0.655 | 20 | 20 | fits | 69,093 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 473,494 | 4.735 | 20 | 20 | fits | 65,515 | 51 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 69,106 | 0.691 | 20 | 24 | fits | 69,093 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 937,885 | 9.379 | 20 | 24 | fits | 45,872 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 68,066 | 0.681 | 20 | 50 | fits | 69,093 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 342,133 | 3.421 | 20 | 50 | fits | 86,405 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 169,096 | 1.691 | 18 | 18 | fits | 101,485 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 989,409 | 9.894 | 18 | 18 | fits | 22,292 | 14 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 244,857 | 2.449 | 20 | 20 | fits | 87,840 | 87 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 67,745 | 0.677 | 20 | 200 | fits | 69,711 | 135 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 322,720 | 3.227 | 20 | 200 | fits | 87,840 | 87 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 68,657 | 0.687 | 20 | 20 | fits | 69,711 | 135 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 460,152 | 4.602 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 72,242 | 0.722 | 20 | 24 | fits | 69,711 | 135 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 913,747 | 9.137 | 20 | 24 | fits | 37,573 | 25 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 71,202 | 0.712 | 20 | 50 | fits | 69,711 | 135 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 326,396 | 3.264 | 20 | 50 | fits | 87,840 | 87 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 172,357 | 1.724 | 18 | 18 | fits | 101,610 | 138 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 999,712 | 9.997 | 18 | 18 | fits | 22,213 | 14 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 259,501 | 2.595 | 20 | 20 | fits | 86,357 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 67,434 | 0.674 | 20 | 200 | fits | 69,180 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 337,670 | 3.377 | 20 | 200 | fits | 86,357 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 68,346 | 0.683 | 20 | 20 | fits | 69,180 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 475,065 | 4.751 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 71,931 | 0.719 | 20 | 24 | fits | 69,180 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 949,741 | 9.497 | 20 | 24 | fits | 45,872 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 70,891 | 0.709 | 20 | 50 | fits | 69,180 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 341,346 | 3.413 | 20 | 50 | fits | 86,357 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 171,891 | 1.719 | 18 | 18 | fits | 101,455 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 978,973 | 9.790 | 18 | 18 | fits | 31,767 | 19 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 259,905 | 2.599 | 20 | 20 | fits | 86,357 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 67,838 | 0.678 | 20 | 200 | fits | 69,180 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 338,074 | 3.381 | 20 | 200 | fits | 86,357 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 68,750 | 0.688 | 20 | 20 | fits | 69,180 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 480,040 | 4.800 | 20 | 20 | fits | 72,416 | 50 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 72,335 | 0.723 | 20 | 24 | fits | 69,180 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 927,630 | 9.276 | 20 | 24 | fits | 45,903 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 71,295 | 0.713 | 20 | 50 | fits | 69,180 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 341,750 | 3.417 | 20 | 50 | fits | 86,357 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 172,295 | 1.723 | 18 | 18 | fits | 101,455 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 987,354 | 9.874 | 18 | 18 | fits | 30,466 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 263,870 | 2.639 | 20 | 20 | fits | 95,860 | 99 | 0.682 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 68,242 | 0.682 | 20 | 200 | fits | 69,180 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 342,365 | 3.424 | 20 | 200 | fits | 95,860 | 99 | 0.682 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 69,154 | 0.692 | 20 | 20 | fits | 69,180 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 479,795 | 4.798 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 72,739 | 0.727 | 20 | 24 | fits | 69,180 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 941,679 | 9.417 | 20 | 24 | fits | 45,903 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 71,699 | 0.717 | 20 | 50 | fits | 69,180 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 346,041 | 3.460 | 20 | 50 | fits | 95,860 | 99 | 0.682 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 163,265 | 1.633 | 18 | 18 | fits | 92,021 | 134 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 993,229 | 9.932 | 18 | 18 | fits | 22,292 | 14 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 331,818 | 3.318 | 20 | 20 | fits | 86,274 | 81 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 139,609 | 1.396 | 20 | 200 | fits | 69,945 | 135 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 409,904 | 4.099 | 20 | 200 | fits | 86,274 | 81 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 140,521 | 1.405 | 20 | 20 | fits | 69,945 | 135 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 547,299 | 5.473 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 144,106 | 1.441 | 20 | 24 | fits | 69,945 | 135 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,021,908 | 10.219 | 20 | 24 | fits | 49,666 | 35 | 0.744 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 143,066 | 1.431 | 20 | 50 | fits | 69,945 | 135 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 413,580 | 4.136 | 20 | 50 | fits | 86,274 | 81 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 244,208 | 2.442 | 18 | 18 | fits | 101,597 | 138 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,051,293 | 10.513 | 18 | 18 | fits | 31,920 | 19 | 0.796 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 260,161 | 2.602 | 20 | 20 | fits | 86,357 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 68,062 | 0.681 | 20 | 200 | fits | 69,392 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 338,330 | 3.383 | 20 | 200 | fits | 86,357 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 68,974 | 0.690 | 20 | 20 | fits | 69,392 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 475,725 | 4.757 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 72,559 | 0.726 | 20 | 24 | fits | 69,392 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 941,967 | 9.420 | 20 | 24 | fits | 45,937 | 29 | 0.740 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 71,519 | 0.715 | 20 | 50 | fits | 69,392 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 342,006 | 3.420 | 20 | 50 | fits | 86,357 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 172,551 | 1.726 | 18 | 18 | fits | 101,487 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 993,491 | 9.935 | 18 | 18 | fits | 22,292 | 14 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 260,363 | 2.604 | 20 | 20 | fits | 86,357 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 68,264 | 0.683 | 20 | 200 | fits | 69,392 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 338,532 | 3.385 | 20 | 200 | fits | 86,357 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 69,176 | 0.692 | 20 | 20 | fits | 69,392 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 459,449 | 4.594 | 20 | 20 | fits | 51,367 | 46 | 0.638 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 72,761 | 0.728 | 20 | 24 | fits | 69,392 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 928,011 | 9.280 | 20 | 24 | fits | 45,872 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 71,721 | 0.717 | 20 | 50 | fits | 69,392 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 342,208 | 3.422 | 20 | 50 | fits | 86,357 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 172,753 | 1.728 | 18 | 18 | fits | 101,487 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 987,709 | 9.877 | 18 | 18 | fits | 30,466 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 260,565 | 2.606 | 20 | 20 | fits | 69,423 | 83 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 68,466 | 0.685 | 20 | 200 | fits | 69,392 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 321,800 | 3.218 | 20 | 200 | fits | 69,423 | 83 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 69,378 | 0.694 | 20 | 20 | fits | 69,392 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 461,550 | 4.615 | 20 | 20 | fits | 68,079 | 44 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 72,963 | 0.730 | 20 | 24 | fits | 69,392 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 927,451 | 9.275 | 20 | 24 | fits | 45,903 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 71,923 | 0.719 | 20 | 50 | fits | 69,392 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 325,476 | 3.255 | 20 | 50 | fits | 69,423 | 83 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 172,955 | 1.730 | 18 | 18 | fits | 101,487 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 987,175 | 9.872 | 18 | 18 | fits | 30,466 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 270,040 | 2.700 | 20 | 20 | fits | 86,317 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 68,668 | 0.687 | 20 | 200 | fits | 69,392 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 347,984 | 3.480 | 20 | 200 | fits | 86,317 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 69,580 | 0.696 | 20 | 20 | fits | 69,392 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 485,435 | 4.854 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 73,165 | 0.732 | 20 | 24 | fits | 69,392 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 951,500 | 9.515 | 20 | 24 | fits | 45,903 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 72,125 | 0.721 | 20 | 50 | fits | 69,392 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 351,660 | 3.517 | 20 | 50 | fits | 86,317 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 173,157 | 1.732 | 18 | 18 | fits | 101,487 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 986,865 | 9.869 | 18 | 18 | fits | 37,900 | 30 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 267,828 | 2.678 | 20 | 20 | fits | 86,355 | 81 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 74,074 | 0.741 | 20 | 200 | fits | 74,596 | 146 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 345,995 | 3.460 | 20 | 200 | fits | 86,355 | 81 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 74,986 | 0.750 | 20 | 20 | fits | 74,596 | 146 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 488,009 | 4.880 | 20 | 20 | fits | 67,936 | 44 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 78,571 | 0.786 | 20 | 24 | fits | 74,596 | 146 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 958,616 | 9.586 | 20 | 24 | fits | 46,091 | 29 | 0.743 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 77,531 | 0.775 | 20 | 50 | fits | 74,596 | 146 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 349,671 | 3.497 | 20 | 50 | fits | 86,355 | 81 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 180,207 | 1.802 | 18 | 18 | fits | 103,131 | 143 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 987,848 | 9.878 | 18 | 18 | fits | 31,767 | 19 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 241,387 | 2.414 | 20 | 20 | fits | 89,017 | 87 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 68,238 | 0.682 | 20 | 200 | fits | 69,245 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 319,190 | 3.192 | 20 | 200 | fits | 89,017 | 87 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 69,150 | 0.692 | 20 | 20 | fits | 69,245 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 456,674 | 4.567 | 20 | 20 | fits | 67,903 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 72,735 | 0.727 | 20 | 24 | fits | 69,245 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 927,402 | 9.274 | 20 | 24 | fits | 45,872 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 71,695 | 0.717 | 20 | 50 | fits | 69,245 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 322,866 | 3.229 | 20 | 50 | fits | 89,017 | 87 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 172,805 | 1.728 | 18 | 18 | fits | 101,565 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 987,100 | 9.871 | 18 | 18 | fits | 30,466 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 239,386 | 2.394 | 20 | 20 | fits | 86,842 | 81 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 68,440 | 0.684 | 20 | 200 | fits | 69,245 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 317,582 | 3.176 | 20 | 200 | fits | 86,842 | 81 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 69,352 | 0.694 | 20 | 20 | fits | 69,245 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 455,005 | 4.550 | 20 | 20 | fits | 67,845 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 72,937 | 0.729 | 20 | 24 | fits | 69,245 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 926,903 | 9.269 | 20 | 24 | fits | 45,903 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 71,897 | 0.719 | 20 | 50 | fits | 69,245 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 321,258 | 3.213 | 20 | 50 | fits | 86,842 | 81 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 234,351 | 2.344 | 18 | 18 | fits | 97,218 | 102 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 986,627 | 9.866 | 18 | 18 | fits | 30,466 | 17 | 0.788 |
| an event behind 15 others | `backlog.event.if0` | 85,085 | 0.851 | 20 | 200 | fits | 62,320 | 104 | 0.502 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 327,367 | 3.274 | 20 | 20 | fits | 44,083 | 44 | 0.517 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 74,993 | 0.750 | 20 | 200 | fits | 75,201 | 138 | 0.517 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 269,841 | 2.698 | 20 | 200 | fits | 54,235 | 55 | 0.564 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 70,734 | 0.707 | 20 | 20 | fits | 75,201 | 138 | 0.517 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 354,441 | 3.544 | 20 | 20 | fits | 44,083 | 44 | 0.517 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 74,319 | 0.743 | 20 | 24 | fits | 75,201 | 138 | 0.517 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 593,487 | 5.935 | 20 | 24 | fits | 23,593 | 29 | 0.520 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 73,279 | 0.733 | 20 | 50 | fits | 75,201 | 138 | 0.517 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 268,346 | 2.683 | 20 | 50 | fits | 54,235 | 55 | 0.564 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 268,281 | 2.683 | 18 | 18 | fits | 54,235 | 55 | 0.564 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 621,133 | 6.211 | 18 | 18 | fits | 9,542 | 17 | 0.339 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 254,300 | 2.543 | 20 | 20 | fits | 91,962 | 92 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 62,552 | 0.626 | 20 | 200 | fits | 67,234 | 135 | 0.487 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 338,195 | 3.382 | 20 | 200 | fits | 91,962 | 92 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 63,464 | 0.635 | 20 | 20 | fits | 67,234 | 135 | 0.487 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 478,856 | 4.789 | 20 | 20 | fits | 68,018 | 44 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 67,049 | 0.670 | 20 | 24 | fits | 67,234 | 135 | 0.487 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 944,484 | 9.445 | 20 | 24 | fits | 45,898 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 66,009 | 0.660 | 20 | 50 | fits | 67,234 | 135 | 0.487 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 341,871 | 3.419 | 20 | 50 | fits | 91,962 | 92 | 0.672 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 166,936 | 1.669 | 18 | 18 | fits | 101,382 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 973,737 | 9.737 | 18 | 18 | fits | 31,788 | 19 | 0.794 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 13,025 | 0.130 | 20 | 20 | fits | 21,572 | 20 | 0.763 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 62,552 | 0.626 | 20 | 200 | fits | 67,234 | 135 | 0.487 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 28,186 | 0.282 | 20 | 200 | fits | 21,572 | 20 | 0.763 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 63,464 | 0.635 | 20 | 20 | fits | 67,234 | 135 | 0.487 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 470,081 | 4.701 | 20 | 20 | fits | 68,149 | 44 | 0.690 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 67,049 | 0.670 | 20 | 24 | fits | 67,234 | 135 | 0.487 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 913,538 | 9.135 | 20 | 24 | fits | 45,898 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 66,009 | 0.660 | 20 | 50 | fits | 67,234 | 135 | 0.487 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 326,538 | 3.265 | 20 | 50 | fits | 76,629 | 71 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 166,936 | 1.669 | 18 | 18 | fits | 101,382 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 973,252 | 9.733 | 18 | 18 | fits | 30,461 | 17 | 0.788 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,202,906 | 62.029 | 20 | 20 | MISS ceiling | 28,300 | 25 | 0.610 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,018,715 | 360.187 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,018,640 | 360.186 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,018,565 | 360.186 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,018,490 | 360.185 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 66,797 | 0.668 | 20 | 200 | fits | 65,091 | 129 | 0.492 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 321,802 | 3.218 | 20 | 200 | fits | 75,394 | 67 | 0.671 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 62,538 | 0.625 | 20 | 20 | fits | 65,091 | 129 | 0.492 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 425,501 | 4.255 | 20 | 20 | fits | 48,207 | 29 | 0.773 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 66,123 | 0.661 | 20 | 24 | fits | 65,091 | 129 | 0.492 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,290,426 | 62.904 | 20 | 24 | MISS ceiling | 22,906 | 21 | 0.640 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 65,083 | 0.651 | 20 | 50 | fits | 65,091 | 129 | 0.492 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 320,307 | 3.203 | 20 | 50 | fits | 75,394 | 67 | 0.671 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 164,273 | 1.643 | 18 | 18 | fits | 99,645 | 131 | 0.639 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 790,395 | 7.904 | 18 | 18 | fits | 22,429 | 17 | 0.810 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
