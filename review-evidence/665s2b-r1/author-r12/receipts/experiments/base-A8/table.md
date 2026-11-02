### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.634 (8.340) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.252 (5.732) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.084 (0.624) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.030 (4.144) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.658 (64.182) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.481 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.892 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.287 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.934 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.679 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.437 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.928 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.974 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.917 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.422 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.121 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 15.769 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.418 | 18 | 220,796 (2.208) | yes | - |
| backlog-adp | 16.345 | 18 | 179,993 (1.800) | yes | - |
| backlog-adp-refill | 40.981 | 25 | 179,993 (1.800) | yes | - |
| backlog-owed | 360.532 | 65 | 190,223 (1.902) | yes | - |

Composed maximum over the 4 backlog windows: 220,796 CPU cycles (2.208 ms), backlog.
Over the windows that released their whole load only: 220,796 (2.208 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 301 | 1 | 220,796 (2.208) | OVER the share |
| backlog-adp | 317 | 0 | 179,993 (1.800) | fits |
| backlog-adp-refill | 324 | 0 | 179,993 (1.800) | fits |
| backlog-owed | 359 | 0 | 190,223 (1.902) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 203,027 | 2.030 | 20 | 200 | fits | 220,796 | 138 | 0.647 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 763,404 | 7.634 | 20 | 20 | fits | 108,305 | 52 | 0.676 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 193,431 | 1.934 | 20 | 200 | fits | 193,639 | 146 | 0.589 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 643,709 | 6.437 | 20 | 200 | fits | 109,105 | 57 | 0.631 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 189,172 | 1.892 | 20 | 20 | fits | 193,639 | 146 | 0.589 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 828,681 | 8.287 | 20 | 20 | fits | 108,305 | 52 | 0.676 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 192,757 | 1.928 | 20 | 24 | fits | 193,639 | 146 | 0.589 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,325,196 | 13.252 | 20 | 24 | fits | 49,261 | 31 | 0.688 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 191,717 | 1.917 | 20 | 50 | fits | 193,639 | 146 | 0.589 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 642,214 | 6.422 | 20 | 50 | fits | 109,105 | 57 | 0.631 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 412,058 | 4.121 | 18 | 18 | fits | 220,796 | 138 | 0.647 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,388,790 | 13.888 | 18 | 18 | fits | 32,396 | 18 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 425,202 | 4.252 | 20 | 20 | fits | 160,923 | 89 | 0.673 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 109,531 | 1.095 | 20 | 200 | fits | 114,213 | 140 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 567,891 | 5.679 | 20 | 200 | fits | 160,923 | 89 | 0.673 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 110,443 | 1.104 | 20 | 20 | fits | 114,213 | 140 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 805,750 | 8.057 | 20 | 20 | fits | 118,096 | 46 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 114,028 | 1.140 | 20 | 24 | fits | 114,213 | 140 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,483,133 | 14.831 | 20 | 24 | fits | 73,838 | 37 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 112,988 | 1.130 | 20 | 50 | fits | 114,213 | 140 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 571,567 | 5.716 | 20 | 50 | fits | 160,923 | 89 | 0.673 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 410,579 | 4.106 | 18 | 18 | fits | 179,993 | 104 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,576,940 | 15.769 | 18 | 18 | fits | 47,519 | 18 | 0.724 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,386 | 0.084 | 20 | 20 | fits | 43,859 | 21 | 0.777 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 109,531 | 1.095 | 20 | 200 | fits | 114,213 | 140 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 44,635 | 0.446 | 20 | 200 | fits | 43,859 | 21 | 0.777 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 110,443 | 1.104 | 20 | 20 | fits | 114,213 | 140 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 785,403 | 7.854 | 20 | 20 | fits | 117,938 | 46 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 114,028 | 1.140 | 20 | 24 | fits | 114,213 | 140 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,465,498 | 14.655 | 20 | 24 | fits | 73,930 | 37 | 0.729 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 112,988 | 1.130 | 20 | 50 | fits | 114,213 | 140 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 551,502 | 5.515 | 20 | 50 | fits | 140,858 | 79 | 0.673 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 410,579 | 4.106 | 18 | 18 | fits | 179,993 | 104 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,559,305 | 15.593 | 18 | 18 | fits | 47,519 | 18 | 0.724 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,365,797 | 63.658 | 20 | 20 | MISS ceiling | 48,878 | 27 | 0.566 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,048,087 | 360.481 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,048,012 | 360.480 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,047,937 | 360.479 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,047,862 | 360.479 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 119,473 | 1.195 | 20 | 200 | fits | 111,196 | 134 | 0.492 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 579,340 | 5.793 | 20 | 200 | fits | 129,775 | 69 | 0.658 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 115,214 | 1.152 | 20 | 20 | fits | 111,196 | 134 | 0.492 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 776,578 | 7.766 | 20 | 20 | fits | 99,049 | 35 | 0.749 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 118,799 | 1.188 | 20 | 24 | fits | 111,196 | 134 | 0.492 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,497,369 | 64.974 | 20 | 24 | MISS ceiling | 30,725 | 23 | 0.555 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 117,759 | 1.178 | 20 | 50 | fits | 111,196 | 134 | 0.492 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 577,845 | 5.778 | 20 | 50 | fits | 129,775 | 69 | 0.658 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 307,527 | 3.075 | 18 | 18 | fits | 190,223 | 138 | 0.644 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,338,551 | 13.386 | 18 | 18 | fits | 34,607 | 18 | 0.779 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
