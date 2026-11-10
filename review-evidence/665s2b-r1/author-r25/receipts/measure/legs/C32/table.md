### 32x32

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

5 of 129 paths and 16 of 182 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.402 (1.411) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.369 (1.328) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.197 (1.179) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.200 (1.193) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.196 (1.759) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.832 (1.759) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.186 (1.737) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.813 (1.737) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.373 (1.396) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.207 (1.229) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.183 (1.173) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.181 (1.178) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.185 (1.180) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.186 (1.183) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.201 (1.211) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.212 (1.223) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.175 (1.182) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.188 (1.172) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.385 (1.824) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.464 (1.902) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.302 (1.748) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.458 (1.839) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.596 (2.690) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 1.319 (2.690) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.444 (1.861) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.584 (2.415) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.472 (1.869) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.386 (1.954) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.368 (1.809) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.513 (2.429) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.267 (1.334) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.295 (1.361) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.052 (0.451) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.066 (0.451) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.023 (0.435) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.038 (0.435) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.022 (2.392) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 1.533 (2.392) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.025 (0.837) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.254 (0.837) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.095 (0.949) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.401 (0.833) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.137 (0.954) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.442 (1.258) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.188 (1.002) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.221 (1.040) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.199 (1.016) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 0.229 (1.049) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.189 (0.999) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.220 (1.036) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.215 (1.048) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 0.246 (1.082) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.453 (1.275) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.487 (1.311) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.418 (1.114) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.449 (1.157) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.435 (1.247) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.470 (1.286) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.241 (1.068) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.266 (1.095) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.454 (1.273) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.492 (1.311) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i33.c0.if0` (aecp) | 0.203 (1.019) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.203 (1.020) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.485 (1.307) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i31.c0.if0` (aecp) | 0.450 (1.272) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i31.c0.if0` (aecp) | 0.201 (1.015) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.460 (1.278) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.490 (1.317) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i287.c0.if0` (aecp) | 0.298 (1.126) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.467 (1.289) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (144 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.461 (1.286) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i32.c0.if0` (aecp) | 0.206 (1.023) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i32.c0.if0` (aecp) | 0.210 (1.030) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.448 (1.262) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.192 (1.019) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.208 (1.026) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.428 (1.143) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.465 (1.191) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.432 (1.250) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 0.467 (1.287) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.668 (1.367) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.703 (1.418) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.899 (1.666) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 1.044 (1.811) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 1.072 (1.853) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 1.081 (1.602) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 1.054 (1.820) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 0.920 (1.687) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.948 (1.730) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 1.083 (1.867) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.922 (1.710) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 1.041 (1.808) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 1.047 (1.814) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 19.996 (21.311) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 13.363 (15.907) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.446 (1.850) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 4.046 (6.685) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 69.219 (70.691) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 1260.951 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.495 (1.343) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.419 (1.295) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.208 (0.592) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.195 (0.604) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.233 (0.638) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.222 (0.639) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.477 (1.343) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.402 (1.295) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.555 (1.362) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 0.576 (1.411) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 3.899 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 21.258 | MISS ceiling | 11 acmp | 4 | 3 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 3.942 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 15.854 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 16.981 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 3.935 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 69.200 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 3.924 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 13.887 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 13.887 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 34.027 | MISS ceiling | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 10.367 (11.196) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 10.480 (11.284) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.356 (1.357) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 1.352 (1.353) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.573 (0.573) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.564 (0.564) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 7.725 (7.830) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 7.764 (7.880) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 33.371 | 21 | 540,030 (5.400) | yes | - |
| backlog-adp | 0 | 35.386 | 23 | 439,532 (4.395) | yes | - |
| backlog-adp-refill | 0 | 43.276 | 27 | 439,532 (4.395) | yes | - |
| backlog-owed | 0 | 1261.002 | 153 | 725,238 (7.252) | yes | - |

Composed maximum over the 4 backlog windows: 725,238 CPU cycles (7.252 ms), backlog-owed.
Over the windows that released their whole load only: 725,238 (7.252 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 5514 | 27 | 735,619 (7.356) | OVER the share |
| adp-advertise | 598 | 16 | 722,215 (7.222) | OVER the share |
| maap | 372 | 10 | 724,888 (7.249) | OVER the share |
| acmp-noresp | 3104 | 20 | 732,454 (7.325) | OVER the share |
| srp | 309 | 12 | 1,019,174 (10.192) | OVER the share |
| backlog | 302 | 15 | 722,215 (7.222) | OVER the share |
| backlog-adp | 330 | 16 | 722,215 (7.222) | OVER the share |
| backlog-adp-refill | 334 | 16 | 722,215 (7.222) | OVER the share |
| backlog-owed | 461 | 20 | 725,238 (7.252) | OVER the share |
| acmp-disc | 1457 | 14 | 733,945 (7.339) | OVER the share |
| adp-link | 90 | 9 | 722,215 (7.222) | OVER the share |
| adp-gm | 87 | 6 | 722,215 (7.222) | OVER the share |
| adp-discover | 87 | 6 | 722,215 (7.222) | OVER the share |
| control | 87 | 6 | 722,215 (7.222) | OVER the share |
| aecp-fanout | 151 | 6 | 722,215 (7.222) | OVER the share |
| acmp-cmd | 122 | 6 | 722,215 (7.222) | OVER the share |
| aecp | 140 | 6 | 722,215 (7.222) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 47,228 | 0.472 | 20 | 20 | fits | 138,915 | 28 (14) | 0.808 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 38,556 | 0.386 | 20 | 20 | fits | 131,111 | 19 (14) | 0.895 |
| LINK_UP | `adp.link_up.if0` | 2,507 | 0.025 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| LINK_UP | `adp.link_up.if1` | 25,363 | 0.254 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,740 | 0.137 | 20 | 200 | fits | 49,659 | 24 (39) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 44,221 | 0.442 | 20 | 200 | fits | 48,172 | 24 (39) | 0.615 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 9,519 | 0.095 | 20 | 200 | fits | 44,793 | 18 (11) | 0.719 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 40,059 | 0.401 | 20 | 200 | fits | 2,009 | 10 (11) | 0.524 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 23,347 | 0.233 | 20 | 50 | fits | 63,834 | 44 | 0.710 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 55,535 | 0.555 | 20 | 50 | fits | 59,719 | 36 | 0.678 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 45,075 | 0.451 | 20 | 50 | fits | 59,709 | 36 | 0.675 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 47,740 | 0.477 | 20 | 50 | fits | 67,905 | 62 | 0.573 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 49,456 | 0.495 | 20 | 50 | fits | 67,905 | 62 | 0.573 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 20,777 | 0.208 | 20 | 50 | fits | 59,188 | 31 | 0.577 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 22,180 | 0.222 | 20 | 50 | fits | 63,932 | 44 | 0.671 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 57,573 | 0.576 | 20 | 50 | fits | 61,367 | 37 | 0.667 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 37,061 | 0.371 | 20 | 50 | fits | 60,595 | 36 | 0.644 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 40,163 | 0.402 | 20 | 50 | fits | 69,905 | 62 | 0.584 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 41,879 | 0.419 | 20 | 50 | fits | 69,905 | 62 | 0.584 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 19,540 | 0.195 | 20 | 50 | fits | 60,353 | 31 | 0.544 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 59,569 | 0.596 | 20 | 20 | fits | 208,592 | 50 (35) | 0.719 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 131,909 | 1.319 | 20 | 20 | fits | 208,592 | 50 (35) | 0.719 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 44,373 | 0.444 | 20 | 20 | fits | 131,245 | 24 (14) | 0.833 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 58,448 | 0.584 | 20 | 20 | fits | 110,295 | 18 (14) | 0.812 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 36,752 | 0.368 | 20 | 20 | fits | 131,965 | 25 (14) | 0.823 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 51,264 | 0.513 | 20 | 20 | fits | 110,974 | 18 (14) | 0.816 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 38,495 | 0.385 | 20 | 20 | fits | 125,512 | 24 (35) | 0.817 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 46,390 | 0.464 | 20 | 20 | fits | 124,607 | 22 (35) | 0.817 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 772,512 | 7.725 | 20 | 20 | fits | 719,173 | 6 | 0.659 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 776,434 | 7.764 | 20 | 20 | fits | 724,583 | 7 | 0.613 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 135,630 | 1.356 | 20 | 20 | fits | 135,695 | 13 | 0.909 |
| malformed MRPDU discard | `srp.malformed.if0` | 57,263 | 0.573 | 20 | 20 | fits | 57,328 | 13 | 0.667 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 1,036,708 | 10.367 | 220 | 220 | fits | 1,009,732 | 10 | 0.684 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 135,185 | 1.352 | 20 | 20 | fits | 135,250 | 13 | 0.902 |
| malformed MRPDU discard | `srp.malformed.if1` | 56,354 | 0.564 | 20 | 20 | fits | 56,419 | 13 | 0.667 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 1,048,015 | 10.480 | 220 | 220 | fits | 1,019,174 | 10 | 0.680 |
| an event behind 15 others | `backlog.event.if0` | 404,597 | 4.046 | 20 | 200 | fits | 274,107 | 129 | 0.538 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,999,562 | 19.996 | 20 | 20 | fits | 187,025 | 34 | 0.782 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 394,153 | 3.942 | 20 | 200 | fits | 394,361 | 147 | 0.537 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 1,698,097 | 16.981 | 20 | 200 | fits | 307,855 | 53 | 0.702 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 389,894 | 3.899 | 20 | 20 | fits | 394,361 | 147 | 0.537 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,125,825 | 21.258 | 20 | 20 | MISS ceiling | 187,025 | 34 | 0.782 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 393,479 | 3.935 | 20 | 24 | fits | 394,361 | 147 | 0.537 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 2,331,648 | 23.316 | 20 | 24 | MISS T_svc | 100,712 | 37 | 0.643 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 392,439 | 3.924 | 20 | 50 | fits | 394,361 | 147 | 0.537 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,388,747 | 13.887 | 20 | 50 | fits | 173,976 | 40 | 0.708 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,388,682 | 13.887 | 20 | 20 | fits | 173,976 | 40 | 0.708 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 3,204,737 | 32.047 | 20 | 20 | MISS ceiling | 72,986 | 13 | 0.827 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,336,303 | 13.363 | 20 | 20 | fits | 345,538 | 61 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 256,684 | 2.567 | 20 | 200 | fits | 261,366 | 144 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 1,585,432 | 15.854 | 20 | 200 | fits | 345,538 | 61 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 257,596 | 2.576 | 20 | 20 | fits | 261,366 | 144 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 2,069,332 | 20.693 | 20 | 20 | MISS ceiling | 189,372 | 34 | 0.784 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 261,181 | 2.612 | 20 | 24 | fits | 261,366 | 144 | 0.496 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 2,346,259 | 23.463 | 20 | 24 | MISS T_svc | 136,159 | 37 | 0.652 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 260,141 | 2.601 | 20 | 50 | fits | 261,366 | 144 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 1,243,570 | 12.436 | 20 | 50 | fits | 210,019 | 58 | 0.736 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 699,218 | 6.992 | 20 | 20 | fits | 439,532 | 142 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 3,402,685 | 34.027 | 20 | 20 | MISS ceiling | 74,865 | 13 | 0.833 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 44,638 | 0.446 | 20 | 20 | fits | 118,479 | 21 | 0.780 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 256,684 | 2.567 | 20 | 200 | fits | 261,366 | 144 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 141,513 | 1.415 | 20 | 200 | fits | 118,479 | 21 | 0.780 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 257,596 | 2.576 | 20 | 20 | fits | 261,366 | 144 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 2,008,451 | 20.085 | 20 | 20 | MISS ceiling | 189,365 | 34 | 0.784 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 261,181 | 2.612 | 20 | 24 | fits | 261,366 | 144 | 0.496 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 2,287,637 | 22.876 | 20 | 24 | MISS T_svc | 136,078 | 37 | 0.652 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 260,141 | 2.601 | 20 | 50 | fits | 261,366 | 144 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 1,243,570 | 12.436 | 20 | 50 | fits | 210,019 | 58 | 0.736 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 699,218 | 6.992 | 20 | 20 | fits | 439,532 | 142 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 3,352,181 | 33.522 | 20 | 20 | MISS ceiling | 79,119 | 19 | 0.848 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,921,936 | 69.219 | 20 | 20 | MISS ceiling | 109,041 | 13 | 0.780 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 126,095,098 | 1260.951 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 126,095,023 | 1260.950 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 126,094,948 | 1260.949 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 126,094,873 | 1260.949 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 275,819 | 2.758 | 20 | 200 | fits | 262,423 | 140 | 0.501 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 1,488,494 | 14.885 | 20 | 200 | fits | 247,150 | 29 | 0.760 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 271,560 | 2.716 | 20 | 20 | fits | 262,423 | 140 | 0.501 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,874,531 | 18.745 | 20 | 20 | fits | 161,140 | 23 | 0.834 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 275,145 | 2.751 | 20 | 24 | fits | 262,423 | 140 | 0.501 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,919,974 | 69.200 | 20 | 24 | MISS ceiling | 121,726 | 23 | 0.658 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 274,105 | 2.741 | 20 | 50 | fits | 262,423 | 140 | 0.501 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,239,849 | 12.398 | 20 | 50 | fits | 309,186 | 83 | 0.659 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 717,614 | 7.176 | 20 | 20 | fits | 443,964 | 136 | 0.646 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 3,129,673 | 31.297 | 20 | 20 | MISS ceiling | 75,481 | 14 | 0.823 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 18,552 | 0.186 | 20 | 20 | fits | 173,664 | 18 (29) | 0.698 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 81,316 | 0.813 | 20 | 20 | fits | 173,664 | 18 (29) | 0.698 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 19,614 | 0.196 | 20 | 20 | fits | 175,908 | 29 (35) | 0.675 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 83,183 | 0.832 | 20 | 20 | fits | 175,908 | 29 (35) | 0.675 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 30,185 | 0.302 | 20 | 20 | fits | 116,287 | 18 (12) | 0.851 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 45,795 | 0.458 | 20 | 20 | fits | 123,272 | 22 (12) | 0.824 |
| LINK_UP | `adp.link_up.if0` | 2,507 | 0.025 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| LINK_UP | `adp.link_up.if1` | 25,363 | 0.254 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,740 | 0.137 | 20 | 200 | fits | 49,659 | 24 (39) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 44,221 | 0.442 | 20 | 200 | fits | 48,172 | 24 (39) | 0.615 |
| LINK_DOWN | `adp.link_down.if0` | 2,161 | 0.022 | 20 | 200 | fits | 239,205 | 39 (9) | 0.695 |
| LINK_DOWN | `adp.link_down.if1` | 153,277 | 1.533 | 20 | 200 | fits | 239,205 | 39 (9) | 0.695 |
| LINK_UP | `adp.link_up.if0` | 2,507 | 0.025 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| LINK_UP | `adp.link_up.if1` | 25,363 | 0.254 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,740 | 0.137 | 20 | 200 | fits | 49,659 | 24 (39) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 44,221 | 0.442 | 20 | 200 | fits | 48,172 | 24 (39) | 0.615 |
| GM_CHANGE | `adp.gm_change.if0` | 2,326 | 0.023 | 20 | 200 | fits | 43,523 | 27 (11) | 0.603 |
| GM_CHANGE | `adp.gm_change.if1` | 3,826 | 0.038 | 20 | 200 | fits | 43,523 | 27 (11) | 0.603 |
| LINK_UP | `adp.link_up.if0` | 2,507 | 0.025 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| LINK_UP | `adp.link_up.if1` | 25,363 | 0.254 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,740 | 0.137 | 20 | 200 | fits | 49,659 | 24 (39) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 44,221 | 0.442 | 20 | 200 | fits | 48,172 | 24 (39) | 0.615 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,175 | 0.052 | 20 | 200 | fits | 45,117 | 24 (31) | 0.511 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 6,578 | 0.066 | 20 | 200 | fits | 45,117 | 24 (31) | 0.511 |
| LINK_UP | `adp.link_up.if0` | 2,507 | 0.025 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| LINK_UP | `adp.link_up.if1` | 25,363 | 0.254 | 20 | 200 | fits | 83,683 | 79 (11) | 0.599 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,740 | 0.137 | 20 | 200 | fits | 49,659 | 24 (39) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 44,221 | 0.442 | 20 | 200 | fits | 48,172 | 24 (39) | 0.615 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,175 | 0.052 | 20 | 200 | fits | 43,041 | 17 (31) | 0.635 |
| set_name | `aecp_fanout.set_name.if0` | 94,813 | 0.948 | 20 | 24 | fits | 99,214 | 161 | 0.357 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 107,155 | 1.072 | 20 | 24 | fits | 97,572 | 162 | 0.363 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 105,443 | 1.054 | 20 | 24 | fits | 94,004 | 140 | 0.358 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 105,218 | 1.052 | 20 | 24 | fits | 94,066 | 140 | 0.358 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 92,224 | 0.922 | 20 | 24 | fits | 96,484 | 160 | 0.341 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 89,883 | 0.899 | 20 | 24 | fits | 92,801 | 140 | 0.339 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 104,140 | 1.041 | 20 | 24 | fits | 92,857 | 140 | 0.339 |
| set_name | `aecp_fanout.set_name.if1` | 108,259 | 1.083 | 20 | 24 | fits | 99,144 | 161 | 0.333 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 108,069 | 1.081 | 20 | 24 | fits | 99,302 | 162 | 0.358 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 91,419 | 0.914 | 20 | 24 | fits | 94,365 | 140 | 0.344 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 91,999 | 0.920 | 20 | 24 | fits | 94,948 | 140 | 0.358 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 104,432 | 1.044 | 20 | 24 | fits | 93,518 | 140 | 0.339 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 104,748 | 1.047 | 20 | 24 | fits | 93,508 | 140 | 0.337 |
| BIND_RX | `acmp.bind_rx.if0` | 40,235 | 0.402 | 20 | 20 | fits | 141,121 | 27 (77) | 0.784 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 17,504 | 0.175 | 20 | 20 | fits | 118,165 | 20 (32) | 0.822 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 37,315 | 0.373 | 20 | 20 | fits | 139,563 | 21 (47) | 0.796 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 26,735 | 0.267 | 20 | 20 | fits | 133,434 | 19 (50) | 0.803 |
| PROBE_TX | `acmp.probe_tx.if0` | 20,109 | 0.201 | 20 | 20 | fits | 121,108 | 19 (48) | 0.750 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 18,495 | 0.185 | 20 | 20 | fits | 118,012 | 17 (48) | 0.768 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 19,654 | 0.197 | 20 | 20 | fits | 117,860 | 17 (48) | 0.727 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 18,272 | 0.183 | 20 | 20 | fits | 117,308 | 17 (48) | 0.757 |
| BIND_RX | `acmp.bind_rx.if1` | 36,885 | 0.369 | 20 | 20 | fits | 132,790 | 28 (77) | 0.710 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 18,791 | 0.188 | 20 | 20 | fits | 117,170 | 21 (32) | 0.806 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 20,701 | 0.207 | 20 | 20 | fits | 122,864 | 17 (47) | 0.774 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 29,512 | 0.295 | 20 | 20 | fits | 136,150 | 20 (50) | 0.824 |
| PROBE_TX | `acmp.probe_tx.if1` | 21,218 | 0.212 | 20 | 20 | fits | 122,282 | 20 (48) | 0.763 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 18,568 | 0.186 | 20 | 20 | fits | 118,329 | 18 (48) | 0.761 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 20,032 | 0.200 | 20 | 20 | fits | 119,327 | 18 (48) | 0.759 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 18,076 | 0.181 | 20 | 20 | fits | 117,801 | 18 (48) | 0.754 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 19,231 | 0.192 | 20 | 24 | fits | 53,944 | 22 | 0.782 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 24,085 | 0.241 | 20 | 24 | fits | 56,805 | 22 | 0.674 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 45,367 | 0.454 | 20 | 24 | fits | 52,026 | 22 | 0.667 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 46,026 | 0.460 | 20 | 24 | fits | 52,506 | 22 | 0.692 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i32.c0.if0` | 20,586 | 0.206 | 20 | 24 | fits | 52,294 | 22 | 0.692 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i32.c0.if0` | 21,039 | 0.210 | 20 | 24 | fits | 52,854 | 22 | 0.685 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 44,802 | 0.448 | 20 | 24 | fits | 50,865 | 22 | 0.664 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i33.c0.if0` | 20,267 | 0.203 | 20 | 24 | fits | 51,767 | 22 | 0.707 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 20,299 | 0.203 | 20 | 24 | fits | 52,007 | 22 | 0.709 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 48,467 | 0.485 | 20 | 24 | fits | 55,344 | 23 | 0.571 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i31.c0.if0` | 44,966 | 0.450 | 20 | 24 | fits | 51,922 | 22 | 0.732 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i31.c0.if0` | 20,116 | 0.201 | 20 | 24 | fits | 51,428 | 22 | 0.724 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i287.c0.if0` | 29,849 | 0.298 | 20 | 24 | fits | 62,570 | 37 | 0.709 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 46,742 | 0.467 | 20 | 24 | fits | 53,625 | 22 | 0.718 |
| READ_DESCRIPTOR (144 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 46,080 | 0.461 | 20 | 24 | fits | 53,247 | 22 | 0.698 |
| get_configuration | `aecp.get_configuration.if0` | 18,873 | 0.189 | 20 | 24 | fits | 49,881 | 22 | 0.725 |
| entity_available | `aecp.entity_available.if0` | 18,797 | 0.188 | 20 | 24 | fits | 50,143 | 22 | 0.715 |
| get_name | `aecp.get_name.if0` | 45,273 | 0.453 | 20 | 24 | fits | 52,085 | 22 | 0.699 |
| get_counters | `aecp.get_counters.if0` | 21,507 | 0.215 | 20 | 24 | fits | 54,722 | 28 | 0.712 |
| get_avb_info | `aecp.get_avb_info.if0` | 19,881 | 0.199 | 20 | 24 | fits | 51,539 | 22 | 0.748 |
| unknown_command | `aecp.unknown_command.if0` | 43,183 | 0.432 | 20 | 24 | fits | 49,574 | 22 | 0.707 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 43,541 | 0.435 | 20 | 24 | fits | 49,361 | 22 | 0.697 |
| set_name | `aecp.set_name.if0` | 42,828 | 0.428 | 20 | 24 | fits | 64,370 | 66 | 0.640 |
| lock_entity | `aecp.lock_entity.if0` | 41,839 | 0.418 | 20 | 24 | fits | 61,212 | 47 | 0.700 |
| unlock_entity | `aecp.unlock_entity.if0` | 66,797 | 0.668 | 20 | 24 | fits | 60,290 | 46 | 0.685 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 20,830 | 0.208 | 20 | 24 | fits | 52,536 | 20 | 0.763 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 26,649 | 0.266 | 20 | 24 | fits | 56,180 | 20 | 0.662 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 49,188 | 0.492 | 20 | 24 | fits | 52,068 | 20 | 0.672 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 49,045 | 0.490 | 20 | 24 | fits | 52,664 | 20 | 0.701 |
| get_configuration | `aecp.get_configuration.if1` | 22,040 | 0.220 | 20 | 24 | fits | 50,116 | 20 | 0.739 |
| entity_available | `aecp.entity_available.if1` | 22,116 | 0.221 | 20 | 24 | fits | 50,506 | 20 | 0.731 |
| get_name | `aecp.get_name.if1` | 48,739 | 0.487 | 20 | 24 | fits | 51,975 | 20 | 0.698 |
| get_counters | `aecp.get_counters.if1` | 24,596 | 0.246 | 20 | 24 | fits | 54,685 | 26 | 0.717 |
| get_avb_info | `aecp.get_avb_info.if1` | 22,881 | 0.229 | 20 | 24 | fits | 51,458 | 20 | 0.754 |
| unknown_command | `aecp.unknown_command.if1` | 46,700 | 0.467 | 20 | 24 | fits | 49,535 | 20 | 0.712 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 47,027 | 0.470 | 20 | 24 | fits | 49,531 | 20 | 0.708 |
| set_name | `aecp.set_name.if1` | 46,516 | 0.465 | 20 | 24 | fits | 65,696 | 69 | 0.619 |
| lock_entity | `aecp.lock_entity.if1` | 44,935 | 0.449 | 20 | 24 | fits | 62,241 | 50 | 0.676 |
| unlock_entity | `aecp.unlock_entity.if1` | 70,347 | 0.703 | 20 | 24 | fits | 61,640 | 49 | 0.662 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
