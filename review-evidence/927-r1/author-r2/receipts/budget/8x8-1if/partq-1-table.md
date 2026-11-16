### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 28 paths and 7 of 151 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.207 (0.468) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.107 (0.302) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.111 (0.305) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.099 (0.288) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.100 (0.293) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.113 (0.307) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.108 (0.350) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.161 (0.429) | fits | 0 acmp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.028 (0.207) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.030 (0.338) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.206 (0.598) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 5.099 (5.612) | fits | 7 adp | 11 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.513 (63.699) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.512 (64.701) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-aged1-3.service.acmp.first.if0` (backlog-adp@program-aged1-3) | 3.120 | fits | 0 acmp | 12 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.380 | MISS ceiling | 11 acmp | 12 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-aged1-3.service.adp.first.if0` (backlog-adp@program-aged1-3) | 3.111 | fits | 0 adp | 12 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.435 | fits | 7 adp | 12 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.584 | fits | 0 aecp | 12 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.030 | MISS ceiling | 15 aecp | 12 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-aged1-3.service.maap.first.if0` (backlog-adp@program-aged1-3) | 3.146 | fits | 0 maap | 12 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.472 | fits | 6 maap | 12 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 6.318 | fits | 0 srp | 12 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-5.service.srp.last.if0` (backlog-adp@blank-aged2-5) | 10.137 | fits | 31 srp | 12 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.786 (0.831) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.443 (0.443) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.231 (0.232) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.797 (0.867) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-aged2-5 | 0 | 10.785 | 10 | 151,453 (1.515) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.547 | 12 | 153,415 (1.534) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 10.681 | 9 | 157,165 (1.572) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.730 | 10 | 151,581 (1.516) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.777 | 10 | 154,728 (1.547) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.864 | 11 | 152,264 (1.523) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.751 | 10 | 158,779 (1.588) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.754 | 10 | 157,031 (1.570) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 10.700 | 9 | 157,167 (1.572) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.716 | 10 | 151,635 (1.516) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.443 | 12 | 154,086 (1.541) | yes | - |
| backlog-owed | 0 | 65.318 | 24 | 154,925 (1.549) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 154,925 CPU cycles (1.549 ms), backlog-owed.
Over the windows that released their whole load only: 154,925 (1.549 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-aged2-5 | 827 | 0 | 151,453 (1.515) | fits |
| backlog-adp@blank-aged1-3 | 766 | 0 | 153,415 (1.534) | fits |
| backlog-adp@blank-aged1-7 | 789 | 0 | 157,165 (1.572) | fits |
| backlog-adp@program-aged2-3 | 1194 | 0 | 151,581 (1.516) | fits |
| backlog-adp@program-aged2-7 | 1219 | 0 | 154,728 (1.547) | fits |
| backlog-adp@program-aged1-3 | 1145 | 0 | 152,264 (1.523) | fits |
| backlog-adp@program-aged1-7 | 1169 | 0 | 158,779 (1.588) | fits |
| backlog-adp@verify-aged2-3 | 1574 | 0 | 157,031 (1.570) | fits |
| backlog-adp@verify-aged2-7 | 1599 | 0 | 157,167 (1.572) | fits |
| backlog-adp@verify-aged1-3 | 1524 | 0 | 151,635 (1.516) | fits |
| backlog-adp@verify-aged1-7 | 1551 | 0 | 154,086 (1.541) | fits |
| srp | 290 | 0 | 44,339 (0.443) | fits |
| backlog-owed | 309 | 0 | 154,925 (1.549) | fits |
| adp-gm | 88 | 0 | 33,791 (0.338) | fits |
| acmp-cmd | 87 | 0 | 46,812 (0.468) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-5 | 2 | +5.414 ms, 76,861 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.137 (20) | 9.863 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.250 (20) | 10.750 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.274 (20) | 10.726 |
| backlog-adp@program-aged2-3 | 2 | none | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.083 (20) | 9.917 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.124 (20) | 9.876 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.415 (20) | 10.585 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.293 (20) | 10.707 |
| backlog-adp@verify-aged2-3 | 2 | +6.474 ms, 77,639 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.105 (20) | 9.895 |
| backlog-adp@verify-aged2-7 | 2 | +4.580 ms, 77,559 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.053 (20) | 9.947 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.302 (20) | 10.698 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.338 (20) | 10.662 |

Least margin over the aged windows: 9.863 ms, `backlog-adp@blank-aged2-5.service.srp.last.if0` at 10.137 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-aged2-5 | 337 | 79,578 (0.796) | 75,730 (0.757) |
| backlog-adp@blank-aged1-3 | 337 | 96,769 (0.968) | 76,201 (0.762) |
| backlog-adp@blank-aged1-7 | 337 | 96,188 (0.962) | 76,252 (0.763) |
| backlog-adp@program-aged2-3 | 446 | 100,997 (1.010) | 78,520 (0.785) |
| backlog-adp@program-aged2-7 | 446 | 100,997 (1.010) | 78,197 (0.782) |
| backlog-adp@program-aged1-3 | 446 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@program-aged1-7 | 446 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@verify-aged2-3 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-7 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-3 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-7 | 556 | 104,873 (1.049) | 78,338 (0.783) |
| srp | 271 | 26,388 (0.264) | 2,374 (0.024) |
| backlog-owed | 277 | 26,388 (0.264) | 2,374 (0.024) |
| adp-gm | 79 | 26,162 (0.262) | 2,374 (0.024) |
| acmp-cmd | 66 | 26,162 (0.262) | 2,374 (0.024) |

Longest pass that carries a step: 104,873 CPU cycles (1.049 ms), backlog-adp@verify-aged2-3; longest step: 78,776 (0.788 ms), backlog-adp@program-aged1-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 409,802 | 4.098 | 20 | 20 | fits | 149,301 | 201 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 304,464 | 3.045 | 20 | 200 | fits | 151,453 | 176 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 453,149 | 4.531 | 20 | 200 | fits | 149,301 | 201 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 305,388 | 3.054 | 20 | 20 | fits | 151,453 | 176 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 536,742 | 5.367 | 20 | 20 | fits | 82,889 | 41 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 157,575 | 1.576 | 20 | 24 | fits | 148,207 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 308,038 | 3.080 | 20 | 24 | fits | 151,453 | 176 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 307,972 | 3.080 | 20 | 50 | fits | 151,453 | 176 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 456,877 | 4.569 | 20 | 50 | fits | 149,301 | 201 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 539,700 | 5.397 | 20 | 20 | fits | 82,889 | 41 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,013,730 | 10.137 | 20 | 20 | fits | 50,192 | 20 | 0.703 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 414,628 | 4.146 | 20 | 20 | fits | 151,353 | 201 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 297,988 | 2.980 | 20 | 200 | fits | 153,415 | 181 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 458,992 | 4.590 | 20 | 200 | fits | 151,353 | 201 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 298,912 | 2.989 | 20 | 20 | fits | 153,415 | 181 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 543,761 | 5.438 | 20 | 20 | fits | 84,065 | 37 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 149,137 | 1.491 | 20 | 24 | fits | 148,058 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 301,562 | 3.016 | 20 | 24 | fits | 153,415 | 181 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 301,496 | 3.015 | 20 | 50 | fits | 153,415 | 181 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 462,720 | 4.627 | 20 | 50 | fits | 151,353 | 201 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 546,719 | 5.467 | 20 | 20 | fits | 84,065 | 37 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 925,028 | 9.250 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 390,512 | 3.905 | 20 | 20 | fits | 157,165 | 201 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 296,070 | 2.961 | 20 | 200 | fits | 154,318 | 185 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 452,619 | 4.526 | 20 | 200 | fits | 157,165 | 201 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 296,994 | 2.970 | 20 | 20 | fits | 154,318 | 185 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 537,310 | 5.373 | 20 | 20 | fits | 83,987 | 37 | 0.734 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 146,316 | 1.463 | 20 | 24 | fits | 148,184 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 299,644 | 2.996 | 20 | 24 | fits | 154,318 | 185 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 299,578 | 2.996 | 20 | 50 | fits | 154,318 | 185 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 456,347 | 4.563 | 20 | 50 | fits | 157,165 | 201 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 540,268 | 5.403 | 20 | 20 | fits | 83,987 | 37 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 927,442 | 9.274 | 20 | 20 | fits | 41,476 | 16 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 405,165 | 4.052 | 20 | 20 | fits | 149,301 | 201 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 299,827 | 2.998 | 20 | 200 | fits | 151,581 | 176 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 448,512 | 4.485 | 20 | 200 | fits | 149,301 | 201 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 300,751 | 3.008 | 20 | 20 | fits | 151,581 | 176 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 532,081 | 5.321 | 20 | 20 | fits | 82,865 | 37 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 152,810 | 1.528 | 20 | 24 | fits | 148,006 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 303,401 | 3.034 | 20 | 24 | fits | 151,581 | 176 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 303,335 | 3.033 | 20 | 50 | fits | 151,581 | 176 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 452,240 | 4.522 | 20 | 50 | fits | 149,301 | 201 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 535,039 | 5.350 | 20 | 20 | fits | 82,865 | 37 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,008,290 | 10.083 | 20 | 20 | fits | 50,192 | 20 | 0.703 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 509,931 | 5.099 | 20 | 20 | fits | 154,728 | 208 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 299,922 | 2.999 | 20 | 200 | fits | 148,861 | 171 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 543,482 | 5.435 | 20 | 200 | fits | 154,728 | 208 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 300,846 | 3.008 | 20 | 20 | fits | 148,861 | 171 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 628,860 | 6.289 | 20 | 20 | fits | 84,674 | 42 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 155,625 | 1.556 | 20 | 24 | fits | 148,071 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 303,496 | 3.035 | 20 | 24 | fits | 148,861 | 171 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 303,430 | 3.034 | 20 | 50 | fits | 148,861 | 171 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 547,210 | 5.472 | 20 | 50 | fits | 154,728 | 208 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 631,818 | 6.318 | 20 | 20 | fits | 84,674 | 42 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,012,410 | 10.124 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 408,078 | 4.081 | 20 | 20 | fits | 150,800 | 185 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 311,103 | 3.111 | 20 | 200 | fits | 152,264 | 197 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 461,287 | 4.613 | 20 | 200 | fits | 150,800 | 185 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 312,027 | 3.120 | 20 | 20 | fits | 152,264 | 197 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 545,065 | 5.451 | 20 | 20 | fits | 83,074 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 153,527 | 1.535 | 20 | 24 | fits | 148,238 | 143 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 314,677 | 3.147 | 20 | 24 | fits | 152,264 | 197 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 314,611 | 3.146 | 20 | 50 | fits | 152,264 | 197 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 465,015 | 4.650 | 20 | 50 | fits | 150,800 | 185 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 548,023 | 5.480 | 20 | 20 | fits | 83,074 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 941,502 | 9.415 | 20 | 20 | fits | 46,108 | 23 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 402,424 | 4.024 | 20 | 20 | fits | 158,779 | 209 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 297,422 | 2.974 | 20 | 200 | fits | 149,824 | 174 | 0.445 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 455,585 | 4.556 | 20 | 200 | fits | 158,779 | 209 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 298,346 | 2.983 | 20 | 20 | fits | 149,824 | 174 | 0.445 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 554,263 | 5.543 | 20 | 20 | fits | 87,622 | 44 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 152,162 | 1.522 | 20 | 24 | fits | 148,178 | 142 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 300,996 | 3.010 | 20 | 24 | fits | 149,824 | 174 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 300,930 | 3.009 | 20 | 50 | fits | 149,824 | 174 | 0.445 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 459,313 | 4.593 | 20 | 50 | fits | 158,779 | 209 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 557,221 | 5.572 | 20 | 20 | fits | 87,622 | 44 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 929,339 | 9.293 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 407,082 | 4.071 | 20 | 20 | fits | 157,031 | 204 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 304,530 | 3.045 | 20 | 200 | fits | 153,374 | 180 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 460,945 | 4.609 | 20 | 200 | fits | 157,031 | 204 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 305,454 | 3.055 | 20 | 20 | fits | 153,374 | 180 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 548,880 | 5.489 | 20 | 20 | fits | 87,231 | 38 | 0.759 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 155,720 | 1.557 | 20 | 24 | fits | 148,112 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 308,104 | 3.081 | 20 | 24 | fits | 153,374 | 180 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 308,038 | 3.080 | 20 | 50 | fits | 153,374 | 180 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 464,673 | 4.647 | 20 | 50 | fits | 157,031 | 204 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 551,838 | 5.518 | 20 | 20 | fits | 87,231 | 38 | 0.759 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,010,466 | 10.105 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 390,480 | 3.905 | 20 | 20 | fits | 157,167 | 201 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 296,038 | 2.960 | 20 | 200 | fits | 154,204 | 185 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 452,589 | 4.526 | 20 | 200 | fits | 157,167 | 201 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 296,962 | 2.970 | 20 | 20 | fits | 154,204 | 185 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 614,661 | 6.147 | 20 | 20 | fits | 83,809 | 38 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 146,398 | 1.464 | 20 | 24 | fits | 149,558 | 147 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 299,612 | 2.996 | 20 | 24 | fits | 154,204 | 185 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 299,546 | 2.995 | 20 | 50 | fits | 154,204 | 185 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 456,317 | 4.563 | 20 | 50 | fits | 157,167 | 201 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 617,619 | 6.176 | 20 | 20 | fits | 83,809 | 38 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,005,291 | 10.053 | 20 | 20 | fits | 41,615 | 16 | 0.760 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 406,310 | 4.063 | 20 | 20 | fits | 149,301 | 201 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 300,972 | 3.010 | 20 | 200 | fits | 151,635 | 176 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 449,657 | 4.497 | 20 | 200 | fits | 149,301 | 201 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 301,896 | 3.019 | 20 | 20 | fits | 151,635 | 176 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 533,834 | 5.338 | 20 | 20 | fits | 83,473 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 153,901 | 1.539 | 20 | 24 | fits | 148,089 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 304,546 | 3.045 | 20 | 24 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 304,480 | 3.045 | 20 | 50 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 453,385 | 4.534 | 20 | 50 | fits | 149,301 | 201 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 536,792 | 5.368 | 20 | 20 | fits | 83,473 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 930,151 | 9.302 | 20 | 20 | fits | 50,331 | 20 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 430,991 | 4.310 | 20 | 20 | fits | 154,086 | 208 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 300,562 | 3.006 | 20 | 200 | fits | 148,915 | 171 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 464,338 | 4.643 | 20 | 200 | fits | 154,086 | 208 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 301,486 | 3.015 | 20 | 20 | fits | 148,915 | 171 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 550,252 | 5.503 | 20 | 20 | fits | 85,210 | 42 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 156,211 | 1.562 | 20 | 24 | fits | 148,024 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 304,136 | 3.041 | 20 | 24 | fits | 148,915 | 171 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 304,070 | 3.041 | 20 | 50 | fits | 148,915 | 171 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 468,066 | 4.681 | 20 | 50 | fits | 154,086 | 208 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 553,210 | 5.532 | 20 | 20 | fits | 85,210 | 42 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 933,802 | 9.338 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 79,654 | 0.797 | 20 | 20 | fits | 26,802 | 8 | 0.784 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,273 | 0.443 | 20 | 20 | fits | 44,339 | 12 | 0.891 |
| malformed MRPDU discard | `srp.malformed.if0` | 23,118 | 0.231 | 20 | 20 | fits | 23,184 | 12 | 0.714 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 78,560 | 0.786 | 220 | 220 | fits | 42,796 | 6 | 0.905 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,351,268 | 63.513 | 20 | 20 | MISS ceiling | 23,931 | 13 | 0.639 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,379,938 | 63.799 | 20 | 20 | MISS ceiling | 27,295 | 18 | 0.716 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,402,679 | 64.027 | 20 | 20 | MISS ceiling | 25,065 | 13 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,427,343 | 64.273 | 20 | 20 | MISS ceiling | 24,114 | 13 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,451,225 | 64.512 | 20 | 20 | MISS ceiling | 23,755 | 13 | 0.630 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 159,106 | 1.591 | 20 | 200 | fits | 154,925 | 177 | 0.463 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 291,568 | 2.916 | 20 | 200 | fits | 133,078 | 207 | 0.400 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 154,784 | 1.548 | 20 | 20 | fits | 154,925 | 177 | 0.463 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,238,023 | 62.380 | 20 | 20 | MISS ceiling | 38,509 | 15 | 0.767 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,424 | 1.584 | 20 | 24 | fits | 154,925 | 177 | 0.463 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,203,000 | 62.030 | 20 | 24 | MISS ceiling | 153,808 | 106 | 0.409 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 157,368 | 1.574 | 20 | 50 | fits | 154,925 | 177 | 0.463 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 290,050 | 2.901 | 20 | 50 | fits | 133,078 | 207 | 0.400 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 371,560 | 3.716 | 20 | 20 | fits | 81,576 | 28 | 0.740 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 707,964 | 7.080 | 20 | 20 | fits | 85,132 | 36 | 0.555 |
| LINK_UP | `adp.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,642 | 0.206 | 20 | 200 | fits | 27,497 | 23 (39) | 0.740 |
| GM_CHANGE | `adp.gm_change.if0` | 2,750 | 0.028 | 20 | 200 | fits | 20,707 | 17 (11) | 0.744 |
| BIND_RX | `acmp.bind_rx.if0` | 20,737 | 0.207 | 20 | 20 | fits | 46,812 | 26 (77) | 0.796 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,848 | 0.108 | 20 | 20 | fits | 35,038 | 19 (32) | 0.830 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,076 | 0.111 | 20 | 20 | fits | 30,520 | 16 (47) | 0.777 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 16,080 | 0.161 | 20 | 20 | fits | 42,913 | 18 (50) | 0.840 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,254 | 0.113 | 20 | 20 | fits | 30,723 | 17 (48) | 0.763 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,044 | 0.100 | 20 | 20 | fits | 29,295 | 16 (48) | 0.735 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 10,716 | 0.107 | 20 | 20 | fits | 30,215 | 16 (48) | 0.771 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,905 | 0.099 | 20 | 20 | fits | 28,850 | 16 (48) | 0.735 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
