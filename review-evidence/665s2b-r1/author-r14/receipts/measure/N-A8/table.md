### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 134 paths and 6 of 456 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.261 (0.662) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.221 (0.607) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.120 (0.470) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.110 (0.460) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.077 (0.631) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.271 (0.631) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.067 (0.611) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.255 (0.611) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.119 (0.488) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.230 (0.619) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.110 (0.454) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.110 (0.460) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.194 (0.538) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.127 (0.480) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.123 (0.476) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.197 (0.564) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.182 (0.574) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.088 (0.477) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.501 (1.830) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.411 (1.867) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.099 (0.874) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.414 (0.827) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.355 (0.802) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.248 (0.804) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.160 (0.887) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.124 (0.689) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.161 (0.893) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.088 (0.539) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.169 (1.626) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.126 (0.680) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.167 (0.601) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.161 (0.598) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.033 (0.222) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.047 (0.222) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.018 (0.204) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.032 (0.204) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.018 (0.609) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.296 (0.609) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.020 (1.310) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.156 (1.310) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.182 (0.382) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.164 (0.382) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.236 (0.614) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.164 (0.614) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.238 (0.553) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.160 (0.468) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.249 (0.567) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 0.172 (0.493) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.143 (0.273) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.249 (0.567) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.183 (0.321) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 0.189 (0.505) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.167 (0.302) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.275 (0.596) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.400 (0.779) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.233 (0.634) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.242 (0.562) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.161 (0.471) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.303 (0.620) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.309 (0.628) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.263 (0.578) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.255 (0.548) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.159 (0.290) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.168 (0.300) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.307 (0.624) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.158 (0.288) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.251 (0.566) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.167 (0.298) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.181 (0.508) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.159 (0.289) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.174 (0.306) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.257 (0.573) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.257 (0.573) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.172 (0.303) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.253 (0.568) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.329 (0.650) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.323 (0.641) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.470 (0.892) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.362 (0.771) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.325 (0.625) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 0.251 (0.568) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.314 (0.691) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.241 (0.633) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.842 (1.232) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.831 (1.332) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.854 (1.370) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.856 (1.389) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.837 (1.228) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 0.712 (1.104) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.845 (1.284) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.989 (1.491) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.823 (1.324) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.718 (1.107) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.718 (1.107) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.636 (7.357) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 5.419 (7.509) | fits | 7 adp | 25 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.107 (0.658) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.467 (2.527) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.777 (64.336) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.866 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 8.269 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.860 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 11.486 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 5.414 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 14.603 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.193 (0.578) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.177 (0.585) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.115 (0.274) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.117 (0.288) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.133 (1.193) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.124 (1.121) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.174 (0.578) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.156 (0.585) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.226 (0.593) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 0.183 (0.576) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.960 | fits | 0 acmp | 28 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 9.021 | fits | 11 acmp | 28 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.951 | fits | 0 adp | 28 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 6.570 | fits | 7 adp | 26 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.846 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.996 | fits | 0 aecp | 28 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 65.135 | MISS ceiling | 15 aecp | 28 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.986 | fits | 0 maap | 28 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.607 | fits | 6 maap | 28 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 5.451 | fits | 0 srp | 28 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@blank-0.service.srp.last.if1` (backlog-adp@blank-0) | 17.234 | fits | 31 srp | 28 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.749 (1.905) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.533 (1.665) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.598 (0.599) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.524 (0.525) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.248 (0.249) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.246 (0.246) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.548 (1.653) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.481 (1.577) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 18.599 | 19 | 189,276 (1.893) | yes | - |
| backlog-adp@blank-1 | 0 | 17.749 | 18 | 189,105 (1.891) | yes | - |
| backlog-adp@blank-2 | 0 | 18.904 | 19 | 195,780 (1.958) | yes | - |
| backlog-adp@blank-3 | 0 | 17.782 | 19 | 183,774 (1.838) | yes | - |
| backlog-adp@blank-4 | 0 | 18.257 | 20 | 191,124 (1.911) | yes | - |
| backlog-adp@blank-5 | 0 | 17.861 | 19 | 189,206 (1.892) | yes | - |
| backlog-adp@blank-6 | 0 | 17.842 | 19 | 187,976 (1.880) | yes | - |
| backlog-adp@blank-7 | 0 | 17.628 | 17 | 195,596 (1.956) | yes | - |
| backlog-adp@program-0 | 0 | 17.977 | 18 | 190,300 (1.903) | yes | - |
| backlog-adp@program-1 | 0 | 17.795 | 18 | 188,346 (1.883) | yes | - |
| backlog-adp@program-2 | 0 | 17.821 | 18 | 188,346 (1.883) | yes | - |
| backlog-adp@program-3 | 0 | 17.726 | 18 | 183,132 (1.831) | yes | - |
| backlog-adp@program-4 | 0 | 17.137 | 19 | 188,357 (1.884) | yes | - |
| backlog-adp@program-5 | 0 | 17.302 | 19 | 188,306 (1.883) | yes | - |
| backlog-adp@program-6 | 0 | 17.379 | 20 | 181,264 (1.813) | yes | - |
| backlog-adp@program-7 | 0 | 17.101 | 18 | 194,731 (1.947) | yes | - |
| backlog-adp@verify-0 | 0 | 17.838 | 17 | 195,742 (1.957) | yes | - |
| backlog-adp@verify-1 | 0 | 19.712 | 21 | 183,766 (1.838) | yes | - |
| backlog-adp@verify-2 | 0 | 18.334 | 18 | 191,006 (1.910) | yes | - |
| backlog-adp@verify-3 | 0 | 18.301 | 19 | 188,833 (1.888) | yes | - |
| backlog-adp@verify-4 | 0 | 17.986 | 18 | 188,833 (1.888) | yes | - |
| backlog-adp@verify-5 | 0 | 18.170 | 18 | 171,917 (1.719) | yes | - |
| backlog-adp@verify-6 | 0 | 18.126 | 18 | 195,385 (1.954) | yes | - |
| backlog-adp@verify-7 | 0 | 17.898 | 17 | 183,824 (1.838) | yes | - |
| backlog | 0 | 14.466 | 20 | 157,383 (1.574) | yes | - |
| backlog-adp | 0 | 16.965 | 19 | 196,985 (1.970) | yes | - |
| backlog-adp-refill | 0 | 41.035 | 28 | 177,795 (1.778) | yes | - |
| backlog-owed | 0 | 360.917 | 65 | 191,323 (1.913) | yes | - |

