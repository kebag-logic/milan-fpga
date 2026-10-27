### 8x8

31 of 129 paths and 59 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.980 (4.171) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 16.390 (36.550) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 15.997 (35.997) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 8.485 (28.480) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 19.539 (52.771) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 20.786 (52.771) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 20.690 (29.456) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 21.914 (29.456) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 18.368 (38.245) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 9.274 (37.213) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 18.128 (38.130) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 4.713 (24.715) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 16.006 (35.999) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 4.736 (24.735) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 18.494 (38.169) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 5.087 (24.754) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 3.725 (21.149) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 3.000 (24.599) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.537 (20.490) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 1.919 (24.272) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 4.931 (22.774) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 4.212 (24.306) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 9.321 (44.672) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 8.716 (44.672) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 3.998 (47.909) | fits | 1 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 4.527 (47.909) | fits | 2 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 5.032 (24.289) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 1.625 (20.476) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 1.417 (20.792) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 4.674 (20.792) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 11.832 (32.039) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 12.938 (25.083) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.611 (2.731) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.781 (2.731) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.480 (2.516) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.545 (2.516) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.465 (12.229) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.130 (12.229) | fits | 1 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.070 (11.843) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.789 (11.843) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.751 (3.789) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.825 (2.789) | fits | 1 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.883 (6.181) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 1.246 (5.181) | fits | 1 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.459 (4.074) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.873 (4.489) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.588 (4.203) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 3.005 (4.621) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.843 (4.458) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.419 (4.034) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 3.139 (4.756) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 2.712 (4.328) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 3.004 (4.620) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 2.997 (4.614) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.955 (6.776) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.859 (4.897) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.155 (3.769) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 1.746 (3.361) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.546 (5.163) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.536 (5.153) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.666 (4.281) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.662 (4.277) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 3.082 (4.698) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 3.054 (4.670) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.877 (5.492) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.533 (4.148) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 2.543 (4.158) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 3.180 (4.795) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 3.169 (4.785) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 3.218 (4.833) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 3.257 (4.872) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.801 (4.416) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 2.766 (4.380) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 3.198 (4.814) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 3.704 (7.277) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.731 (3.338) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 2.137 (3.752) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 3.880 (6.499) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.905 (6.617) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.825 (4.440) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.416 (4.031) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.436 (4.299) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.861 (4.899) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.514 (12.123) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 9.454 (13.063) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.544 (11.982) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 8.431 (9.892) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 8.183 (9.814) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 9.069 (12.679) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 12.254 (16.545) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 12.988 (17.112) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 9.142 (12.561) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.557 (10.187) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 9.460 (13.070) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 57.072 (64.172) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 44.976 (65.338) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 52.286 (67.135) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 14.170 (27.514) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 117.744 (123.362) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 370.341 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 2.775 (6.697) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 1.443 (5.423) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 1.030 (2.943) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.613 (2.546) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.709 (6.714) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.709 (7.153) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 2.627 (6.697) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 1.295 (5.423) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 2.385 (6.675) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 1.413 (5.356) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 13.720 | MISS T_svc | 0 acmp | 4 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 102.654 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 13.762 | MISS T_svc | 0 adp | 4 | 3 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 62.698 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 46.526 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 13.756 | MISS T_svc | 0 aecp | 4 | 3 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 308.609 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 13.745 | MISS T_svc | 0 maap | 4 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 55.999 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 592.271 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 592.251 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 7.597 (9.257) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 7.746 (9.323) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.198 (3.198) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.261 (3.262) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 2.477 (2.477) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.133 (3.134) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.262 (6.714) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.744 (7.140) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 152.284 | 23 | 688,222 (13.764) | yes | - |
| backlog-adp | 545.029 | 29 | 1,439,270 (28.785) | no | {'srp': 32} |
| backlog-adp-refill | 592.288 | 31 | 1,439,211 (28.784) | no | {'srp': 32} |
| backlog-owed | 370.391 | 44 | 571,423 (11.428) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,439,270 CPU cycles (28.785 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 688,222 (13.764 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 251,595 | 5.032 | 10 | 20 | fits | 1,214,433 | 96 (14) | 0.032 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 81,227 | 1.625 | 10 | 20 | fits | 1,023,782 | 71 (14) | 0.035 |
| LINK_UP | `adp.link_up.if0` | 3,486 | 0.070 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| LINK_UP | `adp.link_up.if1` | 39,456 | 0.789 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 94,153 | 1.883 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,289 | 1.246 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 87,568 | 1.751 | 10 | 200 | fits | 7,269 | 18 (11) | 0.095 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 41,237 | 0.825 | 10 | 200 | fits | 7,269 | 18 (11) | 0.095 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 35,426 | 0.709 | 10 | 50 | fits | 335,699 | 154 | 0.024 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 119,233 | 2.385 | 10 | 50 | fits | 147,724 | 44 | 0.046 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 85,615 | 1.712 | 10 | 50 | fits | 127,608 | 38 | 0.041 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 131,356 | 2.627 | 10 | 50 | fits | 165,381 | 71 | 0.043 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 138,758 | 2.775 | 10 | 50 | fits | 165,381 | 71 | 0.043 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 51,501 | 1.030 | 10 | 50 | fits | 147,158 | 54 | 0.044 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 35,466 | 0.709 | 10 | 50 | fits | 357,637 | 160 | 0.026 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 32,418 | 0.648 | 10 | 50 | fits | 128,971 | 38 | 0.040 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 70,651 | 1.413 | 10 | 50 | fits | 128,973 | 38 | 0.040 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 64,739 | 1.295 | 10 | 50 | fits | 146,583 | 65 | 0.040 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 72,141 | 1.443 | 10 | 50 | fits | 146,583 | 65 | 0.040 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 30,642 | 0.613 | 10 | 50 | fits | 127,280 | 47 | 0.036 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 466,037 | 9.321 | 10 | 20 | fits | 1,072,043 | 119 (35) | 0.032 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 435,796 | 8.716 | 10 | 20 | fits | 1,072,043 | 119 (35) | 0.032 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 199,897 | 3.998 | 10 | 20 | fits | 1,045,508 | 73 (14) | 0.032 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 226,332 | 4.527 | 10 | 20 | fits | 1,045,508 | 73 (14) | 0.032 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 70,859 | 1.417 | 10 | 20 | fits | 1,039,618 | 74 (14) | 0.032 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 233,719 | 4.674 | 10 | 20 | fits | 1,039,618 | 74 (14) | 0.032 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 76,846 | 1.537 | 10 | 20 | fits | 1,024,514 | 93 (35) | 0.034 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 95,948 | 1.919 | 10 | 20 | fits | 1,213,619 | 96 (35) | 0.032 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 313,086 | 6.262 | 10 | 18 | fits | 335,699 | 154 | 0.024 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 337,218 | 6.744 | 10 | 18 | fits | 357,018 | 160 | 0.026 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 159,876 | 3.198 | 10 | 18 | fits | 159,908 | 29 | 0.046 |
| malformed MRPDU discard | `srp.malformed.if0` | 123,827 | 2.477 | 10 | 18 | fits | 123,859 | 29 | 0.037 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 379,842 | 7.597 | 210 | 218 | fits | 462,869 | 142 | 0.027 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 163,055 | 3.261 | 10 | 18 | fits | 163,087 | 29 | 0.044 |
| malformed MRPDU discard | `srp.malformed.if1` | 156,647 | 3.133 | 10 | 18 | fits | 156,679 | 36 | 0.042 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 387,315 | 7.746 | 210 | 218 | fits | 466,145 | 142 | 0.026 |
| an event behind 15 others | `backlog.event.if0` | 708,478 | 14.170 | 10 | 200 | MISS T_svc | 687,487 | 375 | 0.030 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,853,578 | 57.072 | 10 | 20 | MISS ceiling | 474,142 | 256 | 0.034 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 688,118 | 13.762 | 10 | 200 | MISS T_svc | 688,222 | 392 | 0.029 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,326,289 | 46.526 | 10 | 200 | MISS T_svc | 441,115 | 285 | 0.030 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 685,989 | 13.720 | 10 | 20 | MISS T_svc | 688,222 | 392 | 0.029 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,205,961 | 64.119 | 10 | 20 | MISS ceiling | 474,142 | 256 | 0.034 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 687,781 | 13.756 | 10 | 24 | MISS T_svc | 688,222 | 392 | 0.029 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,191,491 | 123.830 | 10 | 24 | MISS ceiling | 292,742 | 163 | 0.037 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 687,261 | 13.745 | 10 | 50 | MISS T_svc | 688,222 | 392 | 0.029 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,325,541 | 46.511 | 10 | 50 | MISS T_svc | 441,115 | 285 | 0.030 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,207,419 | 64.148 | 10 | 18 | MISS ceiling | 474,142 | 256 | 0.034 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,310,040 | 146.201 | 10 | 18 | MISS ceiling | 173,299 | 54 | 0.048 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,248,783 | 44.976 | 10 | 20 | MISS ceiling | 1,022,475 | 363 | 0.032 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 610,926 | 12.219 | 10 | 200 | MISS T_svc | 1,079,451 | 400 | 0.030 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,798,089 | 55.962 | 10 | 200 | MISS T_svc | 1,022,475 | 363 | 0.032 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 611,382 | 12.228 | 10 | 20 | MISS T_svc | 1,079,451 | 400 | 0.030 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 5,004,700 | 100.094 | 10 | 20 | MISS ceiling | 1,050,027 | 272 | 0.032 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 613,174 | 12.263 | 10 | 24 | MISS T_svc | 1,079,451 | 400 | 0.030 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 15,412,576 | 308.252 | 10 | 24 | MISS ceiling | 1,008,115 | 188 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 612,654 | 12.253 | 10 | 50 | MISS T_svc | 1,079,451 | 400 | 0.030 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,799,927 | 55.999 | 10 | 50 | MISS ceiling | 1,022,475 | 363 | 0.032 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,250,588 | 545.012 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,249,581 | 544.992 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,614,308 | 52.286 | 10 | 20 | MISS ceiling | 1,218,244 | 307 | 0.030 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 610,926 | 12.219 | 10 | 200 | MISS T_svc | 1,079,451 | 400 | 0.030 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 3,134,916 | 62.698 | 10 | 200 | MISS T_svc | 1,218,244 | 307 | 0.030 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 611,382 | 12.228 | 10 | 20 | MISS T_svc | 1,079,451 | 400 | 0.030 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 5,132,722 | 102.654 | 10 | 20 | MISS ceiling | 1,218,244 | 307 | 0.030 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 613,174 | 12.263 | 10 | 24 | MISS T_svc | 1,079,451 | 400 | 0.030 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,430,435 | 308.609 | 10 | 24 | MISS ceiling | 1,007,983 | 188 | 0.033 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 612,654 | 12.253 | 10 | 50 | MISS T_svc | 1,079,451 | 400 | 0.030 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,745,033 | 54.901 | 10 | 50 | MISS ceiling | 967,581 | 356 | 0.032 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,613,571 | 592.271 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,612,564 | 592.251 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,887,212 | 117.744 | 10 | 20 | MISS ceiling | 414,810 | 191 | 0.039 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,517,042 | 370.341 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,517,004 | 370.340 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,516,967 | 370.339 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,516,929 | 370.339 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 477,669 | 9.553 | 10 | 200 | fits | 469,301 | 344 | 0.028 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 1,872,899 | 37.458 | 10 | 200 | MISS T_svc | 440,873 | 261 | 0.030 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 475,540 | 9.511 | 10 | 20 | fits | 469,301 | 344 | 0.028 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 2,651,173 | 53.023 | 10 | 20 | MISS ceiling | 416,461 | 120 | 0.040 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 477,332 | 9.547 | 10 | 24 | fits | 469,301 | 344 | 0.028 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,089,013 | 141.780 | 10 | 24 | MISS ceiling | 362,417 | 169 | 0.042 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 476,812 | 9.536 | 10 | 50 | fits | 469,301 | 344 | 0.028 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,872,151 | 37.443 | 10 | 50 | MISS T_svc | 440,873 | 261 | 0.030 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 2,652,631 | 53.053 | 10 | 18 | MISS ceiling | 416,461 | 120 | 0.040 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 7,867,603 | 157.352 | 10 | 18 | MISS ceiling | 177,013 | 36 | 0.047 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 1,034,505 | 20.690 | 10 | 20 | MISS ceiling | 1,472,785 | 124 (29) | 0.029 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 1,095,697 | 21.914 | 10 | 20 | MISS ceiling | 1,472,785 | 124 (29) | 0.029 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 976,969 | 19.539 | 10 | 20 | MISS T_svc | 1,288,289 | 132 (35) | 0.031 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,039,320 | 20.786 | 10 | 20 | MISS ceiling | 1,288,289 | 132 (35) | 0.031 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 246,555 | 4.931 | 10 | 20 | fits | 1,138,702 | 71 (12) | 0.028 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 210,623 | 4.212 | 10 | 20 | fits | 1,215,300 | 96 (12) | 0.033 |
| LINK_UP | `adp.link_up.if0` | 3,486 | 0.070 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| LINK_UP | `adp.link_up.if1` | 39,456 | 0.789 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 94,153 | 1.883 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,289 | 1.246 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| LINK_DOWN | `adp.link_down.if0` | 23,266 | 0.465 | 10 | 200 | fits | 611,443 | 58 (9) | 0.035 |
| LINK_DOWN | `adp.link_down.if1` | 256,479 | 5.130 | 10 | 200 | fits | 611,443 | 58 (9) | 0.035 |
| LINK_UP | `adp.link_up.if0` | 3,486 | 0.070 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| LINK_UP | `adp.link_up.if1` | 39,456 | 0.789 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 94,153 | 1.883 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,289 | 1.246 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| GM_CHANGE | `adp.gm_change.if0` | 23,984 | 0.480 | 10 | 200 | fits | 125,800 | 34 (11) | 0.044 |
| GM_CHANGE | `adp.gm_change.if1` | 27,268 | 0.545 | 10 | 200 | fits | 125,800 | 34 (11) | 0.044 |
| LINK_UP | `adp.link_up.if0` | 3,486 | 0.070 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| LINK_UP | `adp.link_up.if1` | 39,456 | 0.789 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 94,153 | 1.883 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,289 | 1.246 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 30,529 | 0.611 | 10 | 200 | fits | 136,560 | 73 (31) | 0.043 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 39,036 | 0.781 | 10 | 200 | fits | 136,560 | 73 (31) | 0.043 |
| LINK_UP | `adp.link_up.if0` | 3,486 | 0.070 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| LINK_UP | `adp.link_up.if1` | 39,456 | 0.789 | 10 | 200 | fits | 592,168 | 304 (11) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 94,153 | 1.883 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,289 | 1.246 | 10 | 200 | fits | 135,330 | 84 (39) | 0.035 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 30,529 | 0.611 | 10 | 200 | fits | 128,277 | 45 (31) | 0.045 |
| set_name | `aecp_fanout.set_name.if0` | 612,690 | 12.254 | 10 | 24 | MISS T_svc | 700,324 | 1131 | 0.076 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 427,185 | 8.544 | 10 | 24 | fits | 473,481 | 590 | 0.107 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 409,127 | 8.183 | 10 | 24 | fits | 490,694 | 563 | 0.106 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 388,458 | 7.769 | 10 | 24 | fits | 470,014 | 556 | 0.107 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 457,085 | 9.142 | 10 | 24 | fits | 464,949 | 590 | 0.109 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 425,694 | 8.514 | 10 | 24 | fits | 488,761 | 656 | 0.104 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 427,826 | 8.557 | 10 | 24 | fits | 509,363 | 662 | 0.103 |
| set_name | `aecp_fanout.set_name.if1` | 649,402 | 12.988 | 10 | 24 | MISS T_svc | 712,373 | 1137 | 0.075 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 421,551 | 8.431 | 10 | 24 | fits | 494,596 | 596 | 0.106 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 423,754 | 8.475 | 10 | 24 | fits | 470,006 | 556 | 0.107 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 453,470 | 9.069 | 10 | 24 | fits | 470,036 | 556 | 0.107 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 472,704 | 9.454 | 10 | 24 | fits | 488,667 | 656 | 0.104 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 473,001 | 9.460 | 10 | 24 | fits | 489,244 | 656 | 0.104 |
| BIND_RX | `acmp.bind_rx.if0` | 49,000 | 0.980 | 10 | 20 | fits | 208,537 | 83 (77) | 0.037 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 186,248 | 3.725 | 10 | 20 | fits | 1,057,449 | 105 (32) | 0.032 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 918,425 | 18.368 | 10 | 20 | MISS T_svc | 1,047,409 | 120 (47) | 0.031 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 591,592 | 11.832 | 10 | 20 | MISS T_svc | 737,973 | 176 (50) | 0.036 |
| PROBE_TX | `acmp.probe_tx.if0` | 924,689 | 18.494 | 10 | 20 | MISS T_svc | 1,045,072 | 122 (48) | 0.030 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 800,282 | 16.006 | 10 | 20 | MISS T_svc | 937,377 | 118 (48) | 0.032 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 799,831 | 15.997 | 10 | 20 | MISS T_svc | 937,079 | 118 (48) | 0.033 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 906,417 | 18.128 | 10 | 20 | MISS T_svc | 1,042,837 | 121 (48) | 0.030 |
| BIND_RX | `acmp.bind_rx.if1` | 819,498 | 16.390 | 10 | 20 | MISS T_svc | 964,919 | 148 (77) | 0.033 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 150,018 | 3.000 | 10 | 20 | fits | 1,229,933 | 100 (32) | 0.033 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 463,719 | 9.274 | 10 | 20 | fits | 1,860,631 | 334 (47) | 0.025 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 646,916 | 12.938 | 10 | 20 | MISS T_svc | 1,254,164 | 118 (50) | 0.034 |
| PROBE_TX | `acmp.probe_tx.if1` | 254,331 | 5.087 | 10 | 20 | fits | 1,237,686 | 117 (48) | 0.033 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 236,823 | 4.736 | 10 | 20 | fits | 1,236,766 | 116 (48) | 0.033 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 424,268 | 8.485 | 10 | 20 | fits | 1,424,008 | 119 (48) | 0.032 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 235,673 | 4.713 | 10 | 20 | fits | 1,235,755 | 116 (48) | 0.033 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 86,574 | 1.731 | 10 | 24 | fits | 166,903 | 47 | 0.045 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 177,312 | 3.546 | 10 | 24 | fits | 258,162 | 132 | 0.039 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 133,322 | 2.666 | 10 | 24 | fits | 214,049 | 73 | 0.037 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 158,983 | 3.180 | 10 | 24 | fits | 239,748 | 91 | 0.041 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 138,288 | 2.766 | 10 | 24 | fits | 219,018 | 83 | 0.036 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 159,915 | 3.198 | 10 | 24 | fits | 240,683 | 90 | 0.041 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 185,189 | 3.704 | 10 | 24 | fits | 215,265 | 73 | 0.038 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 154,112 | 3.082 | 10 | 24 | fits | 234,880 | 75 | 0.042 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 152,715 | 3.054 | 10 | 24 | fits | 233,480 | 72 | 0.042 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 193,856 | 3.877 | 10 | 24 | fits | 274,621 | 167 | 0.036 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 126,661 | 2.533 | 10 | 24 | fits | 207,388 | 52 | 0.038 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 127,173 | 2.543 | 10 | 24 | fits | 207,900 | 52 | 0.038 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 160,880 | 3.218 | 10 | 24 | fits | 241,645 | 76 | 0.040 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 162,856 | 3.257 | 10 | 24 | fits | 243,621 | 82 | 0.040 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 140,057 | 2.801 | 10 | 24 | fits | 220,784 | 71 | 0.036 |
| get_configuration | `aecp.get_configuration.if0` | 142,128 | 2.843 | 10 | 24 | fits | 222,893 | 54 | 0.043 |
| entity_available | `aecp.entity_available.if0` | 122,957 | 2.459 | 10 | 24 | fits | 203,687 | 51 | 0.038 |
| get_name | `aecp.get_name.if0` | 150,223 | 3.004 | 10 | 24 | fits | 231,011 | 71 | 0.043 |
| get_counters | `aecp.get_counters.if0` | 156,966 | 3.139 | 10 | 24 | fits | 237,787 | 87 | 0.043 |
| get_avb_info | `aecp.get_avb_info.if0` | 129,417 | 2.588 | 10 | 24 | fits | 210,147 | 47 | 0.038 |
| unknown_command | `aecp.unknown_command.if0` | 141,249 | 2.825 | 10 | 24 | fits | 222,017 | 54 | 0.043 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 107,743 | 2.155 | 10 | 24 | fits | 188,472 | 58 | 0.050 |
| set_name | `aecp.set_name.if0` | 193,983 | 3.880 | 10 | 24 | fits | 324,973 | 114 | 0.036 |
| lock_entity | `aecp.lock_entity.if0` | 147,743 | 2.955 | 10 | 24 | fits | 215,558 | 67 | 0.042 |
| unlock_entity | `aecp.unlock_entity.if0` | 121,819 | 2.436 | 10 | 24 | fits | 214,933 | 66 | 0.041 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 106,858 | 2.137 | 10 | 24 | fits | 187,610 | 52 | 0.049 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 176,778 | 3.536 | 10 | 24 | fits | 257,660 | 130 | 0.039 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 133,112 | 2.662 | 10 | 24 | fits | 213,874 | 71 | 0.037 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 158,457 | 3.169 | 10 | 24 | fits | 239,257 | 89 | 0.041 |
| get_configuration | `aecp.get_configuration.if1` | 120,959 | 2.419 | 10 | 24 | fits | 201,719 | 45 | 0.038 |
| entity_available | `aecp.entity_available.if1` | 143,644 | 2.873 | 10 | 24 | fits | 224,442 | 56 | 0.043 |
| get_name | `aecp.get_name.if1` | 149,858 | 2.997 | 10 | 24 | fits | 230,676 | 69 | 0.043 |
| get_counters | `aecp.get_counters.if1` | 135,585 | 2.712 | 10 | 24 | fits | 216,398 | 78 | 0.038 |
| get_avb_info | `aecp.get_avb_info.if1` | 150,268 | 3.005 | 10 | 24 | fits | 231,066 | 52 | 0.042 |
| unknown_command | `aecp.unknown_command.if1` | 120,781 | 2.416 | 10 | 24 | fits | 201,541 | 45 | 0.038 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 87,279 | 1.746 | 10 | 24 | fits | 168,032 | 50 | 0.045 |
| set_name | `aecp.set_name.if1` | 195,273 | 3.905 | 10 | 24 | fits | 330,842 | 147 | 0.037 |
| lock_entity | `aecp.lock_entity.if1` | 142,957 | 2.859 | 10 | 24 | fits | 244,848 | 92 | 0.049 |
| unlock_entity | `aecp.unlock_entity.if1` | 143,061 | 2.861 | 10 | 24 | fits | 244,943 | 92 | 0.049 |

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
