### 1x1

4 of 16 paths and 10 of 49 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.194 (4.517) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.035 (4.072) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.109 (0.299) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.266 (2.298) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.922 (62.119) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.144 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.137 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 5.657 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.179 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 4.019 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.172 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.725 | MISS ceiling | 15 aecp | 4 | 3 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.162 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 4.055 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.274 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 11.035 | MISS T_svc | 31 srp | 4 | 2 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 7.062 | 17 | 118,121 (1.181) | yes | - |
| backlog-adp | 11.250 | 18 | 118,858 (1.189) | yes | - |
| backlog-adp-refill | 40.419 | 30 | 118,858 (1.189) | yes | - |
| backlog-owed | 360.195 | 64 | 114,772 (1.148) | yes | - |

Composed maximum over the 4 backlog windows: 118,858 CPU cycles (1.189 ms), backlog-adp.
Over the windows that released their whole load only: 118,858 (1.189 ms), backlog-adp.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 126,571 | 1.266 | 10 | 200 | fits | 111,644 | 394 | 0.421 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 419,381 | 4.194 | 10 | 20 | fits | 50,665 | 249 | 0.270 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 117,913 | 1.179 | 10 | 200 | fits | 118,121 | 388 | 0.462 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 349,383 | 3.494 | 10 | 200 | fits | 57,995 | 317 | 0.256 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 113,654 | 1.137 | 10 | 20 | fits | 118,121 | 388 | 0.462 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 446,424 | 4.464 | 10 | 20 | fits | 50,665 | 249 | 0.270 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 117,239 | 1.172 | 10 | 24 | fits | 118,121 | 388 | 0.462 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 680,340 | 6.803 | 10 | 24 | fits | 22,954 | 162 | 0.214 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 116,199 | 1.162 | 10 | 50 | fits | 118,121 | 388 | 0.462 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 347,888 | 3.479 | 10 | 50 | fits | 57,995 | 317 | 0.256 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 227,388 | 2.274 | 10 | 18 | fits | 111,644 | 394 | 0.421 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 686,577 | 6.866 | 10 | 18 | fits | 8,772 | 49 | 0.140 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 303,548 | 3.035 | 10 | 20 | fits | 106,912 | 345 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 76,874 | 0.769 | 10 | 200 | fits | 81,556 | 382 | 0.347 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 401,864 | 4.019 | 10 | 200 | fits | 106,912 | 345 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 77,786 | 0.778 | 10 | 20 | fits | 81,556 | 382 | 0.347 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 565,669 | 5.657 | 10 | 20 | fits | 79,855 | 249 | 0.520 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 81,371 | 0.814 | 10 | 24 | fits | 81,556 | 382 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,051,904 | 10.519 | 10 | 24 | MISS T_svc | 48,445 | 162 | 0.546 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 80,331 | 0.803 | 10 | 50 | fits | 81,556 | 382 | 0.347 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 405,540 | 4.055 | 10 | 50 | fits | 106,912 | 345 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 198,734 | 1.987 | 10 | 18 | fits | 118,858 | 415 | 0.482 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,103,480 | 11.035 | 10 | 18 | MISS T_svc | 21,747 | 29 | 0.756 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 10,929 | 0.109 | 10 | 20 | fits | 19,161 | 41 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 76,874 | 0.769 | 10 | 200 | fits | 81,556 | 382 | 0.347 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 24,142 | 0.241 | 10 | 200 | fits | 19,161 | 41 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 77,786 | 0.778 | 10 | 20 | fits | 81,556 | 382 | 0.347 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 554,097 | 5.541 | 10 | 20 | fits | 79,752 | 249 | 0.520 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 81,371 | 0.814 | 10 | 24 | fits | 81,556 | 382 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 1,052,393 | 10.524 | 10 | 24 | MISS T_svc | 50,630 | 187 | 0.518 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 80,331 | 0.803 | 10 | 50 | fits | 81,556 | 382 | 0.347 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 388,948 | 3.889 | 10 | 50 | fits | 90,320 | 312 | 0.498 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 198,734 | 1.987 | 10 | 18 | fits | 118,858 | 415 | 0.482 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,082,222 | 10.822 | 10 | 18 | MISS T_svc | 32,364 | 49 | 0.728 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,192,160 | 61.922 | 10 | 20 | MISS ceiling | 26,534 | 146 | 0.247 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,014,441 | 360.144 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,014,366 | 360.144 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,014,291 | 360.143 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,014,216 | 360.142 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 78,314 | 0.783 | 10 | 200 | fits | 77,664 | 340 | 0.345 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 377,441 | 3.774 | 10 | 200 | fits | 88,687 | 293 | 0.512 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 74,055 | 0.741 | 10 | 20 | fits | 77,664 | 340 | 0.345 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 501,561 | 5.016 | 10 | 20 | fits | 65,047 | 119 | 0.700 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 77,640 | 0.776 | 10 | 24 | fits | 77,664 | 340 | 0.345 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,272,485 | 62.725 | 10 | 24 | MISS ceiling | 20,351 | 124 | 0.266 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 76,600 | 0.766 | 10 | 50 | fits | 77,664 | 340 | 0.345 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 375,946 | 3.759 | 10 | 50 | fits | 88,687 | 293 | 0.512 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 190,917 | 1.909 | 10 | 18 | fits | 114,772 | 372 | 0.504 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 864,372 | 8.644 | 10 | 18 | fits | 32,873 | 50 | 0.725 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
