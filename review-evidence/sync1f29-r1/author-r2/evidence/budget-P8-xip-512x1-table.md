### 8x8

80 of 128 paths and 122 of 181 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 5.459 (17.473) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 16.931 (37.945) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 12.458 (32.863) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 26.255 (76.128) | MISS ceiling | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 29.479 (77.188) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 31.105 (77.188) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 56.726 (84.789) | MISS ceiling | 2 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 58.285 (84.789) | MISS ceiling | 3 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 13.262 (33.512) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 19.303 (39.456) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 16.129 (35.638) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 22.549 (36.294) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 16.806 (36.046) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 29.713 (75.036) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 15.298 (33.780) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 29.605 (90.148) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 33.607 (54.505) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 18.471 (39.149) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 7.019 (33.649) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 6.499 (38.663) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 14.742 (76.405) | MISS T_svc | 4 events | 1 | 1 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 9.946 (74.356) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 21.252 (69.245) | MISS ceiling | 1 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 19.968 (69.245) | MISS T_svc | 2 events | 1 | 1 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 5.229 (33.511) | fits | 1 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 19.236 (69.408) | MISS T_svc | 2 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 5.518 (34.063) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 12.366 (32.190) | MISS T_svc | 5 events | 1 | 1 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 20.069 (65.838) | MISS ceiling | 1 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 12.702 (33.665) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 22.156 (54.252) | MISS ceiling | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 8.676 (17.659) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 8.839 (17.659) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 6.305 (17.234) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 6.727 (17.234) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 17.542 (48.562) | MISS T_svc | 0 events | 1 | 1 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 26.373 (48.562) | MISS T_svc | 0 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 26.523 (73.038) | MISS T_svc | 0 events | 5 | 5 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 37.182 (73.038) | MISS T_svc | 0 events | 5 | 5 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.983 (14.992) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.413 (2.298) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 3.291 (10.334) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 1.914 (9.623) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 9.404 (20.604) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 9.419 (20.615) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 10.379 (21.055) | MISS T_svc | 0 aecp | 1 | 1 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 10.206 (20.962) | MISS T_svc | 0 aecp | 1 | 1 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 8.379 (12.368) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 9.655 (20.581) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 9.189 (16.469) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 10.689 (21.921) | MISS T_svc | 0 aecp | 1 | 1 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 9.949 (21.329) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 9.793 (21.164) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 14.621 (22.616) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 12.582 (17.599) | MISS T_svc | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 8.388 (19.408) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 8.398 (19.413) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 10.534 (21.878) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 9.781 (21.649) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 9.998 (21.067) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 8.698 (12.817) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 8.694 (12.818) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 9.979 (21.042) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 10.756 (21.827) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 8.546 (12.685) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 9.868 (20.944) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 10.089 (21.158) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 10.103 (21.162) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 10.133 (21.198) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 22.347 (33.504) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 8.954 (18.975) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 13.337 (21.021) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 9.274 (19.346) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 8.301 (12.832) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 7.772 (12.779) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 8.848 (17.470) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 10.890 (24.790) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 10.989 (23.990) | MISS T_svc | 0 aecp | 1 | 1 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 9.281 (20.389) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 9.335 (20.398) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 10.472 (20.861) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 11.438 (20.591) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 13.092 (18.604) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 14.030 (19.445) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 16.952 (34.883) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 15.449 (19.509) | MISS T_svc | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 13.810 (19.301) | MISS T_svc | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 12.933 (18.287) | MISS T_svc | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 18.602 (25.366) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 16.000 (22.221) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 12.321 (17.673) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 22.145 (42.190) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 13.219 (18.498) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 147.108 (161.385) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 92.684 (130.041) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 130.541 (161.456) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 57.673 (99.764) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 225.151 (237.855) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | at least 860.000 | NEVER ANSWERED | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 5.912 (20.465) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 5.402 (20.502) | fits | 1 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 8.250 (20.313) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 9.032 (20.008) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 22.425 (49.559) | MISS T_svc | 0 events | 1 | 1 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 21.617 (48.854) | MISS T_svc | 1 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 5.724 (20.465) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 5.215 (20.502) | fits | 1 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 7.714 (21.039) | fits | 1 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 8.984 (22.810) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 33.708 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 190.214 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 33.750 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 150.258 | MISS T_svc | 6 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 121.012 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 33.743 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 556.646 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 33.733 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 120.997 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 670.526 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 670.506 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 18.369 (29.022) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 20.089 (29.032) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 16.107 (22.009) | MISS T_svc | 0 srp | 1 | 1 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 15.157 (21.319) | MISS T_svc | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 9.507 (9.619) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 10.624 (18.625) | MISS T_svc | 0 srp | 1 | 1 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 14.952 (22.252) | MISS T_svc | 0 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 17.810 (36.803) | MISS T_svc | 1 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 647.161 | 46 | 2,037,839 (40.757) | yes | - |
| backlog-adp | 592.737 | 17 | 2,360,600 (47.212) | no | {'srp': 32} |
| backlog-adp-refill | 670.543 | 19 | 2,360,576 (47.212) | no | {'srp': 32} |
| backlog-owed | 860.053 | 64 | 1,466,664 (29.333) | yes | - |

