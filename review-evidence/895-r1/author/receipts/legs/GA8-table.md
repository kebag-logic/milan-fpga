### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 136 paths and 7 of 996 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.209 (0.458) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.182 (0.431) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.097 (0.287) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.085 (0.275) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.098 (0.430) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.177 (0.430) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.084 (0.405) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.159 (0.405) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.104 (0.294) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.100 (0.295) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.084 (0.271) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.086 (0.273) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.090 (0.280) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.106 (0.298) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.103 (0.297) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.107 (0.300) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.103 (0.362) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.098 (0.364) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.455 (1.656) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.436 (0.763) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.160 (0.713) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.441 (0.717) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.279 (0.825) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.392 (0.825) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.080 (0.631) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.168 (0.631) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.165 (0.603) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.264 (0.788) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.265 (0.780) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.350 (0.780) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.147 (0.416) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.145 (0.429) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.056 (0.258) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.070 (0.258) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.028 (0.224) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.050 (0.224) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.027 (0.449) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.179 (0.449) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.030 (0.429) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.159 (0.429) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.211 (0.426) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.186 (0.426) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.260 (0.658) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.208 (0.658) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.121 (0.513) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.083 (0.261) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.264 (0.610) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 1 | `aecp.get_avb_info.if1` (aecp) | 0.117 (0.297) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.267 (0.640) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.153 (0.537) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.306 (0.698) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 1 | `aecp.get_counters.if1` (aecp) | 0.184 (0.399) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.282 (0.669) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.171 (0.567) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.241 (0.627) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.244 (0.618) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.125 (0.513) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.077 (0.253) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.203 (0.607) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.207 (0.609) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.157 (0.397) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.178 (0.576) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.278 (0.666) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.292 (0.684) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.191 (0.600) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.278 (0.670) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.143 (0.539) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.092 (0.296) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.112 (0.292) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.149 (0.384) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.094 (0.300) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.158 (0.552) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.153 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.100 (0.303) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.145 (0.544) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.295 (0.679) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.123 (0.523) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.389 (0.586) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.345 (0.710) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.257 (0.642) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 1 | `aecp.unknown_command.if1` (aecp) | 0.155 (0.541) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.315 (0.664) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.232 (0.591) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.507 (0.893) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.501 (0.885) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.485 (0.640) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.536 (0.930) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.550 (0.696) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 0.503 (0.886) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.612 (1.035) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.518 (0.672) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.476 (0.628) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.458 (0.598) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.454 (0.593) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.700 (7.590) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-7.adp_available.if0` (backlog-adp@verify-aged2-7) | 8.605 (9.722) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.180 (0.615) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.800 (2.625) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.634 (63.822) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.571 (64.776) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 8.666 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 1.678 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 3.940 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 6.747 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 4.962 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.172 (0.586) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.178 (0.594) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.112 (0.273) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.114 (0.274) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.135 (0.329) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.121 (0.312) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.155 (0.586) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.161 (0.594) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.261 (0.655) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 0.261 (0.660) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.852 | fits | 0 srp | 6 | 0 |
| an MRPDU its join timer owes, the longest | 1 | `save-held.mrpdu.periodic.if1` (save-held) | 3.804 | fits | 0 srp | 6 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 2.233 | fits | 0 acmp | 76 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.471 | MISS ceiling | 11 acmp | 76 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 2.224 | fits | 0 adp | 76 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-3.service.adp.last.if0` (backlog-adp@verify-aged2-3) | 9.705 | fits | 7 adp | 74 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 7.121 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.269 | fits | 0 aecp | 76 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 61.793 | MISS ceiling | 15 aecp | 76 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 2.259 | fits | 0 maap | 76 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-3.service.maap.last.if0` (backlog-adp@program-aged2-3) | 9.801 | fits | 6 maap | 76 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 6.402 | fits | 0 srp | 76 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-aged2-6.service.srp.last.if1` (backlog-adp@blank-aged2-6) | 9.646 | fits | 31 srp | 76 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.913 (1.267) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 0.791 (1.105) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.496 (0.497) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.428 (0.429) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.252 (0.253) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.235 (0.236) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.785 (0.848) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 0.738 (0.788) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.305 | 8 | 166,218 (1.662) | yes | - |
| backlog-adp@blank-1 | 0 | 10.713 | 8 | 159,662 (1.597) | yes | - |
| backlog-adp@blank-2 | 0 | 10.745 | 8 | 163,827 (1.638) | yes | - |
| backlog-adp@blank-3 | 0 | 10.752 | 9 | 162,549 (1.625) | yes | - |
| backlog-adp@blank-4 | 0 | 10.531 | 7 | 162,399 (1.624) | yes | - |
| backlog-adp@blank-5 | 0 | 10.728 | 8 | 156,414 (1.564) | yes | - |
| backlog-adp@blank-6 | 0 | 10.500 | 7 | 160,336 (1.603) | yes | - |
| backlog-adp@blank-7 | 0 | 10.720 | 8 | 159,314 (1.593) | yes | - |
| backlog-adp@program-0 | 0 | 10.619 | 7 | 161,491 (1.615) | yes | - |
| backlog-adp@program-1 | 0 | 10.905 | 8 | 163,675 (1.637) | yes | - |
| backlog-adp@program-2 | 0 | 10.630 | 7 | 166,290 (1.663) | yes | - |
| backlog-adp@program-3 | 0 | 11.087 | 10 | 161,458 (1.615) | yes | - |
| backlog-adp@program-4 | 0 | 10.051 | 8 | 160,890 (1.609) | yes | - |
| backlog-adp@program-5 | 0 | 10.176 | 8 | 163,691 (1.637) | yes | - |
| backlog-adp@program-6 | 0 | 10.134 | 9 | 161,417 (1.614) | yes | - |
| backlog-adp@program-7 | 0 | 9.987 | 8 | 161,356 (1.614) | yes | - |
| backlog-adp@verify-0 | 0 | 10.815 | 8 | 160,923 (1.609) | yes | - |
| backlog-adp@verify-1 | 0 | 11.124 | 9 | 161,618 (1.616) | yes | - |
| backlog-adp@verify-2 | 0 | 10.778 | 8 | 154,184 (1.542) | yes | - |
| backlog-adp@verify-3 | 0 | 10.806 | 8 | 161,259 (1.613) | yes | - |
| backlog-adp@verify-4 | 0 | 10.529 | 7 | 165,613 (1.656) | yes | - |
| backlog-adp@verify-5 | 0 | 10.745 | 8 | 154,099 (1.541) | yes | - |
| backlog-adp@verify-6 | 0 | 11.460 | 10 | 159,890 (1.599) | yes | - |
| backlog-adp@verify-7 | 0 | 12.258 | 11 | 161,209 (1.612) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.890 | 10 | 161,707 (1.617) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.462 | 7 | 161,272 (1.613) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.659 | 7 | 158,080 (1.581) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.483 | 6 | 159,108 (1.591) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.417 | 6 | 159,861 (1.599) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.145 | 9 | 163,097 (1.631) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.800 | 8 | 165,598 (1.656) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.770 | 8 | 159,512 (1.595) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.181 | 10 | 163,706 (1.637) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.966 | 10 | 162,215 (1.622) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 10.857 | 9 | 162,485 (1.625) | yes | - |
| backlog-adp@blank-aged1-3 | 1 | 10.645 | 7 | 161,560 (1.616) | yes | - |
| backlog-adp@blank-aged1-4 | 1 | 10.637 | 7 | 159,358 (1.594) | yes | - |
| backlog-adp@blank-aged1-5 | 1 | 10.425 | 6 | 162,117 (1.621) | yes | - |
| backlog-adp@blank-aged1-6 | 1 | 10.362 | 6 | 164,117 (1.641) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 10.401 | 6 | 162,051 (1.621) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.033 | 8 | 158,651 (1.587) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.608 | 8 | 163,677 (1.637) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.427 | 7 | 165,779 (1.658) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.907 | 9 | 161,547 (1.615) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.503 | 7 | 163,613 (1.636) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.709 | 8 | 163,613 (1.636) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.533 | 7 | 163,605 (1.636) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.740 | 8 | 159,390 (1.594) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.022 | 8 | 163,613 (1.636) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.826 | 8 | 163,613 (1.636) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.884 | 8 | 157,878 (1.579) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.575 | 10 | 158,662 (1.587) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.106 | 9 | 162,425 (1.624) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.105 | 10 | 162,182 (1.622) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.523 | 7 | 163,613 (1.636) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.802 | 8 | 158,509 (1.585) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 12.261 | 11 | 154,146 (1.541) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.012 | 10 | 161,563 (1.616) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.905 | 9 | 163,706 (1.637) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.709 | 8 | 159,705 (1.597) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 10.439 | 7 | 160,158 (1.602) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.484 | 7 | 162,695 (1.627) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.705 | 8 | 154,408 (1.544) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.702 | 8 | 159,876 (1.599) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.743 | 8 | 165,807 (1.658) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.794 | 8 | 162,401 (1.624) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.855 | 8 | 154,146 (1.541) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.084 | 9 | 161,317 (1.613) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.524 | 7 | 159,409 (1.594) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.510 | 7 | 163,655 (1.637) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.467 | 7 | 159,289 (1.593) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 10.788 | 8 | 160,284 (1.603) | yes | - |
| backlog | 0 | 8.477 | 8 | 168,175 (1.682) | yes | - |
| backlog-adp | 0 | 9.695 | 7 | 165,363 (1.654) | yes | - |
| backlog-adp-refill | 0 | 41.035 | 22 | 160,241 (1.602) | yes | - |
| backlog-owed | 0 | 65.422 | 23 | 164,351 (1.644) | yes | - |

Composed maximum over the 4 backlog windows: 168,175 CPU cycles (1.682 ms), backlog.
Over the windows that released their whole load only: 168,175 (1.682 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 111929 | 0 | 54,208 (0.542) | fits |
| save-held | 2728 | 0 | 163,966 (1.640) | fits |
| save-starved | 53091 | 0 | 163,966 (1.640) | fits |
| acmp-notk | 4624 | 0 | 106,535 (1.065) | fits |
| backlog-adp@blank-0 | 548 | 0 | 166,218 (1.662) | fits |
| backlog-adp@blank-1 | 548 | 0 | 159,662 (1.597) | fits |
| backlog-adp@blank-2 | 548 | 0 | 163,827 (1.638) | fits |
| backlog-adp@blank-3 | 549 | 0 | 162,549 (1.625) | fits |
| backlog-adp@blank-4 | 549 | 0 | 162,399 (1.624) | fits |
| backlog-adp@blank-5 | 550 | 0 | 156,414 (1.564) | fits |
| backlog-adp@blank-6 | 549 | 0 | 160,336 (1.603) | fits |
| backlog-adp@blank-7 | 550 | 0 | 159,314 (1.593) | fits |
| backlog-adp@program-0 | 921 | 0 | 161,619 (1.616) | fits |
| backlog-adp@program-1 | 922 | 0 | 163,675 (1.637) | fits |
| backlog-adp@program-2 | 921 | 0 | 166,290 (1.663) | fits |
| backlog-adp@program-3 | 924 | 0 | 161,458 (1.615) | fits |
| backlog-adp@program-4 | 925 | 0 | 160,890 (1.609) | fits |
| backlog-adp@program-5 | 925 | 0 | 163,691 (1.637) | fits |
| backlog-adp@program-6 | 926 | 0 | 161,417 (1.614) | fits |
| backlog-adp@program-7 | 927 | 0 | 161,356 (1.614) | fits |
| backlog-adp@verify-0 | 1283 | 0 | 160,923 (1.609) | fits |
| backlog-adp@verify-1 | 1285 | 0 | 161,618 (1.616) | fits |
| backlog-adp@verify-2 | 1285 | 0 | 154,184 (1.542) | fits |
| backlog-adp@verify-3 | 1285 | 0 | 161,259 (1.613) | fits |
| backlog-adp@verify-4 | 1284 | 0 | 165,613 (1.656) | fits |
| backlog-adp@verify-5 | 1285 | 0 | 154,099 (1.541) | fits |
| backlog-adp@verify-6 | 1287 | 0 | 159,890 (1.599) | fits |
| backlog-adp@verify-7 | 1288 | 0 | 161,209 (1.612) | fits |
| backlog-adp@blank-aged2-0 | 780 | 0 | 161,707 (1.617) | fits |
| backlog-adp@blank-aged2-1 | 784 | 0 | 161,272 (1.613) | fits |
| backlog-adp@blank-aged2-2 | 790 | 0 | 158,080 (1.581) | fits |
| backlog-adp@blank-aged2-3 | 795 | 0 | 159,108 (1.591) | fits |
| backlog-adp@blank-aged2-4 | 801 | 0 | 159,861 (1.599) | fits |
| backlog-adp@blank-aged2-5 | 810 | 0 | 163,097 (1.631) | fits |
| backlog-adp@blank-aged2-6 | 815 | 0 | 165,598 (1.656) | fits |
| backlog-adp@blank-aged2-7 | 821 | 0 | 159,512 (1.595) | fits |
| backlog-adp@blank-aged1-0 | 732 | 0 | 163,706 (1.637) | fits |
| backlog-adp@blank-aged1-1 | 738 | 0 | 162,215 (1.622) | fits |
| backlog-adp@blank-aged1-2 | 743 | 0 | 162,485 (1.625) | fits |
| backlog-adp@blank-aged1-3 | 748 | 0 | 161,560 (1.616) | fits |
| backlog-adp@blank-aged1-4 | 754 | 0 | 159,358 (1.594) | fits |
| backlog-adp@blank-aged1-5 | 759 | 0 | 162,117 (1.621) | fits |
| backlog-adp@blank-aged1-6 | 765 | 0 | 164,117 (1.641) | fits |
| backlog-adp@blank-aged1-7 | 771 | 0 | 162,051 (1.621) | fits |
| backlog-adp@program-aged2-0 | 1149 | 0 | 158,651 (1.587) | fits |
| backlog-adp@program-aged2-1 | 1155 | 0 | 163,677 (1.637) | fits |
| backlog-adp@program-aged2-2 | 1160 | 0 | 165,779 (1.658) | fits |
| backlog-adp@program-aged2-3 | 1168 | 0 | 161,547 (1.615) | fits |
| backlog-adp@program-aged2-4 | 1172 | 0 | 163,613 (1.636) | fits |
| backlog-adp@program-aged2-5 | 1179 | 0 | 163,613 (1.636) | fits |
| backlog-adp@program-aged2-6 | 1184 | 0 | 163,605 (1.636) | fits |
| backlog-adp@program-aged2-7 | 1191 | 0 | 159,390 (1.594) | fits |
| backlog-adp@program-aged1-0 | 1101 | 0 | 163,613 (1.636) | fits |
| backlog-adp@program-aged1-1 | 1107 | 0 | 163,613 (1.636) | fits |
| backlog-adp@program-aged1-2 | 1113 | 0 | 157,878 (1.579) | fits |
| backlog-adp@program-aged1-3 | 1121 | 0 | 158,662 (1.587) | fits |
| backlog-adp@program-aged1-4 | 1126 | 0 | 162,425 (1.624) | fits |
| backlog-adp@program-aged1-5 | 1133 | 0 | 162,182 (1.622) | fits |
| backlog-adp@program-aged1-6 | 1136 | 0 | 163,613 (1.636) | fits |
| backlog-adp@program-aged1-7 | 1143 | 0 | 158,509 (1.585) | fits |
| backlog-adp@verify-aged2-0 | 1518 | 0 | 154,146 (1.541) | fits |
| backlog-adp@verify-aged2-1 | 1523 | 0 | 161,563 (1.616) | fits |
| backlog-adp@verify-aged2-2 | 1528 | 0 | 163,706 (1.637) | fits |
| backlog-adp@verify-aged2-3 | 1533 | 0 | 159,705 (1.597) | fits |
| backlog-adp@verify-aged2-4 | 1538 | 0 | 160,158 (1.602) | fits |
| backlog-adp@verify-aged2-5 | 1544 | 0 | 162,695 (1.627) | fits |
| backlog-adp@verify-aged2-6 | 1551 | 0 | 154,408 (1.544) | fits |
| backlog-adp@verify-aged2-7 | 1557 | 0 | 159,876 (1.599) | fits |
| backlog-adp@verify-aged1-0 | 1467 | 0 | 165,807 (1.658) | fits |
| backlog-adp@verify-aged1-1 | 1473 | 0 | 162,401 (1.624) | fits |
| backlog-adp@verify-aged1-2 | 1479 | 0 | 154,146 (1.541) | fits |
| backlog-adp@verify-aged1-3 | 1486 | 0 | 161,317 (1.613) | fits |
| backlog-adp@verify-aged1-4 | 1490 | 0 | 159,409 (1.594) | fits |
| backlog-adp@verify-aged1-5 | 1496 | 0 | 163,655 (1.637) | fits |
| backlog-adp@verify-aged1-6 | 1502 | 0 | 159,289 (1.593) | fits |
| backlog-adp@verify-aged1-7 | 1509 | 0 | 160,284 (1.603) | fits |
| adp-advertise | 599 | 0 | 51,538 (0.515) | fits |
| maap | 349 | 0 | 51,850 (0.518) | fits |
| acmp-noresp | 2579 | 0 | 106,146 (1.061) | fits |
| save | 611 | 0 | 51,538 (0.515) | fits |
| srp | 306 | 0 | 80,421 (0.804) | fits |
| backlog | 288 | 0 | 168,175 (1.682) | fits |
| backlog-adp | 312 | 0 | 165,363 (1.654) | fits |
| backlog-adp-refill | 327 | 0 | 160,241 (1.602) | fits |
| backlog-owed | 309 | 0 | 164,351 (1.644) | fits |
| acmp-disc | 1319 | 0 | 103,409 (1.034) | fits |
| adp-link | 91 | 0 | 51,538 (0.515) | fits |
| adp-gm | 89 | 0 | 51,538 (0.515) | fits |
| adp-discover | 89 | 0 | 51,538 (0.515) | fits |
| control | 89 | 0 | 51,538 (0.515) | fits |
| aecp-fanout | 141 | 0 | 74,836 (0.748) | fits |
| acmp-cmd | 105 | 0 | 51,538 (0.515) | fits |
| aecp | 132 | 0 | 58,607 (0.586) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 9.175 (20) | 10.825 |
| backlog-adp@blank-aged2-1 | 2 | none | +9.268 ms, 77,336 (0.773 ms), read-back | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 9.257 (20) | 10.743 |
| backlog-adp@blank-aged2-2 | 2 | +8.796 ms, 77,483 (0.775 ms), read-back | none | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 10.013 (20) | 9.987 |
| backlog-adp@blank-aged2-3 | 2 | +7.539 ms, 77,238 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 9.838 (20) | 10.162 |
| backlog-adp@blank-aged2-4 | 2 | +6.238 ms, 77,192 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 9.777 (20) | 10.223 |
| backlog-adp@blank-aged2-5 | 2 | +6.395 ms, 77,173 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 9.999 (20) | 10.001 |
| backlog-adp@blank-aged2-6 | 2 | +6.419 ms, 77,363 (0.774 ms), read-back | none | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 10.159 (20) | 9.841 |
| backlog-adp@blank-aged2-7 | 2 | +3.195 ms, 77,259 (0.773 ms), read-back | none | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 10.131 (20) | 9.869 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.aecp.last.if1` | 9.053 (20) | 10.947 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.aecp.last.if1` | 8.980 (20) | 11.020 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.aecp.last.if1` | 9.457 (20) | 10.543 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.aecp.last.if1` | 9.243 (20) | 10.757 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.aecp.last.if1` | 9.238 (20) | 10.762 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.aecp.last.if1` | 9.019 (20) | 10.981 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.aecp.last.if1` | 8.959 (20) | 11.041 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.aecp.last.if1` | 8.998 (20) | 11.002 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 9.082 (20) | 10.918 |
| backlog-adp@program-aged2-1 | 2 | none | +9.374 ms, 80,875 (0.809 ms), issue | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 9.098 (20) | 10.902 |
| backlog-adp@program-aged2-2 | 2 | none | +9.191 ms, 80,980 (0.810 ms), issue | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 9.179 (20) | 10.821 |
| backlog-adp@program-aged2-3 | 2 | +7.449 ms, 80,950 (0.809 ms), issue | none | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 10.267 (20) | 9.733 |
| backlog-adp@program-aged2-4 | 2 | +5.747 ms, 81,042 (0.810 ms), issue | none | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 9.858 (20) | 10.142 |
| backlog-adp@program-aged2-5 | 2 | +4.649 ms, 81,042 (0.810 ms), issue | none | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 10.070 (20) | 9.930 |
| backlog-adp@program-aged2-6 | 2 | +4.707 ms, 81,042 (0.810 ms), issue | none | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 9.892 (20) | 10.108 |
| backlog-adp@program-aged2-7 | 2 | +3.205 ms, 80,986 (0.810 ms), issue | none | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 10.101 (20) | 9.899 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.aecp.last.if1` | 9.073 (20) | 10.927 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.aecp.last.if1` | 9.388 (20) | 10.612 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.aecp.last.if1` | 9.446 (20) | 10.554 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.aecp.last.if1` | 9.423 (20) | 10.577 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.aecp.last.if1` | 9.127 (20) | 10.873 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.aecp.last.if1` | 9.336 (20) | 10.664 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.aecp.last.if1` | 9.083 (20) | 10.917 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.aecp.last.if1` | 9.365 (20) | 10.635 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 9.287 (20) | 10.713 |
| backlog-adp@verify-aged2-1 | 2 | none | none | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 9.005 (20) | 10.995 |
| backlog-adp@verify-aged2-2 | 2 | none | none | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 9.162 (20) | 10.838 |
| backlog-adp@verify-aged2-3 | 2 | none | none | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 10.071 (20) | 9.929 |
| backlog-adp@verify-aged2-4 | 2 | none | none | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 9.796 (20) | 10.204 |
| backlog-adp@verify-aged2-5 | 2 | +5.900 ms, 78,239 (0.782 ms), read-back | none | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 9.841 (20) | 10.159 |
| backlog-adp@verify-aged2-6 | 2 | +4.693 ms, 78,239 (0.782 ms), read-back | none | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 10.066 (20) | 9.934 |
| backlog-adp@verify-aged2-7 | 2 | none | none | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 10.064 (20) | 9.936 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.aecp.last.if1` | 9.104 (20) | 10.896 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.aecp.last.if1` | 9.124 (20) | 10.876 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.aecp.last.if1` | 9.443 (20) | 10.557 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.aecp.last.if1` | 9.120 (20) | 10.880 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.aecp.last.if1` | 8.999 (20) | 11.001 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.aecp.last.if1` | 9.092 (20) | 10.908 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.aecp.last.if1` | 9.051 (20) | 10.949 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.aecp.last.if1` | 9.376 (20) | 10.624 |

Least margin over the aged windows: 9.733 ms, `backlog-adp@program-aged2-3.service.aecp.last.if1` at 10.267 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22110.064 | 22,150 | 370 | 2 | 31.310 | yes | within |
| save-held | 4697.473 | 12,110 | 370 | - | 14.978 | no | within |
| save-starved | 12088.470 | 12,110 | 370 | - | 33.038 | yes | within |
| save | 4698.022 | 12,110 | 370 | - | 11.884 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1056 | 80,462 (0.805) | 78,155 (0.782) |
| save-held | 1526 | 104,117 (1.041) | 78,918 (0.789) |
| save-starved | 686 | 81,291 (0.813) | 78,699 (0.787) |
| acmp-notk | 1065 | 106,535 (1.065) | 78,583 (0.786) |
| backlog-adp@blank-0 | 337 | 96,481 (0.965) | 76,543 (0.765) |
| backlog-adp@blank-1 | 337 | 96,543 (0.965) | 76,605 (0.766) |
| backlog-adp@blank-2 | 337 | 97,099 (0.971) | 76,544 (0.765) |
| backlog-adp@blank-3 | 337 | 96,392 (0.964) | 76,505 (0.765) |
| backlog-adp@blank-4 | 337 | 98,169 (0.982) | 76,453 (0.765) |
| backlog-adp@blank-5 | 337 | 96,870 (0.969) | 76,544 (0.765) |
| backlog-adp@blank-6 | 337 | 97,248 (0.972) | 76,707 (0.767) |
| backlog-adp@blank-7 | 337 | 96,830 (0.968) | 76,634 (0.766) |
| backlog-adp@program-0 | 443 | 100,746 (1.007) | 78,819 (0.788) |
| backlog-adp@program-1 | 443 | 100,746 (1.007) | 78,852 (0.789) |
| backlog-adp@program-2 | 443 | 100,746 (1.007) | 79,015 (0.790) |
| backlog-adp@program-3 | 443 | 101,524 (1.015) | 78,800 (0.788) |
| backlog-adp@program-4 | 444 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@program-5 | 444 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@program-6 | 444 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@program-7 | 444 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-0 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-1 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-2 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-3 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-4 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-5 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-6 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-7 | 547 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@blank-aged2-0 | 336 | 103,242 (1.032) | 76,545 (0.765) |
| backlog-adp@blank-aged2-1 | 335 | 77,336 (0.773) | 76,221 (0.762) |
| backlog-adp@blank-aged2-2 | 335 | 77,483 (0.775) | 76,311 (0.763) |
| backlog-adp@blank-aged2-3 | 335 | 77,238 (0.772) | 76,207 (0.762) |
| backlog-adp@blank-aged2-4 | 335 | 77,192 (0.772) | 76,207 (0.762) |
| backlog-adp@blank-aged2-5 | 335 | 77,173 (0.772) | 76,142 (0.761) |
| backlog-adp@blank-aged2-6 | 335 | 77,363 (0.774) | 76,189 (0.762) |
| backlog-adp@blank-aged2-7 | 335 | 77,259 (0.773) | 76,140 (0.761) |
| backlog-adp@blank-aged1-0 | 336 | 102,170 (1.022) | 76,708 (0.767) |
| backlog-adp@blank-aged1-1 | 335 | 96,022 (0.960) | 76,444 (0.764) |
| backlog-adp@blank-aged1-2 | 335 | 96,820 (0.968) | 76,545 (0.765) |
| backlog-adp@blank-aged1-3 | 335 | 96,923 (0.969) | 76,545 (0.765) |
| backlog-adp@blank-aged1-4 | 335 | 96,918 (0.969) | 76,545 (0.765) |
| backlog-adp@blank-aged1-5 | 335 | 97,273 (0.973) | 76,590 (0.766) |
| backlog-adp@blank-aged1-6 | 335 | 97,053 (0.971) | 76,480 (0.765) |
| backlog-adp@blank-aged1-7 | 335 | 97,053 (0.971) | 76,480 (0.765) |
| backlog-adp@program-aged2-0 | 442 | 100,748 (1.007) | 79,015 (0.790) |
| backlog-adp@program-aged2-1 | 441 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@program-aged2-2 | 441 | 100,746 (1.007) | 78,677 (0.787) |
| backlog-adp@program-aged2-3 | 441 | 100,746 (1.007) | 78,759 (0.788) |
| backlog-adp@program-aged2-4 | 441 | 100,746 (1.007) | 78,849 (0.788) |
| backlog-adp@program-aged2-5 | 441 | 100,746 (1.007) | 78,849 (0.788) |
| backlog-adp@program-aged2-6 | 441 | 100,746 (1.007) | 78,849 (0.788) |
| backlog-adp@program-aged2-7 | 441 | 100,746 (1.007) | 78,705 (0.787) |
| backlog-adp@program-aged1-0 | 442 | 100,746 (1.007) | 79,015 (0.790) |
| backlog-adp@program-aged1-1 | 441 | 100,746 (1.007) | 78,880 (0.789) |
| backlog-adp@program-aged1-2 | 441 | 100,746 (1.007) | 78,852 (0.789) |
| backlog-adp@program-aged1-3 | 441 | 100,746 (1.007) | 78,925 (0.789) |
| backlog-adp@program-aged1-4 | 441 | 100,746 (1.007) | 78,877 (0.789) |
| backlog-adp@program-aged1-5 | 441 | 100,746 (1.007) | 78,971 (0.790) |
| backlog-adp@program-aged1-6 | 441 | 100,746 (1.007) | 79,015 (0.790) |
| backlog-adp@program-aged1-7 | 441 | 100,746 (1.007) | 78,852 (0.789) |
| backlog-adp@verify-aged2-0 | 547 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged2-1 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged2-2 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged2-3 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged2-4 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged2-5 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged2-6 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged2-7 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged1-0 | 547 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged1-1 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged1-2 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged1-3 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged1-4 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged1-5 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged1-6 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| backlog-adp@verify-aged1-7 | 546 | 100,746 (1.007) | 78,630 (0.786) |
| adp-advertise | 577 | 26,513 (0.265) | 2,970 (0.030) |
| maap | 327 | 26,434 (0.264) | 2,970 (0.030) |
| acmp-noresp | 615 | 106,146 (1.061) | 78,630 (0.786) |
| save | 585 | 103,193 (1.032) | 78,391 (0.784) |
| srp | 278 | 26,391 (0.264) | 3,212 (0.032) |
| backlog | 266 | 26,465 (0.265) | 2,987 (0.030) |
| backlog-adp | 271 | 26,465 (0.265) | 3,162 (0.032) |
| backlog-adp-refill | 274 | 26,465 (0.265) | 3,089 (0.031) |
| backlog-owed | 277 | 26,465 (0.265) | 3,168 (0.032) |
| acmp-disc | 336 | 103,409 (1.034) | 78,540 (0.785) |
| adp-link | 79 | 26,252 (0.263) | 2,970 (0.030) |
| adp-gm | 79 | 26,252 (0.263) | 2,970 (0.030) |
| adp-discover | 79 | 26,252 (0.263) | 2,970 (0.030) |
| control | 79 | 26,252 (0.263) | 2,970 (0.030) |
| aecp-fanout | 92 | 27,302 (0.273) | 2,970 (0.030) |
| acmp-cmd | 67 | 26,252 (0.263) | 2,970 (0.030) |
| aecp | 88 | 26,252 (0.263) | 3,835 (0.038) |

Longest pass that carries a step: 106,535 CPU cycles (1.065 ms), acmp-notk; longest step: 79,015 (0.790 ms), backlog-adp@program-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 163,027 | 1.630 | 20 | 200 | fits | 163,966 | 235 | 0.451 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 852,946 | 8.529 | 20 | 20 | fits | 151,014 | 136 | 0.398 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 377,170 | 3.772 | 20 | 24 | fits | 44,428 | 33 | 0.552 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 662,457 | 6.625 | 20 | 50 | fits | 153,705 | 163 | 0.507 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 486,727 | 4.867 | 20 | 20 | fits | 109,870 | 41 | 0.460 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 91,066 | 0.911 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if1` | 136,651 | 1.367 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 264,117 | 2.641 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if1` | 331,055 | 3.311 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 285,243 | 2.852 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if1` | 380,447 | 3.804 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 167,821 | 1.678 | 20 | 200 | fits | 153,719 | 220 | 0.357 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 866,574 | 8.666 | 20 | 20 | fits | 152,387 | 142 | 0.399 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 394,033 | 3.940 | 20 | 24 | fits | 47,663 | 39 | 0.591 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 674,712 | 6.747 | 20 | 50 | fits | 156,537 | 169 | 0.518 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 496,150 | 4.962 | 20 | 20 | fits | 112,921 | 47 | 0.500 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 85,263 | 0.853 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if1` | 130,671 | 1.307 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 263,786 | 2.638 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if1` | 329,950 | 3.300 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 281,494 | 2.815 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if1` | 356,298 | 3.563 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 16,527 | 0.165 | 20 | 20 | fits | 34,166 | 22 (14) | 0.820 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 26,449 | 0.264 | 20 | 20 | fits | 39,146 | 19 (14) | 0.900 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 767,655 | 7.677 | 20 | 20 | fits | 166,218 | 175 | 0.526 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 222,433 | 2.224 | 20 | 200 | fits | 161,407 | 230 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 817,548 | 8.175 | 20 | 200 | fits | 166,218 | 175 | 0.526 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 223,345 | 2.233 | 20 | 20 | fits | 161,407 | 230 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 960,931 | 9.609 | 20 | 20 | fits | 142,687 | 125 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 226,930 | 2.269 | 20 | 24 | fits | 161,407 | 230 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 964,366 | 9.644 | 20 | 24 | fits | 142,687 | 125 | 0.449 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 225,890 | 2.259 | 20 | 50 | fits | 161,407 | 230 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 821,224 | 8.212 | 20 | 50 | fits | 166,218 | 175 | 0.526 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 379,315 | 3.793 | 20 | 20 | fits | 153,880 | 87 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 652,926 | 6.529 | 20 | 20 | fits | 125,730 | 51 | 0.526 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 716,580 | 7.166 | 20 | 20 | fits | 157,491 | 169 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 158,228 | 1.582 | 20 | 200 | fits | 159,662 | 226 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 745,475 | 7.455 | 20 | 200 | fits | 157,491 | 169 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 159,140 | 1.591 | 20 | 20 | fits | 159,662 | 226 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 901,768 | 9.018 | 20 | 20 | fits | 155,597 | 132 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 162,725 | 1.627 | 20 | 24 | fits | 159,662 | 226 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 905,203 | 9.052 | 20 | 24 | fits | 155,597 | 132 | 0.439 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 161,685 | 1.617 | 20 | 50 | fits | 159,662 | 226 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 749,151 | 7.492 | 20 | 50 | fits | 157,491 | 169 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 315,124 | 3.151 | 20 | 20 | fits | 153,894 | 87 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 589,580 | 5.896 | 20 | 20 | fits | 122,519 | 45 | 0.492 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 704,023 | 7.040 | 20 | 20 | fits | 163,827 | 172 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 148,963 | 1.490 | 20 | 200 | fits | 151,717 | 223 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 741,755 | 7.418 | 20 | 200 | fits | 163,827 | 172 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 149,875 | 1.499 | 20 | 20 | fits | 151,717 | 223 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 898,670 | 8.987 | 20 | 20 | fits | 156,219 | 125 | 0.508 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 153,460 | 1.535 | 20 | 24 | fits | 151,717 | 223 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 934,147 | 9.341 | 20 | 24 | fits | 32,042 | 20 | 0.665 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 152,420 | 1.524 | 20 | 50 | fits | 151,717 | 223 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 745,431 | 7.454 | 20 | 50 | fits | 163,827 | 172 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 306,429 | 3.064 | 20 | 20 | fits | 154,464 | 88 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 579,524 | 5.795 | 20 | 20 | fits | 120,397 | 45 | 0.440 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 279,089 | 2.791 | 20 | 20 | fits | 162,549 | 211 | 0.527 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 156,893 | 1.569 | 20 | 200 | fits | 160,967 | 231 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 328,477 | 3.285 | 20 | 200 | fits | 162,549 | 211 | 0.527 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 157,805 | 1.578 | 20 | 20 | fits | 160,967 | 231 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 898,846 | 8.988 | 20 | 20 | fits | 157,715 | 135 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 161,390 | 1.614 | 20 | 24 | fits | 160,967 | 231 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 902,281 | 9.023 | 20 | 24 | fits | 157,715 | 135 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 160,350 | 1.603 | 20 | 50 | fits | 160,967 | 231 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 332,153 | 3.322 | 20 | 50 | fits | 162,549 | 211 | 0.527 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 487,178 | 4.872 | 20 | 20 | fits | 155,090 | 49 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 742,031 | 7.420 | 20 | 20 | fits | 117,842 | 47 | 0.531 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 689,421 | 6.894 | 20 | 20 | fits | 162,399 | 186 | 0.536 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 155,951 | 1.560 | 20 | 200 | fits | 153,246 | 208 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 738,590 | 7.386 | 20 | 200 | fits | 162,399 | 186 | 0.536 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 156,863 | 1.569 | 20 | 20 | fits | 153,246 | 208 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 898,278 | 8.983 | 20 | 20 | fits | 158,992 | 140 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 160,448 | 1.604 | 20 | 24 | fits | 153,246 | 208 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 901,713 | 9.017 | 20 | 24 | fits | 158,992 | 140 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 159,408 | 1.594 | 20 | 50 | fits | 153,246 | 208 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 742,266 | 7.423 | 20 | 50 | fits | 162,399 | 186 | 0.536 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 312,801 | 3.128 | 20 | 20 | fits | 153,848 | 87 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 577,787 | 5.778 | 20 | 20 | fits | 127,694 | 51 | 0.497 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 680,002 | 6.800 | 20 | 20 | fits | 154,461 | 165 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 154,871 | 1.549 | 20 | 200 | fits | 153,286 | 208 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 729,572 | 7.296 | 20 | 200 | fits | 154,461 | 165 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 155,783 | 1.558 | 20 | 20 | fits | 153,286 | 208 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 896,923 | 8.969 | 20 | 20 | fits | 156,414 | 147 | 0.491 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 159,368 | 1.594 | 20 | 24 | fits | 153,286 | 208 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 932,693 | 9.327 | 20 | 24 | fits | 32,335 | 20 | 0.679 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 158,328 | 1.583 | 20 | 50 | fits | 153,286 | 208 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 899,903 | 8.999 | 20 | 50 | fits | 156,414 | 147 | 0.491 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 311,721 | 3.117 | 20 | 20 | fits | 153,848 | 87 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 576,707 | 5.767 | 20 | 20 | fits | 127,694 | 51 | 0.497 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 721,192 | 7.212 | 20 | 20 | fits | 160,336 | 175 | 0.548 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 159,562 | 1.596 | 20 | 200 | fits | 159,297 | 226 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 750,442 | 7.504 | 20 | 200 | fits | 160,336 | 175 | 0.548 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 160,474 | 1.605 | 20 | 20 | fits | 159,297 | 226 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 906,002 | 9.060 | 20 | 20 | fits | 154,864 | 132 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 164,059 | 1.641 | 20 | 24 | fits | 159,297 | 226 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 909,437 | 9.094 | 20 | 24 | fits | 154,864 | 132 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 163,019 | 1.630 | 20 | 50 | fits | 159,297 | 226 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 754,118 | 7.541 | 20 | 50 | fits | 160,336 | 175 | 0.548 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 316,404 | 3.164 | 20 | 20 | fits | 153,840 | 87 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 581,281 | 5.813 | 20 | 20 | fits | 120,150 | 46 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 273,221 | 2.732 | 20 | 20 | fits | 159,314 | 202 | 0.542 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 150,563 | 1.506 | 20 | 200 | fits | 151,618 | 223 | 0.490 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 309,268 | 3.093 | 20 | 200 | fits | 159,314 | 202 | 0.542 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 151,475 | 1.515 | 20 | 20 | fits | 151,618 | 223 | 0.490 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 884,224 | 8.842 | 20 | 20 | fits | 153,397 | 123 | 0.494 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 155,060 | 1.551 | 20 | 24 | fits | 151,618 | 223 | 0.490 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 931,950 | 9.319 | 20 | 24 | fits | 44,291 | 33 | 0.539 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 154,020 | 1.540 | 20 | 50 | fits | 151,618 | 223 | 0.490 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 312,944 | 3.129 | 20 | 50 | fits | 159,314 | 202 | 0.542 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 468,461 | 4.685 | 20 | 20 | fits | 155,582 | 50 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 731,727 | 7.317 | 20 | 20 | fits | 110,012 | 41 | 0.464 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 265,174 | 2.652 | 20 | 20 | fits | 161,491 | 211 | 0.514 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 153,389 | 1.534 | 20 | 200 | fits | 161,619 | 230 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 314,271 | 3.143 | 20 | 200 | fits | 161,491 | 211 | 0.514 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 154,301 | 1.543 | 20 | 20 | fits | 161,619 | 230 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 876,074 | 8.761 | 20 | 20 | fits | 157,401 | 135 | 0.457 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 157,886 | 1.579 | 20 | 24 | fits | 161,619 | 230 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 879,509 | 8.795 | 20 | 24 | fits | 157,401 | 135 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 156,846 | 1.568 | 20 | 50 | fits | 161,619 | 230 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 317,947 | 3.179 | 20 | 50 | fits | 161,491 | 211 | 0.514 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 472,586 | 4.726 | 20 | 20 | fits | 154,704 | 49 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 719,573 | 7.196 | 20 | 20 | fits | 109,800 | 41 | 0.458 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 724,619 | 7.246 | 20 | 20 | fits | 160,183 | 175 | 0.547 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 171,380 | 1.714 | 20 | 200 | fits | 159,255 | 226 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 753,795 | 7.538 | 20 | 200 | fits | 160,183 | 175 | 0.547 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 172,292 | 1.723 | 20 | 20 | fits | 159,255 | 226 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 910,832 | 9.108 | 20 | 20 | fits | 156,341 | 126 | 0.499 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 175,877 | 1.759 | 20 | 24 | fits | 159,255 | 226 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 946,602 | 9.466 | 20 | 24 | fits | 32,335 | 20 | 0.669 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 174,837 | 1.748 | 20 | 50 | fits | 159,255 | 226 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 757,471 | 7.575 | 20 | 50 | fits | 160,183 | 175 | 0.547 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 338,057 | 3.381 | 20 | 20 | fits | 163,675 | 91 | 0.599 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 585,086 | 5.851 | 20 | 20 | fits | 109,985 | 42 | 0.458 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 721,857 | 7.219 | 20 | 20 | fits | 166,290 | 175 | 0.527 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 169,920 | 1.699 | 20 | 200 | fits | 160,435 | 230 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 772,008 | 7.720 | 20 | 200 | fits | 166,290 | 175 | 0.527 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 170,832 | 1.708 | 20 | 20 | fits | 160,435 | 230 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 915,433 | 9.154 | 20 | 20 | fits | 142,729 | 125 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 174,417 | 1.744 | 20 | 24 | fits | 160,435 | 230 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 918,868 | 9.189 | 20 | 24 | fits | 142,729 | 125 | 0.450 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 173,377 | 1.734 | 20 | 50 | fits | 160,435 | 230 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 775,684 | 7.757 | 20 | 50 | fits | 166,290 | 175 | 0.527 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 326,730 | 3.267 | 20 | 20 | fits | 153,808 | 88 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 607,314 | 6.073 | 20 | 20 | fits | 127,869 | 51 | 0.503 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 745,087 | 7.451 | 20 | 20 | fits | 159,433 | 130 | 0.505 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 160,365 | 1.604 | 20 | 200 | fits | 153,506 | 209 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 894,105 | 8.941 | 20 | 200 | fits | 159,433 | 130 | 0.505 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 161,277 | 1.613 | 20 | 20 | fits | 153,506 | 209 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 894,801 | 8.948 | 20 | 20 | fits | 159,433 | 130 | 0.505 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 164,862 | 1.649 | 20 | 24 | fits | 153,506 | 209 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 931,075 | 9.311 | 20 | 24 | fits | 32,839 | 20 | 0.682 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 163,822 | 1.638 | 20 | 50 | fits | 153,506 | 209 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 328,434 | 3.284 | 20 | 50 | fits | 155,568 | 222 | 0.490 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 489,827 | 4.898 | 20 | 20 | fits | 161,458 | 55 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 736,268 | 7.363 | 20 | 20 | fits | 109,647 | 41 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 714,571 | 7.146 | 20 | 20 | fits | 154,403 | 171 | 0.537 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 173,131 | 1.731 | 20 | 200 | fits | 160,890 | 230 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 750,775 | 7.508 | 20 | 200 | fits | 154,403 | 171 | 0.537 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 174,043 | 1.740 | 20 | 20 | fits | 160,890 | 230 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 906,180 | 9.062 | 20 | 20 | fits | 154,709 | 134 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 177,628 | 1.776 | 20 | 24 | fits | 160,890 | 230 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 909,615 | 9.096 | 20 | 24 | fits | 154,709 | 134 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 176,588 | 1.766 | 20 | 50 | fits | 160,890 | 230 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 754,451 | 7.545 | 20 | 50 | fits | 154,403 | 171 | 0.537 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 329,936 | 3.299 | 20 | 20 | fits | 153,803 | 87 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 587,526 | 5.875 | 20 | 20 | fits | 120,279 | 46 | 0.433 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 696,730 | 6.967 | 20 | 20 | fits | 154,356 | 164 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 162,855 | 1.629 | 20 | 200 | fits | 153,170 | 208 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 746,336 | 7.463 | 20 | 200 | fits | 154,356 | 164 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 163,767 | 1.638 | 20 | 20 | fits | 153,170 | 208 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 900,505 | 9.005 | 20 | 20 | fits | 153,473 | 135 | 0.528 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 167,352 | 1.674 | 20 | 24 | fits | 153,170 | 208 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 948,330 | 9.483 | 20 | 24 | fits | 44,390 | 33 | 0.543 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 166,312 | 1.663 | 20 | 50 | fits | 153,170 | 208 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 903,485 | 9.035 | 20 | 50 | fits | 153,473 | 135 | 0.528 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 329,548 | 3.295 | 20 | 20 | fits | 163,691 | 91 | 0.602 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 593,576 | 5.936 | 20 | 20 | fits | 112,154 | 41 | 0.516 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 280,901 | 2.809 | 20 | 20 | fits | 161,417 | 212 | 0.513 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 158,555 | 1.586 | 20 | 200 | fits | 151,510 | 224 | 0.488 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 328,946 | 3.289 | 20 | 200 | fits | 161,417 | 212 | 0.513 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 159,467 | 1.595 | 20 | 20 | fits | 151,510 | 224 | 0.488 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 894,610 | 8.946 | 20 | 20 | fits | 153,507 | 124 | 0.492 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 163,052 | 1.631 | 20 | 24 | fits | 151,510 | 224 | 0.488 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 944,221 | 9.442 | 20 | 24 | fits | 36,246 | 26 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 162,012 | 1.620 | 20 | 50 | fits | 151,510 | 224 | 0.488 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 332,622 | 3.326 | 20 | 50 | fits | 161,417 | 212 | 0.513 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 487,238 | 4.872 | 20 | 20 | fits | 154,681 | 49 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 742,003 | 7.420 | 20 | 20 | fits | 109,528 | 41 | 0.450 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 280,984 | 2.810 | 20 | 20 | fits | 161,120 | 201 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 157,052 | 1.571 | 20 | 200 | fits | 161,356 | 230 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 317,563 | 3.176 | 20 | 200 | fits | 161,120 | 201 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 157,964 | 1.580 | 20 | 20 | fits | 161,356 | 230 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 893,145 | 8.931 | 20 | 20 | fits | 160,267 | 139 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 161,549 | 1.615 | 20 | 24 | fits | 161,356 | 230 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 929,301 | 9.293 | 20 | 24 | fits | 32,721 | 20 | 0.684 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 160,509 | 1.605 | 20 | 50 | fits | 161,356 | 230 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 321,239 | 3.212 | 20 | 50 | fits | 161,120 | 201 | 0.554 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 476,080 | 4.761 | 20 | 20 | fits | 154,906 | 49 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 723,177 | 7.232 | 20 | 20 | fits | 109,960 | 42 | 0.460 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 801,509 | 8.015 | 20 | 20 | fits | 160,046 | 130 | 0.515 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 175,727 | 1.757 | 20 | 200 | fits | 159,260 | 226 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 910,129 | 9.101 | 20 | 200 | fits | 160,046 | 130 | 0.515 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 176,639 | 1.766 | 20 | 20 | fits | 159,260 | 226 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 910,825 | 9.108 | 20 | 20 | fits | 160,046 | 130 | 0.515 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 180,224 | 1.802 | 20 | 24 | fits | 159,260 | 226 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 914,260 | 9.143 | 20 | 24 | fits | 160,046 | 130 | 0.515 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 179,184 | 1.792 | 20 | 50 | fits | 159,260 | 226 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 339,717 | 3.397 | 20 | 50 | fits | 160,923 | 216 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 504,598 | 5.046 | 20 | 20 | fits | 155,144 | 49 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 751,679 | 7.517 | 20 | 20 | fits | 109,950 | 41 | 0.462 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 778,929 | 7.789 | 20 | 20 | fits | 159,399 | 130 | 0.508 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 154,176 | 1.542 | 20 | 200 | fits | 159,209 | 227 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 887,367 | 8.874 | 20 | 200 | fits | 159,399 | 130 | 0.508 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 155,088 | 1.551 | 20 | 20 | fits | 159,209 | 227 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 888,063 | 8.881 | 20 | 20 | fits | 159,399 | 130 | 0.508 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 158,673 | 1.587 | 20 | 24 | fits | 159,209 | 227 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 891,498 | 8.915 | 20 | 24 | fits | 159,399 | 130 | 0.508 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 157,633 | 1.576 | 20 | 50 | fits | 159,209 | 227 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 328,541 | 3.285 | 20 | 50 | fits | 161,618 | 215 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 483,232 | 4.832 | 20 | 20 | fits | 154,756 | 49 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 729,564 | 7.296 | 20 | 20 | fits | 109,647 | 41 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 696,867 | 6.969 | 20 | 20 | fits | 153,598 | 165 | 0.546 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 157,186 | 1.572 | 20 | 200 | fits | 151,652 | 223 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 723,980 | 7.240 | 20 | 200 | fits | 153,598 | 165 | 0.546 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 158,098 | 1.581 | 20 | 20 | fits | 151,652 | 223 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 878,829 | 8.788 | 20 | 20 | fits | 154,153 | 125 | 0.531 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 161,683 | 1.617 | 20 | 24 | fits | 151,652 | 223 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 937,111 | 9.371 | 20 | 24 | fits | 44,846 | 33 | 0.560 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 160,643 | 1.606 | 20 | 50 | fits | 151,652 | 223 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 727,656 | 7.277 | 20 | 50 | fits | 153,598 | 165 | 0.546 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 314,372 | 3.144 | 20 | 20 | fits | 154,184 | 87 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 571,978 | 5.720 | 20 | 20 | fits | 120,263 | 45 | 0.434 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 709,263 | 7.093 | 20 | 20 | fits | 158,481 | 165 | 0.579 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 165,473 | 1.655 | 20 | 200 | fits | 161,259 | 230 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 736,828 | 7.368 | 20 | 200 | fits | 158,481 | 165 | 0.579 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 166,385 | 1.664 | 20 | 20 | fits | 161,259 | 230 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 903,419 | 9.034 | 20 | 20 | fits | 155,466 | 132 | 0.491 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 169,970 | 1.700 | 20 | 24 | fits | 161,259 | 230 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 939,388 | 9.394 | 20 | 24 | fits | 32,534 | 20 | 0.680 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 168,930 | 1.689 | 20 | 50 | fits | 161,259 | 230 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 740,504 | 7.405 | 20 | 50 | fits | 158,481 | 165 | 0.579 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 322,446 | 3.224 | 20 | 20 | fits | 153,971 | 87 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 579,943 | 5.799 | 20 | 20 | fits | 120,186 | 45 | 0.432 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 703,559 | 7.036 | 20 | 20 | fits | 165,613 | 192 | 0.545 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 156,248 | 1.562 | 20 | 200 | fits | 153,354 | 208 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 752,927 | 7.529 | 20 | 200 | fits | 165,613 | 192 | 0.545 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 157,160 | 1.572 | 20 | 20 | fits | 153,354 | 208 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 907,873 | 9.079 | 20 | 20 | fits | 154,250 | 133 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 160,745 | 1.607 | 20 | 24 | fits | 153,354 | 208 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 911,308 | 9.113 | 20 | 24 | fits | 154,250 | 133 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 159,705 | 1.597 | 20 | 50 | fits | 153,354 | 208 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 756,603 | 7.566 | 20 | 50 | fits | 165,613 | 192 | 0.545 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 313,349 | 3.133 | 20 | 20 | fits | 154,099 | 87 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 578,489 | 5.785 | 20 | 20 | fits | 127,787 | 52 | 0.497 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 695,636 | 6.956 | 20 | 20 | fits | 153,906 | 164 | 0.548 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 154,928 | 1.549 | 20 | 200 | fits | 153,340 | 208 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 745,121 | 7.451 | 20 | 200 | fits | 153,906 | 164 | 0.548 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 155,840 | 1.558 | 20 | 20 | fits | 153,340 | 208 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 897,950 | 8.979 | 20 | 20 | fits | 152,133 | 141 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 159,425 | 1.594 | 20 | 24 | fits | 153,340 | 208 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 933,585 | 9.336 | 20 | 24 | fits | 32,200 | 20 | 0.673 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 158,385 | 1.584 | 20 | 50 | fits | 153,340 | 208 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 900,930 | 9.009 | 20 | 50 | fits | 152,133 | 141 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 312,029 | 3.120 | 20 | 20 | fits | 154,099 | 87 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 592,811 | 5.928 | 20 | 20 | fits | 125,415 | 51 | 0.521 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 787,752 | 7.878 | 20 | 20 | fits | 159,890 | 129 | 0.514 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 159,619 | 1.596 | 20 | 200 | fits | 159,351 | 226 | 0.506 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 896,299 | 8.963 | 20 | 200 | fits | 159,890 | 129 | 0.514 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 160,531 | 1.605 | 20 | 20 | fits | 159,351 | 226 | 0.506 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 896,995 | 8.970 | 20 | 20 | fits | 159,890 | 129 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 164,116 | 1.641 | 20 | 24 | fits | 159,351 | 226 | 0.506 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 933,631 | 9.336 | 20 | 24 | fits | 33,201 | 20 | 0.688 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 163,076 | 1.631 | 20 | 50 | fits | 159,351 | 226 | 0.506 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 321,914 | 3.219 | 20 | 50 | fits | 159,228 | 206 | 0.517 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 490,697 | 4.907 | 20 | 20 | fits | 158,781 | 55 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 738,005 | 7.380 | 20 | 20 | fits | 109,892 | 41 | 0.458 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 284,450 | 2.845 | 20 | 20 | fits | 161,209 | 202 | 0.552 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 150,736 | 1.507 | 20 | 200 | fits | 151,788 | 224 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 320,751 | 3.208 | 20 | 200 | fits | 161,209 | 202 | 0.552 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 151,648 | 1.516 | 20 | 20 | fits | 151,788 | 224 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 882,487 | 8.825 | 20 | 20 | fits | 153,532 | 123 | 0.494 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 155,233 | 1.552 | 20 | 24 | fits | 151,788 | 224 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 930,206 | 9.302 | 20 | 24 | fits | 44,284 | 34 | 0.536 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 154,193 | 1.542 | 20 | 50 | fits | 151,788 | 224 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 324,427 | 3.244 | 20 | 50 | fits | 161,209 | 202 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 482,997 | 4.830 | 20 | 20 | fits | 158,635 | 55 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 729,855 | 7.299 | 20 | 20 | fits | 109,739 | 41 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 272,857 | 2.729 | 20 | 20 | fits | 161,707 | 211 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 151,431 | 1.514 | 20 | 200 | fits | 153,059 | 203 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 322,153 | 3.222 | 20 | 200 | fits | 161,707 | 211 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 152,343 | 1.523 | 20 | 20 | fits | 153,059 | 203 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 882,254 | 8.823 | 20 | 20 | fits | 155,409 | 141 | 0.489 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 155,928 | 1.559 | 20 | 24 | fits | 153,059 | 203 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 917,546 | 9.175 | 20 | 24 | fits | 31,857 | 20 | 0.660 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 154,888 | 1.549 | 20 | 50 | fits | 153,059 | 203 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 885,234 | 8.852 | 20 | 50 | fits | 155,409 | 141 | 0.489 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 481,010 | 4.810 | 20 | 20 | fits | 155,246 | 49 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 727,745 | 7.277 | 20 | 20 | fits | 109,724 | 41 | 0.456 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 255,203 | 2.552 | 20 | 20 | fits | 161,272 | 211 | 0.516 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 143,799 | 1.438 | 20 | 200 | fits | 152,231 | 202 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 304,462 | 3.045 | 20 | 200 | fits | 161,272 | 211 | 0.516 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 144,711 | 1.447 | 20 | 20 | fits | 152,231 | 202 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 868,777 | 8.688 | 20 | 20 | fits | 159,473 | 148 | 0.500 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 148,296 | 1.483 | 20 | 24 | fits | 152,231 | 202 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 925,653 | 9.257 | 20 | 24 | fits | 43,761 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 147,256 | 1.473 | 20 | 50 | fits | 152,231 | 202 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 871,757 | 8.718 | 20 | 50 | fits | 159,473 | 148 | 0.500 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 463,217 | 4.632 | 20 | 20 | fits | 155,144 | 49 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 710,204 | 7.102 | 20 | 20 | fits | 109,800 | 41 | 0.458 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 733,100 | 7.331 | 20 | 20 | fits | 158,080 | 124 | 0.554 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 143,724 | 1.437 | 20 | 200 | fits | 152,217 | 202 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 874,357 | 8.744 | 20 | 200 | fits | 158,080 | 124 | 0.554 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 144,636 | 1.446 | 20 | 20 | fits | 152,217 | 202 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 875,053 | 8.751 | 20 | 20 | fits | 158,080 | 124 | 0.554 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 148,221 | 1.482 | 20 | 24 | fits | 152,217 | 202 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 1,001,262 | 10.013 | 20 | 24 | fits | 45,291 | 33 | 0.567 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 147,181 | 1.472 | 20 | 50 | fits | 152,217 | 202 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 301,597 | 3.016 | 20 | 50 | fits | 154,806 | 222 | 0.478 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 455,956 | 4.560 | 20 | 20 | fits | 154,424 | 49 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 707,519 | 7.075 | 20 | 20 | fits | 114,593 | 48 | 0.511 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 273,409 | 2.734 | 20 | 20 | fits | 159,108 | 212 | 0.497 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 150,446 | 1.504 | 20 | 200 | fits | 159,014 | 187 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 308,945 | 3.089 | 20 | 200 | fits | 159,108 | 212 | 0.497 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 151,358 | 1.514 | 20 | 20 | fits | 159,014 | 187 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 980,360 | 9.804 | 20 | 20 | fits | 153,795 | 125 | 0.494 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 154,943 | 1.549 | 20 | 24 | fits | 159,014 | 187 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 983,795 | 9.838 | 20 | 24 | fits | 153,795 | 125 | 0.494 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 153,903 | 1.539 | 20 | 50 | fits | 159,014 | 187 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 312,621 | 3.126 | 20 | 50 | fits | 159,108 | 212 | 0.497 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 467,367 | 4.674 | 20 | 20 | fits | 154,811 | 87 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 750,227 | 7.502 | 20 | 20 | fits | 130,297 | 51 | 0.545 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 254,578 | 2.546 | 20 | 20 | fits | 159,861 | 212 | 0.503 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 143,170 | 1.432 | 20 | 200 | fits | 151,813 | 183 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 302,422 | 3.024 | 20 | 200 | fits | 159,861 | 212 | 0.503 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 144,082 | 1.441 | 20 | 20 | fits | 151,813 | 183 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 974,270 | 9.743 | 20 | 20 | fits | 156,992 | 131 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 147,667 | 1.477 | 20 | 24 | fits | 151,813 | 183 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 977,705 | 9.777 | 20 | 24 | fits | 156,992 | 131 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 146,627 | 1.466 | 20 | 50 | fits | 151,813 | 183 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 306,098 | 3.061 | 20 | 50 | fits | 159,861 | 212 | 0.503 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 460,516 | 4.605 | 20 | 20 | fits | 154,483 | 88 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 818,178 | 8.182 | 20 | 20 | fits | 120,909 | 45 | 0.459 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 328,244 | 3.282 | 20 | 20 | fits | 163,097 | 170 | 0.512 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 142,523 | 1.425 | 20 | 200 | fits | 151,241 | 163 | 0.540 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 471,451 | 4.715 | 20 | 200 | fits | 163,097 | 170 | 0.512 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 143,435 | 1.434 | 20 | 20 | fits | 151,241 | 163 | 0.540 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 472,147 | 4.721 | 20 | 20 | fits | 163,097 | 170 | 0.512 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 147,020 | 1.470 | 20 | 24 | fits | 151,241 | 163 | 0.540 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 999,946 | 9.999 | 20 | 24 | fits | 35,441 | 20 | 0.734 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 145,980 | 1.460 | 20 | 50 | fits | 151,241 | 163 | 0.540 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 302,429 | 3.024 | 20 | 50 | fits | 156,839 | 227 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 637,782 | 6.378 | 20 | 20 | fits | 162,720 | 55 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 961,970 | 9.620 | 20 | 20 | fits | 109,724 | 41 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 295,198 | 2.952 | 20 | 20 | fits | 165,598 | 216 | 0.517 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 149,611 | 1.496 | 20 | 200 | fits | 158,404 | 185 | 0.523 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 323,981 | 3.240 | 20 | 200 | fits | 165,598 | 216 | 0.517 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 150,523 | 1.505 | 20 | 20 | fits | 158,404 | 185 | 0.523 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 475,455 | 4.755 | 20 | 20 | fits | 150,778 | 160 | 0.487 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 154,108 | 1.541 | 20 | 24 | fits | 158,404 | 185 | 0.523 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 1,015,851 | 10.159 | 20 | 24 | fits | 38,220 | 26 | 0.746 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 153,068 | 1.531 | 20 | 50 | fits | 158,404 | 185 | 0.523 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 327,657 | 3.277 | 20 | 50 | fits | 165,598 | 216 | 0.517 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 640,187 | 6.402 | 20 | 20 | fits | 161,817 | 55 | 0.645 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 964,612 | 9.646 | 20 | 20 | fits | 109,818 | 42 | 0.450 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 817,432 | 8.174 | 20 | 20 | fits | 159,512 | 145 | 0.541 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 156,783 | 1.568 | 20 | 200 | fits | 152,412 | 202 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 964,046 | 9.640 | 20 | 200 | fits | 159,512 | 145 | 0.541 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 157,695 | 1.577 | 20 | 20 | fits | 152,412 | 202 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 964,742 | 9.647 | 20 | 20 | fits | 159,512 | 145 | 0.541 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 161,280 | 1.613 | 20 | 24 | fits | 152,412 | 202 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 1,013,073 | 10.131 | 20 | 24 | fits | 44,896 | 33 | 0.552 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 160,240 | 1.602 | 20 | 50 | fits | 152,412 | 202 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 967,722 | 9.677 | 20 | 50 | fits | 159,512 | 145 | 0.541 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 549,109 | 5.491 | 20 | 20 | fits | 154,008 | 49 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 795,929 | 7.959 | 20 | 20 | fits | 109,843 | 42 | 0.458 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 715,962 | 7.160 | 20 | 20 | fits | 163,706 | 172 | 0.538 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 160,535 | 1.605 | 20 | 200 | fits | 159,378 | 224 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 753,682 | 7.537 | 20 | 200 | fits | 163,706 | 172 | 0.538 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 161,447 | 1.614 | 20 | 20 | fits | 159,378 | 224 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 901,844 | 9.018 | 20 | 20 | fits | 147,466 | 132 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 165,032 | 1.650 | 20 | 24 | fits | 159,378 | 224 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if1` | 905,279 | 9.053 | 20 | 24 | fits | 147,466 | 132 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 163,992 | 1.640 | 20 | 50 | fits | 159,378 | 224 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 757,358 | 7.574 | 20 | 50 | fits | 163,706 | 172 | 0.538 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 317,859 | 3.179 | 20 | 20 | fits | 154,322 | 88 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if1` | 591,572 | 5.916 | 20 | 20 | fits | 120,463 | 45 | 0.442 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 283,442 | 2.834 | 20 | 20 | fits | 162,215 | 211 | 0.526 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 161,485 | 1.615 | 20 | 200 | fits | 160,403 | 225 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 332,684 | 3.327 | 20 | 200 | fits | 162,215 | 211 | 0.526 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 162,397 | 1.624 | 20 | 20 | fits | 160,403 | 225 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 894,575 | 8.946 | 20 | 20 | fits | 157,301 | 134 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 165,982 | 1.660 | 20 | 24 | fits | 160,403 | 225 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if1` | 898,010 | 8.980 | 20 | 24 | fits | 157,301 | 134 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 164,942 | 1.649 | 20 | 50 | fits | 160,403 | 225 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 336,360 | 3.364 | 20 | 50 | fits | 162,215 | 211 | 0.526 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 491,439 | 4.914 | 20 | 20 | fits | 155,144 | 49 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if1` | 738,174 | 7.382 | 20 | 20 | fits | 109,724 | 41 | 0.456 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 690,825 | 6.908 | 20 | 20 | fits | 162,485 | 186 | 0.536 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 164,620 | 1.646 | 20 | 200 | fits | 152,594 | 203 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 740,029 | 7.400 | 20 | 200 | fits | 162,485 | 186 | 0.536 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 165,532 | 1.655 | 20 | 20 | fits | 152,594 | 203 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 896,290 | 8.963 | 20 | 20 | fits | 155,565 | 128 | 0.496 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 169,117 | 1.691 | 20 | 24 | fits | 152,594 | 203 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if1` | 945,721 | 9.457 | 20 | 24 | fits | 36,134 | 26 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 168,077 | 1.681 | 20 | 50 | fits | 152,594 | 203 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 743,705 | 7.437 | 20 | 50 | fits | 162,485 | 186 | 0.536 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 321,649 | 3.216 | 20 | 20 | fits | 154,027 | 87 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if1` | 579,140 | 5.791 | 20 | 20 | fits | 120,231 | 45 | 0.432 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 257,538 | 2.575 | 20 | 20 | fits | 161,560 | 211 | 0.518 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 145,887 | 1.459 | 20 | 200 | fits | 152,665 | 202 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 306,838 | 3.068 | 20 | 200 | fits | 161,560 | 211 | 0.518 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 146,799 | 1.468 | 20 | 20 | fits | 152,665 | 202 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 888,598 | 8.886 | 20 | 20 | fits | 158,281 | 147 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 150,384 | 1.504 | 20 | 24 | fits | 152,665 | 202 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if1` | 924,283 | 9.243 | 20 | 24 | fits | 32,250 | 20 | 0.675 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 149,344 | 1.493 | 20 | 50 | fits | 152,665 | 202 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 891,578 | 8.916 | 20 | 50 | fits | 158,281 | 147 | 0.504 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 465,593 | 4.656 | 20 | 20 | fits | 155,144 | 49 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if1` | 720,782 | 7.208 | 20 | 20 | fits | 118,025 | 48 | 0.533 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 737,861 | 7.379 | 20 | 20 | fits | 159,358 | 130 | 0.507 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 145,873 | 1.459 | 20 | 200 | fits | 152,651 | 202 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 886,600 | 8.866 | 20 | 200 | fits | 159,358 | 130 | 0.507 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 146,785 | 1.468 | 20 | 20 | fits | 152,651 | 202 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 887,296 | 8.873 | 20 | 20 | fits | 159,358 | 130 | 0.507 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 150,370 | 1.504 | 20 | 24 | fits | 152,651 | 202 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if1` | 923,847 | 9.238 | 20 | 24 | fits | 33,116 | 20 | 0.688 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 149,330 | 1.493 | 20 | 50 | fits | 152,651 | 202 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 304,034 | 3.040 | 20 | 50 | fits | 155,094 | 222 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 458,393 | 4.584 | 20 | 20 | fits | 154,424 | 49 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if1` | 728,838 | 7.288 | 20 | 20 | fits | 115,103 | 47 | 0.546 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 789,499 | 7.895 | 20 | 20 | fits | 159,326 | 130 | 0.511 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 151,805 | 1.518 | 20 | 200 | fits | 158,583 | 220 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 897,807 | 8.978 | 20 | 200 | fits | 159,326 | 130 | 0.511 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 152,717 | 1.527 | 20 | 20 | fits | 158,583 | 220 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 898,503 | 8.985 | 20 | 20 | fits | 159,326 | 130 | 0.511 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 156,302 | 1.563 | 20 | 24 | fits | 158,583 | 220 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if1` | 901,938 | 9.019 | 20 | 24 | fits | 159,326 | 130 | 0.511 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 155,262 | 1.553 | 20 | 50 | fits | 158,583 | 220 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 315,673 | 3.157 | 20 | 50 | fits | 160,801 | 215 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 477,725 | 4.777 | 20 | 20 | fits | 162,117 | 56 | 0.649 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if1` | 740,077 | 7.401 | 20 | 20 | fits | 109,868 | 41 | 0.460 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 263,959 | 2.640 | 20 | 20 | fits | 160,198 | 213 | 0.504 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 152,370 | 1.524 | 20 | 200 | fits | 159,148 | 224 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 311,959 | 3.120 | 20 | 200 | fits | 160,198 | 213 | 0.504 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 153,282 | 1.533 | 20 | 20 | fits | 159,148 | 224 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 892,460 | 8.925 | 20 | 20 | fits | 157,069 | 131 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 156,867 | 1.569 | 20 | 24 | fits | 159,148 | 224 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if1` | 895,895 | 8.959 | 20 | 24 | fits | 157,069 | 131 | 0.462 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 155,827 | 1.558 | 20 | 50 | fits | 159,148 | 224 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 315,635 | 3.156 | 20 | 50 | fits | 160,198 | 213 | 0.504 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 489,396 | 4.894 | 20 | 20 | fits | 164,117 | 61 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if1` | 736,291 | 7.363 | 20 | 20 | fits | 109,801 | 41 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 265,358 | 2.654 | 20 | 20 | fits | 162,051 | 212 | 0.518 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 153,101 | 1.531 | 20 | 200 | fits | 159,879 | 224 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 314,543 | 3.145 | 20 | 200 | fits | 162,051 | 212 | 0.518 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 154,013 | 1.540 | 20 | 20 | fits | 159,879 | 224 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 896,361 | 8.964 | 20 | 20 | fits | 157,639 | 134 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 157,598 | 1.576 | 20 | 24 | fits | 159,879 | 224 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if1` | 899,796 | 8.998 | 20 | 24 | fits | 157,639 | 134 | 0.462 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 156,558 | 1.566 | 20 | 50 | fits | 159,879 | 224 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 318,219 | 3.182 | 20 | 50 | fits | 162,051 | 212 | 0.518 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 482,083 | 4.821 | 20 | 20 | fits | 154,232 | 57 | 0.668 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if1` | 739,622 | 7.396 | 20 | 20 | fits | 120,162 | 45 | 0.431 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 720,339 | 7.203 | 20 | 20 | fits | 157,519 | 169 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 163,480 | 1.635 | 20 | 200 | fits | 158,651 | 220 | 0.504 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 749,324 | 7.493 | 20 | 200 | fits | 157,519 | 169 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 164,392 | 1.644 | 20 | 20 | fits | 158,651 | 220 | 0.504 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 904,810 | 9.048 | 20 | 20 | fits | 154,790 | 132 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 167,977 | 1.680 | 20 | 24 | fits | 158,651 | 220 | 0.504 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 908,245 | 9.082 | 20 | 24 | fits | 154,790 | 132 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 166,937 | 1.669 | 20 | 50 | fits | 158,651 | 220 | 0.504 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 753,000 | 7.530 | 20 | 50 | fits | 157,519 | 169 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 319,943 | 3.199 | 20 | 20 | fits | 153,461 | 87 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if1` | 593,401 | 5.934 | 20 | 20 | fits | 125,730 | 51 | 0.528 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 720,372 | 7.204 | 20 | 20 | fits | 163,677 | 172 | 0.538 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 164,001 | 1.640 | 20 | 200 | fits | 159,247 | 224 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 758,035 | 7.580 | 20 | 200 | fits | 163,677 | 172 | 0.538 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 164,913 | 1.649 | 20 | 20 | fits | 159,247 | 224 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 906,331 | 9.063 | 20 | 20 | fits | 147,600 | 132 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 168,498 | 1.685 | 20 | 24 | fits | 159,247 | 224 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 909,766 | 9.098 | 20 | 24 | fits | 147,600 | 132 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 167,458 | 1.675 | 20 | 50 | fits | 159,247 | 224 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 761,711 | 7.617 | 20 | 50 | fits | 163,677 | 172 | 0.538 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 320,786 | 3.208 | 20 | 20 | fits | 153,783 | 87 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if1` | 595,954 | 5.960 | 20 | 20 | fits | 122,521 | 45 | 0.492 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 708,725 | 7.087 | 20 | 20 | fits | 165,779 | 175 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 164,571 | 1.646 | 20 | 200 | fits | 159,892 | 224 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 758,792 | 7.588 | 20 | 200 | fits | 165,779 | 175 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 165,483 | 1.655 | 20 | 20 | fits | 159,892 | 224 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 914,484 | 9.145 | 20 | 20 | fits | 154,996 | 129 | 0.494 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 169,068 | 1.691 | 20 | 24 | fits | 159,892 | 224 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 917,919 | 9.179 | 20 | 24 | fits | 154,996 | 129 | 0.494 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 168,028 | 1.680 | 20 | 50 | fits | 159,892 | 224 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 762,468 | 7.625 | 20 | 50 | fits | 165,779 | 175 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 321,311 | 3.213 | 20 | 20 | fits | 153,738 | 88 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if1` | 594,609 | 5.946 | 20 | 20 | fits | 120,379 | 45 | 0.442 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 278,678 | 2.787 | 20 | 20 | fits | 161,547 | 211 | 0.523 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 157,412 | 1.574 | 20 | 200 | fits | 152,808 | 203 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 327,974 | 3.280 | 20 | 200 | fits | 161,547 | 211 | 0.523 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 158,324 | 1.583 | 20 | 20 | fits | 152,808 | 203 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 977,127 | 9.771 | 20 | 20 | fits | 155,856 | 142 | 0.492 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 161,909 | 1.619 | 20 | 24 | fits | 152,808 | 203 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 1,026,650 | 10.267 | 20 | 24 | fits | 36,302 | 26 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 160,869 | 1.609 | 20 | 50 | fits | 152,808 | 203 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 980,107 | 9.801 | 20 | 50 | fits | 155,856 | 142 | 0.492 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 486,345 | 4.863 | 20 | 20 | fits | 154,760 | 49 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if1` | 741,221 | 7.412 | 20 | 20 | fits | 117,842 | 47 | 0.531 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 763,486 | 7.635 | 20 | 20 | fits | 162,340 | 187 | 0.534 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 149,924 | 1.499 | 20 | 200 | fits | 152,271 | 202 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 812,803 | 8.128 | 20 | 200 | fits | 162,340 | 187 | 0.534 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 150,836 | 1.508 | 20 | 20 | fits | 152,271 | 202 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 982,404 | 9.824 | 20 | 20 | fits | 158,714 | 139 | 0.465 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 154,421 | 1.544 | 20 | 24 | fits | 152,271 | 202 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 985,839 | 9.858 | 20 | 24 | fits | 158,714 | 139 | 0.465 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 153,381 | 1.534 | 20 | 50 | fits | 152,271 | 202 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 816,479 | 8.165 | 20 | 50 | fits | 162,340 | 187 | 0.534 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 316,539 | 3.165 | 20 | 20 | fits | 163,613 | 91 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if1` | 571,017 | 5.710 | 20 | 20 | fits | 117,382 | 47 | 0.521 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 768,593 | 7.686 | 20 | 20 | fits | 157,109 | 170 | 0.559 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 149,933 | 1.499 | 20 | 200 | fits | 152,257 | 202 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 818,470 | 8.185 | 20 | 200 | fits | 157,109 | 170 | 0.559 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 150,845 | 1.508 | 20 | 20 | fits | 152,257 | 202 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 971,206 | 9.712 | 20 | 20 | fits | 152,040 | 141 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 154,430 | 1.544 | 20 | 24 | fits | 152,257 | 202 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 1,006,966 | 10.070 | 20 | 24 | fits | 32,325 | 20 | 0.675 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 153,390 | 1.534 | 20 | 50 | fits | 152,257 | 202 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 974,186 | 9.742 | 20 | 50 | fits | 152,040 | 141 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 316,548 | 3.165 | 20 | 20 | fits | 163,613 | 91 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if1` | 652,412 | 6.524 | 20 | 20 | fits | 110,149 | 42 | 0.475 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 800,449 | 8.004 | 20 | 20 | fits | 157,797 | 169 | 0.542 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 155,845 | 1.558 | 20 | 200 | fits | 158,244 | 220 | 0.502 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 829,493 | 8.295 | 20 | 200 | fits | 157,797 | 169 | 0.542 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 156,757 | 1.568 | 20 | 20 | fits | 158,244 | 220 | 0.502 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 985,770 | 9.858 | 20 | 20 | fits | 155,581 | 132 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 160,342 | 1.603 | 20 | 24 | fits | 158,244 | 220 | 0.502 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 989,205 | 9.892 | 20 | 24 | fits | 155,581 | 132 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 159,302 | 1.593 | 20 | 50 | fits | 158,244 | 220 | 0.502 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 833,169 | 8.332 | 20 | 50 | fits | 157,797 | 169 | 0.542 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 322,452 | 3.225 | 20 | 20 | fits | 163,605 | 91 | 0.598 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if1` | 662,985 | 6.630 | 20 | 20 | fits | 114,901 | 48 | 0.524 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 279,181 | 2.792 | 20 | 20 | fits | 159,390 | 202 | 0.541 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 156,425 | 1.564 | 20 | 200 | fits | 158,899 | 224 | 0.492 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 315,206 | 3.152 | 20 | 200 | fits | 159,390 | 202 | 0.541 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 157,337 | 1.573 | 20 | 20 | fits | 158,899 | 224 | 0.492 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 974,699 | 9.747 | 20 | 20 | fits | 157,105 | 130 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 160,922 | 1.609 | 20 | 24 | fits | 158,899 | 224 | 0.492 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 1,010,148 | 10.101 | 20 | 24 | fits | 32,014 | 20 | 0.667 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 159,882 | 1.599 | 20 | 50 | fits | 158,899 | 224 | 0.492 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 318,882 | 3.189 | 20 | 50 | fits | 159,390 | 202 | 0.541 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 558,263 | 5.583 | 20 | 20 | fits | 158,460 | 56 | 0.639 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if1` | 818,494 | 8.185 | 20 | 20 | fits | 110,247 | 41 | 0.468 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 685,207 | 6.852 | 20 | 20 | fits | 162,057 | 187 | 0.533 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 160,149 | 1.601 | 20 | 200 | fits | 151,905 | 202 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 734,213 | 7.342 | 20 | 200 | fits | 162,057 | 187 | 0.533 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 161,061 | 1.611 | 20 | 20 | fits | 151,905 | 202 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 903,846 | 9.038 | 20 | 20 | fits | 158,907 | 139 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 164,646 | 1.646 | 20 | 24 | fits | 151,905 | 202 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if1` | 907,281 | 9.073 | 20 | 24 | fits | 158,907 | 139 | 0.466 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 163,606 | 1.636 | 20 | 50 | fits | 151,905 | 202 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 737,889 | 7.379 | 20 | 50 | fits | 162,057 | 187 | 0.533 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 326,764 | 3.268 | 20 | 20 | fits | 163,613 | 91 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if1` | 573,752 | 5.738 | 20 | 20 | fits | 109,892 | 41 | 0.458 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 689,392 | 6.894 | 20 | 20 | fits | 156,764 | 170 | 0.558 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 160,074 | 1.601 | 20 | 200 | fits | 151,891 | 202 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 739,264 | 7.393 | 20 | 200 | fits | 156,764 | 170 | 0.558 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 160,986 | 1.610 | 20 | 20 | fits | 151,891 | 202 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 892,284 | 8.923 | 20 | 20 | fits | 152,324 | 141 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 164,571 | 1.646 | 20 | 24 | fits | 151,891 | 202 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if1` | 938,800 | 9.388 | 20 | 24 | fits | 43,081 | 29 | 0.694 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 163,531 | 1.635 | 20 | 50 | fits | 151,891 | 202 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 895,264 | 8.953 | 20 | 50 | fits | 152,324 | 141 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 326,689 | 3.267 | 20 | 20 | fits | 163,613 | 91 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if1` | 573,770 | 5.738 | 20 | 20 | fits | 109,985 | 42 | 0.458 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 722,930 | 7.229 | 20 | 20 | fits | 157,581 | 169 | 0.539 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 165,986 | 1.660 | 20 | 200 | fits | 157,878 | 220 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 751,915 | 7.519 | 20 | 200 | fits | 157,581 | 169 | 0.539 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 166,898 | 1.669 | 20 | 20 | fits | 157,878 | 220 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 908,705 | 9.087 | 20 | 20 | fits | 156,094 | 126 | 0.497 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 170,483 | 1.705 | 20 | 24 | fits | 157,878 | 220 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if1` | 944,615 | 9.446 | 20 | 24 | fits | 32,475 | 20 | 0.671 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 169,443 | 1.694 | 20 | 50 | fits | 157,878 | 220 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 755,591 | 7.556 | 20 | 50 | fits | 157,581 | 169 | 0.539 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 322,449 | 3.224 | 20 | 20 | fits | 153,461 | 87 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if1` | 595,930 | 5.959 | 20 | 20 | fits | 125,730 | 51 | 0.528 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 781,012 | 7.810 | 20 | 20 | fits | 156,091 | 128 | 0.489 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 166,695 | 1.667 | 20 | 200 | fits | 158,662 | 224 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 905,600 | 9.056 | 20 | 200 | fits | 156,091 | 128 | 0.489 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 167,607 | 1.676 | 20 | 20 | fits | 158,662 | 224 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 906,296 | 9.063 | 20 | 20 | fits | 156,091 | 128 | 0.489 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 171,192 | 1.712 | 20 | 24 | fits | 158,662 | 224 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if1` | 942,321 | 9.423 | 20 | 24 | fits | 32,590 | 20 | 0.679 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 170,152 | 1.702 | 20 | 50 | fits | 158,662 | 224 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 753,185 | 7.532 | 20 | 50 | fits | 153,969 | 159 | 0.569 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 323,573 | 3.236 | 20 | 20 | fits | 153,876 | 88 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if1` | 597,136 | 5.971 | 20 | 20 | fits | 120,463 | 45 | 0.442 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 289,786 | 2.898 | 20 | 20 | fits | 162,425 | 211 | 0.527 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 167,756 | 1.678 | 20 | 200 | fits | 159,798 | 225 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 339,165 | 3.392 | 20 | 200 | fits | 162,425 | 211 | 0.527 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 168,668 | 1.687 | 20 | 20 | fits | 159,798 | 225 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 909,272 | 9.093 | 20 | 20 | fits | 157,956 | 134 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 172,253 | 1.723 | 20 | 24 | fits | 159,798 | 225 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if1` | 912,707 | 9.127 | 20 | 24 | fits | 157,956 | 134 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 171,213 | 1.712 | 20 | 50 | fits | 159,798 | 225 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 342,841 | 3.428 | 20 | 50 | fits | 162,425 | 211 | 0.527 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 497,434 | 4.974 | 20 | 20 | fits | 154,658 | 49 | 0.628 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if1` | 752,216 | 7.522 | 20 | 20 | fits | 109,528 | 41 | 0.450 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 281,720 | 2.817 | 20 | 20 | fits | 162,182 | 211 | 0.527 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 160,029 | 1.600 | 20 | 200 | fits | 152,146 | 203 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 331,194 | 3.312 | 20 | 200 | fits | 162,182 | 211 | 0.527 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 160,941 | 1.609 | 20 | 20 | fits | 152,146 | 203 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 898,170 | 8.982 | 20 | 20 | fits | 155,652 | 141 | 0.489 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 164,526 | 1.645 | 20 | 24 | fits | 152,146 | 203 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if1` | 933,604 | 9.336 | 20 | 24 | fits | 31,999 | 21 | 0.658 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 163,486 | 1.635 | 20 | 50 | fits | 152,146 | 203 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 901,150 | 9.011 | 20 | 50 | fits | 155,652 | 141 | 0.489 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 496,799 | 4.968 | 20 | 20 | fits | 161,994 | 55 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if1` | 743,418 | 7.434 | 20 | 20 | fits | 109,724 | 41 | 0.456 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 686,121 | 6.861 | 20 | 20 | fits | 162,800 | 187 | 0.537 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 153,320 | 1.533 | 20 | 200 | fits | 152,495 | 202 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 735,467 | 7.355 | 20 | 200 | fits | 162,800 | 187 | 0.537 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 154,232 | 1.542 | 20 | 20 | fits | 152,495 | 202 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 904,851 | 9.049 | 20 | 20 | fits | 158,356 | 139 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 157,817 | 1.578 | 20 | 24 | fits | 152,495 | 202 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if1` | 908,286 | 9.083 | 20 | 24 | fits | 158,356 | 139 | 0.463 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 156,777 | 1.568 | 20 | 50 | fits | 152,495 | 202 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 739,143 | 7.391 | 20 | 50 | fits | 162,800 | 187 | 0.537 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 319,935 | 3.199 | 20 | 20 | fits | 163,613 | 91 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if1` | 574,263 | 5.743 | 20 | 20 | fits | 109,773 | 41 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 740,791 | 7.408 | 20 | 20 | fits | 157,534 | 139 | 0.536 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 153,245 | 1.532 | 20 | 200 | fits | 152,481 | 202 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 887,706 | 8.877 | 20 | 200 | fits | 157,534 | 139 | 0.536 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 154,157 | 1.542 | 20 | 20 | fits | 152,481 | 202 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 888,402 | 8.884 | 20 | 20 | fits | 157,534 | 139 | 0.536 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 157,742 | 1.577 | 20 | 24 | fits | 152,481 | 202 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if1` | 936,499 | 9.365 | 20 | 24 | fits | 44,662 | 33 | 0.545 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 156,702 | 1.567 | 20 | 50 | fits | 152,481 | 202 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 891,382 | 8.914 | 20 | 50 | fits | 157,534 | 139 | 0.536 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 468,745 | 4.687 | 20 | 20 | fits | 153,989 | 49 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if1` | 731,768 | 7.318 | 20 | 20 | fits | 115,576 | 47 | 0.555 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 690,187 | 6.902 | 20 | 20 | fits | 154,114 | 164 | 0.549 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 157,082 | 1.571 | 20 | 200 | fits | 152,022 | 202 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 739,920 | 7.399 | 20 | 200 | fits | 154,114 | 164 | 0.549 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 157,994 | 1.580 | 20 | 20 | fits | 152,022 | 202 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 892,959 | 8.930 | 20 | 20 | fits | 152,343 | 141 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 161,579 | 1.616 | 20 | 24 | fits | 152,022 | 202 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 928,678 | 9.287 | 20 | 24 | fits | 32,284 | 20 | 0.673 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 160,539 | 1.605 | 20 | 50 | fits | 152,022 | 202 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 895,939 | 8.959 | 20 | 50 | fits | 152,343 | 141 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 314,230 | 3.142 | 20 | 20 | fits | 154,146 | 88 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 587,402 | 5.874 | 20 | 20 | fits | 120,379 | 45 | 0.442 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 787,772 | 7.878 | 20 | 20 | fits | 159,650 | 130 | 0.509 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 163,126 | 1.631 | 20 | 200 | fits | 158,141 | 221 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 896,394 | 8.964 | 20 | 200 | fits | 159,650 | 130 | 0.509 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 164,038 | 1.640 | 20 | 20 | fits | 158,141 | 221 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 897,090 | 8.971 | 20 | 20 | fits | 159,650 | 130 | 0.509 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 167,623 | 1.676 | 20 | 24 | fits | 158,141 | 221 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 900,525 | 9.005 | 20 | 24 | fits | 159,650 | 130 | 0.509 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 166,583 | 1.666 | 20 | 50 | fits | 158,141 | 221 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 337,340 | 3.373 | 20 | 50 | fits | 161,563 | 215 | 0.473 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 491,985 | 4.920 | 20 | 20 | fits | 154,710 | 49 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 738,340 | 7.383 | 20 | 20 | fits | 109,647 | 41 | 0.454 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 714,117 | 7.141 | 20 | 20 | fits | 163,706 | 172 | 0.536 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 174,716 | 1.747 | 20 | 200 | fits | 159,066 | 225 | 0.492 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 751,638 | 7.516 | 20 | 200 | fits | 163,706 | 172 | 0.536 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 175,628 | 1.756 | 20 | 20 | fits | 159,066 | 225 | 0.492 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 912,734 | 9.127 | 20 | 20 | fits | 160,400 | 134 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 179,213 | 1.792 | 20 | 24 | fits | 159,066 | 225 | 0.492 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 916,169 | 9.162 | 20 | 24 | fits | 160,400 | 134 | 0.480 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 178,173 | 1.782 | 20 | 50 | fits | 159,066 | 225 | 0.492 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 755,314 | 7.553 | 20 | 50 | fits | 163,706 | 172 | 0.536 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 331,945 | 3.319 | 20 | 20 | fits | 154,227 | 87 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 589,528 | 5.895 | 20 | 20 | fits | 120,231 | 45 | 0.432 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 845,124 | 8.451 | 20 | 20 | fits | 159,705 | 134 | 0.505 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 156,743 | 1.567 | 20 | 200 | fits | 158,891 | 224 | 0.491 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 970,472 | 9.705 | 20 | 200 | fits | 159,705 | 134 | 0.505 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 157,655 | 1.577 | 20 | 20 | fits | 158,891 | 224 | 0.491 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 971,168 | 9.712 | 20 | 20 | fits | 159,705 | 134 | 0.505 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 161,240 | 1.612 | 20 | 24 | fits | 158,891 | 224 | 0.491 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 1,007,115 | 10.071 | 20 | 24 | fits | 32,512 | 20 | 0.680 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 160,200 | 1.602 | 20 | 50 | fits | 158,891 | 224 | 0.491 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 727,305 | 7.273 | 20 | 50 | fits | 153,659 | 160 | 0.564 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 313,899 | 3.139 | 20 | 20 | fits | 154,154 | 87 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 571,566 | 5.716 | 20 | 20 | fits | 120,231 | 45 | 0.432 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 784,507 | 7.845 | 20 | 20 | fits | 154,640 | 171 | 0.538 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 157,935 | 1.579 | 20 | 200 | fits | 160,158 | 224 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 820,785 | 8.208 | 20 | 200 | fits | 154,640 | 171 | 0.538 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 158,847 | 1.588 | 20 | 20 | fits | 160,158 | 224 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 976,157 | 9.762 | 20 | 20 | fits | 154,676 | 134 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 162,432 | 1.624 | 20 | 24 | fits | 160,158 | 224 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 979,592 | 9.796 | 20 | 24 | fits | 154,676 | 134 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 161,392 | 1.614 | 20 | 50 | fits | 160,158 | 224 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 824,461 | 8.245 | 20 | 50 | fits | 154,640 | 171 | 0.538 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 314,862 | 3.149 | 20 | 20 | fits | 153,925 | 87 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 579,960 | 5.800 | 20 | 20 | fits | 127,787 | 52 | 0.497 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 776,494 | 7.765 | 20 | 20 | fits | 162,695 | 186 | 0.537 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 149,853 | 1.499 | 20 | 200 | fits | 152,151 | 202 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 825,635 | 8.256 | 20 | 200 | fits | 162,695 | 186 | 0.537 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 150,765 | 1.508 | 20 | 20 | fits | 152,151 | 202 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 980,698 | 9.807 | 20 | 20 | fits | 154,367 | 133 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 154,350 | 1.544 | 20 | 24 | fits | 152,151 | 202 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 984,133 | 9.841 | 20 | 24 | fits | 154,367 | 133 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 153,310 | 1.533 | 20 | 50 | fits | 152,151 | 202 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 829,311 | 8.293 | 20 | 50 | fits | 162,695 | 186 | 0.537 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 306,908 | 3.069 | 20 | 20 | fits | 154,053 | 87 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 586,297 | 5.863 | 20 | 20 | fits | 131,739 | 57 | 0.538 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 767,884 | 7.679 | 20 | 20 | fits | 154,408 | 164 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 149,778 | 1.498 | 20 | 200 | fits | 152,137 | 202 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 817,547 | 8.175 | 20 | 200 | fits | 154,408 | 164 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 150,690 | 1.507 | 20 | 20 | fits | 152,137 | 202 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 970,909 | 9.709 | 20 | 20 | fits | 152,666 | 141 | 0.467 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 154,275 | 1.543 | 20 | 24 | fits | 152,137 | 202 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 1,006,628 | 10.066 | 20 | 24 | fits | 32,284 | 20 | 0.673 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 153,235 | 1.532 | 20 | 50 | fits | 152,137 | 202 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 973,889 | 9.739 | 20 | 50 | fits | 152,666 | 141 | 0.467 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 306,926 | 3.069 | 20 | 20 | fits | 154,146 | 88 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 664,735 | 6.647 | 20 | 20 | fits | 120,933 | 45 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 860,515 | 8.605 | 20 | 20 | fits | 159,876 | 129 | 0.514 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 155,714 | 1.557 | 20 | 200 | fits | 158,148 | 220 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 969,115 | 9.691 | 20 | 200 | fits | 159,876 | 129 | 0.514 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 156,626 | 1.566 | 20 | 20 | fits | 158,148 | 220 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 969,811 | 9.698 | 20 | 20 | fits | 159,876 | 129 | 0.514 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 160,211 | 1.602 | 20 | 24 | fits | 158,148 | 220 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 1,006,447 | 10.064 | 20 | 24 | fits | 33,201 | 20 | 0.688 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 159,171 | 1.592 | 20 | 50 | fits | 158,148 | 220 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 317,906 | 3.179 | 20 | 50 | fits | 159,125 | 206 | 0.517 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 563,920 | 5.639 | 20 | 20 | fits | 158,513 | 55 | 0.644 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 810,835 | 8.108 | 20 | 20 | fits | 109,842 | 41 | 0.458 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 714,197 | 7.142 | 20 | 20 | fits | 165,807 | 175 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 169,267 | 1.693 | 20 | 200 | fits | 160,220 | 224 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 764,006 | 7.640 | 20 | 200 | fits | 165,807 | 175 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 170,179 | 1.702 | 20 | 20 | fits | 160,220 | 224 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 906,982 | 9.070 | 20 | 20 | fits | 142,280 | 125 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 173,764 | 1.738 | 20 | 24 | fits | 160,220 | 224 | 0.497 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if1` | 910,417 | 9.104 | 20 | 24 | fits | 142,280 | 125 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 172,724 | 1.727 | 20 | 50 | fits | 160,220 | 224 | 0.497 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 767,682 | 7.677 | 20 | 50 | fits | 165,807 | 175 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 326,194 | 3.262 | 20 | 20 | fits | 153,925 | 87 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if1` | 599,795 | 5.998 | 20 | 20 | fits | 125,630 | 51 | 0.525 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 704,458 | 7.045 | 20 | 20 | fits | 162,401 | 186 | 0.536 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 161,185 | 1.612 | 20 | 200 | fits | 152,213 | 202 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 753,557 | 7.536 | 20 | 200 | fits | 162,401 | 186 | 0.536 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 162,097 | 1.621 | 20 | 20 | fits | 152,213 | 202 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 908,982 | 9.090 | 20 | 20 | fits | 154,729 | 133 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 165,682 | 1.657 | 20 | 24 | fits | 152,213 | 202 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if1` | 912,417 | 9.124 | 20 | 24 | fits | 154,729 | 133 | 0.436 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 164,642 | 1.646 | 20 | 50 | fits | 152,213 | 202 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 757,233 | 7.572 | 20 | 50 | fits | 162,401 | 186 | 0.536 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 318,240 | 3.182 | 20 | 20 | fits | 154,053 | 87 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if1` | 592,752 | 5.928 | 20 | 20 | fits | 122,360 | 45 | 0.489 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 693,641 | 6.936 | 20 | 20 | fits | 153,479 | 164 | 0.546 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 161,110 | 1.611 | 20 | 200 | fits | 152,199 | 202 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 743,196 | 7.432 | 20 | 200 | fits | 153,479 | 164 | 0.546 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 162,022 | 1.620 | 20 | 20 | fits | 152,199 | 202 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 896,557 | 8.966 | 20 | 20 | fits | 152,665 | 135 | 0.525 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 165,607 | 1.656 | 20 | 24 | fits | 152,199 | 202 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if1` | 944,291 | 9.443 | 20 | 24 | fits | 44,299 | 33 | 0.541 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 164,567 | 1.646 | 20 | 50 | fits | 152,199 | 202 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 899,537 | 8.995 | 20 | 50 | fits | 152,665 | 135 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 318,258 | 3.183 | 20 | 20 | fits | 154,146 | 88 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if1` | 591,313 | 5.913 | 20 | 20 | fits | 120,379 | 45 | 0.442 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 799,580 | 7.996 | 20 | 20 | fits | 159,192 | 130 | 0.507 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 167,176 | 1.672 | 20 | 200 | fits | 158,340 | 221 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 907,844 | 9.078 | 20 | 200 | fits | 159,192 | 130 | 0.507 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 168,088 | 1.681 | 20 | 20 | fits | 158,340 | 221 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 908,540 | 9.085 | 20 | 20 | fits | 159,192 | 130 | 0.507 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 171,673 | 1.717 | 20 | 24 | fits | 158,340 | 221 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if1` | 911,975 | 9.120 | 20 | 24 | fits | 159,192 | 130 | 0.507 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 170,633 | 1.706 | 20 | 50 | fits | 158,340 | 221 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 341,176 | 3.412 | 20 | 50 | fits | 161,317 | 215 | 0.471 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 495,821 | 4.958 | 20 | 20 | fits | 154,710 | 49 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if1` | 750,248 | 7.502 | 20 | 20 | fits | 117,742 | 47 | 0.530 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 707,488 | 7.075 | 20 | 20 | fits | 157,212 | 169 | 0.535 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 159,033 | 1.590 | 20 | 200 | fits | 157,850 | 220 | 0.500 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 736,397 | 7.364 | 20 | 200 | fits | 157,212 | 169 | 0.535 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 159,945 | 1.599 | 20 | 20 | fits | 157,850 | 220 | 0.500 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 896,502 | 8.965 | 20 | 20 | fits | 159,409 | 139 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 163,530 | 1.635 | 20 | 24 | fits | 157,850 | 220 | 0.500 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if1` | 899,937 | 8.999 | 20 | 24 | fits | 159,409 | 139 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 162,490 | 1.625 | 20 | 50 | fits | 157,850 | 220 | 0.500 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 740,073 | 7.401 | 20 | 50 | fits | 157,212 | 169 | 0.535 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 315,776 | 3.158 | 20 | 20 | fits | 153,741 | 87 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if1` | 580,781 | 5.808 | 20 | 20 | fits | 127,694 | 51 | 0.497 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 705,996 | 7.060 | 20 | 20 | fits | 163,655 | 173 | 0.535 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 159,493 | 1.595 | 20 | 200 | fits | 158,385 | 224 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 743,622 | 7.436 | 20 | 200 | fits | 163,655 | 173 | 0.535 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 160,405 | 1.604 | 20 | 20 | fits | 158,385 | 224 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 905,815 | 9.058 | 20 | 20 | fits | 150,882 | 134 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 163,990 | 1.640 | 20 | 24 | fits | 158,385 | 224 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if1` | 909,250 | 9.092 | 20 | 24 | fits | 150,882 | 134 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 162,950 | 1.629 | 20 | 50 | fits | 158,385 | 224 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 747,298 | 7.473 | 20 | 50 | fits | 163,655 | 173 | 0.535 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 316,649 | 3.166 | 20 | 20 | fits | 154,154 | 87 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if1` | 581,563 | 5.816 | 20 | 20 | fits | 120,102 | 45 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 710,012 | 7.100 | 20 | 20 | fits | 155,057 | 171 | 0.540 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 160,322 | 1.603 | 20 | 200 | fits | 159,289 | 224 | 0.492 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 746,217 | 7.462 | 20 | 200 | fits | 155,057 | 171 | 0.540 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 161,234 | 1.612 | 20 | 20 | fits | 159,289 | 224 | 0.492 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 901,712 | 9.017 | 20 | 20 | fits | 154,799 | 134 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 164,819 | 1.648 | 20 | 24 | fits | 159,289 | 224 | 0.492 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if1` | 905,147 | 9.051 | 20 | 24 | fits | 154,799 | 134 | 0.432 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 163,779 | 1.638 | 20 | 50 | fits | 159,289 | 224 | 0.492 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 749,893 | 7.499 | 20 | 50 | fits | 155,057 | 171 | 0.540 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 317,249 | 3.172 | 20 | 20 | fits | 153,925 | 87 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if1` | 582,187 | 5.822 | 20 | 20 | fits | 120,150 | 46 | 0.429 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 275,858 | 2.759 | 20 | 20 | fits | 160,284 | 201 | 0.551 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 152,811 | 1.528 | 20 | 200 | fits | 151,853 | 202 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 312,486 | 3.125 | 20 | 200 | fits | 160,284 | 201 | 0.551 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 153,723 | 1.537 | 20 | 20 | fits | 151,853 | 202 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 889,866 | 8.899 | 20 | 20 | fits | 156,169 | 141 | 0.496 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 157,308 | 1.573 | 20 | 24 | fits | 151,853 | 202 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if1` | 937,639 | 9.376 | 20 | 24 | fits | 44,338 | 33 | 0.543 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 156,268 | 1.563 | 20 | 50 | fits | 151,853 | 202 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 892,846 | 8.928 | 20 | 50 | fits | 156,169 | 141 | 0.496 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 471,581 | 4.716 | 20 | 20 | fits | 155,484 | 50 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if1` | 734,597 | 7.346 | 20 | 20 | fits | 109,935 | 41 | 0.462 |
| LINK_UP | `adp.link_up.if0` | 3,012 | 0.030 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| LINK_UP | `adp.link_up.if1` | 15,868 | 0.159 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,019 | 0.260 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 20,812 | 0.208 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 21,089 | 0.211 | 20 | 200 | fits | 5,615 | 19 (11) | 0.618 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 18,565 | 0.186 | 20 | 200 | fits | 5,615 | 19 (11) | 0.618 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,538 | 0.135 | 20 | 50 | fits | 32,905 | 44 | 0.739 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 12,144 | 0.121 | 20 | 50 | fits | 29,645 | 36 | 0.719 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 26,082 | 0.261 | 20 | 50 | fits | 29,274 | 36 | 0.712 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 15,528 | 0.155 | 20 | 50 | fits | 33,771 | 62 | 0.617 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 17,245 | 0.172 | 20 | 50 | fits | 33,771 | 62 | 0.617 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,167 | 0.112 | 20 | 50 | fits | 27,333 | 31 | 0.632 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 12,131 | 0.121 | 20 | 50 | fits | 31,184 | 44 | 0.703 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 20,102 | 0.201 | 20 | 50 | fits | 29,849 | 37 | 0.719 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 26,133 | 0.261 | 20 | 50 | fits | 28,681 | 36 | 0.683 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 16,080 | 0.161 | 20 | 50 | fits | 34,408 | 62 | 0.640 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 17,770 | 0.178 | 20 | 50 | fits | 34,408 | 62 | 0.640 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 11,430 | 0.114 | 20 | 50 | fits | 27,413 | 31 | 0.611 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 27,922 | 0.279 | 20 | 20 | fits | 44,971 | 35 (35) | 0.760 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 39,193 | 0.392 | 20 | 20 | fits | 44,971 | 35 (35) | 0.760 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 8,003 | 0.080 | 20 | 20 | fits | 39,963 | 27 (14) | 0.834 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 16,788 | 0.168 | 20 | 20 | fits | 39,963 | 27 (14) | 0.834 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 26,491 | 0.265 | 20 | 20 | fits | 38,693 | 28 (14) | 0.828 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 34,963 | 0.350 | 20 | 20 | fits | 38,693 | 28 (14) | 0.828 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 45,543 | 0.455 | 20 | 20 | fits | 34,478 | 22 (35) | 0.821 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 43,578 | 0.436 | 20 | 20 | fits | 43,335 | 35 (35) | 0.800 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 78,522 | 0.785 | 20 | 20 | fits | 51,850 | 6 | 0.895 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 73,818 | 0.738 | 20 | 20 | fits | 46,947 | 6 | 0.872 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 49,599 | 0.496 | 20 | 20 | fits | 49,664 | 13 | 0.909 |
| malformed MRPDU discard | `srp.malformed.if0` | 25,194 | 0.252 | 20 | 20 | fits | 25,259 | 13 | 0.771 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 91,264 | 0.913 | 220 | 220 | fits | 80,421 | 9 | 0.899 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 42,802 | 0.428 | 20 | 20 | fits | 42,867 | 13 | 0.900 |
| malformed MRPDU discard | `srp.malformed.if1` | 23,510 | 0.235 | 20 | 20 | fits | 23,575 | 13 | 0.769 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 79,094 | 0.791 | 220 | 220 | fits | 69,685 | 9 | 0.897 |
| an event behind 15 others | `backlog.event.if0` | 179,963 | 1.800 | 20 | 200 | fits | 94,321 | 131 | 0.542 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 669,975 | 6.700 | 20 | 20 | fits | 156,232 | 132 | 0.463 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 167,967 | 1.680 | 20 | 200 | fits | 168,175 | 233 | 0.505 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 352,898 | 3.529 | 20 | 200 | fits | 91,219 | 55 | 0.643 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 163,708 | 1.637 | 20 | 20 | fits | 168,175 | 233 | 0.505 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 753,756 | 7.538 | 20 | 20 | fits | 156,232 | 132 | 0.463 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 167,293 | 1.673 | 20 | 24 | fits | 168,175 | 233 | 0.505 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 757,191 | 7.572 | 20 | 24 | fits | 156,232 | 132 | 0.463 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 166,253 | 1.663 | 20 | 50 | fits | 168,175 | 233 | 0.505 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 351,403 | 3.514 | 20 | 50 | fits | 91,219 | 55 | 0.643 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 453,008 | 4.530 | 20 | 20 | fits | 97,258 | 53 | 0.556 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 598,424 | 5.984 | 20 | 20 | fits | 63,515 | 37 | 0.488 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 706,992 | 7.070 | 20 | 20 | fits | 165,363 | 175 | 0.525 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 155,559 | 1.556 | 20 | 200 | fits | 160,241 | 230 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 756,780 | 7.568 | 20 | 200 | fits | 165,363 | 175 | 0.525 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 156,471 | 1.565 | 20 | 20 | fits | 160,241 | 230 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 899,719 | 8.997 | 20 | 20 | fits | 142,243 | 125 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 160,056 | 1.601 | 20 | 24 | fits | 160,241 | 230 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 903,154 | 9.032 | 20 | 24 | fits | 142,243 | 125 | 0.447 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 159,016 | 1.590 | 20 | 50 | fits | 160,241 | 230 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 760,456 | 7.605 | 20 | 50 | fits | 165,363 | 175 | 0.525 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 312,197 | 3.122 | 20 | 20 | fits | 153,636 | 88 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 593,013 | 5.930 | 20 | 20 | fits | 127,860 | 51 | 0.503 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 18,028 | 0.180 | 20 | 20 | fits | 33,050 | 20 | 0.802 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 155,559 | 1.556 | 20 | 200 | fits | 160,241 | 230 | 0.493 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 40,652 | 0.407 | 20 | 200 | fits | 33,050 | 20 | 0.802 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 156,471 | 1.565 | 20 | 20 | fits | 160,241 | 230 | 0.493 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 884,149 | 8.841 | 20 | 20 | fits | 132,488 | 119 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 160,056 | 1.601 | 20 | 24 | fits | 160,241 | 230 | 0.493 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 887,584 | 8.876 | 20 | 24 | fits | 132,488 | 119 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 159,016 | 1.590 | 20 | 50 | fits | 160,241 | 230 | 0.493 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 754,641 | 7.546 | 20 | 50 | fits | 159,548 | 174 | 0.500 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 312,197 | 3.122 | 20 | 20 | fits | 153,636 | 88 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 593,013 | 5.930 | 20 | 20 | fits | 127,860 | 51 | 0.503 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,363,368 | 63.634 | 20 | 20 | MISS ceiling | 29,671 | 19 | 0.743 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,385,434 | 63.854 | 20 | 20 | MISS ceiling | 25,036 | 14 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,410,234 | 64.102 | 20 | 20 | MISS ceiling | 23,665 | 14 | 0.704 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,433,804 | 64.338 | 20 | 20 | MISS ceiling | 23,462 | 14 | 0.680 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,457,076 | 64.571 | 20 | 20 | MISS ceiling | 23,267 | 14 | 0.657 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 158,818 | 1.588 | 20 | 200 | fits | 155,389 | 198 | 0.516 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 712,125 | 7.121 | 20 | 200 | fits | 130,397 | 154 | 0.501 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 154,559 | 1.546 | 20 | 20 | fits | 155,389 | 198 | 0.516 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,247,139 | 62.471 | 20 | 20 | MISS ceiling | 35,781 | 16 | 0.760 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,144 | 1.581 | 20 | 24 | fits | 155,389 | 198 | 0.516 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,179,264 | 61.793 | 20 | 24 | MISS ceiling | 158,197 | 136 | 0.373 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 157,104 | 1.571 | 20 | 50 | fits | 155,389 | 198 | 0.516 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 710,630 | 7.106 | 20 | 50 | fits | 130,397 | 154 | 0.501 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 321,000 | 3.210 | 20 | 20 | fits | 164,351 | 92 | 0.601 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 578,153 | 5.782 | 20 | 20 | fits | 119,101 | 48 | 0.542 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 8,394 | 0.084 | 20 | 20 | fits | 40,503 | 22 (29) | 0.662 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 15,886 | 0.159 | 20 | 20 | fits | 40,503 | 22 (29) | 0.662 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 9,821 | 0.098 | 20 | 20 | fits | 42,996 | 33 (35) | 0.656 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 17,741 | 0.177 | 20 | 20 | fits | 42,996 | 33 (35) | 0.656 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 15,966 | 0.160 | 20 | 20 | fits | 39,939 | 25 (12) | 0.845 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 44,121 | 0.441 | 20 | 20 | fits | 38,465 | 29 (12) | 0.819 |
| LINK_UP | `adp.link_up.if0` | 3,012 | 0.030 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| LINK_UP | `adp.link_up.if1` | 15,868 | 0.159 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,019 | 0.260 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 20,812 | 0.208 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| LINK_DOWN | `adp.link_down.if0` | 2,697 | 0.027 | 20 | 200 | fits | 44,922 | 39 (9) | 0.745 |
| LINK_DOWN | `adp.link_down.if1` | 17,949 | 0.179 | 20 | 200 | fits | 44,922 | 39 (9) | 0.745 |
| LINK_UP | `adp.link_up.if0` | 3,012 | 0.030 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| LINK_UP | `adp.link_up.if1` | 15,868 | 0.159 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,019 | 0.260 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 20,812 | 0.208 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| GM_CHANGE | `adp.gm_change.if0` | 2,815 | 0.028 | 20 | 200 | fits | 22,425 | 27 (11) | 0.698 |
| GM_CHANGE | `adp.gm_change.if1` | 5,039 | 0.050 | 20 | 200 | fits | 22,425 | 27 (11) | 0.698 |
| LINK_UP | `adp.link_up.if0` | 3,012 | 0.030 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| LINK_UP | `adp.link_up.if1` | 15,868 | 0.159 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,019 | 0.260 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 20,812 | 0.208 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,599 | 0.056 | 20 | 200 | fits | 25,793 | 28 (31) | 0.524 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 7,030 | 0.070 | 20 | 200 | fits | 25,793 | 28 (31) | 0.524 |
| LINK_UP | `adp.link_up.if0` | 3,012 | 0.030 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| LINK_UP | `adp.link_up.if1` | 15,868 | 0.159 | 20 | 200 | fits | 42,878 | 79 (11) | 0.654 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 26,019 | 0.260 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 20,812 | 0.208 | 20 | 200 | fits | 30,396 | 39 (39) | 0.640 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 5,599 | 0.056 | 20 | 200 | fits | 21,263 | 17 (31) | 0.681 |
| set_name | `aecp_fanout.set_name.if0` | 61,211 | 0.612 | 20 | 24 | fits | 74,836 | 161 | 0.404 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 48,549 | 0.485 | 20 | 24 | fits | 63,998 | 140 | 0.418 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 51,080 | 0.511 | 20 | 24 | fits | 60,703 | 140 | 0.388 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 54,968 | 0.550 | 20 | 24 | fits | 69,643 | 149 | 0.413 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 47,589 | 0.476 | 20 | 24 | fits | 62,771 | 116 | 0.422 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 50,701 | 0.507 | 20 | 24 | fits | 60,445 | 140 | 0.387 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,776 | 0.458 | 20 | 24 | fits | 59,841 | 140 | 0.372 |
| set_name | `aecp_fanout.set_name.if1` | 51,787 | 0.518 | 20 | 24 | fits | 67,212 | 117 | 0.392 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 53,638 | 0.536 | 20 | 24 | fits | 64,315 | 140 | 0.424 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 45,065 | 0.451 | 20 | 24 | fits | 59,672 | 140 | 0.374 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 50,311 | 0.503 | 20 | 24 | fits | 59,793 | 140 | 0.379 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 50,150 | 0.501 | 20 | 24 | fits | 59,772 | 140 | 0.377 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 45,393 | 0.454 | 20 | 24 | fits | 59,316 | 140 | 0.367 |
| BIND_RX | `acmp.bind_rx.if0` | 20,932 | 0.209 | 20 | 20 | fits | 45,795 | 27 (77) | 0.786 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,280 | 0.103 | 20 | 20 | fits | 36,199 | 20 (32) | 0.846 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,364 | 0.104 | 20 | 20 | fits | 29,426 | 16 (47) | 0.762 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,725 | 0.147 | 20 | 20 | fits | 41,551 | 19 (50) | 0.829 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,255 | 0.103 | 20 | 20 | fits | 29,749 | 18 (48) | 0.743 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 8,992 | 0.090 | 20 | 20 | fits | 27,970 | 18 (48) | 0.697 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,695 | 0.097 | 20 | 20 | fits | 28,695 | 17 (48) | 0.743 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,365 | 0.084 | 20 | 20 | fits | 27,109 | 17 (48) | 0.681 |
| BIND_RX | `acmp.bind_rx.if1` | 18,164 | 0.182 | 20 | 20 | fits | 43,059 | 28 (77) | 0.731 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 9,789 | 0.098 | 20 | 20 | fits | 36,387 | 21 (32) | 0.829 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 9,980 | 0.100 | 20 | 20 | fits | 29,502 | 17 (47) | 0.758 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 14,522 | 0.145 | 20 | 20 | fits | 42,875 | 22 (50) | 0.819 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if1` | 10,722 | 0.107 | 20 | 20 | fits | 29,981 | 20 (48) | 0.747 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 10,576 | 0.106 | 20 | 20 | fits | 29,834 | 18 (48) | 0.750 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 8,508 | 0.085 | 20 | 20 | fits | 27,536 | 18 (48) | 0.684 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if1` | 8,584 | 0.086 | 20 | 20 | fits | 27,287 | 18 (48) | 0.675 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 29,472 | 0.295 | 20 | 24 | fits | 29,377 | 22 | 0.776 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 20,282 | 0.203 | 20 | 24 | fits | 33,725 | 22 | 0.702 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 15,658 | 0.157 | 20 | 24 | fits | 39,715 | 31 | 0.720 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 9,174 | 0.092 | 20 | 24 | fits | 29,639 | 22 | 0.706 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 15,321 | 0.153 | 20 | 24 | fits | 30,005 | 22 | 0.717 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 9,971 | 0.100 | 20 | 24 | fits | 30,252 | 22 | 0.712 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,536 | 0.145 | 20 | 24 | fits | 29,397 | 22 | 0.720 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 27,785 | 0.278 | 20 | 24 | fits | 28,740 | 22 | 0.719 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 29,221 | 0.292 | 20 | 24 | fits | 29,432 | 22 | 0.741 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 19,074 | 0.191 | 20 | 24 | fits | 34,899 | 23 | 0.658 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 27,808 | 0.278 | 20 | 24 | fits | 29,146 | 22 | 0.755 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 14,284 | 0.143 | 20 | 24 | fits | 29,006 | 22 | 0.759 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 14,861 | 0.149 | 20 | 24 | fits | 38,417 | 31 | 0.708 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 9,425 | 0.094 | 20 | 24 | fits | 30,044 | 22 | 0.718 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,838 | 0.158 | 20 | 24 | fits | 29,996 | 22 | 0.725 |
| get_configuration | `aecp.get_configuration.if0` | 26,663 | 0.267 | 20 | 24 | fits | 25,954 | 22 | 0.723 |
| entity_available | `aecp.entity_available.if0` | 12,136 | 0.121 | 20 | 24 | fits | 26,593 | 22 | 0.723 |
| get_name | `aecp.get_name.if0` | 28,157 | 0.282 | 20 | 24 | fits | 29,076 | 22 | 0.724 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 30,619 | 0.306 | 20 | 24 | fits | 30,738 | 28 | 0.710 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 26,423 | 0.264 | 20 | 24 | fits | 30,548 | 31 | 0.735 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 25,667 | 0.257 | 20 | 24 | fits | 26,059 | 22 | 0.716 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 12,500 | 0.125 | 20 | 24 | fits | 25,597 | 22 | 0.700 |
| set_name | `aecp.set_name.if0` | 38,854 | 0.389 | 20 | 24 | fits | 58,607 | 75 | 0.685 |
| lock_entity | `aecp.lock_entity.if0` | 24,095 | 0.241 | 20 | 24 | fits | 35,895 | 47 | 0.716 |
| unlock_entity | `aecp.unlock_entity.if0` | 31,456 | 0.315 | 20 | 24 | fits | 35,813 | 46 | 0.724 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 12,272 | 0.123 | 20 | 24 | fits | 28,290 | 20 | 0.757 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 20,738 | 0.207 | 20 | 24 | fits | 32,697 | 20 | 0.698 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 17,808 | 0.178 | 20 | 24 | fits | 30,128 | 20 | 0.735 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 11,224 | 0.112 | 20 | 24 | fits | 29,154 | 20 | 0.700 |
| get_configuration | `aecp.get_configuration.if1` | 15,295 | 0.153 | 20 | 24 | fits | 26,214 | 20 | 0.743 |
| entity_available | `aecp.entity_available.if1` | 8,273 | 0.083 | 20 | 24 | fits | 26,142 | 20 | 0.715 |
| get_name | `aecp.get_name.if1` | 17,082 | 0.171 | 20 | 24 | fits | 29,379 | 20 | 0.742 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if1` | 18,430 | 0.184 | 20 | 24 | fits | 39,948 | 35 | 0.706 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if1` | 11,712 | 0.117 | 20 | 24 | fits | 29,656 | 29 | 0.731 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if1` | 15,542 | 0.155 | 20 | 24 | fits | 26,089 | 20 | 0.733 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 7,687 | 0.077 | 20 | 24 | fits | 25,264 | 20 | 0.694 |
| set_name | `aecp.set_name.if1` | 34,474 | 0.345 | 20 | 24 | fits | 43,857 | 25 | 0.750 |
| lock_entity | `aecp.lock_entity.if1` | 24,374 | 0.244 | 20 | 24 | fits | 36,368 | 50 | 0.693 |
| unlock_entity | `aecp.unlock_entity.if1` | 23,197 | 0.232 | 20 | 24 | fits | 36,470 | 49 | 0.701 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
