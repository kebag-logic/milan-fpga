### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 313 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.361 (7.056) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.866 (6.870) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.185 (0.741) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.381 (2.361) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.748 (64.124) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.553 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.706 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-3.service.acmp.last.if0` (backlog-adp@blank-3) | 8.197 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.697 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-3.service.adp.last.if0` (backlog-adp@blank-3) | 5.944 | fits | 7 adp | 26 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.377 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.742 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.119 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.731 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 5.960 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.059 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-0.service.srp.last.if1` (backlog-adp@blank-0) | 15.789 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 17.175 | 19 | 176,671 (1.767) | yes | - |
| backlog-adp@blank-1 | 0 | 16.597 | 18 | 176,743 (1.767) | yes | - |
| backlog-adp@blank-2 | 0 | 16.578 | 19 | 176,743 (1.767) | yes | - |
| backlog-adp@blank-3 | 0 | 17.784 | 19 | 186,432 (1.864) | yes | - |
| backlog-adp@blank-4 | 0 | 17.455 | 21 | 178,385 (1.784) | yes | - |
| backlog-adp@blank-5 | 0 | 16.958 | 20 | 176,711 (1.767) | yes | - |
| backlog-adp@blank-6 | 0 | 16.828 | 19 | 156,045 (1.560) | yes | - |
| backlog-adp@blank-7 | 0 | 16.448 | 18 | 183,180 (1.832) | yes | - |
| backlog-adp@program-0 | 0 | 16.419 | 18 | 177,705 (1.777) | yes | - |
| backlog-adp@program-1 | 0 | 17.039 | 19 | 176,049 (1.760) | yes | - |
| backlog-adp@program-2 | 0 | 16.673 | 19 | 176,121 (1.761) | yes | - |
| backlog-adp@program-3 | 0 | 16.428 | 18 | 170,838 (1.708) | yes | - |
| backlog-adp@program-4 | 0 | 15.836 | 19 | 176,186 (1.762) | yes | - |
| backlog-adp@program-5 | 0 | 15.817 | 19 | 175,973 (1.760) | yes | - |
| backlog-adp@program-6 | 0 | 15.935 | 19 | 170,943 (1.709) | yes | - |
| backlog-adp@program-7 | 0 | 16.268 | 20 | 182,293 (1.823) | yes | - |
| backlog-adp@verify-0 | 0 | 17.018 | 19 | 176,477 (1.765) | yes | - |
| backlog-adp@verify-1 | 0 | 16.776 | 18 | 171,547 (1.715) | yes | - |
| backlog-adp@verify-2 | 0 | 17.999 | 19 | 178,269 (1.783) | yes | - |
| backlog-adp@verify-3 | 0 | 17.184 | 20 | 176,781 (1.768) | yes | - |
| backlog-adp@verify-4 | 0 | 16.919 | 18 | 176,781 (1.768) | yes | - |
| backlog-adp@verify-5 | 0 | 16.933 | 19 | 176,709 (1.767) | yes | - |
| backlog-adp@verify-6 | 0 | 16.980 | 19 | 163,781 (1.638) | yes | - |
| backlog-adp@verify-7 | 0 | 16.911 | 19 | 171,493 (1.715) | yes | - |
| backlog | 0 | 13.590 | 19 | 150,562 (1.506) | yes | - |
| backlog-adp | 0 | 15.977 | 20 | 186,185 (1.862) | yes | - |
| backlog-adp-refill | 0 | 41.133 | 30 | 166,796 (1.668) | yes | - |
| backlog-owed | 0 | 360.603 | 65 | 181,005 (1.810) | yes | - |

