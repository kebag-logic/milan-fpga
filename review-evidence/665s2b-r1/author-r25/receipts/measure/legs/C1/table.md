### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 81 paths and 6 of 141 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.230 (0.408) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.107 (0.235) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.072 (0.214) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.130 (0.394) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.125 (0.267) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.109 (0.235) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.125 (0.246) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.127 (0.248) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.084 (0.263) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.207 (0.472) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.192 (0.456) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.150 (0.434) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.131 (0.413) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.106 (0.455) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.093 (0.379) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.142 (0.341) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.049 (0.108) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.023 (0.112) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.028 (0.248) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.026 (0.227) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.087 (0.199) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.180 (0.392) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.120 (0.314) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.195 (0.403) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.175 (0.377) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.152 (0.359) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.195 (0.407) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.184 (0.295) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.079 (0.193) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.243 (0.446) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.141 (0.342) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.141 (0.342) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.097 (0.212) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.161 (0.358) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.090 (0.205) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.128 (0.327) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.194 (0.401) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.185 (0.399) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.143 (0.339) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.100 (0.215) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.143 (0.343) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.196 (0.409) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.200 (0.402) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.193 (0.409) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.258 (0.494) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.122 (0.322) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.177 (0.288) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.449 (0.658) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.407 (0.617) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.457 (0.679) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.493 (0.707) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.458 (0.654) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.476 (0.715) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.465 (0.661) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.468 (0.669) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.928 (5.519) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 6.108 (6.476) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.088 (0.359) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.746 (2.461) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.509 (62.635) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.209 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.280 (0.373) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.151 (0.373) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.103 (0.175) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.120 (0.227) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.129 (0.373) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.174 (0.380) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.551 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.872 | fits | 11 acmp | 5 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.594 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 6.727 | fits | 7 adp | 5 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.587 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.679 | MISS ceiling | 15 aecp | 5 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.577 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 6.712 | fits | 6 maap | 5 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 3.689 | fits | 0 srp | 5 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 4.881 | fits | 31 srp | 5 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.818 (1.183) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.368 (0.369) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.142 (0.143) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.790 (0.859) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.332 | 8 | 159,611 (1.596) | yes | - |
| backlog-adp | 0 | 9.013 | 8 | 155,766 (1.558) | yes | - |
| backlog-adp-refill | 0 | 40.558 | 23 | 153,867 (1.539) | yes | - |
| backlog-owed | 0 | 360.260 | 50 | 146,170 (1.462) | yes | - |
| fixture | 0 | 1.126 | 2 | 80,837 (0.808) | yes | - |

