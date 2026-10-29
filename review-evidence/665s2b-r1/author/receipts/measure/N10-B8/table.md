### 8x8

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 8.153 (8.876) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.321 (5.828) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.228 (0.757) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.103 (4.304) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.639 (64.005) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.490 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.956 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.823 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.999 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.775 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.692 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.992 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.940 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.982 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.677 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.280 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 16.324 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.871 | 17 | 230,298 (2.303) | yes | - |
| backlog-adp | 16.880 | 18 | 190,427 (1.904) | yes | - |
| backlog-adp-refill | 41.284 | 24 | 190,427 (1.904) | yes | - |
| backlog-owed | 360.541 | 64 | 198,166 (1.982) | yes | - |

Composed maximum over the 4 backlog windows: 230,298 CPU cycles (2.303 ms), backlog.
Over the windows that released their whole load only: 230,298 (2.303 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 210,256 | 2.103 | 20 | 200 | fits | 230,298 | 138 | 0.650 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 815,265 | 8.153 | 20 | 20 | fits | 103,683 | 46 | 0.662 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 199,893 | 1.999 | 20 | 200 | fits | 200,101 | 146 | 0.584 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 669,200 | 6.692 | 20 | 200 | fits | 113,471 | 57 | 0.630 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 195,634 | 1.956 | 20 | 20 | fits | 200,101 | 146 | 0.584 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 882,337 | 8.823 | 20 | 20 | fits | 103,683 | 46 | 0.662 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 199,219 | 1.992 | 20 | 24 | fits | 200,101 | 146 | 0.584 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,401,931 | 14.019 | 20 | 24 | fits | 51,455 | 31 | 0.676 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 198,179 | 1.982 | 20 | 50 | fits | 200,101 | 146 | 0.584 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 667,705 | 6.677 | 20 | 50 | fits | 113,471 | 57 | 0.630 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 428,022 | 4.280 | 18 | 18 | fits | 230,298 | 138 | 0.650 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,434,521 | 14.345 | 18 | 18 | fits | 35,125 | 20 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 432,124 | 4.321 | 20 | 20 | fits | 164,528 | 89 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 111,786 | 1.118 | 20 | 200 | fits | 116,468 | 140 | 0.479 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 577,489 | 5.775 | 20 | 200 | fits | 164,528 | 89 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 112,698 | 1.127 | 20 | 20 | fits | 116,468 | 140 | 0.479 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 823,193 | 8.232 | 20 | 20 | fits | 110,275 | 34 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 116,283 | 1.163 | 20 | 24 | fits | 116,468 | 140 | 0.479 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,584,091 | 15.841 | 20 | 24 | fits | 67,744 | 31 | 0.695 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 115,243 | 1.152 | 20 | 50 | fits | 116,468 | 140 | 0.479 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 581,165 | 5.812 | 20 | 50 | fits | 164,528 | 89 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 305,215 | 3.052 | 18 | 18 | fits | 190,427 | 140 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,632,441 | 16.324 | 18 | 18 | fits | 50,885 | 20 | 0.721 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 22,755 | 0.228 | 20 | 20 | fits | 44,122 | 21 | 0.770 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 111,786 | 1.118 | 20 | 200 | fits | 116,468 | 140 | 0.479 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 58,783 | 0.588 | 20 | 200 | fits | 44,122 | 21 | 0.770 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 112,698 | 1.127 | 20 | 20 | fits | 116,468 | 140 | 0.479 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 801,521 | 8.015 | 20 | 20 | fits | 121,427 | 46 | 0.667 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 116,283 | 1.163 | 20 | 24 | fits | 116,468 | 140 | 0.479 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,483,379 | 14.834 | 20 | 24 | fits | 79,175 | 37 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 115,243 | 1.152 | 20 | 50 | fits | 116,468 | 140 | 0.479 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 560,413 | 5.604 | 20 | 50 | fits | 143,776 | 79 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 305,215 | 3.052 | 18 | 18 | fits | 190,427 | 140 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,617,703 | 16.177 | 18 | 18 | fits | 35,293 | 15 | 0.771 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,363,882 | 63.639 | 20 | 20 | MISS ceiling | 49,101 | 27 | 0.507 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,049,048 | 360.490 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,048,973 | 360.490 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,048,898 | 360.489 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,048,823 | 360.488 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 117,536 | 1.175 | 20 | 200 | fits | 114,024 | 134 | 0.486 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 597,222 | 5.972 | 20 | 200 | fits | 135,298 | 69 | 0.658 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 113,277 | 1.133 | 20 | 20 | fits | 114,024 | 134 | 0.486 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 802,287 | 8.023 | 20 | 20 | fits | 102,783 | 35 | 0.744 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 116,862 | 1.169 | 20 | 24 | fits | 114,024 | 134 | 0.486 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,493,984 | 64.940 | 20 | 24 | MISS ceiling | 30,106 | 23 | 0.482 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 115,822 | 1.158 | 20 | 50 | fits | 114,024 | 134 | 0.486 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 595,727 | 5.957 | 20 | 50 | fits | 135,298 | 69 | 0.658 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 313,533 | 3.135 | 18 | 18 | fits | 198,166 | 138 | 0.641 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,375,787 | 13.758 | 18 | 18 | fits | 51,198 | 21 | 0.733 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
