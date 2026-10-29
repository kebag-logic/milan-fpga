### 8x8

Clock: CPU 50 MHz, the product's split CPU clock (the Milan clock), bus 100 MHz.

4 of 17 paths and 13 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 13.602 (14.769) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 7.874 (9.886) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.413 (1.369) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 3.644 (6.765) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 66.200 (67.171) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.923 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 3.421 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 14.716 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 3.464 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 9.833 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 11.229 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 3.457 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 68.456 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 3.446 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 11.214 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 9.257 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 27.253 | MISS ceiling | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 25.686 | 19 | 173,282 (3.466) | yes | - |
| backlog-adp | 28.244 | 19 | 160,133 (3.203) | yes | - |
| backlog-adp-refill | 42.276 | 23 | 160,133 (3.203) | yes | - |
| backlog-owed | 360.974 | 64 | 158,772 (3.175) | yes | - |

Composed maximum over the 4 backlog windows: 173,282 CPU cycles (3.466 ms), backlog.
Over the windows that released their whole load only: 173,282 (3.466 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 100,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 302 | 6 | 173,282 (3.466) | OVER the share |
| backlog-adp | 311 | 8 | 160,133 (3.203) | OVER the share |
| backlog-adp-refill | 315 | 8 | 160,133 (3.203) | OVER the share |
| backlog-owed | 358 | 8 | 158,772 (3.175) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 182,224 | 3.644 | 20 | 200 | fits | 164,947 | 129 | 0.612 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 680,083 | 13.602 | 20 | 20 | fits | 88,074 | 46 | 0.688 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 173,178 | 3.464 | 20 | 200 | fits | 173,282 | 146 | 0.599 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 561,451 | 11.229 | 20 | 200 | fits | 97,829 | 57 | 0.677 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 171,049 | 3.421 | 20 | 20 | fits | 173,282 | 146 | 0.599 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 735,817 | 14.716 | 20 | 20 | fits | 88,074 | 46 | 0.688 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 172,841 | 3.457 | 20 | 24 | fits | 173,282 | 146 | 0.599 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,158,781 | 23.176 | 20 | 24 | MISS T_svc | 41,233 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 172,321 | 3.446 | 20 | 50 | fits | 173,282 | 146 | 0.599 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 560,703 | 11.214 | 20 | 50 | fits | 97,829 | 57 | 0.677 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 462,842 | 9.257 | 18 | 18 | fits | 125,801 | 85 | 0.680 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,216,067 | 24.321 | 18 | 18 | MISS ceiling | 28,966 | 18 | 0.708 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 393,716 | 7.874 | 20 | 20 | fits | 105,466 | 74 | 0.630 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 101,307 | 2.026 | 20 | 200 | fits | 103,648 | 140 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 491,650 | 9.833 | 20 | 200 | fits | 105,466 | 74 | 0.630 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 101,763 | 2.035 | 20 | 20 | fits | 103,648 | 140 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 705,667 | 14.113 | 20 | 20 | fits | 94,881 | 34 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 103,556 | 2.071 | 20 | 24 | fits | 103,648 | 140 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,280,672 | 25.613 | 20 | 24 | MISS ceiling | 53,739 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 103,036 | 2.061 | 20 | 50 | fits | 103,648 | 140 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 493,488 | 9.870 | 20 | 50 | fits | 105,466 | 74 | 0.630 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 262,941 | 5.259 | 18 | 18 | fits | 160,133 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,362,657 | 27.253 | 18 | 18 | MISS ceiling | 41,307 | 18 | 0.727 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 20,657 | 0.413 | 20 | 20 | fits | 38,059 | 21 | 0.779 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 101,307 | 2.026 | 20 | 200 | fits | 103,648 | 140 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 52,731 | 1.055 | 20 | 200 | fits | 38,059 | 21 | 0.779 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 101,763 | 2.035 | 20 | 20 | fits | 103,648 | 140 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 687,219 | 13.744 | 20 | 20 | fits | 104,153 | 50 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 103,556 | 2.071 | 20 | 24 | fits | 103,648 | 140 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,226,833 | 24.537 | 20 | 24 | MISS ceiling | 54,031 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 103,036 | 2.061 | 20 | 50 | fits | 103,648 | 140 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 474,988 | 9.500 | 20 | 50 | fits | 86,966 | 64 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 262,941 | 5.259 | 18 | 18 | fits | 160,133 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,339,047 | 26.781 | 18 | 18 | MISS ceiling | 29,717 | 15 | 0.783 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 3,310,020 | 66.200 | 20 | 20 | MISS ceiling | 51,565 | 33 | 0.656 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,046,153 | 360.923 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,046,115 | 360.922 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,046,078 | 360.922 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,046,040 | 360.921 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 110,372 | 2.207 | 20 | 200 | fits | 101,335 | 134 | 0.502 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 512,766 | 10.255 | 20 | 200 | fits | 113,812 | 69 | 0.686 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 108,243 | 2.165 | 20 | 20 | fits | 101,335 | 134 | 0.502 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 684,502 | 13.690 | 20 | 20 | fits | 85,533 | 35 | 0.758 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 110,035 | 2.201 | 20 | 24 | fits | 101,335 | 134 | 0.502 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 3,422,786 | 68.456 | 20 | 24 | MISS ceiling | 25,849 | 23 | 0.518 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 109,515 | 2.190 | 20 | 50 | fits | 101,335 | 134 | 0.502 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 512,018 | 10.240 | 20 | 50 | fits | 113,812 | 69 | 0.686 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 268,060 | 5.361 | 18 | 18 | fits | 158,772 | 133 | 0.658 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,155,704 | 23.114 | 18 | 18 | MISS ceiling | 42,173 | 21 | 0.742 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
