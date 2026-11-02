### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 313 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.011 (7.560) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 5.396 (7.807) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.122 (0.722) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.535 (2.673) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.194 (64.797) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.508 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.869 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 9.299 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.859 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.853 | fits | 7 adp | 26 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 6.071 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.904 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.312 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.894 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.890 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.613 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-6.service.srp.last.if1` (backlog-adp@verify-6) | 17.292 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.561 | 18 | 191,910 (1.919) | yes | - |
| backlog-adp@blank-1 | 0 | 17.958 | 18 | 191,910 (1.919) | yes | - |
| backlog-adp@blank-2 | 0 | 19.298 | 19 | 191,910 (1.919) | yes | - |
| backlog-adp@blank-3 | 0 | 18.341 | 19 | 191,910 (1.919) | yes | - |
| backlog-adp@blank-4 | 0 | 18.062 | 18 | 191,910 (1.919) | yes | - |
| backlog-adp@blank-5 | 0 | 18.075 | 18 | 191,910 (1.919) | yes | - |
| backlog-adp@blank-6 | 0 | 18.146 | 19 | 190,350 (1.903) | yes | - |
| backlog-adp@blank-7 | 0 | 18.195 | 18 | 198,079 (1.981) | yes | - |
| backlog-adp@program-0 | 0 | 17.965 | 18 | 190,986 (1.910) | yes | - |
| backlog-adp@program-1 | 0 | 18.142 | 18 | 190,986 (1.910) | yes | - |
| backlog-adp@program-2 | 0 | 18.050 | 18 | 190,986 (1.910) | yes | - |
| backlog-adp@program-3 | 0 | 18.245 | 18 | 197,228 (1.972) | yes | - |
| backlog-adp@program-4 | 0 | 17.138 | 17 | 191,185 (1.912) | yes | - |
| backlog-adp@program-5 | 0 | 17.341 | 18 | 190,864 (1.909) | yes | - |
| backlog-adp@program-6 | 0 | 17.250 | 18 | 190,864 (1.909) | yes | - |
| backlog-adp@program-7 | 0 | 17.445 | 18 | 197,106 (1.971) | yes | - |
| backlog-adp@verify-0 | 0 | 18.472 | 18 | 191,760 (1.918) | yes | - |
| backlog-adp@verify-1 | 0 | 19.432 | 18 | 191,760 (1.918) | yes | - |
| backlog-adp@verify-2 | 0 | 18.440 | 18 | 191,760 (1.918) | yes | - |
| backlog-adp@verify-3 | 0 | 18.373 | 18 | 191,760 (1.918) | yes | - |
| backlog-adp@verify-4 | 0 | 18.321 | 18 | 191,760 (1.918) | yes | - |
| backlog-adp@verify-5 | 0 | 18.366 | 18 | 175,046 (1.750) | yes | - |
| backlog-adp@verify-6 | 0 | 18.715 | 19 | 197,872 (1.979) | yes | - |
| backlog-adp@verify-7 | 0 | 18.430 | 18 | 191,711 (1.917) | yes | - |
| backlog | 0 | 15.073 | 20 | 162,557 (1.626) | yes | - |
| backlog-adp | 0 | 17.142 | 18 | 190,868 (1.909) | yes | - |
| backlog-adp-refill | 0 | 41.296 | 23 | 190,868 (1.909) | yes | - |
| backlog-owed | 0 | 360.559 | 64 | 195,358 (1.954) | yes | - |

