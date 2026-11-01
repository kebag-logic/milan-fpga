### 8x8

75 of 129 paths and 117 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 8.133 (23.628) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 16.766 (37.773) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 12.309 (32.710) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 25.819 (76.040) | MISS ceiling | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 27.307 (76.898) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 28.929 (76.898) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 55.098 (83.547) | MISS ceiling | 2 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 56.653 (83.547) | MISS ceiling | 3 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 13.287 (33.047) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 19.151 (39.301) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 15.965 (35.478) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 21.961 (36.142) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 16.639 (35.886) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 29.437 (74.960) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 14.644 (33.623) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 29.261 (89.799) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 33.050 (54.257) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 18.311 (38.997) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 7.609 (34.713) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 6.848 (38.271) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 12.506 (36.687) | MISS T_svc | 3 events | 1 | 1 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 5.904 (38.701) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 18.869 (68.971) | MISS T_svc | 1 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 16.636 (68.971) | MISS T_svc | 3 events | 1 | 1 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 5.321 (33.373) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 18.257 (69.848) | MISS T_svc | 2 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 20.987 (69.311) | MISS ceiling | 2 events | 1 | 1 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 13.267 (59.303) | MISS T_svc | 1 events | 1 | 1 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 8.543 (33.390) | fits | 2 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 9.825 (68.103) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 11.516 (32.472) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 21.990 (54.054) | MISS ceiling | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 7.880 (20.151) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 8.043 (20.150) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 5.523 (19.727) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 5.943 (19.727) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 16.779 (46.065) | MISS T_svc | 0 events | 1 | 1 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 25.620 (46.065) | MISS T_svc | 0 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 27.339 (72.769) | MISS T_svc | 0 events | 5 | 5 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 37.952 (72.769) | MISS T_svc | 0 events | 5 | 5 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 7.472 (19.753) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 6.165 (10.977) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 5.232 (18.751) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 4.022 (20.292) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 9.240 (20.492) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 9.252 (20.500) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 10.208 (20.938) | MISS T_svc | 0 aecp | 1 | 1 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 10.033 (20.846) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 9.528 (20.508) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 9.491 (20.470) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 9.012 (16.374) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 10.515 (21.799) | MISS T_svc | 0 aecp | 1 | 1 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 9.788 (21.217) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 9.624 (21.047) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 14.435 (22.493) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 8.192 (28.084) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 8.225 (19.300) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 8.234 (19.304) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 8.664 (13.550) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 10.023 (21.538) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 8.538 (12.751) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 9.845 (20.957) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 9.836 (20.954) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 9.810 (20.926) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 10.592 (21.717) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 9.695 (20.817) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 9.708 (20.829) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 9.930 (21.048) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 9.934 (21.048) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 9.964 (21.082) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 22.148 (33.358) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 8.799 (12.882) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 13.149 (20.906) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 8.246 (12.856) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 8.555 (12.768) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 10.603 (19.085) | MISS T_svc | 0 aecp | 1 | 1 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 7.867 (17.567) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 10.715 (24.660) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 9.127 (21.913) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 9.120 (20.281) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 9.172 (20.285) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 10.311 (20.650) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 8.089 (14.173) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 12.952 (18.529) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 12.949 (18.378) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 16.800 (34.737) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 15.351 (19.428) | MISS T_svc | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 13.671 (19.222) | MISS T_svc | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 12.796 (18.217) | MISS T_svc | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 20.134 (33.501) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 16.902 (23.140) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 12.230 (17.600) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 20.206 (25.669) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 13.980 (19.408) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 157.142 (170.593) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 92.856 (130.557) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 132.552 (162.464) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 58.664 (99.269) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 216.767 (229.651) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | at least 860.000 | NEVER ANSWERED | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 7.326 (21.130) | fits | 1 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 7.658 (20.491) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 7.650 (19.999) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 8.000 (20.055) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 23.213 (49.335) | MISS T_svc | 0 events | 1 | 1 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 19.623 (47.146) | MISS T_svc | 0 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 7.138 (21.130) | fits | 1 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 7.471 (20.491) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 5.693 (17.856) | fits | 1 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 7.065 (19.542) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 34.817 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 192.148 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 34.859 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 152.192 | MISS T_svc | 6 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 121.690 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 34.852 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp.service.aecp.last.if1` (backlog-adp) | 556.799 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 34.842 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 121.675 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 672.538 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 672.517 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 16.405 (20.213) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 19.308 (28.893) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 14.700 (20.575) | MISS T_svc | 0 srp | 1 | 1 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 14.956 (21.196) | MISS T_svc | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 7.859 (9.565) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 10.163 (18.515) | MISS T_svc | 0 srp | 1 | 1 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 15.791 (22.155) | MISS T_svc | 0 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 17.665 (36.666) | MISS T_svc | 1 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 657.195 | 46 | 2,027,538 (40.551) | yes | - |
| backlog-adp | 592.909 | 17 | 2,497,118 (49.942) | no | {'srp': 32} |
| backlog-adp-refill | 672.554 | 19 | 2,339,853 (46.797) | no | {'srp': 32} |
| backlog-owed | 860.053 | 65 | 1,448,761 (28.975) | yes | - |

Composed maximum over the 4 backlog windows: at least 2,497,118 CPU cycles (49.942 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 2,027,538 (40.551 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 1,049,344 | 20.987 | 10 | 20 | MISS ceiling | 1,697,564 | 132 (14) | 0.011 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 663,367 | 13.267 | 10 | 20 | MISS T_svc | 1,106,881 | 87 (14) | 0.009 |
| LINK_UP | `adp.link_up.if0` | 1,366,963 | 27.339 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,897,583 | 37.952 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 261,609 | 5.232 | 10 | 200 | fits | 525,137 | 53 (39) | 0.028 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,106 | 4.022 | 10 | 200 | fits | 489,475 | 53 (39) | 0.026 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 373,622 | 7.472 | 10 | 200 | fits | 434,538 | 25 (11) | 0.025 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 308,225 | 6.165 | 10 | 200 | fits | 114,294 | 15 (11) | 0.040 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 1,160,633 | 23.213 | 10 | 50 | MISS T_svc | 1,359,000 | 178 | 0.012 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 284,669 | 5.693 | 10 | 50 | fits | 574,875 | 44 | 0.030 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 272,328 | 5.447 | 10 | 50 | fits | 562,765 | 44 | 0.029 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 356,917 | 7.138 | 10 | 50 | fits | 659,683 | 77 | 0.027 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 366,287 | 7.326 | 10 | 50 | fits | 659,683 | 77 | 0.027 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 382,510 | 7.650 | 10 | 50 | fits | 588,558 | 54 | 0.030 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 981,156 | 19.623 | 10 | 50 | MISS T_svc | 1,322,531 | 178 | 0.011 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 264,329 | 5.287 | 10 | 50 | fits | 567,729 | 44 | 0.028 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 353,254 | 7.065 | 10 | 50 | fits | 564,543 | 44 | 0.028 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 373,528 | 7.471 | 10 | 50 | fits | 611,772 | 71 | 0.028 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 382,898 | 7.658 | 10 | 50 | fits | 611,772 | 71 | 0.028 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 399,999 | 8.000 | 10 | 50 | fits | 581,093 | 53 | 0.029 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 943,469 | 18.869 | 10 | 20 | MISS T_svc | 1,445,965 | 141 (35) | 0.011 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 831,801 | 16.636 | 10 | 20 | MISS T_svc | 1,445,965 | 141 (35) | 0.011 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 266,059 | 5.321 | 10 | 20 | fits | 1,668,646 | 109 (14) | 0.011 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 912,850 | 18.257 | 10 | 20 | MISS T_svc | 1,823,745 | 126 (14) | 0.009 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 427,168 | 8.543 | 10 | 20 | fits | 1,669,518 | 110 (14) | 0.011 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 491,244 | 9.825 | 10 | 20 | fits | 1,735,655 | 135 (14) | 0.010 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 380,467 | 7.609 | 10 | 20 | fits | 1,735,655 | 135 (35) | 0.010 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 342,395 | 6.848 | 10 | 20 | fits | 1,913,550 | 149 (35) | 0.009 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 789,549 | 15.791 | 10 | 18 | MISS T_svc | 1,107,762 | 130 | 0.010 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 883,246 | 17.665 | 10 | 18 | MISS T_svc | 1,833,293 | 292 | 0.007 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 735,003 | 14.700 | 10 | 18 | MISS T_svc | 706,227 | 35 | 0.029 |
| malformed MRPDU discard | `srp.malformed.if0` | 392,939 | 7.859 | 10 | 18 | fits | 478,226 | 36 | 0.022 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 820,235 | 16.405 | 210 | 218 | fits | 1,010,660 | 149 | 0.010 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 747,789 | 14.956 | 10 | 18 | MISS T_svc | 616,768 | 36 | 0.023 |
| malformed MRPDU discard | `srp.malformed.if1` | 508,143 | 10.163 | 10 | 18 | MISS T_svc | 485,377 | 36 | 0.021 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 965,386 | 19.308 | 210 | 218 | fits | 1,003,939 | 149 | 0.009 |
| an event behind 15 others | `backlog.event.if0` | 2,933,186 | 58.664 | 10 | 200 | MISS T_svc | 2,027,538 | 377 | 0.015 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 7,857,109 | 157.142 | 10 | 20 | MISS ceiling | 1,063,446 | 225 | 0.015 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,742,957 | 34.859 | 10 | 200 | MISS T_svc | 1,770,164 | 394 | 0.015 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 6,084,477 | 121.690 | 10 | 200 | MISS T_svc | 1,148,520 | 299 | 0.015 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,740,828 | 34.817 | 10 | 20 | MISS ceiling | 1,770,164 | 394 | 0.015 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 8,499,888 | 169.998 | 10 | 20 | MISS ceiling | 1,063,446 | 225 | 0.015 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,742,620 | 34.852 | 10 | 24 | MISS ceiling | 1,770,164 | 394 | 0.015 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 16,734,657 | 334.693 | 10 | 24 | MISS ceiling | 718,471 | 132 | 0.018 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,742,100 | 34.842 | 10 | 50 | MISS T_svc | 1,770,164 | 394 | 0.015 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 6,083,729 | 121.675 | 10 | 50 | MISS ceiling | 1,148,520 | 299 | 0.015 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 7,437,900 | 148.758 | 10 | 18 | MISS ceiling | 1,354,203 | 270 | 0.017 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 22,011,810 | 440.236 | 10 | 18 | MISS ceiling | 532,412 | 54 | 0.021 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 4,642,804 | 92.856 | 10 | 20 | MISS ceiling | 1,613,596 | 363 | 0.013 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 1,484,144 | 29.683 | 10 | 200 | MISS T_svc | 2,236,670 | 428 | 0.013 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 5,775,015 | 115.500 | 10 | 200 | MISS T_svc | 1,613,596 | 363 | 0.013 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 1,484,600 | 29.692 | 10 | 20 | MISS ceiling | 2,236,670 | 428 | 0.013 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 9,539,108 | 190.782 | 10 | 20 | MISS ceiling | 1,978,014 | 299 | 0.012 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 1,486,392 | 29.728 | 10 | 24 | MISS ceiling | 2,236,670 | 428 | 0.013 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 27,839,960 | 556.799 | 10 | 24 | MISS ceiling | 1,750,418 | 212 | 0.013 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 1,485,872 | 29.717 | 10 | 50 | MISS T_svc | 2,236,670 | 428 | 0.013 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 5,776,853 | 115.537 | 10 | 50 | MISS ceiling | 1,613,596 | 363 | 0.013 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 29,644,609 | 592.892 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 29,643,602 | 592.872 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 6,627,612 | 132.552 | 10 | 20 | MISS ceiling | 1,992,406 | 331 | 0.011 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 1,484,144 | 29.683 | 10 | 200 | MISS T_svc | 2,236,670 | 428 | 0.013 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 7,609,594 | 152.192 | 10 | 200 | MISS T_svc | 1,992,406 | 331 | 0.011 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 1,484,600 | 29.692 | 10 | 20 | MISS ceiling | 2,236,670 | 428 | 0.013 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 9,607,400 | 192.148 | 10 | 20 | MISS ceiling | 1,992,406 | 331 | 0.011 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 1,486,392 | 29.728 | 10 | 24 | MISS ceiling | 2,236,670 | 428 | 0.013 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 27,755,903 | 555.118 | 10 | 24 | MISS ceiling | 1,860,834 | 222 | 0.012 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 1,485,872 | 29.717 | 10 | 50 | MISS T_svc | 2,236,670 | 428 | 0.013 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 5,684,248 | 113.685 | 10 | 50 | MISS ceiling | 1,520,991 | 356 | 0.014 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 33,626,875 | 672.538 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 33,625,868 | 672.517 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 10,838,365 | 216.767 | 10 | 20 | MISS ceiling | 912,451 | 160 | 0.018 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 11,797,790 | 235.956 | 10 | 20 | MISS ceiling | 1,447,324 | 376 | 0.008 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 13,251,001 | 265.020 | 10 | 20 | MISS ceiling | 991,313 | 166 | 0.018 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 14,176,341 | 283.527 | 10 | 20 | MISS ceiling | 899,452 | 160 | 0.017 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 42,999,998 | 860.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 1,458,401 | 29.168 | 10 | 200 | MISS T_svc | 1,208,498 | 346 | 0.015 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 5,363,915 | 107.278 | 10 | 200 | MISS T_svc | 1,241,764 | 296 | 0.013 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 1,456,272 | 29.125 | 10 | 20 | MISS ceiling | 1,208,498 | 346 | 0.015 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 7,424,844 | 148.497 | 10 | 20 | MISS ceiling | 1,024,731 | 203 | 0.013 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 1,458,064 | 29.161 | 10 | 24 | MISS ceiling | 1,208,498 | 346 | 0.015 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 17,454,984 | 349.100 | 10 | 24 | MISS ceiling | 927,613 | 177 | 0.015 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 1,457,544 | 29.151 | 10 | 50 | MISS T_svc | 1,208,498 | 346 | 0.015 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 5,363,167 | 107.263 | 10 | 50 | MISS ceiling | 1,241,764 | 296 | 0.013 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 10,405,989 | 208.120 | 10 | 18 | MISS ceiling | 1,234,106 | 180 | 0.022 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 27,185,406 | 543.708 | 10 | 18 | MISS ceiling | 536,230 | 36 | 0.021 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,754,900 | 55.098 | 10 | 20 | MISS ceiling | 1,957,230 | 174 (29) | 0.008 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 2,832,668 | 56.653 | 10 | 20 | MISS ceiling | 1,957,230 | 174 (29) | 0.008 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,365,344 | 27.307 | 10 | 20 | MISS ceiling | 2,023,048 | 185 (35) | 0.009 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,446,461 | 28.929 | 10 | 20 | MISS ceiling | 2,023,048 | 185 (35) | 0.009 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 625,301 | 12.506 | 10 | 20 | MISS T_svc | 1,834,328 | 110 (12) | 0.007 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 295,200 | 5.904 | 10 | 20 | fits | 1,935,063 | 149 (12) | 0.009 |
| LINK_UP | `adp.link_up.if0` | 1,366,963 | 27.339 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,897,583 | 37.952 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 261,609 | 5.232 | 10 | 200 | fits | 525,137 | 53 (39) | 0.028 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,106 | 4.022 | 10 | 200 | fits | 489,475 | 53 (39) | 0.026 |
| LINK_DOWN | `adp.link_down.if0` | 838,956 | 16.779 | 10 | 200 | MISS T_svc | 1,444,084 | 70 (9) | 0.013 |
| LINK_DOWN | `adp.link_down.if1` | 1,281,013 | 25.620 | 10 | 200 | MISS T_svc | 1,444,084 | 70 (9) | 0.013 |
| LINK_UP | `adp.link_up.if0` | 1,366,963 | 27.339 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,897,583 | 37.952 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 261,609 | 5.232 | 10 | 200 | fits | 525,137 | 53 (39) | 0.028 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,106 | 4.022 | 10 | 200 | fits | 489,475 | 53 (39) | 0.026 |
| GM_CHANGE | `adp.gm_change.if0` | 276,161 | 5.523 | 10 | 200 | fits | 444,191 | 34 (11) | 0.025 |
| GM_CHANGE | `adp.gm_change.if1` | 297,158 | 5.943 | 10 | 200 | fits | 444,191 | 34 (11) | 0.025 |
| LINK_UP | `adp.link_up.if0` | 1,366,963 | 27.339 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,897,583 | 37.952 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 261,609 | 5.232 | 10 | 200 | fits | 525,137 | 53 (39) | 0.028 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,106 | 4.022 | 10 | 200 | fits | 489,475 | 53 (39) | 0.026 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 393,984 | 7.880 | 10 | 200 | fits | 465,436 | 73 (31) | 0.025 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 402,158 | 8.043 | 10 | 200 | fits | 465,436 | 73 (31) | 0.025 |
| LINK_UP | `adp.link_up.if0` | 1,366,963 | 27.339 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,897,583 | 37.952 | 10 | 200 | MISS T_svc | 2,091,469 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 261,609 | 5.232 | 10 | 200 | fits | 525,137 | 53 (39) | 0.028 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,106 | 4.022 | 10 | 200 | fits | 489,475 | 53 (39) | 0.026 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 393,984 | 7.880 | 10 | 200 | fits | 457,485 | 45 (31) | 0.026 |
| set_name | `aecp_fanout.set_name.if0` | 1,006,689 | 20.134 | 10 | 24 | MISS T_svc | 1,263,790 | 1178 | 0.009 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 839,990 | 16.800 | 10 | 24 | MISS T_svc | 951,021 | 619 | 0.011 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 683,530 | 13.671 | 10 | 24 | MISS T_svc | 961,103 | 593 | 0.011 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 637,564 | 12.751 | 10 | 24 | MISS T_svc | 958,274 | 593 | 0.011 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 611,505 | 12.230 | 10 | 24 | MISS T_svc | 879,990 | 597 | 0.011 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 647,591 | 12.952 | 10 | 24 | MISS T_svc | 926,430 | 685 | 0.010 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 1,010,313 | 20.206 | 10 | 24 | MISS T_svc | 1,283,432 | 801 | 0.013 |
| set_name | `aecp_fanout.set_name.if1` | 845,096 | 16.902 | 10 | 24 | MISS T_svc | 1,157,010 | 1145 | 0.008 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 767,554 | 15.351 | 10 | 24 | MISS T_svc | 971,404 | 626 | 0.011 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 639,816 | 12.796 | 10 | 24 | MISS T_svc | 910,868 | 587 | 0.010 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 638,701 | 12.774 | 10 | 24 | MISS T_svc | 909,521 | 586 | 0.010 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 647,443 | 12.949 | 10 | 24 | MISS T_svc | 918,919 | 685 | 0.010 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 698,987 | 13.980 | 10 | 24 | MISS T_svc | 970,383 | 692 | 0.010 |
| BIND_RX | `acmp.bind_rx.if0` | 406,643 | 8.133 | 10 | 20 | fits | 768,923 | 83 (77) | 0.026 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 1,652,486 | 33.050 | 10 | 20 | MISS ceiling | 1,996,975 | 144 (32) | 0.012 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 664,357 | 13.287 | 10 | 20 | MISS T_svc | 1,652,326 | 139 (47) | 0.013 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 575,808 | 11.516 | 10 | 20 | MISS T_svc | 1,623,613 | 194 (50) | 0.016 |
| PROBE_TX | `acmp.probe_tx.if0` | 732,214 | 14.644 | 10 | 20 | MISS T_svc | 1,681,158 | 141 (48) | 0.014 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 831,959 | 16.639 | 10 | 20 | MISS T_svc | 1,794,287 | 150 (48) | 0.012 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 615,447 | 12.309 | 10 | 20 | MISS T_svc | 1,635,485 | 140 (48) | 0.013 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 798,253 | 15.965 | 10 | 20 | MISS T_svc | 1,773,908 | 150 (48) | 0.012 |
| BIND_RX | `acmp.bind_rx.if1` | 838,306 | 16.766 | 10 | 20 | MISS T_svc | 1,888,669 | 180 (77) | 0.013 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 915,574 | 18.311 | 10 | 20 | MISS T_svc | 1,949,830 | 153 (32) | 0.009 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 957,555 | 19.151 | 10 | 20 | MISS T_svc | 1,965,060 | 168 (47) | 0.009 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 1,099,490 | 21.990 | 10 | 20 | MISS ceiling | 2,702,695 | 387 (50) | 0.008 |
| PROBE_TX | `acmp.probe_tx.if1` | 1,463,069 | 29.261 | 10 | 20 | MISS ceiling | 1,787,260 | 153 (48) | 0.011 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 1,471,829 | 29.437 | 10 | 20 | MISS ceiling | 1,960,753 | 169 (48) | 0.009 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 1,290,948 | 25.819 | 10 | 20 | MISS ceiling | 1,841,224 | 176 (48) | 0.012 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 1,098,030 | 21.961 | 10 | 20 | MISS ceiling | 1,807,082 | 176 (48) | 0.011 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 530,136 | 10.603 | 10 | 24 | MISS T_svc | 541,812 | 49 | 0.023 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 433,202 | 8.664 | 10 | 24 | fits | 677,507 | 133 | 0.018 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 426,909 | 8.538 | 10 | 24 | fits | 637,571 | 82 | 0.018 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 496,522 | 9.930 | 10 | 24 | fits | 642,170 | 93 | 0.018 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 657,471 | 13.149 | 10 | 24 | MISS T_svc | 557,946 | 85 | 0.017 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 412,293 | 8.246 | 10 | 24 | fits | 642,807 | 91 | 0.018 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 427,729 | 8.555 | 10 | 24 | fits | 638,376 | 81 | 0.018 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 491,806 | 9.836 | 10 | 24 | fits | 637,521 | 77 | 0.018 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 490,509 | 9.810 | 10 | 24 | fits | 636,034 | 74 | 0.018 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 529,581 | 10.592 | 10 | 24 | MISS T_svc | 675,999 | 169 | 0.016 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 484,740 | 9.695 | 10 | 24 | fits | 630,980 | 61 | 0.019 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 485,422 | 9.708 | 10 | 24 | fits | 631,480 | 61 | 0.019 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 498,177 | 9.964 | 10 | 24 | fits | 643,999 | 78 | 0.018 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 1,107,404 | 22.148 | 10 | 24 | MISS T_svc | 714,867 | 89 | 0.018 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 439,959 | 8.799 | 10 | 24 | fits | 644,092 | 79 | 0.018 |
| get_configuration | `aecp.get_configuration.if0` | 476,396 | 9.528 | 10 | 24 | fits | 615,172 | 56 | 0.019 |
| entity_available | `aecp.entity_available.if0` | 461,987 | 9.240 | 10 | 24 | fits | 614,423 | 60 | 0.018 |
| get_name | `aecp.get_name.if0` | 489,386 | 9.788 | 10 | 24 | fits | 650,765 | 72 | 0.019 |
| get_counters | `aecp.get_counters.if0` | 450,587 | 9.012 | 10 | 24 | fits | 818,702 | 122 | 0.022 |
| get_avb_info | `aecp.get_avb_info.if0` | 510,386 | 10.208 | 10 | 24 | MISS T_svc | 636,707 | 56 | 0.018 |
| unknown_command | `aecp.unknown_command.if0` | 456,020 | 9.120 | 10 | 24 | fits | 603,743 | 56 | 0.018 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 411,271 | 8.225 | 10 | 24 | fits | 554,703 | 60 | 0.021 |
| set_name | `aecp.set_name.if0` | 535,737 | 10.715 | 10 | 24 | MISS T_svc | 822,768 | 149 | 0.014 |
| lock_entity | `aecp.lock_entity.if0` | 721,773 | 14.435 | 10 | 24 | MISS T_svc | 710,045 | 96 | 0.019 |
| unlock_entity | `aecp.unlock_entity.if0` | 515,558 | 10.311 | 10 | 24 | MISS T_svc | 703,643 | 96 | 0.018 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 393,349 | 7.867 | 10 | 24 | fits | 551,778 | 54 | 0.020 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 501,173 | 10.023 | 10 | 24 | MISS T_svc | 666,547 | 132 | 0.017 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 492,232 | 9.845 | 10 | 24 | fits | 637,409 | 80 | 0.018 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 496,693 | 9.934 | 10 | 24 | fits | 642,020 | 91 | 0.018 |
| get_configuration | `aecp.get_configuration.if1` | 474,546 | 9.491 | 10 | 24 | fits | 613,106 | 54 | 0.019 |
| entity_available | `aecp.entity_available.if1` | 462,610 | 9.252 | 10 | 24 | fits | 614,566 | 58 | 0.018 |
| get_name | `aecp.get_name.if1` | 481,178 | 9.624 | 10 | 24 | fits | 641,981 | 71 | 0.019 |
| get_counters | `aecp.get_counters.if1` | 525,756 | 10.515 | 10 | 24 | MISS T_svc | 679,463 | 92 | 0.020 |
| get_avb_info | `aecp.get_avb_info.if1` | 501,672 | 10.033 | 10 | 24 | MISS T_svc | 631,771 | 54 | 0.018 |
| unknown_command | `aecp.unknown_command.if1` | 458,588 | 9.172 | 10 | 24 | fits | 603,780 | 54 | 0.018 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 411,689 | 8.234 | 10 | 24 | fits | 554,746 | 58 | 0.021 |
| set_name | `aecp.set_name.if1` | 456,363 | 9.127 | 10 | 24 | fits | 685,231 | 142 | 0.012 |
| lock_entity | `aecp.lock_entity.if1` | 409,590 | 8.192 | 10 | 24 | fits | 617,264 | 109 | 0.016 |
| unlock_entity | `aecp.unlock_entity.if1` | 404,426 | 8.089 | 10 | 24 | fits | 708,636 | 115 | 0.018 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
- `adp-advertise`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `maap`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `srp`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait tx TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-link`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-gm`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `adp-discover`: wait quiet TIMEOUT
- `control`: wait quiet TIMEOUT
- `control`: wait quiet TIMEOUT
- `control`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
