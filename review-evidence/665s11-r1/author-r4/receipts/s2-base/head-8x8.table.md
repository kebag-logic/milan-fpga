### 8x8

29 of 129 paths and 57 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.003 (4.268) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 16.983 (37.136) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 1.168 (21.169) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 8.846 (28.847) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 23.203 (53.495) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 24.481 (53.495) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 21.964 (29.867) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 23.210 (29.867) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 16.784 (36.663) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 5.207 (25.097) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 16.536 (36.537) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 5.041 (25.042) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 16.589 (36.583) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 5.085 (25.079) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 12.527 (19.051) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 13.602 (25.069) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 4.488 (21.440) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 7.149 (28.758) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.845 (21.478) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 1.148 (20.840) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 1.871 (23.120) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 4.356 (24.663) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 2.795 (20.785) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 7.646 (45.370) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 3.097 (24.309) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 6.830 (44.818) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 3.752 (24.637) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 2.418 (20.791) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 2.713 (24.268) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 8.033 (45.746) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 1.358 (21.556) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 5.837 (34.235) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.202 (2.398) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.380 (2.398) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.082 (2.229) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.176 (2.229) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.064 (12.692) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.120 (12.692) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.081 (12.212) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.857 (12.212) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.072 (2.148) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 1.220 (2.230) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.852 (6.341) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 1.248 (5.341) | fits | 1 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.489 (4.144) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.484 (4.141) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.614 (4.268) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.609 (4.266) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.450 (4.105) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 3.107 (4.763) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.762 (4.419) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 3.195 (4.853) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 3.048 (4.703) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 2.604 (4.261) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 3.353 (5.235) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 3.351 (5.391) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.198 (3.852) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 2.199 (3.854) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.591 (5.247) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.585 (5.241) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.691 (4.346) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.687 (4.343) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 3.128 (4.784) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.659 (4.314) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.920 (5.576) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.999 (4.654) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 3.009 (4.665) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.784 (4.440) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 2.837 (4.875) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 2.823 (4.478) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 3.301 (4.956) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.827 (4.483) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 2.792 (4.447) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 3.243 (4.899) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 3.146 (4.801) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.756 (3.405) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 1.752 (3.406) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.332 (7.362) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.958 (6.672) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.485 (4.533) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.442 (4.098) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.917 (4.799) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 3.355 (5.391) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.367 (10.041) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 9.895 (13.624) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.206 (9.713) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 7.794 (9.301) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 8.091 (11.820) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 9.520 (13.249) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.868 (14.614) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 12.574 (16.820) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 7.808 (11.350) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 9.906 (13.635) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 9.945 (13.675) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 58.950 (64.793) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 48.176 (66.699) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 53.978 (68.436) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 14.974 (28.857) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 119.155 (122.892) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 370.587 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.988 (5.504) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.841 (7.419) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.645 (2.630) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.077 (3.091) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.754 (7.324) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.755 (7.368) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.839 (5.504) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.693 (7.419) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.403 (5.871) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 2.403 (6.935) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 14.392 | MISS T_svc | 0 acmp | 4 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 104.475 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 14.434 | MISS T_svc | 0 adp | 4 | 3 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 64.519 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 48.241 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 14.428 | MISS T_svc | 0 aecp | 4 | 3 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 315.392 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 14.417 | MISS T_svc | 0 maap | 4 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 59.364 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 593.963 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 593.943 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 7.791 (9.560) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 8.540 (10.225) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.322 (3.322) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.914 (3.914) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 3.081 (3.081) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.236 (3.237) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.817 (7.324) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.898 (7.351) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 160.899 | 25 | 721,820 (14.436) | yes | - |
| backlog-adp | 548.229 | 29 | 1,460,751 (29.215) | no | {'srp': 32} |
| backlog-adp-refill | 593.980 | 31 | 1,460,243 (29.205) | no | {'srp': 32} |
| backlog-owed | 370.638 | 41 | 627,277 (12.546) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,460,751 CPU cycles (29.215 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 721,820 (14.436 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 187,620 | 3.752 | 10 | 20 | fits | 1,231,875 | 166 (14) | 0.026 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 120,920 | 2.418 | 10 | 20 | fits | 1,039,525 | 127 (14) | 0.030 |
| LINK_UP | `adp.link_up.if0` | 4,053 | 0.081 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 42,860 | 0.857 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 92,597 | 1.852 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,420 | 1.248 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 3,607 | 0.072 | 10 | 200 | fits | 107,394 | 19 (11) | 0.062 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 61,020 | 1.220 | 10 | 200 | fits | 4,098 | 9 (11) | 0.168 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 37,698 | 0.754 | 10 | 50 | fits | 366,219 | 160 | 0.041 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 70,165 | 1.403 | 10 | 50 | fits | 154,654 | 44 | 0.070 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 38,785 | 0.776 | 10 | 50 | fits | 133,575 | 38 | 0.066 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 41,941 | 0.839 | 10 | 50 | fits | 173,564 | 71 | 0.071 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 49,375 | 0.988 | 10 | 50 | fits | 173,564 | 71 | 0.071 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 32,268 | 0.645 | 10 | 50 | fits | 131,506 | 48 | 0.060 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 37,768 | 0.755 | 10 | 50 | fits | 368,422 | 160 | 0.041 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 120,166 | 2.403 | 10 | 50 | fits | 156,561 | 44 | 0.069 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 87,270 | 1.745 | 10 | 50 | fits | 135,048 | 38 | 0.065 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 134,635 | 2.693 | 10 | 50 | fits | 175,342 | 71 | 0.070 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 142,069 | 2.841 | 10 | 50 | fits | 175,342 | 71 | 0.070 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 53,834 | 1.077 | 10 | 50 | fits | 154,542 | 54 | 0.064 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 139,761 | 2.795 | 10 | 20 | fits | 1,039,254 | 149 (35) | 0.029 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 382,293 | 7.646 | 10 | 20 | fits | 1,229,236 | 166 (35) | 0.026 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 154,848 | 3.097 | 10 | 20 | fits | 1,215,475 | 143 (14) | 0.026 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 341,522 | 6.830 | 10 | 20 | fits | 1,025,426 | 126 (14) | 0.029 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 135,662 | 2.713 | 10 | 20 | fits | 1,213,416 | 144 (14) | 0.026 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 401,667 | 8.033 | 10 | 20 | fits | 1,073,883 | 152 (14) | 0.028 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 92,232 | 1.845 | 10 | 20 | fits | 1,073,883 | 152 (35) | 0.028 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 57,398 | 1.148 | 10 | 20 | fits | 1,042,009 | 149 (35) | 0.029 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 340,840 | 6.817 | 10 | 18 | fits | 366,219 | 160 | 0.041 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 344,906 | 6.898 | 10 | 18 | fits | 367,542 | 160 | 0.041 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 166,090 | 3.322 | 10 | 18 | fits | 166,122 | 29 | 0.069 |
| malformed MRPDU discard | `srp.malformed.if0` | 154,041 | 3.081 | 10 | 18 | fits | 154,073 | 36 | 0.062 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 389,552 | 7.791 | 210 | 218 | fits | 477,997 | 142 | 0.045 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 195,690 | 3.914 | 10 | 18 | fits | 195,722 | 36 | 0.070 |
| malformed MRPDU discard | `srp.malformed.if1` | 161,807 | 3.236 | 10 | 18 | fits | 161,839 | 36 | 0.059 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 426,997 | 8.540 | 210 | 218 | fits | 511,255 | 149 | 0.046 |
| an event behind 15 others | `backlog.event.if0` | 748,703 | 14.974 | 10 | 200 | MISS T_svc | 721,049 | 377 | 0.057 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,947,480 | 58.950 | 10 | 20 | MISS ceiling | 413,657 | 219 | 0.037 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 721,716 | 14.434 | 10 | 200 | MISS T_svc | 721,820 | 394 | 0.056 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,412,057 | 48.241 | 10 | 200 | MISS T_svc | 448,236 | 287 | 0.038 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 719,587 | 14.392 | 10 | 20 | MISS T_svc | 721,820 | 394 | 0.056 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,237,014 | 64.740 | 10 | 20 | MISS ceiling | 413,657 | 219 | 0.037 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 721,379 | 14.428 | 10 | 24 | MISS T_svc | 721,820 | 394 | 0.056 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,239,449 | 124.789 | 10 | 24 | MISS ceiling | 248,990 | 126 | 0.040 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 720,859 | 14.417 | 10 | 50 | MISS T_svc | 721,820 | 394 | 0.056 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,411,309 | 48.226 | 10 | 50 | MISS T_svc | 448,236 | 287 | 0.038 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,575,167 | 71.503 | 10 | 18 | MISS ceiling | 336,695 | 171 | 0.053 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,729,318 | 154.586 | 10 | 18 | MISS ceiling | 179,053 | 54 | 0.067 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,408,782 | 48.176 | 10 | 20 | MISS ceiling | 1,164,731 | 403 | 0.032 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 621,710 | 12.434 | 10 | 200 | MISS T_svc | 989,990 | 427 | 0.034 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,966,361 | 59.327 | 10 | 200 | MISS T_svc | 1,164,731 | 403 | 0.032 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 622,166 | 12.443 | 10 | 20 | MISS T_svc | 989,990 | 427 | 0.034 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 5,201,823 | 104.036 | 10 | 20 | MISS ceiling | 1,170,947 | 319 | 0.029 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 623,958 | 12.479 | 10 | 24 | MISS T_svc | 989,990 | 427 | 0.034 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 15,747,778 | 314.956 | 10 | 24 | MISS ceiling | 1,021,059 | 232 | 0.029 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 623,438 | 12.469 | 10 | 50 | MISS T_svc | 989,990 | 427 | 0.034 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,968,199 | 59.364 | 10 | 50 | MISS ceiling | 1,164,731 | 403 | 0.032 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,410,587 | 548.212 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,409,580 | 548.192 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,698,877 | 53.978 | 10 | 20 | MISS ceiling | 1,126,577 | 341 | 0.031 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 621,710 | 12.434 | 10 | 200 | MISS T_svc | 989,990 | 427 | 0.034 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 3,225,964 | 64.519 | 10 | 200 | MISS T_svc | 1,126,577 | 341 | 0.031 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 622,166 | 12.443 | 10 | 20 | MISS T_svc | 989,990 | 427 | 0.034 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 5,223,770 | 104.475 | 10 | 20 | MISS ceiling | 1,126,577 | 341 | 0.031 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 623,958 | 12.479 | 10 | 24 | MISS T_svc | 989,990 | 427 | 0.034 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,769,607 | 315.392 | 10 | 24 | MISS ceiling | 1,021,210 | 232 | 0.029 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 623,438 | 12.469 | 10 | 50 | MISS T_svc | 989,990 | 427 | 0.034 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,912,561 | 58.251 | 10 | 50 | MISS ceiling | 1,109,093 | 396 | 0.032 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,698,140 | 593.963 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,697,133 | 593.943 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,957,753 | 119.155 | 10 | 20 | MISS ceiling | 422,612 | 193 | 0.049 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,529,359 | 370.587 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,529,321 | 370.586 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,529,284 | 370.586 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,529,246 | 370.585 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 487,810 | 9.756 | 10 | 200 | fits | 485,561 | 346 | 0.042 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 2,165,702 | 43.314 | 10 | 200 | MISS T_svc | 549,610 | 302 | 0.044 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 485,681 | 9.714 | 10 | 20 | fits | 485,561 | 346 | 0.042 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,034,394 | 60.688 | 10 | 20 | MISS ceiling | 401,270 | 122 | 0.048 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 487,473 | 9.749 | 10 | 24 | fits | 485,561 | 346 | 0.042 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,183,817 | 143.676 | 10 | 24 | MISS ceiling | 297,896 | 146 | 0.047 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 486,953 | 9.739 | 10 | 50 | fits | 485,561 | 346 | 0.042 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,164,954 | 43.299 | 10 | 50 | MISS T_svc | 549,610 | 302 | 0.044 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,615,312 | 32.306 | 10 | 18 | MISS ceiling | 627,277 | 345 | 0.051 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 7,836,443 | 156.729 | 10 | 18 | MISS ceiling | 225,252 | 54 | 0.068 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 1,098,181 | 21.964 | 10 | 20 | MISS ceiling | 1,493,357 | 208 (29) | 0.024 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 1,160,487 | 23.210 | 10 | 20 | MISS ceiling | 1,493,357 | 208 (29) | 0.024 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,160,169 | 23.203 | 10 | 20 | MISS ceiling | 1,306,755 | 202 (35) | 0.026 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,224,058 | 24.481 | 10 | 20 | MISS ceiling | 1,306,755 | 202 (35) | 0.026 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 93,544 | 1.871 | 10 | 20 | fits | 1,156,013 | 127 (12) | 0.025 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 217,790 | 4.356 | 10 | 20 | fits | 1,233,151 | 166 (12) | 0.027 |
| LINK_UP | `adp.link_up.if0` | 4,053 | 0.081 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 42,860 | 0.857 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 92,597 | 1.852 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,420 | 1.248 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| LINK_DOWN | `adp.link_down.if0` | 3,179 | 0.064 | 10 | 200 | fits | 634,591 | 52 (9) | 0.081 |
| LINK_DOWN | `adp.link_down.if1` | 255,987 | 5.120 | 10 | 200 | fits | 634,591 | 52 (9) | 0.081 |
| LINK_UP | `adp.link_up.if0` | 4,053 | 0.081 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 42,860 | 0.857 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 92,597 | 1.852 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,420 | 1.248 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| GM_CHANGE | `adp.gm_change.if0` | 4,110 | 0.082 | 10 | 200 | fits | 111,459 | 28 (11) | 0.065 |
| GM_CHANGE | `adp.gm_change.if1` | 8,825 | 0.176 | 10 | 200 | fits | 111,459 | 28 (11) | 0.065 |
| LINK_UP | `adp.link_up.if0` | 4,053 | 0.081 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 42,860 | 0.857 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 92,597 | 1.852 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,420 | 1.248 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 10,113 | 0.202 | 10 | 200 | fits | 119,885 | 67 (31) | 0.056 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 18,979 | 0.380 | 10 | 200 | fits | 119,885 | 67 (31) | 0.056 |
| LINK_UP | `adp.link_up.if0` | 4,053 | 0.081 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 42,860 | 0.857 | 10 | 200 | fits | 610,615 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 92,597 | 1.852 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 62,420 | 1.248 | 10 | 200 | fits | 141,793 | 84 (39) | 0.061 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 10,113 | 0.202 | 10 | 200 | fits | 111,240 | 39 (31) | 0.057 |
| set_name | `aecp_fanout.set_name.if0` | 593,383 | 11.868 | 10 | 24 | MISS T_svc | 730,711 | 1179 | 0.041 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 410,314 | 8.206 | 10 | 24 | fits | 485,634 | 620 | 0.057 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 376,095 | 7.522 | 10 | 24 | fits | 459,790 | 580 | 0.054 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 404,552 | 8.091 | 10 | 24 | fits | 459,316 | 580 | 0.054 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 390,402 | 7.808 | 10 | 24 | fits | 435,851 | 592 | 0.057 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 418,336 | 8.367 | 10 | 24 | fits | 502,069 | 686 | 0.054 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 495,293 | 9.906 | 10 | 24 | fits | 501,442 | 686 | 0.054 |
| set_name | `aecp_fanout.set_name.if1` | 628,723 | 12.574 | 10 | 24 | MISS T_svc | 660,860 | 1132 | 0.039 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 389,683 | 7.794 | 10 | 24 | fits | 465,041 | 613 | 0.055 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 467,998 | 9.360 | 10 | 24 | fits | 460,698 | 580 | 0.054 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 476,003 | 9.520 | 10 | 24 | fits | 460,138 | 580 | 0.054 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 494,743 | 9.895 | 10 | 24 | fits | 479,463 | 679 | 0.052 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 497,231 | 9.945 | 10 | 24 | fits | 481,261 | 679 | 0.052 |
| BIND_RX | `acmp.bind_rx.if0` | 50,149 | 1.003 | 10 | 20 | fits | 213,410 | 83 (77) | 0.051 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 224,396 | 4.488 | 10 | 20 | fits | 1,071,983 | 154 (32) | 0.030 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 839,182 | 16.784 | 10 | 20 | MISS T_svc | 954,791 | 159 (47) | 0.030 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 67,910 | 1.358 | 10 | 20 | fits | 1,077,792 | 172 (50) | 0.029 |
| PROBE_TX | `acmp.probe_tx.if0` | 626,343 | 12.527 | 10 | 20 | MISS T_svc | 952,528 | 161 (48) | 0.031 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 829,439 | 16.589 | 10 | 20 | MISS T_svc | 952,211 | 160 (48) | 0.030 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 58,380 | 1.168 | 10 | 20 | fits | 1,058,434 | 170 (48) | 0.028 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 826,813 | 16.536 | 10 | 20 | MISS T_svc | 950,381 | 160 (48) | 0.030 |
| BIND_RX | `acmp.bind_rx.if1` | 849,126 | 16.983 | 10 | 20 | MISS T_svc | 979,915 | 190 (77) | 0.031 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 357,456 | 7.149 | 10 | 20 | fits | 1,437,923 | 187 (32) | 0.025 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 260,371 | 5.207 | 10 | 20 | fits | 1,254,827 | 185 (47) | 0.027 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 291,838 | 5.837 | 10 | 20 | fits | 1,711,754 | 404 (50) | 0.026 |
| PROBE_TX | `acmp.probe_tx.if1` | 680,116 | 13.602 | 10 | 20 | MISS T_svc | 1,253,458 | 187 (48) | 0.027 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 254,235 | 5.085 | 10 | 20 | fits | 1,253,954 | 186 (48) | 0.027 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 442,282 | 8.846 | 10 | 20 | fits | 1,442,336 | 203 (48) | 0.025 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 252,073 | 5.041 | 10 | 20 | fits | 1,252,110 | 186 (48) | 0.027 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 87,782 | 1.756 | 10 | 24 | fits | 170,257 | 49 | 0.052 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 179,571 | 3.591 | 10 | 24 | fits | 262,358 | 134 | 0.046 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 134,534 | 2.691 | 10 | 24 | fits | 217,318 | 75 | 0.044 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 139,216 | 2.784 | 10 | 24 | fits | 222,000 | 86 | 0.043 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 139,578 | 2.792 | 10 | 24 | fits | 222,365 | 85 | 0.043 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 162,162 | 3.243 | 10 | 24 | fits | 244,949 | 92 | 0.048 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 157,278 | 3.146 | 10 | 24 | fits | 240,065 | 81 | 0.049 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 156,401 | 3.128 | 10 | 24 | fits | 239,188 | 77 | 0.049 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 132,928 | 2.659 | 10 | 24 | fits | 215,712 | 67 | 0.044 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 196,016 | 3.920 | 10 | 24 | fits | 278,800 | 169 | 0.043 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 149,941 | 2.999 | 10 | 24 | fits | 232,725 | 61 | 0.050 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 150,443 | 3.009 | 10 | 24 | fits | 233,227 | 61 | 0.050 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 141,140 | 2.823 | 10 | 24 | fits | 223,924 | 71 | 0.042 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 165,027 | 3.301 | 10 | 24 | fits | 247,811 | 84 | 0.047 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 141,347 | 2.827 | 10 | 24 | fits | 224,131 | 73 | 0.042 |
| get_configuration | `aecp.get_configuration.if0` | 122,515 | 2.450 | 10 | 24 | fits | 205,261 | 49 | 0.045 |
| entity_available | `aecp.entity_available.if0` | 124,433 | 2.489 | 10 | 24 | fits | 207,182 | 53 | 0.045 |
| get_name | `aecp.get_name.if0` | 152,417 | 3.048 | 10 | 24 | fits | 235,157 | 73 | 0.050 |
| get_counters | `aecp.get_counters.if0` | 138,111 | 2.762 | 10 | 24 | fits | 220,934 | 87 | 0.045 |
| get_avb_info | `aecp.get_avb_info.if0` | 130,676 | 2.614 | 10 | 24 | fits | 213,416 | 49 | 0.044 |
| unknown_command | `aecp.unknown_command.if0` | 124,252 | 2.485 | 10 | 24 | fits | 226,646 | 56 | 0.051 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 109,913 | 2.198 | 10 | 24 | fits | 192,603 | 60 | 0.057 |
| set_name | `aecp.set_name.if0` | 216,596 | 4.332 | 10 | 24 | fits | 368,092 | 156 | 0.038 |
| lock_entity | `aecp.lock_entity.if0` | 167,632 | 3.353 | 10 | 24 | fits | 261,763 | 97 | 0.050 |
| unlock_entity | `aecp.unlock_entity.if0` | 145,838 | 2.917 | 10 | 24 | fits | 239,931 | 90 | 0.045 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 87,584 | 1.752 | 10 | 24 | fits | 170,305 | 47 | 0.052 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 179,261 | 3.585 | 10 | 24 | fits | 262,067 | 132 | 0.046 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 134,325 | 2.687 | 10 | 24 | fits | 217,131 | 73 | 0.044 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 141,848 | 2.837 | 10 | 24 | fits | 243,763 | 91 | 0.048 |
| get_configuration | `aecp.get_configuration.if1` | 155,348 | 3.107 | 10 | 24 | fits | 238,174 | 75 | 0.052 |
| entity_available | `aecp.entity_available.if1` | 124,221 | 2.484 | 10 | 24 | fits | 207,047 | 51 | 0.045 |
| get_name | `aecp.get_name.if1` | 130,224 | 2.604 | 10 | 24 | fits | 213,041 | 64 | 0.045 |
| get_counters | `aecp.get_counters.if1` | 159,744 | 3.195 | 10 | 24 | fits | 242,644 | 92 | 0.050 |
| get_avb_info | `aecp.get_avb_info.if1` | 130,464 | 2.609 | 10 | 24 | fits | 213,281 | 47 | 0.044 |
| unknown_command | `aecp.unknown_command.if1` | 122,101 | 2.442 | 10 | 24 | fits | 204,918 | 47 | 0.045 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 109,925 | 2.199 | 10 | 24 | fits | 192,692 | 58 | 0.057 |
| set_name | `aecp.set_name.if1` | 197,884 | 3.958 | 10 | 24 | fits | 333,620 | 149 | 0.038 |
| lock_entity | `aecp.lock_entity.if1` | 167,539 | 3.351 | 10 | 24 | fits | 269,530 | 116 | 0.050 |
| unlock_entity | `aecp.unlock_entity.if1` | 167,764 | 3.355 | 10 | 24 | fits | 269,541 | 116 | 0.050 |

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
