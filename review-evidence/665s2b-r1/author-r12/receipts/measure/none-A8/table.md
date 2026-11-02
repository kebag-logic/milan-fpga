### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 17 paths and 13 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 14.286 (15.529) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 8.748 (11.724) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.224 (1.471) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 3.162 (5.434) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 67.419 (68.644) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 361.199 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 2.896 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 16.080 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.939 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 11.671 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 11.695 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.932 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 70.066 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.921 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 11.707 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 11.368 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 30.257 | MISS ceiling | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 27.063 | 19 | 350,615 (3.506) | yes | - |
| backlog-adp | 0 | 31.595 | 20 | 339,711 (3.397) | yes | - |
| backlog-adp-refill | 0 | 42.338 | 24 | 339,711 (3.397) | yes | - |
| backlog-owed | 0 | 361.250 | 64 | 361,269 (3.613) | yes | - |

Composed maximum over the 4 backlog windows: 361,269 CPU cycles (3.613 ms), backlog-owed.
Over the windows that released their whole load only: 361,269 (3.613 ms), backlog-owed.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 303 | 16 | 350,615 (3.506) | OVER the share |
| backlog-adp | 324 | 15 | 339,711 (3.397) | OVER the share |
| backlog-adp-refill | 328 | 15 | 339,711 (3.397) | OVER the share |
| backlog-owed | 359 | 16 | 361,269 (3.613) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 316,212 | 3.162 | 20 | 200 | fits | 249,334 | 125 | 0.818 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,428,569 | 14.286 | 20 | 20 | fits | 212,318 | 52 | 0.820 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 293,858 | 2.939 | 20 | 200 | fits | 294,066 | 143 | 0.824 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 1,138,377 | 11.384 | 20 | 200 | fits | 245,179 | 57 | 0.822 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 289,599 | 2.896 | 20 | 20 | fits | 294,066 | 143 | 0.824 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,547,606 | 15.476 | 20 | 20 | fits | 212,318 | 52 | 0.820 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 293,184 | 2.932 | 20 | 24 | fits | 294,066 | 143 | 0.824 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 2,377,441 | 23.774 | 20 | 24 | MISS T_svc | 82,640 | 31 | 0.816 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 292,144 | 2.921 | 20 | 50 | fits | 294,066 | 143 | 0.824 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,136,882 | 11.369 | 20 | 50 | fits | 245,179 | 57 | 0.822 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,136,817 | 11.368 | 18 | 18 | fits | 245,179 | 57 | 0.822 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 2,580,557 | 25.806 | 18 | 18 | MISS ceiling | 64,690 | 18 | 0.817 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 874,809 | 8.748 | 20 | 20 | fits | 303,799 | 83 | 0.820 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 252,352 | 2.524 | 20 | 200 | fits | 257,034 | 140 | 0.821 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 1,167,064 | 11.671 | 20 | 200 | fits | 303,799 | 83 | 0.820 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 253,264 | 2.533 | 20 | 20 | fits | 257,034 | 140 | 0.821 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 1,608,041 | 16.080 | 20 | 20 | fits | 246,245 | 58 | 0.820 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 256,849 | 2.568 | 20 | 24 | fits | 257,034 | 140 | 0.821 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 2,683,218 | 26.832 | 20 | 24 | MISS ceiling | 107,315 | 31 | 0.814 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 255,809 | 2.558 | 20 | 50 | fits | 257,034 | 140 | 0.821 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 1,170,740 | 11.707 | 20 | 50 | fits | 303,799 | 83 | 0.820 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 866,876 | 8.669 | 18 | 18 | fits | 339,711 | 104 | 0.824 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 3,025,732 | 30.257 | 18 | 18 | MISS ceiling | 69,369 | 21 | 0.812 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 22,393 | 0.224 | 20 | 20 | fits | 91,096 | 21 | 0.811 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 252,352 | 2.524 | 20 | 200 | fits | 257,034 | 140 | 0.821 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 103,702 | 1.037 | 20 | 200 | fits | 91,096 | 21 | 0.811 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 253,264 | 2.533 | 20 | 20 | fits | 257,034 | 140 | 0.821 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 1,564,424 | 15.644 | 20 | 20 | fits | 256,241 | 69 | 0.819 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 256,849 | 2.568 | 20 | 24 | fits | 257,034 | 140 | 0.821 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 2,666,714 | 26.667 | 20 | 24 | MISS ceiling | 107,315 | 31 | 0.814 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 255,809 | 2.558 | 20 | 50 | fits | 257,034 | 140 | 0.821 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 1,123,074 | 11.231 | 20 | 50 | fits | 256,133 | 73 | 0.822 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 866,876 | 8.669 | 18 | 18 | fits | 339,711 | 104 | 0.824 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 2,939,859 | 29.399 | 18 | 18 | MISS ceiling | 96,729 | 28 | 0.812 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,741,885 | 67.419 | 20 | 20 | MISS ceiling | 99,820 | 27 | 0.811 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,119,930 | 361.199 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,119,855 | 361.199 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,119,780 | 361.198 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,119,705 | 361.197 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 284,059 | 2.841 | 20 | 200 | fits | 251,913 | 134 | 0.819 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 1,169,502 | 11.695 | 20 | 200 | fits | 251,449 | 69 | 0.820 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 279,800 | 2.798 | 20 | 20 | fits | 251,913 | 134 | 0.819 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,503,822 | 15.038 | 20 | 20 | fits | 196,648 | 41 | 0.812 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 283,385 | 2.834 | 20 | 24 | fits | 251,913 | 134 | 0.819 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,006,554 | 70.066 | 20 | 24 | MISS ceiling | 60,546 | 23 | 0.812 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 282,345 | 2.823 | 20 | 50 | fits | 251,913 | 134 | 0.819 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,168,007 | 11.680 | 20 | 50 | fits | 251,449 | 69 | 0.820 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 643,159 | 6.432 | 18 | 18 | fits | 361,269 | 138 | 0.822 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 2,583,204 | 25.832 | 18 | 18 | MISS ceiling | 88,956 | 21 | 0.813 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
