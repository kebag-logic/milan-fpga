### 1x1

Clock: CPU 50 MHz, the product's split CPU clock (the Milan clock), bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.778 (7.239) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.877 (6.432) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.086 (0.487) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.056 (3.688) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.332 (63.722) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.407 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.845 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 8.897 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.887 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.379 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.880 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 64.673 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.870 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.416 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 4.312 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 17.025 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 11.728 | 18 | 94,463 (1.889) | yes | - |
| backlog-adp | 17.493 | 17 | 92,382 (1.848) | yes | - |
| backlog-adp-refill | 40.989 | 22 | 92,382 (1.848) | yes | - |
| backlog-owed | 360.458 | 63 | 85,996 (1.720) | yes | - |

Composed maximum over the 4 backlog windows: 94,463 CPU cycles (1.889 ms), backlog.
Over the windows that released their whole load only: 94,463 (1.889 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 100,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 292 | 0 | 94,463 (1.889) | fits |
| backlog-adp | 300 | 0 | 92,382 (1.848) | fits |
| backlog-adp-refill | 305 | 0 | 92,382 (1.848) | fits |
| backlog-owed | 348 | 0 | 85,996 (1.720) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 102,805 | 2.056 | 20 | 200 | fits | 89,936 | 117 | 0.598 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 338,910 | 6.778 | 20 | 20 | fits | 39,877 | 35 | 0.574 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 94,359 | 1.887 | 20 | 200 | fits | 94,463 | 141 | 0.623 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 279,534 | 5.591 | 20 | 200 | fits | 46,501 | 55 | 0.510 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 92,230 | 1.845 | 20 | 20 | fits | 94,463 | 141 | 0.623 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 359,285 | 7.186 | 20 | 20 | fits | 39,877 | 35 | 0.574 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 94,022 | 1.880 | 20 | 24 | fits | 94,463 | 141 | 0.623 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 549,464 | 10.989 | 20 | 24 | fits | 18,353 | 29 | 0.526 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 93,502 | 1.870 | 20 | 50 | fits | 94,463 | 141 | 0.623 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 278,786 | 5.576 | 20 | 50 | fits | 46,501 | 55 | 0.510 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 183,211 | 3.664 | 18 | 18 | fits | 89,936 | 117 | 0.598 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 564,706 | 11.294 | 18 | 18 | fits | 8,022 | 17 | 0.411 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 243,847 | 4.877 | 20 | 20 | fits | 84,460 | 87 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 64,721 | 1.294 | 20 | 200 | fits | 67,062 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 318,939 | 6.379 | 20 | 200 | fits | 84,460 | 87 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 65,177 | 1.304 | 20 | 20 | fits | 67,062 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 444,862 | 8.897 | 20 | 20 | fits | 53,914 | 33 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 66,970 | 1.339 | 20 | 24 | fits | 67,062 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 852,514 | 17.050 | 20 | 24 | fits | 36,380 | 29 | 0.750 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 66,450 | 1.329 | 20 | 50 | fits | 67,062 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 320,777 | 6.416 | 20 | 50 | fits | 84,460 | 87 | 0.692 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 158,604 | 3.172 | 18 | 18 | fits | 92,382 | 138 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 851,247 | 17.025 | 18 | 18 | fits | 36,380 | 29 | 0.750 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 4,320 | 0.086 | 20 | 20 | fits | 17,386 | 20 | 0.781 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 64,721 | 1.294 | 20 | 200 | fits | 67,062 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 17,422 | 0.348 | 20 | 200 | fits | 17,386 | 20 | 0.781 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 65,177 | 1.304 | 20 | 20 | fits | 67,062 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 436,464 | 8.729 | 20 | 20 | fits | 62,492 | 44 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 66,970 | 1.339 | 20 | 24 | fits | 67,062 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 809,550 | 16.191 | 20 | 24 | fits | 36,516 | 29 | 0.753 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 66,450 | 1.329 | 20 | 50 | fits | 67,062 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 312,191 | 6.244 | 20 | 50 | fits | 75,874 | 77 | 0.689 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 158,604 | 3.172 | 18 | 18 | fits | 92,382 | 138 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 833,697 | 16.674 | 18 | 18 | fits | 25,414 | 19 | 0.795 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 3,166,607 | 63.332 | 20 | 20 | MISS ceiling | 22,723 | 25 | 0.631 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,020,348 | 360.407 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,020,310 | 360.406 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,020,273 | 360.405 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,020,235 | 360.405 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 67,995 | 1.360 | 20 | 200 | fits | 63,707 | 129 | 0.503 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 285,800 | 5.716 | 20 | 200 | fits | 69,438 | 67 | 0.690 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 65,866 | 1.317 | 20 | 20 | fits | 63,707 | 129 | 0.503 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 378,950 | 7.579 | 20 | 20 | fits | 46,519 | 33 | 0.778 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 67,658 | 1.353 | 20 | 24 | fits | 63,707 | 129 | 0.503 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 3,233,657 | 64.673 | 20 | 24 | MISS ceiling | 17,571 | 21 | 0.647 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 67,138 | 1.343 | 20 | 50 | fits | 63,707 | 129 | 0.503 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 285,052 | 5.701 | 20 | 50 | fits | 69,438 | 67 | 0.690 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 215,582 | 4.312 | 18 | 18 | fits | 85,996 | 95 | 0.691 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 689,301 | 13.786 | 18 | 18 | fits | 25,431 | 20 | 0.789 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
