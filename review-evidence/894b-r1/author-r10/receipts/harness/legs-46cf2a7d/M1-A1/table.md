### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 22 paths and 0 of 100 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.174) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.027 (0.267) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.106 (0.440) | fits | 0 events | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.446 (2.770) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.532 (0.836) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.482 (0.807) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.575 (0.948) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.540 (0.842) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.649 (0.989) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.359 (3.690) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.423 (0.717) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-4.adp_available.if0` (backlog-adp@program-4) | 3.594 (5.108) | fits | 7 adp | 8 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-4.service.acmp.first.if0` (backlog-adp@blank-aged1-4) | 3.071 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-4.service.acmp.last.if0` (backlog-adp@program-4) | 4.167 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-4.service.adp.first.if0` (backlog-adp@blank-aged1-4) | 3.062 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-4.service.adp.last.if0` (backlog-adp@program-4) | 4.160 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-4.service.aecp.first.if0` (backlog-adp@program-4) | 1.613 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-4.service.aecp.last.if0` (backlog-adp@blank-aged1-4) | 3.098 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-4.service.maap.first.if0` (backlog-adp@blank-aged1-4) | 3.097 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-4.service.maap.last.if0` (backlog-adp@program-4) | 4.197 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-4.service.srp.first.if0` (backlog-adp@program-4) | 5.033 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-4.service.srp.last.if0` (backlog-adp@verify-aged2-4) | 10.823 | fits | 31 srp | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-4 | 0 | 10.523 | 11 | 152,567 (1.526) | yes | - |
| backlog-adp@verify-4 | 0 | 11.306 | 12 | 152,988 (1.530) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.262 | 11 | 151,895 (1.519) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.978 | 13 | 152,235 (1.522) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.210 | 11 | 152,316 (1.523) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.265 | 11 | 152,316 (1.523) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.354 | 12 | 152,655 (1.527) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.216 | 11 | 152,485 (1.525) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 44852 | 0 | 50,548 (0.505) | fits |
| backlog-adp@program-4 | 522 | 0 | 152,567 (1.526) | fits |
| backlog-adp@verify-4 | 615 | 0 | 152,988 (1.530) | fits |
| backlog-adp@blank-aged2-4 | 725 | 0 | 151,895 (1.519) | fits |
| backlog-adp@blank-aged1-4 | 671 | 0 | 152,235 (1.522) | fits |
| backlog-adp@program-aged2-4 | 825 | 0 | 152,316 (1.523) | fits |
| backlog-adp@program-aged1-4 | 767 | 0 | 152,316 (1.523) | fits |
| backlog-adp@verify-aged2-4 | 923 | 0 | 152,655 (1.527) | fits |
| backlog-adp@verify-aged1-4 | 864 | 0 | 152,485 (1.525) | fits |
| save | 610 | 0 | 45,408 (0.454) | fits |
| adp-gm | 88 | 0 | 30,145 (0.301) | fits |
| aecp-fanout | 112 | 0 | 67,721 (0.677) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-4 | 2 | none | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.729 (20) | 9.271 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.687 (20) | 9.313 |
| backlog-adp@program-aged2-4 | 2 | +5.761 ms, 80,912 (0.809 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.677 (20) | 9.323 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.926 (20) | 10.074 |
| backlog-adp@verify-aged2-4 | 2 | +5.785 ms, 77,579 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.823 (20) | 9.177 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.920 (20) | 10.080 |

Least margin over the aged windows: 9.177 ms, `backlog-adp@verify-aged2-4.service.srp.last.if0` at 10.823 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.392 | 6,070 | 102 | 2 | 30.865 | yes | within |
| save | 2019.743 | 4,070 | 102 | - | 10.938 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 520 | 79,958 (0.800) | 77,725 (0.777) |
| backlog-adp@program-4 | 329 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-4 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@blank-aged2-4 | 297 | 86,002 (0.860) | 76,128 (0.761) |
| backlog-adp@blank-aged1-4 | 297 | 92,933 (0.929) | 76,289 (0.763) |
| backlog-adp@program-aged2-4 | 326 | 96,381 (0.964) | 78,723 (0.787) |
| backlog-adp@program-aged1-4 | 326 | 96,758 (0.968) | 79,007 (0.790) |
| backlog-adp@verify-aged2-4 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-aged1-4 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| save | 585 | 95,336 (0.953) | 77,985 (0.780) |
| adp-gm | 79 | 22,142 (0.221) | 2,242 (0.022) |
| aecp-fanout | 80 | 24,344 (0.243) | 4,305 (0.043) |

Longest pass that carries a step: 96,758 CPU cycles (0.968 ms), backlog-adp@program-aged1-4; longest step: 79,007 (0.790 ms), backlog-adp@program-aged1-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 359,350 | 3.594 | 20 | 20 | fits | 103,113 | 149 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 304,967 | 3.050 | 20 | 200 | fits | 148,249 | 249 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 415,976 | 4.160 | 20 | 200 | fits | 103,113 | 149 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 305,891 | 3.059 | 20 | 20 | fits | 148,249 | 249 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 416,680 | 4.167 | 20 | 20 | fits | 103,113 | 149 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 161,282 | 1.613 | 20 | 24 | fits | 152,567 | 155 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 308,541 | 3.085 | 20 | 24 | fits | 148,249 | 249 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 308,475 | 3.085 | 20 | 50 | fits | 148,249 | 249 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 419,704 | 4.197 | 20 | 50 | fits | 103,113 | 149 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 503,294 | 5.033 | 20 | 20 | fits | 83,656 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 994,195 | 9.942 | 20 | 20 | fits | 66,146 | 26 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 337,137 | 3.371 | 20 | 20 | fits | 104,358 | 160 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 302,971 | 3.030 | 20 | 200 | fits | 146,535 | 235 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 406,713 | 4.067 | 20 | 200 | fits | 104,358 | 160 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 303,895 | 3.039 | 20 | 20 | fits | 146,535 | 235 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 407,417 | 4.074 | 20 | 20 | fits | 104,358 | 160 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 153,071 | 1.531 | 20 | 24 | fits | 152,988 | 156 | 0.396 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 306,545 | 3.065 | 20 | 24 | fits | 146,535 | 235 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 306,479 | 3.065 | 20 | 50 | fits | 146,535 | 235 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 410,441 | 4.104 | 20 | 50 | fits | 104,358 | 160 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 499,702 | 4.997 | 20 | 20 | fits | 89,327 | 30 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,001,102 | 10.011 | 20 | 20 | fits | 65,218 | 27 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 346,580 | 3.466 | 20 | 20 | fits | 99,917 | 142 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 303,651 | 3.037 | 20 | 200 | fits | 147,694 | 248 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 402,952 | 4.030 | 20 | 200 | fits | 99,917 | 142 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 304,575 | 3.046 | 20 | 20 | fits | 147,694 | 248 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 403,656 | 4.037 | 20 | 20 | fits | 99,917 | 142 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 160,521 | 1.605 | 20 | 24 | fits | 151,895 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 307,225 | 3.072 | 20 | 24 | fits | 147,694 | 248 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 307,159 | 3.072 | 20 | 50 | fits | 147,694 | 248 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 406,680 | 4.067 | 20 | 50 | fits | 99,917 | 142 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 490,438 | 4.904 | 20 | 20 | fits | 83,824 | 24 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,072,940 | 10.729 | 20 | 20 | fits | 85,227 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 352,297 | 3.523 | 20 | 20 | fits | 96,558 | 151 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 306,196 | 3.062 | 20 | 200 | fits | 150,643 | 237 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 402,138 | 4.021 | 20 | 200 | fits | 96,558 | 151 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 307,120 | 3.071 | 20 | 20 | fits | 150,643 | 237 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 402,842 | 4.028 | 20 | 20 | fits | 96,558 | 151 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 160,117 | 1.601 | 20 | 24 | fits | 152,235 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 309,770 | 3.098 | 20 | 24 | fits | 150,643 | 237 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 309,704 | 3.097 | 20 | 50 | fits | 150,643 | 237 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 405,866 | 4.059 | 20 | 50 | fits | 96,558 | 151 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 490,250 | 4.902 | 20 | 20 | fits | 84,450 | 24 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,068,727 | 10.687 | 20 | 20 | fits | 85,174 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 345,540 | 3.455 | 20 | 20 | fits | 96,932 | 152 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 299,459 | 2.995 | 20 | 200 | fits | 150,734 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 395,775 | 3.958 | 20 | 200 | fits | 96,932 | 152 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 300,383 | 3.004 | 20 | 20 | fits | 150,734 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 396,479 | 3.965 | 20 | 20 | fits | 96,932 | 152 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 153,289 | 1.533 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 303,033 | 3.030 | 20 | 24 | fits | 150,734 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 302,967 | 3.030 | 20 | 50 | fits | 150,734 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 399,503 | 3.995 | 20 | 50 | fits | 96,932 | 152 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 494,867 | 4.949 | 20 | 20 | fits | 86,675 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,067,737 | 10.677 | 20 | 20 | fits | 72,767 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 341,818 | 3.418 | 20 | 20 | fits | 100,328 | 142 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 298,691 | 2.987 | 20 | 200 | fits | 148,063 | 248 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 398,403 | 3.984 | 20 | 200 | fits | 100,328 | 142 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 299,615 | 2.996 | 20 | 20 | fits | 148,063 | 248 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 399,107 | 3.991 | 20 | 20 | fits | 100,328 | 142 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 155,192 | 1.552 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 302,265 | 3.023 | 20 | 24 | fits | 148,063 | 248 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 302,199 | 3.022 | 20 | 50 | fits | 148,063 | 248 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 402,131 | 4.021 | 20 | 50 | fits | 100,328 | 142 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 486,085 | 4.861 | 20 | 20 | fits | 84,020 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 992,608 | 9.926 | 20 | 20 | fits | 85,283 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 339,718 | 3.397 | 20 | 20 | fits | 104,338 | 160 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 305,552 | 3.056 | 20 | 200 | fits | 146,459 | 235 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 409,274 | 4.093 | 20 | 200 | fits | 104,338 | 160 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 306,476 | 3.065 | 20 | 20 | fits | 146,459 | 235 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 409,978 | 4.100 | 20 | 20 | fits | 104,338 | 160 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 155,786 | 1.558 | 20 | 24 | fits | 152,655 | 153 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 309,126 | 3.091 | 20 | 24 | fits | 146,459 | 235 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 309,060 | 3.091 | 20 | 50 | fits | 146,459 | 235 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 413,002 | 4.130 | 20 | 50 | fits | 104,338 | 160 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 497,223 | 4.972 | 20 | 20 | fits | 84,287 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,082,278 | 10.823 | 20 | 20 | fits | 77,498 | 31 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 344,876 | 3.449 | 20 | 20 | fits | 99,448 | 143 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 302,354 | 3.024 | 20 | 200 | fits | 147,858 | 248 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 401,186 | 4.012 | 20 | 200 | fits | 99,448 | 143 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 303,278 | 3.033 | 20 | 20 | fits | 147,858 | 248 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 401,890 | 4.019 | 20 | 20 | fits | 99,448 | 143 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 159,060 | 1.591 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 305,928 | 3.059 | 20 | 24 | fits | 147,858 | 248 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 305,862 | 3.059 | 20 | 50 | fits | 147,858 | 248 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 404,914 | 4.049 | 20 | 50 | fits | 99,448 | 143 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 500,482 | 5.005 | 20 | 20 | fits | 86,873 | 31 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 991,971 | 9.920 | 20 | 20 | fits | 72,767 | 24 | 0.653 |
| LINK_UP | `adp.link_up.if0` | 2,674 | 0.027 | 20 | 200 | fits | 26,711 | 43 (11) | 0.737 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,642 | 0.106 | 20 | 200 | fits | 23,487 | 23 (39) | 0.762 |
| GM_CHANGE | `adp.gm_change.if0` | 2,419 | 0.024 | 20 | 200 | fits | 17,371 | 17 (11) | 0.753 |
| set_name | `aecp_fanout.set_name.if0` | 64,916 | 0.649 | 20 | 24 | fits | 67,721 | 95 | 0.594 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 57,474 | 0.575 | 20 | 24 | fits | 56,319 | 78 | 0.597 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 45,006 | 0.450 | 20 | 24 | fits | 54,847 | 79 | 0.571 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 54,008 | 0.540 | 20 | 24 | fits | 51,589 | 78 | 0.564 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 48,213 | 0.482 | 20 | 24 | fits | 60,707 | 66 | 0.632 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 244,631 | 2.446 | 20 | 24 | fits | 58,903 | 65 | 0.637 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 335,903 | 3.359 | 20 | 24 | fits | 53,298 | 67 | 0.584 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 53,154 | 0.532 | 20 | 24 | fits | 50,824 | 78 | 0.557 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 42,276 | 0.423 | 20 | 24 | fits | 51,393 | 79 | 0.562 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
