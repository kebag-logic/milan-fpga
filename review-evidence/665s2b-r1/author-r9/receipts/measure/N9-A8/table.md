### 8x8

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.866 (8.564) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.231 (5.747) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.129 (0.636) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.152 (4.371) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.439 (63.939) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.393 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 2.019 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.511 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.061 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.694 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.675 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.054 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.662 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.044 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.660 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.347 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 16.298 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.634 | 18 | 230,763 (2.308) | yes | - |
| backlog-adp | 16.841 | 19 | 182,325 (1.823) | yes | - |
| backlog-adp-refill | 40.974 | 27 | 182,325 (1.823) | yes | - |
| backlog-owed | 360.443 | 64 | 192,968 (1.930) | yes | - |

Composed maximum over the 4 backlog windows: 230,763 CPU cycles (2.308 ms), backlog.
Over the windows that released their whole load only: 230,763 (2.308 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 215,189 | 2.152 | 20 | 200 | fits | 230,763 | 136 | 0.689 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 786,583 | 7.866 | 20 | 20 | fits | 108,385 | 50 | 0.656 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 206,118 | 2.061 | 20 | 200 | fits | 206,326 | 144 | 0.639 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 667,504 | 6.675 | 20 | 200 | fits | 108,955 | 55 | 0.610 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 201,859 | 2.019 | 20 | 20 | fits | 206,326 | 144 | 0.639 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 851,121 | 8.511 | 20 | 20 | fits | 108,385 | 50 | 0.656 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 205,444 | 2.054 | 20 | 24 | fits | 206,326 | 144 | 0.639 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,346,971 | 13.470 | 20 | 24 | fits | 49,257 | 29 | 0.680 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 204,404 | 2.044 | 20 | 50 | fits | 206,326 | 144 | 0.639 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 666,009 | 6.660 | 20 | 50 | fits | 108,955 | 55 | 0.610 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 434,712 | 4.347 | 18 | 18 | fits | 230,763 | 136 | 0.689 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,413,073 | 14.131 | 18 | 18 | fits | 33,839 | 18 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 423,075 | 4.231 | 20 | 20 | fits | 164,800 | 87 | 0.683 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 107,583 | 1.076 | 20 | 200 | fits | 112,265 | 138 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 569,410 | 5.694 | 20 | 200 | fits | 164,800 | 87 | 0.683 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 108,495 | 1.085 | 20 | 20 | fits | 112,265 | 138 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 811,880 | 8.119 | 20 | 20 | fits | 119,948 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 112,080 | 1.121 | 20 | 24 | fits | 112,265 | 138 | 0.440 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,491,799 | 14.918 | 20 | 24 | fits | 76,782 | 35 | 0.747 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 111,040 | 1.110 | 20 | 50 | fits | 112,265 | 138 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 573,086 | 5.731 | 20 | 50 | fits | 164,800 | 87 | 0.683 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 408,221 | 4.082 | 18 | 18 | fits | 182,325 | 102 | 0.660 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,629,796 | 16.298 | 18 | 18 | fits | 35,607 | 15 | 0.789 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,882 | 0.129 | 20 | 20 | fits | 42,729 | 21 | 0.740 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 107,583 | 1.076 | 20 | 200 | fits | 112,265 | 138 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 46,890 | 0.469 | 20 | 200 | fits | 42,729 | 21 | 0.740 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 108,495 | 1.085 | 20 | 20 | fits | 112,265 | 138 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 791,229 | 7.912 | 20 | 20 | fits | 119,904 | 44 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 112,080 | 1.121 | 20 | 24 | fits | 112,265 | 138 | 0.440 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,488,163 | 14.882 | 20 | 24 | fits | 76,155 | 35 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 111,040 | 1.110 | 20 | 50 | fits | 112,265 | 138 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 552,583 | 5.526 | 20 | 50 | fits | 144,297 | 77 | 0.680 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 408,221 | 4.082 | 18 | 18 | fits | 182,325 | 102 | 0.660 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,589,369 | 15.894 | 18 | 18 | fits | 51,323 | 18 | 0.787 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,343,909 | 63.439 | 20 | 20 | MISS ceiling | 45,436 | 25 | 0.444 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,039,259 | 360.393 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,039,184 | 360.392 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,039,109 | 360.391 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,039,034 | 360.390 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 114,179 | 1.142 | 20 | 200 | fits | 108,699 | 132 | 0.446 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 582,018 | 5.820 | 20 | 200 | fits | 132,173 | 67 | 0.675 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 109,920 | 1.099 | 20 | 20 | fits | 108,699 | 132 | 0.446 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 780,902 | 7.809 | 20 | 20 | fits | 100,197 | 33 | 0.761 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 113,505 | 1.135 | 20 | 24 | fits | 108,699 | 132 | 0.446 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,466,239 | 64.662 | 20 | 24 | MISS ceiling | 28,113 | 21 | 0.471 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 112,465 | 1.125 | 20 | 50 | fits | 108,699 | 132 | 0.446 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 580,523 | 5.805 | 20 | 50 | fits | 132,173 | 67 | 0.675 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 304,978 | 3.050 | 18 | 18 | fits | 192,968 | 136 | 0.654 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,362,203 | 13.622 | 18 | 18 | fits | 52,007 | 21 | 0.784 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
