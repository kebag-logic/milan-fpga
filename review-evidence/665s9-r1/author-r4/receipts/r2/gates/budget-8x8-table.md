head 3ba76ae7c75f655fb77cad80866f6799d0e73087
command: run.py --point 8x8 --record-budget-findings: results/table.md
full log: 40421 bytes, sha256 a90a3164229d477e6b355e0a4d98aaf6206e7169a80fb16e59b34a240f4ba376
---
### 8x8

31 of 129 paths and 63 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.432 (4.681) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 16.945 (37.100) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 16.511 (36.512) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 5.052 (25.053) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 22.879 (53.527) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 24.159 (53.527) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 17.754 (26.075) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 19.000 (26.075) | MISS T_svc | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 16.753 (36.633) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 5.835 (33.937) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 16.523 (36.524) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 1.754 (21.754) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 18.725 (38.719) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 8.902 (28.896) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 16.871 (36.551) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 5.416 (25.086) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 4.027 (21.423) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 7.152 (28.765) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.508 (21.472) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 3.239 (48.252) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 2.164 (23.119) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 2.567 (50.760) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 3.149 (24.594) | fits | 1 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 7.918 (49.182) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 2.520 (24.313) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 7.665 (44.814) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 4.102 (24.646) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 3.386 (24.577) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.379 (24.276) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 8.926 (45.748) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 14.530 (34.731) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 13.468 (25.451) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.199 (2.379) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.375 (2.379) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.079 (2.207) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.171 (2.207) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.063 (12.989) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.063 (12.989) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.078 (12.213) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.862 (12.213) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.308 (2.333) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.214 (2.333) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.459 (5.915) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.855 (4.915) | fits | 1 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.496 (4.124) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.927 (4.559) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 4.589 (6.705) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.618 (4.250) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.895 (4.524) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.889 (4.521) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.772 (4.402) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 2.768 (4.400) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 3.040 (4.669) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 3.049 (4.680) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 3.356 (5.212) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.925 (4.936) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.204 (3.833) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 1.778 (3.408) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.598 (5.228) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.590 (5.220) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 3.134 (4.764) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.697 (4.327) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 2.697 (4.327) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.668 (4.298) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.490 (5.120) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.569 (4.199) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 3.013 (4.643) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.794 (4.424) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 3.351 (6.883) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 2.832 (4.462) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.871 (4.501) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.837 (4.466) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 2.801 (4.431) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 3.248 (4.878) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 4.341 (7.990) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 2.200 (3.823) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 1.760 (3.389) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.337 (7.342) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.960 (6.646) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.455 (4.083) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.885 (4.516) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 3.356 (5.210) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.924 (4.930) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 9.523 (13.211) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 9.696 (13.384) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.126 (9.607) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 7.725 (9.207) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 9.117 (12.803) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 9.309 (12.995) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.360 (14.081) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 10.946 (13.112) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 8.269 (11.770) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.271 (9.920) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 9.752 (13.442) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 58.714 (64.540) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 47.982 (66.595) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 53.762 (68.398) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 14.843 (28.667) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 118.773 (124.511) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 370.373 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 2.673 (6.720) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.580 (6.685) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 1.079 (3.052) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 1.078 (3.078) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.761 (7.313) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.762 (6.919) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 2.524 (6.720) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.431 (6.685) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 2.113 (6.124) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 2.292 (6.361) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 14.288 | MISS T_svc | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 104.246 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 14.331 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 64.290 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 48.020 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 14.324 | MISS T_svc | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 315.046 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 14.314 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 59.157 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 593.747 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 593.727 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 8.323 (10.071) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 8.552 (10.218) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.308 (3.309) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.376 (3.377) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 3.064 (3.064) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.215 (3.216) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.824 (7.313) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.486 (6.921) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 160.402 | 25 | 716,697 (14.334) | yes | - |
| backlog-adp | 548.035 | 29 | 1,460,373 (29.207) | no | {'srp': 32} |
| backlog-adp-refill | 593.764 | 31 | 1,460,077 (29.202) | no | {'srp': 32} |
| backlog-owed | 370.424 | 43 | 626,272 (12.525) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,460,373 CPU cycles (29.207 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 716,697 (14.334 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 205,110 | 4.102 | 10 | 20 | fits | 1,232,286 | 166 (14) | 0.027 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 169,288 | 3.386 | 10 | 20 | fits | 1,228,859 | 144 (14) | 0.028 |
| LINK_UP | `adp.link_up.if0` | 3,905 | 0.078 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,108 | 0.862 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,956 | 1.459 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,748 | 0.855 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 15,399 | 0.308 | 10 | 200 | fits | 8,671 | 18 (11) | 0.144 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 10,682 | 0.214 | 10 | 200 | fits | 8,671 | 18 (11) | 0.144 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 38,037 | 0.761 | 10 | 50 | fits | 365,668 | 160 | 0.041 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 105,654 | 2.113 | 10 | 50 | fits | 132,885 | 38 | 0.064 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 67,952 | 1.359 | 10 | 50 | fits | 132,856 | 38 | 0.064 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 126,181 | 2.524 | 10 | 50 | fits | 150,928 | 65 | 0.063 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 133,639 | 2.673 | 10 | 50 | fits | 150,928 | 65 | 0.063 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 53,970 | 1.079 | 10 | 50 | fits | 152,582 | 54 | 0.064 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 38,114 | 0.762 | 10 | 50 | fits | 345,952 | 153 | 0.038 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 53,408 | 1.068 | 10 | 50 | fits | 134,364 | 38 | 0.063 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 114,591 | 2.292 | 10 | 50 | fits | 134,335 | 38 | 0.063 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 121,537 | 2.431 | 10 | 50 | fits | 152,389 | 65 | 0.062 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 128,995 | 2.580 | 10 | 50 | fits | 152,389 | 65 | 0.062 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 53,885 | 1.078 | 10 | 50 | fits | 153,916 | 54 | 0.063 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 157,459 | 3.149 | 10 | 20 | fits | 1,229,683 | 166 (35) | 0.027 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 395,883 | 7.918 | 10 | 20 | fits | 1,229,415 | 166 (35) | 0.027 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 126,007 | 2.520 | 10 | 20 | fits | 1,215,672 | 143 (14) | 0.027 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 383,230 | 7.665 | 10 | 20 | fits | 1,025,010 | 126 (14) | 0.029 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 18,931 | 0.379 | 10 | 20 | fits | 1,213,811 | 144 (14) | 0.027 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 446,298 | 8.926 | 10 | 20 | fits | 1,073,603 | 152 (14) | 0.029 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 75,403 | 1.508 | 10 | 20 | fits | 1,073,603 | 152 (35) | 0.029 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 161,938 | 3.239 | 10 | 20 | fits | 1,231,345 | 166 (35) | 0.027 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 341,206 | 6.824 | 10 | 18 | fits | 365,668 | 160 | 0.041 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 324,289 | 6.486 | 10 | 18 | fits | 346,048 | 154 | 0.038 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 165,419 | 3.308 | 10 | 18 | fits | 165,451 | 29 | 0.067 |
| malformed MRPDU discard | `srp.malformed.if0` | 153,176 | 3.064 | 10 | 18 | fits | 153,208 | 36 | 0.058 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 416,137 | 8.323 | 210 | 218 | fits | 503,565 | 149 | 0.046 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 168,794 | 3.376 | 10 | 18 | fits | 168,826 | 29 | 0.066 |
| malformed MRPDU discard | `srp.malformed.if1` | 160,750 | 3.215 | 10 | 18 | fits | 160,782 | 36 | 0.056 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 427,609 | 8.552 | 210 | 218 | fits | 510,896 | 149 | 0.045 |
| an event behind 15 others | `backlog.event.if0` | 742,135 | 14.843 | 10 | 200 | MISS T_svc | 716,697 | 377 | 0.053 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,935,698 | 58.714 | 10 | 20 | MISS ceiling | 412,784 | 219 | 0.036 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 716,550 | 14.331 | 10 | 200 | MISS T_svc | 716,654 | 394 | 0.052 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,400,994 | 48.020 | 10 | 200 | MISS T_svc | 447,769 | 287 | 0.037 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 714,421 | 14.288 | 10 | 20 | MISS T_svc | 716,654 | 394 | 0.052 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,224,364 | 64.487 | 10 | 20 | MISS ceiling | 412,784 | 219 | 0.036 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 716,213 | 14.324 | 10 | 24 | MISS T_svc | 716,654 | 394 | 0.052 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,223,770 | 124.475 | 10 | 24 | MISS ceiling | 248,105 | 126 | 0.038 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 715,693 | 14.314 | 10 | 50 | MISS T_svc | 716,654 | 394 | 0.052 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,400,246 | 48.005 | 10 | 50 | MISS T_svc | 447,769 | 287 | 0.037 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,561,493 | 71.230 | 10 | 18 | MISS ceiling | 335,671 | 171 | 0.052 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,706,796 | 154.136 | 10 | 18 | MISS ceiling | 173,515 | 36 | 0.067 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,399,101 | 47.982 | 10 | 20 | MISS ceiling | 1,163,955 | 403 | 0.032 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 615,896 | 12.318 | 10 | 200 | MISS T_svc | 989,347 | 427 | 0.034 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,956,011 | 59.120 | 10 | 200 | MISS T_svc | 1,163,955 | 403 | 0.032 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 616,352 | 12.327 | 10 | 20 | MISS T_svc | 989,347 | 427 | 0.034 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 5,190,588 | 103.812 | 10 | 20 | MISS ceiling | 1,170,890 | 319 | 0.029 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 618,144 | 12.363 | 10 | 24 | MISS T_svc | 989,347 | 427 | 0.034 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 15,730,851 | 314.617 | 10 | 24 | MISS ceiling | 1,020,573 | 232 | 0.030 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 617,624 | 12.352 | 10 | 50 | MISS T_svc | 989,347 | 427 | 0.034 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,957,849 | 59.157 | 10 | 50 | MISS ceiling | 1,163,955 | 403 | 0.032 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,400,906 | 548.018 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,399,899 | 547.998 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,688,093 | 53.762 | 10 | 20 | MISS ceiling | 1,125,782 | 341 | 0.031 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 615,896 | 12.318 | 10 | 200 | MISS T_svc | 989,347 | 427 | 0.034 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 3,214,501 | 64.290 | 10 | 200 | MISS T_svc | 1,125,782 | 341 | 0.031 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 616,352 | 12.327 | 10 | 20 | MISS T_svc | 989,347 | 427 | 0.034 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 5,212,307 | 104.246 | 10 | 20 | MISS ceiling | 1,125,782 | 341 | 0.031 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 618,144 | 12.363 | 10 | 24 | MISS T_svc | 989,347 | 427 | 0.034 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,752,292 | 315.046 | 10 | 24 | MISS ceiling | 1,020,689 | 232 | 0.030 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 617,624 | 12.352 | 10 | 50 | MISS T_svc | 989,347 | 427 | 0.034 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,902,258 | 58.045 | 10 | 50 | MISS ceiling | 1,108,364 | 396 | 0.032 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,687,356 | 593.747 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,686,349 | 593.727 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,938,641 | 118.773 | 10 | 20 | MISS ceiling | 421,525 | 193 | 0.048 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,518,655 | 370.373 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,518,617 | 370.372 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,518,580 | 370.372 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,518,542 | 370.371 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 568,004 | 11.360 | 10 | 200 | MISS T_svc | 483,460 | 346 | 0.040 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 2,154,433 | 43.089 | 10 | 200 | MISS T_svc | 461,592 | 263 | 0.035 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 565,875 | 11.317 | 10 | 20 | MISS T_svc | 483,460 | 346 | 0.040 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,021,878 | 60.438 | 10 | 20 | MISS ceiling | 400,639 | 122 | 0.047 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 567,667 | 11.353 | 10 | 24 | MISS T_svc | 483,460 | 346 | 0.040 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,117,001 | 142.340 | 10 | 24 | MISS ceiling | 368,941 | 171 | 0.051 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 567,147 | 11.343 | 10 | 50 | MISS T_svc | 483,460 | 346 | 0.040 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,153,685 | 43.074 | 10 | 50 | MISS T_svc | 461,592 | 263 | 0.035 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,692,061 | 33.841 | 10 | 18 | MISS ceiling | 626,272 | 345 | 0.050 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 8,115,806 | 162.316 | 10 | 18 | MISS ceiling | 152,670 | 29 | 0.061 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 887,698 | 17.754 | 10 | 20 | MISS T_svc | 1,303,767 | 191 (29) | 0.027 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 950,016 | 19.000 | 10 | 20 | MISS T_svc | 1,303,767 | 191 (29) | 0.027 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,143,961 | 22.879 | 10 | 20 | MISS ceiling | 1,307,170 | 202 (35) | 0.027 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,207,958 | 24.159 | 10 | 20 | MISS ceiling | 1,307,170 | 202 (35) | 0.027 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 108,195 | 2.164 | 10 | 20 | fits | 1,155,928 | 127 (12) | 0.025 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 128,372 | 2.567 | 10 | 20 | fits | 1,116,992 | 149 (12) | 0.029 |
| LINK_UP | `adp.link_up.if0` | 3,905 | 0.078 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,108 | 0.862 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,956 | 1.459 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,748 | 0.855 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| LINK_DOWN | `adp.link_down.if0` | 3,129 | 0.063 | 10 | 200 | fits | 649,448 | 58 (9) | 0.075 |
| LINK_DOWN | `adp.link_down.if1` | 253,174 | 5.063 | 10 | 200 | fits | 649,448 | 58 (9) | 0.075 |
| LINK_UP | `adp.link_up.if0` | 3,905 | 0.078 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,108 | 0.862 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,956 | 1.459 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,748 | 0.855 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| GM_CHANGE | `adp.gm_change.if0` | 3,971 | 0.079 | 10 | 200 | fits | 110,340 | 28 (11) | 0.060 |
| GM_CHANGE | `adp.gm_change.if1` | 8,574 | 0.171 | 10 | 200 | fits | 110,340 | 28 (11) | 0.060 |
| LINK_UP | `adp.link_up.if0` | 3,905 | 0.078 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,108 | 0.862 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,956 | 1.459 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,748 | 0.855 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 9,974 | 0.199 | 10 | 200 | fits | 118,931 | 67 (31) | 0.053 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 18,729 | 0.375 | 10 | 200 | fits | 118,931 | 67 (31) | 0.053 |
| LINK_UP | `adp.link_up.if0` | 3,905 | 0.078 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,108 | 0.862 | 10 | 200 | fits | 610,672 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 72,956 | 1.459 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 42,748 | 0.855 | 10 | 200 | fits | 140,893 | 84 (39) | 0.058 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 9,974 | 0.199 | 10 | 200 | fits | 110,397 | 39 (31) | 0.054 |
| set_name | `aecp_fanout.set_name.if0` | 568,020 | 11.360 | 10 | 24 | MISS T_svc | 704,055 | 1172 | 0.032 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 406,309 | 8.126 | 10 | 24 | fits | 480,350 | 620 | 0.048 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 455,839 | 9.117 | 10 | 24 | fits | 476,060 | 587 | 0.047 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 442,413 | 8.848 | 10 | 24 | fits | 454,203 | 580 | 0.044 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 413,471 | 8.269 | 10 | 24 | fits | 430,700 | 591 | 0.048 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 476,139 | 9.523 | 10 | 24 | fits | 475,552 | 680 | 0.043 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 413,555 | 8.271 | 10 | 24 | fits | 495,983 | 686 | 0.045 |
| set_name | `aecp_fanout.set_name.if1` | 547,304 | 10.946 | 10 | 24 | MISS T_svc | 655,612 | 1132 | 0.032 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 386,255 | 7.725 | 10 | 24 | fits | 460,334 | 613 | 0.046 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 457,022 | 9.140 | 10 | 24 | fits | 455,711 | 580 | 0.044 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 465,431 | 9.309 | 10 | 24 | fits | 455,081 | 580 | 0.044 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 484,805 | 9.696 | 10 | 24 | fits | 474,497 | 680 | 0.043 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 487,623 | 9.752 | 10 | 24 | fits | 476,524 | 680 | 0.043 |
| BIND_RX | `acmp.bind_rx.if0` | 71,592 | 1.432 | 10 | 20 | fits | 234,050 | 90 (77) | 0.052 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 201,346 | 4.027 | 10 | 20 | fits | 1,071,174 | 154 (32) | 0.030 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 837,654 | 16.753 | 10 | 20 | MISS T_svc | 954,097 | 159 (47) | 0.031 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 726,508 | 14.530 | 10 | 20 | MISS T_svc | 858,757 | 214 (50) | 0.034 |
| PROBE_TX | `acmp.probe_tx.if0` | 843,563 | 16.871 | 10 | 20 | MISS T_svc | 951,780 | 161 (48) | 0.031 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 936,260 | 18.725 | 10 | 20 | MISS T_svc | 1,059,572 | 170 (48) | 0.029 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 825,568 | 16.511 | 10 | 20 | MISS T_svc | 949,813 | 160 (48) | 0.030 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 826,161 | 16.523 | 10 | 20 | MISS T_svc | 950,043 | 160 (48) | 0.031 |
| BIND_RX | `acmp.bind_rx.if1` | 847,229 | 16.945 | 10 | 20 | MISS T_svc | 978,802 | 190 (77) | 0.032 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 357,577 | 7.152 | 10 | 20 | fits | 1,438,225 | 187 (32) | 0.026 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 291,731 | 5.835 | 10 | 20 | fits | 1,696,831 | 401 (47) | 0.025 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 673,386 | 13.468 | 10 | 20 | MISS T_svc | 1,272,562 | 188 (50) | 0.029 |
| PROBE_TX | `acmp.probe_tx.if1` | 270,816 | 5.416 | 10 | 20 | fits | 1,254,293 | 187 (48) | 0.028 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 445,086 | 8.902 | 10 | 20 | fits | 1,444,798 | 203 (48) | 0.026 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 252,624 | 5.052 | 10 | 20 | fits | 1,252,648 | 186 (48) | 0.028 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 87,678 | 1.754 | 10 | 20 | fits | 1,087,715 | 217 (48) | 0.032 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 109,980 | 2.200 | 10 | 24 | fits | 191,144 | 56 | 0.055 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 179,915 | 3.598 | 10 | 24 | fits | 261,410 | 134 | 0.044 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 156,688 | 3.134 | 10 | 24 | fits | 238,180 | 82 | 0.047 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 139,698 | 2.794 | 10 | 24 | fits | 221,190 | 86 | 0.041 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 140,060 | 2.801 | 10 | 24 | fits | 221,555 | 85 | 0.041 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 162,408 | 3.248 | 10 | 24 | fits | 243,903 | 92 | 0.046 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 217,067 | 4.341 | 10 | 24 | fits | 217,629 | 75 | 0.042 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 134,869 | 2.697 | 10 | 24 | fits | 216,364 | 70 | 0.042 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 133,410 | 2.668 | 10 | 24 | fits | 214,902 | 67 | 0.042 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 174,514 | 3.490 | 10 | 24 | fits | 256,006 | 162 | 0.036 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 128,433 | 2.569 | 10 | 24 | fits | 209,925 | 54 | 0.043 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 150,653 | 3.013 | 10 | 24 | fits | 232,145 | 61 | 0.048 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 141,622 | 2.832 | 10 | 24 | fits | 223,114 | 71 | 0.041 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 143,566 | 2.871 | 10 | 24 | fits | 225,058 | 77 | 0.041 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 141,829 | 2.837 | 10 | 24 | fits | 223,321 | 73 | 0.041 |
| get_configuration | `aecp.get_configuration.if0` | 144,744 | 2.895 | 10 | 24 | fits | 226,196 | 56 | 0.049 |
| entity_available | `aecp.entity_available.if0` | 124,801 | 2.496 | 10 | 24 | fits | 206,207 | 53 | 0.043 |
| get_name | `aecp.get_name.if0` | 151,980 | 3.040 | 10 | 24 | fits | 233,435 | 73 | 0.048 |
| get_counters | `aecp.get_counters.if0` | 138,609 | 2.772 | 10 | 24 | fits | 220,104 | 87 | 0.044 |
| get_avb_info | `aecp.get_avb_info.if0` | 229,435 | 4.589 | 10 | 24 | fits | 212,910 | 50 | 0.042 |
| unknown_command | `aecp.unknown_command.if0` | 122,764 | 2.455 | 10 | 24 | fits | 204,170 | 49 | 0.043 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 110,183 | 2.204 | 10 | 24 | fits | 191,638 | 60 | 0.055 |
| set_name | `aecp.set_name.if0` | 216,835 | 4.337 | 10 | 24 | fits | 367,106 | 156 | 0.037 |
| lock_entity | `aecp.lock_entity.if0` | 167,801 | 3.356 | 10 | 24 | fits | 260,594 | 97 | 0.047 |
| unlock_entity | `aecp.unlock_entity.if0` | 167,779 | 3.356 | 10 | 24 | fits | 260,501 | 97 | 0.047 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 88,024 | 1.760 | 10 | 24 | fits | 169,449 | 47 | 0.050 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 179,477 | 3.590 | 10 | 24 | fits | 260,991 | 132 | 0.044 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 134,848 | 2.697 | 10 | 24 | fits | 216,362 | 73 | 0.042 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 167,547 | 3.351 | 10 | 24 | fits | 221,325 | 85 | 0.041 |
| get_configuration | `aecp.get_configuration.if1` | 144,460 | 2.889 | 10 | 24 | fits | 226,032 | 54 | 0.049 |
| entity_available | `aecp.entity_available.if1` | 146,353 | 2.927 | 10 | 24 | fits | 227,925 | 58 | 0.048 |
| get_name | `aecp.get_name.if1` | 152,435 | 3.049 | 10 | 24 | fits | 234,007 | 71 | 0.048 |
| get_counters | `aecp.get_counters.if1` | 138,409 | 2.768 | 10 | 24 | fits | 220,021 | 85 | 0.044 |
| get_avb_info | `aecp.get_avb_info.if1` | 130,919 | 2.618 | 10 | 24 | fits | 212,491 | 47 | 0.042 |
| unknown_command | `aecp.unknown_command.if1` | 144,226 | 2.885 | 10 | 24 | fits | 225,798 | 54 | 0.048 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 88,885 | 1.778 | 10 | 24 | fits | 170,408 | 52 | 0.050 |
| set_name | `aecp.set_name.if1` | 198,012 | 3.960 | 10 | 24 | fits | 332,322 | 149 | 0.036 |
| lock_entity | `aecp.lock_entity.if1` | 146,236 | 2.925 | 10 | 24 | fits | 246,820 | 109 | 0.043 |
| unlock_entity | `aecp.unlock_entity.if1` | 146,223 | 2.924 | 10 | 24 | fits | 246,492 | 109 | 0.043 |

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
- `aecp`: wait quiet TIMEOUT
