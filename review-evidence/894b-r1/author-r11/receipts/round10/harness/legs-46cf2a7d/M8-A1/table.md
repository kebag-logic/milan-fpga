### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 28 paths and 0 of 107 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.207 (0.466) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.094 (0.282) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.113 (0.305) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.106 (0.296) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.106 (0.290) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.110 (0.303) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.105 (0.351) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.154 (0.423) | fits | 0 acmp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.029 (0.336) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.098 (0.294) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.142 (0.533) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-0.adp_available.if0` (backlog-adp@verify-0) | 4.876 (6.341) | fits | 7 adp | 8 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.783 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 2.984 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.424 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 2.388 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 7.490 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-held.mrpdu.join.if0` (save-held) | 2.735 | fits | 0 srp | 3 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 3.884 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.acmp.last.if0` (backlog-adp@verify-0) | 6.720 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 3.875 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.adp.last.if0` (backlog-adp@verify-0) | 5.392 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 2.289 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.aecp.last.if0` (backlog-adp@verify-0) | 3.911 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 3.910 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 5.429 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.srp.first.if0` (backlog-adp@verify-0) | 6.750 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.srp.last.if0` (backlog-adp@verify-0) | 9.100 | fits | 31 srp | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-0 | 0 | 10.296 | 8 | 155,147 (1.551) | yes | - |
| backlog-adp@verify-0 | 0 | 11.226 | 9 | 153,411 (1.534) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.124 | 8 | 155,474 (1.555) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.028 | 8 | 152,171 (1.522) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.340 | 8 | 157,451 (1.575) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.425 | 8 | 152,478 (1.525) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.218 | 9 | 155,264 (1.553) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.602 | 10 | 157,944 (1.579) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 2772 | 0 | 160,758 (1.608) | fits |
| backlog-adp@program-0 | 938 | 0 | 155,147 (1.551) | fits |
| backlog-adp@verify-0 | 1314 | 0 | 153,411 (1.534) | fits |
| backlog-adp@blank-aged2-0 | 797 | 0 | 155,474 (1.555) | fits |
| backlog-adp@blank-aged1-1 | 753 | 0 | 152,171 (1.522) | fits |
| backlog-adp@program-aged2-0 | 1176 | 0 | 157,451 (1.575) | fits |
| backlog-adp@program-aged1-0 | 1125 | 0 | 152,478 (1.525) | fits |
| backlog-adp@verify-aged2-0 | 1557 | 0 | 155,264 (1.553) | fits |
| backlog-adp@verify-aged1-0 | 1508 | 0 | 157,944 (1.579) | fits |
| adp-advertise | 598 | 0 | 34,872 (0.349) | fits |
| acmp-cmd | 87 | 0 | 46,561 (0.466) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.356 (20) | 11.644 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.409 (20) | 11.591 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.427 (20) | 11.573 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.319 (20) | 11.681 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.332 (20) | 11.668 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.469 (20) | 11.531 |

Least margin over the aged windows: 11.531 ms, `backlog-adp@verify-aged1-0.service.srp.last.if0` at 8.469 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4817.559 | 12,470 | 382 | - | 14.655 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,381 (1.004) | 78,079 (0.781) |
| backlog-adp@program-0 | 448 | 100,322 (1.003) | 78,286 (0.783) |
| backlog-adp@verify-0 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@blank-aged2-0 | 338 | 95,952 (0.960) | 75,944 (0.759) |
| backlog-adp@blank-aged1-1 | 337 | 95,090 (0.951) | 75,893 (0.759) |
| backlog-adp@program-aged2-0 | 447 | 100,322 (1.003) | 78,436 (0.784) |
| backlog-adp@program-aged1-0 | 447 | 100,322 (1.003) | 78,354 (0.784) |
| backlog-adp@verify-aged2-0 | 556 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@verify-aged1-0 | 556 | 104,189 (1.042) | 78,074 (0.781) |
| adp-advertise | 577 | 26,071 (0.261) | 2,306 (0.023) |
| acmp-cmd | 66 | 25,989 (0.260) | 2,306 (0.023) |

