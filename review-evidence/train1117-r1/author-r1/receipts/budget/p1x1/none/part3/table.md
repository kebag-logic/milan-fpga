### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 23 paths and 0 of 111 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.028 (0.278) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.084 (0.250) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.161 (0.483) | fits | 0 events | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.945 (3.253) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.398 (0.688) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.579 (0.892) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.426 (0.744) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.448 (0.726) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.488 (0.824) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.267 (3.583) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.458 (0.737) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-0.adp_available.if0` (backlog-adp@program-0) | 4.208 (5.764) | fits | 7 adp | 8 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.072 (0.268) | fits | 0 adp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-0.service.acmp.first.if0` (backlog-adp@program-0) | 3.606 | fits | 0 acmp | 9 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-0.service.acmp.last.if0` (backlog-adp@program-0) | 4.821 | fits | 11 acmp | 9 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-0.service.adp.first.if0` (backlog-adp@program-0) | 3.597 | fits | 0 adp | 9 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-0.service.adp.last.if0` (backlog-adp@program-0) | 4.814 | fits | 7 adp | 9 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-0.service.aecp.first.if0` (backlog-adp@program-0) | 2.158 | fits | 0 aecp | 9 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@program-0.service.aecp.last.if0` (backlog-adp@program-0) | 3.633 | fits | 15 aecp | 9 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-0.service.maap.first.if0` (backlog-adp@program-0) | 3.632 | fits | 0 maap | 9 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-0.service.maap.last.if0` (backlog-adp@program-0) | 4.851 | fits | 6 maap | 9 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-0.service.srp.first.if0` (backlog-adp@program-0) | 5.691 | fits | 0 srp | 9 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-0.service.srp.last.if0` (backlog-adp@program-0) | 10.761 | fits | 31 srp | 9 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-0 | 0 | 12.181 | 11 | 152,870 (1.529) | yes | - |
| backlog-adp@verify-0 | 0 | 13.362 | 11 | 152,657 (1.527) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.918 | 12 | 151,805 (1.518) | yes | - |
| backlog-adp@blank-aged1-0 | 1 | 14.075 | 12 | 150,073 (1.501) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 12.730 | 13 | 151,321 (1.513) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 12.324 | 11 | 151,252 (1.513) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.789 | 11 | 151,369 (1.514) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 13.128 | 12 | 151,802 (1.518) | yes | - |
| backlog-adp-refill | 0 | 40.744 | 25 | 151,773 (1.518) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-owed not run): 151,773 CPU cycles (1.518 ms), backlog-adp-refill.
Over the windows that released their whole load only: 151,773 (1.518 ms), backlog-adp-refill.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 46391 | 0 | 51,886 (0.519) | fits |
| backlog-adp@program-0 | 493 | 0 | 152,870 (1.529) | fits |
| backlog-adp@verify-0 | 499 | 0 | 152,657 (1.527) | fits |
| backlog-adp@blank-aged2-0 | 743 | 0 | 151,805 (1.518) | fits |
| backlog-adp@blank-aged1-0 | 683 | 0 | 151,394 (1.514) | fits |
| backlog-adp@program-aged2-0 | 772 | 0 | 151,321 (1.513) | fits |
| backlog-adp@program-aged1-0 | 709 | 0 | 151,252 (1.513) | fits |
| backlog-adp@verify-aged2-0 | 786 | 0 | 151,369 (1.514) | fits |
| backlog-adp@verify-aged1-0 | 727 | 0 | 151,802 (1.518) | fits |
| adp-advertise | 598 | 0 | 30,398 (0.304) | fits |
| backlog-adp-refill | 329 | 0 | 151,773 (1.518) | fits |
| aecp-fanout | 113 | 0 | 62,847 (0.628) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.307 ms, 77,001 (0.770 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 10.269 (20) | 9.731 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.068 (20) | 9.932 |
| backlog-adp@program-aged2-0 | 2 | none | +10.208 ms, 80,430 (0.804 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 10.171 (20) | 9.829 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.165 (20) | 9.835 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.152 ms, 77,604 (0.776 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 10.114 (20) | 9.886 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.325 (20) | 9.675 |

Least margin over the aged windows: 9.675 ms, `backlog-adp@verify-aged1-0.service.srp.last.if0` at 10.325 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.416 | 6,070 | 102 | 2 | 30.898 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 520 | 80,178 (0.802) | 78,146 (0.781) |
| backlog-adp@program-0 | 371 | 95,469 (0.955) | 78,491 (0.785) |
| backlog-adp@verify-0 | 397 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@blank-aged2-0 | 339 | 93,540 (0.935) | 75,933 (0.759) |
| backlog-adp@blank-aged1-0 | 340 | 93,226 (0.932) | 76,395 (0.764) |
| backlog-adp@program-aged2-0 | 369 | 95,100 (0.951) | 78,517 (0.785) |
| backlog-adp@program-aged1-0 | 368 | 96,080 (0.961) | 78,849 (0.788) |
| backlog-adp@verify-aged2-0 | 397 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@verify-aged1-0 | 397 | 94,984 (0.950) | 78,276 (0.783) |
| adp-advertise | 577 | 22,571 (0.226) | 2,593 (0.026) |
| backlog-adp-refill | 274 | 22,571 (0.226) | 2,593 (0.026) |
| aecp-fanout | 80 | 22,571 (0.226) | 2,593 (0.026) |

Longest pass that carries a step: 96,080 CPU cycles (0.961 ms), backlog-adp@program-aged1-0; longest step: 78,849 (0.788 ms), backlog-adp@program-aged1-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 420,828 | 4.208 | 20 | 20 | fits | 122,313 | 169 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 359,682 | 3.597 | 20 | 200 | fits | 148,441 | 226 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 481,379 | 4.814 | 20 | 200 | fits | 122,313 | 169 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 360,606 | 3.606 | 20 | 20 | fits | 148,441 | 226 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 482,083 | 4.821 | 20 | 20 | fits | 122,313 | 169 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 215,805 | 2.158 | 20 | 24 | fits | 152,870 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 363,256 | 3.633 | 20 | 24 | fits | 148,441 | 226 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 363,190 | 3.632 | 20 | 50 | fits | 148,441 | 226 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 485,107 | 4.851 | 20 | 50 | fits | 122,313 | 169 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 569,138 | 5.691 | 20 | 20 | fits | 84,097 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,076,091 | 10.761 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 395,372 | 3.954 | 20 | 20 | fits | 113,211 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 342,799 | 3.428 | 20 | 200 | fits | 148,682 | 226 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 455,394 | 4.554 | 20 | 200 | fits | 113,211 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 343,723 | 3.437 | 20 | 20 | fits | 148,682 | 226 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 456,098 | 4.561 | 20 | 20 | fits | 113,211 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 198,681 | 1.987 | 20 | 24 | fits | 152,657 | 155 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 346,373 | 3.464 | 20 | 24 | fits | 148,682 | 226 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 346,307 | 3.463 | 20 | 50 | fits | 148,682 | 226 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 459,122 | 4.591 | 20 | 50 | fits | 113,211 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 543,416 | 5.434 | 20 | 20 | fits | 84,360 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,056,198 | 10.562 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 368,744 | 3.687 | 20 | 20 | fits | 113,391 | 163 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 316,054 | 3.161 | 20 | 200 | fits | 151,523 | 231 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 428,829 | 4.288 | 20 | 200 | fits | 113,391 | 163 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 316,978 | 3.170 | 20 | 20 | fits | 151,523 | 231 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 429,533 | 4.295 | 20 | 20 | fits | 113,391 | 163 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 158,215 | 1.582 | 20 | 24 | fits | 151,805 | 153 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 319,628 | 3.196 | 20 | 24 | fits | 151,523 | 231 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 319,562 | 3.196 | 20 | 50 | fits | 151,523 | 231 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 432,557 | 4.326 | 20 | 50 | fits | 113,391 | 163 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 516,756 | 5.168 | 20 | 20 | fits | 84,265 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,026,947 | 10.269 | 20 | 20 | fits | 70,580 | 33 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 363,797 | 3.638 | 20 | 20 | fits | 119,798 | 169 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 294,683 | 2.947 | 20 | 200 | fits | 150,073 | 232 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 425,253 | 4.253 | 20 | 200 | fits | 119,798 | 169 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 295,607 | 2.956 | 20 | 20 | fits | 150,073 | 232 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 425,957 | 4.260 | 20 | 20 | fits | 119,798 | 169 | 0.474 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 149,174 | 1.492 | 20 | 24 | fits | 151,394 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 298,257 | 2.983 | 20 | 24 | fits | 150,073 | 232 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 298,191 | 2.982 | 20 | 50 | fits | 150,073 | 232 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 428,981 | 4.290 | 20 | 50 | fits | 119,798 | 169 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 513,128 | 5.131 | 20 | 20 | fits | 84,213 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,006,845 | 10.068 | 20 | 20 | fits | 66,711 | 26 | 0.737 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 382,215 | 3.822 | 20 | 20 | fits | 120,293 | 173 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 303,845 | 3.038 | 20 | 200 | fits | 148,047 | 223 | 0.439 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 435,028 | 4.350 | 20 | 200 | fits | 120,293 | 173 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 304,769 | 3.048 | 20 | 20 | fits | 148,047 | 223 | 0.439 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 435,732 | 4.357 | 20 | 20 | fits | 120,293 | 173 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 160,362 | 1.604 | 20 | 24 | fits | 151,321 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 307,419 | 3.074 | 20 | 24 | fits | 148,047 | 223 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 307,353 | 3.074 | 20 | 50 | fits | 148,047 | 223 | 0.439 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 438,756 | 4.388 | 20 | 50 | fits | 120,293 | 173 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 523,087 | 5.231 | 20 | 20 | fits | 84,397 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,017,065 | 10.171 | 20 | 20 | fits | 66,648 | 26 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 364,636 | 3.646 | 20 | 20 | fits | 113,190 | 166 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 303,221 | 3.032 | 20 | 200 | fits | 147,737 | 222 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 415,795 | 4.158 | 20 | 200 | fits | 113,190 | 166 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 304,145 | 3.041 | 20 | 20 | fits | 147,737 | 222 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 416,499 | 4.165 | 20 | 20 | fits | 113,190 | 166 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 160,048 | 1.600 | 20 | 24 | fits | 151,252 | 152 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 306,795 | 3.068 | 20 | 24 | fits | 147,737 | 222 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 306,729 | 3.067 | 20 | 50 | fits | 147,737 | 222 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 419,523 | 4.195 | 20 | 50 | fits | 113,190 | 166 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 504,179 | 5.042 | 20 | 20 | fits | 84,722 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,016,503 | 10.165 | 20 | 20 | fits | 79,218 | 30 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 350,862 | 3.509 | 20 | 20 | fits | 113,104 | 163 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 298,312 | 2.983 | 20 | 200 | fits | 148,484 | 226 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 410,800 | 4.108 | 20 | 200 | fits | 113,104 | 163 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 299,236 | 2.992 | 20 | 20 | fits | 148,484 | 226 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 411,504 | 4.115 | 20 | 20 | fits | 113,104 | 163 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 154,392 | 1.544 | 20 | 24 | fits | 151,369 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 301,886 | 3.019 | 20 | 24 | fits | 148,484 | 226 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 301,820 | 3.018 | 20 | 50 | fits | 148,484 | 226 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 414,528 | 4.145 | 20 | 50 | fits | 113,104 | 163 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 498,822 | 4.988 | 20 | 20 | fits | 84,360 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,011,411 | 10.114 | 20 | 20 | fits | 79,022 | 30 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 381,370 | 3.814 | 20 | 20 | fits | 119,874 | 184 | 0.414 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 314,650 | 3.147 | 20 | 200 | fits | 146,191 | 209 | 0.451 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 433,908 | 4.339 | 20 | 200 | fits | 119,874 | 184 | 0.414 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 315,574 | 3.156 | 20 | 20 | fits | 146,191 | 209 | 0.451 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 434,612 | 4.346 | 20 | 20 | fits | 119,874 | 184 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 162,055 | 1.621 | 20 | 24 | fits | 151,802 | 153 | 0.424 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 318,224 | 3.182 | 20 | 24 | fits | 146,191 | 209 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 318,158 | 3.182 | 20 | 50 | fits | 146,191 | 209 | 0.451 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 437,636 | 4.376 | 20 | 50 | fits | 119,874 | 184 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 522,162 | 5.222 | 20 | 20 | fits | 84,592 | 24 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,032,504 | 10.325 | 20 | 20 | fits | 70,654 | 33 | 0.750 |
| LINK_UP | `adp.link_up.if0` | 2,771 | 0.028 | 20 | 200 | fits | 27,812 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,072 | 0.161 | 20 | 200 | fits | 22,379 | 23 (39) | 0.719 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 8,407 | 0.084 | 20 | 200 | fits | 2,855 | 10 (11) | 0.613 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 7,210 | 0.072 | 20 | 20 | fits | 26,844 | 19 | 0.784 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 295,152 | 2.952 | 20 | 200 | fits | 148,129 | 223 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 25,736 | 0.257 | 20 | 200 | fits | 26,844 | 19 | 0.784 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 296,076 | 2.961 | 20 | 20 | fits | 148,129 | 223 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 416,506 | 4.165 | 20 | 20 | fits | 109,930 | 163 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 151,587 | 1.516 | 20 | 24 | fits | 151,773 | 155 | 0.422 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 298,726 | 2.987 | 20 | 24 | fits | 148,129 | 223 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 298,660 | 2.987 | 20 | 50 | fits | 148,129 | 223 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 419,530 | 4.195 | 20 | 50 | fits | 109,930 | 163 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 503,276 | 5.033 | 20 | 20 | fits | 83,812 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 997,318 | 9.973 | 20 | 20 | fits | 72,980 | 24 | 0.639 |
| set_name | `aecp_fanout.set_name.if0` | 48,796 | 0.488 | 20 | 24 | fits | 60,633 | 89 | 0.586 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 42,573 | 0.426 | 20 | 24 | fits | 51,371 | 78 | 0.596 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 44,758 | 0.448 | 20 | 24 | fits | 46,174 | 79 | 0.545 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 38,795 | 0.388 | 20 | 24 | fits | 44,763 | 78 | 0.531 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 57,947 | 0.579 | 20 | 24 | fits | 62,847 | 110 | 0.592 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 294,492 | 2.945 | 20 | 24 | fits | 61,043 | 109 | 0.588 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 326,735 | 3.267 | 20 | 24 | fits | 49,757 | 67 | 0.583 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 39,777 | 0.398 | 20 | 24 | fits | 45,823 | 78 | 0.541 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,761 | 0.458 | 20 | 24 | fits | 46,065 | 79 | 0.541 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
