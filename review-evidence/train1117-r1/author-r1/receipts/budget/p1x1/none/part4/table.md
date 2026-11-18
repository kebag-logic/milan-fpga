### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 14 paths and 0 of 113 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.048 (0.164) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.028 (0.278) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.161 (0.483) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-4.adp_available.if0` (backlog-adp@program-4) | 4.440 (5.915) | fits | 7 adp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-4.service.acmp.first.if0` (backlog-adp@verify-4) | 3.852 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-4.service.acmp.last.if0` (backlog-adp@verify-4) | 4.979 | fits | 11 acmp | 10 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-4.service.adp.first.if0` (backlog-adp@verify-4) | 3.843 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-4.service.adp.last.if0` (backlog-adp@verify-4) | 4.972 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-4.service.aecp.first.if0` (backlog-adp@verify-4) | 2.396 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-4.service.aecp.last.if0` (backlog-adp@verify-4) | 3.879 | fits | 15 aecp | 10 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-4.service.maap.first.if0` (backlog-adp@verify-4) | 3.878 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-4.service.maap.last.if0` (backlog-adp@verify-4) | 5.009 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-4.service.srp.first.if0` (backlog-adp@verify-4) | 5.855 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-4.service.srp.last.if0` (backlog-adp@verify-aged2-4) | 11.127 | fits | 31 srp | 10 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 14.196 | 13 | 153,018 (1.530) | yes | - |
| backlog-adp@blank-4 | 0 | 13.565 | 12 | 153,370 (1.534) | yes | - |
| backlog-adp@program-4 | 0 | 12.331 | 11 | 152,957 (1.530) | yes | - |
| backlog-adp@verify-4 | 0 | 13.788 | 11 | 152,657 (1.527) | yes | - |
| backlog-adp@blank-aged2-4 | 1 | 14.813 | 12 | 149,872 (1.499) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 12.943 | 11 | 151,466 (1.515) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 12.324 | 11 | 151,393 (1.514) | yes | - |
| backlog-adp@program-aged1-4 | 1 | 12.237 | 10 | 150,432 (1.504) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 13.929 | 12 | 151,570 (1.516) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 15.071 | 13 | 151,480 (1.515) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 484 | 0 | 153,018 (1.530) | fits |
| backlog-adp@blank-4 | 483 | 0 | 153,370 (1.534) | fits |
| backlog-adp@program-4 | 493 | 0 | 152,957 (1.530) | fits |
| backlog-adp@verify-4 | 499 | 0 | 152,657 (1.527) | fits |
| backlog-adp@blank-aged2-4 | 774 | 0 | 151,380 (1.514) | fits |
| backlog-adp@blank-aged1-4 | 712 | 0 | 151,466 (1.515) | fits |
| backlog-adp@program-aged2-4 | 800 | 0 | 151,393 (1.514) | fits |
| backlog-adp@program-aged1-4 | 739 | 0 | 151,307 (1.513) | fits |
| backlog-adp@verify-aged2-4 | 818 | 0 | 151,570 (1.516) | fits |
| backlog-adp@verify-aged1-4 | 758 | 0 | 151,480 (1.515) | fits |
| save | 610 | 0 | 46,323 (0.463) | fits |
| control | 88 | 0 | 30,398 (0.304) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-4 | 2 | +5.917 ms, 76,941 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.813 (20) | 9.187 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.171 (20) | 9.829 |
| backlog-adp@program-aged2-4 | 2 | none | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.906 (20) | 9.094 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.081 (20) | 9.919 |
| backlog-adp@verify-aged2-4 | 2 | +5.161 ms, 77,572 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.127 (20) | 8.873 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.118 (20) | 9.882 |

Least margin over the aged windows: 8.873 ms, `backlog-adp@verify-aged2-4.service.srp.last.if0` at 11.127 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save | 1081.121 | 4,070 | 102 | - | 25.850 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 342 | 93,288 (0.933) | 76,165 (0.762) |
| backlog-adp@blank-4 | 342 | 92,500 (0.925) | 76,179 (0.762) |
| backlog-adp@program-4 | 373 | 95,349 (0.953) | 78,491 (0.785) |
| backlog-adp@verify-4 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@blank-aged2-4 | 341 | 93,301 (0.933) | 76,107 (0.761) |
| backlog-adp@blank-aged1-4 | 339 | 92,520 (0.925) | 76,409 (0.764) |
| backlog-adp@program-aged2-4 | 369 | 95,347 (0.953) | 78,702 (0.787) |
| backlog-adp@program-aged1-4 | 368 | 95,805 (0.958) | 78,849 (0.788) |
| backlog-adp@verify-aged2-4 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@verify-aged1-4 | 399 | 94,984 (0.950) | 78,276 (0.783) |
| save | 679 | 94,255 (0.943) | 78,786 (0.788) |
| control | 79 | 22,571 (0.226) | 2,593 (0.026) |

