### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.976 (6.469) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.052 (5.486) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.100 (0.651) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.363 (2.374) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.798 (64.175) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.523 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.219 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.674 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.262 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.433 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.255 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 64.802 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.245 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 5.470 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.866 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 14.941 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 10.633 | 20 | 158,929 (1.589) | yes | - |
| backlog-adp | 0 | 15.554 | 19 | 159,592 (1.596) | yes | - |
| backlog-adp-refill | 0 | 41.003 | 28 | 159,592 (1.596) | yes | - |
| backlog-owed | 0 | 360.573 | 63 | 158,209 (1.582) | yes | - |

Composed maximum over the 4 backlog windows: 159,592 CPU cycles (1.596 ms), backlog-adp.
Over the windows that released their whole load only: 159,592 (1.596 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 294 | 0 | 158,929 (1.589) | fits |
| backlog-adp | 313 | 0 | 159,592 (1.596) | fits |
| backlog-adp-refill | 322 | 0 | 159,592 (1.596) | fits |
| backlog-owed | 348 | 0 | 158,209 (1.582) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 266 | 48,491 (0.485) | 2,803 (0.028) |
| backlog-adp | 271 | 48,491 (0.485) | 2,803 (0.028) |
| backlog-adp-refill | 273 | 48,491 (0.485) | 2,803 (0.028) |
| backlog-owed | 305 | 48,491 (0.485) | 2,825 (0.028) |

Longest pass that carries a step: 48,491 CPU cycles (0.485 ms), backlog; longest step: 2,825 (0.028 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 136,277 | 1.363 | 20 | 200 | fits | 110,948 | 104 | 0.505 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 597,636 | 5.976 | 20 | 20 | fits | 78,739 | 44 | 0.510 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 126,204 | 1.262 | 20 | 200 | fits | 126,412 | 138 | 0.510 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 488,185 | 4.882 | 20 | 200 | fits | 92,713 | 55 | 0.542 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 121,945 | 1.219 | 20 | 20 | fits | 126,412 | 138 | 0.510 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 641,583 | 6.416 | 20 | 20 | fits | 78,739 | 44 | 0.510 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 125,530 | 1.255 | 20 | 24 | fits | 126,412 | 138 | 0.510 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 941,812 | 9.418 | 20 | 24 | fits | 29,214 | 29 | 0.455 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 124,490 | 1.245 | 20 | 50 | fits | 126,412 | 138 | 0.510 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 486,690 | 4.867 | 20 | 50 | fits | 92,713 | 55 | 0.542 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 486,625 | 4.866 | 18 | 18 | fits | 92,713 | 55 | 0.542 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 1,009,164 | 10.092 | 18 | 18 | fits | 17,316 | 17 | 0.309 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 405,238 | 4.052 | 20 | 20 | fits | 152,662 | 87 | 0.665 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 111,382 | 1.114 | 20 | 200 | fits | 116,064 | 135 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 543,282 | 5.433 | 20 | 200 | fits | 152,662 | 87 | 0.665 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 112,294 | 1.123 | 20 | 20 | fits | 116,064 | 135 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 767,425 | 7.674 | 20 | 20 | fits | 110,990 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 115,879 | 1.159 | 20 | 24 | fits | 116,064 | 135 | 0.486 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,365,684 | 13.657 | 20 | 24 | fits | 59,212 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 114,839 | 1.148 | 20 | 50 | fits | 116,064 | 135 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 546,958 | 5.470 | 20 | 50 | fits | 152,662 | 87 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 394,231 | 3.942 | 18 | 18 | fits | 159,592 | 102 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,494,111 | 14.941 | 18 | 18 | fits | 35,815 | 14 | 0.820 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 9,962 | 0.100 | 20 | 20 | fits | 43,968 | 20 | 0.768 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 111,382 | 1.114 | 20 | 200 | fits | 116,064 | 135 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 45,451 | 0.455 | 20 | 200 | fits | 43,968 | 20 | 0.768 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 112,294 | 1.123 | 20 | 20 | fits | 116,064 | 135 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 746,221 | 7.462 | 20 | 20 | fits | 110,939 | 44 | 0.663 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 115,879 | 1.159 | 20 | 24 | fits | 116,064 | 135 | 0.486 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 1,355,652 | 13.557 | 20 | 24 | fits | 59,212 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 114,839 | 1.148 | 20 | 50 | fits | 116,064 | 135 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 526,071 | 5.261 | 20 | 50 | fits | 131,775 | 77 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 394,231 | 3.942 | 18 | 18 | fits | 159,592 | 102 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,474,414 | 14.744 | 18 | 18 | fits | 35,896 | 14 | 0.821 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,379,767 | 63.798 | 20 | 20 | MISS ceiling | 49,081 | 25 | 0.617 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,052,280 | 360.523 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,052,205 | 360.522 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,052,130 | 360.521 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,052,055 | 360.521 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 115,731 | 1.157 | 20 | 200 | fits | 112,327 | 129 | 0.487 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 509,583 | 5.096 | 20 | 200 | fits | 124,254 | 67 | 0.654 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 111,472 | 1.115 | 20 | 20 | fits | 112,327 | 129 | 0.487 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 691,314 | 6.913 | 20 | 20 | fits | 91,463 | 33 | 0.747 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 115,057 | 1.151 | 20 | 24 | fits | 112,327 | 129 | 0.487 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,480,207 | 64.802 | 20 | 24 | MISS ceiling | 29,610 | 21 | 0.575 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 114,017 | 1.140 | 20 | 50 | fits | 112,327 | 129 | 0.487 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 508,088 | 5.081 | 20 | 50 | fits | 124,254 | 67 | 0.654 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 383,769 | 3.838 | 18 | 18 | fits | 158,209 | 95 | 0.659 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 1,241,486 | 12.415 | 18 | 18 | fits | 45,493 | 20 | 0.765 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
