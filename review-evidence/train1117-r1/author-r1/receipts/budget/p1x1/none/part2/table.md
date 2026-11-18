### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 28 paths and 7 of 118 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.187 (0.418) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.099 (0.238) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.108 (0.258) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.100 (0.238) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.105 (0.249) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.115 (0.266) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.098 (0.324) | fits | 0 acmp | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.101 (0.525) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.139 (0.395) | fits | 0 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-1.adp_available.if0` (backlog-adp@program-1) | 3.958 (5.514) | fits | 7 adp | 8 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.953 (63.136) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.701 (63.886) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.300 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.574 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.958 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.357 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 9.394 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.571 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-1.service.acmp.first.if0` (backlog-adp@program-1) | 3.356 | fits | 0 acmp | 9 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.058 | MISS ceiling | 11 acmp | 9 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-1.service.adp.first.if0` (backlog-adp@program-1) | 3.347 | fits | 0 adp | 9 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-1.service.adp.last.if0` (backlog-adp@program-1) | 4.564 | fits | 7 adp | 9 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-1.service.aecp.first.if0` (backlog-adp@program-1) | 1.908 | fits | 0 aecp | 9 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.795 | MISS ceiling | 15 aecp | 9 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-1.service.maap.first.if0` (backlog-adp@program-1) | 3.382 | fits | 0 maap | 9 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-1.service.maap.last.if0` (backlog-adp@program-1) | 4.601 | fits | 6 maap | 9 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-1.service.srp.first.if0` (backlog-adp@program-1) | 5.441 | fits | 0 srp | 9 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-1.service.srp.last.if0` (backlog-adp@program-aged2-1) | 11.037 | fits | 31 srp | 9 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-1 | 0 | 11.931 | 11 | 152,870 (1.529) | yes | - |
| backlog-adp@verify-1 | 0 | 13.237 | 11 | 152,657 (1.527) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 13.626 | 10 | 150,542 (1.505) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 13.051 | 12 | 151,757 (1.518) | yes | - |
| backlog-adp@program-aged2-1 | 1 | 12.455 | 11 | 151,593 (1.516) | yes | - |
| backlog-adp@program-aged1-1 | 1 | 12.200 | 10 | 149,860 (1.499) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 13.746 | 11 | 151,369 (1.514) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 12.897 | 11 | 151,480 (1.515) | yes | - |
| backlog-owed | 0 | 64.342 | 25 | 139,541 (1.395) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 139,541 CPU cycles (1.395 ms), backlog-owed.
Over the windows that released their whole load only: 139,541 (1.395 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3609 | 0 | 102,333 (1.023) | fits |
| backlog-adp@program-1 | 493 | 0 | 152,870 (1.529) | fits |
| backlog-adp@verify-1 | 499 | 0 | 152,657 (1.527) | fits |
| backlog-adp@blank-aged2-1 | 749 | 0 | 151,380 (1.514) | fits |
| backlog-adp@blank-aged1-1 | 690 | 0 | 151,757 (1.518) | fits |
| backlog-adp@program-aged2-1 | 778 | 0 | 151,718 (1.517) | fits |
| backlog-adp@program-aged1-1 | 716 | 0 | 151,252 (1.513) | fits |
| backlog-adp@verify-aged2-1 | 794 | 0 | 151,369 (1.514) | fits |
| backlog-adp@verify-aged1-1 | 733 | 0 | 151,480 (1.515) | fits |
| save-held | 1462 | 0 | 158,363 (1.584) | fits |
| backlog-owed | 311 | 0 | 150,255 (1.503) | fits |
| acmp-cmd | 85 | 0 | 41,760 (0.418) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-1 | 2 | +9.262 ms, 76,941 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.857 (20) | 9.143 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.275 (20) | 9.725 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.037 (20) | 8.963 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.043 (20) | 9.957 |
| backlog-adp@verify-aged2-1 | 2 | +9.347 ms, 77,604 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 10.947 (20) | 9.053 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.097 (20) | 9.903 |

Least margin over the aged windows: 8.963 ms, `backlog-adp@program-aged2-1.service.srp.last.if0` at 11.037 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 1096.520 | 4,070 | 102 | - | 17.198 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1158 | 102,333 (1.023) | 78,402 (0.784) |
| backlog-adp@program-1 | 371 | 95,469 (0.955) | 78,491 (0.785) |
| backlog-adp@verify-1 | 397 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@blank-aged2-1 | 340 | 92,163 (0.922) | 76,052 (0.761) |
| backlog-adp@blank-aged1-1 | 339 | 92,779 (0.928) | 76,409 (0.764) |
| backlog-adp@program-aged2-1 | 369 | 95,347 (0.953) | 78,702 (0.787) |
| backlog-adp@program-aged1-1 | 368 | 95,708 (0.957) | 78,835 (0.788) |
| backlog-adp@verify-aged2-1 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@verify-aged1-1 | 397 | 94,984 (0.950) | 78,276 (0.783) |
| save-held | 815 | 93,833 (0.938) | 78,337 (0.783) |
| backlog-owed | 276 | 22,571 (0.226) | 2,593 (0.026) |
| acmp-cmd | 65 | 22,571 (0.226) | 2,593 (0.026) |

Longest pass that carries a step: 102,333 CPU cycles (1.023 ms), acmp-notk; longest step: 78,835 (0.788 ms), backlog-adp@program-aged1-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 10,095 | 0.101 | 20 | 20 | fits | 34,147 | 19 (14) | 0.883 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 395,828 | 3.958 | 20 | 20 | fits | 122,313 | 169 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 334,682 | 3.347 | 20 | 200 | fits | 148,441 | 226 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 456,379 | 4.564 | 20 | 200 | fits | 122,313 | 169 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 335,606 | 3.356 | 20 | 20 | fits | 148,441 | 226 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 457,083 | 4.571 | 20 | 20 | fits | 122,313 | 169 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 190,805 | 1.908 | 20 | 24 | fits | 152,870 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 338,256 | 3.383 | 20 | 24 | fits | 148,441 | 226 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 338,190 | 3.382 | 20 | 50 | fits | 148,441 | 226 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 460,107 | 4.601 | 20 | 50 | fits | 122,313 | 169 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 544,138 | 5.441 | 20 | 20 | fits | 84,097 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,051,091 | 10.511 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 382,872 | 3.829 | 20 | 20 | fits | 113,211 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 330,299 | 3.303 | 20 | 200 | fits | 148,682 | 226 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 442,894 | 4.429 | 20 | 200 | fits | 113,211 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 331,223 | 3.312 | 20 | 20 | fits | 148,682 | 226 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 443,598 | 4.436 | 20 | 20 | fits | 113,211 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 186,181 | 1.862 | 20 | 24 | fits | 152,657 | 155 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 333,873 | 3.339 | 20 | 24 | fits | 148,682 | 226 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 333,807 | 3.338 | 20 | 50 | fits | 148,682 | 226 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 446,622 | 4.466 | 20 | 50 | fits | 113,211 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 530,916 | 5.309 | 20 | 20 | fits | 84,360 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,043,698 | 10.437 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 347,721 | 3.477 | 20 | 20 | fits | 113,464 | 163 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 294,938 | 2.949 | 20 | 200 | fits | 150,542 | 231 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 407,786 | 4.078 | 20 | 200 | fits | 113,464 | 163 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 295,862 | 2.959 | 20 | 20 | fits | 150,542 | 231 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 408,490 | 4.085 | 20 | 20 | fits | 113,464 | 163 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 148,960 | 1.490 | 20 | 24 | fits | 151,380 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 298,512 | 2.985 | 20 | 24 | fits | 150,542 | 231 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 298,446 | 2.984 | 20 | 50 | fits | 150,542 | 231 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 411,514 | 4.115 | 20 | 50 | fits | 113,464 | 163 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 495,691 | 4.957 | 20 | 20 | fits | 84,243 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,085,682 | 10.857 | 20 | 20 | fits | 86,246 | 29 | 0.621 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 375,643 | 3.756 | 20 | 20 | fits | 113,423 | 166 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 314,088 | 3.141 | 20 | 200 | fits | 151,337 | 227 | 0.449 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 426,895 | 4.269 | 20 | 200 | fits | 113,423 | 166 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 315,012 | 3.150 | 20 | 20 | fits | 151,337 | 227 | 0.449 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 427,599 | 4.276 | 20 | 20 | fits | 113,423 | 166 | 0.409 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 156,508 | 1.565 | 20 | 24 | fits | 151,757 | 153 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 317,662 | 3.177 | 20 | 24 | fits | 151,337 | 227 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 317,596 | 3.176 | 20 | 50 | fits | 151,337 | 227 | 0.449 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 430,623 | 4.306 | 20 | 50 | fits | 113,423 | 166 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 514,891 | 5.149 | 20 | 20 | fits | 84,334 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,027,550 | 10.275 | 20 | 20 | fits | 78,999 | 31 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 363,496 | 3.635 | 20 | 20 | fits | 117,143 | 169 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 307,564 | 3.076 | 20 | 200 | fits | 151,593 | 231 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 424,091 | 4.241 | 20 | 200 | fits | 117,143 | 169 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 308,488 | 3.085 | 20 | 20 | fits | 151,593 | 231 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 424,795 | 4.248 | 20 | 20 | fits | 117,143 | 169 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 149,498 | 1.495 | 20 | 24 | fits | 151,718 | 153 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 311,138 | 3.111 | 20 | 24 | fits | 151,593 | 231 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 311,072 | 3.111 | 20 | 50 | fits | 151,593 | 231 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 427,819 | 4.278 | 20 | 50 | fits | 117,143 | 169 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 512,097 | 5.121 | 20 | 20 | fits | 84,344 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,103,682 | 11.037 | 20 | 20 | fits | 79,204 | 31 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 346,878 | 3.469 | 20 | 20 | fits | 113,320 | 164 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 294,328 | 2.943 | 20 | 200 | fits | 149,860 | 231 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 407,032 | 4.070 | 20 | 200 | fits | 113,320 | 164 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 295,252 | 2.953 | 20 | 20 | fits | 149,860 | 231 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 407,736 | 4.077 | 20 | 20 | fits | 113,320 | 164 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 149,032 | 1.490 | 20 | 24 | fits | 151,252 | 152 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 297,902 | 2.979 | 20 | 24 | fits | 149,860 | 231 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 297,836 | 2.978 | 20 | 50 | fits | 149,860 | 231 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 410,760 | 4.108 | 20 | 50 | fits | 113,320 | 164 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 510,533 | 5.105 | 20 | 20 | fits | 88,130 | 31 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,004,337 | 10.043 | 20 | 20 | fits | 73,094 | 24 | 0.641 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 364,565 | 3.646 | 20 | 20 | fits | 113,190 | 166 | 0.406 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 303,150 | 3.031 | 20 | 200 | fits | 147,722 | 222 | 0.437 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 415,724 | 4.157 | 20 | 200 | fits | 113,190 | 166 | 0.406 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 304,074 | 3.041 | 20 | 20 | fits | 147,722 | 222 | 0.437 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 416,428 | 4.164 | 20 | 20 | fits | 113,190 | 166 | 0.406 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 159,992 | 1.600 | 20 | 24 | fits | 151,369 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 306,724 | 3.067 | 20 | 24 | fits | 147,722 | 222 | 0.437 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 306,658 | 3.067 | 20 | 50 | fits | 147,722 | 222 | 0.437 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 419,452 | 4.195 | 20 | 50 | fits | 113,190 | 166 | 0.406 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 503,815 | 5.038 | 20 | 20 | fits | 84,429 | 24 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,094,653 | 10.947 | 20 | 20 | fits | 86,088 | 29 | 0.616 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 357,686 | 3.577 | 20 | 20 | fits | 113,244 | 166 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 296,271 | 2.963 | 20 | 200 | fits | 147,630 | 222 | 0.436 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 408,899 | 4.089 | 20 | 200 | fits | 113,244 | 166 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 297,195 | 2.972 | 20 | 20 | fits | 147,630 | 222 | 0.436 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 409,603 | 4.096 | 20 | 20 | fits | 113,244 | 166 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 153,205 | 1.532 | 20 | 24 | fits | 151,480 | 152 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 299,845 | 2.998 | 20 | 24 | fits | 147,630 | 222 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 299,779 | 2.998 | 20 | 50 | fits | 147,630 | 222 | 0.436 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 412,627 | 4.126 | 20 | 50 | fits | 113,244 | 166 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 496,912 | 4.969 | 20 | 20 | fits | 84,351 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,009,721 | 10.097 | 20 | 20 | fits | 85,809 | 28 | 0.604 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 157,423 | 1.574 | 20 | 200 | fits | 158,363 | 243 | 0.494 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 229,985 | 2.300 | 20 | 20 | fits | 92,699 | 91 | 0.627 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 295,794 | 2.958 | 20 | 24 | fits | 79,814 | 49 | 0.582 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 135,660 | 1.357 | 20 | 50 | fits | 43,554 | 67 | 0.472 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 939,420 | 9.394 | 20 | 20 | fits | 33,124 | 12 | 0.810 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 257,094 | 2.571 | 49 | 49 | fits | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,295,302 | 62.953 | 20 | 20 | MISS ceiling | 18,754 | 13 | 0.562 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,314,054 | 63.141 | 20 | 20 | MISS ceiling | 18,848 | 13 | 0.545 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,332,829 | 63.328 | 20 | 20 | MISS ceiling | 18,812 | 13 | 0.545 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,351,496 | 63.515 | 20 | 20 | MISS ceiling | 18,743 | 13 | 0.554 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,370,084 | 63.701 | 20 | 20 | MISS ceiling | 18,651 | 13 | 0.571 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 149,919 | 1.499 | 20 | 200 | fits | 150,255 | 222 | 0.450 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 238,331 | 2.383 | 20 | 200 | fits | 89,028 | 164 | 0.318 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 145,597 | 1.456 | 20 | 20 | fits | 150,255 | 222 | 0.450 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,205,808 | 62.058 | 20 | 20 | MISS ceiling | 29,764 | 15 | 0.731 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 149,237 | 1.492 | 20 | 24 | fits | 150,255 | 222 | 0.450 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,179,530 | 61.795 | 20 | 24 | MISS ceiling | 139,541 | 106 | 0.468 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 148,181 | 1.482 | 20 | 50 | fits | 150,255 | 222 | 0.450 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 236,813 | 2.368 | 20 | 50 | fits | 89,028 | 164 | 0.318 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 320,728 | 3.207 | 20 | 20 | fits | 83,981 | 24 | 0.773 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 824,457 | 8.245 | 20 | 20 | fits | 74,609 | 24 | 0.662 |
| BIND_RX | `acmp.bind_rx.if0` | 18,708 | 0.187 | 20 | 20 | fits | 41,760 | 26 (77) | 0.786 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,765 | 0.098 | 20 | 20 | fits | 32,401 | 19 (32) | 0.813 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,821 | 0.108 | 20 | 20 | fits | 25,814 | 15 (47) | 0.748 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,874 | 0.139 | 20 | 20 | fits | 39,488 | 18 (50) | 0.821 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,543 | 0.115 | 20 | 20 | fits | 26,592 | 17 (48) | 0.747 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,497 | 0.105 | 20 | 20 | fits | 24,917 | 16 (48) | 0.713 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,924 | 0.099 | 20 | 20 | fits | 23,800 | 16 (48) | 0.694 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,953 | 0.100 | 20 | 20 | fits | 23,781 | 16 (48) | 0.694 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
