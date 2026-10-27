### 8x8

50 of 129 paths and 83 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 8.347 (19.548) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 10.399 (30.968) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 8.889 (28.855) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 13.700 (34.018) | MISS T_svc | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 27.089 (69.192) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 29.542 (69.192) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 34.980 (69.436) | MISS ceiling | 2 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 37.325 (69.436) | MISS ceiling | 3 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 10.231 (29.875) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 19.546 (50.753) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 9.348 (29.352) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 14.279 (33.931) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 9.101 (29.136) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 15.926 (33.713) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 11.269 (29.367) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 22.247 (37.776) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 19.874 (32.492) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 12.239 (33.358) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 4.400 (29.586) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 6.532 (31.327) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 7.141 (59.618) | fits | 2 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 8.577 (63.840) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 11.347 (61.380) | MISS T_svc | 1 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 10.097 (61.380) | MISS T_svc | 2 events | 1 | 1 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 5.242 (27.274) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 5.652 (27.274) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 5.992 (35.210) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 3.162 (32.324) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 4.561 (30.296) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 13.002 (59.882) | MISS T_svc | 2 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 8.990 (29.551) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 22.552 (83.493) | MISS ceiling | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 5.170 (12.006) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 5.333 (12.005) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 3.408 (11.196) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 3.603 (11.196) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 15.986 (37.365) | MISS T_svc | 0 events | 1 | 1 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 23.253 (37.365) | MISS T_svc | 0 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.912 (23.901) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 3.452 (23.901) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.615 (5.452) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 3.129 (6.417) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.967 (7.035) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 4.033 (11.924) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 4.719 (12.768) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 4.475 (7.842) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 7.415 (10.882) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 4.686 (12.593) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 5.898 (9.367) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 5.913 (12.479) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 5.259 (13.223) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 6.011 (9.469) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 6.352 (9.861) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 6.191 (12.796) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 8.063 (14.877) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 7.234 (14.059) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 3.478 (9.883) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 3.365 (11.260) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 5.578 (8.832) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 5.238 (8.523) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 6.219 (9.641) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 6.143 (9.557) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 6.044 (9.550) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 4.804 (11.316) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 6.997 (13.613) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 5.894 (9.417) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 4.741 (12.711) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 8.850 (17.031) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 4.845 (11.317) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 8.554 (28.729) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 4.992 (11.505) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 6.349 (12.971) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 4.928 (12.929) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 6.160 (9.666) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 4.843 (12.851) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 8.070 (14.730) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 4.874 (11.500) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 7.313 (12.479) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 5.553 (10.367) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 7.625 (14.245) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 5.559 (9.058) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 5.115 (13.060) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 6.850 (13.209) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 11.510 (18.023) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 9.864 (19.381) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 10.402 (18.383) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 9.731 (17.875) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 12.851 (19.492) | MISS T_svc | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 11.304 (17.813) | MISS T_svc | 0 aecp | 2 | 1 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 13.786 (22.960) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 15.572 (22.936) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 11.925 (17.561) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 12.619 (19.265) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 11.281 (17.802) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 121.943 (135.637) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 80.248 (109.599) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 110.741 (144.078) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 30.763 (58.341) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 220.909 (231.711) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind1.if0` (backlog-owed) | at least 860.001 | NEVER ANSWERED | 9 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 4.608 (13.139) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.568 (11.518) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 3.335 (7.203) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 2.791 (9.503) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 3.253 (19.272) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 1.983 (12.969) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 4.465 (13.139) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.425 (11.518) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 4.934 (12.875) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 1.675 (6.812) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 29.026 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 169.154 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 29.068 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 129.198 | MISS T_svc | 6 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 96.869 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 29.062 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp.service.aecp.last.if1` (backlog-adp) | 466.095 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 29.051 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 100.150 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 650.727 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 650.707 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 13.650 (20.162) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 15.731 (23.564) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 11.466 (13.664) | MISS T_svc | 0 srp | 1 | 1 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 9.754 (13.116) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 5.415 (10.212) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 11.449 (14.884) | MISS T_svc | 0 srp | 1 | 1 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 14.577 (19.272) | MISS T_svc | 0 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 12.398 (14.180) | MISS T_svc | 0 events | 1 | 1 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 621.996 | 54 | 1,415,819 (28.316) | yes | - |
| backlog-adp | 580.300 | 20 | 2,088,796 (41.776) | no | {'srp': 32} |
| backlog-adp-refill | 650.743 | 23 | 1,946,182 (38.924) | no | {'srp': 32} |
| backlog-owed | 860.053 | 72 | 1,549,529 (30.991) | yes | - |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 299,592 | 5.992 | 10 | 20 | fits | 1,760,509 | 96 (14) | 0.005 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 158,116 | 3.162 | 10 | 20 | fits | 1,616,196 | 71 (14) | 0.007 |
| LINK_UP | `adp.link_up.if0` | 45,620 | 0.912 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| LINK_UP | `adp.link_up.if1` | 172,616 | 3.452 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 98,373 | 1.967 | 10 | 200 | fits | 351,728 | 53 (39) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,655 | 4.033 | 10 | 200 | fits | 244,448 | 47 (39) | 0.011 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 30,755 | 0.615 | 10 | 200 | fits | 272,589 | 25 (11) | 0.014 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 156,443 | 3.129 | 10 | 200 | fits | 26,804 | 9 (11) | 0.066 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 162,667 | 3.253 | 10 | 50 | fits | 813,370 | 160 | 0.012 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 246,697 | 4.934 | 10 | 50 | fits | 334,165 | 44 | 0.015 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 243,319 | 4.866 | 10 | 50 | fits | 329,738 | 44 | 0.014 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 223,268 | 4.465 | 10 | 50 | fits | 350,619 | 71 | 0.013 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 230,388 | 4.608 | 10 | 50 | fits | 350,619 | 71 | 0.013 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 166,742 | 3.335 | 10 | 50 | fits | 360,134 | 54 | 0.016 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 99,160 | 1.983 | 10 | 50 | fits | 648,453 | 154 | 0.008 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 83,775 | 1.675 | 10 | 50 | fits | 340,611 | 44 | 0.015 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 68,002 | 1.360 | 10 | 50 | fits | 313,512 | 44 | 0.013 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 121,265 | 2.425 | 10 | 50 | fits | 333,526 | 65 | 0.014 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 128,385 | 2.568 | 10 | 50 | fits | 333,526 | 65 | 0.014 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 139,567 | 2.791 | 10 | 50 | fits | 274,462 | 47 | 0.012 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 567,365 | 11.347 | 10 | 20 | MISS T_svc | 1,472,815 | 116 (35) | 0.008 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 504,856 | 10.097 | 10 | 20 | MISS T_svc | 1,472,815 | 116 (35) | 0.008 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 262,117 | 5.242 | 10 | 20 | fits | 1,363,684 | 70 (14) | 0.007 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 282,617 | 5.652 | 10 | 20 | fits | 1,363,684 | 70 (14) | 0.007 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 228,027 | 4.561 | 10 | 20 | fits | 1,514,817 | 71 (14) | 0.006 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 650,078 | 13.002 | 10 | 20 | MISS T_svc | 1,479,307 | 93 (14) | 0.008 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 220,003 | 4.400 | 10 | 20 | fits | 1,479,307 | 93 (35) | 0.008 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 326,617 | 6.532 | 10 | 20 | fits | 1,566,334 | 93 (35) | 0.007 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 728,827 | 14.577 | 10 | 18 | MISS T_svc | 813,370 | 160 | 0.012 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 619,889 | 12.398 | 10 | 18 | MISS T_svc | 709,009 | 160 | 0.009 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 573,314 | 11.466 | 10 | 18 | MISS T_svc | 440,461 | 29 | 0.018 |
| malformed MRPDU discard | `srp.malformed.if0` | 270,765 | 5.415 | 10 | 18 | fits | 260,593 | 30 | 0.011 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 682,523 | 13.650 | 210 | 218 | fits | 758,115 | 143 | 0.006 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 487,704 | 9.754 | 10 | 18 | fits | 420,182 | 36 | 0.013 |
| malformed MRPDU discard | `srp.malformed.if1` | 572,447 | 11.449 | 10 | 18 | MISS T_svc | 338,050 | 36 | 0.013 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 786,553 | 15.731 | 210 | 218 | fits | 559,230 | 39 | 0.011 |
| an event behind 15 others | `backlog.event.if0` | 1,538,158 | 30.763 | 10 | 200 | MISS T_svc | 1,299,203 | 375 | 0.009 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 6,097,140 | 121.943 | 10 | 20 | MISS ceiling | 890,328 | 223 | 0.012 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,453,414 | 29.068 | 10 | 200 | MISS T_svc | 1,415,819 | 392 | 0.011 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 4,843,461 | 96.869 | 10 | 200 | MISS T_svc | 947,985 | 291 | 0.011 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,451,285 | 29.026 | 10 | 20 | MISS ceiling | 1,415,819 | 392 | 0.011 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 6,617,474 | 132.349 | 10 | 20 | MISS ceiling | 890,328 | 223 | 0.012 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,453,077 | 29.062 | 10 | 24 | MISS ceiling | 1,415,819 | 392 | 0.011 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 12,977,657 | 259.553 | 10 | 24 | MISS ceiling | 684,520 | 150 | 0.014 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,452,557 | 29.051 | 10 | 50 | MISS T_svc | 1,415,819 | 392 | 0.011 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 4,842,713 | 96.854 | 10 | 50 | MISS ceiling | 947,985 | 291 | 0.011 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 7,509,888 | 150.198 | 10 | 18 | MISS ceiling | 890,956 | 175 | 0.017 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 19,045,274 | 380.905 | 10 | 18 | MISS ceiling | 385,221 | 36 | 0.014 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 4,012,377 | 80.248 | 10 | 20 | MISS ceiling | 1,557,072 | 357 | 0.011 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 1,253,752 | 25.075 | 10 | 200 | MISS T_svc | 1,727,751 | 397 | 0.009 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 5,005,666 | 100.113 | 10 | 200 | MISS T_svc | 1,557,072 | 357 | 0.011 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 1,254,208 | 25.084 | 10 | 20 | MISS ceiling | 1,727,751 | 397 | 0.009 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 8,320,036 | 166.401 | 10 | 20 | MISS ceiling | 1,672,881 | 269 | 0.009 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 1,256,000 | 25.120 | 10 | 24 | MISS ceiling | 1,727,751 | 397 | 0.009 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 23,304,753 | 466.095 | 10 | 24 | MISS ceiling | 1,433,590 | 185 | 0.007 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 1,255,480 | 25.110 | 10 | 50 | MISS T_svc | 1,727,751 | 397 | 0.009 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 5,007,504 | 100.150 | 10 | 50 | MISS ceiling | 1,557,072 | 357 | 0.011 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 29,014,182 | 580.284 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 29,013,175 | 580.263 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 5,537,070 | 110.741 | 10 | 20 | MISS ceiling | 1,873,799 | 304 | 0.008 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 1,253,752 | 25.075 | 10 | 200 | MISS T_svc | 1,727,751 | 397 | 0.009 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 6,459,890 | 129.198 | 10 | 200 | MISS T_svc | 1,873,799 | 304 | 0.008 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 1,254,208 | 25.084 | 10 | 20 | MISS ceiling | 1,727,751 | 397 | 0.009 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 8,457,696 | 169.154 | 10 | 20 | MISS ceiling | 1,873,799 | 304 | 0.008 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 1,256,000 | 25.120 | 10 | 24 | MISS ceiling | 1,727,751 | 397 | 0.009 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 23,300,482 | 466.010 | 10 | 24 | MISS ceiling | 1,433,860 | 185 | 0.007 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 1,255,480 | 25.110 | 10 | 50 | MISS T_svc | 1,727,751 | 397 | 0.009 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 4,897,475 | 97.950 | 10 | 50 | MISS ceiling | 1,447,043 | 350 | 0.011 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 32,536,333 | 650.727 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 32,535,326 | 650.707 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 11,045,438 | 220.909 | 10 | 20 | MISS ceiling | 972,227 | 197 | 0.013 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 12,017,621 | 240.352 | 10 | 20 | MISS ceiling | 972,221 | 197 | 0.013 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 43,000,073 | 860.001 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 12,989,759 | 259.795 | 10 | 20 | MISS ceiling | 972,213 | 197 | 0.013 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 42,999,998 | 860.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 1,038,297 | 20.766 | 10 | 200 | MISS T_svc | 1,020,577 | 344 | 0.011 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 3,969,355 | 79.387 | 10 | 200 | MISS T_svc | 1,049,321 | 288 | 0.010 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 1,036,168 | 20.723 | 10 | 20 | MISS ceiling | 1,020,577 | 344 | 0.011 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 5,867,001 | 117.340 | 10 | 20 | MISS ceiling | 952,051 | 201 | 0.011 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 1,037,960 | 20.759 | 10 | 24 | MISS T_svc | 1,020,577 | 344 | 0.011 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 15,309,671 | 306.193 | 10 | 24 | MISS ceiling | 549,790 | 130 | 0.011 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 1,037,440 | 20.749 | 10 | 50 | MISS T_svc | 1,020,577 | 344 | 0.011 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 3,968,607 | 79.372 | 10 | 50 | MISS ceiling | 1,049,321 | 288 | 0.010 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 6,910,510 | 138.210 | 10 | 18 | MISS ceiling | 1,042,051 | 178 | 0.018 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 20,019,231 | 400.385 | 10 | 18 | MISS ceiling | 389,532 | 36 | 0.013 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 1,749,004 | 34.980 | 10 | 20 | MISS ceiling | 1,558,822 | 177 (29) | 0.009 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 1,866,232 | 37.325 | 10 | 20 | MISS ceiling | 1,558,822 | 177 (29) | 0.009 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,354,440 | 27.089 | 10 | 20 | MISS ceiling | 1,863,431 | 132 (35) | 0.005 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,477,103 | 29.542 | 10 | 20 | MISS ceiling | 1,863,431 | 132 (35) | 0.005 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 357,049 | 7.141 | 10 | 20 | fits | 1,125,108 | 56 (12) | 0.008 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 428,851 | 8.577 | 10 | 20 | fits | 1,589,387 | 93 (12) | 0.007 |
| LINK_UP | `adp.link_up.if0` | 45,620 | 0.912 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| LINK_UP | `adp.link_up.if1` | 172,616 | 3.452 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 98,373 | 1.967 | 10 | 200 | fits | 351,728 | 53 (39) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,655 | 4.033 | 10 | 200 | fits | 244,448 | 47 (39) | 0.011 |
| LINK_DOWN | `adp.link_down.if0` | 799,322 | 15.986 | 10 | 200 | MISS T_svc | 1,094,293 | 70 (9) | 0.008 |
| LINK_DOWN | `adp.link_down.if1` | 1,162,647 | 23.253 | 10 | 200 | MISS T_svc | 1,094,293 | 70 (9) | 0.008 |
| LINK_UP | `adp.link_up.if0` | 45,620 | 0.912 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| LINK_UP | `adp.link_up.if1` | 172,616 | 3.452 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 98,373 | 1.967 | 10 | 200 | fits | 351,728 | 53 (39) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,655 | 4.033 | 10 | 200 | fits | 244,448 | 47 (39) | 0.011 |
| GM_CHANGE | `adp.gm_change.if0` | 170,375 | 3.408 | 10 | 200 | fits | 254,641 | 34 (11) | 0.012 |
| GM_CHANGE | `adp.gm_change.if1` | 180,152 | 3.603 | 10 | 200 | fits | 254,641 | 34 (11) | 0.012 |
| LINK_UP | `adp.link_up.if0` | 45,620 | 0.912 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| LINK_UP | `adp.link_up.if1` | 172,616 | 3.452 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 98,373 | 1.967 | 10 | 200 | fits | 351,728 | 53 (39) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,655 | 4.033 | 10 | 200 | fits | 244,448 | 47 (39) | 0.011 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 258,494 | 5.170 | 10 | 200 | fits | 294,661 | 73 (31) | 0.013 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 266,663 | 5.333 | 10 | 200 | fits | 294,661 | 73 (31) | 0.013 |
| LINK_UP | `adp.link_up.if0` | 45,620 | 0.912 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| LINK_UP | `adp.link_up.if1` | 172,616 | 3.452 | 10 | 200 | fits | 1,044,820 | 304 (11) | 0.007 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 98,373 | 1.967 | 10 | 200 | fits | 351,728 | 53 (39) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 201,655 | 4.033 | 10 | 200 | fits | 244,448 | 47 (39) | 0.011 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 258,494 | 5.170 | 10 | 200 | fits | 286,715 | 45 (31) | 0.014 |
| set_name | `aecp_fanout.set_name.if0` | 689,299 | 13.786 | 10 | 24 | MISS T_svc | 904,883 | 1130 | 0.005 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 520,113 | 10.402 | 10 | 24 | MISS T_svc | 673,823 | 589 | 0.006 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 642,543 | 12.851 | 10 | 24 | MISS T_svc | 701,783 | 563 | 0.007 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 590,023 | 11.800 | 10 | 24 | MISS T_svc | 614,378 | 557 | 0.005 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 596,260 | 11.925 | 10 | 24 | MISS T_svc | 635,065 | 589 | 0.006 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 575,479 | 11.510 | 10 | 24 | MISS T_svc | 629,622 | 655 | 0.005 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 630,971 | 12.619 | 10 | 24 | MISS T_svc | 705,110 | 662 | 0.006 |
| set_name | `aecp_fanout.set_name.if1` | 778,622 | 15.572 | 10 | 24 | MISS T_svc | 923,021 | 1137 | 0.005 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 486,560 | 9.731 | 10 | 24 | fits | 648,518 | 589 | 0.006 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 565,192 | 11.304 | 10 | 24 | MISS T_svc | 617,725 | 556 | 0.005 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 492,000 | 9.840 | 10 | 24 | fits | 615,142 | 556 | 0.005 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 493,182 | 9.864 | 10 | 24 | fits | 626,794 | 655 | 0.005 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 564,037 | 11.281 | 10 | 24 | MISS T_svc | 630,901 | 655 | 0.005 |
| BIND_RX | `acmp.bind_rx.if0` | 417,368 | 8.347 | 10 | 20 | fits | 712,728 | 90 (77) | 0.022 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 993,707 | 19.874 | 10 | 20 | MISS T_svc | 1,624,588 | 102 (32) | 0.009 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 511,564 | 10.231 | 10 | 20 | MISS T_svc | 1,493,739 | 114 (47) | 0.009 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 449,519 | 8.990 | 10 | 20 | fits | 1,477,554 | 176 (50) | 0.011 |
| PROBE_TX | `acmp.probe_tx.if0` | 563,463 | 11.269 | 10 | 20 | MISS T_svc | 1,468,348 | 116 (48) | 0.009 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 455,074 | 9.101 | 10 | 20 | fits | 1,456,793 | 115 (48) | 0.009 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 444,472 | 8.889 | 10 | 20 | fits | 1,442,737 | 115 (48) | 0.009 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 467,408 | 9.348 | 10 | 20 | fits | 1,467,607 | 115 (48) | 0.009 |
| BIND_RX | `acmp.bind_rx.if1` | 519,947 | 10.399 | 10 | 20 | MISS T_svc | 1,548,402 | 145 (77) | 0.010 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 611,933 | 12.239 | 10 | 20 | MISS T_svc | 1,667,908 | 97 (32) | 0.007 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 977,319 | 19.546 | 10 | 20 | MISS T_svc | 2,537,665 | 331 (47) | 0.006 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 1,127,623 | 22.552 | 10 | 20 | MISS ceiling | 1,636,976 | 112 (50) | 0.010 |
| PROBE_TX | `acmp.probe_tx.if1` | 1,112,340 | 22.247 | 10 | 20 | MISS ceiling | 1,888,811 | 117 (48) | 0.006 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 796,315 | 15.926 | 10 | 20 | MISS T_svc | 1,685,657 | 113 (48) | 0.007 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 685,012 | 13.700 | 10 | 20 | MISS T_svc | 1,700,878 | 113 (48) | 0.008 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 713,952 | 14.279 | 10 | 20 | MISS T_svc | 1,696,550 | 137 (48) | 0.007 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 403,512 | 8.070 | 10 | 24 | fits | 471,828 | 54 | 0.017 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 278,879 | 5.578 | 10 | 24 | fits | 441,601 | 125 | 0.010 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 310,947 | 6.219 | 10 | 24 | fits | 482,061 | 80 | 0.012 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 442,519 | 8.850 | 10 | 24 | fits | 482,373 | 91 | 0.012 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 246,395 | 4.928 | 10 | 24 | fits | 404,557 | 83 | 0.009 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 307,986 | 6.160 | 10 | 24 | fits | 483,277 | 90 | 0.012 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 242,164 | 4.843 | 10 | 24 | fits | 400,475 | 72 | 0.010 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 302,218 | 6.044 | 10 | 24 | fits | 477,494 | 75 | 0.012 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 240,190 | 4.804 | 10 | 24 | fits | 398,069 | 65 | 0.010 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 349,859 | 6.997 | 10 | 24 | fits | 438,576 | 161 | 0.008 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 294,701 | 5.894 | 10 | 24 | fits | 470,838 | 59 | 0.012 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 237,043 | 4.741 | 10 | 24 | fits | 393,979 | 53 | 0.010 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 427,702 | 8.554 | 10 | 24 | fits | 566,303 | 82 | 0.013 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 249,605 | 4.992 | 10 | 24 | fits | 408,132 | 75 | 0.009 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 317,431 | 6.349 | 10 | 24 | fits | 406,689 | 72 | 0.009 |
| get_configuration | `aecp.get_configuration.if0` | 294,879 | 5.898 | 10 | 24 | fits | 468,334 | 54 | 0.013 |
| entity_available | `aecp.entity_available.if0` | 235,937 | 4.719 | 10 | 24 | fits | 396,555 | 51 | 0.011 |
| get_name | `aecp.get_name.if0` | 317,599 | 6.352 | 10 | 24 | fits | 493,030 | 71 | 0.013 |
| get_counters | `aecp.get_counters.if0` | 262,945 | 5.259 | 10 | 24 | fits | 419,179 | 80 | 0.011 |
| get_avb_info | `aecp.get_avb_info.if0` | 370,730 | 7.415 | 10 | 24 | fits | 544,084 | 82 | 0.013 |
| unknown_command | `aecp.unknown_command.if0` | 381,257 | 7.625 | 10 | 24 | fits | 457,083 | 54 | 0.012 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 173,879 | 3.478 | 10 | 24 | fits | 329,246 | 51 | 0.011 |
| set_name | `aecp.set_name.if0` | 365,648 | 7.313 | 10 | 24 | fits | 623,927 | 114 | 0.010 |
| lock_entity | `aecp.lock_entity.if0` | 403,161 | 8.063 | 10 | 24 | fits | 487,001 | 73 | 0.012 |
| unlock_entity | `aecp.unlock_entity.if0` | 255,744 | 5.115 | 10 | 24 | fits | 410,794 | 66 | 0.010 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 243,714 | 4.874 | 10 | 24 | fits | 402,322 | 52 | 0.013 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 261,915 | 5.238 | 10 | 24 | fits | 426,159 | 123 | 0.009 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 307,157 | 6.143 | 10 | 24 | fits | 477,848 | 78 | 0.012 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 242,228 | 4.845 | 10 | 24 | fits | 399,710 | 82 | 0.009 |
| get_configuration | `aecp.get_configuration.if1` | 295,642 | 5.913 | 10 | 24 | fits | 381,735 | 46 | 0.010 |
| entity_available | `aecp.entity_available.if1` | 223,775 | 4.475 | 10 | 24 | fits | 392,119 | 49 | 0.010 |
| get_name | `aecp.get_name.if1` | 309,567 | 6.191 | 10 | 24 | fits | 397,583 | 63 | 0.010 |
| get_counters | `aecp.get_counters.if1` | 300,570 | 6.011 | 10 | 24 | fits | 473,470 | 85 | 0.012 |
| get_avb_info | `aecp.get_avb_info.if1` | 234,313 | 4.686 | 10 | 24 | fits | 387,411 | 46 | 0.009 |
| unknown_command | `aecp.unknown_command.if1` | 277,974 | 5.559 | 10 | 24 | fits | 452,920 | 52 | 0.012 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 168,239 | 3.365 | 10 | 24 | fits | 320,737 | 50 | 0.010 |
| set_name | `aecp.set_name.if1` | 277,674 | 5.553 | 10 | 24 | fits | 518,359 | 140 | 0.007 |
| lock_entity | `aecp.lock_entity.if1` | 361,694 | 7.234 | 10 | 24 | fits | 418,013 | 85 | 0.010 |
| unlock_entity | `aecp.unlock_entity.if1` | 342,486 | 6.850 | 10 | 24 | fits | 418,050 | 86 | 0.010 |

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
- `acmp-cmd`: wait quiet TIMEOUT
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