Longest pass that carries a step: 95,805 CPU cycles (0.958 ms), backlog-adp@program-aged1-4; longest step: 78,849 (0.788 ms), backlog-adp@program-aged1-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 386,680 | 3.867 | 20 | 20 | fits | 126,561 | 193 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 302,015 | 3.020 | 20 | 200 | fits | 150,750 | 206 | 0.459 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 439,370 | 4.394 | 20 | 200 | fits | 126,561 | 193 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 302,939 | 3.029 | 20 | 20 | fits | 150,750 | 206 | 0.459 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 440,074 | 4.401 | 20 | 20 | fits | 126,561 | 193 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 155,829 | 1.558 | 20 | 24 | fits | 153,018 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 305,589 | 3.056 | 20 | 24 | fits | 150,750 | 206 | 0.459 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 305,523 | 3.055 | 20 | 50 | fits | 150,750 | 206 | 0.459 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 443,098 | 4.431 | 20 | 50 | fits | 126,561 | 193 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 527,356 | 5.274 | 20 | 20 | fits | 84,324 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,014,326 | 10.143 | 20 | 20 | fits | 59,768 | 20 | 0.683 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 417,933 | 4.179 | 20 | 20 | fits | 125,344 | 181 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 353,246 | 3.532 | 20 | 200 | fits | 149,967 | 220 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 477,974 | 4.780 | 20 | 200 | fits | 125,344 | 181 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 354,170 | 3.542 | 20 | 20 | fits | 149,967 | 220 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 478,678 | 4.787 | 20 | 20 | fits | 125,344 | 181 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 196,582 | 1.966 | 20 | 24 | fits | 153,370 | 156 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 356,820 | 3.568 | 20 | 24 | fits | 149,967 | 220 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 356,754 | 3.568 | 20 | 50 | fits | 149,967 | 220 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 481,702 | 4.817 | 20 | 50 | fits | 125,344 | 181 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 565,833 | 5.658 | 20 | 20 | fits | 84,197 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,079,249 | 10.792 | 20 | 20 | fits | 81,599 | 31 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 443,985 | 4.440 | 20 | 20 | fits | 119,642 | 184 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 377,472 | 3.775 | 20 | 200 | fits | 150,917 | 209 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 496,498 | 4.965 | 20 | 200 | fits | 119,642 | 184 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 378,396 | 3.784 | 20 | 20 | fits | 150,917 | 209 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 497,202 | 4.972 | 20 | 20 | fits | 119,642 | 184 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 231,119 | 2.311 | 20 | 24 | fits | 152,957 | 155 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 381,046 | 3.810 | 20 | 24 | fits | 150,917 | 209 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 380,980 | 3.810 | 20 | 50 | fits | 150,917 | 209 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 500,226 | 5.002 | 20 | 50 | fits | 119,642 | 184 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 584,893 | 5.849 | 20 | 20 | fits | 84,733 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,091,300 | 10.913 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 437,093 | 4.371 | 20 | 20 | fits | 113,487 | 163 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 384,287 | 3.843 | 20 | 200 | fits | 149,259 | 226 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 497,158 | 4.972 | 20 | 200 | fits | 113,487 | 163 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 385,211 | 3.852 | 20 | 20 | fits | 149,259 | 226 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 497,862 | 4.979 | 20 | 20 | fits | 113,487 | 163 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 239,592 | 2.396 | 20 | 24 | fits | 152,657 | 155 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 387,861 | 3.879 | 20 | 24 | fits | 149,259 | 226 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 387,795 | 3.878 | 20 | 50 | fits | 149,259 | 226 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 500,886 | 5.009 | 20 | 50 | fits | 113,487 | 163 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 585,503 | 5.855 | 20 | 20 | fits | 84,683 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,098,395 | 10.984 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 347,364 | 3.474 | 20 | 20 | fits | 113,040 | 164 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 294,468 | 2.945 | 20 | 200 | fits | 149,872 | 231 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 406,892 | 4.069 | 20 | 200 | fits | 113,040 | 164 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 295,392 | 2.954 | 20 | 20 | fits | 149,872 | 231 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 407,596 | 4.076 | 20 | 20 | fits | 113,040 | 164 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 149,160 | 1.492 | 20 | 24 | fits | 151,380 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 298,042 | 2.980 | 20 | 24 | fits | 149,872 | 231 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 297,976 | 2.980 | 20 | 50 | fits | 149,872 | 231 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 410,620 | 4.106 | 20 | 50 | fits | 113,040 | 164 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 510,387 | 5.104 | 20 | 20 | fits | 88,291 | 31 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,081,290 | 10.813 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 356,801 | 3.568 | 20 | 20 | fits | 113,158 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 304,251 | 3.043 | 20 | 200 | fits | 148,480 | 226 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 416,793 | 4.168 | 20 | 200 | fits | 113,158 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 305,175 | 3.052 | 20 | 20 | fits | 148,480 | 226 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 417,497 | 4.175 | 20 | 20 | fits | 113,158 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 160,335 | 1.603 | 20 | 24 | fits | 151,466 | 152 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 307,825 | 3.078 | 20 | 24 | fits | 148,480 | 226 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 307,759 | 3.078 | 20 | 50 | fits | 148,480 | 226 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 420,521 | 4.205 | 20 | 50 | fits | 113,158 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 504,506 | 5.045 | 20 | 20 | fits | 84,051 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,017,078 | 10.171 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 358,604 | 3.586 | 20 | 20 | fits | 113,121 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 298,349 | 2.983 | 20 | 200 | fits | 148,928 | 226 | 0.432 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 410,854 | 4.109 | 20 | 200 | fits | 113,121 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 299,273 | 2.993 | 20 | 20 | fits | 148,928 | 226 | 0.432 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 411,558 | 4.116 | 20 | 20 | fits | 113,121 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 153,985 | 1.540 | 20 | 24 | fits | 151,393 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 301,923 | 3.019 | 20 | 24 | fits | 148,928 | 226 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 301,857 | 3.019 | 20 | 50 | fits | 148,928 | 226 | 0.432 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 414,582 | 4.146 | 20 | 50 | fits | 113,121 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 499,081 | 4.991 | 20 | 20 | fits | 84,565 | 24 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,090,634 | 10.906 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 355,210 | 3.552 | 20 | 20 | fits | 113,069 | 163 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 294,955 | 2.950 | 20 | 200 | fits | 150,432 | 231 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 407,408 | 4.074 | 20 | 200 | fits | 113,069 | 163 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 295,879 | 2.959 | 20 | 20 | fits | 150,432 | 231 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 408,112 | 4.081 | 20 | 20 | fits | 113,069 | 163 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 149,087 | 1.491 | 20 | 24 | fits | 151,307 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 298,529 | 2.985 | 20 | 24 | fits | 150,432 | 231 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 298,463 | 2.985 | 20 | 50 | fits | 150,432 | 231 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 411,136 | 4.111 | 20 | 50 | fits | 113,069 | 163 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 495,557 | 4.956 | 20 | 20 | fits | 84,487 | 24 | 0.778 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,008,123 | 10.081 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 366,282 | 3.663 | 20 | 20 | fits | 120,582 | 184 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 313,549 | 3.135 | 20 | 200 | fits | 146,404 | 209 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 433,515 | 4.335 | 20 | 200 | fits | 120,582 | 184 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 314,473 | 3.145 | 20 | 20 | fits | 146,404 | 209 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 434,219 | 4.342 | 20 | 20 | fits | 120,582 | 184 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 160,668 | 1.607 | 20 | 24 | fits | 151,570 | 153 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 317,123 | 3.171 | 20 | 24 | fits | 146,404 | 209 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 317,057 | 3.171 | 20 | 50 | fits | 146,404 | 209 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 437,243 | 4.372 | 20 | 50 | fits | 120,582 | 184 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 514,366 | 5.144 | 20 | 20 | fits | 77,189 | 26 | 0.823 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,112,688 | 11.127 | 20 | 20 | fits | 88,263 | 29 | 0.660 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 353,775 | 3.538 | 20 | 20 | fits | 113,734 | 164 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 300,992 | 3.010 | 20 | 200 | fits | 149,001 | 226 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 414,110 | 4.141 | 20 | 200 | fits | 113,734 | 164 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 301,916 | 3.019 | 20 | 20 | fits | 149,001 | 226 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 414,814 | 4.148 | 20 | 20 | fits | 113,734 | 164 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 156,555 | 1.566 | 20 | 24 | fits | 151,480 | 152 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 304,566 | 3.046 | 20 | 24 | fits | 149,001 | 226 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 304,500 | 3.045 | 20 | 50 | fits | 149,001 | 226 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 417,838 | 4.178 | 20 | 50 | fits | 113,734 | 164 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 517,784 | 5.178 | 20 | 20 | fits | 88,351 | 31 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,011,815 | 10.118 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| LINK_UP | `adp.link_up.if0` | 2,771 | 0.028 | 20 | 200 | fits | 27,812 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,072 | 0.161 | 20 | 200 | fits | 22,379 | 23 (39) | 0.719 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,807 | 0.048 | 20 | 200 | fits | 16,437 | 16 (31) | 0.567 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