Composed maximum over the 4 backlog windows: at least 2,360,600 CPU cycles (47.212 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 2,037,839 (40.757 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 275,909 | 5.518 | 10 | 20 | fits | 1,703,172 | 132 (14) | 0.011 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | - | - | - | - | no start: no deadline:3 after the mark | - | - | - |
| LINK_UP | `adp.link_up.if0` | 1,326,164 | 26.523 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,859,115 | 37.182 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 164,565 | 3.291 | 10 | 200 | fits | 516,716 | 53 (39) | 0.027 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,708 | 1.914 | 10 | 200 | fits | 481,143 | 53 (39) | 0.025 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 49,138 | 0.983 | 10 | 200 | fits | 334,096 | 19 (11) | 0.022 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 20,651 | 0.413 | 10 | 200 | fits | 114,895 | 15 (11) | 0.040 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 1,121,240 | 22.425 | 10 | 50 | MISS T_svc | 1,365,369 | 178 | 0.012 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 385,707 | 7.714 | 10 | 50 | fits | 633,134 | 50 | 0.028 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 379,181 | 7.584 | 10 | 50 | fits | 565,996 | 44 | 0.029 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 286,213 | 5.724 | 10 | 50 | fits | 609,591 | 71 | 0.028 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 295,602 | 5.912 | 10 | 50 | fits | 609,591 | 71 | 0.028 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 412,492 | 8.250 | 10 | 50 | fits | 592,015 | 53 | 0.030 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 1,080,847 | 21.617 | 10 | 50 | MISS T_svc | 1,403,784 | 184 | 0.012 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 449,224 | 8.984 | 10 | 50 | fits | 572,398 | 44 | 0.029 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 227,424 | 4.548 | 10 | 50 | fits | 566,858 | 44 | 0.028 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 260,727 | 5.215 | 10 | 50 | fits | 609,910 | 71 | 0.027 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 270,116 | 5.402 | 10 | 50 | fits | 609,910 | 71 | 0.027 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 451,607 | 9.032 | 10 | 50 | fits | 585,018 | 54 | 0.029 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 1,062,623 | 21.252 | 10 | 20 | MISS ceiling | 1,452,398 | 141 (35) | 0.011 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 998,400 | 19.968 | 10 | 20 | MISS T_svc | 1,452,398 | 141 (35) | 0.011 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 261,452 | 5.229 | 10 | 20 | fits | 1,675,548 | 109 (14) | 0.011 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 961,778 | 19.236 | 10 | 20 | MISS T_svc | 1,794,863 | 126 (14) | 0.008 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 618,314 | 12.366 | 10 | 20 | MISS T_svc | 1,609,487 | 110 (14) | 0.010 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 1,003,460 | 20.069 | 10 | 20 | MISS ceiling | 1,682,434 | 135 (14) | 0.010 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 350,954 | 7.019 | 10 | 20 | fits | 1,682,434 | 135 (35) | 0.010 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 324,950 | 6.499 | 10 | 20 | fits | 1,933,152 | 149 (35) | 0.009 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 747,596 | 14.952 | 10 | 18 | MISS T_svc | 1,112,575 | 130 | 0.010 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 890,496 | 17.810 | 10 | 18 | MISS T_svc | 1,840,164 | 292 | 0.007 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 805,330 | 16.107 | 10 | 18 | MISS T_svc | 710,575 | 35 | 0.029 |
| malformed MRPDU discard | `srp.malformed.if0` | 475,359 | 9.507 | 10 | 18 | fits | 480,948 | 36 | 0.022 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 918,439 | 18.369 | 210 | 218 | fits | 1,015,130 | 149 | 0.010 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 757,874 | 15.157 | 10 | 18 | MISS T_svc | 620,174 | 35 | 0.023 |
| malformed MRPDU discard | `srp.malformed.if1` | 531,178 | 10.624 | 10 | 18 | MISS T_svc | 488,101 | 36 | 0.021 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 1,004,428 | 20.089 | 210 | 218 | fits | 1,008,286 | 149 | 0.009 |
| an event behind 15 others | `backlog.event.if0` | 2,883,633 | 57.673 | 10 | 200 | MISS T_svc | 2,037,839 | 377 | 0.015 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 7,355,381 | 147.108 | 10 | 20 | MISS ceiling | 964,778 | 225 | 0.013 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,687,511 | 33.750 | 10 | 200 | MISS T_svc | 1,778,866 | 394 | 0.015 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 6,050,616 | 121.012 | 10 | 200 | MISS T_svc | 1,154,095 | 299 | 0.015 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,685,382 | 33.708 | 10 | 20 | MISS ceiling | 1,778,866 | 394 | 0.015 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 7,975,328 | 159.507 | 10 | 20 | MISS ceiling | 964,778 | 225 | 0.013 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,687,174 | 33.743 | 10 | 24 | MISS ceiling | 1,778,866 | 394 | 0.015 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 16,546,728 | 330.935 | 10 | 24 | MISS ceiling | 878,437 | 177 | 0.017 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,686,654 | 33.733 | 10 | 50 | MISS T_svc | 1,778,866 | 394 | 0.015 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 6,049,868 | 120.997 | 10 | 50 | MISS ceiling | 1,154,095 | 299 | 0.015 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 9,822,536 | 196.451 | 10 | 18 | MISS ceiling | 1,094,011 | 177 | 0.023 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 22,607,096 | 452.142 | 10 | 18 | MISS ceiling | 535,502 | 54 | 0.021 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 4,634,184 | 92.684 | 10 | 20 | MISS ceiling | 1,600,671 | 363 | 0.013 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 1,437,857 | 28.757 | 10 | 200 | MISS T_svc | 2,168,332 | 427 | 0.013 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 5,771,269 | 115.425 | 10 | 200 | MISS T_svc | 1,600,671 | 363 | 0.013 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 1,438,313 | 28.766 | 10 | 20 | MISS ceiling | 2,168,332 | 427 | 0.013 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 9,449,747 | 188.995 | 10 | 20 | MISS ceiling | 1,929,824 | 299 | 0.011 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 1,440,105 | 28.802 | 10 | 24 | MISS ceiling | 2,168,332 | 427 | 0.013 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 27,742,803 | 554.856 | 10 | 24 | MISS ceiling | 1,701,780 | 212 | 0.013 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 1,439,585 | 28.792 | 10 | 50 | MISS T_svc | 2,168,332 | 427 | 0.013 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 5,773,107 | 115.462 | 10 | 50 | MISS ceiling | 1,600,671 | 363 | 0.013 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 29,635,989 | 592.720 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 29,634,982 | 592.700 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 6,527,033 | 130.541 | 10 | 20 | MISS ceiling | 2,047,824 | 331 | 0.011 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 1,437,857 | 28.757 | 10 | 200 | MISS T_svc | 2,168,332 | 427 | 0.013 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 7,512,887 | 150.258 | 10 | 200 | MISS T_svc | 2,047,824 | 331 | 0.011 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 1,438,313 | 28.766 | 10 | 20 | MISS ceiling | 2,168,332 | 427 | 0.013 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 9,510,693 | 190.214 | 10 | 20 | MISS ceiling | 2,047,824 | 331 | 0.011 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 1,440,105 | 28.802 | 10 | 24 | MISS ceiling | 2,168,332 | 427 | 0.013 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 27,832,304 | 556.646 | 10 | 24 | MISS ceiling | 1,868,878 | 222 | 0.012 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 1,439,585 | 28.792 | 10 | 50 | MISS T_svc | 2,168,332 | 427 | 0.013 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 5,680,186 | 113.604 | 10 | 50 | MISS ceiling | 1,507,750 | 356 | 0.014 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 33,526,296 | 670.526 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 33,525,289 | 670.506 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 11,257,570 | 225.151 | 10 | 20 | MISS ceiling | 914,573 | 160 | 0.017 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 12,234,006 | 244.680 | 10 | 20 | MISS ceiling | 1,466,664 | 376 | 0.008 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 13,709,007 | 274.180 | 10 | 20 | MISS ceiling | 1,010,981 | 166 | 0.017 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 14,776,661 | 295.533 | 10 | 20 | MISS ceiling | 1,050,323 | 180 | 0.017 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 42,999,998 | 860.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 1,482,163 | 29.643 | 10 | 200 | MISS T_svc | 1,214,615 | 346 | 0.015 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 5,406,540 | 108.131 | 10 | 200 | MISS T_svc | 1,247,639 | 296 | 0.013 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 1,480,034 | 29.601 | 10 | 20 | MISS ceiling | 1,214,615 | 346 | 0.015 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 7,477,183 | 149.544 | 10 | 20 | MISS ceiling | 1,029,604 | 203 | 0.013 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 1,481,826 | 29.637 | 10 | 24 | MISS ceiling | 1,214,615 | 346 | 0.015 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 18,039,293 | 360.786 | 10 | 24 | MISS ceiling | 932,128 | 177 | 0.015 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 1,481,306 | 29.626 | 10 | 50 | MISS T_svc | 1,214,615 | 346 | 0.015 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 5,405,792 | 108.116 | 10 | 50 | MISS ceiling | 1,247,639 | 296 | 0.013 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 8,768,876 | 175.378 | 10 | 18 | MISS ceiling | 1,290,235 | 186 | 0.022 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 26,697,569 | 533.951 | 10 | 18 | MISS ceiling | 646,954 | 60 | 0.017 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,836,320 | 56.726 | 10 | 20 | MISS ceiling | 1,976,082 | 174 (29) | 0.008 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 2,914,226 | 58.285 | 10 | 20 | MISS ceiling | 1,976,082 | 174 (29) | 0.008 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,473,954 | 29.479 | 10 | 20 | MISS ceiling | 2,030,599 | 185 (35) | 0.009 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,555,228 | 31.105 | 10 | 20 | MISS ceiling | 2,030,599 | 185 (35) | 0.009 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 737,085 | 14.742 | 10 | 20 | MISS T_svc | 1,698,773 | 108 (12) | 0.009 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 497,317 | 9.946 | 10 | 20 | fits | 1,695,012 | 132 (12) | 0.011 |
| LINK_UP | `adp.link_up.if0` | 1,326,164 | 26.523 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,859,115 | 37.182 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 164,565 | 3.291 | 10 | 200 | fits | 516,716 | 53 (39) | 0.027 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,708 | 1.914 | 10 | 200 | fits | 481,143 | 53 (39) | 0.025 |
| LINK_DOWN | `adp.link_down.if0` | 877,105 | 17.542 | 10 | 200 | MISS T_svc | 1,448,379 | 70 (9) | 0.013 |
| LINK_DOWN | `adp.link_down.if1` | 1,318,637 | 26.373 | 10 | 200 | MISS T_svc | 1,448,379 | 70 (9) | 0.013 |
| LINK_UP | `adp.link_up.if0` | 1,326,164 | 26.523 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,859,115 | 37.182 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 164,565 | 3.291 | 10 | 200 | fits | 516,716 | 53 (39) | 0.027 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,708 | 1.914 | 10 | 200 | fits | 481,143 | 53 (39) | 0.025 |
| GM_CHANGE | `adp.gm_change.if0` | 315,239 | 6.305 | 10 | 200 | fits | 446,848 | 34 (11) | 0.025 |
| GM_CHANGE | `adp.gm_change.if1` | 336,371 | 6.727 | 10 | 200 | fits | 446,848 | 34 (11) | 0.025 |
| LINK_UP | `adp.link_up.if0` | 1,326,164 | 26.523 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,859,115 | 37.182 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 164,565 | 3.291 | 10 | 200 | fits | 516,716 | 53 (39) | 0.027 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,708 | 1.914 | 10 | 200 | fits | 481,143 | 53 (39) | 0.025 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 433,776 | 8.676 | 10 | 200 | fits | 468,129 | 73 (31) | 0.025 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 441,950 | 8.839 | 10 | 200 | fits | 468,129 | 73 (31) | 0.025 |
| LINK_UP | `adp.link_up.if0` | 1,326,164 | 26.523 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| LINK_UP | `adp.link_up.if1` | 1,859,115 | 37.182 | 10 | 200 | MISS T_svc | 2,099,901 | 340 (11) | 0.008 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 164,565 | 3.291 | 10 | 200 | fits | 516,716 | 53 (39) | 0.027 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,708 | 1.914 | 10 | 200 | fits | 481,143 | 53 (39) | 0.025 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 433,776 | 8.676 | 10 | 200 | fits | 460,178 | 45 (31) | 0.026 |
| set_name | `aecp_fanout.set_name.if0` | 930,091 | 18.602 | 10 | 24 | MISS T_svc | 1,268,317 | 1178 | 0.009 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 847,590 | 16.952 | 10 | 24 | MISS T_svc | 955,281 | 619 | 0.011 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 690,514 | 13.810 | 10 | 24 | MISS T_svc | 965,038 | 593 | 0.011 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 646,912 | 12.938 | 10 | 24 | MISS T_svc | 912,667 | 587 | 0.010 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 616,058 | 12.321 | 10 | 24 | MISS T_svc | 883,659 | 597 | 0.011 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 654,620 | 13.092 | 10 | 24 | MISS T_svc | 930,200 | 685 | 0.010 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 1,107,234 | 22.145 | 10 | 24 | MISS T_svc | 1,132,139 | 747 | 0.012 |
| set_name | `aecp_fanout.set_name.if1` | 800,014 | 16.000 | 10 | 24 | MISS T_svc | 1,111,031 | 1138 | 0.007 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 772,470 | 15.449 | 10 | 24 | MISS T_svc | 975,447 | 626 | 0.011 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 646,649 | 12.933 | 10 | 24 | MISS T_svc | 914,373 | 586 | 0.010 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 645,707 | 12.914 | 10 | 24 | MISS T_svc | 913,348 | 586 | 0.010 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 701,509 | 14.030 | 10 | 24 | MISS T_svc | 972,235 | 692 | 0.010 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 660,939 | 13.219 | 10 | 24 | MISS T_svc | 924,892 | 685 | 0.010 |
| BIND_RX | `acmp.bind_rx.if0` | 272,942 | 5.459 | 10 | 20 | fits | 873,632 | 89 (77) | 0.028 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 1,680,367 | 33.607 | 10 | 20 | MISS ceiling | 2,005,518 | 144 (32) | 0.012 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 663,081 | 13.262 | 10 | 20 | MISS T_svc | 1,675,601 | 139 (47) | 0.014 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 635,110 | 12.702 | 10 | 20 | MISS T_svc | 1,683,228 | 194 (50) | 0.017 |
| PROBE_TX | `acmp.probe_tx.if0` | 764,921 | 15.298 | 10 | 20 | MISS T_svc | 1,688,986 | 141 (48) | 0.014 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 840,279 | 16.806 | 10 | 20 | MISS T_svc | 1,802,302 | 150 (48) | 0.012 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 622,924 | 12.458 | 10 | 20 | MISS T_svc | 1,643,127 | 140 (48) | 0.013 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 806,450 | 16.129 | 10 | 20 | MISS T_svc | 1,781,905 | 150 (48) | 0.012 |
| BIND_RX | `acmp.bind_rx.if1` | 846,550 | 16.931 | 10 | 20 | MISS T_svc | 1,897,258 | 180 (77) | 0.013 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 923,551 | 18.471 | 10 | 20 | MISS T_svc | 1,957,434 | 153 (32) | 0.009 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 965,163 | 19.303 | 10 | 20 | MISS T_svc | 1,972,779 | 168 (47) | 0.009 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 1,107,798 | 22.156 | 10 | 20 | MISS ceiling | 2,712,615 | 387 (50) | 0.008 |
| PROBE_TX | `acmp.probe_tx.if1` | 1,480,256 | 29.605 | 10 | 20 | MISS ceiling | 1,794,762 | 153 (48) | 0.011 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 1,485,661 | 29.713 | 10 | 20 | MISS ceiling | 1,957,020 | 169 (48) | 0.009 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 1,312,750 | 26.255 | 10 | 20 | MISS ceiling | 1,849,375 | 176 (48) | 0.012 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 1,127,451 | 22.549 | 10 | 20 | MISS ceiling | 1,814,701 | 176 (48) | 0.011 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 388,605 | 7.772 | 10 | 24 | fits | 638,965 | 56 | 0.025 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 526,716 | 10.534 | 10 | 24 | MISS T_svc | 681,181 | 134 | 0.018 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 499,915 | 9.998 | 10 | 24 | fits | 640,662 | 81 | 0.018 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 504,428 | 10.089 | 10 | 24 | MISS T_svc | 645,282 | 92 | 0.018 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 666,843 | 13.337 | 10 | 24 | MISS T_svc | 560,805 | 85 | 0.017 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 463,685 | 9.274 | 10 | 24 | fits | 554,731 | 85 | 0.016 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 415,075 | 8.301 | 10 | 24 | fits | 641,586 | 80 | 0.018 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 434,722 | 8.694 | 10 | 24 | fits | 640,879 | 77 | 0.018 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 498,955 | 9.979 | 10 | 24 | fits | 639,398 | 74 | 0.018 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 537,781 | 10.756 | 10 | 24 | MISS T_svc | 679,037 | 168 | 0.016 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 427,317 | 8.546 | 10 | 24 | fits | 634,270 | 61 | 0.019 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 493,420 | 9.868 | 10 | 24 | fits | 634,862 | 61 | 0.019 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 506,627 | 10.133 | 10 | 24 | MISS T_svc | 647,409 | 78 | 0.018 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 1,117,363 | 22.347 | 10 | 24 | MISS T_svc | 718,785 | 89 | 0.018 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 447,703 | 8.954 | 10 | 24 | fits | 647,394 | 79 | 0.018 |
| get_configuration | `aecp.get_configuration.if0` | 418,956 | 8.379 | 10 | 24 | fits | 618,419 | 56 | 0.019 |
| entity_available | `aecp.entity_available.if0` | 470,202 | 9.404 | 10 | 24 | fits | 617,613 | 60 | 0.018 |
| get_name | `aecp.get_name.if0` | 497,472 | 9.949 | 10 | 24 | fits | 653,830 | 72 | 0.019 |
| get_counters | `aecp.get_counters.if0` | 459,430 | 9.189 | 10 | 24 | fits | 823,447 | 122 | 0.022 |
| get_avb_info | `aecp.get_avb_info.if0` | 518,969 | 10.379 | 10 | 24 | MISS T_svc | 640,137 | 56 | 0.018 |
| unknown_command | `aecp.unknown_command.if0` | 464,040 | 9.281 | 10 | 24 | fits | 607,004 | 56 | 0.018 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 419,407 | 8.388 | 10 | 24 | fits | 557,697 | 60 | 0.021 |
| set_name | `aecp.set_name.if0` | 544,485 | 10.890 | 10 | 24 | MISS T_svc | 826,789 | 149 | 0.014 |
| lock_entity | `aecp.lock_entity.if0` | 731,045 | 14.621 | 10 | 24 | MISS T_svc | 713,786 | 96 | 0.019 |
| unlock_entity | `aecp.unlock_entity.if0` | 523,606 | 10.472 | 10 | 24 | MISS T_svc | 707,284 | 96 | 0.018 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 442,420 | 8.848 | 10 | 24 | fits | 460,757 | 47 | 0.018 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 489,034 | 9.781 | 10 | 24 | fits | 669,628 | 131 | 0.017 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 434,877 | 8.698 | 10 | 24 | fits | 640,853 | 80 | 0.018 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 505,130 | 10.103 | 10 | 24 | MISS T_svc | 645,381 | 91 | 0.018 |
| get_configuration | `aecp.get_configuration.if1` | 482,729 | 9.655 | 10 | 24 | fits | 616,455 | 54 | 0.019 |
| entity_available | `aecp.entity_available.if1` | 470,956 | 9.419 | 10 | 24 | fits | 617,929 | 58 | 0.018 |
| get_name | `aecp.get_name.if1` | 489,641 | 9.793 | 10 | 24 | fits | 645,388 | 71 | 0.019 |
| get_counters | `aecp.get_counters.if1` | 534,448 | 10.689 | 10 | 24 | MISS T_svc | 683,166 | 92 | 0.020 |
| get_avb_info | `aecp.get_avb_info.if1` | 510,290 | 10.206 | 10 | 24 | MISS T_svc | 635,191 | 54 | 0.018 |
| unknown_command | `aecp.unknown_command.if1` | 466,762 | 9.335 | 10 | 24 | fits | 607,035 | 54 | 0.018 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 419,893 | 8.398 | 10 | 24 | fits | 557,750 | 58 | 0.021 |
| set_name | `aecp.set_name.if1` | 549,433 | 10.989 | 10 | 24 | MISS T_svc | 786,726 | 148 | 0.014 |
| lock_entity | `aecp.lock_entity.if1` | 629,089 | 12.582 | 10 | 24 | MISS T_svc | 879,957 | 170 | 0.019 |
| unlock_entity | `aecp.unlock_entity.if1` | 571,893 | 11.438 | 10 | 24 | MISS T_svc | 616,383 | 109 | 0.016 |

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
