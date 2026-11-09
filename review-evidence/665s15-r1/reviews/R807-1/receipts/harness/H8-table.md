### 8x8

31 of 129 paths and 63 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.431 (4.680) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 16.944 (37.100) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 16.511 (36.512) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 5.052 (25.052) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 22.883 (53.525) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 24.163 (53.525) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 17.759 (26.082) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 19.006 (26.082) | MISS T_svc | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 16.751 (36.632) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 5.834 (33.936) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 16.522 (36.523) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 1.753 (21.754) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 18.724 (38.717) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 8.902 (28.896) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 16.870 (36.550) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 5.416 (25.086) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 4.026 (21.423) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 7.151 (28.764) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.488 (21.472) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 3.215 (48.247) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 2.155 (23.117) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 2.558 (50.758) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 3.142 (24.594) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 7.910 (49.183) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 2.515 (24.314) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 7.659 (44.813) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 4.097 (24.646) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 3.368 (24.576) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.359 (24.276) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 8.906 (45.747) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 14.530 (34.731) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 13.468 (25.452) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.199 (2.379) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.375 (2.379) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.079 (2.207) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.171 (2.207) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.063 (12.989) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.063 (12.989) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.078 (12.213) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.862 (12.213) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.266 (2.291) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.172 (2.291) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.453 (5.908) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.848 (4.908) | fits | 1 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.496 (4.124) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.927 (4.558) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 4.588 (6.705) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.618 (4.250) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.894 (4.524) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.889 (4.520) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.772 (4.402) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 2.768 (4.400) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 3.039 (4.668) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 3.048 (4.680) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 3.356 (5.212) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.925 (4.936) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.204 (3.833) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 1.778 (3.408) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.599 (5.229) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.590 (5.220) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 3.134 (4.764) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.697 (4.327) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 2.697 (4.327) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.668 (4.298) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.490 (5.120) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.569 (4.198) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 3.013 (4.643) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.794 (4.424) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 3.350 (6.883) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 2.832 (4.462) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.871 (4.501) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.837 (4.466) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 2.801 (4.431) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 3.249 (4.879) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 4.341 (7.990) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 2.199 (3.822) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 1.760 (3.389) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.337 (7.343) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.959 (6.645) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.455 (4.083) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.884 (4.516) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 3.356 (5.211) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.924 (4.930) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 9.523 (13.211) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 9.696 (13.384) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.126 (9.607) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 7.725 (9.207) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 9.118 (12.805) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 9.308 (12.995) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.360 (14.081) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 10.946 (13.112) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 8.269 (11.769) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.271 (9.920) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 9.753 (13.442) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 58.721 (64.547) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 47.983 (66.599) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 53.763 (68.398) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 14.843 (28.667) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 118.769 (124.507) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 370.366 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 2.671 (6.719) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.570 (6.675) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 1.079 (3.051) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.077 (3.078) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.761 (7.313) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.762 (6.919) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 2.522 (6.719) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.420 (6.675) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 2.111 (6.122) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 2.287 (6.357) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 14.288 | MISS T_svc | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 104.248 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 14.331 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 64.292 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 48.027 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 14.324 | MISS T_svc | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 315.049 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 14.314 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 59.158 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 593.749 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 593.729 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 8.322 (10.070) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 8.552 (10.218) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.308 (3.309) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.376 (3.377) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 3.063 (3.064) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.215 (3.216) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.824 (7.313) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.486 (6.921) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 160.403 | 25 | 716,696 (14.334) | yes | - |
| backlog-adp | 548.036 | 29 | 1,460,384 (29.208) | no | {'srp': 32} |
| backlog-adp-refill | 593.766 | 31 | 1,459,979 (29.200) | no | {'srp': 32} |
| backlog-owed | 370.417 | 43 | 626,234 (12.525) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,460,384 CPU cycles (29.208 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 716,696 (14.334 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 204,856 | 4.097 | 10 | 20 | fits | 1,232,279 | 166 (14) | 0.027 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 168,424 | 3.368 | 10 | 20 | fits | 1,228,824 | 144 (14) | 0.028 |
| LINK_UP | `adp.link_up.if0` | 3,904 | 0.078 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,104 | 0.862 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,629 | 1.453 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,419 | 0.848 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 13,306 | 0.266 | 10 | 200 | fits | 8,669 | 18 (11) | 0.144 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 8,589 | 0.172 | 10 | 200 | fits | 8,669 | 18 (11) | 0.144 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 38,035 | 0.761 | 10 | 50 | fits | 365,665 | 160 | 0.041 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 105,565 | 2.111 | 10 | 50 | fits | 132,882 | 38 | 0.064 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 67,509 | 1.350 | 10 | 50 | fits | 132,853 | 38 | 0.064 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 126,111 | 2.522 | 10 | 50 | fits | 150,925 | 65 | 0.063 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 133,569 | 2.671 | 10 | 50 | fits | 150,925 | 65 | 0.063 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 53,942 | 1.079 | 10 | 50 | fits | 152,554 | 54 | 0.064 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 38,111 | 0.762 | 10 | 50 | fits | 345,948 | 153 | 0.038 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 53,071 | 1.061 | 10 | 50 | fits | 134,361 | 38 | 0.063 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 114,362 | 2.287 | 10 | 50 | fits | 134,332 | 38 | 0.063 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 121,020 | 2.420 | 10 | 50 | fits | 152,386 | 65 | 0.062 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 128,478 | 2.570 | 10 | 50 | fits | 152,386 | 65 | 0.062 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 53,866 | 1.077 | 10 | 50 | fits | 153,897 | 54 | 0.063 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 157,088 | 3.142 | 10 | 20 | fits | 1,229,703 | 166 (35) | 0.027 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 395,511 | 7.910 | 10 | 20 | fits | 1,229,426 | 166 (35) | 0.027 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 125,730 | 2.515 | 10 | 20 | fits | 1,215,702 | 143 (14) | 0.027 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 382,934 | 7.659 | 10 | 20 | fits | 1,024,960 | 126 (14) | 0.029 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 17,943 | 0.359 | 10 | 20 | fits | 1,213,777 | 144 (14) | 0.027 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 445,296 | 8.906 | 10 | 20 | fits | 1,073,587 | 152 (14) | 0.029 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 74,388 | 1.488 | 10 | 20 | fits | 1,073,587 | 152 (35) | 0.029 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 160,773 | 3.215 | 10 | 20 | fits | 1,231,199 | 166 (35) | 0.027 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 341,203 | 6.824 | 10 | 18 | fits | 365,665 | 160 | 0.041 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 324,285 | 6.486 | 10 | 18 | fits | 346,044 | 154 | 0.038 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 165,418 | 3.308 | 10 | 18 | fits | 165,450 | 29 | 0.067 |
| malformed MRPDU discard | `srp.malformed.if0` | 153,175 | 3.063 | 10 | 18 | fits | 153,207 | 36 | 0.058 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 416,081 | 8.322 | 210 | 218 | fits | 503,509 | 149 | 0.046 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 168,793 | 3.376 | 10 | 18 | fits | 168,825 | 29 | 0.066 |
| malformed MRPDU discard | `srp.malformed.if1` | 160,749 | 3.215 | 10 | 18 | fits | 160,781 | 36 | 0.056 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 427,617 | 8.552 | 210 | 218 | fits | 510,904 | 149 | 0.045 |
| an event behind 15 others | `backlog.event.if0` | 742,133 | 14.843 | 10 | 200 | MISS T_svc | 716,696 | 377 | 0.053 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,936,058 | 58.721 | 10 | 20 | MISS ceiling | 412,783 | 219 | 0.036 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 716,548 | 14.331 | 10 | 200 | MISS T_svc | 716,652 | 394 | 0.052 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,401,373 | 48.027 | 10 | 200 | MISS T_svc | 447,768 | 287 | 0.037 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 714,419 | 14.288 | 10 | 20 | MISS T_svc | 716,652 | 394 | 0.052 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,224,723 | 64.494 | 10 | 20 | MISS ceiling | 412,783 | 219 | 0.036 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 716,211 | 14.324 | 10 | 24 | MISS T_svc | 716,652 | 394 | 0.052 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,224,100 | 124.482 | 10 | 24 | MISS ceiling | 248,104 | 126 | 0.038 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 715,691 | 14.314 | 10 | 50 | MISS T_svc | 716,652 | 394 | 0.052 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,400,625 | 48.013 | 10 | 50 | MISS T_svc | 447,768 | 287 | 0.037 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,561,769 | 71.235 | 10 | 18 | MISS ceiling | 335,588 | 171 | 0.052 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,706,848 | 154.137 | 10 | 18 | MISS ceiling | 173,542 | 36 | 0.067 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,399,159 | 47.983 | 10 | 20 | MISS ceiling | 1,163,930 | 403 | 0.032 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 615,688 | 12.314 | 10 | 200 | MISS T_svc | 989,287 | 427 | 0.034 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,956,068 | 59.121 | 10 | 200 | MISS T_svc | 1,163,930 | 403 | 0.032 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 616,144 | 12.323 | 10 | 20 | MISS T_svc | 989,287 | 427 | 0.034 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 5,190,467 | 103.809 | 10 | 20 | MISS ceiling | 1,170,819 | 319 | 0.029 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 617,936 | 12.359 | 10 | 24 | MISS T_svc | 989,287 | 427 | 0.034 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 15,730,392 | 314.608 | 10 | 24 | MISS ceiling | 1,020,207 | 232 | 0.030 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 617,416 | 12.348 | 10 | 50 | MISS T_svc | 989,287 | 427 | 0.034 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,957,906 | 59.158 | 10 | 50 | MISS ceiling | 1,163,930 | 403 | 0.032 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,400,964 | 548.019 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,399,957 | 547.999 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,688,174 | 53.763 | 10 | 20 | MISS ceiling | 1,125,766 | 341 | 0.031 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 615,688 | 12.314 | 10 | 200 | MISS T_svc | 989,287 | 427 | 0.034 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 3,214,581 | 64.292 | 10 | 200 | MISS T_svc | 1,125,766 | 341 | 0.031 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 616,144 | 12.323 | 10 | 20 | MISS T_svc | 989,287 | 427 | 0.034 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 5,212,387 | 104.248 | 10 | 20 | MISS ceiling | 1,125,766 | 341 | 0.031 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 617,936 | 12.359 | 10 | 24 | MISS T_svc | 989,287 | 427 | 0.034 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,752,454 | 315.049 | 10 | 24 | MISS ceiling | 1,020,700 | 232 | 0.030 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 617,416 | 12.348 | 10 | 50 | MISS T_svc | 989,287 | 427 | 0.034 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,902,316 | 58.046 | 10 | 50 | MISS ceiling | 1,108,340 | 396 | 0.032 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,687,437 | 593.749 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,686,430 | 593.729 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,938,433 | 118.769 | 10 | 20 | MISS ceiling | 421,542 | 193 | 0.048 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,518,320 | 370.366 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,518,282 | 370.366 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,518,245 | 370.365 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,518,207 | 370.364 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 567,856 | 11.357 | 10 | 200 | MISS T_svc | 483,458 | 346 | 0.040 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 2,154,272 | 43.085 | 10 | 200 | MISS T_svc | 461,582 | 263 | 0.035 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 565,727 | 11.315 | 10 | 20 | MISS T_svc | 483,458 | 346 | 0.040 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,021,660 | 60.433 | 10 | 20 | MISS ceiling | 400,565 | 122 | 0.047 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 567,519 | 11.350 | 10 | 24 | MISS T_svc | 483,458 | 346 | 0.040 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,116,679 | 142.334 | 10 | 24 | MISS ceiling | 368,894 | 171 | 0.051 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 566,999 | 11.340 | 10 | 50 | MISS T_svc | 483,458 | 346 | 0.040 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,153,524 | 43.070 | 10 | 50 | MISS T_svc | 461,582 | 263 | 0.035 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,691,910 | 33.838 | 10 | 18 | MISS ceiling | 626,234 | 345 | 0.050 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 8,115,438 | 162.309 | 10 | 18 | MISS ceiling | 152,670 | 29 | 0.061 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 887,974 | 17.759 | 10 | 20 | MISS T_svc | 1,304,109 | 191 (29) | 0.027 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 950,292 | 19.006 | 10 | 20 | MISS T_svc | 1,304,109 | 191 (29) | 0.027 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,144,153 | 22.883 | 10 | 20 | MISS ceiling | 1,307,126 | 202 (35) | 0.027 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,208,149 | 24.163 | 10 | 20 | MISS ceiling | 1,307,126 | 202 (35) | 0.027 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 107,738 | 2.155 | 10 | 20 | fits | 1,155,847 | 127 (12) | 0.025 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 127,898 | 2.558 | 10 | 20 | fits | 1,116,939 | 149 (12) | 0.029 |
| LINK_UP | `adp.link_up.if0` | 3,904 | 0.078 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,104 | 0.862 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,629 | 1.453 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,419 | 0.848 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| LINK_DOWN | `adp.link_down.if0` | 3,128 | 0.063 | 10 | 200 | fits | 649,472 | 58 (9) | 0.075 |
| LINK_DOWN | `adp.link_down.if1` | 253,172 | 5.063 | 10 | 200 | fits | 649,472 | 58 (9) | 0.075 |
| LINK_UP | `adp.link_up.if0` | 3,904 | 0.078 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,104 | 0.862 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,629 | 1.453 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,419 | 0.848 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| GM_CHANGE | `adp.gm_change.if0` | 3,969 | 0.079 | 10 | 200 | fits | 110,338 | 28 (11) | 0.060 |
| GM_CHANGE | `adp.gm_change.if1` | 8,572 | 0.171 | 10 | 200 | fits | 110,338 | 28 (11) | 0.060 |
| LINK_UP | `adp.link_up.if0` | 3,904 | 0.078 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,104 | 0.862 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,629 | 1.453 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,419 | 0.848 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 9,972 | 0.199 | 10 | 200 | fits | 118,929 | 67 (31) | 0.053 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 18,727 | 0.375 | 10 | 200 | fits | 118,929 | 67 (31) | 0.053 |
| LINK_UP | `adp.link_up.if0` | 3,904 | 0.078 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,104 | 0.862 | 10 | 200 | fits | 610,648 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,629 | 1.453 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,419 | 0.848 | 10 | 200 | fits | 140,888 | 84 (39) | 0.058 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 9,972 | 0.199 | 10 | 200 | fits | 110,395 | 39 (31) | 0.054 |
| set_name | `aecp_fanout.set_name.if0` | 568,019 | 11.360 | 10 | 24 | MISS T_svc | 704,045 | 1172 | 0.032 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 406,308 | 8.126 | 10 | 24 | fits | 480,349 | 620 | 0.048 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 455,914 | 9.118 | 10 | 24 | fits | 476,077 | 587 | 0.047 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 442,389 | 8.848 | 10 | 24 | fits | 454,202 | 580 | 0.044 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 413,428 | 8.269 | 10 | 24 | fits | 430,699 | 591 | 0.048 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 476,152 | 9.523 | 10 | 24 | fits | 475,551 | 680 | 0.043 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 413,554 | 8.271 | 10 | 24 | fits | 495,982 | 686 | 0.045 |
| set_name | `aecp_fanout.set_name.if1` | 547,303 | 10.946 | 10 | 24 | MISS T_svc | 655,611 | 1132 | 0.032 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 386,254 | 7.725 | 10 | 24 | fits | 460,333 | 613 | 0.046 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 457,026 | 9.141 | 10 | 24 | fits | 455,710 | 580 | 0.044 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 465,417 | 9.308 | 10 | 24 | fits | 455,080 | 580 | 0.044 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 484,818 | 9.696 | 10 | 24 | fits | 474,496 | 680 | 0.043 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 487,627 | 9.753 | 10 | 24 | fits | 476,523 | 680 | 0.043 |
| BIND_RX | `acmp.bind_rx.if0` | 71,554 | 1.431 | 10 | 20 | fits | 234,003 | 90 (77) | 0.052 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 201,318 | 4.026 | 10 | 20 | fits | 1,071,156 | 154 (32) | 0.030 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 837,567 | 16.751 | 10 | 20 | MISS T_svc | 954,017 | 159 (47) | 0.031 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 726,519 | 14.530 | 10 | 20 | MISS T_svc | 858,784 | 214 (50) | 0.034 |
| PROBE_TX | `acmp.probe_tx.if0` | 843,523 | 16.870 | 10 | 20 | MISS T_svc | 951,744 | 161 (48) | 0.031 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 936,188 | 18.724 | 10 | 20 | MISS T_svc | 1,059,555 | 170 (48) | 0.029 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 825,554 | 16.511 | 10 | 20 | MISS T_svc | 949,788 | 160 (48) | 0.030 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 826,111 | 16.522 | 10 | 20 | MISS T_svc | 950,000 | 160 (48) | 0.031 |
| BIND_RX | `acmp.bind_rx.if1` | 847,203 | 16.944 | 10 | 20 | MISS T_svc | 978,784 | 190 (77) | 0.032 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 357,559 | 7.151 | 10 | 20 | fits | 1,438,208 | 187 (32) | 0.026 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 291,724 | 5.834 | 10 | 20 | fits | 1,696,824 | 401 (47) | 0.025 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 673,423 | 13.468 | 10 | 20 | MISS T_svc | 1,272,599 | 188 (50) | 0.029 |
| PROBE_TX | `acmp.probe_tx.if1` | 270,818 | 5.416 | 10 | 20 | fits | 1,254,293 | 187 (48) | 0.028 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 445,103 | 8.902 | 10 | 20 | fits | 1,444,816 | 203 (48) | 0.026 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 252,598 | 5.052 | 10 | 20 | fits | 1,252,622 | 186 (48) | 0.028 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 87,654 | 1.753 | 10 | 20 | fits | 1,087,691 | 217 (48) | 0.032 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 109,942 | 2.199 | 10 | 24 | fits | 191,106 | 56 | 0.055 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 179,940 | 3.599 | 10 | 24 | fits | 261,435 | 134 | 0.044 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 156,713 | 3.134 | 10 | 24 | fits | 238,205 | 82 | 0.047 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 139,696 | 2.794 | 10 | 24 | fits | 221,188 | 86 | 0.041 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 140,058 | 2.801 | 10 | 24 | fits | 221,553 | 85 | 0.041 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 162,433 | 3.249 | 10 | 24 | fits | 243,928 | 92 | 0.046 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 217,064 | 4.341 | 10 | 24 | fits | 217,627 | 75 | 0.042 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 134,867 | 2.697 | 10 | 24 | fits | 216,362 | 70 | 0.042 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 133,408 | 2.668 | 10 | 24 | fits | 214,900 | 67 | 0.042 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 174,512 | 3.490 | 10 | 24 | fits | 256,004 | 162 | 0.036 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 128,431 | 2.569 | 10 | 24 | fits | 209,923 | 54 | 0.043 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 150,669 | 3.013 | 10 | 24 | fits | 232,161 | 61 | 0.048 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 141,620 | 2.832 | 10 | 24 | fits | 223,112 | 71 | 0.041 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 143,564 | 2.871 | 10 | 24 | fits | 225,056 | 77 | 0.041 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 141,827 | 2.837 | 10 | 24 | fits | 223,319 | 73 | 0.041 |
| get_configuration | `aecp.get_configuration.if0` | 144,724 | 2.894 | 10 | 24 | fits | 226,176 | 56 | 0.049 |
| entity_available | `aecp.entity_available.if0` | 124,799 | 2.496 | 10 | 24 | fits | 206,205 | 53 | 0.043 |
| get_name | `aecp.get_name.if0` | 151,969 | 3.039 | 10 | 24 | fits | 233,424 | 73 | 0.048 |
| get_counters | `aecp.get_counters.if0` | 138,607 | 2.772 | 10 | 24 | fits | 220,102 | 87 | 0.044 |
| get_avb_info | `aecp.get_avb_info.if0` | 229,421 | 4.588 | 10 | 24 | fits | 212,909 | 50 | 0.042 |
| unknown_command | `aecp.unknown_command.if0` | 122,762 | 2.455 | 10 | 24 | fits | 204,168 | 49 | 0.043 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 110,181 | 2.204 | 10 | 24 | fits | 191,636 | 60 | 0.055 |
| set_name | `aecp.set_name.if0` | 216,852 | 4.337 | 10 | 24 | fits | 367,132 | 156 | 0.037 |
| lock_entity | `aecp.lock_entity.if0` | 167,800 | 3.356 | 10 | 24 | fits | 260,593 | 97 | 0.047 |
| unlock_entity | `aecp.unlock_entity.if0` | 167,805 | 3.356 | 10 | 24 | fits | 260,527 | 97 | 0.047 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 88,022 | 1.760 | 10 | 24 | fits | 169,447 | 47 | 0.050 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 179,475 | 3.590 | 10 | 24 | fits | 260,989 | 132 | 0.044 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 134,846 | 2.697 | 10 | 24 | fits | 216,360 | 73 | 0.042 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 167,519 | 3.350 | 10 | 24 | fits | 221,324 | 85 | 0.041 |
| get_configuration | `aecp.get_configuration.if1` | 144,449 | 2.889 | 10 | 24 | fits | 226,021 | 54 | 0.049 |
| entity_available | `aecp.entity_available.if1` | 146,342 | 2.927 | 10 | 24 | fits | 227,914 | 58 | 0.048 |
| get_name | `aecp.get_name.if1` | 152,415 | 3.048 | 10 | 24 | fits | 233,987 | 71 | 0.048 |
| get_counters | `aecp.get_counters.if1` | 138,407 | 2.768 | 10 | 24 | fits | 220,019 | 85 | 0.044 |
| get_avb_info | `aecp.get_avb_info.if1` | 130,917 | 2.618 | 10 | 24 | fits | 212,489 | 47 | 0.042 |
| unknown_command | `aecp.unknown_command.if1` | 144,215 | 2.884 | 10 | 24 | fits | 225,787 | 54 | 0.048 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 88,883 | 1.778 | 10 | 24 | fits | 170,406 | 52 | 0.050 |
| set_name | `aecp.set_name.if1` | 197,957 | 3.959 | 10 | 24 | fits | 332,267 | 149 | 0.036 |
| lock_entity | `aecp.lock_entity.if1` | 146,235 | 2.925 | 10 | 24 | fits | 246,819 | 109 | 0.043 |
| unlock_entity | `aecp.unlock_entity.if1` | 146,222 | 2.924 | 10 | 24 | fits | 246,491 | 109 | 0.043 |

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
- `backlog-owed`: wait tx TIMEOUT
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
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
