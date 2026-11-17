### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 20 paths and 0 of 118 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.117 (0.478) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.219 (0.615) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.172 (0.557) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.201 (0.574) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.045 (0.170) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.027 (0.267) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.106 (0.440) | fits | 0 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.977 (4.191) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-3.adp_available.if0` (backlog-adp@verify-3) | 3.639 (5.119) | fits | 7 adp | 9 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.701 (2.122) | fits | 15 events | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.145 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-3.service.acmp.last.if0` (backlog-adp@verify-3) | 4.212 | fits | 11 acmp | 10 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.189 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-3.service.adp.last.if0` (backlog-adp@verify-3) | 4.205 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-3.service.aecp.first.if0` (backlog-adp@verify-3) | 1.661 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.172 | fits | 15 aecp | 10 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.171 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-3.service.maap.last.if0` (backlog-adp@verify-3) | 4.242 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-3.service.srp.first.if0` (backlog-adp@verify-3) | 5.080 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-3.service.srp.last.if0` (backlog-adp@program-aged2-3) | 10.765 | fits | 31 srp | 10 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-5 | 0 | 11.336 | 12 | 152,754 (1.528) | yes | - |
| backlog-adp@program-3 | 0 | 11.240 | 11 | 152,479 (1.525) | yes | - |
| backlog-adp@verify-3 | 0 | 11.746 | 13 | 152,836 (1.528) | yes | - |
| backlog-adp@blank-aged2-3 | 1 | 11.179 | 10 | 151,725 (1.517) | yes | - |
| backlog-adp@blank-aged1-3 | 1 | 12.010 | 13 | 149,863 (1.499) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.298 | 11 | 152,316 (1.523) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.300 | 11 | 152,316 (1.523) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.532 | 13 | 152,485 (1.525) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.297 | 11 | 152,485 (1.525) | yes | - |
| backlog | 0 | 5.602 | 7 | 156,380 (1.564) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 156,380 CPU cycles (1.564 ms), backlog.
Over the windows that released their whole load only: 156,380 (1.564 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-5 | 417 | 0 | 152,754 (1.528) | fits |
| backlog-adp@program-3 | 521 | 0 | 152,479 (1.525) | fits |
| backlog-adp@verify-3 | 616 | 0 | 152,836 (1.528) | fits |
| backlog-adp@blank-aged2-3 | 717 | 0 | 151,895 (1.519) | fits |
| backlog-adp@blank-aged1-3 | 664 | 0 | 152,206 (1.522) | fits |
| backlog-adp@program-aged2-3 | 818 | 0 | 152,316 (1.523) | fits |
| backlog-adp@program-aged1-3 | 760 | 0 | 152,316 (1.523) | fits |
| backlog-adp@verify-aged2-3 | 917 | 0 | 152,485 (1.525) | fits |
| backlog-adp@verify-aged1-3 | 857 | 0 | 152,485 (1.525) | fits |
| acmp-noresp | 1890 | 0 | 40,360 (0.404) | fits |
| backlog | 286 | 0 | 156,380 (1.564) | fits |
| control | 88 | 0 | 30,145 (0.301) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-3 | 2 | +6.466 ms, 76,845 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.647 (20) | 9.353 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.721 (20) | 9.279 |
| backlog-adp@program-aged2-3 | 2 | +6.577 ms, 80,844 (0.808 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.765 (20) | 9.235 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.960 (20) | 10.040 |
| backlog-adp@verify-aged2-3 | 2 | +6.684 ms, 77,404 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.711 (20) | 9.289 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.999 (20) | 10.001 |

Least margin over the aged windows: 9.235 ms, `backlog-adp@program-aged2-3.service.srp.last.if0` at 10.765 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-5 | 299 | 94,658 (0.947) | 76,335 (0.763) |
| backlog-adp@program-3 | 328 | 96,938 (0.969) | 78,878 (0.789) |
| backlog-adp@verify-3 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@blank-aged2-3 | 297 | 76,845 (0.768) | 75,900 (0.759) |
| backlog-adp@blank-aged1-3 | 297 | 92,758 (0.928) | 76,219 (0.762) |
| backlog-adp@program-aged2-3 | 326 | 96,381 (0.964) | 78,723 (0.787) |
| backlog-adp@program-aged1-3 | 326 | 96,801 (0.968) | 79,007 (0.790) |
| backlog-adp@verify-aged2-3 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-aged1-3 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| acmp-noresp | 615 | 96,342 (0.963) | 78,143 (0.781) |
| backlog | 265 | 22,268 (0.223) | 2,242 (0.022) |
| control | 79 | 22,142 (0.221) | 2,242 (0.022) |

Longest pass that carries a step: 96,938 CPU cycles (0.969 ms), backlog-adp@program-3; longest step: 79,007 (0.790 ms), backlog-adp@program-aged1-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 352,960 | 3.530 | 20 | 20 | fits | 99,164 | 142 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 310,532 | 3.105 | 20 | 200 | fits | 150,353 | 253 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 409,080 | 4.091 | 20 | 200 | fits | 99,164 | 142 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 311,456 | 3.115 | 20 | 20 | fits | 150,353 | 253 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 409,784 | 4.098 | 20 | 20 | fits | 99,164 | 142 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 156,844 | 1.568 | 20 | 24 | fits | 152,754 | 156 | 0.396 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 314,106 | 3.141 | 20 | 24 | fits | 150,353 | 253 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 314,040 | 3.140 | 20 | 50 | fits | 150,353 | 253 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 412,808 | 4.128 | 20 | 50 | fits | 99,164 | 142 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 502,123 | 5.021 | 20 | 20 | fits | 89,381 | 30 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 992,632 | 9.926 | 20 | 20 | fits | 64,521 | 27 | 0.726 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 352,541 | 3.525 | 20 | 20 | fits | 105,387 | 166 | 0.397 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 296,530 | 2.965 | 20 | 200 | fits | 148,255 | 227 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 401,301 | 4.013 | 20 | 200 | fits | 105,387 | 166 | 0.397 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 297,454 | 2.975 | 20 | 20 | fits | 148,255 | 227 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 402,005 | 4.020 | 20 | 20 | fits | 105,387 | 166 | 0.397 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 152,839 | 1.528 | 20 | 24 | fits | 152,479 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 300,104 | 3.001 | 20 | 24 | fits | 148,255 | 227 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 300,038 | 3.000 | 20 | 50 | fits | 148,255 | 227 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 405,029 | 4.050 | 20 | 50 | fits | 105,387 | 166 | 0.397 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 489,113 | 4.891 | 20 | 20 | fits | 84,150 | 25 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 989,826 | 9.898 | 20 | 20 | fits | 72,855 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 363,932 | 3.639 | 20 | 20 | fits | 103,022 | 149 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 309,599 | 3.096 | 20 | 200 | fits | 148,034 | 249 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 420,467 | 4.205 | 20 | 200 | fits | 103,022 | 149 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 310,523 | 3.105 | 20 | 20 | fits | 148,034 | 249 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 421,171 | 4.212 | 20 | 20 | fits | 103,022 | 149 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 166,129 | 1.661 | 20 | 24 | fits | 152,836 | 155 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 313,173 | 3.132 | 20 | 24 | fits | 148,034 | 249 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 313,107 | 3.131 | 20 | 50 | fits | 148,034 | 249 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 424,195 | 4.242 | 20 | 50 | fits | 103,022 | 149 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 508,015 | 5.080 | 20 | 20 | fits | 83,886 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 998,938 | 9.989 | 20 | 20 | fits | 72,767 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 342,951 | 3.430 | 20 | 20 | fits | 96,279 | 151 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 297,060 | 2.971 | 20 | 200 | fits | 151,725 | 242 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 392,723 | 3.927 | 20 | 200 | fits | 96,279 | 151 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 297,984 | 2.980 | 20 | 20 | fits | 151,725 | 242 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 393,427 | 3.934 | 20 | 20 | fits | 96,279 | 151 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 149,899 | 1.499 | 20 | 24 | fits | 151,895 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 300,634 | 3.006 | 20 | 24 | fits | 151,725 | 242 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 300,568 | 3.006 | 20 | 50 | fits | 151,725 | 242 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 396,451 | 3.965 | 20 | 50 | fits | 96,279 | 151 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 480,252 | 4.803 | 20 | 20 | fits | 83,867 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,064,656 | 10.647 | 20 | 20 | fits | 85,201 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 348,736 | 3.487 | 20 | 20 | fits | 102,506 | 148 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 303,291 | 3.033 | 20 | 200 | fits | 149,863 | 253 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 405,181 | 4.052 | 20 | 200 | fits | 102,506 | 148 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 304,215 | 3.042 | 20 | 20 | fits | 149,863 | 253 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 405,885 | 4.059 | 20 | 20 | fits | 102,506 | 148 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 150,101 | 1.501 | 20 | 24 | fits | 152,206 | 153 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 306,865 | 3.069 | 20 | 24 | fits | 149,863 | 253 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 306,799 | 3.068 | 20 | 50 | fits | 149,863 | 253 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 408,909 | 4.089 | 20 | 50 | fits | 102,506 | 148 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 493,250 | 4.933 | 20 | 20 | fits | 84,407 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,072,107 | 10.721 | 20 | 20 | fits | 85,396 | 28 | 0.623 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 344,439 | 3.444 | 20 | 20 | fits | 100,328 | 142 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 301,312 | 3.013 | 20 | 200 | fits | 147,987 | 248 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 401,024 | 4.010 | 20 | 200 | fits | 100,328 | 142 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 302,236 | 3.022 | 20 | 20 | fits | 147,987 | 248 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 401,728 | 4.017 | 20 | 20 | fits | 100,328 | 142 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 157,889 | 1.579 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 304,886 | 3.049 | 20 | 24 | fits | 147,987 | 248 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 304,820 | 3.048 | 20 | 50 | fits | 147,987 | 248 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 404,752 | 4.048 | 20 | 50 | fits | 100,328 | 142 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 488,840 | 4.888 | 20 | 20 | fits | 84,154 | 25 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,076,485 | 10.765 | 20 | 20 | fits | 85,326 | 28 | 0.617 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 352,581 | 3.526 | 20 | 20 | fits | 97,360 | 154 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 304,624 | 3.046 | 20 | 200 | fits | 149,396 | 233 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 401,368 | 4.014 | 20 | 200 | fits | 97,360 | 154 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 305,548 | 3.055 | 20 | 20 | fits | 149,396 | 233 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 402,072 | 4.021 | 20 | 20 | fits | 97,360 | 154 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 159,792 | 1.598 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 308,198 | 3.082 | 20 | 24 | fits | 149,396 | 233 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 308,132 | 3.081 | 20 | 50 | fits | 149,396 | 233 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 405,096 | 4.051 | 20 | 50 | fits | 97,360 | 154 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 489,019 | 4.890 | 20 | 20 | fits | 83,989 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 996,011 | 9.960 | 20 | 20 | fits | 85,230 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 358,229 | 3.582 | 20 | 20 | fits | 103,032 | 149 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 303,829 | 3.038 | 20 | 200 | fits | 148,170 | 249 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 414,764 | 4.148 | 20 | 200 | fits | 103,032 | 149 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 304,753 | 3.048 | 20 | 20 | fits | 148,170 | 249 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 415,468 | 4.155 | 20 | 20 | fits | 103,032 | 149 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 160,223 | 1.602 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 307,403 | 3.074 | 20 | 24 | fits | 148,170 | 249 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 307,337 | 3.073 | 20 | 50 | fits | 148,170 | 249 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 418,492 | 4.185 | 20 | 50 | fits | 103,032 | 149 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 502,312 | 5.023 | 20 | 20 | fits | 83,886 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,071,094 | 10.711 | 20 | 20 | fits | 72,865 | 25 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 355,531 | 3.555 | 20 | 20 | fits | 96,490 | 151 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 309,535 | 3.095 | 20 | 200 | fits | 150,439 | 237 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 405,409 | 4.054 | 20 | 200 | fits | 96,490 | 151 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 310,459 | 3.105 | 20 | 20 | fits | 150,439 | 237 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 406,113 | 4.061 | 20 | 20 | fits | 96,490 | 151 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 163,660 | 1.637 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 313,109 | 3.131 | 20 | 24 | fits | 150,439 | 237 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 313,043 | 3.130 | 20 | 50 | fits | 150,439 | 237 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 409,137 | 4.091 | 20 | 50 | fits | 96,490 | 151 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 493,535 | 4.935 | 20 | 20 | fits | 84,464 | 25 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 999,924 | 9.999 | 20 | 20 | fits | 85,283 | 28 | 0.615 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 21,857 | 0.219 | 20 | 20 | fits | 30,030 | 21 (35) | 0.825 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 17,167 | 0.172 | 20 | 20 | fits | 26,833 | 17 (14) | 0.865 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 20,146 | 0.201 | 20 | 20 | fits | 26,021 | 18 (14) | 0.861 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 11,652 | 0.117 | 20 | 20 | fits | 29,632 | 21 (35) | 0.820 |
| an event behind 15 others | `backlog.event.if0` | 170,128 | 1.701 | 20 | 200 | fits | 55,854 | 78 | 0.568 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 397,670 | 3.977 | 20 | 20 | fits | 146,887 | 168 | 0.376 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 418,850 | 4.189 | 20 | 200 | fits | 146,887 | 168 | 0.376 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 418,234 | 4.182 | 20 | 200 | fits | 146,887 | 168 | 0.376 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 414,528 | 4.145 | 20 | 20 | fits | 146,887 | 168 | 0.376 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 413,692 | 4.137 | 20 | 20 | fits | 146,887 | 168 | 0.376 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 155,489 | 1.555 | 20 | 24 | fits | 156,380 | 158 | 0.405 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 417,178 | 4.172 | 20 | 24 | fits | 146,887 | 168 | 0.376 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 417,112 | 4.171 | 20 | 50 | fits | 146,887 | 168 | 0.376 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 416,716 | 4.167 | 20 | 50 | fits | 146,887 | 168 | 0.376 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 447,885 | 4.479 | 20 | 20 | fits | 31,235 | 56 | 0.234 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 507,983 | 5.080 | 20 | 20 | fits | 24,666 | 41 | 0.197 |
| LINK_UP | `adp.link_up.if0` | 2,674 | 0.027 | 20 | 200 | fits | 26,711 | 43 (11) | 0.737 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,642 | 0.106 | 20 | 200 | fits | 23,487 | 23 (39) | 0.762 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,546 | 0.045 | 20 | 200 | fits | 17,026 | 16 (31) | 0.663 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
