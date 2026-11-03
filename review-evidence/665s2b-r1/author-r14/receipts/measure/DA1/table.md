### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 21 paths and 6 of 323 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.272 (3.598) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 3.309 (4.921) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.077 (0.342) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.875 (1.395) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.060 (62.321) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.218 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.823 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.368 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 5.596 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.372 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.652 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.417 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 5.435 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.407 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.077 | fits | 7 adp | 28 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.452 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.926 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.442 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.114 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.692 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.srp.last.if0` (backlog-adp@blank-0) | 10.511 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.602 | 18 | 101,390 (1.014) | yes | - |
| backlog-adp@blank-1 | 0 | 10.922 | 18 | 101,592 (1.016) | yes | - |
| backlog-adp@blank-2 | 0 | 10.855 | 18 | 101,390 (1.014) | yes | - |
| backlog-adp@blank-3 | 0 | 10.860 | 18 | 101,458 (1.015) | yes | - |
| backlog-adp@blank-4 | 0 | 10.995 | 18 | 101,390 (1.014) | yes | - |
| backlog-adp@blank-5 | 0 | 10.899 | 17 | 103,269 (1.033) | yes | - |
| backlog-adp@blank-6 | 0 | 10.898 | 18 | 101,467 (1.015) | yes | - |
| backlog-adp@blank-7 | 0 | 10.893 | 18 | 96,346 (0.963) | yes | - |
| backlog-adp@program-0 | 0 | 10.963 | 18 | 101,258 (1.013) | yes | - |
| backlog-adp@program-1 | 0 | 11.128 | 18 | 98,336 (0.983) | yes | - |
| backlog-adp@program-2 | 0 | 11.054 | 18 | 101,327 (1.013) | yes | - |
| backlog-adp@program-3 | 0 | 10.971 | 18 | 92,215 (0.922) | yes | - |
| backlog-adp@program-4 | 0 | 10.539 | 20 | 101,558 (1.016) | yes | - |
| backlog-adp@program-5 | 0 | 10.107 | 17 | 101,271 (1.013) | yes | - |
| backlog-adp@program-6 | 0 | 10.252 | 18 | 101,271 (1.013) | yes | - |
| backlog-adp@program-7 | 0 | 10.278 | 18 | 94,954 (0.950) | yes | - |
| backlog-adp@verify-0 | 0 | 11.526 | 18 | 101,327 (1.013) | yes | - |
| backlog-adp@verify-1 | 0 | 10.993 | 18 | 101,456 (1.015) | yes | - |
| backlog-adp@verify-2 | 0 | 10.846 | 17 | 101,456 (1.015) | yes | - |
| backlog-adp@verify-3 | 0 | 10.865 | 18 | 101,388 (1.014) | yes | - |
| backlog-adp@verify-4 | 0 | 10.991 | 18 | 101,456 (1.015) | yes | - |
| backlog-adp@verify-5 | 0 | 10.915 | 17 | 103,246 (1.032) | yes | - |
| backlog-adp@verify-6 | 0 | 10.906 | 18 | 101,447 (1.014) | yes | - |
| backlog-adp@verify-7 | 0 | 10.906 | 18 | 96,485 (0.965) | yes | - |
| backlog | 0 | 6.536 | 19 | 78,373 (0.784) | yes | - |
| backlog-adp | 0 | 10.239 | 19 | 101,152 (1.012) | yes | - |
| backlog-adp-refill | 0 | 40.524 | 31 | 101,152 (1.012) | yes | - |
| backlog-owed | 0 | 360.269 | 65 | 100,189 (1.002) | yes | - |

