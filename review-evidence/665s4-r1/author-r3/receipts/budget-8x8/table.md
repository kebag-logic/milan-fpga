### 8x8

30 of 129 paths and 62 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.000 (4.233) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 16.902 (37.056) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 16.452 (36.453) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 4.996 (24.996) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 22.798 (53.410) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 24.077 (53.410) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 21.852 (29.824) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 23.099 (29.824) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 18.849 (38.726) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 5.782 (33.891) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 16.465 (36.465) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 5.009 (25.009) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 1.157 (21.152) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 8.833 (28.827) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 16.815 (36.495) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 5.366 (25.036) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 4.417 (21.399) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 7.100 (28.712) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 6.866 (44.977) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 5.403 (48.152) | fits | 2 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 7.561 (45.634) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 1.172 (24.620) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 2.490 (20.749) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 7.741 (45.286) | fits | 3 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 2.891 (24.261) | fits | 1 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 6.586 (48.519) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 3.466 (24.602) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 6.332 (48.024) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 3.481 (24.219) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 3.602 (44.639) | fits | 2 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 12.306 (32.506) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 13.426 (25.399) | MISS T_svc | 0 acmp | 1 | 1 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.631 (2.806) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.807 (2.806) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.511 (2.623) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.596 (2.623) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.493 (13.016) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.500 (13.016) | fits | 1 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.082 (12.211) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.861 (12.211) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.550 (3.570) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 1.454 (3.570) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 1.477 (5.921) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.875 (4.921) | fits | 1 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.495 (4.126) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.926 (4.558) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 3.637 (13.490) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 3.048 (4.680) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.460 (4.091) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.885 (4.517) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.768 (4.399) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 2.764 (4.395) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 3.037 (4.668) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 3.055 (4.687) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.919 (4.777) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.920 (4.934) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.775 (3.406) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 1.776 (3.407) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.595 (5.227) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.586 (5.218) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.695 (4.326) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.691 (4.323) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 3.128 (4.760) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.663 (4.294) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.485 (5.116) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.563 (4.194) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 3.011 (4.642) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 3.224 (4.855) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 2.785 (4.416) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 2.827 (4.458) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.866 (4.497) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 3.267 (4.899) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 2.796 (4.427) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 2.807 (4.439) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.712 (4.343) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.771 (3.395) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 1.762 (3.393) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.329 (7.335) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.957 (6.646) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 3.388 (7.033) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.447 (4.078) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.919 (4.776) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.920 (4.930) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.180 (11.864) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 9.732 (13.415) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.189 (9.671) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 7.779 (9.263) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 9.157 (12.841) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 9.347 (13.030) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.416 (14.136) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 12.398 (16.599) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 7.650 (11.148) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.339 (9.989) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 9.778 (13.463) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 58.596 (64.415) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 47.659 (66.408) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 53.368 (68.302) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 14.803 (28.595) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 122.150 (127.877) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 370.764 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 3.130 (7.163) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.174 (6.264) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 1.074 (3.034) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.636 (2.620) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.757 (6.890) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 1.187 (7.347) | fits | 1 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 2.982 (7.163) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.026 (6.264) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 2.248 (6.672) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 0.993 (5.049) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 14.258 | MISS T_svc | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 103.840 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 14.301 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 63.883 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 47.909 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 14.294 | MISS T_svc | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 314.391 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 14.284 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 58.806 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 593.354 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 593.334 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 8.296 (10.059) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 7.926 (9.605) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.297 (3.297) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.366 (3.366) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 3.060 (3.061) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 5.382 (7.558) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.400 (6.890) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.483 (6.917) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 159.990 | 25 | 715,141 (14.303) | yes | - |
| backlog-adp | 547.712 | 29 | 1,459,629 (29.193) | no | {'srp': 32} |
| backlog-adp-refill | 593.371 | 31 | 1,459,540 (29.191) | no | {'srp': 32} |
| backlog-owed | 370.815 | 42 | 624,548 (12.491) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,459,629 CPU cycles (29.193 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 715,141 (14.303 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 173,276 | 3.466 | 10 | 20 | fits | 1,230,096 | 166 (14) | 0.025 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 316,615 | 6.332 | 10 | 20 | fits | 1,032,082 | 127 (14) | 0.028 |
| LINK_UP | `adp.link_up.if0` | 4,084 | 0.082 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,060 | 0.861 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 73,834 | 1.477 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 43,738 | 0.875 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 77,477 | 1.550 | 10 | 200 | fits | 8,946 | 18 (11) | 0.152 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 72,719 | 1.454 | 10 | 200 | fits | 8,946 | 18 (11) | 0.152 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 37,858 | 0.757 | 10 | 50 | fits | 344,495 | 154 | 0.038 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 112,407 | 2.248 | 10 | 50 | fits | 153,484 | 44 | 0.065 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 63,135 | 1.263 | 10 | 50 | fits | 132,271 | 38 | 0.060 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 149,107 | 2.982 | 10 | 50 | fits | 171,675 | 71 | 0.064 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 156,517 | 3.130 | 10 | 50 | fits | 171,675 | 71 | 0.064 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 53,679 | 1.074 | 10 | 50 | fits | 151,722 | 54 | 0.060 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 59,371 | 1.187 | 10 | 50 | fits | 367,353 | 160 | 0.040 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 45,666 | 0.913 | 10 | 50 | fits | 133,773 | 38 | 0.059 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 49,641 | 0.993 | 10 | 50 | fits | 133,744 | 38 | 0.059 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 101,278 | 2.026 | 10 | 50 | fits | 151,881 | 65 | 0.059 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 108,688 | 2.174 | 10 | 50 | fits | 151,881 | 65 | 0.059 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 31,822 | 0.636 | 10 | 50 | fits | 131,018 | 47 | 0.052 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 124,489 | 2.490 | 10 | 20 | fits | 1,037,440 | 149 (35) | 0.028 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 387,057 | 7.741 | 10 | 20 | fits | 1,226,852 | 166 (35) | 0.025 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 144,571 | 2.891 | 10 | 20 | fits | 1,213,072 | 143 (14) | 0.024 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 329,316 | 6.586 | 10 | 20 | fits | 1,212,901 | 143 (14) | 0.024 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 174,043 | 3.481 | 10 | 20 | fits | 1,210,967 | 144 (14) | 0.025 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 180,078 | 3.602 | 10 | 20 | fits | 1,020,999 | 126 (14) | 0.027 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 343,278 | 6.866 | 10 | 20 | fits | 1,227,873 | 166 (35) | 0.025 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 270,128 | 5.403 | 10 | 20 | fits | 1,228,987 | 166 (35) | 0.025 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 319,996 | 6.400 | 10 | 18 | fits | 344,495 | 154 | 0.038 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 324,144 | 6.483 | 10 | 18 | fits | 345,841 | 154 | 0.037 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 164,832 | 3.297 | 10 | 18 | fits | 164,864 | 29 | 0.065 |
| malformed MRPDU discard | `srp.malformed.if0` | 152,993 | 3.060 | 10 | 18 | fits | 153,025 | 36 | 0.058 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 414,800 | 8.296 | 210 | 218 | fits | 502,972 | 149 | 0.046 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 168,276 | 3.366 | 10 | 18 | fits | 168,308 | 29 | 0.065 |
| malformed MRPDU discard | `srp.malformed.if1` | 269,110 | 5.382 | 10 | 18 | fits | 160,629 | 36 | 0.056 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 396,283 | 7.926 | 210 | 218 | fits | 480,247 | 142 | 0.044 |
| an event behind 15 others | `backlog.event.if0` | 740,148 | 14.803 | 10 | 200 | MISS T_svc | 714,623 | 377 | 0.052 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,929,814 | 58.596 | 10 | 20 | MISS ceiling | 412,441 | 219 | 0.036 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 715,037 | 14.301 | 10 | 200 | MISS T_svc | 715,141 | 394 | 0.051 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,395,454 | 47.909 | 10 | 200 | MISS T_svc | 446,827 | 287 | 0.036 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 712,908 | 14.258 | 10 | 20 | MISS T_svc | 715,141 | 394 | 0.051 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,218,129 | 64.363 | 10 | 20 | MISS ceiling | 412,441 | 219 | 0.036 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 714,700 | 14.294 | 10 | 24 | MISS T_svc | 715,141 | 394 | 0.051 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,257,004 | 125.140 | 10 | 24 | MISS ceiling | 247,949 | 126 | 0.037 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 714,180 | 14.284 | 10 | 50 | MISS T_svc | 715,141 | 394 | 0.051 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,394,706 | 47.894 | 10 | 50 | MISS T_svc | 446,827 | 287 | 0.036 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,555,061 | 71.101 | 10 | 18 | MISS ceiling | 335,474 | 171 | 0.051 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,557,332 | 151.147 | 10 | 18 | MISS ceiling | 152,133 | 48 | 0.060 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,382,945 | 47.659 | 10 | 20 | MISS ceiling | 1,161,952 | 403 | 0.030 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 605,252 | 12.105 | 10 | 200 | MISS T_svc | 986,864 | 427 | 0.032 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,938,481 | 58.770 | 10 | 200 | MISS T_svc | 1,161,952 | 403 | 0.030 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 605,708 | 12.114 | 10 | 20 | MISS T_svc | 986,864 | 427 | 0.032 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 5,170,695 | 103.414 | 10 | 20 | MISS ceiling | 1,169,529 | 319 | 0.028 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 607,500 | 12.150 | 10 | 24 | MISS T_svc | 986,864 | 427 | 0.032 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 15,698,446 | 313.969 | 10 | 24 | MISS ceiling | 1,019,249 | 232 | 0.028 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 606,980 | 12.140 | 10 | 50 | MISS T_svc | 986,864 | 427 | 0.032 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,940,319 | 58.806 | 10 | 50 | MISS ceiling | 1,161,952 | 403 | 0.030 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,384,750 | 547.695 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,383,743 | 547.675 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,668,423 | 53.368 | 10 | 20 | MISS ceiling | 1,124,672 | 341 | 0.029 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 605,252 | 12.105 | 10 | 200 | MISS T_svc | 986,864 | 427 | 0.032 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 3,194,171 | 63.883 | 10 | 200 | MISS T_svc | 1,124,672 | 341 | 0.029 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 605,708 | 12.114 | 10 | 20 | MISS T_svc | 986,864 | 427 | 0.032 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 5,191,977 | 103.840 | 10 | 20 | MISS ceiling | 1,124,672 | 341 | 0.029 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 607,500 | 12.150 | 10 | 24 | MISS T_svc | 986,864 | 427 | 0.032 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,719,549 | 314.391 | 10 | 24 | MISS ceiling | 1,019,250 | 232 | 0.028 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 606,980 | 12.140 | 10 | 50 | MISS T_svc | 986,864 | 427 | 0.032 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,884,590 | 57.692 | 10 | 50 | MISS ceiling | 1,106,223 | 396 | 0.030 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,667,686 | 593.354 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,666,679 | 593.334 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,107,510 | 122.150 | 10 | 20 | MISS ceiling | 305,594 | 148 | 0.034 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,538,221 | 370.764 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,538,183 | 370.764 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,538,146 | 370.763 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,538,108 | 370.762 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 559,568 | 11.191 | 10 | 200 | MISS T_svc | 481,047 | 346 | 0.037 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 2,185,184 | 43.704 | 10 | 200 | MISS T_svc | 504,713 | 283 | 0.039 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 557,439 | 11.149 | 10 | 20 | MISS T_svc | 481,047 | 346 | 0.037 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,155,049 | 63.101 | 10 | 20 | MISS ceiling | 503,622 | 215 | 0.041 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 559,231 | 11.185 | 10 | 24 | MISS T_svc | 481,047 | 346 | 0.037 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,031,617 | 140.632 | 10 | 24 | MISS ceiling | 368,621 | 171 | 0.051 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 558,711 | 11.174 | 10 | 50 | MISS T_svc | 481,047 | 346 | 0.037 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,184,436 | 43.689 | 10 | 50 | MISS T_svc | 504,713 | 283 | 0.039 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,679,691 | 33.594 | 10 | 18 | MISS ceiling | 624,548 | 345 | 0.048 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 8,027,638 | 160.553 | 10 | 18 | MISS ceiling | 152,530 | 30 | 0.060 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 1,092,601 | 21.852 | 10 | 20 | MISS ceiling | 1,491,203 | 208 (29) | 0.023 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 1,154,928 | 23.099 | 10 | 20 | MISS ceiling | 1,491,203 | 208 (29) | 0.023 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,139,896 | 22.798 | 10 | 20 | MISS ceiling | 1,304,630 | 202 (35) | 0.025 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,203,839 | 24.077 | 10 | 20 | MISS ceiling | 1,304,630 | 202 (35) | 0.025 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 378,073 | 7.561 | 10 | 20 | fits | 1,006,934 | 116 (12) | 0.022 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 58,581 | 1.172 | 10 | 20 | fits | 1,230,977 | 166 (12) | 0.025 |
| LINK_UP | `adp.link_up.if0` | 4,084 | 0.082 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,060 | 0.861 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 73,834 | 1.477 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 43,738 | 0.875 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| LINK_DOWN | `adp.link_down.if0` | 24,642 | 0.493 | 10 | 200 | fits | 650,786 | 58 (9) | 0.077 |
| LINK_DOWN | `adp.link_down.if1` | 274,997 | 5.500 | 10 | 200 | fits | 650,786 | 58 (9) | 0.077 |
| LINK_UP | `adp.link_up.if0` | 4,084 | 0.082 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,060 | 0.861 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 73,834 | 1.477 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 43,738 | 0.875 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| GM_CHANGE | `adp.gm_change.if0` | 25,574 | 0.511 | 10 | 200 | fits | 131,146 | 34 (11) | 0.063 |
| GM_CHANGE | `adp.gm_change.if1` | 29,789 | 0.596 | 10 | 200 | fits | 131,146 | 34 (11) | 0.063 |
| LINK_UP | `adp.link_up.if0` | 4,084 | 0.082 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,060 | 0.861 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 73,834 | 1.477 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 43,738 | 0.875 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 31,552 | 0.631 | 10 | 200 | fits | 140,319 | 73 (31) | 0.059 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 40,359 | 0.807 | 10 | 200 | fits | 140,319 | 73 (31) | 0.059 |
| LINK_UP | `adp.link_up.if0` | 4,084 | 0.082 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 43,060 | 0.861 | 10 | 200 | fits | 610,573 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 73,834 | 1.477 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 43,738 | 0.875 | 10 | 200 | fits | 140,758 | 84 (39) | 0.057 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 31,552 | 0.631 | 10 | 200 | fits | 131,733 | 45 (31) | 0.060 |
| set_name | `aecp_fanout.set_name.if0` | 570,787 | 11.416 | 10 | 24 | MISS T_svc | 706,823 | 1172 | 0.035 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 409,430 | 8.189 | 10 | 24 | fits | 483,568 | 620 | 0.053 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 457,868 | 9.157 | 10 | 24 | fits | 479,162 | 587 | 0.051 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 444,441 | 8.889 | 10 | 24 | fits | 457,245 | 580 | 0.049 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 382,515 | 7.650 | 10 | 24 | fits | 434,003 | 592 | 0.053 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 408,997 | 8.180 | 10 | 24 | fits | 478,775 | 680 | 0.048 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 416,937 | 8.339 | 10 | 24 | fits | 499,457 | 686 | 0.050 |
| set_name | `aecp_fanout.set_name.if1` | 619,924 | 12.398 | 10 | 24 | MISS T_svc | 658,740 | 1132 | 0.035 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 388,962 | 7.779 | 10 | 24 | fits | 463,138 | 613 | 0.051 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 458,890 | 9.178 | 10 | 24 | fits | 458,804 | 580 | 0.049 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 467,336 | 9.347 | 10 | 24 | fits | 458,174 | 580 | 0.049 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 486,597 | 9.732 | 10 | 24 | fits | 477,411 | 679 | 0.048 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 488,880 | 9.778 | 10 | 24 | fits | 479,426 | 679 | 0.048 |
| BIND_RX | `acmp.bind_rx.if0` | 49,998 | 1.000 | 10 | 20 | fits | 211,662 | 83 (77) | 0.046 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 220,842 | 4.417 | 10 | 20 | fits | 1,069,975 | 154 (32) | 0.028 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 942,429 | 18.849 | 10 | 20 | MISS T_svc | 1,060,061 | 169 (47) | 0.026 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 615,316 | 12.306 | 10 | 20 | MISS T_svc | 749,690 | 204 (50) | 0.036 |
| PROBE_TX | `acmp.probe_tx.if0` | 840,760 | 16.815 | 10 | 20 | MISS T_svc | 950,248 | 161 (48) | 0.029 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 57,865 | 1.157 | 10 | 20 | fits | 1,057,578 | 170 (48) | 0.026 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 822,624 | 16.452 | 10 | 20 | MISS T_svc | 948,195 | 160 (48) | 0.029 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 823,235 | 16.465 | 10 | 20 | MISS T_svc | 948,408 | 160 (48) | 0.029 |
| BIND_RX | `acmp.bind_rx.if1` | 845,081 | 16.902 | 10 | 20 | MISS T_svc | 977,826 | 190 (77) | 0.030 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 355,005 | 7.100 | 10 | 20 | fits | 1,435,610 | 187 (32) | 0.024 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 289,104 | 5.782 | 10 | 20 | fits | 1,694,545 | 401 (47) | 0.024 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 671,320 | 13.426 | 10 | 20 | MISS T_svc | 1,269,933 | 188 (50) | 0.027 |
| PROBE_TX | `acmp.probe_tx.if1` | 268,295 | 5.366 | 10 | 20 | fits | 1,251,793 | 187 (48) | 0.026 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 441,645 | 8.833 | 10 | 20 | fits | 1,441,358 | 203 (48) | 0.024 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 249,785 | 4.996 | 10 | 20 | fits | 1,249,809 | 186 (48) | 0.026 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 250,454 | 5.009 | 10 | 20 | fits | 1,250,457 | 186 (48) | 0.026 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 88,565 | 1.771 | 10 | 24 | fits | 169,742 | 50 | 0.049 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 179,760 | 3.595 | 10 | 24 | fits | 261,336 | 134 | 0.043 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 134,774 | 2.695 | 10 | 24 | fits | 216,324 | 75 | 0.041 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 161,198 | 3.224 | 10 | 24 | fits | 242,771 | 93 | 0.045 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 139,797 | 2.796 | 10 | 24 | fits | 221,350 | 85 | 0.040 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 140,373 | 2.807 | 10 | 24 | fits | 221,926 | 85 | 0.040 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 135,613 | 2.712 | 10 | 24 | fits | 217,166 | 74 | 0.041 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 156,406 | 3.128 | 10 | 24 | fits | 237,982 | 77 | 0.046 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 133,147 | 2.663 | 10 | 24 | fits | 214,697 | 67 | 0.041 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 174,251 | 3.485 | 10 | 24 | fits | 255,801 | 162 | 0.035 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 128,170 | 2.563 | 10 | 24 | fits | 209,720 | 54 | 0.042 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 150,533 | 3.011 | 10 | 24 | fits | 232,106 | 61 | 0.047 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 141,359 | 2.827 | 10 | 24 | fits | 222,909 | 71 | 0.039 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 143,303 | 2.866 | 10 | 24 | fits | 224,853 | 77 | 0.039 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 163,363 | 3.267 | 10 | 24 | fits | 244,936 | 80 | 0.045 |
| get_configuration | `aecp.get_configuration.if0` | 122,997 | 2.460 | 10 | 24 | fits | 204,534 | 49 | 0.043 |
| entity_available | `aecp.entity_available.if0` | 124,748 | 2.495 | 10 | 24 | fits | 206,288 | 53 | 0.042 |
| get_name | `aecp.get_name.if0` | 151,843 | 3.037 | 10 | 24 | fits | 233,406 | 73 | 0.047 |
| get_counters | `aecp.get_counters.if0` | 138,389 | 2.768 | 10 | 24 | fits | 219,942 | 87 | 0.042 |
| get_avb_info | `aecp.get_avb_info.if0` | 181,867 | 3.637 | 10 | 24 | fits | 674,499 | 272 | 0.028 |
| unknown_command | `aecp.unknown_command.if0` | 169,401 | 3.388 | 10 | 24 | fits | 204,335 | 50 | 0.042 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 88,741 | 1.775 | 10 | 24 | fits | 170,281 | 53 | 0.049 |
| set_name | `aecp.set_name.if0` | 216,452 | 4.329 | 10 | 24 | fits | 366,759 | 156 | 0.036 |
| lock_entity | `aecp.lock_entity.if0` | 145,964 | 2.919 | 10 | 24 | fits | 238,852 | 90 | 0.042 |
| unlock_entity | `aecp.unlock_entity.if0` | 145,962 | 2.919 | 10 | 24 | fits | 238,812 | 90 | 0.042 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 88,110 | 1.762 | 10 | 24 | fits | 169,639 | 47 | 0.050 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 179,284 | 3.586 | 10 | 24 | fits | 260,879 | 132 | 0.043 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 134,566 | 2.691 | 10 | 24 | fits | 216,138 | 73 | 0.041 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 139,227 | 2.785 | 10 | 24 | fits | 220,799 | 84 | 0.040 |
| get_configuration | `aecp.get_configuration.if1` | 144,228 | 2.885 | 10 | 24 | fits | 225,826 | 54 | 0.048 |
| entity_available | `aecp.entity_available.if1` | 146,296 | 2.926 | 10 | 24 | fits | 227,894 | 58 | 0.047 |
| get_name | `aecp.get_name.if1` | 152,748 | 3.055 | 10 | 24 | fits | 234,346 | 71 | 0.047 |
| get_counters | `aecp.get_counters.if1` | 138,178 | 2.764 | 10 | 24 | fits | 219,766 | 85 | 0.042 |
| get_avb_info | `aecp.get_avb_info.if1` | 152,381 | 3.048 | 10 | 24 | fits | 233,979 | 54 | 0.046 |
| unknown_command | `aecp.unknown_command.if1` | 122,326 | 2.447 | 10 | 24 | fits | 203,901 | 47 | 0.042 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 88,788 | 1.776 | 10 | 24 | fits | 170,363 | 52 | 0.049 |
| set_name | `aecp.set_name.if1` | 197,861 | 3.957 | 10 | 24 | fits | 332,283 | 149 | 0.036 |
| lock_entity | `aecp.lock_entity.if1` | 145,979 | 2.920 | 10 | 24 | fits | 246,696 | 109 | 0.042 |
| unlock_entity | `aecp.unlock_entity.if1` | 145,977 | 2.920 | 10 | 24 | fits | 246,482 | 109 | 0.042 |

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
