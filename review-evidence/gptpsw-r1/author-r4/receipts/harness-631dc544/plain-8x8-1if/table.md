### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 16 paths and 7 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.451 (4.819) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.879 (4.543) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.123 (0.522) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.615 (2.071) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.211 (63.555) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.105 (64.449) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.106 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.160 | MISS ceiling | 11 acmp | 4 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.149 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 4.489 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.642 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.840 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.132 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 4.526 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 5.807 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 8.357 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 5.873 | 7 | 151,639 (1.516) | yes | - |
| backlog-adp | 0 | 8.930 | 7 | 150,087 (1.501) | yes | - |
| backlog-adp-refill | 0 | 40.851 | 21 | 150,087 (1.501) | yes | - |
| backlog-owed | 0 | 65.028 | 23 | 151,526 (1.515) | yes | - |

Composed maximum over the 4 backlog windows: 151,639 CPU cycles (1.516 ms), backlog.
Over the windows that released their whole load only: 151,639 (1.516 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 286 | 0 | 151,639 (1.516) | fits |
| backlog-adp | 309 | 0 | 150,087 (1.501) | fits |
| backlog-adp-refill | 323 | 0 | 150,087 (1.501) | fits |
| backlog-owed | 308 | 0 | 151,526 (1.515) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 265 | 23,811 (0.238) | 2,211 (0.022) |
| backlog-adp | 271 | 23,811 (0.238) | 2,211 (0.022) |
| backlog-adp-refill | 274 | 23,811 (0.238) | 2,211 (0.022) |
| backlog-owed | 277 | 23,811 (0.238) | 2,284 (0.023) |

Longest pass that carries a step: 23,811 CPU cycles (0.238 ms), backlog; longest step: 2,284 (0.023 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 161,507 | 1.615 | 20 | 200 | fits | 55,476 | 78 | 0.539 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 445,113 | 4.451 | 20 | 20 | fits | 66,781 | 90 | 0.289 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 414,940 | 4.149 | 20 | 200 | fits | 146,956 | 122 | 0.386 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 414,324 | 4.143 | 20 | 200 | fits | 146,956 | 122 | 0.386 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 410,618 | 4.106 | 20 | 20 | fits | 146,956 | 122 | 0.386 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 476,563 | 4.766 | 20 | 20 | fits | 66,781 | 90 | 0.289 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 150,748 | 1.507 | 20 | 24 | fits | 151,639 | 167 | 0.386 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 266,312 | 2.663 | 20 | 24 | fits | 61,078 | 26 | 0.683 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 413,202 | 4.132 | 20 | 50 | fits | 146,956 | 122 | 0.386 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 412,806 | 4.128 | 20 | 50 | fits | 146,956 | 122 | 0.386 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 479,521 | 4.795 | 20 | 20 | fits | 66,781 | 90 | 0.289 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 533,849 | 5.338 | 20 | 20 | fits | 23,927 | 41 | 0.057 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 387,927 | 3.879 | 20 | 20 | fits | 145,738 | 173 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 294,542 | 2.945 | 20 | 200 | fits | 150,087 | 214 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 448,893 | 4.489 | 20 | 200 | fits | 145,738 | 173 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 295,466 | 2.955 | 20 | 20 | fits | 150,087 | 214 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 449,597 | 4.496 | 20 | 20 | fits | 145,738 | 173 | 0.474 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,019 | 1.490 | 20 | 24 | fits | 149,205 | 164 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 298,116 | 2.981 | 20 | 24 | fits | 150,087 | 214 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 298,050 | 2.981 | 20 | 50 | fits | 150,087 | 214 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 452,621 | 4.526 | 20 | 50 | fits | 145,738 | 173 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 580,682 | 5.807 | 20 | 20 | fits | 128,127 | 48 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 835,716 | 8.357 | 20 | 20 | fits | 125,645 | 52 | 0.670 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,314 | 0.123 | 20 | 20 | fits | 31,531 | 19 | 0.769 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 294,542 | 2.945 | 20 | 200 | fits | 150,087 | 214 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 34,330 | 0.343 | 20 | 200 | fits | 31,531 | 19 | 0.769 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 295,466 | 2.955 | 20 | 20 | fits | 150,087 | 214 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 435,351 | 4.354 | 20 | 20 | fits | 131,492 | 163 | 0.431 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,019 | 1.490 | 20 | 24 | fits | 149,205 | 164 | 0.373 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 298,116 | 2.981 | 20 | 24 | fits | 150,087 | 214 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 298,050 | 2.981 | 20 | 50 | fits | 150,087 | 214 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 438,375 | 4.384 | 20 | 50 | fits | 131,492 | 163 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 565,781 | 5.658 | 20 | 20 | fits | 127,472 | 48 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 820,815 | 8.208 | 20 | 20 | fits | 125,645 | 52 | 0.670 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,321,072 | 63.211 | 20 | 20 | MISS ceiling | 22,513 | 13 | 0.636 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,343,510 | 63.435 | 20 | 20 | MISS ceiling | 22,497 | 13 | 0.613 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,365,923 | 63.659 | 20 | 20 | MISS ceiling | 22,487 | 13 | 0.620 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,388,244 | 63.882 | 20 | 20 | MISS ceiling | 22,397 | 13 | 0.628 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,410,518 | 64.105 | 20 | 20 | MISS ceiling | 22,337 | 13 | 0.636 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 164,845 | 1.648 | 20 | 200 | fits | 151,526 | 196 | 0.461 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 314,985 | 3.150 | 20 | 200 | fits | 150,756 | 192 | 0.502 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 160,523 | 1.605 | 20 | 20 | fits | 151,526 | 196 | 0.461 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,215,963 | 62.160 | 20 | 20 | MISS ceiling | 35,447 | 15 | 0.697 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 164,163 | 1.642 | 20 | 24 | fits | 151,526 | 196 | 0.461 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,184,002 | 61.840 | 20 | 24 | MISS ceiling | 138,021 | 106 | 0.438 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 163,107 | 1.631 | 20 | 50 | fits | 151,526 | 196 | 0.461 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 313,467 | 3.135 | 20 | 50 | fits | 150,756 | 192 | 0.502 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 313,401 | 3.134 | 20 | 20 | fits | 150,756 | 192 | 0.502 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 679,187 | 6.792 | 20 | 20 | fits | 108,031 | 44 | 0.699 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
