### 8x8

29 of 129 paths and 61 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.976 (4.145) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 15.615 (35.769) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 15.203 (35.201) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 4.094 (24.092) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 17.317 (28.807) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 18.564 (28.807) | MISS T_svc | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 19.238 (28.753) | MISS T_svc | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 20.462 (28.753) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 17.545 (37.427) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 4.251 (24.144) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 17.303 (37.304) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 7.748 (27.750) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 15.226 (35.221) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 7.803 (27.799) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.792 (20.480) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 8.820 (20.440) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 3.230 (20.687) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 6.138 (27.676) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.752 (23.645) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 1.698 (23.657) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 7.874 (44.710) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 4.890 (46.333) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 7.773 (47.213) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 7.571 (47.213) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 3.760 (20.407) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 2.884 (20.407) | fits | 1 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 3.716 (23.667) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 6.048 (46.301) | fits | 1 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 3.712 (20.303) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 4.183 (20.303) | fits | 1 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 11.169 (31.367) | MISS T_svc | 0 acmp | 1 | 1 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 8.536 (36.788) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.596 (2.699) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.765 (2.699) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.465 (2.484) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.528 (2.484) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.450 (12.128) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.087 (12.128) | fits | 1 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.068 (11.415) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.783 (11.415) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.881 (3.827) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 1.808 (3.827) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 2.581 (6.481) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 2.218 (6.481) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.826 (4.423) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.823 (4.421) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.546 (4.143) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.946 (4.545) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.382 (3.978) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.784 (4.383) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 3.081 (4.681) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 2.666 (4.265) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.949 (4.546) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 2.944 (4.542) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.397 (4.209) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.398 (4.356) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.107 (3.702) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 2.100 (3.696) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.490 (5.088) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.078 (4.676) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 3.033 (4.628) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 3.020 (4.618) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 3.023 (4.618) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.998 (4.593) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.820 (5.414) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 2.489 (4.083) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 2.906 (4.502) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.714 (4.309) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 2.710 (4.307) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 3.161 (4.757) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.791 (4.387) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 3.163 (4.760) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 3.127 (4.723) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 3.143 (4.738) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.638 (4.233) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.692 (3.281) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 2.371 (5.908) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 3.826 (6.385) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.441 (6.074) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.781 (4.377) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.781 (4.378) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 3.395 (13.258) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.817 (4.771) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 9.196 (12.768) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 7.783 (11.351) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 7.335 (8.780) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 6.955 (8.401) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 7.241 (10.812) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 7.661 (11.230) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.024 (13.311) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 10.993 (13.121) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 7.499 (10.884) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.193 (11.763) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 8.234 (11.805) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 56.532 (63.567) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 41.875 (64.264) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 48.294 (63.776) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 14.022 (27.265) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 117.042 (122.626) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 370.618 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 2.336 (6.221) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 2.206 (6.563) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.612 (2.505) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.612 (2.533) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.704 (6.692) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.706 (6.723) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 2.190 (6.221) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 2.060 (6.563) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.083 (4.934) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 2.014 (5.922) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 13.588 | MISS T_svc | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 98.524 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 13.630 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 58.567 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 46.086 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 13.624 | MISS T_svc | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 302.254 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 13.613 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 52.763 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 588.279 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 588.259 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 7.590 (9.243) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 8.287 (9.866) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.202 (3.202) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.255 (3.256) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 2.465 (2.466) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.103 (3.104) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.251 (6.692) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.326 (6.719) | fits | 0 events | 1 | 0 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 150.877 | 23 | 681,617 (13.632) | yes | - |
| backlog-adp | 541.928 | 29 | 1,417,430 (28.349) | no | {'srp': 32} |
| backlog-adp-refill | 588.296 | 32 | 1,417,585 (28.352) | no | {'srp': 32} |
| backlog-owed | 370.669 | 42 | 606,489 (12.130) | yes | - |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 185,779 | 3.716 | 10 | 20 | fits | 1,183,346 | 96 (14) | 0.012 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 302,397 | 6.048 | 10 | 20 | fits | 998,057 | 71 (14) | 0.015 |
| LINK_UP | `adp.link_up.if0` | 3,419 | 0.068 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| LINK_UP | `adp.link_up.if1` | 39,157 | 0.783 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 129,071 | 2.581 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 110,916 | 2.218 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 94,057 | 1.881 | 10 | 200 | fits | 7,198 | 18 (11) | 0.087 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 90,388 | 1.808 | 10 | 200 | fits | 7,198 | 18 (11) | 0.087 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 35,204 | 0.704 | 10 | 50 | fits | 334,586 | 154 | 0.022 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 54,164 | 1.083 | 10 | 50 | fits | 126,636 | 38 | 0.037 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 38,942 | 0.779 | 10 | 50 | fits | 126,604 | 38 | 0.037 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 109,503 | 2.190 | 10 | 50 | fits | 143,845 | 65 | 0.035 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 116,820 | 2.336 | 10 | 50 | fits | 143,845 | 65 | 0.035 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 30,598 | 0.612 | 10 | 50 | fits | 125,235 | 48 | 0.032 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 35,304 | 0.706 | 10 | 50 | fits | 336,132 | 154 | 0.022 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 42,258 | 0.845 | 10 | 50 | fits | 128,060 | 38 | 0.036 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 100,701 | 2.014 | 10 | 50 | fits | 128,074 | 38 | 0.036 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 102,993 | 2.060 | 10 | 50 | fits | 166,116 | 71 | 0.040 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 110,310 | 2.206 | 10 | 50 | fits | 166,116 | 71 | 0.040 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 30,598 | 0.612 | 10 | 50 | fits | 126,654 | 48 | 0.032 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 388,668 | 7.773 | 10 | 20 | fits | 1,046,692 | 119 (35) | 0.014 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 378,556 | 7.571 | 10 | 20 | fits | 1,046,692 | 119 (35) | 0.014 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 187,997 | 3.760 | 10 | 20 | fits | 1,020,331 | 73 (14) | 0.013 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 144,214 | 2.884 | 10 | 20 | fits | 1,020,331 | 73 (14) | 0.013 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 185,614 | 3.712 | 10 | 20 | fits | 1,015,171 | 74 (14) | 0.014 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 209,153 | 4.183 | 10 | 20 | fits | 1,015,171 | 74 (14) | 0.014 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 87,609 | 1.752 | 10 | 20 | fits | 1,182,232 | 96 (35) | 0.013 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 84,904 | 1.698 | 10 | 20 | fits | 1,182,832 | 96 (35) | 0.013 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 312,538 | 6.251 | 10 | 18 | fits | 334,586 | 154 | 0.022 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 316,310 | 6.326 | 10 | 18 | fits | 335,972 | 154 | 0.022 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 160,091 | 3.202 | 10 | 18 | fits | 160,123 | 30 | 0.045 |
| malformed MRPDU discard | `srp.malformed.if0` | 123,246 | 2.465 | 10 | 18 | fits | 123,278 | 29 | 0.034 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 379,491 | 7.590 | 210 | 218 | fits | 462,142 | 143 | 0.025 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 162,768 | 3.255 | 10 | 18 | fits | 162,800 | 29 | 0.043 |
| malformed MRPDU discard | `srp.malformed.if1` | 155,175 | 3.103 | 10 | 18 | fits | 155,207 | 36 | 0.037 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 414,375 | 8.287 | 210 | 218 | fits | 493,317 | 149 | 0.026 |
| an event behind 15 others | `backlog.event.if0` | 701,107 | 14.022 | 10 | 200 | MISS T_svc | 681,610 | 375 | 0.024 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 2,826,615 | 56.532 | 10 | 20 | MISS ceiling | 469,950 | 256 | 0.028 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 681,513 | 13.630 | 10 | 200 | MISS T_svc | 681,617 | 392 | 0.023 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,304,300 | 46.086 | 10 | 200 | MISS T_svc | 437,179 | 285 | 0.024 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 679,384 | 13.588 | 10 | 20 | MISS T_svc | 681,617 | 392 | 0.023 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,175,701 | 63.514 | 10 | 20 | MISS ceiling | 469,950 | 256 | 0.028 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 681,176 | 13.624 | 10 | 24 | MISS T_svc | 681,617 | 392 | 0.023 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,131,155 | 122.623 | 10 | 24 | MISS ceiling | 290,322 | 163 | 0.031 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 680,656 | 13.613 | 10 | 50 | MISS T_svc | 681,617 | 392 | 0.023 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,303,552 | 46.071 | 10 | 50 | MISS T_svc | 437,179 | 285 | 0.024 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 3,177,159 | 63.543 | 10 | 18 | MISS ceiling | 469,950 | 256 | 0.028 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,242,478 | 144.850 | 10 | 18 | MISS ceiling | 171,802 | 54 | 0.043 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,093,742 | 41.875 | 10 | 20 | MISS ceiling | 899,285 | 360 | 0.020 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 623,386 | 12.468 | 10 | 200 | MISS T_svc | 1,199,994 | 405 | 0.016 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,636,297 | 52.726 | 10 | 200 | MISS T_svc | 899,285 | 360 | 0.020 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 623,842 | 12.477 | 10 | 20 | MISS T_svc | 1,199,994 | 405 | 0.016 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 4,903,866 | 98.077 | 10 | 20 | MISS ceiling | 1,133,432 | 275 | 0.015 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 625,634 | 12.513 | 10 | 24 | MISS T_svc | 1,199,994 | 405 | 0.016 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 15,090,881 | 301.818 | 10 | 24 | MISS ceiling | 985,915 | 188 | 0.015 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 625,114 | 12.502 | 10 | 50 | MISS T_svc | 1,199,994 | 405 | 0.016 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,638,135 | 52.763 | 10 | 50 | MISS ceiling | 899,285 | 360 | 0.020 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,095,547 | 541.911 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,094,540 | 541.891 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,414,681 | 48.294 | 10 | 20 | MISS ceiling | 1,195,323 | 307 | 0.015 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 623,386 | 12.468 | 10 | 200 | MISS T_svc | 1,199,994 | 405 | 0.016 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 2,928,374 | 58.567 | 10 | 200 | MISS T_svc | 1,195,323 | 307 | 0.015 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 623,842 | 12.477 | 10 | 20 | MISS T_svc | 1,199,994 | 405 | 0.016 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 4,926,180 | 98.524 | 10 | 20 | MISS ceiling | 1,195,323 | 307 | 0.015 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 625,634 | 12.513 | 10 | 24 | MISS T_svc | 1,199,994 | 405 | 0.016 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,112,710 | 302.254 | 10 | 24 | MISS ceiling | 985,783 | 188 | 0.015 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 625,114 | 12.502 | 10 | 50 | MISS T_svc | 1,199,994 | 405 | 0.016 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,583,692 | 51.674 | 10 | 50 | MISS ceiling | 844,842 | 353 | 0.021 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,413,944 | 588.279 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,412,937 | 588.259 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,852,102 | 117.042 | 10 | 20 | MISS ceiling | 410,199 | 191 | 0.031 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,530,920 | 370.618 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,530,882 | 370.618 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,530,845 | 370.617 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,530,807 | 370.616 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 546,138 | 10.923 | 10 | 200 | MISS T_svc | 465,045 | 344 | 0.021 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 2,168,781 | 43.376 | 10 | 200 | MISS T_svc | 534,896 | 300 | 0.029 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 544,009 | 10.880 | 10 | 20 | MISS T_svc | 465,045 | 344 | 0.021 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,011,886 | 60.238 | 10 | 20 | MISS ceiling | 388,200 | 120 | 0.030 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 545,801 | 10.916 | 10 | 24 | MISS T_svc | 465,045 | 344 | 0.021 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,999,689 | 139.994 | 10 | 24 | MISS ceiling | 358,253 | 169 | 0.034 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 545,281 | 10.906 | 10 | 50 | MISS T_svc | 465,045 | 344 | 0.021 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,168,033 | 43.361 | 10 | 50 | MISS T_svc | 534,896 | 300 | 0.029 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,633,105 | 32.662 | 10 | 18 | MISS ceiling | 606,489 | 343 | 0.031 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 7,771,112 | 155.422 | 10 | 18 | MISS ceiling | 175,408 | 36 | 0.041 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 961,901 | 19.238 | 10 | 20 | MISS T_svc | 1,437,630 | 124 (29) | 0.011 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 1,023,096 | 20.462 | 10 | 20 | MISS ceiling | 1,437,630 | 124 (29) | 0.011 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 865,827 | 17.317 | 10 | 20 | MISS T_svc | 1,440,337 | 135 (35) | 0.011 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 928,176 | 18.564 | 10 | 20 | MISS T_svc | 1,440,337 | 135 (35) | 0.011 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 393,705 | 7.874 | 10 | 20 | fits | 1,006,340 | 67 (12) | 0.011 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 244,509 | 4.890 | 10 | 20 | fits | 1,001,043 | 93 (12) | 0.015 |
| LINK_UP | `adp.link_up.if0` | 3,419 | 0.068 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| LINK_UP | `adp.link_up.if1` | 39,157 | 0.783 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 129,071 | 2.581 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 110,916 | 2.218 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| LINK_DOWN | `adp.link_down.if0` | 22,521 | 0.450 | 10 | 200 | fits | 606,394 | 58 (9) | 0.031 |
| LINK_DOWN | `adp.link_down.if1` | 254,351 | 5.087 | 10 | 200 | fits | 606,394 | 58 (9) | 0.031 |
| LINK_UP | `adp.link_up.if0` | 3,419 | 0.068 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| LINK_UP | `adp.link_up.if1` | 39,157 | 0.783 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 129,071 | 2.581 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 110,916 | 2.218 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| GM_CHANGE | `adp.gm_change.if0` | 23,230 | 0.465 | 10 | 200 | fits | 124,212 | 34 (11) | 0.036 |
| GM_CHANGE | `adp.gm_change.if1` | 26,406 | 0.528 | 10 | 200 | fits | 124,212 | 34 (11) | 0.036 |
| LINK_UP | `adp.link_up.if0` | 3,419 | 0.068 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| LINK_UP | `adp.link_up.if1` | 39,157 | 0.783 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 129,071 | 2.581 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 110,916 | 2.218 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 29,799 | 0.596 | 10 | 200 | fits | 134,950 | 73 (31) | 0.036 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 38,257 | 0.765 | 10 | 200 | fits | 134,950 | 73 (31) | 0.036 |
| LINK_UP | `adp.link_up.if0` | 3,419 | 0.068 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| LINK_UP | `adp.link_up.if1` | 39,157 | 0.783 | 10 | 200 | fits | 570,743 | 298 (11) | 0.017 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 129,071 | 2.581 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 110,916 | 2.218 | 10 | 200 | fits | 134,595 | 84 (39) | 0.033 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 29,799 | 0.596 | 10 | 200 | fits | 126,716 | 45 (31) | 0.038 |
| set_name | `aecp_fanout.set_name.if0` | 551,178 | 11.024 | 10 | 24 | MISS T_svc | 665,567 | 1137 | 0.014 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 366,759 | 7.335 | 10 | 24 | fits | 439,014 | 596 | 0.019 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 362,066 | 7.241 | 10 | 24 | fits | 414,752 | 556 | 0.014 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 353,708 | 7.074 | 10 | 24 | fits | 434,327 | 563 | 0.017 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 374,946 | 7.499 | 10 | 24 | fits | 410,846 | 589 | 0.017 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 459,805 | 9.196 | 10 | 24 | fits | 493,412 | 711 | 0.015 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 409,654 | 8.193 | 10 | 24 | fits | 433,594 | 656 | 0.013 |
| set_name | `aecp_fanout.set_name.if1` | 549,655 | 10.993 | 10 | 24 | MISS T_svc | 656,073 | 1137 | 0.013 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 347,761 | 6.955 | 10 | 24 | fits | 420,057 | 589 | 0.017 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 383,052 | 7.661 | 10 | 24 | fits | 416,011 | 557 | 0.014 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 354,741 | 7.095 | 10 | 24 | fits | 435,380 | 563 | 0.017 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 389,131 | 7.783 | 10 | 24 | fits | 432,936 | 655 | 0.013 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 411,722 | 8.234 | 10 | 24 | fits | 435,183 | 656 | 0.013 |
| BIND_RX | `acmp.bind_rx.if0` | 48,815 | 0.976 | 10 | 20 | fits | 207,255 | 83 (77) | 0.034 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 161,486 | 3.230 | 10 | 20 | fits | 1,034,373 | 105 (32) | 0.016 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 877,250 | 17.545 | 10 | 20 | MISS T_svc | 1,025,672 | 120 (47) | 0.015 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 558,459 | 11.169 | 10 | 20 | MISS T_svc | 723,625 | 176 (50) | 0.022 |
| PROBE_TX | `acmp.probe_tx.if0` | 39,614 | 0.792 | 10 | 20 | fits | 1,024,025 | 122 (48) | 0.015 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 761,315 | 15.226 | 10 | 20 | MISS T_svc | 918,203 | 118 (48) | 0.016 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 760,162 | 15.203 | 10 | 20 | MISS T_svc | 916,774 | 118 (48) | 0.016 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 865,170 | 17.303 | 10 | 20 | MISS T_svc | 1,021,419 | 121 (48) | 0.014 |
| BIND_RX | `acmp.bind_rx.if1` | 780,774 | 15.615 | 10 | 20 | MISS T_svc | 945,062 | 148 (77) | 0.017 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 306,903 | 6.138 | 10 | 20 | fits | 1,383,780 | 103 (32) | 0.012 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 212,529 | 4.251 | 10 | 20 | fits | 1,207,180 | 115 (47) | 0.014 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 426,821 | 8.536 | 10 | 20 | fits | 1,839,425 | 337 (50) | 0.012 |
| PROBE_TX | `acmp.probe_tx.if1` | 441,018 | 8.820 | 10 | 20 | fits | 1,022,021 | 114 (48) | 0.016 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 390,146 | 7.803 | 10 | 20 | fits | 1,389,972 | 119 (48) | 0.012 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 204,703 | 4.094 | 10 | 20 | fits | 1,204,602 | 116 (48) | 0.013 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 387,420 | 7.748 | 10 | 20 | fits | 1,387,485 | 119 (48) | 0.011 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 84,591 | 1.692 | 10 | 24 | fits | 164,068 | 47 | 0.033 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 174,491 | 3.490 | 10 | 24 | fits | 254,392 | 132 | 0.029 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 151,663 | 3.033 | 10 | 24 | fits | 231,409 | 80 | 0.031 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 135,704 | 2.714 | 10 | 24 | fits | 215,434 | 84 | 0.026 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 156,353 | 3.127 | 10 | 24 | fits | 236,164 | 90 | 0.030 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 157,135 | 3.143 | 10 | 24 | fits | 236,919 | 90 | 0.030 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 131,882 | 2.638 | 10 | 24 | fits | 211,646 | 72 | 0.027 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 151,134 | 3.023 | 10 | 24 | fits | 230,903 | 75 | 0.030 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 149,915 | 2.998 | 10 | 24 | fits | 229,654 | 72 | 0.031 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 190,977 | 3.820 | 10 | 24 | fits | 270,716 | 167 | 0.027 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 124,439 | 2.489 | 10 | 24 | fits | 204,169 | 52 | 0.028 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 145,305 | 2.906 | 10 | 24 | fits | 225,113 | 59 | 0.031 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 158,069 | 3.161 | 10 | 24 | fits | 237,850 | 76 | 0.030 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 139,569 | 2.791 | 10 | 24 | fits | 219,330 | 75 | 0.026 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 158,168 | 3.163 | 10 | 24 | fits | 237,976 | 78 | 0.029 |
| get_configuration | `aecp.get_configuration.if0` | 119,096 | 2.382 | 10 | 24 | fits | 198,880 | 47 | 0.028 |
| entity_available | `aecp.entity_available.if0` | 141,308 | 2.826 | 10 | 24 | fits | 221,169 | 58 | 0.032 |
| get_name | `aecp.get_name.if0` | 147,470 | 2.949 | 10 | 24 | fits | 227,324 | 71 | 0.032 |
| get_counters | `aecp.get_counters.if0` | 154,036 | 3.081 | 10 | 24 | fits | 234,025 | 87 | 0.032 |
| get_avb_info | `aecp.get_avb_info.if0` | 127,289 | 2.546 | 10 | 24 | fits | 207,147 | 47 | 0.028 |
| unknown_command | `aecp.unknown_command.if0` | 139,035 | 2.781 | 10 | 24 | fits | 218,854 | 54 | 0.031 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 105,334 | 2.107 | 10 | 24 | fits | 185,095 | 58 | 0.035 |
| set_name | `aecp.set_name.if0` | 191,306 | 3.826 | 10 | 24 | fits | 319,273 | 114 | 0.025 |
| lock_entity | `aecp.lock_entity.if0` | 119,875 | 2.397 | 10 | 24 | fits | 210,460 | 66 | 0.026 |
| unlock_entity | `aecp.unlock_entity.if0` | 169,761 | 3.395 | 10 | 24 | fits | 662,909 | 289 | 0.016 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 118,559 | 2.371 | 10 | 24 | fits | 164,522 | 46 | 0.033 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 153,890 | 3.078 | 10 | 24 | fits | 233,817 | 123 | 0.025 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 151,005 | 3.020 | 10 | 24 | fits | 230,898 | 78 | 0.030 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 135,500 | 2.710 | 10 | 24 | fits | 215,369 | 82 | 0.026 |
| get_configuration | `aecp.get_configuration.if1` | 139,209 | 2.784 | 10 | 24 | fits | 219,130 | 52 | 0.032 |
| entity_available | `aecp.entity_available.if1` | 141,140 | 2.823 | 10 | 24 | fits | 221,061 | 56 | 0.032 |
| get_name | `aecp.get_name.if1` | 147,204 | 2.944 | 10 | 24 | fits | 227,099 | 69 | 0.032 |
| get_counters | `aecp.get_counters.if1` | 133,277 | 2.666 | 10 | 24 | fits | 213,256 | 78 | 0.028 |
| get_avb_info | `aecp.get_avb_info.if1` | 147,277 | 2.946 | 10 | 24 | fits | 227,235 | 52 | 0.031 |
| unknown_command | `aecp.unknown_command.if1` | 139,057 | 2.781 | 10 | 24 | fits | 218,890 | 52 | 0.031 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 104,993 | 2.100 | 10 | 24 | fits | 184,797 | 56 | 0.035 |
| set_name | `aecp.set_name.if1` | 172,057 | 3.441 | 10 | 24 | fits | 303,685 | 140 | 0.021 |
| lock_entity | `aecp.lock_entity.if1` | 119,917 | 2.398 | 10 | 24 | fits | 217,785 | 85 | 0.025 |
| unlock_entity | `aecp.unlock_entity.if1` | 140,838 | 2.817 | 10 | 24 | fits | 238,526 | 92 | 0.029 |

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