Composed maximum over the 4 backlog windows: 186,185 CPU cycles (1.862 ms), backlog-adp.
Over the windows that released their whole load only: 186,185 (1.862 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 488 | 0 | 176,671 (1.767) | fits |
| backlog-adp@blank-1 | 487 | 0 | 176,743 (1.767) | fits |
| backlog-adp@blank-2 | 488 | 0 | 176,743 (1.767) | fits |
| backlog-adp@blank-3 | 489 | 0 | 186,432 (1.864) | fits |
| backlog-adp@blank-4 | 490 | 0 | 178,385 (1.784) | fits |
| backlog-adp@blank-5 | 490 | 0 | 176,711 (1.767) | fits |
| backlog-adp@blank-6 | 490 | 0 | 156,045 (1.560) | fits |
| backlog-adp@blank-7 | 488 | 0 | 183,180 (1.832) | fits |
| backlog-adp@program-0 | 749 | 0 | 177,705 (1.777) | fits |
| backlog-adp@program-1 | 751 | 0 | 176,049 (1.760) | fits |
| backlog-adp@program-2 | 751 | 0 | 176,121 (1.761) | fits |
| backlog-adp@program-3 | 750 | 0 | 170,838 (1.708) | fits |
| backlog-adp@program-4 | 752 | 0 | 176,186 (1.762) | fits |
| backlog-adp@program-5 | 752 | 0 | 175,973 (1.760) | fits |
| backlog-adp@program-6 | 752 | 0 | 170,943 (1.709) | fits |
| backlog-adp@program-7 | 755 | 0 | 182,293 (1.823) | fits |
| backlog-adp@verify-0 | 1023 | 0 | 176,477 (1.765) | fits |
| backlog-adp@verify-1 | 1022 | 0 | 171,547 (1.715) | fits |
| backlog-adp@verify-2 | 1023 | 0 | 178,269 (1.783) | fits |
| backlog-adp@verify-3 | 1025 | 0 | 176,781 (1.768) | fits |
| backlog-adp@verify-4 | 1024 | 0 | 176,781 (1.768) | fits |
| backlog-adp@verify-5 | 1024 | 0 | 176,709 (1.767) | fits |
| backlog-adp@verify-6 | 1024 | 0 | 163,781 (1.638) | fits |
| backlog-adp@verify-7 | 1024 | 0 | 171,493 (1.715) | fits |
| save | 617 | 0 | 128,456 (1.285) | fits |
| backlog | 302 | 0 | 150,562 (1.506) | fits |
| backlog-adp | 323 | 0 | 186,185 (1.862) | fits |
| backlog-adp-refill | 333 | 0 | 166,796 (1.668) | fits |
| backlog-owed | 359 | 0 | 181,005 (1.810) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 486,594 | 4.866 | 20 | 20 | fits | 116,677 | 85 | 0.628 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 169,679 | 1.697 | 20 | 200 | fits | 109,764 | 140 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 592,322 | 5.923 | 20 | 200 | fits | 116,677 | 85 | 0.628 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 170,591 | 1.706 | 20 | 20 | fits | 109,764 | 140 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 812,341 | 8.123 | 20 | 20 | fits | 108,437 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 174,176 | 1.742 | 20 | 24 | fits | 109,764 | 140 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,450,755 | 14.508 | 20 | 24 | fits | 67,273 | 37 | 0.743 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 173,136 | 1.731 | 20 | 50 | fits | 109,764 | 140 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 595,998 | 5.960 | 20 | 50 | fits | 116,677 | 85 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 349,352 | 3.494 | 18 | 18 | fits | 176,671 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,578,937 | 15.789 | 18 | 18 | fits | 35,616 | 15 | 0.806 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 450,808 | 4.508 | 20 | 20 | fits | 152,346 | 101 | 0.683 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 122,166 | 1.222 | 20 | 200 | fits | 109,590 | 140 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 580,550 | 5.806 | 20 | 200 | fits | 152,346 | 101 | 0.683 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 123,078 | 1.231 | 20 | 20 | fits | 109,590 | 140 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 798,623 | 7.986 | 20 | 20 | fits | 108,161 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 126,663 | 1.267 | 20 | 24 | fits | 109,590 | 140 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,439,872 | 14.399 | 20 | 24 | fits | 62,858 | 31 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 125,623 | 1.256 | 20 | 50 | fits | 109,590 | 140 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 584,226 | 5.842 | 20 | 50 | fits | 152,346 | 101 | 0.683 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 301,911 | 3.019 | 18 | 18 | fits | 176,743 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,521,094 | 15.211 | 18 | 18 | fits | 35,731 | 15 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 442,026 | 4.420 | 20 | 20 | fits | 139,939 | 83 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 112,966 | 1.130 | 20 | 200 | fits | 109,590 | 140 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 571,027 | 5.710 | 20 | 200 | fits | 139,939 | 83 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 113,878 | 1.139 | 20 | 20 | fits | 109,590 | 140 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 760,670 | 7.607 | 20 | 20 | fits | 79,788 | 37 | 0.637 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 117,463 | 1.175 | 20 | 24 | fits | 109,590 | 140 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,380,525 | 13.805 | 20 | 24 | fits | 62,662 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 116,423 | 1.164 | 20 | 50 | fits | 109,590 | 140 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 574,703 | 5.747 | 20 | 50 | fits | 139,939 | 83 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 292,711 | 2.927 | 18 | 18 | fits | 176,743 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,519,003 | 15.190 | 18 | 18 | fits | 46,578 | 18 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 475,050 | 4.750 | 20 | 20 | fits | 130,347 | 60 | 0.679 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 155,679 | 1.557 | 20 | 200 | fits | 109,553 | 142 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 594,448 | 5.944 | 20 | 200 | fits | 130,347 | 60 | 0.679 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 156,591 | 1.566 | 20 | 20 | fits | 109,553 | 142 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 819,701 | 8.197 | 20 | 20 | fits | 108,197 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 50,623 | 0.506 | 20 | 24 | fits | 51,950 | 65 | 0.573 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,390,094 | 13.901 | 20 | 24 | fits | 62,962 | 31 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 49,583 | 0.496 | 20 | 50 | fits | 51,950 | 65 | 0.573 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 467,777 | 4.678 | 20 | 50 | fits | 122,599 | 76 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 345,113 | 3.451 | 18 | 18 | fits | 186,432 | 157 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,518,340 | 15.183 | 18 | 18 | fits | 35,698 | 15 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 438,189 | 4.382 | 20 | 20 | fits | 110,474 | 74 | 0.612 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 119,537 | 1.195 | 20 | 200 | fits | 115,261 | 151 | 0.541 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 537,714 | 5.377 | 20 | 200 | fits | 110,474 | 74 | 0.612 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 120,449 | 1.204 | 20 | 20 | fits | 115,261 | 151 | 0.541 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 762,701 | 7.627 | 20 | 20 | fits | 108,219 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 124,034 | 1.240 | 20 | 24 | fits | 115,261 | 151 | 0.541 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,374,240 | 13.742 | 20 | 24 | fits | 62,662 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 122,994 | 1.230 | 20 | 50 | fits | 115,261 | 151 | 0.541 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 541,390 | 5.414 | 20 | 50 | fits | 110,474 | 74 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 300,924 | 3.009 | 18 | 18 | fits | 178,385 | 145 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,519,881 | 15.199 | 18 | 18 | fits | 53,783 | 24 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 408,582 | 4.086 | 20 | 20 | fits | 146,315 | 89 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 113,794 | 1.138 | 20 | 200 | fits | 109,526 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 536,982 | 5.370 | 20 | 200 | fits | 146,315 | 89 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 114,706 | 1.147 | 20 | 20 | fits | 109,526 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 750,666 | 7.507 | 20 | 20 | fits | 103,646 | 53 | 0.708 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 118,291 | 1.183 | 20 | 24 | fits | 109,526 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,398,847 | 13.988 | 20 | 24 | fits | 71,349 | 37 | 0.744 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 117,251 | 1.173 | 20 | 50 | fits | 109,526 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 540,658 | 5.407 | 20 | 50 | fits | 146,315 | 89 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 293,507 | 2.935 | 18 | 18 | fits | 176,711 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,534,207 | 15.342 | 18 | 18 | fits | 42,452 | 26 | 0.812 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 418,072 | 4.181 | 20 | 20 | fits | 140,821 | 83 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 104,594 | 1.046 | 20 | 200 | fits | 109,526 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 547,738 | 5.477 | 20 | 200 | fits | 140,821 | 83 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 105,506 | 1.055 | 20 | 20 | fits | 109,526 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 745,613 | 7.456 | 20 | 20 | fits | 109,875 | 52 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 109,091 | 1.091 | 20 | 24 | fits | 109,526 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,357,388 | 13.574 | 20 | 24 | fits | 62,900 | 31 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 108,051 | 1.081 | 20 | 50 | fits | 109,526 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 551,414 | 5.514 | 20 | 50 | fits | 140,821 | 83 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 254,483 | 2.545 | 18 | 18 | fits | 146,887 | 136 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,544,012 | 15.440 | 18 | 18 | fits | 35,793 | 15 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 438,118 | 4.381 | 20 | 20 | fits | 116,677 | 85 | 0.628 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 114,694 | 1.147 | 20 | 200 | fits | 109,526 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 543,846 | 5.438 | 20 | 200 | fits | 116,677 | 85 | 0.628 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 115,606 | 1.156 | 20 | 20 | fits | 109,526 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 763,865 | 7.639 | 20 | 20 | fits | 108,437 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 119,191 | 1.192 | 20 | 24 | fits | 109,526 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,414,024 | 14.140 | 20 | 24 | fits | 62,982 | 31 | 0.723 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 118,151 | 1.182 | 20 | 50 | fits | 109,526 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 547,522 | 5.475 | 20 | 50 | fits | 116,677 | 85 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 300,876 | 3.009 | 18 | 18 | fits | 183,180 | 145 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,505,947 | 15.059 | 18 | 18 | fits | 46,759 | 18 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 439,471 | 4.395 | 20 | 20 | fits | 140,005 | 83 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 121,434 | 1.214 | 20 | 200 | fits | 115,410 | 151 | 0.541 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 568,462 | 5.685 | 20 | 200 | fits | 140,005 | 83 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 122,346 | 1.223 | 20 | 20 | fits | 115,410 | 151 | 0.541 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 786,460 | 7.865 | 20 | 20 | fits | 108,152 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 125,931 | 1.259 | 20 | 24 | fits | 115,410 | 151 | 0.541 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,404,570 | 14.046 | 20 | 24 | fits | 62,609 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 124,891 | 1.249 | 20 | 50 | fits | 115,410 | 151 | 0.541 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 572,138 | 5.721 | 20 | 50 | fits | 140,005 | 83 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 302,141 | 3.021 | 18 | 18 | fits | 177,705 | 145 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,496,530 | 14.965 | 18 | 18 | fits | 46,724 | 18 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 423,047 | 4.230 | 20 | 20 | fits | 139,922 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 106,689 | 1.067 | 20 | 200 | fits | 109,760 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 551,955 | 5.520 | 20 | 200 | fits | 139,922 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 107,601 | 1.076 | 20 | 20 | fits | 109,760 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 756,945 | 7.569 | 20 | 20 | fits | 117,096 | 58 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 111,186 | 1.112 | 20 | 24 | fits | 109,760 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,386,319 | 13.863 | 20 | 24 | fits | 62,595 | 31 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 110,146 | 1.101 | 20 | 50 | fits | 109,760 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 555,631 | 5.556 | 20 | 50 | fits | 139,922 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 285,740 | 2.857 | 18 | 18 | fits | 176,049 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,489,589 | 14.896 | 18 | 18 | fits | 51,489 | 24 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 410,002 | 4.100 | 20 | 20 | fits | 149,062 | 95 | 0.661 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 107,589 | 1.076 | 20 | 200 | fits | 109,760 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 539,115 | 5.391 | 20 | 200 | fits | 149,062 | 95 | 0.661 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 108,501 | 1.085 | 20 | 20 | fits | 109,760 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 757,595 | 7.576 | 20 | 20 | fits | 108,412 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 112,086 | 1.121 | 20 | 24 | fits | 109,760 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,387,755 | 13.878 | 20 | 24 | fits | 62,689 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 111,046 | 1.110 | 20 | 50 | fits | 109,760 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 542,791 | 5.428 | 20 | 50 | fits | 149,062 | 95 | 0.661 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 286,712 | 2.867 | 18 | 18 | fits | 176,121 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,522,024 | 15.220 | 18 | 18 | fits | 35,367 | 15 | 0.801 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 407,469 | 4.075 | 20 | 20 | fits | 141,138 | 83 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 108,489 | 1.085 | 20 | 200 | fits | 109,760 | 140 | 0.524 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 537,430 | 5.374 | 20 | 200 | fits | 141,138 | 83 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 109,401 | 1.094 | 20 | 20 | fits | 109,760 | 140 | 0.524 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 755,598 | 7.556 | 20 | 20 | fits | 108,161 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 112,986 | 1.130 | 20 | 24 | fits | 109,760 | 140 | 0.524 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,405,515 | 14.055 | 20 | 24 | fits | 62,662 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 111,946 | 1.119 | 20 | 50 | fits | 109,760 | 140 | 0.524 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 541,106 | 5.411 | 20 | 50 | fits | 141,138 | 83 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 399,903 | 3.999 | 18 | 18 | fits | 170,838 | 104 | 0.660 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,497,415 | 14.974 | 18 | 18 | fits | 46,724 | 18 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 425,141 | 4.251 | 20 | 20 | fits | 139,922 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 108,627 | 1.086 | 20 | 200 | fits | 110,106 | 140 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 554,049 | 5.540 | 20 | 200 | fits | 139,922 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 109,539 | 1.095 | 20 | 20 | fits | 110,106 | 140 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 784,351 | 7.844 | 20 | 20 | fits | 120,456 | 64 | 0.711 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 113,124 | 1.131 | 20 | 24 | fits | 110,106 | 140 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,393,997 | 13.940 | 20 | 24 | fits | 62,595 | 31 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 112,084 | 1.121 | 20 | 50 | fits | 110,106 | 140 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 557,725 | 5.577 | 20 | 50 | fits | 139,922 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 287,815 | 2.878 | 18 | 18 | fits | 176,186 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,492,638 | 14.926 | 18 | 18 | fits | 53,535 | 29 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 438,029 | 4.380 | 20 | 20 | fits | 152,411 | 101 | 0.683 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 110,073 | 1.101 | 20 | 200 | fits | 109,813 | 140 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 567,771 | 5.678 | 20 | 200 | fits | 152,411 | 101 | 0.683 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 110,985 | 1.110 | 20 | 20 | fits | 109,813 | 140 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 764,371 | 7.644 | 20 | 20 | fits | 114,922 | 52 | 0.691 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 114,570 | 1.146 | 20 | 24 | fits | 109,813 | 140 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,375,121 | 13.751 | 20 | 24 | fits | 62,664 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 113,530 | 1.135 | 20 | 50 | fits | 109,813 | 140 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 571,447 | 5.714 | 20 | 50 | fits | 152,411 | 101 | 0.683 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 289,048 | 2.890 | 18 | 18 | fits | 175,973 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,513,539 | 15.135 | 18 | 18 | fits | 46,496 | 18 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 410,059 | 4.101 | 20 | 20 | fits | 148,025 | 89 | 0.673 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 110,973 | 1.110 | 20 | 200 | fits | 109,813 | 140 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 540,040 | 5.400 | 20 | 200 | fits | 148,025 | 89 | 0.673 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 111,885 | 1.119 | 20 | 20 | fits | 109,813 | 140 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 758,235 | 7.582 | 20 | 20 | fits | 108,161 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 115,470 | 1.155 | 20 | 24 | fits | 109,813 | 140 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,390,610 | 13.906 | 20 | 24 | fits | 62,962 | 31 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 114,430 | 1.144 | 20 | 50 | fits | 109,813 | 140 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 543,716 | 5.437 | 20 | 50 | fits | 148,025 | 89 | 0.673 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 395,626 | 3.956 | 18 | 18 | fits | 170,943 | 104 | 0.660 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,525,602 | 15.256 | 18 | 18 | fits | 35,534 | 15 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 442,113 | 4.421 | 20 | 20 | fits | 139,922 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 119,471 | 1.195 | 20 | 200 | fits | 109,543 | 140 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 571,021 | 5.710 | 20 | 200 | fits | 139,922 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 120,383 | 1.204 | 20 | 20 | fits | 109,543 | 140 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 766,957 | 7.670 | 20 | 20 | fits | 86,090 | 48 | 0.656 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 123,968 | 1.240 | 20 | 24 | fits | 109,543 | 140 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,401,093 | 14.011 | 20 | 24 | fits | 62,962 | 31 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 122,928 | 1.229 | 20 | 50 | fits | 109,543 | 140 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 574,697 | 5.747 | 20 | 50 | fits | 139,922 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 304,766 | 3.048 | 18 | 18 | fits | 182,293 | 145 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,535,913 | 15.359 | 18 | 18 | fits | 42,272 | 26 | 0.810 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 441,606 | 4.416 | 20 | 20 | fits | 139,986 | 83 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 112,577 | 1.126 | 20 | 200 | fits | 109,882 | 140 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 570,607 | 5.706 | 20 | 200 | fits | 139,986 | 83 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 113,489 | 1.135 | 20 | 20 | fits | 109,882 | 140 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 788,623 | 7.886 | 20 | 20 | fits | 108,161 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 117,074 | 1.171 | 20 | 24 | fits | 109,882 | 140 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,402,671 | 14.027 | 20 | 24 | fits | 35,229 | 22 | 0.676 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 116,034 | 1.160 | 20 | 50 | fits | 109,882 | 140 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 574,283 | 5.743 | 20 | 50 | fits | 139,986 | 83 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 292,056 | 2.921 | 18 | 18 | fits | 176,477 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,561,999 | 15.620 | 18 | 18 | fits | 35,878 | 15 | 0.810 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 415,615 | 4.156 | 20 | 20 | fits | 141,073 | 83 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 122,721 | 1.227 | 20 | 200 | fits | 109,541 | 140 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 545,576 | 5.456 | 20 | 200 | fits | 141,073 | 83 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 123,633 | 1.236 | 20 | 20 | fits | 109,541 | 140 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 763,791 | 7.638 | 20 | 20 | fits | 108,161 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 127,218 | 1.272 | 20 | 24 | fits | 109,541 | 140 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,445,236 | 14.452 | 20 | 24 | fits | 93,345 | 45 | 0.753 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 126,178 | 1.262 | 20 | 50 | fits | 109,541 | 140 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 549,252 | 5.493 | 20 | 50 | fits | 141,073 | 83 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 408,114 | 4.081 | 18 | 18 | fits | 171,547 | 104 | 0.660 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,537,587 | 15.376 | 18 | 18 | fits | 46,724 | 18 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 437,754 | 4.378 | 20 | 20 | fits | 139,904 | 83 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 119,172 | 1.192 | 20 | 200 | fits | 115,100 | 151 | 0.537 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 566,662 | 5.667 | 20 | 200 | fits | 139,904 | 83 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 120,084 | 1.201 | 20 | 20 | fits | 115,100 | 151 | 0.537 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 763,538 | 7.635 | 20 | 20 | fits | 115,063 | 52 | 0.692 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 123,669 | 1.237 | 20 | 24 | fits | 115,100 | 151 | 0.537 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,405,770 | 14.058 | 20 | 24 | fits | 62,662 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 122,629 | 1.226 | 20 | 50 | fits | 115,100 | 151 | 0.537 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 570,338 | 5.703 | 20 | 50 | fits | 139,904 | 83 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 300,443 | 3.004 | 18 | 18 | fits | 178,269 | 145 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,527,741 | 15.277 | 18 | 18 | fits | 76,795 | 32 | 0.788 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 430,845 | 4.308 | 20 | 20 | fits | 110,438 | 74 | 0.612 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 113,754 | 1.138 | 20 | 200 | fits | 109,640 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 530,287 | 5.303 | 20 | 200 | fits | 110,438 | 74 | 0.612 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 114,666 | 1.147 | 20 | 20 | fits | 109,640 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 732,972 | 7.330 | 20 | 20 | fits | 85,917 | 48 | 0.655 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 118,251 | 1.183 | 20 | 24 | fits | 109,640 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,368,245 | 13.682 | 20 | 24 | fits | 62,662 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 117,211 | 1.172 | 20 | 50 | fits | 109,640 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 533,963 | 5.340 | 20 | 50 | fits | 110,438 | 74 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 293,537 | 2.935 | 18 | 18 | fits | 176,781 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,578,754 | 15.788 | 18 | 18 | fits | 44,977 | 27 | 0.799 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 417,382 | 4.174 | 20 | 20 | fits | 147,724 | 89 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 104,554 | 1.046 | 20 | 200 | fits | 109,640 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 546,536 | 5.465 | 20 | 200 | fits | 147,724 | 89 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 105,466 | 1.055 | 20 | 20 | fits | 109,640 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 744,646 | 7.446 | 20 | 20 | fits | 110,004 | 52 | 0.689 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 109,051 | 1.091 | 20 | 24 | fits | 109,640 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,376,469 | 13.765 | 20 | 24 | fits | 62,869 | 31 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 108,011 | 1.080 | 20 | 50 | fits | 109,640 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 550,212 | 5.502 | 20 | 50 | fits | 147,724 | 89 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 284,337 | 2.843 | 18 | 18 | fits | 176,781 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,552,086 | 15.521 | 18 | 18 | fits | 35,793 | 15 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 438,374 | 4.384 | 20 | 20 | fits | 116,839 | 85 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 114,654 | 1.147 | 20 | 200 | fits | 109,640 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 544,228 | 5.442 | 20 | 200 | fits | 116,839 | 85 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 115,566 | 1.156 | 20 | 20 | fits | 109,640 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 764,247 | 7.642 | 20 | 20 | fits | 108,437 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 119,151 | 1.192 | 20 | 24 | fits | 109,640 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,383,610 | 13.836 | 20 | 24 | fits | 35,315 | 22 | 0.678 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 118,111 | 1.181 | 20 | 50 | fits | 109,640 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 547,904 | 5.479 | 20 | 50 | fits | 116,839 | 85 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 294,365 | 2.944 | 18 | 18 | fits | 176,709 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,553,377 | 15.534 | 18 | 18 | fits | 46,496 | 18 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 377,548 | 3.775 | 20 | 20 | fits | 163,781 | 89 | 0.706 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 105,454 | 1.055 | 20 | 200 | fits | 109,640 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 527,448 | 5.274 | 20 | 200 | fits | 163,781 | 89 | 0.706 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 106,366 | 1.064 | 20 | 20 | fits | 109,640 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 746,873 | 7.469 | 20 | 20 | fits | 108,545 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 109,951 | 1.100 | 20 | 24 | fits | 109,640 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,429,342 | 14.293 | 20 | 24 | fits | 93,460 | 45 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 108,911 | 1.089 | 20 | 50 | fits | 109,640 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 531,124 | 5.311 | 20 | 50 | fits | 163,781 | 89 | 0.706 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 367,278 | 3.673 | 18 | 18 | fits | 153,676 | 111 | 0.665 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,558,200 | 15.582 | 18 | 18 | fits | 35,796 | 15 | 0.809 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 415,107 | 4.151 | 20 | 20 | fits | 141,073 | 83 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 115,554 | 1.156 | 20 | 200 | fits | 109,640 | 140 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 545,068 | 5.451 | 20 | 200 | fits | 141,073 | 83 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 116,466 | 1.165 | 20 | 20 | fits | 109,640 | 140 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 763,283 | 7.633 | 20 | 20 | fits | 108,161 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 120,051 | 1.201 | 20 | 24 | fits | 109,640 | 140 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,410,990 | 14.110 | 20 | 24 | fits | 62,662 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 119,011 | 1.190 | 20 | 50 | fits | 109,640 | 140 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 548,744 | 5.487 | 20 | 50 | fits | 141,073 | 83 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 407,606 | 4.076 | 18 | 18 | fits | 171,493 | 104 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,502,890 | 15.029 | 18 | 18 | fits | 46,724 | 18 | 0.759 |
| an event behind 15 others | `backlog.event.if0` | 138,131 | 1.381 | 20 | 200 | fits | 108,211 | 125 | 0.538 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 636,127 | 6.361 | 20 | 20 | fits | 101,984 | 52 | 0.685 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 127,661 | 1.277 | 20 | 200 | fits | 127,869 | 143 | 0.539 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 507,472 | 5.075 | 20 | 200 | fits | 121,647 | 57 | 0.679 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 123,402 | 1.234 | 20 | 20 | fits | 127,869 | 143 | 0.539 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 700,265 | 7.003 | 20 | 20 | fits | 101,984 | 52 | 0.685 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 126,987 | 1.270 | 20 | 24 | fits | 127,869 | 143 | 0.539 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,198,176 | 11.982 | 20 | 24 | fits | 49,547 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 125,947 | 1.259 | 20 | 50 | fits | 127,869 | 143 | 0.539 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 505,977 | 5.060 | 20 | 50 | fits | 121,647 | 57 | 0.679 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 505,912 | 5.059 | 18 | 18 | fits | 121,647 | 57 | 0.679 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,298,793 | 12.988 | 18 | 18 | fits | 33,843 | 18 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 329,494 | 3.295 | 20 | 20 | fits | 186,185 | 89 | 0.701 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 101,953 | 1.020 | 20 | 200 | fits | 106,635 | 140 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 498,368 | 4.984 | 20 | 200 | fits | 186,185 | 89 | 0.701 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 102,865 | 1.029 | 20 | 20 | fits | 106,635 | 140 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 717,732 | 7.177 | 20 | 20 | fits | 108,438 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 106,450 | 1.065 | 20 | 24 | fits | 106,635 | 140 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,358,005 | 13.580 | 20 | 24 | fits | 71,597 | 37 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 105,410 | 1.054 | 20 | 50 | fits | 106,635 | 140 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 502,044 | 5.020 | 20 | 50 | fits | 186,185 | 89 | 0.701 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 501,979 | 5.020 | 18 | 18 | fits | 186,185 | 89 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,533,124 | 15.331 | 18 | 18 | fits | 35,693 | 15 | 0.807 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 18,537 | 0.185 | 20 | 20 | fits | 44,806 | 21 | 0.768 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 101,953 | 1.020 | 20 | 200 | fits | 106,635 | 140 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 54,625 | 0.546 | 20 | 200 | fits | 44,806 | 21 | 0.768 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 102,865 | 1.029 | 20 | 20 | fits | 106,635 | 140 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 698,183 | 6.982 | 20 | 20 | fits | 108,429 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 106,450 | 1.065 | 20 | 24 | fits | 106,635 | 140 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,284,129 | 12.841 | 20 | 24 | fits | 35,187 | 22 | 0.672 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 105,410 | 1.054 | 20 | 50 | fits | 106,635 | 140 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 482,655 | 4.827 | 20 | 50 | fits | 166,796 | 79 | 0.704 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 482,590 | 4.826 | 18 | 18 | fits | 166,796 | 79 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,523,889 | 15.239 | 18 | 18 | fits | 46,573 | 18 | 0.756 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,374,789 | 63.748 | 20 | 20 | MISS ceiling | 50,503 | 27 | 0.598 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,055,253 | 360.553 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,055,178 | 360.552 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,055,103 | 360.551 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,055,028 | 360.550 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 108,107 | 1.081 | 20 | 200 | fits | 104,193 | 134 | 0.505 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 537,673 | 5.377 | 20 | 200 | fits | 120,145 | 69 | 0.666 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 103,848 | 1.038 | 20 | 20 | fits | 104,193 | 134 | 0.505 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 727,912 | 7.279 | 20 | 20 | fits | 95,609 | 35 | 0.751 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 107,433 | 1.074 | 20 | 24 | fits | 104,193 | 134 | 0.505 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,511,920 | 65.119 | 20 | 24 | MISS ceiling | 32,023 | 23 | 0.573 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 106,393 | 1.064 | 20 | 50 | fits | 104,193 | 134 | 0.505 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 536,178 | 5.362 | 20 | 50 | fits | 120,145 | 69 | 0.666 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 286,943 | 2.869 | 18 | 18 | fits | 181,005 | 138 | 0.645 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,271,743 | 12.717 | 18 | 18 | fits | 35,395 | 18 | 0.791 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
