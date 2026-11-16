### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 24 paths and 7 of 213 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.203 (0.456) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.094 (0.275) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.113 (0.293) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.096 (0.274) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.105 (0.281) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.116 (0.303) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.144 (0.389) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.148 (0.431) | fits | 0 acmp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.025 (0.182) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.027 (0.307) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.174 (0.521) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged1-6.adp_available.if0` (backlog-adp@verify-aged1-6) | 3.946 (4.683) | fits | 7 adp | 17 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.127 (63.468) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.069 (64.409) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-6.service.acmp.first.if0` (backlog-adp@blank-6) | 3.069 | fits | 0 acmp | 18 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.082 | MISS ceiling | 11 acmp | 18 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-6.service.adp.first.if0` (backlog-adp@blank-6) | 3.060 | fits | 0 adp | 18 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-6.service.adp.last.if0` (backlog-adp@verify-aged1-6) | 4.562 | fits | 7 adp | 18 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-6.service.aecp.first.if0` (backlog-adp@blank-6) | 1.613 | fits | 0 aecp | 18 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.746 | MISS ceiling | 15 aecp | 18 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-6.service.maap.first.if0` (backlog-adp@blank-6) | 3.095 | fits | 0 maap | 18 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-6.service.maap.last.if0` (backlog-adp@verify-aged1-6) | 4.600 | fits | 6 maap | 18 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 6.295 | fits | 0 srp | 18 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.srp.last.if0` (backlog-adp@program-aged2-6) | 10.517 | fits | 31 srp | 18 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-6 | 0 | 11.181 | 10 | 149,286 (1.493) | yes | - |
| backlog-adp@program-2 | 0 | 11.100 | 10 | 147,351 (1.474) | yes | - |
| backlog-adp@program-6 | 0 | 10.337 | 10 | 147,899 (1.479) | yes | - |
| backlog-adp@verify-2 | 0 | 11.011 | 10 | 147,240 (1.472) | yes | - |
| backlog-adp@verify-6 | 1 | 10.990 | 9 | 148,497 (1.485) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.054 | 10 | 150,436 (1.504) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.011 | 10 | 148,586 (1.486) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.694 | 12 | 148,209 (1.482) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.986 | 10 | 148,026 (1.480) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.983 | 10 | 147,684 (1.477) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.697 | 12 | 150,164 (1.502) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.110 | 11 | 148,825 (1.488) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 11.091 | 10 | 148,151 (1.482) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.007 | 10 | 147,322 (1.473) | yes | - |
| backlog-adp@verify-aged2-6 | 1 | 11.001 | 9 | 149,001 (1.490) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.945 | 10 | 147,794 (1.478) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.709 | 12 | 149,672 (1.497) | yes | - |
| backlog-owed | 0 | 64.780 | 25 | 149,699 (1.497) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 149,699 CPU cycles (1.497 ms), backlog-owed.
Over the windows that released their whole load only: 149,699 (1.497 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 137258 | 0 | 105,005 (1.050) | fits |
| backlog-adp@blank-6 | 537 | 0 | 149,286 (1.493) | fits |
| backlog-adp@program-2 | 894 | 0 | 147,351 (1.474) | fits |
| backlog-adp@program-6 | 897 | 0 | 147,899 (1.479) | fits |
| backlog-adp@verify-2 | 1242 | 0 | 147,240 (1.472) | fits |
| backlog-adp@verify-6 | 1243 | 0 | 148,497 (1.485) | fits |
| backlog-adp@blank-aged2-2 | 826 | 0 | 150,436 (1.504) | fits |
| backlog-adp@blank-aged2-6 | 854 | 0 | 148,586 (1.486) | fits |
| backlog-adp@blank-aged1-2 | 771 | 0 | 148,209 (1.482) | fits |
| backlog-adp@blank-aged1-6 | 797 | 0 | 148,026 (1.480) | fits |
| backlog-adp@program-aged2-2 | 1177 | 0 | 147,684 (1.477) | fits |
| backlog-adp@program-aged2-6 | 1208 | 0 | 150,164 (1.502) | fits |
| backlog-adp@program-aged1-2 | 1121 | 0 | 148,825 (1.488) | fits |
| backlog-adp@program-aged1-6 | 1149 | 0 | 148,151 (1.482) | fits |
| backlog-adp@verify-aged2-2 | 1529 | 0 | 147,322 (1.473) | fits |
| backlog-adp@verify-aged2-6 | 1558 | 0 | 149,001 (1.490) | fits |
| backlog-adp@verify-aged1-2 | 1472 | 0 | 147,794 (1.478) | fits |
| backlog-adp@verify-aged1-6 | 1503 | 0 | 149,672 (1.497) | fits |
| save | 608 | 0 | 94,822 (0.948) | fits |
| backlog-owed | 308 | 0 | 149,699 (1.497) | fits |
| adp-gm | 87 | 0 | 94,822 (0.948) | fits |
| acmp-cmd | 85 | 0 | 94,822 (0.948) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-2 | 2 | +8.036 ms, 75,987 (0.760 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.483 (20) | 9.517 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.438 (20) | 9.562 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.716 (20) | 10.284 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.662 (20) | 10.338 |
| backlog-adp@program-aged2-2 | 2 | +7.959 ms, 80,626 (0.806 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.415 (20) | 9.585 |
| backlog-adp@program-aged2-6 | 2 | +4.611 ms, 80,895 (0.809 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.517 (20) | 9.483 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.612 (20) | 10.388 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.709 (20) | 10.291 |
| backlog-adp@verify-aged2-2 | 2 | +8.131 ms, 77,128 (0.771 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.437 (20) | 9.563 |
| backlog-adp@verify-aged2-6 | 2 | +4.392 ms, 77,457 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.437 (20) | 9.563 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.611 (20) | 10.389 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.717 (20) | 10.283 |

Least margin over the aged windows: 9.483 ms, `backlog-adp@program-aged2-6.service.srp.last.if0` at 10.517 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.674 | 22,870 | 382 | 2 | 32.267 | yes | within |
| save | 4817.769 | 12,470 | 382 | - | 11.370 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 81,321 (0.813) | 78,276 (0.783) |
| backlog-adp@blank-6 | 339 | 93,461 (0.935) | 75,585 (0.756) |
| backlog-adp@program-2 | 448 | 100,309 (1.003) | 78,213 (0.782) |
| backlog-adp@program-6 | 449 | 100,309 (1.003) | 77,865 (0.779) |
| backlog-adp@verify-2 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-6 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@blank-aged2-2 | 337 | 77,166 (0.772) | 75,321 (0.753) |
| backlog-adp@blank-aged2-6 | 337 | 85,007 (0.850) | 75,639 (0.756) |
| backlog-adp@blank-aged1-2 | 337 | 93,634 (0.936) | 75,532 (0.755) |
| backlog-adp@blank-aged1-6 | 337 | 93,367 (0.934) | 75,586 (0.756) |
| backlog-adp@program-aged2-2 | 446 | 100,309 (1.003) | 78,038 (0.780) |
| backlog-adp@program-aged2-6 | 446 | 100,309 (1.003) | 78,245 (0.782) |
| backlog-adp@program-aged1-2 | 446 | 100,309 (1.003) | 78,301 (0.783) |
| backlog-adp@program-aged1-6 | 446 | 100,309 (1.003) | 78,397 (0.784) |
| backlog-adp@verify-aged2-2 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged2-6 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged1-2 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged1-6 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| save | 585 | 100,117 (1.001) | 77,804 (0.778) |
| backlog-owed | 277 | 25,967 (0.260) | 2,512 (0.025) |
| adp-gm | 79 | 25,733 (0.257) | 2,512 (0.025) |
| acmp-cmd | 66 | 25,733 (0.257) | 2,512 (0.025) |

Longest pass that carries a step: 104,105 CPU cycles (1.041 ms), backlog-adp@verify-2; longest step: 78,512 (0.785 ms), backlog-adp@verify-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 381,736 | 3.817 | 20 | 20 | fits | 148,394 | 168 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 305,977 | 3.060 | 20 | 200 | fits | 149,286 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 453,755 | 4.538 | 20 | 200 | fits | 148,394 | 168 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 306,901 | 3.069 | 20 | 20 | fits | 149,286 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 454,459 | 4.545 | 20 | 20 | fits | 148,394 | 168 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 161,255 | 1.613 | 20 | 24 | fits | 146,232 | 164 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 309,551 | 3.096 | 20 | 24 | fits | 149,286 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 309,485 | 3.095 | 20 | 50 | fits | 149,286 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 457,483 | 4.575 | 20 | 50 | fits | 148,394 | 168 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 547,055 | 5.471 | 20 | 20 | fits | 89,638 | 24 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 985,666 | 9.857 | 20 | 20 | fits | 69,747 | 25 | 0.649 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 364,845 | 3.648 | 20 | 20 | fits | 138,740 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 298,339 | 2.983 | 20 | 200 | fits | 147,351 | 217 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 436,463 | 4.365 | 20 | 200 | fits | 138,740 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 299,263 | 2.993 | 20 | 20 | fits | 147,351 | 217 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 437,167 | 4.372 | 20 | 20 | fits | 138,740 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 155,552 | 1.556 | 20 | 24 | fits | 145,200 | 164 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 301,913 | 3.019 | 20 | 24 | fits | 147,351 | 217 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 301,847 | 3.018 | 20 | 50 | fits | 147,351 | 217 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 440,191 | 4.402 | 20 | 50 | fits | 138,740 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 534,720 | 5.347 | 20 | 20 | fits | 94,595 | 30 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 972,597 | 9.726 | 20 | 20 | fits | 67,885 | 24 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 373,106 | 3.731 | 20 | 20 | fits | 138,730 | 163 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 297,667 | 2.977 | 20 | 200 | fits | 147,899 | 217 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 435,781 | 4.358 | 20 | 200 | fits | 138,730 | 163 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 298,591 | 2.986 | 20 | 20 | fits | 147,899 | 217 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 436,485 | 4.365 | 20 | 20 | fits | 138,730 | 163 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 154,332 | 1.543 | 20 | 24 | fits | 145,593 | 164 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 301,241 | 3.012 | 20 | 24 | fits | 147,899 | 217 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 301,175 | 3.012 | 20 | 50 | fits | 147,899 | 217 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 439,509 | 4.395 | 20 | 50 | fits | 138,730 | 163 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 534,015 | 5.340 | 20 | 20 | fits | 94,572 | 30 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 972,034 | 9.720 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 359,487 | 3.595 | 20 | 20 | fits | 138,981 | 163 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 292,761 | 2.928 | 20 | 200 | fits | 147,240 | 217 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 431,126 | 4.311 | 20 | 200 | fits | 138,981 | 163 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 293,685 | 2.937 | 20 | 20 | fits | 147,240 | 217 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 431,830 | 4.318 | 20 | 20 | fits | 138,981 | 163 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 150,085 | 1.501 | 20 | 24 | fits | 145,311 | 164 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 296,335 | 2.963 | 20 | 24 | fits | 147,240 | 217 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 296,269 | 2.963 | 20 | 50 | fits | 147,240 | 217 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 434,854 | 4.349 | 20 | 50 | fits | 138,981 | 163 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 524,600 | 5.246 | 20 | 20 | fits | 89,812 | 25 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 967,620 | 9.676 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 373,671 | 3.737 | 20 | 20 | fits | 148,497 | 170 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 286,785 | 2.868 | 20 | 200 | fits | 146,935 | 218 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 434,666 | 4.347 | 20 | 200 | fits | 148,497 | 170 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 287,709 | 2.877 | 20 | 20 | fits | 146,935 | 218 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 435,370 | 4.354 | 20 | 20 | fits | 148,497 | 170 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 144,414 | 1.444 | 20 | 24 | fits | 146,257 | 164 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 290,359 | 2.904 | 20 | 24 | fits | 146,935 | 218 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 290,293 | 2.903 | 20 | 50 | fits | 146,935 | 218 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 438,394 | 4.384 | 20 | 50 | fits | 148,497 | 170 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 527,742 | 5.277 | 20 | 20 | fits | 89,414 | 24 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 965,661 | 9.657 | 20 | 20 | fits | 67,821 | 24 | 0.604 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 363,114 | 3.631 | 20 | 20 | fits | 150,436 | 206 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 285,012 | 2.850 | 20 | 200 | fits | 149,000 | 223 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 434,832 | 4.348 | 20 | 200 | fits | 150,436 | 206 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 285,936 | 2.859 | 20 | 20 | fits | 149,000 | 223 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 435,536 | 4.355 | 20 | 20 | fits | 150,436 | 206 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 132,771 | 1.328 | 20 | 24 | fits | 136,091 | 121 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 288,586 | 2.886 | 20 | 24 | fits | 149,000 | 223 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 288,520 | 2.885 | 20 | 50 | fits | 149,000 | 223 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 438,560 | 4.386 | 20 | 50 | fits | 150,436 | 206 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 528,442 | 5.284 | 20 | 20 | fits | 89,948 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,048,305 | 10.483 | 20 | 20 | fits | 72,790 | 31 | 0.679 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 367,161 | 3.672 | 20 | 20 | fits | 148,586 | 170 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 291,034 | 2.910 | 20 | 200 | fits | 147,554 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 439,004 | 4.390 | 20 | 200 | fits | 148,586 | 170 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 291,958 | 2.920 | 20 | 20 | fits | 147,554 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 439,708 | 4.397 | 20 | 20 | fits | 148,586 | 170 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 148,044 | 1.480 | 20 | 24 | fits | 144,249 | 161 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 294,608 | 2.946 | 20 | 24 | fits | 147,554 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 294,542 | 2.945 | 20 | 50 | fits | 147,554 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 442,732 | 4.427 | 20 | 50 | fits | 148,586 | 170 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 620,436 | 6.204 | 20 | 20 | fits | 92,763 | 31 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,043,846 | 10.438 | 20 | 20 | fits | 67,647 | 24 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 377,299 | 3.773 | 20 | 20 | fits | 142,916 | 170 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 298,893 | 2.989 | 20 | 200 | fits | 148,209 | 218 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 449,862 | 4.499 | 20 | 200 | fits | 142,916 | 170 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 299,817 | 2.998 | 20 | 20 | fits | 148,209 | 218 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 450,566 | 4.506 | 20 | 20 | fits | 142,916 | 170 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 155,248 | 1.552 | 20 | 24 | fits | 144,509 | 161 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 302,467 | 3.025 | 20 | 24 | fits | 148,209 | 218 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 302,401 | 3.024 | 20 | 50 | fits | 148,209 | 218 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 453,590 | 4.536 | 20 | 50 | fits | 142,916 | 170 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 543,593 | 5.436 | 20 | 20 | fits | 90,069 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 971,632 | 9.716 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 363,477 | 3.635 | 20 | 20 | fits | 147,800 | 169 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 287,901 | 2.879 | 20 | 200 | fits | 148,026 | 217 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 435,085 | 4.351 | 20 | 200 | fits | 147,800 | 169 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 288,825 | 2.888 | 20 | 20 | fits | 148,026 | 217 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 435,789 | 4.358 | 20 | 20 | fits | 147,800 | 169 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 144,439 | 1.444 | 20 | 24 | fits | 144,303 | 161 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 291,475 | 2.915 | 20 | 24 | fits | 148,026 | 217 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 291,409 | 2.914 | 20 | 50 | fits | 148,026 | 217 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 438,813 | 4.388 | 20 | 50 | fits | 147,800 | 169 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 528,353 | 5.284 | 20 | 20 | fits | 89,606 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 966,173 | 9.662 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 353,406 | 3.534 | 20 | 20 | fits | 138,687 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 287,419 | 2.874 | 20 | 200 | fits | 147,684 | 217 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 425,490 | 4.255 | 20 | 200 | fits | 138,687 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 288,343 | 2.883 | 20 | 20 | fits | 147,684 | 217 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 426,194 | 4.262 | 20 | 20 | fits | 138,687 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 144,299 | 1.443 | 20 | 24 | fits | 144,483 | 161 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 290,993 | 2.910 | 20 | 24 | fits | 147,684 | 217 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 290,927 | 2.909 | 20 | 50 | fits | 147,684 | 217 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 429,218 | 4.292 | 20 | 50 | fits | 138,687 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 518,145 | 5.181 | 20 | 20 | fits | 88,993 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,041,495 | 10.415 | 20 | 20 | fits | 78,564 | 28 | 0.549 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 385,092 | 3.851 | 20 | 20 | fits | 150,164 | 173 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 297,632 | 2.976 | 20 | 200 | fits | 147,663 | 218 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 455,702 | 4.557 | 20 | 200 | fits | 150,164 | 173 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 298,556 | 2.986 | 20 | 20 | fits | 147,663 | 218 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 456,406 | 4.564 | 20 | 20 | fits | 150,164 | 173 | 0.472 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 154,533 | 1.545 | 20 | 24 | fits | 144,630 | 161 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 301,206 | 3.012 | 20 | 24 | fits | 147,663 | 218 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 301,140 | 3.011 | 20 | 50 | fits | 147,663 | 218 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 459,430 | 4.594 | 20 | 50 | fits | 150,164 | 173 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 629,532 | 6.295 | 20 | 20 | fits | 89,273 | 25 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,051,657 | 10.517 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 364,109 | 3.641 | 20 | 20 | fits | 138,781 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 298,072 | 2.981 | 20 | 200 | fits | 148,825 | 222 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 436,237 | 4.362 | 20 | 200 | fits | 138,781 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 298,996 | 2.990 | 20 | 20 | fits | 148,825 | 222 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 436,941 | 4.369 | 20 | 20 | fits | 138,781 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 146,099 | 1.461 | 20 | 24 | fits | 144,763 | 162 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 301,646 | 3.016 | 20 | 24 | fits | 148,825 | 222 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 301,580 | 3.016 | 20 | 50 | fits | 148,825 | 222 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 439,965 | 4.400 | 20 | 50 | fits | 138,781 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 528,968 | 5.290 | 20 | 20 | fits | 89,069 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 961,235 | 9.612 | 20 | 20 | fits | 71,641 | 31 | 0.633 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 371,197 | 3.712 | 20 | 20 | fits | 148,151 | 170 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 295,452 | 2.955 | 20 | 200 | fits | 147,753 | 217 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 442,987 | 4.430 | 20 | 200 | fits | 148,151 | 170 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 296,376 | 2.964 | 20 | 20 | fits | 147,753 | 217 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 443,691 | 4.437 | 20 | 20 | fits | 148,151 | 170 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 152,263 | 1.523 | 20 | 24 | fits | 144,413 | 161 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 299,026 | 2.990 | 20 | 24 | fits | 147,753 | 217 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 298,960 | 2.990 | 20 | 50 | fits | 147,753 | 217 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 446,715 | 4.467 | 20 | 50 | fits | 148,151 | 170 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 547,563 | 5.476 | 20 | 20 | fits | 91,918 | 31 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 970,898 | 9.709 | 20 | 20 | fits | 67,647 | 24 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 357,898 | 3.579 | 20 | 20 | fits | 139,019 | 163 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 291,180 | 2.912 | 20 | 200 | fits | 147,322 | 217 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 429,583 | 4.296 | 20 | 200 | fits | 139,019 | 163 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 292,104 | 2.921 | 20 | 20 | fits | 147,322 | 217 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 430,287 | 4.303 | 20 | 20 | fits | 139,019 | 163 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 148,422 | 1.484 | 20 | 24 | fits | 144,249 | 161 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 294,754 | 2.948 | 20 | 24 | fits | 147,322 | 217 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 294,688 | 2.947 | 20 | 50 | fits | 147,322 | 217 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 433,311 | 4.333 | 20 | 50 | fits | 139,019 | 163 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 522,913 | 5.229 | 20 | 20 | fits | 89,668 | 25 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,043,687 | 10.437 | 20 | 20 | fits | 67,454 | 24 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 372,005 | 3.720 | 20 | 20 | fits | 149,001 | 171 | 0.467 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 285,475 | 2.855 | 20 | 200 | fits | 148,633 | 222 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 433,860 | 4.339 | 20 | 200 | fits | 149,001 | 171 | 0.467 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 286,399 | 2.864 | 20 | 20 | fits | 148,633 | 222 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 434,564 | 4.346 | 20 | 20 | fits | 149,001 | 171 | 0.467 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 141,406 | 1.414 | 20 | 24 | fits | 146,470 | 166 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 289,049 | 2.890 | 20 | 24 | fits | 148,633 | 222 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 288,983 | 2.890 | 20 | 50 | fits | 148,633 | 222 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 437,588 | 4.376 | 20 | 50 | fits | 149,001 | 171 | 0.467 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 604,701 | 6.047 | 20 | 20 | fits | 89,722 | 25 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,043,739 | 10.437 | 20 | 20 | fits | 67,748 | 24 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 354,371 | 3.544 | 20 | 20 | fits | 138,347 | 163 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 288,151 | 2.882 | 20 | 200 | fits | 147,794 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 425,882 | 4.259 | 20 | 200 | fits | 138,347 | 163 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 289,075 | 2.891 | 20 | 20 | fits | 147,794 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 426,586 | 4.266 | 20 | 20 | fits | 138,347 | 163 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 144,921 | 1.449 | 20 | 24 | fits | 144,373 | 161 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 291,725 | 2.917 | 20 | 24 | fits | 147,794 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 291,659 | 2.917 | 20 | 50 | fits | 147,794 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 429,610 | 4.296 | 20 | 50 | fits | 138,347 | 163 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 519,051 | 5.191 | 20 | 20 | fits | 89,507 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 961,137 | 9.611 | 20 | 20 | fits | 78,408 | 28 | 0.544 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 394,552 | 3.946 | 20 | 20 | fits | 149,672 | 171 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 298,654 | 2.987 | 20 | 200 | fits | 148,063 | 218 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 456,227 | 4.562 | 20 | 200 | fits | 149,672 | 171 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 299,578 | 2.996 | 20 | 20 | fits | 148,063 | 218 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 456,931 | 4.569 | 20 | 20 | fits | 149,672 | 171 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 155,155 | 1.552 | 20 | 24 | fits | 144,520 | 161 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 302,228 | 3.022 | 20 | 24 | fits | 148,063 | 218 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 302,162 | 3.022 | 20 | 50 | fits | 148,063 | 218 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 459,955 | 4.600 | 20 | 50 | fits | 149,672 | 171 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 549,755 | 5.498 | 20 | 20 | fits | 89,866 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 971,655 | 9.717 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,312,704 | 63.127 | 20 | 20 | MISS ceiling | 22,040 | 13 | 0.621 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,334,808 | 63.348 | 20 | 20 | MISS ceiling | 22,221 | 14 | 0.597 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,362,415 | 63.624 | 20 | 20 | MISS ceiling | 26,771 | 18 | 0.701 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,383,774 | 63.838 | 20 | 20 | MISS ceiling | 23,394 | 13 | 0.603 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,406,888 | 64.069 | 20 | 20 | MISS ceiling | 22,070 | 13 | 0.603 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 155,146 | 1.551 | 20 | 200 | fits | 149,699 | 200 | 0.438 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 278,852 | 2.789 | 20 | 200 | fits | 124,322 | 185 | 0.371 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 150,824 | 1.508 | 20 | 20 | fits | 149,699 | 200 | 0.438 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,208,207 | 62.082 | 20 | 20 | MISS ceiling | 37,127 | 15 | 0.753 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 154,464 | 1.545 | 20 | 24 | fits | 149,699 | 200 | 0.438 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,174,566 | 61.746 | 20 | 24 | MISS ceiling | 134,299 | 106 | 0.426 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 153,408 | 1.534 | 20 | 50 | fits | 149,699 | 200 | 0.438 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 277,334 | 2.773 | 20 | 50 | fits | 124,322 | 185 | 0.371 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 367,246 | 3.672 | 20 | 20 | fits | 89,978 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 800,818 | 8.008 | 20 | 20 | fits | 68,508 | 24 | 0.602 |
| LINK_UP | `adp.link_up.if0` | 2,690 | 0.027 | 20 | 200 | fits | 30,690 | 43 (11) | 0.710 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,416 | 0.174 | 20 | 200 | fits | 24,384 | 23 (39) | 0.726 |
| GM_CHANGE | `adp.gm_change.if0` | 2,494 | 0.025 | 20 | 200 | fits | 18,156 | 17 (11) | 0.667 |
| BIND_RX | `acmp.bind_rx.if0` | 20,290 | 0.203 | 20 | 20 | fits | 45,632 | 26 (77) | 0.799 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 14,387 | 0.144 | 20 | 20 | fits | 38,905 | 26 (32) | 0.825 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,338 | 0.113 | 20 | 20 | fits | 29,257 | 15 (47) | 0.770 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,763 | 0.148 | 20 | 20 | fits | 43,079 | 19 (50) | 0.831 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,641 | 0.116 | 20 | 20 | fits | 30,279 | 17 (48) | 0.772 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,538 | 0.105 | 20 | 20 | fits | 28,097 | 16 (48) | 0.727 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,389 | 0.094 | 20 | 20 | fits | 27,452 | 16 (48) | 0.721 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,631 | 0.096 | 20 | 20 | fits | 27,433 | 16 (48) | 0.721 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
