### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 129 paths and 6 of 446 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.258 (0.674) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.216 (0.625) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.119 (0.464) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.111 (0.459) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.075 (0.632) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.270 (0.632) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.185 (0.745) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.373 (0.745) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.122 (0.550) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.129 (0.510) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.110 (0.450) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.110 (0.457) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.124 (0.533) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.232 (0.589) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.126 (0.474) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.135 (0.495) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.089 (0.483) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.085 (0.533) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.482 (1.808) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.417 (1.870) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.080 (0.670) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.243 (0.844) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.378 (0.801) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.274 (0.837) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.341 (0.754) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.193 (0.766) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.204 (0.932) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.144 (0.810) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.185 (1.636) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.138 (0.701) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.166 (0.626) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.255 (0.734) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.031 (0.219) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.045 (0.219) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.018 (0.208) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.033 (0.208) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.018 (0.607) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.297 (0.607) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.021 (1.321) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.156 (1.321) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.192 (0.393) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.172 (0.393) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.263 (0.648) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.174 (0.648) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.287 (0.605) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.214 (0.522) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.299 (0.621) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 0.225 (0.540) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.195 (0.503) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.296 (0.616) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.239 (0.563) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 0.332 (0.659) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.222 (0.536) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.323 (0.648) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.270 (0.651) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.379 (0.772) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.290 (0.612) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.216 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.355 (0.676) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.359 (0.680) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.313 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.328 (0.649) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.284 (0.539) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.221 (0.546) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.358 (0.679) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.216 (0.524) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.303 (0.623) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.222 (0.531) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.236 (0.547) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.281 (0.593) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.230 (0.557) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.312 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.306 (0.626) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.231 (0.539) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.301 (0.621) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.206 (0.531) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.202 (0.524) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.568 (1.189) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.629 (1.248) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.231 (0.535) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 0.298 (0.619) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.362 (0.742) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.285 (0.679) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.882 (1.274) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.875 (1.364) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.906 (1.653) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.910 (1.672) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.879 (1.271) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 0.747 (1.141) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 1.101 (1.745) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 1.029 (1.430) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.876 (1.391) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.755 (1.146) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.754 (1.146) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.593 (7.302) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 5.292 (7.379) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.118 (0.675) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.473 (2.523) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.746 (64.305) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 361.051 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.151 (0.539) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.263 (0.673) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.110 (0.272) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.112 (0.287) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.134 (1.207) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.122 (1.134) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.132 (0.539) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.241 (0.673) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.215 (0.583) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 0.202 (0.596) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.854 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 8.886 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.845 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.442 | fits | 7 adp | 26 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.850 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.890 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.098 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.879 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.478 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 5.425 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-2.service.srp.last.if1` (backlog-adp@verify-2) | 16.985 | fits | 31 srp | 28 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.730 (1.890) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.512 (1.642) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.594 (0.595) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.522 (0.522) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.248 (0.248) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.244 (0.245) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.563 (1.668) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.484 (1.581) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.234 | 18 | 187,825 (1.878) | yes | - |
| backlog-adp@blank-1 | 0 | 17.640 | 18 | 187,796 (1.878) | yes | - |
| backlog-adp@blank-2 | 0 | 18.837 | 19 | 194,879 (1.949) | yes | - |
| backlog-adp@blank-3 | 0 | 18.613 | 20 | 183,130 (1.831) | yes | - |
| backlog-adp@blank-4 | 0 | 18.019 | 19 | 190,467 (1.905) | yes | - |
| backlog-adp@blank-5 | 0 | 17.805 | 19 | 187,848 (1.878) | yes | - |
| backlog-adp@blank-6 | 0 | 17.864 | 19 | 186,612 (1.866) | yes | - |
| backlog-adp@blank-7 | 0 | 17.611 | 17 | 194,404 (1.944) | yes | - |
| backlog-adp@program-0 | 0 | 18.081 | 18 | 189,881 (1.899) | yes | - |
| backlog-adp@program-1 | 0 | 17.741 | 18 | 187,164 (1.872) | yes | - |
| backlog-adp@program-2 | 0 | 18.049 | 19 | 187,164 (1.872) | yes | - |
| backlog-adp@program-3 | 0 | 18.265 | 19 | 181,494 (1.815) | yes | - |
| backlog-adp@program-4 | 0 | 17.174 | 19 | 186,918 (1.869) | yes | - |
| backlog-adp@program-5 | 0 | 17.170 | 19 | 186,918 (1.869) | yes | - |
| backlog-adp@program-6 | 0 | 17.318 | 19 | 181,327 (1.813) | yes | - |
| backlog-adp@program-7 | 0 | 17.079 | 18 | 193,751 (1.938) | yes | - |
| backlog-adp@verify-0 | 0 | 18.257 | 19 | 194,663 (1.947) | yes | - |
| backlog-adp@verify-1 | 0 | 19.553 | 20 | 182,735 (1.827) | yes | - |
| backlog-adp@verify-2 | 0 | 18.365 | 19 | 190,406 (1.904) | yes | - |
| backlog-adp@verify-3 | 0 | 18.222 | 19 | 187,709 (1.877) | yes | - |
| backlog-adp@verify-4 | 0 | 18.047 | 18 | 187,709 (1.877) | yes | - |
| backlog-adp@verify-5 | 0 | 18.230 | 18 | 170,885 (1.709) | yes | - |
| backlog-adp@verify-6 | 0 | 18.214 | 19 | 194,376 (1.944) | yes | - |
| backlog-adp@verify-7 | 1 | 18.841 | 19 | 183,083 (1.831) | yes | - |
| backlog | 0 | 14.373 | 20 | 155,796 (1.558) | yes | - |
| backlog-adp | 0 | 17.190 | 20 | 196,295 (1.963) | yes | - |
| backlog-adp-refill | 0 | 41.058 | 28 | 175,986 (1.760) | yes | - |
| backlog-owed | 0 | 361.102 | 65 | 190,353 (1.904) | yes | - |

