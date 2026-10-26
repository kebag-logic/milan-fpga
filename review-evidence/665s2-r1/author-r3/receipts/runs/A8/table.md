### 8x8

60 of 129 paths and 102 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 4.513 (13.219) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 11.356 (31.598) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 10.624 (30.625) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 20.181 (32.585) | MISS ceiling | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 27.410 (41.443) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 29.722 (41.443) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 45.449 (83.134) | MISS ceiling | 2 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 47.729 (83.134) | MISS ceiling | 3 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 10.963 (30.768) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 19.785 (39.603) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 10.627 (30.628) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 19.699 (39.518) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 10.670 (30.663) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 27.595 (87.087) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 11.168 (30.679) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 21.016 (54.449) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 19.403 (35.121) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 15.990 (39.218) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 5.694 (38.791) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 8.577 (38.799) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 8.513 (37.513) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 5.665 (31.484) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 14.193 (70.108) | MISS T_svc | 1 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 12.885 (70.108) | MISS T_svc | 3 events | 1 | 1 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 4.432 (24.890) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 5.238 (24.890) | fits | 3 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 15.234 (75.590) | MISS T_svc | 1 events | 1 | 1 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 5.426 (38.640) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 27.137 (76.552) | MISS ceiling | 1 events | 1 | 1 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 26.206 (76.552) | MISS ceiling | 3 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 6.748 (27.032) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 19.804 (40.083) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 2.568 (9.271) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 2.856 (9.270) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 2.379 (8.950) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 2.502 (8.950) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 18.351 (42.598) | MISS T_svc | 1 events | 1 | 1 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 26.844 (42.598) | MISS T_svc | 1 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 32.514 (73.307) | MISS T_svc | 1 events | 5 | 5 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 41.690 (73.307) | MISS T_svc | 1 events | 5 | 5 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.063 (8.284) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 1.374 (4.599) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 2.644 (9.095) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 3.699 (10.871) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 4.999 (11.158) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 5.767 (11.586) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 5.916 (11.353) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 5.211 (11.031) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 14.822 (27.427) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 5.690 (11.104) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 6.570 (12.388) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 6.214 (12.034) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 7.048 (12.866) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 5.206 (11.356) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 8.318 (14.499) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 8.189 (14.640) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 3.518 (9.681) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 3.532 (9.352) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 6.169 (12.334) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 6.190 (12.336) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 6.094 (11.912) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 6.116 (11.934) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 6.078 (11.504) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 5.298 (11.116) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 7.497 (12.923) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 5.767 (11.585) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 5.092 (10.910) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 6.207 (12.025) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 5.537 (11.356) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 6.230 (11.691) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 5.595 (11.413) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 6.264 (11.719) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 6.942 (11.687) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 6.281 (12.099) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 5.384 (11.202) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 5.913 (11.720) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 4.866 (10.684) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 7.474 (15.076) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 7.524 (15.195) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 5.653 (11.471) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 5.685 (11.505) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 5.606 (11.509) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 6.119 (12.563) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 16.075 (21.922) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 16.393 (22.247) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 15.085 (19.863) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 14.794 (19.926) | MISS T_svc | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 14.616 (20.463) | MISS T_svc | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 15.434 (21.288) | MISS T_svc | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 20.683 (27.815) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 22.979 (29.454) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 15.081 (18.862) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 15.643 (21.490) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 15.736 (21.592) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 108.712 (120.299) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 83.506 (107.827) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 118.807 (156.287) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 44.651 (73.699) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 161.102 (170.624) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind1.if0` (backlog-owed) | at least 860.001 | NEVER ANSWERED | 9 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 4.174 (8.855) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.900 (9.405) | fits | 1 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 1.716 (8.047) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.969 (8.231) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 18.489 (38.979) | MISS T_svc | 1 events | 1 | 1 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 17.039 (39.823) | MISS T_svc | 0 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 3.915 (8.855) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.641 (9.405) | fits | 1 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 3.784 (10.885) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 2.963 (9.413) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 27.363 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 177.896 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 27.406 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 137.940 | MISS T_svc | 6 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 88.955 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 27.399 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 510.223 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 27.388 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 103.708 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 658.793 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 658.773 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 14.283 (20.311) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 8.174 (20.999) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 9.114 (12.337) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 8.328 (9.556) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 7.695 (11.044) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 5.694 (9.173) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 15.788 (18.010) | MISS T_svc | 1 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 13.246 (33.172) | MISS T_svc | 1 events | 1 | 1 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 608.765 | 59 | 1,392,016 (27.840) | yes | - |
| backlog-adp | 583.559 | 18 | 2,208,710 (44.174) | no | {'srp': 32} |
| backlog-adp-refill | 658.809 | 21 | 2,209,308 (44.186) | no | {'srp': 32} |
| backlog-owed | 860.053 | 84 | 1,111,766 (22.235) | yes | - |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 761,721 | 15.234 | 10 | 20 | MISS T_svc | 1,934,973 | 93 (14) | 0.889 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 271,282 | 5.426 | 10 | 20 | fits | 1,931,989 | 71 (14) | 0.889 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 53,169 | 1.063 | 10 | 200 | fits | 205,284 | 25 (11) | 0.868 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 68,695 | 1.374 | 10 | 200 | fits | 43,248 | 15 (11) | 0.886 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 924,464 | 18.489 | 10 | 50 | MISS T_svc | 1,048,452 | 178 | 0.864 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 189,196 | 3.784 | 10 | 50 | fits | 251,051 | 44 | 0.874 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 69,941 | 1.399 | 10 | 50 | fits | 214,829 | 38 | 0.872 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 195,752 | 3.915 | 10 | 50 | fits | 247,053 | 65 | 0.875 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 208,700 | 4.174 | 10 | 50 | fits | 247,053 | 65 | 0.875 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 85,813 | 1.716 | 10 | 50 | fits | 211,279 | 48 | 0.868 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 851,969 | 17.039 | 10 | 50 | MISS T_svc | 1,071,742 | 178 | 0.866 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 148,137 | 2.963 | 10 | 50 | fits | 216,431 | 37 | 0.870 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 83,279 | 1.666 | 10 | 50 | fits | 254,180 | 44 | 0.873 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 132,044 | 2.641 | 10 | 50 | fits | 286,163 | 71 | 0.875 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 144,992 | 2.900 | 10 | 50 | fits | 286,163 | 71 | 0.875 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 98,445 | 1.969 | 10 | 50 | fits | 213,312 | 48 | 0.866 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 709,672 | 14.193 | 10 | 20 | MISS T_svc | 1,296,146 | 113 (35) | 0.884 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 644,258 | 12.885 | 10 | 20 | MISS T_svc | 1,296,146 | 113 (35) | 0.884 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 221,590 | 4.432 | 10 | 20 | fits | 1,244,481 | 67 (14) | 0.884 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 261,885 | 5.238 | 10 | 20 | fits | 1,244,481 | 67 (14) | 0.884 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 1,356,847 | 27.137 | 10 | 20 | MISS ceiling | 1,237,282 | 68 (14) | 0.884 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 1,310,294 | 26.206 | 10 | 20 | MISS ceiling | 1,237,282 | 68 (14) | 0.884 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 284,715 | 5.694 | 10 | 20 | fits | 1,939,530 | 93 (35) | 0.889 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 428,855 | 8.577 | 10 | 20 | fits | 1,939,942 | 93 (35) | 0.889 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 789,405 | 15.788 | 10 | 18 | MISS T_svc | 900,485 | 124 | 0.860 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 662,320 | 13.246 | 10 | 18 | MISS T_svc | 610,130 | 160 | 0.855 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 455,724 | 9.114 | 10 | 18 | fits | 299,380 | 36 | 0.866 |
| malformed MRPDU discard | `srp.malformed.if0` | 384,759 | 7.695 | 10 | 18 | fits | 245,990 | 36 | 0.864 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 714,165 | 14.283 | 210 | 218 | fits | 780,248 | 142 | 0.850 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 416,377 | 8.328 | 10 | 18 | fits | 266,435 | 30 | 0.861 |
| malformed MRPDU discard | `srp.malformed.if1` | 284,721 | 5.694 | 10 | 18 | fits | 257,218 | 36 | 0.863 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 408,680 | 8.174 | 210 | 218 | fits | 449,780 | 39 | 0.857 |
| an event behind 15 others | `backlog.event.if0` | 2,232,539 | 44.651 | 10 | 200 | MISS T_svc | 1,392,016 | 364 | 0.877 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 5,435,592 | 108.712 | 10 | 20 | MISS ceiling | 732,610 | 217 | 0.877 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,370,279 | 27.406 | 10 | 200 | MISS T_svc | 881,915 | 386 | 0.876 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 4,447,775 | 88.955 | 10 | 200 | MISS T_svc | 827,550 | 291 | 0.877 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,368,150 | 27.363 | 10 | 20 | MISS ceiling | 881,915 | 386 | 0.876 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 5,948,006 | 118.960 | 10 | 20 | MISS ceiling | 732,610 | 217 | 0.877 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,369,942 | 27.399 | 10 | 24 | MISS ceiling | 881,915 | 386 | 0.876 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 11,248,370 | 224.967 | 10 | 24 | MISS ceiling | 478,451 | 130 | 0.882 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,369,422 | 27.388 | 10 | 50 | MISS T_svc | 881,915 | 386 | 0.876 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 4,447,027 | 88.941 | 10 | 50 | MISS ceiling | 827,550 | 291 | 0.877 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 6,562,356 | 131.247 | 10 | 18 | MISS ceiling | 612,892 | 175 | 0.879 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 13,926,804 | 278.536 | 10 | 18 | MISS ceiling | 283,960 | 54 | 0.866 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 4,175,292 | 83.506 | 10 | 20 | MISS ceiling | 1,916,229 | 363 | 0.883 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 1,080,414 | 21.608 | 10 | 200 | MISS T_svc | 1,287,907 | 391 | 0.881 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 5,183,559 | 103.671 | 10 | 200 | MISS T_svc | 1,916,229 | 363 | 0.883 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 1,080,870 | 21.617 | 10 | 20 | MISS ceiling | 1,287,907 | 391 | 0.881 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 8,856,833 | 177.137 | 10 | 20 | MISS ceiling | 1,939,489 | 272 | 0.885 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 1,082,663 | 21.653 | 10 | 24 | MISS T_svc | 1,287,907 | 391 | 0.881 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 25,360,345 | 507.207 | 10 | 24 | MISS ceiling | 1,556,087 | 208 | 0.886 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 1,082,143 | 21.643 | 10 | 50 | MISS T_svc | 1,287,907 | 391 | 0.881 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 5,185,397 | 103.708 | 10 | 50 | MISS ceiling | 1,916,229 | 363 | 0.883 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 29,177,097 | 583.542 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 29,176,090 | 583.522 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 5,940,372 | 118.807 | 10 | 20 | MISS ceiling | 2,052,038 | 304 | 0.884 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 1,080,414 | 21.608 | 10 | 200 | MISS T_svc | 1,287,907 | 391 | 0.881 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 6,897,001 | 137.940 | 10 | 200 | MISS T_svc | 2,052,038 | 304 | 0.884 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 1,080,870 | 21.617 | 10 | 20 | MISS ceiling | 1,287,907 | 391 | 0.881 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 8,894,807 | 177.896 | 10 | 20 | MISS ceiling | 2,052,038 | 304 | 0.884 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 1,082,663 | 21.653 | 10 | 24 | MISS T_svc | 1,287,907 | 391 | 0.881 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 25,511,137 | 510.223 | 10 | 24 | MISS ceiling | 1,668,432 | 185 | 0.889 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 1,082,143 | 21.643 | 10 | 50 | MISS T_svc | 1,287,907 | 391 | 0.881 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 5,084,681 | 101.694 | 10 | 50 | MISS ceiling | 1,815,513 | 356 | 0.884 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 32,939,635 | 658.793 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 32,938,628 | 658.773 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 8,055,113 | 161.102 | 10 | 20 | MISS ceiling | 587,791 | 152 | 0.878 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 8,825,989 | 176.520 | 10 | 20 | MISS ceiling | 770,914 | 197 | 0.874 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 43,000,073 | 860.001 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 9,413,605 | 188.272 | 10 | 20 | MISS ceiling | 587,691 | 152 | 0.878 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 42,999,998 | 860.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 903,416 | 18.068 | 10 | 200 | MISS T_svc | 875,875 | 344 | 0.875 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 3,618,084 | 72.362 | 10 | 200 | MISS T_svc | 959,228 | 288 | 0.875 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 901,286 | 18.026 | 10 | 20 | MISS T_svc | 875,875 | 344 | 0.875 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 5,269,518 | 105.390 | 10 | 20 | MISS ceiling | 826,771 | 201 | 0.875 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 903,079 | 18.062 | 10 | 24 | MISS T_svc | 875,875 | 344 | 0.875 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 11,205,284 | 224.106 | 10 | 24 | MISS ceiling | 491,827 | 130 | 0.881 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 902,559 | 18.051 | 10 | 50 | MISS T_svc | 875,875 | 344 | 0.875 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 3,617,337 | 72.347 | 10 | 50 | MISS ceiling | 959,228 | 288 | 0.875 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 7,195,626 | 143.913 | 10 | 18 | MISS ceiling | 799,904 | 197 | 0.875 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 17,042,393 | 340.848 | 10 | 18 | MISS ceiling | 241,120 | 30 | 0.861 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,272,459 | 45.449 | 10 | 20 | MISS ceiling | 1,699,407 | 177 (29) | 0.886 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 2,386,439 | 47.729 | 10 | 20 | MISS ceiling | 1,699,407 | 177 (29) | 0.886 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,370,524 | 27.410 | 10 | 20 | MISS ceiling | 2,072,158 | 129 (35) | 0.887 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,486,120 | 29.722 | 10 | 20 | MISS ceiling | 2,072,158 | 129 (35) | 0.887 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 425,632 | 8.513 | 10 | 20 | fits | 1,875,664 | 67 (12) | 0.871 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 283,246 | 5.665 | 10 | 20 | fits | 1,574,180 | 90 (12) | 0.888 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| LINK_DOWN | `adp.link_down.if0` | 917,527 | 18.351 | 10 | 200 | MISS T_svc | 1,169,168 | 70 (9) | 0.876 |
| LINK_DOWN | `adp.link_down.if1` | 1,342,185 | 26.844 | 10 | 200 | MISS T_svc | 1,169,168 | 70 (9) | 0.876 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| GM_CHANGE | `adp.gm_change.if0` | 118,927 | 2.379 | 10 | 200 | fits | 209,423 | 34 (11) | 0.867 |
| GM_CHANGE | `adp.gm_change.if1` | 125,077 | 2.502 | 10 | 200 | fits | 209,423 | 34 (11) | 0.867 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 128,423 | 2.568 | 10 | 200 | fits | 225,549 | 73 (31) | 0.867 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 142,798 | 2.856 | 10 | 200 | fits | 225,549 | 73 (31) | 0.867 |
| LINK_UP | `adp.link_up.if0` | 1,625,718 | 32.514 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| LINK_UP | `adp.link_up.if1` | 2,084,480 | 41.690 | 10 | 200 | MISS T_svc | 2,004,666 | 345 (11) | 0.865 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 132,204 | 2.644 | 10 | 200 | fits | 194,884 | 47 (39) | 0.866 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 184,969 | 3.699 | 10 | 200 | fits | 230,949 | 53 (39) | 0.869 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 128,423 | 2.568 | 10 | 200 | fits | 211,550 | 45 (31) | 0.867 |
| set_name | `aecp_fanout.set_name.if0` | 1,034,137 | 20.683 | 10 | 24 | MISS T_svc | 1,205,519 | 1137 | 0.883 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 754,267 | 15.085 | 10 | 24 | MISS T_svc | 794,840 | 596 | 0.879 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 730,813 | 14.616 | 10 | 24 | MISS T_svc | 751,081 | 556 | 0.879 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 619,292 | 12.386 | 10 | 24 | MISS T_svc | 787,071 | 563 | 0.880 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 754,072 | 15.081 | 10 | 24 | MISS T_svc | 744,918 | 589 | 0.879 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 803,735 | 16.075 | 10 | 24 | MISS T_svc | 825,430 | 662 | 0.882 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 782,173 | 15.643 | 10 | 24 | MISS T_svc | 787,713 | 655 | 0.882 |
| set_name | `aecp_fanout.set_name.if1` | 1,148,961 | 22.979 | 10 | 24 | MISS T_svc | 1,186,488 | 1137 | 0.882 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 739,685 | 14.794 | 10 | 24 | MISS T_svc | 761,014 | 590 | 0.879 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 771,679 | 15.434 | 10 | 24 | MISS T_svc | 790,359 | 563 | 0.880 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 748,139 | 14.963 | 10 | 24 | MISS T_svc | 752,249 | 556 | 0.880 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 819,673 | 16.393 | 10 | 24 | MISS T_svc | 824,048 | 662 | 0.882 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 786,796 | 15.736 | 10 | 24 | MISS T_svc | 791,521 | 655 | 0.882 |
| BIND_RX | `acmp.bind_rx.if0` | 225,669 | 4.513 | 10 | 20 | fits | 397,264 | 90 (77) | 0.870 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 970,162 | 19.403 | 10 | 20 | MISS T_svc | 1,756,026 | 102 (32) | 0.886 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 548,143 | 10.963 | 10 | 20 | MISS T_svc | 1,538,378 | 114 (47) | 0.886 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 337,377 | 6.748 | 10 | 20 | fits | 1,351,576 | 176 (50) | 0.884 |
| PROBE_TX | `acmp.probe_tx.if0` | 558,421 | 11.168 | 10 | 20 | MISS T_svc | 1,533,927 | 116 (48) | 0.886 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 533,518 | 10.670 | 10 | 20 | MISS T_svc | 1,533,135 | 115 (48) | 0.886 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 531,202 | 10.624 | 10 | 20 | MISS T_svc | 1,531,239 | 115 (48) | 0.886 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 531,375 | 10.627 | 10 | 20 | MISS T_svc | 1,531,412 | 115 (48) | 0.886 |
| BIND_RX | `acmp.bind_rx.if1` | 567,820 | 11.356 | 10 | 20 | MISS T_svc | 1,579,911 | 145 (77) | 0.885 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 799,519 | 15.990 | 10 | 20 | MISS T_svc | 1,960,887 | 97 (32) | 0.888 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 989,260 | 19.785 | 10 | 20 | MISS T_svc | 1,980,144 | 112 (47) | 0.888 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 990,219 | 19.804 | 10 | 20 | MISS T_svc | 2,004,171 | 115 (50) | 0.888 |
| PROBE_TX | `acmp.probe_tx.if1` | 1,050,781 | 21.016 | 10 | 20 | MISS ceiling | 2,722,461 | 330 (48) | 0.875 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 1,379,768 | 27.595 | 10 | 20 | MISS ceiling | 1,631,892 | 134 (48) | 0.887 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 1,009,034 | 20.181 | 10 | 20 | MISS ceiling | 1,629,266 | 134 (48) | 0.887 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 984,953 | 19.699 | 10 | 20 | MISS T_svc | 1,975,919 | 113 (48) | 0.889 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 295,637 | 5.913 | 10 | 24 | fits | 322,322 | 54 | 0.876 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 308,462 | 6.169 | 10 | 24 | fits | 419,415 | 125 | 0.881 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 304,685 | 6.094 | 10 | 24 | fits | 415,178 | 80 | 0.880 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 310,358 | 6.207 | 10 | 24 | fits | 420,854 | 121 | 0.880 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 347,097 | 6.942 | 10 | 24 | fits | 387,250 | 83 | 0.880 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 314,051 | 6.281 | 10 | 24 | fits | 424,778 | 90 | 0.880 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 269,182 | 5.384 | 10 | 24 | fits | 379,768 | 72 | 0.880 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 303,905 | 6.078 | 10 | 24 | fits | 378,116 | 69 | 0.880 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 264,885 | 5.298 | 10 | 24 | fits | 375,226 | 65 | 0.880 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 374,850 | 7.497 | 10 | 24 | fits | 448,860 | 160 | 0.882 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 288,349 | 5.767 | 10 | 24 | fits | 401,741 | 59 | 0.879 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 254,607 | 5.092 | 10 | 24 | fits | 366,939 | 52 | 0.879 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 311,494 | 6.230 | 10 | 24 | fits | 388,308 | 70 | 0.878 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 279,743 | 5.595 | 10 | 24 | fits | 392,458 | 75 | 0.879 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 313,215 | 6.264 | 10 | 24 | fits | 389,334 | 71 | 0.879 |
| get_configuration | `aecp.get_configuration.if0` | 741,103 | 14.822 | 10 | 24 | MISS T_svc | 429,227 | 60 | 0.880 |
| entity_available | `aecp.entity_available.if0` | 249,962 | 4.999 | 10 | 24 | fits | 360,902 | 51 | 0.880 |
| get_name | `aecp.get_name.if0` | 352,412 | 7.048 | 10 | 24 | fits | 463,357 | 99 | 0.881 |
| get_counters | `aecp.get_counters.if0` | 328,487 | 6.570 | 10 | 24 | fits | 383,452 | 80 | 0.881 |
| get_avb_info | `aecp.get_avb_info.if0` | 295,784 | 5.916 | 10 | 24 | fits | 370,724 | 48 | 0.878 |
| unknown_command | `aecp.unknown_command.if0` | 282,639 | 5.653 | 10 | 24 | fits | 393,659 | 54 | 0.880 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 175,890 | 3.518 | 10 | 24 | fits | 287,415 | 52 | 0.875 |
| set_name | `aecp.set_name.if0` | 373,683 | 7.474 | 10 | 24 | fits | 574,214 | 114 | 0.872 |
| lock_entity | `aecp.lock_entity.if0` | 415,903 | 8.318 | 10 | 24 | fits | 414,858 | 73 | 0.880 |
| unlock_entity | `aecp.unlock_entity.if0` | 280,323 | 5.606 | 10 | 24 | fits | 377,791 | 66 | 0.879 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 243,277 | 4.866 | 10 | 24 | fits | 322,957 | 52 | 0.876 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 309,523 | 6.190 | 10 | 24 | fits | 419,147 | 123 | 0.881 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 305,789 | 6.116 | 10 | 24 | fits | 415,313 | 78 | 0.881 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 276,870 | 5.537 | 10 | 24 | fits | 386,540 | 82 | 0.880 |
| get_configuration | `aecp.get_configuration.if1` | 284,520 | 5.690 | 10 | 24 | fits | 357,532 | 46 | 0.879 |
| entity_available | `aecp.entity_available.if1` | 288,329 | 5.767 | 10 | 24 | fits | 397,872 | 56 | 0.880 |
| get_name | `aecp.get_name.if1` | 260,314 | 5.206 | 10 | 24 | fits | 370,756 | 62 | 0.880 |
| get_counters | `aecp.get_counters.if1` | 310,723 | 6.214 | 10 | 24 | fits | 420,382 | 85 | 0.881 |
| get_avb_info | `aecp.get_avb_info.if1` | 260,573 | 5.211 | 10 | 24 | fits | 370,125 | 45 | 0.879 |
| unknown_command | `aecp.unknown_command.if1` | 284,265 | 5.685 | 10 | 24 | fits | 394,012 | 52 | 0.880 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 176,594 | 3.532 | 10 | 24 | fits | 286,816 | 49 | 0.875 |
| set_name | `aecp.set_name.if1` | 376,217 | 7.524 | 10 | 24 | fits | 578,124 | 147 | 0.870 |
| lock_entity | `aecp.lock_entity.if1` | 409,460 | 8.189 | 10 | 24 | fits | 428,393 | 92 | 0.880 |
| unlock_entity | `aecp.unlock_entity.if1` | 305,942 | 6.119 | 10 | 24 | fits | 390,914 | 85 | 0.879 |

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
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
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
