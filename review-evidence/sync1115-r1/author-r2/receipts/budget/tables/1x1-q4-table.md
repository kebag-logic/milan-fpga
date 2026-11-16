### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 52 paths and 7 of 225 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.191 (0.414) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.087 (0.245) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.184 (0.532) | fits | 0 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.104 (0.263) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.089 (0.244) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.099 (0.254) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.107 (0.267) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.095 (0.322) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.148 (0.507) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.277 (0.532) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.141 (0.494) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.250 (0.494) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.130 (0.384) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.045 (0.170) | fits | 0 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.175) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.026 (0.264) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.026 (0.268) | fits | 0 events | 3 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.183 (0.513) | fits | 0 events | 2 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.175 (3.502) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.993 (2.369) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.925 (4.286) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.061 (3.422) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.294 (1.464) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-7.adp_available.if0` (backlog-adp@verify-aged2-7) | 4.237 (4.811) | fits | 7 adp | 14 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.956 (63.094) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.707 (63.849) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.314 (0.458) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.273 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.571 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.986 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.878 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 9.072 | fits | 31 srp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.171 (0.509) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.091 (0.222) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.100 (0.268) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.149 (0.509) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.203 (0.525) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.491 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.acmp.first.if0` (backlog-adp@verify-aged2-5) | 3.147 | fits | 0 acmp | 16 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.049 | MISS ceiling | 11 acmp | 16 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.adp.first.if0` (backlog-adp@verify-aged2-5) | 3.137 | fits | 0 adp | 16 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.adp.last.if0` (backlog-adp@verify-aged2-7) | 4.809 | fits | 7 adp | 16 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-7.service.aecp.first.if0` (backlog-adp@verify-aged1-7) | 1.647 | fits | 0 aecp | 16 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.782 | MISS ceiling | 15 aecp | 16 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.maap.first.if0` (backlog-adp@verify-aged2-5) | 3.173 | fits | 0 maap | 16 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.maap.last.if0` (backlog-adp@verify-aged2-7) | 4.846 | fits | 6 maap | 16 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.srp.first.if0` (backlog-adp@verify-aged2-5) | 5.852 | fits | 0 srp | 16 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.srp.last.if0` (backlog-adp@verify-aged2-5) | 10.909 | fits | 31 srp | 16 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.894 (0.985) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.447 (0.448) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.219 (0.219) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.772 (0.855) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-aged2-7 | 1 | 11.516 | 11 | 148,500 (1.485) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.430 | 12 | 150,799 (1.508) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.306 | 11 | 150,670 (1.507) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.323 | 11 | 150,717 (1.507) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.876 | 13 | 150,670 (1.507) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.280 | 11 | 150,748 (1.507) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.583 | 13 | 150,701 (1.507) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.436 | 12 | 152,425 (1.524) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 12.269 | 12 | 150,618 (1.506) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.320 | 11 | 150,618 (1.506) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.341 | 11 | 150,571 (1.506) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.644 | 12 | 151,783 (1.518) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.501 | 12 | 150,757 (1.508) | yes | - |
| backlog-adp | 0 | 10.461 | 11 | 150,933 (1.509) | yes | - |
| backlog-owed | 0 | 64.368 | 26 | 149,815 (1.498) | yes | - |
| fixture | 0 | 1.380 | 2 | 88,440 (0.884) | yes | - |

