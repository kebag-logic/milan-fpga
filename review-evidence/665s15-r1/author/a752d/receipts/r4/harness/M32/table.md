### 32x32

56 of 129 paths and 90 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 5.858 (15.862) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 11.341 (36.320) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 6.546 (31.548) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 19.428 (33.910) | MISS T_svc | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 2.440 (43.217) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 6.258 (43.217) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 66.244 (118.785) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 74.286 (118.785) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 48.213 (100.614) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 25.322 (39.773) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 6.563 (31.552) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 25.214 (39.698) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 3.994 (31.574) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 24.325 (52.186) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 6.909 (31.586) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 27.357 (93.663) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 16.968 (31.415) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 17.552 (33.720) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.490 (33.349) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 3.998 (60.901) | fits | 2 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 1.622 (33.001) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 3.578 (33.430) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 23.797 (105.445) | MISS ceiling | 6 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 33.006 (132.931) | MISS ceiling | 8 events | 1 | 1 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 8.067 (61.686) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 5.641 (26.087) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 11.572 (58.675) | MISS T_svc | 0 events | 1 | 1 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 8.435 (69.002) | fits | 3 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 4.881 (32.946) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 6.797 (65.881) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 6.952 (31.932) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 16.321 (30.872) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 1.913 (12.775) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 2.091 (12.774) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 1.788 (12.590) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 1.875 (12.590) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 17.677 (66.062) | MISS T_svc | 1 events | 1 | 1 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 35.699 (66.062) | MISS T_svc | 1 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.315 (60.920) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 1.770 (60.920) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.456 (6.946) | fits | 1 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.547 (0.705) | fits | 1 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 2.401 (12.585) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 1.336 (12.585) | fits | 2 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 8.923 (18.595) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 8.928 (18.600) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 9.483 (19.154) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 8.947 (14.496) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 8.898 (18.565) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 8.894 (18.567) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 9.256 (18.930) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 9.260 (14.815) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 9.046 (18.717) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 9.050 (18.722) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 6.610 (16.509) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 7.072 (17.123) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 7.671 (13.230) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 36.718 (70.348) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 8.856 (18.481) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 9.606 (14.609) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 42.501 (71.168) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 9.135 (14.150) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i33.c0.if0` (aecp) | 8.501 (14.151) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 8.466 (18.090) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 9.288 (18.912) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i31.c0.if0` (aecp) | 8.401 (18.026) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i31.c0.if0` (aecp) | 8.442 (14.628) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 8.513 (14.152) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 9.226 (18.899) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i287.c0.if0` (aecp) | 7.024 (14.749) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 38.236 (71.869) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (144 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 9.811 (14.824) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i32.c0.if0` (aecp) | 8.555 (18.180) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i32.c0.if0` (aecp) | 5.327 (14.231) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 8.481 (14.131) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 7.615 (13.116) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 2.967 (7.279) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 10.415 (17.000) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 10.446 (21.908) | MISS T_svc | 0 aecp | 1 | 1 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 8.884 (14.444) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 8.884 (13.899) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 28.090 (72.579) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 5.618 (15.611) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 10.169 (20.186) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 14.862 (20.725) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 10.913 (21.881) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 10.923 (21.891) | MISS T_svc | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 42.779 (77.341) | MISS ceiling | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 14.363 (20.218) | MISS T_svc | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 17.594 (24.159) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 17.043 (24.166) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 13.957 (21.076) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 14.871 (24.583) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 14.353 (20.202) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 174.034 (188.022) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 86.207 (136.910) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 122.550 (157.502) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 41.864 (79.724) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 211.155 (226.507) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind1.if0` (backlog-owed) | at least 3260.001 | NEVER ANSWERED | 9 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 2.931 (13.445) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 5.005 (15.880) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 6.285 (16.929) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.283 (7.215) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 1.669 (33.375) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 1.586 (38.783) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 2.782 (13.445) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 4.856 (15.880) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 4.870 (12.489) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 4.156 (13.151) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 41.310 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 186.465 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 41.352 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 144.809 | MISS T_svc | 6 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 150.178 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 41.346 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 489.054 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 41.335 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 150.163 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 2162.535 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 2162.515 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 51.419 (78.676) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 46.095 (50.079) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 16.335 (19.710) | MISS T_svc | 0 srp | 1 | 1 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 10.161 (15.815) | MISS T_svc | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 12.155 (13.962) | MISS T_svc | 0 srp | 1 | 1 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 7.168 (8.024) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 32.314 (33.375) | MISS ceiling | 0 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 42.432 (47.890) | MISS ceiling | 0 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 2174.087 | 204 | 2,542,696 (50.854) | yes | - |
| backlog-adp | 2086.260 | 70 | 4,073,412 (81.468) | no | {'srp': 32} |
| backlog-adp-refill | 2162.552 | 73 | 4,073,412 (81.468) | no | {'srp': 32} |
| backlog-owed | 3260.053 | 296 | 3,203,755 (64.075) | yes | - |

Composed maximum over the 4 backlog windows: at least 4,073,412 CPU cycles (81.468 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 3,203,755 (64.075 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 578,595 | 11.572 | 10 | 20 | MISS T_svc | 1,150,690 | 136 (14) | 0.025 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 421,752 | 8.435 | 10 | 20 | fits | 1,663,912 | 127 (14) | 0.018 |
| LINK_UP | `adp.link_up.if0` | 15,751 | 0.315 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| LINK_UP | `adp.link_up.if1` | 88,483 | 1.770 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 120,039 | 2.401 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 66,820 | 1.336 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 72,823 | 1.456 | 10 | 200 | fits | 35,274 | 24 (11) | 0.050 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 27,371 | 0.547 | 10 | 200 | fits | 35,274 | 24 (11) | 0.050 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 83,445 | 1.669 | 10 | 50 | fits | 1,668,729 | 382 | 0.006 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 137,261 | 2.745 | 10 | 50 | fits | 358,375 | 44 | 0.029 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 243,507 | 4.870 | 10 | 50 | fits | 332,018 | 38 | 0.029 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 139,077 | 2.782 | 10 | 50 | fits | 379,807 | 71 | 0.030 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 146,534 | 2.931 | 10 | 50 | fits | 379,807 | 71 | 0.030 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 314,249 | 6.285 | 10 | 50 | fits | 357,614 | 54 | 0.027 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 79,293 | 1.586 | 10 | 50 | fits | 1,645,459 | 376 | 0.006 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 168,026 | 3.361 | 10 | 50 | fits | 335,046 | 38 | 0.029 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 207,778 | 4.156 | 10 | 50 | fits | 361,931 | 44 | 0.029 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 242,793 | 4.856 | 10 | 50 | fits | 382,568 | 71 | 0.029 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 250,250 | 5.005 | 10 | 50 | fits | 382,568 | 71 | 0.029 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 64,172 | 1.283 | 10 | 50 | fits | 360,728 | 54 | 0.027 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 1,189,870 | 23.797 | 10 | 20 | MISS ceiling | 1,085,582 | 115 (35) | 0.022 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 1,650,283 | 33.006 | 10 | 20 | MISS ceiling | 1,374,324 | 132 (35) | 0.019 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 403,338 | 8.067 | 10 | 20 | fits | 1,304,342 | 139 (14) | 0.026 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 282,028 | 5.641 | 10 | 20 | fits | 1,304,342 | 139 (14) | 0.026 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 244,040 | 4.881 | 10 | 20 | fits | 1,647,303 | 127 (14) | 0.017 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 339,839 | 6.797 | 10 | 20 | fits | 1,646,763 | 126 (14) | 0.017 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 74,494 | 1.490 | 10 | 20 | fits | 1,667,447 | 149 (35) | 0.018 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 199,903 | 3.998 | 10 | 20 | fits | 1,377,621 | 132 (35) | 0.019 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 1,615,725 | 32.314 | 10 | 18 | MISS ceiling | 1,668,729 | 382 | 0.006 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 2,121,608 | 42.432 | 10 | 18 | MISS ceiling | 2,394,490 | 352 | 0.016 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 816,727 | 16.335 | 10 | 18 | MISS T_svc | 418,814 | 36 | 0.033 |
| malformed MRPDU discard | `srp.malformed.if0` | 607,766 | 12.155 | 10 | 18 | MISS T_svc | 376,158 | 36 | 0.024 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 2,570,963 | 51.419 | 210 | 218 | fits | 2,262,722 | 382 | 0.012 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 508,029 | 10.161 | 10 | 18 | MISS T_svc | 443,225 | 36 | 0.032 |
| malformed MRPDU discard | `srp.malformed.if1` | 358,384 | 7.168 | 10 | 18 | fits | 401,189 | 36 | 0.022 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 2,304,728 | 46.095 | 210 | 218 | fits | 2,156,737 | 364 | 0.011 |
| an event behind 15 others | `backlog.event.if0` | 2,093,214 | 41.864 | 10 | 200 | MISS T_svc | 1,843,283 | 377 | 0.041 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 8,701,720 | 174.034 | 10 | 20 | MISS ceiling | 908,271 | 225 | 0.029 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 2,067,623 | 41.352 | 10 | 200 | MISS T_svc | 1,000,974 | 388 | 0.033 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 7,508,919 | 150.178 | 10 | 200 | MISS T_svc | 1,055,621 | 311 | 0.029 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 2,065,494 | 41.310 | 10 | 20 | MISS ceiling | 1,000,974 | 388 | 0.033 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 9,323,250 | 186.465 | 10 | 20 | MISS ceiling | 908,271 | 225 | 0.029 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 2,067,286 | 41.346 | 10 | 24 | MISS ceiling | 1,000,974 | 388 | 0.033 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 14,296,352 | 285.927 | 10 | 24 | MISS ceiling | 504,488 | 132 | 0.021 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 2,066,766 | 41.335 | 10 | 50 | MISS T_svc | 1,000,974 | 388 | 0.033 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 7,508,171 | 150.163 | 10 | 50 | MISS ceiling | 1,055,621 | 311 | 0.029 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 13,287,089 | 265.742 | 10 | 18 | MISS ceiling | 606,093 | 171 | 0.029 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 20,279,813 | 405.596 | 10 | 18 | MISS ceiling | 402,603 | 54 | 0.028 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 4,310,354 | 86.207 | 10 | 20 | MISS ceiling | 1,810,272 | 383 | 0.026 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 1,363,106 | 27.262 | 10 | 200 | MISS T_svc | 1,344,200 | 407 | 0.028 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 5,486,509 | 109.730 | 10 | 200 | MISS T_svc | 1,810,272 | 383 | 0.026 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 1,363,562 | 27.271 | 10 | 20 | MISS ceiling | 1,344,200 | 407 | 0.028 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 9,215,494 | 184.310 | 10 | 20 | MISS ceiling | 1,968,563 | 309 | 0.021 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 1,365,354 | 27.307 | 10 | 24 | MISS ceiling | 1,344,200 | 407 | 0.028 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 24,430,244 | 488.605 | 10 | 24 | MISS ceiling | 1,563,142 | 222 | 0.015 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 1,364,834 | 27.297 | 10 | 50 | MISS T_svc | 1,344,200 | 407 | 0.028 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 5,488,347 | 109.767 | 10 | 50 | MISS ceiling | 1,810,272 | 383 | 0.026 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 104,312,159 | 2086.243 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 104,311,152 | 2086.223 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 6,127,486 | 122.550 | 10 | 20 | MISS ceiling | 2,157,978 | 341 | 0.022 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 1,363,106 | 27.262 | 10 | 200 | MISS T_svc | 1,344,200 | 407 | 0.028 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 7,240,442 | 144.809 | 10 | 200 | MISS T_svc | 2,157,978 | 341 | 0.022 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 1,363,562 | 27.271 | 10 | 20 | MISS ceiling | 1,344,200 | 407 | 0.028 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 9,238,248 | 184.765 | 10 | 20 | MISS ceiling | 2,157,978 | 341 | 0.022 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 1,365,354 | 27.307 | 10 | 24 | MISS ceiling | 1,344,200 | 407 | 0.028 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 24,452,691 | 489.054 | 10 | 24 | MISS ceiling | 1,563,142 | 222 | 0.015 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 1,364,834 | 27.297 | 10 | 50 | MISS T_svc | 1,344,200 | 407 | 0.028 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 5,306,845 | 106.137 | 10 | 50 | MISS ceiling | 1,628,770 | 376 | 0.024 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 108,126,749 | 2162.535 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 108,125,742 | 2162.515 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 10,557,736 | 211.155 | 10 | 20 | MISS ceiling | 917,454 | 199 | 0.027 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 11,475,179 | 229.504 | 10 | 20 | MISS ceiling | 917,481 | 199 | 0.028 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 163,000,073 | 3260.001 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 12,392,814 | 247.856 | 10 | 20 | MISS ceiling | 917,710 | 199 | 0.028 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 162,999,998 | 3260.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 1,062,723 | 21.254 | 10 | 200 | MISS T_svc | 983,779 | 346 | 0.033 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 4,527,642 | 90.553 | 10 | 200 | MISS T_svc | 1,211,376 | 290 | 0.029 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 1,060,594 | 21.212 | 10 | 20 | MISS ceiling | 983,779 | 346 | 0.033 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,680,103 | 133.602 | 10 | 20 | MISS ceiling | 1,064,114 | 203 | 0.029 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 1,062,386 | 21.248 | 10 | 24 | MISS T_svc | 983,779 | 346 | 0.033 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 14,713,317 | 294.266 | 10 | 24 | MISS ceiling | 739,336 | 177 | 0.026 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 1,061,866 | 21.237 | 10 | 50 | MISS T_svc | 983,779 | 346 | 0.033 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 4,526,894 | 90.538 | 10 | 50 | MISS ceiling | 1,211,376 | 290 | 0.029 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 7,610,287 | 152.206 | 10 | 18 | MISS ceiling | 928,726 | 199 | 0.033 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 22,268,595 | 445.372 | 10 | 18 | MISS ceiling | 502,533 | 54 | 0.029 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 3,312,215 | 66.244 | 10 | 20 | MISS ceiling | 1,462,720 | 166 (29) | 0.026 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 3,714,292 | 74.286 | 10 | 20 | MISS ceiling | 1,462,720 | 166 (29) | 0.026 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 122,000 | 2.440 | 10 | 20 | fits | 2,160,871 | 202 (35) | 0.018 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 312,910 | 6.258 | 10 | 20 | fits | 2,160,871 | 202 (35) | 0.018 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 81,102 | 1.622 | 10 | 20 | fits | 1,650,036 | 126 (12) | 0.017 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 178,919 | 3.578 | 10 | 20 | fits | 1,671,503 | 149 (12) | 0.018 |
| LINK_UP | `adp.link_up.if0` | 15,751 | 0.315 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| LINK_UP | `adp.link_up.if1` | 88,483 | 1.770 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 120,039 | 2.401 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 66,820 | 1.336 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| LINK_DOWN | `adp.link_down.if0` | 883,865 | 17.677 | 10 | 200 | MISS T_svc | 2,240,558 | 81 (9) | 0.044 |
| LINK_DOWN | `adp.link_down.if1` | 1,784,945 | 35.699 | 10 | 200 | MISS T_svc | 2,240,558 | 81 (9) | 0.044 |
| LINK_UP | `adp.link_up.if0` | 15,751 | 0.315 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| LINK_UP | `adp.link_up.if1` | 88,483 | 1.770 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 120,039 | 2.401 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 66,820 | 1.336 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| GM_CHANGE | `adp.gm_change.if0` | 89,392 | 1.788 | 10 | 200 | fits | 303,144 | 34 (11) | 0.026 |
| GM_CHANGE | `adp.gm_change.if1` | 93,736 | 1.875 | 10 | 200 | fits | 303,144 | 34 (11) | 0.026 |
| LINK_UP | `adp.link_up.if0` | 15,751 | 0.315 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| LINK_UP | `adp.link_up.if1` | 88,483 | 1.770 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 120,039 | 2.401 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 66,820 | 1.336 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 95,659 | 1.913 | 10 | 200 | fits | 312,442 | 73 (31) | 0.025 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 104,537 | 2.091 | 10 | 200 | fits | 312,442 | 73 (31) | 0.025 |
| LINK_UP | `adp.link_up.if0` | 15,751 | 0.315 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| LINK_UP | `adp.link_up.if1` | 88,483 | 1.770 | 10 | 200 | fits | 3,045,985 | 748 (11) | 0.005 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 120,039 | 2.401 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 66,820 | 1.336 | 10 | 200 | fits | 334,873 | 90 (39) | 0.029 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 95,659 | 1.913 | 10 | 200 | fits | 303,790 | 45 (31) | 0.024 |
| set_name | `aecp_fanout.set_name.if0` | 879,684 | 17.594 | 10 | 24 | MISS T_svc | 910,117 | 1172 | 0.024 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 545,674 | 10.913 | 10 | 24 | MISS T_svc | 812,491 | 640 | 0.028 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 509,794 | 10.196 | 10 | 24 | MISS T_svc | 740,080 | 587 | 0.029 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 2,138,938 | 42.779 | 10 | 24 | MISS ceiling | 872,874 | 617 | 0.028 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 697,856 | 13.957 | 10 | 24 | MISS T_svc | 755,954 | 631 | 0.029 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 508,465 | 10.169 | 10 | 24 | MISS T_svc | 711,465 | 679 | 0.029 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 743,548 | 14.871 | 10 | 24 | MISS T_svc | 738,397 | 686 | 0.029 |
| set_name | `aecp_fanout.set_name.if1` | 852,128 | 17.043 | 10 | 24 | MISS T_svc | 910,504 | 1172 | 0.024 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 546,135 | 10.923 | 10 | 24 | MISS T_svc | 813,168 | 640 | 0.028 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 509,468 | 10.189 | 10 | 24 | MISS T_svc | 740,092 | 587 | 0.029 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 718,139 | 14.363 | 10 | 24 | MISS T_svc | 713,084 | 580 | 0.029 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 743,101 | 14.862 | 10 | 24 | MISS T_svc | 738,437 | 686 | 0.029 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 717,638 | 14.353 | 10 | 24 | MISS T_svc | 712,226 | 680 | 0.029 |
| BIND_RX | `acmp.bind_rx.if0` | 292,907 | 5.858 | 10 | 20 | fits | 498,724 | 83 (77) | 0.032 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 848,425 | 16.968 | 10 | 20 | MISS T_svc | 1,570,752 | 134 (32) | 0.019 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 2,410,628 | 48.213 | 10 | 20 | MISS ceiling | 956,267 | 119 (47) | 0.025 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 347,595 | 6.952 | 10 | 20 | fits | 1,596,599 | 152 (50) | 0.019 |
| PROBE_TX | `acmp.probe_tx.if0` | 345,437 | 6.909 | 10 | 20 | fits | 1,579,279 | 151 (48) | 0.019 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 199,719 | 3.994 | 10 | 20 | fits | 1,578,723 | 150 (48) | 0.019 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 327,288 | 6.546 | 10 | 20 | fits | 1,577,413 | 150 (48) | 0.019 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 328,150 | 6.563 | 10 | 20 | fits | 1,577,587 | 150 (48) | 0.019 |
| BIND_RX | `acmp.bind_rx.if1` | 567,037 | 11.341 | 10 | 20 | MISS T_svc | 1,815,999 | 190 (77) | 0.019 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 877,580 | 17.552 | 10 | 20 | MISS T_svc | 1,685,987 | 153 (32) | 0.018 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 1,266,111 | 25.322 | 10 | 20 | MISS ceiling | 1,988,671 | 185 (47) | 0.016 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 816,056 | 16.321 | 10 | 20 | MISS T_svc | 1,543,605 | 254 (50) | 0.024 |
| PROBE_TX | `acmp.probe_tx.if1` | 1,367,836 | 27.357 | 10 | 20 | MISS ceiling | 4,683,146 | 847 (48) | 0.006 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 1,216,267 | 24.325 | 10 | 20 | MISS ceiling | 1,696,150 | 169 (48) | 0.017 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 971,393 | 19.428 | 10 | 20 | MISS T_svc | 1,695,525 | 169 (48) | 0.017 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 1,260,713 | 25.214 | 10 | 20 | MISS ceiling | 1,984,888 | 186 (48) | 0.016 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 380,764 | 7.615 | 10 | 24 | fits | 361,457 | 50 | 0.025 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 442,806 | 8.856 | 10 | 24 | fits | 458,161 | 134 | 0.023 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 2,125,073 | 42.501 | 10 | 24 | MISS ceiling | 567,622 | 111 | 0.024 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 425,632 | 8.513 | 10 | 24 | fits | 413,123 | 87 | 0.023 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i32.c0.if0` | 427,760 | 8.555 | 10 | 24 | fits | 441,963 | 92 | 0.024 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i32.c0.if0` | 266,362 | 5.327 | 10 | 24 | fits | 417,121 | 85 | 0.023 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 424,070 | 8.481 | 10 | 24 | fits | 412,118 | 74 | 0.023 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i33.c0.if0` | 425,073 | 8.501 | 10 | 24 | fits | 413,121 | 71 | 0.023 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 423,286 | 8.466 | 10 | 24 | fits | 438,166 | 74 | 0.024 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 464,384 | 9.288 | 10 | 24 | fits | 479,267 | 169 | 0.022 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i31.c0.if0` | 420,055 | 8.401 | 10 | 24 | fits | 434,938 | 61 | 0.024 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i31.c0.if0` | 422,103 | 8.442 | 10 | 24 | fits | 436,986 | 61 | 0.024 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i287.c0.if0` | 351,178 | 7.024 | 10 | 24 | fits | 440,640 | 71 | 0.022 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 1,911,798 | 38.236 | 10 | 24 | MISS ceiling | 600,276 | 114 | 0.023 |
| READ_DESCRIPTOR (144 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 490,526 | 9.811 | 10 | 24 | fits | 444,318 | 86 | 0.022 |
| get_configuration | `aecp.get_configuration.if0` | 444,908 | 8.898 | 10 | 24 | fits | 425,651 | 56 | 0.024 |
| entity_available | `aecp.entity_available.if0` | 446,175 | 8.923 | 10 | 24 | fits | 427,359 | 60 | 0.024 |
| get_name | `aecp.get_name.if0` | 452,300 | 9.046 | 10 | 24 | fits | 433,455 | 73 | 0.024 |
| get_counters | `aecp.get_counters.if0` | 462,817 | 9.256 | 10 | 24 | fits | 444,129 | 94 | 0.025 |
| get_avb_info | `aecp.get_avb_info.if0` | 474,148 | 9.483 | 10 | 24 | fits | 455,198 | 56 | 0.023 |
| unknown_command | `aecp.unknown_command.if0` | 444,180 | 8.884 | 10 | 24 | fits | 425,361 | 56 | 0.024 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 383,540 | 7.671 | 10 | 24 | fits | 364,680 | 53 | 0.025 |
| set_name | `aecp.set_name.if0` | 520,734 | 10.415 | 10 | 24 | MISS T_svc | 553,204 | 149 | 0.021 |
| lock_entity | `aecp.lock_entity.if0` | 330,504 | 6.610 | 10 | 24 | fits | 503,089 | 97 | 0.023 |
| unlock_entity | `aecp.unlock_entity.if0` | 1,404,515 | 28.090 | 10 | 24 | MISS ceiling | 635,741 | 127 | 0.024 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 148,348 | 2.967 | 10 | 24 | fits | 363,967 | 48 | 0.025 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 480,324 | 9.606 | 10 | 24 | fits | 433,612 | 126 | 0.022 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 456,751 | 9.135 | 10 | 24 | fits | 410,652 | 74 | 0.023 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 461,290 | 9.226 | 10 | 24 | fits | 442,023 | 91 | 0.024 |
| get_configuration | `aecp.get_configuration.if1` | 444,714 | 8.894 | 10 | 24 | fits | 425,428 | 54 | 0.024 |
| entity_available | `aecp.entity_available.if1` | 446,379 | 8.928 | 10 | 24 | fits | 427,133 | 58 | 0.024 |
| get_name | `aecp.get_name.if1` | 452,501 | 9.050 | 10 | 24 | fits | 433,229 | 71 | 0.024 |
| get_counters | `aecp.get_counters.if1` | 463,021 | 9.260 | 10 | 24 | fits | 443,906 | 92 | 0.024 |
| get_avb_info | `aecp.get_avb_info.if1` | 447,371 | 8.947 | 10 | 24 | fits | 427,953 | 47 | 0.022 |
| unknown_command | `aecp.unknown_command.if1` | 444,194 | 8.884 | 10 | 24 | fits | 398,116 | 47 | 0.023 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 1,835,912 | 36.718 | 10 | 24 | MISS ceiling | 524,161 | 88 | 0.025 |
| set_name | `aecp.set_name.if1` | 522,306 | 10.446 | 10 | 24 | MISS T_svc | 592,058 | 189 | 0.021 |
| lock_entity | `aecp.lock_entity.if1` | 353,614 | 7.072 | 10 | 24 | fits | 510,659 | 116 | 0.024 |
| unlock_entity | `aecp.unlock_entity.if1` | 280,888 | 5.618 | 10 | 24 | fits | 483,674 | 109 | 0.023 |

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

Save groups owed to #823, not run and not graded: this point is built without saved state (#859): `commit`, `valid`, `absent`, `torn`, `version`, `guard`, `reorder-settle`, `reorder-bindings`, `guard-removed`, `slow-step`.
