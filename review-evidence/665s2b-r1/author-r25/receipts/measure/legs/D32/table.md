### 32x32

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 129 paths and 10 of 182 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.344 (0.868) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.313 (0.843) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.138 (0.596) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.127 (0.600) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.169 (0.873) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.348 (0.873) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.155 (0.845) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.327 (0.845) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.140 (0.605) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.141 (0.611) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.122 (0.590) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.126 (0.598) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.131 (0.594) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.133 (0.597) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.137 (0.605) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.138 (0.608) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.156 (0.699) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.139 (0.670) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.354 (1.332) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.283 (1.260) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.541 (1.482) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.334 (1.312) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.611 (1.622) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.853 (1.622) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.488 (1.606) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.663 (1.606) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.385 (1.342) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.435 (1.540) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.452 (1.610) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.620 (1.610) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.244 (0.861) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.263 (0.891) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.050 (0.445) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.064 (0.445) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.017 (0.425) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.029 (0.425) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.016 (2.466) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 1.605 (2.466) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.020 (0.832) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.244 (0.832) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.375 (0.805) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.358 (0.805) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.461 (1.275) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.390 (1.275) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.428 (1.255) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.463 (1.294) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.180 (1.087) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 0.212 (1.045) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.176 (0.997) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.208 (1.031) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.209 (1.043) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 0.239 (1.076) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.458 (1.285) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.489 (1.319) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.657 (1.364) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.693 (1.412) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.171 (0.990) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.204 (1.025) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.239 (1.065) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.262 (1.096) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.453 (1.288) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.483 (1.323) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i33.c0.if0` (aecp) | 0.195 (1.020) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.192 (1.021) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.492 (1.316) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i31.c0.if0` (aecp) | 0.455 (1.278) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i31.c0.if0` (aecp) | 0.192 (1.018) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.458 (1.284) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.235 (1.061) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i287.c0.if0` (aecp) | 0.351 (1.189) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.452 (1.288) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (144 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.209 (1.030) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i32.c0.if0` (aecp) | 0.195 (1.023) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i32.c0.if0` (aecp) | 0.200 (1.031) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.445 (1.272) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.156 (0.983) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.192 (1.016) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.417 (1.134) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.451 (1.181) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.430 (1.254) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 0.465 (1.293) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.668 (1.360) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.705 (1.412) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 1.044 (1.815) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 1.048 (1.818) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.934 (1.738) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.942 (1.733) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.918 (1.690) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 1.057 (1.828) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 1.095 (1.884) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.948 (1.755) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 1.066 (1.856) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 1.046 (1.547) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.917 (1.704) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 13.781 (14.652) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 7.634 (9.176) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.254 (1.216) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.943 (4.490) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 65.247 (66.166) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 1261.096 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.246 (1.097) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.443 (1.323) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.194 (0.584) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.194 (0.600) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.225 (0.634) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.213 (0.636) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.227 (1.097) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.424 (1.323) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.552 (1.358) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 0.269 (1.102) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 2.797 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 14.599 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.840 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 9.123 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 12.083 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.833 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.233 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.822 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 10.090 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 10.090 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 25.864 | MISS ceiling | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 10.406 (11.235) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 10.514 (11.316) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 1.335 (1.336) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 1.344 (1.344) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.715 (0.715) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.557 (0.558) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 7.697 (7.801) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 7.754 (7.869) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 25.966 | 20 | 439,913 (4.399) | yes | - |
| backlog-adp | 0 | 27.225 | 21 | 326,341 (3.263) | yes | - |
| backlog-adp-refill | 0 | 42.089 | 27 | 326,341 (3.263) | yes | - |
| backlog-owed | 0 | 1261.147 | 153 | 723,579 (7.236) | yes | - |

Composed maximum over the 4 backlog windows: 723,579 CPU cycles (7.236 ms), backlog-owed.
Over the windows that released their whole load only: 723,579 (7.236 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 5664 | 26 | 735,874 (7.359) | OVER the share |
| adp-advertise | 595 | 16 | 720,691 (7.207) | OVER the share |
| maap | 371 | 10 | 723,591 (7.236) | OVER the share |
| acmp-noresp | 3088 | 18 | 732,621 (7.326) | OVER the share |
| srp | 308 | 12 | 1,023,903 (10.239) | OVER the share |
| backlog | 299 | 12 | 720,691 (7.207) | OVER the share |
| backlog-adp | 326 | 13 | 720,691 (7.207) | OVER the share |
| backlog-adp-refill | 332 | 12 | 720,691 (7.207) | OVER the share |
| backlog-owed | 458 | 16 | 723,579 (7.236) | OVER the share |
| acmp-disc | 1391 | 12 | 735,816 (7.358) | OVER the share |
| adp-link | 89 | 9 | 720,691 (7.207) | OVER the share |
| adp-gm | 86 | 6 | 720,691 (7.207) | OVER the share |
| adp-discover | 86 | 6 | 720,691 (7.207) | OVER the share |
| control | 86 | 6 | 720,691 (7.207) | OVER the share |
| aecp-fanout | 155 | 8 | 720,691 (7.207) | OVER the share |
| acmp-cmd | 113 | 6 | 720,691 (7.207) | OVER the share |
| aecp | 139 | 6 | 720,691 (7.207) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 38,476 | 0.385 | 20 | 20 | fits | 91,030 | 37 (14) | 0.759 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 43,522 | 0.435 | 20 | 20 | fits | 81,252 | 19 (14) | 0.892 |
| LINK_UP | `adp.link_up.if0` | 1,972 | 0.020 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| LINK_UP | `adp.link_up.if1` | 24,370 | 0.244 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 46,117 | 0.461 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 39,024 | 0.390 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 37,495 | 0.375 | 20 | 200 | fits | 3,571 | 19 (11) | 0.406 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 35,809 | 0.358 | 20 | 200 | fits | 3,571 | 19 (11) | 0.406 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 22,467 | 0.225 | 20 | 50 | fits | 63,444 | 44 | 0.688 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 55,243 | 0.552 | 20 | 50 | fits | 59,297 | 36 | 0.654 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 35,097 | 0.351 | 20 | 50 | fits | 74,791 | 42 | 0.609 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 22,740 | 0.227 | 20 | 50 | fits | 67,208 | 62 | 0.526 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 24,579 | 0.246 | 20 | 50 | fits | 67,208 | 62 | 0.526 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 19,437 | 0.194 | 20 | 50 | fits | 58,400 | 31 | 0.544 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 21,258 | 0.213 | 20 | 50 | fits | 63,610 | 44 | 0.646 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 26,918 | 0.269 | 20 | 50 | fits | 60,540 | 37 | 0.627 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 23,863 | 0.239 | 20 | 50 | fits | 59,466 | 36 | 0.565 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 42,391 | 0.424 | 20 | 50 | fits | 69,832 | 62 | 0.568 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 44,265 | 0.443 | 20 | 50 | fits | 69,832 | 62 | 0.568 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 19,381 | 0.194 | 20 | 50 | fits | 60,022 | 31 | 0.518 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 61,098 | 0.611 | 20 | 20 | fits | 114,951 | 47 (35) | 0.725 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 85,317 | 0.853 | 20 | 20 | fits | 114,951 | 47 (35) | 0.725 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 48,818 | 0.488 | 20 | 20 | fits | 98,954 | 33 (14) | 0.790 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 66,284 | 0.663 | 20 | 20 | fits | 98,954 | 33 (14) | 0.790 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 45,180 | 0.452 | 20 | 20 | fits | 99,458 | 34 (14) | 0.782 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 61,982 | 0.620 | 20 | 20 | fits | 99,458 | 34 (14) | 0.782 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 35,358 | 0.354 | 20 | 20 | fits | 75,450 | 22 (35) | 0.814 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 28,326 | 0.283 | 20 | 20 | fits | 74,368 | 22 (35) | 0.796 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 769,720 | 7.697 | 20 | 20 | fits | 716,660 | 6 | 0.641 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 775,366 | 7.754 | 20 | 20 | fits | 723,170 | 7 | 0.616 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 133,515 | 1.335 | 20 | 20 | fits | 133,580 | 13 | 0.902 |
| malformed MRPDU discard | `srp.malformed.if0` | 71,452 | 0.715 | 20 | 20 | fits | 71,517 | 19 | 0.611 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 1,040,597 | 10.406 | 220 | 220 | fits | 1,015,153 | 10 | 0.658 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 134,371 | 1.344 | 20 | 20 | fits | 134,436 | 13 | 0.901 |
| malformed MRPDU discard | `srp.malformed.if1` | 55,732 | 0.557 | 20 | 20 | fits | 55,797 | 13 | 0.627 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 1,051,356 | 10.514 | 220 | 220 | fits | 1,023,903 | 10 | 0.656 |
| an event behind 15 others | `backlog.event.if0` | 294,307 | 2.943 | 20 | 200 | fits | 164,804 | 129 | 0.514 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,378,132 | 13.781 | 20 | 20 | fits | 120,119 | 43 | 0.667 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 283,961 | 2.840 | 20 | 200 | fits | 284,169 | 147 | 0.510 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 1,208,339 | 12.083 | 20 | 200 | fits | 197,824 | 53 | 0.683 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 279,702 | 2.797 | 20 | 20 | fits | 284,169 | 147 | 0.510 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,459,944 | 14.599 | 20 | 20 | fits | 120,119 | 43 | 0.667 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 283,287 | 2.833 | 20 | 24 | fits | 284,169 | 147 | 0.510 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,653,863 | 16.539 | 20 | 24 | fits | 89,633 | 28 | 0.700 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 282,247 | 2.822 | 20 | 50 | fits | 284,169 | 147 | 0.510 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,009,020 | 10.090 | 20 | 50 | fits | 113,583 | 40 | 0.702 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,008,955 | 10.090 | 20 | 20 | fits | 113,583 | 40 | 0.702 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 2,464,792 | 24.648 | 20 | 20 | MISS ceiling | 72,403 | 17 | 0.714 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 763,395 | 7.634 | 20 | 20 | fits | 217,905 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 146,082 | 1.461 | 20 | 200 | fits | 150,764 | 144 | 0.472 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 912,338 | 9.123 | 20 | 200 | fits | 217,905 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 146,994 | 1.470 | 20 | 20 | fits | 150,764 | 144 | 0.472 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 1,366,688 | 13.667 | 20 | 20 | fits | 155,732 | 50 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 150,579 | 1.506 | 20 | 24 | fits | 150,764 | 144 | 0.472 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,633,022 | 16.330 | 20 | 24 | fits | 120,517 | 28 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 149,539 | 1.495 | 20 | 50 | fits | 150,764 | 144 | 0.472 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 916,014 | 9.160 | 20 | 50 | fits | 217,905 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 475,425 | 4.754 | 20 | 20 | fits | 326,341 | 142 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 2,586,362 | 25.864 | 20 | 20 | MISS ceiling | 107,211 | 17 | 0.720 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 25,365 | 0.254 | 20 | 20 | fits | 72,481 | 20 | 0.787 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 146,082 | 1.461 | 20 | 200 | fits | 150,764 | 144 | 0.472 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 77,804 | 0.778 | 20 | 200 | fits | 72,481 | 20 | 0.787 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 146,994 | 1.470 | 20 | 20 | fits | 150,764 | 144 | 0.472 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 1,335,998 | 13.360 | 20 | 20 | fits | 151,540 | 44 | 0.668 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 150,579 | 1.506 | 20 | 24 | fits | 150,764 | 144 | 0.472 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,605,720 | 16.057 | 20 | 24 | fits | 120,504 | 28 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 149,539 | 1.495 | 20 | 50 | fits | 150,764 | 144 | 0.472 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 888,020 | 8.880 | 20 | 50 | fits | 189,911 | 75 | 0.608 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 475,425 | 4.754 | 20 | 20 | fits | 326,341 | 142 | 0.605 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 2,561,560 | 25.616 | 20 | 20 | MISS ceiling | 107,211 | 17 | 0.720 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,524,740 | 65.247 | 20 | 20 | MISS ceiling | 53,456 | 13 | 0.734 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 126,109,597 | 1261.096 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 126,109,522 | 1261.095 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 126,109,447 | 1261.094 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 126,109,372 | 1261.094 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 172,386 | 1.724 | 20 | 200 | fits | 160,584 | 140 | 0.488 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 982,910 | 9.829 | 20 | 200 | fits | 146,537 | 29 | 0.738 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 168,127 | 1.681 | 20 | 20 | fits | 160,584 | 140 | 0.488 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,226,080 | 12.261 | 20 | 20 | fits | 119,401 | 22 | 0.741 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 171,712 | 1.717 | 20 | 24 | fits | 160,584 | 140 | 0.488 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,523,282 | 65.233 | 20 | 24 | MISS ceiling | 66,961 | 23 | 0.658 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 170,672 | 1.707 | 20 | 50 | fits | 160,584 | 140 | 0.488 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 834,878 | 8.349 | 20 | 50 | fits | 206,824 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 627,989 | 6.280 | 20 | 20 | fits | 328,940 | 95 | 0.653 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 2,448,330 | 24.483 | 20 | 20 | MISS ceiling | 107,862 | 18 | 0.719 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 15,529 | 0.155 | 20 | 20 | fits | 84,528 | 18 (29) | 0.696 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 32,689 | 0.327 | 20 | 20 | fits | 84,528 | 18 (29) | 0.696 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 16,917 | 0.169 | 20 | 20 | fits | 87,326 | 29 (35) | 0.690 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 34,836 | 0.348 | 20 | 20 | fits | 87,326 | 29 (35) | 0.690 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 54,146 | 0.541 | 20 | 20 | fits | 73,781 | 22 (12) | 0.817 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 33,414 | 0.334 | 20 | 20 | fits | 84,751 | 25 (12) | 0.826 |
| LINK_UP | `adp.link_up.if0` | 1,972 | 0.020 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| LINK_UP | `adp.link_up.if1` | 24,370 | 0.244 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 46,117 | 0.461 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 39,024 | 0.390 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| LINK_DOWN | `adp.link_down.if0` | 1,556 | 0.016 | 20 | 200 | fits | 246,598 | 39 (9) | 0.680 |
| LINK_DOWN | `adp.link_down.if1` | 160,483 | 1.605 | 20 | 200 | fits | 246,598 | 39 (9) | 0.680 |
| LINK_UP | `adp.link_up.if0` | 1,972 | 0.020 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| LINK_UP | `adp.link_up.if1` | 24,370 | 0.244 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 46,117 | 0.461 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 39,024 | 0.390 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| GM_CHANGE | `adp.gm_change.if0` | 1,702 | 0.017 | 20 | 200 | fits | 42,510 | 27 (11) | 0.518 |
| GM_CHANGE | `adp.gm_change.if1` | 2,945 | 0.029 | 20 | 200 | fits | 42,510 | 27 (11) | 0.518 |
| LINK_UP | `adp.link_up.if0` | 1,972 | 0.020 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| LINK_UP | `adp.link_up.if1` | 24,370 | 0.244 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 46,117 | 0.461 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 39,024 | 0.390 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,988 | 0.050 | 20 | 200 | fits | 44,521 | 24 (31) | 0.477 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 6,421 | 0.064 | 20 | 200 | fits | 44,521 | 24 (31) | 0.477 |
| LINK_UP | `adp.link_up.if0` | 1,972 | 0.020 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| LINK_UP | `adp.link_up.if1` | 24,370 | 0.244 | 20 | 200 | fits | 83,226 | 79 (11) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 46,117 | 0.461 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 39,024 | 0.390 | 20 | 200 | fits | 55,789 | 39 (39) | 0.529 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,988 | 0.050 | 20 | 200 | fits | 42,382 | 17 (31) | 0.591 |
| set_name | `aecp_fanout.set_name.if0` | 109,451 | 1.095 | 20 | 24 | fits | 100,749 | 161 | 0.380 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 93,354 | 0.934 | 20 | 24 | fits | 97,715 | 162 | 0.369 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 91,795 | 0.918 | 20 | 24 | fits | 94,274 | 140 | 0.366 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 91,760 | 0.918 | 20 | 24 | fits | 94,120 | 140 | 0.363 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 106,643 | 1.066 | 20 | 24 | fits | 98,235 | 160 | 0.369 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 104,417 | 1.044 | 20 | 24 | fits | 93,746 | 140 | 0.354 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 104,551 | 1.046 | 20 | 24 | fits | 94,544 | 140 | 0.349 |
| set_name | `aecp_fanout.set_name.if1` | 94,771 | 0.948 | 20 | 24 | fits | 99,278 | 161 | 0.327 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 94,175 | 0.942 | 20 | 24 | fits | 98,900 | 162 | 0.372 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 105,681 | 1.057 | 20 | 24 | fits | 94,923 | 140 | 0.362 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 105,366 | 1.054 | 20 | 24 | fits | 94,984 | 140 | 0.363 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 104,802 | 1.048 | 20 | 24 | fits | 94,492 | 140 | 0.355 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 91,717 | 0.917 | 20 | 24 | fits | 94,034 | 140 | 0.345 |
| BIND_RX | `acmp.bind_rx.if0` | 34,429 | 0.344 | 20 | 20 | fits | 86,849 | 27 (77) | 0.785 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 15,568 | 0.156 | 20 | 20 | fits | 69,928 | 21 (32) | 0.817 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 13,973 | 0.140 | 20 | 20 | fits | 60,508 | 16 (47) | 0.734 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 24,384 | 0.244 | 20 | 20 | fits | 86,131 | 19 (50) | 0.824 |
| PROBE_TX | `acmp.probe_tx.if0` | 13,707 | 0.137 | 20 | 20 | fits | 60,522 | 18 (48) | 0.715 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 13,062 | 0.131 | 20 | 20 | fits | 59,395 | 17 (48) | 0.691 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 13,820 | 0.138 | 20 | 20 | fits | 59,554 | 17 (48) | 0.709 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 12,197 | 0.122 | 20 | 20 | fits | 58,976 | 17 (48) | 0.682 |
| BIND_RX | `acmp.bind_rx.if1` | 31,348 | 0.313 | 20 | 20 | fits | 84,348 | 28 (77) | 0.742 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 13,871 | 0.139 | 20 | 20 | fits | 67,026 | 23 (32) | 0.776 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 14,054 | 0.141 | 20 | 20 | fits | 61,053 | 17 (47) | 0.739 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 26,287 | 0.263 | 20 | 20 | fits | 89,106 | 29 (50) | 0.799 |
| PROBE_TX | `acmp.probe_tx.if1` | 13,840 | 0.138 | 20 | 20 | fits | 60,828 | 20 (48) | 0.706 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 13,291 | 0.133 | 20 | 20 | fits | 59,694 | 18 (48) | 0.688 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 12,677 | 0.127 | 20 | 20 | fits | 59,953 | 20 (48) | 0.692 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 12,603 | 0.126 | 20 | 20 | fits | 59,829 | 18 (48) | 0.706 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 15,581 | 0.156 | 20 | 24 | fits | 53,981 | 22 | 0.783 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 23,879 | 0.239 | 20 | 24 | fits | 58,133 | 22 | 0.705 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 45,323 | 0.453 | 20 | 24 | fits | 54,138 | 22 | 0.723 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 45,751 | 0.458 | 20 | 24 | fits | 54,260 | 22 | 0.732 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i32.c0.if0` | 19,456 | 0.195 | 20 | 24 | fits | 53,945 | 22 | 0.729 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i32.c0.if0` | 20,009 | 0.200 | 20 | 24 | fits | 54,656 | 22 | 0.729 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 44,532 | 0.445 | 20 | 24 | fits | 52,886 | 22 | 0.718 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i33.c0.if0` | 19,471 | 0.195 | 20 | 24 | fits | 53,648 | 22 | 0.749 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 19,224 | 0.192 | 20 | 24 | fits | 53,713 | 22 | 0.747 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 49,203 | 0.492 | 20 | 24 | fits | 57,250 | 23 | 0.629 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i31.c0.if0` | 45,469 | 0.455 | 20 | 24 | fits | 53,619 | 22 | 0.767 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i31.c0.if0` | 19,169 | 0.192 | 20 | 24 | fits | 53,371 | 22 | 0.767 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i287.c0.if0` | 35,093 | 0.351 | 20 | 24 | fits | 70,509 | 52 | 0.655 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 45,196 | 0.452 | 20 | 24 | fits | 54,265 | 22 | 0.730 |
| READ_DESCRIPTOR (144 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 20,860 | 0.209 | 20 | 24 | fits | 54,500 | 22 | 0.729 |
| get_configuration | `aecp.get_configuration.if0` | 17,577 | 0.176 | 20 | 24 | fits | 51,272 | 22 | 0.757 |
| entity_available | `aecp.entity_available.if0` | 42,778 | 0.428 | 20 | 24 | fits | 51,097 | 22 | 0.736 |
| get_name | `aecp.get_name.if0` | 45,766 | 0.458 | 20 | 24 | fits | 54,348 | 22 | 0.750 |
| get_counters | `aecp.get_counters.if0` | 20,950 | 0.209 | 20 | 24 | fits | 55,927 | 29 | 0.729 |
| get_avb_info | `aecp.get_avb_info.if0` | 17,962 | 0.180 | 20 | 24 | fits | 52,636 | 22 | 0.763 |
| unknown_command | `aecp.unknown_command.if0` | 42,955 | 0.430 | 20 | 24 | fits | 50,824 | 22 | 0.741 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 17,114 | 0.171 | 20 | 24 | fits | 50,591 | 22 | 0.728 |
| set_name | `aecp.set_name.if0` | 41,660 | 0.417 | 20 | 24 | fits | 65,100 | 66 | 0.642 |
| lock_entity | `aecp.lock_entity.if0` | 65,714 | 0.657 | 20 | 24 | fits | 61,024 | 47 | 0.690 |
| unlock_entity | `aecp.unlock_entity.if0` | 66,764 | 0.668 | 20 | 24 | fits | 61,541 | 46 | 0.701 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 19,168 | 0.192 | 20 | 24 | fits | 53,296 | 20 | 0.772 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 26,246 | 0.262 | 20 | 24 | fits | 57,822 | 20 | 0.703 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 48,339 | 0.483 | 20 | 24 | fits | 54,190 | 20 | 0.729 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 23,529 | 0.235 | 20 | 24 | fits | 54,314 | 20 | 0.738 |
| get_configuration | `aecp.get_configuration.if1` | 20,762 | 0.208 | 20 | 24 | fits | 51,289 | 20 | 0.764 |
| entity_available | `aecp.entity_available.if1` | 46,339 | 0.463 | 20 | 24 | fits | 51,367 | 20 | 0.746 |
| get_name | `aecp.get_name.if1` | 48,927 | 0.489 | 20 | 24 | fits | 54,009 | 20 | 0.745 |
| get_counters | `aecp.get_counters.if1` | 23,936 | 0.239 | 20 | 24 | fits | 55,804 | 27 | 0.730 |
| get_avb_info | `aecp.get_avb_info.if1` | 21,249 | 0.212 | 20 | 24 | fits | 52,739 | 20 | 0.776 |
| unknown_command | `aecp.unknown_command.if1` | 46,537 | 0.465 | 20 | 24 | fits | 51,052 | 20 | 0.748 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 20,383 | 0.204 | 20 | 24 | fits | 50,667 | 20 | 0.735 |
| set_name | `aecp.set_name.if1` | 45,055 | 0.451 | 20 | 24 | fits | 66,356 | 69 | 0.620 |
| lock_entity | `aecp.lock_entity.if1` | 69,272 | 0.693 | 20 | 24 | fits | 62,089 | 50 | 0.667 |
| unlock_entity | `aecp.unlock_entity.if1` | 70,513 | 0.705 | 20 | 24 | fits | 62,991 | 49 | 0.681 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
