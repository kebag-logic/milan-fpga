### 8x8

34 of 129 paths and 66 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.999 (4.218) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 1.465 (21.628) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 16.300 (36.299) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 4.899 (24.899) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 21.385 (53.196) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 22.664 (53.196) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 21.221 (29.719) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 22.467 (29.719) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 18.679 (38.550) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 5.071 (24.956) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 16.294 (36.295) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 8.681 (28.682) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 16.320 (36.313) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 4.926 (24.919) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 18.799 (38.477) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 13.457 (24.909) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 3.929 (21.323) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 3.222 (24.822) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 5.575 (45.413) | fits | 3 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 7.291 (47.879) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 1.941 (47.824) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 8.213 (51.707) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 1.143 (24.408) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 10.461 (45.027) | MISS T_svc | 2 events | 1 | 1 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.615 (24.153) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 1.736 (48.297) | fits | 2 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 2.119 (24.469) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 3.729 (24.407) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 3.052 (48.193) | fits | 2 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 1.986 (20.978) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 12.114 (32.323) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 9.470 (37.887) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.627 (2.775) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.805 (2.775) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.496 (2.556) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.565 (2.556) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.482 (12.640) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.324 (12.640) | fits | 1 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.074 (11.682) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.812 (11.682) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.370 (3.365) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 1.292 (3.365) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 2.330 (6.699) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 1.714 (5.699) | fits | 1 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.925 (4.551) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.922 (4.548) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.623 (4.248) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.618 (4.244) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.461 (4.086) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.457 (4.082) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 3.184 (4.810) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 2.748 (4.375) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.618 (4.243) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 4.412 (8.028) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.900 (4.780) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.474 (4.536) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.793 (12.633) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 2.209 (3.834) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.593 (5.219) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.586 (5.212) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 3.130 (4.756) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.697 (4.323) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 2.698 (4.323) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 3.098 (4.723) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.491 (5.116) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.569 (4.194) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 3.010 (4.635) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.794 (4.419) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 3.219 (4.845) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 2.833 (4.458) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 3.302 (4.928) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.837 (4.462) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 2.802 (4.427) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 3.244 (4.869) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 4.028 (7.642) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.768 (3.384) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 1.759 (3.383) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.288 (8.913) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.946 (6.682) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.878 (4.503) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.883 (4.509) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.901 (4.780) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.474 (4.534) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.377 (10.019) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 10.014 (13.665) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 9.074 (12.557) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 8.251 (9.725) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 9.637 (13.287) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 9.639 (13.290) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 12.814 (17.150) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 13.562 (17.729) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 8.515 (9.969) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 10.017 (13.668) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 10.032 (13.685) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 57.960 (63.770) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 46.429 (66.016) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 52.003 (65.594) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 14.448 (28.053) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 122.316 (127.995) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 369.841 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.553 (5.536) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.718 (7.182) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.624 (2.564) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.054 (3.021) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.723 (6.818) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.727 (7.276) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.405 (5.536) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.570 (7.182) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.659 (5.605) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 1.732 (5.736) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 13.986 | MISS T_svc | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 102.464 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 14.029 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 62.508 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 47.295 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 14.022 | MISS T_svc | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 312.350 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 14.012 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 57.555 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 591.988 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 591.968 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 7.755 (9.518) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 7.910 (9.588) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.278 (3.279) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.867 (3.868) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 2.533 (2.534) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.194 (3.195) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.323 (6.818) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.821 (7.261) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 159.293 | 25 | 701,553 (14.031) | yes | - |
| backlog-adp | 546.482 | 29 | 1,455,929 (29.119) | no | {'srp': 32} |
| backlog-adp-refill | 592.005 | 31 | 1,455,957 (29.119) | no | {'srp': 32} |
| backlog-owed | 369.892 | 41 | 623,013 (12.460) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,455,957 CPU cycles (29.119 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 701,553 (14.031 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 105,927 | 2.119 | 10 | 20 | fits | 1,223,466 | 96 (14) | 0.037 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 186,451 | 3.729 | 10 | 20 | fits | 1,220,367 | 74 (14) | 0.038 |
| LINK_UP | `adp.link_up.if0` | 3,692 | 0.074 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| LINK_UP | `adp.link_up.if1` | 40,624 | 0.812 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 116,521 | 2.330 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 85,707 | 1.714 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 68,486 | 1.370 | 10 | 200 | fits | 7,701 | 18 (11) | 0.128 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 64,605 | 1.292 | 10 | 200 | fits | 7,701 | 18 (11) | 0.128 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 36,175 | 0.723 | 10 | 50 | fits | 340,912 | 154 | 0.033 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 82,947 | 1.659 | 10 | 50 | fits | 129,401 | 38 | 0.051 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 32,871 | 0.657 | 10 | 50 | fits | 129,500 | 38 | 0.051 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 70,243 | 1.405 | 10 | 50 | fits | 146,993 | 65 | 0.049 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 77,645 | 1.553 | 10 | 50 | fits | 146,993 | 65 | 0.049 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 31,219 | 0.624 | 10 | 50 | fits | 128,204 | 48 | 0.046 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 36,340 | 0.727 | 10 | 50 | fits | 363,813 | 160 | 0.035 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 29,966 | 0.599 | 10 | 50 | fits | 130,863 | 38 | 0.049 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 86,618 | 1.732 | 10 | 50 | fits | 130,925 | 38 | 0.049 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 128,485 | 2.570 | 10 | 50 | fits | 169,678 | 71 | 0.053 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 135,887 | 2.718 | 10 | 50 | fits | 169,678 | 71 | 0.053 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 52,703 | 1.054 | 10 | 50 | fits | 151,030 | 54 | 0.052 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 57,170 | 1.143 | 10 | 20 | fits | 1,220,385 | 96 (35) | 0.037 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 523,060 | 10.461 | 10 | 20 | MISS T_svc | 1,030,958 | 93 (35) | 0.039 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 80,757 | 1.615 | 10 | 20 | fits | 1,207,630 | 73 (14) | 0.037 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 86,823 | 1.736 | 10 | 20 | fits | 1,207,228 | 73 (14) | 0.037 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 152,596 | 3.052 | 10 | 20 | fits | 1,048,909 | 74 (14) | 0.037 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 99,280 | 1.986 | 10 | 20 | fits | 1,048,909 | 74 (14) | 0.037 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 278,743 | 5.575 | 10 | 20 | fits | 1,221,765 | 96 (35) | 0.037 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 364,530 | 7.291 | 10 | 20 | fits | 1,221,674 | 96 (35) | 0.037 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 316,133 | 6.323 | 10 | 18 | fits | 340,912 | 154 | 0.033 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 341,063 | 6.821 | 10 | 18 | fits | 363,050 | 160 | 0.035 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 163,909 | 3.278 | 10 | 18 | fits | 163,941 | 29 | 0.062 |
| malformed MRPDU discard | `srp.malformed.if0` | 126,651 | 2.533 | 10 | 18 | fits | 126,683 | 30 | 0.049 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 387,735 | 7.755 | 210 | 218 | fits | 475,880 | 142 | 0.043 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 193,353 | 3.867 | 10 | 18 | fits | 193,385 | 36 | 0.065 |
| malformed MRPDU discard | `srp.malformed.if1` | 159,696 | 3.194 | 10 | 18 | fits | 159,728 | 36 | 0.053 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 395,516 | 7.910 | 210 | 218 | fits | 479,424 | 142 | 0.042 |
| an event behind 15 others | `backlog.event.if0` | 722,398 | 14.448 | 10 | 200 | MISS T_svc | 701,095 | 375 | 0.043 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,897,982 | 57.960 | 10 | 20 | MISS ceiling | 411,605 | 217 | 0.037 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 701,449 | 14.029 | 10 | 200 | MISS T_svc | 701,553 | 392 | 0.042 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,364,755 | 47.295 | 10 | 200 | MISS T_svc | 445,571 | 285 | 0.036 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 699,320 | 13.986 | 10 | 20 | MISS T_svc | 701,553 | 392 | 0.042 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,185,834 | 63.717 | 10 | 20 | MISS ceiling | 411,605 | 217 | 0.037 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 701,112 | 14.022 | 10 | 24 | MISS T_svc | 701,553 | 392 | 0.042 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,227,941 | 124.559 | 10 | 24 | MISS ceiling | 247,806 | 124 | 0.040 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 700,592 | 14.012 | 10 | 50 | MISS T_svc | 701,553 | 392 | 0.042 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,364,007 | 47.280 | 10 | 50 | MISS T_svc | 445,571 | 285 | 0.036 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,522,395 | 70.448 | 10 | 18 | MISS ceiling | 335,103 | 169 | 0.053 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,528,072 | 150.561 | 10 | 18 | MISS ceiling | 152,219 | 48 | 0.059 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,321,442 | 46.429 | 10 | 20 | MISS ceiling | 1,032,763 | 363 | 0.038 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 683,953 | 13.679 | 10 | 200 | MISS T_svc | 1,108,526 | 401 | 0.037 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,875,935 | 57.519 | 10 | 200 | MISS T_svc | 1,032,763 | 363 | 0.038 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 684,409 | 13.688 | 10 | 20 | MISS T_svc | 1,108,526 | 401 | 0.037 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 5,100,427 | 102.009 | 10 | 20 | MISS ceiling | 1,058,083 | 272 | 0.037 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 686,201 | 13.724 | 10 | 24 | MISS T_svc | 1,108,526 | 401 | 0.037 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 15,594,581 | 311.892 | 10 | 24 | MISS ceiling | 1,016,032 | 188 | 0.038 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 685,681 | 13.714 | 10 | 50 | MISS T_svc | 1,108,526 | 401 | 0.037 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,877,773 | 57.555 | 10 | 50 | MISS ceiling | 1,032,763 | 363 | 0.038 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,323,247 | 546.465 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,322,240 | 546.445 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,600,153 | 52.003 | 10 | 20 | MISS ceiling | 1,121,515 | 304 | 0.037 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 683,953 | 13.679 | 10 | 200 | MISS T_svc | 1,108,526 | 401 | 0.037 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 3,125,398 | 62.508 | 10 | 200 | MISS T_svc | 1,121,515 | 304 | 0.037 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 684,409 | 13.688 | 10 | 20 | MISS T_svc | 1,108,526 | 401 | 0.037 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 5,123,204 | 102.464 | 10 | 20 | MISS ceiling | 1,121,515 | 304 | 0.037 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 686,201 | 13.724 | 10 | 24 | MISS T_svc | 1,108,526 | 401 | 0.037 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,617,522 | 312.350 | 10 | 24 | MISS ceiling | 1,015,833 | 188 | 0.038 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 685,681 | 13.714 | 10 | 50 | MISS T_svc | 1,108,526 | 401 | 0.037 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,822,071 | 56.441 | 10 | 50 | MISS ceiling | 977,061 | 356 | 0.038 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,599,416 | 591.988 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,598,409 | 591.968 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,115,798 | 122.316 | 10 | 20 | MISS ceiling | 305,378 | 146 | 0.036 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,492,065 | 369.841 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,492,027 | 369.841 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,491,990 | 369.840 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,491,952 | 369.839 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 520,849 | 10.417 | 10 | 200 | MISS T_svc | 474,778 | 344 | 0.035 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 2,183,095 | 43.662 | 10 | 200 | MISS T_svc | 548,202 | 300 | 0.045 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 518,720 | 10.374 | 10 | 20 | MISS T_svc | 474,778 | 344 | 0.035 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,155,522 | 63.110 | 10 | 20 | MISS ceiling | 504,961 | 213 | 0.044 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 520,512 | 10.410 | 10 | 24 | MISS T_svc | 474,778 | 344 | 0.035 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,040,884 | 140.818 | 10 | 24 | MISS ceiling | 369,744 | 169 | 0.055 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 519,992 | 10.400 | 10 | 50 | MISS T_svc | 474,778 | 344 | 0.035 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,182,347 | 43.647 | 10 | 50 | MISS T_svc | 548,202 | 300 | 0.045 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,634,113 | 32.682 | 10 | 18 | MISS ceiling | 623,013 | 343 | 0.049 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 7,886,431 | 157.729 | 10 | 18 | MISS ceiling | 224,318 | 54 | 0.066 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 1,061,066 | 21.221 | 10 | 20 | MISS ceiling | 1,485,955 | 124 (29) | 0.035 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 1,123,367 | 22.467 | 10 | 20 | MISS ceiling | 1,485,955 | 124 (29) | 0.035 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,069,241 | 21.385 | 10 | 20 | MISS ceiling | 1,299,797 | 132 (35) | 0.037 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,133,183 | 22.664 | 10 | 20 | MISS ceiling | 1,299,797 | 132 (35) | 0.037 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 97,040 | 1.941 | 10 | 20 | fits | 1,032,924 | 67 (12) | 0.033 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 410,667 | 8.213 | 10 | 20 | fits | 1,223,469 | 96 (12) | 0.037 |
| LINK_UP | `adp.link_up.if0` | 3,692 | 0.074 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| LINK_UP | `adp.link_up.if1` | 40,624 | 0.812 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 116,521 | 2.330 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 85,707 | 1.714 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| LINK_DOWN | `adp.link_down.if0` | 24,090 | 0.482 | 10 | 200 | fits | 631,982 | 58 (9) | 0.057 |
| LINK_DOWN | `adp.link_down.if1` | 266,212 | 5.324 | 10 | 200 | fits | 631,982 | 58 (9) | 0.057 |
| LINK_UP | `adp.link_up.if0` | 3,692 | 0.074 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| LINK_UP | `adp.link_up.if1` | 40,624 | 0.812 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 116,521 | 2.330 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 85,707 | 1.714 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| GM_CHANGE | `adp.gm_change.if0` | 24,808 | 0.496 | 10 | 200 | fits | 127,816 | 34 (11) | 0.053 |
| GM_CHANGE | `adp.gm_change.if1` | 28,245 | 0.565 | 10 | 200 | fits | 127,816 | 34 (11) | 0.053 |
| LINK_UP | `adp.link_up.if0` | 3,692 | 0.074 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| LINK_UP | `adp.link_up.if1` | 40,624 | 0.812 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 116,521 | 2.330 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 85,707 | 1.714 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 31,373 | 0.627 | 10 | 200 | fits | 138,743 | 73 (31) | 0.052 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 40,244 | 0.805 | 10 | 200 | fits | 138,743 | 73 (31) | 0.052 |
| LINK_UP | `adp.link_up.if0` | 3,692 | 0.074 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| LINK_UP | `adp.link_up.if1` | 40,624 | 0.812 | 10 | 200 | fits | 584,090 | 298 (11) | 0.030 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 116,521 | 2.330 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 85,707 | 1.714 | 10 | 200 | fits | 138,116 | 84 (39) | 0.049 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 31,373 | 0.627 | 10 | 200 | fits | 130,099 | 45 (31) | 0.053 |
| set_name | `aecp_fanout.set_name.if0` | 640,708 | 12.814 | 10 | 24 | MISS T_svc | 712,543 | 1131 | 0.086 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 453,701 | 9.074 | 10 | 24 | fits | 485,897 | 590 | 0.121 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 473,314 | 9.466 | 10 | 24 | fits | 482,583 | 557 | 0.121 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 481,828 | 9.637 | 10 | 24 | fits | 482,603 | 557 | 0.121 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 425,731 | 8.515 | 10 | 24 | fits | 498,462 | 596 | 0.122 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 418,830 | 8.377 | 10 | 24 | fits | 500,943 | 655 | 0.117 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 500,843 | 10.017 | 10 | 24 | MISS T_svc | 500,819 | 655 | 0.117 |
| set_name | `aecp_fanout.set_name.if1` | 678,100 | 13.562 | 10 | 24 | MISS T_svc | 704,139 | 1130 | 0.085 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 412,542 | 8.251 | 10 | 24 | fits | 486,253 | 589 | 0.121 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 473,115 | 9.462 | 10 | 24 | fits | 482,417 | 556 | 0.121 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 481,974 | 9.639 | 10 | 24 | fits | 482,367 | 556 | 0.121 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 500,717 | 10.014 | 10 | 24 | MISS T_svc | 500,818 | 655 | 0.117 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 501,625 | 10.032 | 10 | 24 | MISS T_svc | 501,370 | 655 | 0.117 |
| BIND_RX | `acmp.bind_rx.if0` | 49,927 | 0.999 | 10 | 20 | fits | 210,911 | 83 (77) | 0.044 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 196,445 | 3.929 | 10 | 20 | fits | 1,066,168 | 105 (32) | 0.038 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 933,947 | 18.679 | 10 | 20 | MISS T_svc | 1,055,670 | 120 (47) | 0.036 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 605,716 | 12.114 | 10 | 20 | MISS T_svc | 744,755 | 176 (50) | 0.042 |
| PROBE_TX | `acmp.probe_tx.if0` | 939,974 | 18.799 | 10 | 20 | MISS T_svc | 1,053,633 | 122 (48) | 0.036 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 816,003 | 16.320 | 10 | 20 | MISS T_svc | 945,462 | 118 (48) | 0.037 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 814,999 | 16.300 | 10 | 20 | MISS T_svc | 944,365 | 118 (48) | 0.038 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 814,715 | 16.294 | 10 | 20 | MISS T_svc | 944,125 | 118 (48) | 0.038 |
| BIND_RX | `acmp.bind_rx.if1` | 73,267 | 1.465 | 10 | 20 | fits | 1,081,418 | 151 (77) | 0.037 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 161,078 | 3.222 | 10 | 20 | fits | 1,241,113 | 100 (32) | 0.038 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 253,572 | 5.071 | 10 | 20 | fits | 1,247,795 | 115 (47) | 0.038 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 473,514 | 9.470 | 10 | 20 | fits | 1,894,336 | 337 (50) | 0.032 |
| PROBE_TX | `acmp.probe_tx.if1` | 672,826 | 13.457 | 10 | 20 | MISS T_svc | 1,245,426 | 117 (48) | 0.037 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 246,289 | 4.926 | 10 | 20 | fits | 1,245,943 | 116 (48) | 0.038 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 244,969 | 4.899 | 10 | 20 | fits | 1,244,927 | 116 (48) | 0.038 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 434,047 | 8.681 | 10 | 20 | fits | 1,434,087 | 119 (48) | 0.036 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 88,387 | 1.768 | 10 | 24 | fits | 169,183 | 48 | 0.052 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 179,650 | 3.593 | 10 | 24 | fits | 260,932 | 132 | 0.046 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 156,513 | 3.130 | 10 | 24 | fits | 237,792 | 80 | 0.049 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 139,720 | 2.794 | 10 | 24 | fits | 220,969 | 84 | 0.043 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 140,082 | 2.802 | 10 | 24 | fits | 221,334 | 83 | 0.043 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 162,183 | 3.244 | 10 | 24 | fits | 243,465 | 90 | 0.048 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 201,380 | 4.028 | 10 | 24 | fits | 217,408 | 73 | 0.044 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 134,891 | 2.698 | 10 | 24 | fits | 216,143 | 68 | 0.044 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 154,887 | 3.098 | 10 | 24 | fits | 236,166 | 72 | 0.049 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 174,536 | 3.491 | 10 | 24 | fits | 255,785 | 160 | 0.038 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 128,455 | 2.569 | 10 | 24 | fits | 209,704 | 52 | 0.045 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 150,495 | 3.010 | 10 | 24 | fits | 231,774 | 59 | 0.050 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 141,641 | 2.833 | 10 | 24 | fits | 222,890 | 69 | 0.043 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 165,116 | 3.302 | 10 | 24 | fits | 246,395 | 82 | 0.047 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 141,851 | 2.837 | 10 | 24 | fits | 223,100 | 71 | 0.043 |
| get_configuration | `aecp.get_configuration.if0` | 123,040 | 2.461 | 10 | 24 | fits | 204,289 | 47 | 0.046 |
| entity_available | `aecp.entity_available.if0` | 146,256 | 2.925 | 10 | 24 | fits | 227,538 | 58 | 0.051 |
| get_name | `aecp.get_name.if0` | 130,882 | 2.618 | 10 | 24 | fits | 212,134 | 64 | 0.045 |
| get_counters | `aecp.get_counters.if0` | 159,225 | 3.184 | 10 | 24 | fits | 240,507 | 87 | 0.050 |
| get_avb_info | `aecp.get_avb_info.if0` | 131,126 | 2.623 | 10 | 24 | fits | 212,378 | 47 | 0.044 |
| unknown_command | `aecp.unknown_command.if0` | 143,882 | 2.878 | 10 | 24 | fits | 225,164 | 54 | 0.051 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 139,672 | 2.793 | 10 | 24 | fits | 631,635 | 274 | 0.030 |
| set_name | `aecp.set_name.if0` | 214,401 | 4.288 | 10 | 24 | fits | 307,441 | 108 | 0.038 |
| lock_entity | `aecp.lock_entity.if0` | 145,009 | 2.900 | 10 | 24 | fits | 239,004 | 73 | 0.053 |
| unlock_entity | `aecp.unlock_entity.if0` | 145,033 | 2.901 | 10 | 24 | fits | 238,977 | 73 | 0.053 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 87,926 | 1.759 | 10 | 24 | fits | 169,128 | 45 | 0.052 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 179,281 | 3.586 | 10 | 24 | fits | 260,595 | 130 | 0.046 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 134,863 | 2.697 | 10 | 24 | fits | 216,147 | 71 | 0.044 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 160,939 | 3.219 | 10 | 24 | fits | 242,253 | 89 | 0.048 |
| get_configuration | `aecp.get_configuration.if1` | 122,833 | 2.457 | 10 | 24 | fits | 204,115 | 45 | 0.046 |
| entity_available | `aecp.entity_available.if1` | 146,102 | 2.922 | 10 | 24 | fits | 227,414 | 56 | 0.050 |
| get_name | `aecp.get_name.if1` | 220,615 | 4.412 | 10 | 24 | fits | 212,215 | 63 | 0.045 |
| get_counters | `aecp.get_counters.if1` | 137,419 | 2.748 | 10 | 24 | fits | 218,731 | 78 | 0.045 |
| get_avb_info | `aecp.get_avb_info.if1` | 130,919 | 2.618 | 10 | 24 | fits | 212,201 | 45 | 0.044 |
| unknown_command | `aecp.unknown_command.if1` | 144,128 | 2.883 | 10 | 24 | fits | 225,440 | 52 | 0.050 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 110,432 | 2.209 | 10 | 24 | fits | 191,692 | 56 | 0.058 |
| set_name | `aecp.set_name.if1` | 197,297 | 3.946 | 10 | 24 | fits | 334,076 | 147 | 0.043 |
| lock_entity | `aecp.lock_entity.if1` | 123,704 | 2.474 | 10 | 24 | fits | 226,792 | 85 | 0.053 |
| unlock_entity | `aecp.unlock_entity.if1` | 123,684 | 2.474 | 10 | 24 | fits | 226,707 | 85 | 0.053 |

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
