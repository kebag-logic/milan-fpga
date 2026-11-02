### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 313 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.634 (3.966) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-0.adp_available.if0` (backlog-adp@verify-0) | 3.552 (5.260) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.099 (0.352) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.929 (1.515) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.140 (62.399) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.221 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 1.464 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.acmp.last.if0` (backlog-adp@verify-0) | 5.924 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 1.454 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.adp.last.if0` (backlog-adp@verify-0) | 4.421 | fits | 7 adp | 28 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 1.499 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 63.005 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 1.489 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 4.458 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.918 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.srp.last.if0` (backlog-adp@blank-0) | 11.140 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.204 | 18 | 110,323 (1.103) | yes | - |
| backlog-adp@blank-1 | 0 | 11.538 | 17 | 110,377 (1.104) | yes | - |
| backlog-adp@blank-2 | 0 | 11.626 | 18 | 110,303 (1.103) | yes | - |
| backlog-adp@blank-3 | 0 | 11.557 | 17 | 110,503 (1.105) | yes | - |
| backlog-adp@blank-4 | 0 | 11.565 | 17 | 110,377 (1.104) | yes | - |
| backlog-adp@blank-5 | 0 | 11.619 | 17 | 110,303 (1.103) | yes | - |
| backlog-adp@blank-6 | 0 | 11.541 | 18 | 110,377 (1.104) | yes | - |
| backlog-adp@blank-7 | 0 | 13.367 | 20 | 120,900 (1.209) | yes | - |
| backlog-adp@program-0 | 0 | 11.602 | 17 | 110,349 (1.103) | yes | - |
| backlog-adp@program-1 | 0 | 11.703 | 18 | 110,138 (1.101) | yes | - |
| backlog-adp@program-2 | 0 | 11.618 | 17 | 110,349 (1.103) | yes | - |
| backlog-adp@program-3 | 0 | 11.920 | 19 | 101,256 (1.013) | yes | - |
| backlog-adp@program-4 | 0 | 10.776 | 17 | 110,250 (1.103) | yes | - |
| backlog-adp@program-5 | 0 | 10.786 | 17 | 110,302 (1.103) | yes | - |
| backlog-adp@program-6 | 0 | 10.879 | 18 | 110,302 (1.103) | yes | - |
| backlog-adp@program-7 | 0 | 10.930 | 18 | 101,209 (1.012) | yes | - |
| backlog-adp@verify-0 | 0 | 12.202 | 17 | 110,290 (1.103) | yes | - |
| backlog-adp@verify-1 | 0 | 11.538 | 17 | 110,344 (1.103) | yes | - |
| backlog-adp@verify-2 | 0 | 11.627 | 18 | 110,344 (1.103) | yes | - |
| backlog-adp@verify-3 | 0 | 11.698 | 18 | 110,344 (1.103) | yes | - |
| backlog-adp@verify-4 | 0 | 11.648 | 18 | 110,344 (1.103) | yes | - |
| backlog-adp@verify-5 | 0 | 11.625 | 18 | 110,344 (1.103) | yes | - |
| backlog-adp@verify-6 | 0 | 11.557 | 17 | 110,194 (1.102) | yes | - |
| backlog-adp@verify-7 | 0 | 12.516 | 18 | 112,604 (1.126) | yes | - |
| backlog | 0 | 6.852 | 19 | 83,408 (0.834) | yes | - |
| backlog-adp | 0 | 10.792 | 18 | 110,192 (1.102) | yes | - |
| backlog-adp-refill | 0 | 40.649 | 24 | 110,192 (1.102) | yes | - |
| backlog-owed | 0 | 360.271 | 65 | 107,232 (1.072) | yes | - |

