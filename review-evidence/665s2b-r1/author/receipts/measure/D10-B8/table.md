### 8x8

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.454 (8.170) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.029 (5.406) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.125 (0.654) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.021 (4.122) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.739 (64.140) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.481 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.873 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.117 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.916 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.353 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.332 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.909 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.086 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.899 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.317 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.099 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 15.404 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.351 | 18 | 220,440 (2.204) | yes | - |
| backlog-adp | 15.968 | 19 | 180,366 (1.804) | yes | - |
| backlog-adp-refill | 41.165 | 23 | 180,366 (1.804) | yes | - |
| backlog-owed | 360.532 | 65 | 190,337 (1.903) | yes | - |

Composed maximum over the 4 backlog windows: 220,440 CPU cycles (2.204 ms), backlog.
Over the windows that released their whole load only: 220,440 (2.204 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 202,144 | 2.021 | 20 | 200 | fits | 220,440 | 138 | 0.652 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 745,422 | 7.454 | 20 | 20 | fits | 105,545 | 52 | 0.686 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 191,584 | 1.916 | 20 | 200 | fits | 191,792 | 146 | 0.604 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 633,153 | 6.332 | 20 | 200 | fits | 104,971 | 57 | 0.628 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 187,325 | 1.873 | 20 | 20 | fits | 191,792 | 146 | 0.604 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 811,663 | 8.117 | 20 | 20 | fits | 105,545 | 52 | 0.686 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 190,910 | 1.909 | 20 | 24 | fits | 191,792 | 146 | 0.604 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,316,270 | 13.163 | 20 | 24 | fits | 50,068 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 189,870 | 1.899 | 20 | 50 | fits | 191,792 | 146 | 0.604 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 631,658 | 6.317 | 20 | 50 | fits | 104,971 | 57 | 0.628 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 409,855 | 4.099 | 18 | 18 | fits | 220,440 | 138 | 0.652 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,381,340 | 13.813 | 18 | 18 | fits | 33,379 | 18 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 402,868 | 4.029 | 20 | 20 | fits | 151,341 | 89 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 103,307 | 1.033 | 20 | 200 | fits | 107,989 | 140 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 535,312 | 5.353 | 20 | 200 | fits | 151,341 | 89 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 104,219 | 1.042 | 20 | 20 | fits | 107,989 | 140 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 756,107 | 7.561 | 20 | 20 | fits | 99,434 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 107,804 | 1.078 | 20 | 24 | fits | 107,989 | 140 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,461,145 | 14.611 | 20 | 24 | fits | 75,062 | 37 | 0.747 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 106,764 | 1.068 | 20 | 50 | fits | 107,989 | 140 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 538,988 | 5.390 | 20 | 50 | fits | 151,341 | 89 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 286,675 | 2.867 | 18 | 18 | fits | 180,366 | 140 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,540,384 | 15.404 | 18 | 18 | fits | 34,211 | 15 | 0.805 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,487 | 0.125 | 20 | 20 | fits | 42,854 | 21 | 0.756 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 103,307 | 1.033 | 20 | 200 | fits | 107,989 | 140 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 47,877 | 0.479 | 20 | 200 | fits | 42,854 | 21 | 0.756 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 104,219 | 1.042 | 20 | 20 | fits | 107,989 | 140 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 737,709 | 7.377 | 20 | 20 | fits | 109,861 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 107,804 | 1.078 | 20 | 24 | fits | 107,989 | 140 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,380,202 | 13.802 | 20 | 24 | fits | 63,590 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 106,764 | 1.068 | 20 | 50 | fits | 107,989 | 140 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 520,036 | 5.200 | 20 | 50 | fits | 132,389 | 79 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 286,675 | 2.867 | 18 | 18 | fits | 180,366 | 140 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,482,373 | 14.824 | 18 | 18 | fits | 46,729 | 18 | 0.763 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,373,898 | 63.739 | 20 | 20 | MISS ceiling | 50,205 | 27 | 0.571 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,048,144 | 360.481 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,048,069 | 360.481 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,047,994 | 360.480 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,047,919 | 360.479 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 108,152 | 1.082 | 20 | 200 | fits | 106,659 | 134 | 0.499 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 555,761 | 5.558 | 20 | 200 | fits | 123,824 | 69 | 0.663 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 103,893 | 1.039 | 20 | 20 | fits | 106,659 | 134 | 0.499 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 751,995 | 7.520 | 20 | 20 | fits | 98,630 | 35 | 0.754 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 107,478 | 1.075 | 20 | 24 | fits | 106,659 | 134 | 0.499 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,508,610 | 65.086 | 20 | 24 | MISS ceiling | 31,168 | 23 | 0.557 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 106,438 | 1.064 | 20 | 50 | fits | 106,659 | 134 | 0.499 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 554,266 | 5.543 | 20 | 50 | fits | 123,824 | 69 | 0.663 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 296,320 | 2.963 | 18 | 18 | fits | 190,337 | 138 | 0.650 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,308,310 | 13.083 | 18 | 18 | fits | 34,862 | 18 | 0.792 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
