### 8x8

29 of 129 paths and 61 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.973 (4.110) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 15.429 (35.575) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 15.011 (35.014) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 3.990 (23.993) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 16.514 (28.715) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 17.758 (28.715) | MISS T_svc | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 18.989 (28.662) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 20.209 (28.662) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 17.359 (37.244) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 4.156 (24.056) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 17.121 (37.120) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 7.675 (27.675) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 15.041 (35.034) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 7.719 (27.705) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.691 (20.383) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 8.641 (20.354) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 3.100 (20.588) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 6.045 (27.586) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 3.583 (19.889) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 8.656 (49.794) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 5.582 (46.709) | fits | 2 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 3.128 (46.159) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 7.382 (47.036) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 6.808 (47.036) | fits | 3 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 2.233 (20.324) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 2.351 (20.324) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 8.458 (46.170) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 7.579 (46.125) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 7.088 (46.431) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 7.542 (46.431) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 10.995 (31.185) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 8.434 (36.600) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.187 (2.257) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.355 (2.257) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.059 (2.051) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.127 (2.051) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.045 (11.570) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 4.628 (11.570) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.062 (11.680) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.762 (11.680) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.405 (3.398) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.477 (2.398) | fits | 1 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.999 (5.202) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.358 (2.645) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.774 (4.366) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.771 (4.363) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.904 (4.495) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.499 (4.084) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.340 (3.927) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.734 (4.325) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 3.026 (4.618) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 3.023 (4.615) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.899 (4.491) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 2.891 (4.482) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.359 (4.161) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.360 (4.307) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.060 (3.649) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 2.056 (3.646) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.441 (5.035) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.036 (4.626) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.582 (4.169) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.976 (4.568) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 2.577 (4.164) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.548 (4.135) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.771 (5.363) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.850 (4.442) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 2.459 (4.046) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 3.075 (4.667) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 2.670 (4.258) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 3.107 (4.699) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 3.153 (4.745) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 3.119 (4.711) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 3.084 (4.676) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 3.096 (4.688) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.597 (4.185) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.655 (3.234) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 2.112 (5.613) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 3.769 (6.314) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.385 (6.004) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.334 (3.920) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.733 (4.324) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 3.347 (13.131) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.771 (4.721) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 7.461 (9.068) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 7.437 (9.044) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 6.914 (8.345) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 6.920 (8.372) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 7.420 (10.960) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 7.202 (10.742) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.007 (13.279) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 11.503 (15.553) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 7.289 (10.636) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 7.050 (8.653) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 7.609 (11.147) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 56.152 (63.137) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 41.065 (63.933) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 47.278 (63.467) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 13.916 (27.053) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 116.148 (121.690) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 371.465 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 2.346 (6.581) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.549 (6.840) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.598 (2.463) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.594 (2.483) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.690 (6.628) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.679 (6.636) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 2.199 (6.581) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.402 (6.840) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.524 (5.320) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 2.083 (5.937) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 13.489 | MISS T_svc | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 97.486 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 13.531 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 57.530 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 45.753 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 13.525 | MISS T_svc | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 300.061 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 13.514 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 51.925 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 587.263 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 587.243 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 7.487 (9.097) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 7.615 (9.152) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.127 (3.128) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.178 (3.179) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 2.433 (2.434) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 2.496 (2.497) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.196 (6.628) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.262 (6.639) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 151.165 | 24 | 676,669 (13.533) | yes | - |
| backlog-adp | 541.118 | 29 | 1,408,512 (28.170) | no | {'srp': 32} |
| backlog-adp-refill | 587.280 | 32 | 1,408,341 (28.167) | no | {'srp': 32} |
| backlog-owed | 371.516 | 45 | 564,565 (11.291) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,408,512 CPU cycles (28.170 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 676,669 (13.533 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 422,914 | 8.458 | 10 | 20 | fits | 1,180,051 | 96 (14) | 0.010 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 378,948 | 7.579 | 10 | 20 | fits | 993,248 | 71 (14) | 0.012 |
| LINK_UP | `adp.link_up.if0` | 3,085 | 0.062 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| LINK_UP | `adp.link_up.if1` | 38,077 | 0.762 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 49,932 | 0.999 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,882 | 0.358 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 70,272 | 1.405 | 10 | 200 | fits | 6,576 | 18 (11) | 0.035 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 23,834 | 0.477 | 10 | 200 | fits | 6,576 | 18 (11) | 0.035 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 34,499 | 0.690 | 10 | 50 | fits | 331,403 | 153 | 0.017 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 76,202 | 1.524 | 10 | 50 | fits | 124,407 | 38 | 0.025 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 38,783 | 0.776 | 10 | 50 | fits | 124,513 | 38 | 0.025 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 109,949 | 2.199 | 10 | 50 | fits | 161,722 | 71 | 0.028 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 117,295 | 2.346 | 10 | 50 | fits | 161,722 | 71 | 0.028 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 29,876 | 0.598 | 10 | 50 | fits | 123,140 | 48 | 0.020 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 33,927 | 0.679 | 10 | 50 | fits | 331,794 | 154 | 0.014 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 61,248 | 1.225 | 10 | 50 | fits | 125,876 | 38 | 0.024 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 104,159 | 2.083 | 10 | 50 | fits | 125,656 | 38 | 0.022 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 120,088 | 2.402 | 10 | 50 | fits | 163,464 | 71 | 0.029 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 127,434 | 2.549 | 10 | 50 | fits | 163,464 | 71 | 0.029 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 29,715 | 0.594 | 10 | 50 | fits | 124,140 | 47 | 0.019 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 369,081 | 7.382 | 10 | 20 | fits | 1,041,626 | 119 (35) | 0.010 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 340,399 | 6.808 | 10 | 20 | fits | 1,041,626 | 119 (35) | 0.010 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 111,652 | 2.233 | 10 | 20 | fits | 1,016,218 | 73 (14) | 0.010 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 117,532 | 2.351 | 10 | 20 | fits | 1,016,218 | 73 (14) | 0.010 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 354,415 | 7.088 | 10 | 20 | fits | 1,010,434 | 74 (14) | 0.010 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 377,110 | 7.542 | 10 | 20 | fits | 1,010,434 | 74 (14) | 0.010 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 179,130 | 3.583 | 10 | 20 | fits | 994,467 | 93 (35) | 0.011 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 432,819 | 8.656 | 10 | 20 | fits | 1,177,884 | 96 (35) | 0.009 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 309,820 | 6.196 | 10 | 18 | fits | 331,403 | 153 | 0.017 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 313,083 | 6.262 | 10 | 18 | fits | 331,929 | 154 | 0.014 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 156,351 | 3.127 | 10 | 18 | fits | 156,383 | 29 | 0.032 |
| malformed MRPDU discard | `srp.malformed.if0` | 121,670 | 2.433 | 10 | 18 | fits | 121,702 | 30 | 0.025 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 374,328 | 7.487 | 210 | 218 | fits | 454,867 | 143 | 0.016 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 158,924 | 3.178 | 10 | 18 | fits | 158,956 | 29 | 0.029 |
| malformed MRPDU discard | `srp.malformed.if1` | 124,823 | 2.496 | 10 | 18 | fits | 124,855 | 29 | 0.023 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 380,746 | 7.615 | 210 | 218 | fits | 457,578 | 142 | 0.015 |
| an event behind 15 others | `backlog.event.if0` | 695,803 | 13.916 | 10 | 200 | MISS T_svc | 675,967 | 375 | 0.018 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,807,617 | 56.152 | 10 | 20 | MISS ceiling | 467,186 | 256 | 0.024 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 676,565 | 13.531 | 10 | 200 | MISS T_svc | 676,669 | 392 | 0.017 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,287,653 | 45.753 | 10 | 200 | MISS T_svc | 434,881 | 285 | 0.020 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 674,436 | 13.489 | 10 | 20 | MISS T_svc | 676,669 | 392 | 0.017 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,154,200 | 63.084 | 10 | 20 | MISS ceiling | 467,186 | 256 | 0.024 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 676,228 | 13.525 | 10 | 24 | MISS T_svc | 676,669 | 392 | 0.017 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,026,059 | 120.521 | 10 | 24 | MISS ceiling | 310,334 | 169 | 0.025 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 675,708 | 13.514 | 10 | 50 | MISS T_svc | 676,669 | 392 | 0.017 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,286,905 | 45.738 | 10 | 50 | MISS T_svc | 434,881 | 285 | 0.020 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,155,658 | 63.113 | 10 | 18 | MISS ceiling | 467,186 | 256 | 0.024 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,260,831 | 145.217 | 10 | 18 | MISS ceiling | 168,467 | 54 | 0.031 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,053,244 | 41.065 | 10 | 20 | MISS ceiling | 893,846 | 360 | 0.016 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 592,807 | 11.856 | 10 | 200 | MISS T_svc | 1,194,731 | 405 | 0.013 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,594,425 | 51.889 | 10 | 200 | MISS T_svc | 893,846 | 360 | 0.016 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 593,263 | 11.865 | 10 | 20 | MISS T_svc | 1,194,731 | 405 | 0.013 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,852,495 | 97.050 | 10 | 20 | MISS ceiling | 1,128,767 | 275 | 0.013 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 595,055 | 11.901 | 10 | 24 | MISS T_svc | 1,194,731 | 405 | 0.013 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 14,982,140 | 299.643 | 10 | 24 | MISS ceiling | 981,019 | 188 | 0.012 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 594,535 | 11.891 | 10 | 50 | MISS T_svc | 1,194,731 | 405 | 0.013 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,596,263 | 51.925 | 10 | 50 | MISS ceiling | 893,846 | 360 | 0.016 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,055,049 | 541.101 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,054,042 | 541.081 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,363,889 | 47.278 | 10 | 20 | MISS ceiling | 1,190,472 | 307 | 0.013 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 592,807 | 11.856 | 10 | 200 | MISS T_svc | 1,194,731 | 405 | 0.013 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,876,487 | 57.530 | 10 | 200 | MISS T_svc | 1,190,472 | 307 | 0.013 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 593,263 | 11.865 | 10 | 20 | MISS T_svc | 1,194,731 | 405 | 0.013 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,874,293 | 97.486 | 10 | 20 | MISS ceiling | 1,190,472 | 307 | 0.013 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 595,055 | 11.901 | 10 | 24 | MISS T_svc | 1,194,731 | 405 | 0.013 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,003,058 | 300.061 | 10 | 24 | MISS ceiling | 980,070 | 188 | 0.011 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 594,535 | 11.891 | 10 | 50 | MISS T_svc | 1,194,731 | 405 | 0.013 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,541,693 | 50.834 | 10 | 50 | MISS ceiling | 839,276 | 353 | 0.016 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,363,152 | 587.263 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,362,145 | 587.243 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,807,386 | 116.148 | 10 | 20 | MISS ceiling | 405,748 | 191 | 0.024 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,573,268 | 371.465 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,573,230 | 371.465 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,573,193 | 371.464 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,573,155 | 371.463 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 509,734 | 10.195 | 10 | 200 | MISS T_svc | 461,551 | 344 | 0.016 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 1,882,833 | 37.657 | 10 | 200 | MISS T_svc | 434,206 | 261 | 0.020 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 507,605 | 10.152 | 10 | 20 | MISS T_svc | 461,551 | 344 | 0.016 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 2,646,189 | 52.924 | 10 | 20 | MISS ceiling | 407,554 | 120 | 0.026 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 509,397 | 10.188 | 10 | 24 | MISS T_svc | 461,551 | 344 | 0.016 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,942,281 | 138.846 | 10 | 24 | MISS ceiling | 353,422 | 169 | 0.025 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 508,877 | 10.178 | 10 | 50 | MISS T_svc | 461,551 | 344 | 0.016 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,882,085 | 37.642 | 10 | 50 | MISS T_svc | 434,206 | 261 | 0.020 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 2,647,647 | 52.953 | 10 | 18 | MISS ceiling | 407,554 | 120 | 0.026 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 7,843,973 | 156.879 | 10 | 18 | MISS ceiling | 172,293 | 36 | 0.031 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 949,454 | 18.989 | 10 | 20 | MISS T_svc | 1,433,089 | 124 (29) | 0.008 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 1,010,470 | 20.209 | 10 | 20 | MISS ceiling | 1,433,089 | 124 (29) | 0.008 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 825,719 | 16.514 | 10 | 20 | MISS T_svc | 1,435,742 | 135 (35) | 0.009 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 887,894 | 17.758 | 10 | 20 | MISS T_svc | 1,435,742 | 135 (35) | 0.009 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 279,119 | 5.582 | 10 | 20 | fits | 928,954 | 68 (12) | 0.012 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 156,396 | 3.128 | 10 | 20 | fits | 996,499 | 93 (12) | 0.012 |
| LINK_UP | `adp.link_up.if0` | 3,085 | 0.062 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| LINK_UP | `adp.link_up.if1` | 38,077 | 0.762 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 49,932 | 0.999 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,882 | 0.358 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| LINK_DOWN | `adp.link_down.if0` | 2,249 | 0.045 | 10 | 200 | fits | 578,516 | 52 (9) | 0.020 |
| LINK_DOWN | `adp.link_down.if1` | 231,421 | 4.628 | 10 | 200 | fits | 578,516 | 52 (9) | 0.020 |
| LINK_UP | `adp.link_up.if0` | 3,085 | 0.062 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| LINK_UP | `adp.link_up.if1` | 38,077 | 0.762 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 49,932 | 0.999 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,882 | 0.358 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| GM_CHANGE | `adp.gm_change.if0` | 2,930 | 0.059 | 10 | 200 | fits | 102,537 | 28 (11) | 0.020 |
| GM_CHANGE | `adp.gm_change.if1` | 6,351 | 0.127 | 10 | 200 | fits | 102,537 | 28 (11) | 0.020 |
| LINK_UP | `adp.link_up.if0` | 3,085 | 0.062 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| LINK_UP | `adp.link_up.if1` | 38,077 | 0.762 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 49,932 | 0.999 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,882 | 0.358 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 9,340 | 0.187 | 10 | 200 | fits | 112,870 | 67 (31) | 0.020 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 17,749 | 0.355 | 10 | 200 | fits | 112,870 | 67 (31) | 0.020 |
| LINK_UP | `adp.link_up.if0` | 3,085 | 0.062 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| LINK_UP | `adp.link_up.if1` | 38,077 | 0.762 | 10 | 200 | fits | 584,013 | 304 (11) | 0.011 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 49,932 | 0.999 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,882 | 0.358 | 10 | 200 | fits | 132,232 | 84 (39) | 0.020 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 9,340 | 0.187 | 10 | 200 | fits | 104,685 | 39 (31) | 0.021 |
| set_name | `aecp_fanout.set_name.if0` | 550,334 | 11.007 | 10 | 24 | MISS T_svc | 663,954 | 1137 | 0.012 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 345,694 | 6.914 | 10 | 24 | fits | 417,272 | 589 | 0.015 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 371,021 | 7.420 | 10 | 24 | fits | 414,192 | 557 | 0.013 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 352,762 | 7.055 | 10 | 24 | fits | 433,168 | 563 | 0.015 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 364,436 | 7.289 | 10 | 24 | fits | 409,114 | 589 | 0.015 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 373,027 | 7.461 | 10 | 24 | fits | 453,418 | 662 | 0.014 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 352,522 | 7.050 | 10 | 24 | fits | 432,646 | 655 | 0.012 |
| set_name | `aecp_fanout.set_name.if1` | 575,163 | 11.503 | 10 | 24 | MISS T_svc | 634,647 | 1131 | 0.009 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 345,998 | 6.920 | 10 | 24 | fits | 418,616 | 590 | 0.014 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 354,357 | 7.087 | 10 | 24 | fits | 434,783 | 563 | 0.015 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 360,103 | 7.202 | 10 | 24 | fits | 414,196 | 556 | 0.013 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 371,839 | 7.437 | 10 | 24 | fits | 452,210 | 662 | 0.014 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 380,430 | 7.609 | 10 | 24 | fits | 434,201 | 655 | 0.012 |
| BIND_RX | `acmp.bind_rx.if0` | 48,650 | 0.973 | 10 | 20 | fits | 205,486 | 83 (77) | 0.028 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 155,022 | 3.100 | 10 | 20 | fits | 1,029,410 | 105 (32) | 0.012 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 867,935 | 17.359 | 10 | 20 | MISS T_svc | 1,021,118 | 120 (47) | 0.011 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 549,746 | 10.995 | 10 | 20 | MISS T_svc | 718,938 | 176 (50) | 0.018 |
| PROBE_TX | `acmp.probe_tx.if0` | 34,540 | 0.691 | 10 | 20 | fits | 1,019,171 | 122 (48) | 0.012 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 752,047 | 15.041 | 10 | 20 | MISS T_svc | 913,156 | 118 (48) | 0.012 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 750,541 | 15.011 | 10 | 20 | MISS T_svc | 912,112 | 118 (48) | 0.013 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 856,034 | 17.121 | 10 | 20 | MISS T_svc | 1,016,712 | 121 (48) | 0.011 |
| BIND_RX | `acmp.bind_rx.if1` | 771,444 | 15.429 | 10 | 20 | MISS T_svc | 940,027 | 148 (77) | 0.013 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 302,237 | 6.045 | 10 | 20 | fits | 1,379,293 | 103 (32) | 0.010 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 207,816 | 4.156 | 10 | 20 | fits | 1,202,818 | 115 (47) | 0.011 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 421,690 | 8.434 | 10 | 20 | fits | 1,830,021 | 337 (50) | 0.009 |
| PROBE_TX | `acmp.probe_tx.if1` | 432,073 | 8.641 | 10 | 20 | fits | 1,017,708 | 114 (48) | 0.013 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 385,971 | 7.719 | 10 | 20 | fits | 1,385,240 | 119 (48) | 0.009 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 199,519 | 3.990 | 10 | 20 | fits | 1,199,655 | 116 (48) | 0.011 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 383,764 | 7.675 | 10 | 20 | fits | 1,383,738 | 119 (48) | 0.009 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 82,771 | 1.655 | 10 | 24 | fits | 161,689 | 47 | 0.023 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 172,063 | 3.441 | 10 | 24 | fits | 251,751 | 132 | 0.021 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 129,081 | 2.582 | 10 | 24 | fits | 208,441 | 73 | 0.019 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 153,742 | 3.075 | 10 | 24 | fits | 233,345 | 91 | 0.022 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 154,213 | 3.084 | 10 | 24 | fits | 233,819 | 90 | 0.022 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 154,798 | 3.096 | 10 | 24 | fits | 234,404 | 90 | 0.022 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 129,863 | 2.597 | 10 | 24 | fits | 209,226 | 72 | 0.018 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 128,856 | 2.577 | 10 | 24 | fits | 208,219 | 68 | 0.018 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 127,397 | 2.548 | 10 | 24 | fits | 206,757 | 65 | 0.018 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 188,552 | 3.771 | 10 | 24 | fits | 268,155 | 167 | 0.019 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 142,515 | 2.850 | 10 | 24 | fits | 222,118 | 59 | 0.023 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 122,932 | 2.459 | 10 | 24 | fits | 202,292 | 52 | 0.019 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 155,371 | 3.107 | 10 | 24 | fits | 234,974 | 76 | 0.021 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 157,636 | 3.153 | 10 | 24 | fits | 237,239 | 82 | 0.022 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 155,948 | 3.119 | 10 | 24 | fits | 235,551 | 78 | 0.022 |
| get_configuration | `aecp.get_configuration.if0` | 116,978 | 2.340 | 10 | 24 | fits | 196,348 | 47 | 0.019 |
| entity_available | `aecp.entity_available.if0` | 138,717 | 2.774 | 10 | 24 | fits | 218,283 | 58 | 0.022 |
| get_name | `aecp.get_name.if0` | 144,962 | 2.899 | 10 | 24 | fits | 224,540 | 71 | 0.023 |
| get_counters | `aecp.get_counters.if0` | 151,318 | 3.026 | 10 | 24 | fits | 230,906 | 87 | 0.023 |
| get_avb_info | `aecp.get_avb_info.if0` | 145,179 | 2.904 | 10 | 24 | fits | 224,737 | 54 | 0.023 |
| unknown_command | `aecp.unknown_command.if0` | 116,722 | 2.334 | 10 | 24 | fits | 196,008 | 47 | 0.018 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 102,976 | 2.060 | 10 | 24 | fits | 182,435 | 58 | 0.025 |
| set_name | `aecp.set_name.if0` | 188,433 | 3.769 | 10 | 24 | fits | 315,698 | 114 | 0.018 |
| lock_entity | `aecp.lock_entity.if0` | 117,972 | 2.359 | 10 | 24 | fits | 208,068 | 66 | 0.018 |
| unlock_entity | `aecp.unlock_entity.if0` | 167,346 | 3.347 | 10 | 24 | fits | 656,539 | 289 | 0.010 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 105,576 | 2.112 | 10 | 24 | fits | 162,044 | 46 | 0.023 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 151,803 | 3.036 | 10 | 24 | fits | 231,280 | 123 | 0.018 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 148,778 | 2.976 | 10 | 24 | fits | 228,416 | 78 | 0.022 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 133,523 | 2.670 | 10 | 24 | fits | 212,918 | 82 | 0.018 |
| get_configuration | `aecp.get_configuration.if1` | 136,701 | 2.734 | 10 | 24 | fits | 216,255 | 52 | 0.022 |
| entity_available | `aecp.entity_available.if1` | 138,569 | 2.771 | 10 | 24 | fits | 218,131 | 56 | 0.022 |
| get_name | `aecp.get_name.if1` | 144,547 | 2.891 | 10 | 24 | fits | 224,121 | 69 | 0.022 |
| get_counters | `aecp.get_counters.if1` | 151,145 | 3.023 | 10 | 24 | fits | 230,729 | 85 | 0.022 |
| get_avb_info | `aecp.get_avb_info.if1` | 124,936 | 2.499 | 10 | 24 | fits | 204,218 | 45 | 0.018 |
| unknown_command | `aecp.unknown_command.if1` | 136,627 | 2.733 | 10 | 24 | fits | 216,181 | 52 | 0.022 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 102,789 | 2.056 | 10 | 24 | fits | 182,308 | 56 | 0.025 |
| set_name | `aecp.set_name.if1` | 169,253 | 3.385 | 10 | 24 | fits | 300,211 | 140 | 0.013 |
| lock_entity | `aecp.lock_entity.if1` | 117,987 | 2.360 | 10 | 24 | fits | 215,368 | 85 | 0.017 |
| unlock_entity | `aecp.unlock_entity.if1` | 138,568 | 2.771 | 10 | 24 | fits | 236,027 | 92 | 0.021 |

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
