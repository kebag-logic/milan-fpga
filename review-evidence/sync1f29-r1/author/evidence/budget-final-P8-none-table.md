### 8x8

58 of 127 paths and 100 of 180 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 4.707 (13.357) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 11.615 (31.857) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 10.949 (30.949) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 22.599 (66.250) | MISS ceiling | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 31.774 (79.527) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 34.086 (79.527) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 47.323 (84.392) | MISS ceiling | 2 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 49.603 (84.392) | MISS ceiling | 3 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 11.294 (31.099) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 20.416 (40.233) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 10.954 (30.955) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 22.745 (40.146) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 11.010 (31.002) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 29.505 (88.237) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 11.489 (30.999) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 22.408 (55.081) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 19.622 (35.473) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 16.528 (39.841) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 9.972 (26.975) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 8.380 (32.013) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 9.010 (39.446) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 9.725 (71.190) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 9.347 (71.190) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 16.253 (77.626) | MISS T_svc | 5 events | 1 | 1 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 15.354 (77.626) | MISS T_svc | 6 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 18.776 (69.449) | MISS T_svc | 0 events | 1 | 1 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 3.561 (30.123) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 15.832 (64.529) | MISS T_svc | 0 events | 1 | 1 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 16.575 (64.529) | MISS T_svc | 2 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 2.909 (23.193) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 20.853 (40.715) | MISS ceiling | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 1.572 (8.220) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 1.860 (8.219) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 1.391 (7.927) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 1.528 (7.927) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 17.360 (42.628) | MISS T_svc | 0 events | 1 | 1 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 25.868 (42.628) | MISS T_svc | 0 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 32.056 (73.374) | MISS T_svc | 0 events | 5 | 5 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 41.246 (73.374) | MISS T_svc | 0 events | 5 | 5 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.959 (7.376) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.265 (4.086) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 2.759 (9.160) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 1.576 (7.818) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 4.880 (10.642) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 4.905 (10.669) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 6.942 (11.329) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 5.843 (11.338) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 7.675 (27.676) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 5.577 (11.082) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 6.489 (12.251) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 5.383 (11.147) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 5.818 (11.580) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 5.862 (11.355) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 5.566 (11.693) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 8.780 (15.175) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 3.402 (9.659) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 3.435 (9.681) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 6.056 (12.314) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 6.070 (12.317) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 5.987 (11.749) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 6.006 (11.768) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 5.968 (11.730) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 5.183 (10.945) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 7.356 (12.867) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 5.660 (11.422) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 4.972 (11.242) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 6.109 (11.872) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 5.419 (11.182) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 6.124 (11.887) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 5.495 (11.258) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 6.162 (11.704) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 6.858 (11.679) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 6.191 (11.954) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 5.272 (11.034) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 6.129 (11.880) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 4.764 (10.527) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 8.001 (16.163) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 7.442 (15.058) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 5.538 (11.300) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 5.584 (11.348) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 6.927 (12.174) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 6.705 (13.094) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 15.998 (20.415) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 13.853 (17.185) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 16.350 (19.762) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 14.009 (18.396) | MISS T_svc | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 15.979 (21.771) | MISS T_svc | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 16.054 (21.854) | MISS T_svc | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 20.460 (28.572) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 20.483 (29.471) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 12.612 (15.676) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 13.827 (17.190) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 16.375 (20.471) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 108.725 (120.257) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 81.201 (104.680) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 117.114 (152.861) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 27.684 (52.954) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 161.209 (170.675) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind1.if0` (backlog-owed) | at least 860.001 | NEVER ANSWERED | 9 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 3.828 (10.202) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.009 (8.919) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 1.581 (8.102) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.823 (8.187) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 18.038 (38.991) | MISS T_svc | 0 events | 1 | 1 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 1.703 (15.387) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 3.569 (10.202) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 1.750 (8.919) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 1.595 (5.020) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 2.980 (9.384) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 26.837 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 176.282 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 26.880 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 136.326 | MISS T_svc | 6 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 88.934 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 26.873 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 511.949 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 26.862 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 101.483 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 657.100 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 657.080 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 17.027 (23.027) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 8.258 (11.452) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 7.328 (9.514) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 5.662 (8.983) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 4.410 (8.591) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 16.034 (17.982) | MISS T_svc | 0 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 13.290 (33.216) | MISS T_svc | 1 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 608.778 | 63 | 1,241,802 (24.836) | yes | - |
| backlog-adp | 581.254 | 18 | 2,223,818 (44.476) | no | {'srp': 32} |
| backlog-adp-refill | 657.116 | 21 | 2,224,435 (44.489) | no | {'srp': 32} |
| backlog-owed | 860.053 | 84 | 1,111,047 (22.221) | yes | - |

Composed maximum over the 4 backlog windows: at least 2,224,435 CPU cycles (44.489 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 1,241,802 (24.836 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 938,817 | 18.776 | 10 | 20 | MISS T_svc | 1,595,941 | 132 (14) | 0.886 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 178,061 | 3.561 | 10 | 20 | fits | 1,506,175 | 109 (14) | 0.888 |
| LINK_UP | `adp.link_up.if0` | 1,602,793 | 32.056 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,305 | 41.246 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,932 | 2.759 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 78,823 | 1.576 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 47,972 | 0.959 | 10 | 200 | fits | 166,940 | 19 (11) | 0.861 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 13,247 | 0.265 | 10 | 200 | fits | 5,959 | 9 (11) | 0.867 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 901,917 | 18.038 | 10 | 50 | MISS T_svc | 1,050,434 | 178 | 0.863 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 58,705 | 1.174 | 10 | 50 | fits | 214,121 | 38 | 0.870 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 79,747 | 1.595 | 10 | 50 | fits | 250,985 | 44 | 0.872 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 178,447 | 3.569 | 10 | 50 | fits | 283,910 | 71 | 0.875 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 191,395 | 3.828 | 10 | 50 | fits | 283,910 | 71 | 0.875 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 79,073 | 1.581 | 10 | 50 | fits | 209,888 | 48 | 0.866 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 85,137 | 1.703 | 10 | 50 | fits | 574,160 | 154 | 0.853 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 137,092 | 2.742 | 10 | 50 | fits | 216,163 | 38 | 0.868 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 148,987 | 2.980 | 10 | 50 | fits | 254,239 | 44 | 0.871 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 87,507 | 1.750 | 10 | 50 | fits | 248,759 | 65 | 0.872 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 100,455 | 2.009 | 10 | 50 | fits | 248,759 | 65 | 0.872 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 91,160 | 1.823 | 10 | 50 | fits | 211,802 | 48 | 0.864 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 486,265 | 9.725 | 10 | 20 | fits | 1,686,236 | 158 (35) | 0.885 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 467,361 | 9.347 | 10 | 20 | fits | 1,686,236 | 158 (35) | 0.885 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 812,647 | 16.253 | 10 | 20 | MISS T_svc | 1,264,031 | 95 (14) | 0.883 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 767,692 | 15.354 | 10 | 20 | MISS T_svc | 1,264,031 | 95 (14) | 0.883 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 791,595 | 15.832 | 10 | 20 | MISS T_svc | 1,348,753 | 122 (14) | 0.881 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 828,727 | 16.575 | 10 | 20 | MISS T_svc | 1,348,753 | 122 (14) | 0.881 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 498,611 | 9.972 | 10 | 20 | fits | 1,348,753 | 122 (35) | 0.881 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 418,991 | 8.380 | 10 | 20 | fits | 1,600,626 | 132 (35) | 0.887 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 801,715 | 16.034 | 10 | 18 | MISS T_svc | 899,094 | 124 | 0.859 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 664,525 | 13.290 | 10 | 18 | MISS T_svc | 610,353 | 160 | 0.854 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 412,878 | 8.258 | 10 | 18 | fits | 298,724 | 36 | 0.864 |
| malformed MRPDU discard | `srp.malformed.if0` | 283,105 | 5.662 | 10 | 18 | fits | 200,643 | 29 | 0.858 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 851,328 | 17.027 | 210 | 218 | fits | 823,573 | 149 | 0.851 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 366,394 | 7.328 | 10 | 18 | fits | 265,044 | 30 | 0.860 |
| malformed MRPDU discard | `srp.malformed.if1` | 220,518 | 4.410 | 10 | 18 | fits | 207,553 | 30 | 0.858 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | - | - | - | - | no end: missing ['tx:4'] | - | - | - |
| an event behind 15 others | `backlog.event.if0` | 1,384,180 | 27.684 | 10 | 200 | MISS T_svc | 1,241,802 | 377 | 0.874 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 5,436,274 | 108.725 | 10 | 20 | MISS ceiling | 771,034 | 225 | 0.877 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,343,978 | 26.880 | 10 | 200 | MISS T_svc | 854,511 | 388 | 0.874 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 4,446,716 | 88.934 | 10 | 200 | MISS T_svc | 828,733 | 293 | 0.876 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,341,849 | 26.837 | 10 | 20 | MISS ceiling | 854,511 | 388 | 0.874 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 5,948,381 | 118.968 | 10 | 20 | MISS ceiling | 771,034 | 225 | 0.877 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,343,641 | 26.873 | 10 | 24 | MISS ceiling | 854,511 | 388 | 0.874 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 10,759,332 | 215.187 | 10 | 24 | MISS ceiling | 478,849 | 132 | 0.881 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,343,121 | 26.862 | 10 | 50 | MISS T_svc | 854,511 | 388 | 0.874 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 4,445,968 | 88.919 | 10 | 50 | MISS ceiling | 828,733 | 293 | 0.876 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 9,322,573 | 186.451 | 10 | 18 | MISS ceiling | 576,287 | 171 | 0.878 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 14,713,161 | 294.263 | 10 | 18 | MISS ceiling | 240,067 | 48 | 0.861 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 4,060,055 | 81.201 | 10 | 20 | MISS ceiling | 1,727,055 | 383 | 0.881 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 1,171,039 | 23.421 | 10 | 200 | MISS T_svc | 1,332,434 | 407 | 0.880 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 5,072,292 | 101.446 | 10 | 200 | MISS T_svc | 1,727,055 | 383 | 0.881 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 1,171,495 | 23.430 | 10 | 20 | MISS ceiling | 1,332,434 | 407 | 0.880 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 8,778,603 | 175.572 | 10 | 20 | MISS ceiling | 1,957,264 | 309 | 0.884 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 1,173,288 | 23.466 | 10 | 24 | MISS T_svc | 1,332,434 | 407 | 0.880 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 25,444,596 | 508.892 | 10 | 24 | MISS ceiling | 1,571,360 | 238 | 0.885 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 1,172,768 | 23.455 | 10 | 50 | MISS T_svc | 1,332,434 | 407 | 0.880 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 5,074,130 | 101.483 | 10 | 50 | MISS ceiling | 1,727,055 | 383 | 0.881 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 29,061,860 | 581.237 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 29,060,853 | 581.217 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 5,855,720 | 117.114 | 10 | 20 | MISS ceiling | 2,069,882 | 341 | 0.883 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 1,171,039 | 23.421 | 10 | 200 | MISS T_svc | 1,332,434 | 407 | 0.880 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 6,816,319 | 136.326 | 10 | 200 | MISS T_svc | 2,069,882 | 341 | 0.883 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 1,171,495 | 23.430 | 10 | 20 | MISS ceiling | 1,332,434 | 407 | 0.880 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 8,814,125 | 176.282 | 10 | 20 | MISS ceiling | 2,069,882 | 341 | 0.883 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 1,173,288 | 23.466 | 10 | 24 | MISS T_svc | 1,332,434 | 407 | 0.880 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 25,597,433 | 511.949 | 10 | 24 | MISS ceiling | 1,686,744 | 222 | 0.887 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 1,172,768 | 23.455 | 10 | 50 | MISS T_svc | 1,332,434 | 407 | 0.880 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 4,973,421 | 99.468 | 10 | 50 | MISS ceiling | 1,626,346 | 376 | 0.883 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 32,854,983 | 657.100 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 32,853,976 | 657.080 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 8,060,443 | 161.209 | 10 | 20 | MISS ceiling | 588,371 | 154 | 0.878 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 8,832,465 | 176.649 | 10 | 20 | MISS ceiling | 772,060 | 199 | 0.874 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 43,000,073 | 860.001 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 9,420,798 | 188.416 | 10 | 20 | MISS ceiling | 588,408 | 154 | 0.878 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 42,999,998 | 860.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 892,125 | 17.842 | 10 | 200 | MISS T_svc | 881,549 | 346 | 0.874 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 3,614,986 | 72.300 | 10 | 200 | MISS T_svc | 959,942 | 290 | 0.875 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 889,995 | 17.800 | 10 | 20 | MISS T_svc | 881,549 | 346 | 0.874 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 5,269,081 | 105.382 | 10 | 20 | MISS ceiling | 827,948 | 203 | 0.875 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 891,788 | 17.836 | 10 | 24 | MISS T_svc | 881,549 | 346 | 0.874 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 11,213,251 | 224.265 | 10 | 24 | MISS ceiling | 492,055 | 132 | 0.880 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 891,268 | 17.825 | 10 | 50 | MISS T_svc | 881,549 | 346 | 0.874 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 3,614,239 | 72.285 | 10 | 50 | MISS ceiling | 959,942 | 290 | 0.875 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 7,198,552 | 143.971 | 10 | 18 | MISS ceiling | 801,505 | 199 | 0.874 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 17,040,215 | 340.804 | 10 | 18 | MISS ceiling | 239,726 | 30 | 0.859 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,366,169 | 47.323 | 10 | 20 | MISS ceiling | 1,725,102 | 219 (29) | 0.885 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 2,480,149 | 49.603 | 10 | 20 | MISS ceiling | 1,725,102 | 219 (29) | 0.885 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,588,717 | 31.774 | 10 | 20 | MISS ceiling | 2,102,309 | 185 (35) | 0.886 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,704,313 | 34.086 | 10 | 20 | MISS ceiling | 2,102,309 | 185 (35) | 0.886 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | - | - | - | - | no start: no deadline:2 after the mark | - | - | - |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 450,495 | 9.010 | 10 | 20 | fits | 1,972,309 | 149 (12) | 0.888 |
| LINK_UP | `adp.link_up.if0` | 1,602,793 | 32.056 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,305 | 41.246 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,932 | 2.759 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 78,823 | 1.576 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| LINK_DOWN | `adp.link_down.if0` | 867,983 | 17.360 | 10 | 200 | MISS T_svc | 1,172,077 | 70 (9) | 0.875 |
| LINK_DOWN | `adp.link_down.if1` | 1,293,388 | 25.868 | 10 | 200 | MISS T_svc | 1,172,077 | 70 (9) | 0.875 |
| LINK_UP | `adp.link_up.if0` | 1,602,793 | 32.056 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,305 | 41.246 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,932 | 2.759 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 78,823 | 1.576 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| GM_CHANGE | `adp.gm_change.if0` | 69,533 | 1.391 | 10 | 200 | fits | 173,208 | 28 (11) | 0.861 |
| GM_CHANGE | `adp.gm_change.if1` | 76,413 | 1.528 | 10 | 200 | fits | 173,208 | 28 (11) | 0.861 |
| LINK_UP | `adp.link_up.if0` | 1,602,793 | 32.056 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,305 | 41.246 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,932 | 2.759 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 78,823 | 1.576 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 78,622 | 1.572 | 10 | 200 | fits | 187,880 | 67 (31) | 0.862 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 93,000 | 1.860 | 10 | 200 | fits | 187,880 | 67 (31) | 0.862 |
| LINK_UP | `adp.link_up.if0` | 1,602,793 | 32.056 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,305 | 41.246 | 10 | 200 | MISS T_svc | 2,009,396 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 137,932 | 2.759 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 78,823 | 1.576 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 78,622 | 1.572 | 10 | 200 | fits | 173,878 | 39 (31) | 0.861 |
| set_name | `aecp_fanout.set_name.if0` | 1,022,976 | 20.460 | 10 | 24 | MISS T_svc | 1,231,176 | 1172 | 0.881 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 817,520 | 16.350 | 10 | 24 | MISS T_svc | 790,356 | 613 | 0.876 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 798,973 | 15.979 | 10 | 24 | MISS T_svc | 821,227 | 587 | 0.878 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 774,071 | 15.481 | 10 | 24 | MISS T_svc | 782,838 | 580 | 0.877 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 630,623 | 12.612 | 10 | 24 | MISS T_svc | 783,776 | 598 | 0.879 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 799,912 | 15.998 | 10 | 24 | MISS T_svc | 823,097 | 679 | 0.880 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 691,372 | 13.827 | 10 | 24 | MISS T_svc | 859,521 | 686 | 0.880 |
| set_name | `aecp_fanout.set_name.if1` | 1,024,132 | 20.483 | 10 | 24 | MISS T_svc | 1,149,702 | 1132 | 0.882 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 700,471 | 14.009 | 10 | 24 | MISS T_svc | 919,804 | 674 | 0.879 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 802,700 | 16.054 | 10 | 24 | MISS T_svc | 823,532 | 587 | 0.878 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 778,422 | 15.568 | 10 | 24 | MISS T_svc | 784,858 | 580 | 0.878 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 692,664 | 13.853 | 10 | 24 | MISS T_svc | 859,242 | 686 | 0.880 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 818,750 | 16.375 | 10 | 24 | MISS T_svc | 825,618 | 679 | 0.880 |
| BIND_RX | `acmp.bind_rx.if0` | 235,367 | 4.707 | 10 | 20 | fits | 396,614 | 90 (77) | 0.869 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 981,103 | 19.622 | 10 | 20 | MISS T_svc | 1,773,628 | 144 (32) | 0.885 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 564,686 | 11.294 | 10 | 20 | MISS T_svc | 1,554,928 | 149 (47) | 0.884 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 145,457 | 2.909 | 10 | 20 | fits | 1,159,649 | 194 (50) | 0.881 |
| PROBE_TX | `acmp.probe_tx.if0` | 574,459 | 11.489 | 10 | 20 | MISS T_svc | 1,549,972 | 151 (48) | 0.884 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 550,504 | 11.010 | 10 | 20 | MISS T_svc | 1,550,121 | 150 (48) | 0.884 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 547,428 | 10.949 | 10 | 20 | MISS T_svc | 1,547,465 | 150 (48) | 0.884 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 547,689 | 10.954 | 10 | 20 | MISS T_svc | 1,547,726 | 150 (48) | 0.884 |
| BIND_RX | `acmp.bind_rx.if1` | 580,771 | 11.615 | 10 | 20 | MISS T_svc | 1,592,855 | 180 (77) | 0.883 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 826,403 | 16.528 | 10 | 20 | MISS T_svc | 1,992,049 | 153 (32) | 0.887 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 1,020,784 | 20.416 | 10 | 20 | MISS ceiling | 2,011,675 | 168 (47) | 0.887 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 1,042,634 | 20.853 | 10 | 20 | MISS ceiling | 2,035,758 | 171 (50) | 0.887 |
| PROBE_TX | `acmp.probe_tx.if1` | 1,120,384 | 22.408 | 10 | 20 | MISS ceiling | 2,754,069 | 386 (48) | 0.874 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 1,475,274 | 29.505 | 10 | 20 | MISS ceiling | 1,657,805 | 176 (48) | 0.886 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 1,129,954 | 22.599 | 10 | 20 | MISS ceiling | 1,654,680 | 176 (48) | 0.886 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 1,137,232 | 22.745 | 10 | 20 | MISS ceiling | 2,007,278 | 169 (48) | 0.887 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 306,447 | 6.129 | 10 | 24 | fits | 322,754 | 56 | 0.874 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 302,805 | 6.056 | 10 | 24 | fits | 419,161 | 127 | 0.880 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 299,332 | 5.987 | 10 | 24 | fits | 415,411 | 82 | 0.879 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 305,464 | 6.109 | 10 | 24 | fits | 421,369 | 123 | 0.879 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 342,915 | 6.858 | 10 | 24 | fits | 387,383 | 86 | 0.879 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 309,574 | 6.191 | 10 | 24 | fits | 425,404 | 92 | 0.879 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 263,577 | 5.272 | 10 | 24 | fits | 379,506 | 74 | 0.879 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 298,404 | 5.968 | 10 | 24 | fits | 414,674 | 77 | 0.879 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 259,151 | 5.183 | 10 | 24 | fits | 374,964 | 67 | 0.878 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 367,822 | 7.356 | 10 | 24 | fits | 448,993 | 163 | 0.880 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 283,003 | 5.660 | 10 | 24 | fits | 402,304 | 61 | 0.878 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 248,576 | 4.972 | 10 | 24 | fits | 366,677 | 54 | 0.878 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 306,218 | 6.124 | 10 | 24 | fits | 424,066 | 78 | 0.877 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 274,772 | 5.495 | 10 | 24 | fits | 392,196 | 77 | 0.878 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 308,097 | 6.162 | 10 | 24 | fits | 389,467 | 74 | 0.878 |
| get_configuration | `aecp.get_configuration.if0` | 383,751 | 7.675 | 10 | 24 | fits | 430,165 | 62 | 0.879 |
| entity_available | `aecp.entity_available.if0` | 244,000 | 4.880 | 10 | 24 | fits | 360,662 | 53 | 0.879 |
| get_name | `aecp.get_name.if0` | 290,885 | 5.818 | 10 | 24 | fits | 407,596 | 73 | 0.879 |
| get_counters | `aecp.get_counters.if0` | 324,432 | 6.489 | 10 | 24 | fits | 384,302 | 87 | 0.880 |
| get_avb_info | `aecp.get_avb_info.if0` | 347,116 | 6.942 | 10 | 24 | fits | 370,067 | 49 | 0.877 |
| unknown_command | `aecp.unknown_command.if0` | 276,876 | 5.538 | 10 | 24 | fits | 393,699 | 56 | 0.878 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 170,095 | 3.402 | 10 | 24 | fits | 287,120 | 54 | 0.873 |
| set_name | `aecp.set_name.if0` | 400,059 | 8.001 | 10 | 24 | fits | 636,907 | 156 | 0.869 |
| lock_entity | `aecp.lock_entity.if0` | 278,318 | 5.566 | 10 | 24 | fits | 411,905 | 90 | 0.875 |
| unlock_entity | `aecp.unlock_entity.if0` | 346,351 | 6.927 | 10 | 24 | fits | 411,882 | 90 | 0.875 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 238,220 | 4.764 | 10 | 24 | fits | 323,187 | 54 | 0.875 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 303,512 | 6.070 | 10 | 24 | fits | 418,892 | 125 | 0.880 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 300,284 | 6.006 | 10 | 24 | fits | 415,867 | 80 | 0.879 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 270,962 | 5.419 | 10 | 24 | fits | 386,285 | 84 | 0.879 |
| get_configuration | `aecp.get_configuration.if1` | 278,875 | 5.577 | 10 | 24 | fits | 357,277 | 48 | 0.878 |
| entity_available | `aecp.entity_available.if1` | 245,232 | 4.905 | 10 | 24 | fits | 360,465 | 51 | 0.879 |
| get_name | `aecp.get_name.if1` | 293,110 | 5.862 | 10 | 24 | fits | 370,896 | 65 | 0.879 |
| get_counters | `aecp.get_counters.if1` | 269,142 | 5.383 | 10 | 24 | fits | 384,105 | 85 | 0.880 |
| get_avb_info | `aecp.get_avb_info.if1` | 292,166 | 5.843 | 10 | 24 | fits | 369,870 | 47 | 0.877 |
| unknown_command | `aecp.unknown_command.if1` | 279,193 | 5.584 | 10 | 24 | fits | 394,488 | 54 | 0.879 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 171,752 | 3.435 | 10 | 24 | fits | 286,923 | 52 | 0.873 |
| set_name | `aecp.set_name.if1` | 372,110 | 7.442 | 10 | 24 | fits | 579,466 | 149 | 0.870 |
| lock_entity | `aecp.lock_entity.if1` | 438,979 | 8.780 | 10 | 24 | fits | 463,485 | 116 | 0.876 |
| unlock_entity | `aecp.unlock_entity.if1` | 335,260 | 6.705 | 10 | 24 | fits | 425,006 | 109 | 0.876 |

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
