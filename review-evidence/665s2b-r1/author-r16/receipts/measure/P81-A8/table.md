### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.875 (6.356) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.819 (4.909) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.224 (0.709) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.333 (2.286) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.360 (63.697) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.420 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.181 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.810 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.224 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 5.656 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.217 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 64.514 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.207 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 4.893 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.764 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | 14.930 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 10.321 | 20 | 159,045 (1.590) | yes | - |
| backlog-adp | 0 | 15.711 | 22 | 156,180 (1.562) | yes | - |
| backlog-adp-refill | 0 | 41.035 | 34 | 156,180 (1.562) | yes | - |
| backlog-owed | 0 | 360.471 | 65 | 131,671 (1.317) | yes | - |

Composed maximum over the 4 backlog windows: 159,045 CPU cycles (1.590 ms), backlog.
Over the windows that released their whole load only: 159,045 (1.590 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 299 | 0 | 159,045 (1.590) | fits |
| backlog-adp | 324 | 0 | 156,180 (1.562) | fits |
| backlog-adp-refill | 336 | 0 | 156,180 (1.562) | fits |
| backlog-owed | 355 | 0 | 131,671 (1.317) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 266 | 50,461 (0.505) | 3,116 (0.031) |
| backlog-adp | 271 | 50,461 (0.505) | 3,116 (0.031) |
| backlog-adp-refill | 273 | 50,461 (0.505) | 3,116 (0.031) |
| backlog-owed | 305 | 50,461 (0.505) | 3,116 (0.031) |

Longest pass that carries a step: 50,461 CPU cycles (0.505 ms), backlog; longest step: 3,116 (0.031 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 133,266 | 1.333 | 20 | 200 | fits | 105,982 | 104 | 0.517 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 587,531 | 5.875 | 20 | 20 | fits | 78,109 | 44 | 0.523 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 122,368 | 1.224 | 20 | 200 | fits | 122,576 | 138 | 0.524 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 477,944 | 4.779 | 20 | 200 | fits | 91,158 | 55 | 0.562 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 118,109 | 1.181 | 20 | 20 | fits | 122,576 | 138 | 0.524 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 630,289 | 6.303 | 20 | 20 | fits | 78,109 | 44 | 0.523 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 121,694 | 1.217 | 20 | 24 | fits | 122,576 | 138 | 0.524 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 918,149 | 9.181 | 20 | 24 | fits | 27,838 | 29 | 0.447 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 120,654 | 1.207 | 20 | 50 | fits | 122,576 | 138 | 0.524 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 476,449 | 4.764 | 20 | 50 | fits | 91,158 | 55 | 0.562 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 476,384 | 4.764 | 18 | 18 | fits | 91,158 | 55 | 0.562 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 979,257 | 9.793 | 18 | 18 | fits | 15,127 | 14 | 0.226 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 381,888 | 3.819 | 20 | 20 | fits | 115,469 | 73 | 0.609 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 105,404 | 1.054 | 20 | 200 | fits | 110,086 | 135 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 485,632 | 4.856 | 20 | 200 | fits | 115,469 | 73 | 0.609 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 106,316 | 1.063 | 20 | 20 | fits | 110,086 | 135 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 780,975 | 7.810 | 20 | 20 | fits | 90,319 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 109,901 | 1.099 | 20 | 24 | fits | 110,086 | 135 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,317,441 | 13.174 | 20 | 24 | fits | 59,136 | 29 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 108,861 | 1.089 | 20 | 50 | fits | 110,086 | 135 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 489,308 | 4.893 | 20 | 50 | fits | 115,469 | 73 | 0.609 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 373,774 | 3.738 | 18 | 18 | fits | 156,180 | 103 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,488,269 | 14.883 | 18 | 18 | fits | 44,100 | 18 | 0.723 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 22,386 | 0.224 | 20 | 20 | fits | 41,854 | 20 | 0.780 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 105,404 | 1.054 | 20 | 200 | fits | 110,086 | 135 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 54,796 | 0.548 | 20 | 200 | fits | 41,854 | 20 | 0.780 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 106,316 | 1.063 | 20 | 20 | fits | 110,086 | 135 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 759,730 | 7.597 | 20 | 20 | fits | 90,262 | 37 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 109,901 | 1.099 | 20 | 24 | fits | 110,086 | 135 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 1,298,215 | 12.982 | 20 | 24 | fits | 59,136 | 29 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 108,861 | 1.089 | 20 | 50 | fits | 110,086 | 135 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 467,893 | 4.679 | 20 | 50 | fits | 94,054 | 63 | 0.595 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 373,774 | 3.738 | 18 | 18 | fits | 156,180 | 103 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,493,010 | 14.930 | 18 | 18 | fits | 34,013 | 15 | 0.777 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,336,037 | 63.360 | 20 | 20 | MISS ceiling | 45,549 | 25 | 0.578 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,042,033 | 360.420 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,041,958 | 360.420 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,041,883 | 360.419 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,041,808 | 360.418 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 110,637 | 1.106 | 20 | 200 | fits | 107,378 | 129 | 0.506 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 565,643 | 5.656 | 20 | 200 | fits | 104,196 | 41 | 0.702 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 106,378 | 1.064 | 20 | 20 | fits | 107,378 | 129 | 0.506 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 718,057 | 7.181 | 20 | 20 | fits | 65,173 | 24 | 0.763 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 109,963 | 1.100 | 20 | 24 | fits | 107,378 | 129 | 0.506 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,451,381 | 64.514 | 20 | 24 | MISS ceiling | 26,108 | 21 | 0.524 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 108,923 | 1.089 | 20 | 50 | fits | 107,378 | 129 | 0.506 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 459,952 | 4.600 | 20 | 50 | fits | 131,671 | 89 | 0.623 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 328,216 | 3.282 | 18 | 18 | fits | 113,680 | 59 | 0.745 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 1,248,912 | 12.489 | 18 | 18 | fits | 44,586 | 20 | 0.734 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