Composed maximum over the 4 backlog windows: 110,192 CPU cycles (1.102 ms), backlog-adp.
Over the windows that released their whole load only: 110,192 (1.102 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 331 | 0 | 110,323 (1.103) | fits |
| backlog-adp@blank-1 | 330 | 0 | 110,377 (1.104) | fits |
| backlog-adp@blank-2 | 331 | 0 | 110,303 (1.103) | fits |
| backlog-adp@blank-3 | 331 | 0 | 110,503 (1.105) | fits |
| backlog-adp@blank-4 | 331 | 0 | 110,377 (1.104) | fits |
| backlog-adp@blank-5 | 331 | 0 | 110,303 (1.103) | fits |
| backlog-adp@blank-6 | 331 | 0 | 110,377 (1.104) | fits |
| backlog-adp@blank-7 | 333 | 0 | 120,900 (1.209) | fits |
| backlog-adp@program-0 | 360 | 0 | 119,486 (1.195) | fits |
| backlog-adp@program-1 | 362 | 0 | 119,486 (1.195) | fits |
| backlog-adp@program-2 | 361 | 0 | 119,486 (1.195) | fits |
| backlog-adp@program-3 | 362 | 0 | 119,486 (1.195) | fits |
| backlog-adp@program-4 | 361 | 0 | 119,486 (1.195) | fits |
| backlog-adp@program-5 | 361 | 0 | 119,486 (1.195) | fits |
| backlog-adp@program-6 | 362 | 0 | 119,486 (1.195) | fits |
| backlog-adp@program-7 | 362 | 0 | 119,486 (1.195) | fits |
| backlog-adp@verify-0 | 387 | 0 | 119,486 (1.195) | fits |
| backlog-adp@verify-1 | 387 | 0 | 119,486 (1.195) | fits |
| backlog-adp@verify-2 | 388 | 0 | 119,486 (1.195) | fits |
| backlog-adp@verify-3 | 388 | 0 | 119,486 (1.195) | fits |
| backlog-adp@verify-4 | 388 | 0 | 119,486 (1.195) | fits |
| backlog-adp@verify-5 | 388 | 0 | 119,486 (1.195) | fits |
| backlog-adp@verify-6 | 388 | 0 | 119,486 (1.195) | fits |
| backlog-adp@verify-7 | 389 | 0 | 119,486 (1.195) | fits |
| save | 602 | 0 | 119,162 (1.192) | fits |
| backlog | 293 | 0 | 83,408 (0.834) | fits |
| backlog-adp | 301 | 0 | 110,192 (1.102) | fits |
| backlog-adp-refill | 307 | 0 | 110,192 (1.102) | fits |
| backlog-owed | 350 | 0 | 107,232 (1.072) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 347,665 | 3.477 | 20 | 20 | fits | 95,116 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 137,733 | 1.377 | 20 | 200 | fits | 78,383 | 135 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 434,615 | 4.346 | 20 | 200 | fits | 95,116 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 138,645 | 1.386 | 20 | 20 | fits | 78,383 | 135 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 584,876 | 5.849 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 142,230 | 1.422 | 20 | 24 | fits | 78,383 | 135 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,084,656 | 10.847 | 20 | 24 | fits | 47,117 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 141,190 | 1.412 | 20 | 50 | fits | 78,383 | 135 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 438,291 | 4.383 | 20 | 50 | fits | 95,116 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 251,058 | 2.511 | 18 | 18 | fits | 110,323 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,113,995 | 11.140 | 18 | 18 | fits | 31,874 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 289,390 | 2.894 | 20 | 20 | fits | 95,116 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 79,354 | 0.794 | 20 | 200 | fits | 77,454 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 376,340 | 3.763 | 20 | 200 | fits | 95,116 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 80,266 | 0.803 | 20 | 20 | fits | 77,454 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 526,601 | 5.266 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 83,851 | 0.839 | 20 | 24 | fits | 77,454 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 1,049,429 | 10.494 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 82,811 | 0.828 | 20 | 50 | fits | 77,454 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 380,016 | 3.800 | 20 | 50 | fits | 95,116 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 192,733 | 1.927 | 18 | 18 | fits | 110,377 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,046,894 | 10.469 | 18 | 18 | fits | 46,976 | 29 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 289,656 | 2.897 | 20 | 20 | fits | 95,116 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 79,694 | 0.797 | 20 | 200 | fits | 77,454 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 376,606 | 3.766 | 20 | 200 | fits | 95,116 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 80,606 | 0.806 | 20 | 20 | fits | 77,454 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 526,867 | 5.269 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 84,191 | 0.842 | 20 | 24 | fits | 77,454 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 1,026,847 | 10.268 | 20 | 24 | fits | 47,011 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 83,151 | 0.832 | 20 | 50 | fits | 77,454 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 380,282 | 3.803 | 20 | 50 | fits | 95,116 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 192,999 | 1.930 | 18 | 18 | fits | 110,303 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,056,186 | 10.562 | 18 | 18 | fits | 31,874 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 314,662 | 3.147 | 20 | 20 | fits | 88,040 | 58 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 110,214 | 1.102 | 20 | 200 | fits | 77,791 | 137 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 394,536 | 3.945 | 20 | 200 | fits | 88,040 | 58 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 111,126 | 1.111 | 20 | 20 | fits | 77,791 | 137 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 543,846 | 5.438 | 20 | 20 | fits | 63,449 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 36,920 | 0.369 | 20 | 24 | fits | 38,108 | 63 | 0.589 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 1,019,919 | 10.199 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 35,880 | 0.359 | 20 | 50 | fits | 38,108 | 63 | 0.589 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 310,172 | 3.102 | 20 | 50 | fits | 86,388 | 74 | 0.636 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 223,719 | 2.237 | 18 | 18 | fits | 110,503 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,049,223 | 10.492 | 18 | 18 | fits | 31,839 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 282,145 | 2.821 | 20 | 20 | fits | 95,116 | 81 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 72,109 | 0.721 | 20 | 200 | fits | 77,454 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 369,095 | 3.691 | 20 | 200 | fits | 95,116 | 81 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 73,021 | 0.730 | 20 | 20 | fits | 77,454 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 497,043 | 4.970 | 20 | 20 | fits | 41,035 | 24 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 76,606 | 0.766 | 20 | 24 | fits | 77,454 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 1,020,791 | 10.208 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 75,566 | 0.756 | 20 | 50 | fits | 77,454 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 372,771 | 3.728 | 20 | 50 | fits | 95,116 | 81 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 185,488 | 1.855 | 18 | 18 | fits | 110,377 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,050,095 | 10.501 | 18 | 18 | fits | 31,839 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 282,411 | 2.824 | 20 | 20 | fits | 87,058 | 77 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 72,449 | 0.724 | 20 | 200 | fits | 77,454 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 361,303 | 3.613 | 20 | 200 | fits | 87,058 | 77 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 73,361 | 0.734 | 20 | 20 | fits | 77,454 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 515,387 | 5.154 | 20 | 20 | fits | 63,470 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 76,946 | 0.769 | 20 | 24 | fits | 77,454 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 1,034,166 | 10.342 | 20 | 24 | fits | 46,965 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 75,906 | 0.759 | 20 | 50 | fits | 77,454 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 364,979 | 3.650 | 20 | 50 | fits | 87,058 | 77 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 185,754 | 1.858 | 18 | 18 | fits | 110,303 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,055,537 | 10.555 | 18 | 18 | fits | 23,906 | 16 | 0.819 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 263,073 | 2.631 | 20 | 20 | fits | 98,115 | 87 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 72,789 | 0.728 | 20 | 200 | fits | 77,454 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 349,640 | 3.496 | 20 | 200 | fits | 98,115 | 87 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 73,701 | 0.737 | 20 | 20 | fits | 77,454 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 499,801 | 4.998 | 20 | 20 | fits | 63,363 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 77,286 | 0.773 | 20 | 24 | fits | 77,454 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 1,018,443 | 10.184 | 20 | 24 | fits | 46,968 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 76,246 | 0.762 | 20 | 50 | fits | 77,454 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 353,316 | 3.533 | 20 | 50 | fits | 98,115 | 87 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 186,168 | 1.862 | 18 | 18 | fits | 110,377 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,047,808 | 10.478 | 18 | 18 | fits | 31,900 | 19 | 0.782 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 262,185 | 2.622 | 20 | 20 | fits | 95,355 | 81 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 73,129 | 0.731 | 20 | 200 | fits | 77,454 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 349,127 | 3.491 | 20 | 200 | fits | 95,355 | 81 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 74,041 | 0.740 | 20 | 20 | fits | 77,454 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 499,383 | 4.994 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 77,626 | 0.776 | 20 | 24 | fits | 77,454 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 1,018,049 | 10.180 | 20 | 24 | fits | 46,968 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 76,586 | 0.766 | 20 | 50 | fits | 77,454 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 352,803 | 3.528 | 20 | 50 | fits | 95,355 | 81 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 257,383 | 2.574 | 18 | 18 | fits | 105,993 | 102 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,047,345 | 10.473 | 18 | 18 | fits | 31,831 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 290,100 | 2.901 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 80,295 | 0.803 | 20 | 200 | fits | 78,121 | 135 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 376,978 | 3.770 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 81,207 | 0.812 | 20 | 20 | fits | 78,121 | 135 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 527,239 | 5.272 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 84,792 | 0.848 | 20 | 24 | fits | 78,121 | 135 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 1,050,147 | 10.501 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 83,752 | 0.838 | 20 | 50 | fits | 78,121 | 135 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 380,654 | 3.807 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 193,646 | 1.936 | 18 | 18 | fits | 110,349 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,047,612 | 10.476 | 18 | 18 | fits | 46,976 | 29 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 315,582 | 3.156 | 20 | 20 | fits | 87,968 | 58 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 111,491 | 1.115 | 20 | 200 | fits | 78,482 | 137 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 395,384 | 3.954 | 20 | 200 | fits | 87,968 | 58 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 112,403 | 1.124 | 20 | 20 | fits | 78,482 | 137 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 544,694 | 5.447 | 20 | 20 | fits | 63,449 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 37,506 | 0.375 | 20 | 24 | fits | 38,420 | 63 | 0.595 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 998,093 | 9.981 | 20 | 24 | fits | 47,011 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 36,466 | 0.365 | 20 | 50 | fits | 38,420 | 63 | 0.595 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 311,092 | 3.111 | 20 | 50 | fits | 86,396 | 74 | 0.636 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 224,631 | 2.246 | 18 | 18 | fits | 110,138 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,058,225 | 10.582 | 18 | 18 | fits | 30,793 | 17 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 283,195 | 2.832 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 73,390 | 0.734 | 20 | 200 | fits | 78,121 | 135 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 370,073 | 3.701 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 74,302 | 0.743 | 20 | 20 | fits | 78,121 | 135 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 501,141 | 5.011 | 20 | 20 | fits | 66,883 | 39 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 77,887 | 0.779 | 20 | 24 | fits | 78,121 | 135 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 1,020,490 | 10.205 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 76,847 | 0.768 | 20 | 50 | fits | 78,121 | 135 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 373,749 | 3.737 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 186,741 | 1.867 | 18 | 18 | fits | 110,349 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,049,794 | 10.498 | 18 | 18 | fits | 31,839 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 278,913 | 2.789 | 20 | 20 | fits | 94,988 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 74,070 | 0.741 | 20 | 200 | fits | 78,121 | 135 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 365,712 | 3.657 | 20 | 200 | fits | 94,988 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 74,982 | 0.750 | 20 | 20 | fits | 78,121 | 135 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 515,374 | 5.154 | 20 | 20 | fits | 63,175 | 33 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 78,567 | 0.786 | 20 | 24 | fits | 78,121 | 135 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 1,034,099 | 10.341 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 77,527 | 0.775 | 20 | 50 | fits | 78,121 | 135 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 369,388 | 3.694 | 20 | 50 | fits | 94,988 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 178,328 | 1.783 | 18 | 18 | fits | 101,256 | 134 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,055,486 | 10.555 | 18 | 18 | fits | 23,922 | 16 | 0.819 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 284,091 | 2.841 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 74,230 | 0.742 | 20 | 200 | fits | 78,596 | 135 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 370,969 | 3.710 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 75,142 | 0.751 | 20 | 20 | fits | 78,596 | 135 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 521,230 | 5.212 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 78,727 | 0.787 | 20 | 24 | fits | 78,596 | 135 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 1,044,138 | 10.441 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 77,687 | 0.777 | 20 | 50 | fits | 78,596 | 135 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 374,645 | 3.746 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 187,482 | 1.875 | 18 | 18 | fits | 110,250 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,041,603 | 10.416 | 18 | 18 | fits | 46,976 | 29 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 285,034 | 2.850 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 75,071 | 0.751 | 20 | 200 | fits | 78,038 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 371,912 | 3.719 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 75,983 | 0.760 | 20 | 20 | fits | 78,038 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 522,173 | 5.222 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 79,568 | 0.796 | 20 | 24 | fits | 78,038 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 1,045,001 | 10.450 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 78,528 | 0.785 | 20 | 50 | fits | 78,038 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 375,588 | 3.756 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 188,375 | 1.884 | 18 | 18 | fits | 110,302 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,042,466 | 10.425 | 18 | 18 | fits | 46,976 | 29 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 285,714 | 2.857 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 75,751 | 0.758 | 20 | 200 | fits | 78,038 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 372,592 | 3.726 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 76,663 | 0.767 | 20 | 20 | fits | 78,038 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 503,660 | 5.037 | 20 | 20 | fits | 66,883 | 39 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 80,248 | 0.802 | 20 | 24 | fits | 78,038 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 1,023,009 | 10.230 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 79,208 | 0.792 | 20 | 50 | fits | 78,038 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 376,268 | 3.763 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 189,055 | 1.891 | 18 | 18 | fits | 110,302 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,052,313 | 10.523 | 18 | 18 | fits | 31,839 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 281,282 | 2.813 | 20 | 20 | fits | 94,865 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 76,431 | 0.764 | 20 | 200 | fits | 78,038 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 367,958 | 3.680 | 20 | 200 | fits | 94,865 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 77,343 | 0.773 | 20 | 20 | fits | 78,038 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 517,506 | 5.175 | 20 | 20 | fits | 63,145 | 33 | 0.711 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 80,928 | 0.809 | 20 | 24 | fits | 78,038 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 1,036,231 | 10.362 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 79,888 | 0.799 | 20 | 50 | fits | 78,038 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 371,634 | 3.716 | 20 | 50 | fits | 94,865 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 180,642 | 1.806 | 18 | 18 | fits | 101,209 | 134 | 0.613 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,057,618 | 10.576 | 18 | 18 | fits | 23,922 | 16 | 0.819 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 355,218 | 3.552 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 145,449 | 1.454 | 20 | 200 | fits | 78,929 | 135 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 442,096 | 4.421 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 146,361 | 1.464 | 20 | 20 | fits | 78,929 | 135 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 592,357 | 5.924 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 149,946 | 1.499 | 20 | 24 | fits | 78,929 | 135 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,115,265 | 11.153 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 148,906 | 1.489 | 20 | 50 | fits | 78,929 | 135 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 445,772 | 4.458 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 258,741 | 2.587 | 18 | 18 | fits | 110,290 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,112,730 | 11.127 | 18 | 18 | fits | 46,976 | 29 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 288,873 | 2.889 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 79,000 | 0.790 | 20 | 200 | fits | 78,120 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 375,751 | 3.758 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 79,912 | 0.799 | 20 | 20 | fits | 78,120 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 526,012 | 5.260 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 83,497 | 0.835 | 20 | 24 | fits | 78,120 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 1,048,840 | 10.488 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 82,457 | 0.825 | 20 | 50 | fits | 78,120 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 379,427 | 3.794 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 192,346 | 1.923 | 18 | 18 | fits | 110,344 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,046,305 | 10.463 | 18 | 18 | fits | 46,976 | 29 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 289,213 | 2.892 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 79,340 | 0.793 | 20 | 200 | fits | 78,120 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 376,091 | 3.761 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 80,252 | 0.803 | 20 | 20 | fits | 78,120 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 526,352 | 5.264 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 83,837 | 0.838 | 20 | 24 | fits | 78,120 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 1,026,332 | 10.263 | 20 | 24 | fits | 47,011 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 82,797 | 0.828 | 20 | 50 | fits | 78,120 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 379,767 | 3.798 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 192,686 | 1.927 | 18 | 18 | fits | 110,344 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,055,671 | 10.557 | 18 | 18 | fits | 31,874 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 289,553 | 2.896 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 79,680 | 0.797 | 20 | 200 | fits | 78,120 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 376,431 | 3.764 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 80,592 | 0.806 | 20 | 20 | fits | 78,120 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 526,692 | 5.267 | 20 | 20 | fits | 63,348 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 84,177 | 0.842 | 20 | 24 | fits | 78,120 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 1,041,392 | 10.414 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 83,137 | 0.831 | 20 | 50 | fits | 78,120 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 380,107 | 3.801 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 193,026 | 1.930 | 18 | 18 | fits | 110,344 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,062,779 | 10.628 | 18 | 18 | fits | 23,922 | 16 | 0.819 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 289,893 | 2.899 | 20 | 20 | fits | 95,044 | 81 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 80,020 | 0.800 | 20 | 200 | fits | 78,120 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 376,771 | 3.768 | 20 | 200 | fits | 95,044 | 81 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 80,932 | 0.809 | 20 | 20 | fits | 78,120 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 504,719 | 5.047 | 20 | 20 | fits | 41,035 | 24 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 84,517 | 0.845 | 20 | 24 | fits | 78,120 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 1,028,467 | 10.285 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 83,477 | 0.835 | 20 | 50 | fits | 78,120 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 380,447 | 3.804 | 20 | 50 | fits | 95,044 | 81 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 193,366 | 1.934 | 18 | 18 | fits | 110,344 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,057,771 | 10.578 | 18 | 18 | fits | 31,839 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 290,142 | 2.901 | 20 | 20 | fits | 71,834 | 72 | 0.601 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 80,269 | 0.803 | 20 | 200 | fits | 78,120 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 353,810 | 3.538 | 20 | 200 | fits | 71,834 | 72 | 0.601 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 81,181 | 0.812 | 20 | 20 | fits | 78,120 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 507,455 | 5.075 | 20 | 20 | fits | 63,414 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 84,766 | 0.848 | 20 | 24 | fits | 78,120 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 1,026,180 | 10.262 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 83,726 | 0.837 | 20 | 50 | fits | 78,120 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 357,486 | 3.575 | 20 | 50 | fits | 71,834 | 72 | 0.601 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 193,615 | 1.936 | 18 | 18 | fits | 110,344 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,055,553 | 10.556 | 18 | 18 | fits | 31,908 | 19 | 0.782 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 318,882 | 3.189 | 20 | 20 | fits | 87,762 | 58 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 110,931 | 1.109 | 20 | 200 | fits | 78,356 | 137 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 398,568 | 3.986 | 20 | 200 | fits | 87,762 | 58 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 111,843 | 1.118 | 20 | 20 | fits | 78,356 | 137 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 547,359 | 5.474 | 20 | 20 | fits | 63,276 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 37,072 | 0.371 | 20 | 24 | fits | 38,351 | 63 | 0.593 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 1,019,418 | 10.194 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 36,032 | 0.360 | 20 | 50 | fits | 38,351 | 63 | 0.593 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 314,482 | 3.145 | 20 | 50 | fits | 90,290 | 80 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 224,127 | 2.241 | 18 | 18 | fits | 110,194 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,048,722 | 10.487 | 18 | 18 | fits | 31,839 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 317,865 | 3.179 | 20 | 20 | fits | 87,968 | 58 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 111,308 | 1.113 | 20 | 200 | fits | 78,393 | 137 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 397,667 | 3.977 | 20 | 200 | fits | 87,968 | 58 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 112,220 | 1.122 | 20 | 20 | fits | 78,393 | 137 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 546,977 | 5.470 | 20 | 20 | fits | 63,449 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 37,412 | 0.374 | 20 | 24 | fits | 38,351 | 63 | 0.593 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 1,019,036 | 10.190 | 20 | 24 | fits | 46,976 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 36,372 | 0.364 | 20 | 50 | fits | 38,351 | 63 | 0.593 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 313,375 | 3.134 | 20 | 50 | fits | 86,396 | 74 | 0.636 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 226,914 | 2.269 | 18 | 18 | fits | 112,604 | 143 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,048,340 | 10.483 | 18 | 18 | fits | 31,839 | 19 | 0.781 |
| an event behind 15 others | `backlog.event.if0` | 92,921 | 0.929 | 20 | 200 | fits | 68,533 | 104 | 0.525 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 363,414 | 3.634 | 20 | 20 | fits | 50,875 | 44 | 0.543 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 82,795 | 0.828 | 20 | 200 | fits | 83,003 | 138 | 0.524 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 293,320 | 2.933 | 20 | 200 | fits | 59,193 | 55 | 0.555 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 78,536 | 0.785 | 20 | 20 | fits | 83,003 | 138 | 0.524 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 391,304 | 3.913 | 20 | 20 | fits | 50,875 | 44 | 0.543 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 82,121 | 0.821 | 20 | 24 | fits | 83,003 | 138 | 0.524 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 629,026 | 6.290 | 20 | 24 | fits | 23,568 | 29 | 0.525 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 81,081 | 0.811 | 20 | 50 | fits | 83,003 | 138 | 0.524 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 291,825 | 2.918 | 20 | 50 | fits | 59,193 | 55 | 0.555 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 291,760 | 2.918 | 18 | 18 | fits | 59,193 | 55 | 0.555 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 656,815 | 6.568 | 18 | 18 | fits | 9,666 | 17 | 0.391 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 281,371 | 2.814 | 20 | 20 | fits | 94,726 | 81 | 0.648 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 71,767 | 0.718 | 20 | 200 | fits | 76,449 | 135 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 367,989 | 3.680 | 20 | 200 | fits | 94,726 | 81 | 0.648 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 72,679 | 0.727 | 20 | 20 | fits | 76,449 | 135 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 517,728 | 5.177 | 20 | 20 | fits | 63,173 | 33 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 76,264 | 0.763 | 20 | 24 | fits | 76,449 | 135 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,017,452 | 10.175 | 20 | 24 | fits | 47,009 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 75,224 | 0.752 | 20 | 50 | fits | 76,449 | 135 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 371,665 | 3.717 | 20 | 50 | fits | 94,726 | 81 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 184,961 | 1.850 | 18 | 18 | fits | 110,192 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,046,789 | 10.468 | 18 | 18 | fits | 31,872 | 19 | 0.781 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 9,884 | 0.099 | 20 | 20 | fits | 21,144 | 20 | 0.768 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 71,767 | 0.718 | 20 | 200 | fits | 76,449 | 135 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 24,920 | 0.249 | 20 | 200 | fits | 21,144 | 20 | 0.768 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 72,679 | 0.727 | 20 | 20 | fits | 76,449 | 135 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 510,957 | 5.110 | 20 | 20 | fits | 75,460 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 76,264 | 0.763 | 20 | 24 | fits | 76,449 | 135 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 978,745 | 9.787 | 20 | 24 | fits | 47,032 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 75,224 | 0.752 | 20 | 50 | fits | 76,449 | 135 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 361,816 | 3.618 | 20 | 50 | fits | 84,877 | 71 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 184,961 | 1.850 | 18 | 18 | fits | 110,192 | 138 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,032,417 | 10.324 | 18 | 18 | fits | 24,337 | 18 | 0.749 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,214,019 | 62.140 | 20 | 20 | MISS ceiling | 29,517 | 25 | 0.650 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,022,062 | 360.221 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,021,987 | 360.220 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,021,912 | 360.219 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,021,837 | 360.218 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 80,562 | 0.806 | 20 | 200 | fits | 73,517 | 129 | 0.500 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 359,635 | 3.596 | 20 | 200 | fits | 83,263 | 67 | 0.666 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 76,303 | 0.763 | 20 | 20 | fits | 73,517 | 129 | 0.500 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 471,750 | 4.718 | 20 | 20 | fits | 62,785 | 39 | 0.771 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 79,888 | 0.799 | 20 | 24 | fits | 73,517 | 129 | 0.500 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,300,508 | 63.005 | 20 | 24 | MISS ceiling | 22,245 | 21 | 0.621 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 78,848 | 0.788 | 20 | 50 | fits | 73,517 | 129 | 0.500 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 358,140 | 3.581 | 20 | 50 | fits | 83,263 | 67 | 0.666 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 185,625 | 1.856 | 18 | 18 | fits | 107,232 | 131 | 0.637 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 842,785 | 8.428 | 18 | 18 | fits | 23,582 | 17 | 0.812 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
