### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 52 paths and 7 of 225 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.184 (0.404) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.089 (0.231) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.133 (0.482) | fits | 0 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.105 (0.241) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.092 (0.230) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.100 (0.236) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.105 (0.253) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.097 (0.320) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.137 (0.471) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.223 (0.559) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.165 (0.503) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.057 (0.243) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.132 (0.393) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.044 (0.159) | fits | 0 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.026 (0.160) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.027 (0.273) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.028 (0.264) | fits | 0 events | 3 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.174 (0.464) | fits | 0 events | 2 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 1.652 (1.943) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.293 (1.631) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.879 (3.212) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.516 (2.849) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.403 (1.706) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.411 (5.115) | fits | 7 adp | 14 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.766 (63.031) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.456 (63.721) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.323 (0.456) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.326 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.553 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.792 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.931 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 8.086 | fits | 31 srp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.195 (0.501) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.088 (0.204) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.111 (0.264) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.173 (0.501) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.207 (0.511) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.834 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.acmp.first.if0` (backlog-adp@program-aged2-7) | 3.092 | fits | 0 acmp | 16 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 61.930 | MISS ceiling | 11 acmp | 16 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.adp.first.if0` (backlog-adp@program-aged2-7) | 3.083 | fits | 0 adp | 16 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 4.988 | fits | 7 adp | 16 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.589 | fits | 0 aecp | 16 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.680 | MISS ceiling | 15 aecp | 16 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.maap.first.if0` (backlog-adp@program-aged2-7) | 3.118 | fits | 0 maap | 16 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.026 | fits | 6 maap | 16 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 5.926 | fits | 0 srp | 16 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.srp.last.if0` (backlog-adp@program-aged2-7) | 9.961 | fits | 31 srp | 16 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.975 (1.088) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.438 (0.439) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.210 (0.211) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.888 (0.960) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-aged2-7 | 0 | 10.459 | 11 | 149,819 (1.498) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.815 | 12 | 147,844 (1.478) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.290 | 9 | 143,598 (1.436) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.368 | 10 | 149,472 (1.495) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.332 | 10 | 147,778 (1.478) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.127 | 10 | 147,835 (1.478) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.216 | 9 | 145,121 (1.451) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.426 | 11 | 147,935 (1.479) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.304 | 10 | 147,787 (1.478) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.615 | 11 | 144,713 (1.447) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.315 | 10 | 149,329 (1.493) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.239 | 10 | 147,844 (1.478) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 10.498 | 12 | 147,966 (1.480) | yes | - |
| backlog-adp | 0 | 9.480 | 10 | 149,643 (1.496) | yes | - |
| backlog-owed | 0 | 64.044 | 25 | 148,769 (1.488) | yes | - |
| fixture | 0 | 1.315 | 2 | 87,886 (0.879) | yes | - |

