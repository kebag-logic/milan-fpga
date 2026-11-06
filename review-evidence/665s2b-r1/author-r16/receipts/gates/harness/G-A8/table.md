### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 134 paths and 6 of 984 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.256 (0.614) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.225 (0.570) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.126 (0.449) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.107 (0.430) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.076 (0.603) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.273 (0.603) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.054 (0.567) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.240 (0.567) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.122 (0.451) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.128 (0.475) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.107 (0.422) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.107 (0.430) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.114 (0.424) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.126 (0.450) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.122 (0.439) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.140 (0.471) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.089 (0.433) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.088 (0.436) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.443 (1.794) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.479 (1.855) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.083 (0.810) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.282 (0.882) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.261 (0.786) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.130 (0.663) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.278 (0.733) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.089 (0.626) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.142 (0.778) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.190 (0.798) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.264 (0.733) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.075 (0.604) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.162 (0.546) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.155 (0.552) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.035 (0.190) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.050 (0.190) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.187) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.042 (0.187) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.023 (0.679) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.330 (0.679) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.028 (0.425) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.170 (0.425) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.118 (0.327) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.092 (0.327) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.206 (0.574) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.126 (0.574) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.252 (0.557) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.305 (0.611) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.192 (0.339) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 0.286 (0.598) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.271 (0.528) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.298 (0.556) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.293 (0.607) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 0.336 (0.607) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.289 (0.552) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.298 (0.611) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.322 (0.683) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.360 (0.704) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.251 (0.559) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.302 (0.612) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.328 (0.641) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.338 (0.651) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.217 (0.516) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.325 (0.590) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.288 (0.555) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.291 (0.603) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.321 (0.630) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.286 (0.550) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.265 (0.575) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.298 (0.618) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.308 (0.620) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.287 (0.550) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.277 (0.587) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.274 (0.584) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.275 (0.589) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.299 (0.566) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.267 (0.578) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.259 (0.557) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.274 (0.582) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.419 (0.780) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.400 (0.788) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.309 (0.561) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 0.295 (0.557) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.332 (0.644) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.355 (0.733) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.770 (1.153) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.760 (1.149) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.779 (1.183) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.778 (1.178) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.800 (1.187) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 0.809 (1.195) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.959 (1.336) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.861 (1.257) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.752 (1.150) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.828 (1.214) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.827 (1.212) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.106 (7.840) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-4.adp_available.if0` (backlog-adp@program-aged2-4) | 6.666 (8.069) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.089 (0.457) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.505 (2.559) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.552 (63.918) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.408 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 8.391 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.743 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 11.234 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 5.268 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 15.076 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.185 (0.566) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.233 (0.631) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.115 (0.256) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.112 (0.257) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.145 (0.311) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.133 (0.306) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.168 (0.566) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.214 (0.631) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.244 (0.605) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 0.204 (0.581) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.863 | fits | 0 acmp | 76 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.acmp.last.if0` (backlog-adp@program-aged2-4) | 10.165 | fits | 11 acmp | 76 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.854 | fits | 0 adp | 76 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.adp.last.if0` (backlog-adp@program-aged2-4) | 7.971 | fits | 7 adp | 74 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 6.580 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.899 | fits | 0 aecp | 76 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.811 | MISS ceiling | 15 aecp | 76 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.888 | fits | 0 maap | 76 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.maap.last.if0` (backlog-adp@blank-aged2-7) | 6.511 | fits | 6 maap | 76 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.487 | fits | 0 srp | 76 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-aged1-7.service.srp.last.if1` (backlog-adp@verify-aged1-7) | 17.765 | fits | 31 srp | 76 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 2.034 (2.208) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.729 (1.877) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.578 (0.579) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.501 (0.501) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.221 (0.222) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.221 (0.221) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 8.557 (8.672) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 9.302 (9.409) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.480 | 22 | 188,691 (1.887) | yes | - |
| backlog-adp@blank-1 | 0 | 17.834 | 21 | 188,730 (1.887) | yes | - |
| backlog-adp@blank-2 | 0 | 18.711 | 21 | 182,674 (1.827) | yes | - |
| backlog-adp@blank-3 | 0 | 17.952 | 21 | 190,301 (1.903) | yes | - |
| backlog-adp@blank-4 | 0 | 17.760 | 21 | 188,585 (1.886) | yes | - |
| backlog-adp@blank-5 | 0 | 17.861 | 21 | 188,585 (1.886) | yes | - |
| backlog-adp@blank-6 | 0 | 18.197 | 22 | 163,148 (1.631) | yes | - |
| backlog-adp@blank-7 | 0 | 17.932 | 21 | 149,710 (1.497) | yes | - |
| backlog-adp@program-0 | 0 | 17.497 | 20 | 187,435 (1.874) | yes | - |
| backlog-adp@program-1 | 0 | 18.551 | 24 | 187,471 (1.875) | yes | - |
| backlog-adp@program-2 | 0 | 18.133 | 21 | 187,608 (1.876) | yes | - |
| backlog-adp@program-3 | 0 | 18.089 | 22 | 162,902 (1.629) | yes | - |
| backlog-adp@program-4 | 0 | 16.801 | 20 | 187,239 (1.872) | yes | - |
| backlog-adp@program-5 | 0 | 17.292 | 21 | 187,275 (1.873) | yes | - |
| backlog-adp@program-6 | 0 | 17.224 | 21 | 188,720 (1.887) | yes | - |
| backlog-adp@program-7 | 0 | 17.037 | 21 | 162,902 (1.629) | yes | - |
| backlog-adp@verify-0 | 0 | 18.012 | 20 | 190,420 (1.904) | yes | - |
| backlog-adp@verify-1 | 0 | 19.143 | 21 | 189,947 (1.899) | yes | - |
| backlog-adp@verify-2 | 0 | 18.086 | 21 | 188,611 (1.886) | yes | - |
| backlog-adp@verify-3 | 0 | 18.844 | 23 | 188,575 (1.886) | yes | - |
| backlog-adp@verify-4 | 0 | 18.417 | 23 | 188,611 (1.886) | yes | - |
| backlog-adp@verify-5 | 0 | 18.494 | 22 | 162,703 (1.627) | yes | - |
| backlog-adp@verify-6 | 0 | 18.249 | 21 | 166,266 (1.663) | yes | - |
| backlog-adp@verify-7 | 0 | 18.264 | 21 | 182,437 (1.824) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 17.764 | 22 | 188,833 (1.888) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 17.356 | 19 | 189,582 (1.896) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 18.743 | 22 | 187,582 (1.876) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 18.499 | 21 | 188,481 (1.885) | yes | - |
| backlog-adp@blank-aged2-4 | 1 | 19.199 | 22 | 189,452 (1.895) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 18.613 | 22 | 188,481 (1.885) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 18.648 | 22 | 165,531 (1.655) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 18.357 | 20 | 165,382 (1.654) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 17.497 | 21 | 188,598 (1.886) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 17.501 | 21 | 187,420 (1.874) | yes | - |
| backlog-adp@blank-aged1-2 | 1 | 18.526 | 19 | 189,597 (1.896) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 17.494 | 20 | 188,626 (1.886) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 17.801 | 20 | 188,626 (1.886) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 18.012 | 21 | 188,626 (1.886) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 18.126 | 22 | 163,098 (1.631) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 17.957 | 22 | 182,833 (1.828) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 17.741 | 20 | 188,325 (1.883) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 17.715 | 21 | 187,354 (1.874) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 18.150 | 22 | 181,644 (1.816) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 18.118 | 21 | 189,048 (1.890) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 18.003 | 21 | 187,561 (1.876) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 17.876 | 21 | 188,532 (1.885) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 17.858 | 22 | 162,365 (1.624) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 17.810 | 21 | 162,269 (1.623) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 17.819 | 21 | 166,342 (1.663) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 17.656 | 20 | 188,813 (1.888) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 18.205 | 22 | 187,326 (1.873) | yes | - |
| backlog-adp@program-aged1-3 | 1 | 18.023 | 21 | 188,297 (1.883) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 17.626 | 20 | 187,326 (1.873) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 17.655 | 20 | 186,148 (1.861) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 17.803 | 22 | 162,891 (1.629) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 17.540 | 19 | 162,902 (1.629) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 18.209 | 23 | 190,113 (1.901) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 18.107 | 22 | 188,626 (1.886) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 18.854 | 20 | 189,597 (1.896) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 18.861 | 21 | 187,525 (1.875) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 19.048 | 21 | 188,274 (1.883) | yes | - |
| backlog-adp@verify-aged2-5 | 1 | 19.554 | 23 | 189,245 (1.892) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 19.052 | 22 | 160,299 (1.603) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 19.179 | 22 | 162,560 (1.626) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 17.816 | 20 | 189,347 (1.893) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 17.943 | 22 | 187,363 (1.874) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 19.173 | 21 | 188,419 (1.884) | yes | - |
| backlog-adp@verify-aged1-3 | 1 | 18.008 | 19 | 189,390 (1.894) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 18.393 | 22 | 188,419 (1.884) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 18.132 | 20 | 188,419 (1.884) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 18.358 | 22 | 182,929 (1.829) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 18.641 | 23 | 182,866 (1.829) | yes | - |
| backlog | 0 | 14.728 | 21 | 162,846 (1.628) | yes | - |
| backlog-adp | 0 | 17.342 | 23 | 160,997 (1.610) | yes | - |
| backlog-adp-refill | 0 | 40.947 | 32 | 140,480 (1.405) | yes | - |
| backlog-owed | 0 | 360.458 | 66 | 160,340 (1.603) | yes | - |

