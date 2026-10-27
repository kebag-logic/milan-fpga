### 8x8

111 of 125 paths and 151 of 178 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 20.230 (43.809) | MISS ceiling | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 9.192 (56.712) | fits | 1 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 5.750 (58.321) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 55.925 (150.121) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 60.539 (150.121) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 56.817 (103.644) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 61.050 (103.644) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 38.427 (66.552) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 36.602 (111.247) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 34.662 (135.597) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 33.259 (94.538) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 32.205 (48.832) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 19.081 (63.134) | MISS T_svc | 1 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 13.277 (35.091) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 34.811 (56.739) | MISS ceiling | 1 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 34.137 (106.649) | MISS ceiling | 1 events | 1 | 1 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 35.630 (102.515) | MISS ceiling | 4 events | 1 | 1 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 31.134 (101.490) | MISS ceiling | 4 events | 1 | 1 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 46.460 (93.577) | MISS ceiling | 4 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 30.048 (142.422) | MISS ceiling | 2 events | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 32.696 (142.422) | MISS ceiling | 4 events | 1 | 1 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 36.948 (95.059) | MISS ceiling | 4 events | 1 | 1 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 35.452 (95.059) | MISS ceiling | 6 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 39.686 (137.818) | MISS ceiling | 3 events | 1 | 1 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 26.905 (72.647) | MISS ceiling | 2 events | 1 | 1 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 26.770 (104.476) | MISS ceiling | 3 events | 1 | 1 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 26.511 (104.476) | MISS ceiling | 3 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 5.410 (66.552) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 15.322 (37.292) | MISS T_svc | 0 adp | 2 | 2 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 16.020 (37.292) | MISS T_svc | 1 adp | 1 | 1 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 11.364 (37.478) | MISS T_svc | 1 events | 1 | 1 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 12.324 (37.478) | MISS T_svc | 1 events | 1 | 1 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 73.601 (139.513) | MISS T_svc | 1 events | 1 | 1 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 108.378 (139.513) | MISS T_svc | 1 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 4.868 (61.663) | fits | 1 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 10.922 (61.663) | MISS T_svc | 1 events | 5 | 5 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 5.398 (27.039) | fits | 1 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 5.858 (9.448) | fits | 2 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 6.873 (28.460) | fits | 1 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 4.359 (28.460) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 23.381 (43.382) | MISS T_svc | 0 aecp | 1 | 1 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 27.050 (46.593) | MISS ceiling | 0 aecp | 1 | 1 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 26.959 (46.960) | MISS ceiling | 0 aecp | 1 | 1 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 26.977 (46.977) | MISS ceiling | 0 aecp | 1 | 1 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 26.579 (46.580) | MISS ceiling | 0 aecp | 1 | 1 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 50.537 (101.748) | MISS ceiling | 0 aecp | 1 | 1 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 24.096 (44.097) | MISS ceiling | 0 aecp | 1 | 1 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 27.361 (47.362) | MISS ceiling | 0 aecp | 1 | 1 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 27.164 (47.165) | MISS ceiling | 0 aecp | 1 | 1 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 23.992 (43.992) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 24.160 (44.493) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 13.167 (35.710) | MISS T_svc | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 32.035 (52.035) | MISS ceiling | 0 aecp | 1 | 1 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 25.105 (45.106) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 24.496 (44.585) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 24.567 (44.568) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 23.450 (43.371) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 26.969 (46.970) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 53.863 (105.188) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 27.525 (43.742) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 32.531 (52.532) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 26.935 (46.935) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 17.171 (37.092) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 23.792 (43.872) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 11.247 (59.896) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 23.831 (43.911) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 27.152 (47.153) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 23.924 (43.925) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 27.076 (47.076) | MISS ceiling | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 23.862 (43.863) | MISS T_svc | 0 aecp | 1 | 1 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 11.403 (60.053) | MISS T_svc | 0 aecp | 1 | 1 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 22.761 (38.412) | MISS T_svc | 0 aecp | 1 | 1 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 26.741 (45.613) | MISS ceiling | 0 aecp | 1 | 1 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 26.007 (49.374) | MISS ceiling | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 26.075 (49.697) | MISS ceiling | 0 aecp | 1 | 1 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 26.359 (46.359) | MISS ceiling | 0 aecp | 1 | 1 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 23.180 (43.181) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 11.102 (29.966) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 12.508 (31.161) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 63.900 (83.478) | MISS ceiling | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 64.025 (112.792) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 67.376 (85.829) | MISS ceiling | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 67.273 (86.630) | MISS ceiling | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 63.201 (83.857) | MISS ceiling | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 64.588 (85.244) | MISS ceiling | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 66.919 (88.853) | MISS ceiling | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 67.200 (88.285) | MISS ceiling | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 65.863 (86.326) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 62.555 (82.558) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 92.810 (196.878) | MISS ceiling | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 379.610 (400.339) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 193.083 (264.261) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 301.705 (380.670) | MISS ceiling | 8 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 122.977 (214.302) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 460.817 (488.504) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 598.263 (625.953) | MISS ceiling | 11 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 6.383 (24.069) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 10.635 (45.533) | MISS T_svc | 1 events | 1 | 1 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 20.438 (38.674) | MISS T_svc | 0 maap | 1 | 1 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 6.640 (17.955) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 8.979 (38.518) | fits | 1 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 59.835 (149.940) | MISS ceiling | 0 events | 1 | 1 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 5.980 (24.069) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 10.232 (45.533) | MISS T_svc | 1 events | 1 | 1 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 12.636 (39.910) | MISS T_svc | 1 events | 2 | 1 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 10.085 (40.092) | MISS T_svc | 1 events | 2 | 2 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 77.254 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 400.281 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 77.296 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 337.259 | MISS ceiling | 8 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 272.706 | MISS ceiling | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 77.290 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | at least 841.695 | STARVED: never released | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 77.279 | MISS ceiling | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 272.691 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 841.690 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-owed.service.srp.last.if1` (backlog-owed) | at least 860.009 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 48.729 (79.156) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 42.770 (61.433) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 39.467 (47.634) | MISS ceiling | 0 srp | 1 | 1 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 46.451 (53.038) | MISS ceiling | 0 srp | 1 | 1 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 14.810 (25.342) | MISS T_svc | 0 srp | 1 | 1 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 25.539 (29.088) | MISS ceiling | 0 srp | 1 | 1 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 32.282 (38.518) | MISS ceiling | 1 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 50.808 (70.360) | MISS ceiling | 0 events | 1 | 1 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 800.001 | 18 | 4,639,759 (92.795) | no | {'srp': 28} |
| backlog-adp | 693.136 | 12 | 4,938,228 (98.765) | no | {'aecp': 4, 'srp': 32} |
| backlog-adp-refill | 841.707 | 15 | 4,718,054 (94.361) | no | {'aecp': 1, 'srp': 32} |
| backlog-owed | 860.053 | 21 | 4,756,879 (95.138) | no | {'srp': 27} |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 1,984,296 | 39.686 | 10 | 20 | MISS ceiling | 4,160,526 | 303 (14) | 0.026 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 1,345,248 | 26.905 | 10 | 20 | MISS ceiling | 1,201,158 | 39 (14) | 0.030 |
| LINK_UP | `adp.link_up.if0` | 243,400 | 4.868 | 10 | 200 | fits | 3,083,161 | 316 (11) | 0.033 |
| LINK_UP | `adp.link_up.if1` | 546,076 | 10.922 | 10 | 200 | MISS T_svc | 3,083,161 | 316 (11) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 343,650 | 6.873 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 217,945 | 4.359 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 269,905 | 5.398 | 10 | 200 | fits | 472,382 | 30 (11) | 0.092 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 292,918 | 5.858 | 10 | 200 | fits | 472,382 | 30 (11) | 0.092 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 448,969 | 8.979 | 10 | 50 | fits | 1,925,879 | 166 | 0.037 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 631,781 | 12.636 | 10 | 50 | MISS T_svc | 1,118,407 | 50 | 0.058 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 187,238 | 3.745 | 10 | 50 | fits | 1,093,948 | 49 | 0.057 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 298,981 | 5.980 | 10 | 50 | fits | 1,203,466 | 76 | 0.057 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 319,152 | 6.383 | 10 | 50 | fits | 1,203,466 | 76 | 0.057 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 1,021,877 | 20.438 | 10 | 50 | MISS T_svc | 1,053,946 | 60 | 0.054 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 2,991,750 | 59.835 | 10 | 50 | MISS ceiling | 4,307,306 | 200 | 0.049 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 504,024 | 10.080 | 10 | 50 | MISS T_svc | 1,116,355 | 50 | 0.057 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 504,264 | 10.085 | 10 | 50 | MISS T_svc | 1,281,119 | 56 | 0.059 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 511,582 | 10.232 | 10 | 50 | MISS T_svc | 1,393,331 | 83 | 0.059 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 531,753 | 10.635 | 10 | 50 | MISS T_svc | 1,393,331 | 83 | 0.059 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 331,977 | 6.640 | 10 | 50 | fits | 897,735 | 53 | 0.051 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 1,502,403 | 30.048 | 10 | 20 | MISS ceiling | 4,374,812 | 329 (35) | 0.027 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 1,634,823 | 32.696 | 10 | 20 | MISS ceiling | 4,374,812 | 329 (35) | 0.027 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 1,847,401 | 36.948 | 10 | 20 | MISS ceiling | 2,318,709 | 64 (14) | 0.039 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 1,772,576 | 35.452 | 10 | 20 | MISS ceiling | 2,318,709 | 64 (14) | 0.039 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 1,338,479 | 26.770 | 10 | 20 | MISS ceiling | 2,815,839 | 94 (14) | 0.030 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 1,325,529 | 26.511 | 10 | 20 | MISS ceiling | 2,815,839 | 94 (14) | 0.030 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 1,706,836 | 34.137 | 10 | 20 | MISS ceiling | 2,623,180 | 87 (35) | 0.033 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 1,781,501 | 35.630 | 10 | 20 | MISS ceiling | 2,632,693 | 87 (35) | 0.033 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 1,614,086 | 32.282 | 10 | 18 | MISS ceiling | 1,925,879 | 166 | 0.037 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 2,540,403 | 50.808 | 10 | 18 | MISS ceiling | 3,517,994 | 147 | 0.045 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 1,973,359 | 39.467 | 10 | 18 | MISS ceiling | 1,498,024 | 41 | 0.063 |
| malformed MRPDU discard | `srp.malformed.if0` | 740,483 | 14.810 | 10 | 18 | MISS T_svc | 1,267,124 | 47 | 0.054 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 2,436,450 | 48.729 | 210 | 218 | fits | 3,054,009 | 154 | 0.043 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 2,322,530 | 46.451 | 10 | 18 | MISS ceiling | 2,651,885 | 76 | 0.059 |
| malformed MRPDU discard | `srp.malformed.if1` | 1,276,950 | 25.539 | 10 | 18 | MISS ceiling | 1,454,420 | 53 | 0.051 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 2,138,511 | 42.770 | 210 | 218 | fits | 3,071,629 | 154 | 0.042 |
| an event behind 15 others | `backlog.event.if0` | 6,148,832 | 122.977 | 10 | 200 | MISS T_svc | 4,639,759 | 375 | 0.046 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 18,980,480 | 379.610 | 10 | 20 | MISS ceiling | 2,781,595 | 258 | 0.042 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 3,864,814 | 77.296 | 10 | 200 | MISS T_svc | 3,865,160 | 392 | 0.043 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 13,635,294 | 272.706 | 10 | 200 | MISS ceiling | 2,920,858 | 326 | 0.041 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 3,862,685 | 77.254 | 10 | 20 | MISS ceiling | 3,865,160 | 392 | 0.043 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 20,014,063 | 400.281 | 10 | 20 | MISS ceiling | 2,781,595 | 258 | 0.042 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 3,864,477 | 77.290 | 10 | 24 | MISS ceiling | 3,865,160 | 392 | 0.043 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 36,144,448 | 722.889 | 10 | 24 | MISS ceiling | 1,470,112 | 142 | 0.042 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 3,863,957 | 77.279 | 10 | 50 | MISS ceiling | 3,865,160 | 392 | 0.043 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 13,634,546 | 272.691 | 10 | 50 | MISS ceiling | 2,920,858 | 326 | 0.041 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 37,859,867 | 757.197 | 10 | 18 | MISS ceiling | 1,715,679 | 68 | 0.064 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 39,997,865 | 799.957 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 9,654,151 | 193.083 | 10 | 20 | MISS ceiling | 4,938,228 | 570 | 0.030 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 2,912,711 | 58.254 | 10 | 200 | MISS T_svc | 3,085,506 | 391 | 0.033 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 13,039,947 | 260.799 | 10 | 200 | MISS ceiling | 4,938,228 | 570 | 0.030 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 2,913,167 | 58.263 | 10 | 20 | MISS ceiling | 3,085,506 | 391 | 0.033 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 18,776,370 | 375.527 | 10 | 20 | MISS ceiling | 2,867,987 | 260 | 0.038 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 2,914,959 | 58.299 | 10 | 24 | MISS ceiling | 3,085,506 | 391 | 0.033 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 34,656,216 | 693.124 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 2,914,439 | 58.289 | 10 | 50 | MISS ceiling | 3,085,506 | 391 | 0.033 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 13,041,785 | 260.836 | 10 | 50 | MISS ceiling | 4,938,228 | 570 | 0.030 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 34,655,956 | 693.119 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 34,654,949 | 693.099 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,085,233 | 301.705 | 10 | 20 | MISS ceiling | 3,108,541 | 292 | 0.036 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 2,912,711 | 58.254 | 10 | 200 | MISS T_svc | 3,085,506 | 391 | 0.033 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 16,862,948 | 337.259 | 10 | 200 | MISS ceiling | 3,108,541 | 292 | 0.036 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 2,913,167 | 58.263 | 10 | 20 | MISS ceiling | 3,085,506 | 391 | 0.033 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 18,860,754 | 377.215 | 10 | 20 | MISS ceiling | 3,108,541 | 292 | 0.036 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 2,914,959 | 58.299 | 10 | 24 | MISS ceiling | 3,085,506 | 391 | 0.033 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 42,084,756 | 841.695 | 10 | 24 | STARVED: never released | 0 | - | 0.000 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 2,914,439 | 58.289 | 10 | 50 | MISS ceiling | 3,085,506 | 391 | 0.033 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 12,821,611 | 256.432 | 10 | 50 | MISS ceiling | 4,718,054 | 563 | 0.030 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 42,084,496 | 841.690 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 42,083,489 | 841.670 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 23,040,857 | 460.817 | 10 | 20 | MISS ceiling | 1,638,130 | 164 | 0.038 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 24,838,750 | 496.775 | 10 | 20 | MISS ceiling | 1,797,931 | 170 | 0.040 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 26,476,932 | 529.539 | 10 | 20 | MISS ceiling | 1,638,219 | 164 | 0.038 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 28,274,941 | 565.499 | 10 | 20 | MISS ceiling | 1,798,047 | 170 | 0.040 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 29,913,127 | 598.263 | 10 | 20 | MISS ceiling | 1,638,223 | 164 | 0.038 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 2,316,999 | 46.340 | 10 | 200 | MISS T_svc | 2,278,050 | 344 | 0.036 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 12,444,351 | 248.887 | 10 | 200 | MISS ceiling | 3,089,796 | 323 | 0.038 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 2,314,870 | 46.297 | 10 | 20 | MISS ceiling | 2,278,050 | 344 | 0.036 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 18,188,937 | 363.779 | 10 | 20 | MISS ceiling | 2,876,122 | 236 | 0.038 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 2,316,662 | 46.333 | 10 | 24 | MISS ceiling | 2,278,050 | 344 | 0.036 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 35,024,685 | 700.494 | 10 | 24 | MISS ceiling | 1,469,508 | 142 | 0.041 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 2,316,142 | 46.323 | 10 | 50 | MISS T_svc | 2,278,050 | 344 | 0.036 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 12,443,603 | 248.872 | 10 | 50 | MISS ceiling | 3,089,796 | 323 | 0.038 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 36,717,425 | 734.348 | 10 | 18 | MISS ceiling | 1,693,000 | 49 | 0.063 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 43,000,448 | 860.009 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,840,874 | 56.817 | 10 | 20 | MISS ceiling | 3,067,607 | 174 (29) | 0.033 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 3,052,481 | 61.050 | 10 | 20 | MISS ceiling | 3,067,607 | 174 (29) | 0.033 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 2,796,246 | 55.925 | 10 | 20 | MISS ceiling | 4,760,437 | 342 (35) | 0.024 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 3,026,941 | 60.539 | 10 | 20 | MISS ceiling | 4,760,437 | 342 (35) | 0.024 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 1,556,712 | 31.134 | 10 | 20 | MISS ceiling | 2,647,467 | 87 (12) | 0.033 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 2,323,011 | 46.460 | 10 | 20 | MISS ceiling | 1,846,347 | 53 (12) | 0.022 |
| LINK_UP | `adp.link_up.if0` | 243,400 | 4.868 | 10 | 200 | fits | 3,083,161 | 316 (11) | 0.033 |
| LINK_UP | `adp.link_up.if1` | 546,076 | 10.922 | 10 | 200 | MISS T_svc | 3,083,161 | 316 (11) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 343,650 | 6.873 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 217,945 | 4.359 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| LINK_DOWN | `adp.link_down.if0` | 3,680,060 | 73.601 | 10 | 200 | MISS T_svc | 2,995,789 | 40 (9) | 0.060 |
| LINK_DOWN | `adp.link_down.if1` | 5,418,916 | 108.378 | 10 | 200 | MISS T_svc | 2,995,789 | 40 (9) | 0.060 |
| LINK_UP | `adp.link_up.if0` | 243,400 | 4.868 | 10 | 200 | fits | 3,083,161 | 316 (11) | 0.033 |
| LINK_UP | `adp.link_up.if1` | 546,076 | 10.922 | 10 | 200 | MISS T_svc | 3,083,161 | 316 (11) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 343,650 | 6.873 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 217,945 | 4.359 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| GM_CHANGE | `adp.gm_change.if0` | 568,218 | 11.364 | 10 | 200 | MISS T_svc | 995,600 | 40 (11) | 0.058 |
| GM_CHANGE | `adp.gm_change.if1` | 616,176 | 12.324 | 10 | 200 | MISS T_svc | 995,600 | 40 (11) | 0.058 |
| LINK_UP | `adp.link_up.if0` | 243,400 | 4.868 | 10 | 200 | fits | 3,083,161 | 316 (11) | 0.033 |
| LINK_UP | `adp.link_up.if1` | 546,076 | 10.922 | 10 | 200 | MISS T_svc | 3,083,161 | 316 (11) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 343,650 | 6.873 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 217,945 | 4.359 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 766,085 | 15.322 | 10 | 200 | MISS T_svc | 986,282 | 79 (31) | 0.053 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 801,017 | 16.020 | 10 | 200 | MISS T_svc | 986,282 | 79 (31) | 0.053 |
| LINK_UP | `adp.link_up.if0` | 243,400 | 4.868 | 10 | 200 | fits | 3,083,161 | 316 (11) | 0.033 |
| LINK_UP | `adp.link_up.if1` | 546,076 | 10.922 | 10 | 200 | MISS T_svc | 3,083,161 | 316 (11) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 343,650 | 6.873 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 217,945 | 4.359 | 10 | 200 | fits | 1,423,000 | 102 (39) | 0.063 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 766,085 | 15.322 | 10 | 200 | MISS T_svc | 951,737 | 51 (31) | 0.055 |
| set_name | `aecp_fanout.set_name.if0` | 3,345,962 | 66.919 | 10 | 24 | MISS ceiling | 3,368,800 | 1142 | 0.041 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 3,368,779 | 67.376 | 10 | 24 | MISS ceiling | 4,291,475 | 638 | 0.045 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 3,160,070 | 63.201 | 10 | 24 | MISS ceiling | 4,192,849 | 605 | 0.042 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 3,151,409 | 63.028 | 10 | 24 | MISS ceiling | 4,094,569 | 605 | 0.043 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 3,293,129 | 65.863 | 10 | 24 | MISS ceiling | 4,316,306 | 638 | 0.046 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 3,195,024 | 63.900 | 10 | 24 | MISS ceiling | 4,173,875 | 704 | 0.043 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 3,127,726 | 62.555 | 10 | 24 | MISS ceiling | 4,127,890 | 704 | 0.043 |
| set_name | `aecp_fanout.set_name.if1` | 3,359,999 | 67.200 | 10 | 24 | MISS ceiling | 4,414,251 | 1179 | 0.035 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 3,363,644 | 67.273 | 10 | 24 | MISS ceiling | 4,331,510 | 638 | 0.045 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 3,229,422 | 64.588 | 10 | 24 | MISS ceiling | 4,262,201 | 605 | 0.042 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 3,216,227 | 64.325 | 10 | 24 | MISS ceiling | 4,159,407 | 605 | 0.044 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 3,201,257 | 64.025 | 10 | 24 | MISS ceiling | 5,639,621 | 920 | 0.033 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 4,640,522 | 92.810 | 10 | 24 | MISS ceiling | 4,204,298 | 704 | 0.043 |
| BIND_RX | `acmp.bind_rx.if0` | 1,011,479 | 20.230 | 10 | 20 | MISS ceiling | 1,471,938 | 95 (77) | 0.049 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 663,855 | 13.277 | 10 | 20 | MISS T_svc | 1,754,538 | 65 (32) | 0.043 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 1,921,327 | 38.427 | 10 | 20 | MISS ceiling | 3,327,620 | 216 (47) | 0.037 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 270,498 | 5.410 | 10 | 20 | fits | 3,327,620 | 216 (50) | 0.037 |
| PROBE_TX | `acmp.probe_tx.if0` | 1,610,243 | 32.205 | 10 | 20 | MISS ceiling | 2,441,618 | 107 (48) | 0.040 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | - | - | - | - | no end: missing ['resp:1:4104'] | - | - | - |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 459,587 | 9.192 | 10 | 20 | fits | 2,835,581 | 152 (48) | 0.033 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 1,733,083 | 34.662 | 10 | 20 | MISS ceiling | 3,944,282 | 322 (48) | 0.029 |
| BIND_RX | `acmp.bind_rx.if1` | - | - | - | - | no end: missing ['resp:1:4107', 'acmp_cmd:1:PROBE_TX', 'arm:3', 'pub:710'] | - | - | - |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 1,740,570 | 34.811 | 10 | 20 | MISS ceiling | 2,836,964 | 157 (32) | 0.039 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 1,830,107 | 36.602 | 10 | 20 | MISS ceiling | 2,725,409 | 106 (47) | 0.033 |
| UNBIND_RX | `acmp.unbind_rx.if1` | - | - | - | - | no end: missing ['resp:1:4109', 'tmr:3'] | - | - | - |
| PROBE_TX | `acmp.probe_tx.if1` | 954,056 | 19.081 | 10 | 20 | MISS T_svc | 3,156,694 | 177 (48) | 0.033 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | - | - | - | - | no end: missing ['resp:1:410b'] | - | - | - |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 287,485 | 5.750 | 10 | 20 | fits | 2,916,031 | 150 (48) | 0.031 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 1,662,932 | 33.259 | 10 | 20 | MISS ceiling | 1,810,862 | 124 (48) | 0.058 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 1,138,066 | 22.761 | 10 | 24 | MISS T_svc | 1,202,072 | 59 | 0.050 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 1,224,817 | 24.496 | 10 | 24 | MISS ceiling | 1,156,720 | 131 | 0.037 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 1,172,477 | 23.450 | 10 | 24 | MISS T_svc | 2,168,534 | 179 | 0.053 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 1,189,588 | 23.792 | 10 | 24 | MISS T_svc | 1,280,882 | 96 | 0.042 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 1,353,788 | 27.076 | 10 | 24 | MISS ceiling | 1,281,268 | 95 | 0.042 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 1,193,095 | 23.862 | 10 | 24 | MISS T_svc | 1,121,943 | 89 | 0.039 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 570,174 | 11.403 | 10 | 24 | MISS T_svc | 3,002,642 | 308 | 0.028 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 2,693,151 | 53.863 | 10 | 24 | MISS ceiling | 2,256,775 | 117 | 0.052 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 1,376,258 | 27.525 | 10 | 24 | MISS ceiling | 1,274,657 | 77 | 0.043 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 1,626,549 | 32.531 | 10 | 24 | MISS ceiling | 1,554,159 | 200 | 0.041 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 1,346,735 | 26.935 | 10 | 24 | MISS ceiling | 1,269,724 | 64 | 0.043 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 858,552 | 17.171 | 10 | 24 | MISS T_svc | 1,854,612 | 106 | 0.050 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 1,191,546 | 23.831 | 10 | 24 | MISS T_svc | 1,282,975 | 81 | 0.041 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 1,357,618 | 27.152 | 10 | 24 | MISS ceiling | 1,284,971 | 87 | 0.041 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 1,196,224 | 23.924 | 10 | 24 | MISS T_svc | 1,123,629 | 77 | 0.039 |
| get_configuration | `aecp.get_configuration.if0` | 1,328,969 | 26.579 | 10 | 24 | MISS ceiling | 1,256,349 | 59 | 0.044 |
| entity_available | `aecp.entity_available.if0` | 1,169,058 | 23.381 | 10 | 24 | MISS T_svc | 1,096,414 | 57 | 0.041 |
| get_name | `aecp.get_name.if0` | 1,358,215 | 27.164 | 10 | 24 | MISS ceiling | 1,285,525 | 76 | 0.044 |
| get_counters | `aecp.get_counters.if0` | 1,204,810 | 24.096 | 10 | 24 | MISS ceiling | 1,132,123 | 86 | 0.040 |
| get_avb_info | `aecp.get_avb_info.if0` | 1,347,968 | 26.959 | 10 | 24 | MISS ceiling | 1,273,111 | 59 | 0.043 |
| unknown_command | `aecp.unknown_command.if0` | 1,317,931 | 26.359 | 10 | 24 | MISS ceiling | 1,245,072 | 59 | 0.044 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 1,601,729 | 32.035 | 10 | 24 | MISS ceiling | 1,688,777 | 124 | 0.054 |
| set_name | `aecp.set_name.if0` | 1,300,329 | 26.007 | 10 | 24 | MISS ceiling | 1,395,730 | 113 | 0.033 |
| lock_entity | `aecp.lock_entity.if0` | 1,207,989 | 24.160 | 10 | 24 | MISS ceiling | 2,224,657 | 153 | 0.046 |
| unlock_entity | `aecp.unlock_entity.if0` | 555,089 | 11.102 | 10 | 24 | MISS T_svc | 1,498,305 | 86 | 0.044 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 1,337,037 | 26.741 | 10 | 24 | MISS ceiling | 1,200,140 | 57 | 0.050 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 1,228,351 | 24.567 | 10 | 24 | MISS ceiling | 1,154,854 | 129 | 0.037 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 1,348,475 | 26.969 | 10 | 24 | MISS ceiling | 1,273,905 | 83 | 0.042 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 562,355 | 11.247 | 10 | 24 | MISS T_svc | 2,994,823 | 318 | 0.028 |
| get_configuration | `aecp.get_configuration.if1` | 2,526,850 | 50.537 | 10 | 24 | MISS ceiling | 2,092,595 | 89 | 0.052 |
| entity_available | `aecp.entity_available.if1` | 1,352,518 | 27.050 | 10 | 24 | MISS ceiling | 1,256,426 | 61 | 0.044 |
| get_name | `aecp.get_name.if1` | 1,199,589 | 23.992 | 10 | 24 | MISS T_svc | 1,126,120 | 68 | 0.041 |
| get_counters | `aecp.get_counters.if1` | 1,368,050 | 27.361 | 10 | 24 | MISS ceiling | 1,294,594 | 90 | 0.043 |
| get_avb_info | `aecp.get_avb_info.if1` | 1,348,839 | 26.977 | 10 | 24 | MISS ceiling | 1,273,288 | 57 | 0.043 |
| unknown_command | `aecp.unknown_command.if1` | 1,159,005 | 23.180 | 10 | 24 | MISS T_svc | 1,245,327 | 57 | 0.044 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 1,255,252 | 25.105 | 10 | 24 | MISS ceiling | 1,181,639 | 62 | 0.049 |
| set_name | `aecp.set_name.if1` | 1,303,751 | 26.075 | 10 | 24 | MISS ceiling | 1,571,111 | 152 | 0.034 |
| lock_entity | `aecp.lock_entity.if1` | 658,374 | 13.167 | 10 | 24 | MISS T_svc | 1,785,478 | 112 | 0.041 |
| unlock_entity | `aecp.unlock_entity.if1` | 625,383 | 12.508 | 10 | 24 | MISS T_svc | 1,558,037 | 105 | 0.044 |

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
- `backlog`: wait tx TIMEOUT
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
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait tx TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
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
- `aecp`: wait tx TIMEOUT
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
- `aecp`: wait tx TIMEOUT
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