Longest pass that carries a step: 104,189 CPU cycles (1.042 ms), backlog-adp@verify-0; longest step: 78,436 (0.784 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 298,448 | 2.984 | 20 | 200 | fits | 138,630 | 133 | 0.536 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 278,311 | 2.783 | 20 | 20 | fits | 138,630 | 133 | 0.536 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 242,431 | 2.424 | 20 | 24 | fits | 72,335 | 50 | 0.496 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 238,836 | 2.388 | 20 | 50 | fits | 138,630 | 133 | 0.536 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 748,996 | 7.490 | 20 | 20 | fits | 122,033 | 71 | 0.525 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 273,453 | 2.735 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 175,024 | 1.750 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 194,132 | 1.941 | 49 | 49 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 394,949 | 3.949 | 20 | 20 | fits | 155,147 | 195 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 300,859 | 3.009 | 20 | 200 | fits | 149,437 | 192 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 455,390 | 4.554 | 20 | 200 | fits | 155,147 | 195 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 301,783 | 3.018 | 20 | 20 | fits | 149,437 | 192 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 587,928 | 5.879 | 20 | 20 | fits | 131,834 | 56 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 155,986 | 1.560 | 20 | 24 | fits | 148,966 | 145 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 304,433 | 3.044 | 20 | 24 | fits | 149,437 | 192 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 304,367 | 3.044 | 20 | 50 | fits | 149,437 | 192 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 459,118 | 4.591 | 20 | 50 | fits | 155,147 | 195 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 590,886 | 5.909 | 20 | 20 | fits | 131,834 | 56 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 843,202 | 8.432 | 20 | 20 | fits | 110,153 | 48 | 0.509 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 487,573 | 4.876 | 20 | 20 | fits | 152,324 | 204 | 0.341 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 387,492 | 3.875 | 20 | 200 | fits | 153,411 | 185 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 539,200 | 5.392 | 20 | 200 | fits | 152,324 | 204 | 0.341 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 388,416 | 3.884 | 20 | 20 | fits | 153,411 | 185 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 672,035 | 6.720 | 20 | 20 | fits | 132,131 | 55 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 228,950 | 2.289 | 20 | 24 | fits | 149,731 | 146 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 391,066 | 3.911 | 20 | 24 | fits | 153,411 | 185 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 391,000 | 3.910 | 20 | 50 | fits | 153,411 | 185 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 542,928 | 5.429 | 20 | 50 | fits | 152,324 | 204 | 0.341 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 674,993 | 6.750 | 20 | 20 | fits | 132,131 | 55 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 910,011 | 9.100 | 20 | 20 | fits | 109,580 | 48 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 388,566 | 3.886 | 20 | 20 | fits | 155,474 | 196 | 0.342 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 294,473 | 2.945 | 20 | 200 | fits | 149,313 | 192 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 449,331 | 4.493 | 20 | 200 | fits | 155,474 | 196 | 0.342 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 295,397 | 2.954 | 20 | 20 | fits | 149,313 | 192 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 597,530 | 5.975 | 20 | 20 | fits | 136,987 | 62 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 149,724 | 1.497 | 20 | 24 | fits | 147,758 | 142 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 298,047 | 2.980 | 20 | 24 | fits | 149,313 | 192 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 297,981 | 2.980 | 20 | 50 | fits | 149,313 | 192 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 453,059 | 4.531 | 20 | 50 | fits | 155,474 | 196 | 0.342 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 600,488 | 6.005 | 20 | 20 | fits | 136,987 | 62 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 835,599 | 8.356 | 20 | 20 | fits | 109,772 | 48 | 0.500 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 401,058 | 4.011 | 20 | 20 | fits | 152,171 | 204 | 0.340 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 301,131 | 3.011 | 20 | 200 | fits | 150,980 | 180 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 452,686 | 4.527 | 20 | 200 | fits | 152,171 | 204 | 0.340 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 302,055 | 3.021 | 20 | 20 | fits | 150,980 | 180 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 585,753 | 5.858 | 20 | 20 | fits | 132,363 | 56 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 154,715 | 1.547 | 20 | 24 | fits | 147,749 | 142 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 304,705 | 3.047 | 20 | 24 | fits | 150,980 | 180 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 304,639 | 3.046 | 20 | 50 | fits | 150,980 | 180 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 456,414 | 4.564 | 20 | 50 | fits | 152,171 | 204 | 0.340 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 588,711 | 5.887 | 20 | 20 | fits | 132,363 | 56 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 840,908 | 8.409 | 20 | 20 | fits | 110,153 | 48 | 0.509 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 419,985 | 4.200 | 20 | 20 | fits | 157,451 | 211 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 305,006 | 3.050 | 20 | 200 | fits | 151,098 | 181 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 472,192 | 4.722 | 20 | 200 | fits | 157,451 | 211 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 305,930 | 3.059 | 20 | 20 | fits | 151,098 | 181 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 604,700 | 6.047 | 20 | 20 | fits | 131,804 | 55 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 158,472 | 1.585 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 308,580 | 3.086 | 20 | 24 | fits | 151,098 | 181 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 308,514 | 3.085 | 20 | 50 | fits | 151,098 | 181 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 475,920 | 4.759 | 20 | 50 | fits | 157,451 | 211 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 607,658 | 6.077 | 20 | 20 | fits | 131,804 | 55 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 842,692 | 8.427 | 20 | 20 | fits | 109,580 | 48 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 394,456 | 3.945 | 20 | 20 | fits | 152,478 | 205 | 0.343 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 294,466 | 2.945 | 20 | 200 | fits | 150,843 | 180 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 446,328 | 4.463 | 20 | 200 | fits | 152,478 | 205 | 0.343 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 295,390 | 2.954 | 20 | 20 | fits | 150,843 | 180 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 593,839 | 5.938 | 20 | 20 | fits | 136,299 | 62 | 0.645 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 148,187 | 1.482 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 298,040 | 2.980 | 20 | 24 | fits | 150,843 | 180 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 297,974 | 2.980 | 20 | 50 | fits | 150,843 | 180 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 450,056 | 4.501 | 20 | 50 | fits | 152,478 | 205 | 0.343 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 596,797 | 5.968 | 20 | 20 | fits | 136,299 | 62 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 831,908 | 8.319 | 20 | 20 | fits | 109,772 | 48 | 0.500 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 401,883 | 4.019 | 20 | 20 | fits | 155,264 | 195 | 0.340 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 307,718 | 3.077 | 20 | 200 | fits | 151,843 | 197 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 462,366 | 4.624 | 20 | 200 | fits | 155,264 | 195 | 0.340 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 308,642 | 3.086 | 20 | 20 | fits | 151,843 | 197 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 595,264 | 5.953 | 20 | 20 | fits | 132,194 | 55 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 150,810 | 1.508 | 20 | 24 | fits | 147,768 | 143 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 311,292 | 3.113 | 20 | 24 | fits | 151,843 | 197 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 311,226 | 3.112 | 20 | 50 | fits | 151,843 | 197 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 466,094 | 4.661 | 20 | 50 | fits | 155,264 | 195 | 0.340 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 598,222 | 5.982 | 20 | 20 | fits | 132,194 | 55 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 833,240 | 8.332 | 20 | 20 | fits | 109,580 | 48 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 406,512 | 4.065 | 20 | 20 | fits | 157,944 | 212 | 0.389 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 308,244 | 3.082 | 20 | 200 | fits | 151,176 | 181 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 475,923 | 4.759 | 20 | 200 | fits | 157,944 | 212 | 0.389 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 309,168 | 3.092 | 20 | 20 | fits | 151,176 | 181 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 608,861 | 6.089 | 20 | 20 | fits | 132,234 | 55 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 161,632 | 1.616 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 311,818 | 3.118 | 20 | 24 | fits | 151,176 | 181 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 311,752 | 3.118 | 20 | 50 | fits | 151,176 | 181 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 479,651 | 4.797 | 20 | 50 | fits | 157,944 | 212 | 0.389 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 611,819 | 6.118 | 20 | 20 | fits | 132,234 | 55 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 846,911 | 8.469 | 20 | 20 | fits | 109,580 | 48 | 0.495 |
| LINK_UP | `adp.link_up.if0` | 2,856 | 0.029 | 20 | 200 | fits | 33,635 | 43 (11) | 0.730 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,239 | 0.142 | 20 | 200 | fits | 27,591 | 23 (39) | 0.747 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 9,779 | 0.098 | 20 | 200 | fits | 3,100 | 10 (11) | 0.538 |
| BIND_RX | `acmp.bind_rx.if0` | 20,680 | 0.207 | 20 | 20 | fits | 46,561 | 26 (77) | 0.790 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,482 | 0.105 | 20 | 20 | fits | 35,071 | 20 (32) | 0.827 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,287 | 0.113 | 20 | 20 | fits | 30,539 | 15 (47) | 0.779 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 15,441 | 0.154 | 20 | 20 | fits | 42,298 | 18 (50) | 0.834 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,978 | 0.110 | 20 | 20 | fits | 30,286 | 17 (48) | 0.757 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,622 | 0.106 | 20 | 20 | fits | 29,019 | 16 (48) | 0.727 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,384 | 0.094 | 20 | 20 | fits | 28,222 | 17 (48) | 0.714 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 10,602 | 0.106 | 20 | 20 | fits | 29,588 | 16 (48) | 0.760 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
