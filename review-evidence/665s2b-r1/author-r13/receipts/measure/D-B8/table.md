### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 313 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.372 (7.066) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.961 (7.177) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.248 (0.808) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.389 (2.369) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.756 (64.176) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.467 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.810 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 8.394 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.801 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.238 | fits | 7 adp | 26 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.346 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.846 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.143 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.836 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.275 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.064 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-5.service.srp.last.if1` (backlog-adp@verify-5) | 15.459 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 16.735 | 17 | 176,393 (1.764) | yes | - |
| backlog-adp@blank-1 | 0 | 16.062 | 17 | 176,510 (1.765) | yes | - |
| backlog-adp@blank-2 | 0 | 16.358 | 18 | 176,438 (1.764) | yes | - |
| backlog-adp@blank-3 | 0 | 17.426 | 19 | 176,438 (1.764) | yes | - |
| backlog-adp@blank-4 | 0 | 16.380 | 18 | 176,510 (1.765) | yes | - |
| backlog-adp@blank-5 | 0 | 16.475 | 19 | 176,510 (1.765) | yes | - |
| backlog-adp@blank-6 | 0 | 16.347 | 18 | 175,031 (1.750) | yes | - |
| backlog-adp@blank-7 | 0 | 16.078 | 17 | 183,027 (1.830) | yes | - |
| backlog-adp@program-0 | 0 | 16.407 | 18 | 175,549 (1.755) | yes | - |
| backlog-adp@program-1 | 0 | 16.301 | 18 | 175,621 (1.756) | yes | - |
| backlog-adp@program-2 | 0 | 16.367 | 18 | 175,549 (1.755) | yes | - |
| backlog-adp@program-3 | 0 | 16.415 | 18 | 182,210 (1.822) | yes | - |
| backlog-adp@program-4 | 0 | 15.674 | 18 | 175,587 (1.756) | yes | - |
| backlog-adp@program-5 | 0 | 15.567 | 18 | 175,515 (1.755) | yes | - |
| backlog-adp@program-6 | 0 | 15.635 | 18 | 175,587 (1.756) | yes | - |
| backlog-adp@program-7 | 0 | 15.682 | 18 | 182,200 (1.822) | yes | - |
| backlog-adp@verify-0 | 0 | 16.285 | 16 | 176,342 (1.763) | yes | - |
| backlog-adp@verify-1 | 0 | 16.373 | 17 | 176,234 (1.762) | yes | - |
| backlog-adp@verify-2 | 0 | 17.834 | 19 | 176,306 (1.763) | yes | - |
| backlog-adp@verify-3 | 0 | 16.816 | 19 | 176,306 (1.763) | yes | - |
| backlog-adp@verify-4 | 0 | 16.682 | 18 | 176,234 (1.762) | yes | - |
| backlog-adp@verify-5 | 0 | 16.846 | 19 | 176,234 (1.762) | yes | - |
| backlog-adp@verify-6 | 0 | 17.118 | 19 | 182,873 (1.829) | yes | - |
| backlog-adp@verify-7 | 1 | 16.765 | 18 | 177,361 (1.774) | yes | - |
| backlog | 0 | 13.559 | 19 | 149,768 (1.498) | yes | - |
| backlog-adp | 0 | 15.450 | 18 | 175,331 (1.753) | yes | - |
| backlog-adp-refill | 0 | 41.336 | 24 | 175,331 (1.753) | yes | - |
| backlog-owed | 0 | 360.518 | 64 | 182,113 (1.821) | yes | - |

