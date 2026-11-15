### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 30 paths and 7 of 233 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.186 (0.400) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.088 (0.230) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.089 (0.414) | fits | 0 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.104 (0.243) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.090 (0.230) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.100 (0.236) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.105 (0.251) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.097 (0.317) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.176 (0.586) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.134 (0.389) | fits | 0 acmp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.023 (0.157) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.266) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.025 (0.257) | fits | 0 events | 3 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.055 (0.202) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.087 (0.379) | fits | 0 events | 2 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-4.adp_available.if0` (backlog-adp@program-4) | 3.646 (5.072) | fits | 7 adp | 17 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.768 (63.033) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.441 (63.705) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.327 (0.463) | fits | 0 aecp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 3.261 | fits | 0 acmp | 19 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.949 | MISS ceiling | 11 acmp | 19 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 3.252 | fits | 0 adp | 19 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.adp.last.if0` (backlog-adp@verify-0) | 4.307 | fits | 7 adp | 19 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 1.856 | fits | 0 aecp | 19 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.703 | MISS ceiling | 15 aecp | 19 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 3.287 | fits | 0 maap | 19 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 4.344 | fits | 6 maap | 19 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.srp.first.if0` (backlog-adp@verify-0) | 5.247 | fits | 0 srp | 19 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.srp.last.if0` (backlog-adp@program-aged2-4) | 9.880 | fits | 31 srp | 19 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.210 (0.210) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-4 | 0 | 10.309 | 10 | 150,145 (1.501) | yes | - |
| backlog-adp@program-0 | 0 | 10.407 | 11 | 149,642 (1.496) | yes | - |
| backlog-adp@program-4 | 0 | 9.707 | 11 | 149,624 (1.496) | yes | - |
| backlog-adp@verify-0 | 0 | 10.749 | 11 | 149,559 (1.496) | yes | - |
| backlog-adp@verify-4 | 0 | 10.987 | 12 | 149,622 (1.496) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 10.234 | 10 | 143,175 (1.432) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.311 | 10 | 149,137 (1.491) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.124 | 12 | 148,278 (1.483) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.366 | 14 | 149,195 (1.492) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.689 | 12 | 149,235 (1.492) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.362 | 10 | 149,036 (1.490) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.641 | 11 | 149,036 (1.490) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.310 | 10 | 149,055 (1.491) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.279 | 11 | 149,118 (1.491) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 10.200 | 9 | 142,979 (1.430) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.447 | 12 | 149,244 (1.492) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.266 | 10 | 149,099 (1.491) | yes | - |
| backlog-owed | 0 | 64.026 | 25 | 144,199 (1.442) | yes | - |
| fixture | 0 | 1.254 | 2 | 81,796 (0.818) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 144,199 CPU cycles (1.442 ms), backlog-owed.
Over the windows that released their whole load only: 144,199 (1.442 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 50568 | 0 | 48,654 (0.487) | fits |
| backlog-adp@blank-4 | 406 | 0 | 150,145 (1.501) | fits |
| backlog-adp@program-0 | 503 | 0 | 149,642 (1.496) | fits |
| backlog-adp@program-4 | 506 | 0 | 149,624 (1.496) | fits |
| backlog-adp@verify-0 | 591 | 0 | 149,559 (1.496) | fits |
| backlog-adp@verify-4 | 592 | 0 | 149,622 (1.496) | fits |
| backlog-adp@blank-aged2-0 | 729 | 0 | 154,245 (1.542) | fits |
| backlog-adp@blank-aged2-4 | 758 | 0 | 149,137 (1.491) | fits |
| backlog-adp@blank-aged1-0 | 665 | 0 | 149,175 (1.492) | fits |
| backlog-adp@blank-aged1-4 | 700 | 0 | 149,195 (1.492) | fits |
| backlog-adp@program-aged2-0 | 821 | 0 | 149,235 (1.492) | fits |
| backlog-adp@program-aged2-4 | 853 | 0 | 149,036 (1.490) | fits |
| backlog-adp@program-aged1-0 | 754 | 0 | 149,036 (1.490) | fits |
| backlog-adp@program-aged1-4 | 786 | 0 | 149,055 (1.491) | fits |
| backlog-adp@verify-aged2-0 | 910 | 0 | 149,118 (1.491) | fits |
| backlog-adp@verify-aged2-4 | 942 | 0 | 149,118 (1.491) | fits |
| backlog-adp@verify-aged1-0 | 845 | 0 | 149,244 (1.492) | fits |
| backlog-adp@verify-aged1-4 | 876 | 0 | 149,099 (1.491) | fits |
| adp-advertise | 599 | 0 | 42,159 (0.422) | fits |
| save | 610 | 0 | 44,539 (0.445) | fits |
| backlog-owed | 310 | 0 | 144,199 (1.442) | fits |
| adp-gm | 89 | 0 | 42,159 (0.422) | fits |
| acmp-cmd | 87 | 0 | 42,159 (0.422) | fits |
| fixture | 161 | 0 | 81,796 (0.818) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.168 ms, 76,333 (0.763 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.936 (20) | 11.064 |
| backlog-adp@blank-aged2-4 | 2 | +5.748 ms, 76,435 (0.764 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.830 (20) | 10.170 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.920 (20) | 11.080 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.839 (20) | 10.161 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.871 (20) | 11.129 |
| backlog-adp@program-aged2-4 | 2 | +5.925 ms, 80,362 (0.804 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.880 (20) | 10.120 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.976 (20) | 11.024 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.027 (20) | 10.973 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.952 (20) | 11.048 |
| backlog-adp@verify-aged2-4 | 2 | +5.801 ms, 77,281 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.715 (20) | 10.285 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.960 (20) | 11.040 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.022 (20) | 10.978 |

Least margin over the aged windows: 10.120 ms, `backlog-adp@program-aged2-4.service.srp.last.if0` at 9.880 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.432 | 6,070 | 102 | 2 | 30.895 | yes | within |
| save | 2018.675 | 4,070 | 102 | - | 10.971 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 520 | 79,478 (0.795) | 77,516 (0.775) |
| backlog-adp@blank-4 | 299 | 90,960 (0.910) | 75,948 (0.759) |
| backlog-adp@program-0 | 328 | 94,759 (0.948) | 78,389 (0.784) |
| backlog-adp@program-4 | 329 | 94,759 (0.948) | 77,749 (0.777) |
| backlog-adp@verify-0 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-4 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@blank-aged2-0 | 297 | 76,333 (0.763) | 75,386 (0.754) |
| backlog-adp@blank-aged2-4 | 297 | 76,435 (0.764) | 75,481 (0.755) |
| backlog-adp@blank-aged1-0 | 298 | 95,354 (0.954) | 75,899 (0.759) |
| backlog-adp@blank-aged1-4 | 297 | 89,739 (0.897) | 75,729 (0.757) |
| backlog-adp@program-aged2-0 | 327 | 94,999 (0.950) | 78,640 (0.786) |
| backlog-adp@program-aged2-4 | 326 | 94,759 (0.948) | 78,192 (0.782) |
| backlog-adp@program-aged1-0 | 327 | 94,899 (0.949) | 78,640 (0.786) |
| backlog-adp@program-aged1-4 | 326 | 94,759 (0.948) | 78,431 (0.784) |
| backlog-adp@verify-aged2-0 | 356 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged2-4 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged1-0 | 356 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged1-4 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| adp-advertise | 578 | 20,761 (0.208) | 1,935 (0.019) |
| save | 585 | 93,963 (0.940) | 77,627 (0.776) |
| backlog-owed | 276 | 20,761 (0.208) | 2,210 (0.022) |
| adp-gm | 80 | 20,719 (0.207) | 1,935 (0.019) |
| acmp-cmd | 65 | 20,719 (0.207) | 1,935 (0.019) |
| fixture | 54 | 15,636 (0.156) | 1,935 (0.019) |

Longest pass that carries a step: 95,354 CPU cycles (0.954 ms), backlog-adp@blank-aged1-0; longest step: 78,640 (0.786 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 344,129 | 3.441 | 20 | 20 | fits | 109,955 | 167 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 297,433 | 2.974 | 20 | 200 | fits | 144,079 | 231 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 415,531 | 4.155 | 20 | 200 | fits | 109,955 | 167 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 298,357 | 2.984 | 20 | 20 | fits | 144,079 | 231 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 416,235 | 4.162 | 20 | 20 | fits | 109,955 | 167 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 157,918 | 1.579 | 20 | 24 | fits | 150,145 | 155 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 301,007 | 3.010 | 20 | 24 | fits | 144,079 | 231 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 300,941 | 3.009 | 20 | 50 | fits | 144,079 | 231 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 419,259 | 4.193 | 20 | 50 | fits | 109,955 | 167 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 509,932 | 5.099 | 20 | 20 | fits | 90,739 | 28 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 906,900 | 9.069 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 335,812 | 3.358 | 20 | 20 | fits | 100,774 | 142 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 292,261 | 2.923 | 20 | 200 | fits | 147,215 | 248 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 392,419 | 3.924 | 20 | 200 | fits | 100,774 | 142 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 293,185 | 2.932 | 20 | 20 | fits | 147,215 | 248 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 393,123 | 3.931 | 20 | 20 | fits | 100,774 | 142 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 149,610 | 1.496 | 20 | 24 | fits | 149,642 | 155 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 295,835 | 2.958 | 20 | 24 | fits | 147,215 | 248 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 295,769 | 2.958 | 20 | 50 | fits | 147,215 | 248 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 396,147 | 3.961 | 20 | 50 | fits | 100,774 | 142 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 486,512 | 4.865 | 20 | 20 | fits | 90,431 | 29 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 893,312 | 8.933 | 20 | 20 | fits | 52,570 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 364,641 | 3.646 | 20 | 20 | fits | 102,600 | 161 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 303,367 | 3.034 | 20 | 200 | fits | 149,467 | 234 | 0.404 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 414,402 | 4.144 | 20 | 200 | fits | 102,600 | 161 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 304,291 | 3.043 | 20 | 20 | fits | 149,467 | 234 | 0.404 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 415,106 | 4.151 | 20 | 20 | fits | 102,600 | 161 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 158,464 | 1.585 | 20 | 24 | fits | 149,624 | 155 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 306,941 | 3.069 | 20 | 24 | fits | 149,467 | 234 | 0.404 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 306,875 | 3.069 | 20 | 50 | fits | 149,467 | 234 | 0.404 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 418,130 | 4.181 | 20 | 50 | fits | 102,600 | 161 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 508,439 | 5.084 | 20 | 20 | fits | 90,375 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 898,520 | 8.985 | 20 | 20 | fits | 52,572 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 359,836 | 3.598 | 20 | 20 | fits | 106,101 | 160 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 325,203 | 3.252 | 20 | 200 | fits | 144,156 | 230 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 430,688 | 4.307 | 20 | 200 | fits | 106,101 | 160 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 326,127 | 3.261 | 20 | 20 | fits | 144,156 | 230 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 431,392 | 4.314 | 20 | 20 | fits | 106,101 | 160 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 185,611 | 1.856 | 20 | 24 | fits | 149,559 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 328,777 | 3.288 | 20 | 24 | fits | 144,156 | 230 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 328,711 | 3.287 | 20 | 50 | fits | 144,156 | 230 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 434,416 | 4.344 | 20 | 50 | fits | 106,101 | 160 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 524,701 | 5.247 | 20 | 20 | fits | 90,351 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 931,964 | 9.320 | 20 | 20 | fits | 53,123 | 20 | 0.675 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 357,708 | 3.577 | 20 | 20 | fits | 104,949 | 149 | 0.468 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 301,796 | 3.018 | 20 | 200 | fits | 147,441 | 249 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 415,137 | 4.151 | 20 | 200 | fits | 104,949 | 149 | 0.468 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 302,720 | 3.027 | 20 | 20 | fits | 147,441 | 249 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 415,841 | 4.158 | 20 | 20 | fits | 104,949 | 149 | 0.468 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 158,919 | 1.589 | 20 | 24 | fits | 149,622 | 155 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 305,370 | 3.054 | 20 | 24 | fits | 147,441 | 249 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 305,304 | 3.053 | 20 | 50 | fits | 147,441 | 249 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 418,865 | 4.189 | 20 | 50 | fits | 104,949 | 149 | 0.468 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 504,539 | 5.045 | 20 | 20 | fits | 85,740 | 30 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 905,538 | 9.055 | 20 | 20 | fits | 63,418 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 349,676 | 3.497 | 20 | 20 | fits | 109,977 | 170 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 289,979 | 2.900 | 20 | 200 | fits | 143,175 | 231 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 399,340 | 3.993 | 20 | 200 | fits | 109,977 | 170 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 290,903 | 2.909 | 20 | 20 | fits | 143,175 | 231 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 400,044 | 4.000 | 20 | 20 | fits | 109,977 | 170 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 151,368 | 1.514 | 20 | 24 | fits | 154,245 | 157 | 0.412 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 293,553 | 2.936 | 20 | 24 | fits | 143,175 | 231 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 293,487 | 2.935 | 20 | 50 | fits | 143,175 | 231 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 403,068 | 4.031 | 20 | 50 | fits | 109,977 | 170 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 503,756 | 5.038 | 20 | 20 | fits | 90,866 | 29 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 893,646 | 8.936 | 20 | 20 | fits | 52,530 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 327,553 | 3.276 | 20 | 20 | fits | 105,855 | 160 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 292,936 | 2.929 | 20 | 200 | fits | 143,792 | 230 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 398,175 | 3.982 | 20 | 200 | fits | 105,855 | 160 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 293,860 | 2.939 | 20 | 20 | fits | 143,792 | 230 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 398,879 | 3.989 | 20 | 20 | fits | 105,855 | 160 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 153,708 | 1.537 | 20 | 24 | fits | 149,137 | 152 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 296,510 | 2.965 | 20 | 24 | fits | 143,792 | 230 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 296,444 | 2.964 | 20 | 50 | fits | 143,792 | 230 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 401,903 | 4.019 | 20 | 50 | fits | 105,855 | 160 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 491,820 | 4.918 | 20 | 20 | fits | 89,983 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 982,952 | 9.830 | 20 | 20 | fits | 63,378 | 24 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 334,590 | 3.346 | 20 | 20 | fits | 100,818 | 142 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 290,959 | 2.910 | 20 | 200 | fits | 148,278 | 253 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 391,161 | 3.912 | 20 | 200 | fits | 100,818 | 142 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 291,883 | 2.919 | 20 | 20 | fits | 148,278 | 253 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 391,865 | 3.919 | 20 | 20 | fits | 100,818 | 142 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 147,245 | 1.472 | 20 | 24 | fits | 149,175 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 294,533 | 2.945 | 20 | 24 | fits | 148,278 | 253 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 294,467 | 2.945 | 20 | 50 | fits | 148,278 | 253 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 394,889 | 3.949 | 20 | 50 | fits | 100,818 | 142 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 485,295 | 4.853 | 20 | 20 | fits | 90,472 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 891,984 | 8.920 | 20 | 20 | fits | 52,530 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 352,670 | 3.527 | 20 | 20 | fits | 105,930 | 163 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 303,906 | 3.039 | 20 | 200 | fits | 143,539 | 231 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 409,220 | 4.092 | 20 | 200 | fits | 105,930 | 163 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 304,830 | 3.048 | 20 | 20 | fits | 143,539 | 231 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 409,924 | 4.099 | 20 | 20 | fits | 105,930 | 163 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 157,197 | 1.572 | 20 | 24 | fits | 149,195 | 153 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 307,480 | 3.075 | 20 | 24 | fits | 143,539 | 231 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 307,414 | 3.074 | 20 | 50 | fits | 143,539 | 231 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 412,948 | 4.129 | 20 | 50 | fits | 105,930 | 163 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 503,361 | 5.034 | 20 | 20 | fits | 90,479 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 983,920 | 9.839 | 20 | 20 | fits | 63,626 | 25 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 346,062 | 3.461 | 20 | 20 | fits | 101,788 | 142 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 302,258 | 3.023 | 20 | 200 | fits | 149,235 | 253 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 403,430 | 4.034 | 20 | 200 | fits | 101,788 | 142 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 303,182 | 3.032 | 20 | 20 | fits | 149,235 | 253 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 404,134 | 4.041 | 20 | 20 | fits | 101,788 | 142 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 149,837 | 1.498 | 20 | 24 | fits | 149,230 | 153 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 305,832 | 3.058 | 20 | 24 | fits | 149,235 | 253 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 305,766 | 3.058 | 20 | 50 | fits | 149,235 | 253 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 407,158 | 4.072 | 20 | 50 | fits | 101,788 | 142 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 497,183 | 4.972 | 20 | 20 | fits | 90,091 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 887,143 | 8.871 | 20 | 20 | fits | 52,572 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 352,320 | 3.523 | 20 | 20 | fits | 98,423 | 154 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 303,452 | 3.035 | 20 | 200 | fits | 148,943 | 233 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 401,259 | 4.013 | 20 | 200 | fits | 98,423 | 154 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 304,376 | 3.044 | 20 | 20 | fits | 148,943 | 233 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 401,963 | 4.020 | 20 | 20 | fits | 98,423 | 154 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 159,073 | 1.591 | 20 | 24 | fits | 149,036 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 307,026 | 3.070 | 20 | 24 | fits | 148,943 | 233 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 306,960 | 3.070 | 20 | 50 | fits | 148,943 | 233 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 404,987 | 4.050 | 20 | 50 | fits | 98,423 | 154 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 495,135 | 4.951 | 20 | 20 | fits | 90,214 | 29 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 988,050 | 9.880 | 20 | 20 | fits | 63,418 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 342,727 | 3.427 | 20 | 20 | fits | 101,908 | 143 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 299,052 | 2.991 | 20 | 200 | fits | 147,254 | 248 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 400,344 | 4.003 | 20 | 200 | fits | 101,908 | 143 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 299,976 | 3.000 | 20 | 20 | fits | 147,254 | 248 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 401,048 | 4.010 | 20 | 20 | fits | 101,908 | 143 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 156,362 | 1.564 | 20 | 24 | fits | 149,036 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 302,626 | 3.026 | 20 | 24 | fits | 147,254 | 248 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 302,560 | 3.026 | 20 | 50 | fits | 147,254 | 248 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 404,072 | 4.041 | 20 | 50 | fits | 101,908 | 143 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 496,387 | 4.964 | 20 | 20 | fits | 82,946 | 31 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 897,625 | 8.976 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 336,815 | 3.368 | 20 | 20 | fits | 105,400 | 160 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 290,064 | 2.901 | 20 | 200 | fits | 143,815 | 230 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 394,848 | 3.948 | 20 | 200 | fits | 105,400 | 160 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 290,988 | 2.910 | 20 | 20 | fits | 143,815 | 230 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 395,552 | 3.956 | 20 | 20 | fits | 105,400 | 160 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 150,813 | 1.508 | 20 | 24 | fits | 149,055 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 293,638 | 2.936 | 20 | 24 | fits | 143,815 | 230 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 293,572 | 2.936 | 20 | 50 | fits | 143,815 | 230 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 398,576 | 3.986 | 20 | 50 | fits | 105,400 | 160 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 488,550 | 4.886 | 20 | 20 | fits | 90,040 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 902,682 | 9.027 | 20 | 20 | fits | 63,496 | 24 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 336,888 | 3.369 | 20 | 20 | fits | 100,748 | 142 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 293,337 | 2.933 | 20 | 200 | fits | 147,039 | 248 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 393,469 | 3.935 | 20 | 200 | fits | 100,748 | 142 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 294,261 | 2.943 | 20 | 20 | fits | 147,039 | 248 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 394,173 | 3.942 | 20 | 20 | fits | 100,748 | 142 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 150,862 | 1.509 | 20 | 24 | fits | 149,118 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 296,911 | 2.969 | 20 | 24 | fits | 147,039 | 248 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 296,845 | 2.968 | 20 | 50 | fits | 147,039 | 248 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 397,197 | 3.972 | 20 | 50 | fits | 100,748 | 142 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 487,345 | 4.873 | 20 | 20 | fits | 90,214 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 895,219 | 8.952 | 20 | 20 | fits | 54,475 | 21 | 0.708 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 352,073 | 3.521 | 20 | 20 | fits | 110,283 | 169 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 284,211 | 2.842 | 20 | 200 | fits | 142,979 | 232 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 402,808 | 4.028 | 20 | 200 | fits | 110,283 | 169 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 285,135 | 2.851 | 20 | 20 | fits | 142,979 | 232 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 403,512 | 4.035 | 20 | 20 | fits | 110,283 | 169 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 145,796 | 1.458 | 20 | 24 | fits | 149,118 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 287,785 | 2.878 | 20 | 24 | fits | 142,979 | 232 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 287,719 | 2.877 | 20 | 50 | fits | 142,979 | 232 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 406,536 | 4.065 | 20 | 50 | fits | 110,283 | 169 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 497,099 | 4.971 | 20 | 20 | fits | 90,629 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 971,517 | 9.715 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 354,725 | 3.547 | 20 | 20 | fits | 101,788 | 142 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 310,921 | 3.109 | 20 | 200 | fits | 149,235 | 253 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 412,093 | 4.121 | 20 | 200 | fits | 101,788 | 142 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 311,845 | 3.118 | 20 | 20 | fits | 149,235 | 253 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 412,797 | 4.128 | 20 | 20 | fits | 101,788 | 142 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 158,500 | 1.585 | 20 | 24 | fits | 149,244 | 153 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 314,495 | 3.145 | 20 | 24 | fits | 149,235 | 253 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 314,429 | 3.144 | 20 | 50 | fits | 149,235 | 253 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 415,821 | 4.158 | 20 | 50 | fits | 101,788 | 142 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 506,088 | 5.061 | 20 | 20 | fits | 90,333 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 896,048 | 8.960 | 20 | 20 | fits | 52,572 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 338,195 | 3.382 | 20 | 20 | fits | 105,426 | 160 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 291,444 | 2.914 | 20 | 200 | fits | 143,849 | 230 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 396,254 | 3.963 | 20 | 200 | fits | 105,426 | 160 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 292,368 | 2.924 | 20 | 20 | fits | 143,849 | 230 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 396,958 | 3.970 | 20 | 20 | fits | 105,426 | 160 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 152,159 | 1.522 | 20 | 24 | fits | 149,099 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 295,018 | 2.950 | 20 | 24 | fits | 143,849 | 230 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 294,952 | 2.950 | 20 | 50 | fits | 143,849 | 230 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 399,982 | 4.000 | 20 | 50 | fits | 105,426 | 160 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 490,316 | 4.903 | 20 | 20 | fits | 90,400 | 29 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 902,183 | 9.022 | 20 | 20 | fits | 63,418 | 24 | 0.600 |
| LINK_UP | `adp.link_up.if0` | 2,501 | 0.025 | 20 | 200 | fits | 25,663 | 43 (11) | 0.728 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,715 | 0.087 | 20 | 200 | fits | 21,370 | 23 (39) | 0.723 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 5,454 | 0.055 | 20 | 200 | fits | 2,587 | 10 (11) | 0.600 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,276,837 | 62.768 | 20 | 20 | MISS ceiling | 16,968 | 13 | 0.589 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,293,730 | 62.937 | 20 | 20 | MISS ceiling | 16,969 | 13 | 0.597 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,310,545 | 63.105 | 20 | 20 | MISS ceiling | 16,872 | 13 | 0.606 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,327,342 | 63.273 | 20 | 20 | MISS ceiling | 16,873 | 13 | 0.606 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,344,137 | 63.441 | 20 | 20 | MISS ceiling | 16,804 | 13 | 0.600 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 154,294 | 1.543 | 20 | 200 | fits | 144,199 | 222 | 0.418 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 241,380 | 2.414 | 20 | 200 | fits | 87,702 | 164 | 0.375 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 149,972 | 1.500 | 20 | 20 | fits | 144,199 | 222 | 0.418 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,194,918 | 61.949 | 20 | 20 | MISS ceiling | 28,078 | 15 | 0.759 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 153,612 | 1.536 | 20 | 24 | fits | 144,199 | 222 | 0.418 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,170,326 | 61.703 | 20 | 24 | MISS ceiling | 137,610 | 106 | 0.429 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 152,556 | 1.526 | 20 | 50 | fits | 144,199 | 222 | 0.418 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 239,862 | 2.399 | 20 | 50 | fits | 87,702 | 164 | 0.375 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 329,956 | 3.300 | 20 | 20 | fits | 90,160 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 728,238 | 7.282 | 20 | 20 | fits | 52,781 | 20 | 0.653 |
| LINK_UP | `adp.link_up.if0` | 2,501 | 0.025 | 20 | 200 | fits | 25,663 | 43 (11) | 0.728 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,715 | 0.087 | 20 | 200 | fits | 21,370 | 23 (39) | 0.723 |
| GM_CHANGE | `adp.gm_change.if0` | 2,296 | 0.023 | 20 | 200 | fits | 15,705 | 17 (11) | 0.700 |
| BIND_RX | `acmp.bind_rx.if0` | 17,883 | 0.179 | 20 | 20 | fits | 39,329 | 26 (77) | 0.799 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,697 | 0.097 | 20 | 20 | fits | 31,723 | 19 (32) | 0.847 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,433 | 0.104 | 20 | 20 | fits | 24,278 | 15 (47) | 0.776 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,358 | 0.134 | 20 | 20 | fits | 38,859 | 18 (50) | 0.847 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,471 | 0.105 | 20 | 20 | fits | 25,109 | 17 (48) | 0.771 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,030 | 0.100 | 20 | 20 | fits | 23,574 | 16 (48) | 0.747 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,757 | 0.088 | 20 | 20 | fits | 23,023 | 16 (48) | 0.745 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,999 | 0.090 | 20 | 20 | fits | 22,978 | 16 (48) | 0.743 |
| LINK_UP | `fixture.link_up.if0` | 2,501 | 0.025 | 20 | 200 | fits | 25,663 | 43 (11) | 0.728 |
| malformed MRPDU discard | `fixture.malformed.if0` | 20,984 | 0.210 | 20 | 20 | fits | 21,050 | 12 | 0.719 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,688 | 0.327 | 20 | 24 | fits | 46,281 | 43 | 0.777 |
| LINK_DOWN | `fixture.link_down.if0` | 2,492 | 0.025 | 20 | 200 | fits | 26,583 | 23 (9) | 0.791 |
| BIND_RX | `fixture.bind_rx.if0` | 18,587 | 0.186 | 20 | 20 | fits | 40,034 | 26 (77) | 0.806 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 17,571 | 0.176 | 20 | 20 | fits | 35,317 | 29 (35) | 0.794 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 8,854 | 0.089 | 20 | 20 | fits | 24,420 | 13 (29) | 0.831 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 81,692 | 0.817 | 20 | 200 | fits | 81,796 | 49 | 0.756 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 81,692 | 0.817 | 20 | 200 | fits | 81,796 | 49 | 0.756 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 81,418 | 0.814 | 20 | 20 | fits | 81,796 | 49 | 0.756 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 81,418 | 0.814 | 20 | 20 | fits | 81,796 | 49 | 0.756 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 81,626 | 0.816 | 20 | 24 | fits | 81,796 | 49 | 0.756 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 81,626 | 0.816 | 20 | 24 | fits | 81,796 | 49 | 0.756 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 81,560 | 0.816 | 20 | 50 | fits | 81,796 | 49 | 0.756 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 81,560 | 0.816 | 20 | 50 | fits | 81,796 | 49 | 0.756 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 81,494 | 0.815 | 20 | 20 | fits | 81,796 | 49 | 0.756 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 81,494 | 0.815 | 20 | 20 | fits | 81,796 | 49 | 0.756 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
