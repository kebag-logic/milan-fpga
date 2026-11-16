### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 38 paths and 7 of 97 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.195 (0.414) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.090 (0.245) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.196 (0.548) | fits | 0 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.105 (0.262) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.090 (0.243) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.093 (0.253) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.107 (0.267) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.095 (0.320) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.139 (0.574) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.129 (0.382) | fits | 0 acmp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.177) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.026 (0.265) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.026 (0.271) | fits | 0 events | 2 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.095 (0.424) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged1-5.adp_available.if0` (backlog-adp@verify-aged1-5) | 3.652 (4.229) | fits | 7 adp | 4 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.905 (63.201) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.652 (63.948) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.317 (0.464) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.310 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.577 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.998 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.915 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 9.119 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.293 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.acmp.first.if0` (backlog-adp@verify-aged2-5) | 3.165 | fits | 0 acmp | 6 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.002 | MISS ceiling | 11 acmp | 6 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.adp.first.if0` (backlog-adp@verify-aged2-5) | 3.155 | fits | 0 adp | 6 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.adp.last.if0` (backlog-adp@verify-aged2-5) | 4.284 | fits | 7 adp | 6 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.aecp.first.if0` (backlog-adp@verify-aged2-5) | 1.641 | fits | 0 aecp | 6 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.736 | MISS ceiling | 15 aecp | 6 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.maap.first.if0` (backlog-adp@verify-aged2-5) | 3.190 | fits | 0 maap | 6 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.maap.last.if0` (backlog-adp@verify-aged2-5) | 4.322 | fits | 6 maap | 6 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.srp.first.if0` (backlog-adp@verify-aged2-5) | 5.953 | fits | 0 srp | 6 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.srp.last.if0` (backlog-adp@verify-aged2-5) | 10.976 | fits | 31 srp | 6 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.904 (0.996) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.449 (0.450) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.218 (0.219) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.774 (0.856) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-aged1-5 | 0 | 11.413 | 11 | 152,239 (1.522) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.506 | 12 | 152,298 (1.523) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.266 | 11 | 152,317 (1.523) | yes | - |
| backlog-adp@verify-aged1-5 | 1 | 11.633 | 12 | 151,414 (1.514) | yes | - |
| backlog-owed | 0 | 64.307 | 26 | 149,154 (1.492) | yes | - |
| fixture | 0 | 1.308 | 2 | 81,156 (0.812) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 149,154 CPU cycles (1.492 ms), backlog-owed.
Over the windows that released their whole load only: 149,154 (1.492 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@program-aged1-5 | 774 | 0 | 152,239 (1.522) | fits |
| backlog-adp@verify-aged2-5 | 931 | 0 | 152,298 (1.523) | fits |
| backlog-adp@verify-aged1-1 | 842 | 0 | 152,317 (1.523) | fits |
| backlog-adp@verify-aged1-5 | 873 | 0 | 152,364 (1.524) | fits |
| save-held | 1467 | 0 | 158,615 (1.586) | fits |
| srp | 290 | 0 | 57,083 (0.571) | fits |
| backlog-owed | 311 | 0 | 149,154 (1.492) | fits |
| adp-gm | 88 | 0 | 30,305 (0.303) | fits |
| acmp-cmd | 85 | 0 | 41,470 (0.415) | fits |
| fixture | 151 | 0 | 81,156 (0.812) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.073 (20) | 9.927 |
| backlog-adp@verify-aged2-5 | 2 | +4.338 ms, 77,749 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.976 (20) | 9.024 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.971 (20) | 10.029 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.916 (20) | 10.084 |

Least margin over the aged windows: 9.024 ms, `backlog-adp@verify-aged2-5.service.srp.last.if0` at 10.976 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 2019.304 | 4,070 | 102 | - | 15.519 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@program-aged1-5 | 326 | 96,998 (0.970) | 78,944 (0.789) |
| backlog-adp@verify-aged2-5 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-1 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-5 | 355 | 100,110 (1.001) | 78,341 (0.783) |
| save-held | 722 | 95,696 (0.957) | 78,773 (0.788) |
| srp | 271 | 22,507 (0.225) | 2,414 (0.024) |
| backlog-owed | 276 | 22,507 (0.225) | 2,414 (0.024) |
| adp-gm | 79 | 22,267 (0.223) | 2,414 (0.024) |
| acmp-cmd | 65 | 22,267 (0.223) | 2,414 (0.024) |
| fixture | 54 | 20,164 (0.202) | 2,414 (0.024) |

Longest pass that carries a step: 100,110 CPU cycles (1.001 ms), backlog-adp@verify-aged1-5; longest step: 78,944 (0.789 ms), backlog-adp@program-aged1-5.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 364,165 | 3.642 | 20 | 20 | fits | 106,125 | 160 | 0.467 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 308,539 | 3.085 | 20 | 200 | fits | 149,925 | 233 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 414,048 | 4.140 | 20 | 200 | fits | 106,125 | 160 | 0.467 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 309,463 | 3.095 | 20 | 20 | fits | 149,925 | 233 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 414,752 | 4.148 | 20 | 20 | fits | 106,125 | 160 | 0.467 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 163,178 | 1.632 | 20 | 24 | fits | 152,239 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 312,113 | 3.121 | 20 | 24 | fits | 149,925 | 233 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 312,047 | 3.120 | 20 | 50 | fits | 149,925 | 233 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 417,776 | 4.178 | 20 | 50 | fits | 106,125 | 160 | 0.467 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 508,014 | 5.080 | 20 | 20 | fits | 90,304 | 31 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,007,330 | 10.073 | 20 | 20 | fits | 60,257 | 20 | 0.721 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 357,179 | 3.572 | 20 | 20 | fits | 113,527 | 166 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 315,535 | 3.155 | 20 | 200 | fits | 147,065 | 235 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 428,446 | 4.284 | 20 | 200 | fits | 113,527 | 166 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 316,459 | 3.165 | 20 | 20 | fits | 147,065 | 235 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 429,150 | 4.292 | 20 | 20 | fits | 113,527 | 166 | 0.474 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 164,114 | 1.641 | 20 | 24 | fits | 152,298 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 319,109 | 3.191 | 20 | 24 | fits | 147,065 | 235 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 319,043 | 3.190 | 20 | 50 | fits | 147,065 | 235 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 432,174 | 4.322 | 20 | 50 | fits | 113,527 | 166 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 595,325 | 5.953 | 20 | 20 | fits | 85,468 | 25 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,097,555 | 10.976 | 20 | 20 | fits | 73,608 | 24 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 341,407 | 3.414 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 298,536 | 2.985 | 20 | 200 | fits | 148,518 | 248 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 398,493 | 3.985 | 20 | 200 | fits | 100,573 | 142 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 299,460 | 2.995 | 20 | 20 | fits | 148,518 | 248 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 399,197 | 3.992 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 154,582 | 1.546 | 20 | 24 | fits | 152,317 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 302,110 | 3.021 | 20 | 24 | fits | 148,518 | 248 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 302,044 | 3.020 | 20 | 50 | fits | 148,518 | 248 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 402,221 | 4.022 | 20 | 50 | fits | 100,573 | 142 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 488,378 | 4.884 | 20 | 20 | fits | 86,223 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 997,073 | 9.971 | 20 | 20 | fits | 86,040 | 28 | 0.647 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 365,154 | 3.652 | 20 | 20 | fits | 109,728 | 166 | 0.479 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 297,075 | 2.971 | 20 | 200 | fits | 151,414 | 239 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 415,582 | 4.156 | 20 | 200 | fits | 109,728 | 166 | 0.479 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 297,999 | 2.980 | 20 | 20 | fits | 151,414 | 239 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 416,286 | 4.163 | 20 | 20 | fits | 109,728 | 166 | 0.479 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 150,225 | 1.502 | 20 | 24 | fits | 152,364 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 300,649 | 3.006 | 20 | 24 | fits | 151,414 | 239 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 300,583 | 3.006 | 20 | 50 | fits | 151,414 | 239 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 419,310 | 4.193 | 20 | 50 | fits | 109,728 | 166 | 0.479 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 505,412 | 5.054 | 20 | 20 | fits | 86,168 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 991,557 | 9.916 | 20 | 20 | fits | 60,102 | 20 | 0.713 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 157,675 | 1.577 | 20 | 200 | fits | 158,615 | 273 | 0.454 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 230,978 | 2.310 | 20 | 20 | fits | 93,440 | 65 | 0.693 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 299,827 | 2.998 | 20 | 24 | fits | 81,359 | 48 | 0.567 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 191,503 | 1.915 | 20 | 50 | fits | 93,440 | 65 | 0.693 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 911,858 | 9.119 | 20 | 20 | fits | 86,315 | 28 | 0.651 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 229,289 | 2.293 | 20 | 20 | fits | 0 | - | 0.000 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 77,429 | 0.774 | 20 | 20 | fits | 28,178 | 8 | 0.760 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,919 | 0.449 | 20 | 20 | fits | 44,985 | 12 | 0.896 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,239 | 0.212 | 20 | 20 | fits | 21,305 | 12 | 0.691 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 90,436 | 0.904 | 220 | 220 | fits | 57,083 | 6 | 0.901 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,290,483 | 62.905 | 20 | 20 | MISS ceiling | 18,812 | 14 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,309,229 | 63.092 | 20 | 20 | MISS ceiling | 18,822 | 13 | 0.630 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,327,978 | 63.280 | 20 | 20 | MISS ceiling | 18,806 | 13 | 0.630 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,346,639 | 63.466 | 20 | 20 | MISS ceiling | 18,737 | 13 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,365,221 | 63.652 | 20 | 20 | MISS ceiling | 18,645 | 13 | 0.654 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 160,211 | 1.602 | 20 | 200 | fits | 149,154 | 204 | 0.437 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 246,865 | 2.469 | 20 | 200 | fits | 87,270 | 179 | 0.395 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 155,889 | 1.559 | 20 | 20 | fits | 149,154 | 204 | 0.437 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,200,208 | 62.002 | 20 | 20 | MISS ceiling | 30,113 | 15 | 0.781 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 159,529 | 1.595 | 20 | 24 | fits | 149,154 | 204 | 0.437 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,173,581 | 61.736 | 20 | 24 | MISS ceiling | 141,054 | 106 | 0.415 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 158,473 | 1.585 | 20 | 50 | fits | 149,154 | 204 | 0.437 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 245,347 | 2.453 | 20 | 50 | fits | 87,270 | 179 | 0.395 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 331,191 | 3.312 | 20 | 20 | fits | 85,910 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 826,591 | 8.266 | 20 | 20 | fits | 73,553 | 24 | 0.673 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| GM_CHANGE | `adp.gm_change.if0` | 2,371 | 0.024 | 20 | 200 | fits | 17,717 | 17 (11) | 0.759 |
| BIND_RX | `acmp.bind_rx.if0` | 19,035 | 0.190 | 20 | 20 | fits | 41,470 | 26 (77) | 0.798 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,493 | 0.095 | 20 | 20 | fits | 31,952 | 19 (32) | 0.835 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,544 | 0.105 | 20 | 20 | fits | 26,236 | 15 (47) | 0.783 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 12,858 | 0.129 | 20 | 20 | fits | 38,179 | 18 (50) | 0.825 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,702 | 0.107 | 20 | 20 | fits | 26,682 | 17 (48) | 0.775 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,342 | 0.093 | 20 | 20 | fits | 25,296 | 16 (48) | 0.747 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,004 | 0.090 | 20 | 20 | fits | 24,460 | 16 (48) | 0.739 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,957 | 0.090 | 20 | 20 | fits | 24,311 | 16 (48) | 0.736 |
| LINK_UP | `fixture.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| malformed MRPDU discard | `fixture.malformed.if0` | 21,785 | 0.218 | 20 | 20 | fits | 21,851 | 12 | 0.735 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 31,707 | 0.317 | 20 | 24 | fits | 46,401 | 43 | 0.781 |
| LINK_DOWN | `fixture.link_down.if0` | 2,648 | 0.026 | 20 | 200 | fits | 26,482 | 23 (9) | 0.794 |
| BIND_RX | `fixture.bind_rx.if0` | 19,508 | 0.195 | 20 | 20 | fits | 41,432 | 26 (77) | 0.800 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 13,902 | 0.139 | 20 | 20 | fits | 36,762 | 29 (35) | 0.789 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 19,599 | 0.196 | 20 | 20 | fits | 25,207 | 13 (29) | 0.818 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 81,052 | 0.811 | 20 | 200 | fits | 81,156 | 49 | 0.757 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 81,052 | 0.811 | 20 | 200 | fits | 81,156 | 49 | 0.757 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 80,778 | 0.808 | 20 | 20 | fits | 81,156 | 49 | 0.757 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 80,778 | 0.808 | 20 | 20 | fits | 81,156 | 49 | 0.757 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 80,986 | 0.810 | 20 | 24 | fits | 81,156 | 49 | 0.757 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 80,986 | 0.810 | 20 | 24 | fits | 81,156 | 49 | 0.757 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 80,920 | 0.809 | 20 | 50 | fits | 81,156 | 49 | 0.757 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 80,920 | 0.809 | 20 | 50 | fits | 81,156 | 49 | 0.757 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 80,854 | 0.809 | 20 | 20 | fits | 81,156 | 49 | 0.757 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 80,854 | 0.809 | 20 | 20 | fits | 81,156 | 49 | 0.757 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