Composed maximum over the 4 backlog windows: 196,295 CPU cycles (1.963 ms), backlog-adp.
Over the windows that released their whole load only: 196,295 (1.963 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 2813 | 0 | 132,078 (1.321) | fits |
| backlog-adp@blank-0 | 484 | 0 | 187,825 (1.878) | fits |
| backlog-adp@blank-1 | 484 | 0 | 187,796 (1.878) | fits |
| backlog-adp@blank-2 | 485 | 0 | 194,879 (1.949) | fits |
| backlog-adp@blank-3 | 486 | 0 | 183,130 (1.831) | fits |
| backlog-adp@blank-4 | 485 | 0 | 190,467 (1.905) | fits |
| backlog-adp@blank-5 | 486 | 0 | 187,848 (1.878) | fits |
| backlog-adp@blank-6 | 486 | 0 | 186,612 (1.866) | fits |
| backlog-adp@blank-7 | 484 | 0 | 194,404 (1.944) | fits |
| backlog-adp@program-0 | 758 | 0 | 189,881 (1.899) | fits |
| backlog-adp@program-1 | 759 | 0 | 187,164 (1.872) | fits |
| backlog-adp@program-2 | 760 | 0 | 187,164 (1.872) | fits |
| backlog-adp@program-3 | 760 | 0 | 181,494 (1.815) | fits |
| backlog-adp@program-4 | 761 | 0 | 186,918 (1.869) | fits |
| backlog-adp@program-5 | 761 | 0 | 186,918 (1.869) | fits |
| backlog-adp@program-6 | 761 | 0 | 181,327 (1.813) | fits |
| backlog-adp@program-7 | 763 | 0 | 193,751 (1.938) | fits |
| backlog-adp@verify-0 | 1015 | 0 | 194,663 (1.947) | fits |
| backlog-adp@verify-1 | 1016 | 0 | 182,735 (1.827) | fits |
| backlog-adp@verify-2 | 1015 | 0 | 190,406 (1.904) | fits |
| backlog-adp@verify-3 | 1016 | 0 | 187,709 (1.877) | fits |
| backlog-adp@verify-4 | 1015 | 0 | 187,709 (1.877) | fits |
| backlog-adp@verify-5 | 1015 | 0 | 170,885 (1.709) | fits |
| backlog-adp@verify-6 | 1016 | 0 | 194,376 (1.944) | fits |
| backlog-adp@verify-7 | 1017 | 0 | 183,083 (1.831) | fits |
| adp-advertise | 605 | 0 | 132,078 (1.321) | fits |
| maap | 349 | 0 | 133,316 (1.333) | fits |
| acmp-noresp | 1545 | 0 | 132,078 (1.321) | fits |
| save | 617 | 0 | 132,078 (1.321) | fits |
| srp | 307 | 0 | 188,971 (1.890) | fits |
| backlog | 303 | 0 | 155,796 (1.558) | fits |
| backlog-adp | 322 | 0 | 196,295 (1.963) | fits |
| backlog-adp-refill | 330 | 0 | 175,986 (1.760) | fits |
| backlog-owed | 359 | 0 | 190,353 (1.904) | fits |
| acmp-disc | 832 | 0 | 132,078 (1.321) | fits |
| adp-link | 92 | 0 | 132,078 (1.321) | fits |
| adp-gm | 90 | 0 | 132,078 (1.321) | fits |
| adp-discover | 90 | 0 | 132,078 (1.321) | fits |
| control | 90 | 0 | 132,078 (1.321) | fits |
| aecp-fanout | 146 | 0 | 144,890 (1.449) | fits |
| acmp-cmd | 100 | 0 | 132,078 (1.321) | fits |
| aecp | 136 | 0 | 132,078 (1.321) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 20,374 | 0.204 | 20 | 20 | fits | 64,434 | 51 (14) | 0.709 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 14,400 | 0.144 | 20 | 20 | fits | 54,971 | 20 (14) | 0.876 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 529,195 | 5.292 | 20 | 20 | fits | 126,383 | 85 | 0.630 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 184,488 | 1.845 | 20 | 200 | fits | 119,368 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 644,153 | 6.442 | 20 | 200 | fits | 126,383 | 85 | 0.630 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 185,400 | 1.854 | 20 | 20 | fits | 119,368 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 888,560 | 8.886 | 20 | 20 | fits | 121,026 | 46 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 188,985 | 1.890 | 20 | 24 | fits | 119,368 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,586,147 | 15.861 | 20 | 24 | fits | 67,554 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 187,945 | 1.879 | 20 | 50 | fits | 119,368 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 647,829 | 6.478 | 20 | 50 | fits | 126,383 | 85 | 0.630 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 375,315 | 3.753 | 18 | 18 | fits | 187,825 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,685,509 | 16.855 | 18 | 18 | fits | 50,289 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 456,465 | 4.565 | 20 | 20 | fits | 156,675 | 89 | 0.665 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 115,875 | 1.159 | 20 | 200 | fits | 119,024 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 599,259 | 5.993 | 20 | 200 | fits | 156,675 | 89 | 0.665 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 116,787 | 1.168 | 20 | 20 | fits | 119,024 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 842,533 | 8.425 | 20 | 20 | fits | 120,730 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 120,372 | 1.204 | 20 | 24 | fits | 119,024 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,526,656 | 15.267 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 119,332 | 1.193 | 20 | 50 | fits | 119,024 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 602,935 | 6.029 | 20 | 50 | fits | 156,675 | 89 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 306,673 | 3.067 | 18 | 18 | fits | 187,796 | 140 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,626,092 | 16.261 | 18 | 18 | fits | 50,355 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 477,012 | 4.770 | 20 | 20 | fits | 154,496 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 122,594 | 1.226 | 20 | 200 | fits | 119,024 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 620,083 | 6.201 | 20 | 200 | fits | 154,496 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 123,506 | 1.235 | 20 | 20 | fits | 119,024 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 835,741 | 8.357 | 20 | 20 | fits | 126,410 | 52 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 127,091 | 1.271 | 20 | 24 | fits | 119,024 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,527,700 | 15.277 | 20 | 24 | fits | 67,565 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 126,051 | 1.261 | 20 | 50 | fits | 119,024 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 623,759 | 6.238 | 20 | 50 | fits | 154,496 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 320,475 | 3.205 | 18 | 18 | fits | 194,879 | 151 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,627,028 | 16.270 | 18 | 18 | fits | 50,340 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 445,031 | 4.450 | 20 | 20 | fits | 156,174 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 129,313 | 1.293 | 20 | 200 | fits | 119,024 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 589,184 | 5.892 | 20 | 200 | fits | 156,174 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 130,225 | 1.302 | 20 | 20 | fits | 119,024 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 838,746 | 8.387 | 20 | 20 | fits | 120,821 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 133,810 | 1.338 | 20 | 24 | fits | 119,024 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,531,569 | 15.316 | 20 | 24 | fits | 67,508 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 132,770 | 1.328 | 20 | 50 | fits | 119,024 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 592,860 | 5.929 | 20 | 50 | fits | 156,174 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 436,621 | 4.366 | 18 | 18 | fits | 183,130 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,637,175 | 16.372 | 18 | 18 | fits | 56,525 | 24 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 477,347 | 4.773 | 20 | 20 | fits | 161,253 | 89 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 123,064 | 1.231 | 20 | 200 | fits | 124,873 | 151 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 620,449 | 6.204 | 20 | 200 | fits | 161,253 | 89 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 123,976 | 1.240 | 20 | 20 | fits | 124,873 | 151 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 870,296 | 8.703 | 20 | 20 | fits | 127,692 | 57 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 127,561 | 1.276 | 20 | 24 | fits | 124,873 | 151 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,548,115 | 15.481 | 20 | 24 | fits | 74,295 | 37 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 126,521 | 1.265 | 20 | 50 | fits | 124,873 | 151 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 624,125 | 6.241 | 20 | 50 | fits | 161,253 | 89 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 316,533 | 3.165 | 18 | 18 | fits | 190,467 | 145 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,633,955 | 16.340 | 18 | 18 | fits | 36,794 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 431,923 | 4.319 | 20 | 20 | fits | 160,006 | 89 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 114,381 | 1.144 | 20 | 200 | fits | 118,805 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 573,352 | 5.734 | 20 | 200 | fits | 160,006 | 89 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 115,293 | 1.153 | 20 | 20 | fits | 118,805 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 789,602 | 7.896 | 20 | 20 | fits | 93,952 | 48 | 0.658 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 118,878 | 1.189 | 20 | 24 | fits | 118,805 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,480,855 | 14.809 | 20 | 24 | fits | 67,935 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 117,838 | 1.178 | 20 | 50 | fits | 118,805 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 577,028 | 5.770 | 20 | 50 | fits | 160,006 | 89 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 305,231 | 3.052 | 18 | 18 | fits | 187,848 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,642,756 | 16.428 | 18 | 18 | fits | 50,771 | 18 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 434,580 | 4.346 | 20 | 20 | fits | 155,967 | 83 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 121,100 | 1.211 | 20 | 200 | fits | 118,805 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 578,617 | 5.786 | 20 | 200 | fits | 155,967 | 83 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 122,012 | 1.220 | 20 | 20 | fits | 118,805 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 833,749 | 8.337 | 20 | 20 | fits | 121,064 | 46 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 125,597 | 1.256 | 20 | 24 | fits | 118,805 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,498,644 | 14.986 | 20 | 24 | fits | 71,314 | 37 | 0.724 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 124,557 | 1.246 | 20 | 50 | fits | 118,805 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 582,293 | 5.823 | 20 | 50 | fits | 155,967 | 83 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 426,261 | 4.263 | 18 | 18 | fits | 186,612 | 104 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,648,498 | 16.485 | 18 | 18 | fits | 50,209 | 18 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 490,676 | 4.907 | 20 | 20 | fits | 166,102 | 101 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 127,819 | 1.278 | 20 | 200 | fits | 118,805 | 140 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 633,870 | 6.339 | 20 | 200 | fits | 166,102 | 101 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 128,731 | 1.287 | 20 | 20 | fits | 118,805 | 140 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 876,812 | 8.768 | 20 | 20 | fits | 120,656 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 132,316 | 1.323 | 20 | 24 | fits | 118,805 | 140 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,574,251 | 15.743 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 131,276 | 1.313 | 20 | 50 | fits | 118,805 | 140 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 637,546 | 6.375 | 20 | 50 | fits | 166,102 | 101 | 0.681 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 325,225 | 3.252 | 18 | 18 | fits | 194,404 | 145 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,623,188 | 16.232 | 18 | 18 | fits | 51,472 | 20 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 484,393 | 4.844 | 20 | 20 | fits | 154,359 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 137,424 | 1.374 | 20 | 200 | fits | 125,718 | 151 | 0.537 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 627,330 | 6.273 | 20 | 200 | fits | 154,359 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 138,336 | 1.383 | 20 | 20 | fits | 125,718 | 151 | 0.537 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 877,166 | 8.772 | 20 | 20 | fits | 127,692 | 57 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 141,921 | 1.419 | 20 | 24 | fits | 125,718 | 151 | 0.537 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,565,763 | 15.658 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 140,881 | 1.409 | 20 | 50 | fits | 125,718 | 151 | 0.537 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 631,006 | 6.310 | 20 | 50 | fits | 154,359 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 330,307 | 3.303 | 18 | 18 | fits | 189,881 | 145 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,614,700 | 16.147 | 18 | 18 | fits | 51,472 | 20 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 460,757 | 4.608 | 20 | 20 | fits | 154,223 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 116,717 | 1.167 | 20 | 200 | fits | 119,610 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 603,581 | 6.036 | 20 | 200 | fits | 154,223 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 117,629 | 1.176 | 20 | 20 | fits | 119,610 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 863,986 | 8.640 | 20 | 20 | fits | 121,090 | 46 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 121,214 | 1.212 | 20 | 24 | fits | 119,610 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,556,244 | 15.562 | 20 | 24 | fits | 68,113 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 120,174 | 1.202 | 20 | 50 | fits | 119,610 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 607,257 | 6.073 | 20 | 50 | fits | 154,223 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 306,883 | 3.069 | 18 | 18 | fits | 187,164 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,605,325 | 16.053 | 18 | 18 | fits | 51,616 | 20 | 0.730 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 454,707 | 4.547 | 20 | 20 | fits | 162,842 | 95 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 130,155 | 1.302 | 20 | 200 | fits | 119,610 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 597,109 | 5.971 | 20 | 200 | fits | 162,842 | 95 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 131,067 | 1.311 | 20 | 20 | fits | 119,610 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 840,262 | 8.403 | 20 | 20 | fits | 120,833 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 134,652 | 1.347 | 20 | 24 | fits | 119,610 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,525,981 | 15.260 | 20 | 24 | fits | 68,024 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 133,612 | 1.336 | 20 | 50 | fits | 119,610 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 600,785 | 6.008 | 20 | 50 | fits | 162,842 | 95 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 320,321 | 3.203 | 18 | 18 | fits | 187,164 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,661,515 | 16.615 | 18 | 18 | fits | 36,663 | 15 | 0.774 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 447,470 | 4.475 | 20 | 20 | fits | 156,056 | 83 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 130,547 | 1.305 | 20 | 200 | fits | 125,381 | 151 | 0.534 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 591,440 | 5.914 | 20 | 200 | fits | 156,056 | 83 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 131,459 | 1.315 | 20 | 20 | fits | 125,381 | 151 | 0.534 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 834,059 | 8.341 | 20 | 20 | fits | 120,636 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 135,044 | 1.350 | 20 | 24 | fits | 125,381 | 151 | 0.534 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,533,567 | 15.336 | 20 | 24 | fits | 67,509 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 134,004 | 1.340 | 20 | 50 | fits | 125,381 | 151 | 0.534 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 595,116 | 5.951 | 20 | 50 | fits | 156,056 | 83 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 438,995 | 4.390 | 18 | 18 | fits | 181,494 | 104 | 0.660 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,633,081 | 16.331 | 18 | 18 | fits | 50,433 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 465,933 | 4.659 | 20 | 20 | fits | 154,203 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 122,050 | 1.220 | 20 | 200 | fits | 119,626 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 608,646 | 6.086 | 20 | 200 | fits | 154,203 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 122,962 | 1.230 | 20 | 20 | fits | 119,626 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 825,751 | 8.258 | 20 | 20 | fits | 121,844 | 52 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 126,547 | 1.265 | 20 | 24 | fits | 119,626 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,496,058 | 14.961 | 20 | 24 | fits | 60,888 | 38 | 0.750 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 125,507 | 1.255 | 20 | 50 | fits | 119,626 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 612,322 | 6.123 | 20 | 50 | fits | 154,203 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 311,970 | 3.120 | 18 | 18 | fits | 186,918 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,650,546 | 16.505 | 18 | 18 | fits | 50,294 | 18 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 456,662 | 4.567 | 20 | 20 | fits | 156,808 | 89 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 116,724 | 1.167 | 20 | 200 | fits | 119,626 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 599,456 | 5.995 | 20 | 200 | fits | 156,808 | 89 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 117,636 | 1.176 | 20 | 20 | fits | 119,626 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 849,182 | 8.492 | 20 | 20 | fits | 120,858 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 121,221 | 1.212 | 20 | 24 | fits | 119,626 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,508,155 | 15.082 | 20 | 24 | fits | 67,800 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 120,181 | 1.202 | 20 | 50 | fits | 119,626 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 603,132 | 6.031 | 20 | 50 | fits | 156,808 | 89 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 306,644 | 3.066 | 18 | 18 | fits | 186,918 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,650,675 | 16.507 | 18 | 18 | fits | 43,039 | 21 | 0.787 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 422,123 | 4.221 | 20 | 20 | fits | 181,327 | 89 | 0.710 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 130,162 | 1.302 | 20 | 200 | fits | 119,626 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 584,490 | 5.845 | 20 | 200 | fits | 181,327 | 89 | 0.710 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 131,074 | 1.311 | 20 | 20 | fits | 119,626 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 828,414 | 8.284 | 20 | 20 | fits | 120,726 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 134,659 | 1.347 | 20 | 24 | fits | 119,626 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,529,554 | 15.296 | 20 | 24 | fits | 68,009 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 133,619 | 1.336 | 20 | 50 | fits | 119,626 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 588,166 | 5.882 | 20 | 50 | fits | 181,327 | 89 | 0.710 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 406,774 | 4.068 | 18 | 18 | fits | 152,347 | 100 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,665,394 | 16.654 | 18 | 18 | fits | 36,748 | 15 | 0.776 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 510,817 | 5.108 | 20 | 20 | fits | 143,555 | 60 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 169,054 | 1.691 | 20 | 200 | fits | 120,207 | 142 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 642,950 | 6.429 | 20 | 200 | fits | 143,555 | 60 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 169,966 | 1.700 | 20 | 20 | fits | 120,207 | 142 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 859,274 | 8.593 | 20 | 20 | fits | 121,521 | 52 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 53,344 | 0.533 | 20 | 24 | fits | 54,354 | 65 | 0.544 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,479,048 | 14.790 | 20 | 24 | fits | 67,610 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 52,304 | 0.523 | 20 | 50 | fits | 54,354 | 65 | 0.544 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 503,071 | 5.031 | 20 | 50 | fits | 137,199 | 76 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 365,807 | 3.658 | 18 | 18 | fits | 193,751 | 145 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,641,006 | 16.410 | 18 | 18 | fits | 50,771 | 18 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 478,267 | 4.783 | 20 | 20 | fits | 154,496 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 124,058 | 1.241 | 20 | 200 | fits | 119,716 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 621,338 | 6.213 | 20 | 200 | fits | 154,496 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 124,970 | 1.250 | 20 | 20 | fits | 119,716 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 864,156 | 8.642 | 20 | 20 | fits | 120,703 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 128,555 | 1.286 | 20 | 24 | fits | 119,716 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,504,061 | 15.041 | 20 | 24 | fits | 54,028 | 27 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 127,515 | 1.275 | 20 | 50 | fits | 119,716 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 625,014 | 6.250 | 20 | 50 | fits | 154,496 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 321,723 | 3.217 | 18 | 18 | fits | 194,663 | 151 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,686,958 | 16.870 | 18 | 18 | fits | 50,150 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 446,183 | 4.462 | 20 | 20 | fits | 156,124 | 83 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 130,841 | 1.308 | 20 | 200 | fits | 119,500 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 590,286 | 5.903 | 20 | 200 | fits | 156,124 | 83 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 131,753 | 1.318 | 20 | 20 | fits | 119,500 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 800,037 | 8.000 | 20 | 20 | fits | 87,607 | 37 | 0.639 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 135,338 | 1.353 | 20 | 24 | fits | 119,500 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,534,890 | 15.349 | 20 | 24 | fits | 68,213 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 134,298 | 1.343 | 20 | 50 | fits | 119,500 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 593,962 | 5.940 | 20 | 50 | fits | 156,124 | 83 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 437,773 | 4.378 | 18 | 18 | fits | 182,735 | 104 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,684,771 | 16.848 | 18 | 18 | fits | 50,294 | 18 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 472,169 | 4.722 | 20 | 20 | fits | 154,211 | 83 | 0.656 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 124,873 | 1.249 | 20 | 200 | fits | 125,630 | 151 | 0.541 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 615,023 | 6.150 | 20 | 200 | fits | 154,211 | 83 | 0.656 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 125,785 | 1.258 | 20 | 20 | fits | 125,630 | 151 | 0.541 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 830,440 | 8.304 | 20 | 20 | fits | 126,368 | 52 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 129,370 | 1.294 | 20 | 24 | fits | 125,630 | 151 | 0.541 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,557,103 | 15.571 | 20 | 24 | fits | 101,046 | 45 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 128,330 | 1.283 | 20 | 50 | fits | 125,630 | 151 | 0.541 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 618,699 | 6.187 | 20 | 50 | fits | 154,211 | 83 | 0.656 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 318,281 | 3.183 | 18 | 18 | fits | 190,406 | 145 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,698,524 | 16.985 | 18 | 18 | fits | 46,940 | 27 | 0.800 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 460,855 | 4.609 | 20 | 20 | fits | 120,271 | 74 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 116,314 | 1.163 | 20 | 200 | fits | 119,599 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 569,701 | 5.697 | 20 | 200 | fits | 120,271 | 74 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 117,226 | 1.172 | 20 | 20 | fits | 119,599 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 829,881 | 8.299 | 20 | 20 | fits | 132,598 | 64 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 120,811 | 1.208 | 20 | 24 | fits | 119,599 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,537,180 | 15.372 | 20 | 24 | fits | 107,731 | 56 | 0.749 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 119,771 | 1.198 | 20 | 50 | fits | 119,599 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 573,377 | 5.734 | 20 | 50 | fits | 120,271 | 74 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 307,025 | 3.070 | 18 | 18 | fits | 187,709 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,684,167 | 16.842 | 18 | 18 | fits | 36,826 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 440,342 | 4.403 | 20 | 20 | fits | 159,964 | 89 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 123,033 | 1.230 | 20 | 200 | fits | 119,599 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 581,660 | 5.817 | 20 | 200 | fits | 159,964 | 89 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 123,945 | 1.239 | 20 | 20 | fits | 119,599 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 837,159 | 8.372 | 20 | 20 | fits | 121,154 | 46 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 127,530 | 1.275 | 20 | 24 | fits | 119,599 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,566,344 | 15.663 | 20 | 24 | fits | 68,070 | 31 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 126,490 | 1.265 | 20 | 50 | fits | 119,599 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 585,336 | 5.853 | 20 | 50 | fits | 159,964 | 89 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 313,744 | 3.137 | 18 | 18 | fits | 187,709 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,665,888 | 16.659 | 18 | 18 | fits | 50,433 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 481,274 | 4.813 | 20 | 20 | fits | 166,478 | 101 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 129,752 | 1.298 | 20 | 200 | fits | 119,599 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 624,538 | 6.245 | 20 | 200 | fits | 166,478 | 101 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 130,664 | 1.307 | 20 | 20 | fits | 119,599 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 867,669 | 8.677 | 20 | 20 | fits | 120,615 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 134,249 | 1.342 | 20 | 24 | fits | 119,599 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,584,624 | 15.846 | 20 | 24 | fits | 100,278 | 45 | 0.738 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 133,209 | 1.332 | 20 | 50 | fits | 119,599 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 628,214 | 6.282 | 20 | 50 | fits | 166,478 | 101 | 0.681 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 290,786 | 2.908 | 18 | 18 | fits | 158,032 | 136 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,684,145 | 16.841 | 18 | 18 | fits | 50,211 | 18 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 441,860 | 4.419 | 20 | 20 | fits | 155,457 | 89 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 117,654 | 1.177 | 20 | 200 | fits | 119,599 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 584,443 | 5.844 | 20 | 200 | fits | 155,457 | 89 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 118,566 | 1.186 | 20 | 20 | fits | 119,599 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 827,560 | 8.276 | 20 | 20 | fits | 120,833 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 122,151 | 1.222 | 20 | 24 | fits | 119,599 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,512,668 | 15.127 | 20 | 24 | fits | 67,699 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 121,111 | 1.211 | 20 | 50 | fits | 119,599 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 588,119 | 5.881 | 20 | 50 | fits | 155,457 | 89 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 315,032 | 3.150 | 18 | 18 | fits | 194,376 | 145 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,682,571 | 16.826 | 18 | 18 | fits | 50,690 | 18 | 0.727 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 435,356 | 4.354 | 20 | 20 | fits | 156,124 | 83 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 118,711 | 1.187 | 20 | 200 | fits | 124,360 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 579,459 | 5.795 | 20 | 200 | fits | 156,124 | 83 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 119,623 | 1.196 | 20 | 20 | fits | 124,360 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 822,239 | 8.222 | 20 | 20 | fits | 120,636 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 123,208 | 1.232 | 20 | 24 | fits | 124,360 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,507,975 | 15.080 | 20 | 24 | fits | 67,699 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 122,168 | 1.222 | 20 | 50 | fits | 124,360 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 583,135 | 5.831 | 20 | 50 | fits | 156,124 | 83 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 426,946 | 4.269 | 18 | 18 | fits | 183,083 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,677,266 | 16.773 | 18 | 18 | fits | 36,663 | 15 | 0.774 |
| LINK_UP | `adp.link_up.if0` | 2,055 | 0.021 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| LINK_UP | `adp.link_up.if1` | 15,594 | 0.156 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,347 | 0.263 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,376 | 0.174 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 19,152 | 0.192 | 20 | 200 | fits | 4,182 | 18 (11) | 0.375 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 17,240 | 0.172 | 20 | 200 | fits | 4,182 | 18 (11) | 0.375 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,448 | 0.134 | 20 | 50 | fits | 120,721 | 50 | 0.689 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 19,406 | 0.194 | 20 | 50 | fits | 29,302 | 38 | 0.560 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 21,478 | 0.215 | 20 | 50 | fits | 29,187 | 38 | 0.551 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 13,221 | 0.132 | 20 | 50 | fits | 35,011 | 65 | 0.500 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 15,148 | 0.151 | 20 | 50 | fits | 35,011 | 65 | 0.500 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 10,977 | 0.110 | 20 | 50 | fits | 27,248 | 33 | 0.449 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 12,224 | 0.122 | 20 | 50 | fits | 113,355 | 50 | 0.631 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 20,198 | 0.202 | 20 | 50 | fits | 30,270 | 38 | 0.556 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 14,211 | 0.142 | 20 | 50 | fits | 29,544 | 38 | 0.506 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 24,109 | 0.241 | 20 | 50 | fits | 36,872 | 65 | 0.521 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 26,268 | 0.263 | 20 | 50 | fits | 36,872 | 65 | 0.521 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 11,211 | 0.112 | 20 | 50 | fits | 28,668 | 33 | 0.436 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 37,842 | 0.378 | 20 | 20 | fits | 52,410 | 30 (35) | 0.728 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 27,382 | 0.274 | 20 | 20 | fits | 48,183 | 24 (35) | 0.709 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 34,140 | 0.341 | 20 | 20 | fits | 47,777 | 25 (14) | 0.771 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 19,267 | 0.193 | 20 | 20 | fits | 42,732 | 19 (14) | 0.790 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 18,460 | 0.185 | 20 | 20 | fits | 57,913 | 47 (14) | 0.698 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 13,831 | 0.138 | 20 | 20 | fits | 42,007 | 19 (14) | 0.772 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 48,179 | 0.482 | 20 | 20 | fits | 51,279 | 24 (35) | 0.753 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 41,676 | 0.417 | 20 | 20 | fits | 63,843 | 51 (35) | 0.701 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 156,337 | 1.563 | 18 | 18 | fits | 46,041 | 14 | 0.823 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 148,390 | 1.484 | 18 | 18 | fits | 45,579 | 14 | 0.812 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 59,386 | 0.594 | 18 | 18 | fits | 59,451 | 15 | 0.883 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,760 | 0.248 | 18 | 18 | fits | 24,825 | 15 | 0.458 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 173,042 | 1.730 | 218 | 218 | fits | 188,971 | 22 | 0.797 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 52,182 | 0.522 | 18 | 18 | fits | 52,247 | 15 | 0.869 |
| malformed MRPDU discard | `srp.malformed.if1` | 24,430 | 0.244 | 18 | 18 | fits | 24,495 | 15 | 0.480 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 151,165 | 1.512 | 218 | 218 | fits | 164,194 | 22 | 0.794 |
| an event behind 15 others | `backlog.event.if0` | 147,275 | 1.473 | 20 | 200 | fits | 115,439 | 125 | 0.531 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 659,294 | 6.593 | 20 | 20 | fits | 108,104 | 52 | 0.667 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 136,650 | 1.367 | 20 | 200 | fits | 136,858 | 143 | 0.538 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 537,084 | 5.371 | 20 | 200 | fits | 129,808 | 57 | 0.692 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 132,391 | 1.324 | 20 | 20 | fits | 136,858 | 143 | 0.538 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 724,886 | 7.249 | 20 | 20 | fits | 108,104 | 52 | 0.667 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 135,976 | 1.360 | 20 | 24 | fits | 136,858 | 143 | 0.538 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,241,993 | 12.420 | 20 | 24 | fits | 51,416 | 31 | 0.692 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 134,936 | 1.349 | 20 | 50 | fits | 136,858 | 143 | 0.538 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 535,589 | 5.356 | 20 | 50 | fits | 129,808 | 57 | 0.692 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 535,524 | 5.355 | 18 | 18 | fits | 129,808 | 57 | 0.692 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,378,226 | 13.782 | 18 | 18 | fits | 34,291 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 360,180 | 3.602 | 20 | 20 | fits | 196,295 | 89 | 0.701 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 111,586 | 1.116 | 20 | 200 | fits | 116,268 | 140 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 538,849 | 5.388 | 20 | 200 | fits | 196,295 | 89 | 0.701 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 112,498 | 1.125 | 20 | 20 | fits | 116,268 | 140 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 783,380 | 7.834 | 20 | 20 | fits | 120,750 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 116,083 | 1.161 | 20 | 24 | fits | 116,268 | 140 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,469,482 | 14.695 | 20 | 24 | fits | 67,690 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 115,043 | 1.150 | 20 | 50 | fits | 116,268 | 140 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 542,525 | 5.425 | 20 | 50 | fits | 196,295 | 89 | 0.701 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 542,460 | 5.425 | 18 | 18 | fits | 196,295 | 89 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,655,570 | 16.556 | 18 | 18 | fits | 36,739 | 15 | 0.776 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,791 | 0.118 | 20 | 20 | fits | 44,947 | 21 | 0.758 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 111,586 | 1.116 | 20 | 200 | fits | 116,268 | 140 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 48,404 | 0.484 | 20 | 200 | fits | 44,947 | 21 | 0.758 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 112,498 | 1.125 | 20 | 20 | fits | 116,268 | 140 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 763,081 | 7.631 | 20 | 20 | fits | 120,614 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 116,083 | 1.161 | 20 | 24 | fits | 116,268 | 140 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,463,124 | 14.631 | 20 | 24 | fits | 67,500 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 115,043 | 1.150 | 20 | 50 | fits | 116,268 | 140 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 522,216 | 5.222 | 20 | 50 | fits | 175,986 | 79 | 0.703 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 522,151 | 5.222 | 18 | 18 | fits | 175,986 | 79 | 0.703 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,612,913 | 16.129 | 18 | 18 | fits | 50,293 | 18 | 0.713 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,374,561 | 63.746 | 20 | 20 | MISS ceiling | 50,305 | 27 | 0.564 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,105,137 | 361.051 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,105,062 | 361.051 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,104,987 | 361.050 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,104,912 | 361.049 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 120,101 | 1.201 | 20 | 200 | fits | 113,031 | 134 | 0.503 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 585,012 | 5.850 | 20 | 200 | fits | 132,000 | 69 | 0.663 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 115,842 | 1.158 | 20 | 20 | fits | 113,031 | 134 | 0.503 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 785,480 | 7.855 | 20 | 20 | fits | 100,585 | 35 | 0.743 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 119,427 | 1.194 | 20 | 24 | fits | 113,031 | 134 | 0.503 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,509,757 | 65.098 | 20 | 24 | MISS ceiling | 31,656 | 23 | 0.516 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 118,387 | 1.184 | 20 | 50 | fits | 113,031 | 134 | 0.503 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 583,517 | 5.835 | 20 | 50 | fits | 132,000 | 69 | 0.663 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 308,285 | 3.083 | 18 | 18 | fits | 190,353 | 138 | 0.647 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,336,197 | 13.362 | 18 | 18 | fits | 49,338 | 21 | 0.674 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 18,499 | 0.185 | 20 | 20 | fits | 74,459 | 46 (29) | 0.663 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 37,334 | 0.373 | 20 | 20 | fits | 74,459 | 46 (29) | 0.663 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,488 | 0.075 | 20 | 20 | fits | 63,202 | 30 (35) | 0.667 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 27,040 | 0.270 | 20 | 20 | fits | 63,202 | 30 (35) | 0.667 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 7,987 | 0.080 | 20 | 20 | fits | 45,474 | 19 (12) | 0.796 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 24,345 | 0.243 | 20 | 20 | fits | 51,862 | 24 (12) | 0.761 |
| LINK_UP | `adp.link_up.if0` | 2,055 | 0.021 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| LINK_UP | `adp.link_up.if1` | 15,594 | 0.156 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,347 | 0.263 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,376 | 0.174 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| LINK_DOWN | `adp.link_down.if0` | 1,845 | 0.018 | 20 | 200 | fits | 60,737 | 38 (9) | 0.646 |
| LINK_DOWN | `adp.link_down.if1` | 29,672 | 0.297 | 20 | 200 | fits | 60,737 | 38 (9) | 0.646 |
| LINK_UP | `adp.link_up.if0` | 2,055 | 0.021 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| LINK_UP | `adp.link_up.if1` | 15,594 | 0.156 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,347 | 0.263 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,376 | 0.174 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| GM_CHANGE | `adp.gm_change.if0` | 1,813 | 0.018 | 20 | 200 | fits | 20,838 | 28 (11) | 0.250 |
| GM_CHANGE | `adp.gm_change.if1` | 3,274 | 0.033 | 20 | 200 | fits | 20,838 | 28 (11) | 0.250 |
| LINK_UP | `adp.link_up.if0` | 2,055 | 0.021 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| LINK_UP | `adp.link_up.if1` | 15,594 | 0.156 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,347 | 0.263 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,376 | 0.174 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 3,085 | 0.031 | 20 | 200 | fits | 21,916 | 25 (31) | 0.318 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 4,478 | 0.045 | 20 | 200 | fits | 21,916 | 25 (31) | 0.318 |
| LINK_UP | `adp.link_up.if0` | 2,055 | 0.021 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| LINK_UP | `adp.link_up.if1` | 15,594 | 0.156 | 20 | 200 | fits | 132,078 | 86 (11) | 0.630 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,347 | 0.263 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 17,376 | 0.174 | 20 | 200 | fits | 37,955 | 42 (39) | 0.431 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 3,085 | 0.031 | 20 | 200 | fits | 20,521 | 18 (31) | 0.429 |
| set_name | `aecp_fanout.set_name.if0` | 110,056 | 1.101 | 20 | 24 | fits | 144,890 | 225 | 0.214 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 90,639 | 0.906 | 20 | 24 | fits | 89,859 | 205 | 0.231 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 87,852 | 0.879 | 20 | 24 | fits | 84,194 | 205 | 0.196 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 74,158 | 0.742 | 20 | 24 | fits | 83,563 | 205 | 0.189 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 87,620 | 0.876 | 20 | 24 | fits | 86,274 | 181 | 0.218 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 88,173 | 0.882 | 20 | 24 | fits | 84,350 | 205 | 0.194 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 75,454 | 0.755 | 20 | 24 | fits | 84,228 | 205 | 0.191 |
| set_name | `aecp_fanout.set_name.if1` | 102,919 | 1.029 | 20 | 24 | fits | 142,985 | 187 | 0.194 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 90,998 | 0.910 | 20 | 24 | fits | 90,239 | 205 | 0.235 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 74,746 | 0.747 | 20 | 24 | fits | 83,691 | 205 | 0.194 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 74,160 | 0.742 | 20 | 24 | fits | 83,688 | 205 | 0.191 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 87,450 | 0.875 | 20 | 24 | fits | 83,501 | 205 | 0.181 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 75,436 | 0.754 | 20 | 24 | fits | 84,112 | 205 | 0.190 |
| BIND_RX | `acmp.bind_rx.if0` | 25,842 | 0.258 | 20 | 20 | fits | 67,379 | 30 (77) | 0.761 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,900 | 0.089 | 20 | 20 | fits | 48,257 | 21 (32) | 0.820 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 12,158 | 0.122 | 20 | 20 | fits | 54,994 | 28 (47) | 0.749 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 16,569 | 0.166 | 20 | 20 | fits | 62,624 | 21 (50) | 0.838 |
| PROBE_TX | `acmp.probe_tx.if0` | 12,603 | 0.126 | 20 | 20 | fits | 47,426 | 20 (48) | 0.726 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 12,416 | 0.124 | 20 | 20 | fits | 53,280 | 29 (48) | 0.737 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 11,890 | 0.119 | 20 | 20 | fits | 46,382 | 19 (48) | 0.729 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 10,996 | 0.110 | 20 | 20 | fits | 44,991 | 19 (48) | 0.683 |
| BIND_RX | `acmp.bind_rx.if1` | 21,624 | 0.216 | 20 | 20 | fits | 62,481 | 31 (77) | 0.717 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 8,528 | 0.085 | 20 | 20 | fits | 53,336 | 32 (32) | 0.786 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 12,933 | 0.129 | 20 | 20 | fits | 51,023 | 19 (47) | 0.755 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 25,534 | 0.255 | 20 | 20 | fits | 73,437 | 40 (50) | 0.805 |
| PROBE_TX | `acmp.probe_tx.if1` | 13,504 | 0.135 | 20 | 20 | fits | 49,547 | 21 (48) | 0.732 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 23,224 | 0.232 | 20 | 20 | fits | 58,941 | 38 (48) | 0.742 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 11,116 | 0.111 | 20 | 20 | fits | 45,878 | 20 (48) | 0.677 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 10,999 | 0.110 | 20 | 20 | fits | 45,704 | 20 (48) | 0.669 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 20,649 | 0.206 | 20 | 24 | fits | 30,548 | 24 | 0.706 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 35,470 | 0.355 | 20 | 24 | fits | 34,749 | 24 | 0.618 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 31,297 | 0.313 | 20 | 24 | fits | 30,451 | 24 | 0.627 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 22,155 | 0.222 | 20 | 24 | fits | 29,721 | 24 | 0.578 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 30,635 | 0.306 | 20 | 24 | fits | 29,977 | 24 | 0.585 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 23,057 | 0.231 | 20 | 24 | fits | 30,544 | 24 | 0.595 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 30,123 | 0.301 | 20 | 24 | fits | 29,372 | 24 | 0.605 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 28,375 | 0.284 | 20 | 24 | fits | 29,800 | 24 | 0.607 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 22,056 | 0.221 | 20 | 24 | fits | 29,543 | 24 | 0.613 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 35,775 | 0.358 | 20 | 24 | fits | 35,193 | 24 | 0.531 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 21,588 | 0.216 | 20 | 24 | fits | 28,945 | 24 | 0.626 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 30,290 | 0.303 | 20 | 24 | fits | 29,381 | 24 | 0.642 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 28,097 | 0.281 | 20 | 24 | fits | 35,884 | 30 | 0.620 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 22,987 | 0.230 | 20 | 24 | fits | 30,474 | 24 | 0.600 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 31,227 | 0.312 | 20 | 24 | fits | 30,518 | 24 | 0.621 |
| get_configuration | `aecp.get_configuration.if0` | 19,497 | 0.195 | 20 | 24 | fits | 26,835 | 24 | 0.561 |
| entity_available | `aecp.entity_available.if0` | 28,685 | 0.287 | 20 | 24 | fits | 27,736 | 24 | 0.566 |
| get_name | `aecp.get_name.if0` | 22,248 | 0.222 | 20 | 24 | fits | 30,200 | 24 | 0.646 |
| get_counters | `aecp.get_counters.if0` | 23,936 | 0.239 | 20 | 24 | fits | 31,786 | 31 | 0.627 |
| get_avb_info | `aecp.get_avb_info.if0` | 29,872 | 0.299 | 20 | 24 | fits | 29,439 | 24 | 0.659 |
| unknown_command | `aecp.unknown_command.if0` | 23,110 | 0.231 | 20 | 24 | fits | 27,899 | 24 | 0.623 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 28,983 | 0.290 | 20 | 24 | fits | 28,233 | 24 | 0.616 |
| set_name | `aecp.set_name.if0` | 56,812 | 0.568 | 20 | 24 | fits | 95,604 | 69 | 0.607 |
| lock_entity | `aecp.lock_entity.if0` | 26,999 | 0.270 | 20 | 24 | fits | 40,557 | 50 | 0.614 |
| unlock_entity | `aecp.unlock_entity.if0` | 36,223 | 0.362 | 20 | 24 | fits | 40,281 | 50 | 0.608 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 20,208 | 0.202 | 20 | 24 | fits | 28,216 | 22 | 0.590 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 35,931 | 0.359 | 20 | 24 | fits | 32,840 | 22 | 0.580 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 32,805 | 0.328 | 20 | 24 | fits | 30,126 | 22 | 0.625 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 23,648 | 0.236 | 20 | 24 | fits | 29,475 | 22 | 0.577 |
| get_configuration | `aecp.get_configuration.if1` | 29,625 | 0.296 | 20 | 24 | fits | 26,992 | 22 | 0.568 |
| entity_available | `aecp.entity_available.if1` | 21,358 | 0.214 | 20 | 24 | fits | 27,036 | 22 | 0.534 |
| get_name | `aecp.get_name.if1` | 32,342 | 0.323 | 20 | 24 | fits | 30,209 | 22 | 0.653 |
| get_counters | `aecp.get_counters.if1` | 33,209 | 0.332 | 20 | 24 | fits | 31,633 | 29 | 0.633 |
| get_avb_info | `aecp.get_avb_info.if1` | 22,541 | 0.225 | 20 | 24 | fits | 28,515 | 22 | 0.634 |
| unknown_command | `aecp.unknown_command.if1` | 29,806 | 0.298 | 20 | 24 | fits | 27,528 | 22 | 0.606 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 21,564 | 0.216 | 20 | 24 | fits | 27,420 | 22 | 0.590 |
| set_name | `aecp.set_name.if1` | 62,902 | 0.629 | 20 | 24 | fits | 90,284 | 31 | 0.615 |
| lock_entity | `aecp.lock_entity.if1` | 37,885 | 0.379 | 20 | 24 | fits | 41,849 | 55 | 0.570 |
| unlock_entity | `aecp.unlock_entity.if1` | 28,508 | 0.285 | 20 | 24 | fits | 40,731 | 55 | 0.547 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
