### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 12 paths and 0 of 254 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.118 (0.528) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.250 (5.723) | fits | 7 adp | 23 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 3.758 | fits | 0 acmp | 23 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 4.839 | fits | 11 acmp | 23 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 3.749 | fits | 0 adp | 23 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.832 | fits | 7 adp | 23 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.354 | fits | 0 aecp | 23 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.aecp.last.if0` (backlog-adp@blank-0) | 3.785 | fits | 15 aecp | 23 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 3.784 | fits | 0 maap | 23 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.869 | fits | 6 maap | 23 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 5.818 | fits | 0 srp | 23 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-6.service.srp.last.if0` (backlog-adp@blank-aged1-6) | 9.970 | fits | 31 srp | 23 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.243 | 11 | 148,553 (1.486) | yes | - |
| backlog-adp@blank-2 | 0 | 10.369 | 10 | 148,236 (1.482) | yes | - |
| backlog-adp@blank-4 | 0 | 10.318 | 10 | 148,179 (1.482) | yes | - |
| backlog-adp@blank-6 | 0 | 10.662 | 12 | 148,334 (1.483) | yes | - |
| backlog-adp@program-0 | 0 | 10.452 | 11 | 148,354 (1.484) | yes | - |
| backlog-adp@program-2 | 0 | 10.372 | 10 | 149,403 (1.494) | yes | - |
| backlog-adp@program-4 | 0 | 9.655 | 11 | 148,486 (1.485) | yes | - |
| backlog-adp@program-6 | 0 | 9.615 | 10 | 148,362 (1.484) | yes | - |
| backlog-adp@verify-0 | 0 | 10.736 | 11 | 148,378 (1.484) | yes | - |
| backlog-adp@verify-2 | 0 | 10.303 | 10 | 148,079 (1.481) | yes | - |
| backlog-adp@verify-4 | 0 | 10.914 | 12 | 148,136 (1.481) | yes | - |
| backlog-adp@verify-6 | 0 | 10.339 | 10 | 148,251 (1.483) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 10.267 | 10 | 145,868 (1.459) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.390 | 11 | 148,338 (1.483) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.244 | 10 | 149,544 (1.495) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.191 | 9 | 144,916 (1.449) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.228 | 13 | 147,698 (1.477) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.157 | 12 | 147,698 (1.477) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.305 | 14 | 147,716 (1.477) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.218 | 12 | 147,669 (1.477) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.748 | 12 | 147,953 (1.480) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.295 | 10 | 147,844 (1.478) | yes | - |
| backlog-adp@program-aged2-4 | 1 | 10.266 | 9 | 144,434 (1.444) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3607 | 0 | 41,840 (0.418) | fits |
| backlog-adp@blank-0 | 406 | 0 | 148,553 (1.486) | fits |
| backlog-adp@blank-2 | 405 | 0 | 148,236 (1.482) | fits |
| backlog-adp@blank-4 | 405 | 0 | 148,179 (1.482) | fits |
| backlog-adp@blank-6 | 407 | 0 | 148,334 (1.483) | fits |
| backlog-adp@program-0 | 502 | 0 | 148,354 (1.484) | fits |
| backlog-adp@program-2 | 503 | 0 | 149,403 (1.494) | fits |
| backlog-adp@program-4 | 505 | 0 | 148,486 (1.485) | fits |
| backlog-adp@program-6 | 506 | 0 | 148,362 (1.484) | fits |
| backlog-adp@verify-0 | 590 | 0 | 148,378 (1.484) | fits |
| backlog-adp@verify-2 | 589 | 0 | 148,079 (1.481) | fits |
| backlog-adp@verify-4 | 591 | 0 | 148,136 (1.481) | fits |
| backlog-adp@verify-6 | 591 | 0 | 148,251 (1.483) | fits |
| backlog-adp@blank-aged2-0 | 721 | 0 | 153,200 (1.532) | fits |
| backlog-adp@blank-aged2-2 | 734 | 0 | 148,338 (1.483) | fits |
| backlog-adp@blank-aged2-4 | 749 | 0 | 149,544 (1.495) | fits |
| backlog-adp@blank-aged2-6 | 765 | 0 | 147,510 (1.475) | fits |
| backlog-adp@blank-aged1-0 | 659 | 0 | 147,698 (1.477) | fits |
| backlog-adp@blank-aged1-2 | 674 | 0 | 147,698 (1.477) | fits |
| backlog-adp@blank-aged1-4 | 692 | 0 | 147,716 (1.477) | fits |
| backlog-adp@blank-aged1-6 | 707 | 0 | 147,669 (1.477) | fits |
| backlog-adp@program-aged2-0 | 813 | 0 | 147,953 (1.480) | fits |
| backlog-adp@program-aged2-2 | 827 | 0 | 147,844 (1.478) | fits |
| backlog-adp@program-aged2-4 | 843 | 0 | 147,844 (1.478) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.192 ms, 76,386 (0.764 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.952 (20) | 11.048 |
| backlog-adp@blank-aged2-2 | 2 | +8.485 ms, 76,482 (0.765 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.780 (20) | 10.220 |
| backlog-adp@blank-aged2-4 | 2 | +5.812 ms, 76,572 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.754 (20) | 10.246 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.697 (20) | 10.303 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.994 (20) | 11.006 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.553 (20) | 10.447 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.774 (20) | 10.226 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.970 (20) | 10.030 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.917 (20) | 11.083 |
| backlog-adp@program-aged2-2 | 2 | +8.392 ms, 80,312 (0.803 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.796 (20) | 10.204 |
| backlog-adp@program-aged2-4 | 2 | +5.835 ms, 80,312 (0.803 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.771 (20) | 10.229 |

Least margin over the aged windows: 10.030 ms, `backlog-adp@blank-aged1-6.service.srp.last.if0` at 9.970 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 95,856 (0.959) | 78,015 (0.780) |
| backlog-adp@blank-0 | 299 | 90,451 (0.905) | 76,020 (0.760) |
| backlog-adp@blank-2 | 299 | 91,469 (0.915) | 76,194 (0.762) |
| backlog-adp@blank-4 | 299 | 91,597 (0.916) | 76,194 (0.762) |
| backlog-adp@blank-6 | 299 | 98,086 (0.981) | 76,252 (0.763) |
| backlog-adp@program-0 | 328 | 95,454 (0.955) | 78,722 (0.787) |
| backlog-adp@program-2 | 328 | 95,776 (0.958) | 78,879 (0.789) |
| backlog-adp@program-4 | 329 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@program-6 | 329 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-0 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-2 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-4 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-6 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@blank-aged2-0 | 297 | 76,386 (0.764) | 75,474 (0.755) |
| backlog-adp@blank-aged2-2 | 297 | 76,482 (0.765) | 75,558 (0.756) |
| backlog-adp@blank-aged2-4 | 297 | 76,572 (0.766) | 75,648 (0.756) |
| backlog-adp@blank-aged2-6 | 297 | 84,224 (0.842) | 75,493 (0.755) |
| backlog-adp@blank-aged1-0 | 298 | 96,481 (0.965) | 76,210 (0.762) |
| backlog-adp@blank-aged1-2 | 297 | 97,481 (0.975) | 76,282 (0.763) |
| backlog-adp@blank-aged1-4 | 297 | 90,051 (0.901) | 76,128 (0.761) |
| backlog-adp@blank-aged1-6 | 297 | 91,227 (0.912) | 76,212 (0.762) |
| backlog-adp@program-aged2-0 | 327 | 95,507 (0.955) | 79,049 (0.790) |
| backlog-adp@program-aged2-2 | 326 | 95,454 (0.955) | 78,349 (0.783) |
| backlog-adp@program-aged2-4 | 326 | 95,454 (0.955) | 78,349 (0.783) |

Longest pass that carries a step: 98,086 CPU cycles (0.981 ms), backlog-adp@blank-6; longest step: 79,049 (0.790 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 11,775 | 0.118 | 20 | 20 | fits | 33,568 | 19 (14) | 0.882 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 425,004 | 4.250 | 20 | 20 | fits | 108,893 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 374,895 | 3.749 | 20 | 200 | fits | 144,088 | 226 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 483,172 | 4.832 | 20 | 200 | fits | 108,893 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 375,819 | 3.758 | 20 | 20 | fits | 144,088 | 226 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 483,876 | 4.839 | 20 | 20 | fits | 108,893 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 235,371 | 2.354 | 20 | 24 | fits | 148,553 | 155 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 378,469 | 3.785 | 20 | 24 | fits | 144,088 | 226 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 378,403 | 3.784 | 20 | 50 | fits | 144,088 | 226 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 486,900 | 4.869 | 20 | 50 | fits | 108,893 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 577,036 | 5.770 | 20 | 20 | fits | 90,202 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 980,625 | 9.806 | 20 | 20 | fits | 52,962 | 20 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 350,056 | 3.501 | 20 | 20 | fits | 108,364 | 163 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 299,878 | 2.999 | 20 | 200 | fits | 144,072 | 226 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 407,626 | 4.076 | 20 | 200 | fits | 108,364 | 163 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 300,802 | 3.008 | 20 | 20 | fits | 144,072 | 226 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 408,330 | 4.083 | 20 | 20 | fits | 108,364 | 163 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 160,370 | 1.604 | 20 | 24 | fits | 148,236 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 303,452 | 3.035 | 20 | 24 | fits | 144,072 | 226 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 303,386 | 3.034 | 20 | 50 | fits | 144,072 | 226 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 411,354 | 4.114 | 20 | 50 | fits | 108,364 | 163 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 501,443 | 5.014 | 20 | 20 | fits | 90,155 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 911,843 | 9.118 | 20 | 20 | fits | 52,689 | 20 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 358,789 | 3.588 | 20 | 20 | fits | 112,925 | 170 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 297,043 | 2.970 | 20 | 200 | fits | 143,672 | 227 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 417,582 | 4.176 | 20 | 200 | fits | 112,925 | 170 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 297,967 | 2.980 | 20 | 20 | fits | 143,672 | 227 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 418,286 | 4.183 | 20 | 20 | fits | 112,925 | 170 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 157,935 | 1.579 | 20 | 24 | fits | 148,179 | 155 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 300,617 | 3.006 | 20 | 24 | fits | 143,672 | 227 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 300,551 | 3.006 | 20 | 50 | fits | 143,672 | 227 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 421,310 | 4.213 | 20 | 50 | fits | 112,925 | 170 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 511,994 | 5.120 | 20 | 20 | fits | 90,750 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 906,622 | 9.066 | 20 | 20 | fits | 52,507 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 369,799 | 3.698 | 20 | 20 | fits | 117,510 | 169 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 303,656 | 3.037 | 20 | 200 | fits | 145,049 | 231 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 420,550 | 4.205 | 20 | 200 | fits | 117,510 | 169 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 304,580 | 3.046 | 20 | 20 | fits | 145,049 | 231 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 421,254 | 4.213 | 20 | 20 | fits | 117,510 | 169 | 0.472 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 155,712 | 1.557 | 20 | 24 | fits | 148,334 | 156 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 307,230 | 3.072 | 20 | 24 | fits | 145,049 | 231 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 307,164 | 3.072 | 20 | 50 | fits | 145,049 | 231 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 424,278 | 4.243 | 20 | 50 | fits | 117,510 | 169 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 514,597 | 5.146 | 20 | 20 | fits | 90,385 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 902,240 | 9.022 | 20 | 20 | fits | 52,435 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 340,004 | 3.400 | 20 | 20 | fits | 108,682 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 290,099 | 2.901 | 20 | 200 | fits | 143,377 | 226 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 398,165 | 3.982 | 20 | 200 | fits | 108,682 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 291,023 | 2.910 | 20 | 20 | fits | 143,377 | 226 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 398,869 | 3.989 | 20 | 20 | fits | 108,682 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 151,286 | 1.513 | 20 | 24 | fits | 148,354 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 293,673 | 2.937 | 20 | 24 | fits | 143,377 | 226 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 293,607 | 2.936 | 20 | 50 | fits | 143,377 | 226 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 401,893 | 4.019 | 20 | 50 | fits | 108,682 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 491,408 | 4.914 | 20 | 20 | fits | 89,581 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 895,902 | 8.959 | 20 | 20 | fits | 52,452 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 346,053 | 3.461 | 20 | 20 | fits | 102,535 | 142 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 301,527 | 3.015 | 20 | 200 | fits | 149,403 | 248 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 403,446 | 4.034 | 20 | 200 | fits | 102,535 | 142 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 302,451 | 3.025 | 20 | 20 | fits | 149,403 | 248 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 404,150 | 4.042 | 20 | 20 | fits | 102,535 | 142 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 156,688 | 1.567 | 20 | 24 | fits | 148,465 | 155 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 305,101 | 3.051 | 20 | 24 | fits | 149,403 | 248 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 305,035 | 3.050 | 20 | 50 | fits | 149,403 | 248 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 407,174 | 4.072 | 20 | 50 | fits | 102,535 | 142 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 492,430 | 4.924 | 20 | 20 | fits | 85,322 | 30 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 906,526 | 9.065 | 20 | 20 | fits | 68,654 | 31 | 0.678 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 358,240 | 3.582 | 20 | 20 | fits | 112,884 | 170 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 288,763 | 2.888 | 20 | 200 | fits | 144,159 | 227 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 409,555 | 4.096 | 20 | 200 | fits | 112,884 | 170 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 289,687 | 2.897 | 20 | 20 | fits | 144,159 | 227 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 410,259 | 4.103 | 20 | 20 | fits | 112,884 | 170 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 149,168 | 1.492 | 20 | 24 | fits | 148,486 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 292,337 | 2.923 | 20 | 24 | fits | 144,159 | 227 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 292,271 | 2.923 | 20 | 50 | fits | 144,159 | 227 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 413,283 | 4.133 | 20 | 50 | fits | 112,884 | 170 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 503,473 | 5.035 | 20 | 20 | fits | 90,256 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 891,204 | 8.912 | 20 | 20 | fits | 52,507 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 345,069 | 3.451 | 20 | 20 | fits | 108,763 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 295,100 | 2.951 | 20 | 200 | fits | 143,850 | 226 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 403,247 | 4.032 | 20 | 200 | fits | 108,763 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 296,024 | 2.960 | 20 | 20 | fits | 143,850 | 226 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 403,951 | 4.040 | 20 | 20 | fits | 108,763 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 155,814 | 1.558 | 20 | 24 | fits | 148,362 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 298,674 | 2.987 | 20 | 24 | fits | 143,850 | 226 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 298,608 | 2.986 | 20 | 50 | fits | 143,850 | 226 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 406,975 | 4.070 | 20 | 50 | fits | 108,763 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 492,327 | 4.923 | 20 | 20 | fits | 85,418 | 30 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 906,977 | 9.070 | 20 | 20 | fits | 63,273 | 24 | 0.593 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 381,540 | 3.815 | 20 | 20 | fits | 108,754 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 324,049 | 3.240 | 20 | 200 | fits | 143,788 | 226 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 432,187 | 4.322 | 20 | 200 | fits | 108,754 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 324,973 | 3.250 | 20 | 20 | fits | 143,788 | 226 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 432,891 | 4.329 | 20 | 20 | fits | 108,754 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 184,825 | 1.848 | 20 | 24 | fits | 148,378 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 327,623 | 3.276 | 20 | 24 | fits | 143,788 | 226 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 327,557 | 3.276 | 20 | 50 | fits | 143,788 | 226 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 435,915 | 4.359 | 20 | 50 | fits | 108,754 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 525,883 | 5.259 | 20 | 20 | fits | 90,034 | 28 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 929,525 | 9.295 | 20 | 20 | fits | 52,962 | 20 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 350,106 | 3.501 | 20 | 20 | fits | 108,754 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 292,615 | 2.926 | 20 | 200 | fits | 143,770 | 226 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 400,753 | 4.008 | 20 | 200 | fits | 108,754 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 293,539 | 2.935 | 20 | 20 | fits | 143,770 | 226 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 401,457 | 4.015 | 20 | 20 | fits | 108,754 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 153,409 | 1.534 | 20 | 24 | fits | 148,079 | 155 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 296,189 | 2.962 | 20 | 24 | fits | 143,770 | 226 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 296,123 | 2.961 | 20 | 50 | fits | 143,770 | 226 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 404,481 | 4.045 | 20 | 50 | fits | 108,754 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 494,694 | 4.947 | 20 | 20 | fits | 90,279 | 29 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 904,926 | 9.049 | 20 | 20 | fits | 52,585 | 20 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 352,004 | 3.520 | 20 | 20 | fits | 112,549 | 170 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 289,744 | 2.897 | 20 | 200 | fits | 143,220 | 227 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 409,967 | 4.100 | 20 | 200 | fits | 112,549 | 170 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 290,668 | 2.907 | 20 | 20 | fits | 143,220 | 227 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 410,671 | 4.107 | 20 | 20 | fits | 112,549 | 170 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 151,088 | 1.511 | 20 | 24 | fits | 148,136 | 155 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 293,318 | 2.933 | 20 | 24 | fits | 143,220 | 227 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 293,252 | 2.933 | 20 | 50 | fits | 143,220 | 227 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 413,695 | 4.137 | 20 | 50 | fits | 112,549 | 170 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 499,469 | 4.995 | 20 | 20 | fits | 85,840 | 30 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 897,943 | 8.979 | 20 | 20 | fits | 63,179 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 346,618 | 3.466 | 20 | 20 | fits | 114,957 | 184 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 296,701 | 2.967 | 20 | 200 | fits | 145,277 | 209 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 411,042 | 4.110 | 20 | 200 | fits | 114,957 | 184 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 297,625 | 2.976 | 20 | 20 | fits | 145,277 | 209 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 411,746 | 4.117 | 20 | 20 | fits | 114,957 | 184 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 155,988 | 1.560 | 20 | 24 | fits | 148,251 | 155 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 300,275 | 3.003 | 20 | 24 | fits | 145,277 | 209 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 300,209 | 3.002 | 20 | 50 | fits | 145,277 | 209 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 414,770 | 4.148 | 20 | 50 | fits | 114,957 | 184 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 504,632 | 5.046 | 20 | 20 | fits | 89,928 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 908,217 | 9.082 | 20 | 20 | fits | 58,261 | 27 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 346,118 | 3.461 | 20 | 20 | fits | 113,350 | 170 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 291,424 | 2.914 | 20 | 200 | fits | 145,868 | 231 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 404,158 | 4.042 | 20 | 200 | fits | 113,350 | 170 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 292,348 | 2.923 | 20 | 20 | fits | 145,868 | 231 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 404,862 | 4.049 | 20 | 20 | fits | 113,350 | 170 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 150,120 | 1.501 | 20 | 24 | fits | 153,200 | 157 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 294,998 | 2.950 | 20 | 24 | fits | 145,868 | 231 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 294,932 | 2.949 | 20 | 50 | fits | 145,868 | 231 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 407,886 | 4.079 | 20 | 50 | fits | 113,350 | 170 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 507,369 | 5.074 | 20 | 20 | fits | 90,068 | 29 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 895,231 | 8.952 | 20 | 20 | fits | 52,449 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 352,303 | 3.523 | 20 | 20 | fits | 108,480 | 163 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 301,758 | 3.018 | 20 | 200 | fits | 144,647 | 231 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 409,622 | 4.096 | 20 | 200 | fits | 108,480 | 163 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 302,682 | 3.027 | 20 | 20 | fits | 144,647 | 231 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 410,326 | 4.103 | 20 | 20 | fits | 108,480 | 163 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 153,010 | 1.530 | 20 | 24 | fits | 148,338 | 153 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 305,332 | 3.053 | 20 | 24 | fits | 144,647 | 231 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 305,266 | 3.053 | 20 | 50 | fits | 144,647 | 231 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 413,350 | 4.133 | 20 | 50 | fits | 108,480 | 163 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 502,783 | 5.028 | 20 | 20 | fits | 89,499 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 977,991 | 9.780 | 20 | 20 | fits | 56,772 | 28 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 337,664 | 3.377 | 20 | 20 | fits | 102,351 | 142 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 293,186 | 2.932 | 20 | 200 | fits | 149,544 | 248 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 394,921 | 3.949 | 20 | 200 | fits | 102,351 | 142 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 294,110 | 2.941 | 20 | 20 | fits | 149,544 | 248 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 395,625 | 3.956 | 20 | 20 | fits | 102,351 | 142 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 148,206 | 1.482 | 20 | 24 | fits | 147,510 | 152 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 296,760 | 2.968 | 20 | 24 | fits | 149,544 | 248 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 296,694 | 2.967 | 20 | 50 | fits | 149,544 | 248 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 398,649 | 3.986 | 20 | 50 | fits | 102,351 | 142 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 488,109 | 4.881 | 20 | 20 | fits | 89,526 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 975,355 | 9.754 | 20 | 20 | fits | 52,412 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 342,788 | 3.428 | 20 | 20 | fits | 117,163 | 170 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 284,574 | 2.846 | 20 | 200 | fits | 144,916 | 231 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 401,121 | 4.011 | 20 | 200 | fits | 117,163 | 170 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 285,498 | 2.855 | 20 | 20 | fits | 144,916 | 231 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 401,825 | 4.018 | 20 | 20 | fits | 117,163 | 170 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 144,222 | 1.442 | 20 | 24 | fits | 147,510 | 152 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 288,148 | 2.881 | 20 | 24 | fits | 144,916 | 231 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 288,082 | 2.881 | 20 | 50 | fits | 144,916 | 231 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 404,849 | 4.048 | 20 | 50 | fits | 117,163 | 170 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 581,767 | 5.818 | 20 | 20 | fits | 92,760 | 35 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 969,688 | 9.697 | 20 | 20 | fits | 52,451 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 344,267 | 3.443 | 20 | 20 | fits | 108,810 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 294,198 | 2.942 | 20 | 200 | fits | 143,471 | 226 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 402,392 | 4.024 | 20 | 200 | fits | 108,810 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 295,122 | 2.951 | 20 | 20 | fits | 143,471 | 226 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 403,096 | 4.031 | 20 | 20 | fits | 108,810 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 155,291 | 1.553 | 20 | 24 | fits | 147,698 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 297,772 | 2.978 | 20 | 24 | fits | 143,471 | 226 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 297,706 | 2.977 | 20 | 50 | fits | 143,471 | 226 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 406,120 | 4.061 | 20 | 50 | fits | 108,810 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 496,103 | 4.961 | 20 | 20 | fits | 90,049 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 899,377 | 8.994 | 20 | 20 | fits | 52,465 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 345,748 | 3.457 | 20 | 20 | fits | 113,353 | 170 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 290,994 | 2.910 | 20 | 200 | fits | 143,995 | 226 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 403,731 | 4.037 | 20 | 200 | fits | 113,353 | 170 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 291,918 | 2.919 | 20 | 20 | fits | 143,995 | 226 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 404,435 | 4.044 | 20 | 20 | fits | 113,353 | 170 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 151,563 | 1.516 | 20 | 24 | fits | 147,698 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 294,568 | 2.946 | 20 | 24 | fits | 143,995 | 226 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 294,502 | 2.945 | 20 | 50 | fits | 143,995 | 226 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 407,459 | 4.075 | 20 | 50 | fits | 113,353 | 170 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 506,602 | 5.066 | 20 | 20 | fits | 90,387 | 29 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 955,271 | 9.553 | 20 | 20 | fits | 65,921 | 25 | 0.679 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 353,320 | 3.533 | 20 | 20 | fits | 108,799 | 163 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 295,656 | 2.957 | 20 | 200 | fits | 144,985 | 231 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 403,839 | 4.038 | 20 | 200 | fits | 108,799 | 163 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 296,580 | 2.966 | 20 | 20 | fits | 144,985 | 231 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 404,543 | 4.045 | 20 | 20 | fits | 108,799 | 163 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 147,853 | 1.479 | 20 | 24 | fits | 147,716 | 153 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 299,230 | 2.992 | 20 | 24 | fits | 144,985 | 231 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 299,164 | 2.992 | 20 | 50 | fits | 144,985 | 231 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 407,567 | 4.076 | 20 | 50 | fits | 108,799 | 163 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 497,600 | 4.976 | 20 | 20 | fits | 90,099 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 977,430 | 9.774 | 20 | 20 | fits | 63,326 | 25 | 0.592 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 366,113 | 3.661 | 20 | 20 | fits | 129,870 | 169 | 0.500 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 296,437 | 2.964 | 20 | 200 | fits | 143,821 | 226 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 425,691 | 4.257 | 20 | 200 | fits | 129,870 | 169 | 0.500 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 297,361 | 2.974 | 20 | 20 | fits | 143,821 | 226 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 426,395 | 4.264 | 20 | 20 | fits | 129,870 | 169 | 0.500 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 157,180 | 1.572 | 20 | 24 | fits | 147,669 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 300,011 | 3.000 | 20 | 24 | fits | 143,821 | 226 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 299,945 | 2.999 | 20 | 50 | fits | 143,821 | 226 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 429,419 | 4.294 | 20 | 50 | fits | 129,870 | 169 | 0.500 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 560,681 | 5.607 | 20 | 20 | fits | 89,800 | 29 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 997,044 | 9.970 | 20 | 20 | fits | 52,412 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 361,111 | 3.611 | 20 | 20 | fits | 109,461 | 166 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 302,036 | 3.020 | 20 | 200 | fits | 143,662 | 227 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 410,881 | 4.109 | 20 | 200 | fits | 109,461 | 166 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 302,960 | 3.030 | 20 | 20 | fits | 143,662 | 227 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 411,585 | 4.116 | 20 | 20 | fits | 109,461 | 166 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 155,540 | 1.555 | 20 | 24 | fits | 147,953 | 153 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 305,610 | 3.056 | 20 | 24 | fits | 143,662 | 227 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 305,544 | 3.055 | 20 | 50 | fits | 143,662 | 227 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 414,609 | 4.146 | 20 | 50 | fits | 109,461 | 166 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 504,189 | 5.042 | 20 | 20 | fits | 89,646 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 891,710 | 8.917 | 20 | 20 | fits | 52,507 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 338,978 | 3.390 | 20 | 20 | fits | 108,260 | 163 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 288,940 | 2.889 | 20 | 200 | fits | 143,815 | 226 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 396,584 | 3.966 | 20 | 200 | fits | 108,260 | 163 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 289,864 | 2.899 | 20 | 20 | fits | 143,815 | 226 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 397,288 | 3.973 | 20 | 20 | fits | 108,260 | 163 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 149,689 | 1.497 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 292,514 | 2.925 | 20 | 24 | fits | 143,815 | 226 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 292,448 | 2.924 | 20 | 50 | fits | 143,815 | 226 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 400,312 | 4.003 | 20 | 50 | fits | 108,260 | 163 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 489,875 | 4.899 | 20 | 20 | fits | 89,629 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 979,587 | 9.796 | 20 | 20 | fits | 63,806 | 25 | 0.610 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 336,011 | 3.360 | 20 | 20 | fits | 108,369 | 163 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 285,677 | 2.857 | 20 | 200 | fits | 144,434 | 231 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 393,430 | 3.934 | 20 | 200 | fits | 108,369 | 163 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 286,601 | 2.866 | 20 | 20 | fits | 144,434 | 231 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 394,134 | 3.941 | 20 | 20 | fits | 108,369 | 163 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 145,807 | 1.458 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 289,251 | 2.893 | 20 | 24 | fits | 144,434 | 231 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 289,185 | 2.892 | 20 | 50 | fits | 144,434 | 231 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 397,158 | 3.972 | 20 | 50 | fits | 108,369 | 163 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 486,988 | 4.870 | 20 | 20 | fits | 89,896 | 29 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 977,138 | 9.771 | 20 | 20 | fits | 63,195 | 24 | 0.591 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
