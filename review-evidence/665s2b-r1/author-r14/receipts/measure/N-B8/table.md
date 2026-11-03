### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 22 paths and 6 of 323 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.702 (7.427) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 5.354 (7.718) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.188 (0.746) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.478 (2.544) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.767 (64.173) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 361.080 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 8.498 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.876 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 11.352 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 5.606 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 14.810 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.909 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 9.235 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.900 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.786 | fits | 7 adp | 26 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.833 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.945 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.133 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.935 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.822 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.433 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-0.service.srp.last.if1` (backlog-adp@blank-0) | 16.910 | fits | 31 srp | 28 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.264 | 18 | 188,469 (1.885) | yes | - |
| backlog-adp@blank-1 | 0 | 17.295 | 17 | 188,538 (1.885) | yes | - |
| backlog-adp@blank-2 | 0 | 18.772 | 19 | 188,469 (1.885) | yes | - |
| backlog-adp@blank-3 | 0 | 17.667 | 18 | 188,538 (1.885) | yes | - |
| backlog-adp@blank-4 | 0 | 17.440 | 17 | 188,469 (1.885) | yes | - |
| backlog-adp@blank-5 | 0 | 17.469 | 17 | 188,538 (1.885) | yes | - |
| backlog-adp@blank-6 | 0 | 17.441 | 18 | 187,553 (1.876) | yes | - |
| backlog-adp@blank-7 | 0 | 17.514 | 18 | 194,842 (1.948) | yes | - |
| backlog-adp@program-0 | 0 | 17.581 | 18 | 187,512 (1.875) | yes | - |
| backlog-adp@program-1 | 0 | 18.090 | 19 | 187,512 (1.875) | yes | - |
| backlog-adp@program-2 | 0 | 17.772 | 19 | 187,581 (1.876) | yes | - |
| backlog-adp@program-3 | 0 | 17.448 | 17 | 193,998 (1.940) | yes | - |
| backlog-adp@program-4 | 0 | 16.888 | 18 | 187,595 (1.876) | yes | - |
| backlog-adp@program-5 | 0 | 18.083 | 19 | 187,512 (1.875) | yes | - |
| backlog-adp@program-6 | 0 | 16.992 | 19 | 187,581 (1.876) | yes | - |
| backlog-adp@program-7 | 0 | 16.669 | 17 | 193,998 (1.940) | yes | - |
| backlog-adp@verify-0 | 0 | 17.950 | 18 | 188,480 (1.885) | yes | - |
| backlog-adp@verify-1 | 0 | 19.243 | 20 | 188,480 (1.885) | yes | - |
| backlog-adp@verify-2 | 0 | 18.041 | 19 | 188,411 (1.884) | yes | - |
| backlog-adp@verify-3 | 0 | 17.877 | 18 | 188,480 (1.885) | yes | - |
| backlog-adp@verify-4 | 0 | 18.062 | 19 | 188,411 (1.884) | yes | - |
| backlog-adp@verify-5 | 0 | 18.058 | 18 | 170,980 (1.710) | yes | - |
| backlog-adp@verify-6 | 0 | 17.815 | 17 | 194,784 (1.948) | yes | - |
| backlog-adp@verify-7 | 0 | 18.012 | 18 | 194,771 (1.948) | yes | - |
| backlog | 0 | 14.551 | 20 | 159,838 (1.598) | yes | - |
| backlog-adp | 0 | 16.537 | 17 | 187,379 (1.874) | yes | - |
| backlog-adp-refill | 0 | 41.273 | 22 | 187,379 (1.874) | yes | - |
| backlog-owed | 0 | 361.131 | 65 | 191,979 (1.920) | yes | - |