Composed maximum over 2 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill not run): 149,643 CPU cycles (1.496 ms), backlog-adp.
Over the windows that released their whole load only: 149,643 (1.496 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@program-aged2-7 | 869 | 0 | 149,819 (1.498) | fits |
| backlog-adp@program-aged1-1 | 756 | 0 | 147,844 (1.478) | fits |
| backlog-adp@program-aged1-3 | 770 | 0 | 149,746 (1.497) | fits |
| backlog-adp@program-aged1-5 | 787 | 0 | 149,472 (1.495) | fits |
| backlog-adp@program-aged1-7 | 803 | 0 | 147,778 (1.478) | fits |
| backlog-adp@verify-aged2-1 | 909 | 0 | 147,835 (1.478) | fits |
| backlog-adp@verify-aged2-3 | 925 | 0 | 147,835 (1.478) | fits |
| backlog-adp@verify-aged2-5 | 943 | 0 | 147,935 (1.479) | fits |
| backlog-adp@verify-aged2-7 | 958 | 0 | 147,787 (1.478) | fits |
| backlog-adp@verify-aged1-1 | 846 | 0 | 147,887 (1.479) | fits |
| backlog-adp@verify-aged1-3 | 861 | 0 | 149,329 (1.493) | fits |
| backlog-adp@verify-aged1-5 | 877 | 0 | 147,844 (1.478) | fits |
| backlog-adp@verify-aged1-7 | 895 | 0 | 147,966 (1.480) | fits |
| save-held | 1400 | 0 | 156,249 (1.562) | fits |
| acmp-noresp | 2026 | 0 | 41,738 (0.417) | fits |
| srp | 289 | 0 | 69,263 (0.693) | fits |
| backlog-adp | 311 | 0 | 149,643 (1.496) | fits |
| backlog-owed | 309 | 0 | 148,769 (1.488) | fits |
| maap | 177 | 0 | 41,738 (0.417) | fits |
| adp-gm | 89 | 0 | 41,738 (0.417) | fits |
| control | 89 | 0 | 41,738 (0.417) | fits |
| acmp-cmd | 87 | 0 | 41,738 (0.417) | fits |
| aecp-largest-notice | 107 | 0 | 146,123 (1.461) | fits |
| fixture | 161 | 0 | 87,886 (0.879) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@program-aged2-7 | 2 | +3.130 ms, 80,027 (0.800 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.961 (20) | 10.039 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.991 (20) | 11.009 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.989 (20) | 11.011 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.072 (20) | 10.928 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.028 (20) | 10.972 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.038 ms, 77,251 (0.773 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.000 (20) | 11.000 |
| backlog-adp@verify-aged2-3 | 2 | +6.667 ms, 77,161 (0.772 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.721 (20) | 10.279 |
| backlog-adp@verify-aged2-5 | 2 | +5.025 ms, 77,522 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.814 (20) | 10.186 |
| backlog-adp@verify-aged2-7 | 2 | +2.955 ms, 76,855 (0.769 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.812 (20) | 10.188 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.934 (20) | 11.066 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.061 (20) | 10.939 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.983 (20) | 11.017 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.965 (20) | 11.035 |

Least margin over the aged windows: 10.039 ms, `backlog-adp@program-aged2-7.service.srp.last.if0` at 9.961 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 2018.461 | 4,070 | 102 | - | 15.332 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@program-aged2-7 | 326 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@program-aged1-1 | 326 | 95,454 (0.955) | 78,828 (0.788) |
| backlog-adp@program-aged1-3 | 326 | 95,454 (0.955) | 78,828 (0.788) |
| backlog-adp@program-aged1-5 | 326 | 95,454 (0.955) | 78,879 (0.789) |
| backlog-adp@program-aged1-7 | 326 | 95,507 (0.955) | 79,049 (0.790) |
| backlog-adp@verify-aged2-1 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged2-3 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged2-5 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged2-7 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged1-1 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged1-3 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged1-5 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged1-7 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| save-held | 722 | 95,955 (0.960) | 78,415 (0.784) |
| acmp-noresp | 615 | 95,456 (0.955) | 78,015 (0.780) |
| srp | 271 | 21,172 (0.212) | 2,067 (0.021) |
| backlog-adp | 271 | 21,172 (0.212) | 2,340 (0.023) |
| backlog-owed | 276 | 21,172 (0.212) | 2,137 (0.021) |
| maap | 165 | 21,172 (0.212) | 2,067 (0.021) |
| adp-gm | 80 | 21,172 (0.212) | 2,067 (0.021) |
| control | 80 | 21,172 (0.212) | 2,067 (0.021) |
| acmp-cmd | 65 | 21,172 (0.212) | 2,067 (0.021) |
| aecp-largest-notice | 78 | 21,172 (0.212) | 2,067 (0.021) |
| fixture | 54 | 15,907 (0.159) | 1,986 (0.020) |

Longest pass that carries a step: 95,955 CPU cycles (0.960 ms), save-held; longest step: 79,049 (0.790 ms), backlog-adp@program-aged1-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 441,077 | 4.411 | 20 | 20 | fits | 111,149 | 169 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 308,280 | 3.083 | 20 | 200 | fits | 149,819 | 231 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 498,840 | 4.988 | 20 | 200 | fits | 111,149 | 169 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 309,204 | 3.092 | 20 | 20 | fits | 149,819 | 231 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 499,544 | 4.995 | 20 | 20 | fits | 111,149 | 169 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 155,826 | 1.558 | 20 | 24 | fits | 147,909 | 153 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 311,854 | 3.119 | 20 | 24 | fits | 149,819 | 231 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 311,788 | 3.118 | 20 | 50 | fits | 149,819 | 231 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 502,568 | 5.026 | 20 | 50 | fits | 111,149 | 169 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 592,599 | 5.926 | 20 | 20 | fits | 90,097 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 996,126 | 9.961 | 20 | 20 | fits | 57,993 | 27 | 0.726 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 358,857 | 3.589 | 20 | 20 | fits | 112,884 | 170 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 289,284 | 2.893 | 20 | 200 | fits | 143,968 | 227 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 410,172 | 4.102 | 20 | 200 | fits | 112,884 | 170 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 290,208 | 2.902 | 20 | 20 | fits | 143,968 | 227 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 410,876 | 4.109 | 20 | 20 | fits | 112,884 | 170 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 149,880 | 1.499 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 292,858 | 2.929 | 20 | 24 | fits | 143,968 | 227 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 292,792 | 2.928 | 20 | 50 | fits | 143,968 | 227 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 413,900 | 4.139 | 20 | 50 | fits | 112,884 | 170 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 504,090 | 5.041 | 20 | 20 | fits | 90,256 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 899,115 | 8.991 | 20 | 20 | fits | 59,801 | 26 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 343,304 | 3.433 | 20 | 20 | fits | 112,973 | 193 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 282,197 | 2.822 | 20 | 200 | fits | 143,598 | 233 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 394,554 | 3.946 | 20 | 200 | fits | 112,973 | 193 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 283,121 | 2.831 | 20 | 20 | fits | 143,598 | 233 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 395,258 | 3.953 | 20 | 20 | fits | 112,973 | 193 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 143,163 | 1.432 | 20 | 24 | fits | 149,746 | 131 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 285,771 | 2.858 | 20 | 24 | fits | 143,598 | 233 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 285,705 | 2.857 | 20 | 50 | fits | 143,598 | 233 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 398,282 | 3.983 | 20 | 50 | fits | 112,973 | 193 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 488,449 | 4.884 | 20 | 20 | fits | 90,233 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 898,913 | 8.989 | 20 | 20 | fits | 57,565 | 27 | 0.718 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 346,421 | 3.464 | 20 | 20 | fits | 102,535 | 142 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 301,895 | 3.019 | 20 | 200 | fits | 149,472 | 248 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 403,814 | 4.038 | 20 | 200 | fits | 102,535 | 142 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 302,819 | 3.028 | 20 | 20 | fits | 149,472 | 248 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 404,518 | 4.045 | 20 | 20 | fits | 102,535 | 142 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 156,987 | 1.570 | 20 | 24 | fits | 147,778 | 152 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 305,469 | 3.055 | 20 | 24 | fits | 149,472 | 248 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 305,403 | 3.054 | 20 | 50 | fits | 149,472 | 248 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 407,542 | 4.075 | 20 | 50 | fits | 102,535 | 142 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 492,866 | 4.929 | 20 | 20 | fits | 85,390 | 30 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 907,249 | 9.072 | 20 | 20 | fits | 63,195 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 354,586 | 3.546 | 20 | 20 | fits | 120,563 | 178 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 292,706 | 2.927 | 20 | 200 | fits | 144,011 | 225 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 421,183 | 4.212 | 20 | 200 | fits | 120,563 | 178 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 293,630 | 2.936 | 20 | 20 | fits | 144,011 | 225 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 421,887 | 4.219 | 20 | 20 | fits | 120,563 | 178 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 153,259 | 1.533 | 20 | 24 | fits | 147,778 | 152 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 296,280 | 2.963 | 20 | 24 | fits | 144,011 | 225 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 296,214 | 2.962 | 20 | 50 | fits | 144,011 | 225 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 424,911 | 4.249 | 20 | 50 | fits | 120,563 | 178 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 515,076 | 5.151 | 20 | 20 | fits | 90,231 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 902,807 | 9.028 | 20 | 20 | fits | 52,507 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 337,702 | 3.377 | 20 | 20 | fits | 108,763 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 287,733 | 2.877 | 20 | 200 | fits | 143,711 | 226 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 395,880 | 3.959 | 20 | 200 | fits | 108,763 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 288,657 | 2.887 | 20 | 20 | fits | 143,711 | 226 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 396,584 | 3.966 | 20 | 20 | fits | 108,763 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 148,586 | 1.486 | 20 | 24 | fits | 147,835 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 291,307 | 2.913 | 20 | 24 | fits | 143,711 | 226 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 291,241 | 2.912 | 20 | 50 | fits | 143,711 | 226 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 399,608 | 3.996 | 20 | 50 | fits | 108,763 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 489,538 | 4.895 | 20 | 20 | fits | 89,996 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 900,017 | 9.000 | 20 | 20 | fits | 59,155 | 26 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 342,930 | 3.429 | 20 | 20 | fits | 109,037 | 164 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 285,415 | 2.854 | 20 | 200 | fits | 145,121 | 231 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 393,836 | 3.938 | 20 | 200 | fits | 109,037 | 164 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 286,339 | 2.863 | 20 | 20 | fits | 145,121 | 231 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 394,540 | 3.945 | 20 | 20 | fits | 109,037 | 164 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 144,858 | 1.449 | 20 | 24 | fits | 147,835 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 288,989 | 2.890 | 20 | 24 | fits | 145,121 | 231 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 288,923 | 2.889 | 20 | 50 | fits | 145,121 | 231 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 397,564 | 3.976 | 20 | 50 | fits | 109,037 | 164 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 488,731 | 4.887 | 20 | 20 | fits | 82,725 | 31 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 972,052 | 9.721 | 20 | 20 | fits | 63,300 | 24 | 0.595 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 354,008 | 3.540 | 20 | 20 | fits | 108,574 | 163 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 303,505 | 3.035 | 20 | 200 | fits | 144,248 | 231 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 411,463 | 4.115 | 20 | 200 | fits | 108,574 | 163 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 304,429 | 3.044 | 20 | 20 | fits | 144,248 | 231 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 412,167 | 4.122 | 20 | 20 | fits | 108,574 | 163 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 156,622 | 1.566 | 20 | 24 | fits | 147,935 | 153 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 307,079 | 3.071 | 20 | 24 | fits | 144,248 | 231 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 307,013 | 3.070 | 20 | 50 | fits | 144,248 | 231 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 415,191 | 4.152 | 20 | 50 | fits | 108,574 | 163 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 500,838 | 5.008 | 20 | 20 | fits | 85,713 | 30 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 981,423 | 9.814 | 20 | 20 | fits | 67,995 | 31 | 0.629 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 417,284 | 4.173 | 20 | 20 | fits | 115,730 | 172 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 290,705 | 2.907 | 20 | 200 | fits | 143,426 | 224 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 482,674 | 4.827 | 20 | 200 | fits | 115,730 | 172 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 291,629 | 2.916 | 20 | 20 | fits | 143,426 | 224 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 483,378 | 4.834 | 20 | 20 | fits | 115,730 | 172 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 151,843 | 1.518 | 20 | 24 | fits | 147,787 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 294,279 | 2.943 | 20 | 24 | fits | 143,426 | 224 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 294,213 | 2.942 | 20 | 50 | fits | 143,426 | 224 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 486,402 | 4.864 | 20 | 50 | fits | 115,730 | 172 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 576,310 | 5.763 | 20 | 20 | fits | 89,974 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 981,190 | 9.812 | 20 | 20 | fits | 52,452 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 346,273 | 3.463 | 20 | 20 | fits | 111,587 | 169 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 293,176 | 2.932 | 20 | 200 | fits | 144,713 | 231 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 404,147 | 4.041 | 20 | 200 | fits | 111,587 | 169 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 294,100 | 2.941 | 20 | 20 | fits | 144,713 | 231 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 404,851 | 4.049 | 20 | 20 | fits | 111,587 | 169 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 145,629 | 1.456 | 20 | 24 | fits | 147,887 | 153 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 296,750 | 2.967 | 20 | 24 | fits | 144,713 | 231 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 296,684 | 2.967 | 20 | 50 | fits | 144,713 | 231 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 407,875 | 4.079 | 20 | 50 | fits | 111,587 | 169 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 498,362 | 4.984 | 20 | 20 | fits | 90,553 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 893,385 | 8.934 | 20 | 20 | fits | 59,799 | 26 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 345,855 | 3.459 | 20 | 20 | fits | 102,561 | 142 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 301,329 | 3.013 | 20 | 200 | fits | 149,329 | 248 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 403,274 | 4.033 | 20 | 200 | fits | 102,561 | 142 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 302,253 | 3.023 | 20 | 20 | fits | 149,329 | 248 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 403,978 | 4.040 | 20 | 20 | fits | 102,561 | 142 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 156,564 | 1.566 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 304,903 | 3.049 | 20 | 24 | fits | 149,329 | 248 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 304,837 | 3.048 | 20 | 50 | fits | 149,329 | 248 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 407,002 | 4.070 | 20 | 50 | fits | 102,561 | 142 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 496,907 | 4.969 | 20 | 20 | fits | 89,971 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 906,122 | 9.061 | 20 | 20 | fits | 63,195 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 341,336 | 3.413 | 20 | 20 | fits | 108,967 | 164 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 291,431 | 2.914 | 20 | 200 | fits | 143,159 | 226 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 399,782 | 3.998 | 20 | 200 | fits | 108,967 | 164 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 292,355 | 2.924 | 20 | 20 | fits | 143,159 | 226 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 400,486 | 4.005 | 20 | 20 | fits | 108,967 | 164 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 152,836 | 1.528 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 295,005 | 2.950 | 20 | 24 | fits | 143,159 | 226 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 294,939 | 2.949 | 20 | 50 | fits | 143,159 | 226 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 403,510 | 4.035 | 20 | 50 | fits | 108,967 | 164 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 499,458 | 4.995 | 20 | 20 | fits | 87,664 | 37 | 0.754 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 898,260 | 8.983 | 20 | 20 | fits | 63,181 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 349,788 | 3.498 | 20 | 20 | fits | 118,400 | 190 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 296,722 | 2.967 | 20 | 200 | fits | 144,857 | 209 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 414,506 | 4.145 | 20 | 200 | fits | 118,400 | 190 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 297,646 | 2.976 | 20 | 20 | fits | 144,857 | 209 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 415,210 | 4.152 | 20 | 20 | fits | 118,400 | 190 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 149,230 | 1.492 | 20 | 24 | fits | 147,966 | 153 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 300,296 | 3.003 | 20 | 24 | fits | 144,857 | 209 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 300,230 | 3.002 | 20 | 50 | fits | 144,857 | 209 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 418,234 | 4.182 | 20 | 50 | fits | 118,400 | 190 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 508,547 | 5.085 | 20 | 20 | fits | 90,379 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 896,455 | 8.965 | 20 | 20 | fits | 52,684 | 21 | 0.648 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 155,309 | 1.553 | 20 | 200 | fits | 156,249 | 251 | 0.470 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 232,617 | 2.326 | 20 | 20 | fits | 97,445 | 86 | 0.648 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 279,246 | 2.792 | 20 | 24 | fits | 87,164 | 53 | 0.515 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 193,142 | 1.931 | 20 | 50 | fits | 97,445 | 86 | 0.648 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 808,588 | 8.086 | 20 | 20 | fits | 70,638 | 30 | 0.661 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 283,426 | 2.834 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 22,325 | 0.223 | 20 | 20 | fits | 28,266 | 21 (35) | 0.816 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 16,458 | 0.165 | 20 | 20 | fits | 24,774 | 17 (14) | 0.850 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 5,673 | 0.057 | 20 | 20 | fits | 24,303 | 18 (14) | 0.846 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 13,674 | 0.137 | 20 | 20 | fits | 28,605 | 21 (35) | 0.822 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 88,795 | 0.888 | 20 | 20 | fits | 27,898 | 8 | 0.819 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 43,807 | 0.438 | 20 | 20 | fits | 43,873 | 12 | 0.884 |
| malformed MRPDU discard | `srp.malformed.if0` | 20,632 | 0.206 | 20 | 20 | fits | 20,698 | 12 | 0.654 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 97,479 | 0.975 | 220 | 220 | fits | 69,263 | 6 | 0.878 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 342,190 | 3.422 | 20 | 20 | fits | 107,768 | 149 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 292,894 | 2.929 | 20 | 200 | fits | 149,643 | 248 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 400,046 | 4.000 | 20 | 200 | fits | 107,768 | 149 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 293,818 | 2.938 | 20 | 20 | fits | 149,643 | 248 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 400,750 | 4.008 | 20 | 20 | fits | 107,768 | 149 | 0.472 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 147,815 | 1.478 | 20 | 24 | fits | 148,001 | 155 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 296,468 | 2.965 | 20 | 24 | fits | 149,643 | 248 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 296,402 | 2.964 | 20 | 50 | fits | 149,643 | 248 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 403,774 | 4.038 | 20 | 50 | fits | 107,768 | 149 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 502,056 | 5.021 | 20 | 20 | fits | 89,877 | 29 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 897,000 | 8.970 | 20 | 20 | fits | 63,176 | 24 | 0.591 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,276,597 | 62.766 | 20 | 20 | MISS ceiling | 17,404 | 13 | 0.605 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,293,926 | 62.939 | 20 | 20 | MISS ceiling | 17,405 | 13 | 0.613 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,311,177 | 63.112 | 20 | 20 | MISS ceiling | 17,308 | 13 | 0.622 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,328,410 | 63.284 | 20 | 20 | MISS ceiling | 17,309 | 13 | 0.622 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,345,641 | 63.456 | 20 | 20 | MISS ceiling | 17,294 | 13 | 0.622 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 159,612 | 1.596 | 20 | 200 | fits | 148,769 | 208 | 0.418 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 248,330 | 2.483 | 20 | 200 | fits | 89,334 | 176 | 0.408 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 155,290 | 1.553 | 20 | 20 | fits | 148,769 | 208 | 0.418 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,192,973 | 61.930 | 20 | 20 | MISS ceiling | 28,445 | 15 | 0.754 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,930 | 1.589 | 20 | 24 | fits | 148,769 | 208 | 0.418 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,168,014 | 61.680 | 20 | 24 | MISS ceiling | 133,966 | 106 | 0.391 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 157,874 | 1.579 | 20 | 50 | fits | 148,769 | 208 | 0.418 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 246,812 | 2.468 | 20 | 50 | fits | 89,334 | 176 | 0.408 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 336,466 | 3.365 | 20 | 20 | fits | 89,720 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 733,956 | 7.340 | 20 | 20 | fits | 52,993 | 20 | 0.657 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,088 | 0.111 | 20 | 50 | fits | 26,390 | 43 | 0.720 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 20,685 | 0.207 | 20 | 50 | fits | 22,741 | 35 | 0.705 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 13,975 | 0.140 | 20 | 50 | fits | 26,666 | 41 | 0.671 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 17,343 | 0.173 | 20 | 50 | fits | 27,805 | 61 | 0.643 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,507 | 0.195 | 20 | 50 | fits | 27,805 | 61 | 0.643 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,811 | 0.088 | 20 | 50 | fits | 20,372 | 30 | 0.629 |
| LINK_UP | `adp.link_up.if0` | 2,785 | 0.028 | 20 | 200 | fits | 26,390 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,387 | 0.174 | 20 | 200 | fits | 21,319 | 23 (39) | 0.714 |
| GM_CHANGE | `adp.gm_change.if0` | 2,630 | 0.026 | 20 | 200 | fits | 16,000 | 17 (11) | 0.704 |
| LINK_UP | `adp.link_up.if0` | 2,785 | 0.028 | 20 | 200 | fits | 26,390 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,387 | 0.174 | 20 | 200 | fits | 21,319 | 23 (39) | 0.714 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,393 | 0.044 | 20 | 200 | fits | 15,870 | 16 (31) | 0.659 |
| BIND_RX | `acmp.bind_rx.if0` | 17,648 | 0.176 | 20 | 20 | fits | 39,276 | 26 (77) | 0.791 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,740 | 0.097 | 20 | 20 | fits | 31,993 | 19 (32) | 0.842 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,486 | 0.105 | 20 | 20 | fits | 24,079 | 15 (47) | 0.757 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,167 | 0.132 | 20 | 20 | fits | 39,309 | 18 (50) | 0.843 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,534 | 0.105 | 20 | 20 | fits | 25,319 | 17 (48) | 0.764 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,994 | 0.100 | 20 | 20 | fits | 23,565 | 16 (48) | 0.729 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,922 | 0.089 | 20 | 20 | fits | 23,093 | 16 (48) | 0.729 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,164 | 0.092 | 20 | 20 | fits | 23,012 | 16 (48) | 0.727 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 140,272 | 1.403 | 20 | 24 | fits | 146,123 | 92 | 0.332 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 165,166 | 1.652 | 20 | 24 | fits | 138,532 | 69 | 0.311 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 129,283 | 1.293 | 20 | 24 | fits | 40,914 | 17 | 0.694 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 287,927 | 2.879 | 20 | 24 | fits | 91,751 | 18 | 0.668 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 251,598 | 2.516 | 20 | 24 | fits | 93,958 | 17 | 0.677 |
| LINK_UP | `fixture.link_up.if0` | 2,785 | 0.028 | 20 | 200 | fits | 26,390 | 43 (11) | 0.720 |
| malformed MRPDU discard | `fixture.malformed.if0` | 21,009 | 0.210 | 20 | 20 | fits | 21,075 | 12 | 0.713 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 32,306 | 0.323 | 20 | 24 | fits | 45,602 | 43 | 0.772 |
| LINK_DOWN | `fixture.link_down.if0` | 2,743 | 0.027 | 20 | 200 | fits | 27,324 | 23 (9) | 0.789 |
| BIND_RX | `fixture.bind_rx.if0` | 18,443 | 0.184 | 20 | 20 | fits | 40,445 | 26 (77) | 0.805 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 8,400 | 0.084 | 20 | 20 | fits | 35,938 | 29 (35) | 0.795 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 13,349 | 0.133 | 20 | 20 | fits | 24,654 | 13 (29) | 0.822 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 87,782 | 0.878 | 20 | 200 | fits | 87,886 | 75 | 0.736 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 87,782 | 0.878 | 20 | 200 | fits | 87,886 | 75 | 0.736 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 87,508 | 0.875 | 20 | 20 | fits | 87,886 | 75 | 0.736 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 87,508 | 0.875 | 20 | 20 | fits | 87,886 | 75 | 0.736 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 87,716 | 0.877 | 20 | 24 | fits | 87,886 | 75 | 0.736 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 87,716 | 0.877 | 20 | 24 | fits | 87,886 | 75 | 0.736 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 87,650 | 0.876 | 20 | 50 | fits | 87,886 | 75 | 0.736 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 87,650 | 0.876 | 20 | 50 | fits | 87,886 | 75 | 0.736 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 87,584 | 0.876 | 20 | 20 | fits | 87,886 | 75 | 0.736 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 87,584 | 0.876 | 20 | 20 | fits | 87,886 | 75 | 0.736 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
