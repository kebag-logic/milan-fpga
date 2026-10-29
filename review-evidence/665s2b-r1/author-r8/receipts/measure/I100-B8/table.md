### 8x8

4 of 17 paths and 13 of 49 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 8.415 (9.149) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.419 (5.968) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.213 (0.723) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.192 (4.455) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.782 (64.170) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.452 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 2.061 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 9.096 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.104 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.916 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.907 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.097 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.147 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.087 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.892 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.432 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 16.642 | MISS T_svc | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 15.193 | 17 | 234,934 (2.349) | yes | - |
| backlog-adp | 17.180 | 18 | 192,463 (1.925) | yes | - |
| backlog-adp-refill | 41.229 | 24 | 192,463 (1.925) | yes | - |
| backlog-owed | 360.503 | 64 | 198,963 (1.990) | yes | - |

Composed maximum over the 4 backlog windows: 234,934 CPU cycles (2.349 ms), backlog.
Over the windows that released their whole load only: 234,934 (2.349 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 219,247 | 2.192 | 10 | 200 | fits | 234,934 | 414 | 0.538 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 841,532 | 8.415 | 10 | 20 | fits | 106,231 | 250 | 0.483 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 210,391 | 2.104 | 10 | 200 | fits | 210,599 | 392 | 0.483 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 690,701 | 6.907 | 10 | 200 | fits | 116,065 | 318 | 0.446 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 206,132 | 2.061 | 10 | 20 | fits | 210,599 | 392 | 0.483 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 909,559 | 9.096 | 10 | 20 | fits | 106,231 | 250 | 0.483 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 209,717 | 2.097 | 10 | 24 | fits | 210,599 | 392 | 0.483 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,436,097 | 14.361 | 10 | 24 | MISS T_svc | 52,364 | 163 | 0.484 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 208,677 | 2.087 | 10 | 50 | fits | 210,599 | 392 | 0.483 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 689,206 | 6.892 | 10 | 50 | fits | 116,065 | 318 | 0.446 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 443,156 | 4.432 | 10 | 18 | fits | 234,934 | 414 | 0.538 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,468,392 | 14.684 | 10 | 18 | MISS T_svc | 34,830 | 50 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 441,903 | 4.419 | 10 | 20 | fits | 168,923 | 350 | 0.524 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 116,091 | 1.161 | 10 | 200 | fits | 120,773 | 386 | 0.347 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 591,554 | 5.916 | 10 | 200 | fits | 168,923 | 350 | 0.524 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 117,003 | 1.170 | 10 | 20 | fits | 120,773 | 386 | 0.347 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 841,781 | 8.418 | 10 | 20 | fits | 112,144 | 136 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 120,588 | 1.206 | 10 | 24 | fits | 120,773 | 386 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,615,746 | 16.157 | 10 | 24 | MISS T_svc | 69,112 | 163 | 0.534 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 119,548 | 1.195 | 10 | 50 | fits | 120,773 | 386 | 0.347 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 595,230 | 5.952 | 10 | 50 | fits | 168,923 | 350 | 0.524 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 311,556 | 3.116 | 10 | 18 | fits | 192,463 | 416 | 0.488 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,664,209 | 16.642 | 10 | 18 | MISS T_svc | 50,998 | 50 | 0.708 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 21,275 | 0.213 | 10 | 20 | fits | 43,707 | 42 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 116,091 | 1.161 | 10 | 200 | fits | 120,773 | 386 | 0.347 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 55,914 | 0.559 | 10 | 200 | fits | 43,707 | 42 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 117,003 | 1.170 | 10 | 20 | fits | 120,773 | 386 | 0.347 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 821,462 | 8.215 | 10 | 20 | fits | 124,669 | 250 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 120,588 | 1.206 | 10 | 24 | fits | 120,773 | 386 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,513,842 | 15.138 | 10 | 24 | MISS T_svc | 79,006 | 169 | 0.578 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 119,548 | 1.195 | 10 | 50 | fits | 120,773 | 386 | 0.347 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 573,666 | 5.737 | 10 | 50 | fits | 147,359 | 319 | 0.515 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 311,556 | 3.116 | 10 | 18 | fits | 192,463 | 416 | 0.488 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,649,755 | 16.498 | 10 | 18 | MISS T_svc | 35,203 | 30 | 0.732 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,378,202 | 63.782 | 10 | 20 | MISS ceiling | 50,036 | 147 | 0.254 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,045,223 | 360.452 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,045,148 | 360.451 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,045,073 | 360.451 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,044,998 | 360.450 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 120,889 | 1.209 | 10 | 200 | fits | 116,542 | 344 | 0.340 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 606,152 | 6.062 | 10 | 200 | fits | 137,280 | 294 | 0.510 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 116,630 | 1.166 | 10 | 20 | fits | 116,542 | 344 | 0.340 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 811,099 | 8.111 | 10 | 20 | fits | 101,148 | 114 | 0.673 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 120,215 | 1.202 | 10 | 24 | fits | 116,542 | 344 | 0.340 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,514,738 | 65.147 | 10 | 24 | MISS ceiling | 31,432 | 125 | 0.286 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 119,175 | 1.192 | 10 | 50 | fits | 116,542 | 344 | 0.340 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 604,657 | 6.047 | 10 | 50 | fits | 137,280 | 294 | 0.510 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 317,683 | 3.177 | 10 | 18 | fits | 198,963 | 378 | 0.523 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,380,063 | 13.801 | 10 | 18 | MISS T_svc | 50,882 | 51 | 0.702 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
