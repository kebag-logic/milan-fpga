### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 313 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.279 (3.604) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 3.259 (4.849) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.061 (0.196) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.875 (1.394) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.021 (62.265) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.232 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.369 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 5.326 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.359 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.023 | fits | 7 adp | 28 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.404 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.865 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.394 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.059 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.697 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.srp.last.if0` (backlog-adp@blank-0) | 10.311 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.372 | 17 | 101,657 (1.017) | yes | - |
| backlog-adp@blank-1 | 0 | 10.804 | 18 | 101,366 (1.014) | yes | - |
| backlog-adp@blank-2 | 0 | 10.694 | 17 | 101,366 (1.014) | yes | - |
| backlog-adp@blank-3 | 0 | 10.712 | 17 | 101,366 (1.014) | yes | - |
| backlog-adp@blank-4 | 0 | 10.790 | 18 | 101,366 (1.014) | yes | - |
| backlog-adp@blank-5 | 0 | 10.727 | 18 | 101,519 (1.015) | yes | - |
| backlog-adp@blank-6 | 0 | 10.810 | 18 | 101,519 (1.015) | yes | - |
| backlog-adp@blank-7 | 0 | 10.749 | 18 | 95,807 (0.958) | yes | - |
| backlog-adp@program-0 | 0 | 10.784 | 17 | 101,620 (1.016) | yes | - |
| backlog-adp@program-1 | 0 | 10.804 | 18 | 101,510 (1.015) | yes | - |
| backlog-adp@program-2 | 0 | 10.766 | 17 | 101,510 (1.015) | yes | - |
| backlog-adp@program-3 | 0 | 10.724 | 17 | 101,620 (1.016) | yes | - |
| backlog-adp@program-4 | 0 | 9.967 | 16 | 101,466 (1.015) | yes | - |
| backlog-adp@program-5 | 0 | 9.996 | 17 | 101,317 (1.013) | yes | - |
| backlog-adp@program-6 | 0 | 9.942 | 17 | 101,523 (1.015) | yes | - |
| backlog-adp@program-7 | 0 | 10.103 | 18 | 92,316 (0.923) | yes | - |
| backlog-adp@verify-0 | 0 | 11.351 | 17 | 101,614 (1.016) | yes | - |
| backlog-adp@verify-1 | 0 | 10.861 | 18 | 101,566 (1.016) | yes | - |
| backlog-adp@verify-2 | 0 | 10.671 | 17 | 101,354 (1.014) | yes | - |
| backlog-adp@verify-3 | 0 | 10.690 | 17 | 101,354 (1.014) | yes | - |
| backlog-adp@verify-4 | 0 | 10.701 | 17 | 101,354 (1.014) | yes | - |
| backlog-adp@verify-5 | 0 | 10.781 | 18 | 101,354 (1.014) | yes | - |
| backlog-adp@verify-6 | 0 | 10.788 | 17 | 101,566 (1.016) | yes | - |
| backlog-adp@verify-7 | 0 | 10.730 | 18 | 96,016 (0.960) | yes | - |
| backlog | 0 | 6.390 | 19 | 79,342 (0.793) | yes | - |
| backlog-adp | 0 | 9.894 | 17 | 101,362 (1.014) | yes | - |
| backlog-adp-refill | 0 | 40.560 | 24 | 101,362 (1.014) | yes | - |
| backlog-owed | 0 | 360.283 | 65 | 100,152 (1.002) | yes | - |

