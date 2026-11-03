### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 22 paths and 6 of 323 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.368 (7.058) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 5.028 (7.026) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.080 (0.447) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.386 (2.368) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.759 (64.330) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.472 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 7.316 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.511 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 10.358 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 4.951 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 13.880 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.836 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 8.301 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.827 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.081 | fits | 7 adp | 26 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.444 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.872 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.134 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.862 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.118 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 5.049 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-2.service.srp.last.if1` (backlog-adp@verify-2) | 16.479 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 17.180 | 18 | 178,624 (1.786) | yes | - |
| backlog-adp@blank-1 | 0 | 16.624 | 18 | 178,622 (1.786) | yes | - |
| backlog-adp@blank-2 | 0 | 16.619 | 19 | 178,622 (1.786) | yes | - |
| backlog-adp@blank-3 | 0 | 18.625 | 21 | 173,946 (1.739) | yes | - |
| backlog-adp@blank-4 | 0 | 17.423 | 21 | 180,728 (1.807) | yes | - |
| backlog-adp@blank-5 | 0 | 16.996 | 20 | 178,512 (1.785) | yes | - |
| backlog-adp@blank-6 | 0 | 16.867 | 19 | 158,404 (1.584) | yes | - |
| backlog-adp@blank-7 | 0 | 16.569 | 18 | 185,900 (1.859) | yes | - |
| backlog-adp@program-0 | 0 | 16.295 | 17 | 180,291 (1.803) | yes | - |
| backlog-adp@program-1 | 0 | 17.127 | 19 | 178,032 (1.780) | yes | - |
| backlog-adp@program-2 | 0 | 16.689 | 18 | 178,032 (1.780) | yes | - |
| backlog-adp@program-3 | 0 | 16.724 | 19 | 173,510 (1.735) | yes | - |
| backlog-adp@program-4 | 0 | 15.750 | 18 | 178,045 (1.780) | yes | - |
| backlog-adp@program-5 | 0 | 15.807 | 18 | 178,016 (1.780) | yes | - |
| backlog-adp@program-6 | 0 | 15.895 | 18 | 173,084 (1.731) | yes | - |
| backlog-adp@program-7 | 0 | 16.184 | 20 | 185,337 (1.853) | yes | - |
| backlog-adp@verify-0 | 0 | 17.060 | 19 | 185,438 (1.854) | yes | - |
| backlog-adp@verify-1 | 0 | 16.925 | 19 | 173,981 (1.740) | yes | - |
| backlog-adp@verify-2 | 0 | 18.162 | 19 | 181,017 (1.810) | yes | - |
| backlog-adp@verify-3 | 0 | 17.353 | 20 | 178,894 (1.789) | yes | - |
| backlog-adp@verify-4 | 0 | 17.034 | 19 | 178,894 (1.789) | yes | - |
| backlog-adp@verify-5 | 0 | 17.185 | 19 | 178,892 (1.789) | yes | - |
| backlog-adp@verify-6 | 0 | 17.085 | 19 | 186,280 (1.863) | yes | - |
| backlog-adp@verify-7 | 1 | 16.883 | 18 | 174,088 (1.741) | yes | - |
| backlog | 0 | 13.566 | 19 | 146,809 (1.468) | yes | - |
| backlog-adp | 0 | 16.235 | 21 | 188,790 (1.888) | yes | - |
| backlog-adp-refill | 0 | 41.036 | 28 | 169,532 (1.695) | yes | - |
| backlog-owed | 0 | 360.523 | 64 | 183,241 (1.832) | yes | - |

