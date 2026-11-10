### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 81 paths and 6 of 141 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.233 (0.408) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.111 (0.208) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.076 (0.213) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.143 (0.406) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.128 (0.232) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.114 (0.207) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.115 (0.215) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.124 (0.230) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.088 (0.258) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.142 (0.408) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.142 (0.405) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.217 (0.550) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.143 (0.420) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.083 (0.434) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.055 (0.211) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.160 (0.342) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.040 (0.118) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.022 (0.113) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.023 (0.251) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.023 (0.231) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.115 (0.235) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.100 (0.323) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.125 (0.333) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.178 (0.404) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.157 (0.378) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.160 (0.376) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.184 (0.406) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.211 (0.419) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.166 (0.383) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.229 (0.453) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.140 (0.361) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.139 (0.359) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.181 (0.398) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.165 (0.379) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.175 (0.395) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.133 (0.350) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.183 (0.400) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.174 (0.398) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.147 (0.359) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.145 (0.369) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.150 (0.364) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.189 (0.409) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.181 (0.402) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.109 (0.229) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.307 (0.557) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.121 (0.341) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.266 (0.488) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.417 (0.655) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.389 (0.606) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.471 (0.690) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.460 (0.681) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.428 (0.635) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.460 (0.691) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.401 (0.607) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.433 (0.638) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.716 (5.411) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 6.606 (7.813) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.095 (0.370) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.672 (2.351) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.429 (62.562) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.271 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.286 (0.377) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.198 (0.438) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.108 (0.184) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.119 (0.231) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.178 (0.438) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.115 (0.339) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.523 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.767 | fits | 11 acmp | 5 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.566 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 7.760 | fits | 7 adp | 5 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.559 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.598 | MISS ceiling | 15 aecp | 5 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.549 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.261 | fits | 6 maap | 5 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 3.548 | fits | 0 srp | 5 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 4.766 | fits | 31 srp | 5 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.806 (1.183) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.365 (0.366) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.151 (0.152) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.791 (0.863) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 5.986 | 8 | 156,781 (1.568) | yes | - |
| backlog-adp | 0 | 8.562 | 8 | 153,579 (1.536) | yes | - |
| backlog-adp-refill | 0 | 40.593 | 23 | 147,458 (1.475) | yes | - |
| backlog-owed | 0 | 360.322 | 51 | 146,582 (1.466) | yes | - |
| fixture | 0 | 1.095 | 2 | 75,258 (0.753) | yes | - |

