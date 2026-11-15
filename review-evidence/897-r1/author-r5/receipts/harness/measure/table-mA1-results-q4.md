### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 23 paths and 0 of 231 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.079 (0.250) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.060 (0.227) | fits | 0 adp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.141 (0.470) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.136 (0.465) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.210 (0.541) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.171 (0.508) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.087 (0.412) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.047 (0.159) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.025 (0.257) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.087 (0.379) | fits | 0 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.049 (4.249) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.495 (5.088) | fits | 7 adp | 19 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.681 (2.087) | fits | 15 events | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.204 | fits | 0 acmp | 20 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.acmp.last.if0` (backlog-adp@program-aged2-7) | 4.994 | fits | 11 acmp | 20 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.247 | fits | 0 adp | 20 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 4.987 | fits | 7 adp | 20 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-7.service.aecp.first.if0` (backlog-adp@program-7) | 1.617 | fits | 0 aecp | 20 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.230 | fits | 15 aecp | 20 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.230 | fits | 0 maap | 20 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.024 | fits | 6 maap | 20 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 5.927 | fits | 0 srp | 20 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.srp.last.if0` (backlog-adp@program-aged2-7) | 9.996 | fits | 31 srp | 20 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-1 | 0 | 10.315 | 10 | 150,145 (1.501) | yes | - |
| backlog-adp@blank-3 | 0 | 10.253 | 10 | 150,062 (1.501) | yes | - |
| backlog-adp@blank-7 | 0 | 10.281 | 10 | 149,823 (1.498) | yes | - |
| backlog-adp@program-3 | 0 | 10.338 | 10 | 149,623 (1.496) | yes | - |
| backlog-adp@program-7 | 0 | 9.626 | 10 | 149,460 (1.495) | yes | - |
| backlog-adp@verify-3 | 0 | 10.277 | 10 | 149,393 (1.494) | yes | - |
| backlog-adp@verify-7 | 0 | 10.245 | 10 | 149,618 (1.496) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.325 | 10 | 149,094 (1.491) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.245 | 10 | 149,137 (1.491) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.476 | 13 | 148,313 (1.483) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.246 | 12 | 149,118 (1.491) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.267 | 10 | 149,036 (1.490) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.480 | 11 | 149,152 (1.492) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.340 | 10 | 149,035 (1.490) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.272 | 10 | 149,055 (1.491) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.234 | 10 | 149,118 (1.491) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.364 | 10 | 149,099 (1.491) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.301 | 10 | 149,099 (1.491) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 10.510 | 12 | 149,221 (1.492) | yes | - |
| backlog | 0 | 5.631 | 7 | 154,801 (1.548) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 154,801 CPU cycles (1.548 ms), backlog.
Over the windows that released their whole load only: 154,801 (1.548 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-1 | 406 | 0 | 150,145 (1.501) | fits |
| backlog-adp@blank-3 | 406 | 0 | 150,062 (1.501) | fits |
| backlog-adp@blank-7 | 408 | 0 | 149,823 (1.498) | fits |
| backlog-adp@program-3 | 504 | 0 | 149,623 (1.496) | fits |
| backlog-adp@program-7 | 507 | 0 | 149,460 (1.495) | fits |
| backlog-adp@verify-3 | 590 | 0 | 149,393 (1.494) | fits |
| backlog-adp@verify-7 | 592 | 0 | 149,618 (1.496) | fits |
| backlog-adp@blank-aged2-3 | 750 | 0 | 149,094 (1.491) | fits |
| backlog-adp@blank-aged2-7 | 783 | 0 | 149,137 (1.491) | fits |
| backlog-adp@blank-aged1-3 | 691 | 0 | 149,175 (1.492) | fits |
| backlog-adp@blank-aged1-7 | 723 | 0 | 149,118 (1.491) | fits |
| backlog-adp@program-aged2-3 | 844 | 0 | 149,036 (1.490) | fits |
| backlog-adp@program-aged2-7 | 879 | 0 | 149,152 (1.492) | fits |
| backlog-adp@program-aged1-3 | 778 | 0 | 149,035 (1.490) | fits |
| backlog-adp@program-aged1-7 | 811 | 0 | 149,055 (1.491) | fits |
| backlog-adp@verify-aged2-3 | 934 | 0 | 149,118 (1.491) | fits |
| backlog-adp@verify-aged2-7 | 968 | 0 | 149,099 (1.491) | fits |
| backlog-adp@verify-aged1-3 | 868 | 0 | 149,099 (1.491) | fits |
| backlog-adp@verify-aged1-7 | 903 | 0 | 149,221 (1.492) | fits |
| acmp-noresp | 2027 | 0 | 42,159 (0.422) | fits |
| backlog | 286 | 0 | 154,801 (1.548) | fits |
| acmp-disc | 938 | 0 | 42,159 (0.422) | fits |
| control | 89 | 0 | 42,159 (0.422) | fits |
| datapath-events | 119 | 0 | 42,159 (0.422) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-3 | 2 | +6.726 ms, 76,435 (0.764 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.845 (20) | 10.155 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.760 (20) | 10.240 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.793 (20) | 10.207 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.936 (20) | 10.064 |
| backlog-adp@program-aged2-3 | 2 | +6.679 ms, 80,362 (0.804 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.786 (20) | 10.214 |
| backlog-adp@program-aged2-7 | 2 | +3.148 ms, 79,818 (0.798 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.996 (20) | 10.004 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.053 (20) | 10.947 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.980 (20) | 11.020 |
| backlog-adp@verify-aged2-3 | 2 | +6.685 ms, 77,281 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.752 (20) | 10.248 |
| backlog-adp@verify-aged2-7 | 2 | +3.035 ms, 76,699 (0.767 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.884 (20) | 10.116 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.058 (20) | 10.942 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.979 (20) | 11.021 |

Least margin over the aged windows: 10.004 ms, `backlog-adp@program-aged2-7.service.srp.last.if0` at 9.996 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-1 | 299 | 90,899 (0.909) | 75,948 (0.759) |
| backlog-adp@blank-3 | 299 | 90,977 (0.910) | 76,016 (0.760) |
| backlog-adp@blank-7 | 299 | 90,584 (0.906) | 75,898 (0.759) |
| backlog-adp@program-3 | 328 | 94,759 (0.948) | 78,482 (0.785) |
| backlog-adp@program-7 | 329 | 94,759 (0.948) | 77,749 (0.777) |
| backlog-adp@verify-3 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-7 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@blank-aged2-3 | 297 | 76,435 (0.764) | 75,481 (0.755) |
| backlog-adp@blank-aged2-7 | 297 | 84,573 (0.846) | 75,395 (0.754) |
| backlog-adp@blank-aged1-3 | 297 | 90,991 (0.910) | 75,848 (0.758) |
| backlog-adp@blank-aged1-7 | 298 | 90,774 (0.908) | 76,057 (0.761) |
| backlog-adp@program-aged2-3 | 326 | 94,759 (0.948) | 78,192 (0.782) |
| backlog-adp@program-aged2-7 | 326 | 94,759 (0.948) | 77,774 (0.778) |
| backlog-adp@program-aged1-3 | 326 | 94,759 (0.948) | 78,431 (0.784) |
| backlog-adp@program-aged1-7 | 326 | 94,999 (0.950) | 78,640 (0.786) |
| backlog-adp@verify-aged2-3 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged2-7 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged1-3 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged1-7 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| acmp-noresp | 615 | 94,877 (0.949) | 77,742 (0.777) |
| backlog | 265 | 20,761 (0.208) | 1,935 (0.019) |
| acmp-disc | 305 | 94,878 (0.949) | 77,742 (0.777) |
| control | 80 | 20,719 (0.207) | 1,935 (0.019) |
| datapath-events | 70 | 20,719 (0.207) | 1,935 (0.019) |

Longest pass that carries a step: 95,201 CPU cycles (0.952 ms), backlog-adp@verify-3; longest step: 78,640 (0.786 ms), backlog-adp@program-aged1-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 342,508 | 3.425 | 20 | 20 | fits | 101,667 | 142 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 298,753 | 2.988 | 20 | 200 | fits | 147,295 | 248 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 399,804 | 3.998 | 20 | 200 | fits | 101,667 | 142 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 299,677 | 2.997 | 20 | 20 | fits | 147,295 | 248 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 400,508 | 4.005 | 20 | 20 | fits | 101,667 | 142 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 156,022 | 1.560 | 20 | 24 | fits | 150,145 | 155 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 302,327 | 3.023 | 20 | 24 | fits | 147,295 | 248 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 302,261 | 3.023 | 20 | 50 | fits | 147,295 | 248 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 403,532 | 4.035 | 20 | 50 | fits | 101,667 | 142 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 493,933 | 4.939 | 20 | 20 | fits | 90,467 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 907,663 | 9.077 | 20 | 20 | fits | 59,212 | 26 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 338,558 | 3.386 | 20 | 20 | fits | 105,755 | 161 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 291,727 | 2.917 | 20 | 200 | fits | 143,920 | 230 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 396,866 | 3.969 | 20 | 200 | fits | 105,755 | 161 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 292,651 | 2.927 | 20 | 20 | fits | 143,920 | 230 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 397,570 | 3.976 | 20 | 20 | fits | 105,755 | 161 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 152,371 | 1.524 | 20 | 24 | fits | 150,062 | 155 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 295,301 | 2.953 | 20 | 24 | fits | 143,920 | 230 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 295,235 | 2.952 | 20 | 50 | fits | 143,920 | 230 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 400,594 | 4.006 | 20 | 50 | fits | 105,755 | 161 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 493,153 | 4.932 | 20 | 20 | fits | 83,376 | 31 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 901,461 | 9.015 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 340,242 | 3.402 | 20 | 20 | fits | 112,660 | 184 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 291,607 | 2.916 | 20 | 200 | fits | 143,141 | 209 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 403,651 | 4.037 | 20 | 200 | fits | 112,660 | 184 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 292,531 | 2.925 | 20 | 20 | fits | 143,141 | 209 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 404,355 | 4.044 | 20 | 20 | fits | 112,660 | 184 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 153,030 | 1.530 | 20 | 24 | fits | 149,823 | 155 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 295,181 | 2.952 | 20 | 24 | fits | 143,141 | 209 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 295,115 | 2.951 | 20 | 50 | fits | 143,141 | 209 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 407,379 | 4.074 | 20 | 50 | fits | 112,660 | 184 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 497,649 | 4.976 | 20 | 20 | fits | 90,336 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 904,478 | 9.045 | 20 | 20 | fits | 53,046 | 20 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 340,589 | 3.406 | 20 | 20 | fits | 112,590 | 184 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 292,034 | 2.920 | 20 | 200 | fits | 143,353 | 209 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 404,008 | 4.040 | 20 | 200 | fits | 112,590 | 184 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 292,958 | 2.930 | 20 | 20 | fits | 143,353 | 209 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 404,712 | 4.047 | 20 | 20 | fits | 112,590 | 184 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 153,245 | 1.532 | 20 | 24 | fits | 149,623 | 155 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 295,608 | 2.956 | 20 | 24 | fits | 143,353 | 209 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 295,542 | 2.955 | 20 | 50 | fits | 143,353 | 209 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 407,736 | 4.077 | 20 | 50 | fits | 112,590 | 184 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 497,716 | 4.977 | 20 | 20 | fits | 90,046 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 904,975 | 9.050 | 20 | 20 | fits | 52,570 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 353,782 | 3.538 | 20 | 20 | fits | 106,887 | 164 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 305,325 | 3.053 | 20 | 200 | fits | 148,207 | 231 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 411,596 | 4.116 | 20 | 200 | fits | 106,887 | 164 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 306,249 | 3.062 | 20 | 20 | fits | 148,207 | 231 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 412,300 | 4.123 | 20 | 20 | fits | 106,887 | 164 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 161,682 | 1.617 | 20 | 24 | fits | 149,460 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 308,899 | 3.089 | 20 | 24 | fits | 148,207 | 231 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 308,833 | 3.088 | 20 | 50 | fits | 148,207 | 231 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 415,324 | 4.153 | 20 | 50 | fits | 106,887 | 164 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 507,639 | 5.076 | 20 | 20 | fits | 82,946 | 31 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 908,877 | 9.089 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 341,262 | 3.413 | 20 | 20 | fits | 101,908 | 143 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 297,587 | 2.976 | 20 | 200 | fits | 147,431 | 248 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 398,879 | 3.989 | 20 | 200 | fits | 101,908 | 143 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 298,511 | 2.985 | 20 | 20 | fits | 147,431 | 248 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 399,583 | 3.996 | 20 | 20 | fits | 101,908 | 143 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 154,720 | 1.547 | 20 | 24 | fits | 149,393 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 301,161 | 3.012 | 20 | 24 | fits | 147,431 | 248 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 301,095 | 3.011 | 20 | 50 | fits | 147,431 | 248 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 402,607 | 4.026 | 20 | 50 | fits | 101,908 | 143 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 495,061 | 4.951 | 20 | 20 | fits | 83,174 | 31 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 903,233 | 9.032 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 342,314 | 3.423 | 20 | 20 | fits | 106,068 | 163 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 293,486 | 2.935 | 20 | 200 | fits | 147,787 | 231 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 398,938 | 3.989 | 20 | 200 | fits | 106,068 | 163 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 294,410 | 2.944 | 20 | 20 | fits | 147,787 | 231 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 399,642 | 3.996 | 20 | 20 | fits | 106,068 | 163 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 150,263 | 1.503 | 20 | 24 | fits | 149,618 | 155 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 297,060 | 2.971 | 20 | 24 | fits | 147,787 | 231 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 296,994 | 2.970 | 20 | 50 | fits | 147,787 | 231 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 402,666 | 4.027 | 20 | 50 | fits | 106,068 | 163 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 492,888 | 4.929 | 20 | 20 | fits | 90,288 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 900,254 | 9.003 | 20 | 20 | fits | 52,648 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 351,876 | 3.519 | 20 | 20 | fits | 98,201 | 154 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 303,056 | 3.031 | 20 | 200 | fits | 148,945 | 233 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 400,641 | 4.006 | 20 | 200 | fits | 98,201 | 154 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 303,980 | 3.040 | 20 | 20 | fits | 148,945 | 233 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 401,345 | 4.013 | 20 | 20 | fits | 98,201 | 154 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 158,675 | 1.587 | 20 | 24 | fits | 149,094 | 152 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 306,630 | 3.066 | 20 | 24 | fits | 148,945 | 233 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 306,564 | 3.066 | 20 | 50 | fits | 148,945 | 233 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 404,369 | 4.044 | 20 | 50 | fits | 98,201 | 154 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 494,206 | 4.942 | 20 | 20 | fits | 89,903 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 984,541 | 9.845 | 20 | 20 | fits | 53,046 | 20 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 428,471 | 4.285 | 20 | 20 | fits | 116,200 | 190 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 292,047 | 2.920 | 20 | 200 | fits | 143,353 | 210 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 492,204 | 4.922 | 20 | 200 | fits | 116,200 | 190 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 292,971 | 2.930 | 20 | 20 | fits | 143,353 | 210 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 492,908 | 4.929 | 20 | 20 | fits | 116,200 | 190 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 153,258 | 1.533 | 20 | 24 | fits | 149,137 | 152 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 295,621 | 2.956 | 20 | 24 | fits | 143,353 | 210 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 295,555 | 2.956 | 20 | 50 | fits | 143,353 | 210 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 495,932 | 4.959 | 20 | 50 | fits | 116,200 | 190 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 586,197 | 5.862 | 20 | 20 | fits | 90,331 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 975,982 | 9.760 | 20 | 20 | fits | 52,532 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 346,835 | 3.468 | 20 | 20 | fits | 104,689 | 148 | 0.468 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 290,944 | 2.909 | 20 | 200 | fits | 148,313 | 254 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 404,025 | 4.040 | 20 | 200 | fits | 104,689 | 148 | 0.468 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 291,868 | 2.919 | 20 | 20 | fits | 148,313 | 254 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 404,729 | 4.047 | 20 | 20 | fits | 104,689 | 148 | 0.468 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 147,195 | 1.472 | 20 | 24 | fits | 149,175 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 294,518 | 2.945 | 20 | 24 | fits | 148,313 | 254 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 294,452 | 2.945 | 20 | 50 | fits | 148,313 | 254 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 407,753 | 4.078 | 20 | 50 | fits | 104,689 | 148 | 0.468 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 498,370 | 4.984 | 20 | 20 | fits | 90,683 | 28 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 979,255 | 9.793 | 20 | 20 | fits | 63,854 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 370,035 | 3.700 | 20 | 20 | fits | 120,900 | 196 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 299,877 | 2.999 | 20 | 200 | fits | 147,578 | 198 | 0.461 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 420,161 | 4.202 | 20 | 200 | fits | 120,900 | 196 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 300,801 | 3.008 | 20 | 20 | fits | 147,578 | 198 | 0.461 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 420,865 | 4.209 | 20 | 20 | fits | 120,900 | 196 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 156,863 | 1.569 | 20 | 24 | fits | 149,118 | 152 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 303,451 | 3.035 | 20 | 24 | fits | 147,578 | 198 | 0.461 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 303,385 | 3.034 | 20 | 50 | fits | 147,578 | 198 | 0.461 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 423,889 | 4.239 | 20 | 50 | fits | 120,900 | 196 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 549,807 | 5.498 | 20 | 20 | fits | 83,933 | 32 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 993,604 | 9.936 | 20 | 20 | fits | 63,317 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 335,037 | 3.350 | 20 | 20 | fits | 100,774 | 142 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 291,486 | 2.915 | 20 | 200 | fits | 146,959 | 248 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 391,644 | 3.916 | 20 | 200 | fits | 100,774 | 142 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 292,410 | 2.924 | 20 | 20 | fits | 146,959 | 248 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 392,348 | 3.923 | 20 | 20 | fits | 100,774 | 142 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 149,091 | 1.491 | 20 | 24 | fits | 149,036 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 295,060 | 2.951 | 20 | 24 | fits | 146,959 | 248 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 294,994 | 2.950 | 20 | 50 | fits | 146,959 | 248 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 395,372 | 3.954 | 20 | 50 | fits | 100,774 | 142 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 485,414 | 4.854 | 20 | 20 | fits | 90,108 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 978,561 | 9.786 | 20 | 20 | fits | 63,479 | 24 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 449,470 | 4.495 | 20 | 20 | fits | 109,438 | 172 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 310,017 | 3.100 | 20 | 200 | fits | 147,771 | 227 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 498,657 | 4.987 | 20 | 200 | fits | 109,438 | 172 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 310,941 | 3.109 | 20 | 20 | fits | 147,771 | 227 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 499,361 | 4.994 | 20 | 20 | fits | 109,438 | 172 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 159,139 | 1.591 | 20 | 24 | fits | 149,152 | 153 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 313,591 | 3.136 | 20 | 24 | fits | 147,771 | 227 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 313,525 | 3.135 | 20 | 50 | fits | 147,771 | 227 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 502,385 | 5.024 | 20 | 50 | fits | 109,438 | 172 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 592,735 | 5.927 | 20 | 20 | fits | 90,416 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 999,565 | 9.996 | 20 | 20 | fits | 58,238 | 27 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 341,615 | 3.416 | 20 | 20 | fits | 100,748 | 142 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 298,064 | 2.981 | 20 | 200 | fits | 146,982 | 248 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 398,196 | 3.982 | 20 | 200 | fits | 100,748 | 142 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 298,988 | 2.990 | 20 | 20 | fits | 146,982 | 248 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 398,900 | 3.989 | 20 | 20 | fits | 100,748 | 142 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 155,646 | 1.556 | 20 | 24 | fits | 149,035 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 301,638 | 3.016 | 20 | 24 | fits | 146,982 | 248 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 301,572 | 3.016 | 20 | 50 | fits | 146,982 | 248 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 401,924 | 4.019 | 20 | 50 | fits | 100,748 | 142 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 491,966 | 4.920 | 20 | 20 | fits | 90,108 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 905,329 | 9.053 | 20 | 20 | fits | 57,877 | 27 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 362,793 | 3.628 | 20 | 20 | fits | 115,643 | 190 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 289,615 | 2.896 | 20 | 200 | fits | 143,416 | 210 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 413,817 | 4.138 | 20 | 200 | fits | 115,643 | 190 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 290,539 | 2.905 | 20 | 20 | fits | 143,416 | 210 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 414,521 | 4.145 | 20 | 20 | fits | 115,643 | 190 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 150,763 | 1.508 | 20 | 24 | fits | 149,055 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 293,189 | 2.932 | 20 | 24 | fits | 143,416 | 210 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 293,123 | 2.931 | 20 | 50 | fits | 143,416 | 210 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 417,545 | 4.175 | 20 | 50 | fits | 115,643 | 190 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 507,934 | 5.079 | 20 | 20 | fits | 90,455 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 898,015 | 8.980 | 20 | 20 | fits | 52,572 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 336,838 | 3.368 | 20 | 20 | fits | 101,033 | 143 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 293,287 | 2.933 | 20 | 200 | fits | 147,039 | 248 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 393,704 | 3.937 | 20 | 200 | fits | 101,033 | 143 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 294,211 | 2.942 | 20 | 20 | fits | 147,039 | 248 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 394,408 | 3.944 | 20 | 20 | fits | 101,033 | 143 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 150,812 | 1.508 | 20 | 24 | fits | 149,118 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 296,861 | 2.969 | 20 | 24 | fits | 147,039 | 248 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 296,795 | 2.968 | 20 | 50 | fits | 147,039 | 248 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 397,432 | 3.974 | 20 | 50 | fits | 101,033 | 143 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 489,707 | 4.897 | 20 | 20 | fits | 83,129 | 31 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 975,192 | 9.752 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 435,921 | 4.359 | 20 | 20 | fits | 111,383 | 184 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 298,794 | 2.988 | 20 | 200 | fits | 143,250 | 209 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 486,260 | 4.863 | 20 | 200 | fits | 111,383 | 184 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 299,718 | 2.997 | 20 | 20 | fits | 143,250 | 209 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 486,964 | 4.870 | 20 | 20 | fits | 111,383 | 184 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 160,108 | 1.601 | 20 | 24 | fits | 149,099 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 302,368 | 3.024 | 20 | 24 | fits | 143,250 | 209 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 302,302 | 3.023 | 20 | 50 | fits | 143,250 | 209 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 489,988 | 4.900 | 20 | 50 | fits | 111,383 | 184 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 580,169 | 5.802 | 20 | 20 | fits | 90,247 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 988,391 | 9.884 | 20 | 20 | fits | 52,578 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 343,178 | 3.432 | 20 | 20 | fits | 100,774 | 142 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 299,627 | 2.996 | 20 | 200 | fits | 147,016 | 248 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 399,785 | 3.998 | 20 | 200 | fits | 100,774 | 142 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 300,551 | 3.006 | 20 | 20 | fits | 147,016 | 248 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 400,489 | 4.005 | 20 | 20 | fits | 100,774 | 142 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 157,175 | 1.572 | 20 | 24 | fits | 149,099 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 303,201 | 3.032 | 20 | 24 | fits | 147,016 | 248 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 303,135 | 3.031 | 20 | 50 | fits | 147,016 | 248 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 403,513 | 4.035 | 20 | 50 | fits | 100,774 | 142 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 493,661 | 4.937 | 20 | 20 | fits | 90,214 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 905,760 | 9.058 | 20 | 20 | fits | 63,418 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 362,757 | 3.628 | 20 | 20 | fits | 114,655 | 190 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 299,278 | 2.993 | 20 | 200 | fits | 143,940 | 209 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 413,317 | 4.133 | 20 | 200 | fits | 114,655 | 190 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 300,202 | 3.002 | 20 | 20 | fits | 143,940 | 209 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 414,021 | 4.140 | 20 | 20 | fits | 114,655 | 190 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 152,231 | 1.522 | 20 | 24 | fits | 149,221 | 153 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 302,852 | 3.029 | 20 | 24 | fits | 143,940 | 209 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 302,786 | 3.028 | 20 | 50 | fits | 143,940 | 209 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 417,045 | 4.170 | 20 | 50 | fits | 114,655 | 190 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 507,556 | 5.076 | 20 | 20 | fits | 90,577 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 897,891 | 8.979 | 20 | 20 | fits | 52,826 | 21 | 0.659 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 20,975 | 0.210 | 20 | 20 | fits | 27,652 | 21 (35) | 0.816 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 17,114 | 0.171 | 20 | 20 | fits | 24,440 | 17 (14) | 0.854 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 8,716 | 0.087 | 20 | 20 | fits | 23,863 | 18 (14) | 0.847 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 14,084 | 0.141 | 20 | 20 | fits | 28,013 | 21 (35) | 0.822 |
| an event behind 15 others | `backlog.event.if0` | 168,106 | 1.681 | 20 | 200 | fits | 53,880 | 78 | 0.543 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 404,882 | 4.049 | 20 | 20 | fits | 149,565 | 168 | 0.401 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 424,711 | 4.247 | 20 | 200 | fits | 149,565 | 168 | 0.401 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 424,095 | 4.241 | 20 | 200 | fits | 149,565 | 168 | 0.401 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 420,389 | 4.204 | 20 | 20 | fits | 149,565 | 168 | 0.401 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 419,553 | 4.196 | 20 | 20 | fits | 149,565 | 168 | 0.401 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 153,910 | 1.539 | 20 | 24 | fits | 154,801 | 158 | 0.391 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 423,039 | 4.230 | 20 | 24 | fits | 149,565 | 168 | 0.401 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 422,973 | 4.230 | 20 | 50 | fits | 149,565 | 168 | 0.401 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 422,577 | 4.226 | 20 | 50 | fits | 149,565 | 168 | 0.401 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 455,244 | 4.552 | 20 | 20 | fits | 32,733 | 56 | 0.194 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 516,637 | 5.166 | 20 | 20 | fits | 25,493 | 41 | 0.154 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,998 | 0.060 | 20 | 20 | fits | 22,712 | 13 (29) | 0.795 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,913 | 0.079 | 20 | 20 | fits | 24,959 | 19 (35) | 0.804 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 13,609 | 0.136 | 20 | 20 | fits | 27,598 | 21 (12) | 0.814 |
| LINK_UP | `adp.link_up.if0` | 2,501 | 0.025 | 20 | 200 | fits | 25,663 | 43 (11) | 0.728 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,715 | 0.087 | 20 | 200 | fits | 21,370 | 23 (39) | 0.723 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,683 | 0.047 | 20 | 200 | fits | 15,869 | 16 (31) | 0.667 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
