### 8x8

58 of 127 paths and 100 of 180 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 4.694 (13.343) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 11.610 (31.852) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 10.950 (30.951) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 22.600 (66.241) | MISS ceiling | 0 acmp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 31.768 (79.516) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 34.080 (79.516) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 47.331 (84.402) | MISS ceiling | 2 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 49.610 (84.402) | MISS ceiling | 3 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 11.295 (31.099) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 20.429 (40.247) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 10.955 (30.956) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 22.745 (40.145) | MISS ceiling | 0 acmp | 1 | 1 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 11.009 (31.001) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 29.509 (88.228) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 11.487 (30.998) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 22.417 (55.077) | MISS ceiling | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 19.633 (35.483) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 16.526 (39.839) | MISS T_svc | 0 acmp | 1 | 1 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 9.479 (26.985) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 3.831 (32.014) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 8.937 (39.445) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 9.720 (71.187) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 9.341 (71.187) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 16.253 (77.629) | MISS T_svc | 5 events | 1 | 1 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 15.354 (77.629) | MISS T_svc | 6 events | 1 | 1 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 18.753 (69.442) | MISS T_svc | 0 events | 1 | 1 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 1.692 (30.124) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 14.082 (64.533) | MISS T_svc | 0 events | 1 | 1 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 14.834 (64.533) | MISS T_svc | 2 events | 1 | 1 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 2.909 (23.193) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 20.866 (40.715) | MISS ceiling | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 1.574 (8.221) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 1.861 (8.220) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 1.392 (7.928) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 1.529 (7.928) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 17.361 (42.624) | MISS T_svc | 0 events | 1 | 1 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 25.869 (42.624) | MISS T_svc | 0 events | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 32.050 (73.380) | MISS T_svc | 0 events | 5 | 5 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 41.240 (73.380) | MISS T_svc | 0 events | 5 | 5 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.959 (7.376) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.265 (4.086) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 2.728 (9.129) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 1.542 (7.815) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 4.880 (10.643) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 4.904 (10.668) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 6.941 (11.330) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 5.841 (11.337) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 7.675 (27.675) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 5.585 (11.084) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 6.487 (12.249) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 5.381 (11.145) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 5.820 (11.583) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 5.860 (11.355) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 5.573 (11.699) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 8.779 (15.175) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 3.406 (9.662) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 3.435 (9.681) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 6.057 (12.316) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 6.059 (12.303) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 5.985 (11.747) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 6.003 (11.766) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 5.965 (11.728) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 5.182 (10.945) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 7.356 (12.867) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 5.673 (11.435) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 4.977 (11.246) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 6.111 (11.874) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 5.420 (11.183) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 6.128 (11.890) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 5.495 (11.257) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 6.162 (11.703) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 6.870 (11.681) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 6.194 (11.957) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 5.272 (11.035) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 6.115 (11.867) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 4.763 (10.526) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 8.000 (16.165) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 7.444 (15.059) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 5.537 (11.299) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 5.584 (11.349) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 6.924 (12.174) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 6.705 (13.094) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 15.996 (20.416) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 13.851 (17.185) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 16.351 (19.761) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 14.010 (18.396) | MISS T_svc | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 15.975 (21.766) | MISS T_svc | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 16.053 (21.853) | MISS T_svc | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 20.459 (28.575) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 20.484 (29.472) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 12.610 (15.677) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 13.837 (17.189) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 16.375 (20.470) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 108.664 (120.246) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 81.196 (104.671) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 117.104 (152.847) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 27.633 (52.954) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 161.212 (170.678) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind1.if0` (backlog-owed) | at least 860.001 | NEVER ANSWERED | 9 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 3.825 (10.199) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.000 (8.920) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 1.582 (8.102) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.823 (8.187) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 18.032 (38.988) | MISS T_svc | 0 events | 1 | 1 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 1.699 (15.383) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 3.566 (10.199) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 1.741 (8.920) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 1.594 (5.019) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 2.973 (9.377) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 26.786 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 176.272 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 26.829 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 136.316 | MISS T_svc | 6 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 88.873 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 26.822 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 511.894 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 26.811 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 101.477 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 657.089 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 657.069 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 12.839 (15.585) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 8.277 (11.472) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 8.217 (11.540) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 5.682 (9.002) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 5.312 (8.763) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 16.028 (17.982) | MISS T_svc | 0 events | 1 | 1 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 13.288 (33.213) | MISS T_svc | 1 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 608.717 | 63 | 1,241,802 (24.836) | yes | - |
| backlog-adp | 581.249 | 18 | 2,224,762 (44.495) | no | {'srp': 32} |
| backlog-adp-refill | 657.106 | 21 | 2,224,229 (44.485) | no | {'srp': 32} |
| backlog-owed | 860.053 | 84 | 1,111,083 (22.222) | yes | - |

Composed maximum over the 4 backlog windows: at least 2,224,762 CPU cycles (44.495 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 1,241,802 (24.836 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 937,634 | 18.753 | 10 | 20 | MISS T_svc | 1,595,572 | 132 (14) | 0.886 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 84,607 | 1.692 | 10 | 20 | fits | 1,506,220 | 125 (14) | 0.887 |
| LINK_UP | `adp.link_up.if0` | 1,602,488 | 32.050 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,000 | 41.240 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 136,380 | 2.728 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 77,119 | 1.542 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 47,949 | 0.959 | 10 | 200 | fits | 166,940 | 19 (11) | 0.861 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 13,242 | 0.265 | 10 | 200 | fits | 5,959 | 9 (11) | 0.867 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 901,612 | 18.032 | 10 | 50 | MISS T_svc | 1,050,297 | 178 | 0.863 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 57,337 | 1.147 | 10 | 50 | fits | 214,121 | 38 | 0.870 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 79,720 | 1.594 | 10 | 50 | fits | 250,973 | 44 | 0.872 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 178,302 | 3.566 | 10 | 50 | fits | 283,915 | 71 | 0.875 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 191,250 | 3.825 | 10 | 50 | fits | 283,915 | 71 | 0.875 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 79,100 | 1.582 | 10 | 50 | fits | 209,888 | 48 | 0.866 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 84,956 | 1.699 | 10 | 50 | fits | 574,160 | 154 | 0.853 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 135,943 | 2.719 | 10 | 50 | fits | 216,163 | 38 | 0.868 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 148,666 | 2.973 | 10 | 50 | fits | 254,226 | 44 | 0.871 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 87,041 | 1.741 | 10 | 50 | fits | 248,759 | 65 | 0.872 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 99,989 | 2.000 | 10 | 50 | fits | 248,759 | 65 | 0.872 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 91,156 | 1.823 | 10 | 50 | fits | 211,802 | 48 | 0.864 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 485,977 | 9.720 | 10 | 20 | fits | 1,686,267 | 158 (35) | 0.885 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 467,073 | 9.341 | 10 | 20 | fits | 1,686,267 | 158 (35) | 0.885 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 812,647 | 16.253 | 10 | 20 | MISS T_svc | 1,264,064 | 95 (14) | 0.883 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 767,692 | 15.354 | 10 | 20 | MISS T_svc | 1,264,064 | 95 (14) | 0.883 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 704,085 | 14.082 | 10 | 20 | MISS T_svc | 1,349,245 | 122 (14) | 0.881 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 741,683 | 14.834 | 10 | 20 | MISS T_svc | 1,349,245 | 122 (14) | 0.881 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 473,939 | 9.479 | 10 | 20 | fits | 1,349,245 | 122 (35) | 0.881 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 191,556 | 3.831 | 10 | 20 | fits | 1,600,695 | 132 (35) | 0.887 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 801,410 | 16.028 | 10 | 18 | MISS T_svc | 899,094 | 124 | 0.859 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 664,388 | 13.288 | 10 | 18 | MISS T_svc | 610,353 | 160 | 0.854 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 413,845 | 8.277 | 10 | 18 | fits | 298,724 | 36 | 0.864 |
| malformed MRPDU discard | `srp.malformed.if0` | 284,079 | 5.682 | 10 | 18 | fits | 200,643 | 29 | 0.858 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 641,950 | 12.839 | 210 | 218 | fits | 779,250 | 143 | 0.849 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 410,866 | 8.217 | 10 | 18 | fits | 309,502 | 36 | 0.863 |
| malformed MRPDU discard | `srp.malformed.if1` | 265,589 | 5.312 | 10 | 18 | fits | 257,120 | 36 | 0.861 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | - | - | - | - | no end: missing ['tx:4'] | - | - | - |
| an event behind 15 others | `backlog.event.if0` | 1,381,630 | 27.633 | 10 | 200 | MISS T_svc | 1,241,802 | 377 | 0.874 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 5,433,204 | 108.664 | 10 | 20 | MISS ceiling | 771,093 | 225 | 0.877 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,341,428 | 26.829 | 10 | 200 | MISS T_svc | 854,511 | 388 | 0.874 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 4,443,675 | 88.873 | 10 | 200 | MISS T_svc | 828,584 | 293 | 0.876 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,339,299 | 26.786 | 10 | 20 | MISS ceiling | 854,511 | 388 | 0.874 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 5,945,311 | 118.906 | 10 | 20 | MISS ceiling | 771,093 | 225 | 0.877 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,341,091 | 26.822 | 10 | 24 | MISS ceiling | 854,511 | 388 | 0.874 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 10,756,014 | 215.120 | 10 | 24 | MISS ceiling | 478,721 | 132 | 0.881 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,340,571 | 26.811 | 10 | 50 | MISS T_svc | 854,511 | 388 | 0.874 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 4,442,927 | 88.859 | 10 | 50 | MISS ceiling | 828,584 | 293 | 0.876 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 9,319,541 | 186.391 | 10 | 18 | MISS ceiling | 576,135 | 171 | 0.878 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 14,710,820 | 294.216 | 10 | 18 | MISS ceiling | 240,067 | 48 | 0.861 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 4,059,781 | 81.196 | 10 | 20 | MISS ceiling | 1,726,808 | 383 | 0.881 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 1,171,236 | 23.425 | 10 | 200 | MISS T_svc | 1,332,452 | 407 | 0.880 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 5,072,018 | 101.440 | 10 | 200 | MISS T_svc | 1,726,808 | 383 | 0.881 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 1,171,692 | 23.434 | 10 | 20 | MISS ceiling | 1,332,452 | 407 | 0.880 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 8,777,277 | 175.546 | 10 | 20 | MISS ceiling | 1,956,560 | 309 | 0.884 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 1,173,485 | 23.470 | 10 | 24 | MISS T_svc | 1,332,452 | 407 | 0.880 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 25,445,829 | 508.917 | 10 | 24 | MISS ceiling | 1,571,267 | 238 | 0.885 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 1,172,965 | 23.459 | 10 | 50 | MISS T_svc | 1,332,452 | 407 | 0.880 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 5,073,856 | 101.477 | 10 | 50 | MISS ceiling | 1,726,808 | 383 | 0.881 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 29,061,586 | 581.232 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 29,060,579 | 581.212 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 5,855,204 | 117.104 | 10 | 20 | MISS ceiling | 2,069,857 | 341 | 0.883 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 1,171,236 | 23.425 | 10 | 200 | MISS T_svc | 1,332,452 | 407 | 0.880 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 6,815,803 | 136.316 | 10 | 200 | MISS T_svc | 2,069,857 | 341 | 0.883 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 1,171,692 | 23.434 | 10 | 20 | MISS ceiling | 1,332,452 | 407 | 0.880 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 8,813,609 | 176.272 | 10 | 20 | MISS ceiling | 2,069,857 | 341 | 0.883 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 1,173,485 | 23.470 | 10 | 24 | MISS T_svc | 1,332,452 | 407 | 0.880 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 25,594,684 | 511.894 | 10 | 24 | MISS ceiling | 1,686,069 | 222 | 0.887 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 1,172,965 | 23.459 | 10 | 50 | MISS T_svc | 1,332,452 | 407 | 0.880 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 4,973,147 | 99.463 | 10 | 50 | MISS ceiling | 1,626,099 | 376 | 0.883 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 32,854,467 | 657.089 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 32,853,460 | 657.069 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 8,060,608 | 161.212 | 10 | 20 | MISS ceiling | 588,396 | 154 | 0.878 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 8,832,749 | 176.655 | 10 | 20 | MISS ceiling | 772,179 | 199 | 0.874 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 43,000,073 | 860.001 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 9,488,460 | 189.769 | 10 | 20 | MISS ceiling | 655,786 | 174 | 0.875 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 42,999,998 | 860.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 892,558 | 17.851 | 10 | 200 | MISS T_svc | 881,519 | 346 | 0.874 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 3,615,252 | 72.305 | 10 | 200 | MISS T_svc | 959,829 | 290 | 0.874 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 890,428 | 17.809 | 10 | 20 | MISS T_svc | 881,519 | 346 | 0.874 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 5,269,605 | 105.392 | 10 | 20 | MISS ceiling | 828,248 | 203 | 0.875 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 892,221 | 17.844 | 10 | 24 | MISS T_svc | 881,519 | 346 | 0.874 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 11,281,466 | 225.629 | 10 | 24 | MISS ceiling | 492,608 | 132 | 0.880 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 891,701 | 17.834 | 10 | 50 | MISS T_svc | 881,519 | 346 | 0.874 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 3,614,505 | 72.290 | 10 | 50 | MISS ceiling | 959,829 | 290 | 0.874 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 7,198,905 | 143.978 | 10 | 18 | MISS ceiling | 801,535 | 199 | 0.874 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 17,040,648 | 340.813 | 10 | 18 | MISS ceiling | 239,726 | 30 | 0.859 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 2,366,532 | 47.331 | 10 | 20 | MISS ceiling | 1,725,071 | 219 (29) | 0.885 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 2,480,512 | 49.610 | 10 | 20 | MISS ceiling | 1,725,071 | 219 (29) | 0.885 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,588,391 | 31.768 | 10 | 20 | MISS ceiling | 2,102,270 | 185 (35) | 0.886 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,703,987 | 34.080 | 10 | 20 | MISS ceiling | 2,102,270 | 185 (35) | 0.886 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | - | - | - | - | no start: no deadline:2 after the mark | - | - | - |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 446,867 | 8.937 | 10 | 20 | fits | 1,972,266 | 149 (12) | 0.888 |
| LINK_UP | `adp.link_up.if0` | 1,602,488 | 32.050 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,000 | 41.240 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 136,380 | 2.728 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 77,119 | 1.542 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| LINK_DOWN | `adp.link_down.if0` | 868,039 | 17.361 | 10 | 200 | MISS T_svc | 1,171,843 | 70 (9) | 0.875 |
| LINK_DOWN | `adp.link_down.if1` | 1,293,444 | 25.869 | 10 | 200 | MISS T_svc | 1,171,843 | 70 (9) | 0.875 |
| LINK_UP | `adp.link_up.if0` | 1,602,488 | 32.050 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,000 | 41.240 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 136,380 | 2.728 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 77,119 | 1.542 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| GM_CHANGE | `adp.gm_change.if0` | 69,589 | 1.392 | 10 | 200 | fits | 173,208 | 28 (11) | 0.861 |
| GM_CHANGE | `adp.gm_change.if1` | 76,469 | 1.529 | 10 | 200 | fits | 173,208 | 28 (11) | 0.861 |
| LINK_UP | `adp.link_up.if0` | 1,602,488 | 32.050 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,000 | 41.240 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 136,380 | 2.728 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 77,119 | 1.542 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 78,678 | 1.574 | 10 | 200 | fits | 187,880 | 67 (31) | 0.862 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 93,056 | 1.861 | 10 | 200 | fits | 187,880 | 67 (31) | 0.862 |
| LINK_UP | `adp.link_up.if0` | 1,602,488 | 32.050 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| LINK_UP | `adp.link_up.if1` | 2,062,000 | 41.240 | 10 | 200 | MISS T_svc | 2,009,722 | 345 (11) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 136,380 | 2.728 | 10 | 200 | fits | 194,270 | 47 (39) | 0.864 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 77,119 | 1.542 | 10 | 200 | fits | 194,277 | 47 (39) | 0.864 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 78,678 | 1.574 | 10 | 200 | fits | 173,878 | 39 (31) | 0.861 |
| set_name | `aecp_fanout.set_name.if0` | 1,022,927 | 20.459 | 10 | 24 | MISS T_svc | 1,231,245 | 1172 | 0.881 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 817,550 | 16.351 | 10 | 24 | MISS T_svc | 790,356 | 613 | 0.876 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 798,730 | 15.975 | 10 | 24 | MISS T_svc | 821,222 | 587 | 0.878 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 774,495 | 15.490 | 10 | 24 | MISS T_svc | 782,838 | 580 | 0.877 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 630,525 | 12.610 | 10 | 24 | MISS T_svc | 783,855 | 598 | 0.879 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 799,821 | 15.996 | 10 | 24 | MISS T_svc | 823,097 | 679 | 0.880 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 691,828 | 13.837 | 10 | 24 | MISS T_svc | 859,431 | 686 | 0.880 |
| set_name | `aecp_fanout.set_name.if1` | 1,024,215 | 20.484 | 10 | 24 | MISS T_svc | 1,149,702 | 1132 | 0.882 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 700,488 | 14.010 | 10 | 24 | MISS T_svc | 919,792 | 674 | 0.879 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 802,650 | 16.053 | 10 | 24 | MISS T_svc | 823,369 | 587 | 0.878 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 778,457 | 15.569 | 10 | 24 | MISS T_svc | 784,858 | 580 | 0.878 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 692,562 | 13.851 | 10 | 24 | MISS T_svc | 859,253 | 686 | 0.880 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 818,728 | 16.375 | 10 | 24 | MISS T_svc | 825,618 | 679 | 0.880 |
| BIND_RX | `acmp.bind_rx.if0` | 234,684 | 4.694 | 10 | 20 | fits | 396,518 | 90 (77) | 0.869 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 981,633 | 19.633 | 10 | 20 | MISS T_svc | 1,774,170 | 144 (32) | 0.885 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 564,733 | 11.295 | 10 | 20 | MISS T_svc | 1,554,975 | 149 (47) | 0.884 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 145,454 | 2.909 | 10 | 20 | fits | 1,159,646 | 194 (50) | 0.881 |
| PROBE_TX | `acmp.probe_tx.if0` | 574,372 | 11.487 | 10 | 20 | MISS T_svc | 1,549,885 | 151 (48) | 0.884 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 550,456 | 11.009 | 10 | 20 | MISS T_svc | 1,550,073 | 150 (48) | 0.884 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 547,504 | 10.950 | 10 | 20 | MISS T_svc | 1,547,541 | 150 (48) | 0.884 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 547,763 | 10.955 | 10 | 20 | MISS T_svc | 1,547,800 | 150 (48) | 0.884 |
| BIND_RX | `acmp.bind_rx.if1` | 580,497 | 11.610 | 10 | 20 | MISS T_svc | 1,592,581 | 180 (77) | 0.883 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 826,304 | 16.526 | 10 | 20 | MISS T_svc | 1,991,950 | 153 (32) | 0.887 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 1,021,462 | 20.429 | 10 | 20 | MISS ceiling | 2,012,353 | 168 (47) | 0.887 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 1,043,311 | 20.866 | 10 | 20 | MISS ceiling | 2,035,757 | 171 (50) | 0.887 |
| PROBE_TX | `acmp.probe_tx.if1` | 1,120,861 | 22.417 | 10 | 20 | MISS ceiling | 2,753,869 | 386 (48) | 0.874 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 1,475,461 | 29.509 | 10 | 20 | MISS ceiling | 1,657,515 | 176 (48) | 0.886 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 1,129,991 | 22.600 | 10 | 20 | MISS ceiling | 1,654,530 | 176 (48) | 0.886 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 1,137,231 | 22.745 | 10 | 20 | MISS ceiling | 2,007,240 | 169 (48) | 0.887 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 305,764 | 6.115 | 10 | 24 | fits | 322,670 | 56 | 0.874 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 302,864 | 6.057 | 10 | 24 | fits | 419,161 | 127 | 0.880 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 299,227 | 5.985 | 10 | 24 | fits | 415,283 | 82 | 0.879 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 305,572 | 6.111 | 10 | 24 | fits | 421,369 | 123 | 0.879 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 343,480 | 6.870 | 10 | 24 | fits | 387,383 | 86 | 0.879 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 309,719 | 6.194 | 10 | 24 | fits | 425,483 | 92 | 0.879 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 263,625 | 5.272 | 10 | 24 | fits | 379,506 | 74 | 0.879 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 298,272 | 5.965 | 10 | 24 | fits | 414,502 | 77 | 0.879 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 259,120 | 5.182 | 10 | 24 | fits | 374,964 | 67 | 0.878 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 367,799 | 7.356 | 10 | 24 | fits | 448,993 | 163 | 0.880 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 283,654 | 5.673 | 10 | 24 | fits | 402,268 | 61 | 0.878 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 248,871 | 4.977 | 10 | 24 | fits | 366,677 | 54 | 0.878 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 306,391 | 6.128 | 10 | 24 | fits | 424,042 | 78 | 0.877 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 274,736 | 5.495 | 10 | 24 | fits | 392,196 | 77 | 0.878 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 308,080 | 6.162 | 10 | 24 | fits | 389,467 | 74 | 0.878 |
| get_configuration | `aecp.get_configuration.if0` | 383,742 | 7.675 | 10 | 24 | fits | 430,186 | 62 | 0.879 |
| entity_available | `aecp.entity_available.if0` | 244,009 | 4.880 | 10 | 24 | fits | 360,662 | 53 | 0.879 |
| get_name | `aecp.get_name.if0` | 291,023 | 5.820 | 10 | 24 | fits | 407,794 | 73 | 0.879 |
| get_counters | `aecp.get_counters.if0` | 324,349 | 6.487 | 10 | 24 | fits | 384,302 | 87 | 0.880 |
| get_avb_info | `aecp.get_avb_info.if0` | 347,065 | 6.941 | 10 | 24 | fits | 370,067 | 49 | 0.877 |
| unknown_command | `aecp.unknown_command.if0` | 276,851 | 5.537 | 10 | 24 | fits | 393,658 | 56 | 0.878 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 170,304 | 3.406 | 10 | 24 | fits | 287,120 | 54 | 0.873 |
| set_name | `aecp.set_name.if0` | 399,996 | 8.000 | 10 | 24 | fits | 636,986 | 156 | 0.869 |
| lock_entity | `aecp.lock_entity.if0` | 278,633 | 5.573 | 10 | 24 | fits | 411,905 | 90 | 0.875 |
| unlock_entity | `aecp.unlock_entity.if0` | 346,221 | 6.924 | 10 | 24 | fits | 411,882 | 90 | 0.875 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 238,167 | 4.763 | 10 | 24 | fits | 323,151 | 54 | 0.875 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 302,964 | 6.059 | 10 | 24 | fits | 418,892 | 125 | 0.880 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 300,162 | 6.003 | 10 | 24 | fits | 415,780 | 80 | 0.879 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 270,996 | 5.420 | 10 | 24 | fits | 386,285 | 84 | 0.879 |
| get_configuration | `aecp.get_configuration.if1` | 279,241 | 5.585 | 10 | 24 | fits | 357,277 | 48 | 0.878 |
| entity_available | `aecp.entity_available.if1` | 245,193 | 4.904 | 10 | 24 | fits | 360,465 | 51 | 0.879 |
| get_name | `aecp.get_name.if1` | 293,023 | 5.860 | 10 | 24 | fits | 370,896 | 65 | 0.879 |
| get_counters | `aecp.get_counters.if1` | 269,059 | 5.381 | 10 | 24 | fits | 384,105 | 85 | 0.880 |
| get_avb_info | `aecp.get_avb_info.if1` | 292,029 | 5.841 | 10 | 24 | fits | 369,870 | 47 | 0.877 |
| unknown_command | `aecp.unknown_command.if1` | 279,221 | 5.584 | 10 | 24 | fits | 394,512 | 54 | 0.879 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 171,752 | 3.435 | 10 | 24 | fits | 286,923 | 52 | 0.873 |
| set_name | `aecp.set_name.if1` | 372,189 | 7.444 | 10 | 24 | fits | 579,520 | 149 | 0.870 |
| lock_entity | `aecp.lock_entity.if1` | 438,952 | 8.779 | 10 | 24 | fits | 463,489 | 116 | 0.876 |
| unlock_entity | `aecp.unlock_entity.if1` | 335,233 | 6.705 | 10 | 24 | fits | 425,006 | 109 | 0.876 |

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
