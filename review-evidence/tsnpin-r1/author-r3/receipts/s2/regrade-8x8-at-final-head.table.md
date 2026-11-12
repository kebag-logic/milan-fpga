### 8x8

31 of 129 paths and 59 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.837 (3.358) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 15.393 (35.662) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 17.162 (37.162) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 7.328 (27.328) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 18.200 (27.797) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 18.687 (27.797) | MISS T_svc | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 18.445 (27.714) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 18.893 (27.714) | MISS T_svc | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 17.484 (37.225) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 4.496 (32.453) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 15.036 (35.037) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 3.620 (23.620) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 15.087 (35.078) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 3.660 (23.651) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 17.595 (37.183) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 7.793 (27.374) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 3.406 (20.353) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 5.854 (27.414) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.892 (23.263) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 6.668 (46.260) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 6.232 (45.204) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 3.375 (19.574) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 6.568 (42.758) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 6.197 (42.758) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 1.452 (42.387) | fits | 1 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 4.959 (42.387) | fits | 3 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 8.462 (46.393) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.911 (23.283) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 5.018 (42.303) | fits | 2 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 1.763 (19.198) | fits | 2 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 10.779 (31.135) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 11.974 (24.118) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.622 (2.833) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.796 (2.833) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.498 (2.656) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.584 (2.656) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.484 (12.950) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.460 (12.950) | fits | 1 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.489 (12.146) | fits | 1 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 1.225 (12.146) | fits | 1 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.548 (2.611) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.456 (2.611) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.060 (5.510) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.378 (2.699) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.438 (4.108) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.433 (4.104) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.576 (4.246) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.571 (4.241) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.409 (4.079) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.834 (4.504) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 4.477 (8.203) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 3.149 (4.820) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.984 (4.654) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 2.565 (4.236) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.868 (4.745) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.869 (4.881) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.726 (3.396) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 1.722 (3.392) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.534 (5.204) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.531 (5.201) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.653 (4.323) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.649 (4.319) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 2.650 (4.320) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.621 (4.291) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.443 (5.113) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.521 (4.191) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 2.532 (4.202) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.747 (4.417) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 2.745 (4.416) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 3.214 (4.884) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.824 (4.494) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.789 (4.459) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 2.754 (4.424) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 2.960 (4.866) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.670 (4.340) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.723 (3.388) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 2.144 (3.815) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.279 (7.299) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.901 (6.587) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.409 (4.079) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.404 (4.075) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 3.296 (5.172) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.869 (4.879) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 7.662 (9.354) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 7.395 (11.162) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 7.509 (9.032) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 8.293 (11.893) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 8.896 (12.663) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 6.843 (8.534) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.155 (13.911) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 10.495 (14.778) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 7.886 (11.465) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 7.229 (8.920) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 7.671 (9.363) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 50.281 (55.301) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 39.365 (59.334) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 40.657 (58.497) | MISS ceiling | 2 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 20.637 (33.358) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 111.934 (116.885) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 137.688 (142.098) | MISS ceiling | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.878 (5.410) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.742 (5.485) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.605 (2.591) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.034 (3.061) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 1.122 (7.284) | fits | 1 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 1.134 (7.328) | fits | 1 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 1.730 (5.410) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.594 (5.485) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 2.530 (5.075) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 1.822 (5.958) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 12.660 | MISS T_svc | 0 acmp | 4 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 89.225 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 12.703 | MISS T_svc | 0 adp | 4 | 3 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 48.438 | MISS T_svc | 2 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 41.799 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 12.696 | MISS T_svc | 0 aecp | 4 | 3 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 296.145 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 12.686 | MISS T_svc | 0 maap | 4 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 47.746 | MISS T_svc | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 580.642 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 580.622 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 8.246 (10.051) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 8.476 (10.195) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.784 (3.784) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.411 (3.412) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 2.585 (2.586) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.250 (3.251) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.768 (7.284) | fits | 1 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.439 (6.903) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 148.909 | 24 | 639,239 (12.785) | yes | - |
| backlog-adp | 539.418 | 29 | 1,445,020 (28.900) | no | {'srp': 32} |
| backlog-adp-refill | 580.659 | 32 | 1,445,223 (28.904) | no | {'srp': 32} |
| backlog-owed | 160.683 | 25 | 415,926 (8.319) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,445,223 CPU cycles (28.904 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 639,239 (12.785 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 423,103 | 8.462 | 10 | 20 | fits | 1,163,709 | 166 (14) | 0.026 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 45,545 | 0.911 | 10 | 20 | fits | 1,164,144 | 144 (14) | 0.026 |
| LINK_UP | `adp.link_up.if0` | 24,472 | 0.489 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 61,228 | 1.225 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,997 | 1.060 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 18,908 | 0.378 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 27,402 | 0.548 | 10 | 200 | fits | 8,607 | 18 (11) | 0.137 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 22,806 | 0.456 | 10 | 200 | fits | 8,607 | 18 (11) | 0.137 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 56,103 | 1.122 | 10 | 50 | fits | 364,189 | 160 | 0.041 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 126,479 | 2.530 | 10 | 50 | fits | 131,749 | 38 | 0.065 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 82,640 | 1.653 | 10 | 50 | fits | 152,439 | 44 | 0.066 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 86,494 | 1.730 | 10 | 50 | fits | 148,035 | 65 | 0.064 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 93,879 | 1.878 | 10 | 50 | fits | 148,035 | 65 | 0.064 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 30,239 | 0.605 | 10 | 50 | fits | 129,543 | 47 | 0.059 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 56,714 | 1.134 | 10 | 50 | fits | 366,417 | 160 | 0.041 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 72,525 | 1.450 | 10 | 50 | fits | 154,305 | 44 | 0.066 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 91,088 | 1.822 | 10 | 50 | fits | 133,566 | 38 | 0.064 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 129,720 | 2.594 | 10 | 50 | fits | 149,929 | 65 | 0.065 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 137,105 | 2.742 | 10 | 50 | fits | 149,929 | 65 | 0.065 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 51,718 | 1.034 | 10 | 50 | fits | 153,049 | 54 | 0.064 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 328,407 | 6.568 | 10 | 20 | fits | 983,762 | 175 (35) | 0.030 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 309,854 | 6.197 | 10 | 20 | fits | 983,762 | 175 (35) | 0.030 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 72,624 | 1.452 | 10 | 20 | fits | 965,650 | 129 (14) | 0.029 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 247,951 | 4.959 | 10 | 20 | fits | 965,650 | 129 (14) | 0.029 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 250,886 | 5.018 | 10 | 20 | fits | 959,894 | 130 (14) | 0.029 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 88,150 | 1.763 | 10 | 20 | fits | 959,894 | 130 (14) | 0.029 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 44,614 | 0.892 | 10 | 20 | fits | 1,163,127 | 166 (35) | 0.026 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 333,388 | 6.668 | 10 | 20 | fits | 1,163,066 | 166 (35) | 0.026 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 338,405 | 6.768 | 10 | 18 | fits | 364,189 | 160 | 0.041 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 321,961 | 6.439 | 10 | 18 | fits | 345,171 | 153 | 0.039 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 189,179 | 3.784 | 10 | 18 | fits | 189,211 | 36 | 0.073 |
| malformed MRPDU discard | `srp.malformed.if0` | 129,260 | 2.585 | 10 | 18 | fits | 129,292 | 29 | 0.060 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 412,301 | 8.246 | 210 | 218 | fits | 502,572 | 149 | 0.049 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 170,574 | 3.411 | 10 | 18 | fits | 170,606 | 29 | 0.069 |
| malformed MRPDU discard | `srp.malformed.if1` | 162,521 | 3.250 | 10 | 18 | fits | 162,553 | 36 | 0.060 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 423,789 | 8.476 | 210 | 218 | fits | 509,747 | 149 | 0.048 |
| an event behind 15 others | `backlog.event.if0` | 1,031,872 | 20.637 | 10 | 200 | MISS T_svc | 639,239 | 348 | 0.063 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,514,048 | 50.281 | 10 | 20 | MISS ceiling | 299,984 | 213 | 0.044 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 635,142 | 12.703 | 10 | 200 | MISS T_svc | 635,246 | 394 | 0.062 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,089,971 | 41.799 | 10 | 200 | MISS T_svc | 422,468 | 326 | 0.054 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 633,013 | 12.660 | 10 | 20 | MISS T_svc | 635,246 | 394 | 0.062 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 2,762,398 | 55.248 | 10 | 20 | MISS ceiling | 299,984 | 213 | 0.044 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 634,805 | 12.696 | 10 | 24 | MISS T_svc | 635,246 | 394 | 0.062 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 5,730,237 | 114.605 | 10 | 24 | MISS ceiling | 246,917 | 126 | 0.039 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 634,285 | 12.686 | 10 | 50 | MISS T_svc | 635,246 | 394 | 0.062 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,089,223 | 41.784 | 10 | 50 | MISS T_svc | 422,468 | 326 | 0.054 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 2,089,191 | 41.784 | 10 | 18 | MISS ceiling | 422,468 | 326 | 0.054 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 6,892,423 | 137.848 | 10 | 18 | MISS ceiling | 154,399 | 48 | 0.066 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 1,968,238 | 39.365 | 10 | 20 | MISS ceiling | 890,962 | 393 | 0.037 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 543,952 | 10.879 | 10 | 200 | MISS T_svc | 1,124,901 | 449 | 0.032 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,385,461 | 47.709 | 10 | 200 | MISS T_svc | 890,962 | 393 | 0.037 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 544,408 | 10.888 | 10 | 20 | MISS T_svc | 1,124,901 | 449 | 0.032 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,397,494 | 87.950 | 10 | 20 | MISS ceiling | 1,058,716 | 319 | 0.031 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 546,200 | 10.924 | 10 | 24 | MISS T_svc | 1,124,901 | 449 | 0.032 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 14,783,692 | 295.674 | 10 | 24 | MISS ceiling | 1,004,887 | 232 | 0.029 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 545,680 | 10.914 | 10 | 50 | MISS T_svc | 1,124,901 | 449 | 0.032 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,387,299 | 47.746 | 10 | 50 | MISS T_svc | 890,962 | 393 | 0.037 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 26,970,043 | 539.401 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 26,969,036 | 539.381 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,032,854 | 40.657 | 10 | 20 | MISS ceiling | 978,589 | 341 | 0.035 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 543,952 | 10.879 | 10 | 200 | MISS T_svc | 1,124,901 | 449 | 0.032 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,421,907 | 48.438 | 10 | 200 | MISS T_svc | 978,589 | 341 | 0.035 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 544,408 | 10.888 | 10 | 20 | MISS T_svc | 1,124,901 | 449 | 0.032 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,419,713 | 88.394 | 10 | 20 | MISS ceiling | 978,589 | 341 | 0.035 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 546,200 | 10.924 | 10 | 24 | MISS T_svc | 1,124,901 | 449 | 0.032 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 14,807,275 | 296.145 | 10 | 24 | MISS ceiling | 1,005,077 | 232 | 0.029 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 545,680 | 10.914 | 10 | 50 | MISS T_svc | 1,124,901 | 449 | 0.032 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,369,174 | 47.383 | 10 | 50 | MISS T_svc | 872,837 | 386 | 0.036 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,032,117 | 580.642 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,031,110 | 580.622 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,596,719 | 111.934 | 10 | 20 | MISS ceiling | 262,179 | 148 | 0.041 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 5,974,383 | 119.488 | 10 | 20 | MISS ceiling | 377,656 | 193 | 0.054 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,352,123 | 127.042 | 10 | 20 | MISS ceiling | 377,777 | 193 | 0.054 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,614,218 | 132.284 | 10 | 20 | MISS ceiling | 262,179 | 148 | 0.041 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,884,384 | 137.688 | 10 | 20 | MISS ceiling | 243,164 | 78 | 0.069 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 469,582 | 9.392 | 10 | 200 | fits | 385,830 | 346 | 0.050 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 1,665,209 | 33.304 | 10 | 200 | MISS T_svc | 415,926 | 283 | 0.054 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 467,453 | 9.349 | 10 | 20 | fits | 385,830 | 346 | 0.050 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 4,461,238 | 89.225 | 10 | 20 | MISS ceiling | 406,545 | 214 | 0.054 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 469,245 | 9.385 | 10 | 24 | fits | 385,830 | 346 | 0.050 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,760,304 | 135.206 | 10 | 24 | MISS ceiling | 262,179 | 148 | 0.041 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 468,725 | 9.374 | 10 | 50 | fits | 385,830 | 346 | 0.050 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,664,461 | 33.289 | 10 | 50 | MISS T_svc | 415,926 | 283 | 0.054 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,664,429 | 33.289 | 10 | 18 | MISS ceiling | 415,926 | 283 | 0.054 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 7,340,163 | 146.803 | 10 | 18 | MISS ceiling | 183,540 | 36 | 0.067 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 922,269 | 18.445 | 10 | 20 | MISS T_svc | 1,385,720 | 208 (29) | 0.024 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 944,641 | 18.893 | 10 | 20 | MISS T_svc | 1,385,720 | 208 (29) | 0.024 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 910,021 | 18.200 | 10 | 20 | MISS T_svc | 1,389,866 | 219 (35) | 0.025 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 934,371 | 18.687 | 10 | 20 | MISS T_svc | 1,389,866 | 219 (35) | 0.025 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 311,597 | 6.232 | 10 | 20 | fits | 1,007,238 | 123 (12) | 0.022 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 168,747 | 3.375 | 10 | 20 | fits | 978,713 | 149 (12) | 0.029 |
| LINK_UP | `adp.link_up.if0` | 24,472 | 0.489 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 61,228 | 1.225 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,997 | 1.060 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 18,908 | 0.378 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| LINK_DOWN | `adp.link_down.if0` | 24,201 | 0.484 | 10 | 200 | fits | 647,484 | 58 (9) | 0.078 |
| LINK_DOWN | `adp.link_down.if1` | 273,015 | 5.460 | 10 | 200 | fits | 647,484 | 58 (9) | 0.078 |
| LINK_UP | `adp.link_up.if0` | 24,472 | 0.489 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 61,228 | 1.225 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,997 | 1.060 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 18,908 | 0.378 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| GM_CHANGE | `adp.gm_change.if0` | 24,897 | 0.498 | 10 | 200 | fits | 132,786 | 34 (11) | 0.068 |
| GM_CHANGE | `adp.gm_change.if1` | 29,219 | 0.584 | 10 | 200 | fits | 132,786 | 34 (11) | 0.068 |
| LINK_UP | `adp.link_up.if0` | 24,472 | 0.489 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 61,228 | 1.225 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,997 | 1.060 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 18,908 | 0.378 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 31,107 | 0.622 | 10 | 200 | fits | 141,659 | 73 (31) | 0.062 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 39,799 | 0.796 | 10 | 200 | fits | 141,659 | 73 (31) | 0.062 |
| LINK_UP | `adp.link_up.if0` | 24,472 | 0.489 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 61,228 | 1.225 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,997 | 1.060 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 18,908 | 0.378 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 31,107 | 0.622 | 10 | 200 | fits | 133,188 | 45 (31) | 0.064 |
| set_name | `aecp_fanout.set_name.if0` | 557,736 | 11.155 | 10 | 24 | MISS T_svc | 695,545 | 1179 | 0.046 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 375,428 | 7.509 | 10 | 24 | fits | 451,612 | 620 | 0.067 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 444,821 | 8.896 | 10 | 24 | fits | 447,577 | 587 | 0.066 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 432,309 | 8.646 | 10 | 24 | fits | 426,593 | 580 | 0.065 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 394,295 | 7.886 | 10 | 24 | fits | 401,415 | 592 | 0.069 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 383,120 | 7.662 | 10 | 24 | fits | 467,681 | 686 | 0.064 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 361,458 | 7.229 | 10 | 24 | fits | 445,981 | 679 | 0.063 |
| set_name | `aecp_fanout.set_name.if1` | 524,753 | 10.495 | 10 | 24 | MISS T_svc | 627,702 | 1133 | 0.045 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 414,657 | 8.293 | 10 | 24 | fits | 431,138 | 613 | 0.066 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 341,791 | 6.836 | 10 | 24 | fits | 427,063 | 581 | 0.065 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 342,172 | 6.843 | 10 | 24 | fits | 426,695 | 580 | 0.065 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 369,754 | 7.395 | 10 | 24 | fits | 446,207 | 680 | 0.063 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 383,575 | 7.671 | 10 | 24 | fits | 468,136 | 686 | 0.064 |
| BIND_RX | `acmp.bind_rx.if0` | 41,866 | 0.837 | 10 | 20 | fits | 167,898 | 83 (77) | 0.066 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 170,297 | 3.406 | 10 | 20 | fits | 1,017,650 | 154 (32) | 0.030 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 874,208 | 17.484 | 10 | 20 | MISS T_svc | 997,003 | 169 (47) | 0.028 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 538,954 | 10.779 | 10 | 20 | MISS T_svc | 693,306 | 204 (50) | 0.040 |
| PROBE_TX | `acmp.probe_tx.if0` | 879,757 | 17.595 | 10 | 20 | MISS T_svc | 891,261 | 161 (48) | 0.031 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 754,337 | 15.087 | 10 | 20 | MISS T_svc | 891,443 | 160 (48) | 0.031 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 858,079 | 17.162 | 10 | 20 | MISS T_svc | 995,356 | 170 (48) | 0.028 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 751,812 | 15.036 | 10 | 20 | MISS T_svc | 889,699 | 160 (48) | 0.031 |
| BIND_RX | `acmp.bind_rx.if1` | 769,670 | 15.393 | 10 | 20 | MISS T_svc | 920,354 | 190 (77) | 0.033 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 292,707 | 5.854 | 10 | 20 | fits | 1,370,681 | 187 (32) | 0.025 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 224,776 | 4.496 | 10 | 20 | fits | 1,622,662 | 401 (47) | 0.025 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 598,706 | 11.974 | 10 | 20 | MISS T_svc | 1,205,890 | 188 (50) | 0.028 |
| PROBE_TX | `acmp.probe_tx.if1` | 389,672 | 7.793 | 10 | 20 | fits | 1,368,685 | 204 (48) | 0.024 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 183,016 | 3.660 | 10 | 20 | fits | 1,182,554 | 186 (48) | 0.026 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 366,380 | 7.328 | 10 | 20 | fits | 1,366,377 | 203 (48) | 0.024 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 180,986 | 3.620 | 10 | 20 | fits | 1,181,023 | 186 (48) | 0.026 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 86,131 | 1.723 | 10 | 24 | fits | 169,390 | 49 | 0.055 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 176,689 | 3.534 | 10 | 24 | fits | 260,192 | 134 | 0.045 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 132,662 | 2.653 | 10 | 24 | fits | 216,162 | 75 | 0.045 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 137,331 | 2.747 | 10 | 24 | fits | 220,831 | 86 | 0.044 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 137,693 | 2.754 | 10 | 24 | fits | 221,196 | 85 | 0.044 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 147,992 | 2.960 | 10 | 24 | fits | 243,320 | 92 | 0.048 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 133,509 | 2.670 | 10 | 24 | fits | 217,012 | 74 | 0.045 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 132,502 | 2.650 | 10 | 24 | fits | 216,005 | 70 | 0.045 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 131,043 | 2.621 | 10 | 24 | fits | 214,543 | 67 | 0.045 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 172,147 | 3.443 | 10 | 24 | fits | 255,647 | 162 | 0.039 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 126,066 | 2.521 | 10 | 24 | fits | 209,566 | 54 | 0.046 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 126,581 | 2.532 | 10 | 24 | fits | 210,081 | 54 | 0.046 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 160,714 | 3.214 | 10 | 24 | fits | 244,214 | 78 | 0.047 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 141,199 | 2.824 | 10 | 24 | fits | 224,699 | 77 | 0.043 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 139,462 | 2.789 | 10 | 24 | fits | 222,962 | 73 | 0.043 |
| get_configuration | `aecp.get_configuration.if0` | 120,452 | 2.409 | 10 | 24 | fits | 203,952 | 49 | 0.046 |
| entity_available | `aecp.entity_available.if0` | 121,883 | 2.438 | 10 | 24 | fits | 205,386 | 53 | 0.046 |
| get_name | `aecp.get_name.if0` | 149,180 | 2.984 | 10 | 24 | fits | 232,683 | 73 | 0.050 |
| get_counters | `aecp.get_counters.if0` | 223,863 | 4.477 | 10 | 24 | fits | 220,072 | 88 | 0.046 |
| get_avb_info | `aecp.get_avb_info.if0` | 128,783 | 2.576 | 10 | 24 | fits | 212,286 | 49 | 0.045 |
| unknown_command | `aecp.unknown_command.if0` | 120,429 | 2.409 | 10 | 24 | fits | 203,932 | 49 | 0.046 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 86,312 | 1.726 | 10 | 24 | fits | 169,815 | 53 | 0.054 |
| set_name | `aecp.set_name.if0` | 213,975 | 4.279 | 10 | 24 | fits | 364,927 | 156 | 0.038 |
| lock_entity | `aecp.lock_entity.if0` | 143,393 | 2.868 | 10 | 24 | fits | 237,258 | 90 | 0.046 |
| unlock_entity | `aecp.unlock_entity.if0` | 164,778 | 3.296 | 10 | 24 | fits | 258,605 | 97 | 0.049 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 107,184 | 2.144 | 10 | 24 | fits | 190,746 | 54 | 0.058 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 176,530 | 3.531 | 10 | 24 | fits | 260,052 | 132 | 0.045 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 132,451 | 2.649 | 10 | 24 | fits | 215,973 | 73 | 0.045 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 137,257 | 2.745 | 10 | 24 | fits | 220,779 | 84 | 0.044 |
| get_configuration | `aecp.get_configuration.if1` | 141,681 | 2.834 | 10 | 24 | fits | 225,201 | 54 | 0.050 |
| entity_available | `aecp.entity_available.if1` | 121,669 | 2.433 | 10 | 24 | fits | 205,189 | 51 | 0.046 |
| get_name | `aecp.get_name.if1` | 128,271 | 2.565 | 10 | 24 | fits | 211,791 | 64 | 0.046 |
| get_counters | `aecp.get_counters.if1` | 157,461 | 3.149 | 10 | 24 | fits | 240,981 | 92 | 0.050 |
| get_avb_info | `aecp.get_avb_info.if1` | 128,554 | 2.571 | 10 | 24 | fits | 212,074 | 47 | 0.045 |
| unknown_command | `aecp.unknown_command.if1` | 120,215 | 2.404 | 10 | 24 | fits | 203,735 | 47 | 0.046 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 86,098 | 1.722 | 10 | 24 | fits | 169,618 | 51 | 0.054 |
| set_name | `aecp.set_name.if1` | 195,035 | 3.901 | 10 | 24 | fits | 329,365 | 149 | 0.038 |
| lock_entity | `aecp.lock_entity.if1` | 143,462 | 2.869 | 10 | 24 | fits | 244,058 | 109 | 0.047 |
| unlock_entity | `aecp.unlock_entity.if1` | 143,433 | 2.869 | 10 | 24 | fits | 243,965 | 109 | 0.047 |

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
