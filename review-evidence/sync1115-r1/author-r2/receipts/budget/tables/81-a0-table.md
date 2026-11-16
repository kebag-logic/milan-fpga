### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 24 paths and 7 of 213 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.204 (0.458) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.152 (0.361) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.113 (0.307) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.100 (0.286) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.103 (0.291) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.107 (0.304) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.114 (0.352) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.165 (0.433) | fits | 0 acmp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.027 (0.206) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.030 (0.337) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.150 (0.535) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-6.adp_available.if0` (backlog-adp@verify-aged2-6) | 4.284 (4.845) | fits | 7 adp | 17 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.514 (63.889) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.510 (64.872) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-2.service.acmp.first.if0` (backlog-adp@blank-aged2-2) | 3.233 | fits | 0 acmp | 18 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.389 | MISS ceiling | 11 acmp | 18 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-2.service.adp.first.if0` (backlog-adp@blank-aged2-2) | 3.224 | fits | 0 adp | 18 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-2.service.adp.last.if0` (backlog-adp@blank-aged2-2) | 4.777 | fits | 7 adp | 18 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.aecp.first.if0` (backlog-adp@verify-aged2-6) | 1.698 | fits | 0 aecp | 18 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.039 | MISS ceiling | 15 aecp | 18 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-2.service.maap.first.if0` (backlog-adp@blank-aged2-2) | 3.259 | fits | 0 maap | 18 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-2.service.maap.last.if0` (backlog-adp@blank-aged2-2) | 4.815 | fits | 6 maap | 18 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 6.350 | fits | 0 srp | 18 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-2.service.srp.last.if0` (backlog-adp@blank-aged2-2) | 10.214 | fits | 31 srp | 18 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-6 | 1 | 10.580 | 9 | 155,489 (1.555) | yes | - |
| backlog-adp@program-2 | 0 | 10.602 | 9 | 155,705 (1.557) | yes | - |
| backlog-adp@program-6 | 0 | 9.984 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@verify-2 | 0 | 10.690 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@verify-6 | 0 | 10.735 | 11 | 155,568 (1.556) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.851 | 11 | 155,980 (1.560) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.655 | 10 | 157,775 (1.578) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 10.577 | 10 | 152,595 (1.526) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.726 | 10 | 154,944 (1.549) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.312 | 8 | 158,582 (1.586) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.728 | 10 | 150,425 (1.504) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.725 | 11 | 158,628 (1.586) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.612 | 10 | 157,236 (1.572) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.703 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.813 | 11 | 155,568 (1.556) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.530 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@verify-aged1-6 | 1 | 10.539 | 9 | 158,214 (1.582) | yes | - |
| backlog-owed | 0 | 65.309 | 24 | 153,953 (1.540) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 153,953 CPU cycles (1.540 ms), backlog-owed.
Over the windows that released their whole load only: 153,953 (1.540 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 121789 | 0 | 53,996 (0.540) | fits |
| backlog-adp@blank-6 | 538 | 0 | 155,489 (1.555) | fits |
| backlog-adp@program-2 | 895 | 0 | 155,705 (1.557) | fits |
| backlog-adp@program-6 | 898 | 0 | 156,507 (1.565) | fits |
| backlog-adp@verify-2 | 1243 | 0 | 156,507 (1.565) | fits |
| backlog-adp@verify-6 | 1245 | 0 | 155,568 (1.556) | fits |
| backlog-adp@blank-aged2-2 | 793 | 0 | 155,980 (1.560) | fits |
| backlog-adp@blank-aged2-6 | 817 | 0 | 157,775 (1.578) | fits |
| backlog-adp@blank-aged1-2 | 741 | 0 | 152,595 (1.526) | fits |
| backlog-adp@blank-aged1-6 | 767 | 0 | 154,944 (1.549) | fits |
| backlog-adp@program-aged2-2 | 1142 | 0 | 158,582 (1.586) | fits |
| backlog-adp@program-aged2-6 | 1169 | 0 | 150,425 (1.504) | fits |
| backlog-adp@program-aged1-2 | 1094 | 0 | 158,628 (1.586) | fits |
| backlog-adp@program-aged1-6 | 1118 | 0 | 157,236 (1.572) | fits |
| backlog-adp@verify-aged2-2 | 1497 | 0 | 156,507 (1.565) | fits |
| backlog-adp@verify-aged2-6 | 1523 | 0 | 155,568 (1.556) | fits |
| backlog-adp@verify-aged1-2 | 1446 | 0 | 156,507 (1.565) | fits |
| backlog-adp@verify-aged1-6 | 1471 | 0 | 158,214 (1.582) | fits |
| save | 610 | 0 | 48,154 (0.482) | fits |
| backlog-owed | 309 | 0 | 153,953 (1.540) | fits |
| adp-gm | 88 | 0 | 33,705 (0.337) | fits |
| acmp-cmd | 87 | 0 | 45,817 (0.458) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-2 | 2 | +8.148 ms, 76,795 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.214 (20) | 9.786 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.013 (20) | 9.987 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.177 (20) | 10.823 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.332 (20) | 10.668 |
| backlog-adp@program-aged2-2 | 2 | +8.062 ms, 80,268 (0.803 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.669 (20) | 10.331 |
| backlog-adp@program-aged2-6 | 2 | +4.718 ms, 80,262 (0.803 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.085 (20) | 9.915 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.948 (20) | 11.052 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.169 (20) | 10.831 |
| backlog-adp@verify-aged2-2 | 2 | +8.068 ms, 77,668 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.063 (20) | 9.937 |
| backlog-adp@verify-aged2-6 | 2 | +4.763 ms, 77,792 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.177 (20) | 9.823 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.127 (20) | 10.873 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.130 (20) | 10.870 |

Least margin over the aged windows: 9.786 ms, `backlog-adp@blank-aged2-2.service.srp.last.if0` at 10.214 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.537 | 22,870 | 382 | 2 | 31.396 | yes | within |
| save | 4818.810 | 12,470 | 382 | - | 10.859 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 80,751 (0.808) | 77,471 (0.775) |
| backlog-adp@blank-6 | 339 | 95,740 (0.957) | 76,146 (0.761) |
| backlog-adp@program-2 | 448 | 100,633 (1.006) | 78,390 (0.784) |
| backlog-adp@program-6 | 449 | 100,633 (1.006) | 77,865 (0.779) |
| backlog-adp@verify-2 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-6 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@blank-aged2-2 | 337 | 79,331 (0.793) | 75,650 (0.756) |
| backlog-adp@blank-aged2-6 | 337 | 86,218 (0.862) | 75,633 (0.756) |
| backlog-adp@blank-aged1-2 | 337 | 96,251 (0.963) | 76,173 (0.762) |
| backlog-adp@blank-aged1-6 | 337 | 95,767 (0.958) | 76,224 (0.762) |
| backlog-adp@program-aged2-2 | 446 | 100,633 (1.006) | 77,960 (0.780) |
| backlog-adp@program-aged2-6 | 446 | 100,633 (1.006) | 77,865 (0.779) |
| backlog-adp@program-aged1-2 | 446 | 100,633 (1.006) | 78,306 (0.783) |
| backlog-adp@program-aged1-6 | 446 | 100,633 (1.006) | 78,388 (0.784) |
| backlog-adp@verify-aged2-2 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged2-6 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged1-2 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged1-6 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| save | 585 | 100,580 (1.006) | 77,655 (0.777) |
| backlog-owed | 277 | 26,258 (0.263) | 2,254 (0.023) |
| adp-gm | 79 | 26,196 (0.262) | 2,254 (0.023) |
| acmp-cmd | 66 | 26,196 (0.262) | 2,340 (0.023) |

Longest pass that carries a step: 104,368 CPU cycles (1.044 ms), backlog-adp@verify-2; longest step: 78,390 (0.784 ms), backlog-adp@program-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 406,331 | 4.063 | 20 | 20 | fits | 155,489 | 205 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 293,921 | 2.939 | 20 | 200 | fits | 151,768 | 181 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 448,794 | 4.488 | 20 | 200 | fits | 155,489 | 205 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 294,845 | 2.948 | 20 | 20 | fits | 151,768 | 181 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 532,256 | 5.323 | 20 | 20 | fits | 82,758 | 37 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 146,717 | 1.467 | 20 | 24 | fits | 148,362 | 145 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 297,495 | 2.975 | 20 | 24 | fits | 151,768 | 181 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 297,429 | 2.974 | 20 | 50 | fits | 151,768 | 181 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 452,522 | 4.525 | 20 | 50 | fits | 155,489 | 205 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 535,214 | 5.352 | 20 | 20 | fits | 82,758 | 37 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 918,517 | 9.185 | 20 | 20 | fits | 42,331 | 17 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 379,418 | 3.794 | 20 | 20 | fits | 155,705 | 205 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 295,115 | 2.951 | 20 | 200 | fits | 152,161 | 180 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 450,204 | 4.502 | 20 | 200 | fits | 155,705 | 205 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 296,039 | 2.960 | 20 | 20 | fits | 152,161 | 180 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 539,581 | 5.396 | 20 | 20 | fits | 88,673 | 39 | 0.748 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 147,518 | 1.475 | 20 | 24 | fits | 148,019 | 145 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 298,689 | 2.987 | 20 | 24 | fits | 152,161 | 180 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 298,623 | 2.986 | 20 | 50 | fits | 152,161 | 180 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 453,932 | 4.539 | 20 | 50 | fits | 155,705 | 205 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 542,539 | 5.425 | 20 | 20 | fits | 88,673 | 39 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 916,357 | 9.164 | 20 | 20 | fits | 32,968 | 12 | 0.833 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 411,408 | 4.114 | 20 | 20 | fits | 156,507 | 209 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 307,601 | 3.076 | 20 | 200 | fits | 150,474 | 176 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 463,492 | 4.635 | 20 | 200 | fits | 156,507 | 209 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 308,525 | 3.085 | 20 | 20 | fits | 150,474 | 176 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 552,798 | 5.528 | 20 | 20 | fits | 88,602 | 39 | 0.748 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 161,691 | 1.617 | 20 | 24 | fits | 148,186 | 145 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 311,175 | 3.112 | 20 | 24 | fits | 150,474 | 176 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 311,109 | 3.111 | 20 | 50 | fits | 150,474 | 176 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 467,220 | 4.672 | 20 | 50 | fits | 156,507 | 209 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 555,756 | 5.558 | 20 | 20 | fits | 88,602 | 39 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 929,741 | 9.297 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 410,393 | 4.104 | 20 | 20 | fits | 156,507 | 209 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 306,586 | 3.066 | 20 | 200 | fits | 150,610 | 176 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 462,477 | 4.625 | 20 | 200 | fits | 156,507 | 209 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 307,510 | 3.075 | 20 | 20 | fits | 150,610 | 176 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 545,257 | 5.453 | 20 | 20 | fits | 82,076 | 32 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 160,540 | 1.605 | 20 | 24 | fits | 148,309 | 145 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 310,160 | 3.102 | 20 | 24 | fits | 150,610 | 176 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 310,094 | 3.101 | 20 | 50 | fits | 150,610 | 176 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 466,205 | 4.662 | 20 | 50 | fits | 156,507 | 209 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 548,215 | 5.482 | 20 | 20 | fits | 82,076 | 32 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 928,614 | 9.286 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 421,865 | 4.219 | 20 | 20 | fits | 155,568 | 205 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 309,378 | 3.094 | 20 | 200 | fits | 150,695 | 176 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 464,330 | 4.643 | 20 | 200 | fits | 155,568 | 205 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 310,302 | 3.103 | 20 | 20 | fits | 150,695 | 176 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 547,709 | 5.477 | 20 | 20 | fits | 82,675 | 37 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 163,247 | 1.632 | 20 | 24 | fits | 148,092 | 146 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 312,952 | 3.130 | 20 | 24 | fits | 150,695 | 176 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 312,886 | 3.129 | 20 | 50 | fits | 150,695 | 176 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 468,058 | 4.681 | 20 | 50 | fits | 155,568 | 205 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 550,667 | 5.507 | 20 | 20 | fits | 82,675 | 37 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 933,040 | 9.330 | 20 | 20 | fits | 41,573 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 406,860 | 4.069 | 20 | 20 | fits | 155,980 | 205 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 322,375 | 3.224 | 20 | 200 | fits | 154,177 | 185 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 477,739 | 4.777 | 20 | 200 | fits | 155,980 | 205 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 323,299 | 3.233 | 20 | 20 | fits | 154,177 | 185 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 560,761 | 5.608 | 20 | 20 | fits | 82,318 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 163,009 | 1.630 | 20 | 24 | fits | 147,289 | 143 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 325,949 | 3.259 | 20 | 24 | fits | 154,177 | 185 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 325,883 | 3.259 | 20 | 50 | fits | 154,177 | 185 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 481,467 | 4.815 | 20 | 50 | fits | 155,980 | 205 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 563,719 | 5.637 | 20 | 20 | fits | 82,318 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,021,368 | 10.214 | 20 | 20 | fits | 42,331 | 17 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 404,738 | 4.047 | 20 | 20 | fits | 157,775 | 192 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 300,419 | 3.004 | 20 | 200 | fits | 149,915 | 192 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 457,578 | 4.576 | 20 | 200 | fits | 157,775 | 192 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 301,343 | 3.013 | 20 | 20 | fits | 149,915 | 192 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 632,033 | 6.320 | 20 | 20 | fits | 87,533 | 44 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 155,068 | 1.551 | 20 | 24 | fits | 147,168 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 303,993 | 3.040 | 20 | 24 | fits | 149,915 | 192 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 303,927 | 3.039 | 20 | 50 | fits | 149,915 | 192 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 461,306 | 4.613 | 20 | 50 | fits | 157,775 | 192 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 634,991 | 6.350 | 20 | 20 | fits | 87,533 | 44 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,001,305 | 10.013 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 396,248 | 3.962 | 20 | 20 | fits | 150,900 | 203 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 297,667 | 2.977 | 20 | 200 | fits | 152,595 | 181 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 458,123 | 4.581 | 20 | 200 | fits | 150,900 | 203 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 298,591 | 2.986 | 20 | 20 | fits | 152,595 | 181 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 541,940 | 5.419 | 20 | 20 | fits | 83,113 | 37 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 149,636 | 1.496 | 20 | 24 | fits | 147,168 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 301,241 | 3.012 | 20 | 24 | fits | 152,595 | 181 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 301,175 | 3.012 | 20 | 50 | fits | 152,595 | 181 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 461,851 | 4.619 | 20 | 50 | fits | 150,900 | 203 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 544,898 | 5.449 | 20 | 20 | fits | 83,113 | 37 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 917,665 | 9.177 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 402,613 | 4.026 | 20 | 20 | fits | 154,944 | 201 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 309,534 | 3.095 | 20 | 200 | fits | 152,308 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 463,862 | 4.639 | 20 | 200 | fits | 154,944 | 201 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 310,458 | 3.105 | 20 | 20 | fits | 152,308 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 547,647 | 5.476 | 20 | 20 | fits | 83,081 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 161,790 | 1.618 | 20 | 24 | fits | 147,121 | 142 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 313,108 | 3.131 | 20 | 24 | fits | 152,308 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 313,042 | 3.130 | 20 | 50 | fits | 152,308 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 467,590 | 4.676 | 20 | 50 | fits | 154,944 | 201 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 550,605 | 5.506 | 20 | 20 | fits | 83,081 | 37 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 933,173 | 9.332 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 386,162 | 3.862 | 20 | 20 | fits | 158,582 | 226 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 290,278 | 2.903 | 20 | 200 | fits | 149,755 | 198 | 0.415 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 448,244 | 4.482 | 20 | 200 | fits | 158,582 | 226 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 291,202 | 2.912 | 20 | 20 | fits | 149,755 | 198 | 0.415 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 539,046 | 5.390 | 20 | 20 | fits | 90,098 | 35 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 145,087 | 1.451 | 20 | 24 | fits | 149,079 | 111 | 0.365 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 293,852 | 2.939 | 20 | 24 | fits | 149,755 | 198 | 0.415 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 293,786 | 2.938 | 20 | 50 | fits | 149,755 | 198 | 0.415 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 451,972 | 4.520 | 20 | 50 | fits | 158,582 | 226 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 542,004 | 5.420 | 20 | 20 | fits | 90,098 | 35 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 966,869 | 9.669 | 20 | 20 | fits | 84,130 | 37 | 0.549 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 423,493 | 4.235 | 20 | 20 | fits | 150,425 | 190 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 306,436 | 3.064 | 20 | 200 | fits | 150,020 | 193 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 466,410 | 4.664 | 20 | 200 | fits | 150,425 | 190 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 307,360 | 3.074 | 20 | 20 | fits | 150,020 | 193 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 630,658 | 6.307 | 20 | 20 | fits | 83,282 | 43 | 0.699 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 160,980 | 1.610 | 20 | 24 | fits | 147,000 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 310,010 | 3.100 | 20 | 24 | fits | 150,020 | 193 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 309,944 | 3.099 | 20 | 50 | fits | 150,020 | 193 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 470,138 | 4.701 | 20 | 50 | fits | 150,425 | 190 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 633,616 | 6.336 | 20 | 20 | fits | 83,282 | 43 | 0.699 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,008,489 | 10.085 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 407,140 | 4.071 | 20 | 20 | fits | 158,628 | 195 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 311,387 | 3.114 | 20 | 200 | fits | 151,667 | 197 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 469,399 | 4.694 | 20 | 200 | fits | 158,628 | 195 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 312,311 | 3.123 | 20 | 20 | fits | 151,667 | 197 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 560,233 | 5.602 | 20 | 20 | fits | 90,130 | 35 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 154,474 | 1.545 | 20 | 24 | fits | 147,177 | 143 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 314,961 | 3.150 | 20 | 24 | fits | 151,667 | 197 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 314,895 | 3.149 | 20 | 50 | fits | 151,667 | 197 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 473,127 | 4.731 | 20 | 50 | fits | 158,628 | 195 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 563,191 | 5.632 | 20 | 20 | fits | 90,130 | 35 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 894,826 | 8.948 | 20 | 20 | fits | 84,314 | 37 | 0.548 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 397,701 | 3.977 | 20 | 20 | fits | 157,236 | 193 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 293,495 | 2.935 | 20 | 200 | fits | 150,006 | 192 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 450,115 | 4.501 | 20 | 200 | fits | 157,236 | 193 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 294,419 | 2.944 | 20 | 20 | fits | 150,006 | 192 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 547,667 | 5.477 | 20 | 20 | fits | 86,391 | 44 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 148,053 | 1.481 | 20 | 24 | fits | 147,047 | 142 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 297,069 | 2.971 | 20 | 24 | fits | 150,006 | 192 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 297,003 | 2.970 | 20 | 50 | fits | 150,006 | 192 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 453,843 | 4.538 | 20 | 50 | fits | 157,236 | 193 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 550,625 | 5.506 | 20 | 20 | fits | 86,391 | 44 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 916,925 | 9.169 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 410,436 | 4.104 | 20 | 20 | fits | 156,507 | 209 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 306,629 | 3.066 | 20 | 200 | fits | 150,685 | 176 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 462,520 | 4.625 | 20 | 200 | fits | 156,507 | 209 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 307,553 | 3.076 | 20 | 20 | fits | 150,685 | 176 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 545,300 | 5.453 | 20 | 20 | fits | 82,076 | 32 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 160,508 | 1.605 | 20 | 24 | fits | 147,023 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 310,203 | 3.102 | 20 | 24 | fits | 150,685 | 176 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 310,137 | 3.101 | 20 | 50 | fits | 150,685 | 176 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 466,248 | 4.662 | 20 | 50 | fits | 156,507 | 209 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 548,258 | 5.483 | 20 | 20 | fits | 82,076 | 32 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,006,268 | 10.063 | 20 | 20 | fits | 41,125 | 16 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 428,449 | 4.284 | 20 | 20 | fits | 155,568 | 205 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 315,962 | 3.160 | 20 | 200 | fits | 150,692 | 176 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 470,914 | 4.709 | 20 | 200 | fits | 155,568 | 205 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 316,886 | 3.169 | 20 | 20 | fits | 150,692 | 176 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 631,987 | 6.320 | 20 | 20 | fits | 82,577 | 38 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 169,834 | 1.698 | 20 | 24 | fits | 147,179 | 143 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 319,536 | 3.195 | 20 | 24 | fits | 150,692 | 176 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 319,470 | 3.195 | 20 | 50 | fits | 150,692 | 176 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 474,642 | 4.746 | 20 | 50 | fits | 155,568 | 205 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 634,945 | 6.349 | 20 | 20 | fits | 82,577 | 38 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,017,650 | 10.177 | 20 | 20 | fits | 41,164 | 16 | 0.751 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 397,342 | 3.973 | 20 | 20 | fits | 156,507 | 209 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 293,535 | 2.935 | 20 | 200 | fits | 150,685 | 176 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 449,426 | 4.494 | 20 | 200 | fits | 156,507 | 209 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 294,459 | 2.945 | 20 | 20 | fits | 150,685 | 176 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 532,156 | 5.322 | 20 | 20 | fits | 82,026 | 31 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 147,414 | 1.474 | 20 | 24 | fits | 146,958 | 142 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 297,109 | 2.971 | 20 | 24 | fits | 150,685 | 176 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 297,043 | 2.970 | 20 | 50 | fits | 150,685 | 176 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 453,154 | 4.532 | 20 | 50 | fits | 156,507 | 209 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 535,114 | 5.351 | 20 | 20 | fits | 82,026 | 31 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 912,693 | 9.127 | 20 | 20 | fits | 32,570 | 12 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 417,349 | 4.173 | 20 | 20 | fits | 158,214 | 211 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 292,591 | 2.926 | 20 | 200 | fits | 151,984 | 182 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 460,315 | 4.603 | 20 | 200 | fits | 158,214 | 211 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 293,515 | 2.935 | 20 | 20 | fits | 151,984 | 182 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 543,784 | 5.438 | 20 | 20 | fits | 82,765 | 37 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 145,171 | 1.452 | 20 | 24 | fits | 146,958 | 142 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 296,165 | 2.962 | 20 | 24 | fits | 151,984 | 182 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 296,099 | 2.961 | 20 | 50 | fits | 151,984 | 182 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 464,043 | 4.640 | 20 | 50 | fits | 158,214 | 211 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 546,742 | 5.467 | 20 | 20 | fits | 82,765 | 37 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 913,002 | 9.130 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,351,429 | 63.514 | 20 | 20 | MISS ceiling | 23,821 | 13 | 0.639 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,375,175 | 63.752 | 20 | 20 | MISS ceiling | 23,822 | 13 | 0.605 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,398,924 | 63.989 | 20 | 20 | MISS ceiling | 23,806 | 13 | 0.605 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,422,585 | 64.226 | 20 | 20 | MISS ceiling | 23,737 | 13 | 0.613 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,451,032 | 64.510 | 20 | 20 | MISS ceiling | 27,260 | 18 | 0.743 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 160,896 | 1.609 | 20 | 200 | fits | 153,953 | 177 | 0.455 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 291,760 | 2.918 | 20 | 200 | fits | 131,480 | 207 | 0.379 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 156,574 | 1.566 | 20 | 20 | fits | 153,953 | 177 | 0.455 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,238,917 | 62.389 | 20 | 20 | MISS ceiling | 38,510 | 15 | 0.764 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 160,214 | 1.602 | 20 | 24 | fits | 153,953 | 177 | 0.455 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,203,893 | 62.039 | 20 | 24 | MISS ceiling | 152,725 | 106 | 0.402 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 159,158 | 1.592 | 20 | 50 | fits | 153,953 | 177 | 0.455 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 290,242 | 2.902 | 20 | 50 | fits | 131,480 | 207 | 0.379 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 379,012 | 3.790 | 20 | 20 | fits | 88,836 | 32 | 0.696 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 701,791 | 7.018 | 20 | 20 | fits | 75,331 | 32 | 0.551 |
| LINK_UP | `adp.link_up.if0` | 2,986 | 0.030 | 20 | 200 | fits | 33,705 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,035 | 0.150 | 20 | 200 | fits | 26,764 | 23 (39) | 0.725 |
| GM_CHANGE | `adp.gm_change.if0` | 2,726 | 0.027 | 20 | 200 | fits | 20,622 | 17 (11) | 0.744 |
| BIND_RX | `acmp.bind_rx.if0` | 20,356 | 0.204 | 20 | 20 | fits | 45,817 | 26 (77) | 0.786 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 11,351 | 0.114 | 20 | 20 | fits | 35,212 | 19 (32) | 0.827 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,262 | 0.113 | 20 | 20 | fits | 30,700 | 16 (47) | 0.778 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 16,511 | 0.165 | 20 | 20 | fits | 43,271 | 18 (50) | 0.841 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,717 | 0.107 | 20 | 20 | fits | 30,435 | 17 (48) | 0.752 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,294 | 0.103 | 20 | 20 | fits | 29,113 | 16 (48) | 0.727 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 15,177 | 0.152 | 20 | 20 | fits | 36,115 | 24 (48) | 0.742 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 10,035 | 0.100 | 20 | 20 | fits | 28,596 | 16 (48) | 0.729 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
