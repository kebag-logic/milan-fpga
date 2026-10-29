### 8x8

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.642 (8.350) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.327 (5.141) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.176 (0.711) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.010 (4.109) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.686 (64.224) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.434 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.864 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.297 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.906 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.088 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.309 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.900 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.020 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.889 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.295 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 5.124 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 15.599 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.223 | 17 | 220,017 (2.200) | yes | - |
| backlog-adp | 16.181 | 20 | 194,299 (1.943) | yes | - |
| backlog-adp-refill | 41.076 | 29 | 174,835 (1.748) | yes | - |
| backlog-owed | 360.485 | 65 | 189,781 (1.898) | yes | - |

Composed maximum over the 4 backlog windows: 220,017 CPU cycles (2.200 ms), backlog.
Over the windows that released their whole load only: 220,017 (2.200 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 201,018 | 2.010 | 20 | 200 | fits | 220,017 | 138 | 0.651 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 764,201 | 7.642 | 20 | 20 | fits | 96,063 | 46 | 0.673 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 190,625 | 1.906 | 20 | 200 | fits | 190,833 | 146 | 0.602 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 630,947 | 6.309 | 20 | 200 | fits | 104,497 | 57 | 0.625 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 186,366 | 1.864 | 20 | 20 | fits | 190,833 | 146 | 0.602 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 829,677 | 8.297 | 20 | 20 | fits | 96,063 | 46 | 0.673 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 189,951 | 1.900 | 20 | 24 | fits | 190,833 | 146 | 0.602 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,337,442 | 13.374 | 20 | 24 | fits | 50,351 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 188,911 | 1.889 | 20 | 50 | fits | 190,833 | 146 | 0.602 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 629,452 | 6.295 | 20 | 50 | fits | 104,497 | 57 | 0.625 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 408,473 | 4.085 | 18 | 18 | fits | 220,017 | 138 | 0.651 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,368,838 | 13.688 | 18 | 18 | fits | 33,931 | 20 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 332,679 | 3.327 | 20 | 20 | fits | 194,299 | 89 | 0.701 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 102,799 | 1.028 | 20 | 200 | fits | 107,481 | 140 | 0.484 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 508,806 | 5.088 | 20 | 200 | fits | 194,299 | 89 | 0.701 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 103,711 | 1.037 | 20 | 20 | fits | 107,481 | 140 | 0.484 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 733,507 | 7.335 | 20 | 20 | fits | 110,548 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 107,296 | 1.073 | 20 | 24 | fits | 107,481 | 140 | 0.484 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,373,906 | 13.739 | 20 | 24 | fits | 73,358 | 37 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 106,256 | 1.063 | 20 | 50 | fits | 107,481 | 140 | 0.484 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 512,482 | 5.125 | 20 | 50 | fits | 194,299 | 89 | 0.701 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 512,417 | 5.124 | 18 | 18 | fits | 194,299 | 89 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,559,872 | 15.599 | 18 | 18 | fits | 46,723 | 18 | 0.757 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 17,647 | 0.176 | 20 | 20 | fits | 43,016 | 21 | 0.746 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 102,799 | 1.028 | 20 | 200 | fits | 107,481 | 140 | 0.484 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 53,054 | 0.531 | 20 | 200 | fits | 43,016 | 21 | 0.746 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 103,711 | 1.037 | 20 | 20 | fits | 107,481 | 140 | 0.484 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 713,338 | 7.133 | 20 | 20 | fits | 110,466 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 107,296 | 1.073 | 20 | 24 | fits | 107,481 | 140 | 0.484 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,355,379 | 13.554 | 20 | 24 | fits | 74,752 | 37 | 0.744 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 106,256 | 1.063 | 20 | 50 | fits | 107,481 | 140 | 0.484 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 493,018 | 4.930 | 20 | 50 | fits | 174,835 | 79 | 0.704 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 492,953 | 4.930 | 18 | 18 | fits | 174,835 | 79 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,541,313 | 15.413 | 18 | 18 | fits | 46,723 | 18 | 0.757 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,368,617 | 63.686 | 20 | 20 | MISS ceiling | 49,712 | 27 | 0.564 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,043,434 | 360.434 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,043,359 | 360.434 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,043,284 | 360.433 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,043,209 | 360.432 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 112,965 | 1.130 | 20 | 200 | fits | 106,255 | 134 | 0.492 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 558,850 | 5.588 | 20 | 200 | fits | 123,426 | 69 | 0.661 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 108,706 | 1.087 | 20 | 20 | fits | 106,255 | 134 | 0.492 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 754,770 | 7.548 | 20 | 20 | fits | 98,505 | 35 | 0.754 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 112,291 | 1.123 | 20 | 24 | fits | 106,255 | 134 | 0.492 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,502,028 | 65.020 | 20 | 24 | MISS ceiling | 30,883 | 23 | 0.550 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 111,251 | 1.113 | 20 | 50 | fits | 106,255 | 134 | 0.492 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 557,355 | 5.574 | 20 | 50 | fits | 123,426 | 69 | 0.661 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 300,577 | 3.006 | 18 | 18 | fits | 189,781 | 138 | 0.645 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,308,167 | 13.082 | 18 | 18 | fits | 34,920 | 18 | 0.795 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
