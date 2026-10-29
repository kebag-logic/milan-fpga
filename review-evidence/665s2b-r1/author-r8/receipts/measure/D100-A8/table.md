### 8x8

4 of 17 paths and 13 of 49 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.982 (8.675) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.235 (5.648) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.243 (0.771) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.149 (4.391) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.779 (64.175) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.450 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 2.012 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.622 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.055 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.595 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.640 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.048 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.789 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.038 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.625 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.367 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 15.807 | MISS T_svc | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.438 | 17 | 233,392 (2.334) | yes | - |
| backlog-adp | 16.397 | 19 | 191,907 (1.919) | yes | - |
| backlog-adp-refill | 41.139 | 28 | 191,907 (1.919) | yes | - |
| backlog-owed | 360.501 | 64 | 193,673 (1.937) | yes | - |

Composed maximum over the 4 backlog windows: 233,392 CPU cycles (2.334 ms), backlog.
Over the windows that released their whole load only: 233,392 (2.334 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 214,854 | 2.149 | 10 | 200 | fits | 233,392 | 136 | 0.699 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 798,157 | 7.982 | 10 | 20 | fits | 95,546 | 44 | 0.646 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 205,491 | 2.055 | 10 | 200 | fits | 205,699 | 144 | 0.637 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 664,042 | 6.640 | 10 | 200 | fits | 106,425 | 55 | 0.616 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 201,232 | 2.012 | 10 | 20 | fits | 205,699 | 144 | 0.637 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 862,168 | 8.622 | 10 | 20 | fits | 95,546 | 44 | 0.646 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 204,817 | 2.048 | 10 | 24 | fits | 205,699 | 144 | 0.637 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,356,519 | 13.565 | 10 | 24 | MISS T_svc | 49,033 | 29 | 0.682 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 203,777 | 2.038 | 10 | 50 | fits | 205,699 | 144 | 0.637 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 662,547 | 6.625 | 10 | 50 | fits | 106,425 | 55 | 0.616 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 436,714 | 4.367 | 10 | 18 | fits | 233,392 | 136 | 0.699 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,388,828 | 13.888 | 10 | 18 | MISS T_svc | 34,844 | 20 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 423,526 | 4.235 | 10 | 20 | fits | 155,023 | 87 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 105,204 | 1.052 | 10 | 200 | fits | 109,886 | 138 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 559,544 | 5.595 | 10 | 200 | fits | 155,023 | 87 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 106,116 | 1.061 | 10 | 20 | fits | 109,886 | 138 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 784,835 | 7.848 | 10 | 20 | fits | 111,712 | 44 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 109,701 | 1.097 | 10 | 24 | fits | 109,886 | 138 | 0.449 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,446,980 | 14.470 | 10 | 24 | MISS T_svc | 75,563 | 35 | 0.740 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 108,661 | 1.087 | 10 | 50 | fits | 109,886 | 138 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 563,220 | 5.632 | 10 | 50 | fits | 155,023 | 87 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 300,113 | 3.001 | 10 | 18 | fits | 191,907 | 140 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,580,741 | 15.807 | 10 | 18 | MISS T_svc | 35,630 | 15 | 0.802 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 24,346 | 0.243 | 10 | 20 | fits | 43,073 | 21 | 0.718 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 105,204 | 1.052 | 10 | 200 | fits | 109,886 | 138 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 58,885 | 0.589 | 10 | 200 | fits | 43,073 | 21 | 0.718 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 106,116 | 1.061 | 10 | 20 | fits | 109,886 | 138 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 764,220 | 7.642 | 10 | 20 | fits | 111,668 | 44 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 109,701 | 1.097 | 10 | 24 | fits | 109,886 | 138 | 0.449 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,365,421 | 13.654 | 10 | 24 | MISS T_svc | 33,542 | 20 | 0.612 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 108,661 | 1.087 | 10 | 50 | fits | 109,886 | 138 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 542,547 | 5.425 | 10 | 50 | fits | 134,350 | 77 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 300,113 | 3.001 | 10 | 18 | fits | 191,907 | 140 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,570,397 | 15.704 | 10 | 18 | MISS T_svc | 48,971 | 18 | 0.774 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,377,879 | 63.779 | 10 | 20 | MISS ceiling | 47,610 | 25 | 0.454 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,045,042 | 360.450 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,044,967 | 360.450 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,044,892 | 360.449 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,044,817 | 360.448 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 108,645 | 1.086 | 10 | 200 | fits | 107,818 | 132 | 0.452 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 563,919 | 5.639 | 10 | 200 | fits | 125,341 | 67 | 0.662 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 104,386 | 1.044 | 10 | 20 | fits | 107,818 | 132 | 0.452 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 760,342 | 7.603 | 10 | 20 | fits | 98,800 | 33 | 0.745 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 107,971 | 1.080 | 10 | 24 | fits | 107,818 | 132 | 0.452 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,478,873 | 64.789 | 10 | 24 | MISS ceiling | 30,505 | 21 | 0.491 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 106,931 | 1.069 | 10 | 50 | fits | 107,818 | 132 | 0.452 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 562,424 | 5.624 | 10 | 50 | fits | 125,341 | 67 | 0.662 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 300,149 | 3.001 | 10 | 18 | fits | 193,673 | 136 | 0.662 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,319,927 | 13.199 | 10 | 18 | MISS T_svc | 49,880 | 21 | 0.769 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
