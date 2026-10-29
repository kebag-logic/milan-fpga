### 8x8

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 8.291 (8.994) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.319 (5.834) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.142 (0.668) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.195 (4.474) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.510 (64.038) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.520 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 2.062 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.941 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.104 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.781 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.855 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.098 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.794 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.087 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.840 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.450 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 16.391 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.914 | 17 | 236,719 (2.367) | yes | - |
| backlog-adp | 16.966 | 18 | 191,074 (1.911) | yes | - |
| backlog-adp-refill | 41.199 | 24 | 191,074 (1.911) | yes | - |
| backlog-owed | 360.570 | 65 | 197,967 (1.980) | yes | - |

Composed maximum over the 4 backlog windows: 236,719 CPU cycles (2.367 ms), backlog.
Over the windows that released their whole load only: 236,719 (2.367 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 219,510 | 2.195 | 20 | 200 | fits | 236,719 | 136 | 0.690 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 829,105 | 8.291 | 20 | 20 | fits | 101,108 | 44 | 0.643 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 210,439 | 2.104 | 20 | 200 | fits | 210,647 | 144 | 0.638 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 685,515 | 6.855 | 20 | 200 | fits | 111,759 | 55 | 0.609 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 206,180 | 2.062 | 20 | 20 | fits | 210,647 | 144 | 0.638 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 894,133 | 8.941 | 20 | 20 | fits | 101,108 | 44 | 0.643 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 209,765 | 2.098 | 20 | 24 | fits | 210,647 | 144 | 0.638 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,403,164 | 14.032 | 20 | 24 | fits | 50,587 | 29 | 0.679 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 208,725 | 2.087 | 20 | 50 | fits | 210,647 | 144 | 0.638 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 684,020 | 6.840 | 20 | 50 | fits | 111,759 | 55 | 0.609 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 444,989 | 4.450 | 18 | 18 | fits | 236,719 | 136 | 0.690 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,436,884 | 14.369 | 18 | 18 | fits | 36,255 | 20 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 431,934 | 4.319 | 20 | 20 | fits | 164,639 | 87 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 111,869 | 1.119 | 20 | 200 | fits | 116,551 | 138 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 578,141 | 5.781 | 20 | 200 | fits | 164,639 | 87 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 112,781 | 1.128 | 20 | 20 | fits | 116,551 | 138 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 824,839 | 8.248 | 20 | 20 | fits | 112,490 | 34 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 116,366 | 1.164 | 20 | 24 | fits | 116,551 | 138 | 0.446 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,588,523 | 15.885 | 20 | 24 | fits | 68,120 | 29 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 115,326 | 1.153 | 20 | 50 | fits | 116,551 | 138 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 581,817 | 5.818 | 20 | 50 | fits | 164,639 | 87 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 305,945 | 3.059 | 18 | 18 | fits | 191,074 | 138 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,639,146 | 16.391 | 18 | 18 | fits | 53,158 | 20 | 0.783 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 14,164 | 0.142 | 20 | 20 | fits | 43,638 | 21 | 0.728 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 111,869 | 1.119 | 20 | 200 | fits | 116,551 | 138 | 0.446 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 49,192 | 0.492 | 20 | 200 | fits | 43,638 | 21 | 0.728 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 112,781 | 1.128 | 20 | 20 | fits | 116,551 | 138 | 0.446 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 801,086 | 8.011 | 20 | 20 | fits | 120,576 | 44 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 116,366 | 1.164 | 20 | 24 | fits | 116,551 | 138 | 0.446 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,484,985 | 14.850 | 20 | 24 | fits | 78,007 | 35 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 115,326 | 1.153 | 20 | 50 | fits | 116,551 | 138 | 0.446 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 561,469 | 5.615 | 20 | 50 | fits | 144,291 | 77 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 305,945 | 3.059 | 18 | 18 | fits | 191,074 | 138 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,625,626 | 16.256 | 18 | 18 | fits | 36,374 | 15 | 0.786 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,351,000 | 63.510 | 20 | 20 | MISS ceiling | 46,980 | 25 | 0.444 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,051,970 | 360.520 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,051,895 | 360.519 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,051,820 | 360.518 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,051,745 | 360.517 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 122,613 | 1.226 | 20 | 200 | fits | 113,374 | 132 | 0.447 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 603,018 | 6.030 | 20 | 200 | fits | 134,756 | 67 | 0.672 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 118,354 | 1.184 | 20 | 20 | fits | 113,374 | 132 | 0.447 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 804,844 | 8.048 | 20 | 20 | fits | 101,447 | 33 | 0.758 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 121,939 | 1.219 | 20 | 24 | fits | 113,374 | 132 | 0.447 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,479,379 | 64.794 | 20 | 24 | MISS ceiling | 29,657 | 21 | 0.471 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 120,899 | 1.209 | 20 | 50 | fits | 113,374 | 132 | 0.447 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 601,523 | 6.015 | 20 | 50 | fits | 134,756 | 67 | 0.672 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 318,411 | 3.184 | 18 | 18 | fits | 197,967 | 136 | 0.652 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,428,223 | 14.282 | 18 | 18 | fits | 37,554 | 18 | 0.786 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