Composed maximum over the 4 backlog windows: 196,985 CPU cycles (1.970 ms), backlog-adp.
Over the windows that released their whole load only: 196,985 (1.970 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 8474 | 0 | 168,634 (1.686) | fits |
| save-starved | 52488 | 0 | 171,111 (1.711) | fits |
| acmp-notk | 2656 | 0 | 130,958 (1.310) | fits |
| backlog-adp@blank-0 | 480 | 0 | 189,276 (1.893) | fits |
| backlog-adp@blank-1 | 479 | 0 | 189,105 (1.891) | fits |
| backlog-adp@blank-2 | 480 | 0 | 195,780 (1.958) | fits |
| backlog-adp@blank-3 | 480 | 0 | 183,774 (1.838) | fits |
| backlog-adp@blank-4 | 481 | 0 | 191,124 (1.911) | fits |
| backlog-adp@blank-5 | 482 | 0 | 189,206 (1.892) | fits |
| backlog-adp@blank-6 | 482 | 0 | 187,976 (1.880) | fits |
| backlog-adp@blank-7 | 480 | 0 | 195,596 (1.956) | fits |
| backlog-adp@program-0 | 762 | 0 | 190,300 (1.903) | fits |
| backlog-adp@program-1 | 764 | 0 | 188,346 (1.883) | fits |
| backlog-adp@program-2 | 764 | 0 | 188,346 (1.883) | fits |
| backlog-adp@program-3 | 764 | 0 | 183,132 (1.831) | fits |
| backlog-adp@program-4 | 766 | 0 | 188,357 (1.884) | fits |
| backlog-adp@program-5 | 766 | 0 | 188,306 (1.883) | fits |
| backlog-adp@program-6 | 767 | 0 | 181,264 (1.813) | fits |
| backlog-adp@program-7 | 766 | 0 | 194,731 (1.947) | fits |
| backlog-adp@verify-0 | 1043 | 0 | 195,742 (1.957) | fits |
| backlog-adp@verify-1 | 1047 | 0 | 183,766 (1.838) | fits |
| backlog-adp@verify-2 | 1045 | 0 | 191,006 (1.910) | fits |
| backlog-adp@verify-3 | 1046 | 0 | 188,833 (1.888) | fits |
| backlog-adp@verify-4 | 1045 | 0 | 188,833 (1.888) | fits |
| backlog-adp@verify-5 | 1045 | 0 | 171,917 (1.719) | fits |
| backlog-adp@verify-6 | 1045 | 0 | 195,385 (1.954) | fits |
| backlog-adp@verify-7 | 1045 | 0 | 183,824 (1.838) | fits |
| adp-advertise | 605 | 0 | 130,958 (1.310) | fits |
| maap | 349 | 0 | 131,286 (1.313) | fits |
| acmp-noresp | 1547 | 0 | 130,958 (1.310) | fits |
| save | 617 | 0 | 130,958 (1.310) | fits |
| srp | 307 | 0 | 190,478 (1.905) | fits |
| backlog | 303 | 0 | 157,383 (1.574) | fits |
| backlog-adp | 320 | 0 | 196,985 (1.970) | fits |
| backlog-adp-refill | 329 | 0 | 177,795 (1.778) | fits |
| backlog-owed | 359 | 0 | 191,323 (1.913) | fits |
| acmp-disc | 783 | 0 | 130,958 (1.310) | fits |
| adp-link | 92 | 0 | 130,958 (1.310) | fits |
| adp-gm | 90 | 0 | 130,958 (1.310) | fits |
| adp-discover | 90 | 0 | 130,958 (1.310) | fits |
| control | 90 | 0 | 130,958 (1.310) | fits |
| aecp-fanout | 146 | 0 | 130,958 (1.310) | fits |
| acmp-cmd | 98 | 0 | 130,958 (1.310) | fits |
| aecp | 137 | 0 | 130,958 (1.310) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---|---|
| save-held | 4696.877 | 12,110 | 370 | 19.447 | no | within |
| save-starved | 12087.011 | 12,110 | 370 | 31.325 | yes | within |
| save | 4697.358 | 12,110 | 370 | 12.611 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1526 | 127,290 (1.273) | 96,203 (0.962) |
| save-starved | 687 | 102,374 (1.024) | 96,213 (0.962) |
| acmp-notk | 1065 | 129,153 (1.292) | 96,034 (0.960) |
| backlog-adp@blank-0 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-1 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-2 | 338 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-3 | 337 | 102,374 (1.024) | 76,347 (0.763) |
| backlog-adp@blank-4 | 337 | 102,374 (1.024) | 76,375 (0.764) |
| backlog-adp@blank-5 | 337 | 102,374 (1.024) | 76,234 (0.762) |
| backlog-adp@blank-6 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@blank-7 | 337 | 102,374 (1.024) | 76,231 (0.762) |
| backlog-adp@program-0 | 443 | 122,002 (1.220) | 82,302 (0.823) |
| backlog-adp@program-1 | 443 | 122,002 (1.220) | 82,388 (0.824) |
| backlog-adp@program-2 | 443 | 122,002 (1.220) | 82,302 (0.823) |
| backlog-adp@program-3 | 443 | 122,002 (1.220) | 82,302 (0.823) |
| backlog-adp@program-4 | 444 | 122,002 (1.220) | 82,162 (0.822) |
| backlog-adp@program-5 | 444 | 122,002 (1.220) | 82,162 (0.822) |
| backlog-adp@program-6 | 444 | 122,002 (1.220) | 82,162 (0.822) |
| backlog-adp@program-7 | 444 | 122,002 (1.220) | 82,162 (0.822) |
| backlog-adp@verify-0 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-1 | 547 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-2 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-3 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-4 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-5 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-6 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| backlog-adp@verify-7 | 546 | 122,002 (1.220) | 96,031 (0.960) |
| adp-advertise | 577 | 102,374 (1.024) | 2,982 (0.030) |
| maap | 327 | 47,960 (0.480) | 3,045 (0.030) |
| acmp-noresp | 615 | 128,475 (1.285) | 95,887 (0.959) |
| save | 585 | 126,870 (1.269) | 95,525 (0.955) |
| srp | 278 | 102,374 (1.024) | 2,982 (0.030) |
| backlog | 266 | 102,374 (1.024) | 2,982 (0.030) |
| backlog-adp | 271 | 102,374 (1.024) | 2,982 (0.030) |
| backlog-adp-refill | 273 | 102,374 (1.024) | 2,982 (0.030) |
| backlog-owed | 306 | 102,374 (1.024) | 2,982 (0.030) |
| acmp-disc | 336 | 123,484 (1.235) | 82,162 (0.822) |
| adp-link | 79 | 102,374 (1.024) | 2,982 (0.030) |
| adp-gm | 79 | 102,374 (1.024) | 2,982 (0.030) |
| adp-discover | 79 | 102,374 (1.024) | 2,982 (0.030) |
| control | 79 | 102,374 (1.024) | 2,982 (0.030) |
| aecp-fanout | 93 | 102,374 (1.024) | 3,588 (0.036) |
| acmp-cmd | 67 | 102,374 (1.024) | 2,982 (0.030) |
| aecp | 88 | 102,374 (1.024) | 2,982 (0.030) |

Longest pass that carries a step: 129,153 CPU cycles (1.292 ms), acmp-notk; longest step: 96,213 (0.962 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 477,582 | 4.776 | 20 | 200 | fits | 124,109 | 85 | 0.569 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 810,580 | 8.106 | 20 | 20 | fits | 117,445 | 46 | 0.671 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 1,091,524 | 10.915 | 20 | 24 | fits | 39,893 | 29 | 0.607 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 529,557 | 5.296 | 20 | 50 | fits | 111,587 | 56 | 0.642 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 1,412,057 | 14.121 | 18 | 18 | fits | 66,231 | 31 | 0.693 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 485,990 | 4.860 | 20 | 200 | fits | 127,001 | 91 | 0.592 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 826,870 | 8.269 | 20 | 20 | fits | 120,819 | 52 | 0.684 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 1,148,572 | 11.486 | 20 | 24 | fits | 34,628 | 29 | 0.595 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 541,435 | 5.414 | 20 | 50 | fits | 115,057 | 62 | 0.663 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,460,328 | 14.603 | 18 | 18 | fits | 69,473 | 37 | 0.709 |
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 16,129 | 0.161 | 20 | 20 | fits | 64,819 | 51 (14) | 0.716 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 8,791 | 0.088 | 20 | 20 | fits | 53,891 | 20 (14) | 0.874 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 541,888 | 5.419 | 20 | 20 | fits | 126,468 | 85 | 0.632 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 195,101 | 1.951 | 20 | 200 | fits | 120,046 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 657,043 | 6.570 | 20 | 200 | fits | 126,468 | 85 | 0.632 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 196,013 | 1.960 | 20 | 20 | fits | 120,046 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 902,111 | 9.021 | 20 | 20 | fits | 121,406 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 199,598 | 1.996 | 20 | 24 | fits | 120,046 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,586,544 | 15.865 | 20 | 24 | fits | 67,834 | 31 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 198,558 | 1.986 | 20 | 50 | fits | 120,046 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 660,719 | 6.607 | 20 | 50 | fits | 126,468 | 85 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 387,379 | 3.874 | 18 | 18 | fits | 189,276 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,723,372 | 17.234 | 18 | 18 | fits | 36,804 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 466,768 | 4.668 | 20 | 20 | fits | 156,626 | 89 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 125,772 | 1.258 | 20 | 200 | fits | 119,376 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 610,004 | 6.100 | 20 | 200 | fits | 156,626 | 89 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 126,684 | 1.267 | 20 | 20 | fits | 119,376 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 854,049 | 8.540 | 20 | 20 | fits | 121,198 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 130,269 | 1.303 | 20 | 24 | fits | 119,376 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,538,242 | 15.382 | 20 | 24 | fits | 67,444 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 129,229 | 1.292 | 20 | 50 | fits | 119,376 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 613,680 | 6.137 | 20 | 50 | fits | 156,626 | 89 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 317,879 | 3.179 | 18 | 18 | fits | 189,105 | 140 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,638,009 | 16.380 | 18 | 18 | fits | 50,387 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 486,478 | 4.865 | 20 | 20 | fits | 154,258 | 83 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 131,021 | 1.310 | 20 | 200 | fits | 119,376 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 629,485 | 6.295 | 20 | 200 | fits | 154,258 | 83 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 131,933 | 1.319 | 20 | 20 | fits | 119,376 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 846,522 | 8.465 | 20 | 20 | fits | 127,322 | 52 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 135,518 | 1.355 | 20 | 24 | fits | 119,376 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,533,996 | 15.340 | 20 | 24 | fits | 67,249 | 31 | 0.698 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 134,478 | 1.345 | 20 | 50 | fits | 119,376 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 633,161 | 6.332 | 20 | 50 | fits | 154,258 | 83 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 329,803 | 3.298 | 18 | 18 | fits | 195,780 | 151 | 0.642 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,633,879 | 16.339 | 18 | 18 | fits | 50,451 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 434,017 | 4.340 | 20 | 20 | fits | 156,143 | 83 | 0.669 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 117,663 | 1.177 | 20 | 200 | fits | 119,376 | 140 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 578,454 | 5.785 | 20 | 200 | fits | 156,143 | 83 | 0.669 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 118,575 | 1.186 | 20 | 20 | fits | 119,376 | 140 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 828,915 | 8.289 | 20 | 20 | fits | 120,974 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 122,160 | 1.222 | 20 | 24 | fits | 119,376 | 140 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,484,919 | 14.849 | 20 | 24 | fits | 67,363 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 121,120 | 1.211 | 20 | 50 | fits | 119,376 | 140 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 582,130 | 5.821 | 20 | 50 | fits | 156,143 | 83 | 0.669 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 425,922 | 4.259 | 18 | 18 | fits | 183,774 | 104 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,641,208 | 16.412 | 18 | 18 | fits | 56,522 | 24 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 484,011 | 4.840 | 20 | 20 | fits | 161,170 | 89 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 128,713 | 1.287 | 20 | 200 | fits | 125,177 | 151 | 0.528 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 627,104 | 6.271 | 20 | 200 | fits | 161,170 | 89 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 129,625 | 1.296 | 20 | 20 | fits | 125,177 | 151 | 0.528 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 877,293 | 8.773 | 20 | 20 | fits | 127,595 | 57 | 0.692 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 133,210 | 1.332 | 20 | 24 | fits | 125,177 | 151 | 0.528 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,554,645 | 15.546 | 20 | 24 | fits | 75,217 | 37 | 0.720 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 132,170 | 1.322 | 20 | 50 | fits | 125,177 | 151 | 0.528 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 630,780 | 6.308 | 20 | 50 | fits | 161,170 | 89 | 0.666 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 322,839 | 3.228 | 18 | 18 | fits | 191,124 | 145 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,641,381 | 16.414 | 18 | 18 | fits | 36,914 | 15 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 436,677 | 4.367 | 20 | 20 | fits | 160,605 | 89 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 117,804 | 1.178 | 20 | 200 | fits | 118,945 | 140 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 579,018 | 5.790 | 20 | 200 | fits | 160,605 | 89 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 118,716 | 1.187 | 20 | 20 | fits | 118,945 | 140 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 795,992 | 7.960 | 20 | 20 | fits | 94,171 | 48 | 0.654 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 122,301 | 1.223 | 20 | 24 | fits | 118,945 | 140 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,487,691 | 14.877 | 20 | 24 | fits | 67,783 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 121,261 | 1.213 | 20 | 50 | fits | 118,945 | 140 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 582,694 | 5.827 | 20 | 50 | fits | 160,605 | 89 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 310,012 | 3.100 | 18 | 18 | fits | 189,206 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,649,202 | 16.492 | 18 | 18 | fits | 50,332 | 18 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 438,080 | 4.381 | 20 | 20 | fits | 156,352 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 123,053 | 1.231 | 20 | 200 | fits | 118,945 | 140 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 582,664 | 5.827 | 20 | 200 | fits | 156,352 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 123,965 | 1.240 | 20 | 20 | fits | 118,945 | 140 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 800,764 | 8.008 | 20 | 20 | fits | 122,359 | 52 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 127,550 | 1.276 | 20 | 24 | fits | 118,945 | 140 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,497,430 | 14.974 | 20 | 24 | fits | 70,650 | 37 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 126,510 | 1.265 | 20 | 50 | fits | 118,945 | 140 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 586,340 | 5.863 | 20 | 50 | fits | 156,352 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 429,923 | 4.299 | 18 | 18 | fits | 187,976 | 104 | 0.661 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,647,333 | 16.473 | 18 | 18 | fits | 50,217 | 18 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 492,940 | 4.929 | 20 | 20 | fits | 165,840 | 101 | 0.677 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 128,302 | 1.283 | 20 | 200 | fits | 118,945 | 140 | 0.508 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 636,103 | 6.361 | 20 | 200 | fits | 165,840 | 101 | 0.677 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 129,214 | 1.292 | 20 | 20 | fits | 118,945 | 140 | 0.508 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 880,296 | 8.803 | 20 | 20 | fits | 121,144 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 132,799 | 1.328 | 20 | 24 | fits | 118,945 | 140 | 0.508 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,576,492 | 15.765 | 20 | 24 | fits | 67,444 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 131,759 | 1.318 | 20 | 50 | fits | 118,945 | 140 | 0.508 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 639,779 | 6.398 | 20 | 50 | fits | 165,840 | 101 | 0.677 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 326,900 | 3.269 | 18 | 18 | fits | 195,596 | 145 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,625,872 | 16.259 | 18 | 18 | fits | 51,915 | 20 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 472,902 | 4.729 | 20 | 20 | fits | 154,589 | 83 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 125,177 | 1.252 | 20 | 200 | fits | 125,249 | 151 | 0.525 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 616,240 | 6.162 | 20 | 200 | fits | 154,589 | 83 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 126,089 | 1.261 | 20 | 20 | fits | 125,249 | 151 | 0.525 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 860,077 | 8.601 | 20 | 20 | fits | 120,971 | 46 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 129,674 | 1.297 | 20 | 24 | fits | 125,249 | 151 | 0.525 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,556,206 | 15.562 | 20 | 24 | fits | 67,363 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 128,634 | 1.286 | 20 | 50 | fits | 125,249 | 151 | 0.525 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 619,916 | 6.199 | 20 | 50 | fits | 154,589 | 83 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 318,479 | 3.185 | 18 | 18 | fits | 190,300 | 145 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,605,586 | 16.056 | 18 | 18 | fits | 51,915 | 20 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 466,028 | 4.660 | 20 | 20 | fits | 154,947 | 83 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 119,984 | 1.200 | 20 | 200 | fits | 119,444 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 609,662 | 6.097 | 20 | 200 | fits | 154,947 | 83 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 120,896 | 1.209 | 20 | 20 | fits | 119,444 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 870,273 | 8.703 | 20 | 20 | fits | 121,500 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 124,481 | 1.245 | 20 | 24 | fits | 119,444 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,562,201 | 15.622 | 20 | 24 | fits | 67,796 | 31 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 123,441 | 1.234 | 20 | 50 | fits | 119,444 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 613,338 | 6.133 | 20 | 50 | fits | 154,947 | 83 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 311,332 | 3.113 | 18 | 18 | fits | 188,346 | 140 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,611,436 | 16.114 | 18 | 18 | fits | 51,770 | 20 | 0.734 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 456,030 | 4.560 | 20 | 20 | fits | 162,739 | 95 | 0.657 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 130,482 | 1.305 | 20 | 200 | fits | 119,444 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 598,879 | 5.989 | 20 | 200 | fits | 162,739 | 95 | 0.657 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 131,394 | 1.314 | 20 | 20 | fits | 119,444 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 842,903 | 8.429 | 20 | 20 | fits | 121,084 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 134,979 | 1.350 | 20 | 24 | fits | 119,444 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,539,065 | 15.391 | 20 | 24 | fits | 67,696 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 133,939 | 1.339 | 20 | 50 | fits | 119,444 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 602,555 | 6.026 | 20 | 50 | fits | 162,739 | 95 | 0.657 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 321,830 | 3.218 | 18 | 18 | fits | 188,346 | 140 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,638,885 | 16.389 | 18 | 18 | fits | 50,387 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 444,741 | 4.447 | 20 | 20 | fits | 156,319 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 122,373 | 1.224 | 20 | 200 | fits | 119,444 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 589,354 | 5.894 | 20 | 200 | fits | 156,319 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 123,285 | 1.233 | 20 | 20 | fits | 119,444 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 833,356 | 8.334 | 20 | 20 | fits | 121,026 | 46 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 126,870 | 1.269 | 20 | 24 | fits | 119,444 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,529,636 | 15.296 | 20 | 24 | fits | 67,422 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 125,830 | 1.258 | 20 | 50 | fits | 119,444 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 593,030 | 5.930 | 20 | 50 | fits | 156,319 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 436,646 | 4.366 | 18 | 18 | fits | 183,132 | 104 | 0.665 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,629,456 | 16.295 | 18 | 18 | fits | 50,387 | 18 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 463,930 | 4.639 | 20 | 20 | fits | 154,760 | 83 | 0.662 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 117,965 | 1.180 | 20 | 200 | fits | 120,277 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 607,377 | 6.074 | 20 | 200 | fits | 154,760 | 83 | 0.662 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 118,877 | 1.189 | 20 | 20 | fits | 120,277 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 825,405 | 8.254 | 20 | 20 | fits | 122,141 | 52 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 122,462 | 1.225 | 20 | 24 | fits | 120,277 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,506,234 | 15.062 | 20 | 24 | fits | 61,438 | 38 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 121,422 | 1.214 | 20 | 50 | fits | 120,277 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 611,053 | 6.111 | 20 | 50 | fits | 154,760 | 83 | 0.662 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 309,324 | 3.093 | 18 | 18 | fits | 188,357 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,647,973 | 16.480 | 18 | 18 | fits | 36,746 | 15 | 0.768 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 468,806 | 4.688 | 20 | 20 | fits | 156,672 | 89 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 128,552 | 1.286 | 20 | 200 | fits | 119,533 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 612,088 | 6.121 | 20 | 200 | fits | 156,672 | 89 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 129,464 | 1.295 | 20 | 20 | fits | 119,533 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 863,023 | 8.630 | 20 | 20 | fits | 121,277 | 46 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 133,049 | 1.330 | 20 | 24 | fits | 119,533 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,520,907 | 15.209 | 20 | 24 | fits | 67,610 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 132,009 | 1.320 | 20 | 50 | fits | 119,533 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 615,764 | 6.158 | 20 | 50 | fits | 156,672 | 89 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 319,860 | 3.199 | 18 | 18 | fits | 188,306 | 140 | 0.632 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,664,219 | 16.642 | 18 | 18 | fits | 43,042 | 21 | 0.775 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 412,899 | 4.129 | 20 | 20 | fits | 181,264 | 89 | 0.708 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 120,443 | 1.204 | 20 | 200 | fits | 119,533 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 575,369 | 5.754 | 20 | 200 | fits | 181,264 | 89 | 0.708 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 121,355 | 1.214 | 20 | 20 | fits | 119,533 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 819,569 | 8.196 | 20 | 20 | fits | 120,782 | 46 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 124,940 | 1.249 | 20 | 24 | fits | 119,533 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,471,503 | 14.715 | 20 | 24 | fits | 74,704 | 37 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 123,900 | 1.239 | 20 | 50 | fits | 119,533 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 579,045 | 5.790 | 20 | 50 | fits | 181,264 | 89 | 0.708 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 397,716 | 3.977 | 18 | 18 | fits | 152,612 | 100 | 0.656 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,671,775 | 16.718 | 18 | 18 | fits | 50,155 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 474,421 | 4.744 | 20 | 20 | fits | 154,947 | 83 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 121,992 | 1.220 | 20 | 200 | fits | 119,609 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 618,055 | 6.181 | 20 | 200 | fits | 154,947 | 83 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 122,904 | 1.229 | 20 | 20 | fits | 119,609 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 872,214 | 8.722 | 20 | 20 | fits | 124,418 | 52 | 0.694 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 126,489 | 1.265 | 20 | 24 | fits | 119,609 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,553,089 | 15.531 | 20 | 24 | fits | 61,416 | 38 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 125,449 | 1.254 | 20 | 50 | fits | 119,609 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 621,731 | 6.217 | 20 | 50 | fits | 154,947 | 83 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 319,725 | 3.197 | 18 | 18 | fits | 194,731 | 145 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,644,326 | 16.443 | 18 | 18 | fits | 36,998 | 15 | 0.778 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 478,010 | 4.780 | 20 | 20 | fits | 154,381 | 83 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 122,514 | 1.225 | 20 | 200 | fits | 119,194 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 621,140 | 6.211 | 20 | 200 | fits | 154,381 | 83 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 123,426 | 1.234 | 20 | 20 | fits | 119,194 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 865,049 | 8.650 | 20 | 20 | fits | 121,031 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 127,011 | 1.270 | 20 | 24 | fits | 119,194 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,596,277 | 15.963 | 20 | 24 | fits | 101,497 | 45 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 125,971 | 1.260 | 20 | 50 | fits | 119,194 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 624,816 | 6.248 | 20 | 50 | fits | 154,381 | 83 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 321,258 | 3.213 | 18 | 18 | fits | 195,742 | 151 | 0.643 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,645,795 | 16.458 | 18 | 18 | fits | 52,053 | 20 | 0.741 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 444,035 | 4.440 | 20 | 20 | fits | 156,266 | 83 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 127,763 | 1.278 | 20 | 200 | fits | 119,194 | 140 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 588,595 | 5.886 | 20 | 200 | fits | 156,266 | 83 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 128,675 | 1.287 | 20 | 20 | fits | 119,194 | 140 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 799,625 | 7.996 | 20 | 20 | fits | 88,164 | 37 | 0.637 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 132,260 | 1.323 | 20 | 24 | fits | 119,194 | 140 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,467,167 | 14.672 | 20 | 24 | fits | 35,362 | 22 | 0.644 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 131,220 | 1.312 | 20 | 50 | fits | 119,194 | 140 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 592,271 | 5.923 | 20 | 50 | fits | 156,266 | 83 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 435,940 | 4.359 | 18 | 18 | fits | 183,766 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,701,985 | 17.020 | 18 | 18 | fits | 50,155 | 18 | 0.707 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 468,686 | 4.687 | 20 | 20 | fits | 154,589 | 83 | 0.660 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 120,255 | 1.203 | 20 | 200 | fits | 125,044 | 151 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 612,024 | 6.120 | 20 | 200 | fits | 154,589 | 83 | 0.660 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 121,167 | 1.212 | 20 | 20 | fits | 125,044 | 151 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 855,875 | 8.559 | 20 | 20 | fits | 114,371 | 53 | 0.710 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 124,752 | 1.248 | 20 | 24 | fits | 125,044 | 151 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,541,364 | 15.414 | 20 | 24 | fits | 100,643 | 45 | 0.737 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 123,712 | 1.237 | 20 | 50 | fits | 125,044 | 151 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 615,700 | 6.157 | 20 | 50 | fits | 154,589 | 83 | 0.660 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 314,263 | 3.143 | 18 | 18 | fits | 191,006 | 145 | 0.633 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,695,709 | 16.957 | 18 | 18 | fits | 46,640 | 27 | 0.796 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 475,641 | 4.756 | 20 | 20 | fits | 120,483 | 74 | 0.622 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 129,187 | 1.292 | 20 | 200 | fits | 119,319 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 584,811 | 5.848 | 20 | 200 | fits | 120,483 | 74 | 0.622 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 130,099 | 1.301 | 20 | 20 | fits | 119,319 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 844,520 | 8.445 | 20 | 20 | fits | 124,408 | 52 | 0.694 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 133,684 | 1.337 | 20 | 24 | fits | 119,319 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,531,702 | 15.317 | 20 | 24 | fits | 107,053 | 56 | 0.745 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 132,644 | 1.326 | 20 | 50 | fits | 119,319 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 588,487 | 5.885 | 20 | 50 | fits | 120,483 | 74 | 0.622 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 321,022 | 3.210 | 18 | 18 | fits | 188,833 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,692,257 | 16.923 | 18 | 18 | fits | 50,156 | 18 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 434,272 | 4.343 | 20 | 20 | fits | 160,651 | 89 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 115,829 | 1.158 | 20 | 200 | fits | 119,319 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 576,659 | 5.767 | 20 | 200 | fits | 160,651 | 89 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 116,741 | 1.167 | 20 | 20 | fits | 119,319 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 831,984 | 8.320 | 20 | 20 | fits | 121,339 | 46 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 120,326 | 1.203 | 20 | 24 | fits | 119,319 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,561,130 | 15.611 | 20 | 24 | fits | 68,014 | 31 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 119,286 | 1.193 | 20 | 50 | fits | 119,319 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 580,335 | 5.803 | 20 | 50 | fits | 160,651 | 89 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 307,664 | 3.077 | 18 | 18 | fits | 188,833 | 140 | 0.630 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,660,721 | 16.607 | 18 | 18 | fits | 50,334 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 473,871 | 4.739 | 20 | 20 | fits | 166,968 | 101 | 0.682 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 121,078 | 1.211 | 20 | 200 | fits | 119,319 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 617,926 | 6.179 | 20 | 200 | fits | 166,968 | 101 | 0.682 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 121,990 | 1.220 | 20 | 20 | fits | 119,319 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 862,217 | 8.622 | 20 | 20 | fits | 121,198 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 125,575 | 1.256 | 20 | 24 | fits | 119,319 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,579,381 | 15.794 | 20 | 24 | fits | 101,362 | 45 | 0.744 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 124,535 | 1.245 | 20 | 50 | fits | 119,319 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 621,602 | 6.216 | 20 | 50 | fits | 166,968 | 101 | 0.682 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 282,652 | 2.827 | 18 | 18 | fits | 158,572 | 136 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,679,162 | 16.792 | 18 | 18 | fits | 50,284 | 18 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 490,409 | 4.904 | 20 | 20 | fits | 154,924 | 83 | 0.663 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 126,327 | 1.263 | 20 | 200 | fits | 119,319 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 633,980 | 6.340 | 20 | 200 | fits | 154,924 | 83 | 0.663 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 127,239 | 1.272 | 20 | 20 | fits | 119,319 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 878,112 | 8.781 | 20 | 20 | fits | 121,144 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 130,824 | 1.308 | 20 | 24 | fits | 119,319 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,540,239 | 15.402 | 20 | 24 | fits | 35,316 | 22 | 0.641 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 129,784 | 1.298 | 20 | 50 | fits | 119,319 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 637,656 | 6.377 | 20 | 50 | fits | 154,924 | 83 | 0.663 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 324,714 | 3.247 | 18 | 18 | fits | 195,385 | 145 | 0.629 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,674,766 | 16.748 | 18 | 18 | fits | 50,712 | 18 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 434,500 | 4.345 | 20 | 20 | fits | 156,453 | 83 | 0.671 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 117,538 | 1.175 | 20 | 200 | fits | 123,888 | 140 | 0.510 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 579,247 | 5.792 | 20 | 200 | fits | 156,453 | 83 | 0.671 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 118,450 | 1.185 | 20 | 20 | fits | 123,888 | 140 | 0.510 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 823,400 | 8.234 | 20 | 20 | fits | 121,100 | 46 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 122,035 | 1.220 | 20 | 24 | fits | 123,888 | 140 | 0.510 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,517,639 | 15.176 | 20 | 24 | fits | 67,358 | 31 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 120,995 | 1.210 | 20 | 50 | fits | 123,888 | 140 | 0.510 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 582,923 | 5.829 | 20 | 50 | fits | 156,453 | 83 | 0.671 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 426,405 | 4.264 | 18 | 18 | fits | 183,824 | 104 | 0.663 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,651,864 | 16.519 | 18 | 18 | fits | 50,594 | 18 | 0.723 |
| LINK_UP | `adp.link_up.if0` | 2,010 | 0.020 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| LINK_UP | `adp.link_up.if1` | 15,566 | 0.156 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,565 | 0.236 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 16,446 | 0.164 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 18,207 | 0.182 | 20 | 200 | fits | 3,932 | 18 (11) | 0.355 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 16,363 | 0.164 | 20 | 200 | fits | 3,932 | 18 (11) | 0.355 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 13,309 | 0.133 | 20 | 50 | fits | 119,266 | 50 | 0.695 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 22,581 | 0.226 | 20 | 50 | fits | 28,954 | 38 | 0.575 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 17,520 | 0.175 | 20 | 50 | fits | 28,634 | 38 | 0.545 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 17,390 | 0.174 | 20 | 50 | fits | 34,827 | 65 | 0.507 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 19,267 | 0.193 | 20 | 50 | fits | 34,827 | 65 | 0.507 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,531 | 0.115 | 20 | 50 | fits | 27,436 | 33 | 0.450 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 12,416 | 0.124 | 20 | 50 | fits | 112,123 | 50 | 0.623 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 18,329 | 0.183 | 20 | 50 | fits | 30,137 | 38 | 0.575 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 15,384 | 0.154 | 20 | 50 | fits | 29,450 | 38 | 0.518 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 15,609 | 0.156 | 20 | 50 | fits | 36,410 | 65 | 0.528 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 17,721 | 0.177 | 20 | 50 | fits | 36,410 | 65 | 0.528 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 11,721 | 0.117 | 20 | 50 | fits | 28,789 | 33 | 0.436 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 35,533 | 0.355 | 20 | 20 | fits | 52,046 | 30 (35) | 0.738 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 24,824 | 0.248 | 20 | 20 | fits | 48,589 | 24 (35) | 0.729 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 16,040 | 0.160 | 20 | 20 | fits | 58,547 | 46 (14) | 0.718 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 12,351 | 0.124 | 20 | 20 | fits | 43,042 | 19 (14) | 0.802 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 16,888 | 0.169 | 20 | 20 | fits | 58,285 | 47 (14) | 0.714 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 12,582 | 0.126 | 20 | 20 | fits | 41,871 | 19 (14) | 0.786 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 50,140 | 0.501 | 20 | 20 | fits | 51,172 | 24 (35) | 0.766 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 41,150 | 0.411 | 20 | 20 | fits | 64,355 | 51 (35) | 0.712 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 154,836 | 1.548 | 18 | 18 | fits | 46,054 | 14 | 0.821 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 148,123 | 1.481 | 18 | 18 | fits | 45,472 | 14 | 0.811 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 59,805 | 0.598 | 18 | 18 | fits | 59,870 | 15 | 0.880 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,849 | 0.248 | 18 | 18 | fits | 24,914 | 15 | 0.435 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 174,909 | 1.749 | 218 | 218 | fits | 190,478 | 22 | 0.799 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 52,408 | 0.524 | 18 | 18 | fits | 52,473 | 15 | 0.860 |
| malformed MRPDU discard | `srp.malformed.if1` | 24,577 | 0.246 | 18 | 18 | fits | 24,642 | 15 | 0.435 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 153,263 | 1.533 | 218 | 218 | fits | 166,514 | 22 | 0.799 |
| an event behind 15 others | `backlog.event.if0` | 146,726 | 1.467 | 20 | 200 | fits | 116,547 | 125 | 0.538 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 663,614 | 6.636 | 20 | 20 | fits | 109,867 | 52 | 0.674 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 135,954 | 1.360 | 20 | 200 | fits | 136,162 | 143 | 0.528 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 540,108 | 5.401 | 20 | 200 | fits | 130,833 | 57 | 0.696 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 131,695 | 1.317 | 20 | 20 | fits | 136,162 | 143 | 0.528 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 730,436 | 7.304 | 20 | 20 | fits | 109,867 | 52 | 0.674 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 135,280 | 1.353 | 20 | 24 | fits | 136,162 | 143 | 0.528 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,250,905 | 12.509 | 20 | 24 | fits | 51,616 | 31 | 0.688 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 134,240 | 1.342 | 20 | 50 | fits | 136,162 | 143 | 0.528 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 538,613 | 5.386 | 20 | 50 | fits | 130,833 | 57 | 0.696 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 538,548 | 5.385 | 18 | 18 | fits | 130,833 | 57 | 0.696 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,388,120 | 13.881 | 18 | 18 | fits | 34,410 | 18 | 0.678 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 361,759 | 3.618 | 20 | 20 | fits | 196,985 | 89 | 0.703 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 112,346 | 1.123 | 20 | 200 | fits | 117,028 | 140 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 541,444 | 5.414 | 20 | 200 | fits | 196,985 | 89 | 0.703 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 113,258 | 1.133 | 20 | 20 | fits | 117,028 | 140 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 786,777 | 7.868 | 20 | 20 | fits | 121,001 | 46 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 116,843 | 1.168 | 20 | 24 | fits | 117,028 | 140 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,483,396 | 14.834 | 20 | 24 | fits | 67,417 | 31 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 115,803 | 1.158 | 20 | 50 | fits | 117,028 | 140 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 545,120 | 5.451 | 20 | 50 | fits | 196,985 | 89 | 0.703 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 545,055 | 5.451 | 18 | 18 | fits | 196,985 | 89 | 0.703 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,633,415 | 16.334 | 18 | 18 | fits | 50,209 | 18 | 0.709 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 10,727 | 0.107 | 20 | 20 | fits | 44,989 | 21 | 0.763 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 112,346 | 1.123 | 20 | 200 | fits | 117,028 | 140 | 0.499 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 46,868 | 0.469 | 20 | 200 | fits | 44,989 | 21 | 0.763 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 113,258 | 1.133 | 20 | 20 | fits | 117,028 | 140 | 0.499 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 767,676 | 7.677 | 20 | 20 | fits | 121,023 | 46 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 116,843 | 1.168 | 20 | 24 | fits | 117,028 | 140 | 0.499 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,435,244 | 14.352 | 20 | 24 | fits | 67,757 | 31 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 115,803 | 1.158 | 20 | 50 | fits | 117,028 | 140 | 0.499 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 525,930 | 5.259 | 20 | 50 | fits | 177,795 | 79 | 0.707 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 525,865 | 5.259 | 18 | 18 | fits | 177,795 | 79 | 0.707 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,635,442 | 16.354 | 18 | 18 | fits | 50,150 | 18 | 0.707 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,377,719 | 63.777 | 20 | 20 | MISS ceiling | 50,318 | 27 | 0.562 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,086,607 | 360.866 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,086,532 | 360.865 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,086,457 | 360.865 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,086,382 | 360.864 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 118,156 | 1.182 | 20 | 200 | fits | 112,981 | 134 | 0.500 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 584,588 | 5.846 | 20 | 200 | fits | 132,287 | 69 | 0.669 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 113,897 | 1.139 | 20 | 20 | fits | 112,981 | 134 | 0.500 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 784,845 | 7.848 | 20 | 20 | fits | 100,268 | 35 | 0.739 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 117,482 | 1.175 | 20 | 24 | fits | 112,981 | 134 | 0.500 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,513,453 | 65.135 | 20 | 24 | MISS ceiling | 31,887 | 23 | 0.532 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 116,442 | 1.164 | 20 | 50 | fits | 112,981 | 134 | 0.500 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 583,093 | 5.831 | 20 | 50 | fits | 132,287 | 69 | 0.669 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 307,310 | 3.073 | 18 | 18 | fits | 191,323 | 138 | 0.646 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,333,470 | 13.335 | 18 | 18 | fits | 49,086 | 21 | 0.664 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,701 | 0.067 | 20 | 20 | fits | 61,057 | 19 (29) | 0.702 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 25,540 | 0.255 | 20 | 20 | fits | 61,057 | 19 (29) | 0.702 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,686 | 0.077 | 20 | 20 | fits | 63,083 | 30 (35) | 0.675 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 27,082 | 0.271 | 20 | 20 | fits | 63,083 | 30 (35) | 0.675 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 9,916 | 0.099 | 20 | 20 | fits | 64,261 | 26 (12) | 0.796 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 41,409 | 0.414 | 20 | 20 | fits | 53,287 | 30 (12) | 0.747 |
| LINK_UP | `adp.link_up.if0` | 2,010 | 0.020 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| LINK_UP | `adp.link_up.if1` | 15,566 | 0.156 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,565 | 0.236 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 16,446 | 0.164 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| LINK_DOWN | `adp.link_down.if0` | 1,815 | 0.018 | 20 | 200 | fits | 60,887 | 38 (9) | 0.646 |
| LINK_DOWN | `adp.link_down.if1` | 29,629 | 0.296 | 20 | 200 | fits | 60,887 | 38 (9) | 0.646 |
| LINK_UP | `adp.link_up.if0` | 2,010 | 0.020 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| LINK_UP | `adp.link_up.if1` | 15,566 | 0.156 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,565 | 0.236 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 16,446 | 0.164 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| GM_CHANGE | `adp.gm_change.if0` | 1,784 | 0.018 | 20 | 200 | fits | 20,421 | 28 (11) | 0.231 |
| GM_CHANGE | `adp.gm_change.if1` | 3,235 | 0.032 | 20 | 200 | fits | 20,421 | 28 (11) | 0.231 |
| LINK_UP | `adp.link_up.if0` | 2,010 | 0.020 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| LINK_UP | `adp.link_up.if1` | 15,566 | 0.156 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,565 | 0.236 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 16,446 | 0.164 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 3,297 | 0.033 | 20 | 200 | fits | 22,190 | 25 (31) | 0.343 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 4,690 | 0.047 | 20 | 200 | fits | 22,190 | 25 (31) | 0.343 |
| LINK_UP | `adp.link_up.if0` | 2,010 | 0.020 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| LINK_UP | `adp.link_up.if1` | 15,566 | 0.156 | 20 | 200 | fits | 130,958 | 86 (11) | 0.636 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 23,565 | 0.236 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 16,446 | 0.164 | 20 | 200 | fits | 33,938 | 42 (39) | 0.423 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 3,297 | 0.033 | 20 | 200 | fits | 20,795 | 18 (31) | 0.453 |
| set_name | `aecp_fanout.set_name.if0` | 84,489 | 0.845 | 20 | 24 | fits | 102,936 | 225 | 0.204 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 85,416 | 0.854 | 20 | 24 | fits | 88,335 | 205 | 0.223 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 83,723 | 0.837 | 20 | 24 | fits | 84,936 | 205 | 0.203 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 70,690 | 0.707 | 20 | 24 | fits | 84,248 | 205 | 0.194 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 82,345 | 0.823 | 20 | 24 | fits | 85,104 | 181 | 0.210 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 84,183 | 0.842 | 20 | 24 | fits | 85,351 | 205 | 0.204 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 71,772 | 0.718 | 20 | 24 | fits | 84,978 | 205 | 0.195 |
| set_name | `aecp_fanout.set_name.if1` | 98,925 | 0.989 | 20 | 24 | fits | 101,815 | 187 | 0.196 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 85,624 | 0.856 | 20 | 24 | fits | 88,518 | 205 | 0.224 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 71,179 | 0.712 | 20 | 24 | fits | 84,648 | 205 | 0.200 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 68,568 | 0.686 | 20 | 24 | fits | 84,448 | 205 | 0.195 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 83,060 | 0.831 | 20 | 24 | fits | 84,092 | 205 | 0.177 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 71,776 | 0.718 | 20 | 24 | fits | 84,946 | 205 | 0.194 |
| BIND_RX | `acmp.bind_rx.if0` | 26,077 | 0.261 | 20 | 20 | fits | 66,201 | 30 (77) | 0.757 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 18,220 | 0.182 | 20 | 20 | fits | 57,412 | 39 (32) | 0.785 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,859 | 0.119 | 20 | 20 | fits | 48,814 | 18 (47) | 0.726 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 16,655 | 0.167 | 20 | 20 | fits | 60,086 | 21 (50) | 0.827 |
| PROBE_TX | `acmp.probe_tx.if0` | 12,260 | 0.123 | 20 | 20 | fits | 47,562 | 20 (48) | 0.718 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 19,402 | 0.194 | 20 | 20 | fits | 53,845 | 25 (48) | 0.695 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 11,983 | 0.120 | 20 | 20 | fits | 47,012 | 19 (48) | 0.725 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 11,011 | 0.110 | 20 | 20 | fits | 45,362 | 19 (48) | 0.667 |
| BIND_RX | `acmp.bind_rx.if1` | 22,144 | 0.221 | 20 | 20 | fits | 60,746 | 31 (77) | 0.712 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 8,791 | 0.088 | 20 | 20 | fits | 47,717 | 22 (32) | 0.800 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 22,955 | 0.230 | 20 | 20 | fits | 61,875 | 37 (47) | 0.740 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 16,074 | 0.161 | 20 | 20 | fits | 59,802 | 22 (50) | 0.808 |
| PROBE_TX | `acmp.probe_tx.if1` | 19,727 | 0.197 | 20 | 20 | fits | 56,387 | 27 (48) | 0.722 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 12,721 | 0.127 | 20 | 20 | fits | 48,047 | 20 (48) | 0.722 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 10,998 | 0.110 | 20 | 20 | fits | 45,977 | 20 (48) | 0.658 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 10,979 | 0.110 | 20 | 20 | fits | 45,958 | 20 (48) | 0.658 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 32,929 | 0.329 | 20 | 24 | fits | 30,670 | 24 | 0.697 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 30,268 | 0.303 | 20 | 24 | fits | 34,547 | 24 | 0.614 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 26,265 | 0.263 | 20 | 24 | fits | 30,596 | 24 | 0.630 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,722 | 0.167 | 20 | 24 | fits | 29,811 | 24 | 0.562 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 25,676 | 0.257 | 20 | 24 | fits | 30,274 | 24 | 0.595 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 17,222 | 0.172 | 20 | 24 | fits | 30,350 | 24 | 0.574 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 25,279 | 0.253 | 20 | 24 | fits | 29,456 | 24 | 0.605 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 15,910 | 0.159 | 20 | 24 | fits | 28,998 | 23 | 0.579 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 16,839 | 0.168 | 20 | 24 | fits | 29,967 | 24 | 0.623 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 30,661 | 0.307 | 20 | 24 | fits | 35,256 | 24 | 0.531 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 15,818 | 0.158 | 20 | 24 | fits | 28,803 | 24 | 0.606 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 25,064 | 0.251 | 20 | 24 | fits | 29,360 | 24 | 0.639 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 15,907 | 0.159 | 20 | 24 | fits | 28,917 | 24 | 0.574 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 17,444 | 0.174 | 20 | 24 | fits | 30,572 | 24 | 0.613 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 25,744 | 0.257 | 20 | 24 | fits | 30,213 | 24 | 0.618 |
| get_configuration | `aecp.get_configuration.if0` | 14,285 | 0.143 | 20 | 24 | fits | 27,334 | 24 | 0.574 |
| entity_available | `aecp.entity_available.if0` | 23,839 | 0.238 | 20 | 24 | fits | 28,182 | 24 | 0.598 |
| get_name | `aecp.get_name.if0` | 16,687 | 0.167 | 20 | 24 | fits | 30,180 | 24 | 0.638 |
| get_counters | `aecp.get_counters.if0` | 18,274 | 0.183 | 20 | 24 | fits | 32,072 | 31 | 0.636 |
| get_avb_info | `aecp.get_avb_info.if0` | 24,889 | 0.249 | 20 | 24 | fits | 29,410 | 24 | 0.661 |
| unknown_command | `aecp.unknown_command.if0` | 32,530 | 0.325 | 20 | 24 | fits | 28,463 | 24 | 0.642 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 24,219 | 0.242 | 20 | 24 | fits | 28,843 | 24 | 0.645 |
| set_name | `aecp.set_name.if0` | 47,002 | 0.470 | 20 | 24 | fits | 53,559 | 70 | 0.581 |
| lock_entity | `aecp.lock_entity.if0` | 39,952 | 0.400 | 20 | 24 | fits | 41,604 | 50 | 0.630 |
| unlock_entity | `aecp.unlock_entity.if0` | 31,438 | 0.314 | 20 | 24 | fits | 40,923 | 50 | 0.618 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 32,340 | 0.323 | 20 | 24 | fits | 28,142 | 22 | 0.568 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 30,900 | 0.309 | 20 | 24 | fits | 33,266 | 22 | 0.596 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 25,483 | 0.255 | 20 | 24 | fits | 30,458 | 22 | 0.631 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 18,089 | 0.181 | 20 | 24 | fits | 29,576 | 22 | 0.561 |
| get_configuration | `aecp.get_configuration.if1` | 24,937 | 0.249 | 20 | 24 | fits | 27,675 | 22 | 0.610 |
| entity_available | `aecp.entity_available.if1` | 15,984 | 0.160 | 20 | 24 | fits | 27,322 | 22 | 0.549 |
| get_name | `aecp.get_name.if1` | 27,536 | 0.275 | 20 | 24 | fits | 30,546 | 22 | 0.667 |
| get_counters | `aecp.get_counters.if1` | 18,945 | 0.189 | 20 | 24 | fits | 30,933 | 29 | 0.606 |
| get_avb_info | `aecp.get_avb_info.if1` | 17,239 | 0.172 | 20 | 24 | fits | 28,893 | 22 | 0.655 |
| unknown_command | `aecp.unknown_command.if1` | 25,057 | 0.251 | 20 | 24 | fits | 27,807 | 22 | 0.620 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 16,083 | 0.161 | 20 | 24 | fits | 27,650 | 22 | 0.598 |
| set_name | `aecp.set_name.if1` | 36,224 | 0.362 | 20 | 24 | fits | 48,151 | 31 | 0.607 |
| lock_entity | `aecp.lock_entity.if1` | 23,255 | 0.233 | 20 | 24 | fits | 41,857 | 55 | 0.562 |
| unlock_entity | `aecp.unlock_entity.if1` | 24,130 | 0.241 | 20 | 24 | fits | 42,161 | 55 | 0.572 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