Composed maximum over the 4 backlog windows: 195,358 CPU cycles (1.954 ms), backlog-owed.
Over the windows that released their whole load only: 195,358 (1.954 ms), backlog-owed.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 381 | 0 | 191,910 (1.919) | fits |
| backlog-adp@blank-1 | 381 | 0 | 191,910 (1.919) | fits |
| backlog-adp@blank-2 | 382 | 0 | 191,910 (1.919) | fits |
| backlog-adp@blank-3 | 382 | 0 | 191,910 (1.919) | fits |
| backlog-adp@blank-4 | 381 | 0 | 191,910 (1.919) | fits |
| backlog-adp@blank-5 | 381 | 0 | 191,910 (1.919) | fits |
| backlog-adp@blank-6 | 382 | 0 | 190,350 (1.903) | fits |
| backlog-adp@blank-7 | 382 | 0 | 198,079 (1.981) | fits |
| backlog-adp@program-0 | 490 | 0 | 190,986 (1.910) | fits |
| backlog-adp@program-1 | 490 | 0 | 190,986 (1.910) | fits |
| backlog-adp@program-2 | 490 | 0 | 190,986 (1.910) | fits |
| backlog-adp@program-3 | 490 | 0 | 197,228 (1.972) | fits |
| backlog-adp@program-4 | 490 | 0 | 191,185 (1.912) | fits |
| backlog-adp@program-5 | 491 | 0 | 190,864 (1.909) | fits |
| backlog-adp@program-6 | 491 | 0 | 190,864 (1.909) | fits |
| backlog-adp@program-7 | 491 | 0 | 197,106 (1.971) | fits |
| backlog-adp@verify-0 | 596 | 0 | 191,760 (1.918) | fits |
| backlog-adp@verify-1 | 596 | 0 | 191,760 (1.918) | fits |
| backlog-adp@verify-2 | 596 | 0 | 191,760 (1.918) | fits |
| backlog-adp@verify-3 | 596 | 0 | 191,760 (1.918) | fits |
| backlog-adp@verify-4 | 596 | 0 | 191,760 (1.918) | fits |
| backlog-adp@verify-5 | 596 | 0 | 175,046 (1.750) | fits |
| backlog-adp@verify-6 | 597 | 0 | 197,872 (1.979) | fits |
| backlog-adp@verify-7 | 597 | 0 | 191,711 (1.917) | fits |
| save | 617 | 0 | 136,958 (1.370) | fits |
| backlog | 303 | 0 | 162,557 (1.626) | fits |
| backlog-adp | 310 | 0 | 190,868 (1.909) | fits |
| backlog-adp-refill | 315 | 0 | 190,868 (1.909) | fits |
| backlog-owed | 358 | 0 | 195,358 (1.954) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 539,596 | 5.396 | 20 | 20 | fits | 157,056 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 185,940 | 1.859 | 20 | 200 | fits | 125,525 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 685,305 | 6.853 | 20 | 200 | fits | 157,056 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 186,852 | 1.869 | 20 | 20 | fits | 125,525 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 929,914 | 9.299 | 20 | 20 | fits | 110,713 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 190,437 | 1.904 | 20 | 24 | fits | 125,525 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,664,307 | 16.643 | 20 | 24 | fits | 68,598 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 189,397 | 1.894 | 20 | 50 | fits | 125,525 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 688,981 | 6.890 | 20 | 50 | fits | 157,056 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 380,852 | 3.809 | 18 | 18 | fits | 191,910 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,714,362 | 17.144 | 18 | 18 | fits | 52,590 | 20 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 475,389 | 4.754 | 20 | 20 | fits | 157,056 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 121,733 | 1.217 | 20 | 200 | fits | 125,193 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 621,098 | 6.211 | 20 | 200 | fits | 157,056 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 122,645 | 1.226 | 20 | 20 | fits | 125,193 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 853,056 | 8.531 | 20 | 20 | fits | 98,062 | 30 | 0.735 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 126,230 | 1.262 | 20 | 24 | fits | 125,193 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,617,972 | 16.180 | 20 | 24 | fits | 68,375 | 31 | 0.696 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 125,190 | 1.252 | 20 | 50 | fits | 125,193 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 624,774 | 6.248 | 20 | 50 | fits | 157,056 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 316,645 | 3.166 | 18 | 18 | fits | 191,910 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,654,493 | 16.545 | 18 | 18 | fits | 39,056 | 17 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 491,915 | 4.919 | 20 | 20 | fits | 157,056 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 138,259 | 1.383 | 20 | 200 | fits | 125,193 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 637,624 | 6.376 | 20 | 200 | fits | 157,056 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 139,171 | 1.392 | 20 | 20 | fits | 125,193 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 855,433 | 8.554 | 20 | 20 | fits | 117,280 | 40 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 142,756 | 1.428 | 20 | 24 | fits | 125,193 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,615,389 | 16.154 | 20 | 24 | fits | 68,655 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 141,716 | 1.417 | 20 | 50 | fits | 125,193 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 641,300 | 6.413 | 20 | 50 | fits | 157,056 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 333,171 | 3.332 | 18 | 18 | fits | 191,910 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,665,400 | 16.654 | 18 | 18 | fits | 52,546 | 20 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 488,223 | 4.882 | 20 | 20 | fits | 123,550 | 74 | 0.612 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 134,567 | 1.346 | 20 | 200 | fits | 125,193 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 600,426 | 6.004 | 20 | 200 | fits | 123,550 | 74 | 0.612 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 135,479 | 1.355 | 20 | 20 | fits | 125,193 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 850,893 | 8.509 | 20 | 20 | fits | 111,066 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 139,064 | 1.391 | 20 | 24 | fits | 125,193 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,598,080 | 15.981 | 20 | 24 | fits | 55,878 | 27 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 138,024 | 1.380 | 20 | 50 | fits | 125,193 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 604,102 | 6.041 | 20 | 50 | fits | 123,550 | 74 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 329,479 | 3.295 | 18 | 18 | fits | 191,910 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,692,801 | 16.928 | 18 | 18 | fits | 38,084 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 491,130 | 4.911 | 20 | 20 | fits | 163,871 | 89 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 130,875 | 1.309 | 20 | 200 | fits | 125,193 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 637,055 | 6.371 | 20 | 200 | fits | 163,871 | 89 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 131,787 | 1.318 | 20 | 20 | fits | 125,193 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 882,301 | 8.823 | 20 | 20 | fits | 110,905 | 34 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 135,372 | 1.354 | 20 | 24 | fits | 125,193 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,614,444 | 16.144 | 20 | 24 | fits | 68,784 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 134,332 | 1.343 | 20 | 50 | fits | 125,193 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 640,731 | 6.407 | 20 | 50 | fits | 163,871 | 89 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 325,787 | 3.258 | 18 | 18 | fits | 191,910 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,664,499 | 16.645 | 18 | 18 | fits | 52,590 | 20 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 487,217 | 4.872 | 20 | 20 | fits | 157,548 | 83 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 127,183 | 1.272 | 20 | 200 | fits | 125,193 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 633,254 | 6.333 | 20 | 200 | fits | 157,548 | 83 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 128,095 | 1.281 | 20 | 20 | fits | 125,193 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 878,259 | 8.783 | 20 | 20 | fits | 110,905 | 34 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 131,680 | 1.317 | 20 | 24 | fits | 125,193 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,629,519 | 16.295 | 20 | 24 | fits | 68,390 | 31 | 0.696 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 130,640 | 1.306 | 20 | 50 | fits | 125,193 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 636,930 | 6.369 | 20 | 50 | fits | 157,548 | 83 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 322,095 | 3.221 | 18 | 18 | fits | 191,910 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,666,107 | 16.661 | 18 | 18 | fits | 39,123 | 17 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 446,195 | 4.462 | 20 | 20 | fits | 159,171 | 83 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 123,491 | 1.235 | 20 | 200 | fits | 125,193 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 593,259 | 5.933 | 20 | 200 | fits | 159,171 | 83 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 124,403 | 1.244 | 20 | 20 | fits | 125,193 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 838,323 | 8.383 | 20 | 20 | fits | 110,888 | 34 | 0.711 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 127,988 | 1.280 | 20 | 24 | fits | 125,193 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,571,485 | 15.715 | 20 | 24 | fits | 68,598 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 126,948 | 1.269 | 20 | 50 | fits | 125,193 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 596,935 | 5.969 | 20 | 50 | fits | 159,171 | 83 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 437,699 | 4.377 | 18 | 18 | fits | 190,350 | 104 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,672,857 | 16.729 | 18 | 18 | fits | 51,317 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 529,755 | 5.298 | 20 | 20 | fits | 144,189 | 60 | 0.674 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 180,839 | 1.808 | 20 | 200 | fits | 125,427 | 142 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 662,586 | 6.626 | 20 | 200 | fits | 144,189 | 60 | 0.674 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 181,751 | 1.818 | 20 | 20 | fits | 125,427 | 142 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 906,596 | 9.066 | 20 | 20 | fits | 110,588 | 34 | 0.706 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 59,909 | 0.599 | 20 | 24 | fits | 60,806 | 65 | 0.557 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,590,266 | 15.903 | 20 | 24 | fits | 68,390 | 31 | 0.696 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 58,869 | 0.589 | 20 | 50 | fits | 60,806 | 65 | 0.557 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 522,073 | 5.221 | 20 | 50 | fits | 140,088 | 76 | 0.646 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 381,920 | 3.819 | 18 | 18 | fits | 198,079 | 145 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,678,082 | 16.781 | 18 | 18 | fits | 37,952 | 15 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 473,689 | 4.737 | 20 | 20 | fits | 157,121 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 120,892 | 1.209 | 20 | 200 | fits | 125,537 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 619,398 | 6.194 | 20 | 200 | fits | 157,121 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 121,804 | 1.218 | 20 | 20 | fits | 125,537 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 864,072 | 8.641 | 20 | 20 | fits | 110,778 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 125,389 | 1.254 | 20 | 24 | fits | 125,537 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,598,465 | 15.985 | 20 | 24 | fits | 68,598 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 124,349 | 1.243 | 20 | 50 | fits | 125,537 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 623,074 | 6.231 | 20 | 50 | fits | 157,121 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 314,880 | 3.149 | 18 | 18 | fits | 190,986 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,648,520 | 16.485 | 18 | 18 | fits | 52,590 | 20 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 486,523 | 4.865 | 20 | 20 | fits | 157,121 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 133,726 | 1.337 | 20 | 200 | fits | 125,537 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 632,232 | 6.322 | 20 | 200 | fits | 157,121 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 134,638 | 1.346 | 20 | 20 | fits | 125,537 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 883,529 | 8.835 | 20 | 20 | fits | 110,996 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 138,223 | 1.382 | 20 | 24 | fits | 125,537 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,641,859 | 16.419 | 20 | 24 | fits | 68,516 | 31 | 0.696 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 137,183 | 1.372 | 20 | 50 | fits | 125,537 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 635,908 | 6.359 | 20 | 50 | fits | 157,121 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 327,714 | 3.277 | 18 | 18 | fits | 190,986 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,639,324 | 16.393 | 18 | 18 | fits | 68,516 | 31 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 452,119 | 4.521 | 20 | 20 | fits | 162,719 | 89 | 0.647 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 126,342 | 1.263 | 20 | 200 | fits | 125,537 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 596,505 | 5.965 | 20 | 200 | fits | 162,719 | 89 | 0.647 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 127,254 | 1.273 | 20 | 20 | fits | 125,537 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 842,023 | 8.420 | 20 | 20 | fits | 111,090 | 34 | 0.711 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 130,839 | 1.308 | 20 | 24 | fits | 125,537 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,606,974 | 16.070 | 20 | 24 | fits | 68,533 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 129,799 | 1.298 | 20 | 50 | fits | 125,537 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 600,181 | 6.002 | 20 | 50 | fits | 162,719 | 89 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 320,330 | 3.203 | 18 | 18 | fits | 190,986 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,656,969 | 16.570 | 18 | 18 | fits | 52,530 | 20 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 498,123 | 4.981 | 20 | 20 | fits | 157,121 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 139,084 | 1.391 | 20 | 200 | fits | 125,537 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 643,832 | 6.438 | 20 | 200 | fits | 157,121 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 139,996 | 1.400 | 20 | 20 | fits | 125,537 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 888,506 | 8.885 | 20 | 20 | fits | 110,778 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 143,581 | 1.436 | 20 | 24 | fits | 125,537 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,640,363 | 16.404 | 20 | 24 | fits | 68,390 | 31 | 0.696 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 142,541 | 1.425 | 20 | 50 | fits | 125,537 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 647,508 | 6.475 | 20 | 50 | fits | 157,121 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 339,314 | 3.393 | 18 | 18 | fits | 197,228 | 145 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,676,951 | 16.770 | 18 | 18 | fits | 39,123 | 17 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 490,809 | 4.908 | 20 | 20 | fits | 157,121 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 137,854 | 1.379 | 20 | 200 | fits | 125,975 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 636,518 | 6.365 | 20 | 200 | fits | 157,121 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 138,766 | 1.388 | 20 | 20 | fits | 125,975 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 881,192 | 8.812 | 20 | 20 | fits | 110,778 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 142,351 | 1.424 | 20 | 24 | fits | 125,975 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,644,797 | 16.448 | 20 | 24 | fits | 68,394 | 31 | 0.696 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 141,311 | 1.413 | 20 | 50 | fits | 125,975 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 640,194 | 6.402 | 20 | 50 | fits | 157,121 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 332,041 | 3.320 | 18 | 18 | fits | 191,185 | 140 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,642,262 | 16.423 | 18 | 18 | fits | 68,394 | 31 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 483,646 | 4.836 | 20 | 20 | fits | 157,121 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 131,012 | 1.310 | 20 | 200 | fits | 125,606 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 629,355 | 6.294 | 20 | 200 | fits | 157,121 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 131,924 | 1.319 | 20 | 20 | fits | 125,606 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 880,652 | 8.807 | 20 | 20 | fits | 110,996 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 135,509 | 1.355 | 20 | 24 | fits | 125,606 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,638,982 | 16.390 | 20 | 24 | fits | 68,516 | 31 | 0.696 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 134,469 | 1.345 | 20 | 50 | fits | 125,606 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 633,031 | 6.330 | 20 | 50 | fits | 157,121 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 324,878 | 3.249 | 18 | 18 | fits | 190,864 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,636,447 | 16.364 | 18 | 18 | fits | 68,516 | 31 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 449,283 | 4.493 | 20 | 20 | fits | 162,678 | 89 | 0.647 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 123,628 | 1.236 | 20 | 200 | fits | 125,606 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 593,628 | 5.936 | 20 | 200 | fits | 162,678 | 89 | 0.647 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 124,540 | 1.245 | 20 | 20 | fits | 125,606 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 839,146 | 8.391 | 20 | 20 | fits | 111,090 | 34 | 0.711 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 128,125 | 1.281 | 20 | 24 | fits | 125,606 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,604,097 | 16.041 | 20 | 24 | fits | 68,533 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 127,085 | 1.271 | 20 | 50 | fits | 125,606 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 597,304 | 5.973 | 20 | 50 | fits | 162,678 | 89 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 317,494 | 3.175 | 18 | 18 | fits | 190,864 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,654,092 | 16.541 | 18 | 18 | fits | 52,530 | 20 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 495,338 | 4.953 | 20 | 20 | fits | 157,121 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 136,462 | 1.365 | 20 | 200 | fits | 125,606 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 641,047 | 6.410 | 20 | 200 | fits | 157,121 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 137,374 | 1.374 | 20 | 20 | fits | 125,606 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 885,721 | 8.857 | 20 | 20 | fits | 110,778 | 34 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 140,959 | 1.410 | 20 | 24 | fits | 125,606 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,637,578 | 16.376 | 20 | 24 | fits | 68,390 | 31 | 0.696 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 139,919 | 1.399 | 20 | 50 | fits | 125,606 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 644,723 | 6.447 | 20 | 50 | fits | 157,121 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 336,570 | 3.366 | 18 | 18 | fits | 197,106 | 145 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,674,166 | 16.742 | 18 | 18 | fits | 39,123 | 17 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 492,933 | 4.929 | 20 | 20 | fits | 156,964 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 139,519 | 1.395 | 20 | 200 | fits | 125,742 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 638,550 | 6.386 | 20 | 200 | fits | 156,964 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 140,431 | 1.404 | 20 | 20 | fits | 125,742 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 883,248 | 8.832 | 20 | 20 | fits | 110,837 | 34 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 144,016 | 1.440 | 20 | 24 | fits | 125,742 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,668,364 | 16.684 | 20 | 24 | fits | 69,260 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 142,976 | 1.430 | 20 | 50 | fits | 125,742 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 642,226 | 6.422 | 20 | 50 | fits | 156,964 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 334,281 | 3.343 | 18 | 18 | fits | 191,760 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,705,090 | 17.051 | 18 | 18 | fits | 39,261 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 489,241 | 4.892 | 20 | 20 | fits | 156,964 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 135,827 | 1.358 | 20 | 200 | fits | 125,676 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 634,858 | 6.349 | 20 | 200 | fits | 156,964 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 136,739 | 1.367 | 20 | 20 | fits | 125,676 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 885,894 | 8.859 | 20 | 20 | fits | 117,175 | 40 | 0.719 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 140,324 | 1.403 | 20 | 24 | fits | 125,676 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,678,741 | 16.787 | 20 | 24 | fits | 68,703 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 139,284 | 1.393 | 20 | 50 | fits | 125,676 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 638,534 | 6.385 | 20 | 50 | fits | 156,964 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 330,589 | 3.306 | 18 | 18 | fits | 191,760 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,676,206 | 16.762 | 18 | 18 | fits | 68,703 | 31 | 0.699 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 485,549 | 4.855 | 20 | 20 | fits | 156,964 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 132,135 | 1.321 | 20 | 200 | fits | 125,676 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 631,166 | 6.312 | 20 | 200 | fits | 156,964 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 133,047 | 1.330 | 20 | 20 | fits | 125,676 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 882,487 | 8.825 | 20 | 20 | fits | 111,055 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 136,632 | 1.366 | 20 | 24 | fits | 125,676 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,643,778 | 16.438 | 20 | 24 | fits | 37,511 | 22 | 0.659 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 135,592 | 1.356 | 20 | 50 | fits | 125,676 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 634,842 | 6.348 | 20 | 50 | fits | 156,964 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 326,897 | 3.269 | 18 | 18 | fits | 191,760 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,701,272 | 17.013 | 18 | 18 | fits | 60,029 | 26 | 0.753 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 481,857 | 4.819 | 20 | 20 | fits | 123,363 | 74 | 0.610 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 128,443 | 1.284 | 20 | 200 | fits | 125,676 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 593,873 | 5.939 | 20 | 200 | fits | 123,363 | 74 | 0.610 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 129,355 | 1.294 | 20 | 20 | fits | 125,676 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 844,464 | 8.445 | 20 | 20 | fits | 111,190 | 34 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 132,940 | 1.329 | 20 | 24 | fits | 125,676 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,644,635 | 16.446 | 20 | 24 | fits | 69,073 | 31 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 131,900 | 1.319 | 20 | 50 | fits | 125,676 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 597,549 | 5.975 | 20 | 50 | fits | 123,363 | 74 | 0.610 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 323,205 | 3.232 | 18 | 18 | fits | 191,760 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,694,650 | 16.947 | 18 | 18 | fits | 52,550 | 20 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 451,050 | 4.511 | 20 | 20 | fits | 162,654 | 89 | 0.647 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 124,751 | 1.248 | 20 | 200 | fits | 125,676 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 595,436 | 5.954 | 20 | 200 | fits | 162,654 | 89 | 0.647 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 125,663 | 1.257 | 20 | 20 | fits | 125,676 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 840,978 | 8.410 | 20 | 20 | fits | 111,149 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 129,248 | 1.292 | 20 | 24 | fits | 125,676 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,639,436 | 16.394 | 20 | 24 | fits | 68,803 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 128,208 | 1.282 | 20 | 50 | fits | 125,676 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 599,112 | 5.991 | 20 | 50 | fits | 162,654 | 89 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 319,513 | 3.195 | 18 | 18 | fits | 191,760 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,689,451 | 16.895 | 18 | 18 | fits | 52,550 | 20 | 0.719 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 469,293 | 4.693 | 20 | 20 | fits | 158,008 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 121,059 | 1.211 | 20 | 200 | fits | 125,676 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 615,408 | 6.154 | 20 | 200 | fits | 158,008 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 121,971 | 1.220 | 20 | 20 | fits | 125,676 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 860,407 | 8.604 | 20 | 20 | fits | 110,864 | 34 | 0.711 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 125,556 | 1.256 | 20 | 24 | fits | 125,676 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,657,410 | 16.574 | 20 | 24 | fits | 101,854 | 45 | 0.738 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 124,516 | 1.245 | 20 | 50 | fits | 125,676 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 619,084 | 6.191 | 20 | 50 | fits | 158,008 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 285,965 | 2.860 | 18 | 18 | fits | 161,904 | 136 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,694,500 | 16.945 | 18 | 18 | fits | 39,625 | 17 | 0.793 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 497,111 | 4.971 | 20 | 20 | fits | 156,964 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 137,585 | 1.376 | 20 | 200 | fits | 125,676 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 642,728 | 6.427 | 20 | 200 | fits | 156,964 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 138,497 | 1.385 | 20 | 20 | fits | 125,676 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 887,426 | 8.874 | 20 | 20 | fits | 110,837 | 34 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 142,082 | 1.421 | 20 | 24 | fits | 125,676 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,640,924 | 16.409 | 20 | 24 | fits | 100,887 | 45 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 141,042 | 1.410 | 20 | 50 | fits | 125,676 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 646,404 | 6.464 | 20 | 50 | fits | 156,964 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 338,459 | 3.385 | 18 | 18 | fits | 197,872 | 145 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,729,229 | 17.292 | 18 | 18 | fits | 37,906 | 15 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 493,166 | 4.932 | 20 | 20 | fits | 156,964 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 139,801 | 1.398 | 20 | 200 | fits | 126,050 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 638,783 | 6.388 | 20 | 200 | fits | 156,964 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 140,713 | 1.407 | 20 | 20 | fits | 126,050 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 883,481 | 8.835 | 20 | 20 | fits | 110,837 | 34 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 144,298 | 1.443 | 20 | 24 | fits | 126,050 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,616,221 | 16.162 | 20 | 24 | fits | 37,381 | 22 | 0.655 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 143,258 | 1.433 | 20 | 50 | fits | 126,050 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 642,459 | 6.425 | 20 | 50 | fits | 156,964 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 334,514 | 3.345 | 18 | 18 | fits | 191,711 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,700,028 | 17.000 | 18 | 18 | fits | 86,342 | 34 | 0.775 |
| an event behind 15 others | `backlog.event.if0` | 153,539 | 1.535 | 20 | 200 | fits | 124,291 | 125 | 0.536 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 701,126 | 7.011 | 20 | 20 | fits | 85,790 | 37 | 0.638 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 142,808 | 1.428 | 20 | 200 | fits | 143,016 | 143 | 0.538 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 562,884 | 5.629 | 20 | 200 | fits | 133,837 | 57 | 0.692 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 138,549 | 1.385 | 20 | 20 | fits | 143,016 | 143 | 0.538 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 750,703 | 7.507 | 20 | 20 | fits | 85,790 | 37 | 0.638 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 142,134 | 1.421 | 20 | 24 | fits | 143,016 | 143 | 0.538 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,298,889 | 12.989 | 20 | 24 | fits | 53,712 | 31 | 0.693 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 141,094 | 1.411 | 20 | 50 | fits | 143,016 | 143 | 0.538 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 561,389 | 5.614 | 20 | 50 | fits | 133,837 | 57 | 0.692 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 561,324 | 5.613 | 18 | 18 | fits | 133,837 | 57 | 0.692 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,442,064 | 14.421 | 18 | 18 | fits | 36,092 | 18 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 442,191 | 4.422 | 20 | 20 | fits | 162,670 | 89 | 0.647 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 117,174 | 1.172 | 20 | 200 | fits | 121,856 | 140 | 0.488 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 586,706 | 5.867 | 20 | 200 | fits | 162,670 | 89 | 0.647 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 118,086 | 1.181 | 20 | 20 | fits | 121,856 | 140 | 0.488 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 831,287 | 8.313 | 20 | 20 | fits | 110,494 | 34 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 121,671 | 1.217 | 20 | 24 | fits | 121,856 | 140 | 0.488 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,596,363 | 15.964 | 20 | 24 | fits | 68,528 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 120,631 | 1.206 | 20 | 50 | fits | 121,856 | 140 | 0.488 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 590,382 | 5.904 | 20 | 50 | fits | 162,670 | 89 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 311,044 | 3.110 | 18 | 18 | fits | 190,868 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,646,353 | 16.464 | 18 | 18 | fits | 52,525 | 20 | 0.719 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,183 | 0.122 | 20 | 20 | fits | 46,433 | 21 | 0.759 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 117,174 | 1.172 | 20 | 200 | fits | 121,856 | 140 | 0.488 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 50,089 | 0.501 | 20 | 200 | fits | 46,433 | 21 | 0.759 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 118,086 | 1.181 | 20 | 20 | fits | 121,856 | 140 | 0.488 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 810,738 | 8.107 | 20 | 20 | fits | 121,490 | 46 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 121,671 | 1.217 | 20 | 24 | fits | 121,856 | 140 | 0.488 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,510,482 | 15.105 | 20 | 24 | fits | 68,820 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 120,631 | 1.206 | 20 | 50 | fits | 121,856 | 140 | 0.488 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 570,026 | 5.700 | 20 | 50 | fits | 142,314 | 79 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 311,044 | 3.110 | 18 | 18 | fits | 190,868 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,611,758 | 16.118 | 18 | 18 | fits | 51,261 | 18 | 0.707 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,419,436 | 64.194 | 20 | 20 | MISS ceiling | 53,053 | 27 | 0.572 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,050,811 | 360.508 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,050,736 | 360.507 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,050,661 | 360.507 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,050,586 | 360.506 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 127,086 | 1.271 | 20 | 200 | fits | 119,385 | 134 | 0.504 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 607,066 | 6.071 | 20 | 200 | fits | 136,175 | 69 | 0.662 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 122,827 | 1.228 | 20 | 20 | fits | 119,385 | 134 | 0.504 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 811,602 | 8.116 | 20 | 20 | fits | 102,848 | 35 | 0.746 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 126,412 | 1.264 | 20 | 24 | fits | 119,385 | 134 | 0.504 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,531,179 | 65.312 | 20 | 24 | MISS ceiling | 34,634 | 23 | 0.543 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 125,372 | 1.254 | 20 | 50 | fits | 119,385 | 134 | 0.504 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 605,571 | 6.056 | 20 | 50 | fits | 136,175 | 69 | 0.662 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 320,275 | 3.203 | 18 | 18 | fits | 195,358 | 138 | 0.641 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,383,093 | 13.831 | 18 | 18 | fits | 51,215 | 21 | 0.677 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
