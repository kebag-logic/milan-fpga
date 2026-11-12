### 8x8

31 of 129 paths and 59 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.839 (3.351) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 15.427 (35.693) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 17.203 (37.203) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 7.358 (27.358) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 18.437 (27.827) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 18.925 (27.827) | MISS T_svc | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 18.493 (27.751) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 18.945 (27.751) | MISS T_svc | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 17.524 (37.263) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 4.523 (32.450) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 15.070 (35.071) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 3.640 (23.641) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 15.124 (35.115) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 3.682 (23.673) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 17.634 (37.219) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 7.823 (27.401) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 3.415 (20.371) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 5.861 (27.426) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 2.891 (23.290) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 3.105 (46.427) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 7.377 (45.230) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 2.723 (48.949) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 1.301 (23.264) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 6.613 (46.521) | fits | 1 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 6.894 (42.431) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 5.474 (42.431) | fits | 3 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 3.174 (23.302) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 1.940 (19.623) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 4.719 (42.338) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 4.605 (19.220) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 10.800 (31.159) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 11.968 (24.144) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.202 (2.402) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.376 (2.402) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.082 (2.237) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.174 (2.237) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.064 (12.456) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.011 (12.456) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.079 (12.077) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.796 (12.077) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.420 (2.473) | fits | 1 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 1.328 (3.473) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 2.231 (6.345) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 1.912 (6.345) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.840 (4.514) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.848 (4.523) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.561 (4.235) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.555 (4.230) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.395 (4.069) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.819 (4.495) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.754 (4.813) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 2.704 (4.379) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.555 (4.229) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 2.984 (4.660) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 3.284 (5.165) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.856 (4.875) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.138 (3.812) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 1.706 (3.381) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.521 (5.195) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.511 (5.185) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.639 (4.313) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 3.063 (4.737) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 2.636 (4.310) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.607 (4.280) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.429 (5.103) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.507 (4.181) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 2.517 (4.191) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.732 (4.406) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 2.726 (4.400) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 3.201 (4.875) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.810 (4.484) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.775 (4.449) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 3.170 (4.844) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 2.751 (4.425) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.656 (4.330) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.707 (3.375) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 2.129 (3.804) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.271 (7.297) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.889 (6.584) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.394 (4.068) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.817 (4.492) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 3.280 (5.160) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 3.286 (5.300) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 7.682 (9.378) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 7.219 (8.915) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.783 (12.378) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 8.239 (11.834) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 6.914 (10.676) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 8.842 (12.604) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.184 (13.948) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 10.411 (14.691) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 7.826 (10.548) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.967 (12.730) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 7.368 (11.130) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 51.129 (56.134) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 39.882 (59.325) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 41.201 (58.546) | MISS ceiling | 2 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 12.858 (24.647) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 112.723 (117.669) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 138.526 (142.934) | MISS ceiling | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.413 (5.487) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 1.856 (6.018) | fits | 1 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.594 (2.564) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.023 (3.043) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.695 (6.824) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 1.117 (7.289) | fits | 1 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.265 (5.487) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 1.708 (6.018) | fits | 1 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 2.421 (6.878) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 2.289 (6.411) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 12.271 | MISS T_svc | 0 acmp | 4 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 88.933 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 12.313 | MISS T_svc | 0 adp | 4 | 3 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 48.976 | MISS T_svc | 2 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 42.650 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 12.306 | MISS T_svc | 0 aecp | 4 | 3 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 298.837 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 12.296 | MISS T_svc | 0 maap | 4 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 48.246 | MISS T_svc | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 581.187 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 581.166 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 7.713 (9.498) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 7.871 (9.564) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.342 (3.343) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.924 (3.925) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 3.097 (3.098) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.249 (3.250) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.317 (6.824) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.407 (6.865) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 141.823 | 22 | 616,581 (12.332) | yes | - |
| backlog-adp | 539.935 | 29 | 1,443,942 (28.879) | no | {'srp': 32} |
| backlog-adp-refill | 581.203 | 32 | 1,443,970 (28.879) | no | {'srp': 32} |
| backlog-owed | 160.594 | 25 | 478,510 (9.570) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,443,970 CPU cycles (28.879 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 616,581 (12.332 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 158,693 | 3.174 | 10 | 20 | fits | 1,165,104 | 166 (14) | 0.027 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 97,011 | 1.940 | 10 | 20 | fits | 981,152 | 127 (14) | 0.030 |
| LINK_UP | `adp.link_up.if0` | 3,942 | 0.079 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| LINK_UP | `adp.link_up.if1` | 39,810 | 0.796 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 111,565 | 2.231 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,595 | 1.912 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 21,012 | 0.420 | 10 | 200 | fits | 8,594 | 18 (11) | 0.137 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 66,382 | 1.328 | 10 | 200 | fits | 8,594 | 18 (11) | 0.137 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 34,731 | 0.695 | 10 | 50 | fits | 341,197 | 154 | 0.035 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 121,043 | 2.421 | 10 | 50 | fits | 151,533 | 44 | 0.065 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 65,957 | 1.319 | 10 | 50 | fits | 130,494 | 38 | 0.060 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 63,256 | 1.265 | 10 | 50 | fits | 167,817 | 71 | 0.063 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 70,657 | 1.413 | 10 | 50 | fits | 167,817 | 71 | 0.063 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 29,685 | 0.594 | 10 | 50 | fits | 128,194 | 47 | 0.055 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 55,870 | 1.117 | 10 | 50 | fits | 364,430 | 160 | 0.038 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 54,808 | 1.096 | 10 | 50 | fits | 153,692 | 44 | 0.064 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 114,428 | 2.289 | 10 | 50 | fits | 132,651 | 38 | 0.061 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 85,383 | 1.708 | 10 | 50 | fits | 170,179 | 71 | 0.064 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 92,784 | 1.856 | 10 | 50 | fits | 170,179 | 71 | 0.064 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 51,152 | 1.023 | 10 | 50 | fits | 152,155 | 54 | 0.061 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 65,056 | 1.301 | 10 | 20 | fits | 1,163,190 | 166 (35) | 0.026 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 330,656 | 6.613 | 10 | 20 | fits | 1,162,870 | 166 (35) | 0.026 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 344,701 | 6.894 | 10 | 20 | fits | 966,706 | 129 (14) | 0.030 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 273,725 | 5.474 | 10 | 20 | fits | 966,706 | 129 (14) | 0.030 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 235,944 | 4.719 | 10 | 20 | fits | 960,994 | 130 (14) | 0.030 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 230,266 | 4.605 | 10 | 20 | fits | 960,994 | 130 (14) | 0.030 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 144,537 | 2.891 | 10 | 20 | fits | 1,164,508 | 166 (35) | 0.026 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 155,270 | 3.105 | 10 | 20 | fits | 1,164,425 | 166 (35) | 0.026 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 315,830 | 6.317 | 10 | 18 | fits | 341,197 | 154 | 0.035 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 320,344 | 6.407 | 10 | 18 | fits | 343,232 | 154 | 0.036 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 167,110 | 3.342 | 10 | 18 | fits | 167,142 | 29 | 0.071 |
| malformed MRPDU discard | `srp.malformed.if0` | 154,858 | 3.097 | 10 | 18 | fits | 154,890 | 36 | 0.063 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 385,654 | 7.713 | 210 | 218 | fits | 474,912 | 142 | 0.046 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 196,213 | 3.924 | 10 | 18 | fits | 196,245 | 36 | 0.071 |
| malformed MRPDU discard | `srp.malformed.if1` | 162,446 | 3.249 | 10 | 18 | fits | 162,478 | 36 | 0.060 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 393,541 | 7.871 | 210 | 218 | fits | 478,219 | 142 | 0.045 |
| an event behind 15 others | `backlog.event.if0` | 642,877 | 12.858 | 10 | 200 | MISS T_svc | 616,581 | 377 | 0.062 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,556,437 | 51.129 | 10 | 20 | MISS ceiling | 299,295 | 213 | 0.043 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 615,657 | 12.313 | 10 | 200 | MISS T_svc | 615,761 | 394 | 0.061 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,132,498 | 42.650 | 10 | 200 | MISS T_svc | 408,808 | 326 | 0.051 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 613,528 | 12.271 | 10 | 20 | MISS T_svc | 615,761 | 394 | 0.061 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,804,076 | 56.082 | 10 | 20 | MISS ceiling | 299,295 | 213 | 0.043 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 615,320 | 12.306 | 10 | 24 | MISS T_svc | 615,761 | 394 | 0.061 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 5,768,790 | 115.376 | 10 | 24 | MISS ceiling | 246,181 | 126 | 0.038 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 614,800 | 12.296 | 10 | 50 | MISS T_svc | 615,761 | 394 | 0.061 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,131,750 | 42.635 | 10 | 50 | MISS T_svc | 408,808 | 326 | 0.051 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,722,910 | 34.458 | 10 | 18 | MISS ceiling | 491,756 | 375 | 0.055 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 6,775,845 | 135.517 | 10 | 18 | MISS ceiling | 179,269 | 54 | 0.067 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,994,103 | 39.882 | 10 | 20 | MISS ceiling | 891,509 | 393 | 0.038 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 568,830 | 11.377 | 10 | 200 | MISS T_svc | 1,124,325 | 449 | 0.032 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,410,474 | 48.209 | 10 | 200 | MISS T_svc | 891,509 | 393 | 0.038 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 569,286 | 11.386 | 10 | 20 | MISS T_svc | 1,124,325 | 449 | 0.032 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,424,090 | 88.482 | 10 | 20 | MISS ceiling | 953,704 | 309 | 0.034 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 571,078 | 11.422 | 10 | 24 | MISS T_svc | 1,124,325 | 449 | 0.032 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 14,919,490 | 298.390 | 10 | 24 | MISS ceiling | 1,004,914 | 232 | 0.029 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 570,558 | 11.411 | 10 | 50 | MISS T_svc | 1,124,325 | 449 | 0.032 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,412,312 | 48.246 | 10 | 50 | MISS T_svc | 891,509 | 393 | 0.038 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 26,995,908 | 539.918 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 26,994,901 | 539.898 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,060,063 | 41.201 | 10 | 20 | MISS ceiling | 979,386 | 341 | 0.035 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 568,830 | 11.377 | 10 | 200 | MISS T_svc | 1,124,325 | 449 | 0.032 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,448,822 | 48.976 | 10 | 200 | MISS T_svc | 979,386 | 341 | 0.035 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 569,286 | 11.386 | 10 | 20 | MISS T_svc | 1,124,325 | 449 | 0.032 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,446,628 | 88.933 | 10 | 20 | MISS ceiling | 979,386 | 341 | 0.035 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 571,078 | 11.422 | 10 | 24 | MISS T_svc | 1,124,325 | 449 | 0.032 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 14,941,836 | 298.837 | 10 | 24 | MISS ceiling | 1,005,019 | 232 | 0.029 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 570,558 | 11.411 | 10 | 50 | MISS T_svc | 1,124,325 | 449 | 0.032 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,394,104 | 47.882 | 10 | 50 | MISS T_svc | 873,301 | 386 | 0.036 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,059,326 | 581.187 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,058,319 | 581.166 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,636,146 | 112.723 | 10 | 20 | MISS ceiling | 262,319 | 149 | 0.041 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,014,436 | 120.289 | 10 | 20 | MISS ceiling | 378,506 | 194 | 0.054 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,393,008 | 127.860 | 10 | 20 | MISS ceiling | 378,609 | 194 | 0.054 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,655,467 | 133.109 | 10 | 20 | MISS ceiling | 262,319 | 149 | 0.041 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,926,314 | 138.526 | 10 | 20 | MISS ceiling | 243,997 | 79 | 0.070 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 458,639 | 9.173 | 10 | 200 | fits | 385,543 | 346 | 0.050 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 1,714,924 | 34.298 | 10 | 200 | MISS T_svc | 478,510 | 302 | 0.057 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 456,510 | 9.130 | 10 | 20 | fits | 385,543 | 346 | 0.050 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 4,103,199 | 82.064 | 10 | 20 | MISS ceiling | 406,488 | 214 | 0.054 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 458,302 | 9.166 | 10 | 24 | fits | 385,543 | 346 | 0.050 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,801,777 | 136.036 | 10 | 24 | MISS ceiling | 262,319 | 149 | 0.041 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 457,782 | 9.156 | 10 | 50 | fits | 385,543 | 346 | 0.050 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,714,176 | 34.284 | 10 | 50 | MISS T_svc | 478,510 | 302 | 0.057 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,714,144 | 34.283 | 10 | 18 | MISS ceiling | 478,510 | 302 | 0.057 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 7,198,931 | 143.979 | 10 | 18 | MISS ceiling | 154,425 | 29 | 0.067 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 924,669 | 18.493 | 10 | 20 | MISS T_svc | 1,387,558 | 208 (29) | 0.025 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 947,265 | 18.945 | 10 | 20 | MISS T_svc | 1,387,558 | 208 (29) | 0.025 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 921,847 | 18.437 | 10 | 20 | MISS T_svc | 1,391,368 | 219 (35) | 0.025 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 946,270 | 18.925 | 10 | 20 | MISS T_svc | 1,391,368 | 219 (35) | 0.025 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 368,846 | 7.377 | 10 | 20 | fits | 1,007,184 | 123 (12) | 0.023 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 136,160 | 2.723 | 10 | 20 | fits | 1,054,675 | 149 (12) | 0.029 |
| LINK_UP | `adp.link_up.if0` | 3,942 | 0.079 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| LINK_UP | `adp.link_up.if1` | 39,810 | 0.796 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 111,565 | 2.231 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,595 | 1.912 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| LINK_DOWN | `adp.link_down.if0` | 3,179 | 0.064 | 10 | 200 | fits | 622,791 | 52 (9) | 0.076 |
| LINK_DOWN | `adp.link_down.if1` | 250,527 | 5.011 | 10 | 200 | fits | 622,791 | 52 (9) | 0.076 |
| LINK_UP | `adp.link_up.if0` | 3,942 | 0.079 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| LINK_UP | `adp.link_up.if1` | 39,810 | 0.796 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 111,565 | 2.231 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,595 | 1.912 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| GM_CHANGE | `adp.gm_change.if0` | 4,085 | 0.082 | 10 | 200 | fits | 111,873 | 28 (11) | 0.066 |
| GM_CHANGE | `adp.gm_change.if1` | 8,713 | 0.174 | 10 | 200 | fits | 111,873 | 28 (11) | 0.066 |
| LINK_UP | `adp.link_up.if0` | 3,942 | 0.079 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| LINK_UP | `adp.link_up.if1` | 39,810 | 0.796 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 111,565 | 2.231 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,595 | 1.912 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 10,103 | 0.202 | 10 | 200 | fits | 120,125 | 67 (31) | 0.057 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 18,792 | 0.376 | 10 | 200 | fits | 120,125 | 67 (31) | 0.057 |
| LINK_UP | `adp.link_up.if0` | 3,942 | 0.079 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| LINK_UP | `adp.link_up.if1` | 39,810 | 0.796 | 10 | 200 | fits | 603,852 | 304 (11) | 0.034 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 111,565 | 2.231 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 95,595 | 1.912 | 10 | 200 | fits | 134,582 | 84 (39) | 0.064 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 10,103 | 0.202 | 10 | 200 | fits | 111,657 | 39 (31) | 0.059 |
| set_name | `aecp_fanout.set_name.if0` | 559,189 | 11.184 | 10 | 24 | MISS T_svc | 697,385 | 1179 | 0.048 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 439,136 | 8.783 | 10 | 24 | fits | 431,286 | 614 | 0.068 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 341,941 | 6.839 | 10 | 24 | fits | 426,725 | 580 | 0.066 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 345,718 | 6.914 | 10 | 24 | fits | 426,225 | 581 | 0.065 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 391,276 | 7.826 | 10 | 24 | fits | 402,973 | 592 | 0.072 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 384,086 | 7.682 | 10 | 24 | fits | 468,908 | 686 | 0.066 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 448,355 | 8.967 | 10 | 24 | fits | 446,335 | 679 | 0.064 |
| set_name | `aecp_fanout.set_name.if1` | 520,565 | 10.411 | 10 | 24 | MISS T_svc | 627,022 | 1132 | 0.045 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 411,938 | 8.239 | 10 | 24 | fits | 432,418 | 613 | 0.069 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 442,087 | 8.842 | 10 | 24 | fits | 428,177 | 580 | 0.068 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 347,435 | 6.949 | 10 | 24 | fits | 427,535 | 581 | 0.066 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 360,962 | 7.219 | 10 | 24 | fits | 445,764 | 679 | 0.063 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 368,382 | 7.368 | 10 | 24 | fits | 448,412 | 680 | 0.066 |
| BIND_RX | `acmp.bind_rx.if0` | 41,947 | 0.839 | 10 | 20 | fits | 167,572 | 83 (77) | 0.065 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 170,754 | 3.415 | 10 | 20 | fits | 1,018,558 | 154 (32) | 0.031 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 876,205 | 17.524 | 10 | 20 | MISS T_svc | 998,051 | 169 (47) | 0.029 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 540,016 | 10.800 | 10 | 20 | MISS T_svc | 693,574 | 204 (50) | 0.040 |
| PROBE_TX | `acmp.probe_tx.if0` | 881,704 | 17.634 | 10 | 20 | MISS T_svc | 892,136 | 161 (48) | 0.032 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 756,194 | 15.124 | 10 | 20 | MISS T_svc | 892,260 | 160 (48) | 0.032 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 860,139 | 17.203 | 10 | 20 | MISS T_svc | 996,397 | 170 (48) | 0.029 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 753,501 | 15.070 | 10 | 20 | MISS T_svc | 890,666 | 160 (48) | 0.032 |
| BIND_RX | `acmp.bind_rx.if1` | 771,354 | 15.427 | 10 | 20 | MISS T_svc | 921,032 | 190 (77) | 0.033 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 293,074 | 5.861 | 10 | 20 | fits | 1,371,320 | 187 (32) | 0.025 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 226,156 | 4.523 | 10 | 20 | fits | 1,622,503 | 401 (47) | 0.025 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 598,381 | 11.968 | 10 | 20 | MISS T_svc | 1,207,213 | 188 (50) | 0.029 |
| PROBE_TX | `acmp.probe_tx.if1` | 391,161 | 7.823 | 10 | 20 | fits | 1,370,069 | 204 (48) | 0.025 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 184,125 | 3.682 | 10 | 20 | fits | 1,183,672 | 186 (48) | 0.027 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 367,920 | 7.358 | 10 | 20 | fits | 1,367,917 | 203 (48) | 0.024 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 182,014 | 3.640 | 10 | 20 | fits | 1,182,051 | 186 (48) | 0.027 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 85,360 | 1.707 | 10 | 24 | fits | 168,750 | 49 | 0.053 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 176,052 | 3.521 | 10 | 24 | fits | 259,751 | 134 | 0.044 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 131,945 | 2.639 | 10 | 24 | fits | 215,641 | 75 | 0.044 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 136,614 | 2.732 | 10 | 24 | fits | 220,310 | 86 | 0.043 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 158,521 | 3.170 | 10 | 24 | fits | 242,220 | 92 | 0.047 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 137,552 | 2.751 | 10 | 24 | fits | 221,251 | 85 | 0.043 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 132,792 | 2.656 | 10 | 24 | fits | 216,491 | 74 | 0.044 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 131,785 | 2.636 | 10 | 24 | fits | 215,484 | 70 | 0.044 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 130,326 | 2.607 | 10 | 24 | fits | 214,022 | 67 | 0.044 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 171,430 | 3.429 | 10 | 24 | fits | 255,126 | 162 | 0.038 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 125,349 | 2.507 | 10 | 24 | fits | 209,045 | 54 | 0.045 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 125,864 | 2.517 | 10 | 24 | fits | 209,560 | 54 | 0.045 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 160,043 | 3.201 | 10 | 24 | fits | 243,739 | 78 | 0.046 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 140,482 | 2.810 | 10 | 24 | fits | 224,178 | 77 | 0.042 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 138,745 | 2.775 | 10 | 24 | fits | 222,441 | 73 | 0.043 |
| get_configuration | `aecp.get_configuration.if0` | 119,755 | 2.395 | 10 | 24 | fits | 203,451 | 49 | 0.046 |
| entity_available | `aecp.entity_available.if0` | 141,991 | 2.840 | 10 | 24 | fits | 225,690 | 60 | 0.050 |
| get_name | `aecp.get_name.if0` | 127,733 | 2.555 | 10 | 24 | fits | 211,432 | 66 | 0.045 |
| get_counters | `aecp.get_counters.if0` | 137,724 | 2.754 | 10 | 24 | fits | 240,626 | 94 | 0.050 |
| get_avb_info | `aecp.get_avb_info.if0` | 128,044 | 2.561 | 10 | 24 | fits | 211,743 | 49 | 0.044 |
| unknown_command | `aecp.unknown_command.if0` | 119,712 | 2.394 | 10 | 24 | fits | 203,411 | 49 | 0.045 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 106,904 | 2.138 | 10 | 24 | fits | 190,603 | 60 | 0.057 |
| set_name | `aecp.set_name.if0` | 213,527 | 4.271 | 10 | 24 | fits | 364,848 | 156 | 0.037 |
| lock_entity | `aecp.lock_entity.if0` | 164,213 | 3.284 | 10 | 24 | fits | 258,252 | 97 | 0.049 |
| unlock_entity | `aecp.unlock_entity.if0` | 163,988 | 3.280 | 10 | 24 | fits | 257,989 | 97 | 0.049 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 106,461 | 2.129 | 10 | 24 | fits | 190,195 | 54 | 0.057 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 175,530 | 3.511 | 10 | 24 | fits | 259,248 | 132 | 0.044 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 153,150 | 3.063 | 10 | 24 | fits | 236,868 | 80 | 0.048 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 136,296 | 2.726 | 10 | 24 | fits | 220,014 | 84 | 0.043 |
| get_configuration | `aecp.get_configuration.if1` | 140,962 | 2.819 | 10 | 24 | fits | 224,726 | 54 | 0.049 |
| entity_available | `aecp.entity_available.if1` | 142,385 | 2.848 | 10 | 24 | fits | 226,149 | 58 | 0.049 |
| get_name | `aecp.get_name.if1` | 149,224 | 2.984 | 10 | 24 | fits | 232,988 | 71 | 0.049 |
| get_counters | `aecp.get_counters.if1` | 135,207 | 2.704 | 10 | 24 | fits | 218,971 | 85 | 0.045 |
| get_avb_info | `aecp.get_avb_info.if1` | 127,745 | 2.555 | 10 | 24 | fits | 211,509 | 47 | 0.044 |
| unknown_command | `aecp.unknown_command.if1` | 140,850 | 2.817 | 10 | 24 | fits | 224,614 | 54 | 0.049 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 85,300 | 1.706 | 10 | 24 | fits | 169,064 | 51 | 0.053 |
| set_name | `aecp.set_name.if1` | 194,449 | 3.889 | 10 | 24 | fits | 329,219 | 149 | 0.038 |
| lock_entity | `aecp.lock_entity.if1` | 142,803 | 2.856 | 10 | 24 | fits | 243,766 | 109 | 0.047 |
| unlock_entity | `aecp.unlock_entity.if1` | 164,285 | 3.286 | 10 | 24 | fits | 264,978 | 116 | 0.050 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
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
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
