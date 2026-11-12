### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 136 paths and 7 of 996 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.211 (0.462) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.184 (0.425) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.176 (0.396) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.109 (0.290) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.081 (0.406) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.157 (0.406) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.078 (0.383) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.147 (0.383) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.108 (0.291) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.093 (0.283) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.102 (0.285) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.086 (0.274) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.094 (0.279) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.112 (0.294) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.116 (0.297) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.100 (0.289) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.102 (0.340) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.096 (0.347) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.310 (1.496) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.246 (0.670) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.192 (0.694) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.358 (0.665) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.293 (0.758) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.404 (0.758) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.279 (0.709) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.364 (0.709) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.304 (0.655) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.113 (0.606) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.333 (0.700) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.416 (0.700) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.143 (0.412) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.156 (0.451) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.045 (0.246) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.060 (0.246) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.022 (0.204) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.039 (0.204) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.021 (0.598) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.271 (0.598) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.024 (0.424) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.156 (0.424) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.185 (0.389) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.165 (0.389) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.105 (0.282) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.061 (0.282) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.139 (0.510) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.261 (0.620) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.169 (0.552) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 1 | `aecp.get_avb_info.if1` (aecp) | 0.287 (0.670) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.229 (0.587) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.161 (0.536) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.269 (0.645) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 1 | `aecp.get_counters.if1` (aecp) | 0.373 (0.779) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.246 (0.620) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.186 (0.566) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.368 (0.694) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.332 (0.483) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.138 (0.504) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.247 (0.610) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.194 (0.580) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.212 (0.599) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.150 (0.557) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.186 (0.417) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.147 (0.407) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.242 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.206 (0.586) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.246 (0.614) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.149 (0.531) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.254 (0.639) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.279 (0.666) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.249 (0.613) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.259 (0.643) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.157 (0.542) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.155 (0.535) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.262 (0.625) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.153 (0.530) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.223 (0.603) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.242 (0.615) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.456 (0.817) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.350 (0.699) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.168 (0.532) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 1 | `aecp.unknown_command.if1` (aecp) | 0.171 (0.543) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.283 (0.602) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.218 (0.358) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.510 (0.872) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.511 (0.874) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.673 (1.068) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.540 (0.916) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.776 (1.136) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 0.652 (1.012) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.611 (1.025) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.711 (1.089) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.658 (1.046) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.649 (1.008) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.649 (1.009) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.663 (8.461) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-5.adp_available.if0` (backlog-adp@verify-aged2-5) | 9.524 (10.640) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.085 (0.316) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.846 (2.715) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.697 (64.076) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.562 (64.940) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 9.237 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 1.715 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 4.775 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 7.344 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 6.001 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.269 (0.659) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.148 (0.545) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.118 (0.265) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.125 (0.276) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.132 (0.313) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.125 (0.306) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.251 (0.659) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.128 (0.545) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.263 (0.633) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 0.204 (0.579) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 3.169 | fits | 0 srp | 6 | 0 |
| an MRPDU its join timer owes, the longest | 1 | `save-starved.mrpdu.periodic.if1` (save-starved) | 5.799 | fits | 0 srp | 6 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 2.307 | fits | 0 acmp | 76 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.568 | MISS ceiling | 11 acmp | 76 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 2.298 | fits | 0 adp | 76 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.adp.last.if0` (backlog-adp@verify-aged2-5) | 10.527 | fits | 7 adp | 74 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 7.971 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.343 | fits | 0 aecp | 76 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 61.903 | MISS ceiling | 15 aecp | 76 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 2.332 | fits | 0 maap | 76 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.maap.last.if0` (backlog-adp@verify-aged2-5) | 10.564 | fits | 6 maap | 76 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-7.service.srp.first.if0` (backlog-adp@program-aged2-7) | 7.223 | fits | 0 srp | 76 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@program-aged2-7.service.srp.last.if1` (backlog-adp@program-aged2-7) | 10.203 | fits | 31 srp | 76 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.874 (2.347) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.775 (2.206) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.547 (0.548) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.522 (0.523) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.247 (0.248) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.254 (0.254) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.448 (1.515) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.364 (1.425) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.207 | 8 | 160,898 (1.609) | yes | - |
| backlog-adp@blank-1 | 0 | 11.539 | 8 | 160,898 (1.609) | yes | - |
| backlog-adp@blank-2 | 0 | 11.962 | 10 | 161,105 (1.611) | yes | - |
| backlog-adp@blank-3 | 0 | 11.537 | 9 | 163,232 (1.632) | yes | - |
| backlog-adp@blank-4 | 0 | 11.488 | 8 | 167,660 (1.677) | yes | - |
| backlog-adp@blank-5 | 0 | 11.610 | 8 | 160,902 (1.609) | yes | - |
| backlog-adp@blank-6 | 0 | 11.489 | 8 | 167,495 (1.675) | yes | - |
| backlog-adp@blank-7 | 0 | 13.603 | 11 | 164,159 (1.642) | yes | - |
| backlog-adp@program-0 | 0 | 11.558 | 8 | 158,856 (1.589) | yes | - |
| backlog-adp@program-1 | 0 | 11.548 | 8 | 158,980 (1.590) | yes | - |
| backlog-adp@program-2 | 0 | 12.075 | 10 | 167,645 (1.676) | yes | - |
| backlog-adp@program-3 | 0 | 12.207 | 10 | 159,581 (1.596) | yes | - |
| backlog-adp@program-4 | 0 | 10.640 | 7 | 159,142 (1.591) | yes | - |
| backlog-adp@program-5 | 0 | 10.887 | 8 | 159,825 (1.598) | yes | - |
| backlog-adp@program-6 | 0 | 11.044 | 10 | 161,600 (1.616) | yes | - |
| backlog-adp@program-7 | 0 | 10.695 | 7 | 162,325 (1.623) | yes | - |
| backlog-adp@verify-0 | 0 | 11.996 | 10 | 160,684 (1.607) | yes | - |
| backlog-adp@verify-1 | 0 | 11.686 | 9 | 165,093 (1.651) | yes | - |
| backlog-adp@verify-2 | 0 | 11.545 | 8 | 161,522 (1.615) | yes | - |
| backlog-adp@verify-3 | 0 | 11.431 | 8 | 160,473 (1.605) | yes | - |
| backlog-adp@verify-4 | 0 | 11.530 | 8 | 165,776 (1.658) | yes | - |
| backlog-adp@verify-5 | 0 | 11.490 | 7 | 166,597 (1.666) | yes | - |
| backlog-adp@verify-6 | 0 | 13.019 | 11 | 165,776 (1.658) | yes | - |
| backlog-adp@verify-7 | 0 | 11.940 | 10 | 165,924 (1.659) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.450 | 9 | 164,610 (1.646) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.164 | 7 | 163,982 (1.640) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.459 | 8 | 160,633 (1.606) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.546 | 8 | 161,501 (1.615) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 11.480 | 8 | 167,989 (1.680) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 12.051 | 10 | 164,199 (1.642) | yes | - |
| backlog-adp@blank-aged2-6 | 1 | 11.445 | 8 | 163,142 (1.631) | yes | - |
| backlog-adp@blank-aged2-7 | 1 | 12.326 | 8 | 163,484 (1.635) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.970 | 10 | 160,885 (1.609) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.626 | 9 | 164,610 (1.646) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.515 | 9 | 160,675 (1.607) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.459 | 8 | 161,092 (1.611) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.558 | 8 | 165,837 (1.658) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.491 | 8 | 167,966 (1.680) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 13.468 | 11 | 163,978 (1.640) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 12.632 | 9 | 162,905 (1.629) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.263 | 8 | 159,235 (1.592) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.357 | 8 | 158,609 (1.586) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.776 | 10 | 159,718 (1.597) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 11.576 | 9 | 165,612 (1.656) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.568 | 8 | 163,825 (1.638) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 11.351 | 7 | 162,322 (1.623) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.553 | 8 | 167,852 (1.679) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 11.764 | 8 | 165,511 (1.655) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.517 | 8 | 158,642 (1.586) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.405 | 8 | 158,534 (1.585) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.542 | 8 | 159,314 (1.593) | yes | - |
| backlog-adp@program-aged1-3 | 1 | 11.811 | 9 | 164,126 (1.641) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.583 | 9 | 162,685 (1.627) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.495 | 8 | 160,413 (1.604) | yes | - |
| backlog-adp@program-aged1-6 | 1 | 11.315 | 7 | 159,409 (1.594) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 12.033 | 9 | 162,167 (1.622) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.834 | 9 | 166,378 (1.664) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.365 | 9 | 163,118 (1.631) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.476 | 8 | 165,887 (1.659) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 11.295 | 7 | 163,050 (1.631) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.497 | 8 | 167,488 (1.675) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 11.622 | 8 | 165,277 (1.653) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.786 | 10 | 163,471 (1.635) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 13.246 | 11 | 167,008 (1.670) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.512 | 8 | 160,331 (1.603) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.943 | 8 | 164,250 (1.643) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 12.007 | 10 | 160,819 (1.608) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.591 | 9 | 162,897 (1.629) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.935 | 8 | 163,342 (1.633) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.492 | 8 | 166,482 (1.665) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.588 | 8 | 167,461 (1.675) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 13.507 | 11 | 163,291 (1.633) | yes | - |
| backlog | 0 | 9.369 | 8 | 173,253 (1.733) | yes | - |
| backlog-adp | 0 | 10.678 | 8 | 163,269 (1.633) | yes | - |
| backlog-adp-refill | 0 | 40.897 | 23 | 163,269 (1.633) | yes | - |
| backlog-owed | 0 | 65.344 | 23 | 168,877 (1.689) | yes | - |