Composed maximum over the 4 backlog windows: 191,979 CPU cycles (1.920 ms), backlog-owed.
Over the windows that released their whole load only: 191,979 (1.920 ms), backlog-owed.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 8489 | 0 | 169,428 (1.694) | fits |
| save-starved | 52090 | 0 | 171,628 (1.716) | fits |
| backlog-adp@blank-0 | 381 | 0 | 188,469 (1.885) | fits |
| backlog-adp@blank-1 | 380 | 0 | 188,538 (1.885) | fits |
| backlog-adp@blank-2 | 382 | 0 | 188,469 (1.885) | fits |
| backlog-adp@blank-3 | 381 | 0 | 188,538 (1.885) | fits |
| backlog-adp@blank-4 | 380 | 0 | 188,469 (1.885) | fits |
| backlog-adp@blank-5 | 380 | 0 | 188,538 (1.885) | fits |
| backlog-adp@blank-6 | 381 | 0 | 187,553 (1.876) | fits |
| backlog-adp@blank-7 | 381 | 0 | 194,842 (1.948) | fits |
| backlog-adp@program-0 | 490 | 0 | 187,512 (1.875) | fits |
| backlog-adp@program-1 | 491 | 0 | 187,512 (1.875) | fits |
| backlog-adp@program-2 | 491 | 0 | 187,581 (1.876) | fits |
| backlog-adp@program-3 | 489 | 0 | 193,998 (1.940) | fits |
| backlog-adp@program-4 | 491 | 0 | 187,595 (1.876) | fits |
| backlog-adp@program-5 | 492 | 0 | 187,512 (1.875) | fits |
| backlog-adp@program-6 | 492 | 0 | 187,581 (1.876) | fits |
| backlog-adp@program-7 | 490 | 0 | 193,998 (1.940) | fits |
| backlog-adp@verify-0 | 596 | 0 | 188,480 (1.885) | fits |
| backlog-adp@verify-1 | 598 | 0 | 188,480 (1.885) | fits |
| backlog-adp@verify-2 | 597 | 0 | 188,411 (1.884) | fits |
| backlog-adp@verify-3 | 596 | 0 | 188,480 (1.885) | fits |
| backlog-adp@verify-4 | 597 | 0 | 188,411 (1.884) | fits |
| backlog-adp@verify-5 | 596 | 0 | 170,980 (1.710) | fits |
| backlog-adp@verify-6 | 595 | 0 | 194,784 (1.948) | fits |
| backlog-adp@verify-7 | 597 | 0 | 194,771 (1.948) | fits |
| save | 617 | 0 | 132,371 (1.324) | fits |
| backlog | 303 | 0 | 159,838 (1.598) | fits |
| backlog-adp | 309 | 0 | 187,379 (1.874) | fits |
| backlog-adp-refill | 314 | 0 | 187,379 (1.874) | fits |
| backlog-owed | 359 | 0 | 191,979 (1.920) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---|---|
| save-held | 4696.732 | 12,110 | 370 | 19.545 | no | within |
| save-starved | 12087.030 | 12,110 | 370 | 31.254 | yes | within |
| save | 4697.427 | 12,110 | 370 | 12.561 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1526 | 126,560 (1.266) | 96,208 (0.962) |
| save-starved | 686 | 96,382 (0.964) | 96,029 (0.960) |
| backlog-adp@blank-0 | 337 | 94,670 (0.947) | 75,962 (0.760) |
| backlog-adp@blank-1 | 337 | 95,922 (0.959) | 75,962 (0.760) |
| backlog-adp@blank-2 | 338 | 94,670 (0.947) | 75,962 (0.760) |
| backlog-adp@blank-3 | 337 | 94,686 (0.947) | 76,022 (0.760) |
| backlog-adp@blank-4 | 337 | 95,922 (0.959) | 75,962 (0.760) |
| backlog-adp@blank-5 | 337 | 95,922 (0.959) | 75,962 (0.760) |
| backlog-adp@blank-6 | 337 | 94,982 (0.950) | 75,962 (0.760) |
| backlog-adp@blank-7 | 337 | 94,926 (0.949) | 75,962 (0.760) |
| backlog-adp@program-0 | 443 | 120,226 (1.202) | 82,182 (0.822) |
| backlog-adp@program-1 | 444 | 120,226 (1.202) | 82,182 (0.822) |
| backlog-adp@program-2 | 443 | 120,226 (1.202) | 82,182 (0.822) |
| backlog-adp@program-3 | 443 | 120,226 (1.202) | 82,182 (0.822) |
| backlog-adp@program-4 | 444 | 120,226 (1.202) | 81,796 (0.818) |
| backlog-adp@program-5 | 445 | 120,226 (1.202) | 81,796 (0.818) |
| backlog-adp@program-6 | 444 | 120,226 (1.202) | 81,796 (0.818) |
| backlog-adp@program-7 | 444 | 120,226 (1.202) | 81,796 (0.818) |
| backlog-adp@verify-0 | 546 | 120,226 (1.202) | 95,482 (0.955) |
| backlog-adp@verify-1 | 547 | 120,226 (1.202) | 95,482 (0.955) |
| backlog-adp@verify-2 | 546 | 120,226 (1.202) | 95,482 (0.955) |
| backlog-adp@verify-3 | 546 | 120,226 (1.202) | 95,482 (0.955) |
| backlog-adp@verify-4 | 546 | 120,226 (1.202) | 95,482 (0.955) |
| backlog-adp@verify-5 | 546 | 120,226 (1.202) | 95,482 (0.955) |
| backlog-adp@verify-6 | 546 | 120,226 (1.202) | 95,482 (0.955) |
| backlog-adp@verify-7 | 546 | 120,226 (1.202) | 95,482 (0.955) |
| save | 585 | 126,142 (1.261) | 95,530 (0.955) |
| backlog | 266 | 47,159 (0.472) | 2,744 (0.027) |
| backlog-adp | 271 | 47,159 (0.472) | 2,743 (0.027) |
| backlog-adp-refill | 273 | 47,159 (0.472) | 2,743 (0.027) |
| backlog-owed | 306 | 47,456 (0.475) | 2,780 (0.028) |

