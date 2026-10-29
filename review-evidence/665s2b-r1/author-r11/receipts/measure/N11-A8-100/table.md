### 8x8

Clock: CPU 100 MHz, a labelled option: not the product's split CPU clock, 50 MHz, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 8.127 (8.846) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.126 (5.838) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.087 (0.635) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.094 (4.279) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.702 (64.082) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.379 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.947 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.793 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.989 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.785 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.666 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.983 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.035 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.972 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.651 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.255 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 16.949 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.823 | 17 | 228,766 (2.288) | yes | - |
| backlog-adp | 17.533 | 20 | 184,481 (1.845) | yes | - |
| backlog-adp-refill | 40.998 | 29 | 167,403 (1.674) | yes | - |
| backlog-owed | 360.430 | 64 | 197,674 (1.977) | yes | - |

Composed maximum over the 4 backlog windows: 228,766 CPU cycles (2.288 ms), backlog.
Over the windows that released their whole load only: 228,766 (2.288 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 300 | 1 | 228,766 (2.288) | OVER the share |
| backlog-adp | 322 | 0 | 184,481 (1.845) | fits |
| backlog-adp-refill | 331 | 0 | 167,403 (1.674) | fits |
| backlog-owed | 358 | 0 | 197,674 (1.977) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 209,421 | 2.094 | 20 | 200 | fits | 228,766 | 138 | 0.649 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 812,677 | 8.127 | 20 | 20 | fits | 103,351 | 46 | 0.660 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 198,948 | 1.989 | 20 | 200 | fits | 199,156 | 146 | 0.589 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 666,572 | 6.666 | 20 | 200 | fits | 113,238 | 57 | 0.630 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 194,689 | 1.947 | 20 | 20 | fits | 199,156 | 146 | 0.589 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 879,312 | 8.793 | 20 | 20 | fits | 103,351 | 46 | 0.660 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 198,274 | 1.983 | 20 | 24 | fits | 199,156 | 146 | 0.589 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,395,938 | 13.959 | 20 | 24 | fits | 51,257 | 31 | 0.682 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 197,234 | 1.972 | 20 | 50 | fits | 199,156 | 146 | 0.589 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 665,077 | 6.651 | 20 | 50 | fits | 113,238 | 57 | 0.630 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 425,545 | 4.255 | 18 | 18 | fits | 228,766 | 138 | 0.649 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,428,617 | 14.286 | 18 | 18 | fits | 35,214 | 20 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 412,553 | 4.126 | 20 | 20 | fits | 184,481 | 89 | 0.693 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 113,176 | 1.132 | 20 | 200 | fits | 117,858 | 140 | 0.492 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 578,525 | 5.785 | 20 | 200 | fits | 184,481 | 89 | 0.693 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 114,088 | 1.141 | 20 | 20 | fits | 117,858 | 140 | 0.492 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 826,611 | 8.266 | 20 | 20 | fits | 122,288 | 46 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 117,673 | 1.177 | 20 | 24 | fits | 117,858 | 140 | 0.492 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,509,563 | 15.096 | 20 | 24 | fits | 69,169 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 116,633 | 1.166 | 20 | 50 | fits | 117,858 | 140 | 0.492 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 582,201 | 5.822 | 20 | 50 | fits | 184,481 | 89 | 0.693 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 283,581 | 2.836 | 18 | 18 | fits | 167,403 | 145 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,694,911 | 16.949 | 18 | 18 | fits | 35,671 | 15 | 0.774 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,702 | 0.087 | 20 | 20 | fits | 44,827 | 21 | 0.772 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 113,176 | 1.132 | 20 | 200 | fits | 117,858 | 140 | 0.492 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 45,665 | 0.457 | 20 | 200 | fits | 44,827 | 21 | 0.772 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 114,088 | 1.141 | 20 | 20 | fits | 117,858 | 140 | 0.492 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 805,676 | 8.057 | 20 | 20 | fits | 121,973 | 46 | 0.670 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 117,673 | 1.177 | 20 | 24 | fits | 117,858 | 140 | 0.492 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,508,049 | 15.080 | 20 | 24 | fits | 68,698 | 31 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 116,633 | 1.166 | 20 | 50 | fits | 117,858 | 140 | 0.492 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 561,698 | 5.617 | 20 | 50 | fits | 163,978 | 79 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 283,581 | 2.836 | 18 | 18 | fits | 167,403 | 145 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,657,221 | 16.572 | 18 | 18 | fits | 50,042 | 18 | 0.718 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,370,164 | 63.702 | 20 | 20 | MISS ceiling | 49,953 | 27 | 0.548 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,037,899 | 360.379 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,037,824 | 360.378 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,037,749 | 360.377 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,037,674 | 360.377 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 117,904 | 1.179 | 20 | 200 | fits | 114,903 | 134 | 0.496 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 595,968 | 5.960 | 20 | 200 | fits | 134,970 | 69 | 0.658 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 113,645 | 1.136 | 20 | 20 | fits | 114,903 | 134 | 0.496 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 800,721 | 8.007 | 20 | 20 | fits | 102,786 | 35 | 0.749 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 117,230 | 1.172 | 20 | 24 | fits | 114,903 | 134 | 0.496 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,503,469 | 65.035 | 20 | 24 | MISS ceiling | 30,946 | 23 | 0.521 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 116,190 | 1.162 | 20 | 50 | fits | 114,903 | 134 | 0.496 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 594,473 | 5.945 | 20 | 50 | fits | 134,970 | 69 | 0.658 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 313,409 | 3.134 | 18 | 18 | fits | 197,674 | 138 | 0.646 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,365,504 | 13.655 | 18 | 18 | fits | 50,320 | 21 | 0.724 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