Composed maximum over the 4 backlog windows: 173,253 CPU cycles (1.733 ms), backlog.
Over the windows that released their whole load only: 173,253 (1.733 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 123148 | 0 | 120,238 (1.202) | fits |
| save-held | 2738 | 0 | 165,952 (1.660) | fits |
| save-starved | 57691 | 0 | 166,966 (1.670) | fits |
| acmp-notk | 4871 | 0 | 120,238 (1.202) | fits |
| backlog-adp@blank-0 | 548 | 0 | 160,898 (1.609) | fits |
| backlog-adp@blank-1 | 548 | 0 | 160,898 (1.609) | fits |
| backlog-adp@blank-2 | 550 | 0 | 161,105 (1.611) | fits |
| backlog-adp@blank-3 | 549 | 0 | 163,232 (1.632) | fits |
| backlog-adp@blank-4 | 550 | 0 | 167,660 (1.677) | fits |
| backlog-adp@blank-5 | 550 | 0 | 160,902 (1.609) | fits |
| backlog-adp@blank-6 | 550 | 0 | 167,495 (1.675) | fits |
| backlog-adp@blank-7 | 553 | 0 | 164,159 (1.642) | fits |
| backlog-adp@program-0 | 922 | 0 | 158,856 (1.589) | fits |
| backlog-adp@program-1 | 922 | 0 | 158,980 (1.590) | fits |
| backlog-adp@program-2 | 924 | 0 | 167,645 (1.676) | fits |
| backlog-adp@program-3 | 924 | 0 | 159,581 (1.596) | fits |
| backlog-adp@program-4 | 925 | 0 | 159,142 (1.591) | fits |
| backlog-adp@program-5 | 925 | 0 | 159,825 (1.598) | fits |
| backlog-adp@program-6 | 927 | 0 | 161,600 (1.616) | fits |
| backlog-adp@program-7 | 927 | 0 | 162,325 (1.623) | fits |
| backlog-adp@verify-0 | 1285 | 0 | 160,684 (1.607) | fits |
| backlog-adp@verify-1 | 1284 | 0 | 165,093 (1.651) | fits |
| backlog-adp@verify-2 | 1285 | 0 | 161,522 (1.615) | fits |
| backlog-adp@verify-3 | 1285 | 0 | 160,473 (1.605) | fits |
| backlog-adp@verify-4 | 1285 | 0 | 165,776 (1.658) | fits |
| backlog-adp@verify-5 | 1285 | 0 | 166,597 (1.666) | fits |
| backlog-adp@verify-6 | 1288 | 0 | 165,776 (1.658) | fits |
| backlog-adp@verify-7 | 1287 | 0 | 165,924 (1.659) | fits |
| backlog-adp@blank-aged2-0 | 802 | 0 | 164,610 (1.646) | fits |
| backlog-adp@blank-aged2-1 | 807 | 0 | 163,982 (1.640) | fits |
| backlog-adp@blank-aged2-2 | 814 | 0 | 160,633 (1.606) | fits |
| backlog-adp@blank-aged2-3 | 821 | 0 | 161,501 (1.615) | fits |
| backlog-adp@blank-aged2-4 | 827 | 0 | 167,989 (1.680) | fits |
| backlog-adp@blank-aged2-5 | 836 | 0 | 164,199 (1.642) | fits |
| backlog-adp@blank-aged2-6 | 841 | 0 | 163,142 (1.631) | fits |
| backlog-adp@blank-aged2-7 | 848 | 0 | 163,484 (1.635) | fits |
| backlog-adp@blank-aged1-0 | 750 | 0 | 160,885 (1.609) | fits |
| backlog-adp@blank-aged1-1 | 756 | 0 | 164,610 (1.646) | fits |
| backlog-adp@blank-aged1-2 | 762 | 0 | 160,675 (1.607) | fits |
| backlog-adp@blank-aged1-3 | 768 | 0 | 161,092 (1.611) | fits |
| backlog-adp@blank-aged1-4 | 775 | 0 | 165,837 (1.658) | fits |
| backlog-adp@blank-aged1-5 | 781 | 0 | 167,966 (1.680) | fits |
| backlog-adp@blank-aged1-6 | 791 | 0 | 163,978 (1.640) | fits |
| backlog-adp@blank-aged1-7 | 796 | 0 | 162,905 (1.629) | fits |
| backlog-adp@program-aged2-0 | 1170 | 0 | 159,235 (1.592) | fits |
| backlog-adp@program-aged2-1 | 1177 | 0 | 158,609 (1.586) | fits |
| backlog-adp@program-aged2-2 | 1185 | 0 | 159,718 (1.597) | fits |
| backlog-adp@program-aged2-3 | 1191 | 0 | 165,612 (1.656) | fits |
| backlog-adp@program-aged2-4 | 1197 | 0 | 163,825 (1.638) | fits |
| backlog-adp@program-aged2-5 | 1203 | 0 | 162,322 (1.623) | fits |
| backlog-adp@program-aged2-6 | 1210 | 0 | 167,852 (1.679) | fits |
| backlog-adp@program-aged2-7 | 1217 | 0 | 165,511 (1.655) | fits |
| backlog-adp@program-aged1-0 | 1118 | 0 | 158,642 (1.586) | fits |
| backlog-adp@program-aged1-1 | 1124 | 0 | 158,534 (1.585) | fits |
| backlog-adp@program-aged1-2 | 1131 | 0 | 159,314 (1.593) | fits |
| backlog-adp@program-aged1-3 | 1139 | 0 | 164,126 (1.641) | fits |
| backlog-adp@program-aged1-4 | 1145 | 0 | 162,685 (1.627) | fits |
| backlog-adp@program-aged1-5 | 1151 | 0 | 160,413 (1.604) | fits |
| backlog-adp@program-aged1-6 | 1157 | 0 | 159,409 (1.594) | fits |
| backlog-adp@program-aged1-7 | 1165 | 0 | 162,167 (1.622) | fits |
| backlog-adp@verify-aged2-0 | 1537 | 0 | 166,378 (1.664) | fits |
| backlog-adp@verify-aged2-1 | 1543 | 0 | 163,118 (1.631) | fits |
| backlog-adp@verify-aged2-2 | 1549 | 0 | 165,887 (1.659) | fits |
| backlog-adp@verify-aged2-3 | 1555 | 0 | 163,050 (1.631) | fits |
| backlog-adp@verify-aged2-4 | 1562 | 0 | 167,488 (1.675) | fits |
| backlog-adp@verify-aged2-5 | 1569 | 0 | 165,277 (1.653) | fits |
| backlog-adp@verify-aged2-6 | 1577 | 0 | 163,471 (1.635) | fits |
| backlog-adp@verify-aged2-7 | 1585 | 0 | 167,008 (1.670) | fits |
| backlog-adp@verify-aged1-0 | 1483 | 0 | 160,331 (1.603) | fits |
| backlog-adp@verify-aged1-1 | 1490 | 0 | 164,250 (1.643) | fits |
| backlog-adp@verify-aged1-2 | 1498 | 0 | 160,819 (1.608) | fits |
| backlog-adp@verify-aged1-3 | 1504 | 0 | 162,897 (1.629) | fits |
| backlog-adp@verify-aged1-4 | 1510 | 0 | 163,342 (1.633) | fits |
| backlog-adp@verify-aged1-5 | 1516 | 0 | 166,482 (1.665) | fits |
| backlog-adp@verify-aged1-6 | 1523 | 0 | 167,461 (1.675) | fits |
| backlog-adp@verify-aged1-7 | 1532 | 0 | 163,291 (1.633) | fits |
| adp-advertise | 599 | 0 | 120,238 (1.202) | fits |
| maap | 349 | 0 | 120,238 (1.202) | fits |
| acmp-noresp | 2714 | 0 | 120,238 (1.202) | fits |
| save | 611 | 0 | 120,238 (1.202) | fits |
| srp | 306 | 0 | 186,522 (1.865) | fits |
| backlog | 288 | 0 | 173,253 (1.733) | fits |
| backlog-adp | 313 | 0 | 163,269 (1.633) | fits |
| backlog-adp-refill | 328 | 0 | 163,269 (1.633) | fits |
| backlog-owed | 309 | 0 | 168,877 (1.689) | fits |
| acmp-disc | 1387 | 0 | 120,720 (1.207) | fits |
| adp-link | 91 | 0 | 120,238 (1.202) | fits |
| adp-gm | 89 | 0 | 120,238 (1.202) | fits |
| adp-discover | 89 | 0 | 120,238 (1.202) | fits |
| control | 89 | 0 | 120,238 (1.202) | fits |
| aecp-fanout | 143 | 0 | 120,238 (1.202) | fits |
| acmp-cmd | 105 | 0 | 120,238 (1.202) | fits |
| aecp | 132 | 0 | 120,238 (1.202) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +10.292 ms, 76,933 (0.769 ms), read-back | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 10.281 (20) | 9.719 |
| backlog-adp@blank-aged2-1 | 2 | none | +10.001 ms, 76,939 (0.769 ms), read-back | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 9.989 (20) | 10.011 |
| backlog-adp@blank-aged2-2 | 2 | +9.516 ms, 77,001 (0.770 ms), read-back | none | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 10.866 (20) | 9.134 |
| backlog-adp@blank-aged2-3 | 2 | +8.119 ms, 77,164 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 10.952 (20) | 9.048 |
| backlog-adp@blank-aged2-4 | 2 | +6.384 ms, 77,057 (0.771 ms), read-back | none | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 10.886 (20) | 9.114 |
| backlog-adp@blank-aged2-5 | 2 | +4.953 ms, 77,161 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 10.990 (20) | 9.010 |
| backlog-adp@blank-aged2-6 | 2 | +4.752 ms, 77,161 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 10.855 (20) | 9.145 |
| backlog-adp@blank-aged2-7 | 2 | +4.637 ms, 77,223 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 10.704 (20) | 9.296 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.aecp.last.if1` | 10.117 (20) | 9.883 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.aecp.last.if1` | 10.279 (20) | 9.721 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.aecp.last.if1` | 10.167 (20) | 9.833 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.aecp.last.if1` | 10.108 (20) | 9.892 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.aecp.last.if1` | 10.203 (20) | 9.797 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.aecp.last.if1` | 10.136 (20) | 9.864 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.aecp.last.if1` | 10.217 (20) | 9.783 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.aecp.last.if1` | 9.939 (20) | 10.061 |
| backlog-adp@program-aged2-0 | 2 | none | +10.060 ms, 80,574 (0.806 ms), issue | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 10.049 (20) | 9.951 |
| backlog-adp@program-aged2-1 | 2 | none | +10.154 ms, 80,653 (0.807 ms), issue | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 10.142 (20) | 9.858 |
| backlog-adp@program-aged2-2 | 2 | +9.484 ms, 80,686 (0.807 ms), issue | none | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 10.878 (20) | 9.122 |
| backlog-adp@program-aged2-3 | 2 | +8.105 ms, 80,791 (0.808 ms), issue | none | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 10.989 (20) | 9.011 |
| backlog-adp@program-aged2-4 | 2 | +6.336 ms, 80,856 (0.809 ms), issue | none | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 10.978 (20) | 9.022 |
| backlog-adp@program-aged2-5 | 2 | +6.180 ms, 80,856 (0.809 ms), issue | none | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 10.758 (20) | 9.242 |
| backlog-adp@program-aged2-6 | 2 | +4.721 ms, 80,960 (0.810 ms), issue | none | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 10.959 (20) | 9.041 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 10.850 (20) | 9.150 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.aecp.last.if1` | 10.125 (20) | 9.875 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.aecp.last.if1` | 10.011 (20) | 9.989 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.aecp.last.if1` | 10.146 (20) | 9.854 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.aecp.last.if1` | 9.923 (20) | 10.077 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.aecp.last.if1` | 10.193 (20) | 9.807 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.aecp.last.if1` | 10.106 (20) | 9.894 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.aecp.last.if1` | 9.924 (20) | 10.076 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.aecp.last.if1` | 10.134 (20) | 9.866 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.011 ms, 77,962 (0.780 ms), read-back | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 9.999 (20) | 10.001 |
| backlog-adp@verify-aged2-1 | 2 | none | +10.194 ms, 78,122 (0.781 ms), read-back | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 10.182 (20) | 9.818 |
| backlog-adp@verify-aged2-2 | 2 | none | none | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 10.885 (20) | 9.115 |
| backlog-adp@verify-aged2-3 | 2 | none | none | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 10.703 (20) | 9.297 |
| backlog-adp@verify-aged2-4 | 2 | none | none | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 10.903 (20) | 9.097 |
| backlog-adp@verify-aged2-5 | 2 | none | none | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 11.027 (20) | 8.973 |
| backlog-adp@verify-aged2-6 | 2 | +4.836 ms, 78,181 (0.782 ms), read-back | none | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 10.885 (20) | 9.115 |
| backlog-adp@verify-aged2-7 | 2 | none | none | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 10.952 (20) | 9.048 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.aecp.last.if1` | 10.146 (20) | 9.854 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.aecp.last.if1` | 10.034 (20) | 9.966 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.aecp.last.if1` | 10.144 (20) | 9.856 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.aecp.last.if1` | 10.130 (20) | 9.870 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.aecp.last.if1` | 10.028 (20) | 9.972 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.aecp.last.if1` | 10.126 (20) | 9.874 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.aecp.last.if1` | 10.220 (20) | 9.780 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.aecp.last.if1` | 10.081 (20) | 9.919 |

Least margin over the aged windows: 8.973 ms, `backlog-adp@verify-aged2-5.service.aecp.last.if1` at 11.027 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22110.074 | 22,150 | 370 | 2 | 32.632 | yes | within |
| save-held | 4697.016 | 12,110 | 370 | - | 13.683 | no | within |
| save-starved | 12088.526 | 12,110 | 370 | - | 35.283 | yes | within |
| save | 4697.463 | 12,110 | 370 | - | 13.319 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1056 | 80,433 (0.804) | 78,735 (0.787) |
| save-held | 1526 | 109,419 (1.094) | 79,151 (0.792) |
| save-starved | 686 | 80,750 (0.807) | 78,878 (0.789) |
| acmp-notk | 1065 | 110,035 (1.100) | 79,297 (0.793) |
| backlog-adp@blank-0 | 337 | 96,060 (0.961) | 76,718 (0.767) |
| backlog-adp@blank-1 | 337 | 96,126 (0.961) | 76,639 (0.766) |
| backlog-adp@blank-2 | 337 | 95,917 (0.959) | 76,619 (0.766) |
| backlog-adp@blank-3 | 337 | 95,549 (0.955) | 76,786 (0.768) |
| backlog-adp@blank-4 | 337 | 95,703 (0.957) | 76,764 (0.768) |
| backlog-adp@blank-5 | 337 | 95,939 (0.959) | 76,660 (0.767) |
| backlog-adp@blank-6 | 337 | 96,182 (0.962) | 76,843 (0.768) |
| backlog-adp@blank-7 | 338 | 95,927 (0.959) | 76,658 (0.767) |
| backlog-adp@program-0 | 443 | 105,763 (1.058) | 79,190 (0.792) |
| backlog-adp@program-1 | 443 | 105,763 (1.058) | 79,233 (0.792) |
| backlog-adp@program-2 | 443 | 105,763 (1.058) | 79,337 (0.793) |
| backlog-adp@program-3 | 444 | 105,763 (1.058) | 79,416 (0.794) |
| backlog-adp@program-4 | 444 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@program-5 | 444 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@program-6 | 444 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@program-7 | 444 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@verify-0 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-1 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-2 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-3 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-4 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-5 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-6 | 547 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-7 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@blank-aged2-0 | 335 | 76,933 (0.769) | 76,141 (0.761) |
| backlog-adp@blank-aged2-1 | 335 | 76,939 (0.769) | 76,141 (0.761) |
| backlog-adp@blank-aged2-2 | 335 | 77,001 (0.770) | 76,203 (0.762) |
| backlog-adp@blank-aged2-3 | 335 | 77,164 (0.772) | 76,266 (0.763) |
| backlog-adp@blank-aged2-4 | 335 | 77,057 (0.771) | 76,139 (0.761) |
| backlog-adp@blank-aged2-5 | 335 | 77,161 (0.772) | 76,243 (0.762) |
| backlog-adp@blank-aged2-6 | 335 | 77,161 (0.772) | 76,243 (0.762) |
| backlog-adp@blank-aged2-7 | 336 | 95,573 (0.956) | 76,879 (0.769) |
| backlog-adp@blank-aged1-0 | 335 | 96,065 (0.961) | 76,719 (0.767) |
| backlog-adp@blank-aged1-1 | 335 | 95,261 (0.953) | 76,556 (0.766) |
| backlog-adp@blank-aged1-2 | 335 | 95,509 (0.955) | 76,765 (0.768) |
| backlog-adp@blank-aged1-3 | 335 | 95,645 (0.956) | 76,683 (0.767) |
| backlog-adp@blank-aged1-4 | 335 | 96,029 (0.960) | 76,787 (0.768) |
| backlog-adp@blank-aged1-5 | 335 | 96,085 (0.961) | 76,787 (0.768) |
| backlog-adp@blank-aged1-6 | 336 | 95,981 (0.960) | 76,683 (0.767) |
| backlog-adp@blank-aged1-7 | 336 | 96,044 (0.960) | 76,866 (0.769) |
| backlog-adp@program-aged2-0 | 441 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@program-aged2-1 | 441 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@program-aged2-2 | 441 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@program-aged2-3 | 441 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@program-aged2-4 | 441 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@program-aged2-5 | 441 | 105,763 (1.058) | 78,934 (0.789) |
| backlog-adp@program-aged2-6 | 441 | 105,763 (1.058) | 78,940 (0.789) |
| backlog-adp@program-aged2-7 | 442 | 105,763 (1.058) | 79,003 (0.790) |
| backlog-adp@program-aged1-0 | 441 | 105,763 (1.058) | 79,190 (0.792) |
| backlog-adp@program-aged1-1 | 441 | 105,763 (1.058) | 79,252 (0.793) |
| backlog-adp@program-aged1-2 | 441 | 105,763 (1.058) | 79,353 (0.794) |
| backlog-adp@program-aged1-3 | 441 | 105,763 (1.058) | 79,337 (0.793) |
| backlog-adp@program-aged1-4 | 441 | 105,763 (1.058) | 79,233 (0.792) |
| backlog-adp@program-aged1-5 | 441 | 105,763 (1.058) | 79,209 (0.792) |
| backlog-adp@program-aged1-6 | 441 | 105,763 (1.058) | 79,416 (0.794) |
| backlog-adp@program-aged1-7 | 442 | 105,763 (1.058) | 79,231 (0.792) |
| backlog-adp@verify-aged2-0 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged2-1 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged2-2 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged2-3 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged2-4 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged2-5 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged2-6 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged2-7 | 547 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged1-0 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged1-1 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged1-2 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged1-3 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged1-4 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged1-5 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged1-6 | 546 | 105,763 (1.058) | 79,261 (0.793) |
| backlog-adp@verify-aged1-7 | 547 | 105,763 (1.058) | 79,261 (0.793) |
| adp-advertise | 577 | 31,651 (0.317) | 3,214 (0.032) |
| maap | 327 | 31,614 (0.316) | 3,214 (0.032) |
| acmp-noresp | 615 | 109,723 (1.097) | 79,297 (0.793) |
| save | 585 | 108,654 (1.087) | 79,084 (0.791) |
| srp | 278 | 31,648 (0.316) | 3,460 (0.035) |
| backlog | 266 | 31,651 (0.317) | 3,255 (0.033) |
| backlog-adp | 271 | 31,651 (0.317) | 3,256 (0.033) |
| backlog-adp-refill | 274 | 31,651 (0.317) | 3,214 (0.032) |
| backlog-owed | 277 | 31,651 (0.317) | 3,214 (0.032) |
| acmp-disc | 336 | 106,287 (1.063) | 78,842 (0.788) |
| adp-link | 79 | 31,304 (0.313) | 3,214 (0.032) |
| adp-gm | 79 | 31,304 (0.313) | 3,214 (0.032) |
| adp-discover | 79 | 31,304 (0.313) | 3,214 (0.032) |
| control | 79 | 31,304 (0.313) | 3,214 (0.032) |
| aecp-fanout | 93 | 31,304 (0.313) | 3,214 (0.032) |
| acmp-cmd | 67 | 31,304 (0.313) | 3,214 (0.032) |
| aecp | 88 | 31,304 (0.313) | 3,214 (0.032) |

Longest pass that carries a step: 110,035 CPU cycles (1.100 ms), acmp-notk; longest step: 79,416 (0.794 ms), backlog-adp@program-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 165,013 | 1.650 | 20 | 200 | fits | 165,952 | 234 | 0.474 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 923,689 | 9.237 | 20 | 20 | fits | 158,749 | 133 | 0.489 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 462,279 | 4.623 | 20 | 24 | fits | 58,794 | 46 | 0.544 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 725,465 | 7.255 | 20 | 50 | fits | 156,128 | 150 | 0.584 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 590,705 | 5.907 | 20 | 20 | fits | 145,654 | 49 | 0.410 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 188,624 | 1.886 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if1` | 298,594 | 2.986 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 277,980 | 2.780 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if1` | 516,896 | 5.169 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 311,347 | 3.113 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if1` | 570,317 | 5.703 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 171,503 | 1.715 | 20 | 200 | fits | 158,893 | 222 | 0.369 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 922,255 | 9.223 | 20 | 20 | fits | 148,355 | 128 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 477,533 | 4.775 | 20 | 24 | fits | 75,482 | 65 | 0.539 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 734,425 | 7.344 | 20 | 50 | fits | 157,140 | 156 | 0.582 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 600,056 | 6.001 | 20 | 20 | fits | 149,410 | 61 | 0.444 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 189,309 | 1.893 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if1` | 299,476 | 2.995 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 274,199 | 2.742 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if1` | 516,916 | 5.169 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 316,882 | 3.169 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if1` | 579,855 | 5.799 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 30,354 | 0.304 | 20 | 20 | fits | 34,678 | 29 (14) | 0.790 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 11,342 | 0.113 | 20 | 20 | fits | 38,521 | 19 (14) | 0.887 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 922,842 | 9.228 | 20 | 20 | fits | 150,929 | 119 | 0.570 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 229,775 | 2.298 | 20 | 200 | fits | 155,002 | 204 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 1,022,630 | 10.226 | 20 | 200 | fits | 150,929 | 119 | 0.570 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 230,687 | 2.307 | 20 | 20 | fits | 155,002 | 204 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 1,023,326 | 10.233 | 20 | 20 | fits | 150,929 | 119 | 0.570 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 234,272 | 2.343 | 20 | 24 | fits | 155,002 | 204 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,085,196 | 10.852 | 20 | 24 | fits | 58,435 | 42 | 0.614 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 233,232 | 2.332 | 20 | 50 | fits | 155,002 | 204 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 875,377 | 8.754 | 20 | 50 | fits | 155,983 | 179 | 0.532 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 393,675 | 3.937 | 20 | 20 | fits | 160,898 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 717,314 | 7.173 | 20 | 20 | fits | 159,219 | 59 | 0.416 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 769,910 | 7.699 | 20 | 20 | fits | 155,245 | 176 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 163,417 | 1.634 | 20 | 200 | fits | 156,077 | 208 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 805,617 | 8.056 | 20 | 200 | fits | 155,245 | 176 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 164,329 | 1.643 | 20 | 20 | fits | 156,077 | 208 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 956,503 | 9.565 | 20 | 20 | fits | 150,190 | 119 | 0.535 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 167,914 | 1.679 | 20 | 24 | fits | 156,077 | 208 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,018,333 | 10.183 | 20 | 24 | fits | 58,395 | 42 | 0.617 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 166,874 | 1.669 | 20 | 50 | fits | 156,077 | 208 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 809,293 | 8.093 | 20 | 50 | fits | 155,245 | 176 | 0.551 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 327,317 | 3.273 | 20 | 20 | fits | 160,898 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 651,968 | 6.520 | 20 | 20 | fits | 156,845 | 53 | 0.398 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 749,343 | 7.493 | 20 | 20 | fits | 159,623 | 164 | 0.571 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 152,430 | 1.524 | 20 | 200 | fits | 156,060 | 208 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 798,251 | 7.983 | 20 | 200 | fits | 159,623 | 164 | 0.571 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 153,342 | 1.533 | 20 | 20 | fits | 156,060 | 208 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 948,520 | 9.485 | 20 | 20 | fits | 149,573 | 124 | 0.590 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 156,927 | 1.569 | 20 | 24 | fits | 156,060 | 208 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,010,923 | 10.109 | 20 | 24 | fits | 58,968 | 46 | 0.547 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 155,887 | 1.559 | 20 | 50 | fits | 156,060 | 208 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 951,500 | 9.515 | 20 | 50 | fits | 149,573 | 124 | 0.590 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 316,537 | 3.165 | 20 | 20 | fits | 161,105 | 80 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 640,224 | 6.402 | 20 | 20 | fits | 154,833 | 53 | 0.329 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 829,371 | 8.294 | 20 | 20 | fits | 162,723 | 122 | 0.586 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 157,597 | 1.576 | 20 | 200 | fits | 153,192 | 220 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 955,991 | 9.560 | 20 | 200 | fits | 162,723 | 122 | 0.586 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 158,509 | 1.585 | 20 | 20 | fits | 153,192 | 220 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 956,687 | 9.567 | 20 | 20 | fits | 162,723 | 122 | 0.586 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 162,094 | 1.621 | 20 | 24 | fits | 153,192 | 220 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,018,730 | 10.187 | 20 | 24 | fits | 48,858 | 39 | 0.627 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 161,054 | 1.611 | 20 | 50 | fits | 153,192 | 220 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 324,008 | 3.240 | 20 | 50 | fits | 153,977 | 205 | 0.520 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 487,175 | 4.872 | 20 | 20 | fits | 163,232 | 41 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 794,864 | 7.949 | 20 | 20 | fits | 154,331 | 55 | 0.418 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 758,438 | 7.584 | 20 | 20 | fits | 167,660 | 163 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 152,789 | 1.528 | 20 | 200 | fits | 151,701 | 220 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 790,419 | 7.904 | 20 | 200 | fits | 167,660 | 163 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 153,701 | 1.537 | 20 | 20 | fits | 151,701 | 220 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 951,374 | 9.514 | 20 | 20 | fits | 149,806 | 119 | 0.562 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 157,286 | 1.573 | 20 | 24 | fits | 151,701 | 220 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,013,694 | 10.137 | 20 | 24 | fits | 58,885 | 46 | 0.547 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 156,246 | 1.562 | 20 | 50 | fits | 151,701 | 220 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 794,095 | 7.941 | 20 | 50 | fits | 167,660 | 163 | 0.579 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 316,782 | 3.168 | 20 | 20 | fits | 160,991 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 792,015 | 7.920 | 20 | 20 | fits | 167,660 | 163 | 0.579 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 772,158 | 7.722 | 20 | 20 | fits | 158,118 | 157 | 0.595 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 164,713 | 1.647 | 20 | 200 | fits | 155,533 | 208 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 804,738 | 8.047 | 20 | 200 | fits | 158,118 | 157 | 0.595 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 165,625 | 1.656 | 20 | 20 | fits | 155,533 | 208 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 963,335 | 9.633 | 20 | 20 | fits | 157,901 | 134 | 0.559 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 169,210 | 1.692 | 20 | 24 | fits | 155,533 | 208 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,025,548 | 10.255 | 20 | 24 | fits | 58,778 | 46 | 0.543 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 168,170 | 1.682 | 20 | 50 | fits | 155,533 | 208 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 966,315 | 9.663 | 20 | 50 | fits | 157,901 | 134 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 328,617 | 3.286 | 20 | 20 | fits | 160,902 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 806,334 | 8.063 | 20 | 20 | fits | 158,118 | 157 | 0.595 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 862,949 | 8.629 | 20 | 20 | fits | 161,661 | 138 | 0.573 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 152,247 | 1.522 | 20 | 200 | fits | 154,037 | 204 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 963,310 | 9.633 | 20 | 200 | fits | 161,661 | 138 | 0.573 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 153,159 | 1.532 | 20 | 20 | fits | 154,037 | 204 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 964,006 | 9.640 | 20 | 20 | fits | 161,661 | 138 | 0.573 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 156,744 | 1.567 | 20 | 24 | fits | 154,037 | 204 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,013,283 | 10.133 | 20 | 24 | fits | 45,842 | 33 | 0.605 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 155,704 | 1.557 | 20 | 50 | fits | 154,037 | 204 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 966,986 | 9.670 | 20 | 50 | fits | 161,661 | 138 | 0.573 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 316,151 | 3.162 | 20 | 20 | fits | 160,902 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 803,245 | 8.032 | 20 | 20 | fits | 167,495 | 167 | 0.573 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 285,864 | 2.859 | 20 | 20 | fits | 156,230 | 194 | 0.564 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 158,013 | 1.580 | 20 | 200 | fits | 151,768 | 220 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 313,634 | 3.136 | 20 | 200 | fits | 156,230 | 194 | 0.564 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 158,925 | 1.589 | 20 | 20 | fits | 151,768 | 220 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 944,327 | 9.443 | 20 | 20 | fits | 149,338 | 113 | 0.571 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 162,510 | 1.625 | 20 | 24 | fits | 151,768 | 220 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,020,050 | 10.200 | 20 | 24 | fits | 72,288 | 59 | 0.514 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 161,470 | 1.615 | 20 | 50 | fits | 151,768 | 220 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 317,310 | 3.173 | 20 | 50 | fits | 156,230 | 194 | 0.564 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 481,404 | 4.814 | 20 | 20 | fits | 164,159 | 42 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 795,889 | 7.959 | 20 | 20 | fits | 145,012 | 49 | 0.352 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 836,070 | 8.361 | 20 | 20 | fits | 154,128 | 121 | 0.585 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 162,461 | 1.625 | 20 | 200 | fits | 152,465 | 219 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 953,267 | 9.533 | 20 | 200 | fits | 154,128 | 121 | 0.585 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 163,373 | 1.634 | 20 | 20 | fits | 152,465 | 219 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 953,963 | 9.540 | 20 | 20 | fits | 154,128 | 121 | 0.585 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 166,958 | 1.670 | 20 | 24 | fits | 152,465 | 219 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,016,280 | 10.163 | 20 | 24 | fits | 58,882 | 42 | 0.623 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 165,918 | 1.659 | 20 | 50 | fits | 152,465 | 219 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 792,602 | 7.926 | 20 | 50 | fits | 158,856 | 166 | 0.541 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 324,166 | 3.242 | 20 | 20 | fits | 158,703 | 79 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 631,666 | 6.317 | 20 | 20 | fits | 154,604 | 53 | 0.318 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 767,787 | 7.678 | 20 | 20 | fits | 153,373 | 159 | 0.585 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 162,604 | 1.626 | 20 | 200 | fits | 155,543 | 208 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 795,375 | 7.954 | 20 | 200 | fits | 153,373 | 159 | 0.585 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 163,516 | 1.635 | 20 | 20 | fits | 155,543 | 208 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 952,998 | 9.530 | 20 | 20 | fits | 156,927 | 134 | 0.552 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 167,101 | 1.671 | 20 | 24 | fits | 155,543 | 208 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,015,347 | 10.153 | 20 | 24 | fits | 58,914 | 46 | 0.547 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 166,061 | 1.661 | 20 | 50 | fits | 155,543 | 208 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 955,978 | 9.560 | 20 | 50 | fits | 156,927 | 134 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 324,586 | 3.246 | 20 | 20 | fits | 158,980 | 79 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 632,205 | 6.322 | 20 | 20 | fits | 154,771 | 54 | 0.319 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 775,991 | 7.760 | 20 | 20 | fits | 167,645 | 162 | 0.580 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 156,100 | 1.561 | 20 | 200 | fits | 151,974 | 220 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 807,724 | 8.077 | 20 | 200 | fits | 167,645 | 162 | 0.580 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 157,012 | 1.570 | 20 | 20 | fits | 151,974 | 220 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 955,812 | 9.558 | 20 | 20 | fits | 147,392 | 116 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 160,597 | 1.606 | 20 | 24 | fits | 151,974 | 220 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,018,090 | 10.181 | 20 | 24 | fits | 58,843 | 46 | 0.544 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 159,557 | 1.596 | 20 | 50 | fits | 151,974 | 220 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 811,400 | 8.114 | 20 | 50 | fits | 167,645 | 162 | 0.580 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 318,378 | 3.184 | 20 | 20 | fits | 159,276 | 80 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 809,320 | 8.093 | 20 | 20 | fits | 167,645 | 162 | 0.580 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 839,128 | 8.391 | 20 | 20 | fits | 152,631 | 114 | 0.605 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 155,470 | 1.555 | 20 | 200 | fits | 154,279 | 205 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 935,745 | 9.357 | 20 | 200 | fits | 152,631 | 114 | 0.605 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 156,382 | 1.564 | 20 | 20 | fits | 154,279 | 205 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 936,441 | 9.364 | 20 | 20 | fits | 152,631 | 114 | 0.605 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 159,967 | 1.600 | 20 | 24 | fits | 154,279 | 205 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,012,327 | 10.123 | 20 | 24 | fits | 62,736 | 52 | 0.581 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 158,927 | 1.589 | 20 | 50 | fits | 154,279 | 205 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 317,846 | 3.178 | 20 | 50 | fits | 150,252 | 215 | 0.493 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 477,362 | 4.774 | 20 | 20 | fits | 159,581 | 43 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 784,710 | 7.847 | 20 | 20 | fits | 154,485 | 53 | 0.316 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 750,969 | 7.510 | 20 | 20 | fits | 156,100 | 182 | 0.548 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 150,932 | 1.509 | 20 | 200 | fits | 155,837 | 208 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 786,548 | 7.865 | 20 | 200 | fits | 156,100 | 182 | 0.548 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 151,844 | 1.518 | 20 | 20 | fits | 155,837 | 208 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 937,303 | 9.373 | 20 | 20 | fits | 150,059 | 119 | 0.535 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 155,429 | 1.554 | 20 | 24 | fits | 155,837 | 208 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 999,216 | 9.992 | 20 | 24 | fits | 58,478 | 42 | 0.616 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 154,389 | 1.544 | 20 | 50 | fits | 155,837 | 208 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 790,224 | 7.902 | 20 | 50 | fits | 156,100 | 182 | 0.548 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 313,076 | 3.131 | 20 | 20 | fits | 159,142 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 620,696 | 6.207 | 20 | 20 | fits | 154,771 | 54 | 0.319 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 811,067 | 8.111 | 20 | 20 | fits | 159,825 | 124 | 0.571 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 164,037 | 1.640 | 20 | 200 | fits | 151,790 | 220 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 960,558 | 9.606 | 20 | 200 | fits | 159,825 | 124 | 0.571 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 164,949 | 1.649 | 20 | 20 | fits | 151,790 | 220 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 961,254 | 9.613 | 20 | 20 | fits | 159,825 | 124 | 0.571 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 168,534 | 1.685 | 20 | 24 | fits | 151,790 | 220 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,023,801 | 10.238 | 20 | 24 | fits | 59,112 | 46 | 0.546 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 167,494 | 1.675 | 20 | 50 | fits | 151,790 | 220 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 804,409 | 8.044 | 20 | 50 | fits | 151,380 | 153 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 326,270 | 3.263 | 20 | 20 | fits | 159,231 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 650,949 | 6.509 | 20 | 20 | fits | 156,959 | 53 | 0.399 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 849,312 | 8.493 | 20 | 20 | fits | 151,244 | 112 | 0.609 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 163,603 | 1.636 | 20 | 200 | fits | 154,291 | 205 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 945,921 | 9.459 | 20 | 200 | fits | 151,244 | 112 | 0.609 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 164,515 | 1.645 | 20 | 20 | fits | 154,291 | 205 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 946,617 | 9.466 | 20 | 20 | fits | 151,244 | 112 | 0.609 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 168,100 | 1.681 | 20 | 24 | fits | 154,291 | 205 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,009,897 | 10.099 | 20 | 24 | fits | 59,845 | 47 | 0.559 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 167,060 | 1.671 | 20 | 50 | fits | 154,291 | 205 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 327,881 | 3.279 | 20 | 50 | fits | 151,918 | 219 | 0.489 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 489,416 | 4.894 | 20 | 20 | fits | 161,600 | 41 | 0.639 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 796,273 | 7.963 | 20 | 20 | fits | 154,407 | 53 | 0.318 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 274,793 | 2.748 | 20 | 20 | fits | 156,537 | 194 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 146,750 | 1.468 | 20 | 200 | fits | 151,724 | 220 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 302,678 | 3.027 | 20 | 200 | fits | 156,537 | 194 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 147,662 | 1.477 | 20 | 20 | fits | 151,724 | 220 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 929,318 | 9.293 | 20 | 20 | fits | 148,016 | 115 | 0.560 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 151,247 | 1.512 | 20 | 24 | fits | 151,724 | 220 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,005,076 | 10.051 | 20 | 24 | fits | 72,323 | 59 | 0.515 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 150,207 | 1.502 | 20 | 50 | fits | 151,724 | 220 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 306,354 | 3.064 | 20 | 50 | fits | 156,537 | 194 | 0.565 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 468,614 | 4.686 | 20 | 20 | fits | 162,325 | 41 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 771,073 | 7.711 | 20 | 20 | fits | 148,877 | 56 | 0.391 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 850,729 | 8.507 | 20 | 20 | fits | 151,108 | 119 | 0.571 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 157,894 | 1.579 | 20 | 200 | fits | 154,907 | 204 | 0.530 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 950,650 | 9.507 | 20 | 200 | fits | 151,108 | 119 | 0.571 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 158,806 | 1.588 | 20 | 20 | fits | 154,907 | 204 | 0.530 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 951,346 | 9.513 | 20 | 20 | fits | 151,108 | 119 | 0.571 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 162,391 | 1.624 | 20 | 24 | fits | 154,907 | 204 | 0.530 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,013,252 | 10.133 | 20 | 24 | fits | 58,471 | 42 | 0.615 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 161,351 | 1.614 | 20 | 50 | fits | 154,907 | 204 | 0.530 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 803,218 | 8.032 | 20 | 50 | fits | 155,897 | 179 | 0.532 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 321,580 | 3.216 | 20 | 20 | fits | 160,684 | 80 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 645,241 | 6.452 | 20 | 20 | fits | 154,803 | 53 | 0.329 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 288,815 | 2.888 | 20 | 20 | fits | 165,093 | 211 | 0.541 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 163,969 | 1.640 | 20 | 200 | fits | 152,400 | 221 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 338,085 | 3.381 | 20 | 200 | fits | 165,093 | 211 | 0.541 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 164,881 | 1.649 | 20 | 20 | fits | 152,400 | 221 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 956,741 | 9.567 | 20 | 20 | fits | 153,918 | 115 | 0.581 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 168,466 | 1.685 | 20 | 24 | fits | 152,400 | 221 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,022,645 | 10.226 | 20 | 24 | fits | 62,469 | 53 | 0.565 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 167,426 | 1.674 | 20 | 50 | fits | 152,400 | 221 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 341,761 | 3.418 | 20 | 50 | fits | 165,093 | 211 | 0.541 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 505,695 | 5.057 | 20 | 20 | fits | 163,999 | 41 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 803,723 | 8.037 | 20 | 20 | fits | 144,458 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 767,339 | 7.673 | 20 | 20 | fits | 161,522 | 176 | 0.572 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 163,564 | 1.636 | 20 | 200 | fits | 155,467 | 208 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 794,439 | 7.944 | 20 | 200 | fits | 161,522 | 176 | 0.572 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 164,476 | 1.645 | 20 | 20 | fits | 155,467 | 208 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 955,566 | 9.556 | 20 | 20 | fits | 150,482 | 118 | 0.567 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 168,061 | 1.681 | 20 | 24 | fits | 155,467 | 208 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,018,292 | 10.183 | 20 | 24 | fits | 59,291 | 46 | 0.553 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 167,021 | 1.670 | 20 | 50 | fits | 155,467 | 208 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 798,115 | 7.981 | 20 | 50 | fits | 161,522 | 176 | 0.572 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 327,039 | 3.270 | 20 | 20 | fits | 160,473 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 634,513 | 6.345 | 20 | 20 | fits | 154,585 | 53 | 0.318 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 759,184 | 7.592 | 20 | 20 | fits | 153,270 | 159 | 0.585 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 152,577 | 1.526 | 20 | 200 | fits | 155,450 | 208 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 786,760 | 7.868 | 20 | 200 | fits | 153,270 | 159 | 0.585 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 153,489 | 1.535 | 20 | 20 | fits | 155,450 | 208 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 944,370 | 9.444 | 20 | 20 | fits | 156,914 | 134 | 0.552 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 157,074 | 1.571 | 20 | 24 | fits | 155,450 | 208 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,006,719 | 10.067 | 20 | 24 | fits | 58,914 | 46 | 0.547 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 156,034 | 1.560 | 20 | 50 | fits | 155,450 | 208 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 947,350 | 9.473 | 20 | 50 | fits | 156,914 | 134 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 316,052 | 3.161 | 20 | 20 | fits | 160,473 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 623,693 | 6.237 | 20 | 20 | fits | 154,752 | 54 | 0.319 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 839,609 | 8.396 | 20 | 20 | fits | 162,594 | 124 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 157,549 | 1.575 | 20 | 200 | fits | 152,387 | 219 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 966,346 | 9.663 | 20 | 200 | fits | 162,594 | 124 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 158,461 | 1.585 | 20 | 20 | fits | 152,387 | 219 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 967,042 | 9.670 | 20 | 20 | fits | 162,594 | 124 | 0.579 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 162,046 | 1.620 | 20 | 24 | fits | 152,387 | 219 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,016,425 | 10.164 | 20 | 24 | fits | 45,948 | 33 | 0.602 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 161,006 | 1.610 | 20 | 50 | fits | 152,387 | 219 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 807,428 | 8.074 | 20 | 50 | fits | 165,776 | 163 | 0.579 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 320,747 | 3.207 | 20 | 20 | fits | 160,196 | 79 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 805,348 | 8.053 | 20 | 20 | fits | 165,776 | 163 | 0.579 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 328,922 | 3.289 | 20 | 20 | fits | 154,996 | 161 | 0.596 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 149,980 | 1.500 | 20 | 200 | fits | 155,788 | 165 | 0.557 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 458,547 | 4.585 | 20 | 200 | fits | 154,996 | 161 | 0.596 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 150,892 | 1.509 | 20 | 20 | fits | 155,788 | 165 | 0.557 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 1,008,930 | 10.089 | 20 | 20 | fits | 73,637 | 53 | 0.615 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 154,477 | 1.545 | 20 | 24 | fits | 155,788 | 165 | 0.557 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,012,365 | 10.124 | 20 | 24 | fits | 73,637 | 53 | 0.615 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 153,437 | 1.534 | 20 | 50 | fits | 155,788 | 165 | 0.557 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 462,223 | 4.622 | 20 | 50 | fits | 154,996 | 161 | 0.596 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 638,155 | 6.382 | 20 | 20 | fits | 166,597 | 47 | 0.655 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 936,193 | 9.362 | 20 | 20 | fits | 144,458 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 796,054 | 7.961 | 20 | 20 | fits | 163,175 | 139 | 0.577 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 157,677 | 1.577 | 20 | 200 | fits | 155,450 | 208 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 949,324 | 9.493 | 20 | 200 | fits | 163,175 | 139 | 0.577 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 158,589 | 1.586 | 20 | 20 | fits | 155,450 | 208 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 950,020 | 9.500 | 20 | 20 | fits | 163,175 | 139 | 0.577 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 162,174 | 1.622 | 20 | 24 | fits | 155,450 | 208 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,012,689 | 10.127 | 20 | 24 | fits | 59,234 | 46 | 0.551 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 161,134 | 1.611 | 20 | 50 | fits | 155,450 | 208 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 953,000 | 9.530 | 20 | 50 | fits | 163,175 | 139 | 0.577 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 489,716 | 4.897 | 20 | 20 | fits | 165,776 | 47 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 787,745 | 7.877 | 20 | 20 | fits | 144,458 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 828,458 | 8.285 | 20 | 20 | fits | 162,776 | 122 | 0.586 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 162,782 | 1.628 | 20 | 200 | fits | 152,520 | 220 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 955,016 | 9.550 | 20 | 200 | fits | 162,776 | 122 | 0.586 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 163,694 | 1.637 | 20 | 20 | fits | 152,520 | 220 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 955,712 | 9.557 | 20 | 20 | fits | 162,776 | 122 | 0.586 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 167,279 | 1.673 | 20 | 24 | fits | 152,520 | 220 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,031,374 | 10.314 | 20 | 24 | fits | 62,477 | 52 | 0.577 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 166,239 | 1.662 | 20 | 50 | fits | 152,520 | 220 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 330,128 | 3.301 | 20 | 50 | fits | 155,264 | 195 | 0.546 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 495,987 | 4.960 | 20 | 20 | fits | 165,924 | 47 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 793,836 | 7.938 | 20 | 20 | fits | 144,428 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 286,847 | 2.868 | 20 | 20 | fits | 164,610 | 211 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 162,283 | 1.623 | 20 | 200 | fits | 151,743 | 215 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 336,014 | 3.360 | 20 | 200 | fits | 164,610 | 211 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 163,195 | 1.632 | 20 | 20 | fits | 151,743 | 215 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 953,709 | 9.537 | 20 | 20 | fits | 152,779 | 121 | 0.543 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 166,780 | 1.668 | 20 | 24 | fits | 151,743 | 215 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 1,028,063 | 10.281 | 20 | 24 | fits | 60,830 | 48 | 0.621 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 165,740 | 1.657 | 20 | 50 | fits | 151,743 | 215 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 339,690 | 3.397 | 20 | 50 | fits | 164,610 | 211 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 503,802 | 5.038 | 20 | 20 | fits | 164,177 | 41 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 801,830 | 8.018 | 20 | 20 | fits | 144,458 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 257,717 | 2.577 | 20 | 20 | fits | 163,697 | 211 | 0.535 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 143,829 | 1.438 | 20 | 200 | fits | 151,115 | 214 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 306,917 | 3.069 | 20 | 200 | fits | 163,697 | 211 | 0.535 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 144,741 | 1.447 | 20 | 20 | fits | 151,115 | 214 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 937,261 | 9.373 | 20 | 20 | fits | 154,500 | 126 | 0.546 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 148,326 | 1.483 | 20 | 24 | fits | 151,115 | 214 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 998,925 | 9.989 | 20 | 24 | fits | 58,229 | 42 | 0.616 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 147,286 | 1.473 | 20 | 50 | fits | 151,115 | 214 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 310,593 | 3.106 | 20 | 50 | fits | 163,697 | 211 | 0.535 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 474,510 | 4.745 | 20 | 20 | fits | 163,982 | 41 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 772,659 | 7.727 | 20 | 20 | fits | 144,625 | 50 | 0.336 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 747,792 | 7.478 | 20 | 20 | fits | 160,164 | 170 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 155,370 | 1.554 | 20 | 200 | fits | 154,838 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 796,689 | 7.967 | 20 | 200 | fits | 160,164 | 170 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 156,282 | 1.563 | 20 | 20 | fits | 154,838 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 946,968 | 9.470 | 20 | 20 | fits | 149,583 | 124 | 0.585 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 159,867 | 1.599 | 20 | 24 | fits | 154,838 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 1,086,564 | 10.866 | 20 | 24 | fits | 59,160 | 46 | 0.549 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 158,827 | 1.588 | 20 | 50 | fits | 154,838 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 949,948 | 9.499 | 20 | 50 | fits | 149,583 | 124 | 0.585 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 319,005 | 3.190 | 20 | 20 | fits | 160,633 | 79 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 626,786 | 6.268 | 20 | 20 | fits | 154,782 | 54 | 0.319 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 918,476 | 9.185 | 20 | 20 | fits | 161,501 | 124 | 0.576 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 160,378 | 1.604 | 20 | 200 | fits | 151,793 | 213 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 1,045,243 | 10.452 | 20 | 200 | fits | 161,501 | 124 | 0.576 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 161,290 | 1.613 | 20 | 20 | fits | 151,793 | 213 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 1,045,939 | 10.459 | 20 | 20 | fits | 161,501 | 124 | 0.576 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 164,875 | 1.649 | 20 | 24 | fits | 151,793 | 213 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 1,095,234 | 10.952 | 20 | 24 | fits | 45,860 | 33 | 0.597 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 163,835 | 1.638 | 20 | 50 | fits | 151,793 | 213 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 810,254 | 8.103 | 20 | 50 | fits | 160,722 | 159 | 0.575 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 323,792 | 3.238 | 20 | 20 | fits | 160,412 | 79 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 647,452 | 6.475 | 20 | 20 | fits | 159,163 | 59 | 0.414 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 846,397 | 8.464 | 20 | 20 | fits | 167,989 | 162 | 0.584 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 148,651 | 1.487 | 20 | 200 | fits | 151,119 | 214 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 878,143 | 8.781 | 20 | 200 | fits | 167,989 | 162 | 0.584 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 149,563 | 1.496 | 20 | 20 | fits | 151,119 | 214 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 1,026,343 | 10.263 | 20 | 20 | fits | 147,504 | 116 | 0.551 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 153,148 | 1.531 | 20 | 24 | fits | 151,119 | 214 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 1,088,630 | 10.886 | 20 | 24 | fits | 58,852 | 46 | 0.544 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 152,108 | 1.521 | 20 | 50 | fits | 151,119 | 214 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 881,819 | 8.818 | 20 | 50 | fits | 167,989 | 162 | 0.584 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 312,296 | 3.123 | 20 | 20 | fits | 160,643 | 79 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 879,739 | 8.797 | 20 | 20 | fits | 167,989 | 162 | 0.584 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 846,459 | 8.465 | 20 | 20 | fits | 164,199 | 158 | 0.581 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 160,188 | 1.602 | 20 | 200 | fits | 154,838 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 887,135 | 8.871 | 20 | 200 | fits | 164,199 | 158 | 0.581 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 161,100 | 1.611 | 20 | 20 | fits | 154,838 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 1,036,716 | 10.367 | 20 | 20 | fits | 148,885 | 131 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 164,685 | 1.647 | 20 | 24 | fits | 154,838 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 1,099,041 | 10.990 | 20 | 24 | fits | 58,890 | 46 | 0.545 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 163,645 | 1.636 | 20 | 50 | fits | 154,838 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 1,039,696 | 10.397 | 20 | 50 | fits | 148,885 | 131 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 324,030 | 3.240 | 20 | 20 | fits | 160,840 | 80 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 888,731 | 8.887 | 20 | 20 | fits | 164,199 | 158 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 912,256 | 9.123 | 20 | 20 | fits | 151,286 | 112 | 0.610 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 147,065 | 1.471 | 20 | 200 | fits | 153,475 | 199 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 1,008,628 | 10.086 | 20 | 200 | fits | 151,286 | 112 | 0.610 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 147,977 | 1.480 | 20 | 20 | fits | 153,475 | 199 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 1,009,324 | 10.093 | 20 | 20 | fits | 151,286 | 112 | 0.610 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 151,562 | 1.516 | 20 | 24 | fits | 153,475 | 199 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 1,085,492 | 10.855 | 20 | 24 | fits | 62,929 | 52 | 0.584 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 150,522 | 1.505 | 20 | 50 | fits | 153,475 | 199 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 310,445 | 3.104 | 20 | 50 | fits | 151,396 | 219 | 0.487 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 473,522 | 4.735 | 20 | 20 | fits | 163,142 | 49 | 0.676 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 858,938 | 8.589 | 20 | 20 | fits | 154,669 | 53 | 0.322 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 894,147 | 8.941 | 20 | 20 | fits | 162,808 | 127 | 0.584 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 143,469 | 1.435 | 20 | 200 | fits | 151,609 | 214 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 1,020,365 | 10.204 | 20 | 200 | fits | 162,808 | 127 | 0.584 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 144,381 | 1.444 | 20 | 20 | fits | 151,609 | 214 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 1,021,061 | 10.211 | 20 | 20 | fits | 162,808 | 127 | 0.584 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 147,966 | 1.480 | 20 | 24 | fits | 151,609 | 214 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 1,070,355 | 10.704 | 20 | 24 | fits | 45,859 | 33 | 0.603 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 146,926 | 1.469 | 20 | 50 | fits | 151,609 | 214 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 298,554 | 2.986 | 20 | 50 | fits | 152,018 | 205 | 0.506 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 461,973 | 4.620 | 20 | 20 | fits | 163,484 | 49 | 0.686 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 847,652 | 8.477 | 20 | 20 | fits | 154,806 | 54 | 0.324 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 849,221 | 8.492 | 20 | 20 | fits | 150,984 | 119 | 0.571 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 156,215 | 1.562 | 20 | 200 | fits | 153,682 | 198 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 949,058 | 9.491 | 20 | 200 | fits | 150,984 | 119 | 0.571 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 157,127 | 1.571 | 20 | 20 | fits | 153,682 | 198 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 949,754 | 9.498 | 20 | 20 | fits | 150,984 | 119 | 0.571 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 160,712 | 1.607 | 20 | 24 | fits | 153,682 | 198 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if1` | 1,011,689 | 10.117 | 20 | 24 | fits | 58,500 | 42 | 0.615 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 159,672 | 1.597 | 20 | 50 | fits | 153,682 | 198 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 801,750 | 8.018 | 20 | 50 | fits | 155,929 | 179 | 0.532 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 320,102 | 3.201 | 20 | 20 | fits | 160,885 | 80 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if1` | 643,741 | 6.437 | 20 | 20 | fits | 154,833 | 53 | 0.329 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 286,570 | 2.866 | 20 | 20 | fits | 164,610 | 211 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 162,087 | 1.621 | 20 | 200 | fits | 151,501 | 215 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 335,737 | 3.357 | 20 | 200 | fits | 164,610 | 211 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 162,999 | 1.630 | 20 | 20 | fits | 151,501 | 215 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 953,745 | 9.537 | 20 | 20 | fits | 153,092 | 121 | 0.545 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 166,584 | 1.666 | 20 | 24 | fits | 151,501 | 215 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if1` | 1,027,929 | 10.279 | 20 | 24 | fits | 60,741 | 48 | 0.618 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 165,544 | 1.655 | 20 | 50 | fits | 151,501 | 215 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 339,413 | 3.394 | 20 | 50 | fits | 164,610 | 211 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 503,525 | 5.035 | 20 | 20 | fits | 164,177 | 41 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if1` | 801,553 | 8.016 | 20 | 20 | fits | 144,458 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 753,672 | 7.537 | 20 | 20 | fits | 155,037 | 176 | 0.546 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 164,846 | 1.648 | 20 | 200 | fits | 154,604 | 203 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 789,578 | 7.896 | 20 | 200 | fits | 155,037 | 176 | 0.546 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 165,758 | 1.658 | 20 | 20 | fits | 154,604 | 203 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 944,813 | 9.448 | 20 | 20 | fits | 154,539 | 121 | 0.566 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 169,343 | 1.693 | 20 | 24 | fits | 154,604 | 203 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if1` | 1,016,682 | 10.167 | 20 | 24 | fits | 58,736 | 46 | 0.548 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 168,303 | 1.683 | 20 | 50 | fits | 154,604 | 203 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 793,254 | 7.933 | 20 | 50 | fits | 155,037 | 176 | 0.546 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 328,523 | 3.285 | 20 | 20 | fits | 160,675 | 79 | 0.636 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if1` | 636,137 | 6.361 | 20 | 20 | fits | 154,615 | 53 | 0.318 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 751,067 | 7.511 | 20 | 20 | fits | 161,092 | 161 | 0.586 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 156,231 | 1.562 | 20 | 200 | fits | 154,898 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 786,893 | 7.869 | 20 | 200 | fits | 161,092 | 161 | 0.586 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 157,143 | 1.571 | 20 | 20 | fits | 154,898 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 948,422 | 9.484 | 20 | 20 | fits | 150,676 | 134 | 0.554 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 160,728 | 1.607 | 20 | 24 | fits | 154,898 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if1` | 1,010,813 | 10.108 | 20 | 24 | fits | 58,956 | 46 | 0.548 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 159,688 | 1.597 | 20 | 50 | fits | 154,898 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 951,402 | 9.514 | 20 | 50 | fits | 150,676 | 134 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 319,862 | 3.199 | 20 | 20 | fits | 160,629 | 79 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if1` | 627,397 | 6.274 | 20 | 20 | fits | 154,615 | 53 | 0.318 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 843,541 | 8.435 | 20 | 20 | fits | 162,464 | 124 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 161,241 | 1.612 | 20 | 200 | fits | 151,855 | 213 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 970,213 | 9.702 | 20 | 200 | fits | 162,464 | 124 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 162,153 | 1.622 | 20 | 20 | fits | 151,855 | 213 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 970,909 | 9.709 | 20 | 20 | fits | 162,464 | 124 | 0.579 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 165,738 | 1.657 | 20 | 24 | fits | 151,855 | 213 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if1` | 1,020,292 | 10.203 | 20 | 24 | fits | 45,948 | 33 | 0.602 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 164,698 | 1.647 | 20 | 50 | fits | 151,855 | 213 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 811,425 | 8.114 | 20 | 50 | fits | 165,837 | 163 | 0.579 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 324,576 | 3.246 | 20 | 20 | fits | 160,333 | 79 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if1` | 809,345 | 8.093 | 20 | 20 | fits | 165,837 | 163 | 0.579 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 771,355 | 7.714 | 20 | 20 | fits | 167,966 | 162 | 0.582 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 149,668 | 1.497 | 20 | 200 | fits | 151,335 | 214 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 803,161 | 8.032 | 20 | 200 | fits | 167,966 | 162 | 0.582 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 150,580 | 1.506 | 20 | 20 | fits | 151,335 | 214 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 951,286 | 9.513 | 20 | 20 | fits | 147,429 | 116 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 154,165 | 1.542 | 20 | 24 | fits | 151,335 | 214 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if1` | 1,013,573 | 10.136 | 20 | 24 | fits | 58,852 | 46 | 0.544 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 153,125 | 1.531 | 20 | 50 | fits | 151,335 | 214 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 806,837 | 8.068 | 20 | 50 | fits | 167,966 | 162 | 0.582 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 313,309 | 3.133 | 20 | 20 | fits | 160,639 | 79 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if1` | 804,757 | 8.048 | 20 | 20 | fits | 167,966 | 162 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 769,210 | 7.692 | 20 | 20 | fits | 163,978 | 158 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 161,049 | 1.610 | 20 | 200 | fits | 154,898 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 809,882 | 8.099 | 20 | 200 | fits | 163,978 | 158 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 161,961 | 1.620 | 20 | 20 | fits | 154,898 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 959,394 | 9.594 | 20 | 20 | fits | 148,816 | 131 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 165,546 | 1.655 | 20 | 24 | fits | 154,898 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if1` | 1,021,715 | 10.217 | 20 | 24 | fits | 58,886 | 46 | 0.545 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 164,506 | 1.645 | 20 | 50 | fits | 154,898 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 962,374 | 9.624 | 20 | 50 | fits | 148,816 | 131 | 0.549 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 324,887 | 3.249 | 20 | 20 | fits | 160,836 | 80 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if1` | 811,478 | 8.115 | 20 | 20 | fits | 163,978 | 158 | 0.579 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 833,754 | 8.338 | 20 | 20 | fits | 151,165 | 112 | 0.609 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 146,992 | 1.470 | 20 | 200 | fits | 153,402 | 198 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 930,171 | 9.302 | 20 | 200 | fits | 151,165 | 112 | 0.609 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 147,904 | 1.479 | 20 | 20 | fits | 153,402 | 198 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 930,867 | 9.309 | 20 | 20 | fits | 151,165 | 112 | 0.609 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 151,489 | 1.515 | 20 | 24 | fits | 153,402 | 198 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if1` | 993,857 | 9.939 | 20 | 24 | fits | 59,555 | 46 | 0.558 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 150,449 | 1.504 | 20 | 50 | fits | 153,402 | 198 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 301,187 | 3.012 | 20 | 50 | fits | 151,128 | 220 | 0.484 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 473,268 | 4.733 | 20 | 20 | fits | 162,905 | 49 | 0.672 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if1` | 780,602 | 7.806 | 20 | 20 | fits | 154,458 | 53 | 0.313 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 756,816 | 7.568 | 20 | 20 | fits | 155,170 | 176 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 153,695 | 1.537 | 20 | 200 | fits | 155,071 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 792,386 | 7.924 | 20 | 200 | fits | 155,170 | 176 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 154,607 | 1.546 | 20 | 20 | fits | 155,071 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 943,120 | 9.431 | 20 | 20 | fits | 150,038 | 119 | 0.534 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 158,192 | 1.582 | 20 | 24 | fits | 155,071 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 1,004,867 | 10.049 | 20 | 24 | fits | 58,312 | 42 | 0.616 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 157,152 | 1.572 | 20 | 50 | fits | 155,071 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 796,062 | 7.961 | 20 | 50 | fits | 155,170 | 176 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 315,227 | 3.152 | 20 | 20 | fits | 158,530 | 79 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if1` | 638,812 | 6.388 | 20 | 20 | fits | 159,235 | 59 | 0.414 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 851,957 | 8.520 | 20 | 20 | fits | 150,921 | 118 | 0.572 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 160,168 | 1.602 | 20 | 200 | fits | 153,499 | 198 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 951,571 | 9.516 | 20 | 200 | fits | 150,921 | 118 | 0.572 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 161,080 | 1.611 | 20 | 20 | fits | 153,499 | 198 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 952,267 | 9.523 | 20 | 20 | fits | 150,921 | 118 | 0.572 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 164,665 | 1.647 | 20 | 24 | fits | 153,499 | 198 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 1,014,234 | 10.142 | 20 | 24 | fits | 58,532 | 42 | 0.617 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 163,625 | 1.636 | 20 | 50 | fits | 153,499 | 198 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 804,326 | 8.043 | 20 | 50 | fits | 155,950 | 179 | 0.532 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 321,779 | 3.218 | 20 | 20 | fits | 158,609 | 79 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if1` | 646,296 | 6.463 | 20 | 20 | fits | 156,864 | 53 | 0.396 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 823,749 | 8.237 | 20 | 20 | fits | 153,323 | 109 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 147,392 | 1.474 | 20 | 200 | fits | 151,776 | 213 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 943,069 | 9.431 | 20 | 200 | fits | 153,323 | 109 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 148,304 | 1.483 | 20 | 20 | fits | 151,776 | 213 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 943,765 | 9.438 | 20 | 20 | fits | 153,323 | 109 | 0.617 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 151,889 | 1.519 | 20 | 24 | fits | 151,776 | 213 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 1,087,775 | 10.878 | 20 | 24 | fits | 59,889 | 46 | 0.554 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 150,849 | 1.508 | 20 | 50 | fits | 151,776 | 213 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 793,422 | 7.934 | 20 | 50 | fits | 158,732 | 165 | 0.543 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 309,023 | 3.090 | 20 | 20 | fits | 158,629 | 80 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if1` | 632,610 | 6.326 | 20 | 20 | fits | 154,822 | 53 | 0.329 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 284,208 | 2.842 | 20 | 20 | fits | 165,612 | 211 | 0.542 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 158,736 | 1.587 | 20 | 200 | fits | 155,294 | 203 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 333,007 | 3.330 | 20 | 200 | fits | 165,612 | 211 | 0.542 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 159,648 | 1.596 | 20 | 20 | fits | 155,294 | 203 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 1,037,028 | 10.370 | 20 | 20 | fits | 150,287 | 130 | 0.559 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 163,233 | 1.632 | 20 | 24 | fits | 155,294 | 203 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 1,098,882 | 10.989 | 20 | 24 | fits | 48,531 | 39 | 0.622 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 162,193 | 1.622 | 20 | 50 | fits | 155,294 | 203 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 1,040,008 | 10.400 | 20 | 50 | fits | 150,287 | 130 | 0.559 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 498,976 | 4.990 | 20 | 20 | fits | 162,358 | 41 | 0.646 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if1` | 806,850 | 8.069 | 20 | 20 | fits | 154,422 | 55 | 0.418 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 832,399 | 8.324 | 20 | 20 | fits | 163,825 | 159 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 160,848 | 1.608 | 20 | 200 | fits | 154,879 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 873,023 | 8.730 | 20 | 200 | fits | 163,825 | 159 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 161,760 | 1.618 | 20 | 20 | fits | 154,879 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 1,035,317 | 10.353 | 20 | 20 | fits | 151,065 | 134 | 0.556 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 165,345 | 1.653 | 20 | 24 | fits | 154,879 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 1,097,779 | 10.978 | 20 | 24 | fits | 59,027 | 46 | 0.551 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 164,305 | 1.643 | 20 | 50 | fits | 154,879 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 1,038,297 | 10.383 | 20 | 50 | fits | 151,065 | 134 | 0.556 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 322,396 | 3.224 | 20 | 20 | fits | 158,546 | 79 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if1` | 874,619 | 8.746 | 20 | 20 | fits | 163,825 | 159 | 0.579 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 916,374 | 9.164 | 20 | 20 | fits | 162,322 | 122 | 0.586 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 146,969 | 1.470 | 20 | 200 | fits | 153,379 | 198 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 1,025,855 | 10.259 | 20 | 200 | fits | 162,322 | 122 | 0.586 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 147,881 | 1.479 | 20 | 20 | fits | 153,379 | 198 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 1,026,551 | 10.266 | 20 | 20 | fits | 162,322 | 122 | 0.586 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 151,466 | 1.515 | 20 | 24 | fits | 153,379 | 198 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 1,075,805 | 10.758 | 20 | 24 | fits | 45,819 | 33 | 0.604 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 150,426 | 1.504 | 20 | 50 | fits | 153,379 | 198 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 300,783 | 3.008 | 20 | 50 | fits | 150,747 | 219 | 0.483 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 461,878 | 4.619 | 20 | 20 | fits | 161,160 | 41 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if1` | 853,935 | 8.539 | 20 | 20 | fits | 158,813 | 60 | 0.383 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 854,547 | 8.545 | 20 | 20 | fits | 167,852 | 162 | 0.587 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 153,853 | 1.539 | 20 | 200 | fits | 151,160 | 214 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 886,229 | 8.862 | 20 | 200 | fits | 167,852 | 162 | 0.587 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 154,765 | 1.548 | 20 | 20 | fits | 151,160 | 214 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 1,046,969 | 10.470 | 20 | 20 | fits | 160,044 | 126 | 0.538 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 158,350 | 1.583 | 20 | 24 | fits | 151,160 | 214 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 1,095,873 | 10.959 | 20 | 24 | fits | 45,469 | 33 | 0.596 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 157,310 | 1.573 | 20 | 50 | fits | 151,160 | 214 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 889,905 | 8.899 | 20 | 50 | fits | 167,852 | 162 | 0.587 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 315,433 | 3.154 | 20 | 20 | fits | 158,578 | 79 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if1` | 887,825 | 8.878 | 20 | 20 | fits | 167,852 | 162 | 0.587 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 357,724 | 3.577 | 20 | 20 | fits | 156,036 | 148 | 0.595 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 154,926 | 1.549 | 20 | 200 | fits | 163,286 | 184 | 0.537 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 463,893 | 4.639 | 20 | 200 | fits | 156,036 | 148 | 0.595 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 155,838 | 1.558 | 20 | 20 | fits | 163,286 | 184 | 0.537 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 464,589 | 4.646 | 20 | 20 | fits | 156,036 | 148 | 0.595 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 159,423 | 1.594 | 20 | 24 | fits | 163,286 | 184 | 0.537 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 1,084,979 | 10.850 | 20 | 24 | fits | 62,184 | 46 | 0.579 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 158,383 | 1.584 | 20 | 50 | fits | 163,286 | 184 | 0.537 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 311,533 | 3.115 | 20 | 50 | fits | 153,540 | 204 | 0.512 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 722,278 | 7.223 | 20 | 20 | fits | 165,511 | 47 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if1` | 1,020,260 | 10.203 | 20 | 20 | fits | 144,477 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 751,283 | 7.513 | 20 | 20 | fits | 158,642 | 166 | 0.561 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 160,477 | 1.605 | 20 | 200 | fits | 151,218 | 214 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 786,681 | 7.867 | 20 | 200 | fits | 158,642 | 166 | 0.561 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 161,389 | 1.614 | 20 | 20 | fits | 151,218 | 214 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 950,799 | 9.508 | 20 | 20 | fits | 153,413 | 126 | 0.542 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 164,974 | 1.650 | 20 | 24 | fits | 151,218 | 214 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if1` | 1,012,452 | 10.125 | 20 | 24 | fits | 58,218 | 42 | 0.614 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 163,934 | 1.639 | 20 | 50 | fits | 151,218 | 214 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 790,357 | 7.904 | 20 | 50 | fits | 158,642 | 166 | 0.561 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 322,102 | 3.221 | 20 | 20 | fits | 158,623 | 79 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if1` | 629,635 | 6.296 | 20 | 20 | fits | 154,604 | 53 | 0.318 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 752,979 | 7.530 | 20 | 20 | fits | 156,226 | 182 | 0.548 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 153,359 | 1.534 | 20 | 200 | fits | 155,153 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 788,558 | 7.886 | 20 | 200 | fits | 156,226 | 182 | 0.548 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 154,271 | 1.543 | 20 | 20 | fits | 155,153 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 939,313 | 9.393 | 20 | 20 | fits | 150,059 | 119 | 0.535 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 157,856 | 1.579 | 20 | 24 | fits | 155,153 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if1` | 1,001,064 | 10.011 | 20 | 24 | fits | 58,316 | 42 | 0.615 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 156,816 | 1.568 | 20 | 50 | fits | 155,153 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 792,234 | 7.922 | 20 | 50 | fits | 156,226 | 182 | 0.548 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 314,895 | 3.149 | 20 | 20 | fits | 158,534 | 79 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if1` | 622,593 | 6.226 | 20 | 20 | fits | 154,771 | 54 | 0.319 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 842,909 | 8.429 | 20 | 20 | fits | 152,108 | 111 | 0.610 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 159,832 | 1.598 | 20 | 200 | fits | 153,581 | 198 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 951,466 | 9.515 | 20 | 200 | fits | 152,108 | 111 | 0.610 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 160,744 | 1.607 | 20 | 20 | fits | 153,581 | 198 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 952,162 | 9.522 | 20 | 20 | fits | 152,108 | 111 | 0.610 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 164,329 | 1.643 | 20 | 24 | fits | 153,581 | 198 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if1` | 1,014,604 | 10.146 | 20 | 24 | fits | 59,007 | 46 | 0.545 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 163,289 | 1.633 | 20 | 50 | fits | 153,581 | 198 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 803,034 | 8.030 | 20 | 50 | fits | 155,764 | 179 | 0.531 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 321,447 | 3.214 | 20 | 20 | fits | 158,613 | 79 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if1` | 645,190 | 6.452 | 20 | 20 | fits | 159,314 | 59 | 0.416 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 815,852 | 8.159 | 20 | 20 | fits | 163,146 | 121 | 0.588 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 145,442 | 1.454 | 20 | 200 | fits | 151,852 | 213 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 942,452 | 9.425 | 20 | 200 | fits | 163,146 | 121 | 0.588 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 146,354 | 1.464 | 20 | 20 | fits | 151,852 | 213 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 943,148 | 9.431 | 20 | 20 | fits | 163,146 | 121 | 0.588 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 149,939 | 1.499 | 20 | 24 | fits | 151,852 | 213 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if1` | 992,307 | 9.923 | 20 | 24 | fits | 45,724 | 33 | 0.599 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 148,899 | 1.489 | 20 | 50 | fits | 151,852 | 213 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 300,719 | 3.007 | 20 | 50 | fits | 152,210 | 206 | 0.507 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 473,967 | 4.740 | 20 | 20 | fits | 164,126 | 47 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if1` | 780,902 | 7.809 | 20 | 20 | fits | 153,372 | 55 | 0.397 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 283,804 | 2.838 | 20 | 20 | fits | 152,790 | 201 | 0.536 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 158,413 | 1.584 | 20 | 200 | fits | 155,389 | 203 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 319,781 | 3.198 | 20 | 200 | fits | 152,790 | 201 | 0.536 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 159,325 | 1.593 | 20 | 20 | fits | 155,389 | 203 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 944,069 | 9.441 | 20 | 20 | fits | 151,402 | 129 | 0.563 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 162,910 | 1.629 | 20 | 24 | fits | 155,389 | 203 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if1` | 1,019,287 | 10.193 | 20 | 24 | fits | 61,944 | 52 | 0.570 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 161,870 | 1.619 | 20 | 50 | fits | 155,389 | 203 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 947,049 | 9.470 | 20 | 50 | fits | 151,402 | 129 | 0.563 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 486,077 | 4.861 | 20 | 20 | fits | 162,685 | 41 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if1` | 793,567 | 7.936 | 20 | 20 | fits | 154,655 | 53 | 0.322 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 348,558 | 3.486 | 20 | 20 | fits | 157,236 | 161 | 0.567 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 143,045 | 1.430 | 20 | 200 | fits | 151,082 | 175 | 0.535 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 460,875 | 4.609 | 20 | 200 | fits | 157,236 | 161 | 0.567 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 143,957 | 1.440 | 20 | 20 | fits | 151,082 | 175 | 0.535 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 461,571 | 4.616 | 20 | 20 | fits | 157,236 | 161 | 0.567 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 147,542 | 1.475 | 20 | 24 | fits | 151,082 | 175 | 0.535 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if1` | 1,010,555 | 10.106 | 20 | 24 | fits | 63,662 | 52 | 0.578 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 146,502 | 1.465 | 20 | 50 | fits | 151,082 | 175 | 0.535 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 307,315 | 3.073 | 20 | 50 | fits | 151,558 | 200 | 0.518 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 624,899 | 6.249 | 20 | 20 | fits | 160,413 | 43 | 0.684 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if1` | 932,876 | 9.329 | 20 | 20 | fits | 154,809 | 54 | 0.321 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 832,665 | 8.327 | 20 | 20 | fits | 151,264 | 117 | 0.601 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 146,887 | 1.469 | 20 | 200 | fits | 153,297 | 198 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 928,663 | 9.287 | 20 | 200 | fits | 151,264 | 117 | 0.601 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 147,799 | 1.478 | 20 | 20 | fits | 153,297 | 198 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 929,359 | 9.294 | 20 | 20 | fits | 151,264 | 117 | 0.601 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 151,384 | 1.514 | 20 | 24 | fits | 153,297 | 198 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if1` | 992,361 | 9.924 | 20 | 24 | fits | 59,567 | 46 | 0.558 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 150,344 | 1.503 | 20 | 50 | fits | 153,297 | 198 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 300,758 | 3.008 | 20 | 50 | fits | 150,804 | 219 | 0.484 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 460,102 | 4.601 | 20 | 20 | fits | 159,409 | 43 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if1` | 767,571 | 7.676 | 20 | 20 | fits | 154,652 | 54 | 0.317 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 281,204 | 2.812 | 20 | 20 | fits | 156,180 | 194 | 0.563 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 153,518 | 1.535 | 20 | 200 | fits | 151,234 | 214 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 309,089 | 3.091 | 20 | 200 | fits | 156,180 | 194 | 0.563 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 154,430 | 1.544 | 20 | 20 | fits | 151,234 | 214 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 937,742 | 9.377 | 20 | 20 | fits | 149,245 | 113 | 0.570 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 158,015 | 1.580 | 20 | 24 | fits | 151,234 | 214 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if1` | 1,013,444 | 10.134 | 20 | 24 | fits | 72,267 | 59 | 0.514 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 156,975 | 1.570 | 20 | 50 | fits | 151,234 | 214 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 312,765 | 3.128 | 20 | 50 | fits | 156,180 | 194 | 0.563 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 474,867 | 4.749 | 20 | 20 | fits | 162,167 | 41 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if1` | 789,397 | 7.894 | 20 | 20 | fits | 149,534 | 55 | 0.451 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 258,815 | 2.588 | 20 | 20 | fits | 164,379 | 212 | 0.538 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 144,478 | 1.445 | 20 | 200 | fits | 151,340 | 214 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 308,248 | 3.082 | 20 | 200 | fits | 164,379 | 212 | 0.538 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 145,390 | 1.454 | 20 | 20 | fits | 151,340 | 214 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 937,935 | 9.379 | 20 | 20 | fits | 153,379 | 120 | 0.548 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 148,975 | 1.490 | 20 | 24 | fits | 151,340 | 214 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 999,923 | 9.999 | 20 | 24 | fits | 58,553 | 42 | 0.621 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 147,935 | 1.479 | 20 | 50 | fits | 151,340 | 214 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 311,924 | 3.119 | 20 | 50 | fits | 164,379 | 212 | 0.538 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 487,441 | 4.874 | 20 | 20 | fits | 166,378 | 47 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 785,456 | 7.855 | 20 | 20 | fits | 144,458 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 790,399 | 7.904 | 20 | 20 | fits | 162,729 | 140 | 0.574 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 156,338 | 1.563 | 20 | 200 | fits | 155,129 | 203 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 943,223 | 9.432 | 20 | 200 | fits | 162,729 | 140 | 0.574 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 157,250 | 1.573 | 20 | 20 | fits | 155,129 | 203 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 943,919 | 9.439 | 20 | 20 | fits | 162,729 | 140 | 0.574 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 160,835 | 1.608 | 20 | 24 | fits | 155,129 | 203 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 1,018,237 | 10.182 | 20 | 24 | fits | 61,215 | 48 | 0.622 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 159,795 | 1.598 | 20 | 50 | fits | 155,129 | 203 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 946,899 | 9.469 | 20 | 50 | fits | 162,729 | 140 | 0.574 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 484,174 | 4.842 | 20 | 20 | fits | 163,118 | 41 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 782,090 | 7.821 | 20 | 20 | fits | 144,458 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 815,362 | 8.154 | 20 | 20 | fits | 163,277 | 117 | 0.621 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 144,846 | 1.448 | 20 | 200 | fits | 154,690 | 199 | 0.529 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 934,104 | 9.341 | 20 | 200 | fits | 163,277 | 117 | 0.621 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 145,758 | 1.458 | 20 | 20 | fits | 154,690 | 199 | 0.529 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 934,800 | 9.348 | 20 | 20 | fits | 163,277 | 117 | 0.621 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 149,343 | 1.493 | 20 | 24 | fits | 154,690 | 199 | 0.529 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 1,088,543 | 10.885 | 20 | 24 | fits | 63,010 | 52 | 0.585 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 148,303 | 1.483 | 20 | 50 | fits | 154,690 | 199 | 0.529 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 308,765 | 3.088 | 20 | 50 | fits | 151,597 | 219 | 0.488 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 474,587 | 4.746 | 20 | 20 | fits | 165,887 | 47 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 772,423 | 7.724 | 20 | 20 | fits | 144,428 | 49 | 0.335 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 894,137 | 8.941 | 20 | 20 | fits | 163,050 | 127 | 0.584 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 144,159 | 1.442 | 20 | 200 | fits | 151,849 | 213 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 1,020,401 | 10.204 | 20 | 200 | fits | 163,050 | 127 | 0.584 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 145,071 | 1.451 | 20 | 20 | fits | 151,849 | 213 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 1,021,097 | 10.211 | 20 | 20 | fits | 163,050 | 127 | 0.584 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 148,656 | 1.487 | 20 | 24 | fits | 151,849 | 213 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 1,070,340 | 10.703 | 20 | 24 | fits | 45,808 | 33 | 0.602 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 147,616 | 1.476 | 20 | 50 | fits | 151,849 | 213 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 299,707 | 2.997 | 20 | 50 | fits | 152,481 | 205 | 0.509 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 462,642 | 4.626 | 20 | 20 | fits | 163,000 | 41 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 770,577 | 7.706 | 20 | 20 | fits | 154,498 | 56 | 0.419 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 848,651 | 8.487 | 20 | 20 | fits | 167,488 | 179 | 0.581 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 155,235 | 1.552 | 20 | 200 | fits | 154,872 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 880,591 | 8.806 | 20 | 200 | fits | 167,488 | 179 | 0.581 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 156,147 | 1.561 | 20 | 20 | fits | 154,872 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 1,041,571 | 10.416 | 20 | 20 | fits | 160,284 | 125 | 0.545 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 159,732 | 1.597 | 20 | 24 | fits | 154,872 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 1,090,342 | 10.903 | 20 | 24 | fits | 45,336 | 33 | 0.593 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 158,692 | 1.587 | 20 | 50 | fits | 154,872 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 884,267 | 8.843 | 20 | 50 | fits | 167,488 | 179 | 0.581 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 318,714 | 3.187 | 20 | 20 | fits | 160,477 | 79 | 0.637 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 882,187 | 8.822 | 20 | 20 | fits | 167,488 | 179 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 952,433 | 9.524 | 20 | 20 | fits | 161,751 | 138 | 0.574 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 161,649 | 1.616 | 20 | 200 | fits | 153,468 | 198 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 1,052,733 | 10.527 | 20 | 200 | fits | 161,751 | 138 | 0.574 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 162,561 | 1.626 | 20 | 20 | fits | 153,468 | 198 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 1,053,429 | 10.534 | 20 | 20 | fits | 161,751 | 138 | 0.574 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 166,146 | 1.661 | 20 | 24 | fits | 153,468 | 198 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 1,102,738 | 11.027 | 20 | 24 | fits | 45,874 | 33 | 0.607 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 165,106 | 1.651 | 20 | 50 | fits | 153,468 | 198 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 1,056,409 | 10.564 | 20 | 50 | fits | 161,751 | 138 | 0.574 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 325,207 | 3.252 | 20 | 20 | fits | 160,556 | 79 | 0.638 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 892,578 | 8.926 | 20 | 20 | fits | 165,277 | 161 | 0.565 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 911,744 | 9.117 | 20 | 20 | fits | 162,509 | 124 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 148,977 | 1.490 | 20 | 200 | fits | 151,849 | 213 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 1,038,441 | 10.384 | 20 | 200 | fits | 162,509 | 124 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 149,889 | 1.499 | 20 | 20 | fits | 151,849 | 213 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 1,039,137 | 10.391 | 20 | 20 | fits | 162,509 | 124 | 0.579 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 153,474 | 1.535 | 20 | 24 | fits | 151,849 | 213 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 1,088,524 | 10.885 | 20 | 24 | fits | 45,952 | 33 | 0.602 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 152,434 | 1.524 | 20 | 50 | fits | 151,849 | 213 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 879,608 | 8.796 | 20 | 50 | fits | 163,471 | 157 | 0.568 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 312,540 | 3.125 | 20 | 20 | fits | 160,561 | 80 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 877,528 | 8.775 | 20 | 20 | fits | 163,471 | 157 | 0.568 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 289,717 | 2.897 | 20 | 20 | fits | 158,058 | 195 | 0.565 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 160,053 | 1.601 | 20 | 200 | fits | 154,872 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 317,502 | 3.175 | 20 | 200 | fits | 158,058 | 195 | 0.565 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 160,965 | 1.610 | 20 | 20 | fits | 154,872 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 1,032,858 | 10.329 | 20 | 20 | fits | 160,259 | 134 | 0.571 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 164,550 | 1.645 | 20 | 24 | fits | 154,872 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 1,095,154 | 10.952 | 20 | 24 | fits | 58,861 | 46 | 0.545 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 163,510 | 1.635 | 20 | 50 | fits | 154,872 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 1,035,838 | 10.358 | 20 | 50 | fits | 160,259 | 134 | 0.571 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 574,879 | 5.749 | 20 | 20 | fits | 167,008 | 47 | 0.655 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 873,499 | 8.735 | 20 | 20 | fits | 144,749 | 49 | 0.344 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 834,686 | 8.347 | 20 | 20 | fits | 151,745 | 117 | 0.577 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 155,944 | 1.559 | 20 | 200 | fits | 151,796 | 213 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 951,771 | 9.518 | 20 | 200 | fits | 151,745 | 117 | 0.577 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 156,856 | 1.569 | 20 | 20 | fits | 151,796 | 213 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 952,467 | 9.525 | 20 | 20 | fits | 151,745 | 117 | 0.577 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 160,441 | 1.604 | 20 | 24 | fits | 151,796 | 213 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if1` | 1,014,615 | 10.146 | 20 | 24 | fits | 58,713 | 42 | 0.615 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 159,401 | 1.594 | 20 | 50 | fits | 151,796 | 213 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 803,702 | 8.037 | 20 | 50 | fits | 158,712 | 165 | 0.543 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 319,277 | 3.193 | 20 | 20 | fits | 160,331 | 79 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if1` | 642,910 | 6.429 | 20 | 20 | fits | 159,136 | 59 | 0.414 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 258,486 | 2.585 | 20 | 20 | fits | 164,250 | 211 | 0.538 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 144,149 | 1.441 | 20 | 200 | fits | 151,054 | 214 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 307,790 | 3.078 | 20 | 200 | fits | 164,250 | 211 | 0.538 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 145,061 | 1.451 | 20 | 20 | fits | 151,054 | 214 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 941,477 | 9.415 | 20 | 20 | fits | 153,623 | 120 | 0.549 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 148,646 | 1.486 | 20 | 24 | fits | 151,054 | 214 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if1` | 1,003,413 | 10.034 | 20 | 24 | fits | 58,501 | 42 | 0.620 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 147,606 | 1.476 | 20 | 50 | fits | 151,054 | 214 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 311,466 | 3.115 | 20 | 50 | fits | 164,250 | 211 | 0.538 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 468,030 | 4.680 | 20 | 20 | fits | 156,629 | 44 | 0.685 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if1` | 788,754 | 7.888 | 20 | 20 | fits | 154,554 | 53 | 0.320 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 752,750 | 7.527 | 20 | 20 | fits | 159,727 | 164 | 0.571 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 156,160 | 1.562 | 20 | 200 | fits | 155,020 | 202 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 801,661 | 8.017 | 20 | 200 | fits | 159,727 | 164 | 0.571 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 157,072 | 1.571 | 20 | 20 | fits | 155,020 | 202 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 951,970 | 9.520 | 20 | 20 | fits | 149,613 | 124 | 0.590 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 160,657 | 1.607 | 20 | 24 | fits | 155,020 | 202 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if1` | 1,014,413 | 10.144 | 20 | 24 | fits | 59,008 | 46 | 0.548 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 159,617 | 1.596 | 20 | 50 | fits | 155,020 | 202 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 954,950 | 9.550 | 20 | 50 | fits | 149,613 | 124 | 0.590 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 319,981 | 3.200 | 20 | 20 | fits | 160,819 | 80 | 0.638 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if1` | 643,530 | 6.435 | 20 | 20 | fits | 154,803 | 53 | 0.329 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 832,658 | 8.327 | 20 | 20 | fits | 162,750 | 121 | 0.586 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 161,034 | 1.610 | 20 | 200 | fits | 152,068 | 214 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 959,240 | 9.592 | 20 | 200 | fits | 162,750 | 121 | 0.586 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 161,946 | 1.619 | 20 | 20 | fits | 152,068 | 214 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 959,936 | 9.599 | 20 | 20 | fits | 162,750 | 121 | 0.586 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 165,531 | 1.655 | 20 | 24 | fits | 152,068 | 214 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if1` | 1,013,046 | 10.130 | 20 | 24 | fits | 49,675 | 40 | 0.627 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 164,491 | 1.645 | 20 | 50 | fits | 152,068 | 214 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 327,486 | 3.275 | 20 | 50 | fits | 154,045 | 205 | 0.521 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 490,318 | 4.903 | 20 | 20 | fits | 162,897 | 41 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if1` | 798,086 | 7.981 | 20 | 20 | fits | 154,331 | 55 | 0.418 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 263,123 | 2.631 | 20 | 20 | fits | 163,342 | 212 | 0.531 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 148,221 | 1.482 | 20 | 200 | fits | 156,070 | 183 | 0.526 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 310,954 | 3.110 | 20 | 200 | fits | 163,342 | 212 | 0.531 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 149,133 | 1.491 | 20 | 20 | fits | 156,070 | 183 | 0.526 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 953,042 | 9.530 | 20 | 20 | fits | 159,008 | 114 | 0.589 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 152,718 | 1.527 | 20 | 24 | fits | 156,070 | 183 | 0.526 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if1` | 1,002,842 | 10.028 | 20 | 24 | fits | 46,365 | 33 | 0.608 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 151,678 | 1.517 | 20 | 50 | fits | 156,070 | 183 | 0.526 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 314,630 | 3.146 | 20 | 50 | fits | 163,342 | 212 | 0.531 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 475,463 | 4.755 | 20 | 20 | fits | 160,898 | 79 | 0.635 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if1` | 953,942 | 9.539 | 20 | 20 | fits | 159,008 | 114 | 0.589 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 770,961 | 7.710 | 20 | 20 | fits | 166,482 | 179 | 0.577 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 154,964 | 1.550 | 20 | 200 | fits | 154,790 | 202 | 0.522 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 802,839 | 8.028 | 20 | 200 | fits | 166,482 | 179 | 0.577 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 155,876 | 1.559 | 20 | 20 | fits | 154,790 | 202 | 0.522 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 963,815 | 9.638 | 20 | 20 | fits | 160,280 | 125 | 0.545 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 159,461 | 1.595 | 20 | 24 | fits | 154,790 | 202 | 0.522 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if1` | 1,012,582 | 10.126 | 20 | 24 | fits | 45,332 | 33 | 0.593 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 158,421 | 1.584 | 20 | 50 | fits | 154,790 | 202 | 0.522 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 806,515 | 8.065 | 20 | 50 | fits | 166,482 | 179 | 0.577 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 318,507 | 3.185 | 20 | 20 | fits | 160,541 | 79 | 0.638 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if1` | 804,435 | 8.044 | 20 | 20 | fits | 166,482 | 179 | 0.577 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 871,653 | 8.717 | 20 | 20 | fits | 161,698 | 138 | 0.573 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 161,378 | 1.614 | 20 | 200 | fits | 153,386 | 198 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 972,009 | 9.720 | 20 | 200 | fits | 161,698 | 138 | 0.573 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 162,290 | 1.623 | 20 | 20 | fits | 153,386 | 198 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 972,705 | 9.727 | 20 | 20 | fits | 161,698 | 138 | 0.573 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 165,875 | 1.659 | 20 | 24 | fits | 153,386 | 198 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if1` | 1,022,014 | 10.220 | 20 | 24 | fits | 45,874 | 33 | 0.607 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 164,835 | 1.648 | 20 | 50 | fits | 153,386 | 198 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 975,685 | 9.757 | 20 | 50 | fits | 161,698 | 138 | 0.573 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 325,000 | 3.250 | 20 | 20 | fits | 160,620 | 79 | 0.639 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if1` | 811,907 | 8.119 | 20 | 20 | fits | 167,461 | 167 | 0.573 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 817,942 | 8.179 | 20 | 20 | fits | 163,025 | 121 | 0.588 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 148,708 | 1.487 | 20 | 200 | fits | 151,769 | 213 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 944,707 | 9.447 | 20 | 200 | fits | 163,025 | 121 | 0.588 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 149,620 | 1.496 | 20 | 20 | fits | 151,769 | 213 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 945,403 | 9.454 | 20 | 20 | fits | 163,025 | 121 | 0.588 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 153,205 | 1.532 | 20 | 24 | fits | 151,769 | 213 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if1` | 1,008,084 | 10.081 | 20 | 24 | fits | 59,246 | 46 | 0.552 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 152,165 | 1.522 | 20 | 50 | fits | 151,769 | 213 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 305,931 | 3.059 | 20 | 50 | fits | 154,156 | 195 | 0.537 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 469,157 | 4.692 | 20 | 20 | fits | 163,291 | 42 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if1` | 783,278 | 7.833 | 20 | 20 | fits | 144,675 | 49 | 0.346 |
| LINK_UP | `adp.link_up.if0` | 2,381 | 0.024 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 15,617 | 0.156 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,490 | 0.105 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 6,069 | 0.061 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 18,507 | 0.185 | 20 | 200 | fits | 4,622 | 19 (11) | 0.533 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 16,491 | 0.165 | 20 | 200 | fits | 4,622 | 19 (11) | 0.533 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,164 | 0.132 | 20 | 50 | fits | 31,298 | 44 | 0.718 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 14,355 | 0.144 | 20 | 50 | fits | 27,669 | 36 | 0.681 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 26,330 | 0.263 | 20 | 50 | fits | 27,416 | 36 | 0.675 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 25,121 | 0.251 | 20 | 50 | fits | 32,045 | 62 | 0.576 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 26,866 | 0.269 | 20 | 50 | fits | 32,045 | 62 | 0.576 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,834 | 0.118 | 20 | 50 | fits | 26,525 | 31 | 0.608 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 12,462 | 0.125 | 20 | 50 | fits | 30,617 | 44 | 0.701 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 17,013 | 0.170 | 20 | 50 | fits | 28,607 | 37 | 0.688 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 20,352 | 0.204 | 20 | 50 | fits | 27,160 | 36 | 0.638 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 12,839 | 0.128 | 20 | 50 | fits | 33,705 | 62 | 0.603 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 14,807 | 0.148 | 20 | 50 | fits | 33,705 | 62 | 0.603 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 12,512 | 0.125 | 20 | 50 | fits | 27,594 | 31 | 0.615 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 29,290 | 0.293 | 20 | 20 | fits | 44,971 | 42 (35) | 0.729 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 40,398 | 0.404 | 20 | 20 | fits | 44,971 | 42 (35) | 0.729 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 27,907 | 0.279 | 20 | 20 | fits | 40,091 | 34 (14) | 0.787 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 36,419 | 0.364 | 20 | 20 | fits | 40,091 | 34 (14) | 0.787 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 33,320 | 0.333 | 20 | 20 | fits | 38,996 | 35 (14) | 0.784 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 41,627 | 0.416 | 20 | 20 | fits | 38,996 | 35 (14) | 0.784 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 31,037 | 0.310 | 20 | 20 | fits | 33,733 | 22 (35) | 0.821 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 24,558 | 0.246 | 20 | 20 | fits | 40,973 | 28 (35) | 0.799 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 144,774 | 1.448 | 20 | 20 | fits | 120,238 | 6 | 0.820 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 136,447 | 1.364 | 20 | 20 | fits | 111,706 | 6 | 0.778 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 54,695 | 0.547 | 20 | 20 | fits | 54,760 | 13 | 0.902 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,728 | 0.247 | 20 | 20 | fits | 24,793 | 13 | 0.722 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 187,438 | 1.874 | 220 | 220 | fits | 186,522 | 10 | 0.816 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 52,206 | 0.522 | 20 | 20 | fits | 52,271 | 13 | 0.896 |
| malformed MRPDU discard | `srp.malformed.if1` | 25,365 | 0.254 | 20 | 20 | fits | 25,430 | 13 | 0.719 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 177,518 | 1.775 | 220 | 220 | fits | 173,631 | 9 | 0.808 |
| an event behind 15 others | `backlog.event.if0` | 184,568 | 1.846 | 20 | 200 | fits | 98,235 | 130 | 0.568 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 766,316 | 7.663 | 20 | 20 | fits | 152,073 | 117 | 0.545 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 173,045 | 1.730 | 20 | 200 | fits | 173,253 | 211 | 0.528 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 411,620 | 4.116 | 20 | 200 | fits | 140,949 | 77 | 0.621 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 168,786 | 1.688 | 20 | 20 | fits | 173,253 | 211 | 0.528 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 840,796 | 8.408 | 20 | 20 | fits | 152,073 | 117 | 0.545 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 172,371 | 1.724 | 20 | 24 | fits | 173,253 | 211 | 0.528 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 876,005 | 8.760 | 20 | 24 | fits | 31,774 | 20 | 0.697 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 171,331 | 1.713 | 20 | 50 | fits | 173,253 | 211 | 0.528 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 410,125 | 4.101 | 20 | 50 | fits | 140,949 | 77 | 0.621 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 523,973 | 5.240 | 20 | 20 | fits | 109,665 | 53 | 0.538 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 689,623 | 6.896 | 20 | 20 | fits | 78,131 | 43 | 0.500 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 829,411 | 8.294 | 20 | 20 | fits | 162,475 | 124 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 147,474 | 1.475 | 20 | 200 | fits | 152,156 | 219 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 956,139 | 9.561 | 20 | 200 | fits | 162,475 | 124 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 148,386 | 1.484 | 20 | 20 | fits | 152,156 | 219 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 956,835 | 9.568 | 20 | 20 | fits | 162,475 | 124 | 0.579 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 151,971 | 1.520 | 20 | 24 | fits | 152,156 | 219 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,006,213 | 10.062 | 20 | 24 | fits | 45,943 | 33 | 0.602 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 150,931 | 1.509 | 20 | 50 | fits | 152,156 | 219 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 797,340 | 7.973 | 20 | 50 | fits | 163,269 | 157 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 309,553 | 3.096 | 20 | 20 | fits | 159,077 | 80 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 795,260 | 7.953 | 20 | 20 | fits | 163,269 | 157 | 0.566 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,470 | 0.085 | 20 | 20 | fits | 31,564 | 20 | 0.782 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 147,474 | 1.475 | 20 | 200 | fits | 152,156 | 219 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 30,981 | 0.310 | 20 | 200 | fits | 31,564 | 20 | 0.782 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 148,386 | 1.484 | 20 | 20 | fits | 152,156 | 219 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 943,747 | 9.437 | 20 | 20 | fits | 149,387 | 117 | 0.557 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 151,971 | 1.520 | 20 | 24 | fits | 152,156 | 219 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 992,798 | 9.928 | 20 | 24 | fits | 45,616 | 33 | 0.596 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 150,931 | 1.509 | 20 | 50 | fits | 152,156 | 219 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 797,340 | 7.973 | 20 | 50 | fits | 163,269 | 157 | 0.566 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 309,553 | 3.096 | 20 | 20 | fits | 159,077 | 80 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 795,260 | 7.953 | 20 | 20 | fits | 163,269 | 157 | 0.566 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,369,748 | 63.697 | 20 | 20 | MISS ceiling | 21,673 | 14 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,391,408 | 63.914 | 20 | 20 | MISS ceiling | 21,735 | 14 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,412,928 | 64.129 | 20 | 20 | MISS ceiling | 21,655 | 14 | 0.619 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,434,655 | 64.347 | 20 | 20 | MISS ceiling | 21,723 | 14 | 0.591 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,456,163 | 64.562 | 20 | 20 | MISS ceiling | 21,571 | 14 | 0.609 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 169,602 | 1.696 | 20 | 200 | fits | 157,589 | 198 | 0.523 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 797,146 | 7.971 | 20 | 200 | fits | 153,407 | 158 | 0.541 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 165,343 | 1.653 | 20 | 20 | fits | 157,589 | 198 | 0.523 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,256,783 | 62.568 | 20 | 20 | MISS ceiling | 34,870 | 16 | 0.761 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 168,928 | 1.689 | 20 | 24 | fits | 157,589 | 198 | 0.523 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,190,282 | 61.903 | 20 | 24 | MISS ceiling | 168,877 | 131 | 0.488 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 167,888 | 1.679 | 20 | 50 | fits | 157,589 | 198 | 0.523 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 795,651 | 7.957 | 20 | 50 | fits | 153,407 | 158 | 0.541 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 328,667 | 3.287 | 20 | 20 | fits | 161,234 | 80 | 0.644 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 793,571 | 7.936 | 20 | 20 | fits | 153,407 | 158 | 0.541 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,836 | 0.078 | 20 | 20 | fits | 38,333 | 22 (29) | 0.653 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 14,745 | 0.147 | 20 | 20 | fits | 38,333 | 22 (29) | 0.653 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,127 | 0.081 | 20 | 20 | fits | 40,637 | 33 (35) | 0.650 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 15,670 | 0.157 | 20 | 20 | fits | 40,637 | 33 (35) | 0.650 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 19,231 | 0.192 | 20 | 20 | fits | 37,242 | 25 (12) | 0.820 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 35,844 | 0.358 | 20 | 20 | fits | 35,558 | 29 (12) | 0.793 |
| LINK_UP | `adp.link_up.if0` | 2,381 | 0.024 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 15,617 | 0.156 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,490 | 0.105 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 6,069 | 0.061 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| LINK_DOWN | `adp.link_down.if0` | 2,089 | 0.021 | 20 | 200 | fits | 59,799 | 39 (9) | 0.701 |
| LINK_DOWN | `adp.link_down.if1` | 27,132 | 0.271 | 20 | 200 | fits | 59,799 | 39 (9) | 0.701 |
| LINK_UP | `adp.link_up.if0` | 2,381 | 0.024 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 15,617 | 0.156 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,490 | 0.105 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 6,069 | 0.061 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| GM_CHANGE | `adp.gm_change.if0` | 2,207 | 0.022 | 20 | 200 | fits | 20,390 | 27 (11) | 0.646 |
| GM_CHANGE | `adp.gm_change.if1` | 3,931 | 0.039 | 20 | 200 | fits | 20,390 | 27 (11) | 0.646 |
| LINK_UP | `adp.link_up.if0` | 2,381 | 0.024 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 15,617 | 0.156 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,490 | 0.105 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 6,069 | 0.061 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,533 | 0.045 | 20 | 200 | fits | 24,649 | 28 (31) | 0.458 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 5,983 | 0.060 | 20 | 200 | fits | 24,649 | 28 (31) | 0.458 |
| LINK_UP | `adp.link_up.if0` | 2,381 | 0.024 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 15,617 | 0.156 | 20 | 200 | fits | 42,385 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,490 | 0.105 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 6,069 | 0.061 | 20 | 200 | fits | 28,166 | 39 (39) | 0.623 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,533 | 0.045 | 20 | 200 | fits | 20,127 | 17 (31) | 0.632 |
| set_name | `aecp_fanout.set_name.if0` | 61,077 | 0.611 | 20 | 24 | fits | 76,145 | 161 | 0.418 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 67,274 | 0.673 | 20 | 24 | fits | 63,749 | 140 | 0.420 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 51,565 | 0.516 | 20 | 24 | fits | 60,402 | 140 | 0.382 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 77,636 | 0.776 | 20 | 24 | fits | 72,697 | 149 | 0.396 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 65,837 | 0.658 | 20 | 24 | fits | 62,344 | 116 | 0.418 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 51,021 | 0.510 | 20 | 24 | fits | 60,259 | 140 | 0.377 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 64,873 | 0.649 | 20 | 24 | fits | 59,206 | 140 | 0.364 |
| set_name | `aecp_fanout.set_name.if1` | 71,067 | 0.711 | 20 | 24 | fits | 67,715 | 117 | 0.398 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 54,033 | 0.540 | 20 | 24 | fits | 64,436 | 140 | 0.427 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 64,796 | 0.648 | 20 | 24 | fits | 59,901 | 140 | 0.378 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 65,188 | 0.652 | 20 | 24 | fits | 60,155 | 140 | 0.381 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 51,117 | 0.511 | 20 | 24 | fits | 60,200 | 140 | 0.378 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 64,873 | 0.649 | 20 | 24 | fits | 59,344 | 140 | 0.365 |
| BIND_RX | `acmp.bind_rx.if0` | 21,082 | 0.211 | 20 | 20 | fits | 46,236 | 27 (77) | 0.795 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,167 | 0.102 | 20 | 20 | fits | 34,041 | 21 (32) | 0.819 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,850 | 0.108 | 20 | 20 | fits | 29,108 | 16 (47) | 0.764 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,311 | 0.143 | 20 | 20 | fits | 41,239 | 20 (50) | 0.823 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,586 | 0.116 | 20 | 20 | fits | 29,670 | 18 (48) | 0.755 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,445 | 0.094 | 20 | 20 | fits | 27,911 | 17 (48) | 0.712 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 17,650 | 0.176 | 20 | 20 | fits | 39,618 | 26 (48) | 0.695 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 10,162 | 0.102 | 20 | 20 | fits | 28,458 | 17 (48) | 0.752 |
| BIND_RX | `acmp.bind_rx.if1` | 18,358 | 0.184 | 20 | 20 | fits | 42,546 | 28 (77) | 0.745 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 9,600 | 0.096 | 20 | 20 | fits | 34,672 | 21 (32) | 0.821 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 9,280 | 0.093 | 20 | 20 | fits | 28,256 | 19 (47) | 0.714 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 15,630 | 0.156 | 20 | 20 | fits | 45,107 | 20 (50) | 0.843 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if1` | 9,990 | 0.100 | 20 | 20 | fits | 28,940 | 20 (48) | 0.721 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 11,240 | 0.112 | 20 | 20 | fits | 29,404 | 20 (48) | 0.743 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 10,873 | 0.109 | 20 | 20 | fits | 29,018 | 18 (48) | 0.752 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if1` | 8,603 | 0.086 | 20 | 20 | fits | 27,444 | 18 (48) | 0.699 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 22,348 | 0.223 | 20 | 24 | fits | 29,925 | 22 | 0.792 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 19,408 | 0.194 | 20 | 24 | fits | 34,288 | 22 | 0.711 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 14,997 | 0.150 | 20 | 24 | fits | 30,812 | 22 | 0.744 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 25,424 | 0.254 | 20 | 24 | fits | 29,914 | 22 | 0.722 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 15,493 | 0.155 | 20 | 24 | fits | 30,064 | 22 | 0.727 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 26,229 | 0.262 | 20 | 24 | fits | 30,335 | 22 | 0.724 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 15,338 | 0.153 | 20 | 24 | fits | 29,535 | 22 | 0.733 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 14,670 | 0.147 | 20 | 24 | fits | 40,675 | 31 | 0.711 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 24,236 | 0.242 | 20 | 24 | fits | 29,255 | 22 | 0.741 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 20,604 | 0.206 | 20 | 24 | fits | 34,684 | 23 | 0.655 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 24,565 | 0.246 | 20 | 24 | fits | 29,061 | 22 | 0.758 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 14,948 | 0.149 | 20 | 24 | fits | 29,217 | 22 | 0.764 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 24,940 | 0.249 | 20 | 24 | fits | 29,017 | 22 | 0.726 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 25,904 | 0.259 | 20 | 24 | fits | 30,727 | 22 | 0.741 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,673 | 0.157 | 20 | 24 | fits | 30,465 | 22 | 0.740 |
| get_configuration | `aecp.get_configuration.if0` | 22,904 | 0.229 | 20 | 24 | fits | 26,479 | 22 | 0.734 |
| entity_available | `aecp.entity_available.if0` | 13,923 | 0.139 | 20 | 24 | fits | 27,482 | 22 | 0.743 |
| get_name | `aecp.get_name.if0` | 24,587 | 0.246 | 20 | 24 | fits | 29,640 | 22 | 0.751 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 26,923 | 0.269 | 20 | 24 | fits | 31,098 | 29 | 0.724 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 16,913 | 0.169 | 20 | 24 | fits | 31,139 | 31 | 0.762 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 16,808 | 0.168 | 20 | 24 | fits | 27,621 | 22 | 0.767 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 13,793 | 0.138 | 20 | 24 | fits | 26,352 | 22 | 0.725 |
| set_name | `aecp.set_name.if0` | 45,602 | 0.456 | 20 | 24 | fits | 49,666 | 66 | 0.692 |
| lock_entity | `aecp.lock_entity.if0` | 36,751 | 0.368 | 20 | 24 | fits | 35,356 | 47 | 0.717 |
| unlock_entity | `aecp.unlock_entity.if0` | 28,282 | 0.283 | 20 | 24 | fits | 35,553 | 46 | 0.720 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 24,246 | 0.242 | 20 | 24 | fits | 28,441 | 20 | 0.763 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 21,250 | 0.212 | 20 | 24 | fits | 32,914 | 20 | 0.717 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 18,572 | 0.186 | 20 | 24 | fits | 41,708 | 29 | 0.718 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 27,920 | 0.279 | 20 | 24 | fits | 29,740 | 20 | 0.730 |
| get_configuration | `aecp.get_configuration.if1` | 16,138 | 0.161 | 20 | 24 | fits | 26,960 | 20 | 0.755 |
| entity_available | `aecp.entity_available.if1` | 26,132 | 0.261 | 20 | 24 | fits | 26,944 | 20 | 0.743 |
| get_name | `aecp.get_name.if1` | 18,613 | 0.186 | 20 | 24 | fits | 30,080 | 20 | 0.767 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if1` | 37,300 | 0.373 | 20 | 24 | fits | 42,673 | 36 | 0.704 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if1` | 28,693 | 0.287 | 20 | 24 | fits | 30,192 | 29 | 0.757 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if1` | 17,074 | 0.171 | 20 | 24 | fits | 27,491 | 20 | 0.770 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 24,711 | 0.247 | 20 | 24 | fits | 25,825 | 20 | 0.718 |
| set_name | `aecp.set_name.if1` | 34,983 | 0.350 | 20 | 24 | fits | 43,383 | 25 | 0.756 |
| lock_entity | `aecp.lock_entity.if1` | 33,222 | 0.332 | 20 | 24 | fits | 48,262 | 59 | 0.685 |
| unlock_entity | `aecp.unlock_entity.if1` | 21,797 | 0.218 | 20 | 24 | fits | 35,840 | 49 | 0.694 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
