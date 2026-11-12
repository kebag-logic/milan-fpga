### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 136 paths and 6 of 996 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.277 (0.643) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.238 (0.585) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.130 (0.456) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.121 (0.443) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.076 (0.635) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.277 (0.635) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.063 (0.606) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.252 (0.606) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.136 (0.467) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.144 (0.478) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.121 (0.442) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.120 (0.443) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.224 (0.584) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.125 (0.452) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.133 (0.461) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.155 (0.486) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.096 (0.450) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.093 (0.447) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.402 (1.717) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.254 (0.807) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.116 (0.871) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.287 (0.838) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.288 (1.094) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.557 (1.094) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.335 (0.989) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.554 (0.989) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.139 (0.524) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.249 (0.883) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.335 (0.974) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.548 (0.974) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.173 (0.557) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.176 (0.570) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.052 (0.244) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.066 (0.244) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.025 (0.212) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.042 (0.212) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.024 (0.672) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.304 (0.672) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.027 (0.449) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.175 (0.449) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.150 (0.352) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.130 (0.352) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.187 (0.567) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.110 (0.567) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.231 (0.608) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.170 (0.533) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.451 (0.839) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 1 | `aecp.get_avb_info.if1` (aecp) | 0.206 (0.591) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.145 (0.506) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.255 (0.627) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.189 (0.567) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 1 | `aecp.get_counters.if1` (aecp) | 0.282 (0.566) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.173 (0.536) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.282 (0.657) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.282 (0.650) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.404 (0.742) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.232 (0.597) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.161 (0.522) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.302 (0.689) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.319 (0.699) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.243 (0.563) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.282 (0.662) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.240 (0.645) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.169 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.298 (0.680) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.164 (0.532) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.247 (0.629) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.174 (0.557) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.195 (0.562) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.162 (0.534) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.177 (0.558) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.258 (0.640) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.254 (0.634) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.177 (0.546) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.248 (0.630) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.143 (0.517) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.155 (0.534) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.485 (0.851) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.448 (0.812) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.149 (0.522) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 1 | `aecp.unknown_command.if1` (aecp) | 0.264 (0.638) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.384 (0.713) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.317 (0.656) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.628 (1.005) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.628 (1.004) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.569 (0.981) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.656 (1.045) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.630 (1.007) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 0.546 (0.924) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.734 (1.154) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.614 (1.010) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.558 (0.947) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.547 (0.928) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.547 (0.926) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 9.403 (10.702) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-6.adp_available.if0` (backlog-adp@verify-aged2-6) | 11.014 (11.847) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.198 (0.733) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 2.033 (3.215) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.055 (64.576) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.391 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 10.915 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 9.403 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 6.906 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 10.019 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 5.939 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.192 (0.586) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.294 (0.695) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.126 (0.277) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.128 (0.281) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.146 (0.332) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.135 (0.321) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.173 (0.586) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.275 (0.695) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.291 (0.668) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 0.206 (0.587) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 3.000 | fits | 0 srp | 6 | 0 |
| an MRPDU its join timer owes, the longest | 1 | `save-starved.mrpdu.periodic.if1` (save-starved) | 5.571 | fits | 0 srp | 6 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 2.404 | fits | 0 acmp | 76 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.acmp.last.if0` (backlog-adp@verify-aged2-6) | 13.451 | fits | 11 acmp | 76 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 2.395 | fits | 0 adp | 76 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-3.service.adp.last.if0` (backlog-adp@verify-aged2-3) | 12.220 | fits | 7 adp | 74 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 9.547 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.440 | fits | 0 aecp | 76 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 62.122 | MISS ceiling | 15 aecp | 76 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 2.430 | fits | 0 maap | 76 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-3.service.maap.last.if0` (backlog-adp@verify-aged2-3) | 12.256 | fits | 6 maap | 76 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.srp.first.if0` (backlog-adp@verify-aged2-6) | 7.242 | fits | 0 srp | 76 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-aged2-7.service.srp.last.if1` (backlog-adp@blank-aged2-7) | 10.292 | fits | 31 srp | 76 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.912 (2.368) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.631 (2.035) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.558 (0.559) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.511 (0.512) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.241 (0.242) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.243 (0.244) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.444 (1.509) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.359 (1.418) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 15.070 | 11 | 166,365 (1.664) | yes | - |
| backlog-adp@blank-1 | 0 | 14.248 | 11 | 163,821 (1.638) | yes | - |
| backlog-adp@blank-2 | 0 | 13.968 | 10 | 174,650 (1.746) | yes | - |
| backlog-adp@blank-3 | 0 | 13.968 | 10 | 172,565 (1.726) | yes | - |
| backlog-adp@blank-4 | 0 | 13.835 | 9 | 168,075 (1.681) | yes | - |
| backlog-adp@blank-5 | 0 | 14.957 | 10 | 164,267 (1.643) | yes | - |
| backlog-adp@blank-6 | 0 | 14.989 | 11 | 168,572 (1.686) | yes | - |
| backlog-adp@blank-7 | 0 | 14.467 | 11 | 172,802 (1.728) | yes | - |
| backlog-adp@program-0 | 0 | 13.939 | 9 | 166,900 (1.669) | yes | - |
| backlog-adp@program-1 | 0 | 13.774 | 8 | 168,248 (1.682) | yes | - |
| backlog-adp@program-2 | 0 | 14.607 | 11 | 163,802 (1.638) | yes | - |
| backlog-adp@program-3 | 0 | 13.984 | 10 | 172,498 (1.725) | yes | - |
| backlog-adp@program-4 | 0 | 13.035 | 9 | 174,508 (1.745) | yes | - |
| backlog-adp@program-5 | 0 | 13.427 | 11 | 172,035 (1.720) | yes | - |
| backlog-adp@program-6 | 0 | 13.158 | 10 | 171,062 (1.711) | yes | - |
| backlog-adp@program-7 | 0 | 13.376 | 9 | 159,992 (1.600) | yes | - |
| backlog-adp@verify-0 | 0 | 14.176 | 10 | 171,195 (1.712) | yes | - |
| backlog-adp@verify-1 | 0 | 14.137 | 10 | 166,488 (1.665) | yes | - |
| backlog-adp@verify-2 | 0 | 13.927 | 9 | 171,471 (1.715) | yes | - |
| backlog-adp@verify-3 | 0 | 13.833 | 9 | 173,111 (1.731) | yes | - |
| backlog-adp@verify-4 | 0 | 13.769 | 8 | 168,612 (1.686) | yes | - |
| backlog-adp@verify-5 | 0 | 15.191 | 11 | 166,374 (1.664) | yes | - |
| backlog-adp@verify-6 | 0 | 14.260 | 11 | 171,603 (1.716) | yes | - |
| backlog-adp@verify-7 | 0 | 14.173 | 10 | 176,363 (1.764) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 14.014 | 10 | 170,576 (1.706) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 13.776 | 8 | 175,174 (1.752) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 13.810 | 9 | 169,378 (1.694) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 14.203 | 11 | 173,002 (1.730) | yes | - |
| backlog-adp@blank-aged2-4 | 1 | 14.002 | 10 | 171,535 (1.715) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 15.019 | 11 | 171,277 (1.713) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 14.802 | 10 | 173,312 (1.733) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 14.782 | 8 | 168,477 (1.685) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 13.976 | 10 | 163,802 (1.638) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 14.013 | 10 | 170,636 (1.706) | yes | - |
| backlog-adp@blank-aged1-2 | 1 | 13.802 | 8 | 169,319 (1.693) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 13.779 | 9 | 171,621 (1.716) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 13.774 | 9 | 172,942 (1.729) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 15.192 | 12 | 166,297 (1.663) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 14.072 | 11 | 171,116 (1.711) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 13.811 | 9 | 170,030 (1.700) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 14.162 | 11 | 163,821 (1.638) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 14.064 | 10 | 165,999 (1.660) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 13.956 | 9 | 177,225 (1.772) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 13.942 | 10 | 170,589 (1.706) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 13.808 | 9 | 173,537 (1.735) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 14.019 | 9 | 172,453 (1.725) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 13.948 | 9 | 167,483 (1.675) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 14.606 | 11 | 174,876 (1.749) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 13.931 | 9 | 164,603 (1.646) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 13.793 | 9 | 164,040 (1.640) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 14.239 | 11 | 165,860 (1.659) | yes | - |
| backlog-adp@program-aged1-3 | 1 | 13.812 | 9 | 172,954 (1.730) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 13.940 | 10 | 170,524 (1.705) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 14.447 | 11 | 171,153 (1.712) | yes | - |
| backlog-adp@program-aged1-6 | 1 | 13.742 | 9 | 173,828 (1.738) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 14.546 | 11 | 171,461 (1.715) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 14.066 | 10 | 163,802 (1.638) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 13.846 | 10 | 173,085 (1.731) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 13.992 | 10 | 164,196 (1.642) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 13.876 | 9 | 171,597 (1.716) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 13.678 | 9 | 164,019 (1.640) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 14.953 | 11 | 166,336 (1.663) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 14.868 | 9 | 164,198 (1.642) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 14.838 | 10 | 164,435 (1.644) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 14.159 | 11 | 166,374 (1.664) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 14.230 | 11 | 163,821 (1.638) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 13.920 | 10 | 174,624 (1.746) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 13.889 | 10 | 172,515 (1.725) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 13.798 | 9 | 168,049 (1.680) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 15.425 | 12 | 164,040 (1.640) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 13.826 | 10 | 166,341 (1.663) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 14.293 | 10 | 164,401 (1.644) | yes | - |
| backlog | 0 | 11.300 | 8 | 192,237 (1.922) | yes | - |
| backlog-adp | 0 | 13.495 | 11 | 171,701 (1.717) | yes | - |
| backlog-adp-refill | 0 | 41.125 | 22 | 161,827 (1.618) | yes | - |
| backlog-owed | 0 | 360.442 | 52 | 169,488 (1.695) | yes | - |

Composed maximum over the 4 backlog windows: 192,237 CPU cycles (1.922 ms), backlog.
Over the windows that released their whole load only: 192,237 (1.922 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 122793 | 0 | 117,985 (1.180) | fits |
| save-held | 3005 | 0 | 173,397 (1.734) | fits |
| save-starved | 55635 | 0 | 173,156 (1.732) | fits |
| acmp-notk | 4874 | 0 | 117,985 (1.180) | fits |
| backlog-adp@blank-0 | 551 | 0 | 166,365 (1.664) | fits |
| backlog-adp@blank-1 | 551 | 0 | 163,821 (1.638) | fits |
| backlog-adp@blank-2 | 550 | 0 | 174,650 (1.746) | fits |
| backlog-adp@blank-3 | 550 | 0 | 172,565 (1.726) | fits |
| backlog-adp@blank-4 | 551 | 0 | 168,075 (1.681) | fits |
| backlog-adp@blank-5 | 552 | 0 | 164,267 (1.643) | fits |
| backlog-adp@blank-6 | 554 | 0 | 168,572 (1.686) | fits |
| backlog-adp@blank-7 | 553 | 0 | 172,802 (1.728) | fits |
| backlog-adp@program-0 | 923 | 0 | 166,900 (1.669) | fits |
| backlog-adp@program-1 | 923 | 0 | 168,248 (1.682) | fits |
| backlog-adp@program-2 | 925 | 0 | 163,802 (1.638) | fits |
| backlog-adp@program-3 | 924 | 0 | 172,498 (1.725) | fits |
| backlog-adp@program-4 | 926 | 0 | 174,508 (1.745) | fits |
| backlog-adp@program-5 | 928 | 0 | 172,035 (1.720) | fits |
| backlog-adp@program-6 | 927 | 0 | 171,062 (1.711) | fits |
| backlog-adp@program-7 | 929 | 0 | 159,992 (1.600) | fits |
| backlog-adp@verify-0 | 1285 | 0 | 171,195 (1.712) | fits |
| backlog-adp@verify-1 | 1285 | 0 | 166,488 (1.665) | fits |
| backlog-adp@verify-2 | 1286 | 0 | 171,471 (1.715) | fits |
| backlog-adp@verify-3 | 1286 | 0 | 173,111 (1.731) | fits |
| backlog-adp@verify-4 | 1286 | 0 | 174,314 (1.743) | fits |
| backlog-adp@verify-5 | 1288 | 0 | 166,374 (1.664) | fits |
| backlog-adp@verify-6 | 1288 | 0 | 171,603 (1.716) | fits |
| backlog-adp@verify-7 | 1287 | 0 | 176,363 (1.764) | fits |
| backlog-adp@blank-aged2-0 | 803 | 0 | 170,576 (1.706) | fits |
| backlog-adp@blank-aged2-1 | 808 | 0 | 175,174 (1.752) | fits |
| backlog-adp@blank-aged2-2 | 815 | 0 | 169,378 (1.694) | fits |
| backlog-adp@blank-aged2-3 | 824 | 0 | 173,002 (1.730) | fits |
| backlog-adp@blank-aged2-4 | 830 | 0 | 171,535 (1.715) | fits |
| backlog-adp@blank-aged2-5 | 837 | 0 | 171,277 (1.713) | fits |
| backlog-adp@blank-aged2-6 | 843 | 0 | 173,312 (1.733) | fits |
| backlog-adp@blank-aged2-7 | 848 | 0 | 168,477 (1.685) | fits |
| backlog-adp@blank-aged1-0 | 750 | 0 | 163,802 (1.638) | fits |
| backlog-adp@blank-aged1-1 | 757 | 0 | 170,636 (1.706) | fits |
| backlog-adp@blank-aged1-2 | 763 | 0 | 169,319 (1.693) | fits |
| backlog-adp@blank-aged1-3 | 769 | 0 | 171,621 (1.716) | fits |
| backlog-adp@blank-aged1-4 | 776 | 0 | 172,942 (1.729) | fits |
| backlog-adp@blank-aged1-5 | 785 | 0 | 166,297 (1.663) | fits |
| backlog-adp@blank-aged1-6 | 791 | 0 | 171,116 (1.711) | fits |
| backlog-adp@blank-aged1-7 | 796 | 0 | 170,030 (1.700) | fits |
| backlog-adp@program-aged2-0 | 1173 | 0 | 163,821 (1.638) | fits |
| backlog-adp@program-aged2-1 | 1179 | 0 | 165,999 (1.660) | fits |
| backlog-adp@program-aged2-2 | 1185 | 0 | 177,225 (1.772) | fits |
| backlog-adp@program-aged2-3 | 1192 | 0 | 170,589 (1.706) | fits |
| backlog-adp@program-aged2-4 | 1198 | 0 | 173,537 (1.735) | fits |
| backlog-adp@program-aged2-5 | 1205 | 0 | 172,453 (1.725) | fits |
| backlog-adp@program-aged2-6 | 1211 | 0 | 167,483 (1.675) | fits |
| backlog-adp@program-aged2-7 | 1220 | 0 | 174,876 (1.749) | fits |
| backlog-adp@program-aged1-0 | 1119 | 0 | 164,603 (1.646) | fits |
| backlog-adp@program-aged1-1 | 1125 | 0 | 164,040 (1.640) | fits |
| backlog-adp@program-aged1-2 | 1134 | 0 | 165,860 (1.659) | fits |
| backlog-adp@program-aged1-3 | 1139 | 0 | 172,954 (1.730) | fits |
| backlog-adp@program-aged1-4 | 1146 | 0 | 170,524 (1.705) | fits |
| backlog-adp@program-aged1-5 | 1154 | 0 | 171,153 (1.712) | fits |
| backlog-adp@program-aged1-6 | 1159 | 0 | 173,828 (1.738) | fits |
| backlog-adp@program-aged1-7 | 1167 | 0 | 171,461 (1.715) | fits |
| backlog-adp@verify-aged2-0 | 1538 | 0 | 163,802 (1.638) | fits |
| backlog-adp@verify-aged2-1 | 1544 | 0 | 173,085 (1.731) | fits |
| backlog-adp@verify-aged2-2 | 1551 | 0 | 164,196 (1.642) | fits |
| backlog-adp@verify-aged2-3 | 1557 | 0 | 171,597 (1.716) | fits |
| backlog-adp@verify-aged2-4 | 1563 | 0 | 164,019 (1.640) | fits |
| backlog-adp@verify-aged2-5 | 1572 | 0 | 166,336 (1.663) | fits |
| backlog-adp@verify-aged2-6 | 1577 | 0 | 164,198 (1.642) | fits |
| backlog-adp@verify-aged2-7 | 1584 | 0 | 164,435 (1.644) | fits |
| backlog-adp@verify-aged1-0 | 1486 | 0 | 166,374 (1.664) | fits |
| backlog-adp@verify-aged1-1 | 1493 | 0 | 163,821 (1.638) | fits |
| backlog-adp@verify-aged1-2 | 1498 | 0 | 174,624 (1.746) | fits |
| backlog-adp@verify-aged1-3 | 1505 | 0 | 172,515 (1.725) | fits |
| backlog-adp@verify-aged1-4 | 1511 | 0 | 168,049 (1.680) | fits |
| backlog-adp@verify-aged1-5 | 1520 | 0 | 164,040 (1.640) | fits |
| backlog-adp@verify-aged1-6 | 1525 | 0 | 166,341 (1.663) | fits |
| backlog-adp@verify-aged1-7 | 1532 | 0 | 164,401 (1.644) | fits |
| adp-advertise | 599 | 0 | 117,985 (1.180) | fits |
| maap | 366 | 0 | 117,748 (1.177) | fits |
| acmp-noresp | 2720 | 0 | 117,985 (1.180) | fits |
| save | 611 | 0 | 117,985 (1.180) | fits |
| srp | 306 | 0 | 187,289 (1.873) | fits |
| backlog | 288 | 0 | 192,237 (1.922) | fits |
| backlog-adp | 316 | 0 | 171,701 (1.717) | fits |
| backlog-adp-refill | 327 | 0 | 161,827 (1.618) | fits |
| backlog-owed | 340 | 0 | 169,488 (1.695) | fits |
| acmp-disc | 1390 | 0 | 118,210 (1.182) | fits |
| adp-link | 91 | 0 | 117,985 (1.180) | fits |
| adp-gm | 89 | 0 | 117,985 (1.180) | fits |
| adp-discover | 89 | 0 | 117,985 (1.180) | fits |
| control | 89 | 0 | 117,985 (1.180) | fits |
| aecp-fanout | 143 | 0 | 117,985 (1.180) | fits |
| acmp-cmd | 106 | 0 | 117,985 (1.180) | fits |
| aecp | 133 | 0 | 117,985 (1.180) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +11.375 ms, 77,633 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 13.412 (20) | 6.588 |
| backlog-adp@blank-aged2-1 | 2 | +11.122 ms, 77,517 (0.775 ms), read-back | none | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 13.172 (20) | 6.828 |
| backlog-adp@blank-aged2-2 | 2 | +9.605 ms, 77,638 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 13.203 (20) | 6.797 |
| backlog-adp@blank-aged2-3 | 2 | +8.185 ms, 77,701 (0.777 ms), read-back | none | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 13.281 (20) | 6.719 |
| backlog-adp@blank-aged2-4 | 2 | +6.580 ms, 77,563 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 13.080 (20) | 6.920 |
| backlog-adp@blank-aged2-5 | 2 | +4.943 ms, 77,519 (0.775 ms), read-back | none | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 13.388 (20) | 6.612 |
| backlog-adp@blank-aged2-6 | 2 | +5.179 ms, 77,526 (0.775 ms), read-back | none | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 13.441 (20) | 6.559 |
| backlog-adp@blank-aged2-7 | 2 | +4.862 ms, 77,436 (0.774 ms), read-back | none | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 13.414 (20) | 6.586 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.aecp.last.if1` | 12.609 (20) | 7.391 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.aecp.last.if1` | 12.650 (20) | 7.350 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.aecp.last.if1` | 12.435 (20) | 7.565 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.aecp.last.if1` | 12.414 (20) | 7.586 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.aecp.last.if1` | 12.410 (20) | 7.590 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.aecp.last.if1` | 12.302 (20) | 7.698 |
| backlog-adp@blank-aged1-6 | 1 | none | +12.907 ms, 77,091 (0.771 ms), read-back | `backlog-adp@blank-aged1-6.service.aecp.last.if1` | 12.618 (20) | 7.382 |
| backlog-adp@blank-aged1-7 | 1 | none | +12.637 ms, 77,510 (0.775 ms), read-back | `backlog-adp@blank-aged1-7.service.aecp.last.if1` | 12.625 (20) | 7.375 |
| backlog-adp@program-aged2-0 | 2 | +11.164 ms, 80,734 (0.807 ms), issue | none | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 13.237 (20) | 6.763 |
| backlog-adp@program-aged2-1 | 2 | +9.724 ms, 80,670 (0.807 ms), issue | none | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 13.461 (20) | 6.539 |
| backlog-adp@program-aged2-2 | 2 | +9.505 ms, 80,469 (0.805 ms), issue | none | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 13.353 (20) | 6.647 |
| backlog-adp@program-aged2-3 | 2 | +8.071 ms, 80,553 (0.806 ms), issue | none | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 13.334 (20) | 6.666 |
| backlog-adp@program-aged2-4 | 2 | +6.524 ms, 80,754 (0.808 ms), issue | none | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 13.206 (20) | 6.794 |
| backlog-adp@program-aged2-5 | 2 | +4.788 ms, 80,731 (0.807 ms), issue | none | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 13.098 (20) | 6.902 |
| backlog-adp@program-aged2-6 | 2 | +4.868 ms, 80,754 (0.808 ms), issue | none | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 13.293 (20) | 6.707 |
| backlog-adp@program-aged2-7 | 2 | +3.627 ms, 80,517 (0.805 ms), issue | none | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 13.479 (20) | 6.521 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.aecp.last.if1` | 12.526 (20) | 7.474 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.aecp.last.if1` | 12.392 (20) | 7.608 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.aecp.last.if1` | 12.518 (20) | 7.482 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.aecp.last.if1` | 12.413 (20) | 7.587 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.aecp.last.if1` | 12.536 (20) | 7.464 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.aecp.last.if1` | 12.541 (20) | 7.459 |
| backlog-adp@program-aged1-6 | 1 | none | +12.540 ms, 80,237 (0.802 ms), issue | `backlog-adp@program-aged1-6.service.aecp.last.if1` | 12.253 (20) | 7.747 |
| backlog-adp@program-aged1-7 | 1 | none | +12.665 ms, 80,405 (0.804 ms), issue | `backlog-adp@program-aged1-7.service.aecp.last.if1` | 12.654 (20) | 7.346 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 13.460 (20) | 6.540 |
| backlog-adp@verify-aged2-1 | 2 | +11.349 ms, 78,736 (0.787 ms), read-back | none | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 13.246 (20) | 6.754 |
| backlog-adp@verify-aged2-2 | 2 | none | none | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 13.385 (20) | 6.615 |
| backlog-adp@verify-aged2-3 | 2 | none | none | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 13.271 (20) | 6.729 |
| backlog-adp@verify-aged2-4 | 2 | none | none | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 13.072 (20) | 6.928 |
| backlog-adp@verify-aged2-5 | 2 | none | none | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 13.155 (20) | 6.845 |
| backlog-adp@verify-aged2-6 | 2 | +4.838 ms, 78,778 (0.788 ms), read-back | none | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 13.485 (20) | 6.515 |
| backlog-adp@verify-aged2-7 | 2 | none | none | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 13.454 (20) | 6.546 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.aecp.last.if1` | 12.469 (20) | 7.531 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.aecp.last.if1` | 12.535 (20) | 7.465 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.aecp.last.if1` | 12.546 (20) | 7.454 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.aecp.last.if1` | 12.516 (20) | 7.484 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.aecp.last.if1` | 12.422 (20) | 7.578 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.aecp.last.if1` | 12.299 (20) | 7.701 |
| backlog-adp@verify-aged1-6 | 1 | none | +12.648 ms, 78,214 (0.782 ms), read-back | `backlog-adp@verify-aged1-6.service.aecp.last.if1` | 12.361 (20) | 7.638 |
| backlog-adp@verify-aged1-7 | 1 | none | +12.582 ms, 78,752 (0.788 ms), read-back | `backlog-adp@verify-aged1-7.service.aecp.last.if1` | 12.570 (20) | 7.430 |

Least margin over the aged windows: 6.515 ms, `backlog-adp@verify-aged2-6.service.aecp.last.if1` at 13.485 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22110.079 | 22,150 | 370 | 2 | 32.734 | yes | within |
| save-held | 4697.145 | 12,110 | 370 | - | 14.607 | no | within |
| save-starved | 12088.523 | 12,110 | 370 | - | 35.367 | yes | within |
| save | 4697.801 | 12,110 | 370 | - | 13.519 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1056 | 80,435 (0.804) | 78,092 (0.781) |
| save-held | 1526 | 108,273 (1.083) | 78,657 (0.787) |
| save-starved | 686 | 80,512 (0.805) | 78,194 (0.782) |
| acmp-notk | 1065 | 109,040 (1.090) | 78,521 (0.785) |
| backlog-adp@blank-0 | 337 | 95,760 (0.958) | 76,345 (0.763) |
| backlog-adp@blank-1 | 337 | 95,435 (0.954) | 76,362 (0.764) |
| backlog-adp@blank-2 | 337 | 95,745 (0.957) | 76,408 (0.764) |
| backlog-adp@blank-3 | 337 | 95,632 (0.956) | 76,362 (0.764) |
| backlog-adp@blank-4 | 337 | 95,884 (0.959) | 76,362 (0.764) |
| backlog-adp@blank-5 | 338 | 95,956 (0.960) | 76,395 (0.764) |
| backlog-adp@blank-6 | 337 | 95,000 (0.950) | 76,302 (0.763) |
| backlog-adp@blank-7 | 337 | 101,718 (1.017) | 76,277 (0.763) |
| backlog-adp@program-0 | 443 | 105,091 (1.051) | 78,675 (0.787) |
| backlog-adp@program-1 | 443 | 105,091 (1.051) | 78,642 (0.786) |
| backlog-adp@program-2 | 444 | 105,091 (1.051) | 78,751 (0.788) |
| backlog-adp@program-3 | 443 | 105,091 (1.051) | 78,645 (0.786) |
| backlog-adp@program-4 | 444 | 105,091 (1.051) | 78,220 (0.782) |
| backlog-adp@program-5 | 444 | 105,091 (1.051) | 78,220 (0.782) |
| backlog-adp@program-6 | 444 | 105,091 (1.051) | 78,220 (0.782) |
| backlog-adp@program-7 | 444 | 105,091 (1.051) | 78,220 (0.782) |
| backlog-adp@verify-0 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-1 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-2 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-3 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-4 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-5 | 547 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-6 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-7 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@blank-aged2-0 | 335 | 77,633 (0.776) | 76,340 (0.763) |
| backlog-adp@blank-aged2-1 | 335 | 77,517 (0.775) | 76,224 (0.762) |
| backlog-adp@blank-aged2-2 | 335 | 77,638 (0.776) | 76,277 (0.763) |
| backlog-adp@blank-aged2-3 | 335 | 77,701 (0.777) | 76,340 (0.763) |
| backlog-adp@blank-aged2-4 | 335 | 77,563 (0.776) | 76,283 (0.763) |
| backlog-adp@blank-aged2-5 | 336 | 94,704 (0.947) | 76,317 (0.763) |
| backlog-adp@blank-aged2-6 | 336 | 95,415 (0.954) | 76,320 (0.763) |
| backlog-adp@blank-aged2-7 | 336 | 96,188 (0.962) | 76,378 (0.764) |
| backlog-adp@blank-aged1-0 | 335 | 96,045 (0.960) | 76,409 (0.764) |
| backlog-adp@blank-aged1-1 | 335 | 95,664 (0.957) | 76,363 (0.764) |
| backlog-adp@blank-aged1-2 | 335 | 96,031 (0.960) | 76,363 (0.764) |
| backlog-adp@blank-aged1-3 | 335 | 95,819 (0.958) | 76,363 (0.764) |
| backlog-adp@blank-aged1-4 | 335 | 95,707 (0.957) | 76,363 (0.764) |
| backlog-adp@blank-aged1-5 | 336 | 95,329 (0.953) | 76,363 (0.764) |
| backlog-adp@blank-aged1-6 | 335 | 77,091 (0.771) | 76,170 (0.762) |
| backlog-adp@blank-aged1-7 | 335 | 77,510 (0.775) | 76,287 (0.763) |
| backlog-adp@program-aged2-0 | 441 | 105,091 (1.051) | 78,556 (0.786) |
| backlog-adp@program-aged2-1 | 441 | 105,091 (1.051) | 78,424 (0.784) |
| backlog-adp@program-aged2-2 | 441 | 105,091 (1.051) | 78,297 (0.783) |
| backlog-adp@program-aged2-3 | 441 | 105,091 (1.051) | 78,550 (0.785) |
| backlog-adp@program-aged2-4 | 441 | 105,091 (1.051) | 78,595 (0.786) |
| backlog-adp@program-aged2-5 | 442 | 105,091 (1.051) | 78,553 (0.786) |
| backlog-adp@program-aged2-6 | 442 | 105,091 (1.051) | 78,595 (0.786) |
| backlog-adp@program-aged2-7 | 442 | 105,091 (1.051) | 78,271 (0.783) |
| backlog-adp@program-aged1-0 | 441 | 105,091 (1.051) | 78,642 (0.786) |
| backlog-adp@program-aged1-1 | 441 | 105,091 (1.051) | 78,675 (0.787) |
| backlog-adp@program-aged1-2 | 441 | 105,091 (1.051) | 78,705 (0.787) |
| backlog-adp@program-aged1-3 | 441 | 105,091 (1.051) | 78,751 (0.788) |
| backlog-adp@program-aged1-4 | 441 | 105,091 (1.051) | 78,705 (0.787) |
| backlog-adp@program-aged1-5 | 442 | 105,091 (1.051) | 78,705 (0.787) |
| backlog-adp@program-aged1-6 | 441 | 105,091 (1.051) | 78,465 (0.785) |
| backlog-adp@program-aged1-7 | 441 | 105,091 (1.051) | 78,297 (0.783) |
| backlog-adp@verify-aged2-0 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged2-1 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged2-2 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged2-3 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged2-4 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged2-5 | 547 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged2-6 | 547 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged2-7 | 547 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged1-0 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged1-1 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged1-2 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged1-3 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged1-4 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged1-5 | 547 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged1-6 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| backlog-adp@verify-aged1-7 | 546 | 105,091 (1.051) | 78,373 (0.784) |
| adp-advertise | 577 | 31,014 (0.310) | 3,002 (0.030) |
| maap | 344 | 30,918 (0.309) | 2,970 (0.030) |
| acmp-noresp | 615 | 108,881 (1.089) | 78,523 (0.785) |
| save | 585 | 107,587 (1.076) | 78,489 (0.785) |
| srp | 278 | 30,861 (0.309) | 3,276 (0.033) |
| backlog | 266 | 30,944 (0.309) | 3,126 (0.031) |
| backlog-adp | 272 | 30,944 (0.309) | 3,063 (0.031) |
| backlog-adp-refill | 274 | 30,944 (0.309) | 3,063 (0.031) |
| backlog-owed | 306 | 38,088 (0.381) | 3,129 (0.031) |
| acmp-disc | 336 | 105,915 (1.059) | 78,220 (0.782) |
| adp-link | 79 | 30,835 (0.308) | 3,002 (0.030) |
| adp-gm | 79 | 30,835 (0.308) | 3,002 (0.030) |
| adp-discover | 79 | 30,835 (0.308) | 3,002 (0.030) |
| control | 79 | 30,835 (0.308) | 3,002 (0.030) |
| aecp-fanout | 93 | 30,835 (0.308) | 3,002 (0.030) |
| acmp-cmd | 67 | 30,835 (0.308) | 3,002 (0.030) |
| aecp | 88 | 30,835 (0.308) | 4,122 (0.041) |

Longest pass that carries a step: 109,040 CPU cycles (1.090 ms), acmp-notk; longest step: 78,751 (0.788 ms), backlog-adp@program-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 792,628 | 7.926 | 20 | 200 | fits | 173,397 | 135 | 0.546 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 1,091,484 | 10.915 | 20 | 20 | fits | 158,178 | 86 | 0.520 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 668,906 | 6.689 | 20 | 24 | fits | 97,626 | 86 | 0.444 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 893,831 | 8.938 | 20 | 50 | fits | 160,815 | 100 | 0.609 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 587,320 | 5.873 | 20 | 20 | fits | 141,747 | 49 | 0.532 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 195,004 | 1.950 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if1` | 303,716 | 3.037 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 267,935 | 2.679 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if1` | 502,871 | 5.029 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 297,588 | 2.976 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if1` | 550,149 | 5.501 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 940,311 | 9.403 | 20 | 200 | fits | 156,499 | 125 | 0.552 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 1,082,705 | 10.827 | 20 | 20 | fits | 162,531 | 75 | 0.586 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 690,584 | 6.906 | 20 | 24 | fits | 128,083 | 118 | 0.439 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 1,001,856 | 10.019 | 20 | 50 | fits | 150,229 | 109 | 0.533 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 593,915 | 5.939 | 20 | 20 | fits | 145,923 | 61 | 0.551 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 186,852 | 1.869 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if1` | 295,541 | 2.955 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 271,727 | 2.717 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if1` | 511,281 | 5.113 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 299,964 | 3.000 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if1` | 557,142 | 5.571 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 13,884 | 0.139 | 20 | 20 | fits | 52,439 | 29 (14) | 0.783 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 24,908 | 0.249 | 20 | 20 | fits | 52,858 | 19 (14) | 0.894 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 891,239 | 8.912 | 20 | 20 | fits | 166,365 | 107 | 0.572 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 239,512 | 2.395 | 20 | 200 | fits | 164,724 | 155 | 0.552 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 1,047,628 | 10.476 | 20 | 200 | fits | 166,365 | 107 | 0.572 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 240,424 | 2.404 | 20 | 20 | fits | 164,724 | 155 | 0.552 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 1,202,184 | 12.022 | 20 | 20 | fits | 153,860 | 68 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 244,009 | 2.440 | 20 | 24 | fits | 164,724 | 155 | 0.552 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,317,772 | 13.178 | 20 | 24 | fits | 112,153 | 99 | 0.445 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 242,969 | 2.430 | 20 | 50 | fits | 164,724 | 155 | 0.552 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 1,051,304 | 10.513 | 20 | 50 | fits | 166,365 | 107 | 0.572 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 401,389 | 4.014 | 20 | 20 | fits | 158,875 | 79 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 717,465 | 7.175 | 20 | 20 | fits | 155,812 | 59 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 981,160 | 9.812 | 20 | 20 | fits | 161,244 | 69 | 0.641 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 167,971 | 1.680 | 20 | 200 | fits | 159,242 | 176 | 0.534 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 1,124,603 | 11.246 | 20 | 200 | fits | 161,244 | 69 | 0.641 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 168,883 | 1.689 | 20 | 20 | fits | 159,242 | 176 | 0.534 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 1,252,740 | 12.527 | 20 | 20 | fits | 127,441 | 94 | 0.494 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 172,468 | 1.725 | 20 | 24 | fits | 159,242 | 176 | 0.534 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,256,175 | 12.562 | 20 | 24 | fits | 127,441 | 94 | 0.494 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 171,428 | 1.714 | 20 | 50 | fits | 159,242 | 176 | 0.534 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 967,035 | 9.670 | 20 | 50 | fits | 163,821 | 114 | 0.543 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 329,794 | 3.298 | 20 | 20 | fits | 158,821 | 79 | 0.665 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 647,074 | 6.471 | 20 | 20 | fits | 152,731 | 53 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 876,181 | 8.762 | 20 | 20 | fits | 174,650 | 93 | 0.623 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 174,429 | 1.744 | 20 | 200 | fits | 174,258 | 177 | 0.536 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 977,006 | 9.770 | 20 | 200 | fits | 174,650 | 93 | 0.623 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 175,341 | 1.753 | 20 | 20 | fits | 174,258 | 177 | 0.536 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 1,142,174 | 11.422 | 20 | 20 | fits | 164,472 | 70 | 0.579 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 178,926 | 1.789 | 20 | 24 | fits | 174,258 | 177 | 0.536 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,260,384 | 12.604 | 20 | 24 | fits | 103,916 | 92 | 0.494 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 177,886 | 1.779 | 20 | 50 | fits | 174,258 | 177 | 0.536 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 980,682 | 9.807 | 20 | 50 | fits | 174,650 | 93 | 0.623 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 336,447 | 3.364 | 20 | 20 | fits | 159,016 | 80 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 652,867 | 6.529 | 20 | 20 | fits | 150,683 | 53 | 0.477 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 918,502 | 9.185 | 20 | 20 | fits | 172,565 | 112 | 0.582 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 176,000 | 1.760 | 20 | 200 | fits | 164,980 | 156 | 0.553 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 980,016 | 9.800 | 20 | 200 | fits | 172,565 | 112 | 0.582 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 176,912 | 1.769 | 20 | 20 | fits | 164,980 | 156 | 0.553 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 1,144,564 | 11.446 | 20 | 20 | fits | 153,082 | 87 | 0.614 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 180,497 | 1.805 | 20 | 24 | fits | 164,980 | 156 | 0.553 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,260,467 | 12.605 | 20 | 24 | fits | 112,468 | 99 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 179,457 | 1.795 | 20 | 50 | fits | 164,980 | 156 | 0.553 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 1,147,544 | 11.475 | 20 | 50 | fits | 153,082 | 87 | 0.614 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 509,891 | 5.099 | 20 | 20 | fits | 161,699 | 41 | 0.692 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 809,047 | 8.090 | 20 | 20 | fits | 150,019 | 55 | 0.525 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 1,017,382 | 10.174 | 20 | 20 | fits | 168,075 | 94 | 0.599 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 174,238 | 1.742 | 20 | 200 | fits | 163,285 | 151 | 0.563 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 1,141,710 | 11.417 | 20 | 200 | fits | 168,075 | 94 | 0.599 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 175,150 | 1.752 | 20 | 20 | fits | 163,285 | 151 | 0.563 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 1,142,406 | 11.424 | 20 | 20 | fits | 168,075 | 94 | 0.599 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 178,735 | 1.787 | 20 | 24 | fits | 163,285 | 151 | 0.563 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,246,942 | 12.469 | 20 | 24 | fits | 101,101 | 86 | 0.468 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 177,695 | 1.777 | 20 | 50 | fits | 163,285 | 151 | 0.563 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 1,145,386 | 11.454 | 20 | 50 | fits | 168,075 | 94 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 336,220 | 3.362 | 20 | 20 | fits | 158,980 | 79 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 644,867 | 6.449 | 20 | 20 | fits | 159,874 | 59 | 0.506 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 971,049 | 9.710 | 20 | 20 | fits | 156,316 | 73 | 0.597 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 161,373 | 1.614 | 20 | 200 | fits | 158,978 | 176 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 1,118,443 | 11.184 | 20 | 200 | fits | 156,316 | 73 | 0.597 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 162,285 | 1.623 | 20 | 20 | fits | 158,978 | 176 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 1,234,155 | 12.342 | 20 | 20 | fits | 115,016 | 79 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 165,870 | 1.659 | 20 | 24 | fits | 158,978 | 176 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,237,590 | 12.376 | 20 | 24 | fits | 115,016 | 79 | 0.524 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 164,830 | 1.648 | 20 | 50 | fits | 158,978 | 176 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 965,803 | 9.658 | 20 | 50 | fits | 164,267 | 114 | 0.553 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 322,968 | 3.230 | 20 | 20 | fits | 158,593 | 79 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 631,689 | 6.317 | 20 | 20 | fits | 150,341 | 53 | 0.472 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 444,178 | 4.442 | 20 | 20 | fits | 168,572 | 150 | 0.577 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 154,921 | 1.549 | 20 | 200 | fits | 161,084 | 122 | 0.584 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 482,090 | 4.821 | 20 | 200 | fits | 168,572 | 150 | 0.577 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 155,833 | 1.558 | 20 | 20 | fits | 161,084 | 122 | 0.584 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 1,245,138 | 12.451 | 20 | 20 | fits | 137,438 | 86 | 0.511 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 159,418 | 1.594 | 20 | 24 | fits | 161,084 | 122 | 0.584 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,248,573 | 12.486 | 20 | 24 | fits | 137,438 | 86 | 0.511 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 158,378 | 1.584 | 20 | 50 | fits | 161,084 | 122 | 0.584 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 1,110,680 | 11.107 | 20 | 50 | fits | 154,508 | 82 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 647,322 | 6.473 | 20 | 20 | fits | 161,621 | 42 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 954,092 | 9.541 | 20 | 20 | fits | 140,551 | 49 | 0.489 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 922,980 | 9.230 | 20 | 20 | fits | 172,365 | 111 | 0.583 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 169,400 | 1.694 | 20 | 200 | fits | 164,714 | 155 | 0.553 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 984,443 | 9.844 | 20 | 200 | fits | 172,365 | 111 | 0.583 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 170,312 | 1.703 | 20 | 20 | fits | 164,714 | 155 | 0.553 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 1,147,720 | 11.477 | 20 | 20 | fits | 162,581 | 94 | 0.570 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 173,897 | 1.739 | 20 | 24 | fits | 164,714 | 155 | 0.553 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,262,808 | 12.628 | 20 | 24 | fits | 111,653 | 95 | 0.468 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 172,857 | 1.729 | 20 | 50 | fits | 164,714 | 155 | 0.553 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 1,150,700 | 11.507 | 20 | 50 | fits | 162,581 | 94 | 0.570 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 507,044 | 5.070 | 20 | 20 | fits | 161,840 | 42 | 0.692 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 813,674 | 8.137 | 20 | 20 | fits | 140,480 | 49 | 0.488 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 978,698 | 9.787 | 20 | 20 | fits | 161,203 | 69 | 0.640 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 171,733 | 1.717 | 20 | 200 | fits | 159,468 | 176 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 1,121,836 | 11.218 | 20 | 200 | fits | 161,203 | 69 | 0.640 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 172,645 | 1.726 | 20 | 20 | fits | 159,468 | 176 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 1,249,962 | 12.500 | 20 | 20 | fits | 127,430 | 93 | 0.494 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 176,230 | 1.762 | 20 | 24 | fits | 159,468 | 176 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,253,397 | 12.534 | 20 | 24 | fits | 127,430 | 93 | 0.494 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 175,190 | 1.752 | 20 | 50 | fits | 159,468 | 176 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 964,309 | 9.643 | 20 | 50 | fits | 166,900 | 120 | 0.562 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 331,809 | 3.318 | 20 | 20 | fits | 157,074 | 79 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 630,770 | 6.308 | 20 | 20 | fits | 150,204 | 53 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 893,544 | 8.935 | 20 | 20 | fits | 168,248 | 110 | 0.566 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 160,080 | 1.601 | 20 | 200 | fits | 164,964 | 155 | 0.551 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 954,414 | 9.544 | 20 | 200 | fits | 168,248 | 110 | 0.566 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 160,992 | 1.610 | 20 | 20 | fits | 164,964 | 155 | 0.551 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 1,119,874 | 11.199 | 20 | 20 | fits | 164,764 | 69 | 0.582 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 164,577 | 1.646 | 20 | 24 | fits | 164,964 | 155 | 0.551 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,237,145 | 12.371 | 20 | 24 | fits | 113,836 | 99 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 163,537 | 1.635 | 20 | 50 | fits | 164,964 | 155 | 0.551 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 958,090 | 9.581 | 20 | 50 | fits | 168,248 | 110 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 320,459 | 3.205 | 20 | 20 | fits | 157,377 | 79 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 619,628 | 6.196 | 20 | 20 | fits | 150,371 | 54 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 967,972 | 9.680 | 20 | 20 | fits | 156,247 | 74 | 0.595 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 156,908 | 1.569 | 20 | 200 | fits | 159,501 | 176 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 1,115,612 | 11.156 | 20 | 200 | fits | 156,247 | 74 | 0.595 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 157,820 | 1.578 | 20 | 20 | fits | 159,501 | 176 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 1,246,373 | 12.464 | 20 | 20 | fits | 119,632 | 85 | 0.558 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 161,405 | 1.614 | 20 | 24 | fits | 159,501 | 176 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,249,808 | 12.498 | 20 | 24 | fits | 119,632 | 85 | 0.558 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 160,365 | 1.604 | 20 | 50 | fits | 159,501 | 176 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 963,041 | 9.630 | 20 | 50 | fits | 163,802 | 114 | 0.542 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 317,079 | 3.171 | 20 | 20 | fits | 157,169 | 80 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 643,072 | 6.431 | 20 | 20 | fits | 160,166 | 59 | 0.508 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 904,158 | 9.042 | 20 | 20 | fits | 172,498 | 112 | 0.582 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 164,989 | 1.650 | 20 | 200 | fits | 165,291 | 156 | 0.552 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 965,612 | 9.656 | 20 | 200 | fits | 172,498 | 112 | 0.582 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 165,901 | 1.659 | 20 | 20 | fits | 165,291 | 156 | 0.552 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 1,129,980 | 11.300 | 20 | 20 | fits | 152,970 | 87 | 0.613 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 169,486 | 1.695 | 20 | 24 | fits | 165,291 | 156 | 0.552 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,258,584 | 12.586 | 20 | 24 | fits | 125,169 | 108 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 168,446 | 1.684 | 20 | 50 | fits | 165,291 | 156 | 0.552 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 1,132,960 | 11.330 | 20 | 50 | fits | 152,970 | 87 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 495,681 | 4.957 | 20 | 20 | fits | 158,544 | 43 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 794,710 | 7.947 | 20 | 20 | fits | 150,276 | 53 | 0.470 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 891,843 | 8.918 | 20 | 20 | fits | 157,838 | 90 | 0.576 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 172,466 | 1.725 | 20 | 200 | fits | 174,508 | 177 | 0.536 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 951,719 | 9.517 | 20 | 200 | fits | 157,838 | 90 | 0.576 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 173,378 | 1.734 | 20 | 20 | fits | 174,508 | 177 | 0.536 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 1,234,399 | 12.344 | 20 | 20 | fits | 128,070 | 93 | 0.499 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 176,963 | 1.770 | 20 | 24 | fits | 174,508 | 177 | 0.536 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,237,834 | 12.378 | 20 | 24 | fits | 128,070 | 93 | 0.499 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 175,923 | 1.759 | 20 | 50 | fits | 174,508 | 177 | 0.536 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 955,395 | 9.554 | 20 | 50 | fits | 157,838 | 90 | 0.576 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 332,788 | 3.328 | 20 | 20 | fits | 157,320 | 79 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 631,996 | 6.320 | 20 | 20 | fits | 150,371 | 54 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 1,015,691 | 10.157 | 20 | 20 | fits | 167,608 | 94 | 0.595 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 163,509 | 1.635 | 20 | 200 | fits | 163,260 | 151 | 0.561 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 1,140,080 | 11.401 | 20 | 200 | fits | 167,608 | 94 | 0.595 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 164,421 | 1.644 | 20 | 20 | fits | 163,260 | 151 | 0.561 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 1,140,776 | 11.408 | 20 | 20 | fits | 167,608 | 94 | 0.595 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 168,006 | 1.680 | 20 | 24 | fits | 163,260 | 151 | 0.561 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,245,115 | 12.451 | 20 | 24 | fits | 100,904 | 87 | 0.466 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 166,966 | 1.670 | 20 | 50 | fits | 163,260 | 151 | 0.561 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 1,143,756 | 11.438 | 20 | 50 | fits | 167,608 | 94 | 0.595 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 323,952 | 3.240 | 20 | 20 | fits | 157,441 | 79 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 641,324 | 6.413 | 20 | 20 | fits | 152,811 | 53 | 0.522 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 809,757 | 8.098 | 20 | 20 | fits | 171,062 | 109 | 0.588 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 167,540 | 1.675 | 20 | 200 | fits | 165,000 | 156 | 0.552 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 969,915 | 9.699 | 20 | 200 | fits | 171,062 | 109 | 0.588 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 168,452 | 1.685 | 20 | 20 | fits | 165,000 | 156 | 0.552 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 1,134,495 | 11.345 | 20 | 20 | fits | 153,043 | 88 | 0.611 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 172,037 | 1.720 | 20 | 24 | fits | 165,000 | 156 | 0.552 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,250,253 | 12.503 | 20 | 24 | fits | 112,323 | 99 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 170,997 | 1.710 | 20 | 50 | fits | 165,000 | 156 | 0.552 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 1,137,475 | 11.375 | 20 | 50 | fits | 153,043 | 88 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 501,177 | 5.012 | 20 | 20 | fits | 159,928 | 41 | 0.691 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 800,449 | 8.004 | 20 | 20 | fits | 140,149 | 49 | 0.482 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 428,622 | 4.286 | 20 | 20 | fits | 158,953 | 129 | 0.592 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 151,978 | 1.520 | 20 | 200 | fits | 158,291 | 136 | 0.554 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 465,703 | 4.657 | 20 | 200 | fits | 158,953 | 129 | 0.592 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 152,890 | 1.529 | 20 | 20 | fits | 158,291 | 136 | 0.554 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 1,241,213 | 12.412 | 20 | 20 | fits | 150,344 | 75 | 0.555 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 156,475 | 1.565 | 20 | 24 | fits | 158,291 | 136 | 0.554 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,244,648 | 12.446 | 20 | 24 | fits | 150,344 | 75 | 0.555 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 155,435 | 1.554 | 20 | 50 | fits | 158,291 | 136 | 0.554 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 469,379 | 4.694 | 20 | 50 | fits | 158,953 | 129 | 0.592 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 629,306 | 6.293 | 20 | 20 | fits | 159,992 | 42 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 936,126 | 9.361 | 20 | 20 | fits | 140,551 | 49 | 0.489 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 819,563 | 8.196 | 20 | 20 | fits | 171,195 | 108 | 0.594 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 185,440 | 1.854 | 20 | 200 | fits | 164,906 | 155 | 0.553 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 980,026 | 9.800 | 20 | 200 | fits | 171,195 | 108 | 0.594 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 186,352 | 1.864 | 20 | 20 | fits | 164,906 | 155 | 0.553 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 1,135,338 | 11.353 | 20 | 20 | fits | 154,616 | 80 | 0.631 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 189,937 | 1.899 | 20 | 24 | fits | 164,906 | 155 | 0.553 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,280,137 | 12.801 | 20 | 24 | fits | 130,356 | 118 | 0.464 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 188,897 | 1.889 | 20 | 50 | fits | 164,906 | 155 | 0.553 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 1,138,318 | 11.383 | 20 | 50 | fits | 154,616 | 80 | 0.631 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 520,807 | 5.208 | 20 | 20 | fits | 161,729 | 41 | 0.696 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 810,427 | 8.104 | 20 | 20 | fits | 140,104 | 49 | 0.481 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 927,261 | 9.273 | 20 | 20 | fits | 166,488 | 110 | 0.624 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 177,504 | 1.775 | 20 | 200 | fits | 165,051 | 156 | 0.553 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 965,355 | 9.654 | 20 | 200 | fits | 166,488 | 110 | 0.624 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 178,416 | 1.784 | 20 | 20 | fits | 165,051 | 156 | 0.553 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 1,272,470 | 12.725 | 20 | 20 | fits | 142,964 | 106 | 0.503 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 182,001 | 1.820 | 20 | 24 | fits | 165,051 | 156 | 0.553 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,275,905 | 12.759 | 20 | 24 | fits | 142,964 | 106 | 0.503 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 180,961 | 1.810 | 20 | 50 | fits | 165,051 | 156 | 0.553 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 1,122,051 | 11.221 | 20 | 50 | fits | 153,020 | 88 | 0.604 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 511,215 | 5.112 | 20 | 20 | fits | 161,479 | 41 | 0.692 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 800,463 | 8.005 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 1,025,678 | 10.257 | 20 | 20 | fits | 168,047 | 94 | 0.599 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 175,559 | 1.756 | 20 | 200 | fits | 163,236 | 151 | 0.562 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 1,150,029 | 11.500 | 20 | 200 | fits | 168,047 | 94 | 0.599 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 176,471 | 1.765 | 20 | 20 | fits | 163,236 | 151 | 0.562 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 1,150,725 | 11.507 | 20 | 20 | fits | 168,047 | 94 | 0.599 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 180,056 | 1.801 | 20 | 24 | fits | 163,236 | 151 | 0.562 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,255,261 | 12.553 | 20 | 24 | fits | 101,101 | 86 | 0.468 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 179,016 | 1.790 | 20 | 50 | fits | 163,236 | 151 | 0.562 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 1,153,705 | 11.537 | 20 | 50 | fits | 168,047 | 94 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 337,354 | 3.374 | 20 | 20 | fits | 158,793 | 79 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 636,427 | 6.364 | 20 | 20 | fits | 150,204 | 53 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 979,133 | 9.791 | 20 | 20 | fits | 156,325 | 73 | 0.598 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 162,898 | 1.629 | 20 | 200 | fits | 159,133 | 176 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 1,126,622 | 11.266 | 20 | 200 | fits | 156,325 | 73 | 0.598 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 163,810 | 1.638 | 20 | 20 | fits | 159,133 | 176 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 1,242,334 | 12.423 | 20 | 20 | fits | 115,016 | 79 | 0.524 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 167,395 | 1.674 | 20 | 24 | fits | 159,133 | 176 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,245,769 | 12.458 | 20 | 24 | fits | 115,016 | 79 | 0.524 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 166,355 | 1.664 | 20 | 50 | fits | 159,133 | 176 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 973,973 | 9.740 | 20 | 50 | fits | 164,304 | 114 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 324,306 | 3.243 | 20 | 20 | fits | 158,406 | 79 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 623,338 | 6.233 | 20 | 20 | fits | 150,204 | 53 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 909,233 | 9.092 | 20 | 20 | fits | 168,612 | 111 | 0.562 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 169,521 | 1.695 | 20 | 200 | fits | 174,314 | 177 | 0.535 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 969,478 | 9.695 | 20 | 200 | fits | 168,612 | 111 | 0.562 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 170,433 | 1.704 | 20 | 20 | fits | 174,314 | 177 | 0.535 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 1,135,142 | 11.351 | 20 | 20 | fits | 164,968 | 69 | 0.584 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 174,018 | 1.740 | 20 | 24 | fits | 174,314 | 177 | 0.535 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,239,379 | 12.394 | 20 | 24 | fits | 100,802 | 86 | 0.464 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 172,978 | 1.730 | 20 | 50 | fits | 174,314 | 177 | 0.535 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 973,154 | 9.732 | 20 | 50 | fits | 168,612 | 111 | 0.562 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 331,112 | 3.311 | 20 | 20 | fits | 158,589 | 79 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 802,462 | 8.025 | 20 | 20 | fits | 157,480 | 106 | 0.601 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 822,418 | 8.224 | 20 | 20 | fits | 166,374 | 108 | 0.570 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 170,721 | 1.707 | 20 | 200 | fits | 164,665 | 155 | 0.552 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 978,812 | 9.788 | 20 | 200 | fits | 166,374 | 108 | 0.570 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 171,633 | 1.716 | 20 | 20 | fits | 164,665 | 155 | 0.552 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 1,141,598 | 11.416 | 20 | 20 | fits | 162,090 | 94 | 0.564 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 175,218 | 1.752 | 20 | 24 | fits | 164,665 | 155 | 0.552 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,243,545 | 12.435 | 20 | 24 | fits | 98,512 | 86 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 174,178 | 1.742 | 20 | 50 | fits | 164,665 | 155 | 0.552 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 1,144,578 | 11.446 | 20 | 50 | fits | 162,090 | 94 | 0.564 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 332,515 | 3.325 | 20 | 20 | fits | 158,792 | 79 | 0.671 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 658,385 | 6.584 | 20 | 20 | fits | 155,777 | 59 | 0.538 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 989,431 | 9.894 | 20 | 20 | fits | 171,603 | 98 | 0.598 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 160,734 | 1.607 | 20 | 200 | fits | 163,236 | 151 | 0.562 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 1,114,206 | 11.142 | 20 | 200 | fits | 171,603 | 98 | 0.598 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 161,646 | 1.616 | 20 | 20 | fits | 163,236 | 151 | 0.562 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 1,257,815 | 12.578 | 20 | 20 | fits | 132,028 | 99 | 0.528 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 165,231 | 1.652 | 20 | 24 | fits | 163,236 | 151 | 0.562 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,261,250 | 12.613 | 20 | 24 | fits | 132,028 | 99 | 0.528 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 164,191 | 1.642 | 20 | 50 | fits | 163,236 | 151 | 0.562 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 1,117,882 | 11.179 | 20 | 50 | fits | 171,603 | 98 | 0.598 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 500,848 | 5.008 | 20 | 20 | fits | 164,133 | 47 | 0.699 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 790,467 | 7.905 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 855,519 | 8.555 | 20 | 20 | fits | 170,350 | 109 | 0.584 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 182,908 | 1.829 | 20 | 200 | fits | 174,561 | 178 | 0.536 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 995,302 | 9.953 | 20 | 200 | fits | 170,350 | 109 | 0.584 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 183,820 | 1.838 | 20 | 20 | fits | 174,561 | 178 | 0.536 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 1,164,239 | 11.642 | 20 | 20 | fits | 157,346 | 74 | 0.627 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 187,405 | 1.874 | 20 | 24 | fits | 174,561 | 178 | 0.536 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,280,067 | 12.801 | 20 | 24 | fits | 112,393 | 99 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 186,365 | 1.864 | 20 | 50 | fits | 174,561 | 178 | 0.536 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 998,978 | 9.990 | 20 | 50 | fits | 170,350 | 109 | 0.584 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 537,108 | 5.371 | 20 | 20 | fits | 164,181 | 47 | 0.694 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 826,548 | 8.265 | 20 | 20 | fits | 140,112 | 49 | 0.481 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 804,100 | 8.041 | 20 | 20 | fits | 170,576 | 109 | 0.587 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 170,261 | 1.703 | 20 | 200 | fits | 163,681 | 150 | 0.550 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 963,944 | 9.639 | 20 | 200 | fits | 170,576 | 109 | 0.587 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 171,173 | 1.712 | 20 | 20 | fits | 163,681 | 150 | 0.550 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 1,132,879 | 11.329 | 20 | 20 | fits | 157,462 | 85 | 0.639 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 174,758 | 1.748 | 20 | 24 | fits | 163,681 | 150 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 1,341,183 | 13.412 | 20 | 24 | fits | 127,236 | 112 | 0.443 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 173,718 | 1.737 | 20 | 50 | fits | 163,681 | 150 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 1,135,859 | 11.359 | 20 | 50 | fits | 157,462 | 85 | 0.639 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 505,787 | 5.058 | 20 | 20 | fits | 161,563 | 41 | 0.691 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 794,964 | 7.950 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 891,251 | 8.913 | 20 | 20 | fits | 175,174 | 116 | 0.598 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 148,620 | 1.486 | 20 | 200 | fits | 157,077 | 131 | 0.563 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 952,707 | 9.527 | 20 | 200 | fits | 175,174 | 116 | 0.598 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 149,532 | 1.495 | 20 | 20 | fits | 157,077 | 131 | 0.563 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 1,313,731 | 13.137 | 20 | 20 | fits | 128,572 | 93 | 0.508 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 153,117 | 1.531 | 20 | 24 | fits | 157,077 | 131 | 0.563 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 1,317,166 | 13.172 | 20 | 24 | fits | 128,572 | 93 | 0.508 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 152,077 | 1.521 | 20 | 50 | fits | 157,077 | 131 | 0.563 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 956,383 | 9.564 | 20 | 50 | fits | 175,174 | 116 | 0.598 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 468,484 | 4.685 | 20 | 20 | fits | 158,855 | 79 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 767,830 | 7.678 | 20 | 20 | fits | 150,443 | 54 | 0.471 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 1,077,326 | 10.773 | 20 | 20 | fits | 169,378 | 94 | 0.604 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 160,741 | 1.607 | 20 | 200 | fits | 161,814 | 145 | 0.559 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 1,202,187 | 12.022 | 20 | 200 | fits | 169,378 | 94 | 0.604 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 161,653 | 1.617 | 20 | 20 | fits | 161,814 | 145 | 0.559 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 1,202,883 | 12.029 | 20 | 20 | fits | 169,378 | 94 | 0.604 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 165,238 | 1.652 | 20 | 24 | fits | 161,814 | 145 | 0.559 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 1,320,331 | 13.203 | 20 | 24 | fits | 114,013 | 99 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 164,198 | 1.642 | 20 | 50 | fits | 161,814 | 145 | 0.559 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 1,205,863 | 12.059 | 20 | 50 | fits | 169,378 | 94 | 0.604 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 322,526 | 3.225 | 20 | 20 | fits | 158,783 | 79 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 621,659 | 6.217 | 20 | 20 | fits | 150,371 | 54 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 998,073 | 9.981 | 20 | 20 | fits | 167,270 | 111 | 0.560 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 179,313 | 1.793 | 20 | 200 | fits | 173,002 | 171 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 1,058,208 | 10.582 | 20 | 200 | fits | 167,270 | 111 | 0.560 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 180,225 | 1.802 | 20 | 20 | fits | 173,002 | 171 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 1,223,724 | 12.237 | 20 | 20 | fits | 164,820 | 69 | 0.583 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 183,810 | 1.838 | 20 | 24 | fits | 173,002 | 171 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 1,328,101 | 13.281 | 20 | 24 | fits | 100,942 | 87 | 0.466 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 182,770 | 1.828 | 20 | 50 | fits | 173,002 | 171 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 1,061,884 | 10.619 | 20 | 50 | fits | 167,270 | 111 | 0.560 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 341,047 | 3.410 | 20 | 20 | fits | 158,732 | 79 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 657,119 | 6.571 | 20 | 20 | fits | 155,844 | 59 | 0.540 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 882,064 | 8.821 | 20 | 20 | fits | 171,535 | 108 | 0.594 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 157,068 | 1.571 | 20 | 200 | fits | 163,415 | 149 | 0.550 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 1,042,558 | 10.426 | 20 | 200 | fits | 171,535 | 108 | 0.594 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 157,980 | 1.580 | 20 | 20 | fits | 163,415 | 149 | 0.550 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 1,192,753 | 11.928 | 20 | 20 | fits | 149,499 | 85 | 0.590 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 161,565 | 1.616 | 20 | 24 | fits | 163,415 | 149 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 1,308,025 | 13.080 | 20 | 24 | fits | 111,837 | 100 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 160,525 | 1.605 | 20 | 50 | fits | 163,415 | 149 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 1,195,733 | 11.957 | 20 | 50 | fits | 149,499 | 85 | 0.590 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 479,963 | 4.800 | 20 | 20 | fits | 161,804 | 42 | 0.692 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 872,619 | 8.726 | 20 | 20 | fits | 140,797 | 49 | 0.504 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 1,094,859 | 10.949 | 20 | 20 | fits | 168,227 | 95 | 0.597 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 163,981 | 1.640 | 20 | 200 | fits | 161,814 | 145 | 0.559 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 1,219,366 | 12.194 | 20 | 200 | fits | 168,227 | 95 | 0.597 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 164,893 | 1.649 | 20 | 20 | fits | 161,814 | 145 | 0.559 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 1,220,062 | 12.201 | 20 | 20 | fits | 168,227 | 95 | 0.597 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 168,478 | 1.685 | 20 | 24 | fits | 161,814 | 145 | 0.559 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 1,338,808 | 13.388 | 20 | 24 | fits | 104,560 | 92 | 0.499 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 167,438 | 1.674 | 20 | 50 | fits | 161,814 | 145 | 0.559 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 1,223,042 | 12.230 | 20 | 50 | fits | 168,227 | 95 | 0.597 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 325,944 | 3.259 | 20 | 20 | fits | 158,961 | 80 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 890,745 | 8.907 | 20 | 20 | fits | 171,277 | 106 | 0.593 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 922,550 | 9.226 | 20 | 20 | fits | 171,173 | 109 | 0.590 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 182,863 | 1.829 | 20 | 200 | fits | 173,312 | 172 | 0.534 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 1,062,737 | 10.627 | 20 | 200 | fits | 171,173 | 109 | 0.590 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 183,775 | 1.838 | 20 | 20 | fits | 173,312 | 172 | 0.534 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 1,228,672 | 12.287 | 20 | 20 | fits | 154,344 | 79 | 0.586 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 187,360 | 1.874 | 20 | 24 | fits | 173,312 | 172 | 0.534 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 1,344,105 | 13.441 | 20 | 24 | fits | 111,998 | 95 | 0.471 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 186,320 | 1.863 | 20 | 50 | fits | 173,312 | 172 | 0.534 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 1,066,413 | 10.664 | 20 | 50 | fits | 171,173 | 109 | 0.590 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 516,265 | 5.163 | 20 | 20 | fits | 159,883 | 43 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 893,160 | 8.932 | 20 | 20 | fits | 150,204 | 53 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 443,072 | 4.431 | 20 | 20 | fits | 168,477 | 150 | 0.577 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 153,827 | 1.538 | 20 | 200 | fits | 162,910 | 127 | 0.584 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 480,955 | 4.810 | 20 | 200 | fits | 168,477 | 150 | 0.577 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 154,739 | 1.547 | 20 | 20 | fits | 162,910 | 127 | 0.584 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 1,337,921 | 13.379 | 20 | 20 | fits | 154,597 | 89 | 0.555 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 158,324 | 1.583 | 20 | 24 | fits | 162,910 | 127 | 0.584 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 1,341,356 | 13.414 | 20 | 24 | fits | 154,597 | 89 | 0.555 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 157,284 | 1.573 | 20 | 50 | fits | 162,910 | 127 | 0.584 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 1,186,304 | 11.863 | 20 | 50 | fits | 155,048 | 82 | 0.623 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 722,833 | 7.228 | 20 | 20 | fits | 160,831 | 41 | 0.678 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 1,029,176 | 10.292 | 20 | 20 | fits | 145,881 | 55 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 970,284 | 9.703 | 20 | 20 | fits | 161,442 | 70 | 0.640 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 158,397 | 1.584 | 20 | 200 | fits | 157,799 | 170 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 1,113,971 | 11.140 | 20 | 200 | fits | 161,442 | 70 | 0.640 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 159,309 | 1.593 | 20 | 20 | fits | 157,799 | 170 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 1,257,437 | 12.574 | 20 | 20 | fits | 131,875 | 99 | 0.527 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 162,894 | 1.629 | 20 | 24 | fits | 157,799 | 170 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if1` | 1,260,872 | 12.609 | 20 | 24 | fits | 131,875 | 99 | 0.527 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 161,854 | 1.619 | 20 | 50 | fits | 157,799 | 170 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 956,205 | 9.562 | 20 | 50 | fits | 163,802 | 114 | 0.542 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 320,271 | 3.203 | 20 | 20 | fits | 158,872 | 80 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if1` | 636,593 | 6.366 | 20 | 20 | fits | 150,578 | 53 | 0.474 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 805,105 | 8.051 | 20 | 20 | fits | 170,636 | 109 | 0.588 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 171,487 | 1.715 | 20 | 200 | fits | 163,505 | 150 | 0.550 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 965,009 | 9.650 | 20 | 200 | fits | 170,636 | 109 | 0.588 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 172,399 | 1.724 | 20 | 20 | fits | 163,505 | 150 | 0.550 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 1,133,944 | 11.339 | 20 | 20 | fits | 157,462 | 85 | 0.639 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 175,984 | 1.760 | 20 | 24 | fits | 163,505 | 150 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if1` | 1,264,959 | 12.650 | 20 | 24 | fits | 127,580 | 112 | 0.442 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 174,944 | 1.749 | 20 | 50 | fits | 163,505 | 150 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 1,136,924 | 11.369 | 20 | 50 | fits | 157,462 | 85 | 0.639 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 506,792 | 5.068 | 20 | 20 | fits | 161,563 | 41 | 0.691 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if1` | 795,969 | 7.960 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 898,465 | 8.985 | 20 | 20 | fits | 169,319 | 117 | 0.625 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 158,498 | 1.585 | 20 | 200 | fits | 164,950 | 150 | 0.558 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 936,629 | 9.366 | 20 | 200 | fits | 169,319 | 117 | 0.625 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 159,410 | 1.594 | 20 | 20 | fits | 164,950 | 150 | 0.558 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 1,240,093 | 12.401 | 20 | 20 | fits | 141,435 | 106 | 0.486 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 162,995 | 1.630 | 20 | 24 | fits | 164,950 | 150 | 0.558 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if1` | 1,243,528 | 12.435 | 20 | 24 | fits | 141,435 | 106 | 0.486 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 161,955 | 1.620 | 20 | 50 | fits | 164,950 | 150 | 0.558 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 1,101,638 | 11.016 | 20 | 50 | fits | 150,351 | 83 | 0.605 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 479,762 | 4.798 | 20 | 20 | fits | 161,643 | 41 | 0.692 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if1` | 768,906 | 7.689 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 1,011,813 | 10.118 | 20 | 20 | fits | 168,073 | 94 | 0.599 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 161,890 | 1.619 | 20 | 200 | fits | 161,754 | 145 | 0.559 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 1,136,190 | 11.362 | 20 | 200 | fits | 168,073 | 94 | 0.599 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 162,802 | 1.628 | 20 | 20 | fits | 161,754 | 145 | 0.559 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 1,136,886 | 11.369 | 20 | 20 | fits | 168,073 | 94 | 0.599 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 166,387 | 1.664 | 20 | 24 | fits | 161,754 | 145 | 0.559 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if1` | 1,241,422 | 12.414 | 20 | 24 | fits | 101,101 | 86 | 0.468 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 165,347 | 1.653 | 20 | 50 | fits | 161,754 | 145 | 0.559 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 1,139,866 | 11.399 | 20 | 50 | fits | 168,073 | 94 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 323,675 | 3.237 | 20 | 20 | fits | 158,783 | 79 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if1` | 622,602 | 6.226 | 20 | 20 | fits | 150,204 | 53 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 911,337 | 9.113 | 20 | 20 | fits | 157,883 | 90 | 0.577 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 180,462 | 1.805 | 20 | 200 | fits | 172,942 | 171 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 971,213 | 9.712 | 20 | 200 | fits | 157,883 | 90 | 0.577 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 181,374 | 1.814 | 20 | 20 | fits | 172,942 | 171 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 1,136,907 | 11.369 | 20 | 20 | fits | 164,998 | 69 | 0.585 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 184,959 | 1.850 | 20 | 24 | fits | 172,942 | 171 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if1` | 1,241,002 | 12.410 | 20 | 24 | fits | 100,660 | 86 | 0.463 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 183,919 | 1.839 | 20 | 50 | fits | 172,942 | 171 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 974,889 | 9.749 | 20 | 50 | fits | 157,883 | 90 | 0.577 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 342,196 | 3.422 | 20 | 20 | fits | 158,732 | 79 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if1` | 651,029 | 6.510 | 20 | 20 | fits | 160,110 | 60 | 0.507 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 821,052 | 8.211 | 20 | 20 | fits | 166,297 | 107 | 0.571 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 159,347 | 1.593 | 20 | 200 | fits | 163,355 | 149 | 0.550 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 977,373 | 9.774 | 20 | 200 | fits | 166,297 | 107 | 0.571 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 160,259 | 1.603 | 20 | 20 | fits | 163,355 | 149 | 0.550 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 1,128,164 | 11.282 | 20 | 20 | fits | 150,095 | 74 | 0.561 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 163,844 | 1.638 | 20 | 24 | fits | 163,355 | 149 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if1` | 1,230,200 | 12.302 | 20 | 24 | fits | 98,601 | 87 | 0.451 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 162,804 | 1.628 | 20 | 50 | fits | 163,355 | 149 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 981,049 | 9.810 | 20 | 50 | fits | 166,297 | 107 | 0.571 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 321,179 | 3.212 | 20 | 20 | fits | 158,830 | 79 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if1` | 647,039 | 6.470 | 20 | 20 | fits | 155,793 | 59 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 1,017,885 | 10.179 | 20 | 20 | fits | 168,108 | 95 | 0.597 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 165,130 | 1.651 | 20 | 200 | fits | 161,754 | 145 | 0.559 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 1,142,321 | 11.423 | 20 | 200 | fits | 168,108 | 95 | 0.597 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 166,042 | 1.660 | 20 | 20 | fits | 161,754 | 145 | 0.559 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 1,143,017 | 11.430 | 20 | 20 | fits | 168,108 | 95 | 0.597 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 169,627 | 1.696 | 20 | 24 | fits | 161,754 | 145 | 0.559 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if1` | 1,261,763 | 12.618 | 20 | 24 | fits | 104,560 | 92 | 0.499 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 168,587 | 1.686 | 20 | 50 | fits | 161,754 | 145 | 0.559 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 1,145,997 | 11.460 | 20 | 50 | fits | 168,108 | 95 | 0.597 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 327,093 | 3.271 | 20 | 20 | fits | 158,961 | 80 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if1` | 813,879 | 8.139 | 20 | 20 | fits | 171,116 | 106 | 0.592 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 403,183 | 4.032 | 20 | 20 | fits | 155,365 | 124 | 0.619 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 144,566 | 1.446 | 20 | 200 | fits | 152,718 | 133 | 0.550 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 477,707 | 4.777 | 20 | 200 | fits | 155,365 | 124 | 0.619 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 145,478 | 1.455 | 20 | 20 | fits | 152,718 | 133 | 0.550 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 1,259,076 | 12.591 | 20 | 20 | fits | 144,069 | 107 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 149,063 | 1.491 | 20 | 24 | fits | 152,718 | 133 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if1` | 1,262,511 | 12.625 | 20 | 24 | fits | 144,069 | 107 | 0.522 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 148,023 | 1.480 | 20 | 50 | fits | 152,718 | 133 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 481,383 | 4.814 | 20 | 50 | fits | 155,365 | 124 | 0.619 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 645,915 | 6.459 | 20 | 20 | fits | 164,597 | 47 | 0.691 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if1` | 934,980 | 9.350 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 967,552 | 9.676 | 20 | 20 | fits | 161,333 | 69 | 0.642 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 156,870 | 1.569 | 20 | 200 | fits | 158,549 | 170 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 1,111,084 | 11.111 | 20 | 200 | fits | 161,333 | 69 | 0.642 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 157,782 | 1.578 | 20 | 20 | fits | 158,549 | 170 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 1,320,261 | 13.203 | 20 | 20 | fits | 127,747 | 94 | 0.499 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 161,367 | 1.614 | 20 | 24 | fits | 158,549 | 170 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 1,323,696 | 13.237 | 20 | 24 | fits | 127,747 | 94 | 0.499 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 160,327 | 1.603 | 20 | 50 | fits | 158,549 | 170 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 953,427 | 9.534 | 20 | 50 | fits | 163,821 | 114 | 0.543 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 316,964 | 3.170 | 20 | 20 | fits | 157,092 | 79 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if1` | 633,151 | 6.332 | 20 | 20 | fits | 155,732 | 59 | 0.541 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 882,201 | 8.822 | 20 | 20 | fits | 157,580 | 105 | 0.628 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 169,589 | 1.696 | 20 | 200 | fits | 163,884 | 149 | 0.548 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 967,127 | 9.671 | 20 | 200 | fits | 157,580 | 105 | 0.628 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 170,501 | 1.705 | 20 | 20 | fits | 163,884 | 149 | 0.548 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 1,214,492 | 12.145 | 20 | 20 | fits | 165,999 | 70 | 0.591 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 174,086 | 1.741 | 20 | 24 | fits | 163,884 | 149 | 0.548 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 1,346,057 | 13.461 | 20 | 24 | fits | 117,271 | 105 | 0.478 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 173,046 | 1.730 | 20 | 50 | fits | 163,884 | 149 | 0.548 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 970,803 | 9.708 | 20 | 50 | fits | 157,580 | 105 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 329,929 | 3.299 | 20 | 20 | fits | 157,338 | 80 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if1` | 646,413 | 6.464 | 20 | 20 | fits | 150,683 | 53 | 0.477 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 907,048 | 9.070 | 20 | 20 | fits | 166,343 | 110 | 0.624 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 157,537 | 1.575 | 20 | 200 | fits | 163,884 | 149 | 0.548 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 945,228 | 9.452 | 20 | 200 | fits | 166,343 | 110 | 0.624 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 158,449 | 1.584 | 20 | 20 | fits | 163,884 | 149 | 0.548 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 1,203,618 | 12.036 | 20 | 20 | fits | 177,225 | 91 | 0.589 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 162,034 | 1.620 | 20 | 24 | fits | 163,884 | 149 | 0.548 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 1,335,288 | 13.353 | 20 | 24 | fits | 117,391 | 105 | 0.479 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 160,994 | 1.610 | 20 | 50 | fits | 163,884 | 149 | 0.548 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 1,206,598 | 12.066 | 20 | 50 | fits | 177,225 | 91 | 0.589 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 490,961 | 4.910 | 20 | 20 | fits | 162,900 | 47 | 0.699 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if1` | 780,481 | 7.805 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 998,378 | 9.984 | 20 | 20 | fits | 152,953 | 94 | 0.609 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 160,254 | 1.603 | 20 | 200 | fits | 158,693 | 171 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 1,035,287 | 10.353 | 20 | 200 | fits | 152,953 | 94 | 0.609 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 161,166 | 1.612 | 20 | 20 | fits | 158,693 | 171 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 1,329,995 | 13.300 | 20 | 20 | fits | 113,780 | 79 | 0.511 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 164,751 | 1.648 | 20 | 24 | fits | 158,693 | 171 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 1,333,430 | 13.334 | 20 | 24 | fits | 113,780 | 79 | 0.511 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 163,711 | 1.637 | 20 | 50 | fits | 158,693 | 171 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 1,038,963 | 10.390 | 20 | 50 | fits | 152,953 | 94 | 0.609 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 504,323 | 5.043 | 20 | 20 | fits | 159,837 | 41 | 0.690 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if1` | 803,377 | 8.034 | 20 | 20 | fits | 149,878 | 55 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 913,350 | 9.133 | 20 | 20 | fits | 161,497 | 93 | 0.613 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 179,877 | 1.799 | 20 | 200 | fits | 173,537 | 171 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 1,051,203 | 10.512 | 20 | 200 | fits | 161,497 | 93 | 0.613 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 180,789 | 1.808 | 20 | 20 | fits | 173,537 | 171 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 1,216,277 | 12.163 | 20 | 20 | fits | 164,378 | 69 | 0.580 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 184,374 | 1.844 | 20 | 24 | fits | 173,537 | 171 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 1,320,555 | 13.206 | 20 | 24 | fits | 100,843 | 86 | 0.466 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 183,334 | 1.833 | 20 | 50 | fits | 173,537 | 171 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 1,054,879 | 10.549 | 20 | 50 | fits | 161,497 | 93 | 0.613 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 340,009 | 3.400 | 20 | 20 | fits | 157,130 | 79 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if1` | 648,709 | 6.487 | 20 | 20 | fits | 159,874 | 59 | 0.506 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 884,032 | 8.840 | 20 | 20 | fits | 172,453 | 108 | 0.600 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 157,553 | 1.576 | 20 | 200 | fits | 163,900 | 149 | 0.548 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 1,044,584 | 10.446 | 20 | 200 | fits | 172,453 | 108 | 0.600 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 158,465 | 1.585 | 20 | 20 | fits | 163,900 | 149 | 0.548 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 1,194,700 | 11.947 | 20 | 20 | fits | 149,420 | 85 | 0.589 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 162,050 | 1.621 | 20 | 24 | fits | 163,900 | 149 | 0.548 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 1,309,782 | 13.098 | 20 | 24 | fits | 111,647 | 99 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 161,010 | 1.610 | 20 | 50 | fits | 163,900 | 149 | 0.548 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 1,197,680 | 11.977 | 20 | 50 | fits | 149,420 | 85 | 0.589 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 477,073 | 4.771 | 20 | 20 | fits | 158,450 | 43 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if1` | 873,727 | 8.737 | 20 | 20 | fits | 155,846 | 59 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 1,087,385 | 10.874 | 20 | 20 | fits | 167,483 | 94 | 0.595 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 164,554 | 1.646 | 20 | 200 | fits | 162,391 | 145 | 0.558 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 1,211,575 | 12.116 | 20 | 200 | fits | 167,483 | 94 | 0.595 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 165,466 | 1.655 | 20 | 20 | fits | 162,391 | 145 | 0.558 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 1,212,271 | 12.123 | 20 | 20 | fits | 167,483 | 94 | 0.595 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 169,051 | 1.691 | 20 | 24 | fits | 162,391 | 145 | 0.558 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 1,329,299 | 13.293 | 20 | 24 | fits | 113,593 | 95 | 0.478 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 168,011 | 1.680 | 20 | 50 | fits | 162,391 | 145 | 0.558 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 1,215,251 | 12.153 | 20 | 50 | fits | 167,483 | 94 | 0.595 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 324,715 | 3.247 | 20 | 20 | fits | 157,159 | 79 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if1` | 718,423 | 7.184 | 20 | 20 | fits | 154,520 | 60 | 0.503 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 937,219 | 9.372 | 20 | 20 | fits | 170,968 | 108 | 0.591 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 183,117 | 1.831 | 20 | 200 | fits | 173,570 | 171 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 1,077,172 | 10.772 | 20 | 200 | fits | 170,968 | 108 | 0.591 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 184,029 | 1.840 | 20 | 20 | fits | 173,570 | 171 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 1,232,214 | 12.322 | 20 | 20 | fits | 154,346 | 68 | 0.616 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 187,614 | 1.876 | 20 | 24 | fits | 173,570 | 171 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 1,347,877 | 13.479 | 20 | 24 | fits | 112,228 | 99 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 186,574 | 1.866 | 20 | 50 | fits | 173,570 | 171 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 1,080,848 | 10.808 | 20 | 50 | fits | 170,968 | 108 | 0.591 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 604,458 | 6.045 | 20 | 20 | fits | 162,946 | 48 | 0.691 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if1` | 907,800 | 9.078 | 20 | 20 | fits | 140,435 | 49 | 0.488 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 1,003,322 | 10.033 | 20 | 20 | fits | 160,025 | 91 | 0.628 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 172,622 | 1.726 | 20 | 200 | fits | 162,435 | 145 | 0.559 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 1,120,079 | 11.201 | 20 | 200 | fits | 160,025 | 91 | 0.628 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 173,534 | 1.735 | 20 | 20 | fits | 162,435 | 145 | 0.559 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 1,249,165 | 12.492 | 20 | 20 | fits | 128,390 | 93 | 0.501 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 177,119 | 1.771 | 20 | 24 | fits | 162,435 | 145 | 0.559 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if1` | 1,252,600 | 12.526 | 20 | 24 | fits | 128,390 | 93 | 0.501 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 176,079 | 1.761 | 20 | 50 | fits | 162,435 | 145 | 0.559 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 1,123,755 | 11.238 | 20 | 50 | fits | 160,025 | 91 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 332,762 | 3.328 | 20 | 20 | fits | 157,138 | 79 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if1` | 631,792 | 6.318 | 20 | 20 | fits | 150,204 | 53 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 964,347 | 9.643 | 20 | 20 | fits | 161,087 | 69 | 0.640 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 157,280 | 1.573 | 20 | 200 | fits | 158,621 | 170 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 1,107,742 | 11.077 | 20 | 200 | fits | 161,087 | 69 | 0.640 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 158,192 | 1.582 | 20 | 20 | fits | 158,621 | 170 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 1,235,735 | 12.357 | 20 | 20 | fits | 127,297 | 93 | 0.493 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 161,777 | 1.618 | 20 | 24 | fits | 158,621 | 170 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if1` | 1,239,170 | 12.392 | 20 | 24 | fits | 127,297 | 93 | 0.493 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 160,737 | 1.607 | 20 | 50 | fits | 158,621 | 170 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 950,331 | 9.503 | 20 | 50 | fits | 164,040 | 114 | 0.544 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 317,374 | 3.174 | 20 | 20 | fits | 157,092 | 79 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if1` | 616,571 | 6.166 | 20 | 20 | fits | 150,371 | 54 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 882,852 | 8.829 | 20 | 20 | fits | 157,520 | 105 | 0.627 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 169,987 | 1.700 | 20 | 200 | fits | 163,944 | 149 | 0.549 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 967,718 | 9.677 | 20 | 200 | fits | 157,520 | 105 | 0.627 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 170,899 | 1.709 | 20 | 20 | fits | 163,944 | 149 | 0.549 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 1,134,274 | 11.343 | 20 | 20 | fits | 165,860 | 69 | 0.585 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 174,484 | 1.745 | 20 | 24 | fits | 163,944 | 149 | 0.549 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if1` | 1,251,767 | 12.518 | 20 | 24 | fits | 114,058 | 100 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 173,444 | 1.734 | 20 | 50 | fits | 163,944 | 149 | 0.549 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 971,394 | 9.714 | 20 | 50 | fits | 157,520 | 105 | 0.627 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 330,149 | 3.301 | 20 | 20 | fits | 157,160 | 79 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if1` | 646,317 | 6.463 | 20 | 20 | fits | 155,812 | 59 | 0.539 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 899,581 | 8.996 | 20 | 20 | fits | 172,954 | 111 | 0.587 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 157,597 | 1.576 | 20 | 200 | fits | 163,944 | 149 | 0.549 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 961,044 | 9.610 | 20 | 200 | fits | 172,954 | 111 | 0.587 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 158,509 | 1.585 | 20 | 20 | fits | 163,944 | 149 | 0.549 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 1,111,295 | 11.113 | 20 | 20 | fits | 149,555 | 85 | 0.593 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 162,094 | 1.621 | 20 | 24 | fits | 163,944 | 149 | 0.549 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if1` | 1,241,333 | 12.413 | 20 | 24 | fits | 116,197 | 105 | 0.471 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 161,054 | 1.611 | 20 | 50 | fits | 163,944 | 149 | 0.549 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 1,114,275 | 11.143 | 20 | 50 | fits | 149,555 | 85 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 490,748 | 4.907 | 20 | 20 | fits | 162,900 | 47 | 0.699 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if1` | 789,686 | 7.897 | 20 | 20 | fits | 149,458 | 55 | 0.515 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 918,631 | 9.186 | 20 | 20 | fits | 153,304 | 94 | 0.608 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 160,601 | 1.606 | 20 | 200 | fits | 158,702 | 171 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 955,403 | 9.554 | 20 | 200 | fits | 153,304 | 94 | 0.608 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 161,513 | 1.615 | 20 | 20 | fits | 158,702 | 171 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 1,250,196 | 12.502 | 20 | 20 | fits | 113,780 | 79 | 0.511 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 165,098 | 1.651 | 20 | 24 | fits | 158,702 | 171 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if1` | 1,253,631 | 12.536 | 20 | 24 | fits | 113,780 | 79 | 0.511 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 164,058 | 1.641 | 20 | 50 | fits | 158,702 | 171 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 959,079 | 9.591 | 20 | 50 | fits | 153,304 | 94 | 0.608 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 504,605 | 5.046 | 20 | 20 | fits | 159,837 | 41 | 0.690 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if1` | 803,695 | 8.037 | 20 | 20 | fits | 140,138 | 49 | 0.482 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 813,898 | 8.139 | 20 | 20 | fits | 171,153 | 109 | 0.590 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 173,546 | 1.735 | 20 | 200 | fits | 164,263 | 150 | 0.549 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 973,931 | 9.739 | 20 | 200 | fits | 171,153 | 109 | 0.590 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 174,458 | 1.745 | 20 | 20 | fits | 164,263 | 150 | 0.549 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 1,138,331 | 11.383 | 20 | 20 | fits | 152,931 | 88 | 0.610 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 178,043 | 1.780 | 20 | 24 | fits | 164,263 | 150 | 0.549 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if1` | 1,254,089 | 12.541 | 20 | 24 | fits | 112,323 | 99 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 177,003 | 1.770 | 20 | 50 | fits | 164,263 | 150 | 0.549 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 1,141,311 | 11.413 | 20 | 50 | fits | 152,931 | 88 | 0.610 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 505,356 | 5.054 | 20 | 20 | fits | 158,275 | 43 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if1` | 804,374 | 8.044 | 20 | 20 | fits | 150,276 | 53 | 0.470 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 799,726 | 7.997 | 20 | 20 | fits | 173,828 | 114 | 0.602 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 157,493 | 1.575 | 20 | 200 | fits | 163,840 | 149 | 0.547 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 959,793 | 9.598 | 20 | 200 | fits | 173,828 | 114 | 0.602 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 158,405 | 1.584 | 20 | 20 | fits | 163,840 | 149 | 0.547 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 1,110,080 | 11.101 | 20 | 20 | fits | 149,591 | 85 | 0.590 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 161,990 | 1.620 | 20 | 24 | fits | 163,840 | 149 | 0.547 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if1` | 1,225,284 | 12.253 | 20 | 24 | fits | 111,769 | 99 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 160,950 | 1.609 | 20 | 50 | fits | 163,840 | 149 | 0.547 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 1,113,060 | 11.131 | 20 | 50 | fits | 149,591 | 85 | 0.590 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 477,155 | 4.772 | 20 | 20 | fits | 158,450 | 43 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if1` | 776,198 | 7.762 | 20 | 20 | fits | 150,371 | 54 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 995,166 | 9.952 | 20 | 20 | fits | 171,461 | 97 | 0.599 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 164,832 | 1.648 | 20 | 200 | fits | 162,331 | 145 | 0.558 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 1,119,799 | 11.198 | 20 | 200 | fits | 171,461 | 97 | 0.599 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 165,744 | 1.657 | 20 | 20 | fits | 162,331 | 145 | 0.558 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 1,261,954 | 12.620 | 20 | 20 | fits | 141,459 | 101 | 0.513 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 169,329 | 1.693 | 20 | 24 | fits | 162,331 | 145 | 0.558 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if1` | 1,265,389 | 12.654 | 20 | 24 | fits | 141,459 | 101 | 0.513 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 168,289 | 1.683 | 20 | 50 | fits | 162,331 | 145 | 0.558 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 1,123,475 | 11.235 | 20 | 50 | fits | 171,461 | 97 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 489,441 | 4.894 | 20 | 20 | fits | 159,652 | 41 | 0.687 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if1` | 795,759 | 7.958 | 20 | 20 | fits | 145,773 | 55 | 0.558 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 977,097 | 9.771 | 20 | 20 | fits | 161,272 | 70 | 0.639 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 165,094 | 1.651 | 20 | 200 | fits | 158,171 | 170 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 1,120,614 | 11.206 | 20 | 200 | fits | 161,272 | 70 | 0.639 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 166,006 | 1.660 | 20 | 20 | fits | 158,171 | 170 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 1,342,530 | 13.425 | 20 | 20 | fits | 133,208 | 99 | 0.536 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 169,591 | 1.696 | 20 | 24 | fits | 158,171 | 170 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 1,345,965 | 13.460 | 20 | 24 | fits | 133,208 | 99 | 0.536 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 168,551 | 1.686 | 20 | 50 | fits | 158,171 | 170 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 963,018 | 9.630 | 20 | 50 | fits | 163,802 | 114 | 0.542 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 326,908 | 3.269 | 20 | 20 | fits | 158,812 | 80 | 0.665 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 643,382 | 6.434 | 20 | 20 | fits | 150,649 | 53 | 0.476 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 821,457 | 8.215 | 20 | 20 | fits | 169,671 | 109 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 168,480 | 1.685 | 20 | 200 | fits | 173,085 | 172 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 961,015 | 9.610 | 20 | 200 | fits | 169,671 | 109 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 169,392 | 1.694 | 20 | 20 | fits | 173,085 | 172 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 1,130,260 | 11.303 | 20 | 20 | fits | 157,650 | 74 | 0.627 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 172,977 | 1.730 | 20 | 24 | fits | 173,085 | 172 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 1,324,618 | 13.246 | 20 | 24 | fits | 112,187 | 99 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 171,937 | 1.719 | 20 | 50 | fits | 173,085 | 172 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 964,691 | 9.647 | 20 | 50 | fits | 169,671 | 109 | 0.579 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 503,692 | 5.037 | 20 | 20 | fits | 161,292 | 41 | 0.691 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 792,940 | 7.929 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 867,874 | 8.679 | 20 | 20 | fits | 160,463 | 113 | 0.626 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 178,942 | 1.789 | 20 | 200 | fits | 164,196 | 150 | 0.557 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 952,653 | 9.527 | 20 | 200 | fits | 160,463 | 113 | 0.626 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 179,854 | 1.799 | 20 | 20 | fits | 164,196 | 150 | 0.557 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 1,335,045 | 13.350 | 20 | 20 | fits | 141,596 | 106 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 183,439 | 1.834 | 20 | 24 | fits | 164,196 | 150 | 0.557 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 1,338,480 | 13.385 | 20 | 24 | fits | 141,596 | 106 | 0.487 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 182,399 | 1.824 | 20 | 50 | fits | 164,196 | 150 | 0.557 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 1,196,429 | 11.964 | 20 | 50 | fits | 152,100 | 81 | 0.619 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 340,530 | 3.405 | 20 | 20 | fits | 158,586 | 79 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 639,578 | 6.396 | 20 | 20 | fits | 150,204 | 53 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 1,097,672 | 10.977 | 20 | 20 | fits | 168,020 | 94 | 0.599 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 169,400 | 1.694 | 20 | 200 | fits | 161,908 | 145 | 0.558 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 1,221,966 | 12.220 | 20 | 200 | fits | 168,020 | 94 | 0.599 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 170,312 | 1.703 | 20 | 20 | fits | 161,908 | 145 | 0.558 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 1,222,662 | 12.227 | 20 | 20 | fits | 168,020 | 94 | 0.599 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 173,897 | 1.739 | 20 | 24 | fits | 161,908 | 145 | 0.558 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 1,327,135 | 13.271 | 20 | 24 | fits | 101,038 | 86 | 0.467 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 172,857 | 1.729 | 20 | 50 | fits | 161,908 | 145 | 0.558 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 1,225,642 | 12.256 | 20 | 50 | fits | 168,020 | 94 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 331,125 | 3.311 | 20 | 20 | fits | 158,723 | 79 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 630,237 | 6.302 | 20 | 20 | fits | 150,204 | 53 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 1,040,898 | 10.409 | 20 | 20 | fits | 155,974 | 73 | 0.595 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 154,002 | 1.540 | 20 | 200 | fits | 158,038 | 170 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 1,188,265 | 11.883 | 20 | 200 | fits | 155,974 | 73 | 0.595 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 154,914 | 1.549 | 20 | 20 | fits | 158,038 | 170 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 1,303,777 | 13.038 | 20 | 20 | fits | 114,816 | 79 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 158,499 | 1.585 | 20 | 24 | fits | 158,038 | 170 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 1,307,212 | 13.072 | 20 | 24 | fits | 114,816 | 79 | 0.522 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 157,459 | 1.575 | 20 | 50 | fits | 158,038 | 170 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 1,035,967 | 10.360 | 20 | 50 | fits | 164,019 | 114 | 0.544 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 315,493 | 3.155 | 20 | 20 | fits | 158,489 | 79 | 0.665 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 624,576 | 6.246 | 20 | 20 | fits | 160,175 | 60 | 0.507 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 906,422 | 9.064 | 20 | 20 | fits | 166,336 | 107 | 0.572 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 166,857 | 1.669 | 20 | 200 | fits | 163,509 | 149 | 0.549 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 1,062,782 | 10.628 | 20 | 200 | fits | 166,336 | 107 | 0.572 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 167,769 | 1.678 | 20 | 20 | fits | 163,509 | 149 | 0.549 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 1,213,573 | 12.136 | 20 | 20 | fits | 150,095 | 74 | 0.561 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 171,354 | 1.714 | 20 | 24 | fits | 163,509 | 149 | 0.549 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 1,315,459 | 13.155 | 20 | 24 | fits | 98,451 | 86 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 170,314 | 1.703 | 20 | 50 | fits | 163,509 | 149 | 0.549 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 1,066,458 | 10.665 | 20 | 50 | fits | 166,336 | 107 | 0.572 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 328,560 | 3.286 | 20 | 20 | fits | 158,701 | 79 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 732,167 | 7.322 | 20 | 20 | fits | 156,362 | 59 | 0.546 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 1,101,374 | 11.014 | 20 | 20 | fits | 164,198 | 74 | 0.627 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 149,281 | 1.493 | 20 | 200 | fits | 157,461 | 131 | 0.565 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 1,175,916 | 11.759 | 20 | 200 | fits | 164,198 | 74 | 0.627 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 150,193 | 1.502 | 20 | 20 | fits | 157,461 | 131 | 0.565 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 1,345,083 | 13.451 | 20 | 20 | fits | 157,947 | 93 | 0.572 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 153,778 | 1.538 | 20 | 24 | fits | 157,461 | 131 | 0.565 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 1,348,518 | 13.485 | 20 | 24 | fits | 157,947 | 93 | 0.572 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 152,738 | 1.527 | 20 | 50 | fits | 157,461 | 131 | 0.565 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 482,169 | 4.822 | 20 | 50 | fits | 162,493 | 149 | 0.574 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 724,188 | 7.242 | 20 | 20 | fits | 163,306 | 47 | 0.689 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 1,013,314 | 10.133 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 1,025,275 | 10.253 | 20 | 20 | fits | 156,320 | 73 | 0.597 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 157,242 | 1.572 | 20 | 200 | fits | 158,038 | 170 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 1,172,794 | 11.728 | 20 | 200 | fits | 156,320 | 73 | 0.597 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 158,154 | 1.582 | 20 | 20 | fits | 158,038 | 170 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 1,341,917 | 13.419 | 20 | 20 | fits | 158,022 | 95 | 0.569 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 161,739 | 1.617 | 20 | 24 | fits | 158,038 | 170 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 1,345,352 | 13.454 | 20 | 24 | fits | 158,022 | 95 | 0.569 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 160,699 | 1.607 | 20 | 50 | fits | 158,038 | 170 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 1,020,150 | 10.201 | 20 | 50 | fits | 158,228 | 93 | 0.583 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 570,448 | 5.704 | 20 | 20 | fits | 164,435 | 47 | 0.702 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 859,842 | 8.598 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 805,162 | 8.052 | 20 | 20 | fits | 166,374 | 108 | 0.570 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 163,360 | 1.634 | 20 | 200 | fits | 163,516 | 149 | 0.549 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 961,556 | 9.616 | 20 | 200 | fits | 166,374 | 108 | 0.570 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 164,272 | 1.643 | 20 | 20 | fits | 163,516 | 149 | 0.549 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 1,116,180 | 11.162 | 20 | 20 | fits | 153,928 | 78 | 0.629 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 167,857 | 1.679 | 20 | 24 | fits | 163,516 | 149 | 0.549 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if1` | 1,246,900 | 12.469 | 20 | 24 | fits | 127,285 | 113 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 166,817 | 1.668 | 20 | 50 | fits | 163,516 | 149 | 0.549 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 1,119,160 | 11.192 | 20 | 50 | fits | 153,928 | 78 | 0.629 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 325,042 | 3.250 | 20 | 20 | fits | 158,680 | 79 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if1` | 641,325 | 6.413 | 20 | 20 | fits | 155,845 | 59 | 0.540 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 978,570 | 9.786 | 20 | 20 | fits | 161,163 | 69 | 0.641 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 165,345 | 1.653 | 20 | 200 | fits | 158,117 | 170 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 1,121,932 | 11.219 | 20 | 200 | fits | 161,163 | 69 | 0.641 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 166,257 | 1.663 | 20 | 20 | fits | 158,117 | 170 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 1,250,069 | 12.501 | 20 | 20 | fits | 127,441 | 94 | 0.494 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 169,842 | 1.698 | 20 | 24 | fits | 158,117 | 170 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if1` | 1,253,504 | 12.535 | 20 | 24 | fits | 127,441 | 94 | 0.494 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 168,802 | 1.688 | 20 | 50 | fits | 158,117 | 170 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 964,445 | 9.644 | 20 | 50 | fits | 163,821 | 114 | 0.543 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 326,981 | 3.270 | 20 | 20 | fits | 158,634 | 79 | 0.666 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if1` | 644,460 | 6.445 | 20 | 20 | fits | 152,802 | 53 | 0.525 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 870,410 | 8.704 | 20 | 20 | fits | 174,624 | 93 | 0.623 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 168,716 | 1.687 | 20 | 200 | fits | 173,016 | 171 | 0.533 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 971,209 | 9.712 | 20 | 200 | fits | 174,624 | 93 | 0.623 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 169,628 | 1.696 | 20 | 20 | fits | 173,016 | 171 | 0.533 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 1,136,377 | 11.364 | 20 | 20 | fits | 164,472 | 70 | 0.579 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 173,213 | 1.732 | 20 | 24 | fits | 173,016 | 171 | 0.533 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if1` | 1,254,587 | 12.546 | 20 | 24 | fits | 103,916 | 92 | 0.494 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 172,173 | 1.722 | 20 | 50 | fits | 173,016 | 171 | 0.533 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 974,885 | 9.749 | 20 | 50 | fits | 174,624 | 93 | 0.623 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 330,547 | 3.305 | 20 | 20 | fits | 158,829 | 80 | 0.669 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if1` | 647,158 | 6.472 | 20 | 20 | fits | 150,754 | 53 | 0.478 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 909,655 | 9.097 | 20 | 20 | fits | 172,515 | 112 | 0.581 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 166,919 | 1.669 | 20 | 200 | fits | 163,835 | 150 | 0.550 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 971,143 | 9.711 | 20 | 200 | fits | 172,515 | 112 | 0.581 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 167,831 | 1.678 | 20 | 20 | fits | 163,835 | 150 | 0.550 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 1,135,691 | 11.357 | 20 | 20 | fits | 153,082 | 87 | 0.614 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 171,416 | 1.714 | 20 | 24 | fits | 163,835 | 150 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if1` | 1,251,594 | 12.516 | 20 | 24 | fits | 112,468 | 99 | 0.446 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 170,376 | 1.704 | 20 | 50 | fits | 163,835 | 150 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 1,138,671 | 11.387 | 20 | 50 | fits | 153,082 | 87 | 0.614 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 500,997 | 5.010 | 20 | 20 | fits | 161,479 | 41 | 0.692 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if1` | 800,224 | 8.002 | 20 | 20 | fits | 150,019 | 55 | 0.525 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 1,012,691 | 10.127 | 20 | 20 | fits | 168,049 | 94 | 0.599 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 169,678 | 1.697 | 20 | 200 | fits | 161,815 | 145 | 0.557 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 1,136,993 | 11.370 | 20 | 200 | fits | 168,049 | 94 | 0.599 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 170,590 | 1.706 | 20 | 20 | fits | 161,815 | 145 | 0.557 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 1,137,689 | 11.377 | 20 | 20 | fits | 168,049 | 94 | 0.599 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 174,175 | 1.742 | 20 | 24 | fits | 161,815 | 145 | 0.557 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if1` | 1,242,225 | 12.422 | 20 | 24 | fits | 101,101 | 86 | 0.468 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 173,135 | 1.731 | 20 | 50 | fits | 161,815 | 145 | 0.557 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 1,140,669 | 11.407 | 20 | 50 | fits | 168,049 | 94 | 0.599 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 331,403 | 3.314 | 20 | 20 | fits | 158,723 | 79 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if1` | 640,146 | 6.401 | 20 | 20 | fits | 159,874 | 59 | 0.506 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 963,711 | 9.637 | 20 | 20 | fits | 155,893 | 73 | 0.594 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 154,388 | 1.544 | 20 | 200 | fits | 158,086 | 170 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 1,110,997 | 11.110 | 20 | 200 | fits | 155,893 | 73 | 0.594 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 155,300 | 1.553 | 20 | 20 | fits | 158,086 | 170 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 1,226,509 | 12.265 | 20 | 20 | fits | 114,816 | 79 | 0.522 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 158,885 | 1.589 | 20 | 24 | fits | 158,086 | 170 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if1` | 1,229,944 | 12.299 | 20 | 24 | fits | 114,816 | 79 | 0.522 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 157,845 | 1.578 | 20 | 50 | fits | 158,086 | 170 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 958,780 | 9.588 | 20 | 50 | fits | 164,040 | 114 | 0.544 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 315,879 | 3.159 | 20 | 20 | fits | 158,489 | 79 | 0.665 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if1` | 624,919 | 6.249 | 20 | 20 | fits | 150,579 | 54 | 0.473 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 827,339 | 8.273 | 20 | 20 | fits | 166,341 | 107 | 0.572 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 167,135 | 1.671 | 20 | 200 | fits | 163,449 | 149 | 0.549 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 983,537 | 9.835 | 20 | 200 | fits | 166,341 | 107 | 0.572 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 168,047 | 1.680 | 20 | 20 | fits | 163,449 | 149 | 0.549 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 1,134,328 | 11.343 | 20 | 20 | fits | 150,095 | 74 | 0.561 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 171,632 | 1.716 | 20 | 24 | fits | 163,449 | 149 | 0.549 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if1` | 1,236,150 | 12.361 | 20 | 24 | fits | 98,387 | 86 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 170,592 | 1.706 | 20 | 50 | fits | 163,449 | 149 | 0.549 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 987,213 | 9.872 | 20 | 50 | fits | 166,341 | 107 | 0.572 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 328,838 | 3.288 | 20 | 20 | fits | 158,701 | 79 | 0.670 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if1` | 641,792 | 6.418 | 20 | 20 | fits | 154,597 | 60 | 0.493 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 1,023,545 | 10.235 | 20 | 20 | fits | 164,401 | 73 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 149,667 | 1.497 | 20 | 200 | fits | 157,509 | 131 | 0.565 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 1,098,042 | 10.980 | 20 | 200 | fits | 164,401 | 73 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 150,579 | 1.506 | 20 | 20 | fits | 157,509 | 131 | 0.565 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 1,253,603 | 12.536 | 20 | 20 | fits | 154,865 | 87 | 0.558 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 154,164 | 1.542 | 20 | 24 | fits | 157,509 | 131 | 0.565 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if1` | 1,257,038 | 12.570 | 20 | 24 | fits | 154,865 | 87 | 0.558 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 153,124 | 1.531 | 20 | 50 | fits | 157,509 | 131 | 0.565 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 471,303 | 4.713 | 20 | 50 | fits | 161,973 | 150 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 645,690 | 6.457 | 20 | 20 | fits | 164,210 | 47 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if1` | 935,237 | 9.352 | 20 | 20 | fits | 140,040 | 49 | 0.480 |
| LINK_UP | `adp.link_up.if0` | 2,706 | 0.027 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| LINK_UP | `adp.link_up.if1` | 17,474 | 0.175 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,723 | 0.187 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 10,980 | 0.110 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 14,971 | 0.150 | 20 | 200 | fits | 4,847 | 19 (11) | 0.500 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 13,000 | 0.130 | 20 | 200 | fits | 4,847 | 19 (11) | 0.500 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 14,627 | 0.146 | 20 | 50 | fits | 33,187 | 44 | 0.716 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 29,144 | 0.291 | 20 | 50 | fits | 29,752 | 36 | 0.694 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 14,236 | 0.142 | 20 | 50 | fits | 30,094 | 36 | 0.701 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 17,254 | 0.173 | 20 | 50 | fits | 35,670 | 62 | 0.619 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,166 | 0.192 | 20 | 50 | fits | 35,670 | 62 | 0.619 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 12,591 | 0.126 | 20 | 50 | fits | 27,685 | 31 | 0.615 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 13,497 | 0.135 | 20 | 50 | fits | 32,080 | 44 | 0.691 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 20,588 | 0.206 | 20 | 50 | fits | 30,593 | 37 | 0.700 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 18,008 | 0.180 | 20 | 50 | fits | 29,189 | 36 | 0.670 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 27,542 | 0.275 | 20 | 50 | fits | 37,000 | 62 | 0.636 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 29,379 | 0.294 | 20 | 50 | fits | 37,000 | 62 | 0.636 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 12,826 | 0.128 | 20 | 50 | fits | 28,126 | 31 | 0.615 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 28,796 | 0.288 | 20 | 20 | fits | 77,736 | 42 (35) | 0.749 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 55,659 | 0.557 | 20 | 20 | fits | 77,736 | 42 (35) | 0.749 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 33,526 | 0.335 | 20 | 20 | fits | 67,197 | 34 (14) | 0.809 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 55,407 | 0.554 | 20 | 20 | fits | 67,197 | 34 (14) | 0.809 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 33,470 | 0.335 | 20 | 20 | fits | 65,419 | 35 (14) | 0.802 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 54,792 | 0.548 | 20 | 20 | fits | 65,419 | 35 (14) | 0.802 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 40,168 | 0.402 | 20 | 20 | fits | 50,887 | 22 (35) | 0.821 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 25,370 | 0.254 | 20 | 20 | fits | 50,815 | 22 (35) | 0.818 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 144,410 | 1.444 | 20 | 20 | fits | 117,748 | 6 | 0.795 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 135,923 | 1.359 | 20 | 20 | fits | 108,772 | 6 | 0.733 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 55,818 | 0.558 | 20 | 20 | fits | 55,883 | 13 | 0.897 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,124 | 0.241 | 20 | 20 | fits | 24,189 | 13 | 0.671 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 191,225 | 1.912 | 220 | 220 | fits | 187,289 | 10 | 0.800 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 51,137 | 0.511 | 20 | 20 | fits | 51,202 | 13 | 0.889 |
| malformed MRPDU discard | `srp.malformed.if1` | 24,332 | 0.243 | 20 | 20 | fits | 24,397 | 13 | 0.667 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 163,143 | 1.631 | 220 | 220 | fits | 157,336 | 9 | 0.789 |
| an event behind 15 others | `backlog.event.if0` | 203,307 | 2.033 | 20 | 200 | fits | 129,233 | 129 | 0.562 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 940,280 | 9.403 | 20 | 20 | fits | 138,098 | 106 | 0.468 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 192,029 | 1.920 | 20 | 200 | fits | 192,237 | 180 | 0.541 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 931,241 | 9.312 | 20 | 200 | fits | 167,535 | 72 | 0.603 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 187,770 | 1.878 | 20 | 20 | fits | 192,237 | 180 | 0.541 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,064,864 | 10.649 | 20 | 20 | fits | 138,098 | 106 | 0.468 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 191,355 | 1.914 | 20 | 24 | fits | 192,237 | 180 | 0.541 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,068,299 | 10.683 | 20 | 24 | fits | 138,098 | 106 | 0.468 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 190,315 | 1.903 | 20 | 50 | fits | 192,237 | 180 | 0.541 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 492,193 | 4.922 | 20 | 50 | fits | 173,035 | 78 | 0.640 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 601,963 | 6.020 | 20 | 20 | fits | 105,327 | 53 | 0.558 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 760,131 | 7.601 | 20 | 20 | fits | 75,291 | 43 | 0.523 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 798,412 | 7.984 | 20 | 20 | fits | 171,701 | 108 | 0.597 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 157,145 | 1.571 | 20 | 200 | fits | 161,827 | 155 | 0.537 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 958,993 | 9.590 | 20 | 200 | fits | 171,701 | 108 | 0.597 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 158,057 | 1.581 | 20 | 20 | fits | 161,827 | 155 | 0.537 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 1,109,261 | 11.093 | 20 | 20 | fits | 149,572 | 86 | 0.590 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 161,642 | 1.616 | 20 | 24 | fits | 161,827 | 155 | 0.537 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,239,185 | 12.392 | 20 | 24 | fits | 116,083 | 105 | 0.470 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 160,602 | 1.606 | 20 | 50 | fits | 161,827 | 155 | 0.537 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 1,112,241 | 11.122 | 20 | 50 | fits | 149,572 | 86 | 0.590 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 489,678 | 4.897 | 20 | 20 | fits | 159,279 | 43 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 788,888 | 7.889 | 20 | 20 | fits | 150,199 | 53 | 0.469 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 19,774 | 0.198 | 20 | 20 | fits | 42,499 | 20 | 0.770 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 157,145 | 1.571 | 20 | 200 | fits | 161,827 | 155 | 0.537 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 53,687 | 0.537 | 20 | 200 | fits | 42,499 | 20 | 0.770 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 158,057 | 1.581 | 20 | 20 | fits | 161,827 | 155 | 0.537 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 1,091,544 | 10.915 | 20 | 20 | fits | 150,755 | 87 | 0.584 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 161,642 | 1.616 | 20 | 24 | fits | 161,827 | 155 | 0.537 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,221,773 | 12.218 | 20 | 24 | fits | 116,201 | 105 | 0.472 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 160,602 | 1.606 | 20 | 50 | fits | 161,827 | 155 | 0.537 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 1,094,524 | 10.945 | 20 | 50 | fits | 150,755 | 87 | 0.584 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 489,678 | 4.897 | 20 | 20 | fits | 159,279 | 43 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 788,888 | 7.889 | 20 | 20 | fits | 150,199 | 53 | 0.469 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,405,527 | 64.055 | 20 | 20 | MISS ceiling | 36,264 | 13 | 0.683 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,039,144 | 360.391 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,039,069 | 360.391 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,038,994 | 360.390 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,038,919 | 360.389 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 165,048 | 1.650 | 20 | 200 | fits | 156,601 | 148 | 0.539 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 954,735 | 9.547 | 20 | 200 | fits | 165,558 | 118 | 0.545 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 160,789 | 1.608 | 20 | 20 | fits | 156,601 | 148 | 0.539 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,003,528 | 10.035 | 20 | 20 | fits | 53,268 | 20 | 0.589 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 164,374 | 1.644 | 20 | 24 | fits | 156,601 | 148 | 0.539 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,212,226 | 62.122 | 20 | 24 | MISS ceiling | 168,464 | 136 | 0.419 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 163,334 | 1.633 | 20 | 50 | fits | 156,601 | 148 | 0.539 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 953,240 | 9.532 | 20 | 50 | fits | 165,558 | 118 | 0.545 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 494,047 | 4.940 | 20 | 20 | fits | 161,680 | 42 | 0.691 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 785,602 | 7.856 | 20 | 20 | fits | 141,336 | 50 | 0.495 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,328 | 0.063 | 20 | 20 | fits | 60,633 | 22 (29) | 0.625 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 25,151 | 0.252 | 20 | 20 | fits | 60,633 | 22 (29) | 0.625 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,643 | 0.076 | 20 | 20 | fits | 63,501 | 33 (35) | 0.629 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 27,655 | 0.277 | 20 | 20 | fits | 63,501 | 33 (35) | 0.629 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 11,629 | 0.116 | 20 | 20 | fits | 63,037 | 25 (12) | 0.837 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 28,742 | 0.287 | 20 | 20 | fits | 50,183 | 22 (12) | 0.812 |
| LINK_UP | `adp.link_up.if0` | 2,706 | 0.027 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| LINK_UP | `adp.link_up.if1` | 17,474 | 0.175 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,723 | 0.187 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 10,980 | 0.110 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| LINK_DOWN | `adp.link_down.if0` | 2,414 | 0.024 | 20 | 200 | fits | 67,242 | 39 (9) | 0.692 |
| LINK_DOWN | `adp.link_down.if1` | 30,371 | 0.304 | 20 | 200 | fits | 67,242 | 39 (9) | 0.692 |
| LINK_UP | `adp.link_up.if0` | 2,706 | 0.027 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| LINK_UP | `adp.link_up.if1` | 17,474 | 0.175 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,723 | 0.187 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 10,980 | 0.110 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| GM_CHANGE | `adp.gm_change.if0` | 2,543 | 0.025 | 20 | 200 | fits | 21,179 | 27 (11) | 0.633 |
| GM_CHANGE | `adp.gm_change.if1` | 4,192 | 0.042 | 20 | 200 | fits | 21,179 | 27 (11) | 0.633 |
| LINK_UP | `adp.link_up.if0` | 2,706 | 0.027 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| LINK_UP | `adp.link_up.if1` | 17,474 | 0.175 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,723 | 0.187 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 10,980 | 0.110 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,163 | 0.052 | 20 | 200 | fits | 24,357 | 28 (31) | 0.458 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 6,612 | 0.066 | 20 | 200 | fits | 24,357 | 28 (31) | 0.458 |
| LINK_UP | `adp.link_up.if0` | 2,706 | 0.027 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| LINK_UP | `adp.link_up.if1` | 17,474 | 0.175 | 20 | 200 | fits | 44,949 | 79 (11) | 0.633 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,723 | 0.187 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 10,980 | 0.110 | 20 | 200 | fits | 35,327 | 39 (39) | 0.616 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,163 | 0.052 | 20 | 200 | fits | 19,666 | 17 (31) | 0.622 |
| set_name | `aecp_fanout.set_name.if0` | 73,430 | 0.734 | 20 | 24 | fits | 77,379 | 161 | 0.405 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 56,939 | 0.569 | 20 | 24 | fits | 65,386 | 140 | 0.410 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 63,025 | 0.630 | 20 | 24 | fits | 62,095 | 140 | 0.382 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 62,670 | 0.627 | 20 | 24 | fits | 61,781 | 140 | 0.381 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 55,804 | 0.558 | 20 | 24 | fits | 63,970 | 116 | 0.418 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 62,764 | 0.628 | 20 | 24 | fits | 61,818 | 140 | 0.373 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 54,687 | 0.547 | 20 | 24 | fits | 61,207 | 140 | 0.370 |
| set_name | `aecp_fanout.set_name.if1` | 61,372 | 0.614 | 20 | 24 | fits | 70,322 | 117 | 0.396 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 65,567 | 0.656 | 20 | 24 | fits | 65,905 | 140 | 0.413 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 54,152 | 0.542 | 20 | 24 | fits | 61,260 | 140 | 0.372 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 54,620 | 0.546 | 20 | 24 | fits | 61,652 | 140 | 0.383 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 62,755 | 0.628 | 20 | 24 | fits | 61,839 | 140 | 0.382 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 54,662 | 0.547 | 20 | 24 | fits | 61,182 | 140 | 0.368 |
| BIND_RX | `acmp.bind_rx.if0` | 27,707 | 0.277 | 20 | 20 | fits | 64,341 | 27 (77) | 0.782 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,632 | 0.096 | 20 | 20 | fits | 44,978 | 21 (32) | 0.812 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 13,609 | 0.136 | 20 | 20 | fits | 46,666 | 16 (47) | 0.750 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 17,270 | 0.173 | 20 | 20 | fits | 55,731 | 19 (50) | 0.821 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 13,310 | 0.133 | 20 | 20 | fits | 46,055 | 18 (48) | 0.741 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 22,396 | 0.224 | 20 | 20 | fits | 58,423 | 26 (48) | 0.723 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 12,963 | 0.130 | 20 | 20 | fits | 45,578 | 17 (48) | 0.763 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 12,110 | 0.121 | 20 | 20 | fits | 44,171 | 17 (48) | 0.737 |
| BIND_RX | `acmp.bind_rx.if1` | 23,766 | 0.238 | 20 | 20 | fits | 58,481 | 28 (77) | 0.730 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 9,317 | 0.093 | 20 | 20 | fits | 44,671 | 21 (32) | 0.802 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 14,358 | 0.144 | 20 | 20 | fits | 47,788 | 17 (47) | 0.757 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 17,621 | 0.176 | 20 | 20 | fits | 56,988 | 20 (50) | 0.823 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if1` | 15,495 | 0.155 | 20 | 20 | fits | 48,592 | 20 (48) | 0.755 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 12,478 | 0.125 | 20 | 20 | fits | 45,192 | 18 (48) | 0.734 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 12,067 | 0.121 | 20 | 20 | fits | 44,318 | 18 (48) | 0.725 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if1` | 12,023 | 0.120 | 20 | 20 | fits | 44,276 | 18 (48) | 0.727 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,283 | 0.143 | 20 | 24 | fits | 29,401 | 22 | 0.769 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 30,178 | 0.302 | 20 | 24 | fits | 35,233 | 22 | 0.716 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 24,273 | 0.243 | 20 | 24 | fits | 30,674 | 22 | 0.728 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,416 | 0.174 | 20 | 24 | fits | 30,102 | 22 | 0.722 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 25,365 | 0.254 | 20 | 24 | fits | 30,276 | 22 | 0.728 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 17,682 | 0.177 | 20 | 24 | fits | 30,765 | 22 | 0.725 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 24,805 | 0.248 | 20 | 24 | fits | 29,745 | 22 | 0.735 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 24,009 | 0.240 | 20 | 24 | fits | 40,592 | 31 | 0.703 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 16,915 | 0.169 | 20 | 24 | fits | 29,664 | 22 | 0.745 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 29,827 | 0.298 | 20 | 24 | fits | 35,018 | 23 | 0.641 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 16,387 | 0.164 | 20 | 24 | fits | 29,394 | 22 | 0.753 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 24,680 | 0.247 | 20 | 24 | fits | 29,494 | 22 | 0.762 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 16,167 | 0.162 | 20 | 24 | fits | 29,580 | 22 | 0.729 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 17,707 | 0.177 | 20 | 24 | fits | 30,858 | 22 | 0.738 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 25,806 | 0.258 | 20 | 24 | fits | 30,912 | 22 | 0.738 |
| get_configuration | `aecp.get_configuration.if0` | 14,532 | 0.145 | 20 | 24 | fits | 26,795 | 22 | 0.729 |
| entity_available | `aecp.entity_available.if0` | 23,057 | 0.231 | 20 | 24 | fits | 27,584 | 22 | 0.736 |
| get_name | `aecp.get_name.if0` | 17,277 | 0.173 | 20 | 24 | fits | 29,765 | 22 | 0.745 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 18,906 | 0.189 | 20 | 24 | fits | 31,655 | 29 | 0.720 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 45,069 | 0.451 | 20 | 24 | fits | 50,138 | 61 | 0.691 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 14,906 | 0.149 | 20 | 24 | fits | 27,831 | 22 | 0.752 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 23,239 | 0.232 | 20 | 24 | fits | 26,353 | 22 | 0.714 |
| set_name | `aecp.set_name.if0` | 48,467 | 0.485 | 20 | 24 | fits | 61,524 | 75 | 0.678 |
| lock_entity | `aecp.lock_entity.if0` | 28,227 | 0.282 | 20 | 24 | fits | 36,630 | 47 | 0.717 |
| unlock_entity | `aecp.unlock_entity.if0` | 38,361 | 0.384 | 20 | 24 | fits | 36,587 | 46 | 0.722 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 15,549 | 0.155 | 20 | 24 | fits | 28,505 | 20 | 0.745 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 31,909 | 0.319 | 20 | 24 | fits | 33,395 | 20 | 0.701 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 28,213 | 0.282 | 20 | 24 | fits | 30,138 | 20 | 0.736 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 19,486 | 0.195 | 20 | 24 | fits | 29,589 | 20 | 0.720 |
| get_configuration | `aecp.get_configuration.if1` | 25,486 | 0.255 | 20 | 24 | fits | 26,707 | 20 | 0.737 |
| entity_available | `aecp.entity_available.if1` | 17,001 | 0.170 | 20 | 24 | fits | 26,876 | 20 | 0.725 |
| get_name | `aecp.get_name.if1` | 28,170 | 0.282 | 20 | 24 | fits | 29,784 | 20 | 0.756 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if1` | 28,168 | 0.282 | 20 | 24 | fits | 31,056 | 27 | 0.712 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if1` | 20,578 | 0.206 | 20 | 24 | fits | 30,475 | 29 | 0.747 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if1` | 26,374 | 0.264 | 20 | 24 | fits | 27,628 | 20 | 0.752 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 16,102 | 0.161 | 20 | 24 | fits | 25,821 | 20 | 0.707 |
| set_name | `aecp.set_name.if1` | 44,778 | 0.448 | 20 | 24 | fits | 45,225 | 25 | 0.758 |
| lock_entity | `aecp.lock_entity.if1` | 40,355 | 0.404 | 20 | 24 | fits | 37,506 | 50 | 0.693 |
| unlock_entity | `aecp.unlock_entity.if1` | 31,692 | 0.317 | 20 | 24 | fits | 37,078 | 49 | 0.695 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