Composed maximum over the 4 backlog windows: 101,152 CPU cycles (1.012 ms), backlog-adp.
Over the windows that released their whole load only: 101,152 (1.012 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 388 | 0 | 101,390 (1.014) | fits |
| backlog-adp@blank-1 | 389 | 0 | 101,592 (1.016) | fits |
| backlog-adp@blank-2 | 388 | 0 | 101,390 (1.014) | fits |
| backlog-adp@blank-3 | 388 | 0 | 101,458 (1.015) | fits |
| backlog-adp@blank-4 | 388 | 0 | 101,390 (1.014) | fits |
| backlog-adp@blank-5 | 387 | 0 | 103,269 (1.033) | fits |
| backlog-adp@blank-6 | 389 | 0 | 101,467 (1.015) | fits |
| backlog-adp@blank-7 | 389 | 0 | 96,346 (0.963) | fits |
| backlog-adp@program-0 | 464 | 0 | 118,240 (1.182) | fits |
| backlog-adp@program-1 | 464 | 0 | 118,240 (1.182) | fits |
| backlog-adp@program-2 | 467 | 0 | 118,240 (1.182) | fits |
| backlog-adp@program-3 | 466 | 0 | 118,240 (1.182) | fits |
| backlog-adp@program-4 | 469 | 0 | 118,240 (1.182) | fits |
| backlog-adp@program-5 | 467 | 0 | 118,240 (1.182) | fits |
| backlog-adp@program-6 | 468 | 0 | 118,240 (1.182) | fits |
| backlog-adp@program-7 | 468 | 0 | 118,240 (1.182) | fits |
| backlog-adp@verify-0 | 534 | 0 | 118,240 (1.182) | fits |
| backlog-adp@verify-1 | 534 | 0 | 118,240 (1.182) | fits |
| backlog-adp@verify-2 | 534 | 0 | 118,240 (1.182) | fits |
| backlog-adp@verify-3 | 534 | 0 | 118,240 (1.182) | fits |
| backlog-adp@verify-4 | 534 | 0 | 118,240 (1.182) | fits |
| backlog-adp@verify-5 | 533 | 0 | 118,240 (1.182) | fits |
| backlog-adp@verify-6 | 535 | 0 | 118,240 (1.182) | fits |
| backlog-adp@verify-7 | 535 | 0 | 118,240 (1.182) | fits |
| save-held | 3405 | 0 | 76,331 (0.763) | fits |
| save-starved | 39664 | 0 | 79,057 (0.791) | fits |
| save | 602 | 0 | 117,362 (1.174) | fits |
| backlog | 293 | 0 | 78,373 (0.784) | fits |
| backlog-adp | 315 | 0 | 101,152 (1.012) | fits |
| backlog-adp-refill | 327 | 0 | 101,152 (1.012) | fits |
| backlog-owed | 350 | 0 | 100,189 (1.002) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---|---|
| save-held | 2018.102 | 4,070 | 102 | 13.895 | no | within |
| save-starved | 4047.950 | 4,070 | 102 | 31.080 | yes | within |
| save | 2018.253 | 4,070 | 102 | 10.862 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 299 | 85,493 (0.855) | 75,924 (0.759) |
| backlog-adp@blank-1 | 299 | 85,567 (0.856) | 75,924 (0.759) |
| backlog-adp@blank-2 | 299 | 85,605 (0.856) | 75,953 (0.760) |
| backlog-adp@blank-3 | 299 | 85,605 (0.856) | 75,953 (0.760) |
| backlog-adp@blank-4 | 299 | 85,055 (0.851) | 75,820 (0.758) |
| backlog-adp@blank-5 | 299 | 85,552 (0.856) | 75,900 (0.759) |
| backlog-adp@blank-6 | 299 | 85,503 (0.855) | 75,851 (0.759) |
| backlog-adp@blank-7 | 299 | 85,581 (0.856) | 75,929 (0.759) |
| backlog-adp@program-0 | 328 | 118,240 (1.182) | 81,624 (0.816) |
| backlog-adp@program-1 | 328 | 118,240 (1.182) | 81,624 (0.816) |
| backlog-adp@program-2 | 328 | 118,240 (1.182) | 81,653 (0.817) |
| backlog-adp@program-3 | 328 | 118,240 (1.182) | 81,653 (0.817) |
| backlog-adp@program-4 | 329 | 118,240 (1.182) | 81,122 (0.811) |
| backlog-adp@program-5 | 329 | 118,240 (1.182) | 81,122 (0.811) |
| backlog-adp@program-6 | 329 | 118,240 (1.182) | 81,122 (0.811) |
| backlog-adp@program-7 | 329 | 118,240 (1.182) | 81,122 (0.811) |
| backlog-adp@verify-0 | 355 | 118,240 (1.182) | 95,401 (0.954) |
| backlog-adp@verify-1 | 355 | 118,240 (1.182) | 95,401 (0.954) |
| backlog-adp@verify-2 | 355 | 118,240 (1.182) | 95,401 (0.954) |
| backlog-adp@verify-3 | 355 | 118,240 (1.182) | 95,401 (0.954) |
| backlog-adp@verify-4 | 355 | 118,240 (1.182) | 95,401 (0.954) |
| backlog-adp@verify-5 | 355 | 118,240 (1.182) | 95,401 (0.954) |
| backlog-adp@verify-6 | 355 | 118,240 (1.182) | 95,401 (0.954) |
| backlog-adp@verify-7 | 355 | 118,240 (1.182) | 95,401 (0.954) |
| save-held | 722 | 104,255 (1.043) | 95,471 (0.955) |
| save-starved | 418 | 97,125 (0.971) | 96,579 (0.966) |
| save | 585 | 117,362 (1.174) | 95,536 (0.955) |
| backlog | 265 | 44,227 (0.442) | 2,908 (0.029) |
| backlog-adp | 271 | 44,227 (0.442) | 2,908 (0.029) |
| backlog-adp-refill | 274 | 44,227 (0.442) | 2,908 (0.029) |
| backlog-owed | 306 | 45,590 (0.456) | 2,908 (0.029) |

Longest pass that carries a step: 118,240 CPU cycles (1.182 ms), backlog-adp@program-0; longest step: 96,579 (0.966 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 330,923 | 3.309 | 20 | 20 | fits | 84,648 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 140,739 | 1.407 | 20 | 200 | fits | 70,367 | 135 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 407,676 | 4.077 | 20 | 200 | fits | 84,648 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 141,651 | 1.417 | 20 | 20 | fits | 70,367 | 135 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 543,484 | 5.435 | 20 | 20 | fits | 67,123 | 44 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 145,236 | 1.452 | 20 | 24 | fits | 70,367 | 135 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 987,276 | 9.873 | 20 | 24 | fits | 24,385 | 20 | 0.672 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 144,196 | 1.442 | 20 | 50 | fits | 70,367 | 135 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 411,352 | 4.114 | 20 | 50 | fits | 84,648 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 245,131 | 2.451 | 18 | 18 | fits | 101,390 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,051,056 | 10.511 | 18 | 18 | fits | 30,320 | 17 | 0.787 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 286,741 | 2.867 | 20 | 20 | fits | 78,458 | 58 | 0.673 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 100,451 | 1.005 | 20 | 200 | fits | 69,745 | 137 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 357,304 | 3.573 | 20 | 200 | fits | 78,458 | 58 | 0.673 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 101,363 | 1.014 | 20 | 20 | fits | 69,745 | 137 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 492,346 | 4.923 | 20 | 20 | fits | 67,077 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 35,203 | 0.352 | 20 | 24 | fits | 36,344 | 63 | 0.580 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 894,195 | 8.942 | 20 | 24 | fits | 49,587 | 35 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 34,163 | 0.342 | 20 | 50 | fits | 36,344 | 63 | 0.580 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 282,522 | 2.825 | 20 | 50 | fits | 77,412 | 74 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 205,045 | 2.050 | 18 | 18 | fits | 101,592 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 982,999 | 9.830 | 18 | 18 | fits | 29,837 | 17 | 0.780 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 256,466 | 2.565 | 20 | 20 | fits | 84,648 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 66,110 | 0.661 | 20 | 200 | fits | 69,920 | 135 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 333,219 | 3.332 | 20 | 200 | fits | 84,648 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 67,022 | 0.670 | 20 | 20 | fits | 69,920 | 135 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 452,956 | 4.530 | 20 | 20 | fits | 51,052 | 46 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 70,607 | 0.706 | 20 | 24 | fits | 69,920 | 135 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 917,151 | 9.172 | 20 | 24 | fits | 45,210 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 69,567 | 0.696 | 20 | 50 | fits | 69,920 | 135 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 336,895 | 3.369 | 20 | 50 | fits | 84,648 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 170,502 | 1.705 | 18 | 18 | fits | 101,390 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 976,247 | 9.762 | 18 | 18 | fits | 30,304 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 258,148 | 2.581 | 20 | 20 | fits | 68,704 | 83 | 0.611 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 67,724 | 0.677 | 20 | 200 | fits | 69,706 | 135 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 318,957 | 3.190 | 20 | 200 | fits | 68,704 | 83 | 0.611 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 68,636 | 0.686 | 20 | 20 | fits | 69,706 | 135 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 456,860 | 4.569 | 20 | 20 | fits | 67,237 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 72,221 | 0.722 | 20 | 24 | fits | 69,706 | 135 | 0.496 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 917,710 | 9.177 | 20 | 24 | fits | 45,132 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 71,181 | 0.712 | 20 | 50 | fits | 69,706 | 135 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 322,633 | 3.226 | 20 | 50 | fits | 68,704 | 83 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 172,184 | 1.722 | 18 | 18 | fits | 101,458 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 976,824 | 9.768 | 18 | 18 | fits | 30,300 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 269,969 | 2.700 | 20 | 20 | fits | 84,916 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 69,766 | 0.698 | 20 | 200 | fits | 69,920 | 135 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 346,881 | 3.469 | 20 | 200 | fits | 84,916 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 70,678 | 0.707 | 20 | 20 | fits | 69,920 | 135 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 483,154 | 4.832 | 20 | 20 | fits | 67,250 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 74,263 | 0.743 | 20 | 24 | fits | 69,920 | 135 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 942,540 | 9.425 | 20 | 24 | fits | 45,028 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 73,223 | 0.732 | 20 | 50 | fits | 69,920 | 135 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 350,557 | 3.506 | 20 | 50 | fits | 84,916 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 174,158 | 1.742 | 18 | 18 | fits | 101,390 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 971,250 | 9.713 | 18 | 18 | fits | 31,245 | 19 | 0.792 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 269,028 | 2.690 | 20 | 20 | fits | 84,836 | 81 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 76,603 | 0.766 | 20 | 200 | fits | 74,929 | 146 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 345,969 | 3.460 | 20 | 200 | fits | 84,836 | 81 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 77,515 | 0.775 | 20 | 20 | fits | 74,929 | 146 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 487,193 | 4.872 | 20 | 20 | fits | 67,593 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 81,100 | 0.811 | 20 | 24 | fits | 74,929 | 146 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 952,146 | 9.521 | 20 | 24 | fits | 45,456 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 80,060 | 0.801 | 20 | 50 | fits | 74,929 | 146 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 349,645 | 3.496 | 20 | 50 | fits | 84,836 | 81 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 182,874 | 1.829 | 18 | 18 | fits | 103,269 | 143 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 980,826 | 9.808 | 18 | 18 | fits | 31,215 | 19 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 243,203 | 2.432 | 20 | 20 | fits | 87,584 | 87 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 70,853 | 0.709 | 20 | 200 | fits | 69,593 | 135 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 319,556 | 3.196 | 20 | 200 | fits | 87,584 | 87 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 71,765 | 0.718 | 20 | 20 | fits | 69,593 | 135 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 455,532 | 4.555 | 20 | 20 | fits | 67,078 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 75,350 | 0.753 | 20 | 24 | fits | 69,593 | 135 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 921,608 | 9.216 | 20 | 24 | fits | 45,376 | 29 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 74,310 | 0.743 | 20 | 50 | fits | 69,593 | 135 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 323,232 | 3.232 | 20 | 50 | fits | 87,584 | 87 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 175,322 | 1.753 | 18 | 18 | fits | 101,467 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 980,698 | 9.807 | 18 | 18 | fits | 30,292 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 242,121 | 2.421 | 20 | 20 | fits | 85,059 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 71,797 | 0.718 | 20 | 200 | fits | 69,593 | 135 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 319,059 | 3.191 | 20 | 200 | fits | 85,059 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 72,709 | 0.727 | 20 | 20 | fits | 69,593 | 135 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 454,695 | 4.547 | 20 | 20 | fits | 67,037 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 76,294 | 0.763 | 20 | 24 | fits | 69,593 | 135 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 921,070 | 9.211 | 20 | 24 | fits | 45,124 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 75,254 | 0.753 | 20 | 50 | fits | 69,593 | 135 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 322,735 | 3.227 | 20 | 50 | fits | 85,059 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 237,611 | 2.376 | 18 | 18 | fits | 96,346 | 102 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 980,142 | 9.801 | 18 | 18 | fits | 30,292 | 17 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 259,781 | 2.598 | 20 | 20 | fits | 84,688 | 81 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 69,809 | 0.698 | 20 | 200 | fits | 70,361 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 336,693 | 3.367 | 20 | 200 | fits | 84,688 | 81 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 70,721 | 0.707 | 20 | 20 | fits | 70,361 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 481,982 | 4.820 | 20 | 20 | fits | 70,641 | 50 | 0.699 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 74,306 | 0.743 | 20 | 24 | fits | 70,361 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 916,931 | 9.169 | 20 | 24 | fits | 24,434 | 20 | 0.674 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 73,266 | 0.733 | 20 | 50 | fits | 70,361 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 340,369 | 3.404 | 20 | 50 | fits | 84,688 | 81 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 174,069 | 1.741 | 18 | 18 | fits | 101,258 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 981,092 | 9.811 | 18 | 18 | fits | 30,421 | 17 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 263,661 | 2.637 | 20 | 20 | fits | 85,045 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 73,465 | 0.735 | 20 | 200 | fits | 70,361 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 340,779 | 3.408 | 20 | 200 | fits | 85,045 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 74,377 | 0.744 | 20 | 20 | fits | 70,361 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 477,035 | 4.770 | 20 | 20 | fits | 67,281 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 77,962 | 0.780 | 20 | 24 | fits | 70,361 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 938,069 | 9.381 | 20 | 24 | fits | 45,132 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 76,922 | 0.769 | 20 | 50 | fits | 70,361 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 344,455 | 3.445 | 20 | 50 | fits | 85,045 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 174,803 | 1.748 | 18 | 18 | fits | 98,336 | 145 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 997,450 | 9.975 | 18 | 18 | fits | 32,464 | 23 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 286,588 | 2.866 | 20 | 20 | fits | 78,595 | 58 | 0.674 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 100,657 | 1.007 | 20 | 200 | fits | 70,267 | 137 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 357,332 | 3.573 | 20 | 200 | fits | 78,595 | 58 | 0.674 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 101,569 | 1.016 | 20 | 20 | fits | 70,267 | 137 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 489,409 | 4.894 | 20 | 20 | fits | 72,151 | 50 | 0.700 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 34,887 | 0.349 | 20 | 24 | fits | 35,955 | 63 | 0.582 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 900,719 | 9.007 | 20 | 24 | fits | 45,132 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 33,847 | 0.338 | 20 | 50 | fits | 35,955 | 63 | 0.582 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 282,413 | 2.824 | 20 | 50 | fits | 77,362 | 74 | 0.642 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 204,986 | 2.050 | 18 | 18 | fits | 101,327 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 990,029 | 9.900 | 18 | 18 | fits | 30,196 | 17 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 253,271 | 2.533 | 20 | 20 | fits | 85,008 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 68,099 | 0.681 | 20 | 200 | fits | 70,008 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 330,349 | 3.303 | 20 | 200 | fits | 85,008 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 69,011 | 0.690 | 20 | 20 | fits | 70,008 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 463,949 | 4.639 | 20 | 20 | fits | 64,815 | 51 | 0.699 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 72,596 | 0.726 | 20 | 24 | fits | 70,008 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 922,654 | 9.227 | 20 | 24 | fits | 45,136 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 71,556 | 0.716 | 20 | 50 | fits | 70,008 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 334,025 | 3.340 | 20 | 50 | fits | 85,008 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 163,316 | 1.633 | 18 | 18 | fits | 92,215 | 134 | 0.603 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 981,776 | 9.818 | 18 | 18 | fits | 30,150 | 17 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 243,653 | 2.437 | 20 | 20 | fits | 86,644 | 87 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 67,406 | 0.674 | 20 | 200 | fits | 70,999 | 135 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 320,735 | 3.207 | 20 | 200 | fits | 86,644 | 87 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 68,318 | 0.683 | 20 | 20 | fits | 70,999 | 135 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 457,107 | 4.571 | 20 | 20 | fits | 67,240 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 71,903 | 0.719 | 20 | 24 | fits | 70,999 | 135 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 913,638 | 9.136 | 20 | 24 | fits | 45,236 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 70,863 | 0.709 | 20 | 50 | fits | 70,999 | 135 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 324,411 | 3.244 | 20 | 50 | fits | 86,644 | 87 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 171,966 | 1.720 | 18 | 18 | fits | 101,558 | 138 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 977,478 | 9.775 | 18 | 18 | fits | 30,443 | 17 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 259,166 | 2.592 | 20 | 20 | fits | 84,572 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 69,086 | 0.691 | 20 | 200 | fits | 70,233 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 335,962 | 3.360 | 20 | 200 | fits | 84,572 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 69,998 | 0.700 | 20 | 20 | fits | 70,233 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 471,860 | 4.719 | 20 | 20 | fits | 67,145 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 73,583 | 0.736 | 20 | 24 | fits | 70,233 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 942,918 | 9.429 | 20 | 24 | fits | 45,132 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 72,543 | 0.725 | 20 | 50 | fits | 70,233 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 339,638 | 3.396 | 20 | 50 | fits | 84,572 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 173,359 | 1.734 | 18 | 18 | fits | 101,271 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 971,860 | 9.719 | 18 | 18 | fits | 31,477 | 19 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 261,054 | 2.611 | 20 | 20 | fits | 84,572 | 81 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 70,974 | 0.710 | 20 | 200 | fits | 70,233 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 337,850 | 3.378 | 20 | 200 | fits | 84,572 | 81 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 71,886 | 0.719 | 20 | 20 | fits | 70,233 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 478,762 | 4.788 | 20 | 20 | fits | 72,159 | 50 | 0.700 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 75,471 | 0.755 | 20 | 24 | fits | 70,233 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 935,177 | 9.352 | 20 | 24 | fits | 45,136 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 74,431 | 0.744 | 20 | 50 | fits | 70,233 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 341,526 | 3.415 | 20 | 50 | fits | 84,572 | 81 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 175,247 | 1.752 | 18 | 18 | fits | 101,271 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 986,267 | 9.863 | 18 | 18 | fits | 22,118 | 14 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 267,141 | 2.671 | 20 | 20 | fits | 94,954 | 99 | 0.677 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 72,862 | 0.729 | 20 | 200 | fits | 70,233 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 344,949 | 3.449 | 20 | 200 | fits | 94,954 | 99 | 0.677 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 73,774 | 0.738 | 20 | 20 | fits | 70,233 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 481,519 | 4.815 | 20 | 20 | fits | 67,280 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 77,359 | 0.774 | 20 | 24 | fits | 70,233 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 937,810 | 9.378 | 20 | 24 | fits | 45,236 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 76,319 | 0.763 | 20 | 50 | fits | 70,233 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 348,625 | 3.486 | 20 | 50 | fits | 94,954 | 99 | 0.677 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 167,970 | 1.680 | 18 | 18 | fits | 92,106 | 134 | 0.602 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 988,943 | 9.889 | 18 | 18 | fits | 22,116 | 14 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 320,452 | 3.205 | 20 | 20 | fits | 84,688 | 81 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 130,384 | 1.304 | 20 | 200 | fits | 71,164 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 397,364 | 3.974 | 20 | 200 | fits | 84,688 | 81 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 131,296 | 1.313 | 20 | 20 | fits | 71,164 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 533,262 | 5.333 | 20 | 20 | fits | 67,145 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 134,881 | 1.349 | 20 | 24 | fits | 71,164 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 978,480 | 9.785 | 20 | 24 | fits | 24,384 | 20 | 0.670 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 133,841 | 1.338 | 20 | 50 | fits | 71,164 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 401,040 | 4.010 | 20 | 50 | fits | 84,688 | 81 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 234,713 | 2.347 | 18 | 18 | fits | 101,327 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,042,596 | 10.426 | 18 | 18 | fits | 30,417 | 17 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 263,415 | 2.634 | 20 | 20 | fits | 84,688 | 81 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 73,266 | 0.733 | 20 | 200 | fits | 70,370 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 340,327 | 3.403 | 20 | 200 | fits | 84,688 | 81 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 74,178 | 0.742 | 20 | 20 | fits | 70,370 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 476,225 | 4.762 | 20 | 20 | fits | 67,145 | 44 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 77,763 | 0.778 | 20 | 24 | fits | 70,370 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 938,097 | 9.381 | 20 | 24 | fits | 45,554 | 29 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 76,723 | 0.767 | 20 | 50 | fits | 70,370 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 344,003 | 3.440 | 20 | 50 | fits | 84,688 | 81 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 177,724 | 1.777 | 18 | 18 | fits | 101,456 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 989,181 | 9.892 | 18 | 18 | fits | 22,116 | 14 | 0.816 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 255,487 | 2.555 | 20 | 20 | fits | 84,688 | 81 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 65,338 | 0.653 | 20 | 200 | fits | 70,370 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 332,399 | 3.324 | 20 | 200 | fits | 84,688 | 81 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 66,250 | 0.662 | 20 | 20 | fits | 70,370 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 452,158 | 4.522 | 20 | 20 | fits | 51,006 | 46 | 0.633 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 69,835 | 0.698 | 20 | 24 | fits | 70,370 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 915,621 | 9.156 | 20 | 24 | fits | 45,102 | 29 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 68,795 | 0.688 | 20 | 50 | fits | 70,370 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 336,075 | 3.361 | 20 | 50 | fits | 84,688 | 81 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 169,796 | 1.698 | 18 | 18 | fits | 101,456 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 974,501 | 9.745 | 18 | 18 | fits | 30,042 | 17 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 257,461 | 2.575 | 20 | 20 | fits | 68,762 | 83 | 0.612 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 67,380 | 0.674 | 20 | 200 | fits | 70,584 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 318,447 | 3.184 | 20 | 200 | fits | 68,762 | 83 | 0.612 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 68,292 | 0.683 | 20 | 20 | fits | 70,584 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 456,635 | 4.566 | 20 | 20 | fits | 67,391 | 44 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 71,877 | 0.719 | 20 | 24 | fits | 70,584 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 917,485 | 9.175 | 20 | 24 | fits | 45,132 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 70,837 | 0.708 | 20 | 50 | fits | 70,584 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 322,123 | 3.221 | 20 | 50 | fits | 68,762 | 83 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 171,770 | 1.718 | 18 | 18 | fits | 101,388 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 976,599 | 9.766 | 18 | 18 | fits | 30,146 | 17 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 268,755 | 2.688 | 20 | 20 | fits | 85,062 | 81 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 68,994 | 0.690 | 20 | 200 | fits | 70,370 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 345,895 | 3.459 | 20 | 200 | fits | 85,062 | 81 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 69,906 | 0.699 | 20 | 20 | fits | 70,370 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 482,304 | 4.823 | 20 | 20 | fits | 67,318 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 73,491 | 0.735 | 20 | 24 | fits | 70,370 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 942,770 | 9.428 | 20 | 24 | fits | 45,136 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 72,451 | 0.725 | 20 | 50 | fits | 70,370 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 349,571 | 3.496 | 20 | 50 | fits | 85,062 | 81 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 173,452 | 1.735 | 18 | 18 | fits | 101,456 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 977,843 | 9.778 | 18 | 18 | fits | 37,608 | 30 | 0.801 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 268,501 | 2.685 | 20 | 20 | fits | 84,898 | 81 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 76,256 | 0.763 | 20 | 200 | fits | 75,804 | 146 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 345,623 | 3.456 | 20 | 200 | fits | 84,898 | 81 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 77,168 | 0.772 | 20 | 20 | fits | 75,804 | 146 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 486,983 | 4.870 | 20 | 20 | fits | 67,661 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 80,753 | 0.808 | 20 | 24 | fits | 75,804 | 146 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 952,557 | 9.526 | 20 | 24 | fits | 45,502 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 79,713 | 0.797 | 20 | 50 | fits | 75,804 | 146 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 349,299 | 3.493 | 20 | 50 | fits | 84,898 | 81 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 182,504 | 1.825 | 18 | 18 | fits | 103,246 | 143 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 981,525 | 9.815 | 18 | 18 | fits | 31,503 | 19 | 0.796 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 242,839 | 2.428 | 20 | 20 | fits | 87,719 | 87 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 70,439 | 0.704 | 20 | 200 | fits | 70,312 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 319,273 | 3.193 | 20 | 200 | fits | 87,719 | 87 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 71,351 | 0.714 | 20 | 20 | fits | 70,312 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 455,549 | 4.555 | 20 | 20 | fits | 67,186 | 44 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 74,936 | 0.749 | 20 | 24 | fits | 70,312 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 921,381 | 9.214 | 20 | 24 | fits | 45,132 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 73,896 | 0.739 | 20 | 50 | fits | 70,312 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 322,949 | 3.229 | 20 | 50 | fits | 87,719 | 87 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 174,888 | 1.749 | 18 | 18 | fits | 101,447 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 980,495 | 9.805 | 18 | 18 | fits | 30,146 | 17 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 242,148 | 2.421 | 20 | 20 | fits | 85,387 | 81 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 71,383 | 0.714 | 20 | 200 | fits | 70,312 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 319,223 | 3.192 | 20 | 200 | fits | 85,387 | 81 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 72,295 | 0.723 | 20 | 20 | fits | 70,312 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 455,367 | 4.554 | 20 | 20 | fits | 67,224 | 44 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 75,880 | 0.759 | 20 | 24 | fits | 70,312 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 921,480 | 9.215 | 20 | 24 | fits | 45,132 | 29 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 74,840 | 0.748 | 20 | 50 | fits | 70,312 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 322,899 | 3.229 | 20 | 50 | fits | 85,387 | 81 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 237,447 | 2.374 | 18 | 18 | fits | 96,485 | 102 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 980,568 | 9.806 | 18 | 18 | fits | 30,146 | 17 | 0.786 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 228,249 | 2.282 | 20 | 200 | fits | 64,148 | 84 | 0.588 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 366,136 | 3.661 | 20 | 20 | fits | 50,274 | 32 | 0.697 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 503,827 | 5.038 | 20 | 24 | fits | 22,628 | 21 | 0.618 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 226,799 | 2.268 | 20 | 50 | fits | 56,740 | 55 | 0.664 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 707,245 | 7.072 | 18 | 18 | fits | 44,832 | 29 | 0.730 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 236,771 | 2.368 | 20 | 200 | fits | 67,473 | 90 | 0.611 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 382,327 | 3.823 | 20 | 20 | fits | 52,391 | 38 | 0.699 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 559,624 | 5.596 | 20 | 24 | fits | 25,195 | 27 | 0.648 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 237,227 | 2.372 | 20 | 50 | fits | 59,884 | 61 | 0.680 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 765,169 | 7.652 | 18 | 18 | fits | 50,281 | 41 | 0.725 |
| an event behind 15 others | `backlog.event.if0` | 87,473 | 0.875 | 20 | 200 | fits | 62,885 | 104 | 0.487 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 327,222 | 3.272 | 20 | 20 | fits | 43,722 | 44 | 0.498 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 76,448 | 0.764 | 20 | 200 | fits | 76,656 | 138 | 0.515 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 270,730 | 2.707 | 20 | 200 | fits | 53,633 | 55 | 0.553 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 72,189 | 0.722 | 20 | 20 | fits | 76,656 | 138 | 0.515 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 354,505 | 3.545 | 20 | 20 | fits | 43,722 | 44 | 0.498 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 75,774 | 0.758 | 20 | 24 | fits | 76,656 | 138 | 0.515 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 595,027 | 5.950 | 20 | 24 | fits | 23,662 | 29 | 0.503 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 74,734 | 0.747 | 20 | 50 | fits | 76,656 | 138 | 0.515 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 269,235 | 2.692 | 20 | 50 | fits | 53,633 | 55 | 0.553 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 269,170 | 2.692 | 18 | 18 | fits | 53,633 | 55 | 0.553 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 624,362 | 6.244 | 18 | 18 | fits | 10,052 | 17 | 0.400 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 253,705 | 2.537 | 20 | 20 | fits | 68,691 | 83 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 63,896 | 0.639 | 20 | 200 | fits | 68,578 | 135 | 0.481 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 314,580 | 3.146 | 20 | 200 | fits | 68,691 | 83 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 64,808 | 0.648 | 20 | 20 | fits | 68,578 | 135 | 0.481 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 452,642 | 4.526 | 20 | 20 | fits | 67,413 | 44 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 68,393 | 0.684 | 20 | 24 | fits | 68,578 | 135 | 0.481 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 907,102 | 9.071 | 20 | 24 | fits | 45,308 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 67,353 | 0.674 | 20 | 50 | fits | 68,578 | 135 | 0.481 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 318,256 | 3.183 | 20 | 50 | fits | 68,691 | 83 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 168,050 | 1.681 | 18 | 18 | fits | 101,152 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 988,213 | 9.882 | 18 | 18 | fits | 22,007 | 14 | 0.813 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 7,735 | 0.077 | 20 | 20 | fits | 21,575 | 20 | 0.768 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 63,896 | 0.639 | 20 | 200 | fits | 68,578 | 135 | 0.481 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 22,797 | 0.228 | 20 | 200 | fits | 21,575 | 20 | 0.768 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 64,808 | 0.648 | 20 | 20 | fits | 68,578 | 135 | 0.481 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 442,866 | 4.429 | 20 | 20 | fits | 67,441 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 68,393 | 0.684 | 20 | 24 | fits | 68,578 | 135 | 0.481 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 905,295 | 9.053 | 20 | 24 | fits | 45,308 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 67,353 | 0.674 | 20 | 50 | fits | 68,578 | 135 | 0.481 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 308,942 | 3.089 | 20 | 50 | fits | 59,377 | 73 | 0.601 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 168,050 | 1.681 | 18 | 18 | fits | 101,152 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 964,373 | 9.644 | 18 | 18 | fits | 30,295 | 17 | 0.788 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,206,049 | 62.060 | 20 | 20 | MISS ceiling | 28,112 | 25 | 0.589 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,021,842 | 360.218 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,021,767 | 360.218 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,021,692 | 360.217 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,021,617 | 360.216 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 74,431 | 0.744 | 20 | 200 | fits | 66,620 | 129 | 0.485 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 327,892 | 3.279 | 20 | 200 | fits | 74,465 | 67 | 0.663 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 70,172 | 0.702 | 20 | 20 | fits | 66,620 | 129 | 0.485 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 430,255 | 4.303 | 20 | 20 | fits | 47,785 | 29 | 0.767 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 73,757 | 0.738 | 20 | 24 | fits | 66,620 | 129 | 0.485 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,292,621 | 62.926 | 20 | 24 | MISS ceiling | 22,633 | 21 | 0.618 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 72,717 | 0.727 | 20 | 50 | fits | 66,620 | 129 | 0.485 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 326,397 | 3.264 | 20 | 50 | fits | 74,465 | 67 | 0.663 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 172,451 | 1.725 | 18 | 18 | fits | 100,189 | 131 | 0.637 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 795,947 | 7.959 | 18 | 18 | fits | 22,718 | 17 | 0.814 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