Composed maximum over the 4 backlog windows: 101,362 CPU cycles (1.014 ms), backlog-adp.
Over the windows that released their whole load only: 101,362 (1.014 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 330 | 0 | 101,657 (1.017) | fits |
| backlog-adp@blank-1 | 331 | 0 | 101,366 (1.014) | fits |
| backlog-adp@blank-2 | 330 | 0 | 101,366 (1.014) | fits |
| backlog-adp@blank-3 | 330 | 0 | 101,366 (1.014) | fits |
| backlog-adp@blank-4 | 331 | 0 | 101,366 (1.014) | fits |
| backlog-adp@blank-5 | 331 | 0 | 101,519 (1.015) | fits |
| backlog-adp@blank-6 | 331 | 0 | 101,519 (1.015) | fits |
| backlog-adp@blank-7 | 331 | 0 | 95,807 (0.958) | fits |
| backlog-adp@program-0 | 360 | 0 | 116,371 (1.164) | fits |
| backlog-adp@program-1 | 361 | 0 | 116,371 (1.164) | fits |
| backlog-adp@program-2 | 360 | 0 | 116,371 (1.164) | fits |
| backlog-adp@program-3 | 360 | 0 | 116,371 (1.164) | fits |
| backlog-adp@program-4 | 361 | 0 | 116,371 (1.164) | fits |
| backlog-adp@program-5 | 361 | 0 | 116,371 (1.164) | fits |
| backlog-adp@program-6 | 361 | 0 | 116,371 (1.164) | fits |
| backlog-adp@program-7 | 362 | 0 | 116,371 (1.164) | fits |
| backlog-adp@verify-0 | 387 | 0 | 116,371 (1.164) | fits |
| backlog-adp@verify-1 | 388 | 0 | 116,371 (1.164) | fits |
| backlog-adp@verify-2 | 387 | 0 | 116,371 (1.164) | fits |
| backlog-adp@verify-3 | 387 | 0 | 116,371 (1.164) | fits |
| backlog-adp@verify-4 | 387 | 0 | 116,371 (1.164) | fits |
| backlog-adp@verify-5 | 388 | 0 | 116,371 (1.164) | fits |
| backlog-adp@verify-6 | 388 | 0 | 116,371 (1.164) | fits |
| backlog-adp@verify-7 | 388 | 0 | 116,371 (1.164) | fits |
| save | 602 | 0 | 116,384 (1.164) | fits |
| backlog | 293 | 0 | 79,342 (0.793) | fits |
| backlog-adp | 300 | 0 | 101,362 (1.014) | fits |
| backlog-adp-refill | 307 | 0 | 101,362 (1.014) | fits |
| backlog-owed | 350 | 0 | 100,152 (1.002) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 325,874 | 3.259 | 20 | 20 | fits | 84,354 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 135,949 | 1.359 | 20 | 200 | fits | 70,136 | 135 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 402,271 | 4.023 | 20 | 200 | fits | 84,354 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 136,861 | 1.369 | 20 | 20 | fits | 70,136 | 135 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 532,571 | 5.326 | 20 | 20 | fits | 54,278 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 140,446 | 1.404 | 20 | 24 | fits | 70,136 | 135 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,033,655 | 10.337 | 20 | 24 | fits | 49,452 | 35 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 139,406 | 1.394 | 20 | 50 | fits | 70,136 | 135 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 405,947 | 4.059 | 20 | 50 | fits | 84,354 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 240,608 | 2.406 | 18 | 18 | fits | 101,657 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,031,120 | 10.311 | 18 | 18 | fits | 49,452 | 35 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 256,212 | 2.562 | 20 | 20 | fits | 84,354 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 66,538 | 0.665 | 20 | 200 | fits | 69,760 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 332,609 | 3.326 | 20 | 200 | fits | 84,354 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 67,450 | 0.674 | 20 | 20 | fits | 69,760 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 462,909 | 4.629 | 20 | 20 | fits | 54,278 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 71,035 | 0.710 | 20 | 24 | fits | 69,760 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 955,807 | 9.558 | 20 | 24 | fits | 44,829 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 69,995 | 0.700 | 20 | 50 | fits | 69,760 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 336,285 | 3.363 | 20 | 50 | fits | 84,354 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 170,906 | 1.709 | 18 | 18 | fits | 101,366 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 975,400 | 9.754 | 18 | 18 | fits | 22,128 | 16 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 257,980 | 2.580 | 20 | 20 | fits | 84,354 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 68,306 | 0.683 | 20 | 200 | fits | 69,760 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 334,377 | 3.344 | 20 | 200 | fits | 84,354 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 69,218 | 0.692 | 20 | 20 | fits | 69,760 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 464,677 | 4.647 | 20 | 20 | fits | 54,278 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 72,803 | 0.728 | 20 | 24 | fits | 69,760 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 966,033 | 9.660 | 20 | 24 | fits | 44,686 | 29 | 0.736 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 71,763 | 0.718 | 20 | 50 | fits | 69,760 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 338,053 | 3.381 | 20 | 50 | fits | 84,354 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 172,674 | 1.727 | 18 | 18 | fits | 101,366 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 963,498 | 9.635 | 18 | 18 | fits | 44,686 | 29 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 259,748 | 2.597 | 20 | 20 | fits | 84,354 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 70,074 | 0.701 | 20 | 200 | fits | 69,760 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 336,145 | 3.361 | 20 | 200 | fits | 84,354 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 70,986 | 0.710 | 20 | 20 | fits | 69,760 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 466,445 | 4.664 | 20 | 20 | fits | 54,278 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 74,571 | 0.746 | 20 | 24 | fits | 69,760 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 967,864 | 9.679 | 20 | 24 | fits | 44,686 | 29 | 0.736 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 73,531 | 0.735 | 20 | 50 | fits | 69,760 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 339,821 | 3.398 | 20 | 50 | fits | 84,354 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 174,442 | 1.744 | 18 | 18 | fits | 101,366 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 965,329 | 9.653 | 18 | 18 | fits | 44,686 | 29 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 261,425 | 2.614 | 20 | 20 | fits | 84,354 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 71,751 | 0.718 | 20 | 200 | fits | 69,760 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 337,822 | 3.378 | 20 | 200 | fits | 84,354 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 72,663 | 0.727 | 20 | 20 | fits | 69,760 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 468,122 | 4.681 | 20 | 20 | fits | 54,278 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 76,248 | 0.762 | 20 | 24 | fits | 69,760 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 946,189 | 9.462 | 20 | 24 | fits | 44,598 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 75,208 | 0.752 | 20 | 50 | fits | 69,760 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 341,498 | 3.415 | 20 | 50 | fits | 84,354 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 176,119 | 1.761 | 18 | 18 | fits | 101,366 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 973,773 | 9.738 | 18 | 18 | fits | 30,119 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 255,407 | 2.554 | 20 | 20 | fits | 84,354 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 65,620 | 0.656 | 20 | 200 | fits | 69,693 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 331,804 | 3.318 | 20 | 200 | fits | 84,354 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 66,532 | 0.665 | 20 | 20 | fits | 69,693 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 444,483 | 4.445 | 20 | 20 | fits | 58,429 | 39 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 70,117 | 0.701 | 20 | 24 | fits | 69,693 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 939,750 | 9.398 | 20 | 24 | fits | 44,547 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 69,077 | 0.691 | 20 | 50 | fits | 69,693 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 335,480 | 3.355 | 20 | 50 | fits | 84,354 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 170,141 | 1.701 | 18 | 18 | fits | 101,519 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 967,399 | 9.674 | 18 | 18 | fits | 30,184 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 252,530 | 2.525 | 20 | 20 | fits | 88,538 | 87 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 67,388 | 0.674 | 20 | 200 | fits | 69,693 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 329,508 | 3.295 | 20 | 200 | fits | 88,538 | 87 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 68,300 | 0.683 | 20 | 20 | fits | 69,693 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 459,856 | 4.599 | 20 | 20 | fits | 54,312 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 71,885 | 0.719 | 20 | 24 | fits | 69,693 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 956,197 | 9.562 | 20 | 24 | fits | 44,678 | 29 | 0.737 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 70,845 | 0.708 | 20 | 50 | fits | 69,693 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 333,184 | 3.332 | 20 | 50 | fits | 88,538 | 87 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 171,909 | 1.719 | 18 | 18 | fits | 101,519 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 975,746 | 9.757 | 18 | 18 | fits | 22,084 | 16 | 0.818 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 238,699 | 2.387 | 20 | 20 | fits | 84,888 | 81 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 69,156 | 0.692 | 20 | 200 | fits | 69,693 | 135 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 315,331 | 3.153 | 20 | 200 | fits | 84,888 | 81 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 70,068 | 0.701 | 20 | 20 | fits | 69,693 | 135 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 445,633 | 4.456 | 20 | 20 | fits | 54,278 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 73,653 | 0.737 | 20 | 24 | fits | 69,693 | 135 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 941,966 | 9.420 | 20 | 24 | fits | 44,642 | 29 | 0.736 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 72,613 | 0.726 | 20 | 50 | fits | 69,693 | 135 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 319,007 | 3.190 | 20 | 50 | fits | 84,888 | 81 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 234,054 | 2.341 | 18 | 18 | fits | 95,807 | 102 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 969,607 | 9.696 | 18 | 18 | fits | 30,176 | 19 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 261,978 | 2.620 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 71,993 | 0.720 | 20 | 200 | fits | 70,407 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 338,555 | 3.386 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 72,905 | 0.729 | 20 | 20 | fits | 70,407 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 468,730 | 4.687 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 76,490 | 0.765 | 20 | 24 | fits | 70,407 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 968,813 | 9.688 | 20 | 24 | fits | 49,361 | 35 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 75,450 | 0.754 | 20 | 50 | fits | 70,407 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 342,231 | 3.422 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 176,615 | 1.766 | 18 | 18 | fits | 101,620 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 966,278 | 9.663 | 18 | 18 | fits | 49,361 | 35 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 257,729 | 2.577 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 67,814 | 0.678 | 20 | 200 | fits | 70,615 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 334,306 | 3.343 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 68,726 | 0.687 | 20 | 20 | fits | 70,615 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 464,481 | 4.645 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 72,311 | 0.723 | 20 | 24 | fits | 70,615 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 941,876 | 9.419 | 20 | 24 | fits | 44,401 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 71,271 | 0.713 | 20 | 50 | fits | 70,615 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 337,982 | 3.380 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 172,326 | 1.723 | 18 | 18 | fits | 101,510 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 969,470 | 9.695 | 18 | 18 | fits | 30,129 | 19 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 261,265 | 2.613 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 71,350 | 0.714 | 20 | 200 | fits | 70,615 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 337,842 | 3.378 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 72,262 | 0.723 | 20 | 20 | fits | 70,615 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 472,575 | 4.726 | 20 | 20 | fits | 58,743 | 39 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 75,847 | 0.758 | 20 | 24 | fits | 70,615 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 966,886 | 9.669 | 20 | 24 | fits | 44,456 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 74,807 | 0.748 | 20 | 50 | fits | 70,615 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 341,518 | 3.415 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 175,862 | 1.759 | 18 | 18 | fits | 101,510 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 964,351 | 9.644 | 18 | 18 | fits | 44,456 | 29 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 260,524 | 2.605 | 20 | 20 | fits | 84,809 | 81 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 66,755 | 0.668 | 20 | 200 | fits | 70,407 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 337,211 | 3.372 | 20 | 200 | fits | 84,809 | 81 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 67,667 | 0.677 | 20 | 20 | fits | 70,407 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 467,444 | 4.674 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 71,252 | 0.713 | 20 | 24 | fits | 70,407 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 962,725 | 9.627 | 20 | 24 | fits | 44,559 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 70,212 | 0.702 | 20 | 50 | fits | 70,407 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 340,887 | 3.409 | 20 | 50 | fits | 84,809 | 81 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 171,377 | 1.714 | 18 | 18 | fits | 101,620 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 960,190 | 9.602 | 18 | 18 | fits | 44,559 | 29 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 256,042 | 2.560 | 20 | 20 | fits | 84,699 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 66,137 | 0.661 | 20 | 200 | fits | 70,926 | 135 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 332,653 | 3.327 | 20 | 200 | fits | 84,699 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 67,049 | 0.670 | 20 | 20 | fits | 70,926 | 135 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 462,941 | 4.629 | 20 | 20 | fits | 54,276 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 70,634 | 0.706 | 20 | 24 | fits | 70,926 | 135 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 964,025 | 9.640 | 20 | 24 | fits | 49,452 | 35 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 69,594 | 0.696 | 20 | 50 | fits | 70,926 | 135 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 336,329 | 3.363 | 20 | 50 | fits | 84,699 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 170,605 | 1.706 | 18 | 18 | fits | 101,466 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 961,490 | 9.615 | 18 | 18 | fits | 49,452 | 35 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 260,014 | 2.600 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 70,292 | 0.703 | 20 | 200 | fits | 70,452 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 336,591 | 3.366 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 71,204 | 0.712 | 20 | 20 | fits | 70,452 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 466,766 | 4.668 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 74,789 | 0.748 | 20 | 24 | fits | 70,452 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 967,193 | 9.672 | 20 | 24 | fits | 44,595 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 73,749 | 0.737 | 20 | 50 | fits | 70,452 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 340,267 | 3.403 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 174,611 | 1.746 | 18 | 18 | fits | 101,317 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 964,658 | 9.647 | 18 | 18 | fits | 44,595 | 29 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 255,860 | 2.559 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 65,972 | 0.660 | 20 | 200 | fits | 70,519 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 332,437 | 3.324 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 66,884 | 0.669 | 20 | 20 | fits | 70,519 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 467,170 | 4.672 | 20 | 20 | fits | 58,743 | 39 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 70,469 | 0.705 | 20 | 24 | fits | 70,519 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 961,481 | 9.615 | 20 | 24 | fits | 44,456 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 69,429 | 0.694 | 20 | 50 | fits | 70,519 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 336,113 | 3.361 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 170,497 | 1.705 | 18 | 18 | fits | 101,523 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 958,946 | 9.589 | 18 | 18 | fits | 44,456 | 29 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 254,279 | 2.543 | 20 | 20 | fits | 84,809 | 81 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 69,508 | 0.695 | 20 | 200 | fits | 70,519 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 330,966 | 3.310 | 20 | 200 | fits | 84,809 | 81 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 70,420 | 0.704 | 20 | 20 | fits | 70,519 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 461,199 | 4.612 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 74,005 | 0.740 | 20 | 24 | fits | 70,519 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 956,480 | 9.565 | 20 | 24 | fits | 44,559 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 72,965 | 0.730 | 20 | 50 | fits | 70,519 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 334,642 | 3.346 | 20 | 50 | fits | 84,809 | 81 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 164,826 | 1.648 | 18 | 18 | fits | 92,316 | 134 | 0.606 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 975,946 | 9.759 | 18 | 18 | fits | 22,001 | 16 | 0.817 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 324,307 | 3.243 | 20 | 20 | fits | 84,598 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 134,328 | 1.343 | 20 | 200 | fits | 71,032 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 400,817 | 4.008 | 20 | 200 | fits | 84,598 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 135,240 | 1.352 | 20 | 20 | fits | 71,032 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 530,992 | 5.310 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 138,825 | 1.388 | 20 | 24 | fits | 71,032 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,031,075 | 10.311 | 20 | 24 | fits | 49,361 | 35 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 137,785 | 1.378 | 20 | 50 | fits | 71,032 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 404,493 | 4.045 | 20 | 50 | fits | 84,598 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 238,944 | 2.389 | 18 | 18 | fits | 101,614 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,028,540 | 10.285 | 18 | 18 | fits | 49,361 | 35 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 262,567 | 2.626 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 72,636 | 0.726 | 20 | 200 | fits | 70,674 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 339,144 | 3.391 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 73,548 | 0.735 | 20 | 20 | fits | 70,674 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 469,319 | 4.693 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 77,133 | 0.771 | 20 | 24 | fits | 70,674 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 961,216 | 9.612 | 20 | 24 | fits | 44,738 | 29 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 76,093 | 0.761 | 20 | 50 | fits | 70,674 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 342,820 | 3.428 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 177,204 | 1.772 | 18 | 18 | fits | 101,566 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 980,718 | 9.807 | 18 | 18 | fits | 22,037 | 16 | 0.817 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 256,264 | 2.563 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 66,505 | 0.665 | 20 | 200 | fits | 70,607 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 332,841 | 3.328 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 67,417 | 0.674 | 20 | 20 | fits | 70,607 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 463,016 | 4.630 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 71,002 | 0.710 | 20 | 24 | fits | 70,607 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 963,371 | 9.634 | 20 | 24 | fits | 44,595 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 69,962 | 0.700 | 20 | 50 | fits | 70,607 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 336,517 | 3.365 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 170,861 | 1.709 | 18 | 18 | fits | 101,354 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 960,836 | 9.608 | 18 | 18 | fits | 44,595 | 29 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 258,032 | 2.580 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 68,273 | 0.683 | 20 | 200 | fits | 70,607 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 334,609 | 3.346 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 69,185 | 0.692 | 20 | 20 | fits | 70,607 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 464,784 | 4.648 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 72,770 | 0.728 | 20 | 24 | fits | 70,607 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 965,202 | 9.652 | 20 | 24 | fits | 44,595 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 71,730 | 0.717 | 20 | 50 | fits | 70,607 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 338,285 | 3.383 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 172,629 | 1.726 | 18 | 18 | fits | 101,354 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 962,667 | 9.627 | 18 | 18 | fits | 44,595 | 29 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 259,800 | 2.598 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 70,041 | 0.700 | 20 | 200 | fits | 70,607 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 336,377 | 3.364 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 70,953 | 0.710 | 20 | 20 | fits | 70,607 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 466,552 | 4.666 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 74,538 | 0.745 | 20 | 24 | fits | 70,607 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 966,006 | 9.660 | 20 | 24 | fits | 44,559 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 73,498 | 0.735 | 20 | 50 | fits | 70,607 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 340,053 | 3.401 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 174,397 | 1.744 | 18 | 18 | fits | 101,354 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 963,471 | 9.635 | 18 | 18 | fits | 44,559 | 29 | 0.735 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 261,568 | 2.616 | 20 | 20 | fits | 84,665 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 71,809 | 0.718 | 20 | 200 | fits | 70,607 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 338,145 | 3.381 | 20 | 200 | fits | 84,665 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 72,721 | 0.727 | 20 | 20 | fits | 70,607 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 450,700 | 4.507 | 20 | 20 | fits | 58,337 | 39 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 76,306 | 0.763 | 20 | 24 | fits | 70,607 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 944,965 | 9.450 | 20 | 24 | fits | 44,456 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 75,266 | 0.753 | 20 | 50 | fits | 70,607 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 341,821 | 3.418 | 20 | 50 | fits | 84,665 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 176,165 | 1.762 | 18 | 18 | fits | 101,354 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 972,523 | 9.725 | 18 | 18 | fits | 30,093 | 19 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 250,905 | 2.509 | 20 | 20 | fits | 88,773 | 87 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 65,721 | 0.657 | 20 | 200 | fits | 70,674 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 328,092 | 3.281 | 20 | 200 | fits | 88,773 | 87 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 66,633 | 0.666 | 20 | 20 | fits | 70,674 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 458,315 | 4.583 | 20 | 20 | fits | 54,219 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 70,218 | 0.702 | 20 | 24 | fits | 70,674 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 953,596 | 9.536 | 20 | 24 | fits | 44,559 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 69,178 | 0.692 | 20 | 50 | fits | 70,674 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 331,768 | 3.318 | 20 | 50 | fits | 88,773 | 87 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 170,289 | 1.703 | 18 | 18 | fits | 101,566 | 138 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 973,062 | 9.731 | 18 | 18 | fits | 22,001 | 16 | 0.817 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 237,462 | 2.375 | 20 | 20 | fits | 85,030 | 81 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 67,489 | 0.675 | 20 | 200 | fits | 70,674 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 314,147 | 3.141 | 20 | 200 | fits | 85,030 | 81 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 68,401 | 0.684 | 20 | 20 | fits | 70,674 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 444,436 | 4.444 | 20 | 20 | fits | 54,185 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 71,986 | 0.720 | 20 | 24 | fits | 70,674 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 939,717 | 9.397 | 20 | 24 | fits | 44,559 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 70,946 | 0.709 | 20 | 50 | fits | 70,674 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 317,823 | 3.178 | 20 | 50 | fits | 85,030 | 81 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 232,728 | 2.327 | 18 | 18 | fits | 96,016 | 102 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 967,275 | 9.673 | 18 | 18 | fits | 30,093 | 19 | 0.789 |
| an event behind 15 others | `backlog.event.if0` | 87,540 | 0.875 | 20 | 200 | fits | 63,042 | 104 | 0.497 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 327,931 | 3.279 | 20 | 20 | fits | 43,686 | 44 | 0.512 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 76,107 | 0.761 | 20 | 200 | fits | 76,315 | 138 | 0.512 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 271,219 | 2.712 | 20 | 200 | fits | 53,337 | 55 | 0.557 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 71,848 | 0.718 | 20 | 20 | fits | 76,315 | 138 | 0.512 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 355,104 | 3.551 | 20 | 20 | fits | 43,686 | 44 | 0.512 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 75,433 | 0.754 | 20 | 24 | fits | 76,315 | 138 | 0.512 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 587,426 | 5.874 | 20 | 24 | fits | 22,818 | 29 | 0.488 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 74,393 | 0.744 | 20 | 50 | fits | 76,315 | 138 | 0.512 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 269,724 | 2.697 | 20 | 50 | fits | 53,337 | 55 | 0.557 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 269,659 | 2.697 | 18 | 18 | fits | 53,337 | 55 | 0.557 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 612,909 | 6.129 | 18 | 18 | fits | 8,962 | 17 | 0.250 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 253,308 | 2.533 | 20 | 20 | fits | 84,340 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 63,685 | 0.637 | 20 | 200 | fits | 68,367 | 135 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 329,770 | 3.298 | 20 | 200 | fits | 84,340 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 64,597 | 0.646 | 20 | 20 | fits | 68,367 | 135 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 459,898 | 4.599 | 20 | 20 | fits | 54,182 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 68,182 | 0.682 | 20 | 24 | fits | 68,367 | 135 | 0.486 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 960,191 | 9.602 | 20 | 24 | fits | 44,590 | 29 | 0.735 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 67,142 | 0.671 | 20 | 50 | fits | 68,367 | 135 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 333,446 | 3.334 | 20 | 50 | fits | 84,340 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 168,049 | 1.680 | 18 | 18 | fits | 101,362 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 957,656 | 9.577 | 18 | 18 | fits | 44,590 | 29 | 0.735 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 6,113 | 0.061 | 20 | 20 | fits | 19,579 | 20 | 0.730 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 63,685 | 0.637 | 20 | 200 | fits | 68,367 | 135 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 19,503 | 0.195 | 20 | 200 | fits | 19,579 | 20 | 0.730 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 64,597 | 0.646 | 20 | 20 | fits | 68,367 | 135 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 454,569 | 4.546 | 20 | 20 | fits | 66,376 | 44 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 68,182 | 0.682 | 20 | 24 | fits | 68,367 | 135 | 0.486 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 911,721 | 9.117 | 20 | 24 | fits | 44,823 | 29 | 0.737 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 67,142 | 0.671 | 20 | 50 | fits | 68,367 | 135 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 323,986 | 3.240 | 20 | 50 | fits | 74,880 | 71 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 168,049 | 1.680 | 18 | 18 | fits | 101,362 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 939,336 | 9.393 | 18 | 18 | fits | 30,150 | 19 | 0.790 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,202,147 | 62.021 | 20 | 20 | MISS ceiling | 27,514 | 25 | 0.580 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,023,217 | 360.232 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,023,142 | 360.231 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,023,067 | 360.231 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,022,992 | 360.230 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 72,932 | 0.729 | 20 | 200 | fits | 66,656 | 129 | 0.492 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 326,178 | 3.262 | 20 | 200 | fits | 74,326 | 67 | 0.666 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 68,673 | 0.687 | 20 | 20 | fits | 66,656 | 129 | 0.492 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 428,781 | 4.288 | 20 | 20 | fits | 47,851 | 29 | 0.774 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 72,258 | 0.723 | 20 | 24 | fits | 66,656 | 129 | 0.492 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,286,550 | 62.865 | 20 | 24 | MISS ceiling | 22,067 | 21 | 0.611 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 71,218 | 0.712 | 20 | 50 | fits | 66,656 | 129 | 0.492 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 324,683 | 3.247 | 20 | 50 | fits | 74,326 | 67 | 0.666 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 170,915 | 1.709 | 18 | 18 | fits | 100,152 | 131 | 0.636 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 787,448 | 7.874 | 18 | 18 | fits | 21,968 | 17 | 0.810 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