Composed maximum over the 4 backlog windows: 188,790 CPU cycles (1.888 ms), backlog-adp.
Over the windows that released their whole load only: 188,790 (1.888 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 8504 | 0 | 163,368 (1.634) | fits |
| save-starved | 52624 | 0 | 166,488 (1.665) | fits |
| backlog-adp@blank-0 | 482 | 0 | 178,624 (1.786) | fits |
| backlog-adp@blank-1 | 482 | 0 | 178,622 (1.786) | fits |
| backlog-adp@blank-2 | 483 | 0 | 178,622 (1.786) | fits |
| backlog-adp@blank-3 | 485 | 0 | 173,946 (1.739) | fits |
| backlog-adp@blank-4 | 485 | 0 | 180,728 (1.807) | fits |
| backlog-adp@blank-5 | 486 | 0 | 178,512 (1.785) | fits |
| backlog-adp@blank-6 | 486 | 0 | 158,404 (1.584) | fits |
| backlog-adp@blank-7 | 484 | 0 | 185,900 (1.859) | fits |
| backlog-adp@program-0 | 747 | 0 | 180,291 (1.803) | fits |
| backlog-adp@program-1 | 750 | 0 | 178,032 (1.780) | fits |
| backlog-adp@program-2 | 750 | 0 | 178,032 (1.780) | fits |
| backlog-adp@program-3 | 750 | 0 | 173,510 (1.735) | fits |
| backlog-adp@program-4 | 750 | 0 | 178,045 (1.780) | fits |
| backlog-adp@program-5 | 750 | 0 | 178,016 (1.780) | fits |
| backlog-adp@program-6 | 750 | 0 | 173,084 (1.731) | fits |
| backlog-adp@program-7 | 753 | 0 | 185,337 (1.853) | fits |
| backlog-adp@verify-0 | 999 | 0 | 185,438 (1.854) | fits |
| backlog-adp@verify-1 | 999 | 0 | 173,981 (1.740) | fits |
| backlog-adp@verify-2 | 999 | 0 | 181,017 (1.810) | fits |
| backlog-adp@verify-3 | 1001 | 0 | 178,894 (1.789) | fits |
| backlog-adp@verify-4 | 1000 | 0 | 178,894 (1.789) | fits |
| backlog-adp@verify-5 | 1000 | 0 | 178,892 (1.789) | fits |
| backlog-adp@verify-6 | 1000 | 0 | 186,280 (1.863) | fits |
| backlog-adp@verify-7 | 1000 | 0 | 174,088 (1.741) | fits |
| save | 617 | 0 | 130,087 (1.301) | fits |
| backlog | 302 | 0 | 146,809 (1.468) | fits |
| backlog-adp | 323 | 0 | 188,790 (1.888) | fits |
| backlog-adp-refill | 330 | 0 | 169,532 (1.695) | fits |
| backlog-owed | 358 | 0 | 183,241 (1.832) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---|---|
| save-held | 4696.997 | 12,110 | 370 | 18.424 | no | within |
| save-starved | 12087.088 | 12,110 | 370 | 31.476 | yes | within |
| save | 4697.383 | 12,110 | 370 | 12.717 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1527 | 124,581 (1.246) | 96,375 (0.964) |
| save-starved | 686 | 96,299 (0.963) | 95,809 (0.958) |
| backlog-adp@blank-0 | 337 | 95,636 (0.956) | 76,126 (0.761) |
| backlog-adp@blank-1 | 337 | 95,463 (0.955) | 76,126 (0.761) |
| backlog-adp@blank-2 | 337 | 95,636 (0.956) | 76,126 (0.761) |
| backlog-adp@blank-3 | 338 | 95,636 (0.956) | 76,126 (0.761) |
| backlog-adp@blank-4 | 337 | 95,463 (0.955) | 76,126 (0.761) |
| backlog-adp@blank-5 | 337 | 95,030 (0.950) | 75,994 (0.760) |
| backlog-adp@blank-6 | 337 | 95,547 (0.955) | 76,210 (0.762) |
| backlog-adp@blank-7 | 337 | 95,636 (0.956) | 76,126 (0.761) |
| backlog-adp@program-0 | 443 | 119,507 (1.195) | 82,210 (0.822) |
| backlog-adp@program-1 | 444 | 119,507 (1.195) | 82,122 (0.821) |
| backlog-adp@program-2 | 443 | 119,507 (1.195) | 82,187 (0.822) |
| backlog-adp@program-3 | 443 | 119,507 (1.195) | 82,210 (0.822) |
| backlog-adp@program-4 | 444 | 119,507 (1.195) | 81,669 (0.817) |
| backlog-adp@program-5 | 444 | 119,507 (1.195) | 81,669 (0.817) |
| backlog-adp@program-6 | 444 | 119,507 (1.195) | 81,669 (0.817) |
| backlog-adp@program-7 | 444 | 119,507 (1.195) | 81,669 (0.817) |
| backlog-adp@verify-0 | 546 | 119,507 (1.195) | 95,491 (0.955) |
| backlog-adp@verify-1 | 546 | 119,507 (1.195) | 95,491 (0.955) |
| backlog-adp@verify-2 | 547 | 119,507 (1.195) | 95,491 (0.955) |
| backlog-adp@verify-3 | 546 | 119,507 (1.195) | 95,491 (0.955) |
| backlog-adp@verify-4 | 546 | 119,507 (1.195) | 95,491 (0.955) |
| backlog-adp@verify-5 | 546 | 119,507 (1.195) | 95,491 (0.955) |
| backlog-adp@verify-6 | 546 | 119,507 (1.195) | 95,491 (0.955) |
| backlog-adp@verify-7 | 546 | 119,507 (1.195) | 95,491 (0.955) |
| save | 585 | 124,462 (1.245) | 95,321 (0.953) |
| backlog | 266 | 45,495 (0.455) | 3,073 (0.031) |
| backlog-adp | 271 | 45,495 (0.455) | 3,073 (0.031) |
| backlog-adp-refill | 273 | 45,495 (0.455) | 3,073 (0.031) |
| backlog-owed | 305 | 45,495 (0.455) | 3,073 (0.031) |

Longest pass that carries a step: 124,581 CPU cycles (1.246 ms), save-held; longest step: 96,375 (0.964 ms), save-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 443,181 | 4.432 | 20 | 200 | fits | 110,616 | 85 | 0.560 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 716,633 | 7.166 | 20 | 20 | fits | 114,761 | 52 | 0.682 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 982,345 | 9.823 | 20 | 24 | fits | 32,253 | 23 | 0.574 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 484,027 | 4.840 | 20 | 50 | fits | 100,458 | 56 | 0.642 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 1,342,203 | 13.422 | 18 | 18 | fits | 62,282 | 31 | 0.707 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 451,119 | 4.511 | 20 | 200 | fits | 113,584 | 91 | 0.585 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 731,621 | 7.316 | 20 | 20 | fits | 115,556 | 58 | 0.672 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 1,035,789 | 10.358 | 20 | 24 | fits | 34,799 | 29 | 0.619 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 495,128 | 4.951 | 20 | 50 | fits | 103,621 | 62 | 0.663 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,387,978 | 13.880 | 18 | 18 | fits | 65,072 | 37 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 502,769 | 5.028 | 20 | 20 | fits | 116,482 | 85 | 0.626 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 182,700 | 1.827 | 20 | 200 | fits | 109,747 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 608,089 | 6.081 | 20 | 200 | fits | 116,482 | 85 | 0.626 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 183,612 | 1.836 | 20 | 20 | fits | 109,747 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 830,086 | 8.301 | 20 | 20 | fits | 109,387 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 187,197 | 1.872 | 20 | 24 | fits | 109,747 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,486,356 | 14.864 | 20 | 24 | fits | 63,503 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 186,157 | 1.862 | 20 | 50 | fits | 109,747 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 611,765 | 6.118 | 20 | 50 | fits | 116,482 | 85 | 0.626 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 364,326 | 3.643 | 18 | 18 | fits | 178,624 | 140 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,579,124 | 15.791 | 18 | 18 | fits | 47,185 | 18 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 447,909 | 4.479 | 20 | 20 | fits | 152,445 | 101 | 0.678 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 116,557 | 1.166 | 20 | 200 | fits | 109,528 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 577,907 | 5.779 | 20 | 200 | fits | 152,445 | 101 | 0.678 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 117,469 | 1.175 | 20 | 20 | fits | 109,528 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 797,737 | 7.977 | 20 | 20 | fits | 109,059 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 121,054 | 1.211 | 20 | 24 | fits | 109,528 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,443,219 | 14.432 | 20 | 24 | fits | 63,282 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 120,014 | 1.200 | 20 | 50 | fits | 109,528 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 581,583 | 5.816 | 20 | 50 | fits | 152,445 | 101 | 0.678 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 298,181 | 2.982 | 18 | 18 | fits | 178,622 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,523,739 | 15.237 | 18 | 18 | fits | 34,992 | 15 | 0.787 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 406,592 | 4.066 | 20 | 20 | fits | 142,126 | 89 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 108,701 | 1.087 | 20 | 200 | fits | 109,528 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 535,799 | 5.358 | 20 | 200 | fits | 142,126 | 89 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 109,613 | 1.096 | 20 | 20 | fits | 109,528 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 727,029 | 7.270 | 20 | 20 | fits | 80,474 | 37 | 0.637 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 113,198 | 1.132 | 20 | 24 | fits | 109,528 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,383,058 | 13.831 | 20 | 24 | fits | 63,321 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 112,158 | 1.122 | 20 | 50 | fits | 109,528 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 539,475 | 5.395 | 20 | 50 | fits | 142,126 | 89 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 290,325 | 2.903 | 18 | 18 | fits | 178,622 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,523,024 | 15.230 | 18 | 18 | fits | 47,015 | 18 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 416,518 | 4.165 | 20 | 20 | fits | 141,633 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 120,369 | 1.204 | 20 | 200 | fits | 109,528 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 546,554 | 5.466 | 20 | 200 | fits | 141,633 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 121,281 | 1.213 | 20 | 20 | fits | 109,528 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 744,997 | 7.450 | 20 | 20 | fits | 116,256 | 52 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 124,866 | 1.249 | 20 | 24 | fits | 109,528 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,392,663 | 13.927 | 20 | 24 | fits | 63,321 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 123,826 | 1.238 | 20 | 50 | fits | 109,528 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 550,230 | 5.502 | 20 | 50 | fits | 141,633 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 408,532 | 4.085 | 18 | 18 | fits | 173,946 | 104 | 0.665 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,532,629 | 15.326 | 18 | 18 | fits | 47,015 | 18 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 440,288 | 4.403 | 20 | 20 | fits | 110,583 | 74 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 117,887 | 1.179 | 20 | 200 | fits | 114,902 | 151 | 0.535 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 539,709 | 5.397 | 20 | 200 | fits | 110,583 | 74 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 118,799 | 1.188 | 20 | 20 | fits | 114,902 | 151 | 0.535 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 766,997 | 7.670 | 20 | 20 | fits | 109,390 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 122,384 | 1.224 | 20 | 24 | fits | 114,902 | 151 | 0.535 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,383,469 | 13.835 | 20 | 24 | fits | 63,114 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 121,344 | 1.213 | 20 | 50 | fits | 114,902 | 151 | 0.535 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 543,385 | 5.434 | 20 | 50 | fits | 110,583 | 74 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 301,617 | 3.016 | 18 | 18 | fits | 180,728 | 145 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,553,989 | 15.540 | 18 | 18 | fits | 35,152 | 15 | 0.792 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 409,980 | 4.100 | 20 | 20 | fits | 147,676 | 89 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 112,121 | 1.121 | 20 | 200 | fits | 109,456 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 538,806 | 5.388 | 20 | 200 | fits | 147,676 | 89 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 113,033 | 1.130 | 20 | 20 | fits | 109,456 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 753,269 | 7.533 | 20 | 20 | fits | 103,847 | 53 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 116,618 | 1.166 | 20 | 24 | fits | 109,456 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,402,729 | 14.027 | 20 | 24 | fits | 71,529 | 37 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 115,578 | 1.156 | 20 | 50 | fits | 109,456 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 542,482 | 5.425 | 20 | 50 | fits | 147,676 | 89 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 293,635 | 2.936 | 18 | 18 | fits | 178,512 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,530,205 | 15.302 | 18 | 18 | fits | 34,955 | 15 | 0.787 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 421,607 | 4.216 | 20 | 20 | fits | 141,001 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 104,265 | 1.043 | 20 | 200 | fits | 109,456 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 551,294 | 5.513 | 20 | 200 | fits | 141,001 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 105,177 | 1.052 | 20 | 20 | fits | 109,456 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 750,074 | 7.501 | 20 | 20 | fits | 110,833 | 52 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 108,762 | 1.088 | 20 | 24 | fits | 109,456 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,362,716 | 13.627 | 20 | 24 | fits | 63,175 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 107,722 | 1.077 | 20 | 50 | fits | 109,456 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 554,970 | 5.550 | 20 | 50 | fits | 141,001 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 255,500 | 2.555 | 18 | 18 | fits | 148,233 | 136 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,547,917 | 15.479 | 18 | 18 | fits | 34,810 | 15 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 443,443 | 4.434 | 20 | 20 | fits | 116,482 | 85 | 0.626 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 115,933 | 1.159 | 20 | 200 | fits | 109,456 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 548,763 | 5.488 | 20 | 200 | fits | 116,482 | 85 | 0.626 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 116,845 | 1.168 | 20 | 20 | fits | 109,456 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 770,760 | 7.708 | 20 | 20 | fits | 109,387 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 120,430 | 1.204 | 20 | 24 | fits | 109,456 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,425,223 | 14.252 | 20 | 24 | fits | 63,477 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 119,390 | 1.194 | 20 | 50 | fits | 109,456 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 552,439 | 5.524 | 20 | 50 | fits | 116,482 | 85 | 0.626 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 304,835 | 3.048 | 18 | 18 | fits | 185,900 | 145 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,518,072 | 15.181 | 18 | 18 | fits | 47,185 | 18 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 435,213 | 4.352 | 20 | 20 | fits | 140,243 | 83 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 113,382 | 1.134 | 20 | 200 | fits | 115,365 | 151 | 0.537 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 564,294 | 5.643 | 20 | 200 | fits | 140,243 | 83 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 114,294 | 1.143 | 20 | 20 | fits | 115,365 | 151 | 0.537 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 783,830 | 7.838 | 20 | 20 | fits | 108,929 | 46 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 117,879 | 1.179 | 20 | 24 | fits | 115,365 | 151 | 0.537 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,438,505 | 14.385 | 20 | 24 | fits | 63,114 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 116,839 | 1.168 | 20 | 50 | fits | 115,365 | 151 | 0.537 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 567,970 | 5.680 | 20 | 50 | fits | 140,243 | 83 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 296,675 | 2.967 | 18 | 18 | fits | 180,291 | 145 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,484,283 | 14.843 | 18 | 18 | fits | 48,313 | 20 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 439,979 | 4.400 | 20 | 20 | fits | 140,184 | 83 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 120,502 | 1.205 | 20 | 200 | fits | 109,939 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 569,001 | 5.690 | 20 | 200 | fits | 140,184 | 83 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 121,414 | 1.214 | 20 | 20 | fits | 109,939 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 776,069 | 7.761 | 20 | 20 | fits | 119,094 | 58 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 124,999 | 1.250 | 20 | 24 | fits | 109,939 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,411,197 | 14.112 | 20 | 24 | fits | 63,114 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 123,959 | 1.240 | 20 | 50 | fits | 109,939 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 572,677 | 5.727 | 20 | 50 | fits | 140,184 | 83 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 301,536 | 3.015 | 18 | 18 | fits | 178,032 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,517,242 | 15.172 | 18 | 18 | fits | 47,510 | 18 | 0.758 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 409,811 | 4.098 | 20 | 20 | fits | 150,111 | 95 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 104,790 | 1.048 | 20 | 200 | fits | 109,939 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 539,283 | 5.393 | 20 | 200 | fits | 150,111 | 95 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 105,702 | 1.057 | 20 | 20 | fits | 109,939 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 758,973 | 7.590 | 20 | 20 | fits | 109,007 | 46 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 109,287 | 1.093 | 20 | 24 | fits | 109,939 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,376,225 | 13.762 | 20 | 24 | fits | 63,050 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 108,247 | 1.082 | 20 | 50 | fits | 109,939 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 542,959 | 5.430 | 20 | 50 | fits | 150,111 | 95 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 285,824 | 2.858 | 18 | 18 | fits | 178,032 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,523,681 | 15.237 | 18 | 18 | fits | 47,015 | 18 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 411,766 | 4.118 | 20 | 20 | fits | 141,698 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 108,602 | 1.086 | 20 | 200 | fits | 109,939 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 541,867 | 5.419 | 20 | 200 | fits | 141,698 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 109,514 | 1.095 | 20 | 20 | fits | 109,939 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 761,567 | 7.616 | 20 | 20 | fits | 109,010 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 113,099 | 1.131 | 20 | 24 | fits | 109,939 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,387,023 | 13.870 | 20 | 24 | fits | 63,321 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 112,059 | 1.121 | 20 | 50 | fits | 109,939 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 545,543 | 5.455 | 20 | 50 | fits | 141,698 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 403,780 | 4.038 | 18 | 18 | fits | 173,510 | 104 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,526,989 | 15.270 | 18 | 18 | fits | 47,015 | 18 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 430,661 | 4.307 | 20 | 20 | fits | 140,184 | 83 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 111,038 | 1.110 | 20 | 200 | fits | 110,267 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 559,683 | 5.597 | 20 | 200 | fits | 140,184 | 83 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 111,950 | 1.119 | 20 | 20 | fits | 110,267 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 790,439 | 7.904 | 20 | 20 | fits | 113,413 | 52 | 0.699 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 115,535 | 1.155 | 20 | 24 | fits | 110,267 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,432,064 | 14.321 | 20 | 24 | fits | 62,820 | 31 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 114,495 | 1.145 | 20 | 50 | fits | 110,267 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 563,359 | 5.634 | 20 | 50 | fits | 140,184 | 83 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 292,085 | 2.921 | 18 | 18 | fits | 178,045 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,483,976 | 14.840 | 18 | 18 | fits | 54,447 | 31 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 444,215 | 4.442 | 20 | 20 | fits | 144,455 | 89 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 114,810 | 1.148 | 20 | 200 | fits | 110,267 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 574,331 | 5.743 | 20 | 200 | fits | 144,455 | 89 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 115,722 | 1.157 | 20 | 20 | fits | 110,267 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 772,725 | 7.727 | 20 | 20 | fits | 116,347 | 52 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 119,307 | 1.193 | 20 | 24 | fits | 110,267 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,419,573 | 14.196 | 20 | 24 | fits | 63,112 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 118,267 | 1.183 | 20 | 50 | fits | 110,267 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 578,007 | 5.780 | 20 | 50 | fits | 144,455 | 89 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 295,828 | 2.958 | 18 | 18 | fits | 178,016 | 140 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,512,460 | 15.125 | 18 | 18 | fits | 47,185 | 18 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 420,983 | 4.210 | 20 | 20 | fits | 149,178 | 89 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 118,622 | 1.186 | 20 | 200 | fits | 110,267 | 140 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 551,522 | 5.515 | 20 | 200 | fits | 149,178 | 89 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 119,534 | 1.195 | 20 | 20 | fits | 110,267 | 140 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 771,233 | 7.712 | 20 | 20 | fits | 109,033 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 123,119 | 1.231 | 20 | 24 | fits | 110,267 | 140 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,428,181 | 14.282 | 20 | 24 | fits | 71,711 | 37 | 0.736 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 122,079 | 1.221 | 20 | 50 | fits | 110,267 | 140 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 555,198 | 5.552 | 20 | 50 | fits | 149,178 | 89 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 405,955 | 4.060 | 18 | 18 | fits | 173,084 | 104 | 0.665 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,521,332 | 15.213 | 18 | 18 | fits | 47,185 | 18 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 438,220 | 4.382 | 20 | 20 | fits | 140,184 | 83 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 111,406 | 1.114 | 20 | 200 | fits | 109,997 | 140 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 567,242 | 5.672 | 20 | 200 | fits | 140,184 | 83 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 112,318 | 1.123 | 20 | 20 | fits | 109,997 | 140 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 763,951 | 7.640 | 20 | 20 | fits | 86,161 | 48 | 0.650 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 115,903 | 1.159 | 20 | 24 | fits | 109,997 | 140 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,381,049 | 13.810 | 20 | 24 | fits | 63,057 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 114,863 | 1.149 | 20 | 50 | fits | 109,997 | 140 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 570,918 | 5.709 | 20 | 50 | fits | 140,184 | 83 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 299,745 | 2.997 | 18 | 18 | fits | 185,337 | 145 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,527,402 | 15.274 | 18 | 18 | fits | 53,458 | 29 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 444,775 | 4.448 | 20 | 20 | fits | 140,187 | 83 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 114,303 | 1.143 | 20 | 200 | fits | 109,787 | 140 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 573,923 | 5.739 | 20 | 200 | fits | 140,187 | 83 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 115,215 | 1.152 | 20 | 20 | fits | 109,787 | 140 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 793,441 | 7.934 | 20 | 20 | fits | 108,959 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 118,800 | 1.188 | 20 | 24 | fits | 109,787 | 140 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,408,725 | 14.087 | 20 | 24 | fits | 51,769 | 27 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 117,760 | 1.178 | 20 | 50 | fits | 109,787 | 140 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 577,599 | 5.776 | 20 | 50 | fits | 140,187 | 83 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 302,743 | 3.027 | 18 | 18 | fits | 185,438 | 151 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,566,482 | 15.665 | 18 | 18 | fits | 35,053 | 15 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 402,778 | 4.028 | 20 | 20 | fits | 141,771 | 83 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 106,606 | 1.066 | 20 | 200 | fits | 109,549 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 532,952 | 5.330 | 20 | 200 | fits | 141,771 | 83 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 107,518 | 1.075 | 20 | 20 | fits | 109,549 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 752,652 | 7.527 | 20 | 20 | fits | 109,010 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 111,103 | 1.111 | 20 | 24 | fits | 109,549 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,381,486 | 13.815 | 20 | 24 | fits | 35,046 | 22 | 0.665 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 110,063 | 1.101 | 20 | 50 | fits | 109,549 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 536,628 | 5.366 | 20 | 50 | fits | 141,771 | 83 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 394,792 | 3.948 | 18 | 18 | fits | 173,981 | 104 | 0.666 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,552,803 | 15.528 | 18 | 18 | fits | 47,113 | 18 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 446,205 | 4.462 | 20 | 20 | fits | 140,243 | 83 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 123,648 | 1.236 | 20 | 200 | fits | 114,923 | 151 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 575,286 | 5.753 | 20 | 200 | fits | 140,243 | 83 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 124,560 | 1.246 | 20 | 20 | fits | 114,923 | 151 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 773,636 | 7.736 | 20 | 20 | fits | 116,388 | 52 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 128,145 | 1.281 | 20 | 24 | fits | 114,923 | 151 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,421,556 | 14.216 | 20 | 24 | fits | 63,321 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 127,105 | 1.271 | 20 | 50 | fits | 114,923 | 151 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 578,962 | 5.790 | 20 | 50 | fits | 140,243 | 83 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 307,667 | 3.077 | 18 | 18 | fits | 181,017 | 145 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,647,909 | 16.479 | 18 | 18 | fits | 54,257 | 29 | 0.777 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 439,661 | 4.397 | 20 | 20 | fits | 110,524 | 74 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 119,322 | 1.193 | 20 | 200 | fits | 109,683 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 539,023 | 5.390 | 20 | 200 | fits | 110,524 | 74 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 120,234 | 1.202 | 20 | 20 | fits | 109,683 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 743,571 | 7.436 | 20 | 20 | fits | 86,615 | 48 | 0.656 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 123,819 | 1.238 | 20 | 24 | fits | 109,683 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,383,560 | 13.836 | 20 | 24 | fits | 63,114 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 122,779 | 1.228 | 20 | 50 | fits | 109,683 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 542,699 | 5.427 | 20 | 50 | fits | 110,524 | 74 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 301,218 | 3.012 | 18 | 18 | fits | 178,894 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,595,817 | 15.958 | 18 | 18 | fits | 35,462 | 15 | 0.798 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 427,668 | 4.277 | 20 | 20 | fits | 148,930 | 89 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 111,466 | 1.115 | 20 | 200 | fits | 109,683 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 557,419 | 5.574 | 20 | 200 | fits | 148,930 | 89 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 112,378 | 1.124 | 20 | 20 | fits | 109,683 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 756,573 | 7.566 | 20 | 20 | fits | 111,052 | 52 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 115,963 | 1.160 | 20 | 24 | fits | 109,683 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,396,504 | 13.965 | 20 | 24 | fits | 69,269 | 42 | 0.723 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 114,923 | 1.149 | 20 | 50 | fits | 109,683 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 561,095 | 5.611 | 20 | 50 | fits | 148,930 | 89 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 293,362 | 2.934 | 18 | 18 | fits | 178,894 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,563,889 | 15.639 | 18 | 18 | fits | 35,078 | 15 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 450,465 | 4.505 | 20 | 20 | fits | 116,221 | 85 | 0.624 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 123,042 | 1.230 | 20 | 200 | fits | 109,683 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 555,665 | 5.557 | 20 | 200 | fits | 116,221 | 85 | 0.624 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 123,954 | 1.240 | 20 | 20 | fits | 109,683 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 777,836 | 7.778 | 20 | 20 | fits | 109,392 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 127,539 | 1.275 | 20 | 24 | fits | 109,683 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,420,684 | 14.207 | 20 | 24 | fits | 63,545 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 126,499 | 1.265 | 20 | 50 | fits | 109,683 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 559,341 | 5.593 | 20 | 50 | fits | 116,221 | 85 | 0.624 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 304,936 | 3.049 | 18 | 18 | fits | 178,892 | 140 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,579,031 | 15.790 | 18 | 18 | fits | 35,964 | 15 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 420,736 | 4.207 | 20 | 20 | fits | 142,126 | 89 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 115,278 | 1.153 | 20 | 200 | fits | 109,683 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 549,943 | 5.499 | 20 | 200 | fits | 142,126 | 89 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 116,190 | 1.162 | 20 | 20 | fits | 109,683 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 769,694 | 7.697 | 20 | 20 | fits | 108,995 | 46 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 119,775 | 1.198 | 20 | 24 | fits | 109,683 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,441,198 | 14.412 | 20 | 24 | fits | 93,455 | 45 | 0.752 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 118,735 | 1.187 | 20 | 50 | fits | 109,683 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 553,619 | 5.536 | 20 | 50 | fits | 142,126 | 89 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 304,560 | 3.046 | 18 | 18 | fits | 186,280 | 145 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,568,975 | 15.690 | 18 | 18 | fits | 34,955 | 15 | 0.787 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 406,026 | 4.060 | 20 | 20 | fits | 141,698 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 108,754 | 1.088 | 20 | 200 | fits | 114,444 | 140 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 536,127 | 5.361 | 20 | 200 | fits | 141,698 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 109,666 | 1.097 | 20 | 20 | fits | 114,444 | 140 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 755,827 | 7.558 | 20 | 20 | fits | 109,010 | 46 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 113,251 | 1.133 | 20 | 24 | fits | 114,444 | 140 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,407,660 | 14.077 | 20 | 24 | fits | 62,820 | 31 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 112,211 | 1.122 | 20 | 50 | fits | 114,444 | 140 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 539,803 | 5.398 | 20 | 50 | fits | 141,698 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 398,040 | 3.980 | 18 | 18 | fits | 174,088 | 104 | 0.666 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,499,985 | 15.000 | 18 | 18 | fits | 46,891 | 18 | 0.743 |
| an event behind 15 others | `backlog.event.if0` | 138,624 | 1.386 | 20 | 200 | fits | 109,052 | 125 | 0.544 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 636,795 | 6.368 | 20 | 20 | fits | 103,134 | 52 | 0.684 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 127,521 | 1.275 | 20 | 200 | fits | 127,729 | 143 | 0.535 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 506,046 | 5.060 | 20 | 200 | fits | 123,273 | 57 | 0.683 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 123,262 | 1.233 | 20 | 20 | fits | 127,729 | 143 | 0.535 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 700,536 | 7.005 | 20 | 20 | fits | 103,134 | 52 | 0.684 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 126,847 | 1.268 | 20 | 24 | fits | 127,729 | 143 | 0.535 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,196,682 | 11.967 | 20 | 24 | fits | 49,339 | 31 | 0.692 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 125,807 | 1.258 | 20 | 50 | fits | 127,729 | 143 | 0.535 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 504,551 | 5.046 | 20 | 50 | fits | 123,273 | 57 | 0.683 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 504,486 | 5.045 | 18 | 18 | fits | 123,273 | 57 | 0.683 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,295,672 | 12.957 | 18 | 18 | fits | 33,246 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 330,578 | 3.306 | 20 | 20 | fits | 188,790 | 89 | 0.704 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 101,878 | 1.019 | 20 | 200 | fits | 106,560 | 140 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 501,269 | 5.013 | 20 | 200 | fits | 188,790 | 89 | 0.704 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 102,790 | 1.028 | 20 | 20 | fits | 106,560 | 140 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 722,964 | 7.230 | 20 | 20 | fits | 109,243 | 46 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 106,375 | 1.064 | 20 | 24 | fits | 106,560 | 140 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,337,411 | 13.374 | 20 | 24 | fits | 70,463 | 37 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 105,335 | 1.053 | 20 | 50 | fits | 106,560 | 140 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 504,945 | 5.049 | 20 | 50 | fits | 188,790 | 89 | 0.704 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 504,880 | 5.049 | 18 | 18 | fits | 188,790 | 89 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,558,341 | 15.583 | 18 | 18 | fits | 34,948 | 15 | 0.785 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,029 | 0.080 | 20 | 20 | fits | 44,658 | 21 | 0.779 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 101,878 | 1.019 | 20 | 200 | fits | 106,560 | 140 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 43,884 | 0.439 | 20 | 200 | fits | 44,658 | 21 | 0.779 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 102,790 | 1.028 | 20 | 20 | fits | 106,560 | 140 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 703,568 | 7.036 | 20 | 20 | fits | 109,125 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 106,375 | 1.064 | 20 | 24 | fits | 106,560 | 140 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,349,000 | 13.490 | 20 | 24 | fits | 71,937 | 37 | 0.736 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 105,335 | 1.053 | 20 | 50 | fits | 106,560 | 140 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 485,687 | 4.857 | 20 | 50 | fits | 169,532 | 79 | 0.706 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 485,622 | 4.856 | 18 | 18 | fits | 169,532 | 79 | 0.706 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,523,221 | 15.232 | 18 | 18 | fits | 34,870 | 15 | 0.783 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,375,902 | 63.759 | 20 | 20 | MISS ceiling | 50,604 | 27 | 0.602 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,047,190 | 360.472 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,047,115 | 360.471 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,047,040 | 360.470 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,046,965 | 360.470 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 112,585 | 1.126 | 20 | 200 | fits | 103,738 | 134 | 0.501 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 544,429 | 5.444 | 20 | 200 | fits | 119,493 | 69 | 0.661 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 108,326 | 1.083 | 20 | 20 | fits | 103,738 | 134 | 0.501 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 734,492 | 7.345 | 20 | 20 | fits | 95,562 | 35 | 0.743 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 111,911 | 1.119 | 20 | 24 | fits | 103,738 | 134 | 0.501 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,513,377 | 65.134 | 20 | 24 | MISS ceiling | 32,221 | 23 | 0.570 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 110,871 | 1.109 | 20 | 50 | fits | 103,738 | 134 | 0.501 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 542,934 | 5.429 | 20 | 50 | fits | 119,493 | 69 | 0.661 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 293,657 | 2.937 | 18 | 18 | fits | 183,241 | 138 | 0.651 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,258,197 | 12.582 | 18 | 18 | fits | 46,785 | 21 | 0.733 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
