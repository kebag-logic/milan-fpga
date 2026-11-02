### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.547 (8.253) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.254 (5.733) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.084 (0.624) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 3.086 (5.240) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.701 (64.225) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.510 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.873 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.200 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.915 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.680 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.349 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.909 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.017 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.898 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.334 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.217 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 16.008 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.653 | 19 | 220,700 (2.207) | yes | - |
| backlog-adp | 16.582 | 19 | 183,148 (1.831) | yes | - |
| backlog-adp-refill | 40.981 | 25 | 183,148 (1.831) | yes | - |
| backlog-owed | 360.561 | 65 | 186,930 (1.869) | yes | - |

Composed maximum over the 4 backlog windows: 220,700 CPU cycles (2.207 ms), backlog.
Over the windows that released their whole load only: 220,700 (2.207 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 302 | 1 | 220,700 (2.207) | OVER the share |
| backlog-adp | 318 | 0 | 183,148 (1.831) | fits |
| backlog-adp-refill | 324 | 0 | 183,148 (1.831) | fits |
| backlog-owed | 359 | 0 | 186,930 (1.869) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 308,635 | 3.086 | 20 | 200 | fits | 220,700 | 115 | 0.688 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 754,653 | 7.547 | 20 | 20 | fits | 108,297 | 52 | 0.677 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 191,536 | 1.915 | 20 | 200 | fits | 191,744 | 134 | 0.601 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 634,888 | 6.349 | 20 | 200 | fits | 111,675 | 57 | 0.651 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 187,277 | 1.873 | 20 | 20 | fits | 191,744 | 134 | 0.601 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 820,033 | 8.200 | 20 | 20 | fits | 108,297 | 52 | 0.677 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 190,862 | 1.909 | 20 | 24 | fits | 191,744 | 134 | 0.601 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,316,476 | 13.165 | 20 | 24 | fits | 49,261 | 31 | 0.688 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 189,822 | 1.898 | 20 | 50 | fits | 191,744 | 134 | 0.601 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 633,393 | 6.334 | 20 | 50 | fits | 111,675 | 57 | 0.651 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 521,653 | 5.217 | 18 | 18 | fits | 220,700 | 115 | 0.688 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,412,309 | 14.123 | 18 | 18 | fits | 32,239 | 18 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 425,359 | 4.254 | 20 | 20 | fits | 160,924 | 89 | 0.673 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 107,558 | 1.076 | 20 | 200 | fits | 112,240 | 128 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 568,048 | 5.680 | 20 | 200 | fits | 160,924 | 89 | 0.673 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 108,470 | 1.085 | 20 | 20 | fits | 112,240 | 128 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 805,909 | 8.059 | 20 | 20 | fits | 118,097 | 46 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 112,055 | 1.121 | 20 | 24 | fits | 112,240 | 128 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,471,953 | 14.720 | 20 | 24 | fits | 74,776 | 37 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 111,015 | 1.110 | 20 | 50 | fits | 112,240 | 128 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 571,724 | 5.717 | 20 | 50 | fits | 160,924 | 89 | 0.673 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 410,735 | 4.107 | 18 | 18 | fits | 183,148 | 122 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,600,755 | 16.008 | 18 | 18 | fits | 34,141 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,423 | 0.084 | 20 | 20 | fits | 43,858 | 21 | 0.777 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 107,558 | 1.076 | 20 | 200 | fits | 112,240 | 128 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 44,672 | 0.447 | 20 | 200 | fits | 43,858 | 21 | 0.777 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 108,470 | 1.085 | 20 | 20 | fits | 112,240 | 128 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 785,562 | 7.856 | 20 | 20 | fits | 117,939 | 46 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 112,055 | 1.121 | 20 | 24 | fits | 112,240 | 128 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,465,662 | 14.657 | 20 | 24 | fits | 73,934 | 37 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 111,015 | 1.110 | 20 | 50 | fits | 112,240 | 128 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 551,659 | 5.517 | 20 | 50 | fits | 140,859 | 79 | 0.673 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 410,735 | 4.107 | 18 | 18 | fits | 183,148 | 122 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,559,469 | 15.595 | 18 | 18 | fits | 47,519 | 18 | 0.724 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,370,133 | 63.701 | 20 | 20 | MISS ceiling | 48,877 | 27 | 0.566 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,051,028 | 360.510 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,050,953 | 360.510 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,050,878 | 360.509 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,050,803 | 360.508 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 117,428 | 1.174 | 20 | 200 | fits | 109,301 | 122 | 0.506 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 542,669 | 5.427 | 20 | 200 | fits | 131,600 | 69 | 0.674 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 113,169 | 1.132 | 20 | 20 | fits | 109,301 | 122 | 0.506 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 739,909 | 7.399 | 20 | 20 | fits | 99,050 | 35 | 0.749 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 116,754 | 1.168 | 20 | 24 | fits | 109,301 | 122 | 0.506 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,501,702 | 65.017 | 20 | 24 | MISS ceiling | 30,724 | 23 | 0.555 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 115,714 | 1.157 | 20 | 50 | fits | 109,301 | 122 | 0.506 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 541,174 | 5.412 | 20 | 50 | fits | 131,600 | 69 | 0.674 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 409,509 | 4.095 | 18 | 18 | fits | 186,930 | 115 | 0.664 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,325,591 | 13.256 | 18 | 18 | fits | 47,915 | 21 | 0.724 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