Composed maximum over the 4 backlog windows: 159,611 CPU cycles (1.596 ms), backlog.
Over the windows that released their whole load only: 159,611 (1.596 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3597 | 0 | 63,198 (0.632) | fits |
| adp-advertise | 592 | 0 | 63,198 (0.632) | fits |
| acmp-noresp | 2019 | 0 | 63,198 (0.632) | fits |
| save | 603 | 0 | 63,198 (0.632) | fits |
| srp | 285 | 0 | 85,828 (0.858) | fits |
| backlog | 283 | 0 | 159,611 (1.596) | fits |
| backlog-adp | 308 | 0 | 155,766 (1.558) | fits |
| backlog-adp-refill | 323 | 0 | 153,867 (1.539) | fits |
| backlog-owed | 332 | 0 | 149,858 (1.499) | fits |
| acmp-disc | 931 | 0 | 63,198 (0.632) | fits |
| maap | 176 | 0 | 63,198 (0.632) | fits |
| adp-link | 88 | 0 | 63,198 (0.632) | fits |
| adp-gm | 87 | 0 | 63,198 (0.632) | fits |
| adp-discover | 87 | 0 | 63,198 (0.632) | fits |
| control | 87 | 0 | 63,198 (0.632) | fits |
| aecp-fanout | 109 | 0 | 63,198 (0.632) | fits |
| acmp-cmd | 83 | 0 | 63,198 (0.632) | fits |
| aecp | 110 | 0 | 63,198 (0.632) | fits |
| fixture | 149 | 0 | 80,837 (0.808) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save | 2018.440 | 4,070 | 102 | - | 10.814 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 92,123 (0.921) | 78,449 (0.784) |
| adp-advertise | 578 | 17,761 (0.178) | 3,119 (0.031) |
| acmp-noresp | 615 | 91,821 (0.918) | 78,449 (0.784) |
| save | 585 | 90,849 (0.908) | 78,340 (0.783) |
| srp | 271 | 17,761 (0.178) | 3,119 (0.031) |
| backlog | 265 | 17,761 (0.178) | 3,119 (0.031) |
| backlog-adp | 271 | 17,761 (0.178) | 3,119 (0.031) |
| backlog-adp-refill | 274 | 17,761 (0.178) | 3,119 (0.031) |
| backlog-owed | 306 | 17,914 (0.179) | 3,119 (0.031) |
| acmp-disc | 305 | 91,745 (0.917) | 78,449 (0.784) |
| maap | 166 | 17,761 (0.178) | 3,119 (0.031) |
| adp-link | 80 | 17,712 (0.177) | 3,075 (0.031) |
| adp-gm | 80 | 17,712 (0.177) | 3,075 (0.031) |
| adp-discover | 80 | 17,712 (0.177) | 3,075 (0.031) |
| control | 80 | 17,712 (0.177) | 3,075 (0.031) |
| aecp-fanout | 79 | 17,712 (0.177) | 3,075 (0.031) |
| acmp-cmd | 65 | 17,712 (0.177) | 3,075 (0.031) |
| aecp | 79 | 17,712 (0.177) | 3,075 (0.031) |
| fixture | 54 | 14,284 (0.143) | 2,913 (0.029) |

Longest pass that carries a step: 92,123 CPU cycles (0.921 ms), acmp-notk; longest step: 78,449 (0.784 ms), acmp-notk.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 10,566 | 0.106 | 20 | 20 | fits | 29,605 | 19 (14) | 0.892 |
| LINK_UP | `adp.link_up.if0` | 2,640 | 0.026 | 20 | 200 | fits | 22,720 | 43 (11) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,005 | 0.180 | 20 | 200 | fits | 19,699 | 23 (39) | 0.713 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 8,689 | 0.087 | 20 | 200 | fits | 2,575 | 10 (11) | 0.500 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 15,007 | 0.150 | 20 | 20 | fits | 28,219 | 21 (35) | 0.816 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 13,136 | 0.131 | 20 | 20 | fits | 22,501 | 17 (14) | 0.865 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 9,332 | 0.093 | 20 | 20 | fits | 21,916 | 18 (14) | 0.852 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 20,653 | 0.207 | 20 | 20 | fits | 28,341 | 21 (35) | 0.815 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 78,976 | 0.790 | 20 | 20 | fits | 63,198 | 6 | 0.878 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 36,841 | 0.368 | 20 | 20 | fits | 36,906 | 12 | 0.894 |
| malformed MRPDU discard | `srp.malformed.if0` | 13,631 | 0.136 | 20 | 20 | fits | 13,696 | 12 | 0.537 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 81,839 | 0.818 | 220 | 220 | fits | 85,828 | 9 | 0.858 |
| an event behind 15 others | `backlog.event.if0` | 174,618 | 1.746 | 20 | 200 | fits | 86,444 | 108 | 0.537 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 492,785 | 4.928 | 20 | 20 | fits | 142,616 | 97 | 0.428 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 159,403 | 1.594 | 20 | 200 | fits | 159,611 | 195 | 0.506 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 343,251 | 3.433 | 20 | 200 | fits | 98,013 | 56 | 0.572 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 155,144 | 1.551 | 20 | 20 | fits | 159,611 | 195 | 0.506 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 546,612 | 5.466 | 20 | 20 | fits | 142,616 | 97 | 0.428 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 158,729 | 1.587 | 20 | 24 | fits | 159,611 | 195 | 0.506 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 599,847 | 5.998 | 20 | 24 | fits | 49,800 | 42 | 0.423 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 157,689 | 1.577 | 20 | 50 | fits | 159,611 | 195 | 0.506 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 341,756 | 3.418 | 20 | 50 | fits | 98,013 | 56 | 0.572 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 368,882 | 3.689 | 20 | 20 | fits | 23,988 | 53 | 0.219 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 404,896 | 4.049 | 20 | 20 | fits | 16,743 | 36 | 0.073 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 610,796 | 6.108 | 20 | 20 | fits | 155,766 | 171 | 0.489 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 149,185 | 1.492 | 20 | 200 | fits | 153,867 | 192 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 642,292 | 6.423 | 20 | 200 | fits | 155,766 | 171 | 0.489 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 150,097 | 1.501 | 20 | 20 | fits | 153,867 | 192 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 787,164 | 7.872 | 20 | 20 | fits | 144,176 | 95 | 0.476 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 153,682 | 1.537 | 20 | 24 | fits | 153,867 | 192 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 865,946 | 8.659 | 20 | 24 | fits | 75,347 | 66 | 0.310 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 152,642 | 1.526 | 20 | 50 | fits | 153,867 | 192 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 645,968 | 6.460 | 20 | 50 | fits | 155,766 | 171 | 0.489 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 289,969 | 2.900 | 20 | 20 | fits | 137,782 | 95 | 0.602 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 488,122 | 4.881 | 20 | 20 | fits | 77,207 | 36 | 0.493 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,812 | 0.088 | 20 | 20 | fits | 22,035 | 19 | 0.771 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 149,185 | 1.492 | 20 | 200 | fits | 153,867 | 192 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 23,971 | 0.240 | 20 | 200 | fits | 22,035 | 19 | 0.771 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 150,097 | 1.501 | 20 | 20 | fits | 153,867 | 192 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 777,552 | 7.776 | 20 | 20 | fits | 143,907 | 95 | 0.476 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 153,682 | 1.537 | 20 | 24 | fits | 153,867 | 192 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 856,451 | 8.565 | 20 | 24 | fits | 75,464 | 66 | 0.315 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 152,642 | 1.526 | 20 | 50 | fits | 153,867 | 192 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 636,625 | 6.366 | 20 | 50 | fits | 146,423 | 161 | 0.478 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 289,969 | 2.900 | 20 | 20 | fits | 137,782 | 95 | 0.602 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 488,122 | 4.881 | 20 | 20 | fits | 77,207 | 36 | 0.493 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,250,852 | 62.509 | 20 | 20 | MISS ceiling | 16,068 | 12 | 0.692 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,020,889 | 360.209 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,020,814 | 360.208 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,020,739 | 360.207 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,020,664 | 360.207 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 149,684 | 1.497 | 20 | 200 | fits | 145,526 | 178 | 0.509 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 672,741 | 6.727 | 20 | 200 | fits | 50,173 | 57 | 0.474 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 145,425 | 1.454 | 20 | 20 | fits | 145,526 | 178 | 0.509 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 668,266 | 6.683 | 20 | 20 | fits | 50,173 | 57 | 0.474 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 149,010 | 1.490 | 20 | 24 | fits | 145,526 | 178 | 0.509 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,167,874 | 61.679 | 20 | 24 | MISS ceiling | 146,170 | 126 | 0.269 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 147,970 | 1.480 | 20 | 50 | fits | 145,526 | 178 | 0.509 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 671,246 | 6.712 | 20 | 50 | fits | 50,173 | 57 | 0.474 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 287,046 | 2.870 | 20 | 20 | fits | 139,531 | 95 | 0.610 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 473,567 | 4.736 | 20 | 20 | fits | 78,711 | 37 | 0.514 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,369 | 0.054 | 20 | 20 | fits | 20,431 | 13 (29) | 0.785 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,211 | 0.072 | 20 | 20 | fits | 21,437 | 19 (35) | 0.768 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 19,209 | 0.192 | 20 | 20 | fits | 27,712 | 21 (12) | 0.807 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 12,027 | 0.120 | 20 | 50 | fits | 22,720 | 43 | 0.711 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 17,376 | 0.174 | 20 | 50 | fits | 18,388 | 35 | 0.648 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 11,635 | 0.116 | 20 | 50 | fits | 18,297 | 35 | 0.645 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 12,929 | 0.129 | 20 | 50 | fits | 24,386 | 61 | 0.575 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 15,116 | 0.151 | 20 | 50 | fits | 24,386 | 61 | 0.575 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 10,289 | 0.103 | 20 | 50 | fits | 17,536 | 30 | 0.560 |
| LINK_UP | `adp.link_up.if0` | 2,640 | 0.026 | 20 | 200 | fits | 22,720 | 43 (11) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,005 | 0.180 | 20 | 200 | fits | 19,699 | 23 (39) | 0.713 |
| LINK_DOWN | `adp.link_down.if0` | 2,356 | 0.024 | 20 | 200 | fits | 23,246 | 23 (9) | 0.771 |
| LINK_UP | `adp.link_up.if0` | 2,640 | 0.026 | 20 | 200 | fits | 22,720 | 43 (11) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,005 | 0.180 | 20 | 200 | fits | 19,699 | 23 (39) | 0.713 |
| GM_CHANGE | `adp.gm_change.if0` | 2,330 | 0.023 | 20 | 200 | fits | 11,224 | 17 (11) | 0.620 |
| LINK_UP | `adp.link_up.if0` | 2,640 | 0.026 | 20 | 200 | fits | 22,720 | 43 (11) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,005 | 0.180 | 20 | 200 | fits | 19,699 | 23 (39) | 0.713 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,856 | 0.049 | 20 | 200 | fits | 10,761 | 16 (31) | 0.463 |
| LINK_UP | `adp.link_up.if0` | 2,640 | 0.026 | 20 | 200 | fits | 22,720 | 43 (11) | 0.711 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,005 | 0.180 | 20 | 200 | fits | 19,699 | 23 (39) | 0.713 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,856 | 0.049 | 20 | 200 | fits | 10,761 | 16 (31) | 0.463 |
| set_name | `aecp_fanout.set_name.if0` | 47,596 | 0.476 | 20 | 24 | fits | 55,329 | 88 | 0.526 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 49,262 | 0.493 | 20 | 24 | fits | 50,091 | 77 | 0.552 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 41,248 | 0.412 | 20 | 24 | fits | 45,775 | 78 | 0.498 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 45,814 | 0.458 | 20 | 24 | fits | 45,296 | 77 | 0.494 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 45,743 | 0.457 | 20 | 24 | fits | 51,421 | 66 | 0.573 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 44,901 | 0.449 | 20 | 24 | fits | 50,580 | 65 | 0.572 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 46,459 | 0.465 | 20 | 24 | fits | 48,452 | 66 | 0.556 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 40,729 | 0.407 | 20 | 24 | fits | 45,295 | 77 | 0.489 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 46,845 | 0.468 | 20 | 24 | fits | 45,237 | 78 | 0.487 |
| BIND_RX | `acmp.bind_rx.if0` | 22,840 | 0.228 | 20 | 20 | fits | 40,442 | 26 (77) | 0.775 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,372 | 0.084 | 20 | 20 | fits | 26,250 | 20 (32) | 0.821 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 12,463 | 0.125 | 20 | 20 | fits | 26,744 | 15 (47) | 0.755 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,196 | 0.142 | 20 | 20 | fits | 34,106 | 18 (50) | 0.809 |
| PROBE_TX | `acmp.probe_tx.if0` | 12,715 | 0.127 | 20 | 20 | fits | 24,803 | 18 (48) | 0.723 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 12,496 | 0.125 | 20 | 20 | fits | 24,603 | 16 (48) | 0.725 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 10,661 | 0.107 | 20 | 20 | fits | 23,465 | 16 (48) | 0.694 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 10,874 | 0.109 | 20 | 20 | fits | 23,496 | 16 (48) | 0.696 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 19,264 | 0.193 | 20 | 24 | fits | 22,844 | 20 | 0.762 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 24,279 | 0.243 | 20 | 24 | fits | 26,138 | 20 | 0.672 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 14,087 | 0.141 | 20 | 24 | fits | 21,274 | 20 | 0.685 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 19,449 | 0.194 | 20 | 24 | fits | 21,549 | 20 | 0.693 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 14,268 | 0.143 | 20 | 24 | fits | 21,711 | 20 | 0.676 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 19,602 | 0.196 | 20 | 24 | fits | 22,339 | 20 | 0.697 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 20,029 | 0.200 | 20 | 24 | fits | 21,367 | 20 | 0.691 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 14,082 | 0.141 | 20 | 24 | fits | 21,241 | 20 | 0.697 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 9,711 | 0.097 | 20 | 24 | fits | 21,248 | 20 | 0.711 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 16,088 | 0.161 | 20 | 24 | fits | 23,174 | 21 | 0.588 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 9,007 | 0.090 | 20 | 24 | fits | 20,525 | 20 | 0.729 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 12,814 | 0.128 | 20 | 24 | fits | 20,071 | 20 | 0.709 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 18,519 | 0.185 | 20 | 24 | fits | 21,367 | 20 | 0.700 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 14,320 | 0.143 | 20 | 24 | fits | 21,211 | 20 | 0.678 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 9,997 | 0.100 | 20 | 24 | fits | 21,530 | 20 | 0.713 |
| get_configuration | `aecp.get_configuration.if0` | 17,510 | 0.175 | 20 | 24 | fits | 19,213 | 20 | 0.721 |
| entity_available | `aecp.entity_available.if0` | 11,991 | 0.120 | 20 | 24 | fits | 18,724 | 20 | 0.688 |
| get_name | `aecp.get_name.if0` | 19,518 | 0.195 | 20 | 24 | fits | 22,206 | 20 | 0.741 |
| get_counters | `aecp.get_counters.if0` | 15,241 | 0.152 | 20 | 24 | fits | 23,177 | 27 | 0.693 |
| get_avb_info | `aecp.get_avb_info.if0` | 19,455 | 0.195 | 20 | 24 | fits | 21,621 | 20 | 0.768 |
| unknown_command | `aecp.unknown_command.if0` | 12,217 | 0.122 | 20 | 24 | fits | 19,264 | 20 | 0.723 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 7,943 | 0.079 | 20 | 24 | fits | 19,254 | 20 | 0.713 |
| set_name | `aecp.set_name.if0` | 25,839 | 0.258 | 20 | 24 | fits | 37,087 | 42 | 0.721 |
| lock_entity | `aecp.lock_entity.if0` | 18,357 | 0.184 | 20 | 24 | fits | 29,489 | 32 | 0.745 |
| unlock_entity | `aecp.unlock_entity.if0` | 17,663 | 0.177 | 20 | 24 | fits | 28,798 | 33 | 0.734 |
| LINK_UP | `fixture.link_up.if0` | 2,640 | 0.026 | 20 | 200 | fits | 22,720 | 43 (11) | 0.711 |
| malformed MRPDU discard | `fixture.malformed.if0` | 14,211 | 0.142 | 20 | 20 | fits | 14,276 | 12 | 0.648 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 28,009 | 0.280 | 20 | 24 | fits | 37,324 | 42 | 0.727 |
| LINK_DOWN | `fixture.link_down.if0` | 2,756 | 0.028 | 20 | 200 | fits | 24,816 | 23 (9) | 0.773 |
| BIND_RX | `fixture.bind_rx.if0` | 22,961 | 0.230 | 20 | 20 | fits | 40,773 | 26 (77) | 0.776 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 12,218 | 0.122 | 20 | 20 | fits | 38,895 | 38 (35) | 0.757 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 13,014 | 0.130 | 20 | 20 | fits | 20,863 | 13 (29) | 0.789 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 80,734 | 0.807 | 20 | 200 | fits | 80,837 | 51 | 0.754 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 80,734 | 0.807 | 20 | 200 | fits | 80,837 | 51 | 0.754 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 80,464 | 0.805 | 20 | 20 | fits | 80,837 | 51 | 0.754 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 80,464 | 0.805 | 20 | 20 | fits | 80,837 | 51 | 0.754 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 80,669 | 0.807 | 20 | 24 | fits | 80,837 | 51 | 0.754 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 80,669 | 0.807 | 20 | 24 | fits | 80,837 | 51 | 0.754 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 80,604 | 0.806 | 20 | 50 | fits | 80,837 | 51 | 0.754 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 80,604 | 0.806 | 20 | 50 | fits | 80,837 | 51 | 0.754 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 80,539 | 0.805 | 20 | 20 | fits | 80,837 | 51 | 0.754 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 80,539 | 0.805 | 20 | 20 | fits | 80,837 | 51 | 0.754 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
