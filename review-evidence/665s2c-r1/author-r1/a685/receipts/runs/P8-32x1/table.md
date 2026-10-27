### 8x8

37 of 129 paths and 65 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.028 (4.293) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 17.073 (37.241) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 16.619 (36.619) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 5.134 (25.135) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 23.646 (53.733) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 24.961 (53.733) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 21.848 (30.035) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 23.131 (30.035) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 19.012 (38.881) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 6.067 (34.473) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 16.621 (36.622) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 5.146 (25.147) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 18.819 (38.809) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 8.993 (28.983) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 16.976 (36.649) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 5.515 (25.179) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 4.154 (21.518) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 7.244 (28.859) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 2.296 (42.089) | fits | 2 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 4.806 (24.692) | fits | 2 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 3.438 (23.194) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 7.274 (48.391) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 3.373 (20.847) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 8.584 (45.504) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 4.110 (24.392) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 7.868 (44.968) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 4.453 (24.719) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 1.531 (24.651) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 3.739 (48.673) | fits | 2 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 3.789 (21.214) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 12.444 (32.655) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 13.870 (25.548) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.210 (2.381) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.395 (2.381) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.080 (2.198) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.173 (2.198) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.064 (13.317) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.225 (13.317) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.079 (12.489) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.840 (12.489) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.115 (5.174) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.235 (2.202) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.772 (4.821) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 2.192 (4.839) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.970 (4.602) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.964 (4.597) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.647 (4.280) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.642 (4.276) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.486 (4.119) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.922 (4.556) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 3.201 (4.834) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 2.771 (4.405) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.641 (4.274) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 3.077 (4.711) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.502 (4.396) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.502 (4.589) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.805 (3.437) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 1.800 (3.433) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.629 (5.262) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.623 (5.257) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.724 (4.357) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.720 (4.353) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 2.721 (4.354) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 3.132 (4.765) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.514 (5.146) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.592 (4.225) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 2.602 (4.235) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 3.258 (4.891) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 2.813 (4.446) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 3.296 (4.929) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.895 (4.527) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.860 (4.493) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 2.824 (4.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 2.836 (4.469) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.741 (4.374) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.791 (3.415) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 2.225 (3.858) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 3.961 (6.621) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.976 (6.734) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.871 (4.546) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.915 (4.548) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.502 (4.395) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.503 (4.584) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.652 (10.305) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 10.478 (14.165) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.940 (10.423) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 8.987 (10.470) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 10.073 (13.760) | MISS T_svc | 0 aecp | 2 | 1 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 10.122 (13.809) | MISS T_svc | 0 aecp | 2 | 1 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 12.638 (14.979) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 14.440 (18.642) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 11.920 (15.420) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 10.491 (14.179) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 10.551 (14.240) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 63.824 (70.791) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 48.168 (67.017) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 54.254 (68.886) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 15.073 (29.138) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 119.309 (123.471) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 368.918 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.545 (5.578) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.338 (6.866) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 1.073 (3.032) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.636 (2.623) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.748 (7.439) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.749 (7.044) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.395 (5.578) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.188 (6.866) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.968 (4.956) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 1.244 (5.295) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 14.534 | MISS T_svc | 0 acmp | 4 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 104.865 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 14.576 | MISS T_svc | 0 adp | 4 | 3 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 64.909 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 51.739 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 14.570 | MISS T_svc | 0 aecp | 4 | 3 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 316.800 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 14.559 | MISS T_svc | 0 maap | 4 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 59.458 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 594.239 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 594.219 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 8.558 (10.384) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 8.788 (10.530) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.329 (3.330) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 6.021 (8.122) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 3.081 (3.081) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.234 (3.235) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.939 (7.439) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 7.024 (7.467) | fits | 0 events | 1 | 0 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 160.405 | 22 | 728,920 (14.578) | yes | - |
| backlog-adp | 548.221 | 29 | 1,486,741 (29.735) | no | {'srp': 32} |
| backlog-adp-refill | 594.256 | 31 | 1,378,764 (27.575) | no | {'srp': 32} |
| backlog-owed | 368.969 | 41 | 635,784 (12.716) | yes | - |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 222,627 | 4.453 | 10 | 20 | fits | 1,235,953 | 96 (14) | 0.043 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 76,566 | 1.531 | 10 | 20 | fits | 1,232,545 | 74 (14) | 0.044 |
| LINK_UP | `adp.link_up.if0` | 3,953 | 0.079 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| LINK_UP | `adp.link_up.if1` | 42,019 | 0.840 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 38,601 | 0.772 | 10 | 200 | fits | 120,951 | 47 (39) | 0.056 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 109,590 | 2.192 | 10 | 200 | fits | 120,989 | 47 (39) | 0.056 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 55,760 | 1.115 | 10 | 200 | fits | 105,964 | 19 (11) | 0.057 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 11,762 | 0.235 | 10 | 200 | fits | 4,138 | 9 (11) | 0.197 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 37,383 | 0.748 | 10 | 50 | fits | 371,932 | 160 | 0.052 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 48,379 | 0.968 | 10 | 50 | fits | 131,012 | 37 | 0.059 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 33,526 | 0.671 | 10 | 50 | fits | 131,369 | 38 | 0.058 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 69,746 | 1.395 | 10 | 50 | fits | 149,750 | 65 | 0.060 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 77,254 | 1.545 | 10 | 50 | fits | 149,750 | 65 | 0.060 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 53,671 | 1.073 | 10 | 50 | fits | 151,595 | 54 | 0.061 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 37,463 | 0.749 | 10 | 50 | fits | 352,204 | 154 | 0.048 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 41,160 | 0.823 | 10 | 50 | fits | 132,732 | 38 | 0.057 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 62,179 | 1.244 | 10 | 50 | fits | 132,831 | 38 | 0.057 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 109,406 | 2.188 | 10 | 50 | fits | 173,049 | 71 | 0.065 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 116,914 | 2.338 | 10 | 50 | fits | 173,049 | 71 | 0.065 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 31,806 | 0.636 | 10 | 50 | fits | 131,149 | 48 | 0.052 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 168,662 | 3.373 | 10 | 20 | fits | 1,042,341 | 93 (35) | 0.046 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 429,185 | 8.584 | 10 | 20 | fits | 1,232,860 | 96 (35) | 0.043 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 205,517 | 4.110 | 10 | 20 | fits | 1,219,621 | 73 (14) | 0.043 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 393,386 | 7.868 | 10 | 20 | fits | 1,028,803 | 70 (14) | 0.046 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 186,928 | 3.739 | 10 | 20 | fits | 1,060,704 | 74 (14) | 0.044 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 189,448 | 3.789 | 10 | 20 | fits | 1,060,704 | 74 (14) | 0.044 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 114,803 | 2.296 | 10 | 20 | fits | 1,043,767 | 93 (35) | 0.046 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 240,285 | 4.806 | 10 | 20 | fits | 1,234,600 | 96 (35) | 0.043 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 346,935 | 6.939 | 10 | 18 | fits | 371,932 | 160 | 0.052 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 351,195 | 7.024 | 10 | 18 | fits | 373,340 | 160 | 0.051 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 166,469 | 3.329 | 10 | 18 | fits | 166,501 | 29 | 0.070 |
| malformed MRPDU discard | `srp.malformed.if0` | 154,037 | 3.081 | 10 | 18 | fits | 154,069 | 36 | 0.063 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 427,887 | 8.558 | 210 | 218 | fits | 519,225 | 149 | 0.064 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 301,071 | 6.021 | 10 | 18 | fits | 196,356 | 36 | 0.073 |
| malformed MRPDU discard | `srp.malformed.if1` | 161,714 | 3.234 | 10 | 18 | fits | 161,746 | 36 | 0.061 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 439,422 | 8.788 | 210 | 218 | fits | 526,485 | 149 | 0.063 |
| an event behind 15 others | `backlog.event.if0` | 753,642 | 15.073 | 10 | 200 | MISS T_svc | 727,992 | 375 | 0.065 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 3,191,198 | 63.824 | 10 | 20 | MISS ceiling | 476,059 | 256 | 0.051 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 728,816 | 14.576 | 10 | 200 | MISS T_svc | 728,920 | 392 | 0.065 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,586,968 | 51.739 | 10 | 200 | MISS T_svc | 511,023 | 324 | 0.051 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 726,687 | 14.534 | 10 | 20 | MISS T_svc | 728,920 | 392 | 0.065 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,536,885 | 70.738 | 10 | 20 | MISS ceiling | 476,059 | 256 | 0.051 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 728,479 | 14.570 | 10 | 24 | MISS T_svc | 728,920 | 392 | 0.065 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,543,268 | 130.865 | 10 | 24 | MISS ceiling | 326,026 | 169 | 0.057 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 727,959 | 14.559 | 10 | 50 | MISS T_svc | 728,920 | 392 | 0.065 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,586,220 | 51.724 | 10 | 50 | MISS ceiling | 511,023 | 324 | 0.051 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 2,075,165 | 41.503 | 10 | 18 | MISS ceiling | 619,441 | 379 | 0.059 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,370,780 | 147.416 | 10 | 18 | MISS ceiling | 153,927 | 48 | 0.066 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,408,423 | 48.168 | 10 | 20 | MISS ceiling | 1,172,438 | 366 | 0.045 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 615,512 | 12.310 | 10 | 200 | MISS T_svc | 995,008 | 397 | 0.046 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,971,058 | 59.421 | 10 | 200 | MISS T_svc | 1,172,438 | 366 | 0.045 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 615,968 | 12.319 | 10 | 20 | MISS T_svc | 995,008 | 397 | 0.046 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 5,219,751 | 104.395 | 10 | 20 | MISS ceiling | 1,177,937 | 275 | 0.042 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 617,760 | 12.355 | 10 | 24 | MISS T_svc | 995,008 | 397 | 0.046 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 15,816,619 | 316.332 | 10 | 24 | MISS ceiling | 1,024,004 | 188 | 0.043 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 617,240 | 12.345 | 10 | 50 | MISS T_svc | 995,008 | 397 | 0.046 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,972,896 | 59.458 | 10 | 50 | MISS ceiling | 1,172,438 | 366 | 0.045 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,410,228 | 548.205 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,409,221 | 548.184 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,712,705 | 54.254 | 10 | 20 | MISS ceiling | 1,243,060 | 307 | 0.042 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 615,512 | 12.310 | 10 | 200 | MISS T_svc | 995,008 | 397 | 0.046 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 3,245,449 | 64.909 | 10 | 200 | MISS T_svc | 1,243,060 | 307 | 0.042 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 615,968 | 12.319 | 10 | 20 | MISS T_svc | 995,008 | 397 | 0.046 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 5,243,255 | 104.865 | 10 | 20 | MISS ceiling | 1,243,060 | 307 | 0.042 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 617,760 | 12.355 | 10 | 24 | MISS T_svc | 995,008 | 397 | 0.046 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,839,993 | 316.800 | 10 | 24 | MISS ceiling | 1,023,808 | 188 | 0.043 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 617,240 | 12.345 | 10 | 50 | MISS T_svc | 995,008 | 397 | 0.046 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,915,803 | 58.316 | 10 | 50 | MISS ceiling | 1,115,345 | 359 | 0.045 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,711,968 | 594.239 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,710,961 | 594.219 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,965,429 | 119.309 | 10 | 20 | MISS ceiling | 428,022 | 191 | 0.058 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,445,893 | 368.918 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,445,855 | 368.917 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,445,818 | 368.916 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,445,780 | 368.916 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 486,761 | 9.735 | 10 | 200 | fits | 506,395 | 344 | 0.053 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 2,120,192 | 42.404 | 10 | 200 | MISS T_svc | 513,296 | 281 | 0.051 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 484,632 | 9.693 | 10 | 20 | fits | 506,395 | 344 | 0.053 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,005,389 | 60.108 | 10 | 20 | MISS ceiling | 409,197 | 120 | 0.062 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 486,424 | 9.728 | 10 | 24 | fits | 506,395 | 344 | 0.053 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,156,233 | 143.125 | 10 | 24 | MISS ceiling | 254,706 | 124 | 0.043 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 485,904 | 9.718 | 10 | 50 | fits | 506,395 | 344 | 0.053 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,119,444 | 42.389 | 10 | 50 | MISS T_svc | 513,296 | 281 | 0.051 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,606,116 | 32.122 | 10 | 18 | MISS ceiling | 635,784 | 343 | 0.060 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 8,015,502 | 160.310 | 10 | 18 | MISS ceiling | 198,568 | 48 | 0.074 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 1,092,400 | 21.848 | 10 | 20 | MISS ceiling | 1,501,742 | 124 (29) | 0.042 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 1,156,563 | 23.131 | 10 | 20 | MISS ceiling | 1,501,742 | 124 (29) | 0.042 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,182,301 | 23.646 | 10 | 20 | MISS ceiling | 1,314,374 | 132 (35) | 0.044 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,248,045 | 24.961 | 10 | 20 | MISS ceiling | 1,314,374 | 132 (35) | 0.044 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 171,921 | 3.438 | 10 | 20 | fits | 1,159,709 | 71 (12) | 0.039 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 363,675 | 7.274 | 10 | 20 | fits | 1,236,002 | 96 (12) | 0.043 |
| LINK_UP | `adp.link_up.if0` | 3,953 | 0.079 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| LINK_UP | `adp.link_up.if1` | 42,019 | 0.840 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 38,601 | 0.772 | 10 | 200 | fits | 120,951 | 47 (39) | 0.056 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 109,590 | 2.192 | 10 | 200 | fits | 120,989 | 47 (39) | 0.056 |
| LINK_DOWN | `adp.link_down.if0` | 3,220 | 0.064 | 10 | 200 | fits | 665,837 | 58 (9) | 0.088 |
| LINK_DOWN | `adp.link_down.if1` | 261,228 | 5.225 | 10 | 200 | fits | 665,837 | 58 (9) | 0.088 |
| LINK_UP | `adp.link_up.if0` | 3,953 | 0.079 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| LINK_UP | `adp.link_up.if1` | 42,019 | 0.840 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 38,601 | 0.772 | 10 | 200 | fits | 120,951 | 47 (39) | 0.056 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 109,590 | 2.192 | 10 | 200 | fits | 120,989 | 47 (39) | 0.056 |
| GM_CHANGE | `adp.gm_change.if0` | 4,001 | 0.080 | 10 | 200 | fits | 109,892 | 28 (11) | 0.062 |
| GM_CHANGE | `adp.gm_change.if1` | 8,637 | 0.173 | 10 | 200 | fits | 109,892 | 28 (11) | 0.062 |
| LINK_UP | `adp.link_up.if0` | 3,953 | 0.079 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| LINK_UP | `adp.link_up.if1` | 42,019 | 0.840 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 38,601 | 0.772 | 10 | 200 | fits | 120,951 | 47 (39) | 0.056 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 109,590 | 2.192 | 10 | 200 | fits | 120,989 | 47 (39) | 0.056 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 10,482 | 0.210 | 10 | 200 | fits | 119,049 | 66 (31) | 0.054 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 19,730 | 0.395 | 10 | 200 | fits | 119,049 | 66 (31) | 0.054 |
| LINK_UP | `adp.link_up.if0` | 3,953 | 0.079 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| LINK_UP | `adp.link_up.if1` | 42,019 | 0.840 | 10 | 200 | fits | 624,441 | 304 (11) | 0.050 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 38,601 | 0.772 | 10 | 200 | fits | 120,951 | 47 (39) | 0.056 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 109,590 | 2.192 | 10 | 200 | fits | 120,989 | 47 (39) | 0.056 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 10,482 | 0.210 | 10 | 200 | fits | 110,286 | 39 (31) | 0.052 |
| set_name | `aecp_fanout.set_name.if0` | 631,886 | 12.638 | 10 | 24 | MISS T_svc | 748,929 | 1137 | 0.101 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 446,990 | 8.940 | 10 | 24 | fits | 521,134 | 596 | 0.139 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 412,230 | 8.245 | 10 | 24 | fits | 494,828 | 556 | 0.140 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 503,666 | 10.073 | 10 | 24 | MISS T_svc | 494,394 | 556 | 0.140 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 596,012 | 11.920 | 10 | 24 | MISS T_svc | 577,536 | 652 | 0.136 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 432,597 | 8.652 | 10 | 24 | fits | 515,246 | 655 | 0.137 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 524,536 | 10.491 | 10 | 24 | MISS T_svc | 514,000 | 655 | 0.137 |
| set_name | `aecp_fanout.set_name.if1` | 721,981 | 14.440 | 10 | 24 | MISS T_svc | 738,081 | 1137 | 0.099 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 449,334 | 8.987 | 10 | 24 | fits | 523,514 | 596 | 0.140 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 414,178 | 8.284 | 10 | 24 | fits | 496,776 | 556 | 0.141 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 506,100 | 10.122 | 10 | 24 | MISS T_svc | 495,566 | 556 | 0.140 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 523,876 | 10.478 | 10 | 24 | MISS T_svc | 513,401 | 655 | 0.136 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 527,539 | 10.551 | 10 | 24 | MISS T_svc | 517,227 | 655 | 0.139 |
| BIND_RX | `acmp.bind_rx.if0` | 51,415 | 1.028 | 10 | 20 | fits | 214,669 | 83 (77) | 0.054 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 207,698 | 4.154 | 10 | 20 | fits | 1,075,887 | 105 (32) | 0.043 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 950,596 | 19.012 | 10 | 20 | MISS T_svc | 1,065,012 | 120 (47) | 0.041 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 622,209 | 12.444 | 10 | 20 | MISS T_svc | 753,808 | 176 (50) | 0.049 |
| PROBE_TX | `acmp.probe_tx.if0` | 848,784 | 16.976 | 10 | 20 | MISS T_svc | 954,880 | 119 (48) | 0.043 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 940,928 | 18.819 | 10 | 20 | MISS T_svc | 1,062,488 | 121 (48) | 0.041 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 830,928 | 16.619 | 10 | 20 | MISS T_svc | 953,213 | 118 (48) | 0.043 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 831,065 | 16.621 | 10 | 20 | MISS T_svc | 953,054 | 118 (48) | 0.043 |
| BIND_RX | `acmp.bind_rx.if1` | 853,636 | 17.073 | 10 | 20 | MISS T_svc | 984,118 | 148 (77) | 0.045 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 362,180 | 7.244 | 10 | 20 | fits | 1,442,926 | 103 (32) | 0.043 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 303,326 | 6.067 | 10 | 20 | fits | 1,723,634 | 331 (47) | 0.045 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 693,479 | 13.870 | 10 | 20 | MISS T_svc | 1,277,405 | 118 (50) | 0.045 |
| PROBE_TX | `acmp.probe_tx.if1` | 275,771 | 5.515 | 10 | 20 | fits | 1,258,935 | 117 (48) | 0.044 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 449,665 | 8.993 | 10 | 20 | fits | 1,449,173 | 119 (48) | 0.042 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 256,714 | 5.134 | 10 | 20 | fits | 1,256,751 | 116 (48) | 0.044 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 257,313 | 5.146 | 10 | 20 | fits | 1,257,350 | 116 (48) | 0.044 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 89,545 | 1.791 | 10 | 24 | fits | 170,763 | 47 | 0.058 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 181,463 | 3.629 | 10 | 24 | fits | 263,107 | 132 | 0.051 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 136,207 | 2.724 | 10 | 24 | fits | 217,848 | 73 | 0.048 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 162,921 | 3.258 | 10 | 24 | fits | 244,562 | 91 | 0.053 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 141,222 | 2.824 | 10 | 24 | fits | 222,866 | 83 | 0.047 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 141,798 | 2.836 | 10 | 24 | fits | 223,442 | 83 | 0.047 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 137,038 | 2.741 | 10 | 24 | fits | 218,682 | 72 | 0.048 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 136,031 | 2.721 | 10 | 24 | fits | 217,675 | 68 | 0.048 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 156,588 | 3.132 | 10 | 24 | fits | 238,229 | 72 | 0.054 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 175,676 | 3.514 | 10 | 24 | fits | 257,317 | 160 | 0.042 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 129,595 | 2.592 | 10 | 24 | fits | 211,236 | 52 | 0.050 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 130,107 | 2.602 | 10 | 24 | fits | 211,748 | 52 | 0.049 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 164,803 | 3.296 | 10 | 24 | fits | 246,444 | 76 | 0.052 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 144,728 | 2.895 | 10 | 24 | fits | 226,369 | 75 | 0.046 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 142,991 | 2.860 | 10 | 24 | fits | 224,632 | 71 | 0.047 |
| get_configuration | `aecp.get_configuration.if0` | 124,294 | 2.486 | 10 | 24 | fits | 205,935 | 47 | 0.051 |
| entity_available | `aecp.entity_available.if0` | 148,475 | 2.970 | 10 | 24 | fits | 230,119 | 58 | 0.057 |
| get_name | `aecp.get_name.if0` | 132,054 | 2.641 | 10 | 24 | fits | 213,698 | 64 | 0.049 |
| get_counters | `aecp.get_counters.if0` | 160,071 | 3.201 | 10 | 24 | fits | 241,715 | 87 | 0.055 |
| get_avb_info | `aecp.get_avb_info.if0` | 132,337 | 2.647 | 10 | 24 | fits | 213,981 | 47 | 0.049 |
| unknown_command | `aecp.unknown_command.if0` | 143,542 | 2.871 | 10 | 24 | fits | 227,297 | 54 | 0.056 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 90,235 | 1.805 | 10 | 24 | fits | 171,827 | 51 | 0.059 |
| set_name | `aecp.set_name.if0` | 198,061 | 3.961 | 10 | 24 | fits | 331,052 | 114 | 0.046 |
| lock_entity | `aecp.lock_entity.if0` | 125,104 | 2.502 | 10 | 24 | fits | 219,787 | 66 | 0.055 |
| unlock_entity | `aecp.unlock_entity.if0` | 125,122 | 2.502 | 10 | 24 | fits | 219,754 | 66 | 0.055 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 111,273 | 2.225 | 10 | 24 | fits | 192,897 | 52 | 0.064 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 181,163 | 3.623 | 10 | 24 | fits | 262,839 | 130 | 0.051 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 135,990 | 2.720 | 10 | 24 | fits | 217,666 | 71 | 0.048 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 140,643 | 2.813 | 10 | 24 | fits | 222,319 | 82 | 0.047 |
| get_configuration | `aecp.get_configuration.if1` | 146,106 | 2.922 | 10 | 24 | fits | 227,780 | 52 | 0.056 |
| entity_available | `aecp.entity_available.if1` | 148,188 | 2.964 | 10 | 24 | fits | 229,862 | 56 | 0.057 |
| get_name | `aecp.get_name.if1` | 153,857 | 3.077 | 10 | 24 | fits | 235,531 | 69 | 0.055 |
| get_counters | `aecp.get_counters.if1` | 138,560 | 2.771 | 10 | 24 | fits | 220,234 | 78 | 0.049 |
| get_avb_info | `aecp.get_avb_info.if1` | 132,117 | 2.642 | 10 | 24 | fits | 213,791 | 45 | 0.049 |
| unknown_command | `aecp.unknown_command.if1` | 145,728 | 2.915 | 10 | 24 | fits | 227,402 | 52 | 0.056 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 90,015 | 1.800 | 10 | 24 | fits | 171,637 | 49 | 0.059 |
| set_name | `aecp.set_name.if1` | 198,799 | 3.976 | 10 | 24 | fits | 336,695 | 147 | 0.048 |
| lock_entity | `aecp.lock_entity.if1` | 125,119 | 2.502 | 10 | 24 | fits | 229,433 | 85 | 0.061 |
| unlock_entity | `aecp.unlock_entity.if1` | 125,137 | 2.503 | 10 | 24 | fits | 229,204 | 85 | 0.060 |

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