Composed maximum over the 4 backlog windows: 182,113 CPU cycles (1.821 ms), backlog-owed.
Over the windows that released their whole load only: 182,113 (1.821 ms), backlog-owed.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 380 | 0 | 176,393 (1.764) | fits |
| backlog-adp@blank-1 | 380 | 0 | 176,510 (1.765) | fits |
| backlog-adp@blank-2 | 381 | 0 | 176,438 (1.764) | fits |
| backlog-adp@blank-3 | 382 | 0 | 176,438 (1.764) | fits |
| backlog-adp@blank-4 | 381 | 0 | 176,510 (1.765) | fits |
| backlog-adp@blank-5 | 382 | 0 | 176,510 (1.765) | fits |
| backlog-adp@blank-6 | 381 | 0 | 175,031 (1.750) | fits |
| backlog-adp@blank-7 | 380 | 0 | 183,027 (1.830) | fits |
| backlog-adp@program-0 | 490 | 0 | 175,549 (1.755) | fits |
| backlog-adp@program-1 | 490 | 0 | 175,621 (1.756) | fits |
| backlog-adp@program-2 | 490 | 0 | 175,549 (1.755) | fits |
| backlog-adp@program-3 | 490 | 0 | 182,210 (1.822) | fits |
| backlog-adp@program-4 | 491 | 0 | 175,587 (1.756) | fits |
| backlog-adp@program-5 | 491 | 0 | 175,515 (1.755) | fits |
| backlog-adp@program-6 | 491 | 0 | 175,587 (1.756) | fits |
| backlog-adp@program-7 | 491 | 0 | 182,200 (1.822) | fits |
| backlog-adp@verify-0 | 595 | 0 | 176,342 (1.763) | fits |
| backlog-adp@verify-1 | 595 | 0 | 176,234 (1.762) | fits |
| backlog-adp@verify-2 | 597 | 0 | 176,306 (1.763) | fits |
| backlog-adp@verify-3 | 597 | 0 | 176,306 (1.763) | fits |
| backlog-adp@verify-4 | 596 | 0 | 176,234 (1.762) | fits |
| backlog-adp@verify-5 | 597 | 0 | 176,234 (1.762) | fits |
| backlog-adp@verify-6 | 597 | 0 | 182,873 (1.829) | fits |
| backlog-adp@verify-7 | 597 | 0 | 177,361 (1.774) | fits |
| save | 617 | 0 | 130,534 (1.305) | fits |
| backlog | 302 | 0 | 149,768 (1.498) | fits |
| backlog-adp | 310 | 0 | 175,331 (1.753) | fits |
| backlog-adp-refill | 316 | 0 | 175,331 (1.753) | fits |
| backlog-owed | 358 | 0 | 182,113 (1.821) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 496,057 | 4.961 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 180,098 | 1.801 | 20 | 200 | fits | 108,764 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 623,842 | 6.238 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 181,010 | 1.810 | 20 | 20 | fits | 108,764 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 839,366 | 8.394 | 20 | 20 | fits | 97,565 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 184,595 | 1.846 | 20 | 24 | fits | 108,764 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,537,670 | 15.377 | 20 | 24 | fits | 62,345 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 183,555 | 1.836 | 20 | 50 | fits | 108,764 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 627,518 | 6.275 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 359,493 | 3.595 | 18 | 18 | fits | 176,393 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,535,135 | 15.351 | 18 | 18 | fits | 62,345 | 31 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 428,648 | 4.286 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 112,572 | 1.126 | 20 | 200 | fits | 108,588 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 556,433 | 5.564 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 113,484 | 1.135 | 20 | 20 | fits | 108,588 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 771,957 | 7.720 | 20 | 20 | fits | 97,565 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 117,069 | 1.171 | 20 | 24 | fits | 108,588 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,470,369 | 14.704 | 20 | 24 | fits | 62,345 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 116,029 | 1.160 | 20 | 50 | fits | 108,588 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 560,109 | 5.601 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 292,084 | 2.921 | 18 | 18 | fits | 176,510 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,467,834 | 14.678 | 18 | 18 | fits | 62,345 | 31 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 437,226 | 4.372 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 121,222 | 1.212 | 20 | 200 | fits | 108,588 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 565,011 | 5.650 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 122,134 | 1.221 | 20 | 20 | fits | 108,588 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 752,419 | 7.524 | 20 | 20 | fits | 69,449 | 25 | 0.665 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 125,719 | 1.257 | 20 | 24 | fits | 108,588 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,452,283 | 14.523 | 20 | 24 | fits | 62,345 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 124,679 | 1.247 | 20 | 50 | fits | 108,588 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 568,687 | 5.687 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 300,662 | 3.007 | 18 | 18 | fits | 176,438 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,497,929 | 14.979 | 18 | 18 | fits | 48,181 | 20 | 0.771 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 426,954 | 4.270 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 110,950 | 1.109 | 20 | 200 | fits | 108,588 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 554,739 | 5.547 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 111,862 | 1.119 | 20 | 20 | fits | 108,588 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 749,030 | 7.490 | 20 | 20 | fits | 105,855 | 40 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 115,447 | 1.154 | 20 | 24 | fits | 108,588 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,438,547 | 14.385 | 20 | 24 | fits | 62,321 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 114,407 | 1.144 | 20 | 50 | fits | 108,588 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 558,415 | 5.584 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 290,390 | 2.904 | 18 | 18 | fits | 176,438 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,484,004 | 14.840 | 18 | 18 | fits | 47,992 | 20 | 0.767 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 435,768 | 4.358 | 20 | 20 | fits | 109,053 | 74 | 0.606 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 119,692 | 1.197 | 20 | 200 | fits | 108,588 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 534,101 | 5.341 | 20 | 200 | fits | 109,053 | 74 | 0.606 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 120,604 | 1.206 | 20 | 20 | fits | 108,588 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 757,479 | 7.575 | 20 | 20 | fits | 97,649 | 34 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 124,189 | 1.242 | 20 | 24 | fits | 108,588 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,446,952 | 14.470 | 20 | 24 | fits | 62,346 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 123,149 | 1.231 | 20 | 50 | fits | 108,588 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 537,777 | 5.378 | 20 | 50 | fits | 109,053 | 74 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 299,204 | 2.992 | 18 | 18 | fits | 176,510 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,500,200 | 15.002 | 18 | 18 | fits | 55,783 | 26 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 403,845 | 4.038 | 20 | 20 | fits | 145,893 | 89 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 109,328 | 1.093 | 20 | 200 | fits | 108,588 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 531,120 | 5.311 | 20 | 200 | fits | 145,893 | 89 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 110,240 | 1.102 | 20 | 20 | fits | 108,588 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 747,054 | 7.471 | 20 | 20 | fits | 97,866 | 34 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 113,825 | 1.138 | 20 | 24 | fits | 108,588 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,416,888 | 14.169 | 20 | 24 | fits | 70,271 | 37 | 0.725 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 112,785 | 1.128 | 20 | 50 | fits | 108,588 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 534,796 | 5.348 | 20 | 50 | fits | 145,893 | 89 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 288,840 | 2.888 | 18 | 18 | fits | 176,510 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,509,580 | 15.096 | 18 | 18 | fits | 47,011 | 18 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 408,440 | 4.084 | 20 | 20 | fits | 140,311 | 83 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 118,070 | 1.181 | 20 | 200 | fits | 108,588 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 537,395 | 5.374 | 20 | 200 | fits | 140,311 | 83 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 118,982 | 1.190 | 20 | 20 | fits | 108,588 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 752,834 | 7.528 | 20 | 20 | fits | 97,500 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 122,567 | 1.226 | 20 | 24 | fits | 108,588 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,451,148 | 14.511 | 20 | 24 | fits | 62,345 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 121,527 | 1.215 | 20 | 50 | fits | 108,588 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 541,071 | 5.411 | 20 | 50 | fits | 140,311 | 83 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 400,695 | 4.007 | 18 | 18 | fits | 175,031 | 104 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,496,769 | 14.968 | 18 | 18 | fits | 48,156 | 20 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 430,250 | 4.303 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 107,706 | 1.077 | 20 | 200 | fits | 108,588 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 558,035 | 5.580 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 108,618 | 1.086 | 20 | 20 | fits | 108,588 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 773,559 | 7.736 | 20 | 20 | fits | 97,565 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 112,203 | 1.122 | 20 | 24 | fits | 108,588 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,471,975 | 14.720 | 20 | 24 | fits | 62,345 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 111,163 | 1.112 | 20 | 50 | fits | 108,588 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 561,711 | 5.617 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 293,735 | 2.937 | 18 | 18 | fits | 183,027 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,469,440 | 14.694 | 18 | 18 | fits | 62,345 | 31 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 430,687 | 4.307 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 115,572 | 1.156 | 20 | 200 | fits | 109,219 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 558,472 | 5.585 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 116,484 | 1.165 | 20 | 20 | fits | 109,219 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 774,061 | 7.741 | 20 | 20 | fits | 97,630 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 120,069 | 1.201 | 20 | 24 | fits | 109,219 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,463,312 | 14.633 | 20 | 24 | fits | 62,493 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 119,029 | 1.190 | 20 | 50 | fits | 109,219 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 562,148 | 5.621 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 294,123 | 2.941 | 18 | 18 | fits | 175,549 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,497,093 | 14.971 | 18 | 18 | fits | 36,316 | 17 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 429,137 | 4.291 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 113,950 | 1.139 | 20 | 200 | fits | 109,219 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 556,922 | 5.569 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 114,862 | 1.149 | 20 | 20 | fits | 109,219 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 751,278 | 7.513 | 20 | 20 | fits | 105,920 | 40 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 118,447 | 1.184 | 20 | 24 | fits | 109,219 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,440,795 | 14.408 | 20 | 24 | fits | 62,321 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 117,407 | 1.174 | 20 | 50 | fits | 109,219 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 560,598 | 5.606 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 292,573 | 2.926 | 18 | 18 | fits | 175,621 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,486,252 | 14.863 | 18 | 18 | fits | 47,992 | 20 | 0.767 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 405,884 | 4.059 | 20 | 20 | fits | 145,893 | 89 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 112,328 | 1.123 | 20 | 200 | fits | 109,219 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 533,159 | 5.332 | 20 | 200 | fits | 145,893 | 89 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 113,240 | 1.132 | 20 | 20 | fits | 109,219 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 749,158 | 7.492 | 20 | 20 | fits | 97,931 | 34 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 116,825 | 1.168 | 20 | 24 | fits | 109,219 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,447,279 | 14.473 | 20 | 24 | fits | 71,086 | 37 | 0.736 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 115,785 | 1.158 | 20 | 50 | fits | 109,219 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 536,835 | 5.368 | 20 | 50 | fits | 145,893 | 89 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 290,879 | 2.909 | 18 | 18 | fits | 175,549 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,492,900 | 14.929 | 18 | 18 | fits | 48,156 | 20 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 432,433 | 4.324 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 110,706 | 1.107 | 20 | 200 | fits | 109,219 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 560,218 | 5.602 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 111,618 | 1.116 | 20 | 20 | fits | 109,219 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 775,807 | 7.758 | 20 | 20 | fits | 97,630 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 115,203 | 1.152 | 20 | 24 | fits | 109,219 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,464,106 | 14.641 | 20 | 24 | fits | 62,493 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 114,163 | 1.142 | 20 | 50 | fits | 109,219 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 563,894 | 5.639 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 295,918 | 2.959 | 18 | 18 | fits | 182,210 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,497,887 | 14.979 | 18 | 18 | fits | 36,316 | 17 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 434,226 | 4.342 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 119,122 | 1.191 | 20 | 200 | fits | 109,275 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 562,011 | 5.620 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 120,034 | 1.200 | 20 | 20 | fits | 109,275 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 777,600 | 7.776 | 20 | 20 | fits | 97,630 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 123,619 | 1.236 | 20 | 24 | fits | 109,275 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,466,851 | 14.669 | 20 | 24 | fits | 62,493 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 122,579 | 1.226 | 20 | 50 | fits | 109,275 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 565,687 | 5.657 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 297,711 | 2.977 | 18 | 18 | fits | 175,587 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,500,632 | 15.006 | 18 | 18 | fits | 36,316 | 17 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 432,532 | 4.325 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 117,500 | 1.175 | 20 | 200 | fits | 109,275 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 560,317 | 5.603 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 118,412 | 1.184 | 20 | 20 | fits | 109,275 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 754,673 | 7.547 | 20 | 20 | fits | 105,920 | 40 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 121,997 | 1.220 | 20 | 24 | fits | 109,275 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,444,190 | 14.442 | 20 | 24 | fits | 62,321 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 120,957 | 1.210 | 20 | 50 | fits | 109,275 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 563,993 | 5.640 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 296,017 | 2.960 | 18 | 18 | fits | 175,515 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,489,647 | 14.896 | 18 | 18 | fits | 47,992 | 20 | 0.767 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 409,524 | 4.095 | 20 | 20 | fits | 145,848 | 89 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 115,878 | 1.159 | 20 | 200 | fits | 109,275 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 536,754 | 5.368 | 20 | 200 | fits | 145,848 | 89 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 116,790 | 1.168 | 20 | 20 | fits | 109,275 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 752,753 | 7.528 | 20 | 20 | fits | 97,931 | 34 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 120,375 | 1.204 | 20 | 24 | fits | 109,275 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,450,874 | 14.509 | 20 | 24 | fits | 71,086 | 37 | 0.736 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 119,335 | 1.193 | 20 | 50 | fits | 109,275 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 540,430 | 5.404 | 20 | 50 | fits | 145,848 | 89 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 294,467 | 2.945 | 18 | 18 | fits | 175,587 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,496,495 | 14.965 | 18 | 18 | fits | 48,156 | 20 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 435,973 | 4.360 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 114,256 | 1.143 | 20 | 200 | fits | 109,275 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 563,758 | 5.638 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 115,168 | 1.152 | 20 | 20 | fits | 109,275 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 779,347 | 7.793 | 20 | 20 | fits | 97,630 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 118,753 | 1.188 | 20 | 24 | fits | 109,275 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,467,646 | 14.676 | 20 | 24 | fits | 62,493 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 117,713 | 1.177 | 20 | 50 | fits | 109,275 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 567,434 | 5.674 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 299,458 | 2.995 | 18 | 18 | fits | 182,200 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,501,427 | 15.014 | 18 | 18 | fits | 36,316 | 17 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 419,901 | 4.199 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 104,042 | 1.040 | 20 | 200 | fits | 108,950 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 547,686 | 5.477 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 104,954 | 1.050 | 20 | 20 | fits | 108,950 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 763,275 | 7.633 | 20 | 20 | fits | 97,630 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 108,539 | 1.085 | 20 | 24 | fits | 108,950 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,491,527 | 14.915 | 20 | 24 | fits | 92,293 | 45 | 0.748 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 107,499 | 1.075 | 20 | 50 | fits | 108,950 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 551,362 | 5.514 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 283,386 | 2.834 | 18 | 18 | fits | 176,342 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,488,992 | 14.890 | 18 | 18 | fits | 92,293 | 45 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 428,650 | 4.287 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 112,899 | 1.129 | 20 | 200 | fits | 108,774 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 556,435 | 5.564 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 113,811 | 1.138 | 20 | 20 | fits | 108,774 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 772,024 | 7.720 | 20 | 20 | fits | 97,630 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 117,396 | 1.174 | 20 | 24 | fits | 108,774 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,500,453 | 15.005 | 20 | 24 | fits | 62,618 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 116,356 | 1.164 | 20 | 50 | fits | 108,774 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 560,111 | 5.601 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 292,135 | 2.921 | 18 | 18 | fits | 176,234 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,497,918 | 14.979 | 18 | 18 | fits | 62,618 | 31 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 437,372 | 4.374 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 121,549 | 1.215 | 20 | 200 | fits | 108,774 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 565,157 | 5.652 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 122,461 | 1.225 | 20 | 20 | fits | 108,774 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 759,513 | 7.595 | 20 | 20 | fits | 105,920 | 40 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 126,046 | 1.260 | 20 | 24 | fits | 108,774 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,449,030 | 14.490 | 20 | 24 | fits | 62,321 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 125,006 | 1.250 | 20 | 50 | fits | 108,774 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 568,833 | 5.688 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 300,857 | 3.009 | 18 | 18 | fits | 176,306 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,523,483 | 15.235 | 18 | 18 | fits | 76,988 | 34 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 427,100 | 4.271 | 20 | 20 | fits | 109,053 | 74 | 0.606 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 111,277 | 1.113 | 20 | 200 | fits | 108,774 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 525,433 | 5.254 | 20 | 200 | fits | 109,053 | 74 | 0.606 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 112,189 | 1.122 | 20 | 20 | fits | 108,774 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 748,876 | 7.489 | 20 | 20 | fits | 97,714 | 34 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 115,774 | 1.158 | 20 | 24 | fits | 108,774 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,426,994 | 14.270 | 20 | 24 | fits | 50,991 | 27 | 0.722 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 114,734 | 1.147 | 20 | 50 | fits | 108,774 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 529,109 | 5.291 | 20 | 50 | fits | 109,053 | 74 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 290,585 | 2.906 | 18 | 18 | fits | 176,306 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,543,109 | 15.431 | 18 | 18 | fits | 42,043 | 21 | 0.797 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 414,312 | 4.143 | 20 | 20 | fits | 145,848 | 89 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 120,019 | 1.200 | 20 | 200 | fits | 108,774 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 541,542 | 5.415 | 20 | 200 | fits | 145,848 | 89 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 120,931 | 1.209 | 20 | 20 | fits | 108,774 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 757,541 | 7.575 | 20 | 20 | fits | 97,931 | 34 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 124,516 | 1.245 | 20 | 24 | fits | 108,774 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,483,629 | 14.836 | 20 | 24 | fits | 99,053 | 51 | 0.746 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 123,476 | 1.235 | 20 | 50 | fits | 108,774 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 545,218 | 5.452 | 20 | 50 | fits | 145,848 | 89 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 299,255 | 2.993 | 18 | 18 | fits | 176,234 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,529,412 | 15.294 | 18 | 18 | fits | 48,318 | 20 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 432,765 | 4.328 | 20 | 20 | fits | 138,745 | 83 | 0.652 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 109,655 | 1.097 | 20 | 200 | fits | 108,774 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 560,722 | 5.607 | 20 | 200 | fits | 138,745 | 83 | 0.652 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 110,567 | 1.106 | 20 | 20 | fits | 108,774 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 776,376 | 7.764 | 20 | 20 | fits | 97,630 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 114,152 | 1.142 | 20 | 24 | fits | 108,774 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,465,079 | 14.651 | 20 | 24 | fits | 91,380 | 45 | 0.741 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 113,112 | 1.131 | 20 | 50 | fits | 108,774 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 564,398 | 5.644 | 20 | 50 | fits | 138,745 | 83 | 0.652 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 288,891 | 2.889 | 18 | 18 | fits | 176,234 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,545,903 | 15.459 | 18 | 18 | fits | 35,220 | 15 | 0.803 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 440,787 | 4.408 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 118,397 | 1.184 | 20 | 200 | fits | 108,774 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 568,572 | 5.686 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 119,309 | 1.193 | 20 | 20 | fits | 108,774 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 784,161 | 7.842 | 20 | 20 | fits | 97,630 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 122,894 | 1.229 | 20 | 24 | fits | 108,774 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,472,460 | 14.725 | 20 | 24 | fits | 62,493 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 121,854 | 1.219 | 20 | 50 | fits | 108,774 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 572,248 | 5.722 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 304,272 | 3.043 | 18 | 18 | fits | 182,873 | 145 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,506,241 | 15.062 | 18 | 18 | fits | 36,316 | 17 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 424,393 | 4.244 | 20 | 20 | fits | 138,505 | 83 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 107,466 | 1.075 | 20 | 200 | fits | 113,164 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 552,178 | 5.522 | 20 | 200 | fits | 138,505 | 83 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 108,378 | 1.084 | 20 | 20 | fits | 113,164 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 767,767 | 7.678 | 20 | 20 | fits | 97,630 | 34 | 0.713 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 111,963 | 1.120 | 20 | 24 | fits | 113,164 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,456,423 | 14.564 | 20 | 24 | fits | 62,493 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 110,923 | 1.109 | 20 | 50 | fits | 113,164 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 555,854 | 5.559 | 20 | 50 | fits | 138,505 | 83 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 287,829 | 2.878 | 18 | 18 | fits | 177,361 | 145 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,490,204 | 14.902 | 18 | 18 | fits | 36,316 | 17 | 0.809 |
| an event behind 15 others | `backlog.event.if0` | 138,944 | 1.389 | 20 | 200 | fits | 108,475 | 125 | 0.536 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 637,173 | 6.372 | 20 | 20 | fits | 102,884 | 52 | 0.691 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 128,184 | 1.282 | 20 | 200 | fits | 128,392 | 143 | 0.543 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 507,953 | 5.080 | 20 | 200 | fits | 122,135 | 57 | 0.683 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 123,925 | 1.239 | 20 | 20 | fits | 128,392 | 143 | 0.543 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 701,339 | 7.013 | 20 | 20 | fits | 102,884 | 52 | 0.691 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 127,510 | 1.275 | 20 | 24 | fits | 128,392 | 143 | 0.543 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,195,013 | 11.950 | 20 | 24 | fits | 49,024 | 31 | 0.690 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 126,470 | 1.265 | 20 | 50 | fits | 128,392 | 143 | 0.543 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 506,458 | 5.065 | 20 | 50 | fits | 122,135 | 57 | 0.683 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 506,393 | 5.064 | 18 | 18 | fits | 122,135 | 57 | 0.683 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,294,641 | 12.946 | 18 | 18 | fits | 33,443 | 18 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 394,642 | 3.946 | 20 | 20 | fits | 145,869 | 89 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 101,253 | 1.013 | 20 | 200 | fits | 105,935 | 140 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 521,890 | 5.219 | 20 | 200 | fits | 145,869 | 89 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 102,165 | 1.022 | 20 | 20 | fits | 105,935 | 140 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 737,272 | 7.373 | 20 | 20 | fits | 97,291 | 34 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 105,750 | 1.058 | 20 | 24 | fits | 105,935 | 140 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,435,354 | 14.354 | 20 | 24 | fits | 62,308 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 104,710 | 1.047 | 20 | 50 | fits | 105,935 | 140 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 525,566 | 5.256 | 20 | 50 | fits | 145,869 | 89 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 279,586 | 2.796 | 18 | 18 | fits | 175,331 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,480,973 | 14.810 | 18 | 18 | fits | 48,154 | 20 | 0.770 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 24,831 | 0.248 | 20 | 20 | fits | 43,251 | 21 | 0.756 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 101,253 | 1.013 | 20 | 200 | fits | 105,935 | 140 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 59,984 | 0.600 | 20 | 200 | fits | 43,251 | 21 | 0.756 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 102,165 | 1.022 | 20 | 20 | fits | 105,935 | 140 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 717,721 | 7.177 | 20 | 20 | fits | 106,929 | 46 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 105,750 | 1.058 | 20 | 24 | fits | 105,935 | 140 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,335,485 | 13.355 | 20 | 24 | fits | 51,058 | 27 | 0.725 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 104,710 | 1.047 | 20 | 50 | fits | 105,935 | 140 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 506,161 | 5.062 | 20 | 50 | fits | 126,464 | 79 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 279,586 | 2.796 | 18 | 18 | fits | 175,331 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,471,021 | 14.710 | 18 | 18 | fits | 35,026 | 15 | 0.800 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,375,646 | 63.756 | 20 | 20 | MISS ceiling | 51,118 | 27 | 0.610 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,046,727 | 360.467 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,046,652 | 360.467 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,046,577 | 360.466 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,046,502 | 360.465 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 103,755 | 1.038 | 20 | 200 | fits | 103,897 | 134 | 0.500 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 534,649 | 5.346 | 20 | 200 | fits | 119,885 | 69 | 0.663 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 99,496 | 0.995 | 20 | 20 | fits | 103,897 | 134 | 0.500 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 724,871 | 7.249 | 20 | 20 | fits | 95,668 | 35 | 0.750 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 103,081 | 1.031 | 20 | 24 | fits | 103,897 | 134 | 0.500 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,514,320 | 65.143 | 20 | 24 | MISS ceiling | 32,440 | 23 | 0.590 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 102,041 | 1.020 | 20 | 50 | fits | 103,897 | 134 | 0.500 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 533,154 | 5.332 | 20 | 50 | fits | 119,885 | 69 | 0.663 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 283,699 | 2.837 | 18 | 18 | fits | 182,113 | 138 | 0.648 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,254,997 | 12.550 | 18 | 18 | fits | 47,368 | 21 | 0.759 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
