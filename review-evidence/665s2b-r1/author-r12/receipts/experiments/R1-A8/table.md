### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.610 (7.120) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.304 (5.768) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.230 (0.772) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.438 (2.470) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.620 (64.148) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.471 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.301 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 8.080 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.343 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.715 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.813 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.336 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.931 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.326 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 5.798 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.264 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 15.972 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 13.949 | 20 | 155,330 (1.553) | yes | - |
| backlog-adp | 16.549 | 19 | 191,593 (1.916) | yes | - |
| backlog-adp-refill | 41.134 | 29 | 191,593 (1.916) | yes | - |
| backlog-owed | 360.521 | 64 | 190,451 (1.905) | yes | - |

Composed maximum over the 4 backlog windows: 191,593 CPU cycles (1.916 ms), backlog-adp.
Over the windows that released their whole load only: 191,593 (1.916 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 303 | 0 | 155,330 (1.553) | fits |
| backlog-adp | 323 | 0 | 191,593 (1.916) | fits |
| backlog-adp-refill | 333 | 0 | 191,593 (1.916) | fits |
| backlog-owed | 358 | 0 | 190,451 (1.905) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 143,790 | 1.438 | 20 | 200 | fits | 112,443 | 125 | 0.523 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 661,009 | 6.610 | 20 | 20 | fits | 80,768 | 37 | 0.616 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 134,315 | 1.343 | 20 | 200 | fits | 134,523 | 143 | 0.531 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 527,985 | 5.280 | 20 | 200 | fits | 126,506 | 57 | 0.677 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 130,056 | 1.301 | 20 | 20 | fits | 134,523 | 143 | 0.531 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 706,692 | 7.067 | 20 | 20 | fits | 80,768 | 37 | 0.616 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 133,641 | 1.336 | 20 | 24 | fits | 134,523 | 143 | 0.531 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,213,931 | 12.139 | 20 | 24 | fits | 49,109 | 31 | 0.683 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 132,601 | 1.326 | 20 | 50 | fits | 134,523 | 143 | 0.531 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 526,490 | 5.265 | 20 | 50 | fits | 126,506 | 57 | 0.677 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 526,425 | 5.264 | 18 | 18 | fits | 126,506 | 57 | 0.677 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,341,731 | 13.417 | 18 | 18 | fits | 32,194 | 18 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 430,414 | 4.304 | 20 | 20 | fits | 159,394 | 89 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 109,680 | 1.097 | 20 | 200 | fits | 114,362 | 140 | 0.492 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 571,463 | 5.715 | 20 | 200 | fits | 159,394 | 89 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 110,592 | 1.106 | 20 | 20 | fits | 114,362 | 140 | 0.492 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 807,958 | 8.080 | 20 | 20 | fits | 117,009 | 46 | 0.661 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 114,177 | 1.142 | 20 | 24 | fits | 114,362 | 140 | 0.492 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,468,873 | 14.689 | 20 | 24 | fits | 74,801 | 37 | 0.725 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 113,137 | 1.131 | 20 | 50 | fits | 114,362 | 140 | 0.492 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 575,139 | 5.751 | 20 | 50 | fits | 159,394 | 89 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 304,275 | 3.043 | 18 | 18 | fits | 191,593 | 151 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,597,166 | 15.972 | 18 | 18 | fits | 34,154 | 15 | 0.769 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 23,020 | 0.230 | 20 | 20 | fits | 43,756 | 21 | 0.770 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 109,680 | 1.097 | 20 | 200 | fits | 114,362 | 140 | 0.492 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 59,354 | 0.594 | 20 | 200 | fits | 43,756 | 21 | 0.770 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 110,592 | 1.106 | 20 | 20 | fits | 114,362 | 140 | 0.492 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 787,475 | 7.875 | 20 | 20 | fits | 116,898 | 46 | 0.660 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 114,177 | 1.142 | 20 | 24 | fits | 114,362 | 140 | 0.492 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,387,100 | 13.871 | 20 | 24 | fits | 33,340 | 22 | 0.634 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 113,137 | 1.131 | 20 | 50 | fits | 114,362 | 140 | 0.492 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 555,054 | 5.551 | 20 | 50 | fits | 139,309 | 79 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 304,275 | 3.043 | 18 | 18 | fits | 191,593 | 151 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,585,717 | 15.857 | 18 | 18 | fits | 47,126 | 18 | 0.686 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,361,951 | 63.620 | 20 | 20 | MISS ceiling | 48,732 | 27 | 0.549 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,047,074 | 360.471 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,046,999 | 360.470 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,046,924 | 360.469 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,046,849 | 360.468 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 123,412 | 1.234 | 20 | 200 | fits | 110,721 | 134 | 0.490 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 581,297 | 5.813 | 20 | 200 | fits | 128,843 | 69 | 0.650 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 119,153 | 1.192 | 20 | 20 | fits | 110,721 | 134 | 0.490 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 776,196 | 7.762 | 20 | 20 | fits | 97,716 | 35 | 0.731 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 122,738 | 1.227 | 20 | 24 | fits | 110,721 | 134 | 0.490 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,493,118 | 64.931 | 20 | 24 | MISS ceiling | 30,497 | 23 | 0.529 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 121,698 | 1.217 | 20 | 50 | fits | 110,721 | 134 | 0.490 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 579,802 | 5.798 | 20 | 50 | fits | 128,843 | 69 | 0.650 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 311,694 | 3.117 | 18 | 18 | fits | 190,451 | 138 | 0.642 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,306,816 | 13.068 | 18 | 18 | fits | 47,260 | 21 | 0.690 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
