### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 37 paths and 1 of 250 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.269 (0.539) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.073 (0.365) | fits | 0 adp | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.225 (0.725) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.358) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.027 (0.307) | fits | 0 events | 2 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.044 (0.220) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.174 (0.521) | fits | 0 events | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.408 (0.700) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.549 (0.914) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.418 (0.712) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.493 (0.829) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.465 (0.768) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.520 (0.825) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-0.adp_available.if0` (backlog-adp@verify-0) | 4.216 (5.859) | fits | 7 adp | 19 | 0 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.371 (0.510) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.420 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 2.621 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 3.021 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.789 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 8.955 | fits | 31 srp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.198 (0.563) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.117 (0.258) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.132 (0.307) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.178 (0.563) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.247 (0.587) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-held.mrpdu.leaveall.if0` (save-held) | 161.123 | MISS ceiling | 0 srp | 3 | 1 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 3.563 | fits | 0 acmp | 20 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.acmp.last.if0` (backlog-adp@verify-0) | 4.938 | fits | 11 acmp | 20 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 3.554 | fits | 0 adp | 20 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.adp.last.if0` (backlog-adp@verify-0) | 4.931 | fits | 7 adp | 20 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 2.121 | fits | 0 aecp | 20 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.aecp.last.if0` (backlog-adp@verify-0) | 3.589 | fits | 15 aecp | 20 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 3.589 | fits | 0 maap | 20 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 4.968 | fits | 6 maap | 20 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.srp.first.if0` (backlog-adp@verify-0) | 5.863 | fits | 0 srp | 20 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.srp.last.if0` (backlog-adp@program-aged2-4) | 10.555 | fits | 31 srp | 20 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.238 (0.239) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-1 | 0 | 10.981 | 10 | 147,472 (1.475) | yes | - |
| backlog-adp@blank-4 | 0 | 11.455 | 12 | 148,127 (1.481) | yes | - |
| backlog-adp@program-0 | 0 | 11.073 | 10 | 147,637 (1.476) | yes | - |
| backlog-adp@program-4 | 0 | 10.261 | 10 | 147,813 (1.478) | yes | - |
| backlog-adp@verify-0 | 0 | 11.631 | 10 | 147,843 (1.478) | yes | - |
| backlog-adp@verify-4 | 0 | 11.535 | 12 | 147,485 (1.475) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 10.943 | 11 | 148,068 (1.481) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.034 | 10 | 147,802 (1.478) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.104 | 10 | 149,162 (1.492) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.260 | 12 | 148,961 (1.490) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.159 | 12 | 149,003 (1.490) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.119 | 10 | 147,684 (1.477) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.186 | 11 | 147,691 (1.477) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.103 | 10 | 147,436 (1.474) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.037 | 11 | 147,570 (1.476) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.253 | 12 | 148,039 (1.480) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.277 | 12 | 148,869 (1.489) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.941 | 9 | 148,994 (1.490) | yes | - |
| backlog-adp | 0 | 10.176 | 10 | 147,788 (1.478) | yes | - |
| fixture | 0 | 1.504 | 2 | 98,887 (0.989) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill, backlog-owed not run): 147,788 CPU cycles (1.478 ms), backlog-adp.
Over the windows that released their whole load only: 147,788 (1.478 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3367 | 0 | 155,509 (1.555) | fits |
| backlog-adp@blank-1 | 536 | 0 | 147,472 (1.475) | fits |
| backlog-adp@blank-4 | 538 | 0 | 148,127 (1.481) | fits |
| backlog-adp@program-0 | 892 | 0 | 147,637 (1.476) | fits |
| backlog-adp@program-4 | 895 | 0 | 147,813 (1.478) | fits |
| backlog-adp@verify-0 | 1242 | 0 | 147,843 (1.478) | fits |
| backlog-adp@verify-4 | 1244 | 0 | 147,485 (1.475) | fits |
| backlog-adp@blank-aged2-0 | 812 | 0 | 148,068 (1.481) | fits |
| backlog-adp@blank-aged2-4 | 840 | 0 | 147,802 (1.478) | fits |
| backlog-adp@blank-aged1-0 | 755 | 0 | 149,162 (1.492) | fits |
| backlog-adp@blank-aged1-4 | 785 | 0 | 148,961 (1.490) | fits |
| backlog-adp@program-aged2-0 | 1165 | 0 | 149,003 (1.490) | fits |
| backlog-adp@program-aged2-4 | 1192 | 0 | 147,684 (1.477) | fits |
| backlog-adp@program-aged1-0 | 1107 | 0 | 147,691 (1.477) | fits |
| backlog-adp@program-aged1-4 | 1135 | 0 | 147,436 (1.474) | fits |
| backlog-adp@verify-aged2-0 | 1516 | 0 | 147,570 (1.476) | fits |
| backlog-adp@verify-aged2-4 | 1545 | 0 | 148,039 (1.480) | fits |
| backlog-adp@verify-aged1-0 | 1460 | 0 | 148,869 (1.489) | fits |
| backlog-adp@verify-aged1-4 | 1486 | 0 | 148,994 (1.490) | fits |
| adp-advertise | 596 | 0 | 94,822 (0.948) | fits |
| backlog-adp | 310 | 0 | 147,788 (1.478) | fits |
| maap | 185 | 0 | 94,822 (0.948) | fits |
| aecp-fanout | 109 | 0 | 94,822 (0.948) | fits |
| fixture | 159 | 0 | 98,887 (0.989) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.812 ms, 76,035 (0.760 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.553 (20) | 10.447 |
| backlog-adp@blank-aged2-4 | 2 | +5.335 ms, 76,158 (0.762 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.467 (20) | 9.533 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.571 (20) | 10.429 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.631 (20) | 10.369 |
| backlog-adp@program-aged2-0 | 2 | none | +9.981 ms, 80,444 (0.804 ms), issue | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.579 (20) | 10.421 |
| backlog-adp@program-aged2-4 | 2 | none | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.555 (20) | 9.445 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.595 (20) | 10.405 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.727 (20) | 10.273 |
| backlog-adp@verify-aged2-0 | 2 | none | +9.899 ms, 77,021 (0.770 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.644 (20) | 10.356 |
| backlog-adp@verify-aged2-4 | 2 | +5.394 ms, 77,355 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.377 (20) | 9.623 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.591 (20) | 10.409 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.607 (20) | 10.393 |

Least margin over the aged windows: 9.445 ms, `backlog-adp@program-aged2-4.service.srp.last.if0` at 10.555 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4817.416 | 12,470 | 382 | - | 16.543 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,524 (1.005) | 78,069 (0.781) |
| backlog-adp@blank-1 | 339 | 93,561 (0.936) | 75,531 (0.755) |
| backlog-adp@blank-4 | 339 | 93,633 (0.936) | 75,531 (0.755) |
| backlog-adp@program-0 | 448 | 100,309 (1.003) | 78,162 (0.782) |
| backlog-adp@program-4 | 449 | 100,309 (1.003) | 77,865 (0.779) |
| backlog-adp@verify-0 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-4 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@blank-aged2-0 | 337 | 77,166 (0.772) | 75,343 (0.753) |
| backlog-adp@blank-aged2-4 | 337 | 77,166 (0.772) | 75,372 (0.754) |
| backlog-adp@blank-aged1-0 | 337 | 92,542 (0.925) | 75,437 (0.754) |
| backlog-adp@blank-aged1-4 | 337 | 92,267 (0.923) | 75,488 (0.755) |
| backlog-adp@program-aged2-0 | 446 | 100,309 (1.003) | 78,029 (0.780) |
| backlog-adp@program-aged2-4 | 446 | 100,309 (1.003) | 78,238 (0.782) |
| backlog-adp@program-aged1-0 | 446 | 100,309 (1.003) | 78,184 (0.782) |
| backlog-adp@program-aged1-4 | 446 | 100,309 (1.003) | 78,213 (0.782) |
| backlog-adp@verify-aged2-0 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged2-4 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged1-0 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged1-4 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| adp-advertise | 577 | 25,967 (0.260) | 2,512 (0.025) |
| backlog-adp | 271 | 25,967 (0.260) | 2,512 (0.025) |
| maap | 174 | 25,780 (0.258) | 2,512 (0.025) |
| aecp-fanout | 79 | 25,733 (0.257) | 2,512 (0.025) |
| fixture | 54 | 26,717 (0.267) | 2,376 (0.024) |

Longest pass that carries a step: 104,105 CPU cycles (1.041 ms), backlog-adp@verify-0; longest step: 78,512 (0.785 ms), backlog-adp@verify-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 262,118 | 2.621 | 20 | 200 | fits | 107,549 | 133 | 0.427 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 241,981 | 2.420 | 20 | 20 | fits | 107,549 | 133 | 0.427 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 302,104 | 3.021 | 20 | 24 | fits | 93,550 | 59 | 0.558 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 178,938 | 1.789 | 20 | 50 | fits | 54,930 | 55 | 0.513 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 895,512 | 8.955 | 20 | 20 | fits | 45,292 | 16 | 0.714 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 112,717 | 1.127 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 16,112,321 | 161.123 | 20 | 20 | MISS ceiling | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 370,063 | 3.701 | 20 | 20 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 357,170 | 3.572 | 20 | 20 | fits | 138,884 | 163 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 290,520 | 2.905 | 20 | 200 | fits | 147,472 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 428,788 | 4.288 | 20 | 200 | fits | 138,884 | 163 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 291,444 | 2.914 | 20 | 20 | fits | 147,472 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 429,492 | 4.295 | 20 | 20 | fits | 138,884 | 163 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 147,612 | 1.476 | 20 | 24 | fits | 145,224 | 164 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 294,094 | 2.941 | 20 | 24 | fits | 147,472 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 294,028 | 2.940 | 20 | 50 | fits | 147,472 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 432,516 | 4.325 | 20 | 50 | fits | 138,884 | 163 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 522,276 | 5.223 | 20 | 20 | fits | 89,826 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 965,514 | 9.655 | 20 | 20 | fits | 72,846 | 30 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 370,832 | 3.708 | 20 | 20 | fits | 142,862 | 170 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 292,265 | 2.923 | 20 | 200 | fits | 148,127 | 218 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 443,265 | 4.433 | 20 | 200 | fits | 142,862 | 170 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 293,189 | 2.932 | 20 | 20 | fits | 148,127 | 218 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 443,969 | 4.440 | 20 | 20 | fits | 142,862 | 170 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 148,702 | 1.487 | 20 | 24 | fits | 145,179 | 164 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 295,839 | 2.958 | 20 | 24 | fits | 148,127 | 218 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 295,773 | 2.958 | 20 | 50 | fits | 148,127 | 218 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 446,993 | 4.470 | 20 | 50 | fits | 142,862 | 170 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 537,209 | 5.372 | 20 | 20 | fits | 90,282 | 24 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 965,165 | 9.652 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 361,788 | 3.618 | 20 | 20 | fits | 138,678 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 295,801 | 2.958 | 20 | 200 | fits | 147,637 | 217 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 433,863 | 4.339 | 20 | 200 | fits | 138,678 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 296,725 | 2.967 | 20 | 20 | fits | 147,637 | 217 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 434,567 | 4.346 | 20 | 20 | fits | 138,678 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 152,728 | 1.527 | 20 | 24 | fits | 145,574 | 164 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 299,375 | 2.994 | 20 | 24 | fits | 147,637 | 217 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 299,309 | 2.993 | 20 | 50 | fits | 147,637 | 217 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 437,591 | 4.376 | 20 | 50 | fits | 138,678 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 526,711 | 5.267 | 20 | 20 | fits | 89,186 | 25 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 969,667 | 9.697 | 20 | 20 | fits | 72,846 | 30 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 371,105 | 3.711 | 20 | 20 | fits | 142,537 | 170 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 292,152 | 2.922 | 20 | 200 | fits | 147,813 | 218 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 442,878 | 4.429 | 20 | 200 | fits | 142,537 | 170 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 293,076 | 2.931 | 20 | 20 | fits | 147,813 | 218 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 443,582 | 4.436 | 20 | 20 | fits | 142,537 | 170 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 148,903 | 1.489 | 20 | 24 | fits | 145,787 | 164 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 295,726 | 2.957 | 20 | 24 | fits | 147,813 | 218 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 295,660 | 2.957 | 20 | 50 | fits | 147,813 | 218 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 446,606 | 4.466 | 20 | 50 | fits | 142,537 | 170 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 536,093 | 5.361 | 20 | 20 | fits | 89,553 | 24 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 964,131 | 9.641 | 20 | 20 | fits | 73,403 | 30 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 421,618 | 4.216 | 20 | 20 | fits | 138,295 | 163 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 355,374 | 3.554 | 20 | 200 | fits | 147,843 | 217 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 493,053 | 4.931 | 20 | 200 | fits | 138,295 | 163 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 356,298 | 3.563 | 20 | 20 | fits | 147,843 | 217 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 493,757 | 4.938 | 20 | 20 | fits | 138,295 | 163 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 212,095 | 2.121 | 20 | 24 | fits | 146,247 | 164 | 0.364 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 358,948 | 3.589 | 20 | 24 | fits | 147,843 | 217 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 358,882 | 3.589 | 20 | 50 | fits | 147,843 | 217 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 496,781 | 4.968 | 20 | 50 | fits | 138,295 | 163 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 586,274 | 5.863 | 20 | 20 | fits | 89,559 | 24 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,029,592 | 10.296 | 20 | 20 | fits | 72,846 | 30 | 0.642 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 379,131 | 3.791 | 20 | 20 | fits | 143,180 | 170 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 299,570 | 2.996 | 20 | 200 | fits | 147,485 | 218 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 450,903 | 4.509 | 20 | 200 | fits | 143,180 | 170 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 300,494 | 3.005 | 20 | 20 | fits | 147,485 | 218 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 451,607 | 4.516 | 20 | 20 | fits | 143,180 | 170 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 156,649 | 1.566 | 20 | 24 | fits | 145,450 | 164 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 303,144 | 3.031 | 20 | 24 | fits | 147,485 | 218 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 303,078 | 3.031 | 20 | 50 | fits | 147,485 | 218 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 454,631 | 4.546 | 20 | 50 | fits | 143,180 | 170 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 549,839 | 5.498 | 20 | 20 | fits | 95,274 | 30 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 971,944 | 9.719 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 363,587 | 3.636 | 20 | 20 | fits | 138,826 | 164 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 288,162 | 2.882 | 20 | 200 | fits | 148,068 | 217 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 426,372 | 4.264 | 20 | 200 | fits | 138,826 | 164 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 289,086 | 2.891 | 20 | 20 | fits | 148,068 | 217 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 427,076 | 4.271 | 20 | 20 | fits | 138,826 | 164 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 144,658 | 1.447 | 20 | 24 | fits | 144,238 | 161 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 291,736 | 2.917 | 20 | 24 | fits | 148,068 | 217 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 291,670 | 2.917 | 20 | 50 | fits | 148,068 | 217 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 430,100 | 4.301 | 20 | 50 | fits | 138,826 | 164 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 531,966 | 5.320 | 20 | 20 | fits | 93,015 | 31 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 955,347 | 9.553 | 20 | 20 | fits | 67,647 | 24 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 361,093 | 3.611 | 20 | 20 | fits | 138,835 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 295,022 | 2.950 | 20 | 200 | fits | 147,802 | 217 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 433,241 | 4.332 | 20 | 200 | fits | 138,835 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 295,946 | 2.959 | 20 | 20 | fits | 147,802 | 217 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 433,945 | 4.339 | 20 | 20 | fits | 138,835 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 151,784 | 1.518 | 20 | 24 | fits | 144,249 | 161 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 298,596 | 2.986 | 20 | 24 | fits | 147,802 | 217 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 298,530 | 2.985 | 20 | 50 | fits | 147,802 | 217 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 436,969 | 4.370 | 20 | 50 | fits | 138,835 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 531,824 | 5.318 | 20 | 20 | fits | 94,921 | 30 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,046,689 | 10.467 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 354,033 | 3.540 | 20 | 20 | fits | 149,162 | 202 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 277,329 | 2.773 | 20 | 200 | fits | 149,011 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 425,875 | 4.259 | 20 | 200 | fits | 149,162 | 202 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 278,253 | 2.783 | 20 | 20 | fits | 149,011 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 426,579 | 4.266 | 20 | 20 | fits | 149,162 | 202 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 132,882 | 1.329 | 20 | 24 | fits | 135,970 | 120 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 280,903 | 2.809 | 20 | 24 | fits | 149,011 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 280,837 | 2.808 | 20 | 50 | fits | 149,011 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 429,603 | 4.296 | 20 | 50 | fits | 149,162 | 202 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 519,253 | 5.193 | 20 | 20 | fits | 89,716 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 957,089 | 9.571 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 369,881 | 3.699 | 20 | 20 | fits | 138,913 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 303,784 | 3.038 | 20 | 200 | fits | 148,961 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 442,081 | 4.421 | 20 | 200 | fits | 138,913 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 304,708 | 3.047 | 20 | 20 | fits | 148,961 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 442,785 | 4.428 | 20 | 20 | fits | 138,913 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 151,582 | 1.516 | 20 | 24 | fits | 144,583 | 162 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 307,358 | 3.074 | 20 | 24 | fits | 148,961 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 307,292 | 3.073 | 20 | 50 | fits | 148,961 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 445,809 | 4.458 | 20 | 50 | fits | 138,913 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 540,870 | 5.409 | 20 | 20 | fits | 95,127 | 30 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 963,103 | 9.631 | 20 | 20 | fits | 67,509 | 25 | 0.590 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 380,276 | 3.803 | 20 | 20 | fits | 138,874 | 163 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 304,797 | 3.048 | 20 | 200 | fits | 149,003 | 222 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 443,055 | 4.431 | 20 | 200 | fits | 138,874 | 163 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 305,721 | 3.057 | 20 | 20 | fits | 149,003 | 222 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 443,759 | 4.438 | 20 | 20 | fits | 138,874 | 163 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 152,646 | 1.526 | 20 | 24 | fits | 144,512 | 162 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 308,371 | 3.084 | 20 | 24 | fits | 149,003 | 222 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 308,305 | 3.083 | 20 | 50 | fits | 149,003 | 222 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 446,783 | 4.468 | 20 | 50 | fits | 138,874 | 163 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 535,748 | 5.357 | 20 | 20 | fits | 89,031 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 957,860 | 9.579 | 20 | 20 | fits | 67,509 | 25 | 0.590 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 367,380 | 3.674 | 20 | 20 | fits | 138,687 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 301,393 | 3.014 | 20 | 200 | fits | 147,684 | 217 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 439,464 | 4.395 | 20 | 200 | fits | 138,687 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 302,317 | 3.023 | 20 | 20 | fits | 147,684 | 217 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 440,168 | 4.402 | 20 | 20 | fits | 138,687 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 158,273 | 1.583 | 20 | 24 | fits | 144,630 | 161 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 304,967 | 3.050 | 20 | 24 | fits | 147,684 | 217 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 304,901 | 3.049 | 20 | 50 | fits | 147,684 | 217 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 443,192 | 4.432 | 20 | 50 | fits | 138,687 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 529,401 | 5.294 | 20 | 20 | fits | 86,275 | 33 | 0.798 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,055,528 | 10.555 | 20 | 20 | fits | 78,408 | 28 | 0.544 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 358,897 | 3.589 | 20 | 20 | fits | 139,063 | 164 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 292,838 | 2.928 | 20 | 200 | fits | 147,691 | 217 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 431,285 | 4.313 | 20 | 200 | fits | 139,063 | 164 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 293,762 | 2.938 | 20 | 20 | fits | 147,691 | 217 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 431,989 | 4.320 | 20 | 20 | fits | 139,063 | 164 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 149,711 | 1.497 | 20 | 24 | fits | 144,635 | 161 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 296,412 | 2.964 | 20 | 24 | fits | 147,691 | 217 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 296,346 | 2.963 | 20 | 50 | fits | 147,691 | 217 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 435,013 | 4.350 | 20 | 50 | fits | 139,063 | 164 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 536,148 | 5.361 | 20 | 20 | fits | 92,382 | 31 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 959,483 | 9.595 | 20 | 20 | fits | 67,647 | 24 | 0.596 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 365,381 | 3.654 | 20 | 20 | fits | 138,650 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 298,875 | 2.989 | 20 | 200 | fits | 147,436 | 217 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 436,909 | 4.369 | 20 | 200 | fits | 138,650 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 299,799 | 2.998 | 20 | 20 | fits | 147,436 | 217 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 437,613 | 4.376 | 20 | 20 | fits | 138,650 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 156,003 | 1.560 | 20 | 24 | fits | 144,413 | 161 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 302,449 | 3.024 | 20 | 24 | fits | 147,436 | 217 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 302,383 | 3.024 | 20 | 50 | fits | 147,436 | 217 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 440,637 | 4.406 | 20 | 50 | fits | 138,650 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 535,021 | 5.350 | 20 | 20 | fits | 94,450 | 30 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 972,739 | 9.727 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 361,293 | 3.613 | 20 | 20 | fits | 138,800 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 295,168 | 2.952 | 20 | 200 | fits | 147,570 | 217 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 433,352 | 4.334 | 20 | 200 | fits | 138,800 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 296,092 | 2.961 | 20 | 20 | fits | 147,570 | 217 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 434,056 | 4.341 | 20 | 20 | fits | 138,800 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 152,162 | 1.522 | 20 | 24 | fits | 144,249 | 161 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 298,742 | 2.987 | 20 | 24 | fits | 147,570 | 217 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 298,676 | 2.987 | 20 | 50 | fits | 147,570 | 217 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 437,080 | 4.371 | 20 | 50 | fits | 138,800 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 526,558 | 5.266 | 20 | 20 | fits | 89,544 | 24 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 964,446 | 9.644 | 20 | 20 | fits | 67,885 | 24 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 367,017 | 3.670 | 20 | 20 | fits | 142,695 | 170 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 288,157 | 2.882 | 20 | 200 | fits | 148,039 | 218 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 438,791 | 4.388 | 20 | 200 | fits | 142,695 | 170 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 289,081 | 2.891 | 20 | 20 | fits | 148,039 | 218 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 439,495 | 4.395 | 20 | 20 | fits | 142,695 | 170 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 144,682 | 1.447 | 20 | 24 | fits | 144,249 | 161 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 291,731 | 2.917 | 20 | 24 | fits | 148,039 | 218 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 291,665 | 2.917 | 20 | 50 | fits | 148,039 | 218 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 442,519 | 4.425 | 20 | 50 | fits | 142,695 | 170 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 537,646 | 5.376 | 20 | 20 | fits | 95,193 | 30 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,037,666 | 10.377 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 371,538 | 3.715 | 20 | 20 | fits | 138,932 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 305,359 | 3.054 | 20 | 200 | fits | 148,869 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 443,675 | 4.437 | 20 | 200 | fits | 138,932 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 306,283 | 3.063 | 20 | 20 | fits | 148,869 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 444,379 | 4.444 | 20 | 20 | fits | 138,932 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 153,390 | 1.534 | 20 | 24 | fits | 144,402 | 162 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 308,933 | 3.089 | 20 | 24 | fits | 148,869 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 308,867 | 3.089 | 20 | 50 | fits | 148,869 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 447,403 | 4.474 | 20 | 50 | fits | 138,932 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 536,957 | 5.370 | 20 | 20 | fits | 89,620 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 959,069 | 9.591 | 20 | 20 | fits | 67,509 | 25 | 0.590 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 362,986 | 3.630 | 20 | 20 | fits | 148,994 | 203 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 277,216 | 2.772 | 20 | 200 | fits | 148,883 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 425,594 | 4.256 | 20 | 200 | fits | 148,994 | 203 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 278,140 | 2.781 | 20 | 20 | fits | 148,883 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 426,298 | 4.263 | 20 | 20 | fits | 148,994 | 203 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 132,897 | 1.329 | 20 | 24 | fits | 136,089 | 120 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 280,790 | 2.808 | 20 | 24 | fits | 148,883 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 280,724 | 2.807 | 20 | 50 | fits | 148,883 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 429,322 | 4.293 | 20 | 50 | fits | 148,994 | 203 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 518,946 | 5.189 | 20 | 20 | fits | 89,690 | 25 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 960,713 | 9.607 | 20 | 20 | fits | 78,408 | 28 | 0.544 |
| LINK_UP | `adp.link_up.if0` | 2,690 | 0.027 | 20 | 200 | fits | 30,690 | 43 (11) | 0.710 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,416 | 0.174 | 20 | 200 | fits | 24,384 | 23 (39) | 0.726 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 4,384 | 0.044 | 20 | 200 | fits | 2,567 | 10 (11) | 0.520 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 366,228 | 3.662 | 20 | 20 | fits | 142,373 | 170 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 288,277 | 2.883 | 20 | 200 | fits | 147,788 | 218 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 438,567 | 4.386 | 20 | 200 | fits | 142,373 | 170 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 289,201 | 2.892 | 20 | 20 | fits | 147,788 | 218 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 439,271 | 4.393 | 20 | 20 | fits | 142,373 | 170 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 145,053 | 1.451 | 20 | 24 | fits | 145,239 | 164 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 291,851 | 2.919 | 20 | 24 | fits | 147,788 | 218 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 291,785 | 2.918 | 20 | 50 | fits | 147,788 | 218 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 442,295 | 4.423 | 20 | 50 | fits | 142,373 | 170 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 537,003 | 5.370 | 20 | 20 | fits | 94,774 | 30 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 959,083 | 9.591 | 20 | 20 | fits | 67,412 | 24 | 0.591 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,187 | 0.132 | 20 | 50 | fits | 30,690 | 43 | 0.710 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 24,003 | 0.240 | 20 | 50 | fits | 31,237 | 41 | 0.651 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 24,711 | 0.247 | 20 | 50 | fits | 31,412 | 41 | 0.654 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 17,819 | 0.178 | 20 | 50 | fits | 32,805 | 61 | 0.629 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,831 | 0.198 | 20 | 50 | fits | 32,805 | 61 | 0.629 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,721 | 0.117 | 20 | 50 | fits | 25,782 | 30 | 0.613 |
| set_name | `aecp_fanout.set_name.if0` | 49,262 | 0.493 | 20 | 24 | fits | 61,615 | 89 | 0.567 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 54,932 | 0.549 | 20 | 24 | fits | 52,294 | 78 | 0.591 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 41,830 | 0.418 | 20 | 24 | fits | 49,355 | 79 | 0.572 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,700 | 0.407 | 20 | 24 | fits | 48,320 | 78 | 0.563 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 46,463 | 0.465 | 20 | 24 | fits | 52,124 | 67 | 0.589 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 40,768 | 0.408 | 20 | 24 | fits | 48,225 | 78 | 0.561 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 51,965 | 0.520 | 20 | 24 | fits | 46,095 | 79 | 0.525 |
| LINK_UP | `fixture.link_up.if0` | 2,690 | 0.027 | 20 | 200 | fits | 30,690 | 43 (11) | 0.710 |
| malformed MRPDU discard | `fixture.malformed.if0` | 23,791 | 0.238 | 20 | 20 | fits | 23,857 | 12 | 0.697 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 37,074 | 0.371 | 20 | 24 | fits | 51,044 | 43 | 0.775 |
| LINK_DOWN | `fixture.link_down.if0` | 2,530 | 0.025 | 20 | 200 | fits | 35,821 | 23 (9) | 0.765 |
| BIND_RX | `fixture.bind_rx.if0` | 26,937 | 0.269 | 20 | 20 | fits | 53,862 | 34 (77) | 0.789 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 22,529 | 0.225 | 20 | 20 | fits | 49,174 | 37 (35) | 0.743 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 7,257 | 0.073 | 20 | 20 | fits | 36,456 | 21 (29) | 0.751 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 98,783 | 0.988 | 20 | 200 | fits | 98,887 | 77 | 0.738 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 98,783 | 0.988 | 20 | 200 | fits | 98,887 | 77 | 0.738 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 98,509 | 0.985 | 20 | 20 | fits | 98,887 | 77 | 0.738 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 98,509 | 0.985 | 20 | 20 | fits | 98,887 | 77 | 0.738 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 98,717 | 0.987 | 20 | 24 | fits | 98,887 | 77 | 0.738 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 98,717 | 0.987 | 20 | 24 | fits | 98,887 | 77 | 0.738 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 98,651 | 0.987 | 20 | 50 | fits | 98,887 | 77 | 0.738 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 98,651 | 0.987 | 20 | 50 | fits | 98,887 | 77 | 0.738 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 98,585 | 0.986 | 20 | 20 | fits | 98,887 | 77 | 0.738 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 98,585 | 0.986 | 20 | 20 | fits | 98,887 | 77 | 0.738 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