Composed maximum over the 4 backlog windows: 162,846 CPU cycles (1.628 ms), backlog.
Over the windows that released their whole load only: 162,846 (1.628 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 129900 | 0 | 130,867 (1.309) | fits |
| save-held | 8623 | 0 | 165,978 (1.660) | fits |
| save-starved | 57407 | 0 | 168,703 (1.687) | fits |
| acmp-notk | 3642 | 0 | 130,212 (1.302) | fits |
| backlog-adp@blank-0 | 571 | 0 | 188,691 (1.887) | fits |
| backlog-adp@blank-1 | 570 | 0 | 188,730 (1.887) | fits |
| backlog-adp@blank-2 | 570 | 0 | 182,674 (1.827) | fits |
| backlog-adp@blank-3 | 570 | 0 | 190,301 (1.903) | fits |
| backlog-adp@blank-4 | 572 | 0 | 188,585 (1.886) | fits |
| backlog-adp@blank-5 | 572 | 0 | 188,585 (1.886) | fits |
| backlog-adp@blank-6 | 573 | 0 | 163,148 (1.631) | fits |
| backlog-adp@blank-7 | 572 | 0 | 149,710 (1.497) | fits |
| backlog-adp@program-0 | 945 | 0 | 187,435 (1.874) | fits |
| backlog-adp@program-1 | 949 | 0 | 187,471 (1.875) | fits |
| backlog-adp@program-2 | 947 | 0 | 187,608 (1.876) | fits |
| backlog-adp@program-3 | 947 | 0 | 162,902 (1.629) | fits |
| backlog-adp@program-4 | 948 | 0 | 187,239 (1.872) | fits |
| backlog-adp@program-5 | 949 | 0 | 187,275 (1.873) | fits |
| backlog-adp@program-6 | 949 | 0 | 188,720 (1.887) | fits |
| backlog-adp@program-7 | 951 | 0 | 162,902 (1.629) | fits |
| backlog-adp@verify-0 | 1309 | 0 | 190,420 (1.904) | fits |
| backlog-adp@verify-1 | 1309 | 0 | 189,947 (1.899) | fits |
| backlog-adp@verify-2 | 1311 | 0 | 188,611 (1.886) | fits |
| backlog-adp@verify-3 | 1313 | 0 | 188,575 (1.886) | fits |
| backlog-adp@verify-4 | 1313 | 0 | 188,611 (1.886) | fits |
| backlog-adp@verify-5 | 1312 | 0 | 162,703 (1.627) | fits |
| backlog-adp@verify-6 | 1311 | 0 | 166,266 (1.663) | fits |
| backlog-adp@verify-7 | 1312 | 0 | 182,437 (1.824) | fits |
| backlog-adp@blank-aged2-0 | 832 | 0 | 188,833 (1.888) | fits |
| backlog-adp@blank-aged2-1 | 836 | 0 | 189,582 (1.896) | fits |
| backlog-adp@blank-aged2-2 | 845 | 0 | 187,582 (1.876) | fits |
| backlog-adp@blank-aged2-3 | 852 | 0 | 188,481 (1.885) | fits |
| backlog-adp@blank-aged2-4 | 860 | 0 | 189,452 (1.895) | fits |
| backlog-adp@blank-aged2-5 | 866 | 0 | 188,481 (1.885) | fits |
| backlog-adp@blank-aged2-6 | 873 | 0 | 165,531 (1.655) | fits |
| backlog-adp@blank-aged2-7 | 878 | 0 | 165,382 (1.654) | fits |
| backlog-adp@blank-aged1-0 | 776 | 0 | 188,598 (1.886) | fits |
| backlog-adp@blank-aged1-1 | 783 | 0 | 187,420 (1.874) | fits |
| backlog-adp@blank-aged1-2 | 789 | 0 | 189,597 (1.896) | fits |
| backlog-adp@blank-aged1-3 | 796 | 0 | 188,626 (1.886) | fits |
| backlog-adp@blank-aged1-4 | 803 | 0 | 188,626 (1.886) | fits |
| backlog-adp@blank-aged1-5 | 811 | 0 | 188,626 (1.886) | fits |
| backlog-adp@blank-aged1-6 | 819 | 0 | 163,098 (1.631) | fits |
| backlog-adp@blank-aged1-7 | 826 | 0 | 182,833 (1.828) | fits |
| backlog-adp@program-aged2-0 | 1202 | 0 | 188,325 (1.883) | fits |
| backlog-adp@program-aged2-1 | 1209 | 0 | 187,354 (1.874) | fits |
| backlog-adp@program-aged2-2 | 1217 | 0 | 181,644 (1.816) | fits |
| backlog-adp@program-aged2-3 | 1223 | 0 | 189,048 (1.890) | fits |
| backlog-adp@program-aged2-4 | 1230 | 0 | 187,561 (1.876) | fits |
| backlog-adp@program-aged2-5 | 1237 | 0 | 188,532 (1.885) | fits |
| backlog-adp@program-aged2-6 | 1244 | 0 | 162,365 (1.624) | fits |
| backlog-adp@program-aged2-7 | 1251 | 0 | 162,269 (1.623) | fits |
| backlog-adp@program-aged1-0 | 1148 | 0 | 166,342 (1.663) | fits |
| backlog-adp@program-aged1-1 | 1154 | 0 | 188,813 (1.888) | fits |
| backlog-adp@program-aged1-2 | 1163 | 0 | 187,326 (1.873) | fits |
| backlog-adp@program-aged1-3 | 1169 | 0 | 188,297 (1.883) | fits |
| backlog-adp@program-aged1-4 | 1174 | 0 | 187,326 (1.873) | fits |
| backlog-adp@program-aged1-5 | 1181 | 0 | 186,148 (1.861) | fits |
| backlog-adp@program-aged1-6 | 1190 | 0 | 162,891 (1.629) | fits |
| backlog-adp@program-aged1-7 | 1194 | 0 | 162,902 (1.629) | fits |
| backlog-adp@verify-aged2-0 | 1572 | 0 | 190,113 (1.901) | fits |
| backlog-adp@verify-aged2-1 | 1578 | 0 | 188,626 (1.886) | fits |
| backlog-adp@verify-aged2-2 | 1583 | 0 | 189,597 (1.896) | fits |
| backlog-adp@verify-aged2-3 | 1590 | 0 | 187,525 (1.875) | fits |
| backlog-adp@verify-aged2-4 | 1598 | 0 | 188,274 (1.883) | fits |
| backlog-adp@verify-aged2-5 | 1607 | 0 | 189,245 (1.892) | fits |
| backlog-adp@verify-aged2-6 | 1612 | 0 | 160,299 (1.603) | fits |
| backlog-adp@verify-aged2-7 | 1619 | 0 | 162,560 (1.626) | fits |
| backlog-adp@verify-aged1-0 | 1515 | 0 | 189,347 (1.893) | fits |
| backlog-adp@verify-aged1-1 | 1523 | 0 | 187,363 (1.874) | fits |
| backlog-adp@verify-aged1-2 | 1530 | 0 | 188,419 (1.884) | fits |
| backlog-adp@verify-aged1-3 | 1535 | 0 | 189,390 (1.894) | fits |
| backlog-adp@verify-aged1-4 | 1544 | 0 | 188,419 (1.884) | fits |
| backlog-adp@verify-aged1-5 | 1549 | 0 | 188,419 (1.884) | fits |
| backlog-adp@verify-aged1-6 | 1558 | 0 | 182,929 (1.829) | fits |
| backlog-adp@verify-aged1-7 | 1566 | 0 | 182,866 (1.829) | fits |
| adp-advertise | 613 | 0 | 109,314 (1.093) | fits |
| maap | 358 | 0 | 111,310 (1.113) | fits |
| acmp-noresp | 2026 | 0 | 129,096 (1.291) | fits |
| save | 625 | 0 | 125,422 (1.254) | fits |
| srp | 318 | 0 | 171,351 (1.714) | fits |
| backlog | 309 | 0 | 162,846 (1.628) | fits |
| backlog-adp | 336 | 0 | 160,997 (1.610) | fits |
| backlog-adp-refill | 345 | 0 | 140,480 (1.405) | fits |
| backlog-owed | 365 | 0 | 160,340 (1.603) | fits |
| acmp-disc | 1056 | 0 | 124,327 (1.243) | fits |
| adp-link | 95 | 0 | 108,899 (1.089) | fits |
| adp-gm | 93 | 0 | 108,899 (1.089) | fits |
| adp-discover | 93 | 0 | 108,899 (1.089) | fits |
| control | 93 | 0 | 108,899 (1.089) | fits |
| aecp-fanout | 150 | 0 | 108,899 (1.089) | fits |
| acmp-cmd | 111 | 0 | 108,899 (1.089) | fits |
| aecp | 139 | 0 | 108,899 (1.089) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +10.248 ms, 77,900 (0.779 ms), read-back | none | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 17.146 (18) | 0.854 |
| backlog-adp@blank-aged2-1 | 2 | +9.013 ms, 77,835 (0.778 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 16.733 (18) | 1.267 |
| backlog-adp@blank-aged2-2 | 2 | +8.139 ms, 85,052 (0.851 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 16.805 (18) | 1.195 |
| backlog-adp@blank-aged2-3 | 2 | +6.743 ms, 78,182 (0.782 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 17.118 (18) | 0.882 |
| backlog-adp@blank-aged2-4 | 2 | +5.549 ms, 78,231 (0.782 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 17.034 (18) | 0.966 |
| backlog-adp@blank-aged2-5 | 2 | +5.203 ms, 85,111 (0.851 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 17.132 (18) | 0.868 |
| backlog-adp@blank-aged2-6 | 2 | +3.614 ms, 85,164 (0.852 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 17.274 (18) | 0.726 |
| backlog-adp@blank-aged2-7 | 2 | +2.578 ms, 85,100 (0.851 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 16.976 (18) | 1.024 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if1` | 16.116 (18) | 1.884 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if1` | 16.121 (18) | 1.879 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if1` | 15.951 (18) | 2.049 |
| backlog-adp@blank-aged1-3 | 1 | none | +16.303 ms, 77,835 (0.778 ms), read-back | `backlog-adp@blank-aged1-3.service.srp.last.if1` | 16.267 (18) | 1.733 |
| backlog-adp@blank-aged1-4 | 1 | +15.175 ms, 77,835 (0.778 ms), read-back | none | `backlog-adp@blank-aged1-4.service.srp.last.if1` | 16.920 (18) | 1.080 |
| backlog-adp@blank-aged1-5 | 1 | +13.880 ms, 77,835 (0.778 ms), read-back | none | `backlog-adp@blank-aged1-5.service.srp.last.if1` | 17.136 (18) | 0.864 |
| backlog-adp@blank-aged1-6 | 1 | +12.752 ms, 77,900 (0.779 ms), read-back | none | `backlog-adp@blank-aged1-6.service.srp.last.if1` | 17.250 (18) | 0.750 |
| backlog-adp@blank-aged1-7 | 1 | +11.411 ms, 77,900 (0.779 ms), read-back | none | `backlog-adp@blank-aged1-7.service.srp.last.if1` | 17.340 (18) | 0.660 |
| backlog-adp@program-aged2-0 | 2 | +10.168 ms, 84,075 (0.841 ms), issue | none | `backlog-adp@program-aged2-0.service.srp.last.if1` | 16.871 (18) | 1.129 |
| backlog-adp@program-aged2-1 | 2 | +8.823 ms, 84,076 (0.841 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if1` | 16.835 (18) | 1.165 |
| backlog-adp@program-aged2-2 | 2 | +7.965 ms, 84,314 (0.843 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if1` | 16.991 (18) | 1.009 |
| backlog-adp@program-aged2-3 | 2 | +7.029 ms, 84,249 (0.842 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if1` | 17.186 (18) | 0.814 |
| backlog-adp@program-aged2-4 | 2 | +5.784 ms, 84,246 (0.842 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if1` | 17.338 (18) | 0.662 |
| backlog-adp@program-aged2-5 | 2 | +4.195 ms, 84,246 (0.842 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if1` | 17.203 (18) | 0.797 |
| backlog-adp@program-aged2-6 | 2 | +3.676 ms, 84,275 (0.843 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if1` | 17.185 (18) | 0.815 |
| backlog-adp@program-aged2-7 | 2 | +3.539 ms, 84,275 (0.843 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if1` | 17.137 (18) | 0.863 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if1` | 16.116 (18) | 1.884 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if1` | 15.955 (18) | 2.045 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if1` | 16.174 (18) | 1.826 |
| backlog-adp@program-aged1-3 | 1 | +16.249 ms, 84,053 (0.841 ms), issue | none | `backlog-adp@program-aged1-3.service.srp.last.if1` | 17.406 (18) | 0.594 |
| backlog-adp@program-aged1-4 | 1 | +15.249 ms, 84,011 (0.840 ms), issue | none | `backlog-adp@program-aged1-4.service.srp.last.if1` | 17.003 (18) | 0.997 |
| backlog-adp@program-aged1-5 | 1 | +13.976 ms, 84,011 (0.840 ms), issue | none | `backlog-adp@program-aged1-5.service.srp.last.if1` | 17.031 (18) | 0.969 |
| backlog-adp@program-aged1-6 | 1 | +12.743 ms, 84,010 (0.840 ms), issue | none | `backlog-adp@program-aged1-6.service.srp.last.if1` | 17.181 (18) | 0.819 |
| backlog-adp@program-aged1-7 | 1 | +11.250 ms, 83,951 (0.840 ms), issue | none | `backlog-adp@program-aged1-7.service.srp.last.if1` | 16.917 (18) | 1.083 |
| backlog-adp@verify-aged2-0 | 2 | +10.202 ms, 78,733 (0.787 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 17.592 (18) | 0.408 |
| backlog-adp@verify-aged2-1 | 2 | +8.930 ms, 78,733 (0.787 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 17.489 (18) | 0.511 |
| backlog-adp@verify-aged2-2 | 2 | +8.122 ms, 78,999 (0.790 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 17.467 (18) | 0.533 |
| backlog-adp@verify-aged2-3 | 2 | +6.935 ms, 78,950 (0.789 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 17.477 (18) | 0.523 |
| backlog-adp@verify-aged2-4 | 2 | +5.693 ms, 79,064 (0.791 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 17.665 (18) | 0.335 |
| backlog-adp@verify-aged2-5 | 2 | +5.178 ms, 79,064 (0.791 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 17.540 (18) | 0.460 |
| backlog-adp@verify-aged2-6 | 2 | +3.586 ms, 79,027 (0.790 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 17.406 (18) | 0.594 |
| backlog-adp@verify-aged2-7 | 2 | +2.548 ms, 79,027 (0.790 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 17.539 (18) | 0.461 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if1` | 16.428 (18) | 1.572 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if1` | 16.555 (18) | 1.445 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if1` | 16.579 (18) | 1.421 |
| backlog-adp@verify-aged1-3 | 1 | +16.287 ms, 78,733 (0.787 ms), read-back | none | `backlog-adp@verify-aged1-3.service.srp.last.if1` | 17.391 (18) | 0.609 |
| backlog-adp@verify-aged1-4 | 1 | +15.154 ms, 78,668 (0.787 ms), read-back | none | `backlog-adp@verify-aged1-4.service.srp.last.if1` | 17.319 (18) | 0.681 |
| backlog-adp@verify-aged1-5 | 1 | +14.185 ms, 78,919 (0.789 ms), read-back | none | `backlog-adp@verify-aged1-5.service.srp.last.if1` | 17.251 (18) | 0.749 |
| backlog-adp@verify-aged1-6 | 1 | +12.618 ms, 78,733 (0.787 ms), read-back | none | `backlog-adp@verify-aged1-6.service.srp.last.if1` | 17.483 (18) | 0.517 |
| backlog-adp@verify-aged1-7 | 1 | +11.593 ms, 78,668 (0.787 ms), read-back | none | `backlog-adp@verify-aged1-7.service.srp.last.if1` | 17.765 (18) | 0.235 |

Least margin over the aged windows: 0.235 ms, `backlog-adp@verify-aged1-7.service.srp.last.if1` at 17.765 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22110.071 | 22,150 | 370 | 2 | 31.041 | yes | within |
| save-held | 4696.929 | 12,110 | 370 | - | 18.923 | no | within |
| save-starved | 12086.978 | 12,110 | 370 | - | 31.092 | yes | within |
| save | 4697.307 | 12,110 | 370 | - | 11.300 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1056 | 96,832 (0.968) | 95,296 (0.953) |
| save-held | 1527 | 126,746 (1.267) | 95,999 (0.960) |
| save-starved | 686 | 97,347 (0.973) | 95,781 (0.958) |
| acmp-notk | 1065 | 130,212 (1.302) | 95,803 (0.958) |
| backlog-adp@blank-0 | 337 | 100,446 (1.004) | 75,510 (0.755) |
| backlog-adp@blank-1 | 337 | 105,615 (1.056) | 75,654 (0.757) |
| backlog-adp@blank-2 | 338 | 106,514 (1.065) | 75,734 (0.757) |
| backlog-adp@blank-3 | 337 | 105,827 (1.058) | 75,733 (0.757) |
| backlog-adp@blank-4 | 337 | 98,650 (0.987) | 75,585 (0.756) |
| backlog-adp@blank-5 | 337 | 98,650 (0.987) | 75,585 (0.756) |
| backlog-adp@blank-6 | 337 | 99,270 (0.993) | 75,664 (0.757) |
| backlog-adp@blank-7 | 337 | 106,239 (1.062) | 75,733 (0.757) |
| backlog-adp@program-0 | 443 | 122,291 (1.223) | 81,633 (0.816) |
| backlog-adp@program-1 | 443 | 122,291 (1.223) | 81,692 (0.817) |
| backlog-adp@program-2 | 443 | 122,291 (1.223) | 81,846 (0.818) |
| backlog-adp@program-3 | 443 | 122,291 (1.223) | 81,702 (0.817) |
| backlog-adp@program-4 | 444 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-5 | 444 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-6 | 444 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-7 | 444 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@verify-0 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-1 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-2 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-3 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-4 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-5 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-6 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-7 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@blank-aged2-0 | 335 | 77,900 (0.779) | 75,557 (0.756) |
| backlog-adp@blank-aged2-1 | 335 | 77,835 (0.778) | 75,557 (0.756) |
| backlog-adp@blank-aged2-2 | 336 | 96,667 (0.967) | 75,773 (0.758) |
| backlog-adp@blank-aged2-3 | 336 | 99,270 (0.993) | 75,773 (0.758) |
| backlog-adp@blank-aged2-4 | 336 | 99,234 (0.992) | 75,773 (0.758) |
| backlog-adp@blank-aged2-5 | 336 | 99,853 (0.999) | 75,773 (0.758) |
| backlog-adp@blank-aged2-6 | 336 | 98,650 (0.987) | 75,829 (0.758) |
| backlog-adp@blank-aged2-7 | 336 | 99,270 (0.993) | 75,829 (0.758) |
| backlog-adp@blank-aged1-0 | 335 | 99,271 (0.993) | 75,665 (0.757) |
| backlog-adp@blank-aged1-1 | 335 | 99,271 (0.993) | 75,665 (0.757) |
| backlog-adp@blank-aged1-2 | 336 | 99,272 (0.993) | 75,666 (0.757) |
| backlog-adp@blank-aged1-3 | 335 | 77,835 (0.778) | 75,557 (0.756) |
| backlog-adp@blank-aged1-4 | 335 | 77,835 (0.778) | 75,557 (0.756) |
| backlog-adp@blank-aged1-5 | 335 | 77,835 (0.778) | 75,557 (0.756) |
| backlog-adp@blank-aged1-6 | 335 | 77,900 (0.779) | 75,557 (0.756) |
| backlog-adp@blank-aged1-7 | 335 | 77,900 (0.779) | 75,557 (0.756) |
| backlog-adp@program-aged2-0 | 441 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-aged2-1 | 441 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-aged2-2 | 442 | 122,291 (1.223) | 81,755 (0.818) |
| backlog-adp@program-aged2-3 | 442 | 122,291 (1.223) | 81,755 (0.818) |
| backlog-adp@program-aged2-4 | 442 | 122,291 (1.223) | 81,755 (0.818) |
| backlog-adp@program-aged2-5 | 442 | 122,291 (1.223) | 81,755 (0.818) |
| backlog-adp@program-aged2-6 | 442 | 122,291 (1.223) | 81,811 (0.818) |
| backlog-adp@program-aged2-7 | 442 | 122,291 (1.223) | 81,811 (0.818) |
| backlog-adp@program-aged1-0 | 441 | 122,291 (1.223) | 81,716 (0.817) |
| backlog-adp@program-aged1-1 | 441 | 122,291 (1.223) | 81,716 (0.817) |
| backlog-adp@program-aged1-2 | 442 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-aged1-3 | 441 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-aged1-4 | 441 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-aged1-5 | 441 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-aged1-6 | 441 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@program-aged1-7 | 441 | 122,291 (1.223) | 81,562 (0.816) |
| backlog-adp@verify-aged2-0 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-1 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-2 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-3 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-4 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-5 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-6 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged2-7 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged1-0 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged1-1 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged1-2 | 547 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged1-3 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged1-4 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged1-5 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged1-6 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| backlog-adp@verify-aged1-7 | 546 | 122,291 (1.223) | 95,651 (0.957) |
| adp-advertise | 577 | 50,112 (0.501) | 2,200 (0.022) |
| maap | 327 | 50,105 (0.501) | 2,200 (0.022) |
| acmp-noresp | 615 | 129,096 (1.291) | 95,651 (0.957) |
| save | 585 | 125,422 (1.254) | 95,409 (0.954) |
| srp | 280 | 50,105 (0.501) | 2,224 (0.022) |
| backlog | 266 | 50,112 (0.501) | 2,240 (0.022) |
| backlog-adp | 271 | 50,112 (0.501) | 2,224 (0.022) |
| backlog-adp-refill | 273 | 50,112 (0.501) | 2,303 (0.023) |
| backlog-owed | 305 | 50,112 (0.501) | 2,255 (0.023) |
| acmp-disc | 336 | 124,327 (1.243) | 81,562 (0.816) |
| adp-link | 79 | 50,112 (0.501) | 2,200 (0.022) |
| adp-gm | 79 | 50,112 (0.501) | 2,200 (0.022) |
| adp-discover | 79 | 50,112 (0.501) | 2,200 (0.022) |
| control | 79 | 50,112 (0.501) | 2,200 (0.022) |
| aecp-fanout | 92 | 50,112 (0.501) | 2,200 (0.022) |
| acmp-cmd | 67 | 50,112 (0.501) | 2,292 (0.023) |
| aecp | 88 | 50,112 (0.501) | 2,200 (0.022) |

Longest pass that carries a step: 130,212 CPU cycles (1.302 ms), acmp-notk; longest step: 95,999 (0.960 ms), save-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 464,555 | 4.646 | 20 | 200 | fits | 120,651 | 85 | 0.559 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 817,551 | 8.176 | 20 | 20 | fits | 95,136 | 39 | 0.737 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 1,055,941 | 10.559 | 20 | 24 | fits | 29,634 | 23 | 0.560 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 513,554 | 5.136 | 20 | 50 | fits | 108,611 | 56 | 0.641 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 1,452,657 | 14.527 | 18 | 18 | fits | 52,104 | 28 | 0.736 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 474,301 | 4.743 | 20 | 200 | fits | 124,326 | 91 | 0.584 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 839,061 | 8.391 | 20 | 20 | fits | 98,326 | 45 | 0.742 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 1,123,428 | 11.234 | 20 | 24 | fits | 39,249 | 35 | 0.594 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 526,835 | 5.268 | 20 | 50 | fits | 112,146 | 62 | 0.663 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,507,595 | 15.076 | 18 | 18 | fits | 55,096 | 34 | 0.745 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 14,179 | 0.142 | 20 | 20 | fits | 52,682 | 31 (14) | 0.779 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 18,982 | 0.190 | 20 | 20 | fits | 51,260 | 20 (14) | 0.884 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 496,893 | 4.969 | 20 | 20 | fits | 153,585 | 90 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 185,378 | 1.854 | 20 | 200 | fits | 118,725 | 140 | 0.521 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 637,012 | 6.370 | 20 | 200 | fits | 153,585 | 90 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 186,290 | 1.863 | 20 | 20 | fits | 118,725 | 140 | 0.521 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 879,245 | 8.792 | 20 | 20 | fits | 120,371 | 47 | 0.702 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 189,875 | 1.899 | 20 | 24 | fits | 118,725 | 140 | 0.521 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,540,160 | 15.402 | 20 | 24 | fits | 65,447 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 188,835 | 1.888 | 20 | 50 | fits | 118,725 | 140 | 0.521 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 640,688 | 6.407 | 20 | 50 | fits | 153,585 | 90 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 377,071 | 3.771 | 18 | 18 | fits | 188,691 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,666,091 | 16.661 | 18 | 18 | fits | 34,129 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 478,200 | 4.782 | 20 | 20 | fits | 154,039 | 84 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 128,339 | 1.283 | 20 | 200 | fits | 117,962 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 620,027 | 6.200 | 20 | 200 | fits | 154,039 | 84 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 129,251 | 1.293 | 20 | 20 | fits | 117,962 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 837,253 | 8.373 | 20 | 20 | fits | 85,619 | 37 | 0.646 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 132,836 | 1.328 | 20 | 24 | fits | 117,962 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,489,781 | 14.898 | 20 | 24 | fits | 65,482 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 131,796 | 1.318 | 20 | 50 | fits | 117,962 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 623,703 | 6.237 | 20 | 50 | fits | 154,039 | 84 | 0.672 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 320,071 | 3.201 | 18 | 18 | fits | 188,730 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,620,338 | 16.203 | 18 | 18 | fits | 34,320 | 16 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 430,899 | 4.309 | 20 | 20 | fits | 155,436 | 84 | 0.679 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 121,998 | 1.220 | 20 | 200 | fits | 117,963 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 573,755 | 5.738 | 20 | 200 | fits | 155,436 | 84 | 0.679 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 122,910 | 1.229 | 20 | 20 | fits | 117,963 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 894,548 | 8.945 | 20 | 20 | fits | 97,689 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 126,495 | 1.265 | 20 | 24 | fits | 117,963 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,488,083 | 14.881 | 20 | 24 | fits | 65,627 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 125,455 | 1.255 | 20 | 50 | fits | 117,963 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 577,431 | 5.774 | 20 | 50 | fits | 155,436 | 84 | 0.679 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 421,930 | 4.219 | 18 | 18 | fits | 182,674 | 105 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,734,105 | 17.341 | 18 | 18 | fits | 40,513 | 19 | 0.792 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 462,784 | 4.628 | 20 | 20 | fits | 139,659 | 80 | 0.679 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 115,618 | 1.156 | 20 | 200 | fits | 118,017 | 141 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 590,322 | 5.903 | 20 | 200 | fits | 139,659 | 80 | 0.679 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 116,530 | 1.165 | 20 | 20 | fits | 118,017 | 141 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 911,877 | 9.119 | 20 | 20 | fits | 98,277 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 120,115 | 1.201 | 20 | 24 | fits | 118,017 | 141 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,510,622 | 15.106 | 20 | 24 | fits | 65,815 | 32 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 119,075 | 1.191 | 20 | 50 | fits | 118,017 | 141 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 593,998 | 5.940 | 20 | 50 | fits | 139,659 | 80 | 0.679 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 308,921 | 3.089 | 18 | 18 | fits | 190,301 | 146 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,631,630 | 16.316 | 18 | 18 | fits | 41,301 | 20 | 0.789 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 565,719 | 5.657 | 20 | 20 | fits | 140,699 | 57 | 0.710 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 117,833 | 1.178 | 20 | 200 | fits | 117,635 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 696,240 | 6.962 | 20 | 200 | fits | 140,699 | 57 | 0.710 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 118,745 | 1.187 | 20 | 20 | fits | 117,635 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 881,783 | 8.818 | 20 | 20 | fits | 98,249 | 46 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 122,330 | 1.223 | 20 | 24 | fits | 117,635 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,471,236 | 14.712 | 20 | 24 | fits | 52,975 | 27 | 0.742 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 121,290 | 1.213 | 20 | 50 | fits | 117,635 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 559,217 | 5.592 | 20 | 50 | fits | 104,640 | 64 | 0.729 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 309,420 | 3.094 | 18 | 18 | fits | 188,585 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,638,600 | 16.386 | 18 | 18 | fits | 34,101 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 575,545 | 5.755 | 20 | 20 | fits | 107,385 | 49 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 128,245 | 1.282 | 20 | 200 | fits | 117,635 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 672,521 | 6.725 | 20 | 200 | fits | 107,385 | 49 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 129,157 | 1.292 | 20 | 20 | fits | 117,635 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 892,156 | 8.922 | 20 | 20 | fits | 98,313 | 40 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 132,742 | 1.327 | 20 | 24 | fits | 117,635 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,476,411 | 14.764 | 20 | 24 | fits | 65,701 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 131,702 | 1.317 | 20 | 50 | fits | 117,635 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 568,812 | 5.688 | 20 | 50 | fits | 143,030 | 98 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 319,832 | 3.198 | 18 | 18 | fits | 188,585 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,648,738 | 16.487 | 18 | 18 | fits | 34,101 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 537,865 | 5.379 | 20 | 20 | fits | 145,225 | 64 | 0.716 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 121,904 | 1.219 | 20 | 200 | fits | 117,636 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 669,142 | 6.691 | 20 | 200 | fits | 145,225 | 64 | 0.716 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 122,816 | 1.228 | 20 | 20 | fits | 117,636 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 887,622 | 8.876 | 20 | 20 | fits | 97,876 | 40 | 0.740 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 126,401 | 1.264 | 20 | 24 | fits | 117,636 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,481,366 | 14.814 | 20 | 24 | fits | 65,096 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 125,361 | 1.254 | 20 | 50 | fits | 117,636 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 527,593 | 5.276 | 20 | 50 | fits | 163,148 | 99 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 364,380 | 3.644 | 18 | 18 | fits | 125,263 | 64 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,618,768 | 16.188 | 18 | 18 | fits | 46,171 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 556,135 | 5.561 | 20 | 20 | fits | 141,717 | 58 | 0.713 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 115,469 | 1.155 | 20 | 200 | fits | 117,635 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 687,130 | 6.871 | 20 | 200 | fits | 141,717 | 58 | 0.713 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 116,381 | 1.164 | 20 | 20 | fits | 117,635 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 914,976 | 9.150 | 20 | 20 | fits | 96,812 | 39 | 0.737 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 119,966 | 1.200 | 20 | 24 | fits | 117,635 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,487,688 | 14.877 | 20 | 24 | fits | 65,271 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 118,926 | 1.189 | 20 | 50 | fits | 117,635 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 549,089 | 5.491 | 20 | 50 | fits | 147,882 | 105 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 251,432 | 2.514 | 18 | 18 | fits | 132,961 | 105 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,629,346 | 16.293 | 18 | 18 | fits | 50,259 | 25 | 0.720 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 465,807 | 4.658 | 20 | 20 | fits | 153,623 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 122,035 | 1.220 | 20 | 200 | fits | 118,066 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 607,576 | 6.076 | 20 | 200 | fits | 153,623 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 122,947 | 1.229 | 20 | 20 | fits | 118,066 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 815,616 | 8.156 | 20 | 20 | fits | 86,475 | 38 | 0.651 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 126,532 | 1.265 | 20 | 24 | fits | 118,066 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,479,883 | 14.799 | 20 | 24 | fits | 65,452 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 125,492 | 1.255 | 20 | 50 | fits | 118,066 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 611,252 | 6.113 | 20 | 50 | fits | 153,623 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 312,472 | 3.125 | 18 | 18 | fits | 187,435 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,605,924 | 16.059 | 18 | 18 | fits | 34,080 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 469,914 | 4.699 | 20 | 20 | fits | 119,068 | 75 | 0.630 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 126,106 | 1.261 | 20 | 200 | fits | 118,067 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 577,128 | 5.771 | 20 | 200 | fits | 119,068 | 75 | 0.630 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 127,018 | 1.270 | 20 | 20 | fits | 118,067 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 851,602 | 8.516 | 20 | 20 | fits | 97,574 | 40 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 130,603 | 1.306 | 20 | 24 | fits | 118,067 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,453,216 | 14.532 | 20 | 24 | fits | 65,452 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 129,563 | 1.296 | 20 | 50 | fits | 118,067 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 580,804 | 5.808 | 20 | 50 | fits | 119,068 | 75 | 0.630 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 316,579 | 3.166 | 18 | 18 | fits | 187,471 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,625,660 | 16.257 | 18 | 18 | fits | 34,080 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 527,522 | 5.275 | 20 | 20 | fits | 140,598 | 58 | 0.708 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 113,238 | 1.132 | 20 | 200 | fits | 118,067 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 657,961 | 6.580 | 20 | 200 | fits | 140,598 | 58 | 0.708 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 114,150 | 1.141 | 20 | 20 | fits | 118,067 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 885,731 | 8.857 | 20 | 20 | fits | 98,293 | 39 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 117,735 | 1.177 | 20 | 24 | fits | 118,067 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,460,236 | 14.602 | 20 | 24 | fits | 59,205 | 32 | 0.758 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 116,695 | 1.167 | 20 | 50 | fits | 118,067 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 521,039 | 5.210 | 20 | 50 | fits | 103,298 | 65 | 0.711 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 303,848 | 3.038 | 18 | 18 | fits | 187,608 | 141 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,752,168 | 17.522 | 18 | 18 | fits | 34,081 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 539,690 | 5.397 | 20 | 20 | fits | 140,202 | 57 | 0.704 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 117,362 | 1.174 | 20 | 200 | fits | 118,121 | 141 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 670,108 | 6.701 | 20 | 200 | fits | 140,202 | 57 | 0.704 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 118,274 | 1.183 | 20 | 20 | fits | 118,121 | 141 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 889,040 | 8.890 | 20 | 20 | fits | 97,980 | 39 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 121,859 | 1.219 | 20 | 24 | fits | 118,121 | 141 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,466,592 | 14.666 | 20 | 24 | fits | 65,609 | 32 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 120,819 | 1.208 | 20 | 50 | fits | 118,121 | 141 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 523,446 | 5.234 | 20 | 50 | fits | 162,902 | 99 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 360,479 | 3.605 | 18 | 18 | fits | 124,344 | 65 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,639,422 | 16.394 | 18 | 18 | fits | 34,181 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 464,236 | 4.642 | 20 | 20 | fits | 139,466 | 80 | 0.679 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 120,615 | 1.206 | 20 | 200 | fits | 118,196 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 591,848 | 5.918 | 20 | 200 | fits | 139,466 | 80 | 0.679 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 121,527 | 1.215 | 20 | 20 | fits | 118,196 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 837,136 | 8.371 | 20 | 20 | fits | 120,541 | 47 | 0.704 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 125,112 | 1.251 | 20 | 24 | fits | 118,196 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,487,408 | 14.874 | 20 | 24 | fits | 65,627 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 124,072 | 1.241 | 20 | 50 | fits | 118,196 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 595,524 | 5.955 | 20 | 50 | fits | 139,466 | 80 | 0.679 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 310,856 | 3.109 | 18 | 18 | fits | 187,239 | 140 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,613,449 | 16.134 | 18 | 18 | fits | 34,080 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 473,090 | 4.731 | 20 | 20 | fits | 154,043 | 84 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 124,684 | 1.247 | 20 | 200 | fits | 118,195 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 614,921 | 6.149 | 20 | 200 | fits | 154,043 | 84 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 125,596 | 1.256 | 20 | 20 | fits | 118,195 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 934,931 | 9.349 | 20 | 20 | fits | 98,089 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 129,181 | 1.292 | 20 | 24 | fits | 118,195 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,528,466 | 15.285 | 20 | 24 | fits | 65,627 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 128,141 | 1.281 | 20 | 50 | fits | 118,195 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 618,597 | 6.186 | 20 | 50 | fits | 154,043 | 84 | 0.672 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 314,961 | 3.150 | 18 | 18 | fits | 187,275 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,613,400 | 16.134 | 18 | 18 | fits | 34,617 | 16 | 0.769 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 549,278 | 5.493 | 20 | 20 | fits | 139,691 | 57 | 0.705 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 128,718 | 1.287 | 20 | 200 | fits | 118,251 | 141 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 679,557 | 6.796 | 20 | 200 | fits | 139,691 | 57 | 0.705 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 129,630 | 1.296 | 20 | 20 | fits | 118,251 | 141 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 898,778 | 8.988 | 20 | 20 | fits | 98,182 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 133,215 | 1.332 | 20 | 24 | fits | 118,251 | 141 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,490,601 | 14.906 | 20 | 24 | fits | 65,344 | 32 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 132,175 | 1.322 | 20 | 50 | fits | 118,251 | 141 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 533,685 | 5.337 | 20 | 50 | fits | 102,969 | 65 | 0.709 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 320,440 | 3.204 | 18 | 18 | fits | 188,720 | 146 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,629,081 | 16.291 | 18 | 18 | fits | 46,551 | 19 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 573,826 | 5.738 | 20 | 20 | fits | 107,222 | 49 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 124,978 | 1.250 | 20 | 200 | fits | 118,124 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 670,684 | 6.707 | 20 | 200 | fits | 107,222 | 49 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 125,890 | 1.259 | 20 | 20 | fits | 118,124 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 890,079 | 8.901 | 20 | 20 | fits | 98,152 | 40 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 129,475 | 1.295 | 20 | 24 | fits | 118,124 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,452,732 | 14.527 | 20 | 24 | fits | 65,126 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 128,435 | 1.284 | 20 | 50 | fits | 118,124 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 567,138 | 5.671 | 20 | 50 | fits | 144,295 | 98 | 0.620 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 259,876 | 2.599 | 18 | 18 | fits | 131,896 | 105 | 0.699 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,636,372 | 16.364 | 18 | 18 | fits | 46,171 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 503,891 | 5.039 | 20 | 20 | fits | 143,096 | 61 | 0.697 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 165,650 | 1.657 | 20 | 200 | fits | 118,509 | 142 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 634,866 | 6.349 | 20 | 200 | fits | 143,096 | 61 | 0.697 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 166,562 | 1.666 | 20 | 20 | fits | 118,509 | 142 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 884,725 | 8.847 | 20 | 20 | fits | 120,076 | 46 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 51,638 | 0.516 | 20 | 24 | fits | 52,806 | 65 | 0.556 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,474,884 | 14.749 | 20 | 24 | fits | 69,249 | 38 | 0.722 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 50,598 | 0.506 | 20 | 50 | fits | 52,806 | 65 | 0.556 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 495,446 | 4.954 | 20 | 50 | fits | 136,309 | 77 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 359,072 | 3.591 | 18 | 18 | fits | 190,420 | 146 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,637,105 | 16.371 | 18 | 18 | fits | 34,348 | 16 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 479,363 | 4.794 | 20 | 20 | fits | 152,006 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 123,760 | 1.238 | 20 | 200 | fits | 117,994 | 141 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 620,347 | 6.203 | 20 | 200 | fits | 152,006 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 124,672 | 1.247 | 20 | 20 | fits | 117,994 | 141 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 931,532 | 9.315 | 20 | 20 | fits | 97,818 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 128,257 | 1.283 | 20 | 24 | fits | 117,994 | 141 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,564,179 | 15.642 | 20 | 24 | fits | 99,766 | 46 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 127,217 | 1.272 | 20 | 50 | fits | 117,994 | 141 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 624,023 | 6.240 | 20 | 50 | fits | 152,006 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 316,709 | 3.167 | 18 | 18 | fits | 189,947 | 146 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,644,784 | 16.448 | 18 | 18 | fits | 34,501 | 16 | 0.767 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 471,355 | 4.714 | 20 | 20 | fits | 153,675 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 126,407 | 1.264 | 20 | 200 | fits | 117,960 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 613,176 | 6.132 | 20 | 200 | fits | 153,675 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 127,319 | 1.273 | 20 | 20 | fits | 117,960 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 868,870 | 8.689 | 20 | 20 | fits | 98,573 | 46 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 130,904 | 1.309 | 20 | 24 | fits | 117,960 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,455,872 | 14.559 | 20 | 24 | fits | 51,757 | 27 | 0.737 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 129,864 | 1.299 | 20 | 50 | fits | 117,960 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 616,852 | 6.169 | 20 | 50 | fits | 153,675 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 318,020 | 3.180 | 18 | 18 | fits | 188,611 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,670,165 | 16.702 | 18 | 18 | fits | 40,506 | 19 | 0.792 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 464,886 | 4.649 | 20 | 20 | fits | 119,055 | 74 | 0.631 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 119,974 | 1.200 | 20 | 200 | fits | 117,961 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 572,087 | 5.721 | 20 | 200 | fits | 119,055 | 74 | 0.631 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 120,886 | 1.209 | 20 | 20 | fits | 117,961 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 862,159 | 8.622 | 20 | 20 | fits | 98,195 | 40 | 0.742 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 124,471 | 1.245 | 20 | 24 | fits | 117,961 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,499,682 | 14.997 | 20 | 24 | fits | 99,748 | 45 | 0.755 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 123,431 | 1.234 | 20 | 50 | fits | 117,961 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 575,763 | 5.758 | 20 | 50 | fits | 119,055 | 74 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 311,551 | 3.116 | 18 | 18 | fits | 188,575 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,667,323 | 16.673 | 18 | 18 | fits | 34,101 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 505,815 | 5.058 | 20 | 20 | fits | 141,191 | 64 | 0.694 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 113,539 | 1.135 | 20 | 200 | fits | 117,960 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 634,960 | 6.350 | 20 | 200 | fits | 141,191 | 64 | 0.694 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 114,451 | 1.145 | 20 | 20 | fits | 117,960 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 854,328 | 8.543 | 20 | 20 | fits | 98,189 | 40 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 118,036 | 1.180 | 20 | 24 | fits | 117,960 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,449,480 | 14.495 | 20 | 24 | fits | 58,997 | 32 | 0.758 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 116,996 | 1.170 | 20 | 50 | fits | 117,960 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 497,445 | 4.974 | 20 | 50 | fits | 82,397 | 61 | 0.646 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 305,152 | 3.052 | 18 | 18 | fits | 188,611 | 140 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,658,258 | 16.583 | 18 | 18 | fits | 34,108 | 15 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 541,225 | 5.412 | 20 | 20 | fits | 142,107 | 58 | 0.713 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 124,043 | 1.240 | 20 | 200 | fits | 117,960 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 672,178 | 6.722 | 20 | 200 | fits | 142,107 | 58 | 0.713 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 124,955 | 1.250 | 20 | 20 | fits | 117,960 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 899,766 | 8.998 | 20 | 20 | fits | 96,760 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 128,540 | 1.285 | 20 | 24 | fits | 117,960 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,472,565 | 14.726 | 20 | 24 | fits | 65,256 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 127,500 | 1.275 | 20 | 50 | fits | 117,960 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 533,747 | 5.337 | 20 | 50 | fits | 162,703 | 105 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 285,410 | 2.854 | 18 | 18 | fits | 158,365 | 136 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,685,483 | 16.855 | 18 | 18 | fits | 34,214 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 571,527 | 5.715 | 20 | 20 | fits | 141,080 | 58 | 0.708 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 117,610 | 1.176 | 20 | 200 | fits | 117,961 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 701,976 | 7.020 | 20 | 200 | fits | 141,080 | 58 | 0.708 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 118,522 | 1.185 | 20 | 20 | fits | 117,961 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 929,295 | 9.293 | 20 | 20 | fits | 97,877 | 39 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 122,107 | 1.221 | 20 | 24 | fits | 117,961 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,518,771 | 15.188 | 20 | 24 | fits | 69,152 | 38 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 121,067 | 1.211 | 20 | 50 | fits | 117,961 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 564,572 | 5.646 | 20 | 50 | fits | 144,492 | 99 | 0.620 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 253,749 | 2.537 | 18 | 18 | fits | 133,137 | 106 | 0.699 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,610,716 | 16.107 | 18 | 18 | fits | 46,543 | 19 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 546,053 | 5.461 | 20 | 20 | fits | 139,950 | 57 | 0.705 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 83,783 | 0.838 | 20 | 200 | fits | 90,568 | 105 | 0.600 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 676,531 | 6.765 | 20 | 200 | fits | 139,950 | 57 | 0.705 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 84,695 | 0.847 | 20 | 20 | fits | 90,568 | 105 | 0.600 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 895,949 | 8.959 | 20 | 20 | fits | 98,266 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 88,280 | 0.883 | 20 | 24 | fits | 90,568 | 105 | 0.600 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,453,126 | 14.531 | 20 | 24 | fits | 65,514 | 32 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 87,240 | 0.872 | 20 | 50 | fits | 90,568 | 105 | 0.600 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 530,367 | 5.304 | 20 | 50 | fits | 145,451 | 99 | 0.627 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 384,851 | 3.849 | 18 | 18 | fits | 182,437 | 105 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,662,270 | 16.623 | 18 | 18 | fits | 34,348 | 16 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 479,386 | 4.794 | 20 | 20 | fits | 152,020 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 124,979 | 1.250 | 20 | 200 | fits | 117,370 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 620,384 | 6.204 | 20 | 200 | fits | 152,020 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 125,891 | 1.259 | 20 | 20 | fits | 117,370 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 862,321 | 8.623 | 20 | 20 | fits | 120,356 | 46 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 129,476 | 1.295 | 20 | 24 | fits | 117,370 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 1,529,390 | 15.294 | 20 | 24 | fits | 65,334 | 32 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 128,436 | 1.284 | 20 | 50 | fits | 117,370 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 624,060 | 6.241 | 20 | 50 | fits | 152,020 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 316,814 | 3.168 | 18 | 18 | fits | 188,833 | 141 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 1,714,608 | 17.146 | 18 | 18 | fits | 36,750 | 15 | 0.837 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 464,812 | 4.648 | 20 | 20 | fits | 153,533 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 110,373 | 1.104 | 20 | 200 | fits | 117,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 606,400 | 6.064 | 20 | 200 | fits | 153,533 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 111,285 | 1.113 | 20 | 20 | fits | 117,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 834,585 | 8.346 | 20 | 20 | fits | 106,503 | 42 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 114,870 | 1.149 | 20 | 24 | fits | 117,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 1,581,632 | 15.816 | 20 | 24 | fits | 65,789 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 113,830 | 1.138 | 20 | 50 | fits | 117,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 610,076 | 6.101 | 20 | 50 | fits | 153,533 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 302,957 | 3.030 | 18 | 18 | fits | 189,582 | 146 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 1,673,302 | 16.733 | 18 | 18 | fits | 46,452 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 466,813 | 4.668 | 20 | 20 | fits | 153,419 | 83 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 114,166 | 1.142 | 20 | 200 | fits | 117,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 608,378 | 6.084 | 20 | 200 | fits | 153,419 | 83 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 115,078 | 1.151 | 20 | 20 | fits | 117,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 995,105 | 9.951 | 20 | 20 | fits | 100,740 | 45 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 118,663 | 1.187 | 20 | 24 | fits | 117,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 1,588,806 | 15.888 | 20 | 24 | fits | 65,642 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 117,623 | 1.176 | 20 | 50 | fits | 117,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 612,054 | 6.121 | 20 | 50 | fits | 153,419 | 83 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 313,346 | 3.133 | 18 | 18 | fits | 187,582 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 1,680,476 | 16.805 | 18 | 18 | fits | 46,452 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 471,434 | 4.714 | 20 | 20 | fits | 118,999 | 74 | 0.630 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 126,616 | 1.266 | 20 | 200 | fits | 117,098 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 578,579 | 5.786 | 20 | 200 | fits | 118,999 | 74 | 0.630 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 127,528 | 1.275 | 20 | 20 | fits | 117,098 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 931,151 | 9.312 | 20 | 20 | fits | 98,588 | 46 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 131,113 | 1.311 | 20 | 24 | fits | 117,098 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 1,532,846 | 15.328 | 20 | 24 | fits | 65,452 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 130,073 | 1.301 | 20 | 50 | fits | 117,098 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 582,255 | 5.823 | 20 | 50 | fits | 118,999 | 74 | 0.630 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 318,099 | 3.181 | 18 | 18 | fits | 188,481 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 1,711,799 | 17.118 | 18 | 18 | fits | 46,311 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 637,156 | 6.372 | 20 | 20 | fits | 105,641 | 49 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 110,936 | 1.109 | 20 | 200 | fits | 117,051 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 733,465 | 7.335 | 20 | 200 | fits | 105,641 | 49 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 111,848 | 1.118 | 20 | 20 | fits | 117,051 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 953,555 | 9.536 | 20 | 20 | fits | 98,313 | 40 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 115,433 | 1.154 | 20 | 24 | fits | 117,051 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 1,519,019 | 15.190 | 20 | 24 | fits | 59,159 | 32 | 0.739 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 114,393 | 1.144 | 20 | 50 | fits | 117,051 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 553,269 | 5.533 | 20 | 50 | fits | 104,640 | 64 | 0.729 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 303,390 | 3.034 | 18 | 18 | fits | 189,452 | 145 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 1,703,362 | 17.034 | 18 | 18 | fits | 46,344 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 612,791 | 6.128 | 20 | 20 | fits | 143,466 | 63 | 0.712 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 114,335 | 1.143 | 20 | 200 | fits | 117,051 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 743,543 | 7.435 | 20 | 200 | fits | 143,466 | 63 | 0.712 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 115,247 | 1.152 | 20 | 20 | fits | 117,051 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 962,794 | 9.628 | 20 | 20 | fits | 98,171 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 118,832 | 1.188 | 20 | 24 | fits | 117,051 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 1,539,963 | 15.400 | 20 | 24 | fits | 65,486 | 32 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 117,792 | 1.178 | 20 | 50 | fits | 117,051 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 518,642 | 5.186 | 20 | 50 | fits | 102,929 | 64 | 0.711 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 305,818 | 3.058 | 18 | 18 | fits | 188,481 | 140 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 1,713,232 | 17.132 | 18 | 18 | fits | 34,341 | 16 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 617,511 | 6.175 | 20 | 20 | fits | 141,986 | 57 | 0.715 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 117,288 | 1.173 | 20 | 200 | fits | 117,051 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 748,766 | 7.488 | 20 | 200 | fits | 141,986 | 57 | 0.715 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 118,200 | 1.182 | 20 | 20 | fits | 117,051 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 967,572 | 9.676 | 20 | 20 | fits | 97,957 | 39 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 121,785 | 1.218 | 20 | 24 | fits | 117,051 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 1,543,100 | 15.431 | 20 | 24 | fits | 65,295 | 32 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 120,745 | 1.207 | 20 | 50 | fits | 117,051 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 610,456 | 6.105 | 20 | 50 | fits | 165,531 | 104 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 359,696 | 3.597 | 18 | 18 | fits | 125,195 | 64 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 1,727,374 | 17.274 | 18 | 18 | fits | 33,961 | 15 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 657,791 | 6.578 | 20 | 20 | fits | 140,887 | 57 | 0.709 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 120,241 | 1.202 | 20 | 200 | fits | 117,051 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 788,314 | 7.883 | 20 | 200 | fits | 140,887 | 57 | 0.709 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 121,153 | 1.212 | 20 | 20 | fits | 117,051 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 1,007,235 | 10.072 | 20 | 20 | fits | 97,980 | 39 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 124,738 | 1.247 | 20 | 24 | fits | 117,051 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 1,606,202 | 16.062 | 20 | 24 | fits | 65,598 | 31 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 123,698 | 1.237 | 20 | 50 | fits | 117,051 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 651,103 | 6.511 | 20 | 50 | fits | 144,456 | 98 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 256,100 | 2.561 | 18 | 18 | fits | 132,857 | 105 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 1,697,592 | 16.976 | 18 | 18 | fits | 46,312 | 18 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 467,626 | 4.676 | 20 | 20 | fits | 153,533 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 114,257 | 1.143 | 20 | 200 | fits | 117,323 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 609,214 | 6.092 | 20 | 200 | fits | 153,533 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 115,169 | 1.152 | 20 | 20 | fits | 117,323 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 851,208 | 8.512 | 20 | 20 | fits | 120,356 | 46 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 118,754 | 1.188 | 20 | 24 | fits | 117,323 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if1` | 1,461,571 | 14.616 | 20 | 24 | fits | 65,506 | 32 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 117,714 | 1.177 | 20 | 50 | fits | 117,323 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 612,890 | 6.129 | 20 | 50 | fits | 153,533 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 305,857 | 3.059 | 18 | 18 | fits | 188,598 | 141 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if1` | 1,611,589 | 16.116 | 18 | 18 | fits | 46,290 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 470,584 | 4.706 | 20 | 20 | fits | 153,349 | 83 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 118,050 | 1.181 | 20 | 200 | fits | 117,276 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 612,079 | 6.121 | 20 | 200 | fits | 153,349 | 83 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 118,962 | 1.190 | 20 | 20 | fits | 117,276 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 840,158 | 8.402 | 20 | 20 | fits | 106,514 | 42 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 122,547 | 1.225 | 20 | 24 | fits | 117,276 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if1` | 1,474,120 | 14.741 | 20 | 24 | fits | 65,614 | 31 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 121,507 | 1.215 | 20 | 50 | fits | 117,276 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 615,755 | 6.158 | 20 | 50 | fits | 153,349 | 83 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 317,117 | 3.171 | 18 | 18 | fits | 187,420 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if1` | 1,612,080 | 16.121 | 18 | 18 | fits | 46,290 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 456,999 | 4.570 | 20 | 20 | fits | 153,689 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 110,983 | 1.110 | 20 | 200 | fits | 117,098 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 598,834 | 5.988 | 20 | 200 | fits | 153,689 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 111,895 | 1.119 | 20 | 20 | fits | 117,098 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 899,918 | 8.999 | 20 | 20 | fits | 97,850 | 40 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 115,480 | 1.155 | 20 | 24 | fits | 117,098 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if1` | 1,503,404 | 15.034 | 20 | 24 | fits | 65,642 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 114,440 | 1.144 | 20 | 50 | fits | 117,098 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 602,510 | 6.025 | 20 | 50 | fits | 153,689 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 303,582 | 3.036 | 18 | 18 | fits | 189,597 | 145 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if1` | 1,595,074 | 15.951 | 18 | 18 | fits | 46,452 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 459,843 | 4.598 | 20 | 20 | fits | 139,602 | 80 | 0.680 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 114,880 | 1.149 | 20 | 200 | fits | 117,098 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 587,591 | 5.876 | 20 | 200 | fits | 139,602 | 80 | 0.680 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 115,792 | 1.158 | 20 | 20 | fits | 117,098 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 902,727 | 9.027 | 20 | 20 | fits | 98,467 | 40 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 119,377 | 1.194 | 20 | 24 | fits | 117,098 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if1` | 1,506,056 | 15.061 | 20 | 24 | fits | 65,642 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 118,337 | 1.183 | 20 | 50 | fits | 117,098 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 591,267 | 5.913 | 20 | 50 | fits | 139,602 | 80 | 0.680 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 306,508 | 3.065 | 18 | 18 | fits | 188,626 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if1` | 1,626,653 | 16.267 | 18 | 18 | fits | 41,184 | 19 | 0.796 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 568,635 | 5.686 | 20 | 20 | fits | 140,874 | 58 | 0.709 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 117,833 | 1.178 | 20 | 200 | fits | 117,098 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 699,143 | 6.991 | 20 | 200 | fits | 140,874 | 58 | 0.709 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 118,745 | 1.187 | 20 | 20 | fits | 117,098 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 918,894 | 9.189 | 20 | 20 | fits | 98,395 | 40 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 122,330 | 1.223 | 20 | 24 | fits | 117,098 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if1` | 1,516,336 | 15.163 | 20 | 24 | fits | 60,172 | 32 | 0.762 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 121,290 | 1.213 | 20 | 50 | fits | 117,098 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 561,945 | 5.619 | 20 | 50 | fits | 107,327 | 71 | 0.721 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 309,461 | 3.095 | 18 | 18 | fits | 188,626 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if1` | 1,692,049 | 16.920 | 18 | 18 | fits | 51,731 | 25 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 571,193 | 5.712 | 20 | 20 | fits | 141,323 | 58 | 0.709 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 120,786 | 1.208 | 20 | 200 | fits | 117,098 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 701,840 | 7.018 | 20 | 200 | fits | 141,323 | 58 | 0.709 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 121,698 | 1.217 | 20 | 20 | fits | 117,098 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 929,841 | 9.298 | 20 | 20 | fits | 96,923 | 39 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 125,283 | 1.253 | 20 | 24 | fits | 117,098 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if1` | 1,595,788 | 15.958 | 20 | 24 | fits | 65,571 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 124,243 | 1.242 | 20 | 50 | fits | 117,098 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 564,193 | 5.642 | 20 | 50 | fits | 143,074 | 99 | 0.616 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 312,414 | 3.124 | 18 | 18 | fits | 188,626 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if1` | 1,713,601 | 17.136 | 18 | 18 | fits | 34,320 | 16 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 538,574 | 5.386 | 20 | 20 | fits | 142,033 | 58 | 0.713 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 123,739 | 1.237 | 20 | 200 | fits | 117,098 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 669,609 | 6.696 | 20 | 200 | fits | 142,033 | 58 | 0.713 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 124,651 | 1.247 | 20 | 20 | fits | 117,098 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 897,168 | 8.972 | 20 | 20 | fits | 98,091 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 128,236 | 1.282 | 20 | 24 | fits | 117,098 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if1` | 1,552,185 | 15.522 | 20 | 24 | fits | 65,503 | 32 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 127,196 | 1.272 | 20 | 50 | fits | 117,098 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 531,252 | 5.313 | 20 | 50 | fits | 163,098 | 99 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 368,089 | 3.681 | 18 | 18 | fits | 127,096 | 71 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if1` | 1,725,011 | 17.250 | 18 | 18 | fits | 34,180 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 563,355 | 5.634 | 20 | 20 | fits | 139,939 | 57 | 0.705 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 126,687 | 1.267 | 20 | 200 | fits | 117,185 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 693,822 | 6.938 | 20 | 200 | fits | 139,939 | 57 | 0.705 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 127,599 | 1.276 | 20 | 20 | fits | 117,185 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 913,076 | 9.131 | 20 | 20 | fits | 98,266 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 131,184 | 1.312 | 20 | 24 | fits | 117,185 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if1` | 1,548,812 | 15.488 | 20 | 24 | fits | 65,491 | 32 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 130,144 | 1.301 | 20 | 50 | fits | 117,185 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 547,669 | 5.477 | 20 | 50 | fits | 145,480 | 99 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 402,124 | 4.021 | 18 | 18 | fits | 182,833 | 105 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if1` | 1,733,974 | 17.340 | 18 | 18 | fits | 36,694 | 15 | 0.835 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 461,103 | 4.611 | 20 | 20 | fits | 157,365 | 90 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 111,823 | 1.118 | 20 | 200 | fits | 118,164 | 134 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 602,190 | 6.022 | 20 | 200 | fits | 157,365 | 90 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 112,735 | 1.127 | 20 | 20 | fits | 118,164 | 134 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 844,681 | 8.447 | 20 | 20 | fits | 120,570 | 47 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 116,320 | 1.163 | 20 | 24 | fits | 118,164 | 134 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 1,556,384 | 15.564 | 20 | 24 | fits | 65,268 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 115,280 | 1.153 | 20 | 50 | fits | 118,164 | 134 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 605,866 | 6.059 | 20 | 50 | fits | 157,365 | 90 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 303,150 | 3.031 | 18 | 18 | fits | 188,325 | 145 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if1` | 1,687,078 | 16.871 | 18 | 18 | fits | 38,890 | 22 | 0.775 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 425,396 | 4.254 | 20 | 20 | fits | 153,519 | 90 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 115,222 | 1.152 | 20 | 200 | fits | 117,607 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 565,449 | 5.654 | 20 | 200 | fits | 153,519 | 90 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 116,134 | 1.161 | 20 | 20 | fits | 117,607 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 807,682 | 8.077 | 20 | 20 | fits | 120,371 | 47 | 0.702 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 119,719 | 1.197 | 20 | 24 | fits | 117,607 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 1,553,797 | 15.538 | 20 | 24 | fits | 65,447 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 118,679 | 1.187 | 20 | 50 | fits | 117,607 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 569,125 | 5.691 | 20 | 50 | fits | 153,519 | 90 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 305,578 | 3.056 | 18 | 18 | fits | 187,354 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if1` | 1,683,481 | 16.835 | 18 | 18 | fits | 50,229 | 25 | 0.720 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 426,033 | 4.260 | 20 | 20 | fits | 155,370 | 84 | 0.679 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 118,175 | 1.182 | 20 | 200 | fits | 117,607 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 568,823 | 5.688 | 20 | 200 | fits | 155,370 | 84 | 0.679 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 119,087 | 1.191 | 20 | 20 | fits | 117,607 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 973,477 | 9.735 | 20 | 20 | fits | 97,236 | 39 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 122,672 | 1.227 | 20 | 24 | fits | 117,607 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 1,572,071 | 15.721 | 20 | 24 | fits | 70,427 | 38 | 0.725 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 121,632 | 1.216 | 20 | 50 | fits | 117,607 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 572,499 | 5.725 | 20 | 50 | fits | 155,370 | 84 | 0.679 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 417,064 | 4.171 | 18 | 18 | fits | 181,644 | 105 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if1` | 1,699,113 | 16.991 | 18 | 18 | fits | 34,354 | 16 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 467,128 | 4.671 | 20 | 20 | fits | 139,593 | 80 | 0.679 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 121,215 | 1.212 | 20 | 200 | fits | 117,694 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 594,600 | 5.946 | 20 | 200 | fits | 139,593 | 80 | 0.679 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 122,127 | 1.221 | 20 | 20 | fits | 117,694 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 1,000,259 | 10.003 | 20 | 20 | fits | 98,414 | 39 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 125,712 | 1.257 | 20 | 24 | fits | 117,694 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 1,584,646 | 15.846 | 20 | 24 | fits | 52,158 | 28 | 0.738 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 124,672 | 1.247 | 20 | 50 | fits | 117,694 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 598,276 | 5.983 | 20 | 50 | fits | 139,593 | 80 | 0.679 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 313,265 | 3.133 | 18 | 18 | fits | 189,048 | 146 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if1` | 1,718,555 | 17.186 | 18 | 18 | fits | 46,551 | 19 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 666,649 | 6.666 | 20 | 20 | fits | 139,796 | 57 | 0.705 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 127,189 | 1.272 | 20 | 200 | fits | 117,864 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 797,142 | 7.971 | 20 | 200 | fits | 139,796 | 57 | 0.705 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 128,101 | 1.281 | 20 | 20 | fits | 117,864 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 1,016,481 | 10.165 | 20 | 20 | fits | 98,171 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 131,686 | 1.317 | 20 | 24 | fits | 117,864 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 1,595,260 | 15.953 | 20 | 24 | fits | 65,740 | 32 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 130,646 | 1.306 | 20 | 50 | fits | 117,864 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 576,776 | 5.768 | 20 | 50 | fits | 103,798 | 64 | 0.723 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 317,752 | 3.178 | 18 | 18 | fits | 187,561 | 141 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if1` | 1,733,753 | 17.338 | 18 | 18 | fits | 34,192 | 15 | 0.770 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 651,281 | 6.513 | 20 | 20 | fits | 141,118 | 57 | 0.710 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 111,487 | 1.115 | 20 | 200 | fits | 117,864 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 781,990 | 7.820 | 20 | 200 | fits | 141,118 | 57 | 0.710 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 112,399 | 1.124 | 20 | 20 | fits | 117,864 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 1,001,271 | 10.013 | 20 | 20 | fits | 98,182 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 115,984 | 1.160 | 20 | 24 | fits | 117,864 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 1,535,880 | 15.359 | 20 | 24 | fits | 65,867 | 31 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 114,944 | 1.149 | 20 | 50 | fits | 117,864 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 644,548 | 6.445 | 20 | 50 | fits | 142,386 | 98 | 0.614 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 303,021 | 3.030 | 18 | 18 | fits | 188,532 | 146 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if1` | 1,720,277 | 17.203 | 18 | 18 | fits | 46,290 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 619,673 | 6.197 | 20 | 20 | fits | 141,916 | 57 | 0.714 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 116,376 | 1.164 | 20 | 200 | fits | 117,864 | 135 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 750,858 | 7.509 | 20 | 200 | fits | 141,916 | 57 | 0.714 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 117,288 | 1.173 | 20 | 20 | fits | 117,864 | 135 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 936,097 | 9.361 | 20 | 20 | fits | 64,390 | 31 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 120,873 | 1.209 | 20 | 24 | fits | 117,864 | 135 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 1,534,851 | 15.349 | 20 | 24 | fits | 65,276 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 119,833 | 1.198 | 20 | 50 | fits | 117,864 | 135 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 612,618 | 6.126 | 20 | 50 | fits | 162,365 | 98 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 365,913 | 3.659 | 18 | 18 | fits | 124,350 | 64 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if1` | 1,718,541 | 17.185 | 18 | 18 | fits | 46,150 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 605,898 | 6.059 | 20 | 20 | fits | 141,896 | 57 | 0.715 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 110,333 | 1.103 | 20 | 200 | fits | 117,216 | 134 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 737,063 | 7.371 | 20 | 200 | fits | 141,896 | 57 | 0.715 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 111,245 | 1.112 | 20 | 20 | fits | 117,216 | 134 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 922,611 | 9.226 | 20 | 20 | fits | 98,136 | 46 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 114,830 | 1.148 | 20 | 24 | fits | 117,216 | 134 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 1,483,881 | 14.839 | 20 | 24 | fits | 65,109 | 31 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 113,790 | 1.138 | 20 | 50 | fits | 117,216 | 134 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 598,843 | 5.988 | 20 | 50 | fits | 162,269 | 98 | 0.665 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 352,234 | 3.522 | 18 | 18 | fits | 123,963 | 64 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if1` | 1,713,721 | 17.137 | 18 | 18 | fits | 46,150 | 18 | 0.688 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 454,202 | 4.542 | 20 | 20 | fits | 154,432 | 84 | 0.672 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 118,772 | 1.188 | 20 | 200 | fits | 117,713 | 134 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 596,146 | 5.961 | 20 | 200 | fits | 154,432 | 84 | 0.672 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 119,684 | 1.197 | 20 | 20 | fits | 117,713 | 134 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 846,262 | 8.463 | 20 | 20 | fits | 118,890 | 46 | 0.696 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 123,269 | 1.233 | 20 | 24 | fits | 117,713 | 134 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if1` | 1,469,705 | 14.697 | 20 | 24 | fits | 52,825 | 28 | 0.738 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 122,229 | 1.222 | 20 | 50 | fits | 117,713 | 134 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 599,822 | 5.998 | 20 | 50 | fits | 154,432 | 84 | 0.672 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 278,983 | 2.790 | 18 | 18 | fits | 157,209 | 137 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if1` | 1,611,616 | 16.116 | 18 | 18 | fits | 46,390 | 19 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 467,494 | 4.675 | 20 | 20 | fits | 153,812 | 84 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 121,816 | 1.218 | 20 | 200 | fits | 117,757 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 609,185 | 6.092 | 20 | 200 | fits | 153,812 | 84 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 122,728 | 1.227 | 20 | 20 | fits | 117,757 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 845,826 | 8.458 | 20 | 20 | fits | 106,411 | 42 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 126,313 | 1.263 | 20 | 24 | fits | 117,757 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if1` | 1,503,314 | 15.033 | 20 | 24 | fits | 69,343 | 38 | 0.722 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 125,273 | 1.253 | 20 | 50 | fits | 117,757 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 612,861 | 6.129 | 20 | 50 | fits | 153,812 | 84 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 313,631 | 3.136 | 18 | 18 | fits | 188,813 | 146 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if1` | 1,595,539 | 15.955 | 18 | 18 | fits | 46,683 | 19 | 0.695 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 479,896 | 4.799 | 20 | 20 | fits | 151,954 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 126,996 | 1.270 | 20 | 200 | fits | 117,607 | 135 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 620,828 | 6.208 | 20 | 200 | fits | 151,954 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 127,908 | 1.279 | 20 | 20 | fits | 117,607 | 135 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 895,401 | 8.954 | 20 | 20 | fits | 97,337 | 39 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 131,493 | 1.315 | 20 | 24 | fits | 117,607 | 135 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if1` | 1,478,723 | 14.787 | 20 | 24 | fits | 65,506 | 32 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 130,453 | 1.305 | 20 | 50 | fits | 117,607 | 135 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 624,504 | 6.245 | 20 | 50 | fits | 151,954 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 317,324 | 3.173 | 18 | 18 | fits | 187,326 | 141 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if1` | 1,617,385 | 16.174 | 18 | 18 | fits | 46,530 | 19 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 464,696 | 4.647 | 20 | 20 | fits | 139,248 | 79 | 0.679 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 111,546 | 1.115 | 20 | 200 | fits | 117,923 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 591,999 | 5.920 | 20 | 200 | fits | 139,248 | 79 | 0.679 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 112,458 | 1.125 | 20 | 20 | fits | 117,923 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 904,611 | 9.046 | 20 | 20 | fits | 98,277 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 116,043 | 1.160 | 20 | 24 | fits | 117,923 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if1` | 1,488,801 | 14.888 | 20 | 24 | fits | 65,666 | 32 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 115,003 | 1.150 | 20 | 50 | fits | 117,923 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 595,675 | 5.957 | 20 | 50 | fits | 139,248 | 79 | 0.679 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 302,845 | 3.028 | 18 | 18 | fits | 188,297 | 146 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if1` | 1,740,637 | 17.406 | 18 | 18 | fits | 35,341 | 15 | 0.798 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 571,465 | 5.715 | 20 | 20 | fits | 140,674 | 57 | 0.709 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 116,613 | 1.166 | 20 | 200 | fits | 117,923 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 701,961 | 7.020 | 20 | 200 | fits | 140,674 | 57 | 0.709 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 117,525 | 1.175 | 20 | 20 | fits | 117,923 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 921,286 | 9.213 | 20 | 20 | fits | 98,182 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 121,110 | 1.211 | 20 | 24 | fits | 117,923 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if1` | 1,523,733 | 15.237 | 20 | 24 | fits | 61,056 | 32 | 0.772 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 120,070 | 1.201 | 20 | 50 | fits | 117,923 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 564,963 | 5.650 | 20 | 50 | fits | 104,522 | 64 | 0.729 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 306,941 | 3.069 | 18 | 18 | fits | 187,326 | 141 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if1` | 1,700,341 | 17.003 | 18 | 18 | fits | 46,500 | 18 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 574,026 | 5.740 | 20 | 20 | fits | 141,297 | 57 | 0.712 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 120,406 | 1.204 | 20 | 200 | fits | 117,923 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 704,914 | 7.049 | 20 | 200 | fits | 141,297 | 57 | 0.712 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 121,318 | 1.213 | 20 | 20 | fits | 117,923 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 924,124 | 9.241 | 20 | 20 | fits | 98,159 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 124,903 | 1.249 | 20 | 24 | fits | 117,923 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if1` | 1,611,602 | 16.116 | 20 | 24 | fits | 65,462 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 123,863 | 1.239 | 20 | 50 | fits | 117,923 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 567,293 | 5.673 | 20 | 50 | fits | 143,030 | 98 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 318,201 | 3.182 | 18 | 18 | fits | 186,148 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if1` | 1,703,113 | 17.031 | 18 | 18 | fits | 46,473 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 525,384 | 5.254 | 20 | 20 | fits | 141,708 | 57 | 0.713 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 114,066 | 1.141 | 20 | 200 | fits | 117,565 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 656,361 | 6.564 | 20 | 200 | fits | 141,708 | 57 | 0.713 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 114,978 | 1.150 | 20 | 20 | fits | 117,565 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 841,896 | 8.419 | 20 | 20 | fits | 98,178 | 46 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 118,563 | 1.186 | 20 | 24 | fits | 117,565 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if1` | 1,487,612 | 14.876 | 20 | 24 | fits | 65,229 | 31 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 117,523 | 1.175 | 20 | 50 | fits | 117,565 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 518,329 | 5.183 | 20 | 50 | fits | 162,891 | 98 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 355,373 | 3.554 | 18 | 18 | fits | 124,153 | 64 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if1` | 1,718,056 | 17.181 | 18 | 18 | fits | 46,311 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 570,226 | 5.702 | 20 | 20 | fits | 144,839 | 64 | 0.709 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 117,019 | 1.170 | 20 | 200 | fits | 117,565 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 700,225 | 7.002 | 20 | 200 | fits | 144,839 | 64 | 0.709 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 117,931 | 1.179 | 20 | 20 | fits | 117,565 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 919,614 | 9.196 | 20 | 20 | fits | 98,183 | 40 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 121,516 | 1.215 | 20 | 24 | fits | 117,565 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if1` | 1,600,220 | 16.002 | 20 | 24 | fits | 65,462 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 120,476 | 1.205 | 20 | 50 | fits | 117,565 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 559,062 | 5.591 | 20 | 50 | fits | 144,295 | 98 | 0.620 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 251,800 | 2.518 | 18 | 18 | fits | 131,779 | 105 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if1` | 1,691,731 | 16.917 | 18 | 18 | fits | 46,473 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 474,788 | 4.748 | 20 | 20 | fits | 152,006 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 119,019 | 1.190 | 20 | 200 | fits | 117,341 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 615,772 | 6.158 | 20 | 200 | fits | 152,006 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 119,931 | 1.199 | 20 | 20 | fits | 117,341 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 857,709 | 8.577 | 20 | 20 | fits | 120,356 | 46 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 123,516 | 1.235 | 20 | 24 | fits | 117,341 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 1,527,311 | 15.273 | 20 | 24 | fits | 65,615 | 32 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 122,476 | 1.225 | 20 | 50 | fits | 117,341 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 619,448 | 6.194 | 20 | 50 | fits | 152,006 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 312,134 | 3.121 | 18 | 18 | fits | 190,113 | 146 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 1,759,228 | 17.592 | 18 | 18 | fits | 34,250 | 15 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 478,622 | 4.786 | 20 | 20 | fits | 153,519 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 125,225 | 1.252 | 20 | 200 | fits | 117,464 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 620,196 | 6.202 | 20 | 200 | fits | 153,519 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 126,137 | 1.261 | 20 | 20 | fits | 117,464 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 828,252 | 8.283 | 20 | 20 | fits | 86,418 | 37 | 0.652 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 129,722 | 1.297 | 20 | 24 | fits | 117,464 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 1,564,332 | 15.643 | 20 | 24 | fits | 65,362 | 32 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 128,682 | 1.287 | 20 | 50 | fits | 117,464 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 623,872 | 6.239 | 20 | 50 | fits | 153,519 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 316,853 | 3.169 | 18 | 18 | fits | 188,626 | 141 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 1,748,937 | 17.489 | 18 | 18 | fits | 34,080 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 465,069 | 4.651 | 20 | 20 | fits | 153,519 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 110,619 | 1.106 | 20 | 200 | fits | 117,464 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 606,643 | 6.066 | 20 | 200 | fits | 153,519 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 111,531 | 1.115 | 20 | 20 | fits | 117,464 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 983,954 | 9.840 | 20 | 20 | fits | 97,315 | 39 | 0.741 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 115,116 | 1.151 | 20 | 24 | fits | 117,464 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 1,626,221 | 16.262 | 20 | 24 | fits | 65,789 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 114,076 | 1.141 | 20 | 50 | fits | 117,464 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 610,319 | 6.103 | 20 | 50 | fits | 153,519 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 303,218 | 3.032 | 18 | 18 | fits | 189,597 | 146 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 1,746,735 | 17.467 | 18 | 18 | fits | 41,101 | 19 | 0.794 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 467,002 | 4.670 | 20 | 20 | fits | 139,186 | 79 | 0.678 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 114,412 | 1.144 | 20 | 200 | fits | 117,464 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 594,334 | 5.943 | 20 | 200 | fits | 139,186 | 79 | 0.678 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 115,324 | 1.153 | 20 | 20 | fits | 117,464 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 989,674 | 9.897 | 20 | 20 | fits | 102,330 | 46 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 118,909 | 1.189 | 20 | 24 | fits | 117,464 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 1,620,768 | 16.208 | 20 | 24 | fits | 58,832 | 32 | 0.757 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 117,869 | 1.179 | 20 | 50 | fits | 117,464 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 598,010 | 5.980 | 20 | 50 | fits | 139,186 | 79 | 0.678 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 313,535 | 3.135 | 18 | 18 | fits | 187,525 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 1,747,678 | 17.477 | 18 | 18 | fits | 34,101 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 652,424 | 6.524 | 20 | 20 | fits | 126,825 | 54 | 0.717 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 126,631 | 1.266 | 20 | 200 | fits | 117,165 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 769,917 | 7.699 | 20 | 200 | fits | 126,825 | 54 | 0.717 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 127,543 | 1.275 | 20 | 20 | fits | 117,165 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 993,007 | 9.930 | 20 | 20 | fits | 98,515 | 40 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 131,128 | 1.311 | 20 | 24 | fits | 117,165 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 1,557,820 | 15.578 | 20 | 24 | fits | 33,463 | 22 | 0.672 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 130,088 | 1.301 | 20 | 50 | fits | 117,165 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 567,704 | 5.677 | 20 | 50 | fits | 104,640 | 64 | 0.729 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 317,907 | 3.179 | 18 | 18 | fits | 188,274 | 140 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 1,766,473 | 17.665 | 18 | 18 | fits | 34,113 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 600,761 | 6.008 | 20 | 20 | fits | 105,368 | 49 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 111,003 | 1.110 | 20 | 200 | fits | 117,118 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 696,913 | 6.969 | 20 | 200 | fits | 105,368 | 49 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 111,915 | 1.119 | 20 | 20 | fits | 117,118 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 916,706 | 9.167 | 20 | 20 | fits | 98,110 | 40 | 0.743 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 115,500 | 1.155 | 20 | 24 | fits | 117,118 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 1,534,741 | 15.347 | 20 | 24 | fits | 99,715 | 45 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 114,460 | 1.145 | 20 | 50 | fits | 117,118 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 516,157 | 5.162 | 20 | 50 | fits | 102,929 | 64 | 0.711 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 303,250 | 3.033 | 18 | 18 | fits | 189,245 | 145 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 1,754,031 | 17.540 | 18 | 18 | fits | 34,080 | 15 | 0.764 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 553,075 | 5.531 | 20 | 20 | fits | 160,299 | 64 | 0.736 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 114,350 | 1.143 | 20 | 200 | fits | 117,118 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 701,399 | 7.014 | 20 | 200 | fits | 160,299 | 64 | 0.736 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 115,262 | 1.153 | 20 | 20 | fits | 117,118 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 922,087 | 9.221 | 20 | 20 | fits | 98,465 | 40 | 0.745 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 118,847 | 1.188 | 20 | 24 | fits | 117,118 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 1,551,664 | 15.517 | 20 | 24 | fits | 65,719 | 31 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 117,807 | 1.178 | 20 | 50 | fits | 117,118 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 544,776 | 5.448 | 20 | 50 | fits | 108,792 | 90 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 356,892 | 3.569 | 18 | 18 | fits | 125,229 | 64 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 1,740,604 | 17.406 | 18 | 18 | fits | 51,312 | 25 | 0.720 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 610,929 | 6.109 | 20 | 20 | fits | 142,240 | 58 | 0.714 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 117,303 | 1.173 | 20 | 200 | fits | 117,118 | 134 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 742,093 | 7.421 | 20 | 200 | fits | 142,240 | 58 | 0.714 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 118,215 | 1.182 | 20 | 20 | fits | 117,118 | 134 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 969,754 | 9.698 | 20 | 20 | fits | 96,760 | 39 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 121,800 | 1.218 | 20 | 24 | fits | 117,118 | 134 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 1,576,183 | 15.762 | 20 | 24 | fits | 99,566 | 45 | 0.754 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 120,760 | 1.208 | 20 | 50 | fits | 117,118 | 134 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 603,529 | 6.035 | 20 | 50 | fits | 162,560 | 105 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 253,113 | 2.531 | 18 | 18 | fits | 132,808 | 105 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 1,753,862 | 17.539 | 18 | 18 | fits | 34,324 | 16 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 464,150 | 4.641 | 20 | 20 | fits | 153,519 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 109,950 | 1.099 | 20 | 200 | fits | 117,900 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 605,724 | 6.057 | 20 | 200 | fits | 153,519 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 110,862 | 1.109 | 20 | 20 | fits | 117,900 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 847,718 | 8.477 | 20 | 20 | fits | 120,356 | 46 | 0.705 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 114,447 | 1.144 | 20 | 24 | fits | 117,900 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if1` | 1,492,818 | 14.928 | 20 | 24 | fits | 65,534 | 32 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 113,407 | 1.134 | 20 | 50 | fits | 117,900 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 609,400 | 6.094 | 20 | 50 | fits | 153,519 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 302,299 | 3.023 | 18 | 18 | fits | 189,347 | 146 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if1` | 1,642,783 | 16.428 | 18 | 18 | fits | 46,290 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 466,523 | 4.665 | 20 | 20 | fits | 153,335 | 83 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 114,189 | 1.142 | 20 | 200 | fits | 117,343 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 608,004 | 6.080 | 20 | 200 | fits | 153,335 | 83 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 115,101 | 1.151 | 20 | 20 | fits | 117,343 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 836,083 | 8.361 | 20 | 20 | fits | 106,514 | 42 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 118,686 | 1.187 | 20 | 24 | fits | 117,343 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if1` | 1,471,288 | 14.713 | 20 | 24 | fits | 65,416 | 31 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 117,646 | 1.176 | 20 | 50 | fits | 117,343 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 611,680 | 6.117 | 20 | 50 | fits | 153,335 | 83 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 313,056 | 3.131 | 18 | 18 | fits | 187,363 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if1` | 1,655,538 | 16.555 | 18 | 18 | fits | 46,290 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 471,690 | 4.717 | 20 | 20 | fits | 153,675 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 126,934 | 1.269 | 20 | 200 | fits | 116,850 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 613,511 | 6.135 | 20 | 200 | fits | 153,675 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 127,846 | 1.278 | 20 | 20 | fits | 116,850 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 916,138 | 9.161 | 20 | 20 | fits | 101,625 | 46 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 131,431 | 1.314 | 20 | 24 | fits | 116,850 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if1` | 1,519,985 | 15.200 | 20 | 24 | fits | 65,467 | 31 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 130,391 | 1.304 | 20 | 50 | fits | 116,850 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 617,187 | 6.172 | 20 | 50 | fits | 153,675 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 318,355 | 3.184 | 18 | 18 | fits | 188,419 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if1` | 1,657,945 | 16.579 | 18 | 18 | fits | 46,290 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 456,859 | 4.569 | 20 | 20 | fits | 139,456 | 79 | 0.680 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 111,050 | 1.111 | 20 | 200 | fits | 117,165 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 584,461 | 5.845 | 20 | 200 | fits | 139,456 | 79 | 0.680 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 111,962 | 1.120 | 20 | 20 | fits | 117,165 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 901,162 | 9.012 | 20 | 20 | fits | 98,487 | 40 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 115,547 | 1.155 | 20 | 24 | fits | 117,165 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if1` | 1,538,949 | 15.389 | 20 | 24 | fits | 65,642 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 114,507 | 1.145 | 20 | 50 | fits | 117,165 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 588,137 | 5.881 | 20 | 50 | fits | 139,456 | 79 | 0.680 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 303,442 | 3.034 | 18 | 18 | fits | 189,390 | 145 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if1` | 1,739,122 | 17.391 | 18 | 18 | fits | 35,399 | 15 | 0.801 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 565,699 | 5.657 | 20 | 20 | fits | 143,773 | 64 | 0.711 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 114,722 | 1.147 | 20 | 200 | fits | 117,165 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 696,217 | 6.962 | 20 | 200 | fits | 143,773 | 64 | 0.711 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 115,634 | 1.156 | 20 | 20 | fits | 117,165 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 915,897 | 9.159 | 20 | 20 | fits | 98,372 | 40 | 0.744 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 119,219 | 1.192 | 20 | 24 | fits | 117,165 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if1` | 1,514,261 | 15.143 | 20 | 24 | fits | 60,052 | 32 | 0.763 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 118,179 | 1.182 | 20 | 50 | fits | 117,165 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 556,120 | 5.561 | 20 | 50 | fits | 104,820 | 65 | 0.729 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 306,143 | 3.061 | 18 | 18 | fits | 188,419 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if1` | 1,731,918 | 17.319 | 18 | 18 | fits | 46,311 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 569,040 | 5.690 | 20 | 20 | fits | 141,337 | 58 | 0.709 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 117,675 | 1.177 | 20 | 200 | fits | 117,165 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 699,701 | 6.997 | 20 | 200 | fits | 141,337 | 58 | 0.709 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 118,587 | 1.186 | 20 | 20 | fits | 117,165 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 927,702 | 9.277 | 20 | 20 | fits | 96,923 | 39 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 122,172 | 1.222 | 20 | 24 | fits | 117,165 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if1` | 1,628,072 | 16.281 | 20 | 24 | fits | 65,720 | 31 | 0.717 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 121,132 | 1.211 | 20 | 50 | fits | 117,165 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 562,040 | 5.620 | 20 | 50 | fits | 147,026 | 105 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 309,096 | 3.091 | 18 | 18 | fits | 188,419 | 140 | 0.626 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if1` | 1,725,116 | 17.251 | 18 | 18 | fits | 46,988 | 19 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 510,056 | 5.101 | 20 | 20 | fits | 142,793 | 58 | 0.718 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 120,628 | 1.206 | 20 | 200 | fits | 117,165 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 641,759 | 6.418 | 20 | 200 | fits | 142,793 | 58 | 0.718 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 121,540 | 1.215 | 20 | 20 | fits | 117,165 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 869,994 | 8.700 | 20 | 20 | fits | 97,110 | 39 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 125,125 | 1.251 | 20 | 24 | fits | 117,165 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if1` | 1,574,633 | 15.746 | 20 | 24 | fits | 70,306 | 38 | 0.725 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 124,085 | 1.241 | 20 | 50 | fits | 117,165 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 502,642 | 5.026 | 20 | 50 | fits | 182,929 | 105 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 502,577 | 5.026 | 18 | 18 | fits | 182,929 | 105 | 0.654 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if1` | 1,748,285 | 17.483 | 18 | 18 | fits | 34,354 | 16 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 551,458 | 5.515 | 20 | 20 | fits | 141,355 | 58 | 0.709 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 123,581 | 1.236 | 20 | 200 | fits | 117,165 | 134 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 682,182 | 6.822 | 20 | 200 | fits | 141,355 | 58 | 0.709 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 124,493 | 1.245 | 20 | 20 | fits | 117,165 | 134 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 910,197 | 9.102 | 20 | 20 | fits | 98,164 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 128,078 | 1.281 | 20 | 24 | fits | 117,165 | 134 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if1` | 1,556,298 | 15.563 | 20 | 24 | fits | 67,623 | 38 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 127,038 | 1.270 | 20 | 50 | fits | 117,165 | 134 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 544,503 | 5.445 | 20 | 50 | fits | 145,518 | 99 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 398,920 | 3.989 | 18 | 18 | fits | 182,866 | 105 | 0.653 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if1` | 1,776,520 | 17.765 | 18 | 18 | fits | 34,353 | 16 | 0.757 |
| LINK_UP | `adp.link_up.if0` | 2,772 | 0.028 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| LINK_UP | `adp.link_up.if1` | 16,983 | 0.170 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,636 | 0.206 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 12,589 | 0.126 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 11,775 | 0.118 | 20 | 200 | fits | 5,398 | 18 (11) | 0.592 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 9,159 | 0.092 | 20 | 200 | fits | 5,398 | 18 (11) | 0.592 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 14,452 | 0.145 | 20 | 50 | fits | 31,127 | 46 | 0.686 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 22,768 | 0.228 | 20 | 50 | fits | 28,206 | 38 | 0.658 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 24,375 | 0.244 | 20 | 50 | fits | 28,180 | 38 | 0.661 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 16,757 | 0.168 | 20 | 50 | fits | 34,349 | 65 | 0.599 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 18,487 | 0.185 | 20 | 50 | fits | 34,349 | 65 | 0.599 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,457 | 0.115 | 20 | 50 | fits | 25,556 | 33 | 0.537 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 13,349 | 0.133 | 20 | 50 | fits | 30,572 | 46 | 0.680 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 12,120 | 0.121 | 20 | 50 | fits | 28,749 | 38 | 0.667 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 20,447 | 0.204 | 20 | 50 | fits | 28,062 | 38 | 0.649 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 21,431 | 0.214 | 20 | 50 | fits | 35,543 | 65 | 0.615 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 23,289 | 0.233 | 20 | 50 | fits | 35,543 | 65 | 0.615 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 11,208 | 0.112 | 20 | 50 | fits | 25,650 | 33 | 0.506 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 26,072 | 0.261 | 20 | 20 | fits | 51,819 | 30 (35) | 0.783 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 13,033 | 0.130 | 20 | 20 | fits | 47,640 | 24 (35) | 0.778 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 27,835 | 0.278 | 20 | 20 | fits | 46,376 | 25 (14) | 0.825 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 8,950 | 0.089 | 20 | 20 | fits | 40,852 | 19 (14) | 0.833 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 26,439 | 0.264 | 20 | 20 | fits | 46,318 | 26 (14) | 0.815 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 7,510 | 0.075 | 20 | 20 | fits | 40,091 | 19 (14) | 0.822 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 44,322 | 0.443 | 20 | 20 | fits | 50,710 | 24 (35) | 0.802 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 47,879 | 0.479 | 20 | 20 | fits | 53,473 | 31 (35) | 0.774 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 855,698 | 8.557 | 18 | 18 | fits | 50,105 | 15 | 0.844 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 930,227 | 9.302 | 18 | 18 | fits | 49,465 | 15 | 0.836 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 57,793 | 0.578 | 18 | 18 | fits | 57,858 | 15 | 0.884 |
| malformed MRPDU discard | `srp.malformed.if0` | 22,106 | 0.221 | 18 | 18 | fits | 22,171 | 15 | 0.527 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 203,449 | 2.034 | 218 | 218 | fits | 171,351 | 18 | 0.775 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 50,054 | 0.501 | 18 | 18 | fits | 50,119 | 15 | 0.860 |
| malformed MRPDU discard | `srp.malformed.if1` | 22,084 | 0.221 | 18 | 18 | fits | 22,149 | 15 | 0.500 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 172,893 | 1.729 | 218 | 218 | fits | 142,654 | 18 | 0.778 |
| an event behind 15 others | `backlog.event.if0` | 150,513 | 1.505 | 20 | 200 | fits | 116,968 | 125 | 0.541 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 710,630 | 7.106 | 20 | 20 | fits | 80,418 | 39 | 0.713 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 138,707 | 1.387 | 20 | 200 | fits | 138,915 | 143 | 0.529 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 550,213 | 5.502 | 20 | 200 | fits | 132,301 | 57 | 0.695 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 134,448 | 1.344 | 20 | 20 | fits | 138,915 | 143 | 0.529 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 778,734 | 7.787 | 20 | 20 | fits | 80,418 | 39 | 0.713 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 138,033 | 1.380 | 20 | 24 | fits | 138,915 | 143 | 0.529 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,248,697 | 12.487 | 20 | 24 | fits | 51,735 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 136,993 | 1.370 | 20 | 50 | fits | 138,915 | 143 | 0.529 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 548,718 | 5.487 | 20 | 50 | fits | 132,301 | 57 | 0.695 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 548,653 | 5.487 | 18 | 18 | fits | 132,301 | 57 | 0.695 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,414,026 | 14.140 | 18 | 18 | fits | 32,236 | 15 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 468,610 | 4.686 | 20 | 20 | fits | 160,997 | 58 | 0.750 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 111,058 | 1.111 | 20 | 200 | fits | 115,740 | 140 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 618,902 | 6.189 | 20 | 200 | fits | 160,997 | 58 | 0.750 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 111,970 | 1.120 | 20 | 20 | fits | 115,740 | 140 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 847,333 | 8.473 | 20 | 20 | fits | 98,060 | 39 | 0.746 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 115,555 | 1.156 | 20 | 24 | fits | 115,740 | 140 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,421,336 | 14.213 | 20 | 24 | fits | 51,943 | 28 | 0.741 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 114,515 | 1.145 | 20 | 50 | fits | 115,740 | 140 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 461,581 | 4.616 | 20 | 50 | fits | 124,785 | 65 | 0.741 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 461,516 | 4.615 | 18 | 18 | fits | 124,785 | 65 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,644,714 | 16.447 | 18 | 18 | fits | 34,175 | 16 | 0.754 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,904 | 0.089 | 20 | 20 | fits | 45,742 | 27 | 0.780 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 111,058 | 1.111 | 20 | 200 | fits | 115,740 | 140 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 42,854 | 0.429 | 20 | 200 | fits | 45,742 | 27 | 0.780 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 111,970 | 1.120 | 20 | 20 | fits | 115,740 | 140 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 826,736 | 8.267 | 20 | 20 | fits | 98,091 | 39 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 115,555 | 1.156 | 20 | 24 | fits | 115,740 | 140 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,416,171 | 14.162 | 20 | 24 | fits | 65,292 | 32 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 114,515 | 1.145 | 20 | 50 | fits | 115,740 | 140 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 461,581 | 4.616 | 20 | 50 | fits | 124,785 | 65 | 0.741 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 461,516 | 4.615 | 18 | 18 | fits | 124,785 | 65 | 0.741 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,604,560 | 16.046 | 18 | 18 | fits | 46,385 | 19 | 0.682 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,355,246 | 63.552 | 20 | 20 | MISS ceiling | 48,040 | 27 | 0.586 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,040,782 | 360.408 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,040,707 | 360.407 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,040,632 | 360.406 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,040,557 | 360.406 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 114,586 | 1.146 | 20 | 200 | fits | 112,944 | 134 | 0.519 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 657,978 | 6.580 | 20 | 200 | fits | 112,730 | 43 | 0.725 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 110,327 | 1.103 | 20 | 20 | fits | 112,944 | 134 | 0.519 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 821,724 | 8.217 | 20 | 20 | fits | 68,724 | 25 | 0.732 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 113,912 | 1.139 | 20 | 24 | fits | 112,944 | 134 | 0.519 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,481,074 | 64.811 | 20 | 24 | MISS ceiling | 29,461 | 23 | 0.556 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 112,872 | 1.129 | 20 | 50 | fits | 112,944 | 134 | 0.519 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 543,753 | 5.438 | 20 | 50 | fits | 140,962 | 91 | 0.642 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 242,386 | 2.424 | 18 | 18 | fits | 129,969 | 102 | 0.705 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,318,573 | 13.186 | 18 | 18 | fits | 45,473 | 21 | 0.653 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,434 | 0.054 | 20 | 20 | fits | 56,726 | 19 (29) | 0.658 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 24,039 | 0.240 | 20 | 20 | fits | 56,726 | 19 (29) | 0.658 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,572 | 0.076 | 20 | 20 | fits | 60,279 | 30 (35) | 0.673 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 27,263 | 0.273 | 20 | 20 | fits | 60,279 | 30 (35) | 0.673 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 8,261 | 0.083 | 20 | 20 | fits | 61,587 | 26 (12) | 0.825 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 28,245 | 0.282 | 20 | 20 | fits | 49,741 | 24 (12) | 0.800 |
| LINK_UP | `adp.link_up.if0` | 2,772 | 0.028 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| LINK_UP | `adp.link_up.if1` | 16,983 | 0.170 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,636 | 0.206 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 12,589 | 0.126 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| LINK_DOWN | `adp.link_down.if0` | 2,266 | 0.023 | 20 | 200 | fits | 67,905 | 38 (9) | 0.690 |
| LINK_DOWN | `adp.link_down.if1` | 33,028 | 0.330 | 20 | 200 | fits | 67,905 | 38 (9) | 0.690 |
| LINK_UP | `adp.link_up.if0` | 2,772 | 0.028 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| LINK_UP | `adp.link_up.if1` | 16,983 | 0.170 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,636 | 0.206 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 12,589 | 0.126 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| GM_CHANGE | `adp.gm_change.if0` | 2,359 | 0.024 | 20 | 200 | fits | 18,729 | 28 (11) | 0.483 |
| GM_CHANGE | `adp.gm_change.if1` | 4,181 | 0.042 | 20 | 200 | fits | 18,729 | 28 (11) | 0.483 |
| LINK_UP | `adp.link_up.if0` | 2,772 | 0.028 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| LINK_UP | `adp.link_up.if1` | 16,983 | 0.170 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,636 | 0.206 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 12,589 | 0.126 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 3,512 | 0.035 | 20 | 200 | fits | 18,956 | 25 (31) | 0.343 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 5,037 | 0.050 | 20 | 200 | fits | 18,956 | 25 (31) | 0.343 |
| LINK_UP | `adp.link_up.if0` | 2,772 | 0.028 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| LINK_UP | `adp.link_up.if1` | 16,983 | 0.170 | 20 | 200 | fits | 42,515 | 82 (11) | 0.615 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,636 | 0.206 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 12,589 | 0.126 | 20 | 200 | fits | 33,906 | 42 (39) | 0.571 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 3,512 | 0.035 | 20 | 200 | fits | 17,434 | 18 (31) | 0.455 |
| set_name | `aecp_fanout.set_name.if0` | 95,904 | 0.959 | 20 | 24 | fits | 98,329 | 225 | 0.211 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 77,944 | 0.779 | 20 | 24 | fits | 84,043 | 205 | 0.262 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 75,804 | 0.758 | 20 | 24 | fits | 79,897 | 205 | 0.223 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 80,007 | 0.800 | 20 | 24 | fits | 77,816 | 205 | 0.193 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 75,234 | 0.752 | 20 | 24 | fits | 80,472 | 181 | 0.240 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 76,998 | 0.770 | 20 | 24 | fits | 81,336 | 205 | 0.221 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 82,810 | 0.828 | 20 | 24 | fits | 79,893 | 205 | 0.192 |
| set_name | `aecp_fanout.set_name.if1` | 86,095 | 0.861 | 20 | 24 | fits | 91,773 | 181 | 0.190 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 77,797 | 0.778 | 20 | 24 | fits | 83,663 | 205 | 0.256 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 80,869 | 0.809 | 20 | 24 | fits | 78,621 | 205 | 0.208 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 75,506 | 0.755 | 20 | 24 | fits | 79,232 | 205 | 0.217 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 75,976 | 0.760 | 20 | 24 | fits | 81,411 | 205 | 0.217 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 82,731 | 0.827 | 20 | 24 | fits | 79,814 | 205 | 0.192 |
| BIND_RX | `acmp.bind_rx.if0` | 25,626 | 0.256 | 20 | 20 | fits | 61,435 | 30 (77) | 0.746 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,857 | 0.089 | 20 | 20 | fits | 43,332 | 21 (32) | 0.806 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 12,248 | 0.122 | 20 | 20 | fits | 45,133 | 18 (47) | 0.733 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 16,151 | 0.162 | 20 | 20 | fits | 54,634 | 21 (50) | 0.812 |
| PROBE_TX | `acmp.probe_tx.if0` | 12,194 | 0.122 | 20 | 20 | fits | 43,881 | 20 (48) | 0.699 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,357 | 0.114 | 20 | 20 | fits | 42,395 | 18 (48) | 0.661 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 12,638 | 0.126 | 20 | 20 | fits | 44,883 | 19 (48) | 0.730 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 10,708 | 0.107 | 20 | 20 | fits | 42,182 | 19 (48) | 0.655 |
| BIND_RX | `acmp.bind_rx.if1` | 22,524 | 0.225 | 20 | 20 | fits | 57,006 | 31 (77) | 0.705 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 8,835 | 0.088 | 20 | 20 | fits | 43,623 | 22 (32) | 0.787 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 12,791 | 0.128 | 20 | 20 | fits | 47,471 | 19 (47) | 0.737 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 15,456 | 0.155 | 20 | 20 | fits | 55,190 | 23 (50) | 0.788 |
| PROBE_TX | `acmp.probe_tx.if1` | 13,970 | 0.140 | 20 | 20 | fits | 47,106 | 22 (48) | 0.724 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 12,560 | 0.126 | 20 | 20 | fits | 44,992 | 20 (48) | 0.721 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 10,727 | 0.107 | 20 | 20 | fits | 43,006 | 20 (48) | 0.650 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 10,708 | 0.107 | 20 | 20 | fits | 42,987 | 20 (48) | 0.650 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 25,929 | 0.259 | 20 | 24 | fits | 27,616 | 24 | 0.710 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 32,773 | 0.328 | 20 | 24 | fits | 33,181 | 24 | 0.659 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 21,675 | 0.217 | 20 | 24 | fits | 29,580 | 24 | 0.678 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 29,840 | 0.298 | 20 | 24 | fits | 28,929 | 24 | 0.664 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 27,531 | 0.275 | 20 | 24 | fits | 28,998 | 24 | 0.669 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 29,938 | 0.299 | 20 | 24 | fits | 28,911 | 24 | 0.657 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 26,665 | 0.267 | 20 | 24 | fits | 28,078 | 24 | 0.682 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 28,835 | 0.288 | 20 | 24 | fits | 27,734 | 24 | 0.662 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 29,127 | 0.291 | 20 | 24 | fits | 28,059 | 24 | 0.685 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 32,069 | 0.321 | 20 | 24 | fits | 33,206 | 24 | 0.605 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 28,639 | 0.286 | 20 | 24 | fits | 27,498 | 24 | 0.681 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 26,509 | 0.265 | 20 | 24 | fits | 27,556 | 24 | 0.697 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 28,679 | 0.287 | 20 | 24 | fits | 27,429 | 24 | 0.667 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 27,679 | 0.277 | 20 | 24 | fits | 28,802 | 24 | 0.673 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 27,421 | 0.274 | 20 | 24 | fits | 28,508 | 24 | 0.682 |
| get_configuration | `aecp.get_configuration.if0` | 27,068 | 0.271 | 20 | 24 | fits | 25,301 | 24 | 0.659 |
| entity_available | `aecp.entity_available.if0` | 25,243 | 0.252 | 20 | 24 | fits | 26,013 | 24 | 0.659 |
| get_name | `aecp.get_name.if0` | 28,909 | 0.289 | 20 | 24 | fits | 27,725 | 24 | 0.681 |
| get_counters | `aecp.get_counters.if0` | 29,325 | 0.293 | 20 | 24 | fits | 30,668 | 30 | 0.682 |
| get_avb_info | `aecp.get_avb_info.if0` | 19,236 | 0.192 | 20 | 24 | fits | 33,909 | 30 | 0.703 |
| unknown_command | `aecp.unknown_command.if0` | 30,851 | 0.309 | 20 | 24 | fits | 25,914 | 24 | 0.681 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 25,078 | 0.251 | 20 | 24 | fits | 25,851 | 24 | 0.679 |
| set_name | `aecp.set_name.if0` | 41,874 | 0.419 | 20 | 24 | fits | 50,254 | 70 | 0.599 |
| lock_entity | `aecp.lock_entity.if0` | 32,247 | 0.322 | 20 | 24 | fits | 37,701 | 50 | 0.643 |
| unlock_entity | `aecp.unlock_entity.if0` | 33,230 | 0.332 | 20 | 24 | fits | 35,649 | 49 | 0.602 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 27,400 | 0.274 | 20 | 24 | fits | 25,909 | 22 | 0.661 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 33,771 | 0.338 | 20 | 24 | fits | 31,774 | 22 | 0.644 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 32,535 | 0.325 | 20 | 24 | fits | 28,280 | 22 | 0.667 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 30,751 | 0.308 | 20 | 24 | fits | 28,812 | 22 | 0.671 |
| get_configuration | `aecp.get_configuration.if1` | 29,753 | 0.298 | 20 | 24 | fits | 24,829 | 22 | 0.647 |
| entity_available | `aecp.entity_available.if1` | 30,512 | 0.305 | 20 | 24 | fits | 25,589 | 22 | 0.658 |
| get_name | `aecp.get_name.if1` | 29,831 | 0.298 | 20 | 24 | fits | 27,938 | 22 | 0.692 |
| get_counters | `aecp.get_counters.if1` | 33,553 | 0.336 | 20 | 24 | fits | 29,713 | 28 | 0.671 |
| get_avb_info | `aecp.get_avb_info.if1` | 28,566 | 0.286 | 20 | 24 | fits | 26,648 | 22 | 0.715 |
| unknown_command | `aecp.unknown_command.if1` | 29,513 | 0.295 | 20 | 24 | fits | 24,878 | 22 | 0.647 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 30,180 | 0.302 | 20 | 24 | fits | 25,715 | 22 | 0.685 |
| set_name | `aecp.set_name.if1` | 40,018 | 0.400 | 20 | 24 | fits | 46,071 | 31 | 0.633 |
| lock_entity | `aecp.lock_entity.if1` | 35,957 | 0.360 | 20 | 24 | fits | 37,556 | 55 | 0.569 |
| unlock_entity | `aecp.unlock_entity.if1` | 35,548 | 0.355 | 20 | 24 | fits | 38,431 | 55 | 0.585 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