Composed maximum over the 4 backlog windows: 156,781 CPU cycles (1.568 ms), backlog.
Over the windows that released their whole load only: 156,781 (1.568 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3597 | 0 | 63,200 (0.632) | fits |
| adp-advertise | 592 | 0 | 63,200 (0.632) | fits |
| acmp-noresp | 2019 | 0 | 63,200 (0.632) | fits |
| save | 603 | 0 | 63,200 (0.632) | fits |
| srp | 285 | 0 | 86,514 (0.865) | fits |
| backlog | 283 | 0 | 156,781 (1.568) | fits |
| backlog-adp | 308 | 0 | 153,579 (1.536) | fits |
| backlog-adp-refill | 323 | 0 | 147,458 (1.475) | fits |
| backlog-owed | 332 | 0 | 149,342 (1.493) | fits |
| acmp-disc | 931 | 0 | 63,200 (0.632) | fits |
| maap | 176 | 0 | 63,200 (0.632) | fits |
| adp-link | 88 | 0 | 63,200 (0.632) | fits |
| adp-gm | 87 | 0 | 63,200 (0.632) | fits |
| adp-discover | 87 | 0 | 63,200 (0.632) | fits |
| control | 87 | 0 | 63,200 (0.632) | fits |
| aecp-fanout | 110 | 0 | 63,200 (0.632) | fits |
| acmp-cmd | 83 | 0 | 63,200 (0.632) | fits |
| aecp | 110 | 0 | 63,200 (0.632) | fits |
| fixture | 150 | 0 | 75,258 (0.753) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save | 2018.429 | 4,070 | 102 | - | 10.804 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 92,283 (0.923) | 78,129 (0.781) |
| adp-advertise | 578 | 18,346 (0.183) | 3,119 (0.031) |
| acmp-noresp | 615 | 92,202 (0.922) | 78,030 (0.780) |
| save | 585 | 91,288 (0.913) | 77,929 (0.779) |
| srp | 271 | 18,346 (0.183) | 3,119 (0.031) |
| backlog | 265 | 18,346 (0.183) | 3,119 (0.031) |
| backlog-adp | 271 | 18,346 (0.183) | 3,119 (0.031) |
| backlog-adp-refill | 274 | 18,346 (0.183) | 3,119 (0.031) |
| backlog-owed | 306 | 18,346 (0.183) | 3,119 (0.031) |
| acmp-disc | 305 | 92,087 (0.921) | 78,030 (0.780) |
| maap | 166 | 18,346 (0.183) | 3,119 (0.031) |
| adp-link | 80 | 18,346 (0.183) | 3,119 (0.031) |
| adp-gm | 80 | 18,346 (0.183) | 3,119 (0.031) |
| adp-discover | 80 | 18,346 (0.183) | 3,119 (0.031) |
| control | 80 | 18,346 (0.183) | 3,119 (0.031) |
| aecp-fanout | 79 | 18,346 (0.183) | 3,119 (0.031) |
| acmp-cmd | 65 | 18,346 (0.183) | 3,119 (0.031) |
| aecp | 79 | 18,346 (0.183) | 3,119 (0.031) |
| fixture | 54 | 14,750 (0.147) | 3,081 (0.031) |

Longest pass that carries a step: 92,283 CPU cycles (0.923 ms), acmp-notk; longest step: 78,129 (0.781 ms), acmp-notk.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 8,260 | 0.083 | 20 | 20 | fits | 28,918 | 19 (14) | 0.891 |
| LINK_UP | `adp.link_up.if0` | 2,343 | 0.023 | 20 | 200 | fits | 23,064 | 43 (11) | 0.701 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,025 | 0.100 | 20 | 200 | fits | 19,642 | 23 (39) | 0.690 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 11,477 | 0.115 | 20 | 200 | fits | 2,370 | 10 (11) | 0.429 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 21,438 | 0.214 | 20 | 20 | fits | 27,129 | 21 (35) | 0.814 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 14,336 | 0.143 | 20 | 20 | fits | 21,349 | 17 (14) | 0.856 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 5,535 | 0.055 | 20 | 20 | fits | 21,083 | 18 (14) | 0.852 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 14,192 | 0.142 | 20 | 20 | fits | 27,317 | 21 (35) | 0.818 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 79,122 | 0.791 | 20 | 20 | fits | 63,200 | 6 | 0.878 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 36,547 | 0.365 | 20 | 20 | fits | 36,612 | 12 | 0.887 |
| malformed MRPDU discard | `srp.malformed.if0` | 14,423 | 0.144 | 20 | 20 | fits | 14,488 | 12 | 0.638 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 80,581 | 0.806 | 220 | 220 | fits | 86,514 | 9 | 0.871 |
| an event behind 15 others | `backlog.event.if0` | 167,238 | 1.672 | 20 | 200 | fits | 78,278 | 109 | 0.505 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 471,586 | 4.716 | 20 | 20 | fits | 145,286 | 110 | 0.415 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 156,573 | 1.566 | 20 | 200 | fits | 156,781 | 204 | 0.469 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 328,841 | 3.288 | 20 | 200 | fits | 94,599 | 55 | 0.587 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 152,314 | 1.523 | 20 | 20 | fits | 156,781 | 204 | 0.469 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 535,823 | 5.358 | 20 | 20 | fits | 145,286 | 110 | 0.415 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 155,899 | 1.559 | 20 | 24 | fits | 156,781 | 204 | 0.469 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 563,317 | 5.633 | 20 | 24 | fits | 24,059 | 18 | 0.656 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 154,859 | 1.549 | 20 | 50 | fits | 156,781 | 204 | 0.469 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 327,346 | 3.273 | 20 | 50 | fits | 94,599 | 55 | 0.587 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 354,772 | 3.548 | 20 | 20 | fits | 24,454 | 53 | 0.228 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 391,437 | 3.914 | 20 | 20 | fits | 17,125 | 36 | 0.067 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 660,559 | 6.606 | 20 | 20 | fits | 153,579 | 116 | 0.502 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 141,475 | 1.415 | 20 | 200 | fits | 146,157 | 197 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 776,018 | 7.760 | 20 | 200 | fits | 153,579 | 116 | 0.502 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 142,387 | 1.424 | 20 | 20 | fits | 146,157 | 197 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 776,714 | 7.767 | 20 | 20 | fits | 153,579 | 116 | 0.502 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 145,972 | 1.460 | 20 | 24 | fits | 146,157 | 197 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 818,024 | 8.180 | 20 | 24 | fits | 37,875 | 30 | 0.534 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 144,932 | 1.449 | 20 | 50 | fits | 146,157 | 197 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 626,115 | 6.261 | 20 | 50 | fits | 147,458 | 173 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 278,567 | 2.786 | 20 | 20 | fits | 134,090 | 95 | 0.571 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 476,577 | 4.766 | 20 | 20 | fits | 77,323 | 36 | 0.491 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 9,548 | 0.095 | 20 | 20 | fits | 21,834 | 19 | 0.776 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 141,475 | 1.415 | 20 | 200 | fits | 146,157 | 197 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 24,514 | 0.245 | 20 | 200 | fits | 21,834 | 19 | 0.776 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 142,387 | 1.424 | 20 | 20 | fits | 146,157 | 197 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 765,905 | 7.659 | 20 | 20 | fits | 142,770 | 106 | 0.471 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 145,972 | 1.460 | 20 | 24 | fits | 146,157 | 197 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 806,798 | 8.068 | 20 | 24 | fits | 37,458 | 30 | 0.517 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 144,932 | 1.449 | 20 | 50 | fits | 146,157 | 197 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 626,115 | 6.261 | 20 | 50 | fits | 147,458 | 173 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 278,567 | 2.786 | 20 | 20 | fits | 134,090 | 95 | 0.571 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 476,577 | 4.766 | 20 | 20 | fits | 77,323 | 36 | 0.491 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,242,896 | 62.429 | 20 | 20 | MISS ceiling | 13,548 | 12 | 0.656 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,027,128 | 360.271 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,027,053 | 360.271 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,026,978 | 360.270 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,026,903 | 360.269 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 145,814 | 1.458 | 20 | 200 | fits | 144,888 | 209 | 0.460 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 615,594 | 6.156 | 20 | 200 | fits | 146,582 | 149 | 0.506 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 141,555 | 1.416 | 20 | 20 | fits | 144,888 | 209 | 0.460 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 625,684 | 6.257 | 20 | 20 | fits | 14,565 | 13 | 0.687 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 145,140 | 1.451 | 20 | 24 | fits | 144,888 | 209 | 0.460 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,159,797 | 61.598 | 20 | 24 | MISS ceiling | 145,338 | 127 | 0.315 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 144,100 | 1.441 | 20 | 50 | fits | 144,888 | 209 | 0.460 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 614,099 | 6.141 | 20 | 50 | fits | 146,582 | 149 | 0.506 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 278,762 | 2.788 | 20 | 20 | fits | 135,117 | 95 | 0.578 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 465,437 | 4.654 | 20 | 20 | fits | 78,584 | 37 | 0.503 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,710 | 0.057 | 20 | 20 | fits | 20,237 | 13 (29) | 0.792 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,615 | 0.076 | 20 | 20 | fits | 21,258 | 19 (35) | 0.770 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 14,222 | 0.142 | 20 | 20 | fits | 26,919 | 21 (12) | 0.810 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,942 | 0.119 | 20 | 50 | fits | 23,064 | 43 | 0.701 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 9,466 | 0.095 | 20 | 50 | fits | 19,506 | 35 | 0.661 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 11,485 | 0.115 | 20 | 50 | fits | 19,903 | 35 | 0.678 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 17,765 | 0.178 | 20 | 50 | fits | 25,788 | 61 | 0.604 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,800 | 0.198 | 20 | 50 | fits | 25,788 | 61 | 0.604 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 10,767 | 0.108 | 20 | 50 | fits | 18,366 | 30 | 0.569 |
| LINK_UP | `adp.link_up.if0` | 2,343 | 0.023 | 20 | 200 | fits | 23,064 | 43 (11) | 0.701 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,025 | 0.100 | 20 | 200 | fits | 19,642 | 23 (39) | 0.690 |
| LINK_DOWN | `adp.link_down.if0` | 2,054 | 0.021 | 20 | 200 | fits | 23,155 | 23 (9) | 0.750 |
| LINK_UP | `adp.link_up.if0` | 2,343 | 0.023 | 20 | 200 | fits | 23,064 | 43 (11) | 0.701 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,025 | 0.100 | 20 | 200 | fits | 19,642 | 23 (39) | 0.690 |
| GM_CHANGE | `adp.gm_change.if0` | 2,157 | 0.022 | 20 | 200 | fits | 11,313 | 17 (11) | 0.620 |
| LINK_UP | `adp.link_up.if0` | 2,343 | 0.023 | 20 | 200 | fits | 23,064 | 43 (11) | 0.701 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,025 | 0.100 | 20 | 200 | fits | 19,642 | 23 (39) | 0.690 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,006 | 0.040 | 20 | 200 | fits | 11,752 | 16 (31) | 0.547 |
| LINK_UP | `adp.link_up.if0` | 2,343 | 0.023 | 20 | 200 | fits | 23,064 | 43 (11) | 0.701 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,025 | 0.100 | 20 | 200 | fits | 19,642 | 23 (39) | 0.690 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,006 | 0.040 | 20 | 200 | fits | 11,752 | 16 (31) | 0.547 |
| set_name | `aecp_fanout.set_name.if0` | 45,970 | 0.460 | 20 | 24 | fits | 55,352 | 88 | 0.527 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 45,979 | 0.460 | 20 | 24 | fits | 50,918 | 77 | 0.568 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 39,217 | 0.392 | 20 | 24 | fits | 45,668 | 78 | 0.489 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 42,786 | 0.428 | 20 | 24 | fits | 46,015 | 77 | 0.500 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 47,140 | 0.471 | 20 | 24 | fits | 51,818 | 66 | 0.587 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 41,720 | 0.417 | 20 | 24 | fits | 49,564 | 65 | 0.550 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 40,091 | 0.401 | 20 | 24 | fits | 47,932 | 66 | 0.542 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 38,852 | 0.389 | 20 | 24 | fits | 45,185 | 77 | 0.484 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 43,304 | 0.433 | 20 | 24 | fits | 45,274 | 78 | 0.487 |
| BIND_RX | `acmp.bind_rx.if0` | 23,291 | 0.233 | 20 | 20 | fits | 40,770 | 26 (77) | 0.781 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,784 | 0.088 | 20 | 20 | fits | 25,827 | 20 (32) | 0.821 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 12,758 | 0.128 | 20 | 20 | fits | 23,240 | 15 (47) | 0.747 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 16,005 | 0.160 | 20 | 20 | fits | 34,230 | 18 (50) | 0.813 |
| PROBE_TX | `acmp.probe_tx.if0` | 12,375 | 0.124 | 20 | 20 | fits | 22,973 | 17 (48) | 0.724 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,457 | 0.115 | 20 | 20 | fits | 21,472 | 16 (48) | 0.664 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 11,120 | 0.111 | 20 | 20 | fits | 20,810 | 16 (48) | 0.661 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 11,393 | 0.114 | 20 | 20 | fits | 20,664 | 16 (48) | 0.658 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 10,896 | 0.109 | 20 | 24 | fits | 22,918 | 20 | 0.764 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 22,909 | 0.229 | 20 | 24 | fits | 27,122 | 20 | 0.689 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 14,002 | 0.140 | 20 | 24 | fits | 21,641 | 20 | 0.686 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 18,285 | 0.183 | 20 | 24 | fits | 21,973 | 20 | 0.698 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 14,969 | 0.150 | 20 | 24 | fits | 22,113 | 20 | 0.681 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 18,921 | 0.189 | 20 | 24 | fits | 22,725 | 20 | 0.702 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 18,097 | 0.181 | 20 | 24 | fits | 21,916 | 20 | 0.701 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 13,921 | 0.139 | 20 | 24 | fits | 21,560 | 20 | 0.701 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 18,075 | 0.181 | 20 | 24 | fits | 21,514 | 20 | 0.717 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 16,456 | 0.165 | 20 | 24 | fits | 23,510 | 21 | 0.590 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 17,510 | 0.175 | 20 | 24 | fits | 21,156 | 20 | 0.739 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 13,289 | 0.133 | 20 | 24 | fits | 20,617 | 20 | 0.718 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 17,356 | 0.174 | 20 | 24 | fits | 21,779 | 20 | 0.708 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 14,747 | 0.147 | 20 | 24 | fits | 21,566 | 20 | 0.686 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 14,533 | 0.145 | 20 | 24 | fits | 22,100 | 20 | 0.721 |
| get_configuration | `aecp.get_configuration.if0` | 15,655 | 0.157 | 20 | 24 | fits | 19,580 | 20 | 0.724 |
| entity_available | `aecp.entity_available.if0` | 12,454 | 0.125 | 20 | 24 | fits | 18,933 | 20 | 0.692 |
| get_name | `aecp.get_name.if0` | 18,415 | 0.184 | 20 | 24 | fits | 22,516 | 20 | 0.748 |
| get_counters | `aecp.get_counters.if0` | 15,992 | 0.160 | 20 | 24 | fits | 23,356 | 25 | 0.709 |
| get_avb_info | `aecp.get_avb_info.if0` | 17,788 | 0.178 | 20 | 24 | fits | 21,805 | 20 | 0.761 |
| unknown_command | `aecp.unknown_command.if0` | 12,057 | 0.121 | 20 | 24 | fits | 19,727 | 20 | 0.724 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 16,648 | 0.166 | 20 | 24 | fits | 19,843 | 20 | 0.728 |
| set_name | `aecp.set_name.if0` | 30,688 | 0.307 | 20 | 24 | fits | 37,545 | 42 | 0.733 |
| lock_entity | `aecp.lock_entity.if0` | 21,072 | 0.211 | 20 | 24 | fits | 29,563 | 32 | 0.750 |
| unlock_entity | `aecp.unlock_entity.if0` | 26,593 | 0.266 | 20 | 24 | fits | 28,941 | 33 | 0.743 |
| LINK_UP | `fixture.link_up.if0` | 2,343 | 0.023 | 20 | 200 | fits | 23,064 | 43 (11) | 0.701 |
| malformed MRPDU discard | `fixture.malformed.if0` | 15,136 | 0.151 | 20 | 20 | fits | 15,201 | 12 | 0.699 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 28,553 | 0.286 | 20 | 24 | fits | 37,676 | 42 | 0.731 |
| LINK_DOWN | `fixture.link_down.if0` | 2,345 | 0.023 | 20 | 200 | fits | 25,103 | 23 (9) | 0.773 |
| BIND_RX | `fixture.bind_rx.if0` | 22,626 | 0.226 | 20 | 20 | fits | 40,430 | 26 (77) | 0.775 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 21,696 | 0.217 | 20 | 20 | fits | 33,812 | 29 (35) | 0.777 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 14,347 | 0.143 | 20 | 20 | fits | 20,802 | 13 (29) | 0.800 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 75,155 | 0.752 | 20 | 200 | fits | 75,258 | 51 | 0.737 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 75,155 | 0.752 | 20 | 200 | fits | 75,258 | 51 | 0.737 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 74,885 | 0.749 | 20 | 20 | fits | 75,258 | 51 | 0.737 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 74,885 | 0.749 | 20 | 20 | fits | 75,258 | 51 | 0.737 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 75,090 | 0.751 | 20 | 24 | fits | 75,258 | 51 | 0.737 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 75,090 | 0.751 | 20 | 24 | fits | 75,258 | 51 | 0.737 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 75,025 | 0.750 | 20 | 50 | fits | 75,258 | 51 | 0.737 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 75,025 | 0.750 | 20 | 50 | fits | 75,258 | 51 | 0.737 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 74,960 | 0.750 | 20 | 20 | fits | 75,258 | 51 | 0.737 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 74,960 | 0.750 | 20 | 20 | fits | 75,258 | 51 | 0.737 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