Composed maximum over 2 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill not run): 150,933 CPU cycles (1.509 ms), backlog-adp.
Over the windows that released their whole load only: 150,933 (1.509 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@program-aged2-7 | 855 | 0 | 151,670 (1.517) | fits |
| backlog-adp@program-aged1-1 | 751 | 0 | 150,799 (1.508) | fits |
| backlog-adp@program-aged1-3 | 765 | 0 | 150,670 (1.507) | fits |
| backlog-adp@program-aged1-5 | 780 | 0 | 150,717 (1.507) | fits |
| backlog-adp@program-aged1-7 | 797 | 0 | 150,670 (1.507) | fits |
| backlog-adp@verify-aged2-1 | 906 | 0 | 150,748 (1.507) | fits |
| backlog-adp@verify-aged2-3 | 923 | 0 | 150,701 (1.507) | fits |
| backlog-adp@verify-aged2-5 | 937 | 0 | 152,425 (1.524) | fits |
| backlog-adp@verify-aged2-7 | 952 | 0 | 150,618 (1.506) | fits |
| backlog-adp@verify-aged1-1 | 847 | 0 | 150,618 (1.506) | fits |
| backlog-adp@verify-aged1-3 | 862 | 0 | 150,571 (1.506) | fits |
| backlog-adp@verify-aged1-5 | 878 | 0 | 151,783 (1.518) | fits |
| backlog-adp@verify-aged1-7 | 893 | 0 | 150,757 (1.508) | fits |
| save-held | 1466 | 0 | 158,049 (1.580) | fits |
| acmp-noresp | 2024 | 0 | 41,099 (0.411) | fits |
| srp | 290 | 0 | 56,298 (0.563) | fits |
| backlog-adp | 314 | 0 | 150,933 (1.509) | fits |
| backlog-owed | 311 | 0 | 149,815 (1.498) | fits |
| maap | 178 | 0 | 30,379 (0.304) | fits |
| adp-gm | 88 | 0 | 30,379 (0.304) | fits |
| control | 88 | 0 | 30,379 (0.304) | fits |
| acmp-cmd | 85 | 0 | 41,099 (0.411) | fits |
| aecp-largest-notice | 107 | 0 | 146,403 (1.464) | fits |
| fixture | 151 | 0 | 88,440 (0.884) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@program-aged2-7 | 2 | +4.045 ms, 80,340 (0.803 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.750 (20) | 9.250 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.096 (20) | 9.904 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.975 (20) | 10.025 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.993 (20) | 10.007 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.999 (20) | 10.001 |
| backlog-adp@verify-aged2-1 | 2 | +9.147 ms, 77,468 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 10.748 (20) | 9.252 |
| backlog-adp@verify-aged2-3 | 2 | +6.692 ms, 77,468 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.763 (20) | 9.237 |
| backlog-adp@verify-aged2-5 | 2 | +4.236 ms, 77,651 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.909 (20) | 9.091 |
| backlog-adp@verify-aged2-7 | 2 | +3.038 ms, 77,307 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.781 (20) | 9.219 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.029 (20) | 9.971 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.049 (20) | 9.951 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.887 (20) | 10.113 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.098 (20) | 9.902 |

Least margin over the aged windows: 9.091 ms, `backlog-adp@verify-aged2-5.service.srp.last.if0` at 10.909 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 2019.186 | 4,070 | 102 | - | 15.666 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@program-aged2-7 | 327 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@program-aged1-1 | 326 | 97,240 (0.972) | 78,891 (0.789) |
| backlog-adp@program-aged1-3 | 326 | 97,240 (0.972) | 78,891 (0.789) |
| backlog-adp@program-aged1-5 | 326 | 97,240 (0.972) | 78,891 (0.789) |
| backlog-adp@program-aged1-7 | 327 | 97,240 (0.972) | 78,891 (0.789) |
| backlog-adp@verify-aged2-1 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged2-3 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged2-5 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged2-7 | 356 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged1-1 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged1-3 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged1-5 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged1-7 | 356 | 97,240 (0.972) | 78,381 (0.784) |
| save-held | 722 | 95,305 (0.953) | 78,731 (0.787) |
| acmp-noresp | 615 | 97,278 (0.973) | 78,246 (0.782) |
| srp | 271 | 22,757 (0.228) | 2,490 (0.025) |
| backlog-adp | 271 | 22,757 (0.228) | 2,511 (0.025) |
| backlog-owed | 276 | 22,757 (0.228) | 2,490 (0.025) |
| maap | 165 | 22,757 (0.228) | 2,490 (0.025) |
| adp-gm | 79 | 22,757 (0.228) | 2,490 (0.025) |
| control | 79 | 22,757 (0.228) | 2,490 (0.025) |
| acmp-cmd | 65 | 22,757 (0.228) | 2,490 (0.025) |
| aecp-largest-notice | 78 | 22,757 (0.228) | 2,490 (0.025) |
| fixture | 54 | 20,221 (0.202) | 2,490 (0.025) |

Longest pass that carries a step: 97,278 CPU cycles (0.973 ms), acmp-noresp; longest step: 78,891 (0.789 ms), backlog-adp@program-aged1-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 342,168 | 3.422 | 20 | 20 | fits | 109,541 | 154 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 290,215 | 2.902 | 20 | 200 | fits | 148,500 | 253 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 399,140 | 3.991 | 20 | 200 | fits | 109,541 | 154 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 291,139 | 2.911 | 20 | 20 | fits | 148,500 | 253 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 399,844 | 3.998 | 20 | 20 | fits | 109,541 | 154 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 146,279 | 1.463 | 20 | 24 | fits | 151,670 | 157 | 0.346 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 293,789 | 2.938 | 20 | 24 | fits | 148,500 | 253 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 293,723 | 2.937 | 20 | 50 | fits | 148,500 | 253 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 402,868 | 4.029 | 20 | 50 | fits | 109,541 | 154 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 568,824 | 5.688 | 20 | 20 | fits | 85,682 | 25 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,074,984 | 10.750 | 20 | 20 | fits | 73,795 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 352,740 | 3.527 | 20 | 20 | fits | 99,231 | 142 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 310,211 | 3.102 | 20 | 200 | fits | 149,598 | 253 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 408,826 | 4.088 | 20 | 200 | fits | 99,231 | 142 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 311,135 | 3.111 | 20 | 20 | fits | 149,598 | 253 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 409,530 | 4.095 | 20 | 20 | fits | 99,231 | 142 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 156,616 | 1.566 | 20 | 24 | fits | 150,799 | 153 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 313,785 | 3.138 | 20 | 24 | fits | 149,598 | 253 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 313,719 | 3.137 | 20 | 50 | fits | 149,598 | 253 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 412,554 | 4.126 | 20 | 50 | fits | 99,231 | 142 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 498,529 | 4.985 | 20 | 20 | fits | 86,041 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,009,645 | 10.096 | 20 | 20 | fits | 78,709 | 31 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 347,105 | 3.471 | 20 | 20 | fits | 97,179 | 154 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 299,280 | 2.993 | 20 | 200 | fits | 148,863 | 233 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 395,843 | 3.958 | 20 | 200 | fits | 97,179 | 154 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 300,204 | 3.002 | 20 | 20 | fits | 148,863 | 233 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 396,547 | 3.965 | 20 | 20 | fits | 97,179 | 154 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 154,981 | 1.550 | 20 | 24 | fits | 150,670 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 302,854 | 3.029 | 20 | 24 | fits | 148,863 | 233 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 302,788 | 3.028 | 20 | 50 | fits | 148,863 | 233 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 399,571 | 3.996 | 20 | 50 | fits | 97,179 | 154 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 485,560 | 4.856 | 20 | 20 | fits | 86,055 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 997,454 | 9.975 | 20 | 20 | fits | 86,449 | 28 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 349,016 | 3.490 | 20 | 20 | fits | 97,179 | 154 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 301,191 | 3.012 | 20 | 200 | fits | 148,787 | 233 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 397,754 | 3.978 | 20 | 200 | fits | 97,179 | 154 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 302,115 | 3.021 | 20 | 20 | fits | 148,787 | 233 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 398,458 | 3.985 | 20 | 20 | fits | 97,179 | 154 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 156,968 | 1.570 | 20 | 24 | fits | 150,717 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 304,765 | 3.048 | 20 | 24 | fits | 148,787 | 233 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 304,699 | 3.047 | 20 | 50 | fits | 148,787 | 233 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 401,482 | 4.015 | 20 | 50 | fits | 97,179 | 154 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 492,609 | 4.926 | 20 | 20 | fits | 91,193 | 31 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 999,295 | 9.993 | 20 | 20 | fits | 73,812 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 371,106 | 3.711 | 20 | 20 | fits | 110,424 | 172 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 301,762 | 3.018 | 20 | 200 | fits | 147,465 | 228 | 0.406 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 420,782 | 4.208 | 20 | 200 | fits | 110,424 | 172 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 302,686 | 3.027 | 20 | 20 | fits | 147,465 | 228 | 0.406 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 421,486 | 4.215 | 20 | 20 | fits | 110,424 | 172 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 158,861 | 1.589 | 20 | 24 | fits | 150,670 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 305,336 | 3.053 | 20 | 24 | fits | 147,465 | 228 | 0.406 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 305,270 | 3.053 | 20 | 50 | fits | 147,465 | 228 | 0.406 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 424,510 | 4.245 | 20 | 50 | fits | 110,424 | 172 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 510,419 | 5.104 | 20 | 20 | fits | 85,975 | 24 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 999,926 | 9.999 | 20 | 20 | fits | 60,416 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 333,035 | 3.330 | 20 | 20 | fits | 97,426 | 151 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 298,902 | 2.989 | 20 | 200 | fits | 150,142 | 237 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 395,712 | 3.957 | 20 | 200 | fits | 97,426 | 151 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 299,826 | 2.998 | 20 | 20 | fits | 150,142 | 237 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 396,416 | 3.964 | 20 | 20 | fits | 97,426 | 151 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 153,324 | 1.533 | 20 | 24 | fits | 150,748 | 152 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 302,476 | 3.025 | 20 | 24 | fits | 150,142 | 237 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 302,410 | 3.024 | 20 | 50 | fits | 150,142 | 237 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 399,440 | 3.994 | 20 | 50 | fits | 97,426 | 151 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 485,348 | 4.853 | 20 | 20 | fits | 85,974 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,074,837 | 10.748 | 20 | 20 | fits | 86,459 | 29 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 348,443 | 3.484 | 20 | 20 | fits | 102,552 | 158 | 0.481 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 301,034 | 3.010 | 20 | 200 | fits | 150,381 | 238 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 412,091 | 4.121 | 20 | 200 | fits | 102,552 | 158 | 0.481 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 301,958 | 3.020 | 20 | 20 | fits | 150,381 | 238 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 412,795 | 4.128 | 20 | 20 | fits | 102,552 | 158 | 0.481 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 155,217 | 1.552 | 20 | 24 | fits | 150,701 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 304,608 | 3.046 | 20 | 24 | fits | 150,381 | 238 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 304,542 | 3.045 | 20 | 50 | fits | 150,381 | 238 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 415,819 | 4.158 | 20 | 50 | fits | 102,552 | 158 | 0.481 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 501,643 | 5.016 | 20 | 20 | fits | 85,890 | 24 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,076,261 | 10.763 | 20 | 20 | fits | 73,905 | 25 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 355,234 | 3.552 | 20 | 20 | fits | 105,056 | 157 | 0.475 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 313,744 | 3.137 | 20 | 200 | fits | 152,425 | 242 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 418,184 | 4.182 | 20 | 200 | fits | 105,056 | 157 | 0.475 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 314,668 | 3.147 | 20 | 20 | fits | 152,425 | 242 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 418,888 | 4.189 | 20 | 20 | fits | 105,056 | 157 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 157,322 | 1.573 | 20 | 24 | fits | 150,866 | 153 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 317,318 | 3.173 | 20 | 24 | fits | 152,425 | 242 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 317,252 | 3.173 | 20 | 50 | fits | 152,425 | 242 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 421,912 | 4.219 | 20 | 50 | fits | 105,056 | 157 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 585,165 | 5.852 | 20 | 20 | fits | 85,668 | 25 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,090,906 | 10.909 | 20 | 20 | fits | 74,080 | 24 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 423,696 | 4.237 | 20 | 20 | fits | 105,094 | 163 | 0.421 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 299,073 | 2.991 | 20 | 200 | fits | 148,069 | 231 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 480,858 | 4.809 | 20 | 200 | fits | 105,094 | 163 | 0.421 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 299,997 | 3.000 | 20 | 20 | fits | 148,069 | 231 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 481,562 | 4.816 | 20 | 20 | fits | 105,094 | 163 | 0.421 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 155,568 | 1.556 | 20 | 24 | fits | 150,618 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 302,647 | 3.026 | 20 | 24 | fits | 148,069 | 231 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 302,581 | 3.026 | 20 | 50 | fits | 148,069 | 231 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 484,586 | 4.846 | 20 | 50 | fits | 105,094 | 163 | 0.421 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 570,629 | 5.706 | 20 | 20 | fits | 86,109 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,078,149 | 10.781 | 20 | 20 | fits | 73,765 | 24 | 0.681 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 352,793 | 3.528 | 20 | 20 | fits | 97,179 | 154 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 304,968 | 3.050 | 20 | 200 | fits | 148,876 | 233 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 401,531 | 4.015 | 20 | 200 | fits | 97,179 | 154 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 305,892 | 3.059 | 20 | 20 | fits | 148,876 | 233 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 402,235 | 4.022 | 20 | 20 | fits | 97,179 | 154 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 160,656 | 1.607 | 20 | 24 | fits | 150,618 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 308,542 | 3.085 | 20 | 24 | fits | 148,876 | 233 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 308,476 | 3.085 | 20 | 50 | fits | 148,876 | 233 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 405,259 | 4.053 | 20 | 50 | fits | 97,179 | 154 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 491,271 | 4.913 | 20 | 20 | fits | 86,078 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,002,865 | 10.029 | 20 | 20 | fits | 86,548 | 28 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 354,762 | 3.548 | 20 | 20 | fits | 97,179 | 154 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 306,937 | 3.069 | 20 | 200 | fits | 148,952 | 233 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 403,500 | 4.035 | 20 | 200 | fits | 97,179 | 154 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 307,861 | 3.079 | 20 | 20 | fits | 148,952 | 233 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 404,204 | 4.042 | 20 | 20 | fits | 97,179 | 154 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 162,549 | 1.625 | 20 | 24 | fits | 150,571 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 310,511 | 3.105 | 20 | 24 | fits | 148,952 | 233 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 310,445 | 3.104 | 20 | 50 | fits | 148,952 | 233 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 407,228 | 4.072 | 20 | 50 | fits | 97,179 | 154 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 493,334 | 4.933 | 20 | 20 | fits | 86,172 | 25 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,004,913 | 10.049 | 20 | 20 | fits | 86,215 | 28 | 0.636 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 353,461 | 3.535 | 20 | 20 | fits | 101,299 | 157 | 0.467 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 294,912 | 2.949 | 20 | 200 | fits | 151,783 | 243 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 404,442 | 4.044 | 20 | 200 | fits | 101,299 | 157 | 0.467 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 295,836 | 2.958 | 20 | 20 | fits | 151,783 | 243 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 405,146 | 4.051 | 20 | 20 | fits | 101,299 | 157 | 0.467 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 147,693 | 1.477 | 20 | 24 | fits | 150,571 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 298,486 | 2.985 | 20 | 24 | fits | 151,783 | 243 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 298,420 | 2.984 | 20 | 50 | fits | 151,783 | 243 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 408,170 | 4.082 | 20 | 50 | fits | 101,299 | 157 | 0.467 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 499,133 | 4.991 | 20 | 20 | fits | 91,029 | 30 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 988,713 | 9.887 | 20 | 20 | fits | 60,416 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 363,142 | 3.631 | 20 | 20 | fits | 104,809 | 163 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 308,823 | 3.088 | 20 | 200 | fits | 148,726 | 231 | 0.402 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 413,016 | 4.130 | 20 | 200 | fits | 104,809 | 163 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 309,747 | 3.097 | 20 | 20 | fits | 148,726 | 231 | 0.402 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 413,720 | 4.137 | 20 | 20 | fits | 104,809 | 163 | 0.416 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 164,661 | 1.647 | 20 | 24 | fits | 150,757 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 312,397 | 3.124 | 20 | 24 | fits | 148,726 | 231 | 0.402 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 312,331 | 3.123 | 20 | 50 | fits | 148,726 | 231 | 0.402 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 416,744 | 4.167 | 20 | 50 | fits | 104,809 | 163 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 502,747 | 5.027 | 20 | 20 | fits | 86,069 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,009,751 | 10.098 | 20 | 20 | fits | 73,799 | 24 | 0.682 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 157,109 | 1.571 | 20 | 200 | fits | 158,049 | 258 | 0.452 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 227,304 | 2.273 | 20 | 20 | fits | 90,332 | 77 | 0.685 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 298,578 | 2.986 | 20 | 24 | fits | 80,900 | 49 | 0.556 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 187,829 | 1.878 | 20 | 50 | fits | 90,332 | 77 | 0.685 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 907,203 | 9.072 | 20 | 20 | fits | 86,469 | 28 | 0.643 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 249,063 | 2.491 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 27,676 | 0.277 | 20 | 20 | fits | 32,368 | 27 (35) | 0.811 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 14,085 | 0.141 | 20 | 20 | fits | 28,703 | 23 (14) | 0.836 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 25,018 | 0.250 | 20 | 20 | fits | 28,542 | 24 (14) | 0.841 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 14,778 | 0.148 | 20 | 20 | fits | 29,518 | 21 (35) | 0.815 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 77,178 | 0.772 | 20 | 20 | fits | 28,270 | 8 | 0.772 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,704 | 0.447 | 20 | 20 | fits | 44,770 | 12 | 0.894 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,234 | 0.212 | 20 | 20 | fits | 21,300 | 12 | 0.694 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 89,372 | 0.894 | 220 | 220 | fits | 56,298 | 6 | 0.898 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 354,906 | 3.549 | 20 | 20 | fits | 101,238 | 158 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 296,261 | 2.963 | 20 | 200 | fits | 150,078 | 238 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 405,840 | 4.058 | 20 | 200 | fits | 101,238 | 158 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 297,185 | 2.972 | 20 | 20 | fits | 150,078 | 238 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 406,544 | 4.065 | 20 | 20 | fits | 101,238 | 158 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 150,747 | 1.507 | 20 | 24 | fits | 150,933 | 155 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 299,835 | 2.998 | 20 | 24 | fits | 150,078 | 238 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 299,769 | 2.998 | 20 | 50 | fits | 150,078 | 238 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 409,568 | 4.096 | 20 | 50 | fits | 101,238 | 158 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 495,275 | 4.953 | 20 | 20 | fits | 85,773 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 991,549 | 9.915 | 20 | 20 | fits | 73,604 | 24 | 0.671 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,295,584 | 62.956 | 20 | 20 | MISS ceiling | 18,850 | 13 | 0.654 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,314,432 | 63.144 | 20 | 20 | MISS ceiling | 18,924 | 13 | 0.639 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,333,283 | 63.333 | 20 | 20 | MISS ceiling | 18,908 | 13 | 0.639 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,352,046 | 63.520 | 20 | 20 | MISS ceiling | 18,839 | 13 | 0.646 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,370,730 | 63.707 | 20 | 20 | MISS ceiling | 18,747 | 13 | 0.662 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 154,097 | 1.541 | 20 | 200 | fits | 149,815 | 208 | 0.424 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 239,893 | 2.399 | 20 | 200 | fits | 86,412 | 176 | 0.397 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 149,775 | 1.498 | 20 | 20 | fits | 149,815 | 208 | 0.424 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,204,948 | 62.049 | 20 | 20 | MISS ceiling | 30,221 | 15 | 0.780 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 153,415 | 1.534 | 20 | 24 | fits | 149,815 | 208 | 0.424 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,178,213 | 61.782 | 20 | 24 | MISS ceiling | 139,864 | 106 | 0.402 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 152,359 | 1.524 | 20 | 50 | fits | 149,815 | 208 | 0.424 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 238,375 | 2.384 | 20 | 50 | fits | 86,412 | 176 | 0.397 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 323,936 | 3.239 | 20 | 20 | fits | 85,627 | 24 | 0.781 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 822,988 | 8.230 | 20 | 20 | fits | 74,077 | 24 | 0.673 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,046 | 0.100 | 20 | 50 | fits | 26,823 | 43 | 0.735 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 14,354 | 0.144 | 20 | 50 | fits | 23,538 | 35 | 0.719 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 20,267 | 0.203 | 20 | 50 | fits | 23,427 | 35 | 0.719 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 14,855 | 0.149 | 20 | 50 | fits | 28,377 | 61 | 0.643 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 17,060 | 0.171 | 20 | 50 | fits | 28,377 | 61 | 0.643 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,110 | 0.091 | 20 | 50 | fits | 22,182 | 30 | 0.656 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 26,823 | 43 (11) | 0.735 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,339 | 0.183 | 20 | 200 | fits | 23,214 | 23 (39) | 0.757 |
| GM_CHANGE | `adp.gm_change.if0` | 2,371 | 0.024 | 20 | 200 | fits | 17,509 | 17 (11) | 0.753 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 26,823 | 43 (11) | 0.735 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,339 | 0.183 | 20 | 200 | fits | 23,214 | 23 (39) | 0.757 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,535 | 0.045 | 20 | 200 | fits | 16,961 | 16 (31) | 0.655 |
| BIND_RX | `acmp.bind_rx.if0` | 18,728 | 0.187 | 20 | 20 | fits | 41,099 | 26 (77) | 0.795 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,549 | 0.095 | 20 | 20 | fits | 32,169 | 19 (32) | 0.836 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,398 | 0.104 | 20 | 20 | fits | 26,266 | 15 (47) | 0.783 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 12,971 | 0.130 | 20 | 20 | fits | 38,414 | 18 (50) | 0.825 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,659 | 0.107 | 20 | 20 | fits | 26,740 | 17 (48) | 0.775 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,858 | 0.099 | 20 | 20 | fits | 25,373 | 16 (48) | 0.745 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,714 | 0.087 | 20 | 20 | fits | 24,540 | 16 (48) | 0.739 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,851 | 0.089 | 20 | 20 | fits | 24,360 | 16 (48) | 0.736 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 129,364 | 1.294 | 20 | 24 | fits | 146,403 | 92 | 0.330 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 317,457 | 3.175 | 20 | 24 | fits | 138,000 | 70 | 0.311 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 199,307 | 1.993 | 20 | 24 | fits | 42,014 | 17 | 0.690 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 392,488 | 3.925 | 20 | 24 | fits | 92,122 | 18 | 0.668 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 306,121 | 3.061 | 20 | 24 | fits | 93,495 | 17 | 0.668 |
| LINK_UP | `fixture.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 26,823 | 43 (11) | 0.735 |
| malformed MRPDU discard | `fixture.malformed.if0` | 21,862 | 0.219 | 20 | 20 | fits | 21,928 | 12 | 0.743 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 31,394 | 0.314 | 20 | 24 | fits | 45,830 | 43 | 0.777 |
| LINK_DOWN | `fixture.link_down.if0` | 2,568 | 0.026 | 20 | 200 | fits | 26,416 | 23 (9) | 0.794 |
| BIND_RX | `fixture.bind_rx.if0` | 19,136 | 0.191 | 20 | 20 | fits | 41,410 | 26 (77) | 0.801 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 19,259 | 0.193 | 20 | 20 | fits | 36,876 | 29 (35) | 0.791 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 18,448 | 0.184 | 20 | 20 | fits | 25,232 | 13 (29) | 0.819 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 88,336 | 0.883 | 20 | 200 | fits | 88,440 | 77 | 0.742 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 88,336 | 0.883 | 20 | 200 | fits | 88,440 | 77 | 0.742 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 88,062 | 0.881 | 20 | 20 | fits | 88,440 | 77 | 0.742 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 88,062 | 0.881 | 20 | 20 | fits | 88,440 | 77 | 0.742 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 88,270 | 0.883 | 20 | 24 | fits | 88,440 | 77 | 0.742 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 88,270 | 0.883 | 20 | 24 | fits | 88,440 | 77 | 0.742 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 88,204 | 0.882 | 20 | 50 | fits | 88,440 | 77 | 0.742 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 88,204 | 0.882 | 20 | 50 | fits | 88,440 | 77 | 0.742 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 88,138 | 0.881 | 20 | 20 | fits | 88,440 | 77 | 0.742 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 88,138 | 0.881 | 20 | 20 | fits | 88,440 | 77 | 0.742 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
