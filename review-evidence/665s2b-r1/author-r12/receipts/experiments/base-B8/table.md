### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.659 (8.363) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.392 (5.858) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.117 (0.639) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.037 (4.159) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.849 (64.236) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.469 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.895 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.310 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.938 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.805 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.457 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.931 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.849 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.921 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.442 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.135 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 15.872 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.462 | 18 | 221,920 (2.219) | yes | - |
| backlog-adp | 16.427 | 18 | 183,598 (1.836) | yes | - |
| backlog-adp-refill | 41.157 | 23 | 183,598 (1.836) | yes | - |
| backlog-owed | 360.520 | 65 | 184,553 (1.846) | yes | - |

Composed maximum over the 4 backlog windows: 221,920 CPU cycles (2.219 ms), backlog.
Over the windows that released their whole load only: 221,920 (2.219 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 301 | 1 | 221,920 (2.219) | OVER the share |
| backlog-adp | 310 | 0 | 183,598 (1.836) | fits |
| backlog-adp-refill | 315 | 0 | 183,598 (1.836) | fits |
| backlog-owed | 359 | 0 | 184,553 (1.846) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 203,708 | 2.037 | 20 | 200 | fits | 221,920 | 138 | 0.651 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 765,943 | 7.659 | 20 | 20 | fits | 108,331 | 52 | 0.675 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 193,795 | 1.938 | 20 | 200 | fits | 194,003 | 146 | 0.588 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 645,734 | 6.457 | 20 | 200 | fits | 109,118 | 57 | 0.630 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 189,536 | 1.895 | 20 | 20 | fits | 194,003 | 146 | 0.588 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 831,036 | 8.310 | 20 | 20 | fits | 108,331 | 52 | 0.675 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 193,121 | 1.931 | 20 | 24 | fits | 194,003 | 146 | 0.588 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,329,672 | 13.297 | 20 | 24 | fits | 49,396 | 31 | 0.682 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 192,081 | 1.921 | 20 | 50 | fits | 194,003 | 146 | 0.588 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 644,239 | 6.442 | 20 | 50 | fits | 109,118 | 57 | 0.630 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 413,546 | 4.135 | 18 | 18 | fits | 221,920 | 138 | 0.651 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,393,349 | 13.933 | 18 | 18 | fits | 32,656 | 18 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 439,193 | 4.392 | 20 | 20 | fits | 160,200 | 89 | 0.665 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 108,348 | 1.083 | 20 | 200 | fits | 113,030 | 140 | 0.484 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 580,479 | 5.805 | 20 | 200 | fits | 160,200 | 89 | 0.665 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 109,260 | 1.093 | 20 | 20 | fits | 113,030 | 140 | 0.484 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 817,908 | 8.179 | 20 | 20 | fits | 106,553 | 34 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 112,845 | 1.128 | 20 | 24 | fits | 113,030 | 140 | 0.484 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,554,650 | 15.546 | 20 | 24 | fits | 65,840 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 111,805 | 1.118 | 20 | 50 | fits | 113,030 | 140 | 0.484 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 584,155 | 5.842 | 20 | 50 | fits | 160,200 | 89 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 294,948 | 2.949 | 18 | 18 | fits | 183,598 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,587,229 | 15.872 | 18 | 18 | fits | 35,114 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,658 | 0.117 | 20 | 20 | fits | 42,731 | 21 | 0.767 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 108,348 | 1.083 | 20 | 200 | fits | 113,030 | 140 | 0.484 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 46,884 | 0.469 | 20 | 200 | fits | 42,731 | 21 | 0.767 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 109,260 | 1.093 | 20 | 20 | fits | 113,030 | 140 | 0.484 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 797,326 | 7.973 | 20 | 20 | fits | 117,641 | 46 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 112,845 | 1.128 | 20 | 24 | fits | 113,030 | 140 | 0.484 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,469,312 | 14.693 | 20 | 24 | fits | 75,042 | 37 | 0.736 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 111,805 | 1.118 | 20 | 50 | fits | 113,030 | 140 | 0.484 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 564,294 | 5.643 | 20 | 50 | fits | 140,339 | 79 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 294,948 | 2.949 | 18 | 18 | fits | 183,598 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,550,011 | 15.500 | 18 | 18 | fits | 33,988 | 15 | 0.776 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,384,946 | 63.849 | 20 | 20 | MISS ceiling | 48,314 | 27 | 0.533 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,046,911 | 360.469 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,046,836 | 360.468 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,046,761 | 360.468 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,046,686 | 360.467 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 111,850 | 1.119 | 20 | 200 | fits | 110,731 | 134 | 0.490 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 536,366 | 5.364 | 20 | 200 | fits | 132,443 | 69 | 0.677 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 107,591 | 1.076 | 20 | 20 | fits | 110,731 | 134 | 0.490 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 733,810 | 7.338 | 20 | 20 | fits | 99,150 | 35 | 0.746 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 111,176 | 1.112 | 20 | 24 | fits | 110,731 | 134 | 0.490 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,484,926 | 64.849 | 20 | 24 | MISS ceiling | 30,276 | 23 | 0.529 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 110,136 | 1.101 | 20 | 50 | fits | 110,731 | 134 | 0.490 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 534,871 | 5.349 | 20 | 50 | fits | 132,443 | 69 | 0.677 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 402,363 | 4.024 | 18 | 18 | fits | 184,553 | 97 | 0.682 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,332,745 | 13.327 | 18 | 18 | fits | 49,108 | 21 | 0.733 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