Longest pass that carries a step: 126,560 CPU cycles (1.266 ms), save-held; longest step: 96,208 (0.962 ms), save-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 480,191 | 4.802 | 20 | 200 | fits | 125,007 | 85 | 0.575 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 817,202 | 8.172 | 20 | 20 | fits | 119,137 | 46 | 0.677 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 1,099,884 | 10.999 | 20 | 24 | fits | 39,934 | 29 | 0.636 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 533,170 | 5.332 | 20 | 50 | fits | 112,591 | 56 | 0.646 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 1,419,746 | 14.197 | 18 | 18 | fits | 66,331 | 31 | 0.698 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 487,573 | 4.876 | 20 | 200 | fits | 127,515 | 91 | 0.594 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 849,812 | 8.498 | 20 | 20 | fits | 121,852 | 52 | 0.686 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 1,135,226 | 11.352 | 20 | 24 | fits | 34,702 | 29 | 0.626 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 560,581 | 5.606 | 20 | 50 | fits | 132,620 | 73 | 0.674 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,480,981 | 14.810 | 18 | 18 | fits | 69,089 | 37 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 535,412 | 5.354 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 189,993 | 1.900 | 20 | 200 | fits | 119,919 | 140 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 678,557 | 6.786 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 190,905 | 1.909 | 20 | 20 | fits | 119,919 | 140 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 923,500 | 9.235 | 20 | 20 | fits | 111,066 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 194,490 | 1.945 | 20 | 24 | fits | 119,919 | 140 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,656,372 | 16.564 | 20 | 24 | fits | 66,594 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 193,450 | 1.935 | 20 | 50 | fits | 119,919 | 140 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 682,233 | 6.822 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 381,464 | 3.815 | 18 | 18 | fits | 188,469 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,690,973 | 16.910 | 18 | 18 | fits | 37,136 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 465,174 | 4.652 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 119,686 | 1.197 | 20 | 200 | fits | 119,238 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 608,319 | 6.083 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 120,598 | 1.206 | 20 | 20 | fits | 119,238 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 853,262 | 8.533 | 20 | 20 | fits | 111,066 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 124,183 | 1.242 | 20 | 24 | fits | 119,238 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,595,279 | 15.953 | 20 | 24 | fits | 66,299 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 123,143 | 1.231 | 20 | 50 | fits | 119,238 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 611,995 | 6.120 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 311,226 | 3.112 | 18 | 18 | fits | 188,538 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,592,744 | 15.927 | 18 | 18 | fits | 66,299 | 31 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 467,785 | 4.678 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 122,366 | 1.224 | 20 | 200 | fits | 119,238 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 610,930 | 6.109 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 123,278 | 1.233 | 20 | 20 | fits | 119,238 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 849,145 | 8.491 | 20 | 20 | fits | 118,175 | 40 | 0.719 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 126,863 | 1.269 | 20 | 24 | fits | 119,238 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,587,775 | 15.878 | 20 | 24 | fits | 66,689 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 125,823 | 1.258 | 20 | 50 | fits | 119,238 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 614,606 | 6.146 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 313,837 | 3.138 | 18 | 18 | fits | 188,469 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,622,429 | 16.224 | 18 | 18 | fits | 37,189 | 17 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 470,534 | 4.705 | 20 | 20 | fits | 140,508 | 79 | 0.664 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 125,046 | 1.250 | 20 | 200 | fits | 119,238 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 599,717 | 5.997 | 20 | 200 | fits | 140,508 | 79 | 0.664 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 125,958 | 1.260 | 20 | 20 | fits | 119,238 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 851,641 | 8.516 | 20 | 20 | fits | 111,044 | 34 | 0.711 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 129,543 | 1.295 | 20 | 24 | fits | 119,238 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,589,972 | 15.900 | 20 | 24 | fits | 66,594 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 128,503 | 1.285 | 20 | 50 | fits | 119,238 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 603,393 | 6.034 | 20 | 50 | fits | 140,508 | 79 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 316,586 | 3.166 | 18 | 18 | fits | 188,538 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,631,288 | 16.313 | 18 | 18 | fits | 43,851 | 23 | 0.790 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 480,118 | 4.801 | 20 | 20 | fits | 161,397 | 89 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 127,726 | 1.277 | 20 | 200 | fits | 119,238 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 623,217 | 6.232 | 20 | 200 | fits | 161,397 | 89 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 128,638 | 1.286 | 20 | 20 | fits | 119,238 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 868,058 | 8.681 | 20 | 20 | fits | 111,066 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 132,223 | 1.322 | 20 | 24 | fits | 119,238 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,609,818 | 16.098 | 20 | 24 | fits | 66,475 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 131,183 | 1.312 | 20 | 50 | fits | 119,238 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 626,893 | 6.269 | 20 | 50 | fits | 161,397 | 89 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 319,197 | 3.192 | 18 | 18 | fits | 188,469 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,607,283 | 16.073 | 18 | 18 | fits | 66,475 | 31 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 482,752 | 4.828 | 20 | 20 | fits | 154,568 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 130,406 | 1.304 | 20 | 200 | fits | 119,238 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 625,995 | 6.260 | 20 | 200 | fits | 154,568 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 131,318 | 1.313 | 20 | 20 | fits | 119,238 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 870,938 | 8.709 | 20 | 20 | fits | 111,066 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 134,903 | 1.349 | 20 | 24 | fits | 119,238 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,612,717 | 16.127 | 20 | 24 | fits | 66,299 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 133,863 | 1.339 | 20 | 50 | fits | 119,238 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 629,671 | 6.297 | 20 | 50 | fits | 154,568 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 321,946 | 3.219 | 18 | 18 | fits | 188,538 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,610,182 | 16.102 | 18 | 18 | fits | 66,299 | 31 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 429,218 | 4.292 | 20 | 20 | fits | 155,979 | 83 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 114,846 | 1.148 | 20 | 200 | fits | 119,238 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 573,494 | 5.735 | 20 | 200 | fits | 155,979 | 83 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 115,758 | 1.158 | 20 | 20 | fits | 119,238 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 818,362 | 8.184 | 20 | 20 | fits | 110,991 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 119,343 | 1.193 | 20 | 24 | fits | 119,238 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,560,366 | 15.604 | 20 | 24 | fits | 66,380 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 118,303 | 1.183 | 20 | 50 | fits | 119,238 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 577,170 | 5.772 | 20 | 50 | fits | 155,979 | 83 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 421,126 | 4.211 | 18 | 18 | fits | 187,553 | 104 | 0.657 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,608,391 | 16.084 | 18 | 18 | fits | 50,560 | 20 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 469,318 | 4.693 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 117,526 | 1.175 | 20 | 200 | fits | 119,238 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 612,463 | 6.125 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 118,438 | 1.184 | 20 | 20 | fits | 119,238 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 857,406 | 8.574 | 20 | 20 | fits | 111,066 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 122,023 | 1.220 | 20 | 24 | fits | 119,238 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,567,527 | 15.675 | 20 | 24 | fits | 66,284 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 120,983 | 1.210 | 20 | 50 | fits | 119,238 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 616,139 | 6.161 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 315,370 | 3.154 | 18 | 18 | fits | 194,842 | 145 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,615,671 | 16.157 | 18 | 18 | fits | 50,679 | 20 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 469,661 | 4.697 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 125,149 | 1.251 | 20 | 200 | fits | 119,835 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 612,806 | 6.128 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 126,061 | 1.261 | 20 | 20 | fits | 119,835 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 857,814 | 8.578 | 20 | 20 | fits | 111,131 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 129,646 | 1.296 | 20 | 24 | fits | 119,835 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,568,045 | 15.680 | 20 | 24 | fits | 66,397 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 128,606 | 1.286 | 20 | 50 | fits | 119,835 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 616,482 | 6.165 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 315,663 | 3.157 | 18 | 18 | fits | 187,512 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,616,184 | 16.162 | 18 | 18 | fits | 50,674 | 20 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 475,021 | 4.750 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 130,509 | 1.305 | 20 | 200 | fits | 119,835 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 618,166 | 6.182 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 131,421 | 1.314 | 20 | 20 | fits | 119,835 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 835,162 | 8.352 | 20 | 20 | fits | 117,657 | 40 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 135,006 | 1.350 | 20 | 24 | fits | 119,835 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,570,649 | 15.706 | 20 | 24 | fits | 66,377 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 133,966 | 1.340 | 20 | 50 | fits | 119,835 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 621,842 | 6.218 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 321,023 | 3.210 | 18 | 18 | fits | 187,512 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,618,621 | 16.186 | 18 | 18 | fits | 50,507 | 20 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 434,176 | 4.342 | 20 | 20 | fits | 160,503 | 89 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 117,629 | 1.176 | 20 | 200 | fits | 119,835 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 576,422 | 5.764 | 20 | 200 | fits | 160,503 | 89 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 118,541 | 1.185 | 20 | 20 | fits | 119,835 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 821,602 | 8.216 | 20 | 20 | fits | 111,219 | 34 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 122,126 | 1.221 | 20 | 24 | fits | 119,835 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,551,685 | 15.517 | 20 | 24 | fits | 66,784 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 121,086 | 1.211 | 20 | 50 | fits | 119,835 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 580,098 | 5.801 | 20 | 50 | fits | 160,503 | 89 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 308,212 | 3.082 | 18 | 18 | fits | 187,581 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,635,599 | 16.356 | 18 | 18 | fits | 35,611 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 473,987 | 4.740 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 122,989 | 1.230 | 20 | 200 | fits | 119,835 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 617,132 | 6.171 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 123,901 | 1.239 | 20 | 20 | fits | 119,835 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 862,140 | 8.621 | 20 | 20 | fits | 111,131 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 127,486 | 1.275 | 20 | 24 | fits | 119,835 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,604,343 | 16.043 | 20 | 24 | fits | 66,299 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 126,446 | 1.264 | 20 | 50 | fits | 119,835 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 620,808 | 6.208 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 319,989 | 3.200 | 18 | 18 | fits | 193,998 | 145 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,601,808 | 16.018 | 18 | 18 | fits | 66,299 | 31 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 468,778 | 4.688 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 124,183 | 1.242 | 20 | 200 | fits | 120,449 | 140 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 611,923 | 6.119 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 125,095 | 1.251 | 20 | 20 | fits | 120,449 | 140 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 856,931 | 8.569 | 20 | 20 | fits | 111,131 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 128,680 | 1.287 | 20 | 24 | fits | 120,449 | 140 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,589,757 | 15.898 | 20 | 24 | fits | 66,594 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 127,640 | 1.276 | 20 | 50 | fits | 120,449 | 140 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 615,599 | 6.156 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 314,780 | 3.148 | 18 | 18 | fits | 187,595 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,624,358 | 16.244 | 18 | 18 | fits | 37,136 | 17 | 0.781 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 474,305 | 4.743 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 129,793 | 1.298 | 20 | 200 | fits | 119,835 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 617,450 | 6.175 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 130,705 | 1.307 | 20 | 20 | fits | 119,835 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 834,446 | 8.344 | 20 | 20 | fits | 117,657 | 40 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 134,290 | 1.343 | 20 | 24 | fits | 119,835 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,569,933 | 15.699 | 20 | 24 | fits | 66,377 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 133,250 | 1.333 | 20 | 50 | fits | 119,835 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 621,126 | 6.211 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 320,307 | 3.203 | 18 | 18 | fits | 187,512 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,617,905 | 16.179 | 18 | 18 | fits | 50,507 | 20 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 433,460 | 4.335 | 20 | 20 | fits | 160,503 | 89 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 116,913 | 1.169 | 20 | 200 | fits | 119,835 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 575,706 | 5.757 | 20 | 200 | fits | 160,503 | 89 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 117,825 | 1.178 | 20 | 20 | fits | 119,835 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 820,886 | 8.209 | 20 | 20 | fits | 111,219 | 34 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 121,410 | 1.214 | 20 | 24 | fits | 119,835 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,550,969 | 15.510 | 20 | 24 | fits | 66,784 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 120,370 | 1.204 | 20 | 50 | fits | 119,835 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 579,382 | 5.794 | 20 | 50 | fits | 160,503 | 89 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 307,496 | 3.075 | 18 | 18 | fits | 187,581 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,634,883 | 16.349 | 18 | 18 | fits | 35,611 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 473,271 | 4.733 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 122,273 | 1.223 | 20 | 200 | fits | 119,835 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 616,416 | 6.164 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 123,185 | 1.232 | 20 | 20 | fits | 119,835 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 861,424 | 8.614 | 20 | 20 | fits | 111,131 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 126,770 | 1.268 | 20 | 24 | fits | 119,835 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,603,627 | 16.036 | 20 | 24 | fits | 66,299 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 125,730 | 1.257 | 20 | 50 | fits | 119,835 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 620,092 | 6.201 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 319,273 | 3.193 | 18 | 18 | fits | 193,998 | 145 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,601,092 | 16.011 | 18 | 18 | fits | 66,299 | 31 | 0.697 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 476,943 | 4.769 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 131,548 | 1.315 | 20 | 200 | fits | 119,631 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 620,088 | 6.201 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 132,460 | 1.325 | 20 | 20 | fits | 119,631 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 865,096 | 8.651 | 20 | 20 | fits | 111,131 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 136,045 | 1.360 | 20 | 24 | fits | 119,631 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,609,717 | 16.097 | 20 | 24 | fits | 100,787 | 45 | 0.746 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 135,005 | 1.350 | 20 | 50 | fits | 119,631 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 623,764 | 6.238 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 323,030 | 3.230 | 18 | 18 | fits | 188,480 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,658,290 | 16.583 | 18 | 18 | fits | 51,108 | 20 | 0.741 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 461,383 | 4.614 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 115,988 | 1.160 | 20 | 200 | fits | 119,631 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 604,528 | 6.045 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 116,900 | 1.169 | 20 | 20 | fits | 119,631 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 817,492 | 8.175 | 20 | 20 | fits | 79,087 | 25 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 120,485 | 1.205 | 20 | 24 | fits | 119,631 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,583,085 | 15.831 | 20 | 24 | fits | 100,808 | 45 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 119,445 | 1.194 | 20 | 50 | fits | 119,631 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 608,204 | 6.082 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 307,470 | 3.075 | 18 | 18 | fits | 188,480 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,667,692 | 16.677 | 18 | 18 | fits | 35,684 | 15 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 463,994 | 4.640 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 118,668 | 1.187 | 20 | 200 | fits | 119,631 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 607,139 | 6.071 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 119,580 | 1.196 | 20 | 20 | fits | 119,631 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 824,135 | 8.241 | 20 | 20 | fits | 117,657 | 40 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 123,165 | 1.232 | 20 | 24 | fits | 119,631 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,594,533 | 15.945 | 20 | 24 | fits | 66,980 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 122,125 | 1.221 | 20 | 50 | fits | 119,631 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 610,815 | 6.108 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 310,081 | 3.101 | 18 | 18 | fits | 188,411 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,642,585 | 16.426 | 18 | 18 | fits | 50,587 | 20 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 466,743 | 4.667 | 20 | 20 | fits | 120,334 | 74 | 0.615 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 121,348 | 1.213 | 20 | 200 | fits | 119,631 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 575,752 | 5.758 | 20 | 200 | fits | 120,334 | 74 | 0.615 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 122,260 | 1.223 | 20 | 20 | fits | 119,631 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 826,592 | 8.266 | 20 | 20 | fits | 111,170 | 34 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 125,845 | 1.258 | 20 | 24 | fits | 119,631 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,602,915 | 16.029 | 20 | 24 | fits | 73,249 | 37 | 0.721 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 124,805 | 1.248 | 20 | 50 | fits | 119,631 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 579,428 | 5.794 | 20 | 50 | fits | 120,334 | 74 | 0.615 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 312,830 | 3.128 | 18 | 18 | fits | 188,480 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,650,982 | 16.510 | 18 | 18 | fits | 50,602 | 20 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 441,370 | 4.414 | 20 | 20 | fits | 160,453 | 89 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 124,028 | 1.240 | 20 | 200 | fits | 119,631 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 583,566 | 5.836 | 20 | 200 | fits | 160,453 | 89 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 124,940 | 1.249 | 20 | 20 | fits | 119,631 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 828,746 | 8.287 | 20 | 20 | fits | 111,219 | 34 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 128,525 | 1.285 | 20 | 24 | fits | 119,631 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,572,153 | 15.722 | 20 | 24 | fits | 67,166 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 127,485 | 1.275 | 20 | 50 | fits | 119,631 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 587,242 | 5.872 | 20 | 50 | fits | 160,453 | 89 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 315,441 | 3.154 | 18 | 18 | fits | 188,411 | 140 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,669,563 | 16.696 | 18 | 18 | fits | 49,207 | 18 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 466,673 | 4.667 | 20 | 20 | fits | 155,196 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 126,708 | 1.267 | 20 | 200 | fits | 119,631 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 610,514 | 6.105 | 20 | 200 | fits | 155,196 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 127,620 | 1.276 | 20 | 20 | fits | 119,631 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 855,244 | 8.552 | 20 | 20 | fits | 110,915 | 34 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 131,205 | 1.312 | 20 | 24 | fits | 119,631 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,634,724 | 16.347 | 20 | 24 | fits | 67,201 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 130,165 | 1.302 | 20 | 50 | fits | 119,631 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 614,190 | 6.142 | 20 | 50 | fits | 155,196 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 287,949 | 2.879 | 18 | 18 | fits | 158,239 | 136 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,669,387 | 16.694 | 18 | 18 | fits | 37,198 | 17 | 0.783 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 481,087 | 4.811 | 20 | 20 | fits | 154,470 | 83 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 129,388 | 1.294 | 20 | 200 | fits | 119,631 | 140 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 624,232 | 6.242 | 20 | 200 | fits | 154,470 | 83 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 130,300 | 1.303 | 20 | 20 | fits | 119,631 | 140 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 869,240 | 8.692 | 20 | 20 | fits | 111,131 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 133,885 | 1.339 | 20 | 24 | fits | 119,631 | 140 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,645,875 | 16.459 | 20 | 24 | fits | 100,731 | 45 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 132,845 | 1.328 | 20 | 50 | fits | 119,631 | 140 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 627,908 | 6.279 | 20 | 50 | fits | 154,470 | 83 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 327,174 | 3.272 | 18 | 18 | fits | 194,784 | 145 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,643,340 | 16.433 | 18 | 18 | fits | 100,731 | 45 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 511,434 | 5.114 | 20 | 20 | fits | 143,773 | 60 | 0.676 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 168,713 | 1.687 | 20 | 200 | fits | 120,153 | 142 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 643,882 | 6.439 | 20 | 200 | fits | 143,773 | 60 | 0.676 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 169,625 | 1.696 | 20 | 20 | fits | 120,153 | 142 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 888,153 | 8.882 | 20 | 20 | fits | 110,948 | 34 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 53,057 | 0.531 | 20 | 24 | fits | 54,363 | 65 | 0.571 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,532,302 | 15.323 | 20 | 24 | fits | 34,708 | 22 | 0.663 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 52,017 | 0.520 | 20 | 50 | fits | 54,363 | 65 | 0.571 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 503,785 | 5.038 | 20 | 50 | fits | 137,234 | 76 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 366,486 | 3.665 | 18 | 18 | fits | 194,771 | 145 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,664,486 | 16.645 | 18 | 18 | fits | 49,468 | 18 | 0.721 |
| an event behind 15 others | `backlog.event.if0` | 147,777 | 1.478 | 20 | 200 | fits | 117,563 | 125 | 0.547 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 670,152 | 6.702 | 20 | 20 | fits | 110,980 | 52 | 0.675 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 136,632 | 1.366 | 20 | 200 | fits | 136,840 | 143 | 0.532 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 544,872 | 5.449 | 20 | 200 | fits | 131,448 | 57 | 0.695 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 132,373 | 1.324 | 20 | 20 | fits | 136,840 | 143 | 0.532 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 737,402 | 7.374 | 20 | 20 | fits | 110,980 | 52 | 0.675 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 135,958 | 1.360 | 20 | 24 | fits | 136,840 | 143 | 0.532 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,259,033 | 12.590 | 20 | 24 | fits | 51,745 | 31 | 0.696 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 134,918 | 1.349 | 20 | 50 | fits | 136,840 | 143 | 0.532 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 543,377 | 5.434 | 20 | 50 | fits | 131,448 | 57 | 0.695 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 543,312 | 5.433 | 18 | 18 | fits | 131,448 | 57 | 0.695 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,395,846 | 13.958 | 18 | 18 | fits | 34,330 | 18 | 0.683 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 463,244 | 4.632 | 20 | 20 | fits | 154,581 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 111,942 | 1.119 | 20 | 200 | fits | 116,624 | 140 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 606,500 | 6.065 | 20 | 200 | fits | 154,581 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 112,854 | 1.129 | 20 | 20 | fits | 116,624 | 140 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 851,224 | 8.512 | 20 | 20 | fits | 110,601 | 34 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 116,439 | 1.164 | 20 | 24 | fits | 116,624 | 140 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,593,021 | 15.930 | 20 | 24 | fits | 66,294 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 115,399 | 1.154 | 20 | 50 | fits | 116,624 | 140 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 610,176 | 6.102 | 20 | 50 | fits | 154,581 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 302,323 | 3.023 | 18 | 18 | fits | 187,379 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,590,486 | 15.905 | 18 | 18 | fits | 66,294 | 31 | 0.697 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 18,845 | 0.188 | 20 | 20 | fits | 44,245 | 21 | 0.771 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 111,942 | 1.119 | 20 | 200 | fits | 116,624 | 140 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 54,324 | 0.543 | 20 | 200 | fits | 44,245 | 21 | 0.771 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 112,854 | 1.129 | 20 | 20 | fits | 116,624 | 140 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 830,987 | 8.310 | 20 | 20 | fits | 121,287 | 46 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 116,439 | 1.164 | 20 | 24 | fits | 116,624 | 140 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,507,916 | 15.079 | 20 | 24 | fits | 66,279 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 115,399 | 1.154 | 20 | 50 | fits | 116,624 | 140 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 590,449 | 5.904 | 20 | 50 | fits | 134,854 | 73 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 302,323 | 3.023 | 18 | 18 | fits | 187,379 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,556,031 | 15.560 | 18 | 18 | fits | 50,650 | 20 | 0.729 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,376,650 | 63.767 | 20 | 20 | MISS ceiling | 51,167 | 27 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,108,021 | 361.080 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,107,946 | 361.079 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,107,871 | 361.079 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,107,796 | 361.078 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 114,333 | 1.143 | 20 | 200 | fits | 113,788 | 134 | 0.504 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 583,349 | 5.833 | 20 | 200 | fits | 133,379 | 69 | 0.672 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 110,074 | 1.101 | 20 | 20 | fits | 113,788 | 134 | 0.504 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 786,631 | 7.866 | 20 | 20 | fits | 101,899 | 35 | 0.747 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 113,659 | 1.137 | 20 | 24 | fits | 113,788 | 134 | 0.504 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,513,293 | 65.133 | 20 | 24 | MISS ceiling | 31,935 | 23 | 0.577 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 112,619 | 1.126 | 20 | 50 | fits | 113,788 | 134 | 0.504 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 581,854 | 5.819 | 20 | 50 | fits | 133,379 | 69 | 0.672 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 304,143 | 3.041 | 18 | 18 | fits | 191,979 | 138 | 0.651 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,345,312 | 13.453 | 18 | 18 | fits | 50,004 | 21 | 0.700 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
