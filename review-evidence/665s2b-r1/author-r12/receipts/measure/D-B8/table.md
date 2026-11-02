### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.207 (6.881) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.105 (5.133) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.087 (0.605) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.354 (2.326) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.680 (64.214) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.377 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.217 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.301 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.259 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.080 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.068 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.253 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.007 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.242 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 5.117 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.001 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 14.809 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 13.316 | 20 | 148,742 (1.487) | yes | - |
| backlog-adp | 0 | 15.366 | 19 | 174,885 (1.749) | yes | - |
| backlog-adp-refill | 0 | 41.111 | 24 | 174,885 (1.749) | yes | - |
| backlog-owed | 0 | 360.428 | 66 | 177,215 (1.772) | yes | - |

Composed maximum over the 4 backlog windows: 177,215 CPU cycles (1.772 ms), backlog-owed.
Over the windows that released their whole load only: 177,215 (1.772 ms), backlog-owed.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 306 | 0 | 148,742 (1.487) | fits |
| backlog-adp | 314 | 0 | 174,885 (1.749) | fits |
| backlog-adp-refill | 319 | 0 | 174,885 (1.749) | fits |
| backlog-owed | 363 | 0 | 177,215 (1.772) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 135,373 | 1.354 | 20 | 200 | fits | 106,489 | 125 | 0.535 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 620,677 | 6.207 | 20 | 20 | fits | 91,731 | 46 | 0.660 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 125,926 | 1.259 | 20 | 200 | fits | 126,134 | 143 | 0.524 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 501,686 | 5.017 | 20 | 200 | fits | 121,138 | 57 | 0.679 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 121,667 | 1.217 | 20 | 20 | fits | 126,134 | 143 | 0.524 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 682,793 | 6.828 | 20 | 20 | fits | 91,731 | 46 | 0.660 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 125,252 | 1.253 | 20 | 24 | fits | 126,134 | 143 | 0.524 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,152,076 | 11.521 | 20 | 24 | fits | 47,115 | 31 | 0.695 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 124,212 | 1.242 | 20 | 50 | fits | 126,134 | 143 | 0.524 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 500,191 | 5.002 | 20 | 50 | fits | 121,138 | 57 | 0.679 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 500,126 | 5.001 | 18 | 18 | fits | 121,138 | 57 | 0.679 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,278,668 | 12.787 | 18 | 18 | fits | 31,915 | 18 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 410,521 | 4.105 | 20 | 20 | fits | 106,314 | 74 | 0.593 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 99,319 | 0.993 | 20 | 200 | fits | 104,001 | 140 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 507,981 | 5.080 | 20 | 200 | fits | 106,314 | 74 | 0.593 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 100,231 | 1.002 | 20 | 20 | fits | 104,001 | 140 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 730,093 | 7.301 | 20 | 20 | fits | 96,474 | 34 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 103,816 | 1.038 | 20 | 24 | fits | 104,001 | 140 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,404,582 | 14.046 | 20 | 24 | fits | 60,809 | 31 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 102,776 | 1.028 | 20 | 50 | fits | 104,001 | 140 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 511,657 | 5.117 | 20 | 50 | fits | 106,314 | 74 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 277,206 | 2.772 | 18 | 18 | fits | 174,885 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,480,873 | 14.809 | 18 | 18 | fits | 43,160 | 21 | 0.827 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,654 | 0.087 | 20 | 20 | fits | 41,496 | 21 | 0.756 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 99,319 | 0.993 | 20 | 200 | fits | 104,001 | 140 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 43,264 | 0.433 | 20 | 200 | fits | 41,496 | 21 | 0.756 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 100,231 | 1.002 | 20 | 20 | fits | 104,001 | 140 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 711,590 | 7.116 | 20 | 20 | fits | 106,027 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 103,816 | 1.038 | 20 | 24 | fits | 104,001 | 140 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,327,550 | 13.275 | 20 | 24 | fits | 60,974 | 31 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 102,776 | 1.028 | 20 | 50 | fits | 104,001 | 140 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 492,909 | 4.929 | 20 | 50 | fits | 87,566 | 64 | 0.581 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 277,206 | 2.772 | 18 | 18 | fits | 174,885 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,417,272 | 14.173 | 18 | 18 | fits | 45,643 | 18 | 0.772 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,368,035 | 63.680 | 20 | 20 | MISS ceiling | 49,080 | 27 | 0.585 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,037,695 | 360.377 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,037,620 | 360.376 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,037,545 | 360.375 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,037,470 | 360.375 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 108,524 | 1.085 | 20 | 200 | fits | 102,533 | 134 | 0.493 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 506,780 | 5.068 | 20 | 200 | fits | 120,750 | 69 | 0.676 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 104,265 | 1.043 | 20 | 20 | fits | 102,533 | 134 | 0.493 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 695,296 | 6.953 | 20 | 20 | fits | 94,649 | 35 | 0.753 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 107,850 | 1.079 | 20 | 24 | fits | 102,533 | 134 | 0.493 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,500,732 | 65.007 | 20 | 24 | MISS ceiling | 30,745 | 23 | 0.578 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 106,810 | 1.068 | 20 | 50 | fits | 102,533 | 134 | 0.493 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 505,285 | 5.053 | 20 | 50 | fits | 120,750 | 69 | 0.676 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 384,470 | 3.845 | 18 | 18 | fits | 177,215 | 97 | 0.685 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,276,054 | 12.761 | 18 | 18 | fits | 33,607 | 18 | 0.798 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
