### 8x8

4 of 17 paths and 13 of 49 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 8.420 (9.155) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.516 (6.082) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.222 (0.735) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.186 (4.452) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.758 (64.188) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.384 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 2.055 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 9.102 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.098 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.029 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.907 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.091 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.128 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.081 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.892 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.428 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 16.893 | MISS T_svc | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 15.251 | 17 | 235,197 (2.352) | yes | - |
| backlog-adp | 17.439 | 18 | 200,048 (2.000) | yes | - |
| backlog-adp-refill | 41.072 | 28 | 200,048 (2.000) | yes | - |
| backlog-owed | 360.434 | 65 | 199,082 (1.991) | yes | - |

Composed maximum over the 4 backlog windows: 235,197 CPU cycles (2.352 ms), backlog.
Over the windows that released their whole load only: 235,197 (2.352 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 218,636 | 2.186 | 10 | 200 | fits | 235,197 | 414 | 0.538 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 841,974 | 8.420 | 10 | 20 | fits | 106,634 | 250 | 0.489 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 209,780 | 2.098 | 10 | 200 | fits | 209,988 | 392 | 0.483 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 690,713 | 6.907 | 10 | 200 | fits | 116,626 | 318 | 0.452 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 205,521 | 2.055 | 10 | 20 | fits | 209,988 | 392 | 0.483 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 910,187 | 9.102 | 10 | 20 | fits | 106,634 | 250 | 0.489 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 209,106 | 2.091 | 10 | 24 | fits | 209,988 | 392 | 0.483 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,441,890 | 14.419 | 10 | 24 | MISS T_svc | 52,913 | 163 | 0.491 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 208,066 | 2.081 | 10 | 50 | fits | 209,988 | 392 | 0.483 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 689,218 | 6.892 | 10 | 50 | fits | 116,626 | 318 | 0.452 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 442,808 | 4.428 | 10 | 18 | fits | 235,197 | 414 | 0.538 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,474,878 | 14.749 | 10 | 18 | MISS T_svc | 35,523 | 50 | 0.660 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 451,607 | 4.516 | 10 | 20 | fits | 170,484 | 350 | 0.530 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 115,030 | 1.150 | 10 | 200 | fits | 119,712 | 386 | 0.329 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 602,889 | 6.029 | 10 | 200 | fits | 170,484 | 350 | 0.530 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 115,942 | 1.159 | 10 | 20 | fits | 119,712 | 386 | 0.329 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 857,106 | 8.571 | 10 | 20 | fits | 125,925 | 250 | 0.515 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 119,527 | 1.195 | 10 | 24 | fits | 119,712 | 386 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,588,364 | 15.884 | 10 | 24 | MISS T_svc | 70,843 | 163 | 0.543 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 118,487 | 1.185 | 10 | 50 | fits | 119,712 | 386 | 0.329 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 606,565 | 6.066 | 10 | 50 | fits | 170,484 | 350 | 0.530 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 318,080 | 3.181 | 10 | 18 | fits | 200,048 | 418 | 0.519 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,689,346 | 16.893 | 10 | 18 | MISS T_svc | 51,191 | 48 | 0.700 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 22,157 | 0.222 | 10 | 20 | fits | 43,685 | 42 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 115,030 | 1.150 | 10 | 200 | fits | 119,712 | 386 | 0.329 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 56,812 | 0.568 | 10 | 200 | fits | 43,685 | 42 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 115,942 | 1.159 | 10 | 20 | fits | 119,712 | 386 | 0.329 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 835,919 | 8.359 | 10 | 20 | fits | 125,881 | 250 | 0.515 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 119,527 | 1.195 | 10 | 24 | fits | 119,712 | 386 | 0.329 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,529,874 | 15.299 | 10 | 24 | MISS T_svc | 70,965 | 163 | 0.545 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 118,487 | 1.185 | 10 | 50 | fits | 119,712 | 386 | 0.329 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 585,337 | 5.853 | 10 | 50 | fits | 149,256 | 319 | 0.523 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 318,080 | 3.181 | 10 | 18 | fits | 200,048 | 418 | 0.519 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,681,958 | 16.820 | 10 | 18 | MISS T_svc | 51,102 | 48 | 0.696 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,375,808 | 63.758 | 10 | 20 | MISS ceiling | 50,188 | 147 | 0.254 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,038,364 | 360.384 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,038,289 | 360.383 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,038,214 | 360.382 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,038,139 | 360.381 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 116,108 | 1.161 | 10 | 200 | fits | 115,922 | 344 | 0.337 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 602,956 | 6.030 | 10 | 200 | fits | 138,112 | 294 | 0.513 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 111,849 | 1.118 | 10 | 20 | fits | 115,922 | 344 | 0.337 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 808,777 | 8.088 | 10 | 20 | fits | 101,517 | 114 | 0.674 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 115,434 | 1.154 | 10 | 24 | fits | 115,922 | 344 | 0.337 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,512,800 | 65.128 | 10 | 24 | MISS ceiling | 31,584 | 125 | 0.286 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 114,394 | 1.144 | 10 | 50 | fits | 115,922 | 344 | 0.337 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 601,461 | 6.015 | 10 | 50 | fits | 138,112 | 294 | 0.513 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 313,021 | 3.130 | 10 | 18 | fits | 199,082 | 378 | 0.524 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,411,245 | 14.112 | 10 | 18 | MISS T_svc | 36,323 | 33 | 0.738 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
