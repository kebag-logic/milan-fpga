### 1x1

Clock: CPU 50 MHz, the product's split CPU clock (the Milan clock), bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.089 (6.594) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.262 (5.243) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.076 (0.326) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.889 (3.426) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.333 (63.602) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.383 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.673 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.457 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.715 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 5.360 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.709 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 64.651 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.698 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 5.345 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 3.403 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 16.260 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 10.934 | 17 | 85,875 (1.718) | yes | - |
| backlog-adp | 16.716 | 18 | 84,199 (1.684) | yes | - |
| backlog-adp-refill | 40.916 | 23 | 84,199 (1.684) | yes | - |
| backlog-owed | 360.434 | 63 | 75,366 (1.507) | yes | - |

Composed maximum over the 4 backlog windows: 85,875 CPU cycles (1.718 ms), backlog.
Over the windows that released their whole load only: 85,875 (1.718 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 100,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 291 | 0 | 85,875 (1.718) | fits |
| backlog-adp | 301 | 0 | 84,199 (1.684) | fits |
| backlog-adp-refill | 306 | 0 | 84,199 (1.684) | fits |
| backlog-owed | 348 | 0 | 75,366 (1.507) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 94,426 | 1.889 | 20 | 200 | fits | 85,444 | 117 | 0.610 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 304,455 | 6.089 | 20 | 20 | fits | 36,326 | 44 | 0.528 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 85,771 | 1.715 | 20 | 200 | fits | 85,875 | 141 | 0.620 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 256,186 | 5.124 | 20 | 200 | fits | 41,363 | 55 | 0.512 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 83,642 | 1.673 | 20 | 20 | fits | 85,875 | 141 | 0.620 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 327,039 | 6.541 | 20 | 20 | fits | 36,326 | 44 | 0.528 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 85,434 | 1.709 | 20 | 24 | fits | 85,875 | 141 | 0.620 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 517,702 | 10.354 | 20 | 24 | fits | 18,326 | 29 | 0.517 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 84,914 | 1.698 | 20 | 50 | fits | 85,875 | 141 | 0.620 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 255,438 | 5.109 | 20 | 50 | fits | 41,363 | 55 | 0.512 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 170,131 | 3.403 | 18 | 18 | fits | 85,444 | 117 | 0.610 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 525,351 | 10.507 | 18 | 18 | fits | 8,917 | 19 | 0.435 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 213,124 | 4.262 | 20 | 20 | fits | 51,743 | 72 | 0.618 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 55,116 | 1.102 | 20 | 200 | fits | 57,457 | 135 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 259,492 | 5.190 | 20 | 200 | fits | 51,743 | 72 | 0.618 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 55,572 | 1.111 | 20 | 20 | fits | 57,457 | 135 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 372,853 | 7.457 | 20 | 20 | fits | 46,123 | 33 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 57,365 | 1.147 | 20 | 24 | fits | 57,457 | 135 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 788,101 | 15.762 | 20 | 24 | fits | 41,822 | 35 | 0.779 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 56,845 | 1.137 | 20 | 50 | fits | 57,457 | 135 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 261,330 | 5.227 | 20 | 50 | fits | 51,743 | 72 | 0.618 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 140,816 | 2.816 | 18 | 18 | fits | 84,199 | 138 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 812,986 | 16.260 | 18 | 18 | fits | 26,152 | 19 | 0.819 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 3,779 | 0.076 | 20 | 20 | fits | 16,281 | 20 | 0.756 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 55,116 | 1.102 | 20 | 200 | fits | 57,457 | 135 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 15,957 | 0.319 | 20 | 200 | fits | 16,281 | 20 | 0.756 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 55,572 | 1.111 | 20 | 20 | fits | 57,457 | 135 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 368,374 | 7.367 | 20 | 20 | fits | 55,635 | 44 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 57,365 | 1.147 | 20 | 24 | fits | 57,457 | 135 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 742,272 | 14.845 | 20 | 24 | fits | 37,054 | 29 | 0.769 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 56,845 | 1.137 | 20 | 50 | fits | 57,457 | 135 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 253,884 | 5.078 | 20 | 50 | fits | 44,297 | 62 | 0.605 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 140,816 | 2.816 | 18 | 18 | fits | 84,199 | 138 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 796,687 | 15.934 | 18 | 18 | fits | 25,414 | 17 | 0.819 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 3,166,641 | 63.333 | 20 | 20 | MISS ceiling | 22,107 | 25 | 0.617 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,019,154 | 360.383 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,019,116 | 360.382 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,019,079 | 360.382 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,019,041 | 360.381 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 56,873 | 1.137 | 20 | 200 | fits | 55,364 | 129 | 0.501 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 267,985 | 5.360 | 20 | 200 | fits | 63,193 | 67 | 0.699 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 54,744 | 1.095 | 20 | 20 | fits | 55,364 | 129 | 0.501 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 361,713 | 7.234 | 20 | 20 | fits | 46,665 | 33 | 0.789 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 56,536 | 1.131 | 20 | 24 | fits | 55,364 | 129 | 0.501 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 3,232,547 | 64.651 | 20 | 24 | MISS ceiling | 17,157 | 21 | 0.642 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 56,016 | 1.120 | 20 | 50 | fits | 55,364 | 129 | 0.501 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 267,237 | 5.345 | 20 | 50 | fits | 63,193 | 67 | 0.699 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 131,155 | 2.623 | 18 | 18 | fits | 75,366 | 127 | 0.655 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 670,043 | 13.401 | 18 | 18 | fits | 18,482 | 17 | 0.836 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
